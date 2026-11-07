#!/usr/bin/env python3
"""MS1: the moving-Sun door, three-rung Richardson / GCI convergence on AC24's ladder.
Criteria: CRITERIA.md (af5d153290, pushed before this script existed).

AC15's physical inputs, cells, field() and grade_snap() are exec'd verbatim from
action_search_2026_11_05/AC15_moving_sun_nonlinear/grade.py, with AC24's one patched line (the plant).
AC24's plant builder (make_plant) is exec'd verbatim from AC24's ac24_grade.py. Parts are read only.

  nice -n 15 python3 -B closure_2026_11_06/MS1_moving_sun_convergence/ms1_grade.py
kappa = 1/2 FITTED; footings never pooled; not theory closed.
"""
import os, sys, json, glob, math, signal, resource
sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.special import eval_legendre

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "action_search_2026_11_05")
AC15 = os.path.join(ROOT, "AC15_moving_sun_nonlinear")
AC24 = os.path.join(ROOT, "AC24_moving_sun_powered")
CACHE = os.path.join(HERE, "rows_cache.json")
OUT, RES = [], {"lane": "MS1_moving_sun_convergence", "criteria": "af5d153290", "checks": {}}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, ok, detail):
    RES["checks"][name] = dict(ok=bool(ok), detail=str(detail)); P(f"{name} {'PASS' if ok else 'FAIL'} {detail}")


# ------------------------------------------------------------------ AC15 block + AC24 patch, verbatim
src = open(os.path.join(AC15, "grade.py")).read().split("\n")
i0 = next(i for i, l in enumerate(src) if l.startswith("# ------------------------------------------------------------------ physical inputs"))
i1 = next(i for i, l in enumerate(src) if l.startswith("# field-code test"))
block = "\n".join(src[i0:i1])
OLD = "    dq = qq - 1.0\n"
assert block.count(OLD) == 1
block = block.replace(OLD, "    dq = qq - 1.0 + (PLANT(rc, tc, Mcell) if PLANT is not None else 0.0)\n")
NS = {"np": np, "math": math, "glob": glob, "os": os, "json": json, "P": lambda s="": None,
      "PARTS": os.path.join(AC15, "parts"), "PLANT": None, "eval_legendre": eval_legendre}
exec(compile(block, "AC15_grade_block", "exec"), NS)
CELLS, GKEYS, grade_snap = NS["CELLS"], NS["GKEYS"], NS["grade_snap"]
NS["CELL_BY_M"] = {round(c["M"], 9): c for c in CELLS}
NS["RUN_M"] = [None]
s24 = open(os.path.join(AC24, "ac24_grade.py")).read()
j0 = s24.index("SH = (0.5, 0.9)"); j1 = s24.index("RUN_M = [None]")
exec(compile(s24[j0:j1], "AC24_plant_block", "exec"), NS)
make_plant = NS["make_plant"]
PLANT_FOR = {**{f"G1_{p}": ("MONO", p) for p in NS["PLAN"]}, **{f"G2_{p}": ("QUAD", p) for p in NS["PLAN"]},
             "G3": ("QUAD3", "Saturn")}

# ------------------------------------------------------------------ resumable row cache
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}


def save_cache(*_):
    json.dump(cache, open(CACHE + ".tmp", "w")); os.replace(CACHE + ".tmp", CACHE)
    if _:
        P("SIGTERM: cache saved, exiting"); sys.exit(1)


signal.signal(signal.SIGTERM, save_cache)


def snap_files(tag):
    for base in (os.path.join(AC24, "parts"), os.path.join(AC15, "parts")):
        fs = sorted(glob.glob(os.path.join(base, tag, "snap_*.npz")))
        if fs:
            return fs
    return None


