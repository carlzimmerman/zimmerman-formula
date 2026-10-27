import json,sys,math
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.integrate import quad
from numpy.polynomial.legendre import leggauss
prior=json.loads(Path('sol61_push/optical_mass_branch_2026_10_14/run/results.json').read_text())
hc=1.973269804e-7; hb=6.582119569e-16; c=299792458.; ej=1.602176634e-19
MR=2.; kph=1.; g=1e-20; intensity=1e12; Lt=.001/hc; w0=2*Lt
zR=kph*w0*w0/2; k=prior['scalar_momentum_eV']; F=g*(intensity/c)/(ej/hc**3)/math.sqrt(2*MR)
checks=[]
def ck(name,error,tol):
    assert error<=tol,(name,error,tol)
    checks.append(dict(name=name,error=float(error),tolerance=tol))
x,y,s=sp.symbols('x y s',real=True)
U=sp.exp(-(x*x+y*y)/(1+sp.I*s))/(1+sp.I*s)
res=sp.simplify(4*sp.I*sp.diff(U,s)+sp.diff(U,x,2)+sp.diff(U,y,2))
assert res==0
shape=sp.exp(-2*(x*x+y*y)/(1+s*s))/(1+s*s)
assert sp.simplify(1/(1+sp.I*s)+1/(1-sp.I*s)-2/(1+s*s))==0
assert sp.simplify(1/((1+sp.I*s)*(1-sp.I*s))-1/(1+s*s))==0
ck('paraxial_equation_symbolic',0.,0.); ck('reciprocal_mode_product_symbolic',0.,0.)
# Infinite Gaussian-mode Fourier integral, independent longitudinal quadrature.
for kz in [0.,1e-8,5e-8]:
    kp=k; A=Lt*Lt*kp*kp/2; b=kz*zR
    integ=2*quad(lambda t:math.exp(-A*t*t)*math.cos(b*t),0,20,epsabs=1e-12)[0]
    analytic=math.sqrt(math.pi/A)*math.exp(-b*b/(4*A))
    ck('longitudinal_transform',abs(integ/analytic-1),1e-10)
# Infinite-source angular integral via a coordinate resolving its narrow peak.
a=Lt*Lt*k*k; B=zR*zR/(Lt*Lt)
J=2*quad(lambda v:math.exp(-a*B/(B+v*v)-v*v)/math.sqrt(B+v*v),0,12,epsabs=1e-14)[0]
full=4*math.pi**2*MR*F*F*Lt*Lt*zR*zR/k*J/hb
full_lead=4*math.pi**2.5*MR*F*F*Lt**3*zR/k*math.exp(-a)/hb
ck('infinite_narrow_angle_control',abs(full/full_lead-1),1e-7)
# Exact angular integral of finite-window paraxial source, no narrow-angle replacement.
# Mirrors truncate the modeled vacuum source at +/-Z; their material is not modeled.
def finite(Z,order):
    Q=k*Z; b=(Z/zR)**2
    nodes,weights=leggauss(order); nseg=int(math.ceil(Q/math.pi))
    total=0.
    for j in range(nseg):
        us=(j+(nodes+1)/2)/nseg
        for u,weight in zip(us,weights):
            A=.5*Lt*Lt*k*k*(1-u*u)
            iz=quad(lambda t:math.exp(-A*b*t*t),0,1,weight='cos',wvar=Q*u,epsabs=1e-12,epsrel=1e-12)[0]
            total+=weight/(2*nseg)*math.exp(-2*A)*iz*iz
    total*=2
    return 2*math.pi*MR*k*F*F*Lt**4*(2*Z)**2*total/hb
rows=[]
for zm in [.5,5.]:
    Z=zm/hc; r12=finite(Z,12); r24=finite(Z,24)
    ck('finite_angular_refinement',abs(r12/r24-1),2e-10)
    approx=full_lead*math.erf(k*Lt*Z/zR)
    radius=Z+zR*zR/Z; cavity_g=1-2*Z/radius
    assert 0<=cavity_g*cavity_g<1
    rows.append(dict(mirror_separation_m=2*zm,mirror_curvature_m=radius*hc,
        symmetric_cavity_g_squared=cavity_g*cavity_g,mediators_per_s=r24,
        narrow_angle_estimate_per_s=approx,relative_approximation_error=approx/r24-1))
result=dict(waist_radius_m=w0*hc,Rayleigh_range_m=zR*hc,
    divergence_radians=2/(kph*w0),circulating_power_each_direction_W=intensity*math.pi*(w0*hc)**2/2,
    infinite_mode_rate_per_s=full,finite_cavities=rows,passed=len(checks),checks=checks,
    scope='Leading scalar paraxial fields, ideal matched modes and prescribed circulating intensity; no material or experimental certification')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
