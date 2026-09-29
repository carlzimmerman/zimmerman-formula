#!/usr/bin/env python3
"""x1_0_gates -- gates of lane X1 (pre-registered G1-G8 in X1_PREREGISTRATION.md).  Nothing physical is decided here: this script checks the machinery against
independent known results BEFORE any pair is scored.
Run (real):    PYTHONDONTWRITEBYTECODE=1 python3 x1_0_gates.py           -> exit 0 if every gate passes (2 otherwise)
Run (control): PYTHONDONTWRITEBYTECODE=1 python3 x1_0_gates.py MUTATE    -> the lane-A bug b_Y = (3/5)(3/5)(41/6) is injected; G1 and G2 (and G8) must FAIL; exit 1 if the control bites, 3 if it does not.
G1  SM (b, B) rebuilt from the field content by the general formula equal lane N1's recalled matrices (converted to the Y normalisation) and the Yukawa vector
G2  my runner reproduces lane U3's central 2L-T and the six other variants for the SM at seven scales
G3  E6 exotic set: (Delta b_Y, Delta b_2, Delta b_3) = (10/9, 2/3, 2/3); complete-SU(5)-multiplet one-loop invariance of (a_1 - a_2, a_3 - a_2)
G4  threshold bookkeeping vs a one-loop closed form
G5  the general two-loop formula reproduces the MSSM matrices (independent published numbers, recalled) -- validates gaugino / scalar / adjoint terms
G6  T-ABS translation vs an exact one-loop shift
G7  the decoupled limit equals the desert; G8 lane U3's quoted residuals are reproduced.
Needs ../{B_rg_asymptotic_safety,N1_joint_couplings,U3_invented_uv_boundary,D_calibration_bar} (read only).  Writes nothing.
"""
import sys
sys.dont_write_bytecode = True
import math
from fractions import Fraction as Fr
import numpy as np
import x1_lib as L

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
chk = L.Checks(MUT)
print("=" * 100)
print("X1-0 gates -- mode:", "MUTATE (control)" if MUT else "REAL RUN")
print("=" * 100)

# ---------------------------------------------------------------- G1
b_ex, B_ex = L.sm_bB_exact()
if MUT:
    b_ex = [Fr(3, 5) * Fr(3, 5) * Fr(41, 6), b_ex[1], b_ex[2]]
chk("G1a one-loop b = (41/6, -19/6, -7) from the SM field content", b_ex == [Fr(41, 6), Fr(-19, 6), Fr(-7)], str([str(x) for x in b_ex]))
B2 = np.array(N1_B := L.N1.B2L)      # lane N1's GUT-normalised matrix (recalled there)
conv = np.array([[25 / 9 * B2[0, 0], 5 / 3 * B2[0, 1], 5 / 3 * B2[0, 2]], [5 / 3 * B2[1, 0], B2[1, 1], B2[1, 2]], [5 / 3 * B2[2, 0], B2[2, 1], B2[2, 2]]])
Bf = np.array([[float(x) for x in r] for r in B_ex])
chk("G1b two-loop matrix B (Y normalisation) from the field content equals N1's matrix converted [(25/9) B11, (5/3) B12, (5/3) B13; (5/3) B21, B22, B23; (5/3) B31, B32, B33]", np.max(np.abs(Bf - conv)) < 1e-12, f"max diff {np.max(np.abs(Bf - conv)):.2e}")
chk("G1c the Y-normalisation entries are 199/18, 9/2, 44/3 / 3/2, 35/6, 12 / 11/6, 9/2, -26", [str(B_ex[0][0]), str(B_ex[0][1]), str(B_ex[0][2]), str(B_ex[1][0]), str(B_ex[1][1]), str(B_ex[1][2]), str(B_ex[2][0]), str(B_ex[2][1]), str(B_ex[2][2])] == ["199/18", "9/2", "44/3", "3/2", "35/6", "12", "11/6", "9/2", "-26"])
chk("G1d the Yukawa vector (Y normalisation) is (17/6, 3/2, 2) = (5/3 x 17/10, 3/2, 2) from N1's C2L", np.max(np.abs(L.CY_TOP - np.array([17 / 6, 3 / 2, 2.0]))) < 1e-12 and np.max(np.abs(np.array([5 / 3, 1, 1]) * L.N1.C2L - L.CY_TOP)) < 1e-12)

