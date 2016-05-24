# -*- coding: utf-8 -*-
"""
ELS 1-asset by Monte Carlo simulation 

test for vectorized calculation

@author: Minhyun Yoo
"""
import time
import numpy as np
from math import sqrt, ceil

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

# vectorization
s = S0 * np.ones([ns]); 
kievent = np.zeros([ns], dtype = 'bool'); 
tag = np.zeros([ns], dtype = 'bool'); 
cnt1 = 0; 
cnt2 = -1.0*np.ones([ns]); # -1 : trick for 1st eary redemption
payoff = np.zeros([ns]); 
idx = np.zeros([ns, numExercise]);
sp1 = np.zeros([ns, nStep]);

# random number
z = np.random.normal(size = [ns, nStep]);

# generating time steps
for i in xrange(nStep):
    s[:] = s[:] * np.exp(drift + sigsqdt*z[:, i]);
    
    # check hitting knock in barrier by logical operator
    kievent = kievent | (s < Kib); 
    
    # save the underlying price at observation dates
    if ((i+1) == obsDate[cnt1]):
        idx[:, cnt1] = s[:];
        cnt1 += 1;

# check for early redemption
for j in xrange(numExercise):
    #(bool set) chk1: aboce barrier & not exercised 
    chk1 = (idx[:,j] >= B[j]) & (cnt2==-1.0);
    
    # save index of observation dates at cnt2
    cnt2[chk1] = j;
    
    # determine payoff 
    payoff[chk1] = payment[j];

#(bool set) chk2: not exercised & hit knock in barrier
chk2 = (cnt2 == -1.0) & (kievent == True);

# determine payoff - loss
payoff[chk2] = 100.0 * s[chk2]; 

#(bool set) chk3: not exercised & not hit Kib & above Kib
chk3 = (cnt2 == -1.0) & (kievent == False) & (s >= Kib);

# determine payoff - dummy
payoff[chk3] = face * (1.0 + dummy);

# discount using index of observation dates
cnt2[(cnt2 == -1.0)] = numExercise-1;
cnt2 = cnt2.astype(int);
payoff = payoff * np.exp(-discr * obsDate[cnt2] / dateConv);

# mean
els1 = np.mean(payoff);

t1 = time.clock();
del z;

print 'Monte Carlo Call Price : %.5f' % els1
print 'CPU time in Python(sec) : %.4f' % (t1-t0)