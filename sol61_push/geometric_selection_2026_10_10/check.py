"""Finite audit of a static counterfamily; not a relativistic galaxy solver."""
import json, math, pathlib, sys

eps = 1e-3
source_radius = .01
source_mass = 1e-3

def primitive(x):
    return x**3/3-4*x**5/5+6*x**7/7-4*x**9/9+x**11/11

def enclosed(r):
    return source_mass * primitive(min(r/source_radius, 1.)) / primitive(1.)

def force(y, a):
    b = y*y-eps*eps*a*a
    root = math.hypot(b, 2*a*y)
    z = (b+root)/2 if b >= 0 else 2*a*a*y*y/(root-b)
    return math.sqrt(z)

def mu(g, a):
    return math.sqrt((g*g+eps*eps*a*a)/(g*g+a*a))

checks=[]
rows=[]
for gamma in (2., math.sqrt(32*math.pi/3), 10.):
    a=1/gamma  # G=c=L=1, Lambda=3, rho_DE=3/(8*pi)
    worst=0.
    eigmin=1.
    eigmax=0.
    for k in range(241):
        r=10**(-14+14*k/240)
        y=enclosed(r)/r**2
        g=force(y,a)
        m=mu(g,a)
        radial=m+(1-eps*eps)*a*a*g*g/(m*(g*g+a*a)**2)
        worst=max(worst, abs(m*g/y-1))
        eigmin=min(eigmin,m,radial)
        eigmax=max(eigmax,m,radial)
    checks.extend([worst<1e-12,eigmin>=eps*(1-1e-12),eigmax<=2])
    y=enclosed(1e-14)/1e-28
    center=eps*force(y,a)/y
    checks.append(abs(center-1)<1e-6)
    checks.append(abs(mu(1000*a,a)-1)<1e-6)
    g=.05*a
    checks.append(abs(mu(g,a)*a/g-1)<.002)
    kappa=a/math.sqrt(3/(8*math.pi))
    rows.append(dict(gamma=gamma,a=a,kappa=kappa,C=3*gamma*gamma,
                     max_flux_relative_error=worst,min_static_eigenvalue=eigmin,
                     max_static_eigenvalue=eigmax,center_limit_ratio=center))
checks.append(math.isclose(rows[1]['kappa'],.5,rel_tol=1e-14))
checks.append(all(abs(rows[i]['kappa']-.5)>.1 for i in (0,2)))
out=dict(passed=sum(checks),count=len(checks),rows=rows,
         source=dict(mass=source_mass,radius=source_radius,
                     density_shape='(1-r^2/R^2)^4 for r<R, zero outside'),
         scope='Static spherical algebra and regularity; boundary value constructed analytically; no relativistic matching or cold substance prediction.')
pathlib.Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
sys.exit(0 if all(checks) else 1)
