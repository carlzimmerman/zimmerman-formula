#!/usr/bin/env python3
"""VERIFY the reviewer's kill of my own tandem-mu result (verify a kill as hard as a win). Claim: the
covariant projection G~_0mu=mu G_0mu gives mu*nabla^2 Phi = 4piG rho, NOT the AQUAL div[mu grad Phi];
the missing grad(mu).grad(Phi) is LEADING order in deep MOND, so the ansatz FAILS the MOND gate."""
import sympy as sp

r, GM, a0, C = sp.symbols('r GM a0 C', positive=True)
Phi = sp.Function('Phi')

print("=== the two operators, spherical, OUTSIDE the source (rho=0) ===")
# deep-MOND constitutive: mu = |gradPhi|/a0 = Phi'/a0
Php = sp.Function('Phi')(r).diff(r)
mu = Php/a0
lap = lambda F: sp.diff(F, r, 2) + 2*sp.diff(F, r)/r

# (A) TANDEM law: mu * nabla^2 Phi = 0 outside
tandem = sp.simplify(mu*lap(sp.Function('Phi')(r)))
# (B) AQUAL: div[mu gradPhi] = (1/r^2) d/dr[r^2 mu Phi'] = 0 outside
aqual = sp.simplify(sp.diff(r**2 * mu * Php, r)/r**2)
print("   (A) tandem  mu*lap(Phi) = 0   and   (B) AQUAL (1/r^2)d_r[r^2 mu Phi'] = 0")

# solve each for the force g=Phi' outside a point mass
gg = sp.Function('g')  # g = Phi'
# (A): mu*lap = (g/a0)(g' + 2g/r) = 0 (g!=0) => g' + 2g/r = 0 => g = C/r^2  (NEWTONIAN)
solA = sp.dsolve(sp.Eq(sp.Function('g')(r).diff(r) + 2*sp.Function('g')(r)/r, 0))
print(f"   (A) tandem outside: g' + 2g/r = 0  =>  {solA}  ->  g ~ 1/r^2  = NEWTONIAN (NO MOND)")
# (B): (g/a0)(...) integrated: r^2 mu g = const => r^2 (g/a0) g = const => g^2 ~ 1/r^2 => g ~ 1/r
print(f"   (B) AQUAL outside:  r^2 (g^2/a0) = const  =>  g ~ 1/r  = MOND (flat rotation curve)")

print("\n=== the missing term is LEADING order in deep MOND ===")
# div[mu gradPhi] = mu lap(Phi) + grad(mu).grad(Phi); compare the two pieces for g~1/r (MOND)
g = sp.sqrt(GM*a0)/r          # the CORRECT deep-MOND force
mu_of_r = g/a0
term_kept    = sp.simplify(mu_of_r * (sp.diff(g,r) + 2*g/r))   # mu * lap(Phi)  with Phi'=g
term_missing = sp.simplify(sp.diff(mu_of_r, r) * g)            # grad(mu).grad(Phi)
print(f"   kept   (mu*lap):        {term_kept}")
print(f"   missing (grad mu.grad): {term_missing}")
print(f"   ratio missing/kept = {sp.simplify(term_missing/term_kept)}  -> O(1): SAME ORDER, not small.")

print("\n=== VERDICT: tandem/projection ansatz KILLED on the MOND gate (reviewer, verified) ===")
print("G~_0mu = mu G_0mu  =>  mu*nabla^2 Phi = 4piG rho  =>  NEWTONIAN outside a point mass (g~1/r^2),")
print("NOT MOND. My earlier 'MOND inherited' was ASSERTED (I assumed the AQUAL form) not DERIVED -- the")
print("projection is missing grad(mu).grad(Phi), which is O(1) vs the kept term in deep MOND. RETRACTED.")
print("The E/F gate results (gamma=1, e^-y Cassini screening) were real but MOOT: the theory has no MOND.")
print("SURVIVING open family (reviewer): metric-derived nonlocal acceleration constitutive gravity --")
print("u^mu from the metric's OWN timelike-Killing/stationary structure, a_mu=grad_mu ln sqrt(-xi^2)~grad Phi,")
print("y=sqrt(a.a)/a0, S=R+a0^2 F(a^2/a0^2), F'~1-e^-y. GATE: can u^mu[g] be defined causally+covariantly")
print("WITHOUT an independent preferred-frame DOF? (scalar-clock=khronometric CLOSED; matter-eigenvector")
print("=geodesic dust a^mu=0 KILLED). That is genuinely new territory -- not bimetric/DHOST/khronometric.")
import json
print("CERTIFICATE_JSON:", json.dumps({"gate":"tandem-projection-MOND","status":"KILL",
 "certificate":("Covariant projection G~_0mu=mu G_0mu gives mu*nabla^2 Phi=4piG rho => NEWTONIAN outside "
   "a point mass (g~1/r^2), NOT MOND. Missing grad(mu).grad(Phi) is O(1) vs the kept term in deep MOND "
   "(same order, verified). My prior 'MOND inherited' was asserted not derived => RETRACTED; E/F results "
   "(gamma=1, e^-y Cassini) real but MOOT without MOND. Reviewer kill, independently verified. Surviving "
   "OPEN family: metric-derived nonlocal acceleration constitutive gravity (u^mu from the metric's own "
   "Killing/stationary structure); gate = define u^mu[g] causally+covariantly with NO independent "
   "preferred-frame DOF."),"numeric_values":{"tandem_outside":"g~1/r^2 Newtonian","missing_over_kept":"O(1)"}}))
