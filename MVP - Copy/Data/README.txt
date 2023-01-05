FREEENERGY(0)= data for free energy for phi=0
FREEENERGY(5)= data for free energy for phi=0.5
JacobiPoisson3= data for solving possion equation, it is in the same form as Davide's 
JacobiMagnetisation= data for solving poisson equation, same form as poisson but electric field columns replaced by magnetic field 
QuantativePoisson= data for quantative data for poisson, same form as Davide
QuantativeMagnetisation= data for quantative data for magnet, same form as Davide
LoopsPoisson= data for SOR this contains the times
wlistPoisson= data for SOR this contains the w values 

Main-python code for checkpoint 3, this is where everything will be called from 

InitialCondtions- this is code which contains code to setup initial matrices for all checkpoints. For this checkpoint the function IVP
                  are used for Cahn Hilliard and then SingleCharge and SingleWire functions are used for the second part of the checkpoint 

IntialValue- this is code for Cahn Hilliard update rule and code to animate

BoundaryValue- this is code for the second part of the checkpoint, it contains the Jacobi and Gauss Siedel algorithms aswell as code to plot

For Cahn Hilliard animation, please run the FreeEnergyDensity function in the main.
