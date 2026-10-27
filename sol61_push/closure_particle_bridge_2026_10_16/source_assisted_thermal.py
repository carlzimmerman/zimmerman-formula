"""Pole-free X+Phi+Phi* -> Phi+Phi thermal reaction density.

Vacuum tree amplitude, common MB temperature, on-shell narrow source.
Nested deterministic quadrature of total COM energy, initial Dalitz mass,
and relative angles. This is not a completed finite-density collision set.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.special import kve, roots_genlaguerre, roots_jacobi, roots_legendre

out=Path(sys.argv[1]);assert out.is_dir()
base=Path(__file__).parent
parent=json.loads((base/'thermal_charge_run_002/results.json').read_text())
p=next(row['parameters'] for row in parent['phase_rows'] if row['parameters']['m']==.002)
m,M,g,lam=p['m'],p['M'],p['g'],p['total']
mu,gh=M/m,g/m
checks=[]
def check(name,value):
    checks.append({'name':name,'passed':bool(value)});assert value,name

amp0=8*g*lam*(M+m)/(M*m*(M+2*m))-2*g**3*(5*M+8*m)/(m*M*M*(M+m)*(M+2*m))
beta0=math.sqrt(1-4*m*m/(M+2*m)**2)
K3zero=beta0*amp0*amp0/(128*math.pi*M*m*m)

class Thermal:
    def __init__(self,ne,nu,na,nphi):
        self.ey,self.ew=roots_genlaguerre(ne,2)
        uz,uw=roots_jacobi(nu,.5,.5)
        self.uv=(uz+1)/2;self.uw=uw/4
        z,w=roots_legendre(na)
        ci,cf,ph=np.meshgrid(z,z,2*math.pi*np.arange(nphi)/nphi,indexing='ij')
        wi,wf,wp=np.meshgrid(w/2,w/2,np.ones(nphi)/nphi,indexing='ij')
        self.ci=ci.reshape(1,-1);self.si=np.sqrt(1-self.ci**2)
        self.cf=cf.reshape(1,-1);self.sf=np.sqrt(1-self.cf**2)
        self.cp=np.cos(ph).reshape(1,-1)
        self.aw=(wi*wf*wp).reshape(1,-1)
        self.dim=(ne,nu,na,nphi)
        self.min_safe_denominator=math.inf
    def phase_integral(self,E):
        # m=1: dPhi3 dPhi2 |M5|^2 has dimension zero.
        s=E*E
        width=(E-mu)**2-4
        if width<=0:return 0.
        vv=self.uv[:,None]
        u=4+width*vv;ru=np.sqrt(u)
        klam=(s-(mu+ru)**2)*(s-(mu-ru)**2)
        klam=np.maximum(klam,0)
        root=np.sqrt(klam)
        kz=root/(2*E)
        EX=(s+mu*mu-u)/(2*E)
        EQ=(s-mu*mu+u)/(2*E)
        q=np.sqrt(u/4-1)
        # Negative-charge incoming daughter r; pair azimuth fixed by
        # global rotations; final azimuth is the physical relative angle.
        er=EQ/2+kz/ru*q*self.ci
        rx=-q*self.si
        rz=-EQ/ru*q*self.ci-kz/2
        kf=math.sqrt(s/4-1)
        dot=rx*kf*self.sf*self.cp+rz*kf*self.cf
        dp0=mu*mu+2*(EX*er-kz*rz)
        dp1=mu*mu-EX*E+2*kz*kf*self.cf
        dp2=mu*mu-EX*E-2*kz*kf*self.cf
        dx0=s-mu*mu
        dx1=2-er*E-2*dot-mu*mu
        dx2=2-er*E+2*dot-mu*mu
        # Exact kinematic sign checks: no real internal source/daughter.
        safe=min(float(np.min(dp0)),float(np.min(-dp1)),float(np.min(-dp2)),
                 dx0,float(np.min(-dx1)),float(np.min(-dx2)))
        self.min_safe_denominator=min(self.min_safe_denominator,safe)
        assert safe>0
        amp=-8*gh*((lam+gh*gh/dx0)/dp0+(lam+gh*gh/dx1)/dp1+(lam+gh*gh/dx2)/dp2)
        average=np.sum(self.aw*amp*amp,axis=1)
        raw=(root*np.sqrt(1-4/u)/np.sqrt(vv*(1-vv))).reshape(-1)
        integral=width*float(np.dot(self.uw,raw*average))
        return math.sqrt(1-4/s)*integral/(1024*math.pi**4*s)
    def gamma_scaled(self,T):
        # gamma_eq exp(4m/T). Final Phi Phi are identical (1/2!).
        th=T/m;emin=mu+2
        values=[]
        for y in self.ey:
            E=emin+th*y
            values.append(E*E*kve(1,E/th)*self.phase_integral(E)/(y*y))
        return m**4*th*th/(8*math.pi**3)*math.exp(-min((M-2*m)/T,750))*float(np.dot(self.ew,values))

def scaled_densities(T):
    A=m*m*T*kve(2,m/T)/(2*math.pi**2)
    B=M*M*T*kve(2,M/T)/(2*math.pi**2)*math.exp(-min((M-2*m)/T,750))
    return A,B

def pair_reverse(T):
    y,w=roots_genlaguerre(128,.5)
    x=M/T;ds=4*M*T*y+T*T*y*y;s=4*M*M+ds
    value=np.sqrt((s-4*m*m)*(4*M*T+T*T*y))/(M**4+m*m*ds)*kve(1,2*x+y)
    return float(g**4*np.dot(w,value)/(4*math.pi*M**4*kve(2,x)**2))

coarse=Thermal(24,12,6,12)
fine=Thermal(40,20,10,20)
rows=[]
for ratio in (.003,.01,.03,.1,.3,1.,3.):
    T=m*ratio
    low,high=coarse.gamma_scaled(T),fine.gamma_scaled(T)
    A,B=scaled_densities(T)
    nr=K3zero*B*A*A
    pair=B*B*pair_reverse(T)
    rows.append(dict(Tdark_over_m=ratio,T_dark_GeV=T,
         gamma3_eq_exp4mT_GeV4=high,coarse_relative_difference=low/high-1,
         gamma3_over_NR_limit=high/nr,
         two_conjugate_channels_over_pair_coefficient=2*high/pair))
    check('thermal density positive ratio='+str(ratio),high>0)
    # This convergence gate is mathematical and may fail; do not relabel a
    # poorly resolved high-T integral as a physical rate.
    check('nested quadrature refinement ratio='+str(ratio),abs(low/high-1)<.02)
check('NR reaction-density normalization',abs(rows[0]['gamma3_over_NR_limit']-1)<.04)

result=dict(verdict='Pole-free source-assisted thermal kernel evaluated within vacuum-tree common-MB narrow-source approximation',
            parameters=p,threshold_amplitude_GeVminus1=amp0,
            NR_event_coefficient_GeVminus5=K3zero,
            rows=rows,coarse_dimensions=coarse.dim,fine_dimensions=fine.dim,
            min_internal_denominator_over_m2=fine.min_safe_denominator,
            checks=checks,
            non_claims=['No full distributional real-intermediate-state subtraction',
                       'Other source-assisted crossings with source poles remain unmatched',
                       'No full Higgs-era production or rerun abundance prediction',
                       'Vacuum tree, ideal MB external states; medium/Bose/virial corrections absent',
                       'Finite quadrature agreement is not an analytic error bound',
                       'No galaxy law, dark-energy magnitude or global novelty established'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
print('All %d bounded thermal controls passed.'%len(checks))
