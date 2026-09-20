#!/usr/bin/env python3
"""
bhstar_l1_ktable_falsification.py -- WAVE L: the K-table falsifies the H1/J1
kappa-suppression hypothesis. THE HONEST KILL.
================================================================================================
ABSORBED (provenance): Chandrasekhar 1965, ApJ 142, 1519, Table 1 ("Values of the constant
K" for the 1PN radial-instability criterion R/R_s = K/(gamma - 4/3)):
    n = 0:   K = 0.452381 (= 19/42; also Chandrasekhar 1964 PRL 12, 437 erratum, eq. 22')
    n = 1:   K = 0.5654        n = 1.5: K = 0.6451
    n = 2:   K = 0.7513        n = 2.5: K = 0.9003
    n = 3:   K = 1.1245        n = 3.25: K = 1.2850   n = 3.5: K = 1.4995
The GR coefficient in the H1/G2 notation (instability when Gamma1 - 4/3 < kappa_GR * alpha,
alpha = GM/(Rc^2)): kappa_GR(structure) = 2K (since R_s/R = 2 alpha):
    n = 0: kappa = 19/21 = 0.905      n = 3: kappa = 2.249      n = 3.5: kappa = 2.999
MONOTONE INCREASING with concentration: MORE centrally condensed => MORE GR-unstable
(for a constant-gamma polytrope). There is NO structure suppression to kappa ~ 1e-3.

THE FALSIFICATION (of my own H1/J1 chain, stated plainly):
  H1 proposed the SMS ceiling 1e5-6 requires a "structure-suppressed" effective
  kappa_GR ~ 1e-3-1e-2 (the central-beta reading: kappa_req(1e5) = 2.773e-3). The K-table
  kills that hypothesis: every tabulated polytrope has kappa_GR in [0.905, 2.999] -- 2.5-3.3
  dex ABOVE the required value. With ANY tabulated K and the certified central-beta chain
  (T2 invariant + T4 envelope), the ceiling would sit at
      M_ceiling = 1e5 * (2.773e-3 / (2K))^(2/5)  =  6.7e3 ... 9.9e3 Msun
  -- one dex BELOW the observed SMS/LRD ceiling. Yet SMSs AT 1e5-6 exist (they are the
  paper's whole premise). Modus tollens: the central-beta-only stability reading is WRONG;
  the stability margin must come from the Gamma1(b) PROFILE -- the gas-dominated ENVELOPE
  layers (beta -> O(1), Gamma1 -> 5/3) whose mass-weighted contribution to the fundamental
  mode keeps Gamma1_eff above 4/3 + kappa*alpha while the central gap vanishes.

WHAT SURVIVES THE KILL (each certified independently):
  T2 invariant x*q^3*M^2 = C (thermodynamics, Lean I01) -- per-layer, survives.
  T4 envelope beta/6 <= Gamma1-4/3 <= beta/3 (thermodynamics, Lean I01) -- per-layer, survives.
  The K-table (Chandrasekhar 1965) -- absorbed with provenance.
  The ceiling 1e5-6 (the paper's premise + Saio+24's structures) -- observational.
WHAT DIES:
  The "structure-suppressed kappa_GR ~ 1e-3" hypothesis (H1's band, J1's central-beta
  closed form as a STABILITY statement). J1's closed form SURVIVES in amended form with
  gap -> gap_profile(M), an unknown until the eigenproblem is run.

THE REDEFINED OPERATOR DOOR (the precise, honest target):
  The 1PN pulsation eigenproblem with the Gamma1(beta(r)) PROFILE from the certified T2/T4
  thermodynamics: does the envelope's gas-dominated mass keep Gamma1_eff above the
  Chandrasekhar criterion at M = 1e5-6, and where exactly does the profile-weighted mode go
  unstable? THAT is the discrete number the framework's 1PN fluid sector must reproduce.
  The K-table is the boundary-case anchor (constant-gamma polytropes, tabulated).

Run:  python3 reviews/bhstar_l1_ktable_falsification.py  (stdlib only)
"""

import math, json, os

C_INV = 29.68                 # the T2 invariant constant: x = C/(q^3 M^2), q=0.4 anchor
Q0 = 0.4
M0 = 1e5
A5 = 2.788e-6
KAPPA_REQ_1E5 = 2.773e-3      # H1's central-beta required coefficient at 1e5 (to be killed)

# ABSORBED: Chandrasekhar 1965 Table 1 (provenance-checked 2026-09-19)
K_TABLE = {0.0: 0.452381, 1.0: 0.5654, 1.5: 0.6451, 2.0: 0.7513,
           2.5: 0.9003, 3.0: 1.1245, 3.25: 1.2850, 3.5: 1.4995}

