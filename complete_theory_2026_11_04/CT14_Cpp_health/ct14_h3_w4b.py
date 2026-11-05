#!/usr/bin/env python3
"""CT14 H3: W4b (v3s solar-background health; V3W/V3X call it W4c) - the finer spectral ladder V3X README:167-169 asks for.
V3X's background and operators are imported READ-ONLY by AST extraction from v3x_w4c_health.py (no file edited, no bytecode).
The radial spectrum is rebuilt in float64 with V3X's exact discretisation, validated against V3X's recorded 40-digit values
at 12 and 16 cells/decade, then run at 24, 32, 48. Criteria: FROZEN_CRITERIA.md (H3), written first.
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, ast, json, math, time, resource, tempfile
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
V3X = os.path.join(ROOT, "rebuild_2026_10_22", "V3X_v3s_close_undecided")
os.environ.setdefault("V3X_SCRATCH", tempfile.mkdtemp(prefix="ct14_v3x_"))
import numpy as np
import scipy.linalg as sla
import mpmath as mp

T0 = time.time(); CH = []
def check(n, ok, note=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"  ({note})" if note else ""), flush=True)

print("=" * 100); print("CT14 H3: W4b (solar background) - V3X's W4c(b) spectrum on a finer ladder"); print("=" * 100)
src = open(os.path.join(V3X, "v3x_w4c_health.py")).read()
tree = ast.parse(src)
WANT_FN = {"J", "forked", "T", "rM_of", "bg_task", "background", "grid_r", "interp_rho", "tridiag", "tri_inv", "mpf_list", "spectrum"}
WANT_AS = {"GM", "AU", "PC", "c_SI", "FOOT", "FLOOR", "RSS_KILL", "S6", "X3J", "d7b", "GE", "GRES", "DPS", "SIDE", "MUT"}
keep = []
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in WANT_FN:
        keep.append(node)
    elif isinstance(node, ast.Assign):
        names = {t.id for t in node.targets if isinstance(t, ast.Name)} | {e.id for t in node.targets if isinstance(t, ast.Tuple) for e in t.elts if isinstance(e, ast.Name)}
        if names & WANT_AS:
            keep.append(node)
    elif isinstance(node, ast.Import) and any(a.name == "v3x_solver" for a in node.names):
        keep.append(node)
mod = ast.Module(body=keep, type_ignores=[])
ns = {"__file__": os.path.join(V3X, "v3x_w4c_health.py"), "__name__": "v3x_extract"}
sys.path.insert(0, V3X)
import json as _j, subprocess as _sp, multiprocessing as _mpc, warnings as _w
_w.filterwarnings("ignore")
ns.update(dict(os=os, sys=sys, json=_j, math=math, time=time, resource=resource, subprocess=_sp, mpc=_mpc, np=np, mp=mp,
               ROOT=ROOT, HERE=V3X, OUT=[], CHK={}, RES={}, t0=time.time(), P=lambda s="": None))
# order: MUT, SIDE etc. must exist before use; exec assignments needing V after the import
ns["MUT"] = ""; ns["SIDE"] = {}
exec(compile(mod, "v3x_w4c_health.py[extract]", "exec"), ns)
print(f"  extracted from V3X: {sorted(n.name for n in keep if isinstance(n, ast.FunctionDef))}; GRES {ns['GRES']}; RSS line {ns['RSS_KILL']/1e9:.2f} GB")
REC = json.load(open(os.path.join(V3X, "v3x_w4c_health.json")))["part_b"]

def tridiag_f(rf, rc, af, ac, l, inner="neumann"):
    n = len(rc); d = np.zeros(n); e = np.zeros(n - 1)
    for k in range(1, n):
        c = af[k] * rf[k]**2 / (rc[k] - rc[k - 1]); d[k - 1] += c; d[k] += c; e[k - 1] -= c
    d[n - 1] += af[n] * rf[n]**2 / (rf[n] - rc[n - 1])
    if inner == "dirichlet": d[0] += af[0] * rf[0]**2 / (rc[0] - rf[0])
    d += ac * l * (l + 1) * (rf[1:] - rf[:-1])
    return d, e

def spectrum_f(rho_f, rho_c, rf, rc, l, gam, M, nlow=5):
    """float64 twin of V3X spectrum(): omega^2 = eig(R^T V-hat R), A-hat = R R^T (same matrices, same scaling)."""
    n = len(rc)
    Vol = (rf[1:]**3 - rf[:-1]**3) / 3; sq = np.sqrt(Vol)
    dA, eA = tridiag_f(rf, rc, rho_f, rho_c, l); dL, eL = tridiag_f(rf, rc, np.ones(n + 1), np.ones(n), l)
    dA = dA / Vol; eA = eA / (sq[:-1] * sq[1:]); dL = dL / Vol; eL = eL / (sq[:-1] * sq[1:])
    Lh = np.diag(dL) + np.diag(eL, 1) + np.diag(eL, -1)
    Vh = (M - 1) * np.linalg.inv(Lh) + gam * np.eye(n); Vh = (Vh + Vh.T) / 2
    Ah = np.diag(dA) + np.diag(eA, 1) + np.diag(eA, -1)
    R = np.linalg.cholesky(Ah)
    C = R.T @ Vh @ R
    w2 = np.sort(np.linalg.eigvalsh((C + C.T) / 2))
    evA = np.linalg.eigvalsh(Ah); evV = np.linalg.eigvalsh(Vh)
    return dict(n=n, omega2_low=w2[:nlow].tolist(), all_positive=bool(w2[0] > 0), A_pd=bool(evA[0] > 0), V_min=float(evV[0]), V_ge_gamma=bool(evV[0] >= gam * (1 - 1e-12)))

ND = (12, 16, 24, 32, 48); LS = range(5); BR = ("lo", "hi")
out = {}; ok_known = True; ok_pos = True; ok_lad = True
for f in ("canonical", "alt"):
    B = ns["background"](f)
    g, rho, vm = B["g"], B["rho"], B["vm"]
    Lam = B["Lam"]; r_out = Lam; dom = g.r <= r_out * (1 + 1e-12); gam = Lam**2 / 2
    rho_lo = rho[dom].min(axis=1) + B["rgal_lo"]; rho_hi = rho[dom].max(axis=1) + B["rgal_hi"]
    Mlo = float(1 + vm[dom].min()); Mhi = float((1 + vm[dom].max())**2); rn = g.r[dom]
    print(f"\n[{f}] background: Route N residual {B['fin']:.1e}, M_lo {Mlo:.6f} (V3X {REC[f]['background']['M_lo']:.6f}), M_hi {Mhi:.6f} (V3X {REC[f]['background']['M_hi']:.6f}), "
          f"min rho_tau {float((rho[dom] + B['rgal_lo']).min()):.4e} (V3X {REC[f]['background']['min_rho_total']:.4e})", flush=True)
    res = {}
    for nd in ND:
        rf, rc = ns["grid_r"](1e-4, r_out, nd)
        for l in LS:
            for br in BR:
                prof = rho_lo if br == "lo" else rho_hi; M_ = Mlo if br == "lo" else Mhi
                res[(nd, l, br)] = spectrum_f(ns["interp_rho"](rn, prof, rf), ns["interp_rho"](rn, prof, rc), rf, rc, l, gam, M_)
        print(f"  nd {nd:2d} (n = {res[(nd, 0, 'lo')]['n']}): lowest omega^2 l=0..4 lower bracket " + ", ".join(f"{res[(nd, l, 'lo')]['omega2_low'][0]:.6e}" for l in LS)
              + f"; all positive {all(res[(nd, l, b)]['all_positive'] for l in LS for b in BR)}; A-hat PD {all(res[(nd, l, b)]['A_pd'] for l in LS for b in BR)}; "
              f"V >= gamma {all(res[(nd, l, b)]['V_ge_gamma'] for l in LS for b in BR)}  ({time.time()-T0:.0f}s)", flush=True)
    # known answer: V3X's 40-digit values at 12 and 16 cells/decade
    dev = 0.0
    for nd in (12, 16):
        for l in LS:
            for br in BR:
                rec = [float(mp.mpf(z)) for z in REC[f]["cases"][f"nd{nd}|l{l}|{br}|neumann"]["omega2_low"][:3]]
                dev = max(dev, max(abs(a / b - 1) for a, b in zip(res[(nd, l, br)]["omega2_low"][:3], rec)))
    ok_known &= dev <= 1e-8
    print(f"  known answer: float64 vs V3X's recorded 40-digit lowest three omega^2 (nd 12, 16; l 0-4; both brackets): max rel {dev:.2e} (<= 1e-8)")
    # ladder
    lad = {}
    for i in range(1, len(ND)):
        a_, b_ = ND[i - 1], ND[i]
        lad[f"{a_}->{b_}"] = max(max(abs(p / q - 1) for p, q in zip(res[(a_, l, br)]["omega2_low"][:3], res[(b_, l, br)]["omega2_low"][:3])) for l in LS for br in BR)
    pos = all(v["all_positive"] and v["A_pd"] and v["V_ge_gamma"] for v in res.values())
    ok_pos &= pos; ok_lad &= lad["32->48"] < 5e-2
    worst_l = max(((l, br) for l in LS for br in BR), key=lambda lb: max(abs(p / q - 1) for p, q in zip(res[(32, lb[0], lb[1])]["omega2_low"][:3], res[(48, lb[0], lb[1])]["omega2_low"][:3])))
    print(f"  ladder, max rel change of the lowest three omega^2 over l 0-4 and both brackets: " + ", ".join(f"{k_} {v_:.3e}" for k_, v_ in lad.items())
          + f"  (V3X line 5e-2 on the last pair; worst at 32->48: l {worst_l[0]} {worst_l[1]})")
    w2min = min(v["omega2_low"][0] for v in res.values())
    print(f"  min omega^2 over all rungs {w2min:.4e} a0/r_M = {w2min * B['A0'] / B['rM']:.3e} s^-2")
    out[f] = dict(ladder=lad, all_positive_PD=pos, known_answer_maxrel=dev, min_omega2=w2min,
                  lowest_by_rung={f"nd{nd}|l{l}|{br}": res[(nd, l, br)]["omega2_low"][:3] for nd in ND for l in LS for br in BR})
# mpmath spot check of one fine rung (precision of the float64 route where it matters most)
f = "canonical"; B = ns["background"](f); g, rho, vm = B["g"], B["rho"], B["vm"]; Lam = B["Lam"]; dom = g.r <= Lam * (1 + 1e-12)
rho_lo = rho[dom].min(axis=1) + B["rgal_lo"]; Mlo = float(1 + vm[dom].min()); rf, rc = ns["grid_r"](1e-4, Lam, 24)
t1 = time.time()
spm = ns["spectrum"](ns["interp_rho"](g.r[dom], rho_lo, rf), ns["interp_rho"](g.r[dom], rho_lo, rc), rf, rc, 4, Lam**2 / 2, Mlo, "neumann", 30, 3)
spf = out[f]["lowest_by_rung"]["nd24|l4|lo"]
dmp = max(abs(float(mp.mpf(a)) / b - 1) for a, b in zip(spm["omega2_low"][:3], spf))
print(f"\n  mpmath (30 digits, V3X's own spectrum()) vs float64 at nd 24, l 4, lower bracket: max rel {dmp:.2e}  ({time.time()-t1:.0f}s)")
check("H3-K float64 route reproduces V3X's 40-digit spectra (<= 1e-8) and a 30-digit rung at nd 24", ok_known and dmp <= 1e-8)
check("H3-a every omega^2 > 0, A-hat PD, V-hat >= gamma_L at every rung 12..48, l 0-4, both brackets, both footings", ok_pos)
check("H3-b V3X's ladder line: lowest three omega^2 change < 5e-2 between the last two rungs (32 -> 48)", ok_lad)
out["side"] = ns["SIDE"]
json.dump(out, open(os.path.join(HERE, "ct14_h3_w4b.json"), "w"), indent=1, default=str)
print(f"\nchecks {sum(CH)}/{len(CH)}; peak RSS (this process) {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.2f} GB; "
      f"background children {[round(v['rss_bytes']/1e9, 2) for v in ns['SIDE'].values()]} GB; {time.time()-T0:.0f}s")
print("kappa = 1/2 FITTED; not theory closed.")
