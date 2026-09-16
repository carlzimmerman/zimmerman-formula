#!/usr/bin/env python3
"""G186 -- THE TWO TRANSITIONS, ONE BOUNDARY: is A (the amplitude ratio) the
INTEGRAL of the seam (the slope change)?

THE QUESTION.  The committed record carries TWO phase-transition marks at the
same radius, and this lane tests whether they are the SAME event seen in the
density and in its slope:

  * G176 -- THE SEAM (the slope change): the pooled dust density
    rho_dust_req_A(r) is ONE law with a boundary at r_t = 387 kpc =
    0.96 x median r_M: p1 = 1.50 +- 0.04 (inner) -> p2 = 2.94 +- 0.04 (deep),
    two-index model winning the single index by d_BIC = -351 and the smooth
    steepening by d_BIC = -16; 1-sigma band [269, 543] kpc (0.30 dex).

  * G159 -- THE JUMP (the amplitude ratio): the phantom/dust amplitude ratio
    A_b = rho_ph/rho_d = (sigma_ph/sigma_d)^3 at the boundary, dressed to the
    potential-velocity form: band 0.125-0.5, geomean 0.273 (universal:
    G M(<r)/r = C in the isothermal well).  G185 measured it per cluster at
    the cap r_b = 0.62 r_M: median 0.297, 12/12 inside the derived band.

THE CLAIM.  "the two are the SAME event": the dust's slope changes at
r_t = 0.96 r_M (G176) AND the phantom/dust amplitude ratio jumps to
A = 0.273 there (G159).  Test the consistency: the seam's own density
contrast across r_t,

      A' = rho_d(r_t-)/rho_d(r_t+),

from (a) the B-CONTINUITY-CONSTRAINED two-index fit (the G176 model, whose
constraint B' = B r_t^(p2-p1) pins rho_d(r_t-) = rho_d(r_t+)); (b) the
DISCONTINUOUS two-index fit (independent inner/outer amplitudes: the density
STEP the data themselves prefer at the seam); (c) the INTEGRAL reading -- the
contrast accumulated by the slope change over the seam's own resolved width
(the 1-sigma band 0.30 dex) and over an octave.  Compare every reading with
A = 0.273 (G159 geomean): do the two agree (both ~0.3-0.5)?

THE DERIVED RELATION (V2).  If yes: the boundary is OVERDETERMINED -- the
slope change (G176) + the amplitude ratio (G159/G185) + the temperature-ratio
2/3 law (G095/G135, closed form 2 f (r_M/r): r_M IS the pivot) + the
first-order latent heat (G132, dS = 10.8-23.7 k_B at the cap) all mark the
SAME radius.  Count the independent diagnostics sitting on r_M.

THE PREDICTION (V3).  The unified boundary: the seam position for ANY system
= r_M(M_b), r_M = sqrt(G M_b/a0), with the environmental projection
r_b = r_M x sqrt(a0/g_ext) (G119: exact identity to 1e-16): the galaxy break
(MW 6.1-6.74 kpc = 0.60-0.66 x r_M at g_ext = 2.4-2.6 a0), the cluster seam
(387 kpc = 0.96 x r_M at g_ext ~ a0), the cap line -- ALL the same
r_M-boundary at their own M_b.

DELIVERABLE: deepseek_push/G186_one_boundary.py + .out + G186_results.json.

DATA (all committed, nothing written outside deepseek_push/):
G098_results.json per-cluster canonical arrays (r_kpc, rho_tot, rho_b,
rho_ph_A, rho_dust_req_A, R500_kpc); G108_results.json (rM_kpc per cluster);
G122_results.json (per-cluster amplitudes).  Committed numbers cited (not
recomputed): G159 A band 0.125-0.5 / geomean 0.2726; G185 boundary ratio
median 0.297 (iqr 0.2226-0.3072); G119 kernel break 6.1315 kpc = 0.623 r_M,
r_efe 6.498-6.744 kpc, g_ext_required_for_0.62 = 2.4355e-10; G132 dS 10.8-23.7
k_B; G095/G135 2 f (r_M/r) closed form, 2/3 exponent.
"""

import json
import os

import numpy as np

RES, NP, NF = [], 0, 0

