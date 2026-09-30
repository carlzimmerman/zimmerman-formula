"""t03: the compensator-scalar sector of Weyl gravity: what fixes the frame, G_eff, the Lambda-like constant, and whether a0^2/k or G_eff rho/a0^2 is fixed.

Matter action of Weyl gravity (mostly-plus, standard signs): L_phi = -1/2 (grad phi)^2 - (1/12) R phi^2 - lambda phi^4  (conformal coupling xi = 1/6, potential V = lambda phi^4),
    EOM:  E = box phi - R phi/6 - 4 lambda phi^3 = 0
    T_mn = d_m phi d_n phi - g_mn (grad phi)^2/2 + (1/6)(g_mn box - nabla_m nabla_n + G_mn) phi^2 - g_mn lambda phi^4,   trace identity  T^m_m = phi E.
The Weyl action contributes 4 alpha_g W_mn (Bach, zero on every conformally-Einstein metric); the full vacuum equation is Bach + T_phi = 0, so T_phi = 0 outside the sources.

 A  controls: trace identity T^m_m = phi E for generic metric function and generic phi(r) (implementation + sign check); a non-conformal coupling breaks it.
 B  MK metric with the profile phi = phi0/(1 + r/a): T_mn = 0 for ALL components iff a = (2-3 beta gamma)/gamma and lambda phi0^2 = -(1/2) k',
    k' = k + gamma^2 (1 - beta gamma)/(2 - 3 beta gamma)^2   (derived here by solving T = 0, not assumed).  Mutations fail.
 C  Einstein frame: g~ = (phi/phi0)^2 g is Schwarzschild-de Sitter with the SAME k' (compare t02 D3), phi~ = phi0 constant, and there T_mn = -phi0^2 (k'/2 + lambda phi0^2) g_mn:
    the two routes to k' = -2 lambda phi0^2 agree.  So the theory's couplings fix k' (the frame invariant) and NOT the split into gamma^2/4 and k.
 D  G_eff = -3/(4 pi phi0^2), rho_V = lambda phi0^4, G_eff rho_V = 3 k'/(8 pi) = Lambda/(8 pi): alpha_g does not appear.  Ratio G_eff rho_V / a0^2 with a0 = gamma/2 is
    (3/8pi)(1 + k/a0^2) (beta -> 0): a free integration ratio.  The value 4 requires k/a0^2 = 32 pi/3 - 1.
 E  open-slicing cosmology of the same theory: a0_phys^2/H_dS^2 = Omega_k/Omega_Lambda-bar (identity), i.e. sinh^2 u; a0/H = 1/Z is an EPOCH condition, sinh u = Z.
"""
import sys
import itertools
import sympy as sp
sys.path.insert(0, '.')
from wg_tools import Geo, static_spherical

ok = []


def chk(name, cond):
    ok.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name)


def tensors(geo, X, phi, lam, xi=sp.Rational(1, 6)):
    """T_mn (lower) and EOM for a scalar phi(x) on geo; xi = coupling coefficient (1/6 conformal)."""
    n, g, gi, G, x = geo.n, geo.g, geo.gi, geo.G, geo.x
    d1 = [sp.diff(phi, x[m]) for m in range(n)]

    def hess(f):
        return sp.Matrix(n, n, lambda m, nn: sp.diff(f, x[m], x[nn]) - sum(G[l][m][nn] * sp.diff(f, x[l]) for l in range(n)))

    def box(f):
        H = hess(f)
        return sum(gi[m, m] * H[m, m] for m in range(n))
    grad2 = sum(gi[m, m] * d1[m]**2 for m in range(n))
    Hphi2 = hess(phi**2)
    boxphi = box(phi)
    boxphi2 = box(phi**2)
    Gmn = geo.Ric - geo.g * geo.R / 2
    T = sp.zeros(n, n)
    for m in range(n):
        for nn in range(n):
            T[m, nn] = (d1[m] * d1[nn] - g[m, nn] * grad2 / 2
                        + xi * (g[m, nn] * boxphi2 - Hphi2[m, nn] + Gmn[m, nn] * phi**2)
                        - g[m, nn] * lam * phi**4)
    E = boxphi - xi * geo.R * phi - 4 * lam * phi**3
    return T, E


