import sys,json,pathlib
import sympy as s
x=s.symbols('x',real=True);A,N=s.symbols('A N',positive=True);F=s.Function('F',positive=True)(x);D=s.Function('D')(x);Y=s.Function('Y')(x)
B=2+s.diff(F,x)/(2*F);b=3*s.exp(-3*x)/(2*F);p=s.exp(2*x)*s.sqrt(F);w=s.Rational(3,2)*s.exp(-x)/s.sqrt(F)
checks={}
def zero(k,v):checks[k]=bool(s.simplify(v)==0)
zero('pprime_over_p',s.diff(p,x)/p-B)
zero('p_b_equals_w',p*b-w)
ode=s.diff(D,x,2)+B*s.diff(D,x)-b*A*D
zero('integrating_factor_equivalence',s.diff(p*s.diff(D,x),x)-A*w*D-p*ode)
r=(s.diff(Y,x)+B*Y)/b
ainverse=s.diff(r,x)/Y
expected=(s.diff(Y,x,2)+(B-s.diff(b,x)/b)*s.diff(Y,x)+(s.diff(B,x)-B*s.diff(b,x)/b)*Y)/(b*Y)
zero('derivative_shape_inverse',ainverse-expected)
# Exact EdS growing mode, arbitrary derivative normalization N.
toyF=s.exp(-3*x);toyD=N*s.exp(x);toyY=s.diff(toyD,x);toyp=s.exp(x/2);toyw=s.Rational(3,2)*s.exp(x/2)
I0=3*(s.exp(x/2)-1);I1=N*(s.exp(3*x/2)-3*s.exp(x/2)+2);delta=N*(s.exp(3*x/2)-1)
zero('toy_I0_derivative',s.diff(I0,x)-toyw)
zero('toy_I1_derivative',s.diff(I1,x)-toyw*(toyD-N))
zero('toy_integrated_relation',delta-N*I0-I1)
pts=[s.log(2),s.log(4)];M=s.Matrix([[I0.subs(x,z),I1.subs(x,z)] for z in pts]);v=s.Matrix([delta.subs(x,z) for z in pts]);sol=M.inv()*v
zero('toy_inferred_matter_A',sol[1]-1)
zero('toy_inferred_initial_product_C0',sol[0]-N)
det=s.simplify(M.det());zero('toy_rank_determinant',det-N*(15*s.sqrt(2)-18))
checks['toy_rank_positive']=bool((15*s.sqrt(2)-18).is_positive)
# Coordinator's fixed-F example has immediate D'' separation .075 at a=1,D=1.
zero('coordinator_local_curvature',s.Rational(3,2)*(s.Rational(1,4)-s.Rational(1,5))-s.Rational(3,40))
assert all(checks.values()),checks
out=pathlib.Path(sys.argv[1]);out.mkdir(exist_ok=True);(out/'results.json').write_text(json.dumps({'check_count':len(checks),'all_checks_pass':all(checks.values()),'checks':checks,'toy_matter_A':str(s.simplify(sol[1])),'toy_C0':str(s.simplify(sol[0])),'toy_determinant':str(det),'scope':'Symbolic identities and one exact toy; no observational covariance or cosmic fit'},indent=2));print(len(checks),'checks passed')
