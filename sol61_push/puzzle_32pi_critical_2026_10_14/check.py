import sympy as s
import json
m,k,L,g,rho,t,d,B,D=s.symbols('m k L g rho t d B D',positive=True)
checks=[]
def ck(name,x):
 assert s.simplify(x)==0,(name,x)
 checks.append(name)
# Derivative of the UV-subtracted Gaussian determinant, one real scalar in 3D.
Jp=s.integrate(-2*m**3/(k*k+m*m),(k,0,L))/(4*s.pi**2)
ck('subtracted_loop_derivative',Jp+m*m*s.atan(L/m)/(2*s.pi**2))
ck('continuum_loop_derivative',s.limit(Jp,L,s.oo)+m*m/(4*s.pi))
J=-m**3/(12*s.pi)
ck('integrated_loop',s.diff(J,m)+m*m/(4*s.pi))
Vaux=g*rho**3/6-m*m*rho/2+J
V=s.factor(Vaux.subs(rho,-m/(4*s.pi)))
ck('critical_coupling',V-m**3/(24*s.pi)*(1-g/(16*s.pi**2)))
ck('flat_critical',V.subs(g,16*s.pi**2))
E=d*m**3/(24*s.pi)-t*m/(8*s.pi)
m0=s.symbols('m0',positive=True)
Es=E.subs(t,d*m0*m0)
ck('stationarity',s.diff(Es,m).subs(m,m0))
depth=-Es.subs(m,m0)
ck('condensation_depth',depth-d*m0**3/(12*s.pi))
W2=s.diff(Es,m,2).subs(m,m0); W3=s.diff(Es,m,3)
ck('amplitude_ratio',depth*W3**2/W2**3-s.Rational(1,3))
x=s.symbols('x',real=True)
Escaled=B*Es.subs(m,m0+D*x)
ck('normalization_independence',(-B*Es.subs(m,m0))*s.diff(Escaled,x,3).subs(x,0)**2/s.diff(Escaled,x,2).subs(x,0)**3-s.Rational(1,3))
# General scaling function jet; all common amplitude and field scales cancel.
f0,f2,f3=s.symbols('f0 f2 f3',positive=True)
ck('general_scaling_ratio',(B*f0)*(B*f3/D**3)**2/(B*f2/D**2)**3-f0*f3*f3/f2**3)
# Additive total-vacuum background does NOT cancel from the physical invariant.
e0=s.symbols('e0',real=True)
ck('background_sensitivity',(depth+e0)*W3**2/W2**3-s.Rational(1,3)-e0*4*s.pi/(d*m0**3))
print(json.dumps({'count':len(checks),'checks':checks,'critical_g':'16pi²','critical_relative_energy':'0 for every m at t=0','deformed_condensation_response_ratio':'1/3','required_total_vacuum_response_ratio':'64pi','ratio_target_over_candidate':float(192*s.pi),'scope':'Leading large-N 3D scalar composite sector. No identification with MOND polarization, 4D gravity or total vacuum energy.'},indent=2))
