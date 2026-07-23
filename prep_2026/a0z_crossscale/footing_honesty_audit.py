#!/usr/bin/env python3
"""
FOOTING + HONESTY AUDIT for the framework a0(z) prediction.

Builds on (does NOT rebuild/contradict) desi_posterior_a0z.py, which already runs the
correlated-posterior Monte Carlo (2x2 Cholesky over (w0,wa)) with the FULL non-monotonic
closed form.  This companion answers four audit questions and freezes every honesty caveat.

The law under test (framework: de Sitter-Unruh MODIFIED INERTIA):
    a0(z) = a0(0) * sqrt(rho_DE(z)/rho_DE0)
    CPL:   rho_DE(z)/rho_DE0 = (1+z)^{3(1+w0+wa)} * exp(-3 wa z/(1+z))
    ratio: a0(z)/a0(0) = (1+z)^{1.5(1+w0+wa)} * exp(-1.5 wa z/(1+z))   [FULL closed form]

The law is NON-MONOTONIC: a small BUMP (ratio>1) at low z peaking near z~0.35, crossing 1
near z~0.9, then DECLINING to ~0.74 at z=3 (DESI+Pantheon+ central).  NEVER truncated here.

(a) PROVE ratio is footing-independent (sympy): Z, a0(0), canonical-vs-alt all cancel.
(b) ABSOLUTE band at z=3 on BOTH footings.
(c) LCDM-DISSOLUTION branch: at what |1+w0| does the z=3 separation from flat fall below 1sigma.
(d) HONEST confrontation of the weak measured hints (MUSE-DARK III; SPARC z=0 a0-line 1.18).
"""
import numpy as np
import sympy as sp
from scipy.special import erfcinv

# ----------------------------------------------------------------------------------------
# (a)  SYMBOLIC PROOF: a0(z)/a0(0) is FOOTING-INDEPENDENT
# ----------------------------------------------------------------------------------------
print("="*88)
print("(a)  FOOTING-INDEPENDENCE OF THE RATIO  a0(z)/a0(0)   [sympy, exact]")
print("="*88)

z, w0, wa, H, c, Z, k = sp.symbols('z w0 wa H c Z k', positive=True)
# Footing enters ONLY through the absolute normalization a0(0).  Two footings on record:
#   canonical:  a0(0) = c*H_Lambda / Z             (rho_DE / cH_Lambda)  -> 9.36e-11
#   alt:        a0(0) = k * c*H0                    (rho_total / cH0)     -> 1.13e-10
# The framework's z-DEPENDENCE is carried entirely by sqrt(rho_DE(z)/rho_DE0), which is a
# PURE RATIO of energy densities and contains NO footing constant.
rd_ratio = (1+z)**(3*(1+w0+wa)) * sp.exp(-3*wa*z/(1+z))        # rho_DE(z)/rho_DE0 (CPL)
a0z_over_a00 = sp.sqrt(rd_ratio)                                # framework ratio

# Build a0(z) on each footing = [footing normalization] * sqrt(rho_DE(z)/rho_DE0).
a0_canon_z = (c*H/Z)        * a0z_over_a00      # canonical footing absolute a0(z)
a0_canon_0 = (c*H/Z)        * a0z_over_a00.subs(z, 0)
a0_alt_z   = (k*c*H)        * a0z_over_a00      # alt footing absolute a0(z)
a0_alt_0   = (k*c*H)        * a0z_over_a00.subs(z, 0)

ratio_canon = sp.simplify(a0_canon_z / a0_canon_0)
ratio_alt   = sp.simplify(a0_alt_z   / a0_alt_0)

print("  canonical footing a0(0) = c*H_Lambda/Z   (carries Z, H_Lambda, c) -> value 9.36e-11")
print("  alt footing       a0(0) = k*c*H0         (carries k, H0, c)       -> value 1.13e-10")
print()
print("  ratio on canonical footing simplifies to :", ratio_canon)
print("  ratio on alt       footing simplifies to :", ratio_alt)
diff = sp.simplify(ratio_canon - ratio_alt)
print("  (canonical ratio) - (alt ratio)          :", diff, " <-- EXACTLY ZERO")
# Confirm no footing symbol survives in the ratio:
free = ratio_canon.free_symbols
print("  free symbols remaining in the ratio      :", sorted([str(s) for s in free]))
assert diff == 0, "footing did NOT cancel"
assert Z not in free and H not in free and c not in free and k not in free, "footing symbol leaked"
print("  RESULT: Z, a0(0), c, H, and the canonical-vs-alt choice ALL CANCEL.")
print("          a0(z)/a0(0) is a PURE function of (w0, wa, z).  Footing-INDEPENDENT. QED.")
print("          => there is exactly ONE ratio band; presenting two ratio bands would be an error.")

