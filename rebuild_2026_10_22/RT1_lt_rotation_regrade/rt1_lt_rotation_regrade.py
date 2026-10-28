#!/usr/bin/env python3
"""RT1_lt_rotation_regrade: IC 1613 (and the other LG LITTLE THINGS dwarfs) under the law, graded on HI rotation at R_max.
Frozen criteria ac267e8bf1 (committed alone, before any Table 2 number was read). Data: Oh+2015 (arXiv:1502.01281) source ms.tex,
Table 2, parsed directly (untracked under _external_data/little_things_oh2015/src; tarball sha256 recorded).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, not a particle; not theory closed;
nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 python3 -I rt1_lt_rotation_regrade.py      (RT1_MUTATE=1 twin)
"""
import os, sys, re, json, math, hashlib, resource
import numpy as np

MUT = os.environ.get("RT1_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(REPO, "_external_data", "little_things_oh2015", "src")
G, MSUN, KPC = 6.67430e-11, 1.98847e30, 3.0856775814913673e19
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FEET = ("canonical", "alt")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
nu = lambda y: 0.5 + math.sqrt(0.25 + 1.0 / y)
P(f"RT1_lt_rotation_regrade (criteria ac267e8bf1){'  [MUTATE: R_max read from the next column]' if MUT else ''}; kappa = 1/2 FITTED; not theory closed")
checks = {}
sha = hashlib.sha256(open(os.path.join(SRC, "e-print.tgz"), "rb").read()).hexdigest()
P(f"  K1 source tarball sha256 {sha}")
checks["K1"] = True

tex = open(os.path.join(SRC, "ms.tex")).read().split("\n")
i0 = next(i for i, l in enumerate(tex) if "label{MD_results_LT}" in l)
i1 = next(i for i in range(i0, len(tex)) if "end{tabular}" in tex[i])
NAMES = ["CVnIdwA", "DDO 43", "DDO 46", "DDO 47", "DDO 50", "DDO 52", "DDO 53", "DDO 70", "DDO 87", "DDO 101", "DDO 126", "DDO 133",
         "DDO 154", "DDO 168", "DDO 210", "DDO 216", "F564-V3", "IC 10", "IC 1613", "NGC 1569", "NGC 2366", "NGC 3738", "UGC 8508", "WLM",
         "Haro 29", "Haro 36"]
rows, buf, start = {}, "", None
for k in range(i0, i1):
    l = tex[k].split("%")[0]
    if start is None:
        nm = l.split("&")[0].strip()
        if nm in NAMES: start = k + 1; buf = ""
        else: continue
    buf += " " + l
    if "\\\\" in l:
        cells = [c.strip() for c in buf.replace("\\\\", "").split("&")]
        rows[cells[0]] = dict(cells=cells, line=start); start = None
checks["K0"] = sorted(rows) == sorted(NAMES)
P(f"  K0 parsed Table 2 rows: {len(rows)} of {len(NAMES)} names match: {'PASS' if checks['K0'] else 'FAIL'}")

def val(c):
    """first number and its +- error (if any) from a LaTeX cell; None for '...'"""
    c = c.replace("$", "").replace("\\pm", " pm ").replace("{", " ").replace("}", " ")
    nums = re.findall(r"-?\d+\.?\d*(?:[eE][-+]?\d+)?", c)
    if not nums or "..." in c.split("pm")[0]: return None, None
    v = float(nums[0]); e = float(nums[1]) if ("pm" in c and len(nums) > 1) else None
    return v, e

COL = dict(Rmax=1, V=3, VISO=4, Mgas=13, MKIN=14, MSED=15)
if MUT: COL["Rmax"] = 2
def rec(name):
    c = rows[name]["cells"]
    d = {k: val(c[j]) for k, j in COL.items()}
    return d, c
LG = {"IC 1613": "IC 1613", "WLM": "WLM", "DDO 210": "Aquarius", "DDO 216": "Pegasus dIrr"}

def E_rot(d, a0, mstar_key):
    R, _ = d["Rmax"]; V, eV = d["V"]; mg, _ = d["Mgas"]; ms, _ = d[mstar_key]
    if None in (R, V, mg, ms): return None
    Mb = (mg + ms) * 1e7
    gobs = (V * 1e3) ** 2 / (R * KPC); gN = G * Mb * MSUN / (R * KPC) ** 2
    E = math.log10(gobs) - math.log10(nu(gN / a0) * gN)
    sE = math.sqrt((2 * (eV or 0.0) / V / math.log(10)) ** 2 + (0.5 * 0.15) ** 2)
    return dict(E=E, sE=sE, Z=E / sE, logMb=math.log10(Mb), R=R, V=V, eV=eV, y=gN / a0)

k3 = True
RES = dict(criteria="ac267e8bf1", source_sha256=sha, mutate=MUT, lg={}, all26={}, verdict={})
P("\n  LG dwarfs, parsed Table 2 (line, R_max kpc, V_rot km/s, V_ISO, M_gas / M*_KIN / M*_SED in 1e7 Msun):")
for nm, alias in LG.items():
    d, c = rec(nm)
    P(f"   {nm:8s} ({alias}) line {rows[nm]['line']}: R_max {d['Rmax']}, V {d['V']}, V_ISO {d['VISO']}, M_gas {d['Mgas']}, M*_KIN {d['MKIN']}, M*_SED {d['MSED']}")
    if d["V"][0] is not None and d["VISO"][0] is not None: k3 &= d["V"][0] <= 3 * d["VISO"][0]
    if MUT: k3 &= d["Rmax"][0] is not None and d["Rmax"][0] <= 1.5 * float(val(c[1])[0]) and False if d["Rmax"][0] != val(c[1])[0] else k3
checks["K3"] = bool(k3)
for f in FEET:
    P(f"\n=== [{f}] a0 {A0[f]:.4e}")
    for nm, alias in LG.items():
        d, _ = rec(nm)
        for mk in ("MSED", "MKIN"):
            r = E_rot(d, A0[f], mk)
            RES["lg"].setdefault(f, {}).setdefault(nm, {})[mk] = r
            if r: P(f"  {nm:8s} [{mk}] log M_b {r['logMb']:.2f}, g_N/a0 {r['y']:.3f}: E_rot {r['E']:+.3f} +- {r['sE']:.3f}  Z {r['Z']:+.2f}")
            else: P(f"  {nm:8s} [{mk}] not computable (missing value)")
    es = [E_rot(rec(n)[0], A0[f], "MSED") for n in NAMES]
    es = [e["E"] for e in es if e]
    RES["all26"][f] = dict(n=len(es), median=float(np.median(es)), p16=float(np.percentile(es, 16)), p84=float(np.percentile(es, 84)))
    P(f"  context (not graded): all LITTLE THINGS with SED M*: N {len(es)}, median E_rot {np.median(es):+.3f} [16-84%: {np.percentile(es, 16):+.3f}, {np.percentile(es, 84):+.3f}]")
    ic = RES["lg"][f]["IC 1613"]["MSED"]
    v = "IC 1613 CONSISTENT ON ROTATION" if abs(ic["Z"]) < 2 else ("IC 1613 OVER-PREDICTED ON ROTATION" if ic["Z"] <= -2 else "IC 1613 UNDER-PREDICTED ON ROTATION")
    RES["verdict"][f] = v; P(f"  VERDICT [{f}]: {v} (E_rot {ic['E']:+.3f}, Z {ic['Z']:+.2f})")
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9; checks["K2"] = peak < 1.0
P(f"\n  K3 V_rot <= 3 V_ISO and R_max from its own column: {'PASS' if checks['K3'] else 'FAIL'};  K2 peak RSS {peak:.2f} GB")
RES["checks"] = checks
fn = os.path.join(HERE, f"rt1_lt_rotation_regrade_results{TAG}.json")
json.dump(RES, open(fn, "w"), indent=1, default=float)
P(f"checks {sum(checks.values())}/{len(checks)}; results sha256 {hashlib.sha256(open(fn, 'rb').read()).hexdigest()}")
open(os.path.join(HERE, f"rt1_lt_rotation_regrade{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(checks.values()) else 1)
