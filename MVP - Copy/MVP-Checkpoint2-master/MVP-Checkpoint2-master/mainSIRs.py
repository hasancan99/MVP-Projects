""" Checkpoint 2 MVP"""
"""Main function SIRS"""
import math as m
import numpy as np
import matplotlib.pyplot as plt
from Classes import SIRS

def main():
    
    array_size=(50)
    steps=10100
    
    p1=np.arange(0.0,1,0.05)
    p1vary=np.arange(0.2,0.51,0.01)
    p2=0.5
    p3=np.arange(0.0,1,0.05)
    p3const=0.5
    array=np.random.choice([1,0,-1], [array_size,array_size],p=[1/3,1/3,1/3])
    sirs=SIRS(array_size,array)
    #sirs.animateSIR(p1,p2,p3,steps)
    sirs.phase(p1vary,p2,p3,steps)
    #infected=np.loadtxt("Infected Numbers Small")
    
    #print(infected)
    #sirs.plots(steps,p1,p3)
    sirs.plotsP1varied(steps,p1,p3const)
    
    #waves params p1=0.8 p2=0.01 p3=0.1
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
main()    

