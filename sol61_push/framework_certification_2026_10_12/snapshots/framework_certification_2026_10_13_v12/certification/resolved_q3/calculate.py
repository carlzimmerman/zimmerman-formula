import os
for x in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[x]='1'
from pathlib import Path
from itertools import product,combinations_with_replacement
from collections import Counter,defaultdict
import json,sys,time
import numpy as np
from scipy.linalg import eigh,solve
DEST=Path(sys.argv[2]);cut=int(sys.argv[1]);start=time.monotonic()
m=1.;delta=.0002;M=2*m+delta;Delta=delta*(M+2*m);lmin=lrep=.05;lt=lmin+lrep
g=np.sqrt(lmin*Delta);c3=g/(2*m*np.sqrt(2*M));k=lt/(4*m*m);k0=np.sqrt(m*delta);volume=(2*np.pi/k0)**3;gamma=c3/np.sqrt(volume)/delta;kappa=k/volume/delta
mom=list(product(range(-cut,cut+1),repeat=3));index={v:i for i,v in enumerate(mom)};P=(1,0,0);nm=len(mom)
B=[]
for ib,pb in enumerate(mom):
 pa=tuple(P[j]-pb[j] for j in range(3))
 if pa in index:B.append((ib,index[pa]))
A=[]
for i in range(nm):
 for j in range(i,nm):
  v=tuple(P[d]-mom[i][d]-mom[j][d] for d in range(3));q=index.get(v)
  if q is not None and q>=j:A.append((i,j,q))
nb,na=len(B),len(A);dim=nb+na;Ai={a:i for i,a in enumerate(A)};Bi={b:i for i,b in enumerate(B)}
checks=[]
def check(name,value,tol):checks.append({'name':name,'value':float(value),'tolerance':float(tol),'passed':bool(np.isfinite(value) and abs(value)<=tol)})
def require(name,c):checks.append({'name':name,'passed':bool(c)})
brute=[tr for tr in combinations_with_replacement(range(nm),3) if all(sum(mom[t][d] for t in tr)==P[d] for d in range(3))]
require('complete independent unordered threepsi enumeration',set(brute)==set(A));del brute
require('complete oneb onepsi enumeration',all((ib,ia) in Bi for ib in range(nm) for ia in range(nm) if all(mom[ib][d]+mom[ia][d]==P[d] for d in range(3))))
require('all basis Q3 exact momentum',all(all(sum(mom[t][d] for t in tr)==P[d] for d in range(3)) for tr in A) and all(all(mom[i][d]+mom[j][d]==P[d] for d in range(3)) for i,j in B))
V=np.zeros((nb,na));U=np.zeros((na,na));F=np.zeros((nm,na));paircreate=defaultdict(list)
for i in range(nm):
 for j in range(i,nm):paircreate[tuple(mom[i][d]+mom[j][d] for d in range(3))].append((i,j))
for col,tr in enumerate(A):
 counts=Counter(tr);occ=sorted(counts)
 for qi in occ:
  for qj in occ:
   if qj<qi or (qj==qi and counts[qi]<2):continue
   remainder=counts.copy();ann=np.sqrt(remainder[qi]);remainder[qi]-=1;ann*=np.sqrt(remainder[qj]);remainder[qj]-=1
   mult_ann=1 if qi==qj else 2;ann*=mult_ann
   survivor=next(i for i,n in remainder.items() if n)
   F[survivor,col]+=ann
   total=tuple(mom[qi][d]+mom[qj][d] for d in range(3));ib=index.get(total)
   if ib is not None:V[Bi[(ib,survivor)],col]+=gamma*ann
   # ALL pair totals, including sums not on the retained b/source grid.
   for ci,cj in paircreate[total]:
    final=remainder.copy();cre=np.sqrt(final[ci]+1);final[ci]+=1;cre*=np.sqrt(final[cj]+1);final[cj]+=1
    mult_cre=1 if ci==cj else 2;ft=tuple(sorted(i for i,n in final.items() for _ in range(n)))
    U[Ai[ft],col]+=kappa*ann*cre*mult_cre
