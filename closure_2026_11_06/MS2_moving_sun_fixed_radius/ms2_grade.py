#!/usr/bin/env python3
"""MS2: the moving-Sun door with a fixed-physical-radius readout (R1), time-mean rungs (R2), and the M234
ultra rung (R3) when it exists. Criteria: CRITERIA.md (local dfd90815b6, origin 92b0894440), pushed before
this script existed.

AC15's field()/grade_snap() are exec'd verbatim (AC24's plant line added); R1's field_fixed() is the same
source with the two readout lines replaced (text substitution, asserted). AC24's make_plant() is exec'd
verbatim. MS1's rich() is exec'd verbatim for KA1. Parts are read only.

  nice -n 15 python3 -B closure_2026_11_06/MS2_moving_sun_fixed_radius/ms2_grade.py
kappa = 1/2 FITTED; footings never pooled; not theory closed.
"""
import os, sys, json, glob, math, signal, resource
sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.special import eval_legendre

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, "..", "..")
ROOT = os.path.join(REPO, "action_search_2026_11_05")
AC15, AC24 = os.path.join(ROOT, "AC15_moving_sun_nonlinear"), os.path.join(ROOT, "AC24_moving_sun_powered")
MS1 = os.path.join(HERE, "..", "MS1_moving_sun_convergence")
CACHE = os.path.join(HERE, "rows_cache.json")
OUT, RES = [], {"lane": "MS2_moving_sun_fixed_radius", "criteria": ["dfd90815b6", "92b0894440"], "checks": {}}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, ok, detail):
    RES["checks"][name] = dict(ok=bool(ok), detail=str(detail)); P(f"{name} {'PASS' if ok else 'FAIL'} {detail}")


# ------------------------------------------------------------------ AC15 block (+ AC24 plant line), and R1 variant
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
field_edge = NS["field"]

fsrc = block[block.index("def field("):block.index("def grade_snap(")]
R_OLD1 = ("        rp = float(re[np.argmin(np.abs(re - rp0))])                        # evaluate on the nearest radial edge (exact shell split)\n"
          "        inner = rc < rp\n")
R_NEW1 = ("        rp = float(rp0)                                                    # R1: exact physical radius\n"
          "        j = int(np.searchsorted(re, rp, side='right') - 1)\n"
          "        lo_, hi_ = re[j], re[j + 1]\n"
          "        f_in = (rp ** 3 - lo_ ** 3) / (hi_ ** 3 - lo_ ** 3)\n"
          "        r_a = 0.75 * (rp ** 4 - lo_ ** 4) / (rp ** 3 - lo_ ** 3) if f_in > 0 else rp\n"
          "        r_b = 0.75 * (hi_ ** 4 - rp ** 4) / (hi_ ** 3 - rp ** 3) if f_in < 1 else rp\n"
          "        inner = np.arange(len(rc)) < j; outer = np.arange(len(rc)) > j\n")
R_OLD2 = ("            Ilt = np.sum(mom[l][inner] * rc[inner] ** l)\n"
          "            Igt = np.sum(mom[l][~inner] * rc[~inner] ** (-l - 1.0))\n")
R_NEW2 = ("            Ilt = np.sum(mom[l][inner] * rc[inner] ** l) + f_in * mom[l][j] * r_a ** l\n"
          "            Igt = np.sum(mom[l][outer] * rc[outer] ** (-l - 1.0)) + (1 - f_in) * mom[l][j] * r_b ** (-l - 1.0)\n")
assert fsrc.count(R_OLD1) == 1 and fsrc.count(R_OLD2) == 1
exec(compile(fsrc.replace("def field(", "def field_fixed(").replace(R_OLD1, R_NEW1).replace(R_OLD2, R_NEW2),
             "R1_field_fixed", "exec"), NS)
