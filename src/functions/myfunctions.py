import numpy as np
import pandas as pd

def generate_bins(endpoints,myvariable):
    store_position = np.zeros(shape=len(endpoints))
    store_bin = np.zeros(shape=len(myvariable))
    for i,endpoints_iterate in enumerate(endpoints): 
        # find who is the HH at the end-point of the bin
        store_position[i] = [ n for n,ii in enumerate(myvariable) if ii>endpoints_iterate ][0]
        # assign HHs to bins
        if (i == 0):
            store_bin[0:(int(store_position[i]))] = i+1
        else:
            store_bin[int(store_position[i-1]):(int(store_position[i]))] = i+1
            
    store_bin[store_bin==0] = len(endpoints)+1
    return store_bin




def generate_densities(myweight,myvariable):
    # zip weights and variable
    zipped_pairs= zip(myvariable, myweight)
    # sort weights according to variable
    weights_sorted = [x for _, x in sorted(zipped_pairs)]
    # take cumulative sum - for normalization in case do not add up to one
    weights_cumsum = np.cumsum(weights_sorted)
    # compute pdf
    variable_pdf = weights_sorted/weights_cumsum[-1]
    # compute cdf
    variable_cdf = weights_cumsum/weights_cumsum[-1]
    return variable_pdf, variable_cdf





def generate_gini(myvariable, myweights, mynobs): 

    x = myvariable
    w = pd.Series(myweights).reset_index(drop=True)
    n = mynobs
    wxsum = sum(w * x)
    wsum = sum(w)
    sxw = np.argsort(x)
    sx = x[sxw] * w[sxw]
    sw = w[sxw]
    pxi = np.cumsum(sx) / wxsum
    pci = np.cumsum(sw) / wsum
    ginico = 0.0
    for i in np.arange(1, n):
        ginico = ginico + pxi.iloc[i] * pci.iloc[i - 1] - pci.iloc[i] * pxi.iloc[i - 1]
        
#    lorenzcur_step = weighted_variable.cumsum()/weighted_variable.sum()
    lorenzcur_step = pxi
    lorenzcur = np.concatenate(([0],lorenzcur_step))
    
    return ginico, lorenzcur



def generate_averages(mydataset,myweight,mygroup=None):
    myvariables = list(mydataset)
    if mygroup is None:
        myaverages = pd.DataFrame(columns=myvariables,index=range(1,2))
        for variable_iterate in myvariables:
            myaverages[variable_iterate] = np.average(mydataset[variable_iterate],weights=mydataset[myweight])
    else:
        myaverages = pd.DataFrame(columns=myvariables,index=range(1,(len(np.unique(mydataset[mygroup]))+1)))
        for variable_iterate in myvariables:
            myaverages[variable_iterate] = mydataset.groupby(mygroup).apply(lambda mydataset: 
                np.average(mydataset[variable_iterate],weights=mydataset[myweight]))
    return myaverages
   
        