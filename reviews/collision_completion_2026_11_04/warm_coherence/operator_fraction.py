"""Whole25 exact-angle charged RHS fraction and unequal-diagonal control."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[k]='1'
import json,time,resource,math
import numpy as np
from pathlib import Path
from matrix_api import *
from angular_fast import exact_events_fast

def main(out):
    start=time.monotonic();here=Path(__file__).resolve().parent;local=json.loads((here/'run_local001/result.json').read_text());rows=[]
    for record in local['rows']:
        snap=snapshot(ROOT/record['input']);data=snap['bg'].at(snap['x']);pid=record['parent_id'];wm={key:{k:np.asarray(v) for k,v in w.items()} for key,w in record['matrices'].items()}
        keys=list(wm);loss=sum(w['loss'] for w in wm.values());gain=sum(w['gain'] for w in wm.values());D=loss-gain
        weighted=snap['t']**3*snap['W']/(2*math.pi**2);diag_channels={key:0. for key in keys};normchannels={key:0. for key in keys}
        offdiag=[];basis_commutators=[]
        for i in range(len(snap['q'])):
            fdiag=np.diag(gain[i])/np.diag(D[i]);rho=np.diag(fdiag)
            fullrho=np.asarray(record['summary']['momentum_rows'][i]['rho_steady'])
            offdiag.append(float(np.linalg.norm(fullrho-np.diag(np.diag(fullrho)))/np.linalg.norm(fullrho)))
            for key,w in wm.items():
                dd=w['loss'][i]-w['gain'][i];gg=w['gain'][i]
                diag_channels[key]+=weighted[i]*float(np.trace(dd@rho-gg))
        def carriers(key):return int(key.split('|')[0].startswith(('Sc_','Fc_')))+int(key.split('|')[1].startswith(('Sc_','Fc_')))
        diagloss=-sum(carriers(key)*v for key,v in diag_channels.items())
        fullop=exact_events_fast(data,snap['t'],snap['q'],snap['W'],source=data['current_source'])
        f=snap['f'].ravel();av=snap['availability'].ravel();charged=np.repeat([g['charged'] for g in fullop.groups],len(snap['q']))
        rhs=fullop.number_rhs(f,av);allloss=-snap['t']**3*float(charged@rhs)
        filtered=dict(data,channels=[c for c in data['channels'] if c['parent']==pid])
        pop=exact_events_fast(filtered,snap['t'],snap['q'],snap['W'])
        prhs=pop.number_rhs(f,av);ploss=-snap['t']**3*float(charged@prhs)
        channels=record['summary'];C=channels['coherent_stationary_charged_loss_mu4'];I=channels['isotropic_stationary_charged_loss_mu4'];A=channels['actual_isotropic_charged_loss_mu4']
        chargedcurrent=np.zeros(len(fullop.measure));directsum=0.
        # A total-RHS replacement is only a local frozen-bath diagnostic.
        local_correction=C-A;newall=allloss+local_correction
        # Compare full and unequal-diagonal stationary parents in their stated
        # actual adapted basis; this control is basis-dependent by design.
        rows.append(dict(input=record['input'],N=record['N'],x=record['x'],
            whole25_exact_charged_loss_mu4=allloss,parent_only_existing_exact_charged_loss_mu4=ploss,
            actual_matrix_isotropic_charged_loss_mu4=A,
            parent_trace_normalization_relative=abs(ploss/A-1) if A else None,
            actual_parent_fraction_of_whole25=ploss/allloss if allloss else None,
            coherent_stationary_parent_charged_loss_mu4=C,isotropic_stationary_parent_charged_loss_mu4=I,
            unequal_diagonal_stationary_parent_charged_loss_mu4=diagloss,
            coherent_over_unequal_diagonal=C/diagloss if diagloss else None,
            unequal_diagonal_over_isotropic=diagloss/I if I else None,
            coherent_over_isotropic=C/I if I else None,
            maximum_adapted_basis_offdiagonal_density_fraction=max(offdiag),
            whole25_if_only_parent_replaced_mu4=newall,
            parent_stationary_replacement_change_over_whole25=local_correction/allloss if allloss else None,
            absolute_parent_coherence_correction_mu4=abs(C-I),
            absolute_parent_coherence_correction_over_whole25=abs(C-I)/abs(allloss) if allloss else None,
            exact_full_operator_energy_residual=float(fullop.energy_residual),
            full_operator_segments=len(fullop.coefficient),parent_operator_segments=len(pop.coefficient),
            scope='Local fixed-bath current only; whole25 comparison uses frozen interpolated background, matrix comparison uses exact actual-x vertices with same masses. Parent trace mismatch separately measures vertex interpolation. Unequal-diagonal control is basis-dependent, not a physical dephasing prescription.'))
    checks=dict(parent_normalization=all(r['parent_trace_normalization_relative']<.001 for r in rows),
                finite=all(math.isfinite(r['whole25_exact_charged_loss_mu4']) and math.isfinite(r['coherent_over_unequal_diagonal']) for r in rows),
                energy_projection=all(r['exact_full_operator_energy_residual']<1e-11 for r in rows))
    result=dict(claim_id='CC10_WARM_COHERENCE_WHOLE_OPERATOR_FRACTION',checks=checks,rows=rows,
                runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(out).write_text(json.dumps(serialize(result),indent=2)+'\n');print(json.dumps(serialize(result)));assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
