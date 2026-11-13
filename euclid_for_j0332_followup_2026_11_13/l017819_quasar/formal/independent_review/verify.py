"""Independent bounded positive and genuine false-mutation Lean compilation.

Only writes this review directory. Canonical Lean project and audited file are
read-only inputs. A nonzero exit alone never qualifies as a negative control.
"""
from pathlib import Path
import hashlib,json,re,subprocess,time,platform
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
SOURCE=P.parent/'TwoImageShear.lean'
WORK=ROOT/'fable_independent_2026/lean_2026'
HASH=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
INPUTS=[SOURCE,ROOT/'euclid_for_j0332_followup_2026_11_13/l017819_quasar/host_control/fit_host.py',ROOT/'euclid_for_j0332_fit_2026_11_13/lens_models.py',WORK/'lean-toolchain',WORK/'lakefile.toml',WORK/'lake-manifest.json',P/'verify.py']
before={str(p):HASH(p) for p in INPUTS}
raw=SOURCE.read_text()
assert not re.search(r'\b(sorry|admit|sorryAx)\b|^\s*axiom\b',raw,re.M)
def run(args,name):
    start=time.monotonic()
    proc=subprocess.run(args,cwd=WORK,capture_output=True,text=True,timeout=90)
    log=proc.stdout+proc.stderr;(P/name).write_text(log)
    return dict(argv=args,cwd=str(WORK),exit_code=proc.returncode,seconds=time.monotonic()-start,log=str(P/name),log_sha256=HASH(P/name)),log
version,versiontext=run(['lake','env','lean','--version'],'version.log')
positive,plog=run(['lake','env','lean',str(SOURCE)],'compile.log')
assert positive['exit_code']==0 and 'sorryAx' not in plog and 'warning: declaration uses' not in plog
audit=P/'TwoImageShear_AllAxioms.lean'
names=['inverse_components','shear_norm_identity','unique_shear','any_two_deflections_have_common_source','distinct_pair_denominator']
audit.write_text(raw+'\n'+''.join('#print axioms TwoImageShear.'+n+'\n' for n in names))
axrun,axlog=run(['lake','env','lean',str(audit)],'all_axioms.log')
assert axrun['exit_code']==0
lists=re.findall(r'depends on axioms:\s*\[([^\]]*)\]',axlog)
assert len(lists)>=len(names)
axioms=sorted(set(a.strip() for s in lists for a in s.split(',') if a.strip()))
assert set(axioms)<= {'propext','Classical.choice','Quot.sound'}
old='(vx ^ 2 + vy ^ 2) / (dx ^ 2 + dy ^ 2) := by'
assert raw.count(old)==1
mutation=P/'TwoImageShear_FALSE.lean'
mutation.write_text(raw.replace(old,'2 * (vx ^ 2 + vy ^ 2) / (dx ^ 2 + dy ^ 2) := by'))
negative,nlog=run(['lake','env','lean',str(mutation)],'mutation_compile.log')
bad=re.search(r'file.not.found|no such file|unknown module|unknown package|does not exist|failed to open|object file.*does not exist|invalid.*import',nlog,re.I)
assert not bad,('Invalid negative control: dependency/input failure',bad.group(0) if bad else '')
assert negative['exit_code']!=0 and re.search(r'unsolved goals|tactic.*failed|failed to prove',nlog,re.I)
assert 'shear_norm_identity' in mutation.read_text() and 'TwoImageShear_FALSE.lean:' in nlog
after={str(p):HASH(p) for p in INPUTS};assert before==after
result=dict(status='completed',review_provenance='Independent subagent raw-source audit; fresh derivation and unchanged-source compile.',
    claim='Two distinct positions admit a unique unrestricted trace-free shear for any supplied deflection difference and fixed convergence.',
    scope='Algebraic nuisance elimination only; not physical environment, observational association, image fit, PDE or gravity-law certification.',
    positive_compile=positive,all_axioms_compile=axrun,negative_control_compile=negative,
    negative_control='Norm RHS multiplied by2: false at dx=1,dy=0,vx=1,vy=0. Requires genuine unsolved-goal diagnostic.',
    mutation_sha256=HASH(mutation),axioms=axioms,version=versiontext.strip(),platform=platform.platform(),
    input_sha256_before=before,input_sha256_after=after)
(P/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
