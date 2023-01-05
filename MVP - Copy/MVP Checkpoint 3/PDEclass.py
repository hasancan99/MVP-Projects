"""

Checkpoint 3

"""


import math as m
import numpy as np
import random
import matplotlib.pyplot as plt


class PDE(object):
    def __init__(self,a,b,kap,M,XderSq,Tder,phi):
        self.a=a
        self.b=b
        self.kap=kap
        self.M=M
        self.XderSq=XderSq
        self.Tder=Tder
        self.phi=phi
        self.a_s=len(self.phi)
        self.mew=np.zeros((self.a_s,self.a_s))
        self.newphi=np.zeros((self.a_s,self.a_s))
       
       
    def chemical_potential(self,i,j):
        """calculates the chem pot from the new phi"""
        self.mew[i,j] = -self.a*self.phi[i,j]+(self.b*(self.phi[i,j])**3)-(self.kap/self.XderSq)*(self.phi[(i+1)%self.a_s,j]+self.phi[(i-1)%self.a_s,j]+self.phi[i,(j+1)%self.a_s]\
                 +self.phi[i,(j-1)%self.a_s]-(4*self.phi[i,j]))
        #back slashes is used to continue the line from above on a different line
       
    def phiNext(self,i,j):
       """gives the next iteration of Phi"""
       self.newphi[i,j] = self.phi[i,j]+(self.M*(self.Tder/self.XderSq))*(self.mew[((i+1)%self.a_s),j]+self.mew[((i-1)%self.a_s),j] +\
                self.mew[i,(j+1)%self.a_s]+self.mew[i,(j-1)%self.a_s]-4*self.mew[i,j])
        #return
        
    def initChemical(self):
        """a function to keep the phiCal function clean""" 
        for i in range(0,self.a_s):
            for j in range(0,self.a_s):
                self.chemical_potential(i,j)
                
   
    def phiCal(self,time,runanimate):
        """Function to calculate the phi matrix and also output the free energy of each matrix"""
        self.free_Es=[] #list for the free energies throughout the simulation
        for t in range (0,time):
            self.initChemical()
            freeE=0
            for i in range(0,self.a_s):
                for j in range(0,self.a_s):
                        self.phiNext(i,j)
                        freeE+=self.free_energy(i,j)
            #print(freeE)
            self.free_Es.append(freeE)
            self.phi=self.newphi
            if t%1000==0:
                print(t)
            if str(runanimate)== "yes":
                if t>100:
                    if t%50==0:
                        self.animate(self.phi)
                        print("yes")
        return self.free_Es
        
    def file_write(self,savedfile,File_name):
        #simple write function where the function can be written in two forms 
        #the form used mainly here is the numpy text file saved
        #If error comes up then this might be due to not using the other method of writing the file
        """
        f=open(str(File_name),'w')
        for i in range(len(savedfile)):
            f.write('%d %lf\n' %(i,savedfile[i]))
        f.close()"""
        np.savetxt(str(File_name),savedfile)         #File_name can also be hardcoded in if this provideds problems
        
    def file_plot(self,xdata,ydata,title,xlabel,ylabel,label):
        """This is a plot function with all the plot variables externally inputted. """
        x=np.loadtxt(str(xdata))
        y=np.loadtxt(str(ydata))
        plt.figure()
        plt.title(str(title))
        plt.xlabel(str(xlabel))
        plt.ylabel(str(ylabel))
        plt.text(x[-70000],-7, str(label),style='italic',bbox={'facecolor': 'blue', 'alpha': 0.5, 'pad': 10} )
        plt.plot(x,y)
        plt.show()
        plt.savefig("PlotPhi0.5")
        
        
    def animate(self, array):
        """Simple Animate Function"""
        f=open('Data.dat','w')
        for i in range(len(array)):
            for j in range(len(array)):
                f.write('%d %d %lf\n'%(i,j,array[i,j]))
        f.close()
        plt.cla()
        im=plt.imshow(array, animated=True, cmap='GnBu')
        plt.draw()
        plt.pause(0.01)
    
    def free_energy(self,i,j):
        """Function to calculate the free energy for each matrix element"""
        f=-(self.a/2)*((self.phi[i,j])**2)+(self.a/4)*((self.phi[i,j])**4)+(self.kap/4.0*self.XderSq)*(((self.phi[((i+1)%self.a_s),j])-(self.phi[((i-1)%self.a_s),j]))+\
            ((self.phi[i,((j+1)%self.a_s)])-(self.phi[i,((j-1)%self.a_s)])))
        return f
       
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Phibuild(object):
    def __init__(self,a_s):
        self.a_s=a_s
       
    def arrayGen(self,phi0):
        """Function to generate an array with an input size and initial values"""
        array=np.random.choice([phi0], [self.a_s,self.a_s],[1])
        for i in range(self.a_s):
            for j in range(self.a_s):
                noise=np.random.normal()*0.01
                #print(noise)
                array[i][j]=array[i][j]+noise
        return array
    
    
