#!/usr/bin/env python3
"""Evolve the constant-tensor IC28 action with one slow-clock D(S) IVP."""
import argparse
import json
import mpmath as mp
import numpy as np
from scipy.integrate import DOP853,solve_ivp
from scipy.interpolate import CubicSpline,BPoly,PPoly
import ic28_constant_tensor as base


def initial(target_M='-1000',pin_h0='1'):
    b=base.witness(target_M)
    r=base.integrated_state(b['S'],b['q'],b['z'],b['Q'],b['fluids'],b['parameters'],target_M)
    r['pin_h0']=mp.mpf(pin_h0)
    if r['pin_h0']<=0:raise ValueError('Positive activation scale required')
    return r


def pin_info(b):
    wc=base.old.normalized.constants()['wc']
    r=-mp.exp(-3*wc)*b['q']/(3*b.get('pin_h0',mp.mpf(1)))
    eta=base.old.normalized.legacy.activation(r)
    return dict(eta=eta,domain_margin=r*r-mp.mpf('.5'),
                plateau_margin=r*r-mp.mpf('.75'),
                log_eta=mp.log(eta) if eta>0 else mp.ninf)


def snapshot(b):
    pin=pin_info(b)
    return {**{x:float(b[x]) for x in ('Q','S','q','z','M','a','H_physical','Qdot')},
        'cg2':float(b['principal']['gravity_diagonal']),
        'D_jets':[float(x) for x in b['jets']['d']],
        'charge':float(b['charge']),
        'pin_activation':mp.nstr(pin['eta'],20),
        'pin_log_activation':str(pin['log_eta']),
        'pin_domain_margin':float(pin['domain_margin']),
        'pin_plateau_margin':float(pin['plateau_margin']),
        'constraint_residual':float(max(abs(x) for x in b['constraints']))}


def evolve(target_Q=1,max_step=.005,target_M='-1000',pin_h0='1',rtol=1e-11,max_steps=3000):
    with mp.workdps(35):
        b=initial(target_M,pin_h0)
        def point(Q,y):
            S,q,z=map(mp.mpf,y)
            r=base.integrated_state(S,q,z,mp.mpf(Q),b['fluids'],b['parameters'],target_M)
            r['pin_h0']=b['pin_h0'];return r
        def rhs(Q,y):
            r=point(Q,y)
            return [float(x/r['Qdot']) for x in r['flow']]
        solver=DOP853(rhs,0,[float(b[x]) for x in ('S','q','z')],float(target_Q),
                      rtol=rtol,atol=rtol*.01,max_step=max_step)
        rows=[b];reason='requested endpoint reached';success=True
        for _ in range(max_steps):
            if solver.status!='running':break
            current=rows[-1]
            if current['z']<=mp.mpf('1e-6'):
                success=False;reason='positive-z diagnostic floor reached';break
            rate=abs(current['flow'][2]/current['Qdot'])
            if rate:solver.max_step=min(max_step,float(current['z']/(4*rate)))
            try:
                solver.step()
                if solver.status=='failed':
                    success=False;reason='adaptive integrator failed';break
                r=point(solver.t,solver.y);rows.append(r);view=snapshot(r)
                if min(pin_info(r)['domain_margin'],r['H_physical'],r['a'],-r['M'],
                       -r['raw']['zz'],r['jets']['d'][0],view['cg2'],1-view['cg2'])<=0:
                    success=False;reason='accepted state violates pin/regular/causal conditions';break
            except (ValueError,ZeroDivisionError) as error:
                success=False;reason='unaccepted stage: '+str(error);break
        else:
            success=False;reason='step budget exhausted'
        return dict(success=success,reason=reason,target_M=str(target_M),pin_h0=str(pin_h0),requested_Q=target_Q,
            Q_end=float(rows[-1]['Q']),max_step=max_step,rtol=rtol,nfev=solver.nfev,
            states=[snapshot(r) for r in rows],
            maximum_charge_drift=float(max(abs(r['charge']-b['charge']) for r in rows)),
            maximum_constraint_residual=float(max(abs(x) for r in rows for x in r['constraints'])))


