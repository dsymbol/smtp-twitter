from utils import twitter_stream
from urllib3.exceptions import ProtocolError

if __name__ == "__main__":
    while True:
        try:
            ts = twitter_stream.TweetBot()
            ts.fetch_tweets()
        except ProtocolError:
            continue
