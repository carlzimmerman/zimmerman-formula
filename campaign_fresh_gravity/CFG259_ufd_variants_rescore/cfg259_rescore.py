#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG259 -- re-score candidate B's ultra-faint offset (CFG28/29 statistic and error model, exactly) and CFG244's Gate H bound-core lean under five
data variants of the 40 ultra-faint dispersions (DV0 committed LVD; DV1 DEIMOS where matched; DV2 Arroyo-Polonio+26 free-f log ratio on the eight;
DV3 f = 0.7 ratio; DV4 = DV1 then DV2).  Frozen criteria: FROZEN_CRITERIA.md (committed cd8aa9856), written before this script and before any variant number.
The record's code is exec'd READ-ONLY (CFG28's prefix: FG001's loader and estimator, offsets, Kaplan-Meier, bootstrap; CFG244 Gate H's prefix: the readings,
the scoring, the classes); the inputs are the committed CFG257 tables.  Nothing is downloaded; no record file is written.
Run: python3 cfg259_rescore.py   |   MUTATE=1 (a -0.33 dex plant on every ultra-faint) / MUTATE=2 (plants on the eight only) / MUTATE=3 (wrong denominator)  python3 cfg259_rescore.py
Exit: main 0 (1 if a control fails); MUTATE exits 1 when the control BITES (as CFG28/29/244), 0 otherwise.
kappa = 1/2 FITTED; no dark-matter particle; the mass is required; nothing here is closure.
"""
import os, sys, io, csv, json, math, time, contextlib
sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
C257 = os.path.join(LANES, "CFG257_ufd_kinematics_scoping")
MUT = os.environ.get("MUTATE", "").strip()
SFX = f"_MUTATE{MUT}" if MUT else ""
T0 = time.time()
LOG = []


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


P(__doc__.split("Run: python3")[0].strip())
P(f"\n  mode: {'MUTATE=' + MUT if MUT else 'main'}")

# ================================================================================================ the record's code, exec'd read-only
def exec_prefix_file(path, marker, env_mut, extra_paths=()):
    src = open(path).read()
    pre = src[:src.index(marker)]
    g = {"__file__": path, "__name__": "prefix_" + os.path.basename(path)}
    _e = os.environ.get("MUTATE")
    os.environ["MUTATE"] = env_mut
    for p_ in extra_paths:
        sys.path.insert(0, p_)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(pre, path, "exec"), g)
    finally:
        if _e is None:
            os.environ.pop("MUTATE", None)
        else:
            os.environ["MUTATE"] = _e
    return g


BAR = "# ================================================================================================ "
G28 = exec_prefix_file(os.path.join(LANES, "CFG28_ufd_referee.py"), BAR + "C1", "0", extra_paths=(LANES,))
H44 = exec_prefix_file(os.path.join(LANES, "CFG244_bound_fluid", "CFG244_H_satellites.py"), BAR + "main", "", extra_paths=(os.path.join(LANES, "CFG244_bound_fluid"),))
A0H = G28["A0H"]
FOOTS = ("canonical", "alt")
assert set(A0H) == set(FOOTS)

# the record's base values (copies), by name
BASE28_R = [dict(d) for d in G28["UFD"]]; BASE28_L = [dict(d) for d in G28["UL"]]
BASE44_R = [dict(d) for d in H44["SAMPLES"]["ufd"]]; BASE44_L = [dict(d) for d in H44["UL"]]
BASE_SIG = {d["name"]: float(d["sig"]) for d in BASE28_R}
BASE_UL = {d["name"]: float(d["sig_ul"]) for d in BASE28_L}
ORDER = [d["name"] for d in BASE28_R] + [d["name"] for d in BASE28_L]


def set_data(val):
    """val: name -> (sigma, is_limit); systems absent from val are dropped.  Rebinds the sample lists in BOTH of the record's namespaces (copies of the dicts)."""
    r28 = [dict(d, sig=val[d["name"]][0]) for d in BASE28_R if d["name"] in val and not val[d["name"]][1]]
    l28 = [dict(d, sig_ul=val[d["name"]][0]) for d in BASE28_L if d["name"] in val and val[d["name"]][1]]
    r44 = [dict(d, sig=val[d["name"]][0]) for d in BASE44_R if d["name"] in val and not val[d["name"]][1]]
    l44 = [dict(d, sig_ul=val[d["name"]][0]) for d in BASE44_L if d["name"] in val and val[d["name"]][1]]
    assert len(r28) == len(r44) and len(l28) == len(l44)
    G28["UFD"], G28["UL"] = r28, l28
    H44["SAMPLES"]["ufd"], H44["UL"] = r44, l44


def reset_data():
    G28["UFD"], G28["UL"] = [dict(d) for d in BASE28_R], [dict(d) for d in BASE28_L]
    H44["SAMPLES"]["ufd"], H44["UL"] = [dict(d) for d in BASE44_R], [dict(d) for d in BASE44_L]


# ================================================================================================ the inputs (committed CFG257 tables) and the five variants
def fnum(s):
    s = (s or "").strip()
    return float(s) if s not in ("", "-999") else None


ARR_ROWS = list(csv.DictReader(open(os.path.join(C257, "arroyo_polonio2026_tableA1.csv"))))
EIGHT = [r for r in ARR_ROWS if r["in_cfg28_29_sample"].strip() == "1"]
EIGHT_NAMES = [r["lvd_name"] for r in EIGHT]
MATCH_ALL = list(csv.DictReader(open(os.path.join(C257, "geha_vs_lvd_match.csv"))))
MATCHED = [r for r in MATCH_ALL if r["match_method"].strip()]


class StatusMismatch(Exception):
    pass


