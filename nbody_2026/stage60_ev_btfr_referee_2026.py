#!/usr/bin/env python3
# BTFRREF_recompute.py -- adversarial re-derivation of BTFR_discriminator_2026.py's
# dilution formula, sample y values, and sigma arithmetic.  Read-only referee scratch.
import math

A0 = 9.3619e-11
OM = 0.315
G = 6.674e-11
MSUN = 1.989e30
KPC = 3.0857e19

def E(z, Om=OM):
    return math.sqrt(Om * (1 + z) ** 3 + (1 - Om))

# ---------- kernel-exact velocity ratio at fixed M_b, fixed r ----------
# a0-line kernel: g = gN * sqrt(1 + 1/y_z), y_z = gN/(f a0)
def vratio2_line(f, y):
    return math.sqrt((y + f) / (y + 1.0))          # v^2(f)/v^2(1)

# MS08 alpha=1/2 kernel (operative, Amdt 8/9): nu = 1/(1 - exp(-sqrt(y)))
def nu_ms08(y):
    return 1.0 / (1.0 - math.exp(-math.sqrt(y)))

def vratio2_ms08(f, y):
    return nu_ms08(y / f) / nu_ms08(y)

# mass-direction zero-point shift when fitting with fixed slope a:
#   delta_b = -a * dlogv = -(a/4) * log10[(y+f)/(y+1)]  (line kernel)
def mass_shift(f, y, a=4.0, kernel="line"):
    v2 = vratio2_line(f, y) if kernel == "line" else vratio2_ms08(f, y)
    return -a * 0.5 * math.log10(v2)

print("=== 1. dilution formula check (line kernel, slope 4) vs script ===")
f23 = E(2.3)
print(f"  script mass_shift(f={f23:.3f}, y=2) = {-math.log10((2+f23)/3):+.4f}")
print(f"  rederived (a=4, line)              = {mass_shift(f23, 2):+.4f}   [must match]")

print("\n=== 2. empirical y of the samples ===")
def y_from_obs(v_kms, r_kpc, f=1.0):
    gobs = (v_kms * 1e3) ** 2 / (r_kpc * KPC)
    yobs = gobs / A0
    # invert gobs^2 = gN^2 + gN*f*a0  (in a0 units): yN^2 + f*yN - yobs^2 = 0
    yN = (-f + math.sqrt(f * f + 4 * yobs ** 2)) / 2
    return yobs, yN

# KMOS3D Table 1 medians: vcirc,max at r = 2.2 Rd = 2.2*Re/1.678
for z, v, Re in ((0.9, 239.0, 4.8), (2.3, 260.0, 4.0)):
    r = 2.2 * Re / 1.678
    yo, yN = y_from_obs(v, r)
    yo_c, yN_c = y_from_obs(v, r, f=E(z))       # under the cH hypothesis itself
    print(f"  KMOS3D z~{z}: v={v} km/s at r={r:.2f} kpc -> y_obs={yo:.2f}, "
          f"y_N={yN:.2f} (const-a0) / {yN_c:.2f} (under cH)")
# KDS z~3.5: Turner+17 rot-dom, log M* ~ 9.8, v ~ 100-150, Re ~ 2 kpc
for v, Re in ((120.0, 2.0), (150.0, 2.5)):
    r = 2.2 * Re / 1.678
    yo, yN = y_from_obs(v, r)
    print(f"  KDS-like z~3.5: v={v} at r={r:.2f} kpc -> y_obs={yo:.2f}, y_N={yN:.2f}")
# z~4.5 [CII] discs (Fraternali+21 class): v~450-500 at 3-5 kpc
for v, r in ((500.0, 3.0), (460.0, 5.0), (350.0, 4.0)):
    yo, yN = y_from_obs(v, r)
    print(f"  [CII] z~4.5: v={v} at r={r} kpc -> y_obs={yo:.1f}, y_N={yN:.1f}  (script says y~7-15)")

print("\n=== 3. Test A (U17 internal 0.9->2.3, obs +0.17 +/- 0.064 stat, 0.20 sys) ===")
obs, stat, sys_ = 0.17, 0.064, 0.20
tot = math.sqrt(stat ** 2 + sys_ ** 2)
f09 = E(0.9)
scen = [
    ("script: y=2 both, slope4, line", 2.0, 2.0, 4.0, "line"),
    ("slope 3.75 (Lelli), y=2 both", 2.0, 2.0, 3.75, "line"),
    ("empirical y: 2.7 / 4.0, slope4", 2.7, 4.0, 4.0, "line"),
    ("empirical y + slope 3.75", 2.7, 4.0, 3.75, "line"),
    ("MS08 kernel, y=2 both, slope4", 2.0, 2.0, 4.0, "ms08"),
    ("MS08, empirical y, slope 3.75", 2.7, 4.0, 3.75, "ms08"),
]
for lbl, y1, y2, a, k in scen:
    pred = mass_shift(f23, y2, a, k) - mass_shift(f09, y1, a, k)
    sig = (obs - pred) / tot
    print(f"  {lbl:36s}: pred {pred:+.3f}, gap {obs-pred:+.3f}, sigma_tot {sig:.2f}")

