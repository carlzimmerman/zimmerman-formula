"""Two-temperature MB collision model; equilibrium R only, no phi kinetics/QED."""
import json,sys,math
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import solve_ivp
pi=math.pi;me=.51099895;GF=1.1664e-11;sw2=.223;Mpl=1.220890e22
C=3-4*sw2+24*sw2**2
checks=[]
def ck(n,v):checks.append({'name':n,'passed':bool(v)});assert v,n
class Model:
 def __init__(self,n,Rmass=None,Qon=True):
  q,w=leggauss(n);self.q=(q+1)*40;self.w=w*40;self.mass=Rmass;self.Qon=Qon
 def species(self,T,m,g,sgn):
  q=self.q;E=np.sqrt(q*q+(m/T)**2);z=np.exp(-E);f=z/(1+sgn*z)
  pre=g/(2*pi*pi)
  rho=pre*T**4*np.dot(self.w,q*q*E*f)
  pressure=pre*T**4*np.dot(self.w,q**4/(3*E)*f)
  derivative=pre*T**3*np.dot(self.w,q*q*E*E*f*(1-sgn*f))
  return np.array([rho,pressure,derivative])
 def em(self,T):
  r=pi*pi/15*T**4
  out=np.array([r,r/3,4*r/T])+self.species(T,me,4,1)
  if self.mass is not None:out+=self.species(T,self.mass,1,-1)
  return out
 def terms(self,Y):
  Tg,Tn=np.exp(Y);r,p,d=self.em(Tg);rn=7*pi*pi/40*Tn**4
  H=math.sqrt(8*pi*(r+rn)/3)/Mpl
  F=(Tg-Tn)*(32*sum(Tg**(8-i)*Tn**i for i in range(9))+56*Tg**4*Tn**4)
  Q=GF*GF/pi**5*C*F if self.Qon else 0.
  return Tg,Tn,r,p,d,rn,H,Q
 def rhs(self,u,Y):
  Tg,Tn,r,p,d,rn,H,Q=self.terms(Y)
  return [-(3*(r+p)+Q/H)/(Tg*d),-1+Q/(4*H*rn)]
 def run(self,start=10.,rtol=1e-8):
  def end(u,Y):return math.exp(Y[0])-.01
  end.terminal=True;end.direction=-1
  sol=solve_ivp(self.rhs,(0,10),np.log([start,start]),method='Radau',rtol=rtol,atol=rtol/50,events=end,dense_output=True)
  ck('solver '+str((self.mass,self.Qon,start,rtol,len(self.q))),sol.success and len(sol.t_events[0])==1)
  Tg,Tn=np.exp(sol.y[:,-1]);neff=3*(11/4)**(4/3)*(Tn/Tg)**4
  max_res=0.
  for u in np.linspace(0,sol.t[-1],31):
   Y=sol.sol(u);Tg,Tn,r,p,d,rn,H,Q=self.terms(Y);dg,dn=self.rhs(u,Y)
   residual=Tg*d*dg+4*rn*dn+3*(r+p)+4*rn
   max_res=max(max_res,abs(residual)/(3*(r+p)+4*rn))
  ck('energy conservation '+str((self.mass,self.Qon,start,rtol,len(self.q))),max_res<1e-10)
  return {'source_mass_MeV':self.mass,'weak_transfer':self.Qon,'start_MeV':start,'quadrature_nodes':len(self.q),'rtol':rtol,'Neff':neff,'final_Tgamma_over_Tnu':Tg/Tn,'steps':len(sol.t),'max_energy_residual':max_res}
# Heat capacity checked independently by finite differences of energy density.
for T in [.1,.5,2.,10.]:
 mod=Model(256,2.);r,p,d=mod.em(T);eps=1e-4
 numeric=(mod.em(T*(1+eps))[0]-mod.em(T*(1-eps))[0])/(2*eps*T)
 ck('heat capacity '+str(T),abs(numeric/d-1)<1e-7)
rows=[]
for mass in [None,2.]:
 a=Model(160,mass).run(rtol=1e-7);b=Model(320,mass).run(rtol=2e-9);c=Model(320,mass).run(start=5.,rtol=2e-9)
 ck('numerical refinement '+str(mass),abs(a['Neff']-b['Neff'])<1e-5)
 ck('initial temperature comparison '+str(mass),abs(c['Neff']-b['Neff'])<.001)
 rows.extend([a,b,c])
# With weak exchange turned off at 2 MeV, recover entropy conservation exactly.
for mass in [None,2.]:
 mod=Model(320,mass,False);row=mod.run(start=2.,rtol=2e-9);rows.append(row)
 r,p,_=mod.em(2.);gs=45/(2*pi*pi)*(r+p)/2.**4
 analytic=3*(5.5/gs)**(4/3)
 ck('instantaneous entropy recovery '+str(mass),abs(row['Neff']-analytic)<1e-6)
 row['entropy_formula_Neff']=analytic
baseline=rows[1]['Neff'];withR=rows[4]['Neff']
ck('published MB SM baseline',abs(baseline-3.042)<.002)
result={'all_pass':all(c['passed'] for c in checks),'checks':checks,'rows':rows,'refined_baseline_Neff':baseline,'refined_R_only_Neff':withR,'R_only_shift':withR-baseline,
 'non_claims':['No phi population or energy-transfer calculation',
 'R remains at zero-chemical-potential EM equilibrium by assumption',
 'No finite-temperature QED, full quantum weak collision integrals, spectral distortion or neutrino flavor separation',
 'Not a cosmological likelihood or exclusion of the full production model']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
