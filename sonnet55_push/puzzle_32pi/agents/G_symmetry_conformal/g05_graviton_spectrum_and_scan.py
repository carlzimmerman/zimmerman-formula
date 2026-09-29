"""g05: (A) the massive-graviton (Fierz-Pauli) helicity-2 spectrum in dS4 computed from the covariant equation (Box - 2H^2 - m^2) h_{mu nu} = 0,
          giving Delta(3 - Delta) = m^2/H^2 for the tensor mode too (massless graviton Delta = 0,3; partially massless m^2 = 2H^2 at Delta = 1,2);
      (B) the dimensionless dS4 / S^4 numbers (rational or algebraic) placed next to the framework's Z = sqrt(32 pi/3) with a
          NULL-CALIBRATED look-elsewhere test: the menu is fixed in this file, I know the target, so this characterises, it does not discover.

The Higuchi bound (unitarity m^2 >= 2H^2 for the massive spin-2 field) is QUOTED from the literature (Higuchi 1987; Deser-Waldron), not recomputed here.
"""
import sympy as sp, mpmath as mp, numpy as np, sys, random
ok = []
def chk(n, c):
    ok.append(bool(c)); print(("PASS " if c else "FAIL ") + n)

# ---------------- A: tensor mode in dS4, flat slicing, cosmic time
t, x, y, z = sp.symbols('t x y z', real=True); H, k, m2 = sp.symbols('H k m2', positive=True)
Y = (t, x, y, z)
a = sp.exp(H * t)
g = sp.diag(-1, a**2, a**2, a**2); gi = g.inv()
Gam = [[[sum(gi[l, s] * (sp.diff(g[s, mu], Y[nu]) + sp.diff(g[s, nu], Y[mu]) - sp.diff(g[mu, nu], Y[s])) for s in range(4)) / 2 for nu in range(4)] for mu in range(4)] for l in range(4)]
gam = sp.Function('gamma')(t)
h = sp.zeros(4, 4); h[1, 1] = a**2 * gam * sp.cos(k * z); h[2, 2] = -a**2 * gam * sp.cos(k * z)
def cov1(T):        # T_{mu nu} -> (nabla_rho T)_{rho mu nu}
    return [[[sp.diff(T[mu, nu], Y[rho]) - sum(Gam[l][rho][mu] * T[l, nu] + Gam[l][rho][nu] * T[mu, l] for l in range(4)) for nu in range(4)] for mu in range(4)] for rho in range(4)]
D1 = cov1(h)
def cov2(D):        # (nabla_sigma D)_{sigma rho mu nu}
    out = {}
    for s in range(4):
        for r in range(4):
            for mu in range(4):
                for nu in range(4):
                    out[(s, r, mu, nu)] = sp.diff(D[r][mu][nu], Y[s]) - sum(Gam[l][s][r] * D[l][mu][nu] + Gam[l][s][mu] * D[r][l][nu] + Gam[l][s][nu] * D[r][mu][l] for l in range(4))
    return out
D2 = cov2(D1)
box = sp.zeros(4, 4)
for mu in range(4):
    for nu in range(4):
        box[mu, nu] = sp.simplify(sum(gi[r, r] * D2[(r, r, mu, nu)] for r in range(4)))
trace = sp.simplify(sum(gi[i, i] * h[i, i] for i in range(4)))
div = [sp.simplify(sum(gi[r, r] * D1[r][r][nu] for r in range(4))) for nu in range(4)]
chk("A1 the ansatz h_xx = -h_yy = a^2 gamma(t) cos(k z) is traceless and transverse (TT) in dS4", trace == 0 and all(d == 0 for d in div))
eq = sp.simplify((box[1, 1] - 2 * H**2 * h[1, 1] - m2 * h[1, 1]) / (a**2 * sp.cos(k * z)))
target = -(sp.diff(gam, t, 2) + 3 * H * sp.diff(gam, t) + (k**2 * sp.exp(-2 * H * t) + m2) * gam)
chk("A2 (Box - 2H^2 - m^2) h_xx / (a^2 cos kz) = -(gamma'' + 3H gamma' + (k^2/a^2 + m^2) gamma): the helicity-2 mode obeys a massive-scalar equation", sp.simplify(eq - target) == 0)
# the other components of the equation vanish identically for this ansatz
rest = [sp.simplify(box[i, j] - (2 * H**2 + m2) * h[i, j]) for i in range(4) for j in range(4) if (i, j) not in [(1, 1), (2, 2)]]
chk("A3 all other components of (Box - 2H^2 - m^2) h are zero for this ansatz, and the yy component is minus the xx one", all(r == 0 for r in rest) and sp.simplify(box[2, 2] - (2 * H**2 + m2) * h[2, 2] + (box[1, 1] - (2 * H**2 + m2) * h[1, 1])) == 0)
# late times (k a^-1 -> 0): gamma ~ exp(-Delta H t):  Delta (3 - Delta) = m^2/H^2
Dl = sp.symbols('Delta')
late = sp.simplify((sp.diff(sp.exp(-Dl * H * t), t, 2) + 3 * H * sp.diff(sp.exp(-Dl * H * t), t) + m2 * sp.exp(-Dl * H * t)) / sp.exp(-Dl * H * t))
chk("A4 late-time falloff gamma ~ exp(-Delta H t) requires m^2 = H^2 Delta (3 - Delta) (same relation as the scalar, from the tensor equation itself)", sp.simplify(late - (Dl**2 * H**2 - 3 * Dl * H**2 + m2)) == 0)
print("   spin-2 (helicity-2) spectrum, m^2/H^2 = Delta(3-Delta):")
for nm, m2v in [('massless graviton', 0), ('partially massless / Higuchi edge', 2), ('principal-series edge', sp.Rational(9, 4)), ('m^2 = 3/(32 pi) H^2 (framework a0^2)', sp.Rational(3, 32) / sp.pi)]:
    d_ = sp.Rational(3, 2) - sp.sqrt(sp.Rational(9, 4) - m2v)
    print("      %-42s m^2/H^2 = %-10s  Delta = %s" % (nm, sp.nsimplify(m2v), sp.nsimplify(d_) if m2v in (0, 2, sp.Rational(9, 4)) else '%.6f' % float(d_)))
