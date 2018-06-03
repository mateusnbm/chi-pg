#
# demo.py
#


import os
import random

import algorithms.knn


'''
Parameters.
'''

folds = 5

data_filename = 'sample-data/poker-data.txt' #example-data.txt'
header_filename = 'sample-data/poker-header.txt' #example-header.txt'

configurations = [
    (2, 3, 'am'),
    (2, 3, 'sam'),
]


'''
Create temporary folders to store data folds and prototypes.
'''

folds_path = 'tmp/folds/'
prototypes_path = 'tmp/prototypes/'

os.makedirs(folds_path, exist_ok=True)
os.makedirs(prototypes_path, exist_ok=True)


'''
Create testing and training files for each data fold.
'''

paths = []

basename_w_ext = os.path.basename(data_filename)
basename, basename_ext = os.path.splitext(basename_w_ext)

for i in range(folds):

    te = folds_path + basename + '_testing_fold_' + str(i+1) + '.txt'
    tr = folds_path + basename + '_training_fold_' + str(i+1) + '.txt'

    fte = open(te, 'a+')
    ftr = open(tr, 'a+')

    paths.append([[te, tr], [fte, ftr]])


'''
Divide input data among the testing files.
'''

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
Close training files, we no longer perform I/O with them here.
'''

for i in range(folds):

    paths[i][1][1].close()


'''
Generate prototypes for each data fold and configuration.
'''

for configuration in configurations:

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

        paths[i].append(output_filename)

        argument =  'python3 ../chi-pg/launcher.py '
        argument += str(fs) + ' ' + str(min) + ' ' + aggr + ' '
        argument += training_filename + ' ' + header_filename + ' ' + output_filename

        os.system(argument)


'''
'''

# ...


'''
Measure accuracies.
'''

# ...


'''
Close testing files, we no longer perform I/O with them here.
'''

for i in range(folds):

    paths[i][1][0].close()