# ---------------------------------------------------------------- G10 (right-hand side against N1's)
rng = np.random.default_rng(7)
R0 = L.N1.Runner()
worst = 0.0
for _ in range(20):
    y = np.array([rng.uniform(40, 60), rng.uniform(25, 50), rng.uniform(20, 55), rng.uniform(0.3, 1.0)])
    mine = L.Run("2L-A")._rhs_factory(L.B_SM_F, L.BM_SM_F, True)(0.0, y)
    ref = R0._rhs(0.0, y)
    worst = max(worst, max(abs(a - b) for a, b in zip(mine, ref)))
chk("G1e my right-hand side (b, B, C, top Yukawa) equals lane N1's Runner._rhs at 20 random states", worst < 1e-12, f"worst abs diff {worst:.2e}")

# ---------------------------------------------------------------- G2
scales = [1e3, 1e6, 1e10, 1e13, 1e16, 1e18, L.XP]
worst2, worst1 = 0.0, 0.0
rows = []
for nm in L.VARIANTS:
    mine = L.Run(nm, (), mutate_b=MUT)
    u3 = L.U3.get_traj(nm)
    for mu in scales:
        a, b = mine.A(mu), u3.A(mu)
        rel = float(np.max(np.abs(a / b - 1)))
        if nm.startswith("2L"):
            worst2 = max(worst2, rel)
        else:
            worst1 = max(worst1, rel)
chk("G2a two-loop variants (2L-T, 2L-A, 2L-B, 2L-TB): my runner equals lane U3's trajectories at 7 scales to 1e-6 (relative)", worst2 < 1e-6, f"worst {worst2:.2e}")
chk("G2b one-loop variants (1L-T, 1L-A, 1L-B): equal to 1e-9", worst1 < 1e-9, f"worst {worst1:.2e}")

# ---------------------------------------------------------------- G3
db, dB = L.contrib("w", 3, 1, Fr(-1, 3))
db2, _ = L.contrib("w", 3, 1, Fr(1, 3))
dbh1, _ = L.contrib("w", 1, 2, Fr(1, 2))
dbh2, _ = L.contrib("w", 1, 2, Fr(-1, 2))
tot = [db[i] + db2[i] + dbh1[i] + dbh2[i] for i in range(3)]
chk("G3a one E6 exotic set (D, D^c, two doublets; S neutral) shifts (b_Y, b_2, b_3) by (10/9, 2/3, 2/3) (lane W1 K4b)", tot == [Fr(10, 9), Fr(2, 3), Fr(2, 3)], str([str(x) for x in tot]))
X15 = 1e15
de = L.desert("1L-T")
ex_deg = L.Run("1L-T", L.exotics_e6(1e5, 1e5, 3))
Ad, Ae = de.A(X15), ex_deg.A(X15)
inv_d = np.array([0.6 * Ad[0] - Ad[1], Ad[2] - Ad[1]])
inv_e = np.array([0.6 * Ae[0] - Ae[1], Ae[2] - Ae[1]])
chk("G3b complete-SU(5)-multiplet one-loop invariance: with M_D = M_H the differences (a_1 - a_2, a_3 - a_2) are unchanged to 1e-9 while each a_i moves by the same amount", np.max(np.abs(inv_d - inv_e)) < 1e-9 and abs(Ae[1] - Ad[1]) > 1.0,
    f"(differences {inv_d} vs {inv_e}; a_2 moved by {Ae[1] - Ad[1]:+.3f})")
Asp = L.Run("1L-T", L.exotics_e6(1e5, 1e10, 3)).A(X15)
inv_s = np.array([0.6 * Asp[0] - Asp[1], Asp[2] - Asp[1]])
chk("G3c split masses (M_D != M_H) do change the differences (the only way an exotic set can act on the ratio tests)", np.max(np.abs(inv_s - inv_d)) > 0.5, f"(change {np.max(np.abs(inv_s - inv_d)):.3f})")

