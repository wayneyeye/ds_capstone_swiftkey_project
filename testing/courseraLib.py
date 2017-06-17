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
		item = re.sub(r"^.*\d+.*$","<quantity>",item)
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
				if xS==[]:
					xS=['<other>']
				else:
					xS.append("<eos>")
				logging.debug(xS)
				# xS=xS.append('<eos>')
				Corpus.append(xS)
			else:
				continue
		i+= 1
		printProgressBar(i, l, prefix = 'Loading Corpus:', suffix = 'Complete')
	#close file objs after use
	fileObj.close()
	logging.debug(Corpus)
	return Corpus

def ngramDict(ngramDictObj,word2id,id2word,token):
	logging.debug(token)
	word=token[0]
	ngramDictObj['_c']+=1
	# add new word to dictionary
	if word not in word2id['_word']:
		word2id['_counter']+=1
		wid='W'+str(word2id['_counter'])
		word2id['_word'][word]=wid
		id2word['_id'][wid]=word
	else:
		wid=word2id['_word'][word]

	# add id to ngramDict
	if wid not in ngramDictObj['_n']:
		ngramDictObj['_n'][wid]={"_c":0,"_n":{}}

	if len(token)<=1:
		ngramDictObj['_n'][wid]["_c"]+=1
		logging.debug('end of ngram')
		return 
	else:
		subDict=ngramDictObj['_n'][wid]
		token=token[1:]
		ngramDict(subDict,word2id,id2word,token)

def ngramExtract(tokens,n,ngramDictObj,word2id,id2word):
	if len(tokens)==0:
		return
	if len(tokens)<n:
		ngramDict(ngramDictObj,word2id,id2word,tokens)
		if len(tokens)>1:
			ngramExtract(tokens[1:],n,ngramDictObj,word2id,id2word)
	else:
		ngramDict(ngramDictObj,word2id,id2word,tokens[0:n])
		ngramExtract(tokens[1:],n,ngramDictObj,word2id,id2word)

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

def skimDict(ngramDictObj,print=True,mm=1):
	remove=[]
	#progress bar print
	if print:
		i=0
		l=len(ngramDictObj['_n'])
		printProgressBar(i, l, prefix = 'Shrinking Dict Step 1:', suffix = 'Complete')
	if '_n' not in ngramDictObj:
		return
	for wid in ngramDictObj['_n']:
		if ngramDictObj['_n'][wid]['_c']<=mm:
			remove.append(wid)
		if print:
			i+= 1
			printProgressBar(i, l, prefix = 'Shrinking Dict Step 1:', suffix = 'Complete')
		skimDict(ngramDictObj['_n'][wid],print=False)
	#progress bar print
	if print:
		i=0
		l=len(remove)
		printProgressBar(i, l, prefix = 'Shrinking Dict Step 2:', suffix = 'Complete')
	for wid in remove:
		del ngramDictObj['_n'][wid]
		if print:
			i+= 1
			printProgressBar(i, l, prefix = 'Shrinking Dict Step 2:', suffix = 'Complete')

def skimVacantDict(ngramDictObj):
	if '_n' in ngramDictObj:
		remove_w=[]
		for wid in ngramDictObj['_n']:
			if len(ngramDictObj['_n'][wid])==0:
				remove_w.append(wid)
			skimVacantDict(ngramDictObj['_n'][wid])
		for wid in remove_w:
			del ngramDictObj['_n'][wid]
	

def ExtractCorpus(Corpus,n):
	# create new Dict for storage
	ngramDictObj={'_createDate':str(datetime.datetime.now()),"_model":n,'_n':{},'_c':0}
	word2id={'_word':{},'_counter':0}
	id2word={'_id':{}}
	#progress bar print
	i=0
	l=len(Corpus)
	printProgressBar(i, l, prefix = 'Generating Dict:', suffix = 'Complete')
	#iterate thru corpus
	for tokens in Corpus:
		ngramExtract(tokens,n,ngramDictObj,word2id,id2word)
		i+= 1
		printProgressBar(i, l, prefix = 'Generating Dict:', suffix = 'Complete')
	
	if "<eos>" in word2id["_word"]:
		del ngramDictObj["_n"][word2id["_word"]["<eos>"]]
	ngramDictObj["_word2id"]=word2id
	ngramDictObj["_id2word"]=id2word
	return ngramDictObj

def rankingDict(ngramDictObj,print=True,max=5,parent_ct=100):
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
			if ngramDictObj['_n'][w]['_n']!={}:
				leafChildOnlyFlag=False
			# load freqDict
			ngramDictObj['_f'][w]=ngramDictObj['_n'][w]['_c']
			# recursively call to the next level
			rankingDict(ngramDictObj['_n'][w],print=False,parent_ct=ngramDictObj['_n'][w]['_c'])			
			if print:
				i+= 1
				printProgressBar(i, l, prefix = 'Ranking Dict:', suffix = 'Complete')
		# if the current node has more than max branches--->cache the most frequent child		
		if len(ngramDictObj['_f'])>max:
			ngramDictObj['_r']=sorted(ngramDictObj['_f'],\
			 	key=ngramDictObj['_f'].__getitem__,reverse=True)
		else:
			ngramDictObj['_r']=list(ngramDictObj['_f'].keys())
		# shrink _r
		if len(ngramDictObj['_r'])>max:
			ngramDictObj['_r']=ngramDictObj['_r'][0:max]
		# delete _f 
		del ngramDictObj['_f']
		del ngramDictObj['_c']
		if leafChildOnlyFlag:
			# remove=[];
			# for k in ngramDictObj['_n'].keys():
			# 		remove.append(k)
			# for k in remove:
			# 	del ngramDictObj['_n'][k]
			del ngramDictObj['_n']
	# if a leaf node
	else:
		# free leafnode space
		del ngramDictObj['_n']
		del ngramDictObj['_c']

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
	sentencePATH='/home/yewenhe0904/Developing/ds-capstone-project/sample-data/sentences-sample.txt'
	testPATH='/home/yewenhe0904/Developing/ds-capstone-project/testing-data/twitter-testing.txt'
	Corpus=prepareCorpus(testPATH)
	ngramDictObj=ExtractCorpus(Corpus,3)
	rankingDict(ngramDictObj,parent_ct=ngramDictObj['_c'])
	# print(sys.getsizeof(ngramDictObj))
	if ngramDictObj['_word2id']['_counter']<=100:
		pprint.pprint(ngramDictObj)
	else:
		f1=open('ignoredFiles/sample-ngramDict.json',"w")
		json.dump(ngramDictObj,f1)
		f1.close
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
