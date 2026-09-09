"""Differentiate V2's weighted spatial inverse/projector functional.

Finite 3D periodic cochain realization; exact matrix differentiation, checked
against action differences. This validates operator calculus, not a continuum
metric solution or the full nonlinear gravitational constraint algebra.
"""
import json
import numpy as np
from scipy.linalg import eigh
from functools import lru_cache


def complex_matrices(n):
    m=n**3
    def index(x): return np.ravel_multi_index(tuple(np.asarray(x)%n),(n,n,n))
    D=np.zeros((3*m,m))
    curl=np.zeros((3*m,3*m))
    edge_average=np.zeros((3*m,m))
    face_average=np.zeros((3*m,m))
    pairs=[(0,1),(0,2),(1,2)]
    for x in np.ndindex(n,n,n):
        p=index(x)
        for i in range(3):
            step=np.eye(3,dtype=int)[i]
            p1=index(np.asarray(x)+step)
            D[i*m+p,p]-=1;D[i*m+p,p1]+=1
            edge_average[i*m+p,p]+=.5;edge_average[i*m+p,p1]+=.5
        for f,(i,j) in enumerate(pairs):
            ei,ej=np.eye(3,dtype=int)[i],np.eye(3,dtype=int)[j]
            pi,pj=index(np.asarray(x)+ei),index(np.asarray(x)+ej)
            curl[f*m+p,j*m+pi]+=1;curl[f*m+p,j*m+p]-=1
            curl[f*m+p,i*m+pj]-=1;curl[f*m+p,i*m+p]+=1
            for off in (0*ei,ei,ej,ei+ej):
                face_average[f*m+p,index(np.asarray(x)+off)]+=.25
    assert np.max(abs(curl@D))==0
    return D,curl,edge_average,face_average


def inverse_derivative(H,dH):
    """Symmetric constant-rank pseudoinverse, retaining moving kernel."""
    lam,Q=eigh((H+H.T)/2)
    positive=lam>max(1.,lam.max())*1e-10
    if np.min(lam)<-1e-9: raise ValueError('negative spatial Hodge eigenvalue')
    B=(Q[:,positive]/lam[positive])@Q[:,positive].T
    P=Q[:,~positive]@Q[:,~positive].T
    dB=-B@dH@B+B@B@dH@P+P@dH@B@B
    assert np.max(abs(P@dH@P))<1e-9
    return B,dB,int(np.sum(~positive))


def physical_inverse(H,dH,w,dw):
    root=np.sqrt(w);dr=dw/(2*root)
    inv=1/root;di=-dr/root**2
    Hs=root[:,None]*H*inv[None,:]
    dHs=(dr[:,None]*H*inv[None,:]+root[:,None]*dH*inv[None,:]
          +root[:,None]*H*di[None,:])
    B,dB,nullity=inverse_derivative(Hs,dHs)
    physical=inv[:,None]*B*root[None,:]
    derivative=(di[:,None]*B*root[None,:]+inv[:,None]*dB*root[None,:]
                 +inv[:,None]*B*dr[None,:])
    return physical,derivative,nullity


