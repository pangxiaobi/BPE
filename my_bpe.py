import re,collections
import sys
def get_stats(vocab):
	pairs = collections.defaultdict(int)
	for word,freq in vocab.items():
		symbols = word.split()
		for i in range(len(symbols)-1):
			pairs[symbols[i],symbols[i+1]]+=freq
	return pairs
def merge_vocab(pair,v_in):
	v_out={}
	bigram=re.escape(' '.join(pair))
	p = re.compile(r'(?<!\S)'+bigram+r'(?!\S)')
	for word in v_in:
		w_out = p.sub(''.join(pair),word)
		v_out[w_out]=v_in[word]
	return v_out
if __name__=='__main__':
	num_merges = 500
	file1 = open(sys.argv[1],'rb')
	vocab = {}
	ind = {}
	num=0
	ind_inv={}
	line_num=0
	for line in file1.readlines():
		line = line.rstrip().split(' ')
		for term in line:
			term = term.decode('utf8')
			if len(term)==0:
				continue
			if not ind.has_key(term):
				ind[term]=[]
			ind[term].append(num)
			ind_inv[num]=term
			num+=1
			s = ''
			for i in term[:-1]:
				s+=i
				s+=' '
			s+=term[-1]
			if not vocab.has_key(s):
				vocab[s]=0
			vocab[s]+=1
		ind_inv[num]='<\s>'
		num+=1
		line_num+=1
		if line_num%1000==0:
			print line_num
	print len(vocab)
	for i in range(num_merges):
		print i
		pairs =get_stats(vocab)
		best = max(pairs,key=pairs.get)
		vocab = merge_vocab(best,vocab)
	out=[0]*num
	print num,len(vocab),len(ind)	
	fileout = open(sys.argv[2],'wb')
	for (k,v) in vocab.items():
		s =''.join( k.split(' '))
		for i in ind[s]:
			out[i]=k.split(' ')
	for i in range(num):
		if ind_inv[i]=='<\s>':
			fileout.writelines('\n')
			continue
		for k in out[i]:
			fileout.writelines(str(k.encode('utf8'))+' ')
		
