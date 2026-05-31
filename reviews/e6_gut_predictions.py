#!/usr/bin/env python3
"""
Model-building step 3: the rest of the SUSY-GUT package on (T^2)^3/(Z2xZ2).
==========================================================================

Three more standard, REAL predictions the E6 (-> SO(10)) SUSY GUT makes -- all
INHERITED from being a SUSY GUT, none distinctive to this framework, but all real:

  (1) proton decay rate (dim-6, X/Y gauge-boson exchange);
  (2) b-tau Yukawa unification (m_b = m_tau at M_GUT -> m_b/m_tau at low energy);
  (3) neutrino seesaw from the nu^c automatically present in the SO(10) 16.

We compute each and compare to data, honestly.

Pure stdlib.  Run:  python reviews/e6_gut_predictions.py
"""

import math

M_GUT = 2.3e16       # GeV, from reviews/e6_gauge_unification.py
ALPHA_GUT = 1 / 24.3
M_P = 0.938          # GeV, proton mass


def part1_proton_decay():
    print("=" * 78)
    print("(1) Proton decay  p -> e+ pi0  (dim-6, X/Y gauge boson exchange)")
    print("=" * 78)
    # tau ~ (1/alpha_GUT^2) * M_X^4 / (m_p^5) / |matrix element|^2
    # Use the standard calibrated estimate: for M_X=2e16, alpha_GUT~1/24,
    # tau(p->e+pi0) ~ few x 10^36 yr. Scale from a reference point.
    M_X = M_GUT
    tau_ref = 1.0e36                       # yr at M_X=1e16, alpha_GUT=1/24 (order of mag)
    tau = tau_ref * (M_X / 1e16) ** 4 * (1 / 24) ** 2 / ALPHA_GUT ** 2
    print(f"   M_X ~ M_GUT = {M_X:.1e} GeV,  alpha_GUT ~ 1/{1/ALPHA_GUT:.0f}")
    print(f"   tau(p->e+ pi0) ~ {tau:.0e} yr   (order-of-magnitude; matrix-element ~x3)")
    print(f"   Super-Kamiokande bound:   tau > 2.4e34 yr   -> PREDICTION SAFE (above bound)")
    print(f"   Hyper-Kamiokande reach:   ~1e35 yr          -> mostly BEYOND near-term reach")
    print("   HONEST TENSION: in *minimal* SUSY GUTs the faster dim-5 mode p -> nu-bar K+")
    print("   (Higgsino exchange) is often ALREADY EXCLUDED -- a real problem requiring")
    print("   model-building (split multiplets / suppression). So proton decay is both a")
    print("   genuine prediction and a genuine constraint.\n")


def part2_b_tau():
    print("=" * 78)
    print("(2) b-tau Yukawa unification:  m_b = m_tau at M_GUT")
    print("=" * 78)
    # QCD enhancement of m_b relative to m_tau (which feels no QCD):
    #   m(mu)/m(M) = [alpha_s(mu)/alpha_s(M)]^(12/(33-2 nf))
    a_s_mb = 0.22       # alpha_s(m_b)
    a_s_GUT = ALPHA_GUT  # alpha_3(M_GUT) = alpha_GUT
    nf = 5
    expo = 12 / (33 - 2 * nf)
    qcd_factor = (a_s_mb / a_s_GUT) ** expo
    mb_over_mtau_pred = qcd_factor          # since m_b=m_tau at GUT, m_tau ~ unchanged
    mb_meas, mtau_meas = 4.18, 1.777
    ratio_meas = mb_meas / mtau_meas
    print(f"   QCD enhancement [alpha_s(m_b)/alpha_s(M_GUT)]^(12/23) = {qcd_factor:.2f}")
    print(f"   predicted m_b/m_tau (low energy) ~ {mb_over_mtau_pred:.2f}")
    print(f"   measured  m_b/m_tau = {mb_meas}/{mtau_meas} = {ratio_meas:.2f}")
    print(f"   agreement: {abs(mb_over_mtau_pred-ratio_meas)/ratio_meas*100:.0f}%  -- real success (3rd generation).")
    print("   CAVEATS: depends on alpha_s, the SUSY spectrum, and tan(beta); the first")
    print("   two generations need Georgi-Jarlskog factors (m_mu/m_e etc.). Third-gen")
    print("   b-tau unification is the clean, working case.\n")


def part3_seesaw():
    print("=" * 78)
    print("(3) Neutrino seesaw from the nu^c in the SO(10) 16")
    print("=" * 78)
    print("   The 16 of SO(10) automatically contains a right-handed neutrino nu^c.")
    print("   Type-I seesaw:  m_nu ~ m_D^2 / M_R,  with m_D ~ EW (Dirac, ~ up-type in")
    print("   SO(10)) and M_R the heavy Majorana scale.\n")
    m_D = 100.0          # GeV (third-gen Dirac, ~ top-like in SO(10))
    print(f"   {'M_R [GeV]':>12} | {'m_nu [eV]':>12}")
    for M_R in (1e13, 1e14, 1e15, 1e16):
        m_nu_GeV = m_D ** 2 / M_R
        m_nu_eV = m_nu_GeV * 1e9
        print(f"   {M_R:>12.0e} | {m_nu_eV:>12.3f}")
    print(f"\n   measured scale (atmospheric):  sqrt(Dm^2_atm) ~ 0.05 eV")
    print("   => M_R ~ 1e14-1e15 GeV (intermediate / GUT-ish) gives m_nu ~ 0.01-0.1 eV,")
    print("      the right ballpark. A genuine order-of-magnitude success of SO(10)/E6.")
    print("   CAVEAT: M_R is a free scale (the success is that the NATURAL value -- near")
    print("   the GUT/intermediate scale -- lands in the right range), not a sharp prediction.\n")


def main():
    part1_proton_decay()
    part2_b_tau()
    part3_seesaw()
    print("=" * 78)
    print("VERDICT")
    print("=" * 78)
    print("  All three are REAL and (mostly) WORK:")
    print("   * b-tau unification: m_b/m_tau ~ 2.4 vs measured 2.35 (3rd gen). Success.")
    print("   * seesaw: nu^c is automatic; M_R ~ 1e14-15 -> m_nu ~ 0.05 eV. Success.")
    print("   * proton decay: dim-6 tau ~ 1e36 yr (safe); dim-5 is a real tension.")
    print()
    print("  BUT all three are INHERITED from being a SUSY SO(10)/E6 GUT -- they are the")
    print("  standard package, identical for any such model, NOT distinctive to this")
    print("  framework. Combined with gauge unification + sin^2(theta_W) (step 2), the")
    print("  honest status is: the construction IS a legitimate SUSY GUT, and it earns the")
    print("  standard SUSY-GUT scorecard -- real successes (unification, sin^2, b-tau,")
    print("  seesaw) and real tensions (dim-5 proton decay, SUSY unseen at the LHC).")
    print()
    print("  The framework gains credibility by BEING a real SUSY GUT. It gains nothing")
    print("  DISTINCTIVE here -- the only distinctive, framework-specific prediction")
    print("  remains the evolving-a0 cosmology, which no GUT makes.")


if __name__ == "__main__":
    main()
