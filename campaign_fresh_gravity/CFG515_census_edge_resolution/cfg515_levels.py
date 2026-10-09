#!/usr/bin/env python3
"""CFG515 (b) early-type lensing levels with the census edge (FROZEN_CRITERIA.md 2bbe75602, section 3b; CFG485 caveat 2 / R8).
CFG485's script is executed read-only up to its C6 banner (CFG95 calibration, CFG61 grid stack, released per-class K1 blocks, controls
C1-C5).  Model: nu_mono phantom of each grid node's present baryons, fully settled, out to min(r_edge, r_ta) with
r_ta = CFG61's 0.40 r_ta edge / 0.40 at that node and redshift; + point mass.  Two-halo amplitude profiled per class (6 dof).
PASS (early types) iff chi2(census edge) - chi2(B1 = CFG95's law to 0.40 r_ta) <= 4 on both footings.  Late types: same rule, reported.
MUTATE (CFG515_MUTATE=1): f_ret = 1 and 0.01.
Run: nice -n 15 python3 campaign_fresh_gravity/CFG515_census_edge_resolution/cfg515_levels.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, json, math, contextlib, time
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, LANES)
import cfg515_lib as L                                                       # noqa: E402
try:
    os.nice(15)
except OSError:
    pass
MUTATE = os.environ.get("CFG515_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
MODES = L.modes()
FOOTS = ("canonical", "alt")
LOG, CHK = [], {}
RES = {"lane": "CFG515", "script": "cfg515_levels", "mutate": MUTATE, "modes": list(MODES)}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}: {msg}")


P(__doc__.split("Run:")[0].strip())
# ------------------------------------------------------------------ CFG485 read-only prefix
p485 = os.path.join(LANES, "CFG485_kids_split_settling_completeness", "cfg485_settling_split.py")
src = open(p485).read()
marker = "# ================================================================== C6"
assert src.count(marker) == 1
_e = os.environ.pop("CFG485_MUTATE", None)
NS = {"__file__": p485, "__name__": "cfg485_ro"}
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(compile(src[:src.index(marker)], "cfg485_ro", "exec"), NS)
if _e is not None:
    os.environ["CFG485_MUTATE"] = _e
R485 = NS["R"]
nf485 = [c["name"][:60] for c in R485.checks if c["load_bearing"] and not c["ok"]]
check("K0 CFG485's own controls C1-C5 pass when its prefix is executed read-only", not nf485,
      f"{len(R485.checks)} checks, failures {nf485}")
C = NS["C"]
LMG, ZG, RG, PROF, fcold = NS["LMG"], NS["ZG"], NS["RG"], NS["PROF"], NS["fcold"]
rgrid, project, contrib, parts, chi2_free, chi2_none = NS["rgrid"], NS["project"], NS["contrib"], NS["parts"], NS["chi2_free"], NS["chi2_none"]
CB95, DF, C30, idx, d_early, d_late, NZG, NLMG = NS["CB95"], NS["DF"], NS["C30"], NS["idx"], NS["d_early"], NS["d_late"], NS["NZG"], NS["NLMG"]
P(f"  CFG485 prefix executed ({time.time() - T0:.0f} s)")


def tables(foot, mode):
    """per (foot, b): (NLMG, len(RG)) phantom Delta Sigma truncated at min(r_edge(f_ret), r_ta(node, z))."""
    out = {}; fr = np.zeros(NLMG); xe = np.zeros((NLMG, NZG))
    for b, z in enumerate(ZG):
        tab = np.zeros((NLMG, len(RG)))
        for a, lm in enumerate(LMG):
            Mb = 10 ** lm * (1 + fcold(lm))
            f = L.fret(mode, Mb); fr[a] = f
            re = math.sqrt(C.GMPC * Mb / C.A0[foot]) / L.ln_fac(f)
            rta = PROF[(foot, "red", lm, z)]["re"] / 0.40
            xe[a, b] = re / rta
            rc = np.minimum(rgrid, min(re, rta))
            ML = np.asarray(C.M_law(Mb, rc, C.A0[foot], C.nu_mono), float)
            tab[a] = project(rgrid, ML - Mb, RG)
        out[(foot, b)] = tab
    return out, fr, xe


J485 = json.load(open(os.path.join(LANES, "CFG485_kids_split_settling_completeness", "cfg485_settling_split_results.json")))["numbers"]["R8"]
OUTR = {}
B1 = {}
for foot in FOOTS:
    B1[foot] = {}
    for cls, nm, dd, blk in ((1, "early", d_early, slice(15, 30)), (0, "late", d_late, slice(0, 15))):
        Ph1, Bar1, T1, _ = parts(CB95[(foot, cls)])
        Ci = np.linalg.inv(C30[blk, blk][np.ix_(idx, idx)])
        x1, A1 = chi2_free(dd[idx] - (Ph1 + Bar1)[idx], Ci, T1[idx])
        B1[foot][nm] = dict(chi2=x1, A=A1, Ci=Ci)
k5 = max(abs(B1[f]["early"]["chi2"] - J485[f]["early"]["chi2_B1"]) for f in FOOTS)
check("K5 CFG485 machinery reproduces its committed R8 B1 chi2 (early 2.548 / 2.865) within 1e-3", k5 <= 1e-3, f"max |diff| {k5:.1e}")

for mode in MODES:
    OUTR[mode] = {}
    for foot in FOOTS:
        t = time.time()
        TB, fr, xe = tables(foot, mode)
        r_ = {"fret_nodes": dict(zip([float(x) for x in LMG], fr.tolist())), "xedge_z0.25": dict(zip([float(x) for x in LMG], xe[:, 2].tolist()))}
        for cls, nm, dd, blk in ((1, "early", d_early, slice(15, 30)), (0, "late", d_late, slice(0, 15))):
            cb = contrib(cls, foot, TB, DF[foot][cls])
            Ph, Bar, T, _ = parts(cb)
            mS = (Ph + Bar)[idx]
            Ci = B1[foot][nm]["Ci"]
            xs, As = chi2_free(dd[idx] - mS, Ci, T[idx])
            r_[nm] = dict(chi2=xs, A=As, chi2_no2h=chi2_none(dd[idx] - mS, Ci), chi2_B1=B1[foot][nm]["chi2"], A_B1=B1[foot][nm]["A"],
                          d_vs_B1=xs - B1[foot][nm]["chi2"], model=mS.tolist(), data=dd[idx].tolist(), passed=(xs - B1[foot][nm]["chi2"]) <= 4.0)
        OUTR[mode][foot] = r_
        lmk = [10.3, 10.75, 11.1]
        P(f"\n  [{mode:6s}|{foot:9s}] ({time.time() - t:.0f} s) f_ret at log M* 10.3/10.75/11.1: "
          + "/".join(f"{fr[int(np.argmin(np.abs(LMG - v)))]:.3f}" for v in lmk)
          + "; x_edge (z 0.25): " + "/".join(f"{xe[int(np.argmin(np.abs(LMG - v))), 2]:.3f}" for v in lmk))
        for nm in ("early", "late"):
            q = r_[nm]
            P(f"      {nm:5s}: chi2 {q['chi2']:.2f} (A {q['A']:.2f}; no-2h {q['chi2_no2h']:.1f}) vs B1 {q['chi2_B1']:.2f} (A {q['A_B1']:.2f}): "
              f"d {q['d_vs_B1']:+.2f} -> {'PASS' if q['passed'] else 'FAIL'}{'' if nm == 'early' else ' (reported)'}")
            P(f"             data  {np.round(q['data'], 2).tolist()}\n             model {np.round(q['model'], 2).tolist()}")
    OUTR[mode]["b_pass"] = all(OUTR[mode][f]["early"]["passed"] for f in FOOTS)
    OUTR[mode]["late_pass_reported"] = all(OUTR[mode][f]["late"]["passed"] for f in FOOTS)
    P(f"  => {mode}: (b) early types {'PASS' if OUTR[mode]['b_pass'] else 'FAIL'}; late types (reported) "
      f"{'PASS' if OUTR[mode]['late_pass_reported'] else 'FAIL'}")
RES["rows"] = OUTR
RES["B1"] = {f: {nm: {k: v for k, v in B1[f][nm].items() if k != "Ci"} for nm in B1[f]} for f in FOOTS}
if MUTATE:
    m1 = max(abs(OUTR["one"][f]["early"]["chi2"] - J485[f]["early"]["chi2_S"]) for f in FOOTS)
    check("M1 (levels) f_ret = 1 reproduces CFG485 R8 early-type S chi2 (30.45 / 38.11) within 1", m1 <= 1.0,
          f"max |diff| {m1:.3f}; late {OUTR['one']['canonical']['late']['chi2']:.2f} / {OUTR['one']['alt']['late']['chi2']:.2f} "
          f"(CFG485 47.79 / 52.69, settling q included there)")

RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nlb = sum(1 for c_ in CHK.values() if c_["load_bearing"] and not c_["ok"])
P(f"\n{sum(c_['ok'] for c_ in CHK.values())}/{len(CHK)} checks pass; load-bearing failures {nlb}; elapsed {RES['elapsed_s']} s")
json.dump(RES, open(os.path.join(HERE, f"cfg515_levels_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg515_levels{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nlb else 0)
