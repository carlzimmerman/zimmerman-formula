#!/usr/bin/env python3
"""FN2 A1 (FROZEN_CRITERIA.md, 755f05c3cf): does AC1's scorer run in today's environment? Runs ac1_score.py --selftest once per
environment (default python3 on PATH; the v1.4 pinned interpreter + PYTHONPATH if it still exists), with /usr/bin/time -l, into this
lane's folder, and compares each results JSON with the committed v1.4 selftest JSON. MOCK cubes only, written to a scratch directory
outside the repo and deleted by the scorer. Writes nothing outside this lane.
    python3 -B fn2_a1_env.py SCRATCH_DIR [default|pinned|both]
kappa = 1/2 FITTED; one disc excludes no model; not theory closed."""
import hashlib, json, os, re, subprocess, sys, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
AC1 = os.path.join(ROOT, "rebuild_2026_10_22", "AC1_alma_condor_predictions"); SCORER = os.path.join(AC1, "ac1_score.py")
REV = os.path.join(ROOT, "reviews", "alma_readiness_2026_11_04", "revision_v1_4")
REF_JSON = os.path.join(REV, "selftest", "ac1_score_selftest_results.json")
SCRATCH = os.path.abspath(sys.argv[1]); WHICH = sys.argv[2] if len(sys.argv) > 2 else "both"
HOME = os.path.expanduser("~")
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def scrub(t):
    for a, b in ((SCRATCH, "<scratch>"), (ROOT, "<repo>"), (HOME, "~")): t = t.replace(a, b)
    return t

RS = json.load(open(os.path.join(REV, "run_sources.json")))
PIN_PY = "/usr/bin/python3"; PIN_PATH = None
for c in RS["commands"]:
    m = re.match(r"PYTHONPATH=(\S+) python3 ", c)
    if m: PIN_PATH = m.group(1); break
ENVS = {"default": dict(py="python3", extra={}), "pinned": dict(py=PIN_PY, extra={"PYTHONPATH": PIN_PATH})}

def versions(e):
    env = dict(os.environ, **e["extra"])
    r = subprocess.run([e["py"], "-B", "-c", "import sys, numpy, scipy, astropy; print(sys.version.split()[0], numpy.__version__, scipy.__version__, astropy.__version__, numpy.__file__)"],
                       capture_output=True, text=True, env=env)
    if r.returncode: return None
    v = r.stdout.split(); return dict(python=v[0], numpy=v[1], scipy=v[2], astropy=v[3], numpy_from=scrub(v[4]))

def run(name):
    e = ENVS[name]; od = os.path.join(HERE, f"a1_selftest_{name}"); os.makedirs(od, exist_ok=True)
    sd = os.path.join(SCRATCH, f"a1_{name}"); os.makedirs(sd, exist_ok=True)
    env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", MKL_NUM_THREADS="1", **e["extra"])
    cmd = ["nice", "-n", "15", "/usr/bin/time", "-l", e["py"], "-B", SCORER, "--selftest", sd, "--output-dir", od]
    t0 = time.time(); r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, env=env); wall = time.time() - t0
    err = scrub(r.stderr); open(os.path.join(od, "a1_selftest.time"), "w").write(err)
    rss = re.search(r"(\d+)\s+maximum resident set size", err); real = re.search(r"([\d.]+)\s+real", err)
    res = dict(env=name, command=scrub(" ".join(cmd)).replace(SCRATCH, "<scratch>"), exit=r.returncode, wall_s=round(wall, 1),
               real_s=float(real.group(1)) if real else None, peak_rss_bytes=int(rss.group(1)) if rss else None, outdir=os.path.relpath(od, ROOT))
    j = os.path.join(od, "ac1_score_selftest_results.json")
    res["results_json_sha256"] = sha(j) if os.path.exists(j) else None
    return res, (json.load(open(j)) if os.path.exists(j) else None)

TRUE = lambda x: str(x) in ("True", "true", "1")
def decisions(m):
    d = {"G1_frozen": TRUE(m["G1_frozen"]["PASS"]), "G1_3D": TRUE(m["G1_3D"]["PASS"]), "detected": TRUE(m["detected"])}
    if "flux_check" in m: d["flux30"] = TRUE(m["flux_check"]["within_30pct"])
    for nm, f in (m.get("fits") or {}).items():
        d[f"{nm}.valid"] = TRUE(f["valid"]); d[f"{nm}.G2"] = TRUE(f["G2_reached"])
    for bn, sc in (m.get("score") or {}).items():
        for k, row in sc.items():
            for rd, e in row.items(): d[f"class|{bn}|{k}|{rd}"] = e["class_"]
    return d
def numbers(m):
    n = {"G1_frozen.SN": (m["G1_frozen"]["SN"], 1.0), "G1_3D.SN": (m["G1_3D"]["SN"], 1.0)}
    for nm, f in (m.get("fits") or {}).items():
        v = f["V"]
        for k, ek in (("Vc_PB", "eVc_PB"), ("Vc_P0", "eVc_P0")): n[f"{nm}.{k}"] = (v[k], v[ek])
    return n
def fl(x):
    try: return float(x)
    except Exception: return float("nan")

