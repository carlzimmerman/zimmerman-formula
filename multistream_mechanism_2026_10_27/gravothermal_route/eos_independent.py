"""Independent finite-element radial-mode check of root's pressure-confined logotrope.

Equilibrium integrated in (theta,m), not the root's (theta,theta').
Eigenproblem discretized variationally, without shooting in eigenvalue.
"""
import json
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigsh

eps=1e-6
def rhs(x,y): return [y[1]/x**2,x**2/y[0]]
eq=solve_ivp(rhs,[eps,30],[1+eps**2/6-eps**4/120,eps**3/3-eps**5/30],
             method='DOP853',rtol=3e-12,atol=1e-14,dense_output=True,max_step=.035)
def fields(x):
    th,m=eq.sol(x)
    return th,m,m/np.asarray(x)**2
xc=brentq(lambda x: fields(x)[2]-1/np.sqrt(2),3,15,xtol=1e-12)
critical=float(fields(xc)[0])
q,w=np.polynomial.legendre.leggauss(5)
rows=[]
for contrast in [2.,4.,critical,6.]:
    R=brentq(lambda x:fields(x)[0]-contrast,eps,20,xtol=1e-12)
    vals=[]
    for N in [200,400,800]:
        xx=np.linspace(0,R,N+1); S=lil_matrix((N+1,N+1)); M=lil_matrix((N+1,N+1))
        for i,(lo,hi) in enumerate(zip(xx[:-1],xx[1:])):
            h=hi-lo;x=(lo+hi)/2+h*q/2; wg=w*h/2
            th,_,tp=fields(x);phi=np.array([(1-q)/2,(1+q)/2])
            deriv=(hi**5-lo**5)/(5*h*h)*np.array([[1.,-1.],[-1.,1.]])
            vv=np.einsum('q,iq,jq->ij',wg*(-4*x**3*tp/th),phi,phi)
            mm=np.einsum('q,iq,jq->ij',wg*x**4/th,phi,phi)
            for a in range(2):
                for b in range(2):
                    S[i+a,i+b]+=deriv[a,b]+vv[a,b];M[i+a,i+b]+=mm[a,b]
        # Moving pressure boundary: eta'(R)=-3 eta(R)/R.
        # Integration by parts adds +3 R^3 eta(R)^2 to the quadratic form.
        S[-1,-1]+=3*R**3
        ev,vec=eigsh(S.tocsr(),M=M.tocsr(),k=3,sigma=-.5,which='LM',tol=1e-11)
        order=np.argsort(ev);ev=ev[order];v=vec[:,order[0]]
        significant=v[np.abs(v)>1e-8*np.max(np.abs(v))]
        nodes=int(np.sum(significant[:-1]*significant[1:]<0))
        vals.append(dict(N=N,eigenvalues=ev.tolist(),fundamental_nodes=nodes))
    # Independently evaluate fixed-surface-density mass turning condition.
    dx=1e-4
    def mass(x):th,m,_=fields(x);return float(m/th**2)
    derivative=(mass(R+dx)-mass(R-dx))/(2*dx)
    rows.append(dict(contrast=contrast,edge=R,refinements=vals,
                     fixed_external_pressure_mass_derivative=derivative))
assert abs(rows[1]['refinements'][-1]['eigenvalues'][0]-.0903960231974605)<1e-5
assert rows[1]['refinements'][-1]['fundamental_nodes']==0
assert rows[-1]['refinements'][-1]['eigenvalues'][0]<0
assert abs(rows[2]['refinements'][-1]['eigenvalues'][0])<1e-5
out=dict(status='completed',critical_contrast=critical,rows=rows,
         verdict='Root equation and moving-pressure Robin boundary verified independently; conditional radial stability at contrast four, instability above maximum mass.',
         non_claims=['No open/enclosing halo stability','No independent microscopic derivation of barotropic EOS','Does not select pressure boundary or central density'])
Path(sys.argv[1]).write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
