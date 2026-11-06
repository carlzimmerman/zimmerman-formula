#!/usr/bin/env python3
"""AL1 (criteria FROZEN_CRITERIA.md, 832fb4b7f5): why the 2026-11-06 row-B disc fits ended at I0 = 0. MOCK cubes only, never ALMA data.

    python3 -B alma_followup_2026_11_06/AL1_b1_fit_collapse/al1_check.py --scratch DIR      # main run -> al1_check.out/.json
    AL1_MUTATE=1 python3 -B ... --scratch DIR                                              # T3b with vsys start = true -> al1_check_MUTATE.*

Reads the frozen AC1 scorer and CFG942 helpers read-only (imports; no file is edited). The MUTATE hook replaces C.kinematic_pa's systemic
velocity in this process only. MOCK cubes are written to --scratch (outside the repo) and deleted after use.
kappa = 1/2 FITTED; one disc excludes no model; not theory closed."""
import sys
sys.dont_write_bytecode = True
import hashlib, json, math, os, resource, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
AC1 = os.path.join(ROOT, "rebuild_2026_10_22", "AC1_alma_condor_predictions"); CFG = os.path.join(ROOT, "campaign_fresh_gravity", "CFG942_alma_scoring_readiness")
args = sys.argv[1:]; SCR = os.path.abspath(args[args.index("--scratch") + 1]); MUT = os.environ.get("AL1_MUTATE") == "1"
FROZEN = [os.path.join(AC1, f) for f in ("ac1_score.py", "ac1_fit_checks.py", "ac1_predict.py", "ac1_score_power_results.json", "FROZEN_CRITERIA.md")] + [os.path.join(CFG, "cfg942_common.py")]
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
H0 = {os.path.relpath(p, ROOT): sha(p) for p in FROZEN}
sys.argv = [sys.argv[0]]; sys.path.insert(0, AC1)
import numpy as np
import ac1_score as S                      # read-only import; main() is guarded
C = S.C
OUT, CHK, RES = [], [], {}
def P(s=""): print(s, flush=True); OUT.append(str(s))
def need(n, ok, x=""): CHK.append((n, bool(ok), x)); P(f"[{'PASS' if ok else 'FAIL'}] {n} {x}")
os.makedirs(SCR, exist_ok=True); t0 = time.time()
P(f"AL1 {'MUTATE (vsys start = true)' if MUT else 'main'}; criteria 832fb4b7f5; MOCK only, NOT ALMA DATA; kappa = 1/2 FITTED; not theory closed")

V_OFF = -172.0          # release: z_3D 2.52253 vs scorer z 2.52455
def mock(path, voff, seed=4242):
    sp, Vc = S.spec("realistic", seed=seed)
    sp.update(pix=0.015, n=480, beam=(0.105, 0.087, 30.0), dv=6.0, vlo=-1560.0, vhi=1560.0, sigma=0.132e-3, SdV=0.718,
              nu_line=S.NU * (1 - voff / C.CKMS), label=f"AL1 MOCK voff {voff:+.0f}")
    # scorer velocity v = c (NU - nu)/NU (_vaxis); the mock's line sits at nu_line, so v_line = c (1 - nu_line/NU) = voff exactly
    C.write_mock_cube(path, sp); return sp, Vc

# ---- T1, T2 on a MOCK box (line at v = 0) ----
pa = os.path.join(SCR, "AL1_MOCK_v0.fits"); sp, Vc = mock(pa, 0.0)
box = C.load_box(pa, S.RA, S.DEC, S.NU, S.HALF, 650.0, S.VCONT)
v = box["v"]; sel = np.abs(v) <= 600.0; data = box["data"][sel]; vv = v[sel]; dv = box["dv"]; pix = box["pix"]
ny, nx = data.shape[1:]; hp = int(math.ceil(S.RFIT / pix)) + 4; xc, yc = box["xc"], box["yc"]
x0i, x1i, y0i, y1i = max(0, int(xc) - hp), min(nx, int(xc) + hp + 1), max(0, int(yc) - hp), min(ny, int(yc) + hp + 1)
sub = np.nan_to_num(data[:, y0i:y1i, x0i:x1i].astype(np.float64)); yy, xx = np.indices(sub.shape[1:]); X, Y = (xx - (xc - x0i)) * pix, (yy - (yc - y0i)) * pix
circ = np.hypot(X, Y) <= S.RFIT; kf = C.kernel_rfft(sub.shape[1:], box["beam"], pix); D = sub[:, circ]; inc = C.inc_from_q(S.Q_T)[0]; sig = 0.132e-3
def res(p): return ((C.disc_model(p, X, Y, vv, dv, inc, S.KPA, kf)[:, circ] - D) / sig).ravel()
lo = np.array([-0.5, -0.5, 0.5 - math.pi, -400, 10, 0.05, 3.0, 0.0, 0.01]); hi = np.array([0.5, 0.5, 0.5 + math.pi, 400, 800, 15.0, 250, np.inf, 3.0])
pz = np.array([0.0, 0.0, 0.5, -29.0, 300.0, 1.0, 40.0, 0.0, 0.1]); f0 = res(pz); cols = []
for i in range(9):
    if i == 7: continue
    h = 1e-4 * max(abs(pz[i]), 1e-2); pp = pz.copy(); pp[i] = pp[i] + h if pp[i] + h <= hi[i] else pp[i] - h; cols.append(float(np.max(np.abs((res(pp) - f0) / (pp[i] - pz[i])))))
