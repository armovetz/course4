import scipy
from scipy import *
import numpy
from numpy import *
import sys
import scipy.sparse
from scipy.sparse import *
import scipy.io.mmio
from scipy.io.mmio import *

""" This script 

"""

# .INI parameters
semin_id_position = 0
topic_id_position = 0
meta_file_name = "history_data/topics"
history_file_name = "history_data/users_went_mm"
topic_matrix_file_name = "topic_matrix"

# opening files
meta_file = open(meta_file_name, 'r')
history_file = open(history_file_name, 'r')
topic_matrix_file = open(topic_matrix_file_name, 'w')

# reading history matrix from file
history_matrix = mmread(history_file).tocsr()
users_numb = history_matrix.shape[0]
items_numb = history_matrix.shape[1]

# creating new matrix
topic_matrix = zeros((users_numb, 0), dtype = int)

# some routine before main loop
cur_topic_items = []
cur_topic = 0

# MAIN LOOP
for line in meta_file:
	
	line_topic_id = line.split()[topic_id_position]
	line_semin_id = line.split()[semin_id_position]
	
	# new topic_id detected
	if line_topic_id != cur_topic:
		new_topic_col = zeros((users_numb, 0), dtype = int)
		for cur_item in cur_topic_items:
			cur_item_col = history_matrix[:,cur_item].toarray()
			new_topic_col = new_topic_col + cur_item_col
		topic_matrix = hstack((topic_matrix, new_topic_col))
		
	# clean list if new topic begins
	cur_topic_items = []
	cur_topic = line_topic_id
		
	cur_topic_items.append(line_semin_id)	
	
# writing new <topic_matrix> to file	
now = datetime.datetime.now()
now_string = now.strftime("%Y-%m-%d %H:%M")
mmwrite(topic_matrix_file, topic_matrix, comment = now_string, 'integer')

# closing files
meta_file.close()
history_file.close()
topic_matrix_file.close()

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

meta_to_compute = [3, 4, 6, 9, 11, 15]
    
def createTopicMatrix():
    """ creates matrices concerning attendance of seminars with 
        certain meta data """
    
    
    
