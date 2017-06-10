import sys,os,logging,re,pprint,string,courseraLib
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
		item = re.sub(r"^.*\d+.*$","<Quantity>",item)
		if len(item)>1 or (item=='a' or item=='i'):
			cleanInput.append(item)
	return cleanInput
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
#save to corpus
i = 0
l = len(list(open(dataFileDict[file2read]["path"])))
Corpus=[]
#
courseraLib.printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
for line in fileObj:
	logging.info("------------------------Orginial Text--------------------------")
	logging.info("\n"+line)
	logging.info("------------------------Processing--------------------------")
	# split at end of sentences
	EoSentence="[.,;!?]+"
	line=re.sub(EoSentence,"\n",line) 
	line=line.split("\n")
	logging.debug(line)
	for s in line:
		if s!='':
			xS=cleanInput(s)
			logging.info(xS)
			Corpus.append(xS)
		else:
			continue
	logging.info("********************End of Processing*******************\n")
	i+= 1
	courseraLib.printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

#test
ngramDictObj=courseraLib.ExtractCorpus(Corpus,3)
logging.debug(ngramDictObj)
logging.debug(ngramDictObj["the"])
print(len(ngramDictObj),"items")
#close file objs after use
fileObj.close()