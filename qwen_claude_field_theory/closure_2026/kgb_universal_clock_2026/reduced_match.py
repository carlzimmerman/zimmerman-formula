#!/usr/bin/env python3
"""Eliminate common pressure and shared F_X before three-equation matching.

Only the pressure quadratic root connected to w=0 is searched. Invalid real
charts are rejected, not interpreted as exclusions of other branches.
"""
import json
from dataclasses import asdict
import numpy as np
from scipy.optimize import least_squares
import universal_seed as s
from structure import closed_inverse as c


def pair(theta,spec=s.Spec(),u1=.128):
    dw1,y2,u2=np.exp(theta)
    m1=c.geometry(spec.eps1,spec.y1);m2=c.geometry(spec.eps2,y2)
    w1=-.05*dw1*m1['g']
    a=c.normalized(spec.eps1,spec.y1,spec.X,u1*spec.eps1,w1,spec.F)
    aa=m2['g']+2/m2['r'];disc=aa*aa+1.5*m2['B']*a['P']/spec.F
    if disc<=0:raise ValueError('pressure quadratic has no real regular root')
    w2=m2['B']*a['P']/(aa+np.sqrt(disc))
    b=c.normalized(spec.eps2,y2,spec.X,u2*spec.eps2,w2,spec.F)
    if min(a['Dcoord'],b['Dcoord'])<=0:raise ValueError('target chart not regular')
    return a,b


def curvature_parts(a):
    """D_X(kappa,gamma)=A+f B, exact L0 and complex-step L1."""
    eps,y,X,U,w,F=(a[k] for k in ('eps','y','X','U','w','F'))
    A=np.array([-2*a['gamma']*a['Rrad']/a['p'],-a['gamma']/U])
    point=np.array([y,X,U,w,F]);direction=np.array([1/(a['ry']*w),0.,
        -2*a['g']*a['Q']/w,a['W']/w,1.])
    varied=c.normalized(eps,*(point+1j*1e-25*direction))
    B=np.imag([varied['kappa'],varied['gamma']])/1e-25
    return A,B


def control(A,B):
    denominator=np.dot(B,B)
    if denominator==0:raise ValueError('zero first-preservation control vector')
    f=-np.dot(A,B)/denominator
    return f,A+f*B


def residual(theta,spec=s.Spec(),u1=.128):
    a,b=pair(theta,spec,u1);A1,B1=curvature_parts(a);A2,B2=curvature_parts(b)
    scale=s.scales(spec)[3:]/spec.f;A=(A1-A2)/scale;B=(B1-B2)/scale
    den=np.linalg.norm(A)*np.linalg.norm(B)
    if den==0:raise ValueError('degenerate first-preservation normalization')
    return np.array([(a['H']-b['H'])/(1+abs(a['H'])+abs(b['H'])),
        (a['gamma']-b['gamma'])/(1+abs(a['gamma'])+abs(b['gamma'])),
        (A[0]*B[1]-A[1]*B[0])/den])


def solve(start=(1.5,.15,.128),spec=s.Spec(),u1=.128,max_nfev=250):
    lower=np.log([.005,.005,.0001]);upper=np.log([1e6,30.,1000.])
    out=least_squares(lambda t:residual(t,spec,u1),np.log(start),bounds=(lower,upper),
        jac='3-point',xtol=2e-12,ftol=2e-12,gtol=2e-12,max_nfev=max_nfev)
    a,b=pair(out.x,spec,u1);A1,B1=curvature_parts(a);A2,B2=curvature_parts(b)
    scale=s.scales(spec)[3:]/spec.f;A=(A1-A2)/scale;B=(B1-B2)/scale
    f,err=control(A,B)
    # Independent original varied inverse, no projection of its five residuals.
    jets=[]
    for row in (a,b):
        _,v=s.raw_jet(row['eps'],row['y'],row['X'],row['U'],row['w']/f,spec.F,f)
        jets.append(v)
    rel=abs(jets[0]-jets[1])/np.maximum(np.maximum(abs(jets[0]),abs(jets[1])),1e-100)
    return dict(spec=asdict(spec),u1=u1,start=list(start),parameters=np.exp(out.x).tolist(),
        f=float(f),Dfield=2*(spec.F-spec.X*f),nfev=out.nfev,
        reduced_residual=out.fun.tolist(),component_relative=rel.tolist(),
        max_component_relative=float(max(rel)),actual_jets=[v.tolist() for v in jets],
        states=[dict(eps=r['eps'],y=r['y'],X=r['X'],U=r['U'],w=r['w'],F=r['F']) for r in (a,b)],
        actual_jacobian_singular_values=np.linalg.svd(out.jac,compute_uv=False).tolist(),
        distance_to_log_bounds=float(min(np.min(out.x-lower),np.min(upper-out.x))),
        regular_map=s.regular_jet_map(spec.F,spec.X,f,[a,b]),
        accepted_initial_root=bool(max(rel)<1e-7 and max(abs(out.fun))<1e-7
            and s.regular_jet_map(spec.F,spec.X,f,[a,b])),
        scope='Initial common jets on one pressure root; not preservation closure, interval proof, universal action, or CMB fit')


def main():
    rows=[]
    for u in (.03,.128,.5):
        for dw in (1.5,100.,10000.):
            for y2 in (.08,.2,.8):
                start=(dw,y2,u)
                try:row=solve(start,u1=u)
                except (ValueError,np.linalg.LinAlgError,FloatingPointError) as exc:
                    row=dict(u1=u,start=list(start),error=str(exc))
                rows.append(row);print('REDUCED_PAIR='+json.dumps(row,allow_nan=False),flush=True)
    print('SUMMARY='+json.dumps(dict(attempts=len(rows),
        initial_roots=sum(r.get('accepted_initial_root',False) for r in rows),
        scope='Finite nonrandom scan; no universal exclusion')))
    return 0


if __name__=='__main__':raise SystemExit(main())
