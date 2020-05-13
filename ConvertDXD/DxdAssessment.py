def EvalFile(df, mode, column, filterSignalThres):
    import numpy as np
    import pandas as pd
    
    validM = {'below', 'above', 'equals_0'}
    if mode not in validM:
        raise ValueError("results: mode must be one of %r." % validM)
        
    validC = df.columns
    if column not in validC:
        raise ValueError("results: column must be one of %r." % validC)
        
    #data bv_r_g capteur
    loadeddf=df[[column]]
    
    # Apply the filter only if % of broken value is higher than a threshold
    
    if mode == 'above':
        proportionofFsignal=loadeddf[np.abs(loadeddf[column])>filterSignalThres].shape[0]/loadeddf.shape[0] 

    if mode == 'below':
        proportionofFsignal=loadeddf[np.abs(loadeddf[column])<filterSignalThres].shape[0]/loadeddf.shape[0] 
        
    if mode == 'equals_0':
        proportionofFsignal=loadeddf[np.abs(loadeddf[column])==0].shape[0]/loadeddf.shape[0]
        
    print('proportion of {} signal {} threshold {} is : {}'.format(column, mode, filterSignalThres, proportionofFsignal))

    return [proportionofFsignal]