def rows(fpath, uq, plant=None):
    """per-cell gate rows of one snapshot; plant = (gate, k) or None."""
    key = f"{os.path.relpath(fpath, ROOT)}|{int(uq)}|{plant}"
    if key not in cache:
        s = dict(np.load(fpath))
        if plant is not None:
            NS["RUN_M"][0] = float(s["M"])
            kind, pl = PLANT_FOR[plant[0]]
            NS["PLANT"] = make_plant(kind, pl, plant[1], s["re"])
        r = grade_snap(s, uq)
        NS["PLANT"] = None
        cache[key] = [{k: x[k] for k in GKEYS} for x in r]
        if len(cache) % 10 == 0:
            save_cache()
    return cache[key]


# ------------------------------------------------------------------ Richardson / GCI (frozen rules)
def rich(xc, xm, xf):
    e1, e2 = xc - xm, xm - xf
    out = dict(xc=xc, xm=xm, xf=xf)
    if abs(e2) <= 0.01 * abs(xf):
        return {**out, "cls": "TINY", "p": None, "L": xf - 3 * abs(e2), "U": xf + 3 * abs(e2), "XR": xf}
    if e1 == 0:
        R = None
    else:
        R = e2 / e1
    if R is not None and 0 < R < 1:
        p = math.log2(1 / R); pu = min(p, 2.0); d = 2 ** pu - 1
        XR = xf - e2 / d; E = 1.25 * abs(e2) / d
        return {**out, "cls": "MONOTONE" if p >= 0.5 else "PRE-ASYMPTOTIC", "p": p, "XR": XR,
                "L": max(0.0, min(xf, XR) - E), "U": max(xf, XR) + E}
    if R is None or R <= 0:
        D = max(xc, xm, xf) - min(xc, xm, xf)
        return {**out, "cls": "OSCILLATORY", "p": None, "XR": None, "L": max(0.0, min(xc, xm, xf) - D),
                "U": max(xc, xm, xf) + D}
    return {**out, "cls": "DIVERGENT", "p": None, "XR": None, "L": min(xc, xm, xf), "U": math.inf}


# KA2: known sequences
ka2 = True; det = []
for p in (0.6, 1.0, 2.0):
    x = [0.3 + 0.2 * h ** p for h in (1, 0.5, 0.25)]
    r = rich(*x)
    ok = abs(r["p"] - p) <= 1e-10 and abs(r["XR"] - 0.3) <= 1e-10 and r["L"] <= 0.3 <= r["U"]
    ka2 &= ok; det.append(f"p {p}: got {r['p']:.12f}, XR {r['XR']:.12f}, [{r['L']:.4f}, {r['U']:.4f}]")
ka2 &= rich(1, 0.5, 0.8)["cls"] == "OSCILLATORY" and rich(1, 1.2, 1.5)["cls"] == "DIVERGENT"
check("KA2", ka2, "; ".join(det) + "; (1,0.5,0.8) OSC, (1,1.2,1.5) DIV")

# KA3: AC24 gravity-off errors
g24 = json.load(open(os.path.join(AC24, "GRADE.json")))
e3 = g24["KA3"]["err"]
r3 = rich(e3["coarse"], e3["medium"], e3["fine"])
check("KA3", r3["cls"] == "MONOTONE" and r3["L"] <= 0 <= r3["U"],
      f"errors {e3['coarse']:.3e} {e3['medium']:.3e} {e3['fine']:.3e}: {r3['cls']} p {r3['p']:.3f}, bracket [{r3['L']:.2e}, {r3['U']:.2e}]")

# ------------------------------------------------------------------ ladder series
RUNGS = ("coarse", "medium", "fine")
READ = (("q", False), ("qB", True))
lad = {}            # (M, reading) -> rung -> per-cell rows
for M in (234, 490):
    for k_, uq in READ:
        lad[(M, k_)] = {r: rows(snap_files(f"M{M}_transmit_uniform_{r}_t1000")[-1], uq) for r in RUNGS}
save_cache()

# KA1: reproduce AC24
worst_rel = 0.0; n = 0
for M in (234, 490):
    for k_, _ in READ:
        for r in RUNGS:
            ref = g24["convergence"][str(M)]["rungs"][r][k_]
            for g in GKEYS:
                mine = max(c[g] for c in lad[(M, k_)][r])
                worst_rel = max(worst_rel, abs(mine / ref[g] - 1) if ref[g] else abs(mine)); n += 1
