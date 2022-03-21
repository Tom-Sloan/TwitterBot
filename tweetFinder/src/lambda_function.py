import os
import random
import json
from pathlib import Path
import tweepy
import csv
import requests
import dictnodefinder
import io
from PIL import Image
# python -m venv venv
# venv\Scripts\activate.bat

ROOT = Path(__file__).resolve().parents[0]


def get_tweet(tweets_file, excluded_tweets=None):
    """Get tweet to post from CSV file"""

    with open(tweets_file) as csvfile:
        reader = csv.DictReader(csvfile)
        possible_tweets = [row["tweet"] for row in reader]

    if excluded_tweets:
        recent_tweets = [status_object.text for status_object in excluded_tweets]
        possible_tweets = [tweet for tweet in possible_tweets if tweet not in recent_tweets]

    selected_tweet = random.choice(possible_tweets)

    return selected_tweet

def get_url(dic):
    for key, value  in dic.items():
        if key == 'media_url':
            print(key, value)
        
        



def lambda_handler(event, context):
    print("Get credentials")
    
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")


    print("Authenticate")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    print("Get mentions")
    mentions = api.mentions_timeline(trim_user=True,include_entities=False, count=2)
    # print(json.dumps(mentions, indent=4))



    for mention in mentions:
        for media in mention["extended_entities"]['media']:
            url = media['media_url']
    
        f_ext = os.path.splitext(url)[-1]
        f_name = mention['id_str']

        print( f_name + f_ext)
        response = requests.get(url)

        with open(f_name, 'wb') as f:
            f.write(response.content)
        
        image = Image.open(io.BytesIO(response.content))
        image.show()
        
        print(response)
    # img = PIL.Image.open(image_bytes)
    # img.show()
    return {"statusCode": 200}
