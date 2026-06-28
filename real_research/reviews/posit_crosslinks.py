#!/usr/bin/env python3
r"""
posit_crosslinks.py  --  CLASS D: CROSS-LINK POSITS (both-ways, NOT a TOE)
================================================================================
Each posit JOINS two ALREADY-ESTABLISHED framework consequences into a NEW joint
prediction that is HARDER TO FAKE than either piece alone. Nothing here is a new
derivation; every piece is taken from a committed script, and the NEW content is
only the LINK.

Framework (its OWN premises, reasoned from first):
  inertia = nonlocal-in-time RESPONSE to the de Sitter cosmic-horizon Unruh bath;
  ONE bath clock H_Lambda; a0 = c H_Lambda / Z = 9.36e-11 m/s^2, Z = sqrt(32 pi/3);
  E_L = rho_DE^(1/4) = 2.2395 meV (the SAME rho_DE that sets a0);
  a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0));   dS-Unruh nu: g_obs = sqrt(g_N^2 + g_N a0).

TWO FOOTING BRANCHES for a0(z) (run BOTH, show the spread -- working-rule fork):
  (A) DECLINING  a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0)    [Theory-of-Gravity, canonical]
  (B) RISING     a0(z)/a0(0) = E(z) = H(z)/H0             [scaling-MOND paper reading]
These DISAGREE by a factor ~6 at z=3 -- which is the whole point of D4.

Established pieces this script re-uses (each from a committed sibling script):
  * EFE-vs-z transition-regime offset .............. efe_vs_z_recompute.py
  * dwarf non-adiabatic sigma-boost (plunge hotter)  dwarf_ecc_sigma_pilot_analysis.py
  * cluster-member relational sigma-spread (MI 6-13%, MG=0)  member_sigma_efe_signtest_v2.py
  * a0(z) DESI propagation (declining branch) ...... a0z_desi_chains_propagation.py
  * BTFR zero-point M_bar = v^4/(G a0) ............. btfr_honest.py / btfr_evolution_confound.py

NO git push. Both-ways. FDR-guard any coincidence (none claimed numeric here).
C. Zimmerman corpus, 2026-06-27. numpy only.
================================================================================
"""
import numpy as np

# ---- sealed footing ---------------------------------------------------------
A0   = 9.36e-11                 # m/s^2, c H_Lambda / Z, pure-Lambda de Sitter
Om, OL = 0.315, 0.685
W0, WA = -0.752, -0.86          # DESI DR2 CPL central (declining branch)

def E(z):                       # H(z)/H0  (RISING branch)
    return np.sqrt(Om*(1+z)**3 + OL)

def rho_de_ratio(z, w0=W0, wa=WA):     # rho_DE(z)/rho_DE0 for CPL
    a = 1.0/(1.0+z)
    return (1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*(1-a))

def a0_decl(z):  return np.sqrt(rho_de_ratio(z))   # branch A: a0(z)/a0(0)
def a0_rise(z):  return E(z)                        # branch B: a0(z)/a0(0)

def nu(y):       return np.sqrt(1.0 + 1.0/y)        # framework boost g_obs = nu(g_N/a0) g_N

SEP = "="*84

