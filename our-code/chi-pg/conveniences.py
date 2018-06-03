#
# conveniences.py
#


import os

from variables import NominalVariable, FuzzyVariable


'''
'''

def write_prototypes(prototypes, filename):

    # Format prototypes list.

    output = '\n'.join(prototypes)

    # Write formatted prototypes to file.

    file = open(filename, 'w+')
    file.write(output)
    file.close()


'''
'''

def proccess_attribute_line(line_tokens, kfs):

    attr = line_tokens[1]

    if '{' in attr:

        # Nominal attribute.

        index_0 = attr.find('{')
        index_n = attr.find('}')

        attr_name = attr[:index_0]
        attr_values = attr[index_0+1:index_n].split(',')

        return NominalVariable(attr_name, attr_values)

    else:

        # Numerical attribute.

        index_0 = line_tokens[2].find('[')
        index_n = line_tokens[2].find(']')

        attr_name = attr
        attr_type = line_tokens[2][:index_0]

        attr_range = line_tokens[2][index_0+1:index_n].split(',')
        attr_lower = float(attr_range[0])
        attr_upper = float(attr_range[1])

        if attr_type == "real" or (attr_upper - attr_lower + 1) > kfs:

            return FuzzyVariable(attr_name, attr_type, attr_lower, attr_upper, kfs)

        # As stated by the authors: If the number of integer values is less
        # than the number of linguistic labels, then build a nominal variable.

        attr_values = []
        attr_nominal_base = str(int(attr_upper) - int(attr_lower) + 1)

        for i in range(len(attr_nominal_base)):

            attr_values.append(str(int(attr_lower)+i))

        return NominalVariable(attr_name, attr_values)


'''
'''

def read_header_file(filename, k_fuzzy_sets):

    file = open(filename, 'r')
    file_lines = file.readlines()

    variables = []
    output_attr_name = ''
    class_distribution = []

    # Process header file, mapping each attribute to a nominal variable or
    # fuzzy varible. When a fuzzy variable is initialized it automatically
    # generates the related fuzzy sets.

    for line in file_lines:

        line_tokens = line.replace(', ', ',').split()
        line_kind = line_tokens[0]

        if line_kind == '@attribute':

            variables.append(proccess_attribute_line(line_tokens, k_fuzzy_sets))

        if line_kind == '@outputs':

            output_attr_name = line_tokens[1]

        if line_kind == '@numInstancesByClass':

            class_distribution = line_tokens[1].split(',')
            class_distribution = [int(x) for x in class_distribution]

    # Remove the class attribute from the variables list and extracted the
    # allowed class values.

    filtered = filter(lambda x: x.name == output_attr_name, variables)
    class_variable = next(filtered)
    class_values = class_variable.values
    variables.remove(class_variable)

    # Close the file and return the variables, allowed class names and the
    # number of instances attributed to each class.

    file.close()

    return variables, class_values, class_distribution
