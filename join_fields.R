#Verifying, installing and loading libraries
list.of.packages = c("rgdal","rstudioapi","doParallel","arcgisbinding","foreign")
new.packages = list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages))install.packages(new.packages)
for(j in list.of.packages){library(j,character.only=T)}

join_fields_shp=function(paths_shp,paths_join,field_shp,field_join,new_field_shp,calculate_field_join,n_cores){
  #paths_shp: character con las rutas para leer las capas
  #fields: df o matrix donde la primera columna sea el nombre actual de la capa y la segunda el nombre nuevo que se le quiere dar
  cl=makeCluster(n_cores,type="PSOCK")
  registerDoParallel(cl,n_cores)
  foreach(i=1:length(paths_shp),.inorder=F,.packages=c("foreign"),.errorhandling="pass") %dopar% {
    shp=read.dbf(sub(".shp",".dbf",paths_shp[i]))
    if(field_shp[i]=="FID"){
      shp$abcdefghijk=0:(nrow(shp))-1
    }
    else if (field_shp[i]=="OBJECTID"){
      shp$abcdefghijk=1:nrow(shp)
    }
    else{
      shp$abcdefghijk=shp[,colnames(shp)==field_shp[i]]
    }
    join_tab=read.dbf(paths_join[i])
    rows_shp=which(shp$abcdefghijk %in% join_tab[,colnames(join_tab)==field_join[i]])
    if (length(rows_shp) == nrow(join_tab)){
      shp=shp[,-ncol(shp)]
      shp$new=-9999
      shp$new[rows_shp]=join_tab[,which(colnames(join_tab)==calculate_field_join[i])]
      colnames(shp)[ncol(shp)]=new_field_shp[i]
      write.dbf(shp,sub(".shp",".dbf",paths_shp[i]))
    } 
    else{
      write.table("Error. Not all features in join table were in the shape attributes table",
                  sub(".shp","_ERROR.txt",paths_shp[i]),row.names=F,col.names=F,quote=F)
    }
  }
}
