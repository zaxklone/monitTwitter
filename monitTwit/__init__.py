from __future__ import print_function

import json
import tweepy as t
from collections import defaultdict



class ProcessTweets:
    #init method for the creditionals
    def __init__(self, ak="",ap="", at="", ats="" ):
        self.api_key = ak
        self.api_secret = ap
        self.access_token = at
        self.access_token_secret = ats

        self.username = 'unknown'
        self.tweets = None
        self.result = None
        self.dayDict = None


    def getUserTweets(self, username, last=None):
        auth = t.OAuthHandler( self.api_key, self.api_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = t.API(auth)
        self.tweets = []
        self.username = username
        try:
            for sess in t.Cursor(api.user_timeline, screen_name=username, since_id=last).items():
                s = sess._json
                self.tweets.append(s)
        except Exception, e:
            print (e)
            return False
        return True
        
    def getUserRetweets(self):
        self.result = dict()
        non_uniq_tweets = [tweet for tweet in self.tweets if tweet['text'][:2] == 'RT'  ]    
        uniq_tweets = [tweet for tweet in self.tweets if tweet['text'][:2] != 'RT'  ]    
        self.result['non_unique_tweets'] = non_uniq_tweets 
        self.result['unique_tweets'] = uniq_tweets
        return True

    def tweetsByDays(self):
        
        day_tuple = [(tweet['created_at'].split()[0], tweet['created_at'].split()[3]) for tweet in self.tweets]
        self.dayDict = defaultdict(list)
        for day in day_tuple:
            try:
                self.dayDict[day[0]].append(day[1])
            except:
                self.dayDict[day[0]] = [day[1]]

        return True
 
    def getSearchTweets(self, searchterm, last=None, limit=25):
        auth = t.OAuthHandler( self.api_key, self.api_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = t.API(auth)
        self.tweets = []
        
        try:
            for sess in t.Cursor(api.search, q=searchterm, since_id=last).items(limit):
                s = sess._json
                self.tweets.append(s)
        except Exception, e:
            print (e)
            return False
        return True
     
   
    def loadTweets(self, format_='json'):
        file_n = '{0}.json'.format(self.username)
        self.tweets = json.loads(open(file_n, 'r').read())
 
        pass
        
    def saveTweets(self):
        with open(self.username, 'w') as filename:
             print (json.dumps(self.tweets), file=filename) 

        pass         