chk("A5 massless graviton -> Delta = 0 or 3; m^2 = 2H^2 (partially massless point, also the Higuchi edge quoted from literature) -> Delta = 1 or 2",
    sp.solve(Dl * (3 - Dl) - 0, Dl) == [0, 3] and sorted(sp.solve(Dl * (3 - Dl) - 2, Dl)) == [1, 2])

# ---------------- B: menu (fixed here, before running) and NULL calibration
# dimensionless dS4 / S^4 numbers produced by the group theory above
menu_n = {}
for lval in range(1, 11):
    menu_n['S4 eigenvalue l(l+3), l=%d' % lval] = lval * (lval + 3)
    menu_n['S4 degeneracy D_l=(l+1)(l+2)(2l+3)/6, l=%d' % lval] = (lval + 1) * (lval + 2) * (2 * lval + 3) // 6
for nm, v in [('conformal mass 2', 2), ('principal-series edge 9/4', 2.25), ('Yamabe weight 5/4', 1.25), ('dim SO(4,1)', 10), ('dim SO(4,2)', 15), ('dim SO(5,1)', 15),
              ('graviton polarisations x d.o.f. 2*5', 10), ('rank/dimension combos 4', 4), ('spin-2 Casimir s(s+1)=6', 6), ('Delta=3 Casimir combos 12 (R=12H^2)', 12), ('Kretschmann 24 (K=24H^4)', 24)]:
    menu_n[nm] = v
# maps from a menu number n to a Z candidate: Z = n, Z = sqrt(n)  (two maps, declared in advance; each is an INSERTION, none is derived)
cands = []
for nm, n_ in menu_n.items():
    cands.append(('Z=%s' % nm, float(n_))); cands.append(('Z=sqrt(%s)' % nm, float(n_)**0.5))
Zt = float(mp.sqrt(32 * mp.pi / 3))
tol = 0.02
hits = [(nm, v) for nm, v in cands if abs(v / Zt - 1) < tol]
print("   menu size: %d numbers -> %d Z-candidates; hits within %.0f%% of Z = %.4f: %d" % (len(menu_n), len(cands), 100 * tol, Zt, len(hits)))
for nm, v in hits: print("      HIT", nm, v)
near = sorted(cands, key=lambda c: abs(c[1] / Zt - 1))[:5]
print("   five nearest:", [(nm, round(v, 4), '%+.1f%%' % (100 * (v / Zt - 1))) for nm, v in near])
# null: the same menu against targets Zt * u, u log-uniform in [1/2, 2] (a window of 'plausible' Z values), count hits within tol
rng = np.random.default_rng(1)
nulls = []
for _ in range(20000):
    tgt = Zt * np.exp(rng.uniform(np.log(0.5), np.log(2.0)))
    nulls.append(sum(1 for _, v in cands if abs(v / tgt - 1) < tol))
nulls = np.array(nulls)
frac1 = float((nulls >= 1).mean())
print("   null (20000 targets in Z*[1/2,2]): mean hits %.2f ; fraction of random targets with >= 1 hit within %.0f%% = %.2f" % (nulls.mean(), 100 * tol, frac1))
chk("B1 no candidate from the dS4/S4 spectral menu lies within 2%% of Z (0 hits); a 2%% hit would have occurred by chance for %.0f%% of random targets, so even a hit would have been uninformative" % (100 * frac1), len(hits) == 0 and 0.2 < frac1 < 0.9)
# control of the scan machinery: a target equal to a menu member must be hit
cnt_planted = sum(1 for _, v in cands if abs(v / 14.0 - 1) < tol)
chk("B2 scan control: a planted target equal to a menu member (14 = D_2) IS hit (count %d), so the machinery would see a hit" % cnt_planted, cnt_planted >= 1)
# exact statement: Z^2 = 32 pi/3 is transcendental -> equality with any menu value is impossible
chk("B3 exact statement: Z^2 = 32 pi/3 is not algebraic, hence equals no rational/algebraic menu value; the closest are at the ~%.0f%% level" % (100 * abs(near[0][1] / Zt - 1)), (32 * sp.pi / 3).is_algebraic is False)
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