field_fixed = NS["field_fixed"]
CELLS, GKEYS, grade_snap, PLAN, G, AU, Q2 = NS["CELLS"], NS["GKEYS"], NS["grade_snap"], NS["PLAN"], NS["G"], NS["AU"], NS["Q2_LINE"]
NS["CELL_BY_M"] = {round(c["M"], 9): c for c in CELLS}
NS["RUN_M"] = [None]
s24 = open(os.path.join(AC24, "ac24_grade.py")).read()
exec(compile(s24[s24.index("SH = (0.5, 0.9)"):s24.index("RUN_M = [None]")], "AC24_plant_block", "exec"), NS)
make_plant = NS["make_plant"]
PLANT_FOR = {**{f"G1_{p}": ("MONO", p) for p in PLAN}, **{f"G2_{p}": ("QUAD", p) for p in PLAN}, "G3": ("QUAD3", "Saturn")}
s1 = open(os.path.join(MS1, "ms1_grade.py")).read()
NS1 = {"math": math}
exec(compile(s1[s1.index("def rich("):s1.index("# KA2: known sequences")], "MS1_rich", "exec"), NS1)
rich_ms1 = NS1["rich"]

# ------------------------------------------------------------------ resumable cache
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}


def save_cache(*_):
    json.dump(cache, open(CACHE + ".tmp", "w")); os.replace(CACHE + ".tmp", CACHE)
    if _:
        P("SIGTERM: cache saved"); sys.exit(1)


signal.signal(signal.SIGTERM, save_cache)


def snap_files(tag):
    for base in (os.path.join(HERE, "parts"), os.path.join(AC24, "parts"), os.path.join(AC15, "parts")):
        fs = sorted(glob.glob(os.path.join(base, tag, "snap_*.npz")))
        if fs and (len(fs) == 5 or "NOGRAV" in tag):
            return fs
    return None


def rows(fpath, uq, readout, plant=None):
    key = f"{os.path.relpath(fpath, REPO)}|{int(uq)}|{readout}|{plant}"
    if key not in cache:
        s = dict(np.load(fpath))
        NS["field"] = field_fixed if readout == "fixed" else field_edge
        if plant is not None:
            NS["RUN_M"][0] = float(s["M"])
            kind, pl = PLANT_FOR[plant[0]]
            NS["PLANT"] = make_plant(kind, pl, plant[1], s["re"])
        r = grade_snap(s, uq)
        NS["PLANT"] = None; NS["field"] = field_edge
        cache[key] = [{k: x[k] for k in GKEYS} for x in r]
        if len(cache) % 20 == 0:
            save_cache()
    return cache[key]


def planted_only(fpath, gate, k):
    """AC24 P1 construction under R1: gate value of field(with plant) - field(without)."""
    s = dict(np.load(fpath)); NS["RUN_M"][0] = float(s["M"]); kind, pl = PLANT_FOR[gate]; out = []
    for c in CELLS:
        rp_ = {p_: d * AU / c["RA"] for p_, (d, _) in PLAN.items()}
        NS["PLANT"] = None
        f0, _ = field_fixed(s, c["M"], list(rp_.values()), False)
        NS["PLANT"] = make_plant(kind, pl, k, s["re"])
        f1, _ = field_fixed(s, c["M"], list(rp_.values()), False)
        NS["PLANT"] = None
        conv = G * c["rho"] * c["RA"]; rp = rp_[pl]
        ar, at = f1[rp][0] - f0[rp][0], f1[rp][1] - f0[rp][1]
        ar2, at2 = f1[rp][2] - f0[rp][2], f1[rp][3] - f0[rp][3]
        mag = np.hypot(ar, at) * conv
        out.append(float(dict(MONO=mag.max() / PLAN[pl][1], QUAD=(mag.max() - mag.min()) / PLAN[pl][1],
                              QUAD3=np.hypot(ar2, at2).max() * conv / (rp * c["RA"]) / Q2)[kind]))
    return out


