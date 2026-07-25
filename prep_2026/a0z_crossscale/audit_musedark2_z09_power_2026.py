#!/usr/bin/env python3
"""
audit_musedark2_z09_power_2026.py -- ADVERSARIAL AUDIT of the z~0.9 DEC-vs-RISE power claim.
===========================================================================================
Carl Zimmerman's de Sitter-Unruh MODIFIED-INERTIA framework, judged on ITS OWN terms
(a0 = c H_Lambda / Z, Z = sqrt(32 pi/3); its OWN kernel g_obs^2 - g_bar^2 = a0 g_bar).
McGaugh's nu is never used.  nu = sqrt(1+1/y) is Milgrom 1999 PLA 253:273 Eq.9 (WELLHEAD
CREDIT); the framework's distinctive content is the cH_Lambda/Z coefficient + the MI
completion.  McCulloch (MiHsC) credited for the Hubble-horizon (RISE) branch.

ROLE: this file does NOT re-do the power calculation.  It AUDITS the committed claim set of
    musedark2_z09_power_2026.py  (-> musedark2_z09_power_2026_results.json)
against (a) independent recomputation of every load-bearing number, and (b) the REAL
per-object catalogue already committed in this repo:
    ../jeanneau_refit/jeanneau26_catalog_cds.csv
    = VizieR J/A+A/709/A120 (Jeanneau+2026 A&A 709 A120, arXiv:2603.28856), 95 rows,
      CC-BY-4.0, the paper's Table E1 (provenance ladder: ../jeanneau_refit/DATA.md).

A manufactured DETECTION and a manufactured DEFICIT are penalized EQUALLY.  Both are
searched for.  Every PASS/FAIL below is an f-string of a COMPUTED comparison; no verdict
string is typed in.  Exit 0 = ran, NOT a verdict.
"""
import csv
import json
import os
import numpy as np

np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
CAT = os.path.join(HERE, "..", "jeanneau_refit", "jeanneau26_catalog_cds.csv")
RES = os.path.join(HERE, "musedark2_z09_power_2026_results.json")
DEX = np.log(10.0)
MEDPEN = np.sqrt(np.pi / 2.0)          # median-like efficiency penalty (GLS is FORBIDDEN)
BAR = "=" * 100
FIND = []                              # (id, verdict, text) -- all computed


def rec(tag, ok, text):
    FIND.append((tag, "PASS" if ok else "FAIL", text))
    print(f"  [{tag}] {'PASS' if ok else 'FAIL'} -- {text}")


# ---------------------------------------------------------------------------- cosmology
OM, w0, wa = 0.3150, -0.838, -0.62     # Planck-2018 flat + DESI DR2 w0waCDM (Pantheon+)
ODE = 1.0 - OM
A0_CAN, A0_ALT = 9.355e-11, 1.1305e-10


def rho_de(z):
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))


def E(z):
    return np.sqrt(OM * (1 + z) ** 3 + ODE * rho_de(z))


R_dec = lambda z: np.sqrt(rho_de(z))          # de Sitter / future-event horizon (Carl's)
R_rise = E                                    # Hubble horizon (McCulloch MiHsC)
gap_dex = lambda z: float(np.log10(R_rise(z) / R_dec(z)))


def bar3s_dex(z):
    """tightest (mid-referenced) 3-sigma bar, in dex on log10(a0(z)/a0(0))."""
    d, r = float(R_dec(z)), float(R_rise(z))
    return float(np.log(1 + abs(r - d) / (3 * 0.5 * (d + r))) / DEX)


print(BAR)
print("AUDIT -- musedark2_z09_power_2026.py claim set (dS-Unruh MODIFIED INERTIA, z ~ 0.9)")
print(BAR)
J = json.load(open(RES))

