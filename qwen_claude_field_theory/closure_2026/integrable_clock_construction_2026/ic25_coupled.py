#!/usr/bin/env python3
"""IC25 local designer action: jointly reconstruct A(S) and D(S).

S(Q)=S_initial+kappa Q specifies a construction trajectory, not a new
constraint imposed on the dynamical lapse. Raw action variation must recover it.
"""
import argparse
import json
import mpmath as mp
import numpy as np
import sympy as s
from scipy.integrate import DOP853, solve_ivp
from scipy.interpolate import CubicSpline
import ic24_potential as prior
model=prior.model


def identities():
    alpha,p,hzz,z,v,v0,B,E,L,U,q,Ps,Pq,Pz,sd,qd,HQ,enthalpy=s.symbols(
        'alpha p hzz z v v0 B E L U q Ps Pq Pz sd qd HQ enthalpy',nonzero=True)
    a=-p*p/(2*hzz);Z=-v0+2*z*(L-z*alpha)/p
    zd=-((U+q*alpha)*sd+p*qd)/hzz
    pd=(Ps-alpha)*sd+Pq*qd+Pz*zd
    rho=-4*z/p;rhod=-4*zd/p+4*z*pd/p**2
    cg=(-2*a*v+4*a*Z**2/B)/E-2*a*(rhod+HQ*rho)/E
    C=L-z*alpha-(U+q*alpha)*p/hzz;M=(-C*qd+3*HQ*enthalpy)/sd
    App=s.symbols('App')
    checks=dict(slope_third_derivative=s.diff(cg,alpha,3),
        slope_quadratic_coefficient=s.factor(s.diff(cg,alpha,2)/2+8*z**4/(B*E*hzz)),
        varied_lapse_preservation=s.factor(M*sd+C*qd-3*HQ*enthalpy),
        second_jet_compensation=s.expand(-App*q*z-z*z*(-q*App/z)))
    charge,Q,kappa,enthalpy=s.symbols('charge Q kappa enthalpy',nonzero=True)
    qdot=-s.Rational(3,2)*charge*s.exp(-3*Q)+s.Rational(3,2)*enthalpy
    actual=(-C*qdot+3*HQ*enthalpy)/(kappa*s.exp(-3*Q)*HQ)
    expected=3*C*charge/(2*kappa*HQ)+(3-3*C/(2*HQ))*s.exp(3*Q)*enthalpy/kappa
    checks['charge_scaled_constraint_identity']=s.factor(actual-expected)
    K=s.Matrix(3,3,lambda i,j:s.Symbol('K%d%d'%(min(i,j),max(i,j))))
    W=s.Matrix(3,3,lambda i,j:s.Symbol('W%d%d'%(min(i,j),max(i,j))))
    cross=s.Matrix(3,3,lambda i,j:s.Symbol('L%d%d'%(i,j)))
    D=s.diag(2,1,1);di=D.inv();zero=s.zeros(3)
    G=(2*di*cross).row_join(2*di*K).col_join((-2*di*W).row_join(-2*di*cross.T-3*HQ*s.eye(3)))
    Omega=zero.row_join(D).col_join((-D).row_join(zero))
    residual=G.T*Omega+Omega*G+3*HQ*Omega
    for i in range(6):
        for j in range(6):checks['weighted_symplectic_%d%d'%(i,j)]=s.expand(residual[i,j])
    checks['density_flow_trace']=s.expand(s.trace(G)+3*3*HQ)
    return checks


def initial(kappa='.01',target='.3',profile='linear'):
    b=prior.initial();b['AA']=model.coefficient_jets(b['S'],b['parameters'])['a'][0]
    b['kappa']=mp.mpf(kappa);b['target']=mp.mpf(target)
    if profile not in ('linear','charge'):raise ValueError('Unknown construction history')
    b['profile']=profile
    if b['kappa']<=0:raise ValueError('This construction uses a strictly increasing S chart')
    return b


def clock_slope(b):
    return b['kappa']*(mp.exp(-3*b['Q']) if b['profile']=='charge' else 1)


