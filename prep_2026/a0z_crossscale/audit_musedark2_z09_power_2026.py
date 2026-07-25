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

VERDICT VOCABULARY (three states, so nothing is mislabelled):
    CLAIM-OK           the audited claim reproduces / survives independent recomputation
    CLAIM-CONTRADICTED the audited claim is wrong on that point (in EITHER direction)
    EVIDENCE           an established fact used by a later verdict, not itself a verdict

A manufactured DETECTION and a manufactured DEFICIT are penalized EQUALLY.  Both are
searched for.  Every state below is an f-string of a COMPUTED comparison; no verdict string
is typed in by hand.  Exit 0 = ran, NOT a verdict.
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
FIND = []                              # (id, state, text) -- all computed


def rec(tag, claim_ok, text, evidence=False):
    """claim_ok=True -> CLAIM-OK; False -> CLAIM-CONTRADICTED; evidence=True -> EVIDENCE."""
    st = "EVIDENCE" if evidence else ("CLAIM-OK" if claim_ok else "CLAIM-CONTRADICTED")
    FIND.append((tag, st, text))
    print(f"  [{tag}] {st} -- {text}")


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
    f"published-integrated separations reproduce ON THE CLAIM'S OWN INPUTS: "
    f"S(stat +/-0.06)={S_stat:.3f} sigma, S(honest +/-0.27)={S_hon:.3f} sigma -- neither reaches 3")
amps = dict(V=4 * (Y_ASM + 1), gobs=2 * (Y_ASM + 1), gbar=2 * Y_ASM + 1,
            R=2 * Y_ASM, mu=Y_ASM + 1)
rec("A4", all(abs(amps[k] - J["framework"][f"amp_{k}" if k != "mu" else "amp_mu_exact"]) < 1e-9
              for k in amps),
    f"amplifications reproduce at y={Y_ASM:.4f}: V={amps['V']:.4f} gobs={amps['gobs']:.4f} "
    f"gbar={amps['gbar']:.4f} R={amps['R']:.4f} mu={amps['mu']:.4f} (mu is (y+1), NOT 1:1 -- "
    f"the against-interest correction is real)")
f1 = float(A0_CAN * R_dec(0.9)) / float(A0_CAN * R_dec(0.0))
f2 = float(A0_ALT * R_dec(0.9)) / float(A0_ALT * R_dec(0.0))
rec("A5", abs(f1 - f2) == 0.0,
    f"BOTH FOOTINGS identical for the LAW RATIO: a0(0.9)/a0(0) = {f1:.12f} (canonical "
    f"cH_Lambda/Z) = {f2:.12f} (alt cH0/Z), |diff| = {abs(f1-f2):.1e}")
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
rec("B1", True,
    f"catalogue has N={len(rows)} rows and ALL {len(need)} per-object columns populated on "
    f"every row: {', '.join(need)}", evidence=True)
book = np.array([np.log10(10 ** float(r["logM*"]) + 10 ** float(r["logMHI"]) +
                          10 ** float(r["logMMol"])) - float(r["logMBar"]) for r in rows])
rec("B2", True,
    f"catalogue is internally consistent (authenticity check): M_bar = M* + M_HI + M_mol to "
    f"max |resid| = {np.abs(book).max():.1e} dex on all {len(rows)} rows", evidence=True)
rec("B3", not (J["sample"]["per_object_table_published"] is False and len(full) == len(need)),
    f"*** BLOCKER *** the claim set records per_object_table_published=False and names 'the "
    f"per-object table' as closer #1 ('from the authors, or by re-running lensed GalPaK3D'), "
    f"but the table IS published (VizieR J/A+A/709/A120 = the paper's Table E1, CC-BY-4.0) and "
    f"has been committed in this repo since 2026-07-16; two SIBLING scripts in this very "
    f"directory already read it (jeanneau_perobject_horizon_fork_2026.py, "
    f"jeanneau_z09_dec_vs_rise_2026.py). 'Needs new data' is FALSE for the table itself")

# real sample facts vs the claimed ones
z = np.array([float(r["zR21"]) for r in rows])
mu = np.array([float(r["muR21"]) for r in rows])
lM = np.array([float(r["logM*"]) for r in rows])
sV18 = np.array([float(r["s_logV1_8"]) for r in rows])
sV20 = np.array([float(r["s_logV2_0"]) for r in rows])
print(f"\n  {'quantity':26} {'CLAIMED':>22} {'REAL (catalogue)':>26}")
print("  " + "-" * 76)
print(f"  {'z span':26} {'0.56-1.37':>22} "
      f"{f'{z.min():.4f}-{z.max():.4f} (med {np.median(z):.4f})':>26}")
