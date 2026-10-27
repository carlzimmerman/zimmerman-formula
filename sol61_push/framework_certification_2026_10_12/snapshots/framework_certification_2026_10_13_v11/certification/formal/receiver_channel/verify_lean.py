"""Kernel compilation, axiom inspection and false-statement controls."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SOURCE = HERE.parent/'ReceiverChannel.lean'
LAKE = ROOT/'fable_independent_2026/lean_2026'
out = Path(sys.argv[1]).resolve()
assert out.is_relative_to(HERE) and out.is_dir()
src = SOURCE.read_text()
assert not re.search(r'\b(sorry|admit|native_decide|implemented_by)\b',src)
assert not re.search(r'^\s*(axiom|opaque)\s',src,re.M)
names = re.findall(r'^theorem (\w+)',src,re.M)
assert names == re.findall(r'^#print axioms FrameworkReceiverChannel\.(\w+)',src,re.M)
cases=[('main',SOURCE)]
for name,old,new in [
    ('wrong_energy_sign','p1 * reaction1 D p p2 g2 + p2 * reaction2 D p p1 g1','p1 * reaction1 D p p2 g2 - p2 * reaction2 D p p1 g1'),
    ('missing_recoil','def reaction1 (D p p2 g2 : ℝ) : ℝ := D*g2+p2*p','def reaction1 (D p p2 g2 : ℝ) : ℝ := D*g2'),
    ('wrong_boundary_sign','0 ≤ flux γ h f1 f2 0 f4','flux γ h f1 f2 0 f4 ≤ 0')]:
    assert src.count(old)==1
    path=out/(name+'.lean');path.write_text(src.replace(old,new));cases.append((name,path))
results=[]
for name,path in cases:
    argv=['lake','env','lean','-j','1',str(path)]
    p=subprocess.run(argv,cwd=LAKE,capture_output=True,text=True,timeout=180)
    log=p.stdout+p.stderr;(out/(name+'.log')).write_text(log)
    if name=='main':
        reports=re.findall(r"'FrameworkReceiverChannel\.(\w+)' depends on axioms: \[([^\]]*)\]",log)
        assert [n for n,_ in reports]==names
        assert all(set(a.strip() for a in deps.split(',') if a.strip()) <= {'propext','Classical.choice','Quot.sound'} for _,deps in reports)
        passed=p.returncode==0 and 'error:' not in log and 'warning:' not in log
    else:
        passed=p.returncode!=0 and 'error:' in log
    results.append({'case':name,'argv':argv,'exit_status':p.returncode,'passed':passed,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    print(name+': '+('PASS' if passed else 'FAIL'),flush=True)
summary={'theorems':names,'theorem_count':len(names),'all_passed':all(x['passed'] for x in results),'cases':results,
    'scope':'Conditional two-mode energy/momentum and boundary identities; no local field theory or spatial continuity theorem.'}
(out/'results.json').write_text(json.dumps(summary,indent=2)+'\n')
sys.exit(0 if summary['all_passed'] else 1)
