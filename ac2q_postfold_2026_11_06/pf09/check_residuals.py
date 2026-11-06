import argparse,json,subprocess,sys
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();p=Path(__file__).parent/'review'
results={name:json.loads(subprocess.check_output([sys.executable,str(p/name)],text=True))for name in ['derive_geometry.py','derive_matter.py']}
g=results['derive_geometry.py'];m=results['derive_matter.py'];checks={'geometry_zero_source':g['independent_sources_zero'],'geometry_derivatives_cancel':g['spatial_K_a_derivatives_cancel'],**m['checks']}
out=dict(checks=checks,all_pass=all(checks.values()),raw=results,scope='Exact symbolic residual identities for declared promoted on-branch system; not local existence or singular selection')
Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'all_pass':out['all_pass'],'checks':checks},indent=2));raise SystemExit(0 if out['all_pass']else 1)