print(f"  {'z p5-p95':26} {'(not quoted)':>22} "
      f"{f'{np.percentile(z,5):.4f}-{np.percentile(z,95):.4f}':>26}")
print(f"  {'magnification mu':26} {'1.4-12.4':>22} {f'{mu.min():.3f}-{mu.max():.3f}':>26}")
print(f"  {'log M*':26} {'8.1-10.3':>22} {f'{lM.min():.2f}-{lM.max():.2f}':>26}")
print(f"  {'sigma_V/V per object':26} {'SWEPT 5-30% (15% used)':>22} "
      f"{f'PUBLISHED: med {100*(10**np.median(sV20)-1):.2f}%':>26}")
p5, p95 = float(np.percentile(z, 5)), float(np.percentile(z, 95))
gmean = float(np.mean([gap_dex(v) for v in z]))
rec("B4a", abs(p5 - 0.56) < 0.03 and abs(p95 - 1.37) < 0.03,
    f"the quoted span 0.56-1.37 RECONCILES as a PERCENTILE range, not min-max: catalogue p5-p95 "
    f"= {p5:.4f}-{p95:.4f} matches it to <0.03 while min-max is {z.min():.4f}-{z.max():.4f} "
    f"(same for mu: quoted 1.4-12.4, real {mu.min():.2f}-{mu.max():.2f} with only "
    f"{(mu>12.4).sum()} objects above 12.4). No fabricated column, no misread abstract")
rec("B4b", abs(gap_dex(0.9) - gmean) < 0.01,
    f"the EFFECTIVE REDSHIFT is wrong, and in the pessimistic direction: the claim evaluates the "
    f"whole power calculation at z=0.90, but the sample's real median is {np.median(z):.4f} and "
    f"the sample-MEAN of the DEC-vs-RISE gap is {gmean:.5f} dex vs {gap_dex(0.9):.5f} at z=0.90 "
    f"-- {gmean/gap_dex(0.9):.3f}x more signal than the claim credits it with")
sr_pub = float(np.sqrt((amps["gbar"] * 0.20) ** 2 + (amps["V"] * np.median(sV20)) ** 2))
claim_quad = float(np.sqrt((amps["gbar"] * 0.20) ** 2 + (amps["V"] * 0.16 / DEX) ** 2))
rec("B5", claim_quad <= 0.435,
    f"the claim's own sentence 'N=95 already meets 0.435 dex/object using the paper's +/-0.2 dex "
    f"masses PLUS any velocity precision better than 16%' does NOT add up: at its own y that is "
    f"{amps['gbar']*0.20:.3f} (+) {amps['V']*0.16/DEX:.3f} = {claim_quad:.3f} dex > 0.435 in "
    f"quadrature. The CONCLUSION is right for a different reason: per-object velocity errors are "
    f"PUBLISHED (s_logV2_0, med {np.median(sV20):.4f} dex = {100*(10**np.median(sV20)-1):.2f}%, "
    f"not 16%), giving {sr_pub:.3f} dex/object -- so the 5-30% SWEEP was never needed")

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


KA = np.array([kpc_per_arcsec(v) for v in z])


def y_of_sample(a0, fac=2.0, col="logV2_0"):
    """y = g_bar/a0 per object, g_bar from inverting the framework's OWN kernel at g_obs."""
    R = fac * np.array([float(r["Reff"]) for r in rows]) * KA * KPC
    go = (10 ** np.array([float(r[col]) for r in rows]) * 1000.0) ** 2 / R
    gb = (-a0 + np.sqrt(a0 * a0 + 4 * go * go)) / 2.0
    return gb / a0


Y_CAN, Y_ALT = y_of_sample(A0_CAN), y_of_sample(A0_ALT)
Y18 = y_of_sample(A0_CAN, 1.8, "logV1_8")
ymed = float(np.median(Y_CAN))
L_REAL = 1.0 / (1.0 + 2.0 * ymed)
print(f"  y = g_bar/a0 on the 95 (canonical a0, v_c(2Re) at 2Re -- the paper's own bTFR "
      f"ordinate): q25 {np.percentile(Y_CAN,25):.4f}  MEDIAN {ymed:.4f}  "
      f"q75 {np.percentile(Y_CAN,75):.4f};  frac below 0.3 a0 = {(Y_CAN<0.3).mean():.3f}")
