import json
import random
import time
import sys
import tweepy
from os import environ
import requests

consumer_key = environ['API_KEY']
consumer_secret_key = environ['API_SECRET_KEY']
access_token = environ['ACCESS_TOKEN']
access_token_secret = environ['ACCESS_TOKEN_SECRET']

quotes_user_id = environ['QUOTES_USER_ID']

quotes_token = environ['QUOTES_TOKEN']

authors = [
    {
        'first': 'Marcus',
        'last': 'Aurelius'
    }
]

def get_quotes():
    response = requests.get('https://www.stands4.com/services/v2/quotes.php?uid='+quotes_user_id+'&tokenid='+quotes_token+'&searchtype=AUTHOR&query='+ authors[0]['first']+'+'+authors[0]['last']+'&format=json')
    if response.status_code == 200:
        response = response.json()
        return response['result']
        
    with open('data.json') as f:
        quotes_json = json.load(f)
    return quotes_json['quotes']

def get_random_quote():
    quotes = get_quotes()
    
    old_quotes = {}
    with open('old_quotes.json', 'r', encoding='utf-8') as f:
        old_quotes = json.load(f)
        isUnique = False
        while not isUnique:
            random_quote = random.choice(quotes)
            
            author = random_quote['author']
            quote = random_quote['quote']
            
            for value in old_quotes['used']:
                if value['author'] in author:
                    if quote in value['quote']:
                        continue
                    old_quotes['used'][0]['quote'].append(quote)   
                else:
                    old_quotes['used'].append({"author":author, "quote":[quote]})
            isUnique = True

    with open('old_quotes.json', 'w', encoding='utf-8') as f:
        json.dump(old_quotes, f, ensure_ascii=False, indent=4)

        # json.dump(random_quote, f, ensure_ascii=False, indent=4)

    return random_quote

def create_tweet():
    
    quote = get_random_quote()
    tweet = """
            {}
            ~{}
            """.format(quote['quote'], quote['author'])
    return tweet

def tweet_quote():
    interval = 60*24*24

    # auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    # auth.set_access_token(access_token, access_token_secret)
    # api = tweepy.API(auth)

    # tweet = create_tweet()
    # api.update_status(tweet)

    while True:
        print('getting a random quote...')        
        tweet = create_tweet()
        # api.update_status(tweet)
        print(tweet)
        time.sleep(interval) 
        
   

if __name__ == "__main__":
    tweet_quote()
