"""CFG784 -- fossil free cold energy in dwarfs, gated by CFG782's selector.  Criteria: FROZEN_CRITERIA.md (cfbde092f).
Runs only if CFG782's verdict is SELECTOR VIABLE / BORDERLINE (read from cfg782_results.json).  AUDIT_UFD harness exec'd
read-only (its sections 1-2: data, estimators, KM median); nothing of it is re-written.
Run: python3 cfg784.py   (CFG784_MUTATE=M1 shuffle R_ind among UFDs; =M2 selector off).  Seconds.
kappa = 1/2 FITTED; cold energy mass required; in UFDs this is behaviourally a cold halo of native mass; not theory closed.
"""
import csv
import io
import json
import math
import os
import sys
import contextlib

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
MODE = os.environ.get("CFG784_MUTATE", "")
OUT = []


def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))


v782 = json.load(open(os.path.join(LANES, "CFG782_unbinding_selector", "cfg782_results.json"))).get("verdict", "")
if not (v782.startswith("SELECTOR VIABLE") or v782.startswith("BORDERLINE")):
    P(f"CFG784 NOT RUN: CFG782 verdict '{v782}' (selector dead) - recorded per the frozen conditional")
    open(os.path.join(HERE, "cfg784.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0)

src_path = os.path.join(LANES, "AUDIT_UFD_2026-10-03", "audit_ufd.py")
src = open(src_path).read()
cut = src.index('P("\\n3. VARIANTS')
A = {"__file__": src_path, "__name__": "audit_ufd_head"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:cut], src_path, "exec"), A)
RES, UL, sigma_pred, km_median, boot, fnum = A["RES"], A["UL"], A["sigma_pred"], A["km_median"], A["boot"], A["fnum"]
G, MSUN, PC = A["G"], A["MSUN"], A["PC"]
A0 = A["A0"]

j317 = json.load(open(os.path.join(LANES, "CFG317_baryon_loss_cold_mass", "cfg317_baryon_loss_results.json")))["numbers"]
EST, NAMES = j317["EST"], j317["NAMES"]
KB, MP = 1.380649e-23, 1.6726e-27
VTH = math.sqrt(2) * math.sqrt(KB * 1.5e4 / (0.59 * MP)) / 1e3            # CFG782 primary, 20.49 km/s
rhoc0 = 3 * (70e3 / 3.0857e22) ** 2 / (8 * math.pi * G)
FB, ZF = 0.157, 8.0


def rf_of(Mcoll, zf=ZF):
    rho = 0.308 * rhoc0 * (1 + zf) ** 3
    return (3 * Mcoll * MSUN / (4 * math.pi * 18 * math.pi ** 2 * rho)) ** (1 / 3)


def sudden(Mb, lR, a0=9.3603e-11):
    if MODE == "M2":
        return True
    return (G * Mb * MSUN * 10 ** max(lR, 0.0) * a0) ** 0.25 / 1e3 < VTH


def sig_pred(d, foot, lR, Mb):
    s_law = sigma_pred(d, foot)
    if lR is None or not sudden(Mb, lR):
        return s_law
    R = 10 ** max(lR, 0.0)
    Mfree = 5.364 * (R - 1) * Mb
    rf = rf_of(R * Mb / FB)
    r = (4.0 / 3.0) * d["rh"] * PC
    s2 = G * Mfree * MSUN * min(r / rf, 1.0) / (3 * r)
    return math.sqrt((s_law * 1e3) ** 2 + s2) / 1e3


def lR_map(key, yv="-0.2"):
    return {nm: (None if e is None else e.get("lR")) for nm, e in zip(NAMES[key], EST[f"{yv}|{key}"])}


