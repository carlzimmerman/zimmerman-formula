"""Exact independent checks of the same-field Lorentz well replacement."""
from pathlib import Path
import json,sys
import sympy as S
out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent
out.mkdir(exist_ok=True)
e,q,a,A,ep=S.symbols('e q a A ep',positive=True)
Q0,psi,Phi,v,gx,shift=S.symbols('Q0 psi Phi v gx shift',real=True)
N=1+e*psi;scale=a*S.exp(-e*Phi);Qt=(q+e*v-e**2*shift)/N;Y=e**2*gx**2/scale**2
mu=S.sqrt(Qt**2-Y);F=lambda z:-A*S.exp((z-Q0)/ep)
change=N*scale**3*(-F(mu)+F(Qt))
extra=S.simplify(S.diff(change,e,2).subs(e,0)/2)
F1=S.diff(F(q),q);F2=S.diff(F(q),q,2)
assert S.simplify(extra-a*F1*gx**2/(2*q))==0
assert all(S.diff(extra,z)==0 for z in [psi,Phi,v,shift])
# Real-space variation and a mode's Fourier image.
k,Pamp=S.symbols('k Pamp',real=True)
extra_EL_fourier=S.simplify(S.diff(extra,gx,2)*k**2*Pamp)
assert S.simplify(extra_EL_fourier-a*F1*k*k*Pamp/q)==0
# Covariant k-essence direct chain-rule calculation, X=−(dphi)^2/2.
X=S.Symbol('X',positive=True);P=-F(S.sqrt(2*X));PX=S.diff(P,X);PXX=S.diff(P,X,2)
kin=S.simplify((PX+2*X*PXX).subs(X,q*q/2));grad=S.simplify(PX.subs(X,q*q/2));cs2=S.simplify(grad/kin)
assert S.simplify(kin+F2)==0 and S.simplify(grad+F1/q)==0 and cs2==ep/q
n=-F1;pressure=-F(q);rho=F(q)-q*F1
assert S.simplify(pressure-ep*n)==0 and S.simplify(rho-(q-ep)*n)==0
assert S.simplify(S.diff(pressure,q)/S.diff(rho,q)-ep/q)==0
# Remove the clock from the well exactly, not only quadratically.
Q,Y0=S.symbols('Q Y',real=True);z=S.sqrt(Q**2-Y0);L=-F(z)
clock_defect=S.simplify(-2*Q*S.diff(L,Y0)-S.diff(L,Q))
assert clock_defect==0
# Static weak-field gradient block and completion of the lapse-potential square.
alpha,d,beta,g,p=S.symbols('alpha d beta g p',real=True)
n0=S.Symbol('n0',positive=True)
betaeff=beta+n0/(2*d*q)
static=-(2-alpha)*g*g+2*d*g*p-d*betaeff*p*p
complete=-(2-alpha)*(g-d*p/(2-alpha))**2-d*(betaeff-d/(2-alpha))*p*p
assert S.factor(static-complete)==0
beta_cancel=d/(2-alpha)
beta_repair=beta_cancel-n0/(2*d*q)
assert S.simplify((betaeff-beta_cancel).subs(beta,beta_repair))==0
# Nonlinear local charge and static ellipticity; express Q²=s²+Y.
s,Ys=S.symbols('s Ys',positive=True)
ns=A/ep*S.exp((s-Q0)/ep)
flux=ns/s
fluxY=-S.diff(flux,s)/(2*s)
long=S.factor(flux+2*Ys*fluxY)
expected=ns/s*(1+Ys/s**2-Ys/(s*ep))
assert S.simplify(long-expected)==0
assert S.simplify(long/(ns/s)-(s*s+Ys-Ys*s/ep)/s**2)==0
# Intrinsic sound cone and stationary sonic threshold agree.
Qsq=s*s+Ys
assert S.simplify((1+Ys/s**2-Ys/(s*ep))*s**2*ep-(ep*Qsq-Ys*s))==0
res={'quadratic_extra_density':str(extra),'Fourier_extra_EL_P':str(extra_EL_fourier),'lapse_shift_and_velocity_Hessian_unchanged':True,'intrinsic_temporal_coefficient':str(kin),'intrinsic_gradient_coefficient':str(grad),'intrinsic_sound_speed_squared':str(cs2),'rho':str(rho),'pressure':str(pressure),'clock_defect_zero':True,'beta_eff':'beta+n/(2*d*s), s=sqrt(Q^2−Y); at Y=0 use s=Q','beta_counterterm_cancels_new_quadratic_gradient':True,'nonlinear_longitudinal_static_flux_coefficient':str(long),'static_elliptic_domain':'Y*s < epsilon*Q^2 for the isolated well; total MOND operator differs','scope':'Exact symbolic identities on the timelike Q>0 branch. No full-system stability or same-action galactic solution is certified.','sympy':S.__version__}
(out/'results.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
