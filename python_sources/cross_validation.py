import os, subprocess
import datetime
import numpy
from numpy import *


import scipy.sparse
from scipy.sparse import *
import scipy.io.mmio
from scipy.io.mmio import *

import misc_functions
import estimate
import ini
from ini import *

def launchCrossValidation(prediction_function, prediction_flag, prediction_file_name, \
    estimate_function, estimate_flag, results_file_name, time_flag, report_file):
    """
        Function launches classic cross-validation or special time
        cross-validation - depending on time_flag. In each case of 
        cross-validation - experiments are launching using
        <prediction_function> as prediction engine.
        
        If <estimate_flag> is enforced - results are being estimated.
    """
    
    if prediction_flag:
        print "prediction:  ON"
    else:
        print "prediction:  OFF"
    
    if estimate_flag:
        print "estimate:    ON"
    else:
        print "estimate:    OFF"
        
    if time_flag:
        print "time_flag:   ON"
        print "dir = time_cross_validation"
    else:
        print "time_flag:   OFF"
        print "dir = cross_validation"
    
    timer_start = datetime.datetime.now()
    
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
            
            clusters_list = misc_functions.getClustersListFromClustersFile(DAYS_INTERVAL_EXE)
            
            # MAIN LAUNCH OF PREDICTION ENGINE INSIDE DIRECTORY
            # FOR CURRENT CASE OF CROSS-VALIDATION
            # works if prediction_flag is enforced
            if prediction_flag:
                prediction_function(prediction_file_name, clusters_list)
                
            # ESTIMATE RESULT IF estimate_flag IS ENFORCED
            if estimate_flag:
                loc_ndcgp = estimate_function(prediction_file_name, results_file_name, clusters_list)
                report_file.write(cur_dir + " = " + str(loc_ndcgp) + '\n')
                
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
                
                clusters_list = misc_functions.getClustersListFromClustersFile(DAYS_INTERVAL_EXE)
                
                # MAIN LAUNCH OF PREDICTION ENGINE INSIDE DIRECTORY
                # FOR CURRENT CASE OF CROSS-VALIDATION
                # works if prediction_flag is enforced
                if prediction_flag:
                    prediction_function(prediction_file_name, clusters_list)
                
                # ESTIMATE RESULT IF estimate_flag IS ENFORCED
                if estimate_flag:
                    estimate_function(prediction_file_name, results_file_name, clusters_list)
                    report_file.write(cur_dir + " = " + str(loc_ndcgp) + '\n')
                
                os.chdir("..")

    os.chdir("../../../python_sources")
    timer_stop = datetime.datetime.now()
    print "TOTAL TIME = ", (timer_stop - timer_start).seconds, "secs"
    report_file.write("TOTAL TIME = " + str((timer_stop - timer_start).seconds) + "secs \n")
    report_file.close()
    
    return 0


def launchCase(prediction_function, prediction_flag, time_flag, estimate_flag, \
    prediction_file_name, results_file_name, directory):
        
    timer_start = datetime.datetime.now()
        
    if time_flag:
        """
            SPECIAL TIME CROSS-VALIDATION
        """
        os.chdir("../data/tmp/time_cross_validation")
        os.chdir(directory)
        
        clusters_list = misc_functions.getClustersListFromClustersFile()
            
        # MAIN LAUNCH OF PREDICTION ENGINE INSIDE DIRECTORY
        # FOR CURRENT CASE OF CROSS-VALIDATION
        # works if prediction_flag is enforced
        if prediction_flag:
            print "Running prediction engine..."
            prediction_function(prediction_file_name, clusters_list)
                
        # ESTIMATE RESULT IF estimate_flag IS ENFORCED
        if estimate_flag:
            print "Estimating result..."
            estimate_function(prediction_file_name, results_file_name)
        
    else:
        """
            CLASSIC CROSS-VALIDATION
        """
        os.chdir("../data/tmp/cross_validation")
        os.chdir(directory)
        
        clusters_list = misc_functions.getClustersListFromClustersFile()

        # MAIN LAUNCH OF PREDICTION ENGINE INSIDE DIRECTORY
        # FOR CURRENT CASE OF CROSS-VALIDATION
        # works if prediction_flag is enforced
        if prediction_flag:
            print "Running prediction engine..."
            prediction_function(prediction_file_name, clusters_list)
        
        # ESTIMATE RESULT IF estimate_flag IS ENFORCED
        if estimate_flag:
            print "Estimating result..."
            estimate.estimateLocal(prediction_file_name, results_file_name)
            
    timer_stop = datetime.datetime.now()
    print "case done in <", (timer_stop - timer_start).seconds, "> secs"
        
    os.chdir("../../../../python_sources")

def launchDebugCase(prediction_function, prediction_flag, prediction_file_name, \
    estimate_function, estimate_flag, results_file_name, directory):

    timer_start = datetime.datetime.now()

    os.chdir(directory)

    clusters_list = misc_functions.getClustersListFromClustersFile()

    # MAIN LAUNCH OF PREDICTION ENGINE INSIDE DIRECTORY
    # FOR CURRENT CASE OF CROSS-VALIDATION
    # works if prediction_flag is enforced
    if prediction_flag:
        print "Running prediction engine..."
        prediction_function(prediction_file_name, clusters_list)

    # ESTIMATE RESULT IF estimate_flag IS ENFORCED
    if estimate_flag:
        print "Estimating result..."
        estimate_function(prediction_file_name, results_file_name)

    os.chdir("../../../../python_sources")