def state_at(history,Q):
    if not 0<=float(Q)<=history['Q_end']:raise ValueError('No extrapolation outside constructed action interval')
    b=initial(history['target_M'],history['pin_h0']);rows=history['states']
    spline=CubicSpline([x['Q'] for x in rows],[[x['S'],x['q'],x['z']] for x in rows])
    S,q,z=map(mp.mpf,spline(float(Q)))
    r=base.integrated_state(S,q,z,mp.mpf(Q),b['fluids'],b['parameters'],history['target_M'])
    r['pin_h0']=b['pin_h0'];return r


def transport(history,k_squared=1,nodes=81):
    """Six-dimensional dynamics and independent physical Phi/Psi response."""
    with mp.workdps(40):
        times=np.linspace(0,history['Q_end'],nodes)
        rows=[state_at(history,Q) for Q in times]
        wave=[mp.mpf(k_squared)*mp.exp(-2*r['Q']) for r in rows]
        first=base.matter.quadratic(rows[0],wave[0])
        R=np.array(mp.cholesky(first['A']).T.tolist(),dtype=float)
        Dinv=np.diag([.5,1,1]);H0=float(rows[0]['Qdot'])
        def conversion(row,k):
            quad=base.matter.quadratic(row,k)
            X=2*Dinv@np.array(quad['L'].tolist(),dtype=float)
            P=2*Dinv@np.array(quad['K'].tolist(),dtype=float)
            return np.block([[R,np.zeros_like(R)],[R@X/H0,R@P/H0]])
        T0=conversion(rows[0],wave[0]);inverse=np.linalg.inv(T0)
        gs=[T0@np.array((base.generator(r,k)/r['Qdot']).tolist(),dtype=float)@inverse
            for r,k in zip(rows,wave)]
        spline=CubicSpline(times,np.array(gs))
        solution=solve_ivp(lambda Q,u:(spline(Q)@u.reshape(6,6)).ravel(),
            (0,times[-1]),np.eye(6).ravel(),method='DOP853',rtol=1e-10,atol=1e-12,
            max_step=history['Q_end']/nodes)
        if not solution.success:raise RuntimeError(solution.message)
        U=solution.y[:,-1].reshape(6,6)
        weighted=conversion(rows[-1],wave[-1])@inverse@U
        def metric_map(row,k):
            fields=[base.physical_fields(row,k,mp.eye(6)[:,i]) for i in range(6)]
            return np.array([[x[key] for x in fields] for key in ('Phi','Psi')],dtype=float)
        initial_map=metric_map(rows[0],wave[0])@inverse
        final_map=metric_map(rows[-1],wave[-1])@inverse@U
        predicted=np.exp(-9*history['Q_end']);actual=np.linalg.det(U)
        return dict(Q_end=history['Q_end'],k_squared_initial=k_squared,nodes=nodes,
            determinant=actual,volume_prediction=predicted,relative_volume_error=abs(actual/predicted-1),
            weighted_transfer=weighted.tolist(),singular_values=list(np.linalg.svd(weighted,compute_uv=False)),
            initial_metric_map=initial_map.tolist(),final_metric_map=final_map.tolist(),
            metric_operator_norm_initial=list(np.linalg.norm(initial_map,axis=1)),
            metric_operator_norm_final=list(np.linalg.norm(final_map,axis=1)),
            relative_metric_slip=float(np.linalg.norm(final_map[0]-final_map[1])/max(1,np.linalg.norm(final_map))),
            nfev=solution.nfev,
            norm='Fixed initial kinetic norm on (x,xdot/Qdot_initial); physical maps are responses per unit of that norm, not empirical growth factors')


