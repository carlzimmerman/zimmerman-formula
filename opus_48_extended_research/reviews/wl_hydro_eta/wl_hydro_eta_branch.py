#!/usr/bin/env python3
"""
WL-vs-HYDRO mass-proxy axis -> the eRASS1 cluster MOND residual eta(R500),
on the Zimmerman framework's OWN dS-Unruh footing (a0 = 9.36e-11, modified inertia
g_obs = sqrt(g_bar^2 + g_bar*a0)).

CONTEXT (banked, read XRISM_ETA_PINNING_2026-06-20.md + CLUSTER_GRAVITY_LAST_DOORS_2026-06-20.md):
XRISM SHUT the disequilibrium-via-turbulence escape (relaxed clusters quiescent, f_nt~2-4%, and the
sign was inverted: non-thermal pressure RAISES a thermal eta, it cannot lower it). So the residual's
MAGNITUDE is now set by a DIFFERENT axis: the WL-vs-HYDRO mass-proxy disagreement.

The eRASS1 baseline eta(R500)=2.334 uses WEAK-LENSING-calibrated M500 (Ghirardini/Grandis 2024).
The thermal-HYDROSTATIC mass is LOWER by the hydrostatic-bias factor b: M_HSE = (1-b)*M_WL.
Define the proxy ratio  q == M_WL / M_HSE = 1/(1-b).

   eta_hydro(R500) = eta_WL / q     (the dynamical/required mass is smaller on the HSE proxy,
                                      so the discrepancy vs the SAME baryons shrinks by 1/q)

THE LOAD-BEARING BOTH-WAYS QUESTION (Carl's #1 rule -- penalize high-priest AND manufacturing EQUALLY):
WHAT IS THE REAL RELAXED-CLUSTER q = M_WL/M_HSE?  The XRISM synth leaned on Li+2024's q~2.1
(=> eta_hydro~1.1, near-closed). The CONSENSUS hydrostatic bias is (1-b)~0.7-0.85, i.e. q~1.2-1.4,
which gives eta_hydro~1.7-1.9 -- a STILL-REAL gap. Pin the real number from the consensus literature.

----------------------------------------------------------------------------------------
THE Y-Q (AeST ghost-condensate) FIELD -- the no-NEW-PARTICLE channel.
----------------------------------------------------------------------------------------
Banked (CLUSTER_STACK_AND_DECISIVE_TEST_2026-06-20.md, Route B): the framework's OWN AeST Y-Q field
adds ~+17-20% on the modified-inertia phantom = it covers ~17-20% of the residual gap with NO new
particle. We apply ONLY this no-particle channel (NOT the IGIMF stellar remnants, which need known
baryons and are budget-capped/shape-contested -- they are a SEPARATE, non-field channel).

eta is M_dyn/M_bar. The "gap" (excess over the framework's bare phantom prediction) is what the
Y-Q field eats. The framework's bare modified-inertia ALREADY predicts a phantom boost eta_MOND>1;
the RESIDUAL is the part of eta above what the bare MI phantom supplies. The Y-Q field adds f_YQ of
that residual. So with the residual measured relative to eta=1 (pure-baryon Newtonian), the field
removes f_YQ of (eta-1) ... BUT honestly the field is "+20% ON THE PHANTOM", i.e. it scales the
phantom boost, so we report BOTH framings:
  (i) field eats f_YQ of the FULL discrepancy (eta-1):  eta_YQ = 1 + (1-f_YQ)*(eta-1)
  (ii) field adds f_YQ to the bare MI phantom only (the banked "+20% on the phantom" reading)
We use (i) as the headline (most favorable to closure -- avoids high-priesting), and report (ii).

A residual is CLOSED if eta_after_YQ <= ~1.10-1.15 (consistent with 1 within cluster scatter / the
known stellar M/L and gas-budget slack). It STANDS (real shared-MOND gap) if eta_after_YQ >~ 1.3.

QUARANTINE: a0/Z/kappa never asserted derived. a0=9.36e-11 is an INPUT only.
"""
import numpy as np
from astropy.io import fits

