import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
#import pymongo
import config #config parameters

keyword = '#DataScience'
filename = 'datascience.json'


class CustomStreamListener(StreamListener):
    def __init__(self, api):
        self.api = api
        super(StreamListener, self).__init__()
        #self.db = pymongo.MongoClient().test

    def on_connect(self):
        print("You are connected to the streaming server.")
 
    def on_data(self, data):
        try:
            #self.db.tweets.insert(json.loads(data))
            with open(filename, 'a') as f:
                f.write(data)
                print(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            #returning False in on_data disconnects the stream
            print('Rate limited. Disconnecting...')
            return False    
        return True


if __name__ == '__main__':
    #Twitter authetification and connection to Twitter Streaming API
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)

    twitter_stream = Stream(auth, CustomStreamListener(api))
    twitter_stream.filter(track=[keyword])
    #GEOBOX_LUX = [5.7357001305,49.4478530884,6.5312485695,50.1827735901]
    #stream_LUX = twitter_stream.filter(locations=GEOBOX_LUX)
    #stream_LUX.filter(track=[keyword])
