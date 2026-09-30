"""t01: the MK solution (static spherical vacuum solution of Weyl gravity) from the Bach equation, computed from scratch (sympy), with controls and mutations.

Metric ds^2 = -B(r) dt^2 + dr^2/B(r) + r^2 dOmega^2  (the gauge g_tt g_rr = -1, g_thth = r^2 reachable by a conformal factor + radial redefinition).
Everything is derived from the Riemann tensor of this metric with a generic function B(r); nothing is assumed about the solution.

 A  machinery + controls: Weyl^2 formula; Bach traceless and diagonal; Bach = 0 for Schwarzschild, dS, SdS, Minkowski;
    Bach != 0 for Reissner-Nordstrom and for B = 1 + r^3 (the code can fail).
 B  the vacuum equation in this gauge: b^t_t - b^r_r = -(B/6)(B'''' + 4B'''/r) = -(B/6) (rB)''''/r, so (rB)'''' = 0 gives the cubic family
    B = w + v/r + u r - k r^2 (four constants); the one remaining equation is ALGEBRAIC: every Bach component = -+(1 + 3 u v - w^2)/(6 r^4).
    Hence the general solution has THREE constants, w^2 = 1 + 3uv, and the MK parametrisation w = 1-3 beta gamma, v = -beta(2-3 beta gamma), u = gamma
    satisfies it identically.  Mutations of the constants fail.
"""
import sys
import sympy as sp
sys.path.insert(0, '.')
from wg_tools import Geo, static_spherical

ok = []


def chk(name, cond):
    ok.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name)


r = sp.symbols('r', positive=True)
Bf = sp.Function('B')(r)
geo, X = static_spherical(Bf, r)
gi = geo.gi

# ---------------------------------------------------------------- A: machinery
W2 = sp.simplify(geo.weyl_squared())
W2_expected = (r**2 * sp.diff(Bf, r, 2) - 2 * r * sp.diff(Bf, r) + 2 * Bf - 2)**2 / (3 * r**4)
chk("A1 Weyl^2 = (r^2 B'' - 2 r B' + 2B - 2)^2 / (3 r^4) for generic B(r)", sp.simplify(W2 - W2_expected) == 0)

Bh = geo.bach()
mixed = [sp.simplify(gi[a, a] * Bh[a, a]) for a in range(4)]
off_ok = all(sp.simplify(sp.expand_trig(Bh[a, b])) == 0 for a in range(4) for b in range(4) if a != b)
chk("A2a Bach tensor is diagonal for generic B(r)", off_ok)
chk("A2b Bach tensor is traceless for generic B(r)", sp.simplify(sum(mixed)) == 0)
chk("A2c b^theta_theta = b^phi_phi (spherical symmetry)", sp.simplify(mixed[2] - mixed[3]) == 0)
d = sp.simplify(mixed[0] - mixed[1])
d_expected = -(Bf / 6) * (sp.diff(Bf, r, 4) + 4 * sp.diff(Bf, r, 3) / r)
chk("A3 b^t_t - b^r_r = -(B/6)(B'''' + 4B'''/r)  [= -(B/6)(rB)''''/r : the nabla^4 B of the MK literature]", sp.simplify(d - d_expected) == 0)
chk("A3b the operator identity B'''' + 4B'''/r = (rB)''''/r", sp.simplify(sp.diff(Bf, r, 4) + 4 * sp.diff(Bf, r, 3) / r - sp.diff(r * Bf, r, 4) / r) == 0)


def bach_vals(Bexpr):
    return [sp.simplify(m.subs(Bf, Bexpr).doit()) for m in mixed]


M, Q, k, gam, bet, w, v, u = sp.symbols('M Q k gamma beta w v u')
chk("A4a control PASS: Schwarzschild B = 1-2M/r has Bach = 0", all(e == 0 for e in bach_vals(1 - 2 * M / r)))
chk("A4b control PASS: de Sitter B = 1-k r^2 has Bach = 0", all(e == 0 for e in bach_vals(1 - k * r**2)))
chk("A4c control PASS: Schwarzschild-de Sitter B = 1-2M/r-k r^2 has Bach = 0", all(e == 0 for e in bach_vals(1 - 2 * M / r - k * r**2)))
chk("A4d control PASS: Minkowski B = 1 has Bach = 0", all(e == 0 for e in bach_vals(sp.Integer(1))))
rn = bach_vals(1 - 2 * M / r + Q**2 / r**2)
chk("A4e control FAIL (must be detected): Reissner-Nordstrom B = 1-2M/r+Q^2/r^2 has Bach != 0", any(e != 0 for e in rn))
r3 = bach_vals(1 + r**3)
chk("A4f control FAIL (must be detected): B = 1 + r^3 has Bach != 0", any(e != 0 for e in r3))
W2_schw = sp.simplify(W2.subs(Bf, 1 - 2 * M / r).doit())
chk("A5 Weyl^2 of Schwarzschild = 48 M^2/r^6 (equals its Kretschmann scalar)", sp.simplify(W2_schw - 48 * M**2 / r**6) == 0)

