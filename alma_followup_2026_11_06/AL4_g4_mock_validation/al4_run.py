#!/usr/bin/env python3
"""AL4 (criteria FROZEN_CRITERIA.md, 31e5110862 / origin 8551af59dd): MOCK validation of the filed AC1 addendum G4 (8ff85f806e).
MOCK cubes only, NOT ALMA DATA.

    python3 -B al4_run.py --drive --scratch DIR --workers 6   # resumable; C ladder first, then the rest, then the summary
    python3 -B al4_run.py --job ID --scratch DIR              # one job -> jobs/ID.json
    python3 -B al4_run.py --summary

Reads the frozen AC1 scorer, the CFG942 helpers and AL3's mock writer read-only (imports; no file edited). G4 is applied in-process
by al4_g4.install. kappa = 1/2 FITTED; one disc excludes no model; not theory closed."""
import sys
sys.dont_write_bytecode = True
import hashlib, json, math, os, resource, statistics, subprocess, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
AC1 = os.path.join(ROOT, "rebuild_2026_10_22", "AC1_alma_condor_predictions"); CFG = os.path.join(ROOT, "campaign_fresh_gravity", "CFG942_alma_scoring_readiness")
AL3 = os.path.join(ROOT, "alma_followup_2026_11_06", "AL3_g3_mock_validation")
JOBS = os.path.join(HERE, "jobs"); BASE = os.path.join(ROOT, "reviews", "alma_readiness_2026_11_04", "revision_v1_4", "validation_summary.json")
args = sys.argv[1:]
def opt(k, d=None): return args[args.index(k) + 1] if k in args else d
FROZEN = ([os.path.join(AC1, f) for f in ("ac1_score.py", "ac1_fit_checks.py", "ac1_predict.py", "ac1_score_power_results.json", "FROZEN_CRITERIA.md",
          "ADDENDUM_G3_2026-11-06.md", "ADDENDUM_G4_2026-11-06.md", "ADDENDUM_G4_FILING_2026-11-06.md")] + [os.path.join(CFG, "cfg942_common.py")]
          + [os.path.join(AL3, f) for f in ("al3_g3.py", "al3_mock.py", "al3_run.py")])
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def hashes(): return {os.path.relpath(p, ROOT): sha(p) for p in FROZEN}

CLASSES = {"a": dict(voff=-172.0), "b": dict(clump=True), "c": dict(rho=0.24), "d": dict(voff=-172.0, clump=True, rho=0.24)}
V3 = {"noise": dict(SdV=0.0), "outside": dict(voff=1200.0)}
SUITES = {"archive": [], "sister-like": ["--noise-div", "2.54", "--beam-scale", "1.661,1.299"]}
FLAD = (2, 3, 4); COLL = 1e-12

def J_of(j):
    f = os.path.join(JOBS, j + ".json"); return json.load(open(f)) if os.path.exists(f) else None

def collapsed(rec):
    """frozen criteria: reported best fit of the primary branch (incl-Tadaki) ends with I0 <= 1e-12; undetected = no collapse"""
    f = rec["fits"].get("incl-Tadaki"); return bool(f is not None and f["params"][7] <= COLL)

def c_state():
    """returns (chosen f or None, done?, list of C jobs needed so far)"""
    need = []
    for f in FLAD:
        jj = [f"C_f{f}_{i}" for i in range(6)]; need += jj; R = [J_of(j) for j in jj]
        if any(r is None for r in R): return None, False, need
        if any(collapsed(r["frozen"]) for r in R): return f, True, need
    return None, True, need

def all_jobs():
    J = ["K0", "V1_selftest"]
    J += [f"V2_{c}_{i}" for c in CLASSES for i in range(6)] + [f"V3_{c}_{i}" for c in V3 for i in range(6)]
    J += [f"V1_{s}_{k}_{i}" for s in SUITES for k in ("realistic", "compact", "noise") for i in range(6)]
    f, done, cj = c_state(); J = cj + J
    if done and f is not None: J = [f"V2_e_{i}" for i in range(6)] + J
    return J

