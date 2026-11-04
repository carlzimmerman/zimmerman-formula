"""Finite local decay/inverse integration controls, not a relic calculation."""
import os,sys
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='1'
import json,math,time,resource
from pathlib import Path
import numpy as np
from common import CommonBackground
from loop_transport import pole_events,POLE

def main(output):
    start=time.monotonic()
    bg=CommonBackground();data=bg.at(POLE)
    q=np.geomspace(.001,30000.,72)
    edges=np.r_[0.,np.sqrt(q[:-1]*q[1:]),q[-1]**2/math.sqrt(q[-2]*q[-1])]
    W=np.diff(edges**3)/3
    op=pole_events(data,1e-6,q,W)
    n=len(q);checks={};rows=[]
    packet=json.loads((Path(__file__).resolve().parents[1]/'decay/INTERFACE.json').read_text())
    # Finite projection quantum equilibrium; includes inverse vector channels.
    temperature=.002
    thermal=1/np.expm1(op.energy/temperature)
    fermions=op.eta<0
    thermal[fermions]=1/(np.exp(op.energy[fermions]/temperature)+1)
    audit=op.audit(thermal)
    checks['quantum_detailed_balance']=audit['detailed_balance_RHS_relative']<1e-10
    checks['all_vector_groups_bosonic']=all(np.all(op.eta[i*n:(i+1)*n]==1) for i,g in enumerate(op.groups) if g['kind']=='V')
    for parent in packet['parents']:
        f=np.zeros(len(op.measure));p=op.by[parent['id']]
        # Only soft NR parents; hard daughter support is present explicitly.
        f[p*n:(p+1)*n]=1e-4*np.exp(-q*q/8)
        rhs=op.number_rhs(f);group=rhs.reshape(30,n).sum(axis=1)
        expected=parent['total_width_mu']*np.sum(op.measure[p*n:(p+1)*n]*f[p*n:(p+1)*n]*op.masses[p]/op.energies[p])
        energy_residual=abs(op.energy@rhs)/max(expected*op.masses[p],1e-300)
        chi=group[op.by['F1_1']]/expected
        total_daughters=(sum(group)-group[p])/expected
        omission=(op.omitted_by_parent@f)/expected
        loss=-group[p]/expected
        checks[parent['id']+'_vacuum_loss']=abs(loss-1)<1e-10
        checks[parent['id']+'_chi_branch']=abs(chi-parent['chi_partner_branch'])<1e-10
        checks[parent['id']+'_two_daughters']=abs(total_daughters-2)<1e-10
        checks[parent['id']+'_energy']=energy_residual<1e-10
        checks[parent['id']+'_support']=omission<1e-10
        rows.append(dict(parent=parent['id'],loss_ratio=loss,chi_per_decay=chi,daughter_number=total_daughters,
            energy_residual=energy_residual,omitted_physical_rate_fraction=omission,
            group_number_rates=group.tolist(),parent_mass_relative_deviation=op.packet_mass_relative_deviations[parent['id']]))
    # Interior nonthermal affinity/Jacobian and entropy; no zero logs.
    f=.21*thermal*(1+.07*np.sin(np.arange(len(thermal))))
    rhs=op.number_rhs(f);av=1+op.eta*f
    entropy=-np.log(f/av)@rhs
    direction=.01*op.measure*f*np.cos(np.arange(len(f))*.23)
    eps=1e-4
    difference=(op.number_rhs(f+eps*direction/op.measure)-op.number_rhs(f-eps*direction/op.measure))/(2*eps)
    analytic=op.number_jacobian(f)@direction
    jac=float(np.linalg.norm(difference-analytic)/max(np.linalg.norm(analytic),1e-300))
    checks['nonthermal_entropy']=entropy>=0
    checks['number_jacobian']=jac<2e-6
    result=dict(claim_id='CC11_CHECKED_POLE_LOOP_DECAY_INVERSE_OPERATOR',checks={k:bool(v) for k,v in checks.items()},
        case=dict(q=q.tolist(),t=1e-6,rows=rows,equilibrium_audit=audit,entropy_production=float(entropy),jacobian_relative_error=jac,
            groups=[g['id'] for g in op.groups]),runtime_seconds=time.monotonic()-start,
        peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        scope='Fixed local pole, isotropic rep-averaged scalar parents and spin-symmetric daughters. Retains χ, each partner and gauge sector plus inverses. No evolving cosmological state; no extrapolation of pole widths in x.')
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(checks=result['checks'],rows=rows,jacobian=jac)),flush=True)
    assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
