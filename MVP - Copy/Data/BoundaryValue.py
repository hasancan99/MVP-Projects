"""Class for Boundary Value Problems"""
import numpy as np 
import math as m 
import matplotlib.pyplot as plt
import copy
import scipy.interpolate
from line_profiler import LineProfiler
class BoundaryValue(object):
    def __init__(self,density,dx,ep):
        self.density=density
        self.size=len(density) #gets the length of the density matrix
        self.dx=dx #sets delta x
        self.dt=(dx**2)/4.0
        self.ep=ep
        self.potential=np.zeros((self.size,self.size,self.size)) #current potential matrix
        self.NewPotential=np.zeros((self.size,self.size,self.size)) #new potential matrix
        
#------------------------------------------------------------------------------
# function to update potential
    def JacobiUpdate(self):
        for i in range(1,self.size-1):
            for j in range(1,self.size-1):
                for k in range(1,self.size-1):
                    #calculates the new potential 
                    self.NewPotential[i,j,k]=(1.0/6.0)*(self.potential[i+1,j,k]+self.potential[i-1,j,k]
                    +self.potential[i,j+1,k]+self.potential[i,j-1,k]+self.potential[i,j,k+1]+self.potential[i,j,k-1]
                    +((self.dx)**(2)*self.density[i,j,k]))
                        
#------------------------------------------------------------------------------
##function to solve the given equation to the users choosen accuracy 
    def JacobiSolve(self,p):
        err=1 #set err initial to start while loop
        n=0 #counter to see where i am in the loop
        while err>10**(-p):
            self.JacobiUpdate() #updates the potential 
            diff=np.subtract(self.NewPotential,self.potential) #calculates difference element wise between new and old potential 
            norm=np.absolute(diff) #get the absolute value of this difference 
            err=np.sum(norm) #gets the error 
            self.potential=copy.deepcopy(self.NewPotential) #updates current potential to new potential for next iteration
            #n+=1
            #print n
        #print self.potential
        self.Data() 

#------------------------------------------------------------------------------
#function to save data to a file and calculate x,y,z components of electric field         
    def Data(self):
        f1=open('JacobiPoisson4','w')
        k=(self.size/2)
        for i in range(1,self.size-1):
            for j in range(1,self.size-1):

                Ex=((1/(2.0*self.dx))*(-self.potential[(i+1),j,k]+self.potential[(i-1),j,k])) #calculates x,y components of electric field 
                Ey=((1/(2.0*self.dx))*(-self.potential[i,(j+1),k]+self.potential[i,(j-1),k])) # in the midplane of z=25 
                Ez=((1/(2.0*self.dx))*(-self.potential[i,j,(k)]+self.potential[i,j,(k)])) # calculates Ez
                f1.write('%d %d %d %lf %lf %lf %lf\n'%(i,j,k,self.potential[i,j,k],Ex,Ey,Ez)) #saves data in file in lecturers format
        f1.close()
        
#------------------------------------------------------------------------------
# function to read in data and extract needed data into list to plot data 
    def Read(self):
        f2=open('JacobiMagnetisation','r') #opend data file 
        list1=f2.readlines() #reads in each line, this a a 2d list 
        f3=[x.strip() for x in list1] #splits string of each line into individual strings 
        values=[]
        [values.append(x.split()) for x in f3] 
        self.xlist=[] 
        self.ylist=[]
        self.potential=[]
        self.Ex=[]
        self.Ey=[]
        for q in range(len(values)): #for loops collect needed data from file and puts into individual list 
            self.xlist.append(float(values[q][0])) #appends the neccesary data from file into corresponding lists
            self.ylist.append(float(values[q][1]))
            self.potential.append(float(values[q][3]))
            self.Ex.append(float(values[q][4]))
            self.Ey.append(float(values[q][5]))
        #self.Contour()
        #self.Vector()

#------------------------------------------------------------------------------
#function to perform contour plot 
    def Contour(self):
        X,Y=np.meshgrid(self.xlist,self.ylist)
        h=scipy.interpolate.griddata((self.xlist,self.ylist),self.potential,(X,Y))
        plt.figure()
        plt.title("Potential Field via Jacobi Algorithm (midplane z=25)")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.contourf(X,Y,h,20,cmap='gist_rainbow')
        plt.colorbar()
        