# ============================================================================
# D1 -- EFE x a0(z): does the external-field offset STRENGTHEN with z, jointly
#       testable with high-z kinematics?
# ============================================================================
def D1():
    print(SEP); print("D1  EFE x a0(z)  --  the z-DEPENDENT external-field offset"); print(SEP)
    print("""  PIECE 1 (efe_vs_z_recompute.py): in PURE deep-MOND the EFE offset is a0-INDEPENDENT
            (it saturates to g_ext/g_N), so the naive 'eta=g_ext/a0 grows +36%' story is WRONG.
  PIECE 2 (a0(z) branches): a0 evolves with z.
  THE LINK (new): the EFE offset carries a0(z) ONLY for TRANSITION-regime galaxies
            (g_N ~ a0, g_ext ~ a0). There the offset is neither saturated nor Newtonian, so
            d(offset)/d ln a0 != 0. JOINT prediction = a SPECIFIC, SIGNED z-trend that appears
            in transition galaxies and VANISHES in deep-MOND ones -- a within-sample contrast a
            pure-a0(z) or pure-EFE story cannot fake.""")
    def offset(gN, ge, a0abs):
        D_iso = nu(gN/a0abs)
        D_emb = (nu((gN+ge)/a0abs)*(gN+ge) - nu(ge/a0abs)*ge)/gN
        return np.log10(D_iso/D_emb)
    # two galaxy classes at the SAME external field
    deep = (0.02*A0, 0.05*A0)     # g_N, g_e  both << a0  -> saturated, a0-blind
    tran = (0.7*A0,  1.0*A0)      # transition: g_N ~ a0, MW-like field
    print(f"  {'z':>4} | {'a0/a0_0 (A decl / B rise)':>26} | {'DEEP off [dex]':>15} | {'TRANS off [dex]':>16}")
    base_d_A = offset(*deep, A0*a0_decl(0)); base_t_A = offset(*tran, A0*a0_decl(0))
    base_d_B = offset(*deep, A0*a0_rise(0)); base_t_B = offset(*tran, A0*a0_rise(0))
    for z in (0,1,2,3):
        odA = offset(*deep, A0*a0_decl(z)); otA = offset(*tran, A0*a0_decl(z))
        odB = offset(*deep, A0*a0_rise(z)); otB = offset(*tran, A0*a0_rise(z))
        print(f"  {z:>4} | {a0_decl(z):>11.3f} / {a0_rise(z):>10.3f} | "
              f"{odA:+.4f}/{odB:+.4f} | {otA:+.4f}/{otB:+.4f}")
    # the discriminating CONTRAST: trans z-shift minus deep z-shift (the a0-blind baseline)
    dT_A = offset(*tran, A0*a0_decl(3)) - base_t_A; dD_A = offset(*deep, A0*a0_decl(3)) - base_d_A
    dT_B = offset(*tran, A0*a0_rise(3)) - base_t_B; dD_B = offset(*deep, A0*a0_rise(3)) - base_d_B
    print(f"\n  CONTRAST (z=0->3, transition MINUS deep-MOND z-shift):")
    print(f"     branch A (declining): {dT_A - dD_A:+.4f} dex   [deep baseline shift {dD_A:+.4f}]")
    print(f"     branch B (rising)   : {dT_B - dD_B:+.4f} dex   [deep baseline shift {dD_B:+.4f}]")
    print(f"     => the SIGN of this contrast FLIPS between branches "
          f"({'A<0,B>0' if (dT_A-dD_A)<0<(dT_B-dD_B) else 'check'}): "
          "transition galaxies get MORE-quenched at high z if a0 RISES, LESS if a0 DECLINES.")
    print("""  TEST: high-z (z~1-2) resolved rotation curves (JWST/ALMA), split by environment density
        into 'isolated/deep-MOND' vs 'grouped/transition'. Measure the EFE offset in EACH bin and
        its z-trend. A pure-a0(z) story predicts a UNIFORM shift; a pure-EFE story predicts NO
        z-trend; only THIS link predicts a z-trend CONCENTRATED in the transition bin, with a
        branch-diagnostic SIGN. Harder to fake: needs the right magnitude AND the right
        deep-vs-transition contrast AND the right sign together.
  GRADE: HYPOTHESIS-WITH-FREE-KNOB (the transition-regime offset is FORCED by the framework's nu,
        but which galaxies sit in transition at high z is a sample/selection knob; size ~0.01-0.05 dex
        is small vs current high-z RC errors).""")
    return dict(contrast_A=dT_A-dD_A, contrast_B=dT_B-dD_B)

