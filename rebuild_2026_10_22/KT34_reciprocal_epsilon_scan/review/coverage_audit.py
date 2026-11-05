#!/usr/bin/env python3
"""Independent count and score audit of finished cell-by-width enumerations."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'rebuild_2026_10_22/KT34_reciprocal_epsilon_scan'
SOURCE=ROOT/'rebuild_2026_10_22/KT33_reciprocal_filter/mw/grid_refined_run/results.json'
A0={'canonical':9.3603e-11,'alt':1.1312e-10}
G=4.30091e-6
GAS=11910967635.394314
K_CEILING=67.45934792232582
O_CEILING=59.89250004508689


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    baseline=json.loads(SOURCE.read_text());out={'assertion_tested':'Independently rebuild every cell width range using closed-form integer bounds, compare coverage counts and score labels in the completed exact scans. This is not a new gravity solve or a continuum error certificate.','runs':{},'checks':{}}
    for name in ('exact_run','transition_run'):
        path=BASE/'mw'/name/'results.json'
        record=json.loads(path.read_text());man=json.loads((path.parent/'manifest.json').read_text())
        assert man['run']['status']=='completed'
        checked=out['runs'][name]={}
        for foot,f in record['footings'].items():
            rows=baseline['footings'][foot]['rows'];lo,hi=f['epsilon_closed_band'];expected=Counter();n_per=[];k_ranges=[]
            assert record['cells']==[r['cell'] for r in rows]
            for r in rows:
                rm=math.sqrt(G*(r['Mstar']+GAS)/(A0[foot]*3.0857e19/1e6))
                # Bin intersection is equivalent to these direct integer bounds.
                first=math.ceil(math.log(lo*rm)/.005-.5)
                last=math.floor(math.log(hi*rm)/.005+.5)
                n_per.append(last-first+1);k_ranges.append((first,last))
                expected.update(range(first,last+1))
            actual={r['k']:r['n_cells'] for r in f['width_summaries']}
            checks={
                'population_exact':len(rows)==f['n_cells']==1375,
                'per_cell_bin_counts_exact':n_per==f['cell_width_state_counts'],
                'per_width_population_exact':dict(expected)==actual,
                'all_states_accounted':sum(n_per)==f['n_width_states']==sum(actual.values()),
                'distinct_widths_exact':len(expected)==f['n_distinct_widths'],
                'negative_mass_bound_passes':f['max_negative_mass_bound']<=1e-5,
                'mass_error_bound_passes':f['max_mass_relative_error_bound']<1e-10,
            }
            report={'n_cells':len(rows),'n_cell_width_states':sum(n_per),'n_distinct_widths':len(expected),'epsilon_band':[lo,hi],'checks':checks}
            if name=='exact_run':
                checks['no_recorded_L1_pass']=f['n_L1_pass_states']==0 and all(not r['L1_passes'] for r in f['width_summaries'])
                checks['all_cell_maxima_below_L1']=len(f['cell_max_vc'])==1375 and max(f['cell_max_vc'])<219.9
                checks['dual_reproduction']=max(c['error'] for c in f['dual_checks'])<1e-7
                report['maximum_local_speed']=max(f['cell_max_vc'])
            else:
                scores=f['full_cut_scores'];pairs=[(r['index'],r['k']) for r in scores]
                checks['all_prefilter_survivors_scored']=len(scores)==f['n_full_cut_evaluations']==sum(r['n_L1_pass'] for r in f['width_summaries'])
                checks['unique_scored_pairs']=len(set(pairs))==len(pairs)
                checks['scored_pairs_in_domain']=all(k_ranges[i][0]<=k<=k_ranges[i][1] for i,k in pairs)
                expected_pass=[]
                for row in scores:
                    q=row['scores'];passes=(219.9<=q['vc']<=238.3 and q['cK']<=K_CEILING and abs(q['K0']-66.4)<=4.4 and q['cO']<=O_CEILING)
                    assert passes==q['all_four']
                    if passes:expected_pass.append((row['index'],row['k']))
                checks['passing_pairs_exact']=set(expected_pass)=={(r['index'],r['k']) for r in f['passes']}
                checks['passing_count_exact']=len(expected_pass)==sum(r['n_pass'] for r in f['width_summaries'])==len(f['passes'])
                checks['dual_reproduction']=f['dual_full_vc_error_max']<1e-7
                report.update(n_full_cut_scores=len(scores),n_pass_states=len(expected_pass),pass_interval_union_closed_cover=f.get('pass_interval_union_closed_cover',[]),epsilon_pass_supremum=f.get('epsilon_pass_supremum'))
            checked[foot]=report
            out['checks'][name+'|'+foot]=all(checks.values())
    out['all_checks_pass']=all(out['checks'].values())
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps(out,indent=2))
    if not out['all_checks_pass']:raise SystemExit(1)


if __name__=='__main__':main()
