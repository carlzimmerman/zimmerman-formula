"""Collision/expansion tangent test of the orbit energy, without history evolution."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import math,json,time,resource,gc
import numpy as np
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'reviews/collision_completion_2026_11_04'
sys.path.insert(0,str(BASE/'cascades'))
from angular_fast import exact_events_fast
sys.path.insert(0,str(BASE/'integration'))
from consistent_background import ConsistentVertexBackground
from generic_orbit import GenericOrbit,T0
sys.path.insert(0,str(BASE/'integration_solver'))
from protocol_holes import QuantumState


def precise_orbit(model,N,Y,J):
    approximate=model.orbit(N,Y,J=J);emin=approximate['minimum'];energy=approximate['E'];gap=energy-emin
    lo=emin+gap*.7;hi=energy+gap*.3
    def difference(en):return model.orbit(N,Y,E=en)['J']-J
    energy=brentq(difference,lo,hi,xtol=1e-30,rtol=1e-15)
    return model.orbit(N,Y,E=energy)


def moments(model,bg,N,Y,state,orb):
    t=T0*math.exp(-N);C=[];energies=[]
    for x in orb['xs']:
        data=bg.at(float(x));ev=exact_events_fast(data,t,model.q,model.W,source=data['current_source'])
        C.append(state.rhs(ev));energies.append(ev.energy.copy());del ev;gc.collect()
    C=np.array(C);energies=np.array(energies);w=orb['weights'];avg=w@C;Eavg=w@energies
    cov=t**3*float(np.sum(w[:,None]*(energies-Eavg)*(C-avg)))
    return avg,Eavg,cov


def one_step(bg):
    original=json.loads((BASE/'integration/run_fresh_exact002/result.json').read_text());s=original['state'];control=json.loads((BASE/'history/run_control_log002/result.json').read_text());saved=next(r for r in control['rows'] if r['solver']=='log')
    q=np.array(original['case']['q']);W=np.array(original['case']['W']);model=GenericOrbit(bg,q,W,8);model.J0=s['J0'];model.last_x=s['xmid'];N=s['N'];h=control['dN'];H0=model.hubble(N);H1=model.hubble(N+h);t=T0*math.exp(-N)
    old=QuantumState(model.measure,model.eta,Z=s['Z'],holes=s['hole_flags']);new=QuantumState(model.measure,model.eta,Z=saved['Z'],holes=saved['hole_flags']);Y0=old.numbers();Y1=new.numbers();J0=original['case']['history'][-1]['action'];orb=precise_orbit(model,N,Y0,J0)
    C0,Eavg,cov0=moments(model,bg,N,Y0,old,orb);Cbe,_,_=moments(model,bg,N,Y1,new,orb)
    k0=-3+cov0/(orb['omega']*J0*H0);Jp=J0*math.exp(h*k0);pred=precise_orbit(model,N+h,Y1,Jp);C1,Eavg1,cov1=moments(model,bg,N+h,Y1,new,pred);k1=-3+cov1/(pred['omega']*Jp*H1);Jn=J0*math.exp(h*(k0+k1)/2)
    final=precise_orbit(model,N+h,Y1,Jn);Jcollision=Jn*math.exp(3*h);collision=precise_orbit(model,N,Y1,Jcollision)
    actual_deltaY=Y1-Y0;heun_deltaY=h*(C0/H0+C1/H1)/2
    population_term=t**3*float(Eavg@actual_deltaY);action_term=orb['omega']*(Jcollision-J0)
    flux_centering_mismatch=t**3*float(Eavg@(actual_deltaY-heun_deltaY));covariance_transport_remainder=action_term+t**3*float(Eavg@heun_deltaY)
    collision_energy_change=collision['E']-orb['E'];hamiltonian_curvature_remainder=collision_energy_change-population_term-action_term
    work=lambda o:3*float(o['weights']@(o['kin2']+o['gas']['rho']+o['gas']['pressure']))
    total_residual=final['E']-orb['E']+h*(work(orb)+work(final))/2
    equal_energy=model.orbit(N,Y1,E=orb['E'])
    return dict(input_BE='history/run_control_log002/result.json, log row',dN=h,phase_nodes=8,
        BE_physical_balance_L1=float(sum(abs(actual_deltaY-h/H0*Cbe))),predictor_corrector_logJ_estimator=abs(h*(k1-k0)/2),
        J0=J0,Jcollision_Heun=Jcollision,Jcollision_constant_energy=equal_energy['J'],
        relative_collision_action_difference=(Jcollision-equal_energy['J'])/J0,
        population_linear_energy=population_term,action_linear_collision_energy=action_term,
        actual_collision_energy_change=collision_energy_change,BE_vs_Heun_number_flux_energy_mismatch=flux_centering_mismatch,
        covariance_geometry_log_transport_remainder=covariance_transport_remainder,hamiltonian_curvature_remainder=hamiltonian_curvature_remainder,
        decomposition_sum=flux_centering_mismatch+covariance_transport_remainder+hamiltonian_curvature_remainder,
        one_step_total_FRW_energy_residual=total_residual,total_residual_over_gas0=total_residual/s['gas0'],
        expansion_mixed_remainder=total_residual-collision_energy_change,
        scope='Existing physical frozen-geometry BE step re-used; log-action Heun/FRW update reconstructed for diagnosis. BE dt uses Hstart as in saved control, not Hmid as in history driver. This is not a new accepted production-history step.')


def intercepts(rows,key):
    rows=[r for r in rows if r.get('valid') and key in r]
    if len(rows)<2:return dict(available=False)
    rows=sorted(rows,key=lambda r:r['epsilon'],reverse=True);values=[]
    for a,b in zip(rows[:-1],rows[1:]):
        ea,eb=a['epsilon'],b['epsilon'];values.append(dict(epsilon_large=ea,epsilon_small=eb,linear_intercept=(ea*b[key]-eb*a[key])/(ea-eb)))
    smallest=rows[-3:];scale=max(r['epsilon'] for r in smallest);x=np.array([r['epsilon']/scale for r in smallest]);y=np.array([r[key] for r in smallest]);degree=min(2,len(smallest)-1)
    p=np.polynomial.polynomial.polyfit(x,y,degree)
    return dict(available=True,pairwise_linear_intercepts=values,smallest_quadratic_intercept=float(p[0]),fit_epsilon_scale=scale)


def examine(path,phases,bg):
    started=time.monotonic();d=json.loads(path.read_text());s=d['state'];q=np.array(d['case']['q']);W=np.array(d['case']['W']);N=s['N']
    model=GenericOrbit(bg,q,W,phases);model.J0=s['J0'];model.last_x=s['xmid'];state=QuantumState(model.measure,model.eta,Z=s['Z'],holes=s['hole_flags']);Y=state.numbers();J=s['J'];orb=precise_orbit(model,N,Y,J=J);E=orb['E'];H=model.hubble(N);t=T0*math.exp(-N)
    cs=[];es=[];local=[];event_errors=[]
    for x,gas_energy in zip(orb['xs'],orb['gas']['energy']):
        data=bg.at(float(x));ev=exact_events_fast(data,t,q,W,source=data['current_source']);C=state.rhs(ev)
        cs.append(C);es.append(ev.energy.copy());local.append(float(ev.energy@C));event_errors.append(float(np.max(abs(ev.energy-gas_energy))))
        del ev;gc.collect()
    C=np.array(cs);energies=np.array(es);w=orb['weights'];Cavg=w@C;Eavg=w@energies
    centered=t**3*float(np.sum(w[:,None]*(energies-Eavg)*(C-Cavg)))
    raw=t**3*float(w@np.array(local)-Eavg@Cavg);dY=Cavg/H;dJ=centered/(orb['omega']*H)
    particle_term=t**3*float(Eavg@dY);action_term=orb['omega']*dJ;scale=max(abs(particle_term),abs(action_term),1e-300)
    bounds=[];negative=dY<0
    if np.any(negative):bounds.append(float(np.min(-Y[negative]/dY[negative])))
    upward=(model.eta<0)&(dY>0)
    if np.any(upward):bounds.append(float(np.min((model.measure[upward]-Y[upward])/dY[upward])))
    if dJ<0:bounds.append(-J/dJ)
    maxepsilon=min(bounds) if bounds else math.inf
    requested=[1e-6,1e-7,1e-8];epsilons=list(requested)
    # Extra halved points discriminate an O(epsilon) curvature term from a
    # nonzero tangent intercept. Every population/action trial is checked.
    epsilons.extend([5e-7,5e-8,5e-9])
    if maxepsilon<=1e-8 and maxepsilon>0:epsilons.extend([maxepsilon*.1,maxepsilon*.03,maxepsilon*.01])
    collision=[]
    for epsilon in sorted(set(epsilons),reverse=True):
        yp=Y+epsilon*dY;jp=J+epsilon*dJ
        valid=bool(np.all(yp>=0) and np.all(yp[model.eta<0]<=model.measure[model.eta<0]) and jp>0)
        rec=dict(epsilon=epsilon,requested=epsilon in requested,valid=valid)
        relative_parameters=max(float(np.max(abs(epsilon*dY)/model.measure)),abs(epsilon*dJ/J))
        if relative_parameters<64*np.finfo(float).eps:
            valid=False;rec.update(valid=False,error='parameter perturbation below double-precision resolution; no derivative inferred')
        if valid:
            try:
                pert=precise_orbit(model,N,yp,J=jp);derivative=(pert['E']-E)/epsilon
                rec.update(energy=pert['E'],delta_energy=pert['E']-E,derivative_E_per_N=derivative,
                    derivative_over_collision_energy_scale=derivative/scale,relative_J_variation=epsilon*dJ/J,
                    relative_number_L1=epsilon*float(sum(abs(dY)))/float(sum(Y)),target_action_error=pert['J']-jp)
            except RuntimeError as exc:rec.update(valid=False,error=str(exc))
        elif 'error' not in rec:rec['error']='quantum or positive-action bounds reject the linear tangent trial'
        collision.append(rec)
    work=3*float(w@(orb['kin2']+orb['gas']['rho']+orb['gas']['pressure']));expansion=[]
    for epsilon in (1e-5,1e-6,1e-7,1e-8):
        jp=J-3*J*epsilon;pert=precise_orbit(model,N+epsilon,Y,J=jp);derivative=(pert['E']-E)/epsilon
        expansion.append(dict(epsilon=epsilon,valid=True,derivative_E_per_N=derivative,
            expected_derivative=-work,residual=derivative+work,relative_residual=(derivative+work)/work))
    return dict(input=str(path.relative_to(ROOT)),N=N,phase_nodes=phases,E=E,J=J,omega=orb['omega'],H=H,gas0=s['gas0'],
        maximum_energy_grid_mismatch=max(event_errors),maximum_local_collision_energy_rate=max(abs(np.array(local))),
        weighted_local_collision_energy_per_N=t**3*float(w@local)/H,
        centered_covariance=centered,raw_covariance=raw,centered_vs_raw=centered-raw,
        particle_energy_derivative_term=particle_term,action_energy_derivative_term=action_term,
        algebraic_energy_derivative_sum=particle_term+action_term,collision_energy_scale=scale,
        dJ_per_N=dJ,dY_L1_per_N=float(sum(abs(dY))),maximum_physical_positive_epsilon=maxepsilon,
        collision_trials=collision,collision_extrapolation=intercepts(collision,'derivative_E_per_N'),
        collision_scaled_extrapolation=intercepts(collision,'derivative_over_collision_energy_scale'),
        expansion_trials=expansion,expansion_extrapolation=intercepts(expansion,'relative_residual'),runtime_seconds=time.monotonic()-started)


def main(out):
    start=time.monotonic();bg=ConsistentVertexBackground(BASE/'cascades/run_vertices001/result.json');rows=[]
    for name in ('integration/run_fresh_exact002/result.json','history/run_refine002/result.json'):
        for phases in (8,16,24):
            row=examine(BASE/name,phases,bg);rows.append(row)
            print(json.dumps(dict(input=name,phase_nodes=phases,maxepsilon=row['maximum_physical_positive_epsilon'],collision_intercept=row['collision_extrapolation'],scaled_intercept=row['collision_scaled_extrapolation'],expansion_intercept=row['expansion_extrapolation'],runtime=row['runtime_seconds'])),flush=True)
    decomposition=one_step(bg)
    result=dict(claim_id='CC10_INDEPENDENT_ORBIT_COLLISION_TANGENT_ENERGY_PRECISE',rows=rows,one_step_decomposition=decomposition,
        runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        scope='Frozen collision-direction and expansion-direction energy derivatives at two actual states. No history evolution, no repaired source model, no inference that a residual is wholly due to one mechanism.')
    Path(out).write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main(sys.argv[1])
