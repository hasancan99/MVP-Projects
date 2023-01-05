""" Checkpoint 1 Spin Array initialiser"""
import math as m
import numpy as np
import matplotlib.pyplot as plt
from time import time 



class SpinArray(object):
    def __init__(self,a_s):
        self.array_size=a_s

    def arrays(self):
        array=np.random.choice([1,-1], [self.array_size,self.array_size],[0.5,0.5])     #creates a random array of 1s and minus 1s
        return array
    
    


class Glauber(object):
    def __init__(self,array,a_s,T):      #takes in an array, array size which has to be N by N, and takes in random components i and j to iterate over the arrays
        self.a_s=a_s
        self.array=array
        self.T=T
#Need to add T as an input and further energy calculations to this class to make it complete 
      
    def energy(self,k,l):
        i= k
        j= l
        control=self.array[i][j]
        if i+1> (self.a_s-1):
            e1=((-1)*control*self.array[0][j])
        else:
            e1 =((-1)*control*self.array[i+1][j])
        if i-1< 0:
            e2 =((-1)*control*self.array[(self.a_s)-1][j])
        else:
            e2=((-1)*control*self.array[i-1][j])
        if j+1> (self.a_s-1):
            e3=((-1)*control*self.array[i][0])
        else:
            e3=((-1)*control*self.array[i][j+1])
        if j-1< 0:
            e4=((-1)*control*self.array[i][(self.a_s)-1])
        else:
            e4= ((-1)*control*self.array[i][j-1])
        energy_sum=e1+e2+e3+e4
        return (energy_sum)
    
    def energy_sum(self,i,j):                          #use these conditions for the energy sum to not over count in the total average energies
        control=self.array[i][j]
        if i+1> (self.a_s-1):
            e1=((-1)*control*self.array[0][j])
        else:
            e1 =((-1)*control*self.array[i+1][j])
        if i-1< 0:
            e2 =((-1)*control*self.array[(self.a_s)-1][j])
        else:
            e2=((-1)*control*self.array[i-1][j])
        energy_sum=e1+e2
        return (energy_sum)
    
    def site(self):
        i=(np.random.randint(0,self.a_s))
        j=(np.random.randint(0,self.a_s))
        return i,j
    
    def glauber_energy(self):
        for l in range(0,self.a_s*self.a_s):
            
            i, j= self.site()
            energy=self.energy(i,j)
            self.array[i][j]=-1*self.array[i][j]
            energy2=self.energy(i,j)
            e_diff=energy2-energy
            if e_diff>0 :
                r=np.random.random()
                if r > m.exp((-1*(e_diff))/self.T):
                    self.array[i][j]=-1*self.array[i][j]
                    #print ("No Flip")
        return self.array
    
        
class Kawasaki(object):
    def __init__(self, array, a_s,T):
        self.a_s=a_s
        self.array=array
        self.T=T
        
    def two_sites(self):
        i=(np.random.randint(0,self.a_s))
        j=(np.random.randint(0,self.a_s)) #This part of the code gives coords for two sites within the array 
        i2=(np.random.randint(0,self.a_s))
        j2=(np.random.randint(0,self.a_s))
        return i,j,i2,j2
    
    
    def energy(self,i,j):            #this function calculates the energy with boundary conditions in place
        control=self.array[i][j]
        t0=time()
        if i+1> (self.a_s-1):
            e1=((-1)*control*self.array[0][j])
        else:
            e1 =((-1)*control*self.array[i+1][j])
        if i-1< 0:
            e2 =((-1)*control*self.array[(self.a_s)-1][j])
        else:
            e2=((-1)*control*self.array[i-1][j])
        if j+1> (self.a_s-1):
            e3=((-1)*control*self.array[i][0])
        else:
            e3=((-1)*control*self.array[i][j+1])
        if j-1< 0:
            e4=((-1)*control*self.array[i][(self.a_s)-1])
        else:
            e4= ((-1)*control*self.array[i][j-1])
        energy_sum=e1+e2+e3+e4
        return (energy_sum)
    
    def energy_sum(self,i,j):                          #use these conditions for the energy sum to not over count in the total average energies
        control=self.array[i][j]
        if i+1> (self.a_s-1):
            e1=((-1)*control*self.array[0][j])
        else:
            e1 =((-1)*control*self.array[i+1][j])
        if i-1< 0:
            e2 =((-1)*control*self.array[(self.a_s)-1][j])
        else:
            e2=((-1)*control*self.array[i-1][j])
        energy_sum=e1+e2
        return (energy_sum)
    
    
    def kawasaki_energy(self):                  #goes N squared times 
        for l in range (0,self.a_s*self.a_s):
            i, j, i2, j2=self.two_sites()
            
            if (self.array[i][j] == self.array[i2][j2]):
                i, j, i2, j2=self.two_sites()
       
            else:
                energy=self.energy(i,j)
                self.array[i][j]=-1*self.array[i][j]
                
                energy2=self.energy(i,j)
                e_diff1=energy2-energy

                energy=self.energy(i2,j2)
                self.array[i2][j2]=-1*self.array[i2][j2]
                
                energy2=self.energy(i2,j2)
                e_diff2=energy2-energy
                energy_diff=e_diff1+e_diff2
                if energy_diff>0 :
                    r=np.random.random()
                    if r > m.exp((-1*(energy_diff))/self.T):
                        self.array[i][j]=-1*self.array[i][j]
                        self.array[i2][j2]=-1*self.array[i2][j2]
                    else:
                        pass
                else:
                    pass
        #return energy_diff
        return self.array    
    
    