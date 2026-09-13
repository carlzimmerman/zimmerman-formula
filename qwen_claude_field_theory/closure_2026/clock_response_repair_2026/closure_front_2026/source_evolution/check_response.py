#!/usr/bin/env python3
"""Independent residual/refinement checks for a bounded forced Fourier family."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import time
import numpy as np
import evolve as e


def normdiff(x,y):
    return float(np.max(np.abs(x-y))/max(float(np.max(np.abs(y))),1e-30))


def derivative(values,h):
    return (values[:-4]-8*values[1:-3]+8*values[3:-1]-values[4:])/(12*h)


def one(k,gamma,tmax,amp):
    started=time.monotonic()
    m=e.Model(tmax,gamma)
    grid=np.linspace(0.,tmax,129)
    settings=[('coarse','DOP853',1e-6,.08),('medium','DOP853',1e-9,.04),
              ('fine','DOP853',3e-12,.02),('radau','Radau',1e-10,.04)]
    solutions={}
    potentials={}
    cost={}
    for name,method,tol,step in settings:
        sol=e.integrate_shifted(m,k,amp,method=method,rtol=tol,max_step=step)
        solutions[name]=sol
        potentials[name]=np.array([[e.fields(t,sol.sol(t),m,k,amp)[x]
                                   for x in ('Phi','Psi')] for t in grid])
        cost[name]=dict(nfev=sol.nfev,nsteps=len(sol.t)-1)
    fine=solutions['fine']
    errors={name:normdiff(potentials[name],potentials['fine']) for name in ('coarse','medium','radau')}
    fd=[]
    # Independent time derivatives: differentiate dense solutions, not the RHS.
    # Both grid sizes are retained; a rank/no-slip identity is not a substitute.
    for count in (129,257,513):
        tt=np.linspace(0.,tmax,count)
        state=fine.sol(tt).T
        obs=[e.fields(t,st,m,k,amp) for t,st in zip(tt,state)]
        h=tt[1]-tt[0]
        ud=derivative(np.array([o['u'] for o in obs]),h)
        pd=derivative(state[:,1],h)
        zd=derivative(state[:,0],h)
        actual=obs[2:-2]
        phi_fd=np.array([o['n'] for o in actual])+ud
        psi=np.array([o['Psi'] for o in actual])
        p_target=np.array([o['pdot'] for o in actual])
        z_target=np.array([o['zdot'] for o in actual])
        fd.append(dict(points=count,slip_from_differenced_shift=normdiff(phi_fd,psi),
                       canonical_p_residual=float(np.max(np.abs(pd-p_target))/amp),
                       canonical_z_residual=float(np.max(np.abs(zd-z_target))/amp)))
    c0=e.coefficients(m,0.,k,amp)
    cf=e.coefficients(m,tmax,k,amp)
    phi_final=potentials['fine'][-1,0]
    slip=normdiff(potentials['fine'][:,0],potentials['fine'][:,1])
    # Check ALL raw auxiliary Euler rows, not just the solved momentum row.
    residual=0.
    minA=float('inf'); minDen=float('inf')
    maxpert=0.
    for t in grid:
        st=fine.sol(t); c=e.coefficients(m,t,k,amp); f=e.fields(t,st,m,k,amp)
        v,n,sig,lap=(f[x] for x in ('zdot','n','sigma','LapB'))
        terms=[2*(v-c['Theta']*n)+c['W']*sig,
               6*c['Theta']*v+2*c['Sigma']*n-2*c['Theta']*lap+2*c['r']*st[0]+c['D']*sig-c['rho'],
               c['D']*n-3*c['W']*v+c['W']*lap+(c['E']-c['C']*c['r'])*sig,
               st[1]/c['a']**3-2*lap]
        residual=max(residual,max(abs(x) for x in terms)/amp)
        minA=min(minA,c['A']);minDen=min(minDen,c['den'])
        maxpert=max(maxpert,abs(n),abs(st[0]),abs(f['Phi']),abs(k*sig/c['a']))
    summary=dict(k=k,gamma=gamma,a_final=cf['a'],tmax=tmax,amplitude=amp,
                 response_initial=-2*c0['r']*potentials['fine'][0,0]/c0['rho'],
                 response_final=-2*cf['r']*phi_final/cf['rho'],
                 Phi_final=phi_final,Psi_final=potentials['fine'][-1,1],
                 errors=errors,algebraic_slip_relative=slip,
                 max_auxiliary_residual_per_amplitude=residual,
                 min_sampled_A=minA,min_sampled_denominator=minDen,
                 max_sampled_perturbation=maxpert,finite_difference=fd,cost=cost,
                 elapsed_seconds=time.monotonic()-started)
    # A failing convergence check stops certification; it never changes physics.
    checks=dict(solver_agreement=errors['radau']<1e-6,refinement_agreement=errors['medium']<1e-6,
                independent_shift_slip=fd[-1]['slip_from_differenced_shift']<1e-5,
                time_euler_residual=max(fd[-1]['canonical_p_residual'],fd[-1]['canonical_z_residual'])<1e-5,
                momentum_residual_refines=(fd[2]['canonical_p_residual']<fd[1]['canonical_p_residual']<fd[0]['canonical_p_residual']
                                          or max(x['canonical_p_residual'] for x in fd)<1e-9),
                raw_auxiliary_rows=residual<1e-7,
                divided_branch_regular=minA>0 and minDen>0)
    checks={key:bool(value) for key,value in checks.items()}
    summary['checks']=checks
    print(json.dumps({x:summary[x] for x in ('k','gamma','response_final','errors','checks')}),flush=True)
    return summary


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--k',type=float,nargs='+',default=[.3,1.,3.,10.,30.,100.])
    p.add_argument('--tmax',type=float,default=4.)
    args=p.parse_args()
    # Warm symbolic expressions before parallel calls; each task owns its model.
    e.constitutive.functions()
    jobs=[(k,g,args.tmax,1e-7) for g in (0.,1e-6) for k in args.k]
    with ThreadPoolExecutor(max_workers=2) as pool:
        rows=list(pool.map(lambda v:one(*v),jobs))
    model=e.Model(args.tmax)
    amplitudes=[1e-8,1e-7,1e-6]
    scaled=[]
    for amp in amplitudes:
        sol=e.integrate_shifted(model,3.,amp,rtol=1e-11,max_step=.02)
        f=e.fields(args.tmax,sol.sol(args.tmax),model,3.,amp)
        scaled.append(dict(amplitude=amp,Phi_final=f['Phi'],Phi_per_amplitude=f['Phi']/amp))
    slopes=np.diff(np.log(np.abs([r['Phi_final'] for r in scaled])))/np.diff(np.log(amplitudes))
    result=dict(scope='Finite-time linear signed conserved probe; dimensionless radiation-free reference history',
                theory_status='OPEN',parameter_functions_changed=False,
                initial_data='zeta(0)=zetadot(0)=0; p(0)=a(0)^3 F(0), auxiliary fields solved',
                source='rho=amplitude/a^3, deltaT0i=deltaTij=0, zero homogeneous probe density',
                response_definition='-2 (k/a)^2 Phi/rho, bare Einstein M2=1 reference, not measured G',
                rows=rows,amplitude_scaling=scaled,measured_log_slopes=list(slopes),
                all_checks=all(all(row['checks'].values()) for row in rows),
                non_claims=['Not a positive-density galaxy, cosmological transfer function, PPN fit or CMB test',
                            'Positive sampled A/denominator is not global stability or nonlinear DOF count',
                            'Linear source scaling does not exclude singular or nonperturbative branches'])
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    return 0 if result['all_checks'] else 1


if __name__=='__main__':
    raise SystemExit(main())