def compare(new, ref):
    rows = []; worst = {}
    for kind, mr in ref["results"].items():
        mn = new["results"].get(kind)
        if mn is None: rows.append((kind, "MISSING", 1)); continue
        dr, dn = decisions(mr), decisions(mn); diff = sorted(k for k in set(dr) | set(dn) if dr.get(k) != dn.get(k))
        nr, nn = numbers(mr), numbers(mn); drift = []
        for k in nr:
            if k not in nn: drift.append((k, "missing")); continue
            a, ea = fl(nr[k][0]), fl(nr[k][1]); b = fl(nn[k][0])
            if not (a == a and b == b): continue
            tol = 0.5 if k.endswith(".SN") else (0.5 * ea if ea == ea and ea > 0 else 0.0)
            d = abs(b - a); worst[f"{kind}:{k}"] = d
            if d > tol + 1e-12: drift.append((k, f"|d| {d:.4g} > tol {tol:.4g}"))
        rows.append((kind, diff, drift))
    return rows, worst

if __name__ == "__main__":
    P("FN2 A1: AC1 scorer selftest in today's environment. MOCK cubes only, NOT ALMA DATA. kappa = 1/2 FITTED; not theory closed.")
    P(f"scorer {os.path.relpath(SCORER, ROOT)} sha256 {sha(SCORER)}; pinned in run_sources.json: {RS['sources']['rebuild_2026_10_22/AC1_alma_condor_predictions/ac1_score.py']}")
    P(f"reference v1.4 selftest JSON {os.path.relpath(REF_JSON, ROOT)} sha256 {sha(REF_JSON)}")
    ref = json.load(open(REF_JSON)); OUTJ = {"reference_sha256": sha(REF_JSON), "scorer_sha256": sha(SCORER), "runs": {}}
    for name in (("default", "pinned") if WHICH == "both" else (WHICH,)):
        e = ENVS[name]; ver = versions(e)
        if ver is None or (name == "pinned" and not (PIN_PATH and os.path.isdir(PIN_PATH))):
            P(f"\n[{name}] PINNED ENV UNAVAILABLE" if name == "pinned" else f"\n[{name}] interpreter unavailable"); OUTJ["runs"][name] = dict(label="PINNED ENV UNAVAILABLE"); continue
        P(f"\n[{name}] python {ver['python']}, numpy {ver['numpy']}, scipy {ver['scipy']}, astropy {ver['astropy']} (numpy from {ver['numpy_from']})")
        res, new = run(name); res["versions"] = ver
        checks = new["checks"] if new else []; npass = sum(1 for _, o in checks if TRUE(o))
        P(f"[{name}] exit {res['exit']}; checks {npass} of {len(checks)} PASS; wall {res['wall_s']} s; peak RSS {res['peak_rss_bytes'] / 1e9 if res['peak_rss_bytes'] else float('nan'):.3f} GB")
        for n_, o in checks: P(f"    [{'PASS' if TRUE(o) else 'FAIL'}] {n_}")
        gate = res["exit"] == 0 and len(checks) == 10 and npass == 10; res["gate_A1G"] = gate
        ident = res["results_json_sha256"] == sha(REF_JSON); res["byte_identical_to_v14"] = ident
        rows, worst = compare(new, ref) if new else ([], {})
        ndiff = sum(len(r[1]) if isinstance(r[1], list) else 1 for r in rows); ndrift = sum(len(r[2]) for r in rows if len(r) > 2)
        for kind, diff, *dr in rows:
            P(f"    {kind}: decisions differing {len(diff) if isinstance(diff, list) else diff}" + (f" {diff[:6]}" if isinstance(diff, list) and diff else "") + (f"; numbers outside tolerance {dr[0][:6]}" if dr and dr[0] else ""))
        mx = max(worst.items(), key=lambda kv: kv[1]) if worst else (None, 0.0)
        label = ("ENV FAIL" if not gate else "ENV IDENTICAL" if ident else "ENV DIFFERS" if ndiff else "ENV OK, NUMBERS DRIFT" if ndrift else "ENV OK")
        res.update(label=label, decisions_differing=ndiff, numbers_outside_tolerance=ndrift, largest_abs_difference=dict(key=mx[0], value=mx[1]))
        if name == "pinned": res["A1K_known_answer"] = "PASS" if ident else "FAIL"
        P(f"[{name}] gate A1-G {'PASS' if gate else 'FAIL'}; byte-identical to v1.4: {ident}; largest |difference| {mx[1]:.4g} ({mx[0]}); LABEL: {label}"
          + (f"; A1-K known answer {'PASS' if ident else 'FAIL'}" if name == "pinned" else ""))
        if res["peak_rss_bytes"] and res["peak_rss_bytes"] > 1e9: P(f"[{name}] note: peak RSS above 1 GB (reported, not gated)")
        OUTJ["runs"][name] = res
    tag = "" if WHICH == "both" else f"_{WHICH}"
    json.dump(OUTJ, open(os.path.join(HERE, f"fn2_a1_env{tag}.json"), "w"), indent=1)
    open(os.path.join(HERE, f"fn2_a1_env{tag}.out"), "w").write(scrub("\n".join(OUT)) + "\n")
    sys.exit(0 if all(r.get("gate_A1G", False) or r.get("label") == "PINNED ENV UNAVAILABLE" for r in OUTJ["runs"].values()) else 1)
