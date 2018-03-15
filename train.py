import pandas as pd
import numpy as np 
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import ensemble
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error

df = pd.read_csv("train.csv")
y = df['Choice'].values.tolist()
df = df.drop(['Choice'], axis = 1)
X = df.values.tolist()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 42)

# clf = SVC()
# clf.fit(X_train, y_train)
# y_pred = clf.predict(X_test)
# print(accuracy_score(y_test, y_pred))

params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 2,
          'learning_rate': 0.01, 'loss': 'exponential'}

clf = ensemble.GradientBoostingClassifier(**params)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
# print(y_pred)
print(accuracy_score(y_test, y_pred))
# mse = mean_squared_error(y_test, clf.predict(X_test))
# print("MSE: %.4f" % mse)


