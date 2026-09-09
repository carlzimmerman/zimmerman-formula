"""Second time-jet compatibility, not a full-theory certification.

Physical accelerations are directional derivatives of IC33 Hamiltonian flow.
Only the lapse acceleration is solved for. Initial ell=elldot=ellddot=0 is
a restricted family, not a necessary ansatz for every mixed-branch solution.
"""
import argparse
import json
import numpy as np
import sympy as s
from numpy.polynomial import Chebyshev
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar
import ic35_switch_collar as previous
import ic32_constraint_preservation as base
import ic33_full_metric_evolution as metric


def identities():
    r,tau=s.symbols('r tau',real=True)
    Q,S,beta,H,Hd,jd,gd=(s.Function(n)(r) for n in ('Q','S','beta','H','Hd','jd','gd'))
    j,v=s.symbols('j v',positive=True)
    density=j+tau*jd; gradient=tau*gd; expansion=H+tau*Hd
    J=r*r*s.exp(3*Q)
    equation=beta*s.diff(density,r)-3*expansion*density
    equation+=s.diff(J*s.exp(S-2*Q)*density*gradient/v,r)/J
    actual=s.diff(equation,tau).subs(tau,0)
    expected=matter_second(j,jd,s.diff(jd,r),beta,H,Hd,s.diff(Q,r),s.diff(S,r),
                           r,s.exp(S-2*Q)/v,gd,s.diff(gd,r))
    # Metric/lapse/velocity variations in the flux multiply g=0 at this order.
    Qd,Ud,vd=(s.Function(n)(r) for n in ('Qd','Ud','vd'))
    Jt=r*r*s.exp(3*(Q+tau*Qd))
    flux=s.diff(Jt*s.exp(S+tau*Ud-2*(Q+tau*Qd))*density*gradient/(v+tau*vd),r)/Jt
    fullflux=s.diff(flux,tau).subs(tau,0)
    frozenflux=s.diff(s.diff(J*s.exp(S-2*Q)*density*gradient/v,r)/J,tau).subs(tau,0)
    return {'canonical_density_second_jet':s.simplify(actual-expected),
            'zero_gradient_flux_variations':s.simplify(fullflux-frozenflux)}


def grid(lo,hi,nodes):
    r=(lo+hi)/2-(hi-lo)*np.cos(np.linspace(0,np.pi,nodes))/2
    # Use the exact integrated float endpoints, not rounded recombinations.
    r[0]=lo;r[-1]=hi
    return r


def fit(r,values,degree):
    """Subtract the constant before fitting to protect small spatial variations."""
    offset=float(np.mean(values))
    p=Chebyshev.fit(r,np.asarray(values)-offset,min(degree,len(r)-1))
    p.coef[0]+=offset
    return p


def matter_second(j,jdot,jdot1,beta,HQ,HQdot,Q1,S1,r,flux_factor,gdot,gdot1):
    """At initially uniform j and zero fluid gradient, from canonical flux.

    jdot=beta*j' - 3HQ*j + J^-1 (J e^(S-2Q) j g/v)'.
    flux_factor=e^(S-2Q)/v on this initial slice; J=r^2 exp(3Q).
    """
    return beta*jdot1-3*HQdot*j-3*HQ*jdot+j*flux_factor*(gdot1+(2/r+Q1+S1)*gdot)


