import sys,json,math,resource
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
def main(path):
    p=Path(__file__).parent
    hard=json.loads((ROOT/'reviews/radial_ir_cold_2026_11_01/gapless_charge/decay_bound/run_001/result.json').read_text())
    soft=json.loads((p/'run_soft/result.json').read_text());cross=json.loads((p/'run_crossed/result.json').read_text())
    cold=json.loads((p/'run_002/result.json').read_text())['photino']
    inp=soft['inputs'];e=inp['e'];g=inp['g1_leading'];m=inp['mchi_GeV'];F=inp['F_GeV2'];a=inp['a_GeV']
    M=hard['benchmark']['Mcharged_GeV'];n=soft['phase_pair_annihilation']['local_number_density_GeV3']
    Ymax=32*math.sqrt(24*e*e+30*g*g);C6=32768*Ymax**4/(16*math.pi**2*M*M)
    kap=cold['kappa_dlnm_ds'][-1]
    sv={'heavy_4fermion_inclusive':338*C6*C6*m*m/math.pi,
        'phase_light_gaugino_pairs_inclusive':100*m*m/(math.pi*a**4),
        'separate_radial_Goldstino_pair':100*kap*kap*m**4/(math.pi*a*a*F*F),
        'two_Ward_vertices_inclusive':512*m**6/(math.pi*F**4),
        'crossed_heavy_2vector':cross['sigma_v_bound_GeV_inverse2']}
    rates={k:n*v for k,v in sv.items()};rateG=hard['benchmark']['Gamma_Goldstino_partial_GeV']
    out={'claim_id':'TP04-FOURFERMION-COLD-COLLISIONS','Ymax':Ymax,'C6_bound_GeV_inverse2':C6,
         'sigma_v_bounds_GeV_inverse2':sv,'local_loss_rates_GeV':rates,
         'summed_local_loss_rate_GeV':sum(rates.values()),'summed_loss_over_Ward_decay':sum(rates.values())/rateG,
         'checks':{'fourfermion_threshold_far_below_gap':2*m/M<1e-8,'radial_not_in_contact_gap':cold['benchmark']['mrad_GeV']>100*m,
                   'retained_local_collisions_below_Ward1e_15':sum(rates.values())/rateG<1e-15},
         'maxrss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'scope':'Named leading heavy-contact and light-exchange NR vacuum envelopes, not full finite-temperature or all-order kinetics.'}
    Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(out['checks'].values())
if __name__=='__main__':main(sys.argv[1])
