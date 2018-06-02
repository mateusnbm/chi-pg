#
# variables.py
#

from fuzzy_set import FuzzySet


'''
Represents a nominal variable of the problem.
'''

class NominalVariable(object):

    '''
    '''

    def __init__(self, name, values):

        self.name = name
        self.values = values

    '''
    Returns the variable label index corresponding to the input value.
    '''

    def get_value_index(self, value):

        return self.values.index(value)


'''
Represents a fuzzy variable of the problem, containing 'l' linguistic
labels (fuzzy sets), being 'l' the number of linguistic labels specified
by the user.
'''

class FuzzyVariable(object):

    '''
    '''

    def __init__(self, name, type, lower, upper, kfs):

        self.name = name
        self.type = type
        self.lower = lower
        self.upper = upper
        self.k_fuzzy_sets = kfs

        self.build_fuzzy_sets()

    '''
    Returns the variable label index corresponding to the input value.
    '''

    def get_value_index(self, value):

        return self.get_max_membership_fuzzy_set(float(value))

    '''
    Builds the fuzzy sets (modeled by triangular membership functions) that
    compose this fuzzy variable from the input limits.
    '''

    def build_fuzzy_sets(self):

        fuzzy_sets = []
        merge_points = []

        for i in range(self.k_fuzzy_sets):

            # Compute the half of the triangle's base.

            half_base = (self.upper-self.lower)/(self.k_fuzzy_sets-1)

            # We add the half of the triangle's base n times to the lower
            # limit, depending on the linguistic label and the point we want
            # to obtain (left, mid, right).

            left_point = self.lower + half_base * (i - 1)
            mid_point = self.lower + half_base * i
            right_point = self.lower + half_base * (i + 1)

            # Adjustments to the first and last sets.

            if i == 0: left_point = mid_point

            if i == (self.k_fuzzy_sets - 1): right_point = mid_point

            # Create the fuzzy set and store the merge point.

            fuzzy_sets.append(FuzzySet(left_point, mid_point, right_point, i))

            if i > 0:

                previous_set = fuzzy_sets[i-1]
                point = mid_point - ((mid_point-previous_set.mid_point)/2)

                merge_points.append(point)

        # Store the newly computed fuzzy set.

        self.fuzzy_sets = fuzzy_sets
        self.merge_points = merge_points

    '''
    Returns the index of the fuzzy set with the highest membership degree
    for the given input value.
    '''

    def get_max_membership_fuzzy_set(self, value):

        # Since this function is used only in the learning stage, we do not
        # compute membership degrees. Instead, we check the location of the
        # input value with respect to the point where two fuzzy sets merge.

        for i in range(len(self.merge_points)):

            if value < self.merge_points[i]:

                return i

        return len(self.merge_points)
