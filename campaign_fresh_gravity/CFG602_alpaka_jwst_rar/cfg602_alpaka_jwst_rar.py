#!/usr/bin/env python3
"""CFG602 (FROZEN_CRITERIA.md, committed alone first): JWST-baryon RAR points for ALPAKA IDs 1, 3, 13. Seconds. Run: python3 cfg602_alpaka_jwst_rar.py [MUTATE=1]"""
import os, json, csv, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
T = os.path.join(REPO, "data_assembly", "arxiv_tables")
MUT = os.environ.get("MUTATE", "0") == "1"
SUF = "_MUTATE" if MUT else ""
G = 4.30091e-6; K2SI = 1e6 / 3.0856775814913673e19
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
nu = lambda y: 1.0 / (1.0 - np.exp(-np.sqrt(y)))
rd = lambda f: list(csv.DictReader(open(os.path.join(T, f))))
fit = {int(r["alpaka_id"]): r for r in rd("alpaka_jwst2026_fiducial_fit.csv")}
dat = {int(r["alpaka_id"]): r for r in rd("alpaka_jwst2026_data.csv")}
out = {int(r["id"]): r for r in rd("alpaka1_digitised/alpaka1_outer_summary.csv")}
kin = {}
for r in csv.reader(open(os.path.join(T, "alpaka1_kinematics.csv"))):
    if r and r[0].isdigit(): kin[int(r[0])] = r
geo = {}
for r in csv.reader(open(os.path.join(T, "alpaka1_geometry.csv"))):
    if r and r[0].isdigit(): geo[int(r[0])] = r
f = lambda x: float(x) if x not in ("", "nan") else float("nan")
rng = np.random.default_rng(602)
LOG, RES, CHK = [], {"lane": "CFG602", "mutate": MUT, "discs": {}}, {}
P = lambda *a: (print(*a), LOG.append(" ".join(str(x) for x in a)))
NMC = 10000
for i in (1, 3, 13):
    z = f(out[i]["z"]); R = f(out[i]["R_ext_kpc"]); V = f(kin[i][9]) * (2 if MUT else 1); eh, el = f(kin[i][10]), f(kin[i][11])
    inc_alma, e1, e2 = f(geo[i][11]), f(geo[i][12]), f(geo[i][13])
    # table V_ext is the deprojected circular velocity (CFG272 uses it as such); inclination error enters via V ~ 1/sin i only if projected: kept as the table's own error
    def split(mu, hi, lo, n):
        s = rng.standard_normal(n); return mu + np.where(s > 0, hi, lo) * s
    Vd = split(V, eh, el, NMC)
    lm = lambda k: (f(fit[i][k]), f(fit[i][k + "_errhi"]), f(fit[i][k + "_errlo"]))
    Ms = 10 ** split(*lm("logMstar_dyn"), NMC); Mg = 10 ** split(*lm("logMgas"), NMC)
    Mb = Ms + Mg
    gobs = Vd ** 2 / R * K2SI
    row = {"z": z, "R_ext_kpc": R, "V_ext": V, "logMb_central": math.log10(10 ** f(fit[i]["logMstar_dyn"]) + 10 ** f(fit[i]["logMgas"]))}
    for br, fr in (("B_max", 1.0), ("B_half", 0.5)):
        gb = G * fr * Mb / R ** 2 * K2SI
        D = gobs / gb
        for ft, a0 in FOOT.items():
            y = gb / a0
            lr = np.log10(D / nu(y))
            m, s = float(np.mean(lr)), float(np.std(lr))
            row[f"{br}|{ft}"] = dict(y_median=float(np.median(y)), D_median=float(np.median(D)), log10_D_over_nu=m, sig=s, consistent=bool(abs(m) <= 2 * s))
    lab = {}
    for ft in FOOT:
        cond = row[f"B_max|{ft}"]["y_median"] <= 1.0
        cons = [row[f"{b}|{ft}"]["consistent"] for b in ("B_max", "B_half")]
        lab[ft] = dict(conditioned=cond, consistency="CONSISTENT" if all(cons) else "TENSION" if not any(cons) else "BRACKET-DEPENDENT")
    row["labels"] = lab
    RES["discs"][i] = row
    P(f"ID{i} z {z:.3f} R_ext {R:.2f} kpc V_ext {V:.0f}: log Mb {row['logMb_central']:.2f}")
    for br in ("B_max", "B_half"):
        for ft in FOOT:
            r = row[f"{br}|{ft}"]
            P(f"   {br} {ft:9s} y {r['y_median']:6.2f}  D {r['D_median']:.2f}  log(D/nu) {r['log10_D_over_nu']:+.2f}+-{r['sig']:.2f}  {'consistent' if r['consistent'] else 'outside 2 sigma'}")
    P("   labels:", lab)
# controls
d13 = RES["discs"][13]
# K1: stars-only (SED M*) B_max D for ID13 vs CFG272's committed D = 0.442 (spherical shortcut here differs from CFG272's disc model; tolerance as frozen 0.02)
c272 = json.load(open(os.path.join(os.path.dirname(HERE), "CFG272_alpaka_five_discs", "cfg272_stageB_results.json")))
Msed = 10 ** f(dat[13]["logMstar_sed"]); gb0 = G * Msed / f(out[13]["R_ext_kpc"]) ** 2 * K2SI
D0 = (f(kin[13][9]) ** 2 / f(out[13]["R_ext_kpc"]) * K2SI) / gb0
CHK["K1 ID13 stars-only D vs CFG272 0.442 (tol 0.02)"] = dict(ok=abs(D0 - 0.442) <= 0.02, msg=f"this lane's spherical D {D0:.3f} vs 0.442")
CHK["K2 alt differs only by a0"] = dict(ok=all(abs(RES["discs"][i]["B_max|canonical"]["D_median"] - RES["discs"][i]["B_max|alt"]["D_median"]) < 1e-12 for i in RES["discs"]), msg="D identical across footings")
cond_any = any(RES["discs"][i]["labels"][ft]["conditioned"] and RES["discs"][i]["labels"][ft]["consistency"] != "BRACKET-DEPENDENT" for i in RES["discs"] for ft in FOOT)
RES["verdict"] = "A0-INFORMATIVE" if cond_any else "NOT INFORMATIVE FOR a0 (reported D only)"
for k, v in CHK.items(): P(f"  [{'PASS' if v['ok'] else 'FAIL'}] {k}: {v['msg']}")
P("VERDICT:", RES["verdict"])
RES["checks"] = CHK
json.dump(RES, open(os.path.join(HERE, f"cfg602_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg602{SUF}.out"), "w").write("\n".join(LOG) + "\n")
