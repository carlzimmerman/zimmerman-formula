#!/usr/bin/env python3
"""
LANE C -- DRESSED SPECTRAL POSITIVITY (one-loop, dS KMS bath), NO toy spectra.

Framework premises (reasoned from the framework's OWN definitions):
  * K(z) = (sqrt(1+4z)-1)/(2 sqrt z), Herglotz-Nevanlinna with UNIQUE positive
    Borel measure on the negative real axis (operator_definition.py, banked v4):
        rho_A(t) = (1 - sqrt(1-4|t|)) / (2 pi sqrt|t|)   on -1/4 < t < 0
        rho_B(t) = 1 / (2 pi sqrt|t|)                    on t < -1/4
  * Dynamical-sector frequency identification: z = -omega^2 / a0^2  (c=1 units;
    in SI, a0 -> a0/c as an inverse time).  Branch points z=0 -> omega=0 and
    z=-1/4 -> omega* = a0/(2c).
  * dS bath is KMS at T = H/(2 pi), i.e. beta = 2 pi / H.
  * u is NON-dynamical (Dirac closure banked): the loop lines are matter quanta
    in the KMS bath; the one-loop (second-order) response of the K-vertex is the
    KMS-weighted self-convolution of the vertex's own cut density:
        rho_1loop(w) = Int dw'/(2pi) rho_K(w') rho_K(w-w') [1 + n(w') + n(w-w')]
    Standard identity (verified below in code, not assumed):
        [1+n(w1)+n(w2)] = (1 - e^{-beta(w1+w2)}) (1+n(w1)) (1+n(w2)),
    so with the Wightman ("power spectrum") function
        Gp(w) = (1+n(w)) rho_odd(w) = rho_odd(w) / (1 - e^{-beta w}),
    the dressed density is
        rho_1loop(w) = (1 - e^{-beta w}) * (Gp * Gp)(w) / (2 pi).
    KMS detailed balance for the dressed object: Gp2(-w)/Gp2(w) = e^{-beta w},
    which we CHECK numerically rather than assume.

Frequency-space cut density (change of variables t = -w^2/a0^2, |dt/dw| = 2w/a0^2):
    region A (0 < w < a0/2):  rho(w) = (1 - sqrt(1 - 4 w^2/a0^2)) / (pi a0)
    region B (w > a0/2):      rho(w) = 1 / (pi a0)
  (continuous at w=a0/2, value 1/(pi a0); vertical tangent from the A side).
Bosonic spectral function is ODD: rho_odd(-w) = -rho_odd(w); positivity means
sign(w) * rho(w) >= 0.

What is COMPUTED (not argued):
  1. sanity anchor: Int dmu/(1+t^2) = 0.2295 (framework's own normalization);
  2. the thermal-factor identity above, numerically at random points;
  3. rho_1loop(w) on a grid resolving BOTH branch-point edges (w -> 0+, w -> a0/2,
     and the dressed 2-particle edge w -> a0) up through galactic w ~ 1e-15 s^-1;
  4. KMS detailed balance of the dressed density;
  5. BOTH footings: a0 = 9.36e-11 (canonical, H_Lambda) and 1.13e-10 (alt, H0);
  6. GHOST CONTROL: hand-inserted negative-weight line in the cut density ->
     the SAME pipeline must FLAG negativity, else the pass is vacuous.

Honesty: positivity of (Gp*Gp) for a POSITIVE measure is a theorem (convolution
of nonnegative functions); the numerics here verify (a) that the framework's
density really is everywhere nonnegative including at the edges after the
frequency mapping, (b) that the KMS weights never flip a sign numerically,
(c) that the detector is sharp enough to catch a ghost. This lane is a
positivity/thermalization structure check of the second-order response; it is
NOT the full dS one-loop self-energy with graviton lines and momentum integrals.
"""
import numpy as np
from scipy import integrate
import sys

FAIL = []

# ----------------------------------------------------------------------
# 0. Physical constants and BOTH footings
# ----------------------------------------------------------------------
c = 2.998e8                      # m/s
H0 = 2.184e-18                   # s^-1  (67.4 km/s/Mpc)
Om_L = 0.685
H_Lam = H0 * np.sqrt(Om_L)       # s^-1

FOOTINGS = {
    "canonical (a0=cH_L/Z=9.36e-11, bath H_Lambda)": dict(a0=9.36e-11, H=H_Lam),
    "alt      (a0=cH0-based =1.13e-10, bath H0)":    dict(a0=1.13e-10, H=H0),
}

