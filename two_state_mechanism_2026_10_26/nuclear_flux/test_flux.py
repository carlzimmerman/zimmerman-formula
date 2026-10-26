"""Analytic free-chain and gauge tests; no manufactured chemistry claims."""
import numpy as np
from flux import scattering

def main():
    n=3;N=31;h=.1;mu=50.;t=1/(2*mu*h*h);v=np.array([-.9,-.65,.3]);E=-.6
    vs=np.tile(v,(N,1));links=np.tile(np.eye(n),(N-1,1,1))
    r=scattering(vs,links,E,h,mu);assert list(r['open_indices'])==[0,1]
    theta=np.arccos(1-(E-v[:2])/(2*t));expected=np.exp(2j*N*theta)
    assert np.max(abs(r['S']-np.diag(expected)))<1e-11
    rng=np.random.default_rng(1743);links2=links.copy();signs=rng.choice([-1,1],size=(N,n))
    for j in range(N-1):links2[j]=signs[j,:,None]*links[j]*signs[j+1,None,:]
    q=scattering(vs,links2,E,h,mu);assert np.max(abs(q['S']-r['S']))<1e-11
    # Nontrivial real symmetric interchannel hopping: verify flux and reciprocity.
    links[:,0,1]=.02;links[:,1,0]=.02
    r=scattering(vs,links,E,h,mu);assert r['unitarity']<1e-10 and r['reciprocity']<1e-10
    print('Free discrete phases, closed lead, random electronic signs, flux and reciprocity pass.')
if __name__=='__main__':main()
