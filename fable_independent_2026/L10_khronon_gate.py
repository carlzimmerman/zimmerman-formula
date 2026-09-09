#!/usr/bin/env python3
"""
L10 -- the khronon gate: does the IC-series scalar survive the gates this repository has
       already established for a clock mode in this action class?
================================================================================================
L4 (L4_VERIFICATION.md) rebuilt the lead agent's IC5/IC6/IC7 action independently, confirmed every
load-bearing number, and found the local degree-of-freedom count to be 3, not 2: two tensor
polarisations plus ONE propagating gravitational scalar.  That scalar is healthy (reduced kinetic
Hessian A_0 = 0.4615 > 0, no ghost) and the DeWitt supermetric carries the GR value lambda = 1, so it
is a KHRONON-type mode -- the clock's own scalar -- not a Horava lambda-mode.  The programme's
requirement 2 admits a clock scalar PROVIDED it is separately identified, counted and shown healthy.
It is now identified and counted.  This lane asks the next question: does it survive its own
phenomenology?

THE GATES THIS REPOSITORY HAS ALREADY ESTABLISHED FOR EXACTLY THIS MODE (not rebuilt here, reused):
  * PPN preferred-frame.  g03v_fast_clock_branch.py derives, for the Einstein-aether/khronometric
    sector at the theory's own locus c_1 = -c_3 = K_B (so c_13 = 0), c_4 = c_14 - K_B:
        alpha_1 = -4 c_14,     alpha_2 = -c_14/2 + c_14^2/(2 c_2) + O(c_14^2),
    vanishing exactly at c_2* = c_14/(1 - 2 c_14).  Bound |alpha_2| < 4e-7.  g03v ASSERTS the closed
    form in a comment; section A below DERIVES it symbolically and proves it is K_B-free.
  * Clock tachyon.  g03w_growth_phi_dynamical.py finds the clock equation's condensate-background
    term to be tachyonic, T'' = (|K_2| Q_0^2 eps_0 a^-3 / c_14) T, k-independent, quoting 282 H_0 at
    a = 1 and 2.8e5 H_0 at a = 0.01 for c_14 = 1e-5.  Section A re-derives that rate from the
    Omega_d normalisation and shows |K_2| Q_0^2 CANCELS out of it.
  * Gravitational Cherenkov.  g03v_k2_pincer_closure.py V6 makes it a live gate in this repository:
    "a SUBluminal khronon would let ultra-high-energy cosmic rays radiate gravitationally, so the
    healthy corner needs c_khronon >= c, i.e. c_2 >= c_14".  Section D applies the same gate, with the
    quantitative bound stated and sourced, to the L4 mode's measured speed c_s^2 = 1/3.

WHAT THIS SCRIPT DOES
  A. CONTROLS.  Independent symbolic re-derivation of alpha_1, alpha_2 and the tachyon rate; four
     structural limits that can fail.
  B. THE MAPPING.  What plays c_14, c_2 and |K_2| Q_0^2 in the IC5/IC6/IC7 action, read off by hand
     from IC4_ACTION.md, IC5_ACTION.md and TENSOR_BALANCE.md.  Reported honestly: two of the three
     are NOT determined by the published files, and the precise missing input is named.
  C. THE ALLOWED REGION in (c_14, c_2, M) that any successful clock construction must land in --
     the deliverable the lead can use directly.
  D. CHERENKOV on the measured c_s^2 = 1/3, with the escape routes priced.
  E. VERDICT.

CHECKS THAT CAN FAIL
  K1 [CONTROL]   independent symbolic derivation reproduces g03v's closed form for alpha_2, its zero
                 c_2* = c_14/(1-2c_14), and its two published numbers (-4.72e-5, -5.90e-6);
  K2 [CONTROL]   structural limits: alpha_1 and alpha_2 are exactly K_B-free on the locus c_13 = 0,
                 and both vanish identically at c_14 = 0;
  K3 [CONTROL]   independent re-derivation of g03w's tachyon rate reproduces 282 H_0 and 2.8e5 H_0,
                 and shows the rate depends on c_14 and Omega_d ALONE (|K_2| Q_0^2 cancels);
  K4 [mapping]   is the (c_14, c_2, |K_2|Q_0^2) mapping determined by the lead's published files?
  K5a [region]   with the clock's background offset free, is there a nonempty (c_14, c_2, M) region
                 satisfying PPN + Cherenkov + no-tachyon simultaneously?
  K5b [region]   is that region still nonempty if the clock sector must carry Omega_d = 0.266?
  K6 [exp wall]  does the IC construction's own screening u^2 = 1 - exp(-|a|/a_0) put the Solar
                 System inside the PPN-allowed region?  (both a_0 footings)
  K7 [Cherenkov] is c_s^2 = 1/3 admissible for a gravitational-sector mode in this class?
  K8 [escape]    can the IC screening suppress the Cherenkov coupling along a 10 kpc Galactic
                 ultra-high-energy-cosmic-ray path?  (both a_0 footings)
  K9 [VERDICT]   is the lead's IC-series scalar viable as the programme's allowed clock mode, as
                 published?

NOTHING under closure_2026/integrable_clock_construction_2026/ is imported, executed or copied.  The
IC constants below were transcribed by hand from IC4_ACTION.md, exactly as L4 did.
"""
import sympy as sp, numpy as np, math, sys, time

T0 = time.time(); FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

def head(s):
    print("\n" + "=" * 118); print(s); print("=" * 118, flush=True)

A0_CANON, A0_ALT = 9.3619e-11, 1.1279e-10                                # both footings, every dimensional number
FOOT = (("canonical", A0_CANON), ("alt", A0_ALT))

