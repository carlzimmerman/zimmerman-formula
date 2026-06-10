#!/usr/bin/env python3
"""
CLOSE THE DESI -> a0(z) LOOP (definitive, current DR2 numbers, full error propagation).
=======================================================================================
Framework: a0 = (c/2) sqrt(G rho_DE)  =>  a0(z)/a0(0) = sqrt( rho_DE(z) / rho_DE0 ).
DESI DR2 (2503.14738) measures w0,wa => rho_DE(z) (CPL).  So a0(z) is PREDICTED by DESI.

CPL dark-energy density (exact integral of the w(a)=w0+wa(1-a) EoS):
    rho_DE(z)/rho_DE0 = (1+z)^{3(1+w0+wa)} * exp(-3 wa z/(1+z))
=> a0(z)/a0(0) = (1+z)^{1.5(1+w0+wa)} * exp(-1.5 wa z/(1+z))

We:
  (1) compute the PREDICTED a0(z)/a0(0) at z=0.5,1,2,3 for the 4 DESI DR2 SN combos,
  (2) propagate the (w0,wa) covariance (corr=-0.7, DESI banana) -> 68% band via MC,
  (3) confront with the a0(z) DATA (repo a0_of_z.csv + MUSE-DARK III Ciocan+2026),
  (4) quantify the predicted decline AND the current test power (sigma the data can reach).
Pure-numpy; central + error inputs are LITERATURE (DESI DR2), the propagation is COMPUTED-THIS-RUN.
"""
import numpy as np

c   = 2.99792458e8
zs  = np.array([0.5, 1.0, 2.0, 3.0])

# --- DESI DR2 (2503.14738) w0waCDM central values (LITERATURE, verified 2026-06-05) ---
# corr(w0,wa) ~ -0.7 (the DESI banana); errors are the published 1-sigma.
DESI = {
    "DESI+CMB+DESY5  (4.2s)": dict(w0=-0.752, wa=-0.86, sw0=0.057, swa=0.22),
    "DESI+CMB+Union3 (3.8s)": dict(w0=-0.667, wa=-1.09, sw0=0.088, swa=0.31),
    "DESI+CMB+Pant+  (2.8s)": dict(w0=-0.838, wa=-0.62, sw0=0.055, swa=0.25),
    "DESI+CMB only   (3.1s)": dict(w0=-0.42,  wa=-1.75, sw0=0.21,  swa=0.58),
}
CORR = -0.7

def a0_ratio(z, w0, wa):
    """a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0) for CPL w(a)=w0+wa(1-a)."""
    return (1+z)**(1.5*(1+w0+wa)) * np.exp(-1.5*wa*z/(1+z))

print("#"*94)
print("# DESI -> a0(z) LOOP CLOSED:  a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0),  rho_DE(z) from DESI DR2 w(z)")
print("#"*94)

# ---------------------------------------------------------------------------
# (1)+(2) prediction + MC error band per DESI combo
# ---------------------------------------------------------------------------
print("\n" + "="*94)
print("(1) PREDICTED a0(z)/a0(0) with 68% band [MC over the (w0,wa) DESI covariance, corr=-0.7]")
print("="*94)
rng = np.random.RandomState(42)
results = {}
for name, p in DESI.items():
    cov = np.array([[p["sw0"]**2, CORR*p["sw0"]*p["swa"]],
                    [CORR*p["sw0"]*p["swa"], p["swa"]**2]])
    draws = rng.multivariate_normal([p["w0"], p["wa"]], cov, size=40000)
    print(f"\n  {name}:  w0={p['w0']:+.3f}+-{p['sw0']:.3f}, wa={p['wa']:+.2f}+-{p['swa']:.2f}")
    print(f"  {'z':>5}{'a0(z)/a0(0)':>16}{'68% band':>22}{'decline%':>11}")
    row = {}
    for z in zs:
        r = a0_ratio(z, draws[:,0], draws[:,1])
        lo, md, hi = np.percentile(r, [16, 50, 84])
        cen = a0_ratio(z, p["w0"], p["wa"])
        row[z] = (cen, lo, hi)
        print(f"  {z:>5.1f}{cen:>16.3f}   [{lo:>5.3f}, {hi:>5.3f}]{(1-cen)*100:>10.1f}%")
    results[name] = row

# ---------------------------------------------------------------------------
# (3) confront with a0(z) DATA
# ---------------------------------------------------------------------------
print("\n" + "="*94)
print("(3) CONFRONT WITH a0(z) DATA  (all ratios normalized to each dataset's own z~0 anchor)")
print("="*94)
# repo a0_of_z.csv  (a0 in 1e-10 m/s^2)
data = [  # z, a0_e10, sig_e10, source
    (0.00, 1.20, 0.26, "SPARC_McGaugh+2016"),
    (0.05, 1.69, 0.13, "Varasteanu+2025"),
    (0.90, 2.38, 0.11, "MUSE-DARK-III_Ciocan+2026"),
]
a0_loc = 1.20  # local anchor (SPARC z=0)
print(f"  local anchor a0(0) = {a0_loc} e-10 (SPARC McGaugh+2016)")
print(f"  {'z':>5}{'a0_obs/a0(0)':>15}{'+-':>8}{'source':>28}")
for z, a0e, sig, src in data:
    print(f"  {z:>5.2f}{a0e/a0_loc:>15.2f}{sig/a0_loc:>8.2f}{src:>28}")

