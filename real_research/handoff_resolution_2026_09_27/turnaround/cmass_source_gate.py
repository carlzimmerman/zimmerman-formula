#!/usr/bin/env python3
"""Conditional CMASS/source-gate audit using pinned FP23 profiles and FP20 projector.
No CMASS observational likelihood; uniform component-amplitude bound is not an arbitrary radial-mask bound.
MUTATE deletes retained exterior source mass and must fail source_mass_conservation.
"""
from pathlib import Path
import json,math,os,hashlib
for _v in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS'): os.environ[_v]='2'
import numpy as np
from scipy.special import erfc
from classy import Class
HERE=Path(__file__).resolve().parent; MIR=HERE/'mirror'; CHAIN=MIR/'real_research/derivation_chain_2026'
MUT=os.environ.get('MUTATE')=='1'; out={'mutate':MUT,'checks':{},'cmass_amplitude_bounds':{},'source_profiles':{},'mass_budget':{},'late_web_form_factor':{}}
def check(n,ok,v):out['checks'][n]={'ok':bool(ok),'value':v}
fp23=json.loads((CHAIN/'FP23_galaxy_lensing_web_field_results.json').read_text())['numbers']['C']
for z,d in fp23.items():
 for foot in ['canonical','alt']:
  p=d['prof'][foot]['central']; parts={k:np.array(v) for k,v in p['parts'].items()}; R=np.array(p['R']); lcdm=np.array(p['lcdm']); chain=np.array(p['chain'])
  summed=sum(parts[k] for k in ['baryons','phantom','carrier retained','carrier escaped','2-halo'])
  check(f'decomposition/{z}/{foot}',np.max(abs(summed-chain))<1e-8,float(np.max(abs(summed-chain))))
  fixed=parts['baryons']+parts['carrier retained']+parts['carrier escaped']+parts['LCDM 2-halo']
  web=parts['2-halo']-parts['LCDM 2-halo']; ph=parts['phantom']
  lower=(fixed+np.minimum(ph,0)+np.minimum(web,0))/lcdm
  upper=(fixed+np.maximum(ph,0)+np.maximum(web,0))/lcdm
  out['cmass_amplitude_bounds'][f'{z}/{foot}']={'R':[.1,.3,1.,3.,10.],'baseline_ratio':[float(np.interp(r,R,chain/lcdm)) for r in [.1,.3,1.,3.,10.]],'lower':[float(np.interp(r,R,lower)) for r in [.1,.3,1.,3.,10.]],'upper':[float(np.interp(r,R,upper)) for r in [.1,.3,1.,3.,10.]],'scope':'independent alpha,beta in [0,1] multiplying saved 1-halo phantom and 2-halo excess profiles, fixed other components'}
