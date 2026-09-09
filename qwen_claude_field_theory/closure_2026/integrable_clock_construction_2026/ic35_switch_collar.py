"""Finite-multiplier initial collar across the actual IC29 activation switch.

Local initial constraints, not a time-evolved or static matched MOND galaxy.
The second-jet matrix is varied from the action; it is NOT a Poisson matrix.
"""
import argparse
from functools import lru_cache
import json
import mpmath as mp
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp
import ic30_radial_bridge as radial
import ic32_constraint_preservation as base
import ic33_full_metric_evolution as metric


@lru_cache(None)
def symbolic():
    d=radial.radial_action(); r=d['r']
    S,w,Q,q,z,sh,beta,ell=d['fields']; eq=radial.radial_equations()
    # Keep eta and its derivatives through variation; ell=0 removes the pin force.
    def finite(expr):return s.simplify(expr.subs(ell,0).doit().subs(w,d['wc']).doit())
    C=finite(-eq['S']/d['J']); W=finite(eq['w']/d['J'])
    matrix=s.Matrix([[s.diff(expr,s.diff(f,r,2)) for f in (S,Q)] for expr in (C,W)]).applyfunc(s.factor)
    vp=d['v'].subs(w,d['wc']); u=d['u'].subs(w,d['wc'])
    determinant=s.factor(matrix.det())
    # Closed expression is checked against the actual differentiated matrix.
    checks={'principal_determinant':s.simplify(determinant-16*vp**2*u**2*s.exp(-4*Q)),
            'C_independent_of_activation':s.simplify(C-C.subs(d['eta'],1).doit()),
            'W_independent_of_activation':s.simplify(W-W.subs(d['eta'],1).doit()),
            'multiplier_equation':s.simplify(eq['ell'].subs(w,d['wc']).doit())}
    q2=s.Symbol('qsecond',real=True)
    Fz=2*d['D']+12*d['E4']*z*z
    # The q'' terms in HQ'' and beta'''/3, with the differentiated momentum
    # constraint sh''=-q''/2+terms independent of q'', and z''=-A q''/Fz+... .
    coefficient=s.diff(-d['t']*q2/6-d['A']*(-d['A']*q2/Fz)/2-d['t']*(-q2/2)/3,q2)
    gamma=d['A']**2/(2*Fz)
    checks['Qdot_second_profile_coefficient']=s.simplify(coefficient-gamma)
    joint=matrix*s.diag(1,coefficient)
    checks['first_preservation_principal']=s.simplify(joint.det()-gamma*determinant)
    atzero=matrix.subs(S,-2*d['wc']).doit()
    # Rank is actually computed; no DOF number is inferred from it.
    return checks,matrix,determinant,atzero.rank()


def identities():return symbolic()[0]


