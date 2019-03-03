import numpy as np
import pandas as pd
import pickle as pkl
import matplotlib.pyplot as plt

# -- Read data.

data_to_output = pkl.load( open( "../analysis/data_to_output.pkl", "rb" ) )

# -- Prepare dataframes as if where passed as latex tables

# -- Read out dictionary

net_worth_quintiles = data_to_output['average_net_worth_partition_quintiles']
net_worth_deciles = data_to_output['average_net_worth_partition_deciles']

income_quintiles = data_to_output['average_income_partition_quintiles']
income_deciles = data_to_output['average_income_partition_deciles']

age_partition = data_to_output['average_age_partition']

average_total = data_to_output['average_total']

sfc_clean_pd = data_to_output['sfc_clean_pd']
sfc_net_worth_sort = data_to_output['sfc_clean_sort_net_worth']
sfc_income_sort = data_to_output['sfc_clean_sort_income_total']

lorenz_net_worth = data_to_output['lorenz_net_worth']
lorenz_income = data_to_output['lorenz_income_total']

###############################################################################
############### Prepare Tables to present #####################################
###############################################################################

# -- variables that we want to keep for the tables.

variables_to_keep = ['net_worth','income_total','hh_age'
                     ,'income_wage','income_bussiness',
                     'income_capital','income_transfers',
                     'income_retirementincome',
                     'assets_financial','net_home_equity',
                     'debt_secured']

# -- Reduce data frames.

net_worth_quintiles_table = net_worth_quintiles[variables_to_keep]
net_worth_deciles_table = net_worth_deciles[variables_to_keep]
income_quintiles_table = income_quintiles[variables_to_keep]
income_deciles_table = income_deciles[variables_to_keep]
age_partition_table = age_partition[variables_to_keep]

# -- Rename columns to present.

rename_columns = ['Net Worth','Income','Age','Wages (% of income)',
                  'Business Income (% of income)','Capital Income (% of income)'
                  ,'Transfers Income (% of income)','SS and Retirement Income (% of income)',
                  'Financial Assets (% Net Worth)','Home Equity (% Net Worth)',
                  'Secured Debt (% Net Worth)']

net_worth_deciles_table.columns = rename_columns
net_worth_quintiles_table.columns = rename_columns
income_quintiles_table.columns = rename_columns
income_deciles_table.columns = rename_columns
age_partition_table.columns = rename_columns

# -- Traspose

net_worth_deciles_table = net_worth_deciles_table.T
net_worth_quintiles_table = net_worth_quintiles_table.T
income_deciles_table = income_deciles_table.T
income_quintiles_table = income_quintiles_table.T
age_partition_table = age_partition_table.T

# -- Now rename to quantiles and age groups

rename_quintiles = ['Q1','Q2','Q3','Q4','Q5']
rename_deciles   = ['D1','D2','D3','D4','D5','D6','D7','D8','D9','D10']
rename_age = ['25-35','35-45','45-55','55-65','>65']

net_worth_deciles_table.columns = rename_deciles
income_deciles_table.columns = rename_deciles
net_worth_quintiles_table.columns = rename_quintiles
income_quintiles_table.columns = rename_quintiles
age_partition_table.columns = rename_age


# --- Save to latex

with open('net_worth_deciles_table.tex', 'w') as tf:
     tf.write(net_worth_deciles_table.to_latex())

with open('net_worth_quintiles_table.tex', 'w') as tf:
     tf.write(net_worth_quintiles_table.to_latex())
     
with open('income_deciles_table.tex', 'w') as tf:
     tf.write(income_deciles_table.to_latex())

with open('income_quintiles_table.tex', 'w') as tf:
     tf.write(income_quintiles_table.to_latex())
     
with open('age_partition.tex', 'w') as tf:
     tf.write(age_partition.to_latex())
     
###############################################################################
############### Prepare Histogram and Lorez  ##################################
###############################################################################

# -- drop super wealthy guys to make the histogram nice

sfc_clean_pd.drop(sfc_clean_pd[sfc_clean_pd.net_worth >= 5*float(average_total['net_worth'])].index,inplace=True)
sfc_clean_pd.drop(sfc_clean_pd[sfc_clean_pd.income_total >= 5*float(average_total['income_total'])].index,inplace=True)

plt.figure()
plt.hist(sfc_clean_pd['net_worth']/1000,bins=50)
plt.savefig('histogram_networth.png')

plt.figure()
plt.hist(sfc_clean_pd['income_total']/1000,bins=80)
plt.savefig('histogram_income.png')

plt.figure()
plt.plot(np.linspace(0.0, 1.0, lorenz_income.size), lorenz_income)
plt.plot([0,1], [0,1])
plt.savefig('lorenz_income.png')

plt.figure()
plt.plot(np.linspace(0.0, 1.0, lorenz_net_worth.size), lorenz_net_worth)
plt.plot([0,1], [0,1])
plt.savefig('lorenz_networth')