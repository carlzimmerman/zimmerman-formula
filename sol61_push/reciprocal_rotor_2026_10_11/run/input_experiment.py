"""Finite reciprocal baryonic rotor: transfer experiment, no imposed halo target."""
import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import ellipk, ellipe

M, G, A, SOFT = 1., 1., .2, .05
I = M*A*A
ETA, R0, E0 = .01, 2., -.2
RADII = np.array([.1,.2,.4])
CHECKS = []


def check(name, ok, value=None):
    CHECKS.append(dict(name=name,passed=bool(ok),value=value))


def cross(x,y):
    return x[...,0]*y[...,1]-x[...,1]*y[...,0]


def field(x,theta,mode):
    """Positive Plummer-pair source or its exact planar azimuth average."""
    if mode == 'pair':
        q=A*np.stack([np.cos(theta),np.sin(theta)],axis=-1)
        dp=x-q[...,None,:]
        dm=x+q[...,None,:]
        sp=np.sum(dp*dp,axis=-1)+SOFT**2
        sm=np.sum(dm*dm,axis=-1)+SOFT**2
        phi=-G*M/2*(sp**(-.5)+sm**(-.5))
        acc=-G*M/2*(dp*sp[...,None]**(-1.5)+dm*sm[...,None]**(-1.5))
        return phi,acc
    r=np.linalg.norm(x,axis=-1)
    safe=np.maximum(r,1e-6)
    S=(safe+A)**2+SOFT**2
    m=4*A*safe/S
    K=ellipk(m)
    dK=(ellipe(m)/(1-m)-K)/(2*m)
    dm=4*A/S-m*2*(safe+A)/S
    phi=-2*G*M/math.pi*K/np.sqrt(S)
    dphi=-2*G*M/math.pi*(dK*dm/np.sqrt(S)-K*(safe+A)/S**1.5)
    acc=-dphi[...,None]*x/safe[...,None]
    linear=-G*M*(SOFT**2-A*A/2)/(A*A+SOFT**2)**2.5
    acc=np.where((r<1e-6)[...,None],linear*x,acc)
    phi=np.where(r<1e-6,-G*M/math.sqrt(A*A+SOFT**2)-.5*linear*r*r,phi)
    return phi,acc


def initial(j,omega,mode,nphase=24,asymmetric=False):
    angles=(np.arange(nphase)+.375)*2*math.pi/nphase
    if asymmetric:
        angles=np.array([.31])
    phase=np.repeat(angles,2)
    angular=np.tile([j,-j],len(angles))
    er=np.stack([np.cos(phase),np.sin(phase)],axis=-1)
    et=np.stack([-np.sin(phase),np.cos(phase)],axis=-1)
    pos=R0*er
    phi,_=field(pos,0.,mode)
    vr=-np.sqrt(2*(E0-phi)-(angular/R0)**2)
    vel=vr[:,None]*er+(angular/R0)[:,None]*et
    return np.r_[0.,0.,0.,0.,0.,I*omega,pos.ravel(),vel.ravel()]


def unpack(z,n):
    return z[:2],z[2:4],z[4],z[5],z[6:6+2*n].reshape(n,2),z[6+2*n:].reshape(n,2)


def rhs(mode,n,mutate=False):
    mass=ETA/n
    def evaluate(t,z):
        R,V,theta,L,pos,vel=unpack(z,n)
        x=pos-R
        _,acc=field(x,theta,mode)
        force=-mass*np.sum(acc,axis=0)
        torque=-mass*np.sum(cross(x,acc))
        if mutate:
            torque=-torque
        return np.r_[V,force/M,L/I,torque,vel.ravel(),acc.ravel()]
    return evaluate


