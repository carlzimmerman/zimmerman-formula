#!/usr/bin/env python3
"""Attribute one mixed-jet forcing in the linearized radial constraint ODE.

Injected derivative jets are NOT assumed integrable to a time-rate field.
This script diagnoses a defect; it does not implement a physical repair.
"""
import argparse
import json
from pathlib import Path
import sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import PchipInterpolator, CubicSpline

HERE=Path(__file__).resolve().parent;BASE=HERE.parent
sys.path.insert(0,str(BASE/'nonlinear_evolution_2026'))
from evolve import Evolution, derivatives
from equations import compiled_constraints
from project import project_state, regular_center, radial_profiles


def attribute(system,state,t,eps=1e-5):
    r=system.r;model=system.model
    state=project_state(t,state,r,model)
    rates,_=system.rhs(t,state);fields=system.fields(t,state)
    profiles=radial_profiles(r,*state[[1,4,5,6,7]])
    velocities=radial_profiles(r,*rates[[1,4,5,6,7]])
    dp=PchipInterpolator(r*r,state[7]+eps*rates[7])
    dm=PchipInterpolator(r*r,state[7]-eps*rates[7])
    center=regular_center(t,state,r,model)
    cp=regular_center(t+eps,state+eps*rates,r,model)
    cm=regular_center(t-eps,state-eps*rates,r,model)
    cd={key:(cp[key]-cm[key])/(2*eps) for key in center}
    ac,hc=center['a_c'],center['K_c'];acd,hcd=cd['a_c'],cd['K_c']
    N,Nr,Q=fields['N'],fields['Nr'],fields['Q']
    Qr,Qrr=derivatives(Q,system.dr)
    target=fields['rate'][:,3]*Q+2*Nr*Qr+N*Qrr
    target[0]=fields['rate'][0,3]*Q[0]+N[0]*center['Q2']
    target_spline=CubicSpline(r*r,target)
    background=model.background(t)['raw'];background_dot=np.r_[background[5:15],np.zeros(5)]
    names,func=compiled_constraints();tiny=1e-25
    if {'P_tt','W_YYt','W_YYY','V_tt','P_XX','P_Xt'}.intersection(names):
        raise ValueError('extend background chain before running')

    def algebra(x,y,mode):
        # Modes 0,+1,-1 share one real background and have independent
        # directional A/h rates. A component jet changes only for +/-1.
        column={0:2,1:4,-1:6}[mode]
        A=ac+y[0]+1j*tiny*(acd+y[column])
        h=hc+y[1]+1j*tiny*(hcd+y[column+1])
        def dual(index,order=0):
            if index==4:
                rate=(dp(x*x)-dm(x*x))/(2*eps)
            else:
                rate=velocities[index](x,order)
            if index==2 and order==1:
                rate+=mode*(target_spline(x*x)-velocities[2](x,1))
            return profiles[index](x,order)+1j*tiny*rate
        b,bp,bpp=dual(0),dual(0,1),dual(0,2)
        q,u,w,D=dual(1),dual(2),dual(3),dual(4)
        Y=u*u/A**2;X=q*q-Y
        jets=dict(zip(model.names,model.jetfunc(*(background+1j*tiny*background_dot),X,Y,model.gamma)))
        jets.update(M2=1.,Lambda=.7,gamma=model.gamma,A=A,R=x*b,
                    Rr=b+x*bp,Rrr=2*bp+x*bpp,h=h,Q=q,Qr=dual(1,1),
                    cr=u,crr=dual(2,1),w=w,rho=D/(A*b*b*np.sqrt(1+w*w/A**2)))
        out=np.asarray(func(*(jets[name] for name in names)),dtype=complex)
        solved=np.linalg.solve(out[:9].reshape(3,3),out[9:])
        return solved.real,solved.imag/tiny

    start=r[1]/16
    init=[center['A2']*start**2/2,0.]+[cd['A2']*start**2/2,0.]*3
    def rhs(x,y):
        base,actual=algebra(x,y,0)
        _,injected=algebra(x,y,1);_,reversed_=algebra(x,y,-1)
        return np.r_[base[:2],actual[:2],injected[:2],reversed_[:2]]
    solution=solve_ivp(rhs,(start,r[-1]),init,method='DOP853',rtol=2e-11,atol=2e-13,dense_output=True)
    if not solution.success:raise RuntimeError(solution.message)
    values=solution.sol(r[1:]);derived={mode:np.zeros((3,len(r))) for mode in (0,1,-1)}
    for mode in derived:derived[mode][:,0]=[acd,hcd,hcd]
    for i,x in enumerate(r[1:],1):
        y=values[:,i-1]
        for mode,column in ((0,2),(1,4),(-1,6)):
            _,d=algebra(x,y,mode)
            derived[mode][:,i]=[acd+y[column],hcd+y[column+1],d[2]]
    mask=r<2.8;ids=np.flatnonzero(mask)
    rows={}
    for mode in derived:
        error=derived[mode]-rates[[0,3,2]]
        rows[str(mode)]={key:{'maximum':float(max(abs(error[j,mask]))),
                             'radius':float(r[ids[np.argmax(abs(error[j,mask]))]])}
                         for j,key in enumerate(('A','h','k'))}
    linear_error=float(np.max(abs(derived[1]+derived[-1]-2*derived[0])))
    if linear_error>1e-9:raise AssertionError(('nonlinear response in directional forcing',linear_error))
    defect=velocities[2](r,1)-target
    return dict(points=len(r),t=t,directional_step=eps,nfev=solution.nfev,
                errors=rows,linear_sign_control_error=linear_error,
                mixed_jet_maximum=float(max(abs(defect[mask]))),
                correction_integrability='NOT established; this is component attribution only')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path,required=True)
    args=parser.parse_args();rows=[]
    for n in (129,257,513):
        path=BASE/f'fresh_tangency_2026/offset_001/state_{n}.npz'
        with np.load(path) as data:state=data['state'];r=data['r']
        system=Evolution(.02,.3,len(r),3.,.022,1e-6)
        row=attribute(system,state,.02);rows.append(row)
        print(json.dumps(row),flush=True)
    args.result_file.write_text(json.dumps(dict(cases=rows,full_theory_status='OPEN'),indent=2)+'\n')


if __name__=='__main__':main()
