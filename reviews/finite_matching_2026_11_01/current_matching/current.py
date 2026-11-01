"""Finite full-component one-loop angular current: scalars, Weyls, Landau SV.

Fixed Q², original-X chart, DRbar-prime component minimal subtraction.
No heavy-displacement pullback or small-F Kahler shortcut is included here.
"""
import os,sys,math
sys.dont_write_bytecode=True
for _v in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[_v]='1'
from pathlib import Path
from functools import lru_cache
import numpy as np
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/three_priorities_2026_11_01/spectrum_pressure'))
from spectrum import R,d,tensor
L=16*math.pi**2
QS=np.r_[1.,np.zeros(24),np.ones(24)]
QF=np.r_[QS-.5,np.full(24,.5)]
JS=np.block([[np.zeros((49,49)),-np.diag(QS)],[np.diag(QS),np.zeros((49,49))]])

@lru_cache(maxsize=8)
def cubic(h,lam):return tensor(h,lam)

def assemble(X,h,lam,g,f,theta=0.):
    a=math.sqrt(2*f*h/(30*h*h+lam*lam));b=h*X/lam;z=np.r_[complex(X),1j*a*d,b*d]*np.exp(1j*QS*theta);Y=cubic(h,lam)
    FF=.5*np.einsum('ijk,j,k->i',Y,z,z);FF[0]+=f;M=np.einsum('ijk,k->ij',Y,z);B=np.einsum('k,kij->ij',FF.conj(),Y);A=M.conj().T@M
    rz=np.einsum('aij,j->ai',R,z);D=math.sqrt(2)*g*np.concatenate([rz.real,rz.imag],axis=1)
    H=np.block([[A.real+B.real,-A.imag-B.imag],[A.imag-B.imag,A.real-B.real]])+D.T@D
    mix=math.sqrt(2)*g*np.einsum('i,aij->aj',z.conj(),R);MF=np.block([[M,mix.T],[mix,np.zeros((24,24),complex)]]);MV=2*g*g*(rz.conj()@rz.T).real
    return dict(H=H,MF=MF,MV=MV,z=z,a=a,b=b)

def kernels(a,b,Q2):
    """Return G(a,b), int t(1-t)/D, int t(1-t)ln(D/Q²), int ln(D/Q²)."""
    a,b=float(a),float(b)
    if a<0 or b<0 or Q2<=0:raise ValueError('positive masses and Q² required')
    if a+b==0:raise ValueError('massless pair requires vanishing vertex/IR treatment')
    if min(a,b)==0:
        x=max(a,b);ell=math.log(x/Q2);return x/2,1/(2*x),ell/6-5/36,ell-1
    m=(a+b)/2;delta=(a-b)/(a+b)
    if abs(delta)<.02:
        t=delta*delta
        G=m*sum(2*t**k/((2*k-1)*(2*k+1)) for k in range(1,7))
        I=sum(t**k/(2*(2*k+1)*(2*k+3)) for k in range(7))/m
        LW=math.log(m/Q2)/6-sum(t**k/(4*k*(2*k+1)*(2*k+3)) for k in range(1,7))
        LU=math.log(m/Q2)-sum(t**k/(2*k*(2*k+1)) for k in range(1,7))
        return G,I,LW,LU
    gap=a-b;la=math.log(a/Q2);lb=math.log(b/Q2)
    G=(a+b)/2-a*b/gap*math.log(a/b);I=G/(gap*gap)
    def primitive(x):
        lx=math.log(x/Q2)
        return -x**3*(lx/3-1/9)+(a+b)*x*x*(lx/2-1/4)-a*b*x*(lx-1)
    LW=(primitive(a)-primitive(b))/gap**3;LU=(a*la-a-b*lb+b)/gap
    return G,I,LW,LU

def fermion_blocks(X,h,lam,g,f,Q2):
    a=math.sqrt(2*f*h/(30*h*h+lam*lam));b=h*X/lam;parts={};uv=0.;masses=[]
    for name,r,mult in [('SU3',2.,8),('SU2',-3.,3),('broken',-.5,12)]:
        m=(1+r)*h*X;q=r*lam*a
        if name=='broken':M=np.array([[m,q,5*g*a],[q,0,5*g*b],[5*g*a,5*g*b,0.] ]);charge=np.diag([-.5,.5,.5])
        else:M=np.array([[m,q],[q,0.]]);charge=np.diag([-.5,.5])
        mu,O=eigh(M);AA=-(charge@M+M@charge);A=O.T@AA@O;total=0.;uv+=mult*float(np.sum(A*A))
        for i in range(len(mu)):
            for j in range(len(mu)):
                weight=float(A[i,j]**2)
                if weight<1e-28*max(1,float(np.sum(AA*AA))):continue
                _,I,LW,_=kernels(mu[i]**2,mu[j]**2,Q2)
                total+=weight*(-3*LW+mu[i]*mu[j]*I-1/6)/L
        parts[name]=mult*total;masses.extend([float(x*x) for x in mu for _ in range(mult)])
    return parts,uv,masses

def calculate(X,h,lam,g,f,Q2):
    X,h,lam,g,f,Q2=map(float,(X,h,lam,g,f,Q2));o=assemble(X,h,lam,g,f);H=o['H'];MV=o['MV'];es,V=eigh(H);ev,W=eigh(MV);scale=max(1e-300,float(max(es)),float(max(ev)));tol=1e-10*scale
    if min(es)<-tol or min(ev)<-tol:raise ValueError('negative tree mass beyond null tolerance')
    es=np.where(abs(es)<tol,0,es);ev=np.where(abs(ev)<tol,0,ev);J=V.T@JS@V;scalar=0.
    for i in range(98):
        for j in range(i+1,98):
            if es[i]+es[j]==0:continue
            G,*_=kernels(es[i],es[j],Q2);scalar+=float(J[i,j]**2)*G/(2*L)
    parts,uvf,fm=fermion_blocks(X,h,lam,g,f,Q2);fermion=sum(parts.values())
    w=np.einsum('aij,j->ai',R,QS*o['z']);C=np.concatenate([w.real,w.imag],axis=1);Ce=W.T@C@V;sv=0.;norm=float(np.sum(Ce*Ce));max_IR_vertex=0.
    for a in range(24):
        for i in range(98):
            weight=float(Ce[a,i]**2)
            if es[i]+ev[a]==0:
                max_IR_vertex=max(max_IR_vertex,g*g*weight)
                if g*g*weight>1e-18*max(1,g*g*norm):raise ValueError('unresolved massless SV current vertex')
                continue
            *_,LU=kernels(es[i],ev[a],Q2);sv+=g*g*weight*(3*LU+.5)/L
    expected_uv=(87*h*h*X*X-300*g*g*o['b']**2)/L;actual_uv=(uvf-6*g*g*norm)/L
    return dict(total=float(scalar+fermion+sv),scalar=float(scalar),fermion=float(fermion),scalar_vector=float(sv),fermion_sectors=parts,F_tree=float(X*X+30*o['b']**2),deltaF_over_Ftree=float((scalar+fermion+sv)/(X*X+30*o['b']**2)),UV_scale_derivative=float(actual_uv),UV_expected=float(expected_uv),UV_residual=float(actual_uv-expected_uv),fermion_vertex_norm=float(uvf),SV_current_norm=float(norm),SV_current_norm_expected=float(150*o['b']**2),scalar_null_count=int(np.sum(es==0)),vector_null_count=int(np.sum(ev==0)),max_massless_SV_vertex=max_IR_vertex,scheme='Landau DRbar-prime component minimal subtraction; finiteSV +1/2 retained',includes_heavy_geometric_shift=False)