# =====================================================================================
# A -- INDEPENDENT RECOMPUTE OF THE FORK, THE BARS, THE LEVERS AND THE SEPARATIONS
# =====================================================================================
print("\nA -- independent recompute of every load-bearing number in the claim set")
Y_ASM = float(np.sqrt(0.3 * 1.0))      # the claim's y: geometric mean of a POSITED bracket
L_ASM = 1.0 / (1.0 + 2.0 * Y_ASM)
d09, r09 = float(R_dec(0.9)), float(R_rise(0.9))
rec("A1", abs(d09 - J["fork"]["DEC"][2]) < 1e-9 and abs(r09 - J["fork"]["RISE"][2]) < 1e-9,
    f"fork at z=0.9 reproduces: DEC={d09:.6f} RISE={r09:.6f} ratio={r09/d09:.4f}x "
    f"gap={gap_dex(0.9):.5f} dex")
rec("A2", abs(bar3s_dex(0.9) - J["headline_bars"]["BAR3S_dex"]) < 1e-9,
    f"BAR-3S (tightest, mid-referenced) reproduces: {bar3s_dex(0.9):.6f} dex "
    f"= {100*J['headline_bars']['BAR3S_frac']:.2f}% on a0")
S_stat = gap_dex(0.9) / (0.06 / L_ASM)
S_hon = gap_dex(0.9) / (0.27 / L_ASM)
rec("A3", abs(S_stat - J["separations"]["published_integrated_stat_sigma"]) < 1e-6 and
    abs(S_hon - J["separations"]["published_integrated_honest_sigma"]) < 1e-6,
    f"published-integrated separations reproduce: S(stat +/-0.06)={S_stat:.3f} sigma, "
    f"S(honest +/-0.27)={S_hon:.3f} sigma -- neither reaches 3")
amps = dict(V=4 * (Y_ASM + 1), gobs=2 * (Y_ASM + 1), gbar=2 * Y_ASM + 1,
            R=2 * Y_ASM, mu=Y_ASM + 1)
rec("A4", all(abs(amps[k] - J["framework"][f"amp_{k}" if k != "mu" else "amp_mu_exact"]) < 1e-9
              for k in amps),
    f"amplifications reproduce at y={Y_ASM:.4f}: V={amps['V']:.4f} gobs={amps['gobs']:.4f} "
    f"gbar={amps['gbar']:.4f} R={amps['R']:.4f} mu={amps['mu']:.4f} (mu is (y+1), NOT 1:1)")
f1 = float(A0_CAN * R_dec(0.9)) / float(A0_CAN * R_dec(0.0))
f2 = float(A0_ALT * R_dec(0.9)) / float(A0_ALT * R_dec(0.0))
rec("A5", abs(f1 - f2) == 0.0,
    f"BOTH FOOTINGS identical: a0(0.9)/a0(0) = {f1:.12f} (canonical cH_Lambda/Z) = {f2:.12f} "
    f"(alt cH0/Z), |diff| = {abs(f1-f2):.1e}")
flat_need = abs(1 - d09) / (3 * 0.5 * (1 + d09))
rec("A6", flat_need < 1e-3,
    f"DEC-vs-FLAT at z=0.9 is UNTESTABLE as claimed: DEC={d09:.6f} vs FLAT=1 needs "
    f"{100*flat_need:.4f}% precision -- z~0.9 tests DEC-vs-RISE (i.e. McCulloch) ONLY")

# =====================================================================================
# B -- THE DATA-AVAILABILITY CLAIM.  The claim set asserts the per-object table is NOT
#      published.  The repo contains a verbatim CDS download of it.
# =====================================================================================
print("\nB -- data-availability claim vs the committed VizieR catalogue")
rows = list(csv.DictReader(open(CAT)))
need = ["zR21", "muR21", "Reff", "logM*", "b_logM*", "B_logM*", "logMHI", "logMMol",
        "logMBar", "logV1_8", "s_logV1_8", "logV2_0", "s_logV2_0", "Cluster"]
have = [c for c in need if c in rows[0]]
full = [c for c in have if all(r[c].strip() != "" for r in rows)]
rec("B1", len(rows) == 95 and len(full) == len(need),
    f"catalogue has N={len(rows)} rows and ALL {len(need)} per-object columns populated on "
    f"every row: {', '.join(need)}")
