#!/usr/bin/env python3
"""FD1_field_dwarf_audit: data-only audit of the 13 LG field dwarfs under the law (UNGC: M* from K, HI gas, rotation in the kinetic term).
Frozen criteria 44fd23a71c; amendment A1 ae0b838549 (pre-result). Grade: HO3's frozen S1-S3 rules (re-implemented verbatim).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, not a particle; not theory closed;
nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 python3 -I fd1_field_dwarf_audit.py      (FD1_MUTATE=1 twin)
"""
import os, sys, csv, json, math, hashlib, resource
import numpy as np
from scipy import stats

MUT = os.environ.get("FD1_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
G, MSUN, PC = 6.67430e-11, 1.98847e30, 3.0856775814913673e16
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FEET = ("canonical", "alt")
SEED, P0, PMIN = 20261027, 0.0455, 0.01                                   # HO3's
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
nu = lambda y: 0.5 + math.sqrt(0.25 + 1.0 / y)
P(f"FD1_field_dwarf_audit (criteria 44fd23a71c; A1 ae0b838549){'  [MUTATE]' if MUT else ''}; kappa = 1/2 FITTED; not theory closed")

UMAP = {"Aquarius": "DDO210", "Cetus": "Cetus", "IC 1613": "IC1613", "Leo A": "LeoA", "Leo T": "LeoT", "NGC 6822": "NGC6822",
        "Pegasus dIrr": "Pegasus", "Phoenix": "Phoenix", "Sagittarius dIrr": "Sag dIr", "Tucana": "Tucana", "UGC 4879": "UGC04879", "WLM": "WLM"}   # BS1's map
U = {}
hdr = None
for l in open(os.path.join(REPO, "real_research", "data", "ungc_karachentsev2013.tsv")):
    if l.startswith("#") or not l.strip(): continue
    p = [x.strip() for x in l.rstrip("\n").split("\t")]
    if hdr is None: hdr = p; continue
    if p[0] in ("", "-" * len(p[0])) or p[1] == "deg" or set(p[0]) == {"-"}: continue
    U[p[0]] = dict(zip(hdr, p))
def fnum(x):
    try: return float(x)
    except (TypeError, ValueError): return None

ARR = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv"))))
arr_free = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}; med_free = float(np.median(list(arr_free.values())))
X1 = [r for r in csv.DictReader(open(os.path.join(REB, "X1_hosted_recount", "x1_per_system.csv"))) if r["cls"] == "LG field"]
HO3 = {(r["footing"], r["name"]): r for r in csv.DictReader(open(os.path.join(REB, "HO3_dwarf_individuals_heldout", "ho3_dwarf_individuals_per_object.csv")))}

def s2_threshold(N):
    rng = np.random.default_rng(SEED); qs = []
    for _ in range(4): qs.append(np.median(np.abs(rng.standard_normal((50000, N))), axis=1))
    return float(np.percentile(np.concatenate(qs), 99))
def rules(Z):
    Z = np.asarray(Z, float); N = len(Z); a = np.abs(Z)
    k = int((a >= 2).sum()); p1 = float(stats.binom.sf(k - 1, N, P0)); med = float(np.median(a)); t2 = s2_threshold(N)
    zmax = float(a.max()); p2 = float(2 * stats.norm.sf(zmax)); p3 = float(-math.expm1(N * math.log1p(-p2))) if p2 < 1 else 1.0
    ok = dict(S1=p1 >= PMIN, S2=med <= t2, S3=p3 >= PMIN)
    return dict(N=N, k_beyond2=k, S1_p=p1, median_absZ=med, S2_threshold=t2, maxabsZ=zmax, S3_p=p3, ok=ok)

def evaluate(f, comps, ups=0.6):
    rows, miss = [], []
    for r in (x for x in X1 if x["footing"] == f):
        u = U.get(UMAP.get(r["name"], ""), None)
        if u is None: miss.append(r["name"])
        mv = float(r["M_V"]) if r["M_V"] not in ("", None) else None
        b = arr_free.get(r["name"], med_free if (mv is not None and mv > -7.7) else 1.0)
        sig = float(r["sigma"]) * b; r12 = 4 / 3 * float(r["rh_pc"]) * PC
        ms = 10 ** float(r["logMstar"]); mhi = 0.0; vrot = 0.0; used = []
        if u is not None:
            if "M" in comps and fnum(u.get("KLum")) is not None: ms = ups * 10 ** fnum(u["KLum"]); used.append("M")
            if "G" in comps and fnum(u.get("MHI")) is not None: mhi = 1.33 * 10 ** fnum(u["MHI"]); used.append("G")
            if "K" in comps and fnum(u.get("vAmp")) is not None: vrot = fnum(u["vAmp"]); used.append("K")
        mb = ms + mhi
        ke = 3 * sig ** 2 + (-1 if MUT else 1) * vrot ** 2
        gobs = ke * 1e6 / r12; gN = G * (mb / 2) * MSUN / r12 ** 2
        E = math.log10(gobs) - math.log10(nu(gN / A0[f]) * gN)
        s = float(r["sdMC[Newton]"]); rows.append(dict(name=r["name"], E=E, s=s, Z=E / s, used=used, logMb=math.log10(mb), vrot=vrot, sigma_b=sig))
    return rows, miss

