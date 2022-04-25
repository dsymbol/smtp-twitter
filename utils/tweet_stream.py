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


class TwB:
    def __init__(self):
        self.auth = tp.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
        self.fetch_tweets()

    def fetch_tweets(self):
        listener = DataStream(api_key, api_key_secret, access_token, access_token_secret)
        account_list = self.name_to_id(followed_users)
        listener.filter(follow=account_list)

    def name_to_id(self, users):
        api_object = tp.API(self.auth)
        list_id = []
        for i in users:
            user = api_object.get_user(screen_name=str(i))
            id = user.id
            list_id.append(str(id))
        TwB.welcome_message()
        return list_id

    @staticmethod
    def welcome_message():
        print("""
         ^ ^
        (O,O)
        (   ) WAITING FOR TWEETS
        -"-"------------------------
        """)


class DataStream(tp.Stream):
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
                send_email(email, password, receiver, subject, message)
        except:
            pass
        return True

    def on_error(self, status_code):
        if status_code == 420:
            return False


if __name__ != "__main__":
    config = load_config()
    api_key, api_key_secret, access_token, access_token_secret, followed_users = config["twitter"].values()
    email, password, receiver = config["email"].values()
