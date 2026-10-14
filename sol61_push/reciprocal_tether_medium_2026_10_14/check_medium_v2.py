"""RTM-001: bounded local current-rest-frame construction; no external data."""
import json
from pathlib import Path
import sys
import numpy as np
import sympy as sp
from scipy.optimize import brentq

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=False)
checks = []


def check(name, condition):
    checks.append({'name': name, 'pass': bool(condition)})
    if not condition:
        raise AssertionError(name)


def exact(name, expression):
    check(name, sp.simplify(expression) == 0)


E, D0, D, a, u = sp.symbols('E D0 D a u', positive=True)
Le = D0*E-D0**2*sp.log(1+E/D0)
constitutive = D0*E/(D0+E)
exact('electric displacement', sp.diff(Le, E)-constitutive)
exact('electric differential susceptibility', sp.diff(Le, E, 2)-D0**2/(D0+E)**2)
Ei = D/(1-D/D0)
exact('inverse constitutive law', constitutive.subs(E, Ei)-D)
H = -D0*D-D0**2*sp.log(1-D/D0)
exact('Hamiltonian derivative', sp.diff(H, D)-Ei)
exact('force cancellation', -(sp.Symbol('gb')+u)+u/(1-u/a)-(-sp.Symbol('gb')+u**2/(a-u)))

# Boost expansion with E_lab=E z + lambda e, B_lab=lambda b, v=lambda v.
# Expand the squared norm before taking its square root. This avoids an
# expensive generic covariant tensor simplification and retains all recoil.
lam = sp.Symbol('lam')
ex, ey, ez, bx, by, bz, vx, vy, vz, beta, h = sp.symbols('ex ey ez bx by bz vx vy vz beta h', real=True)
ev = sp.Matrix([lam*ex, lam*ey, E+lam*ez])
bv = lam*sp.Matrix([bx, by, bz]); vv = lam*sp.Matrix([vx, vy, vz])
restE2 = ((ev+vv.cross(bv)).dot(ev+vv.cross(bv))-(ev.dot(vv))**2)/(1-vv.dot(vv))
q2 = sp.series(restE2, lam, 0, 3).removeO().expand().coeff(lam, 2)
expected = ex**2+ey**2+ez**2+2*E*(vx*by-vy*bx)+E**2*(vx**2+vy**2)
exact('covariant electric boost to quadratic order', q2-expected)
restB2 = q2-(ex**2+ey**2+ez**2)+(bx**2+by**2+bz**2)
exact('magnetic boost from invariant', restB2-((bx-E*vy)**2+(by+E*vx)**2+bz**2))
t, p = sp.symbols('t p', positive=True)
boostL = t*(q2-ez**2)/2+p*ez**2/2-beta*restB2/2
expectedL = t*(ex**2+ey**2)/2+p*ez**2/2-beta*(bx**2+by**2+bz**2)/2+(t-beta)*E*(vx*by-vy*bx)+(t-beta)*E**2*(vx**2+vy**2)/2
exact('reciprocal quadratic medium action', boostL-expectedL)
he = sp.Symbol('he', positive=True)
hc = E**2*t*(t-p)/p
bL = p*(he-hc)/(he-E**2*(t-p))
gap = p-beta-E**2*(t-beta)**2/(he+E**2*(t-beta))
exact('luminal threshold', gap.subs(beta, bL))
exact('threshold is strict monotone in beta', sp.diff(gap, beta)+he**2/(he+E**2*(t-beta))**2)
R, x = sp.symbols('R x', positive=True)
blxr = sp.factor(bL.subs(he, R*hc).subs(p, t**2).subs(t, 1-x))
exact('threshold positive expression', blxr-(1-x)**2*(R-1)/(R-(1-x)))
exact('old Lorentz-scalar cone', (t/p).subs(p, t**2).subs(t, 1-x)-1/(1-x))
exact('frozen beta p still supermetric', (p+E**2*(t-p)**2/(h+E**2*(t-p)))/p-1-E**2*(t-p)**2/(p*(h+E**2*(t-p))))


