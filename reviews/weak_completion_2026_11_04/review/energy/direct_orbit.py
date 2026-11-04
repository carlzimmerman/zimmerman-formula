"""Independent direct field/quantum one-period control from fresh CC11 N=0.

No action/energy constraint updates the physical trajectory. Two explicit
field/FRW half flows surround one local positive BE collision at actual xmid.
Action is measured after the update, using adaptive quadrature of frozen U.
"""
import os,sys,json,math,time,resource
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='1'
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'reviews/weak_completion_2026_11_04'
for sub in ('integration','energy','vectors'):sys.path.insert(0,str(BASE/sub))
from common import CommonBackground,T0
from precise_common import PreciseCommonOrbit
from hybrid_number_v4 import QuantumState,implicit_step
from transport_v3 import VectorFactory
from split_energy_v7 import step as averaged_step
MASS=62.

def frozen_action(model,x,N,Y,E):
    xm,emin,left,right,limit=model.well(N,Y)
    if not emin<E<limit:raise RuntimeError('direct endpoint has no retained frozen closed orbit')
    def diff(xx):return float(model.potential(xx,N,Y)[0])-E
    L=brentq(diff,left,xm,xtol=1e-13);R=brentq(diff,xm,right,xtol=1e-13)
    mid=(L+R)/2;half=(R-L)/2
    def integrand(theta,period=False):
        xx=mid-half*math.cos(theta);dx=half*math.sin(theta);gap=-diff(xx)
        if gap<=0:raise RuntimeError('nonpositive adaptive orbit quadrature gap')
        return dx/math.sqrt(gap) if period else dx*math.sqrt(gap)
    J=math.sqrt(2*MASS)/math.pi*quad(integrand,0,math.pi,epsabs=1e-16,epsrel=2e-10,limit=160)[0]
    period=math.sqrt(2*MASS)*quad(lambda z:integrand(z,True),0,math.pi,epsabs=1e-3,epsrel=2e-9,limit=160)[0]
    return dict(J=J,period=period,minimum=emin,excitation=E-emin,inner=L,outer=R,xmid=xm)