r = sp.symbols('r', positive=True)
lam, phi0, aa = sp.symbols('lambda phi0 a', real=True)
gam, bet, k = sp.symbols('gamma beta k', real=True)

# ---------------------------------------------------------------- A: controls with generic B(r), phi(r)
Bf = sp.Function('B')(r)
pf = sp.Function('p')(r)
geoG, XG = static_spherical(Bf, r)
TG, EG = tensors(geoG, XG, pf, lam)
tr = sp.simplify(sum(geoG.gi[m, m] * TG[m, m] for m in range(4)) - pf * EG)
chk("A1 trace identity T^m_m = phi E for generic B(r) and generic phi(r) (sign/implementation check of T_mn and the EOM)", tr == 0)
TG2, EG2 = tensors(geoG, XG, pf, lam, xi=sp.Rational(1, 5))
tr2 = sp.simplify(sum(geoG.gi[m, m] * TG2[m, m] for m in range(4)) - pf * EG2)
chk("A2 CONTROL: a non-conformal coupling xi = 1/5 breaks the trace identity", tr2 != 0)

# ---------------------------------------------------------------- B: T = 0 on the MK metric with phi = phi0/(1 + r/a)
Bmk = (1 - 3 * bet * gam) - bet * (2 - 3 * bet * gam) / r + gam * r - k * r**2
geoM, XM = static_spherical(Bmk, r)
phiM = phi0 / (1 + r / aa)
TM, EM = tensors(geoM, XM, phiM, lam)
mixed = [sp.simplify(geoM.gi[m, m] * TM[m, m]) for m in range(4)]
offd = all(sp.simplify(sp.expand_trig(TM[m, n])) == 0 for m in range(4) for n in range(4) if m != n)
chk("B0 T_mn is diagonal on the static spherical MK metric with phi(r)", offd)
Lam2 = sp.symbols('Lam2')   # Lam2 = lambda phi0^2
eqs = []
for m in mixed:
    num = sp.numer(sp.together(sp.simplify(m.subs(lam, Lam2 / phi0**2))))
    eqs += sp.Poly(sp.expand(num), r).coeffs()
sols = sp.solve(eqs, [aa, Lam2], dict=True)
print("   solve T = 0 for (a, lambda phi0^2):", sols)
a_expected = (2 - 3 * bet * gam) / gam
kprime = k + gam**2 * (1 - bet * gam) / (2 - 3 * bet * gam)**2
good = [s for s in sols if sp.simplify(s[aa] - a_expected) == 0 and sp.simplify(s[Lam2] + kprime / 2) == 0]
chk("B1 solving T_mn = 0 (all components) for (a, lambda phi0^2) gives a = (2 - 3 beta gamma)/gamma and lambda phi0^2 = -k'/2 with k' = k + gamma^2(1-beta gamma)/(2-3 beta gamma)^2",
    len(good) >= 1)
