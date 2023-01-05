""" Checkpoint 2 MVP"""
"""Main function"""
import math as m
import numpy as np
import matplotlib.pyplot as plt
from Classes import RulesGoL



def main():
    array_size=50
    steps=1000
    array=np.random.choice([1,0], [array_size,array_size],[0.5,0.5])     #creates a random array of 1s and minus 1s
    #i,j=(np.random.randint(0,array_size)),(np.random.randint(0,array_size))
    glider_array=np.random.choice([0,0], [array_size,array_size],[0,1])
    glider_array[2][1],glider_array[2][0],glider_array[2][2],glider_array[1][2],glider_array[0][1]=1,1,1,1,1
    oscillator_array=np.random.choice([0,0], [array_size,array_size],[0,1])
    oscillator_array[1][1],oscillator_array[2][1],oscillator_array[3][1]=1,1,1
    array=np.random.choice([1, 0, -1], [array_size,array_size],[1/3.0,1/3.0,1/3.0])     #creates a random array of 1s and minus 1s
    game=RulesGoL(array_size)
    game.interate(glider_array,steps)
    #game.interate(array,steps)
    #game.interate(oscillator_array,steps)
    #times=game.equilibriums(steps)
    #np.savetxt("Array_Size = 50 Equilibrium Times (5Consec)", times)
    
    #x=np.loadtxt("Array_Size = 50 Equilibrium Times (5Consec)")
    #x=np.loadtxt("Array_Size = 50 Equilibrium Times")
    #plt.hist(x,density=False,bins=25)
    #plt.show()
    
    CoMData=game.centreOfmass(glider_array,steps)
    np.savetxt("2nd CoM Data Array_Size = 50", CoMData)
    CoMData=np.loadtxt("3rd CoM Data Array_Size = 50")
    #print((CoMData))
    
    
    plt.figure()
    plt.scatter(CoMData[2],CoMData[0])
    plt.scatter(CoMData[2],CoMData[1])
    plt.show()
    
    game.speed()
    
    
main()