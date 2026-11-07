"""Bounded conditional condensate checks; parameters are fixtures, not fits."""
import argparse, json, math, pathlib, subprocess
import numpy as np
import sympy as sp
from scipy.integrate import quad
p=argparse.ArgumentParser(); p.add_argument('--out',required=True); p.add_argument('--mutate',action='store_true'); args=p.parse_args()
out=pathlib.Path(args.out); out.parent.mkdir(parents=True,exist_ok=True)
checks=[]
def check(name, ok, detail=None):
    checks.append({'name':name,'passed':bool(ok),'detail':detail})
def exact(name, expression):
    check(name, sp.simplify(sp.trigsimp(expression)) == 0)
x=sp.symbols('x', positive=True)
f=sp.sin(x)/x
I=(1-x*sp.cot(x))/x**2
h=x*x+x*sp.sin(x)*sp.cos(x)-2*sp.sin(x)**2
exact('Lane-Emden differential equation',sp.diff(f,x,2)+2*sp.diff(f,x)/x+f)
exact('inventory log derivative',sp.diff(sp.log(x*(1-x*sp.cot(x))),x)*x-(3+x*sp.diff(I,x)/I))
exact('mass primitive',sp.diff(sp.sin(x)-x*sp.cos(x),x)-x*sp.sin(x))
exact('concentration derivative',sp.diff(I,x)-h/(x**3*sp.sin(x)**2))
exact('positive second derivative of h',sp.diff(h,x,2)-4*sp.sin(x)*(sp.sin(x)-x*sp.cos(x)))
check('h zero initial value',sp.limit(h,x,0)==0)
check('h derivative zero initial value',sp.limit(sp.diff(h,x),x,0)==0)
exact('positive derivative of inner factor',sp.diff(sp.sin(x)-x*sp.cos(x),x)-x*sp.sin(x))
B,S,R=sp.symbols('B S R',positive=True)
exact('edge density logarithmic slope',sp.diff(sp.log(sp.sqrt(B+2*S/R)),R)*R+S/(B*R+2*S))
A,D,C=sp.symbols('A D C',positive=True)
energy=A/R**3-D/R+C*R**3+S*R**2
Dstationary=3*A/R**2-3*C*R**4-2*S*R**3
exact('homologous curvature',sp.diff(energy,R,2).subs(D,Dstationary)-(6*A/R**5+12*C*R+6*S))
# Unit fixtures G=m=a=B=1, g=4*pi. No normalization parameter is fitted.
g=4*math.pi
rows=[]
def family(radius,sigma):
    pressure=1+(1 if args.mutate else 2)*sigma/radius
    ne=math.sqrt(2*pressure/g)
    nc=ne*radius/math.sin(radius)
    mass=4*math.pi*nc*(math.sin(radius)-radius*math.cos(radius))
    return ne,nc,mass
for sigma in [0.,0.1,10.]:
    for radius in [0.05,0.2,0.5,1.,1.5,2.,2.5,2.9,3.1]:
        ne,nc,N=family(radius,sigma)
        numerical=quad(lambda r:4*math.pi*nc*np.sinc(r/math.pi)*r*r,0,radius,epsabs=1e-10,epsrel=1e-11)[0]
        boundary=g*ne**2/2-(1+2*sigma/radius)
        concentration=(1-radius/math.tan(radius))/radius**2
        hval=radius**2+radius*math.sin(radius)*math.cos(radius)-2*math.sin(radius)**2
        j=hval/(radius**2*math.sin(radius)**2*concentration)
        t=2*sigma/(radius+2*sigma)
        L=3-t/2+j
        b=2-2/L
        eps=1e-5
        nplus=family(radius*math.exp(eps),sigma)[2]
        nminus=family(radius*math.exp(-eps),sigma)[2]
        fd_full=(math.log(nplus)-math.log(nminus))/(2*eps)
        np_half=family(radius*math.exp(eps/2),sigma)[2]
        nm_half=family(radius*math.exp(-eps/2),sigma)[2]
        fd_half=(math.log(np_half)-math.log(nm_half))/eps
        fd=(4*fd_half-fd_full)/3
        label=f'R={radius},Sigma={sigma}'
        check('quadrature '+label,abs(numerical/N-1)<1e-7)
        check('Laplace force '+label,abs(boundary)<1e-7,boundary)
        check('logarithmic derivative '+label,abs(fd/L-1)<1e-7, {'full_relative_error':fd_full/L-1,'half_relative_error':fd_half/L-1,'richardson_relative_error':fd/L-1})
        check('mass slope bound '+label,b>=1.2-1e-7,b)
        vc4=(N/radius)**2
        rows.append({'R':radius,'Sigma':sigma,'N':N,'edge_density':ne,
                     'L':L,'speed_fourth_power_exponent':b,'vc4_over_N':vc4/N})
source='action_scale_investigation_2026_11_05/joint_phase/lean/CoupledCondensate.lean'
run=subprocess.run(['lean',source],capture_output=True,text=True,timeout=40)
(out.parent/'lean-output.txt').write_text(run.stdout+run.stderr)
axioms=[line for line in run.stdout.splitlines() if 'depends on axioms' in line]
check('Lean exit zero',run.returncode==0,run.returncode)
check('eight Lean axiom reports',len(axioms)==8,len(axioms))
check('no sorryAx', 'sorryAx' not in run.stdout)
result={'mutation':args.mutate,'checks':checks,'rows':rows,'lean_axioms':axioms,
        'passed':sum(c['passed'] for c in checks),'total':len(checks)}
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':result['passed'],'total':result['total'],
                  'failures':[c for c in checks if not c['passed']]},indent=2))
raise SystemExit(int(result['passed']!=result['total']))