def clock_offset(b,Q):
    return b['kappa']*(-mp.expm1(-3*Q)/3 if b['profile']=='charge' else Q)


def trial(b,alpha,App=0):
    S,q,z,Q=b['S'],b['q'],b['z'],b['Q'];alpha=mp.mpf(alpha)
    wc=model.normalized.constants()['wc']
    pin=model.normalized.legacy.activation(-mp.exp(-3*wc)*q/3)
    if pin<=0:raise ValueError('Outside the active pin stratum')
    jets=model.coefficient_jets(S,b['parameters'])
    jets['a']=[b['AA'],alpha,mp.mpf(App)];jets['d']=[mp.mpf(0)]*3
    r=model.raw_jets(S,q,z,0,jets);jets['d'][0]=r['z']/(2*z)
    entries=prior.matter(S,Q,b['fluids']);total=mp.fsum(f['h'] for f in entries)
    pressure=mp.fsum(f['w']*f['h'] for f in entries)
    r=model.raw_jets(S,q,z,0,jets);jets['d'][1]=(r['S']+total)/z**2
    r=model.raw_jets(S,q,z,0,jets);Qdot=r['q']/2;qdot=-mp.mpf(3)/2*(r['h']-pressure)
    sd=clock_slope(b)*Qdot
    if sd==0:raise ValueError('Nonexpanding or noninvertible construction chart')
    C=r['Sq']-r['Sz']*r['qz']/r['zz']
    M=(-C*qdot+3*Qdot*(total+pressure))/sd
    jets['d'][2]=(r['SS']+total-r['Sz']**2/r['zz']-M)/z**2
    row=prior.fixed_state(S,q,z,Q,b['parameters'],b['fluids'],jets)
    row.update(AA=b['AA'],alpha=alpha,kappa=b['kappa'],target=b['target'],pin_activation=pin,profile=b['profile'])
    return row


def polynomial(b):
    f0,fp,fm=[trial(b,x)['principal']['gravity_diagonal'] for x in (0,1,-1)]
    return ((fp+fm)/2-f0,(fp-fm)/2,f0)


def control(b):
    a,c,d=polynomial(b);d-=b['target'];disc=c*c-4*a*d
    if disc<0:raise ValueError('Characteristic derivative equation has no real root')
    if a==0:
        if c==0:raise ValueError('Degenerate derivative equation requires separate treatment')
        alpha=-d/c
    else:
        alpha=(-c-mp.sqrt(disc))/(2*a)
    r=trial(b,alpha);r['discriminant']=disc
    return r


def moved(b,dt):
    r=dict(b)
    for i,x in enumerate(('S','q','z')):r[x]=b[x]+dt*b['flow'][i]
    r['Q']=b['Q']+dt*b['Qdot'];r['AA']=b['AA']+dt*b['alpha']*b['flow'][0]
    return r


def completed(b):
    r=control(b)
    App=mp.diff(lambda dt:control(moved(r,dt))['alpha'],0)/r['flow'][0]
    full=trial(b,r['alpha'],App);full['discriminant']=r['discriminant']
    return full


def integrability(r):
    def value(dt):return completed(moved(r,dt))
    sd=r['flow'][0]
    return dict(Aprime_dot_minus_Asecond_Sdot=mp.diff(lambda dt:value(dt)['alpha'],0)-r['jets']['a'][2]*sd,
        D_dot_minus_Dprime_Sdot=mp.diff(lambda dt:value(dt)['jets']['d'][0],0)-r['jets']['d'][1]*sd,
        Dprime_dot_minus_Dsecond_Sdot=mp.diff(lambda dt:value(dt)['jets']['d'][1],0)-r['jets']['d'][2]*sd,
        charge_dot=mp.diff(lambda dt:value(dt)['charge'],0))


