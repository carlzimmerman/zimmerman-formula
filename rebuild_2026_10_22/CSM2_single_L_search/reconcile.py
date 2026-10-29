import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];REB=HERE.parent
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
paths=[HERE/'run_001/results.json',HERE/'run_001/manifest.json',HERE/'TARGET.md',Path(__file__),REB/'NATIVE_PARTIAL_2026-10-28/measurement_002_three/results.json',REB/'CSM1_consistent_core_switch/feasibility/lg_001/results.json',REB/'CSM1_consistent_core_switch/feasibility/ufd_001/results.json']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hashes={str(p.relative_to(ROOT)):sha(p) for p in paths}
d=json.loads(paths[0].read_text());manifest=json.loads(paths[1].read_text());checks=dict(final_manifest=manifest['run']['status']=='completed',source_checks=all(d['checks'].values()),coverage=len(d['levels'])==15)
rows=[];max_scale_error=0.;flag_checks=0
for lev,cell in d['levels'].items():
    ratio=(float(lev)/3.75)**1.25
    for typ,raw in [('groups',cell['group_raw'])]+([('lens',cell['lens_raw'])] if 'lens_raw' in cell else []):
        ref=d['baseline']['groups' if typ=='groups' else 'lens']
        checks[f'{lev}|{typ}|column_coverage']=len(raw['core_columns'])==len(ref['core_columns'])
        good=True
        for a,b in zip(raw['core_columns'],ref['core_columns']):
            good &= all(a[k]==b[k] for k in ('footing','tag','mass','floor'))
            predicted=b['column']*ratio
            err=abs(a['column']-predicted)/max(abs(predicted),1e-300);max_scale_error=max(max_scale_error,err)
            good &= err<1e-11 and a['expected']==(a['column']>a['floor'])
            if 'core' in a:good &= math.isclose(a['core'],max(a['column'],a['floor']),rel_tol=1e-12)
        checks[f'{lev}|{typ}|independent_L_scaling']=bool(good)
        checks[f'{lev}|{typ}|actual_flags']=all(z['expected']==z['actual'] for z in raw['flags']);flag_checks+=len(raw['flags'])
    for foot in ('canonical','alt'):
        g=cell['groups'][foot];calc_tot=math.hypot(g['se'],g['sys']);gp=calc_tot<=.045 and abs(g['mean']/calc_tot)<2
        checks[f'{lev}|{foot}|group_grade']=math.isclose(calc_tot,g['tot'],rel_tol=1e-12) and math.isclose(g['Z'],g['mean']/calc_tot,rel_tol=1e-12) and gp==g['PASS'] and g['N']==63
        delta=None
        if 'lens_raw' in cell:
            raw=cell['lens_raw']['result'][foot]['all'];delta=raw['H2H']['chi2']-raw['L2H']['chi2']
            checks[f'{lev}|{foot}|lens_grade']=math.isclose(delta,cell['lens_delta_law'][foot],rel_tol=1e-12,abs_tol=1e-12)
        rows.append(dict(L=float(lev),footing=foot,group_Z=g['Z'],group_pass=gp,lens_delta_law=delta,
                         canonical_necessary_survivor=(gp and delta is not None and delta<=9) if foot=='canonical' else None))
    recomputed=cell['groups']['canonical']['PASS'] and cell.get('lens_delta_law',{}).get('canonical',float('inf'))<=9
    checks[f'{lev}|candidate']=recomputed==cell['canonical_survives_necessary_tests']
checks['no_finite_survivors']=not any(r['canonical_necessary_survivor'] for r in rows if r['footing']=='canonical')
native=json.loads(paths[4].read_text());lg=json.loads(paths[5].read_text());ufd=json.loads(paths[6].read_text());deductions={}
for s in ('3','7'):
    L=native['runs'][s]['L_proxy'];critical=lg['thresholds']['canonical']['dwarfs']['A_c2b_refit']['Lcrit'];law=ufd['states']['canonical']['states']['law']
    deductions[s]=dict(L_proxy=L,canonical_UFD_threshold=critical,LG_halo_active=L>critical,UFD_law_Z=law['Z'],fixed_UFD_criterion_pass=law['pass_'])
    checks[f'native_seed{s}|necessary_exclusion']=L<critical and not law['pass_'] and abs(law['Z'])>2
checks['inputs_stable']=all(sha(ROOT/p)==h for p,h in hashes.items())
result=dict(checks=checks,rows=rows,native_proxy_deductions=deductions,max_column_scaling_relative_error=max_scale_error,actual_flag_checks=flag_checks,
    scope='15 finite canonical single-L exclusions, plus two native proxy necessary exclusions; not a continuous-L theorem',input_sha256=hashes)
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
with (out/'scores.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps(dict(checks=len(checks),failed=[k for k,v in checks.items() if not v],max_column_scaling_relative_error=max_scale_error,actual_flag_checks=flag_checks),indent=2));raise SystemExit(0 if all(checks.values()) else 1)
