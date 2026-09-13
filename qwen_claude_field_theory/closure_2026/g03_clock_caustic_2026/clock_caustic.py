#!/usr/bin/env python3
"""Exact C-H geodesic-clock branch: finite foliation singularity, theory OPEN.

No numerical evolution after crossing, no guessed physical mode count,
and no identification of clock caustics with a metric curvature singularity.
"""
import argparse
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import time

import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as sp

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


@lru_cache(None)
def symbolic_geometry():
    A,H=sp.symbols('A H',positive=True)
    P,Px=sp.symbols('P P_x',real=True)
    gamma=sp.sqrt(1+P*P/A**2)
    Pt=-P*Px/(A*A*gamma)
    def derivative(f,i):
        return A*H*sp.diff(f,A)+Pt*sp.diff(f,P) if i==0 else (Px*sp.diff(f,P) if i==1 else sp.Integer(0))
    g=sp.diag(-1,A*A,A*A,A*A); gi=g.inv()
    ch=[[[sp.simplify(sum(gi[i,l]*(derivative(g[l,j],k)+derivative(g[l,k],j)-derivative(g[j,k],l))
        for l in range(4))/2) for k in range(4)] for j in range(4)] for i in range(4)]
    riem={}
    for i in range(4):
        for j in range(4):
            for k in range(4):
                for l in range(4):
                    riem[i,j,k,l]=sp.simplify(derivative(ch[i][l][j],k)-derivative(ch[i][k][j],l)+
                        sum(ch[i][k][m]*ch[m][l][j]-ch[i][l][m]*ch[m][k][j] for m in range(4)))
    ric=sp.Matrix(4,4,lambda j,l:sum(riem[i,j,i,l] for i in range(4)))
    R=sp.simplify(sum(gi[i,j]*ric[i,j] for i in range(4) for j in range(4)))
    R2=sp.simplify(sum(g[i,i]*gi[j,j]*gi[k,k]*gi[l,l]*v*v for (i,j,k,l),v in riem.items()))
    einstein=ric-g*R/2+3*H*H*g
    n=sp.Matrix([gamma,P/A**2,0,0])
    acc=[sp.simplify(sum(n[j]*derivative(n[i],j) for j in range(4))+
          sum(ch[i][j][k]*n[j]*n[k] for j in range(4) for k in range(4))) for i in range(4)]
    K=sp.simplify(sum(derivative(n[i],i)+sum(ch[i][i][j]*n[j] for j in range(4)) for i in range(4)))
    expected=H*(2*gamma+1/gamma)+Px/(A*A*gamma*gamma)
    return dict(spacetime_R=R,spacetime_Riemann_squared=R2,
        Einstein_residuals=[sp.simplify(v) for v in einstein],
        normalization_residual=sp.simplify((n.T*g*n)[0]+1),
        acceleration_residuals=acc,expansion=K,expansion_residual=sp.simplify(K-expected),
        conserved_momentum_transport=Pt,clock_normal=n)


@lru_cache(None)
def kernel_branch_check():
    y=sp.symbols('y',positive=True)
    s=y*(1-sp.exp(-y))
    q=2-2*(1+y)*sp.exp(-y)-y*y*sp.exp(-2*y)
    derivative=sp.factor(sp.diff(q,y)/sp.diff(s,y))
    return dict(q0=sp.limit(q,y,0,dir='+'),
        composite_first_derivative_limit=sp.limit(derivative,y,0,dir='+'),
        constitutive_tangent_limit=sp.limit(derivative/(2*s),y,0,dir='+'))


@lru_cache(None)
def symbolic_characteristics():
    H,E=sp.symbols('H E',positive=True)
    P,Pq,t=sp.symbols('P P_q t',real=True)
    gamma=sp.sqrt(1+P*P*E); gamma0=sp.sqrt(1+P*P)
    D=P*(1-E)/(H*(gamma0+gamma))
    DP=(1-E)/(H*gamma0*gamma*(gamma0+gamma))
    clock=t+sp.log((1+gamma)/(1+gamma0))/H
    Dt=-2*H*E*sp.diff(D,E)
    Ct=sp.diff(clock,t)-2*H*E*sp.diff(clock,E)
    Cq=-P+Pq*sp.diff(clock,P)
    J=1+Pq*DP
    return dict(displacement=D,displacement_P=DP,proper_clock_increment=clock,
        displacement_t_residual=sp.simplify(Dt-P*E/gamma),
        displacement_P_residual=sp.simplify(sp.diff(D,P)-DP),
        clock_t_along_label_residual=sp.simplify(Ct-1/gamma),
        clock_P_residual=sp.simplify(sp.diff(clock,P)+P*DP),
        reconstructed_spatial_clock_residual=sp.simplify(Cq+P*J),
        reconstructed_time_clock_residual=sp.simplify(Ct+P*Dt-gamma))


