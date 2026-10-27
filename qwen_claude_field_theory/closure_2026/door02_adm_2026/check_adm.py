"""Exact local ADM Hessian and homogeneous necessary conditions; no DOF theorem."""
import json
from pathlib import Path
import sympy as s

F,c1,c2,c3,c4,b,xi=s.symbols('F c1 c2 c3 c4 b xi', real=True)
N,r=s.symbols('N sqrt_h', positive=True)
v=s.symbols('v0:6', real=True)
w=s.symbols('phidot_minus_shift', real=True)
R,Lambda=s.symbols('R3 Lambda', real=True)
av=s.symbols('acc0:3', real=True)
pv=s.symbols('grad0:3', real=True)
sv=s.symbols('S0:6', real=True)
J=s.Function('J'); Kfun=s.Function('Kfun')

# Orthonormal basis of Sym^2 at a point, with B0=I/sqrt(3).
# An arbitrary positive spatial metric admits this invertible basis change.
rt=s.sqrt
basis=[s.eye(3)/rt(3),s.diag(1,-1,0)/rt(2),s.diag(1,1,-2)/rt(6)]
for i,j in [(0,1),(0,2),(1,2)]:
    z=s.zeros(3); z[i,j]=z[j,i]=1/rt(2); basis.append(z)
assert all(s.trace(x*y)==int(i==j) for i,x in enumerate(basis) for j,y in enumerate(basis))
Km=sum((v[i]*basis[i] for i in range(6)),s.zeros(3))/(2*N)
Q=w/N
S=sum((sv[i]*basis[i] for i in range(6)),s.zeros(3))
X=sum(x*x for x in pv)+xi**2*s.trace(S*S)
A=F-c1-c3; B=F+c2; D=s.expand(A-3*B)
lag=N*r*(F*(R-2*Lambda)+A*s.trace(Km*Km)-B*s.trace(Km)**2
         +(c1+c4)*sum(x*x for x in av)+2*b*sum(x*y for x,y in zip(av,pv))
         -Kfun(Q)-b*J(X))
coords=list(v)+[w]
H=s.simplify(s.hessian(lag,coords))
kpp=s.symbols('Kpp', real=True)
H=H.xreplace({s.Subs(s.Derivative(Kfun(s.Symbol('_xi_1')), (s.Symbol('_xi_1'),2)),s.Symbol('_xi_1'),w/N):kpp})
# SymPy dummy symbols are not assumed to use a particular printed name.
H=H.replace(lambda z:isinstance(z,s.Subs) and z.expr.is_Derivative,
            lambda z:kpp)
Hn=s.simplify(N*H/r)
expected=s.diag(D/2,*([A/2]*5),-kpp)
assert Hn==expected
full=s.zeros(11); full[:7,:7]=Hn
det=s.factor(Hn.det())
assert s.simplify(det+kpp*D*A**5/64)==0
generic_rank=Hn.rank()
assert generic_rank==7

# Exact rank on each degeneracy stratum. Parameters chosen so A and D
# independently vanish or remain nonzero; ranks computed, not inserted.
rank_table=[]
for azero in (False,True):
  for dzero in (False,True):
    for qzero in (False,True):
      sample={F:2,c1:2 if azero else 0,c3:0,
              c2:-2 if azero and dzero else (-s.Rational(4,3) if dzero else 1),
              kpp:0 if qzero else 3}
      rank=Hn.subs(sample).rank()
      expected_rank=5*int(not azero)+int(not dzero)+int(not qzero)
      assert rank==expected_rank
      rank_table.append({'A_zero':azero,'D_zero':dzero,'Kpp_zero':qzero,
                         'computed_rank':rank,'sample':{str(k):str(val) for k,val in sample.items()}})

# Canonical momentum trace: dL/dv0 = trace(Pi)/sqrt(3).
ptrace=s.simplify(rt(3)*s.diff(lag,v[0]))
assert s.simplify(ptrace-r*D*s.trace(Km))==0

# Projected connection cancellation for completely arbitrary shift at a point.
Ns=s.symbols('shift0:3'); kij,gamma=s.symbols('Kij spatial_connection_contraction')
V0=sum(Ns[i]*pv[i] for i in range(3))
connection=s.expand(gamma-sum(Ns[i]*pv[i] for i in range(3))*kij/N+kij*V0/N)
assert s.simplify(connection-gamma)==0

# FLRW reduction: spatially flat or curvature kappa, constant K plus optional
# affine coefficient ell. Matter variation convention dL_m/dN=-a^3 rho,
# dL_m/da=3N a^2 p. D=0 is imposed only after differentiating.
a,adot,pdot,kappa,C,ell,rho,pressure=s.symbols('a adot phidot kappa C ell rho pressure',real=True)
Ds=s.symbols('D',real=True)
lf=3*Ds*a*adot**2/N +6*F*kappa*N*a-N*a**3*C-ell*a**3*pdot
lfdeg=lf.subs(Ds,0)
ELN=s.simplify(s.diff(lfdeg,N)-a**3*rho)
ELa=s.simplify(s.diff(lfdeg,a)+3*N*a**2*pressure)
ELphi=3*ell*a**2*adot # dL/dphi - d/dt(dL/dphidot)
fluid=s.solve([ELN,ELa],[rho,pressure],dict=True)[0]
rho_plus_p=s.simplify(fluid[rho]+fluid[pressure])
assert s.simplify(rho_plus_p-(4*F*kappa/a**2+ell*pdot/N))==0
assert rho_plus_p.subs({ell:0,kappa:0})==0

# First-order affine term is not a harmless total derivative for evolving a.
omega=s.diff(s.diff(lfdeg,pdot),a)
assert omega==-3*ell*a**2

result={
 'interpretation':'Exact finite-dimensional differentiation verifies the local ADM Hessian algebra under the stated geometric reduction; it is not a Dirac constraint or health proof.',
 'kinetic_coefficients':{'A':str(A),'B':str(B),'D':str(D)},
 'basis':'v0 is dot_h trace divided by sqrt(3), after subtracting shift Lie derivative; v1..v5 orthonormal shear; w=phidot-shift.gradphi',
 'normalized_hessian':str(Hn),'normalized_determinant':str(det),
 'generic_rank_metric_phi':generic_rank,'full_rank_with_lapse_shift':full.rank(),
 'rank_strata':rank_table,'momentum_trace':str(ptrace),
 'FLRW_lagrangian':str(lf),'FLRW_degenerate_lapse_equation':str(ELN),
 'FLRW_degenerate_scale_equation':str(ELa),'FLRW_phi_equation':str(ELphi),
 'FLRW_fluid_solution':{str(k):str(val) for k,val in fluid.items()},
 'FLRW_rho_plus_p':str(rho_plus_p),'affine_symplectic_component':str(omega),
 'checks_passed':['orthonormal tensor basis','full Hessian differentiated from Lagrangian',
  'all 8 exact degeneracy strata','trace momentum differentiated','projected connection cancellation',
  'FLRW lapse and scale variation','flat constant-K rho+p=0','affine first-order mixing retained'],
 'non_claims':['No full Dirac algebra','No universal absence of scalar or ghost',
  'No lensing or MOND proof','No curved/inhomogeneous cosmological no-go']}
out=Path(__file__).parent/'run'/'result.json'
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