Tpsi=np.zeros(dim);Tb=np.zeros(dim);Nsrc=np.zeros(dim)
for j,(ib,ia) in enumerate(B):
 Nsrc[j]=1;Tpsi[j]=sum(a*a for a in mom[ia])*k0*k0/(2*m*delta);Tb[j]=sum(a*a for a in mom[ib])*k0*k0/(2*M*delta)
for j,tr in enumerate(A):Tpsi[nb+j]=sum(sum(q*q for q in mom[i]) for i in tr)*k0*k0/(2*m*delta)
T=Tpsi+Tb;H=np.diag(T+Nsrc);H[:nb,nb:]=V;H[nb:,:nb]=V.T;H[nb:,nb:]+=U
check('Hermitian Hamiltonian',np.max(np.abs(H-H.T)),1e-12)
check('all quartic sums independent Gram reconstruction',np.max(np.abs(U-kappa*F.T@F)),1e-12)
inside_rows=[ia for ib,ia in B];outside_rows=[i for i in range(nm) if i not in inside_rows];Fin=F[inside_rows];Fout=F[outside_rows]
check('trilinear independent pair annihilator reconstruction',np.max(np.abs(V-gamma*Fin)),1e-12)
require('quartic offdiagonal retained',np.linalg.norm(U-np.diag(np.diag(U)))>0)
require('outside source-cutoff pair sums retained',len(outside_rows)>0 and np.linalg.norm(Fout)>0)
diag_expected=[]
for tr in A:
 c=Counter(tr);diag_expected.append(kappa*(sum(n*(n-1) for n in c.values())+4*sum(c[i]*c[j] for i,j in combinations_with_replacement(sorted(c),2) if i<j)))