# ---------------------------------------------------------------- G4
M_ex, Xt = 3.0e4, 1.0e12
ex1 = [(M_ex, "w", 3, 1, Fr(-1, 3), 2)]
r1 = L.Run("1L-T", ex1)
dbx = np.array([float(2 * x) for x in L.contrib("w", 3, 1, Fr(-1, 3))[0]])
closed = de.A(Xt) - dbx / L.TWO_PI * math.log(Xt / M_ex)
chk("G4 threshold bookkeeping: 2 copies of D at 30 TeV, one loop: a_i(1e12) = desert - Delta b_i/(2 pi) ln(X/M) to 1e-9", np.max(np.abs(r1.A(Xt) - closed)) < 1e-9, f"(diff {np.max(np.abs(r1.A(Xt) - closed)):.2e})")

# ---------------------------------------------------------------- G5  MSSM (independent published numbers, RECALLED: Martin-Vaughn)
acc = [list(L.gauge_bB()[0]), [list(r) for r in L.gauge_bB()[1]]]
# gauginos: adjoint Weyl of SU(3), SU(2) (hypercharge gaugino is a neutral singlet, contributes nothing)
for (d3, d2, Y) in ((8, 1, 0), (1, 3, 0)):
    dbg, dBg = L.contrib("w", d3, d2, Y)
    L.add_bB(acc, dbg, dBg, 1)
raw = None
chiral = [(d3, d2, Y, 3) for (d3, d2, Y) in L.SM_GEN[:5]] + [(1, 2, Fr(1, 2), 1), (1, 2, Fr(-1, 2), 1)]      # quark/lepton multiplets x 3 generations; two Higgs doublets
for (d3, d2, Y, mult) in chiral:
    L.add_bB(acc, *L.contrib("w", d3, d2, Y), mult)      # fermion (higgsino for the Higgs multiplets)
    L.add_bB(acc, *L.contrib("s", d3, d2, Y), mult)      # scalar (sfermion / Higgs)
bM = acc[0]
BM_raw = np.array([[float(x) for x in r] for r in acc[1]])
# Amendment A2: the SUSY gaugino-matter coupling is a gauge-Yukawa term that the non-supersymmetric formula does not contain; per chiral multiplet it is -T_i (2 C_j + 2 C_A(i) delta_ij)
for (d3, d2, Y, mult) in chiral:
    T = (Y * Y * d3 * d2, L.T2TAB[d2] * d3, L.T3TAB[d3] * d2)
    C = (Y * Y, L.C2TAB[d2], L.C3TAB[d3])
    for i in range(3):
        for j in range(3):
            acc[1][i][j] -= mult * T[i] * (2 * C[j] + (2 * L.CA[i] if i == j else 0))
BM = np.array([[float(x) for x in r] for r in acc[1]])
mssm_gut = np.array([[199 / 25, 27 / 5, 88 / 5], [9 / 5, 25, 24], [11 / 5, 9, 14]])
mssm_Y = np.array([[25 / 9 * mssm_gut[0, 0], 5 / 3 * mssm_gut[0, 1], 5 / 3 * mssm_gut[0, 2]], [5 / 3 * mssm_gut[1, 0], mssm_gut[1, 1], mssm_gut[1, 2]], [5 / 3 * mssm_gut[2, 0], mssm_gut[2, 1], mssm_gut[2, 2]]])
chk("G5a MSSM one-loop b (Y normalisation) = (11, 1, -3) from gauge + gauginos + 3 generations of fermions and sfermions + 2 Higgs doublets + 2 higgsinos", bM == [Fr(11), Fr(1), Fr(-3)], str([str(x) for x in bM]))
chk("G5b (AMENDED, A2) MSSM two-loop matrix: the general formula plus the SUSY gaugino-Yukawa term equals the published (199/25, 27/5, 88/5; 9/5, 25, 24; 11/5, 9, 14) converted to the Y normalisation, ALL nine entries", np.max(np.abs(BM - mssm_Y)) < 1e-12, f"max diff {np.max(np.abs(BM - mssm_Y)):.2e}; raw difference before the SUSY term: B_33 off by {BM_raw[2, 2] - mssm_Y[2, 2]:+.1f}")

