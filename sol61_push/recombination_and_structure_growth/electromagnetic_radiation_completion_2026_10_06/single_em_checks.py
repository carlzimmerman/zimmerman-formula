"""One Maxwell field: exact fixed-clock Gauss and principal for parallel E,B."""
import argparse,json
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True);args=ap.parse_args();out=args.output_dir.resolve();out.relative_to(HERE);out.mkdir(parents=True,exist_ok=True)
g=s.symbols('g',positive=True);ep,et,bt=s.symbols('Eparallel Etransverse Btransverse',real=True);p=s.symbols('p',positive=True);x=s.symbols('x',real=True);a1,a2,v1,v2,l=s.symbols('a1 a2 v1 v2 l',real=True)
checks=[]
def ze(n,e):e=s.factor(e);checks.append(dict(name=n,passed=e==0,detail=str(e)));print(('PASS 'if e==0 else'FAIL ')+n)
raw=(v1*v1+v2*v2+l*l-p*p*(a1*a1+a2*a2))/2+g*(ep*l+et*v1+bt*p*a2)**2/2
ls=-g*ep*(et*v1+bt*p*a2)/(1+g*ep*ep)
ze('single_U1_Gauss',s.diff(raw,l).subs(l,ls));red=s.factor(raw.subs(l,ls));target=(v1*v1+v2*v2-p*p*(a1*a1+a2*a2))/2+g*(et*v1+bt*p*a2)**2/(2*(1+g*ep*ep));ze('single_U1_reduction',red-target)
vel=[v1,v2];field=[a1,a2];K=s.hessian(red,vel);V=s.hessian(red,field);G=s.Matrix([[s.diff(red,vel[i],field[j])-s.diff(red,field[i],vel[j])for j in range(2)]for i in range(2)]);D=s.factor((-x*x*K-s.I*x*G/p-V/p**2).det());ke=(1+g*(ep*ep+et*et))/(1+g*ep*ep);speed=(1+g*ep*ep-g*bt*bt)/(1+g*(ep*ep+et*et));ze('single_U1_two_physical_modes',D-ke*(1-x*x)*(speed-x*x));ze('single_U1_kinetic_positive_dictionary',K.det()-ke)
ze('perpendicular_magnetic_instability',speed.subs({ep:0,et:0,bt:1,g:2})+1);ze('perpendicular_electric_speed',speed.subs(bt,0).subs(ep,0)-1/(1+g*et*et));ze('parallel_wave_unmodified',speed.subs({et:0,bt:0})-1)
(out/'results.json').write_text(json.dumps(dict(checks=checks,characteristic=str(D),speed_squared=str(speed),scope='One U1 on local constant parallel E,B background, k orientationencoded by parallel/transversecomponents; fixedclockmetric, no isotropicFRW singlefieldclaim'),indent=2)+'\n');raise SystemExit(0 if all(c['passed']for c in checks)else 1)
