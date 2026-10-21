#!/usr/bin/env python3
"""Coordinator's 'no cosmic aether' theorem for the round-2 action.

This is the prerequisite for the preferred-frame PPN parameters alpha1, alpha2 to
vanish at O(1): if the P field has no cosmological background value, there is no
Lorentz-violating VEV for the Solar System to move through.

Action terms that involve P on a homogeneous background:

    W(u) = (a0^2/K)[ -u/a0 - log(1 - u/a0) ],     u = K|P|
    + P^i D_i log N                               (clock; vanishes when N = 1)
    + (eta/2) E_i E^i,  -(gamma/2)(D_i P^i)^2,  -(gamma/4) F_ij F^ij
                                                  (all vanish for homogeneous P)

Claim: on FRW (N = 1, P homogeneous) the unique solution of the P equation is P = 0.
Proof: every derivative operator vanishes identically, so the equation reduces to
dW/du = 0, and dW/du = (u/K)/(1 - u/a0) has its only zero at u = 0.

Run: python3 a22_no_cosmic_aether.py [--mutate]
"""
import sys
import sympy as sp

MUTATE = "--mutate" in sys.argv
u, a0, K = sp.symbols("u a_0 K", positive=True)
res = []


def check(cid, ok, val, thr, note=""):
    ok = bool(ok)
    res.append(ok)
    print(f"{cid} {'PASS' if ok else 'FAIL'} measured={val} threshold={thr} {note}")


W = (a0**2 / K) * (-u / a0 - sp.log(1 - u / a0))
dW = sp.simplify(sp.diff(W, u))
print("dW/du =", dW)
check("K1", sp.simplify(dW - (u / K) / (1 - u / a0)) == 0, dW, "(u/K)/(1-u/a0)",
      "the P equation's only homogeneous term is dW/du")

# NB: u is declared positive, so solve() would exclude 0 by assumption.  Zero the
# numerator instead -- that is the actual statement.
u2 = sp.Symbol("u2")                      # unconstrained
num = sp.numer(sp.together(dW.subs(u, u2)))
sols = sp.solve(sp.Eq(num, 0), u2)
print("numerator:", num, " zeros:", sols)
check("K2", sols == [0], sols, "[0]",
      "dW/du vanishes only at u = 0 -> homogeneous P must vanish")

# the clock source on FRW
N = sp.Integer(1)
check("K3", sp.simplify(sp.diff(sp.log(N), sp.Symbol("x"))) == 0, 0, "0",
      "P^i D_i log N = 0 on FRW: no source that could switch P on")

# a VEV would need W'(u)=0 at u>0, i.e. a second minimum.  Show there is none.
check("K4", sp.simplify(sp.diff(dW, u)).subs(u, 0) > 0, sp.simplify(sp.diff(dW, u).subs(u, 0)),
      "> 0", "W is strictly increasing away from u=0: no symmetry-breaking minimum")

if MUTATE:
    # a Proca mass term m^2 P^2 would allow P=0 but not force it, and a negative
    # mass^2 would give a VEV.  Demonstrate the VEV that a tachyonic mass produces.
    m2 = -sp.Rational(1, 10)
    Wt = W + m2 * u**2 / (2 * K**2)
    sols2 = sp.solve(sp.Eq(sp.together(sp.diff(Wt, u)), 0), u)
    print("with tachyonic mass, zeros:", sols2)
    check("MUT", len(sols2) > 1, sols2, "more than one zero",
          "a tachyonic mass would create a VEV -> alpha2 != 0; the action has none")

print(f"\nA22-AETHER {'COMPLETE' if all(res) else 'INCOMPLETE'}: {sum(res)}/{len(res)}")
print("SCOPE: this closes the VEV route to alpha1/alpha2.  The (1+beta)theta^2")
print("deformation is a separate route and is NOT closed here -- it is A22's job.")
sys.exit(0 if all(res) else 1)
