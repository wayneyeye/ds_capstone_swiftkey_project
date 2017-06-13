import json,os,sys,logging,pprint

def recordFreq(ngramDict,freqDict,level=1):
	if level not in freqDict:
		freqDict[level]={}
	if '_n' not in ngramDict:
		return
	for k in ngramDict['_n']:
		count=ngramDict['_n'][k]['_c']
		logging.debug(count)
		n=level
		if count in freqDict[n]:
			freqDict[n][count]+=1
		else:
			freqDict[n][count]=1
		recordFreq(ngramDict['_n'][k],freqDict,level=n+1)
	return





if __name__=="__main__":
	LOGGING_LVL={
	"debug":logging.DEBUG,
	"info":logging.INFO,
	"warning":logging.WARNING,
	"error":logging.ERROR,
	"critical":logging.CRITICAL,
}
	logging.basicConfig(level=LOGGING_LVL.get(sys.argv[1],'debug'),format='%(asctime)s-%(levelname)s-%(message)s')

#loads data from json file
	jsonFile=open('ignoredFiles/DictOutput/twitter-nGramDict.json','r')
	testDict=json.load(jsonFile)
	freqDict={}
	recordFreq(testDict,freqDict)
	pprint.pprint(freqDict)



