import scipy.io.mmio
import datetime
import math

def estimateLocal():
    # file stuff
    prediction_matrix = scipy.io.mmio.mmread("prediction.mtx")
    test_matrix = scipy.io.mmio.mmread("test.mtx").tocsr()
    clusters_file = open("test_clusters", 'r')
    
    # get 'window' coords
    coords = getWindowCoords()
    
    # skip header
    clusters_file.readline()
    clusters_list = []
    cur_cluster = ["user" + "\t" + str(coords[1])]

    for line in clusters_file:
        # new user
        if line.find("user") != None:
            clusters_list.append(cur_cluster)
            cur_cluster = [line]
        else:
            cur_cluster.append(line)
    
    local_average
    for user_claster in clusters_list:
        user = int(user_claster[0].split("\t")[1])
        user_prediction = prediction_matrix[user].toarray()[0]
        user_visits = test_matrix[user].toarray()[0]
        
        user_average_nDCGp = float(0.0)
        for byte in user_claster[1:]
            #byte_double_array = numpy.zeros((2, byte.split("\t")[1] - byte.split("\t")[0] + 1), dtype = float)
            #byte_double_array[0 : ] = user_visits[byte.split("\t")[0] : byte.split("\t")[1] + 1]
            #byte_double_array[1 : ] = user_prediction[byte.split("\t")[0] : byte.split("\t")[1] + 1]
            
            byte_visits = user_visits[byte.split("\t")[0] : byte.split("\t")[1] + 1]
            byte_predictions = user_prediction[byte.split("\t")[0] : byte.split("\t")[1] + 1]
            
            # get indices of columns by decreasing of prediction value
            indices = numpy.lexsort(key = (byte_prediction, byte_prediction))
            
            # sort vector of visits and predictions with help of indices
            sorted_predictions = byte_predicitions.take(indices, axis = -1)
            sorted_visits = byte_visits.take(indices, axis = -1)
            
            if len(sorted_predictions) != len(sorted_visits):
                raise Exception("visits and prediction clusters have differet size")
            
            """ TO BE NORMALIZED """
            nDCGp = float(0.0)
            p = len(sorted_predictions)
            for i in range(1, p + 1):
                nDCGp += float(sorted_visits[i - 1]) / float(math.log(i + 1, 2))
            """ / TO BE NORMALIZED """
            
            if (nDCGp < 0.0) or (nDCGp > 1.0):
                raise Exception("Incorrect nDCGp")
            user_average_nDCGp += nDCGp
            
        user_average_nDCGp /= (len(user_claster) - 1)
        local_average_nDCGp += user_average_nDCGp
    
    local_average_nDCGp /= (len(clusters_list))
    return local_average_nDCGp
