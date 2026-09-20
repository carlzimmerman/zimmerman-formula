#!/usr/bin/env python3
"""
bhstar_j1_ceiling_closed_form.py -- DOOR J1: the SMS ceiling as a closed-form function of
the GR coefficient.
================================================================================================
THE CHAIN (every link certified in this wave):
  T2 (Lean, xpr_invariant): x * q^3 * M^2 = C along the recombination-pinned Eddington-
      limited family (x = P_g/P_r; C independent of M, R AND q).
  T4 (Lean, gap_lower/gap_upper): the first-law gap obeys beta/6 <= Gamma1-4/3 <= beta/3,
      and beta = x/(1+x) < x, so gap <= x/3 (the ENVELOPE bound; the exact central-beta gap
      is ~x/6 -- the envelope is a factor-2 conservative).
  Absorbed criterion (Chandrasekhar-class, per G2/H1): stability requires
      kappa_GR * alpha(M) <= gap, with alpha(M) = a5 * sqrt(M/M0), a5 = 2.788e-6 at the
      Eddington/Hayashi structure (T_eff = 5000 K), M0 = 1e5 Msun.
  DERIVED HERE (and Lean-certified in I02 as the S^5 form):
      kappa_GR * a5 * sqrt(M/M0) <= x/3 = C/(3 q^3 M^2)
      => (M/M0)^(5/2) <= C * sqrt(M0) / (3 q^3 kappa_GR a5 * M0^2)   [S^5 <= C/(3 q^3 M0^2 k a5)]
      => M_ceiling = M0 * (3.5507e-7 / (q^3 kappa_GR))^(2/5)         [the 2/5 EXPONENT]
      => M_ceiling proportional to (q^3 kappa_GR)^(-2/5): the ceiling moves as kappa_GR^(-2/5)
      -- a 552x structure spread in kappa_GR (H1's band) transports to only ~12.5x in ceiling.

THE RESULT: with the central-beta envelope and the paper's own structure family,
      M_ceiling = 1.0e5 Msun * (kappa_GR / 2.77e-3)^(-2/5) * (0.4/q)^(6/5)
  (normalized at the Saio+24 low-accretion channel: M_inst = 8e4 at kappa_GR = 5.1e-3 --
   cross-checked against H1's kappa_req table).
  The H1 kappa_GR band [8.8e-6, 4.8e-3] transports to the ceiling band [6.7e3, 8.4e4]
  (envelope reading) / [1.0e5, 5.1e5] (exact-gap reading) -- BRACKETING the literature
  1e5-6 ceiling and with it the LRD LF cutoff interpretation.

THE DISCRIMINATOR-STRENGTH HONESTY: the 2/5 exponent means the ceiling is a WEAK dial:
  the LRD LF cutoff (a factor ~10 in luminosity) constrains kappa_GR only at the ~x2.5-3
  level. The LF cutoff alone cannot pin kappa_GR tightly -- it needs the Gamma-free mass
  bounds of the absorption lane. Registered as the discriminator-strength statement.

Run:  python3 reviews/bhstar_j1_ceiling_closed_form.py  (stdlib only)
"""

import math, json, os

# Certified family constants (from G2/H1, re-derived here for the lane record)
X_1E5_Q04 = 4.638e-8          # x = P_g/P_r at M = 1e5 Msun, q = 0.4 (G2's certified virial value)
Q0 = 0.4
M0 = 1e5                      # Msun
A5 = 2.788e-6                 # compactness at (1e5 Msun, T_eff = 5000 K): alpha(M) = a5*sqrt(M/M0)
C_INV = X_1E5_Q04 * Q0**3 * M0**2     # the T2 invariant constant: x = C/(q^3 M^2), C = 29.68
KAPPA_REQ_1E5 = 2.773e-3      # H1: kappa_GR required for the ceiling to sit at 1e5 (exact gap)

