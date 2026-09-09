#!/usr/bin/env python3
"""
L32 -- necessary conditions on ANY theory that produces a0 = kappa c sqrt(G rho_Lambda) with a FIXED coefficient
================================================================================================================
Everything the programme has established about kappa is about ONE action.  k01: in the candidate local aether-scalar
action the MOND primitive's additive constant is a zero mode of the static field equations and is exactly degenerate
with Lambda on the background, so no equation relates a0 to Lambda; the Lambda-free repair has the wrong sign and is
220x too small.  k02: a sequestering-type global average misses rho_Lambda by 1e5.  k04: promoting a0 to a conserved
four-form flux amplitude fixes the SIGN (Legendre energy eps = q P_q - P) and makes a0 ~ sqrt(G rho_Lambda)
STRUCTURAL, at the price of leaving kappa as the free coupling ratio Z/beta^2 = 7.96.  L3: flux quantisation cannot
fix that ratio -- every membrane- and geometry-sector quantity depends on (Z, beta) only through the SUM
Z~ = Z + 2 b beta^2, while kappa needs the SPLIT.

NOBODY HAS ASKED THE GENERAL QUESTION.  What must ANY theory satisfy -- from dimensional analysis, symmetry and the
structure of the field equations, not from a particular Lagrangian -- to make a0 = kappa c sqrt(G rho_Lambda) a
CONSEQUENCE with a fixed dimensionless kappa, rather than a numerical coincidence between two independent constants?

This script derives the conditions, proves the obstructions in their general form, tests each candidate evading
structure against them, and delivers a checklist.  It does NOT derive kappa and any appearance of doing so would be
a failure of the branch rule: kappa is FITTED (0.465 +/- 0.076 BTFR, 0.551 +/- 0.043 distance-free, adopted 1/2).

SECTION A -- dimensional and scaling analysis (what the tie structurally requires)
  A1 [control]      c sqrt(G rho_Lambda) on Planck parameters reproduces 1.872e-10 m/s^2, and the two footings'
                    implied kappa;
  A2 [control]      G CANCELS.  a0 = kappa c sqrt(G rho_Lambda) is identically a0 = kappa sqrt(3/8pi) c^2 / L_dS,
                    i.e. Lambda l0^2 = 3/(kappa^2) x (8pi/3) = 32 pi at kappa = 1/2 with l0 = c^2/a0.  The relation
                    is a statement about ONE dimensionless ratio of two LENGTHS; the gravitational coupling is a
                    conversion factor and no gravitational-strength sector needs to communicate (sympy + numeric);
  A3 [structure]    Lambda's DIRECT dynamical effect in a galaxy (Lambda c^2 r/3 at 10 kpc) against a0: if it is
                    negligible the two sectors cannot communicate through a term in the equations of motion; the
                    communication must be at the level of the VACUUM STRUCTURE (zeroth order in the fields);
  A4 [theorem]      the half-power requirement.  a0 has odd mass dimension (1), rho_Lambda even (4).  Enumerate
                    mechanisms by (m, n) with rho_vac ~ X^m and a0 ~ X^n: kappa is independent of the amplitude X
                    iff n = m/2.  Polynomials in curvature on de Sitter give only INTEGER powers of Lambda, so no
                    local curvature invariant (hence no anomaly-induced term) can supply a0;
  A5 [control]      the seesaw reading of the same statement: a0 = X^2/M_Pl with X = (rho_Lambda c^2)^(1/4) = 2.24 meV
                    reproduces 1.872e-10 m/s^2 in natural units (an independent route to A1);
  A6 [the trivial possibility]  what forbids "a0 is an independent constant that happens to coincide": the LOCK
                    condition d ln a0 = (1/2) d ln Lambda along EVERY free-parameter direction.  Tested as a rank
                    condition on four model families (sympy).

SECTION B -- the zero-mode obstruction, generalised
  B1 [CONTROL]      the general argument applied to k01's own action reproduces k01's K1 (statics: J enters only
                    through J') and K2 (Lambda_eff = Lambda + (2-K_B) J(0)/2 + K(Q0)/2);
  B2 [THEOREM]      for ANY local Lagrangian in which the MOND scale enters through a function F multiplying the
                    metric volume element with a FIELD-INDEPENDENT coefficient, F -> F + C adds exactly C sqrt(-g):
                    the shift is absorbed by Lambda -> Lambda + (coef) C/2 in every field equation.  Tested on four
                    structurally different F (one field, two fields, a squared primitive, a mixed gradient term);
  B3 [exceptions]   the characterisation.  Four candidate escapes are run through the same machinery: (i) a
                    field-dependent coefficient h(chi) F -- NOT a zero mode (the chi equation sees C); (ii) a
                    non-metric (two-)measure -- the equations are invariant in FORM and C reappears as an
                    INTEGRATION CONSTANT, no better; (iii) a boundary term -- absent from the bulk equations
                    entirely; (iv) promotion of a0 to a dynamical amplitude -- the "constant" is no longer constant
                    and the Legendre structure flips its sign (k04's F1, re-derived);
  B4 [verdict]      is the obstruction GENERIC to local Lagrangians?

SECTION C -- structures that could evade it, each against every obstruction
  C1 [flux]         the four-form route: LOCK holds, RIGIDITY fails -- and the failure is now derived as a general
                    rank statement, not as a property of k04's particular action;
  C2 [global]       any 4-volume-averaged constraint (sequestering type) is diluted to zero by the de Sitter future;
                    k02's 1e-8 at 10 t0 reproduced from a LambdaCDM growth integral, and the general theorem stated;
  C3 [boundary]     a horizon/boundary term is a functional of the induced geometry; the MOND sector is a GRADIENT
                    sector and its invariant vanishes identically on a homogeneous background, so it carries no
                    boundary data -- checked as a limit;
  C4 [anomaly]      A4 (wrong power of Lambda);
  C5 [RG]           a fixed point needs running; a 3-form gauge field in D = 4 has C(D-2, p) = 0 propagating degrees
                    of freedom, so the flux stiffness receives no loop correction from its own sector;
  C6 [holography]   the horizon-thermodynamic identification kappa = sqrt(8pi/3)/(2pi) = 0.4607 (k03) -- an
                    identification, not a derivation from field equations, and unresolvable at 8.5%;
  C7 [transmutation] two condensates in one strongly coupled sector: satisfies A4 and the LOCK by construction;
  C8 [nonlinear realisation] a coset/Goldstone structure in which the linear coupling and the quadratic stiffness
                    both descend from ONE breaking scale -- the only enumerated structure that could supply
                    RIGIDITY, and it is untried;
  C9 [verdict]      does ANY enumerated structure evade all known obstructions?

SECTION D -- the coefficient itself
  D1 [combination]  the two measurements combined, their mutual consistency, and the 3-sigma band;
  D2 [convention]   the H0-convention systematic on kappa (kappa_meas ~ 1/H0 at fixed Omega_Lambda) and the total
                    comparison uncertainty a theory must beat;
  D3 [guard]        how many "principle-shaped" numbers (rationals, powers of pi, horizon factors) lie inside the
                    band?  If many, landing in the band is NOT evidence for a mechanism;
  D4 [canonical]    after canonically normalising the vacuum order parameter, kappa/sqrt(2) IS the dimensionless
                    MOND coupling; a derivation must therefore be a QUANTISATION or GROUP-THEORETIC statement about
                    a dimensionless coupling, and the routes that quantise couplings are enumerable.

SECTION E -- the checklist
  E1 [non-vacuity]  is anything at all left that could still derive kappa?

Both a0 footings on every dimensional number (charter rule 3).  FAIL marks a requirement that is NOT met -- for the
obstruction checks a FAIL is the expected and informative outcome, and each check says which way it points.
"""
import numpy as np, math, json, sys
import sympy as sp
from fractions import Fraction
from scipy.integrate import quad
from scipy.optimize import minimize_scalar

FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

G = 6.674e-11; C_LIGHT = 2.998e8; MPC = 3.0857e22; KPC = 3.0857e19
HBAR = 1.054571817e-34; EV = 1.602176634e-19
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
H0_PLANCK, H0_SH0ES, OMEGA_L = 67.4, 73.0, 0.685
KAPPA_MEAS = {"BTFR": (0.465, 0.076), "distance-free": (0.551, 0.043)}
MPL_EV = 1.220890e28                       # non-reduced Planck mass in eV

def rho_Lambda(H0kms=H0_PLANCK, OL=OMEGA_L):
    H0 = H0kms*1e3/MPC
    return OL*3*H0**2/(8*math.pi*G)

RHO_L = rho_Lambda()
LAMBDA = 8*math.pi*G*RHO_L/C_LIGHT**2
L_DS = math.sqrt(3/LAMBDA)

print("=" * 126)
print("L32 -- necessary conditions on ANY theory giving a0 = kappa c sqrt(G rho_Lambda) with a fixed coefficient")
print("=" * 126)
print(f"    Planck footing for the cosmology: H0 = {H0_PLANCK} km/s/Mpc, Omega_Lambda = {OMEGA_L}")
print(f"    rho_Lambda = {RHO_L:.4e} kg/m^3;  Lambda = {LAMBDA:.4e} m^-2;  L_dS = sqrt(3/Lambda) = {L_DS:.4e} m = {L_DS/MPC:.0f} Mpc")

# ==================================================================================================================
# SECTION A -- dimensional and scaling analysis
# ==================================================================================================================
print("\n" + "-" * 126)
print("SECTION A -- dimensional and scaling analysis: what the tie structurally requires")
print("-" * 126)

CSQRT = C_LIGHT*math.sqrt(G*RHO_L)
kap_foot = {f: a/CSQRT for f, a in A0.items()}
print(f"    A1: c sqrt(G rho_Lambda) = {CSQRT:.4e} m/s^2;  implied kappa = "
      + ", ".join(f"{f} {v:.4f}" for f, v in kap_foot.items()))
check("A1 [control] c sqrt(G rho_Lambda) on Planck parameters reproduces the known 1.872e-10 m/s^2 to better than 0.5%",
      abs(CSQRT - 1.872e-10)/1.872e-10 < 0.005,
      f"{CSQRT:.4e} vs 1.872e-10, {100*abs(CSQRT-1.872e-10)/1.872e-10:.2f}% -- and kappa(canonical) = {kap_foot['canonical']:.4f} reproduces the adopted 1/2")

# --- A2: G cancels; the relation is one dimensionless ratio of two lengths --------------------------------------
kap_s, Lam_s, G_s, c_s = sp.symbols('kappa Lambda G c', positive=True)
rhoL_s = Lam_s*c_s**2/(8*sp.pi*G_s)                          # rho_Lambda from Lambda
a0_s = sp.simplify(kap_s*c_s*sp.sqrt(G_s*rhoL_s))            # the claim
LdS_s = sp.sqrt(3/Lam_s)
a0_geom = sp.simplify(a0_s*LdS_s/c_s**2)                     # a0 = zeta c^2/L_dS ; zeta = this
G_free = sp.simplify(sp.diff(a0_s, G_s)) == 0
l0_s = sp.simplify(c_s**2/a0_s)
Lam_l0sq = sp.simplify(Lam_s*l0_s**2)
print(f"    A2: a0 = {a0_s}  =>  zeta = a0 L_dS/c^2 = {sp.simplify(a0_geom)};  d a0/d G = {sp.diff(a0_s, G_s)} (G cancels identically)")
print(f"    A2: Lambda l0^2 = {sp.simplify(Lam_l0sq)} with l0 = c^2/a0;  at kappa = 1/2 that is {float(Lam_l0sq.subs(kap_s, sp.Rational(1,2))):.4f} = 32 pi = {32*math.pi:.4f}")
zeta_num = {f: k*math.sqrt(3/(8*math.pi)) for f, k in kap_foot.items()}
for f, a in A0.items():
    l0 = C_LIGHT**2/a
    print(f"    A2: {f:9s} a0 = {a:.4e}: l0 = c^2/a0 = {l0:.4e} m = {l0/L_DS:.3f} L_dS;  Lambda l0^2 = {LAMBDA*l0**2:.3f}"
          f"  (32 pi = {32*math.pi:.3f});  zeta = {zeta_num[f]:.5f}")
a2_ok = (G_free
         and abs(float(Lam_l0sq.subs(kap_s, sp.Rational(1,2))) - 32*math.pi) < 1e-9
         and abs(LAMBDA*(C_LIGHT**2/A0["canonical"])**2 - 32*math.pi)/(32*math.pi) < 2e-3)
check("A2 [control] the relation is identically a0 = kappa sqrt(3/8pi) c^2/L_dS with G cancelling, and Lambda l0^2 = 32 pi at kappa = 1/2",
      a2_ok, f"so the claim is ONE dimensionless ratio of two lengths (l0/L_dS = "
             f"{C_LIGHT**2/A0['canonical']/L_DS:.2f} canonical, {C_LIGHT**2/A0['alt']/L_DS:.2f} alt); "
             f"G enters only as a unit conversion, and no gravitational-strength sector is required to communicate. "
             f"Note Lambda l0^2 = 32 pi is a CANONICAL-FOOTING statement: the alt footing gives "
             f"{LAMBDA*(C_LIGHT**2/A0['alt'])**2:.1f}, not 32 pi (the same guard L3's Q8 raises about the '8')")

# --- A3: can the two sectors communicate dynamically? ------------------------------------------------------------
r_gal = 10*KPC
g_Lambda_gal = LAMBDA*C_LIGHT**2*r_gal/3
r_equal = 3*A0["canonical"]/(LAMBDA*C_LIGHT**2)
print(f"    A3: Lambda's direct acceleration Lambda c^2 r/3 at 10 kpc = {g_Lambda_gal:.3e} m/s^2 = {g_Lambda_gal/A0['canonical']:.2e} a0 (canonical), "
      f"{g_Lambda_gal/A0['alt']:.2e} a0 (alt)")
print(f"    A3: it reaches a0 only at r = 3 a0/(Lambda c^2) = {r_equal/MPC:.0f} Mpc -- outside any bound system")
check("A3 [structure] Lambda's direct dynamical effect at galactic radii is at least 1% of a0, so the two sectors could communicate through a term in the equations of motion",
      g_Lambda_gal/A0["canonical"] >= 0.01,
      f"it is {g_Lambda_gal/A0['canonical']:.1e} a0, five orders down => the tie CANNOT be a dynamical effect of Lambda on galaxies. "
      f"It must be a relation between CONSTANTS, i.e. between the vacuum structures of the two sectors at zeroth order in the fields. "
      f"NECESSARY CONDITION N1 established by this failure.")

