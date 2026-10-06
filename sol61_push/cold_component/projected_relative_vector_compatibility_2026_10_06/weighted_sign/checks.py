"""Exact Fourier-coefficient counterexample; no quadrature or cutoff approximation."""
from fractions import Fraction as Q
from pathlib import Path
import json,sys

def add(*fs):
 out={}
 for f in fs:
  for k,v in f.items():out[k]=out.get(k,Q(0))+v
 return {k:v for k,v in out.items() if v}
def scale(f,a):return {k:a*v for k,v in f.items() if a*v}
def mul(f,g):
 out={}
 for k,v in f.items():
  for l,w in g.items():out[k+l]=out.get(k+l,Q(0))+v*w
 return {k:v for k,v in out.items() if v}
def cos(n):return {n:Q(1,2),-n:Q(1,2)}
def lap(f):return {k:-k*k*v for k,v in f.items() if k}
def inverse(f):return {k:v/(k*k) for k,v in f.items() if k}
def gradprod(f,g):
 out={}
 for k,v in f.items():
  for l,w in g.items():out[k+l]=out.get(k+l,Q(0))-k*l*v*w
 return {k:v for k,v in out.items() if v}
def mean(f):return f.get(0,Q(0))
def witness(N=40):
 return add(cos(1),scale(mul(add({0:Q(1)},scale(cos(1),Q(1,2))),add(cos(N),scale(cos(2*N),-1))),Q(1,100)))
def evaluate(f,transport=2):
 w=lap(f);u=inverse(f)
 # div(f grad f - transport*w grad u), using lap u=-f.
 R=add(gradprod(f,f),mul(f,w),scale(add(gradprod(w,u),scale(mul(w,f),-1)),-transport))
 I=mean(mul(mul(w,w),R))
 J=mean(add(mul(mul(w,w),gradprod(f,f)),scale(mul(f,mul(w,mul(w,w))),Q(7,3))))
 return I,J,R

def main():
 out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
 ctl=sys.argv[2] if len(sys.argv)>2 else 'none';checks={}
 def check(n,b):checks[n]=bool(b);print(('PASS ' if b else 'FAIL ')+n)
 f=witness();I,J,R=evaluate(f,1 if ctl=='transport' else 2)
 check('real zero mean source',mean(f)==0 and all(v==f.get(-k) for k,v in f.items()))
 check('inverse Poisson exact',lap(inverse(f))==scale(f,-1))
 check('weighted integration identity',I==J)
 check('explicit positive weighted witness',I>0)
 check('pointwise periodic divergence mean zero',mean(R)==0)
 low,lowJ,_=evaluate(cos(1));check('eigenfunction negative control',low==lowJ==Q(-3,4))
 check('not universal positive sign',low<0)
 if ctl=='negative_claim':check('candidate universal nonpositive integral',I<=0)
 if ctl=='mean_only':check('candidate zero mean residual guarantees compatibility',I==0)
 # Algebraic Fourier products finite-support, exact mean is zero coefficient.
 data={'checks':checks,'counterexample':'cos(x)+(1+cos(x)/2)*(cos(40*x)-cos(80*x))/100','I_normalized':str(I),'I_float_display':float(I),'identity_rhs':str(J),'negative_eigenvalue':str(low),'f_max_frequency':max(abs(k) for k in f),'R_max_frequency':max(abs(k) for k in R),'arithmetic':'fractions.Fraction exact Q; integral/(2*pi) is zero Fourier coefficient','scope':'one-dimensional finite polynomial, embedded on flat three-torus; no vector existence inference'}
 (out/'results.json').write_text(json.dumps(data,indent=2)+'\n')
 return 0 if all(checks.values()) else 1
if __name__=='__main__':sys.exit(main())
