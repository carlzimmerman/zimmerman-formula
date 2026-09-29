#!/usr/bin/env python3
"""G4 -- unification running: what group theory supplies (b_i, 3/8) and what stays free (alpha_G, M_G, spectrum). Pre-registered U1-U4 + Amendment 2.
Run: python3 g4_unification_running_and_handles.py [MUTATE]   (MUTATE: SM b_2 sign flipped; the MSSM consistency check U1c must FAIL; exits 1)"""
import sys
import numpy as np
from math import pi, log, exp

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
checks = []
def chk(name, ok, info=""):
    checks.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")

# ---- declared MEASURED inputs (not derived)
mZ = 91.1876; aem_inv = 127.955; s2w = 0.23122; a3 = 0.1179
a_inv0 = np.array([(3/5)*(1 - s2w)*aem_inv, s2w*aem_inv, 1/a3])       # alpha_1^-1 (GUT norm), alpha_2^-1, alpha_3^-1 at m_Z
print("alpha_i^-1(m_Z) =", a_inv0)
b_sm = np.array([41/10, -19/6, -7.0]); b_mssm = np.array([33/5, 1.0, -3.0])
if MUT:
    b_sm = np.array([41/10, +19/6, -7.0]); b_mssm = np.array([33/5, -1.0, -3.0])

def run(a_inv_start, b, L):    # alpha^-1(mu) = alpha^-1(mu0) - b/(2 pi) L,  L = ln(mu/mu0)
    return a_inv_start - b/(2*pi)*L

def crossing_single(b):
    L = 2*pi*(a_inv0[0] - a_inv0[1])/(b[0] - b[1])
    aG = run(a_inv0, b, L)
    return L, aG

def crossing_two_segment(bl, bh, MS):
    L1 = log(MS/mZ)
    a_MS = run(a_inv0, bl, L1)
    L2 = 2*pi*(a_MS[0] - a_MS[1])/(bh[0] - bh[1])
    aG = run(a_MS, bh, L2)
    return L1 + L2, aG

results = {}
for name, b in (("SM", b_sm), ("MSSM@mZ", b_mssm)):
    L, aG = crossing_single(b)
    results[name] = (L, aG)
    print(f"{name}: ln(M_G/m_Z) = {L:.3f}, M_G = {mZ*exp(L):.3e} GeV, alpha_1^-1 = alpha_2^-1 = {aG[0]:.3f}, alpha_3^-1 there = {aG[2]:.3f}  (mismatch {100*(aG[2]/aG[0]-1):+.1f}%)")
L2, aG2 = crossing_two_segment(b_sm, b_mssm, 1000.0)
results["SM+MSSM(M_S=1TeV)"] = (L2, aG2)
print(f"SM+MSSM(M_S=1 TeV): ln(M_G/m_Z) = {L2:.3f}, M_G = {mZ*exp(L2):.3e} GeV, alpha_G^-1 = {aG2[0]:.3f}, alpha_3^-1 there = {aG2[2]:.3f} (mismatch {100*(aG2[2]/aG2[0]-1):+.1f}%)")

# ---- U1
chk("U1a SM one-loop: alpha_3 does NOT meet alpha_1=alpha_2 (mismatch > 10 percent)", abs(results["SM"][1][2]/results["SM"][1][0] - 1) > 0.10)
chk("U1b unification scales are model dependent: M_G(SM) ~ 1e13-1e14, M_G(MSSM) ~ 1e16", 1e12 < mZ*exp(results["SM"][0]) < 1e15 and 1e15 < mZ*exp(results["MSSM@mZ"][0]) < 1e17)
chk("U1c MSSM one-loop: alpha_3 within 10 percent of alpha_G at the crossing", abs(results["MSSM@mZ"][1][2]/results["MSSM@mZ"][1][0] - 1) < 0.10)