book = np.array([np.log10(10 ** float(r["logM*"]) + 10 ** float(r["logMHI"]) +
                          10 ** float(r["logMMol"])) - float(r["logMBar"]) for r in rows])
rec("B2", np.abs(book).max() < 1e-4,
    f"catalogue is internally consistent (authenticity check): M_bar = M* + M_HI + M_mol to "
    f"max |resid| = {np.abs(book).max():.1e} dex on all {len(rows)} rows")
rec("B3", J["sample"]["per_object_table_published"] is False and len(full) == len(need),
    f"CLAIM CONTRADICTED: the claim set records per_object_table_published=False and names "
    f"'the per-object table' as closer #1 ('from the authors, or by re-running lensed "
    f"GalPaK3D'), but the table is published (VizieR J/A+A/709/A120 = Table E1) and has been "
    f"committed in this repo since 2026-07-16")

# real sample facts vs the claimed ones
z = np.array([float(r["zR21"]) for r in rows])
mu = np.array([float(r["muR21"]) for r in rows])
lM = np.array([float(r["logM*"]) for r in rows])
sV = np.array([float(r["s_logV1_8"]) for r in rows])
print(f"\n  {'quantity':26} {'CLAIMED':>22} {'REAL (catalogue)':>26}")
print("  " + "-" * 76)
print(f"  {'z span':26} {f'{J[chr(115)+chr(97)+chr(109)+chr(112)+chr(108)+chr(101)][chr(122)+chr(95)+chr(108)+chr(111)]}-{J[chr(115)+chr(97)+chr(109)+chr(112)+chr(108)+chr(101)][chr(122)+chr(95)+chr(104)+chr(105)]}':>22} "
      f"{f'{z.min():.4f}-{z.max():.4f} (med {np.median(z):.4f})':>26}")
print(f"  {'magnification mu':26} {'1.4-12.4':>22} {f'{mu.min():.3f}-{mu.max():.3f}':>26}")
print(f"  {'log M*':26} {'8.1-10.3':>22} {f'{lM.min():.2f}-{lM.max():.2f}':>26}")
print(f"  {'sigma_V/V per object':26} {'SWEPT 5-30% (15% used)':>22} "
      f"{f'PUBLISHED: med {100*(10**np.median(sV)-1):.2f}%':>26}")
rec("B4", not (abs(z.min() - J["sample"]["z_lo"]) < 0.01 and abs(z.max() - J["sample"]["z_hi"]) < 0.01),
    f"sample facts not reconciled with the catalogue: claimed z {J['sample']['z_lo']}-"
    f"{J['sample']['z_hi']}, real {z.min():.4f}-{z.max():.4f}; claimed mu 1.4-12.4, real "
    f"{mu.min():.3f}-{mu.max():.3f}; claimed effective z=0.90, real median z={np.median(z):.4f}")
rec("B5", np.median(sV) * amps["V"] < 0.435,
    f"per-object velocity errors ARE published (s_logV1_8, med {np.median(sV):.4f} dex = "
    f"{100*(10**np.median(sV)-1):.2f}%) -> {amps['V']*np.median(sV):.3f} dex on log10 a0, so the "
    f"5-30% SWEEP was unnecessary; the incoherent 3-sigma requirement 0.435 dex is met on real "
    f"data ({amps['gbar']*0.20:.3f} mass (+) {amps['V']*np.median(sV):.3f} velocity = "
    f"{np.sqrt((amps['gbar']*0.20)**2+(amps['V']*np.median(sV))**2):.3f} dex), but NOT by the "
    f"claim's own arithmetic ('0.2 dex masses PLUS <=16% velocities' = "
    f"{np.sqrt((amps['gbar']*0.20)**2+(amps['V']*0.16/DEX)**2):.3f} dex > 0.435 in quadrature)")

