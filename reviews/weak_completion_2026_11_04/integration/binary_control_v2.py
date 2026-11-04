"""Algebraic binary collision controls, not a physical Coulomb rate claim."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,time,resource
import numpy as np
from scipy.sparse import hstack
from binary_events_v2 import BinaryEvents

def main(output):
 start=time.monotonic();energy=np.array([1.,2.,3.,2.,3.,4.]);measure=np.array([.5,.7,.9,.6,.8,1.]);index=np.array([[0,5,1,2,3,4],[1,4,0,1,4,5],[0,4,0,1,3,4],[1,4,1,1,4,4]]);weights=np.array([[1,1,.5,.5,.5,.5],[1,1,.5,.5,.5,.5],[1,1,1-1e-8,1e-8,1e-8,1-1e-8],[1,1,1,0,1,0]],float);coefficient=np.array([.1,.2,1e12,.3]);rows=[]
 for eta in (np.ones(6),-np.ones(6)):
  ev=BinaryEvents(index,weights,coefficient,measure,energy,eta,chunk=2);eq=1/(np.exp((energy-.3)/2)-eta);f=np.array([.2,.3,.17,.25,.12,.19]);C=ev.number_rhs(f);J=ev.number_jacobian(f).toarray();v=np.array([.02,-.01,.03,-.02,.01,.015]);h=1e-5;fd=(ev.number_rhs(f+h*v/measure)-ev.number_rhs(f-h*v/measure))/(2*h);jj=J@v;jerr=max(abs(fd-jj))/max(max(abs(jj)),1e-300);ep=ev.entropy_production(f);odds=np.log(f/(1+eta*f));ent=-float(odds@C);gross=sum(ev.number_gross(f));S=hstack([b.S for b in ev.blocks],format='csr');num=abs(sum(C));en=abs(energy@C);nA=abs(sum(C[:3]));nB=abs(sum(C[3:]));equ=ev.number_rhs(eq)
  evsingle=BinaryEvents(index,weights,coefficient,measure,energy,eta,chunk=100);chunkerror=max(abs(C-evsingle.number_rhs(f)))/max(max(abs(C)),1e-300)
  rows.append(dict(statistic=float(eta[0]),stoich_number=ev.number_residual,stoich_energy=ev.energy_residual,number_relative=num/max(gross,1e-300),species_number_relative=max(nA,nB)/max(gross,1e-300),energy_relative=en/max(gross*max(energy),1e-300),entropy_production=ep,entropy_identity_relative=abs(ep-ent)/max(ep,1e-300),equilibrium_rhs_relative=max(abs(equ))/max(gross,1e-300),Jacobian_direction_relative=jerr,chunk_relative=chunkerror))
 ghost_rows=[]
 for exponent in (288,310):
  ev=BinaryEvents(index,weights,coefficient,measure,energy,np.ones(6),chunk=2);f=np.array([.2,.3,10.**(-exponent),.25,.12,.19]);jac=ev.number_jacobian(f);rhs=ev.number_rhs(f);ghost_rows.append(dict(exponent=exponent,finite_rhs=bool(np.all(np.isfinite(rhs))),finite_jacobian=bool(np.all(np.isfinite(jac.data)))))
 checks=dict(subnormal_cells=all(r['finite_rhs'] and r['finite_jacobian'] for r in ghost_rows),stoich=all(r['stoich_number']<1e-15 and r['stoich_energy']<1e-14 for r in rows),number_energy=all(r['number_relative']<1e-13 and r['energy_relative']<1e-13 and r['species_number_relative']<1e-13 for r in rows),entropy=all(r['entropy_production']>=0 and r['entropy_identity_relative']<1e-12 for r in rows),equilibrium=all(r['equilibrium_rhs_relative']<1e-8 for r in rows),Jacobian=all(r['Jacobian_direction_relative']<1e-6 for r in rows),chunk=all(r['chunk_relative']<1e-14 for r in rows))
 out=dict(claim_id='CC11_BINARY_COLLISION_ALGEBRA',checks={k:bool(v) for k,v in checks.items()},rows=rows,ghost_rows=ghost_rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Two labelled species with specified energy-conserving elastic redistribution and a near-forward high-coefficient fixture; no physical Coulomb coefficient or cosmological claim.')
 Path(output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
