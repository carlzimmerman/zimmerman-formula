#!/usr/bin/env python3
"""
AS027 — Effective AQUAL response of the Q branch  (bounded prototype, rev 2)

Task: audit whether the algebraic Q branch (g^2 = B^2 + a0*B, radial law) can be
represented as an effective AQUAL-type divergence law
    div( mu(|grad Phi|/a0) grad Phi ) = 4 pi G rho_b
in spherical symmetry, and derive the effective mu/nu and its domain.

Framework inputs (adopted, not derived here):
  a0 = kappa*c*sqrt(G*rho_Lambda), kappa = 1/2 ADOPTED
  Q branch: g^2 = B^2 + a0*B,  B = g_N = |grad Phi_N| (radial)
  x = g/a0,  y = B/a0  (both > 0)
  G = 6.67430e-11 m^3 kg^-1 s^-2, c = 299792458 m/s, M_sun = 1.98847e30 kg,
  pc = 3.085677581491367e16 m
  footings: a0_can = 9.3619e-11 m/s^2 ; a0_alt = 1.1279e-10 m/s^2 (separate)

rev2 fixes (from rev1 actual run):
  - all algebraic-identity checks use RELATIVE residuals (values reach 1e16 on
    the grid; 50-digit absolute residuals ~1e-34 there are representation
    roundoff, not identity failure; relative residuals are ~1e-49)
  - yofx uses the rationalized stable form y = 2x^2/(1+sqrt(1+4x^2))
  - NC1 (C6a) pass criterion: |d(x)| MUST exceed the detection threshold
    (control fires iff the kernels differ; a zero difference would FAIL)
  - C10a/C10b Hernquist checks use relative residuals; the field-equation
    derivative check uses the analytic derivative PLUS an explicit
    Richardson-extrapolated finite difference (mpmath.diff order >= 2 fails at
    these magnitudes: mp.diff(flux, r, 8) ~ 1e-50, mp.diff(., ., 2) = 6.9e-5 vs
    analytic 1.1e-31 — recorded as failed attempt)
  - C13 converts M_sun -> kg (rev1 reported r_M for Mb = 10^n kg, wrong by
    1.98847e30; corrected numbers: r_M(1e11 Msun, canonical) = 12.2 kpc)
  - C3 inverse-representation check scoped to the well-conditioned domain
    x <= 100; the mu -> 1 tail is characterized as conditioning: (1-mu^2) is an
    O(1)-minus-O(1) subtraction carrying ~1e-50 absolute mantissa error, and
    x*(1-mu^2) amplifies it by x ~ 1/(1-mu) (observed 2.1e-43 at x = 5.0e7)
"""
import time
import mpmath as mp
mp.mp.dps = 50

t0 = time.time()

def muQ(x):  # effective AQUAL mu of the Q branch (rationalized form, stable)
    return 2*x/(1 + mp.sqrt(1 + 4*x**2))

def yofx(x):  # y = B/a0 from x (unique positive root of y^2+y = x^2; stable form)
    return 2*x**2/(1 + mp.sqrt(1 + 4*x**2))

def nuQ(y):  # g/B = sqrt(1+1/y)
    return mp.sqrt(1 + mp.mpf(1)/y)

def muEXP(x):  # historical EXP AQUAL (COMPARISON branch only)
    return 1 - mp.e**(-x)

def Fprim(X):  # closed-form derivative of the AQUAL primitive
    return (1 + 4*X - mp.sqrt(1 + 4*X))/(2*mp.sqrt(X)*mp.sqrt(1 + 4*X))

def F(X):      # closed-form primitive
    return mp.asinh(2*mp.sqrt(X))/4 + (mp.sqrt(X)/2)*mp.sqrt(1 + 4*X) - mp.sqrt(X)

def rel(a, b):
    """relative residual of a == b, guarded for zero-scale quantities"""
    denom = max(mp.mpf(1), abs(a), abs(b))
    return abs(a - b)/denom

# ---------------- grid (task: y = 10^k, k = -10 .. 8 step 0.1) ----------------
ks = [ -10 + 0.1*i for i in range(181) ]          # 181 points <= 512 cells
ys = [ mp.mpf(10)**k for k in ks ]
xs = [ mp.sqrt(y*y + y) for y in ys ]             # Q branch (x from y, stable)

res = {}
def check(name, val, tol, note=""):
    res[name] = (val, tol)
    ok = val <= tol
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: residual={mp.nstr(val, 6)} tol={mp.nstr(tol, 3)} {note}")
    return ok

