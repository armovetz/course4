import sys
import scipy
import numpy
import datetime
import scipy.io.mmio
import scipy.sparse
from scipy.sparse import *
from scipy.io.mmio import *
from numpy import *

"""This module uses output of graphchi SVD method.
It compute prediction matrix from V, S and U matrices that are
stored in files as [U|V].[0-9]+.mm and singular_values.mm

These files are to have <data_name> names.

Prediction matrix is computing using <singular_values_numb> singular
values. If <singular_values_numb> is larger than original number of 
singular values - then exception is raised.

It computes prediction matrix and cut it into square blocks
that are [block_size x block_size].

Results of work - <block_size> x <block_size> matrices that are finally
transmitted into sparsed coordinate Matrix Market format and are stored
in <output_location>

"""

# .INI parameters"
singular_values_numb = 6
data_name = "grapchi_output/users_went_mm"
output_location = "result_matrix_blocks/"
block_size = 1000

sigma = mmread(data_name + ".singular_values")
if sigma.shape[0] < singular_values_numb:
	raise Exception("<Singular_values_numb> is more then singular values in sigma matrice")

sigma = sigma[0:singular_values_numb]
sigma = numpy.diagflat(sigma)

for i in range(singular_values_numb):
	string_to_interpret = "u" + str(i) + " = mmread(\"" + data_name + ".U." + str(i) + "\")"
	exec(string_to_interpret)
	
for i in range(singular_values_numb):
	string_to_interpret = "u" + str(i) + " = mmread(\"" + data_name + ".U." + str(i) + "\")"
	exec(string_to_interpret)

u = mmread(data_name + ".U.0")
v = mmread(data_name + ".V.0")

for i in range(singular_values_numb - 1):
	string_to_interpret = "u" + str(i+1) + " = mmread(\"" + data_name + ".U." + str(i+1) + "\")"
	exec(string_to_interpret)
	
	string_to_interpret = "u = column_stack((u, u" + str(i + 1) + "))"
	exec(string_to_interpret)
	
	string_to_interpret = "v" + str(i+1) + " = mmread(\"" + data_name + ".V." + str(i+1) + "\")"
	exec(string_to_interpret)
	
	string_to_interpret = "v = column_stack((v, v" + str(i + 1) + "))"
	exec(string_to_interpret)

print "vectors pre-computing done!"

left_result = dot(u, sigma)
print "left_result pre-computing done!"
print "Computing result_matrix, this may take few minutes... \n PLEASE DON'T TOUCH ANYTHING!"
result = dot(left_result, v.transpose())
print "result_matrix computing done!"

row_numb = result.shape[0]
col_numb = result.shape[1]

print "starting writing matrix in blocks:"
for i in range(row_numb / block_size + 1):
	for j in range(col_numb / block_size + 1):
		#progress = float(i * row_numb + col_numb) / (row_numb * col_numb)
		#print "block [", i, "][", j, "] - ", int(progress * 100), "% done"
		
		result_file = open(output_location + "result_matrix." + str(i) + "_" + str(j) + ".mm", 'w')

		start_row = block_size * i
		start_col = block_size * j

		finish_row = block_size * (i + 1)
		if finish_row > row_numb:
			finish_row = row_numb

		finish_col = block_size * (j + 1)
		if finish_row > col_numb:
			finish_col = col_numb

		result_block = result[start_row : finish_row, start_col : finish_col]
#		print "    rounding block..."
		result_block = result_block.round()
		result_block = coo_matrix(result_block)
#		print "            ...done!"

		now = datetime.datetime.now()
		now_string = now.strftime("%Y-%m-%d %H:%M")
		
		# writing block to file in Matrix Market format
		mmwrite(target = result_file, a = result_block, comment = now_string, field = 'integer')
#		print "            ...done!"

		result_file.close()

print "SUCCESS!"