class Collar:
    def __init__(self,width=.01):
        if width<=0:raise ValueError('Positive collar width')
        self.width=width;self.r0=2.;self.model=base.hermite.repair(base.exterior.models()[1])
        m=self.model
        self.initial=np.array([(m.table.x[0]+m.table.x[-1])/2,0.,m.Q,0.,0.,0.])
        # Positive canonical fluid densities stay fixed only on this initial slice.
        # Their momentum density is zero initially, not at all later times.
        with mp.workdps(40):
            original=base.exterior.history.initial('-1000','.5')
            entries=base.exterior.history.base.matter.matter(mp.mpf(m.Sref),mp.mpf(m.Q),original['fluids'])
        self.fluids=[{k:float(f[k]) for k in ('w','c','j','h')} for f in entries]

    def profile(self,r):
        x=np.clip((np.asarray(r)-self.r0)/self.width,0.,1.)
        f=x**4*(35-84*x+70*x*x-20*x**3)
        return self.model.q*f,self.model.q*140*x**3*(1-x)**3/self.width

    def evaluate(self,r,y,S2=0.,Q2=0.,qjets=None):
        m=self.model; S,S1,Q,Q1,sh,beta=y
        q,q1=self.profile(r) if qjets is None else qjets
        D=m.table(S)
        if np.any(D<=0):raise ValueError('Nonconvex auxiliary branch')
        z=2*np.sqrt(D/(6*m.E))*np.sinh(np.arcsinh(-3*m.A*q*np.sqrt(6*m.E/D)/(4*D))/3)
        out=base.evaluate(m,r,S,S1,S2,Q,Q1,Q2,q,z,sh)
        hs=[f['h']*np.exp(S-m.Sref) for f in self.fluids]
        rho=sum(hs); pw=sum((1-3*f['w'])*h for f,h in zip(self.fluids,hs))
        out.update(C_total=out['C']+rho,W_total=out['W']-pw,z=z,q=q,q1=q1,
                   rho=rho,pressure=sum(f['w']*h for f,h in zip(self.fluids,hs)),
                   t=2*np.exp(S-2*m.wc)/m.m)
        return out

    def rhs(self,r,y,qjets=None):
        S,S1,Q,Q1,sh,beta=y; v=self.evaluate(r,y,qjets=qjets)
        M=np.array([[v['C_S2'],v['C_Q2']],[v['W_S2'],v['W_Q2']]],dtype=float)
        S2,Q2=np.linalg.solve(M,-np.array([v['C_total'],v['W_total']]))
        sh1=-v['q1']/2-3*(Q1+1/r)*sh
        bp=beta/r-v['t']*sh
        return np.array([S1,S2,Q1,Q2,sh1,bp],dtype=float)

    def solve(self,max_step_fraction=1/100):
        return solve_ivp(self.rhs,(self.r0,self.r0+self.width),self.initial,
            method='DOP853',rtol=1e-11,atol=1e-13,max_step=self.width*max_step_fraction,dense_output=True)


def experiment(width=.01,nodes=401):
    model=Collar(width); m=model.model
    try:
        sol=model.solve()
        if not sol.success:return dict(success=False,reason=sol.message)
    except (ValueError,RuntimeError,np.linalg.LinAlgError) as error:
        return dict(success=False,reason=str(error),width=width)
    r=np.linspace(model.r0,model.r0+width,nodes)
    y=sol.sol(r); S,S1,Q,Q1,sh,beta=y
    rhs=np.column_stack([model.rhs(x,z) for x,z in zip(r,y.T)])
    direct=model.evaluate(r,y,rhs[1],rhs[3])
    # Independently differentiate the integrated dense interpolant.
    h=width/(3*nodes); points=r[1:-1]
    derivative=(-sol.sol(points+2*h)+8*sol.sol(points+h)-8*sol.sol(points-h)+sol.sol(points-2*h))/(12*h)
    values=sol.sol(points)
    expected=np.column_stack([model.rhs(x,z) for x,z in zip(points,values.T)])
    fd=model.evaluate(points,values,derivative[1],derivative[3])
    mom=2*fd['q1']/3+4*derivative[4]/3+4*(values[3]+1/points)*values[4]
    gauge=derivative[5]-values[5]/points+fd['t']*values[4]
    matrix=np.stack([np.stack([direct['C_S2'],direct['C_Q2']],axis=-1),
                     np.stack([direct['W_S2'],direct['W_Q2']],axis=-1)],axis=-2)
    sv=np.linalg.svd(matrix,compute_uv=False)
    q,q1=model.profile(r)
    square=(-np.exp(-3*m.wc)*q/(3*m.m*.5))**2
    positive_logs=[]
    with mp.workdps(50):
        for arg2 in square:
            if .5<arg2<.75:
                eta=base.exterior.history.base.old.normalized.legacy.activation(mp.sqrt(mp.mpf(arg2)))
                positive_logs.append(float(mp.log10(eta)))
    flow=metric.evaluate(m,r,S,S1,rhs[1],Q,Q1,rhs[3],q,q1,direct['z'],sh,rhs[4],beta,rhs[5])
    flow['qdot']=flow['qdot']+3*direct['pressure']/2
    return dict(success=True,width=width,nodes=nodes,nfev=sol.nfev,
        S_range=[float(np.min(S)),float(np.max(S))],Q_range=[float(np.min(Q)),float(np.max(Q))],
        shear_range=[float(np.min(sh)),float(np.max(sh))],
        activation_square_range=[float(np.min(square)),float(np.max(square))],
        transition_log10_eta_range=[min(positive_logs),max(positive_logs)] if positive_logs else [],
        max_ode_residual=float(np.max(abs(derivative-expected))),
        independent_constraint_residuals=dict(lapse=float(np.max(abs(fd['C_total']))),
            w=float(np.max(abs(fd['W_total']))),momentum=float(np.max(abs(mom))),
            shear_gauge=float(np.max(abs(gauge)))),
        max_auxiliary_residual=float(max(np.max(abs(direct['C_total'])),np.max(abs(direct['W_total'])),
            np.max(abs(m.A*q+2*m.table(S)*direct['z']+4*m.E*direct['z']**3)))),
        min_second_jet_singular_value=float(np.min(sv)),
        principal_determinant_range=[float(np.min(np.linalg.det(matrix))),float(np.max(np.linalg.det(matrix)))],
        initial_multiplier=0.,qdot_range=[float(np.min(flow['qdot'])),float(np.max(flow['qdot']))],
        shdot_range=[float(np.min(flow['shdot'])),float(np.max(flow['shdot']))],
        time_extension='NOT ESTABLISHED',full_theory='OPEN')