subsd = {aa: a_expected, lam: -kprime / (2 * phi0**2)}
chk("B2 with those values every mixed component T^m_n vanishes identically in r", all(sp.simplify(m.subs(subsd)) == 0 for m in mixed))
chk("B3 and the scalar EOM E = 0 holds (it follows from T = 0 through the trace identity)", sp.simplify(EM.subs(subsd)) == 0)
# mutations
bad_a = {aa: (2 - 2 * bet * gam) / gam, lam: -kprime / (2 * phi0**2)}
bad_l = {aa: a_expected, lam: +kprime / (2 * phi0**2)}
bad_k = {aa: a_expected, lam: -(k + gam**2 / 4) / (2 * phi0**2)}
chk("B4 MUTATION rejected: a = (2 - 2 beta gamma)/gamma does not give T = 0", any(sp.simplify(m.subs(bad_a)) != 0 for m in mixed))
chk("B5 MUTATION rejected: the opposite sign of lambda does not give T = 0", any(sp.simplify(m.subs(bad_l)) != 0 for m in mixed))
chk("B6 MUTATION rejected: using k + gamma^2/4 (the beta = 0 form) instead of k' at beta != 0 does not give T = 0", any(sp.simplify(m.subs(bad_k)) != 0 for m in mixed))
# uniqueness inside the power family phi0 (1 + r/a)^p at beta = 0 (fast)
p = sp.symbols('p', real=True)
geo0, _ = static_spherical(1 + gam * r - k * r**2, r)
T0, E0 = tensors(geo0, _, phi0 * (1 + r / aa)**p, lam)
mx0 = [sp.simplify(geo0.gi[m, m] * T0[m, m]) for m in range(4)]
ok_p1 = all(sp.simplify(m.subs({p: -1, aa: 2 / gam, lam: -(k + gam**2 / 4) / (2 * phi0**2)})) == 0 for m in mx0)
ok_p2 = any(sp.simplify(m.subs({p: -2, aa: 2 / gam, lam: -(k + gam**2 / 4) / (2 * phi0**2)})) != 0 for m in mx0)
ok_p3 = any(sp.simplify(m.subs({p: 1, aa: 2 / gam, lam: -(k + gam**2 / 4) / (2 * phi0**2)})) != 0 for m in mx0)
chk("B7 beta = 0 slice: the exponent p = -1 works (a = 2/gamma, lambda phi0^2 = -(gamma^2/4 + k)/2); p = -2 and p = +1 fail", ok_p1 and ok_p2 and ok_p3)

# ---------------------------------------------------------------- C: Einstein frame
# g~ = (phi/phi0)^2 g with phi/phi0 = 1/(1 + r/a) = 1 - a_s r' where r' = r/(1 + r/a); a_s = 1/a = gamma/(2 - 3 beta gamma)
a_s = gam / (2 - 3 * bet * gam)
rp = sp.symbols('rp', positive=True)
Bt = sp.simplify((1 - a_s * rp)**2 * Bmk.subs(r, rp / (1 - a_s * rp)))
Mp = bet * (2 - 3 * bet * gam) / 2
Bsds = 1 - 2 * Mp / rp - kprime * rp**2
chk("C1 the Einstein-frame metric (phi = phi0) has B~(r') = 1 - 2M'/r' - k' r'^2: Schwarzschild-de Sitter with M' = beta(2-3 beta gamma)/2 and the SAME k' (cf. t02 D3)",
    sp.simplify(Bt - Bsds) == 0)
geoS, XS = static_spherical(1 - 2 * sp.Symbol('Mm') / rp - sp.Symbol('kk') * rp**2, rp)
chk("C2 curvature of SdS: R = 12 k' (mostly plus)", sp.simplify(geoS.R - 12 * sp.Symbol('kk')) == 0)
TS, ES = tensors(geoS, XS, phi0, lam)
chk("C3 constant phi = phi0 on SdS: EOM reads -R phi0/6 - 4 lambda phi0^3 = 0, i.e. k' = -2 lambda phi0^2",
    sp.simplify(ES - (-2 * sp.Symbol('kk') * phi0 - 4 * lam * phi0**3)) == 0)
Tform = sp.simplify(TS - (-phi0**2 * (sp.Symbol('kk') / 2 + lam * phi0**2) * geoS.g))
chk("C4 constant phi = phi0 on SdS: T_mn = -phi0^2 (k'/2 + lambda phi0^2) g_mn; it vanishes iff k' = -2 lambda phi0^2 (same condition as B1)", Tform == sp.zeros(4, 4))
chk("C5 the two routes agree: MK-frame T = 0 (B1) and Einstein-frame EOM (C3) both give k' = -2 lambda phi0^2",
    sp.simplify((-2 * lam * phi0**2).subs(lam, -kprime / (2 * phi0**2)) - kprime) == 0)
