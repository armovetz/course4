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
    """
        Function computes item_X_meta matrix for all the seminars
        (that shows current meta), and saves this matrix as "items-metas_global.mtx"
        in "data/well_done" directory.
    """
    print "STARTED computing global Item_x_Meta matrix"

    seminars_meta_file = open("../data/well_done/meta", 'r')
    
    item_X_meta_matrix = numpy.zeros((ITEMS_NUMB, MAX_METAS_NUMB), dtype = int)
    
    for seminar_id in range(ITEMS_NUMB):
        
        seminar_string = seminars_meta_file.readline()
        
        #for meta in METAS_TO_USE:
        for meta in range(17):
            item_X_meta_matrix[seminar_id][meta] = misc_functions.getMeta(seminar_string, meta)

    seminars_meta_file.close()
    
    csr_matrix_to_write = scipy.sparse.csr_matrix(item_X_meta_matrix)
    scipy.io.mmio.mmwrite("../data/well_done/items-metas_global", csr_matrix_to_write)

    print "SUCCESS! \n ITEMS x METAS global matrix - prepared!"
# ==  createItem_x_MetaMatrix_global  ================================



def createItem_x_ItemSimilarity_local(training_items, test_items):
    
    meta_matrix = scipy.io.mmio.mmread("../../../well_done/items-metas_global").tocsr()
    similarity_file = open("item_similarities", 'w')
    
    for i in test_items:
        i_vector = meta_matrix[i].toarray()[0]
        print "i_vector = ", i_vector
        
        for j in training_items:
            j_vector = meta_matrix[j].toarray()[0]
            
            similarity = misc_functions.cosineSimilarity(i_vector, j_vector)
            
            similarity_file.write(str(i) + "\t" + str(j) + "\t" + str(similarity) + "\n")
    
    similarity_file.close()

def createItem_x_ItemSimilarities(time_flag):
    
    if time_flag:
        """
            SPECIAL TIME CROSS-VALIDATION
        """
        os.chdir("../data/tmp/time_cross_validation")
    
        for i in range(ITERATIONS_NUMB):
            print "Iteration = ", i + 1, "/", ITERATIONS_NUMB
            
            # changing directory for current case
            cur_dir = str(i)
            os.chdir(cur_dir)
            
            # reading coords for current case
            coords = misc_functions.getWindowCoords()
    
            # get training and test items lists
            test_items = range(coords[1], coords[3] + 1)
            training_items = range(0, coords[1])
            
            createItem_x_ItemSimilarity_local(training_items, test_items)
                
            # returning to "cross_validation" directory
            os.chdir("..")
    else:    
        """
            CLASSIC CROSS-VALIDATION
        """
        os.chdir("../data/tmp/cross_validation")
    
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

                # get training and test items lists
                test_items = range(coords[1], coords[3] + 1)
                training_items = range(0, coords[1])
                training_items.extend(range((coords[3] + 1), ITEMS_NUMB))

                createItem_x_ItemSimilarity_local(training_items, test_items)

                # returning to "cross_validation" directory
                os.chdir("..")

    os.chdir("../../../python_sources")
    print "TOTAL SUCCESS! \n local similarities matrices are prepared!"

# ==  createItem_x_ItemSimilarity  ===================================
def createItem_x_ItemSimilarities2(time_flag):
    
    if time_flag:
        """
            SPECIAL TIME CROSS-VALIDATION
        """
        os.chdir("../data/tmp/time_cross_validation")
    
        for i in range(ITERATIONS_NUMB):
            print "Iteration = ", i + 1, "/", ITERATIONS_NUMB
            
            # changing directory for current case
            cur_dir = str(i)
            os.chdir(cur_dir)
            
            # reading coords for current case
            coords = misc_functions.getWindowCoords()
    
            # get training and test items lists
            test_items = range(coords[1], coords[3] + 1)
            training_items = range(0, coords[1])
            
            createItem_x_ItemSimilarity_local(training_items, test_items)
                
            # returning to "cross_validation" directory
            os.chdir("..")
    else:    
        """
            CLASSIC CROSS-VALIDATION
        """
        os.chdir("../data/tmp/cross_validation")
    
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

                # get training and test items lists
                test_items = range(coords[1], coords[3] + 1)
                training_items = range(0, coords[1])
                training_items.extend(range((coords[3] + 1), ITEMS_NUMB))

                createItem_x_ItemSimilarity_local(training_items, test_items)

                # returning to "cross_validation" directory
                os.chdir("..")

    os.chdir("../../../python_sources")
    print "TOTAL SUCCESS! \n local similarities matrices are prepared!"
