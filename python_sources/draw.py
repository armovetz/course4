import time
from PIL import Image

import scipy.io.mmio
from scipy.io.mmio import *

CONST_HISTORY_MATRIX_FILENAME = "../data/well_done/history.mm"

start = time.time() # beginning

print "reading hist_matrix..."
history_matrix = mmread(CONST_HISTORY_MATRIX_FILENAME)
print "hist_matrix to array..."

history_matrix = history_matrix.toarray()
timer_1 = time.time() # matrices are loaded
print "matrices are loaded in <", int(timer_1 - start),"> seconds"
users_numb = history_matrix.shape[0]
items_numb = history_matrix.shape[1]
print "users_numb = ", users_numb
print "items_numb = ", items_numb


#CONST_PICTURE_SIZE = (3500, 2100)
#width = CONST_PICTURE_SIZE[0]
#height = CONST_PICTURE_SIZE[1]

#height = users_numb
#width = items_numb
height = 5000
width = 5000
picture_size = (width, height)

picture = Image.new('RGB', picture_size)

# setting non-zero pixels
#for i in range(height):
for i in range(height):
#    print "i = ", i
    for j in range(width):
        #print "j = ", j
        if history_matrix[i][j] != 0:
            #print "YES"
            picture.putpixel((j,i), (255,255,255))

timer_2 = time.time() # picture is formed
print "picture is formed in <", int(timer_2 - timer_1),"> seconds"

picture.save("5000x5000.bmp")
print "picture saved"
print "TOTAL TIME = <", int(timer_2 - start),"> seconds"

