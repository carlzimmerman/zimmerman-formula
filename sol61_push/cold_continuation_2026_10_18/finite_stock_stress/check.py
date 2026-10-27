"""Small exact/finite checks of the mass-coordinate finite-stock comparison.

No source evolution, mesh search, spectral scan or population simulation.
The report contains the uniform proof; quadrature only checks one dilation.
"""
import json
import platform
import sys
from pathlib import Path
import mpmath as mp
import sympy as sp

checks = []
def check(name, ok, detail=None):
    checks.append({"name": name, "passed": bool(ok), "detail": detail})
    if not ok:
        raise AssertionError(name)

r = sp.symbols("r", positive=True)
beta = sp.symbols("beta", positive=True)
m = sp.Function("m")(r)
u = m/r**2
rho = sp.diff(m, r)/(4*sp.pi*r**2)
lap = sp.diff(u, r, 2)+2*sp.diff(u, r)/r-2*u/r**2
check("vector stiffness equals local density energy plus endpoint derivative",
      sp.simplify(r**2*sp.diff(u,r)**2+2*u**2
                  -sp.diff(m,r)**2/r**2+2*sp.diff(m**2/r**3,r)) == 0)
check("vector Laplacian is 4pi density derivative",
      sp.simplify(lap-4*sp.pi*sp.diff(rho,r)) == 0)
z = sp.symbols("z", positive=True)
e = 2*sp.pi*beta*z**2
pressure = sp.simplify(z*sp.diff(e,z)-e)
check("positive quadratic pressure", pressure == 2*sp.pi*beta*z**2)
check("sound derivative", sp.diff(pressure,z) == 4*sp.pi*beta*z)

M = r**3*(5-3*r**2)/20
U = sp.cancel(M/r**2)
D = sp.diff(M,r)
RH = sp.simplify(D/(4*sp.pi*r**2))
RR = lambda t: t**2/(1-t)
QP = sp.cancel(r**2*RR(U)+sp.Rational(3,2)*r**3)
Qe = sp.simplify(QP.subs(r,1))
check("exact stock", M.subs(r,1) == sp.Rational(1,10))
check("exact density", sp.simplify(RH-3*(1-r**2)/(16*sp.pi)) == 0)
check("zero edge density and mass derivative", RH.subs(r,1) == 0 and D.subs(r,1) == 0)
check("regular center", sp.limit(M/r**3,r,0) == sp.Rational(1,4))
check("field derivative matches vacuum tail",
      sp.diff(U,r).subs(r,1) == -sp.Rational(1,5))
check("occupied Euler equation",
      sp.simplify(RR(U)-QP/r**2-4*sp.pi*sp.diff(RH,r)) == 0)
check("external total", Qe == sp.Rational(68,45))
u_max = sp.sqrt(5)/18
check("uniform constitutive-domain bound", u_max < sp.Rational(1,8))
check("monotonic-source lower-bound arithmetic",
      sp.Rational(9,2)-sp.Rational(3,49) == sp.Rational(435,98))
S = sp.Rational(1,10)
check("strict exterior-force gap at edge",
      sp.simplify(S*S/(1-S)-Qe) == -sp.Rational(3,2))
xi = r
eta = -D*xi
du = eta/r**2
I = sp.integrate(D*xi**2,(r,0,1))
Hbeta = sp.integrate(r**2*sp.diff(du,r)**2+2*du**2,(r,0,1))
Ebeta = sp.integrate(D**2/(2*r**2),(r,0,1))
check("dilation material inertia", I == sp.Rational(3,70))
check("Eulerian mass Hessian gradient contribution", Hbeta == sp.Rational(9,28))
check("internal energy integral", Ebeta == sp.Rational(3,140))
check("Hessian edge-displacement condition",
      sp.limit(eta/D,r,1,dir="-") == -1)

mp.mp.dps = 60
stock = mp.mpf(1)/10
qedge = mp.mpf(68)/45
def mm(x):
    return x**3*(5-3*x*x)/20 if x < 1 else stock
def qq(x):
    if x >= 1:
        return qedge
    vv = x*(5-3*x*x)/20
    return x*x*vv*vv/(1-vv)+mp.mpf(3)/2*x**3
def ww(v):
    if abs(v) < mp.mpf(".01"):
        return mp.fsum(v**j/j for j in range(3,40))
    return -v*v/2-v-mp.log1p(-v)
def energy(lam):
    def f(x):
        if x == 0:
            return mp.mpf(0)
        if x == 1:
            return -qedge*stock
        rad = x/(1-x)
        mass = mm(rad/lam)
        val = rad*rad*ww(mass/(rad*rad))-qq(rad)*mass/(rad*rad)
        return val/(1-x)**2
    breaks = sorted(set([mp.mpf(0),mp.mpf(".5"),lam/(1+lam),mp.mpf(1)]))
    return mp.quad(f,breaks)+mp.mpf(3)/140/lam**3
def hessian_integrand(x):
    v = x*(5-3*x*x)/20
    q = -mp.mpf(3)/4*x*(1-x*x)
    qprime = -mp.mpf(3)/4+mp.mpf(9)/4*x*x
    rp = v*(2-v)/(1-v)**2
    return x*x*rp*q*q+x*x*qprime*qprime+2*q*q
H = mp.quad(hessian_integrand,[0,1])
E1 = energy(mp.mpf(1))
rows = []
for eps in [mp.mpf(".001"),mp.mpf(".0005"),mp.mpf(".00025")]:
    ep, em = energy(1+eps), energy(1-eps)
    first = (ep-em)/(2*eps)
    second = (ep-2*E1+em)/(eps*eps)
    check("finite dilation first variation eps="+str(eps),abs(first)<mp.mpf("2e-6"),mp.nstr(first,20))
    check("finite dilation second variation eps="+str(eps),abs(second-H)<mp.mpf("3e-6"),mp.nstr(second-H,20))
    rows.append({"epsilon":str(eps),"symmetric_first":mp.nstr(first,35),
                 "symmetric_second":mp.nstr(second,35),"hessian_error":mp.nstr(second-H,35)})
check("strict positive radial Rayleigh witness",H>0)
result = {
    "checks": checks,
    "count": len(checks),
    "python": platform.python_version(),
    "sympy": sp.__version__,
    "mpmath": mp.__version__,
    "precision_decimal_digits": mp.mp.dps,
    "exact": {"stock":"1/10","outer_radius":"1","external_total":"68/45",
              "material_dilation_inertia":"3/70","gradient_mass_hessian":"9/28"},
    "dilation_hessian":mp.nstr(H,45),
    "dilation_rayleigh_frequency_squared":mp.nstr(H/(mp.mpf(3)/70),45),
    "finite_dilations": rows,
    "scope":"Exact identities plus three finite dilation checks of one manufactured radial fixed-source equilibrium; no universal stability/physical carrier/covariant claim."
}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"checks":len(checks),"hessian":result["dilation_hessian"],"finite_dilations":rows},indent=2))