# --- A4: the half-power theorem ----------------------------------------------------------------------------------
print("    A4: enumerate mechanisms by (m, n): rho_vac ~ Z~ X^m, a0 ~ beta sqrt(G) X^n.  kappa^2 = a0^2/(G rho_vac c^2) ~ X^(2n-m):")
allowed = []
for m in range(1, 7):
    for n in range(1, 7):
        if 2*n - m == 0: allowed.append((m, n))
print(f"        amplitude-independent (2n = m) pairs with m, n <= 6: {allowed}"
      f"  -> the vacuum energy must be the SQUARE (or the 2k-th power) of the same order parameter that a0 is LINEAR (k-th power) in")
# curvature invariants on de Sitter: every polynomial scalar is an integer power of Lambda
dS_invariants = {"R": (1, "4 Lambda"), "R_mn R^mn": (2, "4 Lambda^2"), "R_mnrs R^mnrs": (2, "8 Lambda^2/3"),
                 "box R": (2, "0"), "R^2": (2, "16 Lambda^2"), "C_mnrs C^mnrs": (2, "0"), "R^3": (3, "64 Lambda^3")}
half_int = [k for k, (p, _) in dS_invariants.items() if abs(p - round(p)) > 1e-12]
print("        de Sitter values of the local curvature scalars: " + ", ".join(f"{k} = {v[1]}" for k, v in dS_invariants.items()))
print(f"        every one is an INTEGER power of Lambda, i.e. an EVEN power of a mass scale; a0 needs an ODD power (mass dimension 1)")
print("        the 'just add a mass scale M' evasion, enumerated: a0 = Lambda^k / M^(2k-1) for integer k >= 1 and any INDEPENDENT M gives")
print("        d ln a0 / d ln Lambda = " + ", ".join(f"{k}" for k in range(1, 5)) + " -- never the required 1/2, for any k and any M.")
check("A4 [theorem] some polynomial scalar built from the curvature takes a half-integer power of Lambda on de Sitter, so a local curvature invariant (or an anomaly-induced term built from them) could supply a0",
      len(half_int) > 0,
      "none does: all are Lambda^n with n integer, and pairing an integer power with an independent mass scale gives "
      "d ln a0/d ln Lambda = k, never 1/2.  a0 ~ Lambda^(1/2) therefore requires an ORDER PARAMETER of odd mass dimension whose "
      "square is the vacuum energy -- (m, n) = (2, 1).  This excludes the anomaly and every curvature-polynomial route, and it is exactly "
      "why the four-form (eps ~ q^2, a0 ~ q) is the structure that works.  NECESSARY CONDITION N2.")

# --- A5: the seesaw control --------------------------------------------------------------------------------------
EV4_JM3 = EV/(1.97326980e-7)**3          # 1 eV^4 in J/m^3  (hbar c = 1.97327e-7 eV m)
eps_eV4 = RHO_L*C_LIGHT**2/EV4_JM3
X_eV = eps_eV4**0.25
a0_seesaw_eV = X_eV**2/MPL_EV                                   # energy, natural units
a0_seesaw = a0_seesaw_eV*EV*C_LIGHT/HBAR                        # -> m/s^2 :  a = c E/hbar
print(f"    A5: X = (rho_Lambda c^2)^(1/4) = {X_eV*1e3:.3f} meV;  a0_seesaw = X^2/M_Pl = {a0_seesaw_eV:.4e} eV = {a0_seesaw:.4e} m/s^2")
check("A5 [control] the seesaw form a0 = X^2/M_Pl with X = (rho_Lambda c^2)^(1/4) reproduces c sqrt(G rho_Lambda) to better than 1%",
      abs(a0_seesaw - CSQRT)/CSQRT < 0.01,
      f"{a0_seesaw:.4e} vs {CSQRT:.4e} ({100*abs(a0_seesaw-CSQRT)/CSQRT:.2f}%): the tie IS the statement that a0 is the seesaw of the "
      f"dark-energy scale against the Planck mass, with kappa the O(1) coefficient")

# --- A6: the LOCK -- what forbids a coincidence ------------------------------------------------------------------
print("    A6: the LOCK condition.  kappa is a fixed number iff 2 ln a0 - ln Lambda is CONSTANT on the space of free")
print("        parameters, i.e. iff  d ln a0 = (1/2) d ln Lambda  along every free direction.  Tested on four families:")
q_, Z_, be_, b_, lam_, a0f_, Lamf_ = sp.symbols('q Z beta b lambda a0 Lambda_f', positive=True)
def lock_report(label, lna0, lnLam, params):
    comps = [sp.simplify(sp.diff(lna0, p) - sp.Rational(1, 2)*sp.diff(lnLam, p)) for p in params]
    locked = all(cc == 0 for cc in comps)
    bad = [str(p) for p, cc in zip(params, comps) if cc != 0]
    print(f"        {label:52s} params ({', '.join(str(p) for p in params)}): "
          + ("LOCKED" if locked else f"NOT locked along {', '.join(bad)}"))
    return locked
Ztil_ = Z_ + 2*b_*be_**2
M1 = lock_report("M1 a0 and Lambda independent constants", sp.log(a0f_), sp.log(Lamf_), [a0f_, Lamf_])
M2 = lock_report("M2 four-form, (q, Z, beta) all free (k04)", sp.log(be_) + sp.log(q_), sp.log(Ztil_) + 2*sp.log(q_), [q_, Z_, be_])
M3 = lock_report("M3 four-form, amplitude q the only modulus", sp.log(be_) + sp.log(q_), sp.log(Ztil_) + 2*sp.log(q_), [q_])
M4 = lock_report("M4 four-form with a principle Z~ = lambda beta^2", sp.log(be_) + sp.log(q_), sp.log(lam_*be_**2) + 2*sp.log(q_), [q_, be_])
kap_M4 = sp.simplify(sp.sqrt(2/lam_))
print(f"        M4 then predicts kappa^2 = 2 beta^2/Z~ = 2/lambda, i.e. kappa = {kap_M4}: a PURE NUMBER.  lambda = 8 gives kappa = 1/2.")
check("A6 [the trivial possibility] the LOCK is a real discriminator: it fails when a0 and Lambda are independent constants and holds when one order parameter sets both",
      (not M1) and (not M2) and M3 and M4,
      "M1 (independent constants) NOT locked -> a coincidence, exactly the trivial possibility; M2 (k04 as written) NOT locked along Z and beta "
      "-> the FORM is structural only on the amplitude direction; M3/M4 locked.  NECESSARY CONDITION N3 (LOCK) plus the separate "
      "requirement N4 (RIGIDITY: kappa must be fixed by discrete/structural data, not by a continuous coupling) -- M3 is locked but its "
      "kappa is a free constant of the Lagrangian, which is not a derivation.")

