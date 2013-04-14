import scipy.io.mmio
import datetime
import math
import misc_functions
from misc_functions import *
import sys

import numpy

def estimateLocal():
    """
        Function estimates accuracy of prediction in each case of 
        cross-validation - it gets results of prediction from 
        "prediction.mtx", test matrix from "test.mtx", and get info
        about clusters from "test_clusters" file.
        
        Function uses normalized DCGp metrics - it counts error for
        each cluster and get average error between clusters per user
        and then average for all users in current cross-validation case.
    """
    
    # file stuff
    prediction_matrix = scipy.io.mmio.mmread("prediction.mtx").tocsr()
    test_matrix = scipy.io.mmio.mmread("test.mtx").tocsr()
    clusters_file = open("test_clusters", 'r')
    
    # get 'window' coords
    coords = getWindowCoords()
    
    # skip header
    clusters_file.readline()
    clusters_file.readline()
    
    clusters_list = []
    cur_cluster = ["user" + "\t" + str(coords[0] + 1)]

    for line in clusters_file:
        #print line
        #print "Press any key to continue:"
        #sys.stdin.read(1)
        # if new user
        if line.find("user") != -1:
            clusters_list.append(cur_cluster)
            cur_cluster = [line]
        else:
            cur_cluster.append(line)
    """    
# == DEBUG PRINT =====================================================
    for user_cluster in clusters_list:
        for line in user_cluster:
            print line
        print "Press any key to continue:"
        sys.stdin.read(1)
# == \DEBUG PRINT =====================================================
    """
    local_average_nDCGp = 0.0
    user_ctr = 0
    for user_cluster in clusters_list:
        #print "user = ", user_ctr
        user_ctr += 1
        #print "user_cluster = ", user_cluster
        #print "user_cluster[0] = ", user_cluster[0]
        user = int((user_cluster[0]).split("\t")[1]) - 1
        user_prediction = prediction_matrix[user].toarray()[0]
        user_visits = test_matrix[user].toarray()[0]
        
        user_average_nDCGp = float(0.0)
        for byte in user_cluster[1 : ] :
            #byte_double_array = numpy.zeros((2, byte.split("\t")[1] - byte.split("\t")[0] + 1), dtype = float)
            #byte_double_array[0 : ] = user_visits[byte.split("\t")[0] : byte.split("\t")[1] + 1]
            #byte_double_array[1 : ] = user_prediction[byte.split("\t")[0] : byte.split("\t")[1] + 1]
            
            #byte_visits = user_visits[byte.split("\t")[0] : byte.split("\t")[1] + 1]
            byte_visits = user_visits[getMeta(byte, 0) : getMeta(byte, 1) + 1]
            #byte_predictions = user_prediction[byte.split("\t")[0] : byte.split("\t")[1] + 1]
            byte_predictions = user_prediction[getMeta(byte, 0) : getMeta(byte, 1) + 1]
            
            # get indices of columns by decreasing of prediction value
            indices = numpy.lexsort(keys = (byte_predictions, byte_predictions))
            ideal_indices = numpy.lexsort(keys = (byte_visits, byte_visits))
            
            # sort vector of visits and predictions with help of indices
            sorted_predictions = byte_predictions.take(indices, axis = -1)
            sorted_visits = byte_visits.take(indices, axis = -1)
            
            if len(sorted_predictions) != len(sorted_visits):
                raise Exception("visits and prediction clusters have differet size")
            
            
            #print "sorted_visits[] = ", sorted_visits
            """ TO BE NORMALIZED """
            nDCGp = float(0.0)
            p = len(sorted_predictions)
            for i in range(1, p + 1):
                nDCGp += float(sorted_visits[i - 1]) / float(math.log(i + 1, 2))
            """ / TO BE NORMALIZED """
            
            #print "nDCGp = ", nDCGp
            #step()
            if (nDCGp < 0.0):
                raise Exception("Incorrect nDCGp")
            #if (nDCGp < 0.0) or (nDCGp > 1.0):
                #print "nDCGp = ", nDCGp
                #raise Exception("Incorrect nDCGp")
            
            if (nDCGp > 1.0):
                nDCGp = 1.0
            user_average_nDCGp += nDCGp
        
        if (len(user_cluster) != 1):                       # WHY -1??
            user_average_nDCGp /= (len(user_cluster) - 1)   # WHY -1??
        local_average_nDCGp += user_average_nDCGp
        
    
    local_average_nDCGp /= (len(clusters_list))
    
    results_file = open("results", 'w')
    results_file.write(str(local_average_nDCGp))
    results_file.close()
    
    return local_average_nDCGp
