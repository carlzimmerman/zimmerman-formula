#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG322 -- RESOLUTION DECIDER FOR CFG321's FAIL (recipe G5/G10, zero-field nonlinear dependence of the ungated chassis).

THE QUESTION.  CFG321 (frozen cb089fb29, results 6cb69cdc1) found the nonlinear chassis evolution about an open zero-field
region saturated and regular, but in the 1-D eps = 1e-3 set the pair-separation (Lyapunov) exponent rose with resolution
(0.0124 / 0.0414 / 0.0663 at N = 63/127/255; max amplification 95 / 339 / 1052) -- its frozen FAIL signature.  Does
lambda(N) saturate at a finite value as N -> infinity (continuous dependence with a finite Lyapunov time), or keep
growing (CFG321's FAIL confirmed)?  Criteria frozen first: FROZEN_CRITERIA.md (commit 16139a770).

METHOD.  CFG321's engine copied byte-for-byte (hash verified below), nu_mono kernel unchanged, data class D unchanged
(seeds 321/322, rms yhat 1e-4, L = 16, T = 80).  1-D N = 63/127/255/511 at eps = 1e-3 and 1e-4, base + pairs
delta = 1e-3/1e-5.  N = 1023 is not run (2-8 h per run > budget; disclosed in the frozen file).
CONTROLS  C1 the N <= 255 eps = 1e-3 rows reproduce CFG321's printed lambda and max amplification; C2 GR (MOND off)
converges up to N = 511; C3 MUTATE (CFG322_MUTATE=1): the mu_exp kernel must branch or fail (rc = 1 when it does).

Work arrays go to ../_external_data/cfg322_work[_MUTATE]/ (outside git, relative to the repository root).
Run from the repository root:  python3 campaign_fresh_gravity/CFG322_zero_field_resolution/cfg322_zero_field_resolution.py
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, json, math, time, hashlib, warnings
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")   # spurious macOS BLAS flags (as CFG321)
import numpy as np
from multiprocessing import get_context

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
ENGINE_SHA256 = "bde2fbb6abb12fad4e8392917b792374016fd8127da2a02dcaa8338ff8952174"   # cfg321_engine.py at 6cb69cdc1
_h = hashlib.sha256(open(os.path.join(HERE, "cfg322_engine.py"), "rb").read()).hexdigest()
if _h != ENGINE_SHA256:
    sys.exit(f"ABORT: cfg322_engine.py sha256 {_h} != CFG321's engine {ENGINE_SHA256}")
sys.path.insert(0, HERE)
import cfg322_engine as EN

MUTATE = os.environ.get("CFG322_MUTATE", "0") == "1"
REUSE = os.environ.get("CFG322_REUSE", "0") == "1"       # resume only: load finished work arrays instead of recomputing
SLUG = "cfg322_zero_field_resolution" + ("_MUTATE" if MUTATE else "")
EXT = os.path.join(os.path.dirname(REPO), "_external_data", "cfg322_work" + ("_MUTATE" if MUTATE else ""))
NPROC = min(14, int(os.environ.get("CFG322_NPROC", "14")))
OUT = {"lane": "CFG322", "gate": "recipe G5/G10 (zero-field nonlinear dependence)", "mutate": MUTATE, "frozen": "16139a770",
       "engine_sha256": _h, "reuse": REUSE, "checks": {}, "numbers": {}}
CH = []
T0 = time.time()


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 112 + "\n" + t + "\n" + "=" * 112)