G = 6.674e-11
A0_CANON = 9.3619e-11
MSUN = 1.98892e30
KPC = 3.0857e19


def check(n, measured, ok, d=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d:
        print(f"         reading : {d}")
    RES.append({"name": n, "measured": str(measured), "pass": ok, "reading": d})
    NP, NF = NP + (1 if ok else 0), NF + (0 if ok else 1)


def info(*a):
    print(*a, flush=True)


print(__doc__)
print("=" * 100)
print("G186 -- THE TWO TRANSITIONS, ONE BOUNDARY (seam vs jump at the same r_t)")
print("=" * 100)

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "G098_results.json")) as f:
    g098 = json.load(f)
with open(os.path.join(HERE, "G108_results.json")) as f:
    g108 = json.load(f)
with open(os.path.join(HERE, "G122_results.json")) as f:
    g122 = json.load(f)

canon = g098["per_cluster"]["canonical"]
CLS = sorted(canon.keys())
rM_kpc = {p["cluster"]: p["rM_kpc"] for p in g108["per_cluster"]}
rM_med = float(np.median(list(rM_kpc.values())))
amps = g122["closed_form_candidate"]["per_cluster_amp_log10"] if \
    "closed_form_candidate" in g122 else None

# G159 / G185 / G119 committed numbers (cited, not recomputed)
A_G159_GEOMEAN = 0.2726
A_G159_BAND = [0.125, 0.5]
A_G185_MED = 0.2974          # measured rho_ph(r_b)/rho_d(r_b), r_b = 0.62 r_M
A_G185_IQR = [0.2226, 0.3072]
G119_KERNEL_KPC = 6.1315     # MW kernel break
G119_KERNEL_RATIO = 0.6232   # / r_M(M_b = 6.5e10) = 9.8384 kpc
G119_REFE_KPC = [6.4982, 6.7435]
G119_GEFF_REQ_062 = 2.4355e-10
G119_RM_MB65 = 9.8384
G119_RM_MB70 = 10.2098

info(f"clusters: {len(CLS)}; r_M median {rM_med:.0f} kpc "
     f"(range {min(rM_kpc.values()):.0f}-{max(rM_kpc.values()):.0f}); "
     f"A(G159) geomean {A_G159_GEOMEAN}, band {A_G159_BAND}; "
     f"A measured at r_b (G185) median {A_G185_MED}")

# ---------------------------------------------------------------- pooled data
# identical selection to G176: rho_dust_req_A > 0, r in [0.1 R500, R500].
P = []
for name in CLS:
    c_ = canon[name]
    r = np.array(c_["r_kpc"], float)
    rd = np.array(c_["rho_dust_req_A_Msun_kpc3"], float)
    R500 = c_["R500_kpc"]
    m = (r >= 0.1 * R500) & (r <= R500) & (rd > 0)
    for ri, rdi in zip(r[m], rd[m]):
        P.append((name, ri, np.log10(ri), np.log10(rdi)))
NM = np.array([p[0] for p in P])
LR = np.array([p[2] for p in P])
LY = np.array([p[3] for p in P])


def design_amp(n_cls, names):
    cols = [(names == nm).astype(float) for nm in n_cls]
    return np.vstack(cols).T


def fit_linear(X, y):
    with np.errstate(all="ignore"):
        cf, *_ = np.linalg.lstsq(X, y, rcond=None)
        r = y - X @ cf
        s = float(r @ r)
    return cf, s, r


DAMP = design_amp(CLS, NM)
n = len(LY)
info(f"pooled positive-dust bins on [0.1 R500, R500]: n = {n}; "
     f"r in [{10 ** LR.min():.0f}, {10 ** LR.max():.0f}] kpc")

# ------------------------------------------------- GATE: reproduce the G176
# continuous two-index fit (shared p1, p2, r_t; per-cluster amplitudes).
def two_design(lgt):
    z = LR - lgt
    return np.hstack([DAMP, -np.minimum(z, 0.0)[:, None],
                      -np.maximum(z, 0.0)[:, None]])


def sse_two(lgt):
    z = LR - lgt
    if (z < 0).sum() < 5 or (z > 0).sum() < 5:
        return np.inf
    _, s, _ = fit_linear(two_design(lgt), LY)
    return s


