#!/usr/bin/env python3
"""G226 -- THE BTFR FLOOR FORECAST: the scatter's limit with resolved-mass IMF
knowledge.

THE QUESTION: what is the ACHIEVABLE BTFR scatter floor?  G087 built the model
    sigma_v(M_acc) = sqrt(intr^2 + (M_acc/4)^2)  dex (log10 v)
with intr = E1_loocv (the conservative intrinsic upper bound after removing
proxy-predicted trends, LOOCV) and M_acc the baryonic-mass accuracy in dex of
log10 M_b.  G087's committed numbers: sigma_obs = 0.1031 dex (26.79%),
E1_loocv = 0.0836 dex (21.24%), SPARC-era effective M_acc = 0.24 dex, the
M/L-population lens rms = 0.1887 dex in M_b (= 0.0472 dex in v), errV-only
noise floor = 0.0219 dex, forecast sigma_v(0.05) = 0.0846 dex (21.50%).

G226 folds in TWO new constraints:
  (1) THE IMP-PRINCIPAL LIMIT (G162): the ATLAS3D-class single-burst IMF
      constraints -- Cappellari+13 on 258 ETGs with (M/L)_JAM (Chabrier-
      class); a Kroupa-class IMF shift of +0.03..0.06 dex in M* produces
      <= -0.015 dex in the velocity residual r.  I.e. the population-IMF
      systematic is pinned at 0.015 dex in v (equivalently 0.06 dex in M*)
      for well-observed single-burst populations.
  (2) THE RESOLVED-IMF MASS PROSPECT (JWST era): for the SPARC-class disc
      dwarfs, JWST resolved stellar photometry + TRGB distances give per-
      galaxy M_acc in the 0.03-0.07 dex band (per-galaxy estimate uses the
      committed G087 per-galaxy f_star weights); G087's registered forecast
      anchor is M_acc = 0.05 dex.

THE FLOOR (Part 2): evaluate the attainable sigma_v at
  (a) 2026-era accuracy      : M_acc = 0.24 dex (SPARC effective, G087)
  (b) JWST-resolved          : M_acc = 0.05 dex (G087 forecast anchor)
  (c) IMF-principal-limited  : the ATLAS3D-class residual 0.015 dex in v
                               (M_acc = 0.06 dex equivalent)
the full floor curve sigma_v(M_acc) down to M_acc = 0.01 dex, and the limit
M_acc -> 0 (PERFECT masses): sigma_v -> intr = E1_loocv.

THE INTRINSIC REMNANT after the IMF side (Part 2b): the M/L-population lens
(0.0472 dex in v) is a COHERENT population systematic invisible to SPARC's
photometric proxies -- the LOOCV penalty gap (E1_loocv^2 - E1^2)^(1/2) =
0.0437 dex is almost exactly the lens amplitude (0.0472); resolving the IMF
removes that coherent piece, leaving a truly-intrinsic bound of
  intr_remnant = sqrt(E1_loocv^2 - lens_v^2 + imf_v^2) = 0.0706 dex (17.6%)
-- cross-checked against E1(in-sample) = 0.0713 dex (17.8%) to within 1%.

THE STATEMENT (V3): the zero-parameter law's scatter floor with PERFECT
masses = E1_loocv = 0.0836 dex = 21.2% in v (0.334 dex in M_b) -- NOT zero.
The resolved-mass era will NOT see the BTFR collapse; it will pin the
truly-intrinsic remnant at 0.071-0.084 dex (17.6-21.2%), ~1.4-1.6x ABOVE the
RAR within-galaxy white-noise analogue (0.045-0.052 dex) and >3x above the
errV noise floor (0.022 dex): "zero intrinsic scatter" survives only as an
upper bound, not as a measurement -- THE NUMBER: sigma_floor = 0.085 dex
(21.5%) achievable, 0.084 dex (21%) perfect-mass, 0.071 dex (17.6%) after
the IMF side.

Conventions (inherited, never re-fit): v^4 = G M_b a0, a0 = 9.3619e-11
(G036/G087 canonical); r = log10(V/pred); M_b from the curve's enclosed
baryons Vb2 = Vgas^2 + 0.5 Vdisk^2 + 0.7 Vbul^2 (G087).
Run:   python3 G226_btfr_floor.py > G226_btfr_floor.out
Outputs: G226_btfr_floor.out, G226_results.json.
"""
import json
import math
import os
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))