def diagnostics(sol,n,mode,T,dt):
    times=np.linspace(0,T,round(T/dt)+1)
    z=sol.sol(times).T
    R,V,theta,L=z[:,:2],z[:,2:4],z[:,4],z[:,5]
    pos=z[:,6:6+2*n].reshape(-1,n,2)
    vel=z[:,6+2*n:].reshape(-1,n,2)
    x=pos-R[:,None,:]
    vrel=vel-V[:,None,:]
    r=np.linalg.norm(x,axis=-1)
    phi,acc=field(x,theta,mode)
    mass=ETA/n
    ei=.5*np.sum(vel*vel,axis=-1)+phi
    Epart=mass*np.sum(ei,axis=1)
    Kcom=.5*M*np.sum(V*V,axis=1)
    Krot=L*L/(2*I)
    H=Epart+Kcom+Krot
    P=M*V+mass*np.sum(vel,axis=1)
    J=M*cross(R,V)+L+mass*np.sum(cross(pos,vel),axis=1)
    exchange=Epart-Epart[0]+Kcom-Kcom[0]+Krot-Krot[0]
    cuts={}
    for radius in RADII:
        inside=r<radius
        inward=np.logical_and(~inside[:-1],inside[1:])
        outward=np.logical_and(inside[:-1],~inside[1:])
        late=times[:-1]>=T/2
        cuts[str(radius)]=dict(inward=int(inward.sum()),outward=int(outward.sum()),
                              inward_late=int(inward[late].sum()),
                              outward_late=int(outward[late].sum()),
                              inward_by_particle=inward.sum(axis=0).tolist(),
                              residence_mean=float(inside.mean()))
    # First outward R0 crossing after inward start; censor nonreturns.
    returns=(r[:-1]<R0)&(r[1:]>=R0)
    minima=[]
    return_times=[]
    for k in range(n):
        indices=np.flatnonzero(returns[:,k])
        end=int(indices[0]+1) if len(indices) else len(times)-1
        minima.append(float(r[:end+1,k].min()))
        return_times.append(float(times[end]) if len(indices) else None)
    vrad=np.sum(x*vrel,axis=-1)/np.maximum(r,1e-100)
    proxy=(r[-1]>2*R0)&(vrad[-1]>0)&(ei[-1]>0)
    ell=cross(x,vrel)
    return dict(H0=float(H[0]),J0=float(J[0]),P0=P[0].tolist(),
                max_H_error=float(np.max(abs(H-H[0]))),
                max_J_error=float(np.max(abs(J-J[0]))),
                max_P_error=float(np.max(np.linalg.norm(P-P[0],axis=1))),
                max_exchange_error=float(np.max(abs(exchange))),
                max_body_displacement=float(np.max(np.linalg.norm(R,axis=1))),
                delta_Krot=float(Krot[-1]-Krot[0]),delta_Kcom=float(Kcom[-1]-Kcom[0]),
                delta_Estreams=float(Epart[-1]-Epart[0]),
                omega_final=float(L[-1]/I),
                first_pass_minima=minima,first_return_times=return_times,
                first_return_count=sum(t is not None for t in return_times),
                instantaneous_outgoing_positive_energy_proxy=int(proxy.sum()),
                final_j_abs_mean=float(np.abs(ell[-1]).mean()),
                final_j_abs_std=float(np.abs(ell[-1]).std()),
                cuts=cuts,final_relative_radii=r[-1].tolist(),
                final_relative_j=ell[-1].tolist(),
                final_orbital_energy=ei[-1].tolist())


def run_cell(name,j,omega,mode,T=40.,nphase=24,tight=False,asymmetric=False,mutate=False):
    z=initial(j,omega,mode,nphase,asymmetric)
    n=(len(z)-6)//4
    sol=solve_ivp(rhs(mode,n,mutate),(0,T),z,method='DOP853',dense_output=True,
                  rtol=1e-10 if tight else 2e-9,atol=1e-12 if tight else 2e-11,
                  max_step=.02 if tight else .04)
    if not sol.success:
        raise RuntimeError(sol.message)
    d=diagnostics(sol,n,mode,T,.01)
    fine=diagnostics(sol,n,mode,T,.005)
    check(name+'_detector_grid',all(d['cuts'][str(r)]['inward']==fine['cuts'][str(r)]['inward']
          and d['cuts'][str(r)]['outward']==fine['cuts'][str(r)]['outward'] for r in RADII))
    d=fine
    if mutate:
        check(name+'_wrong_torque_rejected',d['max_J_error']>1e-6 or d['max_H_error']>1e-6,
              [d['max_J_error'],d['max_H_error']])
    else:
        for quantity in ['max_H_error','max_J_error','max_P_error','max_exchange_error']:
            check(name+'_'+quantity,d[quantity]<2e-8,d[quantity])
    d.update(name=name,j_initial=j,omega_initial=omega,mode=mode,n=n,T=T,nfev=sol.nfev)
    print(json.dumps(dict(name=name,nfev=sol.nfev,H_error=d['max_H_error'],
                         counts=[d['cuts'][str(r)]['inward'] for r in RADII],
                         returned=d['first_return_count'],omega_final=d['omega_final'])),flush=True)
    return d


