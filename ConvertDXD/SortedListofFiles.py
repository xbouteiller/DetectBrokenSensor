def SortedListofFiles(dirName):
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
    return listOfFiles