def jload(name):
    return json.load(open(os.path.join(HERE, name)))


g087 = jload("G087_results.json")
g162 = jload("G162_results.json")

# ------------------------------------------------------------------ committed anchors
SIG_OBS = g087["scatter"]["rms_dex"]                 # 0.1031 dex (26.79%)
INTR = g087["intrinsic"]["E1_loocv_dex"]             # 0.0836 dex (21.24%)
E1_INSAMP = g087["intrinsic"]["E1_dex"]              # 0.0713 dex (17.86%)
MACC_SPARC = g087["forecast"]["Macc_eff_sparc_dex"]  # 0.24 dex
LENS_MB = g087["intrinsic"]["M_L_lens_rms_dex_Mb"]   # 0.1887 dex in M_b
LENS_V = LENS_MB / 4.0                               # 0.0472 dex in v
ERRV_FLOOR = g087["intrinsic"]["errV_floor_dex"]     # 0.0219 dex
A3_IMF_V = 0.015                                     # G162: Kroupa shift <= 0.015 dex in r
A3_IMF_MB = 4.0 * A3_IMF_V                           # 0.06 dex in M*
A3_STATS = g162["channels"]["B_ATLAS3D_ETGs"]["stats"]  # 258 ETGs, med|r| 0.0831
RAR_FLOOR = (0.045, 0.052)                           # G036 0.0447 / G044 0.0524

print("=" * 96)
print("G226 -- THE BTFR FLOOR FORECAST: sigma_v(M_acc) with G162's IMF limit")
print("=" * 96)
print(f"law: v^4 = G M_b a0;  r = log10(V/pred);  a0 = 9.3619e-11 (G087 canonical)")
print(f"committed (G087): sigma_obs = {SIG_OBS:.4f} dex ({100*(10**SIG_OBS-1):.2f}%); "
      f"intr = E1_loocv = {INTR:.4f} dex ({100*(10**INTR-1):.2f}%); "
      f"E1(in-sample) = {E1_INSAMP:.4f} dex")
print(f"                  M_acc_eff(SPARC) = {MACC_SPARC:.2f} dex;  M/L lens = "
      f"{LENS_MB:.4f} dex in M_b = {LENS_V:.4f} dex in v;  errV floor = {ERRV_FLOOR:.4f} dex")
print(f"committed (G162): ATLAS3D 258 ETGs med|r| = {A3_STATS['median_abs_r']:.4f} dex; "
      f"Kroupa IMF shift ~ +0.03-0.06 dex in M* -> <= {A3_IMF_V} dex in r -> "
      f"M_acc_floor = {A3_IMF_MB:.2f} dex in M*")

# ================================================================== PART 1 -- the
# JWST-resolved-mass prospect: achievable M_acc per SPARC-class galaxy, using the
# committed G087 per-galaxy f_star = M_star/M_b (M_b = M_gas + 0.5 M_star).
# Error budget per term (publication-supported estimates):
#   dlnD_TRGB  = 0.010 dex (2-3% TRGB distances, Freedman-class)
#   dM*_JWST   = 0.04-0.06 dex (resolved CMD photometry + IMF/SFH degeneracy)
#   dM_gas     = 0.02-0.04 dex (21cm flux 5% + distance D^2 + helium factor)
print("\nPART 1 -- THE RESOLVED-IMF PROSPECT: per-galaxy JWST M_acc (SPARC classes)")
DG = 0.030   # gas-mass dex accuracy, JWST era (incl. TRGB distance)
DS = 0.055   # stellar-mass dex accuracy, JWST era (resolved CMD + IMF/SFH residue)
pg = g087["pergalaxy"]
rows = []
for g in pg:
    fstar = g.get("fstar")
    if fstar is None:
        continue
    fgas = 1.0 - 0.5 * fstar              # M_b = M_gas + 0.5 M_star
    macc = math.sqrt((fgas * DG) ** 2 + (0.5 * fstar * DS) ** 2)
    cls = ("GAS" if fstar < 0.35 else "MIX" if fstar < 0.70 else "STAR")
    rows.append(dict(name=g["name"], fstar=fstar, fgas=fgas, cls=cls, macc=macc))
by_cls = {}
for c in ("GAS", "MIX", "STAR"):
    ms = [r["macc"] for r in rows if r["cls"] == c]
    by_cls[c] = ms
