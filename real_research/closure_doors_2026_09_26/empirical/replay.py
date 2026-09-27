#!/usr/bin/env python3
"""Small exact-model KiDS replay and independent gate-interval arithmetic.

Reuses declared L352 model/data; no claim to independently validate that model
or recompute the shear mock/forest. Snapshots an earlier DE2 run with a failed
corner check; source revisions were concurrent during this campaign.
"""
import argparse,contextlib,io,json,math
from pathlib import Path

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    here=Path(__file__).resolve().parent;root=here.parents[2]
    j=json.loads((here/'DE2_snapshot.json').read_text())
    source=root/'real_research/g03_audit_2026/L352_switch_gauss_compensation.py'
    prefix=source.read_text().split('real_mode = ')[0]
    assert prefix.count('def fit_model(')==1
    ns={'__name__':'l352_replay','__file__':str(source)}
    with contextlib.redirect_stdout(io.StringIO()):exec(compile(prefix,str(source),'exec'),ns)
    eK=1+.3138*((1.25)**3-1);eF=1+.3138*((3.5)**3-1)
    # E²(0.5) read in the original DE2 log: rounded value, bounded ±5e-7 below.
    eS=1.745209
    cells={'interior_p1_x2p5':(1.,2.5),'stored_failing_corner':(.5,3.395)}
    checks={};rows={}
    for name,(p,x0) in cells.items():
        xe=x0*eK**p;dd={}
        for foot,a0 in ns['A0'].items():
            baseline=ns['fit_model'](a0,0.,'none',True)[0]
            dd[foot]=ns['fit_model'](a0,round(xe,4),'compensated',True)[0]-baseline
        rows[name]={'p':p,'x0':x0,'xeff_KiDS':xe,'dchi2':dd}
    checks['interior_cell_KiDS_replay']={'passed':all(x<4 for x in rows['interior_p1_x2p5']['dchi2'].values()),'measured':rows['interior_p1_x2p5']}
    checks['failed_corner_reproduced']={'passed':rows['stored_failing_corner']['dchi2']['alt']>4.5,'measured':rows['stored_failing_corner']}
    XF=min(v for k,v in j['numbers']['XF'].items() if float(k.split('/')[1])<=11)
    upperK=j['numbers']['KiDS']['X_K'] # conservative last sampled passing threshold, not entire continuum proof
    intervals={}
    for vk in [600,650]:
        XS=max(v for k,v in j['numbers']['XS'].items() if k.startswith(str(vk)+'/'))
        lower=max(1.5,XS/(eS-5e-7));upper=min(upperK/eK,XF/eF)
        intervals[str(vk)]={'p':1,'x0_lower':lower,'x0_upper':upper,
                            'shear_floor':XS,'flagship_cap':XF}
        checks[f'interior_arithmetic_vk_{vk}']={'passed':lower<2.5<upper,
                                              'measured':intervals[str(vk)]}
    # Recompute the exact logical problem for two supplied epoch factors.
    assert j['numbers']['forest_ungated']['X_forest_const']>upperK
    checks['constant_gate_pincer_from_supplied_thresholds']={'passed':True,
          'forest_floor':j['numbers']['forest_ungated']['X_forest_const'],'KiDS_sampled_cap':upperK}
    for k,v in checks.items():assert v['passed'],(k,v)
    result={'result':'interior gate witness retained; a stored boundary failure independently reproduced',
            'checks':checks,'scope':'two scalar cells, original L352 model, same input data; p=1 interval conditional on supplied floors/caps',
            'non_claims':['No new gate action validated','No fresh shear/forest/growth simulation',
                          'No proof KiDS pass set is an interval between all sampled points',
                          'No new observational bound; replays existing phenomenological model',
                          'eS only known here within rounding interval ±5e-7, propagated conservatively']}
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
