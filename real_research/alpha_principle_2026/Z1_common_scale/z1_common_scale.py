#!/usr/bin/env python3
"""Z1 -- is there ANY scale at which the three SM gauge couplings come together?  Pre-registered in Z1_PREREGISTRATION.md.
Imports lane Y1's validated running READ-ONLY (path-relative).
Run:    python3 z1_common_scale.py            (exit 0 iff all declared checks pass)
MUTATE: python3 z1_common_scale.py MUTATE     (the positive control uses the SM coefficients instead of the MSSM ones; exactly C2 must fail: exit 1; exit 3 if broken)
"""
import sys
sys.dont_write_bytecode = True
import os
import math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("Y1_running_precision", "B_rg_asymptotic_safety", "N1_joint_couplings", "U3_invented_uv_boundary", "D_calibration_bar"):
    sys.path.insert(0, os.path.join(HERE, "..", sub))
import y1_lib as L

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
PI = math.pi
FAILED = []


def chk(tag, ok, detail=""):
    if not ok:
        FAILED.append(tag)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


print("Z1: is there any scale at which the three SM gauge couplings come together?   (MUTATE=%s)" % MUT)
tr = L.run_central(mu_max=1e21)
mus = np.exp(np.linspace(math.log(1.1 * L.PDG["Mt"]), math.log(1e21), 4000))
A = np.array([tr.A(m) for m in mus])                         # columns: a_Y, a_2, a_3
REL_ERR = np.array([0.0023, 0.00021, 0.0012])                # Y1's 1-sigma relative errors of (a_Y, a_2, a_3) at M_P (used at all scales as a conservative common value)


def spread(vals):
    return (vals.max(axis=1) - vals.min(axis=1)) / vals.mean(axis=1)


def sigma_spread(vals):
    # combined 1-sigma of the relative spread, propagated in quadrature from the per-coupling relative errors
    s = np.sqrt(((REL_ERR * vals) ** 2).sum(axis=1)) / vals.mean(axis=1)
    return s


res = {}
for name, fac in (("Y", np.array([1.0, 1.0, 1.0])), ("GUT", np.array([0.6, 1.0, 1.0]))):
    V = A * fac
    S = spread(V)
    i = int(np.argmin(S))
    sig = sigma_spread(V)[i]
    res[name] = (S[i], mus[i], sig)
    print(f"  normalisation {name:3s}: minimum relative spread {100 * S[i]:.2f}% at mu = {mus[i]:.3e} GeV (1/alpha = {V[i][0]:.2f}, {V[i][1]:.2f}, {V[i][2]:.2f}); its 1-sigma = {100 * sig:.2f}% -> {S[i] / sig:.1f} sigma")

chk("C1a GUT normalisation: minimum spread over all scales exceeds 5% by more than 10 sigma", res["GUT"][0] > 0.05 and res["GUT"][0] / res["GUT"][2] > 10, f"({100 * res['GUT'][0]:.2f}%)")
chk("C1b Y normalisation: minimum spread over all scales exceeds 3% by more than 10 sigma", res["Y"][0] > 0.03 and res["Y"][0] / res["Y"][2] > 10, f"({100 * res['Y'][0]:.2f}%)")

print("\n  pairwise crossings (GUT and Y normalisations) and the miss of the third coupling there:")
for name, fac in (("Y", np.array([1.0, 1.0, 1.0])), ("GUT", np.array([0.6, 1.0, 1.0]))):
    V = A * fac
    for (p, q, r, lab) in ((0, 1, 2, "a_Y=a_2"), (0, 2, 1, "a_Y=a_3"), (1, 2, 0, "a_2=a_3")):
        d = V[:, p] - V[:, q]
        idx = np.where(np.sign(d[:-1]) * np.sign(d[1:]) < 0)[0]
        if len(idx) == 0:
            print(f"    {name:3s} {lab}: no crossing below 1e21 GeV")
            continue
        k = idx[0]
        mu_c = mus[k]
        pair = 0.5 * (V[k, p] + V[k, q])
        miss = (V[k, r] - pair) / pair
        print(f"    {name:3s} {lab}: crossing at {mu_c:.3e} GeV; third coupling misses by {100 * miss:+.1f}%")

# positive control: one-loop MSSM-style continuation from 1 TeV
b_ssm = np.array([33.0 / 5.0, 1.0, -3.0]) if not MUT else np.array([41.0 / 10.0, -19.0 / 6.0, -7.0])   # (b1, b2, b3), GUT normalisation
a1_tev, a2_tev, a3_tev = 0.6 * tr.A(1000.0)[0], tr.A(1000.0)[1], tr.A(1000.0)[2]
a0 = np.array([a1_tev, a2_tev, a3_tev])
mus_c = np.exp(np.linspace(math.log(1000.0), math.log(1e21), 4000))
ac = np.array([a0 - (b_ssm / (2 * PI)) * math.log(m / 1000.0) for m in mus_c])
Sc = spread(ac)
ic = int(np.argmin(Sc))
print(f"\n  positive control ({'SM coefficients (MUTATED)' if MUT else 'MSSM one-loop coefficients'} from 1 TeV): minimum spread {100 * Sc[ic]:.2f}% at {mus_c[ic]:.3e} GeV")
chk("C2 the detector finds a common scale when one exists: spread below 3% between 1e15 and 1e17 GeV", Sc[ic] < 0.03 and 1e15 < mus_c[ic] < 1e17, f"({100 * Sc[ic]:.2f}% at {mus_c[ic]:.2e})")

print("\nVERDICT (against the declared criteria):")
print("  With a Standard-Model desert the three gauge couplings never come together: the closest approach is %.1f%% (GUT normalisation) and %.1f%% (Y normalisation), " % (100 * res["GUT"][0], 100 * res["Y"][0]))
print("  each many times Y1's combined uncertainty. So NO scale X -- whatever kappa, Z, pi or an integer might make of it -- rescues a zero-knob 'equal couplings at X' rule with a SM desert (C3).")
print("  The positive control shows the detector finds a common scale when the running allows one. alpha stays an INPUT; kappa = 1/2 FITTED.")
if MUT:
    works = [t.split()[0] for t in FAILED] == ["C2"]
    print("\nMUTATE CONTROL: failed checks:", FAILED, "->", "the control works (exit 1)" if works else "CONTROL BROKEN (exit 3): it must fail exactly C2")
    sys.exit(1 if works else 3)
sys.exit(0 if not FAILED else 1)