print("\n=== 4. Test B (T19 rot-dom +0.02 +/- 0.06 stat, 0.15 sys) ===")
obsB, totB = 0.02, math.sqrt(0.06 ** 2 + 0.15 ** 2)
for lbl, y, a, k in (("script y=2 slope4", 2.0, 4.0, "line"),
                     ("slope 3.6 (Reyes), y=2", 2.0, 3.6, "line"),
                     ("y=2.7, slope 3.6", 2.7, 3.6, "line"),
                     ("MS08 y=2 slope 3.6", 2.0, 3.6, "ms08")):
    pred = mass_shift(f09, y, a, k)
    print(f"  {lbl:26s}: pred {pred:+.3f}, sigma {(obsB-pred)/totB:.2f}")

print("\n=== 5. Test C (KDS v-offset -0.10 +/- 0.13; velocity direction, kernel-exact) ===")
obsC, errC = -0.10, 0.13
f35 = E(3.5)
for lbl, y, k in (("script y=2 line", 2.0, "line"), ("y=1 line", 1.0, "line"),
                  ("y=3 line", 3.0, "line"), ("y=2 MS08", 2.0, "ms08")):
    v2 = vratio2_line(f35, y) if k == "line" else vratio2_ms08(f35, y)
    predv = 0.5 * math.log10(v2)
    print(f"  {lbl:16s}: pred v-shift {predv:+.3f}, sigma {abs(obsC-predv)/errC:.2f}")

print("\n=== 6. combined ===")
def comb(a, b, c):
    return math.sqrt(a * a + b * b + c * c)
print(f"  script:                    {comb(1.62, 0.68, 1.53):.2f}")
# honest conservative: empirical y + fitted slopes, line kernel
pA = mass_shift(f23, 4.0, 3.75) - mass_shift(f09, 2.7, 3.75)
sA = (obs - pA) / tot
pB = mass_shift(f09, 2.7, 3.6)
sB = (obsB - pB) / totB
v2 = vratio2_line(f35, 2.0)
sC = abs(obsC - 0.5 * math.log10(v2)) / errC
print(f"  empirical-y + fitted-slope: A={sA:.2f} B={sB:.2f} C={sC:.2f} -> {comb(sA,sB,sC):.2f}")
# MS08 kernel same y
pA2 = mass_shift(f23, 4.0, 3.75, "ms08") - mass_shift(f09, 2.7, 3.75, "ms08")
sA2 = (obs - pA2) / tot
pB2 = mass_shift(f09, 2.7, 3.6, "ms08")
sB2 = (obsB - pB2) / totB
v22 = vratio2_ms08(f35, 2.0)
sC2 = abs(obsC - 0.5 * math.log10(v22)) / errC
print(f"  MS08 same y:                A={sA2:.2f} B={sB2:.2f} C={sC2:.2f} -> {comb(sA2,sB2,sC2):.2f}")
# correlated M*/L systematic between B and C (worst case: fully correlated)
rho = 1.0
cov_term = 2 * rho * sB * sC * (0.15 / totB) * (0.08 / errC)  # rough shared-sys fraction
print(f"  (B,C M*/L correlation would shave ~0.1-0.2 off the combined -- second order)")

print("\n=== 7. misc arithmetic ===")
print(f"  0.06 dex floor / 1.6e-4 = {0.06/1.6e-4:.0f}x  (script prose says '500x')")
print(f"  footing offset log10(1.13/0.93619) = {math.log10(1.13e-10/9.3619e-11):.4f}")
print(f"  X_stellar = {math.log10(1.94)+0.15:.3f}; X_HI = {2*math.sqrt(math.log10(1.1)**2+0.04**2+0.05**2):.3f}; "
      f"X_CII = {2*math.sqrt(0.15**2+math.log10(1.1)**2+0.05**2):.3f}")
print(f"  T17 v->mass err: 0.13*3.6 = {0.13*3.6:.2f} (script table says 0.47); "
      f"errC quad: sqrt(0.10^2+0.08^2) = {math.sqrt(0.01+0.0064):.3f}")
print(f"  U17 internal err: sqrt(0.04^2+0.05^2) = {math.sqrt(0.0016+0.0025):.4f}")