# ------------------------------------------------------------------ R4 classification (frozen)
def classify(X, S_):
    """X = rung means (coarsest first), S_ = rung time spreads."""
    x1, x2, x3 = X; s1_, s2_, s3_ = S_; S = max(S_)
    e1, e2 = x1 - x2, x2 - x3; D = max(X) - min(X)
    base = dict(X=list(X), s=list(S_))
    if max(abs(e1), abs(e2)) <= 1e-3:
        return {**base, "cls": "TINY_ABS", "p": None, "L": max(0.0, min(X) - 3 * D - S), "U": max(X) + 3 * D + S}
    if abs(e2) <= 0.01 * abs(x3):
        return {**base, "cls": "TINY", "p": None, "L": max(0.0, x3 - 3 * abs(e2) - S), "U": x3 + 3 * abs(e2) + S}
    if abs(e1) <= s1_ + s2_ and abs(e2) <= s2_ + s3_:
        return {**base, "cls": "NOISE", "p": None, "L": max(0.0, min(X) - D - S), "U": max(X) + D + S}
    R = None if e1 == 0 else e2 / e1
    if R is not None and 0 < R < 1:
        p = math.log2(1 / R); pu = min(p, 2.0); d = 2 ** pu - 1
        XR = x3 - e2 / d; E = 1.25 * abs(e2) / d
        return {**base, "cls": "MONOTONE" if p >= 0.5 else "PRE-ASYMPTOTIC", "p": p, "XR": XR,
                "L": max(0.0, min(x3, XR) - E - S), "U": max(x3, XR) + E + S}
    if R is None or R <= 0:
        return {**base, "cls": "OSCILLATORY", "p": None, "L": max(0.0, min(X) - D - S), "U": max(X) + D + S}
    return {**base, "cls": "DIVERGENT", "p": None, "L": max(0.0, min(X) - S), "U": math.inf}


OKCLS = ("TINY_ABS", "TINY", "NOISE", "MONOTONE", "OSCILLATORY")

# ------------------------------------------------------------------ KA3 (procedure)
ka = True; det = []
for p in (0.6, 1.0, 2.0):
    x = [0.3 + 0.2 * h ** p for h in (1, 0.5, 0.25)]
    r = classify(x, (0, 0, 0))
    ok = r["cls"] == "MONOTONE" and abs(r["p"] - p) <= 1e-10 and abs(r["XR"] - 0.3) <= 1e-10 and r["L"] <= 0.3 <= r["U"]
    ka &= ok; det.append(f"p {p}: {r['cls']} {r['p']:.10f} XR {r['XR']:.10f}")
ka &= classify((1, 0.5, 0.8), (0, 0, 0))["cls"] == "OSCILLATORY" and classify((1, 1.2, 1.5), (0, 0, 0))["cls"] == "DIVERGENT"
g24 = json.load(open(os.path.join(AC24, "GRADE.json"))); e3 = g24["KA3"]["err"]
r3 = classify((e3["coarse"], e3["medium"], e3["fine"]), (0, 0, 0))
ka &= r3["L"] <= 0 <= r3["U"] and r3["cls"] in ("MONOTONE", "TINY_ABS")
check("KA3", ka, "; ".join(det) + f"; OSC/DIV classified; AC24 gravity-off errors {r3['cls']} bracket [{r3['L']:.2e}, {r3['U']:.2e}]"
      + (" (the 1e-3 TINY_ABS floor catches these 1e-2-level errors first)" if r3["cls"] == "TINY_ABS" else ""))

# ------------------------------------------------------------------ KA1: MS1 exactly (edge readout, final snapshot)
ms1 = json.load(open(os.path.join(MS1, "MS1.json")))
RUNGS3 = ("coarse", "medium", "fine")
READ = (("q", False), ("qB", True))
worst_rel = 0.0; n = 0; mf = {}
for M in (234, 490):
    for k_, uq in READ:
        rr = {r: rows(snap_files(f"M{M}_transmit_uniform_{r}_t1000")[-1], uq, "edge") for r in RUNGS3}
        for g in GKEYS:
            ser = [rich_ms1(rr["coarse"][i][g], rr["medium"][i][g], rr["fine"][i][g]) for i in range(len(CELLS))]
            w = max(ser, key=lambda v: v["U"]); ref = ms1["ladder"][f"M{M}_{k_}_{g}"]
            for a_, b_ in ((w["xc"], ref["xc"]), (w["xm"], ref["xm"]), (w["xf"], ref["xf"])):
                worst_rel = max(worst_rel, abs(a_ / b_ - 1) if b_ else abs(a_)); n += 1
            mf[(M, k_, g)] = abs(max(c[g] for c in rr["fine"]) / max(c[g] for c in rr["medium"]) - 1)
