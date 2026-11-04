"""Vertex completeness and spacelike-propagator controls for C C*->gauginos."""
import sys,os
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
from scipy.linalg import eigh
from network import build_model,adapt,DCOEF,E,G

def one(x):
 d=build_model(x,E,E,G,vertices=False);Q=np.einsum('a,aij->ij',DCOEF/math.sqrt(30),d['R']);Q2=Q@Q;CS=np.block([[Q2.real,-Q2.imag],[Q2.imag,Q2.real]])
 O=adapt(d['O'],d['mS2'],CS);qs=np.einsum('ia,ia->a',O,CS@O).real;mS=np.sqrt(np.maximum(d['mS2'],0));m=min(mS[(qs>.1)&(mS>1e-12)]);L=np.where((qs>.1)&(abs(mS-m)<1e-8))[0]
 unbroken=np.where(np.diag(Q2[1:25,1:25]).real<.01)[0];assert len(unbroken)==12
 J=np.block([[-Q.imag,-Q.real],[Q.real,-Q.imag]]);q,V=eigh(1j*O[:,L].T@J@O[:,L]);positive=V[:,q>.1];assert positive.shape[1]==6
 Em=d['E']@O[:,L];dy=math.sqrt(2)*G*np.einsum('ka,pki->pia',Em.conj(),d['R'][unbroken],optimize=True)
 # A charged scalar particle is a normalized complex combination of real
 # scalar one-particle states. Sum both external gaugino chiralities.
 yl=np.einsum('pia,ac->pic',dy,positive);yr=np.einsum('pia,ac->pic',dy.conj(),positive)
 norm=(np.sum(abs(yl)**2,axis=(0,1))+np.sum(abs(yr)**2,axis=(0,1)))/G**2
 QF=np.zeros((73,73),complex);QF[:49,:49]=Q2;QF[49:,49:]=Q2[1:25,1:25];U=adapt(d['U'],d['mF'],QF);qf=np.einsum('ia,ia->a',U.conj(),QF@U).real;mf=min(d['mF'][qf>.1])
 return dict(x=x,mC=m,min_charged_F=mf,all_massive_internal_F_above_mC=bool(mf>=m*(1-1e-12)),particle_vertex_norm_over_g2=norm.tolist(),gauge_coefficient_mu2=13*G**4/(128*math.pi*m*m),gaugino_pair_uniform_bound_mu2=50*G**4/(math.pi*m*m))

def main(out):
 start=time.monotonic();rows=[one(x) for x in (5,7.5,10,20,25.4000254000381,30)]
 s1=np.array([[0,1],[1,0]],complex);s2=np.array([[0,-1j],[1j,0]],complex);s3=np.diag([1,-1]);gammas=[np.block([[np.zeros((2,2)),s],[-s,np.zeros((2,2))]]) for s in (s1,s2,s3)]
 controls=[]
 for p in (0,.1,1,10):
  for M in (1,1.1,2,100):
   P=(M*np.eye(4)-p*gammas[2])/(-(p*p+M*M));got=np.linalg.norm(P,2);exact=1/math.sqrt(p*p+M*M);controls.append(abs(got/exact-1))
 checks=dict(vertex_completeness=max(abs(n-5) for r in rows for n in r['particle_vertex_norm_over_g2'])<1e-10,all_internal_F_heavier=all(r['all_massive_internal_F_above_mC'] for r in rows),spacelike_propagator_norm=max(controls)<1e-12)
 result=dict(claim_id='CT09_GAUGINO_PAIR_TCHANNEL_BOUND',checks=checks,cases=rows,uniform_ratio_to_scalar_gauge=6400/13,scope='All12masslessrawunbrokengauginos, t/u charged-fermion exchange only, stablelightchargedscalarbranch. UniformCMvelocity Mollerσv bound50g^4/(pi mC²), using internalMF>=mC and vertexCasimir. No s-channelresonance, scalar-gauginofinalstate, heavyneutralfermion, Goldstino, bosonicannihilationorcosmologicalyieldbound.',runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
