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

    print 'Exact call Price : %.5f\n' % call

def mc_call(S0, E, T, r, sig, numSim, numStep):

    dt = T / numStep; # time step
    accum = 0.0; # accumulated payoff
    t0 = time.clock();
    for i in range(numSim): # simulation loop
        s = S0;
        for j in range(numStep): # timestep loop
            z = np.random.normal();
            # Geometric Brownian motion
            s = s * exp((r - 0.5*sig**2)*dt + sig*sqrt(dt)*z);
        payoff = max(s - E, 0); # vanilla call
        accum = accum + payoff; # accumulate payoff
    call = exp(-r * T) * (accum / numSim); # expectation
    t1 = time.clock();
    
    print 'version 0' 
    print 'Call Price : %.5f' % call
    print 'CPU time in Python(sec) : %.4f' % (t1-t0)
    
def mc_call_vec1(S0, E, T, r, sig, numSim, numStep):
    dt = T / numStep;
    accum = 0.0;
    t0 = time.clock();
    z = np.random.normal(size = [numSim, numStep]);
    for i in range(numSim):
        s = S0;
        for j in range(numStep):
            s = s * exp((r - 0.5*sig**2)*dt + sig*sqrt(dt)*z[i, j]);
        payoff = max(s - E, 0);
        accum = accum + payoff;
    call = exp(-r * T) * (accum / numSim);
    t1 = time.clock();
    
    print 'version 1' 
    print 'Call Price : %.5f' % call
    print 'CPU time in Python(sec) : %.4f' % (t1-t0)
    
def mc_call_vec2(S0, E, T, r, sig, numSim, numStep):
    dt = T / numStep;
    t0 = time.clock();
    z = np.random.normal(size = [numStep, numSim]);
    s = S0 * np.ones([numSim]);
    for i in range(numStep):
        s[:] = s[:] * np.exp((r - 0.5*sig**2)*dt + sig*sqrt(dt)*z[i, :]);
    payoff = np.maximum(s - E, 0);
    call = exp(-r * T) * np.mean(payoff);
    t1 = time.clock();
    
    print 'version 2' 
    print 'Call Price : %.5f' % call
    print 'CPU time in Python(sec) : %.4f' % (t1-t0  )

S0 = 100.0; # underlying price
E = 100.0; # strike price
T = 1.0; # maturity
r = 0.03; # riskless interest rate
sig = 0.3; # volatility
ns = 1000000;  # # of simulations
nStep = 1; # # of time steps (In this example, nStep does not have to over 1 due to European option pricing.)

# functions call
exc_call(S0, E, T, r, sig);
mc_call(S0, E, T, r, sig, ns, nStep);
mc_call_vec1(S0, E, T, r, sig, ns, nStep);
mc_call_vec2(S0, E, T, r, sig, ns, nStep);

