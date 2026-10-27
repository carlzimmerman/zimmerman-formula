"""Compact monopole sees one current functional, not every transport mode."""
import argparse,json
from pathlib import Path
import numpy as np
from dynamics import model,load
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();m=model();z=load('infall_pump_2026_10_25/run_smooth_prepare/state.npz');a=z[0];rho=abs(a)**2/m.vol;re=(m.r[1:]+m.r[:-1])/2;dr=np.diff(m.r);AT=re**2*np.sqrt(rho[0,1:]*rho[0,:-1]);AF=re**2*np.sqrt(rho[1,1:]*rho[1,:-1]);A=AT+AF;B=A*dr;L=2*m.g2*np.diff(rho[0])*AT
ref=load('infall_pump_2026_10_25/run_static_polish/state.npz');target=np.sum(abs(ref[0])**2,axis=0);target*=5.364/np.sum(target);initial=np.sum(abs(a)**2,axis=0);delta=np.cumsum(target-initial)[:-1]
active=(B>max(B)*1e-14)&(re*m.rm<200);vel=np.zeros_like(A);vel[active]=-delta[active]/A[active];bright=np.zeros_like(A);bright[active]=L[active]/B[active]
kin=float(np.sum(B*vel**2));bnorm=float(np.sum(B*bright**2));qdot=float(L@vel);fraction=qdot*qdot/(kin*bnorm);vbright=bright*qdot/bnorm;vdark=vel-vbright
assert abs(L@vdark)<1e-10*max(1.,abs(qdot));assert abs(np.sum(B*vbright*vdark))<1e-10*max(1.,kin)
# Discrete phase construction independently tests the exact linear transport source.
phase=np.r_[0.,np.cumsum(m.sigma/m.k*vel*dr)];eps=1e-5;aa=a*np.exp(1j*eps*phase);_,S,bulk,conv,U,G=m.transfer(aa,z[1],z[3]);measured=float(np.sum(S))/eps
source=[]
for name,path in [('first_pulse','infall_pump_2026_10_25/run_smooth_infall/state.npz'),('continued','sustained_transport_2026_10_26/run_continue/state.npz')]:
 st=load(path);_,S,b,c,U,G=m.transfer(st[0],st[1],st[3]);total=float(np.sum(abs(S)));source.append({'state':name,'absolute_source_weight_inside':{str(R):float(np.sum(abs(S[m.r*m.rm<R]))/total) for R in [3,10,25,50]},'signed_integral':float(np.sum(S))})
res={'metric':'Exact quadratic common-phase transport energy at zero scalar field: .5 sum B_e v_e²; B=A_total dr. No target force introduced.','linear_source_Lv':qdot,'direct_phase_source_derivative':measured,'phase_derivative_relative_error':abs(measured-qdot)/abs(qdot),'required_transport_kinetic_norm':kin,'compact_monopole_bright_fraction':fraction,'compact_monopole_dark_fraction':1-fraction,'dark_source_residual':float(L@vdark),'source_spatial_support':source,'excluded_edge_count':int(np.sum(~active)),'active_edge_count':int(np.sum(active)),'non_claim':'Frozen-profile common-transport tangent and leading compact monopole only; finite-size higher multipoles, conversion and nonlinear mode mixing can couple initially dark directions. This does not prove formation impossible.'}
assert res['phase_derivative_relative_error']<1e-5
np.savez_compressed(Path(args.output).with_name('directions.npz'),radius_kpc=re*m.rm,required_velocity=vel,bright_velocity=vbright,dark_velocity=vdark,kinetic_weight=B,source_functional=L,active=active)
Path(args.output).write_text(json.dumps(res,indent=2)+'\n');print(res)
