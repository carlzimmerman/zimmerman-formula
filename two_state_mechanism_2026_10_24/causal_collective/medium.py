"""Causal Maxwell/neutral-dipole candidate: static branch and local dynamics."""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


def source(x,chi,floor=0.):
    """g_b/a0 from g/a0: cold T, no countercharge, negligible medium gravity.

    beta²=4piG(1+chi); cutoff acceleration chi/(1+chi)*a0.
    The finite-gap variant preserves zero-field susceptibility.
    """
    f=chi/(1+chi);z=np.asarray(x)/f
    a=np.sqrt(1+z*z);b=np.sqrt(floor*floor+z*z)
    # Stable 1 - (1+floor)/(a+b) at very small fields.
    increment=z*z/(a+1)+np.divide(z*z,b+floor,out=np.zeros_like(z),where=(b+floor)>0)
    return np.asarray(x)*f*increment/(a+b)


def prediction(y,chi,floor=0.):
    if y==0:return 0.
    upper=max(1.,y*(1+chi)/chi+2.)
    while source(upper,chi,floor)<y:upper*=2
    return brentq(lambda x:source(x,chi,floor)-y,0.,upper,xtol=1e-14,rtol=1e-12)


def dielectric(E,chi):
    E=np.asarray(E);e=np.linalg.norm(E,axis=-1,keepdims=True)
    return E*(1+chi/(np.sqrt(1+e*e)+e))


def lagrangian(e,chi):
    e=np.asarray(e)
    return .5*e*e+chi/3*(np.expm1(1.5*np.log1p(e*e))-e**3)


def gap_quadrature(N,chi):
    nodes,weights=np.polynomial.legendre.leggauss(N)
    s=(nodes+1)/2;weights=weights/2
    return s,weights,chi*s*weights


def normal_modes(k,omega,strength,plasma):
    """Energy-normalized Hermitian normal-mode problem; returns omega, dω/dk."""
    n=len(omega);A=np.zeros((3+2*n,3+2*n),dtype=complex)
    A[0,1]=A[1,0]=-1j*k
    for j,(o,f) in enumerate(zip(omega,strength)):
        p=2+2*j;q=p+1
        A[0,q]=-np.sqrt(f);A[q,0]=np.sqrt(f)
        A[p,q]=o;A[q,p]=-o
    A[0,-1]=-plasma;A[-1,0]=plasma
    H=1j*A
    if np.max(np.abs(H-H.conj().T))>1e-13:raise ValueError('non-Hermitian linear energy system')
    w,v=np.linalg.eigh(H)
    return w,2*np.real(v[0].conj()*v[1])


def nonlinear(initialD=.1,chi=10.,N=32,duration=30.,rtol=1e-9):
    """Homogeneous D, neutral excitations, explicit relativistic +/- momenta.

    hbar=c=d=Es_max=m_plus=q=1, m_minus=.1, equal number densities=.1.
    No ionization, external drive, damping, fixed countercharge or energy repair.
    """
    s,w,n=gap_quadrature(N,chi);delta=2*s;density=.1;eps=.1
    initial=np.zeros(3+2*N,dtype=complex);initial[0]=initialD;initial[3:3+N]=1.
    def rhs(t,y):
        D,pp,pm=y[:3].real;c0=y[3:3+N];c1=y[3+N:]
        P=2*np.sum(n*np.real(c0.conj()*c1));E=D-P
        vp=pp/np.sqrt(1+pp*pp);vm=pm/np.sqrt(eps*eps+pm*pm)
        return np.concatenate(([-density*(vp-vm),E,-E],1j*E*c1,1j*E*c0-1j*delta*c1))
    sol=solve_ivp(rhs,(0,duration),initial,method='DOP853',rtol=rtol,atol=rtol*1e-3,
                  t_eval=np.linspace(0,duration,2001))
    if not sol.success:raise RuntimeError(sol.message)
    D,pp,pm=sol.y[:3].real;c0=sol.y[3:3+N];c1=sol.y[3+N:]
    P=2*np.sum(n[:,None]*np.real(c0.conj()*c1),axis=0);E=D-P
    kinetic=density*(np.hypot(1,pp)-1+np.hypot(eps,pm)-eps)
    excitation=np.sum((n*delta)[:,None]*abs(c1)**2,axis=0)
    H=.5*E*E+kinetic+excitation;H0=.5*initialD**2
    return dict(initialD=initialD,chi=chi,gap_nodes=N,duration=duration,
                energy_error=float(np.max(abs(H-H0))/H0),
                norm_error=float(np.max(abs(abs(c0)**2+abs(c1)**2-1))),
                momentum_error=float(np.max(abs(density*(pp+pm)))),
                max_speed=float(max(np.max(abs(pp/np.hypot(1,pp))),np.max(abs(pm/np.hypot(eps,pm))))),
                net_free_charge=0.,max_counter_momentum=float(np.max(abs(pm))),
                final=[float(D[-1]),float(pp[-1]),float(pm[-1]),float(excitation[-1])],
                evaluations=sol.nfev)