mf = {M: max(abs(max(c[g] for c in lad[(M, k_)]["fine"]) / max(c[g] for c in lad[(M, k_)]["medium"]) - 1)
             for k_, _ in READ for g in GKEYS) for M in (234, 490)}

BRACKETS = ["M234_transmit_uniform_medium", "M490_transmit_uniform_medium", "M234_absorb_uniform_medium",
            "M490_absorb_uniform_medium", "M234_reflect_uniform_medium", "M490_reflect_uniform_medium",
            "M234_transmit_hedgehog_medium"]
med = {}            # (b, reading) -> per-cell graded values
for b in BRACKETS:
    fs = snap_files(b)
    for k_, uq in READ:
        hist = [rows(f, uq) for f in fs]
        fin = hist[-1]
        wfin = {g: max(c[g] for c in fin) for g in GKEYS}
        chg = max(abs(max(c[g] for c in h) / wfin[g] - 1) if wfin[g] > 0 else 0.0 for h in hist for g in GKEYS)
        steady = chg <= 0.05
        envw = {g: max(max(c[g] for c in h) for h in hist) for g in GKEYS}
        ref = g24["brackets"][b][k_]["graded"]
        for g in GKEYS:
            mine = wfin[g] if steady else envw[g]
            worst_rel = max(worst_rel, abs(mine / ref[g] - 1) if ref[g] else abs(mine)); n += 1
        if steady:
            per = [dict(c) for c in fin]
        else:
            per = [{g: max(h[i][g] for h in hist) * (1 + chg) for g in GKEYS} for i in range(len(CELLS))]
        med[(b, k_)] = dict(cells=per, steady=steady, chg=chg)
save_cache()
mf_ok = abs(mf[234] - 0.496) < 5e-4 and abs(mf[490] - 0.572) < 5e-4
check("KA1", worst_rel <= 1e-12 and mf_ok, f"{n} AC24 numbers reproduced, max rel {worst_rel:.1e} (1e-12); "
      f"medium->fine max {mf[234]:.4f} / {mf[490]:.4f} (AC24 0.496 / 0.572)")

# ------------------------------------------------------------------ Richardson on every series
ser = {}
for (M, k_), d in lad.items():
    for i, c in enumerate(CELLS):
        for g in GKEYS:
            ser[(M, k_, i, g)] = rich(d["coarse"][i][g], d["medium"][i][g], d["fine"][i][g])
cls_count = {}
for v in ser.values():
    cls_count[v["cls"]] = cls_count.get(v["cls"], 0) + 1
conv_ok = all(v["cls"] in ("TINY", "MONOTONE", "OSCILLATORY") for v in ser.values())
bad = [(M, k_, CELLS[i]["foot"], CELLS[i]["Lstar"], CELLS[i]["V"], g, v["cls"], v["p"])
       for (M, k_, i, g), v in ser.items() if v["cls"] not in ("TINY", "MONOTONE", "OSCILLATORY")]
ps = {k_: [v["p"] for (M, kk, i, g), v in ser.items() if kk == k_ and v["p"] is not None] for k_, _ in READ}
check("CONV", conv_ok, f"series classes {cls_count}; observed p range q {min(ps['q']) if ps['q'] else None}"
      f"-{max(ps['q']) if ps['q'] else None}, qB {min(ps['qB']) if ps['qB'] else None}-{max(ps['qB']) if ps['qB'] else None}; "
      f"failing series {len(bad)}")
