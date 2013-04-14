import os, subprocess
import datetime
import numpy
from numpy import *
#import SVD

import scipy.sparse
from scipy.sparse import *
import scipy.io.mmio
from scipy.io.mmio import *

import estimate
import ini
from ini import *

def launchCrossValidation(prediction_function, prediction_flag, time_flag, estimate_flag):
    """
        Function launches classic cross-validation or special time
        cross-validation - depending on time_flag. In each case of 
        cross-validation - experiments are launching using
        <prediction_function> as prediction engine.
        
        If <estimate_flag> is enforced - results are being estimated.
    """
    
    print "WARNING : CORRESPONDING MATRICES FOR EACH CASE MUST BE PREPARED!"
    
    if time_flag:
        """
            SPECIAL TIME CROSS-VALIDATION
        """
        os.chdir("../data/tmp/time_cross_validation")
        
        for i in range(ITERATIONS_NUMB):
            print "Iteration = ", i + 1, "/", ITERATIONS_NUMB
            
            cur_dir = str(i)
            os.chdir(cur_dir)
            
            # MAIN LAUNCH OF PREDICTION ENGINE INSIDE DIRECTORY
            # FOR CURRENT CASE OF CROSS-VALIDATION
            # works if prediction_flag is enforced
            if prediction_flag:
                print "Running prediction engine..."
                prediction_function()
                print "...done!"
                
            # ESTIMATE RESULT IF estimate_flag IS ENFORCED
            if estimate_flag:
                print "Estimating result..."
                estimate.estimateLocal()
                print "...done!"
                
            os.chdir("..")
    else:
        """
            CLASSIC CROSS-VALIDATION
        """
        os.chdir("../data/tmp/cross_validation")
    
        #timer_start = datetime.datetime.now()
    
        for i in range(SWITCHES_USERS_NUMB):
            for j in range(SWITCHES_ITEMS_NUMB):
                print "window: user_window = ", i + 1, "/", SWITCHES_USERS_NUMB , \
                "              item_window = ", j + 1, "/", SWITCHES_USERS_NUMB
                
                cur_dir = str(i) + "_" + str(j)
                os.chdir(cur_dir)            
                
                # MAIN LAUNCH OF PREDICTION ENGINE INSIDE DIRECTORY
                # FOR CURRENT CASE OF CROSS-VALIDATION
                # works if prediction_flag is enforced
                if prediction_flag:
                    print "Running prediction engine..."
                    prediction_function()
                    print "...done!"
                
                # ESTIMATE RESULT IF estimate_flag IS ENFORCED
                if estimate_flag:
                    print "Estimating result..."
                    estimate.estimateLocal()
                    print "...done!"
                
                os.chdir("..")

    #timer_stop = datetime.datetime.now()
    
    #print "TOTAL TIME = ", (finish - start).seconds, "secs"
    
    return 0