# what the coupling constants fix, and what they do not
# a one-parameter family at FIXED lambda phi0^2 (beta = 0 slice): gamma = 0, 2, 4 with k = k' - gamma^2/4, k' = 2 (lambda phi0^2 = -1)
fam_ok = True
for g_val in (2, 4, sp.Rational(1, 3)):
    k_val = 2 - sp.Rational(g_val)**2 / 4
    sub = {gam: g_val, k: k_val, aa: 2 / sp.Rational(g_val), lam: -1 / phi0**2, p: -1}
    fam_ok = fam_ok and all(sp.simplify(m.subs(sub)) == 0 for m in mx0)
chk("C6 at fixed lambda phi0^2 = -1 (k' = 2) the beta = 0 solutions gamma = 2 (k = 1), 4 (k = -2), 1/3 (k = 2 - 1/36) ALL satisfy T = 0: a0 = gamma/2 is a free integration constant",
    fam_ok)
sub_bad = {gam: 2, k: 5, aa: 1, lam: -1 / phi0**2, p: -1}
chk("C6b CONTROL: gamma = 2 with k = 5 (violating (gamma/2)^2 + k = 2) does NOT satisfy T = 0",
    any(sp.simplify(m.subs(sub_bad)) != 0 for m in mx0))

# ---------------------------------------------------------------- D: G_eff, rho_V, Lambda, alpha_g
# action for constant phi0:  L = -(1/12) R phi0^2 - lambda phi0^4 ;  GR:  (1/16 pi G) R - rho_V   =>  1/(16 pi G_eff) = -phi0^2/12  (sign flips overall: L_GR = +R/(16 pi G))
Geff = sp.symbols('G_eff')
solG = sp.solve(sp.Eq(1 / (16 * sp.pi * Geff), -phi0**2 / 12), Geff)[0]
chk("D1 G_eff = -3/(4 pi phi0^2)  (negative for the standard-sign kinetic term)", sp.simplify(solG + 3 / (4 * sp.pi * phi0**2)) == 0)
rhoV = lam * phi0**4
Lam_cc = 8 * sp.pi * solG * rhoV
chk("D2 Lambda = 8 pi G_eff rho_V = -6 lambda phi0^2 and Lambda/3 = -2 lambda phi0^2 = k'", sp.simplify(Lam_cc + 6 * lam * phi0**2) == 0)
alpha_g = sp.symbols('alpha_g')
chk("D3 alpha_g appears in neither G_eff, rho_V nor k' (they are functions of lambda, phi0 only)", all(alpha_g not in e.free_symbols for e in (solG, rhoV, Lam_cc)))
chk("D4 G_eff rho_V = 3 k'/(8 pi) exactly (this is just the de Sitter Friedmann relation)", sp.simplify(solG * rhoV - 3 * (-2 * lam * phi0**2) / (8 * sp.pi)) == 0)
a0s, ksym = sp.symbols('a0 k', positive=True)
ratio = sp.simplify((3 * (a0s**2 + ksym) / (8 * sp.pi)) / a0s**2)     # G_eff rho_V / a0^2 with k' = a0^2 + k (beta -> 0), a0 = gamma/2
chk("D5 G_eff rho_V / a0^2 = (3/(8 pi)) (1 + k/a0^2) at beta = 0: it depends on the free ratio k/a0^2", sp.simplify(ratio - 3 / (8 * sp.pi) * (1 + ksym / a0s**2)) == 0)
Z2 = 32 * sp.pi / 3
need = sp.solve(sp.Eq(ratio, 4), ksym)[0] / a0s**2
chk("D6 the puzzle value G rho_V = 4 a0^2 requires k/a0^2 = 32 pi/3 - 1 = 32.51...: not implied by anything in the action",
    sp.simplify(need - (Z2 - 1)) == 0 and abs(float(need) - 32.5109) < 1e-3)