print(f"  radius-convention check: y median = {np.median(Y18):.4f} at 1.8Re/V1.8 vs "
      f"{ymed:.4f} at 2.0Re/V2.0 -> the conclusion is convention-insensitive")
print(f"  y median on ALT footing = {np.median(Y_ALT):.4f} (lever "
      f"{1/(1+2*np.median(Y_ALT)):.4f}) -- the FORK RATIO is footing-independent; "
      f"the LEVER is NOT, and both are carried")
rec("C1", L_REAL <= L_ASM,
    f"the claim UNDERSTATES its own lever: claimed y={Y_ASM:.4f} -> L={L_ASM:.4f} (labelled "
    f"'this sample's own y', but it is the geometric mean of a POSITED [0.3,1.0] bracket); "
    f"real median y={ymed:.4f} -> L={L_REAL:.4f} = {L_REAL/L_ASM:.3f}x BETTER. On the frozen "
    f"deep cut (y<0.5, N={(Y_CAN<0.5).sum()}) the real median is y="
    f"{np.median(Y_CAN[Y_CAN<0.5]):.4f} -> L={1/(1+2*np.median(Y_CAN[Y_CAN<0.5])):.4f}")
zmed = float(np.median(z))
S_hon_real = gap_dex(zmed) / (0.27 / L_REAL)
S_stat_real = gap_dex(zmed) / (0.06 / L_REAL)
rec("C2", abs(S_hon_real - S_hon) < 0.05,
    f"corrected separations (real lever L={L_REAL:.4f}, real median z={zmed:.4f}, gap "
    f"{gap_dex(zmed):.5f} dex): S(honest)={S_hon_real:.3f} sigma (claim {S_hon:.3f}), "
    f"S(stat)={S_stat_real:.3f} sigma (claim {S_stat:.3f}) -- the claim is "
    f"{S_hon_real/S_hon:.2f}x too PESSIMISTIC. The NO-GO SURVIVES the correction "
    f"({S_hon_real:.2f} < 3), so this is a magnitude error, not a verdict flip")
print(f"  amplifications at the real median y: V={4*(ymed+1):.4f} (claimed {amps['V']:.4f}), "
      f"gbar={2*ymed+1:.4f} (claimed {amps['gbar']:.4f}), mu={ymed+1:.4f} "
      f"(claimed {amps['mu']:.4f}) -- every channel is SMALLER, i.e. every error propagates "
      f"LESS than the claim assumed")

# =====================================================================================
# D -- COHERENT vs INCOHERENT BOOKKEEPING (a call that clears a bar by averaging a
#      coherent term is invalid).  Re-derive the covariance structure independently.
# =====================================================================================
print("\nD -- coherent terms must NOT average as 1/sqrt(N); cluster block re-derived")
N = len(rows)
sr, sc = 0.584, 0.5658
zs = 0.56 + (1.37 - 0.56) * ((np.arange(N) + 0.5) / N)
Dg = np.array([gap_dex(v) for v in zs])
C_inc = np.eye(N) * (MEDPEN * sr) ** 2
S_inc_only = float(np.sqrt(Dg @ np.linalg.inv(C_inc) @ Dg))
S_with_coh = float(np.sqrt(Dg @ np.linalg.inv(C_inc + sc ** 2) @ Dg))
rec("D1", S_inc_only > 3.0 and S_with_coh < 0.5 * S_inc_only,
    f"the rank-1 coherent block does NOT average down (correctly held out of 1/sqrt(N)): "
    f"S={S_inc_only:.2f} sigma with sigma_c=0 but S={S_with_coh:.2f} sigma once "
    f"sigma_c={sc:.4f} dex is added -- it SATURATES at gap/sigma_c = "
    f"{gap_dex(0.9)/sc:.3f} sigma for ANY N, exactly as claimed")
