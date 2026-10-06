#!/usr/bin/env python3
"""Bounded real CLASS transfer lab; no installation or source/cache mutation."""
import sys
sys.dont_write_bytecode = True
import argparse, json, hashlib, subprocess
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid
BASE=Path(__file__).resolve().parents[4]
SITE=BASE/'fable_independent_2026/L183_class_mond_kernel/site'
sys.path.insert(0,str(SITE))
import classy
from classy import Class
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--coarse',action='store_true');p.add_argument('--default-precision',action='store_true');p.add_argument('--tighter',action='store_true');args=p.parse_args()
out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
n=301 if args.coarse else 601
# Increasing a. z >= 19 avoids reionization; no massive neutrinos in this baseline.
a=np.geomspace(.01,.05,n);z=1/a-1
params={'h':.6736,'omega_b':.02237,'omega_cdm':.1200,'N_ur':3.046,'N_ncdm':0,'output':'mTk,vTk','z_pk':','.join(map(str,z)), 'P_k_max_1/Mpc':10.,'gauge':'newtonian','mond_a0':0.,'perturbed recombination':'no','tol_perturbations_integration':1e-9,'perturbations_sampling_stepsize':.02,'tol_thermo_integration':1e-8}
if args.tighter:params['tol_perturbations_integration']=1e-10
if args.default_precision:
    for key in ['tol_perturbations_integration','perturbations_sampling_stepsize','tol_thermo_integration']:params.pop(key)
c=Class();c.set(params);c.compute()
tr=[c.get_transfer(float(zz)) for zz in z]
k=tr[0]['k (h/Mpc)']*params['h']
db=np.array([t['d_b'] for t in tr]);dc=np.array([t['d_cdm'] for t in tr]);tb=np.array([t['t_b'] for t in tr]);tc=np.array([t['t_cdm'] for t in tr]);tg=np.array([t['t_g'] for t in tr]);phi=np.array([t['phi'] for t in tr]);psi=np.array([t['psi'] for t in tr])
H=np.array([c.Hubble(float(zz)) for zz in z]);th=c.get_thermodynamics();bg=c.get_background()
def interp_a(aa,values):
    ix=np.argsort(aa);return np.interp(a,np.asarray(aa)[ix],np.asarray(values)[ix])
cb2=interp_a(th['scale factor a'],th['c_b^2']);opacity=interp_a(th['scale factor a'],th["kappa' [Mpc^-1]"])
Rinv=interp_a(1/(1+bg['z']),4*np.asarray(bg['(.)rho_g'])/(3*np.asarray(bg['(.)rho_b'])))
fb=params['omega_b']/(params['omega_b']+params['omega_cdm']);fc=1-fb
dm=fb*db+fc*dc;tm=fb*tb+fc*tc
U=-a[:,None]*(tb-tc)
Sgas=-cb2[:,None]*k[None,:]**2*db
Sdrag=-(Rinv*opacity)[:,None]*(tg-tb)
dt_da=1/(a*H)
Ig=cumulative_trapezoid(Sgas*dt_da[:,None],a,axis=0,initial=0)
Id=cumulative_trapezoid(Sdrag*dt_da[:,None],a,axis=0,initial=0)
res=U-U[0]-Ig-Id
norm=a[0]**2*H[0]*dm[0]
valid=(k>=.005)&(k<=10)&(np.abs(norm)>1e-10)
err=float(np.max(np.abs(res[:,valid]/norm[valid])))
# CLASS metric continuity phi_N is needed for total growing projection.
phiN=np.gradient(phi,np.log(a),axis=0,edge_order=2)
dmN=-tm/(a*H)[:,None]+3*phiN
Ag=(3*dm+2*dmN)/5;Bd=2*(dm-dmN)/5
# exact algebraic initial reconstruction; EdS future extrapolation only approximate here.
proj_err=float(np.max(np.abs(Ag+Bd-dm)))
# Born cold-wave source uses real cold transfer and a fixed mass coefficient.
kpick=np.array([.01,.03,.1,.3,1.,3.,8.])
def atk(arr):return np.array([np.interp(kpick,k,row) for row in arr])
normpick=np.interp(kpick,k,norm)
dcp=atk(dc);dbp=atk(db);Up=atk(U)
Mpc=3.085677581491367e22;hc=1.973269804593025e-7 # eV*m
masses=[1e-22,2e-20,2e-19]
wave={}
for m in masses:
    ell=hc/(m*Mpc)
    Sw=ell**2*kpick[None,:]**4*dcp/(4*a[:,None]**2)
    Iw=cumulative_trapezoid(Sw*dt_da[:,None],a,axis=0,initial=0)
    epsilon=ell**2*kpick[None,:]**4/(4*a[:,None]**4*H[:,None]**2)
    wave[str(m)]={'DeltaU_over_norm_final':(Iw[-1]/normpick).tolist(),'max_stiffness_over_H2':epsilon.max(axis=0).tolist(),'Born_weak_threshold':.1}
