import tweepy
import yaml
from datetime import date

# Load the authorization keys
try:
    yaml_file = open('config.yaml', 'r')
    p = yaml.load(yaml_file, Loader=yaml.FullLoader)
except:
    print('Tweeting process: Having problems reading/parsing config.yaml, aborting.')
    exit()

try:
    consumer_key = p['api_key']
    consumer_secret = p['api_secret']
    access_token = p['access_token']
    access_secret = p['access_secret']
    bearer_token = p['bearer_token']
except ValueError:
    print('Tweeting process: Key not found in the yaml file, aborting.')
    exit()


def send_tweet(tweet):
    """
    Given a string representing the solution of the wordle bot, style it and Tweet
    """
    # Convert from x/g/y used by our bot to colorful square emoji
    twitter_dict = {'x': '\U00002B1C', 'g': '\U0001F7E9', 'y': '\U0001F7E8'}
    # Leave endline characters unchanged
    formatted_tweet = ''.join([twitter_dict.get(c, c) for c in tweet])

    # Add introduction
    today = str(date.today())
    formatted_tweet = "Solution of Wordle obtained by my bot for " + today + ":\n" + formatted_tweet

    # Create a client and tweet
    client = tweepy.Client(
                            bearer_token = bearer_token,
                            consumer_key=consumer_key,
                            consumer_secret=consumer_secret,
                            access_token=access_token,
                            access_token_secret=access_secret
                            )

    client.create_tweet(text = formatted_tweet)