from collections import Counter
cnt = Counter(r["Cluster"] for r in rows)
wts = np.array([v / N for v in cnt.values()])
red = float(np.sqrt((wts ** 2).sum()))
rec("D2", abs(red - 0.5) < 0.02,
    f"cluster block MIS-sized (against the claim's own interest, i.e. flattering the "
    f"framework): claimed {J['sample']['n_clusters']} equal clusters -> averaging "
    f"1/sqrt(4)=0.5000; the real catalogue has {len(cnt)} lines of sight {dict(cnt)} -> "
    f"effective N_cl = {1/(wts**2).sum():.2f} (A370 alone is "
    f"{max(cnt.values())/N:.0%} of the sample), averaging {red:.4f}, so the coherent "
    f"magnification term is {red/0.5:.3f}x LARGER than quoted")

# =====================================================================================
# E -- THE HI / GAS-MASS WALL AND ITS SIGN (must bias a0 HIGH = toward RISE)
# =====================================================================================
print("\nE -- gas-mass wall: no proxy substituted, and the sign runs AGAINST the framework")
MHI = np.array([10 ** float(r["logMHI"]) for r in rows])
MMOL = np.array([10 ** float(r["logMMol"]) for r in rows])
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
    f"gas wall carried at strength and NOT via an SFR/[OII] proxy substituted by the analysis: "
    f"the test rests on the PAPER'S OWN model-mediated columns (logMHI = "
    f"NEUTRALUNIVERSEMACHINE, logMMol = Tacconi+2020 scaling). Median f_gas = "
    f"{float(np.median((MHI+MMOL)/MB)):.3f} of M_bar is prescription, not measurement. Prior "
    f"M_HI in [0, M_mol] (never zero) gives {min(hi_full):.3f}-{max(hi_full):.3f} dex on "
    f"log10 a0 = {min(hi_full)/bar3s_dex(0.9):.1f}-{max(hi_full)/bar3s_dex(0.9):.1f}x BAR-3S, "
    f"one-sided and coherent")
rec("E3", hi_paper <= hi_trust,
    f"the 'realistic' HI sub-case is OPTIMISTIC (flatters the framework): it uses "
    f"M_HI/M_bar=0.30 with sigma(log M_HI)=0.30 dex -> {hi_trust:.4f} dex, while the "
    f"catalogue's real median M_HI/M_bar = {fHI:.3f} and the paper's own NUM prescription "
    f"carries 0.8 dex scatter in log tau_HI -> {hi_paper:.4f} dex = {hi_paper/hi_trust:.2f}x "
    f"larger (both still exceed BAR-3S, so the NO-GO verdict is unaffected)")

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
    f"gls_lowy {bt['gls_lowy']['max_abs_b']:+.2f} pp -> {bt['gls_lowy']['tier']}, "
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
rec("G1", not (jbig < 0 and s094 > np.log(20) > j094),
    f"BAR-20 = 0.0180 dex is NOT a MUSE-DARK II property -- it is set by the REST of the "
    f"compilation: with the Jeanneau point made uninformative the joint prior-robust "
    f"lnB(DEC/RISE) is already {jbig:.1f} (the committed compilation is dominated by point [2], "
    f"MUSE-DARK III Ciocan, which pulls toward RISE). At 0.094 dex the SINGLE-point bar clears "
    f"20:1 (lnB={s094:.2f} > {np.log(20):.2f}) while the joint one does not (lnB={j094:.1f}), so "
    f"the honest single-point 20:1 bar is ~{0.094/0.018:.1f}x LOOSER than quoted and matches the "
    f"sibling script's 0.0942 dex. The claimed '31x too wide for 20:1' is really ~"
    f"{(0.27/L_REAL)/0.0942:.1f}x on the real lever")

# =====================================================================================
# H -- THE ONE PRO-FRAMEWORK CLAIM: is the a0-line 2.10x per-object gain apples-to-apples?
# =====================================================================================
print("\nH -- the a0-line-vs-bTFR per-object gain (the claim set's one PRO-framework number)")
btfr_implied = 0.06 * np.sqrt(N) / L_ASM
a0line = float(np.sqrt((amps["V"] * 0.15) ** 2 + (amps["gbar"] * 0.20 * DEX) ** 2 +
                       (amps["R"] * 0.10) ** 2) / DEX)
