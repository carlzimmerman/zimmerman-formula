#!/usr/bin/env python3
"""
MSA-3D  a0(z) CONFRONTATION  — the missed door, now swung.
============================================================
Source: Espejo Salcedo et al. 2026, "MSA-3D: ...", arXiv:2606.27853.
JWST/NIRSpec MSA resolved kinematics + NIRCam stellar masses for 30 SFGs at
0.58 < z < 1.68.  Per-galaxy data transcribed from the paper's Table 1
(masses, SFR, R_e) and Table 3 (R_e,disk, sigma_0, V_rot(R_e), f_DM(R_e)).

This is the FIRST NIRSpec-based, MUSE-INDEPENDENT test of whether the
inertia-modification scale a0 RISES with redshift (the contested MUSE-DARK III
rising-a0 claim, which LEANS AGAINST the canonical declining/constant branch)
or stays flat/declining (the framework's own sqrt(rho_DE) expectation).

FOOTING (locked, framework's OWN — NOT MOND / NOT McGaugh's nu):
  * modified INERTIA, horizon-derived a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2.
  * dS-Unruh interpolation:  g_obs = sqrt(g_bar^2 + g_bar*a0).
  * inversion (the a0-line, E-book):  g_obs^2 - g_bar^2 = a0 * g_bar  (EXACT),
        => a0_inferred = (g_obs^2 - g_bar^2) / g_bar.
  * g_obs read from the paper's pressure-corrected circular velocity at R_e;
        g_bar read from the paper's OWN baryonic decomposition via f_DM(R_e):
            g_bar = (1 - f_DM) * g_obs   [f_DM = 1 - V_bar^2/V_c^2 at R_e].

Both-ways discipline (Carl's #1 rule — verify a deficit as hard as a win):
  (i)  the ABSOLUTE a0 normalization is Upsilon/M-L-DEGENERATE (a constant baryon
       offset shifts every galaxy the same way) -> NON-diagnostic of 9.36e-11,
       exactly as the SPARC RAR is.  Reported, but NOT the verdict.
  (ii) the a0(z) TREND is the clean discriminator: a constant M-L offset cancels
       in d ln a0 / d ln(1+z).  Framework canonical (pure Lambda) predicts slope 0
       (flat); the rival rising branch a0 ~ sqrt(rho_total) ~ H(z) predicts a
       STEEP positive slope (x1.5-2.3 over this z-range, x4.6 by z=3).
       THIS is what MUSE-DARK contests and what MSA-3D can now independently judge.

Pressure support (paper Eq. 4):  V_c^2(R_e) = V_rot^2 + 2 sigma_0^2 (R_e/R_d),
   R_d = R_e/1.678  ->  V_c^2(R_e) = V_rot^2 + 3.356 sigma_0^2.
"""
import numpy as np

a0_canon = 9.36e-11          # framework a0 (INPUT, quarantined: NOT derived)
KPC = 3.0856775814913673e19  # m
KMS = 1.0e3                  # m/s per km/s
Om, OL = 0.315, 0.685        # flat LCDM (Planck-ish) for the rival branch

def Ez(z):  return np.sqrt(Om*(1+z)**3 + OL)

