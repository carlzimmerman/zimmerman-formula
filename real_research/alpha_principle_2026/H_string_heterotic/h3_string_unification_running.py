#!/usr/bin/env python3
"""H3 -- string-scale gauge unification: one-loop MSSM running with Lambda tied to g_string (Kaplunovsky/Dienes), predictions of the low-energy couplings, threshold requirement, Thomson step.
Pre-registered S1-S6 in H0_PREREGISTRATION.md + Amendment 2.
Equation (Dienes Eq. 5.8, read): alpha_i^-1(m_Z) = k_i/alpha_G + (b_i/2 pi) ln(Lambda/m_Z) + Delta_i/(4 pi),  Lambda = 5.27e17 GeV * sqrt(4 pi alpha_G) (Kaplunovsky erratum Eq. 26, DR scheme).
levels k = (5/3, 1, 1), MSSM b = (11, 1, -3) in the Y/SU(2)/SU(3) normalisation (Y_eR = 1).  Inputs (MEASURED, not derived): m_Z, alpha_em^-1(m_Z)_MSbar, sin^2 theta_W, alpha_s, lepton masses.
WARNING (Amendment 2): a predicted alpha^-1 at m_Z near 137.0 is a coincidence at the WRONG SCALE; it is scored against 127.955, never against 137.036.
Run: python3 h3_string_unification_running.py [MUTATE]   (MUTATE: b_2 sign flipped; the baseline-sanity check S1a (predictions within 10 percent) must FAIL, exit 1)"""
import sys
import numpy as np
from math import pi, log, sqrt
from scipy.optimize import brentq

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
checks = []
def chk(name, ok, info=""):
    checks.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")

mZ = 91.1876; aem_inv = 127.955; s2w = 0.23122; a_s = 0.1179
AEM0_INV = 137.035999177
meas = np.array([(1 - s2w)*aem_inv, s2w*aem_inv, 1/a_s])       # alpha_Y^-1, alpha_2^-1, alpha_3^-1 at m_Z
k = np.array([5/3, 1.0, 1.0]); b = np.array([11.0, 1.0, -3.0])
if MUT: b = np.array([11.0, -1.0, -3.0])
LAM0 = 5.27e17

def ai(aG, D=np.zeros(3), mult=1.0):
    L = log(mult*LAM0*sqrt(4*pi*aG)/mZ)
    return k/aG + b*L/(2*pi) + D/(4*pi)
def derived(a):
    ae = a[0] + a[1]
    return ae, a[1]/ae, 1/a[2]          # alpha_em^-1, sin^2, alpha_s
def roots(f):
    xs = np.linspace(0.01, 0.5, 5000); v = [f(x) for x in xs]
    return [brentq(f, xs[i], xs[i+1]) for i in range(len(xs)-1) if v[i]*v[i+1] < 0]

D_dienes = np.array([11.6, 13.0, 7.0])          # Dienes Eq. 5.12 (read): two-loop + Yukawa + scheme conversion, model independent
variants = {"V1 one-loop, Delta=0": np.zeros(3), "V2 + Dienes 5.12 corrections": D_dienes}
inputs = {"alpha_em": lambda D: (lambda x: sum(ai(x, D)[:2]) - aem_inv),
          "sin2thW": lambda D: (lambda x: ai(x, D)[1]/(ai(x, D)[0] + ai(x, D)[1]) - s2w),
          "alpha_s": lambda D: (lambda x: ai(x, D)[2] - 1/a_s)}
meas_tuple = {"alpha_em^-1": aem_inv, "sin2thW": s2w, "alpha_s": a_s}

print("Measured at m_Z (inputs): alpha_em^-1 = %.3f, sin^2 theta_W = %.5f, alpha_s = %.4f;  alpha_Y^-1, alpha_2^-1, alpha_3^-1 = %s\n" % (aem_inv, s2w, a_s, np.round(meas, 3)))
ntr = 0; hits = []; table = {}
for vname, D in variants.items():
    print(f"--- {vname} ---")
    for iname, mk in inputs.items():
        rs = roots(mk(D))
        assert len(rs) == 1, (vname, iname, rs)
        aG = rs[0]
        ae, s2, asx = derived(ai(aG, D))
        pred = {"alpha_em^-1": ae, "sin2thW": s2, "alpha_s": asx}
        Lam = LAM0*sqrt(4*pi*aG)
        print(f"  input {iname:9s}: alpha_G^-1 = {1/aG:7.3f} (g_string = {sqrt(4*pi*aG):.3f}, Lambda = {Lam:.3e} GeV) -> predicted alpha_em^-1(m_Z) = {ae:8.3f}, sin^2 = {s2:.4f}, alpha_s = {asx:.4f}")
        for q, val in pred.items():
            if (iname == "alpha_em" and q == "alpha_em^-1") or (iname == "sin2thW" and q == "sin2thW") or (iname == "alpha_s" and q == "alpha_s"):
                continue
            ntr += 1
            rel = val/meas_tuple[q] - 1
            hit = abs(rel) < 1e-3
            if hit: hits.append((vname, iname, q))
            print(f"       prediction of {q:11s}: {val:.5f} vs measured {meas_tuple[q]:.5f}: offset {100*rel:+.2f}%   {'HIT' if hit else ''}")
        table[(vname, iname)] = (aG, ae, s2, asx)
