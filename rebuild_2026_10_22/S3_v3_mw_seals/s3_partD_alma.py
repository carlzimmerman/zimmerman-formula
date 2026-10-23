#!/usr/bin/env python3
"""S3_v3_mw_seals Part D: ALMA U4_27928 (2026-11-06) and GS4_24110 (2026-11-28) disc reading for v3 (tile 43).

Criteria FROZEN_CRITERIA.md §5 (8f6c6587e1) + A1, A2.  AG4e's algebraic n = 1 reading (CFG571's head with nu1) is reproduced by
my own implementation (D1); then the AQUAL-disc requirement (s3_alma.py): razor-thin Freeman stars (M*, R_d) + razor-thin
exponential gas (M_gas, R_g in {R_d, 1.5 R_d}) at the same radius, V_c and a0(z) branch ratios (read from SEALED_N1.json);
M_gas,req,AQ solves C(R; M_gas) nu1(g_N/a0) g_N = V_c^2/R with exact Bessel g_N, C iterated to |d log M_gas| <= 0.002.
FLOOR if stars alone give AQUAL V_c >= V_c.  Variant (reported): both discs sech^2 with z0 = 0.15 R_d.  Isolated (no
external-field estimate for these discs on disk); unscreened (l_g computed).  Every AQUAL cell runs in a short-lived child
process (RSS hygiene).  Writes SEALED_V3_ALMA_AQUAL.json + ALMA_V3_HASH.txt (never under MUTATE or with a failed check).
Run: OMP_NUM_THREADS=1 nice -n 15 python3 s3_partD_alma.py [--mutate]
kappa = 1/2 FITTED; footings never pooled; cold energy's mass still required; one disc excludes no model; not theory closed.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, time, hashlib, resource
import numpy as np
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import s3_aqual as S
import s3_alma as A

REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TAG = S.TAG
OUT, CHECKS = [], []
T0 = time.time()


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); OUT.append(s)


def check(name, ok, detail=""):
    CHECKS.append(dict(name=name, ok=bool(ok), detail=detail))
    P(f"{name} {'PASS' if ok else 'FAIL'} {detail}")
    return bool(ok)


P("=" * 112)
P(f"S3 Part D: ALMA U4_27928 / GS4_24110 under v3 (AQUAL discs) {'*** MUTATE: mu == 1 ***' if S.MUTATE else ''}")
P("kappa = 1/2 FITTED; footings never pooled; one disc excludes no model; not theory closed")
P("=" * 112)
SEALF = os.path.join(REPO, "argon_push", "AG4e_n1_alma_seal", "SEALED_N1.json")
SEAL = json.load(open(SEALF))
sha_n1 = hashlib.sha256(open(SEALF, "rb").read()).hexdigest()
P(f"  SEALED_N1.json sha256 {sha_n1} (AG4e's PREDICTIONS_HASH: 9802de0d...; read only)")
BR = list(SEAL["ratios"].keys())
FOOT = A.FOOT

z4 = 1.41933
dc = 2.99792458e5 / 70.0 * quad(lambda x: 1 / math.sqrt(0.3 * (1 + x) ** 3 + 0.7), 0, z4)[0] * 1e3
Re4 = 0.49 / 206264.806 * dc / (1 + z4)
TARGETS = {}
for lm in ("10.89", "10.76"):
    TARGETS[("GS4_24110", lm)] = dict(R=7.39, Rd=7.39 / 1.678, Mstar=10 ** float(lm), z="1.997", Vcs={"206": 206.0})
VCS = (150, 175, 200, 225, 250, 275, 300)
TARGETS[("U4_27928", "10.74")] = dict(R=2 * Re4, Rd=Re4 / 1.678, Mstar=10 ** 10.74, z="1.41933", Vcs={str(v): float(v) for v in VCS})
P(f"  GS4: R 7.39 kpc, R_d {7.39 / 1.678:.4f}; U4: R_e {Re4:.4f} kpc, R = 2 R_e = {2 * Re4:.4f}, R_d {Re4 / 1.678:.4f}")

# ------------------------------------------------------------------ D1
P("\n--- D1: my algebraic nu1 implementation vs SEALED_N1.json")
w, nfl, ncmp = 0.0, 0, 0
for (tgt, lm), T in TARGETS.items():
    for vk, Vc in T["Vcs"].items():
        for fn, a00 in FOOT.items():
            for m in BR:
                a0 = a00 * SEAL["ratios"][m][T["z"]]
                d = A.alg_cell(T["R"], Vc, T["Mstar"], T["Rd"], a0)
                ref = SEAL[tgt][lm if tgt == "GS4_24110" else vk][f"{fn}|{m}"]
                w = max(w, abs(d["logVbar2R_G"] - ref["logVbar2R_G"])); ncmp += 1
                nfl += int(d["floor"] != (ref["floor"] == "True"))
                for gs in ("Rg=Rd", "Rg=1.5Rd"):
                    a, b = d["logMgas_" + gs], ref["logMgas_" + gs]
                    if (a is None) != (b is None):
                        nfl += 1
                    elif a is not None:
                        w = max(w, abs(a - b))
check("D1", w <= 1e-6 and nfl == 0, f"{ncmp} cells: max |d log| {w:.1e} dex (tol 1e-6); FLOOR mismatches {nfl}")

# ------------------------------------------------------------------ D2, D3
P("\n--- D2 / D3 grid controls (child processes)")
ctrl, cpk = S.run_batch("s3_alma", "job_controls", [dict(Rd=7.39 / 1.678), dict(Rd=Re4 / 1.678)], batch=1)
d2 = max(c["d2"] for c in ctrl); d3 = max(c["d3"] for c in ctrl)
P(f"  grids {[(c['nR'], c['nz']) for c in ctrl]}; child peak RSS {cpk:.0f} MB")
check("D2", d2 <= 0.003, f"razor-thin Freeman on the ALMA grid max |dV2/V2| {d2:.4f} on 0.5-5 R_d (tol 0.003)")
check("D3", d3 <= 0.005, f"Kuzmin AQUAL identity (A1 form) on the ALMA grid max |d| {d3:.4f} (tol 0.005)")
RSSD = dict(controls=cpk)


def cached(func, jobs, name, batch):
    key = hashlib.sha1((name + TAG + json.dumps(jobs, sort_keys=True)).encode()).hexdigest()[:16]
    fn = os.path.join(S.CACHE, f"alma_{name}_{key}.json")
    if os.path.exists(fn):
        d = json.load(open(fn)); return d["res"], d["peak"]
    res, peak = S.run_batch("s3_alma", func, jobs, batch=batch)
    json.dump(dict(res=res, peak=peak), open(fn, "w"))
    return res, peak

# ------------------------------------------------------------------ the AQUAL-disc requirement
P("\n--- AQUAL-disc requirement (razor-thin primary) vs AG4e (algebraic nu1); every cell in a child process")
jobs, keys = [], []
for (tgt, lm), T in TARGETS.items():
    for vk, Vc in T["Vcs"].items():
        ck = lm if tgt == "GS4_24110" else vk
        for fn, a00 in FOOT.items():
            for m in BR:
                a0 = a00 * SEAL["ratios"][m][T["z"]]
                al = A.alg_cell(T["R"], Vc, T["Mstar"], T["Rd"], a0)
                jobs.append(dict(Rd=T["Rd"], R=T["R"], Vc=Vc, Mstar=T["Mstar"], a0_si=a0, alg=al))
                keys.append((tgt, ck, f"{fn}|{m}", al))
res, cpk = cached("job_cell", jobs, "cells", 2)
RSSD["cells"] = cpk
P(f"  {len(jobs)} cells done in {time.time() - T0:.0f} s; child peak RSS {cpk:.0f} MB")
RES = dict(lane="S3_v3_mw_seals", part="D", mutate=S.MUTATE, criteria="8f6c6587e1", amendments=["A1 0501ac4248", "A2 938675e060"],
           sealed_n1_sha256=sha_n1, cells={}, thick={}, decision={})
SEALOBJ = {"law": "v3 static limit: AQUAL div[mu grad Phi] = 4 pi G rho_b, mu = x/(1+x) (nu1 in spherical symmetry)",
           "geometry": "razor-thin Freeman stars + razor-thin exponential gas (R_g = R_d, 1.5 R_d); isolated; unscreened",
           "code": "rebuild_2026_10_22/S3_v3_mw_seals/s3_partD_alma.py + s3_alma.py + s3_aqual.py",
           "ratios": SEAL["ratios"], "GS4_24110": {}, "U4_27928": {}}
maxdV, maxdM, flips, worst_conv = 0.0, 0.0, 0, 0.0
f = lambda x: "FLOOR" if x is None else f"{x:6.3f}"
for (tgt, ck, kk, al), aq in zip(keys, res):
    dV = aq["logVbar2R_G"] - al["logVbar2R_G"]
    dM = {gs: (aq["logMgas_" + gs] - al["logMgas_" + gs]) if (aq["logMgas_" + gs] is not None and al["logMgas_" + gs] is not None) else None
          for gs in ("Rg=Rd", "Rg=1.5Rd")}
    flip = aq["floor"] != al["floor"] or any((aq["logMgas_" + gs] is None) != (al["logMgas_" + gs] is None) for gs in ("Rg=Rd", "Rg=1.5Rd"))
    flips += int(flip)
    if not al["floor"]:
        maxdV = max(maxdV, abs(dV))
    for v in dM.values():
        if v is not None:
            maxdM = max(maxdM, abs(v))
    for gs, h in aq["iters"].items():
        if len(h) > 1:
            worst_conv = max(worst_conv, abs(h[-1] - h[-2]))
    RES["cells"][f"{tgt}|{ck}|{kk}"] = dict(alg=al, aqual=aq, dlogVbar2=dV, dlogMgas=dM, floor_flip=flip)
    SEALOBJ[tgt].setdefault(ck, {})[kk] = {"floor": aq["floor"], "logVbar2R_G": aq["logVbar2R_G"],
                                           "logVbar2R_G_Rg=1.5Rd": aq.get("logVbar2R_G_Rg=1.5Rd", aq["logVbar2R_G"]),
                                           "logMgas_Rg=Rd": aq["logMgas_Rg=Rd"], "logMgas_Rg=1.5Rd": aq["logMgas_Rg=1.5Rd"],
                                           "C_stars": aq["C_stars"], "C_final": aq["C_final"]}
    P(f"  {tgt} {ck:>5} {kk:<30} alg Mgas {f(al['logMgas_Rg=Rd'])}/{f(al['logMgas_Rg=1.5Rd'])}  AQUAL {f(aq['logMgas_Rg=Rd'])}/{f(aq['logMgas_Rg=1.5Rd'])}"
      f"  dlogVbar2 {dV:+.4f}  C* {aq['C_stars']:.4f}{'  FLOOR FLIP' if flip else ''}")
check("D4", worst_conv <= 0.002, f"requirement iterations converged: max last step {worst_conv:.4f} dex (tol 0.002)")
check("D6", maxdM <= 0.3 and maxdV <= 0.3, f"(frozen; AMENDMENT A5: mis-specified near FLOOR) AQUAL requirement within 0.3 dex of the algebraic nu1 one: max |d log Mgas| {maxdM:.3f}, |d log Vbar2| {maxdV:.3f}")
check("D6p", maxdV <= 0.3, f"(AMENDMENT A5) |d log Vbar2,req| <= 0.3 dex on every non-FLOOR cell: max {maxdV:.4f}")
PER = {}
for (tgt, ck, kk, al), aq in zip(keys, res):
    t = tgt if tgt == "U4_27928" else f"{tgt}|{ck}"
    c = RES["cells"][f"{tgt}|{ck}|{kk}"]
    m = PER.setdefault(t, dict(max_dV=0.0, max_dM=0.0, flips=0))
    if not al["floor"]:
        m["max_dV"] = max(m["max_dV"], abs(c["dlogVbar2"]))
    for v in c["dlogMgas"].values():
        if v is not None:
            m["max_dM"] = max(m["max_dM"], abs(v))
    m["flips"] += int(c["floor_flip"])
for t, m in PER.items():
    m["label"] = "AG4e IS v3's reading" if (m["max_dV"] <= 0.01 and m["max_dM"] <= 0.03 and m["flips"] == 0) else "needs addendum F"
    P(f"  per release (A5): {t}: max |dlogVbar2| {m['max_dV']:.4f}, max |dlogMgas| {m['max_dM']:.4f}, FLOOR flips {m['flips']} -> {m['label']}")
RES["per_release"] = PER

# D5 grid refinement on a representative cell
T = TARGETS[("GS4_24110", "10.76")]
a0 = FOOT["canon 9.36e-11"] * SEAL["ratios"]["F-flat"]["1.997"]
al = A.alg_cell(T["R"], 206.0, T["Mstar"], T["Rd"], a0)
(r1, r2), cpk = S.run_batch("s3_alma", "job_cell", [dict(Rd=T["Rd"], R=T["R"], Vc=206.0, Mstar=T["Mstar"], a0_si=a0, alg=al),
                                                    dict(Rd=T["Rd"], R=T["R"], Vc=206.0, Mstar=T["Mstar"], a0_si=a0, alg=al, fine=True)], batch=1)
RSSD["D5"] = cpk
d5 = abs(r1["logMgas_Rg=Rd"] - r2["logMgas_Rg=Rd"]) if (r1["logMgas_Rg=Rd"] is not None and r2["logMgas_Rg=Rd"] is not None) else float("nan")
check("D5", d5 <= 0.005, f"GS4 10.76 canonical F-flat Rg=Rd: log Mgas,req,AQ main {r1['logMgas_Rg=Rd']} fine {r2['logMgas_Rg=Rd']} |d| {d5:.4f} (tol 0.005)")

# thick variant (reported only)
P("\n--- variant (reported only): both discs sech^2 with z0 = 0.15 R_d")
jobs, keys = [], []
for (tgt, lm), T in TARGETS.items():
    for vk, Vc in T["Vcs"].items():
        if tgt == "U4_27928" and vk not in ("200", "250"):
            continue
        ck = lm if tgt == "GS4_24110" else vk
        for fn, a00 in FOOT.items():
            for m in ("F-flat", "F-DESI", "E"):
                a0 = a00 * SEAL["ratios"][m][T["z"]]
                al = A.alg_cell(T["R"], Vc, T["Mstar"], T["Rd"], a0)
                jobs.append(dict(Rd=T["Rd"], R=T["R"], Vc=Vc, Mstar=T["Mstar"], a0_si=a0, alg=al, thick=0.15))
                keys.append((f"{tgt}|{ck}|{fn}|{m}", al))
res, cpk = cached("job_cell", jobs, "thick", 2)
RSSD["thick"] = cpk
for (k, al), aq in zip(keys, res):
    RES["thick"][k] = dict(alg=al, aqual=aq)
    P(f"  {k:<44} alg {f(al['logMgas_Rg=Rd'])}  AQUAL-thick {f(aq['logMgas_Rg=Rd'])}  C* {aq['C_stars']:.4f}")

# screening
rMs = {k: math.sqrt(A.Gk * T["Mstar"] / (FOOT["canon 9.36e-11"] / A.U)) for k, T in TARGETS.items()}
RES["screening_l_g_pc"] = {f"{k[0]}|{k[1]}": {str(L): (L ** 2) / (2 * r * 1e3) for L in (21.7, 22.9, 24.0, 90.0)} for k, r in rMs.items()}
P(f"\n  screening: l_g = L*^2/(2 r_M) <= {max(max(v.values()) for v in RES['screening_l_g_pc'].values()):.3f} pc (stars-only r_M, canonical) -> unscreened at R ~ 7-8 kpc")

# ------------------------------------------------------------------ decision (frozen §5)
is_ag4e = (maxdV <= 0.01 and maxdM <= 0.03 and flips == 0)
dec = "AG4e IS v3's ALMA reading" if is_ag4e else "v3 NEEDS ADDENDUM F"
RES["decision"] = dict(max_abs_dlogVbar2_nonfloor=maxdV, max_abs_dlogMgas=maxdM, floor_flips=flips, label=dec)
P(f"\nDECISION (frozen: |dlogVbar2| <= 0.01, |dlogMgas| <= 0.03, no FLOOR flip): max |dlogVbar2| {maxdV:.4f}, max |dlogMgas| {maxdM:.4f}, flips {flips} -> {dec}")
RES["checks"] = CHECKS
npass = sum(c["ok"] for c in CHECKS)
RES["runtime_s"] = round(time.time() - T0, 1)
RES["peak_rss_MB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6, 1)
RES["child_rss_MB"] = RSSD
seal_ok = all(c["ok"] for c in CHECKS if c["name"] in ("D1", "D2", "D3", "D4", "D5", "D6p"))
HASHF = os.path.join(HERE, "ALMA_V3_HASH.txt")
if not S.MUTATE and seal_ok and os.path.exists(HASHF):
    blob = json.dumps(SEALOBJ, sort_keys=True, default=str).encode()
    sha = hashlib.sha256(blob).hexdigest(); ref = open(HASHF).read().split()[0]
    RES["sealed_sha256"] = ref; RES["recomputed_sha256"] = sha
    P(f"seal exists (never overwritten): recomputed hash {sha} {'EQUALS' if ref == sha else 'DIFFERS FROM'} the sealed {ref}")
elif not S.MUTATE and seal_ok:
    blob = json.dumps(SEALOBJ, sort_keys=True, default=str).encode()
    sha = hashlib.sha256(blob).hexdigest()
    open(os.path.join(HERE, "SEALED_V3_ALMA_AQUAL.json"), "wb").write(blob)
    open(os.path.join(HERE, "ALMA_V3_HASH.txt"), "w").write(f"{sha}  SEALED_V3_ALMA_AQUAL.json\n")
    RES["sealed_sha256"] = sha
    P(f"SEALED_V3_ALMA_AQUAL.json sha256 = {sha}")
else:
    P("nothing sealed (MUTATE or a failed D1-D5 / D6p check)")
json.dump(RES, open(os.path.join(HERE, f"s3_partD_alma_results{TAG}.json"), "w"), indent=1, default=str)
P(f"\nS3_PARTD COMPLETE: {npass}/{len(CHECKS)} checks PASS.  runtime {RES['runtime_s']} s, parent peak RSS {RES['peak_rss_MB']} MB, "
  f"child peaks {RSSD}")
open(os.path.join(HERE, f"s3_partD_alma{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(CHECKS) else 1)
