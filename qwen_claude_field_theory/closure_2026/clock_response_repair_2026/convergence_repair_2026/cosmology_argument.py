#!/usr/bin/env python3
"""Derive the fixed action's ADM invariants; do not select a MOND prescription."""
import json
import contextlib
import importlib.util
import io
from pathlib import Path
import sympy as s


def derive():
    path=Path(__file__).resolve().parent.parent/'spherical_baryon_bridge/action/derive.py'
    spec=importlib.util.spec_from_file_location('fixed_clock_action',path)
    action=importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):spec.loader.exec_module(action)
    N,a=s.symbols('N a',positive=True)
    z,H,zd,q,qd,M,Lambda,gamma=s.symbols('z H zd q qdot M2 Lambda gamma',real=True)
    beta=s.Matrix(s.symbols('beta1:4',real=True));grad=s.Matrix(s.symbols('chi1:4',real=True))
    ct=s.symbols('chi_t',real=True);h=a*a*s.exp(2*z)
    metric=s.zeros(4);metric[0,0]=-N*N+h*beta.dot(beta)
    for i in range(3):
        metric[0,i+1]=metric[i+1,0]=h*beta[i];metric[i+1,i+1]=h
    inverse=s.zeros(4);inverse[0,0]=-1/N**2
    for i in range(3):
        inverse[0,i+1]=inverse[i+1,0]=beta[i]/N**2
        for j in range(3):inverse[i+1,j+1]=(1/h if i==j else 0)-beta[i]*beta[j]/N**2
    n=s.Matrix([1/N,*[-v/N for v in beta]])
    projector=inverse+n*n.T;covector=s.Matrix([ct,*grad])
    X=-(covector.T*inverse*covector)[0]
    Q=(n.T*covector)[0];Y=(covector.T*projector*covector)[0]
    checks=dict(metric_inverse=all(s.simplify(v)==0 for v in metric*inverse-s.eye(4)),
                unit_clock=s.simplify((n.T*metric*n)[0]+1)==0,
                projected_gradient=s.simplify(Y-grad.dot(grad)/h)==0,
                kinetic_decomposition=s.simplify(X-(Q*Q-Y))==0,
                homogeneous_Y=s.simplify(Y.subs(dict.fromkeys(grad,0)))==0)
    # Direct Christoffel contraction, zero shift but arbitrary lapse gradients.
    # g_ii=a^2 exp(2z); no metric field equation or acceleration prescription used.
    Nt=s.symbols('N_t',real=True);Ng=s.symbols('N1:4',real=True);zg=s.symbols('z1:4',real=True)
    diag=s.diag(-N*N,h,h,h);di=diag.inv()
    def partial(expr,index):
        if index==0:return s.diff(expr,N)*Nt+s.diff(expr,a)*a*H+s.diff(expr,z)*zd
        return s.diff(expr,N)*Ng[index-1]+s.diff(expr,z)*zg[index-1]
    conn={}
    for i in range(4):
        for j in range(4):
            for k in range(4):
                conn[i,j,k]=s.simplify(sum(di[i,l]*(partial(diag[l,k],j)+partial(diag[l,j],k)-partial(diag[j,k],l))/2 for l in range(4)))
    nc=s.Matrix([-N,0,0,0]);nv=s.Matrix([1/N,0,0,0])
    acceleration=s.Matrix([s.simplify(sum(nv[j]*(partial(nc[i],j)-sum(conn[k,j,i]*nc[k] for k in range(4))) for j in range(4))) for i in range(4)])
    checks['clock_acceleration_from_connection']=all(s.simplify(v)==0 for v in acceleration-s.Matrix([0,*[v/N for v in Ng]]))
    checks['FLRW_clock_geodesic']=acceleration.subs(dict.fromkeys(Ng,0))==s.zeros(4,1)
    # Homogeneous box chi by divergence, and expansion from extrinsic curvature.
    box=s.simplify((s.diff(-a**3*q,a)*a*H+s.diff(-a**3*q,q)*qd)/a**3)
    K=s.simplify(sum(di[i,i]*partial(diag[i,i],0)/(2*N) for i in range(1,4)))
    checks['homogeneous_box']=s.simplify(box+qd+3*H*q)==0
    checks['extrinsic_expansion']=s.simplify(K-3*(H+zd)/N)==0
    # Same cubic action, with its explicit homogeneous boundary improvement.
    cubic_cov=gamma*q*q*box
    boundary_rate=-gamma*(q*q*qd+H*q**3)
    checks['homogeneous_cubic_boundary']=s.expand(cubic_cov-(-2*gamma*H*q**3)-boundary_rate)==0
    ep,Psi=s.symbols('epsilon Psi',real=True)
    spatial=s.Matrix(s.symbols('sigma1:4',real=True))
    weak=Y.subs({**{x:ep*v for x,v in zip(grad,spatial)},z:-ep*Psi})
    quadratic=s.simplify(s.diff(weak,ep,2).subs(ep,0)/2)
    checks['weak_projected_argument']=s.simplify(quadratic-spatial.dot(spatial)/a**2)==0
    Wsector=action.A*action.R**2*action.W
    checks['actual_action_W_spatial_variation']=s.cancel(action.partial(Wsector,action.u)
        -2*action.R**2*action.u*action.WY/action.A)==0
    checks['actual_action_W_has_no_chi_velocity']=action.partial(Wsector,action.ct)==0
    if not all(checks.values()):raise AssertionError(checks)
    return dict(checks=checks,inherited_action_checks=len(action.checks),
                exact_Y=str(s.simplify(Y)),normal_acceleration=[str(v) for v in acceleration],
                expansion=str(K),homogeneous_box_chi=str(box),weak_Y_at_order_two=str(quadratic),
                conclusion='No additive cH term in this action\'s projected Y or clock four-acceleration; H still enters curvature, expansion, braiding and background coefficients.',
                unresolved='Y is a chi-gradient invariant, not yet the physical acceleration argument of an action-derived exponential MOND law.',
                forbidden_inference='Neither phenomenological PM kernel prescription is thereby certified, and their reported structure ratios cannot be imported as this action\'s prediction.',
                full_theory='OPEN',coefficient_reconstruction=False)


if __name__=='__main__':print(json.dumps(derive(),indent=2))
