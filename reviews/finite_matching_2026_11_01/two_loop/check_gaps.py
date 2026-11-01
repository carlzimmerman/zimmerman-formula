import json,sys,math,resource
from pathlib import Path
import numpy as np
from model import build_model

def main(path,pressure_path):
    d=json.loads(Path(pressure_path).read_text());rows=[]
    for r in d['cases']:
        if r['scheme']!='finite_matched' or r['interpolation_nodes']!=29 or r['stencil_h']!=.0025:continue
        e=r['e']
        for label,ratio,p in [('endpoint',r['boundary_ratio'],r['boundary']),('1p3',1.3,next(s for s in r['samples'] if s['X_over_min']==1.3))]:
            X=r['X_min']*ratio;q=p['omega2'];m=build_model(X,e,e,math.sqrt(29/200)*e,1.,vertices=False)
            record={'e':e,'location':label,'X':X,'X_over_min':ratio,'omega2':q,
                    'phase_cs2_IR':p['cs2_IR'],'phase_fixed_charge_D':p['fixed_charge_D'],
                    'zero_counts':{},'min_positive_m2':{},'omega2_over_gap':{}}
            for key,vals in [('scalar',m['mS2']),('Weyl',m['mF2']),('vector',m['mV2'])]:
                positive=vals[vals>0];gap=float(np.min(positive))
                record['zero_counts'][key]=int(np.sum(vals==0))
                record['min_positive_m2'][key]=gap;record['omega2_over_gap'][key]=q/gap
            rows.append(record)
    checks={'four_spectral_points':len(rows)==4,
            'explicit_zero_mode_counts':all(r['zero_counts']=={'scalar':14,'Weyl':13,'vector':12} for r in rows),
            'positive_gaps_and_omega':all(r['omega2']>0 and all(v>0 for v in r['min_positive_m2'].values()) for r in rows),
            'all_massive_gap_ratios_below_1e-6':max(v for r in rows for v in r['omega2_over_gap'].values())<1e-6}
    out={'claim_id':'FM_ACTUAL_GAPS','checks':checks,'cases':rows,'peak_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'IR_mode_bookkeeping':{'scalar_zeros':'12 gauge Goldstones plus2 real flat-direction coordinates retained at tree order',
                               'Weyl_zeros':'12 unbroken gauginos plusGoldstino',
                               'vector_zeros':'12 unbroken gauge generators'},
         'non_claims':['Positive gaps are tree masses, not correctedpole masses','Massless/retained phase-radial sector is not integrated out',
                       'No bound on all nonlocalIR physics or finite higherderivative terms','The1.3phase sound instability remains']}
    Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1],sys.argv[2])
