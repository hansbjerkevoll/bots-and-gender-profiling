import pandas as pd
import datetime
from preprocessor import get_twitter_data

def get_mean_tweet_length(tweets):
    sum_length = 0
    for tweet in tweets:
        sum_length += len(tweet)
    return round(sum_length / len(tweets), 2)


def lexical_diversity_text(text):
    if len(text) == 0:
        diversity = 0
    else:
        diversity = float(len(set(text))) / len(text)
    return diversity


def lexical_diversity(tweets):
    sum_diversity = 0
    for tweet in tweets:
        sum_diversity += lexical_diversity_text(tweet)
    return round(sum_diversity / len(tweets), 2)


def feature_extraction(account):
    account_data = pd.DataFrame()
    twitter_data = get_twitter_data(account, 200)
    if not twitter_data:
        return None, False
    if not len(twitter_data['tweets']) > 0:
        print("@{} has no tweets...".format(account))
        return None, False
    account_data.set_value(account,'followers_count', twitter_data['followers_count'])
    account_data.set_value(account,'friends_count', twitter_data['friends_count'])
    account_data.set_value(account,'listed_count', twitter_data['listed_count'])
    account_data.set_value(account,'statuses_count', twitter_data['statuses_count'])
    account_data.set_value(account,'account_age_seconds', int(datetime.datetime.now().timestamp() - twitter_data['account_age']))
    account_data.set_value(account,'favourites_count', twitter_data['favourites_count'])
    account_data.set_value(account,'verified', twitter_data['verified'])
    account_data.set_value(account,'diversity', lexical_diversity(twitter_data['tweets']))
    account_data.set_value(account,'mean_tweet_length', get_mean_tweet_length(twitter_data['tweets']))
    return account_data, True

def feature_extraction2(account):
    twitter_data = get_twitter_data(account, 200)
    return { 
        'followers_count': twitter_data['followers_count'],
        'friends_count': twitter_data['friends_count'],
        'listed_count': twitter_data['listed_count'],
        'statuses_count': twitter_data['statuses_count'],
        'account_age_seconds': int(datetime.datetime.now().timestamp() - twitter_data['account_age']),
        'favourites_count': twitter_data['favourites_count'],
        'verified': twitter_data['verified'],
        'diversity': lexical_diversity(twitter_data['tweets']),
        'mean_tweet_length': get_mean_tweet_length(twitter_data['tweets'])
     }


def create_bot_account_data(train_data):
    for index, row in train_data.iterrows():
        twitter_data = get_twitter_data(row['account'], 200)
        if not twitter_data:
            train_data.set_value(index, 'deactivated_account', 'TRUE')
            continue
        if len(twitter_data['tweets']) == 0:
            train_data.set_value(index, 'deactivated_account', 'TRUE')
            continue
        train_data.set_value(index, 'followers_count', twitter_data['followers_count'])
        train_data.set_value(index, 'friends_count', twitter_data['friends_count'])
        train_data.set_value(index, 'listed_count', twitter_data['listed_count'])
        train_data.set_value(index, 'statuses_count', twitter_data['statuses_count'])
        train_data.set_value(index, 'account_age_seconds', int(datetime.datetime.now().timestamp() - twitter_data['account_age']))
        train_data.set_value(index, 'favourites_count', twitter_data['favourites_count'])
        train_data.set_value(index, 'verified', twitter_data['verified'])
        train_data.set_value(index, 'diversity', lexical_diversity(twitter_data['tweets']))
        train_data.set_value(index, 'mean_tweet_length', get_mean_tweet_length(twitter_data['tweets']))
    return train_data

if __name__ == '__main__':

    # Read raw training data and produce tranining data output
    raw_data = pd.read_csv('twitter_data/bot/raw_training_data.csv', encoding='latin-1')
    training_data = create_bot_account_data(raw_data)
    training_data.to_csv('twitter_data/bot/bot_training_data.csv')

    # Read raw test data and produce test data output
    raw_test_data = pd.read_csv('twitter_data/bot/raw_test_data.csv', encoding='latin-1')
    test_data = create_bot_account_data(raw_test_data)
    test_data.to_csv('twitter_data/bot/bot_test_data.csv')
