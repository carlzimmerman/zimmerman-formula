"""Exact algebra for a specified KGB branch; no fitted inputs or parameter scan."""
import argparse,json
from pathlib import Path
import sympy as S
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutate',action='store_true');a=p.parse_args()
r,h,A,M2,X,q,N,f=S.symbols('r h A M2 X q N f',positive=True)
y,yp,fp,np,xp,kx,gx,K,n=S.symbols('y yp fp nuprime Xprime Kx Gx K n',real=True)
checks=[]
def ck(name,e):
 z=S.factor(S.simplify(e));checks.append(dict(name=name,passed=z==0,residual=str(z)))
xdef=q*q/(2*N*N)-f*y*y/2
xd=-q*q*np/(N*N)-fp*y*y/2-f*y*yp
box=f*yp+((n-1)*f/r+f*np+fp/2)*y
jr=f*((kx-gx*box)*y-gx*xd)
reduced=f*(kx*y-gx*((n-1)*f*y*y/r-2*X*np))
ck('general_n_current_reduction',jr-reduced.subs(X,xdef))
C=S.symbols('C',real=True)
ttr=q*(C*y-gx*xp)
ck('offdiagonal_current',ttr-q*(f*(C*y-gx*xp))/f)
# C=Kx-Gx box; zero-current branch C=Gx Xprime/y.
pr=C*f*y*y-2*gx*f*xp*y+K+gx*f*xp*y
rho=C*q*q/(N*N)-K-gx*f*xp*y
ck('radial_pressure_on_zero_flux',pr.subs(C,gx*xp/y)-K)
ck('density_on_zero_flux',(rho.subs(C,gx*xp/y)+K-2*X*gx*xp/y).subs(X,xdef))
# Braiding sign mutation changes the model, not the asserted reference identities.
glog=(1 if not a.mutate else -1)*A/(3*h*S.sqrt(2)*X**S.Rational(3,2))
klog=-A/X
nulocal=f*y*y/(r*X)+3*h*y/S.sqrt(2*X)
ck('logarithmic_zero_current',reduced.subs({n:3,kx:klog,gx:glog,np:nulocal}))
v=S.symbols('v',real=True)
ck('flow_current',nulocal.subs(y,S.sqrt(2*X/f)*v)-(2*v*v/r+3*h*v/S.sqrt(f)))
ck('flow_X',xdef.subs(y,S.sqrt(2*X/f)*v).subs(X,q*q/(2*N*N*(1+v*v)))-q*q/(2*N*N*(1+v*v)))
fd=1-h*h*r*r;yd=-q*h*r/fd
nd=-h*h*r/fd
jds=reduced.subs({n:3,kx:klog,gx:glog}).subs({f:fd,y:yd,np:nd,X:q*q/2})
ck('deSitter_zero_current',jds)
box3=box.subs(n,3)
ck('deSitter_box',box3.subs({f:fd,fp:S.diff(fd,r),np:nd,y:yd,yp:S.diff(yd,r)})+3*h*q)
ck('deSitter_Einstein_density',(1-fd)/r**2-S.diff(fd,r)/r-3*h*h)
ck('deSitter_Einstein_pressure',(fd-1)/r**2+2*fd*nd/r+3*h*h)
u=S.symbols('u',positive=True) # u=G_N m_source
z=S.sqrt(2*u/r+h*h*r*r);fs=1-z*z;ys=-q*z/fs
bs=box3.subs({f:fs,fp:S.diff(fs,r),np:S.diff(fs,r)/(2*fs),y:ys,yp:S.diff(ys,r)})
ck('constantX_SdS_box',bs+3*q*(u/r**2+h*h*r)/z)
ck('constantX_SdS_obstruction',(u/r**2+h*h*r)**2-h*h*z*z-u*u/r**4)
# Leading weak-potential equations retain w^2/r and h*w simultaneously.
w,wp,g=S.symbols('w wp g',real=True)
vlead=-h*r+w
ck('weak_current',S.expand(2*vlead*vlead/r+3*h*vlead)+h*h*r-(2*w*w/r-h*w))
# Xprime/X=-2(nuprime+v vprime) at retained order.
num=-h*h*r+g+vlead*(-h+wp)
ck('density_division', (num-vlead*(wp+2*w/r)).subs(g,2*w*w/r-h*w))
F=S.Function('Phi')(r);rho_b=S.Function('rho_b')(r)
deltaf=-2*r*S.diff(F,r)
ck('Einstein_to_Poisson',(-deltaf/r**2-S.diff(deltaf,r)/r)/2-(S.diff(F,r,2)+2*S.diff(F,r)/r))
ck('integrated_density_derivative',S.diff(r*r*S.Function('w')(r),r)/r**2-(S.diff(S.Function('w')(r),r)+2*S.Function('w')(r)/r))
d=S.symbols('d',positive=True);alpha=3*(1-d)
gN=u/r**2
ss=h*d*r/4*(S.sqrt(1+8*gN/(h*h*d*d*r))-1)
ck('screening_root',2*ss*ss/r+h*d*ss-gN)
bc=alpha*h/(3 if not a.mutate else 6)
gforce=gN+bc*ss
ck('screening_metric_and_scalar_match',gforce-(2*ss*ss/r+h*ss))
ratio=1+2*alpha/(3*d*(S.sqrt(1+8*u/(h*h*d*d*r**3))+1))
ck('force_ratio',gforce/gN-ratio)
ck('outer_inverse_square',S.limit(gforce/gN,r,S.oo)-1/d)
ck('inner_Newton',S.limit(gforce/gN,r,0)-1)
ck('inner_correction_amplitude',S.limit((gforce-gN)*S.sqrt(r),r,0)-alpha*h*S.sqrt(u/2)/3)
rV=(8*u/(h*h*d*d))**S.Rational(1,3)
gV=u/rV**2
ck('transition_mass_exponent',S.simplify(u*S.diff(gV,u)/gV)-S.Rational(1,3))
# Full inhomogeneous classical field rescaling, not quantum matching.
Y,Xv,Xref,V,B0,power=S.symbols('Y Xv Xref V B0 power',positive=True)
Lpot=-A*S.log(Xv*Y/Xref)-V
ck('rescaled_potential',S.expand_log(Lpot,force=True).subs(S.log(Xv),(3*M2*h*h-V)/A+S.log(Xref))+A*S.log(Y)+3*M2*h*h)
g3=-S.sqrt(2)*A/(3*h*S.sqrt(X))
ck('rescaled_braiding',-g3.subs(X,Xv*Y)*S.sqrt(2*Xv)-2*A/(3*h*S.sqrt(Y)))
ck('normalized_clock_invariant',S.sqrt(2*Xv)/S.sqrt(2*Xv*Y)-1/S.sqrt(Y))
ck('response_coefficient',S.expand_power_base(B0*(Xv*Y/Xref)**power,force=True)-B0*(Xv/Xref)**power*Y**power)
result=dict(mutated=a.mutate,passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,scope='exact radial identities and classical rescaling; leading weak-potential screened force; not a global star/horizon or microscopic solution')
Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
