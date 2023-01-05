"""Checkpoint 2 Classes"""
import math as m
import numpy as np
import matplotlib.pyplot as plt
import copy 
import scipy.interpolate


#----------------------------------------------------------------------------------------------------------------------------------

class RulesGoL(object):
    def __init__(self, a_s):
        
        self.a_s=a_s
    
#----------------------------------------------------------------------------------------------------------------------------------
    def sumArray(self, i, j, array):
        #newArray=array
        #newArray=self.array
        neighbourSum=0
        for h in range(-1,2):
            for k in range(-1,2):
                if h == 0 and k ==0 :
                    pass
                else:
                    
                    a=(i+h)%self.a_s
                    b=(j+k)%self.a_s
                    
                    neighbourSum+=array[a][b]
        
        return neighbourSum
        
#----------------------------------------------------------------------------------------------------------------------------------
    def allRules(self, array):
        nextArray=np.zeros((self.a_s,self.a_s))
        for i in range (0,self.a_s):
            for j in range(0,self.a_s):
                neighbourSum=self.sumArray(i, j, array)
                if array[i][j]==1:
                    #print(neighbourSum)
                    if neighbourSum<2:
                        nextArray[i][j]=0
                    if neighbourSum>3:
                        nextArray[i][j]=0
                    
                    if neighbourSum==3 or neighbourSum==2:
                        nextArray[i][j]=1
                else:
                    if neighbourSum == 3:
                        nextArray[i][j]=1
        #print("first iter")
        #print(array)
        #print("Second iter")
        #print(nextArray)
        return nextArray

#----------------------------------------------------------------------------------------------------------------------------------
    
    def newArrayget(self,array):
        """This function sets a copy of the changing array and to optimise it also uses the same for loops to 
        work out number of active sites"""
        array=self.allRules(array)
        arraysum=0     #sums of the number of active sites
        #print(array)
        for i in range(0,self.a_s):
            for j in range(0,self.a_s):
                self.arrayChange[i][j]=array[i][j]
                arraysum+=array[i][j]
        #print(arraysum)
        return self.arrayChange,arraysum
#----------------------------------------------------------------------------------------------------------------------------------
    
    def interate(self,array,steps):
        self.arrayChange=np.zeros((self.a_s,self.a_s))
        self.arraysum=np.zeros(steps)
        for i in range (0,steps):
            array,arraysum=self.newArrayget(array)
            self.animate(self.arrayChange)
            
#----------------------------------------------------------------------------------------------------------------------------------                
            
    def animate(self, array):
        f=open('GameofLife.dat','w')
        for i in range(self.a_s):
            for j in range(self.a_s):
                f.write('%d %d %lf\n'%(i,j,array[i,j]))
        f.close()
        plt.cla()
        im=plt.imshow(array, animated=True)
        plt.draw()
        plt.pause(0.01) 
    
    #def sumTotalArray(self,array):
    
#----------------------------------------------------------------------------------------------------------------------------------
    
    def equilibriums(self,steps):
        
        times=np.zeros(100)
        for k in range (0,100):
            print("Runs = ")
            print(k+1)
            array=np.random.choice([1,0], [self.a_s,self.a_s],[0.5,0.5])
            self.arrayChange=np.zeros((self.a_s,self.a_s))
            self.arraysum=np.zeros(steps)
            for i in range (0,steps):
                array,arraysum=self.newArrayget(array)
                self.arraysum[i]=arraysum
                if self.arraysum[i]==self.arraysum[i-2] and self.arraysum[i]==self.arraysum[i-1] and self.arraysum[i]==self.arraysum[i-3] and self.arraysum[i]==self.arraysum[i-4]:
                    print("Equilibrium reached!")
                    print(i)
                    times[k]=i
                    break
        return times        
#----------------------------------------------------------------------------------------------------------------------------------

    def newArraywithCoM(self,array,time):
        """This function sets a copy of the changing array and to optimise it also uses the same for loops to 
        work out the centre of mass sum"""
        array=self.allRules(array)
        x=[]
        y=[]
        timeofglide=[]
        CoMx=0
        CoMy=0
        #print(array)
        breakcount=0
        for i in range(0,self.a_s):
            for j in range(0,self.a_s):
                #print ("NEW")
                #print (self.arrayChange)
                #print ("OLD")
                #print (array)
                #self.arrayChange[i][j]=array[i][j]
                #print (array)
                if array[i][j]==1:
                    #print("LOL")
                    if 5<i<44 and 5<j<44:  
                        #print("HI")
                        CoMx+= i
                        CoMy+= j
                    else:
                        breakcount=1     #break count is used to break from both for loops
                        break
            if breakcount==1:
                break
        CoMxTot=CoMx/5
        CoMyTot=CoMy/5
        if breakcount!=1:
            print(time)
            self.x.append(CoMxTot)
            self.y.append(CoMyTot)
            self.timeofglide.append(time)
        self.CoMData=[x,y,timeofglide]

        return array
        