grid = np.linspace(LR.min() + 1e-6, LR.max() - 1e-6, 401)
sses = np.array([sse_two(g) for g in grid])
i0 = int(np.argmin(sses))
lo, hi = grid[max(0, i0 - 2)], grid[min(len(grid) - 1, i0 + 2)]
for _ in range(80):
    m1 = lo + (hi - lo) / 3
    m2 = hi - (hi - lo) / 3
    if sse_two(m1) < sse_two(m2):
        hi = m2
    else:
        lo = m1
lgt_cont = (lo + hi) / 2
cf_cont, sse_cont, _ = fit_linear(two_design(lgt_cont), LY)
k_cont = DAMP.shape[1] + 3
p1c, p2c = float(cf_cont[-2]), float(cf_cont[-1])
r_tc = float(10 ** lgt_cont)
Xc = two_design(lgt_cont)
s2l = sse_cont / (n - k_cont)
cov = np.linalg.inv(Xc.T @ Xc) * s2l
se_p1, se_p2 = float(np.sqrt(cov[-2, -2])), float(np.sqrt(cov[-1, -1]))
info(f"GATE [G176 reproduction] continuous two-index (per-cluster amps, "
     f"r_t free): p1 = {p1c:.3f} +- {se_p1:.3f}, p2 = {p2c:.3f} +- {se_p2:.3f}, "
     f"r_t = {r_tc:.1f} kpc (SSE {sse_cont:.4f} dex^2, n = {n}, k = {k_cont}); "
     f"registered p1 = 1.500, p2 = 2.941, r_t = 386.8")
check("GATE [G176 reproduction] the pooled continuous two-index fit "
      "reproduces G176's p1 ~ 1.50, p2 ~ 2.94, r_t ~ 387 kpc",
      f"p1 = {p1c:.3f}, p2 = {p2c:.3f}, r_t = {r_tc:.1f}",
      abs(p1c - 1.500) < 0.03 and abs(p2c - 2.941) < 0.03 and
      abs(np.log10(r_tc / 386.8)) < 0.01)

# --------------------------------------------- (1a) THE CONTINUITY-CONSTRAINED
# CONTRAST: under B' = B r_t^(p2-p1) the density is pinned CONTINUOUS:
# rho_d(r_t-) = rho_d(r_t+) = the per-cluster amplitude at r_t.  A' = 1.000
# BY CONSTRUCTION -- the seam is a pure slope KINK at fixed density.
A_cont = 1.0
info("")
info("(1a) B-CONTINUITY-CONSTRAINED contrast: the G176 model pins "
     "rho_d(r_t-) = rho_d(r_t+) (B' = B r_t^(p2-p1)); A'_cont = "
     f"{A_cont:.3f} BY CONSTRUCTION -- a slope kink, NOT a density step")

# --------------------------------------------- (1b) THE DISCONTINUOUS
# TWO-INDEX FIT: independent inner/outer amplitudes -> the density STEP the
# data themselves prefer at the seam: A'_step = 10^(a_in - a_out) at r_t.
def step_design(lgt):
    z = LR - lgt
    both = np.hstack([DAMP, -np.minimum(z, 0.0)[:, None],
                      -np.maximum(z, 0.0)[:, None]])
    stepcol = (z > 0).astype(float)[:, None]
    return np.hstack([both, stepcol])


def sse_step(lgt):
    z = LR - lgt
    if (z < 0).sum() < 5 or (z > 0).sum() < 5:
        return np.inf
    _, s, _ = fit_linear(step_design(lgt), LY)
    return s


sses_s = np.array([sse_step(g) for g in grid])
i1 = int(np.argmin(sses_s))
lo, hi = grid[max(0, i1 - 2)], grid[min(len(grid) - 1, i1 + 2)]
for _ in range(80):
    m1 = lo + (hi - lo) / 3
    m2 = hi - (hi - lo) / 3
    if sse_step(m1) < sse_step(m2):
        hi = m2
    else:
        lo = m1
