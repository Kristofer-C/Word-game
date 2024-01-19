# -*- coding: utf-8 -*-

import numpy as np

# The length of the word segments
LEN_KEY=3

alphabet='abcdefghijklmnopqrstuvwxyz'
alphabet_dict={}
for i, letter in enumerate(alphabet):
    alphabet_dict[letter]=i
    
len_alpha=len(alphabet)


# Load and sort the words list, filtering out words less than three letters
fname="word_counts.txt"
words, counts=np.loadtxt(fname, dtype=str, unpack=True)
words3bool=np.char.str_len(words)>=LEN_KEY
words=words[words3bool]
counts=counts[words3bool].astype('int64')
sort_inds=np.argsort(counts)[::-1]
words=words[sort_inds]
counts=counts[sort_inds]

# Make a list of keys
ind=0
key_list=[]
while ind<len_alpha**3:
    a=ind%len_alpha
    b=(ind%(len_alpha**2)-a)//len_alpha
    c=(ind%(len_alpha**3)-(a+len_alpha*b))//(len_alpha**2)
    key=alphabet[c]+alphabet[b]+alphabet[a]
    key_list.append(key)
    ind+=1
key_list=np.array(key_list)
  
# Count the number of times each key appears in the corpus
# And record the most common word that uses each key
keys_counts=np.zeros(len(key_list))
first_word=np.empty(len(key_list), dtype='O')

for i, word in enumerate(words):
    for j in range(0,len(word)-LEN_KEY+1):
        key=word[j:j+3]
        # The index in the key list corresponding to the current word segment
        ind=alphabet_dict[key[0]]*len_alpha**2+alphabet_dict[key[1]]*len_alpha+alphabet_dict[key[2]]
        if keys_counts[ind]==0:
            first_word[ind]=word
        keys_counts[ind]+=counts[i]
        
# Sort the keys based on counts
sort_inds=np.argsort(keys_counts)[::-1]
keys_counts_sorted=keys_counts[sort_inds]
keys_sorted=key_list[sort_inds]
first_word_sorted=first_word[sort_inds]

# Save the keys, counts, and most common words 
outname="keys_counts_sorted.txt"
np.savetxt(outname, np.array([keys_sorted, keys_counts_sorted, first_word_sorted]).T, fmt='%s', delimiter='\t')