"""Exact finite Fourier clock kernel and exposed-support witnesses."""
import argparse,json,sys
from pathlib import Path
import sympy as s
from itertools import product
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['omit_shift','average_only','conjugate_square']);args=ap.parse_args();rows=[]
def eq(n,e):
 e=s.expand(e);rows.append(dict(name=n,passed=e==0,residual=str(e)))
def ck(n,b):rows.append(dict(name=n,passed=bool(b)))
def norm(k):return sum(q*q for q in k)
def dot(k,l):return sum(x*y for x,y in zip(k,l))
def add(k,l):return tuple(x+y for x,y in zip(k,l))
def neg(k):return tuple(-x for x in k)
def accum(o,k,c):o[k]=s.expand(o.get(k,0)+c)
def mul(A,B):
 out={}
 for k,c in A.items():
  for l,d in B.items():accum(out,add(k,l),c*d)
 return {k:c for k,c in out.items() if c!=0}
def grad(A,i):return {k:s.I*k[i]*v for k,v in A.items() if k[i]!=0}
def lap(A):return {k:-norm(k)*v for k,v in A.items()}
def invlap(A):return {k:v/s.Integer(norm(k)) for k,v in A.items()}
def raw_source(A):
 # E/(2KaH), independently applying divergence to -nu gradnu + 2Delta nu grad inv(-Delta)nu.
 out={};iv=invlap(A);la=lap(A)
 for i in range(3):
  cur={}
  for k,c in mul(A,grad(A,i)).items():accum(cur,k,-c)
  for k,c in mul(la,grad(iv,i)).items():accum(cur,k,2*c)
  for k,c in grad(cur,i).items():accum(out,k,c)
 return {k:c for k,c in out.items() if c!=0}
def kernel_source(A,omit=False):
 out={}
 for k,c in A.items():
  for l,d in A.items():
   p=add(k,l);factor=dot(p,l)*(1+(0 if omit else 2*s.Rational(norm(k),norm(l))))
   accum(out,p,factor*c*d)
 return {k:c for k,c in out.items() if c!=0}
def real_mode(A,k,c):A[k]=c;A[neg(k)]=s.conjugate(c)
examples=[]
A={};real_mode(A,(1,0,0),s.Rational(1,2));examples.append(('cos',A))
A={};real_mode(A,(1,0,0),-s.I/2);examples.append(('sin',A))
A={};real_mode(A,(1,0,0),s.Rational(1,2));real_mode(A,(0,2,0),s.Rational(1,6));examples.append(('two_shell',A))
A={};real_mode(A,(1,0,0),s.Rational(2,3));real_mode(A,(0,2,0),s.Rational(1,7));real_mode(A,(1,1,1),-s.I*s.Rational(3,10));examples.append(('three_shell_complex_phase',A))
A={};real_mode(A,(2,1,-1),s.Rational(1,4)+s.I/9);real_mode(A,(-1,2,1),s.Rational(2,11)-s.I/7);real_mode(A,(0,1,0),s.Rational(3,8));examples.append(('equal_maxnorm_and_low_shell',A))
for name,A in examples:
 ck(name+'_actual_real_field',all(A[neg(k)]==s.conjugate(c) for k,c in A.items()))
 ck(name+'_zero_mean_support',(0,0,0) not in A)
 R=raw_source(A);F=kernel_source(A)
 for p in set(R)|set(F):eq(name+'_raw_kernel_'+str(p),R.get(p,0)-F.get(p,0))
 eq(name+'_zero_integrated_row',F.get((0,0,0),0))
 star=max(A,key=lambda k:(norm(k),k));p=add(star,star)
 ck(name+'_constructive_exposed_max',all(dot(star,star)>dot(star,k) for k in A if k!=star))
 pairs=[(k,l) for k in A for l in A if add(k,l)==p]
 ck(name+'_unique_extreme_pair',pairs==[(star,star)])
 candidate=F.get(p,0)
 if args.control=='omit_shift':candidate=kernel_source(A,True).get(p,0)
 if args.control=='average_only':candidate=F.get((0,0,0),0)
 if args.control=='conjugate_square':candidate=6*norm(star)*A[star]*s.conjugate(A[star])
 eq(name+'_actual_extreme_coefficient',candidate-6*norm(star)*A[star]**2)
 ck(name+'_extreme_residual_nonzero',F[p]!=0)
# Factor dictionary E=2KaH*kernel, puredecay nu=f/a.
K,H,a=s.symbols('K H a',positive=True);kk=s.symbols('k_squared',positive=True);v=s.symbols('nu_k');ff=s.symbols('f_k')
eq('actual_dimensional_extreme_factor',2*K*a*H*6*kk*v*v-12*K*a*H*kk*v*v)
eq('actual_decay_time_factor',(12*K*a*H*kk*v*v).subs(v,ff/a)-12*K*H*kk*ff*ff/a)
# Same-shell parent identity is a control of the new nonlocal current kernel.
for k in [(1,0,0),(0,1,0),(0,0,-1)]:
 for l in [(1,0,0),(0,-1,0),(0,0,1)]:
  p=add(k,l);sym=(dot(p,l)*(1+2*s.Rational(norm(k),norm(l)))+dot(p,k)*(1+2*s.Rational(norm(l),norm(k))))/2
  eq('parent_eigenshell_symkernel_'+str((k,l)),sym-s.Rational(3,2)*norm(p))
# Exact integer grid verifies witness-selection algorithm despite repeated maxnorms.
grid=[k for k in product(range(-2,3),repeat=3) if k!=(0,0,0)];star=max(grid,key=lambda k:(norm(k),k))
ck('bounded_grid_exposed_support',all(dot(star,star)>dot(star,k) for k in grid if k!=star))
ck('bounded_grid_extreme_pair_unique',[(k,l) for k in grid for l in grid if add(k,l)==add(star,star)]==[(star,star)])
# Algebraic strict exposure identity used by the all-finite proof.
u2,v2,uv=s.symbols('u2 v2 uv',real=True)
eq('strict_exposure_distance_identity',u2-uv-(u2-v2+(u2+v2-2*uv))/2)
out=dict(passed=sum(r['passed'] for r in rows),total=len(rows),checks=rows,control=args.control,scope='finite deterministic exact n3 real scalar Fourier fixtures; uniform theorem analytic; no infinite Fourier/fullvacuumperturbation classification')
p=Path(args.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(passed=out['passed'],total=out['total'],failed=[r['name'] for r in rows if not r['passed']])));sys.exit(not all(r['passed'] for r in rows))