print(f"\ntrial count S1+S2 = {ntr} predictions (declared 12); chance-hit probability per comparison 2e-3/ln10 = {2e-3/log(10):.2e}; expected chance hits = {ntr*2e-3/log(10):.4f}; hits = {hits}")
chk("S1/S2 trial count is the declared 12", ntr == 12)
maxoff = max(abs(v[1]/aem_inv - 1) for v in table.values())
chk("S1a baseline sanity: every alpha_em^-1(m_Z) prediction is within 10 percent of measured (the string relation is not wildly off)", all(abs(v[1]/aem_inv - 1) < 0.10 for v in table.values()), f"(max offset {100*maxoff:.1f}%)")
chk("S1b no prediction is within 1e-3 of the measured value (declared expectation)", len(hits) == 0)
v1as = table[("V1 one-loop, Delta=0", "alpha_s")]
print(f"   NOTE (Amendment 2): V1 alpha_s-input predicts alpha_em^-1(m_Z) = {v1as[1]:.3f}: numerically close to 137.036 but at m_Z, where the measured value is {aem_inv}: a {100*(v1as[1]/aem_inv-1):+.1f}% miss. Not a hit.")

# ---- S3: data count
print("\nS3 data count: unknowns (alpha_G, Delta_Y, Delta_2, Delta_3) = 4 vs 3 couplings.")
aG0 = v1as[0]
def F(vec):
    aG, dY, d2, d3 = vec
    return ai(aG, np.array([dY, d2, d3]))
x0 = np.array([aG0, 0, 0, 0]); eps = 1e-7
J = np.array([(F(x0 + eps*np.eye(4)[j]) - F(x0 - eps*np.eye(4)[j]))/(2*eps) for j in range(4)]).T
rank = np.linalg.matrix_rank(J, tol=1e-6)
print(f"   Jacobian (3x4) rank = {rank}: the map is onto; for ANY measured triple there is a one-parameter family of (alpha_G, Delta_i) that fits it exactly.")
chk("S3a Jacobian rank 3: thresholds absorb all three couplings", rank == 3)
print("   required thresholds (exact fit) as a function of g_string:")
best = None
for g in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2):
    aG = g*g/(4*pi)
    Dreq = 4*pi*(meas - ai(aG))
    mx = np.max(np.abs(Dreq))
    if best is None or mx < best[0]: best = (mx, g, Dreq)
    print(f"      g = {g:.1f}: Delta_Y, Delta_2, Delta_3 required = {np.round(Dreq, 1)}   (Delta_Y - Delta_2 = {Dreq[0]-Dreq[1]:+.1f}, Delta_2 - Delta_3 = {Dreq[1]-Dreq[2]:+.1f})")
gs = np.linspace(0.3, 1.5, 1201)
mxs = [np.max(np.abs(4*pi*(meas - ai(g*g/(4*pi))))) for g in gs]
gmin = gs[int(np.argmin(mxs))]
print(f"   minimum over g in [0.3,1.5] of max|Delta_i| required = {min(mxs):.2f} at g = {gmin:.3f}")
mxs2 = [np.max(np.abs(4*pi*(meas - ai(g*g/(4*pi), D_dienes)))) for g in gs]
print(f"   same with the Dienes 5.12 corrections already included as the base: minimum of max|Delta_i| = {min(mxs2):.2f} at g = {gs[int(np.argmin(mxs2))]:.3f}")
print("   Dienes (read, Sect. 6.5): explicit threshold calculations give |Delta| ~ O(1); the required sizes are O(10)-O(100) (his 6.16-6.18).  The three Delta are model/moduli dependent and NOT computed in this lane.")
chk("S3b the smallest achievable maximal threshold needed for an exact fit is >3 (i.e. larger than the O(1) explicit-calculation scale quoted by Dienes) at every g in [0.3,1.5]", min(mxs) > 3.0 and min(mxs2) > 3.0, f"(min {min(mxs):.2f}; with 5.12 base {min(mxs2):.2f}; the >3 cut is a descriptive marker, see Amendment 3)")

