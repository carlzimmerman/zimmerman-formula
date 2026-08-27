#!/usr/bin/env python3
r"""SF55: MMG constraint-first chassis -- the y=0 degenerate branch, characterized.

y = (c^2/a0)|D ln N| = |grad Phi|/a0 (weak field Phi = c^2 ln N).  So y = 0 is the
ZERO-ACCELERATION / DEEP-MOND point, NOT the Newtonian limit: the Newtonian branch is
y -> infinity where mu -> 1 and the lapse operator is uniformly elliptic.  (FINAL_STATUS.md
line 46 calls y=0 "the exact Newtonian (deep-GR) limit" -- that label is wrong; flagged,
frozen doc not modified.)  Question posed by the gate: is y=0 a RANK CHANGE of the
second-class pair (pi_N, C_M) or a PDE-REGULARITY boundary?  Answer derived here: it is
BOTH, on different strata, and the answer is kernel-agnostic:

 P1  Symbol degeneracy: lambda_perp = mu(y), lambda_par = mu + y mu' both vanish LINEARLY
     (~y, ~2y) at y=0 for mu_exp AND mu_n (n=5,10): identical degeneracy class (the flux
     mu(y)*g is the 3-Laplacian |g|g/a0 to leading order).  At y -> infinity both -> 1:
     the actual Newtonian branch is uniformly elliptic and needs NO separate treatment.
 P2  Strict monotonicity: d(y mu)/dy > 0 for all y > 0, exactly, both kernels  =>  the
     flux field A(xi) = mu(|xi|/a0) xi is strictly monotone  =>  the nonlinear constraint
     C_M = 0 has a UNIQUE weak solution for ln N up to the additive constant (the k=0 mode
     already handled in SF54).  Well-posedness survives the pointwise degeneracy.
 P3  ISOLATED zeros (generic configurations: critical points of Phi): numerical spectrum
     of the linearized lapse operator L_N v = div(A grad v) on a periodic 2D grid with A
     vanishing LINEARLY at isolated points: kernel = constants ONLY (1 zero mode), no
     negative modes, spectral gap stable under refinement  =>  NO rank change; y=0 there
     is a PDE-regularity boundary only (C^{1,alpha} solutions at critical points).
     DIMENSION HONESTY (found while building this test): a 1D toy is MISLEADING here --
     a point disconnects a line and the weighted capacity across a linear zero of A
     vanishes logarithmically (gap ~ 1/ln N -> 0), which is a 1D topology artifact.
     In d >= 2 an isolated point does not disconnect the slice and the weight
     A ~ dist(x, x0) is Muckenhoupt-A2, so the weighted Poincare inequality holds and
     the gap survives.  The test below is therefore 2D; 3D is safer still (codimension).
 P4  OPEN-SET zeros (y = 0 on a region: force-free cavity / exact FLRW / Minkowski):
     the spectrum acquires an EXTENSIVE set of zero modes -- every lapse variation
     supported in the dead region costs zero energy (kernel is infinite-dimensional in
     the continuum), i.e. delta N is COMPLETELY undetermined there at linear order  =>
     GENUINE rank change of the LINEARIZED pair on this stratum.  The maximal case
     (y = 0 everywhere) IS the k=0 homogeneous sector of SF54 -- the branches meet.
 P5  What resolves the open-set stratum: the NONLINEAR constraint.  Response to a source
     on a y=0 background is nonanalytic ~ sqrt(source): the spherical relation
     mu(g/a0) g = g_N gives g = sqrt(a0 g_N) as g_N -> 0 -- which is the deep-MOND/BTFR
     law itself.  Verified symbolically and by a numeric slope fit (d log g/d log g_N ->
     1/2) for mu_exp, mu_5, mu_10.  So the "strong coupling" at y=0 is precisely the
     designed deep-MOND nonlinearity; linear perturbation theory around y=0 backgrounds
     is invalid (sqrt expansions), the nonlinear elliptic problem stays well-posed (P2).

Exit 0 = all checks pass.
"""
import sys
import numpy as np
import sympy as sp

FAILS = []
def check(label, cond):
    ok = bool(cond)
    print(("  [OK]  " if ok else "  [FAIL]") + label)
    if not ok:
        FAILS.append(label)

y = sp.Symbol("y", positive=True)
KERNELS = [("mu_exp", 1 - sp.exp(-y)),
           ("mu_5",  y / (1 + y ** 5) ** sp.Rational(1, 5)),
           ("mu_10", y / (1 + y ** 10) ** sp.Rational(1, 10))]

print("=" * 78)
print("SF55: MMG y=0 DEGENERATE BRANCH")
print("=" * 78)

