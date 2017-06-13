import sys,os,logging,re,pprint,string,datetime,gc,json
import courseraLib as co
LOGGING_LVL={
	"debug":logging.DEBUG,
	"info":logging.INFO,
	"warning":logging.WARNING,
	"error":logging.ERROR,
	"critical":logging.CRITICAL,
}
logging.basicConfig(level=LOGGING_LVL.get(sys.argv[1],'debug'),format='%(asctime)s-%(levelname)s-%(message)s')


#loading training files
logging.debug(os.getcwd())
if input('debug or run?\n')=='run':
	dataFilePath=os.path.join(os.getcwd(),'training-data')
else:
	dataFilePath=os.path.join(os.getcwd(),'mini-data')
dataFileDict={}
for file in os.listdir(dataFilePath):
	logging.debug(file)
	logging.debug(type(file))
	logging.debug(str(os.path.getsize(os.path.join(dataFilePath,file))/1024/1024)+' MB')
	fileName=file.split("-")
	dataFileDict[fileName[0]]=\
	{
	"path":os.path.join(dataFilePath,file),
	"size":os.path.getsize(os.path.join(dataFilePath,file))
	}
pprint.pprint(dataFileDict)


# open desired text file
file2read=input("which file to read?\n type all to generate all\n"+" ".join(dataFileDict.keys())+"\n")
fileList=[]
if file2read.lower()=="all":
	fileList=list(dataFileDict.keys())
else:
	fileList.append(file2read)

n_model=int(input('the n value in n-gram model?\n'))

for f in fileList:
	print("Working on ",f,"...\n")
	Corpus=co.prepareCorpus(dataFileDict[f]['path'])
	ngramDictObj=co.ExtractCorpus(Corpus,n_model)
	co.rankingDict(ngramDictObj,parent_ct=ngramDictObj['_c'])
	savetopath=os.path.join(os.getcwd(),'ignoredFiles','DictOutput',f+'-nGramDict.json')
	f1=open(savetopath,"w")
	json.dump(ngramDictObj,f1)
	f1.close
	gc.collect()