def build(dv, booIII_keep=False, booI=None, plant_all=0.0, plant_eight=0.0, wrong_denom=False):
    """returns (val, change): val name -> (sigma, is_limit); change name -> log10(new / base).  booI in {None, 'own', float, 'drop'}."""
    val = {n: (v, False) for n, v in BASE_SIG.items()}
    val.update({n: (v, True) for n, v in BASE_UL.items()})
    if dv in ("DV1", "DV4"):
        for r in MATCHED:
            n = r["lvd_name"]
            if booIII_keep and n == "Bootes III":
                continue
            resolved = r["geha_sigma_resolved"].strip() == "1"
            new, islim = (fnum(r["geha_sigma"]), False) if resolved else (fnum(r["geha_sigma_ul95"]), True)
            if val[n][1] != islim:
                raise StatusMismatch(f"{n}: LVD limit={val[n][1]} but DEIMOS limit={islim}")
            val[n] = (new, islim)
    if dv in ("DV2", "DV3", "DV4"):
        col = "sig_free" if dv in ("DV2", "DV4") else "sig_f07"
        den = "sig_lit" if wrong_denom else "sig_f0"
        for r in EIGHT:
            n = r["lvd_name"]
            assert not val[n][1]
            val[n] = (val[n][0] * (fnum(r[col]) / fnum(r[den])), False)
    if plant_eight:
        for n in EIGHT_NAMES:
            val[n] = (val[n][0] * 10 ** plant_eight, val[n][1])
    if plant_all:
        val = {n: (v * 10 ** plant_all, lim) for n, (v, lim) in val.items()}
    if booI is not None and booI != "own":
        if booI == "drop":
            val.pop("Bootes I")
        else:
            val["Bootes I"] = (float(booI), False)
    base = {n: v for n, v in BASE_SIG.items()}; base.update(BASE_UL)
    change = {n: math.log10(val[n][0] / base[n]) for n in val}
    return val, change


# ================================================================================================ the statistics (the record's, unchanged)
def S1():
    """CFG28's T1 + T5 on the current data: KM median, bootstrap error (2000, seed 28), floor, z; both footings."""
    off, km, boot = G28["offsets"], G28["km_median"], G28["boot"]
    out = {}
    for foot, a0 in A0H.items():
        x, xu = off(a0)
        m = km(x, xu); e = boot(km, x, xu)
        var = [km(*off(a0, ups=u)) for u in (1.0, 2.0, 4.0)] + [km(*off(a0, deep=True))]
        floor = 0.5 * (max(var) - min(var))
        out[foot] = dict(med=float(m), err=float(e), floor=float(floor), var=[float(v) for v in var], z=float(m / math.sqrt(e ** 2 + floor ** 2)), n=int(len(x)), nu=int(len(xu)))
    return out


def S2(s1):
    """CFG29's headline rows (predicted sigma >= 1.5, >= 2.0, < 1.5 km/s) with the variant's own T5 floor."""
    km, boot, spred = G28["km_median"], G28["boot"], G28["spred"]
    out = {}
    for foot, a0 in A0H.items():
        UFD, UL = G28["UFD"], G28["UL"]
        sp = np.array([spred(d, a0) for d in UFD]); spu = np.array([spred(d, a0) for d in UL])
        so = np.array([d["sig"] for d in UFD]); su = np.array([d["sig_ul"] for d in UL])
        x, xu = np.log10(so / sp), np.log10(su / spu)
        rows = {}
        for lab, cut_, cutu in (("pred >= 1.5", sp >= 1.5, spu >= 1.5), ("pred >= 2.0", sp >= 2.0, spu >= 2.0), ("pred < 1.5", sp < 1.5, spu < 1.5)):
            m = km(x[cut_], xu[cutu]); e = boot(km, x[cut_], xu[cutu])
            rows[lab] = dict(med=float(m), err=float(e), z=float(m / math.sqrt(e ** 2 + s1[foot]["floor"] ** 2)), n=int(cut_.sum()), nu=int(cutu.sum()))
        need = np.sqrt(np.maximum(so ** 2 - sp ** 2, 0.0))
        out[foot] = dict(rows=rows, floor=s1[foot]["floor"], median_binary_floor_needed=float(np.median(need)))
    return out


def S3(kernels=("P2", "RAR"), seed=None):
    """CFG244 Gate H, exactly (recipe C42, 2000 resamples, seed 244001 unless a seed is given): per kernel the classes, Delta chi2 in views V1/V2 on both footings, the ultra-faint offsets."""
    out = {}
    for kern in kernels:
        kw = dict(kernel=kern, recipe="C42")
        if seed is not None:
            kw["seed"] = seed
        o, res, cls, b_ok, zb = H44["run_all"](**kw)
        d = {}
        for foot in FOOTS:
            for view in ("V1", "V2"):
                r = res[(foot, view)]
                d[f"{foot}|{view}"] = dict(delta=float(r["delta"]), chi2_a=float(r["chi2_a"]), chi2_b=float(r["chi2_b"]), a_best=r["a_best"])
            d[f"{foot}|P1_a1"] = {k: float(v) for k, v in o["a"][foot]["a1"]["P1"].items()}
            for view in ("V1", "V2"):
                d[f"{foot}|P1_b_{view}"] = {k: float(v) for k, v in o["b"][foot][view]["P1"].items()}
        d["cls"] = cls; d["b_ok"] = bool(b_ok); d["z_b"] = {k: float(v) for k, v in zb.items()}
        out[kern] = d
    if "P2" in out and "RAR" in out:
        out["final"] = out["P2"]["cls"] if out["P2"]["cls"] == out["RAR"]["cls"] else "H4"
    return out


