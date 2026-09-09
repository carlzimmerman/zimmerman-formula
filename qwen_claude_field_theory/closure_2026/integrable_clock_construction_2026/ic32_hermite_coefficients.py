"""An endpoint-defined C2 coefficient approximation, not expanded-float PPoly.

The mathematical definition uses one common value/first/second jet per knot.
No reference background or physical source is used to refit these node data.
"""
import copy
from functools import lru_cache
import mpmath as mp
import numpy as np
import sympy as s
from scipy.optimize import brentq


@lru_cache(None)
def basis():
    x=s.Symbol('x',real=True)
    h01=10*x**3-15*x**4+6*x**5
    h11=-4*x**3+7*x**4-3*x**5
    h21=(x**3-2*x**4+x**5)/2
    return x,(h01,h11,h21)


def identities():
    x,hs=basis(); h=s.Symbol('h',positive=True)
    a,b,c,d,e,f=s.symbols('a b c d e f',real=True)
    R=(d-a-h*b-h*h*c/2,h*(e-b)-h*h*c,h*h*(f-c))
    P=a+h*b*x+h*h*c*x*x/2+sum(v*H for v,H in zip(R,hs))
    return {'endpoint_%d_%d'%(end,order):s.simplify(s.diff(P,x,order).subs(x,end)/h**order-want)
            for end,targets in ((0,(a,b,c)),(1,(d,e,f))) for order,want in enumerate(targets)}


class HermiteTable:
    def __init__(self,table):
        self.x=table.x.copy()
        if len(self.x)<2 or np.any(np.diff(self.x)<=0):
            raise ValueError('Strictly increasing fixed coefficient knots required')
        jets=np.array([table.c[-1],table.c[-2],2*table.c[-3]]).T
        with mp.workdps(80):
            coeff=[mp.mpf(v) for v in table.c[:,-1]]
            dx=mp.mpf(table.x[-1])-mp.mpf(table.x[-2]); final=[]
            for _ in range(3):
                final.append(float(mp.polyval(coeff,dx)))
                degree=len(coeff)-1
                coeff=[v*(degree-i) for i,v in enumerate(coeff[:-1])]
        self.jets=np.vstack((jets,final))
        xx,hs=basis()
        self.functions=[[s.lambdify(xx,s.diff(H,xx,order),'numpy') for H in hs] for order in range(3)]

    def __call__(self,S,nu=0):
        if nu not in (0,1,2):raise ValueError('Only the defined first three jets are exposed')
        S=np.asarray(S)
        if not np.all(np.isfinite(S)) or np.min(S)<self.x[0] or np.max(S)>self.x[-1]:
            raise ValueError('Outside fixed Hermite coefficient domain')
        i=np.clip(np.searchsorted(self.x,S,side='right')-1,0,len(self.x)-2)
        h=self.x[i+1]-self.x[i]; x=(S-self.x[i])/h
        a,b,c=self.jets[i].T; d,e,f=self.jets[i+1].T
        R=(d-a-h*b-h*h*c/2,h*(e-b)-h*h*c,h*h*(f-c))
        base=(a+h*b*x+h*h*c*x*x/2) if nu==0 else (b+h*c*x) if nu==1 else c
        return base+sum(v*fn(x)/h**nu for v,fn in zip(R,self.functions[nu]))


def repair(model):
    repaired=copy.copy(model)
    repaired.table=HermiteTable(model.table)
    repaired.Sbar=brentq(lambda S:float(repaired.evaluate(2.,S,0.,0.,0.)['C']),
                         model.Sref-1e-6,model.Sref+1e-6,xtol=1e-15)
    return repaired


if __name__=='__main__':
    checks=identities()
    print({k:str(v) for k,v in checks.items()})
    raise SystemExit(0 if all(x==0 for x in checks.values()) else 1)
