from pathlib import Path
import hashlib, json, math, platform, subprocess, sys, time
from fractions import Fraction as F
ROOT=Path('/Users/carlzimmerman/new_physics/zimmerman-formula')
OWN=ROOT/'fine_structure_puzzle/qcd_sea_curvature/reviews/curved_sea'
TARGET=ROOT/'fine_structure_puzzle/qcd_sea_curvature/curved_response'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def simpson(fun,a,b,n=16384):
    h=(b-a)/n
    return h/3*(fun(a)+fun(b)+4*math.fsum(fun(a+h*k) for k in range(1,n,2))+2*math.fsum(fun(a+h*k) for k in range(2,n,2)))

# Preserve the target. Run its documented script from a byte-identical owned copy.
script=TARGET/'checks/check_trace_cut.py'
(OWN/'checks').mkdir(exist_ok=True)
copied=OWN/'checks/check_trace_cut.py'
copied.write_bytes(script.read_bytes())
before={str(p.relative_to(ROOT)):sha(p) for p in [script,TARGET/'DERIVATION.md',TARGET/'REPORT.md',TARGET/'SOURCES.json',TARGET/'INPUTS.json']}
start=time.time()
r=subprocess.run([sys.executable,str(copied)],cwd=ROOT,capture_output=True,text=True,timeout=30)
(OWN/'checks/reproduced_stdout.txt').write_text(r.stdout)
(OWN/'checks/reproduced_stderr.txt').write_text(r.stderr)
assert r.returncode==0
reproduced=json.loads((OWN/'checks/RESULTS.json').read_text())
# Independent invariant: derive the cutoff moment in the original dimensionless
# s/M^2 variable; u=log(s/(4M^2)) fixes the finite interval, not the target's beta map.
cutoff_cases=[]
for b in [5.,9.,16.,25.,100.]:
    top=math.sqrt(math.log(b/4))
    # u=w^2 removes the square-root threshold endpoint.
    def original_s(w):
        s=4*math.exp(w*w)
        return 2*w*math.sqrt(-math.expm1(-w*w))*(s+2)**2/s**3
    numerical=simpson(original_s,0.,top)
    v=math.sqrt(1-4/b)
    exact=(3*v**3-F(6,5)*v**5+F(1,7)*v**7)/8
    assert abs(numerical-float(exact))<2e-13
    cutoff_cases.append({'smax_over_M2':b,'original_s_integral':numerical,'polynomial':float(exact),'absolute_error':abs(numerical-float(exact))})
# Independent analytic bubble versus target quadrature for the minimal case.
module={}
exec(compile(script.read_text(),str(script),'exec'),module)
bubble_cases=[]
for z in [1.,4.,16.,64.]:
    a=math.sqrt(1+4/z)
    L=-2+a*math.log((a+1)/(a-1))
    from_analytic=((2-z)**2*L-2*z/3+(F(1,15)+F(2,3))*z*z)/z**3
    from_cut=module['spectral_kernel'](z,1.)
    err=abs(float(from_analytic)-from_cut)
    assert err<2e-13
    bubble_cases.append({'z':z,'analytic_bubble':float(from_analytic),'cut_quadrature':from_cut,'absolute_error':err})
assert F(1,6)+F(1,15)+F(1,105)==F(17,70)
assert 2*12*F(2,5)/32==F(3,10)
assert -4*F(17,70)/32== -F(17,560)
manifest=json.loads((TARGET/'INPUTS.json').read_text())
input_checks=[]
for x in manifest['snapshots']:
    snap=TARGET/x['snapshot_path']
    actual=sha(snap)
    assert actual==x['sha256']
    source=ROOT/x['source_path']
    input_checks.append({'snapshot':str(snap.relative_to(ROOT)),'expected_sha256':x['sha256'],'actual_sha256':actual,'source_matches_snapshot':sha(source)==actual})
after={p:sha(ROOT/p) for p in before}
assert before==after
out={'status':'completed','outcome':'implementation and finite assertion verified in stated range','claim_scope':'LO chiral trace cut only; no full QCD+QED/sphere coefficient','argv':[sys.executable,str(copied)],'python':sys.version,'platform':platform.platform(),'runtime_seconds':time.time()-start,'git_observation':'not performed by instruction','input_hashes_before':before,'input_hashes_after':after,'target_script_copy_sha256':sha(copied),'target_reproduction_max_error':reproduced['maximum_absolute_kernel_difference'],'independent_cutoff_cases':cutoff_cases,'analytic_bubble_cases':bubble_cases,'input_snapshot_checks':input_checks,'non_claims':['No measured inputs used','Quadrature agreement is bounded numerical evidence, not global certification','No target files modified']}
(OWN/'CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['input_hashes_before','input_hashes_after','independent_cutoff_cases','analytic_bubble_cases','input_snapshot_checks']},indent=2))
