# -*- coding: utf-8 -*-
"""
European call option by Monte Carlo simulation 

test for vectorized calculation

@author: Minhyun Yoo
"""
import time
import numpy as np
from math import exp, sqrt, ceil

S0 = 100.0; # underlying price
E = 100.0; # strike price
T = 3.0; # maturity
r = 0.0165; # riskless interest rate
sig = 0.3; # volatility
ns = 10000;  # # of simulations
dateConv = 360; # 1 year
nStep = int(dateConv * T); # # of time steps

Kib = 60.0;
cpy = 0.025;
dummy = cpy*T;
face = 10000.0;
B = [95, 90, 85, 80, 75, 70];
numExercise = len(B);
obsDate = np.array([ceil(nStep / numExercise), ceil(2.0*nStep/numExercise), ceil(3.0*nStep/numExercise),
           ceil(4.0*nStep / numExercise), ceil(5.0*nStep / numExercise), ceil(nStep)]);
payment = face*(1.0+np.array([cpy*0.5, cpy*1.0, cpy*1.5, cpy*2.0, cpy*2.5, cpy*3.0]));

# functions call
dt = T / nStep;
t0 = time.clock();

sumPayoff = 0.0;
idx = np.zeros(numExercise);

drift = (r - 0.5*sig**2)*dt;
sigsqdt = sig*sqrt(dt);


s = S0 * np.ones([ns]); 
kievent = np.zeros([ns], dtype = 'bool'); 
tag = np.zeros([ns], dtype = 'bool'); 
cnt1 = 0; 
cnt2 = -1.0*np.ones([ns]); # -1 : trick for 1st eary redemption
payoff = np.zeros([ns]); 
idx = np.zeros([ns, numExercise]);
sp1 = np.zeros([ns, nStep]);
z = np.random.normal(size = [ns, nStep]);
for i in xrange(nStep):
    s[:] = s[:] * np.exp(drift + sigsqdt*z[:, i]);
    sp1[:, i] = s[:];
    kievent = kievent | (s < Kib);
      
    if ((i+1) == obsDate[cnt1]):
        idx[:, cnt1] = s[:];
        cnt1 += 1;
            
for j in xrange(numExercise):
#    if (idx[j,:] >= B[j]):
#        payoff = payment[j];
#        tag = True;
#        cnt2 = j;
#        break;
    chk1 = (idx[:,j] >= B[j]) & (cnt2==-1.0);
    cnt2[chk1] = j;
    payoff[chk1] = payment[j];

chk2 = (cnt2 == -1.0) & (kievent == True);
payoff[chk2] = 100.0 * s[chk2]; # loss

chk3 = (cnt2 == -1.0) & (kievent == False) & (s >= Kib);
payoff[chk3] = face * (1.0 + dummy);

cnt2[(cnt2 == -1.0)] = numExercise-1;
cnt2 = cnt2.astype(int);
payoff = payoff * np.exp(-r * obsDate[cnt2] / dateConv);
els1 = np.mean(payoff);
#els1 = mean()
#if (tag == False):
#    payoff = 100.0 * s;
#    if (kievent == False):
#        if (s >= Kib):
#            payoff = face * (1.0 + dummy);
#
#sumPayoff += payoff * exp(-r * obsDate[cnt2] / dateConv);   
#
#    
#els1 = sumPayoff / ns;
t1 = time.clock();
del z;
#    
print 'Monte Carlo Call Price : %.5f' % els1
print 'CPU time in Python(sec) : %.4f' % (t1-t0)