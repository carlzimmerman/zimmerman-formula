"""Audit the returned v7 root against its own reconstructed true stage."""
from direct_orbit import *

def main_stage(output,h='0.0001'):
    start=time.monotonic();h=float(h);saved=json.loads((BASE/'integration/run_initial_vector001/result.json').read_text());s=saved['state'];q=np.array(saved['case']['q']);W=np.array(saved['case']['W']);bg=CommonBackground();model=PreciseCommonOrbit(bg,q,W,8);model.J0=s['J0'];model.last_x=s['xmid'];factory=VectorFactory(BASE/'vectors/run_table003/result.json');old=QuantumState(model.measure,model.eta,Z=s['Z'],holes=s['hole_flags']);Y0=old.numbers();J0=s['J'];calls=[]
    def op(background,xs,weights,t,q,W):
        events=factory.averaged_events(background,xs,weights,t,q,W,angle_order=2)
        calls.append(dict(xs=np.array(xs).copy(),weights=np.array(weights).copy(),events=events));return events
    result=dict(claim_id='CC11_INDEPENDENT_V7_TRUE_STAGE_RESIDUAL',dN=h,completed=False)
    try:
        new,Jn,on,work,info=averaged_step(model,bg,op,0.,old,J0,h,geometry='midpoint',max_outer=10,outer_tol=2e-5)
        Nm=h/2;Ja=J0*math.exp(-3*h/2);Jb=Jn*math.exp(3*h/2);Y1=new.numbers();true=model.orbit(Nm,(Y0+Y1)/2,J=(Ja+Jb)/2)
        used=calls[-1];scale=max((true['x_outer']-true['x_inner'])/2,1e-12);gerr=float(max(abs(used['xs']-true['xs']))/scale);werr=float(max(abs(used['weights']-true['weights']))*len(true['weights']))
        dt=h/model.hubble(Nm);evtrue=factory.averaged_events(bg,true['xs'],true['weights'],T0*math.exp(-Nm),q,W,angle_order=2)
        Rused=Y1-Y0-dt*new.rhs(used['events']);Rtrue=Y1-Y0-dt*new.rhs(evtrue);signed_used=used['events'].energy@Rused;signed_true=evtrue.energy@Rtrue
        # Verify that a new seeded solve still uses the same OLD physical state,
        # with the returned state only a Newton guess.
        recheck,reinfo=implicit_step(evtrue,old,dt,tol=2e-8,maxiter=60,number_floor=1e-14,guess=new)
        result.update(completed=True,initial_J=J0,collision_J_old=Ja,collision_J_new=Jb,final_J=Jn,endpoint_energy_work=on['E']+work-s['E'],
          information=info,operator_calls=len(calls),true_stage_x_scaled_error=gerr,true_stage_weight_scaled_error=werr,
          residual_used_L1=float(sum(abs(Rused))),residual_true_L1=float(sum(abs(Rtrue))),true_vs_used_rhs_L1_dt=float(sum(abs(Rtrue-Rused))),
          residual_used_energy_contraction=float(signed_used),residual_true_energy_contraction=float(signed_true),
          true_stage_resolve_Y_relative=float(sum(abs(recheck.numbers()-Y1))/sum(abs(Y1))),true_stage_resolve_info=reinfo,
          stage_is_harmonic=bool(true['harmonic']),old_numbers_unchanged=bool(np.array_equal(old.numbers(),Y0)))
    except RuntimeError as exc:result['failure']=str(exc)
    result.update(runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        scope='Actual fresh30group v7 step and true midpoint-action/population stage reconstruction; source conserved endpoint energy is structural, not an independent trajectory check.')
    Path(output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('information','true_stage_resolve_info')}),flush=True);assert result['completed'],result
if __name__=='__main__':main_stage(*sys.argv[1:])
