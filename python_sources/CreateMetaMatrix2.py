import datetime
import scipy
from scipy import *
import numpy
from numpy import *
import sys
import scipy.sparse
from scipy.sparse import *
import scipy.io.mmio
from scipy.io.mmio import *

import misc_functions
import ini
from ini import *

"""
	0 - id
	1 - title
	2 - body
	3 - place_id
	4 - presenter_id
	5 - date
	6 - category_id
	7 - visit_conditions
	8 - price
	9 - organizer_id
	10 - publish_at
	11 - city_id
	12 - is_published
	13 - note
	14 - special_offer
	15 - seminar_type_id
	16 - featured
"""
semin_id_position = 0

# .INI
#metas_to_use = {3 : "place", 4 : "presenter", 6 : "category", 9 : "organizer", 11 : "city", 15 : "seminartype"}
metas_to_use = {6 : "categories", 11 : "cities", 15 : "seminar_types"}

def sortMetaListByMeta(list, meta_id_position):
    
    def cmp(op1, op2):
        if op1.split('\t')[meta_id_position] == "":
            return -1
        if op2.split('\t')[meta_id_position] == "":
            return 1
        return int(op1.split('\t')[meta_id_position]) - int(op2.split('\t')[meta_id_position])

    return sorted(list, cmp)

def CreateMetaMatrix(history_matrix, meta_list, meta_matrix_file_name, meta_id_position):
    """ 
    """
    
    meta_list = sortMetaListByMeta(meta_list, meta_id_position)

    # creating new matrix
    meta_matrix = zeros((USERS_NUMB, 0), dtype = int)
    
    # some routine before main loop
    cur_meta_items = []
    cur_meta_id = 1
    
    # MAIN LOOP
    for line in meta_list:
        
        if line.split('\t')[meta_id_position] == "":
            continue   # seminar with unknown meta is ignored

        line_meta_id = int(line.split('\t')[meta_id_position])
        line_semin_id = int(line[0]) # considering everywhere semin_id_position == 0

        if line_meta_id != cur_meta_id: # new meta_id detected
            new_meta_col = zeros((users_numb, 1), dtype = int)
            
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
            print "meta_id = ", cur_meta_id, "; visiters = ", len(cur_meta_items)
            cur_meta_items = []
            cur_meta_id += 1

        cur_meta_items.append(line_semin_id)    
        
    meta_matrix_csr = csr_matrix(meta_matrix)
    
    # writing new <meta_matrix> to file    
    now = datetime.datetime.now()
    now_string = now.strftime("%Y-%m-%d %H:%M")
    #meta_matrix_file = open("meta_matrix_file_name", 'w')
    mmwrite(meta_matrix_file_name, meta_matrix_csr, now_string, 'integer')
    #meta_matrix_file.close()

    return 0

def createUser_x_MetaMatrices(meta_file_name):
    """ """

    print "STARTED computing User_x_Meta matrices"
    #history_file = open(history_file_name, 'r')
    history_matrix = mmread("history.mtx").tocsr()
    #history_file.close()
    
    meta_file = open(meta_file_name, 'r')
    meta_list = []
    for line in meta_file:
        meta_list.append(line)
    meta_file.close()

    for meta_id in metas_to_use:
        print "Computing meta matrix for ", metas_to_use[meta_id]
        meta_matrix_name = "users-" + metas_to_use[meta_id]
        CreateMetaMatrix(history_matrix, meta_list, meta_matrix_name, meta_id)











def prepareUser_x_MetaMatrices():
   
#    """ Function prepares several training matrices, 
#        and corresponding meta matrices for them """

    os.chdir("../data/tmp/cross_validation")
    
    # delete previous old prepared matrices
    subprocess.call(["rm", "-rf", "./*"])
    
    for i in range(SWITCHES_USERS_NUMB):
        for j in range(SWITCHES_ITEMS_NUMB):
            
            print "window: user_window = ", i + 1, "/", SWITCHES_USERS_NUMB
            print "        item_window = ", j + 1, "/", SWITCHES_ITEMS_NUMB
    
            # defining boundaries for blank 'window'
            start_zero_user = WINDOW_USERS_SIZE * i
            start_zero_item = WINDOW_ITEMS_SIZE * j
            stop_zero_user = start_zero_user + WINDOW_USERS_SIZE
            stop_zero_item = start_zero_user + WINDOW_ITEMS_SIZE
            if stop_zero_item > ITEMS_NUMB:
                stop_zero_item = ITEMS_NUMB
            if stop_zero_user > USERS_NUMB:
                stop_zero_user = USERS_NUMB

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

            print "Reading history matrix ..."
            history_matrix = scipy.io.mmio.mmread("../../well_done/history.mm")
            print "...done!"
            print "Converting sparse history_matrix to numpy array ..."
            local_training_matrix = history_matrix.toarray()
            print "...done!"
            print "Creating 'empty' testing window..."
            local_training_matrix[start_zero_user : stop_zero_user, start_zero_item : stop_zero_item] = 0
            print "...done!"
            csr_local_training_matrix = csr_matrix(local_training_matrix)
            del local_training_matrix
            
            print "Writing local training matrix ..."
            now = datetime.datetime.now()
            now_string = now.strftime("%Y-%m-%d %H:%M")
            scipy.io.mmio.mmwrite("history", csr_local_training_matrix, now_string, 'integer')
            print "...done!"
            
            CreateMetaMatrix2.createMetaMatrices("history.mtx", "../../../well_done/meta")

            
            os.chdir("..")

    print "TOTAL SUCCESS! users-metas local matrices are prepared."