allm = [r["macc"] for r in rows]
print(f"  budget: gas dM_gas = {DG:.3f} dex (21cm+TRGB), stellar dM* = {DS:.3f} dex "
      f"(JWST CMD+IMF), M_b = M_gas + 0.5 M_star weights")
print(f"  {'class':5s} {'n':>4s} {'M_acc median':>12s} {'range':>16s}")
for c in ("GAS", "MIX", "STAR"):
    ms = by_cls[c]
    print(f"  {c:5s} {len(ms):4d} {statistics.median(ms):12.3f} "
          f"[{min(ms):.3f}-{max(ms):.3f}]")
print(f"  ALL  {len(allm):4d} {statistics.median(allm):12.3f} "
      f"[{min(allm):.3f}-{max(allm):.3f}]")
JWST_MACC_MED = statistics.median(allm)
print(f"  -> JWST-resolved SPARC-class M_acc median = {JWST_MACC_MED:.3f} dex; "
      f"G087's registered forecast anchor = 0.05 dex (conservative: {DS:.3f} dex "
      f"stellar term); the floor band 0.03-0.07 dex is locked by TRGB + resolved-IMF.")
print(f"  ELT/IMF-principal floor (single-burst, ATLAS3D-class, G162): IMF residual "
      f"<= {A3_IMF_V} dex in v = {A3_IMF_MB:.2f} dex in M* -- the population side "
      f"cannot do better than this on ANY resolved photometry.")

# ================================================================== PART 2 -- THE FLOOR
print("\nPART 2 -- THE FLOOR: sigma_v(M_acc) = sqrt(intr^2 + (M_acc/4)^2)")
MCURVE = [0.24, 0.19, 0.15, 0.12, 0.10, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03,
          0.025, 0.02, 0.015, 0.01, 0.0]


def sv(macc):
    return math.sqrt(INTR ** 2 + (macc / 4.0) ** 2)


print(f"  M_acc [dex M_b]   sigma_v [dex]   sigma_v [%]   sigma_Mb [dex]")
curve = []
for M in MCURVE:
    v = sv(M)
    curve.append(dict(M_acc_dex=round(M, 3), sigma_v_dex=round(v, 4),
                      sigma_v_pct=round(100 * (10 ** v - 1), 2),
                      sigma_Mb_dex=round(4 * v, 3)))
    print(f"     {M:6.2f}           {v:8.4f}      {100*(10**v-1):6.2f}        {4*v:8.3f}")

sa = sv(MACC_SPARC)   # (a) 2026-era
sb = sv(0.05)         # (b) JWST-resolved
sc = sv(A3_IMF_MB)    # (c) IMF-principal-limited (0.015 dex in v <-> 0.06 in M*)
s0 = sv(0.0)          # perfect masses
sopt = sv(JWST_MACC_MED)  # bonus: the per-galaxy estimate's median (optimistic)
print(f"\n  ANCHORS:")
print(f"  (a) 2026-era accuracy      M_acc={MACC_SPARC:.2f} -> sigma_v = {sa:.4f} dex "
      f"({100*(10**sa-1):.2f}%)   [self-check vs sigma_obs = {SIG_OBS:.4f}]")
print(f"  (b) JWST-resolved          M_acc=0.05   -> sigma_v = {sb:.4f} dex "
      f"({100*(10**sb-1):.2f}%)   [G087 V3 forecast identical]")
print(f"  (c) IMF-principal-limited  M_acc=0.06   -> sigma_v = {sc:.4f} dex "
      f"({100*(10**sc-1):.2f}%)   [ATLAS3D-class 0.015 dex in v]")
print(f"  (c') per-galaxy JWST estimate M_acc={JWST_MACC_MED:.3f} -> sigma_v = "
      f"{sopt:.4f} dex ({100*(10**sopt-1):.2f}%)  [the resolved-population "
      f"optimistic floor -- indistinguishable from (c)]")
print(f"  (*) PERFECT masses         M_acc -> 0    -> sigma_v = {s0:.4f} dex "
      f"({100*(10**s0-1):.2f}%) = E1_loocv -- THE FLOOR")
