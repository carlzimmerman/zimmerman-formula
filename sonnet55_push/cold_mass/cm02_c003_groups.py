"""cm02: C003's group prediction tested on the 20 Lovisari+2015 X-ray groups (the record's group sample, loaded exactly as CFG34 does, read-only).
C003 (L191 orbit integration, v_k = 1000 km/s, canonical) retained cold fraction by baryonic mass at the anchor radius:
  1.2e10 -> 0.128, 6.5e10 -> 0.132, 1e12 (group, R500) -> 0.168, 1.4e14 (cluster, R500) -> 0.664; interpolated log-linearly in log M_b (stated choice).
Observed requirement at R500: cold_req = M_HSE - M_law, M_law = nu_mono(g_N/a0) M_b (the phantom-only law, monopole reading as CFG4/CFG34).
Retained-fraction DEFINITION is calibrated on X-COP first (declared before the run): of (A) f = cold_req/((Omega_c/Omega_b) M_b) and
(B) f = cold_req/((1 - Omega_b/Omega_m) M_HSE), use the one whose X-COP median reproduces the ledger's 0.576 (canonical); if neither is within 0.1, STOP (no verdict).
Statistic: median over groups of f_req - f_C003(M_b); error: group scatter/sqrt(N) (+) stellar bracket (+) 20% HSE bias propagated.
Verdict: CONSISTENT if |median| < 2 sigma; else C003's group prediction FAILS (direction reported).
Run: python3 cm02_c003_groups.py | MUTATE=1 sets every group's C003 prediction to 0.9 (must flip to FAIL)
"""
import os, sys, math, json, numpy as np
CFG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "campaign_fresh_gravity")
sys.path.insert(0, CFG)
import CFG7_common as C
C4 = C.C4
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
HUNT = os.path.join(C.REPO, "hunt_2026"); sys.path.insert(0, HUNT)
g7, _ = C4.exec_slices(os.path.join(HUNT, "h7_groups_hot_gas.py"), [(None, 'P("="*116); P("ITEM 7A'), ('lp = os.path.join(DATA, "lovisari2015_groups.tsv")', "R7B = {}")], name="h7_slices")
GR, mstar500, SBR = g7["gr"], g7["mstar500"], g7["SBR"]
G_, KPC, MSUN = g7["G"], g7["kpc"], g7["Msun"]
a0 = C.A0_SI["canonical"]
COSMIC = 0.1200 / 0.02237; FDM = 1 - 0.02237 / (0.1200 + 0.02237)
def nu(y): return float(C.nu_mono(np.array([y]))[0])
# calibration on X-COP (CFG4 per-cluster numbers)
xc = json.load(open(os.path.join(CFG, "CFG4_clusters_results.json")))["numbers"]["C"]["canonical|nu_mono|b0.0"]
fA = [(1 - c["fb"] * (1 + c["phantom_over_Mb"])) / (COSMIC * c["fb"]) for c in xc]
fB = [(1 - c["fb"] * (1 + c["phantom_over_Mb"])) / FDM for c in xc]
mA, mB = float(np.median(fA)), float(np.median(fB))
print(f"   X-COP calibration (ledger 0.576): definition A {mA:.3f}, B {mB:.3f}")
best = min((("A", mA), ("B", mB)), key=lambda t: abs(t[1] - 0.576))
check(f"K calibration: definition {best[0]} reproduces the ledger's X-COP 0.576 within 0.1 ({best[1]:.3f})", abs(best[1] - 0.576) < 0.1)
if abs(best[1] - 0.576) >= 0.1:
    print("STOP: no definition calibrates; no verdict."); sys.exit(1)
lM = np.log10([1.2e10, 6.5e10, 1e12, 1.4e14]); fC = np.array([0.128, 0.132, 0.168, 0.664])
def fc003(Mb): return 0.9 if MUTATE else float(np.interp(math.log10(Mb), lM, fC))
def run(sfac, hse=1.0):
    d, mbs, fr = [], [], []
    for g in GR:
        Mb = g["Mg500"] + mstar500(g["M500"]) * sfac; r = g["R500"] * KPC
        y = G_ * Mb * MSUN / r**2 / a0; Mlaw = nu(y) * Mb; MH = g["M500"] * hse
        cold = MH - Mlaw
        f = cold / (COSMIC * Mb) if best[0] == "A" else cold / (FDM * MH)
        d.append(f - fc003(Mb)); mbs.append(Mb); fr.append(f)
    return np.array(d), np.array(mbs), np.array(fr)
d0, mb0, fr0 = run(1.0)
dlo, _, _ = run(SBR); dhi, _, _ = run(1 / SBR); dH, _, _ = run(1.0, 1.2)
med = float(np.median(d0)); err = float(np.std(d0, ddof=1) / math.sqrt(len(d0)))
star = 0.5 * abs(np.median(dlo) - np.median(dhi)); hseb = abs(np.median(dH) - med)
tot = math.sqrt(err**2 + star**2 + hseb**2); z = med / tot
print(f"   groups: N = {len(d0)}, M_b(R500) {mb0.min():.1e} .. {mb0.max():.1e}; required f median {np.median(fr0):.3f} (16-84% {np.percentile(fr0,16):.2f}..{np.percentile(fr0,84):.2f});"
      f" C003 predicts {np.median([fc003(m) for m in mb0]):.3f}")
print(f"   median (f_req - f_C003) = {med:+.3f} +- {tot:.3f} (scatter {err:.3f}, stars {star:.3f}, HSE 20% {hseb:.3f}) -> {z:+.2f} sigma")
verdict = "CONSISTENT" if abs(z) < 2 else ("FAILS: groups need MORE cold mass than C003 keeps" if med > 0 else "FAILS: groups need LESS cold mass than C003 keeps")
print(f"   VERDICT: {verdict}")
check("V verdict computed under the pre-declared rule (MUTATE must give FAIL)", ("CONSISTENT" in verdict) != MUTATE)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
