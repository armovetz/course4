class Dataset:
    """
        Class represents dataset of historical and meta data - 
        corresponding to dataset stored in magical place
    """
    
    #name = ""
    #dirname = ""
    #history_file_name = ""
    #meta_file_name = ""
    
    users_numb = 0
    items_numb = 0
    metas = {}
    metas_to_use = {}
    binary_ratings = True
    
    def __init__ (self, name_init = "", dirname_init = "", hist_fname_init = "history.mm", meta_fname_init = "semiras.mm"):     
        self.name = name_init
        self.dirname = dirname_init
        self.history_file_name = hist_fname_init
        self.meta_file_name = meta_fname_init
        
    def printDataset(self):
        print "Name = ", self.name
        print "Dirname = ", self.dirname
        print "History file = ", self.history_file_name
        print "Meta file = ", self.meta_file_name
    
    def init_read_dataset_conf_file(self):
        """
            reads configuration file of dataset
            loads parameters of dataset into <Dataset> instace
        """
        
        conf_file = open(self.dirname + "/dataset.conf", 'r')
        
        # string looks like : "users_numb = xxx"
        self.users_numb = int ((conf_file.readline().split())[2])
        
        # string looks like : "items_numb = xxx"
        self.items_numb = int ((conf_file.readline().split())[2])
        
        # string looks like : "binary_ratings = [False|True]"
        binary_ratings = (conf_file.readline().split())[2]
        if binary_line == "False":
            self.binary_ratings = False
        elif binary_line == "True":
            self.binary_ratings = True
        else:
            raise Exception("Incorrect boolean type in dataset's conf file.")

        # begin reading <meta_list>
        # skip header "list of metas"
        if conf_file.readline() != "list of metas:\n":
            raise Exception("Incorrect name of <meta_list>. Must be \"list of metas\".")

        # metas are written in line divided by spaces
        metas_list = conf_file.readline().split()
        
        # turn <metas_list> into dictionary
        self.metas = {}
        for i in range(len(metas_list)):
            self.metas[i] = metas_list[i]
        
        # begin reading <metas_to_use>
        # skip header "list of metas to use"
        if conf_file.readline() != "list of metas to use":
            raise Exception("Incorrect name of <meta_list>. Must be \"list of metas to use\".")

        # metas are written in line divided by spaces
        metas_to_use_list = conf_file.readline().split()

        # turn <metas_to_use> into dictionary
        self.metas_to_use = {}
        for i in range(len(metas_list)):
            if metas_list[i] in metas_to_use_list:
                self.metas_to_use[i] = metas_list[i]
            else:
                raise Exception("Non-existent meta in <metas_to_use>")
        
        
