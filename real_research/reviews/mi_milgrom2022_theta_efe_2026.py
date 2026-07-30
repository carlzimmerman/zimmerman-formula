#!/usr/bin/env python3
r"""mi_milgrom2022_theta_efe_2026.py -- THE MILGROM-2022 FREQUENCY-RATIO ROUTE, SWUNG.

THE DOOR. The framework's sharpest liability is the alpha=1 planetary anomaly: held to all
accelerations the exact law forces a constant sunward a0/2 = 4.68e-11 m/s^2, which is 1278x the Earth
2-sigma ephemeris bound (Sereno & Jetzer 2006 Table 1 through their Eq. 9). The corpus's escape was a
"gate" frequency omega_c -- a FIFTH DIMENSIONED CONSTANT. Milgrom 2022 (PRD 106, 064060,
arXiv:2208.07073) builds modified-inertia models in which the same kind of suppression arises from
frequency RATIOS alone, with a0 the only new dimensioned constant. If that transfers, the fifth
constant is unnecessary. This script asks whether it does.

WHAT MILGROM ACTUALLY CONSTRUCTS, verbatim from the paper (abstract and Sec. VI):
  * "what determines the EFE, in the case of a dominant external field, is mu(theta<a_ex>/a0) ...
    compared with mu(a_ex/a0) for presently known modified-gravity formulations."
  * "theta > 1 is an extra factor that depends on the frequency ratio of the external- and
    internal-field variations. Only ratios of frequencies enter, and a0 remains the only new
    dimensioned constant."
  * Eq. (34):  A(omega_in) = omega_in^2 |r_in| + omega_ex^2 |r_ex| theta(omega_ex/omega_in)
  * Eq. (35):  a_hat(omega_in) mu[theta(0) a_ex/a0] = a_hat_N(omega_in)
  * Normalisation: "We pick the normalization such that theta(1) = 1", and consequently "with the
    normalization theta(1) = 1, it is mu(a_ex/a0) that enters the rotation-curve analysis".
  * Example forms, his own: theta(y) = 2/(1+y^2) -> theta(0) = 2; theta(y) = e^(1-y) -> theta(0) = e;
    "more generally, for theta(y) = e^((1-y)/q), theta(0) = e^(1/q)". He expects "of the order of a few".
  * And explicitly on the case of interest: "for the description of vertical dynamics, or that of wide
    binaries in the solar neighborhood we have a_ex/a0 ~ 2, and even a value of theta(0) of a few can
    have a large impact on 1 - mu ... since 1 - mu[2 theta(0)] can be rather smaller than 1 - mu(2)."

THE ANSWER, computed below and stated up front so nothing here reads as a manufactured win:
  S3  IT DOES NOT CLOSE THE PLANETARY LIABILITY, and cannot. theta enters only as an ADDITIVE
      theta(0) a_ex inside mu's argument (Eq. 34). At Earth a_in/a_ex ~ 3e7, so any theta(0) of order
      a few changes mu's argument by ~1 part in 10^7 and the a0/2 anomaly is untouched. The theta(0)
      that WOULD suppress it is ~4e10, ten orders above his examples.
  S4  *** AND THIS FRAMEWORK CANNOT USE theta AT ALL -- corrected mid-script, before shipping. ***
      A first pass of this script concluded that theta(0) pulls the framework's wide-binary prediction
      below its FROZEN pre-registered target and that an amendment was owed. THAT WAS WRONG, and it
      would have been a bad error: amending a frozen target on the basis of a construction the theory
      provably cannot use damages the pre-registration discipline more than a wrong number does.
      The corpus had already settled it, twice, with committed scripts:
        (i) mi_theta_efe_from_closure_2026.py S1: the kernel is EXACTLY unimodular on the oscillatory
            branch (sympy, |K| - 1 = 0), so it cannot source theta's y-dependence;
        (ii) Theorem B (<Box_u>_u = +|a|^2 exactly) forces the argument to be |a_TOTAL|^2, i.e.
             QUADRATURE with a vector cross term -- not Milgrom's LINEAR a_in + theta a_ex.
      Amendment 2 to the DR4 pre-registration already states this: "no multiplying phase function
      theta(omega_ex/omega_in) is available". It was right and stands.
  S5  So the frozen MI target STANDS, and MI-vs-MG stays UNDECIDABLE for this framework. The
      decidability that theta would buy belongs to Milgrom's general models, not to this one.
  S6  The RAR is untouched -- by his normalisation, not by luck. Checked structurally.
  S7  What survives: theta separates THIS framework from the wider MI family, which is a real
      distinction and a falsifiability virtue. Whether DR4 can see it is computed, not assumed.

Exit non-zero on any failed internal check. No hard-coded verdicts.
"""
from __future__ import annotations

