# Python file for serching
# No longer working on this, Logan took over this

# Imports
from TwitterSearch import *
import datetime

# Authentication varaibles
CONSUMER_KEY = 'glxCFVTU1G99pm3j2ZvJ7QgW8'
CONSUMER_SECRET ='B2uQMSPQDDUnDRFahH8Ybq9G9on2Fcno28E0QGGJXtwpD5z0vK'
OAUTH_TOKEN = '809941682619904000-ntJbBfP85eYfVyTFi6ILGV0GFYJAzzz'
OAUTH_TOKEN_SECRET = 'aGiA9K5SjGMCs0zCvAoJEHOK8rFAswUV9FEpLKRJKocwz'

#search tweets using TWitterSearch module
#install with pip install TwitterSearch
#docs: https://twittersearch.readthedocs.io/en/latest/basic_usage.html


def search_by_hashtag(hashtag, startY, startM, startD, endY, endM, endD, debug=0):

    """
    searches over based on a hashtag and a range of dates
    inputs:
    hashtag: search string
    startY: start year for search
    startM: start month
    startD: start date
    endY: end year for search
    endM: end month
    endD: end date
    debug: prints info to console while working

    returns a dict with:
    the list of tweets for the time range requested
    the number of tweets found
    the number of requests made to the twitter API
    the metadata (dict) returned by twitter 
    """

    

    listOfTweets = []
    stats = []

    try:
        #TwitterSearchOrder object
        tso = TwitterSearchOrder()
        #set options for tso below
        #set search keywords - hashtags for us
        tso.set_keywords([hashtag])
        #set date range using date objects
        start = datetime.date(startY, startM, startD)
        end = datetime.date(endY, endM, endD)
        tso.set_since(start)
        tso.set_until(end)

        #set auth values
        ts = TwitterSearch(
                consumer_key = CONSUMER_KEY,
                consumer_secret = CONSUMER_SECRET,
                access_token = OAUTH_TOKEN,
                access_token_secret = OAUTH_TOKEN_SECRET
            )

        #print out each tweet if debug, add to list
        for tweet in ts.search_tweets_iterable(tso):
            listOfTweets.append(tweet)
            if debug == 1:
                print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))
                print("number of requests: %d, number of tweets found: %d" % (ts.get_statistics()[0], ts.get_statistics()[1]))


    except TwitterSearchException as e: # take care of all those ugly errors if there are some
            print(e)

    

    returnDict = {
        "tweets": listOfTweets,
        "numberOfTweets": ts.get_statistics()[1],
        "numberOfRequests": ts.get_statistics()[0],
        "metadata": ts.get_metadata()
    }

    return returnDict

def example(debug=0):
    #example usage
    #search for #turkey from oct 12 to oct 16 then print number of tweets per day

    results = []
    for day in range(12, 17):
        results.append(search_by_hashtag("#turkey", 2018, 10, day - 1, 2018, 10, day, debug))

    day = 11
    for result in results:
        print("day: %d, number of tweets: %d" % (day, result["numberOfTweets"]))
        day += 1

def searchOverRange(hashtag, startY, startM, startD, endY, endM, endD, debug=0, showTweets=0):
    """
    search over range of days in 1 day intervals
    uses search_by_hashtag() function
    returns a list of result dicts
    """

    results = []
    for day in range(startD, endD):
        results.append(search_by_hashtag("#"+hashtag, startY, startM, day, endY, endM, day + 1, showTweets))

    if debug == 1:
        day = startD
        for result in results:
            print("day: %d, number of tweets: %d" % (day, result["numberOfTweets"]))
            day += 1
    return results