def frequencies(b,k_squared):
    """S-only Taylor jets through third order, followed by actual Euler roots."""
    thirds={name:mp.diff(lambda dt:completed(moved(b,dt))['jets'][name][2],0)/b['flow'][0] for name in ('a','d')}
    k2=mp.mpf(k_squared);base=prior.quadratic(b,k2);n=base['A'].rows
    def qtime(dt):
        shifted=moved(b,dt);S=shifted['S'];ds=S-b['S']
        jets=model.coefficient_jets(S,b['parameters'])
        for name in ('a','d'):
            x0,x1,x2=b['jets'][name];x3=thirds[name]
            jets[name]=[x0+x1*ds+x2*ds**2/2+x3*ds**3/6,x1+x2*ds+x3*ds**2/2,x2+x3*ds]
        r=prior.fixed_state(S,shifted['q'],shifted['z'],shifted['Q'],b['parameters'],b['fluids'],jets)
        return prior.quadratic(r,k2*mp.exp(-2*b['Qdot']*dt))
    Adot=mp.matrix([[mp.diff(lambda dt:qtime(dt)['A'][i,j],0) for j in range(n)] for i in range(n)])
    Bdot=mp.matrix([[mp.diff(lambda dt:qtime(dt)['B'][i,j],0) for j in range(n)] for i in range(n)])
    A,B=base['A'],base['B'];inverse=A**-1
    damping=inverse*(Adot+3*b['Qdot']*A+B-B.T)
    restoring=inverse*(Bdot+3*b['Qdot']*B+base['potential'])
    gen=mp.zeros(2*n)
    for i in range(n):
        gen[i,i+n]=1
        for j in range(n):gen[i+n,j]=-restoring[i,j];gen[i+n,j+n]=-damping[i,j]
    roots,vec=mp.eig(gen,left=False,right=True)
    residual=max(mp.norm(gen*vec[:,i]-roots[i]*vec[:,i])/max(1,mp.norm(gen)*mp.norm(vec[:,i])) for i in range(2*n))
    return dict(roots=roots,residual=residual,third_jets=thirds,kinetic_eigenvalues=list(mp.eigsy(A,eigvals_only=True)))


def hamiltonian_generator(b,k_squared):
    """x,p-density variables, canonical symplectic term V p^T D xdot."""
    quad=prior.quadratic(b,k_squared);n=quad['K'].rows;D=mp.diag([2]+[1]*(n-1));inverse=D**-1
    xx=2*inverse*quad['L'];xp=2*inverse*quad['K']
    px=-2*inverse*quad['W'];pp=-2*inverse*quad['L'].T-3*b['Qdot']*mp.eye(n)
    G=mp.zeros(2*n)
    for i in range(n):
        for j in range(n):G[i,j]=xx[i,j];G[i,j+n]=xp[i,j];G[i+n,j]=px[i,j];G[i+n,j+n]=pp[i,j]
    return G


def completed_at(history,Q):
    base=initial(history['kappa'],history['target'],history['profile']);states=history['states']
    knots=[x['Q'] for x in states]
    values=CubicSpline(knots,[[x['q'],x['z'],x['A']] for x in states])(float(Q))
    base.update(Q=mp.mpf(Q),S=base['S']+clock_offset(base,mp.mpf(Q)))
    base['q'],base['z'],base['AA']=map(mp.mpf,values)
    return completed(base)


