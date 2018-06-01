#!-*- coding: utf8 -*-

# Preprocess for CHI-PG algorithm
# Computes the minimum and maximum values of each attribute

import csv
import copy

CLASS_LABEL_ON_FIRST_COLUMN = False

def main():	
	min_values = []
	max_values = []

	firstRow = True

	with open('data.csv', newline='') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			x = []
			if CLASS_LABEL_ON_FIRST_COLUMN:
				x = list(map(float, row[1:]))
			else:
				x = list(map(float, row[:-1]))

			if firstRow:
				min_values = copy.copy(x)
				max_values = copy.copy(x)
				firstRow = False
			else:	
				for i in range(len(x)):
					min_values[i] = min(min_values[i], x[i])
					max_values[i] = max(max_values[i], x[i])


	with open('header.csv', 'w', newline='') as csvfile:
	    spamwriter = csv.writer(csvfile, delimiter=',',
	                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
	    spamwriter.writerow(min_values)
	    spamwriter.writerow(max_values)



if __name__ == "__main__":
	main()