# ==  createItem_x_ItemSimilarity  ===================================



def prepareDirs(time_flag):
    """
        Function prepares directories and stuff for cross-validation
        - for classic cross-validation or special time cross-validation.
        Directories are located in "data/tmp/cross_validation" and
        "data/tmp/cross_validaton".
    """
    
    if time_flag:
        """
            SPECIAL TIME CROSS-VALIDATION
        """
        os.chdir("../data/tmp/time_cross_validation")
        for i in range(ITERATIONS_NUMB):
            print "Iteration = ", i + 1, "/", ITERATIONS_NUMB    
            
            cur_dir = str(i)
            os.mkdir(cur_dir)
            os.chdir(cur_dir)
            
            # defining boundaries for training 'window'
            start_zero_user = 0
            start_zero_item = ITEM_STEP * (i + 1)
            stop_zero_user = USERS_NUMB - 1
            stop_zero_item = start_zero_item + ITEM_STEP - 1

            # writing coordinates of blank 'window' to local file
            coord_file = open("window_coord", 'w')
            coord_file.write("start_zero_user = " + str(start_zero_user) + "\n")
            coord_file.write("start_zero_item = " + str(start_zero_item) + "\n")
            coord_file.write("stop_zero_user = " + str(stop_zero_user) + "\n")
            coord_file.write("stop_zero_item = " + str(stop_zero_item) + "\n")
            coord_file.close()

            os.chdir("..")
            
    else:
        """
            CLASSIC CROSS-VALIDATION
        """
        os.chdir("../data/tmp/cross_validation")
    
        for i in range(SWITCHES_USERS_NUMB):
            for j in range(SWITCHES_ITEMS_NUMB):
            
                cur_dir = str(i) + "_" + str(j)
                os.mkdir(cur_dir)
                os.chdir(cur_dir)
            
                # defining boundaries for blank 'window'
                start_zero_user = WINDOW_USERS_SIZE * i
                start_zero_item = WINDOW_ITEMS_SIZE * j
                stop_zero_user = start_zero_user + WINDOW_USERS_SIZE - 1
                stop_zero_item = start_zero_item + WINDOW_ITEMS_SIZE - 1
                if stop_zero_user > USERS_NUMB - 1:
                    stop_zero_user = USERS_NUMB - 1
                if stop_zero_item > ITEMS_NUMB - 1:
                    stop_zero_item = ITEMS_NUMB - 1
                
                if (i == SWITCHES_USERS_NUMB - 1): # not enough for last case
                    stop_zero_user = USERS_NUMB - 1    
                if (j == SWITCHES_ITEMS_NUMB - 1): # not enough for last case
                    stop_zero_item = ITEMS_NUMB - 1
                
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
# == prepareDirs  ====================================================


