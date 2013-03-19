import scipy
from scipy import *
import numpy
from numpy import *
import sys
import scipy.sparse
from scipy.sparse import *
import scipy.io.mmio
from scipy.io.mmio import *

def EstimateResult2(original_matrix, result_matrix):
	
	row_numb = original_matrix.shape[0]
	col_numb = original_matrix.shape[1]
	total_nnz = row_numb * col_numb
	
	error = sum(sum(abs(original_matrix - result_matrix)))
	#squared_error = sum(sum((original_matrix - result_matrix) ** 0.2))
	
	bool_original = original_matrix > 0
	bool_result= result_matrix > 0
	
	print result_matrix
	print sum(result_matrix)
	print sum(original_matrix)
	
	numb_true_positive = sum(multiply(bool_original, bool_result))
	print numb_true_positive
	numb_relevant = sum(original_matrix > 0)
	print numb_relevant
	numb_marked_relevant = sum(result_matrix > 0)
	print numb_marked_relevant
	
	mae = (float(error) / float(total_nnz))
#	rmse = (float(squared_error) / float(total_nnz)) ** 0.5
	recall = float(numb_true_positive) / float(numb_relevant)
	precision = float(numb_true_positive) / float(numb_marked_relevant)
	
	return [mae, recall, precision]


"""def EstimateResult():"""
"""Compute RMSE, recall and precision for matrices that are
	stored in <result_location> and <original_data_location> """

"""# .INI parameters"
	result_lzocation = "result_matrix_blocks/"
	original_data_location = "history_data/"
	block_size = 1000

	original_matrix = mmread(original_data_location + "users_went_mm").transpose()
	original_matrix = original_matrix.todense()
	

	row_numb = original_matrix.shape[0]
	col_numb = original_matrix.shape[1]
	
	numb_true_positive = 0
	numb_relevant = 0
	numb_marked_relevant = 0
	total_error = 0
	total_nnz = row_numb * col_numb

	print "starting writing matrix in blocks:"
	for i in range(row_numb / block_size + 1):
		for j in range(col_numb / block_size + 1):
			print "block [", i, "][", j, "]"
		
			start_row = block_size * i
			start_col = block_size * j

			finish_row = block_size * (i + 1)
			if finish_row > row_numb:
				finish_row = row_numb
	
			finish_col = block_size * (j + 1)
			if finish_row > col_numb:
				finish_col = col_numb

			original_block = original_matrix[start_row : finish_row, start_col : finish_col]
			result_block = mmread(result_location + "result_matrix." + str(i) + "_" + str(j) + ".mm").todense()
		
			prev_error = total_error
			total_error += sum(sum(abs(original_block - result_block)))
		
			bool_original_block = original_block > 0
			bool_result_block = result_block > 0
		
			numb_true_positive += sum(multiply(original_block > 0, result_block > 0))
			numb_relevant += sum(original_block > 0)
			numb_marked_relevant += sum(result_block > 0)

		
	mse = (float(total_error) / float(total_nnz))
	recall = float(numb_true_positive) / numb_relevant
	precision = float(numb_true_positive) / numb_marked_relevant
	
	return [mse, recall, precision]"""
