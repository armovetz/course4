import time
from PIL import Image
import numpy
from numpy import *
import misc_functions
import sys

import scipy.io.mmio
from scipy.io.mmio import *

"""
CONST_HISTORY_MATRIX_FILENAME = "../data/well_done/history.mm.reserve"

BRIGHTNESS = 5

start = time.time() # beginning

print "reading hist_matrix..."
history_matrix = mmread(CONST_HISTORY_MATRIX_FILENAME).tocsr()
print "hist_matrix to array..."

#history_matrix = history_matrix.toarray()
timer_1 = time.time() # matrices are loaded
print "matrices are loaded in <", int(timer_1 - start),"> seconds"

picture_size = (400, 700)
width = picture_size[0]
height = picture_size[1]

picture = Image.new('RGB', picture_size)

# setting non-zero pixels
#for i in range(height):
for i in range(height):
    #misc_functions.step()
    print "i = ", i
    for j in range(width):
        #print "j = ", j
        #print "history_matrix[0, 0] = ", history_matrix[0, 0]
        pixel = history_matrix[i * 50 : i * 50 + 50, j * 50 : j * 50 + 50].toarray()
        #print "pixel = ", pixel
        col = int((255 * numpy.sum(numpy.sum(pixel))) / BRIGHTNESS)
        if col > 255:
            col = 255
        #print "col = ", col
        picture.putpixel((j,i), (col, col, col))

timer_2 = time.time() # picture is formed
print "picture is formed in <", int(timer_2 - timer_1),"> seconds"

picture.save("history_5.bmp")
print "picture saved"
print "TOTAL TIME = <", int(timer_2 - start),"> seconds"

"""

def drawVisitsMatrix(file_name):
    
    scale_rate = 50
    BRIGHTNESS = 5
    
    history_matrix = mmread(file_name).tocsr()

    height = history_matrix.shape[0] / scale_rate
    width  = history_matrix.shape[1] / scale_rate
    picture_size = (width, height)

    picture = Image.new('RGB', picture_size)

    # setting non-zero pixels
    for i in range(height):
        #misc_functions.step()
        #print "i = ", i
        for j in range(width):
            #print "j = ", j
            pixel = history_matrix[i * scale_rate : i * scale_rate + scale_rate, j * scale_rate : j * scale_rate + scale_rate].toarray()
            #print "pixel = ", pixel
            col = int((255 * numpy.sum(numpy.sum(pixel))) / BRIGHTNESS)
            if col > 255:
                col = 255
            #print "col = ", col
            picture.putpixel((j,i), (col, col, col))

    picture.save(file_name + ".bmp")
    print "picture saved"

drawVisitsMatrix(sys.argv[1])