# ----------------------------------------------------------------------
# 1. The framework's own cut density in t, sanity anchor Int dmu/(1+t^2)
# ----------------------------------------------------------------------
def rho_t(t):
    at = np.abs(t)
    if -0.25 < t < 0:
        return (1.0 - np.sqrt(1.0 - 4.0*at)) / (2.0*np.pi*np.sqrt(at))
    elif t <= -0.25:
        return 1.0 / (2.0*np.pi*np.sqrt(at))
    return 0.0

IA, _ = integrate.quad(lambda t: rho_t(t)/(1+t*t), -0.25, 0, points=[-0.25], limit=200)
IB, _ = integrate.quad(lambda t: rho_t(t)/(1+t*t), -np.inf, -0.25, limit=200)
norm = IA + IB
print(f"[anchor] Int dmu/(1+t^2) = {norm:.4f}   (framework value 0.2295)")
if abs(norm - 0.2295) > 2e-3:
    FAIL.append(f"measure normalization off: {norm}")

# ----------------------------------------------------------------------
# 2. Thermal-factor identity check (the convolution kernel is EXACTLY the
#    textbook [1+n1+n2] bubble weight -- verify, don't assume)
# ----------------------------------------------------------------------
from mpmath import mp, mpf, exp as mexp
mp.dps = 100                     # float64 suffers catastrophic cancellation here;
                                 # worst case loses ~b|w|/ln10 ~ 18 digits, so 100 dps
                                 # leaves >80 good digits against a 1e-40 tolerance
rng = np.random.default_rng(7)
bad = 0; npts = 500
for _ in range(npts):
    b = mpf(rng.uniform(0.1, 5.0))
    w1, w2 = (mpf(v) for v in rng.uniform(-8, 8, 2))
    if abs(w1) < 1e-3 or abs(w2) < 1e-3 or abs(w1+w2) < 1e-3:
        continue
    n = lambda w: 1/(mexp(b*w) - 1)
    lhs = 1 + n(w1) + n(w2)
    rhs = (1 - mexp(-b*(w1+w2))) * (1+n(w1)) * (1+n(w2))
    if abs(lhs - rhs) > mpf('1e-40') * max(abs(lhs), abs(rhs), 1):
        bad += 1
print(f"[identity] 1+n1+n2 == (1-e^-b(w1+w2))(1+n1)(1+n2): {bad} failures / {npts} random points (100-digit arithmetic)")
if bad:
    FAIL.append("thermal identity failed")

# ----------------------------------------------------------------------
# 3. Dimensionless engine.  x = w / w*,  w* = a0/(2c)  (branch point at x=1).
#    bhat = beta * w* = (2 pi / H) * a0/(2c) = pi * a0 / (c H)  [= pi/Z]
#    rho_hat(x) (units 1/(pi a0) stripped -- overall positive constant):
#       0<x<1 : 1 - sqrt(1-x^2) ;  x>1 : 1 ;  odd in x.
# ----------------------------------------------------------------------
def make_engine(bhat, ghost=None):
    """ghost = (amplitude, x0, width) inserts a NEGATIVE Gaussian line."""
    def rho_pos(x):          # density for x>0
        x = float(x)
        if x <= 0.0:
            return 0.0
        r = (1.0 - np.sqrt(max(0.0, 1.0 - x*x))) if x < 1.0 else 1.0
        if ghost is not None:
            A, x0, wdt = ghost
            r -= A * np.exp(-((x - x0)/wdt)**2)
        return r

    def rho_odd(x):
        return rho_pos(x) if x >= 0 else -rho_pos(-x)

    def Gp(x):               # Wightman: rho_odd(x) / (1 - e^{-bhat x}), >=0 iff no ghost
        x = float(x)
        if abs(x) < 1e-12:
            return 0.0       # rho ~ x^2/2 near 0 -> Gp ~ x/(2 bhat) -> 0
        d = -np.expm1(-bhat*x)
        return rho_odd(x)/d

    TAIL = 60.0/bhat         # e^{-60} cutoff for the thermal tails

    def Gp2(x):              # (Gp * Gp)(x) / (2 pi)
        lo, hi = -TAIL, x + TAIL
        base = [-1.0, 0.0, 1.0, x-1.0, x, x+1.0]
        if ghost is not None:                      # resolve the narrow line
            A, x0, wdt = ghost
            for s in (-1, 1):
                for k in (0.0, 3.0):
                    base += [s*(x0+k*wdt), s*(x0-k*wdt),
                             x - s*(x0+k*wdt), x - s*(x0-k*wdt)]
        pts = sorted({p for p in base if lo < p < hi})
        val, err = integrate.quad(lambda xp: Gp(xp)*Gp(x-xp), lo, hi,
                                  points=pts, limit=400, epsabs=1e-13, epsrel=1e-10)
        return val/(2*np.pi), err/(2*np.pi)

    def rho_dressed(x):
        g, err = Gp2(x)
        return -np.expm1(-bhat*x) * g, err
    return rho_pos, Gp, Gp2, rho_dressed