print("=" * 118)
print("L10 -- the khronon gate: does the IC-series scalar survive the preferred-frame, tachyon and Cherenkov gates?")
print("=" * 118, flush=True)

# =====================================================================================================
head("A -- CONTROLS: independent re-derivation of the two gate formulas this repository already owns")
# =====================================================================================================
KB, c2, c14, c1, c3, c4 = sp.symbols('K_B c_2 c_14 c_1 c_3 c_4', real=True)

# Foster & Jacobson (2006) preferred-frame PPN parameters of Einstein-aether, in the repository's
# sign convention (the same two expressions g03v uses; written out here from the paper's form).
alpha1_gen = -8*(c3**2 + c1*c4)/(2*c1 - c1**2 + c3**2)
alpha2_gen = alpha1_gen/2 - (c1 + 2*c3 - c4)*(2*c1 + 3*c2 + c3 + c4)/((c1 + c2 + c3)*(2 - (c1 + c4)))

# The theory's own locus (THE_ACTION_2026-09-05 section 2): c_1 = -c_3 = K_B  (=> c_13 = 0, required by
# c_T = c / GW170817), and c_4 = c_14 - K_B by the definition c_14 = c_1 + c_4.
LOCUS = {c1: KB, c3: -KB, c4: c14 - KB}
a1 = sp.simplify(alpha1_gen.subs(LOCUS))
a2 = sp.simplify(sp.together(sp.simplify(alpha2_gen.subs(LOCUS))))
print(f"    on the locus c_1 = -c_3 = K_B, c_4 = c_14 - K_B:")
print(f"      alpha_1 = {sp.simplify(a1)}")
print(f"      alpha_2 = {sp.factor(sp.simplify(a2))}")

# closed form and its small-c_14 expansion
a2_series = sp.expand(sp.simplify(sp.series(a2, c14, 0, 3).removeO()))
print(f"      alpha_2 expanded to O(c_14^2) at fixed c_2:  {a2_series}  =  {sp.expand(a2_series)}")
target = -c14/2 + c14**2/(2*c2)                                          # the two-term form g03v's comment asserts
extra = sp.simplify(a2_series - target)
print(f"      g03v's comment asserts alpha_2 = -c_14/2 + c_14^2/(2 c_2) + O(c_14^2); the exact expansion carries one more")
print(f"      quadratic term, {extra}, which the comment folds into its O(c_14^2).  Reported as a refinement, not a discrepancy:")
print(f"      the two-term form is exact in the limit c_2 << 1, which is the regime the closure locus lives in.")
same_closed = sp.simplify(extra - 3*c14**2/4) == 0
# exact zero of alpha_2
zeros = sp.solve(sp.numer(sp.together(a2)), c2)
c2star_sym = sp.simplify([z for z in zeros if sp.simplify(z - c14/(1 - 2*c14)) == 0 or True][0])
print(f"      alpha_2 = 0 exactly at c_2* = {sp.simplify(c2star_sym)}  (= c_14/(1 - 2 c_14))")
same_zero = sp.simplify(c2star_sym - c14/(1 - 2*c14)) == 0

# the two published numbers of g03v
fa1 = sp.lambdify((KB, c2, c14), a1, 'math'); fa2 = sp.lambdify((KB, c2, c14), a2, 'math')
a1_c, a2_c = float(fa1(0.2, 1.0, 1.18e-5)), float(fa2(0.2, 1.0, 1.18e-5))
print(f"      at g03v's corner (K_B = 0.2, c_2 = 1, c_14 = 1.18e-5): alpha_1 = {a1_c:.3e}, alpha_2 = {a2_c:.3e}"
      f"   (g03v / f33 published: -4.72e-5, -5.90e-6)")
c2star_num = 1e-5/(1 - 2e-5); a2_at_star = float(fa2(0.2, c2star_num, 1e-5))
print(f"      at c_2 = c_2*(c_14 = 1e-5) = {c2star_num:.6e}: alpha_2 = {a2_at_star:.2e}  (numerically zero)")
check("K1 [CONTROL] the independent symbolic derivation reproduces g03v's closed form for alpha_2 (with its omitted 3c_14^2/4 "
      "term identified), its exact zero c_2* = c_14/(1-2c_14), and both published numbers",
      same_closed and same_zero and abs(a1_c/(-4.72e-5) - 1) < 1e-3 and abs(a2_c/(-5.90e-6) - 1) < 1e-3 and abs(a2_at_star) < 1e-12,
      f"exact alpha_2 = -c_14(2c_14c_2 + c_14 - c_2)/(c_2(c_14-2)); expansion = -c_14/2 + c_14^2/(2c_2) + 3c_14^2/4 "
      f"{'(confirmed)' if same_closed else '(DIFFERS)'}; c_2* {'identical' if same_zero else 'DIFFERS'}; "
      f"alpha_1 = {a1_c:.3e} vs -4.72e-5, alpha_2 = {a2_c:.3e} vs -5.90e-6, alpha_2(c_2*) = {a2_at_star:.1e}")

# structural limits
KB_free = (sp.simplify(sp.diff(a1, KB)) == 0) and (sp.simplify(sp.diff(a2, KB)) == 0)
a1_at_zero = sp.simplify(a1.subs(c14, 0)); a2_at_zero = sp.simplify(a2.subs(c14, 0))
print(f"      d(alpha_1)/dK_B = {sp.simplify(sp.diff(a1, KB))}, d(alpha_2)/dK_B = {sp.simplify(sp.diff(a2, KB))}"
      f"   -> K_B is pure gauge for a hypersurface-orthogonal clock, as it must be")
