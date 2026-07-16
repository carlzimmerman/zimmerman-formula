#!/usr/bin/env python3
"""
P1 -- KINEMATIC RAR (SPARC 175 galaxies, Lelli+2016 rotmod files, read from the frozen repo).

Framework equation ONLY: g_obs = sqrt(g_bar^2 + g_bar*a0)   [nu(y)=sqrt(1+1/y), the
framework's own dS-Unruh interpolation -- NOT McGaugh's]. Zero per-galaxy freedom;
the only astrophysical dial is the GLOBAL stellar M/L Upsilon_disk (3.6um, SPS range
~0.5-0.8; Upsilon_bul = 1.4 Upsilon_disk as in the committed baseline).

WHAT THIS ROW IS AND IS NOT (honesty rail #1): the RAR is convention-compatible and
NON-diagnostic of the exact a0 -- a0 and Upsilon are degenerate. So this row's product
is a WIDE BAND: the union over the physical Upsilon range of the a0 values whose fit
quality is within a small tolerance of that Upsilon's optimum. The claim is
"the Planck value sits INSIDE the band", never "SPARC pins 9.36e-11".

Systematics owned by this probe: stellar M/L, distances, inclinations.
DISJOINT from P2 (shear calibration, photo-z: photons, not kinematics).

Data: real_research/data/sparc_data/*_rotmod.dat (175 galaxies), read-only.
Committed baseline reproduced 2026-07-16: 0.108 dex @ Upsilon=0.70, reg-MOND 0.122.
"""
import numpy as np, glob, os, json

REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research"
DATA = os.path.join(REPO, "data", "sparc_data")
HERE = os.path.dirname(os.path.abspath(__file__))
kpc = 3.0857e19

anchor = json.load(open(os.path.join(HERE, "anchor_values.json")))
A0C, A0A = anchor["a0_canon"], anchor["a0_alt"]

rows = []
for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
    try:
        d = np.genfromtxt(f, comments="#")
    except Exception:
        continue
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
    rows.append((R*kpc, Vobs, eV, Vgas, Vdisk, Vbul))
assert len(rows) == 175, f"expected 175 SPARC galaxies, got {len(rows)}"

def scatter(Ud, a0):
    res, w = [], []
    for Rm, Vobs, eV, Vgas, Vdisk, Vbul in rows:
        Vbar2 = np.sign(Vgas)*Vgas**2 + Ud*Vdisk**2 + 1.4*Ud*Vbul**2
        gb = Vbar2*1e6/Rm; go = (Vobs*1e3)**2/Rm
        ok = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (Vobs > 0)
        r = np.log10(go[ok]) - 0.5*np.log10(gb[ok]**2 + gb[ok]*a0)
        fr = np.clip(eV[ok], 1, None)/np.clip(Vobs[ok], 1, None)
        res += list(r); w += list(1/fr**2)
    res, w = np.array(res), np.array(w)
    return float(np.sqrt(np.sum(w*res**2)/np.sum(w)))

a0_grid = np.geomspace(3e-11, 4e-10, 61)
TOL_REL = 0.02   # a0 "acceptable at this Upsilon" if scatter <= (1+2%) * min-scatter

print("="*88)
print("P1 KINEMATIC BAND: profile the SPARC weighted RAR scatter over a0, framework nu")
print("="*88)
print(f"{'Upsilon_d':>10} {'a0_best':>11} {'min scat':>9} {'2%-window a0':>26} "
      f"{'pen@canon':>10} {'pen@alt':>9}")

band_lo, band_hi = np.inf, -np.inf
results = {}
for Ud in (0.50, 0.60, 0.70, 0.80):
    s = np.array([scatter(Ud, a) for a in a0_grid])
    i = int(np.argmin(s))
    win = a0_grid[s <= s[i]*(1+TOL_REL)]
    pen_c = 100*(scatter(Ud, A0C)/s[i] - 1)
    pen_a = 100*(scatter(Ud, A0A)/s[i] - 1)
    results[Ud] = dict(a0_best=float(a0_grid[i]), smin=float(s[i]),
                       lo=float(win.min()), hi=float(win.max()),
                       pen_canon=pen_c, pen_alt=pen_a)
    band_lo = min(band_lo, win.min()); band_hi = max(band_hi, win.max())
    print(f"{Ud:>10.2f} {a0_grid[i]:>11.3e} {s[i]:>9.4f} "
          f"[{win.min():.2e}, {win.max():.2e}]      {pen_c:>9.2f}% {pen_a:>8.2f}%")

in_c = band_lo <= A0C <= band_hi
in_a = band_lo <= A0A <= band_hi
print("-"*88)
print(f"  KINEMATIC a0 BAND (union over physical Upsilon 0.5-0.8, 2%-scatter tolerance):")
print(f"      [{band_lo:.2e}, {band_hi:.2e}] m/s^2")
print(f"  Planck CANONICAL a0 = {A0C:.3e}: {'INSIDE' if in_c else 'OUTSIDE'} "
      f"(best matched near Upsilon=0.70, penalty {results[0.70]['pen_canon']:.2f}%)")
print(f"  Planck ALT       a0 = {A0A:.3e}: {'INSIDE' if in_a else 'OUTSIDE'} "
      f"(best matched near Upsilon=0.55-0.60, penalty {results[0.60]['pen_alt']:.2f}%)")
print()
print("  HONESTY RAIL: the per-Upsilon windows are WIDE and the best-fit a0 moves ~2x")
print("  across the physical M/L range -- the RAR does NOT pin a0 (non-diagnostic, as")
print("  banked). The row's content: the Planck-fixed value needs NO per-object freedom")
print("  and NO M/L outside the SPS range. Parameter count: 1 global Upsilon; LCDM fits")
print("  the same 175 curves with ~2-3 halo parameters PER GALAXY (~350-525 total).")
assert in_c and in_a, "Planck value(s) fell outside the kinematic band -- ledger row fails"
json.dump(dict(band=[float(band_lo), float(band_hi)], per_upsilon=results),
          open(os.path.join(HERE, "p1_band.json"), "w"), indent=1)
print("\n  [p1_band.json written]")