@lru_cache(None)
def symbolic_focusing():
    H,b,E,delta=sp.symbols('H b E delta',positive=True)
    J=1-b*(1-E)/(2*H)
    K=3*H-b*E/J
    K2=(H-b*E/J)**2+2*H*H
    leaf=sp.factor(6*H*H-K*K+K2)
    root=sp.solve(J,E)[0]
    return dict(center_J=J,center_K=K,center_Kij_squared=K2,center_leaf_R=leaf,
        critical_expansion=sp.simplify(K.subs(b,2*H)),
        caustic_time=-sp.log(root)/(2*H),
        raychaudhuri_residual=sp.factor(-2*H*E*sp.diff(K,E)+K2-3*H*H),
        caustic_pole_residue=sp.limit(sp.simplify(delta*K.subs(E,root*sp.exp(2*H*delta))),delta,0,dir='+'))


def characteristics(t,q,H,p0,k):
    q=np.asarray(q,float); P=-p0*np.sin(k*q); Pq=-p0*k*np.cos(k*q)
    gamma0=np.sqrt(1+P*P)
    E=np.exp(-2*H*t); gamma=np.sqrt(1+P*P*E)
    if H==0:
        D=t*P/gamma0; DP=t/gamma0**3; T=t/gamma0
    else:
        one_minus_E=-np.expm1(-2*H*t)
        D=P*one_minus_E/(H*(gamma0+gamma))
        DP=one_minus_E/(H*gamma0*gamma*(gamma0+gamma))
        T=t+np.log1p(-P*P*one_minus_E/((gamma0+gamma)*(1+gamma0)))/H
    return dict(x=q+D,J=1+Pq*DP,tau=-p0/k*np.cos(k*q)+T,
        P=P,Pq=Pq,gamma=gamma,coordinate_velocity=P*E/gamma,DP=DP)


def caustic_time(H,p0,k):
    if H<0 or p0<=0 or k<=0:
        raise ValueError('H>=0, p0>0, k>0 required')
    b=p0*k
    if H==0: return 1/b
    if b<=2*H: return None
    return float(-np.log1p(-2*H/b)/(2*H))


def geodesic_rhs(H):
    def rhs(t,state):
        x,v,clock,J,Jdot=state
        A2=np.exp(2*H*t)
        return [v,-2*H*v+H*A2*v**3,np.sqrt(1-A2*v*v),
                Jdot,(-2*H+3*H*A2*v*v)*Jdot]
    return rhs


def trajectory_check(q,H,p0,k,t):
    P=-p0*np.sin(k*q); Pq=-p0*k*np.cos(k*q); gamma0=np.sqrt(1+P*P)
    initial=[q,P/gamma0,-p0/k*np.cos(k*q),1,Pq/gamma0**3]
    sol=solve_ivp(geodesic_rhs(H),(0,t),initial,method='DOP853',rtol=2e-12,atol=2e-13)
    exact=characteristics(t,q,H,p0,k)
    target=np.array([exact['x'],exact['coordinate_velocity'],exact['tau'],exact['J']])
    error=np.abs(sol.y[:4,-1]-target)
    return dict(q=q,H=H,p0=p0,k=k,t=t,success=bool(sol.success),
        numerical=sol.y[:4,-1].tolist(),exact=target.tolist(),
        max_absolute_error=float(np.max(error)))


def jacobi_event(H,p0,k):
    # Integrate geodesic and linearized geodesic equations, not the J formula.
    if p0*k<=2*H: return None
    def event(t,state): return state[3]
    event.terminal=True; event.direction=-1
    horizon=2/max(H,1e-8)+2/(p0*k)
    sol=solve_ivp(geodesic_rhs(H),(0,horizon),[0,0,-p0/k,1,-p0*k],
        method='DOP853',rtol=2e-12,atol=2e-13,events=event)
    return float(sol.t_events[0][0]) if len(sol.t_events[0]) else None


