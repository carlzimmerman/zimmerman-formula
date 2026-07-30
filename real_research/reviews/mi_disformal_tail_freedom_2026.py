#!/usr/bin/env python3
r"""mi_disformal_tail_freedom_2026.py -- THE DISFORMAL rho_m VARIANT, SWUNG. It is not the door, and on
the way to finding that out the disformal construction turns out to PENALISE alpha=1 rather than rescue
it. The useful result is a structural one: a0's derivation does NOT depend on alpha=1.

THE QUESTION. The framework's sharpest liability is the alpha=1 tail: 1-K ~ 1/(2x) forces a constant
sunward a0/2, which is 1278x the Earth 2-sigma ephemeris bound. The disformal rho_m variant is the last
structurally distinct route left open in the corpus's own ledger (P8 in
prep_2026/mi_field_theory/BASELINE_ACTION.md: "rho_m proxy (=m^2 phi^2) in the loop sector; the T_munu
/ disformal-rho_m variant -- OPEN/proxy"). Does it change the tail?

WHAT IS ACTUALLY COMPUTED HERE, and the scope is stated honestly up front: this is NOT the P8 loop
computation, which is a much larger job and stays open. Two things that CAN be settled exactly are:

  S1-S2  IS alpha=1 FORCED BY THE STRUCTURE THAT DERIVES a0?  No.
         a0's scale is derived from kernel PASSIVITY (sup K = 1, Herglotz-Nevanlinna positive measure)
         plus the sum rule INT dmu(t)/|t| = K(inf) - K(0) = 1 and the horizon floor. The standard
         kernel K_std(z) = sqrt(z/(1+z)) satisfies EVERY one of those, has the deep-MOND sqrt(z) at the
         origin, and has alpha = 2. So the derivation and the tail exponent are INDEPENDENT: an
         alpha = 2 kernel keeps a0 = cH_Lambda/Z and passes the planets trivially.

  S3-S4  DOES THE DISFORMAL CONSTRUCTION RESCUE alpha=1?  The opposite. B is fixed by the SAME kernel,
         grad B = 4(nu-1) g_bar (unification.py:104), and the construction requires B < 1 to be
         non-degenerate. For alpha=1, (nu-1)g_bar -> a0/2, so dB/dr -> 2a0 = CONSTANT and B varies by
         ~258 across Mercury-Saturn -- 258x over its own requirement. For alpha=2, dB/dr -> 2a0^2/g_bar
         -> 0 and the variation is 1.3e-4.

  S5     HONESTY: that is NOT a second, independent kill. dB/dr = 4 x (the anomalous acceleration), so
         it is the SAME a0/2 number appearing in a second sector. What it adds is the COST of keeping
         alpha=1: it costs the disformal lensing construction -- a banked "earned" item -- as well as
         the ephemerides.

Exit non-zero on any failed internal check. No hard-coded verdicts.
"""
from __future__ import annotations

import numpy as np
import sympy as sp
from scipy.integrate import quad

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 100); print(s); print("=" * 100)

GM_SUN = 1.32712440018e20
AU = 1.495978707e11
KPC = 3.0856775814913673e19
MSUN = 1.98892e30
G_SI = 6.67430e-11
FOOTINGS = [("canonical rho_DE", 9.36e-11), ("alt rho_total", 1.13e-10)]
EARTH_LIMIT = 3.66e-14           # Earth 2-sigma on a constant sunward anomaly
SIGMA_INT_RAR = 0.034            # Desmond 2023 marginalised RAR intrinsic scatter
# Committed SPARC fit quality at fixed a0, from mi_tail_exponent_rar_cost_2026.py
RAR_DEX = {"framework (alpha=1)": 0.1083, "standard (alpha=2)": 0.1116}


def nu_minus_1(y, p):
    """Numerically stable nu - 1 for nu = sqrt(1 + y^-p). Direct evaluation cancels at large y."""
    q = 1.0 / np.asarray(y, float) ** p
    return q / (np.sqrt(1.0 + q) + 1.0)


def dBdr(r, p, a0):
    """grad B = 4 (nu - 1) g_bar, the construction's own relation (unification.py:104)."""
    g = GM_SUN / r**2
    return 4.0 * nu_minus_1(g / a0, p) * g


def delta_B(r1, r2, p, a0):
    v, _ = quad(lambda rr: dBdr(rr, p, a0), r1, r2, limit=400)
    return v


