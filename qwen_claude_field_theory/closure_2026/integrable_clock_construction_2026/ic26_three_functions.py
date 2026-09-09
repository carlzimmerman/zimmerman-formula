#!/usr/bin/env python3
"""Joint A,D,E4 action reconstruction with independently controlled lapse Schur.

All targets are design inputs. Actual raw action variation computes outputs.
"""
import argparse
import json
import mpmath as mp
import numpy as np
import sympy as s
from scipy.integrate import DOP853,solve_ivp
from scipy.interpolate import CubicSpline
from functools import lru_cache
import ic25_coupled as base
prior=base.prior
model=base.model


def initial(target_M='-.03'):
    b=base.initial(profile='charge');b['EE']=model.coefficient_jets(b['S'],b['parameters'])['e'][0]
    b['target_M']=mp.mpf(target_M)
    if b['target_M']>=0:raise ValueError('Negative auxiliary Schur target required')
    return b


def first_jets(b,alpha,beta,App=0,Epp=0):
    S,q,z,Q=b['S'],b['q'],b['z'],b['Q']
    jets=model.coefficient_jets(S,b['parameters'])
    jets['a']=[b['AA'],mp.mpf(alpha),mp.mpf(App)]
    jets['e']=[b['EE'],mp.mpf(beta),mp.mpf(Epp)];jets['d']=[mp.mpf(0)]*3
    r=model.raw_jets(S,q,z,0,jets);jets['d'][0]=r['z']/(2*z)
    total=mp.fsum(x['h'] for x in prior.matter(S,Q,b['fluids']))
    r=model.raw_jets(S,q,z,0,jets);jets['d'][1]=(r['S']+total)/z**2
    return jets


def trial(b,alpha,App=0,Epp=0):
    S,q,z,Q=b['S'],b['q'],b['z'],b['Q'];alpha=mp.mpf(alpha)
    pin=model.normalized.legacy.activation(-mp.exp(-3*model.normalized.constants()['wc'])*q/3)
    if pin<=0:raise ValueError('Inactive pin stratum')
    jets=first_jets(b,alpha,0,App,Epp)
    r=model.raw_jets(S,q,z,0,jets);entries=prior.matter(S,Q,b['fluids'])
    enthalpy=mp.fsum((1+x['w'])*x['h'] for x in entries)
    pressure=mp.fsum(x['w']*x['h'] for x in entries);total=mp.fsum(x['h'] for x in entries)
    qdot=-mp.mpf(3)/2*(r['h']-pressure);HQ=r['q']/2;sd=base.clock_slope(b)*HQ
    C0=r['Sq']-r['Sz']*r['qz']/r['zz'];Cb=2*z**3*r['qz']/r['zz']
    if Cb*qdot==0:raise ValueError('Degenerate third-coefficient control equation')
    target_C=(-b['target_M']*sd+3*HQ*enthalpy)/qdot
    beta=(target_C-C0)/Cb
    jets=first_jets(b,alpha,beta,App,Epp);r=model.raw_jets(S,q,z,0,jets)
    jets['d'][2]=(r['SS']+total-r['Sz']**2/r['zz']-b['target_M'])/z**2
    row=prior.fixed_state(S,q,z,Q,b['parameters'],b['fluids'],jets)
    row.update(AA=b['AA'],EE=b['EE'],alpha=alpha,beta=beta,kappa=b['kappa'],target=b['target'],
               profile=b['profile'],target_M=b['target_M'],pin_activation=pin)
    return row


def control(b):
    y0,yp,ym=[trial(b,x)['principal']['gravity_diagonal'] for x in (0,1,-1)]
    a=(yp+ym)/2-y0;c=(yp-ym)/2;d=y0-b['target'];disc=c*c-4*a*d
    if disc<0:raise ValueError('No real causal slope on this control branch')
    if a==0:
        if c==0:raise ValueError('Degenerate causal slope equation')
        alpha=-d/c
    else:alpha=(-c-mp.sqrt(disc))/(2*a)
    r=trial(b,alpha);r['discriminant']=disc
    return r