m234 = max(v for (M, k_, g), v in mf.items() if M == 234); m490 = max(v for (M, k_, g), v in mf.items() if M == 490)
check("KA1", worst_rel <= 1e-12 and abs(m234 - 0.4964) < 5e-5 and abs(m490 - 0.5721) < 5e-5,
      f"{n} MS1 ladder rung values reproduced, max rel {worst_rel:.1e}; medium->fine maxima {m234:.4f} / {m490:.4f}")
save_cache()

# ------------------------------------------------------------------ KA2: plant recovery under R1
worst_err = 0.0; worst_edge_note = None
for M in (234, 490):
    for r in ("coarse", "medium", "fine", "ultra"):
        fs = snap_files(f"M{M}_transmit_uniform_{r}_t1000")
        if fs is None:
            continue
        for g in GKEYS:
            for k in (2.0, 0.1):
                rec = planted_only(fs[-1], g, k)
                worst_err = max(worst_err, max(abs(x / k - 1) for x in rec))
check("KA2", worst_err <= 0.01, f"planted-only field under R1 recovered within 1 %: worst {worst_err:.2e} (AC24 edge readout 4.6e-2)")

# ------------------------------------------------------------------ ladders under R1 + R2
ultra = snap_files("M234_transmit_uniform_ultra_t1000")
done_u = os.path.join(HERE, "parts", "M234_transmit_uniform_ultra_t1000", "done.json")
LADDER = {490: ("coarse", "medium", "fine"), 234: ("medium", "fine", "ultra") if ultra and os.path.exists(done_u) else ("coarse", "medium", "fine")}
INTERIM = LADDER[234][0] == "coarse"
RES["ladder_rungs"] = {str(k): v for k, v in LADDER.items()}; RES["interim"] = INTERIM
if not INTERIM:
    dj = json.load(open(done_u))
    nan = any(not np.all(np.isfinite(np.load(f)[v])) for f in ultra for v in ("q", "u", "v"))
    check("KA4", abs(dj["t"] - 1000) < 1e-6 and not nan, f"ultra t {dj['t']}, no NaN: {not nan}")
else:
    RES["checks"]["KA4"] = dict(ok=False, detail="ultra rung not available (run stopped under the frozen 1 GB RSS line)")
    P("KA4 NOT RUN: ultra rung not available; M234 graded on (coarse, medium, fine) = INTERIM, not a label")


def rung_stats(M, r, uq, plant=None):
    hist = [rows(f, uq, "fixed", plant) for f in snap_files(f"M{M}_transmit_uniform_{r}_t1000")]
    return [{g: (float(np.mean([h[i][g] for h in hist])), float(max(h[i][g] for h in hist) - min(h[i][g] for h in hist)))
             for g in GKEYS} for i in range(len(CELLS))]


ser = {}; stats = {}
for M in (234, 490):
    for k_, uq in READ:
        st = {r: rung_stats(M, r, uq) for r in LADDER[M]}; stats[(M, k_)] = st
        for i in range(len(CELLS)):
            for g in GKEYS:
                X = tuple(st[r][i][g][0] for r in LADDER[M]); S_ = tuple(st[r][i][g][1] for r in LADDER[M])
                ser[(M, k_, i, g)] = classify(X, S_)
save_cache()
cnt = {}
for (M, k_, i, g), v in ser.items():
    cnt[f"M{M}_{k_}_{v['cls']}"] = cnt.get(f"M{M}_{k_}_{v['cls']}", 0) + 1
