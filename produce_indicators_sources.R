#Verifying, installing and loading libraries

list.of.packages = c("sp","rgdal","doParallel")
new.packages = list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages))install.packages(new.packages)
for(i in list.of.packages){library(i,character.only=T)}
source(paste0(dirname(rstudioapi::getSourceEditorContext()$path),"/defing_groups_for_parallelizing.R"))

#Prepare the source layers for calculating indicators

produce_indicators_sources=function(x,n_cores){
  #Orden necesario de las columnas:
  #1.Capa Base Indicador
  #2.Capa Fuente
  #3.Codigo Capa Base Indicador
  #4.Codigo Fuente
  #5.Campos Capa Base Indicador
  #6.Campos Capa Fuente
  indicators=sort(unique(as.character(x[,1])))
  #Migrating to GRASS by paralellizing
  groups=groups_for_parallelizing(length(indicators),n_cores)
  cl=makeCluster(n_cores,type="PSOCK")
  registerDoParallel(cl,n_cores)
  error_messages=foreach(i=1:length(groups),.inorder=F,.combine=rbind,.packages=c("rgdal"),.errorhandling="pass") %dopar%{
    indicators2=x[which(x[,1]==indicators[groups[[i]]]),]
    sources2=unique(indicators2[,2])
    sizes_list=as.data.frame(matrix(NA,length(sources2),2))
    for (j in 1:length(sources2)){
      sizes_list[j,1]=file.size(sources2[j])
      sizes_list[j,2]=file.size(sub("shp","dbf",sources2[j]))
    }
    sizes_list=sizes_list[,1]+sizes_list[,2]
    sources2=sources2[order(sizes_list)]
    nms=c(unique(indicators2[,3]),unique(indicators2[,5]))
    nas=which(nms=="")
    if (length(nas)==0){
      nms=nms
    }
    else{
      nms=nms[-nas]
    }
    result=SpatialPolygonsDataFrame(SpatialPolygons(list(),proj4string=CRS("+init=epsg:4326")),
                                    data.frame(matrix(NA,0,length(nms))))
    colnames(result@data)=nms
    result@bbox[1,]=c(-101,-46)
    result@bbox[2,]=c(-14,23)
    Message=matrix("NA",1,1)
    Message[1,]=paste0("The work for generating the file ",indicators[groups[[i]]]," began...")
    sum_shps=integer()
    for (j in sources2){
      shp=readOGR(j)
      sum_shps=sum(sum_shps,length(shp))
      nms_n=which(indicators2[,2]==j)
      nms=c(unique(indicators2[nms_n,4]),unique(indicators2[nms_n,6]))
      nas=which(nms=="")
      if (length(nas)==0){
        nms=nms
      }
      else{
        nms=nms[-nas]
      }
      nms_u=match(nms,colnames(shp@data))
      nas=which(is.na(nms_u))
      if (length(nas)==0){
        nms_u=nms_u
      }
      else{
        nms_u=nms_u[-nas]
      }
      if(length(nms)!=length(nms_u) | length(nms)!=length(colnames(result@data))){
        mesage=paste0("ERROR. The fields of the file ",j," did not match with the expected. This shapefile could not be included in the layer ",
                      indicators[groups[[i]]],". Please review the name and/or the existence of these fields")
        Message=rbind(Message,message)
        next()
      }
      else{
        shp@data=data.frame(shp@data[,nms_u])
        nms_n=c(unique(indicators2[nms_n,3]),unique(indicators2[nms_n,5]))
        nas=which(nms_n=="")
        if (length(nas)==0){
          nms_n=nms_n
        }
        else{
          nms_n=nms_n[-nas]
        }
        shp@data=data.frame(shp@data[,match(nms_n,colnames(result@data))])
        colnames(shp@data)=nms_n
        shp=spTransform(shp,CRS("+init=epsg:4326"))
        result=rbind(result,shp,makeUniqueIDs=T)
      }
    }
    if (length(result)!=sum_shps){
      Message=rbind(Message,paste0("The work for generating the file ",indicators[groups[[i]]]," failed."))
    }
    else{
      nms=gregexpr("/",indicators[groups[[i]]])[[1]]
      writeOGR(result,substr(indicators[groups[[i]]],1,nms[length(nms)]-1),
               substr(indicators[groups[[i]]],nms[length(nms)]+1,nchar(indicators[groups[[i]]])-4),driver="ESRI Shapefile")
      Message=rbind(Message,paste0("The work for generating the file ",indicators[groups[[i]]]," finished."))
    }
    write.table(Message,paste0(indicators[groups[[i]]],".MESSAGES.txt"),row.names=F,col.names=F,quote=F)
    return(Message)
  }
  stopCluster(cl)
  cat(paste0("\n",as.character(error_messages[,1])))
  nms=gregexpr("/",indicators[1])[[1]]
  files=list.files(substr(indicators[1],1,nms[length(nms)]-1),".dbf",full.names=T)
  files=sub(".dbf",".shp",files)
  nms=match(indicators,files)
  nas=which(is.na(nms))
  if (length(nas)==0){
    cat("\nThe process to produce source layers for calculating indicators was completed successfully")
  }
  else{
    cat("\nThe process to produce source layers for calculating indicators was not completed successfully",
        "\nThe the layer(s) below could not be generated",
        paste("\n",indicators[nas]))
  }
}