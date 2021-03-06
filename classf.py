import numpy as np
import pandas as pd



phish=pd.read_csv("dataset.csv")


phish= phish.drop("id",axis=1)
print(phish.columns)





from sklearn.model_selection import train_test_split
train_set, test_set = train_test_split(phish, test_size=0.2, random_state=42)
print(f"Rows in train set: {len(train_set)}\nRows in test set: {len(test_set)}\n" )

from sklearn.model_selection import StratifiedShuffleSplit
split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(phish, phish['Result']):
     strat_train_set = phish.loc[train_index]
     strat_test_set = phish.loc[test_index]



phish = strat_train_set.drop("Result", axis=1)
phish_labels = strat_train_set["Result"].copy()

print(phish_labels)

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=62,random_state=42)
model.fit(phish, phish_labels)

# some_data = phish.iloc[:5]
# some_labels = phish_labels.iloc[:5]
# model.predict(some_data)
# list(some_labels)

from sklearn.metrics import mean_squared_error
phish_check = model.predict(phish)
mse = mean_squared_error(phish_labels, phish_check)
rmse = np.sqrt(mse)
print(rmse)
from sklearn.model_selection import cross_val_score
scores= cross_val_score(model,phish, phish_labels, scoring="neg_mean_squared_error",cv=10)
rmse_scores = np.sqrt(-scores)

print(rmse_scores)

def print_scores(scores):
    print("Scores:",scores)
    print("Standard deviation:", scores.std())

print_scores(rmse_scores)


import pickle
file_name = "RandomForrestModel.sav"
pickle.dump(model,open(file_name,'wb'))



X_test=strat_test_set.drop("Result",axis=1)
Y_test= strat_test_set["Result"].copy()
final_predictions = model.predict(X_test)
final_mse = mean_squared_error(Y_test, final_predictions)
final_rmse = np.sqrt(final_mse)
print(final_predictions, list(Y_test))

print(final_rmse)


from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

print(confusion_matrix(Y_test,final_predictions))
print(classification_report(Y_test,final_predictions))
print(accuracy_score(Y_test, final_predictions))