def load_scorer(extra_args=()):
    sys.argv = [sys.argv[0]] + list(extra_args); sys.path.insert(0, AC1); sys.path.insert(0, AL3); sys.path.insert(0, HERE)
    import ac1_score as S
    import al4_g4 as G
    G.install(S); return S, G

def rel_spec(S, seed, voff=0.0, clump=False, rho=0.0, SdV=0.718, label="", hscale=1.0):
    """AL3's rel_spec (AL1 T3 release settings), plus the class-(e) disc scale factor."""
    C = S.C; sp, Vc = S.spec("realistic", seed=seed)
    sp.update(pix=0.015, n=480, beam=(0.105, 0.087, 30.0), dv=6.0, vlo=-1560.0, vhi=1560.0, sigma=0.132e-3, SdV=SdV,
              nu_line=S.NU * (1 - voff / C.CKMS), label=f"AL3 MOCK {label}")
    if clump: sp["clump"] = dict(frac=0.4, sig_as=0.15 * S.RE_G / S.KPA, r_as=0.5 * S.RE_G / S.KPA, az_deg=45.0)
    if rho: sp["rho_ch"] = rho
    if hscale != 1.0: sp["h"] = sp["h"] * hscale; sp["label"] = f"AL4 MOCK {label} Re x{hscale:g}"
    return sp, Vc

def record(m, G):
    r = dict(detected=bool(m.get("detected")), G1_3D_SN=m.get("G1_3D", {}).get("SN"), z3=m.get("G1_3D", {}).get("z_line"), branches=sorted(m.get("branches", {})), fits={})
    for nm, f in m.get("fits", {}).items():
        r["fits"][nm] = dict(valid=f["valid"], V=f["V"], R_score=f["R_score"], params=f["params"], trial_chi2=f["trial_chi2"], start_spread=f["start_spread"],
                             at_bound=f["at_bound"], inc_clamped=f["inc_clamped"], inc=f["inc"], error_calibration=f.get("error_calibration"))
    r["fit_log"] = list(G.STATE["log"]); return r