xfit, cov, chi2, nfev, nvox, status = C.lm_fit(res, pz, lo, hi, max_iter=10)
need("T1 at I0 = 0 every non-I0 Jacobian column is exactly 0", max(cols) == 0.0, f"max |col| {max(cols):.3g}")
need("T1 lm_fit started at I0 = 0 does not move", float(np.max(np.abs(xfit - pz))) == 0.0, f"max |dp| {float(np.max(np.abs(xfit - pz))):.3g}, status {status}, nfev {nfev}")
c_ref = float(np.sum((D / sig) ** 2)); costs = [float(np.sum(res(np.r_[pz[:4], vf, pz[5:]]) ** 2)) for vf in (150.0, 300.0, 450.0)]
need("T2 cost at I0 = 0 equals sum (D/sigma)^2", abs(costs[1] / c_ref - 1) <= 1e-9, f"{costs[1]:.6f} vs {c_ref:.6f}")
need("T2 cost at I0 = 0 independent of vf", (max(costs) - min(costs)) / c_ref <= 1e-9, f"{[round(c, 4) for c in costs]}")
RES["T1T2"] = dict(jac_cols_max=cols, lm_status=status, costs=costs, c_ref=c_ref)

# ---- T3: the frozen scorer's measure() on release-like mocks ----
def run(path, label):
    n0 = len(S.OUT); m, _ = S.measure(path, use3d=True, inject=False); lines = S.OUT[n0:]
    for s in lines: P("    " + s)
    fits = m.get("fits") or {}; r = dict(detected=m["detected"], G1_3D_SN=m["G1_3D"]["SN"], z_line=m["G1_3D"].get("z_line"))
    for k, f in fits.items(): r[k] = dict(I0=f["params"][7], vsys=f["params"][3], valid=f["valid"], trial_chi2=f["trial_chi2"], Vc_PB=f["V"]["Vc_PB"], Vc_P0=f["V"]["Vc_P0"], spread=f["start_spread"])
    RES[label] = r; return r
if MUT:
    _kp = C.kinematic_pa
    def kp(*a, **k):
        pa0, vs, amp, m1 = _kp(*a, **k); P(f"MUTATE: kinematic_pa vsys {vs:.0f} replaced by the true {V_OFF:.0f}"); return pa0, V_OFF, amp, m1
    C.kinematic_pa = kp; S.C.kinematic_pa = kp
else:
    P("\n=== T3a: line at the scorer's z (v = 0) ==="); ra = run(pa, "T3a")
os.remove(pa)
pb = os.path.join(SCR, "AL1_MOCK_voff.fits"); mock(pb, V_OFF)
P(f"\n=== T3b: line at {V_OFF:+.0f} km/s ==="); rb = run(pb, "T3b"); os.remove(pb)
I0b = [rb[k]["I0"] for k in ("incl-mom0", "incl-Tadaki") if k in rb]
if not MUT:
    I0a = [ra[k]["I0"] for k in ("incl-mom0", "incl-Tadaki") if k in ra]
    rep = len(I0b) > 0 and any(x == 0 for x in I0b) and len(I0a) == 2 and all(x > 0 for x in I0a)
    P(f"\nT3: I0 v=0 {I0a}; I0 v={V_OFF:+.0f} {I0b} -> H1 {'REPRODUCED' if rep else 'NOT REPRODUCED'}"); RES["H1"] = "REPRODUCED" if rep else "NOT REPRODUCED"
else:
    ok = len(I0b) == 2 and all(x > 0 for x in I0b)
    P(f"\nMUTATE T3b I0 {I0b} -> {'no collapse with the true vsys start' if ok else 'still collapses'} (diagnostic only if the main T3b collapsed)"); RES["MUTATE_no_collapse"] = ok
H1_ = {os.path.relpath(p, ROOT): sha(p) for p in FROZEN}
need("T0 frozen files unchanged", H0 == H1_)
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6; P(f"peak RSS {rss:.0f} MB; {time.time() - t0:.0f} s")
tag = "_MUTATE" if MUT else ""
json.dump(dict(checks=CHK, results=RES, frozen_sha256=H0, peak_rss_MB=rss, note="MOCK only, NOT ALMA DATA"), open(os.path.join(HERE, f"al1_check{tag}.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"al1_check{tag}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(o for _, o, _ in CHK) else 1)
