import scipy.sparse
import numpy
import scipy.io.mmio
import misc_functions
#from scipy.io.mmio import *
from numpy import *

import subprocess


def computePredictionMatrixFromEigenVectors(sing_vector_numb, base_file_name, prediction_file_name, window_coord):

    #print "window_coords = ", window_coord

    U_vectors = []
    V_vectors = []
    
    for i in range(sing_vector_numb):
        U_vectors.append(scipy.io.mmio.mmread(base_file_name + ".U." + str(i)))
        V_vectors.append(scipy.io.mmio.mmread(base_file_name + ".V." + str(i)))

    sigma = scipy.io.mmio.mmread(base_file_name + ".singular_values")
    #sigma = sigma[1:sing_numb]
    
    # take first <sing_vector_numb> vectors
    sigma = sigma[1 : sing_vector_numb + 1]
    
    # turn vector into diag matrix
    sigma = numpy.diagflat(sigma)
    
    #print " sigma = ", sigma

    U = numpy.column_stack((U_vectors[0], U_vectors[1]))
    V = numpy.column_stack((V_vectors[0], V_vectors[1]))
    
    #print "U = ", U
    #print "V = ", V
    
    for i in range(2, sing_vector_numb):
        exec("U = numpy.column_stack((U, U_vectors[" + str(i) +"]))")
        exec("V = numpy.column_stack((V, V_vectors[" + str(i) +"]))")
    #print "matrices pre-computing done! \n"
    
    #print "U.shape = ", U.shape
    #print "V.shape = ", V.shape
    
    U_test = U[window_coord[1] : window_coord[3] + 1, : ]
    V_test = V[window_coord[0] : window_coord[2] + 1, : ]
    
    #print "U_test = ", U_test
    #print "V_test = ", V_test
    
    #print "U_test.shape = ", U_test.shape
    #print "V_test.shape = ", V_test.shape
    
    left_result = dot(U_test, sigma)
    #print "left_result.shape =",  left_result.shape
    #print "left_result pre-computing done! \n"
    prediction_matrix = dot(left_result, V_test.transpose()).transpose()
    #print "prediction_matrix.shape = ", prediction_matrix.shape
    
    #print prediction_matrix
    prediction_matrix_csr = scipy.sparse.csr_matrix(prediction_matrix)
    
    #misc_functions.step()
    
    scipy.io.mmio.mmwrite(prediction_file_name, prediction_matrix_csr, field = 'real', precision = 5)

def prediction(prediction_file_name, clusters_list):
    
    #subprocess.call(["~/graphchi/toolkits/collaborative_filtering/svd", "--training=history.mtx", "--nsv=10", "--nv=12", "--max_iter=5", " --quiet=1", "--tol=1e-1"])
    #subprocess.call(["~/graphchi/toolkits/collaborative_filtering/svd", "--training=history.mtx --nsv=10 --nv=12 --max_iter=5 --quiet=1  --tol=1e-1"], )
    subprocess.call(["~/graphchi/toolkits/collaborative_filtering/svd --training=history.mtx --nsv=10 --nv=12 --max_iter=5  --quiet=1 --tol=1e-1  > /dev/null"], shell=True)
        
    window_coord = misc_functions.getWindowCoords()

    computePredictionMatrixFromEigenVectors(5, "history.mtx", prediction_file_name, window_coord)
    

