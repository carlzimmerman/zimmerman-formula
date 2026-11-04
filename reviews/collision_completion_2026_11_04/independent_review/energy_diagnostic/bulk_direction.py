"""Explicitly restricted warm tangent with a recorded removed-energy budget."""
import direction_precise as d

def main(out):
    np=d.np;start=d.time.monotonic();path=d.BASE/'history/run_refine002/result.json';packet=d.json.loads(path.read_text());s=packet['state'];q=np.array(packet['case']['q']);W=np.array(packet['case']['W']);bg=d.ConsistentVertexBackground(d.BASE/'cascades/run_vertices001/result.json');rows=[]
    for phases in (8,16,24):
        model=d.GenericOrbit(bg,q,W,phases);model.J0=s['J0'];model.last_x=s['xmid'];N=s['N'];J=s['J'];state=d.QuantumState(model.measure,model.eta,Z=s['Z'],holes=s['hole_flags']);Y=state.numbers();orb=d.precise_orbit(model,N,Y,J);C,Eavg,cov=d.moments(model,bg,N,Y,state,orb);H=model.hubble(N);t=d.T0*d.math.exp(-N);D=C/H;dJ=cov/(orb['omega']*H);testmax=1e-7
        removed=(Y+1.25*testmax*D<0)|((model.eta<0)&(Y+1.25*testmax*D>model.measure));bulk=D.copy();bulk[removed]=0
        removed_signed=t**3*float(Eavg@(D-bulk));removed_abs=t**3*float(abs(Eavg)@abs(D-bulk));scale=max(abs(t**3*float(Eavg@D)),abs(orb['omega']*dJ),1e-300)
        predicted=orb['omega']*dJ+t**3*float(Eavg@bulk);trials=[]
        for epsilon in (1e-7,5e-8,1e-8,5e-9):
            yp=Y+epsilon*bulk;jp=J+epsilon*dJ;valid=bool(np.all(yp>=0) and np.all(yp[model.eta<0]<=model.measure[model.eta<0]) and jp>0);record=dict(epsilon=epsilon,valid=valid)
            if valid:
                pert=d.precise_orbit(model,N,yp,jp);derivative=(pert['E']-orb['E'])/epsilon;record.update(derivative=derivative,predicted_linear_derivative=predicted,defect=derivative-predicted,scaled_defect=(derivative-predicted)/scale)
            trials.append(record)
        rows.append(dict(phase_nodes=phases,N=N,removed_nodes=int(sum(removed)),removed_node_indices=np.where(removed)[0].tolist(),removed_number_direction_L1=float(sum(abs(D-bulk))),removed_signed_energy_per_N=removed_signed,removed_absolute_energy_per_N=removed_abs,removed_energy_over_collision_scale=removed_abs/scale,
            collision_energy_scale=scale,predicted_bulk_energy_derivative=predicted,trials=trials,defect_extrapolation=d.intercepts(trials,'defect'),scaled_defect_extrapolation=d.intercepts(trials,'scaled_defect')))
        print(d.json.dumps({k:v for k,v in rows[-1].items() if k not in ('removed_node_indices','trials')}),flush=True)
    result=dict(rows=rows,runtime_seconds=d.time.monotonic()-start,peak_rss_bytes_macos=d.resource.getrusage(d.resource.RUSAGE_SELF).ru_maxrss,
        scope='Warm physical trial states with a specified subset of inadmissibly fast number-direction components removed. Original action direction retained; the missing linear energy contribution is reported and subtracted. This is not the full physical collision direction and supplies no universal omitted-direction theorem.')
    d.Path(out).write_text(d.json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main(d.sys.argv[1])
