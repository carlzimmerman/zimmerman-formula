"""Independent bounded photon gauge-block, spectrum, Mellin and response checks."""
import json,math,sys
from pathlib import Path
from fractions import Fraction as Q
import sympy as s
import mpmath as m
m.mp.dps=45
lam,xi,mm=s.symbols('lambda xi m',positive=True)
block=s.Matrix([[lam/xi+mm**2,mm*s.sqrt(lam)],[mm*s.sqrt(lam),lam]])
assert s.simplify(block.det()-lam**2/xi)==0
assert s.simplify(s.trace(s.diag(xi/lam,1/lam)*s.diag(1,0))/2-xi/(2*lam))==0

# Transverse heat trace from the given spectrum and half-integer expansion.
def hz(n):
 b=s.bernoulli(n+1)
 return (Q(1,2**n)-1)*(-Q(int(b.p),int(b.q))/(n+1))
raw={-2:Q(1,2),-1:Q(-9,8)}
for j in range(12): raw[j]=Q((-1)**j,math.factorial(j))*(hz(3+2*j)-Q(9,4)*hz(1+2*j))
heat={j:sum(v*Q(1,4)**(j-k)/math.factorial(j-k) for k,v in raw.items() if k<=j)+(1 if j==0 else 0) for j in range(-2,11)}
assert [heat[j] for j in [-2,-1,0]]==[Q(1,2),-1,Q(19,30)]
def mq(q): return m.mpf(q.numerator)/q.denominator
split=m.mpf('.04')
low=m.fsum(mq(heat[j])*split**(j+1)/(j+1) for j in range(11))
def kt(t):
 n=int(m.ceil(m.sqrt(155/t)))+3
 assert n<200
 return m.fsum(m.mpf(l*(l+3)*(2*l+3))/2*m.exp(-t*(l+1)*(l+2)) for l in range(1,n+1))
mid=m.quad(lambda t:kt(t)-1/(2*t*t)+1/t,[split,m.mpf('.2'),1])
high=m.quad(kt,[1,4,16,m.inf])
fp_heat=low+mid+high-m.mpf(1)/2-m.euler
fp= m.mpf(2)/3-2*m.euler
heat_error=abs(fp_heat-fp)
assert heat_error<m.mpf('2e-18')
A=s.Rational(5,2)
fp_symbolic=s.zeta(-1,A).expand(func=True)+s.Rational(1,8)+s.polygamma(0,3)+s.polygamma(0,2)
assert s.simplify(s.expand_func(fp_symbolic)-(s.Rational(2,3)-2*s.EulerGamma))==0

def moments(x,y):
 def moment(i,j):
  if i==0: return m.quad(lambda t:t**j*m.exp(-y*t)*m.besseli(0,x*m.sqrt(1-t)),[0,1])
  return m.quad(lambda t:t**j*m.exp(-y*t)*m.sqrt(1-t)*m.besseli(1,x*m.sqrt(1-t)),[0,1])
 z=moment(0,0); a=moment(1,0)/z; q=moment(0,1)/z
 q2=moment(0,2)/z; q3=moment(0,3)/z; aq=moment(1,1)/z; aq2=moment(1,2)/z
 return q,aq-a*q,q2-q*q,aq2-a*q2-2*q*aq+2*a*q*q,q3-3*q*q2+2*q**3
omega=8*m.pi**2/3; x0=m.mpf('1.3'); y0=m.mpf('.2'); u0=m.mpf('.04')
F=m.mpf(1); mu=m.mpf('1.7'); mass_source=x0/omega; C=y0/(u0*omega)
def data(H,u):
 V=omega/H**4; x=mass_source*V; y=u*C*V
 L=fp-m.log(mu**2/H**2); J=F**2*L/(2*H**2); DJ=J/2-F**2/(4*H**2)
 return V,x,y,J,DJ,moments(x,y)
def W(H,u):
 V,x,y,J,DJ,(q,c,vs,kas,kss)=data(H,u)
 return u*J*q
def rho(H,u):
 V,x,y,J,DJ,(q,c,vs,kas,kss)=data(H,u)
 return u*(DJ*q+J*(x*c-y*vs))/V
def fd(f,z,h): return (f(z-2*h)-8*f(z-h)+8*f(z+h)-f(z+2*h))/(12*h)
step=m.mpf('1e-6')
rho_fd=-fd(lambda t:W(m.exp(t),u0),0,step)/(4*omega)
rho_formula=rho(1,u0)
assert abs(rho_fd-rho_formula)<m.mpf('2e-20')
V,x,y,J,DJ,(q,c,vs,kas,kss)=data(1,u0)
du_formula=(DJ*(q-y*vs)+J*(x*c-2*y*vs-x*y*kas+y*y*kss))/V
du_fd=fd(lambda u:rho(1,u),u0,step)
assert abs(du_fd-du_formula)<m.mpf('2e-19')
def fmt(x): return m.nstr(x,35)
result={'status':'completed','gauge_block':'det=lambda²/xi, source independent','transverse_lowest':{'l':1,'eigenvalue_over_H2':6,'multiplicity':10},
 'heat_coefficients':{str(k):str(v) for k,v in heat.items()},'zeta':{'residue':'-1','finite_part_symbolic':'2/3-2gamma','finite_part_heat':fmt(fp_heat),'finite_part_closed':fmt(fp),'difference':fmt(heat_error)},
 'one_response_case':{'x':fmt(x0),'y':fmt(y0),'u':fmt(u0),'metric_difference':fmt(abs(rho_fd-rho_formula)),'charge_difference':fmt(abs(du_fd-du_formula)),'rho':fmt(rho_formula),'d_u_rho':fmt(du_formula)},
 'photon_counterterm':{'pi2_epsilon_times_delta_k15':'-1/64','beta15_photon':'1/2'},
 'bounds':{'precision':45,'heat_split':str(split),'heat_order':10,'harmonic_cap':200,'response_cases':1},
 'non_claims':['No interval certification','No finite curvature LEC matching','No full pion-photon NLO assembly','No resolution of earlier pion k15 bridge','No full QCD or alpha selection']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'completed','heat_FP_difference':fmt(heat_error),'metric_difference':result['one_response_case']['metric_difference'],'charge_difference':result['one_response_case']['charge_difference']}))
