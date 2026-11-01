"""Finite heavy-singlet tadpoles from full mass-matrix spectral derivatives.

Float64 first derivatives only. Do not feed normal_data_reference to mp.diff
infinitesimal differentiation: use finite stencils and an explicit repeat.
No direct two-loop vacuum or direct one-loop derivative graph is included.
"""
import sys,math
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
import mpmath as mp
from improved import evaluate
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/three_priorities_2026_11_01/spectrum_pressure'))
from spectrum import R,d,tensor
YH=tensor(1.,0.);YL=tensor(0.,1.)

def real_hessian(A,B):return np.block([[A.real+B.real,-A.imag-B.imag],[A.imag-B.imag,A.real-B.real]])

def matrices(X,a,b,c,dz=None):
    h,l,g,f=map(float,c);Y=h*YH+l*YL;z=np.r_[complex(X),1j*a*d,b*d]
    F=.5*np.einsum('ijk,j,k->i',Y,z,z);F[0]+=f
    M=np.einsum('ijk,k->ij',Y,z);B=np.einsum('k,kij->ij',F.conj(),Y)
    rz=np.einsum('aij,j->ai',R,z);L=math.sqrt(2)*g*np.concatenate([rz.real,rz.imag],axis=1)
    H=real_hessian(M.conj().T@M,B)+L.T@L
    J=math.sqrt(2)*g*np.einsum('i,aij->aj',z.conj(),R)
    MF=np.block([[M,J.T],[J,np.zeros((24,24),complex)]])
    AF=MF.conj().T@MF;MV=2*g*g*(rz.conj()@rz.T).real
    if dz is None:return [H,AF,MV]
    dF=M@dz;dM=np.einsum('ijk,k->ij',Y,dz);dB=np.einsum('k,kij->ij',dF.conj(),Y)
    drz=np.einsum('aij,j->ai',R,dz);dL=math.sqrt(2)*g*np.concatenate([drz.real,drz.imag],axis=1)
    dH=real_hessian(dM.conj().T@M+M.conj().T@dM,dB)+dL.T@L+L.T@dL
    dJ=math.sqrt(2)*g*np.einsum('i,aij->aj',dz.conj(),R)
    dMF=np.block([[dM,dJ.T],[dJ,np.zeros((24,24),complex)]])
    dAF=dMF.conj().T@MF+MF.conj().T@dMF
    dMV=2*g*g*(drz.conj()@rz.T+rz.conj()@drz.T).real
    return [dH,dAF,dMV]

def normal_data(X,c,Q=1.,cp_controls=False):
    h,l,g,f=map(float,c);X=float(X);Q=float(Q)
    a=math.sqrt(2*f*h/(30*h*h+l*l));b=h*X/l
    mm=matrices(X,a,b,[h,l,g,f]);eigens=[eigh(m) for m in mm]
    directions=[np.r_[0j,1j*d,np.zeros(24)],np.r_[0j,np.zeros(24),d]]
    if cp_controls:directions += [np.r_[0j,d,np.zeros(24)],np.r_[0j,np.zeros(24),1j*d]]
    grads=[]
    for dz in directions:
        dm=matrices(X,a,b,[h,l,g,f],dz);total=0.
        for weight,(v,V),dv in zip([1,-2,3],eigens,dm):
            hp=np.zeros_like(v);mask=v>1e-12*max(1,float(max(v)))
            hp[mask]=2*v[mask]*(np.log(v[mask]/(Q*Q))-1)
            diag=np.einsum('ij,ij->j',V.conj(),dv@V).real
            total+=weight*float(np.dot(hp,diag))
        grads.append(total/(64*math.pi**2))
    Ha=120*f*h;Hb=60*l*l*a*a;da=-grads[0]/Ha;db=-grads[1]/Hb
    ans={'CWa':grads[0],'CWb':grads[1],'Haa':Ha,'Hbb':Hb,'a0':a,'b0':b,'X_running':X,
         'deltaa':da,'deltab':db,'deltaU_vac':-.5*(grads[0]**2/Ha+grads[1]**2/Hb),
         'F0':X*X+30*b*b,'deltaF_angular':60*b*db,'F_b':60*b,
         'a_relative_shift':da/a,'b_relative_shift':db/b if b else None,
         'min_scalar_m2':float(min(eigens[0][0]))}
    if cp_controls:ans['CP_odd_tadpoles']=grads[2:]
    return ans

def normal_data_reference(X0,e,steps=32,cp_controls=False):
    """Local matching at centralQm with running couplings/canonical fields."""
    o=evaluate(X0,e,1,'rg2',steps)
    ans=normal_data(o['X_running'],o['couplings'],o['Qm'],cp_controls)
    ans.update(Qm=float(o['Qm']),U_RG=float(o['U']),F_RG=float(o['F']))
    return ans
