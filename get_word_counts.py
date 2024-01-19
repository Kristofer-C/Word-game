# -*- coding: utf-8 -*-

import requests
import json

# Word list
fname="CROSSWD.txt"
with open(fname, 'r') as f:
    dictionary=f.read().splitlines()
len_dict=len(dictionary)

# Output file name
fout="word_counts.txt"

# Endpoint
url="https://api.ngrams.dev/eng/batch"

# Flags
flags="cr"

# Number of words in each query
len_batch=100


# Make batch requests until all words have been requested.
i=0
max_i=len_dict//len_batch
with open(fout, 'w') as f: 
    while i<=max_i:
        
        # Progress indicator
        if i%10==0:
            print("Now working on batch %d out of %d."%(i, max_i))
        
    
        # Get the next batch of words from the word list.
        batch=dictionary[i*len_batch:min((i+1)*len_batch, len_dict)]
    
        # Define search paramenters.
        parameters={
            "queries":batch,
            "flags":flags
        }
        
        # Make the request.
        response=requests.post(url, json=parameters).json()
        
        # Extract the word counts for each word in the batch.
        for j in range(len(batch)):
            if response['results'][j]['ngrams']: # Make sure count>0
                count=response['results'][j]['ngrams'][0]['absTotalMatchCount']
            else: # If not, just record 0
                count=0
        
            # Write the word and its count to a file in a new line.
            f.write(batch[j]+"\t"+str(count)+"\n")
        
        i+=1