#----------------------------------------------------------------------------------------------------------------------------------

    def centreOfmass(self,array,steps):
        self.arrayChange=np.zeros((self.a_s,self.a_s))
        
        self.x=[]
        self.y=[]
        self.timeofglide=[]
        CentreOfMassXY=np.zeros((2,steps))
        #print(CentreOfMassXY)
        self.arraysum=np.zeros(steps)
        for i in range (0,steps):
            array=self.newArraywithCoM(array,i)
            #,CentreOfMassXY[0][i],CentreOfMassXY[1][i]=
            
            #print(CentreOfMassXY[0][i],CentreOfMassXY[1][i])
            #self.animate(self.arrayChange)   
        CoMData=[self.x,self.y,self.timeofglide]
        #np.savetxt("3rd CoM Data Array_Size = 50", CoMData)
        
        return CentreOfMassXY             
#----------------------------------------------------------------------------------------------------------------------------------
    
    def speed(self):
        CoMData=np.loadtxt("3rd CoM Data Array_Size = 50")
        xmax=(np.where(CoMData[0]==(CoMData[0].max())))[0]
        ymax=(np.where(CoMData[1]==(CoMData[1].max())))[0]
        
        Xslice=CoMData[0][0:xmax[0]+1]
        Yslice=CoMData[1][0:ymax[0]+1]
        TimeSliceX=CoMData[2][0:xmax[0]+1]
        TimeSliceY=CoMData[2][0:ymax[0]+1]
        
        funcx=np.polyfit(TimeSliceX,Xslice, 1)
        funcy=np.polyfit(TimeSliceY,Yslice, 1)
        
        #np.gradient(funcx)
        #np.gradient(funcy)
        
        xplot=[funcx[1]+funcx[0]*i for i in TimeSliceX] 
        plt.figure()
        plt.title("X Position of COM with Fit")
        plt.xlabel("Time")
        plt.ylabel("X Position")
        plt.plot(TimeSliceX,xplot) 
        plt.scatter(TimeSliceX,Xslice)
        plt.show()
        
        yplot=[funcy[1]+funcy[0]*i for i in TimeSliceY] 
        plt.figure()
        plt.title("Y Position of COM with Fit")
        plt.xlabel("Time")
        plt.ylabel("Y Position")
        plt.plot(TimeSliceY,yplot) 
        plt.scatter(TimeSliceY,Yslice)
        plt.show()
        
        
        print(funcx[0])
        print(funcy[0])
        Speed= m.sqrt((funcx[0]**2)+(funcy[0]**2))
        
        print("The speed of the object is " + str(Speed))
        
    