P(f"CFG784  fossil free cold energy (selector CFG782: {v782})" + (f"  [MUTATE {MODE}]" if MODE else ""))
P(f"  K2: r_f(M_coll 1e7 Msun, z_f 8) = {rf_of(1e7) / PC:.0f} pc")
RESULTS = {"lane": "CFG784", "mode": MODE, "selector": v782}
for yv in ("-0.2", "-0.5", "0.1"):
    mU = lR_map("ufd", yv)
    ulL = [(None if e is None else e.get("lR")) for e in EST[f"{yv}|ul"]]
    if MODE == "M1":
        vals = [v for v in mU.values() if v is not None]
        perm = np.random.default_rng(784).permutation(len(vals))
        it = iter(np.array(vals)[perm])
        mU = {k: (next(it) if v is not None else None) for k, v in mU.items()}
    for foot in A0:
        x = np.array([math.log10(d["sig"] / sig_pred(d, foot, mU.get(d["name"]), 2.0 * d["LV"] + 1.33 * d["MHI"])) for d in RES])
        xu = np.array([math.log10(d["sig_ul"] / sig_pred(d, foot, lr, 2.0 * d["LV"] + 1.33 * d["MHI"])) for d, lr in zip(UL, ulL)])
        m = km_median(x, xu); e = boot(x, xu)
        RESULTS[f"UFD|{yv}|{foot}"] = dict(km=m, boot=e)
        if yv == "-0.2" or foot == "canonical":
            P(f"  UFD yield {yv} {foot}: KM median {m:+.3f} (boot {e:.3f})")
# K1: M_free = 0 (all lR None) reproduces the audit baseline
x0 = np.array([math.log10(d["sig"] / sigma_pred(d, "canonical")) for d in RES]); xu0 = np.array([math.log10(d["sig_ul"] / sigma_pred(d, "canonical")) for d in UL])
k1 = abs(km_median(x0, xu0) - 0.3245) < 1e-3
P(f"  K1 baseline (no free mass) {km_median(x0, xu0):+.4f} vs AUDIT +0.3245: {'PASS' if k1 else 'FAIL'}")


def lvd_rows(fname):
    out = []
    for r in csv.DictReader(open(os.path.join(A["DATA"], fname))):
        MV = fnum(r.get("M_V")); sig = fnum(r.get("vlos_sigma")); rh = fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical"))
        if MV is None or sig is None or rh is None:
            continue
        mhi = fnum(r.get("mass_HI"))
        out.append(dict(name=r["name"], LV=10 ** (0.4 * (4.83 - MV)), rh=rh, rh_maj=rh, MHI=(10 ** mhi if mhi else 0.0), sig=sig, MV=MV))
    return out


for lab, fname, key, cut in (("MW classicals", "lvd_dwarf_mw.csv", "cls", lambda d: d["MV"] <= -7.7), ("LV field", "lvd_dwarf_local_field.csv", "fld", lambda d: True)):
    mp = lR_map(key)
    rows = [d for d in lvd_rows(fname) if cut(d) and d["name"] in mp and mp[d["name"]] is not None]
    for foot in A0:
        x_law = np.array([math.log10(d["sig"] / sigma_pred(d, foot)) for d in rows])
        x_new = np.array([math.log10(d["sig"] / sig_pred(d, foot, mp[d["name"]], 2.0 * d["LV"] + 1.33 * d["MHI"])) for d in rows])
        if len(x_new) == 0:
            continue
        e = float(np.std([np.median(x_new[np.random.default_rng(42 + k).integers(0, len(x_new), len(x_new))]) for k in range(1000)]))
        z = float(np.median(x_new)) / max(math.hypot(e, 0.077), 1e-9)
        nflag = sum(sudden(2.0 * d["LV"] + 1.33 * d["MHI"], mp[d["name"]]) for d in rows)
        RESULTS[f"{lab}|{foot}"] = dict(n=len(rows), flagged=int(nflag), med_law=float(np.median(x_law)), med_new=float(np.median(x_new)), z=z)
        P(f"  {lab} {foot}: n {len(rows)}, flagged SUDDEN {nflag}; median {np.median(x_law):+.3f} -> {np.median(x_new):+.3f} (z {z:+.2f})")

u = RESULTS["UFD|-0.2|canonical"]
zU = u["km"] / math.hypot(u["boot"], 0.077)
pU = abs(zU) < 2
pS = abs(RESULTS.get("MW classicals|canonical", {}).get("z", 99)) < 2
pF = abs(RESULTS.get("LV field|canonical", {}).get("z", 99)) < 2
V = "SOLVES" if (pU and pS and pF) else ("PARTIAL" if pU and (pS + pF) == 1 else "FAIL")
P(f"\n  P-UFD z {zU:+.2f} {pU}; P-SAT {pS}; P-FIELD {pF} -> {V if not MODE else '(mutate)'}")
RESULTS.update(verdict=V, K1=bool(k1))
json.dump(RESULTS, open(os.path.join(HERE, f"cfg784_results{'_MUTATE_' + MODE if MODE else ''}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg784{'_MUTATE_' + MODE if MODE else ''}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if MODE else 0)