# C1: master identity y^2 + y = x^2  (RELATIVE residual)
c1 = max(rel(y*y + y, x*x) for x, y in zip(xs, ys))
check("C1 y^2+y=x^2 (rel)", c1, mp.mpf("1e-45"))

# C2: mu_Q(x)*x = y (RELATIVE)
c2 = max(rel(muQ(x)*x, yofx(x)) for x in xs)
check("C2 mu_Q(x)*x = y (rel)", c2, mp.mpf("1e-45"))

# C3: inverse representation. The theorem x = mu/(1-mu^2) (equivalently
#     x*(1-mu^2) = mu) is CERTIFIED algebraically in Lean (qMu_inverse). The
#     only numerical issue is CONDITIONING: at mu -> 1 the subtraction (1-mu^2)
#     cancels digits, so the divided/cross-multiplied forms degrade on the
#     far-Newtonian tail (measured 2.1e-43 rel at x=1e8 at 50 digits; the exact
#     identity 1-mu^2 = y/x^2 diagnoses this as representation cancellation).
#     Numeric verification is therefore scoped to the well-conditioned domain
#     x <= 100 (mu <= 0.995); the tail is recorded as a conditioning probe.
maxc3x = mp.mpf(0); maxc3y = mp.mpf(0)
for x in xs:
    if x <= 100:
        mu = muQ(x)
        maxc3x = max(maxc3x, rel(x*(1 - mu**2), mu))           # x(1-mu^2) = mu
        maxc3y = max(maxc3y, rel(yofx(x)*(1 - mu**2), mu**2))  # y(1-mu^2) = mu^2
check("C3a x*(1-mu^2) = mu, well-conditioned domain x<=100", maxc3x, mp.mpf("1e-45"))
check("C3b y*(1-mu^2) = mu^2, well-conditioned domain x<=100", maxc3y, mp.mpf("1e-45"))
# C3c: conditioning of the inverse representation at mu -> 1, with the exact
# mechanism quantified: (1-mu^2) is an O(1) minus O(1) subtraction (few
# non-cancelling digits), so it carries a fixed ABSOLUTE mantissa error ~1e-50;
# the product x*(1-mu^2) then amplifies it by x ~ 1/(1-mu): observed
# |x(1-mu^2) - mu| ~ 2.1e-43 at x = 5.0e7 = 5.0e7 * 1e-50 * 4.1, matching the
# condition number kappa_rel ~ x/(1+mu) ~ 1/(1-mu) of the map mu -> x.
worst_dp = mp.mpf(0); worst_sub = mp.mpf(0)
for x in xs:
    if x > 100:
        mu = muQ(x)
        best = rel(muQ(x), yofx(x)/x)                     # mu = y/x itself
        sub = rel(1 - mu**2, yofx(x)/x**2)                # exact identity 1-mu^2 = y/x^2
        worst_dp = max(worst_dp, best); worst_sub = max(worst_sub, sub)
print(f"[C3c] conditioning probe x>100: rel(mu, y/x) = {mp.nstr(worst_dp,4)} ; "
      f"rel(1-mu^2, y/x^2) = {mp.nstr(worst_sub,4)} ; forward amplification of "
      f"x*(1-mu^2) is ~x*ulp (kappa ~ x ~ 1/(1-mu))")

# C4: deep limit on y <= 1e-3  (x <= 0.03164; |mu/x - 1| <= 1.002 x^2)
deep = [(x, muQ(x)/x - 1) for x, y in zip(xs, ys) if y <= mp.mpf("1e-3")]
c4 = max(abs(r) for _, r in deep)
c4tol = max(1.002*x*x for x, _ in deep)
check("C4 deep |mu/x-1| <= 1.002 x^2", c4, c4tol, f"n={len(deep)}")

# C5: Newtonian regime on y >= 1e3
newt = [(x, muQ(x) - (1 - 1/(2*x))) for x, y in zip(xs, ys) if y >= mp.mpf("1e3")]
c5 = max(abs(r) for _, r in newt)
c5tol = max(1.0001/(8*x*x) for x, _ in newt)
check("C5a |mu_Q-(1-1/2x)| <= 1.0001/(8x^2)", c5, c5tol, f"n={len(newt)}")
off = [(x, y, (x - y) - mp.mpf(1)/2) for x, y in zip(xs, ys) if y >= mp.mpf("1e3")]
c5b = max(abs(r) for _, _, r in off)
c5btol = max(1.02/(8*y) for _, y, _ in off)
check("C5b |(x-y)-1/2| <= 1.02/(8y) (Newton offset a0/2)", c5b, c5btol)

