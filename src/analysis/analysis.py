import pandas as pd
import numpy as np
import pickle as pkl
from myfunctions import generate_bins
from myfunctions import generate_densities
from myfunctions import generate_gini
from myfunctions import generate_averages

sfc_clean_pd = pd.read_pickle('../data_management/sfc_clean_pd.pkl')



###############################################################################
# Create population partitions by net worth, income and age ###################
###############################################################################

# -- number of observations.

sample_nobs = len(sfc_clean_pd)


#____________ Compute empirical cdfs and pdfs of income/wealth________________#




# -- Weights as np array to pass to generage_densities function.
weights_np = np.array(sfc_clean_pd['hh_weight'])

# -- Index of sorted wealth and income. Required to create pdf and cdf.
net_worth_index_sorted = np.argsort(np.array(sfc_clean_pd['net_worth']))
income_total_index_sorted = np.argsort(np.array(sfc_clean_pd['income_total']))

# -- Call generate_densities to get pdf and cdf.
net_worth_pdf, net_worth_cdf = generate_densities(weights_np,net_worth_index_sorted)
income_total_pdf, income_total_cdf = generate_densities(weights_np,income_total_index_sorted)


#________ Compute income deciles/quantiles___________________________________#

# -- bin end-points for deciles quintiles.
deciles = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
quintiles = [.2,0.4,0.6,0.8]


# -- call generate_bins function. Needs cdf from previous step.

income_total_quintiles = generate_bins(quintiles,income_total_cdf)
income_total_deciles  = generate_bins(deciles,income_total_cdf)

# -- sort dataframe by income and add new series.

sfc_clean_sort_income_total = sfc_clean_pd.sort_values(by=['income_total'])
sfc_clean_sort_income_total['income_total_pdf'] = income_total_pdf
sfc_clean_sort_income_total['income_total_cdf'] = income_total_cdf
sfc_clean_sort_income_total['income_total_deciles'] = income_total_deciles
sfc_clean_sort_income_total['income_total_quintiles'] = income_total_quintiles




#________ Compute wealth deciles/quantiles___________________________________#

# -- call generate_bins function. Needs cdf from previous step.

net_worth_quintiles = generate_bins(quintiles,net_worth_cdf)
net_worth_deciles   = generate_bins(deciles,net_worth_cdf)

# -- sort dataframe by wealth and add new series.

sfc_clean_sort_net_worth = sfc_clean_pd.sort_values(by=['net_worth'])
sfc_clean_sort_net_worth['net_worth_pdf'] = net_worth_pdf
sfc_clean_sort_net_worth['net_worth_cdf'] = net_worth_cdf
sfc_clean_sort_net_worth['net_worth_deciles'] = net_worth_deciles
sfc_clean_sort_net_worth['net_worth_quintiles'] = net_worth_quintiles



#_________________________________ compute age groups _______________________#

# -- bin end-points for age.

age_bin_end_points = [35,45,55,65]

# -- extract age as sorted np array

age_np = np.sort(np.array(sfc_clean_pd['hh_age']))

# -- age

age_bin = generate_bins(age_bin_end_points,age_np)

# -- sort dataframe by age and add new series.

sfc_clean_sort_age = sfc_clean_pd.sort_values(by=['hh_age'])
sfc_clean_sort_age['age_bin'] = age_bin




###############################################################################
################# Compute Gini Coefficients ###################################
###############################################################################



# -- Note that gini requires variable to be sorted.

# -- gini co for net worth

gini_net_worth, lorenz_net_worth = generate_gini(np.array(sfc_clean_sort_net_worth['net_worth']),
                                     np.array(sfc_clean_sort_net_worth['hh_weight']),
                                     sample_nobs)

# -- gini co for income
gini_income_total, lorenz_income_total = generate_gini(np.array(sfc_clean_sort_income_total['income_total']),
                                     np.array(sfc_clean_sort_income_total['hh_weight']),
                                     sample_nobs)





###############################################################################
################ Compute averages by partition ################################
###############################################################################



# variables that we want to compute the average of.

variables_here = list(sfc_clean_sort_income_total)


