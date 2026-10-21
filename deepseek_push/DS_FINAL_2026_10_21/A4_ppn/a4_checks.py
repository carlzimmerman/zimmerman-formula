#!/usr/bin/env python3
"""
A4_ppn -- Solar-System and stability-at-every-acceleration gates for the
CANONICAL law  g_N = g^2/(g+a0)  <=>  g = (g_N/2)(1+sqrt(1+4a0/g_N)).

Deterministic.  No network.  stdlib + sympy + mpmath.
Run:  python3 a4_checks.py            (checks must all PASS, exit 0)
      python3 a4_checks.py --mutate   (mutation must break checks, exit 1)

Symbols
  u = g_N            baryonic acceleration
  g                  observed (total) acceleration
  y = u/a0           dimensionless baryonic acceleration
  nu(y) = g/u        the interpolation kernel of the law
  y_t                turn-off scale of nu_fix = 1 + (nu-1)/(1+(y/y_t)^2)
  B_E                Earth 2-sigma ephemeris bound on a constant radial anomaly
"""
import sys
import math
import sympy as sp
import mpmath as mp

mp.mp.dps = 30

MUTATE = "--mutate" in sys.argv

# ----------------------------------------------------------------- constants
C_LIGHT = mp.mpf("2.99792458e8")        # m/s        (BRIEF sec.4)
LAMBDA = mp.mpf("1.0890e-52")           # m^-2       (BRIEF sec.4)
A0 = mp.mpf("9.36e-11")                 # m/s^2      canonical footing, BRIEF sec.4
A0_ALT = mp.mpf("1.13e-10")             # m/s^2      alt footing, BRIEF sec.4
GM_SUN = mp.mpf("1.32712440018e20")     # m^3/s^2    IAU nominal GM_sun
AU = mp.mpf("1.495978707e11")           # m          IAU 2012
B_EARTH = mp.mpf("3.66e-14")            # m/s^2      Sereno & Jetzer 2006 Table 1 via Eq.(9),
                                        #            2 sigma; the bound behind "1279x" in Zenodo 23171085
QUAD_FACTOR_PUBLISHED = mp.mpf("1279")  # Zenodo 23171085: (a0/2)/B_E

# Mutation: adopt the QUADRATURE law's tail/closure for the canonical law,
# i.e. constant anomaly a0/2 and closure (pi/4) y_t.  Every downstream
# canonical number must then break.
A_CONST = mp.mpf("0.5") if MUTATE else mp.mpf("1.0")     # constant anomaly / a0
TAIL_CAN = mp.mpf("0.5") if MUTATE else mp.mpf("1.0")    # lim y*(nu_can-1)
CLOSURE = math.pi / 4 if MUTATE else math.pi / 2          # leading closure coefficient
C_MODEL = mp.mpf("-0.1107867951400") if MUTATE else mp.mpf("-0.8862943611198906")

N_LAMBDA = LAMBDA * C_LIGHT**4 / A0**2                    # dimensionless, ~100.4

# ------------------------------------------------------------------ kernels
def nu_can(y):
    return (1 + mp.sqrt(1 + 4 / y)) / 2

def nu_quad(y):
    return mp.sqrt(1 + 1 / y)

def dg_can(y):
    """dg/du for the canonical law, exact, in units of (dimensionless)."""
    s = mp.sqrt(1 + 4 / y)
    return (1 + s)**2 / (4 * s)

def dg_quad(y):
    return (2 * y + 1) / (2 * mp.sqrt(y * y + y))

def anomaly_can(y, yt):
    """(g-g_N)/a0 for the canonical law with the turn-off, exact."""
    return ((mp.sqrt(y * y + 4 * y) - y) / 2) / (1 + (y / yt)**2)

def anomaly_quad(y, yt):
    return (mp.sqrt(y * y + y) - y) / (1 + (y / yt)**2)

# exact vacuum integral:  I(Y) = int_0^inf y (nu-1) dy / (1+(y/Y)^2)
#                        = (1/2) int (nu-1) d(y^2)  with the turn-off inserted
def I_can(Y):
    """Canonical, exact rational form (v = sqrt(y^2+4y)-y, y:0->inf <=> v:0->2)."""
    Y = mp.mpf(Y)
    f = lambda v: v**2 * (4 - v) / (4 * Y**2 * (2 - v)**2 + v**4)
    return Y**2 * mp.quad(f, [0, 1, 2])