# C6: NC1 — substitute mu = 1 - exp(-x), show difference at finite positive x
d1 = muEXP(mp.mpf(1)) - muQ(mp.mpf(1))
print(f"[C6] d(1) = mu_EXP(1) - mu_Q(1) = {mp.nstr(d1, 15)}")
ok = abs(d1) > mp.mpf("1e-6")
print(f"[{'PASS' if ok else 'FAIL'}] C6a NC1 fires: |d(1)| = {mp.nstr(abs(d1),6)} > 1e-6 "
      f"(control: kernels differ at finite x=1; a zero difference would FAIL)")
res["C6a"] = (abs(d1), mp.mpf("1e-6"), "detection: |d| must exceed tol")
# fine scan for sign changes of d(x), x in [0.02, 5] step 0.01, then bisection
lo = mp.mpf("0.02"); hi = mp.mpf("5.0"); step = mp.mpf("0.01")
prev_x, prev_d = lo, muEXP(lo) - muQ(lo)
brackets = []
x = lo
while x <= hi:
    d = muEXP(x) - muQ(x)
    if d == 0 or (prev_d < 0) != (d < 0):
        brackets.append((prev_x, x))
    prev_x, prev_d = x, d
    x += step
roots = []
for a, b in brackets:
    fa = muEXP(a) - muQ(a)
    for _ in range(220):                      # bisection to 50 dps
        m = (a + b)/2; fm = muEXP(m) - muQ(m)
        if (fa < 0) == (fm < 0): a, fa = m, fm
        else: b = m
        if b - a < mp.mpf("1e-49"): break
    roots.append((a + b)/2)
print(f"[C6] sign-change brackets on [0.02,5]: {[(mp.nstr(a,4), mp.nstr(b,4)) for a,b in brackets]}")
print(f"[C6] bisection roots of d(x)=0: {[mp.nstr(r, 12) for r in roots]}")
for r in roots:
    check(f"C6b bracketed root d({mp.nstr(r,7)})", abs(muEXP(r) - muQ(r)), mp.mpf("1e-47"))
xbig = mp.mpf("100")
d_big = muEXP(xbig) - muQ(xbig)
ok = d_big > 0
print(f"[{'PASS' if ok else 'FAIL'}] C6c d(100) = {mp.nstr(d_big,8)} > 0 (asymptotic ~1/(2x))")

# C7: monotonicity (closed-form derivatives)
def muQp(x):
    s = mp.sqrt(1 + 4*x**2)
    return (s - 1)/(2*x*x*s)
def nuQp(y):
    return -1/(2*y*y*mp.sqrt(1 + mp.mpf(1)/y))
c7a = min(muQp(x) for x in xs)
c7b = max(nuQp(y) for y in ys)
ok1 = c7a > 0; ok2 = c7b < 0
print(f"[{'PASS' if ok1 else 'FAIL'}] C7a min mu_Q' over grid = {mp.nstr(c7a,6)} > 0 "
      f"(strictly increasing; closed form (s-1)/(2x^2 s) > 0 for x>0)")
print(f"[{'PASS' if ok2 else 'FAIL'}] C7b max nu_Q' over grid = {mp.nstr(c7b,6)} < 0 "
      f"(strictly decreasing)")
res["C7a"] = (c7a, mp.mpf(0), "needs > 0"); res["C7b"] = (c7b, mp.mpf(0), "needs < 0")

# C8: Milgrom-1999 form identity: sqrt(1+(2x)^-2) - (2x)^-1 == mu_Q(x)
c8 = max(rel(mp.sqrt(1 + 1/(4*x*x)) - 1/(2*x), muQ(x)) for x in xs)
check("C8 Milgrom-1999 mu_hat = mu_Q (rel)", c8, mp.mpf("1e-45"))

# C9: AQUAL primitive: F'(X) = mu_Q(sqrt X); F(X) vs quadrature
Xs = [ mp.mpf(10)**(-8 + 1.6*i) for i in range(11) ]   # log-spaced X
c9a = max(rel(Fprim(X), muQ(mp.sqrt(X))) for X in Xs)
check("C9a F'(X) = mu_Q(sqrt X) (rel)", c9a, mp.mpf("1e-45"))
c9b = mp.mpf(0)
for X in Xs:
    I = mp.quad(lambda s: muQ(mp.sqrt(s)), [0, X])
    c9b = max(c9b, rel(F(X), I))
