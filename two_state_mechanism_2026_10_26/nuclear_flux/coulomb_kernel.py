"""Fixed-R Feshbach kernel from actual inner H and a pure-Coulomb outer lead.

Outer multipole neglect is explicit and tested against UKRmol propagation.
This is electronic, not the full nonlocal electron+nuclear kernel.
"""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.io import FortranFile
import mpmath as mp
from extract_inner import read_ci,read_boundary
mp.mp.dps=35

def channels(path):
    f=FortranFile(path);f.read_record('u1');f.read_record('u1');nt,nv,nd,n=f.read_ints('<i8');f.read_record('u1');targets=[]
    for _ in range(nt):
        a=f.read_record('u1').tobytes();targets.append(np.frombuffer(a[32:],dtype='<f8')[0])
    target=[];ell=[]
    for _ in range(n):
        a=f.read_record('u1').tobytes();ids=np.frombuffer(a[:32],dtype='<i8');target.append(targets[ids[1]-1]);ell.append(int(ids[2]))
    return np.array(target),np.array(ell)

def references(E,target,ell,radius):
    cache={};out=[]
    for et,l in zip(target,ell):
        key=(float(et),int(l))
        if key not in cache:
            e=E-et
            if e>0:
                k=mp.sqrt(2*e);eta=-1/k;rho=k*radius
                F=mp.coulombf(l,eta,rho)/mp.sqrt(k);G=mp.coulombg(l,eta,rho)/mp.sqrt(k)
                Fp=mp.diff(lambda r:mp.coulombf(l,eta,k*r)/mp.sqrt(k),radius);Gp=mp.diff(lambda r:mp.coulombg(l,eta,k*r)/mp.sqrt(k),radius)
                L=(Gp+1j*Fp)/(G+1j*F)
                cache[key]=(complex(L),float(F),float(G),float(Fp),float(Gp))
            else:
                k=mp.sqrt(-2*e);z=2*k*radius;a=l+1-1/k;b=2*l+2
                # Whittaker W=e^-z/2 z^(l+1) U(a,b,z), analytic logarithmic derivative.
                L=2*k*(-mp.mpf('.5')+(l+1)/z-a*mp.hyperu(a+1,b+1,z)/mp.hyperu(a,b,z))
                cache[key]=(complex(L),0.,0.,0.,0.)
        out.append(cache[key])
    return np.array(out,dtype=complex)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();b=Path(__file__).resolve().parent;c=b.parent/'continuum/run_physical_radial25'
    E,U,phase=read_ci(b/'inputs/inner_R2_N25_L2_M20.ci');eig,W,radius=read_boundary(c/'fort.21');assert max(abs(E-eig))<1e-11
    H=(U*E)@U.T;B=W@U.T;nq=42;np_=len(E)-nq;Hq=H[-nq:,-nq:];V=H[-nq:,:np_];Hp=H[:np_,:np_];Bp=B[:,:np_]
    assert np.linalg.norm(B[:,-nq:])<1e-10
    eq,Q=np.linalg.eigh(Hq);assert np.max(abs(eq[:4]-np.array([-1.1325883965567167,-.7097342169830818,-.4909996519886428,-.3738042836429807])))<1e-9
    target,ell=channels(c/'fort.10');rows=[];arrays={}
    for incident in [.001,.05,.199]:
        total=target.min()+incident;ref=references(total,target,ell,radius);L=ref[:,0];o=np.where(total>target)[0];closed=np.where(total<target)[0]
        R=(W/(E-total))@W.T;Lc=np.diag(L[closed].real)
        Reff=R[np.ix_(o,o)]+R[np.ix_(o,closed)]@Lc@np.linalg.solve(np.eye(len(closed))-R[np.ix_(closed,closed)]@Lc,R[np.ix_(closed,o)])
        F,G,Fp,Gp=[np.diag(ref[o,j].real) for j in range(1,5)]
        K=np.linalg.solve(G-Reff@Gp,Reff@Fp-F);assert np.max(abs(K-K.T))<1e-9
        S=np.linalg.solve(np.eye(len(o))-1j*K,np.eye(len(o))+1j*K)
        Gp_matrix=np.linalg.inv(total*np.eye(np_)-Hp+Bp.T@(L[:,None]*Bp))
        Sigma=V@Gp_matrix@V.T;Gamma=1j*(Sigma-Sigma.conj().T)
        A=V@Gp_matrix@Bp[o,:].T@np.diag(np.sqrt(2*L[o].imag))
        identity_error=float(np.linalg.norm(Gamma-A@A.conj().T)/max(np.linalg.norm(Gamma),1e-30));assert identity_error<1e-8
        width=Q.T@Gamma@Q;values=np.linalg.eigvalsh(Gamma);assert values.min()>-1e-9
        rows.append(dict(incident_energy=incident,open_channels=o.tolist(),K=K.tolist(),S_real=S.real.tolist(),S_imag=S.imag.tolist(),width_eigenvalues=values.tolist(),bound_basis_diagonal_widths=width.diagonal().real.tolist(),optical_identity_relative_error=identity_error,ground_to_all_width=float(width[0,0].real)))
        key=str(incident);arrays['Sigma_'+key]=Sigma;arrays['entrance_'+key]=A;print('kernel',incident,'identity',identity_error,'width_eigenvalues',values[-4:],flush=True)
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);np.savez_compressed(out.parent/'kernel.npz',H_QQ=Hq,Q_eigenvectors=Q,Q_energies=eq,**arrays)
    out.write_text(json.dumps(dict(rows=rows,n_Q=nq,n_P=np_,radius=radius,physical_DR_rates_derived=False,scope='Fixed-R electronic Feshbach kernel with pure Coulomb outer lead; no nuclear capture rate. Q basis/gauge specific; no comparison of diagonals across geometries without tracking.'),indent=2)+'\n')
if __name__=='__main__':main()
