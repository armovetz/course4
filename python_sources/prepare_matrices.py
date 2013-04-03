import scipy.io.mmio
import scipy.sparse
import numpy
import os
import datetime
import subprocess

import ini
from ini import *
import misc_functions
from misc_functions import *

def createItem_x_MetaMatrix_global():
    
    print "STARTED computing global Item_x_Meta matrix"

    seminars_meta_file = open("../data/well_done/meta", 'r')
    
    item_X_meta_matrix = numpy.zeros((ITEMS_NUMB, MAX_METAS_NUMB), dtype = int)
    
    for seminar_id in range(ITEMS_NUMB):
        
        #print seminar_id
        
        seminar_string = seminars_meta_file.readline()
        
        for meta in METAS_TO_USE:
            item_X_meta_matrix[seminar_id][meta] = misc_functions.getMeta(seminar_string, meta)

    seminars_meta_file.close()
    
    csr_matrix_to_write = scipy.sparse.csr_matrix(item_X_meta_matrix)
    scipy.io.mmio.mmwrite("../data/well_done/items-metas_global", csr_matrix_to_write)

    print "SUCCESS! \n ITEMS x METAS global matrix - prepared!"

# =================================

"""def createItem_x_MetaMatrices_local():

    seminars_meta_list = []
    seminars_meta_file = open("../data/well_done/meta", 'r')
    for seminar_string in seminars_meta_file:
        seminars_meta_list.append(seminar_string)
    seminars_meta_file.close()
    
    os.chdir("../data/tmp/cross_validation")
    
    for i in range(SWITCHES_USERS_NUMB):
        for j in range(SWITCHES_ITEMS_NUMB):
            
            print "window: user_window = ", i + 1, "/", SWITCHES_USERS_NUMB
            print "        item_window = ", j + 1, "/", SWITCHES_ITEMS_NUMB
    
            # creating new directory for current case
            cur_dir = str(i) + "_" + str(j)
            os.chdir(cur_dir)
            
            # delete previous old prepared matrices
            subprocess.call(["rm", "-rf", "items_metas-local"])
    
            coords = misc_functions.getWindowCoords()
    
            item_X_meta_matrix = numpy.zeros((coords[3] - coords[1] + 1, MAX_METAS_NUMB), dtype = int)
    
            for seminar_id in range(coords[1], coords[3] + 1):
                seminar_string = seminars_meta_list[seminar_id - coords[1]]
        
                for meta in METAS_TO_USE:
                    item_X_meta_matrix[seminar_id - coords[1]][meta] = misc_functions.getMeta(seminar_string, meta)

            now = datetime.datetime.now()
            now_string = now.strftime("%Y-%m-%d %H:%M")
            csr_matrix_to_write = scipy.sparse.csr_matrix(item_X_meta_matrix)
            scipy.io.mmio.mmwrite("items-metas_local", csr_matrix_to_write, now_string, 'integer')
            
            os.chdir("..")

    print "SUCCESS! \n ITEMS x METAS local matrices - prepared!"
"""

# ===============================================

def prepareDirs():
    
    os.chdir("../data/tmp/cross_validation")
    
    for i in range(SWITCHES_USERS_NUMB):
        for j in range(SWITCHES_ITEMS_NUMB):
            
            cur_dir = str(i) + "_" + str(j)
            os.mkdir(cur_dir)
            os.chdir(cur_dir)
            
            # defining boundaries for blank 'window'
            start_zero_user = WINDOW_USERS_SIZE * i
            start_zero_item = WINDOW_ITEMS_SIZE * j
            stop_zero_user = start_zero_user + WINDOW_USERS_SIZE
            stop_zero_item = start_zero_item + WINDOW_ITEMS_SIZE
            if stop_zero_user > USERS_NUMB:
                stop_zero_user = USERS_NUMB
            if stop_zero_item > ITEMS_NUMB:
                stop_zero_item = ITEMS_NUMB
            

            # writing coordinates of blank 'window' to local file
            coord_file = open("window_coord", 'w')
            coord_file.write("start_zero_user = " + str(start_zero_user) + "\n")
            coord_file.write("start_zero_item = " + str(start_zero_item) + "\n")
            coord_file.write("stop_zero_user = " + str(stop_zero_user) + "\n")
            coord_file.write("stop_zero_item = " + str(stop_zero_item) + "\n")
            coord_file.close()

            os.chdir("..")
        
    os.chdir("../../../python_sources")
    print "DIRS PREPARED!"

