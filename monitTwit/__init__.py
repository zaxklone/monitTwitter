from __future__ import print_function

import json
import tweepy as t
from collections import defaultdict, Counter
import itertools



class ProcessTweets:
    #init method for the creditionals
    def __init__(self, ak="",ap="", at="", ats="" ):

        self.auth = None

        self.username = 'unknown'
        self.tweets = None
        self.searchTweets = []
        self.result = None
        self.dayDict = None
        self.interactions = None
   
    def setAuth(self, api_key="",api_secret="", access_token="", access_token_secret="" ):
        try:
            self.auth = t.OAuthHandler( api_key, api_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            return True
        except Error,e :
            print (e)
            return False
      
    def getUserTweets(self, username, last=None):
        api = t.API(self.auth)
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
        api = t.API(self.auth)
        
        try:
            for sess in t.Cursor(api.search, q=searchterm, since_id=last).items(limit):
                s = sess._json
                self.searchTweets.append(s)
        except Exception, e:
            print (e)
            return False
        return True
     
   
    def loadTweets(self, format_='json'):
        file_n = '{0}.json'.format(self.username)
        self.tweets = json.loads(open(file_n, 'r').read())
        return True

    def saveTweets(self):
        tweets_to_dump = self.tweets
        with open('{0}.json'.format(self.username), 'w') as filename:
             print (json.dumps(tweets_to_dump), file=filename) 
        return True

    def updateUserTweets(self):
        if self.username == None:
            return 'Not Possible'

        old_tweet_list = self.tweets 
        self.getUserTweets(self.username, self.tweets[0]['id_str'])
        self.tweets += old_tweet_list
        return True

    def getUserInteractions(self):
        self.getUserRetweets()
        uniq_tweets = self.result['unique_tweets']
        user_mentions = [tweet['entities']['user_mentions'] 
                         for tweet in uniq_tweets
                         if len(tweet['entities']['user_mentions']) >0]
        merged = list(itertools.chain.from_iterable(user_mentions))
        merge_list = [(name[u'screen_name']) for name in merged]
        self.interactions = Counter(merge_list)
        return True
        
              
        