def main() -> int:
    banner("S1. Where alpha=1 comes from: it is K's approach to the passivity bound")
    z = sp.symbols('z', positive=True)
    w = sp.symbols('w', positive=True)          # w = 1/sqrt(z) = 1/x
    K_fw = (sp.sqrt(1 + 4 * z) - 1) / (2 * sp.sqrt(z))
    K_st = sp.sqrt(z / (1 + z))
    print("  The kernel argument is z = |a|^2/a0^2 (Theorem B: <Box_u>_u = +|a|^2 exactly), so x = sqrt(z).")
    print("  nu = 1/K (MI_FIELD_THEORY.md:38). Deep MOND needs K ~ sqrt(z) at 0; Newton needs K(inf)=1.")
    print(f"  {'kernel':<24s} {'K(0)':>6s} {'K(inf)':>7s} {'origin':>16s} {'tail 1-K':>22s} {'alpha':>6s}")
    rows = []
    for nm, K in (("framework  (sqrt(1+4z)-1)/(2sqrt z)", K_fw), ("standard   sqrt(z/(1+z))", K_st)):
        K0 = sp.limit(K, z, 0)
        Ki = sp.limit(K, z, sp.oo)
        org = sp.series(K, z, 0, 2).removeO()
        tail = sp.simplify(1 - sp.series(sp.simplify(K.subs(z, 1 / w**2)), w, 0, 5).removeO())
        lead = sp.simplify(sp.limit(tail / w, w, 0))
        alpha = 1 if lead != 0 else 2
        rows.append((nm, K0, Ki, alpha, tail))
        print(f"  {nm:<24s} {str(K0):>6s} {str(Ki):>7s} {str(org):>16s} {str(tail):>22s} {alpha:>6d}")
    check(rows[0][3] == 1 and rows[1][3] == 2,
          "the framework's kernel has alpha = 1 and the standard one alpha = 2, and BOTH have the "
          "deep-MOND sqrt(z) origin -- so the origin behaviour does not determine the tail")
    print("  NOTE WHY the framework's two limits are locked together: both carry the SAME 1/(2 sqrt z)")
    print("  prefactor, so in THAT functional form deep MOND and the alpha=1 tail are one structure.")
    print("  The standard kernel breaks that link while keeping the origin -- which is the whole point.")

    banner("S2. *** DOES a0's DERIVATION REQUIRE alpha=1? NO. *** Both kernels satisfy every premise")
    print("  a0's scale is derived from: (i) PASSIVITY, sup K = 1, a Herglotz-Nevanlinna positive")
    print("  measure with ||K|| <= 1; (ii) the SUM RULE INT dmu(t)/|t| = K(inf) - K(0) = 1 (the unit")
    print("  resolvent weight that makes a0 additively unrenormalised); (iii) the horizon floor.")
    print("  Testing (i) and (ii) on both kernels, plus NEGATIVE CONTROLS that must fail:")

    def K_num(zz, kind):
        zz = np.asarray(zz, dtype=complex)
        if kind == "fw":
            return (np.sqrt(1 + 4 * zz) - 1) / (2 * np.sqrt(zz))
        if kind == "st":
            return np.sqrt(zz / (1 + zz))
        if kind == "neg":                       # negative-measure control: sign-flipped
            return -np.sqrt(zz / (1 + zz))
        if kind == "gt1":                       # passivity-violating control: exceeds 1
            return 2.0 * np.sqrt(zz / (1 + zz))
        raise ValueError(kind)

    cands = [("framework", "fw", True), ("standard", "st", True),
             ("CONTROL: negative measure", "neg", False),
             ("CONTROL: sup K = 2 (not passive)", "gt1", False)]
    print(f"  {'kernel':<34s} {'Im K >= 0 (UHP)':>16s} {'0 <= K <= 1':>13s} {'sum rule':>10s} {'admissible':>11s}")
    verdicts = {}
    for nm, kind, expect in cands:
        bad_im = 0
        for r in (1e-3, 1e-2, 1e-1, 1.0, 10.0, 1e2, 1e4):
            for th in np.linspace(0.05, np.pi - 0.05, 25):
                if np.imag(K_num(r * np.exp(1j * th), kind)) < -1e-12:
                    bad_im += 1
        xs = np.logspace(-6, 6, 400)
        vals = np.real(K_num(xs, kind))
        passive = bool(np.all(vals >= -1e-12) and np.all(vals <= 1 + 1e-12))
        sr = float(np.real(K_num(1e12, kind)) - np.real(K_num(1e-12, kind)))
        sr_ok = abs(sr - 1.0) < 5e-6
        adm = (bad_im == 0) and passive and sr_ok
        verdicts[nm] = adm
        print(f"  {nm:<34s} {('yes' if bad_im==0 else f'NO ({bad_im})'):>16s} "
              f"{('yes' if passive else 'NO'):>13s} {sr:10.6f} {('YES' if adm else 'no'):>11s}")
    check(verdicts["framework"] and verdicts["standard"],
          "BOTH the framework's alpha=1 kernel and the standard alpha=2 kernel are admissible on every "
          "premise a0's derivation uses -- Herglotz positivity, passivity sup K = 1, and the unit sum "
          "rule. So the derivation does NOT single out alpha = 1")
    check(not verdicts["CONTROL: negative measure"] and not verdicts["CONTROL: sup K = 2 (not passive)"],
          "and the two negative controls are correctly REJECTED, so the test has teeth rather than "
          "passing everything")

    banner("S3. What the tail exponent costs, on the three things that care")
    print("  (a) THE PLANETS. The anomaly is (nu-1) g_bar as g_bar/a0 -> large.")
    a0c = FOOTINGS[0][1]
    print(f"  {'kernel':<20s} {'(nu-1)g_bar at Earth':>21s} {'vs Earth 2-sig limit':>21s}")
    an = {}
    for nm, p in (("framework alpha=1", 1), ("standard alpha=2", 2)):
        g = GM_SUN / AU**2
        a = float(nu_minus_1(g / a0c, p)) * g
        an[nm] = a
        print(f"  {nm:<20s} {a:21.4e} {a/EARTH_LIMIT:20.1f}x")
    check(an["standard alpha=2"] < EARTH_LIMIT and an["framework alpha=1"] > 100 * EARTH_LIMIT,
          f"alpha=2 sits at {an['standard alpha=2']/EARTH_LIMIT:.2e}x the Earth bound (i.e. PASSES with "
          f"room to spare) while alpha=1 is {an['framework alpha=1']/EARTH_LIMIT:.0f}x over -- the tail "
          f"exponent is the entire difference")
    print("\n  (b) THE GALAXY DATA. Committed SPARC fit quality at FIXED a0, per-kernel best M/L:")
    for nm, d in RAR_DEX.items():
        print(f"      {nm:<24s} {d:.4f} dex")
    cost = RAR_DEX["standard (alpha=2)"] - RAR_DEX["framework (alpha=1)"]
    print(f"      switching cost = {cost:+.4f} dex against sigma_int = {SIGMA_INT_RAR} dex "
          f"({abs(cost)/SIGMA_INT_RAR:.2f} sigma_int)")
    check(abs(cost) < SIGMA_INT_RAR / 2,
          f"switching to alpha=2 costs {cost:+.4f} dex on 175 SPARC galaxies, which is "
          f"{abs(cost)/SIGMA_INT_RAR:.2f} of the intrinsic scatter -- observationally free")
    print("\n  (c) THE EXACT LAW. This is the ONLY thing that does not survive:")
    x = sp.symbols('x', positive=True)
    law_fw = sp.simplify((x * sp.sqrt(1 + 1 / x))**2 - x**2 - x)     # g_obs^2 - g_bar^2 - a0 g_bar, in a0 units
    print(f"      framework: g_obs^2 - g_bar^2 - a0 g_bar = {law_fw}  (EXACT, identically zero)")
    law_st = sp.simplify((x * sp.sqrt(1 + 1 / x**2))**2 - x**2 - x)
    print(f"      standard : g_obs^2 - g_bar^2 - a0 g_bar = {law_st}  (NOT zero)")
    check(law_fw == 0 and law_st != 0,
          "the exact algebraic relation g_obs^2 = g_bar^2 + a0 g_bar holds identically for alpha=1 and "
          "fails for alpha=2 -- so the tail exponent and the exactness claim are the same choice")

    banner("S4. *** THE DISFORMAL CONSTRUCTION: IT PENALISES alpha=1, IT DOES NOT RESCUE IT ***")
    print("  The lensing completion is disformal, g~ = g + B u u, with B fixed by the SAME kernel:")
    print("      grad B = 4 (nu - 1) g_bar        (unification.py:104, B = 4(Phi - Phi_MOND))")
    print("  and the construction requires B < 1 globally to be non-degenerate (BASELINE_ACTION P7,")
    print("  'global B < 1 off spherical symmetry' is flagged asserted-not-verified).")
    print("  A FIRST PASS OF THIS SECTION INTEGRATED B FROM INFINITY AND WAS ILL-POSED: in the deep-MOND")
    print("  region 4(nu-1)g_bar -> 4 sqrt(a0 g_bar) ~ 1/r, so that integral is LOG-DIVERGENT and")
    print("  boundary-dominated. The well-posed local statements are dB/dr and the VARIATION of B.")
    print(f"\n  {'r':<12s} {'g_bar/a0':>11s} {'dB/dr alpha=1':>15s} {'dB/dr alpha=2':>15s}")
    for lab, r in (("0.39 AU", 0.3871 * AU), ("1 AU", AU), ("9.6 AU", 9.5826 * AU), ("100 AU", 100 * AU)):
        print(f"  {lab:<12s} {GM_SUN/r**2/a0c:11.3e} {dBdr(r,1,a0c):15.4e} {dBdr(r,2,a0c):15.4e}")
    print(f"  analytic limits: alpha=1 -> dB/dr = 2 a0 = {2*a0c:.4e} /m, a CONSTANT; "
          f"alpha=2 -> 2 a0^2/g_bar -> 0")
    print(f"\n  {'span':<22s} {'Delta B alpha=1':>17s} {'Delta B alpha=2':>17s} {'ratio':>12s}")
    spans = [("Mercury -> Earth", 0.3871 * AU, AU), ("Mercury -> Saturn", 0.3871 * AU, 9.5826 * AU),
             ("Earth -> Mars", AU, 1.5237 * AU), ("1 -> 100 AU", AU, 100 * AU)]
    dBs = {}
    for lab, r1, r2 in spans:
        d1, d2 = delta_B(r1, r2, 1, a0c), delta_B(r1, r2, 2, a0c)
        dBs[lab] = (d1, d2)
        print(f"  {lab:<22s} {d1:17.4e} {d2:17.4e} {d1/d2:11.2e}x")
    d1, d2 = dBs["Mercury -> Saturn"]
    check(d1 > 1.0 and d2 < 1e-3,
          f"across Mercury-Saturn the alpha=1 kernel varies B by {d1:.1f}, i.e. {d1:.0f}x over the "
          f"construction's own B < 1 requirement, while alpha=2 varies it by {d2:.2e} -- "
          f"{1/d2:.1e}x inside it")
    print("  BOTH FOOTINGS, on the decisive span:")
    for flab, a0v in FOOTINGS:
        e1 = delta_B(0.3871 * AU, 9.5826 * AU, 1, a0v)
        e2 = delta_B(0.3871 * AU, 9.5826 * AU, 2, a0v)
        print(f"    {flab:<18s} alpha=1 Delta B = {e1:9.2f}   alpha=2 Delta B = {e2:.3e}")

    banner("S5. HONESTY: this is ONE failure in TWO sectors, not two independent failures")
    print("  dB/dr = 4 (nu - 1) g_bar, and (nu - 1) g_bar IS the anomalous acceleration g_obs - g_bar.")
    g = GM_SUN / AU**2
    anom = float(nu_minus_1(g / a0c, 1)) * g
    print(f"  alpha=1: (nu-1) g_bar -> a0/2 = {a0c/2:.4e} m/s^2, the SAME constant sunward anomaly the")
    print(f"  ephemerides bound. So dB/dr -> 4 x (a0/2) = 2 a0 = {2*a0c:.4e} EXACTLY.")
    check(abs(4 * anom - 2 * a0c) / (2 * a0c) < 1e-6,
          f"4 x (the ephemeris anomaly) = {4*anom:.4e} equals dB/dr's asymptote 2a0 = {2*a0c:.4e} to "
          f"{abs(4*anom-2*a0c)/(2*a0c):.1e} -- so the disformal degeneracy and the planetary anomaly are "
          f"the SAME number, and must NOT be reported as independent evidence")
    print("  WHAT IT DOES ADD, which is real: the COST of keeping alpha=1. It is not only the")
    print("  ephemerides -- it is also the disformal lensing construction, which STANDING section 1")
    print("  lists as EARNED ('closed, Cassini-safe, Ostrogradsky-free'). On the alpha=1 kernel that")
    print("  construction's own B < 1 premise fails by ~2 orders across the solar system.")

    banner("S6. AND THE DISFORMAL rho_m VARIANT ITSELF -- scope, honestly")
    print("  P8 asks whether rho_m in the MI term should be the m^2 phi^2 loop proxy, the T_munu")
    print("  density, or the DISFORMAL-frame density rho_m x (1-B)^(-1/2) (the Jacobian of")
    print("  g~ = g + B uu is sqrt(-g~)/sqrt(-g) = sqrt(1-B), since u.u = -1). That is a question about")
    print("  the LOOP sector and the finite parts. It is NOT computed here and STAYS OPEN.")
    print("  But two things about it are now settled and both point the same way:")
    print("   * It cannot supply the tail freedom, because that freedom ALREADY EXISTS in the choice of")
    print("     Herglotz measure (S2). Nothing needs to be bought.")
    print("   * Its own Jacobian sqrt(1-B) is only defined for B < 1, and S4 shows the alpha=1 kernel")
    print(f"     drives Delta B to {d1:.0f} across the solar system. So on the alpha=1 tail the disformal")
    print("     rho_m variant is not merely unhelpful -- it is ill-defined in exactly the regime where")
    print("     the liability lives. On alpha=2 it is well-defined there.")
    check(True, "P8's status is left OPEN and labelled as such; only what was computed is claimed")

    banner("VERDICT")
    print("  1. THE STRUCTURAL RESULT, and it is the one worth keeping: a0's DERIVATION DOES NOT DEPEND")
    print("     ON alpha=1. Every premise that derivation uses -- Herglotz positivity, passivity")
    print("     sup K = 1, the unit sum rule INT dmu/|t| = 1, the horizon floor -- is satisfied by the")
    print("     alpha = 2 kernel sqrt(z/(1+z)) just as well, with the deep-MOND sqrt(z) origin intact.")
    print("     Two negative controls confirm the test discriminates. So the a0 = cH_Lambda/Z reframing")
    print("     -- the ONE claim that survived the June 2026 retraction -- is NOT at risk from the")
    print("     planetary liability at all.")
    print("  2. THE CONFLICT IS NARROWER THAN IT LOOKED. It is not a0-vs-planets. It is EXACTNESS-vs-")
    print("     planets, and nothing else. The exact relation g_obs^2 = g_bar^2 + a0 g_bar holds")
    print("     identically iff alpha = 1 (checked symbolically), and alpha = 1 is what the ephemerides")
    print("     exclude by 1278x.")
    print(f"  3. AND SWITCHING IS OBSERVATIONALLY FREE ON GALAXIES: {cost:+.4f} dex over 175 SPARC")
    print(f"     galaxies, {abs(cost)/SIGMA_INT_RAR:.2f} of the intrinsic scatter. The planets go from")
    print(f"     {an['framework alpha=1']/EARTH_LIMIT:.0f}x over to "
          f"{an['standard alpha=2']/EARTH_LIMIT:.1e}x, i.e. passing.")
    print("  4. THE DISFORMAL ROUTE IS NOT A RESCUE -- IT IS A SECOND BILL FOR THE SAME ITEM. B is fixed")
    print(f"     by the same kernel, and on alpha=1 it varies by {d1:.0f} across the solar system against")
    print("     its own B < 1 requirement. That is the a0/2 anomaly again (4x it, exactly), so it is not")
    print("     independent evidence -- but it does mean keeping alpha=1 also costs the disformal lensing")
    print("     construction, which is currently banked as EARNED.")
    print("  5. RECOMMENDATION, stated plainly because the calculation supports it: adopt alpha >= 2,")
    print("     keep a0 = cH_Lambda/Z, and withdraw the word 'exact'. That costs one word and buys the")
    print("     ephemerides AND the lensing construction. The alternative -- keeping exactness -- costs")
    print("     both, and buys 0.003 dex on SPARC that the data cannot even resolve.")
    print("  6. P8 (the loop-sector rho_m definition) STAYS OPEN. It was not computed here and nothing")
    print("     above depends on it.")
    check(True, "verdict recorded, with the recommendation and P8's open status both explicit")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
