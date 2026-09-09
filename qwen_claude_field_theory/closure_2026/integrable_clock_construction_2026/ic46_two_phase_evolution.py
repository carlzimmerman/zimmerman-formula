"""Nonlinear finite-patch evolution with independently diagnosed phase joining.

No momentum or canonical interface projection. Three auxiliary fields solve
the bulk constraints and six specified boundary conditions at each RK stage.
The omitted w_r/interface conditions are diagnostics, not assumed successes.
Endpoint canonical fields use one-sided collocation evolution; this is a
local numerical probe, not a globally well-posed cosmological boundary problem.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import mpmath as mp
import numpy as np
from scipy.optimize import root
import sympy as s
import ic30_radial_bridge as radial
import ic32_constraint_preservation as old
import ic37_local_taylor as local
import ic45_unpinned_angular as angular


def grid(nodes,left,right):
    if nodes<5:raise ValueError('At least five collocation nodes')
    x=(left+right)/2+(right-left)*(-np.cos(np.pi*np.arange(nodes)/(nodes-1)))/2
    weights=(-1.)**np.arange(nodes);weights[[0,-1]]*=.5
    delta=x[:,None]-x[None,:];np.fill_diagonal(delta,1.)
    D=weights[None,:]/weights[:,None]/delta;np.fill_diagonal(D,0.)
    np.fill_diagonal(D,-np.sum(D,axis=1))
    return x,D


@lru_cache(None)
def gravity():
    d=radial.radial_action();r=d['r'];S,w,Q,q,z,sh,beta,ell=d['fields']
    L=d['L'].subs(ell,0)
    C=-radial.euler(L,S,r)/d['J'];W=radial.euler(L,w,r)/d['J']
    fields=s.symbols('S w Q q z shear beta',real=True)
    grads=s.symbols('S_r w_r Q_r q_r z_r shear_r beta_r',real=True)
    seconds=s.symbols('S_rr w_rr Q_rr q_rr z_rr shear_rr beta_rr',real=True)
    actual=d['fields'][:-1]
    mapping={**dict(zip(actual,fields)),**dict(zip([s.diff(f,r) for f in actual],grads)),
             **dict(zip([s.diff(f,r,2) for f in actual],seconds))}
    C,W=C.xreplace(mapping),W.xreplace(mapping)
    flow=angular.derive()
    A,D,D1,E=s.symbols('A D D1 E',real=True);Sf=fields[0]
    coefficients={s.Function('A')(Sf):A,s.Derivative(s.Function('A')(Sf),Sf):0,
        s.Function('D')(Sf):D,s.Derivative(s.Function('D')(Sf),Sf):D1,
        s.Function('E4')(Sf):E,s.Derivative(s.Function('E4')(Sf),Sf):0}
    expressions=[v.subs(coefficients,simultaneous=True) for v in
                 [C,W,flow['Q_flow'],flow['q_flow'],flow['shear_flow']]]
    args=(r,*fields,*grads,*seconds,d['m'],d['a02'],d['lam'],d['kappa'],A,D,D1,E)
    return s.lambdify(args,expressions,'numpy',cse=True)


def physical_fluid(j,g,S,w,Q,wc,f):
    cp=f['c']*np.exp(-(1-3*f['w'])*wc)
    out=old.fluid(np.exp(-3*w)*j,g,S+w,Q+w,f['w'],cp)
    return dict(h=np.exp(3*w)*out['h'],pw=np.exp(3*w)*out['pw'],
                v=out['v'],error=out['legendre_error'],j=j,g=g)


def matter_control():
    j=np.array([.2,1.,3.]);g=np.array([0.,.01,.1]);S=.03;Q=-.01;wc=-.025
    errors=[]
    for wf in (.001,1/3):
        f=dict(w=wf,c=.7);a=physical_fluid(j,g,S,wc,Q,wc,f);b=old.fluid(j,g,S,Q,wf,f['c'])
        errors.extend([np.max(abs(a[k]-b[k])) for k in ('h','pw')])
        errors.append(np.max(abs(np.exp(wc)*a['v']-b['v'])))
    return float(max(errors))


class Evolution:
    def __init__(self,nodes=9,width=3e-5):
        self.nodes=nodes;self.width=width;self.calls=0;self.root_calls=0
        folder=Path(__file__).parent
        p=json.loads((folder/'ic41_run_001/response80/stdout.txt').read_text())['input_parameters']
        boundary=json.loads((folder/'ic45_run_001/compatible60/stdout.txt').read_text())['result']
        with mp.workdps(60):
            m=local.LocalJet(p['U0'],p['U1']);m.initial[1]=mp.mpf(p['Sprime']);m.initial[7]=mp.mpf(p['qprime'])
            Y=local.ode_series(m.rhs,m.r0,m.initial,max(10,nodes+1))
            self.coeff=np.array([[float(v) for v in row] for row in Y])
            self.fluids=[{k:float(f[k]) for k in ('w','c','j')} for f in m.fluids]
            self.cell=(float(m.knots[0]),float(m.knots[1]));self.model=m.ref.model
        self.nf=len(self.fluids);self.count=3+2*self.nf
        self.offset=[];self.D=[]
        for lo,hi in ((-1.,0.),(0.,1.)):
            x,D=grid(nodes,lo,hi);self.offset.append(width*x);self.D.append(D/width)
        self.A=[np.array(boundary[k],float) for k in ('inactive_S_tt_coefficients','active_S_tt_coefficients')]
        self.B=np.array(boundary['inactive_w_tt_coefficients'],float)
        F=[];guess=[]
        for side,x in enumerate(self.offset):
            vals=np.array([self.poly(row,x) for row in self.coeff]);fields=[vals[2],vals[6],vals[4]]
            fields.extend(np.full(nodes,np.log(f['j'])) for f in self.fluids)
            fields.extend(np.zeros(nodes) for _ in self.fluids);F.append(fields);guess.append(vals[0])
        self.initial=np.r_[np.array(F).ravel(),2.]
        self.guess=np.r_[guess[0],np.full(nodes,self.model.wc),guess[1]]
        self.fn=gravity()

    @staticmethod
    def poly(coeff,x):return np.polynomial.polynomial.polyval(x,coeff)

    def fields(self,y):return y[:-1].reshape(2,self.count,self.nodes),float(y[-1])

    def derivative(self,side,value,order=1):
        D=self.D[side]
        # Subtract the constant component before differentiation to reduce
        # cancellation from 1/width^2 on nearly constant metric fields.
        result=D@(value-value[0])
        return result if order==1 else D@result

    def evaluate(self,side,F,R,S,w,beta=None,bp=None):
        m=self.model;n=self.nodes;r=R+self.offset[side];Q,q,sh=F[:3]
        if np.min(S)<=self.cell[0] or np.max(S)>=self.cell[1]:raise ValueError('Leaves fixed coefficient cell')
        u=(S+2*w)/(S+w)
        if np.any(u*u>=1) or np.min(abs(S+w))<1e-8:raise ValueError('Leaves real regular constitutive chart')
        Dc=m.table(S);D1=m.table(S,nu=1)
        if np.min(Dc)<=0:raise ValueError('Leaves monotone z branch')
        z=2*np.sqrt(Dc/(6*m.E))*np.sinh(np.arcsinh(-3*m.A*q*np.sqrt(6*m.E/Dc)/(4*Dc))/3)
        first=[self.derivative(side,v) for v in (S,w,Q,q,z,sh)]
        second=[self.derivative(side,v,2) for v in (S,w,Q,q,z,sh)]
        beta=np.zeros(n) if beta is None else beta;bp=np.zeros(n) if bp is None else bp
        values=self.fn(r,S,w,Q,q,z,sh,beta,*first,bp,*second,np.zeros(n),
                       m.m,m.a02,m.lam,m.kappa,m.A,Dc,D1,m.E)
        out={k:np.broadcast_to(v,(n,)).copy() for k,v in zip(('C','W','Qdot','qdot','shdot'),values)}
        fluids=[physical_fluid(np.exp(F[3+i]),F[3+self.nf+i],S,w,Q,m.wc,f) for i,f in enumerate(self.fluids)]
        out['C']+=sum(f['h'] for f in fluids);out['W']-=sum(f['pw'] for f in fluids)
        return dict(**out,fluids=fluids,r=r,z=z,first=first,
                    tau=2*np.exp(S-2*w)/m.m)

    def boundary(self,time,R):
        xs=[R+self.offset[0][0]-2,R+self.offset[1][-1]-2]
        S=[self.poly(self.coeff[0],x)+time*self.poly(self.coeff[8],x)+time*time*self.poly(self.A[i],x)/2 for i,x in enumerate(xs)]
        return S[0],self.model.wc+time*time*self.poly(self.B,xs[0])/2,S[1]

    def auxiliary(self,F,R,time):
        n=self.nodes;eps=self.width;Sin,win,Sout=self.boundary(time,R)
        def evaluate(g,details=False):
            Sm,wm,Sp=g[:n],g[n:2*n],g[2*n:];wp=np.full(n,self.model.wc)
            a=self.evaluate(0,F[0],R,Sm,wm);b=self.evaluate(1,F[1],R,Sp,wp)
            res=np.r_[eps**2*a['C'][1:-1],eps**2*a['W'][1:-1],eps**2*b['C'][1:-1],
                      Sm[0]-Sin,wm[0]-win,Sp[-1]-Sout,Sm[-1]-Sp[0],
                      eps*(a['first'][0][-1]-b['first'][0][0]),wm[-1]-self.model.wc]
            return (res,[(Sm,wm,a),(Sp,wp,b)]) if details else res
        self.root_calls+=1
        result=root(evaluate,self.guess,method='hybr',options=dict(xtol=1e-10,maxfev=300,eps=1e-12))
        res,states=evaluate(result.x,True);norm=float(np.max(abs(res)))
        if not np.isfinite(norm) or norm>2e-12:raise RuntimeError(f'Auxiliary solve residual {norm:.6g}: {result.message}')
        self.guess=result.x.copy()
        return states,norm

    def rhs(self,y,time):
        self.calls+=1;F,R=self.fields(y);states,auxerr=self.auxiliary(F,R,time)
        deriv=[];data=[]
        for side,(S,w,v) in enumerate(states):
            r=v['r'];sh=F[side,2];lo,hi=((-1.,0.) if side==0 else (0.,1.))
            x=self.offset[side]/self.width
            source=-v['tau']*sh/r
            coef=np.polynomial.polynomial.polyfit(x,source,self.nodes-1)
            anti=np.polynomial.polynomial.polyint(coef)*self.width
            beta=r*(self.poly(anti,x)-self.poly(anti,0.))
            bp=beta/r-v['tau']*sh
            v=self.evaluate(side,F[side],R,S,w,beta,bp);Qd=v['Qdot'];qd=v['qdot'];sd=v['shdot']
            Q=F[side,0];J=r*r*np.exp(3*Q);logs=[];grads=[]
            for fluid in v['fluids']:
                j,g,vf=fluid['j'],fluid['g'],fluid['v']
                pressure=j*np.exp(S+w)*vf-fluid['h']
                anis=np.exp(S-2*Q-w)*j*g*g/(2*vf)
                qd+=3*pressure/2+anis;sd+=anis
                flux=J*j*(beta+np.exp(S-2*Q-w)*g/vf)
                logs.append(self.derivative(side,flux)/(J*j)-3*Qd)
                grads.append(self.derivative(side,np.exp(S+w)*vf+beta*g))
            deriv.append(np.array([Qd,qd,sd,*logs,*grads]))
            mom=2*v['first'][3]/3+4*v['first'][5]/3+4*(v['first'][2]+1/r)*F[side,2]
            mom-=sum(f['j']*f['g'] for f in v['fluids'])
            data.append(dict(S=S,w=w,v=v,momentum=mom,beta=beta,bp=bp))
        slope=data[1]['v']['first'][3][0]
        if abs(slope)<1e-8:raise ValueError('Active interface lost transversal q gradient')
        speed=-deriv[1][1,0]/slope
        for side in range(2):
            deriv[side]+=speed*np.array([self.derivative(side,f) for f in F[side]])
        a,b=data;edge=lambda x,y:float(x[-1]-y[0])
        Vm,Vp=a['v'],b['v'];reaction=-Vp['W'][0]
        diagnostics=dict(time=time,R=R,Rdot=float(speed),auxiliary_scaled_residual=auxerr,
            lapse_max=float(max(np.max(abs(Vm['C'])),np.max(abs(Vp['C'])))),
            inactive_clock_max=float(np.max(abs(Vm['W']))),
            momentum_max=float(max(np.max(abs(a['momentum'])),np.max(abs(b['momentum'])))),
            w_r_interface=float(Vm['first'][1][-1]),q_interface_jump=edge(F[0,1],F[1,1]),
            Q_interface_jump=edge(F[0,0],F[1,0]),shear_interface_jump=edge(F[0,2],F[1,2]),
            physical_lapse_gradient_jump=edge(Vm['first'][0]+Vm['first'][1],Vp['first'][0]+Vp['first'][1]),
            physical_spatial_gradient_jump=edge(-Vm['first'][2]-Vm['first'][1],-Vp['first'][2]-Vp['first'][1]),
            active_clock_reaction=float(reaction),
            conditional_q_gradient_jump_residual=edge(Vm['first'][3],Vp['first'][3])+float(reaction/(2*speed)),
            fluid_legendre_max=float(max(np.max(abs(f['error'])) for d in data for f in d['v']['fluids'])),
            shift_derivative_max=float(max(np.max(abs(self.derivative(i,d['beta'])-d['bp'])) for i,d in enumerate(data))),
            activation_off_max=float(np.max((np.exp(-3*a['w'])*F[0,1]/(1.5*self.model.m))**2-.5)),
            activation_on_min=float(np.min((np.exp(-3*b['w'])*F[1,1]/(1.5*self.model.m))**2-.5)))
        return np.r_[np.array(deriv).ravel(),speed],diagnostics


def experiment(nodes=9,width=3e-5,dt=1e-8,steps=4):
    e=Evolution(nodes,width);y=e.initial.copy();rows=[];i=0
    try:
        for i in range(steps+1):
            k1,diag=e.rhs(y,i*dt);rows.append(diag)
            if i==steps:break
            k2,_=e.rhs(y+dt*k1/2,(i+.5)*dt)
            k3,_=e.rhs(y+dt*k2/2,(i+.5)*dt)
            k4,_=e.rhs(y+dt*k3,(i+1)*dt)
            y+=dt*(k1+2*k2+2*k3+k4)/6
        completed=True;reason=''
    except (ValueError,RuntimeError,np.linalg.LinAlgError) as error:
        completed=False;reason=str(error)
    return dict(completed=completed,reason=reason,completed_steps=i,nodes=nodes,width=width,dt=dt,requested_steps=steps,
        rhs_calls=e.calls,auxiliary_solves=e.root_calls,rows=rows,final_state=y.tolist(),
        junction_projected=False,momentum_projected=False,full_theory='OPEN',
        scope='Nonlinear finite-patch probe with prescribed auxiliary endpoint data and one-sided canonical endpoint evolution; not global well-posedness or empirical closure')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--nodes',type=int,default=9);p.add_argument('--width',type=float,default=3e-5)
    p.add_argument('--dt',type=float,default=1e-8);p.add_argument('--steps',type=int,default=4);p.add_argument('--strict',action='store_true')
    a=vars(p.parse_args());strict=a.pop('strict');result=experiment(**a)
    print(json.dumps(result,indent=2));raise SystemExit(2 if strict else 0 if result['completed'] else 1)
