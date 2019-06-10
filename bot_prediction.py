import pandas as pd
import numpy
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import normalize

attributes = ['followers_count', 'friends_count', 'listed_count', 'favourites_count', 'verified',
                  'statuses_count', 'account_age_seconds', 'diversity', 'mean_tweet_length']

def predict_bot(train_data_path, test_data):
    training_data = pd.read_csv(train_data_path, encoding='latin-1')

    # Fetch the data attributed needed
    training_attr = normalize(training_data[attributes])
    test_attr = normalize(test_data[attributes])
    training_label = training_data[['bot']]
   
    model = RandomForestClassifier(100).fit(training_attr, numpy.ravel(training_label))

    predict = model.predict_proba(test_attr)
    return predict[0]

def test_model():

    training_data = pd.read_csv('twitter_data/bot/bot_training_data.csv', encoding='latin-1')
    test_data = pd.read_csv('twitter_data/bot/bot_test_data.csv', encoding='latin-1')

    # Fetch the data attributed needed
    training_attr = normalize(training_data[attributes])
    test_attr = normalize(test_data[attributes])

    training_label = training_data[['bot']]
    test_label = test_data[['bot']]
   
    model = RandomForestClassifier(100).fit(training_attr, numpy.ravel(training_label))
    actual = numpy.array(test_label)
    predicted = model.predict(test_attr)
    pred = numpy.array(predicted)

    accuracy = accuracy_score(actual, pred) * 100
    precision = precision_score(actual, pred) * 100
    recall = recall_score(actual, pred) * 100
    f1 = f1_score(actual, pred) * 100
    print("Accuracy: ", accuracy)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1 score: ", f1)
    

if __name__ == "__main__":
    test_model()
