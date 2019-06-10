from collections import Counter
import numpy
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
import random
from sklearn.ensemble import RandomForestClassifier
from read_xml import read_json, clean_tweet
from preprocessor import get_twitter_data


def test_model(model, attributes, labels):
  # Test model
  actual = numpy.array(labels)

  test_result = model.predict(attributes)
  pred = numpy.array(test_result)

  # Transform male = 1, female = 0
  actual_calc = []
  pred_calc = []

  for value in actual:
    if value == 'male':
      actual_calc.append(1)
    else:
      actual_calc.append(0)

  for value in pred:
    if value == 'male':
      pred_calc.append(1)
    else:
      pred_calc.append(0)

  accuracy = accuracy_score(actual_calc, pred_calc) * 100
  precision = precision_score(actual_calc, pred_calc) * 100
  recall = recall_score(actual_calc, pred_calc) * 100
  f1 = f1_score(actual_calc, pred_calc) * 100
  print("Accuracy: ", accuracy)
  print("Precision: ", precision)
  print("Recall: ", recall)
  print("F1 score: ", f1)


def predict_gender(account):
  train_data = read_json("gender/tweet_token_train.json")
  test_data = read_json("gender/tweet_token_test.json")


  account_tweets = get_twitter_data(account, 200)['tweets']

  tokenized_account_tweets = []
  for tweet in account_tweets:
    tokenized_account_tweets.extend(clean_tweet(tweet))

  # Create lists with all words mentioned by males and female
  male_words = []
  female_words = []
  for key, value in train_data.items():
    if value["gender"] == "male":
      male_words.extend(value["tweets"])
    elif value["gender"] == "female":
      female_words.extend(value["tweets"])

  # Find the 500 most common words for male and female
  male_top_500 = Counter(male_words).most_common(500)
  female_top_500 = Counter(female_words).most_common(500)

  top_words_male = []
  top_words_female = []

  for word in male_top_500:
    top_words_male.append(word[0])
  for word in female_top_500:
    top_words_female.append(word[0])
  
  # Create a new set containing the symmetric difference between the two sets
  top_words = set(top_words_male) ^ set(top_words_female)

  # Find attributes and labels for training data
  training_attributes = []
  training_labels = []
  train_keys = list(train_data.keys())
  random.shuffle(train_keys)
  for key in train_keys:
    value = train_data[key]
    account_attributes = []
    training_labels.append(value['gender'])
    for word in top_words:
      account_attributes.append(value['tweets'].count(word))
    training_attributes.append(account_attributes)

  # Find attributes and labels for test data
  test_attributes = []
  test_labels = []
  test_keys = list(test_data.keys())
  random.shuffle(test_keys)
  for key in test_keys:
    value = test_data[key]
    account_attributes = []
    test_labels.append(value['gender'])
    for word in top_words:
      account_attributes.append(value['tweets'].count(word))
    test_attributes.append(account_attributes)

  account_attributes = []
  for word in top_words:
    account_attributes.append(tokenized_account_tweets.count(word))


  random_forest_model = RandomForestClassifier(1000).fit(training_attributes, numpy.ravel(training_labels))
  predicted = random_forest_model.predict_proba([account_attributes])

  #test_model(random_forest_model, test_attributes, test_labels)

  return predicted[0]
