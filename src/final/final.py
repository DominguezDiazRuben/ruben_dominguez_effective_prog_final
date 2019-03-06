"""
This module called *final* does the *final step*.

First, it loads the data generated in the *analysis step* and unpacks it appropiately. 

The main goal of this module is to produces tables in latex format and
plots such that they can be included into the .tex file right the way.

The module can be broadly subdivided into two different parts.

	* Prepare tables to present: this part generates the tables to be included in the paper.
	  First, it selects the variables that we want to report in the table (variables_to_keep).
	  Second, it expresses income and net worth in thousands so that they fit nicely in the table.
	  Third, due to the large amount of decimals it converts values to integers. Fourth, it 
	  renames variables as we want them to appear in the paper. Fith, it exports to latex the 
	  following tables:
		* Deciles of Net Worth Distribution.
		* Deciles of Income Distribution.
		* Quintiles of Net Worth Distribution.
		* Quintiles of Income Distribution.
		* Age Distribution.
		* Gini Coefficients.

	* Prepare Histograms and Lorenz: it generates two histograms and two Lorenz curves 
	  that are reported in the paper:
		* Histogram of Income.
		* Histogram of Net Worth.
		* Lorenz curve of Income.
		* Lorenz curve of Net Worth.

Figures and tables are stored in the folders *OUT_FIGURES* and *OUT_TABLES*, respectively.


"""


from bld.project_paths import project_paths_join as ppj
import numpy as np
import pandas as pd
import pickle as pkl
import matplotlib.pyplot as plt

# -- Read data.
data_to_output = pkl.load(open(ppj("OUT_ANALYSIS","data_to_output.pkl"),"rb"))
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

gini_networth = data_to_output['gini_net_worth']
gini_income   = data_to_output['gini_income_total']

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

# -- Some variables in thousands for readability.

variables_in_thousands = ['net_worth','income_total']
net_worth_quintiles_table[variables_in_thousands] = net_worth_quintiles_table[variables_in_thousands]/1000
net_worth_deciles_table[variables_in_thousands] = net_worth_deciles_table[variables_in_thousands]/1000 
income_quintiles_table[variables_in_thousands] = income_quintiles_table[variables_in_thousands]/1000
income_deciles_table[variables_in_thousands] = income_deciles_table[variables_in_thousands]/1000 
age_partition_table[variables_in_thousands] = age_partition_table[variables_in_thousands]/1000

# -- Present values as integers.age_partition_table

net_worth_quintiles_table = net_worth_quintiles_table.astype(int)
net_worth_deciles_table = net_worth_deciles_table.astype(int)
income_quintiles_table = income_quintiles_table.astype(int)
income_deciles_table = income_deciles_table.astype(int)
age_partition_table = age_partition_table.astype(int)


# -- Rename columns to present.

rename_columns = ['Net Worth (Thousands of $)','Income (Thousands of $)','Age','Wages (% of income)',
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

# -- Save the gini coefficients to report in text.

gini_pd = pd.DataFrame(data=([gini_income,gini_networth]))



# --- Save to latex

with open(ppj("OUT_TABLES", "net_worth_deciles_table.tex"), "w") as tf:
     tf.write(net_worth_deciles_table.to_latex())

with open(ppj("OUT_TABLES", "net_worth_quintiles_table.tex"), "w") as tf:
     tf.write(net_worth_quintiles_table.to_latex())
     
with open(ppj("OUT_TABLES", "income_deciles_table.tex"), "w") as tf:
     tf.write(income_deciles_table.to_latex())

with open(ppj("OUT_TABLES", "income_quintiles_table.tex"), "w") as tf:
     tf.write(income_quintiles_table.to_latex())
     
with open(ppj("OUT_TABLES", "age_partition.tex"), "w") as tf:
     tf.write(age_partition_table.to_latex())

with open(ppj("OUT_TABLES", "ginis.tex"), "w") as tf:
     tf.write(gini_pd.to_latex())
     
###############################################################################
############### Prepare Histogram and Lorez  ##################################
###############################################################################

# -- drop super wealthy guys to make the histogram nice

sfc_clean_pd.drop(sfc_clean_pd[sfc_clean_pd.net_worth >= 5*float(average_total['net_worth'])].index,inplace=True)
sfc_clean_pd.drop(sfc_clean_pd[sfc_clean_pd.income_total >= 5*float(average_total['income_total'])].index,inplace=True)

plt.figure()
plt.hist(sfc_clean_pd['net_worth']/1000,bins=50)
plt.xlabel('Net Worth (Thousands) ')
plt.ylabel('Frequency')
plt.title('Histogram of Net Worth')
plt.savefig(ppj("OUT_FIGURES","histogram_networth.png"))

plt.figure()
plt.hist(sfc_clean_pd['income_total']/1000,bins=80)
plt.xlabel('Income (Thousands) ')
plt.ylabel('Frequency')
plt.title('Histogram of Income')
plt.savefig(ppj("OUT_FIGURES","histogram_income.png"))

plt.figure()
plt.plot(np.linspace(0.0, 1.0, lorenz_income.size), lorenz_income,'b')
plt.plot([0,1], [0,1],'k')
plt.xlabel('% of Population')
plt.ylabel('% of Income Owned')
plt.title('Lorenz Curve of Income')
plt.savefig(ppj("OUT_FIGURES","lorenz_income.png"))

plt.figure()
plt.plot(np.linspace(0.0, 1.0, lorenz_net_worth.size), lorenz_net_worth,'b')
plt.plot([0,1], [0,1],'k')
plt.xlabel('% of Population')
plt.ylabel('% of Net Worth Owned')
plt.title('Lorenz Curve of Net Worth')
plt.savefig(ppj("OUT_FIGURES","lorenz_networth.png"))