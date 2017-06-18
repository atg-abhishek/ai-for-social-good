from sklearn import svm
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import csv

filename = 'all_data_R.csv'

def to_float_or_0(elem):
	try:
		return float(elem)
	except:
		return 0

def get_relevant_features(row):
	processed_row = [to_float_or_0(x) for x in row]
	return str(row[0]), processed_row

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


sm = SMOTE(ratio='minority',k_neighbors = 10,random_state=42)

clf = svm.SVC(class_weight = 'balanced')
data, Y = produce_data_from_filename(filename)

x_train, x_test, y_train, y_test = train_test_split(data, Y, test_size = 0.1, random_state = 123)

x_train, y_train = sm.fit_sample(x_train, y_train)

clf.fit(x_train, y_train)

y_preds = clf.predict(x_test)

print(accuracy_score(y_test, y_preds))
print(f1_score(y_test, y_preds, pos_label='0'))

print(len([elem for elem in y_preds if elem == 0]))


