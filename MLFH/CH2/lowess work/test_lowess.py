'''
Lowess testing suite.

Expected outcomes are generate by R's lowess function given the same
arguments. The R script test_lowess_r_outputs.R can be used to 
generate the expected outcomes.

The delta tests utilize Silverman's motorcycle collision data,
available in R's MASS package. 
'''

import os
import numpy as np
from numpy.testing import assert_almost_equal

import cylowess
lowess = cylowess.lowess

# Number of decimals to test equality with. 
# The default is 7.
testdec = 7
curdir = os.path.dirname(os.path.abspath(__file__))
rpath = os.path.join(curdir, 'results')

class  TestLowess(object):
     
    def test_simple(self):
        rfile = os.path.join(rpath, 'test_lowess_simple.csv')
        test_data = np.genfromtxt(open(rfile, 'r'),
                                  delimiter = ',', names = True)        
        expected_lowess = np.array([test_data['x'], test_data['out']]).T

        actual_lowess = lowess(test_data['y'], test_data['x'])

        assert_almost_equal(expected_lowess, actual_lowess, decimal = testdec)


    def test_iter(self):
        rfile = os.path.join(rpath, 'test_lowess_iter.csv')
        test_data = np.genfromtxt(open(rfile, 'r'),
                                  delimiter = ',', names = True)
       
        expected_lowess_no_iter = np.array([test_data['x'], test_data['out_0']]).T
        expected_lowess_3_iter = np.array([test_data['x'], test_data['out_3']]).T
                                            
        actual_lowess_no_iter = lowess(test_data['y'], test_data['x'], it = 0)
        actual_lowess_3_iter = lowess(test_data['y'], test_data['x'], it = 3)

        assert_almost_equal(expected_lowess_no_iter, actual_lowess_no_iter, decimal = testdec)
        assert_almost_equal(expected_lowess_3_iter, actual_lowess_3_iter, decimal = testdec)


    def test_frac(self):
        rfile = os.path.join(rpath, 'test_lowess_frac.csv')
        test_data = np.genfromtxt(open(rfile, 'r'),
                                  delimiter = ',', names = True)
       
        expected_lowess_23 = np.array([test_data['x'], test_data['out_2_3']]).T
        expected_lowess_15 = np.array([test_data['x'], test_data['out_1_5']]).T
	
        actual_lowess_23 = lowess(test_data['y'], test_data['x'] ,frac = 2./3)
        actual_lowess_15 = lowess(test_data['y'], test_data['x'] ,frac = 1./5)

        assert_almost_equal(expected_lowess_23, actual_lowess_23, decimal = testdec)
        assert_almost_equal(expected_lowess_15, actual_lowess_15, decimal = testdec)


    def test_delta(self):
        rfile = os.path.join(rpath, 'test_lowess_delta.csv')
        test_data = np.genfromtxt(open(rfile, 'r'),
                                  delimiter = ',', names = True)

        expected_lowess_del0 = np.array([test_data['x'], test_data['out_0']]).T
        expected_lowess_delRdef = np.array([test_data['x'], test_data['out_Rdef']]).T
	expected_lowess_del1 = np.array([test_data['x'], test_data['out_1']]).T
	
        actual_lowess_del0    = lowess(test_data['y'], test_data['x'], frac = 0.1)
        actual_lowess_delRdef = lowess(test_data['y'], test_data['x'], frac = 0.1,
				       delta = 0.01 * np.ptp(test_data['x']))
        actual_lowess_del1    = lowess(test_data['y'], test_data['x'], frac = 0.1, delta = 1.0)
	
        assert_almost_equal(expected_lowess_del0, actual_lowess_del0, decimal = testdec)
        assert_almost_equal(expected_lowess_delRdef, actual_lowess_delRdef, decimal = testdec)
        assert_almost_equal(expected_lowess_del1, actual_lowess_del1, decimal = testdec)


if __name__ == "__main__":
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--noexe'], exit=False)