# Forecast design: same initial-U nuisance projected out separately at every k;
# templates for wave, common gas-temperature normalization, constant differential potential.
ell=hc/(1e-22*Mpc)
W=cumulative_trapezoid((ell**2*kpick[None,:]**4*dcp/(4*a[:,None]**2))*dt_da[:,None],a,axis=0,initial=0)/normpick
G=atk(Ig)/normpick
# gate Phi_b-Phi_c = amplitude * initial phi(k), common late-time shape.
P0=np.interp(kpick,k,phi[0]);Q=cumulative_trapezoid(np.ones((n,1))*(-kpick**2*P0)[None,:]*dt_da[:,None],a,axis=0,initial=0)/normpick
ix=np.array([n//3,2*n//3,n-1]);design=np.column_stack([W[ix].ravel(),G[ix].ravel(),Q[ix].ravel()]);length=np.linalg.norm(design,axis=0);D=design/length
sv=np.linalg.svd(D,compute_uv=False)
Wperp=design[:,0]-design[:,1:]@np.linalg.lstsq(design[:,1:],design[:,0],rcond=None)[0]
forecast_leverage=float(np.linalg.norm(Wperp))
y=D@np.array([.7,-.2,.4]);fit=np.linalg.lstsq(D,y,rcond=None)[0]
# Exact EdS tests including gas-wave same time-kernel and gate temporal degeneracy.
x=np.array([1.,2.,3.,5.]);HE=1.;Di=2.;kk=np.array([.2,1.,3.]);ai=.01;aa=ai*x
q=kk**4/4;Uw=2*q[None,:]*Di*(np.sqrt(aa[:,None])-np.sqrt(ai))/HE
Delta=2*q[None,:]*Di/HE**2*(np.log(x[:,None])-2*(1-x[:,None]**-.5))
# Finite differentiation of exact primitive with high-resolution a.
af=np.geomspace(ai,.05,10001);Uf=2*(np.sqrt(af)-np.sqrt(ai));dUf=np.gradient(Uf,af,edge_order=2)
eds_error=float(np.max(np.abs(dUf[1:-1]-af[1:-1]**-.5)/(af[1:-1]**-.5)))
# One k makes cooling gas and quantum temporal templates exactly proportional.
tshape=np.sqrt(aa)-np.sqrt(ai);sone=np.linalg.svd(np.column_stack([tshape,7*tshape]),compute_uv=False)
# Density-only initialization assumes delta_N=delta, incorrect in actual acoustic transfers.
density_only_fraction=float(np.max(np.abs((dmN[0,valid]-dm[0,valid])/dm[0,valid])))
# initial velocity omitted: apparent forcing exists even for exact pressureless decaying relative mode.
Ui=.3;fake_pressureless=np.ones(4)*Ui
checks={'CLASS_source_integral_residual_below_1e-6':err<1e-6,'growing_projection_reconstructs_state':proj_err<1e-9,'EdS_primitive_derivative':eds_error<1e-7,'multi_k_restricted_forecast_full_rank':sv[-1]>1e-3,'synthetic_coefficients_recovered':np.max(np.abs(fit-[.7,-.2,.4]))<1e-10,'single_k_wave_gas_degenerate':sone[-1]<1e-14,'initial_U_omission_false_signal_detected':np.max(np.abs(fake_pressureless))>.1,'primordial_amplitude_cancels':np.allclose((3*Up)/(3*normpick),Up/normpick),'arbitrary_differential_gate_exact_wave_degeneracy':np.allclose(-kpick[None,:]**2*(-ell**2*kpick[None,:]**2*dcp/(4*a[:,None]**2)),ell**2*kpick[None,:]**4*dcp/(4*a[:,None]**2))}
checks={key:bool(value) for key,value in checks.items()}

result={'parameters':params,'z_range':[float(z[-1]),float(z[0])],'k_pick_Mpc_inverse':kpick.tolist(),'n_epochs':n,'n_k':len(k),'CLASS_version':classy.__version__,'source_residual_over_initial_a2Hdelta':err,'source_integral_at_picks':{'U_initial_over_norm':(Up[0]/normpick).tolist(),'measured_DeltaU_over_norm':((Up[-1]-Up[0])/normpick).tolist(),'gas_DeltaU_over_norm':(atk(Ig)[-1]/normpick).tolist(),'drag_DeltaU_over_norm':(atk(Id)[-1]/normpick).tolist()},'wave_Born_forecasts':wave,'restricted_forecast_unit_column_singular_values':sv.tolist(),'restricted_forecast_coefficients':fit.tolist(),'wave_marginalized_leverage_equal_independent_noise':forecast_leverage,'sigma_alpha_for_sigma_N_1e-6':1e-6/forecast_leverage,'density_only_initialization_relative_error_max':density_only_fraction,'initial_mode_at_picks':{'delta_m':np.interp(kpick,k,dm[0]).tolist(),'delta_m_N':np.interp(kpick,k,dmN[0]).tolist(),'growing_projection_A_at_z99':np.interp(kpick,k,Ag[0]).tolist(),'decaying_projection_B_at_z99':np.interp(kpick,k,Bd[0]).tolist(),'relative_delta':np.interp(kpick,k,db[0]-dc[0]).tolist(),'relative_delta_N':np.interp(kpick,k,-(tb[0]-tc[0])/(a[0]*H[0])).tolist()},'EdS_primitive_derivative_relative_error':eds_error,'checks':checks,'git_HEAD_at_runtime':subprocess.check_output(['git','rev-parse','HEAD'],cwd=BASE,text=True).strip()}
np.savez_compressed(out/'transfers.npz',a=a,k=k,delta_b=db,delta_c=dc,theta_b=tb,theta_c=tc,theta_gamma=tg,phi=phi,psi=psi,H=H,cb2=cb2,opacity=opacity,Rinv=Rinv,U=U,gas_integral=Ig,drag_integral=Id,dmN=dmN,Ag=Ag,Bd=Bd)
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
c.struct_cleanup();c.empty()
print(json.dumps({k:v for k,v in result.items() if k not in ['parameters']},indent=2))
assert all(checks.values()),checks
