from bot_prediction import test_model, predict_bot
from create_training_data import feature_extraction
from gender_prediction import predict_gender

import warnings

def main():
  account = input("Twitter username: @")
  features, account_exists = feature_extraction(account)

  if not account_exists:
    print("{} is not a valid twitter handle".format(account))
    return


  predicted_bot = predict_bot("twitter_data/bot/bot_training_data.csv", features)

  if predicted_bot[0] > 0.5:
    bot_result = "HUMAN"
    prob_bot = predicted_bot[0]
  else:
    bot_result = "BOT"
    prob_bot = predicted_bot[1]

  print("We predict @{} is a {} with a probability of {}%".format(account, bot_result, round(prob_bot * 100, 1)))
  print()

  if bot_result == "BOT":
    return

  should_predict_gender = input("Do you want to predict the gender of @{} (y / n): ".format(account)).lower()
  if should_predict_gender != "y" and should_predict_gender != "yes":
    return

  # print("Trying to predict gender (This may take a while. It's hard okay...)")
  predicted_gender = predict_gender(account)
  if predicted_gender[0] > 0.5:
    gender_result = "FEMALE"
    prob_gender = predicted_gender[0]
  else:
    gender_result = "MALE"
    prob_gender = predicted_gender[1]
  print(
    "We predict @{} is a {} with a probability of {}%".format(account, gender_result, round(prob_gender * 100, 1)))
  print()


if __name__ == "__main__":
    warnings.simplefilter(action="ignore", category=FutureWarning)
    main()
