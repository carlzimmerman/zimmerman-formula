#!/usr/bin/env python3
"""AL3 (criteria FROZEN_CRITERIA.md, 6dce9813a6): MOCK validation of the filed AC1 addendum G3. MOCK cubes only, NOT ALMA DATA.

    python3 -B al3_run.py --drive --scratch DIR --workers 8   # every job not yet done (resumable), then the summary
    python3 -B al3_run.py --job ID --scratch DIR              # one job -> jobs/ID.json
    python3 -B al3_run.py --summary                           # al3_validate.out/.json from jobs/

Reads the frozen AC1 scorer and CFG942 helpers read-only (imports; no file edited). G3 is applied in-process by al3_g3.install.
kappa = 1/2 FITTED; one disc excludes no model; not theory closed."""
import sys
sys.dont_write_bytecode = True
import hashlib, json, math, os, resource, statistics, subprocess, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
AC1 = os.path.join(ROOT, "rebuild_2026_10_22", "AC1_alma_condor_predictions"); CFG = os.path.join(ROOT, "campaign_fresh_gravity", "CFG942_alma_scoring_readiness")
JOBS = os.path.join(HERE, "jobs"); BASE = os.path.join(ROOT, "reviews", "alma_readiness_2026_11_04", "revision_v1_4", "validation_summary.json")
args = sys.argv[1:]
def opt(k, d=None): return args[args.index(k) + 1] if k in args else d
FROZEN = [os.path.join(AC1, f) for f in ("ac1_score.py", "ac1_fit_checks.py", "ac1_predict.py", "ac1_score_power_results.json", "FROZEN_CRITERIA.md", "ADDENDUM_G3_2026-11-06.md")] + [os.path.join(CFG, "cfg942_common.py")]
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def hashes(): return {os.path.relpath(p, ROOT): sha(p) for p in FROZEN}

CLASSES = {"a": dict(voff=-172.0), "b": dict(clump=True), "c": dict(rho=0.24), "d": dict(voff=-172.0, clump=True, rho=0.24)}
V3 = {"noise": dict(SdV=0.0), "outside": dict(voff=1200.0)}
SUITES = {"archive": [], "sister-like": ["--noise-div", "2.54", "--beam-scale", "1.661,1.299"]}
def all_jobs():
    J = ["K0", "V1_selftest"]
    J += [f"V2_{c}_{i}" for c in CLASSES for i in range(6)] + [f"V3_{c}_{i}" for c in V3 for i in range(6)]
    J += [f"V1_{s}_{k}_{i}" for s in SUITES for k in ("realistic", "compact", "noise") for i in range(6)]
    return J

def load_scorer(extra_args=()):
    sys.argv = [sys.argv[0]] + list(extra_args); sys.path.insert(0, AC1); sys.path.insert(0, HERE)
    import ac1_score as S
    import al3_g3 as G
    G.install(S); return S, G

def rel_spec(S, seed, voff=0.0, clump=False, rho=0.0, SdV=0.718, label=""):
    """AL1 T3's release settings."""
    C = S.C; sp, Vc = S.spec("realistic", seed=seed)
    sp.update(pix=0.015, n=480, beam=(0.105, 0.087, 30.0), dv=6.0, vlo=-1560.0, vhi=1560.0, sigma=0.132e-3, SdV=SdV,
              nu_line=S.NU * (1 - voff / C.CKMS), label=f"AL3 MOCK {label}")
    if clump: sp["clump"] = dict(frac=0.4, sig_as=0.15 * S.RE_G / S.KPA, r_as=0.5 * S.RE_G / S.KPA, az_deg=45.0)
    if rho: sp["rho_ch"] = rho
    return sp, Vc

def record(m, G):
    r = dict(detected=bool(m.get("detected")), G1_3D_SN=m.get("G1_3D", {}).get("SN"), z3=m.get("G1_3D", {}).get("z_line"), branches=sorted(m.get("branches", {})), fits={})
    for nm, f in m.get("fits", {}).items():
        r["fits"][nm] = dict(valid=f["valid"], V=f["V"], R_score=f["R_score"], params=f["params"], trial_chi2=f["trial_chi2"], start_spread=f["start_spread"],
                             at_bound=f["at_bound"], inc_clamped=f["inc_clamped"], inc=f["inc"], error_calibration=f.get("error_calibration"))
    r["g3_log"] = list(G.STATE["log"]); return r

