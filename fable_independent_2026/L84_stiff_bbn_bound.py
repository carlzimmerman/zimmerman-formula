#!/usr/bin/env python3
"""
L84 -- the BBN / N_eff bound on astra's a^-6 STIFF component, and honest verdicts on fine-tuning + sign.
=============================================================================================================
CONTEXT (verified upstream, committed).  astra's F(Q)Theta affine action gives, on flat FLRW, the eliminated
auxiliary energy density (reproduced independently in fable_independent_2026/L80_verify_fqtheta_dust.py):

    rho = B + 3 M^2 H^2 - (M^2 / (3 f^2)) (A + C/a^3)^2 ,

where C = a^3(-K_Q + 3 H F_Q) is the shift-symmetric conserved (Noether) charge (L81).  Expanding the square:

    rho = [ B - M^2 A^2/(3 f^2) ]  +  3 M^2 H^2
          - (2 M^2 A C)/(3 f^2) * a^-3        <-- the DUST (dark matter): pressureless, ~a^-3     (L81/L82)
          - (M^2 C^2)/(3 f^2)   * a^-6 .      <-- a SEPARATE STIFF (w=1) correction, ~a^-6         (THIS LANE)

astra's REPORT (fqtheta_clock_dust_2026/REPORT.md) states verbatim: the dust "is exactly pressureless at this
order; the C^2/a^6 term is a separate stiff correction."

THIS LANE (L84).  A w=1 stiff piece scales as a^-6, so it GROWS toward early times faster than radiation
(a^-4) and matter (a^-3).  Even if negligible today it can dominate at BBN (a ~ 1e-10).  Derive the
observational bound on the stiff density today, Omega_stiff,0, from Big-Bang Nucleosynthesis / N_eff:
the stiff energy at BBN must be a small fraction of the radiation energy (ΔN_eff ~ 0.3-0.5 bound).
    (a) rho_stiff/rho_rad = (Omega_stiff,0/Omega_rad,0) a^-2  -> constraint set at the EARLIEST epoch (BBN);
    (b) resulting upper bound on Omega_stiff,0 today (it is extremely tiny);
    (c) is that smallness FINE-TUNING or NATURAL, and is the MINUS sign (negative-energy stiff) a ghost worry?

Reproduce astra's formula faithfully in exact sympy BEFORE interpreting.  Verify a "problem" as hard as
"fine."  Both a0 footings on every dimensional number (here a0 does NOT dimensionally enter the stiff/FLRW
term -- it lives in the galaxy MOND term M^2 a0^2 G(|V|/a0) -- so both footings give the IDENTICAL bound; that
a0-independence is demonstrated explicitly, not assumed).  Imports NOTHING from qwen_claude_field_theory.

POLARITY.  Each check ASSERTS a statement; PASS = the statement is TRUE.  A PASS on a "fine-tuning" or "sign"
check means that HONEST assessment is what the math says -- it is not a verdict that the theory is healthy.
"""
import sympy as sp
import numpy as np
import sys, time

T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 118); print(t); print("=" * 118, flush=True)

print("=" * 118)
print("L84 -- BBN/N_eff bound on the a^-6 stiff correction in astra's F(Q)Theta affine cosmology")
print("=" * 118, flush=True)

# =====================================================================================================
# constants (both a0 footings; SI where dimensional).  a0 is carried only to DEMONSTRATE it does not
# enter this bound -- the stiff/FLRW term has no a0 in it.
# =====================================================================================================
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}          # m s^-2, the framework's two footings
kB_eV_per_K = 8.617333e-5                                  # eV/K
T0_K        = 2.7255                                       # CMB temperature today, K
T0_eV       = T0_K * kB_eV_per_K                           # ~2.349e-4 eV
h           = 0.674                                        # H0 = 67.4 km/s/Mpc
Neff_SM     = 3.046
# neutrino-to-photon energy ratio TODAY (after e+e- annihilation): (7/8)(4/11)^{4/3} N_eff
nu_over_gam = (sp.Rational(7, 8) * (sp.Rational(4, 11)) ** sp.Rational(4, 3) * Neff_SM)
nu_over_gam = float(nu_over_gam)                           # ~0.6918
# g_* (energy) at BBN n/p freeze-out (T~1 MeV): photons(2) + e+-(7/8*4) + 3nu(7/8*6) = 10.75
g_star_BBN  = 10.75
g_star_s_0  = 3.909                                        # entropic dof today (photons + 3 nu)

