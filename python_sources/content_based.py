import datetime
import sys
import scipy.sparse
import scipy.io.mmio
import numpy
from numpy import *

import misc_functions
import ini
from ini import *

   
    
def prediction(prediction_file_name, clusters_list, trash):
    
    coords = misc_functions.getWindowCoords()
    
    test_users = range(coords[0], coords[2] + 1) 
    test_items = range(coords[1], coords[3] + 1)
    
    #print "len(test_users) = ", len(test_users)
    #print "len(test_items) = ", len(test_items)
    #print "test_items = ", test_items
    
    # this matrix to be written as result finally
    #misc_functions.step()
    prediction_matrix = zeros((len(test_users), len(test_items)), dtype = float)
    
    training_matrix = scipy.io.mmio.mmread("history.mtx").tocsr()
    
    #item_X_meta_matrix = scipy.io.mmio.mmread("../../../well_done/items-metas_global.mtx").toarray()
    item_X_item_matrix = scipy.io.mmio.mmread("../../../well_done/items-items.mtx").tocsr()
    
    #user_counter = 0
    #for user in test_users:
    for cur_cluster in clusters_list:
        user = int (cur_cluster[0].split("\t")[1])
        #print "user = ", user
        user_visits = training_matrix[user].toarray()[0]
        
        prediction_vector = numpy.zeros((len(test_items)), dtype = float)
        
        for cluster in cur_cluster[1 : ]:
            start_cluster_item = int(cluster.split("\t")[0])
            stop_cluster_item  = int(cluster.split("\t")[2])
            
            similarities_for_clusters = item_X_item_matrix[start_cluster_item : stop_cluster_item]
            #print "similarities_for_clusters = ", similarities_for_clusters
            
            prediction_vector += sum(sum(similarities_for_clusters * user_visits)) / K
            
            """
            cluster_items = range(start_cluster_item, stop_cluster_item + 1)
                
            for item in cluster_items:
                similarities = item_X_item_matrix[item].toarray()[0]
                numpy.dot
                #print "similarities = ", similarities
                #print "len(similarities) = ", len(similarities)
                #   indices = numpy.lexsort(keys = (-similarities, -similarities))
                #print "indices = ", indices
                #print "len(indices) = ", len(indices)
                #print "K = ", K
                
                #   indices = indices[0:K]
                #   sorted_similarities = similarities.take(indices, axis = 0)
                #print "indices = ", indices
                #print "sorted_similarities = ", sorted_similarities
                #print "len(sorted_similarities) = ", len(sorted_similarities)
                #sorted_similarities = sorted_similarities[0:K] 
                
                for K_ctr in range(K):
                    index = indices[K_ctr]
                
                
                for K_ctr in range(K):
                    index = indices[K_ctr]
                    #print "user_visits[index] = ", user_visits[index]
                    #print "user_visits[index] = ", user_visits[index]
                    #print "prediction_vector[item - coords[1]] = ", prediction_vector[item - coords[1]]
                    #print "sorted_similarities = ", sorted_similarities
                    #print "sorted_similarities[K_ctr] = ", sorted_similarities[K_ctr]
                    
                    prediction_vector[item - coords[1]] += (user_visits[index] * sorted_similarities[K_ctr]) / K
                """

        prediction_matrix[user - coords[0]] = prediction_vector

        #print "Press any key to continue:"
        #sys.stdin.read(1)
        
#  =====  END OF MAIN CYCLE  =====  

    result_matrix = scipy.sparse.csr_matrix(prediction_matrix)
    scipy.io.mmio.mmwrite(prediction_file_name, result_matrix, field = 'real', precision = 5)
