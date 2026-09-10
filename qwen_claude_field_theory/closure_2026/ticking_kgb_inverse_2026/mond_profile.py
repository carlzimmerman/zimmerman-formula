#!/usr/bin/env python3
"""50-digit inverse reconstruction for the preferred exponential MOND profile.

Units a0=m=|q_clock|=1; epsilon=sqrt(G M a0)/c^2 controls compactness.
The exact relativistic embedding uses B=(1-2ra)^-1, (log A)'=2aB.
Its weak-field circular acceleration is the prescribed a=y, not an asserted
all-orders identity between coordinate acceleration and an observable.
This builds a separate parametric G(X) per profile; universality is tested,
not inferred. No empirical dataset is used in this mathematical construction.
"""
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import mpmath as mp
import sympy as s

spec=importlib.util.spec_from_file_location('kgb_model',Path(__file__).with_name('kgb_inverse.py'))
model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)


@lru_cache(None)
def principal_evaluator():
    a=model.principal_template()
    args=[a['m'],a['G1'],a['G2']]+list(a['v'])+[a['H'][i,j] for i in range(4) for j in range(i,4)]
    return s.lambdify(args,a['M'].subs({a['P']:0,a['P1']:0,a['P2']:0}),'mpmath',cse=True)


def sample(epsilon,y):
    with mp.workdps(50):
        eps=mp.mpf(epsilon);y=mp.mpf(y)
        mu=-mp.expm1(-y);lam=mu+y*mp.exp(-y);lamp=(2-y)*mp.exp(-y)
        r=eps/mp.sqrt(y*mu)
        ay=-2*y*mu/(r*lam)
        ayy=(6*y*mu/(r*r)-lamp*ay*ay)/lam
        compact=r*y;cp=y+r*ay;cpp=2*ay+r*ayy
        if not (0<compact<mp.mpf('0.5')):raise ValueError('outside regular exterior branch')
        B=1/(1-2*compact);W=compact*B
        Wp=cp*B*B;Wpp=cpp*B*B+4*cp*cp*B**3
        g=y*B;gp=ay*B+2*y*cp*B*B
        X=1/(2+W)  # Local field normalization; global A restored below.
        LX=-2*g-Wp/(2+W)
        LXp=-2*gp-Wpp/(2+W)+Wp*Wp/(2+W)**2
        p=mp.sqrt(B*W*X);bp=2*cp*B
        LP=(bp+Wp/W+LX)/2
        rho=4*y*y*mp.exp(-y)/(r*lam)
        Lrho=2*ay/y-ay-1/r-lamp*ay/lam
        GX=rho*p/(2*X*X*LX)
        GXX=GX*(Lrho+LP-2*LX-LXp/LX)/(X*LX)
        H=mp.matrix([[-g*p/B,g/mp.sqrt(B),0,0],[g/mp.sqrt(B),p*(LP-bp/2)/B,0,0],
                     [0,0,p/(B*r),0],[0,0,0,p/(B*r)]])
        v=mp.matrix([-1,p/mp.sqrt(B),0,0]);eta=mp.diag([-1,1,1,1])
        dX=-H*eta*v;box=sum(eta[i,i]*H[i,i] for i in range(4));vdX=(v.T*eta*dX)[0]
        T=-GX*box*v*v.T-GX*(dX*v.T+v*dX.T)+eta*GX*vdX
        residual=max(abs(T[0,0]-rho),abs(T[1,1]),abs(T[2,2]-rho*W/2),abs(T[0,1]))/rho
        args=[mp.mpf(1),GX,GXX]+list(v)+[H[i,j] for i in range(4) for j in range(i,4)]
        M=principal_evaluator()(*args)
        kinetic=M[0,0];disc=M[0,1]**2-M[0,0]*M[1,1]
        healthy=bool(kinetic>0 and disc>0 and M[2,2]<0)
        speeds=[]
        if healthy:
            for i in range(361):
                c=mp.mpf(i)/180-1
                rad=(M[0,1]*c)**2-kinetic*(M[1,1]*c*c+M[2,2]*(1-c*c))
                speeds.extend([abs((M[0,1]*c+mp.sqrt(rad))/kinetic),
                               abs((M[0,1]*c-mp.sqrt(rad))/kinetic)])
        return dict(epsilon=eps,y=y,r=r,mu=mu,lambda_parallel=lam,rho=rho,
                    X_local=X,X_log_derivative=LX,GX_local=GX,GXX_local=GXX,
                    max_relative_field_residual=residual,principal_matrix=M,
                    healthy_local_principal=healthy,
                    max_sampled_characteristic_speed=max(speeds) if speeds else None)


def global_curve(epsilon,y):
    """Same clock normalization, A=1 at y=0.02, separately for each profile."""
    with mp.workdps(50):
        eps=mp.mpf(epsilon);y=mp.mpf(y)
        def integrand(a):
            mu=-mp.expm1(-a);lam=mu+a*mp.exp(-a)
            r=eps/mp.sqrt(a*mu)
            return -r*lam/(mu*(1-2*r*a))
        A=mp.exp(mp.quad(integrand,[mp.mpf('0.02'),y]))
        mu=-mp.expm1(-y);lam=mu+y*mp.exp(-y);r=eps/mp.sqrt(y*mu)
        compact=r*y;B=1/(1-2*compact);W=compact*B
        yp=-2*y*mu/(r*lam);Wp=(y+r*yp)*B*B
        X=1/(A*(2+W));LX=-2*y*B-Wp/(2+W)
        p=mp.sqrt(B*W*X);rho=4*y*y*mp.exp(-y)/(r*lam)
        return X,rho*p/(2*X*X*LX)


def universality_probe():
    with mp.workdps(50):
        epsilons=['0.000001','0.000002'];lo=mp.mpf('0.02');hi=mp.mpf('20')
        intervals=[(global_curve(e,lo)[0],global_curve(e,hi)[0]) for e in epsilons]
        lower=max(x[0] for x in intervals);upper=min(x[1] for x in intervals)
        if not lower<upper:return dict(status='no overlap for this boundary choice')
        target=(lower+upper)/2;rows=[]
        for eps in epsilons:
            a,b=lo,hi
            for _ in range(140):
                mid=(a+b)/2
                if global_curve(eps,mid)[0]<target:a=mid
                else:b=mid
            y=(a+b)/2;X,GX=global_curve(eps,y)
            rows.append(dict(epsilon=eps,y=y,X=X,GX=GX,X_residual=abs(X-target)))
        return dict(boundary='q_clock=-1, A(y=0.02)=1 for each mass',target_X=target,
                    rows=rows,GX_ratio=rows[1]['GX']/rows[0]['GX'],
                    scope='Only the zero-radial-pressure embedding and these boundary choices, not all KGB theories')


def serial(a):
    if isinstance(a,dict):return {k:serial(v) for k,v in a.items()}
    if isinstance(a,(list,tuple)):return [serial(v) for v in a]
    if isinstance(a,(bool,type(None),str)):return a
    if isinstance(a,mp.matrix):return [[mp.nstr(x,30) for x in row] for row in a.tolist()]
    return mp.nstr(a,30)


def main():
    rows=[sample(eps,y) for eps in ('0.000001','0.000002') for y in ('0.02','0.1','0.5','1','2','5','10','20')]
    result=dict(samples=rows,universality=universality_probe(),status='OPEN; no empirical or full-theory certificate')
    print(json.dumps(serial(result),indent=2))
    return 0 if all(float(r['max_relative_field_residual'])<1e-35 for r in rows) else 1


if __name__=='__main__':raise SystemExit(main())