# ===============================================

def computeMetaMatrix(meta_list, meta_id_position):
    """ Function computes user_X_meta matrix for current <meta_id_position>
    (that shows current meta), and saves this matrix as "users-<meta>.mtx
    in directory for current case
    """

    # creating new matrix
    meta_matrix = numpy.zeros((USERS_NUMB, 0), dtype = int)
    
    # reading local history matrix
    history_matrix = scipy.io.mmio.mmread("history.mtx").tocsr()
    
    # some routine before main loop
    cur_meta_items = []
    cur_meta_id = 1
    
    # MAIN LOOP
    for line in meta_list:
        
        if line.split('\t')[meta_id_position] == "":
            continue   # seminar with unknown meta is ignored

        line_meta_id = int(line.split('\t')[meta_id_position])
        """ !!!! DAFUQ!!!! """
        line_semin_id = int(line.split('\t')[0]) # considering everywhere semin_id_position == 0

        if line_meta_id != cur_meta_id: # new meta_id detected
            new_meta_col = numpy.zeros((USERS_NUMB, 1), dtype = int)
            
            # stacking empty columns of meta for not visited seminars
            while(line_meta_id != cur_meta_id + 1):
                if(cur_meta_id != 1) and (line_meta_id != 1):
                    meta_matrix = numpy.hstack((meta_matrix, new_meta_col))
                    cur_meta_id += 1
            
            for cur_item in cur_meta_items:
                cur_item_col = (history_matrix[:,cur_item - 1]).toarray()
                new_meta_col = new_meta_col + cur_item_col
            
            meta_matrix = numpy.hstack((meta_matrix, new_meta_col))
            
            # clean list if new meta_id begins
            #print "meta_id = ", cur_meta_id, "; visiters = ", len(cur_meta_items)
            cur_meta_items = []
            cur_meta_id += 1

        cur_meta_items.append(line_semin_id)    
        
    meta_matrix_csr = scipy.sparse.csr_matrix(meta_matrix)
    
    # writing new <meta_matrix> to file    
    now = datetime.datetime.now()
    now_string = now.strftime("%Y-%m-%d %H:%M")
    meta_matrix_file_name = "users-" + METAS_TO_USE[meta_id_position]
    scipy.io.mmio.mmwrite(meta_matrix_file_name, meta_matrix_csr, now_string, 'integer')
    
# ====



def createUser_x_MetaMatrices():
    """ Function prepares several training matrices, 
        and corresponding meta matrices for them """

    os.chdir("../data/tmp/cross_validation")
    
    # delete previous old prepared matrices
    subprocess.call(["rm", "-rf", "users-.*"])
    
    # cycle for each case
    for i in range(SWITCHES_USERS_NUMB):
        for j in range(SWITCHES_ITEMS_NUMB):
            
            print "window: user_window = ", i + 1, "/", SWITCHES_USERS_NUMB
            print "        item_window = ", j + 1, "/", SWITCHES_ITEMS_NUMB

            # changing directory for current case
            cur_dir = str(i) + "_" + str(j)
            os.chdir(cur_dir)
            
            # reading coords for current case
            coords = misc_functions.getWindowCoords()

            for meta in METAS_TO_USE:
                print "Computing meta matrix for ", METAS_TO_USE[meta]
                meta_matrix_name = "users-" + METAS_TO_USE[meta]
                
                meta_list = []
                meta_file = open("../../../well_done/meta", 'r')
                for line in meta_file:
                    meta_list.append(line)
                meta_file.close()
                
                # sort strings of meta of seminars for future indexing
                sorted_list = misc_functions.sortMetaListByMeta(meta_list, meta)
                
                # main function for current case and <meta>
                computeMetaMatrix(sorted_list, meta)
            
            # returning to "cross_validation" directory
            os.chdir("..")

    os.chdir("../../../python_sources")
    print "TOTAL SUCCESS! \n USER x META local matrices are prepared!"

# =======

# ==========================================

