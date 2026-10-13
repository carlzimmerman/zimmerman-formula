"""CFG740: sealed Gaia DR4 wide-binary prediction of the stiff-polarization construction. Criteria: FROZEN_CRITERIA.md (c4f88c6ee).
gamma_v - 1 with gamma_v = sqrt(1 + anomaly/Newton); anomaly from CFG691's stiff profile at L*_min. Deterministic JSON (no timestamps).
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".
Run:  python3 cfg740_predict.py      (CFG740_MUTATE=1: no stiffness; exit 1 iff gamma_v - 1 at 10 kAU > 0.1)
"""
import os, sys, json, math, hashlib
import numpy as np
from scipy.integrate import solve_bvp
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); sys.path.insert(0, LANES)
import CFG4_common as C4  # noqa: E402
MUT = os.environ.get("CFG740_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
G, MSUN, AU, PC = 6.6743e-11, 1.98847e30, 1.495978707e11, 3.0856775814913673e16
def f(t, y):
    s = np.exp(t); return np.vstack([y[1], -y[1] + 2.0 * y[0] + s ** 2 * y[0] * np.abs(y[0]) - 1.0])
tt = np.linspace(math.log(1e-4), math.log(1e4), 4001); ss = np.exp(tt)
SOL = solve_bvp(f, lambda ya, yb: np.array([ya[1] - (ya[0] - 0.5), yb[0] - (1e-4 - 1e-8)]), tt,
                np.vstack([1 / (ss + 2), -ss / (ss + 2) ** 2]), tol=1e-8, max_nodes=200000)
def S_of(s):
    return 0.5 * s if s < 1e-4 else (1 - 1 / s if s > 1e4 else s * float(SOL.sol(math.log(s))[0]))
Lmin = json.load(open(os.path.join(LANES, "CFG691_stiffness_window", "cfg691_results.json")))["numbers"]["G_SS"]["canonical"]["Lmin_pc"]
M = 1.5 * MSUN
T = 2.146e-10 / (8.18e3 * PC)
rJ = (G * M / T) ** (1 / 3)
BINS = [2, 5, 10, 20, 30, 50, 100, 236]
out = {"lane": "CFG740", "criteria": "c4f88c6ee", "M_Msun": 1.5, "Lstar_pc": round(Lmin, 6), "basin_rJ_pc": round(rJ / PC, 6), "footings": {}}
lines = [__doc__.strip(), f"\nL*_min = {Lmin:.4f} pc; 1.5 Msun free-fall basin r_J = {rJ / PC:.3f} pc"]
for foot in C4.FOOTS:
    a0 = C4.A0[foot]; rM = math.sqrt(G * M / a0); ell = (Lmin * PC) ** 2 / (2 * rM)
    row = {}
    for b in BINS:
        r = b * 1e3 * AU
        an = math.sqrt(G * M * a0) / r * (1.0 if MUT else S_of(r / ell))
        gv1 = math.sqrt(1 + an / (G * M / r ** 2)) - 1
        row[str(b)] = dict(gamma_v_minus_1=float(f"{gv1:.6g}"), inside_basin=bool(r < rJ), inside_ell=bool(r < ell),
                           inner_limit=float(f"{0.5 * (r / (Lmin * PC)) ** 2:.6g}"))
    sl = math.log(row["236"]["gamma_v_minus_1"] / row["50"]["gamma_v_minus_1"]) / math.log(236 / 50)
    out["footings"][foot] = dict(ell_gamma_pc=float(f"{ell / PC:.6g}"), bins_kAU=row, logslope_50_236=float(f"{sl:.6g}"))
    lines.append(f"\n{foot}: l_gamma(1.5 Msun) = {ell / PC:.1f} pc; log-slope 50-236 kAU = {sl:.4f}")
    for b in BINS:
        x = row[str(b)]
        lines.append(f"    {b:4d} kAU: gamma_v - 1 = {x['gamma_v_minus_1']:.3e}  (inner limit (1/2)(s/L*)^2 = {x['inner_limit']:.3e}); inside basin {x['inside_basin']}, inside l_gamma {x['inside_ell']}")
out["contrast_read_from_prereg"] = {"gated_MI_2_30kAU": "1.0004-1.0006, exponent 3 beyond r_gate", "PAPER44_gamma_iso": {"2000": 1.01, "5000": 1.06, "10000": 1.197, "20000": 1.511}}
out["falsifiers"] = ["any boost above the envelope; gamma_v >= 1.01 at s <= 50 kAU kills the construction", "an excess with log-slope inconsistent with 2"]
blob = json.dumps(out, sort_keys=True, indent=1)
open(os.path.join(HERE, f"cfg740_predictions{TAG}.json"), "w").write(blob + "\n")
h = hashlib.sha256((blob + "\n").encode()).hexdigest()
lines.append(f"\nSHA-256 of cfg740_predictions{TAG}.json: {h}")
open(os.path.join(HERE, f"cfg740_predict{TAG}.out"), "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
if MUT:
    v = out["footings"]["canonical"]["bins_kAU"]["10"]["gamma_v_minus_1"]; print(f"MUTATE: gamma_v - 1 at 10 kAU = {v:.3f}"); sys.exit(1 if v > 0.1 else 0)
open(os.path.join(HERE, "PREDICTIONS_HASH.txt"), "w").write(f"{h}  cfg740_predictions.json\n")