def moved(b,dt):
    r=base.moved(b,dt);r['EE']=b['EE']+dt*b['beta']*b['flow'][0]
    return r


def completed(b):
    r=control(b);sd=r['flow'][0]
    if sd==0:raise ValueError('Stationary S requires a separate limiting analysis')
    App=mp.diff(lambda dt:control(moved(r,dt))['alpha'],0)/sd
    Epp=mp.diff(lambda dt:control(moved(r,dt))['beta'],0)/sd
    out=trial(b,r['alpha'],App,Epp);out['discriminant']=r['discriminant']
    return out


def integrability(r):
    def point(dt):return completed(moved(r,dt))
    sd=r['flow'][0]
    return dict(Aprime_dot=mp.diff(lambda dt:point(dt)['alpha'],0)-r['jets']['a'][2]*sd,
        Eprime_dot=mp.diff(lambda dt:point(dt)['beta'],0)-r['jets']['e'][2]*sd,
        D_dot=mp.diff(lambda dt:point(dt)['jets']['d'][0],0)-r['jets']['d'][1]*sd,
        Dprime_dot=mp.diff(lambda dt:point(dt)['jets']['d'][1],0)-r['jets']['d'][2]*sd,
        charge_dot=mp.diff(lambda dt:point(dt)['charge'],0))


def homogeneous_audit():
    h,hq,hqq,q,HQ,qd,pH,zeta,p,zd=s.symbols('h hq hqq q HQ qd pH zeta p zd')
    # Expansion of V exp(3zeta)[2(q+p)(HQ+zetadot)-h(q+p)].
    lag2=2*p*zd+6*q*zeta*zd+(6*HQ-3*hq)*p*zeta+(9*HQ*q-s.Rational(9,2)*h)*zeta**2-hqq*p*p/2
    lag2=lag2-6*q*zeta*zd-3*(qd+3*HQ*q)*zeta**2
    lag2=s.expand(lag2.subs({HQ:hq/2,qd:-s.Rational(3,2)*(h-pH)}))
    expected=2*p*zd-hqq*p*p/2-s.Rational(9,2)*pH*zeta*zeta
    w,hi,j,si=s.symbols('w hi j si',nonzero=True)
    matter=hi*s.exp(-3*w*zeta)*(1+si/j)**(1+w)
    beta=s.symbols('beta');pz,zz,z,C0=s.symbols('pz zz z C0',nonzero=True)
    shifted_C=C0+2*z**3*pz*beta/zz
    return dict(gravity_background_mass_cancellation=s.factor(lag2-expected),
        matter_cross=s.factor(s.diff(matter,zeta,si).subs({zeta:0,si:0})+3*w*(1+w)*hi/j),
        matter_mass=s.factor(s.diff(matter,zeta,2).subs({zeta:0,si:0})/2-s.Rational(9,2)*w*w*hi),
        combined_mass=s.factor(s.Rational(9,2)*(w*hi+w*w*hi)-s.Rational(9,2)*w*(1+w)*hi),
        third_coefficient_constraint_slope=s.diff(shifted_C,beta)-2*z**3*pz/zz)


