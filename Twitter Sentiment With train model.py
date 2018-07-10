# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 15:06:14 2018

@author: KrRish
"""

import pandas as pd  
import numpy as np
import matplotlib.pyplot as plt
cols = ['sentiment','id','date','query_string','user','text']
df = pd.read_csv("./trainingandtestdata/training.1600000.processed.noemoticon.csv",header=None, names=cols,encoding="ISO-8859–1")
# above line will be different depending on where you saved your data, and your file name
df.head()

df.sentiment.value_counts()
#droping unwanted column
df.drop(['id','date','query_string','user'],axis=1,inplace=True)

#chek negative values
df[df.sentiment==0].head(10)


#checking negative values
df[df.sentiment == 4].head(10)

'''Data Preparation'''
df['pre_clean_len'] = [len(t) for t in df.text]
df['pre_clean_len'].head(10)

#Data Dictionary — first draft
from pprint import pprint
data_dict = {
        'sentiment':{
                'type':df.sentiment.dtype,
                'description':'sentiment class- 0:negative, 1:positive'                
                },
        'text':{
                'type':df.text.dtype,
                'description':'tweet text'
                },
        'pre_clean_len':{
                'type':df.pre_clean_len.dtype,
                'description':'Length of tweet before cleaning'
                },
                'dataset_shape':df.shape
        }
pprint(data_dict)

#creating boxplot to see the overall distribution 
#of length of strins in each entry

fig, ax=plt.subplots(figsize=(5,5))
plt.boxplot(df.pre_clean_len)
plt.show()

#from the graph its showing data length is more than 140
#but twitter allow only 140 character long
df[df.pre_clean_len>=140].head(10)

#data cleaning
df['text'][279]
df.text[492]

#its look like html encoding has not converted to textt
from bs4 import BeautifulSoup
example1=BeautifulSoup(df.text[279],'lxml')
print(example1.get_text())

#now removing the links in data
import re
df.text[0]
re.sub('https?://[\w./]+','',df.text[0])

# UTF-8 BOM (Byte Order Mark)
t=df.text[226]

#testing= bytes(df.text[226],"utf-8")
#testing

t.replace(u"ï¿½","\'")

#hashtag Number
df.text[175]
re.sub("[^a-zA-Z]"," ",df.text[175])

#with all above cleaning method going to create a fun
from nltk.tokenize import sent_tokenize, word_tokenize
#this will remove all user handle with @ and link startedd with https or www
com=r'@[A-Za-z0-9_]+|https?://[^ ]+|www.[^ ]+'

def tweet_cleaner(text):
    soup=BeautifulSoup(text,'lxml')
    souped=soup.get_text()
    try:
        clean=souped.replace(u"ï¿½","?")
    except:
        clean=souped
    stripped=re.sub(com,'',clean)
    words=word_tokenize(stripped)
    lower_case=[x.lower() for x in words]
    lower_case=(" ".join(lower_case)).strip()
    letters_only=re.sub("[^A-Za-z']"," ",lower_case).strip()
    rSpace=re.sub(' +', ' ',letters_only)
    return rSpace
    

#testing function on first 100 results
testing=df.text[:100]
test_result=[]
for t in testing:
    test_result.append(tweet_cleaner(t))
print(test_result)

#applying on whole data set
nums=[0,400000,800000,1200000,1600000]
print("cleaning and parsing the tweets.... \n")
clean_tweet_texts= []
for i in range(nums[0],nums[1]):
    if((i+1)%10000==0):
        print("Tweets %d of %d has been processed "% (i+1 , nums[1]))
    clean_tweet_texts.append(tweet_cleaner(df['text'][i]))

print("cleaning and parsing the tweets.... \n")
for i in range(nums[1],nums[2]):
    if((i+1)%10000==0):
        print("Tweets %d of %d has been processed "% (i+1 , nums[2]))
    clean_tweet_texts.append(tweet_cleaner(df['text'][i]))

print("cleaning and parsing the tweets.... \n")
for i in range(nums[2],nums[3]):
    if((i+1)%10000==0):
        print("Tweets %d of %d has been processed "% (i+1 , nums[3]))
    clean_tweet_texts.append(tweet_cleaner(df['text'][i]))
print(len(clean_tweet_texts))

print("cleaning and parsing the tweets.... \n")
for i in range(nums[3],nums[4]):
    if((i+1)%10000==0):
        print("Tweets %d of %d has been processed "% (i+1 , nums[4]))
    clean_tweet_texts.append(tweet_cleaner(df['text'][i]))
print(len(clean_tweet_texts))

#Saving cleaned Data as CSV
len(clean_tweet_texts)
clean_df=pd.DataFrame(clean_tweet_texts,columns=['text'])
clean_df['target']=df.sentiment
clean_df.head()
print(len(clean_tweet_texts))

#reading in clean dataset
clean_df.to_csv('clean_tweet.csv',encoding='utf-8')
csv='clean_tweet.csv'
my_df=pd.read_csv(csv,index_col=0)
my_df.head()

my_df.info()
nullVal=my_df[my_df.isnull().any(axis=1)]
len(nullVal)
np.sum(my_df.isnull().any(axis=1))