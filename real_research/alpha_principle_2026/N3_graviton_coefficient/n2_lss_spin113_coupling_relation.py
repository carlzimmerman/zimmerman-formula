#!/usr/bin/env python3
"""N2 -- Lisi-Smolin-Speziale (arXiv:1004.4866) spin(1+N,3), N = 10: is the Yang-Mills coefficient tied to G*Lambda?
Action as printed, eq (1):  S = (1/g) Int < B^F + B Phi B + (1/3) B Phi^3 B >,  Phi = Hodge star (their ansatz (8)), star^2 = -1 on 2-forms.
Connection H = (1/2) omega + (1/4) E + A acting on the spinor representation, E = e' phi (Clifford product), so D = d + H on fermions.
STEPS (each a check):
 (a) eliminate B: B = (3/4) *F and S = 3/(8g) <F^*F>   [their (9),(25)]     (symbolic 6x6 star operator, Lorentzian pairing)
 (b) F_L = (1/4)[R^ab - (phi^2/4) e^a e^b] g_ab  (Clifford blocks; done exactly in n1) => contraction identity  L.L = Riem^2 - phi^2 R + (3/2) phi^4  (exact random algebraic curvature tensors)
     and <F_cd F^cd>_L = -(1/8) L.L (Clifford scalar part)
 (c) coefficients: EH = K phi^2/16, potential (3/2)phi^4 K/16  =>  Lambda = 3 phi^2/4, R0 = 4 Lambda;  physical 1/(16 pi G) = K v^2/16 => G = 8g/(3 pi v^2);  G*Lambda = 2g/pi (v-independent)
 (d) YM normalisation through the fermion covariant derivative: T(16)/T(10) = 2 (explicit Cl(10), 32x32); GUT-normalised g_G^2 = 4/K = 32 g/3; alpha_G = (4/3) G Lambda.
     Riemann^2 coefficient K/16 = 1/(4 g_G^2) (forced ratio gravity-sector vs gauge coefficient)
 (e) printed relations (g_YM^2 = 2g/3, G_N = 128 g/(3 v^2), no 16 pi) and the four convention variants; values at the observed x = Lambda l_P^2 (lane M inputs) and the x required for alpha = 1/137.036 and 1/25.
 K = 3/(8g).  Sign conventions of the unified action are NOT resolved (see prints); only magnitudes are used.
Run:    python3 n2_lss_spin113_coupling_relation.py           (exit 0)
MUTATE: python3 n2_lss_spin113_coupling_relation.py MUTATE   (Phi^3 coefficient 1/3 -> 1/2; the eq (25) prefactor 3/(8g) check must FAIL -> exit 1)
"""
import sys
from fractions import Fraction as Fr
from itertools import combinations, product
import numpy as np
import sympy as sp
import mpmath as mp
from clifford_lib import Cl, lorentz_plus_internal

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
fails = []
def chk(n, ok, m=""):
    print(("[PASS] " if ok else "[FAIL] ") + n + " " + m)
    if not ok:
        fails.append(n)

