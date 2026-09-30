"""Independent core convention and CFG43 cap coefficient audit."""
import argparse,json,hashlib,math
from pathlib import Path
import sympy as s
checks=[]
def check(name,ok,detail=''):
 checks.append(dict(name=name,passed=bool(ok),detail=detail));print(('PASS ' if ok else 'FAIL ')+name)
G,H,Lambda,kappa,Omega=s.symbols('G H Lambda kappa Omega',positive=True)
rho_total=3*H**2/(8*s.pi*G);rho_vac=Lambda/(8*s.pi*G)
a_H=kappa*s.sqrt(G*rho_total);a_L=kappa*s.sqrt(G*rho_vac)
check('vacuum coefficient identity',s.simplify(Lambda/a_L**2)==8*s.pi/kappa**2)
check('H based coefficient includes Omega_DE',s.simplify((Lambda/a_H**2).subs(Lambda,3*H**2*Omega))==8*s.pi*Omega/kappa**2)
check('half coefficient is inserted target',s.simplify((Lambda/a_L**2).subs(kappa,s.Rational(1,2)))==32*s.pi)
check('H based target agrees only in de Sitter limit',s.solve(s.Eq(32*s.pi*Omega,32*s.pi),Omega)==[1])
b,a=s.symbols('b a',positive=True)
p2=s.sqrt(b*b+a*b);simple=(b+s.sqrt(b*b+4*a*b))/2
check('P2 and simple differ at knee',p2.subs(b,a)!=simple.subs(b,a))
check('P2 high field anomalous half scale',s.limit(p2-b,b,s.oo)==a/2)
check('simple high field anomalous full scale',s.limit(simple-b,b,s.oo)==a)
# Actual CFG43 constitutive input; reconstruct independently.
n,m,eps,nu,Mp,L=s.symbols('n m epsilon nu_s Mp2 L',positive=True)
x=m*n/(nu*Mp*L)
rho=m*n+eps*Mp*L*x*s.atan(x)
pressure=s.simplify(n*s.diff(rho,n)-rho)
check('CFG43 pressure cap derivation',s.simplify(pressure-eps*Mp*L*x*x/(1+x*x))==0)
check('CFG43 vacuum derivative equals minus pressure over Lambda',s.simplify(s.diff(rho,L)+pressure/L)==0)
check('CFG43 a0 dictionary leaves epsilon',s.simplify(L/((eps*Mp*L)/Mp))==1/eps)
check('CFG43 target fixes epsilon as extra input',s.solve(s.Eq(1/eps,32*s.pi),eps)==[1/(32*s.pi)])
xx=s.symbols('x',positive=True)
# rho_n=m[1+eps/nu*(atan x+x/(1+x²))] >0.
# n rho_nn=2m eps x/[nu(1+x²)²] >0.
B=s.atan(xx)+xx*(xx*xx-1)/(1+xx*xx)**2
check('subluminal sound speed inequality derivative',s.simplify(s.diff(B,xx)-8*xx*xx/(1+xx*xx)**3)==0)
check('subluminal sound speed inequality origin',s.limit(B,xx,0)==0)
cs2=s.simplify(n*s.diff(rho,n,2)/s.diff(rho,n))
csxx=2*eps*xx/(nu*(1+xx*xx)**2+eps*((1+xx*xx)**2*s.atan(xx)+xx*(1+xx*xx)))
check('characteristic sound speed independently reduced',s.simplify(cs2.subs(n,xx*nu*Mp*L/m)-csxx)==0)
rows=[]
for C in (16*math.pi,32*math.pi,64*math.pi):
 ep=1/C
 vals=[float(csxx.subs({eps:ep,nu:1,xx:v})) for v in (.001,.1,1,10,1000)]
 check('cap counterfamily local sound speeds C='+str(C),all(0<v<1 for v in vals))
 rows.append(dict(Lambda_over_a0_squared=C,epsilon=ep,sound_speed_squared_values=vals))
# HT T variation yields partial Lambda=0; Lambda variation changes clock divergence,
# not a constraint on eps when clock boundary data are unconstrained.
clock=s.simplify(1+s.diff(rho,L)/Mp)
check('HT clock absorbs fluid Lambda derivative',s.simplify(clock-(1-pressure/(Mp*L)))==0)
sources=['real_research/FOUNDATIONS.md','real_research/THE_SURVIVING_THEORY.md','real_research/derivation_chain_2026/README.md','real_research/derivation_chain_2026/FP0_core_postulates.py','fable_independent_2026/THE_COMPLETE_THEORY_2026-09-08.md','qwen_claude_field_theory/FINAL_THEORY_MMG_CONSOLIDATED_2026-08-27.md','campaign_fresh_gravity/closure_map/README.md','campaign_fresh_gravity/closure_map/DOOR11_RESULT_2026-09-29.md','campaign_fresh_gravity/CFG43_fluid_tie/A1_action_field_equations_dof.py','real_research/papers/v12_FORMAL_CORE_action.md','real_research/papers/ZIMMERMAN_THEORY_OF_GRAVITY.md']
hashes={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in sources}
result=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,cap_counterfamily=rows,source_sha256=hashes,scope='Exact conventions and declared CFG43 fluid characteristic signs. Review of source health verdicts is documentary, not independent full rerun.',non_claims=['Not a full constraint or perturbation audit','No galaxy fluid closure','No choice between empirical candidates','No 32pi prediction'])
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print('%s %s/%s'%(result['status'],result['passed'],result['total']));raise SystemExit(result['status']!='PASS')
