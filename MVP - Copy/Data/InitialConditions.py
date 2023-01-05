"""A class to generate a matrix depending on initial conditions wanted"""
import numpy as np
import math as m
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
class InitialConditions(object):
    def __init__(self,size):
        self.size=size
#------------------------------------------------------------------------------
#this function generates a 2d random matrix
    def Random(self):
        RMatrix=np.random.choice([1,0],[self.size,self.size],[0.5,0.5])
        return RMatrix
#------------------------------------------------------------------------------
#this function generates a 2d matrix with a formation for 1 osicillator
    def Oscillator(self):
        OMatrix=np.random.choice([0,0],[self.size,self.size],[0.5,0.5])
        for i in range(20,23):
            OMatrix[i,30]=1
        return OMatrix
#------------------------------------------------------------------------------
#this function generates a 2d matrix with a formation of a glider
    def Glider(self):
        GMatrix=np.random.choice([0,0],[self.size,self.size],[0.5,0.5])
        GMatrix[1,5]=1
        GMatrix[2,5]=1
        GMatrix[3,5]=1
        GMatrix[3,4]=1
        GMatrix[2,3]=1
        return GMatrix
#------------------------------------------------------------------------------
#function to give intial condition matrix for initial value problem
    def IVP(self,a):
        Matrix=np.zeros((self.size,self.size))
        for i in range(self.size):
            for j in range(self.size):
                Matrix[i,j]=a+(np.random.normal()*0.01)
        return Matrix
#------------------------------------------------------------------------------
#function to produce a 3D matrix to represent the charge density of a single charge in the centre
    def SingleCharge(self,a):
        Matrix=np.zeros((a,a,a))
        b=int(m.ceil(a/2.0))
        Matrix[b,b,b]=1.0
        return Matrix
#------------------------------------------------------------------------------
# function to produce 3D Matrix to represent a single wire going through the centre parrallel to z axis 
    def SingleWire(self,a):
        Matrix=np.zeros((a,a,a))
        for i in range(1,a-1):
            Matrix[(a/2),(a/2),i]=1
        return Matrix 
#------------------------------------------------------------------------------
    def SingleCharge2D(self,a):
         Matrix=np.zeros((a,a))
         b=int(m.ceil(a/2.0))
         Matrix[b,b]=1.0
         return Matrix

     
