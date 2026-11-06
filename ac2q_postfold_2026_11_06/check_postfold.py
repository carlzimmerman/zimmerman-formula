"""PF01: exact jump algebra and bounded FV experiments; not full AC2q evolution."""
import argparse
import json
import math
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import brentq
import sympy as sp


def symbolic_checks():
    a, b, g, j = sp.symbols('a b gamma j', positive=True)
    # Shock rest frame, j=q*u on both sides.
    bern = j**2 / (2*b**2) + g*b - j**2/(2*a**2) - g*a
    mom = j**2/b + g*b**2/2 - j**2/a - g*a**2/2
    jb = 2*g*a**2*b**2/(a+b)
    jm = g*a*b*(a+b)/2
    residual_mom = sp.factor(mom.subs(j**2, jb))
    residual_bern = sp.factor(bern.subs(j**2, jm))
    checks = {
        'bernoulli_jump_root': sp.simplify(bern.subs(j**2, jb)) == 0,
        'momentum_jump_root': sp.simplify(mom.subs(j**2, jm)) == 0,
        'potential_momentum_defect': sp.simplify(residual_mom-g*(b-a)**3/(2*(a+b))) == 0,
        'euler_bernoulli_defect': sp.simplify(residual_bern+g*(b-a)**3/(4*a*b)) == 0,
        'incompatibility': sp.simplify(jm-jb-g*a*b*(a-b)**2/(2*(a+b))) == 0,
    }
    q, v, qx, vx = sp.symbols('q v qx vx', real=True)
    qt = -v*qx-q*vx
    vt = -v*vx-g*qx
    E = q*v**2/2+g*q**2/2
    FE = v*(q*v**2/2+g*q**2)
    checks['smooth_energy'] = sp.expand(sp.diff(E,q)*qt+sp.diff(E,v)*vt+sp.diff(FE,q)*qx+sp.diff(FE,v)*vx)==0
    checks['smooth_momentum'] = sp.expand(v*qt+q*vt+sp.diff(q*v**2+g*q**2/2,q)*qx+sp.diff(q*v**2+g*q**2/2,v)*vx)==0
    return checks, {'j2_potential': str(jb), 'j2_euler': str(jm),
                    'potential_momentum_defect': str(residual_mom),
                    'euler_bernoulli_defect': str(residual_bern)}


def riemann(U, model):
    # q0=gamma=1; colliding states (1,+U),(1,-U).
    if model == 'potential':
        z = (U*U/2+math.sqrt(U**4/4+4*U*U))/2
        r = 1+z
    else:
        r = brentq(lambda r: (r-1)**2*(r+1)/(2*r)-U**2,
                   1+1e-12, 2+2*U+U*U, xtol=1e-14)
    S = U/(r-1)
    # Right shock, left plateau (r,0), right incoming state (1,-U).
    mass_def = -U-S*(1-r)
    vel_def = U*U/2+1-r+S*U
    mom_def = U*U+0.5-r*r/2+S*U
    EL, ER = r*r/2, U*U/2+0.5
    energy_def = -U*(U*U/2+1)-S*(ER-EL)
    return dict(U=U, model=model, density=r, shock_speed=S,
                mass_defect=mass_def, velocity_defect=vel_def,
                momentum_defect=mom_def, energy_defect=energy_def)


def flux(W, model):
    q = W[0]
    if np.min(q) <= 0:
        raise ValueError('Positive-charge experiment left its domain')
    v = W[1] if model == 'potential' else W[1]/q
    if model == 'potential':
        f = np.array([q*v, v*v/2+q])
    else:
        f = np.array([W[1], W[1]*v+q*q/2])
    return f, np.abs(v)+np.sqrt(q)


def rhs(W, dx, model, periodic=True):
    if periodic:
        R = np.roll(W, -1, axis=1)
        f, s = flux(W, model)
        fr, sr = flux(R, model)
        face = (f+fr)/2-np.maximum(s,sr)*(R-W)/2
        return -(face-np.roll(face,1,axis=1))/dx, float(s.max())
    ext = np.pad(W, ((0,0),(1,1)), mode='edge')
    L, R = ext[:,:-1], ext[:,1:]
    f, s = flux(L, model); fr, sr = flux(R, model)
    face = (f+fr)/2-np.maximum(s,sr)*(R-L)/2
    return -(face[:,1:]-face[:,:-1])/dx, float(max(s.max(),sr.max()))


def evolve(W, dx, tmax, model, periodic=True):
    t, steps = 0., 0
    while t < tmax:
        dW, speed = rhs(W, dx, model, periodic)
        dt = min(0.4*dx/speed, tmax-t)
        W = W+dt*dW
        t += dt; steps += 1
    q = W[0]; v = W[1] if model == 'potential' else W[1]/q
    return q, v, steps


def diagnostics(q,v,dx):
    primitive = np.cumsum(q-q.mean())*dx
    primitive -= primitive.mean()
    return dict(charge=float(q.sum()*dx), momentum=float((q*v).sum()*dx),
                energy=float((q*v*v/2+q*q/2).sum()*dx),
                q_min=float(q.min()), q_max=float(q.max())), primitive


