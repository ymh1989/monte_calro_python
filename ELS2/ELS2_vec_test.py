# -*- coding: utf-8 -*-
"""
ELS 2-asset by Monte Carlo simulation 

test for vectorized calculation

@author: Minhyun Yoo
"""
import time
import numpy as np
from math import sqrt, ceil

S0_1 = 100.0;
S0_2 = 100.0; # underlying price 1, 2
r1 = 0.03;
r2 = 0.03; # riskless interest rate 1, 2
sig1 = 0.3;
sig2 = 0.3; # volatility 1, 2
rho = 0.5; # correlation
T = 3.0; # maturity
discr = 0.03; # discount rate
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

drift1 = (r1 - 0.5*sig1*sig1)*dt;
sigsqdt1 = sig1*sqrt(dt);
drift2 = (r2 - 0.5*sig2*sig2)*dt;
sigsqdt2 = sig2*sqrt(dt);

# vectorization
s1 = (S0_1 * np.ones([ns])); 
s2 = (S0_2 * np.ones([ns])); 
wp = np.zeros([ns]);
kievent = np.zeros([ns], dtype = 'bool'); 
tag = np.zeros([ns], dtype = 'bool'); 
cnt1 = 0; 
cnt2 = -1.0*np.ones([ns]); # -1 : trick for 1st eary redemption
payoff = np.zeros([ns]); 
idx = np.zeros([ns, numExercise]);

# random number
mat =  np.matrix([[1, rho],[rho, 1]]); # correlation matrix
chol = np.linalg.cholesky(mat); # cholesky decomposition - lower matrix
z = np.matrix(np.random.normal(size = [2, ns * nStep]));
z = chol * z; # correlated random number
# generating time steps
tmpIdx = np.arange(ns);
for i in xrange(nStep):
    s1[:] = np.multiply(s1[:], np.exp(drift1 + sigsqdt1*z[0, (ns*i)+tmpIdx]));
    s2[:] = np.multiply(s2[:], np.exp(drift2 + sigsqdt2*z[1, (ns*i)+tmpIdx]));
    
    # worst perfomer
    wp = np.min([s1, s2], axis = 0);
    
    # check hitting knock in barrier by logical operator
    kievent = kievent | (wp < Kib); 
    
    # save the underlying price at observation dates
    if ((i+1) == obsDate[cnt1]):
        idx[:, cnt1] = wp;
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
payoff[chk2] = 100.0 * wp[chk2]; 

#(bool set) chk3: not exercised & not hit Kib & above Kib at maturity
chk3 = (cnt2 == -1.0) & (kievent == False) & (wp >= Kib);

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