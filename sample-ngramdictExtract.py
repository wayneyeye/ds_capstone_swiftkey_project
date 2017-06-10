import logging,sys,os,pprint,courseraLib
# Logging header
LOGGING_LVL={
	"debug":logging.DEBUG,
	"info":logging.INFO,
	"warning":logging.WARNING,
	"error":logging.ERROR,
	"critical":logging.CRITICAL,
}
logging.basicConfig(level=LOGGING_LVL.get(sys.argv[1],'debug'),format='%(asctime)s-%(levelname)s-%(message)s')

#
logging.debug(os.getcwd())
dataFilePath=os.path.join(os.getcwd(),'sample-data')
dataFileDict={}
# choose which file to read
for file in os.listdir(dataFilePath):
	logging.info(file)
	logging.debug(type(file))
	logging.info(str(os.path.getsize(os.path.join(dataFilePath,file))/1024/1024)+' MB')
	fileName=file.split("-")
	dataFileDict[fileName[0]]=\
	{
	"path":os.path.join(dataFilePath,file),
	"size":os.path.getsize(os.path.join(dataFilePath,file))
	}
pprint.pprint(dataFileDict)

# open desired text file
file2read=input("which file to read?\n"+" ".join(dataFileDict.keys())+"\n")

# save to corpus
Corpus=courseraLib.prepareCorpus(dataFileDict[file2read]["path"])

# generate dict obj
ngramDictObj=courseraLib.ExtractCorpus(Corpus,4)

# logging.debug(ngramDictObj)
print(len(ngramDictObj),"items loaded")
