#Verifying, installing and loading libraries
list.of.packages = c("foreign")
new.packages = list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages))install.packages(new.packages)
for(i in list.of.packages){library(i,character.only=T)}

#Create hfp_pers field in hfp persistences shape
add_hfp_pers=function(x){
  #x: caracter con las ruta para leer la capa fuente
  sources=sub(".shp",".dbf",x)
  shp=read.dbf(sources)
  old=unique(sort(shp[,2]))
  new=as.character(c("Dinámicas","Estables naturales","Estables altas"))
  shp$CLASE=new[match(shp[,2],old,nomatch=0)]
  write.dbf(shp,sources)
}