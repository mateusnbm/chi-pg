#
# demo.py
#


import os
import sys
import time
import math
import random

import numpy as np

from sklearn.neighbors import KNeighborsClassifier


'''
Parameters.
'''

folds = 5

tmp_path = 'tmp/'
folds_path = tmp_path + 'folds/'
prototypes_path = tmp_path + 'prototypes/'
accuracies_path = tmp_path + 'accuracies/'
data_filename = 'sample-data/poker-data.txt'

configurations = [
	(2,  3, 'am'),
	(2,  5, 'am'),
	(7,  3, 'sam'),
	(9,  3, 'sam'),
]


'''
Create a temporary folder and file to store accuracies.
'''

os.makedirs(accuracies_path, exist_ok=True)

accuracies_file = open(accuracies_path + 'accuracies.txt', 'a+')


'''
Compute testing files paths for each fold.
'''

paths = []

basename_w_ext = os.path.basename(data_filename)
basename, basename_ext = os.path.splitext(basename_w_ext)

for i in range(folds):

	path = folds_path + basename + '_testing_fold_' + str(i+1) + '.txt'

	paths.append([path, []])


'''
Compute prototypes path for each data fold and configuration.
'''

for configuration in configurations:

	fs = configuration[0]
	min = configuration[1]
	aggr = configuration[2]

	for i in range(folds):

		output_filename =  prototypes_path
		output_filename += basename + '-'
		output_filename += str(fs) + 'FS-'
		output_filename += 'min' + str(min) + '-'
		output_filename += aggr + '_'
		output_filename += 'fold_' + str(i+1)
		output_filename += '.txt'

		paths[i][1].append(output_filename)


'''
Measure accuracies.
'''

print('')
print('Measuring accuracies...')
print('')

for k in range(len(configurations)):

	average = 0

	fs = configurations[k][0]
	min = configurations[k][1]
	aggr = configurations[k][2]

	for i in range(folds):

		hits = 0
		testing_set = []
		testing_set_classes = []
		training_set = []
		training_set_classes = []

		testing_data_file = open(paths[i][0], 'r')
		prototypes_fold_file = open(paths[i][1][k], 'r')

		for line in testing_data_file:

			tokens = line[:-1].split(',')
			inputs = [float(tokens[w]) for w in range(len(tokens)-1)]

			testing_set.append(inputs)
			testing_set_classes.append(tokens[-1])

		for line in prototypes_fold_file:

			tokens = line[:-1].split(',')
			inputs = [float(tokens[w]) for w in range(len(tokens)-1)]

			training_set.append(inputs)
			training_set_classes.append(tokens[-1])

		classifier = KNeighborsClassifier(n_neighbors=1, n_jobs=-1)
		classifier.fit(training_set, training_set_classes)
		predictions = classifier.predict(testing_set)

		for w in range(len(predictions)):

			if predictions[w] == testing_set_classes[w]:

				hits += 1

		average += float(hits)/len(testing_set)

		testing_data_file.close()
		prototypes_fold_file.close()

	output  = 'Configuration '
	output += str(fs) + 'FS '
	output += 'min' + str(min) + ' '
	output += aggr.upper() + ': '
	output += '{:.2f}'.format((average/folds)*100)
	output += '%'

	print(output)

	accuracies_file.write(output + '\n')


'''
Termination.
'''

accuracies_file.close()

print('')
print('Done.')
print('')
