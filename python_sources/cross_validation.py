import os, subprocess
import datetime
import numpy
from numpy import *
#import SVD

import scipy.sparse
from scipy.sparse import *
import scipy.io.mmio
from scipy.io.mmio import *

import CreateMetaMatrix2
import ini
from ini import *

"""# .INI settings
TRAINING_USERS_RATE = 0.8
TRAINING_ITEMS_RATE = 0.8
TESTING_USERS_RATE = 1 - TRAINING_USERS_RATE
TESTING_ITEMS_RATE = 1 - TRAINING_ITEMS_RATE
switches_users_numb = int(1 / TESTING_USERS_RATE)
switches_items_numb = int(1 / TESTING_ITEMS_RATE)

history_matrix = scipy.io.mmio.mmread("../data/well_done/history.mm")
users_numb = history_matrix.shape[0]
items_numb = history_matrix.shape[1]
del history_matrix

window_users_size = int(users_numb / switches_users_numb)
window_items_size = int(items_numb / switches_items_numb)"""

meta_matrices = {6 : "users-categories.mtx", 11 : "users-city.mtx", 15 : "users-seminar_types.mtx"}

def prepareUser_x_MetaMatrices():
    """ Function prepares several training matrices, 
        and corresponding meta matrices for them """
        

    os.chdir("../data/tmp/cross_validation")
    
    # delete previous old prepared matrices
    subprocess.call(["rm", "-rf", "*"])
    
    for i in range(switches_users_numb):
        for j in range(switches_items_numb):
            
            print "window: user_window = ", i + 1, "/", switches_users_numb , \
            "; item_window = ", j + 1, "/", switches_items_numb
    
            print "Reading history matrix ..."
            history_matrix = scipy.io.mmio.mmread("../../well_done/history.mm")
            users_numb = history_matrix.shape[0]
            items_numb = history_matrix.shape[1]
            
            # defining boundaries for blank 'window'
            start_zero_user = window_users_size * i
            start_zero_item = window_items_size * j
            stop_zero_user = start_zero_user + window_users_size
            stop_zero_item = start_zero_user + window_items_size
            if stop_zero_item > items_numb:
                stop_zero_item = items_numb
            if stop_zero_user > users_numb:
                stop_zero_user = users_numb

            """
            print "start_zero_user = ", start_zero_user
            print "start_zero_item = ", start_zero_item
            print "stop_zero_user = ", stop_zero_user
            print "stop_zero_item = ", stop_zero_item
            """
            
            # creating new directory for current case
            cur_dir = str(i) + "_" + str(j)
            os.mkdir(cur_dir)
            os.chdir(cur_dir)
            
            # writing coordinates of blank 'window' to local file
            coord_file = open("window_coord", 'w')
            coord_file.write("start_zero_user = " + str(start_zero_user) + "\n")
            coord_file.write("start_zero_item = " + str(start_zero_item) + "\n")
            coord_file.write("stop_zero_user = " + str(stop_zero_user) + "\n")
            coord_file.write("stop_zero_item = " + str(stop_zero_item) + "\n")
            coord_file.close()

            print "Converting sparse history_matrix to numpy array ..."
            local_training_matrix = history_matrix.toarray()
            print "... done!"
            print "Creating 'empty' testing window..."
            local_training_matrix[start_zero_user : stop_zero_user, start_zero_item : stop_zero_item] = 0
            print "... done!"
            csr_local_training_matrix = csr_matrix(local_training_matrix)
            del local_training_matrix
            
            now = datetime.datetime.now()
            now_string = now.strftime("%Y-%m-%d %H:%M")
            scipy.io.mmio.mmwrite("history", csr_local_training_matrix, now_string, 'integer')
            
            CreateMetaMatrix2.createMetaMatrices("history.mtx", "../../../well_done/meta")
            
            os.chdir("..")

    print "TOTAL SUCCESS! Meta matrices are prepared."

def launchCrossValidation(prediction_function):
    """ """
    os.chdir("../data/tmp/cross_validation")
    
    timer_start = datetime.datetime.now()
    
    print "WARNING : CORRESPONDING MATRICES FOR EACH CASE MUST BE PREPARED!"
    
    sum_error = 0
    
    #for i in range(switches_users_numb):
        #for j in range(switches_items_numb):
    
    for i in range(1):
        for j in range(1):
            
            print "window: user_window = ", i + 1, "/", SWITCHES_USERS_NUMB , \
            "; item_window = ", j + 1, "/", SWITCHES_USERS_NUMB
            
            # switching directory for current case
            cur_dir = str(i) + "_" + str(j)
            os.chdir(cur_dir)
    
            prediction_function()
            #sum_error += estimate_function()
            
            os.chdir("..")

    timer_stop = datetime.datetime.now()
    
    print "TOTAL TIME = ", (finish - start).seconds, "secs"
    
    #return (sum_error / (switches_items_numb * switches_users_numb))
    return 0

def prepareItem_x_MetaMatrices():
    """ Function prepares items_x_metas matrices for each case
        of cross-validation """

    os.chdir("../data/tmp/cross_validation")

    for i in range(switches_users_numb):
        for j in range(switches_items_numb):
            
            print "window: user_window = ", i + 1, "/", switches_users_numb , \
            "; item_window = ", j + 1, "/", switches_items_numb
    
            # changing directory for current case
            cur_dir = str(i) + "_" + str(j)
            os.chdir(cur_dir)
            
            # writing coordinates of blank 'window' to local file
            coord_file = open("window_coord", 'w')
            coord_file.write("start_zero_user = " + str(start_zero_user) + "\n")
            coord_file.write("start_zero_item = " + str(start_zero_item) + "\n")
            coord_file.write("stop_zero_user = " + str(stop_zero_user) + "\n")
            coord_file.write("stop_zero_item = " + str(stop_zero_item) + "\n")
            coord_file.close()

            print "Converting sparse history_matrix to numpy array ..."
            local_training_matrix = history_matrix.toarray()
            print "... done!"
            print "Creating 'empty' testing window..."
            local_training_matrix[start_zero_user : stop_zero_user, start_zero_item : stop_zero_item] = 0
            print "... done!"
            csr_local_training_matrix = csr_matrix(local_training_matrix)
            del local_training_matrix
            
            now = datetime.datetime.now()
            now_string = now.strftime("%Y-%m-%d %H:%M")
            scipy.io.mmio.mmwrite("history", csr_local_training_matrix, now_string, 'integer')
            
            CreateMetaMatrix2.createMetaMatrices("history.mtx", "../../../well_done/meta")

            
            os.chdir("..")

    print "TOTAL SUCCESS! Meta matrices are prepared."
