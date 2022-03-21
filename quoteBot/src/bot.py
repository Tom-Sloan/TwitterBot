import json
import random
import time
import sys
import tweepy
import os
import requests
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[0]


authors = [
    {
        'first': 'Marcus',
        'last': 'Aurelius'
    }
]

def get_quotes():
    quotes_user_id = os.getenv("QUOTES_USER_ID")
    quotes_token = os.getenv("QUOTES_TOKEN")
    response = requests.get('https://www.stands4.com/services/v2/quotes.php?uid='+quotes_user_id+'&tokenid='+quotes_token+'&searchtype=AUTHOR&query='+ authors[0]['first']+'+'+authors[0]['last']+'&format=json')
    if response.status_code == 200:
        response = response.json()
        # To display all returned quotes
        # print(json.dumps(response, indent=4))
        return response['result']
        
    with open('data.json') as f:
        quotes_json = json.load(f)
    return quotes_json['quotes']

def get_random_quote():
    quotes = get_quotes()

    
    # old_quotes = {}
    # with open('old_quotes.json', 'r', encoding='utf-8') as f:
    #     old_quotes = json.load(f)
    #     isUnique = False
    #     while not isUnique:
    #         random_quote = random.choice(quotes)
            
    #         author = random_quote['author']
    #         quote = random_quote['quote']
            
    #         for value in old_quotes['used']:
    #             if value['author'] in author:
    #                 if quote in value['quote']:
    #                     continue
    #                 old_quotes['used'][0]['quote'].append(quote)   
    #             else:
    #                 old_quotes['used'].append({"author":author, "quote":[quote]})
    #         isUnique = True

    # with open('old_quotes.json', 'w', encoding='utf-8') as f:
    #     json.dump(old_quotes, f, ensure_ascii=False, indent=4)

    return random.choice(quotes)

def create_tweet():
    
    while True:
        quote = get_random_quote()
        tweet = """
                {}
                ~{}
                """.format(quote['quote'], quote['author'])
        if len(tweet)<260:
            break
    
    return tweet

   

def lambda_handler(event, context):
    print("Get credentials")
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    print("Authenticate")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    print("Get tweet from csv file")
    tweets_file = ROOT / "tweets.csv"
    recent_tweets = api.user_timeline()[:100]
    # tweet = get_tweet(tweets_file, recent_tweets)
    tweet = create_tweet()

    print(f"Post tweet: {tweet}")
    api.update_status(tweet)

    return {"statusCode": 200, "tweet": tweet}