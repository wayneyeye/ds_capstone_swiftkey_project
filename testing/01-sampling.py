import sys,os,logging,re,pprint,random
import courseraLib
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
file2read=input("which file to read?\n type all to generate all\n"+" ".join(dataFileDict.keys())+"\n")
fileList=[]
if file2read.lower()=="all":
	fileList=list(dataFileDict.keys())
else:
	fileList.append(file2read)

for f in fileList:
	fileObj=open(dataFileDict[f]["path"])
	# create sample text file path
	sampleFilePath_training=os.path.join(os.getcwd(),"training-data",f+"-training.txt")
	sampleFilePath_testing=os.path.join(os.getcwd(),"testing-data",f+"-testing.txt")

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
	# Initial call to print 0% progress
	i = 0
	l = len(list(open(dataFileDict[f]["path"])))
	courseraLib.printProgressBar(i, l, prefix = 'Sampling '+f+":", suffix = 'Complete')
	for line in fileObj:
		if (random.randint(1,100)<=sampleCutoff):
			trainingSet.write(line)
		else:
			testingSet.write(line)
		i+=1
		courseraLib.printProgressBar(i, l, prefix = 'Sampling '+f+":", suffix = 'Complete')

	#close file objects after usage
	fileObj.close()
	trainingSet.close()
	testingSet.close()
