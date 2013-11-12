import csv
import os
from datetime import datetime

class SpectralData(object):

    def __init__(self):
        self.data = []
        self.base_filename = os.path.dirname(__file__)

    def add_data(self, X, Y, **kwargs):
        # self.data.append({
        #     'X': X,
        #     'Y': Y,
        # })
        #TODO remake it all
        dt = datetime.now()
        filename = os.path.join(self.base_filename, 'spdata_{0}'.format(dt.strftime('%Y%m%d-%H%M%S')))
        with open(filename, 'wb') as csvfile:
            sp_writer = csv.writer(csvfile)
            for i in range(len(X)):
                sp_writer.writerow([i, X[i]])
