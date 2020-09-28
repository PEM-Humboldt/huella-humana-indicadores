library(rgdal)

merge_list_object=function(paths){
  #paths: character con las rutas para leer las capas
  shp=readOGR(paths[1],encoding="UTF-8",use_iconv=T)
  for (i in 2:length(paths)){
    pol=readOGR(paths[i],encoding="UTF-8",use_iconv=T)
    shp=rbind(shp,pol)
    gc()
  }
  return(shp)
}


