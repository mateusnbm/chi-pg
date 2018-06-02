#
# fuzzy_set.py
#


'''
'''

class FuzzySet(object):

    '''
    '''

    def __init__(self, left_point, mid_point, right_point, label_index):

        self.left_point = left_point
        self.mid_point = mid_point
        self.right_point = right_point
        self.label_index = label_index

    '''
    '''

    def computer_membership_degree(self, value):

        lp = self.left_point
        mp = self.mid_point
        rp = self.right_point

        # Between the left and mid points.

        if lp < value and value < mp: return (value - lp) / (mp - lp)

        # Between the mid and right points.

        if mp < value and value < rp: return (rp - value) / (rp - mp)

        # The value is the mid point.

        if value == mp: return 1.0

        # The value is the left or right point.

        if value == lp or value == rp: return 0.0

        # The value is out of range (from the left).

        if value < lp: return -1.0 if lp == mp else 0.0

        # The value is out of the range of this variable.

        return -1.0 if mp == rp else 0.0
