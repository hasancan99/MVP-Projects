"""Animate Function"""
from MVCP1 import Kawasaki
from MVCP1 import Glauber
import math as m
import numpy as np
from matplotlib import pyplot as plt

class Animation(object):
    def __init__(self,array,a_s,T,sweeps):
        self.a_s=a_s
        self.array=array
        self.T=T
        self.sweeps=sweeps
        
        
    def kawasaki(self):
        array_change=self.array
        for k in range (0,self.sweeps):
            array_new1=Kawasaki(array_change,self.a_s,self.T)
            array_change=array_new1.kawasaki_energy()
            if (k%10 ==0):
                f=open('kspins.dat','w')
                for i in range(self.a_s):
                    for j in range(self.a_s):
                        f.write('%d %d %lf\n'%(i,j,array_change[i,j]))
                f.close()
                plt.cla()
                im=plt.imshow(array_change, animated=True)
                plt.draw()
                plt.pause(0.0001) 
                
    def glauber(self):
        array_change=self.array
        for k in range (0,self.sweeps):
            array_new1=Glauber(array_change,self.a_s,self.T)
            array_change=array_new1.glauber_energy()
            if (k%10 ==0):
                f=open('gspins.dat','w')
                for i in range(self.a_s):
                    for j in range(self.a_s):
                        f.write('%d %d %lf\n'%(i,j,array_change[i,j]))
                f.close()
                plt.cla()
                im=plt.imshow(array_change, animated=True)
                plt.draw()
                plt.pause(0.0001) 