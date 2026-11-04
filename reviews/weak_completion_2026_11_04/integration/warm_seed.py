"""Common warm endpoint refinement and conditional propagation of its chi seed."""
import os,sys
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
from pathlib import Path
import math,json,time,resource
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/production'))
from decays import Cosmology,T0

def main(output,coarse_path,fine_path):
    start=time.monotonic();cos=Cosmology();coslow=Cosmology(8193)
    packet=json.loads((ROOT/'reviews/weak_completion_2026_11_04/decay/INTERFACE.json').read_text())
    mass=packet['masses_GeV']['chi'];records=[];checks={}
    for label,path in (('coarse',coarse_path),('fine',fine_path)):
        data=json.loads(Path(path).read_text());checks[label+'_target_completed']=all(data['checks'].values())
        q=np.array(data['case']['q']);Y=np.array(data['state']['Y']).reshape(30,len(q))
        h=data['case']['history'][-1];groups=h['groups'];chi=groups.index('F1_1');weights=Y[chi]/sum(Y[chi])
        fac=.02**3/(2*math.pi**2/45*106.75)
        ychi=sum(Y[chi])*fac
        # The seed is the actual warm endpoint. The rest mass in the following
        # propagation is explicitly held at the retained-pole value.
        aTc=.02*T0*(cos.gs0/106.75)**(1/3)
        ab=aTc/(h['Tc_over_mu']*2e6)
        alpha=q*aTc/mass
        distance=cos.travel(alpha,np.full(len(q),ab))
        low=coslow.travel(alpha,np.full(len(q),ab))
        fs=float(weights@distance)
        checks[label+'_propagation_grid']=abs(float(weights@low)/fs-1)<3e-4
        checks[label+'_warm_yield_normalization']=abs(ychi/h['photino_number_yield']-1)<1e-12
        records.append(dict(label=label,path=str(path),N=data['state']['N'],J=data['state']['J'],
            max_energy_work_error_over_excitation=data['case']['max_energy_error_over_excitation'],
            Y_charged=h['Y_charged'],Y_chi=ychi,Y_vectors=h['vector_number_yield'],
            chi_rest_density_DM_fraction_if_conserved=ychi*mass/.44e-9,
            fixed_pole_mass_GeV=mass,mean_comoving_momentum_q=float(weights@q),
            conditional_fixed_pole_mean_free_streaming_kpc=fs*1000,
            conditional_fixed_pole_v0_rms_km_s=299792.458*float(np.sqrt(weights@(alpha**2/(1+alpha**2)))),
            propagation_grid_relative_difference=abs(float(weights@low)/fs-1),
            chi_present_Pauli_occupation_max=float(np.max(Y[chi]/(2*np.array(data['case']['W'])/(2*math.pi**2)))),
            warm_charged_rest_energy_over_10percent_gate=h['charged_rest_energy_over_10percent_DM_gate']))
    coarse=json.loads(Path(coarse_path).read_text());fine=json.loads(Path(fine_path).read_text())
    yc=np.array(coarse['state']['Y']);yf=np.array(fine['state']['Y']);
    checks['same_q_grid']=bool(np.array_equal(coarse['case']['q'],fine['case']['q']))
    checks['same_N']=abs(coarse['state']['N']-fine['state']['N'])<1e-14
    differences={key:records[1][key]/records[0][key]-1 for key in ('J','Y_charged','Y_chi','Y_vectors','conditional_fixed_pole_mean_free_streaming_kpc')}
    differences['physical_number_L1_relative']=float(sum(abs(yf-yc))/sum(abs(yf)))
    vector_effects=[]
    for record,name in zip(records,('run_fresh_coarse006','run_fresh_fine007')):
        sf=json.loads((ROOT/'reviews/weak_completion_2026_11_04/energy'/name/'result.json').read_text())
        sfy=np.array(sf['state']['Y']).reshape(25,len(q));sfh=sf['case']['history'][-1]
        sfchi=float(sum(sfy[groups.index('F1_1')])*fac)
        vector_effects.append(dict(resolution=record['label'],scalar_fermion_reference=name,J_relative=record['J']/sf['state']['J']-1,Y_charged_relative=record['Y_charged']/sfh['Y_charged']-1,Y_chi_relative=record['Y_chi']/sfchi-1))
    result=dict(claim_id='CC11_COMMON_WARM_REFINEMENT_AND_CONDITIONAL_CHI_SEED',checks={k:bool(v) for k,v in checks.items()},records=records,
        refinement_fine_over_coarse_minus_one=differences,vector_effects_at_matched_step=vector_effects,runtime_seconds=time.monotonic()-start,
        peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        scope='Actual fresh common30 warm states, with retained finite-step errors. Seed free streaming assumes its number/momenta survive and mass stays at the pole value after this checkpoint. No derived future mass/opacity history, no final abundance, no full cold-matter candidate. Charged gate at the warm endpoint is diagnostic, not a final relic bound.')
    Path(output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));assert all(checks.values()),checks

if __name__=='__main__':main(*sys.argv[1:])
