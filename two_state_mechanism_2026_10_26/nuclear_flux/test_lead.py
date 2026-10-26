import numpy as np
from lead import modes, scattering_lead

def main():
    h=.1;t=1/(100*h*h);V=np.array([-.9,-.65,.3]);H=np.diag(V)+2*t*np.eye(3);W=-t*np.eye(3);E=-.6
    r=modes(H,W,E);assert len(r['open'])==2
    k=np.arccos(1-(E-V[:2])/(2*t));assert np.max(abs(np.sort(np.angle(r['lambda'][r['open']]))-np.sort(k)))<1e-10
    # A genuinely coupled stationary lead must give unitary reciprocal reflection.
    O=np.eye(3);O[0,1]=.03;O[1,0]=-.03;O*=.99
    pots=np.tile(V,(25,1));links=np.tile(O,(24,1,1))
    q=scattering_lead(pots,links,E,h,O)
    assert q['unitarity']<1e-9 and q['reciprocity']<1e-9
    # Invariant under moving the cut through an identical stationary lead:
    # individual scattering phases change but probabilities cannot.
    z=scattering_lead(np.tile(V,(37,1)),np.tile(O,(36,1,1)),E,h,O)
    assert np.max(abs(abs(q['S'])**2-abs(z['S'])**2))<1e-9
    print('Generalized lead dispersion, coupled flux, reciprocity and cut invariance pass.')
if __name__=='__main__':main()