# ============================================================================
# D2 -- cluster relational sigma-spread x a0(z): a REDSHIFT-dependent spread
# ============================================================================
def D2():
    print("\n"+SEP); print("D2  cluster relational sigma-spread x a0(z)  --  z-evolving spread"); print(SEP)
    print("""  PIECE 1 (member_sigma_efe_signtest_v2.py): the MI-DISTINCTIVE observable in clusters is the
            NON-ADIABATIC relational sigma-SPREAD among members at fixed g_ext -- MI predicts a 6-13%
            spread, MG predicts EXACTLY 0 (MG's EFE is instantaneous, single-valued).
  PIECE 2 (a0(z)): the deep-MOND boost amplitude scales with a0.
  THE LINK (new): the relational spread is a fraction of the deep-MOND boost; that boost scales as
            sqrt(a0). So the spread amplitude should track sqrt(a0(z)) -- the SAME cluster population
            at higher z shows a LARGER or SMALLER % spread depending on the branch. Because MG keeps
            the spread at 0 at ALL z, ANY non-zero z-trend in the spread is doubly MG-impossible.""")
    spread0 = np.array([0.06, 0.13])     # MI relational spread today (lo,hi), from sign-test script
    print(f"  {'z':>4} | {'sqrt(a0/a0_0) A/B':>20} | {'MI spread%% A (lo-hi)':>22} | {'MI spread%% B (lo-hi)':>22} | MG")
    for z in (0,0.5,1,2):
        fa = np.sqrt(a0_decl(z)); fb = np.sqrt(a0_rise(z))
        sA = spread0*fa*100; sB = spread0*fb*100
        print(f"  {z:>4} | {fa:>9.3f}/{fb:>9.3f} | {sA[0]:>9.2f}-{sA[1]:<9.2f} | "
              f"{sB[0]:>9.2f}-{sB[1]:<9.2f} | 0.00")
    print("""  TEST: resolved internal sigma of diffuse cluster members (MUSE/4MOST/JWST) in a LOW-z and a
        z~1 cluster sample; measure the member-to-member spread at fixed g_ext/a0. Branch B predicts
        the z~1 spread is ~1.7x the local one; branch A predicts ~1.0x (nearly flat to z~1, then
        declining). MG predicts 0 at every z. Harder to fake: a spread is already MG-impossible; a
        SIGNED z-trend in that spread cannot come from any single-valued-EFE theory at all.
  GRADE: HYPOTHESIS-WITH-FREE-KNOB (the sqrt(a0) scaling of the boost is forced; the FRACTION of the
        boost that shows up as relational spread is theta(y)-hostage at the ~factor-2 level, so the
        absolute % is a free knob -- but the z-RATIO within a branch is much cleaner than the % itself).""")
    return dict(spreadB_z1=spread0*np.sqrt(a0_rise(1.0)))