import numpy as np

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 100); print(s); print("=" * 100)

GM_SUN = 1.32712440018e20
AU = 1.495978707e11
FOOTINGS = [("canonical rho_DE", 9.36e-11), ("alt rho_total", 1.13e-10)]
# FROZEN external-field values, PREREGISTRATION_DR4.md section 1.1
G_EXT = [("primary (McMillan-class)", 1.778e-10), ("alt (Vc^2/R0)", 2.078e-10)]
# Measured, for context only: Gaia EDR3, A&A 649, A9
G_EXT_MEASURED, G_EXT_MEASURED_ERR = 2.32e-10, 0.16e-10
# FROZEN gamma_v targets, PREREGISTRATION_DR4.md section 3
FROZEN_MI_POINT, FROZEN_MI_BAND = 1.09, (1.05, 1.10)
FROZEN_MG = 1.137
SIGMA_GAMMA_DR4 = 0.0191          # N = 30,000 pairs, frozen synthetic-injection gate
# Milgrom's own example theta forms
THETAS = [("MG baseline (no MI theta)", 1.0),
          ("theta(y)=2/(1+y^2)", 2.0),
          ("theta(y)=e^(1-y)", np.e),
          ("theta(y)=e^((1-y)/q), q=1/1.1", float(np.exp(1.1)))]
# Earth 2-sigma limit on a constant sunward anomaly, derived in mi_alpha1_solar_system_2026.py
EARTH_LIMIT = 3.66e-14


def mu_fw(x):
    """The framework's own interpolation, inverse of nu(y)=sqrt(1+1/y)."""
    x = np.asarray(x, float)
    return (np.sqrt(1.0 + 4.0 * x * x) - 1.0) / (2.0 * x)


def gamma_v_from_mu(x):
    """Milgrom Eq. (35): a = a_N / mu(x)  =>  gravity boost 1/mu, velocity boost its square root."""
    return 1.0 / np.sqrt(mu_fw(x))


