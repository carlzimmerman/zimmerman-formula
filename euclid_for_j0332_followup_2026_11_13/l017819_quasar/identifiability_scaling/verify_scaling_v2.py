"""Bounded positive compilation, axioms audit, false mutation and exact examples."""
from pathlib import Path
from fractions import Fraction as Q
import argparse,hashlib,json,re,subprocess,time,platform

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
WORK=ROOT/'fable_independent_2026/lean_2026'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def exact_checks():
    ks=[Q(1,2),Q(1),Q(3,2),Q(2)]
    flux_rows=[]
    def flux(a,g):
        x=abs(g)/a
        return x/(1+x)*g
    for k in ks:
        for a in [Q(1,3),Q(1),Q(2)]:
            for g in [Q(-2),Q(0),Q(1),Q(3)]:
                before=flux(a,g);after=flux(k*a,k*g)
                assert after==k*before
                flux_rows.append([str(x) for x in [k,a,g,before,after]])
    def beta(theta,alpha,shear,kappa):
        x,y=theta;g1,g2=shear
        return ((1-kappa)*x-alpha[0]-g1*x-g2*y,
                (1-kappa)*y-alpha[1]-g2*x+g1*y)
    brightness=lambda b:1+b[0]**2+b[1]**2
    image_rows=[]
    for k in ks:
        for kappa in [Q(-1,5),Q(0),Q(1,10)]:
            for shear in [(Q(0),Q(0)),(Q(3,100),Q(-1,25))]:
                for theta in [(Q(0),Q(0)),(Q(1),Q(0)),(Q(0),Q(2)),(Q(-1,2),Q(3,2))]:
                    x,y=theta;alpha=(x*x-y,x+y*y)
                    b=beta(theta,alpha,shear,kappa)
                    changed=beta(theta,tuple(k*t for t in alpha),tuple(k*t for t in shear),k*kappa+1-k)
                    assert changed==tuple(k*t for t in b)
                    assert brightness(tuple(t/k for t in changed))==brightness(b)
                    image_rows.append({'k':str(k),'kappa':str(kappa),'theta':list(map(str,theta)),
                        'beta':list(map(str,b)),'scaled_beta':list(map(str,changed)),'brightness':str(brightness(b))})
    density_rows=[]
    for k in ks:
        for a in [Q(1,3),Q(1),Q(2)]:
            c,G=Q(2),Q(3);rho=a*a/(c*c*G/4)
            assert (k*a)**2==(c*c*G/4)*(k*k*rho)
            density_rows.append(list(map(str,[k,a,rho,k*k*rho])))
    # Hand-computable failures of omitting required changes.
    assert flux(Q(1),Q(2))!=2*flux(Q(1),Q(1))
    wrong_kappa=Q(2)*0+1-2*Q(2)
    wrong_beta=beta((Q(1),Q(0)),(Q(0),Q(0)),(Q(0),Q(0)),wrong_kappa)
    assert wrong_beta==(Q(4),Q(0)) and wrong_beta!=(Q(2),Q(0))
    return {'arithmetic':'Python fractions.Fraction exact rationals','flux_cases':len(flux_rows),
        'image_cases':len(image_rows),'density_cases':len(density_rows),
        'flux_rows':flux_rows,'image_rows':image_rows,'density_rows':density_rows,
        'fixed_a0_counterexample':'a=1,g=1,k=2: F_a(kg)=4/3, kF_a(g)=1',
        'false_convergence_counterexample':'theta=(1,0),alpha=shear=kappa=0,k=2: correct beta=(2,0); mutated kappa=1-2k gives beta=(4,0)'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--source',required=True);args=p.parse_args()
    out=Path(args.output);out.mkdir(exist_ok=True,parents=True);source=Path(args.source).resolve()
    raw=source.read_text()
    # This source has no nested block comments. English "admit" in a comment
    # is not the Lean tactic; the kernel axioms check below remains mandatory.
    code=re.sub(r'/\-.*?\-/','',raw,flags=re.S)
    code=re.sub(r'--[^\n]*','',code)
    assert not re.search(r'\b(sorry|admit|sorryAx)\b|^\s*axiom\b',code,re.M)
    names=re.findall(r'^theorem\s+(\w+)',raw,re.M)
    assert len(names)==13
    def run(argv,name):
        start=time.monotonic();r=subprocess.run(argv,cwd=WORK,capture_output=True,text=True,timeout=100)
        log=r.stdout+r.stderr;(out/name).write_text(log)
        return {'argv':argv,'cwd':str(WORK),'exit_code':r.returncode,'seconds':time.monotonic()-start,
            'log':str(out/name),'sha256':digest(out/name)},log
    version,vlog=run(['lake','env','lean','--version'],'version.log')
    positive,plog=run(['lake','env','lean',str(source)],'compile.log')
    (out/'positive_compile.json').write_text(json.dumps(positive,indent=2))
    assert positive['exit_code']==0,plog
    assert 'sorryAx' not in plog and 'declaration uses' not in plog
    listed=re.findall(r'depends on axioms:\s*\[([^\]]*)\]',plog)
    axioms=sorted(set(a.strip() for group in listed for a in group.split(',') if a.strip()))
    assert len(listed)==len(names),(len(listed),len(names),plog)
    assert set(axioms)<= {'propext','Classical.choice','Quot.sound'},axioms
    mutation=out/'ConditionalScaling_FALSE.lean'
    assert raw.count('k*kappa+1-k')==3
    mutation.write_text(raw.replace('k*kappa+1-k','k*kappa+1-2*k',1))
    negative,nlog=run(['lake','env','lean',str(mutation.resolve())],'mutation_compile.log')
    invalid=re.search(r'file.not.found|no such file|unknown module|unknown package|does not exist|failed to open|invalid.*import',nlog,re.I)
    assert not invalid,('invalid negative control',nlog)
    assert negative['exit_code']!=0 and re.search(r'unsolved goals|tactic.*failed|failed to prove',nlog,re.I),nlog
    assert 'ConditionalScaling_FALSE.lean:' in nlog
    checks=exact_checks();(out/'exact_countercheck.json').write_text(json.dumps(checks,indent=2))
    mathlib=WORK/'.lake/packages/mathlib'
    rev=subprocess.run(['git','rev-parse','HEAD'],cwd=mathlib,capture_output=True,text=True,check=True).stdout.strip()
    dirty=subprocess.run(['git','status','--porcelain'],cwd=mathlib,capture_output=True,text=True,check=True).stdout
    result={'status':'completed','source':str(source),'source_sha256':digest(source),'theorems':names,'axioms':axioms,
        'positive_compile':positive,'negative_compile':negative,'mutation_sha256':digest(mutation),
        'version':vlog.strip(),'version_command':version,'platform':platform.platform(),
        'mathlib_commit':rev,'mathlib_dirty_status':dirty,
        'finite_exact_checks':{k:v for k,v in checks.items() if not k.endswith('_rows')},
        'scope':'Exact conditional identities over real normed spaces and supplied linear operators; no analytic PDE, physical external sheet, full cosmological family or empirical fit certified.',
        'review_provenance':'Author self-review plus separate exact-rational implementation; not an independent human or independent-model proof audit.',
        'dependency_limit':'Lean/Mathlib installed compiled dependency tree is trusted; lock files, toolchain and source are hashed, not every transitive compiled library artifact.'}
    (out/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ['positive_compile','negative_compile','version_command']},indent=2))

if __name__=='__main__':main()
