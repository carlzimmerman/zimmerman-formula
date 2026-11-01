"""Actual Landau component radial two-derivative graphs, not angular F."""
import os,sys,math
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/finite_matching_2026_11_01/current_matching'))
from current import assemble,cubic,kernels,R,d,QS,L

def derivative(X,h,lam,g,f):
    o=assemble(X,h,lam,g,f);z=o['z'];Y=cubic(h,lam);dz=QS*z;F=.5*np.einsum('ijk,j,k->i',Y,z,z);F[0]+=f;M=np.einsum('ijk,k->ij',Y,z);dF=M@dz;dM=np.einsum('ijk,k->ij',Y,dz);dB=np.einsum('k,kij->ij',dF.conj(),Y);dA=dM.conj().T@M+M.conj().T@dM
    rz=np.einsum('aij,j->ai',R,z);drz=np.einsum('aij,j->ai',R,dz);D=math.sqrt(2)*g*np.concatenate([rz.real,rz.imag],axis=1);dD=math.sqrt(2)*g*np.concatenate([drz.real,drz.imag],axis=1)
    dH=np.block([[dA.real+dB.real,-dA.imag-dB.imag],[dA.imag-dB.imag,dA.real-dB.real]])+dD.T@D+D.T@dD
    dJ=math.sqrt(2)*g*np.einsum('i,aij->aj',dz.conj(),R);dMF=np.block([[dM,dJ.T],[dJ,np.zeros((24,24),complex)]]);dMV=2*g*g*(drz.conj()@rz.T+rz.conj()@drz.T).real
    return o,dH,dMF,dMV,drz

def K(a,b):
    if min(a,b)<=0:raise ValueError('massless VV logarithm needs vanishing vertex')
    m=(a+b)/2;t=(a-b)/(a+b)
    if abs(t)<.02:return sum(t**(2*k)/(2*k+1) for k in range(7))/m
    return math.log(a/b)/(a-b)

def fermion(X,h,lam,g,f,Q2):
    a=math.sqrt(2*f*h/(30*h*h+lam*lam));b=h*X/lam;out={};norm=0.;positive=[]
    for name,r,mult in [('SU3',2.,8),('SU2',-3.,3),('broken',-.5,12)]:
        m=(1+r)*h*X;q=r*lam*a
        if name=='broken':M=np.array([[m,q,5*g*a],[q,0,5*g*b],[5*g*a,5*g*b,0.]]);B=np.array([[m,0,0],[0,0,5*g*b],[0,5*g*b,0.]])
        else:M=np.array([[m,q],[q,0.]]);B=np.diag([m,0.])
        mu,O=eigh(M);B=O.T@B@O;norm+=mult*float(np.sum(B*B));val=0
        for i in range(len(mu)):
            if mu[i]**2>1e-20:positive.append(mu[i]**2)
            for j in range(len(mu)):
                w=float(B[i,j]**2)
                if w<1e-28*max(1,float(np.sum(B*B))):continue
                _,I,LW,_=kernels(mu[i]**2,mu[j]**2,Q2);val+=w*(-3*LW-mu[i]*mu[j]*I-1/6)/L
        out[name]=mult*val
    return out,norm,min(positive) if positive else None

def calculate(X,h,lam,g,f,Q2):
    X,h,lam,g,f,Q2=map(float,(X,h,lam,g,f,Q2));o,dH,dMF,dMV,drz=derivative(X,h,lam,g,f);es,V=eigh(o['H']);ev,W=eigh(o['MV']);scale=max(1e-300,float(max(es)),float(max(ev)));tol=1e-10*scale
    if min(es)<-tol or min(ev)<-tol:raise ValueError('physical negative tree mass')
    es=np.where(abs(es)<tol,0,es);ev=np.where(abs(ev)<tol,0,ev);Hs=V.T@dH@V;Vs=W.T@dMV@W;scalar=0.;vv=0.;nullweight=0.
    for i in range(98):
        for j in range(98):
            weight=float(Hs[i,j]**2)
            if es[i]+es[j]==0:
                nullweight=max(nullweight,weight)
                if weight>1e-18*max(1,float(np.sum(Hs*Hs))):raise ValueError('nonzero massless scalar radial vertex')
                continue
            _,I,_,_=kernels(es[i],es[j],Q2);scalar+=weight*I/(4*L)
    C=np.concatenate([drz.imag,-drz.real],axis=1);Ce=W.T@C@V;cnorm=float(np.sum(Ce*Ce));sv=0.;IRsv=0.
    for a in range(24):
        for i in range(98):
            weight=float(Ce[a,i]**2)
            if es[i]+ev[a]==0:
                IRsv=max(IRsv,g*g*weight)
                if g*g*weight>1e-18*max(1,g*g*cnorm):raise ValueError('massless radial SV vertex')
                continue
            *_,LU=kernels(es[i],ev[a],Q2);sv+=g*g*weight*(3*LU+.5)/L
    for a in range(24):
        for b in range(24):
            weight=float(Vs[a,b]**2)
            if min(ev[a],ev[b])==0:
                if weight>1e-18*max(1,float(np.sum(Vs*Vs))):raise ValueError('massless vector derivative vertex')
                continue
            _,I,_,_=kernels(ev[a],ev[b],Q2);vv+=weight*(3*I+.75*K(ev[a],ev[b]))/(4*L)
    fp,fn,minf=fermion(X,h,lam,g,f,Q2);ff=sum(fp.values());uv=(fn-6*g*g*cnorm)/L;expected=(87*h*h*X*X-300*g*g*o['b']**2)/L
    return dict(total=float(scalar+ff+sv+vv),scalar=float(scalar),fermion=float(ff),scalar_vector=float(sv),vector_vector=float(vv),fermion_parts=fp,A_tree=float(X*X+30*o['b']**2),UV_scale_derivative=float(uv),UV_expected=float(expected),UV_residual=float(uv-expected),scalar_null_count=int(sum(es==0)),vector_null_count=int(sum(ev==0)),max_null_scalar_vertex=nullweight,max_massless_SV_vertex=IRsv,min_positive_scalar_m2=float(min(es[es>0])),min_positive_fermion_m2=float(minf) if minf else None,min_positive_vector_m2=float(min(ev[ev>0])) if np.any(ev>0) else None,includes_heavy_pullback=False)
