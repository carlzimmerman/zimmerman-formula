"""t02: the conformal (special-conformal) map that shifts the MK constants, and which combinations of (beta, gamma, k) are invariant.

The gauge form ds^2 = -B dt^2 + dr^2/B + r^2 dOmega^2 is preserved by a 1-parameter family of conformal maps (a 'special conformal
transformation' acting on 1/r as the shift x = 1/r -> x + a):
      r' = r/(1 + a r),   g' = Omega^2 g,   Omega = 1/(1 + a r)   <=>   B'(r') = (1 - a r')^2 B( r'/(1 - a r') ).
 A  kinematics: the map preserves the gauge form for generic B(r) (explicit Jacobian pull-back of the metric, not the formula).
 B  action on B = w + v/r + u r - k r^2:  w' = w - 3 a v,  v' = v,  u' = u - 2 a w + 3 a^2 v,  k' = k - a^2 w + a^3 v + a u.
    Invariants: v ; H = w^2 - 3uv (the MK constraint H = 1 is therefore conformally invariant) ; the discriminant of the cubic
    p(x) = v x^3 + w x^2 + u x - k (x = 1/r, and p'(x') = p(x) shifts x by a).  Non-invariants: u, k, w, u^2/k, u^2 - 4k, u^2 + k.
    Group law T_a2 T_a1 = T_(a1+a2).  The Weyl^2 transforms as Omega^-4.  Bach transforms as Omega^-4 (checked on a NON-solution).
 C  beta = 0 (w = 1, v = 0): B = 1 + gamma r - k r^2 has vanishing Weyl tensor for every (gamma, k); (gamma, k) -> (gamma - 2a, k + a gamma - a^2);
    the invariant is gamma^2 + 4k = 4 kappa_h^2 (kappa_h = surface gravity of the horizon with t normalised by B(0) = 1); the metric divided by
    r^2 is AdS2 x S^2 (unit radii) with a Delta-dependent Killing time.  Mutation: unequal radii is NOT conformally flat.
 D  every MK solution is the image of a Schwarzschild-de Sitter metric: a* = (w-1)/(3v) gives u' = 0, w' = 1, and
    k' = k + gamma^2 (1 - beta gamma)/(2 - 3 beta gamma)^2 ; the cubic discriminant equals 4 k'(1 - 27 M'^2 k') with 2M' = -v.
 E  the static metric with (gamma, k) is conformal to a Robertson-Walker metric of 3-curvature K = -(gamma^2/4 + k): checked by explicit substitution.
Mutations: a wrong map (r' = r/(1 + a r^2)) breaks the gauge form; wrong 'invariants' are not invariant.
"""
import sys
import sympy as sp
sys.path.insert(0, '.')
from wg_tools import Geo, static_spherical

ok = []


def chk(name, cond):
    ok.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name)


r, rp, a = sp.symbols('r rp a', real=True)
w, v, u, k = sp.symbols('w v u k', real=True)
gam, bet = sp.symbols('gamma beta', real=True)
t, th, ph = sp.symbols('t theta phi')

# ---------------------------------------------------------------- A: kinematics with generic B, by explicit Jacobian
Bg = sp.Function('B')
# old coords (t, r, th, ph); new coords (t, rp, th, ph) with r = rp/(1 - a rp), Omega = 1 - a rp  (= 1/(1 + a r))
r_of_rp = rp / (1 - a * rp)
Om = 1 - a * rp
g_old = sp.diag(-Bg(r_of_rp), 1 / Bg(r_of_rp), r_of_rp**2, r_of_rp**2 * sp.sin(th)**2)   # already evaluated at r(rp)
Jr = sp.diff(r_of_rp, rp)
# pulled-back metric components in new coordinates, times Omega^2:  only the rr component picks up Jr^2
g_new_tt = sp.simplify(Om**2 * g_old[0, 0])
g_new_rr = sp.simplify(Om**2 * g_old[1, 1] * Jr**2)
g_new_thth = sp.simplify(Om**2 * g_old[2, 2])
Btilde = sp.simplify(Om**2 * Bg(r_of_rp))
chk("A1 g'_tt = -B~(r') with B~(r') = (1 - a r')^2 B(r'/(1 - a r'))", sp.simplify(g_new_tt + Btilde) == 0)
chk("A2 g'_r'r' = 1/B~(r')  (the gauge g_tt g_rr = -1 is preserved)", sp.simplify(g_new_rr - 1 / Btilde) == 0)
chk("A3 g'_thth = r'^2  (areal-radius gauge preserved)", sp.simplify(g_new_thth - rp**2) == 0)
# MUTATION: wrong map r' = r/(1 + a r^2) with Omega = r'/r
Om_bad = 1 / (1 + a * r**2)          # r'/r for the wrong map
rp_bad = r / (1 + a * r**2)
Jbad = sp.diff(rp_bad, r)
gtt_bad = Om_bad**2 * (-Bg(r))
grr_bad = Om_bad**2 / Bg(r) * (1 / Jbad**2)        # Omega^2 g_rr (dr/dr')^2
prod = sp.simplify(gtt_bad * grr_bad)
chk("A4 MUTATION rejected: the map r' = r/(1 + a r^2) does NOT preserve g_tt g_rr = -1 (product != -1 for generic B)", sp.simplify(prod + 1) != 0)

