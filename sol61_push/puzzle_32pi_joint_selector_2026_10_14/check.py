import sympy as s,json
A,H,M2,Z,fp,fpp,Vpp=s.symbols('A H M2 Z fp fpp Vpp',positive=True)
d,dp,dpp=s.symbols('d dp dpp',real=True)
checks=[]
def ck(n,e):
 assert s.simplify(e)==0,(n,e)
 checks.append(n)
# Linearized lapse constraint, using Vprime=24 H^4 fprime.
h=4*H**3*fp/M2*d-4*H**2*fp/M2*dp
hd=4*H**3*fp/M2*dp-4*H**2*fp/M2*dpp
lin=Z*(dpp+3*H*dp)+Vpp*d-24*(fpp*H**4*d+fp*(4*H**3*h+H**2*hd))
D=Z+96*H**4*fp**2/M2
N=Vpp-24*H**4*fpp-384*H**6*fp**2/M2
ck('metric_constrained_linearization',lin-(D*dpp+3*H*D*dp+N*d))
a,F,beta,V0,z,eps,p,U=s.symbols('a F beta V0 z eps p U',positive=True)
f=beta*s.log(a/F)
V=V0*s.exp(a**2/F**2)
H2=M2*z/(4*beta); Ueq=3*M2**2*z/(4*beta)
# Substitute a^2=F^2 z after evaluating derivatives, V0 exp(...)=Ueq.
vprime=2*a*U/F**2
vsecond=(2/F**2+4*a**2/F**4)*U
ck('exponential_vacuum_equation',(vprime-24*s.diff(f,a)*H2**2).subs({U:Ueq,a:F*s.sqrt(z)}))
Dexp=D.subs({Z:1,H:s.sqrt(H2),fp:s.diff(f,a)}).subs(a,F*s.sqrt(z))
Nexp=N.subs({Vpp:vsecond,H:s.sqrt(H2),fp:s.diff(f,a),fpp:s.diff(f,a,2)}).subs({U:Ueq,a:F*s.sqrt(z)})
ck('kinetic_coefficient',Dexp-(1+6*M2*z/F**2))
ck('restoring_coefficient',Nexp-4*Ueq/F**2*(1-z))
ck('mass_over_H_squared',(Nexp/Dexp/H2).subs(F**2,eps*M2)-12*(1-z)/(eps+6*z))
ck('amplitude_relation', (V0*s.exp(z)-Ueq).subs(V0,3*M2**2/(4*beta)*z*s.exp(-z)))
ck('amplitude_independent_ratio',3*H2/(F**2*z)-3*M2/(4*beta*F**2))
gamma=s.symbols('gamma',positive=True)
ck('target_coupling',(3/(4*gamma)).subs(gamma,3/(128*s.pi))-32*s.pi)
ck('alternative_coupling',(3/(4*gamma)).subs(gamma,3/(64*s.pi))-16*s.pi)
ck('dimensionless_volume',24*s.pi**2/(3/(4*gamma))**2-s.Rational(128,3)*s.pi**2*gamma**2)
ck('target_volume',(s.Rational(128,3)*s.pi**2*gamma**2).subs(gamma,3/(128*s.pi))-s.Rational(3,128))
# Pure-power potential at its positive-energy stationary point.
Hp2=p*M2/(8*beta); Up=3*M2*Hp2
Np=N.subs({Vpp:p*(p-1)*Up/a**2,H:s.sqrt(Hp2),fp:beta/a,fpp:-beta/a**2})
ck('pure_power_tachyon',Np+p**2*Up/a**2)
# General potential logarithmic slopes: p=d log U/d log a; pd=d p/d log a.
pd=s.symbols('pd',real=True)
Ng=N.subs({Vpp:Up/a**2*(p*p-p+pd),H:s.sqrt(Hp2),fp:beta/a,fpp:-beta/a**2})
ck('general_slope_criterion',Ng-Up/a**2*(pd-p*p))
t=s.symbols('t',real=True)
# At an additive-offset stationary point, w=Uexp/(3M2 Hscale^2)=z/(1+t)^2.
w=z/(1+t)**2
ck('shifted_stationarity',z*w-(w*(1+t))**2)
ck('shifted_ratio',w*(1+t)/z-1/(1+t))
# Log-coupling derivative couples to extra Weyl curvature in a local source.
Weyl=s.symbols('Weyl',real=True)
ck('local_source_residual',24*H**4*beta/a-(24*H**4+Weyl)*beta/a+Weyl*beta/a)
print(json.dumps({'count':len(checks),'checks':checks,'scope':'Conditional scalar-GB vacuum and linear homogeneous perturbations; no MOND source completion or quantum protection.'},indent=2))
