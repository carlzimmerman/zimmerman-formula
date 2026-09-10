#!/usr/bin/env python3
"""Preserve the actual radial equations and measure common-action defects.

The third halo MUST use the first halo's GX,GXX in its stress/current. Giving
it its own reconstructed G would silently replace the common-action problem.
"""
import json
import numpy as np
from scipy.integrate import solve_ivp
import triple_seed as seed

j=seed.j; third=seed.third
EPS=(1e-6,2e-6,1.5e-6)


def initial(b=.25,y1=.1,start=(.3,.16)):
    fit=seed.solve(b,start,y1=y1)
    if fit.get('max_scaled_residual',1)>1e-8:
        raise ValueError('seed equations not solved')
    v=np.array(fit['state'])
    return fit,np.array([*v[:4],np.log(fit['y3']),fit['U3']/EPS[2],v[4],0.])


def parts(X,state):
    pair=np.array([*state[:4],state[6]])
    px,pxx=j.action_jet(X,pair,EPS[:2])
    _,a,b=j.shared(X,pair,EPS[:2])
    c=j.coefficients(EPS[2],np.exp(state[4]),X,EPS[2]*state[5],state[6])
    return px,pxx,(a,b,c)


def rhs(t,state):
    X=.5+EPS[0]*t
    pair=np.array([*state[:4],state[6]])
    px,a,b=j.shared(X,pair,EPS[:2])
    c=j.coefficients(EPS[2],np.exp(state[4]),X,EPS[2]*state[5],state[6])
    out=[]
    for eps,v in zip(EPS,(a,b,c)):
        out.extend([px/(v['y']*v['ry']*v['W']),
                    (-2-2*v['g']*(2*X+v['U'])*px/v['W'])/eps])
    return EPS[0]*np.array(out+[px,px*a['H']])


def preservation(t,state):
    px,pxx,vs=parts(.5+EPS[0]*t,state)
    F=[v['a']+px*v['b'] for v in vs]
    derivatives=[third.derivatives(v,px) for v in vs]
    Fx=[d[0]+px*d[1]+pxx*v['b'] for d,v in zip(derivatives,vs)]
    return np.array([(F[2]-F[0])*EPS[0],(Fx[2]-Fx[0])*EPS[0]**2])


def next_preservation(b,step=1e-5):
    fit,state=initial(b)
    velocity=rhs(0,state)
    # The next Lie derivative of F3_X-F1_X along the full flow. Central
    # differences are deliberately labeled numerical, not exact derivatives.
    slope=(preservation(step,state+step*velocity)[1]
           -preservation(-step,state-step*velocity)[1])/(2*step)
    return dict(bscale=b,step=step,next_scaled_preservation=float(slope),fit=fit)


def actual_common_stress(v,px,pxx,GX,GXX):
    X,U,r,g,gr,P,B,W,BrB=[v[k] for k in ('X','U','r','g','gr','P','B','W','BrB')]
    invA=2*X+U;p=np.sqrt(B*U);Xr=W/px
    Ur=-2*g*invA-2*Xr;Lp=(BrB+Ur/U)/2
    H=np.array([[-g*p/B,g*np.sqrt(invA/B),0,0],
                [g*np.sqrt(invA/B),p*(Lp-BrB/2)/B,0,0],
                [0,0,p/(B*r),0],[0,0,0,p/(B*r)]])
    C,stress=j.source.evaluator()(1,GX,GXX,P,px,pxx,-np.sqrt(invA),np.sqrt(U),0,0,
                                  *[H[i,k] for i in range(4) for k in range(i,4)])
    rho=v['E0']-r*W/v['T']-P
    pt=(gr+g*g-g*BrB/2+(g-BrB/2)/r)/B
    scale=max(abs(rho),abs(P),abs(pt),1e-200)
    error=max(abs(stress[0,0]-rho),abs(stress[1,1]-P),abs(stress[2,2]-pt),abs(stress[0,1]))/scale
    jt=np.array([px*p/B,2*GX*X*g/B,-2*GX*p*p/(B*B*r)])
    return dict(common_action_stress_error=float(error),common_action_current_error=float(abs(sum(jt))/sum(abs(jt))),
                kinetic=float(C[0,0]),radial=float(C[1,1]),angular=float(C[2,2]))


def observe(t,state):
    X=.5+EPS[0]*t;px,pxx,vs=parts(X,state)
    one=j.local(vs[0],px,pxx)
    physical=[actual_common_stress(v,px,pxx,one['GX'],one['GXX']) for v in vs]
    return dict(t=float(t),X=float(X),ys=[float(v['y']) for v in vs],P=float(state[6]),G=float(state[7]),
                value_mismatch=float(vs[2]['H']/vs[0]['H']-1),
                scaled_preservation=preservation(t,state).tolist(),halos=physical)


def integrate(b=.25,duration=.05,rtol=1e-10,max_step=.0005):
    fit,state=initial(b)
    sol=solve_ivp(rhs,(0,duration),state,method='DOP853',rtol=rtol,atol=rtol/100,
                  dense_output=True,max_step=max_step)
    ts=np.linspace(0,sol.t[-1],21)
    return dict(bscale=b,rtol=rtol,max_step=max_step,solver_success=bool(sol.success),
                endpoint=float(sol.t[-1]),message=sol.message,
                rows=[observe(t,sol.sol(t)) for t in ts])


def main():
    for b in (.05,.1,.2,.25,.4,.6,.8):
        for step in (1e-4,1e-5,1e-6):
            try:print('NEXT='+json.dumps(next_preservation(b,step)),flush=True)
            except ValueError as exc:print('UNRESOLVED='+json.dumps(dict(b=b,error=str(exc))))
    for step in (.0005,.00025):
        for end in (.05,-.05):print('FLOW='+json.dumps(integrate(duration=end,max_step=step)),flush=True)
    return 0


if __name__=='__main__':raise SystemExit(main())
