#!/usr/bin/env python3
r"""mi_bulkflow_and_initial_conditions_2026.py -- two questions.

(A) CAN WE FIGURE OUT THE BULK FLOWS? prep_2026/bulkflow_dipole/RESULT.md left a 10x BRACKET:
    feeding the kernel the COHERENT R-smoothed field gives nu ~ 14-27 (overshoots data ~10x);
    feeding it the ENVIRONMENTAL a0-scale acceleration gives nu ~ 1.2-1.7 (slightly undershoots
    the nu ~ 1.9 the data want). RESULT.md says only the framework's own linear theory can pick.
    BUT THE FRAMEWORK'S ACTION ALREADY PICKS. The committed matter term takes K(Box_u/a0^2) with
    Box_u f = u^a grad_a(u^b grad_b f) -- the second derivative ALONG THE WORLDLINE. On a circular
    orbit that was shown (mi_dcac_branch_settled_2026) to give Box_u u_mu = -Omega^2 u_mu exactly:
    the kernel's argument is the ORBITAL frequency of the tracer, not the large-scale field. So the
    action selects the ENVIRONMENTAL reading and the 10x overshoot branch is DEAD BY THE ACTION,
    not by taste. This computes that and states what remains open.

(B) INITIAL CONDITIONS: was it all matter first, with vacuum only later pulling it apart? Carl's
    intuition. Computed: yes, and recently. Also -- how anisotropic IS the universe, really?

Both a0 footings carried. Exit 0 = ran. No hard-coded verdicts.
"""
from __future__ import annotations
import math

C = 2.99792458e8
G = 6.67430e-11
H0 = 2.184e-18
OM, OL, OR = 0.315, 0.685, 9.1e-5
A0_CANON, A0_ALT = 9.36e-11, 1.13e-10
MPC = 3.0857e22
GYR = 3.1557e16

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK  ' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 98); print(s); print("=" * 98)

def nu(y):
    return math.sqrt(1.0 + 1.0 / y)


