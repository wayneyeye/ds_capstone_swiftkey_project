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
	if len(tokens)<n:
		ngramDict(ngramDictObj,tokens)
		if len(tokens)>1:
			ngramExtract(tokens[1:],n,ngramDictObj)
	else:
		ngramDict(ngramDictObj,tokens[0:n])
		ngramExtract(tokens[1:],n,ngramDictObj)

def ExtractCorpus(Corpus,n):
	ngramDictObj={}
	for tokens in Corpus:
		ngramExtract(tokens,n,ngramDictObj)
	return ngramDictObj

	
def test():
	sampleTokens=["apple","<quantity>","banana","i","wonder","why","such","a","big","cake","such","a","wonderful",]
	sampleCorpus=[sampleTokens,sampleTokens]
	ngramDictObj=ExtractCorpus(sampleCorpus,3)
	pprint.pprint(ngramDictObj)
	
if __name__=="__main__":
	test()
