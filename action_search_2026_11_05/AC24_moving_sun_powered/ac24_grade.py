#!/usr/bin/env python3
"""AC24 grader: AC15's moving-Sun observables with the medium base, a fine rung and a planted
known-size control. Criteria: FROZEN_CRITERIA.md (81e48c2a3c, on origin as 845f922d4e).

AC15's physical inputs, cells, field() and grade_snap() are taken VERBATIM from
AC15_moving_sun_nonlinear/grade.py (lines 26-135, read and exec'd here). The only change is one line in
field(): `dq = qq - 1.0` gains `+ PLANT(...)` when a plant is set. With PLANT = None the code is
AC15's (checked by KA0).

  python3 action_search_2026_11_05/AC24_moving_sun_powered/ac24_grade.py
kappa = 1/2 FITTED; footings never pooled; not theory closed.
"""
import os, sys, json, glob, math
sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
AC15 = os.path.join(HERE, "..", "AC15_moving_sun_nonlinear")
OUT, RES = [], {"lane": "AC24_moving_sun_powered", "criteria": ["81e48c2a3c", "845f922d4e"], "checks": {}}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, ok, detail):
    RES["checks"][name] = dict(ok=bool(ok), detail=str(detail)); P(f"{name} {'PASS' if ok else 'FAIL'} {detail}")


# ------------------------------------------------------------------ AC15 code, verbatim (one patched line)
src = open(os.path.join(AC15, "grade.py")).read().split("\n")
i0 = next(i for i, l in enumerate(src) if l.startswith("# ------------------------------------------------------------------ physical inputs"))
i1 = next(i for i, l in enumerate(src) if l.startswith("# field-code test"))
block = "\n".join(src[i0:i1])
OLD = "    dq = qq - 1.0\n"
assert block.count(OLD) == 1
block_p = block.replace(OLD, "    dq = qq - 1.0 + (PLANT(rc, tc, Mcell) if PLANT is not None else 0.0)\n")
NS = {"np": np, "math": math, "glob": glob, "os": os, "json": json, "P": P, "PARTS": os.path.join(AC15, "parts"), "PLANT": None}
from scipy.special import eval_legendre
NS["eval_legendre"] = eval_legendre
exec(compile(block_p, "AC15_grade_block", "exec"), NS)
CELLS, PLAN, Q2_LINE, GKEYS, G, AU = NS["CELLS"], NS["PLAN"], NS["Q2_LINE"], NS["GKEYS"], NS["G"], NS["AU"]
grade_snap, worst, field = NS["grade_snap"], NS["worst"], NS["field"]
CELL_BY_M = {round(c["M"], 9): c for c in CELLS}
assert len(CELL_BY_M) == len(CELLS), "cell M not unique"


def load(tag, k=None):
    for base in (os.path.join(HERE, "parts"), os.path.join(AC15, "parts")):
        fs = sorted(glob.glob(os.path.join(base, tag, "snap_*.npz")))
        if fs:
            return [dict(np.load(f)) for f in (fs if k is None else [fs[k]])]
    return None


# ------------------------------------------------------------------ KA0: code identity with AC15
g15 = json.load(open(os.path.join(AC15, "GRADE.json")))
worst_rel = 0.0; n0 = 0
for b, per in g15["brackets"].items():
    if not b.endswith("_medium"):
        continue
    snaps = load(b)
    for k_, use_qB in (("q", False), ("qB", True)):
        hist = [worst(grade_snap(s_, use_qB)) for s_ in snaps]
        env = {k: max(h[k] for h in hist) for k in GKEYS}
        for k in GKEYS:
            for mine, ref in ((hist[-1][k], per[k_]["final"][k]), (env[k], per[k_]["envelope"][k])):
                worst_rel = max(worst_rel, abs(mine / ref - 1) if ref else abs(mine)); n0 += 1
d15 = open(os.path.join(HERE, "hydro_ac24.diff")).read()
diff_ok = d15.count("\n<") == 2 or d15.count("< ") == 2
check("KA0", worst_rel <= 1e-12 and diff_ok, f"AC15 medium brackets reproduced, {n0} numbers, max rel {worst_rel:.1e} (1e-12); "
      f"hydro diff only the fine choice: {diff_ok}")

