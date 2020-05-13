def ChangeDataPath(WorkingPath):
    import os
    import sys
    
    if os.path.exists(WorkingPath):
        print ("\npath exist")
    else:
        raise Exception('the given path does not exist') 

    # Change working directory    
    os.chdir(WorkingPath)
    print('Working directory changed to: {}'.format(WorkingPath))
    
    if not os.path.exists('log'):
        os.makedirs('log')
        print('log folder created')
    
    if not os.path.exists('FileInfo'):
        os.makedirs('FileInfo')
        print('FileInfo folder created')
        
    if not os.path.exists('DiagPlot\\Perfeature'):
        os.makedirs('DiagPlot\\Perfeature')
        print('DiagPlot\\Perfeature folder created')
        
    if not os.path.exists('DiagPlot\\Mean'):
        os.makedirs('DiagPlot\\Mean')
        print('DiagPlot\\Mean folder created')
        
    for col in ['moteur_g', 't_poulie_g', 't_nez_g', 'mot_x_g', 'affuteur_g', 'bv_r_g', 'bv_a_g']:
        if not os.path.exists('DiagPlot\\Perfeature\\'+col):
            os.makedirs('DiagPlot\\Perfeature\\'+col)
            print('DiagPlot\\Perfeature\\'+col+ ' folder created')    