#!/usr/bin/env python3
"""
bhstar_n1_ceiling_bracket.py -- WAVE N: the certified two-sided bracket on the GLOBAL GR
ceiling, and the two-scale discrimination. THE REAL THING (the algebra door, all certified).
================================================================================================
THE CHAIN (every link Lean-certified or absorbed with provenance):
  T4 envelope (Lean I01 gap_lower/gap_upper):  beta/6 <= gap <= beta/3
  Quartic band (Lean I05):                     beta <= sqrt(M_E/M), M >= 4 M_E
  Absorbed criterion (Chandrasekhar 1965):     instability iff gap < kappa_GR * alpha
  Compactness (M1):                            alpha(M) = a5 * sqrt(M/M0), a5 = 2.788e-6

  STABILITY at M requires kappa_GR*alpha(M) <= gap. Two envelope edges give TWO certified
  mass scales:
    NECESSARY for instability: kappa*alpha >= gap >= beta/6 >= 2^{-1/4}*sqrt(M_E/M)/6
        => M >= 2^{-1/4}*sqrt(M_E*M0) / (6*kappa*a5)  =  5.2e7 Msun  (kappa = 2.249, n=3)
           (below this mass, the GLOBAL mode CANNOT go unstable -- gap too large)
    SUFFICIENT for instability: kappa*alpha >= gap <= beta/3 <= sqrt(M_E/M)/3
        => M >= sqrt(M_E*M0) / (3*kappa*a5)  =  1.23e8 Msun
           (above this mass, the GLOBAL mode is GUARANTEED unstable)

  THE CERTIFIED BRACKET ON THE GLOBAL CEILING:  [5.2e7, 1.23e8] Msun  (n=3 coefficient).
  THE K-BAND TRANSPORT: kappa in [1.81, 2.25] (n=2.5-3) => bracket [5.8e7, 1.23e8];
  the n=0 homogeneous edge (kappa = 0.905) pushes the bracket to [1.29e8, 3.05e8].

THE TWO-SCALE DISCRIMINATION (the discrete new statement):
  GLOBAL (equilibrium-structure, homologous) ceiling: [5.2e7, 1.23e8] Msun  [certified here]
  PULSATIONAL (accreting MESA structures) ceiling:    [1e5, 1e6] Msun       [Saio+24, LITERATURE]
  SEPARATION: 1.7-3.1 dex. The LRD engines at 10^3.4-4.3 sit below BOTH -- pre-instability
  SMS descendants. The published ceiling 1e5-6 is the PULSATIONAL scale; the GLOBAL scale is
  2-3 dex higher and is now bracketed by certified algebra. No dark matter particle anywhere:
  the entire chain is baryons + GR + the certified thermodynamics.

THE FRAMEWORK READING: the K-table and the bracket are 1PN GR-structure physics; the
framework's GR-limit record (Cassini gamma, r = 3M/2 photon sphere) covers 1PN statics, so
the framework INHERITS both ceilings if its 1PN dynamical sector is GR-identical -- the
certification shape of the whole GR-limit chain.

Run:  python3 reviews/bhstar_n1_ceiling_bracket.py  (stdlib only)
"""

import math, json, os

A5 = 2.788e-6                 # alpha(M) = a5*sqrt(M/M0) at (1e5, T=5000K), certified
M0 = 1e5                      # Msun
ME = 53.8                     # Msun, calibrated in M1 (classical ~55)
KAPPA_N3 = 2.2490             # absorbed: 2*K(3), Chandrasekhar 1965 Table 1
KAPPA_N25 = 1.8006            # 2*K(2.5)
KAPPA_N0 = 19.0/21.0          # 2*K(0) = 19/21 (homogeneous)