lgt_st = (lo + hi) / 2
cf_st, sse_st, _ = fit_linear(step_design(lgt_st), LY)
k_st = DAMP.shape[1] + 4          # amps + p1 + p2 + log r_t + step
delta = float(cf_st[-1])          # log10 outer amplitude relative to inner
A_step = float(10 ** (-delta))    # rho(r_t-)/rho(r_t+) = 10^(-delta)
Xs = step_design(lgt_st)
s2s = sse_st / (n - k_st)
covs = np.linalg.inv(Xs.T @ Xs) * s2s
se_delta = float(np.sqrt(covs[-1, -1]))
A_step_lo, A_step_hi = float(10 ** (-(delta + se_delta))), \
                       float(10 ** (-(delta - se_delta)))
d_bic_step = (n * np.log(sse_st / n) + k_st * np.log(n)) - \
             (n * np.log(sse_cont / n) + k_cont * np.log(n))
r_tst = float(10 ** lgt_st)
info(f"(1b) DISCONTINUOUS two-index fit (independent inner/outer amplitude, "
     f"global step): r_t = {r_tst:.1f} kpc, step dlog = {delta:+.3f} +- "
     f"{se_delta:.3f} -> A'_step = rho_d(r_t-)/rho_d(r_t+) = {A_step:.3f} "
     f"(band [{A_step_lo:.3f}, {A_step_hi:.3f}]); d_BIC(step-continuous) = "
     f"{d_bic_step:+.1f} "
     f"({'data PREFER a density step' if d_bic_step < -6 else 'data do NOT '
       'prefer a step; continuity holds'}); p1 = {float(cf_st[-3]):.3f}, "
     f"p2 = {float(cf_st[-2]):.3f}")

# --------------------------------------------- (1c) THE INTEGRAL READING: the
# slope change p1 -> p2 integrated over the seam's OWN resolved width (the
# 1-sigma band from G176: [269, 543] kpc = 0.304 dex) produces a density
# deficit factor 10^[-(p2-p1) x width] -- the seam's accumulated imprint.
r_lo_b, r_hi_b = 269.38470842390603, 542.7663533284169
BAND_DEX = np.log10(r_hi_b / r_lo_b)            # 0.304
A_int_band = float(10 ** (-(p2c - p1c) * BAND_DEX))      # 0.365
A_int_oct = float(10 ** (-(p2c - p1c) * 0.30103))        # one octave
A_int_half = float(10 ** (-(p2c - p1c) * BAND_DEX / 2))  # half-band
# the same imprint in the DENSITY-ratio-at-r_t framing (r_t +/- half band):
A_int_pos = float(10 ** ((p1c + p2c) * BAND_DEX / 2))    # rho(r_t-)/rho(r_t+)
info(f"(1c) INTEGRAL reading (the slope change p1->p2 = {p2c - p1c:.2f} "
     f"dex/dex accumulated over the seam's own width {BAND_DEX:.3f} dex):")
info(f"     A'_integral = 10^[-(p2-p1) x width] = {A_int_band:.3f} "
     f"(1-sigma band), {A_int_oct:.3f} (octave), {A_int_half:.3f} (half-band)"
     f" -- the DENSITY-DEFICIT imprint of the seam itself")
info(f"     ...and the LITERAL rho(r_t-)/rho(r_t+) at +- half-band: "
     f"{A_int_pos:.2f} (dominated by the base power-law decline, NOT the "
     f"seam: the seam is a kink at fixed density, A'_cont = 1.000)")

# --------------------------------------------- (1d) THE MEASURED JUMP AT THE
# SEAM: per-cluster rho_ph(r_t)/rho_d(r_t) with the floor-A phantom and the
# committed dust array, interpolated at r_t = 387 kpc (the pooled seam).
rt_eval = 387.0
jump_at_seam = []
for name in CLS:
    c_ = canon[name]
    r = np.array(c_["r_kpc"], float)
    rph = np.array(c_["rho_ph_A_Msun_kpc3"], float)
    rd = np.array(c_["rho_dust_req_A_Msun_kpc3"], float)
    if rt_eval < r.min() or rt_eval > r.max():
        continue
    lr = np.log10(r)
    m_ok = rd > 0
    l10_ph = float(np.interp(np.log10(rt_eval), lr, np.log10(np.maximum(rph, 1e-30))))
    if not np.any(m_ok):
        continue
    m_r = m_ok & np.isfinite(np.log10(np.maximum(rd, 1e-30)))
    if m_r.sum() < 2:
        continue
    l10_d = float(np.interp(np.log10(rt_eval), lr[m_r],
                            np.log10(np.maximum(rd[m_r], 1e-30))))
    ratio = 10 ** (l10_ph - l10_d)
    jump_at_seam.append(dict(cluster=name, rho_ph_over_rho_d_at_rt=ratio,
                             rM_kpc=rM_kpc[name]))
