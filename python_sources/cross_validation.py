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

import svd

def launchCrossValidation(prediction_function, prediction_flag, prediction_file_name, \
    estimate_function, estimate_flag, results_file_name, \
    svd_prepare_flag, svd_use_flag, svd_sing_vector_numb, \
    report_file):
    """
        Function launches classic cross-validation or special time
        cross-validation - depending on time_flag. In each case of 
        cross-validation - experiments are launching using
        <prediction_function> as prediction engine.
        
        If <estimate_flag> is enforced - results are being estimated.
    """
    
    print "prediction: ", prediction_flag
    print "estimate: ", estimate_flag
    
    timer_start = datetime.datetime.now()
    
    print "WARNING : CORRESPONDING MATRICES FOR EACH CASE MUST BE PREPARED!"
    
    os.chdir("../data/tmp/time_cross_validation")
    
    mean_ndcgp = 0.0
    mean_p = 0.0
    mean_position = 0.0
        
    for i in range(ITERATIONS_NUMB):
        print "Iteration = ", i + 1, "/", ITERATIONS_NUMB
            
        cur_dir = str(i)
        os.chdir(cur_dir)
        
        clusters_list = misc_functions.getClustersListFromClustersFile(DAYS_INTERVAL_EXE)
        
        # IMPLEMENT SVD TO AGREGATED USERS_X_METAS MATRICES
        # works if svd_prepare_flag is enforced
        if svd_prepare_flag:
            for meta in METAS_TO_USE:
                svd.svdForAgregated(meta, svd_sing_vector_numb)
        
        # MAIN LAUNCH OF PREDICTION ENGINE INSIDE DIRECTORY
        # FOR CURRENT CASE OF CROSS-VALIDATION
        # works if prediction_flag is enforced
        if prediction_flag:
            prediction_function(prediction_file_name, clusters_list, svd_use_flag)
        
        # ESTIMATE RESULT IF estimate_flag IS ENFORCED
        if estimate_flag:
            loc = estimate_function(prediction_file_name, results_file_name, clusters_list)
            #report_file = open(report_file_name, 'a')
            report_file.write("ncgp" + " = " + str(loc[0]) + '\n')
            report_file.write("local_p" + " = " + str(loc[1]) + '\n')
            report_file.write("position" + " = " + str(loc[2]) + '\n')
            
            mean_ndcgp += loc[0]
            mean_p += loc[1]
            mean_position += loc[2]
            #report_file.close()
        
        os.chdir("..")
    
    
    
    if estimate_flag:
        mean_ndcgp /= ITERATIONS_NUMB
        mean_p /= ITERATIONS_NUMB
        mean_position /= ITERATIONS_NUMB
    
        report_file.write("\n MEANS ============= \n")
        report_file.write("\n mean_ndcgp = " + str(mean_ndcgp) + '\n')
        report_file.write("\n mean_p = " + str(mean_p) + '\n')
        report_file.write("\n mean_position = " + str(mean_position) + '\n')
        
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