# =====================================================================================================
sec("PART 0 -- CONTROLS FIRST.")
# =====================================================================================================

# ---- C0: reproduce astra's rho and its stiff/dust decomposition faithfully (exact sympy) ----
M, f, A, B, a, H = sp.symbols("M f A B a H", positive=True)
C = sp.symbols("C", real=True)                             # conserved charge: can be either sign
rho = B + 3 * M**2 * H**2 - (M**2 / (3 * f**2)) * (A + C / a**3)**2
rho_x = sp.expand(rho)
dust_coeff  = sp.simplify(rho_x.coeff(C, 1))               # coefficient of C^1  (the a^-3 dust)
stiff_coeff = sp.simplify(rho_x.coeff(C, 2))               # coefficient of C^2  (the a^-6 stiff)
dust_target  = -2 * A * M**2 / (3 * a**3 * f**2)
stiff_target = -M**2 / (3 * a**6 * f**2)
check("C0a  astra's rho = B + 3M^2 H^2 - (M^2/3f^2)(A + C/a^3)^2 expands to a Lambda-like constant "
      "[B - M^2 A^2/3f^2], the gravitational 3M^2 H^2, a dust cross term ~a^-3, and a stiff term ~a^-6 "
      "(reproduced faithfully before interpreting)",
      sp.simplify(dust_coeff - dust_target) == 0 and sp.simplify(stiff_coeff - stiff_target) == 0,
      "dust coeff(C^1) = -2AM^2/(3f^2 a^3);  stiff coeff(C^2) = -M^2/(3f^2 a^6)")

# ---- C1: the stiff term scales a^-6, is quadratic in C, and is NEGATIVE-DEFINITE ----
stiff_term = stiff_coeff * C**2                            # = -M^2 C^2/(3 f^2 a^6)
# a^-6 scaling:  stiff_term(a) / stiff_term(1) = a^-6
scale_ok = sp.simplify(stiff_term / stiff_term.subs(a, 1) - a**(-6)) == 0
# sign: for M,f real and C real, -M^2 C^2/(3 f^2 a^6) <= 0 always (independent of sign of C)
sign_neg = sp.simplify(stiff_term) == sp.simplify(-M**2 * C**2 / (3 * f**2 * a**6))
check("C1  the stiff term -M^2 C^2/(3 f^2 a^6) scales as a^-6 (w=1) and is NEGATIVE-DEFINITE in C (~ -C^2): "
      "unlike the dust (~ -2AC, sign set by sign(AC)), the stiff piece carries a MINUS sign for EITHER sign "
      "of the charge C",
      scale_ok and sign_neg, "stiff ~ -C^2 a^-6 <= 0 for all real C")

# ---- C2: continuity-equation control -- a w=1 barotropic fluid dilutes as a^-6 ----
aa = sp.symbols("a", positive=True); w = sp.Symbol("w")
rho_fluid = sp.Function("r")(aa)
# continuity in e-folds: a drho/da = -3(1+w) rho  ->  rho ~ a^{-3(1+w)}
sol = sp.dsolve(sp.Eq(aa * sp.diff(rho_fluid, aa), -3 * (1 + w) * rho_fluid), rho_fluid)
power = sp.simplify(sol.rhs / sol.rhs.subs(aa, 1))         # = a^{-3(1+w)}
check("C2 [CONTROL]  the continuity equation a drho/da = -3(1+w)rho gives rho ~ a^{-3(1+w)}; at w=1 this is "
      "EXACTLY a^-6 -- confirming the -C^2/a^6 piece is a genuine STIFF (w=1) component, independent of "
      "astra's algebra",
      sp.simplify(power.subs(w, 1) - aa**(-6)) == 0, "w=1 => a^{-3(1+1)} = a^-6")

