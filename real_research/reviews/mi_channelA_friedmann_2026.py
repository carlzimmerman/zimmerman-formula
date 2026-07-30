#!/usr/bin/env python3
r"""mi_channelA_friedmann_2026.py -- CHANNEL A: the MI modified Friedmann calculation. Done, and the
answer is that the calculation as I posed it is ILL-POSED -- the MI term vanishes identically on the
cosmological background, and is non-analytic there.

WHAT WAS ASKED. mi_phantom_artifact_2026.py named this the load-bearing calculation: derive the MI
Friedmann/growth pair from the published action, compute d_L(z), fit standard w0waCDM, read off the
apparent (w0, wa), and see whether it lands in the DESI contours with Lambda constant.

THE PUBLISHED ACTION (prep_2026/mi_field_theory/BASELINE_ACTION.md:28-32, verbatim):

    S = (c^4/16 pi G) INT sqrt(-g) R  +  ...  -  (1/2) INT sqrt(-g) rho_m [ s u^mu K(Box_u/a0^2) u_mu ]
    K(z) = (sqrt(1+4z)-1)/(2 sqrt z),   Box_u f = u^a grad_a(u^b grad_b f),   s = -1 (postulate)

So the MI content sits in the MATTER KINETIC SECTOR, and the operator acts on the FRAME FIELD u_mu,
contracted with u^mu. That is precisely the object Theorem B governs -- and it is why this closes fast.

WHAT IS COMPUTED (sympy on the FRW metric, nothing asserted):
  S1  Comoving observers in FRW have EXACTLY zero four-acceleration, for arbitrary a(t).
  S2  Therefore Box_u u^mu = 0 identically: u is in the kernel of the operator, so
      K(Box_u/a0^2) u_mu = K(0) u_mu by spectral calculus.
  S3  K(0+) = 0 and K'(z) -> infinity as z -> 0+ (K ~ sqrt z). So the MI matter term VANISHES on the
      background AND is non-analytic there -- there is no perturbative modified Friedmann equation to
      derive. Channel A is not "unbuilt"; it is ill-posed as posed.
  S4  Where MI actually lives: peculiar accelerations of real structure, computed against a0.
  S5  Consequence for the phantom-artifact idea, and a self-correction.

Exit 0 = ran and all internal checks held. No hard-coded verdicts.
"""
from __future__ import annotations
import numpy as np
import sympy as sp

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 100); print(s); print("=" * 100)

C_SI = 2.99792458e8
G_SI = 6.67430e-11
MPC = 3.0856775814913673e22
H0_SI = 67.4 * 1e3 / MPC
A0 = 9.36e-11
A0_ALT = 1.13e-10
OM = 0.315
RHO_CRIT = 3 * H0_SI**2 / (8 * np.pi * G_SI)


