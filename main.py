from utils.tweet_stream import TwB
from urllib3.exceptions import ProtocolError, ReadTimeoutError

if __name__ == "__main__":
    while True:
        try:
            ts = TwB()
        except (ProtocolError, ReadTimeoutError):
            continue
