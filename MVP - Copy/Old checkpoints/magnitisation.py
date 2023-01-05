"""Class for magnitisation of the lattice"""
import math as m
import numpy as np
import matplotlib.pyplot as plt
from time import time 
from MVCP1 import Kawasaki
from MVCP1 import SpinArray
from MVCP1 import Glauber


class Magni_and_Energy(object):
    
    def __init__(self):
        nothing=0
        
    def energy_sum(self,array,i,j,a_s):                          #use these conditions for the energy sum to not over count in the total average energies
        control=array[i][j]
        if i+1> (a_s-1):
            e1=((-1)*control*array[0][j])
        else:
            e1 =((-1)*control*array[i+1][j])
        if i-1< 0:
            e2 =((-1)*control*array[(a_s)-1][j])
        else:
            e2=((-1)*control*array[i-1][j])
        energy_sum=e1+e2
        return (energy_sum)
    
    
        
    def averages_Kaw(self,a_s,sweeps,Templist):
        s=int((sweeps-100)/10)
        x=len(Templist)
        Mag_data=np.zeros(shape=(x,s))
        Energy_data=np.zeros(shape=(x,s))
        half_a=np.ones(((a_s),(a_s//2)))
        array=np.concatenate((half_a,-half_a),axis=1)
        
        
        for l in range (0,len(Templist)):
            #arraygen=SpinArray(a_s)                  #generates a random array for the start of each T value
            #array= arraygen.arrays()
            array_new=array
            T=Templist[l]
            m=-1
            
            
            for k in range (0,sweeps):
                
                array_new1=Kawasaki(array_new,a_s,T)
                array_new=array_new1.kawasaki_energy()
                

                energy_sum=0
                magni_sum=0
                if (k >= 100):
                    if (k%10 ==0):
                        m+= 1
                        for i in range (0,a_s-1):
                            for j in range(0,a_s-1):
                                energy_sum+=self.energy_sum(array_new,i,j,a_s)
                                magni_sum+= float(array_new[i][j])
                                print(magni_sum)
                        
                        print(k,l)
                        Mag_data[l][m]=magni_sum
                        Energy_data[l][m]=energy_sum
                
        return Mag_data, Energy_data
        
                
    
    def averages_Gla(self,array,a_s,sweeps,Templist):
        s=int((sweeps-100)/10)
        x=len(Templist)
        Mag_data=np.zeros(shape=(x,s))
        Energy_data=np.zeros(shape=(x,s))
        print(Mag_data,Energy_data)
        array_new=array
        for l in range (0,len(Templist)):
            T=Templist[l]
            m=-1
            for k in range (0,sweeps):
                array_new1=Glauber(array_new,a_s,T)                                     
                array_new=array_new1.glauber_energy()                              #this gets an array back from the Glauber method after putting in the initial input array
                energy_sum=0
                magni_sum=0
                if (k >=100):
                    
                    if (k%10 ==0):
                        m+= 1
                        for i in range (0,a_s-1):
                            for j in range(0,a_s-1):
                                energy_sum+=self.energy_sum(array_new,i,j,a_s)
                                magni_sum+= float(array_new[i][j])
                        print(magni_sum,k,l,m)
                        Mag_data[l][m]=magni_sum
                        #print (Mag_data)
                        Energy_data[l][m]=energy_sum
        return Mag_data, Energy_data                
    
    
    
    
    def Averages(self,text):
        data=(text)
        #Templeng=len(data)
        #listleng=len(data[0])
        averages=np.mean(data,axis=1)
        data_squared=np.power(data,2)
        print(data_squared)
        squared_averages=np.mean(data_squared,axis=1)
        print(squared_averages)
        #averages=np.zeros(shape=(listleng))
        #squared_averages=np.zeros(shape=(listleng))
        #for i in range(Templeng):
         #   sums=0
          #  sumsSquared=0
           # for j in range(listleng):
            #    sums+= data[i][j]
             #   sumsSquared+= ((data[i][j])**2)
            #averages[i]=(sums/listleng)
            #squared_averages[i]=(sumsSquared/listleng)
        return averages,squared_averages
    
    def Calc(self,avs,sqravs,Const,Tconst):
        Tleng=len(Tconst)
        returndata=np.zeros(shape=(Tleng))
        
        for i in range(Tleng):
            
            returndata[i]=(1/((Const)*Tconst[i]))*(sqravs[i]-((avs[i])**2))
        return returndata
        

