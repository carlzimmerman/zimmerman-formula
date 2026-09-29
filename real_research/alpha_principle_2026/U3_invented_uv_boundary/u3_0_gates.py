#!/usr/bin/env python3
"""u3_0 -- gates of lane U3 (pre-registered in U3_PREREGISTRATION.md): the machinery reproduces the committed numbers before any principle is scored.

G1 b's from the SM field content (Fractions): b_Y = 41/6, b_2 = -19/6, b_3 = -7, b_Y = (5/3) b_1.       G2 one-loop 1/alpha_Y(M_P) = 55.48, 1/alpha_2(M_P) = 49.46, 1/alpha_em(M_P) = 104.94 (lane B's rg_common as independent check).
G3 two-loop shift of 1/alpha_em(M_P) within 0.4-1.0%.   G4 this runner reproduces N1's Runner (2L-A) and rg_common (1L-A); the top-threshold central differs from 2L-A by less than the 1% floor.
G5 input-error floor: alpha_s +-0.0009, 1/alpha_em +-0.008, sin^2 +-0.00005 move every a_i(X_P) by < 0.5% (the 1% floor of the tolerance is not eaten by input errors).
G6 multiplet coefficients (Fractions) and the N1 cross-check (one unit-Y Dirac fermion at 1 TeV moves 1/alpha_Y(M_P) by -12.7%).   G7 the H_Lambda decoupling (no charged state below mu = H).
G8 group numbers from the SM content: dual Coxeter numbers of SU(3), SU(2) from the gauge part of b; Dynkin sums I_3 = I_2 = 6, I_Y = 10.   G9 the crossing solver against the closed-form one-loop crossing; the three SM crossing scales.
Run:    python3 u3_0_gates.py            (real run, exit 0 iff every gate passes)
MUTATE: python3 u3_0_gates.py --mutate   (control: the lane-A bug b_Y = (3/5) b_1 is put into G1 and G2; exactly G1 and G2 must FAIL -> exit 1; any other outcome -> exit 3, the control is broken)
"""
import sys
sys.dont_write_bytecode = True
import math
from fractions import Fraction as Fr
import numpy as np
import u3_lib as L

MUT = "--mutate" in sys.argv
FAILED = []
NCHK = []


def chk(tag, ok, detail=""):
    NCHK.append(tag)
    if not ok:
        FAILED.append(tag.split()[0])
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


print("=" * 100)
print("U3-0 gates -- mode: " + ("MUTATE CONTROL (b_Y = 3/5 b_1 in G1, G2)" if MUT else "REAL RUN"))
print("=" * 100)

# G1
bY, b2, b3, b1 = L.N1.sm_coefficients(MUT)
print(f"\nG1  b from the SM content: b_Y = {bY}, b_2 = {b2}, b_3 = {b3}, b_1 = {b1}")
chk("G1 b = (41/6, -19/6, -7) and b_Y = (5/3) b_1", (bY, b2, b3) == (Fr(41, 6), Fr(-19, 6), Fr(-7)) and bY == Fr(5, 3) * b1)

# G2
t1 = L.Traj("1L-A", mutate_b=MUT)
A = t1.A(L.XP)
ref = L.RGC.run_oneloop(L.XP)
print(f"\nG2  one loop at M_P: this runner a_Y, a_2, a_3 = {A[0]:.3f}, {A[1]:.3f}, {A[2]:.3f}; rg_common = {ref[0]:.3f}, {ref[1]:.3f}, {ref[2]:.3f}; a_em = {A[0] + A[1]:.3f}")
chk("G2 1/alpha_Y(M_P) = 55.48, 1/alpha_2(M_P) = 49.46, 1/alpha_em(M_P) = 104.94 (lanes B, M, N1) and equals rg_common to 1e-9",
    abs(A[0] - 55.48) < 0.05 and abs(A[1] - 49.46) < 0.05 and abs(A[0] + A[1] - 104.94) < 0.05 and np.allclose(A, ref, atol=1e-9))

# everything below uses the unmutated runner
t1u = L.get_traj("1L-A")
t2A = L.get_traj("2L-A")
t2T = L.get_traj("2L-T")
tT1 = L.get_traj("1L-T")