def evolve(target_Q=1,max_step=.005,rtol=1e-10,max_steps=2000,target_M='-.03'):
    with mp.workdps(30):
        b0=initial(target_M);S0=b0['S']
        def row(Q,y):
            b=dict(b0);b.update(Q=mp.mpf(Q),S=S0+base.clock_offset(b0,mp.mpf(Q)))
            b['q'],b['z'],b['AA'],b['EE']=map(mp.mpf,y)
            return control(b)
        def rhs(Q,y):
            r=row(Q,y);slope=base.clock_slope(r)
            return [float(r['flow'][1]/r['Qdot']),float(r['flow'][2]/r['Qdot']),float(r['alpha']*slope),float(r['beta']*slope)]
        y0=[float(b0[x]) for x in ('q','z','AA','EE')]
        solver=DOP853(rhs,0,y0,float(target_Q),rtol=rtol,atol=rtol*.001,max_step=max_step)
        rows=[row(0,y0)];success=True;reason='requested endpoint reached'
        def health(r):return min(r['EE'],-r['M'],-r['raw']['zz'],r['a'],r['jets']['d'][0],
            r['principal']['gradient_margin'],r['principal']['lightcone_margin'],r['pin_activation'],r['H_physical'])
        for _ in range(max_steps):
            if solver.status!='running':break
            try:
                solver.step()
                if solver.status=='failed':success=False;reason='adaptive integration failure';break
                r=row(solver.t,solver.y);rows.append(r)
                if health(r)<=0:success=False;reason='accepted state violates regular or causal design domain';break
            except (ValueError,ZeroDivisionError) as error:
                success=False;reason='unaccepted stage failed: '+str(error);break
        else:success=False;reason='step budget reached'
        states=[]
        for r in rows:
            x=prior.snapshot(r);x.update(A=float(r['AA']),E4=float(r['EE']),Aprime=float(r['alpha']),Eprime=float(r['beta']),
                pin_activation=float(r['pin_activation']),discriminant=float(r['discriminant']))
            states.append(x)
        return dict(success=success,reason=reason,Q_end=states[-1]['Q'],requested_Q=target_Q,states=states,
            max_step=max_step,rtol=rtol,nfev=solver.nfev,target_M=target_M,minimum_health_margin=float(min(health(r) for r in rows)),
            maximum_charge_drift=float(max(abs(r['charge']-rows[0]['charge']) for r in rows)),
            maximum_schur_error=float(max(abs(r['M']-r['target_M']) for r in rows)),
            maximum_cone_target_error=float(max(abs(r['principal']['gravity_diagonal']-r['target']) for r in rows)))


def completed_at(history,Q):
    b=initial(history['target_M']);states=history['states'];times=[x['Q'] for x in states]
    y=CubicSpline(times,[[x['q'],x['z'],x['A'],x['E4']] for x in states])(float(Q))
    b.update(Q=mp.mpf(Q),S=b['S']+base.clock_offset(b,mp.mpf(Q)))
    b['q'],b['z'],b['AA'],b['EE']=map(mp.mpf,y)
    return completed(b)


def frequencies(b,k_squared):
    thirds={name:mp.diff(lambda dt:completed(moved(b,dt))['jets'][name][2],0)/b['flow'][0] for name in ('a','d','e')}
    k2=mp.mpf(k_squared);quad=prior.quadratic(b,k2);n=quad['A'].rows
    def shifted_quad(dt):
        row=moved(b,dt);ds=row['S']-b['S'];jets={}
        for name in ('a','d','e'):
            x0,x1,x2=b['jets'][name];x3=thirds[name]
            jets[name]=[x0+x1*ds+x2*ds*ds/2+x3*ds**3/6,x1+x2*ds+x3*ds*ds/2,x2+x3*ds]
        fixed=prior.fixed_state(row['S'],row['q'],row['z'],row['Q'],b['parameters'],b['fluids'],jets)
        return prior.quadratic(fixed,k2*mp.exp(-2*b['Qdot']*dt))
    Adot=mp.matrix([[mp.diff(lambda dt:shifted_quad(dt)['A'][i,j],0) for j in range(n)] for i in range(n)])
    Bdot=mp.matrix([[mp.diff(lambda dt:shifted_quad(dt)['B'][i,j],0) for j in range(n)] for i in range(n)])
    A,B=quad['A'],quad['B'];inverse=A**-1
    damping=inverse*(Adot+3*b['Qdot']*A+B-B.T)
    restoring=inverse*(Bdot+3*b['Qdot']*B+quad['potential']);G=mp.zeros(2*n)
    for i in range(n):
        G[i,i+n]=1
        for j in range(n):G[i+n,j]=-restoring[i,j];G[i+n,j+n]=-damping[i,j]
    roots,vec=mp.eig(G,left=False,right=True)
    residual=max(mp.norm(G*vec[:,i]-roots[i]*vec[:,i])/max(1,mp.norm(G)*mp.norm(vec[:,i])) for i in range(2*n))
    growing=max(range(2*n),key=lambda i:mp.re(roots[i]))
    return dict(roots=roots,residual=residual,third_jets=thirds,kinetic_eigenvalues=list(mp.eigsy(A,eigvals_only=True)),
        fastest_instantaneous_root=roots[growing],fastest_mode_x_velocity=list(vec[:,growing]),
        interpretation='All six time-dependent Euler roots; mode coordinates are (zeta,sigma_r,sigma_m) and their velocities')


