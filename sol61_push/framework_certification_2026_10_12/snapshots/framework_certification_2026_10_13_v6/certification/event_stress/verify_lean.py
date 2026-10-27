from pathlib import Path
import hashlib,json,re,subprocess,sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
LAKE=ROOT/'fable_independent_2026/lean_2026'
dest=Path(sys.argv[1]).resolve(); source=HERE/'EventStress.lean'; text=source.read_text()
names=['completed_stress_identity','completed_stress_nonnegative','projected_relative_motion_strict','every_spatial_projection_nonnegative']
controls={
 'FalseNonpositive':'\ntheorem false_nonpositive : FrameworkEventStress.stressJump 1 1 1 (-1) ≤ 0 := by\n  norm_num [FrameworkEventStress.stressJump]\n',
 'FalseUnrelatedSource':'\ntheorem false_unrelated_source : (0 : ℝ) ≤ 0 ^ 2 / 1 + 0 ^ 2 / 1 - 1 ^ 2 / 2 := by\n  norm_num\n'}
cases=[]
for case,tail in [('main','')]+list(controls.items()):
 p=source if case=='main' else dest/(case+'.lean')
 if tail:p.write_text(text+tail)
 argv=['lake','env','lean','-j','1',str(p)]
 run=subprocess.run(argv,cwd=LAKE,capture_output=True,text=True,timeout=120)
 out=run.stdout+run.stderr;(dest/(case+'.log')).write_text(out)
 if case=='main':
  reports=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",out)
  ok=run.returncode==0 and 'error:' not in out and 'warning:' not in out and set(x[0] for x in reports)=={'FrameworkEventStress.'+x for x in names}
  ok=ok and all(set(y.strip() for y in a.split(',') if y.strip())<={'propext','Classical.choice','Quot.sound'} for _,a in reports)
 else:ok=run.returncode!=0 and '⊢ False' in out and 'unsolved goals' in out
 cases.append({'case':case,'argv':argv,'exit_status':run.returncode,'passed':ok,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
out={'all_passed':all(x['passed'] for x in cases),'theorem_count':4,'theorems':names,'cases':cases,'scope':'Completed particle stress projections only, with energy/momentum additions and positive energies; no coherent tensor, quantum reduction or rate claim.'}
(dest/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert out['all_passed']
