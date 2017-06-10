import sys,os,logging,re,pprint,random
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
sampleFilePath_training=os.path.join(os.getcwd(),"training-data",file2read+"-training.txt")
sampleFilePath_testing=os.path.join(os.getcwd(),"testing-data",,file2read+"-testing.txt")

# purge existing file,if any
if os.path.exists(sampleFilePath_testing):
	print(sampleFilePath_testing+" already exists, will be removed before moving on")
	os.remove(sampleFilePath_testing)
if os.path.exists(sampleFilePath_training):
	print(sampleFilePath_training+" already exists, will be removed before moving on")
	os.remove(sampleFilePath_training)

# create sample file
trainingSet=open(sampleFilePath_training,"a")
testingSet=open(sampleFilePath_testing,"a")

# 8 of 10 go to training 2 go to testing
sampleCutoff=80

for line in fileObj:
	if (random.randint(1,100)<=sampleCutoff):
		trainingSet.write(line)
	else:
		testingSet.write(line)

#close file objects after usage
fileObj.close()
trainingSet.close()
testingSet.close()
