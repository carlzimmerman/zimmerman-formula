"""g03: Noether / trace analysis.  Vacuum:  T^mu_mu = -4 rho_Lambda.   Deep-MOND field:  spatial trace 0, four-trace -u.

Setup (G = c = 1 where needed).  Static AQUAL field: L = -(a0^2/(8 pi G)) F(y) - rho phi,  y = |grad phi|^2/a0^2,  mu = F'(y).
Canonical stress with the sign convention T^{00} = +energy density:
    T^{ij} = (1/(4 pi G)) mu phi_i phi_j - delta_ij (a0^2/(8 pi G)) F ,     T^{00} = u = (a0^2/(8 pi G)) F.
Checks
 A  force balance d_j T^{ij} = rho d_i phi on shell (validates the tensor and its signs), symbolic, generic F and generic phi (d=3).
 B  spatial trace T^i_i = (a0^2/(8 pi G)) (2 y F' - d F)  (d spatial dims; F' = mu):  ZERO iff F = y^{d/2}: deep MOND in d = 3 is
    F = (2/3) y^{3/2} (traceless); Newton F = y gives -g^2/(8 pi G) != 0 (first draft of this script had the sign wrong: caught by check B2).  All d = 2..6 (scale invariance of int |grad phi|^d).
 C  four-trace: T^mu_mu = -u + T^i_i : deep MOND -> -u (negative).  Vacuum T^mu_mu = -4 rho_Lambda (negative).  Both negative:
    a dilatation-restoring cancellation (T_total = 0) is impossible with positive-energy MOND field + positive vacuum.
 D  the scale (dilatation) current D^mu = x_nu T^{mu nu}: d_mu D^mu = T^mu_mu.  The vacuum breaks it by 4 rho_Lambda.  A deep-MOND
    field does not (spatial).  The Ward identity relates each sector to ITSELF: no amplitude relation between the sectors.
 E  the finite scale-charge FLUX at infinity of a point mass reproduces Milgrom's exact deep-MOND virial coefficient (2/3) sqrt(G a0) M^{3/2}:
    the dilatation Noether charge is where the M^{3/2} lives; nothing in it involves rho_Lambda.
 F  ratio bookkeeping: rho_Lambda / (a0^2/(8 pi G)) = 32 pi (pi present) ; rho_Lambda G / a0^2 = 4 (algebraic).  The stress scale that the
    a0-sector itself supplies (field energy of a field of strength a0, pressure of a deep-MOND field at g = a0) carries the 1/(8 pi G) or 1/(4 pi G)
    of the Poisson normalisation, which is a COUPLING normalisation (not fixed by dilatation invariance).
"""
import sympy as sp, mpmath as mp, sys
ok = []
def chk(n, c):
    ok.append(bool(c)); print(("PASS " if c else "FAIL ") + n)

G, a0 = sp.symbols('G a0', positive=True)

# ---------------- A: force balance with generic phi, F = generic function of y (d = 3)
x, y, z = sp.symbols('x y z', real=True)
X = (x, y, z)
phi = sp.Function('phi')(*X)
Fy = sp.Function('F'); Fp = sp.Function('Fp')      # F and F' treated via chain rule below
yv = sum(sp.diff(phi, v)**2 for v in X) / a0**2
Fe = Fy(yv)
mu = sp.diff(Fy(sp.Symbol('t')), sp.Symbol('t')).subs(sp.Symbol('t'), yv)
Tij = lambda i, j: (1 / (4 * sp.pi * G)) * mu * sp.diff(phi, X[i]) * sp.diff(phi, X[j]) - (1 if i == j else 0) * (a0**2 / (8 * sp.pi * G)) * Fe
div = [sum(sp.diff(Tij(i, j), X[j]) for j in range(3)) for i in range(3)]
fieldeq = sum(sp.diff((1 / (4 * sp.pi * G)) * mu * sp.diff(phi, v), v) for v in X)        # = rho on shell
resid = [sp.simplify((div[i] - fieldeq * sp.diff(phi, X[i])).doit()) for i in range(3)]
chk("A1 d_j T^{ij} = (div((1/4 pi G) mu grad phi)) d_i phi  identically (=> = rho d_i phi on shell): generic F, generic phi", all(r == 0 for r in resid))
# control: flip the sign of the F term -> identity must fail
Tbad = lambda i, j: (1 / (4 * sp.pi * G)) * mu * sp.diff(phi, X[i]) * sp.diff(phi, X[j]) + (1 if i == j else 0) * (a0**2 / (8 * sp.pi * G)) * Fe
divb = [sum(sp.diff(Tbad(i, j), X[j]) for j in range(3)) for i in range(3)]
residb = sp.simplify((divb[0] - fieldeq * sp.diff(phi, X[0])).doit())
chk("A2 control: with the wrong sign on the F term the force balance FAILS", residb != 0)