# ---------------------------------------------------------------- P1
print("\n--- P1: symbol degeneracy at y=0; uniform ellipticity at y->infinity ---")
for name, mu in KERNELS:
    lam_perp = mu
    lam_par = sp.simplify(sp.diff(y * mu, y))
    s_perp = sp.series(lam_perp, y, 0, 2).removeO()
    s_par = sp.series(lam_par, y, 0, 2).removeO()
    check(f"{name}: lambda_perp ~ y, lambda_par ~ 2y at y->0 (LINEAR vanishing, both)",
          sp.limit(lam_perp / y, y, 0) == 1 and sp.limit(lam_par / y, y, 0) == 2)
    check(f"{name}: y->inf limits lambda_perp -> 1, lambda_par -> 1 (Newtonian branch "
          "uniformly elliptic)",
          sp.limit(lam_perp, y, sp.oo) == 1 and sp.limit(lam_par, y, sp.oo) == 1)
print("  => y=0 is the DEEP-MOND zero-acceleration point (mu ~ y: 3-Laplacian class);")
print("     the label 'Newtonian limit' for y=0 in FINAL_STATUS.md:46 is a MISLABEL.")

# ---------------------------------------------------------------- P2
print("\n--- P2: strict monotonicity d(y mu)/dy > 0 for all y > 0 (exact) ---")
# mu_exp: d(y(1-e^-y))/dy = 1 - e^-y + y e^-y = 1 - (1-y)e^-y > 0 for y>0:
#   y<=1: 1-(1-y)e^-y >= 1-e^-y > 0;  y>1: (1-y)<0 so expression > 1 > 0.
expr = sp.simplify(sp.diff(y * (1 - sp.exp(-y)), y) - (1 - (1 - y) * sp.exp(-y)))
check("mu_exp: d(y mu)/dy = 1 - (1-y)e^{-y} (exact closed form)", expr == 0)
yy = np.logspace(-8, 3, 4000)
f = sp.lambdify(y, sp.diff(y * (1 - sp.exp(-y)), y), "numpy")
check("mu_exp: d(y mu)/dy > 0 on y in [1e-8, 1e3] (sweep)", bool(np.all(f(yy) > 0)))
for n in (5, 10):
    mun = y / (1 + y ** n) ** sp.Rational(1, n)
    d = sp.simplify(sp.diff(y * mun, y)
                    - y * (2 + y ** n) / (1 + y ** n) ** (1 + sp.Rational(1, n)))
    check(f"mu_{n}: d(y mu)/dy = y(2+y^n)/(1+y^n)^(1+1/n) > 0 exact (positive factors)",
          d == 0)
print("  => flux A(xi) = mu(|xi|/a0) xi strictly monotone => unique weak solution of")
print("     C_M = 0 up to the additive constant mode (monotone-operator theory).")

# ---------------------------------------------------------------- P3 / P4
print("\n--- P3/P4: spectrum of linearized L_N (2D periodic); isolated vs open-set ---")
def spectrum_counts_2d(Afun, N):
    """L = -div(A grad .) on an N x N periodic grid via edge weights (A at edge
    midpoints); symmetric PSD.  Return (n_zero, n_negative, gap)."""
    h = 2 * np.pi / N
    idx = lambda i, j: (i % N) * N + (j % N)
    L = np.zeros((N * N, N * N))
    for i in range(N):
        for j in range(N):
            for (i2, j2, xm, ym) in (
                    (i + 1, j, (i + 0.5) * h, j * h),      # x-edge midpoint
                    (i, j + 1, i * h, (j + 0.5) * h)):     # y-edge midpoint
                a = Afun(xm, ym)
                p_, q_ = idx(i, j), idx(i2, j2)
                L[p_, p_] += a; L[q_, q_] += a; L[p_, q_] -= a; L[q_, p_] -= a
    L /= h ** 2
    w = np.linalg.eigvalsh(L)
    tol = 1e-9 * max(1.0, np.max(np.abs(w)))
    nz = int(np.sum(np.abs(w) < tol))
    nneg = int(np.sum(w < -tol))
    gap = float(np.sort(np.abs(w))[nz]) if nz < N * N else 0.0
    return nz, nneg, gap

lam_par_funs = {}
for name, mu in KERNELS:
    if name == "mu_exp":
        lam_par_funs[name] = sp.lambdify(y, 1 - (1 - y) * sp.exp(-y), "numpy")
    else:
        n = 5 if name == "mu_5" else 10
        lam_par_funs[name] = sp.lambdify(
            y, y * (2 + y ** n) / (1 + y ** n) ** (1 + sp.Rational(1, n)), "numpy")