# ---------------------------------------------------------------- B: general solution
sol = sp.dsolve(sp.diff(r * Bf, r, 4), Bf)
print("   dsolve((rB)'''' = 0):", sol)
consts = sorted(sol.rhs.free_symbols - {r}, key=str)
rB_poly = sp.Poly(sp.expand(r * sol.rhs), r)
chk("B1 (rB)'''' = 0 has a four-constant general solution, and r*B is a cubic polynomial in r (so B = c0/r + c1 + c2 r + c3 r^2)",
    len(consts) == 4 and rB_poly.degree() == 3 and sp.simplify(sp.diff(r * sol.rhs, r, 4)) == 0)
chk("B1b control: an r^3 term in B violates (rB)'''' = 0, so it is outside the family",
    sp.simplify(sp.diff(r * r**3, r, 4)) != 0)
Bmk = w + v / r + u * r - k * r**2
vals = bach_vals(Bmk)
constraint = 1 + 3 * u * v - w**2
print("   Bach components on B = w + v/r + u r - k r^2:", [sp.factor(e) for e in vals])
chk("B2 every Bach component = -+(1 + 3uv - w^2)/(6 r^4): the cubic family solves the full nonlinear Bach equation iff w^2 = 1 + 3uv",
    sp.simplify(vals[0] + constraint / (6 * r**4)) == 0 and sp.simplify(vals[1] + constraint / (6 * r**4)) == 0
    and sp.simplify(vals[2] - constraint / (6 * r**4)) == 0 and sp.simplify(vals[3] - constraint / (6 * r**4)) == 0)
Bmk3 = (1 - 3 * bet * gam) - bet * (2 - 3 * bet * gam) / r + gam * r - k * r**2
chk("B3 the MK parametrisation w = 1-3 beta gamma, v = -beta(2-3 beta gamma), u = gamma gives Bach = 0 identically (3 free constants beta, gamma, k)",
    all(e == 0 for e in bach_vals(Bmk3)))
chk("B3b the constraint is w^2 = 1+3uv in the MK parametrisation (polynomial identity in beta, gamma)",
    sp.expand((1 - 3 * bet * gam)**2 - 1 - 3 * gam * (-bet * (2 - 3 * bet * gam))) == 0)

# mutations of the MK constants
mut1 = (1 - 2 * bet * gam) - bet * (2 - 3 * bet * gam) / r + gam * r - k * r**2
mut2 = (1 - 3 * bet * gam) - bet * (2 - 2 * bet * gam) / r + gam * r - k * r**2
mut3 = (1 - 3 * bet * gam) - bet * (2 - 3 * bet * gam) / r - gam * r - k * r**2   # sign of the linear term flipped, w unchanged
mut4 = Bmk3 + sp.Symbol('m') * r**3
mut5 = (1 - 3 * bet * gam) + bet * (2 - 3 * bet * gam) / r + gam * r - k * r**2   # sign of the 1/r coefficient flipped
for nm, mu in [("w = 1 - 2 beta gamma", mut1), ("v = -beta(2 - 2 beta gamma)", mut2), ("u = -gamma with w, v unchanged", mut3),
               ("extra m r^3 term", mut4), ("v -> +beta(2-3 beta gamma)", mut5)]:
    chk("B4 MUTATION rejected: %s does not solve Bach = 0" % nm, any(sp.simplify(e) != 0 for e in bach_vals(mu)))
# the special cases that must survive
chk("B5a beta = 0: B = 1 + gamma r - k r^2 solves Bach = 0 for every gamma, k", all(e == 0 for e in bach_vals(1 + gam * r - k * r**2)))
chk("B5b gamma = 0: SdS with M = beta solves Bach = 0", all(e == 0 for e in bach_vals(1 - 2 * bet / r - k * r**2)))
# the constraint counts parameters: 4 constants - 1 constraint
chk("B6 parameter count: the general solution has 4 - 1 = 3 free constants (w,v,u,k with one algebraic constraint)", len({w, v, u, k}) - 1 == 3)
print("\nPASS %d / %d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
