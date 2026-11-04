"""Import-safe, vectorized constitutive families for the reciprocal energy.

H(g)=a0**2*primitive(g/a0), so H'(g)=g*(nu(g/a0)-1).
No external source data, execution, output writing or global mutation on import.
"""
from dataclasses import dataclass
import math
import numpy as np
from scipy.integrate import quad
from scipy.special import expit


@dataclass(frozen=True)
class Response:
    family: str='simple'
    scale: float=1.
    power: float=1.

    def __post_init__(self):
        if self.family not in ('simple','power','cutoff','rational','newtonian'):
            raise ValueError('Unknown response family')
        if self.scale<=0 or self.power<=0:
            raise ValueError('Positive scale and power required')

    @property
    def name(self):
        if self.family in ('simple','newtonian'): return self.family
        if self.family=='power': return f'power_n{self.power:g}'
        return f'{self.family}_t{self.scale:g}_p{self.power:g}'

    @property
    def metadata(self):
        return dict(name=self.name,family=self.family,scale=self.scale,power=self.power,
                    extra_shape_parameters=0 if self.family in ('simple','newtonian') else (1 if self.family=='power' else 2),
                    a0_changed=False)

    @staticmethod
    def _simple(y):
        root=np.sqrt(.25+1/y)
        return 1/(y*(root+.5)), -.5/(y*y*root)

    def _both(self,y):
        y=np.maximum(np.asarray(y,dtype=float),1e-300)
        if self.family=='newtonian': return np.zeros_like(y),np.zeros_like(y)
        if self.family=='power':
            logy=np.log(y); logx=-self.power*logy
            logs=.5*np.logaddexp(math.log(.25),logx)
            logdelta=logx-np.logaddexp(logs,math.log(.5))
            logb=np.logaddexp(0.,logdelta)
            lognu=logb/self.power
            excess=np.expm1(lognu)
            derivative=-np.exp(lognu-logy+logx-math.log(2.)-logs-logb)
            return excess,derivative
        s,sd=self._simple(y)
        if self.family=='simple': return s,sd
        zlog=self.power*(np.log(y)-math.log(self.scale))
        if self.family=='cutoff':
            z=np.exp(np.clip(zlog,-745.,700.)); w=np.exp(-z)
            a=s*w
            return a,sd*w-self.power*z*a/y
        w=expit(-zlog)
        return s*w,sd*w-self.power*s*w*(1-w)/y

    def excess(self,y): return self._both(y)[0]
    def nu(self,y): return 1+self.excess(y)
    def nud(self,y): return self._both(y)[1]

    def primitive(self,y):
        """Dimensionless H(y)=integral_0^y t*(nu(t)-1)dt; scalar audit helper."""
        y=float(y)
        if y<0: raise ValueError('Primitive requires y>=0')
        if y==0: return 0.
        return quad(lambda u: 0. if u==0 else 2*u**3*float(self.excess(u*u)),
                    0.,math.sqrt(y),epsabs=2e-11,epsrel=2e-11,limit=150)[0]


def candidates():
    out=[Response('simple')]
    out += [Response('power',power=n) for n in [1,1.25,1.5,2,3]]
    out += [Response(family,scale=t,power=p) for family in ['cutoff','rational']
            for t in [1.5,2,3,4,6] for p in [2,4,6]]
    return out


def finite_admissibility(response):
    y=np.geomspace(1e-12,1e12,24001)
    nu=response.nu(y); dn=response.nud(y); slope=nu+y*dn
    return dict(passed=bool(np.all(nu>=1) and np.all(dn<=0) and np.all(slope>0)),
                minimum_total_slope=float(slope.min()),at_y=float(y[slope.argmin()]),
                y_min=1e-12,y_max=1e12,n_y=len(y),
                qualification='Finite sampling of constitutive monotonicity, not a stability theorem')
