"""Exact flat planar on-branch corner obstruction; no global AC2q no-go claim."""
import argparse
import json
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.integrate import quad


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True)
    ap.add_argument('--mutate',action='store_true'); args=ap.parse_args()
    v,d,g,s2,A,eps=sp.symbols('v d gamma s2 A epsilon',positive=True)
    y=sp.sqrt(1-v*v); C=1/y; B=s2*y*y
    z=C*d
    # After P*A = P*(cosh theta)' -> -P'*cosh theta.
    L=-z+B/2-g*((z+B)**2-B**2)/2
    k=sp.diff(L,d)
    ds=sp.solve(sp.Eq(k,-A),d)[0]
    f=sp.simplify((L+A*d).subs(d,ds))
    fe=((A*y-1-eps*y*y)**2+eps*y*y)/(2*g)
    f3=sp.diff(fe,v,3)
    target=3*v/g*(4*eps**2+A/y**5*(1-eps*(3-2*v*v)*(1-v*v)))
    checks={
        'P_conjugate':sp.simplify(k+C*(1+g*(z+B)))==0,
        'routhian':sp.simplify(f.subs(s2,eps/g)-fe)==0,
        'third_derivative':sp.simplify(f3-target)==0,
        'spatial_stress_reduction':sp.simplify((v*sp.diff(L,v)+d*k-L).subs(d,ds)-(v*sp.diff(f,v)-f))==0,
        'current_envelope':sp.simplify(sp.diff(f,v)-sp.diff(L,v).subs(d,ds))==0,
    }
    # Direct rapidity/tetrad calculation, flat metric, stationary derivatives.
    th,thx,PP,Px=sp.symbols('theta theta_x P P_x',real=True)
    n=sp.Matrix([sp.cosh(th),sp.sinh(th)])
    e=sp.Matrix([sp.sinh(th),sp.cosh(th)])
    metric=sp.diag(-1,1)
    accel=n[1]*n.diff(th)*thx
    pa=sp.simplify(((PP*e).T*metric*accel)[0])
    # h^{mu nu}=e^mu e^nu; stationary: only mu=x derivative.
    Pcov=metric*(PP*e)
    dPcov=Pcov.diff(PP)*Px+Pcov.diff(th)*thx
    div=sp.simplify(e[1]*(e.T*dPcov)[0])
    checks['acceleration_identity']=sp.simplify(pa-PP*sp.sinh(th)*thx)==0
    checks['projected_divergence']=sp.simplify(div-sp.cosh(th)*Px)==0
    # 0<= (3-2v^2)(1-v^2) <=3 on 0<v<1, so f''' >0 for eps<1/3.
    w=sp.symbols('w',real=True)
    checks['convexity_bound_identity']=sp.expand(3-(3-2*w)*(1-w)-w*(5-2*w))==0
    fp=sp.lambdify((v,A,eps),sp.diff(fe*g,v),'numpy')
    fpp=sp.lambdify((v,A,eps),sp.diff(fe*g,v,2),'numpy')
    ff=sp.lambdify((v,A,eps),fe*g,'numpy')
    rows=[]
    for ev in (0.,1e-17,.01,.1,.3):
        for av in (1.01,1.2,2.):
            vmax=np.sqrt(1-av**-2)*(1-1e-10)
            if fpp(0,av,ev)*fpp(vmax,av,ev)>=0:
                rows.append(dict(epsilon=ev,A=av,status='no two-branch minimum in positive-charge domain'))
                continue
            vm=brentq(lambda z:fpp(z,av,ev),0,vmax)
            jm=fp(vm,av,ev); je=min(fp(0,av,ev),fp(vmax,av,ev))
            j=(jm+je)/2
            vl=brentq(lambda z:fp(z,av,ev)-j,0,vm,xtol=1e-14)
            vr=brentq(lambda z:fp(z,av,ev)-j,vm,vmax,xtol=1e-14)
            defect=(vr*j-ff(vr,av,ev))-(vl*j-ff(vl,av,ev))
            integral=quad(lambda z:j-fp(z,av,ev),vl,vr,epsabs=1e-13,epsrel=1e-12)[0]
            signed=-defect if args.mutate else defect
            key=f'positive_corner_defect_{ev}_{av}'
            checks[key]=bool(signed>0 and abs(defect-integral)<1e-10*max(1,abs(defect)))
            rows.append(dict(epsilon=ev,A=av,status='two roots',v_left=vl,v_right=vr,
                current=j,stress_defect=defect,integral=integral,
                charge_gamma_left=float(av*np.sqrt(1-vl*vl)-1),
                charge_gamma_right=float(av*np.sqrt(1-vr*vr)-1)))
    out=dict(checks=checks,all_pass=all(checks.values()),mutate=args.mutate,
        routhian=str(fe),third_derivative=str(target),fixtures=rows,
        scope='Exact flat stationary planar positive-charge finite interface; continuous fields; no surface defect; 0<=epsilon<1/3; same-sign velocities')
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    raise SystemExit(0 if out['all_pass'] else 1)


if __name__=='__main__':
    main()
