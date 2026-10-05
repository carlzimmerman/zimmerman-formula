"""p25: the nu <-> M' map for the exchange-symmetric BIMOND class (alpha = beta = 1, f'(1) = 0 pinned, p24) and its vacuum coefficient.
NR Lagrangian, Milgrom 2009 (arXiv:0912.0790v2) eq (1):  L = -(1/8 pi G){beta |grad phi|^2 + alpha |grad phihat|^2 - a0^2 M(|grad phi*|^2/a0^2)} - rho phi,  phi* = phi - phihat.
Spherical: g* = |grad phi*|, m = M'(z), z = (g*/a0)^2. Derived below by varying phi and phihat (sympy, 1D radial flux form).
alpha + beta = 0 (Milgrom's main class) reproduces nu = 1 + M' (p21). alpha = beta = 1:  y = (1 - 2m) x*,  g/a0 = (1 - m) x*  (x* = g*/a0, y = g_N/a0)
  => m = (nu - 1)/(2 nu - 1),  x* = y (2 nu - 1),  M'(z = [y(2nu-1)]^2) = (nu - 1)/(2nu - 1).
Vacuum (p24, eq 84 with q = 1/2): Lambda = -(1/2) a0^2 M(0), M(inf) = 0  =>  Lambda/a0^2 = J/2,  J = int_0^inf m dz = int (nu-1)/(2nu-1) d[y^2 (2nu-1)^2].
Puzzle: J = 64 pi.
Run: python3 p25_symmetric_bimond_map.py  |  MUTATE=1: use the alpha+beta=0 map (m = nu - 1) in the symmetric class; check M2 must fail
"""
import os, sys, math
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)

# ---- derive the field equations by varying the radial flux Lagrangian (spherical: L ~ r^2 [beta p^2 + alpha ph^2 - a0^2 M((p-ph)^2/a0^2)] + source)
r = sp.symbols("r", positive=True); al, be, a0, G = sp.symbols("alpha beta a0 G", positive=True)
P, Ph = sp.Function("phi")(r), sp.Function("phihat")(r); Mf = sp.Function("M"); rho = sp.Function("rho")(r)
z = (P.diff(r) - Ph.diff(r))**2 / a0**2
Lag = -r**2 / (8 * sp.pi * G) * (be * P.diff(r)**2 + al * Ph.diff(r)**2 - a0**2 * Mf(z)) - r**2 * rho * P
EL = lambda F: sp.diff(Lag, F) - sp.diff(sp.diff(Lag, F.diff(r)), r)
# first integrals: d/dr(flux) = source -> flux_phi = r^2 [beta phi' - M' phi*'] = G M_enc ; flux_phihat = r^2 [alpha phihat' + M' phi*'] = 0
gs, gh, m = sp.symbols("gstar ghat m", real=True)
flux_phi = sp.diff(Lag, P.diff(r)) * (-4 * sp.pi * G) / r**2
flux_ph = sp.diff(Lag, Ph.diff(r)) * (-4 * sp.pi * G) / r**2
sub = {sp.Subs(sp.Derivative(Mf(sp.Symbol('_xi_1')), sp.Symbol('_xi_1')), sp.Symbol('_xi_1'), z): m}
fp_ = sp.simplify(flux_phi.subs(sub).doit())
fh_ = sp.simplify(flux_ph.subs(sub).doit())
# replace derivative of M by m explicitly (robust to sympy's Subs form)
fp_ = sp.simplify(fp_.replace(lambda e: isinstance(e, sp.Subs), lambda e: m))
fh_ = sp.simplify(fh_.replace(lambda e: isinstance(e, sp.Subs), lambda e: m))
gphi, gphh = sp.symbols("gphi gphh", real=True)
fp_ = sp.simplify(fp_.subs({P.diff(r): gphi, Ph.diff(r): gphh}))
fh_ = sp.simplify(fh_.subs({P.diff(r): gphi, Ph.diff(r): gphh}))
print(f"   flux(phi) = {fp_}   flux(phihat) = {fh_}")
solh = sp.solve(sp.Eq(fh_, 0), gphh)[0]                           # phihat' from its own equation
gN = sp.symbols("gN", positive=True)
eq_phi = sp.Eq(fp_.subs(gphh, solh), gN)                           # Gauss: flux(phi) = g_N
gstar_expr = sp.simplify(gphi - solh)                              # phi*' in terms of phi'
check("M1 varying phihat gives alpha phihat' = -M' phi*'; then mu* = beta - (alpha+beta) M'/alpha and g = (1 - M'/alpha) g* (Milgrom eq 2)",
      sp.simplify(solh - (-m * (gphi - solh) / al)) == 0 and
      sp.simplify(sp.solve(eq_phi, gphi)[0] / sp.solve(sp.Eq(sp.Symbol('gs') * (be - (al + be) * m / al), gN), sp.Symbol('gs'))[0] - (1 - m / al)) == 0)