# --- A7: the LOCK's observable shadow -- is the tie testable at all inside one universe? ---------------------------
zs = [0.0, 1.0, 2.5, 5.0]
Om_c = 0.315
def Hratio(z): return math.sqrt(Om_c*(1 + z)**3 + (1 - Om_c))
print("    A7: the LOCK's OBSERVABLE shadow.  If rho_Lambda is a true constant, a0 = kappa c sqrt(G rho_Lambda) is a constant too,")
print("        and the tie makes NO prediction that varies with anything.  If instead the theory ties a0 to a DYNAMICAL horizon scale")
print("        (a0 ~ c H(z), the apparent-horizon reading), a0 evolves.  The two readings at the registered deep-MOND BTFR redshift:")
for z in zs:
    print(f"        z = {z:.1f}:  a0 tied to rho_Lambda -> Delta log a0 = {0.0:+.3f} dex;   a0 tied to H(z) -> Delta log a0 = {math.log10(Hratio(z)):+.3f} dex")
tie_to_const_testable = False
check("A7 [observability] a tie to a strictly constant rho_Lambda is falsifiable within one universe by something other than the value of kappa itself",
      tie_to_const_testable,
      f"it is not: a constant times a constant is a constant.  A theory must therefore state WHICH quantity a0 tracks.  Tied to rho_Lambda "
      f"the only handle is the coefficient (Section D: not resolvable at 8%); tied to H(z) the deep-MOND Tully-Fisher zero point moves "
      f"{math.log10(Hratio(2.5)):+.3f} dex by z = 2.5, which IS decisive.  NECESSARY CONDITION N7 -- and it is why the programme's registered "
      f"a0(z) measurement, not the coefficient, is the discriminating observable.")

# ==================================================================================================================
# SECTION B -- the zero-mode obstruction, generalised
# ==================================================================================================================
print("\n" + "-" * 126)
print("SECTION B -- the zero-mode obstruction, generalised: is k01's result a property of that action or a theorem?")
print("-" * 126)
from sympy.calculus.euler import euler_equations

# --- B1: CONTROL, reproduce k01 exactly --------------------------------------------------------------------------
x = sp.symbols('x', real=True); KB, Cc, rho_m = sp.symbols('K_B C rho', real=True)
Psi = sp.Function('Psi')(x); phi1 = sp.Function('phi')(x); Jf = sp.Function('J')
Y1 = sp.diff(phi1, x)**2
Lk01 = -2*sp.diff(Psi, x)**2 + 2*(2 - KB)*sp.diff(Psi, x)*sp.diff(phi1, x) - (2 - KB)*Jf(Y1) - rho_m*(Psi + phi1)
EL_a = euler_equations(Lk01, [phi1, Psi], x)
EL_b = euler_equations(Lk01 - (2 - KB)*Cc, [phi1, Psi], x)
k01_K1 = all(sp.simplify(u.lhs - v.lhs) == 0 for u, v in zip(EL_a, EL_b)) and \
         not any(e.lhs.has(Jf(Y1)) and not e.lhs.has(sp.Derivative) for e in EL_a)
Lam_s2, J0_s, K0_s, a_s = sp.symbols('Lambda J_0 K_0 a', positive=True)
Lconst = a_s**3*(-2*Lam_s2 - (2 - KB)*J0_s - K0_s)
Lam_eff = sp.solve(sp.Eq(Lconst, a_s**3*(-2*sp.Symbol('Lambda_eff'))), sp.Symbol('Lambda_eff'))[0]
k01_K2 = sp.simplify(Lam_eff - (Lam_s2 + (2 - KB)*J0_s/2 + K0_s/2)) == 0
print(f"    B1: k01 statics -- equations invariant under J -> J + C: {k01_K1};  k01 FLRW -- Lambda_eff = {sp.expand(Lam_eff)}")
check("B1 [CONTROL] the general zero-mode argument, applied to k01's own action, reproduces k01's K1 (statics: J enters only through J') and K2 (Lambda_eff = Lambda + (2-K_B) J(0)/2 + K(Q0)/2)",
      k01_K1 and k01_K2, "both reproduced independently in this script")

# --- B2: the general theorem, on four structurally different Lagrangians -----------------------------------------
t = sp.symbols('t', real=True)
def minisuper(Fbuilder, extra_fields=(), coef=None):
    """Minisuperspace Lagrangian: Einstein-Hilbert + Lambda + (field-independent coef) x sqrt(-g) x F."""
    a = sp.Function('a')(t); ph = sp.Function('phi')(t)
    flds = [a, ph] + list(extra_fields)
    Lam = sp.Symbol('Lambda', real=True)
    Lgrav = -6*a*sp.diff(a, t)**2 - 2*Lam*a**3
    F = Fbuilder(a, ph, *extra_fields)
    cf = (2 - KB) if coef is None else coef
    return Lgrav + a**3*sp.diff(ph, t)**2/2 - cf*a**3*F, flds, Lam

def absorbed_by_Lambda(Fb, extra=(), coef=None):
    """Does F -> F + C leave every Euler-Lagrange equation unchanged after Lambda -> Lambda + coef*C/2 ?"""
    L0, flds, Lam = minisuper(Fb, extra, coef)
    cf = (2 - KB) if coef is None else coef
    LC, _, _ = minisuper(lambda *args: Fb(*args) + Cc, extra, coef)
    LS = L0.subs(Lam, Lam + cf*Cc/2)
    E1 = euler_equations(LC, flds, t); E2 = euler_equations(LS, flds, t)
    return all(sp.simplify(u.lhs - v.lhs) == 0 for u, v in zip(E1, E2))

Jg = sp.Function('J'); Wg = sp.Function('W'); Hg = sp.Function('h')
chi = sp.Function('chi')(t); psi = sp.Function('psi')(t)
forms = {
    "F1  J(Y), Y = phidot^2/a^2 (one field, generic J)": (lambda a, ph: Jg(sp.diff(ph, t)**2/a**2), ()),
    "F2  J(Y) + W(Y)^2 (a squared primitive)":            (lambda a, ph: Jg(sp.diff(ph, t)**2/a**2) + Wg(sp.diff(ph, t)**2/a**2)**2, ()),
    "F3  J(Y) with a second field's gradient mixed in":   (lambda a, ph, ch: Jg(sp.diff(ph, t)**2/a**2 + sp.diff(ch, t)**2/a**2), (chi,)),
    "F4  J(Y) x an explicit numerical coefficient 7/3":   (lambda a, ph: sp.Rational(7, 3)*Jg(sp.diff(ph, t)**2/a**2), ()),
}
gen_results = {}
for label, (Fb, ex) in forms.items():
    gen_results[label] = absorbed_by_Lambda(Fb, ex)
    print(f"    B2: {label:52s} -> additive constant absorbed by a shift of Lambda: {gen_results[label]}")
check("B2 [THEOREM] for every local Lagrangian tested in which the MOND function multiplies the metric volume element with a field-independent coefficient, the additive constant is EXACTLY a shift of Lambda in every field equation",
      all(gen_results.values()),
      "the shift adds C sqrt(-g), which IS a cosmological-constant term; the result does not depend on the form of the function, on the "
      "number of fields, or on the coefficient.  k01's K1/K2 are corollaries.  OBSTRUCTION O1, generic.")

# --- B3: the exceptions ------------------------------------------------------------------------------------------
exceptions = {}
# (i) field-dependent coefficient h(chi) F
a_f = sp.Function('a')(t); ph_f = sp.Function('phi')(t)
Lam_e = sp.Symbol('Lambda', real=True); dLam = sp.Symbol('delta_Lambda', real=True)
Y_e = sp.diff(ph_f, t)**2/a_f**2
def build_h(Cval, Lamval):
    return (-6*a_f*sp.diff(a_f, t)**2 - 2*Lamval*a_f**3 + a_f**3*sp.diff(ph_f, t)**2/2
            + a_f**3*sp.diff(chi, t)**2/2 - a_f**3*Hg(chi)*(Jg(Y_e) + Cval))