def transport(history,k2_initial=1,nodes=41):
    """Actual nonautonomous propagator on an interpolated background.

    Weighted norm uses initial kinetic metric for x and xdot/Qdot_initial.
    It is an explicitly chosen norm, not an invariant instability threshold.
    """
    if history['Q_end']<=0 or nodes<4:raise ValueError('Positive interval and >=4 interpolation nodes required')
    with mp.workdps(40):
        times=np.linspace(0,history['Q_end'],nodes)
        rows=[completed_at(history,Q) for Q in times]
        k2=[mp.mpf(k2_initial)*mp.exp(-2*r['Q']) for r in rows]
        generators=[np.array((hamiltonian_generator(r,k)/r['Qdot']).tolist(),dtype=float) for r,k in zip(rows,k2)]
        first=prior.quadratic(rows[0],k2[0]);A0=np.array(first['A'].tolist(),dtype=float)
        eig,vec=np.linalg.eigh(A0)
        if min(eig)<=0:raise ValueError('Initial kinetic metric is not positive')
        R=(vec*np.sqrt(eig))@vec.T;n=len(eig);HQ0=float(rows[0]['Qdot'])
        def convert(r,k):
            q=prior.quadratic(r,k);di=np.diag([.5]+[1]*(n-1))
            X=2*di@np.array(q['L'].tolist(),dtype=float);P=2*di@np.array(q['K'].tolist(),dtype=float)
            return np.block([[R,np.zeros_like(R)],[R@X/HQ0,R@P/HQ0]])
        T0=convert(rows[0],k2[0]);T0inv=np.linalg.inv(T0);Tf=convert(rows[-1],k2[-1])
        interp=CubicSpline(times,np.array([T0@G@T0inv for G in generators]))
        dim=2*n
        sol=solve_ivp(lambda Q,u:(interp(Q)@u.reshape(dim,dim)).ravel(),(0,times[-1]),np.eye(dim).ravel(),
                      method='DOP853',rtol=1e-10,atol=1e-12,max_step=history['Q_end']/nodes)
        if not sol.success:raise RuntimeError(sol.message)
        U=sol.y[:,-1].reshape(dim,dim);transfer=Tf@T0inv@U
        expected=np.exp(-3*n*times[-1]);actual=np.linalg.det(U)
        return dict(Q_end=float(times[-1]),k2_initial=k2_initial,nodes=nodes,nfev=sol.nfev,
            weighted_singular_values=list(np.linalg.svd(transfer,compute_uv=False)),
            raw_density_propagator_determinant=actual,volume_identity_prediction=expected,
            relative_volume_error=abs(actual/expected-1),weighted_transfer=transfer.tolist(),
            norm='Fixed initial kinetic square root on (x,xdot/Qdot_initial); coordinate-specific finite amplification, not stability certification')


def evolve(target_Q=.1,kappa='.01',target='.3',max_step=.001,rtol=1e-10,max_steps=2000,profile='linear'):
    """Retain accepted solver steps and distinguish stage failure from a boundary."""
    with mp.workdps(30):
        base=initial(kappa,target,profile);S0=base['S']
        def row(Q,y):
            b=dict(base);b.update(Q=mp.mpf(Q),S=S0+clock_offset(base,mp.mpf(Q)))
            b['q'],b['z'],b['AA']=map(mp.mpf,y)
            return control(b)
        def rhs(Q,y):
            r=row(Q,y)
            return [float(r['flow'][1]/r['Qdot']),float(r['flow'][2]/r['Qdot']),float(r['alpha']*clock_slope(r))]
        y0=[float(base[x]) for x in ('q','z','AA')]
        solver=DOP853(rhs,0,y0,float(target_Q),rtol=rtol,atol=rtol*.001,max_step=max_step)
        rows=[row(0,y0)];reason='requested endpoint reached';success=True
        def health(r):
            return min(-r['M']-mp.mpf('1e-5'),-r['raw']['zz'],r['jets']['d'][0],
                r['principal']['gradient_margin'],r['principal']['lightcone_margin'],r['H_physical'],r['discriminant'])
        for _ in range(max_steps):
            if solver.status!='running':break
            try:
                solver.step()
                if solver.status=='failed':reason='adaptive solver failure';success=False;break
                r=row(solver.t,solver.y);rows.append(r)
                if health(r)<=0:reason='accepted point violates regular/causal design margin';success=False;break
            except (ValueError,ZeroDivisionError) as exc:
                reason='unaccepted stage failed: '+str(exc);success=False;break
        else:reason='step budget reached';success=False
        states=[]
        for r in rows:
            s=prior.snapshot(r);s.update(A=float(r['AA']),Aprime=float(r['alpha']),discriminant=float(r['discriminant']),pin_activation=float(r['pin_activation']))
            states.append(s)
        return dict(success=success,reason=reason,requested_Q=float(target_Q),Q_end=states[-1]['Q'],
            max_step=max_step,rtol=rtol,nfev=solver.nfev,kappa=kappa,target=target,profile=profile,states=states,
            maximum_charge_drift=float(max(abs(r['charge']-rows[0]['charge']) for r in rows)),
            maximum_target_error=float(max(abs(r['principal']['gravity_diagonal']-r['target']) for r in rows)),
            minimum_health_margin=float(min(health(r) for r in rows)),
            note='Background uses placeholder Asecond=0 absorbed in Dsecond; completed() supplies genuine action jets for perturbations')