print(f"      at c_14 = 0: alpha_1 = {a1_at_zero}, alpha_2 = {a2_at_zero}  (GR limit of the preferred-frame sector)")
check("K2 [CONTROL] alpha_1 and alpha_2 are exactly K_B-free on the locus c_13 = 0 (K_B is pure gauge for a "
      "hypersurface-orthogonal clock) and both vanish identically at c_14 = 0",
      KB_free and a1_at_zero == 0 and a2_at_zero == 0,
      f"dK_B derivatives {'both zero' if KB_free else 'NONZERO'}; alpha_1(c_14=0) = {a1_at_zero}, alpha_2(c_14=0) = {a2_at_zero}")

# --- the tachyon rate, re-derived ---
print(f"\n    g03w's clock tachyon: T'' = (|K_2| Q_0^2 eps_0 a^-3 / c_14) T.  g03v fixes the background offset by")
print(f"    Omega_d:  eps_0 = 3 H_0^2 Omega_d / (|K_2| Q_0^2), so the product |K_2| Q_0^2 eps_0 = 3 Omega_d H_0^2 is")
print(f"    a FIXED number and the stiffness CANCELS.  The rate therefore depends on c_14 and Omega_d alone:")
Om_d = 0.266
def tachyon_rate(c14v, a, Omd=Om_d):                                     # in units of H_0
    return math.sqrt(3*Omd*a**-3/c14v)
r1, r001 = tachyon_rate(1e-5, 1.0), tachyon_rate(1e-5, 0.01)
print(f"        rate/H_0 = sqrt(3 Omega_d a^-3 / c_14);  at c_14 = 1e-5:  a = 1 -> {r1:.1f} H_0,  a = 0.01 -> {r001:.2e} H_0")
print(f"        g03w published:                                                   282 H_0            2.8e+05 H_0")
check("K3 [CONTROL] the independently re-derived tachyon rate reproduces g03w's two published numbers and shows the rate is "
      "set by c_14 and Omega_d alone -- |K_2| Q_0^2 cancels against the Omega_d normalisation of eps_0",
      abs(r1/282.0 - 1) < 0.01 and abs(r001/2.8e5 - 1) < 0.02,
      f"a = 1: {r1:.1f} vs 282 H_0; a = 0.01: {r001:.3e} vs 2.8e5 H_0")

# =====================================================================================================
head("B -- THE MAPPING: what plays c_14, c_2 and |K_2| Q_0^2 in the lead's IC5/IC6/IC7 action?")
# =====================================================================================================
# IC-4 constants, transcribed by hand from IC4_ACTION.md (as L4 did).  Nothing imported.
ell = math.log(9/5); Tc = -27/16 + 54/(5*ell); e_ic = 1/8; d_ic = -9*e_ic/Tc
alpha_ic = 81*e_ic/Tc**2
beta_ic = 2*d_ic - 1/3 - 3*alpha_ic/4
gamma_ic = e_ic - 1/16 + 9*alpha_ic/64 - 3*d_ic/4
b_ic = -Tc/9 - 3/8
a_star = 3 - 81/(4*Tc); sigma = 1/3
p_R = 8/3 + 4*a_star*sigma; q_R = -1 - 3*p_R/8
A_R = 3*p_R/(16*ell**2); B_R = 3*q_R/(16*ell**2)
u0, xi0 = 2/3, 1/4                                                      # the expanding witness (N_0 = e^{1/4} => xi = ln N = 1/4)
print(f"    IC-4 frozen constants (hand-transcribed): ell = {ell:.12f}, T = {Tc:.12f}, alpha = {alpha_ic:.12f}, b = {b_ic:.12f},")
print(f"                                              a_* = {a_star:.9f}, sigma = {sigma}, A_R = {A_R:.9f}, B_R = {B_R:.9f}")
print(f"    witness: (xi, u) = ({xi0}, {u0:.6f});  F = A_R(xi - 1/4) + B_R(u - 2/3) = 0 there, exactly.")

print(f"\n    B.1  The khronometric dictionary.  For a hypersurface-orthogonal clock, grad_mu n_nu = K_mu_nu - n_mu a_nu, so")
print(f"         the Einstein-aether Lagrangian collapses to    L = (m/2)[ (1 - c_13) K_ij K^ij - (1 + c_2) K^2 + R^(3) + c_14 a^2 ],")
print(f"         i.e. in ADM trace/trace-free variables          L = (m/2)[ (1 - c_13) K_TF^2 - (2/3 + c_2) K^2 + R^(3) + c_14 a^2 ].")
print(f"         Only the three combinations (c_13, c_2, c_14) are physical: K_B drops out (proved in K2).")

print(f"\n    B.2  c_13 = 0 -- DETERMINED.  IC-5's exact canonical map gives H_b = (2 e^(..)/(mV))(pi_TF^2 - pi^2/6), and")
print(f"         GR's ADM Hamiltonian is (16 pi G/sqrt(h))(pi_ij pi^ij - pi^2/2) = (2/(m sqrt(h)))(pi_TF^2 - pi^2/6) at m = 1/(8 pi G),")
print(f"         since pi_ij pi^ij = pi_TF^2 + pi^2/3.  IC-6's plateau Lagrangian L_6 = (m/2)[Q_TF^2 + Rhat - (2/3)Q^2/K_6 - 2C + ...]")
print(f"         carries UNIT coefficient on Q_TF^2, so c_13 = 0 exactly -- consistent with c_T = 1 (TENSOR_BALANCE) and with L4's")
print(f"         DeWitt lambda = 1.  This is the one clean, unambiguous entry in the dictionary.")