#----------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------
 
    
class SIRS(object):
    
    def __init__(self,a_s,array):
        self.a_s=a_s
        self.array=array
        
    
    def transition(self, i, j, array,p1,p2,p3):         # 1 is infected, 0 is susceptible, -1 is recovering
        if self.array[i][j]==0:
            if self.array[(i+1)%self.a_s][j]==1 or self.array[(i-1)%self.a_s][j]==1 or self.array[i][(j-1)%self.a_s]==1 or self.array[i][(j+1)%self.a_s]==1:
                r=np.random.random()
                if r<p1:
                    self.array[i][j]=1
        
        if self.array[i][j]==1:
            r=np.random.random()
            if r<p2:
                self.array[i][j]=-1
            
        if self.array[i][j]==-1:
            r=np.random.random()
            if r<p3:
                self.array[i][j]=0 
                                    
        
    def newArray(self, p1, p2, p3):
        for i in range(self.a_s*self.a_s):
            k=np.random.randint(0,self.a_s)
            l=np.random.randint(0,self.a_s)
            self.transition(k,l,self.array,p1,p2,p3)
        #print(array)
        #return nextArray
    
    def animateSIR(self, p1, p2, p3,steps):
        #self.nextA=np.zeros((self.a_s,self.a_s))
        for k in range(0,steps):
            self.newArray( p1, p2, p3)
            f=open('SIRS','w')
            for o in range(self.a_s):
                for p in range(self.a_s):
                    f.write('%d %d %lf\n'%(o,p,self.array[o,p]))
            f.close()
            plt.cla()
            im=plt.imshow(self.array, animated=True)
            plt.draw()
            plt.pause(0.01) 
            
    def sumfunc(self):
        infected=0
        for i in range(0,self.a_s):
            for j in range (0,self.a_s):
                if self.array[i][j]==1:
                    infected+=1
                    #print("hi")
        return infected
                
            
    def phase(self,p1,p2,p3,sweeps):
        infectedAverages=[]
        infectedAverageSqr=[]
        p1big=[]
        p3big=[]
        print("dingdong")
        for i in range(0,len(p1)):
            for j in range(0,len(p3)):
                p1big.append(p1[i])
                p3big.append(p3[j])
                tempinfcounter=[]
                self.array=np.random.choice([1,0,-1], [self.a_s,self.a_s],p=[1/3,1/3,1/3])
                print(i,j)
                for k in range(0,sweeps):
                    self.newArray(p1[i],p2,p3[j])
                    if k<100:       #this might need to be 101
                        pass
                    else:
                        sumTot=(self.array==1).sum()
                        if sumTot!=0:
                            tempinfcounter.append(sumTot)
                        else:
                            break
                        
                        #infected_sums[(i*10)+j][k-100]=sumTot
                #print(p3[j])
                infectedAverageSqr.append(np.mean(np.square(tempinfcounter)))
                infectedAverages.append(np.mean(tempinfcounter))
            print(i)
        #print infected_sums
        #np.savetxt("Infected Numbers Small", infected_sums)
        #np.savetxt("Infected Numbers", infected_sums)
        np.savetxt("Infected Averages", infectedAverages)
        np.savetxt("Infected Averages Sqr", infectedAverageSqr)
        np.savetxt("p1", p1big)
        np.savetxt("p3", p3big)




    def phaseP1vary(self,p1,p2,p3,sweeps):
        infectedAverages=[]
        infectedAverageSqr=[]
        print("dingdong")
        for i in range(0,len(p1)):
            tempinfcounter=[]
            self.array=np.random.choice([1,0,-1], [self.a_s,self.a_s],p=[1/3,1/3,1/3])
            
            for k in range(0,sweeps):
                self.newArray(p1[i],p2,p3)
                print((self.array==1).sum())
                if k<100:       #this might need to be 101
                    pass
                else:
                    
                    sumTot=(self.array==1).sum()
                    print(sumTot)
                    if sumTot!=0:
                            tempinfcounter.append(sumTot)
                            print(sumTot)
                    else:
                        break
            infectedAverageSqr.append(np.mean(np.square(tempinfcounter)))
            infectedAverages.append(np.mean(tempinfcounter))
            print(i)
        #print infected_sums
        #np.savetxt("Infected Numbers Small", infected_sums)
        #np.savetxt("Infected Numbers", infected_sums)
        #np.savetxt("Infected Averages P1 Varied2", infectedAverages)
        #np.savetxt("Infected Averages Sqr P1 Varied2", infectedAverageSqr)
    
    
    def plots(self,sweeps):
        """This function loads in the data and plots the contour plots"""
        Infs=np.loadtxt("Infected Numbers")
        Infsqrs=np.loadtxt("Infected Averages Sqr")
        p1=np.loadtxt("p1")
        p3=np.loadtxt("p3")
        means=[]
        sqrmeans=[]
        variance=[]
        for i in range(0,len(p1)*len(p3)):
            means.append(np.mean(Infs[i]))
            sqrmeans.append(np.mean(np.square(Infsqrs[i])))
            variance.append((sqrmeans[i]-(means[i]**2))/(self.a_s*self.a_s))
        
        meshX, meshY = np.meshgrid(p1,p3)
        func=scipy.interpolate.griddata((p1,p3), means, (meshX,meshY))
        plt.figure()
        plt.contourf(meshx,meshy,func,cmap="gist_rainbow")
        plt.colorbar()
        plt.title("Means Plot")
        
        
        func=scipy.interpolate.griddata((p1,p3), variance, (meshX,meshY))
        plt.figure()
        plt.contourf(meshx,meshy,func,cmap="gist_rainbow")
        plt.colorbar()
        plt.title("Variance Plot")
        
        
    def plotsP1varied(self,sweeps,p1,p3):
        """This function loads in the data and plots the contour plots"""
        Infs=np.loadtxt("Infected Averages P1 Varied")
        Infsqrs=np.loadtxt("Infected Averages Sqr P1 Varied")
        means=[]
        sqrmeans=[]
        variance=[]
        for i in range(0,len(p1)):
            means.append(np.mean(Infs[i]))
            sqrmeans.append(np.mean(np.square(Infsqrs[i])))
            variance.append((sqrmeans[i]-(means[i]**2))/(self.a_s*self.a_s))
        
        print(Infs)
        print(Infsqrs)
        plt.figure()
        plt.scatter(p1,variance)
        plt.title("Variance Plot")
        
        
        
        
                

                
            
                
                
                
                
                
                
                
                
                
                