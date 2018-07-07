# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 19:52:20 2018

@author: KrRish
"""

import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
class TwitterClient(object):
    def __init__(self):
        #login with twiiter
        # go to https://apps.twitter.com/app/new and create new prooject
        #get consumer key and secret ket paste and run
        consumer_key=""
        consumer_secret=""
        access_token=""
        access_token_secret=""
        try:
            self.auth=OAuthHandler(consumer_key,consumer_secret)
            self.auth.set_access_token(access_token,access_token_secret)
            self.api=tweepy.API(self.auth)
        except:
            print:("Error : Authentication Failed")
    def clean_tweet(self,tweet):
        return ' '.join(re.sub("(@[A-Xa-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/S+)"," ",tweet).split())
    def get_tweet_sentiment(self,tweet):
        analysis=TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity >0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    
    def get_tweets(self,query,count = 10):
        tweets = []
        try:
            fetched_tweets = self.api.search(q=query , count =count)
            
            for tweet in fetched_tweets:
                parsed_tweet = {}
                # saving text of tweet
                parsed_tweet['text']=tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment']=self.get_tweet_sentiment(tweet.text)
                
                if tweet.retweet_count>0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
        
        except tweepy.TweepError as e:
            print("Error: " + str(e))
            
            
def main():
    api=TwitterClient()
      # calling function to get tweets
    tweets = api.get_tweets(query= 'Arvind Kejriwal',count= 200 )
    
      # picking positive tweets from tweets
    ptweets=[tweet for tweet in tweets if tweet['sentiment']=='positive']
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
      # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
      # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
      # percentage of neutral tweets
  #  print("Neutral tweets percentage: {} %".format(100*len(set(tweets) - set(ntweets) - set(ptweets))/len(tweets)))
        # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])
     
      # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])
      
if __name__ == "__main__":
    # calling main function
    main()

                
                
        