def compatibility(r,C,W,FC,FW,degree):
    """Solve LC A=-FC, then test LW A=-FW without imposing boundary A data.

    C,W have columns (zeroth, first, second spatial derivative coefficients).
    Free homogeneous constants are fitted to W; no physical momentum is fitted.
    """
    lo,hi=float(r[0]),float(r[-1]); center=(lo+hi)/2; length=hi-lo
    polys=[fit(r,x,degree) for x in (*C.T,FC)]
    def rhs(x,y):
        a,b,c,f=(p(x) for p in polys)
        Y=y.reshape(2,3)
        acc=-(a*Y[0]+b*Y[1]+np.array([f,0.,0.]))/c
        return np.array([Y[1],acc]).ravel()
    initial=np.array([[0.,1.,0.],[0.,0.,1/length]]).ravel()
    sols=[solve_ivp(rhs,(center,end),initial,method='DOP853',rtol=2e-11,
                    atol=2e-12,max_step=length/100,dense_output=True) for end in (lo,hi)]
    if not all(sol.success for sol in sols):raise RuntimeError('Lapse-acceleration IVP failed')
    Y=np.where(r<=center,sols[0].sol(r),sols[1].sol(r)).reshape(2,3,len(r))
    A,A1=Y; A2=-(C[:,0]*A+C[:,1]*A1+np.array([FC,np.zeros_like(FC),np.zeros_like(FC)]))/C[:,2]
    residual=(W[:,0]*A+W[:,1]*A1+W[:,2]*A2).T
    source=residual[:,0]+FW; matrix=residual[:,1:]
    # Scale columns, report actual singular values, and use a declared cutoff.
    scale=np.linalg.norm(matrix,axis=0)
    if np.any(scale==0):scale=np.where(scale==0,1.,scale)
    normalized=matrix/scale
    coef,_,rank,sv=np.linalg.lstsq(normalized,-source,rcond=1e-11)
    coef=coef/scale
    defect=source+matrix@coef
    solution=A[0]+coef@A[1:]
    solution1=A1[0]+coef@A1[1:]
    solution2=A2[0]+coef@A2[1:]
    return dict(max_W_residual=float(np.max(abs(defect))),
        rms_W_residual=float(np.sqrt(np.mean(defect**2))),
        W_source_scale=float(max(1.,np.max(abs(source)))),
        relative_W_residual=float(np.max(abs(defect))/max(1.,np.max(abs(source)))),
        homogeneous_rank=int(rank),normalized_singular_values=sv.tolist(),
        homogeneous_coefficients=coef.tolist(),
        lapse_acceleration_range=[float(np.min(solution)),float(np.max(solution))],
        lapse_acceleration=solution,lapse_acceleration1=solution1,lapse_acceleration2=solution2,
        W_residual=defect,W_residual_samples=defect[[0,len(r)//2,-1]].tolist())


class FirstJet:
    def __init__(self,width=.006,slope=-100.,U0=0.,U1=0.):
        self.c=previous.Collar(width); m=self.c.model; self.center=self.c.r0; self.width=width
        qcrit=-3*m.m*.5*np.exp(3*m.wc)/np.sqrt(2)
        initial=np.r_[self.c.initial,qcrit,slope,U0,U1]
        self.sols=[solve_ivp(self.rhs,(self.center,end),initial,method='DOP853',
            rtol=1e-11,atol=1e-13,max_step=width/160,dense_output=True)
            for end in (self.center-width/2,self.center+width/2)]
        if not all(sol.success for sol in self.sols):raise RuntimeError('IC35 initial collar failed')

    def rhs(self,r,state):
        q,q1,U,U1=state[6:]
        p=previous.preservation_coefficients(self.c,r,state[:6],q,q1)
        c0,c1,c2,cf=p['C'];w0,w1,w2,wf=p['W']
        matrix=np.array([[c2,p['CQ2']*p['gamma']],[w2,p['WQ2']*p['gamma']]],dtype=float)
        U2,q2=np.linalg.solve(matrix,-np.array([c0*U+c1*U1+cf,w0*U+w1*U1+wf]))
        return np.r_[p['spatial'],q1,q2,U1,U2]

    def field(self,r):
        r=np.asarray(r)
        if np.min(r)<self.center-self.width/2 or np.max(r)>self.center+self.width/2:
            raise ValueError('No dense-solution extrapolation')
        return np.where(r<=self.center,self.sols[0].sol(r),self.sols[1].sol(r))

    def evaluate(self,r,jets):
        m=self.c.model; v=jets; D=m.table(v['S'])
        z=2*np.sqrt(D/(6*m.E))*np.sinh(np.arcsinh(-3*m.A*v['q']*np.sqrt(6*m.E/D)/(4*D))/3)
        eq=base.evaluate(m,r,*(v[k] for k in ('S','S1','S2','Q','Q1','Q2','q')),z,v['sh'])
        flow=metric.evaluate(m,r,*(v[k] for k in ('S','S1','S2','Q','Q1','Q2','q','q1')),
            z,*(v[k] for k in ('sh','sh1','beta','beta1')))
        C=eq['C'].copy(); W=eq['W'].copy(); qd=flow['qdot'].copy(); sd=flow['shdot'].copy()
        for i,f in enumerate(self.c.fluids):
            j,g=v['j'+str(i)],v['g'+str(i)]
            fm=base.fluid(j,g,v['S'],v['Q'],f['w'],f['c'])
            C+=fm['h']; W-=fm['pw']
            pressure=j*np.exp(v['S'])*fm['v']-fm['h']
            anis=np.exp(v['S']-2*v['Q'])*j*g*g/(2*fm['v'])
            qd+=3*pressure/2+anis; sd+=anis
        return dict(C=C,W=W,Qdot=flow['Qdot'],qdot=qd,shdot=sd,z=z,eq=eq)

    def sample(self,degree=12,nodes=65,interval=None):
        lo,hi=(self.center-self.width/2,self.center+self.width/2) if interval is None else interval
        # Sorted Chebyshev-Lobatto audit points; polynomial fit degree is lower.
        r=grid(lo,hi,nodes)
        y=self.field(r); dy=np.column_stack([self.rhs(x,v) for x,v in zip(r,y.T)])
        v=dict(S=y[0],S1=y[1],S2=dy[1],Q=y[2],Q1=y[3],Q2=dy[3],
               q=y[6],q1=y[7],sh=y[4],sh1=dy[4],beta=y[5],beta1=dy[5])
        for i,f in enumerate(self.c.fluids):
            v['j'+str(i)]=np.full(nodes,f['j']);v['g'+str(i)]=np.zeros(nodes)
        initial=self.evaluate(r,v); m=self.c.model; t=2*np.exp(v['S']-2*m.wc)/m.m
        HQ=-t*v['q']/6-m.A*initial['z']/2
        p=[previous.preservation_coefficients(self.c,x,a[:6],a[6],a[7],b[7])
           for x,a,b in zip(r,y.T,dy.T)]
        time=dict(S=y[8],S1=y[9],S2=dy[9],Q=initial['Qdot'],
                  Q1=np.array([a['Qdot1'] for a in p]),Q2=np.array([a['Qdot2'] for a in p]),
                  q=initial['qdot'],sh=initial['shdot'])
        for k in ('q','sh'):time[k+'1']=fit(r,time[k],degree).deriv()(r)
        # Differentiate beta'-beta/r=-t sh. Set beta_dot at this audit
        # interval's midpoint to zero; no polynomial extrapolation is needed.
        anti=fit(r,t*(time['sh']+v['sh']*time['S'])/r,degree).integ()
        time['beta']=-r*(anti(r)-anti((r[0]+r[-1])/2))
        time['beta1']=time['beta']/r-t*(time['sh']+v['sh']*time['S'])
        for i,f in enumerate(self.c.fluids):
            time['j'+str(i)]=-3*HQ*f['j']
            time['g'+str(i)]=np.exp(v['S'])*(1+f['w'])*f['c']*f['j']**f['w']*v['S1']
        C=np.array([a['C'][:3] for a in p],dtype=float)
        W=np.array([a['W'][:3] for a in p],dtype=float)
        return r,v,time,initial,HQ,C,W

    def experiment(self,degree=12,nodes=65,step=1e-3,acceleration_step=1e-4,interval=None):
        r,v,time,initial,HQ,C,W=self.sample(degree,nodes,interval); m=self.c.model
        def kick(eps,acc=None):
            return {k:value+eps*time[k]+(0 if acc is None else eps*eps*acc.get(k,0.)/2)
                    for k,value in v.items()}
        plus=self.evaluate(r,kick(acceleration_step)); minus=self.evaluate(r,kick(-acceleration_step))
        acc={k:(plus[k+'dot']-minus[k+'dot'])/(2*acceleration_step) for k in ('Q','q','sh')}
        for k in ('Q','q','sh'):
            polynomial=fit(r,acc[k],degree)
            acc[k+'1']=polynomial.deriv()(r)
            if k=='Q':acc['Q2']=polynomial.deriv(2)(r)
        eq=initial['eq']; zd=-(eq['hSz']*time['S']+eq['hqz']*time['q'])/eq['hzz']
        t=2*np.exp(v['S']-2*m.wc)/m.m
        HQd=-t*(time['S']*v['q']+time['q'])/6-m.A*zd/2
        for i,f in enumerate(self.c.fluids):
            jd=time['j'+str(i)]; gd=time['g'+str(i)]
            vf=(1+f['w'])*f['c']*f['j']**f['w']
            acc['j'+str(i)]=matter_second(f['j'],jd,fit(r,jd,degree).deriv()(r),v['beta'],
                HQ,HQd,v['Q1'],v['S1'],r,np.exp(v['S']-2*v['Q'])/vf,gd,fit(r,gd,degree).deriv()(r))
            # gddot is unnecessary in Cddot/Wddot because H_g=0 initially.
        fp=self.evaluate(r,kick(step,acc)); fm=self.evaluate(r,kick(-step,acc))
        FC=(fp['C']+fm['C']-2*initial['C'])/step**2
        FW=(fp['W']+fm['W']-2*initial['W'])/step**2
        result=compatibility(r,C,W,FC,FW,degree)
        acc.update(S=result.pop('lapse_acceleration'),S1=result.pop('lapse_acceleration1'),
                   S2=result.pop('lapse_acceleration2'))
        expected=result.pop('W_residual')
        cp=self.evaluate(r,kick(step,acc)); cm=self.evaluate(r,kick(-step,acc))
        correctedC=(cp['C']+cm['C']-2*initial['C'])/step**2
        correctedW=(cp['W']+cm['W']-2*initial['W'])/step**2
        cells=np.searchsorted(m.table.x,v['S'],side='right')-1
        crossing=sum(np.count_nonzero((np.searchsorted(m.table.x,v['S']+sign*step*time['S'],side='right')-1)!=cells)
                     for sign in (-1,1))
        corrected_crossing=sum(np.count_nonzero((np.searchsorted(m.table.x,kick(sign*step,acc)['S'],side='right')-1)!=cells)
                              for sign in (-1,1))
        first=[sum(initial['eq'][key+'_'+k]*time[k] for k in ('S','S1','S2','Q','Q1','Q2','q','sh'))
               +initial['eq'][key+'_z']*zd for key in ('C','W')]
        for i,f in enumerate(self.c.fluids):
            h=f['h']*np.exp(v['S']-m.Sref)
            hd=h*(time['S']+(1+f['w'])*time['j'+str(i)]/f['j'])
            first[0]+=hd;first[1]-=(1-3*f['w'])*hd
        momentum=2*time['q1']/3+4*time['sh1']/3+4*(v['Q1']+1/r)*time['sh']+4*time['Q1']*v['sh']
        momentum-=sum(v['j'+str(i)]*time['g'+str(i)] for i in range(len(self.c.fluids)))
        return dict(degree=degree,nodes=nodes,step=step,acceleration_step=acceleration_step,
            interval=[float(r[0]),float(r[-1])],initial_constraint=float(max(np.max(abs(initial[k])) for k in ('C','W'))),
            first_preservation=float(max(np.max(abs(x)) for x in first)),
            independent_momentum_first=float(np.max(abs(momentum))),
            Qdot_second_fit_error=float(np.max(abs(fit(r,time['Q'],degree).deriv(2)(r)-time['Q2']))),
            C_second_source_range=[float(np.min(FC)),float(np.max(FC))],
            W_second_source_range=[float(np.min(FW)),float(np.max(FW))],
            corrected_C_second=float(np.max(abs(correctedC))),
            corrected_W_second=float(np.max(abs(correctedW))),
            independent_second_response_error=float(np.max(abs(correctedW-expected))),
            coefficient_cells=np.unique(cells).tolist(),time_kick_cell_crossings=int(crossing),
            corrected_kick_cell_crossings=int(corrected_crossing),
            activation_square_range=[float(np.min((-np.exp(-3*m.wc)*v['q']/(3*m.m*.5))**2)),
                                     float(np.max((-np.exp(-3*m.wc)*v['q']/(3*m.m*.5))**2))],
            status='SECOND-JET DIAGNOSTIC ONLY',full_theory='OPEN',**result)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--strict',action='store_true')
    parser.add_argument('--quick',action='store_true');parser.add_argument('--scan',action='store_true');args=parser.parse_args()
    model=FirstJet()
    runs=[(10,1e-3,1e-4)] if args.quick else [(8,1e-4,1e-4),(12,1e-4,1e-4),
        (16,1e-4,1e-4),(12,2e-4,1e-4),(12,5e-5,1e-4),(12,1e-4,5e-5)]
    rows=[model.experiment(degree=d,step=h,acceleration_step=a) for d,h,a in runs]
    scans=[]
    if args.scan:
        for U1 in (-100.,-10.,10.,100.):
            try:
                candidate=FirstJet(U1=U1)
                scans.append(dict(U1=U1,**candidate.experiment(degree=12,step=5e-5)))
            except (ValueError,RuntimeError,np.linalg.LinAlgError) as error:
                scans.append(dict(U1=U1,error=str(error),full_theory='OPEN'))
        # A smaller one-sided interval checks that the mismatch is not merely
        # a global fit across a C2 coefficient knot. No physical endpoints inferred.
        for interval in ((1.9972,1.999),(2.001,2.0028)):
            scans.append(dict(local_interval=True,**model.experiment(degree=8,step=5e-5,interval=interval)))
    optimized=[]
    if args.scan:
        for bounds in ((-10.,0.),(0.,10.)):
            history=[]
            def objective(U1):
                candidate=FirstJet(U1=U1)
                report=candidate.experiment(degree=8,nodes=33,step=5e-5)
                history.append(dict(U1=float(U1),rms=report['rms_W_residual']))
                return report['rms_W_residual']
            opt=minimize_scalar(objective,bounds=bounds,method='bounded',options={'xatol':1e-3,'maxiter':18})
            candidate=FirstJet(U1=float(opt.x))
            audit=[candidate.experiment(degree=d,nodes=65,step=h,acceleration_step=a)
                   for d,h,a in ((8,5e-5,1e-4),(12,5e-5,1e-4),(12,2.5e-5,5e-5))]
            optimized.append(dict(bounds=bounds,U1=float(opt.x),optimizer_success=bool(opt.success),
                                  evaluations=history,independent_resolution_audits=audit))
    checks={k:v==0 for k,v in identities().items()}
    checks['initial_constraints']=all(row['initial_constraint']<1e-8 for row in rows)
    checks['first_preservation']=all(row['first_preservation']<1e-7 for row in rows)
    print(json.dumps(dict(checks=checks,rows=rows,scans=scans,optimized=optimized,full_theory='OPEN'),indent=2))
    return 1 if not all(checks.values()) else 2 if args.strict else 0


if __name__=='__main__':raise SystemExit(main())