def construction_report():
    history=evolve(1,max_step=.005,pin_h0='.5',rtol=1e-12)
    long=evolve(7,max_step=.02,pin_h0='.5')
    fine=evolve(7,max_step=.01,pin_h0='.5')
    legacy=evolve(1,max_step=.0025,pin_h0='1')
    points=[]
    with mp.workdps(50):
        for Q in (0,.1,1,7):
            b=state_at(history if Q<=1 else fine,Q)
            points.append(dict(Q=Q,state=snapshot(b),integrability=base.integrability(b),
                tensor_mass=2*mp.exp(b['S']-2*base.old.normalized.constants()['wc'])/b['t'],
                tensor_speed_squared=-b['t']*b['raw']['R']/mp.exp(2*b['S']),
                brackets=[dict(k_squared=k,**base.matter.brackets(b,k)) for k in (0,1,10000)],
                spectra=[dict(k_squared=k,**base.frequencies(b,k)) for k in (mp.mpf('.001'),mp.mpf('.1'),1,100,10**14)],
                no_slip_residuals=[base.physical_fields(b,k,mp.eye(6)[:,i])['Phi']
                    -base.physical_fields(b,k,mp.eye(6)[:,i])['Psi'] for k in (mp.mpf('.001'),1,100) for i in range(6)]))
        checks=dict(one_efold=history['success'],seven_efolds=long['success'] and fine['success'],
            short_charge=history['maximum_charge_drift']<1e-9,
            genuine_jets=all(abs(x)<mp.mpf('1e-30') for p in points for x in p['integrability'].values()),
            tensor_normalization=all(abs(p['tensor_mass']-1)<mp.mpf('1e-35') for p in points),
            tensor_speed=all(abs(p['tensor_speed_squared']-1)<mp.mpf('1e-35') for p in points),
            no_slip=all(abs(x)<mp.mpf('1e-30') for p in points for x in p['no_slip_residuals']),
            eigen_residuals=all(x['residual']<mp.mpf('1e-30') for p in points for x in p['spectra']),
            active_plateau=all(x['pin_plateau_margin']>0 for x in fine['states']))
    return dict(full_theory='OPEN',checks=checks,history=history,long_history=long,refined_long_history=fine,
        legacy_activation_control=legacy,points=points,
        nonclaims=['h0=.5 is an explicit changed action parameter, not a proof of pin-off transition closure',
            'Seven designed e-folds are not a calibrated cosmological history or a CMB fit',
            'No nonlinear/general/static/PPN, strong-coupling or empirical certification'])


def transport_report():
    history=evolve(1,max_step=.0025,pin_h0='.5',rtol=1e-12);rows=[]
    for k in (.001,.01,.1,1,10,100):
        a=transport(history,k,81);b=transport(history,k,161)
        err=np.linalg.norm(np.array(a['weighted_transfer'])-np.array(b['weighted_transfer']))/max(1,np.linalg.norm(b['weighted_transfer']))
        rows.append(dict(k_squared_initial=k,coarse=a,fine=b,relative_transfer_difference=err))
    return dict(full_theory='OPEN',checks=dict(background=history['success'],
        grid_agreement=all(x['relative_transfer_difference']<1e-3 for x in rows),
        volume_identity=all(x['fine']['relative_volume_error']<1e-7 for x in rows),
        physical_no_slip=all(x['fine']['relative_metric_slip']<1e-10 for x in rows)),
        rows=rows,nonclaims=['Only Q[0,1] and six initial wavelengths; not universal stability or a source-response light-cone proof'])


def coefficient_table(history,nodes=81):
    """A fixed C2 quintic-Hermite representation; each grid defines an approximation."""
    with mp.workdps(40):
        rows=[state_at(history,Q) for Q in np.linspace(0,history['Q_end'],nodes)]
        xs=np.array([float(r['S']) for r in rows])
        if np.any(np.diff(xs)<=0):raise ValueError('Monotone S chart required for this coefficient representation')
        polynomial=BPoly.from_derivatives(xs,[[float(v) for v in r['jets']['d']] for r in rows])
        return PPoly.from_bernstein_basis(polynomial)


def polynomial_jets(S,table):
    """Evaluate and differentiate the fixed polynomial without casting S to float."""
    if not mp.mpf(table.x[0])<=S<=mp.mpf(table.x[-1]):raise ValueError('No frozen-coefficient extrapolation')
    index=min(len(table.x)-2,max(0,int(np.searchsorted(table.x,float(S),side='right')-1)))
    x=S-mp.mpf(table.x[index]);coefficients=[mp.mpf(x) for x in table.c[:,index]]
    out=[]
    for order in range(3):
        out.append(mp.polyval(coefficients,x))
        degree=len(coefficients)-1
        coefficients=[a*(degree-i) for i,a in enumerate(coefficients[:-1])]
    return out


