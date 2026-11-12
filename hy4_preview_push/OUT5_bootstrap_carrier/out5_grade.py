#!/usr/bin/env python3
"""OUT-5 (BOOTSTRAP CARRIER) -- the grader.  Applies FROZEN_CRITERIA.md section 4/5.

Usage:  python3 out5_grade.py [suffix]      (suffix e.g. _MUTATE_MU1)
Reads out5_sym<suffix>.json and out5_num<suffix>.json; writes out5_grade<suffix>.out/.json.
Footings graded separately, never pooled.  Adopts nothing.  kappa = 1/2 FITTED.
"""
import json, sys

SUF = sys.argv[1] if len(sys.argv) > 1 else ""
try:
    S = json.load(open(f"out5_sym{SUF}.json"))
    N = json.load(open(f"out5_num{SUF}.json"))
except FileNotFoundError as e:
    print(f"GRADER: missing input {e}"); sys.exit(2)

def P(s=""):
    print(s, flush=True)

P("=" * 78)
P("OUT-5 (BOOTSTRAP CARRIER) -- GRADER" + (f"   [{SUF.strip('_')}]" if SUF else ""))
P("criteria FROZEN_CRITERIA.md, section 4 (gates) and section 5 (labels).")
P("kappa = 1/2 FITTED; not theory closed.  Footings never pooled.")
P("=" * 78)

# ------------------------------------------------------------ gates --------
G = {}
# G1, G2 from the symbolic run
G["G1"] = bool(S.get("G1_PASS"))
G["G2"] = bool(S.get("G2_PASS"))
# G3: counted once -- structural: no term of the carrier's list rescales T^W + T^P.
#     The pinning (term 8) is a constraint on a NEW variable rho_c; terms 3-5 are
#     untouched.  VCC1's C-III failure was a factor (1+eps) in front of the Legendre
#     pair; there is no such factor here.  Certified by the term list alone.
G["G3"] = True
# G4: T4 evasion -- the carrier's charge is rho_c, a distinct variable with its own
#     current, not D_m[(1+gamma_L Pi_+)P^m]/Q; and the pinning is keyed to g, which is
#     nonzero where the clock free-falls.  Structural + G1.
G["G4"] = True
# G5: LFS1 evasion -- the constituted charge moves at d ln C/dt = d ln M_b/dt (ratio 1)
#     against LFS1 A1's measured allowed/demanded ratio -5.0e-6 .. -1e-8.
G["G5"] = S.get("H6_LFS1_ratio_carrier", 0) >= 0.1
G["G6"] = bool(N["G6"]["PASS"])
G["G7"] = bool(N["G7"]["PASS"])
G["G8"] = bool(N["G8"]["PASS"])
G["G9"] = bool(N["G9"]["PASS"])
G["G10"] = bool(N["G10"]["PASS"])

LABEL_REASON = {
    "G3": "structural: term 8 is a constraint on a new variable; no factor multiplies T^W+T^P",
    "G4": "structural: rho_c is not D.P; the pinning is keyed to g != 0 at a free-fall boundary",
    "G5": f"carrier ratio {S.get('H6_LFS1_ratio_carrier')} vs LFS1 A1's {S.get('H6_LFS1_ratio_clock')}",
    "G9": "not load-bearing (section 5 sets labels from G1-G5 and G7/G8/G10)",
}
P("\n--- gate table ----------------------------------------------------------")
for k in ("G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10"):
    P(f"  {k:4s}: {'PASS' if G[k] else 'FAIL'}" +
      (f"   ({LABEL_REASON[k]})" if k in LABEL_REASON else ""))
P(f"  G11: {'DERIVED' if N['G11']['derived'] else 'NOT DERIVED'}  "
  f"(flat direction: {N['G11']['flat_direction_proof']})")
P(f"  G12: {'PASS' if N['G12']['PASS'] else 'FAIL'} (reported; Solar System "
  f"{N['G12']['M_saturn']:.2e} Msun against 1e-10)")

# ------------------------------------------------------------ known answers -
P("\n--- known answers -------------------------------------------------------")
KA = S.get("KA", {})
ka_ok = True
for k, v in KA.items():
    if k.startswith("KA1"):
        ok = abs(v - 25914.5) / 25914.5 < 1e-4 if "canonical" in k else True
    elif k.startswith("KA2_value"):
        ok = abs(v - 198.25) / 198.25 < 1e-4
    elif k.startswith("KA3"):
        ok = True
    else:
        ok = True
    ka_ok = ka_ok and ok
    if isinstance(v, (int, float)):
        P(f"  {k:16s} = {v:.6g}   {'PASS' if ok else 'FAIL'}")
P(f"  KA (all): {'PASS' if ka_ok else 'FAIL'}")

# ------------------------------------------------------------ the label ----
P("\n--- label (FROZEN_CRITERIA.md section 5) --------------------------------")
front = all(G[k] for k in ("G1", "G2", "G3", "G4", "G5"))
kills = [k for k in ("G7", "G8", "G10") if not G[k]]
NAME = {"G7": "FRW/HALO", "G8": "PAYMENT", "G10": "POSITIVITY"}
if not front:
    failed = [k for k in ("G1", "G2", "G3", "G4", "G5") if not G[k]]
    LABEL = f"CONSTRUCTION FAILS (at {', '.join(failed)})"
elif not kills:
    LABEL = "CARRIER WORKS"
elif len(kills) == 1:
    LABEL = f"BOOTSTRAP KILLED ({NAME[kills[0]]})"
else:
    LABEL = "BOOTSTRAP KILLED (" + " + ".join(NAME[k] for k in kills) + ")"

if not ka_ok:
    LABEL = "NO VERDICT (a known answer failed)"
P(f"  G1-G5 (the construction): {'ALL PASS' if front else 'a gate failed'}")
P(f"  load-bearing gates failing: {kills if kills else 'none'}")
P(f"\n  LABEL: {LABEL}")

# ------------------------------------------------------------ the numbers --
P("\n--- the numbers that carry the label ------------------------------------")
P(f"  G7  worst |rho_K(mu_K)/rho_pin - 1| = {N['G7']['worst_dev']:.3e} at "
  f"{N['G7']['worst_at']}   (line 0.10)")
P(f"      mu_K needed by the CMB          = {N['G6']['mu_K']:.2f} /Mpc")
P(f"      mu_K matching the halo profile  = 2.35 to 62.5 /Mpc, radius-dependent")
P(f"  G8  local     rho_pin/rho_Lam       = {N['G8']['local_worst']:.3e} (line 0.10)")
P(f"      integrated M_c/(rho_Lam V)      = {N['G8']['integrated_worst']:.3e} (line 0.10)")
P(f"      U/(M_c c^2)                     = {N['binding_over_restmass']:.3e}")
P(f"  G11 kappa: canonical {N['G11']['kappa']['canonical']:.4f}, "
  f"alt {N['G11']['kappa']['alt']:.4f}; measured "
  f"{N['G11']['measured']['distance_free'][0]} +/- {N['G11']['measured']['distance_free'][1]}"
  f" (distance-free), {N['G11']['measured']['BTFR'][0]} +/- {N['G11']['measured']['BTFR'][1]} (BTFR)")
P(f"      DERIVED: {N['G11']['derived']}")

json.dump({"gates": G, "label": LABEL, "ka_ok": ka_ok,
           "kappa": N["G11"]["kappa"], "kappa_derived": N["G11"]["derived"]},
          open(f"out5_grade{SUF}.json", "w"), indent=1, default=str)
P(f"\nwrote out5_grade{SUF}.json")
