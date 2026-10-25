import numpy as np
from scipy.integrate import solve_ivp
from field import energy_density


def rar_limit(x,epsilon,delta=.05):
    """Maximum enclosed N_C/N_T for cold spherical positive equilibrium, no F."""
    t=10**delta
    # Stable Amax-1; avoids cancellation at small x or zero tolerance.
    excess=x*(t-1)*(x+1+1/t)/(1+x)
    return excess/(1+epsilon+excess)


def equilibrium(x,epsilon,r):
    """g/a0 given x=g0/a0 and enclosed countercharge fraction r<1."""
    y=x*x/(1+x);A=(1+epsilon*r)/(1-r)
    b=y+A-1
    return .5*(b+np.sqrt(b*b+4*y))


def oscillation(amplitude,epsilon,duration=30.,rtol=1e-9):
    """Neutral homogeneous two-carrier mode; t unit sqrt(m/(n*q²))."""
    omega2=1+1/epsilon
    def rhs(t,y):
        d,p=y
        if abs(d)>=1:raise ValueError('saturation crossed')
        return [p,-omega2*d/(1-abs(d))]
    sol=solve_ivp(rhs,(0,duration),[amplitude,0.],method='DOP853',rtol=rtol,atol=rtol*1e-2,
                  t_eval=np.linspace(0,duration,3001),max_step=.1/np.sqrt(omega2))
    if not sol.success:raise RuntimeError(sol.message)
    d,p=sol.y;H=p*p/(2*omega2)+energy_density(d);H0=float(energy_density(amplitude))
    crossings=int(np.sum(d[1:]*d[:-1]<0))
    return dict(amplitude=amplitude,epsilon=epsilon,duration=duration,
                relative_energy_error=float(np.max(np.abs(H-H0))/H0),zero_crossings=crossings,
                min_displacement=float(np.min(d)),max_displacement=float(np.max(d)),
                max_current=float(np.max(np.abs(p))),evaluations=sol.nfev,
                final=[float(d[-1]),float(p[-1])])
