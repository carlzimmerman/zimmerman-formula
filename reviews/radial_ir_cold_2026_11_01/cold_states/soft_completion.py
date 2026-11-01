"""Scalar evaluation of the analytic leading soft-completion bounds."""
import sys,json,math,resource
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]

def main(path):
    d=json.loads((Path(__file__).parent/'run_002/result.json').read_text())
    p=d['photino'];b=p['benchmark'];m=b['m_GeV'];mu=b['mu_GeV'];e=p['e']
    v=mu*7.367143721278508/math.sqrt(e);a=math.sqrt(2)*v;F=mu*mu/math.sqrt(31)
    g=math.sqrt(29/200)*e;ga=5*g*g/(8*math.pi**2*a)
    direct=m*m/(math.pi**2*a*a)
    anomaly=ga*ga*m*m/(256*math.pi**2)
    combined=(math.sqrt(direct)+math.sqrt(anomaly))**2
    masses=d['cases'][0]['gaugino_masses'];mY=masses['U1']['signed_mass']
    channels={};total=0.
    for name,mult in [('SU3',8),('SU2',3)]:
        r=masses[name]['signed_mass']/mY
        val=4*mult/(math.pi**2*r*r)*(m*m/F)**2
        channels[name]={'mass_ratio':r,'Gamma_bound_over_Ward_two_body':val};total+=val
    # Tree nonrelativistic annihilation norm bound from phase mass law.
    mr=b['mrad_GeV'];kappa=p['kappa_dlnm_ds'][-1]
    C=6+8*abs(kappa)*m*m/(mr*mr-4*m*m)
    sv=C*C*m*m/(64*math.pi*a**4)
    hc=1.973269804e-14;n=.3*hc**3/m
    widthG=6.582119569e-25/b['tau_Goldstino_photon_partial_s']
    out={'claim_id':'TP04-SOFT-COMPLETION','inputs':{'e':e,'mchi_GeV':m,'mu_GeV':mu,'v_GeV':v,'a_GeV':a,'F_GeV2':F,'g1_leading':g},
      'phase_radiation':{'direct_bound_ratio':direct,'anomaly_alone_exact_leading_ratio':anomaly,'combined_bound_ratio':combined,'ga_pi_FtildeF_GeV_inverse':ga},
      'light_Goldstino_exchange':{'channels':channels,'summed_bound_ratio':total},
      'phase_pair_annihilation':{'sigma_v_threshold_bound_GeV_inverse2':sv,'local_number_density_GeV3':n,'loss_rate_bound_GeV':n*sv,'loss_rate_over_Ward_width':n*sv/widthG,'scope':'leading NR vacuum tree EFT; no finite-temperature average'},
      'checks':{'phase_radiation_below_1e_24':combined<1e-24,'light_exchange_below_1e_36':total<1e-36,'annihilation_below_1e_30_of_Ward_rate':n*sv/widthG<1e-30,'radial_not_on_shell':mr>10*m},
      'maxrss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
      'scope':'Leading local Ward/R-current/anomaly EFT and derived norm bounds; not an all-order inclusive rate.'}
    Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(out['checks'].values())
if __name__=='__main__':main(sys.argv[1])