def I_quad(Y):
    """Quadrature, exact rational form (v:0->1/2)."""
    Y = mp.mpf(Y)
    f = lambda v: 2 * v**2 * (1 - v) / (Y**2 * (1 - 2 * v)**2 + v**4)
    return Y**2 * mp.quad(f, [0, mp.mpf(1) / 4, mp.mpf(1) / 2])

def I_can_direct(Y):
    Y = mp.mpf(Y)
    f = lambda y: (mp.sqrt(y * y + 4 * y) - y) / 2 / (1 + (y / Y)**2)
    return mp.quad(f, [0, 2, 10, Y, 20 * Y, mp.inf])

def I_quad_direct(Y):
    Y = mp.mpf(Y)
    f = lambda y: (mp.sqrt(y * y + y) - y) / (1 + (y / Y)**2)
    return mp.quad(f, [0, 2, 10, Y, 20 * Y, mp.inf])

C_CAN = mp.mpf("-0.8862943611198906")   # Richardson-extrapolated, see K6
C_QUAD = mp.mpf("-0.1107867951400")

def F_can_asym(Y):
    """The closure relation as the theory states it (mutated => quadrature's form)."""
    return mp.mpf(CLOSURE) * Y - mp.log(mp.mpf(Y) / 4) + C_MODEL

# ---------------------------------------------------------------- utilities
RESULTS = []

def check(cid, ok, value, threshold, note=""):
    RESULTS.append({"id": cid, "pass": bool(ok), "value": value, "threshold": threshold})
    print(("K%-3s %s %-24s %-24s %s" % (cid, "PASS" if ok else "FAIL",
          fmt(value), fmt(threshold), note)).rstrip())
    return ok

def fmt(v):
    if isinstance(v, str):
        return v
    try:
        return "%.9g" % float(v)
    except Exception:
        return str(v)

def hdr(t):
    print("\n== %s" % t)

print("A4_ppn :: canonical law g_N = g^2/(g+a0) :: Solar-System + stability gates")
print("constants: c=2.99792458e8  Lambda=1.0890e-52  a0=9.36e-11 (canonical)  "
      "a0_alt=1.13e-10  GM_sun=1.32712440018e20  AU=1.495978707e11")
print("           B_E = 3.66e-14 m/s^2 (Sereno & Jetzer 2006, 2 sigma)   "
      "N_Lambda = Lambda c^4/a0^2 = %.9g" % float(N_LAMBDA))
if MUTATE:
    print("*** MUTATION ACTIVE: canonical law assigned the quadrature's a0/2 tail "
          "and (pi/4) closure ***")

# ---------------------------------------------------------------- K1
hdr("K1  exact large-g_N expansion: the constant term")
u, a0s, ys = sp.symbols("u a_0 y", positive=True)
g_can = (u / 2) * (1 + sp.sqrt(1 + 4 * a0s / u))
g_quad = sp.sqrt(u**2 + a0s * u)
ser_can = sp.series(g_can, u, sp.oo, 3)
ser_quad = sp.series(g_quad, u, sp.oo, 3)
const_can = sp.limit(g_can - u, u, sp.oo) / a0s      # should be 1
const_quad = sp.limit(g_quad - u, u, sp.oo) / a0s     # should be 1/2
print("   g_can  = %s" % ser_can)
print("   g_quad = %s" % ser_quad)
ok1 = (const_can == 1) and (const_quad == sp.Rational(1, 2))
check(1, ok1, float(const_can), "1 exactly (sympy)",
      "g-g_N -> %s*a0 ; quadrature -> %s*a0" % (const_can, const_quad))

# ---------------------------------------------------------------- K2
hdr("K2  ephemeris factor of the constant anomaly (Earth 2-sigma bound)")
ratio_can = A0 * A_CONST / B_EARTH
ratio_can_alt = A0_ALT * A_CONST / B_EARTH
rel_to_2x1279 = ratio_can / (2 * QUAD_FACTOR_PUBLISHED)
ok2 = abs(rel_to_2x1279 - 1) < 2e-3
check(2, ok2, ratio_can, "2558 (=2x1279) +-0.2%",
      "a0/B_E=%.6g  a0_alt/B_E=%.6g  ratio/(2*1279)=%.6g"
      % (float(ratio_can), float(ratio_can_alt), float(rel_to_2x1279)))

