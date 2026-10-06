"""Exact directional norm-cube source and high-mode response; report supplies uniform remainder proof."""
import sympy as s,json,sys
from pathlib import Path
x=s.symbols('x',real=True);K,k,v,a0,H,A=s.symbols('K k v a0 H A',positive=True);aa=s.symbols('a',positive=True)
def main():
 out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True);ctl=sys.argv[2] if len(sys.argv)>2 else 'none';checks={}
 def check(n,b):checks[n]=bool(b);print(('PASS ' if b else 'FAIL ')+n)
 # I=gradnu²/(a²a0²); volume a³, coefficient2K a0²(-I^1.5/12).
 g=s.symbols('g',positive=True);cube=2*K*a0*a0*aa**3*(-(g*g/(aa*aa*a0*a0))**s.Rational(3,2)/12)
 check('scale factor cancels from cubic action',s.simplify(cube+K*g**3/(6*a0))==0)
 grad=-v*k*s.sin(x);force=s.diff(-v*v*k*k*s.sin(x)**2,x)*k*K/(2*a0)
 check('actual force on positive-sin cell',s.simplify(force+K*v*v*k**3*s.sin(x)*s.cos(x)/a0)==0)
 # |sin|cos cosine coefficients; odd j, direct exact integral benchmarks.
 for j in (1,3,5,7):
  actual=2/s.pi*s.integrate(s.sin(x)*s.cos(x)*s.cos(j*x),(x,0,s.pi))
  candidate=(2 if ctl=='half' else 4)/(s.pi*(4-j*j))
  check('odd coefficient '+str(j),s.simplify(actual-candidate)==0)
 for j in (0,2,4):check('even coefficient '+str(j),s.integrate(s.sin(x)*s.cos(x)*s.cos(j*x),(x,0,s.pi))==0)
 C=s.symbols('C',real=True);Z=C/(12*H**2)*(aa**-5+3*aa**-1-4*aa**-2)
 dt=lambda z:H*aa*s.diff(z,aa)
 check('high-mode forced temporal equation',s.simplify(dt(dt(Z))+3*H*dt(Z)+2*H**2*Z-C*aa**-5)==0)
 check('zero initial secondorder curvature',Z.subs(aa,1)==0 and dt(Z).subs(aa,1)==0)
 check('nonzero bracket factorization',s.expand(1+3*aa**4-4*aa**3-(aa-1)**2*(3*aa**2+2*aa+1))==0)
 P=s.symbols('P',positive=True);An=s.symbols('An',negative=True)
 kr=An*P/(An*H**2-P);d=P/(An*H**2-P);b=An*H/(An*H**2-P)
 check('high-frequency kinetic orderzero',s.limit(kr,P,s.oo)==-An)
 check('high-frequency direct force survives',s.limit(d,P,s.oo)==-1)
 check('shift Bardeen correction gains two powers',s.limit(P*b,P,s.oo)==-An*H)
 if ctl=='smooth_claim':check('candidate force C1 at zero node',s.limit(s.diff(s.sin(x)*s.cos(x),x),x,0,dir='+')==-s.limit(s.diff(s.sin(x)*s.cos(x),x),x,0,dir='+'))
 if ctl=='smoothing':check('candidate high-mode inverse vanishes',s.limit(1/kr,P,s.oo)==0)
 (out/'results.json').write_text(json.dumps({'checks':checks,'source':'Jnu=−K k³ v|v|/a0 |sin(kx)|cos(kx)','odd_coeff':'4/[pi(4-j²)]','high_mode_solution':'C/(12H²)*(a^-5+3a^-1−4a^-2)','scope':'n3 fixed0<eta<1, finite time interval, zero secondorder curvature data; no full nonlinear or weak admission'},indent=2)+'\n')
 return 0 if all(checks.values()) else 1
if __name__=='__main__':sys.exit(main())
