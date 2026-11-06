#!/usr/bin/env python3
"""AL2 (criteria FROZEN_CRITERIA.md, c3ea324663): trace the row-B I0 collapse on the real spw25 cutout. Diagnosis only.

    python3 -B alma_followup_2026_11_06/AL2_b1_real_trace/al2_trace.py --cube CUT.fits            # -> al2_trace.out/.json
    AL2_MUTATE=1 python3 -B ... --cube CUT.fits                                                  # data x 2 -> al2_trace_MUTATE.*

Frozen AC1 scorer and CFG942 helpers are imported read-only. In this process only: C.fit_disc is wrapped to capture its inputs and
outputs, and the fit is replayed through LOGGED_LM, a line-for-line copy of C.lm_fit that also records accepted steps (the replay must
equal the frozen output exactly). No V_c from any modified start is computed or printed. Nothing is scored.
kappa = 1/2 FITTED; one disc excludes no model; not theory closed."""
import sys
sys.dont_write_bytecode = True
import hashlib, json, math, os, resource, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
AC1 = os.path.join(ROOT, "rebuild_2026_10_22", "AC1_alma_condor_predictions"); CFG = os.path.join(ROOT, "campaign_fresh_gravity", "CFG942_alma_scoring_readiness")
REL = os.path.join(ROOT, "finish_2026_11_04", "FN2_dated_tests", "release_2026_11_06", "ac1", "ac1_score_RELEASE.json")
args = sys.argv[1:]; CUBE = os.path.abspath(args[args.index("--cube") + 1]); MUT = os.environ.get("AL2_MUTATE") == "1"
FROZEN = [os.path.join(AC1, f) for f in ("ac1_score.py", "ac1_fit_checks.py", "ac1_predict.py", "ac1_score_power_results.json", "FROZEN_CRITERIA.md")] + [os.path.join(CFG, "cfg942_common.py"), REL]
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
H0 = {os.path.relpath(p, ROOT): sha(p) for p in FROZEN}
sys.argv = [sys.argv[0]]; sys.path.insert(0, AC1)
import numpy as np
import ac1_score as S
C = S.C
OUT, R = [], {}
def P(s=""): print(s, flush=True); OUT.append(str(s))
t0 = time.time(); tag = "_MUTATE" if MUT else ""
P(f"AL2 {'MUTATE (data x 2)' if MUT else 'main'}; criteria c3ea324663; diagnosis only, no V_c from a modified start, nothing scored; kappa = 1/2 FITTED; not theory closed")

