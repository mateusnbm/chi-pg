#
# reducer.py
#


from variables import NominalVariable, FuzzyVariable


'''
'''

def reduce(combined_data, variables, classes, min, aggregation):

    prototypes = []

    for rule in combined_data.keys():

        instances = combined_data[rule]

        for class_name in classes:

            # Count the number of instances belonging to the current class.

            filtered = filter(lambda x: x[-1] == class_name, instances)
            count = len(list(filtered))

            # Check if the class has the minimum number of required instances.

            if count < min: continue

            # Generate prototype.

            prototype = ''

            for variable in variables:

                if type(variable) == NominalVariable:

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

                    prototype += variable.values[mode_index]
                    prototype += ','

                else:

                    # ----------------------------------------------------
                    dumb_sum = 0
                    dumb_var_index = variables.index(variable)
                    for dumb_instance in instances:
                        #print(dumb_instance[dumb_var_index])
                        dumb_sum += float(dumb_instance[dumb_var_index])
                    # ----------------------------------------------------

                    #print('')

                    if variable.type == 'real':

                        prototype += str(dumb_sum/count)
                        prototype += ','

                    else:

                        prototype += str(round(dumb_sum/count))
                        prototype += ','

            prototype += class_name

            prototypes.append(prototype)

            print('')
            print(prototype)
            print('')

    return prototypes