# ---------------------------------------------------------------- B: action on the cubic family
Bmk = lambda rr, w_, v_, u_, k_: w_ + v_ / rr + u_ * rr - k_ * rr**2
Bt = sp.expand(sp.simplify((1 - a * rp)**2 * Bmk(rp / (1 - a * rp), w, v, u, k)))
Bt_poly = sp.expand(Bt * rp)   # multiply by rp to get a polynomial
coeffs = sp.Poly(Bt_poly, rp).all_coeffs()[::-1]      # coefficient list of rp^0 .. rp^3
w2, v2, u2, k2 = coeffs[1], coeffs[0], coeffs[2], -coeffs[3]
chk("B1 transformed constants: w' = w - 3 a v", sp.expand(w2 - (w - 3 * a * v)) == 0)
chk("B2 transformed constants: v' = v", sp.expand(v2 - v) == 0)
chk("B3 transformed constants: u' = u - 2 a w + 3 a^2 v", sp.expand(u2 - (u - 2 * a * w + 3 * a**2 * v)) == 0)
chk("B4 transformed constants: k' = k - a^2 w + a^3 v + a u", sp.expand(k2 - (k - a**2 * w + a**3 * v + a * u)) == 0)
T = lambda a_, W, V, U, K: (W - 3 * a_ * V, V, U - 2 * a_ * W + 3 * a_**2 * V, K - a_**2 * W + a_**3 * V + a_ * U)
a1, a2 = sp.symbols('a1 a2', real=True)
comp = T(a2, *T(a1, w, v, u, k))
direct = T(a1 + a2, w, v, u, k)
chk("B5 group law: T_a2 o T_a1 = T_(a1 + a2)", all(sp.expand(x - y) == 0 for x, y in zip(comp, direct)))

H_inv = lambda W, V, U, K: W**2 - 3 * U * V
def disc3(W, V, U, K):     # discriminant of V x^3 + W x^2 + U x - K
    A_, B_, C_, D_ = V, W, U, -K
    return B_**2 * C_**2 - 4 * A_ * C_**3 - 4 * B_**3 * D_ - 27 * A_**2 * D_**2 + 18 * A_ * B_ * C_ * D_
wp, vp, up, kp = T(a, w, v, u, k)
chk("B6 invariant: v' = v", sp.expand(vp - v) == 0)
chk("B7 invariant: w'^2 - 3 u' v' = w^2 - 3 u v  (so the MK constraint w^2 - 3uv = 1 is conformally invariant)", sp.expand(H_inv(wp, vp, up, kp) - H_inv(w, v, u, k)) == 0)
chk("B8 invariant: discriminant of the cubic v x^3 + w x^2 + u x - k", sp.expand(disc3(wp, vp, up, kp) - disc3(w, v, u, k)) == 0)
# non-invariants (controls that must FAIL to be invariant)
for nm, f in [("u", lambda W, V, U, K: U), ("k", lambda W, V, U, K: K), ("w", lambda W, V, U, K: W),
              ("u^2/k  (a0^2/k)", lambda W, V, U, K: U**2 / K), ("u^2 - 4k", lambda W, V, U, K: U**2 - 4 * K),
              ("u^2 + k", lambda W, V, U, K: U**2 + K), ("u^2 + 2k (evaluated on the beta=0 slice)", lambda W, V, U, K: U**2 + 2 * K)]:
    d_ = sp.simplify(f(wp, vp, up, kp) - f(w, v, u, k))
    if 'beta=0' in nm:
        d_ = sp.simplify(d_.subs({w: 1, v: 0}))
    chk("B9 CONTROL: %s is NOT invariant under the map" % nm, d_ != 0)