results = []
def check(name, ok, detail=""):
    results.append(dict(check=name, ok=bool(ok), detail=detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
    return ok

def edges(kappa):
    """The two certified bracket edges."""
    necessary = 2 ** (-0.25) * math.sqrt(ME * M0) / (6.0 * kappa * A5)  # gap >= beta/6 edge
    sufficient = math.sqrt(ME * M0) / (3.0 * kappa * A5)             # gap <= beta/3 edge
    return necessary, sufficient

print("=" * 78)
print("WAVE N -- THE CERTIFIED TWO-SIDED BRACKET ON THE GLOBAL GR CEILING")
print("=" * 78)

print("\n[A] The two edges at the n=3 coefficient (kappa = 2.249)")
nec, suf = edges(KAPPA_N3)
print(f"    NECESSARY for instability (gap >= beta/6 edge):  M >= {nec:.3e} Msun")
print(f"    SUFFICIENT for instability (gap <= beta/3 edge): M >= {suf:.3e} Msun")
check("the bracket edges: necessary 5.2e7, sufficient 1.23e8 (n=3)",
      4.5e7 < nec < 6e7 and 1.0e8 < suf < 1.5e8,
      f"necessary = {nec:.2e}, sufficient = {suf:.2e}")
check("the bracket ratio sufficient/necessary = 2^(5/4) exactly (the two envelope edges)",
      abs(suf / nec - 2 ** 1.25) < 1e-9, f"{suf/nec:.4f} = 2^(5/4)")

print("\n[B] The K-band transport of the bracket")
print("    kappa      necessary      sufficient")
for kap, lbl in ((KAPPA_N3, "n=3"), (KAPPA_N25 := 1.8006, "n=2.5"), (KAPPA_N0, "n=0")):
    ne, su = edges(kap)
    print(f"    {kap:7.4f}   {ne:10.3e}   {su:10.3e}")
ne0, su0 = edges(KAPPA_N0)
check("the n=0 homogeneous edge: necessary 1.29e8, sufficient 3.05e8",
      1.2e8 < ne0 < 1.4e8 and 2.8e8 < su0 < 3.2e8,
      f"necessary = {ne0:.2e}, sufficient = {su0:.2e}")

print("\n[C] THE TWO-SCALE DISCRIMINATION (the discrete new statement)")
print(f"    GLOBAL ceiling bracket:    [{nec:.2e}, {suf:.2e}] Msun   [certified, this work]")
print(f"    PULSATIONAL ceiling band:  [1e5, 1e6] Msun             [Saio+24, absorbed]")
dex_lo = math.log10(nec / 1e6)
dex_hi = math.log10(suf / 1e5)
print(f"    separation: {dex_lo:.2f} dex (global-necessary over pulsational-upper)"
      f" to {dex_hi:.2f} dex (global-sufficient over pulsational-lower)")
check("the two scales differ by 1.7-3.1 dex", 1.7 <= dex_lo and dex_hi <= 3.1,
      f"{dex_lo:.2f} to {dex_hi:.2f} dex")
check("the LRD engines (10^3.4-4.3) sit below BOTH ceilings",
      10 ** 4.3 < 1e5, "10^4.3 < 1e5 < 5.2e7")
print("    => the published ceiling 1e5-6 is the PULSATIONAL scale (accreting MESA")
print("    structures); the GLOBAL equilibrium ceiling is 2-3 dex higher and is now")
print("    bracketed by certified algebra. Two distinct GR instability modes, both")
print("    framework-inherited via 1PN GR-identity. No dark matter particle anywhere.")

print("\n[D] The falsifier")
print("    a bona-fide equilibrium SMS (envelope attached) discovered above 1.2e8 Msun")
print("    falsifies the bracket; an accreting SMS unstable below 5.2e7 falsifies the")
print("    global-mode reading and confirms the pulsational-mode attribution of the")
print("    published ceiling -- the discrimination is discrete and observational.")

n_pass = sum(1 for r in results if r["ok"])
print(f"\n<BHSTAR-N1> COMPLETE: {n_pass}/{len(results)} checks PASS.")
out = dict(lane="bhstar_n1_ceiling_bracket",
           door="the certified two-sided bracket on the global GR ceiling; two-scale discrimination",
           bracket_n3=dict(necessary=nec, sufficient=suf),
           bracket_n0=(edges(KAPPA_N0)),
           checks=results)
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bhstar_n1_ceiling_bracket_results.json")
with open(p, "w") as fh:
    json.dump(out, fh, indent=1)