def transport(history,k2_initial=100,nodes=81):
    with mp.workdps(40):
        times=np.linspace(0,history['Q_end'],nodes);rows=[completed_at(history,Q) for Q in times]
        k2=[mp.mpf(k2_initial)*mp.exp(-2*r['Q']) for r in rows]
        gs=[np.array((base.hamiltonian_generator(r,k)/r['Qdot']).tolist(),dtype=float) for r,k in zip(rows,k2)]
        first=prior.quadratic(rows[0],k2[0]);eig,vec=np.linalg.eigh(np.array(first['A'].tolist(),dtype=float))
        if min(eig)<=0:raise ValueError('Initial kinetic norm is not positive')
        R=(vec*np.sqrt(eig))@vec.T;n=len(eig);H0=float(rows[0]['Qdot'])
        def convert(r,k):
            quad=prior.quadratic(r,k);di=np.diag([.5]+[1]*(n-1))
            X=2*di@np.array(quad['L'].tolist(),dtype=float);P=2*di@np.array(quad['K'].tolist(),dtype=float)
            return np.block([[R,np.zeros_like(R)],[R@X/H0,R@P/H0]])
        T0=convert(rows[0],k2[0]);inverse=np.linalg.inv(T0);Tf=convert(rows[-1],k2[-1])
        field=CubicSpline(times,np.array([T0@G@inverse for G in gs]));dim=2*n
        sol=solve_ivp(lambda Q,u:(field(Q)@u.reshape(dim,dim)).ravel(),(0,times[-1]),np.eye(dim).ravel(),
            method='DOP853',rtol=1e-10,atol=1e-12,max_step=history['Q_end']/nodes)
        if not sol.success:raise RuntimeError(sol.message)
        U=sol.y[:,-1].reshape(dim,dim);transfer=Tf@inverse@U
        expected=np.exp(-3*n*times[-1]);actual=np.linalg.det(U)
        return dict(Q_end=history['Q_end'],k2_initial=k2_initial,nodes=nodes,nfev=sol.nfev,
            singular_values=list(np.linalg.svd(transfer,compute_uv=False)),weighted_transfer=transfer.tolist(),
            determinant=actual,volume_prediction=expected,relative_volume_error=abs(actual/expected-1),
            norm='Fixed initial kinetic square root on (x,xdot/Qdot_initial), not a universal instability threshold')


@lru_cache(None)
def band_expression():
    p,H=s.symbols('p H');params=s.symbols('a C m B d e v g0 w0');a,C,m,B,d,e,v,g0,w0=params
    rates=s.symbols('ad Cd md Bd dd ed vd g0d w0d')
    M=m-2*B*p;K=a-C*C/(2*M);L=2*d*p-C*(4*e*p+g0)/(2*M)
    W=-2*v*p+4*d*d*p*p/a+w0-(4*e*p+g0)**2/(2*M)
    ratio=s.cancel(L/K)
    derivative=sum(s.diff(ratio,x)*dx for x,dx in zip(params,rates))-2*H*p*s.diff(ratio,p)
    omega=s.cancel(K*W-L*L-K*(derivative+3*H*ratio))
    numerator,denominator=s.fraction(omega)
    nc=s.Poly(numerator,p).all_coeffs();dc=s.Poly(denominator,p).all_coeffs()
    return dict(numerator_degree=s.degree(numerator,p),denominator_degree=s.degree(denominator,p),
        denominator_factor=str(s.factor(denominator)),
        coefficients=s.lambdify((*params,*rates,H),(nc,dc),'mpmath',cse=True))