def check(name, measured, ok, load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")
    return ok


P(__doc__.split("Work arrays")[0].strip())
P(f"\n  engine sha256 {_h} == CFG321's cfg321_engine.py (6cb69cdc1): verified")
if MUTATE:
    P("\n  *** MUTATE=1: kernel -> mu_exp (a0 -> y* a0), as CFG321's MUTATE; it must branch or fail ***")
if REUSE:
    P("\n  *** REUSE=1: finished work arrays are loaded instead of recomputed (resume mode) ***")

j340 = json.load(open(os.path.join(REPO, "real_research/g03_audit_2026/L340_filtered_khronon_completion_results.json")))
A_MAX = float(j340["numbers"]["P1"]["alpha_c_max"])
P(f"  alpha_c = {A_MAX:.4e} (L340 P1 maximum, as CFG321); kappa = 1/2 FITTED (plays no role)")

L1D, YRMS0, T1D, TGR = 16.0, 1e-4, 80.0, 10.0
NS = (63, 127, 255, 511)
EPSS = (1e-3,) if MUTATE else (1e-3, 1e-4)
DELTAS = (0.0, 1e-3, 1e-5)
KERN = "mu_exp" if MUTATE else "nu_mono"
MAX_WALL = 2400.0 if MUTATE else None
if os.environ.get("CFG322_SMOKE"):              # development smoke test only (separate outputs)
    T1D = 4.0
    SLUG += "_SMOKE"; EXT += "_SMOKE"
CFG321 = {"lambda": {63: 0.0124, 127: 0.0414, 255: 0.0663}, "Amax": {63: 95.1, 127: 338.7, 255: 1051.9}}
ZERO = 0.005


def make_kernel(name):
    return {"nu_mono": EN.NuMonoKernel, "mu_exp": EN.MuExpKernel, "off": EN.ZeroKernel}[name](A_MAX)


def tagof(s):
    return f"{s['kind']}_{s['kern']}_n{s['n']}_eps{s['eps']:.0e}_delta{s['delta']:.0e}"


def task(spec):
    warnings.filterwarnings("ignore", message=".*encountered in matmul.*")
    t0 = time.time()
    fn = os.path.join(EXT, f"cfg322_{tagof(spec)}.npz")
    if REUSE and os.path.exists(fn):
        z = np.load(fn, allow_pickle=False)
        meta = json.loads(str(z["meta"]))
        rec = {k_[4:]: z[k_].tolist() for k_ in z.files if k_.startswith("rec_")}
        return dict(meta, spec=spec, rec=rec, snaps_w=z["snap_w"], snaps_t=z["snap_t"], err=z["err"].tolist(),
                    reused=True, wall_load=time.time() - t0)
    n, eps, delta = spec["n"], spec["eps"], spec["delta"]
    gr = EN.Grid(1, n, L1D); K = make_kernel(spec["kern"])
    psi0, u0, G0, g0 = EN.initial_data(gr, K, eps, 321, YRMS0, delta=delta, seed2=322)
    T = TGR if spec["kind"] == "gr" else T1D
    o = EN.evolve(gr, K, eps, psi0, u0, G0, g0, T, max_wall=MAX_WALL)
    err = []
    if spec["kind"] == "gr":           # exact solution (CFG321 Part D): psi_k(t) = psi_k(0) cos(k t/sqrt(eps)), u = psi/eps
        Pk0 = gr.fft(psi0)
        om = np.sqrt(gr.k2 * ((1 + eps) / eps - 1))
        for tt, sw in zip(o["snaps_t"], o["snaps_w"]):
            we = gr.Bop(gr.ifft(Pk0 * np.cos(om * tt)) / eps)
            err.append(float(np.linalg.norm(sw[0] - we[0]) / np.linalg.norm(we[0])))
    meta = {"status": o["status"], "n_indef": int(o["n_indef"]), "n_refac": int(o["n_refac"]), "max_res": float(o["max_res"]),
            "dt": float(o["dt"]), "m": int(o["m"]), "wall": time.time() - t0}
    try:
        os.makedirs(EXT, exist_ok=True)
        np.savez_compressed(fn, snap_t=o["snaps_t"], snap_w=o["snaps_w"], err=np.array(err), meta=json.dumps(meta),
                            **{"rec_" + k_: np.array(v_) for k_, v_ in o["rec"].items()})
        meta["saved"] = True
    except Exception as e_:
        meta["saved"] = f"not saved: {e_}"
    return dict(meta, spec=spec, rec=o["rec"], snaps_w=o["snaps_w"], snaps_t=o["snaps_t"], err=err, reused=False)


specs = []
for eps in EPSS:
    for n in NS:
        for dl in DELTAS:
            specs.append({"kind": "main", "kern": KERN, "n": n, "eps": eps, "delta": dl})
if not MUTATE:
    for n in NS:
        for dl in DELTAS:
            specs.append({"kind": "gr", "kern": "off", "n": n, "eps": 1e-2, "delta": dl})


def cost(s):
    return (s["n"] / math.sqrt(s["eps"])) * (1.0 if s["kind"] == "main" else 1e-3)


specs.sort(key=lambda s: -cost(s))
banner(f"RUNS  {len(specs)} runs on {NPROC} processes (kernel {KERN}; 1-D; N = {NS}; eps = {EPSS})")
results = []
with get_context("fork").Pool(NPROC) as pool:
    for r in pool.imap_unordered(task, specs):
        s = r["spec"]
        P(f"  done: {s['kind']:4s} n={s['n']:4d} eps={s['eps']:.0e} delta={s['delta']:.0e}  status={r['status']}  "
          f"indef={r['n_indef']}  max_res={r['max_res']:.1e}  wall={r['wall']:.0f} s{' (reused)' if r.get('reused') else ''}  "
          f"(elapsed {time.time() - T0:.0f} s)")
        results.append(r)


def find(**kw):
    out = [r for r in results if all(r["spec"].get(k_) == v_ for k_, v_ in kw.items())]
    return out[0] if out else None


def pair_D(rb, rp):
    m = min(len(rb["snaps_w"]), len(rp["snaps_w"]))
    return np.array([float(np.linalg.norm(a_ - c_) / max(np.linalg.norm(a_), 1e-300))
                     for a_, c_ in zip(rb["snaps_w"][:m], rp["snaps_w"][:m])])


def lyap(D, t, lo=1e-4, hi=1e-1, tmin=None):
    sel = (D >= lo) & (D <= hi) if tmin is None else (t >= tmin)
    if sel.sum() < 8:
        return None, None, None, int(sel.sum())
    x, y = t[sel], np.log(D[sel])
    c, cov = np.polyfit(x, y, 1, cov=True)
    pred = np.polyval(c, x)
    r2 = 1 - np.sum((y - pred) ** 2) / max(np.sum((y - y.mean()) ** 2), 1e-300)
    return float(c[0]), float(math.sqrt(cov[0, 0])), float(r2), int(sel.sum())


def tau_first(rec, thr=0.1):
    y = np.array(rec["yrms"]); t = np.array(rec["t"])
    i = np.where(y >= thr)[0]
    return float(t[i[0]]) if len(i) else None


def zero(x):
    return abs(x) < ZERO


def ratio(num, den):
    if zero(den):
        if zero(num):
            return 0.0
        return float("inf") if num >= ZERO else None
    return num / den


# ================================================================================================= C2: GR control
if not MUTATE:
    banner("C2  GR control: MOND off (GR + the healthy BPS khronon), 1-D, eps = 1e-2, T = 10 (CFG321 Part D extended to N = 511)")
    rows = []
    for n in NS:
        b = find(kind="gr", n=n, delta=0.0); p3 = find(kind="gr", n=n, delta=1e-3); p5 = find(kind="gr", n=n, delta=1e-5)
        E = np.array(b["rec"]["E"])
        drift = float(np.max(np.abs(E - E[0])) / max(np.max(np.abs(E)), 1e-300))
        D3, D5 = pair_D(b, p3), pair_D(b, p5)
        rows.append({"n": n, "dt": b["dt"], "err_T": b["err"][-1], "drift": drift, "maxD5": float(D5.max() / 1e-5),
                     "ratio": float(D3[-1] / D5[-1]), "status": b["status"]})
        P(f"    N = {n}: dt {b['dt']:.3e}; error vs exact at T = 10: {b['err'][-1]:.3e}; energy drift {drift:.2e}; "
          f"max D/delta {D5.max() / 1e-5:.3f}; D(1e-3)/D(1e-5) at T {D3[-1] / D5[-1]:.3f}; status {b['status']}")
    po = [math.log(rows[i]["err_T"] / rows[i + 1]["err_T"]) / math.log(rows[i]["dt"] / rows[i + 1]["dt"]) for i in (1, 2)]
    pd_ = [math.log(rows[i]["drift"] / rows[i + 1]["drift"]) / math.log(rows[i]["dt"] / rows[i + 1]["dt"]) for i in (1, 2)]
    c2 = (all(p_ >= 1.8 for p_ in po) and all(p_ >= 1.8 for p_ in pd_) and rows[-1]["drift"] <= 1e-3
          and all(r_["maxD5"] <= 10 and abs(r_["ratio"] / 100 - 1) < 0.01 and r_["status"] == "ok" for r_ in rows))
    check("C2 GR control converges: error vs exact order >= 1.8 at 127->255 and 255->511, energy drift falls with order >= 1.8 "
          "and is <= 1e-3 at N = 511, pairs bounded (max D/delta <= 10) and linear (100 +- 1%) at every N",
          f"error orders {[round(x_, 3) for x_ in po]} (errors {[f'{r_['err_T']:.2e}' for r_ in rows]}); drift orders "
          f"{[round(x_, 3) for x_ in pd_]} (drifts {[f'{r_['drift']:.1e}' for r_ in rows]}); max D/delta "
          f"{[round(r_['maxD5'], 3) for r_ in rows]}; ratios {[round(r_['ratio'], 3) for r_ in rows]}", c2)
    OUT["numbers"]["C2_GR"] = {"rows": rows, "err_orders": po, "drift_orders": pd_}

# ================================================================================================= the main sets
banner(f"MAIN  lambda(N) and max amplification vs N (kernel {KERN})")
SETS = {}
regular = True; reg_txt = []
for eps in EPSS:
    P(f"\n  --- 1-D, eps = {eps:.0e} ---")
    base = {n: find(kind="main", n=n, eps=eps, delta=0.0) for n in NS}
    p3 = {n: find(kind="main", n=n, eps=eps, delta=1e-3) for n in NS}
    p5 = {n: find(kind="main", n=n, eps=eps, delta=1e-5) for n in NS}
    for n in NS:
        for lab, rr in (("base", base[n]), ("d1e-3", p3[n]), ("d1e-5", p5[n])):
            E = np.array(rr["rec"]["E"]); Ek = np.array(rr["rec"]["Ekin"])
            drift = float(np.max(np.abs(E - E[0])) / max(Ek.max(), 1e-300)) if len(E) else float("inf")
            ok_ = rr["status"] == "ok" and rr["n_indef"] == 0 and rr["max_res"] <= 1e-8
            regular &= ok_
            reg_txt.append(f"eps {eps:.0e} N {n} {lab}: {rr['status']}, indef {rr['n_indef']}, res {rr['max_res']:.1e}, "
                           f"drift {drift:.1e}, t_end {rr['rec']['t'][-1] if rr['rec']['t'] else 0}")
    taus = tau_first(base[NS[-1]]["rec"])
    taus255 = tau_first(base[255]["rec"])
    lam, se, r2s, npt, lam_alt, lam_win, amax, Ats, Ats255, lin, rms_sat = ({} for _ in range(11))
    for n in NS:
        t = np.array(base[n]["rec"]["t"])
        D3, D5 = pair_D(base[n], p3[n]), pair_D(base[n], p5[n])
        tt = t[:len(D5)]
        lam[n], se[n], r2s[n], npt[n] = lyap(D5, tt)
        lam_alt[n] = lyap(D5, tt, 1e-4, 1e-2)[0]
        lam_win[n] = lyap(D5, tt, tmin=T1D / 2)[0]
        amax[n] = float(D5.max() / 1e-5) if len(D5) else float("nan")
        it = None if taus is None else int(round(taus / 0.25))
        it255 = None if taus255 is None else int(round(taus255 / 0.25))
        Ats[n] = float(D5[it] / 1e-5) if it is not None and it < len(D5) else None
        Ats255[n] = float(D5[it255] / 1e-5) if it255 is not None and it255 < len(D5) else None
        rr_ = D3[1:len(D5)] / np.maximum(D5[1:], 1e-300)
        lin[n] = (float(rr_.min()), float(rr_.max())) if len(rr_) else (None, None)
        sel = tt >= T1D / 2
        rms_sat[n] = float(np.mean(np.array(base[n]["rec"]["yrms"])[:len(tt)][sel])) if sel.any() else None
        P(f"    N = {n:4d}: lambda {('%.4f' % lam[n]) if lam[n] is not None else 'not reached'}"
          f"{(' +- %.4f (R^2 %.2f, %d pts)' % (se[n], r2s[n], npt[n])) if lam[n] is not None else ''}; "
          f"alt D<=1e-2 {lam_alt[n] if lam_alt[n] is None else round(lam_alt[n], 4)}; window [T/2,T] "
          f"{lam_win[n] if lam_win[n] is None else round(lam_win[n], 4)}; Amax {amax[n]:.1f}; A(tau_s) "
          f"{Ats[n] if Ats[n] is None else round(Ats[n], 3)}; D(1e-3)/D(1e-5) over run "
          f"[{lin[n][0] if lin[n][0] is None else round(lin[n][0], 1)}, {lin[n][1] if lin[n][1] is None else round(lin[n][1], 1)}]; "
          f"<rms yhat>[T/2,T] {rms_sat[n] if rms_sat[n] is None else round(rms_sat[n], 4)}")
    reached = all(lam[n] is not None for n in NS)
    if reached:
        d1, d2, d3 = lam[127] - lam[63], lam[255] - lam[127], lam[511] - lam[255]
        r2_, r3_ = ratio(d2, d1), ratio(d3, d2)
        if r3_ is not None and r3_ < 1:
            lam_inf = lam[511] + (d3 * r3_ / (1 - r3_) if r3_ != 0 else 0.0)
            p_ord = math.log2(1 / r3_) if 0 < r3_ < 1 else None
        else:
            lam_inf, p_ord = float("inf") if r3_ is not None and r3_ >= 1 and d3 > 0 else None, None
        conv = (r2_ is not None and r3_ is not None and abs(r2_) <= 0.6 and abs(r3_) <= 0.6
                and lam_inf is not None and math.isfinite(lam_inf))
        fail = (d3 >= ZERO and r3_ is not None and r3_ >= 0.9)
    else:
        d1 = d2 = d3 = r2_ = r3_ = lam_inf = p_ord = None; conv = False; fail = False
    amr = [amax[NS[i + 1]] / amax[NS[i]] for i in range(3)]
    lmr = [(lam[NS[i + 1]] / lam[NS[i]]) if (lam[NS[i]] and lam[NS[i + 1]] is not None) else None for i in range(3)]
    sig321_amp = amr[1] > 2 and amr[2] > 2
    sig321_lam = all(x_ is not None for x_ in lmr[1:]) and lmr[1] > 1.25 and lmr[2] > 1.25
    fr = lambda x_: "None" if x_ is None else ("inf" if x_ == float("inf") else f"{x_:.3f}")
    P(f"    increments Delta = {fr(d1)}, {fr(d2)}, {fr(d3)}; ratios r2 = {fr(r2_)}, r3 = {fr(r3_)}; lambda_inf = {fr(lam_inf)}"
      f"{'' if p_ord is None else f' (order p = {p_ord:.2f})'}")
    P(f"    Amax per step x{amr[0]:.2f}, x{amr[1]:.2f}, x{amr[2]:.2f}; lambda per step "
      f"{[None if x_ is None else round(x_, 3) for x_ in lmr]}; CFG321 FAIL signatures on the last three grids: "
      f"amplification {sig321_amp}, Lyapunov {sig321_lam}")
    P(f"    tau_s (finest N = 511) = {taus}; tau_s (N = 255, CFG321's) = {taus255}; A(tau_s, CFG321 def) "
      f"{[None if Ats255[n] is None else round(Ats255[n], 3) for n in NS]}")
    SETS[eps] = {"lambda": lam, "lambda_se": se, "R2": r2s, "npts": npt, "lambda_alt_1e-2": lam_alt, "lambda_window_T2": lam_win,
                 "Amax": amax, "A_tau_s": Ats, "A_tau_s_N255": Ats255, "tau_s": taus, "tau_s_N255": taus255,
                 "linearity_range": lin, "rms_sat": rms_sat, "increments": [d1, d2, d3], "r2": r2_, "r3": r3_,
                 "lambda_inf": lam_inf, "order_p": p_ord, "convergent": conv, "fail": fail, "reached": reached,
                 "Amax_step_ratios": amr, "lambda_step_ratios": lmr, "cfg321_sig_amp": sig321_amp, "cfg321_sig_lam": sig321_lam}
    check(f"[eps {eps:.0e}] lambda(N) increments shrink geometrically: |r2| <= 0.6 and |r3| <= 0.6 with finite lambda_inf "
          "(RESOLVED-CONVERGENT condition for this set)",
          f"lambda {[None if lam[n] is None else round(lam[n], 4) for n in NS]}; r2 {fr(r2_)}, r3 {fr(r3_)}; lambda_inf {fr(lam_inf)}", conv)
    check(f"[eps {eps:.0e}] NOT the confirmed-fail pattern (lambda still rising at the last step with r3 >= 0.9)",
          f"Delta_3 {fr(d3)}, r3 {fr(r3_)}", not fail)

for tx in reg_txt:
    P("    " + tx)
check(f"every {KERN} main run regular: status ok, zero indefinite leaf Hessians, leaf residual <= 1e-8",
      f"{sum(1 for t_ in reg_txt if ': ok,' in t_ and 'indef 0,' in t_)}/{len(reg_txt)} runs ok and convex", regular)
OUT["numbers"]["sets"] = {f"eps{k_:.0e}": {kk: ({str(a): b for a, b in vv.items()} if isinstance(vv, dict) else vv)
                                           for kk, vv in v_.items()} for k_, v_ in SETS.items()}
OUT["numbers"]["regularity"] = reg_txt

# ================================================================================================= C1: reproduction
if not MUTATE:
    banner("C1  reproduction of CFG321's printed eps = 1e-3 rows at N = 63, 127, 255")
    s3 = SETS[1e-3]
    rep = []
    for n in (63, 127, 255):
        lr = None if s3["lambda"][n] is None else round(s3["lambda"][n], 4)
        ar = round(s3["Amax"][n], 1)
        rep.append((n, lr, CFG321["lambda"][n], ar, CFG321["Amax"][n]))
        P(f"    N = {n}: lambda {lr} vs CFG321 {CFG321['lambda'][n]}; Amax {ar} vs CFG321 {CFG321['Amax'][n]}")
    c1 = all(lr == l0 and ar == a0 for (_, lr, l0, ar, a0) in rep)
    check("C1 the N <= 255 eps = 1e-3 rows reproduce CFG321's printed lambda (4 decimals) and max amplification (1 decimal)",
          "; ".join(f"N{n}: {lr}/{l0}, {ar}/{a0}" for (n, lr, l0, ar, a0) in rep), c1)
    OUT["numbers"]["C1"] = rep
else:
    c1 = True

# ================================================================================================= verdict
banner("VERDICT (frozen rule)")
n511_branch = any(r["spec"]["kind"] == "main" and r["spec"]["n"] == 511 and
                  (r["status"] != "ok" or r["n_indef"] > 0) for r in results)
any_branch = any(r["spec"]["kind"] == "main" and (r["status"] == "blowup" or r["status"].startswith("leaf-fail") or r["n_indef"] > 0)
                 for r in results)
ctrl_names = ("C1", "C2") if not MUTATE else ()
ctrl_ok = all(ok for (nm, ok, lb) in CH if nm.startswith(ctrl_names)) if ctrl_names else True
fail_any = any(v_["fail"] for v_ in SETS.values()) or n511_branch
conv_all = all(v_["convergent"] for v_ in SETS.values()) and regular and ctrl_ok
if fail_any and c1:
    verdict = "CONFIRMED-FAIL"
elif conv_all and not fail_any:
    verdict = "RESOLVED-CONVERGENT"
else:
    verdict = "OPEN"
P(f"  per set: " + "; ".join(f"eps {k_:.0e}: convergent {v_['convergent']}, fail-pattern {v_['fail']}, reached {v_['reached']}"
                             for k_, v_ in SETS.items()))
P(f"  N = 511 run branched/failed: {n511_branch}; any run branched/failed: {any_branch}; controls ok: {ctrl_ok}")
P(f"  VERDICT: {verdict}" + (" (MUTATE: must branch or fail, and not be RESOLVED-CONVERGENT)" if MUTATE else ""))
if not MUTATE:
    P("  G5/G10 nonlinear dependence: " + ("CONDITIONAL (data class D, reduced model, eps continuation)" if verdict == "RESOLVED-CONVERGENT"
                                         else "stays FAIL (CFG321)" if verdict == "CONFIRMED-FAIL" else "stays as CFG321 recorded it (FAIL); the decider is not settled"))
P("  Scope: 1-D only; says NOTHING about growth or sigma_8 -- L341's failure (sigma_8 = 18-27) and FP2's failed linear cosmology stand.")
OUT["verdict"] = verdict
OUT["flags"] = {"n511_branch": n511_branch, "any_branch": any_branch, "controls_ok": ctrl_ok}
if MUTATE:
    mut_ok = any_branch and verdict != "RESOLVED-CONVERGENT"
    check("C3 MUTATE the mu_exp kernel branches or fails (indefinite leaf Hessian, leaf failure or blow-up in at least one run) "
          "and does not return RESOLVED-CONVERGENT",
          f"verdict {verdict}; runs: " + "; ".join(f"N{r['spec']['n']}/d{r['spec']['delta']:.0e}: {r['status'][:40]}, indef {r['n_indef']}"
                                                  for r in sorted(results, key=lambda q: (q['spec']['n'], q['spec']['delta']))), mut_ok)
OUT["runs"] = [{"spec": r["spec"], "status": r["status"], "wall_s": r["wall"], "dt": r["dt"], "m": r["m"], "n_refac": r["n_refac"],
                "max_res": r["max_res"], "n_indef": r["n_indef"], "reused": r.get("reused", False)} for r in results]

npass = sum(1 for c_ in CH if c_[1])
P(f"\n  {npass}/{len(CH)} checks pass; verdict {verdict}; wall {time.time() - T0:.0f} s")
OUT["summary"] = {"pass": npass, "total": len(CH), "wall_s": time.time() - T0}
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1,
          default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
if MUTATE:
    sys.exit(1 if mut_ok else 0)      # the control "fails as required" <=> rc = 1
sys.exit(0 if npass == len(CH) else 1)
