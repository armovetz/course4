import scipy.io.mmio
import datetime
import math
import misc_functions
from misc_functions import *
import sys

import numpy

def estimateNDCGp(prediction_file_name, results_file_name, clusters_list):
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
    prediction_matrix = scipy.io.mmio.mmread(prediction_file_name).tocsr()
    test_matrix = scipy.io.mmio.mmread("test.mtx").tocsr()
    
    # get 'window' coords
    coords = getWindowCoords()
    
    """    
# == DEBUG PRINT =====================================================
    for user_cluster in clusters_list:
        for line in user_cluster:
            print line
        print "Press any key to continue:"
        sys.stdin.read(1)
# == \DEBUG PRINT =====================================================
    """
    
    local_average_nDCGp = float(0.0)
    local_average_p = float(0.0)
    #user_ctr = 0
    for user_cluster in clusters_list:
        #misc_functions.step()
        #print "user = ", user_ctr
        #user_ctr += 1
        #print "user_cluster = ", user_cluster
        #print "user_cluster[0] = ", user_cluster[0]
        
        user = int(((user_cluster[0]).split("\t"))[1]) - coords[0]
        #print "user = ", user
        user_prediction = prediction_matrix[user].toarray()[0]
        user_visits = test_matrix[user].toarray()[0]
        
        #print "user_prediction = ", user_prediction
        #print "user_visits = ", user_visits
        
        user_average_nDCGp = float(0.0)
        user_average_p = float(0.0)
        for byte in user_cluster[1 : ] :
            #misc_functions.step()
            byte_visits = user_visits[getMeta(byte, 0) - coords[1] : getMeta(byte, 2) + 1 - coords[1]]
            byte_predictions = user_prediction[getMeta(byte, 0) - coords[1] : getMeta(byte, 2) + 1 - coords[1]]
            
            #print "byte_visits = ", byte_visits
            #print "byte_predictions = ", byte_predictions
            
            # get indices of columns by decreasing of prediction value
            indices = numpy.lexsort(keys = (-byte_predictions, -byte_predictions))
            ideal_indices = numpy.lexsort(keys = (byte_visits, byte_visits))
            
            #print "indices = ", indices
            #print "ideal_indices = ", ideal_indices
            
            # sort vector of visits and predictions with help of indices
            sorted_predictions = byte_predictions.take(indices, axis = 0)
            sorted_visits = byte_visits.take(indices, axis = 0)
            #sorted_predictions = numpy.sort(sorted_predictions)
            #sorted_visits = 
            
            #print "sorted_visits = ", sorted_visits
            #print "sorted_predictions = ", sorted_predictions
            
            if len(sorted_predictions) != len(sorted_visits):
                raise Exception("visits and prediction clusters have different size")
            
            #print "sorted_visits[] = ", sorted_visits
            """ TO BE NORMALIZED """
            nDCGp = float(0.0)
            p = len(sorted_predictions)
            for i in range(p):
                if sorted_visits[i] == 1:
                    nDCGp = float(math.log(2, i + 2))
                    break
            """
            for i in range(1, p + 1):
                #print "i"
                nDCGp += float(sorted_visits[i - 1]) / float(math.log(i + 1, 2))
            """
            """ / TO BE NORMALIZED """
            
            #if (nDCGp > 1.0):
                #nDCGp = 1.0
            #print "nDCGp = ", nDCGp
            #step()
            #if (nDCGp < 0.0):
                #raise Exception("Incorrect nDCGp")
            if (nDCGp < 0.0) or (nDCGp > 1.0):
                print "nDCGp = ", nDCGp
                raise Exception("Incorrect nDCGp")
            
            #print "nDCGp = ", nDCGp
            user_average_nDCGp += nDCGp
            user_average_p += p
        
        if (len(user_cluster) != 1):                       # WHY -1??
            user_average_nDCGp /= (len(user_cluster) - 1)  # WHY -1??
            user_average_p /= (len(user_cluster) - 1)
        local_average_nDCGp += user_average_nDCGp
        local_average_p += user_average_p
    
    local_average_nDCGp /= (len(clusters_list))
    local_average_p /= (len(clusters_list))
    local_average_position = math.pow(2, 1.0 / local_average_nDCGp)
    
    print "nDCGp for case = ", local_average_nDCGp
    print "average p = ", local_average_p
    print "average position", local_average_position
    
    results_file = open(results_file_name + ".nDCGp", 'w')
    results_file.write(str(local_average_nDCGp))
    results_file.close()
    
    return [local_average_nDCGp, local_average_p, local_average_position]

"""
def estimateRecallPrecision(prediction_file_name, results_file_name):
    # file stuff
    prediction_matrix = scipy.io.mmio.mmread(prediction_file_name).tocsr()
    test_matrix = scipy.io.mmio.mmread("test.mtx").tocsr()
    clusters_file = open("test_clusters", 'r')
    
    # get 'window' coords
    coords = getWindowCoords()
    
    # skip header and 
    clusters_file.readline()
    user0 = int(clusters_file.readline().split("\t")[1]) 
    
    clusters_list = []
    cur_cluster = ["user" + "\t" + str(user0)]

    # reading clusters info to local lists
    for line in clusters_file:
        #print line

        # if new user
        if line.find("user") != -1:
            clusters_list.append(cur_cluster)
            cur_cluster = [line]
        else:
            cur_cluster.append(line)
    # appending last cluster
    clusters_list.append(cur_cluster)
    
    total_recall = 0.0
    total_precision = 0.0
    
    results_file = open(results_file_name + ".RP", 'w')
    results_file.write(str(local_average_nDCGp))
    results_file.close()

def estimateRMSE(prediction_file_name, results_file_name):
    


    results_file = open(results_file_name + ".RMSE", 'w')
    results_file.write(str(local_average_nDCGp))
    results_file.close()
"""