ystar = 3.0
print("  isolated zeros: y(x,z) = y* sqrt(sin^2 x + sin^2 z)  (4 point zeros, linear)")
for name in lam_par_funs:
    lp = lam_par_funs[name]
    ybg = lambda xm, zm: ystar * np.sqrt(np.sin(xm) ** 2 + np.sin(zm) ** 2)
    rows = []
    for N in (16, 24, 32):
        nz, nneg, gap = spectrum_counts_2d(lambda xm, zm: lp(ybg(xm, zm)), N)
        rows.append((N, nz, nneg, gap))
    print(f"    {name}: " + "  ".join(f"N={N}: zeros={nz} neg={nneg} gap={gap:.4f}"
                                       for N, nz, nneg, gap in rows))
    g1, g2, g3 = rows[0][3], rows[1][3], rows[2][3]
    check(f"P3 {name}: kernel = constants only (1 zero mode), 0 negative modes, "
          "gap converging to a nonzero limit (2D: isolated zero does not disconnect)",
          all(nz == 1 and nneg == 0 for _, nz, nneg, _ in rows)
          and abs(g3 - g2) <= abs(g2 - g1) + 1e-12 and g3 > 0.05)

print("  open-set zero: y(x,z) = y* max(0, sin x): y = 0 on the half-strip x in (pi,2pi)")
for name in lam_par_funs:
    lp = lam_par_funs[name]
    N = 24
    nz, nneg, gap = spectrum_counts_2d(
        lambda xm, zm: lp(np.maximum(ystar * np.sin(xm), 0.0)), N)
    dead_nodes = sum(1 for i in range(N) for j in range(N)
                     if np.sin((i - 0.5) * 2 * np.pi / N) <= 0
                     and np.sin((i + 0.5) * 2 * np.pi / N) <= 0
                     and np.sin(i * 2 * np.pi / N) <= 0)
    print(f"    {name}: N={N}: zeros={nz} neg={nneg}  (nodes with all incident edge "
          f"weights ~0: about {dead_nodes})")
    check(f"P4 {name}: open-set degeneracy => EXTENSIVE kernel (every delta N supported "
          "in the dead region; >> 1 zero modes): rank change of the linearized pair",
          nz > 10 and nneg == 0)
print("  => isolated zeros: NO rank change (regularity boundary only, d >= 2);")
print("     open-set zeros: linearized rank change (delta N free in the cavity);")
print("     maximal case y==0 everywhere = the k=0 homogeneous sector (SF54).")

# ---------------------------------------------------------------- P5
print("\n--- P5: nonanalytic sqrt response on y=0 backgrounds (both kernels) ---")
gN, a0 = sp.symbols("g_N a0", positive=True)
g = sp.Symbol("g", positive=True)
for name, mu in KERNELS:
    mug = mu.subs(y, g / a0) * g           # algebraic spherical relation mu(g/a0) g = g_N
    # leading behavior: mu ~ y => mu(g/a0) g ~ g^2/a0 = g_N => g = sqrt(a0 g_N)
    lead = sp.limit(mug / (g ** 2 / a0), g, 0)
    check(f"{name}: mu(g/a0) g -> g^2/a0 as g->0  =>  g = sqrt(a0 g_N) (BTFR law; "
          "d g/d g_N -> infinity: L_N|lin = 0 on the y=0 stratum)", lead == 1)
    # numeric slope fit d log g / d log g_N on g_N/a0 in [1e-8, 1e-3]
    mugf = sp.lambdify((g, a0), mug, "numpy")
    gNs = np.logspace(-8, -3, 12)          # in units a0 = 1
    gs = []
    for gn in gNs:
        lo, hi = 1e-12, 10.0               # bisection on monotone mu(g)g - gn
        for _ in range(200):
            mid = np.sqrt(lo * hi)
            if mugf(mid, 1.0) < gn:
                lo = mid
            else:
                hi = mid
        gs.append(np.sqrt(lo * hi))
    slope = np.polyfit(np.log(gNs), np.log(gs), 1)[0]
    check(f"{name}: numeric slope d log g/d log g_N = {slope:.4f} -> 1/2 (sqrt branch)",
          abs(slope - 0.5) < 0.01)
print("  => linear perturbation theory around y=0 backgrounds is INVALID (sqrt")
print("     expansions); the nonlinear constraint resolves it -- this nonanalyticity")
print("     IS deep MOND working as designed, not an extra propagating mode.")

print("\n" + "=" * 78)
if FAILS:
    print("SF55 RESULT: FAIL --", FAILS)
    sys.exit(1)
print("SF55 RESULT: ALL CHECKS PASS")
print("  y=0 = deep-MOND degenerate-elliptic boundary: regularity boundary at isolated")
print("  zeros (no rank change, kernel = known constant mode only); linearized rank")
print("  change only on y==0 open sets, resolved nonlinearly (unique weak solution,")
print("  sqrt response); Newtonian branch y->inf uniformly elliptic. Kernel-agnostic.")
print("=" * 78)