def source_response(history,table,factor):
    """Matter amplitudes change; the supplied D polynomial cannot change."""
    b=initial(history['target_M'],history['pin_h0'])
    fluids=[dict(f,amplitude=f['amplitude']*mp.mpf(factor)) for f in b['fluids']]
    def at(S,z):
        jets=dict(a=[b['parameters']['A0'],0,0],e=[b['parameters']['E40'],0,0],d=polynomial_jets(S,table))
        r=base.fixed(S,b['q'],z,mp.mpf(0),jets,fluids,b['parameters'])
        r['pin_h0']=b['pin_h0'];return r
    def equations(S,z):return at(S,z)['constraints']
    def jacobian(S,z):
        r=at(S,z);raw=r['raw'];rho=mp.fsum(f['h'] for f in r['entries'])
        return mp.matrix([[raw['SS']+rho,raw['Sz']],[raw['Sz'],raw['zz']]])
    # Positive added density shifts S into the represented interval.
    rho=mp.fsum(f['h'] for f in b['entries'])
    ds=-(mp.mpf(factor)-1)*rho/b['M']
    S,z=mp.findroot(equations,(b['S']+ds,b['z']),J=jacobian,tol=mp.mpf('1e-30'),maxsteps=30)
    return at(S,z)


def source_report():
    history=evolve(1,max_step=.0025,pin_h0='.5',rtol=1e-12)
    with mp.workdps(50):
        tables=[coefficient_table(history,n) for n in (41,81)]
        validation=[]
        for Q in (.003,.103,.503,.903):
            reference=state_at(history,Q)
            approx=polynomial_jets(reference['S'],tables[-1])
            validation.append(dict(Q=Q,
                relative_jet_errors=[abs(x-y)/max(1,abs(y)) for x,y in zip(approx,reference['jets']['d'])]))
        rows=[]
        for factor in (2,10,1000):
            a,b=[source_response(history,t,factor) for t in tables]
            rows.append(dict(matter_amplitude_factor=factor,state=snapshot(b),
                actual_M=b['M'],constraints=b['constraints'],
                coefficient_jet_values=b['jets']['d'],
                grid_state_difference=[b[key]-a[key] for key in ('S','z')],
                brackets=[dict(k_squared=k,**base.matter.brackets(b,k)) for k in (0,1)],
                slip=[base.physical_fields(b,k,mp.eye(6)[:,i])['Phi']
                    -base.physical_fields(b,k,mp.eye(6)[:,i])['Psi'] for k in (mp.mpf('.1'),100) for i in range(6)]))
        checks=dict(background=history['success'],
            reference_jet_agreement=all(x<mp.mpf('1e-5') for r in validation for x in r['relative_jet_errors']),
            actual_source_constraints=all(abs(x)<mp.mpf('1e-25') for r in rows for x in r['constraints']),
            source_grid_agreement=all(abs(x)<mp.mpf('1e-10') for r in rows for x in r['grid_state_difference']),
            no_slip=all(abs(x)<mp.mpf('1e-30') for r in rows for x in r['slip']),
            source_regular=all(r['state']['a']>0 and r['actual_M']<0 and 0<r['state']['cg2']<1 for r in rows))
    return dict(full_theory='OPEN',checks=checks,validation=validation,rows=rows,
        nonclaims=['Each fixed C2 polynomial is a numerical approximation to the same implicit D(S); refinements are not pooled as an exact-action proof',
            'These are perturbed homogeneous source constraints, not galaxy, cluster or photon-baryon dynamics',
            'No changed-source full Euler spectrum or time history is certified here'])


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=('construction','transport','sources'),default='construction')
    p.add_argument('--require-full-closure',action='store_true');args=p.parse_args()
    out={'construction':construction_report,'transport':transport_report,'sources':source_report}[args.mode]()
    print(json.dumps(out,default=base.matter.serial,indent=2))
    raise SystemExit(1 if not all(out['checks'].values()) else 2 if args.require_full_closure else 0)