# ________________ Compute total averages ___________________________________ #


average_total = generate_averages(sfc_clean_sort_income_total,'hh_weight')




#________________ Income Partition ___________________________________________#


average_income_partition_quintiles = generate_averages(sfc_clean_sort_income_total,'hh_weight',
                                                       'income_total_quintiles')
average_income_partition_deciles = generate_averages(sfc_clean_sort_income_total,'hh_weight',
                                                       'income_total_deciles')

    
        
#_____________ Net Worth Partition ___________________________________________#
        
        
average_net_worth_partition_quintiles = generate_averages(sfc_clean_sort_net_worth,'hh_weight',
                                                       'net_worth_quintiles')
average_net_worth_partition_deciles = generate_averages(sfc_clean_sort_net_worth,'hh_weight',
                                                       'net_worth_deciles')        
      

#___________ Age Partition ___________________________________________________#

average_age_partition = generate_averages(sfc_clean_sort_age,'hh_weight',
                                                       'age_bin')

        
#____________ Redefine some variables ________________________________________#
        

        
# redefine income sources as percentage of total income
income_sources = ['income_wage','income_bussiness','income_capital','income_transfers','income_retirementincome']

for variable_iterate in income_sources:
    average_net_worth_partition_quintiles[variable_iterate] = average_net_worth_partition_quintiles[variable_iterate]/average_net_worth_partition_quintiles['income_total']*100; 
    average_income_partition_quintiles[variable_iterate] = average_income_partition_quintiles[variable_iterate]/average_income_partition_quintiles['income_total']*100; 
    average_age_partition[variable_iterate] = average_age_partition[variable_iterate]/average_age_partition['income_total']*100; 
    average_net_worth_partition_deciles[variable_iterate] = average_net_worth_partition_deciles[variable_iterate]/average_net_worth_partition_deciles['income_total']*100; 
    average_income_partition_deciles[variable_iterate] = average_income_partition_deciles[variable_iterate]/average_income_partition_deciles['income_total']*100; 
    
# redefine portfolio composition: financial assets/totalassets, home equity/net worth, secured debt/total debt
portfolio_variables = ['assets_financial','debt_secured','net_home_equity']

for variable_iterate in portfolio_variables:
    average_net_worth_partition_quintiles[variable_iterate] = average_net_worth_partition_quintiles[variable_iterate]/average_net_worth_partition_quintiles['net_worth']*100; 
    average_income_partition_quintiles[variable_iterate] = average_income_partition_quintiles[variable_iterate]/average_income_partition_quintiles['net_worth']*100; 
    average_age_partition[variable_iterate] = average_age_partition[variable_iterate]/average_age_partition['net_worth']*100; 
    average_net_worth_partition_deciles[variable_iterate] = average_net_worth_partition_quintiles[variable_iterate]/average_net_worth_partition_quintiles['net_worth']*100; 
    average_income_partition_deciles[variable_iterate] = average_income_partition_quintiles[variable_iterate]/average_income_partition_quintiles['net_worth']*100; 




###############################################################################
############ Store Everything to produce final output #########################
###############################################################################
    
# -- merge into a dictionary
    
data_to_output = {'average_net_worth_partition_quintiles':average_net_worth_partition_quintiles,
              'average_income_partition_quintiles': average_income_partition_quintiles,
              'average_age_partition':average_age_partition,
              'average_net_worth_partition_deciles':average_net_worth_partition_deciles,
              'average_income_partition_deciles':average_income_partition_deciles,
              'average_total':average_total,
              'gini_net_worth': gini_net_worth,
              'gini_income_total':gini_income_total,
              'lorenz_net_worth':lorenz_net_worth,
              'lorenz_income_total': lorenz_income_total,
              'sfc_clean_pd':sfc_clean_pd,
              'sfc_clean_sort_net_worth':sfc_clean_sort_net_worth,
              'sfc_clean_sort_income_total':sfc_clean_sort_income_total
        }


# -- save dictionary
f = open("data_to_output.pkl","wb")
pkl.dump(data_to_output,f)
f.close()