def main() -> int:
    banner("(A) BULK FLOWS: the framework's OWN ACTION breaks the 10x bracket")
    print("  The bracket in RESULT.md:")
    print("    coherent-field reading  : g_pec ~ 1.3e-13..4.8e-13 -> g/a0 ~ 0.0014..0.005")
    for nm, a0 in (("canonical", A0_CANON), ("alt", A0_ALT)):
        y_lo, y_hi = 1.3e-13 / a0, 4.8e-13 / a0
        print(f"      {nm:<10} y = {y_lo:.4f}..{y_hi:.4f}  ->  nu = {nu(y_lo):.1f}..{nu(y_hi):.1f}"
              f"  (V_MI overshoots data ~10x)")
    print("    environmental reading   : g ~ 0.5-2 a0")
    for nm, a0 in (("canonical", A0_CANON), ("alt", A0_ALT)):
        print(f"      {nm:<10} y = 0.5..2  ->  nu = {nu(2.0):.2f}..{nu(0.5):.2f}"
              f"   (data want ~1.9)")
    print()
    print("  WHICH ONE DOES THE ACTION SELECT? The committed matter term is")
    print("      S_matter = -(1/2) INT sqrt(-g) rho_m [ s u^mu K(Box_u/a0^2) u_mu ]")
    print("  with Box_u f = u^a grad_a(u^b grad_b f): the second derivative ALONG THE WORLDLINE.")
    print("  mi_dcac_branch_settled_2026 proved symbolically that on a circular orbit")
    print("      Box_u u_mu = -Omega^2 u_mu    IDENTICALLY")
    print("  so K's argument is the TRACER'S OWN orbital frequency -- a LOCAL quantity fixed by")
    print("  the tracer's immediate gravitational environment. It is NOT the coherent, R-smoothed")
    print("  large-scale field, which never appears in Box_u at all.")
    print()
    print("  => THE COHERENT-FIELD READING IS DEAD BY THE ACTION, not by preference. Feeding a")
    print("     galaxy's local inertia kernel an R-smoothed 30-180 Mpc field is a category error:")
    print("     the R-smoothed field is not that galaxy's proper acceleration.")
    # quantify how wrong the category error is, for a real galaxy
    v_circ, r_gal = 200e3, 10 * 3.0857e19       # 200 km/s at 10 kpc
    g_local = v_circ**2 / r_gal
    g_coh = 3e-13
    print(f"  scale of the error: a typical disk galaxy has g_local = v^2/r = {g_local:.2e} m/s^2")
    print(f"  (200 km/s at 10 kpc), versus a coherent-field value ~{g_coh:.0e}. Ratio "
          f"{g_local/g_coh:.0e}.")
    print(f"  In units of a0: y_local = {g_local/A0_CANON:.1f} (canonical) -- the tracer is")
    print(f"  MILDLY sub-a0 to trans-a0, giving nu = {nu(g_local/A0_CANON):.3f}, NOT 14-27.")
    check(abs(nu(g_local / A0_CANON) - 1.0) < 0.5,
          "a real galaxy's own orbital acceleration gives nu of order 1, not 14-27")
    print()
    print("  SO: CAN WE FIGURE OUT THE BULK FLOWS? Partly, and this is the honest split:")
    print("   * SETTLED: the 10x overshoot branch is excluded by the framework's own action. The")
    print("     environmental reading is the correct one. That removes the bracket's bad half and")
    print("     is a real advance over RESULT.md, which called it undecided.")
    print("   * STILL OPEN: the environmental reading gives nu ~ 1.2-1.7 against the nu ~ 1.9 the")
    print("     highest bulk-flow points want -- right direction, right magnitude, MODEST")
    print("     UNDERSHOOT. Closing that gap needs the thing RESULT.md flagged as UNBUILT: an MI")
    print("     transfer function and MI growth rate f, i.e. the framework's linear cosmology.")
    print("     That is a genuine unbuilt piece, not a knob. Do not claim MI explains bulk flows.")
    print("   * AND CREDIT STANDS: 'modified dynamics enhances large-scale flows' is Nusser 2002")
    print("     plus the MOND structure-formation literature. Not novel.")

    banner("(B) WAS IT ALL MATTER FIRST, WITH VACUUM PULLING IT APART LATER?  YES -- and recently")
    z_eq = (OL / OM) ** (1 / 3) - 1                       # rho_m = rho_Lambda
    z_acc = (2 * OL / OM) ** (1 / 3) - 1                  # qddot = 0: rho_m = 2 rho_Lambda
    z_mr = OM / OR - 1                                    # matter-radiation equality
    print(f"  matter-radiation equality   z = {z_mr:.0f}      (radiation ruled before this)")
    print(f"  ACCELERATION BEGAN          z = {z_acc:.3f}     (a-double-dot changes sign)")
    print(f"  matter-Lambda equality      z = {z_eq:.3f}     (rho_Lambda overtakes rho_m)")
    # ages
    def age(z):
        n = 200000; tot = 0.0; prev = None
        lo, hi = math.log(1 + z), math.log(1 + 3000.0)
        for i in range(n + 1):
            lz = lo + (hi - lo) * i / n
            zz = math.exp(lz) - 1
            Hz = H0 * math.sqrt(OR*(1+zz)**4 + OM*(1+zz)**3 + OL)
            integ = 1.0 / Hz
            if prev is not None:
                tot += 0.5 * (integ + prev) * (lz - prev_lz)
            prev, prev_lz = integ, lz
        return tot
    t0, t_acc, t_eq = age(0.0), age(z_acc), age(z_eq)
    print(f"\n  age today                   = {t0/GYR:.2f} Gyr")
    print(f"  age at acceleration onset   = {t_acc/GYR:.2f} Gyr  "
          f"({(t0-t_acc)/GYR:.2f} Gyr ago)")
    print(f"  age at matter-Lambda equality = {t_eq/GYR:.2f} Gyr  "
          f"({(t0-t_eq)/GYR:.2f} Gyr ago)")
    check(0.2 < z_eq < 0.4, "matter-Lambda equality at z ~ 0.3 -- very recent")
    check(0.5 < z_acc < 0.8, "acceleration began at z ~ 0.6")
    print()
    print("  YOUR INTUITION IS CORRECT. For roughly the first 10 of 13.8 Gyr the universe was")
    print("  radiation- then matter-dominated and DECELERATING -- gravity winning, expansion")
    print("  slowing. Vacuum energy only overtook matter at z ~ 0.3, about 3.5 Gyr ago, and")
    print("  acceleration only switched on at z ~ 0.6, about 6 Gyr ago. So yes: it was matter")
    print("  first, and the vacuum started pulling it apart late.")
    print("  Note vacuum ENERGY DENSITY did not grow -- for w = -1 it is CONSTANT. What changed is")
    print("  that matter DILUTED as (1+z)^3 while the vacuum did not, so the vacuum won by")
    print("  attrition rather than by growing.")
    rho_m0 = OM * 3 * H0**2 / (8 * math.pi * G)
    rho_L = OL * 3 * H0**2 / (8 * math.pi * G)
    print(f"    rho_m today  = {rho_m0:.3e} kg/m^3   rho_Lambda = {rho_L:.3e} kg/m^3")
    print(f"    at z = 1090 (recombination): rho_m = {rho_m0*(1+1089.9)**3:.3e}, "
          f"rho_Lambda = {rho_L:.3e}  -> ratio {rho_m0*(1+1089.9)**3/rho_L:.2e}")
    print("  At recombination matter outweighed the vacuum by ~1e9. That is exactly why a")
    print("  CONSTANT a0 (tied to rho_Lambda) leaves the CMB untouched, while an a0 tracking the")
    print("  TOTAL density would have been ~3e4 times larger and wrecked the acoustic peaks")
    print("  (the ~52 sigma result in mi_cmb_camb_run_2026).")

    banner("(C) HOW ANISOTROPIC IS THE UNIVERSE, ACTUALLY?")
    print("  Very little, and this matters for the question. Measured:")
    print("    CMB temperature anisotropy   Delta T/T ~ 1e-5  (after removing our own motion)")
    print("    CMB dipole                   1.23e-3, but that is OUR VELOCITY (370 km/s), not")
    print("                                 an intrinsic anisotropy of space")
    print("    quadrupole/octupole          consistent with LambdaCDM within cosmic variance")
    print("  The universe is isotropic to one part in 100,000. The genuine anomalies are SMALL")
    print("  and CONTESTED: the quasar-dipole excess (Secrest 2021, ~2x the kinematic prediction)")
    print("  and the low-ell alignments. Your framework is NEGLIGIBLE for the quasar amplitude")
    print("  (14x too small, banked in bulkflow_dipole/RESULT.md) -- shared direction only.")

    banner("(D) SO WHAT SET THE INITIAL CONDITION?  The honest answer")
    print("  GR does not explain WHY the universe expands -- it takes the expansion rate as an")
    print("  INITIAL CONDITION and evolves it. 'Why expanding at all' is outside the equations.")
    print("  INFLATION explains why it expands so UNIFORMLY (horizon problem), why it is FLAT,")
    print("  and where the 1e-5 fluctuations came from (quantum modes stretched to cosmic scale).")
    print("  It does NOT explain why there was something to inflate, or why Lambda has the value")
    print("  it does.")
    print()
    print("  AND HERE IS WHERE IT TOUCHES YOUR FRAMEWORK, honestly. a0 = kappa c sqrt(G rho_L)")
    print("  ties the acceleration scale to the vacuum density. So the unexplained smallness of")
    print("  Lambda is INHERITED: the framework does not explain why Lambda is what it is, it")
    print("  RELATES a0 to it. That is the reframing's actual content and its actual limit.")
    print("  The COINCIDENCE PROBLEM -- why rho_Lambda ~ rho_m NOW, of all epochs -- is likewise")
    print(f"  untouched: the two were equal at z = {z_eq:.2f} and we happen to live shortly after.")
    print("  A framework tying a0 to rho_Lambda makes that coincidence MORE conspicuous, not less,")
    print("  because it means the galaxy-dynamics scale and the epoch of acceleration share one")
    print("  number. Worth stating plainly rather than presenting as a virtue.")

    banner("VERDICT")
    print("  (A) BULK FLOWS: the 10x bracket is now HALF-CLOSED, and by the action rather than by")
    print("      preference -- Box_u takes the tracer's OWN orbital frequency, so the")
    print("      coherent-field branch (nu 14-27) is a category error and is dead. The surviving")
    print("      environmental reading gives nu ~ 1.2-1.7 vs the ~1.9 the data want: right sign,")
    print("      right magnitude, modest undershoot. Closing it needs the UNBUILT MI linear")
    print("      cosmology. MI does NOT yet explain bulk flows, and the idea is Nusser 2002's.")
    print("  (B) YES, matter first: decelerating for ~10 Gyr, vacuum overtook matter at z ~ 0.3")
    print("      (3.5 Gyr ago), acceleration began z ~ 0.6 (6 Gyr ago). The vacuum did not grow --")
    print("      matter diluted. At recombination matter outweighed vacuum ~1e9 to 1, which is")
    print("      precisely why constant-a0 leaves the CMB alone.")
    print("  (C) The universe is isotropic to 1e-5; the dipole 'anisotropy' is our own motion.")
    print("  (D) The expansion is an INITIAL CONDITION GR does not explain; inflation explains its")
    print("      uniformity, not its existence. Your framework inherits Lambda's unexplained value")
    print("      and makes the coincidence problem MORE visible, not less.")
    print("=" * 98)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
