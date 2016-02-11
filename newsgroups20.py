# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 14:47:28 2016

@author: Rok
"""

import collections
import re
import numpy as np
import os
from sklearn.preprocessing import Normalizer

#iterates trough all files in folder and returns a list of and exports a txt file containing n most frequent words
def get_words(root_dir, n=False):
    cnt = collections.Counter() #instantiate a counter
    #Count the words in the entire corpus - all the documents
    subfolders = next(os.walk(root_dir))[1] #get subfolders of folder
    for subfolder in subfolders: #iterate over subfolders
        for filename in os.listdir(os.path.join(root_dir, subfolder)): #iterate over names of files in subfolder
            filepath = root_dir + '/' + subfolder + '/' + filename #get a filepath
            file = open(filepath, encoding="Latin-1")
            removelist = " "
            for row in file: #Count the words in a (text) file
                if "Lines" in row: #Only start procesing after the header lines which end with "Lines" word
                    next(file) #Skip current line and proceed
                    for row in file:                  
                        clean_row = re.sub(r'[^\w'+removelist+']', '',row)
                        for word in clean_row.lower().split():
                            cnt[word] += 1
            file.close()
    #Get the n words that appear most frequently in a text (corpus) as a list of strings
    words = []
    if n:
        d2 = cnt.most_common(n)
#    sorted_d = sorted(d2, key=lambda tup: tup[1], reverse=True)
    d2 = cnt.most_common() #take all words
    for key, value in d2:
        words.append(key)
    if n:
        np.savetxt(str(n) + "_words.txt", words, fmt="%s")
    np.savetxt("words.txt", words, fmt="%s")
    return words

#Iterate over texts in directory and present each text with a n-dimensional vector according to provided list words
#If the k-th vector has a value i on j-th place it means the word words[j] appears i times in this k-th text
#The last column of the vector is the ground truth label
def get_M(root_dir, words):
    n = len(words)
    M = []
    label = 0 #label
    labels = []
    filenames = []
    subfolders = next(os.walk(root_dir))[1] #get subfolders of folder
    for subfolder in subfolders: #iterate over subfolders
        for filename in os.listdir(os.path.join(root_dir, subfolder)): #iterate over names of files in subfolder
            filenames.append(filename)
            filepath = root_dir + '/' + subfolder + '/' + filename #get a filepath  
            vector = np.zeros(n) #a vector representation of the text file
            file = open(filepath, encoding="Latin-1")
            removelist = " "
            for row in file: #Count the words in a (text) file
                if "Lines" in row: #Only start procesing after the header lines which end with Lines word
                    next(file) #Skip current line and proceed
                    for row in file:                  
                        clean_row = re.sub(r'[^\w'+removelist+']', '',row)
                        for word in clean_row.lower().split():
                            if word in words: #if word appears in words list 
                                vector[words.index(word)] += 1 #add 1 to appropriate dimension
            file.close()
            labels.append(label) #add the label to a label vector
            M.append(vector) #add the vector to the M matrix
        label += 1
    M = np.array(M)
    labels = np.array(labels)
    np.savetxt("filenames.txt", filenames, fmt="%s")
    np.savetxt("M_" + str(n) + ".txt", M, fmt="%s")
    np.savetxt("M_" + str(n) + "_labels.txt", labels , fmt="%s")
    return (M, labels)

#TODO: take a close look at this!!!
#takes an M matrix generated by get_M and returns a tf_idf matrix
def get_tf_idf_M(M, tf = ["bin", "raw", "log", "dnorm"], idf = ["c", "smooth", "max", "prob"], norm_samps=False):
    N = len(M)
    if tf == "raw":
        tf_M = np.copy(M) #just the frequency of the word in a text
#    #TODO: check if dnorm is implemented OK
#    elif tf == "dnorm":
#        tf_M = 0.5 + 0.5*(M/(np.amax(M, axis=1).reshape((N,1))))
    if idf == "c":
        idf_v = []
        for i in range(M.shape[1]): #get the number of texts that contain a word words[i]
            idf_v.append(np.count_nonzero(M[:,i])) #count the non zero values in columns of matrix M
        idf_v = np.array(idf_v)
        idf_v = np.log(N/idf_v)
    tf_idf_M = tf_M*idf_v
    if norm_samps:
        normalizer = Normalizer()
        tf_idf_M = normalizer.fit_transform(tf_idf_M)
    np.savetxt("tf_idf_M_" + str(N) + ".txt", tf_idf_M , fmt="%s")
    return tf_idf_M
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    