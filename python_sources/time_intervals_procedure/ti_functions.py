import os
import scipy.io.mmio
import scipy.sparse

import sys
if ".." not in sys.path:
    sys.path.insert(0, "..")
import misc_functions

if "../dataset" not in sys.path:
    sys.path.insert(0, "../dataset")
import dataset

import copy
import datetime
import subprocess
import ConfigParser

#
TI_TRUNK_DIR = os.path.abspath("../..")
TI_DATASET_DIR = TI_TRUNK_DIR + "/data/datasets"
TI_RESULT_DIR = TI_TRUNK_DIR + "/data/time_intervals"

#

class TI_Fabric:
    """
        class to realise creating of TIs (time intervals) for
        different datasets
    """

    def __init__(self, conf_file_name):
        """
            reads settings of TI from conf gile and sets the object
        """
        parser = ConfigParser.ConfigParser()
        parser.read("ti.conf")
        
        # PATHS
        if parser.get("PATHS", "case_dir") == "":
            # if empty <case_dir> string - use current time to name it
            self.case_dir = datetime.datetime.now().strftime("%Y-%m-%d__%H:%M")
        else:
            self.case_dir = parser.get("PATHS", "case_dir")
        
        # DATASET
        self.dataset = dataset.Dataset(TI_DATASET_DIR + "/" + parser.get("DATASET", "dataset_name"))
        
        # BORDERS_SETTINGS
        #borders_settings = settings.items("BORDERS_SETTINGS")
        self.interval_size = int( parser.get("BORDERS_SETTINGS", "interval_size") )
        if parser.get("BORDERS_SETTINGS", "full_length_on") == "False":
            self.full_length_on = False
            self.item_x_user_coef = int( parser.get("BORDERS_SETTINGS", "item_x_user_coef") )
        else:
            self.full_length_on = True
            self.item_x_user_coef = 0
        
        if parser.get("BORDERS_SETTINGS", "manual_borders") == "False":
            self.manual_borders_on = False
        else:
            self.manual_borders_on = True
            self.borders_file_name = parser.get("BORDERS_SETTINGS", "borders_file_name")
        
        if parser.get("BORDERS_SETTINGS", "comment") != "0":
            self.comment = parser.get("BORDERS_SETTINGS", "comment")
        else:
            self.comment = 0

    # end of TI_Fabric.__init__

    def ti_PrintHeaderInfo(self):
        
        print "------------------------"
        print "HELLO WORLD!\n"
        
        print "TIME: ", datetime.datetime.now().strftime("%Y-%m-%d__%H:%M")
        
        if self.comment != 0:
            print "Comment attached:\n", self.comment
        
        print "\n"
        print "Parameters: "
        print "time_interval = ",       self.interval_size
        print "manual_borders_on = ",   self.manual_borders_on
        if self.manual_borders_on :
            print "borders_file_name = ", self.borders_file_name
        print "full-length_on= ",         self.full_length_on
        print "case_dir_name = ",         self.case_dir
        #print "time_interval = ",       INI_time_interval
        print "-------------------------"
        
    # end of ti_PrintHeaderInfo
        
    def ti_PrintTailInfo(self):
        
    #    if error_code != 0 :
    #        print "TIME INTERVAL PREPARING PROCEDURE FAILED!"
    #        print "ti FAIL"
    #        print "EXCEPTION:"
    #        print exception_text
    #    else:
        
        print "TIME INTERVAL PREPARING PROCEDURE PASSED."
        print "ti OK"
        
        print "----------------"
        print "END OF LOG"
    # end of ti_PrintTailInfo
    
    def ti_PrintBorders(self):
        """
            prints info about every window in <borders>
        """
        
        print "BORDERS:"
        
        j = 0
        
        for window_coord in self.borders:
            print "---"
            print "Window #", j
            print "users : [", window_coord[0], ",", window_coord[1], "]"
            print "events : [", window_coord[2], ",", window_coord[3], "]"
            j += 1
        
        print "-------------------------"
    # end of ti_PrintBorders
    
    def ti_CreateDirs(self):
        """
            launchs shell script to make directories and write info
            about windows' borders into files inside created directories
        """
        
        ti_path = TI_RESULT_DIR + "/" + self.case_dir
        
        j = 0
        
        # create list of created dirs
        self.ti_dirs = []
        
        for window_coords in self.borders:
            
            window_dir = str(j) + \
            "_USERS" + str(window_coords[0]) + "x" + str(window_coords[1]) + \
            "_ITEMS" + str(window_coords[2]) + "x" + str(window_coords[3])
            
            subprocess.call(["mkdir", "-p", ti_path + "/" + window_dir])
            self.ti_dirs.append(ti_path + "/" + window_dir)
            
            coords_file = open(ti_path + "/" + window_dir + "/window_coords", 'w')
            coords_file.write("start_user = " + str(window_coords[0]) + "\n")
            coords_file.write("stop_user = "  + str(window_coords[1]) + "\n")
            coords_file.write("start_item = " + str(window_coords[2]) + "\n")
            coords_file.write("stop_item = "  + str(window_coords[3]) + "\n")
            coords_file.close()
            j += 1
    # enf of ti_CreateDirs
    
    def ti_SplitEventsByInterval(self, events):
        """
            gets list of sorted events lines
            returns borders for blocks of events - each block to have
            <INI_time_interval> size
        """
        
        interval_dtime = datetime.timedelta(self.interval_size, 0, 0)
        
        # result to return
        borders = []
        
        # set beginning of the first block
        block = [0, self.dataset.users_numb]
        block.append( int( events[0].split('\t')[0] )) 
        block_head_time_str = (events[0].split('\t')[self.dataset.time_meta_position])
        block_head_dtime = datetime.datetime.strptime(block_head_time_str, "%Y-%m-%d %H:%M:%S")
        
        for event in events:
            event_time_str = event.split('\t')[self.dataset.time_meta_position]
            event_dtime = datetime.datetime.strptime(event_time_str, "%Y-%m-%d %H:%M:%S")
            
            # if new event is older than block_head event more than <interval_dtime>
            # then emit block and start new block
            if event_dtime >= (block_head_dtime + interval_dtime):
                block.append(int(event.split('\t')[0]) - 1)
                borders.append(block)
                block = [0, self.dataset.users_numb]
                block.append( int( event.split('\t')[0] ) )
                block_head_time_str = (event.split('\t')[self.dataset.time_meta_position])
                block_head_dtime = datetime.datetime.strptime(block_head_time_str, "%Y-%m-%d %H:%M:%S")
        
        # emit the last block - with last event
        block.append(self.dataset.events_numb - 1)
        borders.append(block)
        
        print borders
        return borders
    # end of ti_SplitEventsByInterval
    
    def ti_GenerateBorders(self):
        """
            reads parameters of borders,
            gets list of seminars from data files,
            returns borders
        """
        
        events_file = open(self.dataset.events_file_name, 'r')
        
        # TBD: realise special format for events meta file
        # skip first info lines
        # for i in range(2):
        #    events_file.readline()
        
        events_list = []
        
        for event_line in events_file:
            events_list.append(event_line)
        events_file.close()
    
        self.borders = self.ti_SplitEventsByInterval(events_list)
    # enf of ti_GenerateBorders
    
    def ti_ReadBordersManually(self):
        """
            reads borders manually from file
            generate warning if windows are 
        """
        
        borders_file = open(self.borders_file_name)
        
        self.borders = []
        
        for line in borders_file:
            window_coords = map(int,line.split())
            if len(window_coords) != 4 :      # raise exception - one line must correspond to one window
                raise(Exception("Bad windows coords in string: " + line))
            
            self.borders.append(window_coords)
        
        borders_file.close()
    # end of ti_ReadBordersManually
    
    def ti_CheckIntersections(self):
        """
            throws a WARNING message if some windows in <borders> are
            intersected (in both users or seminars)
        """
        
        intersected_windows = []
        
        for window_coords in self.borders:
            borders_clone = copy.deepcopy(self.borders)
            borders_clone.remove(window_coords)
            
            if window_coords in borders_clone :    # every borders list must not repeat
                raise(Exception("Repeated window is forbidden in declaration of borders:" + str(window_coords)))
            
            for cmp_window_coords in borders_clone:
                user_intersect = set(range(cmp_window_coords[0], cmp_window_coords[1] + 1)) & set(range(window_coords[0], window_coords[1] + 1))
                item_intersect = set(range(cmp_window_coords[2], cmp_window_coords[3] + 1)) & set(range(window_coords[2], window_coords[3] + 1))
                
                if self.full_length_on:
                    if len(item_intersect) != 0:
                        print "!!!"
                        intersected_windows.append([window_coords, cmp_window_coords])
                else:
                    if (len(user_intersect) != 0) or (len(item_intersect) != 0)  :
                        print "!!!"
                        intersected_windows.append([window_coords, cmp_window_coords])
        
        return intersected_windows
    # end of ti_CheckIntersections
    
    def ti_CreateTestingMatrices(self):
        """
            creates testing matrices for each window that has been
            created while preparing time intervals
        """
        
        for window_dir in self.ti_dirs:
            now = datetime.datetime.now()
            now_string = now.strftime("%Y-%m-%d %H:%M")
            
            coords = misc_functions.getWindowCoords(window_dir)
            
            # Reading history matrix
            history_matrix = scipy.io.mmio.mmread(self.dataset.history_file_name)
            
            # selecting part for the current window
            local_testing_matrix = (history_matrix.tocsr())[ coords[0] : coords[1] + 1, coords[2] : coords[3] + 1].copy()
            scipy.io.mmio.mmwrite(window_dir + "/test", local_testing_matrix, now_string, 'integer')
    
    # end of ti_CreateTestingMatrices
    
    def ti_CreateTrainingMatrices(self):
        """
            creates training matrices for each window that has been
            created while preparing time intervals
        """
        
        for window_dir in self.ti_dirs:
            # reading coords for current case
            coords = misc_functions.getWindowCoords(window_dir)
            
            original_history_file = open(self.dataset.history_file_name)
            local_training_history_file = open(window_dir + "/train", 'w')
            
            #skip comments and copy some of them
            local_training_history_file.write(original_history_file.readline())
            original_history_file.readline()
            original_history_file.readline()
            now = datetime.datetime.now()
            now_string = now.strftime("%Y-%m-%d %H:%M")
            local_training_history_file.write("%Generated " + now_string + "\n")
                
            # run through the whole history file
            ltw_list = [] #lines_to_write_list
            visits_ctr = 0
            zeros_ctr = 0
            for line in original_history_file:
                event_id = int(line.split("\t")[1]) - 1

                if event_id < coords[1]:
                    ltw_list.append(line)
                    visits_ctr += 1
                else:
                    zeros_ctr += 1
            
            # write properties of the training matrix
            train_users_numb = coords[1] - coords[0] + 1
            train_events_numb = coords[3] - coords[2] + 1
            local_training_history_file.write(str(train_users_numb) + \
                " " + str(train_events_numb) + " " + str(visits_ctr) + "\n")
            
            for line in ltw_list:
                local_training_history_file.write(line)
            
            original_history_file.close()
            local_training_history_file.close()
            
            """ 
            # DEBUGGING STUFF
            print "total_ctr = ", total_ctr
            print "visits_ctr = ", visits_ctr
            print "zeros_ctr = ", zeros_ctr
            print "zeros_ctr + visits_ctr = ", zeros_ctr + visits_ctr
            print " -------------------------- "
            """
            if (zeros_ctr + visits_ctr != self.dataset.visits_numb):
                raise Exception("counters mismatch")
    
    # end of ti_CreateTrainingMatrices
    
    def ti_PrepareIntervals(self):
        """
            main TI function - prepares window-directories with documentation
            and prepares corresponding files for history, meta etc.
        """
        
        error_code = 0
        
        # print configurations and some info
        self.ti_PrintHeaderInfo()
        
        # get list of borders
        if self.manual_borders_on:
            print "Flag for manual borders detected!"
            print "Reading borders manually from file..."
            self.ti_ReadBordersManually()
        else:
            self.ti_GenerateBorders()
            
        # print generated borders
        self.ti_PrintBorders()
        
        # check borders for intersections and print warning if found
        borders_intersections = self.ti_CheckIntersections()
        if borders_intersections != []:
            print "WARNING! Intersected windows found:"
            print "borders_intersections = ", borders_intersections
            for window_couples in borders_intersections:
                print "Window ", str(borders_intersections[0]), "intersects window ", str(borders_intersections[1])
    
        # create directories and write info about borders into them
        self.ti_CreateDirs()
        
        # creating of test and train matrices
        self.ti_CreateTestingMatrices()
        self.ti_CreateTrainMatrices()
        print "GAG -- add creating and copying of files"
        
        self.ti_PrintTailInfo()
        
    # enf of ti_PrepareIntervals

# end of TI_Fabric