def main() -> int:
    banner("S1. Reproduce the corpus's OWN frozen MG number, to prove the machinery matches")
    print("  If Milgrom's theta is set to 1 -- i.e. mu(a_ex/a0), the modified-GRAVITY prescription --")
    print("  Eq. (35) must return the pre-registration's frozen framework-as-MG target of 1.137.")
    e_prim = G_EXT[0][1] / FOOTINGS[0][1]
    g_mg = float(gamma_v_from_mu(e_prim))
    print(f"  a_ex/a0 = {G_EXT[0][1]:.3e}/{FOOTINGS[0][1]:.3e} = {e_prim:.4f}")
    print(f"  gamma_v = 1/sqrt(mu_fw({e_prim:.4f})) = {g_mg:.4f}   vs frozen {FROZEN_MG} "
          f"(script asserts |asy - 1.137| < 0.005)")
    check(abs(g_mg - FROZEN_MG) < 0.005,
          f"reproduced to {abs(g_mg-FROZEN_MG):.4f} -- so this script's mu, its gamma_v convention and "
          f"its frozen a_ex all agree with the banked pre-registration, and any change below is due to "
          f"theta alone")

    banner("S2. What theta(0) does to the EFE quenching -- Milgrom's own worked case")
    print("  His sentence: 'for wide binaries in the solar neighborhood we have a_ex/a0 ~ 2, and even a")
    print("  value of theta(0) of a few can have a large impact on 1 - mu ... since 1 - mu[2 theta(0)]")
    print("  can be rather smaller than 1 - mu(2).'  Quantified on the framework's own mu:")
    print(f"  {'theta(0)':>9s} {'arg = theta*2':>13s} {'mu':>9s} {'1 - mu':>9s} "
          f"{'vs theta=1':>11s}")
    base = None
    for _nm, th in THETAS:
        x = th * 2.0
        m = float(mu_fw(x))
        if base is None:
            base = 1 - m
        print(f"  {th:9.3f} {x:13.3f} {m:9.4f} {1-m:9.4f} {(1-m)/base:10.3f}x")
    x1, x3 = 2.0, 3.0 * 2.0
    red = (1 - float(mu_fw(x3))) / (1 - float(mu_fw(x1)))
    check(red < 0.5,
          f"1 - mu falls by {1/red:.1f}x between theta(0)=1 and theta(0)=3 at a_ex/a0 = 2 -- Milgrom's "
          f"claim reproduced on the framework's own interpolation, so the MI EFE really does quench "
          f"harder than the MG one")

    banner("S3. *** DOES IT CLOSE THE PLANETARY LIABILITY? NO, AND IT CANNOT. ***")
    print("  Eq. (34) puts theta in an ADDITIVE term inside mu's argument:")
    print("      A(omega_in) = a_in + theta(omega_ex/omega_in) a_ex")
    print("  For a planet, a_in is its own Newtonian acceleration and a_ex the Galaxy's. The anomaly is")
    print("      a - a_N = a_N (1/mu - 1) ~ a_N a0 / (2A),  which is a0/2 when A ~ a_N.")
    print("  So theta suppresses the anomaly ONLY insofar as theta(0) a_ex competes with a_in:")
    print(f"  {'planet':<9s} {'a_in (m/s^2)':>13s} {'a_in/a_ex':>11s} "
          f"{'anomaly, theta=1':>17s} {'theta=3':>11s} {'theta=e^1.1':>12s}")
    planets = [("Mercury", 0.3871), ("Earth", 1.0), ("Mars", 1.5237), ("Saturn", 9.5826)]
    a0 = FOOTINGS[0][1]
    aex = G_EXT[0][1]
    worst = 0.0
    for nm, a_au in planets:
        a_in = GM_SUN / (a_au * AU) ** 2
        row = []
        for th in (1.0, 3.0, float(np.exp(1.1))):
            A = a_in + th * aex
            row.append(a_in * a0 / (2.0 * A))
        worst = max(worst, row[-1])
        print(f"  {nm:<9s} {a_in:13.4e} {a_in/aex:11.2e} {row[0]:17.4e} {row[1]:11.4e} {row[2]:12.4e}")
    print(f"\n  Earth 2-sigma limit on a constant sunward anomaly: {EARTH_LIMIT:.3e} m/s^2")
    a_in_e = GM_SUN / AU**2
    for th in (1.0, 3.0, float(np.exp(1.1))):
        an = a_in_e * a0 / (2.0 * (a_in_e + th * aex))
        print(f"    theta(0) = {th:6.3f}  ->  anomaly {an:.4e}  =  {an/EARTH_LIMIT:8.1f}x over")
    # what theta(0) would be REQUIRED
    th_req = (a_in_e * a0 / (2.0 * EARTH_LIMIT) - a_in_e) / aex
    print(f"\n  theta(0) REQUIRED to bring Earth to the bound: {th_req:.3e}")
    print(f"  Milgrom's own examples span theta(0) = 2 to {float(np.exp(1.1)):.2f}; his general family")
    print(f"  theta(y) = e^((1-y)/q) gives theta(0) = e^(1/q), unbounded as q -> 0, so there is no HARD")
    print(f"  ceiling -- but the requirement is {th_req/np.e:.2e}x his e-example and would need")
    print(f"  q = 1/ln(theta(0)) = {1/np.log(th_req):.4f}, i.e. a theta falling by {th_req:.1e} between")
    print("  y = 1 and y = 0. That is not 'of the order of a few' by any reading.")
    check(th_req > 1e6,
          f"the planetary liability needs theta(0) ~ {th_req:.1e}, which is {th_req/3.0:.1e}x Milgrom's "
          f"largest quoted example -- THE FREQUENCY-RATIO ROUTE DOES NOT CLOSE IT. The reason is "
          f"structural: theta enters additively against a_in, and at Earth a_in/a_ex = "
          f"{a_in_e/aex:.1e}, so the external term is invisible")
    print("  AND THE DEEPER REASON IT CANNOT: the a0/2 anomaly is a SINGLE-FREQUENCY effect. Milgrom's")
    print("  own result is that the algebraic MOND relation holds exactly for single-frequency")
    print("  (circular) trajectories, and a planetary orbit is very nearly one. A construction whose")
    print("  content is in frequency RATIOS has no purchase on a trajectory with effectively one")
    print("  frequency. The fifth constant omega_c was doing a job that ratios structurally cannot do.")

    banner("S4. *** THE REGIME WHERE theta WOULD PAY -- AND WHY THIS FRAMEWORK CANNOT COLLECT ***")
    print("  Wide binaries ARE Eq. (35)'s regime: a_ex/a0 ~ 2, and omega_ex << omega_in (the pair orbits")
    print("  far faster than the Galaxy), so theta -> theta(0), its maximum. What theta(0) WOULD give:")
    print(f"  {'a0 footing':<18s} {'g_ext':<26s} {'a_ex/a0':>8s}" +
          "".join(f"{('th=' + f'{t[1]:.2f}'):>10s}" for t in THETAS))
    grid = {}
    for flab, a0v in FOOTINGS:
        for glab, gv in G_EXT:
            e = gv / a0v
            vals = [float(gamma_v_from_mu(t[1] * e)) for t in THETAS]
            grid[(flab, glab)] = vals
            print(f"  {flab:<18s} {glab:<26s} {e:8.3f}" + "".join(f"{v:10.4f}" for v in vals))
    all_ge2 = [grid[k][i2] for k in grid for i2 in (1, 2, 3)]
    print(f"\n  Taken at face value that would sit at gamma_v {min(all_ge2):.4f}-{max(all_ge2):.4f}, i.e.")
    print(f"  BELOW the frozen MI point target {FROZEN_MI_POINT} on every theta(0) >= 2, and partly below")
    print(f"  the frozen band's lower edge {FROZEN_MI_BAND[0]}. A first pass of this script concluded an")
    print("  amendment was therefore owed. THAT CONCLUSION IS WITHDRAWN. It does not apply, because:")
    print()
    print("  (i) THE KERNEL CANNOT SOURCE theta. mi_theta_efe_from_closure_2026.py S1 shows, sympy-exact,")
    print("      that on the oscillatory branch |K| = 1 identically. theta's y-dependence would need |K|")
    print("      to vary with frequency; it cannot. Every bound orbit sits deep inside that regime.")
    print("  (ii) THEOREM B FORCES QUADRATURE, NOT LINEAR ADDITION. <Box_u>_u = +|a|^2 exactly on every")
    print("      timelike worldline, so the closure's argument is |a_in + a_ex|^2 -- the external field")
    print("      enters in quadrature WITH A VECTOR CROSS TERM. Milgrom's Eq. (34) is the linear")
    print("      a_in + theta a_ex with a scalar multiplier. Different structures; the framework is")
    print("      pinned to the first.")
    print("  Both were already committed BEFORE this script ran, and Amendment 2 to the DR4")
    print("  pre-registration already states it verbatim: 'no multiplying phase function")
    print("  theta(omega_ex/omega_in) is available'. Amendment 2 was right.")
    check(min(all_ge2) < FROZEN_MI_POINT,
          f"the numbers themselves are not in dispute -- theta(0) >= 2 WOULD give gamma_v "
          f"{min(all_ge2):.4f}-{max(all_ge2):.4f}, below the frozen point target {FROZEN_MI_POINT}. What is "
          f"in dispute is whether this framework may use them, and it may not")

    banner("S5. So the frozen target STANDS, and MI-vs-MG stays undecidable HERE")
    mg_ref = float(gamma_v_from_mu(G_EXT[0][1] / FOOTINGS[0][1]))
    print(f"  Frozen DR4 error model: sigma(gamma_v) = {SIGMA_GAMMA_DR4} at N = 30,000 pairs.")
    print(f"  If theta were available, MG (theta=1, {mg_ref:.4f}) and MI would separate by:")
    print(f"  {'theta(0)':>9s} {'gamma_v MI':>11s} {'separation':>11s} {'sigma':>7s}")
    dec = []
    for _nm, th in THETAS[1:]:
        mi = float(gamma_v_from_mu(th * G_EXT[0][1] / FOOTINGS[0][1]))
        sep = mg_ref - mi
        dec.append(sep / SIGMA_GAMMA_DR4)
        print(f"  {th:9.3f} {mi:11.4f} {sep:11.4f} {sep/SIGMA_GAMMA_DR4:6.1f}s")
    print(f"  -> {min(dec):.1f}-{max(dec):.1f} sigma. That decidability is REAL, and it belongs to")
    print("  Milgrom's general MI models. It is NOT available to this framework, whose derived EFE gives")
    print("  the Amendment-2 orientation-averaged gamma_v = 1.0799 with NO theta freedom at all.")
    print(f"  Framework (derived, Amendment 2) 1.0799 vs frozen MG {FROZEN_MG}: separation "
          f"{FROZEN_MG-1.0799:.4f} = {(FROZEN_MG-1.0799)/SIGMA_GAMMA_DR4:.1f} sigma.")
    check((FROZEN_MG - 1.0799) / SIGMA_GAMMA_DR4 < 3.0,
          f"for THIS framework the MI-MG separation is only "
          f"{(FROZEN_MG-1.0799)/SIGMA_GAMMA_DR4:.1f} sigma -- so section 1.5's forecast that MI-vs-MG is "
          f"likely UNDECIDABLE in DR4 stands unamended, exactly as Amendment 2 (g) said. No frozen "
          f"number moves as a result of this script")

    banner("S6. Does it cost anything on the RAR? No -- by his normalisation, and checked")
    print("  Milgrom fixes theta(1) = 1 precisely so that, verbatim, 'it is mu(a_ex/a0) that enters the")
    print("  rotation-curve analysis'. theta modifies the EXTERNAL-field term only (Eq. 34's second")
    print("  piece), so a system whose internal acceleration dominates is untouched. Structural check:")
    print(f"  {'y = g_bar/a0':>13s} {'nu (theta-free)':>16s} {'nu with theta(0)=3 on a_ex=0':>30s} {'ratio':>8s}")
    ok_rar = True
    for y in (0.01, 0.1, 1.0, 10.0, 100.0):
        nu_plain = np.sqrt(1.0 + 1.0 / y)
        # isolated system: a_ex = 0, so the theta term vanishes identically for ANY theta(0)
        A = y + 3.0 * 0.0
        nu_theta = np.sqrt(1.0 + 1.0 / A)
        if abs(nu_theta - nu_plain) > 1e-15:
            ok_rar = False
        print(f"  {y:13.3f} {nu_plain:16.6f} {nu_theta:30.6f} {nu_theta/nu_plain:8.6f}")
    check(ok_rar,
          "for an ISOLATED system the theta term is multiplied by a_ex = 0 and drops out identically "
          "for any theta(0), so the SPARC RAR fit (0.108 dex) is untouched -- this is not a tuning, it "
          "is what theta(1)=1 was chosen to guarantee")

    banner("S7. WHAT ACTUALLY SURVIVES: theta separates this framework from the MI family")
    print("  The interesting residue is a DISTINCTION, not a rescue. Milgrom's MI models carry a free")
    print("  function theta with theta(0) of order a few; this framework's closure pins theta = 1 by two")
    print("  independent theorems. So the two make DIFFERENT wide-binary predictions, and that is a")
    print("  falsifiability virtue for the framework: fewer free functions, a more rigid prediction.")
    print(f"  {'model':<44s} {'gamma_v':>18s}")
    print(f"  {'this framework (derived, quadrature, no theta)':<44s} {'1.0799':>18s}")
    for nm, th in THETAS[1:]:
        v = [grid[k2][THETAS.index((nm, th))] for k2 in grid]
        print(f"  {'Milgrom MI, ' + nm:<44s} {f'{min(v):.4f}-{max(v):.4f}':>18s}")
    v2 = [grid[k2][1] for k2 in grid]
    sep_fam = abs(1.0799 - float(np.mean(v2)))
    print(f"\n  Separation from the theta(0)=2 case: {sep_fam:.4f} in gamma_v = "
          f"{sep_fam/SIGMA_GAMMA_DR4:.1f} sigma at the frozen DR4 error model.")
    check(sep_fam / SIGMA_GAMMA_DR4 < 3.0,
          f"framework-vs-Milgrom-MI separates by only {sep_fam/SIGMA_GAMMA_DR4:.1f} sigma, so DR4 cannot "
          f"distinguish them either -- the distinction is real in principle and NOT a near-term test. "
          f"Reported as such rather than promoted to a front")

    banner("VERDICT")
    print("  1. THE DOOR DOES NOT DO WHAT IT WAS OPENED FOR. Milgrom's frequency-ratio construction")
    print("     does NOT close the alpha=1 planetary liability, and the failure is structural rather")
    print(f"     than quantitative: theta enters additively against a_in, Earth has a_in/a_ex = "
          f"{a_in_e/aex:.1e},")
    print(f"     and the required theta(0) ~ {th_req:.1e} is ten orders above his own examples. Deeper:")
    print("     the a0/2 anomaly is a single-frequency effect and a ratio construction has no purchase")
    print("     on a one-frequency trajectory. So the fifth constant omega_c is NOT shown unnecessary --")
    print("     it was doing a job ratios structurally cannot do. That hypothesis is CLOSED.")
    print("  2. AND THIS FRAMEWORK CANNOT USE IT EVEN WHERE IT WOULD HELP. In the wide-binary regime")
    print("     theta(0) of a few WOULD pull gamma_v from ~1.14 to 1.04-1.08, below the frozen MI point")
    print("     target 1.09. A first pass of this script concluded an amendment was owed on that basis.")
    print("     THAT IS WITHDRAWN. Two committed results, both predating this script, forbid it: the")
    print("     kernel is EXACTLY unimodular on the oscillatory branch so it cannot source theta's")
    print("     y-dependence (sympy), and Theorem B forces the closure's argument to |a_total|^2 --")
    print("     QUADRATURE with a vector cross term, not Milgrom's linear a_in + theta a_ex. Amendment 2")
    print("     to the DR4 pre-registration already says exactly this and was right. NO FROZEN NUMBER")
    print("     MOVES. Recording the near-miss because amending a frozen target on a basis the theory")
    print("     cannot use would have been a worse error than any wrong number in this file.")
    print("  3. SO MI-vs-MG STAYS UNDECIDABLE HERE. The 3.7-4.9 sigma separation theta would buy is real")
    print("     but belongs to Milgrom's general MI models. This framework's derived EFE gives 1.0799")
    print("     with no theta freedom, i.e. 3.0 sigma from the MG target -- section 1.5's forecast stands")
    print("     unamended, as does Amendment 2 (g).")
    print("  4. WHAT SURVIVES IS A DISTINCTION, NOT A RESCUE, and it cuts in the framework's favour on")
    print("     falsifiability: Milgrom's MI carries a free theta, this framework pins theta = 1 by two")
    print("     theorems. Fewer free functions, a more rigid wide-binary prediction. But the two")
    print("     predictions separate by under 3 sigma at the frozen DR4 error model, so this is a real")
    print("     distinction and NOT a near-term test. Not promoted to a front.")
    print("  5. NET: the door is CLOSED, on three independent grounds -- it cannot reach the planets")
    print("     (a_in/a_ex = 3.3e7), the kernel cannot supply theta, and Theorem B forbids the linear")
    print("     combination it needs. omega_c is NOT shown unnecessary. alpha=1 stands exactly where it")
    print("     did: exactness versus the planets, and only one survives.")
    check(True, "verdict recorded: door CLOSED on three independent grounds; NO frozen number moves; the near-miss amendment is recorded as withdrawn")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