# ---------------- B: traces in d dimensions for F = y^p
def trace_coeff(dim, p):
    gs = sp.symbols('g0:%d' % dim, real=True)
    ysym = sum(g**2 for g in gs) / a0**2
    F = ysym**p
    mu_ = p * ysym**(p - 1)
    tr = sum((1 / (4 * sp.pi * G)) * mu_ * gs[i]**2 - (a0**2 / (8 * sp.pi * G)) * F for i in range(dim))
    return sp.simplify(tr)
allzero = True; allnonzero_ctrl = True
for dim in range(2, 7):
    t_scale = trace_coeff(dim, sp.Rational(dim, 2))
    t_newt = trace_coeff(dim, 1)
    allzero = allzero and (t_scale == 0)
    allnonzero_ctrl = allnonzero_ctrl and (t_newt != 0 if dim != 2 else True)
chk("B1 T^i_i = 0 identically for F = y^{d/2} in d = 2,3,4,5,6 (deep-MOND-type scale-invariant field)", allzero)
t3_newt = trace_coeff(3, 1)
chk("B2 Newton (F = y), d = 3: T^i_i = -g^2/(8 pi G) != 0 (scale invariance broken)", sp.simplify(t3_newt + sum(sp.symbols('g0:3', real=True)[i]**2 for i in range(3)) / (8 * sp.pi * G)) == 0)
chk("B3 control: exponent p = 1.4 in d = 3 is NOT traceless", trace_coeff(3, sp.Rational(7, 5)) != 0)
chk("B4 for d = 2 Newton (F = y = y^{d/2}) IS traceless (the 2-D Laplacian is conformally invariant): control that the criterion is p = d/2, not 'p = 3/2'", trace_coeff(2, 1) == 0)

# ---------------- C: four-trace signs
g = sp.symbols('g', positive=True)
yD = g**2 / a0**2
FD = sp.Rational(2, 3) * yD**sp.Rational(3, 2)
muD = sp.diff(sp.Rational(2, 3) * sp.Symbol('t')**sp.Rational(3, 2), sp.Symbol('t')).subs(sp.Symbol('t'), yD)
u = (a0**2 / (8 * sp.pi * G)) * FD
Trr = (1 / (4 * sp.pi * G)) * muD * g**2 - (a0**2 / (8 * sp.pi * G)) * FD           # radial component
Tperp = -(a0**2 / (8 * sp.pi * G)) * FD                                              # transverse components (phi_i phi_j has no perp part)
tr3 = sp.simplify(Trr + 2 * Tperp)
chk("C1 deep MOND (radial field): T^r_r + 2 T^perp = 0 and u = g^3/(12 pi G a0)", tr3 == 0 and sp.simplify(u - g**3 / (12 * sp.pi * G * a0)) == 0)
T4 = sp.simplify(-u + tr3)
chk("C2 four-trace T^mu_mu(deep MOND) = -u = -g^3/(12 pi G a0) < 0", sp.simplify(T4 + g**3 / (12 * sp.pi * G * a0)) == 0)
rho_L = sp.symbols('rho_L', positive=True)
eta = sp.diag(-1, 1, 1, 1)
Tmn = -rho_L * eta
tr_vac = sum((eta.inv() * Tmn)[i, i] for i in range(4))
chk("C3 vacuum T_{mu nu} = -rho_Lambda g_{mu nu}: T^mu_mu = -4 rho_Lambda; p = -rho", sp.simplify(tr_vac + 4 * rho_L) == 0)
chk("C4 both traces are negative for any positive u and rho_Lambda: T_total^mu_mu = 0 (dilatation restoration by cancellation) is impossible with a positive-energy deep-MOND field",
    sp.simplify(T4 + tr_vac).subs({g: 1, a0: 1, G: 1, rho_L: sp.Rational(1, 3)}) < 0)
