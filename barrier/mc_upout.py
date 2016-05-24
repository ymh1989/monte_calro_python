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

def exc_upout(S0, E, H, Rebate, T, r, sig):
    # Assume zero dividend
    eta = -1.0; phi = 1.0;
        
    mu = (r - 0.5*sig*sig) / (sig*sig);
    lamb = sqrt(mu*mu + 2.0*r/(sig*sig));
    z = log(H/S0)/(sig*sqrt(T)) + lamb*sig*sqrt(T);
    
    x1 = (log(S0/E) / (sig*sqrt(T))) + (1.0+mu)*sig*sqrt(T);
    x2 = (log(S0/H) / (sig*sqrt(T))) + (1.0+mu)*sig*sqrt(T);
    y1 = (log(H*H/(S0*E)) / (sig*sqrt(T))) + (1.0+mu)*sig*sqrt(T);
    y2 = (log(H/S0) / (sig*sqrt(T))) + (1.0+mu)*sig*sqrt(T);
    
    A = ( phi*S0 * stats.norm.cdf(phi*x1) 
        - phi*E*exp(-r*T) * stats.norm.cdf(phi*(x1 - sig*sqrt(T))) );
        
    B = ( phi*S0 * stats.norm.cdf(phi*x2) 
        - phi*E*exp(-r*T) *stats.norm.cdf(phi*(x2 - sig*sqrt(T))) );
        
    C = ( phi*S0 * ((H/S0)**(2*(1.0+mu))) * stats.norm.cdf(eta*y1) 
        - phi*E*exp(-r*T) * ((H/S0)**(2.0*mu)) * stats.norm.cdf(eta*(y1 - sig*sqrt(T))) );
        
    D = ( phi*S0 * ((H/S0)**(2*(1.0+mu))) * stats.norm.cdf(eta*y2) 
        - phi*E*exp(-r*T) * ((H/S0)**(2.0*mu)) * stats.norm.cdf(eta*(y2 - sig*sqrt(T))) );
    
    F = Rebate *( ((H/S0)**(mu+lamb)) * stats.norm.cdf(eta*z) 
            + ((H/S0)**(mu-lamb))*stats.norm.cdf(eta*(z-2.0*lamb*sig*sqrt(T))));
    
    upout = A - B + C - D + F;    
    
    print'Exact up&out Price : %.5f' % upout;
    
def mc_upout_vec(S0, E, B, T, r, sig, numSim, numStep):
    dt = T / numStep;
    t0 = time.clock();
    z = np.random.normal(size = [numStep, numSim]);
    s = S0 * np.ones([numSim]);
    tag = np.zeros((numSim), dtype=bool);
    for i in xrange(numStep):
        s[:] = s[:] * np.exp((r - 0.5*sig**2)*dt + sig*sqrt(dt)*z[i, :]);
        idx = s > B;
        tag += idx;
    
    payoff = np.maximum(s - E, 0);
    payoff[tag] = 0.0;
    upout = exp(-r * T) * np.mean(payoff);
    t1 = time.clock();
    del z;
    
    print 'Monte Carlo Call Price : %.5f' % upout
    print 'CPU time in Python(sec) : %.4f' % (t1-t0)
    
def mc_upout(S0, E, B, T, r, sig, numSim, numStep):
    dt = T / numStep;
    t0 = time.clock();
    z = np.random.normal(size = [numSim, numStep]);
    sumPayoff = 0.0;
    for i in xrange(numSim):
        s = S0; tag = False;
        for j in xrange(numStep):
            s = s * np.exp((r - 0.5*sig**2)*dt + sig*sqrt(dt)*z[i, j]);
            if (s > B):
                tag = True;
                break;
        if (tag):
            payoff = 0.0;
        else:
            payoff = max(s - E, 0);
        sumPayoff += payoff;
    
    upout = exp(-r * T) * sumPayoff / ns;
    t1 = time.clock();
    del z;
    
    print 'Monte Carlo Call Price : %.5f' % upout
    print 'CPU time in Python(sec) : %.4f' % (t1-t0)

S0 = 100.0; # underlying price
E = 100.0; # strike price
Ko = 130.0;
Rebate = 0.0;
T = 1.0; # maturity
r = 0.03; # riskless interest rate
sig = 0.3; # volatility
ns = 100000;  # # of simulations
dateConv = 360; # 1 year
nStep = int(dateConv * T); # # of time steps

# functions call
exc_upout(S0, E, Ko, Rebate, T, r, sig); # exact solution
mc_upout_vec(S0, E, Ko, T, r, sig, ns, nStep); # Monte Carlo simulation
# mc_upout(S0, E, Ko, T, r, sig, ns, nStep);