# -*- coding: utf-8 -*-
"""
ELS 1-asset by Monte Carlo simulation 

@author: Minhyun Yoo
"""
import time
import numpy as np
from math import exp, sqrt, ceil

S0 = 100.0; # underlying price
T = 3.0; # maturity
r = 0.03; # riskless interest rate
discr = 0.03; # discount rate
sig = 0.3; # volatility
ns = 10000;  # # of simulations
dateConv = 360; # 1 year
nStep = int(dateConv * T); # # of time steps

Kib = 60.0; # knock in barrier
cpy = 0.03; # coupon per year
dummy = cpy*T; # dummy
face = 10000.0; # face value
B = [90.0, 90.0, 85.0, 85.0, 80.0, 80.0]; # early redemption barrier
numExercise = len(B);
obsDate = np.array([ceil(nStep / numExercise), ceil(2.0*nStep/numExercise), ceil(3.0*nStep/numExercise),
           ceil(4.0*nStep / numExercise), ceil(5.0*nStep / numExercise), ceil(nStep)]); # observation dates
payment = face*(1.0+np.array([cpy*0.5, cpy*1.0, cpy*1.5, cpy*2.0, cpy*2.5, cpy*3.0])); # payment

dt = T / nStep; # time step
t0 = time.clock();

sumPayoff = 0.0;
idx = np.zeros(numExercise);

drift = (r - 0.5*sig**2)*dt;
sigsqdt = sig*sqrt(dt);

# simulation loop
for i in xrange(ns):
    s = S0; kievent = False; tag = False;
    cnt1 = 0; cnt2 = 0;
    payoff = 0.0; idx[:] = 0.0;
    
    # random number
    z = np.random.normal(size = [nStep]);
    # generating path
    for j in xrange(nStep):
        s = s * exp(drift + sigsqdt*z[j]);
        
        # check hitting knock in barrier
        kievent = True if s < Kib else kievent;
        
        # save the underlying price at observation dates
        if ((j+1) == obsDate[cnt1]):
            idx[cnt1] = s;
            cnt1 += 1;
            
    # check for early redemption        
    for k in xrange(numExercise):
        if (idx[k] >= B[k]):
            payoff = payment[k];
            tag = True;
            cnt2 = k;
            break;
            
    if (tag == False):
        payoff = 100.0 * s; # loss
        if (kievent == False):
            if (s >= Kib):
                payoff = face * (1.0 + dummy); # dummy
    sumPayoff += payoff * exp(-discr * obsDate[cnt2] / dateConv);   

# mean
els1 = sumPayoff / ns;
t1 = time.clock();
del z;
    
print 'Monte Carlo Call Price : %.5f' % els1
print 'CPU time in Python(sec) : %.4f' % (t1-t0)