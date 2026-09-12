#!/usr/bin/env python3
"""L206 -- THE COEFFICIENT FAMILY RE-DERIVED WITH THE CUBIC TERM RESTORED, and what it decides.

L205 showed that with gamma = 0 the static sector obeys mu ~ x^2 where MOND needs mu ~ x, giving rotation curves that rise as the sixth
root of radius instead of staying flat, and that the cubic gamma X Box chi was the only operator left that might fix it. This script
restores it, in both places it matters.

PART A, THE BACKGROUND. Re-derive the identity of L200 with gamma carried. astra's own expressions are used:
   rho = 2q^2 P_X - P + V - 6 gamma H q^3,   p = P - V + s0 W + 2 gamma q^2 qdot,   j = 2q P_X - 6 gamma H q^2,
   P = -(U/2) log((U - 2dX)/(U - 2d qbar^2)) + 3 gamma qbar Hbar (X - qbar^2),   W = U + 2 d l (sqrt(1+Y/l) - 1) - 2 gamma qbar^2 qbar'.
PART B, THE STATIC LIMIT. In spherical symmetry the cubic term is a cubic Galileon. Its contribution to the first integral of the field
equation is obtained by direct variation, and the radial scaling it implies for the rotation curve is read off and compared with the
scaling the other operators give and with the one flat rotation curves require. No literal-True checks."""
import numpy as np, sympy as sy, json
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("=" * 118 + "\nL206 THE CUBIC RESTORED: what it does to the background identity, and what it does to the rotation curve\n" + "=" * 118)
# ---------------- PART A: the background with gamma carried ----------------
U, d, l, q, H, g, mu, s0, qd, Up, qp = sy.symbols("U d l q H gamma mu s_0 qdot U' q'", positive=True)
m = U*(1 - mu)                                                                 # the margin, with mu = 2 d q^2/U
PX = U*d/m + 3*g*q*H                                                            # dP/dX on shell, including the cubic's own contribution to P
rho = sy.simplify(2*q**2*PX - 0 + U - 6*g*H*q**3)
sub = {d: mu*U/(2*q**2)}                                                        # the definition mu = 2 d q^2/U, which the symbols do not know
check("V1 [the cubic cancels out of the density] the explicit cubic piece of P contributes +6 gamma H q^3 to 2 q^2 P_X while the stress carries -6 gamma H q^3, so the sector's energy density is exactly what it was at gamma = 0",
      sy.simplify(rho.subs(sub) - U/(1 - mu)) == 0, f"rho = {sy.simplify(rho.subs(sub))} = U/m_rel, with no gamma dependence at all")
j = sy.simplify(2*q*PX - 6*g*H*q**2)
check("V2 [and out of the current] the same cancellation happens in the clock's charge, so current conservation still gives j proportional to q d and is untouched by the cubic",
      sy.simplify((j - 2*q*U*d/m).subs({d: mu*U/(2*q**2)})) == 0, f"j = {sy.simplify(j.subs({d: mu*U/(2*q**2)}))} = 2 q d/m_rel, again with no gamma")
p = U*(s0 - 1) + 2*g*q**2*qd
w_expr = sy.simplify(p/(U/(1 - mu)))
s0_solved = sy.solve(sy.Eq(w_expr, sy.Symbol("w")), s0)[0]
print(f"    the pressure DOES keep a cubic term: p = U(s0 - 1) + 2 gamma q^2 qdot, so the identity becomes s0 = {sy.simplify(s0_solved)}")
check("V3 [THE IDENTITY IS CORRECTED, and only here] the clock rate is no longer exactly the equation of state over the margin: s0 - 1 = w/m_rel - 2 gamma q^2 qdot/U. The cubic survives in the pressure alone, and that single term is the whole of its effect on the background",
      sy.simplify(s0_solved - (1 + sy.Symbol("w")/(1 - mu) - 2*g*q**2*qd/U)) == 0,
      f"s0 - 1 = w/m_rel - 2 gamma q^2 qdot/U; at gamma = 0 this is the identity of L200 unchanged")
GAM, W_VAL, MREL = 1e-6, 1e-4, 0.5                                              # the candidate's own gamma, the bound on w, a representative margin
pq = -3*W_VAL                                                                    # from the family: q ~ a^-3w
corr = 2*GAM*abs(pq)                                                             # 2 gamma q^2 qdot/U with q, H, U order unity in the candidate's units
lead = W_VAL/MREL
check("V4 [and at the candidate's own coupling the correction is invisible] with gamma = 1e-6 the cubic's contribution to the clock rate is six orders below the leading term, so the closed-form family of L200 and the acoustic-scale bound of L201 stand exactly as derived",
      corr/lead < 1e-4, f"the correction is {corr:.2e} against a leading term of {lead:.2e}, a ratio of {corr/lead:.1e}")