check('quartic diagonal direct bosonic count',np.max(np.abs(np.diag(U)-diag_expected)),1e-12)
R=np.c_[np.eye(nb),gamma*Fin];positive=R.T@R;positive[nb:,nb:]+=(kappa-gamma*gamma)*(Fin.T@Fin)+kappa*(Fout.T@Fout)
check('positive square outside pair sum reconstruction',np.max(np.abs((H-np.diag(T))-positive)),1e-12)
require('positive leftover coefficient',kappa>=gamma*gamma)
initial=Bi[(index[(0,0,0)],index[P])];y0=np.zeros(dim);y0[initial]=1;E0=H[initial,initial];tau=np.linspace(0,4000,401)
eval,evec=eigh(H,check_finite=False);Y=evec@(np.exp(-1j*eval[:,None]*tau[None,:])*evec[initial,:,None]);probs=np.abs(Y)**2
norm=probs.sum(axis=0);energies=np.sum(eval[:,None]*(np.abs(evec[initial,:,None])**2),axis=0) # invariant spectral expression
HY=H@Y;E=np.einsum('ij,ij->j',Y.conj(),HY).real
Ep=Tpsi@probs;Eb=Tb@probs;gap=Nsrc@probs;WU=np.einsum('ij,ij->j',Y[nb:].conj(),U@Y[nb:]).real;WW=2*np.einsum('ij,ij->j',Y[:nb].conj(),V@Y[nb:]).real
check('state norm',np.max(abs(norm-1)),1e-10);check('total interaction-inclusive D energy',np.max(abs(E-E0))/max(abs(E0),1),1e-9)
check('energy decomposition Tpsi Tb gap W U',np.max(abs(E-(Ep+Eb+gap+WW+WU))),1e-9)
require('omitting interaction coherence fails ledger',np.max(abs(WW))>1e-10)
check('sampled kinetic budget excess',max(0.,float(np.max(Ep+Eb-E0))),1e-9);check('positive Hamiltonian minimum eigenvalue',min(0.,float(eval.min())),1e-9)
distinct=[i for i,(ib,ia) in enumerate(B) if i!=initial and mom[ib]!=(0,0,0) and mom[ia]!=P]
recoil=probs[distinct].sum(axis=0);require('returned distinct b psi channel witness',np.max(recoil)>1e-10)
# Inert-spectator control is an explicit reduced star, not another physical kernel.
active=np.where(abs(V[initial])>0)[0];star=np.diag(np.r_[E0,T[nb+active]]);star[0,1:]=V[initial,active];star[1:,0]=V[initial,active]
sv,se=eigh(star,check_finite=False);SY=se@(np.exp(-1j*sv[:,None]*tau[None,:])*se[0,:,None]);star_survival=np.abs(SY[0])**2
check('inert spectator star has no distinct B state',0.,1e-12)
Hzero=H.copy();Hzero[:nb,nb:]=0;Hzero[nb:,:nb]=0
check('conversion off initial state eigenvector',np.linalg.norm(Hzero@y0-E0*y0),1e-12)
# Full Feshbach kernel from actual matrix blocks; no damping/local collision inserted.
Z=E0+.37j;AA=H[nb:,nb:];BB=H[:nb,:nb];resA=solve(Z*np.eye(na)-AA,V.T,assume_a='gen',check_finite=False);Schur=Z*np.eye(nb)-BB-V@resA
projfull=solve(Z*np.eye(dim)-H,np.r_[np.eye(nb),np.zeros((na,nb))],assume_a='gen',check_finite=False)[:nb]
check('Feshbach projected resolvent identity',np.max(abs(projfull-solve(Schur,np.eye(nb),check_finite=False))),1e-10)
Kzero=V@V.T;require('finite kernel mixes distinct B channels',np.max(abs(Kzero[initial,distinct]))>0)
# Save component-level outputs and recoil channels, not every time-state amplitude.
peak=int(np.argmax(recoil));channels=[{'source_n':mom[B[i][0]],'daughter_n':mom[B[i][1]],'max_probability':float(probs[i].max()),'source_kinetic_delta_units':float(Tb[i]),'daughter_kinetic_delta_units':float(Tpsi[i])} for i in distinct if probs[i].max()>1e-12];channels.sort(key=lambda r:r['max_probability'],reverse=True)
np.savez_compressed(DEST/'trajectory.npz',tau=tau,norm=norm,total_energy=E,daughter_kinetic=Ep,source_kinetic=Eb,source_gap=gap,interaction=WW,quartic=WU,source_probability=probs[:nb].sum(axis=0),distinct_B_probability=recoil,initial_B_probability=probs[initial],star_survival=star_survival)
np.savez_compressed(DEST/'hamiltonian.npz',H=H,V=V,U=U,F=F,momenta=np.array(mom),B_basis=np.array(B),A_basis=np.array(A),initial=initial,Tpsi=Tpsi,Tb=Tb,Nsrc=Nsrc)
out={'cutoff':cut,'dimension':dim,'B_states':nb,'threepsi_states':na,'momentum_modes_each_species':nm,'exact_total_integer_momentum':P,'inputs':{'m':m,'delta':delta,'M':M,'Delta':Delta,'lambda_min':lmin,'lambda_rep':lrep,'g':g,'c3':c3,'k':k,'k0':k0,'volume':volume,'gamma_over_delta':gamma,'kappa_over_delta':kappa,'maximum_daughter_momentum_over_m':np.sqrt(3)*cut*k0/m},'initial_excess_energy_over_delta':E0,'checks':checks,'all_passed':all(c['passed'] for c in checks),'peak_distinct_B_probability':float(recoil[peak]),'peak_time_tau':float(tau[peak]),'max_threepsi_probability':float(probs[nb:].sum(axis=0).max()),'maximum_source_kinetic_over_delta':float(Eb.max()),'max_omitted_interaction_energy_over_delta':float(np.max(abs(WW))),'returned_channels':channels[:15],'outside_source_pair_rows':len(outside_rows),'finite_time_kernel':'K(t)=V exp(-i AA t)Vdagger; finite Hermitian memory, not local damping','scope':'complete finite3D cutoff Q3 P-sector; prepared Fock state; no width/spectral matching or continuum irreversible claim','runtime_child_seconds':time.monotonic()-start}
(DEST/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert out['all_passed']
