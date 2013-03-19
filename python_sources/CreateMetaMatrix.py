import scipy
from scipy import *
import numpy
from numpy import *
import sys
import scipy.sparse
from scipy.sparse import *
import scipy.io.mmio
from scipy.io.mmio import *

def CreateMetaMatrix(history_matrix, meta_list):
	""" This function reads history of visits from <history_file_name> file and
	metadata of seminars from <meta_file_name> file. It computes multiple 
	visits of seminars with current meta - for each user. And create 
	appropriate rectangle <meta_matrix_name> matrix.
	"""

	users_numb = history_matrix.shape[0]
	items_numb = history_matrix.shape[1]

	# creating new matrix
	meta_matrix = zeros((users_numb, 0), dtype = int)
	
	# some routine before main loop
	cur_meta_items = []
	cur_meta_id = 0

	# MAIN LOOP
	print "start of filling <meta_matrix>"
	#for line in meta_file:
	for line in meta_list:
		if line.split('\t')[meta_id_position] == "":
			line_meta_id = -1
		else:
			line_meta_id = int(line.split('\t')[meta_id_position])
		line_semin_id = int(line.split('\t')[semin_id_position])

		if line_meta_id != cur_meta_id:
			#print line_meta_id
			# new meta_id detected
			new_meta_col = zeros((users_numb, 1), dtype = int)
			for cur_item in cur_meta_items:
				cur_item_col = (history_matrix[:,cur_item - 1]).toarray()
				new_meta_col = new_meta_col + cur_item_col
			meta_matrix = numpy.hstack((meta_matrix, new_meta_col))

			# clean list if new meta_id begins
			cur_meta_items = []
			cur_meta_id = line_meta_id

		cur_meta_items.append(line_semin_id)	
	
	return meta_matrix

def sortMetaListByMeta(list, meta_id_position):
	
	def cmp(op1, op2):
		if op1.split('\t')[meta_id_position] == "":
			return -1
		if op2.split('\t')[meta_id_position] == "":
			return 1
		return int(op1.split('\t')[meta_id_position]) - int(op2.split('\t')[meta_id_position])

	return sorted(list, cmp)


###################################################################

######################## MAIN SCRIPT

###################################################################

""" 	select
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
		from theorycopy.seminars where is_published=1;
"""

print "HAVE YOU EVEN CHANGED #.INI PARAMETERS?\n LOOOOOL! CHECK IT OUT"

# .INI parameters
print ".INI parameters:"
semin_id_position = 0
print "semin_id_position = ", semin_id_position
meta_id_position = 3
print "meta_id_position = ", meta_id_position
meta_file_name = "../data/well_made/meta"
print "meta_file_name = ", meta_file_name
history_file_name = "../data/well_made/history.mm"
print "history_file_name = ", history_file_name
meta_matrix_file_name = "../data/well_made/users-places.mm"
print "meta_matrix_file_name = ", meta_matrix_file_name

# opening files
print "opening files..."
meta_file = open(meta_file_name, 'r')
history_file = open(history_file_name, 'r')
meta_matrix_file = open(meta_matrix_file_name, 'w')

# reading history matrix from file
print "reading history..."
history_matrix = mmread(history_file).tocsr()

meta_list = []
for line in meta_file:
	meta_list.append(line)
sorted_meta_list = sortMetaListByMeta(meta_list, meta_id_position)



meta_matrix = CreateMetaMatrix(history_matrix, sorted_meta_list)
meta_matrix_csr = csr_matrix(meta_matrix)

# writing new <meta_matrix> to file	
import datetime
print "writing new <meta_matrix> to file"
now = datetime.datetime.now()
now_string = now.strftime("%Y-%m-%d %H:%M")
mmwrite(meta_matrix_file, meta_matrix_csr, now_string, 'integer')

# closing files
print "closing files"
meta_file.close()
history_file.close()
meta_matrix_file.close()

print "TOTAL SUCCESS"