def dec_B(s1):
    if all(s1[f]["med"] > 0.2 and s1[f]["z"] > 3.0 for f in FOOTS):
        return "SURVIVES"
    if all(s1[f]["med"] > 0 and s1[f]["z"] >= 2.0 for f in FOOTS):
        return "WEAKENED"
    return "LOST"


def dec_G(s3, ref):
    d2 = [s3[k][f"{f}|V2"]["delta"] for k in ("P2", "RAR") for f in FOOTS]
    if any(v <= 0 for v in d2):
        return "GONE"
    if s3["P2"]["cls"] == ref["P2"]["cls"] and s3["final"] == ref["final"]:
        return "INTACT"
    if s3["P2"]["cls"] != "H2":
        return "WEAKER"
    return "STRONGER (not named in the frozen lines: P2 class H2 kept, final class changed)"


def jc(o):
    if isinstance(o, dict):
        return {str(k): jc(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jc(v) for v in o]
    if isinstance(o, np.generic):
        return o.item()
    if isinstance(o, np.ndarray):
        return jc(o.tolist())
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return None
    return o


CK = []
RES = {}


def check(name, detail, ok, kind="control"):
    CK.append(dict(name=name, detail=detail, ok=bool(ok), kind=kind))
    P(f"  [{'PASS' if ok else 'FAIL'}] ({kind}) {name}\n         {detail}")


def finish(extra_exit=None):
    RES["checks"] = CK; RES["seconds"] = round(time.time() - T0, 1)
    json.dump(jc(RES), open(os.path.join(HERE, f"cfg259_rescore{SFX}_results.json"), "w"), indent=1)
    open(os.path.join(HERE, f"cfg259_rescore{SFX}.out"), "w").write("\n".join(LOG) + "\n")


# ================================================================================================ controls shared by every mode
def indep_log_ratio(col, name, den="sig_f0"):
    """an independent code path (csv.reader, column indices) for the expected log10(col / den) of one Arroyo row"""
    with open(os.path.join(C257, "arroyo_polonio2026_tableA1.csv")) as f:
        rd = csv.reader(f); head = next(rd); ix = {h: i for i, h in enumerate(head)}
        for row in rd:
            if row[ix["lvd_name"]] == name:
                return math.log10(float(row[ix[col]]) / float(row[ix[den]]))
    raise KeyError(name)


P("\n" + "=" * 110 + "\nCONTROLS\n" + "=" * 110)
# C1 reproduction at DV0 against the committed record
reset_data()
set_data(build("DV0")[0])
s1_0 = S1(); s2_0 = S2(s1_0); s3_0 = S3()
c28 = json.load(open(os.path.join(LANES, "CFG28_ufd_referee_results.json")))["numbers"]["RES"]
c29 = json.load(open(os.path.join(LANES, "CFG29_ufd_binary_audit_results.json")))["numbers"]["H1"]
c44 = json.load(open(os.path.join(LANES, "CFG244_bound_fluid", "CFG244_H_satellites_results.json")))["numbers"]
dev28 = max(max(abs(s1_0[f]["med"] - c28[f]["km"][0]), abs(s1_0[f]["err"] - c28[f]["km"][1]), abs(s1_0[f]["floor"] - c28[f]["floor"]), abs(s1_0[f]["z"] - c28[f]["z_km"])) for f in FOOTS)
dev29 = max(max(abs(s2_0[f]["rows"][k]["med"] - c29[f]["rows"][k]["med"]), abs(s2_0[f]["rows"][k]["err"] - c29[f]["rows"][k]["err"]), abs(s2_0[f]["rows"][k]["z"] - c29[f]["rows"][k]["z"]))
            for f in FOOTS for k in c29[f]["rows"])
dev44 = 0.0
for kern, key in (("P2", "primary"), ("RAR", "rar_kernel")):
    for f in FOOTS:
        for v in ("V1", "V2"):
            dev44 = max(dev44, abs(s3_0[kern][f"{f}|{v}"]["delta"] - c44[key]["res"][f"{f}|{v}"]["delta"]))
cls_ok = (s3_0["P2"]["cls"] == c44["primary"]["outcome"]) and (s3_0["RAR"]["cls"] == c44["rar_kernel"]["outcome"]) and (s3_0["final"] == c44["final_outcome"])
same_samples = ([(d["name"], d["sig"]) for d in BASE28_R] == [(d["name"], d["sig"]) for d in BASE44_R]) and ([(d["name"], d["sig_ul"]) for d in BASE28_L] == [(d["name"], d["sig_ul"]) for d in BASE44_L])
check("C1 CONTROL (reproduction at DV0): S1 = CFG28's committed RES, S2 = CFG29's committed rows, S3 = CFG244's committed Gate H (both kernels, classes) to 1e-9; CFG28's and CFG244's samples identical",
      f"max |d|: S1 {dev28:.1e}, S2 {dev29:.1e}, S3 {dev44:.1e}; classes P2 {s3_0['P2']['cls']} / RAR {s3_0['RAR']['cls']} / final {s3_0['final']} (committed {c44['primary']['outcome']} / {c44['rar_kernel']['outcome']} / {c44['final_outcome']}); samples identical: {same_samples}",
      max(dev28, dev29, dev44) < 1e-9 and cls_ok and same_samples)
RES["DV0_reference"] = dict(S1=s1_0, S2=s2_0, S3=s3_0)

# C2 the data build
def c2_check(wrong=False):
    """the data build: counts, per-system log changes against an independent recomputation, the scoping's medians and ranges; returns (ok, detail)"""
    msgs = []; ok = True
    try:
        v1, ch1 = build("DV1")
    except StatusMismatch as e:
        return False, "DV1 status mismatch: " + str(e)
    nres = sum(1 for r in MATCHED if r["geha_sigma_resolved"].strip() == "1"); nlim = len(MATCHED) - nres
    changed1 = sorted(n for n, c in ch1.items() if abs(c) > 1e-12)
    exp_changed = sorted(["Bootes I", "Bootes III", "Eridanus IV", "Willman 1", "Aquarius III", "Draco II"])
    ok &= (len(MATCHED) == 19 and nres == 15 and nlim == 4 and changed1 == exp_changed)
    msgs.append(f"DV1: {len(MATCHED)} matched ({nres} resolved + {nlim} limits), changed {changed1} (13 equal: {len(MATCHED) - len(changed1)})")
    for dv, col, med_exp, lo_exp, hi_exp in (("DV2", "sig_free", -0.068, -0.168, -0.018), ("DV3", "sig_f07", -0.104, -0.238, -0.053)):
        v, ch = build(dv, wrong_denom=wrong)
        moved = sorted(n for n, c in ch.items() if abs(c) > 1e-12)
        d_eight = {n: ch[n] for n in EIGHT_NAMES}
        dev = max(abs(d_eight[n] - indep_log_ratio(col, n)) for n in EIGHT_NAMES)
        n_bad = sum(1 for n in EIGHT_NAMES if abs(d_eight[n] - indep_log_ratio(col, n)) > 1e-6)
        ex = sorted(d_eight.values())
        med = float(np.median(ex))
        ok_ = (moved == sorted(EIGHT_NAMES)) and dev <= 1e-12 and abs(med - med_exp) <= 0.002 and abs(ex[0] - lo_exp) <= 0.002 and abs(ex[-1] - hi_exp) <= 0.002
        ok &= ok_
        msgs.append(f"{dv}: moved {len(moved)} systems (the eight: {moved == sorted(EIGHT_NAMES)}); max |d| to the independent log10({col}/sig_f0) {dev:.1e} ({n_bad} of 8 differ by > 1e-6); median {med:+.3f} (scoping {med_exp:+.3f}), range {ex[0]:+.3f} to {ex[-1]:+.3f} (scoping {lo_exp:+.3f} to {hi_exp:+.3f})")
    v4, ch4 = build("DV4"); ch1_, ch2_ = build("DV1")[1], build("DV2")[1]
    dev4 = max(abs(ch4[n] - ch1_[n] - ch2_[n]) for n in ch4)
    ok &= dev4 <= 1e-12
    msgs.append(f"DV4: per-system change = DV1's + DV2's, max |d| {dev4:.1e}")
    return bool(ok), "; ".join(msgs)


ok2, det2 = c2_check(wrong=(MUT == "3"))
if MUT != "3":
    check("C2 CONTROL (the data build): DV1 exactly the 19 matched rows with agreeing status and the six named changes; DV2 / DV3 move exactly the eight by log10(sig_free (sig_f07) / sig_f0), equal to an independent recomputation (1e-12) and to the scoping's medians and ranges (0.002); DV4 = DV1 + DV2", det2, ok2)
else:
    P(f"  (MUTATE=3: the build uses sig_lit as the denominator) C2 on the mutated build: {'PASS' if ok2 else 'FAIL'}\n         {det2}")
    RES["mutate3_c2_ok"] = ok2

# C3 reactivity: a uniform plant shifts the KM median exactly and leaves the error and floor unchanged
if MUT in ("", "1"):
    ok3 = True; rows3 = []
    for c in (-0.05, -0.10, -0.20, -0.33):
        set_data(build("DV0", plant_all=c)[0]); s = S1()
        for f in FOOTS:
            dm, de, dfl = s[f]["med"] - s1_0[f]["med"] - c, s[f]["err"] - s1_0[f]["err"], s[f]["floor"] - s1_0[f]["floor"]
            ok3 &= abs(dm) < 1e-9 and abs(de) < 1e-9 and abs(dfl) < 1e-9
            rows3.append(f"c {c:+.2f} {f}: median shift - c {dm:.1e}, error change {de:.1e}, floor change {dfl:.1e}")
    reset_data()
    check("C3 CONTROL (reactivity, the CFG219 lesson): a uniform plant c on every ultra-faint shifts B's KM median by exactly c and leaves the bootstrap error and the floor unchanged (1e-9)", "; ".join(rows3[:4]) + " ...", ok3)

# C4 seed determinism and liveness (Gate H bootstrap)
reset_data(); set_data(build("DV0")[0])
a = S3(("P2",), seed=259001)["P2"]; b = S3(("P2",), seed=259001)["P2"]; c = S3(("P2",), seed=259002)["P2"]
same = all(a[k]["delta"] == b[k]["delta"] for k in a if isinstance(a[k], dict) and "delta" in a[k])
diff = any(a[k]["delta"] != c[k]["delta"] for k in a if isinstance(a[k], dict) and "delta" in a[k])
check("C4 CONTROL (seed determinism and liveness): the same seed returns the identical Gate H deltas, a different seed does not", f"same seed identical: {same}; different seed differs: {diff}", same and diff)
reset_data()

# ================================================================================================ the variants
VARS = ("DV0", "DV1", "DV2", "DV3", "DV4")
DESC = {"DV0": "the committed LVD values", "DV1": "DEIMOS (Geha 2026) where matched (19 rows)", "DV2": "Arroyo-Polonio+26 free-f log ratio on the eight",
        "DV3": "Arroyo-Polonio+26 f = 0.7 log ratio on the eight", "DV4": "DV1 then DV2"}


def run_variant(dv, **kw):
    reset_data(); set_data(build(dv, **kw)[0])
    s1 = S1(); s2 = S2(s1); s3 = S3()
    reset_data()
    return dict(S1=s1, S2=s2, S3=s3)


if MUT == "":
    P("\n" + "=" * 110 + "\nTHE FIVE VARIANTS (each: S1 = candidate B with the CFG28 / CFG29 statistic and error model; S3 = CFG244 Gate H)\n" + "=" * 110)
    V = {}
    CH = {}
    for dv in VARS:
        V[dv] = run_variant(dv) if dv != "DV0" else dict(S1=s1_0, S2=s2_0, S3=s3_0)
        CH[dv] = build(dv)[1]
    RES["variants"] = V; RES["changes"] = CH
    P("\n  per-system log10 changes against DV0 (dex; only systems that change):")
    for dv in VARS[1:]:
        P(f"   {dv} ({DESC[dv]}): " + ", ".join(f"{n} {c:+.3f}" for n, c in CH[dv].items() if abs(c) > 1e-12))
    P("\n  CANDIDATE B (CFG28 T1 + T5): KM median (dex) +- bootstrap error, systematic floor, z, status by D-B; shift against DV0 and the binary share")
    P(f"  {'variant':6s} {'footing':9s} {'median':>8s} {'err':>6s} {'floor':>6s} {'z':>5s}  {'n+lim':>6s} {'dMedian':>8s} {'share':>7s}   status")
    stat_B = {}
    for dv in VARS:
        st = dec_B(V[dv]["S1"]); stat_B[dv] = st
        for f in FOOTS:
            s = V[dv]["S1"][f]; d = s["med"] - V["DV0"]["S1"][f]["med"]
            P(f"  {dv:6s} {f:9s} {s['med']:+8.4f} {s['err']:6.3f} {s['floor']:6.3f} {s['z']:5.2f}  {s['n']}+{s['nu']:<3d} {d:+8.4f} {100 * (-d) / V['DV0']['S1'][f]['med']:+6.1f}%   {st if f == 'alt' else ''}")
    P("\n  CFG29 headline rows (predicted sigma >= 1.5 / >= 2.0 / < 1.5 km/s; the variant's own floor): median +- error (z)")
    for dv in VARS:
        for f in FOOTS:
            r = V[dv]["S2"][f]["rows"]
            P(f"  {dv:6s} {f:9s} " + "; ".join(f"{k}: {v['med']:+.3f} +- {v['err']:.3f} ({v['z']:.1f}sigma, {v['n']}+{v['nu']})" for k, v in r.items()) + f"; median binary floor needed {V[dv]['S2'][f]['median_binary_floor_needed']:.2f} km/s")
    P("\n  CFG244 GATE H (P2 kernel primary; RAR kernel cross-check): ultra-faint offsets and Delta chi2 = chi2_a - chi2_b; class per kernel; FINAL (cautious) class; D-G")
    P(f"  {'variant':6s} {'foot':9s} {'(a1) P1':>14s} {'(b) V1 P1':>16s} {'(b) V2 P1':>16s} | {'P2 d_V1':>8s} {'P2 d_V2':>8s} {'RAR d_V1':>8s} {'RAR d_V2':>8s}")
    stat_G = {}
    for dv in VARS:
        s3 = V[dv]["S3"]
        stat_G[dv] = dec_G(s3, V["DV0"]["S3"])
        for f in FOOTS:
            a1 = s3["P2"][f"{f}|P1_a1"]; b1 = s3["P2"][f"{f}|P1_b_V1"]; b2 = s3["P2"][f"{f}|P1_b_V2"]
            P(f"  {dv:6s} {f:9s} {a1['off']:+.3f} ({a1['z']:+.2f}) {b1['off']:+.3f} ({b1['z']:+.2f}) {b2['off']:+.3f} ({b2['z']:+.2f}) | {s3['P2'][f'{f}|V1']['delta']:+8.2f} {s3['P2'][f'{f}|V2']['delta']:+8.2f} {s3['RAR'][f'{f}|V1']['delta']:+8.2f} {s3['RAR'][f'{f}|V2']['delta']:+8.2f}")
        P(f"  {dv:6s} classes: P2 {s3['P2']['cls']}, RAR {s3['RAR']['cls']}, FINAL {s3['final']};  (b) acceptable (P2): {s3['P2']['b_ok']};  D-G: {stat_G[dv]}")
    RES["status_B"] = stat_B; RES["status_G"] = stat_G

    # ---------------------------------------------------------------- reported rows
    P("\n" + "=" * 110 + "\nREPORTED ROWS (none changes a verdict)\n" + "=" * 110)
    # (1) the Boo I conflict, without picking a side
    P("\n  THE BOO I CONFLICT (multi-epoch 4.0 km/s, Sandford+26, the LVD value; Arroyo-Polonio's single-epoch free-f value 2.18; DEIMOS 3.19), stated without picking a side.")
    P("  Boo I = the variant's own value / 4.0 / 2.18 / dropped.  B's KM median (canonical | alt) and z; reading (b) P1 offset and P2 Delta chi2_V2 (canonical | alt) and class (P2 kernel only)")
    BI = {}
    for dv in VARS:
        for state in ("own", 4.0, 2.18, "drop"):
            reset_data(); set_data(build(dv, booI=state)[0]); s1 = S1(); s3 = S3(("P2",)); reset_data()
            BI[f"{dv}|{state}"] = dict(S1=s1, S3=s3["P2"])
            P(f"   {dv} Boo I {str(state):5s}: B {s1['canonical']['med']:+.4f} ({s1['canonical']['z']:.2f}sigma) | {s1['alt']['med']:+.4f} ({s1['alt']['z']:.2f}sigma);  (b) V2 {s3['P2']['canonical|P1_b_V2']['off']:+.4f} | {s3['P2']['alt|P1_b_V2']['off']:+.4f};  "
              f"d_V2 {s3['P2']['canonical|V2']['delta']:+.2f} | {s3['P2']['alt|V2']['delta']:+.2f}  class {s3['P2']['cls']}")
    RES["booI"] = BI
    # (2) Boo III kept at the LVD value in DV1 / DV4
    P("\n  BOO III KEPT AT ITS LVD VALUE (1.69 km/s; a tidally disrupting system matched to DEIMOS by name at 0.34 deg), DV1b / DV4b:")
    B3 = {}
    for dv in ("DV1", "DV4"):
        r_ = run_variant(dv, booIII_keep=True); B3[dv + "b"] = r_
        P(f"   {dv}b: B {r_['S1']['canonical']['med']:+.4f} ({r_['S1']['canonical']['z']:.2f}) | {r_['S1']['alt']['med']:+.4f} ({r_['S1']['alt']['z']:.2f});  (b) V2 {r_['S3']['P2']['canonical|P1_b_V2']['off']:+.4f};  "
          f"P2 d_V2 {r_['S3']['P2']['canonical|V2']['delta']:+.2f} | {r_['S3']['P2']['alt|V2']['delta']:+.2f}, P2 {r_['S3']['P2']['cls']} RAR {r_['S3']['RAR']['cls']} FINAL {r_['S3']['final']}  D-B {dec_B(r_['S1'])}  D-G {dec_G(r_['S3'], V['DV0']['S3'])}")
    RES["booIII_keep"] = B3
    # (3) the eight-only response curve
    P("\n  THE EIGHT ALONE (a planted c on the eight Arroyo systems at DV0): B's KM median (canonical | alt) and shift against DV0")
    EC = {}
    for c in (0.0, -0.10, -0.20, -0.33, -0.50):
        reset_data(); set_data(build("DV0", plant_eight=c)[0]); s1 = S1(); reset_data()
        EC[str(c)] = s1
        P(f"   c {c:+.2f}: {s1['canonical']['med']:+.4f} | {s1['alt']['med']:+.4f}   shift {s1['canonical']['med'] - s1_0['canonical']['med']:+.4f} | {s1['alt']['med'] - s1_0['alt']['med']:+.4f}")
    RES["eight_response"] = EC
    # (4) 20-seed stability of Gate H (P2 kernel)
    P("\n  20-SEED STABILITY of the P2-kernel Gate H (seeds 259001-259020): fraction of seeds with class H2, mean +- SD of Delta chi2_V2 (canonical | alt), min of alt")
    ST = {}
    for dv in VARS:
        reset_data(); set_data(build(dv)[0]); rows = []
        for k in range(1, 21):
            s3 = S3(("P2",), seed=259000 + k)["P2"]
            rows.append((s3["cls"], s3["canonical|V2"]["delta"], s3["alt|V2"]["delta"], s3["canonical|V1"]["delta"], s3["alt|V1"]["delta"]))
        reset_data()
        fr = sum(1 for r in rows if r[0] == "H2") / 20.0
        dc = np.array([r[1] for r in rows]); da = np.array([r[2] for r in rows])
        ST[dv] = dict(frac_H2=fr, d_v2_canonical=[float(dc.mean()), float(dc.std(ddof=1))], d_v2_alt=[float(da.mean()), float(da.std(ddof=1)), float(da.min())], classes={c: sum(1 for r in rows if r[0] == c) for c in ("H1", "H2", "H3", "H4")})
        P(f"   {dv}: H2 in {int(round(fr * 20))} of 20; d_V2 canonical {dc.mean():+.2f} +- {dc.std(ddof=1):.2f}; alt {da.mean():+.2f} +- {da.std(ddof=1):.2f} (min {da.min():+.2f}); classes {ST[dv]['classes']}")
    RES["seed_stability"] = ST
    # (5) CFG29's H2 systems
    P("\n  CFG29 H2 SYSTEMS (beyond the 4.5 km/s single-epoch binary ceiling, far from the Milky Way): sigma per variant")
    for nm in ("Eridanus II", "Ursa Major I"):
        P(f"   {nm}: " + ", ".join(f"{dv} {build(dv)[0][nm][0]:.2f}" for dv in VARS))

    # ---------------------------------------------------------------- hand estimates
    P("\n" + "=" * 110 + "\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 3; scored by code)\n" + "=" * 110)
    HE = {}
    dB = {dv: {f: V[dv]["S1"][f]["med"] - V["DV0"]["S1"][f]["med"] for f in FOOTS} for dv in VARS}
    he1 = all(abs(dB[dv][f]) <= 0.02 for dv in VARS[1:] for f in FOOTS) and all(dB["DV1"][f] >= 0 and dB["DV2"][f] <= 0 and dB["DV3"][f] <= 0 for f in FOOTS)
    HE["HE1"] = (he1, "dMedian: " + "; ".join(f"{dv} {dB[dv]['canonical']:+.4f} | {dB[dv]['alt']:+.4f}" for dv in VARS[1:]))
    zmin = min(V[dv]["S1"][f]["z"] for dv in VARS[1:] for f in FOOTS)
    he2 = all(stat_B[dv] == "SURVIVES" for dv in VARS[1:]) and 3.0 <= zmin <= 4.2
    HE["HE2"] = (he2, f"D-B {[stat_B[dv] for dv in VARS[1:]]}; lowest z {zmin:.2f}")
    he3 = True; det3 = []
    for dv in VARS:
        for f in FOOTS:
            m4, m218 = BI[f"{dv}|4.0"]["S1"][f]["med"], BI[f"{dv}|2.18"]["S1"][f]["med"]
            md, mo = BI[f"{dv}|drop"]["S1"][f]["med"], BI[f"{dv}|own"]["S1"][f]["med"]
            b4, b218 = BI[f"{dv}|4.0"]["S3"][f"{f}|P1_b_V2"]["off"], BI[f"{dv}|2.18"]["S3"][f"{f}|P1_b_V2"]["off"]
            ok_ = abs(m4 - m218) <= 1e-9 and abs(md - mo) < 0.01 and abs(b4 - b218) <= 1e-9
            he3 &= ok_; det3.append(f"{dv}/{f[:3]} {m4 - m218:+.1e}, drop {md - mo:+.4f}, (b) {b4 - b218:+.1e}")
    HE["HE3"] = (he3, "; ".join(det3[:6]) + " ...")
    b_off = {dv: V[dv]["S3"]["P2"]["canonical|P1_b_V2"]["off"] for dv in VARS}
    he4 = abs(b_off["DV1"] - 0.0803) <= 0.001 and all(0.063 <= b_off[dv] <= 0.083 for dv in ("DV2", "DV3", "DV4"))
    HE["HE4"] = (he4, "(b) P1 offset (P2, canonical): " + ", ".join(f"{dv} {b_off[dv]:+.4f}" for dv in VARS))
    mx = 0.0
    for dv in VARS[1:]:
        for kern in ("P2", "RAR"):
            for f in FOOTS:
                for v in ("V1", "V2"):
                    mx = max(mx, abs(V[dv]["S3"][kern][f"{f}|{v}"]["delta"] - V["DV0"]["S3"][kern][f"{f}|{v}"]["delta"]))
    he5 = mx < 1.0 and all(V[dv]["S3"]["final"] == "H4" for dv in VARS) and all(stat_G[dv] in ("INTACT", "WEAKER") for dv in VARS[1:])
    HE["HE5"] = (he5, f"largest |d Delta| {mx:.2f}; final classes {[V[dv]['S3']['final'] for dv in VARS]}; D-G {[stat_G[dv] for dv in VARS[1:]]}")
    he6 = ST["DV0"]["frac_H2"] >= 0.9 and 0.05 <= ST["DV0"]["d_v2_alt"][1] <= 0.3
    HE["HE6"] = (he6, f"DV0: H2 in {ST['DV0']['frac_H2']:.2f} of seeds; SD of alt d_V2 {ST['DV0']['d_v2_alt'][1]:.2f}")
    mx9 = max(abs(V[dv]["S2"][f]["rows"]["pred >= 1.5"]["med"] - V["DV0"]["S2"][f]["rows"]["pred >= 1.5"]["med"]) for dv in VARS[1:] for f in FOOTS)
    HE["HE9"] = (mx9 < 0.04, f"largest shift of the pred >= 1.5 median {mx9:.4f}")
    for k, (ok_, det) in HE.items():
        P(f"  {k}: {'PASS' if ok_ else 'MISS'}  {det}")
    P("  HE7 (MUTATE=1) and HE8 (MUTATE=2) are scored in those runs.")
    RES["hand"] = {k: dict(ok=bool(v[0]), detail=v[1]) for k, v in HE.items()}

    # ---------------------------------------------------------------- bottom line
    P("\n" + "=" * 110 + "\nREADING (declared before the run: D-B and D-G of FROZEN_CRITERIA.md section 2)\n" + "=" * 110)
    P(f"  candidate B's UFD failure (CFG28 H1: median > 0.2 dex and z > 3, both footings): " + "; ".join(f"{dv} {stat_B[dv]}" for dv in VARS))
    P(f"  CFG244's lean toward the bound core (Gate H): " + "; ".join(f"{dv} {stat_G[dv]}" for dv in VARS[1:]) + f"  (DV0: P2 {s3_0['P2']['cls']}, RAR {s3_0['RAR']['cls']}, final {s3_0['final']})")
    nf = sum(1 for c in CK if not c["ok"])
    P(f"\n  {len(CK) - nf}/{len(CK)} controls pass" + ("" if not nf else " -> CONTROL FAILURES") + f"  ({time.time() - T0:.0f} s)")
    finish()
    sys.exit(1 if nf else 0)

# ================================================================================================ MUTATE 1: a -0.33 dex plant on every ultra-faint, on top of each variant
if MUT == "1":
    P("\n" + "=" * 110 + "\nMUTATE=1: a -0.33 dex correction planted on EVERY ultra-faint dispersion and limit (on top of each variant): B's offset must vanish and the Gate H lean must flip\n" + "=" * 110)
    out = {}; bites = True
    P(f"  {'variant':6s} {'foot':9s} {'median':>8s} {'z':>6s} {'(unplanted)':>12s} {'shift-0.33':>10s} | {'P2 d_V1':>8s} {'P2 d_V2':>8s} {'RAR d_V2':>8s}  class P2/RAR/FINAL  (b) V2 P1")
    for dv in VARS:
        un = run_variant(dv)
        reset_data(); set_data(build(dv, plant_all=-0.33)[0]); s1 = S1(); s3 = S3(); reset_data()
        out[dv] = dict(S1=s1, S3=s3, unplanted=dict(S1=un["S1"]))
        for f in FOOTS:
            ex = s1[f]["med"] - un["S1"][f]["med"] + 0.33
            P(f"  {dv:6s} {f:9s} {s1[f]['med']:+8.4f} {s1[f]['z']:+6.2f} {un['S1'][f]['med']:+12.4f} {ex:+10.1e} | {s3['P2'][f'{f}|V1']['delta']:+8.2f} {s3['P2'][f'{f}|V2']['delta']:+8.2f} {s3['RAR'][f'{f}|V2']['delta']:+8.2f}  {s3['P2']['cls']}/{s3['RAR']['cls']}/{s3['final']}  {s3['P2'][f'{f}|P1_b_V2']['off']:+.3f}")
            bites &= abs(s1[f]["med"]) < 0.05 and abs(s1[f]["z"]) < 1.5 and s3["P2"][f"{f}|V2"]["delta"] < 0 and s3["P2"]["cls"] != "H2" and abs(ex) < 1e-9
    RES["mutate1"] = out
    he7 = all(abs(out["DV0"]["S1"]["canonical"]["med"] - (-0.005)) < 0.01 and abs(out["DV0"]["S1"]["alt"]["med"] - (-0.026)) < 0.01 and abs(out["DV0"]["S1"][f]["z"]) < 0.5 and
              abs(out["DV0"]["S3"]["P2"][f"{f}|V2"]["delta"] + 22) < 3 and abs(out["DV0"]["S3"]["P2"][f"{f}|V1"]["delta"] + 5) < 2 and out["DV0"]["S3"]["P2"]["cls"] == "H4" for f in FOOTS)
    P(f"\n  HE7: {'PASS' if he7 else 'MISS'}  DV0: B {out['DV0']['S1']['canonical']['med']:+.4f} | {out['DV0']['S1']['alt']['med']:+.4f}; P2 d_V2 {out['DV0']['S3']['P2']['canonical|V2']['delta']:+.2f} | {out['DV0']['S3']['P2']['alt|V2']['delta']:+.2f}; d_V1 {out['DV0']['S3']['P2']['canonical|V1']['delta']:+.2f} | {out['DV0']['S3']['P2']['alt|V1']['delta']:+.2f}; class {out['DV0']['S3']['P2']['cls']}")
    RES["hand"] = {"HE7": dict(ok=bool(he7))}
    nf = sum(1 for c in CK if not c["ok"])
    P(f"\n  [MUTATE CONTROL] MUTATE=1: the planted -0.33 dex {'BITES: B vanishes (|median| < 0.05, z < 1.5) and the P2 lean flips sign (d_V2 < 0, class not H2) in every variant' if bites else 'DOES NOT BITE'}; controls {len(CK) - nf}/{len(CK)} pass")
    RES["bites"] = bool(bites)
    finish()
    sys.exit(1 if bites else 0)

# ================================================================================================ MUTATE 2: plants on the eight only, at DV0
if MUT == "2":
    P("\n" + "=" * 110 + "\nMUTATE=2: a planted c on the eight Arroyo systems ONLY (DV0): the KM median must fall monotonically with |c|, strictly at c = -0.5; each of the eight shifts by c, the other 32 by 0\n" + "=" * 110)
    out = {}; prev = {f: s1_0[f]["med"] for f in FOOTS}; mono = True; exact = True
    for c in (-0.10, -0.20, -0.33, -0.50):
        val, ch = build("DV0", plant_eight=c)
        dev = max(abs(ch[n] - (c if n in EIGHT_NAMES else 0.0)) for n in ch)
        exact &= dev < 1e-12
        reset_data(); set_data(val); s1 = S1(); reset_data()
        out[str(c)] = s1
        for f in FOOTS:
            mono &= s1[f]["med"] <= prev[f] + 1e-12; prev[f] = s1[f]["med"]
        P(f"  c {c:+.2f}: B {s1['canonical']['med']:+.4f} | {s1['alt']['med']:+.4f}   shift {s1['canonical']['med'] - s1_0['canonical']['med']:+.4f} | {s1['alt']['med'] - s1_0['alt']['med']:+.4f}   (per-system change error {dev:.1e})")
    drop5 = {f: s1_0[f]["med"] - out["-0.5"][f]["med"] for f in FOOTS}
    bites = mono and exact and all(drop5[f] >= 0.005 for f in FOOTS)
    he8 = all(0.005 <= s1_0[f]["med"] - out["-0.33"][f]["med"] <= 0.015 and 0.005 <= drop5[f] <= 0.02 for f in FOOTS)
    P(f"\n  HE8: {'PASS' if he8 else 'MISS'}  shifts at c = -0.33: " + " | ".join(f"{s1_0[f]['med'] - out['-0.33'][f]['med']:.4f}" for f in FOOTS) + "; at c = -0.5: " + " | ".join(f"{drop5[f]:.4f}" for f in FOOTS))
    RES["mutate2"] = out; RES["hand"] = {"HE8": dict(ok=bool(he8))}; RES["bites"] = bool(bites)
    nf = sum(1 for c_ in CK if not c_["ok"])
    P(f"\n  [MUTATE CONTROL] MUTATE=2: monotone {mono}, exact per-system shifts {exact}, drop at c = -0.5 {drop5['canonical']:.4f} | {drop5['alt']:.4f} (>= 0.005): the control {'BITES' if bites else 'DOES NOT BITE'}; controls {len(CK) - nf}/{len(CK)} pass")
    finish()
    sys.exit(1 if bites else 0)

# ================================================================================================ MUTATE 3: the wrong denominator
if MUT == "3":
    bites = not ok2
    nbad = 0
    for dv, col in (("DV2", "sig_free"), ("DV3", "sig_f07")):
        ch = build(dv, wrong_denom=True)[1]
        nbad_dv = sum(1 for n in EIGHT_NAMES if abs(ch[n] - indep_log_ratio(col, n)) > 1e-6)
        P(f"  {dv} with the wrong denominator sig_lit: {nbad_dv} of 8 per-system log changes differ from the independent recomputation by more than 1e-6 (needs >= 5)")
        nbad = max(nbad, nbad_dv) if dv == "DV2" else min(nbad, nbad_dv)
    bites = bites and nbad >= 5
    RES["bites"] = bool(bites)
    nf = sum(1 for c_ in CK if not c_["ok"])
    P(f"\n  [MUTATE CONTROL] MUTATE=3: C2 {'FAILS on the mutated build (the control BITES)' if bites else 'does not fail (the control DOES NOT BITE)'}; other controls {len(CK) - nf}/{len(CK)} pass")
    finish()
    sys.exit(1 if bites else 0)