# ----------------------------------------------------------------------
# 4. Output grid: resolve edges x=0, x=1 (branch pt a0/2), x=2 (2-particle
#    edge a0), then log out to the galactic band.
# ----------------------------------------------------------------------
def xgrid(x_gal):
    g = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9,
         0.99, 0.999, 1-1e-4, 1-1e-6, 1.0, 1+1e-6, 1+1e-4, 1.001, 1.01,
         1.1, 1.5, 1.9, 1.99, 1.999, 2-1e-4, 2-1e-6, 2.0, 2+1e-6, 2+1e-4,
         2.001, 2.01, 2.1, 2.5, 3.0, 5.0, 10.0, 30.0, 100.0, 300.0, 1000.0,
         3000.0, x_gal, 2*x_gal]
    return np.array(sorted(set(g)))

def run_footing(name, a0, H, ghost=None, verbose=True):
    wstar = a0/(2*c)                       # s^-1, branch point
    bhat = np.pi * a0 / (c*H)              # beta * wstar  (= pi/Z)
    x_gal = 1e-15 / wstar                  # galactic 1e-15 s^-1 in units of wstar
    rho_pos, Gp, Gp2, rho_dressed = make_engine(bhat, ghost)

    if verbose:
        print(f"\n=== {name} ===")
        print(f"    w* = a0/2c = {wstar:.4e} s^-1 ; beta*w* = {bhat:.4f} "
              f"(=pi/Z, Z={np.pi/bhat:.3f}) ; galactic 1e-15 s^-1 -> x={x_gal:.1f}")

    # free-density positivity (incl. edges) -- the input to the theorem
    xs_free = np.concatenate([np.linspace(1e-9, 1, 4001), np.geomspace(1, 2*x_gal, 2001)])
    free_min = min(rho_pos(x) for x in xs_free)
    if verbose:
        print(f"    free cut density min over grid: {free_min:.3e}  "
              f"({'OK >= 0' if free_min >= -1e-15 else 'NEGATIVE'})")

    # dressed density scan
    worst = (np.inf, None); rows = []
    for x in xgrid(x_gal):
        r, err = rho_dressed(x)
        rows.append((x, r, err))
        if r < worst[0]:
            worst = (r, x)
    # tolerance: quadrature error, never sign-blind
    viol = [(x, r, e) for (x, r, e) in rows if r < -max(1e-12, 10*e)]

    # KMS detailed balance of the DRESSED object: Gp2(-x) e^{bx} / Gp2(x) == 1
    kms_dev = 0.0
    for xk in (0.05, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 40.0):
        gp, _ = Gp2(xk); gm, _ = Gp2(-xk)
        ratio = gm*np.exp(bhat*xk)/gp
        kms_dev = max(kms_dev, abs(ratio-1))
    if verbose:
        print(f"    dressed rho_1loop: min value {worst[0]:.6e} at x={worst[1]}"
              f"  ({'POSITIVE everywhere' if not viol else 'VIOLATIONS: '+str(viol)})")
        print(f"    edge values: x=1e-6:{dict((x,r) for x,r,_ in rows)[1e-6]:.3e}"
              f"  x=1:{dict((x,r) for x,r,_ in rows)[1.0]:.6e}"
              f"  x=2:{dict((x,r) for x,r,_ in rows)[2.0]:.6e}"
              f"  x_gal:{dict((x,r) for x,r,_ in rows)[x_gal]:.4e}")
        print(f"    KMS detailed balance (dressed): max |ratio-1| = {kms_dev:.2e}"
              f"  ({'OK' if kms_dev < 1e-6 else 'BROKEN'})")
        # large-x analytic cross-check: Gp2 ~ (x-2)/(2 pi) from the flat continuum
        gg, _ = Gp2(x_gal)
        pred = (x_gal-2)/(2*np.pi)
        print(f"    UV cross-check at x_gal: Gp2={gg:.4f} vs flat-continuum (x-2)/2pi={pred:.4f}"
              f"  (ratio {gg/pred:.4f})")
    return viol, kms_dev, worst, rows, bhat, x_gal