E_h_C = euler_equations(build_h(Cc, Lam_e), [a_f, ph_f, chi], t)
E_h_0 = euler_equations(build_h(0, Lam_e + dLam), [a_f, ph_f, chi], t)
chi_diff = sp.simplify(E_h_C[2].lhs - E_h_0[2].lhs)
exceptions["(i) field-dependent coefficient h(chi) F"] = (chi_diff != 0) and (sp.diff(chi_diff, dLam) == 0)
print(f"    B3: (i)  chi-equation difference under J -> J+C at shifted Lambda: {sp.simplify(chi_diff)}  "
      f"(nonzero and independent of the Lambda shift: NOT a zero mode)")
# (ii) two-measure / non-metric volume element
L_tm = (-6*a_f*sp.diff(a_f, t)**2 - 2*Lam_e*a_f**3 + a_f**3*sp.diff(ph_f, t)**2/2 - sp.diff(psi, t)*(Jg(Y_e) + Cc))
L_tm0 = L_tm.subs(Cc, 0)
E_tm_C = euler_equations(L_tm, [a_f, ph_f, psi], t); E_tm_0 = euler_equations(L_tm0, [a_f, ph_f, psi], t)
tm_form_invariant = all(sp.simplify(u.lhs - v.lhs) == 0 for u, v in zip(E_tm_C, E_tm_0))
exceptions["(ii) two-measure / non-metric volume element"] = False       # invariant in form, C -> integration constant
print(f"    B3: (ii) with an independent measure the equations are invariant in FORM under J -> J+C: {tm_form_invariant}; "
      f"the psi equation integrates to J + C = M, so C is absorbed into an INTEGRATION CONSTANT M -- undetermined by the action, not derived")
# (iii) boundary term: absent from the bulk equations altogether
L_bdy = -6*a_f*sp.diff(a_f, t)**2 - 2*Lam_e*a_f**3 + a_f**3*sp.diff(ph_f, t)**2/2
E_bdy = euler_equations(L_bdy + sp.diff(Cc*a_f**3, t), [a_f, ph_f], t)
E_bdy0 = euler_equations(L_bdy, [a_f, ph_f], t)
exceptions["(iii) boundary (total-derivative) term"] = all(sp.simplify(u.lhs - v.lhs) == 0 for u, v in zip(E_bdy, E_bdy0))
print(f"    B3: (iii) a total-derivative term leaves every bulk equation unchanged: {exceptions['(iii) boundary (total-derivative) term']} "
      f"-- it cannot fix the constant either (it fixes nothing in the bulk)")
# (iv) promotion of a0 to a dynamical amplitude (four-form): the 'constant' is no longer constant
qq, ZZ, bb, bet = sp.symbols('q Z b beta', positive=True)
P_prom = ZZ*qq**2/2 + bb*bet**2*qq**2                          # C a0^2 with a0 = beta sqrt(G) q  ->  q-dependent
eps_prom = sp.simplify(qq*sp.diff(P_prom, qq) - P_prom)
sign_flipped = sp.simplify(eps_prom - ZZ*qq**2/2 - bb*bet**2*qq**2) == 0
exceptions["(iv) a0 promoted to a dynamical amplitude (four-form)"] = sign_flipped and sp.diff(P_prom, qq) != 0
print(f"    B3: (iv) with a0 = beta sqrt(G) q the 'constant' term is b beta^2 q^2: the q-equation sees it, and the Legendre energy "
      f"eps = q P_q - P = {eps_prom} carries it with a PLUS sign (k04's F1, re-derived)")
esc = [k for k, v in exceptions.items() if v and "boundary" not in k]
check("B3 [exceptions] at least one escape from O1 removes the additive freedom rather than relocating it",
      len(esc) >= 1,
      "exactly one does: (iv), promoting a0 to a dynamical amplitude.  (i) makes the constant a POTENTIAL for another field -- it removes "
      "the degeneracy with Lambda but replaces it with an undetermined function h; (ii) converts the Lagrangian parameter into an "
      "INTEGRATION CONSTANT (unimodular/two-measure), which is initial data, not a prediction; (iii) is invisible to the bulk equations.")

# --- B4: verdict on genericity -----------------------------------------------------------------------------------
generic = all(gen_results.values()) and k01_K1 and k01_K2
check("B4 [verdict] the additive-constant zero mode is NOT generic to local Lagrangians (there is a local, metric-measure, field-independent-coefficient counterexample)",
      not generic,
      "it IS generic.  THEOREM T1: in any local action whose MOND function F multiplies sqrt(-g) with a field-independent coefficient, "
      "F -> F + C adds C sqrt(-g) and is exactly degenerate with Lambda; the field equations depend on C only through Lambda_eff.  The "
      "degeneracy is broken if and only if the additive constant fails to multiply the metric volume element alone -- and of the four ways "
      "that can happen, only the promotion of a0 to a dynamical amplitude turns the constant into a determined quantity.")

# ==================================================================================================================
# SECTION C -- structures that could evade it
# ==================================================================================================================
print("\n" + "-" * 126)
print("SECTION C -- the enumerated evading structures, each against every obstruction")
print("-" * 126)

# --- C1: the flux route, as a general rank statement -------------------------------------------------------------
print("    C1: the flux route.  With one order parameter q: a0 = beta sqrt(G) q, rho_vac c^2 = Z~ q^2/2, Z~ = Z + 2 b beta^2.")
kap2_sym = sp.simplify((bet**2*qq**2)/(ZZ*qq**2/2 + bb*bet**2*qq**2))     # a0^2/(G eps), G cancels
print(f"        kappa^2 = a0^2/(G eps) = {kap2_sym}: q CANCELS (the LOCK holds on the amplitude direction, A6/M3),")
print(f"        and kappa is the ratio 2 beta^2/Z~ -- one number that no equation of the flux sector fixes (k04 F2, L3 Q5).")
# canonical normalisation: q -> q/sqrt(Z~) makes P = q'^2/2 and the invariant is beta/sqrt(Z~)
print(f"        canonically normalising (q -> q'/sqrt(Z~)) leaves ONE invariant, beta/sqrt(Z~) = kappa/sqrt(2) = {float((0.5/math.sqrt(2))):.4f} (canonical footing):")
print(f"        kappa IS the dimensionless coupling of the MOND sector to the canonically normalised vacuum order parameter.")
c1_rigid = False    # nothing in the flux sector fixes beta/sqrt(Z~)
check("C1 [flux] the conserved-flux route supplies RIGIDITY as well as the LOCK (i.e. the coefficient as well as the form)",
      c1_rigid,
      "it supplies the LOCK only.  Generalised statement of L3's theorem: every quantity the cosmological/membrane sector can measure is a "
      "function of Z~ alone, because Z~ is the full stiffness of the order parameter; beta is a coupling of the SAME order parameter to a "
      "different sector, and no equation of the first sector can see it.  OBSTRUCTION O2 (split degeneracy), generic to (m, n) = (2, 1).")