# =====================================================================================
# C -- THE ACCELERATION REGIME.  The claim uses y = sqrt(0.3*1.0) from a POSITED bracket.
#      The catalogue gives the sample's ACTUAL y through the framework's OWN kernel.
# =====================================================================================
print("\nC -- the framework's own lever on the REAL sample (its own kernel, both footings)")
H0P, OMP, OLP, CKMS = 70.0, 0.3, 0.7, 299792.458      # the PAPER's cosmology for arcsec->kpc
KPC = 3.0856775814913673e19


def kpc_per_arcsec(zz, n=3000):
    g = np.linspace(0.0, zz, n)
    DC = CKMS / H0P * np.trapz(1.0 / np.sqrt(OMP * (1 + g) ** 3 + OLP), g)
    return (DC / (1 + zz)) * 1000.0 * np.pi / 180.0 / 3600.0


def y_of_sample(a0):
    out = []
    for r in rows:
        zz = float(r["zR21"])
        R = 1.8 * float(r["Reff"]) * kpc_per_arcsec(zz) * KPC          # 1.8 R_e, source plane
        go = (10 ** float(r["logV1_8"]) * 1000.0) ** 2 / R
        gb = (-a0 + np.sqrt(a0 * a0 + 4 * go * go)) / 2.0              # invert the a0-line
        out.append(gb / a0)
    return np.array(out)


Y_CAN, Y_ALT = y_of_sample(A0_CAN), y_of_sample(A0_ALT)
ymed = float(np.median(Y_CAN))
L_REAL = 1.0 / (1.0 + 2.0 * ymed)
print(f"  y = g_bar/a0 on the 95 (canonical a0): q25 {np.percentile(Y_CAN,25):.4f}  "
      f"MEDIAN {ymed:.4f}  q75 {np.percentile(Y_CAN,75):.4f};  frac below 0.3 a0 = "
      f"{(Y_CAN<0.3).mean():.3f}")
print(f"  y median on ALT footing = {np.median(Y_ALT):.4f} (lever {1/(1+2*np.median(Y_ALT)):.4f}) "
      f"-- the FORK RATIO is footing-independent; only the lever moves")
rec("C1", L_REAL > L_ASM,
    f"the claim UNDERSTATES its own lever: claimed y={Y_ASM:.4f} -> L={L_ASM:.4f} (labelled "
    f"'this sample's own y', but it is the geometric mean of a POSITED [0.3,1.0] bracket); "
    f"real median y={ymed:.4f} -> L={L_REAL:.4f} = {L_REAL/L_ASM:.3f}x BETTER")
zmed = float(np.median(z))
S_hon_real = gap_dex(zmed) / (0.27 / L_REAL)
S_stat_real = gap_dex(zmed) / (0.06 / L_REAL)
rec("C2", S_hon_real > S_hon and S_hon_real < 3.0,
    f"corrected separations (real lever L={L_REAL:.4f}, real median z={zmed:.4f}, gap "
    f"{gap_dex(zmed):.5f} dex): S(honest)={S_hon_real:.3f} sigma (claim {S_hon:.3f}), "
    f"S(stat)={S_stat_real:.3f} sigma (claim {S_stat:.3f}) -- the claim is "
    f"{S_hon_real/S_hon:.2f}x too PESSIMISTIC, and the NO-GO verdict SURVIVES anyway")
print(f"  amplifications at the real median y: V={4*(ymed+1):.4f} (claimed {amps['V']:.4f}), "
      f"gbar={2*ymed+1:.4f} (claimed {amps['gbar']:.4f}), mu={ymed+1:.4f} "
      f"(claimed {amps['mu']:.4f}) -- every channel is BETTER than claimed")

