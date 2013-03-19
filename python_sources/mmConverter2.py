import sys
import datetime

file_name = sys.argv[1]

input_file = open(file_name, 'r')

mm_file = open(file_name + "_mm", 'w')

lines_numb = 0
for line in input_file:
	lines_numb += 1
input_file.seek(0)

mm_file.write("%%MatrixMarket matrix coordinate integer general \n")
	
now = datetime.datetime.now()
now_string = now.strftime("%Y-%m-%d %H:%M")

mm_file.write("%Generated " + now_string + '\n')

for i in range(lines_numb):
	line = input_file.readline()
	mm_file.write(line.split()[0] + " " + line.split()[1] + " 1 \n")
	
input_file.close()
mm_file.close()

	
