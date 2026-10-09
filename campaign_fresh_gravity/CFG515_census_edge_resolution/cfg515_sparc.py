#!/usr/bin/env python3
"""CFG515 (c) SPARC with the census edge (FROZEN_CRITERIA.md 2bbe75602, section 3c).
CFG487's SPARC harness (itself CFG346's: CFG45 + CFG4_galaxy_law prefixes exec'd read-only; SPARC_Lelli2016c.mrt + rotmod) is executed
read-only from cfg487_data.py (its "(a) SPARC" section up to the scoring loop); only the switch profile is replaced:
f(r) = 1 for r <= min(r_edge, r_ta), 0 beyond (fully settled), r_edge = r_M / ln(1 + f_ret f_b/(1 - f_b)), f_ret per galaxy from cfg515_lib.
PASS iff S-A3 >= 90% (|d log v| < 0.03 at R_HI) for spirals AND dwarfs and rotmod RAR |d rms| < 0.005, both footings (CFG346).
MUTATE (CFG515_MUTATE=1): f_ret = 1 and 0.01.
Run: nice -n 15 python3 campaign_fresh_gravity/CFG515_census_edge_resolution/cfg515_sparc.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, math, json, time, contextlib
import numpy as np
from scipy.integrate import quad

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, LANES); sys.path.insert(0, os.path.join(LANES, "CFG487_settled_fraction_switch"))
import cfg515_lib as L                                                       # noqa: E402
import cfg487_lib as LB                                                      # noqa: E402  (read-only)
import CFG7_common as C7                                                     # noqa: E402
import CFG4_common as C4                                                     # noqa: E402
try:
    os.nice(15)
except OSError:
    pass
MUTATE = os.environ.get("CFG515_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
MODES = L.modes()
FOOTS = ("canonical", "alt")
LOG, CHK = [], {}
RES = {"lane": "CFG515", "script": "cfg515_sparc", "mutate": MUTATE, "modes": list(MODES)}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}: {msg}")


P(__doc__.split("Run:")[0].strip())
p487 = os.path.join(LANES, "CFG487_settled_fraction_switch", "cfg487_data.py")
src = open(p487).read()
m0 = "# =================================================================================================== (a) SPARC (CFG346 copy)"
m1 = "SPA = {}"
assert src.count(m0) == 1 and src.count(m1) == 1
NS = dict(os=os, sys=sys, io=io, math=math, json=json, time=time, contextlib=contextlib, np=np, quad=quad, C7=C7, C4=C4, LB=LB,
          LANES=LANES, FOOTS=FOOTS, P=lambda *a: None, m_profile=None, __name__="cfg487_sparc_ro")
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[src.index(m0):src.index(m1)], "cfg487_sparc_ro", "exec"), NS)
MSUN, G_ = NS["MSUN"], NS["G_"]
P(f"  CFG487 SPARC harness executed read-only ({time.time() - T0:.0f} s): {len(NS['SPROWS'])} P3 rows, {len(NS['GMB'])} rotmod galaxies")
FRL = {}


def fprof_sparc(r, Mb, a0, mode, rho_tot, rho_b, r_ta=None, Mta=None):
    """CFG515 replacement: fully settled inside min(r_edge(f_ret), r_ta); mode = ('one', fret_mode or None, False)."""
    fm = mode[1]
    if fm is None:
        return np.ones_like(r)
    f = L.fret(fm, Mb / MSUN)
    FRL.setdefault(fm, []).append(f)
    re = math.sqrt(G_ * Mb / a0) / L.ln_fac(f)
    if r_ta is not None:
        re = min(re, r_ta)
    return np.ones_like(r) * (r <= re)


NS["fprof_sparc"] = fprof_sparc
sparc_a3, sparc_rms_sw, RMS0 = NS["sparc_a3"], NS["sparc_rms_sw"], NS["RMS0"]


def frac_beyond(kind, foot, fm):
    """share of P3 rows of this kind whose R_HI lies beyond the (capped) census edge; max |d log v|."""
    n = b = 0
    for s in NS["SPROWS"]:
        if s["kind"] != kind:
            continue
        Mb = s["Mb"] * MSUN; a0 = NS["A0SI"][foot]
        re = math.sqrt(G_ * Mb / a0) / L.ln_fac(L.fret(fm, s["Mb"]))
        n += 1; b += (s["r"] * NS["KPC"] > min(re, NS["RTA_S"][foot][s["name"]][0]))
    return b / n


SPA = {}
rows = [("C3_one_noedge", ("one", None, False))] + [(m, ("one", m, False)) for m in MODES]
for foot in FOOTS:
    SPA[foot] = {}
    for k, mode in rows:
        a3 = {kind: sparc_a3(kind, foot, mode) for kind in ("spiral", "dwarf")}
        rm, _, npt = sparc_rms_sw(foot, mode)
        SPA[foot][k] = dict(A3_spiral=a3["spiral"][0], A3_dwarf=a3["dwarf"][0], maxdv_spiral=a3["spiral"][1], maxdv_dwarf=a3["dwarf"][1],
                            n_spiral=a3["spiral"][2], n_dwarf=a3["dwarf"][2], drms=rm - RMS0[foot], rotmod_points=npt,
                            frac_RHI_beyond_edge_spiral=None if mode[1] is None else frac_beyond("spiral", foot, mode[1]),
                            frac_RHI_beyond_edge_dwarf=None if mode[1] is None else frac_beyond("dwarf", foot, mode[1]))
    P(f"\n  [{foot}] row            | A3 spiral  A3 dwarf | max|dv| sp / dw | d rms    | R_HI beyond edge: sp / dw")
    for k, r_ in SPA[foot].items():
        fb = "-" if r_["frac_RHI_beyond_edge_spiral"] is None else f"{r_['frac_RHI_beyond_edge_spiral']:.3f} / {r_['frac_RHI_beyond_edge_dwarf']:.3f}"
        P(f"    {k:15s}| {r_['A3_spiral']:8.3f} {r_['A3_dwarf']:9.3f} | {r_['maxdv_spiral']:.4f} / {r_['maxdv_dwarf']:.4f} | {r_['drms']:+.5f} | {fb}")
c39 = json.load(open(os.path.join(LANES, "CFG39_harness_with_rule_results.json")))["numbers"]["sparc"]
k6 = all(SPA[f]["C3_one_noedge"]["A3_spiral"] == 1.0 and SPA[f]["C3_one_noedge"]["A3_dwarf"] == 1.0 and abs(SPA[f]["C3_one_noedge"]["drms"]) < 1e-12
         for f in FOOTS) and abs(RMS0["canonical"] - c39["rms0"]) < 1e-9
check("K6 SPARC harness: m = 1, no edge leaves A3 = 100% and d rms = 0; rms0 equals CFG39's", k6, f"rms0 {RMS0['canonical']:.9f} vs CFG39 {c39['rms0']:.9f}")
OUTR = {}
for m in MODES:
    ok = all(SPA[f][m]["A3_spiral"] >= 0.90 and SPA[f][m]["A3_dwarf"] >= 0.90 and abs(SPA[f][m]["drms"]) < 0.005 for f in FOOTS)
    fr = np.array(FRL.get(m, [np.nan]))
    OUTR[m] = dict(c_pass=ok, fret_min=float(np.min(fr)), fret_median=float(np.median(fr)), fret_max=float(np.max(fr)),
                   **{f: SPA[f][m] for f in FOOTS})
    P(f"  => {m}: (c) {'PASS' if ok else 'FAIL'}  (f_ret over rows {OUTR[m]['fret_min']:.3f}-{OUTR[m]['fret_max']:.3f}, median {OUTR[m]['fret_median']:.3f})")
RES["rows"] = OUTR
RES["control_row"] = {f: SPA[f]["C3_one_noedge"] for f in FOOTS}
if MUTATE:
    d1 = abs(SPA["alt"]["one"]["A3_dwarf"] - 0.864)
    check("M1 (SPARC) f_ret = 1 reproduces CFG487's alt-dwarf A3 0.864 within 0.01", d1 <= 0.01,
          f"alt dwarfs {SPA['alt']['one']['A3_dwarf']:.3f}, canonical {SPA['canonical']['one']['A3_dwarf']:.3f} (CFG487 0.945)")
RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nlb = sum(1 for c_ in CHK.values() if c_["load_bearing"] and not c_["ok"])
P(f"\n{sum(c_['ok'] for c_ in CHK.values())}/{len(CHK)} checks pass; load-bearing failures {nlb}; elapsed {RES['elapsed_s']} s")
json.dump(C4.jclean(RES), open(os.path.join(HERE, f"cfg515_sparc_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg515_sparc{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nlb else 0)
