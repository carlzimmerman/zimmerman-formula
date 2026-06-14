#!/usr/bin/env python3
"""
Monjo (2026) gas-rich UDG confrontation with the framework (arXiv:2604.09652).
==============================================================================
DATASET (Monjo 2026, v1 30-Mar / v2 22-May; SAMPLE = six isolated HI-bearing UDGs,
Mancera Pina+2020 orig. Leisman+2017 ALFALFA). V = CIRCULAR speed (HI rotation at
outer radius) -> BTFR-appropriate. Distances 73-97 Mpc => z~0.02 (LOCAL; the stated
"BTFR-highz" lever is ABSENT -> this is a z~0 BTFR-residual / deep-MOND-floor test).

Monjo uses the REGULAR-MOND default a0=1.2e-10 (Banik-Zhao 2022), MLS nu-hat
interpolation nu(x)=(1-exp(-sqrt x))^-1, x=g_N/a0. Global: chi2_N=9.70,
chi2_HMG=18.1, chi2_MOND=615.7. The UDGs rotate too SLOWLY for their baryons
(BTFR-low) -> MOND over-predicts V by 3.7-5.9 sigma per galaxy.

THE FRAMEWORK CALC (working rule MEMORY.md): run BOTH footings.
  fw:    a0 = 9.36e-11 (rho_DE footing)   -- the framework's own value
  canon: a0 = 1.20e-10 (regular MOND)      -- the paper's baseline
At z~0.02 the a0(z) declining-sqrt(rho_DE) branch is ~1.000 (negligible; computed
below for both CPL sets to confirm it cannot rescue this) -> the only lever the
framework pulls here is the LOWER static a0.

Deep-MOND: V^4 = G Mbar a0  => V_MOND scales as a0^(1/4).
Swapping 1.2e-10 -> 9.36e-11 multiplies every MOND V by (9.36/12)^0.25 = 0.9436.

We recompute, from the SAME published M_bar and V_obs:
  (1) V_MOND(fw) per galaxy and the per-galaxy + global MOND chi2 on BOTH footings;
  (2) whether the lower a0 moves MOND toward confirm / tension / kill;
  (3) the BTFR-floor read: the UDGs vs the canonical BTFR at both a0.
Provenance: Mbar, Vobs, Vmond(canon) from Monjo Table 1/2; sigma from the published
per-galaxy MOND tension z_MOND (V_MOND - V_obs)/sigma_eff -> back out sigma_eff,
then recompute z at the fw a0 holding sigma_eff fixed (the measurement error is
footing-independent).
"""
import numpy as np

G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
A0 = {"fw 9.36e-11": 9.36e-11, "canon 1.2e-10": 1.20e-10}

# ---- a0(z) declining-sqrt(rho_DE) branch at the sample's z (locked CPL sets) ----
OM = 0.315
def rhoDE_ratio(z, w0, wa):
    a = 1.0 / (1.0 + z)
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))
CPL = [(-0.83, -0.75, "DESI24 BAO+CMB+DESY5"), (-0.752, -0.86, "DESI DR2")]

# ---- Table 1 + Table 2 (Monjo 2026), every number transcribed from the prompt ----
# name: Mbar log10, V_obs, [V_MOND_canon, z_MOND_canon], [V_HMG, z_HMG]
GAL = [
    ("AGC114905", 9.21, 23, 74.2, 5.64, 35.0, 2.11),
    ("AGC122966", 9.21, 37, 73.6, 4.84, 35.5, -0.23),
    ("AGC219533", 9.36, 37, 81.1, 3.73, 38.5, 0.20),
    ("AGC248945", 9.05, 27, 67.2, 5.09, 31.6, 1.11),
    ("AGC334315", 9.25, 25, 76.0, 5.91, 35.9, 1.79),
    ("AGC749290", 9.17, 26, 72.5, 5.28, 34.0, 1.20),
]
A0_PAPER = 1.20e-10
FAC = (9.36e-11 / 1.20e-10) ** 0.25   # a0^(1/4) rescale on V_MOND

print("=" * 96)
print("Monjo 2026 UDG confrontation (arXiv:2604.09652) -- the a0-footing swap, both footings")
print("=" * 96)

# (0) confirm the a0(z) branch is inert at z~0.02
zsamp = np.array([76, 90, 96, 84, 73, 97]) / (299792.458 / 70.0)  # crude Hubble z, H0=70
print(f"\n(0) a0(z) declining-sqrt(rho_DE) branch at the sample redshifts (z~{zsamp.min():.3f}-{zsamp.max():.3f}):")
for w0, wa, tag in CPL:
    facs = np.sqrt([rhoDE_ratio(z, w0, wa) for z in zsamp])
    print(f"    {tag:24s}: a0(z)/a0 = {facs.min():.4f}-{facs.max():.4f}  -> swing < {100*(1-facs.min()):.2f}%  (INERT here)")
print("    => the only lever at z~0.02 is the LOWER static a0; declining branch cannot rescue this.")