rec("H1", btfr_implied / a0line <= 1.2,
    f"the claimed {btfr_implied/a0line:.2f}x gain ({btfr_implied:.3f} dex bTFR vs {a0line:.3f} dex "
    f"a0-line) is NOT apples-to-apples: the bTFR figure is back-calibrated from the published "
    f"+/-0.06 and therefore CONTAINS intrinsic bTFR scatter, while the a0-line figure is pure "
    f"measurement propagation with NO intrinsic-scatter term. The claim that the residual is "
    f"'mostly the r-dependence the bTFR throws away' is ASSERTED, not demonstrated -- and note "
    f"the a0-line route ALSO needs a resolved g_bar(r), which 70-85%-prescription-gas M_bar "
    f"cannot supply")

# =====================================================================================
# I -- THE SEPARATIONS THE CLAIM SET FORECASTS, RECOMPUTED ON THE PUBLISHED PER-OBJECT
#      ERRORS AND THE REAL z DISTRIBUTION (the claim's 0.70 / 1.05 / 2.24 sigma row)
# =====================================================================================
print("\nI -- the per-object forecasts, redone with PUBLISHED errors instead of assumed ones")
AV_R, AM_R = 4 * (ymed + 1), 2 * ymed + 1
sig_r_pub = float(np.sqrt((AM_R * 0.20) ** 2 + (AV_R * np.median(sV20)) ** 2))
Dz = np.array([gap_dex(v) for v in z])
S_abs_pub = float(np.sqrt(np.sum(Dz ** 2)) / (MEDPEN * sig_r_pub))
S_tr_pub = float(np.sqrt(np.sum((Dz - Dz.mean()) ** 2)) / (MEDPEN * sig_r_pub))
print(f"  per-object sigma on log10 a0 from PUBLISHED columns only: mass "
      f"{AM_R*0.20:.4f} (+) velocity {AV_R*float(np.median(sV20)):.4f} = {sig_r_pub:.4f} dex")
print(f"  real-z gap: mean {Dz.mean():.5f}  sd {Dz.std(ddof=1):.5f}  "
      f"(at z=0.90 the claim used {gap_dex(0.9):.5f})")
rec("I1", abs(S_abs_pub - J["separations"]["per_object_absolute_perfect_syst_sigma"]) < 0.3,
    f"the 'perfect coherent systematics' counterfactual is UNDERSTATED "
    f"{S_abs_pub/J['separations']['per_object_absolute_perfect_syst_sigma']:.2f}x: on "
    f"published per-object errors and the real z list it is {S_abs_pub:.2f} sigma, not the "
    f"claimed {J['separations']['per_object_absolute_perfect_syst_sigma']:.2f} -- so the "
    f"N-requirement '171 objects (absolute)' is really "
    f"{N*(3.0/S_abs_pub)**2:.0f} (the claim inflates it {171/(N*(3.0/S_abs_pub)**2):.1f}x)")
rec("I2", abs(S_tr_pub - J["separations"]["per_object_trend_sigma"]) < 0.3,
    f"the coherent-immune TREND route is likewise UNDERSTATED "
    f"{S_tr_pub/J['separations']['per_object_trend_sigma']:.2f}x: {S_tr_pub:.2f} sigma on "
    f"published errors + real z (claim {J['separations']['per_object_trend_sigma']:.2f}); "
    f"after the w=0.20 drift absorption {0.771*S_tr_pub:.2f} sigma; N for 3 sigma = "
    f"{N*(3.0/(0.771*S_tr_pub))**2:.0f}, not the claimed 1730-4198. STILL UNDER 3 SIGMA, so "
    f"again a magnitude error and not a verdict flip")
# the drift template vs the fork template: is the trend route really only 23% absorbable?
T = np.log10(1 + z)
slope = float(np.polyfit(T, Dz, 1)[0])
rec("I3", slope / 1.50 <= 0.20,
    f"the trend route's immunity is EXPOSURE-CONDITIONAL, and the favourable headline uses the "
    f"exposure the sibling script argues is wrong: the fork's own slope is d(gap)/dlog10(1+z) = "
    f"{slope:.3f}, so an LCDM apparent drift (1+z)^p mimics it at p = {slope:.2f}/w. At the "
    f"committed w=0.20 that needs p={slope/0.20:.2f} vs a 1.50 ceiling (absorption "
    f"{0.20*1.50/slope:.0%}) -- but w=0.20 was assigned to a ZERO-POINT at one z, and a SLOPE "
    f"across z is exactly the currency the committed likelihood gives w=1.00, where absorption "
    f"is {min(1.0, 1.00*1.50/slope):.0%} and the route DIES. The claim reports the sweep but "
    f"headlines the favourable end")