def preservation_coefficients(collar,r,y,q,q1,q2=0.):
    """Exact field-jet chain rule; no interpolation of Qdot'' sources."""
    m=collar.model; S,S1,Q,Q1,sh,beta=y
    spatial=collar.rhs(r,y,(q,q1)); S2,Q2,sh1,bp=spatial[1],spatial[3],spatial[4],spatial[5]
    v=collar.evaluate(r,y,S2,Q2,(q,q1))
    D,D1,D2=(m.table(S,nu=i) for i in range(3)); z=v['z']; t=v['t']
    Fz=2*D+12*m.E*z*z
    z1=-(m.A*q1+2*D1*S1*z)/Fz
    z2=-(m.A*q2+2*(D2*S1*S1+D1*S2)*z+4*D1*S1*z1+24*m.E*z*z1*z1)/Fz
    M=np.array([[v['C_S2'],v['C_Q2']],[v['W_S2'],v['W_Q2']]],dtype=float)
    spatial_jets=dict(S=S1,S1=S2,Q=Q1,Q1=Q2,q=q1,z=z1,sh=sh1)
    c3=sum(v['C_'+k]*value for k,value in spatial_jets.items())+v['rho']*S1
    w3=sum(v['W_'+k]*value for k,value in spatial_jets.items())
    hs=[f['h']*np.exp(S-m.Sref) for f in collar.fluids]
    pw=sum((1-3*f['w'])*h for f,h in zip(collar.fluids,hs))
    pwent=sum((1-3*f['w'])*(1+f['w'])*h for f,h in zip(collar.fluids,hs))
    ent=sum((1+f['w'])*h for f,h in zip(collar.fluids,hs))
    c3-=2*(v['C_S2']*S1+v['C_Q2']*Q1)/r**2
    w3-=2*(v['W_S2']*S1+v['W_Q2']*Q1)/r**2+pw*S1
    S3,Q3=np.linalg.solve(M,-np.array([c3,w3],dtype=float))
    sh2=-q2/2-3*(Q2-1/r**2)*sh-3*(Q1+1/r)*sh1
    bp2=bp/r-beta/r**2-t*(S1*sh+sh1)
    bp3=bp2/r-2*bp/r**2+2*beta/r**3-t*((S2+S1*S1)*sh+2*S1*sh1+sh2)
    HQ=-t*q/6-m.A*z/2
    HQ1=-t*(S1*q+q1)/6-m.A*z1/2
    HQ2=-t*((S2+S1*S1)*q+2*S1*q1+q2)/6-m.A*z2/2
    Qdot1=HQ1+bp*Q1+beta*Q2+(bp2+2*bp/r-2*beta/r**2)/3
    Qdot2=HQ2+bp2*Q1+2*bp*Q2+beta*Q3+(bp3+2*bp2/r-4*bp/r**2+4*beta/r**3)/3
    flow=metric.evaluate(m,r,S,S1,S2,Q,Q1,Q2,q,q1,z,sh,sh1,beta,bp)
    qdot=flow['qdot']+3*v['pressure']/2; shdot=flow['shdot']
    jets=dict(Q=flow['Qdot'],Q1=Qdot1,Q2=Qdot2,q=qdot,sh=shdot)
    Cf=sum(v['C_'+k]*value for k,value in jets.items())-v['C_z']*v['hqz']*qdot/v['hzz']-3*HQ*ent
    Wf=sum(v['W_'+k]*value for k,value in jets.items())-v['W_z']*v['hqz']*qdot/v['hzz']+3*HQ*pwent
    c0=v['C_S']-v['C_z']*v['hSz']/v['hzz']+v['rho']
    w0=v['W_S']-v['W_z']*v['hSz']/v['hzz']-pw
    return dict(spatial=spatial,C=(c0,v['C_S1'],v['C_S2'],Cf),
                W=(w0,v['W_S1'],v['W_S2'],Wf),gamma=m.A*m.A/(2*Fz),
                CQ2=v['C_Q2'],WQ2=v['W_Q2'],Qdot2=Qdot2,
                qdot=qdot,shdot=shdot,Qdot1=Qdot1,ent=ent)