def matrices(x, ratio, s2, theta):
    e=x/(1-x); t=1-x; p=t*t
    hc=e*e*t*(t-p)/p; h=ratio*hc/(1-s2)
    bL=p*(h*(1-s2)-hc)/(h*(1-s2)-e*e*(t-p))
    beta=bL*ratio/(ratio+1); delta=t-beta
    mass=np.diag([h+e*e*delta, h+e*e*delta, h])
    eps=np.diag([t,t,p])
    k=np.array([np.sin(theta),0.,np.cos(theta)])
    T=np.array([[0.,np.cos(theta)],[1.,0.],[0.,-np.sin(theta)]])
    ek=eps@k
    ka=T.T@(eps-np.outer(ek,ek)/(k@eps@k))@T
    B=np.column_stack([np.cross(k,T[:,i]) for i in range(2)])
    mix=e*delta*np.array([B[1],-B[0],np.zeros(2)])
    pressure=h*s2*np.outer(k,k)
    kin=np.zeros((5,5)); kin[:2,:2]=ka; kin[2:,2:]=mass
    pot=np.zeros((5,5)); pot[:2,:2]=beta*np.eye(2); pot[2:,2:]=pressure
    gyro=np.zeros((5,5)); gyro[:2,2:]=-mix.T; gyro[2:,:2]=mix
    gen=np.block([[np.zeros((5,5)), np.eye(5)],[-np.linalg.solve(kin,pot),-np.linalg.solve(kin,gyro)]])
    vals=np.linalg.eigvals(gen)
    schur=ka-beta*np.eye(2)-mix.T@np.linalg.solve(mass-pressure,mix)
    return locals()


rows=[]; max_dust_error=0.; max_pressure_error=0.
for x0 in [.01,.1,.5,.9,.99]:
    for ratio in [1.01,2.,10.,1e3,1e6]:
        for s2 in [0.,1e-6,.001,.01,.1,1/3]:
            for theta in np.linspace(0,np.pi/2,9):
                v=matrices(x0,ratio,s2,theta)
                vals=v['vals']; speed=float(max(abs(vals.imag)))
                schur=float(np.linalg.eigvalsh(v['schur'])[0])
                kinetic=float(np.linalg.eigvalsh(v['kin'])[0])
                real=float(max(abs(vals.real)))
                check('grid %d kinetic/potential/schur/spectrum'%len(rows), kinetic>0 and np.linalg.eigvalsh(v['pot'])[0]/max(1.,np.linalg.norm(v['pot'],2))>-1e-14 and schur>0 and speed<=1+1e-7 and real<1e-6)
                # Independent closed-form dust dispersion, including both polarizations.
                if s2==0:
                    beff=v['beta']+v['e']**2*v['delta']**2/v['mass'][0,0]
                    expected=np.sqrt([beff*(np.cos(theta)**2/v['t']+np.sin(theta)**2/v['p']), (beff*np.cos(theta)**2+v['beta']*np.sin(theta)**2)/v['t']])
                    actual=np.sort(vals.imag[vals.imag>1e-7])
                    error=float(np.max(abs(actual-np.sort(expected))))
                    max_dust_error=max(max_dust_error,error)
                    check('dust dispersion %d'%len(rows),len(actual)==2 and error<1e-8)
                if abs(theta-np.pi/2)<1e-10:
                    # At perpendicular propagation one coupled pair obeys this quadratic.
                    p0=v['p']; b=v['beta']; M=v['mass'][0,0]; h0=v['h']; C=v['e']*v['delta']
                    roots=np.roots([p0*M,-(p0*h0*s2+b*M+C*C),b*h0*s2])
                    predicted=max(float(max(roots)),b/v['t'])
                    error=abs(speed**2-predicted); max_pressure_error=max(max_pressure_error,error)
                    check('perpendicular polynomial %d'%len(rows),error<1e-8)
                rows.append([x0,ratio,s2,float(theta),speed,real,schur,kinetic,v['beta']])
