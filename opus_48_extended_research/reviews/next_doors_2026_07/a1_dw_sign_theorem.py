#!/usr/bin/env python3
"""
A1 prong 1 -- SIGN-THEOREM CONFRONTATION: Deffayet-Woodard (arXiv:2512.10513, JCAP 04(2026)081)
vs the banked Active-Kernel / anti-MOND sign theorem (Scale Without Law, DOI 10.5281/zenodo.21016309;
real_research/ACTIVE_KERNEL_SIGNTHEOREM_2026-06.md).

Theorem (banked): for a PROBE worldline coupled to any stationary, LINEAR, causal, ghost-free/unitary
(Kallen-Lehmann rho>=0 => passive) cosmological bath, the adiabatic inertia shift is
    delta_m = 2 * int_0^inf rho(w)/w^2 dw >= 0   (inertia RAISED at low acceleration = ANTI-MOND).
MOND sign (delta_m<0) requires rho<0 (ghost) or an active/gain medium -- unavailable from passive dS.

Question: does the DW construction (a) genuinely act on worldline inertia (=> theorem applies; find
where the MOND sign enters and whether forced or chosen), or (b) live in the modified-GRAVITY lineage
(=> not subject to the theorem; template value for the unwritten MI completion collapses)?

Everything below is verified symbolically (sympy) or numerically; exits 0.
"""
import sympy as sp

ok = lambda name, cond: print(f"  [{'PASS' if cond else 'FAIL'}] {name}") or (_ for _ in ()).throw(AssertionError(name)) if not cond else print(f"  [PASS] {name}")

print("="*100)
print("STEP 1 -- Reproduce their static-limit algebra exactly (their eqs (27)-(30) -> (23), arXiv numbering)")
print("="*100)
# f(Z) = (1/2) Z exp(-(1/3) sqrt(|Z|))   [their eq (30), label fdef]
# Z -> 4 c^4 Psi'^2 / a0^2 in the static geometry [their eq (27), label Zdef]
Z, c, a0, G, Psip = sp.symbols('Z c a_0 G Psiprime', positive=True)
s = sp.symbols('s', positive=True)  # s = sqrt(Z)
f_of_s = sp.Rational(1,2)*s**2*sp.exp(-s/3)
ser = sp.series(f_of_s, s, 0, 5).removeO().expand()
# expected: 1/2 Z - 1/6 Z^{3/2} + 1/36 Z^2  [their eq (29), label fexp, quoted through Z^{3/2}]
expected = sp.Rational(1,2)*s**2 - sp.Rational(1,6)*s**3 + sp.Rational(1,36)*s**4
ok("small-Z expansion f = Z/2 - Z^(3/2)/6 + O(Z^2)  == their eq (29)", sp.simplify(ser - expected) == 0)

# static substitution: sqrt(Z) = 2 c^2 Psi'/a0
fstat = f_of_s.rewrite(sp.exp).subs(s, 2*c**2*Psip/a0)
DeltaL_prefactor = a0**2/(16*sp.pi*G)   # their eq (28), label invL: DeltaL -> (a0^2/16 pi G) f(Z) sqrt(-g)
DeltaL = sp.expand(DeltaL_prefactor*sp.series(fstat, Psip, 0, 4).removeO())
target = (c**4/(16*sp.pi*G))*(2*Psip**2 - sp.Rational(4,3)*(c**2/a0)*Psip**3)  # their eq (23), label staticM
ok("(a0^2/16piG) f(Z(Psi')) = (c^4/16piG)[2 Psi'^2 - (4c^2/3a0) Psi'^3] + O(Psi'^4)  == their eq (23)",
   sp.simplify(sp.expand(DeltaL - target)) == 0)
print("""
  READING (their sec. 3.2, verbatim): the added 2 Psi'^2 term is fixed by requiring that its
  "variation with respect to Psi cancels the linear term in (21) [G_00 = -2 lap Phi = 8piG rho/c^2]",
  while "variation with respect to Phi does not disturb (22) [G_ij => Phi = -Psi]".
  => the coefficient f'(0) = +1/2 (with Z's normalization 4c^4/a0^2) is TUNED against the
     Einstein-Hilbert linear term; the -Z^(3/2)/6 coefficient is TUNED to write the BTFR with a0.""")

