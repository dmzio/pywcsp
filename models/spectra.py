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
                try:
                    x = (int(X[i]) + int(X[i-1]) + int(X[i-2]) + int(X[i+1]) + int(X[i+2]) + int(X[i+3]) + int(X[i-3]))/7.0
                    sp_writer.writerow([i*(-0.533) + 842, X[i]])
                except IndexError:
                    continue


