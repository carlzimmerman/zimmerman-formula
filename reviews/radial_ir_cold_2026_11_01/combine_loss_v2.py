"""Compose independently checked leading bounds; preserve all scope limits."""
import sys
sys.dont_write_bytecode=True
import json,argparse,resource
from pathlib import Path
import mpmath as mp
BASE=Path(__file__).resolve().parent


def main(out):
    mp.mp.dps=70
    hard=json.loads((BASE/'gapless_charge/decay_bound/run_001/result.json').read_text())
    soft=json.loads((BASE/'cold_states/run_soft/result.json').read_text())
    four=json.loads((BASE/'cold_states/run_four_fermion_v2/result.json').read_text())
    assert all(four['checks'].values())
    units=json.loads((BASE/'run_units/result.json').read_text())
    thermal=json.loads((BASE/'run_thermal/result.json').read_text())
    assert all(hard['checks'].values()) and all(soft['checks'].values()) and units['all_checks_pass'] and thermal['all_checks_pass']
    q=lambda x:mp.mpf(str(x))
    b=hard['benchmark'];m=q(b['m_GeV']);M=q(b['Mcharged_GeV']);c7=q(hard['majorant']['inclusive_c7_effective_upper'])
    G=q(b['Gamma_Goldstino_partial_GeV']);H=q(b['Gamma_hard_upper_GeV'])
    phase_soft=G*q(soft['phase_radiation']['combined_bound_ratio'])
    light_soft=G*q(soft['light_Goldstino_exchange']['summed_bound_ratio'])
    radiative=phase_soft+light_soft
    Gamma3=(mp.sqrt(H)+mp.sqrt(phase_soft)+mp.sqrt(light_soft))**2
    phase_ann=q(soft['phase_pair_annihilation']['loss_rate_bound_GeV'])
    hbar=q(units['constants']['hbar_GeV_s']);age=q(units['constants']['required_lifetime_s'])
    rho=q('.3')*q(units['constants']['hbarc_GeV_cm'])**3;n=rho/m
    sigma_hard=16*c7*c7*m**4/(mp.pi*M**6);ann_hard=n*sigma_hard
    # A numerical padding is conservative for rounding of the quoted constants;
    # it does not represent an estimate of missing physical perturbative terms.
    ann_classes={k:q(v) for k,v in four['local_loss_rates_GeV'].items()}
    ann_classes['crossed_heavy_2vector']=max(ann_classes['crossed_heavy_2vector'],ann_hard)
    ann_classes['phase_light_gaugino_pairs_inclusive']=max(ann_classes['phase_light_gaugino_pairs_inclusive'],phase_ann)
    Gamma_ann=sum(mp.sqrt(v) for v in ann_classes.values())**2
    retained=(G+Gamma3+Gamma_ann)*(1+q('1e-8'))
    tau=hbar/retained;survival=mp.exp(-age/tau)
    state=next(x for x in thermal['cases'] if x['e']==.003 and x['m_GeV']==.001)
    checks={'same_mass_and_coupling_inputs':abs(q(soft['inputs']['mchi_GeV'])/m-1)<q('1e-12') and abs(soft['inputs']['e']-.003)<1e-12,
            'all_retained_leading_loss_survival_above_99percent':survival>q('.99'),
            'hard_annihilation_negligible':ann_hard/G<q('1e-20'),
            'cold_relic_sub_kpc':state['relic_dynamics']['free_streaming_Mpc']<.001,
            'cold_relic_v_eq_below_1e_6':state['relic_dynamics']['vrms_equality']<1e-6}
    result=dict(claim_id='TP04_COMBINED_LEADING_LOSS_V2',checks=checks,all_checks_pass=all(checks.values()),
                benchmark=dict(e=.003,m_chi_GeV=float(m),mu_GeV=b['mu_GeV'],halo_density_GeV_per_cm3=.3),
                bounds={k:str(v) for k,v in dict(Gamma_Ward_GeV=G,Gamma_hard_upper_GeV=H,Gamma_soft_upper_GeV=radiative,phase_annihilation_loss_GeV=phase_ann,hard_annihilation_sigma_v_GeV_minus2=sigma_hard,hard_annihilation_loss_GeV=ann_hard,interference_safe_Gamma3_upper_GeV=Gamma3,interference_safe_all_local_collisions_GeV=Gamma_ann,leading_loss_upper_GeV=retained,lifetime_lower_s=tau,survival_lower_over_13p8Gyr=survival).items()},
                cold_distribution=state,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                scope='Specified leading rigid-model vacuum/NR loss set with independent hard/soft/four-fermion proofs and amplitude-safe composition, not an all-orders total lifetime or a selected cosmological model.',
                non_claims=['No unprovided production, vacuum-energy, gravity or photon-identification solution','No all-loop/all-body or finite-temperature transport bound','One-loop pole mass and retained Ward/current/hard amplitudes only'])
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(checks=checks,bounds=result['bounds']),indent=2));assert result['all_checks_pass'],checks

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);main(p.parse_args().out)