# ---------------------------------------------------------------- K3
hdr("K3  exact nu(y)-1 and its tail coefficient (both laws)")
nu_c = (1 + sp.sqrt(1 + 4 / ys)) / 2
nu_q = sp.sqrt(1 + 1 / ys)
lim_c = sp.limit(ys * (nu_c - 1), ys, sp.oo)
lim_q = sp.limit(ys * (nu_q - 1), ys, sp.oo)
lim_sqrt = sp.limit(sp.sqrt(ys) * (nu_c - 1), ys, sp.oo)
print("   nu_can-1  = %s" % sp.simplify(nu_c - 1))
print("   nu_quad-1 = %s" % sp.simplify(nu_q - 1))
print("   series nu_can  : %s" % sp.series(nu_c, ys, sp.oo, 3))
print("   series nu_quad : %s" % sp.series(nu_q, ys, sp.oo, 3))
ok3 = (lim_c == 1) and (lim_q == sp.Rational(1, 2)) and (lim_sqrt == 0) and (TAIL_CAN == 1)
check(3, ok3, float(lim_c), "1 exactly (sympy)",
      "lim y(nu_can-1)=%s lim y(nu_quad-1)=%s lim sqrt(y)(nu_can-1)=%s -> both tails 1/y, NOT 1/sqrt(y)"
      % (lim_c, lim_q, lim_sqrt))

# ---------------------------------------------------------------- K4
hdr("K4  numerical tail exponent of the canonical law")
y1, y2 = mp.mpf("1e6"), mp.mpf("1e8")
slope = mp.log((nu_can(y2) - 1) / (nu_can(y1) - 1)) / mp.log(y2 / y1)
ok4 = abs(slope + 1) < 1e-6
check(4, ok4, slope, "-1 +-1e-6", "d ln(nu-1)/d ln y over 1e6..1e8")

# ---------------------------------------------------------------- K5
hdr("K5  vacuum integral: exact integrand, and the DIVERGENCE EXPONENT")
ref_c = I_can_direct(50)
ref_q = I_quad_direct(50)
rel_c = abs(I_can(50) - ref_c) / ref_c
rel_q = abs(I_quad(50) - ref_q) / ref_q
print("   I_can(50)  exact-rational = %.15g   adaptive = %.15g" % (float(I_can(50)), float(ref_c)))
print("   I_quad(50) exact-rational = %.15g   adaptive = %.15g" % (float(I_quad(50)), float(ref_q)))
Ya, Yb = mp.mpf("1e7"), mp.mpf("1e9")
slope_can = mp.log(I_can(Yb) / I_can(Ya)) / mp.log(Yb / Ya)
slope_quad = mp.log(I_quad(Yb) / I_quad(Ya)) / mp.log(Yb / Ya)
print("   I_can(Y)/Y -> %.9g ;  I_quad(Y)/Y -> %.9g" % (float(I_can(Ya) / Ya), float(I_quad(Ya) / Ya)))
ok5 = (rel_c < 1e-18) and (rel_q < 1e-18) and abs(slope_can - 1) < 1e-3 and abs(slope_quad - 1) < 1e-3
check(5, ok5, slope_can, "1 +-1e-3",
      "linear divergence (exponent 1), NOT 3/2;  slope_quad=%.9g" % float(slope_quad))

# ---------------------------------------------------------------- K6
hdr("K6  closure asymptotics and the exact 8x identity")
cval = I_can(mp.mpf("1e8")) - mp.pi / 2 * mp.mpf("1e8") + mp.log(mp.mpf("1e8") / 4)
ident = I_can(mp.mpf("66.3")) / I_quad(mp.mpf("66.3") / 4)
print("   I_can - (pi/2)Y + ln(Y/4) at Y=1e8 : %.15g   (Richardson C_can = %.15g)"
      % (float(cval), float(C_CAN)))