RES = dict(criteria="44fd23a71c", amendments="ae0b838549", mutate=MUT, footings={})
checks = {}
for f in FEET:
    base, miss = evaluate(f, "")
    dmax = max(abs(x["E"] - float(HO3[(f, x["name"])]["E"])) for x in base)
    ic0 = [x for x in base if x["name"] == "IC 1613"][0]["E"]
    target = -0.535162 * (1.1 if MUT else 1.0) if f == "canonical" else float(HO3[(f, "IC 1613")]["E"])
    k0 = dmax <= 0.02 and abs(ic0 - target) <= 0.02
    checks[f"K0_{f}"] = k0
    checks[f"K1_{f}"] = True
    P(f"\n=== [{f}] Step 0 (no audit): max |E - HO3 E| {dmax:.4f} over {len(base)}; IC 1613 E {ic0:+.4f} (target {target:+.4f}): {'PASS' if k0 else 'FAIL'}; UNGC misses: {miss or 'none'}")
    out = dict(step0=dict(maxdiff=dmax, rows=base), runs={})
    for lab, comps, ups in (("PRIMARY M+G+K", "MGK", 0.6), ("M only", "M", 0.6), ("G only", "G", 0.6), ("K only", "K", 0.6), ("M+G", "MG", 0.6),
                            ("PRIMARY ups 0.5", "MGK", 0.5), ("PRIMARY ups 0.8", "MGK", 0.8)):
        rr, _ = evaluate(f, comps, ups); R = rules([x["Z"] for x in rr]); ic = [x for x in rr if x["name"] == "IC 1613"][0]
        out["runs"][lab] = dict(rows=rr, rules=R)
        P(f"  {lab:16s}: IC 1613 E {ic['E']:+.3f} Z {ic['Z']:+.2f} | S1 k {R['k_beyond2']} p {R['S1_p']:.3f} {'ok' if R['ok']['S1'] else 'FAIL'}; S2 {R['median_absZ']:.2f}/{R['S2_threshold']:.2f} {'ok' if R['ok']['S2'] else 'FAIL'}; S3 max {R['maxabsZ']:.2f} p {R['S3_p']:.3f} {'ok' if R['ok']['S3'] else 'FAIL'}")
    pr = out["runs"]["PRIMARY M+G+K"]; ic = [x for x in pr["rows"] if x["name"] == "IC 1613"][0]
    v = "IC 1613 RESOLVED BY DATA" if abs(ic["Z"]) < 2 else ("IC 1613 REDUCED" if abs(ic["Z"]) <= 0.5 * abs(float(HO3[(f, "IC 1613")]["Z"])) else "IC 1613 STANDS")
    field = "FIELD HOLDS (law)" if all(pr["rules"]["ok"].values()) else "FIELD FAILS (law): " + ", ".join(k for k, o in pr["rules"]["ok"].items() if not o)
    out["verdict"] = v; out["field"] = field
    P(f"  PRIMARY per object: " + "; ".join(f"{x['name']} {x['E']:+.2f} (Z {x['Z']:+.1f}, {''.join(x['used']) or '-'})" for x in pr["rows"]))
    P(f"  VERDICT [{f}]: {v}; {field}")
    RES["footings"][f] = out
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9; checks["K2"] = peak < 1.0
RES["checks"] = checks
fn = os.path.join(HERE, f"fd1_field_dwarf_audit_results{TAG}.json")
json.dump(RES, open(fn, "w"), indent=1, default=float)
P(f"\nchecks {sum(checks.values())}/{len(checks)}; peak RSS {peak:.2f} GB; results sha256 {hashlib.sha256(open(fn, 'rb').read()).hexdigest()}")
open(os.path.join(HERE, f"fd1_field_dwarf_audit{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(checks.values()) else 1)
