"""Bounded independent checks; never imports or writes author artifacts."""
import json
import math
import sys
from fractions import Fraction as Q
from pathlib import Path
import mpmath as m
import sympy as s

m.mp.dps=55
def out(v): return m.nstr(v,38)
def mq(v): return m.mpf(v.numerator)/v.denominator

# Half-integer Euler--Maclaurin coefficients, using exact Bernoulli numbers.
def zetahalf_negative(n):
    b=s.bernoulli(n+1)
    return (Q(1,2**n)-1)*(-Q(int(b.p),int(b.q))/(n+1))
unshift={-2:Q(1,6),-1:Q(-1,24)}
for j in range(13):
    unshift[j]=Q((-1)**j,math.factorial(j))*(zetahalf_negative(3+2*j)/3-zetahalf_negative(1+2*j)/12)
heat={j:sum(v*Q(9,4)**(j-p)/math.factorial(j-p) for p,v in unshift.items() if p<=j) for j in range(-2,11)}
assert [heat[j] for j in range(-2,4)]==[Q(1,6),Q(1,3),Q(29,90),Q(37,189),Q(149,1890),Q(179,10395)]

def a(j,xi):
    return m.fsum(mq(heat[p])*(-12*xi)**(j-p)/m.factorial(j-p) for p in range(-2,j+1))
def I(z,xi=0):
    z,xi=m.mpf(z),m.mpf(xi)
    q=z+12*xi
    assert z>0 and q>0
    v=m.sqrt(m.mpf('2.25')-q)
    return m.re((q-2)*(m.digamma(m.mpf('1.5')+v)+m.digamma(m.mpf('1.5')-v)-m.log(z))/6+m.mpf(2)/9-2*xi-a(0,xi)/z)
def B(t,xi):
    # Direct original l-spectrum; no use of rational resolvent or target code.
    n=int(m.ceil(m.sqrt(165/t)))+3
    assert n<200
    return m.exp(-12*xi*t)*m.fsum(m.mpf((l+1)*(l+2)*(2*l+3))/6*m.exp(-t*l*(l+3)) for l in range(n+1))-a(-2,xi)/t**2-a(-1,xi)/t-a(0,xi)
def integral(z,xi=0,action=False):
    z,xi=m.mpf(z),m.mpf(xi)
    split=m.mpf('.04')
    power=0 if action else 1
    low=m.fsum(a(j,xi)*m.gammainc(j+power,0,z*split)/z**(j+power) for j in range(1,11))
    def f(t): return m.exp(-z*t)*B(t,xi)/(t if action else 1)
    high=m.quad(f,[split,m.mpf('.2'),1,5,20,m.inf])
    return -(low+high)/2 if action else low+high

cases=[]
for z,xi in [('1','0'),('2','0'),('2.25','0'),('0.4','-0.02'),('7.3',str(m.mpf(1)/6))]:
    numeric,closed=integral(z,xi),I(z,xi)
    err=abs(numeric-closed)
    assert err<m.mpf('2e-18')
    cases.append({'z':z,'xi':xi,'direct_heat':out(numeric),'closed':out(closed),'difference':out(err)})
assert abs(I(2)-m.mpf(11)/180)<m.mpf('1e-50')

# Independently sum the positive S series, retaining an explicit conservative tail.
brackets=[]
for z,xi in [('2.25','0'),('0.4','-0.02'),('7.3',str(m.mpf(1)/6))]:
    z,xi=m.mpf(z),m.mpf(xi); q=z+12*xi; N=4000
    partial=m.fsum(m.mpf(2*l+3)/(6*(l+1)*(l+2)*(l*(l+3)+q)) for l in range(N))
    # For l>=N, term <= (2l+3)/(6l^4).
    tail=m.mpf(1)/(6*(N-1)**2)+m.mpf(1)/(6*(N-1)**3)
    base=(q-2)*(1-2*m.euler-m.log(z))/6+m.mpf(2)/9-2*xi-a(0,xi)/z
    lo=base+(q-2)**2*partial; hi=lo+(q-2)**2*tail
    assert lo<=I(z,xi)<=hi
    brackets.append({'z':out(z),'xi':out(xi),'lower':out(lo),'upper':out(hi),'closed':out(I(z,xi)),'terms':N})

# Direct fixed-M metric difference of the action, at an untested negative xi.
z=m.mpf('3.7'); xi=m.mpf('-.02'); h=m.mpf('0.00001')
minus_dw=-(integral(z*m.exp(-2*h),xi,True)-integral(z*m.exp(2*h),xi,True))/(2*h)
metric_expected=z*I(z,xi)
assert abs(minus_dw-metric_expected)<m.mpf('2e-10')

# Two real charged modes, simultaneous mass and xi insertion.
b=m.mpf('.3'); k=m.mpf('.007'); H2=1/z; du=m.mpf('.000001')
def charged_rho(u):
    zz=z*(1+b*u); xx=-2*k*u
    return 3*H2**2/(16*m.pi**2)*zz*integral(zz,xx)
fd=(charged_rho(du)-charged_rho(-du))/(2*du)
target=3*H2**2/(16*m.pi**2)*(b*z*m.diff(lambda v:v*I(v),z)-2*k*m.diff(lambda v:z*I(z,v),0))
assert abs(fd-target)<m.mpf('5e-15')

asym=[]
for zz in [64,256,1024]:
    for xx in [m.mpf(0),m.mpf('.02')]:
        asym.append({'z':zz,'xi':out(xx),'z2I':out(zz**2*I(zz,xx)),'a3':out(a(1,xx))})
zm=m.mpf('1e-12'); zero=zm*I(zm)
assert abs(zero-m.mpf(61)/90)<m.mpf('1e-10')

# Exact group/RG/free-anomaly conversions independent of target implementation.
Nv=8; CA=3; nf=3; TF=Q(1,2); S=3*sum(q*q for q in [Q(2,3),Q(-1,3),Q(-1,3)])
beta0=(11*CA-4*nf*TF)/3
afree=Q(62*9+11*9,360)
assert S==2 and beta0==9 and afree==Q(73,40)
assert abs(a(0,m.mpf(1)/6)+m.mpf(1)/90)<m.mpf('1e-53')
result={'status':'completed','heat_coefficients':{str(j):str(v) for j,v in heat.items()},
        'heat_cases':cases,'spectral_brackets':brackets,
        'metric':{'z':out(z),'xi':out(xi),'minus_dlogH_W':out(minus_dw),'zI':out(metric_expected),'difference':out(abs(minus_dw-metric_expected))},
        'charged_mass_and_xi':{'b':out(b),'k15':out(k),'difference':out(abs(fd-target)),'heat_difference':out(fd),'digamma_derivative':out(target)},
        'asymptotic_cases':asym,'minimal_small_z_Psi':out(zero),
        'UV':{'S':str(S),'beta0':str(beta0),'a':str(afree),'rho_over_H4':'219/(320*pi^2)+(u-27*g^2)/(64*pi^4)','d_alpha_rho_over_H4':'1/(16*pi^3)'},
        'non_claims':['No interval certification','No new two-loop graph integration','No full QCD or alpha selection','No physical chiral or massless Gaussian limit']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'completed','heat_cases':len(cases),'spectral_brackets':len(brackets),'max_heat_difference':out(max(m.mpf(c['difference']) for c in cases)),'metric_difference':result['metric']['difference'],'charge_difference':result['charged_mass_and_xi']['difference']}))