def center_invariants(t,H,p0,k):
    E=np.exp(-2*H*t); b=p0*k
    J=1-b*t if H==0 else 1+b*np.expm1(-2*H*t)/(2*H)
    longitudinal=H-b*E/J
    K=longitudinal+2*H; K2=longitudinal**2+2*H*H
    return dict(t=t,J=float(J),K=float(K),Kij_squared=float(K2),
        leaf_R=float(6*H*H-K*K+K2),spacetime_R=12*H*H,
        spacetime_Riemann_squared=24*H**4)


def global_scan(H,p0,k):
    tc=caustic_time(H,p0,k)
    ts=np.array([0,.25,.75,.99])*tc
    qs=np.linspace(0,2*np.pi/k,2049)
    errors=[]; extrema=[]
    for t in ts:
        r=characteristics(t,qs,H,p0,k)
        bound=center_invariants(t,H,p0,k)['J']
        errors.append(abs(float(np.min(r['J']))-bound))
        extrema.append(max(abs(float(np.min(r['tau']))-(t-p0/k)),
                           abs(float(np.max(r['tau']))-(t+p0/k))))
    a=p0/k; lo=a; hi=tc-a
    caps=[lo+(hi-lo)/3,lo+2*(hi-lo)/3]
    bounds=[(s-a,s+a) for s in caps]
    return dict(H=H,p0=p0,k=k,caustic_time=tc,minimum_bound_error=max(errors),
        clock_extrema_error=max(extrema),clock_cap_interval_nonempty=hi>lo,
        clock_caps=caps,cap_cosmic_time_bounds=bounds,
        cap_time_bounds_inside_regular_region=all(0<left<right<tc for left,right in bounds))