# closed-form ratio the MC uses (log form), for the record
print()
print("  closed form:  a0(z)/a0(0) = (1+z)^{1.5(1+w0+wa)} * exp(-1.5*wa*z/(1+z))")

# ----------------------------------------------------------------------------------------
#      shared numerics: the DESI DR2 w0waCDM combos (same inputs as desi_posterior_a0z.py)
# ----------------------------------------------------------------------------------------
def ratio(zv, W0, WA):
    """FULL non-monotonic closed form (never truncated)."""
    return (1+zv)**(1.5*(1+W0+WA)) * np.exp(-1.5*WA*zv/(1+zv))

COMBOS = [   # (label, w0, sw0, wa, swa, corr, LCDM-excl-sigma)
    ("DESI+CMB+Pantheon+", -0.838, 0.055, -0.62, 0.22, -0.86, 2.8),
    ("DESI+CMB+DESY5",     -0.752, 0.057, -0.86, 0.22, -0.86, 4.2),
    ("DESI+CMB+Union3",    -0.667, 0.088, -1.09, 0.31, -0.87, 3.8),
]

def mc_pair(w0v, sw0, wav, swa, corr, N=400000):
    L = np.linalg.cholesky(np.array([[sw0**2, corr*sw0*swa],[corr*sw0*swa, swa**2]]))
    g = np.random.default_rng(0)
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        pr = np.array([w0v, wav]) + g.standard_normal((N,2)) @ L.T
    return pr[:,0], pr[:,1]

# ----------------------------------------------------------------------------------------
# (b)  ABSOLUTE BAND at z=3 on BOTH footings
# ----------------------------------------------------------------------------------------
print()
print("="*88)
print("(b)  ABSOLUTE a0(z=3) ON BOTH FOOTINGS  (ratio is shared; only normalization differs)")
print("="*88)
A0_CANON = 9.36e-11    # canonical  rho_DE / cH_Lambda
A0_ALT   = 1.13e-10    # alt        rho_total / cH0
print(f"  canonical a0(0) = {A0_CANON:.3e} m/s^2   |   alt a0(0) = {A0_ALT:.3e} m/s^2")
print("  (per-combo ratio at z=3, median [16,84], then absolute = ratio * a0(0) on each footing)")
r3_meds = []
for label, w0v, sw0, wav, swa, corr, _ in COMBOS:
    W0, WA = mc_pair(w0v, sw0, wav, swa, corr)
    r3 = ratio(3.0, W0, WA)
    med, lo, hi = np.median(r3), np.percentile(r3,16), np.percentile(r3,84)
    r3_meds.append(med)
    print(f"\n  [{label}]  a0(3)/a0(0) = {med:.3f} [{lo:.3f}, {hi:.3f}]")
    print(f"      canonical: a0(3) = {med*A0_CANON:.3e}  [{lo*A0_CANON:.3e}, {hi*A0_CANON:.3e}]")
    print(f"      alt      : a0(3) = {med*A0_ALT:.3e}  [{lo*A0_ALT:.3e}, {hi*A0_ALT:.3e}]")
r_ref = 0.74   # representative central ratio at z=3 (matches desi_posterior_a0z.py summary)
print(f"\n  HEADLINE (representative ratio {r_ref:.2f} at z=3):")
print(f"      a0(3) = {r_ref}*9.36e-11 = {r_ref*A0_CANON:.3e} m/s^2  (canonical)")
print(f"      a0(3) = {r_ref}*1.13e-10 = {r_ref*A0_ALT:.3e} m/s^2  (alt)")
print("  The 0.74 RATIO is identical on both footings; only the absolute value carries the footing.")