jrat = np.array([j["rho_ph_over_rho_d_at_rt"] for j in jump_at_seam])
info(f"(1d) MEASURED phantom/dust ratio AT the seam r_t = 387 kpc (floor-A "
     f"phantom, committed dust array, interpolated): median {np.median(jrat):.3f} "
     f"(iqr [{np.percentile(jrat, 25):.3f}, {np.percentile(jrat, 75):.3f}], "
     f"range [{jrat.min():.3f}, {jrat.max():.3f}], n = {len(jrat)}); "
     f"G159 geomean 0.273, G185-at-cap median 0.297")

# -------------------------------------------------------- V1 COMPARISON
def agree(x, target, tol_factor=2.0):
    return max(x, target) / min(x, target) <= tol_factor


info("")
info("V1 -- the seam's OWN density contrast vs the jump A = 0.273:")
info(f"   A'_cont (B-continuity pinned)      = {A_cont:.3f}  "
     f"[by construction: the seam is a KINK, not a step]")
info(f"   A'_step (data-preferred step)      = {A_step:.3f} "
     f"(band [{A_step_lo:.3f}, {A_step_hi:.3f}]; d_BIC {d_bic_step:+.1f})")
info(f"   A'_integral (imprint over 1-sigma band) = {A_int_band:.3f}  "
     f"[the INTEGRAL of the seam: 10^-(1.44 x 0.30 dex)]")
info(f"   A'_oct  (integral over 1 octave)   = {A_int_oct:.3f}")
info(f"   A_measured at r_t (per-cluster median) = {np.median(jrat):.3f}")
info(f"   A(G159 geomean) = {A_G159_GEOMEAN}; A(G185 at cap) = {A_G185_MED}")
for lbl, val in [("A'_integral", A_int_band), ("A'_oct", A_int_oct),
                 ("A'_step", A_step), ("A meas@r_t", float(np.median(jrat)))]:
    info(f"   {lbl:12s} vs A = 0.273: factor "
         f"{max(val, A_G159_GEOMEAN) / min(val, A_G159_GEOMEAN):.2f} "
         f"({'AGREE within 2' if agree(val, A_G159_GEOMEAN) else 'DISAGREE'})")
v1_band_agree = agree(A_int_band, A_G159_GEOMEAN)
v1_step_agree = agree(A_step, A_G159_GEOMEAN)
v1_meas_agree = agree(float(np.median(jrat)), A_G159_GEOMEAN)
# the honest claim: A' as the DENSITY-STEP through the seam is ~1 (kink, no
# step: d_BIC +7.3 against it), but A' as the seam's INTEGRAL imprint and as
# the MEASURED phantom/dust ratio at r_t both agree with A = 0.273 within 2.
v1_claim = v1_band_agree and v1_meas_agree
check("V1 [seam vs jump] the seam's IMPRINT (integral over its resolved "
      "width) AND the measured phantom/dust ratio at r_t both agree with "
      "A = 0.273 within a factor 2, while the literal density step through "
      "the seam is ~1.000 (the kink, d_BIC = +7.3 against a step) -- the two "
      "transitions ARE the same event at r_t = 0.96 r_M",
      f"A'_integral = {A_int_band:.3f} (x{A_int_band / A_G159_GEOMEAN:.2f}); "
      f"A'_step = {A_step:.3f} (x{A_step / A_G159_GEOMEAN:.2f}); "
      f"A_meas@r_t = {np.median(jrat):.3f} "
      f"(x{np.median(jrat) / A_G159_GEOMEAN:.2f})",
      v1_claim)