chk("D7 CONTROL: for k/a0^2 = 1 the ratio is 3/(4 pi) = 0.239, not 4", abs(float(ratio.subs({ksym: 1, a0s: 1})) - 3 / (4 * float(sp.pi))) < 1e-12)

# ---------------------------------------------------------------- E: open-slicing cosmology with the same constant
tt, chi, thh, phh, Hc = sp.symbols('tt chi thh phh H_c', positive=True)
a_t = sp.sinh(Hc * tt) / Hc
geoC = Geo((tt, chi, thh, phh), [-1, a_t**2, a_t**2 * sp.sinh(chi)**2, a_t**2 * sp.sinh(chi)**2 * sp.sin(thh)**2])
chk("E1 dS in open slicing a = sinh(Ht)/H has constant R = 12 H^2 and vanishing Weyl tensor (Einstein space, conformally flat)",
    sp.simplify(geoC.R - 12 * Hc**2) == 0 and geoC.weyl_is_zero())
u_ = Hc * tt
adot = sp.diff(a_t, tt)
chk("E2 Friedmann with K = -1: adot^2 - 1 = H^2 a^2", sp.simplify(adot**2 - 1 - Hc**2 * a_t**2) == 0)
Om_L = Hc**2 * a_t**2 / adot**2
Om_k = 1 / adot**2
chk("E3 Omega_Lambda-bar = tanh^2 u and Omega_k = sech^2 u", sp.simplify(Om_L - sp.tanh(u_)**2) == 0 and sp.simplify(Om_k - 1 / sp.cosh(u_)**2) == 0)
a0phys = 1 / a_t          # c^2 sqrt(-K_phys) with K_phys = -1/a^2  (c = 1)
chk("E4 (a0_phys/H)^2 = Omega_k/Omega_Lambda-bar = 1/sinh^2 u  (the CG papers' identification a0 = c^2 sqrt(-K_phys))",
    sp.simplify((a0phys / Hc)**2 - Om_k / Om_L) == 0 and sp.simplify((a0phys / Hc)**2 - 1 / sp.sinh(u_)**2) == 0)
Zv = sp.sqrt(32 * sp.pi / 3)
uZ = sp.asinh(Zv)
chk("E5 a0/H = 1/Z (the puzzle) <=> sinh u = Z: an epoch condition u = asinh(Z) = %.4f (Omega_k = 1/(1+Z^2) = %.4f); a0 = H/sinh(Ht) is NOT constant in time"
    % (float(uZ), float(1 / (1 + Zv**2))), sp.simplify(sp.sinh(uZ) - Zv) == 0 and float(1 / (1 + Zv**2)) < 0.03)
chk("E6 CONTROL: a0/H = 1/sinh u changes with the epoch: u = 1 gives %.4f, u = 2 gives %.4f" % (float(1 / sp.sinh(1)), float(1 / sp.sinh(2))), abs(float(1 / sp.sinh(1) - 1 / sp.sinh(2))) > 0.5)

# ---------------------------------------------------------------- F: the epoch in the CG papers' own cosmology (algebra of the quoted eqs (230)-(232) of astro-ph/0505266)
T, Tm, TV = sp.symbols('T T_m T_V', positive=True)
beta_m = (Tm**4 + TV**4) / (Tm**4 - TV**4)                    # eq (232)
# R^2 = R_min^2 [1 + 2 beta sinh^2(u)/(beta - 1)]  (eq (230) with A != 0),  T^2 = T_m^2 R_min^2/R^2  =>  sinh^2 u:
sinh2 = (beta_m - 1) / (2 * beta_m) * (Tm**2 / T**2 - 1)
tanh2 = sp.simplify(sinh2 / (1 + sinh2))
tanh2_paper = (1 - T**2 / Tm**2) / (1 + T**2 * Tm**2 / TV**4)  # eq (232), second line
chk("F1 from R^2(t) of eq (230) and beta of eq (232): tanh^2(u) = (1 - T^2/T_m^2)/(1 + T^2 T_m^2/T_V^4), reproducing the paper's eq (232)", sp.simplify(tanh2 - tanh2_paper) == 0)
chk("F2 CONTROL: with beta -> (Tm^4 - TV^4)/(Tm^4 + TV^4) (inverted) the paper's eq (232) is NOT reproduced",
    sp.simplify(sp.simplify(((lambda b: (b - 1) / (2 * b) * (Tm**2 / T**2 - 1))((Tm**4 - TV**4) / (Tm**4 + TV**4)))) / (1 + ((lambda b: (b - 1) / (2 * b) * (Tm**2 / T**2 - 1))((Tm**4 - TV**4) / (Tm**4 + TV**4)))) - tanh2_paper) != 0)