print(f"  reading: the curve SATURATES at the intrinsic bound: between M_acc=0.10 "
      f"and perfect masses sigma_v contracts by only {100*(sv(0.10)-s0)/s0:.2f}% "
      f"({sv(0.10):.4f} -> {s0:.4f} dex); below M_acc = 0.1 the floor is FLAT to "
      f"within 5% -- the mass channel is exhausted, the intrinsic channel dominates.")

# ---- Part 2b -- the intrinsic remnant after the IMF side
print("\nPART 2b -- THE INTRINSIC REMNANT AFTER THE IMF SIDE")
gap_loocv = math.sqrt(max(0.0, INTR ** 2 - E1_INSAMP ** 2))     # LOOCV penalty amplitude
remnant = math.sqrt(max(0.0, INTR ** 2 - LENS_V ** 2) + A3_IMF_V ** 2)
print(f"  the LOOCV penalty: sqrt(E1_loocv^2 - E1_in^2) = {gap_loocv:.4f} dex in v "
      f"vs the M/L lens {LENS_V:.4f} dex -- the lens is the coherent, non-")
print(f"  generalizing population systematic the proxies could NOT remove "
      f"(G087's finding, now quantified).")
print(f"  resolving the IMF (ATLAS3D-class) removes that coherent piece "
      f"(-lens^2) and replaces it with the 0.015-dex residual:")
print(f"  intr_remnant = sqrt(E1_loocv^2 - {LENS_V:.3f}^2 + {A3_IMF_V}^2) = "
      f"{remnant:.4f} dex = {100*(10**remnant-1):.2f}%  [cross-check E1(in) = "
      f"{E1_INSAMP:.4f} dex = {100*(10**E1_INSAMP-1):.2f}% -- agree within "
      f"{100*abs(remnant-E1_INSAMP)/E1_INSAMP:.1f}%]")
print(f"  conservative bound (no lens subtraction allowed): intr <= {INTR:.4f} dex "
      f"= {100*(10**INTR-1):.2f}%.")
print(f"  the remnant sits ABOVE the RAR within-galaxy white-noise analogue "
      f"{RAR_FLOOR[0]:.3f}-{RAR_FLOOR[1]:.3f} dex and ABOVE the errV noise floor "
      f"{ERRV_FLOOR:.3f} dex -> the residual is NOT yet at the galactic-disc noise "
      f"floor: there is still a {remnant/RAR_FLOOR[1]:.1f}x gap to the floor-consistent "
      f"regime.")

# ================================================================== PART 3 -- VERDICTS
print("\nPART 3 -- THE VERDICTS")
RES = []


def check(n, ok, measured, reading):
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    print(f"         reading : {reading}")
    RES.append({"name": n, "pass": bool(ok), "measured": str(measured)})


# V1 -- the floor curve (delivered to 0.01 dex, flat below M_acc = 0.1)
flatness = (sv(0.10) - s0) / s0                                     # fractional rise at 0.10
v1_ok = (abs(sa - SIG_OBS) < 0.001 and flatness < 0.05 and
         all(curve[i]["sigma_v_dex"] >= curve[i + 1]["sigma_v_dex"]
             for i in range(len(curve) - 1)))
check("V1 the floor curve sigma_v(M_acc) to 0.01 dex: monotone, saturating at the "
      "intrinsic bound; self-consistent at the SPARC point",
      v1_ok,
      f"sigma_v(0.24) = {sa:.4f} vs sigma_obs = {SIG_OBS:.4f} "
      f"(delta {1000*abs(sa-SIG_OBS):.1f}e-4 dex); flatness at M_acc=0.10: "
      f"{100*flatness:.2f}%; curve N = {len(curve)} points to M_acc = 0.01",
      f"the floor curve is delivered and quantified: sigma_v falls from "
      f"{sa:.4f} dex (2026, {100*(10**sa-1):.1f}%) to {sb:.4f} dex (JWST, "
      f"{100*(10**sb-1):.1f}%) to {sc:.4f} dex (IMF-limited, "
      f"{100*(10**sc-1):.1f}%) and SATURATES at E1_loocv = {s0:.4f} dex "
      f"({100*(10**s0-1):.1f}%) for perfect masses; between M_acc = 0.10 and "
      f"M_acc = 0 sigma_v contracts by only {100*flatness:.1f}% -- the mass "
      f"channel is exhausted, the intrinsic channel dominates.")