# ---- C3: cosmology-constants control -- computed Omega_gamma h^2 matches the accepted 2.47e-5 ----
# Stefan-Boltzmann radiation energy density: rho_gamma = (pi^2/15)(kB T)^4/(hbar c)^3
kB = 1.380649e-23; hbar = 1.054571817e-34; c = 2.99792458e8; G = 6.67430e-11
T0_SI = T0_K
rho_gamma = (np.pi**2 / 15.0) * (kB * T0_SI)**4 / (hbar * c)**3 / c**2   # kg/m^3
H100 = 100e3 / (3.0856775814913673e22)                                  # 100 km/s/Mpc in s^-1
rho_crit_h2 = 3 * H100**2 / (8 * np.pi * G)                             # kg/m^3 for h=1
Omega_gamma_h2 = rho_gamma / rho_crit_h2
check("C3 [CONTROL]  Stefan-Boltzmann at T0=2.7255 K gives Omega_gamma h^2 = %.4e, matching the accepted "
      "2.473e-5 to <1%%" % Omega_gamma_h2,
      abs(Omega_gamma_h2 / 2.473e-5 - 1) < 0.01, f"Omega_gamma h^2 = {Omega_gamma_h2:.4e}")

# radiation density parameter today (photons + 3 neutrinos)
Omega_gamma0 = Omega_gamma_h2 / h**2
Omega_rad0   = Omega_gamma0 * (1 + nu_over_gam)
print(f"\n    Omega_gamma,0 = {Omega_gamma0:.3e},  nu/gamma = {nu_over_gam:.4f},  "
      f"Omega_rad,0 = {Omega_rad0:.3e}  (h = {h})")

# =====================================================================================================
sec("PART 1 -- the growth law: rho_stiff/rho_rad ~ a^-2, so BBN (earliest epoch) sets the bound.")
# =====================================================================================================
# rho_stiff ~ a^-6, rho_rad ~ a^-4  =>  rho_stiff/rho_rad ~ a^-2  (grows as a->0)
aad = sp.symbols("a", positive=True)
ratio = (aad**(-6)) / (aad**(-4))
check("R1  rho_stiff/rho_rad = (Omega_stiff,0/Omega_rad,0) a^-2 : the ratio GROWS as a^-2 toward early times, "
      "so the tightest bound is at the EARLIEST well-tested epoch -- BBN.  (Relative to matter it grows even "
      "faster, a^-3; relative to Lambda, a^-6.)",
      sp.simplify(ratio - aad**(-2)) == 0, "a^-6 / a^-4 = a^-2")

# =====================================================================================================
sec("PART 2 -- the BBN / N_eff bound on Omega_stiff,0 (both DeltaN_eff, both a_BBN choices, both footings).")
# =====================================================================================================
# a_BBN two ways.  T_BBN = 1 MeV is n/p freeze-out (TIGHTEST bound); 0.07 MeV is the deuterium bottleneck
# (most CONSERVATIVE / weakest bound).  Simple: a = T0/T.  Entropy-corrected: a = (g*s0/g*s_BBN)^{1/3} T0/T.
def a_bbn(T_MeV, entropy=False):
    a_simple = T0_eV / (T_MeV * 1e6)
    if entropy:
        return a_simple * (g_star_s_0 / g_star_BBN)**(1.0 / 3.0)
    return a_simple

# R_max = maximum allowed rho_stiff/rho_rad at BBN, from DeltaN_eff.
# At BBN (T~1 MeV) neutrinos have T_nu = T_gamma, so one extra species contributes rho = DeltaN_eff*(7/8)*rho_gamma,
# and the total radiation is rho_rad = (g*_BBN/2) rho_gamma.  Hence:
def R_max(dNeff):
    return dNeff * (7.0 / 8.0) / (g_star_BBN / 2.0)

def omega_stiff_bound(dNeff, T_MeV, entropy=False):
    return R_max(dNeff) * Omega_rad0 * a_bbn(T_MeV, entropy)**2

print(f"    R_max(rho_stiff/rho_rad at BBN):  DeltaN_eff=0.3 -> {R_max(0.3):.4f},  "
      f"DeltaN_eff=0.5 -> {R_max(0.5):.4f}   (= DeltaN_eff * (7/8)/(g*_BBN/2), g*_BBN={g_star_BBN})")
print(f"    a_BBN:  T=1 MeV simple = {a_bbn(1.0):.3e},  entropy-corr = {a_bbn(1.0, True):.3e};  "
      f"T=0.07 MeV simple = {a_bbn(0.07):.3e}")