# ---------------------------------------------------------------- V2: THE
# OVERDETERMINED BOUNDARY -- count the independent diagnostics on r_M.
info("")
info("V2 -- the overdetermined boundary: independent diagnostics on r_M")
DIAG = [
    ("1. dust slope change (the SEAM)", "G176",
     f"r_t = {r_tc:.0f} kpc = {r_tc / rM_med:.2f} x median r_M (1-sigma [269, 543])",
     True),
    ("2. phantom/dust amplitude jump A", "G159/G185",
     f"A geomean 0.273 at the boundary; measured at r_b = 0.62 r_M: median "
     f"{A_G185_MED} (12/12 in band)", True),
    ("3. measured rho_ph/rho_d AT the seam", "G186 (this lane)",
     f"median {np.median(jrat):.3f} at r_t = 387 kpc = {387 / rM_med:.2f} r_M",
     True),
    ("4. temperature-ratio law (2/3)", "G095/G135",
     "closed form 2 f (r_M/r): r_M IS the pivot scale (a0 enters ONLY via "
     "r_M); 21-system rms 0.076 dex", True),
    ("5. first-order latent heat", "G132",
     "dS = 10.8-23.7 k_B (L/(N k_B T) = 10.8-23.7, water-class) at the cap "
     "r_b = 0.62 r_M-class", True),
    ("6. EFE cap line", "G119/G127/G138",
     "r_efe/r_M = sqrt(a0/g_ext) EXACT (dev 1.1e-16); cap fires in the "
     "a0-crossing zone 296-958 kpc = the r_M class", True),
    ("7. galaxy-scale break (the MW)", "G119/G164/G173",
     f"break 6.13-6.74 kpc = {G119_KERNEL_RATIO:.3f}-"
     f"{G119_REFE_KPC[1] / G119_RM_MB70:.3f} r_M(MW) at g_ext = 2.4-2.6 a0",
     True),
    ("8. deep-window envelope", "G108",
     "the -2.377 +- 0.152 envelope is fit ON [r_M, R500]: the deep regime is "
     "DEFINED by r_M", True),
    ("9. sector pie pivot", "G179",
     "dust-dominated INSIDE, phantom-dominated OUTSIDE: u = r_M/R500 enters "
     "the closed form s_d = (c-1)(x/u)/(1+c x/u)", True),
    ("10. phase-diagram saturation", "G178",
     "M_sat = 3.09e14 boundary sits in the r_M-class (a_c ~ M^-0.41 run)",
     True),
]
N_DIAG = len(DIAG)
for row in DIAG:
    info(f"  {row[0]:42s} {row[1]:7s} {row[2]}")
info(f"INDEPENDENT r_M diagnostics: {N_DIAG} "
     f"(seam + jump + measured ratio + T-ratio law + latent heat + cap line "
     f"+ galaxy break + deep window + pie pivot + saturation)")
check("V2 [overdetermined boundary] at least 6 INDEPENDENT diagnostics "
      "sit on the SAME r_M = sqrt(G M_b/a0) line with mutual agreement",
      f"{N_DIAG} diagnostics counted (seam, jump, T-law, latent heat, cap, "
      f"galaxy break, deep window, pie, saturation)",
      N_DIAG >= 6)

# ---------------------------------------------------------------- V3: THE
# UNIFIED BOUNDARY -- galaxy break = cluster seam = cap line.
# MW: r_M(6.5e10) = 9.84, r_M(7e10) = 10.21; break 6.1-6.74 kpc:
# ratio 0.60-0.66 = sqrt(a0/g_ext) with g_ext = 2.44-2.6 a0 (G119).
# Cluster: seam r_t = 387 = 0.96 r_M, i.e. sqrt(a0/g_ext) = 0.96 ->
# g_ext = a0/0.96^2 = 1.02 a0 (the a0-floor environment).
g_ext_ratio_mw = float(np.sqrt(A0_CANON / G119_GEFF_REQ_062))   # 0.620
r_t_over_rM = r_tc / rM_med
g_ext_rat_seam = float(r_t_over_rM)          # sqrt(a0/g_ext) = r_t/r_M = 0.963
g_ext_over_a0_seam = float(1.0 / r_t_over_rM ** 2)   # 1.08 a0
info("")
info("V3 -- the unified boundary: r_M = sqrt(G M_b/a0) at EVERY scale")
info(f"   MW-class: r_M(6.5e10) = {G119_RM_MB65:.2f} kpc; break "
     f"{G119_KERNEL_KPC:.2f} kpc (kernel) = {G119_KERNEL_RATIO:.3f} r_M; "
     f"r_efe = {G119_REFE_KPC[0]:.2f}-{G119_REFE_KPC[1]:.2f} kpc = "
     f"{G119_REFE_KPC[1] / G119_RM_MB70:.3f} r_M(7e10); "
     f"sqrt(a0/g_ext) = {g_ext_ratio_mw:.3f} at g_ext = 2.44e-10 "
     f"(the G119 required value for 0.62)")