def serial(value):
    if isinstance(value,dict): return {str(k):serial(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [serial(v) for v in value]
    if isinstance(value,sp.MatrixBase): return [[str(v) for v in row] for row in value.tolist()]
    if isinstance(value,sp.Basic): return str(value)
    return value


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir',type=Path,default=HERE)
    parser.add_argument('--require-closed',action='store_true')
    args=parser.parse_args(); started=time.time(); checks=[]
    def check(name,ok):
        checks.append(dict(name=name,passed=bool(ok)))
        print(f'[{"PASS" if ok else "FAIL"}] {name}',flush=True)
    geom=symbolic_geometry(); aux=kernel_branch_check(); chars=symbolic_characteristics(); focus=symbolic_focusing()
    check('vacuum de Sitter equation from metric curvature',all(v==0 for v in geom['Einstein_residuals']))
    check('clock normal is unit and geodesic',geom['normalization_residual']==0 and all(v==0 for v in geom['acceleration_residuals']))
    check('zero auxiliary first variation uses continuous composite',aux['q0']==0 and aux['composite_first_derivative_limit']==0 and aux['constitutive_tangent_limit']==sp.oo)
    check('exact clock reconstruction and characteristics',all(v==0 for key,v in chars.items() if key.endswith('_residual')))
    check('invariant expansion and Raychaudhuri equation',geom['expansion_residual']==0 and focus['raychaudhuri_residual']==0 and focus['caustic_pole_residue']==-1)
    trajectories=[trajectory_check(q,1,.2,20,t) for q in (0,.014,.07,.12) for t in (.05,.2)]
    check('independent full geodesic/Jacobi integrations',all(r['success'] and r['max_absolute_error']<2e-9 for r in trajectories))
    events=[dict(H=H,p0=p,k=k,analytic=caustic_time(H,p,k),numerical=jacobi_event(H,p,k))
            for H,p,k in ((1,.2,20),(.3,.1,30),(1,.05,100))]
    check('first crossing times agree with integrated events',all(r['numerical'] is not None and abs(r['analytic']-r['numerical'])<2e-9 for r in events))
    scan=global_scan(1,.1,30)
    check('global first-caustic bound and original compact clock caps',scan['minimum_bound_error']<2e-12 and scan['clock_extrema_error']<2e-12 and
        scan['clock_cap_interval_nonempty'] and scan['cap_time_bounds_inside_regular_region'])
    check('threshold equality and Minkowski controls',caustic_time(1,.1,20) is None and caustic_time(1,.1,10) is None and
        abs(center_invariants(2,1,.1,20)['K']-1)<2e-12 and abs(caustic_time(1e-7,.1,20)-.5)<1e-7 and caustic_time(0,.1,20)==.5)
    tc=scan['caustic_time']; invariants=[center_invariants(tc-d,1,.1,30) for d in (.1,.01,.001,.0001)]
    check('clock and leaf invariants diverge while metric curvature stays fixed',
        all(invariants[i+1]['K']<invariants[i]['K'] and invariants[i+1]['leaf_R']>invariants[i]['leaf_R'] for i in range(3)) and
        len(set(r['spacetime_R'] for r in invariants))==1)
    failed=any(not r['passed'] for r in checks); rc=1 if failed else (2 if args.require_closed else 0)
    data=dict(theory_status='OPEN',branch_status='EXACT_NONLINEAR_CLOCK_CAUSTIC',
        geometry=serial(geom),zero_field=serial(aux),characteristics=serial(chars),focusing=serial(focus),
        trajectories=trajectories,caustic_events=events,compact_domain=scan,invariant_approach=invariants,checks=checks)
    args.output_dir.mkdir(parents=True,exist_ok=True)
    output=args.output_dir/'results.json'; output.write_text(json.dumps(data,indent=2)+'\n')
    inputs=[HERE/'clock_caustic.py',HERE/'test_clock_caustic.py',HERE/'CONTRACT.md',HERE/'REPORT.md',
        HERE.parent/'g03_covariant_action_2026'/'ACTION.md',HERE.parent/'g03_covariant_action_2026'/'FULL_VARIATION.md']
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    manifest=dict(schema_version=1,claim_id='C-H-exact-compact-deSitter-clock-caustic',
        repository=dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            dirty=bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True))),
        command='python3 -B '+str((HERE/'clock_caustic.py').relative_to(ROOT))+(' --require-closed' if args.require_closed else '')+
            (' --output-dir <output-directory>' if args.output_dir!=HERE else ''),
        environment=dict(software=[platform.python_version(),'numpy '+np.__version__,'scipy '+scipy.__version__,'sympy '+sp.__version__],hardware=platform.machine()),
        mathematics=dict(assertion_tested='Exact same-action geodesic-clock branch, finite focusing threshold, invariant singularity and clock-cap domain',
            coefficient_domain='SymPy exact; float64 DOP853 independent ODEs',conventions='c=1; H=sqrt(Lambda/3); k positive torus wave number; p0 dimensionless; U/W spacetime constant',
            inputs=[dict(path=str(p.relative_to(ROOT)),sha256=sha(p)) for p in inputs],
            bounds=dict(trajectory=dict(H=1,p0=.2,k=20,q=[0,.014,.07,.12],t=[.05,.2]),
                events=[[1,.2,20],[.3,.1,30],[1,.05,100]],
                compact_scan=dict(H=1,p0=.1,k=30,nodes=2049,time_fractions=[0,.25,.75,.99]),
                invariant_approach=dict(H=1,p0=.1,k=30,caustic_gaps=[.1,.01,.001,.0001]),
                controls=dict(no_finite_caustic=[[1,.1,10],[1,.1,20]],
                    critical_expansion_time=2,minkowski_limit=[[0,.1,20],[1e-7,.1,20]]),
                ode=dict(method='DOP853',rtol=2e-12,atol=2e-13)),
            non_claims=['new empirical law','primordial origin/abundance','global novelty','ghost or acausality proof','full Cauchy uniqueness or Dirac count','metric curvature singularity','all MOND impossible']),
        randomness=dict(used=False,generator='',seed=None),
        run=dict(started_at=datetime.fromtimestamp(started,timezone.utc).isoformat(),runtime_seconds=time.time()-started,exit_status=rc),
        outputs=[dict(path=str(output.relative_to(ROOT)) if output.is_relative_to(ROOT) else output.name,sha256=sha(output))],
        checks=checks,result='FAILED_DIAGNOSTIC' if failed else 'EXACT_BRANCH_CAUSTIC_FULL_THEORY_OPEN',
        residual_risks=['full nonlinear uniqueness unresolved','weak clock continuation outside smooth action domain','zero-stress branch not itself a matter-observable catastrophe'])
    (args.output_dir/'computation_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Exact branch develops clock caustic; full theory OPEN; exit',rc)
    return rc


if __name__=='__main__':
    raise SystemExit(main())