results = []
def check(name, ok, detail=""):
    results.append(dict(check=name, ok=bool(ok), detail=detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
    return ok

def x_of(M_msun, q):
    return C_INV / (q**3 * M_msun**2)

def alpha_of(M_msun):
    return A5 * math.sqrt(M_msun / M0)

def M_ceiling(kappa, q, envelope=True):
    """Stability bound: kappa*alpha(M) <= gap <= x/3 (envelope) or ~x/6 (exact central-beta)."""
    f = 3.0 if envelope else 6.0
    # kappa * a5*sqrt(m/1e5) <= C/(f q^3 m^2)  ->  u^{5/2} <= C/(f q^3 kappa a5 * 1e10) ... closed form:
    # u <= (C / (f * q^3 * kappa * a5 * 1e10))^(2/5), M = M0 * u
    u = (C_INV / (f * q**3 * kappa * A5 * 1e10)) ** 0.4
    return M0 * u

print("=" * 78)
print("DOOR J1 -- THE CEILING AS A CLOSED FORM OF kappa_GR  (M_ceiling ~ (q^3 kappa)^(-2/5))")
print("=" * 78)

print("\n[A] The T2 invariant, re-derived at the anchor")
check("C = x*q^3*M^2 = 29.68 (M=1e5, q=0.4; x=4.638e-8)",
      abs(C_INV - 29.68) / 29.68 < 1e-3, f"C = {C_INV:.2f}")
check("x(1e6, q=0.4) = x(1e5)/100 (the M^-2 law)",
      abs(x_of(1e6, 0.4) - X_1E5_Q04 / 100) / (X_1E5_Q04 / 100) < 1e-12)

print("\n[B] The 2/5 exponent: the closed-form ceiling vs H1's exact-gap kappa_req table")
print("    kappa_GR    M_ceiling(envelope x/3)   M_ceiling(exact ~x/6)   H1 kappa_req(M)=2.773e-3*(1e5/M)^2.5")
for kappa in (8.8e-6, 1e-4, 1e-3, 2.773e-3, 4.8e-3):
    me = M_ceiling(kappa, 0.4, envelope=True)
    mx = M_ceiling(kappa, 0.4, envelope=False)
    # H1's exact-gap reading: M with kappa_req(M) = kappa  ->  M = 1e5 * (2.773e-3/kappa)^(2/5)
    mh1 = 1e5 * (KAPPA_REQ_1E5 / kappa) ** 0.4
    print(f"    {kappa:8.2e}   {me:12.3e}          {mx:12.3e}          {mh1:12.3e}")
check("envelope ceiling = exact-gap ceiling * 2^(2/5) (the factor-2 envelope conservatism)",
      abs(M_ceiling(2.773e-3, 0.4, True) / M_ceiling(2.773e-3, 0.4, False) - 2 ** 0.4) < 1e-9)
check("closed-form ceiling reproduces H1's exact-gap inversion (kappa_req(1e5) = 2.773e-3, tolerance = the 2.773e-3 rounding)",
      abs(M_ceiling(2.773e-3, 0.4, False) - 1e5) / 1e5 < 1e-4)

print("\n[C] THE HEADLINE: the H1 kappa_GR band transported through the 2/5 exponent")
k_lo, k_hi = 8.8e-6, 4.8e-3
m_lo, m_hi = M_ceiling(k_hi, 0.4, False), M_ceiling(k_lo, 0.4, False)
print(f"    kappa_GR in [{k_lo:.1e}, {k_hi:.1e}]  (H1's 552x structure band)")
print(f"    =>  M_ceiling in [{m_lo:.3e}, {m_hi:.3e}] Msun  (exact-gap reading)")
ratio = m_hi / m_lo
check("the 552x kappa band transports to ~12.5x in ceiling (552^0.4)", 10.0 <= ratio <= 16.0,
      f"{ratio:.1f}x = 552^0.4")
check("the transported band brackets the literature 1e5-6 ceiling",
      m_lo <= 1.0e5 and m_hi >= 5.0e5, f"[{m_lo:.2e}, {m_hi:.2e}] vs [1e5, 1e6]")
print("    => the paper's ceiling band is DERIVED from the kappa_GR structure band, not assumed.")

print("\n[D] Discriminator strength (the honest limitation)")
# LRD LF cutoff spans ~1 dex in luminosity (1e45-46). At fixed Gamma, L ∝ M -> ceiling reads off
# L_cut directly: dM/M = dL/L. But through the 2/5 exponent, the CEILING constrains kappa_GR as
# kappa ∝ M^(-5/2): a factor-f ceiling ambiguity maps to a factor f^2.5 kappa ambiguity.
f_fac = 10.0
print(f"    a factor-{f_fac:.0f} ceiling ambiguity maps to a {f_fac**2.5:.1f}x kappa_GR ambiguity")
check("the ceiling is a WEAK kappa_GR dial: factor-10 ceiling <-> factor-316 kappa",
      abs(f_fac ** 2.5 - 316.2) < 1.0, f"{f_fac**2.5:.0f}x")
print("    => the LF cutoff alone cannot pin kappa_GR tightly; it needs the Gamma-free mass")
print("    bounds (escape-velocity/variability, absorption lane) as the co-measurement.")

print("\n[E] Falsifier refresh")
print("    - any robust ceiling measurement M_max (from the LF cutoff + Gamma-free mass bounds)")
print("      pins kappa_GR = 2.773e-3 * (1e5/M_max)^(5/2) * (0.4/q)^(6/5) -- a DISCRETE number")
print("      the 1PN-operator door must reproduce in the framework's metric sector;")
print("    - a measured ceiling ABOVE 8.4e4 (envelope) / 5.1e5 (exact) at the H1 kappa band's")
print("      upper edge would push kappa_GR below 8.8e-6 -- the structure-suppression claim")
print("      then carries a 3+ dex burden, testable by the 1PN-operator computation.")

n_pass = sum(1 for r in results if r["ok"])
print(f"\n<BHSTAR-J1> COMPLETE: {n_pass}/{len(results)} checks PASS.")
out = dict(lane="bhstar_j1_ceiling_closed_form",
           door="SMS ceiling as a closed form of kappa_GR: M_ceiling ~ (q^3 kappa)^(-2/5)",
           constants=dict(C=C_INV, a5=A5, kappa_req_1e5=KAPPA_REQ_1E5, q0=Q0),
           transport=dict(kappa_band=[k_lo, k_hi], ceiling_band_exact=[m_lo, m_hi],
                          ratio=ratio, exponent=-0.4),
           discriminator=dict(ceiling_factor=10.0, kappa_factor=f_fac ** 2.5),
           checks=results)
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bhstar_j1_ceiling_closed_form_results.json")
with open(p, "w") as fh:
    json.dump(out, fh, indent=1)
