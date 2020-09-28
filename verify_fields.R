#Verifying, installing and loading libraries
list.of.packages = c("rgdal","rstudioapi","doParallel","arcgisbinding","foreign")
new.packages = list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages))install.packages(new.packages)
for(i in list.of.packages){library(i,character.only=T)}

verify_fields_gdb_write=function(paths,fields,n_cores){
  #paths: character con las rutas para leer las capas
  #fields: df o matrix donde la primera columna sea el nombre actual de la capa y la segunda el nombre nuevo que se le quiere dar
  cl=makeCluster(n_cores,type="PSOCK")
  registerDoParallel(cl,n_cores)
  foreach(i=1:length(paths),.inorder=F,.packages=c("rgdal"),.errorhandling="pass") %dopar%{
    pos=gregexpr("\\",paths[i],fixed=T)[[1]]
    pos=pos[length(pos)]
    dsn=substr(paths[i],1,pos-1)
    layer=substr(paths[i],pos+1,nchar(paths[i]))
    shp=readOGR(dsn=dsn,layer=layer,encoding="UTF-8",use_iconv=T)
    nms=fields[which(as.character(fields[,1]) %in% colnames(shp@data)),]
    colnames(shp@data)[which(colnames(shp@data) %in% as.character(fields[,1]))]=
      as.character(nms[match(colnames(shp@data),nms[,1],nomatch=0),2])
    arc.check_product()
    arc.write(paths[i],shp,overwrite=T,validate=T)
  }
}

verify_fields_shp=function(paths,fields,n_cores){
  #paths: character con las rutas para leer las capas
  #fields: df o matrix donde la primera columna sea el nombre actual de la capa y la segunda el nombre nuevo que se le quiere dar
  cl=makeCluster(n_cores,type="PSOCK")
  registerDoParallel(cl,n_cores)
  foreach(i=1:length(paths),.inorder=F,.packages=c("foreign"),.errorhandling="pass") %dopar%{
    shp=read.dbf(sub(".shp",".dbf",paths[i]))
    nms=fields[which(as.character(fields[,1]) %in% colnames(shp)),]
    colnames(shp)[which(colnames(shp) %in% as.character(fields[,1]))]=
      as.character(nms[match(colnames(shp),nms[,1],nomatch=0),2])
    write.dbf(shp,sub(".shp",".dbf",paths[i]))
  }
}

verify_fields_list_object=function(sp_object,fields){
  #sp_objec: spatial object
  #fields: desired order of fields for the layer. They are expected to have the same names that those on the layer.
  #        Fields that do not match will be discarded.
  sp_object@data=sp_object@data[,which(names(sp_object) %in% fields)]
  match_names=match(fields,names(sp_object),nomatch=0)
  match_names=match_names[-which(match_names==0)]
  sp_object@data=sp_object@data[,match_names]
  return(sp_object)
}