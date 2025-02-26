# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 10:45:02 2018

@author: Namsso
"""


#==============================
#-- Metropolis_moves
#==============================
#import random
import numpy as np
from math import exp, log, sqrt
from time import strftime

def Metmoves(x,k1,fvalue,hist,Q):
    
    #y=x
    #k=k1
    #fvalue
    #hist
    #Q
    
    maxx = 0
    minn = 1000
    BTHETA = 10^20
    
    un = np.random.uniform(low=0.0, high=1.0, size=None)
    temp_sum = Q[x-1][0]
    
    z = 1    
    while un>temp_sum and z<10 :
        z = z+1
        temp_sum = temp_sum + Q[x-1][z-1]
        
    if fvalue[z-1]==200 :
        k3 = 1
    elif fvalue[z-1]==100 :
        k3 = 2
    elif fvalue[z-1]==3 :
        k3 = 3
    elif fvalue[z-1]==2 :
        k3 = 4 
    else :
        k3 = 5

    
    ##p(x)=1
    r = 1.0*exp(hist[k1-1][1]-hist[k3-1][1])*(1/1)*(Q[z-1][x-1]/Q[x-1][z-1])

    if r > 1.0 :
        accept = 1
    else :
        un = np.random.uniform(low=0.0, high=1.0, size=None)
        if un < r :
            accept = 1
        else :
            accept = 0
    
    
    if accept == 1 :
        for i in range(0,NE) :
            if i == k3-1 :
                hist[i][1] = hist[i][1] + 1.0*GAMMA*(1.0-STPI[i])
            else :
                hist[i][1] = hist[i][1] - 1.0*GAMMA*STPI[i]

        hist[k3-1][2] = hist[k3-1][2] + 1.0
        x = z
        k1 = k3   
    else :
        for i in range(0,NE) :
            if i == k1-1 :
                hist[i][1] = hist[i][1] + 1.0*GAMMA*(1.0-STPI[i])
            else :
                hist[i][1] = hist[i][1] - 1.0*GAMMA*STPI[i]

        hist[k1-1][2] = hist[k1-1][2] + 1.0
        

    for i in range(0,NE):
        if hist[i][1] > maxx : maxx = hist[i][1]
        if hist[i][1] < minn : minn = hist[i][1]

    
    if maxx > BTHETA :
        for i in range(0,NE):
            hist[i][1] = hist[i][1] + BTHETA/2.0 - maxx
    
    
    if minn < -BTHETA :
        for i in range(0,NE):
            hist[i][1] = hist[i][1] - BTHETA/2.0 - minn
    
    
    y = x
    k = k1
    
    RESULT = y,k,fvalue,hist
    return RESULT



#==============================
#-- Main Program
#==============================

# set parameter
Nrep = 1
Niter = 500000
N = 10
NE = 5
t0 = 10.0
weight = [1,1,2,2,4]


# Generate paramters
fvalue = [] 
hist = np.zeros((NE,3))
Q = np.zeros((10,10))
FV = []
STPI = []


# Mass function
fvalue = [1, 100, 2, 1, 3, 3, 1, 200, 2, 1]  


# Desired sampling distribution
for i in range(0,NE):
    STPI.append(1.0/NE)


# Proposal distribution
fin = 'C://Users//Namsso//Desktop//남소희//스터디 자료//SAMC//Q.csv'
delim = ','

data = []
for line in open(fin, "r"):
    line_items = line.strip().split(delim)
    data.append(line_items)

for i in range(0,10):
    for j in range(0,10):
        Q[i][j] = float(data[i][j])


# Initialize weight
# hist[,2]=theta [theta=log(g) / g=exp(theta)]
for i in range(0,NE):
    hist[i][0] = i+1
    hist[i][2] = 0.0

hist[0][1] = hist[1][1] = log(1)
hist[2][1] = hist[3][1] = log(2)
hist[4][1] = log(4)


# Parameter for the visiting probability of each subset
for i in range(0,N):
    FV.append(0.0)


# Generate subset randomly x => k1
x = 11
while x>10:
    x=round(np.random.uniform(low=0.1, high=1.0, size=None)*10)

if fvalue[x-1]==200: 
    k1 = 1
elif fvalue[x-1]==100:
    k1=2
elif fvalue[x-1]==3:
    k1=3
elif fvalue[x-1]==2:
    k1=4
else:
    k1=5    


# Run MH step 5x10^5 times : 9~11초
for iter in range(1,Niter+1):
    GAMMA = (t0/max(t0,iter))**1.0
    fv = Metmoves(x,k1,fvalue,hist,Q)
    x = fv[0]
    k1 = fv[1]
    fvalue = fv[2]
    hist = fv[3]
    
    FV[x-1] = FV[x-1] + 1.0
    statement = ["Done ", " iterations", " : GAMMA "]
    if iter/1000 == iter//1000:
       print(statement[0] + str(iter) + statement[1] + statement[2] + str(GAMMA))
  


# Check for convergence of estimated sampling distribution
temp_sum = 0.0
for i in range(0,NE):
    if hist[i,2] != 0:
       temp_sum = temp_sum + hist[i,2]

msum = int(1.0*temp_sum/NE)

for i in range(0,NE):
    if hist[i,2] != 0:
       hist_result = int(hist[i,0]), hist[i,1], exp(hist[i,1]), int(hist[i,2]), hist[i,2]/temp_sum, (hist[i,2]/msum)*100.0
       print(hist_result)

temp_sum = 0.0
for i in range(0,N):
    temp_sum = temp_sum + FV[i]
    
for i in range(0,N):
    fv_result = i+1, fvalue[i], 1.0*FV[i]/temp_sum
    print(fv_result)


# Check for convergence of estimated weight
temp_sum = 0.0
for i in range(0,NE):
    if hist[i,2] != 0:
       temp_sum = temp_sum + ((exp(hist[i,1])-weight[i])**2) / weight[i]

print("Estimation Error of g(gain factor) = " + str(sqrt(temp_sum)))




    