print(f"\n    B.3  c_2 -- DERIVED FORMULA, but it VANISHES where the mode was measured.  Matching the K^2 coefficient of L_6,")
print(f"         2/3 + c_2 = (2/3)/K_6  with  K_6 = 1 + 3 F Y/(2 a_0^2),  Y = Rhat + Q_TF^2,  gives")
print(f"                 c_2 = (2/3)(1/K_6 - 1) = - F Y / (a_0^2 K_6).")
print(f"         At the expanding witness F = 0 (by construction) and Y = 0 (homogeneous, isotropic), so c_2 = 0 EXACTLY there.")
print(f"         c_2 = 0 with c_14 > 0 sits on the c_123 = c_1 + c_2 + c_3 = 0 locus, which is the POLE of alpha_2 and the point")
print(f"         where the khronometric spin-0 speed s_0^2 = c_2(2 - c_14)/(c_14(2 + 3c_2)) -> 0.  L4 measured c_s^2 = 1/3, NOT 0.")
print(f"         => the pure khronometric dictionary is INCONSISTENT with the IC construction: the IC scalar takes its gradient")
print(f"         energy from the AUXILIARY sector (the barred curvature Rhat = R^(3)[h] + 4 Delta w - 2|Dw|^2 with w = (u-1)xi,")
print(f"         and the alpha|D(xi + b u)|^2 term), not from c_2.  There is no c_2 to read off at the witness.")

print(f"\n    B.4  c_14 -- NOT DETERMINED: three internally consistent readings of the same published action disagree.")
c14_ic4 = 2*(1 - u0**2)                                                  # IC-4's explicit 2(1-u^2) a_mu a^mu term, at u = 2/3
c14_plat = 2*alpha_ic                                                    # IC-5/IC-6 eta = 1 plateau: 2 alpha |D(xi + b u)|^2
c14_bar = 2*((1 - u0)**2 + (1 - u0**2))                                  # IC-4 rewritten in barred variables (Rhat), a^2 coefficient
print(f"         (i)   IC-4's explicit term (m/2)*2(1-u^2) a_mu a^mu           ->  c_14 = 2(1 - u^2)  = {c14_ic4:.6f} at u = 2/3")
print(f"         (ii)  IC-5/IC-6 on the eta = 1 plateau, (m/2)*2 alpha|D(xi+bu)|^2 ->  c_14 = 2 alpha    = {c14_plat:.6f}")
print(f"         (iii) IC-4 rewritten in the barred variables IC-5 actually uses.  Rhat = R^(3)[h] + 4 Delta w - 2|Dw|^2 with")
print(f"               w = (u-1)xi, so trading R^(3) for Rhat moves m|Dw|^2 = m[(u-1)^2 a^2 + 2(u-1)xi a.Du + xi^2|Du|^2] into")
print(f"               the a^2 slot: c_14 = 2[(u-1)^2 + (1-u^2)] = 4(1 - u) = {c14_bar:.6f} at u = 2/3")
print(f"         All three are O(0.07 - 1.4).  They differ by up to a factor {c14_bar/c14_plat:.1f}, so the published files do not fix c_14;")
print(f"         what is ROBUST is only the order of magnitude: c_14 = O(10^-1 - 1) at the expanding witness.")
print(f"         One structural note that matters below: readings (i) and (iii) both carry the u-dependence and so both")
print(f"         asymptote to 2 exp(-|a|/a_0) on the static regular branch; reading (ii) is u-INDEPENDENT and does not screen")
print(f"         at all.  (ii) is the eta = 1 plateau, and IC-5 puts the static regime at eta = 0 (r = 0 gives |r^2-1| = 1 >= 1/2),")
print(f"         so (ii) is not the branch operative where PPN is measured.  The exp wall in section D is therefore legitimate.")
c14_range = (min(c14_ic4, c14_plat, c14_bar), max(c14_ic4, c14_plat, c14_bar))

print(f"\n    B.5  |K_2| Q_0^2 -- NO COUNTERPART AT ALL.  g03w's tachyon needs a CONDENSATE: a second scalar phi with a")
print(f"         stiffness K(Q) whose background charge Qbar sits a fraction eps_0 off its minimum, supplying the dust")
print(f"         density 2|K_2| Q_0^2 eps_0 a^-3.  The IC action has no such field: its only extra scalar is the auxiliary u,")
print(f"         which carries a potential a_0^2 U(u^2) and NO independent kinetic term (IC-4: 'the correction has no")
print(f"         independent Ndot or udot').  The dust/tachyon arm therefore CANNOT be evaluated from the published files.")
print(f"         MISSING INPUT, named precisely: the mass matrix of the propagating scalar zeta on the expanding witness --")
print(f"         i.e. the O(k^0) term of the same reduced system that gave L4 its A_0 = 0.4615 and c_s^2 = 1/3.  If that mass")
print(f"         term is negative the IC construction has its own tachyon and this gate fires; if positive it does not.  L4")
print(f"         explicitly lists that reduction as OUT OF SCOPE, and IC7 quotes only the k -> large speed 0.388526918.")