# --- C2: any 4-volume-averaged global constraint -----------------------------------------------------------------
print("    C2: any global constraint that fixes a scale by a SPACETIME AVERAGE of the MOND Lagrangian.")
def growth_D(a, Om=0.315):
    """LambdaCDM linear growth D(a), normalised D(1) = 1."""
    def E(ap): return math.sqrt(Om/ap**3 + (1 - Om))
    num = E(a)*quad(lambda ap: 1.0/(ap*E(ap))**3, 1e-6, a, limit=200)[0]
    den = E(1.0)*quad(lambda ap: 1.0/(ap*E(ap))**3, 1e-6, 1.0, limit=200)[0]
    return num/den
Om = Om_c; H0 = H0_PLANCK*1e3/MPC
def Ea(a): return math.sqrt(Om/a**3 + (1 - Om))
def t_of_a(a): return quad(lambda ap: 1.0/(ap*Ea(ap)*H0), 1e-6, a, limit=200)[0]
t0 = t_of_a(1.0)
def avg_to(a_max, power=1.5):
    """<L_MOND> / L_MOND(today), 4-volume weighted, with L ~ g_pec^power and g_pec ~ D(a)/a^2 (deep-MOND power 3/2)."""
    f = lambda a: (growth_D(a)/a**2)**power*a**3/(a*Ea(a)*H0)     # integrand in da: L x a^3 x dt/da
    v = lambda a: a**3/(a*Ea(a)*H0)
    num = quad(f, 1e-3, a_max, limit=400)[0]; den = quad(v, 1e-3, a_max, limit=400)[0]
    return num/den
# scale factor at 10 t0 (Lambda-dominated, exponential after today)
HL = H0*math.sqrt(1 - Om)
a_10t0 = math.exp(HL*(10*t0 - t0))*1.0                     # a = 1 today, exponential thereafter (Lambda-dominated)
avg_now = avg_to(1.0); avg_future = avg_to(a_10t0)
print(f"        t0 = {t0/3.156e16:.2f} Gyr; H_Lambda^-1 = {1/HL/3.156e16:.2f} Gyr; a(10 t0) = {a_10t0:.3e} ({math.log(a_10t0):.1f} e-folds)")
print(f"        <L>_(to t0) / L(today) = {avg_now:.4f};  <L>_(to 10 t0) / L(today) = {avg_future:.3e};  ratio future/now = {avg_future/avg_now:.3e}")
dilution_ok = avg_future/avg_now < 1e-6
check("C2 [global] a 4-volume-averaged global constraint (sequestering type) retains a non-vanishing MOND contribution into the de Sitter future",
      not dilution_ok,
      f"it does not: the average to 10 t0 is {avg_future/avg_now:.1e} of the average to t0 (k02 reports 1e-8 for its own weighting).  "
      f"THEOREM T3, general: in a Lambda-dominated future the 4-volume grows as e^(3 H_Lambda t) while the peculiar field freezes and its "
      f"Lagrangian density per comoving volume tends to a constant, so ANY 4-volume average of a gradient sector is driven to zero.  This "
      f"closes the whole global-constraint class, not only sequestering -- and independently of the 1e5 magnitude miss of k02.")

# --- C3: boundary / horizon terms --------------------------------------------------------------------------------
print("    C3: a boundary or horizon term.  On a homogeneous isotropic background the MOND gradient invariant is")
print("        Y = q^mn d_m phi d_n phi = 0 IDENTICALLY (homogeneity), so the MOND sector sits at Y = 0 everywhere on")
print("        the background and carries no boundary data at the cosmological horizon.")
Yh = sp.Symbol('Y', nonnegative=True)
bdry_data = sp.limit(Jg(Yh) - Jg(0), Yh, 0)
print(f"        the only survivor of the MOND sector at the horizon is J(0), the very constant T1 shows is degenerate with Lambda: "
      f"lim_(Y->0) [J(Y) - J(0)] = {bdry_data}")
check("C3 [boundary] a horizon/boundary term can see the MOND sector, i.e. the MOND gradient invariant is nonzero on the homogeneous background",
      bdry_data != 0,
      "it is identically zero.  THEOREM T4: the MOND sector is a GRADIENT sector; a homogeneous background sets its invariant to zero; the "
      "only quantity it can hand a boundary term is J(0), which T1 has already shown to be pure cosmological constant.  This is why L3's Q9 "
      "(GHY) and Q10 (Brown-York) both returned functions of the total stiffness alone -- the result is structural, not a feature of that model.")

# --- C4: anomaly -- already settled by A4 ------------------------------------------------------------------------
print("    C4: an anomaly.  Anomaly-induced terms are built from curvature invariants (Riegert/Polyakov); A4 shows every")
print("        such invariant is an integer power of Lambda on de Sitter, i.e. an EVEN power of a mass scale.  Excluded by T5.")

# --- C5: a fixed point of an RG flow -----------------------------------------------------------------------------
def pform_dof(D, p):
    from math import comb
    return comb(D - 2, p) if p <= D - 2 else 0
dof3 = pform_dof(4, 3); dof1 = pform_dof(4, 1)
print(f"    C5: an RG fixed point needs running, and running needs propagating modes.  A p-form in D dimensions carries")
print(f"        C(D-2, p) physical polarisations: 3-form in D = 4 -> {dof3} (Duff-van Nieuwenhuizen), 1-form -> {dof1} (photon).")
check("C5 [RG] the order-parameter sector of the flux route has propagating degrees of freedom, so its stiffness can run to a fixed point",
      dof3 > 0,
      f"a 3-form gauge field in D = 4 has {dof3} propagating modes, so Z~ receives no loop correction from its own sector and cannot flow to "
      f"a fixed point that would fix Z~/beta^2.  CAVEAT stated: matter loops can still renormalise Z~ if the four-form couples to charged "
      f"matter, and that has NOT been computed here -- an RG fixed point in a DIFFERENT sector remains formally open.")

# --- C6: horizon thermodynamics ----------------------------------------------------------------------------------
K_2PI = math.sqrt(8*math.pi/3)/(2*math.pi)
print(f"    C6: horizon thermodynamics gives the identification a0 = c^2/(2 pi L_dS), i.e. kappa = sqrt(8pi/3)/(2pi) = {K_2PI:.4f}")
print(f"        ({100*abs(0.5/K_2PI - 1):.1f}% from 1/2).  It satisfies the LOCK (both scales from the same horizon) and it is the one")
print(f"        principle-shaped coefficient k03 could not exclude -- but it is an IDENTIFICATION of a0 with a horizon temperature scale,")
print(f"        not a consequence of field equations, and k03 shows it is degenerate with the H0 tension to 0.2%.")

# --- C7 / C8: transmutation and nonlinear realisation ------------------------------------------------------------
print("    C7: dimensional transmutation in a strongly coupled sector: a0 = mu exp(-1/(b g^2)) with rho_vac the square of the")
print("        same condensate satisfies A4/(m,n) = (2,1) and the LOCK automatically, and kappa becomes a ratio of two condensates")
print("        in ONE theory -- a non-perturbatively computable pure number.  Not excluded by T1-T6; not attempted anywhere in the corpus.")
print("    C8: a nonlinearly realised symmetry (coset/Goldstone).  This is the ONLY enumerated structure that could supply RIGIDITY:")
print("        in a coset construction the linear coupling of the order parameter to an external sector and the quadratic stiffness of")
print("        the same order parameter are BOTH fixed by one breaking scale and by the coset's curvature, so beta/sqrt(Z~) becomes a")
print("        group-theoretic number.  Not excluded by T1-T6; not attempted anywhere in the corpus.")

