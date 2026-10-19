"""AS3 post-run report script (added AFTER as3_trial.py's first run; reported, NOT graded; see Amendment 1 of AS3_PREREGISTRATION.md).
The frozen selection rule says that with two or more admissible roots 'all are reported' and the verdict is NOT DIAGNOSTIC.  as3_trial.py
printed the roots but not f_g and P at each admissible R^2 root; this script reports them.  It also re-derives the flat-space f_g by a second
route: the |beta| -> infinity limit equals the trace restricted to ker(gauge fixing) (for rho = 0 the gauge-fixing matrix is a(s) x a constant
tensor, so its regulator insertion is annihilated by the limit propagator E (E^T K E)^{-1} E^T); the result must equal the brute-force formula
printed by as3_trial.py exactly.  No class changes: the graded verdict stays NOT DIAGNOSTIC."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
_AS2 = Path(__file__).resolve().parent.parent / "AS2_fg_cpr_scheme"
if str(_AS2) not in sys.path:
    sys.path.insert(0, str(_AS2))
import numpy as np
import sympy as sp
import as2_common as A
import as3_trial as T

FG1, C1 = A.FG1, A.C1
F0, F1, F2, dF1, dF2 = A.F0, A.F1, A.F2, A.dF1, A.dF2

# ---- f_g by restriction to ker(gauge fixing)
s = sp.Symbol("s", positive=True)
B, V1, V2, hm, hp, am, ap = FG1.bilinear_action(s)
B = B.subs(FG1.agf, 0).subs({FG1.lam: -F0 / (2 * F1)}).subs({FG1.g: -1 / (16 * sp.pi * F1)})
Hm, _ = FG1.hmat("hm"); Hp, _ = FG1.hmat("hp")
tr = lambda H: sum(H[i, i] for i in range(4))
B += sp.Rational(1, 2) * F2 * s**2 * (tr(Hm) - Hm[3, 3]) * (tr(Hp) - Hp[3, 3])
chim = [Hm[3, m] - sp.Rational(1, 4) * (1 if m == 3 else 0) * tr(Hm) for m in range(4)]
chip = [Hp[3, m] - sp.Rational(1, 4) * (1 if m == 3 else 0) * tr(Hp) for m in range(4)]
GF = -sp.Rational(1, 2) * s**2 * sum(chim[m] * chip[m] for m in range(4))     # coefficient of beta
Phim, Phip = hm + am, hp + ap
n = 14
Mk = sp.Matrix(n, n, lambda i, j: sp.diff(B, Phim[i], Phip[j]))
Agf = sp.Matrix(n, n, lambda i, j: sp.diff(GF, Phim[i], Phip[j]))
M1 = sp.Matrix(n, n, lambda i, j: sp.diff(V1, Phim[i], Phip[j]))
M2 = sp.Matrix(n, n, lambda i, j: sp.diff(V2, Phim[i], Phip[j]))
idx = {pq: i for i, pq in enumerate(FG1.pairs)}
def vec(d):
    v = [0] * n
    for k, c in d.items():
        v[idx[k]] += c
    return v
third = sp.Rational(1, 3)
cols = [vec({(0, 1): 1}), vec({(0, 2): 1}), vec({(1, 2): 1}),
        vec({(0, 0): 1, (3, 3): third}), vec({(1, 1): 1, (3, 3): third}), vec({(2, 2): 1, (3, 3): third})]
cols += [[0] * 10 + [1 if j == k else 0 for j in range(4)] for k in range(4)]
E = sp.Matrix(cols).T
chk_ker = sp.simplify(Agf * E) == sp.zeros(n, 10)
print(f"ker check: gauge-fixing matrix annihilates the 6 graviton + 4 photon basis vectors: {chk_ker}  (6 = 5 TT + the conformal mode h_mn = phi delta_mn)")
kap = FG1.kap
MkP = (E.T * Mk * E).subs(s, 1)
dR = (E.T * sp.diff(Mk, s) * E).subs(s, 1) * 2
dR[:6, :6] += dF1 * ((E.T * sp.diff(Mk, F1) * E)[:6, :6].subs(s, 1) - (E.T * sp.diff(Mk, F1) * E)[:6, :6])
dR[:6, :6] += dF2 * ((E.T * sp.diff(Mk, F2) * E)[:6, :6].subs(s, 1) - (E.T * sp.diff(Mk, F2) * E)[:6, :6])
dR = dR.subs(s, kap**2)
G = sp.zeros(10, 10)
G[:6, :6] = MkP[:6, :6].inv(); G[6:, 6:] = MkP[6:, 6:].inv()
m1, m2 = E.T * M1 * E, E.T * M2 * E
Tr = sp.expand(-sp.Rational(1, 2) * (G * m2 * G * dR).trace() + sp.Rational(1, 2) * (G * m1 * G * m1 * G * dR).trace())
trC = sum(Tr.coeff(Fa, 2) for Fa in FG1.Fs)
cFF = sp.integrate(sp.expand(trC / 12 * kap**3 / (8 * sp.pi**2)), (kap, 0, 1))
fg_proj = sp.factor(sp.simplify(2 * FG1.e**2 * cFF))
fg_brute = -5 * (8 * F0 + 4 * F1 - dF1) / (1152 * sp.pi**2 * (F0 + F1)**2)   # as printed by as3_trial.py (brute-force |beta| -> inf)
print(f"f_g (restricted to ker of the gauge fixing) = {fg_proj}")
print(f"equals the brute-force formula of as3_trial.out exactly: {sp.simplify(fg_proj - fg_brute) == 0}")
g_, l_ = sp.symbols("g lambda", positive=True)
fg_gl = sp.factor(sp.simplify(fg_proj.subs({F0: 2 * l_ / (16 * sp.pi * g_), F1: -1 / (16 * sp.pi * g_), dF1: -2 / (16 * sp.pi * g_)})))
print(f"at a fixed point (d_t f' = 2 g~1), in (g, lambda): f_g = {fg_gl}  (= the AS1 TT-only f_g 5g(eta+4-16L)/(72 pi (1-2L)^2) at eta_N = -2)")

# ---- all admissible R^2 SM roots: f_g, P, systematics (reported, NOT graded)
HK = T.G.heat_kernels()
Xm, _ = A.X_matter(HK)
rows, _ = T.scan(2, HK, sp.expand(Xm.subs(T.SM)))
b2 = C1._exec_lane_b_script("b2_required_boundary.py")
print("\nR^2 with SM matter: every root (the verdict is NOT DIAGNOSTIC: two admissible roots, none is picked)")
for k, r in enumerate(rows, 1):
    gl = r["glb"]
    line = f"  root {k}: (g, lambda, b) = ({gl[0]:.6f}, {gl[1]:.6f}, {gl[2]:.7f})  admissible {r['adm']}  theta = {np.array2string(r['theta'], precision=4)}"
    print(line)
    if r["adm"]:
        fgv = T.fg_at(fg_proj, r["gt"])
        P_ = C1.downstream_P(fgv)
        P2, P1 = T.two_loop_P(C1.gY_star_from_fg(fgv), b2)
        Pr = T.reduced_planck_P(fgv)
        print(f"          f_g = {fgv:.8f}, g_Y* = {C1.gY_star_from_fg(fgv):.6f}, theta_Y = {-2*fgv:.6f} (IR-attractive), P = {P_:.5f};"
              f" two-loop {P2:.5f} ({P2-P_:+.5f}); reduced Planck {Pr:.5f} ({Pr-P_:+.5f}); P - P_EH = {P_-95.57847:+.5f} (P_EH from as3_trial.out)")
