"""Lane B, script 3: counted trials -- does any forced fixed-point value of the AS literature give alpha^-1 = 137.036 or the required boundary value?
Usage: python3 b3_forced_vs_required.py [MUTATE]  (MUTATE promotes the tuned control C6 into the counted trials; the 'no hit' verdict must FAIL)."""
import sys
import numpy as np
from scipy.optimize import fsolve, brentq
from rg_common import *

MUT = "MUTATE" in sys.argv
fails = []
def chk(tag, ok, msg):
    print(("  [PASS] " if ok else "  [FAIL] ") + tag + "  " + msg)
    if not ok:
        fails.append(tag)
print("MODE:", "MUTATE (tuned control C6 counted as a trial)" if MUT else "NORMAL")

TARGET = ALPHA_INV0
HIT = 1e-3
trials = []   # (label, predicted alpha^-1, target, forced?)
def add(label, pred, tgt, note):
    rel = pred / tgt - 1
    hit = abs(rel) < HIT
    trials.append((label, pred, tgt, rel, hit))
    print(f"    {label:28s} predicted {pred:12.5f}  target {tgt:12.5f}  rel {rel:+.4e}  {'HIT' if hit else 'no hit'}   [{note}]")

# ---- HR
B1 = -(24 * 0.5 - 1.0) / (3 * np.pi)
g1 = -2 / B1
def hr_toy(gstar, nF=1):
    return hr_run([(0.000510999, 2 * nF / (3 * np.pi))], gstar, 1.0)
def hr_sm(setno, gstar):
    th = [(m, 2 * ncq2 / (3 * np.pi)) for nm, m, ncq2 in fermions(setno)]
    return hr_run(th, gstar, 1.0, k_end=0.000510999)

print("Counted trials (8): predicted alpha_IR^-1 vs 137.035999177, and fixed-point boundary values vs the required boundary value at M_Planck")
print("\n  --- predictions of the IR value (5) ---")
add("C1 HR toy n_F=1 g*=1.7136", hr_toy(g1), TARGET, "one charged species, gravity FP")
add("C2 HR toy n_F=1 g*=0.83", hr_toy(0.83), TARGET, "quoted g* at lambda*")
c3 = hr_sm(1, g1); c4 = hr_sm(2, g1)
add("C3 HR + SM fermions SET(i)", c3, TARGET, "U(1)_em toy, 9 fermions, MSbar-type light masses")
add("C4 HR + SM fermions SET(ii)", c4, TARGET, "same, constituent light quarks")

# ---- EV chain
ND, NS, NV = 22.5, 4.0, 12.0
def betas(x):
    G, L = x
    d = 1 - 2 * L
    bG = 2 * G + G**2 / (6 * np.pi) * (2 * ND + NS - 4 * NV) - G**2 / (6 * np.pi) * (14 + 6 / d + 9 / d**2)
    bL = (-2 * L + G / (4 * np.pi) * (NS - 4 * ND + 2 * NV) + G * L / (6 * np.pi) * (2 * ND + NS - 4 * NV)
          - 3 * G / (2 * np.pi) - 7 * G * L / (3 * np.pi) - 3 * G / (4 * np.pi * d**2) + 7 * G / (4 * np.pi * d))
    return [bG, bL]
Gs, Ls = fsolve(betas, [2.7, -3.8], xtol=1e-13)
fg = Gs * (1 - 4 * Ls) / (4 * np.pi * (1 - 2 * Ls)**2)
gY_star = 4 * np.pi * np.sqrt(6 * fg / 41)
bY = 41 / 6
def aY_inv_at(k, gstar):
    return 4 * np.pi * (1 / gstar**2 + bY / (8 * np.pi**2) * np.log(MPL / k))
aY_mz_pred = aY_inv_at(MZ, gY_star)
a2_mz = ALPHA_INV_MZ * S2W          # MEASURED
c5 = aY_mz_pred + a2_mz + DELTA_0_MZ
add("C5 EV FP + measured alpha_2", c5, TARGET, f"f_g={fg:.4f}, g_Y*={gY_star:.4f}; alpha_2 and the 0->M_Z offset are MEASURED inputs")

