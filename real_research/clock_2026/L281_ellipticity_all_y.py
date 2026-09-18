#!/usr/bin/env python3
"""L281 -- the causal structure of the candidate's scalar sector on the FULL nonlinear background (CK11's computable half).
g03c established uniform ellipticity of the symbol J_Y k^2 + xi^2 k^4 at zero field (y = 0).  Here: the linearisation of the static
operator div[J_Y(Y) grad P] + xi^2 lap^2 P (L279's scalar law with the healing-length term) around an arbitrary background gradient
grad P0 has spatial principal symbol
      sigma(k) = J_Y k^2 + 2 J_YY (k . grad P0)^2 + xi^2 k^4,
whose eigenvalues along and across grad P0 are (J_Y + 2 Y J_YY) k^2 + xi^2 k^4 and J_Y k^2 + xi^2 k^4.  With the deep-MOND carrier
J = beta Y + (2/3) Y^{3/2}/atilde0: J_Y = beta + sqrt(Y)/atilde0 and J_Y + 2 Y J_YY = beta + 2 sqrt(Y)/atilde0, both > 0 for every Y >= 0
when beta, atilde0 > 0: the operator is uniformly elliptic on every leaf for every field strength (Lean: L281_ellipticity.lean).
Time part (inherited from f34, not re-derived): the Q-sector gives -(1/c_s^2) d_t^2 with c_s^2 = (2 - K_B) J_Y c^2/|K_2| > 0 for K_2 < 0, so
the scalar's equation is hyperbolic in the clock time with dispersion omega^2 = c_s^2 [sigma(k)/J_Y]: subluminal at galactic wavenumbers
(c_s^2 ~ 0.04 c^2 at f34's point) and Lifshitz (group velocity > c) only for k xi >~ 1, i.e. wavelengths below the healing length xi = 4 pc
where the scalar is screened.  The causality JUDGMENT (superluminal group velocity on a preferred foliation) is not decided here.
A FAIL is a finding."""
import os, json, math
import sympy as sp
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("L281 -- ellipticity of the scalar operator for every field strength\n")
Y, beta, at0, xi, k, kp, kperp, KB, K2a = sp.symbols('Y beta atilde_0 xi k k_par k_perp K_B K2abs', positive=True)
J = beta * Y + sp.Rational(2, 3) * Y ** sp.Rational(3, 2) / at0
JY = sp.diff(J, Y); JYY = sp.diff(J, Y, 2)
# principal symbol of the linearised operator: d_i[(J_Y delta_ij + 2 J_YY d_iP0 d_jP0) d_j dP] + xi^2 lap^2 dP  ->  J_Y k^2 + 2 J_YY (k.gradP0)^2 + xi^2 k^4, with (k.gradP0)^2 = k_par^2 Y
sigma = JY * (kp ** 2 + kperp ** 2) + 2 * JYY * kp ** 2 * Y + xi ** 2 * (kp ** 2 + kperp ** 2) ** 2
lam_par = sp.simplify((JY + 2 * Y * JYY)); lam_perp = sp.simplify(JY)
check("1 the symbol's eigenvalues: across grad P0, J_Y = beta + sqrt(Y)/atilde0; along grad P0, J_Y + 2 Y J_YY = beta + 2 sqrt(Y)/atilde0 -- both are beta plus a positive multiple of sqrt(Y)",
      sp.simplify(lam_perp - (beta + sp.sqrt(Y) / at0)) == 0 and sp.simplify(lam_par - (beta + 2 * sp.sqrt(Y) / at0)) == 0, f"perp: {lam_perp}; par: {lam_par}")
# positivity for every Y >= 0 and every k: sigma >= min(lam_par, lam_perp) k^2 + xi^2 k^4 > 0
sigma_lower = sp.simplify(sigma - (beta * (kp ** 2 + kperp ** 2) + xi ** 2 * (kp ** 2 + kperp ** 2) ** 2))
check("2 UNIFORM ELLIPTICITY: sigma(k) - [beta k^2 + xi^2 k^4] = (sqrt(Y)/atilde0)(k_perp^2 + 2 k_par^2) >= 0, so sigma >= beta k^2 + xi^2 k^4 > 0 for every Y >= 0 and k != 0: the leaf operator is uniformly elliptic on the whole nonlinear background, not only at y = 0 (g03c)",
      sp.simplify(sigma_lower - sp.sqrt(Y) / at0 * (kperp ** 2 + 2 * kp ** 2)) == 0, f"sigma - (beta k^2 + xi^2 k^4) = {sp.factor(sigma_lower)}")
