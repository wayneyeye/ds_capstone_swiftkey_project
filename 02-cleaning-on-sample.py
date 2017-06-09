import sys,os,logging,re,pprint,string
#Logging header
LOGGING_LVL={
	"debug":logging.DEBUG,
	"info":logging.INFO,
	"warning":logging.WARNING,
	"error":logging.ERROR,
	"critical":logging.CRITICAL,
}
logging.basicConfig(level=LOGGING_LVL.get(sys.argv[1],'debug'),format='%(asctime)s-%(levelname)s-%(message)s')
#helper functions goes below
def cleanInput(input):
	input=re.sub('\n+'," ",input).lower()
	input=bytes(input,"UTF-8")
	input=input.decode("ascii","ignore")
	input=input.split(' ')
	#strip single letter word other than i and a
	cleanInput=[]
	for item in input:
		logging.debug(item)
		item = item.strip(string.punctuation)
		if len(item)>1 or (item=='a' or item=='i'):
			cleanInput.append(item)
	return cleanInput
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
	logging.info("------------------------Orginial Text--------------------------")
	logging.info("\n"+line)
	logging.info("------------------------Processing--------------------------")
	logging.info(cleanInput(line))
	logging.info("********************End of Processing*******************\n")



#close file objs after use
fileObj.close()
