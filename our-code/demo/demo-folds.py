#
# demo-folds.py
#


import os
import sys
import time
import math
import random


'''
Parameters.
'''

folds = 5

folds_path = 'tmp/folds/'
data_filename = 'sample-data/poker-data.txt'


'''
Create temporary folder to store the data folds.
'''

print('')
print('Creating temporary data folders...')

os.makedirs(folds_path, exist_ok=True)


'''
Create testing and training files for each data fold.
'''

print('Creating files for training and testings data folds...')

paths = []

basename_w_ext = os.path.basename(data_filename)
basename, basename_ext = os.path.splitext(basename_w_ext)

for i in range(folds):

	te = folds_path + basename + '_testing_fold_' + str(i+1) + '.txt'
	tr = folds_path + basename + '_training_fold_' + str(i+1) + '.txt'

	fte = open(te, 'a+')
	ftr = open(tr, 'a+')

	paths.append([[te, tr], [fte, ftr], []])


'''
Divide input data among the testing files.
'''

print('Populating testing files...')

lines_buffer = []

with open(data_filename) as infile:

	for line in infile:

		lines_buffer.append(line)

		if len(lines_buffer) < folds:

			continue

		for i in range(folds):

			file = paths[i][1][0]
			instance = random.choice(lines_buffer)

			file.write(instance)
			lines_buffer.remove(instance)

	for i in range(len(lines_buffer)):

		file = paths[i][1][0]
		instance = lines_buffer[i]

		file.write(instance)


'''
Create training files for each data fold.
'''

print('Populating training files...')

for i in range(folds):

	training_file = paths[i][1][1]
	indexes = [k for k in range(folds)]

	indexes.remove(i)

	for index in indexes:

		testing_file = paths[index][1][0]
		testing_file.seek(0, 0)

		for line in testing_file:

			training_file.write(line)

'''
Close training files, we no longer perform I/O with them here. Closing these
files is very important in order to avoid file handling issues, because CHI-PG
will read from them while generating prototypes.
'''

for i in range(folds):

	paths[i][1][1].close()


'''
Termination.
'''

print('')
print('Done.')
print('')