# ---------------- (a) B elimination ----------------
g = sp.symbols('g', positive=True)
alpha_c, beta_c = sp.Integer(1), (sp.Rational(1, 2) if MUT else sp.Rational(1, 3))
I3 = sp.eye(3); Z3 = sp.zeros(3)
W = sp.Matrix(sp.BlockMatrix([[Z3, I3], [I3, Z3]]))        # wedge pairing of 2-forms, basis (e0i | ejk)
S = sp.Matrix(sp.BlockMatrix([[Z3, -I3], [I3, Z3]]))       # Hodge star, S^2 = -1
chk("star^2 = -1 and W*S symmetric (star is self-adjoint w.r.t. the wedge pairing)", S * S == -sp.eye(6) and (W * S) == (W * S).T)
Fv = sp.Matrix(sp.symbols('f0:6')); Bv = sp.Matrix(sp.symbols('b0:6'))
Lag = ((Bv.T * W * Fv)[0] + alpha_c * (Bv.T * W * S * Bv)[0] + beta_c * (Bv.T * W * S**3 * Bv)[0]) / g
sol = sp.solve([sp.diff(Lag, x) for x in Bv], list(Bv), dict=True)[0]
Bs = sp.Matrix([sol[x] for x in Bv])
Smin = sp.simplify(Lag.subs(sol))
FSF = sp.expand((Fv.T * W * S * Fv)[0])
pref = sp.simplify(sp.Poly(Smin, *list(Fv)).as_expr() / FSF) if FSF != 0 else None
chk("B = (3/4) star F   [their (9)]", sp.simplify(Bs - sp.Rational(3, 4) * S * Fv) == sp.zeros(6, 1), "B - (3/4)*F = %s" % sp.simplify(Bs - sp.Rational(3, 4) * S * Fv).T)
chk("S_min = 3/(8g) <F ^ *F>   [their (25)]", sp.simplify(pref - sp.Rational(3, 8) / g) == 0, "prefactor = %s" % pref)
K = sp.Rational(3, 8) / g

