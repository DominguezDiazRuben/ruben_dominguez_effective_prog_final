### clean data to select variables used later on during the analysis.

import numpy as np
import pandas as pd
import pickle as pk



# -- Load data.

sfc16 = pd.read_stata("../data/sfc2016.dta") 


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

sfc_clean_pd = pd.DataFrame(sfc_clean_dict)
sfc_clean_pd.set_index('hh_id',inplace=True)

# --  Eliminate observations with non-positive income or wealth, for simplicity

#sfc_clean_pd.drop(sfc_clean_pd[sfc_clean_pd.net_worth <= 0].index,inplace = True)
#sfc_clean_pd.drop(sfc_clean_pd[sfc_clean_pd.income_total <= 0].index,inplace = True)
sfc_clean_pd.drop(sfc_clean_pd[sfc_clean_pd.hh_age <= 25].index,inplace = True)
sfc_clean_pd.drop(sfc_clean_pd[sfc_clean_pd.hh_age > 80].index,inplace = True)

# -- Save to pickle.

sfc_clean_pd.to_pickle('sfc_clean_pd.pkl')
