"""Reduced reciprocal field model: exact identities and bounded diagnostics."""
import argparse,json
from pathlib import Path
import sympy as s
import numpy as np
from scipy.integrate import solve_ivp

pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);pa.add_argument('--mutate',action='store_true');args=pa.parse_args()
checks=[]
def ck(name,ok,value):
    checks.append(dict(name=name,passed=bool(ok),value=str(value)))
    print(('PASS ' if ok else 'FAIL ')+name+': '+str(value))

rho,MX,DX,chi,g,k,w=s.symbols('rho MX DX chi g k w',positive=True)
mat=s.Matrix([[-rho*w**2,-s.I*g*k*w],[s.I*g*k*w,chi+DX*k*k-MX*w*w]])
target=w*w*(rho*MX*w*w-rho*(chi+DX*k*k)-g*g*k*k)
ck('reciprocal_transverse_spectrum',s.simplify(mat.det()-target)==0,s.factor(mat.det()))
kv=s.Matrix(s.symbols('kx ky kz'));long=s.symbols('long')
ck('scalar_source_zero',kv.cross(long*kv)==s.zeros(3,1),kv.cross(long*kv))

# Reconstruct the circular Euler-Poincare one-form equation in Cartesian space.
x=s.symbols('x',positive=True);y=s.symbols('y',real=True);p,V=s.symbols('p V',real=True)
r=s.sqrt(x*x+y*y)
vb=s.Matrix([-V*y*r**(p-1),V*x*r**(p-1)])
Xz=g*V*(p+1)*r**(p-1)/chi
Q=s.Matrix([g*s.diff(Xz,y)/rho,-g*s.diff(Xz,x)/rho])
mom=vb+(s.zeros(2,1) if args.mutate else Q)
coords=[x,y]
lie=sum(vb[j]*s.diff(mom[0],coords[j])+mom[j]*s.diff(vb[j],x) for j in range(2))
force=s.simplify((s.diff(vb.dot(vb)/2,x)-lie).subs(y,0))
expected=V*V*x**(2*p-1)*(1+g*g*(1-p)**2*(1+p)/(rho*chi*x*x))
ck('circular_material_variation',s.simplify(force-expected)==0,force)
flat=s.simplify(force.subs(p,0)/(V*V/x))
ck('flat_curve_backreaction',s.simplify(flat-(1+g*g/(rho*chi*x*x)))==0,flat)
ck('rigid_rotation_limit',s.simplify((force- V*V*x**(2*p-1)).subs(p,1))==0,'p=1')
ck('zero_vorticity_limit',s.simplify((force- V*V*x**(2*p-1)).subs(p,-1))==0,'p=-1')

# Static phase minimum and spherical comparison algebra.
e,mu,chi0,h=s.symbols('e mu chi0 h',positive=True)
phase=mu**2*(chi-chi0)-e*e/(2*chi*chi)
ck('passive_phase_equilibrium',s.simplify(phase.subs(e,chi*h).subs(chi,chi0+h*h/(2*mu*mu)))==0,chi0+h*h/(2*mu*mu))
xx=s.symbols('xx',positive=True);phi=s.sin(xx)/xx
ck('comparison_eigenfunction',s.simplify(s.diff(xx*xx*s.diff(phi,xx),xx)+xx*xx*phi)==0,
   s.simplify((xx*xx*s.diff(phi,xx)).subs(xx,s.pi)))

fb=1/6.364;fc=1-fb
N0=-np.log(1101.)
def grow(ell,kval,tol,method):
    def fun(N,Y):
        a=np.exp(N);S=1/(1+(kval*ell/a)**2)
        b,bp,c,cp=Y
        return [bp,-.5*bp+1.5*(fb*b+fc*c),cp,-.5*cp+1.5*(fb*b+fc*S*c)]
    ai=np.exp(N0)
    sol=solve_ivp(fun,(N0,0),[ai,ai,ai,ai],rtol=tol,atol=tol*1e-4,method=method)
    assert sol.success
    b,bp,c,cp=sol.y[:,-1]
    return dict(total=float(fb*b+fc*c),baryon=float(b),cold=float(c),growth_rate=float((fb*bp+fc*cp)/(fb*b+fc*c)))