print(f"\n    B.6  WHAT IS DETERMINED, AND IT IS THE ONE THAT DECIDES.  The scalar's SPEED is an invariant of the mode, not a")
print(f"         parametrisation choice, and L4 measured it: c_s^2 = 1/3 at the witness (IC7 with its counterterm: 0.3886).")
print(f"         In this class the khronon speed is c_s^2 = c_2/c_14 to leading order (the relation g03v_k2_pincer_closure V5")
print(f"         uses).  Inverting it gives the EFFECTIVE ratio the IC construction must be carrying:")
cs2_L4, cs2_IC7 = 1/3, 0.388526918
print(f"                 c_2^eff / c_14^eff = c_s^2 = {cs2_L4:.6f}   (IC7 variant {cs2_IC7:.6f})")
a2_ratio = sp.simplify(a2.subs(c2, c14/sp.Rational(3)))
print(f"         and then alpha_2 collapses to a ONE-parameter function of c_14 alone:  alpha_2 = {sp.factor(a2_ratio)}")
print(f"                 -> alpha_2 = +c_14 + O(c_14^2)  (the c_14^2/(2c_2) term is 3c_14/2 and OVERTURNS the sign of -c_14/2)")
f_ratio = sp.lambdify(c14, a2_ratio, 'math')
c14_ppn_max = float(sp.nsolve(sp.Eq(a2_ratio, sp.Rational(4, 10**7)), c14, 4e-7))
print(f"         |alpha_2| < 4e-7 then requires   c_14 <= {c14_ppn_max:.4e}   -- the binding PPN requirement on the IC mode.")
print(f"         (alpha_1 = -4 c_14 with |alpha_1| < 1e-4 gives only c_14 <= 2.5e-5, so alpha_2 is 63x tighter here.)")
check("K4 [mapping] the (c_14, c_2, |K_2| Q_0^2) mapping is determined by the lead's published files",
      False,
      "c_13 = 0 DETERMINED; c_2 = -F Y/(a_0^2 K_6) DERIVED but identically 0 at the witness where the mode was measured, which "
      "contradicts c_s^2 = 1/3 and shows the scalar's gradient energy is auxiliary-sector, not c_2; c_14 has THREE inconsistent "
      f"readings spanning {c14_range[0]:.3f}-{c14_range[1]:.3f}; |K_2| Q_0^2 has NO counterpart (no condensate in the IC action). "
      "Missing inputs: (a) the PPN/weak-field expansion of the IC action with the auxiliary constraint solved -- IC-5 states its "
      "full metric/clock variation 'has not been expanded in this package'; (b) the O(k^0) mass term of the reduced scalar system")

# =====================================================================================================
head("C -- THE ALLOWED REGION any successful clock construction must land in (the deliverable)")
# =====================================================================================================
ALPHA1_BOUND, ALPHA1_BOUND_TIGHT = 1e-4, 4e-5                            # Will 2014 LLR; the tighter quoted value
ALPHA2_BOUND = 4e-7                                                      # the bound g03v uses
print(f"    Constraints, all three already established in this repository, restated as one region in (c_14, c_2, M) with")
print(f"    M = |K_2| Q_0^2 eps_0 / H_0^2  (the clock/condensate sector's background off-minimum energy, in H_0^2 units):")
print(f"      (1) PPN alpha_1 = -4 c_14,  |alpha_1| < {ALPHA1_BOUND:.0e}       ->  c_14 <= {ALPHA1_BOUND/4:.2e}   (tighter {ALPHA1_BOUND_TIGHT:.0e}: {ALPHA1_BOUND_TIGHT/4:.2e})")
print(f"      (2) PPN alpha_2 exact (section A),  |alpha_2| < {ALPHA2_BOUND:.0e}   ->  a band in c_2 about c_2* = c_14/(1 - 2 c_14)")
print(f"      (3) gravitational Cherenkov (g03v_k2_pincer_closure V6): the khronon must not be subluminal,")
print(f"          c_s^2 = c_2/c_14 >= 1 - 2e-15        ->  c_2 >= c_14  to within 2e-15")
print(f"      (4) no clock tachyon faster than expansion: rate = sqrt(M a^-3/c_14) H_0 <= H_0 at a = 1  ->  M <= c_14")

a2_num = sp.lambdify((c14, c2), a2, 'math')
def c2_band(c14v, eps=ALPHA2_BOUND):
    """exact alpha_2 band: c_2 in [c14^2/(c14(1-2c14) + eps(2-c14)), c14^2/(c14(1-2c14) - eps(2-c14))]"""
    lo_den = c14v*(1 - 2*c14v) + eps*(2 - c14v); hi_den = c14v*(1 - 2*c14v) - eps*(2 - c14v)
    lo = c14v**2/lo_den
    hi = c14v**2/hi_den if hi_den > 0 else math.inf
    return lo, hi

print(f"\n    THE REGION.  For each c_14 the admissible c_2 is [max(c_14, alpha_2 lower edge), alpha_2 upper edge]:")
print(f"      {'c_14':>10} {'c_2 lower':>14} {'c_2 upper':>14} {'binds below':>13} {'c_s^2 = c_2/c_14':>18} {'M_max':>10} {'Omega_off,max':>15}")
rows = []
for c14v in (1e-8, 1e-7, 4e-7, 1e-6, 4e-6, 1e-5, 2.5e-5):
    lo, hi = c2_band(c14v)
    lo_eff = max(lo, c14v*(1 - 2e-15)); binder = "Cherenkov" if lo_eff > lo*(1 + 1e-12) else "alpha_2"
    ok = (c14v <= ALPHA1_BOUND/4) and (hi > lo_eff)
    cs_lo = lo_eff/c14v; cs_hi = hi/c14v if math.isfinite(hi) else math.inf
    Mmax = c14v; Om_max = Mmax/3
    rows.append((c14v, lo_eff, hi, ok, Om_max))
    print(f"      {c14v:10.1e} {lo_eff:14.5e} {hi:14.5e} {binder:>13} {('[%.3f, %s]' % (cs_lo, ('inf' if not math.isfinite(cs_hi) else '%.3f' % cs_hi))):>18} {Mmax:10.1e} {Om_max:15.2e}")