# ---- U2 sensitivity of alpha_em^-1(m_Z) = (5/3) a1 + a2 to (alpha_G^-1, ln M_G)
for name, b in (("SM", b_sm), ("MSSM", b_mssm)):
    dL = ((5/3)*b[0] + b[1])/(2*pi)
    print(f"U2 {name}: alpha_em^-1(m_Z) = (8/3) alpha_G^-1 + {dL:.4f} ln(M_G/m_Z)  => d/d alpha_G^-1 = 2.667, d/d lnM_G = {dL:.4f}")
    # tolerance to hit alpha_em^-1(mZ) within 1e-3 relative:
    tol = 1e-3*aem_inv
    print(f"     to hold alpha_em^-1(m_Z) to 1e-3 (= {tol:.3f}) one needs alpha_G^-1 to +-{tol/(8/3):.3f} ({100*tol/(8/3)/results['MSSM@mZ'][1][0]:.2f}% of ~24-42) OR ln M_G to +-{tol/abs(dL):.3f} ({100*tol/abs(dL):.1f}% in M_G), i.e. two independent inputs")
chk("U2 alpha_em(low) depends on two independent GUT inputs (alpha_G, M_G) beyond group theory: both derivatives nonzero", abs((5/3)*b_mssm[0] + b_mssm[1]) > 0 and abs((5/3)*b_sm[0] + b_sm[1]) > 0)

# ---- U3 handles
handles = {"dim SU(5)=24": 24.0, "dim SO(10)=45": 45.0, "dim E6=78": 78.0, "dim E8=248": 248.0, "4 pi^2": 4*pi**2, "8 pi": 8*pi}
hits = []
ntr = 0
print("\nU3 handle comparison alpha_G^-1 vs handle (|ratio-1| < 1e-3 is a HIT)")
for sname, (L, aG) in results.items():
    v = aG[0]
    row = []
    for hn, hv in handles.items():
        ntr += 1
        off = v/hv - 1
        hit = abs(off) < 1e-3
        if hit: hits.append((sname, hn))
        row.append(f"{hn}:{100*off:+.1f}%")
    print(f"   {sname:20s} alpha_G^-1 = {v:.3f} | " + " ".join(row))
p_chance = 2e-3/log(10)
print(f"trial count = {ntr}; chance-hit probability per comparison {p_chance:.2e}; E[chance hits] = {ntr*p_chance:.4f}; hits = {hits}")
chk("U3a trial count is the declared 18", ntr == 18)
chk("U3b no handle hits at 1e-3 (declared expectation)", len(hits) == 0)
best = min(((abs(results[s][1][0]/hv - 1), s, hn) for s in results for hn, hv in handles.items()))
print(f"   closest comparison (REPORTED, not scored): {best[1]} vs {best[2]}, offset {100*best[0]:.2f}%; systematic uncertainty of a one-loop crossing is several percent (thresholds, two-loop).")
# systematic spread of the MSSM value under M_S and input variation, to show the size of the systematics
spread = []
for MS in (300.0, 1000.0, 3000.0, 10000.0):
    spread.append(crossing_two_segment(b_sm, b_mssm, MS)[1][0])
print("   alpha_G^-1 spread over M_S in {0.3,1,3,10} TeV (SM below, MSSM above; REPORTED ONLY, not scored, not extra trials):", [round(x, 3) for x in spread])
chk("U3c the M_S-induced spread of alpha_G^-1 exceeds the 1e-3 hit window by >10x (so a 1e-3 handle match cannot be meaningful at one loop)", (max(spread) - min(spread))/np.mean(spread) > 1e-2)

# ---- U4 scale statement
print("\nU4 scale: alpha_em(M_G) = (3/8) alpha_G holds at M_G ~ 1e13-1e16 GeV depending on the spectrum; alpha_em(Thomson) = 1/137.036 requires running through the full spectrum below.")
print(f"   e.g. MSSM: (3/8) alpha_G at the crossing gives alpha_em^-1(M_G) = {(8/3)*results['MSSM@mZ'][1][0]:.2f}; SM: {(8/3)*results['SM'][1][0]:.2f}. Neither number is near 137, none is forced.")

nfail = sum(1 for _, ok in checks if not ok)
print(f"\nSUMMARY: {len(checks)-nfail}/{len(checks)} checks pass" + (" [MUTATE]" if MUT else ""))
sys.exit(1 if nfail else 0)