# Rebuild the FP23 central HOD and baseline halo using its exact definitions and constants.
G=6.67430e-11; MPC=3.0857e22; PC=MPC/1e6; MS=1.98892e30
# Source FP6 uses distinct cosmological Mpc and lensing MPCm: preserve both.
s6=(CHAIN/'FP6_gate_survey.py').read_text(); ns={}
# Fixed constants match inspected FP6; its cosmological Mpc is precise.
Mpc_cos=3.0856775814913673e22; h=.6736; ob=.02237; oc=.1200; Om=(ob+oc)/h**2; FB=ob/(ob+oc); H0=100*h*1e3/Mpc_cos; rhoc=3*H0**2/(8*math.pi*G)
c=2.99792458e8; Og=(4*5.670374419e-8*2.7255**4/c**3)/rhoc; Or=Og*(1+3.046*(7/8)*(4/11)**(4/3)); OL=1-Om-Or
cl=Class(); cl.set({'h':h,'omega_b':ob,'omega_cdm':oc,'n_s':.965,'T_cmb':2.7255,'N_ur':3.046,'N_ncdm':0,'sigma8':.811,'output':'mPk','P_k_max_h/Mpc':120.,'z_max_pk':60.,'non_linear':'halofit'}); cl.compute()
# Copy exact function bodies for the projector; no FP23 global execution.
s20=(CHAIN/'FP20_esd_projection_fix.py').read_text(); np20={'np':np,'math':math}; exec(s20[s20.index('def shell_mats('):s20.index('class M2Fix:')],np20)
Rc=np.geomspace(.1,30,36); RR=np.geomspace(1e-4,400,6000)*MPC; FIX=np20['ESDFix'](RR,Rc*MPC,PC,MS)
Mg=10**np.linspace(12.3,15.3,31); kk=np.geomspace(1e-4,50,3000); rhom0=Om*rhoc*MPC**3/MS
ret=json.loads((CHAIN/'FP16_daughter_reaccretion_results.json').read_text())['numbers']['X']['575']['group_ret_z05']; rm=np.array([float(k) for k in ret]); rv=np.array(list(ret.values()))
# Exact Newtonian first-turnaround coefficient using XR36 engine on a unit seed.
s36=(MIR/'real_research/cross_thread_review_2026_09_26/XR36_bound_regions.py').read_text(); nf={'np':np,'math':math,'G_':G,'MS_':MS,'MPC_':MPC,'KPC_':MPC/1000,'LG_H0':67.4*1e3/MPC,'LG_OM':(.02237+.1200)/.674**2,'LG_OL':1-(.02237+.1200)/.674**2}
# Override via FP6's declared LG constants read from its source below if constants differ.
exec(s36[s36.index('def Hof('):s36.index('def W_on(')],nf)
flow=nf['flow_batch']([1e11],9.3603e-11,gate='off',conv='B',z_out=(.5,.65),N1=300,N2=200,nstep=3000)
A0={'canonical':9.3603e-11,'alt':1.1312e-10}
for z in [.5,.65]:
 a=1/(1+z); pk=np.array([cl.pk_lin(k,z) for k in kk]); radii=(3*Mg/(4*math.pi*rhom0))**(1/3)
 sig=[]
 for R in radii:
  x=kk*R; W=3*(np.sin(x)-x*np.cos(x))/x**3;sig.append(np.sqrt(np.trapz(kk**3*pk*W**2/(2*math.pi**2),np.log(kk))))
 nu=1.686/np.array(sig); aa=.707; pp=.3; AA=.3222
 nuf=AA*np.sqrt(2*aa*nu**2/math.pi)*(1+(aa*nu**2)**(-pp))*np.exp(-aa*nu**2/2); dnd=rhom0/Mg*nuf*abs(np.gradient(np.log(nu),np.log(Mg)))
 Ncen=.5*erfc(np.log(10**13.08/h/Mg)/(np.sqrt(2)*.98)); w=dnd*Ncen; w/=w.sum(); mask=w>=1e-5; w=w[mask]; M=Mg[mask]; w/=w.sum()
 bias=1+(aa*nu**2-1)/1.686+2*pp/(1.686*(1+(aa*nu**2)**pp)); bgal=float(np.sum((dnd*Ncen)/(dnd*Ncen).sum()*bias)); bref=fp23[str(z)]['bias']
 check(f'HOD_bias/{z}',abs(bgal/bref-1)<1e-4,{'new':bgal,'baseline':bref,'relative':bgal/bref-1})
 r0unit=float(flow[z]['R0'][0]); rhocz=rhoc*(Om/a**3+Or/a**4+OL)
 for foot,a0 in A0.items():
  profs={k:np.zeros(36) for k in ['lcdm1','base_no_phantom','source_gate','flux_gate','conserved_replacement']}; masses=[]; edges=[]; shell_error=[]; kh=np.geomspace(1e-5,1,51); spectral=np.zeros(51); moment2=0.; meanMh=0.
  for Mh,wt in zip(M,w):
   r200=(3*Mh*MS/(4*math.pi*200*rhocz))**(1/3); cc=5.71*(Mh*h/2e12)**(-.084)*(1+z)**(-.47); rs=r200/cc; mf=lambda x:np.log1p(x)-x/(1+x)
   nfw=lambda r:Mh*MS*mf(np.minimum(r,r200)/rs)/mf(cc)
   Ms=10**11.4*MS; rcg=.07*r200; gas=max(.157*Mh*MS-Ms,0)
   mb=lambda r:Ms*r**2/(r+.005*MPC)**2+gas*(np.minimum(r,r200)/rcg-np.arctan(np.minimum(r,r200)/rcg))/(r200/rcg-np.arctan(r200/rcg))
   X=float(np.exp(np.interp(np.log(Mh),np.log(rm),np.log(rv)))); car=(1-FB)*Mh*MS; seed=(Ms+gas+X*car)/MS; edge=r0unit*(seed/1e11)**(1/3)*MPC
   massbar=mb(RR); yy=G*massbar/RR**2/a0; Mph=(np.sqrt(1+1/yy)-1)*massbar
   yy_e=G*mb(edge)/edge**2/a0; edge_mass=float((np.sqrt(1+1/yy_e)-1)*mb(edge))
   source=np.where(RR<edge,Mph,edge_mass); flux=np.where(RR<edge,Mph,0.)
   if MUT: source=flux.copy()
   check(f'source_mass_conservation/{z}/{foot}/{Mh}',abs(source[-1]/edge_mass-1)<1e-12,float(source[-1]/edge_mass))
   retained=X*(1-FB)*nfw(RR); escaped=(1-X)*car*np.minimum(RR/(5*MPC),1.)**3
   base=massbar+retained+escaped
   for k,m in [('lcdm1',nfw(RR)),('base_no_phantom',base),('source_gate',base+source),('flux_gate',base+flux),('conserved_replacement',massbar+np.minimum(source,Mh*MS-(Ms+gas)))]: profs[k]+=wt*FIX(m,0.)
   masses.append(edge_mass/MS);edges.append(edge/MPC)
   # Separate compact-support control: truncate baryon tail at max(turnaround,R200), retain any remaining dark mass in boundary reservoir.
   cut=max(edge,r200); rcap=np.minimum(RR,cut); bcap=mb(rcap); budget=Mh*MS-mb(cut)
   yc=G*bcap/np.maximum(rcap,1.)**2/a0; phcap=(np.sqrt(1+1/yc)-1)*bcap
   replacement=bcap+np.minimum(phcap,budget)
   replacement=np.where(RR>=cut,Mh*MS,replacement)
   diffmass=np.diff(np.r_[0.,replacement-nfw(RR)])/MS
   rrcom=np.r_[RR[0]/2,(RR[1:]+RR[:-1])/2]/MPC/a
   check(f'compact_mass_zero/{z}/{foot}/{Mh}',abs(diffmass.sum()/Mh)<1e-12,float(diffmass.sum()/Mh))
   spectral+=wt*np.array([np.sum(diffmass*(np.sinc(k*h*rrcom/np.pi)-1)) for k in kh])
   moment2+=wt*np.sum(diffmass*rrcom**2); meanMh+=wt*Mh
  saved=fp23[str(z)]['prof'][foot]['central']; parts=saved['parts']; lcdm=np.array(saved['lcdm']); oldl=np.array(parts['LCDM 1-halo']); err=np.max(abs(profs['lcdm1']-oldl)/np.maximum(abs(oldl),1e-6))
  check(f'LCDM_1halo/{z}/{foot}',err<1e-4,float(err))
  two=np.array(parts['LCDM 2-halo']); profs={k:v+two for k,v in profs.items()}
  out['source_profiles'][f'{z}/{foot}']={'R':Rc.tolist(),'ratios':{k:(v/lcdm).tolist() for k,v in profs.items()},'at_R_0.1_0.3_1_3_10':{k:[float(np.interp(r,Rc,v/lcdm)) for r in [.1,.3,1,3,10]] for k,v in profs.items()},'HOD_mean_edge_Mpc':float(np.dot(w,edges)),'HOD_mean_phantom_mass_Msun':float(np.dot(w,masses)),'HOD_mean_seed_mass_note':'constant compact baryons+retained-carrier surrogate, gas truncated at R200','r0unit':r0unit}
  # Additional retained mass budget in selected central population, no abundance renormalization.
  nsel=float(np.sum((dnd*Ncen)[mask])*(np.log(Mg[1])-np.log(Mg[0]))); excess=float(np.dot(w,masses))*nsel/rhom0
  out['late_web_form_factor'][f'{z}/{foot}']={'k_h_Mpc':kh.tolist(),'delta_u':(spectral/meanMh).tolist(),'small_k_delta_u_over_kh2':float(spectral[0]/meanMh/kh[0]**2),'analytic_coefficient':float(-h*h*moment2/(6*meanMh)),'scope':'compact mass-conserving replacement minus truncated NFW, density form factor only; no nonlinear power prediction'}
  check(f'compensated_small_k/{z}/{foot}',abs(spectral[0]/kh[0]**2/(-h*h*moment2/6)-1)<1e-4,float(spectral[0]/kh[0]**2/(-h*h*moment2/6)-1))
  out['mass_budget'][f'{z}/{foot}']={'number_density_Mpc3':nsel,'phantom_mean_fraction_of_matter_density':excess,'status':'additive source gate must displace this dark-matter mean or alter background; selected population only'}
out['scope']='conditional central-HOD, baryonic P2 source gate with uniform frame subtraction, zero yield, LCDM two-halo, source mask determined by constant compact seed proxy; not fitted data or action-derived regime'
out['verdict']='pass' if all(v['ok'] for v in out['checks'].values()) else 'failed'
(HERE/f"cmass_source_gate_results{'_MUTATE' if MUT else ''}.json").write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k not in ['checks','source_profiles']},indent=2)); print('failed',[(k,v) for k,v in out['checks'].items() if not v['ok']][:8]);raise SystemExit(0 if out['verdict']=='pass' else 1)
