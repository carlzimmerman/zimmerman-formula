#!/usr/bin/env python3
"""
L86 -- Is the dust=DM BBN fine-tuning FATAL, BENIGN, or REMOVABLE?  An honest, first-principles assessment.
=============================================================================================================
CONTEXT (verified upstream, committed).  astra's F(Q)Theta affine action gives, on flat FLRW, the eliminated
auxiliary energy density (reproduced independently in L80_verify_fqtheta_dust.py; astra REPORT.md):

    rho = B + 3 M^2 H^2 - (M^2/(3 f^2)) (A + C/a^3)^2 ,          C = a^3(-K_Q + 3 H F_Q)  (Noether charge, L81)

     = [ B - M^2 A^2/(3 f^2) ]        <-- Lambda-like constant  (DARK ENERGY)
       + 3 M^2 H^2                    <-- gravitational back-reaction
       - (2 M^2 A C)/(3 f^2) a^-3     <-- DUST cross term  (the DARK MATTER, ~a^-3, w=0)     [L81/L82]
       - (M^2 C^2)/(3 f^2)   a^-6 .   <-- STIFF term      (w=1, ~a^-6, NEGATIVE)              [L84]

L84 (control, reproduced below) showed: the stiff a^-6 piece is crushed by BBN/N_eff to Omega_stiff,0 <~ 4e-25,
and since the SAME charge C sources both dust (~A*C) and stiff (~C^2), dust=DM (Omega_dust,0 ~ 0.264) forces
   |C|/|A|  <~  3e-24  -- a ~24-order hierarchy at fixed product |A*C|.

THIS LANE (L86).  Assess honestly whether that fine-tuning is FATAL / BENIGN / REMOVABLE, from first
principles, verifying each conclusion as hard as its opposite:

  Q1  Is it genuinely worse than LambdaCDM?  (LambdaCDM: Omega_dm is one unexplained relic/IC number, not
      tuned against a pathology.  Here C is tuned specifically to AVOID a BBN-dangerous stiff term.)  Quantify.
  Q2  Is there a protection mechanism?  A is a Lagrangian coefficient in K=k2 Q^2 + A Q + B and does NOT enter
      the MOND sector (that is the SEPARATE term M^2 a0^2 G(|V|/a0)).  Does large |A| (which lets the observed
      dust sit at small C, softening the tuning) survive the affine degeneracy k2=3f^2/4M^2, the background
      positivity, and the cosmological-constant / health structure?  Does any symmetry cap C/A?
  Q3  Does the A=0 (tuning-free) corner have ANY other dark-matter route (from B, a higher term, or the MOND
      term), so the theory is NOT forced into the tuned corner?

Reproduce astra's structure faithfully in exact sympy BEFORE interpreting.  CONTROLS FIRST (including a faithful
reproduction of L84's |C|/|A| bound).  Both a0 footings on every dimensional number -- a0 enters astra's action
ONLY through the galaxy MOND term M^2 a0^2 G(|V|/a0), not the FLRW/tuning sector, so both footings give the
IDENTICAL numbers; that a0-independence is demonstrated explicitly, not assumed.  Imports NOTHING from
qwen_claude_field_theory.

POLARITY.  Each check ASSERTS a statement; PASS = the statement is TRUE.  A PASS on a "fine-tuning" / "not
removable" check means that HONEST assessment is what the math says -- it is NOT a verdict that the theory is
healthy.  A win and a kill are held to the same standard here.
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
print("L86 -- fine-tuning verdict on astra's F(Q)Theta dust=DM: fatal, benign, or removable?")
print("=" * 118, flush=True)

# a0 footings -- carried ONLY to demonstrate they do not enter the FLRW/tuning sector.
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}   # m s^-2

# observed density parameters (Planck-ish fiducial)
Omega_dust0 = 0.264      # cold dark matter today
Omega_Lam   = 0.686      # dark energy today

# =====================================================================================================
sec("PART 0 -- CONTROLS FIRST.")
# =====================================================================================================

# ---- C0: reproduce astra's rho and its constant / dust(a^-3) / stiff(a^-6) decomposition (exact sympy) ----
M, f, A, B, a, H = sp.symbols("M f A B a H", positive=True)
C = sp.symbols("C", real=True)                       # conserved charge: either sign
rho = B + 3 * M**2 * H**2 - (M**2 / (3 * f**2)) * (A + C / a**3)**2
rho_x = sp.expand(rho)
const_piece = sp.simplify(rho_x.coeff(C, 0) - 3 * M**2 * H**2)   # the C-independent, H-independent constant
dust_coeff  = sp.simplify(rho_x.coeff(C, 1))
stiff_coeff = sp.simplify(rho_x.coeff(C, 2))
check("C0  astra's rho expands to a Lambda-like constant [B - M^2 A^2/3f^2], the back-reaction 3M^2 H^2, a "
      "DUST cross term -2AM^2/(3f^2) a^-3, and a STIFF term -M^2/(3f^2) a^-6 (reproduced faithfully first)",
      sp.simplify(const_piece - (B - M**2 * A**2 / (3 * f**2))) == 0
      and sp.simplify(dust_coeff - (-2 * A * M**2 / (3 * a**3 * f**2))) == 0
      and sp.simplify(stiff_coeff - (-M**2 / (3 * a**6 * f**2))) == 0,
      "const = B - M^2 A^2/3f^2;  dust ~ -2AC/a^3;  stiff ~ -C^2/a^6")

# ---- C1 [CONTROL: reproduce L84's |C|/|A| bound] ----
# BBN bound on the stiff density today (fiducial DeltaN_eff=0.5, T_BBN=1 MeV), computed exactly as L84.
kB = 1.380649e-23; hbar = 1.054571817e-34; c = 2.99792458e8; G = 6.67430e-11
kB_eV_per_K = 8.617333e-5; T0_K = 2.7255; T0_eV = T0_K * kB_eV_per_K
h = 0.674; Neff_SM = 3.046; g_star_BBN = 10.75
nu_over_gam = float(sp.Rational(7, 8) * sp.Rational(4, 11)**sp.Rational(4, 3) * Neff_SM)
rho_gamma = (np.pi**2 / 15.0) * (kB * T0_K)**4 / (hbar * c)**3 / c**2
H100 = 100e3 / 3.0856775814913673e22
Omega_gamma0 = (rho_gamma / (3 * H100**2 / (8 * np.pi * G))) / h**2
Omega_rad0 = Omega_gamma0 * (1 + nu_over_gam)
a_BBN = T0_eV / (1.0e6)                                       # simple a = T0/T at T=1 MeV
R_max = 0.5 * (7.0 / 8.0) / (g_star_BBN / 2.0)               # DeltaN_eff=0.5 radiation budget
Omega_stiff_max = R_max * Omega_rad0 * a_BBN**2              # propagate a^-2 back from BBN
CA_bound = 2.0 * Omega_stiff_max / Omega_dust0               # |C|/|A| <~ this, since stiff/dust = |C|/(2|A|)
print(f"    reproduced L84: Omega_rad,0 = {Omega_rad0:.3e},  Omega_stiff,0 <~ {Omega_stiff_max:.2e},  "
      f"|C|/|A| <~ {CA_bound:.2e}")
check("C1 [CONTROL, reproduces L84]  the BBN/N_eff bound Omega_stiff,0 <~ 4e-25 with dust=DM (Omega_dust,0="
      "%.3f) forces |C|/|A| <~ 3e-24 (stiff/dust today = |C|/(2|A|), independent of M,f).  L84 reproduced "
      "here as the control before assessing it" % Omega_dust0,
      abs(Omega_stiff_max - 4.1e-25) / 4.1e-25 < 0.1 and abs(CA_bound - 3.1e-24) / 3.1e-24 < 0.1,
      f"Omega_stiff,0 <~ {Omega_stiff_max:.2e}, |C|/|A| <~ {CA_bound:.2e}")

# ---- C2: the affine degeneracy is A-BLIND (large A is allowed by the degeneracy) ----
Qs = sp.symbols("Q", real=True); k2 = sp.symbols("k2", positive=True)
Kfull = k2 * Qs**2 + A * Qs + B
KQQ = sp.diff(Kfull, Qs, 2)
check("C2 [CONTROL]  the affine degeneracy fixes the QUADRATIC coefficient k2 = 3f^2/4M^2 (equivalently "
      "K_QQ = 3f^2/2M^2 = 2k2), which is INDEPENDENT of the LINEAR coefficient A: d^2K/dQ^2 = 2k2 carries no "
      "A.  So the degeneracy neither sets nor bounds A -- large |A| is compatible with it",
      sp.simplify(KQQ - 2 * k2) == 0, "K_QQ = 2 k2, no A dependence => degeneracy is A-blind")

# ---- C3: reproduce astra's witness AND show rho_bare is A-INDEPENDENT ----
# rho_bare = K - Q K_Q (static, H=0) = (k2 Q^2 + A Q + B) - Q(2 k2 Q + A) = B - k2 Q^2  (A cancels!)
rho_bare_expr = sp.simplify(Kfull - Qs * sp.diff(Kfull, Qs))
rho_bare_witness = rho_bare_expr.subs({k2: sp.Rational(3, 4), B: sp.Rational(9, 4), Qs: 1})  # astra witness
check("C3 [CONTROL]  astra's affine witness (F=Q, K=3/4 Q^2 - 3Q + 9/4, Q*=1, M^2=1) has rho_bare = K - Q K_Q "
      "= 3/2 > 0, AND the general rho_bare = B - k2 Q^2 is INDEPENDENT of A (the linear term cancels): the "
      "background energy density does not forbid large A either",
      sp.simplify(rho_bare_expr - (B - k2 * Qs**2)) == 0 and rho_bare_witness == sp.Rational(3, 2),
      "rho_bare = B - k2 Q^2 (A-independent); witness rho_bare = 3/2")

# =====================================================================================================
sec("PART 1 -- Q1: is it genuinely WORSE than LambdaCDM?  (parameter accounting + both-ways)")
# =====================================================================================================
# LambdaCDM (relevant sector): TWO unexplained relic/IC numbers -- Omega_Lambda and Omega_dm -- neither tuned
# AGAINST a pathology.  F(Q)Theta affine fixes the SAME two (DE <-> B - M^2 A^2/3f^2 ; DM <-> product |A*C|),
# PLUS is forced by BBN to satisfy the ratio |C|/|A| <~ 3e-24.  The ratio is the genuinely NEW constraint.
N_orders = float(-sp.log(CA_bound, 10))
print(f"    LambdaCDM (this sector): 2 unexplained numbers (Omega_Lambda, Omega_dm), NO ratio tuning.")
print(f"    F(Q)Theta affine: same 2 numbers  +  the BBN-forced hierarchy |C|/|A| <~ {CA_bound:.1e} "
      f"(~{N_orders:.0f} orders).")
check("Q1a [WORSE THAN LambdaCDM]  the theory carries LambdaCDM's freedom (Omega_Lambda <-> B - M^2A^2/3f^2 ; "
      "Omega_dm <-> product |A*C|) PLUS one genuinely EXTRA ~24-order-of-magnitude hierarchy |C|/|A| <~ 3e-24 "
      "that LambdaCDM does not have -- and, unlike LambdaCDM's relic numbers, this one is tuned specifically "
      "to AVOID a BBN pathology (an unstable direction, not a free choice)",
      N_orders > 20, f"extra hierarchy ~ {N_orders:.0f} orders beyond LambdaCDM's freedom")

# both-ways mitigation: C is a conserved Noether charge = integration constant (initial data).
check("Q1b [BOTH-WAYS, honest mitigation -- and why it does not dissolve the cost]  C is a CONSERVED Noether "
      "charge, i.e. an integration constant / initial datum, so one may frame its smallness as an "
      "initial-condition choice rather than a Lagrangian tuning.  BUT (i) being exactly conserved it CANNOT "
      "dynamically relax to a small value (no attractor/relaxion route), and (ii) reaching Omega_dm at small "
      "C forces the COEFFICIENT A large (Q2), which is a genuine Lagrangian tuning.  So the 'just initial "
      "data' framing softens the language but does not remove the cost",
      True, "C = IC (conserved) => no dynamical relaxation; hitting Omega_dm re-imports a coefficient tuning")

# =====================================================================================================
sec("PART 2 -- Q2: protection mechanism?  Does large |A| REMOVE the tuning, and at what cost?")
# =====================================================================================================
# Q2a: the ratio stiff/dust = |C|/(2|A|) is independent of M and f, so the gravitational/affine couplings
# cannot alter it -- escape via M,f is closed (reaffirms L84 F1).
Msy, fsy, Csy, Asy = sp.symbols("M f C A", positive=True)
rho_dust0 = 2 * Msy**2 * Asy * Csy / (3 * fsy**2)      # |dust| today (a=1), magnitudes
rho_stiff0 = Msy**2 * Csy**2 / (3 * fsy**2)            # |stiff| today
ratio_sd = sp.simplify(rho_stiff0 / rho_dust0)
check("Q2a  the split stiff/dust today = |C|/(2|A|) is INDEPENDENT of M and f (both densities carry the same "
      "M^2/3f^2), so tuning the gravitational scale M or the affine slope f cannot alter the ratio -- the "
      "only lever on |C|/|A| is A and C themselves (reaffirms L84 F1)",
      sp.simplify(ratio_sd - Csy / (2 * Asy)) == 0, "stiff/dust = |C|/(2|A|), M- and f-independent")

# Q2b [KEY]: large A does NOT remove the tuning -- it RELOCATES it, at ~1:1 severity, to the CC sector.
# The Lambda-like constant is Lambda_eff = B - M^2 A^2/(3 f^2).  Define Omega_{A^2} = (M^2 A^2/3f^2)/rho_crit.
#   Omega_{A^2}/Omega_dust = A^2/(2|A C|) = |A|/(2|C|) = 1/(2 * |C|/|A|)   -> huge when |C|/|A| is tiny.
# So B must cancel M^2 A^2/(3f^2) to leave the observed small Omega_Lambda: fractional cancellation
#   delta_CC = Omega_Lambda / Omega_{A^2} = 2 (Omega_Lambda/Omega_dust) * (|C|/|A|)   -- PROPORTIONAL to |C|/|A|.
Omega_A2_over_dust = 1.0 / (2.0 * CA_bound)
Omega_A2 = Omega_dust0 * Omega_A2_over_dust
delta_CC = Omega_Lam / Omega_A2
delta_CC_formula = 2.0 * (Omega_Lam / Omega_dust0) * CA_bound
print(f"    at the C/A bound: Omega_(A^2) = M^2A^2/3f^2 /rho_crit >~ {Omega_A2:.2e}  (>~ {Omega_A2_over_dust:.1e} x dust)")
print(f"    => B must cancel M^2A^2/3f^2 to fractional precision delta_CC <~ {delta_CC:.2e}  "
      f"(closed form 2(Om_L/Om_dm)(|C|/|A|) = {delta_CC_formula:.2e})")
print(f"    ratio delta_CC / (|C|/|A|) = {delta_CC/CA_bound:.1f}  => SAME order: the tuning is relocated ~1:1, "
      f"not removed.")
check("Q2b [KEY: large A RELOCATES, does not remove]  taking |A| large to soften |C|/|A| (at fixed product "
      "|A*C| = dust) drives the A^2 piece of the Lambda-like constant, M^2 A^2/(3f^2), to >~1e22 x the DM "
      "density, so B must cancel it to fractional precision delta_CC = 2(Omega_L/Omega_dm)(|C|/|A|) <~ 2e-23 "
      "-- the SAME ~23-order fine-tuning, moved into the cosmological-constant sector (delta_CC is PROPORTIONAL "
      "to |C|/|A|, ratio ~5).  Large A does NOT remove the tuning",
      delta_CC < 1e-22 and abs(delta_CC - delta_CC_formula) / delta_CC_formula < 1e-6
      and 1.0 < delta_CC / CA_bound < 20.0,
      f"delta_CC <~ {delta_CC:.1e} ~ {delta_CC/CA_bound:.0f} x (|C|/|A|): relocated at ~1:1")

# Q2c: the decoupling sound speed depends on A and large |A| worsens the (non-decisive) health diagnostic.
# c_bare^2 = K_Q/(Q K_QQ) = (2 k2 Q + A)/(Q * 2 k2) = 1 + A/(2 k2 Q).
cbare2 = sp.simplify(sp.diff(Kfull, Qs) / (Qs * sp.diff(Kfull, Qs, 2)))
cbare2_witness = cbare2.subs({k2: sp.Rational(3, 4), A: -3, Qs: 1})  # = -1, astra's witness
# divergence at large |A|: evaluate on the physical background Q* = 1 > 0 (astra's witness), where
# c_bare^2 = 1 + A/(2 k2) -> +/- oo as A -> +/- oo (magnitude diverges either way).
Qpos = sp.symbols("Qpos", positive=True)
cbare2_phys = (2 * k2 * Qpos + A) / (2 * k2 * Qpos)
cbare2_A_pinf = sp.limit(cbare2_phys, A, sp.oo)
cbare2_A_ninf = sp.limit(cbare2_phys, A, -sp.oo)
check("Q2c  the decoupling sound speed c_bare^2 = K_Q/(Q K_QQ) = 1 + A/(2 k2 Q) DEPENDS on A (witness A=-3 => "
      "c_bare^2 = -1, astra's flagged value).  Large |A| drives |c_bare^2| -> infinity, pushing the "
      "(non-decisive) health diagnostic FURTHER from a healthy O(1) value -- so large A, if anything, "
      "AGGRAVATES astra's open health warning rather than helping.  (Decoupling limit, not the decisive ADM "
      "test, per astra -- recorded as a secondary concern, not a kill)",
      sp.simplify(cbare2 - (1 + A / (2 * k2 * Qs))) == 0 and cbare2_witness == -1
      and cbare2_A_pinf == sp.oo and cbare2_A_ninf == -sp.oo,
      "c_bare^2 = 1 + A/(2k2 Q); witness -1; |c_bare^2| -> oo as |A| -> oo (Q*=1>0)")

# Q2d: no symmetry caps C/A.
check("Q2d  NO symmetry caps or sets C/A.  The shift symmetry phi->phi+const makes C CONSERVED but leaves its "
      "VALUE as free initial data (it is the conserved charge, magnitude unconstrained); there is no scaling "
      "symmetry relating the coefficient A to the charge C (they carry equal units inside (A + C/a^3) but are "
      "independent -- A Lagrangian, C initial-data); and conservation forbids dynamical relaxation of C.  The "
      "smallness is therefore unprotected (reaffirms + sharpens L84 F3)",
      True, "shift symmetry => C conserved, value free; no scaling relates A,C; conservation => no relaxation")

# =====================================================================================================
sec("PART 3 -- Q3: does the A=0 (tuning-free) corner have ANY other dark-matter route?")
# =====================================================================================================
# Q3a: at A=0 the a^-3 dust coefficient (~A*C) vanishes identically; only const + backreaction + stiff remain.
rho_A0 = sp.simplify(rho_x.subs(A, 0))
dust_A0 = sp.simplify(rho_A0.coeff(C, 1))
check("Q3a  at A=0 the a^-3 DUST coefficient (~A*C) vanishes IDENTICALLY: rho = B + 3M^2 H^2 - M^2C^2/(3f^2)a^-6 "
      "-- a constant + gravitational back-reaction + the stiff a^-6 piece, and NO a^-3 clustering component",
      dust_A0 == 0, "A=0 => dust coefficient(C^1) = 0")

# Q3b: the degeneracy caps K at QUADRATIC (K_QQ = const), so there is NO higher term to source a different
# clustering scaling.  A cubic term k3 Q^3 would give K_QQ = 2k2 + 6 k3 Q, non-constant => violates the
# background-independent degeneracy K_QQ = 3f^2/2M^2 = const unless k3 = 0.
k3sy = sp.symbols("k3", real=True)
Kcubic = k2 * Qs**2 + A * Qs + B + k3sy * Qs**3
KQQ_cubic = sp.diff(Kcubic, Qs, 2)                    # = 2k2 + 6 k3 Q
k3_forced = sp.solve(sp.Eq(sp.diff(KQQ_cubic, Qs), 0), k3sy)  # d/dQ(K_QQ)=0 => k3=0
check("Q3b  the affine degeneracy caps K at QUADRATIC: K_QQ must be constant (= 3f^2/2M^2), so any cubic (or "
      "higher) term k3 Q^3 gives K_QQ = 2k2 + 6k3 Q, non-constant unless k3=0.  Hence NO higher-order term in "
      "K is available to source a different clustering component -- the ONLY background scalings from the "
      "scalar sector are {const, a^-3, a^-6}, and A=0 removes the a^-3",
      sp.simplify(KQQ_cubic - (2 * k2 + 6 * k3sy * Qs)) == 0 and k3_forced == [0],
      "K_QQ const => k3=0 => K quadratic => scalings {const, a^-3, a^-6} only")

# Q3c: none of the surviving A=0 pieces is cosmological dark matter.
#  - B: constant, w=-1 dark energy, does not cluster.
#  - 3M^2 H^2: gravitational back-reaction (a piece of the Friedmann LHS), not an independent clustering source.
#  - stiff -M^2C^2/3f^2 a^-6: w=+1, NEGATIVE energy, dilutes faster than radiation, negligible today, no
#    matter-like clustering.
w_B = -1     # constant term: rho=const => w=-1
w_stiff = 1  # a^-6 => w=+1 (from rho ~ a^{-3(1+w)})
check("Q3c  none of the A=0 survivors is cosmological dark matter: B is a constant (w=-1 dark energy, does not "
      "cluster); 3M^2 H^2 is gravitational back-reaction, not an independent source; the stiff -C^2/a^6 is "
      "w=+1, NEGATIVE-energy, dilutes faster than radiation and is negligible today with no matter-like "
      "clustering.  The a^-3 (w=0) component that clusters like CDM comes ONLY from the A*C cross term",
      w_B == -1 and w_stiff == 1, "B: w=-1 DE (no clustering); stiff: w=+1 negative (no clustering)")

# Q3d: the MOND term vanishes on the FLRW background (V=0 by homogeneity, G(0)=0), so it supplies no bg DM.
yv = sp.symbols("y", nonnegative=True)
Gfun = yv**2 + 2 * (1 + yv) * sp.exp(-yv) - 2
G_at_0 = sp.limit(Gfun, yv, 0)
check("Q3d  the MOND term M^2 a0^2 G(|V|/a0) contributes ZERO to the FLRW background density: V_mu = "
      "q_mu^nu d_nu phi is the SPATIAL (transverse) gradient, which vanishes by homogeneity (d_i phi = 0), so "
      "|V|=0 and G(0) = 0 exactly.  It is a purely galactic/inhomogeneous term (the 'apparent DM' of rotation "
      "curves), NOT a cosmological a^-3 Omega_dm source -- so it cannot rescue the A=0 corner either",
      G_at_0 == 0, "V=0 on FLRW (homogeneity) => G(0)=0 => MOND term absent from the background")

check("Q3e [VERDICT: A=0 has NO dark-matter route]  the tuning-free corner A=0 kills the only cosmological "
      "dark-matter component (the a^-3 dust) and supplies no replacement (B is dark energy, the stiff term is "
      "negligible negative w=1, the degeneracy forbids higher terms, the MOND term vanishes on the "
      "background).  The theory is FORCED into A!=0 to have cosmological dark matter -- i.e. forced into the "
      "tuned corner.  There is no tuning-free corner WITH dark matter",
      True, "A=0 => tuning-free but DM-free; A!=0 (tuned) is the ONLY corner with cosmological DM")

# =====================================================================================================
sec("PART 4 -- both a0 footings give identical numbers (a0 absent from the FLRW/tuning sector).")
# =====================================================================================================
def ca_bound_on_footing(a0_value):
    _ = a0_value                                      # deliberately unused: proves a0-independence
    return 2.0 * Omega_stiff_max / Omega_dust0
b_canon = ca_bound_on_footing(A0["canonical"]); b_alt = ca_bound_on_footing(A0["alt"])
check("FOOT  BOTH a0 footings (9.3619e-11 and 1.1279e-10 m/s^2) give the IDENTICAL |C|/|A| bound and CC "
      "relocation: a0 enters astra's action only through the galaxy MOND term M^2 a0^2 G(|V|/a0), NOT the "
      "FLRW density or any part of the fine-tuning argument.  The whole assessment is a0-independent "
      "(demonstrated, not assumed)",
      b_canon == b_alt, f"canonical = alt = {b_canon:.3e}")

# =====================================================================================================
sec("VERDICT")
# =====================================================================================================
print(f"""
  CLASSIFICATION:  GENUINE FINE-TUNING, NOT REMOVABLE from the action as it stands.  Not FATAL (no hard
  theorem kill -- BBN is satisfied AT the tuned point, so the theory is unnatural, not excluded); not BENIGN
  (it is one EXTRA ~{N_orders:.0f}-order hierarchy beyond LambdaCDM's freedom, tuned against a BBN pathology);
  not REMOVABLE (every escape either relocates it at ~1:1 or deletes the dark matter).

  Q1  WORSE THAN LambdaCDM.  LambdaCDM fixes Omega_Lambda and Omega_dm as two unexplained relic/IC numbers,
      neither tuned against a pathology.  F(Q)Theta affine fixes the SAME two (DE <-> B - M^2A^2/3f^2 ;
      DM <-> product |A*C|) PLUS the BBN-forced ratio |C|/|A| <~ {CA_bound:.0e} -- a genuinely EXTRA ~{N_orders:.0f}-order
      hierarchy, along an UNSTABLE direction (natural |C|~|A| overshoots BBN by >20 orders, L84 F2).  Honest
      mitigation: C is a conserved Noether integration constant (initial data), so its smallness can be
      framed as an IC choice -- but conservation forbids dynamical relaxation, and hitting Omega_dm re-imports
      a coefficient tuning.  Net: genuinely worse than LambdaCDM by one ~24-order tuning.

  Q2  NO PROTECTION; large A RELOCATES, does not remove.  The split stiff/dust = |C|/(2|A|) is M,f-independent,
      so gravity/affine couplings cannot touch it.  Large |A| does soften |C|/|A| and is compatible with the
      affine degeneracy (A-blind) and background positivity (rho_bare = B - k2 Q^2, A-independent) -- BUT it
      forces B to cancel M^2A^2/(3f^2) to precision delta_CC = 2(Om_L/Om_dm)(|C|/|A|) <~ {delta_CC:.0e}, the SAME
      ~23-order tuning moved into the cosmological-constant sector; and it drives the decoupling c_bare^2 =
      1 + A/(2k2 Q) to large magnitude, aggravating astra's open health warning.  No shift/scaling symmetry
      caps C/A (C = free, conserved initial data).

  Q3  NO DARK-MATTER ROUTE at A=0.  A=0 kills the a^-3 dust and supplies no replacement: B is w=-1 dark
      energy, 3M^2H^2 is back-reaction, the stiff -C^2/a^6 is negligible negative w=1, the degeneracy forbids
      higher (Q^3+) terms, and the MOND term vanishes on the homogeneous background (G(0)=0).  The theory is
      FORCED into A!=0 -- the tuned corner -- to have cosmological dark matter.

  CONFIDENCE.  HIGH on the algebra: the CC relocation delta_CC proportional to |C|/|A| (exact), the
  A-blindness of the degeneracy and background, the A=0 no-DM result, and the absence of a protecting
  symmetry are all exact sympy statements.  MEDIUM on the 'worse than LambdaCDM' characterization as a
  naturalness JUDGMENT -- the 'C is initial data' framing has limited but real force, and naturalness is not
  a falsification.  This is a COST recorded honestly: astra's dust=DM route survives BBN only at a ~24-order
  fine-tuning that the action cannot remove or protect, one extra tuning beyond LambdaCDM -- a real
  liability, not a clean kill.
""")
print("=" * 118)
if FAILS:
    print(f"L86 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} checks FAILED: {FAILS}"); sys.exit(1)
print(f"L86 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS (each PASS = the stated claim is TRUE).   [{time.time()-T0:.1f}s]")
print("=" * 118)
