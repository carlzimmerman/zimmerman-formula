#!/usr/bin/env python3
"""
The framework's one falsifiable prediction, computed exactly:
    a0(z)/a0(0) = sqrt( rho_DE(z) / rho_DE(0) )
because a0 = (c/2) sqrt(G rho_DE), with rho_DE evolving per DESI DR2 (CPL w0-wa).

Compared against the two rival emergent-gravity readings:
    - flat MOND:        a0 = const          (a0 from a fixed scale)
    - Verlinde / QI:    a0 ∝ c H(z)         (a0 from TOTAL density / horizon)

Key outputs:
    (1) the exact a0(z) curve + its NON-MONOTONIC feature (peak where w crosses -1)
    (2) the observable: V_flat offset at fixed M_bar  (V^4 = G M a0)
    (3) the 3-way discriminating power vs redshift
    (4) error band from the DESI w0-wa covariance
C. Zimmerman / verification, 2026-06-06. No external deps beyond numpy (matplotlib optional).
"""
import numpy as np

# ---- DESI DR2 (2025) BAO+CMB+SNe CPL fits, three SNe compilations -------------
# (w0, wa, sig_w0, sig_wa, corr)  -- representative published central values + errors
DESI = {
    "DESI+CMB+DESY5":    dict(w0=-0.752, wa=-0.86, sw0=0.057, swa=0.22, rho=-0.86),
    "DESI+CMB+Union3":   dict(w0=-0.667, wa=-1.09, sw0=0.088, swa=0.31, rho=-0.87),
    "DESI+CMB+Pantheon+":dict(w0=-0.838, wa=-0.62, sw0=0.055, swa=0.28, rho=-0.85),
}
FID = "DESI+CMB+DESY5"   # fiducial = the combo in the project memory (w0=-0.752, wa=-0.86)

OM, OL = 0.3137, 0.6863   # Planck-ish, for H(z) (Verlinde) and for the matter cross-checks

def rho_DE_ratio(z, w0, wa):
    """rho_DE(z)/rho_DE0 for CPL w(a)=w0+wa(1-a).  = a^{-3(1+w0+wa)} exp[-3 wa (1-a)]."""
    a = 1.0/(1.0+z)
    return a**(-3.0*(1.0+w0+wa)) * np.exp(-3.0*wa*(1.0-a))

def a0_framework(z, w0, wa):
    return np.sqrt(rho_DE_ratio(z, w0, wa))           # a0 ∝ sqrt(rho_DE)

def a0_verlinde(z):
    Ez = np.sqrt(OM*(1+z)**3 + OL)                    # H(z)/H0
    return Ez                                          # a0 ∝ cH(z)

def Vflat_offset_dex(a0ratio):
    """V_flat^4 = G M_bar a0  =>  at fixed M_bar, dlog10 V = (1/4) dlog10 a0."""
    return 0.25*np.log10(a0ratio)

def pct(x):  # fractional velocity change from a0 ratio: V ∝ a0^{1/4}
    return (x**0.25 - 1.0)*100.0

# ---- the peak of a0(z): d/da [a^p exp(q(1-a))]=0 => a*=p/q ; p=-3(1+w0+wa)/2, q=-3wa/2 --
def a0_peak(w0, wa):
    p = -1.5*(1.0+w0+wa); q = -1.5*wa
    a_star = p/q
    if not (0 < a_star < 1):  # no interior peak (monotonic)
        return None
    z_star = 1.0/a_star - 1.0
    return z_star, a0_framework(z_star, w0, wa)

f = DESI[FID]; w0, wa = f["w0"], f["wa"]

print("="*78)
print(f"FRAMEWORK PREDICTION  a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0)   [fiducial {FID}]")
print(f"   w0={w0}, wa={wa}  ->  rho_DE(a)/rho0 = a^{-3*(1+w0+wa):.3f} * exp[{-3*wa:.3f}(1-a)]")
print("="*78)

# w crosses -1 (=> rho_DE peak) at  1-a = (-1-w0)/wa
across = (-1.0 - w0)/wa
z_cross = 1.0/(1.0-across) - 1.0
pk = a0_peak(w0, wa)
print(f"\nw(z) crosses -1 at z = {z_cross:.2f}   (rho_DE, hence a0, peaks here)")
if pk:
    print(f"a0(z) PEAK: a0/a0(0) = {pk[1]:.4f} at z = {pk[0]:.2f}   "
          f"(+{(pk[1]-1)*100:.1f}% bump, then monotonic decline)")
print("  => the framework does NOT predict pure decline: it predicts a small RISE to a")
print("     z~0.4 bump (where w=-1), then decline.  Neither flat MOND nor Verlinde does this.")

