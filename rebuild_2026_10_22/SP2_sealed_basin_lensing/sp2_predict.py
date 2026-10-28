#!/usr/bin/env python3
"""SP2_sealed_basin_lensing: sealed prediction of the BASIN switch - same M*, basin member (route-E halo) vs isolated (law).
FROZEN_CRITERIA.md committed alone first (bfd2b9ac3a); machinery = SP1 (1048b648fa / 405bedd901), copied with the grid and the observable changed. Machinery: X53's committed lens code (F2 inventory, AQUAL projector),
executed read-only; the law branch as X62's LF_M (law mass + 'linear' projector), the halo branch as X53's mass_H with CL2's c_f(M).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, never a particle;
not theory closed; nothing here says the data favour the framework. Writes sp2_predictions.json + SEAL.md (sha256).
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I sp2_predict.py      (SP2_MUTATE=1 twin)
"""
import os, sys, io, json, math, hashlib, resource, contextlib
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.stats import norm

MUT = os.environ.get("SP2_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
OUTF = open(os.path.join(HERE, f"sp2_predict{TAG}.out"), "w")


def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()


TSW = 12.3
say(f"SP2_sealed_basin_lensing{' [MUTATE: halo branch replaced by the law]' if MUT else ''}: criteria bfd2b9ac3a; kappa = 1/2 FITTED; not theory closed")
# ---------------- X53 machinery (read-only, up to its main loop), c_f(M) = CL2 S9 ----------------
X53SRC = os.path.join(REB, "X53_outer_lensing_law_vs_halos", "x53_outer_lensing.py")
src = open(X53SRC).read()
src = src[:src.index('H_PRIMARY = dict(bg="A_c2b_refit", cf="cf4", zR200=None)')]
A2 = json.load(open(os.path.join(REB, "X48_native_cf_zoom", "x48_analyze_results_ng48_A2.json")))["cf_by_mass"]
S9 = [A2[k] for k in ("1e+12", "1e+13", "1e+14")]
CF = [4.0 * v / S9[2] for v in S9]
old = '    cf = 4.0 if cfmode == "cf4" else float(np.interp(math.log10(M), CF48_L, CF48_C))'
assert src.count(old) == 1
src = src.replace(old, f'    cf = float(np.interp(math.log10(M), [12.0, 13.0, 14.0], {CF!r})) if cfmode == "cl2" else (4.0 if cfmode == "cf4" else float(np.interp(math.log10(M), CF48_L, CF48_C)))')
ns = {"__file__": X53SRC, "__name__": "x53_ro"}
argv0 = sys.argv; sys.argv = [X53SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, X53SRC, "exec"), ns)
sys.argv = argv0
AQ, RGRID_PC, Gpc, a0u, FOOTS, H_NAT, LMG, INV, Rn, IDX_ALL = (ns[k] for k in ("AQ", "RGRID_PC", "Gpc", "a0u", "FOOTS", "H_NAT", "LMG", "INV", "Rn", "IDX_ALL"))
mass_H, halo_setup, fit = ns["mass_H"], ns["halo_setup"], ns["fit"]
nu = lambda y: 0.5 + np.sqrt(0.25 + 1.0 / y)
CFG = dict(bg="A_c2b_refit", cf="cl2", zR200=0.3)


def law_mass(Mb, foot):
    r = RGRID_PC
    return np.where((r > 0) & (Mb > 0), Mb * nu(np.maximum(Gpc * Mb / np.where(r > 0, r, 1.0) ** 2, 1e-300) / a0u(foot)), Mb)


def lens(foot, lm, tsw):
    Mb, _ = mass_H(foot, lm, H_NAT, CFG, halo=False)
    Mt, meta = mass_H(foot, lm, H_NAT, CFG, halo=True)
    lM200 = math.log10(meta[0])
    return Mb, Mt, lM200


R_MPC = [0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0]
RPC = np.array(R_MPC) * 1e6
LMS = np.round(np.arange(10.0, 11.2001, 0.1), 3)
PRED = {"criteria": "bfd2b9ac3a", "R_Mpc": R_MPC, "logMstar": LMS.tolist(), "cf_table_S9_L4": CF,
        "settings": "kappa = 1/2 FITTED; cold dark energy = gravitating w ~ 0 field component; not theory closed", "footings": {}}