RES["conv_failing_series"] = bad[:60]
mono_dec = {k_: sum(1 for (M, kk, i, g), v in ser.items() if kk == k_ and v["xc"] > v["xm"] > v["xf"]) for k_, _ in READ}
ntot = {k_: sum(1 for (M, kk, i, g) in ser if kk == k_) for k_, _ in READ}
fin_U = max(v["U"] for v in ser.values() if math.isfinite(v["U"]))
rung_max = max(max(v["xc"], v["xm"], v["xf"]) for v in ser.values())
bad_by = {}
for x in bad:
    bad_by[(x[0], x[1], x[6])] = bad_by.get((x[0], x[1], x[6]), 0) + 1
RES["reported"] = dict(monotone_decreasing=mono_dec, n_series=ntot, max_finite_U=fin_U, max_rung_value=rung_max,
                       failing_by_M_reading_class={str(k): v for k, v in bad_by.items()})
P(f"reported: series falling coarse > medium > fine: q {mono_dec['q']}/{ntot['q']}, qB {mono_dec['qB']}/{ntot['qB']}; "
  f"largest rung value anywhere {rung_max:.3e}; largest finite U {fin_U:.3e}; failing by (M, reading, class) {bad_by}")
RES["series_classes"] = cls_count

# per (M, reading, gate): ladder summary over cells
P("ladder brackets (worst over cells, ratio to line) [L, U], fine, class/p of the worst-U cell:")
RES["ladder"] = {}
for (M, k_) in lad:
    for g in GKEYS:
        vs = [ser[(M, k_, i, g)] for i in range(len(CELLS))]
        w = max(vs, key=lambda v: v["U"])
        RES["ladder"][f"M{M}_{k_}_{g}"] = dict(L=max(v["L"] for v in vs), U=w["U"], xc=w["xc"], xm=w["xm"], xf=w["xf"],
                                              cls=w["cls"], p=w["p"], XR=w["XR"])
        P(f"  M{M} {k_:2s} {g:9s} rungs {w['xc']:.3e} {w['xm']:.3e} {w['xf']:.3e}  {w['cls']:14s} p "
          f"{'-' if w['p'] is None else round(w['p'], 2)}  U {w['U']:.3e}")

# ------------------------------------------------------------------ brackets: ladder direct + transfer
brk = {}            # bracket -> reading -> cell -> gate -> (L, U)
for M in (234, 490):
    for k_, _ in READ:
        brk.setdefault(f"M{M}_transmit_uniform_t1000", {})[k_] = [
            {g: (ser[(M, k_, i, g)]["L"], ser[(M, k_, i, g)]["U"]) for g in GKEYS} for i in range(len(CELLS))]
for b in BRACKETS:
    M = int(b[1:4])
    for k_, _ in READ:
        out = []
        for i in range(len(CELLS)):
            gv = med[(b, k_)]["cells"][i]; d = {}
            for g in GKEYS:
                s_ = ser[(M, k_, i, g)]; G_ = gv[g]
                d[g] = (G_ * s_["L"] / s_["xm"], G_ * s_["U"] / s_["xm"]) if s_["xm"] > 0 else (0.0, G_ + s_["U"])
            out.append(d)
        brk.setdefault(b, {})[k_] = out

Umax = {g: max(brk[b][k_][i][g][1] for b in brk for k_, _ in READ for i in range(len(CELLS))) for g in GKEYS}
Lmin = {g: min(brk[b][k_][i][g][0] for b in brk for k_, _ in READ for i in range(len(CELLS))) for g in GKEYS}
arg = {}
for g in GKEYS:
    arg[g] = max(((b, k_, i) for b in brk for k_, _ in READ for i in range(len(CELLS))), key=lambda t: brk[t[0]][t[1]][t[2]][g][1])
P("bracket over cells, brackets and readings, per gate [min L, max U] (ratio to line), worst-U location:")
for g in GKEYS:
    b, k_, i = arg[g]
    P(f"  {g:9s} [{Lmin[g]:.3e}, {Umax[g]:.3e}]  at {b} {k_} {CELLS[i]['foot']} Lstar {CELLS[i]['Lstar']} V {CELLS[i]['V'] / 1e3:.0f}")
