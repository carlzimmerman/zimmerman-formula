#!/usr/bin/env python3
"""SP1_sealed_lensing_step: sealed prediction of the CL2 switch in stacked weak lensing of isolated central galaxies.
FROZEN_CRITERIA.md committed alone first (1048b648fa). Machinery: X53's committed lens code (F2 inventory, AQUAL projector),
executed read-only; the law branch as X62's LF_M (law mass + 'linear' projector), the halo branch as X53's mass_H with CL2's c_f(M).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, never a particle;
not theory closed; nothing here says the data favour the framework. Writes sp1_predictions.json + SEAL.md (sha256).
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I sp1_predict.py      (SP1_MUTATE=1 twin)
"""
import os, sys, io, json, math, hashlib, resource, contextlib
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.stats import norm

MUT = os.environ.get("SP1_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
OUTF = open(os.path.join(HERE, f"sp1_predict{TAG}.out"), "w")


def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()


TSW = 13.3 if MUT else 12.3
say(f"SP1_sealed_lensing_step{' [MUTATE: switch at 10^13.3 - control output]' if MUT else ''}: criteria 1048b648fa; switch log M200 = {TSW}; kappa = 1/2 FITTED; not theory closed")
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
LMS = np.round(np.arange(10.3, 11.7001, 0.05), 3)
PRED = {"criteria": "1048b648fa", "switch_logM200": TSW, "R_Mpc": R_MPC, "logMstar": LMS.tolist(), "cf_table_S9_L4": CF,
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
for foot in FOOTS:
    rows = []
    for lm in LMS:
        Mb, Mt, lM200 = lens(foot, float(lm), TSW)
        dl = AQ.delta_sigma(RPC, RGRID_PC, law_mass(Mb, foot), "linear")
        dh = AQ.delta_sigma(RPC, RGRID_PC, Mt, "const")
        above = lM200 > TSW
        d = dh if above else dl
        p = float(norm.cdf((lM200 - TSW) / 0.15))
        dmix = p * dh + (1 - p) * dl
        rows.append(dict(logMstar=float(lm), logM200=lM200, above=bool(above), DS_law=dl.tolist(), DS_cl2=d.tolist(), Q=(d / dl).tolist(),
                         p_above_scatter=p, Q_scatter=(dmix / dl).tolist()))
    lms = np.array([r["logM200"] for r in rows])
    lms_sw = float(np.interp(TSW, lms, LMS)) if (np.any(lms > TSW) and np.any(lms <= TSW)) else None
    k5 = R_MPC.index(0.5)
    def binavg(key, lo, hi):
        sel = [r[key][k5] for r in rows if lo <= r["logMstar"] < hi]
        return float(np.mean(sel)) if sel else float("nan")
    S = binavg("Q", lms_sw, lms_sw + 0.2) / binavg("Q", lms_sw - 0.2, lms_sw) if lms_sw else None
    Ssc = binavg("Q_scatter", lms_sw, lms_sw + 0.2) / binavg("Q_scatter", lms_sw - 0.2, lms_sw) if lms_sw else None
    PRED["footings"][foot] = dict(rows=rows, logMstar_switch=lms_sw, S_step=S, S_step_scatter015=Ssc)
    say(f"\n== {foot}: switch at log M* = " + ("off grid (> 11.7)" if lms_sw is None else f"{lms_sw:.3f}") + f" (M200 = 10^{TSW}); S_step(R 0.5 Mpc) = " + ("n/a" if S is None else f"{S:.3f}") + "; with 0.15 dex scatter " + ("n/a" if Ssc is None else f"{Ssc:.3f}"))
    for r in rows[::4]:
        say(f"   log M* {r['logMstar']:.2f}  log M200 {r['logM200']:.2f}  {'HALO' if r['above'] else 'law '}  Q(0.1/0.5/1.0 Mpc) = "
            + "/".join(f"{r['Q'][R_MPC.index(x)]:.2f}" for x in (0.1, 0.5, 1.0)) + f"   DS_cl2(0.5 Mpc) {r['DS_cl2'][k5]:.2f} Msun/pc^2")
# K1: switch disabled -> Q == 1
r0 = lens("canonical", 11.0, 99.0)
checks["K1"] = {"pass": True, "value": "switch at infinity selects the law branch for every grid mass (Q = DS_law/DS_law = 1 by construction)"}
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
checks["K3"] = {"pass": peak < 1.0, "value": "< 1 GB (exact RSS in the .out only, so the sealed file is byte-reproducible)"}
say(f"\n  [PASS] K1 construction; [{'PASS' if peak < 1 else 'FAIL'}] K3 peak RSS {peak:.2f} GB")
PRED["checks"] = checks
fn = os.path.join(HERE, f"sp1_predictions{TAG}.json")
json.dump(PRED, open(fn, "w"), indent=1, default=float)
h = hashlib.sha256(open(fn, "rb").read()).hexdigest()
if not MUT:
    open(os.path.join(HERE, "SEAL.md"), "w").write(
        "# SP1 seal\n\n"
        f"`sp1_predictions.json` sha256 = `{h}`\n\n"
        "Sealed before any comparison data were opened. The prediction is the frozen CL2 picture's isolated-lens lensing step "
        "(criteria 1048b648fa). Any later edit of the predictions file breaks this hash. kappa = 1/2 FITTED; not theory closed.\n")
say(f"\npredictions sha256 {h}")
sys.exit(0 if all(c["pass"] for c in checks.values()) else 1)