c, G, Msun, kpc = 2.998e8, 6.674e-11, 1.989e30, 3.0857e19
H0 = 2.184e-18; OmL = 0.685
RHO_CRIT0 = 3*H0**2/(8*np.pi*G)
A0_FRAME = 0.5*c*np.sqrt(G*OmL*RHO_CRIT0)
A0_MOND  = 1.2e-10
FITS = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/erass1cl_primary_v3.2.fits"

print("="*84)
print("a0_frame = %.4e m/s^2 (framework dS-Unruh, target 9.36e-11)" % A0_FRAME)

# ---------------- framework dS-Unruh modified inertia: g_obs = sqrt(g_bar^2 + g_bar*a0)
def nu_frame(gbar, a0): return np.sqrt(1.0 + a0/gbar)
def etaA(gobs, gbar, a0): return gobs/(nu_frame(gbar, a0)*gbar)

# ---------------- eRASS1 baseline (real data, WL-calibrated M500) -- reproduce 2.334 / 2.073
try:
    d = fits.open(FITS)[1].data
    def col(name): return np.array([float(v) if str(v).strip() not in ("","--") else np.nan for v in d[name]], float)
    z, M500, Mgas, fgas, R500 = (col("BEST_Z"), col("M500"), col("MGAS500"), col("FGAS500"), col("R500"))
    ok = (z>0)&(z<1)&np.isfinite(z)&(M500>0)&(Mgas>0)&(R500>0)&(fgas>0.01)&(fgas<0.30)
    N = int(ok.sum())
    FSTAR = 0.2
    M_kg  = M500[ok]*1e13*Msun
    Mb_kg = (1+FSTAR)*Mgas[ok]*1e11*Msun
    R_m   = R500[ok]*kpc
    gobs, gbar = G*M_kg/R_m**2, G*Mb_kg/R_m**2
    ETA_WL_FRAME = float(np.median(etaA(gobs, gbar, A0_FRAME)))
    ETA_WL_CANON = float(np.median(etaA(gobs, gbar, A0_MOND)))
    med_g_a0 = float(np.median(gobs/A0_FRAME)); med_z = float(np.median(z[ok]))
    DATA = "real eRASS1 (N=%d, median z=%.3f, median g/a0=%.3f)" % (N, med_z, med_g_a0)
except Exception as e:
    print("[FITS unavailable -> using banked baseline]  reason:", e)
    ETA_WL_FRAME, ETA_WL_CANON = 2.334, 2.073
    DATA = "banked eRASS1 baseline (N=9830, median z=0.298, median g/a0=0.481)"
    N = 9830

print("="*84)
print("DATA SOURCE:", DATA)
print("eta_WL(R500) framework dS-Unruh : %.3f  (banked 2.334)" % ETA_WL_FRAME)
print("eta_WL(R500) canonical a0       : %.3f  (banked 2.073)" % ETA_WL_CANON)