def computeMetaMatrix(meta_list, meta_id_position):
    """
        Internal function.
        Function computes user_X_meta matrix for current <meta_id_position>
        (that shows current meta), and saves this matrix as "users-<meta>.mtx
        in directory for current case.
    """

    # creating new matrix
    meta_matrix = numpy.zeros((USERS_NUMB, 0), dtype = int)
    
    # reading local history matrix
    history_matrix = scipy.io.mmio.mmread("history.mtx").tocsr()
    
    # some routine before main loop
    cur_meta_items = []
    """ id-- here????? """
    #cur_meta_id = 1
    cur_meta_id = 0 
    
    # MAIN LOOP
    for line in meta_list:
        
        # seminar with unknown meta is ignored
        if (misc_functions.getMeta(line, meta_id_position) == -1):
            continue

        """ !!!! DAFUQ!!!! """
        #line_meta_id = int(line.split('\t')[meta_id_position])
        line_meta_id = getMeta(line, meta_id_position)
        line_semin_id = getMeta(line, 0) # considering everywhere semin_id_position == 0
        #print line_semin_id
        #step()

        # if new meta_id detected
        if line_meta_id != cur_meta_id:
            print line_meta_id
            new_meta_col = numpy.zeros((USERS_NUMB, 1), dtype = int)
            
            for cur_item in cur_meta_items:
                cur_item_col = (history_matrix[ : , cur_item]).toarray()
                new_meta_col = new_meta_col + cur_item_col

            if cur_meta_items != []:
                meta_matrix = numpy.hstack((meta_matrix, new_meta_col))
            
            # stacking empty columns of meta for not visited seminars
            while(line_meta_id != cur_meta_id + 1):
                meta_matrix = numpy.hstack((meta_matrix, numpy.zeros((USERS_NUMB, 1), dtype = int)))
                cur_meta_id += 1
            
            # clean list if new meta_id begins
            #print "meta_id = ", cur_meta_id, "; visiters = ", len(cur_meta_items)
            cur_meta_items = []
            """ !!! """
            cur_meta_id += 1
            
            if cur_meta_id != line_meta_id:
                raise Exception("mismatch cur_meta_id")
            """ !!! """

        cur_meta_items.append(line_semin_id)
    
    # stacking last column
    new_meta_col = numpy.zeros((USERS_NUMB, 1), dtype = int)
    for cur_item in cur_meta_items:
        cur_item_col = (history_matrix[ : , cur_item]).toarray()
        new_meta_col = new_meta_col + cur_item_col
    if cur_meta_items != []:
        meta_matrix = numpy.hstack((meta_matrix, new_meta_col))
        
    meta_matrix_csr = scipy.sparse.csr_matrix(meta_matrix)
    
    # writing new <meta_matrix> to file    
    now = datetime.datetime.now()
    now_string = now.strftime("%Y-%m-%d %H:%M")
    meta_matrix_file_name = "users-" + METAS_TO_USE[meta_id_position]
    scipy.io.mmio.mmwrite(meta_matrix_file_name, meta_matrix_csr, now_string, 'integer')
# ==  computeMetaMatrix  =============================================


def createUser_x_MetaMatrices(time_flag):
    """
        Function prepares user_X_meta matrices for each case of 
        cross-validation or time_cross_validation - depending on flag.
    """

    # delete previous old prepared matrices
    #subprocess.call(["rm", "-rf", "users-.*"])
    
    if time_flag:
        """
            SPECIAL TIME CROSS-VALIDATION
        """
        os.chdir("../data/tmp/time_cross_validation")
    
        for i in range(ITERATIONS_NUMB):
            print "Iteration = ", i + 1, "/", ITERATIONS_NUMB
            
            # changing directory for current case
            cur_dir = str(i)
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
    else:    
        """
            CLASSIC CROSS-VALIDATION
        """
        os.chdir("../data/tmp/cross_validation")
    
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
                
                    print "A"
                    # sort strings of meta of seminars for future indexing
                    sorted_list = misc_functions.sortMetaListByMeta(meta_list, meta)
                
                    # main function for current case and <meta>
                    computeMetaMatrix(sorted_list, meta)
            
                # returning to "cross_validation" directory
                os.chdir("..")

    os.chdir("../../../python_sources")
    print "TOTAL SUCCESS! \n USER x META local matrices are prepared!"
# ==  createUser_x_MetaMatrices  =====================================


