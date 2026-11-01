import sys,json,math,resource
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'reviews/radial_ir_cold_2026_11_01/gapless_charge'))
from gaugino_threshold import build_model,ext_basis,threshold,summarize,Z0

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
    def mass_profile(ds):
        model=build_model(Z0/math.sqrt(31*e)*math.exp(ds),e,e,g,vertices=False)
        ext,labels=ext_basis(model);groups,_=summarize(threshold(model,ext),labels)
        return {k:v['signed_mass'] for k,v in groups.items()}
    m0=mass_profile(0);slopes=[]
    for h in [.001,.0005]:
        mm2,mm1,mp1,mp2=[mass_profile(x) for x in [-2*h,-h,h,2*h]]
        slopes.append({k:(mm2[k]-8*mm1[k]+8*mp1[k]-mp2[k])/(12*h*m0[k]) for k in m0})
    inclusive=(sum(math.sqrt(x) for x in rates.values()))**2
    out={'claim_id':'TP04-FOURFERMION-COLD-COLLISIONS','Ymax':Ymax,'C6_bound_GeV_inverse2':C6,
         'sigma_v_bounds_GeV_inverse2':sv,'local_loss_rates_GeV':rates,
         'class_rate_sum_diagnostic_GeV':sum(rates.values()),'interference_safe_local_loss_rate_GeV':inclusive,'interference_safe_loss_over_Ward_decay':inclusive/rateG,'actual_e003_logmass_slopes':slopes,
         'checks':{'fourfermion_threshold_far_below_gap':2*m/M<1e-8,'radial_not_in_contact_gap':cold['benchmark']['mrad_GeV']>100*m,
                   'retained_local_collisions_below_Ward1e_15':inclusive/rateG<1e-15,'actual_all_logmass_slopes_below_one':max(abs(x) for x in slopes[-1].values())<1,'slope_stencil_convergence':max(abs(slopes[0][k]/slopes[1][k]-1) for k in m0)<1e-5},
         'maxrss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'scope':'Named leading heavy-contact and light-exchange NR vacuum envelopes, not full finite-temperature or all-order kinetics.'}
    Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(out['checks'].values())
if __name__=='__main__':main(sys.argv[1])