def integrable_collar(width=.002,nodes=401,slope=-100.,Sd0=0.):
    """Solve spatial constraints AND first time preservation for the profile.

    q is no longer a prescribed smoothstep. Its second spatial derivative is
    determined jointly with Sdot'' by Cdot=Wdot=0 at ell=elldot=0.
    """
    c=Collar(width);m=c.model; center=c.r0
    qcrit=-3*m.m*.5*np.exp(3*m.wc)/np.sqrt(2)
    y0=np.r_[c.initial,qcrit,slope,Sd0,0.]
    def rhs(r,y):
        state=y[:6]; q,q1,Sd,Sd1=y[6:]
        p=preservation_coefficients(c,r,state,q,q1)
        C0,C1,C2,Cf=p['C'];W0,W1,W2,Wf=p['W'];g=p['gamma']
        K=np.array([[C2,p['CQ2']*g],[W2,p['WQ2']*g]],dtype=float)
        Sd2,q2=np.linalg.solve(K,-np.array([C0*Sd+C1*Sd1+Cf,W0*Sd+W1*Sd1+Wf],dtype=float))
        return np.r_[p['spatial'],q1,q2,Sd1,Sd2]
    try:
        left=solve_ivp(rhs,(center,center-width/2),y0,method='DOP853',rtol=1e-10,atol=1e-12,
                       max_step=width/160,dense_output=True)
        right=solve_ivp(rhs,(center,center+width/2),y0,method='DOP853',rtol=1e-10,atol=1e-12,
                        max_step=width/160,dense_output=True)
        if not left.success or not right.success:return dict(success=False,reason=left.message+'; '+right.message)
        def field(x):
            x=np.asarray(x); a=left.sol(x); b=right.sol(x)
            return np.where(x<=center,a,b)
        r=np.linspace(center-width/2,center+width/2,nodes)
        y=field(r); derivatives=np.column_stack([rhs(x,z) for x,z in zip(r,y.T)])
        errors=[]; gamma_errors=[]; moment=[]; matrices=[]
        h=width/(4*nodes); points=r[1:-1]
        fd=(-field(points+2*h)+8*field(points+h)-8*field(points-h)+field(points-2*h))/(12*h)
        exact=np.column_stack([rhs(x,z) for x,z in zip(points,field(points).T)])
        relative=float(np.max(abs(fd-exact)/np.maximum(1,abs(exact))))
        initial_errors=[]
        for i,(x,state) in enumerate(zip(points,field(points).T)):
            v=c.evaluate(x,state[:6],fd[1,i],fd[3,i],(state[6],state[7]))
            initial_errors.extend([float(v['C_total']),float(v['W_total']),
                float(2*fd[6,i]/3+4*fd[4,i]/3+4*(state[3]+1/x)*state[4]),
                float(fd[5,i]-state[5]/x+v['t']*state[4])])
        for x,state,deriv in zip(r,y.T,derivatives.T):
            p=preservation_coefficients(c,x,state[:6],state[6],state[7],deriv[7])
            for key in ('C','W'):
                v0,v1,v2,f=p[key];errors.append(float(v0*state[8]+v1*state[9]+v2*deriv[9]+f))
            p0=preservation_coefficients(c,x,state[:6],state[6],state[7],0.)
            p1=preservation_coefficients(c,x,state[:6],state[6],state[7],1.)
            gamma_errors.append(float(p1['Qdot2']-p0['Qdot2']-p0['gamma']))
            matrices.append([[p0['C'][2],p0['CQ2']*p0['gamma']],
                             [p0['W'][2],p0['WQ2']*p0['gamma']]])
        # Independent spatial differentiation of actual full-metric time rates.
        def velocities(x):
            states=field(x)
            ps=[preservation_coefficients(c,a,z[:6],z[6],z[7]) for a,z in zip(x,states.T)]
            return np.array([[p['qdot'],p['shdot']] for p in ps],dtype=float).T
        vd=(-velocities(points+2*h)+8*velocities(points+h)-8*velocities(points-h)+velocities(points-2*h))/(12*h)
        for i,(x,state) in enumerate(zip(points,field(points).T)):
            p=preservation_coefficients(c,x,state[:6],state[6],state[7])
            moment.append(float(2*vd[0,i]/3+4*vd[1,i]/3+4*(state[3]+1/x)*p['shdot']
                          +4*p['Qdot1']*state[4]-p['ent']*state[1]))
        square=(-np.exp(-3*m.wc)*y[6]/(3*m.m*.5))**2
        sv=np.linalg.svd(np.array(matrices,dtype=float),compute_uv=False)
        return dict(success=True,width=width,nodes=nodes,slope=slope,Sdot_initial=Sd0,
            nfev=left.nfev+right.nfev,max_relative_ode_residual=relative,
            max_independent_initial_constraint=max(abs(x) for x in initial_errors),
            max_first_preservation_residual=max(abs(x) for x in errors),
            max_Qdot2_coefficient_error=max(abs(x) for x in gamma_errors),
            max_independent_momentum_preservation=max(abs(x) for x in moment),
            min_preservation_singular_value=float(np.min(sv)),
            activation_square_range=[float(np.min(square)),float(np.max(square))],
            S_range=[float(np.min(y[0])),float(np.max(y[0]))],
            q_range=[float(np.min(y[6])),float(np.max(y[6]))],
            Sdot_range=[float(np.min(y[8])),float(np.max(y[8]))],
            qsecond_range=[float(np.min(derivatives[7])),float(np.max(derivatives[7]))],
            multiplier=0.,multiplier_first_time_derivative=0.,
            time_extension='FIRST PRESERVATION ONLY',full_theory='OPEN')
    except (ValueError,RuntimeError,np.linalg.LinAlgError) as error:
        return dict(success=False,width=width,reason=str(error),full_theory='OPEN')


