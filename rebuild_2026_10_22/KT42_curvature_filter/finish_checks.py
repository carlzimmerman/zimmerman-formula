"""Final provenance validation plus independent supplementary-screen grading."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
VALIDATOR='/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py'
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--planet-run',required=True)
args=ap.parse_args()
out=dict(manifests=[],planet_rows=[],complete=False)
for p in sorted(HERE.glob('**/manifest.json')):
    if p.parent==args.output.parent:continue
    a=json.loads(p.read_text())
    v=subprocess.run([sys.executable,VALIDATOR,str(p),'--root',str(ROOT)],capture_output=True,text=True)
    assert v.returncode==0,(str(p),v.stdout,v.stderr)
    out['manifests'].append(dict(path=str(p.relative_to(ROOT)),status=a['run']['status'],valid=True))
q=json.loads((HERE/'planets'/args.planet_run/'results.json').read_text())
tab=json.loads((ROOT/'rebuild_2026_10_22/RQ3_acceptance_v2/tolerances.json').read_text())['PLANETS']
assert q['all_checks_pass']
for foot,f in q['footings'].items():
    assert len(f['rows'])==8
    for r in f['rows']:
        t=tab[r['planet']]
        sigma=t['dg_tight']*max(t['EPM'],t['INPOP'])/min(t['EPM'],t['INPOP'])
        total=(r['A_over_a0']+r['B_over_a0'])*f['a0']
        zg=abs(total)/sigma;zp=abs(r['rate_mas_year'])/max(t['EPM'],t['INPOP'])
        assert abs(zg-r['Z_radial'])<1e-9 and abs(zp-r['Z_rate'])<1e-9
        assert abs(total-r['total_m_s2'])<1e-22
        out['planet_rows'].append(dict(footing=foot,planet=r['planet'],width_kpc=r['width_kpc'],
            total_over_a0=total/f['a0'],radial_error_ratio=zg,precession_error_ratio=zp,
            radial_pass=zg<=2,monopole_precession_pass=zp<=2))
assert len(out['planet_rows'])==16
ctrl=json.loads((HERE/'planets/controls_001/results.json').read_text())
assert ctrl['all_checks_pass'] and all(ctrl['checks'].values())
assert all(v==0 for row in ctrl['model_null'] for v in row['values'])
assert all(r['max_z_bound']<.02 for r in ctrl['orbital_series_domain'])
assert max(r['difference'] for r in ctrl['omitted_return'])>1e-4
out['additional_planet_controls']=dict(model_null_cases=len(ctrl['model_null']),
    omitted_return_cases=len(ctrl['omitted_return']),orbit_domain_cases=len(ctrl['orbital_series_domain']),passed=True)
out['all_planet_screens_fail']=all(not r['radial_pass'] and not r['monopole_precession_pass'] for r in out['planet_rows'])
out['completed_manifests']=sum(m['status']=='completed' for m in out['manifests'])
out['failed_manifests']=sum(m['status']=='failed' for m in out['manifests'])
out['scope']='Archived supplementary monopole screens; no covariance-refitted ephemeris likelihood or all-width claim.'
out['complete']=True;out['all_checks_pass']=True
args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
print(json.dumps({k:out[k] for k in ['completed_manifests','failed_manifests','all_planet_screens_fail','all_checks_pass']}),flush=True)
