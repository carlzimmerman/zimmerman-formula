#!/usr/bin/env python3
"""
btfr_forecast_check.py -- independent re-derivation of the DESI DR2 + JWST
evolving-BTFR forecast, auditing Gemini Task 5
(zimmerman-formula/real_research/reviews/open_doors_2026_07/desi_jwst_btfr_forecast.py,
commit 9e85df27).

CANONICAL a0(z) MACHINERY (framework's own premises, dS-Unruh / horizon-derived):
    a0(z)/a0(0) = sqrt( rho_DE(z) / rho_DE(0) )
so under pure Lambda (w = -1) a0 is EXACTLY CONSTANT, and under the DESI DR2
CPL best fit (w0 = -0.752, wa = -0.86; banked values) rho_DE(z) is
NON-MONOTONIC: a +6.15% a0 bump at z = 0.405, declining to a0(3)/a0(0) ~ 0.74.

ALT FOOTING (footing fork, run both ways per the working rule):
    a0 ~ c H(z)/Z  ->  a0(z)/a0(0) = E(z) = H(z)/H0   (rho_total / cH0 branch)
This branch RISES steeply with z. The fork flips the sign of the prediction;
both are shown, spread reported.

BTFR observables (deep-MOND limit, M_bar = V^4 / (G a0)):
    at fixed M:  dlogV = (1/4) dlog a0 = (1/8) dlog10 rho_DE   (banked rule)
    at fixed V:  dlogM = -dlog a0      = -(1/2) dlog10 rho_DE
Banked anchors this script must reproduce from the machinery (NOT hard-coded):
    +6.15% a0 bump at z = 0.405 ; a0(3)/a0(0) ~ 0.74 ; dlogV(z=3) = -0.033 dex.

Detectability: JWST/ALMA high-z kinematic systematics floor 0.04-0.06 dex
(velocity axis). Two regimes reported honestly:
  (i) floor treated as PER-GALAXY random scatter -> N_3sigma = (3*sigma/|dlogV|)^2
  (ii) floor treated as COHERENT calibration systematic -> detectable only if
       |dlogV| > 3*sigma_floor regardless of N (the honest pessimistic case).

Exit 0 always; asserts only check internal reproduction of banked anchors.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

# ---------------- cosmology ----------------
Om, OL = 0.315, 0.685
W0_DR2, WA_DR2 = -0.752, -0.86      # banked DESI DR2 CPL best fit
W0_GEM, WA_GEM = -0.8, -0.5         # what Task 5 actually used ("representative")

def f_DE(z, w0, wa):
    """rho_DE(z)/rho_DE(0) for CPL w(z) = w0 + wa z/(1+z)."""
    z = np.asarray(z, dtype=float)
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))

def E_z(z, w0, wa):
    """H(z)/H0 with CPL dark energy."""
    return np.sqrt(Om * (1 + np.asarray(z, dtype=float)) ** 3 + OL * f_DE(z, w0, wa))

# ---------------- a0(z) on both footings ----------------
def a0_ratio_canonical(z, w0=W0_DR2, wa=WA_DR2):
    """CANONICAL: a0 = c H_Lambda / Z, H_Lambda^2 ~ rho_DE -> sqrt(rho_DE ratio)."""
    return np.sqrt(f_DE(z, w0, wa))

def a0_ratio_alt(z, w0=W0_DR2, wa=WA_DR2):
    """ALT footing fork: a0 ~ c H(z) (rho_total / cH0 branch, 1.13e-10 at z=0)."""
    return E_z(z, w0, wa)

# ---------------- BTFR offsets (deep-MOND) ----------------
def dlogV(a0_ratio):   # zero-point offset along the velocity axis, fixed M
    return 0.25 * np.log10(a0_ratio)

def dlogM(a0_ratio):   # zero-point offset along the mass axis, fixed V
    return -np.log10(a0_ratio)

# ---------------- anchors ----------------
print("=" * 78)
print("CANONICAL FOOTING  a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)),  DESI DR2 CPL")
print(f"  w0 = {W0_DR2}, wa = {WA_DR2}")
print("=" * 78)

# bump location: d/dz ln rho_DE = 3(1+w(z))/(1+z) = 0  ->  w(z) = -1
res = minimize_scalar(lambda z: -a0_ratio_canonical(z), bounds=(0.0, 3.0), method="bounded")
z_bump = res.x
bump_pct = 100 * (a0_ratio_canonical(z_bump) - 1)
z_bump_analytic = (-(1 + W0_DR2) / WA_DR2) / (1 + (1 + W0_DR2) / WA_DR2)
print(f"  a0 bump: z = {z_bump:.4f} (analytic w(z)=-1 crossing: {z_bump_analytic:.4f}), "
      f"amplitude = +{bump_pct:.2f}%")

r3 = float(a0_ratio_canonical(3.0))
print(f"  a0(3)/a0(0) = {r3:.4f}")
dv3 = float(dlogV(r3)); dm3 = float(dlogM(r3))
print(f"  BTFR at z=3: dlogV = {dv3:+.4f} dex (fixed M) ; dlogM = {dm3:+.4f} dex (fixed V)")
dv_bump = float(dlogV(a0_ratio_canonical(z_bump)))
print(f"  BTFR at bump z={z_bump:.3f}: dlogV = {dv_bump:+.4f} dex  (far below any floor)")

# reproduce banked anchors -- these are CHECKS of the machinery, not inputs
assert abs(z_bump - 0.405) < 0.005, f"bump z {z_bump} != banked 0.405"
assert abs(bump_pct - 6.15) < 0.15, f"bump {bump_pct}% != banked +6.15%"
assert abs(r3 - 0.74) < 0.01, f"a0(3)/a0(0) {r3} != banked ~0.74"
assert abs(dv3 - (-0.033)) < 0.001, f"dlogV(3) {dv3} != banked -0.033 dex"
print("  [OK] banked anchors reproduced: bump z=0.405 +6.15%, a0(3)~0.74, dlogV(3)=-0.033")

# pure-Lambda check
assert np.allclose(a0_ratio_canonical([0.5, 1, 2, 3], w0=-1.0, wa=0.0), 1.0), \
    "pure-Lambda canonical a0 must be exactly constant"
print("  [OK] pure-Lambda (w=-1): canonical a0(z) exactly constant -> dlogV = 0 at all z")

print()
print("=" * 78)
print("ALT FOOTING  a0(z)/a0(0) = E(z)  (rho_total/cH0 branch) -- the footing fork")
print("=" * 78)
for zt in (0.405, 1.0, 2.0, 3.0):
    ra = float(a0_ratio_alt(zt))
    print(f"  z = {zt:5.3f}: a0 ratio = {ra:6.3f}  dlogV = {float(dlogV(ra)):+.4f} dex  "
          f"dlogM = {float(dlogM(ra)):+.4f} dex")
spread3 = float(dlogV(a0_ratio_alt(3.0))) - dv3
print(f"  FORK SPREAD at z=3 (velocity axis): {spread3:+.4f} dex "
      f"(alt {float(dlogV(a0_ratio_alt(3.0))):+.3f} vs canonical {dv3:+.3f}) "
      "-- opposite signs, the fork is decisive")

# what Task 5 actually printed (its 'shift' = dlogM with a0_ratio = E(z))
print()
print("Task 5 reproduction check (its formula: dlogM = -log10(E(z)), its params):")
for zt in (1.0, 2.0, 3.0):
    print(f"  z = {zt:.1f}: Task-5 'DESI' shift = {float(dlogM(E_z(zt, W0_GEM, WA_GEM))):+.3f} dex "
          f"(printed -0.259/-0.482/-0.659); canonical dlogM = "
          f"{float(dlogM(a0_ratio_canonical(zt))):+.3f} dex")

# ---------------- detectability ----------------
print()
print("=" * 78)
print("DETECTABILITY (canonical footing, velocity axis; floor 0.04-0.06 dex)")
print("=" * 78)
zgrid = np.linspace(0.01, 3.5, 800)
sig_v = dlogV(a0_ratio_canonical(zgrid))
print("  Regime (ii) coherent floor: need |dlogV| > 3*sigma_floor")
for s in (0.04, 0.05, 0.06):
    ok = np.abs(sig_v) > 3 * s
    print(f"    sigma_floor = {s:.2f} dex -> 3*floor = {3*s:.2f} dex; "
          f"max |signal| (z<=3.5) = {np.max(np.abs(sig_v)):.4f} dex -> "
          f"{'detectable above z=%.2f' % zgrid[ok][0] if ok.any() else 'NOT detectable at ANY N'}")
print("  Regime (i) per-galaxy random floor: N_3sigma = (3*sigma/|dlogV|)^2")
hdr = "    z      dlogV     N(s=0.04)  N(s=0.05)  N(s=0.06)"
print(hdr)
for zt in (0.405, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5):
    d = abs(float(dlogV(a0_ratio_canonical(zt))))
    Ns = [np.inf if d == 0 else int(np.ceil((3 * s / d) ** 2)) for s in (0.04, 0.05, 0.06)]
    print(f"    {zt:5.3f}  {float(dlogV(a0_ratio_canonical(zt))):+.4f}   "
          + "  ".join(f"{n:>8}" for n in Ns))

print()
print("  HONEST STATEMENT: the canonical signal is |dlogV| <= 0.041 dex out to z=3.5")
print("  (0.033 dex at z=3),")
print("  BELOW the 0.04-0.06 dex kinematic systematics floor per galaxy. If the floor")
print("  averages down as random per-galaxy scatter, a 3-sigma zero-point detection")
print("  needs N ~ 15-40 well-measured rotators at z ~ 2.5-3.5 (N ~ 21 at z=3 for")
print("  sigma = 0.05); at z <~ 1.5 the signal (< 0.01 dex) is undetectable at any")
print("  realistic N, and the +6.15% a0 bump at z = 0.405 maps to only +0.0065 dex --")
print("  invisible. If the floor is a COHERENT calibration systematic, the canonical")
print("  signal is NOT 3-sigma detectable at any N (0.033 < 3 x 0.04). The ALT-footing")
print("  branch (+0.16 dex at z=3) would clear the floor easily -- the BTFR zero-point")
print("  at z ~ 3 is therefore a decisive FOOTING-FORK discriminator even where the")
print("  canonical amplitude itself stays marginal.")

# ---------------- plot ----------------
fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
ax = axes[0]
ax.plot(zgrid, a0_ratio_canonical(zgrid), 'C0-', lw=2.5,
        label='canonical: $\\sqrt{\\rho_{DE}(z)/\\rho_{DE}(0)}$ (DR2 CPL)')
ax.plot(zgrid, np.ones_like(zgrid), 'C0--', lw=1.5, label='canonical, pure $\\Lambda$ (const)')
ax.plot(zgrid, a0_ratio_alt(zgrid), 'C3-', lw=2, label='alt footing: $E(z)$ ($\\rho_{tot}/cH_0$)')
ax.axvline(z_bump, color='gray', ls=':', lw=1)
ax.annotate(f'+{bump_pct:.1f}% bump\n$z={z_bump:.3f}$', xy=(z_bump, 1.0615),
            xytext=(0.9, 1.9), fontsize=9, arrowprops=dict(arrowstyle='->', lw=0.8))
ax.set_xlabel('$z$'); ax.set_ylabel('$a_0(z)/a_0(0)$')
ax.set_title('$a_0(z)$: both footings (fork spread shown)')
ax.set_yscale('log'); ax.grid(alpha=0.3); ax.legend(fontsize=8)

ax = axes[1]
ax.plot(zgrid, sig_v, 'C0-', lw=2.5, label='canonical dlogV (DR2 CPL)')
ax.plot(zgrid, np.zeros_like(zgrid), 'C0--', lw=1.5, label='canonical, pure $\\Lambda$')
ax.plot(zgrid, dlogV(a0_ratio_alt(zgrid)), 'C3-', lw=2, label='alt footing dlogV')
ax.axhspan(-0.06, 0.06, color='gray', alpha=0.18, label='per-galaxy sys. floor 0.04-0.06 dex')
ax.axhspan(-0.04, 0.04, color='gray', alpha=0.18)
ax.set_xlabel('$z$'); ax.set_ylabel('BTFR zero-point offset dlogV (dex, fixed $M$)')
ax.set_title('Deep-MOND BTFR velocity offset vs systematics floor')
ax.grid(alpha=0.3); ax.legend(fontsize=8, loc='upper left')
fig.tight_layout()
out = "/Users/carlzimmerman/new_physics/prep_2026/btfr_forecast_audit/btfr_forecast_check.png"
fig.savefig(out, dpi=160)
print(f"\nSaved plot: {out}")
print("EXIT 0 -- all anchors reproduced from the machinery, no hard-coded passes.")
