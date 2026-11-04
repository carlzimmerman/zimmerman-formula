"""Same uniform pole inequality with every fermionic exit Pauli blocked."""
import sys,os
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
from pathlib import Path
import json,time,resource,numpy as np
ROOT=Path(__file__).resolve().parents[3]

def main(output):
    start=time.monotonic()
    here=ROOT/'reviews/coupled_trapping_2026_11_04'
    p=json.loads((here/'microphysics/run_medium001/result.json').read_text())
    old=json.loads((here/'gravity_resonance/run_bound001/result.json').read_text())
    G=np.array(p['production_Gram_mu2']);boson=np.array(p['Gamma_SSS_matrix_mu'])
    fermion=np.array(p['Gamma_FFS_matrix_mu']);vac=np.array(p['Gamma_other_matrix_mu'])
    sigma=2/(p['mC']*p['Mpole']**2)*float(np.trace(G@np.linalg.inv(boson)))
    ratio=sigma/old['sigma_max_mu_minus2']
    rows=[]
    for prior in old['cases']:
        L=prior['pole_loss_integral_upper']*ratio
        final=1/(1/prior['initial_yield']+L)
        rows.append(dict(kind=prior['kind'],Tc_start_over_mu=prior['Tc_start_over_mu'],
            initial_yield=prior['initial_yield'],charged_yield_gate=prior['charged_yield_gate'],
            pole_loss_integral_upper=L,remaining_yield_lower=final,
            lower_over_charged_gate=final/prior['charged_yield_gate'],
            required_additional_pole_multiplier=(1/prior['charged_yield_gate']-1/prior['initial_yield'])/L))
    checks=dict(irreducible_bosonic_width_positive=min(np.linalg.eigvalsh(boson))>0,
        width_decomposition=np.linalg.norm(boson+fermion-vac)<1e-20,
        independently_reconstructed_medium_bound=abs(sigma/p['sigma_pair_v_all_FFS_blocked_uniform_bound_mu_minus2']-1)<1e-10,
        positive_rate_FFS_suppression_strengthens_envelope=ratio>1,
        protected_after_capture_still_above_gate=all(r['remaining_yield_lower']>r['charged_yield_gate'] for r in rows if r['kind']=='protected' and r['Tc_start_over_mu']<=.001))
    result=dict(claim_id='CT09_BOSONIC_WIDTH_POLE_DEPLETION_BOUND',checks={k:bool(v) for k,v in checks.items()},
        sigma_max_all_FFS_blocked_mu_minus2=sigma,relative_to_vacuum=ratio,cases=rows,
        interpretation='After capture (Tc/mu<=.001), even this enlarged fixed-pole positive-rate envelope misses the protected gate. Starting the ideal envelope at the earlier origin instability does allow the gate, so no blanket early-history exclusion.',
        scope='Fermion exits may be entirely removed but bosonic SSS widths retain vacuum kinematics/couplings and no suppression below spontaneous rates. Not a full medium selfenergy or all-channel network.',
        runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('checks','sigma_max_all_FFS_blocked_mu_minus2','relative_to_vacuum','runtime_seconds','peak_rss_bytes')}))
    assert all(checks.values()), checks
if __name__=='__main__':main(sys.argv[1])
