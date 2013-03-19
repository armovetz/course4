import numpy
from numpy import *
import scipy.io.mmio
from scipy.io.mmio import *
import mmio_misc

# tmp files locations
TRAINING_MATRIX_LOCATION = "~/graphchi/tmp_course_work_files/_training_matrix.mm"

def prediction(training_matrix, optional parameters = 0):
	"""Function executes Singular Value Decomposition for <training_matrix> by calling graphchi
	and returns recomputed matrix"""

	# write original matrix into matrix market format (MM)
	mmwrite(TRAINING_MATRIX_LOCATION, training_matrix, mmio_misc.getNowString(), 'integer')
	
	cmd_line = ".~/graphchi/toolkits/collaborative_filtering/svd --training=" \
		TRAINING_MATRIX_LOCATION + " --nsv=4 --nv=4 --max_iter=4 --quiet=1"
	
	print "finished"
