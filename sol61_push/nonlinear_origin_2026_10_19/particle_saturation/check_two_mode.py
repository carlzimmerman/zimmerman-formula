"""Declared Gaussian Galerkin control; no continuum accuracy claim. Python 3.9+."""
import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.special import erf


def coulomb(d, width):
    return 2 / (math.sqrt(math.pi) * width) if abs(d) < 1e-14 else erf(abs(d) / width) / abs(d)


def overlaps(a=3.5, ell=1.0, B=0.7, m=1.0, hbar=1.0, Mb=1e9, G=1e-8):
    centers = np.array([-a, a])
    s = math.exp(-a*a/(ell*ell))
    p, q = (1+s)**-0.5, (1-s)**-0.5
    C = np.array([[(p+q)/2, (p-q)/2], [(p-q)/2, (p+q)/2]])
    S = np.empty((2, 2)); K = np.empty((2, 2)); V = np.empty((2, 2)); P = np.empty((2, 2), complex)
    for i, j in itertools.product(range(2), repeat=2):
        d = centers[i]-centers[j]
        S[i,j] = math.exp(-d*d/(4*ell*ell))
        K[i,j] = hbar*hbar/(2*m)*S[i,j]*(3/(2*ell*ell)-d*d/(4*ell**4))
        mid = (centers[i]+centers[j])/2
        V[i,j] = -G*m*Mb/2*S[i,j]*sum(coulomb(mid-b, math.sqrt(ell*ell+B*B)) for b in centers)
        P[i,j] = 1j*hbar*d/(2*ell*ell)*S[i,j]
    contact = np.zeros((2,2,2,2)); grav = np.zeros_like(contact)
    c0 = (2*math.pi)**-1.5/ell**3
    for inds in itertools.product(range(2), repeat=4):
        cc = centers[list(inds)]
        contact[inds] = c0*math.exp(-(sum(cc*cc)-sum(cc)**2/4)/(2*ell*ell))
        i,j,k,l = inds
        grav[inds] = -G*m*m*S[i,k]*S[j,l]*coulomb((centers[i]+centers[k]-centers[j]-centers[l])/2, math.sqrt(2)*ell)
    trans = lambda x: np.einsum('ai,bj,ck,dl,abcd->ijkl',C,C,C,C,x)
    return dict(a=a,ell=ell,B=B,m=m,hbar=hbar,Mb=Mb,G=G,s=s,C=C,centers=centers,
                S=C.T@S@C,K=C.T@K@C,V=C.T@V@C,P=C.T@P@C,contact=trans(contact),grav=trans(grav))


def apply_ops(state, annihilate, create):
    counts = list(state); amplitude = 1.0
    for i in annihilate:
        if not counts[i]:
            return None, 0
        amplitude *= math.sqrt(counts[i]); counts[i] -= 1
    for i in create:
        amplitude *= math.sqrt(counts[i]+1); counts[i] += 1
    return tuple(counts), amplitude


def hamiltonian(N, o, g2, include_gravity=True, include_recoil=True):
    h = o['K']*(1+o['m']/o['Mb'] if include_recoil else 1)+o['V']
    v = g2*o['contact']+(o['grav'] if include_gravity else 0)
    if include_recoil:
        v = v + np.einsum('ik,jl->ijkl',o['P'],o['P']).real/o['Mb']
    H = np.zeros((N+1,N+1))
    for n in range(N+1):
        state = (N-n,n)
        for i,j in itertools.product(range(2),repeat=2):
            out,fac=apply_ops(state,[j],[i])
            if out is not None: H[out[1],n] += h[i,j]*fac
        for i,j,k,l in itertools.product(range(2),repeat=4):
            out,fac=apply_ops(state,[k,l],[j,i])
            if out is not None: H[out[1],n] += v[i,j,k,l]*fac/2
    return H-N*h[0,0]*np.eye(N+1)


def gamma_and_derivative(N,A,B=None):
    out=np.zeros((N+1,N+1),complex); der=np.zeros_like(out)
    for n,np_ in itertools.product(range(N+1),repeat=2):
        norm=math.sqrt(math.factorial(N-np_)*math.factorial(np_)/(math.factorial(N-n)*math.factorial(n)))
        for r in range(max(0,np_-n),min(N-n,np_)+1):
            t=np_-r
            powers=[N-n-r,r,n-t,t]
            vals=[A[0,0],A[1,0],A[0,1],A[1,1]]
            coef=norm*math.comb(N-n,r)*math.comb(n,t)
            prod=complex(1)
            for x,p in zip(vals,powers): prod *= x**p
            out[np_,n] += coef*prod
            if B is not None:
                bvals=[B[0,0],B[1,0],B[0,1],B[1,1]]
                for j,p in enumerate(powers):
                    if not p: continue
                    term=complex(p*bvals[j])
                    for i,(x,power) in enumerate(zip(vals,powers)): term *= x**(power-(i==j))
                    der[np_,n] += coef*term
    return out,der