def clock_band(b,completion=completed,motion=moved):
    """Clock canonical-subspace projection diagnostic, NOT the full eigenproblem."""
    def properties(r):
        enthalpy=mp.fsum((1+x['w'])*x['h'] for x in r['entries'])
        mass=mp.mpf(9)/2*mp.fsum(x['w']*(1+x['w'])*x['h'] for x in r['entries'])
        return [r['a'],r['red']['Sq'],r['M'],r['B'],r['red']['qR'],r['red']['SR'],r['v'],-3*enthalpy,mass]
    values=properties(b)
    rates=[mp.diff(lambda dt:properties(completion(motion(b,dt)))[i],0) for i in range(len(values))]
    expr=band_expression();num,den=expr['coefficients'](*values,*rates,b['Qdot'])
    def direct(t,p):
        a,C,m,B,d,e,v,g0,w0=[x+t*dx for x,dx in zip(values,rates)]
        p=p*mp.exp(-2*b['Qdot']*t);M=m-2*B*p
        K=a-C*C/(2*M);L=2*d*p-C*(4*e*p+g0)/(2*M)
        W=-2*v*p+4*d*d*p*p/a+w0-(4*e*p+g0)**2/(2*M)
        return K,L,W
    residuals=[];samples=[]
    for p in map(mp.mpf,('.01','1','10','100','10000')):
        K,L,W=direct(0,p)
        static=K*W-L*L;mixing=-K*mp.diff(lambda t:direct(t,p)[1]/direct(t,p)[0],0)
        expansion=-3*b['Qdot']*L;omega=static+mixing+expansion
        rational=mp.polyval(num,p)/mp.polyval(den,p)
        residuals.append(omega-rational);samples.append(dict(k_squared=p,projected_omega_squared=omega,
            instantaneous_hamiltonian_determinant=static,time_dependent_mixing=mixing,volume_term=expansion))
    roots=np.roots([float(x) for x in num])
    return dict(numerator_degree=int(expr['numerator_degree']),denominator_degree=int(expr['denominator_degree']),
        denominator_factor=expr['denominator_factor'],numerator_coefficients=num,denominator_coefficients=den,
        positive_real_numerator_roots=[float(x.real) for x in roots if abs(x.imag)<1e-8 and x.real>0],
        direct_residuals=residuals,samples=samples,
        nonclaim='Projection sets the other canonical perturbations to zero; it is not an invariant subsystem or a substitute for all six modes')


def precision_transport(history,k2_initial=100,steps=160,dps=60):
    with mp.workdps(dps):
        end=mp.mpf(history['Q_end']);step=end/steps
        first=completed_at(history,0);last=completed_at(history,end)
        R=mp.cholesky(prior.quadratic(first,k2_initial)['A']).T;n=R.rows;dim=2*n
        di=mp.diag([mp.mpf('.5')]+[1]*(n-1))
        def convert(r,k):
            quad=prior.quadratic(r,k);T=mp.zeros(dim)
            X=R*2*di*quad['L']/first['Qdot'];P=R*2*di*quad['K']/first['Qdot']
            for i in range(n):
                for j in range(n):T[i,j]=R[i,j];T[i+n,j]=X[i,j];T[i+n,j+n]=P[i,j]
            return T
        T0=convert(first,k2_initial);Tf=convert(last,mp.mpf(k2_initial)*mp.exp(-2*end));F=mp.eye(dim)
        for i in range(steps):
            Q=(i+mp.mpf('.5'))*step;r=completed_at(history,Q)
            G=base.hamiltonian_generator(r,mp.mpf(k2_initial)*mp.exp(-2*Q))/r['Qdot']
            F=mp.expm(G*step)*F
        prediction=mp.exp(-3*n*end);actual=mp.det(F);T=Tf*F*(T0**-1)
        return dict(k2_initial=k2_initial,Q_end=end,steps=steps,dps=dps,
            singular_values=list(mp.svd(T,compute_uv=False)),determinant=actual,volume_prediction=prediction,
            relative_volume_error=abs(actual/prediction-1),
            norm='Same initial kinetic norm as double transport, orthogonally equivalent Cholesky coordinates')


