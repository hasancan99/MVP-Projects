"""Class to solve Initial Value Problems PDE"""
import numpy as np
import math as m
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from line_profiler import LineProfiler
class InitialValue(object):
    def __init__(self,matrix,dx,dt,M,a,b,k):
        self.matrix=matrix
        self.size=len(matrix)
        self.M=M
        self.dx=dx
        self.dt=dt
        self.a=a
        self.b=b
        self.k=k
        self.EquationM=np.zeros((self.size,self.size))
        self.NewC=np.zeros((self.size,self.size))
       
#------------------------------------------------------------------------------
#Function to calculate mu at a given element 
    def InitEquation(self,i,j):
        mu=(-self.a*self.matrix[i,j])+(self.b*(self.matrix[i,j])**3)-((self.k/(self.dx)**2)*(self.matrix[(i+1)%self.size,j]
                    +self.matrix[(i-1)%self.size,j]+self.matrix[i,(j+1)%self.size]+self.matrix[i,(j-1)%self.size]-(4*self.matrix[i,j])))
        return mu
               



#------------------------------------------------------------------------------
# Function to apply one timestep        
    def Update(self):
        for i in range(self.size): #first for loop updates the whole mu field, so it can be used to calculate phi
            for j in range(self.size):
                self.EquationM[i,j]=self.InitEquation(i,j)
        for i in range(self.size): # for loop updates elements in new array from elements in current array
            for j in range(self.size):
               
                self.NewC[i,j]=self.matrix[i,j]+((self.M*(self.dt/(self.dx)**2))*(self.EquationM[(i+1)%self.size,j] \
                    +self.EquationM[(i-1)%self.size,j]+self.EquationM[i,(j+1)%self.size]+self.EquationM[i,(j-1)%self.size]-(4*self.EquationM[i,j])))
               
 
               
               
                #print(self.matrix[i,j])
        return self.NewC

#------------------------------------------------------------------------------
# another function to animate with colorbar and contours, the other animate function was used in the checkpoint 
    def AnotherAnimate(self,duration):
        plt.figure()
        plt.ion()
        for l in range(duration):
            self.matrix=self.Update()
            if l%100==0:
                plt.clf()
                plt.subplot()
                plt.contourf(self.matrix,vmin=-1.0,vmax=1.0)
                plt.colorbar()
                plt.draw()
                plt.pause(0.01)
                
#------------------------------------------------------------------------------
#function to animate
    def animate(self,duration):
        plt.figure()
        for l in range(0,duration):
            self.matrix=self.Update()
            if l%100==0:
                f=open('INIT','w')
                for q in range(0,self.size):
                    for u in range(0,self.size):
                        f.write('%d %d %lf\n'%(q,u,self.matrix[q,u]))
                f.close()
                plt.cla()
                im=plt.imshow(self.matrix,animated=True)
                plt.draw()
                plt.pause(0.01)
                
#------------------------------------------------------------------------------
#Function to calculate free energy density after each update
           
    def FreeEnergy(self):
        time=[]
        FList=[]
        for k in range(300000):
            print (k)
            self.matrix=self.Update()
            f=0
            for i in range(self.size):
                for j in range(self.size):
                    f+=((-self.a/2.0)*(self.matrix[i,j]**2))+((self.a/4.0)*(self.matrix[i,j]**4))+((self.k/2)*(((1/(2.0*self.dx))*(self.matrix[(i+1)%self.size,j]-self.matrix[(i-1)%self.size,j]))**2\
                         +((1/(2.0*self.dx))*(self.matrix[i,(j+1)%self.size]-self.matrix[i,(j-1)%self.size]))**2.0))
            FList.append(f)
            time.append(k)

        f=open("FREEENERGY(5)",'w')
        for i in range(len(time)):
            f.write('%d %lf\n' %(i,FList[i]))
        f.close()
        np.savetxt("FE0",FList)
        np.loadtxt("FETime",time)
        self.Plot()
            
        
#------------------------------------------------------------------------------
#function to plot the free energy density data
    def Plot(self):
        x=np.loadtxt("FETime")
        y=np.loadtxt("FE0")
        plt.figure()
        plt.title("Free Energy Density vs Time phi=0.0")
        plt.xlabel("Time")
        plt.ylabel("Free Energy Density")
        plt.plot(x,y)
        plt.show()
            
        

        
                
                
    