growth=[]
for ell in [0.,.0004404221297174536,.13378724636959235]:
    for kval in [.01,.1,1.]:
        a=grow(ell,kval,1e-9,'RK45');b=grow(ell,kval,1e-11,'DOP853')
        err=max(abs(a[key]-b[key]) for key in a)
        ck(f'growth_convergence_{ell}_{kval}',err<1e-7,err)
        growth.append(dict(ell_Mpc=ell,k_com_Mpc_inverse=kval,**b))
ck('dust_growth',all(abs(row['total']-1)<1e-9 for row in growth if row['ell_Mpc']==0),growth[:3])

def radial(sc,lam,bmass,tol,method):
    eps=1e-7
    B0=3*bmass
    d0=(B0+(0 if args.mutate else sc+lam*sc**3))/3
    s0=sc-(2/3)*np.sqrt(d0)*eps**1.5-d0*eps**2/4
    def fun(x,Y):
        q,ss=Y;z=max(q,0.)/(x*x)
        acc=(z+np.sqrt(z*z+4*z))/2
        B=3*bmass/(1+x*x)**2.5
        return [x*x*(B+(0 if args.mutate else ss+lam*ss**3)),-acc]
    def end(x,Y):return Y[1]
    end.terminal=True;end.direction=-1
    sol=solve_ivp(fun,(eps,1.1*np.pi),[d0*eps**3,s0],events=end,method=method,rtol=tol,atol=tol*1e-6,max_step=.02)
    assert sol.success,(sc,lam,bmass,sol.message)
    return float(sol.t_events[0][0]) if len(sol.t_events[0])==1 else None
radial_rows=[]
for sc in [.01,.1,1.,10.,100.]:
    for lam in [0.,1.]:
        for bmass in [0.,1.]:
            r1=radial(sc,lam,bmass,1e-8,'RK45');r2=radial(sc,lam,bmass,1e-10,'DOP853')
            radial_rows.append(dict(central_h=sc,lambda_phase=lam,baryon_mass=bmass,zero_radius_over_ell0=r2,relative_difference=abs(r1-r2)/r2 if r1 is not None and r2 is not None else None))
valid=[r for r in radial_rows if r['relative_difference'] is not None]
maxdiff=max((r['relative_difference'] for r in valid),default=None)
ck('radial_convergence_20',len(valid)==20 and maxdiff<1e-5,dict(count=len(valid),maxdiff=maxdiff))
ck('radial_analytic_bound_20',all(r['zero_radius_over_ell0'] is not None and r['zero_radius_over_ell0']<np.pi for r in radial_rows),max((r['zero_radius_over_ell0'] for r in valid),default=None))
# Removing the restoring density is a genuinely different equation: with B=0,
# Q'=0 and Q(0)=0 imply s'=0, so no finite first zero. Check it cannot masquerade
# as the model tested by the radial comparison argument.
ck('restoring_density_required',all(r['zero_radius_over_ell0'] is not None for r in radial_rows if r['baryon_mass']==0),'zero-source branches have a finite first zero')

out=dict(status='checks_passed' if all(c['passed'] for c in checks) else 'checks_failed',
         checks=checks,growth=growth,radial=radial_rows,
         surplus_radius_upper_pc=float(np.pi*440.4221297174536),
         non_claims=['No covariant completion','No data likelihood','No uniquely selected cold mass',
                    'Radial bound is on positive mismatch density, not total cold density or lensing radius'])
path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(out,indent=2)+'\n')
print(f"CHECKS {sum(c['passed'] for c in checks)}/{len(checks)}")
raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
