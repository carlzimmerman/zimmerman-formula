"""Exact binding-energy identities and bounded finite-stock energy budgets."""
import json
import sys
from pathlib import Path
import mpmath as mp
import sympy as sp

q,y,s=sp.symbols('q y s',positive=True)
x=sp.symbols('x',positive=True)
F=-x-sp.log(1-x)-x*x/2
checks=[]
def exact(name,value):
    value=sp.simplify(value)
    assert value==0,(name,value)
    checks.append(name)

exact('positive electric series derivative',sp.diff(F,x)-x*x/(1-x))
R=sp.sqrt(s*(s+1))
exact('canonical edge stock',(sp.sqrt(1+4*R**2)-1)/2-s)
exact('exterior derivative decomposition',s*s/(y*y*(y*y-s))-(-s/y**2+s/(y*y-s)))
minimum=sp.Rational(2,3)*(q**3*sp.asinh(1/q)-q*sp.sqrt(1+q*q)-2*sp.asinh(q))
mu=-sp.sqrt(1+q*q)/q+q*sp.asinh(1/q)
exact('binding formula derivative',sp.diff(minimum,q)-2*q*mu)
exact('zero inventory constant',sp.limit(minimum,q,0,dir='+'))
L=sp.symbols('L',positive=True)
exact('uniform baryon potential',sp.integrate((s*y**3/L**3)/y**2,(y,0,L))+s/L-sp.Rational(3,2)*s/L)
n=sp.symbols('n',integer=True,positive=True)
exact('uniform interior monomial',sp.integrate(y**(n+2),(y,0,1))-1/(n+3))
exact('tail coefficient identity',1/(n*(n+3))+1/(n*(2*n-3))-3/((n+3)*(2*n-3)))
exact('energy dimensional scale',(s*sp.symbols('Mb',positive=True))*sp.symbols('a0',positive=True)*sp.symbols('rM',positive=True)/(s*sp.symbols('Mb',positive=True)*sp.symbols('c',positive=True)**2)-sp.symbols('a0',positive=True)*sp.symbols('rM',positive=True)/sp.symbols('c',positive=True)**2)

mp.mp.dps=70
def fsmall(v):
    if not v:return mp.mpf('0')
    if v<mp.mpf('.05'):
        return mp.fsum(v**k/k for k in range(3,90))
    return -v-mp.log1p(-v)-v*v/2
def min_energy(stock):
    z=mp.sqrt(stock)
    return mp.mpf(2)/3*(z**3*mp.asinh(1/z)-z*mp.sqrt(1+z*z)-2*mp.asinh(z))
def min_integral(stock):
    radius=mp.sqrt(stock*(stock+1));upper=2*mp.asinh(mp.sqrt(stock))
    def inner(t):
        if not t:return mp.mpf('0')
        value=1/mp.cosh(t/2)**2
        field=-value-2*mp.log(mp.tanh(t/2))-value*value/2
        return mp.sinh(t)**2*mp.cosh(t)*field/8
    interior=mp.quad(inner,[0,upper/2,upper])
    exterior=mp.quad(lambda z: radius**3*fsmall(stock*z*z/radius**2)/z**4 if z else 0,[0,1])
    return interior+exterior-mp.asinh(2*radius)

rows=[];max_error=mp.mpf('0')
for catchment in (mp.mpf(3),mp.mpf(6),mp.mpf(10)):
    stock=mp.mpf('5.364')*catchment;radius=mp.sqrt(stock*(stock+1))
    e_min=min_energy(stock);integral=min_integral(stock)
    error=abs(e_min-integral);max_error=max(max_error,error)
    assert error<mp.mpf('1e-50'),error
    for ratio in (mp.mpf('1.5'),mp.mpf(2),mp.mpf(4)):
        length=ratio*radius;a=stock/length**2;terms=50
        electric=length**3*mp.fsum(a**k*(1/(mp.mpf(k)*(k+3))+1/(mp.mpf(k)*(2*k-3))) for k in range(3,terms+1))
        remainder=2*length**3*a**(terms+1)/((terms+1)**2*(1-a))
        initial=electric-mp.mpf(3)*stock/(2*length)
        gap=initial-e_min;assert gap>0 and a<1
        rows.append(dict(N=str(catchment),s=str(stock),start_radius_over_edge=str(ratio),edge_rM=str(radius),capacity_max=str(a),minimum_energy_E0=str(e_min),uniform_energy_lower_E0=str(initial),uniform_energy_truncation_bound_E0=str(remainder),excess_energy_lower_E0=str(gap),excess_per_cold_mass_in_a0rM=str(gap/stock)))

# Assigned unit conversion, not a new measurement or a galaxy-data fit.
G=mp.mpf('6.67430e-11');solar=mp.mpf('1.98892e30');mb=10**mp.mpf('10.5')*solar
a0=mp.mpf('9.3603e-11');c=mp.mpf(299792458);rm=mp.sqrt(G*mb/a0);scale=mb*a0*rm
for row in rows:
    row['excess_energy_lower_joule']=str(mp.mpf(row['excess_energy_lower_E0'])*scale)
    row['fraction_of_cold_rest_energy_lower']=str(a0*rm/c**2*mp.mpf(row['excess_per_cold_mass_in_a0rM']))
result=dict(claim_id='AR4-ENERGY-001',exact_checks=len(checks),check_names=checks,minimum_direct_integral_checks=3,maximum_closed_vs_integral_error=str(max_error),finite_initial_states=rows,assigned_unit_inputs=dict(G_SI=str(G),solar_mass_kg=str(solar),Mb_solar='10^10.5',a0_SI=str(a0),c_SI=str(c),rM_m=str(rm),E0_joule=str(scale)),non_claims=['Gamma-zero fixed-baryon Newtonian reduction; no physical formation rate or radiation channel.','No derived N, cosmological initial state, microscopic retention or stiffness.','The universal formula follows from the analytic argument; finite checks audit its reductions.'])
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'exact_checks':len(checks),'direct_integral_checks':3,'initial_states':len(rows),'maximum_minimum_energy_error':str(max_error)}))
