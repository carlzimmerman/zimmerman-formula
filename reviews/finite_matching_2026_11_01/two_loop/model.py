"""Full SU5 component masses and SSS/SS/FFS vertices in Martin conventions.

Columns: delta r_old=O delta r_mass, psi_old=U psi_mass,
vector_old=Ov vector_mass; U.T MF U=diag(mF)>=0.
Real scalar order is q[49],p[49], z=z0+(q+i p)/sqrt(2).
"""
import sys,math
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/three_priorities_2026_11_01/spectrum_pressure'))
from spectrum import R as SU5_R,d as SU5_D,tensor
YH=tensor(1.,0.);YL=tensor(0.,1.)

def scalar_hessian(A,B):return np.block([[A.real+B.real,-A.imag-B.imag],[A.imag-B.imag,A.real-B.real]])

def component_data(Y,z,linear,R,g,mu=None,vertices=True):
    n=len(z);ng=len(R);nf=n+ng;nr=2*n
    if mu is None:mu=np.zeros((n,n),complex)
    E=np.concatenate([np.eye(n),1j*np.eye(n)],axis=1)/math.sqrt(2)
    F=linear+mu@z+.5*np.einsum('ijk,j,k->i',Y,z,z)
    M=mu+np.einsum('ijk,k->ij',Y,z)
    A=M.conj().T@M;B=np.einsum('k,kij->ij',F.conj(),Y)
    rz=np.einsum('aij,j->ai',R,z) if ng else np.zeros((0,n),complex)
    L=2*g*(E.conj().T@rz.T).real.T
    S=2*g*np.einsum('ia,pij,jb->pab',E.conj(),R,E,optimize=True).real if ng else np.zeros((0,nr,nr))
    D=g*np.einsum('i,ai->a',z.conj(),rz).real
    H=scalar_hessian(A,B)+L.T@L
    if ng:H+=np.einsum('p,pab->ab',D,S)
    J=math.sqrt(2)*g*np.einsum('i,aij->aj',z.conj(),R) if ng else np.zeros((0,n),complex)
    MF=np.block([[M,J.T],[J,np.zeros((ng,ng),complex)]])
    MV=2*g*g*(rz.conj()@rz.T).real
    ms2,O=eigh(H);mv2,Ov=eigh(MV) if ng else (np.empty(0),np.empty((0,0)))
    scale=max(1e-30,float(np.max(abs(ms2))),float(np.max(abs(MF)))**2)
    if min(ms2)<-2e-10*scale:raise ValueError('physical negative scalar mass at requested point')
    ms2[abs(ms2)<2e-11*scale]=0;mv2[abs(mv2)<2e-11*scale]=0
    # CP slice permits exact realification, avoiding degenerate SVD phase errors.
    if n==49:
        phases=np.r_[-1j,np.ones(24),np.full(24,-1j),np.ones(ng)]
    else:
        phases=np.ones(nf,complex)
    realMF=phases[:,None]*MF*phases[None,:]
    if np.max(abs(realMF.imag))>1e-9*max(1,float(np.max(abs(realMF)))):
        raise ValueError('Generic complex background needs another Takagi branch; not silently approximated')
    signed,V=eigh(realMF.real);mass=abs(signed);mass[mass**2<2e-11*scale]=0
    U=phases[:,None]*V*np.where(signed>=0,1,1j)[None,:]
    result={'mS2':ms2,'O':O,'mF':mass,'mF2':mass**2,'U':U,'mV2':mv2,'Ov':Ov,
            'MF':MF,'H':H,'MV':MV,'Y':Y,'z':z,'r0':np.r_[math.sqrt(2)*z.real,math.sqrt(2)*z.imag],
            'R':R,'g':g,'E':E,'L':L,'S':S,'F':F,'M_chiral':M,
            'controls':{'Takagi_max_error':float(np.max(abs(U.T@MF@U-np.diag(mass)))),
                        'U_unitarity_max_error':float(np.max(abs(U.conj().T@U-np.eye(nf)))),
                        'scalar_reconstruction_error':float(np.max(abs(O@np.diag(ms2)@O.T-H))),
                        'D_flat_max':float(np.max(abs(D))) if ng else 0}}
    if not vertices:return result
    Em=E@O;K=M@Em
    YR=np.einsum('ijk,ja,kb->iab',Y,Em,Em,optimize=True)
    Sm=np.einsum('pab,ai,bj->pij',S,O,O,optimize=True) if ng else S
    Lm=L@O
    C=np.einsum('ia,ibc->abc',K.conj(),YR,optimize=True)
    cubic=2*(C+C.transpose(1,0,2)+C.transpose(1,2,0)).real
    if ng:
        CD=np.einsum('pa,pbc->abc',Lm,Sm,optimize=True)
        cubic+=CD+CD.transpose(1,0,2)+CD.transpose(1,2,0)
    diag=np.diagonal(YR,axis1=1,axis2=2)
    quartic_iijj=2*(diag.conj().T@diag).real+4*np.sum(abs(YR)**2,axis=0)
    if ng:
        diagD=np.diagonal(Sm,axis1=1,axis2=2)
        quartic_iijj+=diagD.T@diagD+2*np.sum(Sm**2,axis=0)
    yuk=np.zeros((nf,nf,nr),complex)
    yuk[:n,:n]=np.einsum('ijk,ka->ija',Y,Em)
    if ng:
        dJ=math.sqrt(2)*g*np.einsum('ka,pki->pia',Em.conj(),R,optimize=True)
        yuk[n:,:n]=dJ;yuk[:n,n:]=dJ.transpose(1,0,2)
    yukmass=np.einsum('Iu,Jv,IJa->uva',U,U,yuk,optimize=True)
    result.update(cubic=cubic,quartic_iijj=quartic_iijj,yukawa=yukmass,Em=Em,YR=YR,Sm=Sm,Lm=Lm)
    return result

