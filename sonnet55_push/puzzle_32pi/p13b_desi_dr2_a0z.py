"""p13b: p13's T3 prediction with the REAL DESI DR2 dark-energy fits.
If rho_Lambda is the a0 sector's vacuum energy (G rho_DE = W a0^2), then a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)).

LOOK-UP RECORD (inputs; read 2026-10-03, two reads, values identical):
  source  DESI Collaboration, 'DESI DR2 Results II', arXiv:2503.14738, Table 5 (summary of cosmological constraints),
          block 'w0waCDM' (flat). Read 1: arXiv HTML v3; read 2: arXiv HTML v1. Read as the page's own table DOM
          text in a browser (not through a summarising fetch); row labels matched by text, columns by header
          (Omega_m | H0 | 1e3 Omega_K | w or w0 | wa). No PDF downloaded.
  The table gives MARGINAL 1-sigma errors only; the w0-wa correlation (strong, negative) is not in it, so the
  error band below treats w0 and wa as INDEPENDENT -> it is a conservative envelope, not a posterior.
Run: python3 p13b_desi_dr2_a0z.py     MUTATE=1 -> w0 sign flipped in the first row; its row checks must fail.
"""
import math
import os
import random
import sys

MUTATE = os.environ.get("MUTATE") == "1"

# name: (Omega_m, w0, w0_lo, w0_hi, wa, wa_lo, wa_hi)   [errors as printed: -lo / +hi]
ROWS = {
    "DESI+CMB":           (0.353,  -0.42,  0.21,  0.21,  -1.75, 0.58, 0.58),
    "DESI+CMB+Pantheon+": (0.3114, -0.838, 0.055, 0.055, -0.62, 0.19, 0.22),
    "DESI+CMB+Union3":    (0.3275, -0.667, 0.088, 0.088, -1.09, 0.27, 0.31),
    "DESI+CMB+DESY5":     (0.3191, -0.752, 0.057, 0.057, -0.86, 0.20, 0.23),
}
if MUTATE:
    r = list(ROWS["DESI+CMB"]); r[1] = +0.42; ROWS["DESI+CMB"] = tuple(r)


def rde(z, w0, wa):                     # CPL: rho_DE(z)/rho_DE(0)
    return (1 + z) ** (3 * (1 + w0 + wa)) * math.exp(-3 * wa * z / (1 + z))


def a0r(z, w0, wa):
    return math.sqrt(rde(z, w0, wa))


def Hr(z, om, w0, wa):                  # H(z)/H0 in the same fit (flat): the a0 ~ H(z) rival
    return math.sqrt(om * (1 + z) ** 3 + (1 - om) * rde(z, w0, wa))


def split_normal(rng, mu, lo, hi):
    x = rng.gauss(0, 1)
    return mu + (x * hi if x > 0 else x * lo)


res = []


def check(name, ok):
    res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + name)


zgrid = [i / 100 for i in range(0, 501)]
print(f"{'fit':20s} {'a0(1)/a0(0)':>12s} {'a0(2.5)/a0(0)':>14s} {'68% envelope @2.5':>18s} {'peak z':>7s} {'peak a0/a0(0)':>13s} {'H(2.5)/H0':>9s}")
summary = {}
for name, (om, w0, w0l, w0h, wa, wal, wah) in ROWS.items():
    rng = random.Random(12345)
    v1, v25 = a0r(1.0, w0, wa), a0r(2.5, w0, wa)
    zpk = max(zgrid, key=lambda z: a0r(z, w0, wa))
    samp = sorted(a0r(2.5, split_normal(rng, w0, w0l, w0h), split_normal(rng, wa, wal, wah)) for _ in range(20000))
    lo, hi = samp[int(0.16 * len(samp))], samp[int(0.84 * len(samp))]
    summary[name] = (v1, v25, lo, hi, zpk, a0r(zpk, w0, wa), Hr(2.5, om, w0, wa))
    print(f"{name:20s} {v1:12.3f} {v25:14.3f} {lo:8.3f} - {hi:6.3f}   {zpk:7.2f} {a0r(zpk, w0, wa):13.3f} {Hr(2.5, om, w0, wa):9.2f}")

print()
for name, (v1, v25, lo, hi, zpk, apk, h25) in summary.items():
    check(f"{name}: central a0 FALLS by z = 2.5 ({v25:.3f}); conservative envelope {lo:.2f}-{hi:.2f} "
          f"{'EXCLUDES' if hi < 1 else 'does NOT exclude'} no change", v25 < 1)
    check(f"{name}: a0 peaks at z = {zpk:.2f} ({100*(apk-1):.1f}% above today), then falls", 0 < zpk < 1.5 and apk > 1)
    check(f"{name}: rival a0 ~ H(z) rises x{h25:.2f} at z = 2.5; ratio of predictions {h25/v25:.1f}x", h25 / v25 > 3)
cen = [s[1] for k, s in summary.items() if k != "DESI+CMB"]
check(f"the three SN-anchored fits agree: a0(2.5)/a0(0) = {min(cen):.2f}-{max(cen):.2f}", max(cen) - min(cen) < 0.1)

n = sum(res)
print(f"\n{n}/{len(res)} checks pass" + ("  [MUTATE=1: failures REQUIRED]" if MUTATE else ""))
sys.exit(0 if n == len(res) else 1)