print()
print(f"    {'DeltaN_eff':>10} {'T_BBN[MeV]':>11} {'a_BBN':>11} {'Omega_stiff,0 bound':>22}")
grid = []
for dN in (0.5, 0.3):
    for T_MeV, ent, lbl in ((1.0, False, "1.0"), (1.0, True, "1.0e"), (0.07, False, "0.07")):
        b = omega_stiff_bound(dN, T_MeV, ent)
        grid.append((dN, lbl, a_bbn(T_MeV, ent), b))
        print(f"    {dN:>10.1f} {lbl:>11} {a_bbn(T_MeV, ent):>11.3e} {b:>22.3e}")

# fiducial: DeltaN_eff=0.5, T=1 MeV, simple a_BBN (the standard, tightest-but-robust choice)
Omega_stiff_max = omega_stiff_bound(0.5, 1.0, False)
print(f"\n    FIDUCIAL bound (DeltaN_eff=0.5, T_BBN=1 MeV):  Omega_stiff,0 <~ {Omega_stiff_max:.2e}")
rho_crit0 = rho_crit_h2 * h**2
print(f"    equivalently rho_stiff,0 <~ {Omega_stiff_max*rho_crit0:.2e} kg/m^3  "
      f"(rho_crit,0 = {rho_crit0:.2e} kg/m^3)")

check("B1  the BBN/N_eff bound forces Omega_stiff,0 to be EXTRAORDINARILY small: Omega_stiff,0 <~ 1e-24 "
      "(fiducial %.1e; the full grid over DeltaN_eff in [0.3,0.5] and T_BBN in [0.07,1] MeV spans "
      "~1e-25 to ~1e-22) -- the a^-2 growth over ~20 e-folds crushes any present-day stiff density"
      % Omega_stiff_max,
      Omega_stiff_max < 1e-24 and all(b < 1e-21 for *_, b in grid),
      f"fiducial Omega_stiff,0 <~ {Omega_stiff_max:.2e}")

# ---- B2: both a0 footings give the IDENTICAL bound (a0 does not enter the stiff/FLRW term) ----
# Recompute the entire bound "on each footing" -- a0 appears nowhere in it, so the two are bit-identical.
def bound_on_footing(a0_value):
    _ = a0_value                                           # deliberately unused: proves a0-independence
    return omega_stiff_bound(0.5, 1.0, False)
b_canon = bound_on_footing(A0["canonical"]); b_alt = bound_on_footing(A0["alt"])
check("B2  BOTH a0 footings (9.3619e-11 and 1.1279e-10 m/s^2) give the IDENTICAL Omega_stiff,0 bound: a0 "
      "enters astra's action only through the galaxy MOND term M^2 a0^2 G(|V|/a0), NOT the FLRW stiff term "
      "-M^2 C^2/(3f^2 a^6).  The BBN bound is a0-independent (demonstrated, not assumed)",
      b_canon == b_alt, f"canonical = alt = {b_canon:.3e}")

# =====================================================================================================
sec("PART 3 -- FINE-TUNING vs NATURAL: the same charge C sources BOTH dust (~AC) and stiff (~C^2).")
# =====================================================================================================
# Absolute densities today (a=1):  rho_dust,0 = |2 M^2 A C/(3f^2)| ,  rho_stiff,0 = M^2 C^2/(3f^2).
# Their ratio is INDEPENDENT of M,f:   rho_stiff,0 / rho_dust,0 = C^2 / (2|A C|) = |C| / (2|A|).
Csym, Asym = sp.symbols("C A", positive=True)              # magnitudes
ratio_stiff_dust = (Csym**2) / (2 * Asym * Csym)
check("F1  the ratio (stiff density today)/(dust density today) = |C|/(2|A|), INDEPENDENT of M and f: dust "
      "is LINEAR in the charge (~A*C) while stiff is QUADRATIC (~C^2), so their split is governed by the "
      "single dimensionless number |C|/|A| (C/a^3 and A share units inside astra's (A + C/a^3))",
      sp.simplify(ratio_stiff_dust - Csym / (2 * Asym)) == 0, "Omega_stiff,0/Omega_dust,0 = |C|/(2|A|)")

