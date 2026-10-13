"""Isotropic nonrelativistic three-wave kinetics, conservative finite energy grid."""
import json,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
p=Path(__file__).parent
params=json.loads((p/'repulsive_envelope_run/results.json').read_text())['parameters']
m=params['m_eV'];g=params['cubic_g_eV'];u=params['u']
c=299792458.;hbev=1.054571817e-34/1.602176634e-19;hc=hbev*c;year=365.25*86400
rho=1e-21*c*c/1.602176634e-19*hc**3;n=rho/m;sigma=200000/c;r=sigma/u
A=(2*math.pi)**1.5*n/(m*sigma)**3
GammaNR=g*g*u/(16*math.pi*m);timeGyr=hbev/(2*GammaNR*A)/year/1e9
checks=[]
def check(name,b):checks.append(dict(name=name,passed=bool(b)))
def run(N,emax):
 de=emax/N;e=(np.arange(N)+.5)*de;ec=(np.arange(2*N)+1)*de
 wp=np.sqrt(2*e)*de;wc=4*np.sqrt(np.maximum(ec-1,0))*de
 i,j=np.indices((N,N));ss=i+j
 mask=(e[:,None]+e[None,:]-2)**2 <=4*e[:,None]*e[None,:]
 mask &= ec[ss]>1
 ii=i[mask];jj=j[mask];kk=ss[mask]
 valid=wc>0
 def rhs(t,z):
  a=z[:N];b=z[N:];flux=de*de*(a[ii]*a[jj]-b[kk]*(a[ii]+a[jj]+1/A))
  da=-(np.bincount(ii,weights=flux,minlength=N)+np.bincount(jj,weights=flux,minlength=N))/wp
  db=np.zeros(2*N);tmp=np.bincount(kk,weights=flux,minlength=2*N);db[valid]=tmp[valid]/wc[valid]
  return np.r_[da,db]
 y0=np.r_[np.exp(-e/r**2),np.zeros(2*N)]
 ts=np.linspace(0,20,201)
 sol=solve_ivp(rhs,(0,20),y0,t_eval=ts,method='DOP853',rtol=2e-9,atol=1e-12,max_step=.1)
 check('integration completed',sol.success)
 a=sol.y[:N];b=sol.y[N:];Q=wp@a+2*wc@b;E=(wp*e)@a+(wc*ec)@b
 qerr=float(np.max(abs(Q/Q[0]-1)));eerr=float(np.max(abs(E/E[0]-1)))
 check('charge conservation',qerr<1e-9);check('energy conservation',eerr<1e-9)
 check('nonnegative occupations',float(sol.y.min())>-1e-10)
 # Away from quantum-scale occupations the finite network has classical RJ detailed balance.
 aa=1/(e+.7);bb=1/(ec+1.4);balance=aa[ii]*aa[jj]-bb[kk]*(aa[ii]+aa[jj])
 check('classical detailed balance',float(np.max(abs(balance)))<1e-14)
 # The RHS conserves moments for a non-equilibrium positive sample, not just the trajectory.
 ztest=np.r_[aa,bb];dz=rhs(0,ztest)
 check('collision charge moment',abs(wp@dz[:N]+2*wc@dz[N:])<1e-12)
 check('collision energy moment',abs((wp*e)@dz[:N]+(wc*ec)@dz[N:])<1e-12)
 rows=[]
 for idx in [0,10,50,100,200]:
  daughter=wp@a[:,idx];source=wc@b[:,idx]
  rows.append(dict(tau=float(ts[idx]),time_Gyr=float(ts[idx]*timeGyr),source_charge_fraction=float(2*source/Q[0]),daughter_mean_energy=float((wp*e)@a[:,idx]/daughter),source_mean_energy=float((wc*ec)@b[:,idx]/source) if source>0 else None))
 # High-energy occupation fraction flags sensitivity to the finite domain.
 edge=float((wp[e>.8*emax]@a[e>.8*emax,-1]+2*wc[ec>1.6*emax]@b[ec>1.6*emax,-1])/Q[0])
 return dict(N=N,emax=emax,de=de,allowed_ordered_pairs=len(ii),initial_charge=float(Q[0]),initial_energy_per_charge=float(E[0]/Q[0]),charge_error=qerr,energy_error=eerr,min_occupation=float(sol.y.min()),outer_charge_fraction=edge,snapshots=rows,daughter_energy_grid=e.tolist(),source_energy_grid=ec.tolist(),daughter_final=a[:,-1].tolist(),source_final=b[:,-1].tolist())
runs=[run(64,8.),run(128,8.),run(256,8.),run(256,16.)]
comparisons=dict(refinement_source_fraction_difference=abs(runs[1]['snapshots'][-1]['source_charge_fraction']-runs[2]['snapshots'][-1]['source_charge_fraction']),cutoff_source_fraction_difference=abs(runs[1]['snapshots'][-1]['source_charge_fraction']-runs[3]['snapshots'][-1]['source_charge_fraction']))
# Report grid differences without declaring continuum convergence from a coarse angular-boundary quadrature.
out=dict(all_pass=all(c['passed'] for c in checks),checks=checks,runs=runs,comparisons=comparisons,parameters=dict(m_eV=m,g_eV=g,u=u,rho_daughters_kg_m3=1e-21,sigma_1d_kms=200,occupation_scale=A,time_unit_Gyr=timeGyr),non_claims=['Homogeneous isotropic incoherent kinetic closure, not spatial heat flow','NR resonance gap=m u^2, not exact relativistic dispersion','Finite energy grid; no condensate or continuum convergence proof','No galaxy law, vacuum coupling or cosmological abundance prediction'])
(p/'coupled_kinetics_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(all_pass=out['all_pass'],checks=len(checks),parameters=out['parameters'],comparisons=comparisons,runs=[{k:v for k,v in z.items() if not k.endswith('grid') and k not in ['daughter_final','source_final']} for z in runs]),indent=2));assert out['all_pass']