# ---- R0 ----
cs = sha(CUBE); R["R0"] = dict(sha256=cs, ok=cs.startswith("61f147499c28123e")); P(f"R0 cutout sha256 {cs[:16]} -> {'MATCHES the release cutout' if R['R0']['ok'] else 'DIFFERS: STOP'}")
if not R["R0"]["ok"]:
    open(os.path.join(HERE, f"al2_trace{tag}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(R, open(os.path.join(HERE, f"al2_trace{tag}.json"), "w"), indent=1); sys.exit(2)

# ---- R1: frozen measure(), capturing every fit_disc call ----
CALLS = []; _fd = C.fit_disc
def fd(*a, **k):
    out = _fd(*a, **k); CALLS.append(dict(a=a, k=k, out=out)); return out
C.fit_disc = fd
if MUT:
    _lb = C.load_box
    def lb(*a, **k):
        b = _lb(*a, **k); b["data"] = (b["data"] * 2).astype(np.float32); return b
    C.load_box = lb
m, box = S.measure(CUBE, use3d=True, inject=False)
for s in S.OUT: OUT.append("    " + s)
rel = json.load(open(REL))
R["R1"] = {}
for nm in ("incl-mom0", "incl-Tadaki"):
    f = m["fits"][nm]; pr = np.array(rel["fits"][nm]["params"]); pa = np.array(f["params"])
    d = float(np.max(np.abs(pa - pr) / np.maximum(np.abs(pr), 1e-12))); R["R1"][nm] = dict(I0=pa[7], max_rel_diff=d, trial_chi2=f["trial_chi2"], reproduced=bool(pa[7] == 0 and d <= 1e-6))
    P(f"R1 {nm}: I0 {pa[7]:.3g}, max rel diff from release {d:.2e}, trial chi2 {[round(c, 2) for c in f['trial_chi2']]} -> {'REPRODUCED' if R['R1'][nm]['reproduced'] else 'NOT REPRODUCED'}")

# ---- R2: replay each captured call through a logged copy of lm_fit ----
def LOGGED_LM(res, p0, lo, hi, max_iter=80, tol=1e-9, log=None):
    p = np.clip(np.asarray(p0, float), lo, hi); f = res(p); cost = float(np.sum(f * f)); nfev = 1; lam = 1e-3; status = 0
    log.append(dict(it=-1, cost=cost, p=p.tolist(), lam=lam, tried=[]))
    def jtj(p, f, central=False):
        nonlocal nfev
        n = len(p); cols = []
        for i in range(n):
            h = 1e-4 * max(abs(p[i]), 1e-2 if i not in (7,) else abs(p[i]) + 1e-30)
            if central:
                pp, pm = p.copy(), p.copy(); pp[i] += h; pm[i] -= h; cols.append((res(pp) - res(pm)) / (2 * h)); nfev += 2
            else:
                pp = p.copy(); pp[i] = pp[i] + h if pp[i] + h <= hi[i] else pp[i] - h; cols.append((res(pp) - f) / (pp[i] - p[i])); nfev += 1
        A = np.array([[float(np.sum(c1 * c2)) for c2 in cols] for c1 in cols]); g = np.array([float(np.sum(c * f)) for c in cols]); del cols
        return A, g
    for it in range(max_iter):
        A, g = jtj(p, f); improved = False; tried = []
        for _ in range(12):
            M = A + lam * np.diag(np.maximum(np.diag(A), 1e-30))
            try:
                d = -np.linalg.solve(M, g)
            except np.linalg.LinAlgError:
                lam *= 10; continue
            pn = np.clip(p + d, lo, hi); fn = res(pn); nfev += 1; cn = float(np.sum(fn * fn)); tried.append(dict(lam=lam, cost=cn, I0_unclipped=float(p[7] + d[7]), I0=float(pn[7])))
            if cn < cost:
                rel_ = (cost - cn) / max(cost, 1e-300); p, f, cost = pn, fn, cn; lam = max(lam / 3, 1e-9); improved = True; break
            lam *= 4
        log.append(dict(it=it, cost=cost, p=p.tolist(), lam=lam, tried=tried))
        if not improved: status = 2; break
        if rel_ < tol: status = 1; break
    A, _ = jtj(p, f, central=True)
    try:
        cov = np.linalg.inv(A)
    except np.linalg.LinAlgError:
        cov = np.full((len(p), len(p)), np.nan)
    return p, cov, cost, nfev, int(f.size), status

def setup(a, k):
    """the body of C.fit_disc up to lm_fit, verbatim in effect: returns res, p0, lo, hi, D, X, Y, circ, sub, vv"""
    box, inc, kpa, sig_vox, centre, pa0, vsys0, vf0, h0, R_kpc, Rd_kpc = a[:11]; rfit = k.get("rfit", 1.4); vfit = k.get("vfit", 600.0); I0 = k.get("I0")
    v = box["v"]; sel_v = np.abs(v) <= vfit; data = box["data"][sel_v]; vv = v[sel_v]; dv = box["dv"]; pix = box["pix"]
    ny, nx = data.shape[1:]; hp = int(math.ceil(rfit / pix)) + 4; xc, yc = box["xc"], box["yc"]
    x0i, x1i = max(0, int(xc) - hp), min(nx, int(xc) + hp + 1); y0i, y1i = max(0, int(yc) - hp), min(ny, int(yc) + hp + 1)
    sub = np.nan_to_num(data[:, y0i:y1i, x0i:x1i].astype(np.float64)); yy, xx = np.indices(sub.shape[1:]); X, Y = (xx - (xc - x0i)) * pix, (yy - (yc - y0i)) * pix
    circ = np.hypot(X, Y) <= rfit; kf = C.kernel_rfft(sub.shape[1:], box["beam"], pix)
    if I0 is None: I0 = max(float(np.nanmax(np.nansum(sub, axis=0)) * dv), 1e-12)
    p0 = np.array([centre[0], centre[1], pa0, vsys0, vf0, 1.0, 40.0, I0, h0])
    lo = np.array([-0.5, -0.5, pa0 - math.pi, -400, 10, 0.05, 3.0, 0.0, 0.01]); hi = np.array([0.5, 0.5, pa0 + math.pi, 400, 800, 15.0, 250, np.inf, 3.0]); p0 = np.clip(p0, lo + 1e-6, hi - 1e-6)
    D = sub[:, circ]
    def res(p): return ((C.disc_model(p, X, Y, vv, dv, inc, kpa, kf)[:, circ] - D) / sig_vox).ravel()
    return res, p0, lo, hi, D, X, Y, circ, sub, vv, dict(inc=inc, sig=sig_vox, dv=dv, pix=pix, kpa=kpa, beam=box["beam"], h0=h0)

NAMES = ["x0", "y0", "pa", "vsys", "vf", "rt", "s0", "I0", "h"]
R["R2"] = []; FIRST = None
for j, c in enumerate(CALLS):
    res, p0, lo, hi, D, X, Y, circ, sub, vv, info = setup(c["a"], c["k"]); log = []
    x, cov, cost, nfev, nvox, status = LOGGED_LM(res, p0, lo, hi, log=log); same = bool(np.array_equal(x, np.array(c["out"]["params"])))
    zero = float(np.sum((D / info["sig"]) ** 2)); hit = next((e for e in log if e["p"][7] == 0.0), None)
    rec = dict(call=j, inc=info["inc"], p0=p0.tolist(), start_cost=log[0]["cost"], zero_cost=zero, final_cost=cost, status=status, n_steps=len(log) - 1, replay_equals_frozen=same,
               first_zero_step=None if hit is None else hit["it"], log=log)
    if hit is not None:
        k_ = log.index(hit); prev = log[k_ - 1]; rec.update(cost_before=prev["cost"], cost_after=hit["cost"], step_tried=hit["tried"], p_before=prev["p"])
    R["R2"].append(rec)
    P(f"R2 call {j} (i {info['inc']:.1f}, vf0 {p0[4]:.0f}): replay == frozen {same}; start cost {log[0]['cost']:.2f}, zero-model cost {zero:.2f} (start - zero {log[0]['cost'] - zero:+.2f}); "
      + (f"I0 -> 0 at step {hit['it']} (cost {rec['cost_before']:.2f} -> {rec['cost_after']:.2f}; unclipped I0 {hit['tried'][-1]['I0_unclipped']:.4g})" if hit else f"I0 never 0 (final {x[7]:.4g})") + f"; steps {len(log) - 1}, status {status}")
    if hit is not None and len(log) > 1:
        P("      accepted steps: " + "; ".join(f"[{e['it']}] cost {e['cost']:.1f} I0 {e['p'][7]:.4g} vsys {e['p'][3]:.0f} vf {e['p'][4]:.0f} s0 {e['p'][6]:.0f} h {e['p'][8]:.3f}" for e in log[:hit["it"] + 2]))
    if FIRST is None: FIRST = (res, p0, D, X, Y, circ, sub, vv, info)

# ---- R3: start-cost decomposition (costs only; no fit from a changed start) ----
CK = C.CKMS; R["R3"] = {}
for j, c in enumerate(CALLS):
    res, p0, lo, hi, D, X, Y, circ, sub, vv, info = setup(c["a"], c["k"])
    pa_, h_ = p0[2], p0[8]; cth, sth = math.cos(pa_), math.sin(pa_); ci = math.cos(math.radians(info["inc"]))
    xr, yr = X * cth + Y * sth, -X * sth + Y * cth; bp = C.beam_pix(info["beam"], info["pix"])
    I0_flux = m["G1_3D"]["S"] * bp / np.exp(-np.hypot(xr, yr / ci) / h_).sum(); z3 = m["G1_3D"]["z_line"]; vs_3d = CK * (1 - (1 + S.Z) / (1 + z3))
    zero = float(np.sum((D / info["sig"]) ** 2)); base = float(np.sum(res(p0) ** 2))
    alt = {"I0 -> flux-implied": (7, I0_flux), "vsys -> 3D centroid": (3, vs_3d)}
    row = dict(start=base, zero=zero, I0_start=float(p0[7]), I0_flux=float(I0_flux), vsys_start=float(p0[3]), vsys_3d=float(vs_3d), swaps={})
    for k_, (i, val) in alt.items():
        q = p0.copy(); q[i] = val; row["swaps"][k_] = float(np.sum(res(q) ** 2))
    q = p0.copy(); q[7], q[3] = I0_flux, vs_3d; row["swaps"]["both"] = float(np.sum(res(q) ** 2)); R["R3"][str(j)] = row
    P(f"R3 call {j}: cost start {base - zero:+.2f} vs zero model; I0 start {p0[7]:.4g} vs flux-implied {I0_flux:.4g} (x{p0[7] / I0_flux:.2f}); vsys start {p0[3]:.0f} vs 3D {vs_3d:.0f}; "
      + "; ".join(f"{k_}: {v_ - zero:+.2f}" for k_, v_ in row["swaps"].items()))

# ---- R4: data facts in the fit cylinder ----
res, p0, D, X, Y, circ, sub, vv, info = FIRST; sig = info["sig"]
mask3 = None
v_all = box["v"]; cont = np.abs(v_all) > S.VCONT; dc = np.nan_to_num(box["data"][cont]); yy, xx = np.indices(dc.shape[1:]); rr = np.hypot(xx - box["xc"], yy - box["yc"]) * box["pix"]
cyl = rr <= 1.0; cres = float(np.median(dc[:, cyl]) / sig) if dc.shape[0] else float("nan")
offp = rr > 2.0; sp = dc[:, offp][:, ::97]; sp = sp - sp.mean(axis=0); ac1 = float(np.sum(sp[1:] * sp[:-1]) / np.sum(sp * sp)) if sp.shape[0] > 2 else float("nan")
big = float(np.mean(np.abs(D) > 4 * sig)); peak_per_vox = float(np.max(D) / sig)
R["R4"] = dict(continuum_residual_sigma=cres, lag1_autocorr_offsource=ac1, frac_vox_gt4sigma=big, peak_vox_sigma=peak_per_vox, n_cont_channels=int(cont.sum()))
P(f"R4 continuum residual in r<=1\" (line-free channels) {cres:+.3f} sigma; lag-1 channel autocorrelation off source {ac1:+.3f}; fit voxels |D| > 4 sigma {big:.4f}; peak voxel {peak_per_vox:.1f} sigma")

# ---- trigger call ----
coll = [r for r in R["R2"] if r["first_zero_step"] is not None]
call = "TRIGGER UNRESOLVED"
if coll:
    r0 = coll[0]; t = r0["step_tried"][-1] if r0["step_tried"] else None
    P(f"collapsing step: unclipped I0 {t['I0_unclipped']:.4g} clipped to 0, lam {t['lam']:.3g}, accepted because zero-model cost {r0['cost_after']:.2f} < current {r0['cost_before']:.2f}" if t else "collapse at start")
R["trigger_call"] = call  # set by hand in the README only if R2 and R3 together meet the criteria rule
H1_ = {os.path.relpath(p, ROOT): sha(p) for p in FROZEN}; R["T0_frozen_unchanged"] = H0 == H1_; P(f"T0 frozen files unchanged: {R['T0_frozen_unchanged']}")
if MUT and os.path.exists(os.path.join(HERE, "al2_trace.json")):
    mz = json.load(open(os.path.join(HERE, "al2_trace.json")))["results"]["R2"][0]["zero_cost"]; ratio = R["R2"][0]["zero_cost"] / mz; R["MUTATE_zero_cost_ratio"] = ratio
    P(f"MUTATE zero-model cost ratio {ratio:.9f} -> {'bites' if abs(ratio - 4) <= 4e-6 else 'DOES NOT BITE'}")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6; P(f"peak RSS {rss:.0f} MB; {time.time() - t0:.0f} s")
json.dump(dict(results=R, frozen_sha256=H0, peak_rss_MB=rss), open(os.path.join(HERE, f"al2_trace{tag}.json"), "w"), indent=0, default=str)
open(os.path.join(HERE, f"al2_trace{tag}.out"), "w").write("\n".join(OUT) + "\n")
