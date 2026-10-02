#!/usr/bin/env python3
"""CFG267 helper: ARITHMETIC ONLY, not a re-analysis of any paper.

How much does the predicted g_obs at fixed g_bar change when a published MOND/RAR comparison that used
a0 = 1.2e-10 m/s^2 (and the McGaugh+16 RAR, 'simple' or 'standard' interpolating function) is replaced by
the programme's law as written (a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 FITTED; canonical footing
9.3603e-11, alt footing 1.1312e-10; kernels nu_mono and P2 nu(y) = sqrt(1 + 1/y))?

Deep-MOND scaling g_obs = sqrt(a0 g_bar) gives sqrt(0.936/1.2) = 0.883 and sqrt(1.131/1.2) = 0.971 in g_obs.
At higher g_bar the ratio moves toward 1 because nu -> 1.  No data are read.
"""
import io, os, sys, contextlib, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
sys.path.insert(0, CFG)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as K4                     # the programme's committed kernels (nu_mono, nu_p2), read-only

A0_LIT, A0_CAN, A0_ALT = 1.2e-10, 9.3603e-11, 1.1312e-10

def nu_rar(y):      return 1.0 / (1.0 - np.exp(-np.sqrt(y)))                 # McGaugh, Lelli & Schombert 2016
def nu_simple(y):   return 0.5 + np.sqrt(0.25 + 1.0 / y)                      # 'simple' (Famaey & Binney 2005)
def nu_standard(y): return np.sqrt(0.5 + np.sqrt(0.25 + 1.0 / y**2))         # 'standard' (Kent 1987)
nu_mono = lambda y: np.asarray(K4.nu_mono(y), float)
nu_p2 = lambda y: np.asarray(K4.nu_p2(y), float)

GBAR = np.array([1e-12, 1e-11, 3e-11, 1e-10, 3e-10, 1e-9, 3e-9])            # m/s^2
KERNELS_LIT = {"RAR(McGaugh16)": nu_rar, "simple": nu_simple, "standard": nu_standard}

def g_pred(nu, a0, gbar):
    return gbar * nu(gbar / a0)

rows = []
print("ratio of predicted g_obs at fixed g_bar:  (programme law) / (literature law with a0 = 1.2e-10)")
print("g_bar [m/s^2]  y_lit=g_bar/1.2e-10 | lit kernel      | nu_mono can  nu_mono alt  P2 can  P2 alt | same kernel, a0 can / alt")
for name, nl in KERNELS_LIT.items():
    for gb in GBAR:
        ref = g_pred(nl, A0_LIT, gb)
        r = dict(lit_kernel=name, g_bar=gb, y_lit=gb / A0_LIT,
                 mono_can=float(g_pred(nu_mono, A0_CAN, gb) / ref), mono_alt=float(g_pred(nu_mono, A0_ALT, gb) / ref),
                 p2_can=float(g_pred(nu_p2, A0_CAN, gb) / ref), p2_alt=float(g_pred(nu_p2, A0_ALT, gb) / ref),
                 same_can=float(g_pred(nl, A0_CAN, gb) / ref), same_alt=float(g_pred(nl, A0_ALT, gb) / ref))
        rows.append(r)
        print(f"{gb:9.1e}  {gb/A0_LIT:9.3f}           | {name:15s} | {r['mono_can']:.3f}        {r['mono_alt']:.3f}        "
              f"{r['p2_can']:.3f}   {r['p2_alt']:.3f}  | {r['same_can']:.3f} / {r['same_alt']:.3f}")

# ---- per-lane typical regimes (y_can = g_bar / 9.3603e-11, taken from the lanes' committed READMEs; descriptive only)
LANE_Y = [("KURVS (CFG140, R_max)", 0.06), ("KURVS (CFG140, R_max)", 0.67), ("HZ9 (CFG271, outer ring, M986)", 0.41),
          ("HZ9 (CFG271, outer ring, M103)", 1.13), ("CRISTAL (CFG220, two discs)", 1.0), ("CRISTAL (CFG220, two discs)", 1.6),
          ("ALPINE (CFG228)", 1.3), ("ALPINE (CFG228)", 3.3), ("RC100 (CFG233 median)", 1.96), ("SINS AO (CFG280 median)", 2.14),
          ("KMOS3D (CFG270 T1 median)", 2.20), ("ALESS 122.1 (CFG229)", 4.8), ("Roman-Oliveira (CFG277)", 4.45),
          ("Roman-Oliveira (CFG277)", 21.25), ("Amvrosiadis (CFG274)", 6.0), ("Amvrosiadis (CFG274)", 52.8),
          ("ALPAKA (CFG229/272)", 8.2), ("ALPAKA (CFG229/272)", 157.0), ("SPT0418-47 (CFG228)", 10.0)]
print("\nat the lanes' own regimes: ratio (programme law) / (McGaugh16 RAR with a0 = 1.2e-10) at fixed g_bar")
print("lane                               y_can   g_bar[m/s2]  nu_mono can  nu_mono alt  P2 can  P2 alt")
lane_rows = []
for lab, yc in LANE_Y:
    gb = yc * A0_CAN
    ref = g_pred(nu_rar, A0_LIT, gb)
    r = dict(lane=lab, y_can=yc, g_bar=gb, mono_can=float(g_pred(nu_mono, A0_CAN, gb) / ref), mono_alt=float(g_pred(nu_mono, A0_ALT, gb) / ref),
             p2_can=float(g_pred(nu_p2, A0_CAN, gb) / ref), p2_alt=float(g_pred(nu_p2, A0_ALT, gb) / ref))
    lane_rows.append(r)
    print(f"{lab:34s} {yc:6.2f}  {gb:9.2e}    {r['mono_can']:.3f}        {r['mono_alt']:.3f}        {r['p2_can']:.3f}   {r['p2_alt']:.3f}")

deep = dict(can=float(np.sqrt(A0_CAN / A0_LIT)), alt=float(np.sqrt(A0_ALT / A0_LIT)))
print(f"deep-MOND limit sqrt(a0/1.2e-10): canonical {deep['can']:.4f}, alt {deep['alt']:.4f}")
# control: in the deep limit every kernel's ratio at fixed kernel must equal sqrt(a0 ratio)
ctl = abs(float(g_pred(nu_rar, A0_CAN, 1e-14) / g_pred(nu_rar, A0_LIT, 1e-14)) - deep["can"])
print(f"control: RAR kernel deep-limit ratio minus sqrt(a0 ratio) = {ctl:.2e} (must be < 1e-3)")
assert ctl < 1e-3
json.dump(dict(rows=rows, lane_rows=lane_rows, deep_limit=deep, note="arithmetic only; no data read; kappa = 1/2 FITTED"),
          open(os.path.join(HERE, "a0_kernel_shift_arithmetic_results.json"), "w"), indent=1)