def construction_report():
    history=evolve(1,max_step=.005,rtol=1e-12);long=evolve(7,max_step=.02)
    points=[]
    with mp.workdps(60):
        for Q in (0,.1,1):
            r=completed_at(history,Q)
            points.append(dict(Q=Q,state=prior.snapshot(r),jets=r['jets'],integrability=integrability(r),
                tensor_speed_squared=-r['t']*r['raw']['R']/mp.exp(2*r['S']),tensor_kinetic=1/(4*r['t']),
                clock_projection=clock_band(r),
                spectra=[dict(k_squared=k,**frequencies(r,k)) for k in (.001,.01,.1,1,10,100,1000,10**14)],
                brackets=[dict(k_squared=k,**prior.brackets(r,k)) for k in (0,1,10000)]))
        old=base.completed(base.initial(profile='charge'))
        old_projection=clock_band(old,completion=base.completed,motion=base.moved)
    checks=dict(homogeneous_audit=all(x==0 for x in homogeneous_audit().values()),
        one_efold=history['success'],seven_efolds=long['success'],
        one_efold_charge=history['maximum_charge_drift']<1e-8,
        genuine_coefficient_jets=max(abs(x) for p in points for x in p['integrability'].values())<mp.mpf('1e-35'),
        sampled_kinetics=all(min(f['kinetic_eigenvalues'])>0 for p in points for f in p['spectra']),
        auxiliary_ranks=all(x['rank']==4 for p in points for x in p['brackets']),
        tensor_coefficients=all(abs(p['tensor_speed_squared']-1)<mp.mpf('1e-40') and p['tensor_kinetic']>0 for p in points),
        rational_diagnostic=max(abs(x) for p in points for x in p['clock_projection']['direct_residuals'])<mp.mpf('1e-35'),
        eigen_residuals=all(f['residual']<mp.mpf('1e-35') for p in points for f in p['spectra']))
    return dict(full_theory='OPEN',checks=checks,history=history,long_history=long,points=points,
        old_IC25_initial_clock_projection=old_projection,
        nonclaims=['Projection is not an invariant scalar subsystem; all six full modes remain authoritative',
          'Slow growing low-wavenumber roots may remain; no all-mode stability certification',
          'No nonlinear/global/static/PPN, interaction-scale or empirical closure'])


def transport_report():
    h=evolve(1,max_step=.005,rtol=1e-12);rows=[]
    for k in (.001,.01,.1,1,10,100):
        a=transport(h,k,81);b=transport(h,k,161)
        error=np.linalg.norm(np.array(a['weighted_transfer'])-np.array(b['weighted_transfer']))/max(1,np.linalg.norm(b['weighted_transfer']))
        rows.append(dict(k2_initial=k,coarse=a,fine=b,relative_transfer_difference=error))
    return dict(full_theory='OPEN',checks=dict(background=h['success'],
        grid_agreement=all(x['relative_transfer_difference']<1e-3 for x in rows),
        volume_identity=all(x['fine']['relative_volume_error']<1e-7 for x in rows)),rows=rows,
        nonclaims=['Specified norm and six initial wavelengths, not an all-time or nonlinear stability theorem'])


def precision_report():
    h=evolve(1,max_step=.005,rtol=1e-12)
    a=precision_transport(h,100,160);b=precision_transport(h,100,320)
    with mp.workdps(60):err=abs(a['singular_values'][0]/b['singular_values'][0]-1)
    return dict(full_theory='OPEN',checks=dict(volume_identity=b['relative_volume_error']<mp.mpf('1e-30'),
        step_agreement=err<mp.mpf('.02')),coarse=a,fine=b,relative_largest_amplification_difference=err,
        nonclaims=['Independent time-integration method, but same double-precision background interpolation',
          'Finite amplification is not a global stability certificate'])


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=('construction','transport','precision'),default='construction')
    p.add_argument('--require-full-closure',action='store_true');args=p.parse_args()
    out={'construction':construction_report,'transport':transport_report,'precision':precision_report}[args.mode]()
    print(json.dumps(out,default=prior.serial,indent=2))
    raise SystemExit(1 if not all(out['checks'].values()) else 2 if args.require_full_closure else 0)
