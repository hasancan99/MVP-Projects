"""MVCH1 Run code"""

from MVCP1 import SpinArray
from MVCP1 import Glauber
from MVCP1 import Kawasaki
from Animate import Animation
from magnitisation import Magni_and_Energy

import math as m
import numpy as np
from matplotlib import pyplot as plt



def main():
    array_size=50 #int(input("What is your array size? "))       #These are the inputs of the code
    arraygen=SpinArray(array_size)
    array= arraygen.arrays()
    T=1 #float(input("What is the temperature? "))
    sweeps=10100 #int(input ("What is the number of sweeps? "))
    Templist=np.arange(1,3,0.1)
    TemplistSQR=np.power(Templist,2)
    print(int((sweeps-100)/10))
    
    
    dynamics= input ("Which dynamics do you want to be run? ")
    if (dynamics == "k"):
        #kaw=Kawasaki(array, array_size,T)
        #array_kaw=kaw.kawasaki_energy()
        print("hi")
        #mag=Magni_and_Energy()
        #average_magnitisations,average_energys= mag.averages_Kaw(array_size,sweeps,Templist)
        #np.savetxt("Magnetisation_DataK2",average_magnitisations)
        #np.savetxt("Energy_DataK2",average_energys)
        animate=Animation(array, array_size,T,sweeps)
        animate.kawasaki()
        Mag_DataK=np.loadtxt("Magnetisation_DataK")
        avMag,sqravMag=mag.Averages(Mag_DataK)
        Eng_DataK=np.loadtxt("Energy_DataK")
        avEng,sqravEng=mag.Averages(Eng_DataK)
        absMag=np.absolute(avMag)
        print (len(avMag))
        dataCap=mag.Calc(avEng,sqravEng,array_size,TemplistSQR)
        data=mag.Calc(avMag,sqravMag,array_size,Templist)
        
        plt.figure()
        plt.xlabel("Temp")
        plt.ylabel("Absolute Average Energy")
        plt.plot(Templist,avEng)
        plt.savefig("Kawasaki Av Energy(absolute) against Temp")
        plt.show()
        
        plt.figure()
        plt.xlabel("Temp")
        plt.ylabel("Absolute Average Magnetisation")
        plt.plot(Templist,absMag)
        plt.savefig("Kawasaki Average_Magnetisation(absolute) against Temp")
        plt.show()
        
        plt.figure()    #this part plots the susceptability data against T
        plt.xlabel("Temp")
        plt.ylabel("Susceptability")
        plt.plot(Templist,data)
        plt.savefig("Kawasaki Susceptability")
        plt.show()
        
        plt.figure()
        plt.xlabel("Temp")
        plt.ylabel("Heat Cap")
        plt.plot(Templist,dataCap)
        plt.savefig("Kawasaki Heat Capacity against Temp")
        plt.show()
        
        
    if (dynamics == "g"):
        glauber=Glauber(array,array_size,T)
        array_gla=glauber.glauber_energy()
        #mag=Magni_and_Energy()
        #average_magnitisations,average_energys =mag.averages_Gla(array_gla,array_size,sweeps,Templist)
        #print(average_magnitisations,average_energys)
        #np.savetxt("Magnetisation_DataG",average_magnitisations)
        #np.savetxt("Energy_DataG",average_energys)
        animate=Animation(array, array_size,T,sweeps)
        animate.glauber()
        Mag_DataG=np.loadtxt("Magnetisation_DataG")
        avMag,sqravMag=mag.Averages(Mag_DataG)
        Eng_DataG=np.loadtxt("Energy_DataG")
        avEng,sqravEng=mag.Averages(Eng_DataG)
        absMag=np.absolute(avMag)
        print (len(avMag))
        dataCap=mag.Calc(avEng,sqravEng,array_size,TemplistSQR)
        data=mag.Calc(avMag,sqravMag,array_size,Templist)
        
        
        
        plt.figure()
        plt.xlabel("Temp")
        plt.ylabel("Glauber Absolute Average Magnetisation")
        plt.plot(Templist,absMag)
        plt.savefig("Average_Magnetisation(absolute) against Temp")
        plt.show()
        
        plt.figure()    #this part plots the susceptability data against T
        plt.xlabel("Temp")
        plt.ylabel("Glauber Susceptability")
        plt.plot(Templist,data)
        plt.savefig("Susceptability")
        plt.show()
        
        plt.figure()
        plt.xlabel("Temp")
        plt.ylabel("Heat Cap")
        plt.plot(Templist,dataCap)
        plt.savefig("Glauber Heat Capacity against Temp")
        plt.show()
        
        
    else:
        print ("No such dynamics system")
    
    
    


 

main()