# =====================================================================================
# SUMMARY
# =====================================================================================
print("\n" + BAR)
nc = sum(1 for _, v, _ in FIND if v == "CLAIM-CONTRADICTED")
nk = sum(1 for _, v, _ in FIND if v == "CLAIM-OK")
ne = sum(1 for _, v, _ in FIND if v == "EVIDENCE")
print(f"SUMMARY: {len(FIND)} audited items -- {nk} CLAIM-OK, {nc} CLAIM-CONTRADICTED, "
      f"{ne} EVIDENCE")
print(BAR)
for t, v, txt in FIND:
    print(f"  {t:3} {v}")
print(f"""
  DIRECTION OF THE ERRORS (the symmetric test, both ways):
   * TOWARD A MANUFACTURED DEFICIT (the dominant, load-bearing set): B3 (the per-object table
     is public AND already committed here -- 'needs new data' is false for the table), B4b (the
     effective z: 0.90 used vs real median {np.median(z):.3f}), B5 (velocity errors assumed and
     swept when they are published at {100*(10**np.median(sV20)-1):.1f}%), C1/C2 (a POSITED y
     bracket instead of the catalogue's own y -> lever understated {L_REAL/L_ASM:.2f}x),
     G1 (the 20:1 bar quoted is the JOINT compilation's, not this sample's), I1/I2 (the
     per-object forecasts understated {S_abs_pub/J['separations']['per_object_absolute_perfect_syst_sigma']:.1f}x /
     {S_tr_pub/J['separations']['per_object_trend_sigma']:.1f}x).
   * TOWARD FLATTERING THE FRAMEWORK: D2 (4 equal clusters assumed; really {len(cnt)} lines of
     sight, N_eff {1/(wts**2).sum():.2f}, coherent mu term {red/0.5:.2f}x larger), E3 (the
     'realistic' HI sub-case {hi_paper/hi_trust:.2f}x optimistic vs the paper's own 0.8 dex NUM
     scatter), H1 (the a0-line 2.10x per-object gain is not apples-to-apples), I3 (the
     favourable trend-route headline uses w=0.20 where a slope-in-z observable warrants w=1.00).
   NET: corrected, S(honest) moves {S_hon:.2f} -> {S_hon_real:.2f} sigma and S(stat)
   {S_stat:.2f} -> {S_stat_real:.2f} sigma. BOTH REMAIN UNDER 3, and the coherent floor
   (gas {amps['gbar']*0.20/L_REAL*L_REAL:.3f}, local reference, magnification) still exceeds
   BAR-3S = {bar3s_dex(zmed):.4f} dex at the real median z by {0.20/L_REAL/bar3s_dex(zmed):.1f}x
   on the gas term alone and does NOT average down. So the NO-GO on 3-sigma and on 20:1
   SURVIVES every correction -- the headline shortfall is just ~{0.27/L_REAL/bar3s_dex(zmed):.1f}x
   rather than the claimed 8.27x.
  NO MANUFACTURED DETECTION: no 3-sigma or 20:1 claim is made anywhere in the audited file, and
  every per-object figure in it is labelled a forecast.
  a0's VALUE and the HORIZON CHOICE remain POSITS; z~0.9 can never test DEC-vs-FLAT
  (DEC(0.9)={d09:.6f} vs FLAT=1), so nothing here bears on the framework's distinctive DECLINE --
  only on McCulloch's Hubble-horizon reading. No TOE. No 'theory closed'. No closed doors.
  Exit 0 = ran, NOT a verdict.""")

assert abs(f1 - f2) == 0.0, "footing independence of the law ratio"
assert abs(gap_dex(0.9) - 0.22722669920072153) < 1e-12, "fork gap reproduces"
assert L_REAL > L_ASM, "real lever is better than the claimed one"
assert S_hon_real < 3.0 and S_stat_real < 3.0, "corrected separations still under 3 sigma"
assert S_tr_pub < 3.0 and 0.771 * S_tr_pub < 3.0, "trend route still under 3 sigma"
assert len(rows) == 95 and len(full) == len(need), "the per-object catalogue is complete"
print("\n  SELF-CHECK OK. EXIT 0 (ran; not a verdict).")
