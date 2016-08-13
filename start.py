import matplotlib.pyplot as plt
from parser import parse_all
from sklearn.cross_validation import KFold


class DataHandler(object):
    """
    Handle the diabetes data set
    """
    def __init__(self):
        self.data_list = parse_all()
        self.user = self.data_list[0]['data']
        self.activities = []
        self.dates = []
        self.glucose = []
        self.k_fold = []

    def parse_data(self):
        """
        Parse the data_list into our features
        """
        for user in self.data_list:
            for data in user['data']:
                # I wan't to compress all the dataset in a 24 hours timeframe
                time = data['date'].replace(year=2000, month=1, day=1)

                # Save the features
                self.dates.append(time)
                self.activities.append(data['activity'])
                self.glucose.append(data['glucose'])

    def load_k_fold(self, n_folds):
        """
        Load the test cases into K folds
        """
        self.k_fold = KFold(len(self.data_list), n_folds=n_folds)

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
    dh.load_k_fold(5)
    dh.plot()
