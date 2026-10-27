"""CE-FM-066: target-fraction energy obligation, no original census fit rerun."""
import json,math,sys
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.integrate import quad
P=Path('campaign_fresh_gravity/CFG806_census_from_framework');rec=json.loads((P/'cfg806_results.json').read_text());D=json.loads(Path('campaign_fresh_gravity/CFG654_independent_inputs/cfg654_delta_ta.json').read_text());delta=float(np.interp(0,D['z'],D['D']))
G,ms,kpc=6.674e-11,1.989e30,3.0857e19;fb=1/6.364;rho=2.77536627e11*.31285*.67403**2/1e9;esn=1e42/ms
checks=[]
def ck(name,v):
 checks.append({'name':name,'pass':bool(v)})
 if not v:raise AssertionError(name)
x=sp.symbols('x',positive=True);F=sp.asinh(2*x)-(1+sp.sqrt(1+4*x*x))/(2*x)
ck('exact canonical potential primitive',sp.simplify(sp.diff(F,x)-(1+sp.sqrt(1+4*x*x))/(2*x*x))==0)
prim=lambda x:math.asinh(2*x)-(1+math.sqrt(1+4*x*x))/(2*x)
def system(lm,f,a0):
 Mta=10**lm;Mb=f*fb*Mta*ms;rM=math.sqrt(G*Mb/a0);rt=(3*Mta/(4*math.pi*delta*rho))**(1/3)*kpc;V=(G*Mb*a0)**.25;xx=rt/rM
 return Mb,rM,rt,V,a0*rM*(prim(max(xx,1.0001))-prim(1))
def cooling(Mb,V,rt):
 T=.6*1.6726e-27*V*V/(2*1.380649e-23);kt=np.clip(1.380649e-16*T/1.602177e-9,.01,20)
 lam=(.0086*kt**-1.7+.058*kt**.5+.063)*1e-22
 # t_cool=A r^2 for rho=M/(4pi rt r^2), with n/nH=2.3, ne/nH=1.17.
 A=3*2.3**2*1.380649e-16*T*.6*1.6726e-24*4*math.pi*(rt*100)/(2*1.17*lam*(Mb*1000))
 return min(1,1/(A*V*100)/(rt*100)),T
rows=[]
for foot,a0 in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
 for lm,fc in [(12,.1),(13,.325),(14,.7),(15,.9)]:
  Mb,rm,rt,V,dp=system(lm,fc,a0)
  q=quad(lambda lr:(.5*G*Mb/math.exp(2*lr)+math.sqrt(.25*(G*Mb/math.exp(2*lr))**2+G*Mb/math.exp(2*lr)*a0))*math.exp(lr),math.log(rm),math.log(rt))[0]
  ck('closed potential vs quadrature '+foot+str(lm),abs(dp/q-1)<1e-12)
  req=(1-fc)*dp/(fc*esn);chi,T=cooling(Mb,V,rt)
  ck('target energy identity '+foot+str(lm),abs(fc*(1+req*esn/dp)-1)<1e-14)
  rows.append({'foot':foot,'logMta_physical_Msun':lm,'target_f':fc,'rt_over_rM':rt/rm,'deltaPhi_m2_s2':dp,'required_epsilon_times_stellarformed_over_retainedmass':req,'required_stellarformed_over_retained_at_epsilon0p1':req/.1,'minimum_epsilon_if_all_initial_catchment_baryons_form_stars_once':fc*req,'target_chi_frozen_diffuse_cooling':chi,'epsilon_needed_with_frozen_cooling':req/chi})
  for model,label in [('M1','M1 (s=1) eps=1 '+foot),('M2','M2 PRIMARY eps=1 '+foot)]:
   f=rec['runs'][label]['f'][str(lm)];Mb,rm,rt,V,dp=system(lm,f,a0);s=1 if model=='M1' else cooling(Mb,V,rt)[0];res=f*(1+esn*s/dp)-1
   ck('saved root residual '+foot+model+str(lm),abs(res)<1e-8)
 ck('primary saved failure '+foot,rec['runs']['M2 PRIMARY eps=1 '+foot]['cls']=='NOT DERIVED')
ck('epsilon0p1 fails even all-baryons-once benchmark',all(z['minimum_epsilon_if_all_initial_catchment_baryons_form_stars_once']>.1 for z in rows))
# These frozen one-zone equations, not arbitrary time-dependent feedback.
result={'claim_id':'CE-FM-066','n_checks':len(checks),'all_pass':all(z['pass'] for z in checks),'checks':checks,'rows':rows,'scope':'Physical Msun trial-mass dictionary of CFG806; census target labels retained as declared, not a new mass conversion or census calibration. Conditional final-point-potential energy budget from rM to rta with fixed energy per formed star; no original fit, new cooling profile or feedback history.'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checks':len(checks),'all_pass':result['all_pass'],'canonical':[z for z in rows if z['foot']=='canonical']}))
