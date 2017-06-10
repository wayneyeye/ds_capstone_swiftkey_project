import sys,os,logging,re,pprint,string,datetime
def cleanInput(input):
	input=re.sub('\n+'," ",input).lower()
	input=bytes(input,"UTF-8")
	input=input.decode("ascii","ignore")
	input=input.split(' ')
	#strip single letter word other than i and a
	cleanInput=[]
	for item in input:
		# logging.debug(item)
		item = item.strip(string.punctuation)
		item = re.sub(r"^.*\d+.*$","<Quantity>",item)
		if len(item)>1 or (item=='a' or item=='i'):
			cleanInput.append(item)
	return cleanInput

def prepareCorpus(path):
	fileObj=open(path)
	Corpus=[]
	i = 0
	l = len(list(open(path)))
	# Initial call to print 0% progress
	printProgressBar(i, l, prefix = 'Loading Corpus:', suffix = 'Complete')
	for line in fileObj:
		EoSentence="[.,;!?]+"
		line=re.sub(EoSentence,"\n",line) 
		line=line.split("\n")
		for s in line:
			if s!='':
				xS=cleanInput(s)
				Corpus.append(xS)
			else:
				continue
		i+= 1
		printProgressBar(i, l, prefix = 'Loading Corpus:', suffix = 'Complete')
	#close file objs after use
	fileObj.close()
	return Corpus

def ngramDict(ngramDictObj,token):
	word=token[0]
	if word not in ngramDictObj:
		ngramDictObj[word]={"_count":1,"_nextWord":{}}
	else:
		ngramDictObj[word]["_count"]+=1
	if len(token)<=1:
		return 
	else:
		subDict=ngramDictObj[word]["_nextWord"]
		ngramDict(subDict,token[1:])

def ngramExtract(tokens,n,ngramDictObj):
	if len(tokens)==0:
		return
	if len(tokens)<n:
		ngramDict(ngramDictObj,tokens)
		if len(tokens)>1:
			ngramExtract(tokens[1:],n,ngramDictObj)
	else:
		ngramDict(ngramDictObj,tokens[0:n])
		ngramExtract(tokens[1:],n,ngramDictObj)

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

def ExtractCorpus(Corpus,n):
	ngramDictObj={'_createDate':str(datetime.datetime.now()),'_nextWord':{}}
	i=0
	l=len(Corpus)
	printProgressBar(i, l, prefix = 'Generating Dict:', suffix = 'Complete')
	for tokens in Corpus:
		ngramExtract(tokens,n,ngramDictObj['_nextWord'])
		i+= 1
		printProgressBar(i, l, prefix = 'Generating Dict:', suffix = 'Complete')
	print(len(ngramDictObj),"items loaded")
	return ngramDictObj

def rankingDict(ngramDictObj,print=True):
	if ngramDictObj['_nextWord']!={}:
		ngramDictObj['_freqDict']={}
		# progress bar
		if print:
			i=0
			l=len(ngramDictObj['_nextWord'])
			printProgressBar(i, l, prefix = 'Ranking Dict:', suffix = 'Complete')
		for w in ngramDictObj['_nextWord']:
			ngramDictObj['_freqDict'][w]=ngramDictObj['_nextWord'][w]['_count']
			ngramDictObj['_nextRanking']=sorted(ngramDictObj['_freqDict'],\
				key=ngramDictObj['_freqDict'].__getitem__,reverse=True)
			rankingDict(ngramDictObj['_nextWord'][w],print=False)
			if print:
				i+= 1
				printProgressBar(i, l, prefix = 'Ranking Dict:', suffix = 'Complete')
	else:
		return

def test():
	Corpus=prepareCorpus('/home/yewenhe0904/Developing/ds-capstone-project/sample-data/blogs-sample.txt')
	ngramDictObj=ExtractCorpus(Corpus,3)
	rankingDict(ngramDictObj)
	pprint.pprint(ngramDictObj)
	return	

if __name__=="__main__":
	test()