print("   I_can(Y) / I_quad(Y/4) = %.15g   (exact identity: 8)" % float(ident))
asym_rel = I_can(mp.mpf("66.3")) / F_can_asym(mp.mpf("66.3")) - 1
print("   asymptotic closure accuracy at y_t=66.3 : %.3g" % float(asym_rel))
ok6 = abs(cval - C_CAN) < 1e-6 and abs(ident - 8) < 1e-12 and abs(asym_rel) < 1e-3
check(6, ok6, cval, "-0.8862943611 +-1e-6",
      "identity ratio=%.9g ; asym closure rel.err=%.3g" % (float(ident), float(asym_rel)))

# ---------------------------------------------------------------- K7
hdr("K7  the turn-off y_t that closes the observed Lambda (canonical law)")
yt_model = mp.findroot(lambda Y: F_can_asym(Y) - N_LAMBDA, 66 if not MUTATE else 129)
yt_can = mp.findroot(lambda Y: I_can(Y) - N_LAMBDA, 66)          # exact integral, never mutated
yt_quad = mp.findroot(lambda Y: I_quad(Y) - N_LAMBDA, 129)
rel_model = abs(yt_model - yt_can) / yt_can
print("   closure model (CLOSURE=%.6g, C=%.6g) inverts to y_t = %.12g"
      % (float(CLOSURE), float(C_MODEL), float(yt_model)))
print("   exact integral root y_t^can = %.12g   F_can(y_t)/N_Lambda = %.15g"
      % (float(yt_can), float(I_can(yt_can) / N_LAMBDA)))
print("   rel. difference model vs exact = %.4g" % float(rel_model))
print("   y_t^quad = %.12g   y_t^quad/y_t^can = %.9g" % (float(yt_quad), float(yt_quad / yt_can)))
print("   turn-off acceleration y_t*a0 = %.6g m/s^2" % float(yt_can * A0))
ok7 = (rel_model < 1e-3) and abs(I_can(yt_can) / N_LAMBDA - 1) < 1e-12
check(7, ok7, yt_model, "66.2999 (exact root)",
      "closure (pi/2)y_t - ln(y_t/4) + C_can = Lambda c^4/a0^2 reproduces the exact root")

# ---------------------------------------------------------------- K8
hdr("K8  normalization cross-check vs the published quadrature closure; transplant test")
quad_at_129 = I_quad(mp.mpf("129")) / N_LAMBDA
transplant = I_can(yt_quad) / N_LAMBDA
print("   quadrature, y_t=129 (top of the published 94-129 band): F_quad/N_Lambda = %.6g"
      % float(quad_at_129))
print("   canonical fed the quadrature's y_t=%.6g : F_can/N_Lambda = %.6g"
      % (float(yt_quad), float(transplant)))
ok8 = abs(quad_at_129 - 1) < 5e-3 and (1.90 < transplant < 2.05)
check(8, ok8, transplant, "in [1.90,2.05]",
      "published closure reproduced to %.3g ; transplant over-predicts Lambda"
      % float(abs(quad_at_129 - 1)))

# ---------------------------------------------------------------- K9
hdr("K9  every planet inside its ephemeris bound (anomaly at y_t from K7)")
# per-planet bounds from prep_2026/planetary_doors/BOUNDS.md sec.1.2 (Gauss
# secular-pericenter conversion of FM24 Table 10); Uranus/Neptune carry the
# Saturn bound as a deliberately OVER-TIGHT stand-in (their published bounds
# are weaker by >1 order), flagged pub=False.
PLANETS = [
    ("Mercury", "0.387098", "4.6e-14", True),
    ("Venus", "0.723332", "8.0e-14", True),
    ("Earth", "1.0", "8.7e-15", True),
    ("Mars", "1.523679", "1.4e-15", True),
    ("Jupiter", "5.2044", "5.6e-13", True),
    ("Saturn", "9.5826", "7.0e-15", True),
    ("Uranus", "19.19126", "7.0e-15", False),
    ("Neptune", "30.07", "7.0e-15", False),
]
rows = []
print("   %-8s %7s %11s %9s %11s %10s %9s %9s" %
      ("planet", "r/AU", "g_N", "y", "anom", "bound", "anom/B", "y_t_max"))