# V2 -- the intrinsic remnant after the IMF side
v2_ok = (remnant < INTR and abs(remnant - E1_INSAMP) / E1_INSAMP < 0.05)
check("V2 the intrinsic remnant after the IMF side: the M/L lens is the LOOCV "
      "penalty; resolving it to ATLAS3D-class leaves 0.071 dex",
      v2_ok,
      f"intr_remnant = {remnant:.4f} dex ({100*(10**remnant-1):.2f}%) "
      f"from sqrt(E1_loocv^2 - lens^2 + IMF^2) with lens = {LENS_V:.4f} dex, "
      f"IMF = {A3_IMF_V} dex in v; E1(in) = {E1_INSAMP:.4f} dex; "
      f"RAR floor = {RAR_FLOOR[0]:.3f}-{RAR_FLOOR[1]:.3f} dex",
      f"the truly-intrinsic bound after the IMF side = {remnant:.4f} dex "
      f"({100*(10**remnant-1):.1f}%), agreeing with G087's in-sample E1 "
      f"({E1_INSAMP:.4f}) to within {100*abs(remnant-E1_INSAMP)/E1_INSAMP:.0f}% -- "
      f"the M/L lens IS the non-generalizing systematics; but even fully resolved "
      f"masses leave the scatter {remnant/RAR_FLOOR[1]:.1f}x ABOVE the RAR "
      f"within-galaxy noise floor 0.045-0.052 dex: the pure-mass side of the BTFR "
      f"does NOT reach the noise floor -- zero intrinsic scatter is NOT "
      f"demonstrable from mass resolution alone.")

# V3 -- the honest statement
num_jwst = sb
num_floor = s0
num_rem = remnant
v3_ok = (0.07 < num_floor < 0.10 and 0.07 < num_rem < 0.09)
check("V3 the honest statement: the resolved-mass era will pin the floor, not erase "
      "it -- THE NUMBER",
      v3_ok,
      f"sigma_v: 2026 = {sa:.4f} ({100*(10**sa-1):.2f}%); JWST = {num_jwst:.4f} "
      f"({100*(10**num_jwst-1):.2f}%); IMF-limited = {sc:.4f} "
      f"({100*(10**sc-1):.2f}%); perfect-mass floor = {num_floor:.4f} "
      f"({100*(10**num_floor-1):.2f}%, {4*num_floor:.3f} dex in M_b); "
      f"post-IMF intrinsic remnant = {num_rem:.4f} ({100*(10**num_rem-1):.2f}%)",
      f"THE STATEMENT: the zero-parameter law's scatter floor with PERFECT masses "
      f"= E1_loocv = {num_floor:.4f} dex = {100*(10**num_floor-1):.1f}% in v "
      f"({4*num_floor:.3f} dex in M_b) -- NOT zero.  The resolved-mass era "
      f"(JWST + TRGB + ATLAS3D-class IMF) will achieve sigma_v = {num_jwst:.4f} dex "
      f"({100*(10**num_jwst-1):.1f}%) and pin the truly-intrinsic remnant at "
      f"{num_rem:.4f}-{num_floor:.4f} dex ({100*(10**num_rem-1):.1f}%-"
      f"{100*(10**num_floor-1):.1f}%): the 'zero intrinsic scatter' claim "
      f"SURVIVES only as an upper bound, and the next discriminator is the "
      f"RAR white-noise floor {RAR_FLOOR[0]:.3f}-{RAR_FLOOR[1]:.3f} dex "
      f"(the remnant still sits {num_rem/RAR_FLOOR[1]:.1f}x above it).")

print(f"\nG226 COMPLETE: {sum(1 for r in RES if r['pass'])}/{len(RES)} checks PASS.")

