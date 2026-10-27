import sympy as s
import json,math
M,C,a,b,mu2,delta,R=s.symbols('M C a b mu2 delta R',positive=True)
f=-3*M**2/(16*C*a**2)
V=2*C*M**2*a**2
h2=2*C*a**2/3
E0=24*h2**2
checks={}
def eq(n,x,y):
 assert s.simplify(x-y)==0,(n,s.simplify(x-y))
 checks[n]=str(y)
eq('background_scalar',s.diff(V,a)-s.diff(f,a)*E0,0)
# Fixed a at two distinct Euler invariants requires f'=0; here f' >0.
eq('coupling_derivative',s.diff(f,a),3*M**2/(8*C*a**3))
E=s.symbols('E',positive=True)
eq('fixed_geometry_equilibrium',s.diff(V-f*E,a)*a**3/(4*C*M**2),a**4-3*E/(32*C**2))
Riem2,Ric2,R2=s.symbols('Riem2 Ric2 R2')
GB=Riem2-4*Ric2+R2; Weyl=Riem2-2*Ric2+R2/3
eq('Weyl_blind_identity',GB-Weyl,2*R2/3-2*Ric2)
PR=M**2*R/2-V+f*R**2/6
eq('Ricci_filtered_stationary_metric',(s.diff(PR,R)*R-2*PR).subs(R,8*C*a*a),0)
eq('Ricci_filtered_stationary_scalar',s.diff(PR,a).subs(R,8*C*a*a),0)
eq('Ricci_filtered_tensor_coefficient',2*s.diff(PR,R).subs(R,8*C*a*a),0)
x=s.symbols('x',positive=True); F=s.Function('F')
Q=M*M*a*a*F(R/a**2)
eq('scale_only_scalar_identity',s.diff(Q,a)/(2*M*M*a),(F(x)-x*s.diff(F(x),x)).subs(x,R/a**2))
eq('scale_only_trace_identity',(R*s.diff(Q,R)-2*Q)/(M*M*a*a),(x*s.diff(F(x),x)-2*F(x)).subs(x,R/a**2))
# Stabilizer: zero value and slope at b, with independent positive curvature mu2.
Vs=V+mu2*(a-b)**2/2
res=s.diff(Vs,a)-s.Rational(8,3)*s.diff(f,a)*Vs**2/M**4
eq('stabilizer_preserves_vacuum',res.subs(a,b),0)
eq('stabilizer_restoring_derivative',s.diff(res,a).subs(a,b),mu2)
F1=8*h2*s.diff(f,a)
eq('deSitter_scalar_metric_mixing',F1,2*M**2/a)
D=1+3*F1**2/(2*M**2)
eq('deSitter_kinetic',D,1+6*M**2/a**2)
U2=s.diff(Vs,a,2).subs(a,b)-24*h2.subs(a,b)**2*s.diff(f,a,2).subs(a,b)
eq('Einstein_frame_mass_numerator',U2-2*F1.subs(a,b)**2*V.subs(a,b)/M**4,mu2)
shift_res=s.diff(Vs,a)-s.Rational(8,3)*s.diff(f,a)*(Vs+delta)**2/M**4
eq('vacuum_shift_linear_response',s.diff(shift_res,delta).subs({a:b,delta:0}),-4/b)
# Algebraic coefficient drift is not removed by stabilizing the scalar.
eq('coefficient_drift',(Vs+delta)/(M*M*a*a),2*C+(mu2*(a-b)**2/2+delta)/(M*M*a*a))
eq('positive_restoring_mass',mu2/D,mu2*a*a/(a*a+6*M*M))
# Two-pole decomposition diagnostic, not a curved-background propagator calculation.
z,A,B=s.symbols('z A B',nonzero=True)
eq('opposite_pole_residues',1/(z*(A+B*z)),(1/z-1/(z+A/B))/A)
rows=[]
G=6.67430e-11;c=299792458.;Ms=1.98847e30;au=149597870700.;pc=3.085677581491367e16
for name0,a0 in [('canonical',9.3619e-11),('alternative',1.1279e-10)]:
 H2=32*math.pi*a0*a0/(3*c*c)
 for name,m,r in [('Sun_1AU',Ms,au),('Sun_surface_exterior',Ms,6.957e8),('point_baryon_1e11Msun_10kpc',1e11*Ms,1e4*pc)]:
  ratio=2*(G*m/(r**3*H2))**2
  rows.append({'footing':name0,'example':name,'Euler_excess_over_deSitter':ratio,'frozen_metric_equilibrium_scale_ratio':(1+ratio)**.25,'frozen_metric_mu2_over_M2_for_1pct':64*math.pi*ratio/.01})
print(json.dumps({'checks':checks,'count':len(checks),'benchmarks':rows,'scope':'Exact identities and six fixed-background stress tests; no full stellar or galactic solution'},indent=2))