# G3
a1L = t1u.A(L.XP)
a2L = t2A.A(L.XP)
shift = (a2L[0] + a2L[1]) / (a1L[0] + a1L[1]) - 1
print(f"\nG3  two loop (2L-A) at M_P: a_Y, a_2, a_3 = {a2L[0]:.3f}, {a2L[1]:.3f}, {a2L[2]:.3f}; a_em shift vs one loop {shift:+.3%}")
chk("G3 two-loop shift of 1/alpha_em(M_P) within 0.4-1.0% (lane M: 0.67%)", 0.004 <= abs(shift) <= 0.010, f"(got {shift:+.3%})")

# G4
r_n1 = L.N1.Runner().twoloop(L.XP, L.SET_A)
print(f"\nG4  N1 Runner 2L-A at M_P: {r_n1[0]:.4f}, {r_n1[1]:.4f}, {r_n1[2]:.4f}; this runner 2L-A: {a2L[0]:.4f}, {a2L[1]:.4f}, {a2L[2]:.4f}")
cT = t2T.A(L.XP)
thr = np.max(np.abs(cT / a2L - 1))
print(f"    central 2L-T (top threshold) at M_P: {cT[0]:.4f}, {cT[1]:.4f}, {cT[2]:.4f}; largest relative difference to 2L-A: {thr:.3%}")
chk("G4 this runner's 2L-A equals N1's Runner.twoloop to 1e-4 (relative)", np.allclose(a2L, r_n1, rtol=1e-4))
chk("G4b the top-threshold central differs from 2L-A by less than the 1% floor", thr < 0.01, f"({thr:.3%})")

# G5
def shifted_inputs(dinv=0.0, ds2=0.0, dals=0.0):
    return dict(alpha_inv=127.930 + dinv, s2w=0.23122 + ds2, alpha_s=0.1180 + dals)
worst = 0.0
for kw in (dict(dinv=0.008), dict(dinv=-0.008), dict(ds2=0.00005), dict(ds2=-0.00005), dict(dals=0.0009), dict(dals=-0.0009)):
    tt = L.Traj("2L-T", inp=shifted_inputs(**kw))
    a = tt.A(L.XP)
    worst = max(worst, float(np.max(np.abs(a / cT - 1))))
print(f"\nG5  largest relative shift of any a_i(M_P) under 1-sigma input variations (declared sigmas): {worst:.3%}")
chk("G5 input errors move every a_i(X_P) by < 0.5% (the 1% tolerance floor is not eaten by inputs)", worst < 0.005, f"({worst:.3%})")

# G6
Y = lambda dim, y: Fr(2, 3) * dim * y * y
dbY = 2 * Y(1, 1)                                    # Dirac singlet with Y = 1 = 2 Weyl
db2 = 2 * Fr(2, 3) * Fr(1, 2)                        # vector-like SU(2) doublet: two Weyl doublets, index 1/2
db3 = 2 * Fr(2, 3) * Fr(1, 2)
top_Y = Fr(2, 3) * (3 * Fr(1, 36) + 3 * Fr(4, 9))
print(f"\nG6  Delta b (Y=1 Dirac singlet, SU(2) VL doublet, colour VL triplet) = ({dbY}, {db2}, {db3}); top removal Delta b_Y = {top_Y}")
chk("G6a multiplet coefficients equal the lib's (4/3, 2/3, 2/3) and the top's Delta b_Y = 17/18",
    (float(dbY), float(db2), float(db3)) == tuple(L.DB_MULT) and abs(float(top_Y) - L.DB_TOP[0]) < 1e-15)
sh1 = float(dbY) / (2 * math.pi) * math.log(L.XP / L.TEV) / a1L[0]
mu_c = L.N1.Runner().alpha2_selfconsistent_mu()          # N1's map-A scale, where its -12.7% was quoted (Amendment 2: NOT M_P)
sh_c = float(dbY) / (2 * math.pi) * math.log(mu_c / L.TEV) / L.N1.Runner().run(mu_c)[0]
print(f"    one unit-Y Dirac fermion at 1 TeV lowers a_Y by {sh_c:.2%} at N1's mu_c = {mu_c:.3e} GeV (N1: 12.7%) and by {sh1:.2%} at M_P (one loop)")
chk("G6b N1 cross-check: -12.7% for one unit-Y Dirac fermion at 1 TeV, at N1's own scale mu_c", abs(sh_c - 0.127) < 0.003)