def run_job(jid, scr):
    t0 = time.time(); H0 = hashes(); out = dict(job=jid, note="MOCK only, NOT ALMA DATA")
    import numpy as np
    if jid.startswith("V1_") and jid != "V1_selftest":
        _, suite, kind, i = jid.split("_"); S, G = load_scorer(SUITES[suite])
    else:
        S, G = load_scorer()
    C = S.C; import al3_mock as MK
    os.makedirs(scr, exist_ok=True); path = os.path.join(scr, f"AL3_{jid}.fits")
    def meas(on):
        G.STATE.update(on=on, log=[], vsys_centroid=None); n0 = len(S.OUT); m, _ = S.measure(path, use3d=True, inject=False); del S.OUT[n0:]; return record(m, G)
    if jid == "K0":
        sp, _ = rel_spec(S, 83000, label="K0"); pa, pb = path + ".frozen.fits", path + ".al3.fits"
        ha = C.write_mock_cube(pa, sp); hb = MK.write_mock_cube(C, pb, sp); out.update(sha_frozen=ha, sha_al3=hb, PASS=ha == hb); os.remove(pa); os.remove(pb)
    elif jid == "V1_selftest":
        d = os.path.join(HERE, "v1_selftest"); os.makedirs(d, exist_ok=True); S.RESULT_DIR = d; G.STATE.update(on=True, log=[])
        ok = S.selftest(os.path.join(scr, "selftest")); out.update(PASS=bool(ok), checks=json.load(open(os.path.join(d, "ac1_score_selftest_results.json")))["checks"], g3_log=G.STATE["log"])
    elif jid.startswith("V1_"):
        i = int(i); sp, Vc = S.spec(kind, seed=70000 + 97 * i + sum(map(ord, kind))); C.write_mock_cube(path, sp)
        out.update(suite=suite, kind=kind, seed=i, g3=meas(True)); os.remove(path)
    elif jid.startswith("V2_"):
        _, c, i = jid.split("_"); i = int(i); k = list(CLASSES).index(c); sp, Vc = rel_spec(S, 83000 + 97 * i + 1000 * k, label=jid, **CLASSES[c])
        out["cube_sha256"] = MK.write_mock_cube(C, path, sp); box = C.load_box(path, S.RA, S.DEC, S.NU, S.HALF, 650.0, S.VCONT); out["rho1_measured"] = G.rho1(box, 600.0); del box
        out.update(cls=c, seed=i, frozen=meas(False), g3=meas(True)); os.remove(path)
    elif jid.startswith("V3_"):
        _, c, i = jid.split("_"); i = int(i); k = list(V3).index(c); sp, Vc = rel_spec(S, 89000 + 97 * i + 1000 * k, label=jid, **V3[c])
        out["cube_sha256"] = MK.write_mock_cube(C, path, sp); out.update(cls=c, seed=i, g3=meas(True)); os.remove(path)
    out.update(frozen_sha256_start=H0, frozen_unchanged=H0 == hashes(), seconds=time.time() - t0, peak_rss_MB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6)
    os.makedirs(JOBS, exist_ok=True); tmp = os.path.join(JOBS, jid + ".json.tmp"); json.dump(out, open(tmp, "w"), indent=1, default=str); os.replace(tmp, os.path.join(JOBS, jid + ".json"))

def drive(scr, nw):
    todo = [j for j in all_jobs() if not os.path.exists(os.path.join(JOBS, j + ".json"))]; run = {}; log = open(os.path.join(HERE, "al3_drive.log"), "a")
    print(f"{len(todo)} jobs to run, {nw} workers", flush=True)
    while todo or run:
        while todo and len(run) < nw:
            j = todo.pop(0); run[j] = subprocess.Popen([sys.executable, "-B", os.path.abspath(__file__), "--job", j, "--scratch", scr], stdout=subprocess.DEVNULL, stderr=open(os.path.join(scr, j + ".err"), "w"))
        time.sleep(5)
        for j, p in list(run.items()):
            if p.poll() is not None:
                del run[j]; msg = f"{time.strftime('%H:%M:%S')} {j} exit {p.returncode}"; print(msg, flush=True); log.write(msg + "\n"); log.flush()
    summary()

# ---- summary ----
def truth(radius, pressure):   # the G2 summary's truth(): the generating curve of ac1_score.spec at the radius scored
    rdg = 1.56 / 1.678; vf = math.sqrt(430 ** 2 - 2 * 40 ** 2 * 3 / rdg) / (2 / math.pi * math.atan(3 / .5)); rot = vf * 2 / math.pi * math.atan(radius / .5)
    return math.sqrt(rot ** 2 + 2 * 40 ** 2 * radius / rdg) if pressure == "P-B" else rot

