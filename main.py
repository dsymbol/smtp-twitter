from utils import twitter_stream

if __name__ == "__main__":
    ts = twitter_stream.TweetBot()
    ts.fetch_tweets()
