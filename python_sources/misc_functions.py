import datetime

def getMeta(seminar_meta_string, meta_position_id):
    stri = seminar_meta_string.split('\t')[meta_position_id]
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
