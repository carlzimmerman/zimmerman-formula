"""p20c: branch A2 (sonic horizon around a mass) and branch B at FINITE khronon speed. Criteria: SETUP.md (frozen first). G = c = 1.

A2. k-essence P(s), s = 2X, on a rolling background phi = q t + psi(r) (flat region, galaxy scale); psi' = v(r) is the a0 field's gradient,
    v = q c_s (r_h/r)^p (p = 1 deep MOND, p = 2 Newtonian), so the flow equals the sound speed at r_h. Family P = s^n (c_s^2 = 1/(2n-1)).
    Effective metric G^{mn} = P_X g^{mn} - P_XX d^m phi d^n phi; horizon G^{rr} = 0; kappa = (1/2)|d_r G^{rr}|/sqrt|D| (constant conformal factors cancel),
    Killing vector = lab d_t. In deep MOND v = sqrt(M a0)/r, so r_h = sqrt(M a0)/(q c_s): the radius scales as sqrt(M).
B (finite speed). Any khronon: a universal horizon is where u.chi = 0 with u unit timelike, so chi = d_t is spacelike there: g(chi,chi) = -f > 0.
    In SdS, f < 0 only for r < r_b (black-hole side) or r > r_c. Black-hole side: Lambda r^2 < Lambda r_b^2 <= 1 for EVERY khronon speed.
    So Lambda A = 32 pi^2 (Lambda r^2 = 8 pi) could only sit beyond the cosmological horizon, where a khronon matched to cosmic time has u.chi -> -1 (no UH).

Run: python3 p20c_A2_and_finite_speed_khronon.py  |  MUTATE=1: drop the P_XX term in G^{rr} (A2-0 must fail) and flip the sign of f in B (B1 must fail)
"""
import os, sys
import numpy as np
import sympy as sp
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(nm, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + nm)

# ---------------- A2
r, rh, q, n = sp.symbols("r r_h q n", positive=True)
def kappa_rh(nv, p):
    cs = 1 / sp.sqrt(2 * nv - 1)
    v = q * cs * (rh / r)**p
    s = q**2 - v**2
    Ps = s**nv
    S = sp.symbols("S", positive=True)
    P1 = sp.diff(S**nv, S).subs(S, s); P2 = sp.diff(S**nv, S, 2).subs(S, s)
    PX, PXX = 2 * P1, 4 * P2
    Gtt, Gtr, Grr = -PX - PXX * q**2, PXX * q * v, PX - (0 if MUTATE else PXX) * v**2
    D = Gtt * Grr - Gtr**2
    zero = sp.simplify(Grr.subs(r, rh))
    k = sp.Rational(1, 2) * sp.Abs(sp.diff(Grr, r)) / sp.sqrt(sp.Abs(D))
    return zero, sp.nsimplify(sp.simplify((k * rh).subs(r, rh)))
rows = []
for nv in (sp.Rational(3, 2), 2, 3, 5):
    for p in (1, 2):
        z, kr = kappa_rh(nv, p)
        rows.append((nv, p, z, kr))
        print(f"   A2: P = s^{nv} (c_s^2 = {1/(2*nv-1)}), v ~ r^-{p}:  G^rr(r_h) = {z},  kappa r_h = {kr} = {float(kr):.4f}")
check("A2-0 the effective metric's horizon is exactly where the flow speed equals c_s (G^rr(r_h) = 0)", all(z == 0 for _, _, z, _ in rows))
# POST-HOC (changed after the first run): the pre-written A2-1 guessed kappa r_h = 1/2 for every n in deep MOND; the output refuted it.
# The eight rows follow kappa r_h = p sqrt(2n-1)/(2(n-1)); kappa r_h = 1/2 in deep MOND (p = 1) needs n^2 - 4n + 2 = 0, n = 2 + sqrt 2.
formula = lambda nv, p: p * sp.sqrt(2 * nv - 1) / (2 * (nv - 1))
check("A2-1 kappa r_h = p sqrt(2n-1)/(2(n-1)) for all eight rows (a pure number set by P and the profile slope, independent of M)",
      all(sp.simplify(kr - formula(nv, p)) == 0 for nv, p, z, kr in rows))
nhalf = [x for x in sp.solve(sp.Eq(formula(n, 1), sp.Rational(1, 2)), n) if x.is_real and x > 1]
print(f"   A2: kappa r_h = 1/2 in deep MOND needs the exponent n = {nhalf} = {[float(x) for x in nhalf]} (a tuned P; c_s^2 = {[sp.nsimplify(1/(2*x-1)) for x in nhalf]})")
check("A2-1b the kappa half of the target needs one tuned exponent n = 2 + sqrt 2: INSERTION (criterion 2)",
      len(nhalf) == 1 and sp.simplify(nhalf[0] - (2 + sp.sqrt(2))) == 0)
Ma0, Lam = sp.symbols("Ma0 Lambda", positive=True)
cs = sp.symbols("c_s", positive=True)
rh_M = sp.sqrt(Ma0) / (q * cs)
Msol = sp.solve(sp.Eq(Lam * rh_M**2, 8 * sp.pi), Ma0)[0]
print(f"   A2: r_h = sqrt(M a0)/(q c_s); Lambda r_h^2 = 8 pi only for the one mass  M a0 = {Msol}")
check("A2-2 Lambda r_h^2 = 8 pi is met only by choosing M (and the free roll q): INSERTION, and the radius is mass-dependent (criteria 2, 3 fail)",
      sp.simplify(sp.diff(rh_M, Ma0)) != 0 and Msol.has(q))

# ---------------- B at finite speed: where can u.chi = 0 occur in SdS, and what Lambda r^2 does it allow?
Lv = 1.0; bh_max = 0.0; out_min = np.inf
for m in np.linspace(1e-4, 1 / (3 * np.sqrt(Lv)) * 0.999999, 3000):
    rts = np.roots([-Lv / 3, 0, 1, -2 * m]); rr = np.sort(rts[(abs(rts.imag) < 1e-12) & (rts.real > 0)].real)
    rb, rc = rr[0], rr[1]
    grid = np.linspace(1e-3, 3 * rc, 4000)
    f = 1 - 2 * m / grid - Lv * grid**2 / 3
    if MUTATE: f = -f
    spacelike = grid[f < 0]                                   # where chi = d_t is spacelike (a UH can only sit here)
    inner = spacelike[spacelike < rb]; outer = spacelike[spacelike > rb]
    if len(inner): bh_max = max(bh_max, Lv * inner.max()**2)
    if len(outer): out_min = min(out_min, Lv * outer.min()**2)
print(f"   B: chi spacelike on the black-hole side only where Lambda r^2 <= {bh_max:.4f}; beyond the cosmological horizon from Lambda r^2 >= {out_min:.4f}")
check("B1 for ANY khronon speed a black-hole-side universal horizon has Lambda r^2 < 1 (it lies inside r_b, and Lambda r_b^2 <= 1): Lambda r^2 = 8 pi impossible",
      bh_max < 1.0 + 1e-6 and bh_max > 0.5)
# beyond r_c: cosmic-time khronon in pure dS has u.chi = -1 everywhere (flat slicing: u^r = H r, u_t^2 = f + H^2 r^2 = 1)
H, rr_ = sp.symbols("H rr", positive=True)
check("B2 beyond the cosmological horizon a khronon matched to cosmic time has u.chi = -1 (pure dS, exact), so no universal horizon sits at Lambda r^2 = 8 pi",
      sp.simplify((1 - H**2 * rr_**2) + (H * rr_)**2 - 1) == 0)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
