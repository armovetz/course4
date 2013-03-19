import SVDonSide
import numpy
from numpy import *
import datetime
from datetime import *

import scipy
import scipy.io.mmio
from scipy.io.mmio import *

import cross-validation

# matrices location



cross-validation.launchCrossValidationSVD(




"""
matrix = zeros((10000,1000), dtype = int)

start = datetime.now()

for i in range(10000):
	print "i = ", i
	for j in range(1000):
		r = SVDonSide.computeSingleRating(i,j)
		if r > 0.3:
			matrix[i, j] = 1
		else:
			matrix[i,j] = 0

finish = datetime.now()

print "sum =",  sum(matrix)

delta = finish - start

print delta.seconds, "seconds"

original_matrix = (mmread("../data/well_made/history.mm").toarray())[0:10,0:1000]

print estimate.EstimateResult2(original_matrix, matrix)
