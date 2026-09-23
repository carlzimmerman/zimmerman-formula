"""Exact checks and fresh Lean compilation; no model API calls or observational claims."""
import ast
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import sympy as S

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OUT=Path(sys.argv[1]).resolve()
assert OUT.is_relative_to(HERE)
OUT.mkdir(exist_ok=True)
checks=[]

def zero(name,expr):
    residual=S.simplify(expr)
    if residual != 0: raise AssertionError((name,residual))
    checks.append({'name':name,'residual':str(residual)})

def differs(name,left,right):
    residual=S.simplify(left-right)
    if residual.is_zero is not False: raise AssertionError((name,residual))
    checks.append({'name':name,'nonzero_residual':str(residual)})

s,lam,g,y,x,q1,q2=S.symbols('s lambda g y x q1 q2',positive=True)
N=S.symbols('N',integer=True,positive=True)
U=lambda q:q*q/2-2*q+S.log(q)+S.Rational(3,2)
W=lambda z,l:z*z*(1-q1*q2)+(U(q1)+U(q2))/l**2
p=lam*y/(1+lam*y)
mu=1-(1-p)**2
q=1/(1+lam*y)
a0=s/(2*lam)
raw=s*s*W(g/s,lam)

# Derivation from the raw action, independent of the simplified Lean density.
zero('auxiliary_EL_q1',S.diff(W(y,lam),q1).subs({q1:q,q2:q}))
zero('auxiliary_EL_q2',S.diff(W(y,lam),q2).subs({q1:q,q2:q}))
reduced=W(y,lam).subs({q1:q,q2:q})
zero('envelope_flux',S.diff(W(y,lam),y).subs({q1:q,q2:q})/(2*y)-mu)
zero('reduced_flux',S.diff(reduced,y)/(2*y)-mu)
zero('raw_action_scale_identity',raw-(s/lam)**2*W(g/(s/lam),1))
zero('raw_action_at_fixed_a0',raw-(g*g*(1-q1*q2)+4*a0*a0*(U(q1)+U(q2))))
zero('fixed_a0_curve',mu.subs(y,x/(2*lam))-(1-(1+x/2)**(-2)))
zero('N_channel_slope',S.diff(1-(1-p)**N,y).subs(y,0)-N*lam)
zero('deep_matching',(2*lam/s)*a0-1)
zero('transverse_identity',mu-(lam*y)*(lam*y+2)/(1+lam*y)**2)
zero('longitudinal_identity',mu+y*S.diff(mu,y)-(lam*y)*((lam*y)**2+3*lam*y+4)/(1+lam*y)**3)
zero('zero_drive',mu.subs(y,0))
zero('saturation',S.limit(mu,y,S.oo)-1)
zero('high_drive_tail',S.limit(y*y*(1-mu),y,S.oo)-1/lam**2)
zero('slope_tail_product',(S.diff(mu,y).subs(y,0))**2*S.limit(y*y*(1-mu),y,S.oo)-4)
for order in (0,1,2):
    zero('vacuum_jet_'+str(order),S.limit(S.diff(reduced,y,order),y,0,dir='+'))
zero('cubic_coefficient',S.limit(reduced/y**3,y,0,dir='+')-4*lam/3)
z=S.symbols('z',positive=True)
zero('auxiliary_potential_derivative',S.diff(U(z),z)-(1-z)**2/z)
zero('auxiliary_potential_at_one',U(S.Integer(1)))
zero('promoted_weight_derivative',S.diff(reduced,lam)+4/lam**3*U(q))
zero('unit_weight_derivative_value',S.expand_log(S.diff(reduced,lam).subs({lam:1,y:1}),force=True)
     -(4*S.log(2)-S.Rational(5,2)))

# Explicit controls prevent confusing a0-normalized equivalence with equivalence at fixed s.
zero('half_at_lambda_1',(a0/s).subs(lam,1)-S.Rational(1,2))
zero('quarter_at_lambda_2',(a0/s).subs(lam,2)-S.Rational(1,4))
differs('fixed_s_kappa_counterexample',(a0/s).subs(lam,2),S.Rational(1,2))
differs('fixed_s_force_curves_are_distinct',mu.subs({lam:1,y:1}),mu.subs({lam:2,y:1}))
differs('count_only_slope_is_false',S.diff(1-(1-p)**2,y).subs({y:0,lam:2}),S.Integer(2))

# Existing certificates' exact dependencies: source inspection, not trust in headings.
legacy=ROOT/'deepseek_push/lean/PD21_law_of_nature.lean'
text=legacy.read_text()
assert 'hprinciple : kappa = 1 / (count : ℝ)' in text
assert 'hcount : count = 2' in text
pd08=ast.parse((ROOT/'deepseek_push/PD08_particle_free_derivation.py').read_text())
p_assignments=[ast.unparse(n.value) for n in ast.walk(pd08) if isinstance(n,ast.Assign)
               and any(isinstance(t,ast.Name) and t.id=='p' for t in n.targets)]
assert 'Y + c2 * Y ** 2' in p_assignments

project=ROOT/'fable_independent_2026/lean_2026'
manifest=json.loads((project/'lake-manifest.json').read_text())
libraries=[project/'.lake/build/lib/lean']+[
    project/manifest.get('packagesDir','.lake/packages')/item['name']/'.lake/build/lib/lean'
    for item in manifest['packages']]
env=dict(os.environ,LEAN_PATH=os.pathsep.join(map(str,libraries)))
compiler=subprocess.check_output(['/opt/homebrew/bin/elan','which','lean'],cwd=project,text=True,timeout=10).strip()
formal=[]
for source,log,count in [(HERE/'Selection.lean','lean.txt',13),
                         (HERE.parent/'kappa_unit_response_2026_09_20/UnitResponse.lean','upstream_lean.txt',14)]:
    run=subprocess.run([compiler,str(source)],cwd=project,env=env,capture_output=True,text=True,timeout=90)
    output=run.stdout+run.stderr
    (OUT/log).write_text(output)
    if run.returncode or re.search(r'sorryAx|warning:|error:',output):
        raise AssertionError(output)
    audited=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",output)
    assert len(audited)==count,(source,len(audited),count)
    for name,axioms in audited:
        assert {a.strip() for a in axioms.split(',')} <= {'propext','Classical.choice','Quot.sound'}
    formal.append({'source':str(source.relative_to(ROOT)),'theorems':len(audited),
                   'exit_code':run.returncode,'names':[name for name,_ in audited]})

result={'requested_goal':'Independent physical selection of kappa=1/2',
        'goal_status':'NOT ESTABLISHED; not entailed by the specified static-family conditions',
        'checks':checks,'exact_check_count':len(checks),'formal':formal,
        'strongest_result':'Static action depends only on s/lambda; normalized curve is lambda independent. '
                           'Positive lambda=2 satisfies the tested static conditions but gives kappa=1/4 at fixed s.',
        'legacy_premises':{'PD21':['kappa = 1/count','count = 2'],'PD08_p_assignments':p_assignments},
        'non_claims':['No impossibility theorem for all particle-free theories',
                      'No full covariant stability or observational viability of the counterexample',
                      'No claim that s may be changed when comparing fixed-vacuum physical models',
                      'No global novelty claim; no new physical mechanism selecting lambda=1']}
(OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('checks','legacy_premises')},indent=2))
