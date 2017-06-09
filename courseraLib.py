import pprint
def ngramDict(ngramDictObj,token):
	word=token[0]
	if word not in ngramDictObj:
		ngramDictObj[word]={"_count":1}
	else:
		ngramDictObj[word]["_count"]+=1
	if len(token)<=1:
		return 
	else:
		subDict=ngramDictObj[word]
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

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
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
        print()

def ExtractCorpus(Corpus,n):
	ngramDictObj={}
	i=0
	l=len(Corpus)
	printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
	for tokens in Corpus:
		ngramExtract(tokens,n,ngramDictObj)
		i+= 1
		printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
	return ngramDictObj

# Print iterations progress

def test():
	sampleTokens=["apple","<quantity>","banana","i","wonder","why","such","a","big","cake","such","a","wonderful",]
	sampleCorpus=[sampleTokens,[]]
	ngramDictObj=ExtractCorpus(sampleCorpus,3)
	pprint.pprint(ngramDictObj)
	
if __name__=="__main__":
	test()