#------------------------------------------------------------------------------
#function to plot 3d vector
    def Vector(self):
        X,Y=np.meshgrid(self.xlist,self.ylist) #lays out the coordinate axis 
        fig, ax =plt.subplots()
        
        normex=[] #lists for normalised electrif field data to go in 
        normey=[]
        
        for i in range(len(self.Ex)):
            x=(self.Ex[i])/(m.sqrt((self.Ex[i]**2)+(self.Ey[i]**2)))
            normex.append(x)
            y=(self.Ey[i])/(m.sqrt((self.Ex[i]**2)+(self.Ey[i]**2)))
            normey.append(y)
        eX,eY=np.meshgrid(normex,normey)
        q=scipy.interpolate.griddata((self.xlist,self.ylist),normex,(X,Y)) #interpolates the Ex and Ey data
        w=scipy.interpolate.griddata((self.xlist,self.ylist),normey,(X,Y))
        
                
        plt.title("Electric Field via Jacobi Algorithm (midplane z=25)")
        q=ax.quiver(X,Y,q,w,angles='xy', scale_units='xy', scale=1)
        plt.show()
                
#------------------------------------------------------------------------------
#function to plot potential/electrid field vs distance from centre in 2D
    def Quantitative(self):
        self.Read()
        centre=(self.size/2.0)
        distancelist=[] #list for all distacne values to go in to
        fieldlist=[] #list for magnitude of field to go in to 

        #for loop to calulate distance and magnitude of electric field 
        f=open('QuantativeMagnetic','w')
        for i in range(len(self.xlist)):
            dx=(self.xlist[i]-centre)**2.0
            dy=(self.ylist[i]-centre)**2.0
            distance=m.sqrt(dx+dy)
            distancelist.append(distance)
            field=m.sqrt((self.Ex[i]**2.0)+(self.Ey[i]**2.0))
            fieldlist.append(field)
            f.write('%lf %lf %lf\n'%(distance,self.potential[i],field))
        f.close()
            #logdistance.append(m.log10(distance))
            #logfield.append(m.log10(field))
     
        #plots the log of the potential vs log of the distance 
        plt.figure()
        plt.title("Vector Potential vs R")
        plt.xlabel("log R")
        plt.ylabel("Potential")
        plt.scatter(np.log(distancelist),(self.potential),marker='x')
        
        #the next few lines of code orders the distance and potential list so that is goes in increasing size 
        #because distancelist and self.potential are jumbled lists
        #this orders it so both lists can be sliced by the same numbers and still maintain the data alignment 
        
        logdist=np.log(distancelist)
        logpot=np.log(self.potential)
        logdist,logpot=zip(*sorted(zip(logdist,logpot))) #this orders both lists so the element by element relation stays 
        #e.g [2,3,4,5,1],[two,three,four,five,one] goes to [1,2,3,4,5],[one,two,three,four,five]
        logdist,logpot=(list(t) for t in zip(*sorted(zip(logdist,logpot)))) #this turns them back into lists
        a=logdist.index(2.0302215052732095) #this is to just locate where to cut the list from 
        fitx=logdist[1:a+1] #cuts both list in according to a 
        fity=logpot[1:a+1]
        py=np.polyfit(fitx,fity,1) #then fits the data 
        potfit=[py[1]+py[0]*x for x in fitx] #creates potential values from the fit to be plotted 
        #plt.plot(fitx,potfit) #plots the fit 
        plt.show()
        #print("The gradient of the fit for the potential is {}".format(py[0]))
        # below the same procedure is repeated for the field data      
        
        plt.figure()
        plt.title("Magnetic Field vs R (Gradient of fit is -1.05) ")
        plt.xlabel("Log R")
        plt.ylabel("Log Magnetic Field")
        plt.scatter(np.log(distancelist),np.log(fieldlist),marker='x')
        logdist2=np.log(distancelist)
        logfield=np.log(fieldlist)
        logdist2,logfield=zip(*sorted(zip(logdist2,logfield)))
        logdist2,logfield=(list(t) for t in zip(*sorted(zip(logdist2,logfield))))
        #going to use same cut off point as for potential 
        fitx1=logdist2[1:a+1]
        fity1=logfield[1:a+1]
        py1=np.polyfit(fitx1,fity1,1)
        fieldfit=[py1[1]+py1[0]*x for x in fitx1]
        plt.plot(fitx1,fieldfit)
        plt.show()
        print ("The Gradient of the fit for the field is {}".format(py1[0]))
        
