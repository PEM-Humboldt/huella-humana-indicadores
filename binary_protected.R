#Verifying, installing and loading libraries
list.of.packages = c("rgdal","rstudioapi","doParallel","foreign")
new.packages = list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages))install.packages(new.packages)
for(j in list.of.packages){library(j,character.only=T)}

binary_protected_shp=function(paths_shp,n_cores){
  #paths_shp: character con las rutas para leer las capas
  cl=makeCluster(n_cores,type="PSOCK")
  registerDoParallel(cl,n_cores)
  foreach(i=1:length(paths_shp),.inorder=F,.packages=c("foreign"),.errorhandling="pass") %dopar% {
    shp=read.dbf(sub(".shp",".dbf",paths_shp[i]))
    aps_fields=c("anu","dcs","dnmi","drmi","pnn","pnr","rfpn","rfpr",
                 "rn","rnsc","sfa","sff","sfl","vp","ar")
    match_names=match(colnames(shp),aps_fields,nomatch=0)
    match_names=match_names[-which(match_names==0)]
    if (length(aps_fields)>length(match_names)){
      no_match=aps_fields[!(aps_fields %in% colnames(shp))]
      write.table(paste0("Error. The field(s) ",paste(no_match,collapse=", "),", could not be found in your layer"),
                  sub(".shp","_ERROR.txt",paths_shp[i]),row.names=F,col.names=F,quote=F)
    }
    else{
      binary_protected=shp[,match_names]
      binary_protected[binary_protected>0]=1
      shp$binary_p=apply(binary_protected,1,function(x){paste(x,collapse="")})
      write.dbf(shp,sub(".shp",".dbf",paths_shp[i]))
    }
  }
}
