"""Main for checkpoint 3"""
import numpy as np
import math as m
import matplotlib.pyplot as plt 
from InitialValue import InitialValue
from InitialConditions import InitialConditions
from BoundaryValue import BoundaryValue
import sys
duration=5000
freq=500
np.set_printoptions(1000) #threshold=sys.maxsize
def main():
    x=InitialConditions(50)
    #FreeEnergyDensity(x)
    #JacobiPoisson(x)
    #GaussSiedel(x)
    #JacobiMagnetic(x)
    #Relax(x)
    Plot()
    
#------------------------------------------------------------------------------
#function to calculate free energy density from Initial value problem 
def FreeEnergyDensity(x):
    initial=x.IVP(0.5) #setups up intial matrix, the 0.5 can be changed to 0.0 to check the other condition
    y=InitialValue(initial,1,1,0.1,0.1,0.1,0.1) #(dx,dt,M,a,b,k)
    #y.FreeEnergy() #calls functions to calculate free energy 
    y.animate(300000)
    
#------------------------------------------------------------------------------
#function to Solve Poisson equation with Jacobi method
def JacobiPoisson(x):
    density=x.SingleCharge(50)
    x2=BoundaryValue(density,1.0,1.0)
    x2.JacobiSolve(-3.0) #call function to solve the poisson equation
    x2.Quantitative() #calls function to calculate and plot distance v potential and distance v electric field 
    #x2.Read() #function to plot contour vector plots 
    
#------------------------------------------------------------------------------
# function to solve poisson equation via Gauss Siedel 
def GaussSiedel(x):
    density=x.SingleCharge(50)
    x3=BoundaryValue(density,1.0,1.0)
    x3.GaussSeidelSolve(-3)
    #x3.Read() #function to plot contour and vector plots

#------------------------------------------------------------------------------
#function to solve problem of single wire runing through centre and parallel to z axis 
def JacobiMagnetic(x):
    wire=x.SingleWire(50)
    x4=BoundaryValue(wire,1.0,1.0)
    x4.Magnetisation(-3.0)
    x4.Quantitative()
    #x4.Read()

#------------------------------------------------------------------------------
#function to do SOR relaxation method 
def Relax(x):
    density=x.SingleCharge(50)
    x5=BoundaryValue(density,1.0,1.0)
    x5.Relaxation(3.0)
#------------------------------------------------------------------------------
#function to plot the SOR data 
def Plot():
    x=np.loadtxt("wlistPoisson")
    y=np.loadtxt("LoopsPoisson")
    plt.figure()
    plt.title("SOR")
    plt.xlabel("w")
    plt.ylabel("Time")
    plt.scatter(x,y)
    plt.show()
    

    
    
    
    

            
    
        
main()

    
    
    
    
    
    
    
