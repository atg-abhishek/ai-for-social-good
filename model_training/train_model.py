from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import csv

filename = 'all_data_R.csv'

def get_relevant_features(row):
	return row[0], [int(row[3]),int(row[7]),int(row[8]),int(row[15]),int(row[17])]

def produce_data_from_filename(csvfile):
	data = []
	Y = []
	with open(filename, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		next(reader, None)
		for row in reader:
			y,x_row = get_relevant_features(row)
			Y.append(y)
			data.append(x_row)

	return data, Y



clf = svm.SVC()
data, Y = produce_data_from_filename(filename)

x_train, x_test, y_train, y_test = train_test_split(data, Y, test_size = 0.2, random_state = 123)

clf.fit(x_train, y_train)

y_preds = clf.predict(x_test)
print(accuracy_score(y_test, y_preds))