# ------------------------------------------------------------------ KA3: three rungs
def ka3_err(tag):
    s = load(tag)
    if s is None:
        return None
    s = s[-1]; re = s["re"]; rc = np.sqrt(re[1:] * re[:-1]); sel = rc >= 5
    return float(np.abs(s["q"][sel] - 1).max())


e3 = {r: ka3_err(f"M234_transmit_uniform_{r}_NOGRAV_t50") for r in ("coarse", "medium", "fine")}
if all(v is not None for v in e3.values()):
    p1, p2 = math.log2(e3["coarse"] / e3["medium"]), math.log2(e3["medium"] / e3["fine"])
    check("KA3", e3["medium"] <= 1e-2 and p1 >= 0.8 and p2 >= 0.8,
          f"gravity off t 50 r >= 5: max|q-1| coarse {e3['coarse']:.2e} medium {e3['medium']:.2e} (base line 1e-2) "
          f"fine {e3['fine']:.2e}; observed order {p1:.2f}, {p2:.2f} (line 0.8)")
    RES["KA3"] = dict(err=e3, order=[p1, p2])
else:
    check("KA3", False, f"runs missing {e3}")

# ------------------------------------------------------------------ convergence, fine rung at t 1000
conv_ok = True; RES["convergence"] = {}
for M in (234, 490):
    w = {}
    for r in ("coarse", "medium", "fine"):
        s = load(f"M{M}_transmit_uniform_{r}_t1000")
        w[r] = None if s is None else {k_: worst(grade_snap(s[-1], uq)) for k_, uq in (("q", False), ("qB", True))}
    if w["medium"] is None or w["fine"] is None:
        conv_ok = False; RES["convergence"][M] = "missing"; continue
    ch = max(abs(w["fine"][k_][k] / w["medium"][k_][k] - 1) for k_ in ("q", "qB") for k in GKEYS if w["medium"][k_][k] > 0)
    flip = any((w["fine"][k_][k] > 1) != (w["medium"][k_][k] > 1) for k_ in ("q", "qB") for k in GKEYS)
    chc = (max(abs(w["medium"][k_][k] / w["coarse"][k_][k] - 1) for k_ in ("q", "qB") for k in GKEYS if w["coarse"][k_][k] > 0)
           if w["coarse"] else None)
    s3 = load(f"M{M}_transmit_uniform_medium")
    w3 = {k_: worst(grade_snap(s3[-1], uq)) for k_, uq in (("q", False), ("qB", True))}
    tch = max(abs(w3[k_][k] / w["medium"][k_][k] - 1) for k_ in ("q", "qB") for k in GKEYS if w["medium"][k_][k] > 0)
    RES["convergence"][M] = dict(medium_to_fine=ch, flip=flip, coarse_to_medium=chc, medium_t1000_vs_t3000=tch, rungs=w)
    conv_ok &= ch <= 0.30 and not flip
    P(f"ladder M{M} t 1000: max rel change medium->fine {ch:.3f} (line 0.30), flip {flip}; coarse->medium {chc} (reported); "
      f"medium t1000 vs t3000 {tch:.3f} (reported)")
check("CONV", conv_ok, "medium vs fine at t 1000, every graded ratio within 30 %, no label flip, both M")

# ------------------------------------------------------------------ base brackets (medium)
BRACKETS = ["M234_transmit_uniform_medium", "M490_transmit_uniform_medium", "M234_absorb_uniform_medium",
            "M490_absorb_uniform_medium", "M234_reflect_uniform_medium", "M490_reflect_uniform_medium",
            "M234_transmit_hedgehog_medium"]