def makeClusters():
    """
        Internal function.
        Function prepares test clusters when launched inside directory
        of case of cross-validation. Clusters are being saved in 
        "test_clusters" in directory of the case.
    """
    
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
    cur_user_id = str(coords[0])
    cur_cluster = ["user" + "\t" + str(coords[0])]
    
    # skip comments
    for i2 in range(3):
        test_matrix_file.readline()
    
    cur_user = -1
    cur_cluster = []
    
    for line in test_matrix_file:
        user_id = int(line.split()[0]) - 1 + coords[0]
        item_id = int(line.split()[1]) - 1 + coords[1]
        
        if user_id != cur_user:     # next user
            #print "user_id = ", user_id
            cur_user = user_id
            if cur_cluster != []:
                clusters_list.append(cur_cluster)
            cur_cluster = ["user\t" + str(user_id)]
        time_bounds = getTimeInterval(item_id, item_X_time_list, coords)
        cur_cluster.append(str(time_bounds[0]) + "\t" + str(item_id) + "\t" + str(time_bounds[1]))
        
    test_clusters_file = open("test_clusters_" + str(DAYS_INTERVAL_PREPARE), 'w')
    test_clusters_file.write("low_bound item_id high_bound\n")
    for cluster in clusters_list:
        for line in cluster:
            test_clusters_file.write(line + "\n")
    
    test_clusters_file.close()
# ==  prepareTestClusters  ===========================================

def prepareTrainingMatrices(time_flag):
    """
        Function prepares training matrix for each case of cross-validation
        or time cross-validation - depending on flag. Matrix is saved
        as "history.mtx" in directory for each case.
    """
    
    if time_flag:
        """
            SPECIAL TIME CROSS-VALIDATION
        """
        os.chdir("../data/tmp/time_cross_validation")
        for i in range(ITERATIONS_NUMB):
            print "Iteration = ", i + 1, "/", ITERATIONS_NUMB
            
            # changing directory for current case
            cur_dir = str(i)
            os.chdir(cur_dir)

            # reading coords for current case
            coords = misc_functions.getWindowCoords()
            
            original_history_file = open("../../../well_done/history.mm")
            local_training_history_file = open("history.mtx", 'w')
            
            #skip comments
            for i2 in range(2):
                local_training_history_file.write(original_history_file.readline())
                
            # debugging stuff
            total_ctr = int(original_history_file.readline().split("\t")[2])
            
            # run through the whole history file
            ltw_list = []
            visits_ctr = 0
            zeros_ctr = 0
            for line in original_history_file:
                item = int(line.split("\t")[1]) - 1

                #print "item = ", item
                #step()
                if item < coords[1]:
                    ltw_list.append(line)
                    visits_ctr += 1
                    #print "A"
                else:
                    zeros_ctr += 1
                #step()
            
            local_training_history_file.write(str(USERS_NUMB) + " " + str(ITEMS_NUMB) + " " + str(visits_ctr) + "\n")
            for line in ltw_list:
                local_training_history_file.write(line)
            
            original_history_file.close()
            local_training_history_file.close()
            
            """ 
            # DEBUGGING STUFF
            print "total_ctr = ", total_ctr
            print "visits_ctr = ", visits_ctr
            print "zeros_ctr = ", zeros_ctr
            print "zeros_ctr + visits_ctr = ", zeros_ctr + visits_ctr
            print " -------------------------- "
            """
            if (zeros_ctr + visits_ctr != total_ctr):
                raise Exception("counters mismatch")
            
            os.chdir("..")
    else:
        """
            CLASSIC CROSS-VALIDATION
        """
    
        os.chdir("../data/tmp/cross_validation")
        # cycle for each case
        for i in range(SWITCHES_USERS_NUMB):
            for j in range(SWITCHES_ITEMS_NUMB):
                #print "window: user_window = ", i + 1, "/", SWITCHES_USERS_NUMB
                #print "        item_window = ", j + 1, "/", SWITCHES_ITEMS_NUMB
                print "cur work_dir = " + "<" + str(i) + "_" + str(j) + ">"
            
                # changing directory for current case
                cur_dir = str(i) + "_" + str(j)
                os.chdir(cur_dir)
                
                print "Writing local training matrix ..."
                now = datetime.datetime.now()
                now_string = now.strftime("%Y-%m-%d %H:%M")
            
                # reading coords for current case
                coords = misc_functions.getWindowCoords()

                original_history_file = open("../../../well_done/history.mm")
                local_training_history_file = open("history.mtx", 'w')
            
                #skip comments
                for i2 in range(2):
                    local_training_history_file.write(original_history_file.readline())
                
                # debugging stuff
                total_ctr = int(original_history_file.readline().split("\t")[2])
            
                # run through the whole history file
                ltw_list = []
                visits_ctr = 0
                zeros_ctr = 0
                for line in original_history_file:
                    item = int(line.split("\t")[1]) - 1
                    user = int(line.split("\t")[0]) - 1

                    #print "item = ", item
                    #step()
                    if ((item < coords[1]) or (item > coords[3])) or ((user < coords[0]) or (user > coords[2])):
                        ltw_list.append(line)
                        visits_ctr += 1
                        #print "A"
                    else:
                        zeros_ctr += 1
                    #step()
            
                local_training_history_file.write(str(USERS_NUMB) + " " + str(ITEMS_NUMB) + " " + str(visits_ctr) + "\n")
            
                for line in ltw_list:
                    local_training_history_file.write(line)
            
                original_history_file.close()
                local_training_history_file.close()
            
                """
                # DEBUGGING STUFF
                print "total_ctr = ", total_ctr
                print "visits_ctr = ", visits_ctr
                print "zeros_ctr = ", zeros_ctr
                print "zeros_ctr + visits_ctr = ", zeros_ctr + visits_ctr
                print " -------------------------- "
                """
                
                if (zeros_ctr + visits_ctr != total_ctr):
                    raise Exception("counters mismatch")
            
                os.chdir("..")
    
    os.chdir("../../../python_sources")

    print "TOTAL SUCCESS! \n Training local matrices are prepared!"
