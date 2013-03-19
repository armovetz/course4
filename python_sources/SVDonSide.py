# .INI

import numpy
from numpy import *
import scipy
import scipy.io.mmio
from scipy.io.mmio import *

import datetime



#users_places_file = open("../data/well_made/users-places.mm", 'r')
users_categories_file = open("../data/well_made/users-categories.mm", 'r')
users_semtypes_file = open("../data/well_made/users-seminar_type_ids.mm", 'r')

meta_numbs = 17
meta_weights = array([[0, 0, 0, 0, 0, 0, 0.7, 0, 0, 0, 0, 0, 0, 0, 0, 0.3, 0]], dtype = float)

#users_places_matrix = mmread(users_places_file).toarray()
users_categories_matrix = mmread(users_categories_file).toarray()
users_semtypes_matrix = mmread(users_semtypes_file).toarray()

seminars_meta_list = []
for line in open("../data/well_made/meta"):
	seminars_meta_list.append(line.split('\t'))


def computeSingleRating(user_id, seminar_id):
	attr_positions_list = [6, 15]
	
	#user_hist_vector = history_matrix[user_id, :]
	
#	user_places_vector = users_places_matrix[user_id]
	user_categories_vector = users_categories_matrix[user_id]
	user_semtypes_vector = users_semtypes_matrix[user_id]
	
	# normalizing vectors
#	usr_plcs_weights = (1.0 * user_places_vector) / user_places_vector.amax()
	usr_cat_weights = (1.0 * user_categories_vector) / max(user_categories_vector)
	usr_semtypes_weights = (1.0 * user_semtypes_vector) / max(user_semtypes_vector)
	
	user_meta_vectors_list = [0, 0, 0, 0, 0, 0, usr_cat_weights, 0, 0, 0, 0, 0, 0, 0, 0, usr_semtypes_weights]
	seminar_meta_vector = seminars_meta_list[seminar_id]

	meta_values = zeros((1,17), dtype = float)

	for attr_position in attr_positions_list:
		seminar_meta_value = int(seminar_meta_vector[attr_position])
		#print seminar_meta_value
		#print attr_position
		#print meta_values
		#print user_meta_vectors_list
		#vect = user_meta_vectors_list[attr_position]
		#print "vect = ", vect
		#print "vect[seminar_meta_value] =", vect[seminar_meta_value]
		#print "meta_values =", meta_values
		#print "meta_values[attr_position] = ", meta_values[:, attr_position]
		#meta_values[attr_position] = vect[seminar_meta_value]
		#return 0
		
		meta_values[:, attr_position] = (user_meta_vectors_list[attr_position])[seminar_meta_value - 1]
	return sum(meta_values * meta_weights)