nonempty = any(r[3] for r in rows)
print(f"\n    In words, the target: c_14 <= {ALPHA1_BOUND/4:.1e}; c_2 in a narrow collar just ABOVE c_14, of fractional width")
print(f"    ~ 2 * {ALPHA2_BOUND:.0e} / c_14 about c_2* = c_14/(1 - 2c_14) -- for c_14 <= 8e-7 the collar opens upward without limit,")
print(f"    for c_14 > 8e-7 it closes to a band; and M <= c_14, i.e. the clock's off-minimum background may carry at most")
print(f"    Omega_off = M/3 <= {ALPHA1_BOUND/12:.1e} of the critical density.")
check("K5a [region] with the clock's background offset free, a nonempty (c_14, c_2, M) region satisfies PPN alpha_1, PPN alpha_2, "
      "Cherenkov and no-tachyon SIMULTANEOUSLY",
      nonempty,
      f"nonempty for every c_14 <= {ALPHA1_BOUND/4:.1e}; Cherenkov (c_2 >= c_14) and the alpha_2 zero (c_2* = c_14/(1-2c_14) > c_14) "
      f"are compatible because c_2* exceeds c_14 by the factor 1/(1-2c_14); the region is a thin collar just above the Cherenkov line")

M_dust = 3*Om_d
print(f"\n    Now the second arm.  If the clock/condensate sector must supply the dark component, g03v's normalisation fixes")
print(f"    M = 3 Omega_d = {M_dust:.4f}, whereas the region above allows M <= c_14 <= {ALPHA1_BOUND/4:.1e}.")
print(f"    Shortfall in M: {M_dust/(ALPHA1_BOUND/4):.2e}x;  equivalently the rate at a = 1 is {tachyon_rate(ALPHA1_BOUND/4, 1.0):.0f} H_0 at the largest allowed c_14.")
check("K5b [region] the region is still nonempty if the clock sector must carry Omega_d = 0.266",
      M_dust <= ALPHA1_BOUND/4,
      f"M required = 3 Omega_d = {M_dust:.3f}, M allowed <= c_14 <= {ALPHA1_BOUND/4:.1e}: EMPTY by {M_dust/(ALPHA1_BOUND/4):.1e}x. "
      f"This is g03w's pincer restated exactly: PPN pushes c_14 down, the tachyon rate ~ 1/sqrt(c_14) pushes it up. "
      f"The IC construction is NOT caught by this arm as published, because it has no condensate carrying Omega_d (B.5) -- "
      f"its own mass term is the missing input")

# =====================================================================================================
head("D -- the exponential wall, and where it does and does not work")
# =====================================================================================================
GM_SUN = 1.32712440018e20; AU = 1.495978707e11; kpc = 3.0857e19
print(f"    The IC construction's escape from c_14 = O(1) is its own static regular branch (IC-4, unchanged in IC-5):")
print(f"          u^2 = 1 - exp(-|a|/a_0),   so   c_14 = 2(1 - u^2) = 2 exp(-|a|/a_0).")
print(f"    This screens c_14 exponentially in the strong-field regime -- the 'exp wall'.  Required: c_14 <= {c14_ppn_max:.2e}")
print(f"    (section B.6, the c_s^2 = 1/3 mapping), i.e. |a|/a_0 >= ln(2/{c14_ppn_max:.2e}) = {math.log(2/c14_ppn_max):.2f}.")
thresh = math.log(2/c14_ppn_max)
print(f"\n      {'site':<34} {'|a| [m/s^2]':>12} {'|a|/a_0 canonical':>19} {'|a|/a_0 alt':>13} {'c_14 = 2exp(-|a|/a_0)':>25}")
sites = [("Earth orbit, 1 AU", GM_SUN/AU**2),
         ("Cassini at Saturn, 9.54 AU", GM_SUN/(9.537*AU)**2),
         ("Solar System edge, 100 AU", GM_SUN/(100*AU)**2),
         ("Milky Way at R_sun (v_c=220km/s)", (220e3)**2/(8.2*kpc)),
         ("Milky Way at 10 kpc", (220e3)**2/(10*kpc))]
solar_ok = True
for nm, g in sites:
    xs = [g/A0_CANON, g/A0_ALT]; x_worst = min(xs)                       # the weaker screening of the two footings
    c14_w = f"{2*math.exp(-x_worst):.3e}" if x_worst < 690 else f"2 exp(-{x_worst:.3g})  [underflow]"
    print(f"      {nm:<34} {g:12.3e} {xs[0]:19.4g} {xs[1]:13.4g} {c14_w:>25}")
    if "AU" in nm and 2*math.exp(-min(x_worst, 700)) > c14_ppn_max: solar_ok = False
check("K6 [exp wall] the IC construction's own screening puts the Solar System inside the PPN-allowed region on BOTH a_0 footings",
      solar_ok,
      f"the PPN threshold is |a| >= {thresh:.1f} a_0 = {thresh*A0_CANON:.2e} (canonical) / {thresh*A0_ALT:.2e} (alt) m/s^2; "
      f"Cassini sits at {GM_SUN/(9.537*AU)**2/A0_ALT:.2e} a_0, {GM_SUN/(9.537*AU)**2/A0_ALT/thresh:.1e}x above threshold, so "
      f"c_14 there is exp(-5.8e5) -- zero for every practical purpose.  The PPN arm PASSES, and it passes by an enormous margin. "
      f"Reported cost, not a check: c_14 -> 0 is also the strong-coupling limit of a khronometric clock (the mode's kinetic "
      f"normalisation is proportional to c_14), so the Solar System is where this mode becomes infinitely strongly coupled")

print(f"\n    But note WHERE the wall stops working: it is a function of |a|/a_0, so it is fully OFF exactly in the MOND regime.")
print(f"    Preferred-frame effects in this construction are unscreened below |a| ~ {thresh:.0f} a_0 = {thresh*A0_CANON:.2e} / {thresh*A0_ALT:.2e} m/s^2,")
print(f"    which is the whole of a galaxy outside ~1 kpc.  That is where the next gate is evaluated.")

