import argparse,json
from pathlib import Path
import numpy as np
from solver import Medium,run

def continuity():
    m=Medium(4);W,u,p=m.prepare(.2,.15);W,u,p=m.step(W,u,p,.2)
    rho,phi,n,s,z=m.field(W,u);gr=m.grad(phi)
    hW=m.h0(W)+phi[...,None,None]*W
    hW[...,0,:]+=m.d*gr[...,2,None]*W[...,1,:]+m.g*m.div(u)[...,None]*W[...,0,:]
    hW[...,1,:]+=m.d*gr[...,2,None]*W[...,0,:]-m.g*m.div(u)[...,None]*W[...,1,:]
    wd=-1j*hW
    nd=2*np.real(np.sum(W.conj()*wd,axis=(-2,-1)))
    sd=2*np.real(np.sum(wd[...,0,:].conj()*W[...,1,:]+W[...,0,:].conj()*wd[...,1,:],axis=-1))
    pdot=-p/m.M;pdot[...,2]+=m.d*sd
    rhodot=nd-m.div(pdot)
    H=m.h0(np.eye(2*m.N,dtype=complex).reshape(m.shape)).reshape(2*m.N,-1)
    wf=W.reshape(2*m.N,-1);R=wf@wf.conj().T
    outflow=-2*np.imag(H*R.T)
    div_particle=outflow.sum(axis=1).reshape(m.n,m.n,m.n,2).sum(axis=-1)
    continuity_error=float(np.max(abs(rhodot+div_particle+m.div(pdot))))
    eps=1e-6
    finite=(m.field(W+eps*wd,u+eps*p/m.M)[0]-m.field(W-eps*wd,u-eps*p/m.M)[0])/(2*eps)
    derivative_error=float(np.max(abs(finite-rhodot)))
    assert continuity_error<1e-12
    assert derivative_error<1e-8
    return dict(local_charge_continuity_error=continuity_error,charge_derivative_error=derivative_error)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    result=dict(continuity=continuity(),runs=[])
    cases=[(4,.2,.15,.01,6.,-4/3,0.),(6,.2,.15,.01,6.,-4/3,.02),
           (6,.2,0.,.02,6.,-4/3,.02),(4,.2,0.,.02,24.,-4/3,.02),
           (4,.2,.15,.02,24.,-4/3,.02)]
    for c in cases:
        r=run(*c);result['runs'].append(r);print(c,r['max_energy_error'],flush=True)
        assert r['max_charge_error']<1e-8
        assert r['gram_error']<1e-9
    Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