# ----------------------------------------------------------------------------------------
# (c)  LCDM-DISSOLUTION BRANCH: where does the prediction become untestable?
# ----------------------------------------------------------------------------------------
print()
print("="*88)
print("(c)  LCDM-DISSOLUTION BRANCH  (w -> -1  =>  ratio -> 1, flat, = constant-a0 MOND)")
print("="*88)
# Sanity: exact LCDM limit.  w0=-1, wa=0  =>  1+w0+wa=0 and wa=0 => ratio == 1 for all z.
lam = ratio(np.array([0.5,1.0,2.0,3.0]), -1.0, 0.0)
print(f"  exact check: at (w0,wa)=(-1,0) ratio at z=[0.5,1,2,3] = {np.round(lam,6)}  -> flat 1.000")
print("  => if DE does not evolve, a0(z) is EXACTLY constant and INDISTINGUISHABLE from")
print("     constant-a0 (standard) MOND.  All discriminating power is INHERITED from DESI's")
print("     w0wa evolution being real.  The band is a CONDITIONAL prediction, not a proof.")
print()
# Quantify: hold the DESI-like corr and errors fixed; slide w0 toward -1 (with wa scaled to
# stay on the DESI degeneracy direction) and find where the z=3 separation from flat < 1 sigma.
# Separation-from-flat significance at z=3 := |median(ratio)-1| / std(ratio) over the posterior.
print("  How close to LCDM can w0 sit before the z=3 test dies (separation from flat < 1 sigma)?")
print("  Slide (w0,wa) along the DESI degeneracy toward (-1,0), keep Pantheon+ errors/corr:")
sw0, swa, corr = 0.055, 0.22, -0.86
# DESI degeneracy: wa ~ slope*(1+w0). Use the Pantheon+ central to fix slope.
slope = -0.62 / (1 - 0.838)     # wa/(1+w0) at the Pantheon+ central ~ -3.83
print(f"     (degeneracy slope wa/(1+w0) fixed at Pantheon+ central = {slope:.2f})")
crossed = None
for eps in np.linspace(0.162, 0.0, 82):      # eps = 1+w0, from Pantheon+ central down to 0
    w0v = -1 + eps
    wav = slope*eps
    W0, WA = mc_pair(w0v, sw0, wav, swa, corr)
    r3 = ratio(3.0, W0, WA)
    sep = abs(np.median(r3) - 1.0) / np.std(r3)
    if crossed is None and sep < 1.0:
        crossed = (eps, w0v, wav, np.median(r3), sep)
if crossed:
    eps, w0v, wav, med, sep = crossed
    print(f"     -> separation drops below 1 sigma at |1+w0| ~ {eps:.3f}  (w0~{w0v:.3f}, wa~{wav:.2f}),")
    print(f"        where median a0(3)/a0(0) ~ {med:.3f} and |med-1|/std ~ {sep:.2f} sigma.")
    print(f"     Interpretation: once |1+w0| <~ {eps:.02f} (with DESI-size errors), the z=3 prediction")
    print(f"     is statistically INDISTINGUISHABLE from flat -> UNTESTABLE with this precision.")
else:
    print("     -> separation stayed above 1 sigma across the scan (test remains alive).")
print("  NOTE: the current DESI Pantheon+ central sits at |1+w0| ~ 0.162 -> ~2 sigma from flat;")
print("        it is testable ONLY because DESI currently prefers w0 well away from -1.")

# ----------------------------------------------------------------------------------------
#      Deep-MOND MEASUREMENT PENALTY (calibration rule 4) -- required precision is ~2x tighter
# ----------------------------------------------------------------------------------------
print()
print("-"*88)
print("  MEASUREMENT-PENALTY NOTE (deep-MOND):  a0 = g_obs^2 / g_bar  =>  d ln a0 = 2 d ln g_obs.")
print("  Per-point log-scatter on a0 is DOUBLED: sigma(ln a0) ~ 2 * sigma(ln g)  (not halved).")
sep_target = 1.0 - r_ref      # ~0.26 fractional signal at z=3
print(f"  To resolve a {100*sep_target:.0f}% a0(z) decline at z=3 at, say, 3 sigma needs")
print(f"  sigma(a0)/a0 ~ {sep_target/3:.03f}; the UNDERLYING RAR/rotation-curve data must be")
print(f"  ~2x tighter still, sigma(ln g) ~ {sep_target/6:.03f}, per the doubling above.")