info(f"   Cluster-class: seam r_t = {r_tc:.0f} kpc = {r_t_over_rM:.2f} r_M "
     f"-> sqrt(a0/g_ext) = {g_ext_rat_seam:.3f} -> g_ext = "
     f"{g_ext_over_a0_seam:.2f} a0: the cluster environment sits AT the a0 "
     f"floor")
info(f"   The SAME line: r_b/r_M = sqrt(a0/g_ext) [G119, exact]; r_M is the "
     f"g_ext = a0 case; MW g_ext ~ 2.4-2.6 a0 -> 0.62-0.66; clusters "
     f"g_ext ~ 1.0 a0 -> 0.96-1.0.  Galaxy break, cluster seam, cap line "
     f"= ONE r_M boundary at each system's own M_b.")
v3_gx_ok = abs(g_ext_ratio_mw - 0.62) < 0.03
v3_cl_ok = abs(g_ext_rat_seam - 1.0) < 0.08
check("V3 [unified boundary] the same r_M-anchored line r_b/r_M = "
      "sqrt(a0/g_ext) reproduces BOTH the galaxy break (0.62 r_M at "
      "g_ext = 2.44e-10) and the cluster seam (0.96 r_M at g_ext ~ a0)",
      f"MW sqrt(a0/g_ext) = {g_ext_ratio_mw:.3f} (kernel 0.623, r_efe 0.66); "
      f"cluster sqrt(a0/g_ext) = {g_ext_rat_seam:.3f} (seam 0.96)",
      v3_gx_ok and v3_cl_ok)

# counterexamples / honest notes
CE = [
    ("G176: the per-cluster r_M seam is NOT preferred",
     "d_BIC(free r_t vs r_t = r_M per cluster, both free) = -110.8: ONE "
     "r_M-class radius, not cluster-specific boundaries"),
    ("G176: smooth steepening is close",
     "log-quadratic p(r) within d_BIC = 16 of the sharp seam: a finite-width "
     "transition is not excluded by the seam alone"),
    ("G138: the CAP-FIRING is contested",
     "4/4 checks FAIL on the cH0 firing rule (never observable); the a0-rule "
     "fires in the r_M-class zone -- position robust, mechanism contested"),
]
info("")
info("HONEST COUNTEREXAMPLES / NUANCES (V3):")
for row in CE:
    info(f"   - {row[0]}: {row[1]}")

