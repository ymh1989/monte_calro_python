# -*- coding: utf-8 -*-
"""
ELS 2-asset by Monte Carlo simulation 

@author: Minhyun Yoo
"""
import time
import numpy as np

from math import exp, sqrt, ceil

S0_1 = 100.0; # underlying price 1
S0_2 = 100.0; # underlying price 2
T = 3.0; # maturity
r1 = 0.03; # riskless interest rate 1
r2 = 0.03; # riskless interest rate 2
discr = 0.03;
sig1 = 0.3; # volatility 1
sig2 = 0.3; # volatility 2
rho = 0.5;
ns = 10000;  # # of simulations
dateConv = 360; # 1 year
nStep = int(dateConv * T); # # of time steps

Kib = 60.0;
cpy = 0.03;
dummy = cpy*T;
face = 10000.0;
B = [90.0, 90.0, 85.0, 85.0, 80.0, 80.0]; # early redemption barrier
numExercise = len(B);
obsDate = np.array([ceil(nStep / numExercise), ceil(2.0*nStep/numExercise), ceil(3.0*nStep/numExercise),
           ceil(4.0*nStep / numExercise), ceil(5.0*nStep / numExercise), ceil(nStep)]);
payment = face*(1.0+np.array([cpy*0.5, cpy*1.0, cpy*1.5, cpy*2.0, cpy*2.5, cpy*3.0]));

# functions call
dt = T / nStep;
t0 = time.clock();
sumPayoff = 0.0;
idx = np.zeros(numExercise);

drift1 = (r1 - 0.5*sig1**2)*dt;
drift2 = (r2 - 0.5*sig2**2)*dt;
sigsqdt1 = sig1*sqrt(dt);
sigsqdt2 = sig2*sqrt(dt);

corr = [[1.0, rho],[rho, 1.0]];
M = np.matrix(np.linalg.cholesky(corr));

for i in xrange(ns):
    s1 = S0_1; s2 = S0_2;
    kievent = False; tag = False;
    cnt1 = 0; cnt2 = 0;
    payoff = 0.0; idx[:] = 0.0;
    
    z = M * np.matrix(np.random.normal(size = [2, nStep]));
    
    for j in xrange(nStep):
        s1 = s1 * exp(drift1 + sigsqdt1*z[0, j]);
        s2 = s2 * exp(drift2 + sigsqdt2*z[1, j]);
        
        wp = min(s1, s2);
        
        kievent = True if wp < Kib else kievent;
        
        if ((j+1) == obsDate[cnt1]):
            idx[cnt1] = wp;
            cnt1 += 1;
            
    for k in xrange(numExercise):
        if (idx[k] >= B[k]):
            payoff = payment[k];
            tag = True;
            cnt2 = k;
            break;
            
    if (tag == False):
        payoff = 100.0 * wp;
        if (kievent == False):
            if (wp >= Kib):
                payoff = face * (1.0 + dummy);
    sumPayoff += payoff * exp(-discr * obsDate[cnt2] / dateConv);   

    
els1 = sumPayoff / ns;
t1 = time.clock();
del z;
    
print 'Monte Carlo Call Price : %.5f' % els1
print 'CPU time in Python(sec) : %.4f' % (t1-t0)