# ---- S4: Thomson step
print("\nS4 Thomson step (input: the measured SM low-energy shift, Amendment 2)")
SHIFT = AEM0_INV - aem_inv
me, mmu, mtau = 0.51099895e-3, 0.1056583755, 1.77686
lep = sum(log(mZ**2/m**2) for m in (me, mmu, mtau))/(3*pi)
Da_had = 0.02766            # RECALLED standard e+e- compilation value for Delta alpha_had^(5)(m_Z)
Nc_sumQ2_q = 3*(4/9 + 1/9 + 1/9 + 4/9 + 1/9)
had = AEM0_INV*Da_had + (5/3)*Nc_sumQ2_q/(3*pi)
print(f"   measured shift alpha^-1(0) - alpha^-1_MSbar(m_Z) = {SHIFT:.3f};  decomposition: one-loop leptons (measured masses) {lep:.3f} + hadronic (recalled Delta alpha_had, OS->MSbar) {had:.3f} = {lep+had:.3f}; residual {lep+had-SHIFT:+.3f} ({(lep+had-SHIFT)/aem_inv:+.1e} relative to alpha^-1(m_Z))")
chk("S4a the decomposition reproduces the measured shift to within 0.3 (W/top/scheme conventions; ~2e-3 of alpha^-1)", abs(lep + had - SHIFT) < 0.3)
print("   predicted alpha^-1(0) = alpha_em^-1_pred(m_Z) + measured shift, for each of the four alpha_em predictions that are not inputs:")
for (vname, iname), (aG, ae, s2, asx) in table.items():
    if iname == "alpha_em": continue
    a0 = ae + SHIFT
    print(f"      {vname:32s} input {iname:8s}: alpha^-1(0) = {a0:8.3f}  offset from 137.036: {100*(a0/AEM0_INV-1):+.2f}%   (alpha_G^-1 = {1/aG:.2f}; alpha_em^-1 at Lambda = {(8/3)/aG:.1f}, i.e. (3/8) alpha_G)")
chk("S4b no Thomson-limit prediction within 1e-3 of 137.036 (declared expectation)", all(abs((ae + SHIFT)/AEM0_INV - 1) > 1e-3 for (vn, inn), (aG, ae, s2, asx) in table.items() if inn != "alpha_em"))

# ---- S5: requirement statement
aGs = v1as[0]
h = 1e-6
dae = (sum(ai(aGs*(1 + h))[:2]) - sum(ai(aGs*(1 - h))[:2]))/(2*h*aGs)           # d alpha_em^-1(mZ)/d alpha_G  with Lambda(alpha_G) tied
d_inv = dae*(-aGs**2)                                                          # d alpha_em^-1 / d alpha_G^-1
tol = 1e-3*AEM0_INV
print(f"\nS5 sensitivity at the V1 alpha_s-input solution: d alpha_em^-1(m_Z)/d alpha_G^-1 = {d_inv:.3f}; to hold alpha(0) to 1e-3 (= {tol:.3f} in alpha^-1) alpha_G^-1 must be known to +-{tol/abs(d_inv):.3f}")
print(f"   versus a threshold budget: one unit of Delta_Y+Delta_2 shifts alpha_em^-1(m_Z) by 1/(4 pi) = {1/(4*pi):.4f}; the 1e-3 window is {tol/(1/(4*pi)):.2f} units of Delta_Y+Delta_2 (the Dienes 5.12 corrections alone are {D_dienes[0]+D_dienes[1]:.1f} units)")
chk("S5 the 1e-3 window in alpha(0) is smaller than the known model-independent correction (5.12) by >10x, so 1e-3 cannot be scored without a full two-loop + scheme + threshold calculation", tol/(1/(4*pi)) < (D_dienes[0] + D_dienes[1])/10)

# ---- S6: convention sensitivity
print("\nS6 convention sensitivity (R2): scaling Lambda by sqrt(2) or 2 (Witten vs Kaplunovsky, Dienes vs Kaplunovsky) at fixed alpha_G:")
sh = {}
for mult in (2**0.5, 2.0):
    dl = sum(ai(aGs, mult=mult)[:2]) - sum(ai(aGs, mult=1.0)[:2])
    sh[mult] = dl
    print(f"   Lambda x {mult:.4f}: alpha_em^-1(m_Z) shifts by {dl:+.3f} ({100*dl/aem_inv:+.2f}%)")
chk("S6 the convention uncertainty shifts alpha_em^-1(m_Z) by more than the 1e-3 window (so the tree-level relation cannot be scored at 1e-3 until a convention/scheme is fixed by a full derivation)", min(abs(v) for v in sh.values()) > 1e-3*aem_inv)

nfail = sum(1 for _, ok in checks if not ok)
print(f"\nSUMMARY: {len(checks)-nfail}/{len(checks)} checks pass" + (" [MUTATE]" if MUT else ""))
sys.exit(1 if nfail else 0)
