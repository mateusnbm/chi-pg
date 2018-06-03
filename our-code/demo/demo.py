#
# demo.py
#


import os


'''
Convenience to wrap prototype generation and accuracy measurement.
'''

def run(fs, min, aggregation, data_filename, header_filename, output_filename):

    # Generate prototypes.

    argument = 'python3 ../chi-pg/launcher.py '
    argument += str(fs) + ' ' + str(min) + ' ' + aggregation + ' '
    argument += data_filename + ' ' + header_filename + ' ' + output_filename

    os.system(argument)

    # ...

'''
Run each desired configuration.
'''

data_filename = 'sample-data/example-data.txt'
header_filename = 'sample-data/example-header.txt'
output_basename = 'prototypes/example-'

run(2,  3, 'am', data_filename, header_filename, output_basename+'2FS-min3-AM.txt')
run(2,  5, 'am', data_filename, header_filename, output_basename+'2FS-min5-AM.txt')
run(2, 10, 'am', data_filename, header_filename, output_basename+'2FS-min10-AM.txt')
run(3,  3, 'am', data_filename, header_filename, output_basename+'3FS-min3-AM.txt')
run(3,  5, 'am', data_filename, header_filename, output_basename+'3FS-min5-AM.txt')
run(3, 10, 'am', data_filename, header_filename, output_basename+'3FS-min10-AM.txt')
run(4,  3, 'am', data_filename, header_filename, output_basename+'4FS-min3-AM.txt')
run(4,  5, 'am', data_filename, header_filename, output_basename+'4FS-min5-AM.txt')
run(5,  3, 'am', data_filename, header_filename, output_basename+'5FS-min3-AM.txt')
run(5,  5, 'am', data_filename, header_filename, output_basename+'5FS-min5-AM.txt')
run(7,  3, 'am', data_filename, header_filename, output_basename+'7FS-min3-AM.txt')
run(9,  3, 'am', data_filename, header_filename, output_basename+'9FS-min3-AM.txt')

run(2,  3, 'sam', data_filename, header_filename, output_basename+'2FS-min3-SAM.txt')
run(2,  5, 'sam', data_filename, header_filename, output_basename+'2FS-min5-SAM.txt')
run(2, 10, 'sam', data_filename, header_filename, output_basename+'2FS-min10-SAM.txt')
run(3,  3, 'sam', data_filename, header_filename, output_basename+'3FS-min3-SAM.txt')
run(3,  5, 'sam', data_filename, header_filename, output_basename+'3FS-min5-SAM.txt')
run(3, 10, 'sam', data_filename, header_filename, output_basename+'3FS-min10-SAM.txt')
run(4,  3, 'sam', data_filename, header_filename, output_basename+'4FS-min3-SAM.txt')
run(4,  5, 'sam', data_filename, header_filename, output_basename+'4FS-min5-SAM.txt')
run(5,  3, 'sam', data_filename, header_filename, output_basename+'5FS-min3-SAM.txt')
run(5,  5, 'sam', data_filename, header_filename, output_basename+'5FS-min5-SAM.txt')
run(7,  3, 'sam', data_filename, header_filename, output_basename+'7FS-min3-SAM.txt')
run(9,  3, 'sam', data_filename, header_filename, output_basename+'9FS-min3-SAM.txt')