@lru_cache(maxsize=None)
def evaluate(n,parameter=0.,omit=None):
    D,curl,E,F=complex_matrices(n)
    m=n**3
    rng=np.random.default_rng(2909+n)
    sigma=.15*rng.normal(size=m)
    dsigma=.12*rng.normal(size=m)
    nu=.1*rng.normal(size=m)
    dnu=.09*rng.normal(size=m)
    trace=rng.normal(size=m)
    dtrace=.07*rng.normal(size=m)
    divK=rng.normal(size=3*m)
    ddivK=.08*rng.normal(size=3*m)
    weights=[np.exp(3*(sigma+parameter*dsigma)),
             np.exp(E@(sigma+parameter*dsigma)),
             np.exp(-F@(sigma+parameter*dsigma))]
    dw=[weights[0]*3*dsigma,weights[1]*(E@dsigma),-weights[2]*(F@dsigma)]
    w0,w1,w2=weights;v0,v1,v2=dw
    adj=(D.T*w1[None,:])/w0[:,None]
    dadj=(D.T*v1[None,:])/w0[:,None]-adj*(v0/w0)[:,None]
    h0=adj@D;dh0=dadj@D
    cadj=(curl.T*w2[None,:])/w1[:,None]
    dcadj=(curl.T*v2[None,:])/w1[:,None]-cadj*(v1/w1)[:,None]
    h1=D@adj+cadj@curl
    dh1=D@dadj+dcadj@curl
    B0,dB0,z0=physical_inverse(h0,dh0,w0,v0)
    B1,dB1,z1=physical_inverse(h1,dh1,w1,v1)
    if omit=='inverse':dB0*=0;dB1*=0
    mean=np.ones((m,1))@(w0/w0.sum())[None,:]
    dmean=np.ones((m,1))@((v0*w0.sum()-w0*v0.sum())/w0.sum()**2)[None,:]
    PT=np.eye(3*m)-D@B0@adj
    dPT=-D@(dB0@adj+B0@dadj)
    if omit=='projector':dmean*=0;dPT*=0
    tr=trace+parameter*dtrace
    r=divK+parameter*ddivK
    V=PT@r;dV=dPT@r+PT@ddivK
    W=B0@adj@r
    dW=dB0@adj@r+B0@dadj@r+B0@adj@ddivK
    U=(np.eye(m)-mean)@tr-W
    dU=(np.eye(m)-mean)@dtrace-dmean@tr-dW
    N0=np.exp(nu+parameter*dnu);N1=np.exp(E@(nu+parameter*dnu))
    q0=w0*N0;q1=w1*N1
    dq0=v0*N0+q0*dnu;dq1=v1*N1+q1*(E@dnu)
    # V2 coefficients, as derived in source_response_v2.py.
    C=5/3
    etaV,etaU,etaX=C-2,(2-C)/4,2-C
    BV=B1@V
    value=etaV*np.dot(q1*V,BV)+np.dot(q0,etaU*U*U+etaX*U*W)
    derivative=(etaV*(np.dot(dq1*V,BV)+np.dot(q1*dV,BV)
                         +np.dot(q1*V,dB1@V+B1@dV))
                +np.dot(dq0,etaU*U*U+etaX*U*W)
                +np.dot(q0,2*etaU*U*dU+etaX*(dU*W+U*dW)))
    residuals=dict(projector_idempotence=float(np.max(abs(PT@PT-PT))),
                   projected_divergence=float(np.max(abs(adj@PT))),
                   mean_removed=float(abs(np.dot(w0,U))),
                   scalar_kernel_dimension=z0,oneform_kernel_dimension=z1)
    assert residuals['projector_idempotence']<1e-9
    assert residuals['projected_divergence']<1e-9
    assert residuals['mean_removed']<1e-9
    return value,float(derivative),residuals


def audit():
    rows=[]
    for n in (3,4):
        value,derivative,residuals=evaluate(n)
        controls=[]
        for h in (1e-3,3e-4,1e-4):
            finite=(evaluate(n,h)[0]-evaluate(n,-h)[0])/(2*h)
            controls.append(dict(step=h,finite_difference=finite,
                                 absolute_error=abs(finite-derivative)))
        assert controls[-1]['absolute_error']<2e-7
        badinv=abs(evaluate(n,omit='inverse')[1]-derivative)
        badprojector=abs(evaluate(n,omit='projector')[1]-derivative)
        assert badinv>1e-4 and badprojector>1e-4
        rows.append(dict(grid=n,value=value,analytic_derivative=derivative,
                         finite_differences=controls,omitted_inverse_error=badinv,
                         omitted_projector_error=badprojector,checks=residuals))
    return dict(status='FINITE_OPERATOR_VARIATION_VERIFIED',rows=rows,
                scope='weighted finite periodic cochains, not continuum metric equations',
                seed='2909+n',unknowns=['full embedding of varying Kij and h in spacetime',
                'continuum convergence','nonlinear gravitational Dirac algebra'])


if __name__=='__main__':
    print(json.dumps(audit(),indent=2))