print("\n  --- boundary comparisons at M_Planck (3) ---")
aY_req, a2_req, a3_req = run_oneloop(MPL)
aem_req = aY_req + a2_req
print(f"    required at M_Planck (SM one-loop from measured alpha(M_Z)): alpha_Y^-1 = {aY_req:.3f}, alpha_em^-1 = {aem_req:.3f}")
add("B1 HR alpha* (n_F=1,g*=1.7136)", 1 / (9 * g1), aem_req, "fixed-point alpha*^-1 vs required alpha_em^-1(M_Pl)")
add("B2 HR alpha* (n_F=1,g*=0.83)", 1 / (9 * 0.83), aem_req, "same")
add("B3 EV alpha_Y*^-1", 4 * np.pi / gY_star**2, aY_req, "fixed-point alpha_Y*^-1 vs required alpha_Y^-1(M_Pl)")

# ---- tuned control (NOT a trial unless MUTATE)
print("\n  --- control C6 (tuned after seeing the target; not a forced value) ---")
aY_needed = TARGET - DELTA_0_MZ - a2_mz
gstar_needed = 1 / np.sqrt(aY_needed / (4 * np.pi) - bY / (8 * np.pi**2) * np.log(MPL / MZ))
f_needed = bY * gstar_needed**2 / (16 * np.pi**2)
c6 = aY_inv_at(MZ, 4 * np.pi * np.sqrt(6 * f_needed / 41)) + a2_mz + DELTA_0_MZ
print(f"    f_g needed for alpha_em^-1(0) = 137.036 with measured alpha_2: {f_needed:.6f} = {f_needed*np.pi**2:.4f}/pi^2 (published-truncation f_g = {fg:.5f}, ratio {fg/f_needed:.2f});")
print("    this reproduces the measured alpha_Y by construction: it fixes ONE number (f_g) with ONE measured number (alpha_Y), so it is a re-expression, not a prediction.")
c6trial = ("C6 tuned f_g (control)", c6, TARGET, c6 / TARGET - 1, abs(c6 / TARGET - 1) < HIT)
print(f"    C6 gives alpha_em^-1(0) = {c6:.5f} (rel {c6/TARGET-1:+.2e}) -> {'HIT' if c6trial[4] else 'no hit'} (by construction)")
if MUT:
    trials.append(c6trial)

# ---- statistics
N = len(trials)
p1 = 2 * HIT / np.log(1000.0)
print(f"\nStatistics: N_trials = {N}; hit window = +-{HIT:g} relative; log-uniform prior on alpha over 3 decades gives p = {p1:.2e} per trial;")
print(f"            expected chance hits = {N*p1:.2e}; observed hits = {sum(t[4] for t in trials)}")
hits = [t for t in trials if t[4]]
chk("V1", len(hits) == 0, f"no counted trial hits at 1e-3 ({[t[0] for t in hits] if hits else 'none'})")

# ---- structural statements verified numerically
print("\nStructural checks")
# S1: IR value set by content: HR-SM prediction is close to the charged-content log sum
logsum = sum(2 * ncq2 / (3 * np.pi) * np.log(MPL / m) for nm, m, ncq2 in fermions(1))
print(f"    sum_f (2 N_c Q^2/3 pi) ln(M_Pl/m_f) (SET i) = {logsum:.3f};  C3 = {c3:.3f};  (C3 - logsum) = {c3-logsum:.3f} (the O(A) gravity-FP offset)")
chk("S1", abs(c3 - logsum) < 0.05 * c3, "HR NGFP2 prediction equals the charged-content log sum up to <5%: content and measured masses, not a fixed-point number, set alpha_IR")
chk("S2", 60 < c3 < 200 and 60 < c4 < 200, f"C3 = {c3:.1f}, C4 = {c4:.1f}: order-of-magnitude close to 137 only through the mass hierarchy and content; brackets the target? {min(c3,c4)<TARGET<max(c3,c4)}")
# S3: alpha_em not fixed by g_Y alone
chk("S3", abs(c5 / TARGET - 1) > 0.05, f"EV interacting FP gives alpha_em^-1(0) = {c5:.2f} (off by {(c5/TARGET-1)*100:.1f}%); and even a perfect g_Y leaves alpha_2 as a measured input")
# S5: the EV bound is an UPPER bound on alpha, i.e. a LOWER bound on alpha^-1; is the observed value inside it?
chk("S5", c5 < TARGET, f"observed alpha^-1(0) = {TARGET:.3f} lies inside the EV-allowed region alpha^-1 >= {c5:.2f} (bound satisfied, but a bound is not a value)")
# S4: HR SM-like consistent scale statement
print("    scale: all values above are the Thomson limit alpha(0) reached by running (no running below m_e in HR; +9.106 measured offset in C5).")
print("\nCHECKS FAILED:", fails if fails else "none")
sys.exit(1 if fails else 0)