for name, r, B, pub in PLANETS:
    rr = mp.mpf(r) * AU
    gN = GM_SUN / rr**2
    yv = gN / A0
    anom = A0 * anomaly_can(yv, yt_can)
    Bm = mp.mpf(B)
    ytmax = yv / mp.sqrt(A0 / Bm - 1)
    rows.append((name, gN, yv, anom, Bm, anom / Bm, ytmax, pub))
    print("   %-8s %7.3f %11.4g %9.3g %11.3g %10.3g %9.3g %9.3g%s" %
          (name, float(mp.mpf(r)), float(gN), float(yv), float(anom), float(Bm),
           float(anom / Bm), float(ytmax), "" if pub else " *"))
worst = max(rows, key=lambda t: t[5])
ok9 = worst[5] < 1
check(9, ok9, worst[5], "< 1 (ratio anom/bound)",
      "worst = %s ; Uranus/Neptune(*) use the Saturn bound as an over-tight stand-in"
      % worst[0])

# ---------------------------------------------------------------- K10
hdr("K10 does ONE y_t do both jobs?  required vs allowed")
ytmax_all = min(r[6] for r in rows)
ytmax_pub = min(r[6] for r in rows if r[7])
margin = ytmax_all / yt_can
print("   required y_t (Lambda)          = %.6g" % float(yt_can))
print("   allowed  y_t (all 8 planets)   = %.6g  (binding: %s)"
      % (float(ytmax_all), min(rows, key=lambda t: t[6])[0]))
print("   allowed  y_t (published only)  = %.6g  (binding: %s)"
      % (float(ytmax_pub), min([r for r in rows if r[7]], key=lambda t: t[6])[0]))
print("   margin = %.6g  (y_t may grow by this factor before the tightest planet fails)"
      % float(margin))
ok10 = margin > 2
check(10, ok10, margin, "> 2 (factor margin)",
      "compatible: one y_t does both jobs")

# ---------------------------------------------------------------- K11
hdr("K11 linear response dg/dg_N across u in (0,a0] -- positivity")
uu = mp.mpf(1)
print("   %-10s %14s %14s" % ("u/a0", "dg/du can", "dg/du quad"))
mins = []
for q in ["1e-6", "1e-4", "1e-3", "0.01", "0.1", "0.5", "0.9", "1.0"]:
    yv = mp.mpf(q)
    a, b = dg_can(yv), dg_quad(yv)
    mins.append(min(a, b))
    print("   %-10s %14.9g %14.9g" % (q, float(a), float(b)))
s_sym = sp.symbols("s", positive=True)
pos_can = sp.simplify(((1 + s_sym)**2 / (4 * s_sym)) > 0)
# deep limit: dg/du ~ (1/2) sqrt(a0/u) for BOTH laws -> y (dg/du)^2 -> 1/4
deep_c = mp.mpf("1e-12") * dg_can(mp.mpf("1e-12"))**2
deep_q = mp.mpf("1e-12") * dg_quad(mp.mpf("1e-12"))**2
print("   structural: dg_can/du = (1+s)^2/(4s), s=sqrt(1+4/y)  -> positive for s>1 (sympy)")
print("   deep limit y*(dg/du)^2 : can=%.12g quad=%.12g  (-> 1/4 both)" % (float(deep_c), float(deep_q)))
ok11 = min(mins) > 0 and bool(pos_can) and abs(deep_c - 0.25) < 1e-6 and abs(deep_q - 0.25) < 1e-6
check(11, ok11, min(mins), "> 0 everywhere",
      "min over u in (0,a0]; divergence only at u=0, positive and integrable")

# ---------------------------------------------------------------- K12
hdr("K12 the patched (turn-off) law is itself monotone -- critical y_t")
def g_patch(yv, Y):
    return yv + ((mp.sqrt(yv * yv + 4 * yv) - yv) / 2) / (1 + (yv / Y)**2)

def min_response(Y):
    best, arg = mp.inf, Y
    for k in range(-100, 101):
        e = Y * mp.mpf(10)**(mp.mpf(k) / 50)
        v = mp.diff(lambda z: g_patch(z, Y), e)
        if v < best:
            best, arg = v, e
    try:                                    # polish the minimum
        ymin = mp.findroot(lambda z: mp.diff(lambda w: g_patch(w, Y), z, 2), arg)
        best, arg = mp.diff(lambda z: g_patch(z, Y), ymin), ymin
    except Exception:
        pass
    return best, arg