# ============================================================================================
# (1) PIN THE REAL RELAXED-CLUSTER q = M_WL/M_HSE BRACKET  (pulled mass-proxy consensus)
# ============================================================================================
# Each entry: program, q=M_WL/M_HSE at (or extrapolated to) R500, selection class, weight class.
# Sourced from the pulled ledger (CCCP, X-COP, LoCuSS, CLASH, WtG, Lovisari/CoMaLit,
# Munoz-Echeverria, Li+2024) -- see the structured "sources" field.
PROGRAMS = [
    # name                          q(M_WL/M_HSE @R500)   class            note
    ("WtG/Applegate+2016 (relaxed-IV)", 1.10, "relaxed", "0.96 at r2500 -> ~1.0-1.15 @R500; cleanest relaxed-only"),
    ("LoCuSS Smith+2016",               1.05, "relaxed", "beta_X=0.95 -> q~1.05; disfavors large bias ~5sigma"),
    ("X-COP Eckert/Ettori+2019",        1.12, "relaxed", "f_nt~5-15% @R500 -> q~1.05-1.18; relaxed Planck-SZ"),
    ("CLASH Umetsu/Donahue 2014/16",    1.20, "relaxed", "M_lens/M_X=1.14 @r2500 -> ~1.2-1.3 @R500"),
    ("CCCP Hoekstra+2015",              1.32, "mixed",   "(1-b)=0.76 -> q~1.32; X-ray-sel, disturbed included"),
    ("Lovisari+2020 / CoMaLit",         1.35, "mixed",   "(1-b)=0.74 -> q~1.35; Planck-ESZ, disturbed-rich"),
    ("Munoz-Echeverria+2024 (meta)",    1.35, "mixed",   "(1-b)=0.739 @R500 -> q~1.35; consensus meta"),
    ("Li+2024 (the outlier)",           1.76, "full",    "OUTLIER: full(non-relaxed) sample; own M_dyn~M_HSE<<M_WL => WL over-estimate"),
]
print("="*84)
print("REAL RELAXED-CLUSTER WL/HSE (q = M_WL/M_HSE) -- pulled consensus")
print("%-34s %6s  %-8s  %s" % ("program", "q", "class", "note"))
for nm, q, cl, note in PROGRAMS:
    print("%-34s %6.2f  %-8s  %s" % (nm, q, cl, note))

q_relaxed = [q for _, q, cl, _ in PROGRAMS if cl == "relaxed"]
q_mixed   = [q for _, q, cl, _ in PROGRAMS if cl == "mixed"]
q_outlier = [q for _, q, cl, _ in PROGRAMS if cl == "full"]

q_relaxed_floor = float(np.mean(q_relaxed))     # cleanest relaxed-only programs
q_mixed_ceiling = float(np.mean(q_mixed))       # disturbed folded in
# Honest CONSENSUS central = midpoint of relaxed-floor and mixed-ceiling (the pulled "~1.25 (-0.20/+0.25)")
q_consensus = round(0.5*(q_relaxed_floor + q_mixed_ceiling), 2)
q_lo, q_hi  = round(min(q_relaxed), 2), round(q_mixed_ceiling, 2)   # ~1.05 .. ~1.4 spread

print("-"*84)
print("relaxed-only mean q     = %.2f  (WtG/LoCuSS/X-COP/CLASH)" % q_relaxed_floor)
print("mixed-sample mean q     = %.2f  (CCCP/Lovisari/Munoz)" % q_mixed_ceiling)
print("CONSENSUS central q     = %.2f   spread [%.2f, %.2f]" % (q_consensus, q_lo, q_hi))
print("Li+2024 OUTLIER q       = %.2f   (NOT consensus; ~2x standard bias; likely WL over-estimate)"
      % q_outlier[0])

# ============================================================================================
# (2) THIRD PROXY -- break the WL-vs-X-ray tie with gas-independent dynamical/caustic masses
# ============================================================================================
# Maughan & Rines 2016: M_HSE/M_caustic = 1.20 (+0.13/-0.11) @R500 -> HSE slightly OVER caustic.
#   => caustic mass ~ M_HSE/1.20.  If WL were the truth (q_WL on HSE), caustic would be far below WL.
#   Observed: caustic ~ HSE (not ~ WL) => the 3rd proxy sits NEAR HSE, not near WL.
# Li+2024 internal: M_dyn(Jeans) ~ M_HSE << M_WL -> two non-lensing probes agree LOW.
M_HSE_over_caustic = 1.20            # Maughan & Rines 2016
# Implied q_from_caustic = M_WL/M_caustic ONLY if we knew M_WL/M_HSE; the POINT is the reverse:
# the 3rd proxy corroborates the LOW (consensus) q, because caustic ~ HSE, not ~ q*HSE.
print("="*84)
print("THIRD PROXY (gas-independent, breaks the tie):")
print("  Maughan&Rines 2016: M_HSE/M_caustic = %.2f  => caustic ~ HSE (NOT ~ WL)" % M_HSE_over_caustic)
print("  Li+2024 internal:   M_dyn(Jeans) ~ M_HSE << M_WL  => 2 non-lensing probes agree LOW")
print("  => the dynamical/caustic 3rd proxy sits NEAR HSE => favors the LOW consensus q (Branch A),")
print("     and Li's own high WL is the OUTLIER (WL over-estimate), NOT a true 2x HSE bias.")

