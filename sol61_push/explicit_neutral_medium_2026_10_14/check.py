"""Homogeneous coherent neutral equilibrium and explicit-mediator Bogoliubov modes."""
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.optimize import brentq,minimize_scalar
prior=json.loads(Path('sol61_push/neutral_carrier_identity_2026_10_14/run/results.json').read_text())
h=prior['pair_mediator_coupling_eV_minus_half'];gs=prior['same_sign_NR_coupling_eV_minus2'];gc=prior['opposite_nonresonant_NR_coupling_eV_minus2'];gp=gs+gc
m=1.;M=2.;delta=2e-9;hc=1.973269804e-7;hb=6.582119569e-16
checks=[]
def ck(name,e,t):
    assert e<=t,(name,e,t)
    checks.append(dict(name=name,error=float(e),tolerance=t))
def equilibrium(n):
    scale=max(delta,h*math.sqrt(n),gp*n)
    df=lambda f:(delta/2-h*math.sqrt(n/2)*(1-3*f)/(2*math.sqrt(f))-gp*n*(1-f)/2)/scale
    f=brentq(df,1e-20,1-1e-14,xtol=1e-18)
    A=math.sqrt(n*(1-f)/2);r=-math.sqrt(n*f/2);chem=gp*A*A+h*r
    energy=delta*r*r+2*h*r*A*A+gp*A**4
    return A,r,chem,energy,f,scale

def bogoliubov(n,k):
    A,r,chem,_,_,_=equilibrium(n)
    L=np.array([[(2*gs+gc)*A*A-chem,gc*A*A,h*A],[gc*A*A,(2*gs+gc)*A*A-chem,h*A],[h*A,h*A,delta-2*chem]])
    B=np.array([[gs*A*A,gc*A*A+h*r,0],[gc*A*A+h*r,gs*A*A,0],[0,0,0.]])
    L+=np.diag([k*k/(2*m),k*k/(2*m),k*k/(2*M)])
    return np.block([[L,B],[-B,-L]]),L,B
rows=[]
for nSI in [1e6,prior['mixing_order_one_density_per_m3'],3e14]:
    n=nSI*hc**3;A,r,chem,E,f,scale=equilibrium(n)
    ck('conserved_number_composition',abs((2*A*A+2*r*r)/n-1),1e-14)
    ck('mediator_stationarity',abs((delta-2*chem)*r+h*A*A)/(scale*math.sqrt(n)),2e-12)
    Bdg,L,B=bogoliubov(n,0.)
    def force(v):
        a,b,R=v
        return np.array([(gs*abs(a)**2+gc*abs(b)**2-chem)*a+h*R*b.conjugate(),(gs*abs(b)**2+gc*abs(a)**2-chem)*b+h*R*a.conjugate(),(delta-2*chem)*R+h*a*b])
    background=np.array([A,A,r],complex);step=math.sqrt(n)*1e-5
    realJ=np.column_stack([(force(background+np.eye(3)[j]*step)-force(background-np.eye(3)[j]*step)).real/(2*step) for j in range(3)])
    imagJ=np.column_stack([(force(background+1j*np.eye(3)[j]*step)-force(background-1j*np.eye(3)[j]*step)).imag/(2*step) for j in range(3)])
    ck('direct_field_linearization_real',float(np.max(abs(realJ-(L+B))))/scale,1e-8)
    ck('direct_field_linearization_imag',float(np.max(abs(imagJ-(L-B))))/scale,1e-8)
    # Thermodynamic derivative, two step sizes, and hydrodynamic BdG comparison.
    derivative=lambda step:(equilibrium(n*(1+step))[2]-equilibrium(n*(1-step))[2])/(2*n*step)
    dp=derivative(1e-3);dpf=derivative(1e-4)
    ck('chemical_derivative_refinement',abs(dp/dpf-1),2e-6)
    assert dpf<0
    ksmall=math.sqrt(m*scale)*1e-4
    growthsmall=max(np.linalg.eigvals(bogoliubov(n,ksmall)[0]).imag)
    predicted=ksmall*math.sqrt(-n*dpf/m)
    ck('hydrodynamic_instability_coefficient',abs(growthsmall/predicted-1),2e-4)
    def growth(logk):return max(0.,float(np.max(np.linalg.eigvals(bogoliubov(n,math.exp(logk))[0]).imag)))
    bounds=np.log(math.sqrt(m*scale))+np.array([-10.,3.])
    grid=np.linspace(*bounds,401);values=np.array([growth(x) for x in grid]);i=int(values.argmax());assert 0<i<len(grid)-1
    optimum=minimize_scalar(lambda x:-growth(x),bounds=(grid[i-1],grid[i+1]),method='bounded',options={'xatol':1e-12})
    k=math.exp(optimum.x);rate=growth(optimum.x)
    ev=np.linalg.eigvals(bogoliubov(n,k)[0]);ck('BdG_plus_minus_symmetry',max(min(abs(z+ev)) for z in ev)/scale,1e-10)
    rows.append(dict(total_conserved_number_density_per_m3=nSI,mediator_fraction_of_constituent_number=f,atomic_fraction=1-f,chemical_potential_eV=chem,energy_per_constituent_eV=E/n,pressure_eV4=n*chem-E,compressibility_coefficient_n_dmu_dn_eV=n*dpf,max_instability_growth_per_s=rate/hb,fastest_wavelength_m=2*math.pi*hc/k,NR_scale_over_mass=scale/m))
result=dict(scope='Homogeneous coherent Q=0 branch of the stated three-field rotating-wave mean-field model; no kinetic halo distribution, gravity, damping or finite-trap spectrum',rows=rows,checks=checks,passed=len(checks))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
