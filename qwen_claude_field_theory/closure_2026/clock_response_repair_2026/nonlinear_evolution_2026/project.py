#!/usr/bin/env python3
"""Solve three actual radial constraints for A_r,h_r,k on every time slice.

Regular-center initial data determine A and h; no target force is prescribed.
This supplies a constrained numerical formulation, not a new field equation.
"""
import numpy as np
from functools import lru_cache
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline,PchipInterpolator
from equations import constraint_rates


@lru_cache(maxsize=8)
def _first_sample_jet_weight(grid):
    r=np.asarray(grid)
    basis=np.zeros(len(r)-1);basis[0]=1/r[1]
    return float(CubicSpline(r[1:]**2,basis)(0.))


def match_odd_center_rate(r,rate,target):
    """Enforce the continuum mixed-derivative jet in the discrete odd basis.

    Only the first positive-radius rate is adjusted. The target comes from
    (N Q)_{rr}(0)=N_{rr}(0) Q(0)+N(0) Q_{rr}(0), not from a fitted residual.
    This is an origin closure, not a change to the bulk continuum equation.
    Its accuracy and evolution convergence require independent tests.
    """
    measured=float(CubicSpline(r[1:]**2,rate[1:]/r[1:])(0.))
    weight=_first_sample_jet_weight(tuple(r))
    corrected=rate.copy();corrected[1]+=(target-measured)/weight
    return corrected


def radial_profiles(r,b,Q,u,w,D):
    """Smooth center parity: even fields F(r²), odd fields r G(r²).

    A spline in r with only its first center derivative fixed can introduce
    a |r|³ cusp into an even field. Projection subsequently differentiates
    that interpolation, so the stronger spherical regularity matters.
    Density uses a shape-preserving interpolant to retain positivity.
    """
    def even(y,positive=False):
        fit=(PchipInterpolator if positive else CubicSpline)(r*r,y)
        def value(x,order=0):
            x=np.asarray(x);z=x*x
            if order==0:return fit(z)
            if order==1:return 2*x*fit(z,1)
            if order==2:return 2*fit(z,1)+4*z*fit(z,2)
            raise ValueError('radial jet order exceeds two')
        return value
    def odd(y):
        fit=CubicSpline(r[1:]**2,y[1:]/r[1:])
        def value(x,order=0):
            x=np.asarray(x);z=x*x
            if order==0:return x*fit(z)
            if order==1:return fit(z)+2*z*fit(z,1)
            if order==2:return 6*x*fit(z,1)+4*x*z*fit(z,2)
            raise ValueError('radial jet order exceeds two')
        return value
    return even(b),even(Q),odd(u),odd(w),even(D,positive=True)


def regular_center(t,state,r,model,profiles=None):
    """Use one regular Taylor jet in projection and lapse preservation."""
    b,Q,u,w,D=state[1],state[4],state[5],state[6],state[7]
    bs,qs,us,ws,ds=profiles if profiles is not None else radial_profiles(r,b,Q,u,w,D)
    ac=b[0];q=Q[0];u1=float(us(0,1));j=model.jets(t,q*q,0.)
    h0=(j["P_t"]-j["V_t"]+6*q*j["W_Y"]*u1/ac**2)/(3*j["W"])
    rho0=D[0]/ac**3
    rhoc=2*q*q*j["P_X"]-j["P"]+j["V"]-6*model.gamma*q**3*h0+6*model.gamma*q*q*u1/ac**2
    b2=float(bs(0,2));A2=3*b2+ac**3*(rhoc+rho0+.7-3*h0*h0)/3
    return dict(a_c=ac,A2=A2,b2=b2,K_c=h0,Q_c=q,Q2=float(qs(0,2)),u1=u1)


def project_state(t,state,r,model):
    b,Q,u,w,D=state[1],state[4],state[5],state[6],state[7]
    profiles=radial_profiles(r,b,Q,u,w,D)
    bs,qs,us,ws,ds=profiles
    center=regular_center(t,state,r,model,profiles)
    ac,A2,h0=center['a_c'],center['A2'],center['K_c']
    start=r[1]/16
    # Integrate departures from the regular center, so adaptive relative error
    # is measured against the perturbation rather than an order-one background.
    # The ODE and the tolerances are unchanged by this affine coordinate shift.
    initial=[A2*start**2/2,0.]

    def values(x,A,h):
        bv=float(bs(x));bp=float(bs(x,1));bpp=float(bs(x,2))
        qv=float(qs(x));uv=float(us(x));wv=float(ws(x));Dv=float(ds(x))
        out=model.jets(t,qv*qv-uv*uv/A**2,uv*uv/A**2)
        out.update(A=A,R=x*bv,Rr=bv+x*bp,Rrr=2*bp+x*bpp,h=h,Q=qv,
                   Qr=float(qs(x,1)),cr=uv,crr=float(us(x,1)),w=wv,
                   rho=Dv/(A*bv*bv*np.sqrt(1+wv*wv/A**2)))
        return out

    def rhs(x,y):return constraint_rates(values(x,ac+y[0],h0+y[1]))[:2]
    solution=solve_ivp(rhs,(start,r[-1]),initial,method="DOP853",rtol=2e-10,atol=2e-12,dense_output=True)
    if not solution.success:raise RuntimeError("radial constraint solve: "+solution.message)
    projected=state.copy()
    projected[0,0]=ac;projected[3,0]=h0;projected[2,0]=h0
    offsets=solution.sol(r[1:])
    projected[0,1:]=ac+offsets[0];projected[3,1:]=h0+offsets[1]
    for i in range(1,len(r)):
        projected[2,i]=constraint_rates(values(r[i],projected[0,i],projected[3,i]))[2]
    return projected


if __name__=="__main__":
    from evolve import Evolution
    system=Evolution(.02,.3,65,3.,.02,1e-6)
    out=project_state(0.,system.initial,system.r,system.model)
    print({"scope":"initial constraint projection control", "max_delta_A":float(max(abs(out[0]-system.initial[0]))),
           "max_delta_H":float(max(abs(out[3]-system.initial[3])))})