# ============================================================================
# D3 -- bath CLOCK (memory kernel) x dwarf eccentricity x a0(z): triple link
# ============================================================================
def D3():
    print("\n"+SEP); print("D3  bath CLOCK x dwarf eccentricity x a0(z)  --  TRIPLE link"); print(SEP)
    print("""  PIECE 1 (freefall_clock_*): inertia is a nonlocal-in-time RESPONSE with ONE bath clock H_Lambda;
            the memory kernel's timescale is ~1/H_Lambda (the de Sitter horizon clock).
  PIECE 2 (dwarf_ecc_sigma_pilot_analysis.py): a radial-PLUNGE MW dwarf runs ~19-28% HOTTER than a
            circular one at fixed pericenter+mass (sign = theorem; the non-adiabatic-inertia signal).
  PIECE 3 (a0(z)): a0 evolves; the bath clock H_Lambda(z) sets BOTH a0(z) AND the kernel timescale.
  THE LINK (new): the SAME clock H_Lambda that sets a0 sets the memory timescale tau ~ 1/H_Lambda. So
            the non-adiabatic boost depends on the ratio (orbital crossing time)/(memory time) ~
            T_orb * H_Lambda. For a dwarf that fell in at look-back z_inf, the memory it carries was
            laid down when the bath clock was H_Lambda(z_inf). The eccentricity-sigma boost should
            therefore scale with the bath state AT INFALL, not today -- a per-dwarf, infall-time-stamped
            prediction. This ties the dwarf's ORBITAL HISTORY to the COSMIC a0(z) history through ONE clock.""")
    # bath-clock ratio at infall epoch: tau(z)/tau(0) = H_Lam(0)/H_Lam(z).
    # canonical (declining a0): H_Lam ~ sqrt(rho_DE) -> tau lengthens at high z (clock SLOWER in past).
    # rising branch: H_Lam ~ H(z) -> tau SHORTENS at high z (clock FASTER in past).
    print(f"  {'z_infall':>9} | {'tau(z)/tau(0)  A (decl)':>24} | {'tau(z)/tau(0)  B (rise)':>24}")
    for z in (0,1,2,3):
        tauA = 1.0/a0_decl(z)     # tau ~ 1/H_Lam ~ 1/(a0/a0_0)
        tauB = 1.0/a0_rise(z)
        print(f"  {z:>9} | {tauA:>24.3f} | {tauB:>24.3f}")
    print("""  CONSEQUENCE: dwarfs that plunged in EARLY (high z_infall) carry a memory laid down under a
        DIFFERENT bath clock. In branch A the past clock was SLOWER (longer memory tau) -> early-infall
        plungers are EVEN HOTTER than today's clock would give. In branch B the opposite. So the
        ecc-sigma correlation should acquire a SECONDARY dependence on INFALL REDSHIFT, branch-signed.
  TEST: Gaia DR4 dwarf orbits give pericenter + eccentricity AND (via backward integration in a MW+LMC
        potential) an infall-time estimate. Partial-correlate residual internal-sigma against
        eccentricity AT FIXED pericenter+mass, THEN look for a residual dependence on infall epoch. MG
        has instantaneous EFE -> ZERO ecc-correlation AND zero infall-epoch dependence: doubly impossible.
  GRADE: SPECULATIVE (the kernel timescale ~1/H_Lambda is plausible but the EXACT memory-kernel shape is
        not pinned -- freefall_clock_rigor_audit flagged the kernel as a steelman, not a theorem; the
        infall-epoch stamp is the weakest, most model-dependent of the four. Honest grade: a real but
        fragile triple link. Underpowered now -- the base ecc-sigma pilot is already NULL-but-UNDERPOWERED.)""")
    return dict(tauA_z3=1.0/a0_decl(3), tauB_z3=1.0/a0_rise(3))