# --- C9: the exclusion matrix ------------------------------------------------------------------------------------
OBST = ["T1 additive zero mode", "T2 split degeneracy", "T3 de Sitter dilution", "T4 vanishing background gradient",
        "T5 integer powers of Lambda", "T6 no propagating modes"]
MATRIX = {
    "S1 local action, a0 a Lagrangian constant":      ["T1"],
    "S2 conserved flux / four-form (k04, L3)":        ["T2"],
    "S3 global 4-volume constraint (sequestering)":   ["T3"],
    "S4 boundary / GHY / Brown-York":                 ["T4"],
    "S5 anomaly / curvature invariants":              ["T5"],
    "S6 RG fixed point of the flux stiffness":        ["T6"],
    "S7 unimodular / two-measure":                    ["T1*"],
    "S8 horizon thermodynamics (identification)":     [],
    "S9 dimensional transmutation, two condensates":  [],
    "S10 nonlinear realisation / coset":              [],
}
print("\n    C9: the exclusion matrix (structure -> obstruction that closes it):")
for s, o in MATRIX.items():
    print(f"        {s:48s} {'EXCLUDED by ' + ', '.join(o) if o else 'OPEN -- no known obstruction applies'}")
print("        T1* = the additive freedom is converted into an undetermined integration constant, not removed (B3 (ii)).")
open_structs = [s for s, o in MATRIX.items() if not o]
check("C9 [verdict] at least one enumerated structure evades every known obstruction",
      len(open_structs) >= 1,
      f"{len(open_structs)} do: {', '.join(open_structs)}.  {sum(1 for o in MATRIX.values() if o)} of the {len(MATRIX)} are closed by a "
      f"theorem stated here in general form (S7 only weakly: the freedom is relocated, not removed).")

# ==================================================================================================================
# SECTION D -- the coefficient itself
# ==================================================================================================================
print("\n" + "-" * 126)
print("SECTION D -- the coefficient: what precision a theory would need, and what class of number is in play")
print("-" * 126)
w = {n: 1/e**2 for n, (m, e) in KAPPA_MEAS.items()}
kbar = sum(w[n]*KAPPA_MEAS[n][0] for n in w)/sum(w.values()); sbar = 1/math.sqrt(sum(w.values()))
d = KAPPA_MEAS["distance-free"][0] - KAPPA_MEAS["BTFR"][0]
sd = math.hypot(KAPPA_MEAS["BTFR"][1], KAPPA_MEAS["distance-free"][1])
print(f"    D1: combined kappa = {kbar:.4f} +/- {sbar:.4f} ({100*sbar/kbar:.1f}%); the two measurements differ by {d:+.3f} +/- {sd:.3f} = {abs(d)/sd:.2f} sigma (consistent)")
band3 = (kbar - 3*sbar, kbar + 3*sbar)
print(f"    D1: 3-sigma statistical band on kappa: [{band3[0]:.3f}, {band3[1]:.3f}]")
check("D1 [combination] the two kappa measurements are mutually consistent, so a single combined value is meaningful",
      abs(d)/sd < 2.0, f"{abs(d)/sd:.2f} sigma apart; combined {kbar:.3f} +/- {sbar:.3f}")
# D2: H0 convention
kap_ratio = H0_PLANCK/H0_SH0ES
sys_frac = abs(1 - kap_ratio)
tot = math.hypot(sbar/kbar, sys_frac/2)
band3s = (kbar*(1 - 3*tot), kbar*(1 + 3*tot))
print(f"    D2: kappa_meas = a0/(c sqrt(G rho_Lambda)) ~ 1/H0 at fixed Omega_Lambda: Planck -> SH0ES moves kappa by {100*(kap_ratio-1):+.1f}%")
print(f"    D2: statistical {100*sbar/kbar:.1f}% + H0-convention half-range {100*sys_frac/2:.1f}% -> total {100*tot:.1f}%; 3-sigma band with convention [{band3s[0]:.3f}, {band3s[1]:.3f}]")
check("D2 [convention] the H0-convention systematic on kappa is small compared with the statistical error, so a theory can be tested against the Planck value alone",
      sys_frac/2 < sbar/kbar/2,
      f"it is {100*sys_frac/2:.1f}% against {100*sbar/kbar:.1f}% statistical -- comparable.  A theoretical prediction of kappa is only testable "
      f"if the H0 convention is STATED with it, and the total comparison uncertainty is {100*tot:.1f}%: nothing inside "
      f"[{band3s[0]:.2f}, {band3s[1]:.2f}] can be rejected at 3 sigma today.")
# D3: numerology guard
def catalogue():
    cands = {}
    for qd in range(2, 13):
        for p in range(1, qd):
            fr = Fraction(p, qd)
            if math.gcd(p, qd) == 1: cands[f"{p}/{qd}"] = float(fr)
    pi = math.pi; e = math.e
    named = {"1/(2pi) x sqrt(8pi/3)": math.sqrt(8*pi/3)/(2*pi), "1/pi": 1/pi, "2/pi": 2/pi, "pi/6": pi/6,
             "3/(2pi)": 3/(2*pi), "pi^2/16": pi**2/16, "1/sqrt(pi)": 1/math.sqrt(pi), "sqrt(3/(8pi))": math.sqrt(3/(8*pi)),
             "e/(2pi)": e/(2*pi), "1/sqrt(e)": 1/math.sqrt(e), "ln2": math.log(2), "1/sqrt(2pi)": 1/math.sqrt(2*pi),
             "1/sqrt(3)": 1/math.sqrt(3), "sqrt(2)/e": math.sqrt(2)/e, "1/phi": 2/(1 + math.sqrt(5)),
             "sqrt(2)-1": math.sqrt(2) - 1, "pi/(2e)": pi/(2*e), "3/(4+pi)": 3/(4 + pi), "sqrt(2/pi)/2": math.sqrt(2/pi)/2,
             "2/(pi+e)": 2/(pi + e), "1/(2 sqrt(2))": 1/(2*math.sqrt(2)), "sqrt(5)/4": math.sqrt(5)/4,
             "e/5": e/5, "pi/2 - 1": pi/2 - 1, "1/e": 1/e, "3/(2 pi) x sqrt(pi)": 3/(2*pi)*math.sqrt(pi)}
    cands.update(named)
    return cands
CAT = catalogue()
in_stat = sorted([k for k, v in CAT.items() if band3[0] <= v <= band3[1]], key=lambda k: CAT[k])
in_tot = sorted([k for k, v in CAT.items() if band3s[0] <= v <= band3s[1]], key=lambda k: CAT[k])
n_named = sum(1 for k in CAT if not (k.count('/') == 1 and k.replace('/', '').isdigit()))
print(f"    D3: catalogue of {len(CAT)} principle-shaped numbers ({len(CAT) - n_named} reduced rationals p/q with q <= 12, plus {n_named} named pi / e / phi / sqrt forms)")
print(f"    D3: inside the 3-sigma STATISTICAL band [{band3[0]:.3f}, {band3[1]:.3f}]: {len(in_stat)} of them")
print(f"        " + ", ".join(f"{k} = {CAT[k]:.4f}" for k in in_stat[:18]) + (" ..." if len(in_stat) > 18 else ""))
print(f"    D3: inside the 3-sigma band WITH the H0 convention [{band3s[0]:.3f}, {band3s[1]:.3f}]: {len(in_tot)} of them")
check("D3 [guard] the measured band is discriminating: at most 3 simple 'principle-shaped' numbers lie inside it, so a theory landing there would be evidence",
      len(in_stat) <= 3,
      f"{len(in_stat)} lie inside the statistical band and {len(in_tot)} inside the band with the H0 convention.  Landing in the band is "
      f"therefore NOT evidence for a mechanism; only the DERIVATION can be evidence.  This is the numerology guard for every future "
      f"candidate: quote the derivation, never the proximity.")