# ==  prepareTrainingMatrices2  =======================================



def prepareTestingMatrices(time_flag):
    """
        Function prepares testing matrix for each case of cross-validation
        or time cross-validation - depending on flag. Matrix is saved
        as "test.mtx" in directory for each case.
    """
    
    if time_flag:
        """
            SPECIAL TIME CROSS-VALIDATION
        """
        os.chdir("../data/tmp/time_cross_validation")

        for i in range(ITERATIONS_NUMB):
            print "Iteration = ", i + 1, "/", ITERATIONS_NUMB
            
            # changing directory for current case
            now = datetime.datetime.now()
            now_string = now.strftime("%Y-%m-%d %H:%M")
            
            cur_dir = str(i)
            os.chdir(cur_dir)
            
            # reading coords for current case
            coords = misc_functions.getWindowCoords()

            print "Reading history matrix ..."
            history_matrix = scipy.io.mmio.mmread("../../../well_done/history.mm")
            
            print "Saving test matrix..."
            if i != ITERATIONS_NUMB - 1:
                local_testing_matrix = (history_matrix.tocsr())[ : , coords[1] : coords[3] + 1].copy()
            else:
                local_testing_matrix = (history_matrix.tocsr())[ : , coords[1] : ].copy()
            scipy.io.mmio.mmwrite("test", local_testing_matrix, now_string, 'integer')
            
            os.chdir("..")
    else:
        """
            CLASSIC CROSS-VALIDATION
        """
        os.chdir("../data/tmp/cross_validation")
    
        # cycle for each case
        for i in range(SWITCHES_USERS_NUMB):
            for j in range(SWITCHES_ITEMS_NUMB):
                print "window: user_window = ", i + 1, "/", SWITCHES_USERS_NUMB
                print "        item_window = ", j + 1, "/", SWITCHES_ITEMS_NUMB

                # changing directory for current case
                cur_dir = str(i) + "_" + str(j)
                os.chdir(cur_dir)

                now = datetime.datetime.now()
                now_string = now.strftime("%Y-%m-%d %H:%M")

                # reading coords for current case
                coords = misc_functions.getWindowCoords()

                print "Reading history matrix ..."
                history_matrix = scipy.io.mmio.mmread("../../../well_done/history.mm")
            
                print "Saving test matrix..."
                local_testing_matrix = (history_matrix.tocsr())[coords[0] : coords[2] + 1, coords[1] : coords[3] + 1].copy()
                scipy.io.mmio.mmwrite("test", local_testing_matrix, now_string, 'integer')
            
                os.chdir("..")
    
    os.chdir("../../../python_sources")
    print "TOTAL SUCCESS! \n Local testing matrices and clusters are prepared!"