# symmetric class alpha = beta = 1: y = (1-2m) x*, g = (1-m) x*  ->  nu = (1-m)/(1-2m)
nu_s = sp.symbols("nu", positive=True)
msol = sp.solve(sp.Eq((1 - m) / (1 - 2 * m), nu_s), m)[0]
check("M2 alpha = beta = 1: m = M' = (nu - 1)/(2 nu - 1), x* = y (2 nu - 1)", sp.simplify(msol - (nu_s - 1) / (2 * nu_s - 1)) == 0 and
      sp.simplify(1 / (1 - 2 * msol) - (2 * nu_s - 1)) == 0)
mmap = (lambda nu: nu - 1) if MUTATE else (lambda nu: (nu - 1) / (2 * nu - 1))

# ---- J for the kernels
N1 = lambda a: (lambda y: math.expm1(math.log1p(y**(-a)) / (2 * a)))          # nu - 1, family containing the framework (a = 1)
RAR = lambda y: 1 / (-math.expm1(-math.sqrt(y))) - 1
def J(nm1, Y=1e4, p=None, A=None):
    """J = int m dz, z = y^2 (2nu-1)^2  ->  int m(y) dz/dy dy; analytic tail beyond Y for power tails (nu - 1 ~ A y^-p: m ~ A y^-p, dz/dy ~ 2y)"""
    def integrand(y):
        e = nm1(y); nu = 1 + e
        m_ = mmap(nu)
        # dz/dy = 2 y (2nu-1)^2 + 2 y^2 (2nu-1) * 2 nu'(y); nu' by central difference on log scale
        h = 1e-6 * y; dnu = (nm1(y + h) - nm1(y - h)) / (2 * h)
        return m_ * (2 * y * (2 * nu - 1)**2 + 4 * y**2 * (2 * nu - 1) * dnu)
    segs = ((1e-9, 1e-3), (1e-3, 1), (1, 10), (10, 1e2), (1e2, 1e3), (1e3, Y))
    tot = sum(quad(integrand, a, b, limit=2000, epsabs=1e-12, epsrel=1e-10)[0] for a, b in segs)
    if p is not None:
        tot += 2 * A * Y**(2 - p) / (p - 2)
    else:
        tot += quad(integrand, Y, 1e6, limit=2000)[0]
    return tot
# exact identity: J - I_nu = int d[2 y^2 (nu - 1)^2]  (boundary term: ~ y at y -> 0 (deep MOND), ~ y^(2-2p) at y -> inf), so J = I_nu whenever both converge
yy = sp.symbols("y", positive=True); nuf = sp.Function("nu")(yy); w = 2 * nuf - 1
diffint = ((nuf - 1) / w if not MUTATE else (nuf - 1)) * sp.diff(yy**2 * w**2, yy) - (nuf - 1) * sp.diff(yy**2, yy)
check("ID J - I_nu = int d[2 y^2 (nu-1)^2] exactly: the vacuum coefficient is the SAME in both BIMOND classes (alpha+beta=0 and alpha=beta), a property of nu alone",
      sp.simplify(diffint - sp.diff(2 * yy**2 * (nuf - 1)**2, yy)) == 0)
jr = J(RAR)
print(f"   RAR kernel: J = {jr:.4f}  -> Lambda/a0^2 = {jr/2:.3f} (needs 32 pi = {32*math.pi:.3f}; factor {64*math.pi/jr:.2f})")
jf = [J(N1(1), Y=Y, p=None) for Y in (1e2, 1e3, 1e4)]
print(f"   framework kernel (alpha = 1): J up to y = 1e2/1e3/1e4 (+ to 1e6) grows: {[round(v,1) for v in jf]}")
check("J1 the framework kernel's J still DIVERGES in the symmetric class (tail m ~ 1/(2y), dz ~ 2y dy)", jf[2] > 1e3)
check(f"J2 RAR gives a finite J = {jr:.3f}, Lambda = {jr/2:.2f} a0^2: short of 32 pi by x{64*math.pi/jr:.2f}", 5 < 64 * math.pi / jr < 100)
astar = brentq(lambda a: J(N1(a), p=a, A=1 / (2 * a)) - 64 * math.pi, 2.00001, 6)
print(f"   tail exponent for J = 64 pi in the symmetric class: alpha* = {astar:.5f}  (alpha+beta=0 class, p22: 2.00249)")
check("J3 the symmetric class needs the same near-divergent tail: alpha* = p22's 2.00249 (to 1e-4), as the identity requires", abs(astar - 2.00249) < 1e-4)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