RES["bracket_per_gate"] = {g: dict(Lmin=Lmin[g], Umax=Umax[g], at=[arg[g][0], arg[g][1], CELLS[arg[g][2]]["foot"],
                                                                  CELLS[arg[g][2]]["Lstar"], CELLS[arg[g][2]]["V"]]) for g in GKEYS}

# ------------------------------------------------------------------ MUTATE through the extrapolation
mut2 = mut01 = True; near = []; mrec = {}; m01fail = []
for M in (234, 490):
    for k_, uq in READ:
        for g in GKEYS:
            for k in (2.0, 0.1):
                pr = {r: rows(snap_files(f"M{M}_transmit_uniform_{r}_t1000")[-1], uq, (g, k)) for r in RUNGS}
                for i, c in enumerate(CELLS):
                    s_ = rich(pr["coarse"][i][g], pr["medium"][i][g], pr["fine"][i][g])
                    base_U = ser[(M, k_, i, g)]["U"]
                    if k == 2.0:
                        mut2 &= s_["L"] > 1
                        mrec[f"M{M}_{k_}_{g}_k2_minL"] = min(mrec.get(f"M{M}_{k_}_{g}_k2_minL", math.inf), s_["L"])
                    else:
                        if base_U + 0.1 < 1:
                            mut01 &= s_["U"] < 1
                            if not s_["U"] < 1:
                                m01fail.append((M, k_, g, c["foot"], c["Lstar"], c["V"], ser[(M, k_, i, g)]["cls"], s_["cls"],
                                                s_["xc"], s_["xm"], s_["xf"]))
                        else:
                            near.append((M, k_, g, c["foot"], c["Lstar"], c["V"], base_U))
                        mrec[f"M{M}_{k_}_{g}_k0.1_maxU"] = max(mrec.get(f"M{M}_{k_}_{g}_k0.1_maxU", -math.inf), s_["U"])
    save_cache()
RES["mutate"] = dict(records=mrec, near_failures=near, k01_failures=m01fail)
P(f"reported: k = 0.1 failures {len(m01fail)}; classes (base -> planted): "
  f"{sorted(set((x[6], x[7]) for x in m01fail))}; first: {m01fail[:3]}")
check("MUTATE_k2", mut2, f"planted 2x reads FAIL (L > 1) in every cell, gate, M, reading: min L "
      f"{min(v for k, v in mrec.items() if 'k2' in k):.3f}")
check("MUTATE_k0.1", mut01, f"planted 0.1x reads PASS (U < 1) where base U + 0.1 < 1: max U "
      f"{max(v for k, v in mrec.items() if 'k0.1' in k):.3f}; near-failures {len(near)}")

# ------------------------------------------------------------------ label
need = ("KA1", "KA2", "KA3", "CONV", "MUTATE_k2", "MUTATE_k0.1")
fails = []
for i, c in enumerate(CELLS):
    for g in GKEYS:
        if all(max(brk[b][k_][i][g][0] for k_, _ in READ) > 1 for b in brk):      # worse reading governs
            fails.append((c["foot"], c["Lstar"], c["V"], g))
allU = max(Umax.values())
if not all(RES["checks"][k]["ok"] for k in need):
    label = "NO VERDICT"
elif allU < 1:
    label = "PASS (moving Sun, scoped)"
elif fails:
    label = "FAIL"
else:
    label = "UNDECIDED"
RES["fail_cells"] = fails; RES["label"] = label; RES["max_U_all"] = allU
RES["rss_MB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024 if sys.platform == "darwin" else 1024)
P(f"max upper bound over everything: {allU:.3e} of the line; RSS {RES['rss_MB']:.0f} MB")
P(f"LABEL: {label}  (v3s; AC2q differs by s^2/rho0 ~ 4e-6 in the charge)  kappa = 1/2 FITTED; not theory closed")
json.dump(RES, open(os.path.join(HERE, "MS1.json"), "w"), indent=1, default=lambda o: None if o is None else float(o))
open(os.path.join(HERE, "ms1.out"), "w").write("\n".join(OUT) + "\n")
save_cache()
