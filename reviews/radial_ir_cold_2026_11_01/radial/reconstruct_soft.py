import sys
sys.dont_write_bytecode=True
import math,json,resource
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent;TP4=HERE.parent
def main(path):
    old=json.load(open(TP4/'cold_states/run_002/result.json'));soft=json.load(open(TP4/'cold_states/run_soft/result.json'));hard=json.load(open(HERE/'run_bound_review/result.json'))
    p=old['photino'];b=p['benchmark'];e=p['e'];m=b['m_GeV'];mu=b['mu_GeV'];v=mu*7.367143721278508/math.sqrt(e);a=math.sqrt(2)*v;F=mu*mu/math.sqrt(31);g2=29/200*e*e
    direct=m*m/(math.pi**2*a*a);ga=5*g2/(8*math.pi**2*a);integral=1-Fraction(3,4)+Fraction(1,8);anom=ga*ga*m*m/(96*math.pi**2)*float(integral);comb=(math.sqrt(direct)+math.sqrt(anom))**2
    masses=old['cases'][0]['gaugino_masses'];ratios={k:masses[k]['signed_mass']/masses['U1']['signed_mass'] for k in ('SU3','SU2')};light=sum(4*d/(math.pi**2*ratios[k]**2)*(m*m/F)**2 for k,d in [('SU3',8),('SU2',3)])
    mr=b['mrad_GeV'];ks=abs(p['kappa_dlnm_ds'][-1]);C=6+8*ks*m*m/(mr*mr-4*m*m);svphase=C*C*m*m/(64*math.pi*a**4)
    n=.3*(1.973269804e-14)**3/m;G2=6.582119569e-25/b['tau_Goldstino_photon_partial_s'];c=hard['c7'];M=hard['Mcharged_GeV']
    svhard=c*c*m**4/(16*math.pi*M**6);svroot=16*c*c*m**4/(math.pi*M**6);svward=512*m**6/(math.pi*F**4)
    checks=dict(direct=abs(direct/soft['phase_radiation']['direct_bound_ratio']-1)<1e-10,anomaly=abs(anom/soft['phase_radiation']['anomaly_alone_exact_leading_ratio']-1)<1e-10,spectral_integral=integral==Fraction(3,8),light=abs(light/soft['light_Goldstino_exchange']['summed_bound_ratio']-1)<1e-10,phase_collision=abs(svphase/soft['phase_pair_annihilation']['sigma_v_threshold_bound_GeV_inverse2']-1)<1e-10,coordinator_cushion=abs(svroot/svhard-256)<1e-10,all_named_collisions_negligible=n*(svroot+svphase+svward)/G2<1e-20)
    out=dict(claim_id='TP04_SOFT_CROSS_REVIEW',checks=checks,direct_phase_ratio=direct,anomaly_ratio=anom,combined_phase_ratio=comb,spectral_integral=str(integral),light_exchange_ratio=light,NR_collisions=dict(n_GeV3=n,phase_sigma_v=svphase,hard_sigma_v_direct_majorant=svhard,hard_sigma_v_coordinator_cushion=svroot,Ward_pairs_sigma_v_inclusive_upper=svward,hard_loss_over_Goldstino=n*svroot/G2,phase_loss_over_Goldstino=n*svphase/G2,Ward_loss_over_Goldstino=n*svward/G2),peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Named leading local current/anomaly/Ward channels and NR crossedhard bound, not allorders or thermal history')
    Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