# ---------------------------------------------------------------- G6
rule = L.make_rule("RD", X=L.XP, xtag="X_P", s1=True)
run1 = L.Run("1L-T", ())
res = L.residuals(rule, run1, L.desert("1L-T"))
delta = res["pred"] - res["A"]
shifted = L.Run("1L-T", (), a0=run1.a0 + delta)
chk("G6a one loop: shifting the m_Z couplings by (pred - A(X)) lands EXACTLY on the rule's values at X (the T-ABS translation is exact at one loop)", np.max(np.abs(shifted.A(L.XP) - res["pred"])) < 1e-9)
run2 = L.Run("2L-T", ())
res2 = L.residuals(rule, run2, L.desert("2L-T"))
pred3 = res2["A"] * 1.03                      # Amendment A3: a 3% shift (the dual-Coxeter shift is ~50% and drives a_3(m_Z) negative, where a two-loop translation is meaningless)
sh2 = L.Run("2L-T", (), a0=run2.a0 + (pred3 - res2["A"]))
dev = float(np.max(np.abs(sh2.A(L.XP) - pred3) / pred3))
chk("G6b (AMENDED, A3) two loop, 3% shift: the translation is off by less than 1e-2 relative (the departure is reported)", dev < 1e-2, f"(relative departure {dev:.2e})")

# ---------------------------------------------------------------- G7
far = L.Run("2L-T", L.exotics_e6(1e25, 1e25, 3))
chk("G7a exotics above the integrated range leave the run identical to the desert", np.max(np.abs(far.A(L.XP) - L.desert("2L-T").A(L.XP))) < 1e-9)
near = L.Run("2L-T", L.exotics_e6(0.5 * L.XP, 0.5 * L.XP, 3))
shift_expect = 3 * (10 / 9) / L.TWO_PI * math.log(2.0)
shift_got = float(L.desert("2L-T").A(L.XP)[0] - near.A(L.XP)[0])
chk("G7b exotics at X/2 move a_Y(X) by Delta b_Y/(2 pi) ln 2 (one-loop estimate within 1%)", abs(shift_got / shift_expect - 1) < 0.01, f"(got {shift_got:.4f}, expect {shift_expect:.4f})")

# ---------------------------------------------------------------- G8
d2 = L.desert("2L-T")
if MUT:
    d2 = L.Run("2L-T", (), mutate_b=True)
rB = L.make_rule("RB", xtag="cross")
resB = L.residuals(rB, d2, d2)
chk("G8a lane U3 V03: the a_1 = a_2 crossing is at 1.091e13 GeV and a_3/a_2 residual is +0.131", abs(resB["X"] / 1.091e13 - 1) < 3e-3 and abs(resB["r"][0] - 0.131) < 2e-3, f"(X = {resB['X']:.4e}, r = {resB['r'][0]:+.4f})")
rA = L.make_rule("RA", X=L.XP, xtag="X_P")
resA = L.residuals(rA, d2, d2)
chk("G8b lane U3 V06: GUT-normalised equal couplings at X_P: residuals (+0.486, -0.071)", abs(resA["r"][0] - 0.486) < 2e-3 and abs(resA["r"][1] + 0.071) < 2e-3, f"({resA['r'][0]:+.4f}, {resA['r'][1]:+.4f})")
rD = L.make_rule("RD", X=L.XP, xtag="X_P", s1=True)
resD = L.residuals(rD, d2, d2)
chk("G8c lane U3 V01: dual-Coxeter absolute at X_P: residuals (+0.898, -0.489, -0.288)", np.max(np.abs(resD["r"] - np.array([0.898, -0.489, -0.288]))) < 3e-3, str(np.round(resD["r"], 4)))
rE = L.make_rule("RE", xtag="het")
resE = L.residuals(rE, d2, d2)
chk("G8d lane U3 V34: heterotic locking X = 2.711e17 GeV, residuals (+0.329, -0.029)", abs(resE["X"] / 2.711e17 - 1) < 3e-3 and abs(resE["r"][0] - 0.329) < 3e-3 and abs(resE["r"][1] + 0.029) < 3e-3, f"(X = {resE['X']:.4e}, r = {np.round(resE['r'], 4)})")

chk.finish("X1-0")
