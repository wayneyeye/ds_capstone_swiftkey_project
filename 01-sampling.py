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
dataFilePath=os.path.join(os.getcwd(),'text-data')
dataFileDict={}
for file in os.listdir(dataFilePath):
	logging.info(file)
	logging.debug(type(file))
	logging.info(str(os.path.getsize(os.path.join(dataFilePath,file))/1024/1024)+' MB')
	fileName=file.split(".")
	dataFileDict[fileName[1]]=\
	{
	"path":os.path.join(dataFilePath,file),
	"size":os.path.getsize(os.path.join(dataFilePath,file))
	}
logging.debug(dataFileDict)
# open desired text file
file2read=input("which file to read?\n"+" ".join(dataFileDict.keys())+"\n")
fileObj=open(dataFileDict[file2read]["path"])
# create sample text file path
sampleFilePath=os.path.join(os.getcwd(),"sample-data",file2read+"-sample.txt")
# purge existing file,if any
if os.path.exists(sampleFilePath):
	print(sampleFilePath+" already exists, will be removed before moving on")
	os.remove(sampleFilePath)
# create sample file
saveObj=open(sampleFilePath,"a")
i=1
for line in fileObj:
	saveObj.write(line)
	i+=1
	if i>=1000:
		break

fileObj.close()
saveObj.close()
