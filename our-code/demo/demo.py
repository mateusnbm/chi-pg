#
# demo.py
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

data_filename = 'sample-data/poker-data.txt'
header_filename = 'sample-data/poker-header.txt'

configurations = [
	(2,  3, 'am'),
	(2,  5, 'am'),
	(7,  3, 'sam'),
	(9,  3, 'sam'),
]


'''
Create temporary folders to store prototypes, times and reduction rates.
'''

print('')
print('Creating temporary data folders...')

folds_path = 'tmp/folds/'
times_path = 'tmp/times/'
rates_path = 'tmp/rates/'
prototypes_path = 'tmp/prototypes/'

os.makedirs(times_path, exist_ok=True)
os.makedirs(rates_path, exist_ok=True)
os.makedirs(prototypes_path, exist_ok=True)


'''
Compute training files path for each data fold.
'''

paths = []

basename_w_ext = os.path.basename(data_filename)
basename, basename_ext = os.path.splitext(basename_w_ext)

for i in range(folds):

	tr = folds_path + basename + '_training_fold_' + str(i+1) + '.txt'

	paths.append([tr, []])


'''
Generate prototypes for each data fold and configuration.
'''

print('Generating prototypes...')
print('')

times_filename = times_path + 'times.txt'
times_file = open(times_filename, 'a')

for configuration in configurations:

	average_time = 0

	fs = configuration[0]
	min = configuration[1]
	aggr = configuration[2]

	for i in range(folds):

		training_filename = paths[i][0]

		output_filename =  prototypes_path
		output_filename += basename + '-'
		output_filename += str(fs) + 'FS-'
		output_filename += 'min' + str(min) + '-'
		output_filename += aggr + '_'
		output_filename += 'fold_' + str(i+1)
		output_filename += '.txt'

		paths[i][1].append(output_filename)

		argument =  'python3 ../chi-pg/launcher.py '
		argument += str(fs) + ' ' + str(min) + ' ' + aggr + ' '
		argument += training_filename + ' ' + header_filename + ' ' + output_filename

		start_time = time.time()

		os.system(argument)

		average_time += time.time() - start_time

	t = (average_time/folds)
	t = '{:02.0f}:{:02.0f}:{:02.0f}'.format(t // 3600, (t % 3600 // 60), t % 60)

	output  = 'Configuration '
	output += str(fs) + 'FS '
	output += 'min' + str(min) + ' '
	output += aggr.upper() + ': '
	output += t + '\n'

	print(output)

	times_file.write(output)

times_file.close()

'''
Measure reduction rates.
'''

print('Computing reduction rates...')
print('')

rates_filename = rates_path + 'rates.txt'
rates_file = open(rates_filename, 'a')

for k in range(len(configurations)):

	average_rate = 0

	fs = configurations[k][0]
	min = configurations[k][1]
	aggr = configurations[k][2]

	for i in range(folds):

		training_file = open(paths[i][0], 'r')
		prototypes_fold_file = open(paths[i][1][k], 'r')

		training_file.seek(0, 0)
		for w, l in enumerate(training_file): pass
		training_file_length = w + 1

		prototypes_fold_file.seek(0, 0)
		for w, l in enumerate(prototypes_fold_file): pass
		prototypes_fold_file_length = w + 1

		print('prototypes file length: ' + str(prototypes_fold_file_length))
		print('training file length: ' + str(training_file_length))

		p = prototypes_fold_file_length / training_file_length
		average_rate += ((1 - p) * 100)

		training_file.close()
		prototypes_fold_file.close()

	output  = 'Configuration '
	output += str(fs) + 'FS '
	output += 'min' + str(min) + ' '
	output += aggr.upper() + ': '
	output += '{:.2f}'.format(average_rate/folds)
	output += '%\n'

	print(output)

	rates_file.write(output)

rates_file.close()


'''
Termination.
'''

print('')
print('Done.')
print('')