def main():
    p=argparse.ArgumentParser();p.add_argument('--strict',action='store_true');args=p.parse_args()
    checks={k:v==0 for k,v in identities().items()}
    rows=[experiment(w,n) for w,n in ((.01,401),(.01,801),(.02,801))]
    joined=[integrable_collar(w,n) for w,n in ((.002,401),(.002,801),(.004,801),(.006,801))]
    checks['initial_collars']=all(r['success'] and r['max_ode_residual']<1e-5
        and r['max_auxiliary_residual']<1e-8 and r['activation_square_range'][0]<.5
        and r['activation_square_range'][1]>.75 for r in rows)
    checks['first_preservation']=all(r['success'] and r['max_relative_ode_residual']<1e-5
        and r['max_first_preservation_residual']<1e-7
        and r['max_independent_initial_constraint']<1e-6
        and r['max_independent_momentum_preservation']<1e-5
        and r['activation_square_range'][0]<.5 and r['activation_square_range'][1]>.5 for r in joined)
    checks['reaches_active_plateau']=joined[-1]['success'] and joined[-1]['activation_square_range'][1]>.75
    print(json.dumps(dict(checks=checks,principal_matrix=str(symbolic()[1]),
        principal_determinant=str(symbolic()[2]),formal_u0_rank=symbolic()[3],
        rows=rows,first_preservation_collars=joined,full_theory='OPEN'),indent=2))
    return 1 if not all(checks.values()) else 2 if args.strict else 0


if __name__=='__main__':
    raise SystemExit(main())
