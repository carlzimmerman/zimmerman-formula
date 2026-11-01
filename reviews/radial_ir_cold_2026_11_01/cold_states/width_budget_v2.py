"""Ward partial widths and explicitly conditional higher-body budget."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import math,json,resource
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/radial_ir_cold_2026_11_01/gapless_charge'))
from gaugino_threshold import build_model,ext_basis,threshold,summarize

def main(path):
    radial=json.loads((ROOT/'reviews/radial_ir_cold_2026_11_01/radial/run_dynamics/result.json').read_text())
    cold=json.loads((Path(__file__).parent/'run_002/result.json').read_text())
    rows=[]
    for r in radial['cases']:
        e=r['e'];v=r['vacuum'][-1];X=r['X_min'];g=math.sqrt(29/200)*e
        def masses(s):
            d=build_model(X*math.exp(s),e,e,g,vertices=False)
            ext,C=ext_basis(d);groups,_=summarize(threshold(d,ext),C)
            return {k:z['signed_mass'] for k,z in groups.items()}
        m0=masses(0);der=[]
        for h in [.001,.0005]:
            mm2,mm1,mp1,mp2=[masses(s) for s in [-2*h,-h,h,2*h]]
            der.append({k:(mm2[k]-8*mm1[k]+8*mp1[k]-mp2[k])/(12*h) for k in m0})
        M=v['m'];Ftot=1/math.sqrt(31)
        channels={}
        for k,count in [('SU3',8),('SU2',3),('U1',1)]:
            y=der[-1][k]/math.sqrt(2*v['A']);beta=math.sqrt(1-4*m0[k]**2/M**2)
            channels[k]={'mhat':m0[k],'dlnm_ds':der[-1][k]/m0[k],
                         'y_radial':y,'Gammahat_pair':count*y*y*M/(16*math.pi)*beta**3}
        rows.append({'e':e,'mrad_hat':M,'Gammahat_phase':v['Gamma_phase'],
                     'Gammahat_Goldstino_pair':M**5/(32*math.pi*Ftot**2),
                     'gaugino_pairs':channels,
                     'slope_stencil_error':max(abs(der[0][k]/der[1][k]-1) for k in der[0]),
                     'scope':'leading Ward/local threshold-derivative partial widths; no new finite momentum triangle'})
    p=cold['photino'];b=p['benchmark'];mu=b['mu_GeV'];m=b['m_GeV'];e=p['e']
    coeff=cold['cases'][0]['charged_heavy_gap']/math.sqrt(.01)
    Mc=mu*coeff*math.sqrt(e);hbar=6.582119569e-25;age=4.355e17
    gamma_unit=m**7/(256*math.pi**3*Mc**6)
    gammaG=hbar/b['tau_Goldstino_photon_partial_s']
    # This is an explicitly normalized conditional coefficient, not a computed Wilson bound.
    budget={'charged_mass_GeV':Mc,'m_over_Mcharged':m/Mc,
       'definition':'Gamma3 = c7_effective_squared * m^7/(256*pi^3*Mcharged^6); inclusive colors/form factors are absorbed into c7_effective_squared',
       'Gamma3_GeV_if_c7eq1':gamma_unit,'Gamma3_over_Goldstino_if_c7eq1':gamma_unit/gammaG,
       'abs_c7_for_equal_Goldstino_width':math.sqrt(gammaG/gamma_unit),
       'abs_c7_for_total_lifetime_one_age':math.sqrt((hbar/age-gammaG)/gamma_unit),
       'status':'Conditional sufficient budget ONLY. No finite-F box integral or rigorous upper bound on c7 has been supplied.'}
    checks={'radial_pair_phase_space_open':all(all(z['mhat']*2<r['mrad_hat'] for z in r['gaugino_pairs'].values()) for r in rows),
            'radial_slope_stencils':max(r['slope_stencil_error'] for r in rows)<1e-5,
            'phase_channel_dominates_computed_other_partial_widths':all(r['Gammahat_Goldstino_pair']+sum(z['Gammahat_pair'] for z in r['gaugino_pairs'].values())<.01*r['Gammahat_phase'] for r in rows),
            'conditional_dim7_budget_positive':budget['abs_c7_for_total_lifetime_one_age']>0}
    out={'claim_id':'TP04-WIDTH-BUDGET','checks':checks,'radial_partial_widths':rows,'photino_dim7_conditional_budget':budget,
         'maxrss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'not_total_width':True}
    Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