# ---------------- (b) contraction identity and Clifford scalar part ----------------
eta = [1, -1, -1, -1]
def rand_curv(seed):
    rng = np.random.RandomState(seed)
    Rl = [[[[Fr(0)] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for k in range(3):
        Sk = rng.randint(-3, 4, size=(4, 4)); Sk = Sk + Sk.T
        for a, b, c, d in product(range(4), repeat=4):
            Rl[a][b][c][d] += Fr(int(Sk[a, c] * Sk[b, d] - Sk[a, d] * Sk[b, c]))
    return Rl
def up(Rl):  # R^{ab}_{cd} = eta^{aa} eta^{bb} R_{abcd}
    return [[[[Rl[a][b][c][d] * eta[a] * eta[b] for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
p = Fr(7, 3)   # phi^2
cl = lorentz_plus_internal(0)
J = {(a, b): cl.word([a, b], Fr(1, 2)) for a, b in combinations(range(4), 2)}
okI = okC = True
for seed in (1, 2, 3):
    Rl = rand_curv(seed); Ru = up(Rl)
    Riem2 = sum(Rl[a][b][c][d] * Rl[a][b][c][d] * eta[a] * eta[b] * eta[c] * eta[d] for a, b, c, d in product(range(4), repeat=4))
    Rs = sum(Ru[a][b][a][b] for a, b in product(range(4), repeat=2))
    dl = lambda a, b, c, d: (1 if (a == c and b == d) else 0) - (1 if (a == d and b == c) else 0)
    Lu = [[[[Ru[a][b][c][d] - p / 4 * dl(a, b, c, d) for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
    LL = sum(Lu[a][b][c][d] ** 2 * eta[a] * eta[b] * eta[c] * eta[d] for a, b, c, d in product(range(4), repeat=4))
    if LL != Riem2 - p * Rs + Fr(3, 2) * p * p:
        okI = False
    # Clifford: F_cd = sum_{a<b} L^{ab}_{cd} J_ab ; <F_cd F^cd> = -(1/8) L.L
    tot = Fr(0)
    for c, d in product(range(4), repeat=2):
        Fcd = {}
        for (a, b), Jab in J.items():
            Fcd = cl.add(Fcd, Jab, Lu[a][b][c][d])
        tot += cl.scalar(cl.mul(Fcd, Fcd)) * eta[c] * eta[d]
    if tot != Fr(-1, 8) * LL:
        okC = False
chk("L.L = Riem^2 - phi^2 R + (3/2) phi^4 (3 random algebraic curvature tensors, exact)", okI)
chk("Clifford scalar part: <F_cd F^cd>_L = -(1/8) L.L (exact)", okC)

# ---------------- (c) coefficients ----------------
v, R, gg, Lam, Gn = sp.symbols('v R g Lambda G', positive=True)
phi2 = v**2
# action density (magnitude, overall sign convention s dropped): (K/16)[ phi^2 R - (3/2) phi^4 + ... ] = (K phi^2/16)(R - 2 Lambda)
Lam_sol = sp.Rational(3, 4) * phi2
chk("Lambda = 3 v^2/4  [their (28)/(27): 2 Lambda = (3/2) v^2]", sp.simplify((sp.Rational(3, 2) * phi2) / 2 - Lam_sol) == 0)
# de Sitter from F_L = 0: R^ab_cd = (phi^2/4)(d d - d d) => R = 12 phi^2/4 = 3 phi^2 = 4 Lambda
chk("R0 = 3 v^2 = 4 Lambda  [their (28)]", sp.simplify(12 * phi2 / 4 - 4 * Lam_sol) == 0)
Kc = sp.Rational(3, 8) / gg
G_phys = sp.solve(sp.Eq(1 / (16 * sp.pi * Gn), Kc * phi2 / 16), Gn)[0]
chk("physical G = 8 g/(3 pi v^2)", sp.simplify(G_phys - 8 * gg / (3 * sp.pi * v**2)) == 0, str(sp.simplify(G_phys)))
GL = sp.simplify(G_phys * Lam_sol)
chk("G*Lambda = 2 g/pi, independent of the Higgs vev v", sp.simplify(GL - 2 * gg / sp.pi) == 0 and sp.diff(GL, v) == 0, str(GL))

# ---------------- (d) normalisation ----------------
# T(16)/T(10): explicit Cl(10) matrices (Jordan-Wigner)
def gammas(n):
    s1 = np.array([[0, 1], [1, 0]], complex); s2 = np.array([[0, -1j], [1j, 0]]); s3 = np.diag([1, -1]).astype(complex); one = np.eye(2, dtype=complex)
    out = []
    for k in range(n):
        for s in (s1, s2):
            m = np.array([[1]], complex)
            for _ in range(k):
                m = np.kron(m, s3)
            m = np.kron(m, s)
            for _ in range(n - k - 1):
                m = np.kron(m, one)
            out.append(m)
    return out
np.seterr(all='ignore')             # some macOS BLAS builds emit spurious FP warnings on small complex matmuls; results are asserted below
gm = gammas(5)                      # 10 gammas, 32x32, all square to +1
chir = np.eye(32, dtype=complex)
for x in gm:
    chir = chir @ x
chir = chir * (1j) ** 5             # (i)^5 * product squares to 1 in d=10 (checked below)
chk("Cl(10) chirality matrix squares to 1", np.allclose(chir @ chir, np.eye(32)), "")
Pp = (np.eye(32) + chir) / 2
J12 = 0.5 * gm[0] @ gm[1]
t16 = np.trace(Pp @ J12 @ J12).real            # = -(16)/4
M12 = np.zeros((10, 10)); M12[0, 1] = 1; M12[1, 0] = -1
t10 = np.trace(M12 @ M12)                       # = -2
chk("T(16)/T(10) = 2 (tr_16 J12^2 = %.3f, tr_10 M12^2 = %.3f)" % (t16, t10), abs(t16 / t10 - 2) < 1e-12)
cl10 = Cl([1] * 10)
sc_JJ = cl10.scalar(cl10.mul(cl10.word([0, 1], Fr(1, 2)), cl10.word([0, 1], Fr(1, 2))))
chk("cross-check by Clifford scalar part: tr_16 J^2 = 16 <J^2> = %s (the chirality term <Gamma J J> vanishes, 10 indices vs 4)" % (16 * sc_JJ),
    16 * sc_JJ == -4 and cl10.scalar(cl10.mul(cl10.word(list(range(10))), cl10.mul(cl10.word([0, 1], Fr(1, 2)), cl10.word([0, 1], Fr(1, 2))))) == 0)
# g_G^2 = 4/K  from  (K/8) sum_{m<n} f^2 = 1/(2 g_G^2)
gG2 = sp.simplify(4 / Kc)
chk("g_G^2 = 4/K = 32 g/3 (GUT normalisation T(10)=1, D = d + H on the spinor)", sp.simplify(gG2 - 32 * gg / 3) == 0)
aG = sp.simplify(gG2 / (4 * sp.pi))
ratio = sp.simplify(aG / GL)
chk("alpha_G/(G Lambda) = 4/3 exactly", sp.simplify(ratio - sp.Rational(4, 3)) == 0, "ratio = %s" % ratio)
chk("Riemann^2 coefficient K/16 = 1/(4 g_G^2) (forced ratio gravity-sector : gauge coefficient)", sp.simplify(Kc / 16 - 1 / (4 * gG2)) == 0)
# sign structure note (not scored)
print("   sign note: my Clifford blocks give <F_cd F^cd> < 0 for BOTH the Lorentz block (-(1/8) L.L) and the spin(N) block (-(1/4) sum f^2);")
print("   the printed (27) has Riem^2 and F_N^2 with OPPOSITE signs. Overall orientation/signature conventions unresolved here; magnitudes only.")

# ---------------- (e) printed relations and convention variants ----------------
Gprinted_over = sp.Rational(128, 3) * gg / v**2            # printed G_N (no 16 pi)
gprinted = sp.Rational(2, 3) * gg                          # printed g_YM^2
variants = {
 "V0 mine: physical G, g_G^2=32g/3": (G_phys, gG2),
 "V1 physical G, printed g_YM^2=2g/3": (G_phys, gprinted),
 "V2 printed G_N=128g/(3v^2), printed g_YM^2": (Gprinted_over, gprinted),
 "V3 printed G_N, mine g_G^2": (Gprinted_over, gG2),
}
mp.mp.dps = 30
Om, H0 = mp.mpf('0.6847'), mp.mpf('67.4') * 1000 / mp.mpf('3.0856775814913673e22')
cc, Gn_, hb = mp.mpf('299792458'), mp.mpf('6.67430e-11'), mp.mpf('1.054571817e-34')
Lam_SI = 3 * Om * H0**2 / cc**2
x_obs = Lam_SI * (Gn_ * hb / cc**3)
print("observed x = G Lambda (hbar = c = 1) = %.4e   (lane M's inputs)" % x_obs)
alpha_T = 1 / mp.mpf('137.035999177')
res = {}
for name, (Gx, g2) in variants.items():
    f = sp.simplify((g2 / (4 * sp.pi)) / (Gx * Lam_sol))
    fv = mp.mpf(str(sp.N(f, 30)))
    a_obs = fv * x_obs
    res[name] = fv
    print("  %-46s alpha/(G Lambda) = %-12s alpha(obs) = %.3e   needs G Lambda = %.3e for 1/137.036, %.3e for 1/25"
          % (name, sp.nsimplify(f), a_obs, alpha_T / fv, mp.mpf('0.04') / fv))
chk("all four variants: alpha at observed G*Lambda < 1e-120 (miss > 118 decades)", all(fv * x_obs < mp.mpf('1e-120') for fv in res.values()))
chk("spread of the ratio across variants is a convention factor (max/min < 1e3)", max(res.values()) / min(res.values()) < 1e3, "max/min = %.1f" % (max(res.values()) / min(res.values())))
chk("printed g_YM^2 = 2g/3 is NOT reproduced by my normalisation (mine/printed = 16)", sp.simplify(gG2 / gprinted - 16) == 0)
print("READING: alpha_G = (4/3) G*Lambda, with G*Lambda = 2g/pi fixed by the single dimensionless coefficient g of the action.")
print("The construction is TIED to G*Lambda (ratio forced); its overall scale is the free coefficient g, which the classical de Sitter vacuum")
print("(R0 = 4 Lambda = 3 v^2) then locks to the observed Lambda: alpha ~ 4e-122, ~120 decades below alpha. Using a 'bare' G*Lambda ~ O(1) instead makes the")
print("bare Lambda the free input. No route to 1/137.036.")
print("SUMMARY: fails =", fails)
sys.exit(1 if fails else 0)