# (1) per-galaxy MOND recompute on both footings
print("\n(1) MOND V_pred and tension z_MOND, BOTH footings (V_MOND_fw = V_MOND_canon * %.4f):" % FAC)
print(f"    {'galaxy':11s} {'Vobs':>5s} {'Vmond_cn':>9s} {'z_cn':>6s} {'sig_eff':>8s} "
      f"{'Vmond_fw':>9s} {'z_fw':>6s} {'dz':>6s}")
chi2_canon = 0.0
chi2_fw = 0.0
rows = []
for name, lMb, Vobs, Vm_cn, z_cn, Vhmg, zhmg in GAL:
    # back out the footing-independent effective sigma from the paper's z_MOND
    sig_eff = (Vm_cn - Vobs) / z_cn
    Vm_fw = Vm_cn * FAC
    z_fw = (Vm_fw - Vobs) / sig_eff
    chi2_canon += z_cn ** 2
    chi2_fw += z_fw ** 2
    rows.append((name, Vobs, Vm_cn, z_cn, sig_eff, Vm_fw, z_fw))
    print(f"    {name:11s} {Vobs:5d} {Vm_cn:9.1f} {z_cn:6.2f} {sig_eff:8.2f} "
          f"{Vm_fw:9.1f} {z_fw:6.2f} {z_fw - z_cn:+6.2f}")

print(f"\n    GLOBAL MOND chi2:  canon (a0=1.2e-10) = {chi2_canon:.1f}  (paper states 615.7)")
print(f"                       fw    (a0=9.36e-11)= {chi2_fw:.1f}")
print(f"    reduction from the a0 swap: {chi2_canon:.1f} -> {chi2_fw:.1f}  "
      f"(x{chi2_fw/chi2_canon:.2f}, {100*(1-chi2_fw/chi2_canon):.0f}% lower)")
print(f"    Newton chi2 = 9.70, HMG chi2 = 18.1 (paper). fw-MOND still >> both.")

# (2) sigma still needed: how much would a0 have to drop to reach MOND chi2 ~ HMG (18.1)?
#     V_MOND ~ a0^1/4 ; z ~ (Vm - Vobs)/sig ; solve for the a0 that lands chi2=18.1 and =9.70
print("\n(2) HOW LOW WOULD a0 HAVE TO GO to rescue MOND on these UDGs? (scan the footing)")
def chi2_at(a0):
    f = (a0 / A0_PAPER) ** 0.25
    c = 0.0
    for name, lMb, Vobs, Vm_cn, z_cn, Vhmg, zhmg in GAL:
        sig = (Vm_cn - Vobs) / z_cn
        c += ((Vm_cn * f - Vobs) / sig) ** 2
    return c
grid = np.logspace(np.log10(2e-12), np.log10(1.2e-10), 400)
c = np.array([chi2_at(a0) for a0 in grid])
for target, lbl in [(18.1, "= HMG (18.1)"), (9.70, "= Newton (9.70)"), (6.0, "(per-gal ~1 sigma)")]:
    i = int(np.argmin(np.abs(c - target)))
    print(f"    MOND chi2 {target:5.1f} {lbl:18s} needs a0 ~ {grid[i]:.2e} "
          f"= {grid[i]/1.2e-10:.3f} x canon = {grid[i]/9.36e-11:.3f} x fw")
print(f"    fw a0=9.36e-11 = {9.36e-11/1.2e-10:.3f} x canon -> only a {100*(1-FAC):.1f}% V cut. NOT ENOUGH.")

# (3) BTFR-floor read: where do these UDGs sit vs the BTFR Mbar = A V^4 ?
#     deep-MOND BTFR: Mbar = V^4 / (G a0).  Compute the implied Mbar(V_obs) vs the real Mbar.
print("\n(3) BTFR-FLOOR read: implied baryonic mass from V_obs vs the published Mbar, both footings")
print(f"    (deep-MOND BTFR: Mbar_pred = V_obs^4/(G a0); offset = log10(Mbar_pred/Mbar_obs))")
print(f"    {'galaxy':11s} {'logMbar':>8s} {'logMbtfr_cn':>12s} {'d_cn':>6s} {'logMbtfr_fw':>12s} {'d_fw':>6s}")
for name, lMb, Vobs, Vm_cn, z_cn, Vhmg, zhmg in GAL:
    line = f"    {name:11s} {lMb:8.2f}"
    for a0 in (1.20e-10, 9.36e-11):
        Mbtfr = (Vobs * 1e3) ** 4 / (G * a0) / MSUN
        d = np.log10(Mbtfr) - lMb
        line += f" {np.log10(Mbtfr):12.2f} {d:+6.2f}"
    print(line)
print("    (negative d = BTFR predicts LESS baryonic mass than observed = the UDG rotates too SLOW")
print("     for its baryons = the MOND over-prediction. fw a0 LOWER -> Mbtfr lower -> d MORE negative,")
print("     i.e. the lower a0 makes the BTFR deficit slightly WORSE on the mass axis, better on the V axis")
print("     by the same 5.6% -- it is the SAME shift, just the inverse projection.)")

print("\n" + "=" * 96)
print("done.")
