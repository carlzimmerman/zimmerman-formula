"""Adversarial audit: actual mass transport versus the rapid internal mode.

This audits ONE explicitly defined endpoint interpolation, not all inside-out
paths. A positive barrier rejects this path, not galaxy formation.
"""
import argparse,json,sys
from pathlib import Path
import numpy as np,torch
from scipy.integrate import simpson
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'physical_completion_2026_10_25'))
from free_formation import FreeVacuum
from joint import T,RESERVOIR
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output)
m=FreeVacuum();initial=json.loads(Path('physical_completion_2026_10_25/run_free_formation/all_F.json').read_text());final=json.loads(Path('physical_completion_2026_10_25/run_free_finish/formed.json').read_text());m0=np.array(initial['mass']);m1=np.array(final['mass']);mt1=m1*np.array(final['q']);assert len(m0)==m.n==len(m1)
rad=m.r.numpy();edges=[0.]
for r in rad:edges.append(2*r-edges[-1])
edges=np.array(edges);vol=m.vol.numpy();r0=m0/vol;r1=m1/vol;delta=r1-r0;cum=np.r_[0,np.cumsum(m1-m0)]
nodes,weights=np.polynomial.legendre.leggauss(24);rr=(edges[:-1,None]+edges[1:,None])/2+(edges[1:,None]-edges[:-1,None])/2*nodes;ww=(edges[1:,None]-edges[:-1,None])/2*weights
flux=cum[:-1,None]+delta[:,None]*(rr**3-edges[:-1,None]**3)/3
qgrid=np.linspace(0,1,1001);N=np.sin(np.pi*qgrid/2)**2;I_N=[];energy=[];caps=[]
for i,n in enumerate(N):
 rho=(1-n)*r0+n*r1;I_N.append(float(np.sum(ww*flux**2/(rr**2*rho[:,None]))))
 if i%2==0:
  mass=(1-n)*m0+n*m1;qt=np.divide(n*mt1,mass,out=np.zeros_like(mass),where=mass>0);x=2/np.pi*np.arcsin(np.sqrt(np.clip(qt,0,1)));E=float(m.energy(T(np.log(mass)),T(x)));energy.append([qgrid[i],n,E]);caps.append(float(min(.9997-m.A.numpy()@(n*mt1))))
I_N=np.array(I_N);E=np.array(energy);assert max(abs(np.sum(m0)-RESERVOIR),abs(np.sum(m1)-RESERVOIR))<1e-10;assert min(caps)>0
e0=E[0,2];emin=min(E[:,2]);emax=max(E[:,2]);available=e0-emin;Iq=I_N*(np.pi**2*N*(1-N));assert available>0
kpc=3.085677581491367e19;Myr=365.25*86400*1e6;vunit=np.sqrt(9.3603e-11*m.rm*kpc);tdyn=m.rm*kpc/vunit/Myr
lower=float(simpson(np.sqrt(Iq/(2*available)),x=qgrid)*tdyn)
inert=json.loads(Path('selective_stress_2026_10_25/run_spinor_inertia/results.json').read_text());Ispin=inert['collective_inertia_in_old_dynamical_units'];j=len(qgrid)//2
out={'path':'m(N)=(1-N)m_initial+N*m_final; mT(N)=N*mT_final; real carrier locked to local material angle. Both endpoints are actual free-domain equilibria from PC. This is a restricted diagnostic curve, not the solved dynamics.','mass_constraint_max_error':float(max(abs(sum(m0)-RESERVOIR),abs(sum(m1)-RESERVOIR))),'cap_slack_min':float(min(caps)),'initial_energy':float(e0),'final_energy':float(E[-1,2]),'maximum_potential_above_initial':float(emax-e0),'minimum_potential':float(emin),'maximum_available_kinetic_energy_on_path':float(available),'energy_endpoint_errors':[float(e0-initial['energy']),float(E[-1,2]-final['energy'])],'middle_total_transport_inertia_for_N':float(I_N[j]),'middle_total_transport_inertia_for_q':float(Iq[j]),'middle_transport_over_internal_inertia':float(Iq[j]/Ispin),'minimum_transit_time_on_this_density_path_Myr':lower,'path_accessible_from_rest_without_extra_energy':bool(emax<=e0+1e-9),'energy_history':E.tolist(),'q':qgrid.tolist(),'transport_I_N':I_N.tolist(),'transport_I_q':Iq.tolist(),'derivation':'Continuity fixes radial total flux=-Ndot delta_M(<r). Cauchy-Schwarz gives sum rho_i v_i² >= total_flux²/(r^4 rho_total), hence T>=Ndot² integral delta_M²/(r²rho)dr/2. Integrate the resulting maximum speed using the largest possible kinetic energy on this curve.','non_claims':['No exclusion of different paths, local fronts, bursts or nonadiabatic density evolution','Energy bound is for the explicitly prescribed density interpolation','An inaccessible curve has no actual finite transit; quoted minimum time is a conditional lower bound, not a prediction','Endpoint halo has the previous K30, not the new virial-reference entropy']}
assert max(abs(np.array(out['energy_endpoint_errors'])))<1e-9
dest.write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k not in ['energy_history','q','transport_I_N','transport_I_q']},flush=True)