bad = [(M, k_, CELLS[i]["foot"], CELLS[i]["Lstar"], CELLS[i]["V"], g, v["cls"], v["X"], v["s"])
       for (M, k_, i, g), v in ser.items() if v["cls"] not in OKCLS]
check("CONV", not bad, f"classes {cnt}; failing series {len(bad)}" + (" (INTERIM M234 ladder)" if INTERIM else ""))
RES["series_classes"] = cnt; RES["conv_failing"] = bad[:80]
P("ladder (R1 + R2), worst-U cell per (M, reading, gate): rung means / time spreads / class / p / U")
RES["ladder"] = {}
for (M, k_) in stats:
    for g in GKEYS:
        vs = [ser[(M, k_, i, g)] for i in range(len(CELLS))]
        w = max(vs, key=lambda v: v["U"])
        RES["ladder"][f"M{M}_{k_}_{g}"] = dict(X=w["X"], s=w["s"], cls=w["cls"], p=w["p"], U=w["U"], Lmax=max(v["L"] for v in vs))
        P(f"  M{M} {k_:2s} {g:9s} X " + " ".join(f"{x:.3e}" for x in w["X"]) + "  s " + " ".join(f"{x:.1e}" for x in w["s"])
          + f"  {w['cls']:14s} p {'-' if w['p'] is None else round(w['p'], 2)}  U {w['U']:.3e}")

# ------------------------------------------------------------------ brackets
BRACKETS = ["M234_transmit_uniform_medium", "M490_transmit_uniform_medium", "M234_absorb_uniform_medium",
            "M490_absorb_uniform_medium", "M234_reflect_uniform_medium", "M490_reflect_uniform_medium",
            "M234_transmit_hedgehog_medium"]
brk = {}
for M in (234, 490):
    for k_, _ in READ:
        brk.setdefault(f"M{M}_transmit_uniform_t1000", {})[k_] = [
            {g: (ser[(M, k_, i, g)]["L"], ser[(M, k_, i, g)]["U"]) for g in GKEYS} for i in range(len(CELLS))]
for b in BRACKETS:
    M = int(b[1:4]); fs = snap_files(b)
    for k_, uq in READ:
        hist = [rows(f, uq, "fixed") for f in fs]; fin = hist[-1]
        wfin = {g: max(c[g] for c in fin) for g in GKEYS}
        chg = max(abs(max(c[g] for c in h) / wfin[g] - 1) if wfin[g] > 0 else 0.0 for h in hist for g in GKEYS)
        per = ([dict(c) for c in fin] if chg <= 0.05 else
               [{g: max(h[i][g] for h in hist) * (1 + chg) for g in GKEYS} for i in range(len(CELLS))])
        im = LADDER[M].index("medium")
        out = []
        for i in range(len(CELLS)):
            d = {}
            for g in GKEYS:
                s_ = ser[(M, k_, i, g)]; xm = s_["X"][im]; G_ = per[i][g]
                d[g] = (G_ * s_["L"] / xm, G_ * s_["U"] / xm) if xm > 0 else (0.0, G_ + s_["U"])
            out.append(d)
        brk.setdefault(b, {})[k_] = out
save_cache()
NB = range(len(CELLS))
Umax = {g: max(brk[b][k_][i][g][1] for b in brk for k_, _ in READ for i in NB) for g in GKEYS}
Lmin = {g: min(brk[b][k_][i][g][0] for b in brk for k_, _ in READ for i in NB) for g in GKEYS}
P("bracket per gate over cells, brackets, readings [min L, max U] (ratio to line), worst-U location:")
RES["bracket_per_gate"] = {}
for g in GKEYS:
    b, k_, i = max(((b, k_, i) for b in brk for k_, _ in READ for i in NB), key=lambda t: brk[t[0]][t[1]][t[2]][g][1])
    RES["bracket_per_gate"][g] = dict(Lmin=Lmin[g], Umax=Umax[g], at=[b, k_, CELLS[i]["foot"], CELLS[i]["Lstar"], CELLS[i]["V"]])
    P(f"  {g:9s} [{Lmin[g]:.3e}, {Umax[g]:.3e}]  at {b} {k_} {CELLS[i]['foot']} Lstar {CELLS[i]['Lstar']} V {CELLS[i]['V'] / 1e3:.0f}")