# G7
H0_eV = 67.4e3 / 3.0856775814913673e22 * 6.582119569e-16
H_eV = H0_eV * math.sqrt(0.685)
me_eV = 0.51099895e6
masses_eV = [0.51099895e6, 105.6583755e6, 1776.86e6]
n_below = sum(1 for m in masses_eV if m < H_eV)
print(f"\nG7  H_Lambda = {H_eV:.3e} eV; m_e / H_Lambda = {me_eV / H_eV:.3e}; charged states lighter than H_Lambda: {n_below}")
chk("G7 no charged state lies below H_Lambda (m_e/H > 1e30), so d(1/alpha_em)/d ln mu = 0 for mu < m_e and a rule at H_Lambda is a rule at m_e", me_eV / H_eV > 1e30 and n_below == 0)

# G8
weyl = [(3, 2, Fr(1, 6)), (3, 1, Fr(-2, 3)), (3, 1, Fr(1, 3)), (1, 2, Fr(-1, 2)), (1, 1, Fr(1))]
T3 = lambda d3: Fr(1, 2) if d3 == 3 else Fr(0)
T2 = lambda d2: Fr(1, 2) if d2 == 2 else Fr(0)
I3 = 3 * sum(T3(d3) * d2 for d3, d2, y in weyl)
I2 = 3 * sum(T2(d2) * d3 for d3, d2, y in weyl)
IY = 3 * sum(d3 * d2 * y * y for d3, d2, y in weyl)
gauge3 = -Fr(11) ; gauge2 = -Fr(22, 3)
h3, h2 = -gauge3 * Fr(3, 11), -gauge2 * Fr(3, 11)
print(f"\nG8  Dynkin sums over 3 generations: I_3 = {I3}, I_2 = {I2}, I_Y = {IY};  dual Coxeter from the gauge part -11 h/3: h(SU(3)) = {h3}, h(SU(2)) = {h2}")
chk("G8 I_3 = 6, I_2 = 6, I_Y = 10 and h(SU(3)) = 3, h(SU(2)) = 2", (I3, I2, IY) == (6, 6, 10) and (h3, h2) == (3, 2))

# G9
class _Sh:
    lnmax = math.log(1e40)
    def __init__(self, t): self.t = t
    def A(self, mu): return self.t.A(mu)
sh = _Sh(t1u)
x12 = L.solve_cross(sh, "a1", "a2")
# closed form: a1(mu) = 0.6 aY0 - 0.6 bY/(2pi) ln, a2 = a20 - b2/(2pi) ln
aY0, a20, a30 = L.boundaries(L.SET_A)
ln12 = (0.6 * aY0 - a20) / ((0.6 * L.B_SM[0] - L.B_SM[1]) / (2 * math.pi))
x12c = L.MZ * math.exp(ln12)
x23 = L.solve_cross(sh, "a2", "a3")
xY2 = L.solve_cross(sh, "aY", "a2")
xY3 = L.solve_cross(sh, "aY", "a3")
a3_at = t1u.A(x12)[2]; a2_at = t1u.A(x12)[1]
print(f"\nG9  one-loop crossings (SM desert, set A): a_1=a_2 at {x12:.3e} GeV (closed form {x12c:.3e}); a_2=a_3 at {x23:.3e}; a_Y=a_2 at {xY2:.3e}; a_Y=a_3 at {xY3:.3e}")
print(f"    at the GUT-norm crossing a_3 / a_2 - 1 = {a3_at / a2_at - 1:+.3%} (N1: alpha_3 off by -13%, i.e. a_3 higher)")
chk("G9a numeric crossing equals the closed form to 1e-6", abs(x12 / x12c - 1) < 1e-6)
chk("G9b SM crossing scales as expected: a_1=a_2 ~1e13 (within a decade), a_2=a_3 ~1e17, a_Y=a_2 beyond M_P", 1e12 < x12 < 1e14 and 3e16 < x23 < 3e17 and xY2 > L.XP)

print("\nFAILED:", FAILED if FAILED else "none")
if MUT:
    works = sorted(FAILED) == ["G1", "G2"]
    print("MUTATE CONTROL:", "works (exactly G1 and G2 failed) -> exit 1" if works else "CONTROL BROKEN (exit 3): exactly G1 and G2 must fail")
    sys.exit(1 if works else 3)
sys.exit(0 if not FAILED else 1)
