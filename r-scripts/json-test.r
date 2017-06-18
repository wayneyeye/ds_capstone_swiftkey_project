library(jsonlite)
getwd()
setwd("/home/yewenhe0904/Developing/ds-capstone-project/")

data1<-read_json('ignoredFiles/Sample-Dict/mixed-nGramDict_10_1.json')
length(data1)
data1$`_n`$W1