def main(output):
    # Force, reciprocal torque and ring averaging checked independently.
    x=np.array([[.31,.17],[-.6,.3],[.05,-.02]])
    theta=.4
    phi,acc=field(x,theta,'pair')
    h=1e-6
    for k in range(2):
        dx=np.zeros_like(x);dx[:,k]=h
        fd=(field(x+dx,theta,'pair')[0]-field(x-dx,theta,'pair')[0])/(2*h)
        check('pair_gradient_'+str(k),np.max(abs(fd+acc[:,k]))<1e-7)
    tfd=(field(x,theta+h,'pair')[0]-field(x,theta-h,'pair')[0])/(2*h)
    check('reciprocal_torque_sign',np.max(abs(tfd-cross(x,acc)))<1e-7)
    angles=np.linspace(0,2*math.pi,8192,endpoint=False)
    for radius in [.001,.05,.2,.6,2.]:
        p=np.array([[radius,0.]])
        direct=np.mean(field(np.broadcast_to(p,(len(angles),1,2)),angles,'pair')[0])
        ring,ar=field(p,0.,'ring')
        check('ring_average_%g'%radius,abs(direct-ring[0])<1e-10)
        fd=(field(p+np.array([[h,0]]),0.,'ring')[0]-field(p-np.array([[h,0]]),0.,'ring')[0])/(2*h)
        check('ring_gradient_%g'%radius,abs(fd[0]+ar[0,0])<2e-7)
    cells=[]
    for mode,omega in [('pair',.5),('pair',0.),('ring',.5)]:
        for j in [.05,.3]:
            cells.append(run_cell('%s_w%s_j%s'%(mode,omega,j),j,omega,mode))
    for mode,omega in [('pair',.5),('pair',0.),('ring',.5)]:
        a,b=[v for v in cells if v['mode']==mode and v['omega_initial']==omega]
        check('matched_totals_%s_%s'%(mode,omega),abs(a['H0']-b['H0'])<1e-13 and
              abs(a['J0']-b['J0'])<1e-13 and np.linalg.norm(np.array(a['P0'])-b['P0'])<1e-13)
    refined=run_cell('pair_w.5_j.05_tight',.05,.5,'pair',tight=True)
    base=cells[0]
    for radius in RADII:
        key=str(radius)
        check('refined_counts_'+key,base['cuts'][key]['inward']==refined['cuts'][key]['inward']
              and base['cuts'][key]['outward']==refined['cuts'][key]['outward'])
    check('refined_spin',abs(base['omega_final']-refined['omega_final'])<1e-5)
    asymmetric=run_cell('recoil_asymmetric',.3,.5,'pair',T=4,asymmetric=True)
    check('recoil_exercised',asymmetric['max_body_displacement']>1e-4)
    mutation=run_cell('wrong_torque',.3,.5,'pair',T=4,asymmetric=True,mutate=True)
    result=dict(base_revision='add3cae0a',model=dict(G=G,M=M,a=A,soft=SOFT,I=I,
                eta=ETA,r_initial=R0,E_initial=E0,radii=RADII.tolist()),cells=cells,
                refined=refined,asymmetric=asymmetric,mutation=mutation,
                checks=CHECKS,assertions=len(CHECKS),passed=sum(c['passed'] for c in CHECKS))
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(assertions=result['assertions'],passed=result['passed'])))
    if result['assertions']!=result['passed']:
        print(json.dumps([c for c in CHECKS if not c['passed']],indent=2))
        raise SystemExit(1)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True)
    main(p.parse_args().output)
