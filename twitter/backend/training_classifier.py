import numpy as np 
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import recall_score, precision_score, f1_score 
from sklearn.metrics import accuracy_score, confusion_matrix


# ===================================
# FOR EXCEL MANIPULATION 
import openpyxl 
from openpyxl import Workbook
# ===================================

# In order to run the naive bayes traing model, the file must have the required format for the system.
def naive_bayes(file, t_size, state, averaging):
	data = pd.read_json(file)
	data.sort_index(inplace = True)


	# labels = set()
	# for i in range(data.shape[0]):
	# 	labels.add(data.iat[i,1])
	labels = (1,2,3,4)
	vectorizer = CountVectorizer(stop_words='english', strip_accents='unicode')
	all_features = vectorizer.fit_transform(data.tweets)
	
	feature_shape = all_features.shape
	vector_vocab = vectorizer.vocabulary_
	feature = all_features
	

	x_train, x_test, y_train, y_test = train_test_split(all_features, data.topic, test_size= float(t_size), random_state= int(state))

	train_shape = [x_train.shape, y_train.shape]
	test_shape = [x_test.shape, y_test.shape]

	# TRAINING OF THE MODEL
	classifier = MultinomialNB()
	classifier.fit(x_train,y_train)


	 # ==========
	y_pred = classifier.predict(x_test)
	# acc_score = accuracy_score(y_test, y_pred)

	conf_mat = confusion_matrix(y_test, y_pred, labels = list(labels))
	print(conf_mat)
	# ==========

	num_correct = (y_test == classifier.predict(x_test)).sum()
	num_incorrect = y_test.size -num_correct

	# fraction = classifier.score(x_test, y_test) 
	accuracy = str(round(num_correct/ (num_incorrect + num_correct)*100,4))+ ' %'
	recall = str(round((recall_score(y_test, classifier.predict(x_test),  average=averaging))* 100, 4)) + ' %'
	precision = str(round((precision_score(y_test, classifier.predict(x_test),  average=averaging))* 100, 4)) + ' %'
	f1 = str(round((f1_score(y_test, classifier.predict(x_test),  average=averaging))* 100, 4)) + ' %'
	# matrix = vectorizer.transform(sample)
	# print(classifier.predict(matrix))
	scores = {
		# 'confusion_matrix': conf_mat,
		'correct': num_correct,
		'incorrect': num_incorrect,
		'accuracy': accuracy,
		'recall': recall,
		'precision': precision,
		'f1_score': f1
	}
	return classifier, scores, vectorizer
