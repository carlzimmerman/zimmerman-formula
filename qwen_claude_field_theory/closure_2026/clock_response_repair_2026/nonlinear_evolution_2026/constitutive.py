#!/usr/bin/env python3
"""Off-trajectory jets of the SAME reconstructed P,W,V, not a new action."""
from functools import lru_cache
import json
import numpy as np
from scipy.integrate import solve_ivp
import sympy as s


@lru_cache(maxsize=1)
def functions():
    a,m,v=s.symbols("a m v",positive=True)
    charge=s.Rational(1,10)/a**3
    q=1/(1+m);U=m*q*charge;d=charge*U/(2*q*(q*charge+U));ell=q*q*m/2
    H=s.sqrt((s.Rational(7,10)+charge)/3);O=charge/(3*H*H)
    mp=3*m*(O*m+2*O+2*m*v+2*v)/(2*(m+2))
    vp=(v-1)*(9*O*m**3+42*O*m*m+66*O*m+36*O+6*m**3*v-4*m**3
              +18*m*m*v-20*m*m+24*m*v-32*m+12*v-16)/(2*(m+1)*(m+2)**2)
    flow=[a*H,mp*H,vp*H]
    def along(e):return sum(s.diff(e,z)*zd for z,zd in zip((a,m,v),flow))
    fields=[q,U,d,H,ell]
    bg_expr=fields+[along(x) for x in fields]+[along(along(x)) for x in fields]
    bgfunc=s.lambdify((a,m,v),bg_expr,"numpy",cse=True)
    flowfunc=s.lambdify((a,m,v),flow,"numpy",cse=True)
    base=s.symbols("qb U d Hb ell",positive=True)
    first=s.symbols("qb1 U1 d1 Hb1 ell1",real=True)
    second=s.symbols("qb2 U2 d2 Hb2 ell2",real=True)
    X,Y,g=s.symbols("X Y gamma",real=True)
    qb,U,d,Hb,ell=base
    P=-U*s.log((U-2*d*X)/(U-2*d*qb*qb))/2+3*g*qb*Hb*(X-qb*qb)
    W=U+2*d*ell*(s.sqrt(1+Y/ell)-1)-2*g*qb*qb*first[0]
    def partial_t(e):
        return sum(s.diff(e,z)*zd for z,zd in zip(base+first,first+second))
    Pt=partial_t(P)
    expressions=dict(P=P,P_X=s.diff(P,X),P_XX=s.diff(P,X,2),P_t=Pt,
                     P_Xt=s.diff(Pt,X),P_tt=partial_t(Pt),V=U,V_t=first[1],V_tt=second[1],
                     W=W,W_Y=s.diff(W,Y),W_YY=s.diff(W,Y,2),W_YYY=s.diff(W,Y,3),
                     W_t=partial_t(W),W_Yt=partial_t(s.diff(W,Y)),W_YYt=partial_t(s.diff(W,Y,2)))
    jetfunc=s.lambdify((*base,*first,*second,X,Y,g),list(expressions.values()),"numpy",cse=True)
    return bgfunc,flowfunc,list(expressions),jetfunc


class Model:
    def __init__(self,tmax,gamma=1e-6):
        self.gamma=float(gamma)
        self.tmax=float(tmax)
        self.bgfunc,self.flowfunc,self.names,self.jetfunc=functions()
        self.solution=solve_ivp(lambda t,y:self.flowfunc(*y),(0.,max(tmax,1e-8)),[1.,.1,.5],
                                method="DOP853",rtol=2e-13,atol=2e-15,dense_output=True)
        if not self.solution.success:raise RuntimeError(self.solution.message)

    @lru_cache(maxsize=128)
    def background(self,t):
        if t < -1e-14 or t > self.tmax+1e-12:
            raise ValueError("outside the integrated background interval")
        state=self.solution.sol(t)
        raw=np.asarray(self.bgfunc(*state),dtype=float)
        return dict(a=state[0],m=state[1],v=state[2],q=raw[0],U=raw[1],d=raw[2],H=raw[3],
                    ell=raw[4],qdot=raw[5],Hdot=raw[8],raw=raw)

    def jets(self,t,X,Y):
        b=self.background(t);raw=b["raw"]
        denominator=b["U"]-2*b["d"]*np.asarray(X)
        if (np.any(denominator<=0) or b["U"]-2*b["d"]*b["q"]**2<=0
                or np.any(1+np.asarray(Y)/b["ell"]<=0)):
            raise ValueError("constitutive domain boundary reached")
        result=dict(zip(self.names,self.jetfunc(*raw,X,Y,self.gamma)))
        result.update(M2=1.,Lambda=.7,gamma=self.gamma,domain_denominator=denominator)
        return result


if __name__=="__main__":
    model=Model(.1)
    rows=[]
    for t in (0.,.05,.1):
        b=model.background(t);j=model.jets(t,.98*b["q"]**2,.003)
        rows.append(dict(t=t,a=b["a"],q=b["q"],P=float(j["P"]),Ptt=float(j["P_tt"])))
    print(json.dumps({"scope":"off-branch coefficient evaluation only","rows":rows},indent=2))
