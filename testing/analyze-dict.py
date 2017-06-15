import json,os,sys,logging,pprint

def recordFreq(ngramDict,freqDict,level=1,print=True):
	if level not in freqDict:
		freqDict[level]={}
	if '_n' not in ngramDict:
		return
	if print:
		i=0
		l=len(ngramDict['_n'])
		printProgressBar(i, l, prefix = 'Analyzing Dict:', suffix = 'Complete')
	for k in ngramDict['_n']:
		count=ngramDict['_n'][k]['_c']
		logging.debug(count)
		n=level
		if count in freqDict[n]:
			freqDict[n][count]+=1
		else:
			freqDict[n][count]=1
		recordFreq(ngramDict['_n'][k],freqDict,print=False,level=n+1)
		if print:
				i+= 1
				printProgressBar(i, l, prefix = 'Analyzing Dict:', suffix = 'Complete')
	return

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 30, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print("\n")




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
	print("Loading from JSON file ...")
	jsonFile=open(sys.argv[2],'r')
	testDict=json.load(jsonFile)
	freqDict={}
	recordFreq(testDict,freqDict)
	# pprint.pprint(freqDict)