# explicit-metric check that the polynomial family maps to the polynomial family: B~ formula equals (1-a r')^2 B(r'/(1-a r'))
chk("B10 the map takes the cubic family to the cubic family (B~ has exactly the 4 monomials rp^-1..rp^2; no others)",
    sp.Poly(Bt_poly, rp).degree() == 3 and len(sp.Poly(Bt_poly, rp).all_coeffs()) == 4)

# Weyl^2 and Bach transform as Omega^-4 (Bach checked on a NON-solution to make the check non-vacuous)
def weyl2_formula(Bexpr, rr):
    return (rr**2 * sp.diff(Bexpr, rr, 2) - 2 * rr * sp.diff(Bexpr, rr) + 2 * Bexpr - 2)**2 / (3 * rr**4)
lhs = sp.simplify(weyl2_formula(Bt, rp))
Bold = Bmk(r_of_rp, w, v, u, k)
# C^2[B~](r') = Omega^-4 C^2[B](r(r'))
rhs = sp.simplify(Om**-4 * weyl2_formula(Bmk(r, w, v, u, k), r).subs(r, r_of_rp))
chk("B11 Weyl^2 transforms as Omega^-4 under the map (formula for Weyl^2; verified against the Riemann tensor in t01)", sp.simplify(lhs - rhs) == 0)

# Bach covariance with the full curvature code on a NON-solution B = 1 + c r^3
c3 = sp.symbols('c3', real=True)
rr_pos = sp.symbols('rr', positive=True)
geo1, _ = static_spherical(1 + c3 * rr_pos**3, rr_pos)
Bh1 = geo1.bach(); gi1 = geo1.gi
mix1 = [sp.simplify(gi1[i, i] * Bh1[i, i]) for i in range(4)]
Bnon_new = sp.simplify((1 - a * rr_pos)**2 * (1 + c3 * (rr_pos / (1 - a * rr_pos))**3))
geo2, _ = static_spherical(Bnon_new, rr_pos)
Bh2 = geo2.bach(); gi2 = geo2.gi
mix2 = [sp.simplify(gi2[i, i] * Bh2[i, i]) for i in range(4)]
Om_r = 1 - a * rr_pos            # Omega evaluated at r' = rr
r_old = rr_pos / (1 - a * rr_pos)
cov_ok = all(sp.simplify(mix2[i] - Om_r**-4 * mix1[i].subs(rr_pos, r_old)) == 0 for i in range(4))
nonzero = any(sp.simplify(m) != 0 for m in mix1)
chk("B12 the Bach code is conformally covariant: b~^a_b(r') = Omega^-4 b^a_b(r) for a NON-solution (B = 1 + c r^3)", cov_ok and nonzero)
mut_cov = all(sp.simplify(mix2[i] - Om_r**-2 * mix1[i].subs(rr_pos, r_old)) == 0 for i in range(4))
chk("B13 MUTATION rejected: with the wrong weight Omega^-2 the covariance check fails", not mut_cov)

# ---------------------------------------------------------------- C: beta = 0 slice
gs, ks = sp.symbols('gamma k', real=True)
rpos = sp.symbols('rpos', positive=True)
geoC, _ = static_spherical(1 + gs * rpos - ks * rpos**2, rpos)
chk("C1 beta = 0: B = 1 + gamma r - k r^2 has vanishing Weyl tensor (all 256 components) for symbolic gamma, k: conformally flat",
    geoC.weyl_is_zero())
geoBad, _ = static_spherical(1 + gs * rpos - ks * rpos**2 + sp.Symbol('m') / rpos, rpos)
chk("C1b control: adding a mass term v/r breaks conformal flatness", not geoBad.weyl_is_zero())
gp = gs - 2 * a
kp_ = ks + a * gs - a**2
Delta = gs**2 + 4 * ks
chk("C2 on the beta = 0 slice the map is gamma' = gamma - 2a, k' = k + a gamma - a^2 (from B1-B4 with w = 1, v = 0)",
    sp.expand(up.subs({w: 1, v: 0, u: gs, k: ks}) - gp) == 0 and sp.expand(kp.subs({w: 1, v: 0, u: gs, k: ks}) - kp_) == 0)