def source(N,o,k):
    if k==0: return np.zeros((N+1,N+1))
    alpha=o['m']/(o['Mb']+N*o['m'])
    def A(t):
        mat=np.empty((2,2),complex)
        for i,j in itertools.product(range(2),repeat=2):
            d=o['centers'][i]-o['centers'][j]
            mat[i,j]=np.exp(-d*d/(4*o['ell']**2)-t*t*o['ell']**2/4+1j*t*(o['centers'][i]+o['centers'][j])/2)
        return o['C'].T@mat@o['C']
    gam,der=gamma_and_derivative(N,A(-k*alpha),A(k*(1-alpha)))
    Fb=math.exp(-o['B']**2*k*k/4)*math.cos(k*o['a'])
    characteristic=o['m']*der+o['Mb']*Fb*gam
    return ((characteristic-characteristic.conj().T)/(2j*k)).real


def response(H,D,E,beta=None):
    vals,vecs=np.linalg.eigh(H-E*D)
    obs=np.diag(vecs.T@D@vecs)
    if beta is None: return float(obs[0]), vals, vecs
    p=np.exp(-beta*(vals-vals[0]));p/=sum(p)
    return float(p@obs),vals,vecs


def direct_distinguishable_source(N,o,k):
    # Orthogonal second implementation: N=1,2 tensor-product multiplication, then symmetrize.
    alpha=o['m']/(o['Mb']+N*o['m'])
    def A(t):
        raw=np.array([[np.exp(-(x-y)**2/(4*o['ell']**2)-t*t*o['ell']**2/4+1j*t*(x+y)/2) for y in o['centers']] for x in o['centers']])
        return o['C'].T@raw@o['C']
    base=A(-k*alpha); special=A(k*(1-alpha))
    kron=lambda mats: np.array([[1]],complex) if not mats else np.kron(mats[0],kron(mats[1:]))
    char=o['Mb']*math.exp(-o['B']**2*k*k/4)*math.cos(k*o['a'])*kron([base]*N)
    for j in range(N): char += o['m']*kron([special if i==j else base for i in range(N)])
    sym=np.zeros((2**N,N+1))
    for index,bits in enumerate(itertools.product(range(2),repeat=N)):
        n=sum(bits);sym[index,n]=1/math.sqrt(math.comb(N,n))
    return (sym.T@((char-char.conj().T)/(2j*k))@sym).real


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    o=overlaps();checks=[];cases=[]
    def check(name,error,tol):
        checks.append(dict(name=name,error=float(error),tolerance=tol,passed=bool(error<tol)))
    check('orthonormality',np.max(abs(o['S']-np.eye(2))),1e-12)
    J=-float((o['K']+o['V'])[0,1]); check('positive tunnel splitting',max(0,-J),1e-14)
    for N in [1,2]:
        check('full-recoil source tensor benchmark N='+str(N),np.max(abs(source(N,o,.25)-direct_distinguishable_source(N,o,.25))),1e-10)
    N=4;D=source(N,o,.25); Hfree=hamiltonian(N,o,0,False,False)
    d=1.0;Dfree=np.diag(np.arange(-N,N+1,2)*d)
    for h in [0,.1*J,J,10*J]:
        actual=response(Hfree,Dfree,h)[0]
        expected=N*h/math.sqrt(J*J+h*h)
        check('noninteracting N=4 h/J='+str(h/J),abs(actual-expected),1e-10)
    for N,g2 in itertools.product([1,2,4,8,12],[1e-4,5e-4]):
        H=hamiltonian(N,o,g2); D=source(N,o,.25); reverse=np.eye(N+1)[::-1]
        # Independent fixed-N expansion of the contact tensor.
        U=g2*o['contact'][0,0,0,0]; T=g2*o['contact'][0,0,0,1]; W=g2*o['contact'][0,0,1,1]
        contact_closed=np.zeros_like(H)
        for n in range(N+1):
            L=N-n
            contact_closed[n,n]=U/2*(L*(L-1)+n*(n-1))+2*W*L*n
            if n<N:
                contact_closed[n+1,n]=contact_closed[n,n+1]=T*(N-1)*math.sqrt((n+1)*L)
            if n+2<=N:
                contact_closed[n+2,n]=contact_closed[n,n+2]=W/2*math.sqrt((n+1)*(n+2)*L*(L-1))
        tensor_contact=hamiltonian(N,o,g2,False,False)-hamiltonian(N,o,0,False,False)
        check('contact tensor vs fixed-N expansion '+str((N,g2)),np.max(abs(contact_closed-tensor_contact)),1e-12)
        check('Hamiltonian hermiticity '+str((N,g2)),np.max(abs(H-H.T)),1e-12)
        check('H parity '+str((N,g2)),np.max(abs(reverse@H@reverse-H)),1e-12)
        check('D parity '+str((N,g2)),np.max(abs(reverse@D@reverse+D)),1e-10)
        dv,dw=np.linalg.eigh(D); psat=float(dv[-1]); HD=dw.T@H@dw
        A=float(sum(abs(HD[j,-1])**2/(psat-dv[j]) for j in range(N)))
        p0,ev,Q=response(H,D,0); gaps=ev[1:]-ev[0]; spectral=(Q.T@D@Q)[:,0]
        chi=float(2*sum(spectral[1:]**2/gaps)); beta=1/J
        boltz=np.exp(-beta*(ev-ev[0]));boltz/=sum(boltz)
        DO=Q.T@D@Q; chith=0.
        for i in range(N+1):
            for j in range(i+1,N+1): chith+=2*(boltz[i]-boltz[j])*DO[i,j]**2/(ev[j]-ev[i])
        step=1e-4*J/max(psat/N,1e-12)
        check('ground Kubo derivative '+str((N,g2)),abs((response(H,D,step)[0]-response(H,D,-step)[0])/(2*step)-chi)/max(chi,1),1e-5)
        check('thermal Kubo derivative '+str((N,g2)),abs((response(H,D,step,beta)[0]-response(H,D,-step,beta)[0])/(2*step)-chith)/max(chith,1),1e-5)
        curves=[]
        for x in [0,.1,1,10,100,1000,10000,100000]:
            E=x*J/(psat/N); val=response(H,D,E)[0]
            curves.append(dict(scaled_bias=x,E=E,P=val,normalized=val/psat,deficit=psat-val,scaled_deficit=(psat-val)*E*E))
        check('high field coefficient '+str((N,g2)),abs(curves[-1]['scaled_deficit']/A-1),.004)
        coherent=np.array([math.sqrt(math.comb(N,n)/2**N) for n in range(N+1)])
        coherent_p=abs(Q.T@coherent)**2
        krows=[]
        for k in [.01,.02,.04,.08]:
            dk=source(N,o,k);spec=(Q.T@dk@Q)[:,0]
            ck=float(2*sum(spec[1:]**2/gaps));krows.append(dict(k=k,Dnorm=float(np.linalg.norm(dk,2)),chi=ck,chi_over_k4=ck/k**4))
        check('source k2 scaling '+str((N,g2)),abs(krows[0]['Dnorm']/krows[1]['Dnorm']*4-1),.005)
        cases.append(dict(N=N,g2=g2,ground_energy=float(ev[0]),gaps=gaps.tolist(),
                          ground_source_weights=(spectral[1:]**2).tolist(),ground_chi=chi,thermal_chi=chith,
                          beta=beta,thermal_populations=boltz.tolist(),coherent_populations=coherent_p.tolist(),
                          D_eigenvalues=dv.tolist(),P_sat=psat,high_field_A=A,curves=curves,IR=krows))
    summary=dict(assertion_tested='Analytic Gaussian overlap projection and complete fixed-N matrices for N in {1,2,4,8,12}, dimensionless g2 in {1e-4,5e-4}; no continuum convergence assertion.',
                 parameters={k:o[k] for k in ['a','ell','B','m','hbar','Mb','G','s']},
                 overlaps=dict(J=J,contact_A=float(o['contact'][0,0,0,0]),contact_B=float(o['contact'][0,0,0,1]),contact_C=float(o['contact'][0,0,1,1]),
                               single_particle_h=(o['K']+o['V']).tolist(),gravity_tensor=o['grav'].tolist(),momentum_matrix_imag=o['P'].imag.tolist()),
                 cases=cases,checks=checks,passed=all(x['passed'] for x in checks),check_count=len(checks))
    path=Path(args.output);path.write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(dict(passed=summary['passed'],check_count=len(checks),overlaps=summary['overlaps'],failed=[x for x in checks if not x['passed']]),indent=2))
    if not summary['passed']: raise SystemExit(1)


if __name__=='__main__': main()