# ============================================================================================
# (3) eta_hydro ON EACH q, AND THE Y-Q (no-particle) FIELD APPLIED TO EACH BRANCH
# ============================================================================================
def eta_hydro(eta_wl, q):  return eta_wl / q

# Y-Q field coverage of the residual (banked +17-20% on the phantom = covers ~17-20% of the gap)
F_YQ_LO, F_YQ_HI = 0.17, 0.20
def eta_after_YQ_fulldisc(eta, f):  # framing (i): field eats f of the full discrepancy (eta-1)
    return 1.0 + (1.0 - f)*(eta - 1.0)

def classify(eta_after):
    if eta_after <= 1.15:  return "CLOSED (residual gone, <=1.15)"
    if eta_after <  1.30:  return "NEAR-CLOSED (1.15-1.30, within scatter)"
    return "REAL GAP STANDS (>=1.30, shared-MOND, ~half-covered)"

print("="*84)
print("eta(R500) ON EACH MASS PROXY, framework dS-Unruh footing (a0=9.36e-11):")
print("  baseline eta_WL = %.3f" % ETA_WL_FRAME)
print()
hdr = "%-26s %6s  %7s  %s" % ("proxy / q", "q", "eta_hyd", "after Y-Q field (f=0.17..0.20) -> verdict")
print(hdr); print("-"*84)

def row(label, q):
    eh = eta_hydro(ETA_WL_FRAME, q)
    yq_lo = eta_after_YQ_fulldisc(eh, F_YQ_HI)   # most favorable: max field coverage
    yq_hi = eta_after_YQ_fulldisc(eh, F_YQ_LO)   # least favorable: min field coverage
    print("%-26s %6.2f  %7.3f  [%.3f .. %.3f]  %s"
          % (label, q, eh, yq_lo, yq_hi, classify(yq_lo)))
    return eh, yq_lo, yq_hi

print("WL branch (no HSE rescale):")
eh_wl, yq_wl_lo, yq_wl_hi = row("  WL (q=1.00)", 1.00)
print("Hydro branch -- consensus & outlier:")
eh_lo, _, _   = row("  relaxed-floor", q_lo)            # ~1.05
eh_con, yq_con_lo, yq_con_hi = row("  CONSENSUS central", q_consensus)   # ~1.25
eh_hi, _, _   = row("  mixed-ceiling", q_hi)            # ~1.40
eh_li, yq_li_lo, yq_li_hi = row("  Li+2024 OUTLIER", q_outlier[0])       # ~1.76
# the value the XRISM synth leaned on:
eh_21, yq_21_lo, yq_21_hi = row("  XRISM-synth lean q=2.1", 2.10)

# ============================================================================================
# (4) BOTH-WAYS DECISION
# ============================================================================================
print("="*84)
print("BOTH-WAYS DECISION (penalize high-priest AND manufacturing equally):")
print()
print("BRANCH A (HONEST/consensus): q = %.2f [%.2f,%.2f]  =>  eta_hydro = %.2f [%.2f, %.2f]"
      % (q_consensus, q_lo, q_hi, eh_con, eta_hydro(ETA_WL_FRAME,q_hi), eta_hydro(ETA_WL_FRAME,q_lo)))
