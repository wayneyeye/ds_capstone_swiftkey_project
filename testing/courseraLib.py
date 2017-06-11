import sys,os,logging,re,pprint,string,datetime,gc,json
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
	# Initial call to print 0% progress
	i = 0
	l = len(list(open(path)))
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
	ngramDictObj['_c']+=1
	if word not in ngramDictObj['_n']:
		ngramDictObj['_n'][word]={"_c":0,"_n":{}}
	if len(token)<=1:
		return 
	else:
		subDict=ngramDictObj['_n'][word]
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
	# create new Dict for storage
	ngramDictObj={'_createDate':str(datetime.datetime.now()),'_n':{},'_c':0}
	#progress bar print
	i=0
	l=len(Corpus)
	printProgressBar(i, l, prefix = 'Generating Dict:', suffix = 'Complete')
	#iterate thru corpus
	for tokens in Corpus:
		ngramExtract(tokens,n,ngramDictObj)
		i+= 1
		printProgressBar(i, l, prefix = 'Generating Dict:', suffix = 'Complete')
	return ngramDictObj

def rankingDict(ngramDictObj,print=True,max=10,parent_ct=100):
	# if not a leaf node
	if ngramDictObj['_n']!={}:
		ngramDictObj['_f']={}
		# progress bar
		if print:
			i=0
			l=len(ngramDictObj['_n'])
			printProgressBar(i, l, prefix = 'Ranking Dict:', suffix = 'Complete')
		# add to freqDict
		leafChildOnlyFlag=True
		for w in ngramDictObj['_n']:
			#fix leaf node count
			if ngramDictObj['_n'][w]['_n']=={}:
				ngramDictObj['_n'][w]['_c']=1
			else:
				leafChildOnlyFlag=False
			# load freqDict
			ngramDictObj['_f'][w]=ngramDictObj['_n'][w]['_c']
			ngramDictObj['_n'][w]['_p']=ngramDictObj['_n'][w]['_c']/parent_ct
			# recursively call to the next level
			rankingDict(ngramDictObj['_n'][w],print=False,parent_ct=ngramDictObj['_n'][w]['_c'])			
			if print:
				i+= 1
				printProgressBar(i, l, prefix = 'Ranking Dict:', suffix = 'Complete')
		# if the current node has more than 5 branches--->cache the most frequent child		
		if len(ngramDictObj['_f'])>5:
			ngramDictObj['_r']=sorted(ngramDictObj['_f'],\
			 	key=ngramDictObj['_f'].__getitem__,reverse=True)
		else:
			ngramDictObj['_r']=list(ngramDictObj['_f'].keys())
		# shrink _r
		if len(ngramDictObj['_r'])>max:
			ngramDictObj['_r']=ngramDictObj['_r'][0:max]
		# delete _f _c
		del ngramDictObj['_f']
		del ngramDictObj['_c']
		if leafChildOnlyFlag:
			remove=[];
			for k in ngramDictObj['_n'].keys():
				if k not in ngramDictObj['_r']:
					remove.append(k)
			for k in remove:
				del ngramDictObj['_n'][k]
	# if a leaf node
	else:
		# free leafnode space
		del ngramDictObj['_n']
		del ngramDictObj['_c']
		# del ngramDictObj['_p']
		


def naivePredict(ngramDictObj,previous):
	previous_list=previous.lower().split(' ')
	print(previous_list)
	try:
		print(ngramDictObj['_n'][previous_list[0]]['_n'][previous_list[1]]\
			['_n'][previous_list[2]]['_n'][previous_list[3]]['_r'])
	except:
		print("Not Exists!")
	return

def test():
	Corpus=prepareCorpus('/home/yewenhe0904/Developing/ds-capstone-project/sample-data/sentences-sample.txt')
	ngramDictObj=ExtractCorpus(Corpus,4)
	rankingDict(ngramDictObj,parent_ct=ngramDictObj['_c'])
	# print(sys.getsizeof(ngramDictObj))
	# f=open('ignoredFiles/sample-output.json',"w")
	pprint.pprint(ngramDictObj)
	# json.dump(ngramDictObj,f)
	# f.close
	# while True:
	# 	previous=input("input something to predict (type quit to exit):\n")
	# 	naivePredict(ngramDictObj,previous)
	# 	if previous=="quit":
	# 		sys.exit()
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

	test()
