#
# mapper.py
#


import fuzzy_rule


'''
'''

def map(filename, variables, classes):

    data = {}

    file = open(filename, 'r')
    file_lines = file.readlines()

    for line in file_lines:

        instance_values = line[:-1].replace(', ', ',').split(',')
        instance_rule = fuzzy_rule.generate(instance_values, variables, classes)
        instance_key = str(instance_rule)

        if instance_key not in data:

            data[instance_key] = []

        data[instance_key].append(instance_values)

    file.close()

    return data
