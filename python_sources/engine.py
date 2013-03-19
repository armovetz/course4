import sys
import scipy.sparse
import scipy.io.mmio
import numpy
from numpy import *

import misc_functions
import ini
from ini import *

# .INI
#metas_to_use = {3 : "place", 4 : "presenter", 6 : "category", 9 : "organizer", 11 : "city", 15 : "seminartype"}
metas_to_use = {6 : "categories", 15 : "seminar_types"}

CONST_RATING_TRESHOLD = 0.4
#meta_weights = numpy.array([[0], [0], [0], [0], [0], [0], [0.7], [0], [0], [0], [0], [0], [0], [0], [0], [0.3], [0]], dtype = float)
meta_weights = numpy.array([[0.7], [0.3]], dtype = float)
#map_vector = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

def myRound(prediction_vector):
    res = zeros((1, len(prediction_vector)), dtype = int)
    for i in range(len(prediction_vector)):
        if prediction_vector[i] > CONST_RATING_TRESHOLD:
            res[i] = rating
        else:
            res[0,i] = 0
    return res

def prediction():
    """
    """
    
    coords = misc_functions.getWindowCoords()
    
    """coord_file = open("window_coord", 'r')
    start_zero_user = int(coord_file.readline().split()[2])
    start_zero_item = int(coord_file.readline().split()[2])
    stop_zero_user = int(coord_file.readline().split()[2])
    stop_zero_item = int(coord_file.readline().split()[2])
    coord_file.close()"""
    
    test_users = range(coords[0], coords[2]) # +-1 OR WHAT!?
    test_items = range(coords[1], coords[3])
    
    prediction_matrix = zeros((len(test_users), len(test_items)), dtype = float)
    
    training_matrix = scipy.io.mmio.mmread("history.mtx").tocsr()
    
    item_X_meta_matrix = scipy.io.mmio.mmread("../../../well_done/items-metas_global.mtx").toarray()
    
    """ CHANGE THIS SHIT 
    # getting metas for seminars
    seminars_meta_list = []
    for line in open("../../../well_done/meta"):
        seminars_meta_list.append(line.split('\t'))
    """
    
    # getting meta matrices for corresponding using metas
    meta_ctr = 0
    meta_matrices = []
    for meta in metas_to_use:
        meta_matrice_file_name = "users-" + metas_to_use[meta] + ".mtx"
        exec("meta_matrices.append(scipy.io.mmio.mmread(\"" + meta_matrice_file_name + "\").toarray())")

    #user_counter = 0
    for user in test_users:
        #print "user #", user
        #form meta 
        #user_metas = {}
        user_metas = {}
        values = zeros((len(metas_to_use), len(test_items)), dtype = float)
        meta_ctr = 0
        for meta in metas_to_use:
            print "meta = ", meta

            print "meta_matrices = ", meta_matrices
            print "meta_matrices[meta_ctr] = ", meta_matrices[meta_ctr]
            print "meta_matrices[meta_ctr][user] = ", meta_matrices[meta_ctr][user]
            user_vector = meta_matrices[meta_ctr][user]
            print "user_vector = ", user_vector
            # normalizing users counts of visited meta for using as weights
            if max(user_vector) != 0:
                user_metas[meta] = 1.0 * user_vector / max(user_vector)
            else:
                user_metas[meta] = zeros((1, len(user_vector)), dtype = float)

            for item in test_items:
                meta_value = item_X_meta_matrix[item - coords[1]][meta]
                #print "meta_ctr = ", meta_ctr
                #print "item = ", item
                #print "start_zero_item = ", start_zero_item
                #print "len(values) = ", len(values)
                
                #print "user_metas = ", user_metas
                #print "meta_value = ", meta_value
                #print "user_metas[meta] = ", user_metas[meta]
                #print "user_metas[meta][meta_value] = ", (user_metas[meta][0])[meta_value]
                
                values[meta_ctr][item - start_zero_item] = (user_metas[meta][0])[meta_value]
                #print "values[meta_ctr][item - start_zero_item] = ", values[meta_ctr][item - start_zero_item]
                #print "user_metas[meta][meta_value] = ", user_metas[meta][meta_value]


        meta_ctr += 1

        print "values.shape = ", values.shape
        print "values = ", values
        print "sum(sum(values)) = ", sum(sum(values))
        print "meta_weights.shape = ", meta_weights.shape
        print "meta_weights = ", meta_weights
        prediction_vector = numpy.sum(meta_weights * values, axis = 0)
        print "prediction_vector = ", prediction_vector
        
        #prediction_matrix[user - start_zero_user] = myRound(prediction_vector)
        prediction_matrix[user - start_zero_user] = prediction_vector
        
        print "Press any key to continue:"
        sys.stdin.read(1)
        
#  =====  END OF MAIN CYCLE  =====  

    result_matrix = scipy.sparse.csr_matrix(prediction_matrix)
    scipy.io.mmio.mmwrite("prediction", result_matrix, field = 'real', precision = 3)







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
        
        
