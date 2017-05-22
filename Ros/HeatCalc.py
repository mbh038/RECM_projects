# -*- coding: utf-8 -*-
"""

Ros's project


Created on Thu Apr 27 11:17:56 2017
@author: mbh
"""

def plotQ(dTlist=[10,20,30,40,50]):
    plt.plot([Q(10,x) for x in dTlist])

def QdT(P):
    
    c=4138 #J/kg/K = specific heat capacity of water
    rho=1000 #kg/m3
    
    return (10**6)*P/(rho*c)

