#
# reducer.py
#


from variables import NominalVariable, FuzzyVariable


'''
'''

def compute_most_frequent_classes(instances):

    highest = 0
    classes = []
    counters = {}

    for instance in instances:

        if instance[-1] not in counters:

            counters[instance[-1]] = 1

        else:

            counters[instance[-1]] += 1

    for key in counters.keys():

        if counters[key] > highest:

            highest = counters[key]

    for key in counters.keys():

        if counters[key] == highest:

            classes.append(key)

    return classes


'''
'''

def nominal_attr_contribution(variables, variable, instances):

    mode_value = 0
    mode_index = 0

    # ----------------------------------------------------
    dumb_counts = {}
    dumb_var_index = variables.index(variable)
    for dumb_value in variable.values:
        dumb_counts[dumb_value] = 0
    for dumb_instance in instances:
        dumb_counts[dumb_instance[dumb_var_index]] += 1
    # ----------------------------------------------------

    for k in range(len(variable.values)):

        mode = dumb_counts[variable.values[k]]

        if mode > mode_value:

            mode_value = mode
            mode_index = k

    return variable.values[mode_index]


'''
'''

def numerical_attr_contribution(variables, variable, instances, count):

    # ----------------------------------------------------
    dumb_sum = 0
    dumb_var_index = variables.index(variable)
    for dumb_instance in instances:
        dumb_sum += float(dumb_instance[dumb_var_index])
    # ----------------------------------------------------

    if variable.type == 'real':

        return str(dumb_sum/count)

    return str(round(dumb_sum/count))


'''
'''

def generate_prototype(variables, instances, count, class_name):

    prototype = ''

    for variable in variables:

        if type(variable) == NominalVariable:

            attr = nominal_attr_contribution(variables, variable, instances)

            prototype += attr
            prototype += ','

        else:

            attr = numerical_attr_contribution(variables, variable, instances, count)

            prototype += attr
            prototype += ','

    prototype += class_name

    return prototype


'''
'''

def reduce(combined_data, variables, classes, min, aggregation):

    prototypes = []

    for rule in combined_data.keys():

        instances = combined_data[rule]

        if aggregation == 'sam':

            classes = compute_most_frequent_classes(instances)

        for class_name in classes:

            # Count the number of instances belonging to the current class.

            filtered = list(filter(lambda x: x[-1] == class_name, instances))
            count = len(filtered)

            # Check if the class has the minimum number of required instances.

            if count < min: continue

            # Generate a prototype and store it.

            prototype = generate_prototype(variables, filtered, count, class_name)

            prototypes.append(prototype)

    return prototypes