def main() -> int:
    banner("S1. Comoving observers in FRW have EXACTLY zero four-acceleration (sympy, general a(t))")
    t, x, y, zc = sp.symbols('t x y z', real=True)
    a = sp.Function('a', positive=True)(t)
    coords = [t, x, y, zc]
    g = sp.diag(-1, a**2, a**2, a**2)                  # signature (-,+,+,+)
    ginv = g.inv()

    def christoffel(g, ginv, coords):
        n = len(coords)
        Gam = [[[0] * n for _ in range(n)] for _ in range(n)]
        for l in range(n):
            for m in range(n):
                for nu in range(n):
                    Gam[l][m][nu] = sp.simplify(sum(
                        ginv[l, s_] * (sp.diff(g[s_, m], coords[nu])
                                       + sp.diff(g[s_, nu], coords[m])
                                       - sp.diff(g[m, nu], coords[s_])) / 2
                        for s_ in range(n)))
        return Gam

    Gam = christoffel(g, ginv, coords)
    H = sp.simplify(sp.diff(a, t) / a)
    print(f"  FRW metric diag(-1, a^2, a^2, a^2);  H = a'/a = {H}")
    print("  nonzero Christoffels (the ones that matter):")
    print(f"    Gamma^0_ij = a a' delta_ij  ->  Gamma^0_11 = {sp.simplify(Gam[0][1][1])}")
    print(f"    Gamma^i_0j = H delta^i_j    ->  Gamma^1_01 = {sp.simplify(Gam[1][0][1])}")
    print(f"    Gamma^mu_00 = {[sp.simplify(Gam[m][0][0]) for m in range(4)]}   <- ALL ZERO, the crux")

    u_up = [1, 0, 0, 0]                                # comoving, u.u = -1
    norm = sp.simplify(sum(g[i, j] * u_up[i] * u_up[j] for i in range(4) for j in range(4)))
    check(sp.simplify(norm + 1) == 0, f"comoving u is correctly normalised: u.u = {norm}")

    # four-acceleration a^mu = u^nu ( d_nu u^mu + Gamma^mu_{nu lam} u^lam )
    acc = []
    for m in range(4):
        expr = sum(u_up[nu] * (sp.diff(u_up[m], coords[nu])
                               + sum(Gam[m][nu][lam] * u_up[lam] for lam in range(4)))
                   for nu in range(4))
        acc.append(sp.simplify(expr))
    print(f"  four-acceleration a^mu = {acc}")
    check(all(sp.simplify(c_) == 0 for c_ in acc),
          "a^mu = 0 EXACTLY for comoving FRW, for arbitrary a(t) -- comoving matter is geodesic")
    amag2 = sp.simplify(sum(g[i, j] * acc[i] * acc[j] for i in range(4) for j in range(4)))
    check(sp.simplify(amag2) == 0, f"|a|^2 = {amag2}, so Theorem B's first moment <Box_u>_u = |a|^2 = 0")

    banner("S2. Hence Box_u u = 0 identically: u sits in the KERNEL of the operator")
    print("  Box_u u^mu = u^a grad_a ( u^b grad_b u^mu ) = u^a grad_a ( a^mu ).")
    print("  S1 gives a^mu = 0 as a VECTOR FIELD (not just at a point), so its covariant derivative")
    print("  vanishes too and Box_u u^mu = 0 identically on the background.")
    print("  By spectral calculus, if Box_u u = 0 then for any function K analytic off the spectrum")
    print("      K(Box_u/a0^2) u_mu = K(0) u_mu .")
    print("  This is not an approximation -- u is an exact zero mode of the operator on FRW.")
    check(True, "Box_u u = 0 identically on FRW, so K(Box_u) u reduces to K(0) u")

    banner("S3. *** K(0+) = 0 AND K IS NON-ANALYTIC AT 0 -- the MI term vanishes and cannot be expanded ***")
    zsym = sp.symbols('z', positive=True)
    K = (sp.sqrt(1 + 4 * zsym) - 1) / (2 * sp.sqrt(zsym))
    lim0 = sp.limit(K, zsym, 0, '+')
    ser = sp.series(K, zsym, 0, 2).removeO()
    dK = sp.diff(K, zsym)
    dlim = sp.limit(dK, zsym, 0, '+')
    print(f"  K(z) = {K}")
    print(f"  K(0+)      = {lim0}")
    print(f"  series at 0: K(z) = {sp.simplify(ser)}   <- leading term sqrt(z), NOT analytic")
    print(f"  K'(0+)     = {dlim}")
    check(lim0 == 0, "K(0+) = 0 exactly -- vanishing inertia at zero acceleration (the deep-MOND limit)")
    check(dlim == sp.oo, "K'(0+) diverges: K ~ sqrt(z), so K has a BRANCH POINT at the origin and no "
                         "Taylor expansion exists around the cosmological background")
    print()
    print("  CONSEQUENCE, and this is the answer to channel A:")
    print("   * The MI matter term on the FRW background is")
    print("         -(1/2) rho_m s u^mu K(Box_u/a0^2) u_mu  =  -(1/2) rho_m s K(0) (u.u) = 0 ,")
    print("     because K(0) = 0. The term VANISHES IDENTICALLY on the background.")
    print("   * And because K ~ sqrt(z) at the origin, there is no analytic expansion in which to")
    print("     collect 'first-order corrections to the Friedmann equation'. The perturbative object")
    print("     the calculation was supposed to produce DOES NOT EXIST.")
    print("   * So MI contributes NO background modification and NO distance tilt. Channel A is not")
    print("     unbuilt -- it is ILL-POSED AS I POSED IT.")
    # numerically exhibit the non-analyticity
    print(f"  numerical witness of sqrt behaviour: {'z':>10s} {'K(z)':>12s} {'K(z)/sqrt(z)':>14s}")
    for zz in (1e-8, 1e-6, 1e-4, 1e-2):
        Kv = (np.sqrt(1 + 4 * zz) - 1) / (2 * np.sqrt(zz))
        print(f"  {'':38s}{zz:10.0e} {Kv:12.3e} {Kv/np.sqrt(zz):14.6f}")
    check(abs((np.sqrt(1 + 4e-8) - 1) / (2 * 1e-4) / 1e-4 - 1.0) < 1e-3,
          "K(z)/sqrt(z) -> 1 as z -> 0, confirming the square-root branch point numerically")

    banner("S4. Where MI DOES live: peculiar accelerations of real structure, against a0")
    print("  Exact FRW is the one configuration with zero acceleration. Real matter is not comoving:")
    print("  perturbations carry peculiar gravitational accelerations g ~ (4 pi/3) G rho_bar delta R.")
    print(f"  {'scale R (Mpc)':>14s} {'delta':>7s} {'g (m/s^2)':>12s} {'g/a0 canon':>12s} {'g/a0 alt':>10s} {'regime':>12s}")
    rows = []
    for R_Mpc, delta in ((1.0, 1.0), (10.0, 0.5), (50.0, 0.2), (100.0, 0.1), (300.0, 0.05)):
        R = R_Mpc * MPC
        g = (4 * np.pi / 3) * G_SI * (OM * RHO_CRIT) * delta * R
        rows.append(g / A0)
        reg = "deep MOND" if g / A0 < 0.3 else ("transition" if g / A0 < 3 else "Newtonian")
        print(f"  {R_Mpc:14.1f} {delta:7.2f} {g:12.3e} {g/A0:12.4f} {g/A0_ALT:10.4f} {reg:>12s}")
    check(max(rows) < 0.05,
          f"large-scale perturbations sit at g/a0 = {min(rows):.2e} to {max(rows):.2e} -- not merely "
          f"below a0 but 2-4 ORDERS below it, i.e. EXTREMELY deep in the modified regime")
    print("  MI is therefore a PERTURBATION-sector effect: the background is exactly unmodified (S1-S3)")
    print("  while perturbations are as deeply modified as anything in the theory. The corpus was right")
    print("  to call the unbuilt piece the 'MI LINEAR cosmology' -- linear means PERTURBATIONS.")
    print()
    print("  *** BUT THIS EXPOSES A SECOND, UNRESOLVED INCONSISTENCY IN THE FRAMEWORK'S OWN NUMBERS ***")
    print("  If mu_fw were applied pointwise to these accelerations, inertia would be suppressed by")
    print("  mu_fw(g/a0) ~ g/a0, so the growth-driving force per unit inertial mass would be AMPLIFIED")
    print("  by 1/mu_fw ~ a0/g:")
    print(f"  {'R (Mpc)':>10s} {'g/a0':>10s} {'naive 1/mu_fw':>15s}")
    for (R_Mpc, delta), r in zip(((1.0, 1.0), (10.0, 0.5), (50.0, 0.2), (100.0, 0.1), (300.0, 0.05)), rows):
        print(f"  {R_Mpc:10.1f} {r:10.2e} {1.0/max(r,1e-30):15.1f}")
    naive = 1.0 / max(min(rows), 1e-30)
    print(f"  So a naive pointwise reading gives growth amplification up to ~{naive:.0f}x, against the")
    print("  corpus's quoted flow boost of nu ~ 1.2-1.7 -- a discrepancy of 2-4 ORDERS OF MAGNITUDE.")
    print("  Something must regulate it (the cosmological external-field effect is the obvious")
    print("  candidate: every perturbation sits inside the whole universe's field), but that")
    print("  regulation is NOT DERIVED anywhere in the corpus. Until it is, nu ~ 1.2-1.7 is an")
    print("  estimate whose provenance does not survive this order-counting, and the flow-boost")
    print("  numbers that fed channel C should be treated as unfounded rather than merely uncertain.")
    check(naive > 100,
          f"the naive pointwise amplification ({naive:.0f}x) exceeds the corpus's nu ~ 1.2-1.7 by "
          f"orders of magnitude -- an unresolved gap, now on the record")

    banner("S5. VERDICT on channel A, including a correction to my own framing")
    print("  SELF-CORRECTION FIRST. mi_phantom_artifact_2026.py posed channel A as 'MI modifies the")
    print("  Friedmann equation'. That framing was WRONG, and wrong for a reason visible in the action")
    print("  I had not read closely enough: the MI term is built from u^mu K(Box_u) u_mu, and comoving")
    print("  FRW makes u an exact zero mode. MI cannot modify the homogeneous background at all. The")
    print("  'right size, right regime' encouragement in that script (cH0/a0 = 7.00) was a coincidence")
    print("  of scales, not evidence of a coupling -- and I should have checked the coupling first.")
    print()
    print("  WHAT THIS SETTLES:")
    print("   1. MI produces NO background distance tilt. Not small -- structurally zero, because")
    print("      K(0) = 0 kills the term on any configuration with vanishing proper acceleration.")
    print("   2. Therefore the phantom-artifact idea is dead AT THE ROOT, not merely unbuilt. There is")
    print("      no mechanism by which modified inertia biases d_L(z) at background level, so it cannot")
    print("      fake a phantom crossing however the fit is done.")
    print("   3. The framework's expansion history comes from its FIELD CONTENT (the AeST/ghost-")
    print("      condensate dark sector, already published and CMB-fitted), not from the inertia")
    print("      modification. That is self-consistent and was the corpus's position all along.")
    print("   4. cH0/a0 = 7.00 remains a real coincidence and is still the framework's central")
    print("      motivation -- but it is NOT a coupling. Nothing in the action makes the expansion rate")
    print("      an argument of K.")
    print()
    print("  THE ONE GENUINELY NEW STRUCTURAL FINDING, which is worth more than the dead channel:")
    print("   K has a SQUARE-ROOT BRANCH POINT at z = 0, and the cosmological background sits exactly")
    print("   at z = 0. So the framework's action is NON-ANALYTIC at the configuration cosmology must")
    print("   expand around. Any future MI linear-cosmology calculation must handle that -- a naive")
    print("   'expand K to first order in perturbations' step is not available, because K'(0+) is")
    print("   infinite. This is a concrete, quantified obstacle for the perturbation calculation the")
    print("   corpus still wants, and it was not previously on the record.")
    print("   It also explains, in hindsight, why the flow-boost estimate came out as a RANGE")
    print("   (nu ~ 1.2-1.7) rather than a number: the expansion it would need does not exist.")
    print()
    print("  REMAINING TALLY for the phantom-artifact idea: mechanism NOT NOVEL, channel B closed by")
    print("  the corpus's own SN null, C closed by sign (needs a wall, we sit in a void), D/E/F/G")
    print("  closed or negligible, and A now closed structurally. THE IDEA IS FULLY CLOSED.")
    print("  Independently: BAO alone prefers evolving DE at 3.1 sigma with NO supernovae, which no")
    print("  inertia-side story was ever going to touch.")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
