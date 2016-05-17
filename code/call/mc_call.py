# -*- coding: utf-8 -*-
"""
European call option by Monte Carlo simulation 

test for vectorized calculation

@author: Minhyun Yoo
"""
import time
import numpy as np
from math import exp, sqrt, log
from scipy import stats

def exc_call(S0, E, T, r, sig):
    d1 = (log(S0/E) + (r + 0.5*sig**2)*T) / (sig*sqrt(T));
    d2 = d1 - sig * sqrt(T);

    call = ( S0 * stats.norm.cdf(d1, 0.0, 1.0) 
        - E * exp(-r * T) * stats.norm.cdf(d2, 0.0, 1.0) )

    print 'Exact call Price : %.5f' % call
    
def mc_call(S0, E, T, r, sig, numSim, numStep):
    dt = T / numStep;
    t0 = time.clock();
    z = np.random.normal(size = [numSim, numStep]);
    s = S0 * np.ones([numSim]);
    for j in xrange(numStep):
        s[:] = s[:] * np.exp((r - 0.5*sig**2)*dt + sig*sqrt(dt)*z[:, j]);
    payoff = np.maximum(s - E, 0);
    call = exp(-r * T) * np.mean(payoff);
    t1 = time.clock();
    del z;
    
    print 'Monte Carlo Call Price : %.5f' % call
    print 'CPU time in Python(sec) : %.4f' % (t1-t0)
    
def mc_call_var_reduc(S0, E, T, r, sig, numSim, numStep):
    dt = T / numStep;
    t0 = time.clock();
    z = np.random.normal(size = [numSim, numStep]);
    sp = S0 * np.ones([numSim]);
    sm = S0 * np.ones([numSim]);
    for j in xrange(numStep):
        sp[:] = sp[:] * np.exp((r - 0.5*sig**2)*dt + sig*sqrt(dt)*z[:, j]);
        sm[:] = sm[:] * np.exp((r - 0.5*sig**2)*dt - sig*sqrt(dt)*z[:, j]);
    payoff1 = np.maximum(sp - E, 0);
    payoff2 = np.maximum(sm - E, 0);
    call = exp(-r * T) * np.mean(0.5*(payoff1+payoff2));
    t1 = time.clock();
    del z;
    
    print 'Monte Carlo Call Price : %.5f' % call
    print 'CPU time in Python(sec) : %.4f' % (t1-t0)

S0 = 100.0; # underlying price
E = 100.0; # strike price
T = 1.0; # maturity
r = 0.03; # riskless interest rate
sig = 0.3; # volatility
ns = 100000;  # # of simulations
nStep = 1; # # of time steps (In this example, nStep does not have to over 1 due to European option pricing.)

# functions call

exc_call(S0, E, T, r, sig); # exact solution

mc_call(S0, E, T, r, sig, ns, nStep); # Monte Carlo simulation

mc_call_var_reduc(S0, E, T, r, sig, ns, nStep);
