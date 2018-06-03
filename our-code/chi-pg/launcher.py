#
# launcher.py
#


import sys

import mapper
import reducer
import conveniences


'''
Parameters.
'''

k_fuzzy_sets = int(sys.argv[1])
k_min = int(sys.argv[2])
k_aggregation = sys.argv[3]

data_filename = sys.argv[4]
header_filename = sys.argv[5]
output_filename = sys.argv[6]


'''
Initialization.
'''

variables, classes, distribution = conveniences.read_header_file(header_filename, k_fuzzy_sets)


'''
Map and combine dataset instances with common antecedents.
'''

combined_data = mapper.map(data_filename, variables, classes)


'''
Reduce (generate prototypes).
'''

prototypes = reducer.reduce(combined_data, variables, classes, k_min, k_aggregation)


'''
Write prototypes to file.
'''

conveniences.write_prototypes(prototypes, output_filename)
