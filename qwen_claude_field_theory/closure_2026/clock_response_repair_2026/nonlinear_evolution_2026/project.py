#!/usr/bin/env python3
"""Solve three actual radial constraints for A_r,h_r,k on every time slice.

Regular-center initial data determine A and h; no target force is prescribed.
This supplies a constrained numerical formulation, not a new field equation.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline,PchipInterpolator
from equations import constraint_rates


def project_state(t,state,r,model):
    b,Q,u,w,D=state[1],state[4],state[5],state[6],state[7]
    even=lambda y:CubicSpline(r,y,bc_type=((1,0.),(2,0.)))
    odd=lambda y:CubicSpline(r,y,bc_type=((2,0.),(2,0.)))
    bs,qs,us,ws,ds=even(b),even(Q),odd(u),odd(w),PchipInterpolator(r,D)
    ac=b[0];q=Q[0];u1=float(us(0,1));j=model.jets(t,q*q,0.)
    h0=(j["P_t"]-j["V_t"]+6*q*j["W_Y"]*u1/ac**2)/(3*j["W"])
    rho0=D[0]/ac**3
    rhoc=2*q*q*j["P_X"]-j["P"]+j["V"]-6*model.gamma*q**3*h0+6*model.gamma*q*q*u1/ac**2
    b2=float(bs(0,2));A2=3*b2+ac**3*(rhoc+rho0+.7-3*h0*h0)/3
    start=r[1]/16
    initial=[ac+A2*start**2/2,h0]

    def values(x,A,h):
        bv=float(bs(x));bp=float(bs(x,1));bpp=float(bs(x,2))
        qv=float(qs(x));uv=float(us(x));wv=float(ws(x));Dv=float(ds(x))
        out=model.jets(t,qv*qv-uv*uv/A**2,uv*uv/A**2)
        out.update(A=A,R=x*bv,Rr=bv+x*bp,Rrr=2*bp+x*bpp,h=h,Q=qv,
                   Qr=float(qs(x,1)),cr=uv,crr=float(us(x,1)),w=wv,
                   rho=Dv/(A*bv*bv*np.sqrt(1+wv*wv/A**2)))
        return out

    def rhs(x,y):return constraint_rates(values(x,*y))[:2]
    solution=solve_ivp(rhs,(start,r[-1]),initial,method="DOP853",rtol=2e-10,atol=2e-12,dense_output=True)
    if not solution.success:raise RuntimeError("radial constraint solve: "+solution.message)
    projected=state.copy()
    projected[0,0]=ac;projected[3,0]=h0;projected[2,0]=h0
    projected[0,1:],projected[3,1:]=solution.sol(r[1:])
    for i in range(1,len(r)):
        projected[2,i]=constraint_rates(values(r[i],projected[0,i],projected[3,i]))[2]
    return projected


if __name__=="__main__":
    from evolve import Evolution
    system=Evolution(.02,.3,65,3.,.02,1e-6)
    out=project_state(0.,system.initial,system.r,system.model)
    print({"scope":"initial constraint projection control", "max_delta_A":float(max(abs(out[0]-system.initial[0]))),
           "max_delta_H":float(max(abs(out[3]-system.initial[3])))})
