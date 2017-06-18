from sklearn import svm
from sklearn.metrics import accuracy_score, f1_score, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
import csv

filename = 'training_data_1.csv'

def to_float_or_0(elem):
	try:
		return float(elem)
	except:
		return 0

def get_relevant_features(row):
	processed_row = [to_float_or_0(x) for x in row]
	processed_row[2] = 0
	return int(row[2]), processed_row

def produce_data_from_filename(filepath):
	data = []
	Y = []
	with open(filepath, 'rt') as csvfile:
		reader = csv.reader(csvfile)
		next(reader, None)
		for row in reader:
			y,x_row = get_relevant_features(row)
			Y.append(y)
			data.append(x_row)

	return data, Y


rf = RandomForestClassifier(max_depth=5, n_estimators=10, class_weight="balanced")

data, Y = produce_data_from_filename(filename)

x_train, x_test, y_train, y_test = train_test_split(data, Y, test_size = 0.1, random_state = 123)

# x_train, y_train = sm.fit_sample(x_train, y_train)

rf.fit(x_train, y_train)
from sklearn.externals import joblib
joblib.dump(clf, 'rfclassifier.pkl') 


