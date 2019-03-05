"""
This module called *data_management* prepares the inputs for the 
*analysis step*.  

First, it loads the raw data from the
folder *original_data*. 

Second, since the original dataset it large, the 
goal is to keep the variables of interest so that we don't have
to carry out the whole analysis with a heavy dataframe. The are contained
in my_variables.

Third, it renames the variables that we are going to use to 
more user-friendly names, such that we can access them more
easily without need to look for them in manual repeatedly.

Fourth, it generates some additional variables that are interesting
for the final results. There are:
   * income_total: a broader measure of total income.
   * income_capital: a measure of total capital income.
   * net_home_equity: total housing assets minus total secured debt.
   * deb_non_secured: total debt minus secured debt.

Finally it saves all these elements together into
a dataframe called *sfc_clean_pd* and saves it to the folder
*OUT_DATA*. This object will be the input for the analysis step.


"""
import numpy as np
import pandas as pd
import pickle as pkl
from bld.project_paths import project_paths_join as ppj


# -- Load data.

sfc16 = pd.read_stata(ppj("IN_DATA","sfc2016.dta"))


# -- Variables that we want to work with.

my_variables =['income_wage',
                           'income_bussiness',
                           'income_dividendsinterests',
                           'income_capitalgains',
                           'income_retirementincome',
                           'income_transfers',
                           'income_capital',
                           'income_total',
                           'net_worth',
                           'assets_total',
                           'assets_financial',
                           'assets_nfin',
                           'assets_house_main',
                           'assets_house_other',
                           'debt_total',
                           'debt_secured',
                           'debt_nonsecured',
                           'net_home_equity',
                           'hh_age',
                           'hh_employment_status',
                           'hh_id',
                           'hh_weight']
# -- Income variables.

income_wage = sfc16['wageinc']
income_bussiness = sfc16['bussefarminc']
income_dividendsinterests = sfc16['intdivinc']
income_capitalgains = sfc16['kginc']
income_retirementincome = sfc16['ssretinc']
income_transfers = sfc16['transfothinc']
income_capital = income_capitalgains + income_dividendsinterests
income_total = income_bussiness + income_capitalgains + income_dividendsinterests + income_retirementincome + income_transfers + income_wage 


# -- Wealth variables.

net_worth = sfc16['networth']
assets_total = sfc16['asset']
assets_financial = sfc16['fin']
assets_nfin = sfc16['nfin']
assets_house_main = sfc16['houses']
assets_house_other = sfc16['oresre']
debt_total = sfc16['debt']
debt_secured = sfc16['mrthel'] + sfc16['resdbt']
debt_nonsecured = debt_total - debt_secured
net_home_equity = assets_house_main + assets_house_other - debt_secured

# -- Household characteristics.

hh_age = sfc16['age']
hh_employment_status = sfc16['OCCAT1']
hh_id = sfc16['YY1']
hh_weight = sfc16['wgt']

# -- Bundle everything into a dictionary.

sfc_clean_dict = {'income_wage':income_wage,
                           'income_bussiness':income_bussiness,
                           'income_dividendsinterests':income_dividendsinterests,
                           'income_capitalgains':income_capitalgains,
                           'income_retirementincome':income_retirementincome,
                           'income_transfers':income_transfers,
                           'income_capital':income_capital,
                           'income_total':income_total,
                           'net_worth':net_worth,
                           'assets_total':assets_total,
                           'assets_financial':assets_financial,
                           'assets_nfin':assets_nfin,
                           'assets_house_main':assets_house_main,
                           'assets_house_other':assets_house_other,
                           'debt_total':debt_total,
                           'debt_secured':debt_secured,
                           'debt_nonsecured':debt_nonsecured,
                           'net_home_equity':net_home_equity,
                           'hh_age':hh_age,
                           'hh_employment_status':hh_employment_status,
                           'hh_id':hh_id,
                           'hh_weight':hh_weight}

# -- Convert to data frame and set index.

sfc_clean_pd = pd.DataFrame(sfc_clean_dict)
sfc_clean_pd.set_index('hh_id',inplace=True)

# --  Eliminate observations with non-positive income or wealth, for simplicity

#sfc_clean_pd.drop(sfc_clean_pd[sfc_clean_pd.net_worth <= 0].index,inplace = True)
#sfc_clean_pd.drop(sfc_clean_pd[sfc_clean_pd.income_total <= 0].index,inplace = True)
#sfc_clean_pd.drop(sfc_clean_pd[sfc_clean_pd.hh_age <= 25].index,inplace = True)
#sfc_clean_pd.drop(sfc_clean_pd[sfc_clean_pd.hh_age > 80].index,inplace = True)

# -- Save to pickle.

with open(ppj("OUT_DATA", "sfc_clean_pd.pkl"), "wb") as out_file:
    pkl.dump(sfc_clean_pd, out_file)