# a component that COULD cancel -4 rho needs T^i_i > u, i.e. w > 1/3 (stiff): equation-of-state bookkeeping
w = sp.symbols('w')
chk("C5 a fluid with T^mu_mu > 0 needs w > 1/3 (T = -rho + 3 p = rho (3w - 1)); the deep-MOND field has effective w = T^i_i/(3u) = 0 (dust-like on average)", sp.simplify(tr3 / (3 * u)) == 0)

# ---------------- D: scale current  d_mu D^mu = T^mu_mu  (check for a static field: d_i(x_j T^{ij}) = T^i_i + x_j d_i T^{ij})
xs = sp.Matrix([x, y, z])
Tm = sp.Matrix(3, 3, lambda i, j: Tij(i, j))
Dcur = [sum(xs[j] * Tm[i, j] for j in range(3)) for i in range(3)]
divD = sum(sp.diff(Dcur[i], X[i]) for i in range(3))
trace3 = sum(Tm[i, i] for i in range(3))
force = sum(xs[i] * div[i] for i in range(3))
chk("D1 d_i(x_j T^{ij}) = T^i_i + x_j d_i T^{ij}  (Noether identity for the spatial scale current; T^i_i = 0 for deep MOND)", sp.simplify((divD - trace3 - force).doit()) == 0)

# ---------------- E: dilatation-charge flux of a point mass = Milgrom's virial coefficient
M = sp.symbols('M', positive=True)
gr = sp.sqrt(G * M * a0) / sp.Symbol('r', positive=True)
r = sp.Symbol('r', positive=True)
yr = gr**2 / a0**2
Trr_r = (1 / (4 * sp.pi * G)) * sp.sqrt(yr) * gr**2 - (a0**2 / (8 * sp.pi * G)) * sp.Rational(2, 3) * yr**sp.Rational(3, 2)
flux = sp.simplify(4 * sp.pi * r**2 * r * Trr_r)                       # int r T^{rr} dS over a sphere
chk("E1 surface integral of x_i T^{ij} n_j over a sphere at any radius r = (2/3) sqrt(G a0) M^{3/2}: r-independent, the deep-MOND virial coefficient",
    sp.simplify(flux - sp.Rational(2, 3) * sp.sqrt(G * a0) * M**sp.Rational(3, 2)) == 0)
chk("E2 that number contains no rho_Lambda, no H, no Lambda (it is fixed by the field equation and the source mass alone)", not any(s in flux.free_symbols for s in [rho_L]))

# ---------------- F: ratio bookkeeping
sigma0 = a0**2 / (8 * sp.pi * G)
rhoL_puz = 4 * a0**2 / G
chk("F1 puzzle: rho_Lambda / (a0^2/(8 pi G)) = 32 pi (pi present)", sp.simplify(rhoL_puz / sigma0 - 32 * sp.pi) == 0)
chk("F2 puzzle: G rho_Lambda / a0^2 = 4 (algebraic)", sp.simplify(G * rhoL_puz / a0**2) == 4)
# The deep-MOND radial tension at g = a0 and its field energy in units of sigma0:
chk("F3 at g = a0: u = (2/3) sigma0, radial stress T^rr = (4/3) sigma0 -- both in the Poisson-normalised unit sigma0 = a0^2/(8 pi G)",
    sp.simplify(u.subs(g, a0) - sp.Rational(2, 3) * sigma0) == 0 and sp.simplify(Trr.subs(g, a0) - sp.Rational(4, 3) * sigma0) == 0)
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
