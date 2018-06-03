#
# knn.py
#
# mnbm@cin.ufpe.br
# Mateus N. de B. Magalhaes
#
# Implementation of the kNN algorithm along with HDVM.
#


import sys
import math
import random
import operator


'''
Returns the most frequent class among the given nearest neighbors.
'''

def standard_voting(neighbors=[]):

	votes = {}

	# Cast a vote for each class appearance.

	for instance in neighbors:

		c = instance[0][-1]

		votes[c] = (votes[c]+1) if (c in votes) else 1

	# Sort votes and return the most voted class.

	return sorted(votes.items(), key=operator.itemgetter(1), reverse=True)[0][0]


'''
Return the class with higher weight among the given neighbors.
'''

def weighted_voting(neighbors=[]):

	# Sum weights for each class.

	votes = {}

	for neighbor in neighbors:
		c = neighbor[0][-1]
		d = (1.0 / (neighbor[1]+0.01))
		votes[c] = (votes[c]+d) if (c in votes) else d

	# Sort votes descending accordingly to the sum of weights.
	sortedVotes = sorted(votes.iteritems(), key=operator.itemgetter(1), reverse=True)

	# Return the class with higher weight.
	return sortedVotes[0][0]


'''
'''

def vdm_matrix():

	return 0


'''
Calculates the euclidean distance between two data set instances.
'''

def euclidean_distance(instance_a=[], instance_b=[]):

	distance = 0

	for i in range(len(instance_a[1])):

		distance += pow((instance_a[1][i] - instance_b[1][i]), 2)

	return math.sqrt(distance)


'''
Calculates the euclidean distance adjusted for HDVM between two data set instances.
'''

def euclidean_distance_hvdm(instance_a=[], instance_b=[], data=[]):

	distance = 0

	for i in range(len(instance_a[1])):

		attr_a = instance_a[1][i]
		attr_b = instance_b[1][i]

		attr_values = [k[1][i] for k in data]

		a = attr_a-attr_b
		b = max(attr_values)
		c = min(attr_values)
		d = math.fabs(a)/(b-c)

		distance += pow(d, 2)

	return distance


'''
Calculates the value difference metric adjusted for HVDM between two data set instances.
'''

def vdm_hvdm(a, b, vdmSet):

	distance = 0
	classes = []

	for i in range(len(a[0])):

		for c in classes:

			nia = vdmSet[a[0][i]][i][0]
			nib = vdmSet[b[0][i]][i][0]

			niac = vdmSet[a[0][i]][i][1][c]
			nibc = vdmSet[b[0][i]][i][1][c]

			if nia == 0: nia = 0.001
			if nib == 0: nib = 0.001

			distance += pow(((float(niac)/nia)-(float(nibc)/nib)), 2)

	return distance


'''
Algorithm implementation (kNN + Euclidean).
'''

def knn(k, instance, neighbors):

	# Compute the distance between the base instance and every given neighbor
	# using the Euclidean Distance.

	distances = [[n, euclidean_distance(n, instance)] for n in neighbors]

	# Sort the neighbors accordingly to the calculated distances and return
	# the k nearest ones with their respective distances.

	return sorted(distances, key=lambda x: x[1])[:k]


'''
Evaluate kNN acurracy for a given test set (kNN + Euclidean).
'''

def knn_accuracy(k, training_set, test_set):

	hits = 0

	for instance in test_set:

		nearest_neighbors = knn(k, instance, training_set)
		predicted_class = standard_voting(nearest_neighbors)

		hits += 1 if (predicted_class == instance[-1]) else 0

	return float(hits)/len(test_set)


'''
Algorithm implementation (kNN + HVDM).
'''

def knn_hvdm(k, instance, neighbors, vdms):

	distances = []

	# Compute the distance between the base instance and every given neighbor
	# using the Heterogeneous Value Difference Metric (HVDM).

	for n in neighbors:

		nominal_sum = vdm_hvdm(instance, neighbors[i], vdms)
		numeric_sum = euclidean_distance_hvdm(instance, neighbors[i], neighbors)

		distances.append([n, math.sqrt(nominal_sum+numeric_sum)])

	# Sort the neighbors accordingly to the calculated distances and return
	# the k nearest ones with their respective distances.

	return sorted(distances, key=lambda x: x[1])[:k]