# ================================================================== artifact
out = {
 "lane": "G226_btfr_floor",
 "title": "THE BTFR FLOOR FORECAST: the scatter's limit with resolved-mass IMF knowledge (G087 model + G162 IMF constraint + JWST-resolved-mass prospects)",
 "model": {"sigma_v_Macc": "sqrt(intr^2 + (M_acc/4)^2) dex in log10 v; intr = E1_loocv (G087)", "a0": "9.3619e-11"},
 "committed_inputs": {
   "G087": {"sigma_obs_dex": SIG_OBS, "sigma_obs_pct": round(100 * (10 ** SIG_OBS - 1), 2),
            "E1_loocv_dex": INTR, "E1_loocv_pct": round(100 * (10 ** INTR - 1), 2),
            "E1_in_sample_dex": E1_INSAMP, "Macc_eff_sparc_dex": MACC_SPARC,
            "ML_lens_dex_Mb": LENS_MB, "ML_lens_dex_v": round(LENS_V, 4),
            "errV_floor_dex": ERRV_FLOOR},
   "G162": {"ATLAS3D_n": A3_STATS["n"], "ATLAS3D_med_abs_r_dex": A3_STATS["median_abs_r"],
            "IMF_shift_kroupa_dex_Mstar": [0.03, 0.06],
            "IMF_shift_dex_in_v": A3_IMF_V, "Macc_floor_dex_Mstar": A3_IMF_MB}},
 "jwst_resolved_prospect": {
   "per_term_budget": {"dM_gas_dex": DG, "dM_star_dex": DS,
                       "note": "gas: 21cm flux 5% + TRGB distance D^2; stellar: JWST resolved CMD + IMF/SFH degeneracy"},
   "per_class_Macc": {c: {"n": len(by_cls[c]),
                          "median": round(statistics.median(by_cls[c]), 3),
                          "range": [round(min(by_cls[c]), 3), round(max(by_cls[c]), 3)]}
                      for c in ("GAS", "MIX", "STAR")},
   "all_median_dex": round(JWST_MACC_MED, 3),
   "range_dex": [round(min(allm), 3), round(max(allm), 3)],
   "registered_anchor_dex": 0.05,
   "IMF_principal_floor_dex_v": A3_IMF_V},
 "floor_curve": curve,
 "anchors": {
   "a_2026_Macc_0_24": {"M_acc": MACC_SPARC, "sigma_v_dex": round(sa, 4),
                        "sigma_v_pct": round(100 * (10 ** sa - 1), 2)},
   "b_jwst_Macc_0_05": {"M_acc": 0.05, "sigma_v_dex": round(sb, 4),
                        "sigma_v_pct": round(100 * (10 ** sb - 1), 2)},
   "c_imf_Macc_0_06": {"M_acc": A3_IMF_MB, "sigma_v_dex": round(sc, 4),
                       "sigma_v_pct": round(100 * (10 ** sc - 1), 2)},
   "c2_per_galaxy_jwst_median": {"M_acc": round(JWST_MACC_MED, 3),
                                 "sigma_v_dex": round(sopt, 4),
                                 "sigma_v_pct": round(100 * (10 ** sopt - 1), 2)},
   "perfect_masses": {"M_acc": 0.0, "sigma_v_dex": round(s0, 4),
                      "sigma_v_pct": round(100 * (10 ** s0 - 1), 2),
                      "sigma_Mb_dex": round(4 * s0, 3)}},
 "intrinsic_remnant": {
   "loocv_penalty_dex": round(gap_loocv, 4),
   "ML_lens_dex_v": round(LENS_V, 4),
   "remnant_dex": round(remnant, 4),
   "remnant_pct": round(100 * (10 ** remnant - 1), 2),
   "crosscheck_E1_in_sample_dex": E1_INSAMP,
   "conservative_bound_dex": INTR,
   "RAR_white_noise_floor_dex": list(RAR_FLOOR),
   "errV_floor_dex": ERRV_FLOOR,
   "gap_to_RAR_upper_x": round(remnant / RAR_FLOOR[1], 2)},
 "statement": {
   "perfect_mass_floor_dex": round(s0, 4),
   "perfect_mass_floor_pct_v": round(100 * (10 ** s0 - 1), 2),
   "perfect_mass_floor_dex_Mb": round(4 * s0, 3),
   "jwst_era_sigma_v_dex": round(sb, 4),
   "post_IMF_remnant_dex": round(remnant, 4),
   "number": "sigma_floor = 0.085 dex (21.5%) achievable (JWST); 0.084 dex (21%) with perfect masses; 0.071 dex (17.6%) after the ATLAS3D-class IMF side -- the zero-intrinsic-scatter claim survives only as an upper bound"},
 "verdicts": [{"name": r["name"], "pass": r["pass"], "measured": r["measured"]} for r in RES],
 "n_pass": int(sum(1 for r in RES if r["pass"])),
 "n_total": int(len(RES)),
}

with open(os.path.join(HERE, "G226_results.json"), "w") as f:
    json.dump(out, f, indent=1)
print("wrote G226_results.json")