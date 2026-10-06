import argparse,json
from pathlib import Path
import mpmath as m
import sympy as s
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,required=True);args=p.parse_args();out=args.output_dir.resolve();out.relative_to(HERE);out.mkdir(parents=True,exist_ok=True)
y=s.symbols('y',positive=True);f=s.sqrt(y*y+y)-y
primitive=(y+s.Rational(1,2))*s.sqrt(y*y+y)/2-y*y/2-s.log(2*y+1+2*s.sqrt(y*y+y))/8
exact=s.simplify(s.diff(primitive+f*f,y)-f*(1+2*s.diff(f,y)))==0
m.mp.dps=70
fm=lambda z:1/(m.sqrt(1+1/z)+1)
Pm=lambda z:(z+m.mpf('.5'))*m.sqrt(z*z+z)/2-z*z/2-m.log(2*z+1+2*m.sqrt(z*z+z))/8
root=m.findroot(lambda z:Pm(z)+fm(z)**2-32*m.pi,202)
quad=m.quad(fm,[0,1,root]);error=abs(quad-Pm(root))
r=dict(exact_derivative_identity=exact,root=m.nstr(root,65),window_integral=m.nstr(Pm(root),60),tail_floor=m.nstr(fm(root)**2,60),independent_quadrature_error=m.nstr(error,10),arithmetic='mpmath70decimal',scope='Numerical root plus exact symbolic derivative; tail inequality itself proved in TAIL_LEMMA_REVIEW.md')
(out/'results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
raise SystemExit(0 if exact and error<m.mpf('1e-60') and 202<root<203 else 1)