# ------------------------------------------------------------------ MUTATE through R1 + R4
mut2 = mut01 = True; near = []; minL2 = math.inf; maxU01 = -math.inf; m01fail = []
for M in (234, 490):
    for k_, uq in READ:
        for g in GKEYS:
            for k in (2.0, 0.1):
                st = {r: rung_stats(M, r, uq, (g, k)) for r in LADDER[M]}
                for i, c in enumerate(CELLS):
                    s_ = classify(tuple(st[r][i][g][0] for r in LADDER[M]), tuple(st[r][i][g][1] for r in LADDER[M]))
                    if k == 2.0:
                        mut2 &= s_["L"] > 1; minL2 = min(minL2, s_["L"])
                    else:
                        maxU01 = max(maxU01, s_["U"])
                        if ser[(M, k_, i, g)]["U"] + 0.1 < 1:
                            if not s_["U"] < 1:
                                mut01 = False; m01fail.append((M, k_, g, c["foot"], c["Lstar"], c["V"], s_["cls"], s_["X"]))
                        else:
                            near.append((M, k_, g, c["foot"], c["Lstar"], c["V"]))
        save_cache()
RES["mutate"] = dict(minL_k2=minL2, maxU_k01=maxU01, k01_failures=m01fail[:40], near_failures=near[:40], n_near=len(near))
check("MUTATE_k2", mut2, f"planted 2x reads FAIL (L > 1) everywhere: min L {minL2:.3f}")
check("MUTATE_k0.1", mut01, f"planted 0.1x reads PASS (U < 1) where base U + 0.1 < 1: max U {maxU01:.3f}; "
      f"failures {len(m01fail)}; near-failures {len(near)}")

# ------------------------------------------------------------------ diagnostic D
def dqB_dV_mean(M, r):
    acc = None
    for f in snap_files(f"M{M}_transmit_uniform_{r}_t1000"):
        s = np.load(f); q, u, v, re, te, Mr = s["q"], s["u"], s["v"], s["re"], s["te"], float(s["M"])
        rc = 0.75 * (re[1:] ** 4 - re[:-1] ** 4) / (re[1:] ** 3 - re[:-1] ** 3)
        qq = np.maximum(1.0 + Mr ** 2 * (0.5 / rc[:, None] + 0.5 * (1.0 - (u ** 2 + v ** 2))), 0.0)
        dV = 2 * np.pi * ((re[1:] ** 3 - re[:-1] ** 3) / 3)[:, None] * (np.cos(te[:-1]) - np.cos(te[1:]))[None, :]
        m = (qq - 1.0) * dV
        acc = m if acc is None else acc + m
    return acc / 5, re