a0_over_H = sp.simplify(1 / sp.sqrt(sinh2))
exact = (1 / sinh2).subs({T: 1, Tm: 10**6, TV: 10**3})
chk("F3 hence (a0/H_dS)^2 = 1/sinh^2 u = T^2 (T_m^4 + T_V^4)/(T_V^4 (T_m^2 - T^2)) -> T^2 T_m^2/T_V^4 for T_m >> T_V, T",
    sp.cancel(sp.together(1 / sinh2 - T**2 * (Tm**4 + TV**4) / (TV**4 * (Tm**2 - T**2)))) == 0
    and abs(sp.N(exact) - 1) < 1e-9)
# what the puzzle would demand: 1/sinh^2 u = 3/(32 pi)  =>  T_m T_0 = T_V^2 sqrt(3/(32 pi)) (leading order): an initial-condition (bounce temperature) statement
chk("F4 the puzzle a0/H = 1/Z would read T_0 T_max = T_V^2/Z (T_max = bounce temperature, an integration constant of the cosmology, not a coupling); numerically Z = %.4f"
    % float(sp.sqrt(32 * sp.pi / 3)), abs(float(sp.sqrt(32 * sp.pi / 3)) - 5.7888) < 1e-3)

# ---------------------------------------------------------------- G: a particle whose mass is generated by the scalar, m = mu*phi(x), moves on Einstein-frame geodesics
# action  S = -mu Integral phi(r) sqrt(B td^2 - rd^2/B - r^2 phid^2) d(lambda)  (dots = d/d lambda).  With r' = r/(1 + r/a), phi = phi0 (1 - r'/a) ... check the integrand identity:
tdot, rdot, phdot = sp.symbols('tdot rdot phdot', real=True)
a_s2 = sp.symbols('a_s2', positive=True)      # a_s = 1/a of the SCT
r_p = sp.symbols('r_p', positive=True)
Bg_ = sp.Function('B')
r_old = r_p / (1 - a_s2 * r_p)                 # r as a function of r'
phi_over_phi0 = 1 - a_s2 * r_p                 # phi/phi0 = 1/(1 + r/a) = 1 - a_s r'
rdot_old = sp.diff(r_old, r_p) * sp.Symbol('rpdot')
lhs = phi_over_phi0**2 * (Bg_(r_old) * tdot**2 - rdot_old**2 / Bg_(r_old) - r_old**2 * phdot**2)
Bt_ = phi_over_phi0**2 * Bg_(r_old)
rhs = Bt_ * tdot**2 - sp.Symbol('rpdot')**2 / Bt_ - r_p**2 * phdot**2
chk("G1 the variable-mass particle Lagrangian (m = mu phi) equals the GEODESIC Lagrangian of the Einstein-frame metric g~ = (phi/phi0)^2 g, identically for any B(r): phi^2 (B td^2 - rd^2/B - r^2 phid^2) = phi0^2 (B~ td^2 - rd'^2/B~ - r'^2 phid^2)",
    sp.simplify(lhs - rhs) == 0)
chk("G1b CONTROL: with a constant mass (no phi factor) the same integrand is NOT the Einstein-frame geodesic Lagrangian",
    sp.simplify((Bg_(r_old) * tdot**2 - rdot_old**2 / Bg_(r_old) - r_old**2 * phdot**2) - rhs) != 0)

print("\nPASS %d / %d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
