import tweepy
import time 
import sqlite3
import json 

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

#        replace sqlite3.server with "localhost" if you are running via your own server!
#                        server       sqlite3 username	sqlite pass  Database name.

conn = sqlite3.connect("sqlite3.server","beginneraccount","cookies","beginneraccount$tutorial")

c = conn.cursor()


print ("   Your application name: "),
app_name = input()

print ("   Your consumer key: "),
ckey = input()

print ("   Your consumer secret: "),
csecret = input()
atoken,asecret = tweepy.oauth_dance(app_name,ckey,csecret)
class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        
        tweet = all_data["text"]
        
        username = all_data["user"]["screen_name"]
        
        c.execute("INSERT INTO taula (time, username, tweet) VALUES (%s,%s,%s)",
            (time.time(), username, tweet))

        conn.commit()
        print((username,tweet))
        
        return True

    def on_error(self, status):
        print (status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
print (" Enter tweet Keyword : "),
key=input()
twitterStream.filter(track=key)