# ----------------------------------------------------------------------------------------
# (d)  HONEST CONFRONTATION OF THE WEAK MEASURED HINTS
# ----------------------------------------------------------------------------------------
print()
print("="*88)
print("(d)  HONEST CONFRONTATION OF WEAK MEASURED HINTS  (no manufactured support)")
print("="*88)
# The low-z BUMP: peak location and amplitude on the Pantheon+ central (FULL law).
zz = np.linspace(0.0, 1.5, 3001)
rr = ratio(zz, -0.838, -0.62)
ipk = int(np.argmax(rr))
zpk, rpk = zz[ipk], rr[ipk]
# crossing back through 1
above = rr > 1.0
icross = np.where(above[:-1] & ~above[1:])[0]
zcross = zz[icross[0]] if len(icross) else float('nan')
print(f"  Low-z BUMP (Pantheon+ central, FULL closed form): peak a0/a0(0) = {rpk:.4f} at z ~ {zpk:.2f};")
print(f"  crosses back through 1 near z ~ {zcross:.2f}, then declines.  Peak excess ~ +{100*(rpk-1):.1f}%.")
print("  MUSE-DARK III (Ciocan 2026) reports a0 RISING with z.  HONEST verdict:")
print("   - A rise is only MILDLY predicted in the narrow low-z bump (+~3.6%, hardest z to measure a0).")
print("   - The reported rise is LCDM-DEGENERATE tension / WATCH, NOT a confirmation of the framework.")
print("   - It is NOT cited as support.  (Faking a 'MUSE rise' by Taylor-dropping wa is the exact")
print("     failure mode this audit forbids; the full law's bump is tiny and quickly reverses.)")
print()
# SPARC z=0 anchor, Lambda-blind (the a0-line).
A0_SPARC = 1.181e-10          # Lambda-blind galaxy readout (a0-line), +/-16%
print(f"  SPARC z=0 anchor (a0-line, Lambda-BLIND) = {A0_SPARC:.3e} m/s^2 (+/-16%).")
print(f"   - vs canonical cosmic a0(0)=9.36e-11: ratio {A0_SPARC/A0_CANON:.2f}  (~1.4 sigma high, tie holds ~1sigma)")
print(f"   - vs alt      cosmic a0(0)=1.13e-10: ratio {A0_SPARC/A0_ALT:.2f}  (consistent)")
print("   - This is a z=0 NORMALIZATION check, Lambda-blind; it does NOT test the a0(z) SLOPE.")
print("   - It neither confirms nor excludes the decline; it only anchors a0(0).")

# ----------------------------------------------------------------------------------------
#      FROZEN HONESTY CAVEATS (must appear verbatim in any frozen artifact)
# ----------------------------------------------------------------------------------------
print()
print("="*88)
print("FROZEN HONESTY CAVEATS  (must appear in the artifact)")
print("="*88)
CAVEATS = [
 "1. The a0(z)/a0(0) ratio is FOOTING-INDEPENDENT (proved exactly): Z, a0(0), c, H, and the "
 "canonical-vs-alt choice all cancel. There is ONE ratio band, not two.",
 "2. The law is NON-MONOTONIC and is always used in FULL closed form: a small low-z BUMP "
 "(+~3.6%, peak z~0.35), crossing 1 near z~0.9, then DECLINING to ~0.74 at z=3. Never truncate/Taylor it.",
 "3. Only the ABSOLUTE a0(z) carries the footing: a0(3) ~= 0.74 * {9.36e-11 canonical, 1.13e-10 alt} "
 f"= {0.74*A0_CANON:.2e} vs {0.74*A0_ALT:.2e} m/s^2. Note both wherever absolute scale is load-bearing.",
 "4. LCDM-DISSOLUTION: if w -> -1 the ratio collapses to EXACTLY 1 (flat) and is INDISTINGUISHABLE "
 "from constant-a0 MOND. All discriminating power is INHERITED from DESI's w0wa evolution being real; "
 "the band is a CONDITIONAL prediction, not a proof.",
 "5. The z=3 test becomes UNTESTABLE (separation from flat < 1 sigma at DESI-size errors) once "
 f"|1+w0| <~ 0.08 along the DESI degeneracy (w0 >~ -0.92). Current Pantheon+ central sits at "
 f"|1+w0|~0.16 -> ~2 sigma only.",
 "6. Deep-MOND MEASUREMENT PENALTY: a0=g_obs^2/g_bar DOUBLES per-point log-scatter "
 "(sigma(ln a0)~2 sigma(ln g)); the underlying RAR/rotation-curve precision must be ~2x tighter "
 "than the precision quoted on a0(z) itself.",
 "7. MUSE-DARK III (Ciocan 2026) rising-a0 is LCDM-DEGENERATE tension / WATCH, NOT confirmation. "
 "A mild rise is predicted only in the tiny low-z bump (+~3.6%, at the z where a0 is hardest to measure). "
 "Do NOT cite it as support.",
 "8. The SPARC z=0 anchor (a0-line 1.18e-10, Lambda-BLIND) is a NORMALIZATION check only "
 "(tie holds ~1 sigma on canonical footing); it does NOT test the a0(z) slope and is neither "
 "confirmation nor exclusion of the decline.",
 "9. No 'theory closed'. The decline at DESI central is ~2.2 sigma (neither detected nor excluded); "
 "a NULL / weak-testability outcome is verified as rigorously as a win.",
]
for cav in CAVEATS:
    print("  * " + cav.replace("\n"," "))

print()
print("EXIT 0")
