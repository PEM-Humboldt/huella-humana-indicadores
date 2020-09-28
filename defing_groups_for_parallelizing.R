#Defing groups for parallelizing
groups_for_parallelizing=function(n_elements,n_cores){
  size=round(n_elements/n_cores,0)
  size=ifelse(size<1,1,size)
  groups=sort(rep(1:n_cores,size))[1:n_elements]
  nas=which(is.na(groups))
  if (length(nas)==0){
    groups=groups
  }
  else {
    groups[nas]=n_cores
  }
  groups_list=list()
  list_length=ifelse(length(groups)>n_cores,n_cores,length(groups))
  for(i in 1:list_length){
    groups_list[[i]]=which(groups==i)
  }
  return(groups_list)
}