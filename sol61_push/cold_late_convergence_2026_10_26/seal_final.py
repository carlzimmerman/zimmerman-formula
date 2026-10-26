"""Add analysis contracts and local regression controls before final execution."""
import argparse,json,subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1];ap=argparse.ArgumentParser();ap.add_argument('case',choices=['analysis','audit']);a=ap.parse_args();subprocess.run([sys.executable,str(P/'seal.py'),a.case],check=True);dest=P/(a.case+'_contract.json');d=json.loads(dest.read_text());extra=['seal_final.py','ANALYSIS_CONTRACT.md','HIGHER_IC_CONTRACT.md','DIAGNOSTIC_ADDENDUM.md','COVERAGE_REPAIR.md']
if a.case=='audit':extra+=['test_comparison_keys.py','test_quadrature.py','quadrature.py']
d['execution_artifacts']=sorted(set(d['execution_artifacts']+[str((P/f).relative_to(ROOT)) for f in extra]));dest.write_text(json.dumps(d,indent=2))