# ---- per-galaxy data: ID, z, Re_kpc, sigma0, Vrot(Re), f_DM(Re), logMstar, SFR, sample
# Re_kpc, sigma0, Vrot, f_DM from Table 3 (R_e,disk); logMstar,SFR from Table 1.
G = [
 # ---------------- Golden sample (primary statistical sample, N=23) ----------------
 ("2111", 0.58, 5.37, 51.5, 152.1, 0.59,  9.97,  1.6, "gold"),
 ("2145", 1.17, 3.38, 43.4,  73.6, 0.67,  9.19,  1.4, "gold"),
 ("2465", 1.25, 2.92, 44.9, 114.9, 0.70,  9.30,  1.6, "gold"),
 ("2824", 0.98, 3.04, 39.4, 165.6, 0.63,  9.49,  0.7, "gold"),
 ("3399", 1.34, 4.13, 54.3, 120.6, 0.47,  9.81,  3.5, "gold"),
 ("4391", 1.08, 1.59, 49.5, 168.9, 0.58,  9.48,  2.7, "gold"),
 ("6199", 1.59, 5.86, 45.5,  79.3, 0.53, 10.00, 17.8, "gold"),
 ("6430", 1.17, 7.63, 58.0, 149.7, 0.79,  9.79,  8.9, "gold"),
 ("7314", 1.28, 2.53, 61.5, 121.8, 0.73,  9.55,  2.6, "gold"),
 ("7561", 1.03, 1.95, 49.8, 106.0, 0.51,  9.21,  0.7, "gold"),
 ("8365", 1.68, 3.94, 37.9, 141.1, 0.83,  9.56,  3.4, "gold"),
 ("8512", 1.10, 5.28, 43.1, 261.6, 0.70, 10.32,  3.2, "gold"),
 ("8576", 1.57, 3.89, 47.1, 208.1, 0.77,  9.60,  3.3, "gold"),
 ("8942", 1.18, 3.67, 55.6, 259.5, 0.77,  9.86, 16.2, "gold"),
 ("9424", 0.98, 5.83, 44.2, 137.9, 0.75,  9.76,  5.4, "gold"),
 ("9636", 0.74, 4.97, 32.6, 110.3, 0.68,  9.35,  1.7, "gold"),
 ("9812", 0.74, 4.98, 43.1, 180.6, 0.57,  9.97,  3.6, "gold"),
 ("9960", 1.51, 2.91, 45.4, 327.9, 0.52, 11.06,  6.0, "gold"),
 ("10910",0.74, 4.52, 36.6, 132.8, 0.36,  9.57,  1.5, "gold"),
 ("11225",1.05, 5.31, 64.5, 105.5, 0.21,  9.67, 12.6, "gold"),
 ("12015",1.24, 4.36, 59.7, 189.8, 0.26, 10.08, 11.2, "gold"),
 ("18586",0.76, 2.58, 43.6,  83.5, 0.50,  9.01,  3.3, "gold"),
 ("29470",1.04, 4.61, 40.3, 187.3, 0.88,  9.71,  2.1, "gold"),
 # ---------------- Good sample (secondary, N=7) ----------------
 ("9337", 1.17, 5.66, 31.3,  45.4, 0.62,  9.27,  2.2, "good"),
 ("10107",1.01, 2.89, 61.0, 137.5, 0.14, 10.01,  3.6, "good"),
 ("11843",1.46, 5.13, 55.9, 298.2, 0.37, 10.74, 19.0, "good"),
 ("12239",0.89, 3.88, 56.9, 181.4, 0.83,  9.49,  1.5, "good"),
 ("13182",1.54, 3.86, 64.0, 185.2, 0.24, 10.25, 15.8, "good"),
 ("13416",1.54, 2.06, 43.5, 217.2, 0.32, 10.76, 20.0, "good"),
 ("18188",0.82, 6.27, 43.8, 152.1, 0.84,  9.56,  2.1, "good"),
]

def infer(gal):
    _id, z, Re, s0, Vrot, fDM, lM, sfr, samp = gal
    Vc2 = (Vrot*KMS)**2 + 3.356*(s0*KMS)**2      # pressure-corrected circular vel^2
    Re_m = Re*KPC
    g_obs = Vc2/Re_m
    g_bar = (1.0 - fDM)*g_obs
    a0_inf = (g_obs**2 - g_bar**2)/g_bar          # framework a0-line inversion
    return dict(id=_id, z=z, samp=samp, g_obs=g_obs, g_bar=g_bar,
                a0=a0_inf, fDM=fDM, x_obs=g_obs/a0_canon, x_bar=g_bar/a0_canon)

rows = [infer(g) for g in G]

def summarize(sel, label):
    r = [x for x in rows if sel(x)]
    a0s = np.array([x["a0"] for x in r])
    zs  = np.array([x["z"]  for x in r])
    med = np.median(a0s)
    # log-space MAD -> approx sigma on the median
    lmad = np.median(np.abs(np.log10(a0s) - np.median(np.log10(a0s))))
    return r, med, lmad, zs, a0s, label

print("="*90)
print("MSA-3D a0(z) CONFRONTATION  (arXiv:2606.27853; framework footing a0=9.36e-11)")
print("="*90)
print(f"{'ID':>6} {'z':>5} {'smp':>4} {'g_bar/a0':>9} {'g_obs/a0':>9} {'f_DM':>5} {'a0_inf/1e-10':>12}")
for x in sorted(rows, key=lambda d: d["z"]):
    print(f"{x['id']:>6} {x['z']:>5.2f} {x['samp']:>4} {x['x_bar']:>9.2f} "
          f"{x['x_obs']:>9.2f} {x['fDM']:>5.2f} {x['a0']*1e10:>12.2f}")