#------------------------------------------------------------------------------
#function to do the Gauss-Seidel algortihm
    def GaussSeidelUpdate(self,w):
        #odd checkerboard
        for i in range(1,(self.size-1)):
            for j in range(1,(self.size-1)):
                for k in range(1,(self.size-1)):
                    if (i+j+k)%2==1:
                        Pnew=(1.0/6.0)*(self.potential[(i+1),j,k]+self.potential[(i-1),j,k] #calculates the odd checkerboard values 
                        +self.potential[i,(j+1),k]+self.potential[i,(j-1),k]+self.potential[i,j,(k+1)]+self.potential[i,j,(k-1)]
                        +((self.dx**(2)*(self.density[i,j,k]))))
                        #implements relaxation parameter 
                        self.NewPotential[i,j,k]=(((1.0-w)*self.potential[i,j,k])+(w*Pnew))

         #even checkerboard               
        for i in range(1,(self.size-1)):
            for j in range(1,(self.size-1)):
                for k in range(1,(self.size-1)):
                    if (i+j+k)%2==0: #Newpotential is used as these are the most recent updated values from the odd checkerboard 
                        Pnew=(1.0/6.0)*(self.NewPotential[(i+1),j,k]+self.NewPotential[(i-1),j,k]
                        +self.NewPotential[i,(j+1),k]+self.NewPotential[i,(j-1),k]+self.NewPotential[i,j,(k+1)]+self.NewPotential[i,j,(k-1)]
                        +((self.dx**2)*(self.density[i,j,k])))
                        self.NewPotential[i,j,k]=(((1.0-w)*self.potential[i,j,k])+(w*Pnew))

#------------------------------------------------------------------------------
#function to solve via GaussSeidelUpdate
    def GaussSeidelSolve(self,p):
        err=1 #set err initial to start while loop
        n=0 #counter to see where i am in the loop
        #still have two arrays so can caluclate steady state 
        while err>10**(-p):
            self.SOR(1.94) #updates the potential 
            diff=np.subtract(self.NewPotential,self.potential) #calculates difference element wise between new and old potential 
            norm=np.absolute(diff) #get the absolute value of this difference 
            err=np.sum(norm) #gets the error 
            self.potential=copy.deepcopy(self.NewPotential) #updates current potential to new potential for next iteration
            n+=1
            print n
        print (n)
        #self.Data()
        
#------------------------------------------------------------------------------
#function to perform relaxation 
    def Relaxation(self,p):
        loops=[] #lists for w and number of iterations to go into 
        wlist=[]
        for w in np.arange(1.00,2.00,0.05): #loop to go through each w 
            self.potential=np.zeros((self.size,self.size,self.size)) #resets the newpotential and potential matrices for next round
            self.NewPotential=np.zeros((self.size,self.size,self.size))
            print (w)
            for l in range(0,1000000): #max iteration length
                self.GaussSeidelUpdate(w) #calls update method to get new potential
                diff=np.subtract(self.NewPotential,self.potential) #subtract new and old element wise 
                norm=np.absolute(diff) #get the absolute value of the difference 
                err=np.sum(norm) #sum the differences 
                #self.potential=copy.deepcopy(self.NewPotential) #updates old potential to be used in next iteration
                if err<10**(-p): #checks convergence 
                    loops.append(l) #appends numbe of iterations to list
                    print l
                    break #breaks out of l for loop
                self.potential=copy.deepcopy(self.NewPotential) #updates old potential to be used in next iteration

            
            wlist.append(w)
   
        np.savetxt("LoopsPoisson",loops)
        np.savetxt("wlistPoisson",wlist)
        

#------------------------------------------------------------------------------
#function to solve single wire problem 
    def Magnetisation(self,p):
        err=1 #set err initial to start while loop
        n=0 #counter to see where i am in the loop
        while err>10**(-p):
            self.JacobiUpdate() #updates the potential 
            diff=np.subtract(self.NewPotential,self.potential) #calculates difference element wise between new and old potential 
            norm=np.absolute(diff) #get the absolute value of this difference 
            err=np.sum(norm) #gets the error 
            self.potential=copy.deepcopy(self.NewPotential) #updates current potential to new potential for next iteration
            #n+=1
            #print n
        #print self.potential

        self.MagentisationData()

#------------------------------------------------------------------------------
#function to save data of single wire and calculate magnetisation
    def MagentisationData(self):
        f1=open('JacobiMagnetisation','w')
        k=(self.size/2) #gets data for midplane 
        for i in range(self.size):
            for j in range(self.size):
                if i==0 or i==(self.size-1) or j==0 or j==(self.size-1): #boundary conditions 
                    pass
                else:
                    Bx=(1.0/(2.0*self.dx))*(self.potential[i,j+1,k]-self.potential[i,j-1,k]-self.potential[i,j,k+1]+self.potential[i,j,k-1]) #x component of magnetic field 
                    By=(1.0/(2.0*self.dx))*(self.potential[i,j,k+1]-self.potential[i,j,k-1]-self.potential[i+1,j,k]+self.potential[i-1,j,k]) #y component of magnetic field 
                    f1.write('%d %d %d %lf %lf %lf\n'%(i,j,k,self.potential[i,j,k],Bx,By)) #saves data in file in lecturers format
        f1.close()
        
#------------------------------------------------------------------------------

            
        
        

        

                    
        


        
        

        
            
            

            
            
            
                
                
                
            
            
                        
        
                    
                        
                    
        
            
            
                
                
        
                
        
                          
                    
                    
                    
                    
                    