def summary():
    OUT = []; CHK = []
    def P(s=""): print(s, flush=True); OUT.append(str(s))
    def need(n, ok, x=""): CHK.append((n, bool(ok), x)); P(f"[{'PASS' if ok else 'FAIL'}] {n} {x}")
    J = {}; missing = []
    for j in all_jobs():
        f = os.path.join(JOBS, j + ".json")
        if os.path.exists(f): J[j] = json.load(open(f))
        else: missing.append(j)
    P("AL3 summary; criteria 6dce9813a6; G3 filed 315d8e4eaa; MOCK only, NOT ALMA DATA; kappa = 1/2 FITTED; not theory closed")
    need("all jobs present", not missing, f"missing {missing}" if missing else f"{len(J)} jobs")
    H = hashes(); need("T0 frozen files unchanged in every job and now", all(x["frozen_unchanged"] and x["frozen_sha256_start"] == H for x in J.values()))
    need("K0 AL3 writer with options off = frozen writer", J.get("K0", {}).get("PASS"), f"{J.get('K0', {}).get('sha_frozen', '')[:16]} vs {J.get('K0', {}).get('sha_al3', '')[:16]}")
    g3runs = [x["g3"] for x in J.values() if "g3" in x]; bad = [x for x in g3runs if x["detected"] and len(x["g3_log"]) != 6]; zero = [g for x in g3runs for g in x["g3_log"] if not g["I0_final"] > 0]
    need("T1 every G3 run: 6 G3 main fits per detected cube, all final I0 > 0", not bad and not zero, f"{len(g3runs)} runs, {sum(len(x['g3_log']) for x in g3runs)} G3 fits, {len(bad)} wrong count, {len(zero)} with I0 <= 0")
    st = J.get("V1_selftest", {}); RES = dict(V1={}, V2={}, V3={}, V4={})
    # V1
    P("\n--- V1 no regression (G3 on) ---")
    need("V1 selftest: all checks PASS", st.get("PASS"), ", ".join(f"{n}:{'P' if o else 'F'}" for n, o in st.get("checks", [])))
    base = json.load(open(BASE))["suites"]; v1 = True
    for s in SUITES:
        for k in ("realistic", "compact", "noise"):
            rows = [J[f"V1_{s}_{k}_{i}"]["g3"] for i in range(6) if f"V1_{s}_{k}_{i}" in J]; b = base[s][k]
            fits = [r["fits"]["incl-Tadaki"] for r in rows if "incl-Tadaki" in r["fits"] and r["fits"]["incl-Tadaki"]["valid"]]
            nv = len(fits); det = sum(r["detected"] for r in rows); met = {}
            for inc in ("incl-mom0", "incl-Tadaki"):
                ff = [r["fits"][inc] for r in rows if inc in r["fits"] and r["fits"][inc]["valid"]]
                for pr, key in (("P-B", "Vc_PB"), ("P0", "Vc_P0")):
                    res_ = [f["V"][key] / truth(f["R_score"], pr) - 1 for f in ff]; met[f"{inc}|{pr}"] = dict(n=len(ff), rms=math.sqrt(sum(x * x for x in res_) / len(res_)) if ff else None, bias=sum(res_) / len(res_) if ff else None)
            ok_n = nv >= b["valid_primary"]; g2r = b["metrics"]["incl-Tadaki|P-B"]["rms_fraction"]; g3r = met["incl-Tadaki|P-B"]["rms"]
            ok_r = True if not b["valid_primary"] else (g3r is not None and g3r <= g2r + 0.02)
            v1 = v1 and ok_n and ok_r; RES["V1"][f"{s}|{k}"] = dict(detected=det, valid=nv, G2_valid=b["valid_primary"], rms_TPB=g3r, G2_rms_TPB=g2r, metrics=met, PASS=ok_n and ok_r)
            P(f"{s:11s} {k:9s}: detected {det}/6; primary valid {nv}/6 (G2 {b['valid_primary']}/6); Tadaki P-B RMS " + (f"{g3r:.4f}" if g3r is not None else "n/a") + (f" (G2 {g2r:.4f})" if g2r is not None else "") + f" -> {'PASS' if ok_n and ok_r else 'FAIL'}"
              + "; others " + ", ".join(f"{kk} n{vv['n']} rms {vv['rms']:.3f}" for kk, vv in met.items() if vv["rms"] is not None and kk != "incl-Tadaki|P-B"))
    need("V1 suites: valid counts >= G2, Tadaki P-B RMS <= G2 + 0.02", v1)
    # V2, V4
    P("\n--- V2 hard classes (G3 on) and V4 (frozen fitter, same cubes) ---"); v2 = True; v4 = False; lab = dict(a="(a) offset -172", b="(b) lopsided 40% clump", c="(c) rho 0.24", d="(d) a+b+c")
    for c in CLASSES:
        rows = [J[f"V2_{c}_{i}"] for i in range(6) if f"V2_{c}_{i}" in J]
        val = [r["g3"]["fits"]["incl-Tadaki"] for r in rows if "incl-Tadaki" in r["g3"]["fits"] and r["g3"]["fits"]["incl-Tadaki"]["valid"]]
        e430 = [abs(f["V"]["Vc_PB"] / 430 - 1) for f in val]; etr = [abs(f["V"]["Vc_PB"] / truth(f["R_score"], "P-B") - 1) for f in val]
        m430 = statistics.median(e430) if val else None; mtr = statistics.median(etr) if val else None
        p430 = len(val) >= 4 and m430 <= 0.10; ptr = len(val) >= 4 and mtr <= 0.10; verdict = "PASS" if p430 and ptr else "FAIL" if not p430 and not ptr else "SPLIT"
        v2 = v2 and verdict == "PASS"
        col = [r["seed"] for r in rows if any(f["params"][7] == 0.0 for f in r["frozen"]["fits"].values())]; fz = [r["frozen"]["fits"].get("incl-Tadaki", {}).get("valid") for r in rows]
        v4 = v4 or bool(col); rho = [round(r["rho1_measured"], 3) for r in rows]
        adequacy = [(round(g["dchi2"]), round(g["thr_filed"], 1), g["would_pass_strict"]) for r in rows for g in r["g3"]["g3_log"][:1]]
        RES["V2"][c] = dict(n_det=sum(r["g3"]["detected"] for r in rows), valid=len(val), Vc=[f["V"]["Vc_PB"] for f in val], R_score=[f["R_score"] for f in val], median_err_430=m430, median_err_truth=mtr, verdict=verdict, rho1=rho)
        RES["V4"][c] = dict(collapsed_seeds=col, frozen_primary_valid=sum(bool(x) for x in fz))
        P(f"{lab[c]:24s}: detected {RES['V2'][c]['n_det']}/6; G3 valid {len(val)}/6, V_c P-B {[round(x) for x in RES['V2'][c]['Vc']]}, median |V/430-1| " + (f"{m430:.3f}" if val else "n/a") + ", vs truth(R) " + (f"{mtr:.3f}" if val else "n/a")
          + f" -> {verdict}; frozen fitter: I0 = 0 in seeds {col}, primary valid {RES['V4'][c]['frozen_primary_valid']}/6; rho1 measured {rho}")
        P(f"    first G3 fit per seed (dchi2, filed thr, passes strict 25(1+2rho)): {adequacy}")
    need("V2 every hard class PASS", v2); need("V4 MUTATE: frozen fitter collapses (I0 = 0) in >= 1 seed of >= 1 class", v4)
    # V3
    P("\n--- V3 no false fits (G3 on) ---"); v3 = True
    for c in V3:
        rows = [J[f"V3_{c}_{i}"]["g3"] for i in range(6) if f"V3_{c}_{i}" in J]; sc = sum(bool(r["branches"]) for r in rows); v3 = v3 and sc == 0
        RES["V3"][c] = dict(detected=sum(r["detected"] for r in rows), scored=sc, SN=[r["G1_3D_SN"] for r in rows])
        P(f"{c:8s}: detected {RES['V3'][c]['detected']}/6, scored {sc}/6; G1-3D S/N {[round(x, 2) for x in RES['V3'][c]['SN']]}")
    need("V3 0 of 6 scored in each class", v3)
    strict = [g for x in g3runs for g in x["g3_log"] if g["adequate"] and not g["would_pass_strict"]]
    P(f"\ninformation: G3 fits passing the filed threshold 25/(1+2rho) but not 25(1+2rho): {len(strict)} of {sum(len(x['g3_log']) for x in g3runs)}")
    base_ok = all(o for n, o, _ in CHK if not n.startswith("V4")); v4ok = dict((n, o) for n, o, _ in CHK).get("V4 MUTATE: frozen fitter collapses (I0 = 0) in >= 1 seed of >= 1 class")
    vd = "G3 VALIDATED" if base_ok and v4ok else "G3 NOT VALIDATED (hard classes do not exercise the repair)" if base_ok else "G3 FAILS VALIDATION"
    if missing: vd = "INCOMPLETE"
    P(f"\nVERDICT: {vd}"); rss = max((x.get("peak_rss_MB", 0) for x in J.values()), default=0); P(f"peak RSS per job {rss:.0f} MB; total job time {sum(x.get('seconds', 0) for x in J.values()) / 3600:.1f} h")
    json.dump(dict(verdict=vd, checks=CHK, results=RES, frozen_sha256=H, note="MOCK only, NOT ALMA DATA"), open(os.path.join(HERE, "al3_validate.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, "al3_validate.out"), "w").write("\n".join(OUT) + "\n")

if __name__ == "__main__":
    if "--job" in args: run_job(opt("--job"), os.path.abspath(opt("--scratch")))
    elif "--drive" in args: drive(os.path.abspath(opt("--scratch")), int(opt("--workers", "8")))
    elif "--summary" in args: summary()
