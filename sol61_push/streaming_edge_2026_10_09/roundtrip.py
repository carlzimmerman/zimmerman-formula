"""Independent density expression and forward Abel reconstruction check."""
import argparse
import json
import math
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq

p=argparse.ArgumentParser()
p.add_argument('--output',required=True)
args=p.parse_args()
r,b,R=sp.symbols('r b R',positive=True)
u=r+b
d=sp.exp(1/u)-1
# Explicit density formula independently differentiated by the reviewer.
rho=b/(2*sp.pi*r*u**3*d)+sp.exp(1/u)/(4*sp.pi*u**4*d**2)
g=1/(u**2*(1-sp.exp(-1/u)))
h=(1-r**2/R**2)*rho
hp=-sp.diff(h,r)/g
hpp=-sp.diff(hp,r)/g
calc=sp.lambdify((r,b,R),[h,hp,hpp],modules='numpy',cse=True)
norm=1/(math.sqrt(8)*math.pi**2)
records=[]
for bv in [.3,1.,3.]:
 for q in [.5364,5.364]:
  rv=brentq(lambda x:x*x/(x+bv)**2/math.expm1(1/(x+bv))-q,1e-8,100)
  ledge=math.log(math.expm1(1/(rv+bv)))
  boundary=float(calc(rv,bv,rv)[1])
  def rad(psi): return 1/float(np.logaddexp(0,psi+ledge))-bv
  def f(Q):
   term=quad(lambda z:float(calc(rad(Q*(1-z*z)),bv,rv)[2]),0,1,epsabs=1e-10,epsrel=2e-9,limit=150)[0]
   return norm*(boundary/math.sqrt(Q)+2*math.sqrt(Q)*term)
  for frac in [.1,.5,.9]:
   rr=frac*rv
   psi=math.log(math.expm1(1/(rr+bv)))-ledge
   expected=float(calc(rr,bv,rv)[0])
   recon=[]
   for n in [32,64]:
    nodes,weights=np.polynomial.legendre.leggauss(n)
    theta=(nodes+1)*math.pi/4
    vals=[2*psi**1.5*f(psi*math.sin(a)**2)*math.sin(a)*math.cos(a)**2 for a in theta]
    got=4*math.pi*math.sqrt(2)*math.pi/4*float(np.dot(weights,vals))
    recon.append(got)
   error=abs(recon[1]/expected-1)
   convergence=abs(recon[1]-recon[0])/expected
   records.append({'b':bv,'q':q,'r_over_R':frac,'target_h':expected,
                   'reconstructed_h_32_64':recon,'relative_error':error,
                   'refinement_difference':convergence,'pass':error<1e-6 and convergence<1e-6})
out=Path(args.output)
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps({'records':records,'limitations':'Shared Abel formula and SymPy; independent density expression and forward integration, not fully independent software.'},indent=2)+'\n')
print(json.dumps({'passed':sum(r['pass'] for r in records),'total':len(records),
                  'max_relative_error':max(r['relative_error'] for r in records),
                  'max_refinement_difference':max(r['refinement_difference'] for r in records)}))
raise SystemExit(0 if all(r['pass'] for r in records) else 1)
