# smtp-twitter

Stream tweets from any Twitter account to your email using gmail's smtp server

## Guide

Get Twitter API and Access Keys
    
    https://developer.twitter.com/en

Allow less secure app access

    https://myaccount.google.com/lesssecureapps

Open config.py and fill the "email" and "twitter" sections with your data

```
{
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
        "followed_users": [
            "LILUZIVERT",
            "Cristiano"
        ]
    }
}
```

## Install

There are two ways to begin using smtp-twitter, depending on your preference:

### Manual

```bash
git clone https://github.com/dsymbol/smtp-twitter
cd smtp-twitter
pip install -r requirements.txt
python main.py
```

### Docker

```bash
git clone https://github.com/dsymbol/smtp-twitter
cd smtp-twitter
docker build -t smtp-twitter .
docker run -d --name smtp-twitter -v `pwd`/config.py:/app/config.py smtp-twitter:latest
```

