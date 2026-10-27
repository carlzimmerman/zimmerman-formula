"""Conditional hot-radiation-era relaxation and instantaneous entropy diagnostic."""
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import kv
prior=json.loads(Path('sol61_push/ordinary_lepton_source_2026_10_13/run/results.json').read_text())
wall=json.loads(Path('sol61_push/electron_material_wall_2026_10_13/run/results.json').read_text())
MR=2e6;me=510998.95;Mpl=1.220890e28;hb=6.582119569e-16
checks=[]
def ck(n,v):checks.append({'name':n,'passed':bool(v)});assert v,n
# BE sign=-1, FD sign=+1; degeneracy g. Stable exponential form.
def thermo(x,g,sign):
 def occ(q):
  E=math.sqrt(q*q+x*x);z=math.exp(-E)
  return z/(1+sign*z)
 ir=quad(lambda q:q*q*math.sqrt(q*q+x*x)*occ(q),0,100,epsabs=1e-11,epsrel=1e-11)[0]
 ip=quad(lambda q:q**4/(3*math.sqrt(q*q+x*x))*occ(q),0,100,epsabs=1e-11,epsrel=1e-11)[0]
 return 15*g/math.pi**4*ir,45*g/(4*math.pi**4)*(ir+ip)
# Independent Bessel expansion for entropy, valid at positive mass/T.
def entropy_series(x,g,sign,nmax=400):
 return 45*g*x*x/(4*math.pi**4)*sum((-sign)**(n-1)*(4*kv(2,n*x)/n**2+x*kv(1,n*x)/n) for n in range(1,nmax+1))
ck('massless boson normalization',math.isclose(thermo(0,1,-1)[1],1,rel_tol=1e-10))
ck('massless fermion normalization',math.isclose(thermo(0,4,1)[1],3.5,rel_tol=1e-10))
rows=[]
for T in [1.5e6,2e6,3e6]:
 x=MR/T
 rhoR,sR=thermo(x,1,-1);rhoe,se=thermo(me/T,4,1)
 ck('boson entropy Bessel '+str(T),math.isclose(sR,entropy_series(x,1,-1),rel_tol=1e-10))
 ck('electron entropy Bessel '+str(T),math.isclose(se,entropy_series(me/T,4,1),rel_tol=1e-10))
 rho=2+rhoe+rhoR+5.25 # neutrinos at same T, no carrier population included
 H=math.sqrt(8*math.pi**3*rho/90)*T*T/Mpl
 av=kv(1,x)/kv(2,x)
 norm=quad(lambda q:q*q*math.exp(-math.sqrt(q*q+x*x)),0,100)[0]
 avgnum=quad(lambda q:q*q*x/math.sqrt(q*q+x*x)*math.exp(-math.sqrt(q*q+x*x)),0,100)[0]
 ck('time dilation integral '+str(T),math.isclose(av,avgnum/norm,rel_tol=1e-10))
 gg=prior['reduced_muon_case']['photon_width_eV']
 ee=wall['rows'][0]['electron_width_eV']
 rate0=gg*av/H;ratee=ee*av/H
 gsEM=2+se
 baseline=3*(5.5/gsEM)**(4/3)
 toy=3*(5.5/(gsEM+sR))**(4/3)
 rows.append({'T_MeV':T/1e6,'g_rho_assumed':rho,'H_per_s':H/hb,'source_entropy_dof':sR,
 'electron_entropy_dof':se,'MB_time_dilation':av,
 'muon_only_photon_relaxation_over_H':rate0,
 'weak_ye_1e_8_electron_relaxation_over_H':ratee,
 'ye_electron_channel_alone_rate_equals_H':1e-8/math.sqrt(ratee),
 'instantaneous_Neff_without_R':baseline,'instantaneous_Neff_with_R_only':toy,
 'source_entropy_suppression_ratio':toy/baseline})
result={'all_pass':all(c['passed'] for c in checks),'checks':checks,'rows':rows,
 'assumptions':['Radiation-dominated GR expansion with reheating above sampled temperatures',
 'R has specified vacuum widths and negligible chemical potential near equilibrium',
 'Maxwell-Boltzmann collision averaging; no plasma corrections',
 'Instantaneous neutrino decoupling toy model at each stated T; R entropy entirely returns to electromagnetic sector',
 'Carrier population omitted in entropy toy; no full neutrino or dark-sector kinetic solution'],
 'non_claims':['No precision Neff prediction or cosmological confidence limit',
 'No measured existence of R, no certification of model-independent exclusion']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
