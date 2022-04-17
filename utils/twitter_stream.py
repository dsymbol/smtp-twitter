from utils.smtp import send_email
from utils.schema_check import config_is_valid
import tweepy as tp
import json


def load_config():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        config_is_valid(config)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        with open('config.json', 'w') as f:
            config = {
                "email": {
                    "email": "me@gmail.com",
                    "password": "password",
                    "receiver": "receiver@gmail.com"
                },
                "twitter": {
                    "api_key": "your_api_key",
                    "api_key_secret": "your_api_key_secret",
                    "access_token": "your_access_token",
                    "access_token_secret": "your_access_token_secret",
                    "followed_users": ["LILUZIVERT", "Cristiano"]
                }
            }
            json.dump(config, f, indent=4)
        raise Exception("Missing values in config.json")
    return config


def email_subject(user, text):
    if len(text) > 31:
        sliced_text = [i for i in text]
        sliced_text = "".join(sliced_text[:31]) + "..."
        message = f"{user} Tweeted: {sliced_text}"
    else:
        message = f"{user} Tweeted: {text}"
    return message


class TwitterStream(tp.StreamListener):
    def __init__(self):
        super().__init__()
        self.email, self.password, self.receiver = load_config()["email"].values()

    def on_data(self, data):
        try:
            d = json.loads(data)
            tw_screen_name = d['user']['screen_name']
            reply = d['in_reply_to_screen_name']
            tweet_id = d['id_str']
            tweet_link = f"https://twitter.com/{tw_screen_name}/status/{tweet_id}"
            if 'extended_tweet' in d:
                text = d['extended_tweet']['full_text']
            else:
                text = d['text']
            if str(reply) == 'None' and 'RT @' not in text:
                subject = email_subject(tw_screen_name, text)
                message = f'@{tw_screen_name}\n{text}\nVia: {tweet_link}'
                print(f'@{tw_screen_name}\n{text}\n')
                send_email(self.email, self.password, self.receiver, subject, message)
        except:
            pass

        return True

    def on_error(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            return False


class TweetBot():
    def __init__(self):
        self.api_key, self.api_key_secret, \
            self.access_token, self.access_token_secret, \
                self.followed_users = load_config()["twitter"].values()

    def authorize(self):
        autho = tp.OAuthHandler(self.api_key, self.api_key_secret)
        autho.set_access_token(self.access_token, self.access_token_secret)
        return autho

    def fetch_tweets(self):
        api = self.authorize()
        api.get_username()
        TweetBot.welcome_message()
        listener = TwitterStream()
        account_list = self.get_tweet_acid(self.followed_users)
        stream_tweet = tp.Stream(api, listener, tweet_mode='extended')
        stream_tweet.filter(follow=account_list)

    def get_tweet_acid(self, user_list):
        api = self.authorize()
        api_object = tp.API(api)
        list_id = []
        for i in user_list:
            user = api_object.get_user(screen_name=str(i))
            id = user.id
            list_id.append(str(id))
        return list_id

    @staticmethod
    def welcome_message():
        print("""
         ^ ^
        (O,O)
        (   ) WAITING FOR TWEETS
        -"-"------------------------
        """)
