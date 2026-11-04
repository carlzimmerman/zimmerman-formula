"""Fixed-duration averaged v7 temporal refinement, fresh input and ledger."""
from direct_orbit import *

def main_average(output,count='2'):
    start=time.monotonic();count=int(count);saved=json.loads((BASE/'integration/run_initial_vector001/result.json').read_text());s=saved['state'];q=np.array(saved['case']['q']);W=np.array(saved['case']['W']);direct=json.loads((Path(__file__).parent/'run_direct128/result.json').read_text());target=direct['state']['N'];bg=CommonBackground();model=PreciseCommonOrbit(bg,q,W,16);model.J0=s['J0'];model.last_x=s['xmid'];factory=VectorFactory(BASE/'vectors/run_table003/result.json');state=QuantumState(model.measure,model.eta,Z=s['Z'],holes=s['hole_flags']);initial=model.orbit(0.,state.numbers(),E=s['E']);J=initial['J'];N=work=0.;history=[];reason='requested same-time endpoint reached'
    def op(background,xs,weights,t,q,W):return factory.averaged_events(background,xs,weights,t,q,W,angle_order=2)
    def save():
        Y=state.numbers();directY=np.array(direct['state']['Y']);directgroup=directY.reshape(model.ns,model.n).sum(axis=1);group=Y.reshape(model.ns,model.n).sum(axis=1)
        result=dict(claim_id='CC11_AVERAGED_ONE_PERIOD_TIME_REFINEMENT',completed=len(history)==count,reason=reason,requested_substeps=count,accepted=len(history),phase_nodes=16,target_N=target,initial_E=s['E'],initial_J=initial['J'],history=history,
          comparison=dict(relative_J=(J-direct['state']['J'])/direct['state']['J'],Y_L1_relative=float(sum(abs(Y-directY))/sum(abs(directY))),
            group_ratios_to_direct128={g['id']:float(a/b) for g,a,b in zip(model.groups,group,directgroup) if b>1e-28}),
          state=dict(N=N,J=J,work=work,E=initial['E'] if not history else history[-1]['E'],Y=Y.tolist(),Z=state.Z.tolist(),hole_flags=state.holes.tolist()),
          runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
          scope='Fresh phase16 averaged v7 BE trajectory over exactly direct128 final N/proper time, with independent FRW work carried from0. No phase or full-history convergence theorem.')
        Path(output).write_text(json.dumps(result,indent=2)+'\n');return result
    save()
    for k in range(count):
        if time.monotonic()-start>195:reason='bounded prefix before next averaged nonlinear interval';break
        new,Jn,on,dw,info=averaged_step(model,bg,op,N,state,J,target/count,geometry='midpoint',max_outer=10,outer_tol=2e-7)
        state=new;J=Jn;N=(k+1)*target/count;work+=dw;f,av=state.arrays()
        history.append(dict(N=N,J=J,E=on['E'],work=work,energy_work_residual=on['E']+work-s['E'],
          residual_over_initial_excitation=(on['E']+work-s['E'])/direct['initial']['excitation'],
          numbers_by_group=state.numbers().reshape(model.ns,model.n).sum(axis=1).tolist(),
          min_f=float(min(f)),max_fermion_f=float(max(f[model.eta<0])),info=info))
        result=save();print(json.dumps(dict(k=k+1,N=N,runtime=result['runtime_seconds'],comparison=result['comparison'])),flush=True)
    result=save();assert result['completed'],reason
if __name__=='__main__':main_average(*sys.argv[1:])
