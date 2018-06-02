#
# fuzzy_rule.py
#


'''
Returns a new rule represented by a byte array containing the index of
antecedents and the class index (at last position of the array).
'''

def generate(values, variables, classes):

    rule = []

    for i in range(len(variables)):

        value = values[i]
        variable = variables[i]

        rule.append(variable.get_value_index(value))

    return rule