checks = {}
# K2: law stack reproduces X53's committed L chi2 (law branch as X62's LF_M + 'linear')
for foot in FOOTS:
    out = np.empty((4, 15))
    for b in range(4):
        tab = np.empty((len(LMG), 15))
        for gi, lm in enumerate(LMG):
            Mb, _ = mass_H(foot, lm, H_NAT, dict(bg="A_c2b_refit", cf="cf4", zR200=None), halo=False)
            tab[gi] = AQ.delta_sigma(Rn[b] * 1e6, RGRID_PC, law_mass(Mb, foot), "linear")
        lMs_nat = INV[b]["logMs70"] + 2 * np.log10(0.70 / H_NAT) + 2 * np.log10(INV[b]["qDA"])
        w = INV[b]["w"]; out[b] = np.array([np.interp(lMs_nat, LMG, tab[:, i]) for i in range(15)]) @ w / w.sum()
    chi = fit(out, IDX_ALL, False)[0]["chi2"]
    ref = {"canonical": 160.70164004429935, "alt": 127.59993186489119}[foot]
    checks[f"K2_{foot}"] = {"pass": abs(chi - ref) < 0.05 * ref, "value": chi, "ref": ref}
    say(f"  [{'PASS' if checks[f'K2_{foot}']['pass'] else 'FAIL'}] K2 {foot}: law-only stack chi2 {chi:.2f} vs X53 L {ref:.2f} (within 5%)")
SP1J = json.load(open(os.path.join(REB, "SP1_sealed_lensing_step", "sp1_predictions.json")))
k3 = 0.3
for foot in FOOTS:
    rows = []
    for lm in LMS:
        Mb, Mt, lM200 = lens(foot, float(lm), TSW)
        dl = AQ.delta_sigma(RPC, RGRID_PC, law_mass(Mb, foot), "linear")
        dh = dl if MUT else AQ.delta_sigma(RPC, RGRID_PC, Mt, "const")
        rows.append(dict(logMstar=float(lm), logM200=lM200, DS_law=dl.tolist(), DS_basin=dh.tolist(), Q_env=(dh / dl).tolist()))
    i3 = R_MPC.index(0.3)
    S = float(np.mean([r["Q_env"][i3] for r in rows if 10.5 <= r["logMstar"] <= 11.0 + 1e-9]))
    # K2: at log M* 11.5 (SP1 grid, above its switch) the basin branch equals SP1's halo branch
    Mb, Mt, lM200 = lens(foot, 11.5, TSW)
    q115 = AQ.delta_sigma(RPC, RGRID_PC, Mt, "const") / AQ.delta_sigma(RPC, RGRID_PC, law_mass(Mb, foot), "linear")
    sp1row = [r for r in SP1J["footings"][foot]["rows"] if abs(r["logMstar"] - 11.5) < 1e-9][0]
    checks[f"K2_{foot}"] = {"pass": bool(np.max(np.abs(q115 - np.array(sp1row["Q"])) / np.array(sp1row["Q"])) < 1e-9), "value": float(np.max(np.abs(q115 - np.array(sp1row["Q"]))))}
    checks[f"K4_{foot}"] = {"pass": abs(S - 1) >= 0.05, "value": S}
    PRED["footings"][foot] = dict(rows=rows, S_env=S)
    say(f"\n== {foot}: S_env (mean Q_env at 0.3 Mpc, log M* 10.5-11.0) = {S:.3f};  K2 vs SP1 at log M* 11.5: {'PASS' if checks[f'K2_{foot}']['pass'] else 'FAIL'};  K4 |S-1| >= 0.05: {'PASS' if checks[f'K4_{foot}']['pass'] else 'FAIL'}")
    for r in rows[::2]:
        say(f"   log M* {r['logMstar']:.1f}  log M200 {r['logM200']:.2f}  Q_env(0.1/0.3/0.5/1.0 Mpc) = " + "/".join(f"{r['Q_env'][R_MPC.index(x)]:.2f}" for x in (0.1, 0.3, 0.5, 1.0)))
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
checks["K3"] = {"pass": peak < 1.0, "value": "< 1 GB (exact RSS in the .out only, so the sealed file is byte-reproducible)"}
say(f"\n  [{'PASS' if peak < 1 else 'FAIL'}] K3 peak RSS {peak:.2f} GB")
PRED["checks"] = checks
fn = os.path.join(HERE, f"sp2_predictions{TAG}.json")
json.dump(PRED, open(fn, "w"), indent=1, default=float)
h = hashlib.sha256(open(fn, "rb").read()).hexdigest()
if not MUT:
    open(os.path.join(HERE, "SEAL.md"), "w").write(
        "# SP2 seal\n\n"
        f"`sp2_predictions.json` sha256 = `{h}`\n\n"
        "Sealed before any comparison data were opened. The prediction is the basin rule's environment step at fixed M* "
        "(criteria bfd2b9ac3a). Any later edit of the predictions file breaks this hash. kappa = 1/2 FITTED; not theory closed.\n")
say(f"\npredictions sha256 {h}")
sys.exit(0 if all(c["pass"] for c in checks.values()) else 1)