check("C9b F(X) = quad(mu_Q(sqrt s)) (rel)", c9b, mp.mpf("1e-44"))
Fdeep = max(abs(F(X)/(X**mp.mpf("1.5")) - mp.mpf(2)/3) for X in Xs if X <= mp.mpf("1e-4"))
print(f"[C9c] max |F(X)/X^1.5 - 2/3| on X<=1e-4 = {mp.nstr(Fdeep,6)} "
      f"(leading neglected term (2/5)X)")

# C10: Hernquist field-equation check (independent representation by substitution)
M_sun = mp.mpf("1.98847e30")
M = mp.mpf(10)**11 * M_sun                                  # 1e11 M_sun
a = mp.mpf("20") * mp.mpf("3.085677581491367e16")           # 20 kpc
pc = mp.mpf("3.085677581491367e16")
G = mp.mpf("6.67430e-11"); c = mp.mpf("299792458")
a0can = mp.mpf("9.3619e-11")
def Mlt(r):   # M(<r) Hernquist
    return M * r**2 / (r + a)**2
def rhoH(r):
    return M * a / (2*mp.pi * r * (r + a)**3)
def B(r):   # g_N
    return G * Mlt(r) / r**2
def gQ(r):  # Q-branch total g (a0 = a0can)
    y = B(r)/a0can
    return a0can * mp.sqrt(y*y + y)
def flux(r):
    return r**2 * muQ(gQ(r)/a0can) * gQ(r)
rs = [ mp.mpf(10)**(-3 + 0.6*i) * a for i in range(11) ]    # 1e-3 a .. 1e3 a
c10a = max(rel(flux(r), G*Mlt(r)) for r in rs)
check("C10a r^2 mu(x) g = G M(<r) (rel)", c10a, mp.mpf("1e-42"))
# C10b: field equation d/dr[r^2 mu g] = 4 pi G rho r^2, two independent routes:
#  (i) ANALYTIC direct differentiation of the closed form (flux = G M(<r)):
#      d/dr[G M r^2/(r+a)^2] = 2 G M a r/(r+a)^3  ==  4 pi G rho r^2  (Hernquist
#      identity dM/dr = 4 pi rho r^2) — exact, residual ~1e-50;
#  (ii) EXPLICIT finite differences with controlled step + Richardson (order 4),
#      in a genuinely different numerical representation. mpmath.diff at order
#      >= 2 is NOT used: a probe showed mp.diff(flux, r, 8) = O(1e-50) and
#      mp.diff(., ., 2) = 6.9e-5 vs analytic 1.1e-31 (step-selection collapse
#      at these magnitudes) — recorded as a failed attempt.
c10b1 = mp.mpf(0)
for r in rs:
    dflux_an = 2*G*M*a*r/(r + a)**3
    c10b1 = max(c10b1, rel(dflux_an, 4*mp.pi*G*rhoH(r)*r**2))
check("C10b-i analytic d/dr[G M(<r)] = 4 pi G rho r^2", c10b1, mp.mpf("1e-42"))

def fd4(f, r, h):
    # 5-point central difference, order 4
    return ( -f(r+2*h) + 8*f(r+h) - 8*f(r-h) + f(r-2*h) ) / (12*h)
c10b2 = mp.mpf(0); c10b2raw = mp.mpf(0); ratio_track = []
for r in rs:
    h1 = r*mp.mpf("1e-4")
    d1, d2 = fd4(flux, r, h1), fd4(flux, r, h1/4)   # steps h1 and h1/4
    # Richardson extrapolation of the order-4 stencil: D = (256 D(h/4) - D(h))/255
    rich = (256*d2 - d1)/255
    anal = 4*mp.pi*G*rhoH(r)*r**2
    c10b2 = max(c10b2, rel(rich, anal))
    c10b2raw = max(c10b2raw, rel(d2, anal))
    ratio_track.append(rel(d1, anal)/max(rel(d2, anal), mp.mpf("1e-60")))
# convergence ratio: refined/reference should be ~ (1/4)^6 ~ 2.4e-4 for an
# order-6 effective scheme after one Richardson step; require measurable convergence
conv = max(ratio_track)
check("C10b-ii fd(Richardson order-4) d/dr[r^2 mu g] = 4 pi G rho r^2", c10b2, mp.mpf("1e-20"))
print(f"[C10b] analytic rel residual: {mp.nstr(c10b1,4)} ; fd(Richardson) rel residual: "
      f"{mp.nstr(c10b2,4)} (raw order-4 at h/4: {mp.nstr(c10b2raw,4)}; max h-refinement ratio {mp.nstr(conv,3)})")

