library(xlsx)
library(sf)
#install.packages("arcgisbinding", repos="http://r-arcgis.github.io/r-bridge", type="win.binary")
source("D:/Modulo_Indicadores/Scripts/produce_indicators_sources.R")
source("D:/Huella/Scripts/add_hfp_cat_year.R")
source("D:/Huella/Scripts/add_hfp_pers.R")
source("D:/Huella/Scripts/join_fields.R")
source("D:/Huella/Scripts/binary_protected.R")
source("D:/Huella/Scripts/calculate_area.R")
source("D:/Huella/Scripts/merge.R")
source("D:/Huella/Scripts/verify_fields.R")

#Read base table
base_t=read.xlsx2("D:/Huella/Tablas/Modelo de datos geográficos indicadores.xls",
                  sheetName="estructura_indicadores",colIndex=3:10,stringsAsFactors=F)
base_t=base_t[,c(4,1,6,2,8,3)]
base_t=base_t[-which(grepl("Indicadores",substr(base_t[,1],1,11))),]
base_t[,1]=paste0("D:/Huella/",base_t[,1])
base_t[,2]=paste0("D:/Huella/",base_t[,2])

#Add hfp_cat and year_hfp fields
add_hfp_cat_year(base_t[1:5,2],5)

#Add hfp_pers field
add_hfp_pers(base_t[6,2])

#Produce capas base
produce_indicators_sources(base_t,nrow(base_t))

#Join fields
paths_shp=read.xlsx("D:/Huella/Scripts/batch_arc_gis.xls",sheetName="4. Zonal Statistics",header=F)
paths_join=as.character(paths_shp[,4])
paths_shp=as.character(paths_shp[,1])
paths_shp=sub("_Dissolve.gdb","",paths_shp)
paths_shp=paste0(paths_shp,".shp")
field_shp=field_join=rep("OBJECTID",length(paths_shp))
new_field_shp=rep("hf_avg",length(paths_shp))
calculate_field_join=rep("MEAN",length(paths_shp))
join_fields_shp(paths_shp,paths_join,
                field_shp,field_join,
                new_field_shp,calculate_field_join,
                length(paths_shp))

#Calculate binary protected
paths_shp=read.xlsx("D:/Huella/Scripts/batch_arc_gis.xls",sheetName="5. Delete Field",header=F)
paths_shp=as.character(paths_shp[,1])
binary_protected_shp(paths_shp,length(paths_shp))

#Calculate area
paths_shp=read.xlsx("D:/Huella/Scripts/batch_arc_gis.xls",sheetName="5. Delete Field",header=F)
paths_shp=as.character(paths_shp[,1])
calculate_area_shp_write(paths_shp,length(paths_shp))
gc()

#Merge and verify fields
paths=read.xlsx("D:/Huella/Scripts/batch_arc_gis.xls",sheetName="5. Delete Field",header=F)
paths=as.character(paths[,1])
paths=data.frame(paths,names=c(rep("geo_hf",5),
                               "geo_hf_persistence",
                               rep("geo_hf_tropical_dry_forest",5),
                               rep("geo_hf_wetland",5),
                               rep("geo_hf_paramo",5)))
merge_names=unique(paths$names)
merge_names=merge_names[-2]
fields_shp=c("id_state","id_ea","id_biome","id_basin","id_zone","id_subzone","ecosystem","ecosy_name","ecosy_type","ecosy_year","hf_cat","hf_year","hf_avg","hf_pers","area_ha","binary_protected")

#n_cores=length(merge_names)
#cl=makeCluster(n_cores,type="PSOCK")
#registerDoParallel(cl,n_cores)
#foreach(i=1:length(merge_names),.inorder=F,.packages=c("rgdal","sf"),.errorhandling="pass",.export=.GlobalEnv) %dopar% {
for (i in 1:length(merge_names)){ 
  paths_shp=paths$paths[paths$names==merge_names[i]]
  shp=merge_list_object(paths_shp)
  names(shp)[names(shp)=="binary_p"]="binary_protected"
  shp=verify_fields_list_object(shp,fields_shp)
  #writeOGR(shp,"D:/Huella/Indicadores",merge_names[i],driver="GPKG")
  shp=st_as_sf(shp)
  st_write(shp,paste0("D:/Huella/Indicadores/",merge_names[i],".gpkg"))
  gc()
}
shp=readOGR(paths$paths[6])
names(shp)[names(shp)=="binary_p"]="binary_protected"
shp=verify_fields_list_object(shp,fields_shp)
shp=st_as_sf(shp)
st_write(shp,paste0("D:/Huella/Indicadores/",paths$names[6],".gpkg"))