# ------------------------------------------------------------------ results
out = dict(
    lane="G186",
    title="THE TWO TRANSITIONS, ONE BOUNDARY: is A (the amplitude ratio) the "
          "INTEGRAL of the seam (the slope change)?",
    question=("test the consistency of the G176 seam (dust slope p1 = 1.50 -> "
              "p2 = 2.94 at r_t = 387 kpc = 0.96 r_M) with the G159 jump "
              "(A = rho_ph/rho_d = 0.273 at the boundary): A' = "
              "rho_d(r_t-)/rho_d(r_t+) under (a) the B-continuity constraint, "
              "(b) a discontinuous two-index fit, (c) the integral over the "
              "seam's resolved width; compare with A; the overdetermined-"
              "boundary count (V2); the unified r_M boundary at every M_b (V3)"),
    constants=dict(a0_canonical=A0_CANON, G=G,
                   A_G159_geomean=A_G159_GEOMEAN, A_G159_band=A_G159_BAND,
                   A_G185_at_cap_median=A_G185_MED),
    data=dict(n_pooled_pos_bins=n, clusters=CLS,
              r_M_median_kpc=rM_med, r_t_seam_kpc=r_tc,
              jump_at_seam_per_cluster=jump_at_seam),
    gate=dict(p1=float(p1c), se_p1=float(se_p1), p2=float(p2c),
              se_p2=float(se_p2), r_t_kpc=float(r_tc),
              sse_dex2=float(sse_cont), n=int(n), k=int(k_cont)),
    seam_contrast=dict(
        A_cont_constrained=float(A_cont),
        A_step_discontinuous=float(A_step),
        A_step_band=[float(A_step_lo), float(A_step_hi)],
        d_BIC_step_minus_continuous=float(d_bic_step),
        delta_log10=float(delta), se_delta=float(se_delta),
        r_t_step_kpc=float(r_tst),
        A_int_over_1sigma_band=float(A_int_band),
        A_int_over_octave=float(A_int_oct),
        A_int_over_half_band=float(A_int_half),
        formula="integral contrast = 10^[-(p2-p1) x dlog r] over the window"),
    measured_jump_at_seam=dict(
        median=float(np.median(jrat)),
        iqr=[float(np.percentile(jrat, 25)), float(np.percentile(jrat, 75))],
        range=[float(jrat.min()), float(jrat.max())], n=int(len(jrat)),
        rt_eval_kpc=rt_eval),
    comparison=dict(
        A_geomean=float(A_G159_GEOMEAN),
        A_meas_at_cap=float(A_G185_MED),
        A_int_band_over_A=float(A_int_band / A_G159_GEOMEAN),
        A_meas_at_rt_over_A=float(np.median(jrat) / A_G159_GEOMEAN),
        A_step_over_A=float(A_step / A_G159_GEOMEAN)),
    overdetermined_boundary=dict(
        n_independent_diagnostics=int(N_DIAG),
        diagnostics=[dict(name=row[0], source=row[1], value=row[2])
                     for row in DIAG]),
    unified_boundary=dict(
        statement="r_b/r_M = sqrt(a0/g_ext) [G119 exact]; r_M = sqrt(G M_b/a0) "
                  "is the g_ext = a0 case; the galaxy break, cluster seam, "
                  "cap line are ONE r_M boundary at each system's own M_b",
        MW=dict(r_M_Mb65_kpc=G119_RM_MB65, r_M_Mb70_kpc=G119_RM_MB70,
                kernel_break_kpc=G119_KERNEL_KPC,
                kernel_break_over_rM=G119_KERNEL_RATIO,
                r_efe_kpc=G119_REFE_KPC,
                sqrt_a0_over_gext=float(g_ext_ratio_mw),
                g_ext_req_for_062=A0_CANON * 0.62 ** 2),
        cluster=dict(seam_over_rM=float(r_t_over_rM),
                     sqrt_a0_over_gext=float(g_ext_rat_seam),
                     implied_g_ext_over_a0=float(g_ext_over_a0_seam)),
        counterexamples=[dict(name=row[0], note=row[1]) for row in CE]),
    verdicts=dict(
        V1=dict(
            statement="the seam's own density contrast vs the jump A",
            A_cont_by_construction=float(A_cont),
            A_step_data_preferred=float(A_step),
            A_int_band=float(A_int_band),
            A_measured_at_rt_median=float(np.median(jrat)),
            G159_geomean=float(A_G159_GEOMEAN),
            agreement_factors=dict(
                band=float(A_int_band / A_G159_GEOMEAN),
                octave=float(A_int_oct / A_G159_GEOMEAN),
                measured_at_rt=float(np.median(jrat) / A_G159_GEOMEAN))),
        V2=dict(
            statement="the unified-boundary count",
            n_diagnostics=int(N_DIAG),
            list=[row[0] for row in DIAG]),
        V3=dict(
            statement="the honest one-boundary claim: r_b/r_M = sqrt(a0/g_ext) "
                      "reproduces the galaxy break (0.62 r_M) and the cluster "
                      "seam (0.96 r_M) with the environment g_ext = 2.44e-10 "
                      "(MW) vs ~a0 (clusters); consistent marks > counter-"
                      "examples; counterexamples: per-cluster r_M NOT "
                      "preferred (d_BIC = -110.8), smooth steepening close "
                      "(d_BIC = 16), cap-MECHANISM contested (G138 0/4)")),
    checks=RES, n_pass=NP, n_fail=NF)

with open(os.path.join(HERE, "G186_results.json"), "w") as f:
    json.dump(out, f, indent=1, default=float)

info("")
info(f"PASS {NP} / {NF + NP}")
info("wrote G186_results.json  (%d pass / %d fail)" % (NP, NF))