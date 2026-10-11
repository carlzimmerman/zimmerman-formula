"""Reciprocal Gaussian breathing source and softened self-gravitating streams.
Finite variational mechanics with a recorded radiative-energy sink; no halo target.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.special import erf
from scipy.integrate import solve_ivp

M=G=1.
A=1/(2*np.sqrt(np.pi))
C=.05*A
MU=3*M
SOFT=.08
N=24
CHECKS=[]


def check(name, value, limit):
    CHECKS.append(dict(name=name,passed=bool(value<limit),value=float(value),limit=float(limit)))


def field(x,b):
    r=np.linalg.norm(x,axis=-1)
    u=r/b
    k=np.sqrt(2/np.pi)
    safe=np.maximum(r,1e-100)
    phi=-erf(u/np.sqrt(2))/safe
    enclosed=erf(u/np.sqrt(2))-k*u*np.exp(-u*u/2)
    fac=enclosed/safe**3
    small=u<1e-3
    phi=np.where(small,-k/b*(1-u*u/6+u**4/40-u**6/336),phi)
    fac=np.where(small,k/b**3*(1/3-u*u/10+u**4/56),fac)
    return phi,-fac[...,None]*x,k/b**2*np.exp(-u*u/2)


def unpack(z):
    return z[:3],z[3:6],z[6],z[7],z[8],z[9:9+3*N].reshape(N,3),z[9+3*N:].reshape(N,3)


def pairs(pos,mass,enabled):
    if not enabled:
        return np.zeros_like(pos),0.,np.zeros(N)
    dx=pos[:,None,:]-pos[None,:,:]
    d2=np.sum(dx*dx,axis=-1)+SOFT**2
    np.fill_diagonal(d2,np.inf)
    acc=-mass*np.sum(dx/d2[...,None]**1.5,axis=1)
    pot=-mass*np.sum(1/np.sqrt(d2),axis=1)
    return acc,float(.5*mass*np.sum(pot)),pot


def initial(eta,selfgravity):
    positions=[]; velocities=[]
    for k in range(6):
        z=(k+.5)/6
        theta=k*np.pi*(3-np.sqrt(5))
        er=np.array([np.sqrt(1-z*z)*np.cos(theta),np.sqrt(1-z*z)*np.sin(theta),z])
        et=np.cross([0.,0.,1.],er); et/=np.linalg.norm(et)
        for parity in (-1.,1.):
            for sense in (-1.,1.):
                # Separate opposite tangential beams in space; preserve exact
                # antipodal pairing and cancel their initial angular momenta.
                radial=er*np.cos(.15)+sense*et*np.sin(.15)
                tangent=-sense*er*np.sin(.15)+et*np.cos(.15)
                positions.append(parity*2*radial)
                velocities.append((parity*radial,parity*sense*tangent))
    pos=np.array(positions)
    _,_,pc=pairs(pos,eta/N,selfgravity)
    pb,_,_=field(pos,1.)
    vel=[]
    for k,(er,et) in enumerate(velocities):
        vt=(.2 if (k//4)%2==0 else .6)/2
        # Same positive instantaneous energy including other streams at t=0.
        vr=-np.sqrt(2*(.05-pb[k]-pc[k])-vt*vt)
        vel.append(vr*er+vt*et)
    return np.r_[np.zeros(6),1.,0.,0.,pos.ravel(),np.array(vel).ravel()]


def energy(z,eta,selfgravity):
    R,V,b,w,Q,pos,vel=unpack(z)
    mass=eta/N
    pb,_,_=field(pos-R,b)
    _,usc,_=pairs(pos,mass,selfgravity)
    return float(.5*M*np.dot(V,V)+.5*MU*w*w+C/b**2-A/b+
                 .5*mass*np.sum(vel*vel)+mass*np.sum(pb)+usc)


def rhs(eta,gamma,selfgravity,mutate=False):
    mass=eta/N
    def evaluate(t,z):
        R,V,b,w,Q,pos,vel=unpack(z)
        if b<=0:
            raise ArithmeticError('Nonpositive source radius')
        _,acc,db=field(pos-R,b)
        ac,_,_=pairs(pos,mass,selfgravity)
        force_b=mass*np.sum(db)
        bw=(2*C/b**3-A/b**2+ (force_b if mutate else -force_b))/MU-gamma*w
        return np.r_[V,-mass*np.sum(acc,axis=0)/M,w,bw,MU*gamma*w*w,
                     vel.ravel(),(acc+ac).ravel()]
    return evaluate


def run(eta,gamma,selfgravity=True,refined=False,mutate=False):
    # The no-self-gravity control retains exactly the same physical inflow.
    z0=initial(eta,True)
    ts=np.linspace(0,30,1501)
    sol=solve_ivp(rhs(eta,gamma,selfgravity,mutate),(0,30),z0,method='DOP853',t_eval=ts,
                  rtol=2e-11 if refined else 1e-9,atol=2e-13 if refined else 1e-11,
                  max_step=.01 if refined else .03)
    if not sol.success: raise RuntimeError(sol.message)
    es=np.array([energy(z,eta,selfgravity) for z in sol.y.T])
    qs=sol.y[8]
    drift=float(np.max(np.abs(es+qs-es[0])))
    p=[];j=[];core=[]
    for z in sol.y.T:
        R,V,b,w,Q,pos,vel=unpack(z)
        p.append(M*V+eta/N*np.sum(vel,axis=0))
        j.append(M*np.cross(R,V)+eta/N*np.sum(np.cross(pos,vel),axis=0))
        core.append(eta*np.mean(np.linalg.norm(pos-R,axis=1)<.4))
    p=np.array(p);j=np.array(j)
    pd=float(np.max(np.linalg.norm(p-p[0],axis=1)))
    jd=float(np.max(np.linalg.norm(j-j[0],axis=1)))
    name=f'eta{eta}_gamma{gamma}_self{selfgravity}_ref{refined}'
    if not mutate:
        check(name+'_energy_plus_heat',drift,2e-6)
        check(name+'_momentum',pd,2e-7)
        check(name+'_angular_momentum',jd,2e-7)
        check(name+'_heat_monotone',float(max(0,-np.min(np.diff(qs)))),1e-12)
        lower=-(A+np.sqrt(2/np.pi)*eta)**2/(4*C)
        if selfgravity: lower-=eta*eta*(1-1/N)/(2*SOFT)
        check(name+'_finite_heat_budget',max(0,float(np.max(qs)-(es[0]-lower))),2e-6)
    last=ts>=20
    return dict(name=name,eta=eta,gamma=gamma,selfgravity=selfgravity,
                energy0=float(es[0]),energy_heat_error=drift,momentum_error=pd,angular_error=jd,
                final_heat=float(qs[-1]),minimum_source_radius=float(np.min(sol.y[6])),
                final_source_radius=float(sol.y[6,-1]),late_radius_range=[float(np.min(sol.y[6,last])),float(np.max(sol.y[6,last]))],
                late_core_mass=float(np.mean(np.array(core)[last])),
                initial_state=z0.tolist(),final_state=sol.y[:,-1].tolist(),
                sampled_time=ts[::10].tolist(),sampled_source_radius=sol.y[6,::10].tolist(),
                sampled_heat=qs[::10].tolist(),sampled_core_mass=np.array(core)[::10].tolist())


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    # Independently finite-difference the full Hamiltonian's directional rate.
    z=initial(.3,True);z[7]=-.15;z[3]=.07
    direction=rhs(.3,.5,True)(0,z)
    eps=1e-6
    rate=(energy(z+eps*direction,.3,True)-energy(z-eps*direction,.3,True))/(2*eps)
    check('hamiltonian_power_balance',abs(rate+direction[8]),2e-8)
    point=np.array([[.23,-.11,.17]])
    phi,acc,db=field(point,.4)
    grad=[]
    for k in range(3):
        dp=np.zeros_like(point);dp[0,k]=eps
        grad.append(float(((field(point+dp,.4)[0]-field(point-dp,.4)[0])/(2*eps))[0]))
    check('gaussian_force_gradient',float(np.max(np.abs(acc[0]+grad))),1e-8)
    dbfd=float(((field(point,.4+eps)[0]-field(point,.4-eps)[0])/(2*eps))[0])
    check('gaussian_b_derivative',abs(dbfd-db[0]),1e-8)
    pos=unpack(z)[5]
    d=np.linalg.norm(pos[:,None,:]-pos[None,:,:],axis=-1)
    np.fill_diagonal(d,np.inf)
    check('initial_beams_separated',float(2*SOFT/np.min(d)),1.)
    rows=[]
    for eta in (.05,1.):
        for gamma in (0.,.5,2.):
            row=run(eta,gamma);rows.append(row)
            print(row['name'],'bfinal',row['final_source_radius'],'late core',row['late_core_mass'],'drift',row['energy_heat_error'],flush=True)
    row=run(1.,.5,False);rows.append(row)
    refined=run(1.,.5,True,True)
    mutation=run(1.,.5,True,False,True)
    CHECKS.append(dict(name='wrong_backreaction_sign_rejected',passed=bool(mutation['energy_heat_error']>1e-3),value=mutation['energy_heat_error']))
    result=dict(base_revision='0e3b9616a35724da12b48b0c655cd936c906fdd6',cells=rows,
                refined=refined,mutation=mutation,checks=CHECKS,
                assertions=len(CHECKS),passed=sum(x['passed'] for x in CHECKS))
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(result['passed'],'/',result['assertions'])
    raise SystemExit(0 if result['passed']==result['assertions'] else 1)


if __name__=='__main__': main()
