#!/usr/bin/env python3
"""
NULL ROWS N1-N4: where the most precise instruments in physics measure ~zero, the
framework must PREDICT ~zero -- and does, either by computed suppression (N1, N2)
or by exact structure (N3, N4). Each row: framework prediction, measured bound
(primary-source citation), pass margin. Both footings where a0 enters.

N1 planetary ephemerides (Cassini/MESSENGER, metre-level ranging):
   The a0/2-CHANNEL SPLIT (banked, real_research/reviews/cassini_mi_evasion_2026/):
   at Saturn the framework's own nu gives nu-1 = a0/(2 g) ~ 7e-7. The ISOTROPIC (DC)
   piece rescales the effective GM_sun and is ABSORBED by the ephemeris fit -- it is
   not an observable anomaly. The observable is the ANISOTROPIC (EFE-direction) piece:
     - MG-read (phantom-field): first order in nu-1 -> Q2 ~ a0/(2 r_Sat) -- computed
       below; sits ORDERS above the Cassini bound => that reading is EXCLUDED.
     - MI-read (this framework): the inertial response keeps the Sun's field exactly
       Newtonian; the l=2 piece is SECOND order -- the committed Legendre decomposition
       gives Q2(MI) = 7.4e-34 s^-2 (cassini_mi_evasion_2026, hand-verified 2026-07-07).
   Bound: Q2 = (1.6 +/- 1.8)e-27 s^-2 (Park et al. 2026, arXiv:2602.17884; methodology
   Desmond, Hees, Famaey 2024, MNRAS 530, 1781). 2-sigma ceiling 5.2e-27 s^-2.

N2 Lunar Laser Ranging (mm-level): same split; Earth-Moon g ~ 2.7e-3 m/s^2. DC piece
   absorbed into GM_earth; observable anisotropic piece suppressed ~(a0/2g)^2.
   Bound: mm-level normal-point residuals (APOLLO: Murphy 2013, Rep. Prog. Phys. 76,
   076901), fractional range sensitivity ~ mm / 385,000 km ~ 2.6e-12.

N3 MICROSCOPE WEP: framework eta = 0 EXACTLY -- modified inertia rescales the inertial
   mass of every body by the SAME universal function of acceleration; no composition
   dependence exists in the equation. Measured: eta(Ti,Pt) = (-1.5 +/- 2.3)e-15
   (Touboul et al. 2022, PRL 129, 121102 -- final mission result).

N4 CPT / photon-sector k_AF: framework k_AF = 0 EXACTLY by structure -- the banked SME
   bridge theorem: the horizon-induced background enters only the CPT-EVEN s_munu
   (project memory: CPT-even-only theorem, 2026-06-17). Measured: |k_AF| < 1e-44 GeV
   (CMB birefringence; Kostelecky & Russell, Rev. Mod. Phys. 83, 11, 2023 data tables).
   FALSIFIED-ALTERNATIVE contrast: the natural CPT-ODD scale a horizon mechanism would
   set is hbar*H -- computed below; it sits ~2 ORDERS ABOVE the bound. A CPT-odd variant
   of this framework is already dead; the actual framework survives by structure, and
   its live CPT-EVEN coefficient (s^TX dipole) retains ~9.6x margin (Gaia DR4 front).
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
anc = json.load(open(os.path.join(HERE, "anchor_values.json")))
A0 = {"canonical": anc["a0_canon"], "alt": anc["a0_alt"]}
H0, HL = anc["H0"], anc["HL"]

GM_sun, GM_earth = 1.32712440018e20, 3.986004418e14
AU = 1.495978707e11
r_sat = 9.5826*AU
r_moon = 3.844e8
hbar = 1.054571817e-34
J_per_GeV = 1.602176634e-10

print("="*88)
print("NULL ROWS N1-N4: framework prediction vs measured bound, margin per footing")
print("="*88)

# ---------------- N1 ----------------
Q2_meas, Q2_sig = 1.6e-27, 1.8e-27
Q2_ceiling = Q2_meas + 2*Q2_sig
Q2_MI_banked = 7.4e-34            # committed Legendre l=2 result (canonical footing)
print("\nN1 PLANETARY EPHEMERIDES (Cassini Q2; Park+2026 arXiv:2602.17884):")
print(f"   bound: Q2 = ({Q2_meas:.1e} +/- {Q2_sig:.1e}) s^-2 -> 2-sigma ceiling {Q2_ceiling:.2e}")
for lab, a0 in A0.items():
    g_sat = GM_sun/r_sat**2
    nu1 = a0/(2*g_sat)                     # DC channel: absorbed into GM_sun by the fit
    Q2_MG = a0/(2*r_sat)                   # first-order anisotropic (MG/phantom read)
    Q2_MI = Q2_MI_banked*(a0/A0["canonical"])**2   # second-order scaling of the banked l=2
    print(f"   [{lab:>9}] g_Sat={g_sat:.3e}; nu-1 = a0/2g = {nu1:.2e} (DC, absorbed);")
    print(f"       MG-read  Q2 ~ a0/(2 r_Sat) = {Q2_MG:.2e} s^-2 -> "
          f"{Q2_MG/Q2_ceiling:.0f}x ABOVE ceiling ({math.log10(Q2_MG/Q2_ceiling):.1f} orders: EXCLUDED reading)")
    print(f"       MI-read  Q2 (committed l=2) = {Q2_MI:.1e} s^-2 -> "
          f"{Q2_ceiling/Q2_MI:.1e}x BELOW ceiling (PASS, ~{math.log10(Q2_ceiling/Q2_MI):.1f} orders)")
print("   => the framework's MI premise passes where the MG reading of the SAME a0 is dead")
print("      (falsified alternative). MESSENGER/INPOP metre-level ranging: the DC channel")
print("      is a GM rescale (no secular anomaly); no residual channel at current accuracy.")

# ---------------- N2 ----------------
print("\nN2 LUNAR LASER RANGING (mm-level; Murphy 2013 Rep.Prog.Phys. 76, 076901):")
frac_llr = 1e-3/r_moon
for lab, a0 in A0.items():
    g_m = GM_earth/r_moon**2
    nu1 = a0/(2*g_m)
    supp2 = nu1**2                          # observable anisotropic channel, second order
    print(f"   [{lab:>9}] g={g_m:.3e}; DC nu-1 = {nu1:.2e} (absorbed into GM_earth);")
    print(f"       observable MI channel ~ (a0/2g)^2 = {supp2:.1e} fractional vs LLR "
          f"sensitivity {frac_llr:.1e} -> {frac_llr/supp2:.0f}x margin "
          f"({math.log10(frac_llr/supp2):.1f} orders, PASS)")

# ---------------- N3 ----------------
eta, seta = -1.5e-15, 2.3e-15
print("\nN3 MICROSCOPE WEP (Touboul+2022 PRL 129, 121102, final):")
print(f"   framework: eta = 0 EXACTLY (universal inertia rescaling; zero composition channel)")
print(f"   measured:  eta(Ti,Pt) = ({eta:.1e} +/- {seta:.1e})")
print(f"   pass: prediction sits {abs(0-eta)/seta:.2f} sigma from the measurement (PASS).")
print(f"   a0-independent: holds on BOTH footings identically (structure, not scale).")

# ---------------- N4 ----------------
kAF_bound = 1e-44
for lab, H in [("canonical (H_Lambda)", HL), ("alt (H0)", H0)]:
    kodd = hbar*H/J_per_GeV
    print(f"\nN4 CPT / k_AF ({lab}):" if lab.startswith("can") else f"   [{lab}]:", end=" ")
    if lab.startswith("can"):
        print()
        print(f"   framework: k_AF = 0 EXACTLY (SME bridge: CPT-even s_munu only, banked theorem)")
        print(f"   bound: |k_AF| < {kAF_bound:.0e} GeV (Kostelecky-Russell RMP 83, 11, 2023 tables)")
        print(f"   [{lab}]:", end=" ")
    print(f"natural CPT-odd scale hbar*H = {kodd:.2e} GeV = {kodd/kAF_bound:.0f}x ABOVE the bound")
print("   => a CPT-ODD horizon variant is excluded by ~2 orders; the framework's exact")
print("      zero passes by structure. Its live CPT-EVEN coefficient s^TX keeps ~9.6x")
print("      margin (banked SME front; Gaia DR4). Real falsified-alternative content:")
print("      the null is not vacuous -- the nearest sibling theory fails it.")

print("\n" + "="*88)
print("NULL SUMMARY: N1 PASS (~6.8-7 orders, MI-read; MG-read of same a0 excluded ~3.8")
print("orders -- the split is the framework's content); N2 PASS (~4 orders); N3 PASS")
print("(exact 0, 0.65 sigma); N4 PASS (exact 0 by structure; CPT-odd sibling dead ~2 orders).")
