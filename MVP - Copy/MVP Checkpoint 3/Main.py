"""Checkpoint 3

Main

"""
import numpy as np
from PDEclass import Phibuild
from PDEclass import PDE


def main():
    NumberOfRuns=300000
    np.savetxt("TimeData",list(range(NumberOfRuns)))
    #--------------------------------------------------------------------------
    #Below are the input parameters
    a=0.1
    b=0.1
    kap=0.1
    M=0.1
    XderSq=1
    Tder=1
    phi0=0.5
    #--------------------------------------------------------------------------
    phi=Phibuild(50).arrayGen(float(phi0))    #array gen input determines whether phi naught is =0 or =0.5
    pde=PDE(a,b,kap,M,XderSq,Tder,phi)
    
    animate=("no") # this could be "yes" if animation was wanted
    
    #freeEs=pde.phiCal(NumberOfRuns,animate)
    #filename=("FreeEnergyPhi=0.5(2nd Take)")
    #pde.file_write(freeEs,filename)
    pde.file_plot(("TimeData"),("FreeEnergyPhi=0.5"),("Free Energy against Time Phi {}".format(float(phi0))),("Time"),\
                  ("Free Energy"),("phi=:{}".format(float(phi0))))
    #pde.file_plot(("TimeData"),("FreeEnergyPhi=0"),("Free Energy against Time Phi {}".format(float(phi0))),("Time"),\
     #             ("Free Energy"),("phi=:{}".format(float(phi0))))
    
    
   
   
main()