def run_job(jid, scr):
    t0 = time.time(); H0 = hashes(); out = dict(job=jid, note="MOCK only, NOT ALMA DATA")
    if jid.startswith("V1_") and jid != "V1_selftest":
        _, suite, kind, i = jid.split("_"); S, G = load_scorer(SUITES[suite])
    else:
        S, G = load_scorer()
    C = S.C; import al3_mock as MK
    os.makedirs(scr, exist_ok=True); path = os.path.join(scr, f"AL4_{jid}.fits")
    def meas(mode):
        G.STATE.update(mode=mode, log=[], vsys_centroid=None, rho1_cache={}); n0 = len(S.OUT); m, _ = S.measure(path, use3d=True, inject=False); del S.OUT[n0:]; return record(m, G)
    def al3_sha(j):
        r = json.load(open(os.path.join(AL3, "jobs", j + ".json"))); return r.get("cube_sha256")
    if jid == "K0":
        sp, _ = rel_spec(S, 83000, label="K0"); pa, pb = path + ".frozen.fits", path + ".al3.fits"
        ha = C.write_mock_cube(pa, sp); hb = MK.write_mock_cube(C, pb, sp); out.update(sha_frozen=ha, sha_al3=hb, PASS=ha == hb); os.remove(pa); os.remove(pb)
    elif jid == "V1_selftest":
        d = os.path.join(HERE, "v1_selftest"); os.makedirs(d, exist_ok=True); S.RESULT_DIR = d; G.STATE.update(mode="g4", log=[])
        ok = S.selftest(os.path.join(scr, "selftest_" + str(os.getpid()))); out.update(PASS=bool(ok), checks=json.load(open(os.path.join(d, "ac1_score_selftest_results.json")))["checks"], fit_log=G.STATE["log"])
    elif jid.startswith("V1_"):
        i = int(i); sp, Vc = S.spec(kind, seed=70000 + 97 * i + sum(map(ord, kind))); C.write_mock_cube(path, sp)
        out.update(suite=suite, kind=kind, seed=i, g4=meas("g4")); os.remove(path)
    elif jid.startswith("C_f"):
        _, fs, i = jid.split("_"); f = int(fs[1:]); i = int(i); sp, Vc = rel_spec(S, 85000 + 97 * i + 100 * f, label=jid, voff=-172.0, rho=0.24, hscale=f)
        out["cube_sha256"] = MK.write_mock_cube(C, path, sp); out.update(cls="e", f=f, seed=i, frozen=meas("frozen")); os.remove(path)
    elif jid.startswith("V2_e_"):
        i = int(jid.split("_")[2]); f, done, _ = c_state(); assert done and f is not None
        sp, Vc = rel_spec(S, 87000 + 97 * i, label=jid, voff=-172.0, rho=0.24, hscale=f)
        out["cube_sha256"] = MK.write_mock_cube(C, path, sp); box = C.load_box(path, S.RA, S.DEC, S.NU, S.HALF, 650.0, S.VCONT); out["rho1_measured"] = G.rho1_g4(box); del box
        out.update(cls="e", f=f, seed=i, frozen=meas("frozen"), g4=meas("g4"), g4lin=meas("g4lin")); os.remove(path)
    elif jid.startswith("V2_"):
        _, c, i = jid.split("_"); i = int(i); k = list(CLASSES).index(c); sp, Vc = rel_spec(S, 83000 + 97 * i + 1000 * k, label=jid, **CLASSES[c])
        out["cube_sha256"] = MK.write_mock_cube(C, path, sp); out["al3_cube_sha256"] = al3_sha(jid)
        box = C.load_box(path, S.RA, S.DEC, S.NU, S.HALF, 650.0, S.VCONT); out["rho1_measured"] = G.rho1_g4(box); del box
        out.update(cls=c, seed=i, g4=meas("g4")); os.remove(path)
    elif jid.startswith("V3_"):
        _, c, i = jid.split("_"); i = int(i); k = list(V3).index(c); sp, Vc = rel_spec(S, 89000 + 97 * i + 1000 * k, label=jid, **V3[c])
        out["cube_sha256"] = MK.write_mock_cube(C, path, sp); out["al3_cube_sha256"] = al3_sha(jid); out.update(cls=c, seed=i, g4=meas("g4")); os.remove(path)
    out.update(frozen_sha256_start=H0, frozen_unchanged=H0 == hashes(), seconds=time.time() - t0, peak_rss_MB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6)
    os.makedirs(JOBS, exist_ok=True); tmp = os.path.join(JOBS, jid + ".json.tmp"); json.dump(out, open(tmp, "w"), indent=1, default=str); os.replace(tmp, os.path.join(JOBS, jid + ".json"))

def drive(scr, nw):
    run = {}; log = open(os.path.join(HERE, "al4_drive.log"), "a"); failed = set()
    while True:
        todo = [j for j in all_jobs() if J_of(j) is None and j not in run and j not in failed]
        if not todo and not run: break
        while todo and len(run) < nw:
            j = todo.pop(0); run[j] = subprocess.Popen(["nice", "-n", "10", sys.executable, "-B", os.path.abspath(__file__), "--job", j, "--scratch", scr],
                                                       stdout=subprocess.DEVNULL, stderr=open(os.path.join(scr, j + ".err"), "w"))
        time.sleep(5)
        for j, p in list(run.items()):
            if p.poll() is not None:
                del run[j]; msg = f"{time.strftime('%H:%M:%S')} {j} exit {p.returncode}"; print(msg, flush=True); log.write(msg + "\n"); log.flush()
                if p.returncode != 0: failed.add(j)
    summary()

def truth(radius, pressure):   # AL3's truth(): G2's generating curve at the radius scored
    rdg = 1.56 / 1.678; vf = math.sqrt(430 ** 2 - 2 * 40 ** 2 * 3 / rdg) / (2 / math.pi * math.atan(3 / .5)); rot = vf * 2 / math.pi * math.atan(radius / .5)
    return math.sqrt(rot ** 2 + 2 * 40 ** 2 * radius / rdg) if pressure == "P-B" else rot

