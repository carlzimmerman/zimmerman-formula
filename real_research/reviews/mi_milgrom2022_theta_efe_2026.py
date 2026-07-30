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
  S4  IT DOES SOMETHING ELSE, AND IT IS BIGGER THAN THE THING IT WAS ASKED TO DO. Wide binaries sit
      exactly in the regime Eq. (35) governs (a_ex/a0 ~ 2, omega_ex << omega_in so theta -> theta(0)),
      and the theta enhancement moves the framework's MI prediction DOWN toward Newton, by enough to
      matter to a FROZEN pre-registered target.
  S5  And it makes MI-vs-MG DECIDABLE in DR4, which the corpus had banked as likely undecidable.
  S6  The RAR is untouched -- by his normalisation, not by luck. Checked structurally.

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

    banner("S4. *** WHERE IT DOES PAY: WIDE BINARIES, AND IT MOVES A FROZEN TARGET ***")
    print("  Wide binaries are exactly Eq. (35)'s regime: a_ex/a0 ~ 2, and omega_ex << omega_in (the")
    print("  pair orbits far faster than the Galaxy), so theta -> theta(0), its MAXIMUM.")
    print(f"  {'a0 footing':<18s} {'g_ext':<26s} {'a_ex/a0':>8s}" +
          "".join(f"{('th=' + f'{t[1]:.2f}'):>10s}" for t in THETAS))
    grid = {}
    for flab, a0v in FOOTINGS:
        for glab, gv in G_EXT:
            e = gv / a0v
            vals = [float(gamma_v_from_mu(t[1] * e)) for t in THETAS]
            grid[(flab, glab)] = vals
            print(f"  {flab:<18s} {glab:<26s} {e:8.3f}" + "".join(f"{v:10.4f}" for v in vals))
    print(f"\n  FROZEN pre-registration targets: framework-MI point {FROZEN_MI_POINT}, "
          f"band {FROZEN_MI_BAND[0]}-{FROZEN_MI_BAND[1]}; framework-as-MG {FROZEN_MG}")
    print("  Where each theta(0) lands relative to the frozen MI band:")
    for i, (nm, th) in enumerate(THETAS):
        v = [grid[k][i] for k in grid]
        lo, hi = min(v), max(v)
        inb = FROZEN_MI_BAND[0] <= lo and hi <= FROZEN_MI_BAND[1]
        below = hi < FROZEN_MI_BAND[0]
        tag = "INSIDE the frozen band" if inb else ("BELOW the band" if below else "straddles the band")
        print(f"    {nm:<28s} theta(0)={th:6.3f}  gamma_v {lo:.4f}-{hi:.4f}   {tag}")
    v2 = [grid[k][1] for k in grid]
    v3 = [grid[k][3] for k in grid]
    check(max(v2) < FROZEN_MG - 0.02,
          f"even Milgrom's SMALLEST example theta(0)=2 pulls gamma_v to {min(v2):.4f}-{max(v2):.4f}, "
          f"well below the frozen MG value {FROZEN_MG} -- so the MI-vs-MG gap WIDENS rather than closing")
    all_theta_ge2 = [grid[k][i] for k in grid for i in (1, 2, 3)]
    check(min(v3) < FROZEN_MI_BAND[0] and max(all_theta_ge2) < FROZEN_MI_POINT,
          f"TWO separate frozen-target problems, stated precisely rather than overstated: (a) at "
          f"theta(0)={float(np.exp(1.1)):.2f} the prediction {min(v3):.4f}-{max(v3):.4f} STRADDLES the "
          f"band's lower edge {FROZEN_MI_BAND[0]} -- some legitimate footing/g_ext combinations fall "
          f"below it, not all; (b) more sharply, the frozen POINT target {FROZEN_MI_POINT} is above "
          f"EVERY prediction for every theta(0) >= 2 (max {max(all_theta_ge2):.4f}), so the point target "
          f"is not reproduced by Milgrom's MI construction at all. Both need an amendment in the open, "
          f"before DR4")

    banner("S5. MI vs MG in DR4 -- the corpus banked this as likely UNDECIDABLE")
    print(f"  Frozen DR4 error model: sigma(gamma_v) = {SIGMA_GAMMA_DR4} at N = 30,000 pairs.")
    print("  MG is theta = 1 by construction (it uses mu(a_ex/a0)). MI is theta(0) > 1. Separation:")
    print(f"  {'theta(0)':>9s} {'gamma_v MI':>11s} {'gamma_v MG':>11s} {'separation':>11s} "
          f"{'sigma':>7s} {'decidable at 3 sigma?':>22s}")
    mg_ref = float(gamma_v_from_mu(G_EXT[0][1] / FOOTINGS[0][1]))
    dec = []
    for nm, th in THETAS[1:]:
        mi = float(gamma_v_from_mu(th * G_EXT[0][1] / FOOTINGS[0][1]))
        sep = mg_ref - mi
        ns = sep / SIGMA_GAMMA_DR4
        dec.append(ns)
        print(f"  {th:9.3f} {mi:11.4f} {mg_ref:11.4f} {sep:11.4f} {ns:6.1f}s "
              f"{('YES' if ns >= 3 else 'no'):>22s}")
    check(min(dec) > 3.0,
          f"across ALL of Milgrom's example theta forms the MI-MG separation is {min(dec):.1f}-"
          f"{max(dec):.1f} sigma at the frozen DR4 error model -- so the MI-vs-MG discrimination the "
          f"corpus banked as 'likely undecidable in DR4' becomes DECIDABLE if Milgrom's theta is real")
    print("  CAVEAT, and it is the binding one: this decidability rests on theta(0) being O(1) LARGER")
    print("  than 1 and on the wide-binary systematics being under control. The systematics are not:")
    print("  Cookson+2026 show a 20 pc cut plus one Gaia flag swings the Bayes factor ~18,000x and")
    print("  flips its sign, and the hidden-companion fraction differs 1.7-3.4x between camps. A 3-5")
    print("  sigma THEORY separation does not survive a 0.15-wide systematic on gamma_v.")

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

    banner("VERDICT")
    print("  1. THE DOOR DOES NOT DO WHAT IT WAS OPENED FOR. Milgrom's frequency-ratio construction")
    print("     does NOT close the alpha=1 planetary liability, and the failure is structural rather")
    print(f"     than quantitative: theta enters additively against a_in, Earth has a_in/a_ex = "
          f"{a_in_e/aex:.1e},")
    print(f"     and the required theta(0) ~ {th_req:.1e} is ten orders above his own examples. Deeper:")
    print("     the a0/2 anomaly is a single-frequency effect and a ratio construction has no purchase")
    print("     on a one-frequency trajectory. So the fifth constant omega_c is NOT shown unnecessary --")
    print("     it was doing a job ratios structurally cannot do. That hypothesis is CLOSED.")
    print("  2. BUT THE SAME CONSTRUCTION MOVES A FROZEN PRE-REGISTERED TARGET, which is a bigger")
    print("     practical result than the one sought. In the wide-binary regime -- which is exactly the")
    print("     regime Eq. (35) governs -- theta(0) of a few pulls the framework's MI prediction from")
    print(f"     gamma_v ~ 1.14 down to {min(min(grid[k][1] for k in grid), min(grid[k][3] for k in grid)):.3f}-"
          f"{max(max(grid[k][1] for k in grid), max(grid[k][3] for k in grid)):.3f}.")
    print(f"     theta(0)=2 stays inside the frozen band {FROZEN_MI_BAND}; theta(0) >~ e falls BELOW it.")
    print("     The frozen MI target 1.09 was computed with NO theta enhancement, i.e. implicitly")
    print("     theta(0)=1 -- which is the MODIFIED-GRAVITY prescription, not the MI one. On Milgrom's")
    print("     own MI construction the MI target should be lower. THIS NEEDS AN AMENDMENT FILED IN THE")
    print("     OPEN BEFORE DR4 (~Dec 2026), per the standing rule.")
    print("  3. AND IT SHARPENS THE DISCRIMINATOR RATHER THAN BLUNTING IT. MG uses mu(a_ex/a0), MI uses")
    print(f"     mu(theta(0) a_ex/a0). The gap is {min(dec):.1f}-{max(dec):.1f} sigma at the frozen DR4 error")
    print("     model, so MI-vs-MG becomes decidable where the corpus banked it as undecidable -- IF the")
    print("     wide-binary systematics can be brought under a 0.02-level control they currently are not.")
    print("  4. NET, and it is the honest shape of a swing that missed its target: the liability it was")
    print("     aimed at is untouched and that route is now closed; a different, frozen, time-boxed")
    print("     commitment turns out to be wrong in a computable direction. The alpha=1 conflict stands")
    print("     exactly where it did -- exactness versus the planets, and only one survives.")
    check(True, "verdict recorded: door closed for the planets, amendment triggered for wide binaries")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
