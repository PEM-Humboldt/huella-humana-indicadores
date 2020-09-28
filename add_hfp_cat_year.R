#Verifying, installing and loading libraries

list.of.packages = c("foreign","doParallel")
new.packages = list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages))install.packages(new.packages)
for(i in list.of.packages){library(i,character.only=T)}
source(paste0(dirname(rstudioapi::getSourceEditorContext()$path),"/defing_groups_for_parallelizing.R"))

#Create hfp_cat and year_hfp fields in hfp classes shapes
add_hfp_cat_year=function(x,n_cores){
  #x: vector con las rutas para leer las capas fuente
  #n_cores: número de núcleos para paralelizar
  groups=groups_for_parallelizing(length(x),n_cores)
  cl=makeCluster(n_cores,type="PSOCK")
  registerDoParallel(cl,n_cores)
  foreach(i=1:length(groups),.inorder=F,.combine=rbind,.packages=c("foreign"),.errorhandling="pass") %dopar%{
    sources=sub(".shp",".dbf",x[groups[[i]]])
    shp=read.dbf(sources)
    old=unique(sort(shp$gridcode))
    new=as.character(c("Natural","Baja","Media","Alta"))
    shp$CLASE=new[match(shp$gridcode,old,nomatch=0)]
    shp$year_hfp=as.integer(substr(sources,nchar(sources)-7,nchar(sources)-4))
    write.dbf(shp,sources)
  }
  stopImplicitCluster()
}