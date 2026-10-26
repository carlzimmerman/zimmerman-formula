"""Finite-rate API. No physical S matrix or guessed rate is supplied here."""
import numpy as np

def thermal_loss(T,energy,probability,mu=201/202,weight=1.):
    """One incoming symmetry block, sigma=weight*pi*P/(2*mu*E).

    Return its resolved Maxwell rate and a unitarity upper bound on the omitted
    energy tails. Does not bound omitted angular momenta or interpolation error.
    Rates in a_D^3/t_D. Statistical/partial-wave weights must be supplied from
    the actual channel definition, not fitted to populations.
    """
    E=np.asarray(energy,dtype=float);P=np.asarray(probability,dtype=float)
    if (not np.isfinite(T) or T<=0 or not np.isfinite(mu) or mu<=0 or
        not np.isfinite(weight) or weight<0 or E.ndim!=1 or len(E)<2 or
        P.shape!=E.shape or not np.all(np.isfinite(E)) or
        not np.all(np.isfinite(P)) or E[0]<0 or np.any(np.diff(E)<=0) or
        np.any(P<0) or np.any(P>1)):
        raise ValueError('Invalid temperature, channel weight, energy grid or loss probability')
    pref=weight*np.sqrt(2*np.pi)/mu**1.5/T**1.5
    rate=pref*np.trapz(P*np.exp(-E/T),E)
    tail=pref*T*(-np.expm1(-E[0]/T)+np.exp(-E[-1]/T))
    return float(rate),float(tail)

def collision_source(y,T,n,age,D,deg,k):
    """T_b+C <-> A+A. y=[a,t_b,K]; reverse event convention i*n_A^2.

    Leading BO thermochemical convention retained from recycling, mu_A=1.
    Identical final atoms' factors belong in the cross-section event definition;
    no additional 1/2 is silently inserted here. k is per occupied initial level,
    already averaged over its magnetic/spin ensemble.
    """
    D=np.asarray(D);deg=np.asarray(deg);k=np.asarray(k)
    if T<=0 or np.any(~np.isfinite(k)) or np.any(k<0) or k.shape!=D.shape:
        raise ValueError('Require positive temperature and finite nonnegative per-level rates')
    a=y[0];t=np.asarray(y[1:-1]);c=1-a-sum(t)
    inverse_ratio=deg/(100*101/201)**1.5*np.exp(-(.5-D)/T)
    events=age*n*k*(t*c-inverse_ratio*a*a)
    return np.r_[2*sum(events),-events,np.dot(.5-D,events)]

def couple(rad,alpha,mass,Mb,b,rates,closed=False):
    """Add finite DR to existing photons; rates(T) must provide physical k_b.

    There is intentionally no default rate callback. Numerical matter-block
    Jacobian for the collision term; photons retain their analytic Jacobian.
    """
    from scipy.sparse import csc_matrix
    base,env=rad.system(alpha,mass,Mb,b,closed);n,Ti,L,age=env
    def source(y):
        x=1-y[0]-2*sum(y[1:rad.nb+1]);T=y[rad.nm-1]/(1.5*(1+x))
        return collision_source(y[:rad.nm],T,n,age,rad.D,rad.deg[1:],rates(T))
    def evaluate(y,jac=False):
        if not jac:
            out=base(y);out[:rad.nm]+=source(y);return out
        block=np.zeros((len(y),len(y)))
        for j in range(rad.nm):
            delta=1e-6*max(abs(y[j]),1e-8)
            yp=y.copy();ym=y.copy();yp[j]+=delta;ym[j]-=delta
            block[:rad.nm,j]=(source(yp)-source(ym))/(2*delta)
        return base(y,True)+csc_matrix(block)
    return evaluate,env