# =====================================================================================================
head("E -- gravitational Cherenkov on the measured c_s^2 = 1/3")
# =====================================================================================================
print(f"    THE BOUND AND ITS SOURCE.  A gravitational-sector mode that propagates SUBluminally lets an ultra-relativistic")
print(f"    particle radiate into it (gravitational Cherenkov).  Moore & Nelson, JHEP 0109:023 (2001), 'Lower bound on the")
print(f"    propagation speed of gravity from gravitational Cherenkov radiation': the survival of cosmic-ray primaries at")
print(f"    E ~ 1e11 GeV over a Galactic path L ~ 10 kpc requires 1 - v_g <~ 2e-15 for a mode coupled with gravitational")
print(f"    strength (extragalactic sources tighten this to ~1e-19).  Elliott, Moore & Stoica, JHEP 0508:066 (2005), applied")
print(f"    it to Einstein-aether and bounded ALL THREE aether mode speeds -- spin-2, spin-1 and spin-0 -- the same way.")
print(f"    THIS REPOSITORY ALREADY USES THIS GATE: g03v_k2_pincer_closure.py V6 turns 'the healthy corner needs")
print(f"    c_khronon >= c, i.e. c_2 >= c_14' into the standing bound |K_2| <= (2 - K_B)^2/c_14 = 3.24e5.  Same gate, same mode.")
CHER = 2e-15
for lab, cs2 in (("L4, at the witness", cs2_L4), ("IC7 with its c_7 counterterm", cs2_IC7)):
    cs = math.sqrt(cs2); print(f"      {lab:<32}: c_s^2 = {cs2:.9f}, c_s = {cs:.9f}, 1 - c_s = {1-cs:.6f}  -> exceeds the bound by {(1-cs)/CHER:.2e}x")
cher_ok = (1 - math.sqrt(cs2_L4)) <= CHER
check("K7 [Cherenkov] the L4 mode's sound speed c_s^2 = 1/3 is admissible for a gravitational-sector mode in this class",
      cher_ok,
      f"1 - c_s = {1-math.sqrt(cs2_L4):.4f} against the bound 1 - c_s <= 2e-15 (Moore & Nelson 2001; Elliott, Moore & Stoica 2005; "
      f"the same gate g03v_k2_pincer_closure V6 already imposes on this repository's khronon): EXCLUDED by "
      f"{(1-math.sqrt(cs2_L4))/CHER:.1e}x.  IC7's own 0.3886 fails by {(1-math.sqrt(cs2_IC7))/CHER:.1e}x")

print(f"\n    THE ONE ESCAPE, PRICED.  The Cherenkov rate is linear in the mode's effective Newton coupling, so a coupling")
print(f"    suppressed by a factor s relaxes the bound to 1 - c_s <= 2e-15/s.  Tolerating 1 - c_s = {1-math.sqrt(cs2_L4):.4f} needs")
s_need = CHER/(1 - math.sqrt(cs2_L4))
print(f"          s <= {s_need:.2e}.")
print(f"    The IC construction's only suppression parameter is the same exp wall, and the MOST FAVOURABLE reading of it")
print(f"    gives s ~ c_14/2 = exp(-|a|/a_0).  (This is generous to the construction: the mode's kinetic normalisation is")
print(f"    proportional to c_14, so canonically normalising it makes the coupling scale as 1/sqrt(c_14) and grow as the wall")
print(f"    screens -- the honest expectation is that small c_14 makes this WORSE, not better.)  Even so it requires")
xreq = -math.log(s_need)
print(f"          |a|/a_0 >= {xreq:.1f}  EVERYWHERE along the cosmic-ray path.")
print(f"      {'footing':<12} {'required |a| [m/s^2]':>21} {'MW radius where reached':>26} {'path length available':>23}")
esc_ok = False
for nm, a0v in FOOT:
    a_req = xreq*a0v; r_req = (220e3)**2/a_req/kpc                       # flat rotation curve, v_c = 220 km/s
    print(f"      {nm:<12} {a_req:21.3e} {('r <= %.2f kpc' % r_req):>26} {('%.2f kpc' % r_req):>23}")
    if r_req >= 10.0: esc_ok = True
print(f"    A 10 kpc Galactic path needs the whole path inside that radius.  It is not: the Galaxy reaches {xreq:.0f} a_0 only")
print(f"    within a few tenths of a kpc of the centre, and the cosmic-ray path is 10 kpc.  The exp wall CANNOT rescue this gate,")
print(f"    and the reason is structural: the wall is a function of |a|/a_0 and the Cherenkov gate is evaluated exactly where")
print(f"    |a| ~ a_0.  The gate that PPN escapes and the gate that Cherenkov imposes are read at opposite ends of the same variable.")
check("K8 [escape] the IC screening can suppress the Cherenkov coupling along a 10 kpc Galactic ultra-high-energy cosmic-ray path "
      "(both a_0 footings)",
      esc_ok,
      f"the required suppression s <= {s_need:.1e} needs |a| >= {xreq:.0f} a_0 = {xreq*A0_CANON:.2e} / {xreq*A0_ALT:.2e} m/s^2 along "
      f"the whole path; a v_c = 220 km/s Galaxy reaches that only within {(220e3)**2/(xreq*A0_ALT)/kpc:.2f}-{(220e3)**2/(xreq*A0_CANON)/kpc:.2f} kpc "
      f"of the centre, {10/((220e3)**2/(xreq*A0_CANON)/kpc):.0f}x short of the 10 kpc path")

