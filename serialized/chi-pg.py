#!-*- coding: utf8 -*-

# CHI-PG - Serialized Implementation

import csv
import numpy as np

min_values = []
max_values = []

# Config parameters
N_FUZZY_SETS = 4
MIN_EXAMPLES = 3
AGGREGATION_AM = False

CLASS_LABEL_ON_FIRST_COLUMN = False

# Reads minimum and maximum values of each attribute
def read_header():
	global min_values, max_values

	with open('header.csv', newline='') as csvfile:
		reader = csv.reader(csvfile)
		rows = []
		for row in reader:
			rows.append(np.array(list(map(float, row))))

		min_values = rows[0]
		max_values = rows[1]


# Gets the fuzzy set for a given value of a given attribute
def get_fuzzy_set(index, value):
	D = (float(max_values[index] - min_values[index])) / (2 * N_FUZZY_SETS - 2)
	Q = int((value - min_values[index]) / D)

	return int((Q + 1) / 2)


def main():
	read_header()

	# Computes a dictionary that combines the instances in each fuzzy rule: keeps the count and the accumulated sum
	cell_dict = dict()

	with open('data.csv', newline='') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			x, y = [], []
			if CLASS_LABEL_ON_FIRST_COLUMN:
				x = np.array(list(map(float, row[1:])))
				y = row[0]
			else:
				x = np.array(list(map(float, row[:-1])))
				y = row[-1]


			cell = tuple(map(lambda j : get_fuzzy_set(j, x[j]), range(len(x))))
			
			class_dict = cell_dict.get(cell, dict())
			pair = class_dict.get(y, [0, np.zeros(len(x))])
			pair[0] += 1
			pair[1] += x

			class_dict[y] = pair
			cell_dict[cell] = class_dict

	# Computes the aggregation using the appropriated method (AM or SAM)
	with open('output.csv', 'w', newline='') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',',
								quotechar='|', quoting=csv.QUOTE_MINIMAL)

		for class_dict in cell_dict.values():
			if AGGREGATION_AM:
				for c, pair in class_dict.items():
					if pair[0] >= MIN_EXAMPLES:
						values = pair[1] / float(pair[0])
						spamwriter.writerow(values.tolist() + [c])

			else:
				max_class = ""
				max_pair = [-1, np.zeros(1)]
				for c, pair in class_dict.items():
					if max_pair[0] < pair[0]:
						max_pair = pair
						max_class = c
				
				if max_pair[0] >= MIN_EXAMPLES:
						values = max_pair[1] / float(max_pair[0])
						spamwriter.writerow(values.tolist() + [max_class])



if __name__ == "__main__":
	main()