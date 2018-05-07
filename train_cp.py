import pandas as pd
import numpy as np 
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, confusion_matrix
from sklearn import ensemble
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB
import sys

class model():
	def __init__(self, model):		
		# clf = SVC()
		# clf.fit(X_train, y_train)
		# y_pred = clf.predict(X_test)
		# print(accuracy_score(y_test, y_pred))
		if model == 'GB':
			params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 2, 'learning_rate': 0.01, 'loss': 'exponential'}
			print('GB')	
			clf = ensemble.GradientBoostingClassifier(**params)
			self.clf = clf
		elif model == 'RF':
			clf = ensemble.RandomForestClassifier(max_depth = 2, random_state = 0)
			self.clf = clf
		elif model == 'SVC':
			clf = SVC()
			self.clf = clf
		elif model == 'NB':
			clf = GaussianNB()
			self.clf = clf
		else:
			sys.exit(1)

	def train(X_train, y_train):
		self.clf.fit(X_train, y_train)

	def predict(self, data):
		return self.clf.predict(data)

df = pd.read_csv("train.csv")
y = df['Choice'].values.tolist()
df = df[['A_follower_count','A_following_count','A_listed_count','A_posts','B_follower_count','B_following_count','B_listed_count','B_posts']]
df['A_follower_following'] = df['A_following_count'] / df['A_follower_count']
df['B_follower_following'] = df['B_following_count'] / df['B_follower_count']
X = df.values
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(X)
X = pd.DataFrame(x_scaled).values.tolist()

m = model(sys.argv[1])
scores = cross_val_score(m.clf, X, y, cv = 10, scoring = 'roc_auc')
print(np.average(scores))
sys.exit()
###
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 42)

m = model(X_train, y_train)

y_pred = m.predict(X_test)
print(confusion_matrix(y_test, y_pred).ravel())
# mse = mean_squared_error(y_test, clf.predict(X_test))
# print("MSE: %.4f" % mse)

###
