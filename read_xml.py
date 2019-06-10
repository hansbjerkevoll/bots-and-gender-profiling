from xml.dom import minidom
import string
import re
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import json

stopwords_english = stopwords.words("english")

def clean_tweet(tweet):
  tweet = tweet.lower()
  # remove stock market tickers like $GE
  tweet = re.sub(r'\$\w*', '', tweet)

  # remove old style retweet text "RT"
  tweet = re.sub(r'^rt[\s]+', '', tweet)

  # remove hyperlinks
  tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)

  # remove hashtags
  # only removing the hash # sign from the word
  tweet = re.sub(r'#', '', tweet)

  # tokenize tweets
  tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
  tweet_tokens = tokenizer.tokenize(tweet)

  tweet_clean = []    
  for word in tweet_tokens:
      if (word not in stopwords_english and # remove stopwords
            word not in string.punctuation): # remove punctuation
          tweet_clean.append(word)

  return tweet_clean


def read_account(account):
  account_xml = minidom.parse("dataset_gender/en/{}.xml".format(account[0]))
  items = account_xml.getElementsByTagName("document")

  raw_tweets = []
  for item in items:
    raw_tweets.append(item.childNodes[0].data.replace("\n", " "))

  tokenized_tweets = []
  for tweet in raw_tweets:
    tokenized_tweets.extend(clean_tweet(tweet))
  
  return tokenized_tweets


def create_account_data(path):
  with open(path, "r") as f:
    accounts = [account.split(":::") for account in f.readlines()]
  return accounts


def create_twitter_data(path, target_path):
  print("Creating twitter data from {}".format(path))
  train_accounts = create_account_data(path)
  tweet_dict = {}
  for account in train_accounts:

    tweet_dict[account[0]] = {
          'gender': account[2].strip(),
          'tweets': read_account(account)
        }

  with open(target_path, "w") as f:
    json.dump(tweet_dict, f)
      

def read_json(file):
  with open(file, "r") as f:
    data = json.load(f)
  return data

def create_account_list(path):
  with open(path, "r") as f:
    accounts = [accounts.split(":::")[0] for accounts in f.readlines]
  return accounts


if __name__ == "__main__":
  create_twitter_data("dataset_gender/truth/truth-train.txt", "gender/tweet_token_train.json")
  create_twitter_data("dataset_gender/truth/truth-dev.txt", "gender/tweet_token_test.json")