# ----------------------------------------------------------------------
# 5. RUN: both footings, physical density
# ----------------------------------------------------------------------
for name, ft in FOOTINGS.items():
    viol, kms_dev, worst, rows, bhat, x_gal = run_footing(name, ft["a0"], ft["H"])
    if viol:
        FAIL.append(f"{name}: dressed positivity VIOLATED at {viol}")
    if kms_dev > 1e-6:
        FAIL.append(f"{name}: dressed KMS broken, dev={kms_dev}")

# ----------------------------------------------------------------------
# 6. GHOST CONTROL + DETECTION THRESHOLD.  A negative Gaussian line at x0=0.5
#    (width 0.02) is inserted into the cut density with increasing amplitude.
#    The SAME pipeline must flag negativity for an O(1) ghost, else the pass
#    above is vacuous.  HONESTY: convolution SMOOTHS -- small ghosts can hide
#    in the dressed density (necessary-not-sufficient test); we MEASURE the
#    sensitivity floor instead of hiding it.
# ----------------------------------------------------------------------
print("\n=== GHOST CONTROL (negative line at x0=0.5, width=0.02, amplitude sweep) ===")
ft0 = FOOTINGS["canonical (a0=cH_L/Z=9.36e-11, bath H_Lambda)"]
a0, H = ft0["a0"], ft0["H"]
wstar = a0/(2*c); bhat = np.pi*a0/(c*H)
xs = np.unique(np.concatenate([np.linspace(1e-4, 3.5, 1751),
                               np.geomspace(3.5, 60, 60)]))
flagged_any = False
POS_WEIGHT = 1 - np.pi/4        # Int_0^1 (1-sqrt(1-x^2)) dx: continuum weight below branch pt
first_flag = None
for amp in (0.5, 1.0, 2.0, 4.0, 8.0):
    rho_g, Gp_g, Gp2_g, rd_g = make_engine(bhat, ghost=(amp, 0.5, 0.02))
    neg_w = amp*0.02*np.sqrt(np.pi)            # integrated negative weight
    vals = [(x,)+rd_g(x) for x in xs]
    gviol = [(x, r) for (x, r, e) in vals if r < -max(1e-12, 10*e)]
    gmin = min(vals, key=lambda v: v[1])
    tag = "FLAGGED" if gviol else "hidden by smoothing"
    print(f"    amp={amp:4.1f} (neg weight {neg_w:.3f} vs sub-branch continuum weight "
          f"{POS_WEIGHT:.3f}): dressed min {gmin[1]: .4e} at x={gmin[0]:.4g} -> {tag}")
    if gviol and not flagged_any:
        flagged_any = True
        first_flag = (amp, neg_w, gmin)
        # KMS survives even with a ghost (detailed balance is sign-blind, as banked)
        gp, _ = Gp2_g(0.7); gm, _ = Gp2_g(-0.7)
        print(f"           ghost KMS ratio at x=0.7: {gm*np.exp(bhat*0.7)/gp:.6f} "
              f"(KMS holds -> the ghost detector is POSITIVITY, not KMS)")
if not flagged_any:
    FAIL.append("GHOST CONTROL FAILED TO FLAG at every amplitude -- positivity test vacuous")
else:
    print(f"    -> detector FLAGS an O(1) ghost (first at amp={first_flag[0]}, "
          f"neg weight {first_flag[1]:.3f}); the physical pass is meaningful.")
    print("    -> HONEST LIMIT: ghosts with integrated weight well below the")
    print("       continuum weight are smoothed over at one loop; dressed")
    print("       positivity is NECESSARY not SUFFICIENT for micro-positivity.")

# ----------------------------------------------------------------------
print("\n" + "="*70)
if FAIL:
    print("LANE C RESULT: FAILURES")
    for f in FAIL:
        print("  *", f)
    sys.exit(1)
print("LANE C RESULT: PASS")
print("  - dressed (one-loop, KMS-weighted self-convolution) spectral density")
print("    >= 0 everywhere on BOTH footings, including branch-point edges")
print("    x=0+, x=1 (w=a0/2c) and the dressed 2-particle edge x=2 (w=a0/c),")
print("    out through the galactic band (x ~ 6.4e3).")
print("  - KMS detailed balance rho(-w)/rho(w)=e^{-beta w} preserved by dressing")
print("    to <1e-6 relative (thermalization intact; matches banked KMS wall:")
print("    sign flip requires a pump, and KMS itself is SIGN_BLIND).")
print("  - ghost control: a negative-weight line IS flagged by the same pipeline.")
sys.exit(0)