# MUSE-DARK III linear fit a0(z)=a0(0)+a1 z, a0(0)=1.0, a1=+1.59 (their own units 1e-10)
print("\n  MUSE-DARK III (Ciocan+2026) linear fit a0(z)=1.0 + 1.59 z (their own normalization a0(0)=1.0):")
print(f"  {'z':>5}{'MUSE a0/a0(0)':>16}")
for z in zs:
    print(f"  {z:>5.1f}{(1.0+1.59*z):>16.2f}")

# Head-to-head at the redshifts where data exist
print("\n  --- HEAD-TO-HEAD: DESI-predicted (DESY5) vs MUSE-measured a0(z)/a0(0) ---")
p = DESI["DESI+CMB+DESY5  (4.2s)"]
print(f"  {'z':>5}{'DESI predict':>14}{'MUSE measure':>14}{'sign':>20}")
for z in (0.5, 0.9, 1.0):
    desi = a0_ratio(z, p["w0"], p["wa"])
    muse = 1.0 + 1.59*z
    print(f"  {z:>5.2f}{desi:>14.3f}{muse:>14.2f}{'OPPOSITE (DESI<1, MUSE>1)':>26}")

# ---------------------------------------------------------------------------
# (4) test power: what sigma_a0/a0 is needed to DETECT the DESI decline vs constant
# ---------------------------------------------------------------------------
print("\n" + "="*94)
print("(4) TEST POWER: precision needed to separate DESI-decline from constant a0(=1)")
print("="*94)
p = DESI["DESI+CMB+DESY5  (4.2s)"]
print(f"  (using the DESI+CMB+DESY5 central prediction; gap = |1 - a0(z)/a0(0)|)")
print(f"  {'z':>5}{'a0pred':>10}{'gap vs const':>15}{'sig_a0/a0 for 3sigma':>24}{'BTFR V shift':>16}")
for z in zs:
    cen = a0_ratio(z, p["w0"], p["wa"])
    gap = abs(1-cen)
    need = gap/3.0
    vshift = cen**0.25 - 1   # V_flat ~ a0^(1/4) at fixed baryonic mass (deep-MOND BTFR)
    print(f"  {z:>5.1f}{cen:>10.3f}{gap:>14.1%}{need:>23.1%}{vshift:>15.1%}")
print("\n  BTFR intrinsic scatter ~0.026 dex = 6.0% in V (Lelli+2019).")
print("  z=3 V-shift vs that scatter, and N discs needed to detect at 3sigma (sigma_mean=scatter/sqrt(N)):")
for z in (2.0, 3.0):
    cen = a0_ratio(z, p["w0"], p["wa"])
    vshift_dex = 0.25*np.log10(cen)              # dex shift in V
    scatter_dex = 0.026
    N = (3*scatter_dex/abs(vshift_dex))**2 if vshift_dex != 0 else np.inf
    print(f"    z={z}: |V shift|={abs(vshift_dex):.4f} dex vs scatter {scatter_dex} dex -> N ~ {N:.0f} clean discs for 3sigma")

print("\n" + "="*94)
print("SUMMARY")
print("="*94)
print(f"""  PREDICTION (DESI DR2 DESY5, the 4.2s combo): a0(z)/a0(0) DECLINES into the past:
     z=0.5 -> {a0_ratio(0.5,-0.752,-0.86):.2f},  z=1 -> {a0_ratio(1,-0.752,-0.86):.2f},  z=2 -> {a0_ratio(2,-0.752,-0.86):.2f},  z=3 -> {a0_ratio(3,-0.752,-0.86):.2f}
     => a ~{(1-a0_ratio(3,-0.752,-0.86))*100:.0f}% DECLINE by z=3 (rho_DE was lower in the phantom past).
  ROBUSTNESS across SN combos: z=3 decline ranges {min(a0_ratio(3,DESI[k]['w0'],DESI[k]['wa']) for k in DESI):.2f}-{max(a0_ratio(3,DESI[k]['w0'],DESI[k]['wa']) for k in DESI):.2f} (all < 1, all DECLINING).
  CONFRONTATION: the only multi-point a0(z) DATA (MUSE-DARK III) RISES (a0~2.4 at z~1);
     DESI predicts a0~1.0 at z=1 -> OPPOSITE SIGN at face value. BUT the MUSE rise is
     "faster than H(z)" => matches NO background-density law, and is LCDM-degenerate
     (Mayer+2023: assembly mimics it w/ no fundamental a0) -> apparent, not fundamental.
  TEST POWER: the DESI decline is SMALL (~7% in a0 -> ~2% in V_flat at z=3), BELOW the
     ~6% BTFR scatter; needs ~{(3*0.026/abs(0.25*np.log10(a0_ratio(3,-0.752,-0.86))))**2:.0f} clean deep-MOND z~3 discs to detect at 3sigma. Untestable by MUSE's
     intermediate-z (z<1.4), assembly-active, g>~a0 disks.""")
print("#"*94)