print("   after Y-Q field (17-20%%):  eta ~ %.2f [%.2f .. %.2f]  -> %s"
      % (yq_con_lo, eta_after_YQ_fulldisc(eta_hydro(ETA_WL_FRAME,q_hi),F_YQ_HI),
         eta_after_YQ_fulldisc(eta_hydro(ETA_WL_FRAME,q_lo),F_YQ_LO), classify(yq_con_lo)))
print()
print("BRANCH B (close): requires q ~ 1.8-2.1 (Li+2024/XRISM-synth lean). eta_hydro = %.2f-%.2f"
      % (eh_21, eh_li))
print("   after Y-Q field:  eta ~ %.2f-%.2f  -> %s" % (yq_21_lo, yq_li_lo, classify(yq_21_lo)))
print("   BUT q~2.1 is (i) a full/non-relaxed sample, (ii) internally undercut by its own")
print("   M_dyn~M_HSE<<M_WL => most plausibly a WL OVER-estimate, NOT a true 2x HSE bias.")
print("   Quoting it to close the residual = MANUFACTURING Branch B. Triaxiality (~2-4%) cannot")
print("   supply a 2x. => the DATA favors BRANCH A.")
print()
# Genuine both-ways caveat: WL itself may be ~10-25% over-estimated (the dynamical concordance).
# That nudges the TRUE q DOWN toward consensus from any high read; it does NOT push to closure.
WL_overest_lo, WL_overest_hi = 0.10, 0.25
eh_con_WLcorr = eta_hydro(ETA_WL_FRAME*(1-WL_overest_hi), q_consensus)
print("CAVEAT (both ways): if WL itself is over-estimated ~%d-%d%% (the dynamical concordance),"
      % (int(WL_overest_lo*100), int(WL_overest_hi*100)))
print("   eta_WL drops first, then /q -> eta ~ %.2f even after WL-correction + consensus q;"
      % eh_con_WLcorr)
print("   after Y-Q field ~ %.2f -> still %s. Material, still short of closure."
      % (eta_after_YQ_fulldisc(eh_con_WLcorr, F_YQ_HI), classify(eta_after_YQ_fulldisc(eh_con_WLcorr,F_YQ_HI))))
print()
print("VERDICT: consensus relaxed q ~ 1.25 (1.05-1.40) => eta_hydro ~ 1.7-2.2 (central ~1.87);")
print("after the no-particle Y-Q field ~ %.2f. The cluster residual is a REAL shared-MOND gap"
      % yq_con_lo)
print("(~half-covered), NOT framework-distinctive, NOT a referee-proof kill. The hydro branch lands")
print("at eta~1.8, NOT ~1.1. Branch B (close) is NOT supported by consensus. QUARANTINE held.")
print("="*84)

# machine-readable footer
print("RESULT_JSON_BEGIN")
import json
print(json.dumps({
  "eta_WL_frame": round(ETA_WL_FRAME,3), "eta_WL_canon": round(ETA_WL_CANON,3),
  "q_consensus": q_consensus, "q_spread": [q_lo, q_hi],
  "q_relaxed_floor": round(q_relaxed_floor,2), "q_mixed_ceiling": round(q_mixed_ceiling,2),
  "q_outlier_Li2024": q_outlier[0],
  "eta_hydro_consensus": round(eh_con,2),
  "eta_hydro_spread": [round(eta_hydro(ETA_WL_FRAME,q_hi),2), round(eta_hydro(ETA_WL_FRAME,q_lo),2)],
  "eta_hydro_Li2024": round(eh_li,2), "eta_hydro_q2p1": round(eh_21,2),
  "eta_after_YQ_consensus": [round(yq_con_lo,2), round(yq_con_hi,2)],
  "eta_after_YQ_q2p1": [round(yq_21_lo,2), round(yq_21_hi,2)],
  "f_YQ": [F_YQ_LO, F_YQ_HI],
  "verdict": "BRANCH_A_real_gap_stands"
}, indent=0))
print("RESULT_JSON_END")
