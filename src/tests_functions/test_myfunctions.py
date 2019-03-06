"""

This module called *test_myfunctions.py* contains several tests for the functions contained
in the module *myfunctions.py*. First, it defines contains two setup functions called by the
tests:
     * setup_mytest: generates the artifical dataset sfc_test that is used in the tests.
     * expected_ouptut: in creates a dataframe containing the results that should come out of
       the functions.
Next, it runs four tests:
     * test_generate_bins: tests the function generate_bins.
     * test_generate_densities: tests the function generate_densities.
     * test_generate_gini: tests the function generate_gini. Checks both the Gini Coefficient
       and the Lorenz Curve.
     * test_generate_averages: tests the function generate_averages.

"""
import sys
import pytest
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal, assert_series_equal
from src.functions.myfunctions import generate_bins, generate_densities,generate_gini,generate_averages

def setup_mytest():
    sfc_test = pd.DataFrame(data=[[1,2,3,4,5],
                             [1,2,3,4,5],
                             [27,36,53,61,78],
                             [1,1,1,1,1]])
    sfc_test = sfc_test.T
    sfc_test.columns = ['net_worth','income_total','hh_age','hh_weights']
    
    return sfc_test

def expected_output():
    expected_out={}
    expected_out['pdf'] = np.array([0.2,0.2,0.2,0.2,0.2])
    expected_out['cdf'] = np.array([0.2,0.4,0.6,0.8,1])
    expected_out['lorenz'] = np.array([1/15,2/15,3/15,4/15,5/15]).cumsum()
    expected_out['lorenz'] = np.insert(expected_out['lorenz'],0,0)
    expected_out['ginico'] = 0.26666666
    expected_out['average_net_worth'] = 3
    expected_out['average_income'] = 3
    expected_out['average_age'] = 51 
    expected_out['average_weights'] = 1
    expected_out['wealth_bin'] = np.array([1,2,3,4,5])
    expected_out['income_bin'] = np.array([1,2,3,4,5])
    expected_out['age_bin'] = np.array([1,2,3,4,5])
    expected_out['average_total'] = pd.DataFrame(columns=['net_worth','income_total','hh_age','hh_weights'],index=range(1,2))
    expected_out['average_total']['net_worth'] = float(expected_out['average_net_worth'])
    expected_out['average_total']['income_total'] = float(expected_out['average_income'])
    expected_out['average_total']['hh_age'] = float(expected_out['average_age'])
    expected_out['average_total']['hh_weights'] = float(expected_out['average_weights'])
    return expected_out

def test_generate_bins():
    sfc_test = setup_mytest()
    expected_out = expected_output()
    endpoints_test = [35,45,55,65]
    actual_output = generate_bins(endpoints_test,sfc_test['hh_age'])
    np.testing.assert_array_almost_equal(actual_output,expected_out['age_bin'])
    
def test_generate_densities():
    sfc_test = setup_mytest()
    expected_out = expected_output()
    actual_output_pdf, actual_output_cdf = generate_densities(sfc_test['hh_weights'],sfc_test['net_worth'])
    np.testing.assert_array_almost_equal(actual_output_pdf,expected_out['pdf'])
    np.testing.assert_array_almost_equal(actual_output_cdf,expected_out['cdf'])
    
def test_generate_gini():
    sfc_test = setup_mytest()
    expected_out = expected_output()
    mynobs = 5
    ginico_actual, lorenz_actual = generate_gini(sfc_test['net_worth'],expected_out['pdf'],
                                                 mynobs)
    np.testing.assert_array_almost_equal(lorenz_actual,expected_out['lorenz'])
    np.testing.assert_array_almost_equal(ginico_actual,expected_out['ginico'])
    
def test_generate_averages():
    sfc_test = setup_mytest()
    expected_out = expected_output()
    actual_average = generate_averages(sfc_test,'hh_weights')
    assert_frame_equal(actual_average, expected_out['average_total'])

if __name__ == '__main__':
    status = pytest.main([sys.argv[1]])
    sys.exit(status)