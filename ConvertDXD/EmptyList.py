def EmptyListofFiles():
    '''
    # function for crating an empty list for the first day
    # should evaluate if file exists and creat it only if file not exists
    '''
    import os
    import pickle
    
    
    if not os.path.isfile("ListOfFiles.txt"): 
        ListOfFiles=[]
        with open("ListOfFiles.txt", "wb") as fp:   #Pickling
            pickle.dump(ListOfFiles, fp)
        
        print('Empty ListOfFiles created')
    else:
        print('ListOfFiles already here, \nnothing done !')
        
        
def PreviousListofFiles():
    import pickle
    import os
    with open("ListOfFiles.txt", "rb") as fp:   # Unpickling
        PreviousLoF = pickle.load(fp)
    print('Previous list of file loaded, length is {}'.format(len(PreviousLoF)))
    return PreviousLoF


def CurrentListofFiles(dirName):
    '''
    parse files trought a path from folder tree and sort the files by natural sorting
    '''
    from natsort import natsorted
    import re
    import os    
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames if file.endswith('.dxd')] #&&&
    #sort fils by natural ordering
    listOfFiles=natsorted(listOfFiles)   
    print('Current list of file loaded, length is {}'.format(len(listOfFiles)))    
    return listOfFiles


#diff between lists
def DifferenceBetweenListofFiles(PreviousLoF, CurrentLoF):
    s = set(PreviousLoF)
    DifferenceLoF = [x for x in CurrentLoF if x not in s]
    print('Difference list of file loaded, length is {}'.format(len(DifferenceLoF)))
    return DifferenceLoF



def SaveCurrentListofFiles(CurrentLoF):
    import pickle
    import os
    with open("ListOfFiles.txt", "wb") as fp:   #Pickling
        pickle.dump(CurrentLoF, fp)
    print('Current list of file saved, replacing old one')