def main(output,steps='128',coarse_path=''):
    start=time.monotonic();steps=int(steps);saved=json.loads((BASE/'integration/run_initial_vector001/result.json').read_text());case=saved['case'];s=saved['state'];q=np.array(case['q']);W=np.array(case['W'])
    bg=CommonBackground();model=PreciseCommonOrbit(bg,q,W,24);model.J0=s['J0'];model.last_x=s['xmid'];factory=VectorFactory(BASE/'vectors/run_table003/result.json')
    state=QuantumState(model.measure,model.eta,Z=s['Z'],holes=s['hole_flags']);Y=state.numbers();x=.18444259422092926;v=0.;N=0.;time_mu=0.;work=0.;Eref=s['E'];H0=model.hubble(0.)
    def obs(xx,vv,nn,yy):
        gas=model.gas(xx,nn,yy);rho=float(gas['rho'][0]);P=float(gas['pressure'][0]);kin=MASS*vv*vv/2
        return dict(E=float(model.v(xx))+rho+kin,gas=rho,P=P,kin=kin,force=float(model.v(xx,1))+float(gas['force'][0]),
          stress_work=3*model.hubble(nn)*(2*kin+rho+P),force_by=gas['force_by'][0])
    old=obs(x,v,N,Y);initial=frozen_action(model,x,N,Y,old['E']);duration=initial['period'];dt0=duration/steps;dt=dt0
    initial_counts=Y.reshape(model.ns,model.n).sum(axis=1);initial_charged=float(initial_counts@model.charged);history=[];accepted=rejected=0;failures=[]
    max_collision_E=max_BE_res=max_occ=max_omission=0.;max_iter=0;min_entropy=0.;max_Eres=0.;deadline=False
    def field_half(xx,vv,nn,yy,h):
        # Exact N(t) in the prescribed radiation H=H0 exp(-2N) background.
        nn1=.5*math.log(math.exp(2*nn)+2*H0*h);dn=nn1-nn
        oo=obs(xx,vv,nn,yy);vh=(vv-h*oo['force']/(2*MASS))*math.exp(-1.5*dn)
        xx1=xx+h*vh;end0=obs(xx1,vh,nn1,yy);vv1=vh*math.exp(-1.5*dn)-h*end0['force']/(2*MASS)
        oo1=obs(xx1,vv1,nn1,yy)
        # Independent trapezoidal integral of physical stress energy. Nothing
        # is set equal to a Hamiltonian difference.
        dw=h*(oo['stress_work']+oo1['stress_work'])/2
        return xx1,vv1,nn1,oo1,dw
    def record():
        nonlocal max_Eres
        measured=frozen_action(model,x,N,Y,old['E']);counts=Y.reshape(model.ns,model.n).sum(axis=1);f,av=state.arrays();res=old['E']+work-Eref;max_Eres=max(max_Eres,abs(res))
        row=dict(time_mu=time_mu,N=N,x=x,v=v,E=old['E'],work=work,energy_work_residual=res,
          residual_over_initial_excitation=res/initial['excitation'],residual_over_gas0=res/s['gas0'],
          measured_action=measured['J'],frozen_inner=measured['inner'],frozen_outer=measured['outer'],
          charged_fraction=float(counts@model.charged/initial_charged),numbers_by_group=counts.tolist(),
          vector_number=float(sum(counts[25:])),vector_force=float(sum(old['force_by'][25:])),
          all_neutral_force=float(old['force_by']@(~model.charged)),min_f=float(min(f)),max_fermion_f=float(max(f[model.eta<0])))
        history.append(row);return row
    reason='requested initial frozen-orbit duration reached';comparison=None
    def save():
        result=dict(claim_id='CC11_INDEPENDENT_DIRECT_FRESH_30GROUP_ORBIT',completed=time_mu>=duration*(1-1e-13),reason=reason,
          nominal_steps_per_initial_period=steps,accepted=accepted,rejected=rejected,rejection_reasons=failures,requested_duration=duration,
          initial=initial,history=history,groups=case['groups'],q=q.tolist(),W=W.tolist(),initial_energy_offset=history[0]['E']-Eref,
          max_collision_energy_change=max_collision_E,max_physical_BE_balance_L1=max_BE_res,max_occupation_change_per_step=max_occ,
          max_population_weighted_forward_omission=max_omission,max_Newton_iterations=max_iter,min_entropy_increment=min_entropy,
          maximum_recorded_energy_residual_over_initial_excitation=max_Eres/initial['excitation'],averaged_comparison=comparison,
          state=dict(N=N,x=x,v=v,Y=Y.tolist(),Z=state.Z.tolist(),hole_flags=state.holes.tolist(),E=old['E'],work=work,J=history[-1]['measured_action']),
          runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
          scope='Direct unaveraged actual scalar/quantum S/F/polarized-vector finite40node trajectory. Shared collision backend and BE solver; independent explicit field/collision composition and stress-energy work. No energy/action root determines accepted field or populations. Not a full history or cold-state proof.')
        if coarse_path and Path(coarse_path).is_file():
            coarse=json.loads(Path(coarse_path).read_text());ss=coarse['state'];result['direct_resolution_comparison']=dict(coarse_completed=coarse['completed'],same_duration_relative=abs(coarse['requested_duration']/duration-1),
                Y_L1_relative=float(sum(abs(Y-np.array(ss['Y'])))/sum(abs(Y))),J_relative=float((history[-1]['measured_action']-ss['J'])/ss['J']),x_difference=x-ss['x'],v_difference=v-ss['v'],
                coarse_energy_residual=coarse['history'][-1]['energy_work_residual'],fine_energy_residual=history[-1]['energy_work_residual'])
        Path(output).write_text(json.dumps(result,indent=2)+'\n');return result
    record();save()
    while time_mu<duration*(1-1e-13):
        if time.monotonic()-start>195:reason='bounded durable prefix before next collision';deadline=True;break
        h=min(dt,dt0,duration-time_mu)
        try:
            xm,vm,Nm,before,dw1=field_half(x,v,N,Y,h/2)
            local=factory.full_events(bg.at(xm),T0*math.exp(-Nm),q,W,angle_order=2)
            ns,info=implicit_step(local,state,h,tol=2e-8,maxiter=60,number_floor=1e-14)
            Yn=ns.numbers();after=obs(xm,vm,Nm,Yn);collision_delta=after['E']-before['E']
            xn,vn,Nn,on,dw2=field_half(xm,vm,Nm,Yn,h/2)
            f0=state.arrays()[0];f1=ns.arrays()[0];inc=float(local.included_by_parent@f0);om=float(local.omitted_by_parent@f0)
            physical_balance=float(sum(abs(Yn-Y-h*ns.rhs(local))))
            if min(f1)<0 or max(f1[model.eta<0])>1:raise RuntimeError('physical collision bounds failed')
            max_collision_E=max(max_collision_E,abs(collision_delta));max_BE_res=max(max_BE_res,physical_balance);max_occ=max(max_occ,float(max(abs(f1-f0))));max_iter=max(max_iter,info['iterations']);max_omission=max(max_omission,om/max(inc+om,1e-300));min_entropy=min(min_entropy,ns.entropy()-state.entropy())
            x,v,N,Y,state,old=xn,vn,Nn,Yn,ns,on;time_mu+=h;work+=dw1+dw2;accepted+=1;dt=min(dt0,dt*1.25)
            if accepted%max(1,steps//8)==0 or time_mu>=duration*(1-1e-13):
                rr=record();save();print(json.dumps(dict(accepted=accepted,time_fraction=time_mu/duration,N=N,x=x,action=rr['measured_action'],energy_ratio=rr['residual_over_initial_excitation'],runtime=time.monotonic()-start)),flush=True)
        except RuntimeError as exc:
            failures.append(str(exc));rejected+=1;dt=h/2
            if dt<dt0/32:reason='local nonlinear solve failed at refinement floor: '+str(exc);break
        if accepted>steps*8:reason='bounded accepted-step budget';break
    if history[-1]['time_mu']!=time_mu:record()
    save()
    # One averaged BE interval with the identical physical proper-time endpoint;
    # direct and averaged states are compared, never forced to agree.
    if time_mu>=duration*(1-1e-13) and time.monotonic()-start<160:
        try:
            avgmodel=PreciseCommonOrbit(bg,q,W,16);avgmodel.J0=s['J0'];avgmodel.last_x=s['xmid']
            st=QuantumState(avgmodel.measure,avgmodel.eta,Z=s['Z'],holes=s['hole_flags']);o0=avgmodel.orbit(0.,st.numbers(),E=Eref)
            def op(background,xs,weights,t,q,W):return factory.averaged_events(background,xs,weights,t,q,W,angle_order=2)
            an,aj,ao,aw,ai=averaged_step(avgmodel,bg,op,0.,st,o0['J'],N,geometry='midpoint',max_outer=10,outer_tol=2e-7)
            comparison=dict(completed=True,N=N,initial_phase16_J=o0['J'],final_J=aj,work=aw,independent_work_residual=ao['E']+aw-Eref,
                direct_J=history[-1]['measured_action'],relative_action_difference=(history[-1]['measured_action']-aj)/aj,
                Y_L1_relative=float(sum(abs(Y-an.numbers()))/sum(abs(Y))),averaged_numbers_by_group=an.numbers().reshape(model.ns,model.n).sum(axis=1).tolist(),info=ai)
        except RuntimeError as exc:comparison=dict(completed=False,failure=str(exc))
    result=save();print(json.dumps(dict(completed=result['completed'],reason=reason,accepted=accepted,rejected=rejected,runtime=result['runtime_seconds'],RSS=result['peak_rss_bytes_macos'],averaged_comparison=comparison is not None)),flush=True)
    assert result['completed'],reason
if __name__=='__main__':main(*sys.argv[1:])