# ============================================================================
# D4 -- BTFR zero-point x a0(z) as a w(z)-INDEPENDENT a0(z) probe
#       (the cleaner a0(z) test the memory flagged as needed)
# ============================================================================
def D4():
    print("\n"+SEP); print("D4  BTFR zero-point x a0(z)  --  a w(z)-INDEPENDENT direct a0(z) probe"); print(SEP)
    print("""  PIECE 1 (btfr_honest.py): the deep-MOND BTFR is M_bar = v_flat^4 / (G a0). The ZERO-POINT
            (intercept at fixed v_flat) is set DIRECTLY by a0 -- it MEASURES a0, it does not assume it.
  PIECE 2 (a0(z) branches): a0(z) is predicted two ways that DISAGREE by ~6x at z=3.
  THE LINK (new -- the memory flagged this as the needed cleaner test): because the BTFR zero-point
            measures a0 KINEMATICALLY (from v_flat and M_bar), it is a probe of a0(z) that does NOT
            route through rho_DE(z) or any w(z) model. It is therefore w(z)-INDEPENDENT: it cannot be
            'dissolved if DESI converges to w=-1' the way the rho_DE-propagated a0(z) can. The two
            branches predict OPPOSITE zero-point shifts, so a single clean high-z BTFR zero-point picks
            the branch (or kills both).""")
    G = 6.674e-11
    # zero-point shift at fixed v_flat: M_bar ∝ 1/a0(z). delta log10 M_bar = -log10(a0(z)/a0_0).
    print(f"  {'z':>4} | {'a0/a0_0 A/B':>18} | {'dlog10 M_bar(fixed v)  A':>26} | {'B':>10}")
    for z in (0,0.9,1,2,2.3,3):
        dA = -np.log10(a0_decl(z)); dB = -np.log10(a0_rise(z))
        print(f"  {z:>4} | {a0_decl(z):>8.3f}/{a0_rise(z):>8.3f} | {dA:>+26.3f} | {dB:>+10.3f}")
    # the KMOS3D anchor: Ubler+2017 measured z=2.3 vs z=0.9 zero-point RISES; the framework branches:
    sA = -np.log10(a0_decl(2.3)/a0_decl(0.9))
    sB = -np.log10(a0_rise(2.3)/a0_rise(0.9))
    print(f"""
  ANCHOR (btfr_evolution_confound.py): KMOS3D (Ubler+2017) baryonic-TFR zero-point z=0.9->2.3.
     branch A predicts the a0-only zero-point shift = {sA:+.3f} dex (RISE)
     branch B predicts                              = {sB:+.3f} dex (DROP)
     The OBSERVED baryonic zero-point RISES -- which NAIVELY favours branch A. BUT (both-ways, loud):
     the observed rise is GAS-FRACTION confounded (M_bar = M_star + M_gas, gas climbs with z), so the
     raw zero-point is NOT a clean a0 probe TODAY. The link is only clean with a PER-GALAXY GAS CENSUS
     that removes the confound -- exactly what the confound script concluded is the needed measurement.""")
    print("""  WHY HARDER TO FAKE than either piece alone:
     * vs the rho_DE-propagated a0(z): D4 does NOT use w(z) at all, so it survives w->-1 (the hostage
       that kills the rho_DE route). It is the w(z)-INDEPENDENT cross-check.
     * vs a raw BTFR-evolution claim: the SIGN is branch-diagnostic, and the gas confound is the ONE
       thing the joint test must (and can) control with resolved gas masses -- a falsifiable, scoped ask.
  TEST: high-z (z~1-3) deep-MOND-tail rotation curves with PER-GALAXY HI/H2 gas census (ALMA+JWST);
        fit the BTFR zero-point with v_flat and M_bar measured independently; compare the gas-corrected
        zero-point shift to branch A (+) vs branch B (-).
  GRADE: HYPOTHESIS-WITH-FREE-KNOB (the M_bar = v^4/G a0 zero-point is FORCED in deep-MOND, and the
        w(z)-independence is a genuine structural advantage; the FREE KNOB is the gas-fraction correction,
        which currently dominates and must be measured per-galaxy before the a0(z) signal is clean).""")
    return dict(shift_A_0p9_2p3=sA, shift_B_0p9_2p3=sB)

# ============================================================================
def main():
    print("#"*84)
    print("# CLASS D CROSS-LINK POSITS  --  de Sitter-Unruh modified inertia (a0 = cH_L/Z)")
    print("# both-ways; NOT a TOE; every piece from a committed sibling script; NO push")
    print("#"*84)
    r1 = D1(); r2 = D2(); r3 = D3(); r4 = D4()
    print("\n"+SEP); print("SUMMARY -- the four cross-links, ranked by 'harder-to-fake'"); print(SEP)
    print(f"""  D4 (BTFR zero-point x a0(z)) -- CRISPIEST cross-link: w(z)-INDEPENDENT, branch-SIGNED,
        survives w->-1; the one clean a0(z) probe the memory flagged as needed. Free knob = gas census.
        branch-A vs branch-B predicted z=0.9->2.3 zero-point shift: {r4['shift_A_0p9_2p3']:+.3f} vs {r4['shift_B_0p9_2p3']:+.3f} dex.
  D1 (EFE x a0(z)) -- a within-sample deep-vs-transition CONTRAST with a branch-flipping sign
        (A {r1['contrast_A']:+.4f} dex, B {r1['contrast_B']:+.4f} dex); small but uniquely shaped.
  D2 (cluster spread x a0(z)) -- a z-evolving MG-IMPOSSIBLE spread (branch B z~1 ~1.7x local).
  D3 (clock x dwarf ecc x a0(z)) -- the most distinctive (doubly MG-impossible) but most fragile
        (kernel-shape + infall-epoch dependent); honestly SPECULATIVE and underpowered now.
  All four LINK the SAME a0(z) into a second observable, so a consistent branch must show up in ALL of
  them -- a joint constraint no single front delivers. NEVER 'no doors': these are new, testable links.""")
    print("#"*84)
    print("# posit_crosslinks.py complete -- exit 0")
    print("#"*84)

if __name__ == "__main__":
    main()
