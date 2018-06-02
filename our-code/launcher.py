#
# launcher.py
#


import mapper
import reducer
import conveniences

from variables import NominalVariable, FuzzyVariable


'''
Parameters.
'''

k_min = 3
k_fuzzy_sets = 2
k_aggregation = 'am'

data_filename = '../sample-data/example/example_data.txt'
header_filename = '../sample-data/example/example_header.txt'
output_filename = 'output/example_prototypes_2FS_min3.txt'


'''
Initialization.
'''

variables, classes, distribution = conveniences.read_header_file(header_filename, k_fuzzy_sets)


'''
Map and combine dataset instances with common antecedents.
'''

combined_data = mapper.map(data_filename, variables, classes)

#print('')
#for key in combined_data.keys(): print(len(combined_data[key]))
#print('')

print('')

for key in combined_data.keys():

    foo = key[1:-1]
    foo = foo.replace(', ', ' | ')

    print(foo)
    print('')

'''
for key in combined_data.keys():

    rule = ''

    for variable in variables:

        index = variables.index(variable)

        if type(variable) == NominalVariable:

            rule += ' ' + str(key[index])
            rule += ' |'

        else:

            rule += ' 1'
            rule += ' |'

    print(rule)
    print('')
'''

'''
Reduce (generate prototypes).
'''

prototypes = reducer.reduce(combined_data, variables, classes, k_min, k_aggregation)

print('')
print('Prototypes count: ' + str(len(prototypes)) + '.')


'''
Write prototypes to file.
'''

#file = open(output_filename, 'w+')
#file.write(prototypes)
#file.close()