check('1350 grid backgrounds',len(rows)==1350)

# Domain check in SI. hcrit/c^2 is a mass density; h=rho c^2 for dust.
G=6.67430e-11; c=299792458.; a0=9.360324825e-11
pc=3.085677581491367e16; msun=1.98847e30
r, rm=sp.symbols('r rm',positive=True)
disc=sp.sqrt(1+4*r*r/rm**2); xx=2/(1+disc)
exact('point-source carrier density',2*xx/r+sp.diff(xx,r)-2/(r*disc))
exact('dimensionless critical enthalpy', (E**2*t*(t-p)/p).subs(p,t**2).subs(t,1-x).subs(E,x/(1-x))-x**3/(1-x)**2)


def point_ratio(radius, mass):
    rm=np.sqrt(G*mass/a0)
    d=np.sqrt(1+4*(radius/rm)**2)
    # Avoid cancellation of 1-x at tiny radii.
    x=2/(1+d); one_minus_x=4*(radius/rm)**2/(1+d)**2
    rho=a0/(2*np.pi*G*radius*d)
    crit=a0*a0/(4*np.pi*G*c*c)*x**3/one_minus_x**2
    return rho/crit


points=[]
for mass_solar in [4e6,6e10]:
    mass=mass_solar*msun; rm=np.sqrt(G*mass/a0); rg=2*G*mass/c**2
    asym=(G**2*mass**2/(2*a0*c*c))**(1/3)
    root=np.exp(brentq(lambda logr:np.log(point_ratio(np.exp(logr),mass)),np.log(asym/10),np.log(asym*10),xtol=1e-12))
    check('exact crossing %g'%mass_solar,abs(point_ratio(root,mass)-1)<1e-9)
    check('cubic gate identity %g'%mass_solar,abs(asym**3/(rg*rm**2/4)-1)<1e-12)
    check('asymptotic gate %g'%mass_solar,abs(root/asym-1)<1e-3)
    points.append(dict(mass_solar=mass_solar,rg_pc=rg/pc,rM_pc=rm/pc,crossing_pc=root/pc,asymptote_pc=asym/pc,ratio_at_rM=point_ratio(rm,mass)))

mass=6e10*msun; scale=3000*pc; profiles=[]
for radius in np.geomspace(.001*pc,1e6*pc,401):
    y=G*mass*radius/(radius**2+scale**2)**1.5/a0
    x=2/(1+np.sqrt(1+4/y))
    dy=y*(1/radius-3*radius/(radius**2+scale**2))
    dx=dy*(1-x)**2/(x*(2-x))
    rho=a0/(4*np.pi*G)*(2*x/radius+dx)
    crit=a0*a0/(4*np.pi*G*c*c)*x**3/(1-x)**2
    check('Plummer positive and admissible %d'%len(profiles),rho>crit>0)
    profiles.append([radius/pc,rho/crit])

np.savetxt(OUT/'modes.csv',np.array(rows),delimiter=',',header='x,R,sound_speed_squared,angle,max_speed,max_abs_real_eigenvalue,min_schur,min_kinetic,beta',comments='')
np.savetxt(OUT/'plummer.csv',np.array(profiles),delimiter=',',header='radius_pc,rho_over_critical',comments='')
result=dict(status='bounded assertions passed',checks=len(checks),grid_cases=len(rows),max_speed=max(row[4] for row in rows),max_abs_real_eigenvalue=max(row[5] for row in rows),min_schur=min(row[6] for row in rows),min_kinetic=min(row[7] for row in rows),max_dust_dispersion_error=max_dust_error,max_pressure_dispersion_error=max_pressure_error,point_sources=points,plummer_min_ratio=min(row[1] for row in profiles),interpretation='Constructed local pure-electric principal-action witness; no global matter, vacuum, cosmological or microscopic completion.')
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