missing = [b for b in BRACKETS if load(b) is None]
RES["brackets"] = {}
for b in BRACKETS:
    snaps = load(b)
    if snaps is None:
        continue
    per = {}
    for k_, uq in (("q", False), ("qB", True)):
        hist = [worst(grade_snap(s_, uq)) for s_ in snaps]
        fin = hist[-1]; env = {k: max(h[k] for h in hist) for k in GKEYS}
        chg = max(abs(h[k] / fin[k] - 1) if fin[k] > 0 else 0.0 for h in hist for k in GKEYS)
        per[k_] = dict(final=fin, envelope=env, max_change_last20=chg, steady=chg <= 0.05,
                       graded=(fin if chg <= 0.05 else env), rows=grade_snap(snaps[-1], uq))
    RES["brackets"][b] = per
    for k_ in ("q", "qB"):
        g = per[k_]["graded"]
        P(f"[{b} {k_}] {'steady' if per[k_]['steady'] else 'NOT STEADY'} (chg {per[k_]['max_change_last20']:.2e}): "
          + ", ".join(f"{k} {g[k]:.3g}" for k in GKEYS))

# ------------------------------------------------------------------ powered control
SH = (0.5, 0.9)


def shell_frac(re_lo, re_hi, s1, s2):
    lo, hi = np.maximum(re_lo, s1), np.minimum(re_hi, s2)
    return np.where(hi > lo, (hi ** 3 - lo ** 3) / (re_hi ** 3 - re_lo ** 3), 0.0)


TH = np.linspace(0, math.pi, 200001)
P2c = 0.5 * (3 * np.cos(TH) ** 2 - 1); dP2c = -3 * np.sin(TH) * np.cos(TH)
QSHAPE = np.sqrt(9 * P2c ** 2 + dP2c ** 2)            # |a| of a unit exterior l = 2 moment, times rp^4
QMAX, QSPAN = float(QSHAPE.max()), float(QSHAPE.max() - QSHAPE.min())


def make_plant(kind, planet, k, re_edges):
    """returns PLANT(rc, tc, Mcell) in code charge units for every cell: analytic continuum amplitude."""
    lo, hi = re_edges[:-1], re_edges[1:]

    def fn(rc, tc, Mcell):
        c = CELL_BY_M[round(Mcell, 9)]
        rp = PLAN[planet][0] * AU / c["RA"]
        s1, s2 = SH[0] * rp, SH[1] * rp
        conv = G * c["rho"] * c["RA"]
        Mrun = RUN_M[0]
        scale = max((Mcell / Mrun) ** 2, 1.0)
        f = shell_frac(lo, hi, s1, s2)[:, None]
        if kind == "MONO":
            T = k * PLAN[planet][1] / conv                              # code accel target at rp
            Mtot = T * rp ** 2
            A = Mtot / (4 * math.pi * (s2 ** 3 - s1 ** 3) / 3)
            return A * f / scale * np.ones_like(tc)[None, :]
        I_unit = 2 * math.pi * (2 / 5) * (s2 ** 5 - s1 ** 5) / 5      # int P2 r^2 dq dV for A = 1
        if kind == "QUAD":
            T = k * PLAN[planet][1] / conv
            I = T * rp ** 4 / QSPAN
        else:                                                           # QUAD3: Q_eff = |a_l2| max / r -> line
            T = k * Q2_LINE * rp * c["RA"] / conv
            I = T * rp ** 4 / QMAX
        A = I / I_unit
        P2 = 0.5 * (3 * np.cos(tc) ** 2 - 1)
        return A * f / scale * P2[None, :]
    return fn


RUN_M = [None]
TESTS = [("MONO", p, f"G1_{p}") for p in PLAN] + [("QUAD", p, f"G2_{p}") for p in PLAN] + [("QUAD3", "Saturn", "G3")]


