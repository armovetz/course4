import ti_settings 
from ti_settings import *
import copy
import datetime
import subprocess

def ti_PrintHeaderInfo():
    
    print "------------------------"
    print "HELLO WORLD!\n"
    
    start_time = datetime.datetime.now().strftime("%Y-%m-%d__%H:%M")
    print "TIME: ", start_time
    
    if INI_comment != 0:
        print "Comment attached:\n", comment
    
    print "\n"
    print "Parameters: "
    print "time_interval = ",       INI_time_interval
    print "manual_borders_on = ",   INI_manual_borders_on
    if INI_manual_borders_on :
        print "borders_file_name = ", INI_borders_file_name
    print "full-length_on= ",       INI_full_length_on
    print "case_dir_name = ",       INI_case_dir_name
    #print "time_interval = ",       INI_time_interval
    print "-------------------------"
    
# end of ti_PrintHeaderInfo
    
def ti_PrintTailInfo(error_code, exception_text):
    
    if error_code != 0 :
        print "TIME INTERVAL PREPARING PROCEDURE FAILED!!!"
        print "ti FAIL"
        print "EXCEPTION:"
        print exception_text
    else:
        print "TIME INTERVAL PREPARING PROCEDURE PASSED!!!"
        print "ti OK"
    
    print "----------------"
    print "END OF LOG"
# end of ti_PrintTailInfo

def ti_PrintBorders(borders):
    """
        prints info about every window in <borders>
    """
    
    print "BORDERS:"
    
    j = 0
    
    for window_coord in borders:
        print "---"
        print "Window #", j
        print "users : [", window_coord[0], ",", window_coord[1], "]"
        print "items : [", window_coord[2], ",", window_coord[3], "]"
    
    print "-------------------------"
# end of ti_PrintBorders

def ti_CreateDirs(borders):
    """
        launch shell script to make directories and write info
        about windows' borders
    """
    
    if INI_case_dir_name == 0:
        # if case name is not set - set is as time of its creating
        case_dir_name = datetime.datetime.now().strftime("%Y-%m-%d__%H:%M")
    else:
        if ( str(type(INI_case_dir_name)) == "<type 'str'>" ):
            case_dir_name = INI_case_dir_name
        else:
            raise(Exception("Bad type of <INI_case_dir_name>"))
    
    j = 0
    
    for window_coords in borders:
        
        window_dir_name = str(j) + \
        "_USERS" + str(window_coords[0]) + "x" + str(window_coords[1]) + \
        "_ITEMS" + str(window_coords[2]) + "x" + str(window_coords[3])
        
        subprocess.call(["mkdir", "-p", INI_ti_dir_path + "/" + case_dir_name + "/" + window_dir_name])
        
        coords_file = open(INI_ti_dir_path + "/" + case_dir_name + "/" + window_dir_name + "/window_coords", 'w')
        coords_file.write("start_user = " + str(window_coords[0]) + "\n")
        coords_file.write("stop_user = "  + str(window_coords[1]) + "\n")
        coords_file.write("start_item = " + str(window_coords[2]) + "\n")
        coords_file.write("stop_item = "  + str(window_coords[3]) + "\n")
        coords_file.close()
        j += 1
# enf of ti_CreateDirs

def ti_GenerateBorders(dataset)
    """
        reads parameters of borders,
        get list of seminars from data files,
        return borders
    """
    
    print "GAG"
    
    seminars_file = open(dataset.meta_file_name, 'r')
    
    seminars_list = []
    for seminar_line in seminars_file:
        seminars_list.append(seminar_line)
    
    
# enf of ti_GenerateBorders

def ti_ReadBordersManually(borders_file_name):
    """
        reads borders manually from file
        generate warning if windows are 
    """
    
    borders_file = open(borders_file_name)
    
    borders = []
    
    for line in borders_file:
        window_coords = map(int,line.split())
        if len(window_coords) != 4 :      # raise exception - one line must correspond to one window
            raise(Exception("Bad windows coords in string: " + line))
        
        borders.append(window_coords)
    
    borders_file.close()
    return borders

# end of ti_ReadBordersManually

def ti_CheckIntersections(borders):
    """
        throws a WARNING message if some windows in <borders> are
        intersected (in both users or seminars)
    """
    
    intersected_windows = []
    
    for window_coords in borders:
        borders_clone = copy.deepcopy(borders)
        borders_clone.remove(window_coords)
        
        if window_coords in borders_clone :    # every borders list must not repeat
            raise(Exception("Repeated window is forbidden in declaration of borders:" + str(window_coords)))
        
        for cmp_window_coords in borders_clone:
            user_intersect = set(range(cmp_window_coords[0], cmp_window_coords[1] + 1)) & set(range(window_coords[0], window_coords[1] + 1))
            item_intersect = set(range(cmp_window_coords[2], cmp_window_coords[3] + 1)) & set(range(window_coords[2], window_coords[3] + 1))
            
            if (len(user_intersect) != 0) or (len(item_intersect) != 0)  :
                #intersected_windows.append([list(user_intersect), list(item_intersect)])
                print "!!!"
                intersected_windows.append([window_coords, cmp_window_coords])
    
    return intersected_windows
    # end of ti_CheckIntersections

#def ti_GenerateBorders():

def ti_PrepareIntervals():
    """
        main TI function - prepares window-directories with documentation
        and prepares corresponding files for history, meta etc.
    """
    
    error_code = 0
    
    # print configurations and some info
    ti_PrintHeaderInfo()
    
    # get list of borders
    if INI_manual_borders_on:
        print "Flag for manual borders detected!"
        print "Reading borders manually from file..."
        borders = ti_ReadBordersManually(INI_borders_file_name)
    else:
        borders = ti_GenerateBorders()
        
    # print generated borders
    ti_PrintBorders(borders)
    
    # check borders for intersections and print warning if found
    borders_intersections = ti_CheckIntersections(borders)
    if borders_intersections != []:
        print "WARNING! Intersected windows found:"
        print "borders_intersections = ", borders_intersections
        for window_couples in borders_intersections:
            print "Window ", str(borders_intersections[0]), "intersects window ", str(borders_intersections[1])

    # create directories and write info about borders into them
    dirs = ti_CreateDirs(borders)
    
    # creating of test and train matrices
    print "GAG -- add creating and copy of files"
    
    ti_PrintTailInfo(error_code)
    
# enf of ti_PrepareIntervals