def build_model(X,h,lam,g,f=1.,a=None,b=None,vertices=True):
    h,lam,g,f,X=map(float,(h,lam,g,f,X))
    if a is None:a=math.sqrt(2*f*h/(30*h*h+lam*lam)) if f else 0.
    if b is None:b=h*X/lam
    z=np.r_[complex(X),1j*a*SU5_D,b*SU5_D];linear=np.r_[complex(f),np.zeros(48)]
    out=component_data(h*YH+lam*YL,z,linear,SU5_R,g,vertices=vertices)
    out.update(X=X,h=h,lam=lam,f=f,a=a,b=b)
    return out

def grouped(values,tolerance=2e-8):
    vals=np.asarray(values);groups=[];ids=np.empty(len(vals),int)
    floor=max(1e-24,float(np.max(abs(vals)))*1e-12)
    for idx in np.argsort(vals):
        x=float(vals[idx])
        if groups and abs(x-groups[-1]['mass2'])<=tolerance*max(floor,abs(x),abs(groups[-1]['mass2'])):
            item=groups[-1];item['indices'].append(int(idx));item['mass2']=float(np.mean(vals[item['indices']]))
        else:groups.append({'mass2':x,'indices':[int(idx)]})
        ids[idx]=len(groups)-1
    return groups,ids

def graph_weights(data):
    ss,si=grouped(data['mS2']);ff,fi=grouped(data['mF2'])
    ns,nf=len(ss),len(ff)
    cs=np.zeros((ns,ns,ns));qs=np.zeros((ns,ns));yf=np.zeros((nf,nf,ns));bf=np.zeros_like(yf)
    c3=data['cubic'];q4=data['quartic_iijj'];y=data['yukawa'];m=data['mF']
    # Exact degeneracy groups sum every ordered index; source prefactors include symmetry factors.
    for i,aa in enumerate(ss):
        a=aa['indices']
        for j,bb in enumerate(ss):
            b=bb['indices'];qs[i,j]=np.sum(q4[np.ix_(a,b)])/8
            for k,cc in enumerate(ss):
                cs[i,j,k]=np.sum(c3[np.ix_(a,b,cc['indices'])]**2)/12
    for i,aa in enumerate(ff):
        a=aa['indices']
        for j,bb in enumerate(ff):
            b=bb['indices']
            for k,cc in enumerate(ss):
                yy=y[np.ix_(a,b,cc['indices'])]
                yf[i,j,k]=np.sum(abs(yy)**2)/2
                bf[i,j,k]=np.sum((yy**2).real*m[a,None,None]*m[None,b,None])/2
    return {'scalar_groups':ss,'fermion_groups':ff,'SSS':cs,'SS':qs,'FFS':yf,'barFFS':bf}
