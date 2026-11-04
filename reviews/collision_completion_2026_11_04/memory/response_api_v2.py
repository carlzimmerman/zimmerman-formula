"""CC10 actual four-state, dilute charged-continuum periodic response.

Units mu=1, tau=mu*t. Empty neutral daughter vacuum widths are held fixed.
The retarded charged self-energy is NOT resummed dynamically here. All returned
matrices retain the actual four neutral states, with one charged production
vector extracted from the numerical rank-one Gram.
"""
import sys
sys.dont_write_bytecode=True
import json, math
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import jv
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[3]
PRIOR=ROOT/'reviews/coupled_trapping_2026_11_04'
POLE=json.loads((PRIOR/'microphysics/run_pole002/result.json').read_text())
MEDIUM=json.loads((PRIOR/'microphysics/run_medium001/result.json').read_text())
G=np.asarray(POLE['production_Gram_mu2'],float)
GAMMA=np.asarray(POLE['Gamma_other_matrix_mu'],float)
GAMMA_SSS=np.asarray(MEDIUM['Gamma_SSS_matrix_mu'],float)
GAMMA_FFS=np.asarray(MEDIUM['Gamma_FFS_matrix_mu'],float)
M=float(POLE['Mpole']); XPOLE=float(POLE['xpole'])
eigen_g,Vg=np.linalg.eigh(G); LAMBDA=float(eigen_g[-1]); VECTOR=Vg[:,-1]
WIDTH,U=np.linalg.eigh(GAMMA); COEFF=U.T@VECTOR

def charged_mass(x):
    return .0015*np.sqrt(np.asarray(x)**2+2/(31*.003))

def charged_mass_derivative(x):
    return .0015*x/math.sqrt(x*x+2/(31*.003))

def continuum_nodes(edges,f_number,radial=3,angular=12,tail=1e-14):
    """Independent isotropic pair measure normalized to one.

    f_number is CT09 fS, so actual scalar occupation is 2*f_number. The factor
    two cancels from this normalized pair measure and is restored in density.
    Returned q1,q2,cosine,w are product Gauss rules inside the actual cells.
    Tail selects cells by total number and reports omitted fraction explicitly.
    """
    edges=np.asarray(edges,float); f=np.asarray(f_number,float)
    cell=f*(edges[1:]**3-edges[:-1]**3)/3
    keep=cell>float(cell.sum())*tail
    z,w=leggauss(radial); aa=edges[:-1][keep]; bb=edges[1:][keep]
    q=((aa+bb)[:,None]/2+(bb-aa)[:,None]/2*z).ravel()
    qw=(f[keep,None]*(bb-aa)[:,None]/2*w*q.reshape(-1,radial)**2).ravel()
    omitted=1-float(cell[keep].sum()/cell.sum()); qw/=qw.sum()
    az,aw=leggauss(angular)
    q1,q2,c=np.meshgrid(q,q,az,indexing='ij')
    pairw=qw[:,None,None]*qw[None,:,None]*aw[None,None,:]/2
    return q1.ravel(),q2.ravel(),c.ravel(),pairw.ravel(),omitted

def mode_data(xmid,amplitude,omega,Tc,edges,f_number,radial=3,angular=12):
    q1,q2,c,w,omitted=continuum_nodes(edges,f_number,radial,angular)
    p1=Tc*q1;p2=Tc*q2;m=float(charged_mass(xmid));dm=charged_mass_derivative(xmid)
    e1=np.sqrt(m*m+p1*p1);e2=np.sqrt(m*m+p2*p2)
    P2=p1*p1+p2*p2+2*p1*p2*c; ep=np.sqrt(M*M+P2)
    # Stable subtraction when all physical detunings are tiny compared with M.
    delta=(((M-2*m)*(M+2*m)+P2)/(ep+2*m)
           -p1*p1/(e1+m)-p2*p2/(e2+m))
    A=amplitude*m*dm*(1/e1+1/e2)
    pref=LAMBDA/(4*e1*e2*ep)
    return dict(delta=delta,A=A,z=A/omega,pref=pref,boost=M/ep,w=w,
                p1=p1,p2=p2,cosine=c,omitted_number_fraction=omitted)

def _matrix_from_eigen(r):
    return U@r@U.T

