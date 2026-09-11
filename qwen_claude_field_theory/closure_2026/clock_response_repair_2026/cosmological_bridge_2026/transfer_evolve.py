#!/usr/bin/env python3
"""Frozen-action finite-k transfer, NOT a CMB Boltzmann calculation.

Integrates all six initial scalar/matter basis modes. Checks the ORIGINAL
eight Euler equations with independently differenced reconstructed fields.
No Phi=Psi assignment, coefficient reconstruction, or particle CDM.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import numpy as np
import sympy as sy
from scipy.integrate import solve_ivp
from scipy.optimize import root
from background_evolve import Model, system_functions
from derive import construct
from transfer_jets import extra_jets

FIELDS=('z','e','sigma','rad','theta','drho','n','b')
ALIASES=dict(P='P',PX='P_X',PXX='P_XX',PXXX='P_XXX',Pt='P_t',
             Ptt='P_tt',PXt='P_Xt',PXXt='P_XXt',PXtt='P_Xtt',
             V='V',Vt='V_t',Vtt='V_tt',W='W',Wt='W_t',WY='W_Y',WYt='W_Yt')


class Background:
    def __init__(self,tend):
        self.model=Model(.2,gamma=1e-6)
        self.names,self.fun=system_functions()
        bg=self.model.background(0.)
        def constraints(x):return self.evaluate([1.,x[0],x[1],0.,.001,.01])[2][:2]
        initial=root(constraints,[bg['H'],bg['q']],tol=1e-11)
        if not initial.success or max(abs(constraints(initial.x)))>1e-11:
            raise RuntimeError('initial sourced constraints did not solve')
        y0=np.array([1.,*initial.x,0.,.001,.01])
        self.solution=solve_ivp(self.rhs,[0.,tend],y0,method='DOP853',
                                rtol=2e-12,atol=2e-14,dense_output=True)
        if not self.solution.success:raise RuntimeError(self.solution.message)

    def evaluate(self,state,extended=False):
        a,H,q,tau,rho,rad=state
        if a<=0 or rho<=0 or rad<=0:raise ValueError('background domain lost')
        jets=self.model.jets(float(tau),q*q,0.)
        if extended:jets.update(extra_jets(self.model,float(tau),q*q))
        v={key:float(jets[value]) for key,value in ALIASES.items() if value in jets}
        v.update(a=a,H=H,q=q,M2=1.,Lambda=.7,gamma=self.model.gamma,
                 rho=rho,Cr=1.,qr=(rad/3.)**.25)
        out=np.asarray(self.fun(*[v[key] for key in self.names]),dtype=float)
        mat=out[:9].reshape(3,3);forcing=out[9:12]
        Hd,qd,sbar=np.linalg.solve(mat,forcing)
        if not np.all(np.isfinite([Hd,qd,sbar])) or sbar<=0:
            raise ValueError('timelike clock/background solve failed')
        v.update(Hd=Hd,qd=qd,sbar=sbar,qrd=-H*v['qr'],rhod=-3*H*rho)
        return v,mat,out[12:],float(jets['domain_denominator'])

    def rhs(self,t,y):
        v,_,_,_=self.evaluate(y)
        return [y[0]*y[1],v['Hd'],v['qd'],v['sbar'],-3*y[1]*y[4],-4*y[1]*y[5]]

    @lru_cache(maxsize=1024)
    def at(self,t):
        return self.evaluate(self.solution.sol(t),extended=True)


def mode_system(v,k):
    """The 4x4 solve from FIRST_ORDER_HANDOFF, with all coefficient rates."""
    a,H,q,m,g,qr,rho,Cr=(v[x] for x in ('a','H','q','M2','gamma','qr','rho','Cr'))
    Hd,qd,s0,PX,PXX,PXt,W,WY=(v[x] for x in
        ('Hd','qd','sbar','PX','PXX','PXt','W','WY'))
    if W==0:raise ValueError('clock reduction requires nonzero W')
    p=k*k/(a*a);pd=-2*H*p;Wd=s0*v['Wt'];WYd=s0*v['WYt']
    PXd=s0*PXt+2*q*qd*PXX
    PXXd=s0*v['PXXt']+2*q*qd*v['PXXX']
    PXtd=s0*v['PXtt']+2*q*qd*v['PXXt']
    B=2*PX+4*q*q*PXX;Bd=2*PXd+8*q*qd*PXX+4*q*q*PXXd
    j=2*q*PX-6*g*H*q*q
    jd=2*qd*PX+2*q*PXd-6*g*Hd*q*q-12*g*H*q*qd
    jr=4*Cr*qr**3;jrd=12*Cr*qr*qr*v['qrd']
    R=12*Cr*qr*qr;Rd=24*Cr*qr*v['qrd']
    F=2*q*PXt/W;Fd=2*(qd*PXt+q*PXtd)/W-F*Wd/W
    G=-2*q*WY*p/W
    Gd=-2*(qd*WY*p+q*WYd*p+q*WY*pd)/W-G*Wd/W
    A=B-12*g*H*q-2*g*q*q*F
    Ad=Bd-12*g*(Hd*q+H*qd)-4*g*q*qd*F-2*g*q*q*Fd
    C=-2*g*q*q*G-2*g*q*p
    Cd=-4*g*q*qd*G-2*g*q*q*Gd-2*g*(qd*p+q*pd)
    Z=-2*PX+2*s0*WY+2*g*(qd+3*H*q)
    Rv=q*B-18*g*H*q*q-2*g*q**3*F
    Rs=-2*g*q**3*G-2*g*q*q*p
    Pv=2*q*PX+4*g*q*qd;Vp=s0*W+2*g*q*q*qd
    matrix=np.array([[A,0.,0.,q*C-jd],[0.,R,0.,-jrd],
                     [0.,0.,1.,-v['rhod']],
                     [F+3*g*q*q/m,0.,0.,q*G-3*Hd+p-3*Vp/(2*m)]])
    source=np.array([
        [Cd+3*H*C+j*G-p*Z,Ad+C+3*H*A+j*F+2*g*q*p,0,0,0,0],
        [jr*G,jr*F,4*Cr*qr*qr*p,Rd+3*H*R,0,0],
        [rho*G,rho*F,0,0,rho*p,3*H],
        [Gd+2*H*G+Rs/(2*m),Fd+G+2*H*F+(Rv+3*Pv)/(2*m),
         0,12*Cr*qr**3/m,0,1/(2*m)]])
    solved=np.linalg.solve(matrix,-source)
    lapse=solved[3];operator=np.zeros((6,6))
    operator[0]=q*lapse;operator[0,1]+=1.
    operator[1]=solved[0]
    operator[2]=qr*lapse;operator[2,3]+=1.
    operator[3]=solved[1];operator[4]=lapse;operator[5]=solved[2]
    Krow=np.array([G,F,0,0,0,0])
    Jrow=np.array([j,2*g*q*q,jr,0,rho,0])
    density=np.array([Rs,Rv,0,12*Cr*qr**3,0,1])
    zrow=(density-2*m*H*Krow)/(2*m*p)
    brow=-(Krow+3*Jrow/(2*m))/k
    if not np.all(np.isfinite(operator)):raise ValueError('nonfinite transfer operator')
    return operator,matrix,lapse,zrow,brow,Jrow


@lru_cache(maxsize=1)
def original_euler_operator():
    """Unmodified action-derived Euler equations, independent of the reduction."""
    d=construct();v=d['s']
    fields=[v[f+suffix] for f in FIELDS for suffix in ('','d','dd')]
    matrix,constant=sy.linear_eq_to_matrix([d['euler'][f] for f in FIELDS],fields)
    if any(x!=0 for x in constant):raise AssertionError('unexpected affine perturbation EL')
    parameters=sorted(matrix.free_symbols,key=str)
    return [str(x) for x in parameters],sy.lambdify(parameters,matrix,'numpy',cse=True)


def metric_fields(bg,sol,k,t):
    v=bg.at(float(t))[0];u=sol.sol(t).reshape(6,6)
    _,_,lapse,zrow,brow,Jrow=mode_system(v,k)
    return np.array([zrow@u,np.zeros(6),u[0],u[2],u[4],u[5],lapse@u,brow@u]),Jrow@u


def diagnose(bg,sol,k,tend,step):
    names,fn=original_euler_operator()
    maximum=np.zeros(8);max_mom=max_slip=0.;potentials=[]
    for t in np.linspace(.2*tend,.8*tend,7):
        sampled=[metric_fields(bg,sol,k,float(t+j*step))[0] for j in (-2,-1,0,1,2)]
        fm2,fm,f,fp,fp2=sampled
        fd=(fm2-8*fm+8*fp-fp2)/(12*step)
        fdd=(-fp2+16*fp-30*f+16*fm-fm2)/(12*step*step)
        jets=np.stack([f,fd,fdd],axis=1).reshape(24,6)
        v=bg.at(float(t))[0];v=dict(v,k=k)
        matrix=np.asarray(fn(*[v[x] for x in names]),dtype=float)
        residual=matrix@jets
        scaled=abs(residual)/(1+abs(matrix)@abs(jets))
        maximum=np.maximum(maximum,np.max(scaled,axis=1))
        J=metric_fields(bg,sol,k,float(t))[1]
        momentum=2*v['M2']*(fd[0]-v['H']*f[6])+J
        max_mom=max(max_mom,float(max(abs(momentum)/
            (1+abs(2*v['M2']*fd[0])+abs(2*v['M2']*v['H']*f[6])+abs(J)))))
        shear=-v['a']**2*f[7]/k
        shear_rate=-v['a']**2*(fd[7]+2*v['H']*f[7])/k
        Phi=f[6]+shear_rate;Psi=-f[0]-v['H']*shear
        max_slip=max(max_slip,float(max(abs(Phi-Psi)/(1+abs(Phi)+abs(Psi)))))
        potentials.append(dict(t=float(t),Phi=Phi.tolist(),Psi=Psi.tolist()))
    return dict(step=step,max_scaled_euler=float(max(maximum)),
                euler_by_field=dict(zip(FIELDS,maximum.tolist())),
                max_scaled_momentum=max_mom,max_scaled_slip=max_slip,potentials=potentials)


def evolve(ks=(.3,3.,30.),tend=.02,rtol=2e-10):
    if not ks or any(not np.isfinite(k) or k<=0 for k in ks):
        raise ValueError('finite-k evolution requires strictly positive wavenumbers')
    if not (0<tend<=.05):raise ValueError('bounded test requires 0<tend<=0.05')
    if not (0<rtol<1):raise ValueError('rtol must be between zero and one')
    bg=Background(tend);rows=[];max_constraint=0.
    for t in np.linspace(0,tend,17):
        v,mat,c,margin=bg.at(float(t));max_constraint=max(max_constraint,float(max(abs(c[:2]))))
        rows.append(dict(t=float(t),a=float(v['a']),H=float(v['H']),
                         tau=float(bg.solution.sol(t)[3]),clock_rate=float(v['sbar']),
                         determinant=float(np.linalg.det(mat)),condition=float(np.linalg.cond(mat)),
                         domain_margin=margin))
    modes=[]
    for k in ks:
        def rhs(t,flat):return (mode_system(bg.at(float(t))[0],k)[0]@flat.reshape(6,6)).ravel()
        sol=solve_ivp(rhs,[0,tend],np.eye(6).ravel(),method='DOP853',
                      rtol=rtol,atol=rtol*.01,dense_output=True)
        if not sol.success:raise RuntimeError(sol.message)
        samples=[]
        for t in np.linspace(0,tend,17):
            _,matrix,*_=mode_system(bg.at(float(t))[0],k)
            samples.append(dict(t=float(t),determinant=float(np.linalg.det(matrix)),
                                condition=float(np.linalg.cond(matrix))))
        diagnostics=[diagnose(bg,sol,k,tend,tend/divisor) for divisor in (20,40)]
        modes.append(dict(k=k,transfer_end=sol.y[:,-1].reshape(6,6).tolist(),
                          nfev=sol.nfev,matrix_samples=samples,diagnostics=diagnostics))
    result=dict(background=rows,max_background_constraint=max_constraint,modes=modes,
                initial_basis=['sigma','deltaQ','radiation_field','deltaQr','dust_velocity','delta_rho_b'],
                parameters=dict(tend=tend,rtol=rtol,atol=rtol*.01,gamma=1e-6),
                scope='Six-basis linear transfer on short fixed-action sourced history; perfect-fluid radiation, NOT primordial or CMB spectra',
                scaling='abs(Euler residual)/(1+sum(abs(each linear term))); all six normalized initial basis columns',
                full_theory_status='OPEN')
    if max_constraint>1e-9:raise AssertionError('background constraints drifted')
    for mode in modes:
        for d in mode['diagnostics']:
            if d['max_scaled_euler']>3e-6 or max(d['max_scaled_momentum'],d['max_scaled_slip'])>1e-6:
                raise AssertionError('uneliminated metric/Euler checks failed: '+str(d))
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path,required=True)
    parser.add_argument('--ks',type=float,nargs='+',default=[.3,3.,30.])
    parser.add_argument('--tend',type=float,default=.02);parser.add_argument('--rtol',type=float,default=2e-10)
    args=parser.parse_args();result=evolve(tuple(args.ks),args.tend,args.rtol)
    args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(full_theory_status='OPEN',
        max_background_constraint=result['max_background_constraint'],
        modes=[dict(k=m['k'],nfev=m['nfev'],max_scaled_euler=max(d['max_scaled_euler'] for d in m['diagnostics']),
                    max_scaled_momentum=max(d['max_scaled_momentum'] for d in m['diagnostics']),
                    max_scaled_slip=max(d['max_scaled_slip'] for d in m['diagnostics']))
               for m in result['modes']]),indent=2))
