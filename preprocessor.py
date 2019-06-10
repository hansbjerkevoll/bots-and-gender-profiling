import tweepy

consumer_key = "LqZEmCpMMaHS6fgxr4J0OVawP"
consumer_secret = "HeTmwvVd0NDFrdvz9j4uNNhNFYhA7rrBKMSE6MxkS5DnVx4VKH"

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_twitter_data(account, count):
  try:
    timeline = api.user_timeline(screen_name=account, count=count, tweet_mode="extended")
    user = api.get_user(screen_name=account)
    name = user.name
    followers_count = user.followers_count
    friends_count = user.friends_count
    created = user.created_at.timestamp()
    listed_count = user.listed_count
    statuses_count = user.statuses_count
    favourites_count = user.favourites_count
    verified = user.verified
    tweets = [tweet.full_text.replace("\n", " ") for tweet in timeline]

    twitter_data = {
      "account": account,
      "name": name,#.encoding("utf-8"),
      "followers_count": followers_count,
      "friends_count": friends_count,
      "listed_count": listed_count,
      "statuses_count": statuses_count,
      "account_age": created,
      "favourites_count": favourites_count,
      "verified": verified,
      "tweets": tweets
    }

    return twitter_data
  except:
    return None