def orbit_response(xmid,amplitude,omega,Tc,edges,f_number,radial=3,angular=12,
                   phase_nodes=256,return_modes=False):
    """Positive continuum-averaged parent density per n+*n- and decay rate.

    rho_pair has dimensions mu^-3; n± = 12*Tc³/(2pi²)*sum(W*f_number).
    rate_pair = Tr(Gamma*rho_pair), dimensions mu^-2, is physical pair sigma*v
    in the leading narrow-resonance relativistic normalization. Lab boosts
    are kept per mode in the decay matrix; returned rest density and exit
    rates use that distinction exactly inside the declared model.
    """
    d=mode_data(xmid,amplitude,omega,Tc,edges,f_number,radial,angular)
    delta,A,z,pref,boost,w=(d[k] for k in ('delta','A','z','pref','boost','w'))
    nmax=int(math.ceil(float(max(z))+12+4*float(max(z))**(1/3)))
    rd=np.zeros((4,4),complex);rs=np.zeros((4,4),complex)
    exitd=0.;exits=0.;sideband_weights=[]
    for n in range(-nmax,nmax+1):
        J2=jv(n,z)**2
        r=COEFF[None,:]/(WIDTH[None,:]*boost[:,None]/2+1j*(delta+n*omega)[:,None])
        ww=w*pref*J2
        rd+=np.einsum('n,ni,nj->ij',ww,r,r.conj(),optimize=True)
        exitd+=float(np.sum(ww*boost*np.sum(WIDTH[None,:]*abs(r)**2,axis=1)))
        sideband_weights.append([n,float(w@J2)])
    # Exact arcsine/Stieltjes phase integral. Re(a)>0 fixes the square-root branch.
    aa=WIDTH[None,:]*boost[:,None]/2+1j*delta[:,None]
    F=1/np.sqrt(aa*aa+A[:,None]**2)
    denom=boost[:,None,None]*(WIDTH[None,:,None]+WIDTH[None,None,:])/2
    phase_rr=(F[:,:,None]+F[:,None,:].conj())/denom
    rs=np.einsum('n,nij,i,j->ij',w*pref,phase_rr,COEFF,COEFF.conj(),optimize=True)
    exits=float(np.sum(w*pref*2*np.sum(abs(COEFF)[None,:]**2*F.real,axis=1)))
    rho=_matrix_from_eigen(rd); staticrho=_matrix_from_eigen(rs)
    e=np.asarray(edges);f=np.asarray(f_number)
    one_number=12*Tc**3/(2*math.pi**2)*float(((e[1:]**3-e[:-1]**3)/3)@f)
    # Positive injection closure preserving total decay trace; it is a separate
    # secular approximation to exact coherent injection and its error is exposed.
    sqrtwidth=np.sqrt(WIDTH); inj_eig=sqrtwidth[:,None]*rd*sqrtwidth[None,:]
    lyap_eig=(WIDTH[:,None]+WIDTH[None,:])/2*rd
    injection=_matrix_from_eigen(inj_eig)
    out=dict(dynamic_pair_sigma_v=exitd,stationary_pair_sigma_v=exits,
             multiplier=exitd/exits,rho_pair=rho,rho_pair_stationary=staticrho,
             parent_density_mu3=one_number**2*float(np.trace(rho).real),
             event_rate_mu4=one_number**2*exitd,one_sign_charged_density_mu3=one_number,
             positive_injection_pair=injection,
             positive_injection_vs_Lyapunov_relative=float(np.linalg.norm(inj_eig-lyap_eig)/np.linalg.norm(lyap_eig)),
             sidebands=sideband_weights,nmax=nmax,
             omitted_number_fraction=d['omitted_number_fraction'],
             max_boost_error=float(max(1-boost)),
             rho_min_eigenvalue=float(np.linalg.eigvalsh(rho).min()))
    if return_modes:out['modes']=d
    return out

def parent_decay_step(rho,dt,source=None,H=None,Gamma=GAMMA):
    """Positive exact constant-coefficient neutral evolution and exit count.

    rho_dot=S-i[H,rho]-{Gamma,rho}/2. Source must be PSD for this closure.
    Returns rho and total neutral exits; density and force belong in ledger.
    Van Loan block integration retains coherences, without Γ/ω elimination.
    """
    from scipy.linalg import expm
    rho=np.asarray(rho,complex); Gamma=np.asarray(Gamma,complex)
    H=np.zeros((4,4),complex) if H is None else np.asarray(H,complex)
    S=np.zeros((4,4),complex) if source is None else np.asarray(source,complex)
    A=-1j*H-Gamma/2; B=np.zeros((8,8),complex)
    B[:4,:4]=A;B[:4,4:]=S;B[4:,4:]=-A.conj().T
    E=expm(B*dt); K=E[:4,:4]; add=E[:4,4:]@K.conj().T
    final=K@rho@K.conj().T+add
    exits=float(np.trace(rho+dt*S-final).real)
    return (final+final.conj().T)/2,exits

def serialize(value):
    if isinstance(value,np.ndarray):
        if np.iscomplexobj(value):return dict(real=value.real.tolist(),imag=value.imag.tolist())
        return value.tolist()
    if isinstance(value,dict):return {k:serialize(v) for k,v in value.items()}
    if isinstance(value,list):return [serialize(v) for v in value]
    if isinstance(value,np.generic):return value.item()
    return value