zs = [0.0,0.2,0.41,0.6,1.0,1.5,2.0,3.0,4.0,5.0,7.0,10.0,20.0,1100.0]
print("\n   z   | a0/a0(0)  | V_flat offset       || flat | Verlinde a0/a0(0) (V offset)")
print("       | (frame)   | dlog10V    %V        ||      | a0      %V")
print("-"*78)
for z in zs:
    af = a0_framework(z, w0, wa)
    av = a0_verlinde(z)
    print(f" {z:6.1f}| {af:7.4f}   | {Vflat_offset_dex(af):+7.4f}  {pct(af):+6.1f}%  "
          f"||  1.00| {av:6.2f}  {pct(av):+6.1f}%")

# ---- 3-way discriminating power: spread in V_flat (fixed M_bar) -----------------
print("\n" + "="*78)
print("3-WAY OBSERVABLE FORK  (V_flat at FIXED baryonic mass, vs z):")
print("   the rising hypothesis is EASY to kill; declining-vs-flat is the hard one")
print("="*78)
print("   z   | frame %V | flat %V | Verlinde %V | frame-vs-flat | Verlinde-vs-flat")
print("-"*78)
for z in [0.5,1.0,2.0,3.0,5.0]:
    af = a0_framework(z,w0,wa); av=a0_verlinde(z)
    print(f" {z:5.1f} | {pct(af):+6.1f}  | {0.0:+6.1f} | {pct(av):+8.1f}   "
          f"| {pct(af)-0:+6.1f} pp    | {pct(av)-0:+7.1f} pp")

# ---- error band on the framework curve from the w0-wa covariance ----------------
print("\n" + "="*78)
print("ERROR BAND on a0(z)/a0(0) from DESI w0-wa covariance (1-sigma, fiducial combo)")
print("="*78)
rng = np.random.default_rng(0)
cov = np.array([[f["sw0"]**2, f["rho"]*f["sw0"]*f["swa"]],
                [f["rho"]*f["sw0"]*f["swa"], f["swa"]**2]])
with np.errstate(all="ignore"):   # suppress spurious Accelerate-BLAS matmul FP warnings
    samp = rng.multivariate_normal([w0,wa], cov, size=20000)
print("   z   | a0/a0(0)  16th--84th pct   |  is 1.000 (flat) inside 1sigma?")
print("-"*78)
for z in [0.5,1.0,2.0,3.0,5.0]:
    vals = np.sqrt(np.array([rho_DE_ratio(z,a,b) for a,b in samp]))
    lo,med,hi = np.percentile(vals,[16,50,84])
    flat_in = "YES (not yet distinguishable)" if lo<=1.0<=hi else "NO (distinguishable)"
    print(f" {z:5.1f} | {med:6.3f}   [{lo:5.3f}, {hi:5.3f}]   |  {flat_in}")

# ---- spread across the three DESI SNe combos (model/systematic spread) ----------
print("\n" + "="*78)
print("ROBUSTNESS across DESI SNe-compilation choice (central values):")
print("="*78)
print("   z   | " + " | ".join(f"{k.split('+')[-1]:>9}" for k in DESI))
for z in [1.0,2.0,3.0,5.0]:
    row = " | ".join(f"{a0_framework(z,v['w0'],v['wa']):9.3f}" for v in DESI.values())
    print(f" {z:5.1f} | {row}")

# ---- optional figure -----------------------------------------------------------
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    zg = np.linspace(0,5,400)
    fig, ax = plt.subplots(figsize=(8,5.2))
    # framework band across the 3 combos
    band = np.array([[a0_framework(z,v['w0'],v['wa']) for z in zg] for v in DESI.values()])
    ax.fill_between(zg, band.min(0), band.max(0), color="C0", alpha=0.18,
                    label="framework $a_0\\propto\\sqrt{\\rho_{DE}}$ (DESI w0-wa spread)")
    ax.plot(zg, [a0_framework(z,w0,wa) for z in zg], "C0-", lw=2.2,
            label=f"framework, fiducial ({FID})")
    ax.plot(zg, np.ones_like(zg), "k--", lw=1.6, label="flat MOND ($a_0=$const)")
    ax.plot(zg, [a0_verlinde(z) for z in zg], "C3-.", lw=2.0,
            label="Verlinde/QI ($a_0\\propto cH$)")
    if pk: ax.plot([pk[0]],[pk[1]],"C0o",ms=7)
    ax.axhline(1.0, color="gray", lw=0.5)
    ax.set_xlabel("redshift z"); ax.set_ylabel("$a_0(z)/a_0(0)$")
    ax.set_title("The 3-way fork: where the framework's $a_0(z)$ prediction is decided")
    ax.set_ylim(0.4, 5.2); ax.legend(fontsize=9, loc="upper left"); ax.grid(alpha=0.25)
    out = "real_research/a0_evolution_prediction_curve.png"
    fig.tight_layout(); fig.savefig(out, dpi=130)
    print(f"\n[figure written: {out}]")
except Exception as e:
    print(f"\n[figure skipped: {e}]")
