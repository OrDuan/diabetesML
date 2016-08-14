import datetime

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_validation import KFold
from sklearn.neighbors import KNeighborsRegressor

from parser import parse_all


class DataHandler(object):
    """
    Handle the diabetes data set
    """
    def __init__(self):
        self.times = []
        self.labels = None
        self.features = None
        self.data_list = parse_all()
        self.user = self.data_list[0]['data']
        self.activities = []
        self.dates = []
        self.glucose = []
        self.k_fold = []
        self.classifier = KNeighborsRegressor()

    def parse_data(self):
        """
        Parse the data_list into our features
        """
        train_data = []
        test_data = []

        for user in self.data_list:
            for data in user['data']:
                # I wan't to compress all the dataset in a 24 hours timeframe
                time = data['date'].replace(year=2000, month=1, day=1)

                # Save the features
                self.dates.append(time)
                self.activities.append(data['activity'])
                self.glucose.append(data['glucose'])
                train_data.append([int(time.strftime("%H")), int(time.strftime("%M")), data['activity']])
                test_data.append([float(data['glucose'])])

        self.features = np.array(train_data)
        self.labels = np.array(test_data)

    def load_k_fold(self):
        """
        Load the test cases into K folds
        """
        self.k_fold = KFold(len(self.data_list), n_folds=len(self.data_list)*0.2)

    def fit(self):
        """
        Train the classifier with the train data
        """
        self.classifier.fit(self.features, self.labels)

    def print_score(self):
        """
        calculates the score on the given kfold test cases
        """
        for train, test in self.k_fold:
            print(self.classifier.score(self.features[test], self.labels[test]))

    def predict(self, date, activity):
        """
        Predict what will be the glucose rate on a given activity and data
        """
        return self.classifier.predict([int(date.strftime('%H')), int(date.strftime('%M')), activity])

    def plot(self):
        """
        Matplotlib it!
        """
        plt.plot(self.dates, self.glucose, 'go')
        plt.plot(self.dates, self.activities, 'ro')
        plt.show()

if __name__ == '__main__':
    dh = DataHandler()
    dh.parse_data()
    dh.load_k_fold()
    dh.fit()
    print(dh.predict(datetime.datetime.now(), 60))
    dh.print_score()
    dh.plot()