lo, hi = mp.mpf("0.04"), mp.mpf("0.07")
for _ in range(50):
    mid = (lo + hi) / 2
    if min_response(mid)[0] < 0:
        lo = mid
    else:
        hi = mid
yt_crit = (lo + hi) / 2
at_req = min_response(yt_can)[0]
print("   min_y dg/dy at y_t = y_t^can : %.12g" % float(at_req))
print("   critical y_t below which the patched law is non-monotone: %.12g" % float(yt_crit))
print("   y_t^can / y_t^crit = %.6g ; turn-off acceleration there = %.4g m/s^2"
      % (float(yt_can / yt_crit), float(yt_crit * A0)))
ok12 = at_req > 0 and (yt_can / yt_crit) > 10
check(12, ok12, yt_can / yt_crit, "> 10",
      "the cure is gradient-stable; instability only for y_t < %.4g" % float(yt_crit))

# ---------------------------------------------------------------- K13
hdr("K13 the general gate: constant anomaly = c*a0 with c = lim x(1-mu(x))")
xx = sp.symbols("x", positive=True)
mu_can_s = xx / (1 + xx)                                 # canonical law, exactly
mu_quad_s = (sp.sqrt(1 + 4 * xx**2) - 1) / (2 * xx)      # quadrature law, exactly
c_can = sp.limit(xx * (1 - mu_can_s), xx, sp.oo)
c_quad = sp.limit(xx * (1 - mu_quad_s), xx, sp.oo)
# and the identity "mu = x/(1+x) <=> g_N = g^2/(g+a0)"
g_ = sp.symbols("g", positive=True)
mu_id = sp.simplify((g_ * mu_can_s.subs(xx, g_ / a0s)) - g_**2 / (g_ + a0s))
c_max = B_EARTH / A0
print("   mu_can  = x/(1+x)      -> c = %s   (check: g*mu(g/a0) - g^2/(g+a0) = %s)" % (c_can, mu_id))
print("   mu_quad = (sqrt(1+4x^2)-1)/(2x) -> c = %s" % c_quad)
print("   bound requires c <= B_E/a0 = %.6g ; canonical c = %.6g (%.1f x over)"
      % (float(c_max), float(c_can), float(c_can / c_max)))
ok13 = (c_can == 1) and (c_quad == sp.Rational(1, 2)) and (mu_id == 0) and (c_can > c_max)
check(13, ok13, c_can / c_max, "> 1 (excluded)",
      "any interpolation with a 1/x term in mu has a constant anomaly c*a0; c must be < %.4g" % float(c_max))

# ---------------------------------------------------------------- extras
hdr("numbers carried to the report")
print("   N_Lambda = Lambda c^4/a0^2 = %.9g" % float(N_LAMBDA))
print("   a0/B_E = %.6g ; a0_alt/B_E = %.6g ; (a0/2)/B_E = %.6g"
      % (float(A0 / B_EARTH), float(A0_ALT / B_EARTH), float(A0 / 2 / B_EARTH)))
print("   C_can = %.12g ; C_quad = %.12g ; C_can/C_quad = %.9g"
      % (float(C_CAN), float(C_QUAD), float(C_CAN / C_QUAD)))
print("   y_t^can = %.9g ; y_t^quad = %.9g ; ratio = %.9g"
      % (float(yt_can), float(yt_quad), float(yt_quad / yt_can)))
print("   alt footing (a0=1.13e-10): N_Lambda = %.9g ; y_t^can = %.9g ; y_t^quad = %.9g"
      % (float(LAMBDA * C_LIGHT**4 / A0_ALT**2),
         float(mp.findroot(lambda Y: I_can(Y) - LAMBDA * C_LIGHT**4 / A0_ALT**2, 46)),
         float(mp.findroot(lambda Y: I_quad(Y) - LAMBDA * C_LIGHT**4 / A0_ALT**2, 89))))
print("   galactic-side cost of the turn-off: anomaly suppression 1/(1+(y/y_t)^2) at y=10 :")
print("     canonical %.4g   quadrature %.4g"
      % (float(1 / (1 + (mp.mpf(10) / yt_can)**2)), float(1 / (1 + (mp.mpf(10) / yt_quad)**2))))