def prepareTrainingMatrices():
    """ Function prepareTrainingMatrices """
    
    os.chdir("../data/tmp/cross_validation")
    
    # cycle for each case
    for i in range(SWITCHES_USERS_NUMB):
        for j in range(SWITCHES_ITEMS_NUMB):
            
            print "Writing local training matrix ..."
            now = datetime.datetime.now()
            now_string = now.strftime("%Y-%m-%d %H:%M")

            print "window: user_window = ", i + 1, "/", SWITCHES_USERS_NUMB
            print "        item_window = ", j + 1, "/", SWITCHES_ITEMS_NUMB

            # changing directory for current case
            cur_dir = str(i) + "_" + str(j)
            os.chdir(cur_dir)
            
            # reading coords for current case
            coords = misc_functions.getWindowCoords()

            print "Reading history matrix ..."
            history_matrix = scipy.io.mmio.mmread("../../../well_done/history.mm")
            print "...done!"
            
            
            
            print "Converting sparse history_matrix to numpy array ..." # getting ENORMOUS matrix
            local_training_matrix = history_matrix.toarray()
            print "...done!"
            
            print "Saving 'empty' testing window..."
            local_training_matrix[coords[0] : coords[2], coords[1] : coords[3]] = 0
            print "...done!"
            csr_local_training_matrix = scipy.sparse.csr_matrix(local_training_matrix)
            #trying to delete this ENORMOUS matrix
            del local_training_matrix
            
            scipy.io.mmio.mmwrite("history", csr_local_training_matrix, now_string, 'integer')
            print "...done!"
            
            
            
            
            os.chdir("..")
    
    os.chdir("../../../python_sources")

    print "TOTAL SUCCESS! \n Training local matrices are prepared!"
    
# =====================================================================

def prepareTestClusters():
    #test_matrix = scipy.io.mmio.mmread("test.mtx")
    test_matrix_file = open("test.mtx", 'r')
    
    # create item_X_time list
    item_X_time_list = []
    meta_file = open("../../../well_done/meta", 'r')
    for line in meta_file:
        item_X_time_list.append(getMetaString(line, TIME_ID))
    meta_file.close()
    
    
    # reading coords for current case
    coords = misc_functions.getWindowCoords()
    
    # stuff before cycle
    clusters_list = []
    cur_cluster = ["user" + "\t" + str(coords[0] + 1)]
    cur_user = 1
    
    # skip comments
    for i in range(3):
        test_matrix_file.readline()
    
    for line in test_matrix_file:
        user = int(line.split()[0])
        
        # next user
        if user != cur_user:
            cur_user = user
            clusters_list.append(cur_cluster)
            cur_cluster = ["user " + str(user)]
        
        item = int(line.split()[1])
        time_bounds = getTimeInterval(item, item_X_time_list)
        cur_cluster.append(str(time_bounds[0]) + "\t" + str(item) + "\t" + str(time_bounds[1]))
    
    test_clusters_file = open("test_clusters", 'w')
    test_clusters_file.write("low_bound high_bound  item_id\n")
    for cluster in clusters_list:
        for line in cluster:
            test_clusters_file.write(line + "\n")


# =====================================================================
def prepareTestingMatrices():
    """ Function prepareTrainingMatrices """
    
    os.chdir("../data/tmp/cross_validation")
    
    # cycle for each case
    for i in range(SWITCHES_USERS_NUMB):
        for j in range(SWITCHES_ITEMS_NUMB):
            
            print "Writing local training matrix ..."
            now = datetime.datetime.now()
            now_string = now.strftime("%Y-%m-%d %H:%M")

            print "window: user_window = ", i + 1, "/", SWITCHES_USERS_NUMB
            print "        item_window = ", j + 1, "/", SWITCHES_ITEMS_NUMB

            # changing directory for current case
            cur_dir = str(i) + "_" + str(j)
            os.chdir(cur_dir)
            
            # reading coords for current case
            coords = misc_functions.getWindowCoords()

            print "Reading history matrix ..."
            history_matrix = scipy.io.mmio.mmread("../../../well_done/history.mm")
            print "...done!"
            
            print "Saving test matrix..."
            local_testing_matrix = (history_matrix.tocsr())[coords[0] : coords[2], coords[1] : coords[3]].copy()
            scipy.io.mmio.mmwrite("test", local_testing_matrix, now_string, 'integer')
            print "...done!"
            
            print "Creating local testing clusters..."
            prepareTestClusters()
            #misc_functions.gag();
            
            os.chdir("..")
    
    os.chdir("../../../python_sources")

    print "TOTAL SUCCESS! \n Local test clusters are prepared!"