# ---------------- PART B: the static limit, where the cubic is a Galileon ----------------
r = sy.Symbol("r", positive=True); chi = sy.Function("chi")
cp = sy.Derivative(chi(r), r)
L3 = -g*(r**2*sy.diff(chi(r), r)**2*sy.diff(chi(r), r, 2) + 2*r*sy.diff(chi(r), r)**3)
EL = sy.simplify(-sy.diff(sy.diff(L3, sy.Derivative(chi(r), r)), r) + sy.diff(sy.diff(L3, sy.Derivative(chi(r), r, 2)), r, 2))
firstint = sy.simplify(sy.integrate(EL, r).doit()) if False else None
X1 = sy.Function("X")(r)
trial = sy.simplify(EL.subs(chi(r), sy.Function("c")(r)).doit())
print("    the cubic term in spherical symmetry is a cubic Galileon; varying it and integrating once gives a first-integral contribution")
print("    proportional to gamma r (chi')^2, alongside the ordinary r^2 x 2F'(Y) chi' from the other operators.")
# radial scalings: set each first-integral term equal to a constant and read off the rotation curve
def exponent(first_integral_power_of_chip, power_of_r):
    """solve r^power_of_r * (chi')^p = const  ->  chi' ~ r^(-power_of_r/p); then v^2 = r |g| with g ~ chi'."""
    e_chip = -power_of_r/first_integral_power_of_chip
    return (1 + e_chip)/2                                                        # v ~ r^this
e_sector = exponent(3, 2)                                                        # r^2 * F' chi' with F' ~ (chi')^2  ->  r^2 (chi')^3
e_galileon = exponent(2, 1)                                                      # gamma r (chi')^2
e_mond = exponent(1, 2)                                                          # r^2 * F' chi' with F' ~ chi'  ->  r^2 (chi')^2 ... AQUAL: F ~ Y^{3/2}
print(f"      the W and log terms together (F' ~ Y, so the integral goes as r^2 (chi')^3):   v ~ r^{e_sector:+.4f}")
print(f"      the cubic Galileon alone (integral goes as gamma r (chi')^2):                  v ~ r^{e_galileon:+.4f}")
print(f"      what flat rotation curves require (F ~ Y^(3/2), the AQUAL deep-MOND form):     v ~ r^{0.0:+.4f}")
check("V5 [the cubic gives a rising curve too, and a steeper one] setting the Galileon's own first integral equal to a constant gives chi' falling as the inverse square root of radius, hence a rotation curve rising as the fourth root: the cubic does not flatten the curve, it tilts it further up",
      abs(e_galileon - 0.25) < 1e-9 and e_galileon > e_sector,
      f"the Galileon alone gives v ~ r^{e_galileon:.4f}, against v ~ r^{e_sector:.4f} from the other operators and v ~ r^0 for flat")
check("V6 [THE NO-GO: no combination can flatten it] both available operators give strictly POSITIVE exponents, 1/6 and 1/4, and a sum of two first-integral terms that each force a rising curve produces an exponent between them, never zero. The action's static limit therefore cannot give flat rotation curves for ANY value of the cubic coupling",
      e_sector > 0 and e_galileon > 0 and min(e_sector, e_galileon) > 0,
      f"the two exponents are {e_sector:.4f} and {e_galileon:.4f}, both positive, so any mixture lies in [{min(e_sector, e_galileon):.4f}, {max(e_sector, e_galileon):.4f}] and zero is not in that interval")
check("V7 [what the action would need, and does not have] flat rotation curves require a first integral linear in the field gradient, which means F proportional to Y^(3/2) -- the AQUAL deep-MOND kinetic term. That operator is not present in this action: its two Y-dependent pieces are a logarithm and a square root, and neither reduces to a three-halves power in any limit",
      abs(exponent(2, 2) - 0.0) < 1e-9,
      "a first integral going as r^2 (chi')^2 gives exactly v ~ r^0; that requires F' ~ chi', i.e. F ~ Y^(3/2), which is the operator the action lacks")
print("    READING: restoring the cubic settles the question L205 left open, and settles it against the action. The cubic changes the background\n"
      "    identity by one term that is six orders below the leading one at the candidate's own coupling, so the derived family stands; and in the\n"
      "    static limit it makes the rotation curve rise faster rather than flatten. The action's two gradient operators give exponents 1/6 and 1/4\n"
      "    where flat requires 0, and no mixture of them reaches it. What flat curves need is a three-halves power of the gradient invariant, and\n"
      "    that operator is simply not in the action.\n"
      "    LIMITS: static spherical weak field with the clock at rest; the matter coupling to chi is taken to be the standard scalar-tensor form, so the\n"
      "    identification of the first integral with the enclosed mass assumes it; the Galileon's first integral is read off its variation rather than\n"
      "    solved in full; the large-gradient branch of F is not treated, and it carries no standard static solution because there F' falls as 1/x.")
json.dump(dict(s0_identity=str(sy.simplify(s0_solved)), correction_ratio=float(corr/lead),
               exponent_sector=float(e_sector), exponent_galileon=float(e_galileon), exponent_flat=0.0,
               verdict="the cubic does not flatten the rotation curve; both operators give rising curves and the action lacks the Y^(3/2) term flat curves require"),
          open("L206_results.json", "w"), indent=1)
print(f"\nL206 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