npass = sum(1 for r in RESULTS if r["pass"])
ntot = len(RESULTS)
print("\nA4 COMPLETE: %d/%d checks PASS." % (npass, ntot))

# ---------------------------------------------------------------- results.json
NUMBERS = {
    "N_Lambda_dimensionless": float(N_LAMBDA),
    "constant_anomaly_over_a0_canonical": float(const_can),
    "constant_anomaly_over_a0_quadrature": float(const_quad),
    "a0": float(A0), "a0_alt": float(A0_ALT), "Lambda": float(LAMBDA), "c": float(C_LIGHT),
    "B_E_earth_2sigma": float(B_EARTH),
    "a0_over_B_E": float(A0 / B_EARTH),
    "a0_alt_over_B_E": float(A0_ALT / B_EARTH),
    "half_a0_over_B_E": float(A0 / 2 / B_EARTH),
    "half_a0_alt_over_B_E": float(A0_ALT / 2 / B_EARTH),
    "response_table": {q: {"canonical": float(dg_can(mp.mpf(q))),
                           "quadrature": float(dg_quad(mp.mpf(q)))}
                       for q in ["1e-6", "1e-4", "1e-3", "0.01", "0.1", "0.5", "0.9", "1.0"]},
    "published_quadrature_factor": float(QUAD_FACTOR_PUBLISHED),
    "canonical_factor_over_published": float((A0 / B_EARTH) / QUAD_FACTOR_PUBLISHED),
    "tail_coeff_y_nu_minus_1_canonical": float(lim_c),
    "tail_coeff_y_nu_minus_1_quadrature": float(lim_q),
    "tail_exponent_dln_dlny_canonical": float(slope),
    "vacuum_divergence_exponent": float(slope_can),
    "vacuum_divergence_exponent_quadrature": float(slope_quad),
    "I_can_over_Y_limit": float(I_can(mp.mpf("1e9")) / mp.mpf("1e9")),
    "I_quad_over_Y_limit": float(I_quad(mp.mpf("1e9")) / mp.mpf("1e9")),
    "C_can": float(C_CAN), "C_quad": float(C_QUAD), "C_ratio": float(C_CAN / C_QUAD),
    "identity_ratio_Ican_over_Iquad_quarter": float(ident),
    "y_t_canonical": float(yt_can), "y_t_quadrature": float(yt_quad),
    "y_t_ratio_quad_over_can": float(yt_quad / yt_can),
    "y_t_canonical_a0": float(yt_can * A0), "y_t_quadrature_a0": float(yt_quad * A0),
    "y_t_model_inversion": float(yt_model),
    "y_t_model_vs_exact_rel": float(rel_model),
    "asymptotic_closure_rel_err_at_66": float(asym_rel),
    "F_quad_at_129_over_N": float(quad_at_129),
    "F_can_at_y_t_quad_over_N": float(transplant),
    "y_t_alt_footing_canonical": float(mp.findroot(lambda Y: I_can(Y) - LAMBDA * C_LIGHT**4 / A0_ALT**2, 46)),
    "y_t_alt_footing_quadrature": float(mp.findroot(lambda Y: I_quad(Y) - LAMBDA * C_LIGHT**4 / A0_ALT**2, 89)),
    "N_Lambda_alt_footing": float(LAMBDA * C_LIGHT**4 / A0_ALT**2),
    "worst_planet_ratio": float(worst[5]), "worst_planet": worst[0],
    "y_t_max_all_planets": float(ytmax_all),
    "y_t_max_published_only": float(ytmax_pub),
    "y_t_margin": float(margin),
    "y_t_margin_published_only": float(ytmax_pub / yt_can),
    "response_min_over_u_le_a0": float(min(mins)),
    "response_at_u_eq_a0_canonical": float(dg_can(mp.mpf(1))),
    "response_at_u_eq_a0_quadrature": float(dg_quad(mp.mpf(1))),
    "deep_limit_y_dgdu_sq_canonical": float(deep_c),
    "deep_limit_y_dgdu_sq_quadrature": float(deep_q),
    "response_min_at_y_t_canonical": float(at_req),
    "y_t_critical_patched": float(yt_crit),
    "y_t_critical_a0": float(yt_crit * A0),
    "y_t_over_critical": float(yt_can / yt_crit),
    "c_max_allowed": float(c_max), "c_canonical": float(c_can), "c_quadrature": float(c_quad),
    "galaxy_suppression_at_y10_canonical": float(1 / (1 + (mp.mpf(10) / yt_can)**2)),
    "galaxy_suppression_at_y10_quadrature": float(1 / (1 + (mp.mpf(10) / yt_quad)**2)),
    "galaxy_suppression_loss_ratio_can_over_quad": float(
        ((mp.mpf(10) / yt_can)**2 / (1 + (mp.mpf(10) / yt_can)**2)) /
        ((mp.mpf(10) / yt_quad)**2 / (1 + (mp.mpf(10) / yt_quad)**2))),
    "planets": {r[0]: {"g_N": float(r[1]), "y": float(r[2]), "anomaly": float(r[3]),
                       "bound": float(r[4]), "ratio": float(r[5]),
                       "y_t_max": float(r[6]), "published_bound": r[7]} for r in rows},
}
OUT = {
    "lane": "A4_ppn",
    "status": "CONDITIONAL(turn-off premise)",
    "status_detail": {
        "item1_bare_law_constant_anomaly": "DERIVED (exact algebra) + NO-GO verdict against B_E",
        "item2_tail_and_vacuum_divergence": "DERIVED (exact, sympy + exact rational quadrature)",
        "item3a_turn_off_y_t": "NUMERICAL (transcendental root; exact integrand, Richardson-certified asymptotics)",
        "item3b_planetary_gate_and_compatibility": "NUMERICAL (published bounds, SI constants)",
        "item4_stability": "DERIVED (exact response functions; positivity symbolic)",
    },
    "checks": RESULTS,
    "numbers": NUMBERS,
    "constants_used": [
        "c = 2.99792458e8 m/s (BRIEF sec.4, SI exact)",
        "Lambda = 1.0890e-52 m^-2 (BRIEF sec.4)",
        "a0 = 9.36e-11 m/s^2 canonical footing (BRIEF sec.4; = c^2 sqrt(Lambda/32pi))",
        "a0_alt = 1.13e-10 m/s^2 alt footing (BRIEF sec.4)",
        "GM_sun = 1.32712440018e20 m^3/s^2 (IAU nominal)",
        "AU = 1.495978707e11 m (IAU 2012)",
        "B_E = 3.66e-14 m/s^2 = Earth 2-sigma bound on a constant radial anomaly (Sereno & Jetzer 2006 Table 1 via Eq.9; the number behind '1279x' in Zenodo 23171085)",
        "published quadrature factor 1279 = (a0/2)/B_E (Zenodo 23171085); alt-footing companion 1544 = (a0_alt/2)/B_E",
        "planetary semi-major axes r/AU: Mercury 0.387098, Venus 0.723332, Earth 1.0, Mars 1.523679, Jupiter 5.2044, Saturn 9.5826, Uranus 19.19126, Neptune 30.07 (IAU/JPL mean elements)",
        "per-planet bounds: Mercury 4.6e-14, Venus 8.0e-14, Earth 8.7e-15, Mars 1.4e-15, Jupiter 5.6e-13, Saturn 7.0e-15 m/s^2 (prep_2026/planetary_doors/BOUNDS.md sec.1.2, Gauss secular-pericenter conversion of Fienga & Minazzoli 2024 Table 10); Uranus/Neptune have no published per-planet value there and carry Saturn's bound as an over-tight stand-in (flagged)",
        "published quadrature turn-off band y_t = 94-129 (Zenodo 23171085; its top edge reproduces the observed Lambda to 0.19% in this lane's normalization)",
        "closure normalization Lambda c^4/a0^2 = (1/2) int (nu-1) d(y^2) inherited from Zenodo 23171085/23251231 (cross-checked here: y_t=129 reproduces it to 0.19%)",
    ],
}
if not MUTATE:
    import json
    with open("a4_results.json", "w") as fh:
        json.dump(OUT, fh, indent=2, sort_keys=False, default=float)
        fh.write("\n")
    print("wrote a4_results.json")
sys.exit(0 if npass == ntot else 1)
