from refl1d.names import*
from numpy import mod, exp, arange, linspace
import math
Probe.view = 'log' #log plot
data_file_n ='C:/Users/saya6/Documents/NCNR/test/TiOx_2.3_trunc.refl'
instrument = NCNR.XRay(wavelength=1.54, Tlo = 1.4975, slits_at_Tlo=0.01, slits_above = 0.01)
probe = instrument.load('C:/Users/saya6/Documents/NCNR/test/TiOx_2.3_trunc.refl',back_reflectivity=False)
Si=SLD('Silicon', rho=20.071, irho= 0.458)
SiO2=SLD('SiO2', rho=18.831, irho=0.2440)
TiO2=SLD('TiO2', rho=30.799, irho=1.557)
TiO2_1=SLD('TiO2_1', rho=30.799, irho=1.557)
gas=SLD('Ambient',rho=0,irho=0)
Si_Thickness = Parameter(name='Si_Thickness', value= 50.0) 
#value has to be float?
SiO2_Thickness=Parameter(name='SiO2_Thickness', value = 15.0)
TiO2_Thickness=Parameter(name='TiO2_Thickness', value=650.0)
TiO2_1_Thickness=Parameter(name='TiO2_1_Thickness', value=100.0)
Si_FracWidth=Parameter(name='Si:SiO2(W/T)', value=0.10)
SiO2_FracWidth = Parameter(name='SiO2:TiO2(W/T)', value=0.10)
TiO2_FracWidth=Parameter(name='TiO2:TiO2_1(W/T)', value = 0.10)
TiO2_1_FracWidth=Parameter(name='TiO2_1:gas(W/T)', value=0.10)
Si_FracWidth.range(0.0, 0.55) # Ptints 'Parameter(Si:SiO2(W/T))'
# use fraction  55% thickness
SiO2_FracWidth.range(0.0, 0.55) # Ptints Parameter(SiO2:TiO2(W/T))
TiO2_FracWidth.range(0.0, 0.55) # Prints Parameter(TiO2:TiO2_1(W/T))
TiO2_1_FracWidth.range(0.0, 0.55) # Prints Parameter(TiO2_1:gas(W/T))

# do not use effective thickness, Si is semi-infinate
# T_eff0 = Parameter(name='Effective Thickness Si:SiO2', value = 50.0)
# T_eff0=pow((pow(Si_Thickness, -4.0)+pow(SiO2_Thickness, -4.0)), -0.25)
T_eff1=Parameter(name='Effective Thickness SiO2:TiO2', value=50.0)
T_eff1=pow((pow(SiO2_Thickness, -4.0)+pow(TiO2_Thickness, -4.0)), -0.25)
T_eff2=Parameter(name='Effective Thickness TiO2:TiO2_1', value=50.0)
T_eff2=pow((pow(TiO2_Thickness, -4.0)+pow(TiO2_1_Thickness, -4.0)), -0.25)
Si_SiO2 = (Si_FracWidth)*(SiO2_Thickness)
SiO2_TiO2 = (SiO2_FracWidth)*(T_eff1)
TiO2_TiO2_1=(TiO2_FracWidth)*(T_eff2)
TiO2_1_gas=(TiO2_1_FracWidth)*(TiO2_1_Thickness)
sample=Si(50.0, Si_SiO2)|SiO2(SiO2_Thickness, SiO2_TiO2)|TiO2(TiO2_Thickness,TiO2_TiO2_1)|TiO2_1(TiO2_1_Thickness, TiO2_1_gas)|gas(0.0, 0.0)
# 50A semi infinate, 
TiO2.rho.range(20, 38) # prints Parameter(TiO2 rho) 
TiO2_1.rho.range(20, 38) # prints Parameter(TiO2_1 rho) SLD 10-6 A^-2
SiO2_Thickness.range(0, 100) # prints Parameter(SiO2_Thickness) A
TiO2_Thickness.range(0, 650) # prints Parameter(TiO2_Thickness)
TiO2_1_Thickness.range(0, 200) # prints Parameter(TiO2_1_Thickness)
theta_offset=Parameter(name='Theta_Offset', value=0.0) # keep, fixed at 0
step = False
intensity=Parameter(name='Intensity', value = 0.9509)
intensity.range(0.9, 1.5)
probe.intensity= intensity
background=Parameter(name='Background', value=1e-10)
background.range(0, 1e-7)
probe.background=background
M=Experiment(probe=probe, sample=sample)
problem=FitProblem(M)
print("end")