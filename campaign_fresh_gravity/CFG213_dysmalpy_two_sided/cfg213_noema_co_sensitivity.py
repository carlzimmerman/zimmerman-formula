#!/usr/bin/env python3
"""NOEMA3D CO-mass sensitivity of the committed lanes that use the measured-CO independent route (CFG213's Z1.4 bin, CFG215's NOEMA3D series, CFG218's NOEMA3D sample).
Why: the data chat's multi-tracer compilation (f5769b7d2, data_assembly/MULTI_TRACER_GAS_2026-09-30.md) found that Table 1's CO masses of the four CO(3-2) galaxies are 0.24 to 0.26 dex LOWER than the
paper's stated R_13 = 1.8 recipe gives from the tabulated fluxes, and G4_23011 (CO(4-3)) is 0.149 dex lower (the CO control of the reconstruction FAILS for exactly these five).  The committed lanes read the
same CO masses (logMgas_CO_P1 = Table 1 for these five).  Here each lane is re-run UNCHANGED except that the five galaxies' CO gas masses are raised by the reconstruction's residual (recipe minus table).
CFG214 (the gate compares digitised model curves with Table 3's V_c) and CFG222 (RC100 + CRISTAL only) use no NOEMA3D gas mass and are not re-run.  The scripts are exec'd read-only with ONE text substitution
(the logMgas read) and their outputs redirected to a scratch folder; committed files are not touched.  Control: with no offset every lane reproduces its committed results JSON to 1e-9.
No verdict words: a cell is reported as moved only if its committed label changes.  kappa = 1/2 FITTED; author decompositions; not a detection."""
import os, sys, io, csv, json, math, contextlib, time, tempfile
sys.dont_write_bytecode = True
import numpy as np
import matplotlib
matplotlib.use("Agg")
LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
OUT = []
T0 = time.time()


def P(s=""):
    print(s, flush=True); OUT.append(s)


P(__doc__.strip())
rec = list(csv.DictReader(open(os.path.join(REPO, "data_assembly", "multitracer_gas", "noema3d_three_tracer_reconstruction.csv"))))
OFF = {r["id"]: float(r["CO_control_residual_dex"]) for r in rec if r["CO_control_pass"].strip() in ("0", "False", "FAIL")}
P("\nCO offsets applied (dex on the CO gas mass, reconstruction minus Table 1): " + ", ".join(f"{k} {v:+.3f}" for k, v in OFF.items()))
assert len(OFF) == 5, OFF

A_GAS = 'logMgas=fnum(r["logMgas_CO_P1"])'


def PATCH213(text):
    assert text.count(A_GAS) == 1
    return text.replace(A_GAS, 'logMgas=PATCHED(r["id"], fnum(r["logMgas_CO_P1"]))')


def PATCH215(src):
    a = 'exec(compile(src213[:src213.index("BINS = {")], "cfg213", "exec"), ns)'
    b = '"__name__": "cfg213"}'
    assert src.count(a) == 1 and src.count(b) == 1
    return src.replace(a, 'exec(compile(PATCH213(src213[:src213.index("BINS = {")]), "cfg213", "exec"), ns)').replace(b, '"__name__": "cfg213", "PATCHED": PATCHED}')


def run(rel, transform, on, outdir, env=None, extra=None):
    path = os.path.join(CFG, rel)
    src = transform(open(path).read())
    assert src.count("R.write(here=LANE)") == 1
    src = src.replace("R.write(here=LANE)", "R.write(here=OUTDIR)")
    PATCHED = (lambda gid, v: v + OFF.get(gid, 0.0)) if on else (lambda gid, v: v)
    ns = {"__file__": path, "__name__": "patched_run", "PATCHED": PATCHED, "PATCH213": PATCH213, "PATCH215": PATCH215, "OUTDIR": outdir}
    ns.update(extra or {})
    _m = os.environ.pop("MUTATE", None)
    _r = os.environ.pop("RC100_INPUT", None)
    if env:
        os.environ.update(env)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                exec(compile(src, rel, "exec"), ns)
            except SystemExit:
                pass
    finally:
        if _m is not None:
            os.environ["MUTATE"] = _m
        os.environ.pop("RC100_INPUT", None)
        if _r is not None:
            os.environ["RC100_INPUT"] = _r


def leaves(x, path=()):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from leaves(v, path + (str(k),))
    elif isinstance(x, (list, tuple)):
        for i, v in enumerate(x):
            yield from leaves(v, path + (str(i),))
    else:
        yield path, x


def diff(a, b):
    A, B = dict(leaves(a)), dict(leaves(b))
    num, strs, missing = [], [], 0
    for k in set(A) | set(B):
        if k not in A or k not in B:
            missing += 1; continue
        x, y = A[k], B[k]
        if isinstance(x, (int, float)) and isinstance(y, (int, float)) and not isinstance(x, bool):
            if not (math.isnan(x) and math.isnan(y)) and abs(x - y) > 1e-9:
                num.append((k, x, y))
        elif x != y:
            strs.append((k, x, y))
    return num, strs, missing


def PATCH218(src):
    a = 'src = open(os.path.join(CFG, "CFG215_decomposition_timeline", "cfg215_timeline.py")).read()'
    b = '"__name__": "cfg215"}'
    c = 'J215 = json.load(open(os.path.join(CFG, "CFG215_decomposition_timeline", "cfg215_timeline_results.json")))["numbers"]'
    d = 'plt.savefig(os.path.join(LANE, "cfg218_ladder" + SFX + ".png"), dpi=150)'
    for t in (a, b, c, d):
        assert src.count(t) == 1, t[:50]
    return (src.replace(a, 'src = PATCH215(open(os.path.join(CFG, "CFG215_decomposition_timeline", "cfg215_timeline.py")).read())')
               .replace(b, '"__name__": "cfg215", "PATCHED": PATCHED, "PATCH213": PATCH213}')
               .replace(c, 'J215 = json.load(open(J215PATH))["numbers"]')
               .replace(d, 'plt.savefig(os.path.join(OUTDIR, "cfg218_ladder" + SFX + ".png"), dpi=60)'))