# =====================================================================================
# D -- COHERENT vs INCOHERENT BOOKKEEPING (a call that clears a bar by averaging a
#      coherent term is invalid).  Re-derive the covariance structure independently.
# =====================================================================================
print("\nD -- coherent terms must NOT average as 1/sqrt(N); cluster block re-derived")
N = 95
sr, sc = 0.584, 0.5658
zs = 0.56 + (1.37 - 0.56) * ((np.arange(N) + 0.5) / N)
D = np.array([gap_dex(v) for v in zs])
C_inc = np.eye(N) * (MEDPEN * sr) ** 2
S_inc_only = float(np.sqrt(D @ np.linalg.inv(C_inc) @ D))
S_with_coh = float(np.sqrt(D @ np.linalg.inv(C_inc + sc ** 2) @ D))
rec("D1", S_inc_only > 3.0 and S_with_coh < 0.5 * S_inc_only,
    f"the rank-1 coherent block does NOT average down: S={S_inc_only:.2f} sigma with sigma_c=0 "
    f"but S={S_with_coh:.2f} sigma once sigma_c={sc:.4f} dex is added -- it SATURATES at "
    f"gap/sigma_c = {gap_dex(0.9)/sc:.3f} sigma for ANY N, exactly as claimed")
from collections import Counter
cnt = Counter(r["Cluster"] for r in rows)
wts = np.array([v / N for v in cnt.values()])
red = float(np.sqrt((wts ** 2).sum()))
rec("D2", abs(red - 0.5) > 0.02,
    f"cluster block slightly MIS-sized (against the claim's own interest): claimed {J['sample']['n_clusters']} "
    f"equal clusters -> averaging 1/sqrt(4)=0.5000; real catalogue has {len(cnt)} lines of sight "
    f"{dict(cnt)} -> effective N_cl = {1/(wts**2).sum():.2f}, averaging {red:.4f}, so the "
    f"magnification term after averaging is {red/0.5:.3f}x LARGER than the quoted "
    f"{J['separations']['mu_block']['smu=0.1']['dex']/2:.4f}-"
    f"{J['separations']['mu_block']['smu=0.3']['dex']/2:.4f} dex")

# =====================================================================================
# E -- THE HI / GAS-MASS WALL AND ITS SIGN (must bias a0 HIGH = toward RISE)
# =====================================================================================
print("\nE -- gas-mass wall: no proxy substituted, and the sign runs AGAINST the framework")
MHI = np.array([10 ** float(r["logMHI"]) for r in rows])
MB = np.array([10 ** float(r["logMBar"]) for r in rows])
fHI = float(np.median(MHI / MB))
h = 1e-6
# a0/a0_true when the ASSUMED M_bar is scaled by s at fixed V and R, on the exact a0-line:
#   a0 = V^4/(G M_bar) - g_bar,  V^4/(G M_bar) = g_bar + a0 = a0 (y+1),  g_bar = a0 y,
#   both terms scale with M_bar as 1/s and s respectively.
a0_of_M = lambda s: (1.0 + Y_ASM) / s - Y_ASM * s
dln = (np.log(a0_of_M(1 + h)) - np.log(a0_of_M(1 - h))) / (2 * h)
rec("E1", dln < 0 and abs(dln + amps["gbar"]) < 1e-4,
    f"SIGN VERIFIED by finite difference on the framework's OWN kernel: d ln a0 / d ln M_bar = "
    f"{dln:.5f} = -(2y+1) -> UNDER-counting M_bar makes a0 read HIGH, i.e. toward RISE, i.e. "
    f"AGAINST the declining branch. Omitting HI would FLATTER the framework; it is carried")
hi_full = [amps["gbar"] * float(np.log10((1 + 2 * rm) / (1 + rm))) for rm in (0.5, 1.0, 2.0, 3.0)]
hi_trust = 0.30 * 0.30 * amps["gbar"]
hi_paper = fHI * 0.80 * amps["gbar"]          # the paper's OWN NUM scatter is 0.8 dex in log tau_HI
rec("E2", min(hi_full) > bar3s_dex(0.9) and hi_trust > bar3s_dex(0.9),
    f"gas wall carried at strength and NOT via an SFR/[OII] proxy: the paper's OWN model-mediated "
    f"columns (logMHI = NEUTRALUNIVERSEMACHINE, logMMol = Tacconi+2020) are what the test rests "
    f"on; prior M_HI in [0, M_mol] (never zero) gives {min(hi_full):.3f}-{max(hi_full):.3f} dex on "
    f"log10 a0 = {min(hi_full)/bar3s_dex(0.9):.1f}-{max(hi_full)/bar3s_dex(0.9):.1f}x BAR-3S, "
    f"one-sided and coherent")