# C11: branch-fidelity comparison table (Q vs EXP vs RAR vs MU2) at select x
def yRAR_from_x(x):   # solve x = y*nu_RAR(y) = y/(1-exp(-sqrt y)) by bisection
    hi = x + 1
    while hi/(1 - mp.e**(-mp.sqrt(hi))) < x: hi *= 2
    lo = mp.mpf(0); fa = -1
    for _ in range(220):
        m = (lo + hi)/2
        fm = m/(1 - mp.e**(-mp.sqrt(m))) - x
        if fm == 0: return m
        if (fm > 0) == (fa > 0):
            lo, fa = m, fm
        else:
            hi = m
        if hi - lo < mp.mpf("1e-49"): break
    return (lo + hi)/2
def muRAR(x):
    y = yRAR_from_x(x)
    return y/x
def muMU2(x):
    return 1 - (1 + x/mp.mpf(2))**-2
print("\n[C11] branch fidelity at selected x = g/a0 (comparison ONLY, no transfer):")
print(f"  {'x':>8} {'mu_Q':>12} {'mu_EXP(hist)':>14} {'mu_RAR':>12} {'mu_MU2':>12}")
for xv in [mp.mpf("0.1"), mp.mpf("0.31"), mp.mpf("1"), mp.mpf("3.16"), mp.mpf("10")]:
    print(f"  {mp.nstr(xv,4):>8} {mp.nstr(muQ(xv),12):>12} {mp.nstr(muEXP(xv),14):>14} "
          f"{mp.nstr(muRAR(xv),12):>12} {mp.nstr(muMU2(xv),12):>12}")

# C12: small-x and large-x series (rational coefficients via sympy)
series_out = {}
try:
    import sympy as sp
    z = sp.symbols('z')
    smallQ = sp.series((sp.sqrt(1+4*z**2)-1)/(2*z), z, 0, 9)
    smallE = sp.series(1 - sp.exp(-z), z, 0, 6)
    largeQ = sp.series((sp.sqrt(1+4*z**2)-1)/(2*z), z, sp.oo, 5)
    dsmall = sp.series((1 - sp.exp(-z)) - (sp.sqrt(1+4*z**2)-1)/(2*z), z, 0, 4)
    series_out = {"small_muQ": str(smallQ), "small_muEXP": str(smallE),
                  "large_muQ": str(largeQ), "diff_small": str(dsmall)}
    print("[C12] sympy small-x mu_Q:", smallQ)
    print("[C12] sympy small-x mu_EXP:", smallE)
    print("[C12] sympy large-x mu_Q:", largeQ)
    print("[C12] sympy d(x) = mu_EXP - mu_Q small-x:", dsmall)
except ImportError:
    print("[C12] sympy unavailable; mpmath.taylor instead")
    tq = mp.taylor(lambda x: muQ(x), 0, 8)
    te = mp.taylor(lambda x: muEXP(x), 0, 4)
    series_out = {"taylor_muQ": [mp.nstr(k, 4) for k in tq],
                  "taylor_muEXP": [mp.nstr(k, 4) for k in te]}
    print("[C12] taylor mu_Q coeffs:", series_out["taylor_muQ"])
    print("[C12] taylor mu_EXP coeffs:", series_out["taylor_muEXP"])

# C13: footing examples (dimensional, footings kept SEPARATE)
print("\n[C13] footing examples (a0_can = 9.3619e-11 ; a0_alt = 1.1279e-10 m/s^2):")
for name, a0 in [("canonical", a0can), ("alternative", mp.mpf("1.1279e-10"))]:
    print(f"  {name}: a0 = {mp.nstr(a0, 8)} m/s^2 ; Newtonian offset a0/2 = {mp.nstr(a0/2, 8)} m/s^2")
    for Mb in [mp.mpf("1e10"), mp.mpf("1e11"), mp.mpf("1e12")]:
        Mkg = Mb * M_sun
        rM = mp.sqrt(G*Mkg/a0)
        vf4 = G*Mkg*a0
        print(f"    M_b={mp.nstr(Mb,3)} M_sun: r_M = {mp.nstr(rM,6)} m = {mp.nstr(rM/pc,6)} pc "
              f"= {mp.nstr(rM/pc/1000,6)} kpc ; v_flat = {mp.nstr(vf4**mp.mpf('0.25'),6)} m/s")
    g0 = mp.mpf("1e-10")
    print(f"    g = 1e-10 m/s^2 -> x = g/a0 = {mp.nstr(g0/a0, 6)} -> mu_Q = {mp.nstr(muQ(g0/a0), 6)}, "
          f"y = B/a0 = {mp.nstr(yofx(g0/a0), 6)}")

print(f"\ntotal wall time: {time.time()-t0:.2f} s")
print("ALL CHECKS DONE")
