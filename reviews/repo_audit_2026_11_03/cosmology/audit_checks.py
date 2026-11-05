#!/usr/bin/env python3
"""Independent bounded audits; no project modules imported or repository writes."""
import json, math, time, hashlib, platform, sys, subprocess
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.special import erf
ROOT=Path('/Users/carlzimmerman/new_physics/zimmerman-formula')
OUT=Path('/private/tmp/cosmology_core_audit_20261103')
FILES=[
'rebuild_2026_10_22/AN1_aest_nonlinear_dust/an1.py',
'rebuild_2026_10_22/AN1_aest_nonlinear_dust/an1_v3.py',
'rebuild_2026_10_22/AN1_aest_nonlinear_dust/FROZEN_CRITERIA.md',
'rebuild_2026_10_22/AN1_aest_nonlinear_dust/README_V3.md',
'rebuild_2026_10_22/AN2_aest_3d_fold/an2.py',
'rebuild_2026_10_22/AN2_aest_3d_fold/an2_shapes.json',
'rebuild_2026_10_22/BOLTZ1_covariant_closure/README.md',
'rebuild_2026_10_22/X48_native_cf_zoom/stable_stress_search/entropy_transport/floor_theorem/preservation_route.md']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs=[dict(path=str(ROOT/p).lstrip('/'),sha256=sha(ROOT/p)) for p in FILES]
started=time.time()
G=4.30091e-6; TU=0.97779; H0=.0672; rx=33.2; rb=rx/5.35; rm=rx+rb
Om=rm/(3*H0**2/(8*math.pi*G)); OL=1-Om; Lam=OL*H0**2; A=4*math.pi*G*rm/3; ai=1/21
at=lambda t:(Om/OL)**(1/3)*np.sinh(1.5*math.sqrt(OL)*H0*t)**(2/3)
tat=lambda a:math.asinh(math.sqrt(OL/Om)*a**1.5)/(1.5*math.sqrt(OL)*H0)
ti=tat(ai); tnow=tat(1); Hi=H0*math.sqrt(Om/ai**3+OL)
# x=r/q gives an exact scale-free uniform-sphere ODE, independent of mass.
def sphere(d,thresh=1e-6):
 def fun(t,y):return [y[1],-A/y[0]**2+Lam*y[0]]
 def end(t,y):return y[0]-thresh*ai
 end.terminal=True; end.direction=-1
 s=solve_ivp(fun,(ti,3*tnow),[ai*(1-d/3),Hi*ai*(1-2*d/3)],events=end,rtol=2e-11,atol=2e-13,method='DOP853')
 assert s.success and len(s.t_events[0])==1
 t=float(s.t_events[0][0]);return dict(t_Gyr=t*TU,z=1/at(t)-1)
shape=json.loads((ROOT/FILES[5]).read_text())['1e12']; d0=shape['d0']; qr=shape['qt']/shape['RG']
checks={'sphere':sphere(.2030),'sphere_box_mean_0p0082':sphere(.2030*(1-.0082))}
# True Gaussian shell focusing need not preserve r1*k/rk=1 (K11).
ks=np.array([1,2,3,5],float)
checks['gaussian_exact_K11']=[]
for N in (300,1200,4800):
 xx=2*qr*ks/N
 gm=3/xx**3*(math.sqrt(math.pi/2)*erf(xx/math.sqrt(2))-xx*np.exp(-xx*xx/2))
 ds=d0*gm
 def ode(t,y):
  x=y[:4];return np.r_[y[4:],-A/x**2+Lam*x]
 def end(t,y):return y[0]/at(t)-1e-3
 end.terminal=True;end.direction=-1
 sol=solve_ivp(ode,(ti,3*tnow),np.r_[ai*(1-ds/3),Hi*ai*(1-2*ds/3)],events=end,rtol=1e-11,atol=1e-13,method='DOP853')
 assert sol.success and len(sol.t_events[0])==1
 x=sol.y_events[0][0][:4]
 dev=max(abs(x[0]/x[1:]-1))
 checks['gaussian_exact_K11'].append(dict(N=N,t_Gyr=float(sol.t_events[0][0])*TU,ratios=(x[0]/x[1:]).tolist(),max_dev=float(dev),frozen_K11_limit=.02,passes_frozen_line=bool(dev<=.02)))