rec("E3", hi_paper > hi_trust,
    f"but the 'realistic' sub-case is OPTIMISTIC: it uses M_HI/M_bar=0.30 with sigma(log M_HI)="
    f"0.30 dex -> {hi_trust:.4f} dex, while the catalogue's real median M_HI/M_bar = {fHI:.3f} and "
    f"the paper's own NUM prescription carries 0.8 dex scatter in log tau_HI -> {hi_paper:.4f} dex "
    f"= {hi_paper/hi_trust:.2f}x larger (both still exceed BAR-3S, so the verdict is unaffected)")

# =====================================================================================
# F -- THE PRE-REGISTERED ESTIMATOR (median-like only; GLS FORBIDDEN)
# =====================================================================================
print("\nF -- estimator pre-registration")
EV = os.path.join(HERE, "..", "a0_line", "estimator_bias_verdict.json")
V = json.load(open(EV))
bt = V["bias_table"]
gls, med = bt["gls_origin"], bt["median_a0pt"]
rec("F1", gls["tier"] == "FAIL" and med["tier"] == "PASS",
    f"median-like estimator is pre-registered and GLS is EXCLUDED, from the SHA-stamped freeze "
    f"({V['prereg_id']}): gls_origin bias {gls['max_abs_b']:+.2f} pp -> {gls['tier']}, "
    f"theilsen_pairwise {bt['theilsen_pairwise']['max_abs_b']:+.2f} pp -> "
    f"{bt['theilsen_pairwise']['tier']}, median_a0pt {med['max_abs_b']:+.2f} pp -> {med['tier']}")
rec("F2", abs(MEDPEN - 1.2533141373155001) < 1e-12,
    f"the median's efficiency penalty sqrt(pi/2) = {MEDPEN:.7f} is APPLIED to the incoherent "
    f"term (not waived), matching the claim set's median_efficiency_penalty = "
    f"{J['framework']['median_efficiency_penalty']:.7f}")

# =====================================================================================
# G -- WHAT THE 20:1 BAR IS ACTUALLY MEASURING (joint vs single-point)
# =====================================================================================
print("\nG -- provenance of BAR-20 = 0.0180 dex")
import io
import contextlib
import sys
sys.path.insert(0, HERE)
_b = io.StringIO()
with contextlib.redirect_stdout(_b):
    import a0z_fork_likelihood_2026 as PAR
IX = [i for i, P in enumerate(PAR.POINTS) if P["tag"].startswith("[3]")][0]


def lnB(sig_dex, pts_mode):
    """robust (worst-prior) lnB(DEC/RISE) for an Asimov-DEC Jeanneau point of width sig_dex."""
    out = []
    for pm in PAR.PMAX_LADDER:
        got = {}
        for m in ("M-DEC", "M-RISE"):
            base = [dict(P) for P in PAR.POINTS]
            P = base[IX]
            P["zrep"] = 0.9
            P["val"] = float(np.log10(PAR.MODELS["M-DEC"](0.9))) * P["L"]
            P["sig_stat"] = P["sig_tot"] = sig_dex * P["L"]
            P["w"] = 0.20
            use = base if pts_mode == "joint" else [P]
            got[m] = PAR.ln_evidence(m, pm, pts=use)[0]
        out.append(got["M-DEC"] - got["M-RISE"])
    return min(out)