results = []
def check(name, ok, detail=""):
    results.append(dict(check=name, ok=bool(ok), detail=detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
    return ok

def kappa_of_n(n):
    return 2.0 * K_TABLE[n]

def M_ceiling_central_beta(kappa):
    """The ceiling the certified central-beta chain gives for a GR coefficient kappa."""
    return 1e5 * (KAPPA_REQ_1E5 / kappa) ** 0.4

print("=" * 78)
print("WAVE L -- THE K-TABLE FALSIFICATION (absorbed: Chandrasekhar 1965, Table 1)")
print("=" * 78)

print("\n[A] The absorbed K-table and the GR coefficients")
print("    n      K       kappa_GR = 2K")
for n, K in K_TABLE.items():
    print(f"    {n:4.2f}  {K:7.4f}   {kappa_of_n(n):8.4f}")
check("n = 0 gives K = 19/42 exactly (the erratum's asymptotic form)",
      abs(K_TABLE[0.0] - 19.0 / 42.0) < 1e-6)
check("kappa_GR monotone INCREASING with concentration (0.905 -> 2.999 over n = 0 -> 3.5)",
      all(kappa_of_n(list(K_TABLE)[i]) < kappa_of_n(list(K_TABLE)[i + 1])
          for i in range(len(K_TABLE) - 1)))

print("\n[B] THE FALSIFICATION: the tabulated coefficients vs the central-beta requirement")
print(f"    central-beta requirement for stability at M = 1e5: kappa_GR <= {KAPPA_REQ_1E5:.2e}")
print(f"    tabulated range: kappa_GR in [{kappa_of_n(0.0):.3f}, {kappa_of_n(3.5):.3f}]")
gap_dex = math.log10(kappa_of_n(0.0) / KAPPA_REQ_1E5)
check("EVERY tabulated polytrope kappa_GR exceeds the central-beta requirement by 2.5-3.3 dex",
      gap_dex > 2.4, f"{gap_dex:.2f} dex (even the LEAST concentrated, n = 0)")
print("\n    central-beta ceilings with the tabulated coefficients:")
for n, K in K_TABLE.items():
    Mc = M_ceiling_central_beta(kappa_of_n(n))
    print(f"      n = {n:4.2f}:  M_ceiling = {Mc:9.3e} Msun")
mc_all = [M_ceiling_central_beta(kappa_of_n(n)) for n in K_TABLE]
check("central-beta ceiling with ANY tabulated K: <= 1e4 Msun (one dex below the observed ceiling)",
      max(mc_all) < 1.05e4, f"max = {max(mc_all):.3e} Msun")

print("\n[C] THE MODUS TOLLENS (the honest kill, then the redefined door)")
print("    SMSs at M = 1e5-6 EXIST (the paper's premise; Saio+24's structures).")
print("    Central-beta + any tabulated K => unstable above ~1e4.")
print("    => the central-beta-only stability reading is FALSIFIED;")
print("    => the stability margin comes from the Gamma1(beta(r)) PROFILE -- the gas-dominated")
print("    envelope layers (beta -> O(1), Gamma1 -> 5/3) whose mass-weighted mode contribution")
print("    holds Gamma1_eff above 4/3 + kappa*alpha while the central gap vanishes.")
check("the required profile gap at M = 1e5 exceeds the central gap by ~800x",
      kappa_of_n(3.0) * A5 / (7.73e-9) > 700.0,
      f"kappa*alpha = {kappa_of_n(3.0) * A5:.2e} vs central gap 7.73e-9")
print("    H1's kappa_GR band [8.8e-6, 4.8e-3]: FALSIFIED as a structure-suppression")
print("    hypothesis. J1's closed form survives AMENDED: M_ceiling ~ (q^3 kappa)^(-2/5)")
print("    with gap -> gap_PROFILE(M), unknown until the eigenproblem is run.")
print("    The redefined 1PN-operator door: the Gamma1(beta(r)) PROFILE eigenproblem with")
print("    the certified T2/T4 per-layer thermodynamics; the K-table is the constant-gamma")
print("    boundary-case anchor (tabulated).")

n_pass = sum(1 for r in results if r["ok"])
print(f"\n<BHSTAR-L1> COMPLETE: {n_pass}/{len(results)} checks PASS.")
out = dict(lane="bhstar_l1_ktable_falsification",
           absorbed="Chandrasekhar 1965 ApJ 142 1519 Table 1: K(n) for n=0..3.5; kappa_GR = 2K",
           k_table=K_TABLE,
           central_beta_ceiling_max=max(mc_all),
           verdict="central-beta-only stability reading FALSIFIED; the Gamma1-profile "
                   "eigenproblem is the redefined operator door",
           checks=results)
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bhstar_l1_ktable_falsification_results.json")
with open(p, "w") as fh:
    json.dump(out, fh, indent=1)