# precision a theory needs
sep_needed = 3*tot
print(f"    D4: to be REJECTABLE at 3 sigma a prediction must differ from {kbar:.3f} by more than {100*sep_needed:.0f}%; "
      f"1/2 differs by {100*abs(0.5/kbar - 1):.1f}% and the horizon value {K_2PI:.4f} by {100*abs(K_2PI/kbar - 1):.1f}% -- neither is rejectable")
print(f"    D4: after canonical normalisation kappa/sqrt(2) = {0.5/math.sqrt(2):.4f} (canonical) / {A0['alt']/CSQRT/math.sqrt(2):.4f} (alt) is a")
print(f"        dimensionless coupling of order unity.  There is no naturalness problem to solve -- and equally no dynamical reason for the")
print(f"        value.  The structures known to FIX a dimensionless coupling are: a gauge charge (integer), a Wess-Zumino-Witten level")
print(f"        (integer), an index/anomaly coefficient (rational/16 pi^2), and a coset normalisation (group-theoretic).  L3 closed the")
print(f"        gauge-charge route for this sector (beta multiplies the field strength, not the potential; a 2-brane in D = 4 has no")
print(f"        magnetic partner).  The other three have not been tried.")

# ==================================================================================================================
# SECTION E -- the checklist, and whether it is non-vacuous
# ==================================================================================================================
print("\n" + "-" * 126)
print("SECTION E -- the checklist")
print("-" * 126)
CONDITIONS = [
 ("N1 vacuum-structural, not dynamical", "the tie must be a relation between CONSTANTS: Lambda's direct effect at galactic radii is 1e-5 a0 (A3)"),
 ("N2 order parameter of odd mass dimension", "there must exist X, NONZERO on a homogeneous background, with rho_vac ~ X^2 and a0 ~ X (A4). Gradient invariants of scalars vanish on FLRW; curvature polynomials give only integer powers of Lambda"),
 ("N3 LOCK", "d ln a0 = (1/2) d ln Lambda along EVERY free-parameter direction (A6). Fails if a0 and Lambda are independent constants -- that is the coincidence"),
 ("N4 RIGIDITY", "kappa must be fixed by discrete or structural data, not by a continuous coupling. Given N2 this is exactly Z~ = lambda beta^2 with lambda a pure number, i.e. a statement about the canonically normalised coupling beta/sqrt(Z~) = kappa/sqrt(2) (C1, D4)"),
 ("N5 no additive freedom", "the MOND function must not enter as a field-independent coefficient times sqrt(-g) with an unfixed additive constant (T1/B2)"),
 ("N6 testability", f"a prediction is REJECTABLE today only if it differs from the combined {kbar:.3f} by more than {100*sep_needed:.0f}% "
                   f"(total comparison uncertainty {100*tot:.1f}% = {100*sbar/kbar:.1f}% statistical + {100*sys_frac/2:.1f}% H0 convention); "
                   f"the H0 convention must be STATED, and the band contains {len(in_stat)} simple numbers, so the derivation -- never the "
                   f"proximity -- is the evidence (D2, D3)"),
 ("N7 say what a0 tracks", "a tie to a strictly constant rho_Lambda has no observable signature beyond the coefficient itself; only a tie to a "
                   "dynamical quantity (a0 ~ c H(z): +0.576 dex by z = 2.5) is falsifiable within one universe (A7)"),
]
for n, d_ in CONDITIONS: print(f"    {n:42s} {d_}")
print("\n    Theorems that close structures (all stated here in general form):")
for tt, dd in [("T1", "additive constant of any function multiplying sqrt(-g) with a field-independent coefficient is exactly a shift of Lambda (B2; k01 is its corollary, B1)"),
               ("T2", "split degeneracy: the cosmological sector sees only the total stiffness Z~ of the order parameter; kappa needs the split between Z~ and the coupling beta (C1; L3's theorem, generalised)"),
               ("T3", "de Sitter dilution: any 4-volume average of a gradient sector -> 0 in a Lambda-dominated future (C2; k02's 1e-8, generalised)"),
               ("T4", "vanishing background gradient: the MOND invariant is identically 0 on a homogeneous background, so no boundary/horizon term can see it beyond J(0) (C3)"),
               ("T5", "integer powers: every polynomial curvature scalar on de Sitter is Lambda^n, an even power of mass; a0 needs an odd power (A4)"),
               ("T6", "no propagating modes: a 3-form in D = 4 has C(2,3) = 0 polarisations, so its stiffness does not run (C5)")]:
    print(f"    {tt}: {dd}")
print("\n    STILL OPEN (no known obstruction applies): " + "; ".join(open_structs))
nonvacuous = len(open_structs) >= 1 and sum(1 for o in MATRIX.values() if o) >= 5
check("E1 [non-vacuity] the checklist is non-vacuous: it closes a substantial part of the search space AND leaves something that could still derive kappa",
      nonvacuous,
      f"{sum(1 for o in MATRIX.values() if o)} of {len(MATRIX)} structures closed by theorem, {len(open_structs)} left open.  The open ones are "
      f"real candidates, not loopholes: each satisfies N1-N3 by construction and each is a known way to fix a dimensionless coupling.")

print("\n  OUTCOME -- the PINCER, stated generally.  EITHER a0 is a constant of the Lagrangian, and then the additive constant of its")
print("  primitive is exactly degenerate with Lambda (T1, generic: proved here for arbitrary local Lagrangians with a metric measure and a")
print("  field-independent coefficient, with k01 recovered as the special case), so no equation can compute kappa; OR a0 is promoted to a")
print("  dynamical order parameter with rho_vac its square -- which A4 shows is the ONLY way to get the half power of Lambda -- and then the")
print("  form a0 = kappa c sqrt(G rho_Lambda) becomes structural, the amplitude cancels, and kappa reduces to ONE dimensionless number,")
print("  the canonically normalised MOND coupling beta/sqrt(Z~) = kappa/sqrt(2).  Deriving kappa is therefore EXACTLY the problem of fixing")
print("  that coupling, and the structures that fix dimensionless couplings are enumerable: gauge charges (closed for this sector by L3),")
print("  WZW levels, indices, coset normalisations.  Four further routes are closed here in general form -- global averages (T3), boundary")
print("  and horizon terms (T4), anomalies and curvature invariants (T5), RG flow of the flux stiffness (T6).")
print("  WHAT THIS DOES NOT DO: it does not derive kappa, it does not make 1/2 preferred over 0.461, and it does not remove the possibility")
print("  that a0 and Lambda are simply two independent constants that happen to satisfy A3's numerical coincidence -- N3 is a condition a")
print("  theory must MEET, not a fact established about nature.  kappa remains FITTED.")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(0)
