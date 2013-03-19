import scipy
import numpy
import datetime
import scipy.io.mmio
import scipy.sparse
from scipy.sparse import *
from scipy.io.mmio import *
from numpy import *

#original_matrix = mmread("users_went_mm").transpose()


u0 = mmread("users_went_mm.U.0")
u1 = mmread("users_went_mm.U.1")
u2 = mmread("users_went_mm.U.2")
u3 = mmread("users_went_mm.U.3")


v0 = mmread("users_went_mm.V.0")
v1 = mmread("users_went_mm.V.1")
v2 = mmread("users_went_mm.V.2")
v3 = mmread("users_went_mm.V.3")

sing_numb = 4

sigma = mmread("users_went_mm.singular_values")
sigma = sigma[0:sing_numb]
sigma = numpy.diagflat(sigma)

u = numpy.column_stack((u0, u1))
u = column_stack((u, u2))
u = column_stack((u, u3))

v = column_stack((v0, v1))
v = column_stack((v, v2))
v = column_stack((v, v3))

print "vectors pre-computing done!"

left_result = dot(u, sigma)
print "left_result pre-computing done!"
print "Computing result_matrix, this may take some... \n PLEASE DON'T TOUCH ANYTHING!"
result = dot(left_result, v.transpose())
print "result_matrix computing done!"

block_size = 1000
row_numb = result.shape[0]
col_numb = result.shape[1]

mse = 0

print "starting writing matrix in blocks:"
for i in range(row_numb / block_size + 1):
	for j in range(col_numb / block_size + 1):
		print "block [", i, "][", j, "]"
		
		result_file = open("result_matrix." + str(i) + "_" + str(j) + ".mm", 'w')

		start_row = block_size * i
		start_col = block_size * j

		finish_row = block_size * (i + 1)
		if finish_row > row_numb:
			finish_row = row_numb

		finish_col = block_size * (j + 1)
		if finish_row > col_numb:
			finish_col = col_numb

		result_block = result[start_row : finish_row, start_col : finish_col]
		print "    rounding block..."
		result_block = result_block.round()
		result_block = coo_matrix(result_block)
		print "            ...done!"

		now = datetime.datetime.now()
		now_string = now.strftime("%Y-%m-%d %H:%M")
		print "    writing block..."
		mmwrite(target = result_file, a = result_block, comment = now_string, field = 'integer')
		print "            ...done!"

		result_file.close()