def construction_report():
    linear=evolve(1,max_step=.01)
    charge=evolve(7,max_step=.02,profile='charge')
    fine=evolve(7,max_step=.01,rtol=1e-12,profile='charge')
    points=[]
    with mp.workdps(60):
        for Q in (0,.1,1,7):
            r=completed_at(fine,Q)
            points.append(dict(Q=Q,state=prior.snapshot(r),A_jets=r['jets']['a'],D_jets=r['jets']['d'],
                integrability=integrability(r),
                spectra=[dict(k_squared=k,**frequencies(r,k)) for k in (1,10**14)],
                brackets=[dict(k_squared=k,**prior.brackets(r,k)) for k in (0,1,10000)]))
    identities_result=identities()
    delta=max(abs(charge['states'][-1][x]-fine['states'][-1][x]) for x in ('S','q','z','A'))
    checks=dict(exact_identities=all(x==0 for x in identities_result.values()),
        linear_one_efold=linear['success'] and linear['Q_end']==1,
        charge_seven_efolds=charge['success'] and fine['success'] and fine['Q_end']==7,
        sampled_causal_margins=min(charge['minimum_health_margin'],fine['minimum_health_margin'])>0,
        endpoint_step_agreement=delta<1e-9,
        finite_charge_accuracy=max(charge['maximum_charge_drift'],fine['maximum_charge_drift'])<1e-5,
        coefficient_integrability=max(abs(x) for p in points for x in p['integrability'].values())<mp.mpf('1e-35'),
        kinetic_samples=all(min(f['kinetic_eigenvalues'])>0 for p in points for f in p['spectra']),
        bracket_samples=all(x['rank']==4 for p in points for x in p['brackets']),
        eigen_residuals=all(f['residual']<mp.mpf('1e-35') for p in points for f in p['spectra']))
    return dict(full_theory='OPEN',checks=checks,exact_identity_count=len(identities_result),
        linear_history=linear,charge_history=charge,fine_charge_history=fine,endpoint_maximum_difference=delta,points=points,
        nonclaims=['Seven barred-scale efolds on a designed ideal-fluid branch, NOT a calibrated recombination cosmology',
          'Different profiles define different actions; their successes are not pooled',
          'No global coefficient extension, nonlinear constraints, relative flow, PPN, strong-coupling or empirical certification'])


def transport_report():
    h=evolve(1,max_step=.005,rtol=1e-12,profile='charge')
    rows=[]
    for k2 in (1,100):
        coarse=transport(h,k2,81);fine=transport(h,k2,161)
        diff=np.linalg.norm(np.array(coarse['weighted_transfer'])-np.array(fine['weighted_transfer']))
        scale=max(1,np.linalg.norm(fine['weighted_transfer']))
        rows.append(dict(k2_initial=k2,coarse=coarse,fine=fine,relative_transfer_difference=diff/scale))
    return dict(full_theory='OPEN',checks=dict(background_completed=h['success'],
        transfer_grid_agreement=all(x['relative_transfer_difference']<1e-3 for x in rows),
        symplectic_volume=all(x['fine']['relative_volume_error']<1e-7 for x in rows)),
        rows=rows,nonclaims=['Specified norm and two initial wavelengths over Q in[0,1], not all-mode stability',
          'No nonlinear perturbations, interaction-scale calculation or cosmological initial-condition fit'])


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--transport',action='store_true')
    parser.add_argument('--require-full-closure',action='store_true');args=parser.parse_args()
    out=transport_report() if args.transport else construction_report()
    print(json.dumps(out,default=prior.serial,indent=2))
    raise SystemExit(1 if not all(out['checks'].values()) else 2 if args.require_full_closure else 0)
