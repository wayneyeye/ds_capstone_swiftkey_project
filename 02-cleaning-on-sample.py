import sys,os,logging,re,pprint
#Logging header
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
logging.debug(dataFileDict)
# open desired text file
file2read=input("which file to read?\n"+" ".join(dataFileDict.keys())+"\n")
fileObj=open(dataFileDict[file2read]["path"])
#
for line in fileObj:
	logging.debug("------------------------Orginial Text--------------------------")
	logging.debug("\n"+line)
	logging.debug("------------------------Processing--------------------------")
	logging.debug("********************End of Processing*******************\n")



#close file objs after use
fileObj.close()