print(f"\n    THE REPAIR, AND IT IS INSIDE THE PUBLISHED DESIGN SPACE.  IC4_ACTION.md calls sigma 'the squared-speed parameter',")
print(f"    sets sigma = 1/3 as a 'fixed design parameter', and states 'more generally the calculation covers 0 < sigma <= 1'.")
print(f"    L4 measured c_s^2 = 1/3 = sigma exactly.  If c_s^2 = sigma (a hypothesis this lane cannot verify without the lead's")
print(f"    reduced system, and which the lead should confirm or refute), then the Cherenkov gate collapses the design interval")
print(f"    0 < sigma <= 1 to the single endpoint")
print(f"          sigma in [1 - 4e-15, 1],   i.e. sigma = 1 to within 4e-15,")
print(f"    a set of measure 4e-15 inside the published domain, with sigma > 1 (superluminal, Cherenkov-safe by the repository's")
print(f"    own precedent) lying outside it.  sigma = 1/3 is excluded by {(1-math.sqrt(cs2_L4))/CHER:.1e}x.  Note that sigma enters")
print(f"    p_R = 8/3 + 4 a_* sigma and hence A_R, B_R, F -- so moving sigma is NOT free: it moves the IC6 obstruction, the IC7")
print(f"    counterterm and the tensor balance, all of which L4 verified only at sigma = 1/3.  That re-verification is the work.")
print(f"      sigma = 1/3 (published):  p_R = {p_R:.9f}, A_R = {A_R:.9f}, B_R = {B_R:.9f}")
p_R1 = 8/3 + 4*a_star*1.0; q_R1 = -1 - 3*p_R1/8
print(f"      sigma = 1   (required):   p_R = {p_R1:.9f}, A_R = {3*p_R1/(16*ell**2):.9f}, B_R = {3*q_R1/(16*ell**2):.9f}   "
      f"(A_R changes by {3*p_R1/(16*ell**2)/A_R:.3f}x)")

# =====================================================================================================
head("F -- VERDICT")
# =====================================================================================================
print(f"    Arm by arm, on the lead's construction as published:")
print(f"      PPN alpha_1, alpha_2 ...... PASSES, via the exp wall.  c_14 = 2 exp(-|a|/a_0) is 2 exp(-5.8e5) at Cassini, i.e.")
print(f"                                  ~250,000 decades below the requirement c_14 <= {c14_ppn_max:.1e} that the mapping generates.")
print(f"                                  Cost recorded: that limit is also the mode's strong-coupling limit.")
print(f"      clock tachyon ............. UNDETERMINED.  The IC action has no condensate, so g03w's rate has no image in it.")
print(f"                                  The missing input is the O(k^0) mass term of the same reduced scalar system that")
print(f"                                  produced A_0 = 0.4615 and c_s^2 = 1/3.  This is a real open door, not a pass.")
print(f"      gravitational Cherenkov ... FAILS, by {(1-math.sqrt(cs2_L4))/CHER:.1e}x, on a gate this repository already imposes on its own")
print(f"                                  khronon.  The failure is NOT screened, because it is read where |a| ~ a_0.")
print(f"    So the IC mode does NOT land in g03v/g03w's pincer -- it escapes the PPN arm outright and the tachyon arm is not")
print(f"    even defined for it -- but it lands in a THIRD gate the same class already carries, and that one it does not survive.")
check("K9 [VERDICT] the lead's IC-series scalar is viable as the programme's allowed clock mode, as published",
      cher_ok and solar_ok and nonempty,
      f"NOT viable as published: subluminal c_s^2 = sigma = 1/3 violates gravitational Cherenkov by {(1-math.sqrt(cs2_L4))/CHER:.1e}x and the "
      f"construction's own exp wall cannot suppress the coupling where the bound is set.  The failure is ONE DESIGN PARAMETER "
      f"deep -- sigma, already free in IC-4 over (0, 1] -- and the target is sigma >= 1 rather than 1/3.  The PPN arm genuinely "
      f"passes; the tachyon arm is undetermined.  Nothing here contradicts a claim the lead has made: IC-4 states sigma is a "
      f"construction choice, and no IC file claims a Cherenkov, PPN or causality pass")

print(f"\n  Caveats, stated in the direction they cut:")
print(f"  * The khronometric dictionary (B.1) is exact only for an action whose scalar sector is the clock's; the IC action has a")
print(f"    second constrained field u, so 'c_2^eff = c_14^eff c_s^2' in B.6 is an EFFECTIVE identification through the observable")
print(f"    mode speed, not a term-by-term match.  It is used only to convert c_s^2 into a PPN requirement, and the Cherenkov")
print(f"    verdict (E) does not use it at all -- that one needs only the measured c_s^2 and the mode's gravitational coupling.")
print(f"  * c_s^2 = 1/3 is L4's value AT THE EXPANDING WITNESS.  If the IC scalar's speed runs to >= 1 in the Galactic MOND regime")
print(f"    the Cherenkov verdict is void; nothing in the published files says it does, and sigma is a constant of the action.")
print(f"    Establishing c_s^2(|a|/a_0) along a Galactic path is the single calculation that would overturn E.")
print(f"  * The Cherenkov bound assumes the mode couples to the matter stress tensor with gravitational strength.  A cancellation")
print(f"    in the mode's overlap with h_mu_nu would evade it; the required size of that cancellation is priced in E as s <= {s_need:.0e}.")
print(f"  * c_s^2 = sigma is INFERRED from IC-4's own naming plus L4's measured 1/3; it is not derived here.  If it is false, the")
print(f"    sigma = 1 repair is void but the Cherenkov failure at c_s^2 = 1/3 stands.")
print(f"  * The alpha_2 bound 4e-7 and alpha_1 bound 1e-4 are the repository's standing values (g03v, THE_ACTION section 2).")
print(f"  total {time.time()-T0:.0f}s")

print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(2 if FAILS else 0)