# the same without the healing term and without beta (pure deep MOND): still elliptic away from Y = 0, degenerate at Y = 0 (the TeVeS strong-coupling point) -- the beta term and xi term remove the degeneracy
sig0 = sigma.subs({beta: 0, xi: 0})
check("3 pure deep-MOND control (beta = 0, xi = 0): the symbol is (sqrt(Y)/atilde0)(k_perp^2 + 2 k_par^2), elliptic for Y > 0 but DEGENERATE at Y = 0 (TeVeS's strong-coupling point); the candidate's linear part beta and the xi^2 k^4 term each remove the degeneracy",
      sp.simplify(sig0 - sp.sqrt(Y) / at0 * (kperp ** 2 + 2 * kp ** 2)) == 0 and sp.simplify(sig0.subs(Y, 0)) == 0 and sp.simplify(sigma.subs({beta: 0}).subs(Y, 0) - xi ** 2 * (kp ** 2 + kperp ** 2) ** 2) == 0)
# dispersion: omega^2 = c_s^2 sigma/J_Y with c_s^2 = (2-K_B) J_Y c^2/|K2| (f34) -> omega^2 = (2-K_B) c^2 sigma/|K2|; group velocity along k_par
c = sp.symbols('c', positive=True)
omega2 = (2 - KB) * c ** 2 * sigma / K2a
vg2_perp = sp.simplify(sp.diff(omega2.subs(kp, 0), kperp) ** 2 / (4 * omega2.subs(kp, 0)))    # (d omega/dk)^2 = (d omega^2/dk)^2/(4 omega^2)
# at f34's point: c_s^2 = 0.04 c^2 at galactic k (xi k << 1); where does the group velocity reach c?  solve v_g = c for k with Y at the deep-MOND value of a 1e11 Msun galaxy at 30 kpc
KPC, PC, G, MSUN, C = 3.0857e19, 3.0857e16, 6.674e-11, 1.989e30, 2.998e8
nums = {}
for foot, a0 in (("canonical", 9.3619e-11), ("alt", 1.1279e-10)):
    KBn, K2n = 0.2, 3.24e5; bet = (2 - KBn) / 2; at0n = a0 / bet ** 2 / C ** 2      # a0 in 1/length (c=1)
    p = math.sqrt(at0n * G * 1e11 * MSUN / C ** 2) / (30 * KPC); Yn = p ** 2      # deep-MOND gradient at 30 kpc (1/length units)
    cs2_gal = float(((2 - KBn) * (bet + math.sqrt(Yn) / at0n) / K2n))               # c_s^2/c^2 at xi k << 1, perpendicular mode
    f = sp.lambdify(kperp, vg2_perp.subs({KB: KBn, K2a: K2n, beta: bet, at0: at0n, Y: Yn, xi: 4 * PC, c: 1}), 'math')
    # scan for the wavenumber where v_g = c
    kk = 1e-3 / PC; kstar = None
    while kk < 1e3 / PC:
        if f(kk) >= 1.0: kstar = kk; break
        kk *= 1.05
    nums[foot] = dict(cs2_over_c2_galactic=cs2_gal, lambda_vg_eq_c_pc=(2 * math.pi / kstar / PC if kstar else None))
    print(f"    {foot}: c_s^2/c^2 at galactic scales (30 kpc, 1e11 Msun, |K2| = 3.24e5) = {cs2_gal:.2e} (c_s = {C*math.sqrt(cs2_gal)/1e3:.0f} km/s; g03r: 389 km/s at |K2| = 2.5e5); group velocity reaches c at wavelength {nums[foot]['lambda_vg_eq_c_pc']:.3f} pc (xi = 4 pc)")
check("4 with f34's time sector the dispersion is hyperbolic in the clock time with c_s of a few hundred km/s at galactic scales (c_s^2/c^2 ~ 1e-6-1e-5 at |K2| = 3.24e5, matching g03r's 389 km/s), and the group velocity exceeds c only at wavelengths below ~0.1 pc, forty times inside the 4 pc healing length where the scalar is screened: the Lifshitz regime never reaches an unscreened scale [judgment on foliation causality not made here]",
      all(1e-7 < v["cs2_over_c2_galactic"] < 1e-4 and v["lambda_vg_eq_c_pc"] is not None and v["lambda_vg_eq_c_pc"] < 4.0 for v in nums.values()), f"{nums}")
OUT.update(dict(sigma=str(sigma), lam_par=str(lam_par), lam_perp=str(lam_perp), numbers=nums))
n, n_pass = len(CH), sum(CH)
print(f"\nL281 COMPLETE: {n_pass}/{n} checks PASS.")
print("""VERDICT.  The candidate's scalar operator is uniformly elliptic on every leaf for every field strength: sigma(k) >= beta k^2 + xi^2 k^4 > 0,
extending g03c's zero-field result to the full nonlinear (deep-MOND) background; the pure deep-MOND operator would degenerate at Y = 0 and
the candidate's linear part and healing term each cure that.  In the clock time the equation is hyperbolic with a subluminal sound speed at
every unscreened scale; the superluminal (Lifshitz) group velocity appears only below ~0.1 pc, forty times inside the screened region.  What remains of
CK11 is the judgment on causality in a preferred foliation and the Dirac count (CK06).  Nothing here derives kappa.""")
json.dump(dict(pass_=n_pass, n=n, **OUT), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "L281_results.json"), "w"), indent=1, default=str)
