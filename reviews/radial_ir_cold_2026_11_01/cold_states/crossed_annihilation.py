import sys,json,math,resource
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
def main(path):
    b=json.loads((ROOT/'reviews/radial_ir_cold_2026_11_01/gapless_charge/decay_bound/run_001/result.json').read_text())
    s=json.loads((Path(__file__).parent/'run_soft/result.json').read_text())
    c=b['majorant']['inclusive_c7_effective_upper'];m=b['benchmark']['m_GeV'];M=b['benchmark']['Mcharged_GeV']
    n=s['phase_pair_annihilation']['local_number_density_GeV3'];rateG=b['benchmark']['Gamma_Goldstino_partial_GeV']
    sv=c*c*m**4/(math.pi*M**6);rate=n*sv
    out={'claim_id':'TP04-CROSSED-HARD-COLLISIONS','sigma_v_bound_GeV_inverse2':sv,'local_rate_bound_GeV':rate,
         'rate_over_Ward_decay':rate/rateG,'hard_plus_phase_rate_GeV':rate+s['phase_pair_annihilation']['loss_rate_bound_GeV'],
         'checks':{'crossed_bundle_below_Ward1e_24':rate/rateG<1e-24,'incoming_threshold_far_below_heavy':2*m/M<1e-8},
         'maxrss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'scope':'Crossed independently bounded leading one-loop hard2fermion2vector class at NR threshold, no finite-temperature rate'}
    Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(out['checks'].values())
if __name__=='__main__':main(sys.argv[1])