def planted_only(snap, uq, kind, planet, k):
    """gate values of the planted vector field alone: field(with) - field(without), through G1/G2/G3 formulas."""
    out = []
    for c in CELLS:
        rp_ = {pl: d * AU / c["RA"] for pl, (d, _) in PLAN.items()}
        NS["PLANT"] = None
        f0, tc = field(snap, c["M"], list(rp_.values()), uq)
        NS["PLANT"] = make_plant(kind, planet, k, snap["re"])
        f1, _ = field(snap, c["M"], list(rp_.values()), uq)
        NS["PLANT"] = None
        conv = G * c["rho"] * c["RA"]; rp = rp_[planet]
        ar, at = f1[rp][0] - f0[rp][0], f1[rp][1] - f0[rp][1]
        ar2, at2 = f1[rp][2] - f0[rp][2], f1[rp][3] - f0[rp][3]
        mag = np.hypot(ar, at) * conv
        v = dict(MONO=mag.max() / PLAN[planet][1], QUAD=(mag.max() - mag.min()) / PLAN[planet][1],
                 QUAD3=np.hypot(ar2, at2).max() * conv / (rp * c["RA"]) / Q2_LINE)[kind]
        out.append(float(v))
    return out


def planted_full(snap, uq, kind, planet, k):
    NS["PLANT"] = make_plant(kind, planet, k, snap["re"])
    rows = grade_snap(snap, uq)
    NS["PLANT"] = None
    return rows


P1 = P2ok = P3 = True; near = []; prep = {}
for b in BRACKETS:
    snaps = load(b)
    if snaps is None:
        continue
    s = snaps[-1]; RUN_M[0] = float(s["M"])
    for kind, planet, gate in TESTS:
        for k in (2.0, 0.1):
            rec = planted_only(s, False, kind, planet, k)
            err = max(abs(x / k - 1) for x in rec)
            P1 &= err <= 0.05
            prep.setdefault(f"{kind}_{planet}_k{k}", []).append(err)
            for k_, uq in (("q", False), ("qB", True)):
                full = planted_full(s, uq, kind, planet, k)
                base = RES["brackets"][b][k_]["rows"]
                for rf, rb in zip(full, base):
                    if k == 2.0:
                        P2ok &= rf[gate] > 1
                    else:
                        if rb[gate] + 0.1 < 1:
                            P3 &= rf[gate] <= 1
                        else:
                            near.append((b, k_, rb["foot"], rb["Lstar"], rb["V"], gate, rb[gate]))
RES["power"] = dict(recovery_max_rel_err={k: max(v) for k, v in prep.items()}, near_failures=near)
check("P1", P1 and not missing, f"planted-only gates recovered within 5 % on every bracket/cell/gate: worst "
      f"{max(max(v) for v in prep.values()) if prep else None:.2e}")
check("P2", P2ok and not missing, "k = 2 plant reads over its line in every cell, every bracket, q and q_B (power)")
check("P3", P3 and not missing, f"k = 0.1 plant reads under its line where base + 0.1 < 1; near-failures reported: {len(near)}")

# ------------------------------------------------------------------ label
over_cell = {}
for b, per in RES["brackets"].items():
    for k_ in ("q", "qB"):
        for r in per[k_]["rows"]:
            vals = [r[k] for k in GKEYS]
            if not per[k_]["steady"]:
                vals = [x_ * (1 + per[k_]["max_change_last20"]) for x_ in vals]
            over_cell.setdefault((r["foot"], r["Lstar"], r["V"]), []).append(max(vals) > 1)
need = ("KA0", "KA3", "CONV", "P1", "P2")
if missing or not all(RES["checks"][k]["ok"] for k in need):
    label = "NO VERDICT"
elif all(not any(v) for v in over_cell.values()) and RES["checks"]["P3"]["ok"]:
    label = "PASS (moving Sun, scoped)"
elif any(all(v) for v in over_cell.values()):
    label = "FAIL"
else:
    label = "UNDECIDED"
RES["missing"] = missing; RES["label"] = label
RES["worst_over_brackets"] = {k: max(per[k_]["graded"][k] for per in RES["brackets"].values() for k_ in ("q", "qB")) for k in GKEYS} if RES["brackets"] else {}
P(f"worst over every medium bracket (ratio to line, q and q_B): {RES['worst_over_brackets']}")
P(f"LABEL: {label}  kappa = 1/2 FITTED; not theory closed")
tag = "GRADE"
for x in RES["brackets"].values():
    for k_ in ("q", "qB"):
        x[k_].pop("rows", None)
json.dump(RES, open(os.path.join(HERE, f"{tag}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "grade.out"), "w").write("\n".join(OUT) + "\n")