def summary():
    OUT = []; CHK = []
    def P(s=""): print(s, flush=True); OUT.append(str(s))
    def need(n, ok, x=""): CHK.append((n, bool(ok), x)); P(f"[{'PASS' if ok else 'FAIL'}] {n} {x}")
    names = all_jobs(); J = {j: J_of(j) for j in names}; missing = [j for j, v in J.items() if v is None]; J = {j: v for j, v in J.items() if v is not None}
    P("AL4 summary; criteria 31e5110862 (origin 8551af59dd); G4 filed 8ff85f806e; MOCK only, NOT ALMA DATA; kappa = 1/2 FITTED; one disc excludes no model; not theory closed")
    need("all jobs present", not missing, f"missing {missing}" if missing else f"{len(J)} jobs")
    H = hashes(); t0 = all(x["frozen_unchanged"] and x["frozen_sha256_start"] == H for x in J.values()); need("T0 frozen + AL3 files unchanged in every job and now", t0)
    k0 = J.get("K0", {}).get("PASS"); need("K0 AL3 writer with options off = frozen writer", k0, f"{J.get('K0', {}).get('sha_frozen', '')[:16]} vs {J.get('K0', {}).get('sha_al3', '')[:16]}")
    k1 = [j for j, x in J.items() if "al3_cube_sha256" in x]; k1bad = [j for j in k1 if J[j]["cube_sha256"] != J[j]["al3_cube_sha256"]]
    need("K1 (a)-(d) and V3 cubes = AL3's sha256", k1 and not k1bad, f"{len(k1)} cubes, {len(k1bad)} differ {k1bad}")
    g4runs = [x["g4"] for x in J.values() if "g4" in x]; bad = [x for x in g4runs if x["detected"] and len([g for g in x["fit_log"] if g.get("mode") == "g4"]) != 6]
    zero = [g for x in g4runs for g in x["fit_log"] if g.get("mode") == "g4" and not g["I0_final"] > 0]
    need("T1 every G4 run on a detected cube: 6 G4 main fits, all final I0 > 0", not bad and not zero, f"{len(g4runs)} runs, {sum(len(x['fit_log']) for x in g4runs)} fits logged, {len(bad)} wrong count, {len(zero)} with I0 <= 0")
    machinery = all(o for n, o, _ in CHK); RES = dict(C={}, V1={}, V2={}, V3={}, V4={})
    # C
    P("\n--- C collapse calibration (frozen fitter only; class e = a + c with R_e x f) ---")
    f_ch, c_done, cj = c_state()
    for f in FLAD:
        rows = [J.get(f"C_f{f}_{i}") for i in range(6)]
        if any(r is None for r in rows): continue
        col = [r["seed"] for r in rows if collapsed(r["frozen"])]; det = sum(r["frozen"]["detected"] for r in rows)
        I0s = [round(r["frozen"]["fits"]["incl-Tadaki"]["params"][7], 6) if "incl-Tadaki" in r["frozen"]["fits"] else None for r in rows]
        RES["C"][f] = dict(detected=det, collapsed_seeds=col, I0_primary=I0s); P(f"f = {f}: detected {det}/6; primary I0 = 0 in seeds {col}; primary I0 {I0s}")
    need("C some f in {2,3,4} collapses (smallest chosen)", c_done and f_ch is not None, f"chosen f = {f_ch}")
    # V1
    P("\n--- V1 no regression (G4 on) ---"); st = J.get("V1_selftest", {})
    need("V1 selftest: all checks PASS", st.get("PASS"), ", ".join(f"{n}:{'P' if o else 'F'}" for n, o in st.get("checks", [])))
    base = json.load(open(BASE))["suites"]; v1 = bool(st.get("PASS"))
    for s in SUITES:
        for k in ("realistic", "compact", "noise"):
            rows = [J[f"V1_{s}_{k}_{i}"]["g4"] for i in range(6) if f"V1_{s}_{k}_{i}" in J]; b = base[s][k]
            fits = [r["fits"]["incl-Tadaki"] for r in rows if "incl-Tadaki" in r["fits"] and r["fits"]["incl-Tadaki"]["valid"]]
            nv = len(fits); det = sum(r["detected"] for r in rows); met = {}
            for inc in ("incl-mom0", "incl-Tadaki"):
                ff = [r["fits"][inc] for r in rows if inc in r["fits"] and r["fits"][inc]["valid"]]
                for pr, key in (("P-B", "Vc_PB"), ("P0", "Vc_P0")):
                    res_ = [f["V"][key] / truth(f["R_score"], pr) - 1 for f in ff]; met[f"{inc}|{pr}"] = dict(n=len(ff), rms=math.sqrt(sum(x * x for x in res_) / len(res_)) if ff else None)
            ok_n = nv >= b["valid_primary"]; g2r = b["metrics"]["incl-Tadaki|P-B"]["rms_fraction"]; g4r = met["incl-Tadaki|P-B"]["rms"]
            ok_r = True if not b["valid_primary"] else (g4r is not None and g4r <= g2r + 0.02)
            v1 = v1 and ok_n and ok_r; RES["V1"][f"{s}|{k}"] = dict(detected=det, valid=nv, G2_valid=b["valid_primary"], rms_TPB=g4r, G2_rms_TPB=g2r, PASS=ok_n and ok_r)
            P(f"{s:11s} {k:9s}: detected {det}/6; primary valid {nv}/6 (G2 {b['valid_primary']}/6); Tadaki P-B RMS " + (f"{g4r:.4f}" if g4r is not None else "n/a")
              + (f" (G2 {g2r:.4f})" if g2r is not None else "") + f" -> {'PASS' if ok_n and ok_r else 'FAIL'}")
    need("V1 selftest + suites: valid counts >= G2, Tadaki P-B RMS <= G2 + 0.02", v1)
    # V2
    P("\n--- V2 recovery (a, c, e) and refusal (b, d), G4 on ---"); v2 = True
    lab = dict(a="(a) offset -172", b="(b) 40% clump", c="(c) rho 0.24", d="(d) a+b+c", e=f"(e) a+c, R_e x{f_ch}")
    for c in ("a", "c", "e", "b", "d"):
        rows = [J.get(f"V2_{c}_{i}") for i in range(6)]; rows = [r for r in rows if r is not None]
        if not rows and c == "e" and c_done and f_ch is None:   # C found no f: class (e) is not drawn (G4: NOT VALIDATED via C), not a V2 failure
            RES["V2"][c] = dict(PASS=None, note="NOT DRAWN: C chose no f"); P(f"{lab[c]}: NOT DRAWN (C found no collapsing f; G4 rule: NOT VALIDATED)"); continue
        if not rows: P(f"{lab[c]}: no rows"); v2 = False; continue
        if c in ("a", "c", "e"):
            val = [r["g4"]["fits"]["incl-Tadaki"] for r in rows if "incl-Tadaki" in r["g4"]["fits"] and r["g4"]["fits"]["incl-Tadaki"]["valid"]]
            etr = [abs(f["V"]["Vc_PB"] / truth(f["R_score"], "P-B") - 1) for f in val]; e430 = [abs(f["V"]["Vc_PB"] / 430 - 1) for f in val]
            mtr = statistics.median(etr) if val else None; ok = len(val) >= 4 and mtr is not None and mtr <= 0.10; v2 = v2 and ok
            RES["V2"][c] = dict(n=len(rows), detected=sum(r["g4"]["detected"] for r in rows), valid=len(val), Vc=[f["V"]["Vc_PB"] for f in val], median_err_truth=mtr,
                                median_err_430=statistics.median(e430) if val else None, rho1=[r.get("rho1_measured") for r in rows], PASS=ok)
            P(f"{lab[c]:22s}: detected {RES['V2'][c]['detected']}/{len(rows)}; G4 primary valid {len(val)}/6; V_c P-B {[round(x) for x in RES['V2'][c]['Vc']]}; median |V/truth-1| "
              + (f"{mtr:.3f}" if val else "n/a") + (f", |V/430-1| {RES['V2'][c]['median_err_430']:.3f}" if val else "") + f" -> {'PASS' if ok else 'FAIL'}; rho1 {[round(x, 3) for x in RES['V2'][c]['rho1'] if x is not None]}")
        else:
            wrong = []; nval = 0
            for r in rows:
                for inc in ("incl-Tadaki", "incl-mom0"):
                    f = r["g4"]["fits"].get(inc)
                    if f and f["valid"]:
                        nval += 1; e = abs(f["V"]["Vc_PB"] / truth(f["R_score"], "P-B") - 1)
                        if e > 0.15: wrong.append((r["seed"], inc, round(f["V"]["Vc_PB"]), round(e, 3)))
            ok = not wrong; v2 = v2 and ok; RES["V2"][c] = dict(n=len(rows), valid_fits=nval, wrong=wrong, PASS=ok)
            P(f"{lab[c]:22s}: valid fits (both inclination branches) {nval}; confident wrong (|V/truth-1| > 0.15) {wrong} -> {'PASS (refused)' if ok else 'FAIL (mis-scored)'}")
        if any(len(r) == 0 for r in []): pass
    need("V2 (a), (c), (e) recover; (b), (d) refused", v2)
    # V3
    P("\n--- V3 no false fits (G4 on) ---"); v3 = True
    for c in V3:
        rows = [J[f"V3_{c}_{i}"]["g4"] for i in range(6) if f"V3_{c}_{i}" in J]; sc = sum(bool(r["branches"]) for r in rows); v3 = v3 and sc == 0 and len(rows) == 6
        RES["V3"][c] = dict(detected=sum(r["detected"] for r in rows), scored=sc); P(f"{c:8s}: detected {RES['V3'][c]['detected']}/6, scored {sc}/6")
    need("V3 0 of 6 scored in each class", v3)
    # V4
    P("\n--- V4 MUTATE on the V2 class-(e) cubes ---")
    rows = [J.get(f"V2_e_{i}") for i in range(6)]; rows = [r for r in rows if r is not None]
    ci = [r["seed"] for r in rows if collapsed(r["frozen"])]; cii = [r["seed"] for r in rows if collapsed(r["g4lin"])]
    RES["V4"] = dict(frozen_collapsed=ci, g4lin_collapsed=cii, g4_I0_primary=[r["g4"]["fits"].get("incl-Tadaki", {}).get("params", [None] * 8)[7] for r in rows])
    v4i = bool(ci); v4ii = bool(cii)
    need("V4 (i) frozen fitter collapses in >= 1 seed", v4i, f"seeds {ci}"); need("V4 (ii) G4 with rule 1 off collapses in >= 1 seed", v4ii, f"seeds {cii}")
    # verdict
    cpass = c_done and f_ch is not None
    if not machinery: vd = "MACHINERY FAIL (no G4 verdict)"
    elif not (v1 and v2 and v3): vd = "G4 FAILS VALIDATION"
    elif not cpass: vd = "G4 NOT VALIDATED (no f collapses: V4 cannot bite)"
    elif not v4i: vd = "G4 NOT VALIDATED (V4 i: frozen fitter does not collapse on the V2 class-(e) cubes)"
    elif not v4ii: vd = "G4 NOT VALIDATED (V4 ii: log amplitude is not what repairs it)"
    else: vd = "G4 VALIDATED"
    if missing: vd = "INCOMPLETE: " + vd
    P(f"\nVERDICT: {vd}")
    rss = max((x.get("peak_rss_MB", 0) for x in J.values()), default=0); P(f"peak RSS per job {rss:.0f} MB; total job time {sum(x.get('seconds', 0) for x in J.values()) / 3600:.1f} h")
    json.dump(dict(verdict=vd, checks=CHK, results=RES, frozen_sha256=H, note="MOCK only, NOT ALMA DATA"), open(os.path.join(HERE, "al4_validate.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, "al4_validate.out"), "w").write("\n".join(OUT) + "\n")

if __name__ == "__main__":
    if "--job" in args: run_job(opt("--job"), os.path.abspath(opt("--scratch")))
    elif "--drive" in args: drive(os.path.abspath(opt("--scratch")), int(opt("--workers", "6")))
    elif "--summary" in args: summary()
