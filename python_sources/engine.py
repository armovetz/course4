import sys
import scipy.sparse
import scipy.io.mmio
import numpy
from numpy import *

import misc_functions
from misc_functions import *
import ini
from ini import *

def prediction(prediction_file_name, clusters_list):
    """
        Main function for computing prediction rating.
    """
    
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
    
    item_X_meta_matrix = scipy.io.mmio.mmread("../../../well_done/items-metas_global.mtx").toarray()
    
    # getting meta matrices for corresponding using metas
    meta_ctr = 0
    meta_matrices = []
    for meta in METAS_TO_USE:
        meta_matrice_file_name = "users-" + METAS_TO_USE[meta] + ".mtx"
        exec("meta_matrices.append(scipy.io.mmio.mmread(\"" + meta_matrice_file_name + "\").toarray())")

    #user_counter = 0
    #for user in test_users:
    for cur_cluster in clusters_list:
    
        #print "cur_cluster[0] = ", cur_cluster[0]
        user = int (cur_cluster[0].split("\t")[1])
        #print "user #", user
        
        #user_metas = {} - changed to list because of problem with dimension
        user_metas = []
        
        values = zeros((len(METAS_TO_USE), len(test_items)), dtype = float)
        meta_ctr = 0
        for meta in METAS_TO_USE:
            #print "    meta_matrices = ", meta_matrices
            #print "    meta_matrices[meta_ctr] = ", meta_matrices[meta_ctr]
            user_vector = meta_matrices[meta_ctr][user]
            #print "    user_vector = ", user_vector
            #print "    len(user_metas) = ", len(user_metas)
            #print "    meta_ctr = ", meta_ctr
            #misc_functions.step()
            
            # normalizing counts of visited metas to use them as weights later
            if max(user_vector) != 0:
                user_metas.append(1.0 * user_vector / max(user_vector))
            else:
                user_metas.append(zeros((len(user_vector), ), dtype = float))
            #print "    user_metas[meta_ctr] = ", user_metas[meta_ctr]
            #print "    user_metas[meta_ctr].shape = ", user_metas[meta_ctr].shape
            
            #for item in test_items:
            for cluster in cur_cluster[1 : ]:
                start_cluster_item = int(cluster.split("\t")[0])
                stop_cluster_item  = int(cluster.split("\t")[2])
                
                cluster_items = range(start_cluster_item, stop_cluster_item + 1)
                
                for item in cluster_items:
                    meta_value = item_X_meta_matrix[item, meta]
                    #print "        meta_value = ", meta_value
                
                    #print "        item = ", item
                    #step()
                    values[meta_ctr][item - coords[1]] = (user_metas[meta_ctr])[meta_value - 1]
                    

            meta_ctr += 1
        #print "values[:, 0:10] = ", values[:, 0:10]
        prediction_vector = numpy.sum(META_WEIGHTS * values, axis = 0)
        #print "prediction_vector[0:10] = ", prediction_vector[0:10]
        #print "sum(prediction_vector) = ", sum(prediction_vector)
        prediction_matrix[user - coords[0]] = prediction_vector
        
        #step()
        
#  =====  END OF MAIN CYCLE  =====  

    result_matrix = scipy.sparse.csr_matrix(prediction_matrix)
    scipy.io.mmio.mmwrite(prediction_file_name, result_matrix, field = 'real', precision = 5)







#------------------------------------------------
# --- ONLY ARCHAEOLOGISTS ALLOWED -----------------
# -------------------------------------------------

"""# using only visited seminars for next predictions
        visited_items = []
        user_vector = training_matrix[user].toarray()
        for item in training_items:
            if user_vector[item] != 0:
                visited_items.append(item)

        metas_X_items = zeros((len(metas_to_use), 0), dtype = int)
        for item in visited_items:
            
            metas_for_item = numpy.zeros(len(metas_to_use))
            i = 0
            for meta in metas_to_use:
                metas_for_item[i] = seminars_meta_list[item][meta]
                i += 1
            
            metas_X_items = numpy.hstack((metas_X_items, metas_for_item))
            
        # filling metas_X_items with values
        
        prediction_values = numpy.array((len(metas_to_use), len(visited_items)), dtype = float)
        i = j = 0
        for meta_vector in metas_X_items:
            for item in meta_vector:
                prediction_values[i,j] = 
"""
        
        
