from sklearn import svm
from sklearn.metrics import accuracy_score, f1_score, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.externals import joblib
import csv

rf = joblib.load('rfclassifier.pkl')

def predict_score(row):
	return rf.predict_proba(row)