print("\n" + "-"*90)
print("ABSOLUTE a0 (Upsilon/M-L-DEGENERATE -> NON-diagnostic of 9.36e-11; reported not judged)")
print("-"*90)
for sel, lab in [ (lambda x: x["samp"]=="gold", "Golden (N=23, primary)"),
                  (lambda x: True,               "Golden+Good (N=30)") ]:
    r, med, lmad, zs, a0s, _ = summarize(sel, lab)
    print(f"  {lab:24s}: median a0 = {med*1e10:.2f}e-10 = {med/a0_canon:.2f} x canonical"
          f"   (log10-MAD {lmad:.2f} dex, N={len(r)})")

print("\n" + "-"*90)
print("THE CLEAN TEST — a0(z) TREND (M-L offset cancels in the slope)")
print("-"*90)
def zbin(lo, hi):
    r = [x for x in rows if x["samp"]=="gold" and lo <= x["z"] < hi]
    a0s = np.array([x["a0"] for x in r])
    return len(r), np.median(a0s), np.mean([x["z"] for x in r]) if r else np.nan
bins = [(0.5,0.9),(0.9,1.2),(1.2,1.8)]
print(f"  {'z-bin':>12} {'N':>3} {'<z>':>5} {'median a0/1e-10':>16} {'a0/canonical':>13}")
base = None
binvals = []
for lo,hi in bins:
    n, med, zm = zbin(lo,hi)
    if base is None: base = med
    binvals.append((zm, med))
    print(f"  {f'[{lo},{hi})':>12} {n:>3} {zm:>5.2f} {med*1e10:>16.2f} {med/a0_canon:>13.2f}")

# fit slope of log10(a0) vs log10(1+z) over the golden sample (per-galaxy)
rg = [x for x in rows if x["samp"]=="gold"]
X = np.log10(1+np.array([x["z"] for x in rg]))
Y = np.log10(np.array([x["a0"] for x in rg]))
slope, inter = np.polyfit(X, Y, 1)
# bootstrap the slope
rng = np.random.default_rng(0)
bs = []
for _ in range(5000):
    idx = rng.integers(0, len(rg), len(rg))
    bs.append(np.polyfit(X[idx], Y[idx], 1)[0])
bs = np.array(bs); slo, shi = np.percentile(bs, [16,84])

# predicted slopes of the two branches over the SAME z-support
zsup = np.array([x["z"] for x in rg])
# rival rising: a0 ~ sqrt(rho_total) ~ H(z) ~ E(z)
Yr = np.log10(Ez(zsup)); sr = np.polyfit(np.log10(1+zsup), Yr - Yr.mean(), 1)[0]
print(f"\n  measured slope  d log10(a0) / d log10(1+z) = {slope:+.2f}  "
      f"[16-84%: {slo:+.2f}, {shi:+.2f}]  (N={len(rg)})")
print(f"  framework canonical (pure-Lambda, rho_DE const)     predicts slope  = 0.00 (flat)")
print(f"  rival rising branch a0 ~ sqrt(rho_total) ~ H(z)      predicts slope  = {sr:+.2f}")

# rival amplitude marker: a0(z=1.5)/a0(z=0.7)
r_ratio = Ez(1.5)/Ez(0.7)
d_lo, d_hi = binvals[0][1], binvals[-1][1]
print(f"\n  rival predicts a0(<z>~{binvals[-1][0]:.2f}) / a0(<z>~{binvals[0][0]:.2f}) ~ {r_ratio:.2f}x (rising)")
print(f"  data    shows  a0(hi-z bin)/a0(lo-z bin)         = {d_hi/d_lo:.2f}x")

print("\n" + "="*90)
print("VERDICT")
print("="*90)
flat_ok  = (slo <= 0.6 <= shi) or abs(slope) < 0.5
rising_ok = slo > 0.6
if slope < 0.3 and shi < sr-0.3:
    print("  -> a0(z) is FLAT/declining within errors; the steep RISING branch")
    print(f"     (slope {sr:+.2f}) is DISFAVORED. This is an INDEPENDENT (NIRSpec, non-MUSE)")
    print("     data point that LEANS WITH the framework's constant/declining expectation")
    print("     and AGAINST the contested MUSE-DARK III rising-a0 reading.")
elif slope > 0.6:
    print("  -> a0(z) RISES; consistent with the rival sqrt(rho_total) branch and with")
    print("     MUSE-DARK III. This HARDENS the tension against the canonical branch.")
else:
    print("  -> a0(z) trend INCONCLUSIVE at this N; slope brackets both branches.")
print("  NOTE: absolute a0 normalization is M-L-degenerate (as SPARC RAR) -> not a verdict.")
print("="*90)
