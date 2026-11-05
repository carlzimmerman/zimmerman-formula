"""Rebuild KT39's cross-check table from raw results and validate provenance."""
import hashlib
import json
import math
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
VALIDATOR = Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py')


def read(path):
    return json.loads((HERE/path).read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    records = []
    for p in sorted(HERE.rglob('manifest.json')):
        check = subprocess.run([sys.executable,str(VALIDATOR),str(p),'--root',str(ROOT)],
                               capture_output=True,text=True)
        records.append(dict(path=str(p.relative_to(HERE)),
                            status=json.loads(p.read_text())['run']['status'],
                            valid=check.returncode==0,sha256=sha(p),
                            validation=check.stdout.strip(),error=check.stderr.strip()))
    assert len(records)==16 and all(r['valid'] and r['status']=='completed' for r in records)
    models = {}
    count = 0
    for tag in ['full_125','full_150','full_175','adaptive_1125','adaptive_125_mid']:
        path = 'mw/'+tag+'_001/results.json'
        d = read(path)
        for foot, f in d['footings'].items():
            for s in f['scans']:
                key = (d['power'],s['ell_kpc'])
                model = models.setdefault(key,dict(power=key[0],ell_kpc=key[1],
                           selection='adaptive' if tag.startswith('adaptive') else 'initial',footings={}))
                assert len(s['rows'])==1375
                assert [r['index'] for r in s['rows']]==list(range(1375))
                good = [r for r in s['rows'] if r['corrected']['all_four']]
                assert all(r['corrected']['all_four']==all(r['corrected'][k] for k in ('L1','L2a','L2b','L3')) for r in s['rows'])
                assert len(good)==s['summary']['n_pass']
                assert sum(r['corrected']['Lh'] for r in good)==s['summary']['n_strict']
                count += len(s['rows'])
                model['footings'][foot] = dict(mw_summary=s['summary'],mw_source=path)
    assert len(models)==20 and count==55000
    solar_count = 0
    for path, adaptive in [('cassini/run_001/results.json',False),('cassini/adaptive_001/results.json',True)]:
        d = read(path)
        assert d['all_checks_pass']
        for foot, f in d['footings'].items():
            rows = [(v['power'],v['length_kpc'],v['fine']) for v in f.values()] if adaptive else [
                (float(p),float(ell),v['fine']) for p,pv in f['powers'].items() for ell,v in pv['physical_lengths'].items()]
            for power, ell, q in rows:
                ratio = abs(q['Q2_signed_s_minus_2'])/5.2e-27
                assert math.isclose(ratio,q['x_ceiling'],rel_tol=2e-14)
                assert q['cassini_pass']==(ratio<=1)
                models[power,ell]['footings'][foot]['cassini'] = dict(
                    Q2_signed_s_minus_2=q['Q2_signed_s_minus_2'],ceiling_ratio=ratio,passed=q['cassini_pass'],source=path)
                solar_count += 1
    assert solar_count==40
    dwarf_count = 0
    for path in ['dwarfs/run_001/results.json','dwarfs/continuation_001/results.json']:
        d = read(path)
        assert d['all_checks_pass'] and len(d['sample'])==24 and len(d['upsilon_grid'])==41
        for key, fs in d['summaries'].items():
            power, ell = map(float,key.split('|'))
            for foot, summary in fs.items():
                sets = []
                for grid in ['coarse','fine','expanded']:
                    rows = d['cases'][grid][key][foot]
                    assert len(rows)==24
                    accepted = []
                    plain = []
                    for r in rows:
                        assert len(r['sigma'])==41 and all(math.isfinite(s) for s in r['sigma'])
                        passed = any(abs(s-r['observed_sigma'])<=2*r['observed_error'] for s in r['sigma'])
                        assert passed==r['passed']
                        if passed: accepted.append(r['name'])
                        if any(abs(s-r['observed_sigma'])<=2*r['observed_error'] for s in r['plain_sigma']):plain.append(r['name'])
                    assert accepted==summary['names_passing'] and len(plain)==summary['plain_isolated_pass']==19
                    sets.append(accepted)
                assert sets[0]==sets[1]==sets[2] and len(sets[0])==summary['pass_count']
                models[power,ell]['footings'][foot]['isolated_dwarfs'] = dict(
                    pass_count=summary['pass_count'],plain_pass_count=19,total=24,source=path)
                dwarf_count += 24*41
    assert dwarf_count==39360
    ref = read('mw/refine_001/results.json')
    assert ref['complete'] and len(ref['rows'])==60
    witnesses = {}
    for foot in ['canonical','alt']:
        rows = [r for r in ref['rows'] if r['power']==1.125 and r['ell_kpc']==3 and r['footing']==foot]
        assert len(rows)==6 and all(r['score']['all_four'] and not r['score']['Lh'] for r in rows)
        witnesses[foot] = next(r for r in rows if r['refine']==5)
    other = [r for r in ref['rows'] if r['power']!=1.125]
    assert all(not r['score']['all_four'] for r in other)
    result = dict(model_family='P=xR(x+s**p), s=ell² H:H/a0²; complete action variation',
                  models=[models[k] for k in sorted(models)],mw_population_evaluations=count,
                  solar_model_footing_pairs=solar_count,distinct_dwarf_configurations=dwarf_count,
                  selected_refinement_evaluations=60,witnesses_refinement5=witnesses,
                  conclusion='A refined two-primary-check witness at p=9/8,ell=3kpc, with strict Lh failure and an isolated dwarf deficit. No broadly viable gravity model or continuous-family exclusion established.')
    (HERE/'RESULTS.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    selected = ['README.md','PLAN.md','ADAPTIVE_PLAN.md','RESULTS.json','mw_witnesses.png','mw_witnesses.pdf',
                'mw/REVIEW.md','mw/selection.json','mw/refine_001/results.json','analytic/DERIVATION.md',
                'analytic/SOLAR_DERIVATION_REVIEW.md','dwarfs/README.md','cassini/README.md']
    out = dict(manifest_count=len(records),statuses=dict(Counter(r['status'] for r in records)),
               all_manifest_hash_checks_valid=True,records=records,
               counts=dict(mw_population_evaluations=count,solar_pairs=solar_count,
                           dwarf_configurations=dwarf_count,selected_refinements=60),
               independent_regrades='MW detailed score regrade in mw/REVIEW.md; this verifier regrades dwarf dispersion flags at three grids and Solar ceiling ratios from raw Q2.',
               visual_review='mw_witnesses.png inspected; sorted vertical radii, no clipped labels.',
               qualification='Completed and hash-valid is separate from scientific acceptance. p and ell are searched phenomenological parameters; satellite EFE, equilibrium and dynamical health remain unestablished.',
               sha256={name:sha(HERE/name) for name in selected})
    (HERE/'VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['manifest_count','statuses','all_manifest_hash_checks_valid','counts']}))


if __name__=='__main__':
    main()