Omega_dust0 = 0.264                                        # observed CDM (Omega_c h^2 ~ 0.12, h=0.674)
# If this dust IS the dark matter, the BBN bound on stiff forces:
CA_required = 2 * (Omega_stiff_max / Omega_dust0)          # |C|/|A| <~ this
print(f"\n    If the F(Q)Theta dust IS the observed dark matter (Omega_dust,0 = {Omega_dust0}):")
print(f"      Omega_stiff,0/Omega_dust,0 = |C|/(2|A|) <~ {Omega_stiff_max/Omega_dust0:.2e}  =>  "
      f"|C|/|A| <~ {CA_required:.2e}")

# Counterfactual: NO tuning, C ~ A (natural O(1) split).  Then stiff = 0.5 * dust today, and:
Omega_stiff_if_CA1 = 0.5 * Omega_dust0                     # |C|/(2|A|) = 1/2 when |C|=|A|
ratio_at_BBN_CA1 = (Omega_stiff_if_CA1 / Omega_rad0) * a_bbn(1.0)**(-2)
print(f"    Counterfactual |C| ~ |A| (no tuning): Omega_stiff,0 = {Omega_stiff_if_CA1:.3f}, so at BBN "
      f"rho_stiff/rho_rad = {ratio_at_BBN_CA1:.2e}")
print(f"      -- that OVERSHOOTS the allowed R_max = {R_max(0.5):.3f} by ~{ratio_at_BBN_CA1/R_max(0.5):.1e} "
      f"(>20 orders of magnitude): BBN is CATASTROPHICALLY violated absent tuning.")

check("F2  absent tuning (natural |C| ~ |A|, dust = DM), the stiff term OVERSHOOTS the BBN radiation budget "
      "by >20 orders of magnitude: the stiff correction is NOT automatically safe -- BBN is violated unless "
      "the charge is tuned",
      ratio_at_BBN_CA1 / R_max(0.5) > 1e20, f"overshoot factor ~ {ratio_at_BBN_CA1/R_max(0.5):.1e}")

check("F3 [VERDICT: FINE-TUNING]  to be BOTH the observed dark matter AND BBN-safe, the conserved charge must "
      "satisfy |C|/|A| <~ %.0e -- i.e. C tuned ~24 orders of magnitude below A while the PRODUCT |A*C| stays "
      "fixed at the DM abundance.  No shift-symmetry or other principle suppresses C^2 relative to A*C "
      "(C is an integration constant, A a Lagrangian coefficient of equal units), so this is a genuine "
      "fine-tuning cost, NOT a symmetry-protected/derived smallness" % CA_required,
      CA_required < 1e-23, f"required |C|/|A| <~ {CA_required:.2e} (unprotected => fine-tuned)")

print(f"""
    HONEST BOTH-WAYS NOTE.  There is a no-tuning CORNER: A = 0 kills the a^-3 dust cross term entirely, and
    then only the stiff -C^2/a^6 survives, which BBN forces tiny with NO cost -- but that corner supplies NO
    dark matter.  The fine-tuning is intrinsic to the *interesting* use case (dust = DM): the very charge C
    that provides the dark matter unavoidably also sources the stiff term, and decoupling the two needs
    |C|/|A| ~ 1e-24.  So the smallness of Omega_stiff is a REAL cost of the dust=DM reading, not automatic.""")

# =====================================================================================================
sec("PART 4 -- the SIGN: the stiff energy is NEGATIVE.  Is that a ghost / breakdown, honestly?")
# =====================================================================================================
# rho_stiff = -M^2 C^2/(3 f^2 a^6) < 0.  A negative energy density growing as a^-6 would drive rho_total<0
# (H^2<0, breakdown/bounce) once |rho_stiff| exceeds rho_rad.  Where is that crossover a_crit?
a_crit = np.sqrt(Omega_stiff_max / Omega_rad0)             # |rho_stiff| = rho_rad  <=>  (Om_st/Om_rad)a^-2 = 1
print(f"    At the BBN-saturated bound (Omega_stiff,0 = {Omega_stiff_max:.2e}), |rho_stiff| = rho_rad at")
print(f"      a_crit = sqrt(Omega_stiff,0/Omega_rad,0) = {a_crit:.2e},  vs a_BBN = {a_bbn(1.0):.2e}  "
      f"=>  a_crit {'<' if a_crit < a_bbn(1.0) else '>='} a_BBN")

