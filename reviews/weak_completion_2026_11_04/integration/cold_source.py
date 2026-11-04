"""Timing needed for a cold component, using the checked local decay packet."""
import os,sys
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import math,json,time,resource
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/production'))
from decays import Cosmology,summarize

def main(output):
    start=time.monotonic();cos=Cosmology();coarse=Cosmology(8193)
    packet=json.loads((ROOT/'reviews/weak_completion_2026_11_04/decay/INTERFACE.json').read_text())
    chi=packet['masses_GeV']['chi']/2e6;rows=[];checks={}
    for parent in packet['parents']:
        mass=parent['parent_mass_GeV']/2e6;width=parent['total_width_mu'];branch=parent['chi_partner_branch']
        baseline=summarize(cos,mass,chi,width,branch)
        refinement=summarize(coarse,mass,chi,width,branch,n=48)
        checks[parent['id']+'_baseline_refinement']=abs(refinement['mean_free_streaming_kpc']/baseline['mean_free_streaming_kpc']-1)<2e-4
        targets=[]
        for target in (1.,100.):
            # Bound a timing question only: no new width or birth history is
            # asserted. Earlier birth is the most favorable fixed-pole case.
            logfactor=brentq(lambda l:math.log(summarize(cos,mass,chi,width*math.exp(l),branch,n=48)['mean_free_streaming_kpc']/target),0.,60.,xtol=1e-10)
            factor=math.exp(logfactor)
            fine=summarize(cos,mass,chi,width*factor,branch,n=96)
            R=mass/(2*chi)
            logalpha=brentq(lambda l:cos.travel(np.array([math.exp(l)]),np.array([math.exp(l)/R]))[0]-target/1000.,-40.,-5.)
            ab=math.exp(logalpha)/R;earlytime=float(cos.time_at_a(ab))
            fraction=-math.expm1(-earlytime/baseline['lifetime_seconds'])
            err=abs(fine['mean_free_streaming_kpc']/target-1)
            checks[parent['id']+'_target_'+str(target)]=err<2e-4 and factor>1 and 0<fraction<1
            targets.append(dict(target_mean_free_streaming_kpc=target,required_total_width_multiplier_fixed_branch=factor,
                verified_mean_free_streaming_kpc=fine['mean_free_streaming_kpc'],
                relative_target_refinement_error=err,monoenergetic_birth_time_cut_seconds=earlytime,
                exponential_number_fraction_with_single_cohort_distance_below_target=fraction))
        rows.append(dict(parent=parent['id'],baseline=baseline,targets=targets))
    result=dict(claim_id='CC11_CHECKED_LATE_SOURCE_COLD_TIMING_DISCRIMINATOR',checks={k:bool(v) for k,v in checks.items()},
        rows=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        scope='Checked fixed-pole leading vacuum widths, early NR parents, standard SM RD/entropy and collisionless chi. Rate multipliers are hypothetical timing requirements, not calculated corrections or a new production mechanism. No global cold-DM exclusion; 1/100kpc are working component diagnostics, not observational transfer-function limits.')
    Path(output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
