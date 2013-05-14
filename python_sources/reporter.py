import datetime
import misc_functions
import ini
from ini import *

"""
def reporter(prediction_function, prediction_flag, prediction_file_name, estimate_function, estimate_flag, results_file_name, time_flag):
    # getting time
    now = datetime.datetime.now()
    now_string = now.strftime("%Y-%m-%d %H:%M")

    # creating file
    results_file = open("session_" + now_string, 'w')

    results_file.write("SESSION STARTED AT:   " + str(now_string) + '\n')
    results_file.write("\n  ========================  \n\n")
    
    results_file.write("time_flag = " + str(time_flag) + '\n')
    results_file.write("prediction_flag = " + str(prediction_flag) + '\n')
    results_file.write("estimate_flag = " + str(estimate_flag) + '\n')
    
    results_file.write("\n  ========================  \n\n")
    
    results_file.write("prediction_file_name = " + prediction_file_name + '\n')
    results_file.write("results_file_name = " + results_file_name + '\n')
    
    results_file.write("\n  == parameters for clusters  ==========  \n\n")
    results_file.write("DAYS_INTERVAL_PREPARE = " + str(DAYS_INTERVAL_PREPARE) + '\n')
    results_file.write("DAYS_INTERVAL_EXE = " + str(DAYS_INTERVAL_EXE) + '\n')
    
    
    results_file.write("\n  == parameters for engine  ==========  \n\n")
    results_file.write("METAS_TO_USE = " + str(METAS_TO_USE.values()) + '\n')
    results_file.write("META_WEIGHTS = " + str(META_WEIGHTS.view()) + '\n')
    
    results_file.write("\n\n\n == computed nDCGps for cases ====== \n\n")
    
    return results_file

"""
    
def reporter(session_comment):
    launch_file = open("lol.py", 'r')

    # getting time
    now = datetime.datetime.now()
    now_string = now.strftime("%Y-%m-%d__%H:%M")

    ltw = "SESSION STARTED AT:    " + now_string
    ltw = ltw + "\n\nLAUNCH FILE  ========================= \n\n"

    line = launch_file.readline()
    while not ("REPORT BEGIN" in line):
        line = launch_file.readline()
    
    line = launch_file.readline()
    
    while not ("REPORT END" in line):
        ltw = ltw + line
        line = launch_file.readline()

    """
    for line1 in launch_file:
        if "REPORT BEGIN" in line1:
            for line2 in launch_file:
                if "REPORT END" in line2:
                    break
                ltw = ltw + line1
        break
    """
    launch_file.close()
    
    ini_file = open("ini.py", 'r')
    
    ltw = ltw + "\n\nINI FILE  ========================= \n\n"
    line = ini_file.readline()
    while not ("REPORT BEGIN" in line):
        line = ini_file.readline()
    
    line = ini_file.readline()
    
    while not ("REPORT END" in line):
        ltw = ltw + line
        line = ini_file.readline()
    
    ini_file.close()
    
    # creating file
    results_file_name = "session_" + now_string + "_" + session_comment
    results_file = open(results_file_name, 'w')
    results_file.write(ltw)
    #results_file.close()
    
    return results_file