chk("C3 invariant: gamma^2 + 4k  (the discriminant of the quadratic 1 + gamma r - k r^2)", sp.expand(gp**2 + 4 * kp_ - Delta) == 0)
chk("C3b CONTROL: gamma^2 - 4k and gamma^2 + k are not invariant", sp.expand(gp**2 - 4 * kp_ - (gs**2 - 4 * ks)) != 0 and sp.expand(gp**2 + kp_ - (gs**2 + ks)) != 0)
# horizon surface gravity with t normalised by B(0) = 1
rplus = (gs + sp.sqrt(Delta)) / (2 * ks)
Bfun = lambda x: 1 + gs * x - ks * x**2
kappa_h = sp.simplify(sp.Abs(sp.diff(Bfun(r), r).subs(r, rplus)) / 2)
kh_sq = sp.simplify(sp.diff(Bfun(r), r).subs(r, rplus)**2 / 4)
chk("C4 surface gravity of the horizon at r_+ = (gamma + sqrt(gamma^2+4k))/(2k): kappa_h^2 = (gamma^2 + 4k)/4 = (gamma/2)^2 + k",
    sp.simplify(kh_sq - Delta / 4) == 0)
chk("C4b pure de Sitter (gamma = 0, k = H^2): kappa_h^2 = H^2", sp.simplify(kh_sq.subs(gs, 0) - ks) == 0)
# the metric / r^2 is AdS2 x S^2 with unit radii: y = 1/r + gamma/2, f = y^2 - Delta/4
y, tt2 = sp.symbols('y tt2', real=True)
f = y**2 - Delta / 4
# check g/r^2 = -f dt^2 + dy^2/f + dOmega^2 by direct substitution r = 1/(y - gamma/2)
r_of_y = 1 / (y - gs / 2)
Bval = Bfun(r_of_y)
chk("C5a g_tt / r^2 = -(y^2 - Delta/4)", sp.simplify(Bval / r_of_y**2 - f) == 0)
drdy = sp.diff(r_of_y, y)
chk("C5b g_rr (dr/dy)^2 / r^2 = 1/(y^2 - Delta/4)", sp.simplify((drdy**2 / Bval) / r_of_y**2 - 1 / f) == 0)
# Weyl tensor of AdS2 x S^2: equal radii -> 0 ; unequal -> nonzero
ya, ta, thh, phh, L2 = sp.symbols('ya ta thh phh L2', positive=True)
geoP = Geo((ta, ya, thh, phh), [-(ya**2 - 1), 1 / (ya**2 - 1), sp.Integer(1), sp.sin(thh)**2])
chk("C6 AdS2 (unit radius) x S^2 (unit radius) is conformally flat (Weyl = 0)", geoP.weyl_is_zero())
geoQ = Geo((ta, ya, thh, phh), [-(ya**2 - 1), 1 / (ya**2 - 1), L2, L2 * sp.sin(thh)**2])
chk("C6b CONTROL: AdS2 x S^2 with S^2 radius^2 = L2 != 1 is NOT conformally flat", not geoQ.weyl_is_zero() and all(sp.simplify(x.subs(L2, 1)) == 0 for x in geoQ.C.values()))

# the invariant as an sl(2,R) Casimir-type quantity of the time-translation generator on the AdS2 factor:  (f'/2)^2 - f = Delta/4 for every y
chk("C7 for the Killing vector d/dt of AdS2 with f = y^2 - Delta/4: (f'/2)^2 - f = Delta/4 = kappa_h^2 for all y (a constant, the twist^2 - norm^2 Casimir-type invariant; hyperbolic for Delta > 0)",
    sp.simplify((sp.diff(f, y) / 2)**2 - f - Delta / 4) == 0)
chk("C7b CONTROL: the combination (f'/2)^2 + f is NOT constant in y", sp.simplify(sp.diff((sp.diff(f, y) / 2)**2 + f, y)) != 0)

