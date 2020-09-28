#Verifying, installing and loading libraries
list.of.packages = c("rgdal","rstudioapi","doParallel","arcgisbinding","raster")
new.packages = list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages))install.packages(new.packages)
for(i in list.of.packages){library(i,character.only=T)}

calculate_area_gdb_write=function(paths,n_cores){
  #paths: character con las rutas para leer las capas
  cl=makeCluster(n_cores,type="PSOCK")
  registerDoParallel(cl,n_cores)
  foreach(i=1:length(paths),.inorder=F,.packages=c("rgdal","raster"),.errorhandling="pass") %dopar%{
    pos=gregexpr("\\",paths[i],fixed=T)[[1]]
    pos=pos[length(pos)]
    dsn=substr(paths[i],1,pos-1)
    layer=substr(paths[i],pos+1,nchar(paths[i]))
    shp=readOGR(dsn=dsn,layer=layer,encoding="UTF-8",use_iconv=T)
    #slot(shp@polygons[[1]],"area")
    shp$area_ha=area(shp)/10000
    arc.check_product()
    arc.write(paths[i],shp,overwrite=T,validate=T)
  }
}

calculate_area_shp_write=function(paths,n_cores){
  #paths: character con las rutas para leer las capas
  cl=makeCluster(n_cores,type="PSOCK")
  registerDoParallel(cl,n_cores)
  foreach(i=1:length(paths),.inorder=F,.packages=c("rgdal","raster"),.errorhandling="pass") %dopar%{
    pos=gregexpr("\\",paths[i],fixed=T)[[1]]
    pos=pos[length(pos)]
    dsn=substr(paths[i],1,pos-1)
    layer=substr(paths[i],pos+1,nchar(paths[i])-4)
    shp=readOGR(paths[i],encoding="UTF-8",use_iconv=T)
    #slot(shp@polygons[[1]],"area")
    shp$area_ha=area(shp)/10000
    writeOGR(shp,dsn,layer,driver="ESRI Shapefile",overwrite_layer=T)
    gc()
  }
}

calculate_area_list_object=function(paths,n_cores){
  #paths: character con las rutas para leer las capas
  cl=makeCluster(n_cores,type="PSOCK")
  registerDoParallel(cl,n_cores)
  results=foreach(i=1:length(paths),.inorder=F,.packages=c("rgdal","raster"),.errorhandling="pass") %dopar%{
    pos=gregexpr("\\",paths[i],fixed=T)[[1]]
    pos=pos[length(pos)]
    dsn=substr(paths[i],1,pos-1)
    layer=substr(paths[i],pos+1,nchar(paths[i]))
    shp=readOGR(dsn=dsn,layer=layer,encoding="UTF-8",use_iconv=T)
    #slot(shp@polygons[[1]],"area")
    shp$area_ha=area(shp)/10000
    return(shp)
  }
  return(results)
}