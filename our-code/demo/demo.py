#
# demo.py
#


import os
import time
import random

import algorithms.knn


'''
Parameters.
'''

folds = 5

data_filename = 'sample-data/poker-data.txt'
header_filename = 'sample-data/poker-header.txt'

data_class_index = 10
data_nominal_indexes = []
data_numerical_indexes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

configurations = [
	(2,  3, 'am'),
	(2,  5, 'am'),
	(2, 10, 'am'),
	(3,  3, 'am'),
	(3,  5, 'am'),
	(3, 10, 'am'),
	(4,  3, 'am'),
	(4,  5, 'am'),
	(5,  3, 'am'),
	(5,  5, 'am'),
	(7,  3, 'am'),
	(9,  3, 'am'),
	(2,  3, 'sam'),
	(2,  5, 'sam'),
	(2, 10, 'sam'),
	(3,  3, 'sam'),
	(3,  5, 'sam'),
	(3, 10, 'sam'),
	(4,  3, 'sam'),
	(4,  5, 'sam'),
	(5,  3, 'sam'),
	(5,  5, 'sam'),
	(7,  3, 'sam'),
	(9,  3, 'sam')
]


'''
Create temporary folders to store data folds, prototypes, times and reduction rates.
'''

print('')
print('Creating temporary data folders...')

folds_path = 'tmp/folds/'
times_path = 'tmp/times/'
rates_path = 'tmp/rates/'
prototypes_path = 'tmp/prototypes/'

os.system('rm -rf tmp')
os.makedirs(folds_path, exist_ok=True)
os.makedirs(times_path, exist_ok=True)
os.makedirs(rates_path, exist_ok=True)
os.makedirs(prototypes_path, exist_ok=True)


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

		training_filename = paths[i][0][1]

		output_filename =  prototypes_path
		output_filename += basename + '-'
		output_filename += str(fs) + 'FS-'
		output_filename += 'min' + str(min) + '-'
		output_filename += aggr + '_'
		output_filename += 'fold_' + str(i+1)
		output_filename += '.txt'

		paths[i][2].append(output_filename)

		argument =  'python3 ../chi-pg/launcher.py '
		argument += str(fs) + ' ' + str(min) + ' ' + aggr + ' '
		argument += training_filename + ' ' + header_filename + ' ' + output_filename

		start_time = time.time()

		os.system(argument)

		average_time += time.time() - start_time

	t = (average_time/folds)
	t = '{:.0f}:{:.0f}:{:.0f}'.format(t // 3600, (t % 3600 // 60), t % 60)

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

		training_file = open(paths[i][0][1], 'r')
		prototypes_fold_file = open(paths[i][2][k], 'r')

		training_file.seek(0, 0)
		for w, l in enumerate(training_file): pass
		training_file_length = w + 1

		prototypes_fold_file.seek(0, 0)
		for w, l in enumerate(prototypes_fold_file): pass
		prototypes_fold_file_length = w + 1

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

exit(0)

'''
Measure accuracies.
'''

print('Measuring accuracies...')
print('')

for k in range(len(configurations)):

	average = 0

	fs = configurations[k][0]
	min = configurations[k][1]
	aggr = configurations[k][2]

	for i in range(folds):

		testing_set = []
		training_set = []

		testing_data_file = paths[i][1][0]
		prototypes_fold_file = open(paths[i][2][k], 'r')

		testing_data_file.seek(0, 0)

		for line in testing_data_file:

			attributes = line[:-1].split(',')
			nominals_set = [attributes[w] for w in data_nominal_indexes]
			numericals_set = [float(attributes[w]) for w in data_numerical_indexes]

			testing_set.append([nominals_set, numericals_set, attributes[data_class_index]])

		for line in prototypes_fold_file:

			attributes = line[:-1].split(',')
			nominals_set = [attributes[w] for w in data_nominal_indexes]
			numericals_set = [float(attributes[w]) for w in data_numerical_indexes]

			training_set.append([nominals_set, numericals_set, attributes[data_class_index]])

		if len(data_nominal_indexes) > 0:

			print('Databases with nominal attributes are not supported yet.')

		else:

			average += algorithms.knn.knn_accuracy(1, training_set, testing_set)

	output  = 'Configuration '
	output += str(fs) + 'FS '
	output += 'min' + str(min) + ' '
	output += aggr + ': '
	output += '{:.2f}'.format(average/folds)
	output += '%'

	print(output)


print('')
print('Done.')
print('')