# ---------------------------------------------------------------- D: every MK solution is the image of SdS
w_mk = 1 - 3 * bet * gam
v_mk = -bet * (2 - 3 * bet * gam)
u_mk = gam
a_star = sp.simplify((w_mk - 1) / (3 * v_mk))
chk("D1 a* = (w-1)/(3v) = gamma/(2 - 3 beta gamma)", sp.simplify(a_star - gam / (2 - 3 * bet * gam)) == 0)
ws, vs, us, ks_ = T(a_star, w_mk, v_mk, u_mk, ks)
chk("D2 at a* the linear term vanishes (u' = 0) and w' = 1: the image is Schwarzschild-de Sitter", sp.simplify(us) == 0 and sp.simplify(ws - 1) == 0)
chk("D3 k' = k + gamma^2 (1 - beta gamma)/(2 - 3 beta gamma)^2  (the SdS 'Lambda/3' of the conformal class)",
    sp.simplify(ks_ - (ks + gam**2 * (1 - bet * gam) / (2 - 3 * bet * gam)**2)) == 0)
Mp = -vs / 2
D3 = sp.simplify(disc3(w_mk, v_mk, u_mk, ks))
chk("D4 the invariant discriminant equals 4 k'(1 - 27 M'^2 k') (the SdS Nariai discriminant) with M' = beta (2 - 3 beta gamma)/2",
    sp.simplify(D3 - 4 * ks_ * (1 - 27 * Mp**2 * ks_)) == 0 and sp.simplify(Mp - bet * (2 - 3 * bet * gam) / 2) == 0)
disc_a = sp.expand(sp.discriminant(sp.expand(up), a))
chk("D5a u'(a) = u - 2 a w + 3 a^2 v is a quadratic in a with discriminant 4 (w^2 - 3 u v)", sp.expand(disc_a - 4 * (w**2 - 3 * u * v)) == 0)
chk("D5b for every MK solution w^2 - 3uv = 1, so the discriminant is 4 > 0: the linear term is removable by a real map for ALL beta, gamma",
    sp.simplify(disc_a.subs({w: w_mk, v: v_mk, u: u_mk})) == 4)
chk("D6 beta -> 0 limit: k' -> k + gamma^2/4  (the (gamma/2)^2 + k sum rule of section C)", sp.simplify(sp.limit(ks_, bet, 0) - (ks + gam**2 / 4)) == 0)

# ---------------------------------------------------------------- E: the Robertson-Walker (Hubble-flow) frame
rho = sp.symbols('rho', positive=True)
g_, k_ = sp.symbols('gamma_ k_', real=True)
den = (1 - g_ * rho / 4)**2 + k_ * rho**2 / 4
r_of_rho = rho / den
F = (1 - (g_**2 / 16 + k_ / 4) * rho**2) / den
Bsub = 1 + g_ * r_of_rho - k_ * r_of_rho**2
Kcur = -(g_**2 / 4 + k_)
iso = (1 + Kcur * rho**2 / 4)
chk("E1 B(r(rho)) = F^2  (time-time part of the static metric = (1/R^2) F^2 (-d tau^2) with dt = d tau/R)", sp.simplify(Bsub - F**2) == 0)
chk("E2 r^2 = F^2 rho^2/(1 + K rho^2/4)^2 with K = -(gamma^2/4 + k)  (angular part of an isotropic RW metric of 3-curvature K)",
    sp.simplify(r_of_rho**2 - F**2 * rho**2 / iso**2) == 0)
chk("E3 (dr/d rho)^2/B = F^2/(1 + K rho^2/4)^2  (radial part)", sp.simplify(sp.diff(r_of_rho, rho)**2 / Bsub - F**2 / iso**2) == 0)
Kbad = -(g_**2 / 4 - k_)
isob = (1 + Kbad * rho**2 / 4)
chk("E4 MUTATION rejected: K = -(gamma^2/4 - k) fails the angular-part identity", sp.simplify(r_of_rho**2 - F**2 * rho**2 / isob**2) != 0)
chk("E5 K depends on (gamma, k) only through gamma^2 + 4k: -4K = gamma^2 + 4k is exactly the invariant of section C", sp.simplify(-4 * Kcur - (g_**2 + 4 * k_)) == 0)
chk("E6 the CG papers' k_static = 0 choice: K = -gamma0^2/4, i.e. gamma0/2 = sqrt(-K)", sp.simplify(Kcur.subs(k_, 0) + g_**2 / 4) == 0)

print("\nPASS %d / %d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