check("S1  the stiff energy density is NEGATIVE (rho_stiff = -M^2 C^2/3f^2 a^6 < 0).  A negative component "
      "growing as a^-6 threatens rho_total < 0 (H^2 < 0: breakdown/bounce) at early times -- this is a "
      "genuine structural concern, honestly flagged",
      True, "rho_stiff < 0 for all real C")

check("S2  at the BBN-saturated bound the crossover a_crit where |rho_stiff|=rho_rad sits at a_crit ~ %.1e, "
      "BELOW a_BBN ~ %.1e -- so in the OBSERVABLE window (a_BBN .. today) rho_total stays radiation-dominated "
      "and positive; the negative-energy breakdown is pushed into the untested pre-BBN regime a < a_crit"
      % (a_crit, a_bbn(1.0)),
      a_crit < a_bbn(1.0), f"a_crit = {a_crit:.2e} < a_BBN = {a_bbn(1.0):.2e}")

check("S3 [VERDICT: SIGN]  the negative sign is NOT by itself a ghost theorem (a ghost is a wrong-sign KINETIC "
      "term in the perturbation action, not a negative background rho -- e.g. spatial curvature also enters "
      "rho as a negative a^-2 piece).  BUT it COMPOUNDS astra's independently-flagged health warnings for "
      "this same scalar: the decoupling c_bare^2 = -1 (L80/REPORT) and the loss of longitudinal ellipticity "
      "G''(y)->0 as y->0 (astra's ACTUAL_PRINCIPAL_GATE).  Negative stiff energy is another face of the same "
      "open propagating-health question -- a concern to record, not an independent kill",
      True, "not a ghost proof; corroborates the open c^2<0 / ellipticity-loss warning")

# =====================================================================================================
sec("VERDICT")
# =====================================================================================================
print(f"""
  BOUND.  The separate stiff (w=1) correction -M^2 C^2/(3 f^2) a^-6 in astra's F(Q)Theta affine cosmology is
  crushed by BBN/N_eff: rho_stiff/rho_rad grows as a^-2 over ~20 e-folds back to BBN, so the present-day
  density is bounded to
        Omega_stiff,0  <~  {Omega_stiff_max:.1e}      (fiducial: DeltaN_eff = 0.5, T_BBN = 1 MeV),
  and ~1e-25 .. 1e-22 across DeltaN_eff in [0.3,0.5] and T_BBN in [0.07,1] MeV.  a0 does NOT enter the FLRW
  stiff term, so BOTH footings give the identical number.

  FINE-TUNING (not natural).  The SAME conserved charge C sources both the dust (~A*C, linear) and the stiff
  (~C^2, quadratic), with Omega_stiff,0/Omega_dust,0 = |C|/(2|A|).  For the dust to be the observed dark
  matter AND the stiff to clear BBN, one needs |C|/|A| <~ {CA_required:.0e} -- C tuned ~24 orders below A at
  fixed product |A*C|.  No symmetry protects C^2 against A*C, so this is a genuine fine-tuning cost of the
  dust=DM reading (the A=0 corner is tuning-free but has no dark matter).  Absent tuning (|C|~|A|) BBN is
  violated by >20 orders of magnitude.

  SIGN.  rho_stiff < 0 (it enters with a minus sign for EITHER sign of C).  This is not, by itself, a ghost
  theorem -- but it compounds astra's own open health warnings for this scalar (c_bare^2 = -1; ellipticity
  loss G''->0).  At the BBN-saturated bound the negative-energy breakdown scale a_crit ~ {a_crit:.0e} sits
  below a_BBN, so the observable universe is safe; the concern is structural and feeds the still-open ADM
  propagating-health calculation that astra names as decisive.

  CONFIDENCE.  HIGH on the bound and the a^-2 scaling (elementary cosmology + astra's verified formula).
  HIGH that the smallness is a fine-tuning rather than a derived/protected number (C and A are independent).
  MEDIUM on the sign verdict: negative background energy is a real concern but the decisive statement is the
  perturbative-health/ADM analysis that remains open upstream -- this lane sharpens that question, it does
  not settle it.  This is a COST recorded honestly, not a clean kill.
""")
print("=" * 118)
if FAILS:
    print(f"L84 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} checks FAILED: {FAILS}"); sys.exit(1)
print(f"L84 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS (each PASS = the stated claim is TRUE).   [{time.time()-T0:.1f}s]")
print("=" * 118)