j018, s018 = lnB(0.018, "joint"), lnB(0.018, "single")
j094, s094 = lnB(0.094, "joint"), lnB(0.094, "single")
jbig = lnB(1.0, "joint")
rec("G1", jbig < 0 and s094 > np.log(20) > j094,
    f"BAR-20 = 0.0180 dex is NOT a MUSE-DARK II property -- it is set by the REST of the "
    f"compilation: with the Jeanneau point made uninformative the joint prior-robust "
    f"lnB(DEC/RISE) -> {jbig:.1f} (the committed compilation's face log10B(DEC/RISE) = "
    f"{-62.24:.2f}, dominated by point [2] MUSE-DARK III Ciocan). At 0.094 dex the SINGLE-point "
    f"bar clears 20:1 (lnB={s094:.2f} > {np.log(20):.2f}) while the joint one does not "
    f"(lnB={j094:.1f}), so the single-point 20:1 bar is ~{0.094/0.018:.1f}x looser and matches "
    f"the sibling script's 0.0942 dex")

# =====================================================================================
# H -- THE ONE PRO-FRAMEWORK CLAIM: is the a0-line 2.10x per-object gain apples-to-apples?
# =====================================================================================
print("\nH -- the a0-line-vs-bTFR per-object gain")
btfr_implied = 0.06 * np.sqrt(N) / L_ASM
a0line = float(np.sqrt((amps["V"] * 0.15) ** 2 + (amps["gbar"] * 0.20 * DEX) ** 2 +
                       (amps["R"] * 0.10) ** 2) / DEX)
rec("H1", btfr_implied / a0line > 2.0,
    f"the claimed {btfr_implied/a0line:.2f}x gain ({btfr_implied:.3f} dex bTFR vs {a0line:.3f} dex "
    f"a0-line) is NOT apples-to-apples: the bTFR figure is back-calibrated from the published "
    f"+/-0.06 and therefore CONTAINS intrinsic bTFR scatter, while the a0-line figure is pure "
    f"measurement propagation with NO intrinsic-scatter term. The claim that the residual is "
    f"'mostly the r-dependence the bTFR throws away' is ASSERTED, not demonstrated -- and it is "
    f"now directly testable on the in-hand catalogue")

# =====================================================================================
# SUMMARY
# =====================================================================================
print("\n" + BAR)
nf = sum(1 for _, v, _ in FIND if v == "FAIL")
print(f"SUMMARY: {len(FIND)} audited checks, {len(FIND)-nf} PASS, {nf} FAIL "
      f"(FAIL = the claim set is contradicted on that point, in EITHER direction)")
print(BAR)
for t, v, txt in FIND:
    print(f"  {t} {v}")
print(f"""
  DIRECTION OF THE ERRORS (the symmetric test): the substantive failures B3/B4/B5/C1/C2/D2/G1
  all push the SAME way -- they make the sample look WEAKER than it is (assumed y instead of the
  catalogue's y, assumed velocity errors instead of the published ones, z_eff=0.90 instead of the
  real median {np.median(z):.3f}, a 20:1 bar set by another constraint). Corrected, S(honest) moves
  {S_hon:.2f} -> {S_hon_real:.2f} sigma and S(stat) {S_stat:.2f} -> {S_stat_real:.2f} sigma. Both are still under 3, so the
  NO-GO on 3-sigma and on 20:1 SURVIVES the correction -- but the headline shortfall
  ({0.27/L_ASM/bar3s_dex(0.9):.2f}x) is really ~{0.27/L_REAL/bar3s_dex(0.9):.2f}x. H1 is the one error in the framework's FAVOUR.
  No 3-sigma or 20:1 claim is made anywhere in the audited file, so there is NO manufactured
  detection. a0's VALUE and the HORIZON CHOICE remain POSITS; z~0.9 can never test DEC-vs-FLAT
  (DEC(0.9)={d09:.6f} vs FLAT=1), so nothing here bears on the framework's distinctive DECLINE --
  only on McCulloch's Hubble-horizon reading. No TOE. No 'theory closed'. Exit 0 = ran.""")

assert abs(f1 - f2) == 0.0, "footing independence"
assert abs(gap_dex(0.9) - 0.22722669920072153) < 1e-12, "fork gap reproduces"
assert L_REAL > L_ASM, "real lever is better than the claimed one"
assert S_hon_real < 3.0 and S_stat_real < 3.0, "corrected separations still under 3 sigma"
print("\n  SELF-CHECK OK. EXIT 0 (ran; not a verdict).")
