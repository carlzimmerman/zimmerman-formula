import sys,subprocess,json
from pathlib import Path
out=Path(sys.argv[1]);base=Path(__file__).parent;mo=out.parent/'modes.json'
subprocess.run([sys.executable,str(base/'modes.py'),str(mo)],check=True,capture_output=True,text=True)
subprocess.run([sys.executable,str(base/'escape.py'),str(out),str(mo)],check=True)
prior=json.loads(Path('sol61_push/radial_phonon_escape_2026_10_14/run/results.json').read_text())
result=json.loads(out.read_text());md=json.loads(mo.read_text());comparisons=[]
for case,old in zip(result['cases'],prior['cases']):
 assert case['candidate']==old['candidate']
 error=abs(case['partial_escape_sums_per_s']['40']/old['partial_escape_sums_per_s']['40']-1)
 assert error<1e-7
 comparisons.append(dict(candidate=case['candidate'],first_40_relative_change=error,relative_increment_160_to_320=case['partial_escape_sums_per_s']['320']/case['partial_escape_sums_per_s']['160']-1))
result['parent_comparisons']=comparisons;result['elastic_checks']=md['passed']
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(parent_comparisons=comparisons,elastic_checks=md['passed']),indent=2))
