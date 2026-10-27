import argparse,json
from pathlib import Path
import numpy as np
from dynamics import model,load
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();m=model();a=load('infall_pump_2026_10_25/run_smooth_prepare/state.npz')[0];mass=np.sum(abs(a)**2,axis=0);rho=abs(a)**2/m.vol;rr=(m.r[1:]+m.r[:-1])/2;dr=np.diff(m.r);AT=rr**2*np.sqrt(rho[0,:-1]*rho[0,1:]);A=AT+rr**2*np.sqrt(rho[1,:-1]*rho[1,1:]);B=A*dr;L=2*m.g2*np.diff(rho[0])*AT;ref=np.load('infall_pump_2026_10_25/run_static_polish/state.npz')['a'];target=np.sum(abs(ref)**2,axis=0);target*=5.364/np.sum(target);delta=np.cumsum(target-mass)[:-1];rows=[]
r=m.r*m.rm;i=np.searchsorted(r,50)-1;f=(50-r[i])/(r[i+1]-r[i]);w=np.zeros(m.n);w[:i]=1;w[i]=.5+.5*f;w[i+1]=.5*f;dw=np.diff(w)
for cutoff in [100,150,200]:
 for floor in [1e-12,1e-14,1e-16]:
  sel=(B>max(B)*floor)&(rr*m.rm<cutoff);v=np.zeros_like(A);v[sel]=-delta[sel]/A[sel];bright=np.zeros_like(A);bright[sel]=L[sel]/B[sel];q=float(L@v);kin=float(B@(v*v));bnorm=float(B@(bright*bright));vb=bright*q/bnorm;vdk=v-vb
  total=float(dw@(A*v));seen=float(dw@(A*vb));dark=float(dw@(A*vdk));assert abs(total-seen-dark)<1e-12
  rows.append({'outer_cutoff_kpc':cutoff,'relative_metric_floor':floor,'bright_kinetic_fraction':q*q/(kin*bnorm),'required_inward_50kpc_mass_rate_per_parameter':total,'bright_inward_50kpc_mass_rate_per_parameter':seen,'dark_inward_50kpc_mass_rate_per_parameter':dark,'bright_fraction_of_required_50kpc_rate':seen/total,'active_edge_count':int(np.sum(sel))})
out={'cases':rows,'non_claim':'Frozen-profile compact-monopole projection; dark directions need not be invariant under subsequent Hamiltonian mixing. Outer cutoff is a diagnostic integration window, not a material boundary.'};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(rows)