def wave(N, model, t):
    dx = 2*np.pi/N; x = (np.arange(N)+.5)*dx
    c = 1+.4*np.sin(x); q0=c*c; v0=2*(c-1)
    initial, _ = diagnostics(q0,v0,dx)
    W = np.array([q0,v0 if model=='potential' else q0*v0])
    q,v,steps = evolve(W,dx,t,model)
    out, primitive = diagnostics(q,v,dx)
    out.update(N=N,model=model,time=t,steps=steps,initial=initial)
    if t < 1/1.2:
        # Monotone characteristic map; vector Newton independently gives exact solution.
        a=x-t
        for _ in range(30):
            a -= (a+(1+1.2*np.sin(a))*t-x)/(1+1.2*np.cos(a)*t)
        residual=np.max(np.abs(a+(1+1.2*np.sin(a))*t-x))
        ce=1+.4*np.sin(a); qe=ce*ce; ve=2*(ce-1)
        out.update(characteristic_residual=float(residual),
                   q_L1_error=float(np.mean(np.abs(q-qe))),
                   v_L1_error=float(np.mean(np.abs(v-ve))))
    return out,q,v,primitive


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True)
    ap.add_argument('--mutate',action='store_true'); args=ap.parse_args()
    checks, algebra=symbolic_checks()
    checks['compression_breaks'] = abs(1/(3*.4)-5/6)<1e-14
    # Affine rarefaction has nonnegative speed slope, unlike compression.
    checks['expanding_control'] = (3*.4>0 and -3*.4<0)
    rs=[riemann(U,m) for U in (.01,.1,1.,10.) for m in ('potential','euler')]
    for r in rs:
        scale=1+r['density']**2+r['U']**2
        key=f"RH_{r['model']}_{r['U']}"
        defect=r['velocity_defect'] if r['model']=='potential' else r['momentum_defect']
        if args.mutate and r['model']=='euler':
            # Plant p=q^2 instead of p=q^2/2 while retaining the independent exact shock.
            defect += (1-r['density']**2)/2
        checks[key]=abs(defect)<1e-10*scale and abs(r['mass_defect'])<1e-10*scale
    rows=[]; comparisons=[]; riemann_runs=[]; snapshots={}
    if not args.mutate:
        for t in (.3,1.5):
            for N in (256,512,1024,2048):
                cur={}
                for m in ('potential','euler'):
                    o,q,v,h=wave(N,m,t); rows.append(o); cur[m]=(q,v,h)
                    snapshots[f'{m}_{t}_{N}']=q
                    checks[f'charge_{m}_{t}_{N}']=abs(o['charge']-o['initial']['charge'])<1e-10
                comparisons.append(dict(N=N,time=t,
                    q_L1_difference=float(np.mean(np.abs(cur['potential'][0]-cur['euler'][0]))),
                    gravity_primitive_Linf_difference=float(np.max(np.abs(cur['potential'][2]-cur['euler'][2])))))
        for m in ('potential','euler'):
            errors=[r['q_L1_error'] for r in rows if r['model']==m and r['time']==.3]
            checks[f'prebreak_refinement_{m}']=all(b<a for a,b in zip(errors,errors[1:]))
            # Independent discontinuous benchmark: no boundary contamination before t=.3.
            exact=riemann(1,m)
            for N in (256,512,1024,2048):
                dx=4/N; x=-2+(np.arange(N)+.5)*dx
                q0=np.ones(N); v0=np.where(x<0,1.,-1.)
                q,v,steps=evolve(np.array([q0,v0]),dx,.3,m,False)
                qe=np.where(np.abs(x)<exact['shock_speed']*.3,exact['density'],1.)
                riemann_runs.append(dict(model=m,N=N,q_L1_error=float(np.mean(np.abs(q-qe))),
                    central_density=float(q[np.abs(x)<.1].mean()),exact=exact))
            er=[r['q_L1_error'] for r in riemann_runs if r['model']==m]
            checks[f'riemann_refinement_{m}']=all(b<a for a,b in zip(er,er[1:]))
        for o in comparisons:
            N=o['N']; t=o['time']
            if N<2048:
                for m in ('potential','euler'):
                    coarse=snapshots[f'{m}_{t}_{N}']
                    fine=snapshots[f'{m}_{t}_{N*2}'].reshape(N,2).mean(axis=1)
                    o[f'{m}_q_successive_L1']=float(np.mean(np.abs(coarse-fine)))
    result=dict(checks=checks,all_pass=all(checks.values()),mutate=args.mutate,
        algebra=algebra,riemann_exact=rs,simple_wave=rows,comparisons=comparisons,
        riemann_numerical=riemann_runs,
        scope='Positive-charge, source-free leading planar PN principal system only',
        libraries=dict(numpy=np.__version__,scipy=scipy.__version__,sympy=sp.__version__))
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'all_pass':result['all_pass'],'checks':checks,
                      'comparisons':comparisons,'riemann_U1':[r for r in rs if r['U']==1]},indent=2))
    raise SystemExit(0 if result['all_pass'] else 1)


if __name__=='__main__':
    main()
