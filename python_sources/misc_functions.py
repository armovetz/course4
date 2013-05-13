import datetime
import sys
import ini
from ini import *
import numpy

def gag():

    print "!!!!!!!!!!!!!!!!!"
    print " SHAME ON YOU!!!!"
    print " It'S A GAG!!!!!!"
    print "!!!!!!!!!!!!!!!!!"



def getMeta(seminar_meta_string, meta_position_id):
    stri = seminar_meta_string.split('\t')[meta_position_id]
    try:
        int(stri)
    except ValueError:
        return 0
    
    if stri == "":
        return 0
    else:
        return int(stri)
        
def getMetaString(seminar_meta_string, meta_position_id):
    return seminar_meta_string.split('\t')[meta_position_id]


def getWindowCoords():
    window_coords_file = open("window_coord", 'r')
    coords = []
    for line in range(4):
        coords.append(int(window_coords_file.readline().split()[2]))
    window_coords_file.close()
    return coords

def sortMetaListByMeta(list, meta_id_position):
    
    def my_cmp(op1, op2):
        if op1.split('\t')[meta_id_position] == "":
            return -1
        if op2.split('\t')[meta_id_position] == "":
            return 1
        return int(op1.split('\t')[meta_id_position]) - int(op2.split('\t')[meta_id_position])

    def cmpTime(op1, op2):
        """ compares time, that is written in format YYYY-MM-DD HH:MM:SS """
        time_string1 = op1.split('\t')[5]
        time_string2 = op2.split('\t')[5]
        time1 = datetime.datetime.strptime(time_string1, "%Y-%m-%d %H:%M:%S")
        time2 = datetime.datetime.strptime(time_string2, "%Y-%m-%d %H:%M:%S")
        if time1.__ge__(time2):
            return 1
        else:
            return -1

    if meta_id_position == 5:
        # if we need to sort list by time
        return sorted(list, cmpTime)
    else:
        return sorted(list, my_cmp)
        
def cmpTime(time_string1, time_string2):
        """ compares time, that is written in format YYYY-MM-DD HH:MM:SS """
        
        time1 = datetime.datetime.strptime(time_string1, "%Y-%m-%d %H:%M:%S")
        time2 = datetime.datetime.strptime(time_string2, "%Y-%m-%d %H:%M:%S")
        if time1.__ge__(time2):
            return 1
        else:
            return -1
            
def ifTimeInterval(time_string1, time_string2):
    time1 = datetime.datetime.strptime(time_string1, "%Y-%m-%d %H:%M:%S")
    time2 = datetime.datetime.strptime(time_string2, "%Y-%m-%d %H:%M:%S")
    
    """
    print "time1 = ", time1
    print "time2 = ", time2
    print "time1 - time2 = ", abs(time1 - time2)
    print "time1 - time2.days = ", (abs(time1 - time2)).days
    print "time1 - time2.hours = ", (abs(time1 - time2))
    exec("help(time1 - time2)")
    step()
    """
    
    if abs((time1 - time2)).days >= DAYS_INTERVAL_PREPARE:
        return True
    else:
        return False

def getTimeInterval(item_id, item_X_time_list, coords):
    
    low_bound = -1
    high_bound = -1
    
    i = item_id
    while not ifTimeInterval(item_X_time_list[i], item_X_time_list[item_id]):
        if (i - 1) < coords[1]:
            break
        i -= 1
    low_bound = i
    
    i = item_id
    #print "len(item_X_time_list) = ", len(item_X_time_list)
    #print "item_id = ", item_id
    while not ifTimeInterval(item_X_time_list[i], item_X_time_list[item_id]):
        if ((i + 1) > coords[3]) or ((i + 1) >= ITEMS_NUMB - 1):
            break
        i += 1
        #print "i = ", i
    high_bound = i
    
    return [low_bound, high_bound]
    
def step():
    print "Press any key to continue:"
    sys.stdin.read(1)


def cosineSimilarity(vec1, vec2):
    result = float(numpy.dot(abs(vec1), abs(vec2)))

    denominator = (float(numpy.sum(abs(vec1) ** 2)) ** 0.5) * (float(numpy.sum((vec2) ** 2)) ** 0.5)
    
    if denominator == 0.0:
        return 0
    else:
        return (result / denominator)

def getClustersListFromClustersFile(days_interval):
    
    clusters_file = open("test_clusters_" + str(days_interval), 'r')
    
    # skip header 
    clusters_file.readline()
    user0 = int(clusters_file.readline().split("\t")[1]) 
    
    clusters_list = []
    cur_cluster = ["user" + "\t" + str(user0)]

    # reading clusters info to local lists
    for line in clusters_file:
        #print line

        # if new user
        if line.find("user") != -1:
            clusters_list.append(cur_cluster)
            cur_cluster = [line]
        else:
            cur_cluster.append(line)
    # appending last cluster
    clusters_list.append(cur_cluster)
    clusters_file.close()
    
    return clusters_list