# == prepareTestingMatrices ==========================================

def prepareTestClusters(time_flag):
    
    if time_flag:
        """
            SPECIAL TIME CROSS-VALIDATION
        """
        os.chdir("../data/tmp/time_cross_validation")

        for i in range(ITERATIONS_NUMB):
            print "Iteration = ", i + 1, "/", ITERATIONS_NUMB
            cur_dir = str(i)
            os.chdir(cur_dir)
            
            print "Creating local testing clusters..."
            makeClusters()
            
            os.chdir("..")
    else:
        """
            CLASSIC CROSS-VALIDATION
        """
        os.chdir("../data/tmp/cross_validation")
    
        # cycle for each case
        for i in range(SWITCHES_USERS_NUMB):
            for j in range(SWITCHES_ITEMS_NUMB):
                print "window: user_window = ", i + 1, "/", SWITCHES_USERS_NUMB
                print "        item_window = ", j + 1, "/", SWITCHES_ITEMS_NUMB

                # changing directory for current case
                cur_dir = str(i) + "_" + str(j)
                os.chdir(cur_dir)
                
                print "Creating local testing clusters..."
                makeClusters()
                
                os.chdir("..")




def fullPrepares(time_flag):
    """
        Function consequentially launches all functions from module
        - thus preparing all the needs for running experiments.
    """

    print "                                *                                "
    print "                                                     *           "
    print "                           *         00                          "
    print "  *                             000000                           "
    print "           *                  0000000                            "
    print "                            0000000                              "
    print "                          00000000                          *    "
    print "           *             00000000             *                  "
    print "                        000000000                                "
    print "                 *      000000000                         *      "
    print "   *                    000000000                                "
    print "                         000000000           *                   "
    print "                           000000000                             "
    print "          *                   0000000                     *      "
    print "                         *       000000                          "
    print "                                     0000                        "
    print "           *                               *             *       "
    print "                                                                 "
    print "      *           *        *                                     "
    print "           *                           *                         "
    print "GOOD NIGHT!\n"

    # check if time_flag is correct
    if (time_flag != True) and (time_flag != False):
        raise Exception("Bad time_flag")

    # create directories for current setting for cross validation
    # prepareDirs(time_flag)
    # classic - done!
    # time - done!

    # create training history matrices for cross validation
    # prepareTrainingMatrices(time_flag)
    # classic - done!
    # time - done!
    
    # create user_X_meta matrices
    createUser_x_MetaMatrices(time_flag)
    # classic - done! 
    # time - done!

    # create item_X_meta matrix (global)
    # createItem_x_MetaMatrix_global()
    # common - done!

    
    # create item_X_item similarities (global)
    # createItem_x_ItemSimilarities(time_flag)
    # common

    # create test history matrices
    # prepareTestingMatrices(time_flag) 
    # classic - done!
    # time - done!
    
    # create test clusters
    # prepareTestClusters(time_flag) 
    # classic - done!
    # time - done!
    
    
    
