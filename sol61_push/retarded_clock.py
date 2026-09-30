import argparse
import cmath
import json
import math
import sympy as s
from scipy.integrate import quad
from scipy.optimize import root

checks=[]
def check(name,ok): checks.append({'name':name,'passed':bool(ok)})
x,r=s.symbols('x r',positive=True)
check('Feynman parameter integral',s.integrate(1/s.sqrt(x*(1-x)),(x,0,1))==s.pi)
Jreal=s.pi*(1-r*r)/4
Jimag=-(r-(1-r*r)*s.atanh(r))/2
check('small-frequency imaginary cubic',s.expand(s.series(Jimag,r,0,6).removeO()).coeff(r,3)==-s.Rational(1,3))
check('small-frequency imaginary fifth coefficient',s.expand(s.series(Jimag,r,0,6).removeO()).coeff(r,5)==-s.Rational(1,15))
check('static angular coefficient',Jreal.subs(r,0)==s.pi/4)
def J_real_boundary(value):
    if value<1:
        return math.pi*(1-value*value)/4-0.5j*(value-(1-value*value)*math.atanh(value))
    if value==1: return -0.5j
    return -0.5j*(value+(value*value-1)*math.atanh(1/value))
def angular_boundary(value):
    if value<1:
        c=math.sqrt(1-value*value)
        real=quad(lambda u:math.sqrt(max(0,c*c-u*u)),0,c,epsabs=1e-12)[0]
        imag=-quad(lambda u:math.sqrt(max(0,u*u-c*c)),c,1,epsabs=1e-12)[0]
        return complex(real,imag)
    return -1j*quad(lambda u:math.sqrt(value*value-1+u*u),0,1,epsabs=1e-12)[0]
angular_rows=[]
for value in (0.01,0.2,0.8,1.,1.2):
    numerical=angular_boundary(value)
    expected=J_real_boundary(value)
    error=abs(numerical-expected)
    check('independent angular integral r='+str(value),error<1e-9)
    check('continuum absorption at every positive frequency r='+str(value),numerical.imag<0)
    angular_rows.append({'r':value,'J_real':expected.real,'J_imag':expected.imag,'absolute_quadrature_error':error})
def J_continued(w):
    return math.pi*(1-w*w)/4-0.5j*(w-(1-w*w)*cmath.atanh(w))
for real,imag in ((0.2,0.1),(1.2,0.1),(-0.5,0.2),(0.,0.4)):
    w=complex(real,imag)
    numerical=complex(quad(lambda u:cmath.sqrt(1-u*u-w*w).real,0,1,epsabs=1e-12)[0],quad(lambda u:cmath.sqrt(1-u*u-w*w).imag,0,1,epsabs=1e-12)[0])
    check('upper-half-plane angular continuation '+str(w),abs(numerical-J_continued(w))<1e-9)
    F=w*w-0.5*numerical
    check('upper-half-plane sign exclusion '+str(w),(F.imag*real>0) if real else (abs(F.imag)<1e-12 and F.real<0))

resonance_rows=[]
for t in (1e-3,1e-2,0.1,0.3):
    initial=math.sqrt(math.pi*t/(4+math.pi*t))
    def equation(pair):
        w=complex(*pair)
        f=w*w-t*J_continued(w)
        return [f.real,f.imag]
    solution=root(equation,[initial,-math.pi*t*t/24],tol=1e-11)
    pole=complex(*solution.x)
    residual=abs(pole*pole-t*J_continued(pole))
    check('damped resonance '+str(t),solution.success and residual<1e-10 and 0<pole.real<1 and pole.imag<0)
    if t==1e-3:
        check('leading three-halves frequency',abs(pole.real/math.sqrt(math.pi*t/4)-1)<0.005)
        check('leading damping coefficient',abs((-pole.imag)/(math.pi*t*t/24)-1)<0.005)
    resonance_rows.append({'t':t,'r_pole_real':pole.real,'r_pole_imag':pole.imag,'root_residual':residual,'width_over_frequency':-pole.imag/pole.real})

nu,y,v,G,q0,a0=s.symbols('nu y v G q0 a0',positive=True)
zeta=s.pi*G*nu*q0*y*y/(2*v*v)
check('loop coefficient tied to bare acceleration scale',s.simplify(zeta.subs(q0,v*v/(2*G*nu*y**3*a0))-s.pi/(4*y*a0))==0)
parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
args=parser.parse_args()
result={'passed':all(c['passed'] for c in checks),'checks':checks,'angular_integrals':angular_rows,'continued_resonances':resonance_rows}
with open(args.output,'w') as f: json.dump(result,f,indent=2)
print(str(sum(c['passed'] for c in checks))+'/'+str(len(checks))+' checks passed')
raise SystemExit(0 if result['passed'] else 1)