# Enclosed mass within the first uniform-density cell, x=r/r_edge.
checks['central_interpolation']=[dict(r_over_cell=x,linear_mass=x,true_mass=x**3,force_ratio=x**-2) for x in (.25,.5,.75)]
# Blank homogeneous universe produces false positive for AN2 total-mass capture read.
R=1350.; z=20.; V=4*math.pi*R**3/3; Md=V*rx*(1+z)**3; Mb=V*rb*(1+z)**3; gN=G*Mb/R**2
checks['unperturbed_capture']={}
for foot,a0SI in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
 a0=a0SI/3.24078e-14; gl=.5*(gN+math.sqrt(gN*gN+4*gN*a0)); Mph=(gl-gN)*R**2/G
 checks['unperturbed_capture'][foot]=dict(Md=Md,Mb=Mb,Mph=Mph,Md_over_Mph=Md/Mph,passes_Md_ge_Mph=Md>=Mph,true_excess_field_mass=0)
# Exact tanh release single-barotrope derivative: c_a^2=-S'/(3 S).
w=.05
checks['single_barotrope_step']=[dict(loga_offset_in_widths=x,S=.5*(1+math.tanh(x)),ca2=-(1-math.tanh(x))/(3*w)) for x in (-5,-1,0,1,5)]
checks['prefix_preservation_examples']=[dict(Ms=ms,Mc=mc,bound_per_k0=((ms-mc)/(1-mc))**3) for ms,mc in[(.10,.05),(.25,.05)]]
checks['gaussian_focus_asymptotic']={str(k):1-k**(-4/3) for k in (2,3,5)}
for row in inputs:row['sha256_after']=sha(Path('/')/row['path'])
assert all(x['sha256']==x['sha256_after'] for x in inputs)
result=OUT/'results.json';result.write_text(json.dumps(checks,indent=2)+'\n')
manifest={
'schema_version':2,'claim_id':'INDEPENDENT-COSMOLOGY-CORE-20261103',
'repository':{'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'dirty':bool(subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True))},
'command':[sys.executable,str(Path(__file__).resolve())],
'environment':{'software':[{'name':'python','version':platform.python_version()},{'name':'numpy','version':np.__version__},{'name':'scipy','version':scipy.__version__}],'hardware':platform.platform()},
'mathematics':{'assertion_tested':'Independent dimensionless dust-sphere and Gaussian shell integration; exact central-cell mass interpolation ratio; unperturbed-background capture false positive; barotrope release sign; conditional prefix bound arithmetic.','coefficient_domain':'binary64 ODE integrations plus analytic identities','conventions':'Project G/H0/rho units; a0 canonical and alt separately; no project implementation imported','inputs':FILES,'bounds':{'N_diagnostic':[300,1200,4800],'ODE_rtol':1e-11,'ODE_atol':1e-13},'non_claims':['No full AN1/AN2 solver reproduction','No nonlinear 3D AeST conclusion','No unconditional X48 entropy floor','No action closure or empirical pass']},
'randomness':{'used':False,'generator':'','seed':None},
'run':{'started_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(started)),'runtime_seconds':time.time()-started,'exit_status':0,'status':'completed','resource_limits':{'memory_bytes':None,'cpu_seconds':None,'max_cores':1,'max_threads':1}},
'outputs':[{'path':str(result).lstrip('/'),'sha256':sha(result),'kind':'result'}],
'checks':['all ODE events reached successfully','input hashes unchanged','independent mathematical reconstruction; no repo modules imported'],
'result':'Control and interpretation obstructions corroborated; numerical integrations conditional on tolerance.','residual_risks':['No outward-rounded ODE certificate','Background mean subtraction fraction .0082 taken from diagnostic note as rounded value','No external-source authentication needed for local identities'],
'input_artifacts':inputs+[{'path':str(Path(__file__).resolve()).lstrip('/'),'sha256':sha(Path(__file__).resolve()),'sha256_after':sha(Path(__file__).resolve())}],
'declared_results':[str(result).lstrip('/')]}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(checks,indent=2))