def restrict(mf_, ref, rec):
    nr = min(len(rec) - 1, (len(ref) - 1) // 2)
    assert np.allclose(ref[:2 * nr + 1:2], rec[:nr + 1], rtol=1e-10)
    a = mf_[:2 * nr]
    return (a[0::2] + a[1::2])[:, 0::2] + (a[0::2] + a[1::2])[:, 1::2], nr


BANDS = ((2, 5), (5, 20), (20, 100), (100, 2000))
RES["diagnostic_D"] = {}
for M in (234, 490):
    for pair in (("coarse", "medium"), ("medium", "fine")) + ((("fine", "ultra"),) if (M == 234 and not INTERIM) else ()):
        mc, rec = dqB_dV_mean(M, pair[0]); mf_, ref = dqB_dV_mean(M, pair[1])
        mr, nr = restrict(mf_, ref, rec)
        dlt = np.abs(mr - mc[:nr]); rcc = np.sqrt(rec[1:nr + 1] * rec[:nr])
        tot = dlt.sum()
        fr = {f"{a}-{b}": float(dlt[(rcc >= a) & (rcc < b)].sum() / tot) for a, b in BANDS}
        RES["diagnostic_D"][f"M{M}_{pair[0]}_{pair[1]}"] = dict(fractions=fr, total_abs=float(tot),
                                                               total_charge_coarser=float(np.abs(mc[:nr]).sum()))
        P(f"D M{M} {pair[0]}->{pair[1]}: |delta dq_B dV| fraction by band {fr}; total {tot:.3e} vs |dq_B dV| {np.abs(mc[:nr]).sum():.3e}")
ms1_div = [(M, k_, g) for (M, k_, f_, L_, V_, g, cls, p_) in [tuple(x) for x in ms1["conv_failing_series"]] if cls == "DIVERGENT"]
key_mf = "M234_medium_fine"
inner = RES["diagnostic_D"][key_mf]["fractions"]["2-5"] + RES["diagnostic_D"][key_mf]["fractions"]["5-20"]
ms1_div_now = []
for x in ms1["conv_failing_series"]:
    M, k_, foot, Ls, V, g, cls, p_ = x
    if cls != "DIVERGENT":
        continue
    i = next(j for j, c in enumerate(CELLS) if c["foot"] == foot and c["Lstar"] == Ls and c["V"] == V)
    ms1_div_now.append(ser[(M, k_, i, g)]["cls"])
temporal = bool(ms1_div_now) and all(c_ == "NOISE" for c_ in ms1_div_now)
Dlab = "R_A-SCALE" if inner >= 0.5 else ("TEMPORAL" if temporal else "DISTRIBUTED")
RES["diagnostic_D"]["verdict"] = dict(label=Dlab, inner_fraction_M234_medium_fine=inner,
                                      ms1_divergent_now={c_: ms1_div_now.count(c_) for c_ in set(ms1_div_now)}, n_ms1_listed=len(ms1_div_now))
P(f"D verdict: {Dlab} (M234 medium->fine fraction at r < 20 R_A {inner:.3f}; MS1-DIVERGENT series now "
  f"{RES['diagnostic_D']['verdict']['ms1_divergent_now']} of {len(ms1_div_now)} listed in MS1.json)")

# ------------------------------------------------------------------ label
need = ("KA1", "KA2", "KA3", "CONV", "MUTATE_k2", "MUTATE_k0.1")
fails = [(c["foot"], c["Lstar"], c["V"], g) for i, c in enumerate(CELLS) for g in GKEYS
         if all(max(brk[b][k_][i][g][0] for k_, _ in READ) > 1 for b in brk)]
allU = max(Umax.values())
if not all(RES["checks"][k]["ok"] for k in need):
    label = "NO VERDICT"
elif allU < 1:
    label = "PASS (moving Sun, scoped)"
elif fails:
    label = "FAIL"
else:
    label = "UNDECIDED"
if INTERIM:
    label = f"INTERIM (not a label; M234 on coarse/medium/fine): would read {label}"
elif not RES["checks"].get("KA4", {}).get("ok"):
    label = "NO VERDICT"
RES.update(label=label, fail_cells=fails, max_U_all=allU,
           rss_MB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024 if sys.platform == "darwin" else 1024))
P(f"max U over everything {allU:.3e} of the line; RSS {RES['rss_MB']:.0f} MB")
P(f"LABEL: {label}  (v3s; AC2q differs by s^2/rho0 ~ 4e-6)  kappa = 1/2 FITTED; not theory closed")
tag = "MS2_interim" if INTERIM else "MS2"
json.dump(RES, open(os.path.join(HERE, f"{tag}.json"), "w"), indent=1, default=lambda o: None if o is None else float(o))
open(os.path.join(HERE, f"{tag.lower()}.out"), "w").write("\n".join(OUT) + "\n")
save_cache()