LANES = [("CFG213", "CFG213_dysmalpy_two_sided/cfg213_two_sided.py", lambda s: PATCH213(s), "CFG213_dysmalpy_two_sided/cfg213_two_sided_results.json"),
         ("CFG215", "CFG215_decomposition_timeline/cfg215_timeline.py", PATCH215, "CFG215_decomposition_timeline/cfg215_timeline_results.json")]
SCR = tempfile.mkdtemp(prefix="cfg213co_")
RESULT = {}
PATCHED_215_JSON = None


def one(name, rel, tr, committed, env=None, slug_override=None, extra_fn=None):
    global PATCHED_215_JSON
    J0 = json.load(open(os.path.join(CFG, committed)))["numbers"]
    out = {}
    for on in (False, True):
        od = os.path.join(SCR, f"{name}_{'patched' if on else 'baseline'}")
        os.makedirs(od)
        t = time.time()
        run(rel, tr, on, od, env=env, extra=(extra_fn(on, od) if extra_fn else None))
        slug = os.path.basename(committed).replace("_results.json", "")
        J1 = json.load(open(os.path.join(od, slug + "_results.json")))["numbers"]
        num, strs, miss = diff(J0, J1)
        if not on:
            ok = len(num) == 0 and len(strs) == 0 and miss == 0
            P(f"\n[{'PASS' if ok else 'FAIL'}] CONTROL {name}: with no offset the re-run reproduces the committed results JSON (numeric differences {len(num)}, label differences {len(strs)}, missing keys {miss}; {time.time() - t:.0f} s)")
            RESULT[(name, "control")] = ok
        else:
            P(f"\n{name}: with the five CO masses raised: {len(num)} numeric leaves move (max |change| {max([abs(x - y) for _, x, y in num] or [0.0]):.3f}), {len(strs)} label leaves change, {miss} keys missing  ({time.time() - t:.0f} s)")
            for k, x, y in strs[:60]:
                P("    LABEL " + "/".join(k) + f": {x!r} -> {y!r}")
            NO = [(k, x, y) for k, x, y in num if any("NOEMA" in part or "Z1.4" in part for part in k)]
            P(f"    numeric leaves with NOEMA3D in their key: {len(NO)} (of {len(num)} that move); largest 6 by |change|:")
            for k, x, y in sorted(NO, key=lambda t: -abs(t[1] - t[2]))[:6]:
                P(f"      {'/'.join(k)}: {x:+.4f} -> {y:+.4f}")
            RESULT[(name, "labels")] = len(strs)
            out = dict(J0=J0, J1=J1, od=od, strs=strs, num=num)
    return out


for name, rel, tr, committed in LANES:
    o = one(name, rel, tr, committed)
    if name == "CFG215":
        J0, J1 = o["J0"], o["J1"]
        PATCHED_215_JSON = os.path.join(o["od"], "cfg215_timeline_results.json")
        P("\n  CFG215 T1 / T2 (primary series, nu_mono canonical), committed -> with the five CO masses raised:")
        for k, v in (("flat", None), ("rival", None)):
            a0, a1 = J0["T2"][k], J1["T2"][k]
            P(f"    T2 {k:5s}: across-sample slope {a0['across'][0]:+.3f} [{a0['across'][1]:+.4f}, {a0['across'][2]:+.3f}] -> {a1['across'][0]:+.3f} [{a1['across'][1]:+.4f}, {a1['across'][2]:+.3f}];  label '{a0['label']}' -> '{a1['label']}'")
        P(f"    T1 primary: {J0['T1_primary']['consistent_in_all']} -> {J1['T1_primary']['consistent_in_all']};  verdicts flat {J0['T1_primary']['verdicts']['flat']} -> {J1['T1_primary']['verdicts']['flat']};  rival {J0['T1_primary']['verdicts']['rival']} -> {J1['T1_primary']['verdicts']['rival']}")
        for k, x, y in o["num"]:
            if k[0] in ("bias", "BIAS", "b_s") or "bias" in "/".join(k).lower():
                P(f"    {'/'.join(k)}: {x:+.4f} -> {y:+.4f}")

for mode, env, tag in (("", None, ""), ("corrected", {"RC100_INPUT": "corrected"}, "_corrected")):
    committed = f"CFG218_signal_vs_systematic/cfg218_ladder{tag}_results.json"
    def extra_fn(on, od, tag=tag):
        return {"J215PATH": (PATCHED_215_JSON if on else os.path.join(CFG, "CFG215_decomposition_timeline", "cfg215_timeline_results.json")), "PATCH215": PATCH215}
    one("CFG218" + (" [" + mode + " RC100]" if mode else ""), "CFG218_signal_vs_systematic/cfg218_ladder.py", PATCH218, committed, env=env, extra_fn=extra_fn)
P("\nCFG214: no gas mass enters (the gate compares the digitised model V with Table 3's V_c): unchanged.  CFG222: no NOEMA3D row is scored: unchanged.")
open(os.path.join(LANE, "cfg213_noema_co_sensitivity.out"), "w").write("\n".join(OUT) + "\n")
