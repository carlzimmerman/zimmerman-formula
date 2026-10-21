"""Pure outgoing solve for an explicitly supplied reduced canonical force.

No profile regeneration, force normalization or physical source is implicit.
Order: (sqrt2u,sqrt2s,xi,sqrt2v,sqrt2tX), reduced by r.
Time convention: +iOmega t plus conjugate; outgoing circular Hankel h2.
"""
import cmath
import math
import numpy as np
from scipy.sparse import coo_matrix, eye
from scipy.sparse.linalg import splu

def hankel_polynomial(ell,z,closed=False):
    """Reduced h2=e^-iz P_l(z); reduced decaying k=e^-z P_l^K(z)."""
    if not isinstance(ell,int) or ell<0:
        raise ValueError('ell must be a nonnegative integer')
    unit=1. if closed else -1j
    return sum(math.factorial(ell+k)/(math.factorial(k)*math.factorial(ell-k))
               *(unit/(2*z))**k for k in range(ell+1))

def ghost_ratio(ell,p2,r,dr):
    if abs(p2)<1e-14:
        return complex((r/(r+dr))**ell)
    if p2>0:
        p=math.sqrt(p2)
        return cmath.exp(-1j*p*dr)*hankel_polynomial(ell,p*(r+dr))/hankel_polynomial(ell,p*r)
    k=math.sqrt(-p2)
    return complex(math.exp(-k*dr)*hankel_polynomial(ell,k*(r+dr),True)/hankel_polynomial(ell,k*r,True))

def circular_transform():
    T=np.zeros((5,5),complex)
    T[0,0]=T[1,0]=T[2,1]=T[3,1]=1/math.sqrt(2)
    T[0,3]=T[2,4]=1j/math.sqrt(2)
    T[1,3]=T[3,4]=-1j/math.sqrt(2)
    T[4,2]=1
    return T

def outgoing_solve(op,Omega,F,params,m=0):
    """Solve A_l(Omega)y=F with free outgoing/decaying exterior ghost ratios.

    `op` is a radial_tools.operators result, including its own ell and relaxed
    stationary background. `F` is the explicit complex 5N reduced source; it is
    not normalized or projected here. The caller owns any profile/source hashes,
    perturbative amplitude convention, and source E/Q/J accounting.

    Returns `summary` (JSON-safe scalars/channels), `y`, `force`, `circular_last`,
    and `circular_ghost`. No files are written. Closed-channel boundary tails and
    grid/box convergence remain the caller's responsibility.
    """
    N=op['N'];r=op['r'];dr=op['dr'];ell=op['ell'];w=op['record']['omega']
    if not (Omega>0 and 0<w<1 and 2*w<math.sqrt(params['MX2'])):
        raise ValueError('This normalization requires Omega>0 and bound vacuum frequencies')
    if abs(m)>ell:
        raise ValueError('|m| cannot exceed ell')
    F=np.asarray(F,dtype=complex)
    if F.shape!=(5*N,) or not np.all(np.isfinite(F)):
        raise ValueError('force must be a finite complex reduced vector of length5N')
    T=circular_transform()
    nus=np.array([w+Omega,w-Omega,2*w+Omega,2*w-Omega,Omega])
    mus=np.array([1.,1.,math.sqrt(params['MX2']),math.sqrt(params['MX2']),params['M_chi']])
    p2=nus*nus-mus*mus
    rho=np.array([ghost_ratio(ell,x,r[-1],dr) for x in p2])
    boundary=T.conj().T@np.diag(rho)@T
    ends=np.arange(1,6)*N-1
    edge=coo_matrix((-boundary.reshape(-1)/(dr*dr),(np.repeat(ends,5),np.tile(ends,5))),shape=(5*N,5*N)).tocsc()
    A=(op['W']-Omega*Omega*eye(5*N,format='csc')+1j*Omega*op['G']+edge).tocsc()
    y=splu(A).solve(F)
    normF=float(np.linalg.norm(F))
    residual=float(np.linalg.norm(A@y-F)/max(normF,1e-300))
    c=T@y[ends];cg=rho*c
    K=-2*Omega/dr*np.imag(np.conj(c)*cg)
    Kcontinuum=np.array([2*Omega*math.sqrt(pp)*abs(cc/hankel_polynomial(ell,math.sqrt(pp)*r[-1]))**2
                         if pp>0 else 0. for pp,cc in zip(p2,c)])
    work=float(2*Omega*np.imag(dr*np.vdot(y,F)))
    channels=[]
    for j,(name,q,sig) in enumerate(zip(['Psi+','Psi-','X+','X-','chi'],[1,1,2,2,0],[1,-1,1,-1,0])):
        channels.append({'name':name,'open':bool(p2[j]>0),'lab_frequency':float(nus[j]),'p2':float(p2[j]),
                         'K_edge':float(K[j]),'K_continuum_amplitude':float(Kcontinuum[j]),
                         'E_edge':float((1+sig*q*w/Omega)*K[j]),'Q_edge':float(sig*q/Omega*K[j]),
                         'Jz_edge':float(m/Omega*K[j])})
    total=float(np.sum(K));cont=float(np.sum(Kcontinuum))
    summary={'Omega':float(Omega),'omega':float(w),'ell':int(ell),'m':int(m),
             'Q':op['record']['Q_target'],'L':op['record']['L'],'N':N,'dr':float(dr),
             'K_edge_total':total,'K_continuum_total':cont,'K_source_work':work,
             'source_work_relative_difference':abs(total-work)/max(abs(total)+abs(work),1e-10),
             'linear_relative_residual':residual,'force_radial_L2_squared':float(dr*np.vdot(F,F).real),
             'response_radial_L2_squared':float(dr*np.vdot(y,y).real),
             'channels':channels,'E_edge_total':sum(c['E_edge'] for c in channels),
             'Q_edge_total':sum(c['Q_edge'] for c in channels),'Jz_edge_total':sum(c['Jz_edge'] for c in channels)}
    return {'summary':summary,'y':y,'force':F,'circular_last':c,'circular_ghost':cg}