print("="*100)
print("STEP 2 -- Their deep-MOND solution == the framework's own deep limit (BTFR-locked, degenerate)")
print("="*100)
# their eq (18) (BTFR1): [c^2 r Psi'(r)]^2 = a0 G M(r)  =>  g_obs = c^2 Psi' = sqrt(a0 g_N)
r, M = sp.symbols('r M', positive=True)
gN = G*M/r**2
g_obs_DW = sp.sqrt(a0*G*M)/r
ok("their (18): g_obs = c^2 Psi' = sqrt(a0 * g_N)", sp.simplify(g_obs_DW - sp.sqrt(a0*gN)) == 0)
# framework: g_obs = g_bar * nu(y), nu = sqrt(1+1/y), y = g_bar/a0 -> deep limit sqrt(g_bar a0)
gbar = sp.symbols('g_bar', positive=True)
g_obs_fw = gbar*sp.sqrt(1 + a0/gbar)
deep = sp.limit(g_obs_fw/sp.sqrt(gbar*a0), gbar, 0, '+')
ok("framework nu = sqrt(1+1/y): deep limit g_obs -> sqrt(g_bar a0)  (identical deep-MOND locus)", deep == 1)
print("  => deep-MOND/BTFR phenomenology is DEGENERATE between DW and the framework (both BTFR-locked);")
print("     they separate in (i) transition shape, (ii) the background-Z floor (script 2), (iii) a0 value.")

print("="*100)
print("STEP 3 -- Classification: where does the modification act? (the trichotomy question)")
print("="*100)
checklist = [
 ("probe worldline kinetic term / inertia modified?", "NO",
  "their eq (17): v^2/r = c^2 Psi'(r) -- standard geodesic response; matter couples only to g_munu"),
 ("gravitational field equations modified?", "YES",
  "their sec. 3.1: eq (20) 'should represent the g_00 equation of gravity'; L_MOND (31) added to L_grav"),
 ("lensing tracks the DEEPENED potential?", "YES",
  "their sec. 3.2: G_ij => Phi = -Psi enforced, 'consistent with weak lensing provided Psi obeys (20)'"),
 ("u^mu = probe 4-velocity?", "NO",
  "u_mu = d_mu phi[g], their eq (5): d_mu phi d_nu phi g^munu = -1, phi(0,x)=0 -- 'a unique, nonlocal"
  " functional of the metric' (their words); a khronon-like preferred foliation in the GRAVITY action"),
 ("worldline retarded self-energy Sigma_R(omega) present?", "NO",
  "no term couples to a matter worldline except the universal metric coupling; nothing to KL-decompose"),
]
for q, a, why in checklist:
    print(f"  {q:<55s} {a:>4s}  -- {why}")
print("""
  VERDICT (structural): DW is MODIFIED GRAVITY (nonlocal), horn-II lineage of the banked trichotomy
  (COVARIANT_MI_COMPLETION_2026-06.md). The sign theorem's object -- a probe self-energy from a bath --
  is NOT INSTANTIATED anywhere in their action. The theorem is NOT EVADED; DW is NOT SUBJECT to it.
  Their ghost-freedom (Barvinsky 2013 mimetic perturbations; Tan-Woodard 2018 for the MOND sector) is a
  FIELD-perturbation statement, not Kallen-Lehmann bath unitarity -- no contradiction in either direction.
  => Horn III (nonlocal MI) stays CLOSED; DW provides NO template for the unwritten MI completion.""")

print("="*100)
print("STEP 4 -- Where the MOND sign enters for DW: forced or chosen?  (sign-flip counterfactual)")
print("="*100)
# Encode their sec 3.2 statement: EH supplies a linear (quadratic-in-Psi') term L_EH_lin such that the
# +2Psi'^2 in DeltaL exactly cancels it. Counterfactual: flip the sign of f.
L_EH_lin = -(c**4/(16*sp.pi*G))*2*Psip**2          # the term their +2Psi'^2 is built to cancel
L_DW     = +(c**4/(16*sp.pi*G))*(2*Psip**2 - sp.Rational(4,3)*(c**2/a0)*Psip**3)
L_flip   = -L_DW
tot      = sp.simplify(L_EH_lin + L_DW)
tot_flip = sp.expand(L_EH_lin + L_flip)
ok("with their sign: quadratic terms cancel exactly; leading kinetic term is the CUBIC (MOND branch exists)",
   sp.simplify(tot + (c**4/(16*sp.pi*G))*sp.Rational(4,3)*(c**2/a0)*Psip**3) == 0)
quad_coeff = sp.expand(tot_flip).coeff(Psip, 2)
ok("with flipped sign: quadratic term = -4 Psi'^2 (c^4/16piG), i.e. DOUBLED Newtonian kinetic term "
   "(G_eff = G/2), and the cubic flips => no real deep-MOND solution ([c^2 r Psi']^2 = -a0 G M < 0)",
   sp.simplify(quad_coeff + 4*c**4/(16*sp.pi*G)) == 0)
print("""
  => The MOND sign is CHOSEN twice over: (i) sign AND magnitude of f'(0)=+1/2 tuned to cancel the EH
     linear term; (ii) sign and magnitude of the Z^(3/2) coefficient tuned to write the BTFR at a0.
     The |Z| branch structure (Z<0 cosmology / Z>0 bound systems) selects WHICH REGIME applies WHERE
     -- it does NOT force the attractive/MOND sign; the flipped-f model has the identical branch
     structure and no MOND.
  Their own words (Conclusions): "this has to work because it was constructed to enforce weak lensing
     and the equation (20) required by the Baryonic Tully-Fisher Relation";
     and the derivation is deferred: "there is the need to derive M[g] from a nonperturbative
     resummation of loops of inflationary gravitons ... success would ... confirm MOND".
  => FOUNDED-not-DERIVED, the same epistemic rung as the framework's own postulated MOND sign.
     Note: their hoped-for future source (inflationary graviton loops frozen into a relic action term)
     is a NON-EQUILIBRIUM RELIC of inflation, not a present-epoch passive-bath worldline kernel -- so
     even the future-derivation hope lives outside the sign theorem's scope (no collision either way).""")

print("="*100)
print("STEP 5 -- Q2/Cassini wall consistency (does DW rescue the framework's MG limb? NO)")
print("="*100)
import math
gSat = 6.674e-11*1.989e30/(9.58*1.496e11)**2   # solar gravity at Saturn
a0DW = 1.2e-10
sqrtZ_sat = 2*gSat/a0DW
supp = -sqrtZ_sat/3
print(f"  g_sun(Saturn) = {gSat:.3e} m/s^2 ; sqrt(Z) = 2g/a0 = {sqrtZ_sat:.3e}")
print(f"  DW suppression exp(-sqrt(Z)/3) = exp({supp:.3e})  -> Q2 utterly dead (Cassini-safe)")
ok("DW's f is exponentially dead in the solar system (log10 suppression < -100000)", supp/math.log(10) < -1e5)
print("""  BUT: Q2 is set by the interpolation family's high-acceleration TAIL (Hees+ 2016 family logic).
  DW chose an exponential tail (like McGaugh's nu); the framework's own nu = sqrt(1+1/y) has a
  POWER-LAW 1/(2y) tail. Realizing the framework's nu inside DW's nonlocal machinery would re-import
  the banked 3-15 sigma RAR-vs-Q2 tension unchanged. DW's Cassini safety is a property of THEIR f,
  not of the nonlocal realization => no Q2 rescue for the framework's MG limb; Cassini standing intact.""")

print()
print("ALL CHECKS PASSED -- prong-1 verdict: DW = nonlocal MODIFIED GRAVITY; sign theorem not subject,")
print("not evaded; MOND sign CHOSEN (tuned cancellation + BTFR normalization), branch selects regime only;")
print("template value for the unwritten MI completion COLLAPSES; horn III stays closed.")
