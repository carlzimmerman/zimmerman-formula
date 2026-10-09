#!/usr/bin/env python3
"""CFG531 verdict (FROZEN_CRITERIA.md section 5, criteria commit 750fa1f55): joins cfg531_kids_results.json and
cfg531_sluggs_results.json and applies the frozen ladder per footing.  No new physics.  Run: python3 cfg531_verdict.py"""
import os, json, math

HERE = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(HERE, "cfg531_kids_results.json")))
S = json.load(open(os.path.join(HERE, "cfg531_sluggs_results.json")))
KM = json.load(open(os.path.join(HERE, "cfg531_kids_results_MUTATE.json")))
SM = json.load(open(os.path.join(HERE, "cfg531_sluggs_results_MUTATE.json")))
FOOTS, CONS = ("canonical", "alt"), ("A", "B")
LOG = []


def P(s=""):
    print(s); LOG.append(s)


RES = {"lane": "CFG531", "script": "cfg531_verdict", "criteria_commit": "750fa1f55"}
P("CFG531 verdict (frozen ladder, per footing; kappa = 1/2 FITTED; footings never pooled)")
# overlaps
geo = K["geometry"]; sg = S["geometry"]
OV = {}
for ft in FOOTS:
    s_R = [min(sg[f"NGC{n}|{ft}"]["R_min"] for n in (4486, 4365, 4374, 5846)), max(sg[f"NGC{n}|{ft}"]["R_max"] for n in (4486, 4365, 4374, 5846))]
    s_x = [min(sg[f"NGC{n}|{ft}"]["r_over_rM"][0] for n in (4486, 4365, 4374, 5846)), max(sg[f"NGC{n}|{ft}"]["r_over_rM"][1] for n in (4486, 4365, 4374, 5846))]
    k_R = [geo["K-in"]["R16_kpc"], geo["K-in"]["R84_kpc"]]
    k_x = geo["K9"]["r_over_rM"][ft]
    s_m = min(sg[f"NGC{n}|{ft}"]["logMs_table"] for n in (4486, 4365, 4374, 5846))
    OV[ft] = dict(kpc=bool(k_R[0] <= s_R[1] and s_R[0] <= k_R[1]), kpc_ranges=dict(KiDS_Kin_16_84=k_R, SLUGGS_outer=s_R),
                  r_over_rM=bool(k_x[0] <= s_x[1] and s_x[0] <= k_x[1]), r_over_rM_ranges=dict(KiDS_K9=k_x, SLUGGS_outer=s_x),
                  Mstar=bool(K["f30_logMs_percentiles"]["95"] >= s_m), Mstar_values=dict(f30_p95=K["f30_logMs_percentiles"]["95"], SLUGGS_min=s_m),
                  environment="f30 isolated lenses vs group/cluster centrals (different)")
    P(f"  overlap [{ft}]: kpc {OV[ft]['kpc']} (KiDS K-in 16-84% {k_R[0]:.0f}-{k_R[1]:.0f}, SLUGGS outer {s_R[0]:.0f}-{s_R[1]:.0f} kpc); "
      f"r/r_M {OV[ft]['r_over_rM']} (KiDS K9 {k_x[0]:.2f}-{k_x[1]:.2f}, SLUGGS {s_x[0]:.2f}-{s_x[1]:.2f}); M* {OV[ft]['Mstar']} "
      f"(f30 p95 {K['f30_logMs_percentiles']['95']:.2f} vs SLUGGS min {s_m:.2f}); environment different")
RES["overlap"] = OV

V = {}
for ft in FOOTS:
    sJ = S["eps"][f"J joint best case|{ft}"]["class4"]
    ag = {}
    for c in CONS:
        kin = K["base"][f"{c}|{ft}|LAW_RTA"]["K-in"]
        sc = math.hypot(kin["sig"], sJ["sig_eps"])
        ag[c] = dict(eps_KiDS_Kin=kin["eps"], sig_K=kin["sig"], eps_SLUGGS_J=sJ["eps"], sig_S=sJ["sig_eps"], diff=kin["eps"] - sJ["eps"],
                     Z=(kin["eps"] - sJ["eps"]) / sc, ok=abs(kin["eps"] - sJ["eps"]) <= 2 * sc)
    AG = all(v["ok"] for v in ag.values())
    KS, SS, RG = K["KS"][ft], S["SS"][ft], K["RG"][ft]
    EA, DB, CR = K["a_verdict"][ft]["explained"], K["b_depends"][ft], K["c_reading"][ft]
    kern = {}
    for kn in ("simple", "standard"):
        for t in ("T-free", "T-fix"):
            kz = all(abs(K["d"][f"{kn}|{t}|{c}|{ft}"]["K9"]["Z"]) < 2 for c in CONS)
            sd = S["d"][f"{kn}|{t}|{ft}"]; sz = abs(sd["eps_J"]) < 2 * sd["sig_eps_J"]
            kern[f"{kn}|{t}"] = dict(KiDS_K9_null=kz, SLUGGS_J_null=sz, sparc_pass=K["d_sparc_CFG468"][kn]["sparc_pass"],
                                     removes_both=bool(kz and sz and K["d_sparc_CFG468"][kn]["sparc_pass"]))
    KD = any(v["removes_both"] for v in kern.values())
    if not KS:
        lab = "NOT DIAGNOSTIC" if AG else "DIFFERENT"
    elif EA:
        lab = "EXPLAINED BY (a)"
    elif DB:
        lab = "EXPLAINED BY (b)"
    elif CR == "CARRIED BY LATE TYPES":
        lab = "DIFFERENT (different galaxy class)"
    elif KD:
        lab = "EXPLAINED BY (d)"
    elif SS and RG and AG:
        lab = "SHARED SHORTFALL"
    else:
        lab = "DIFFERENT"
    V[ft] = dict(KS=KS, SS=SS, RG=RG, AG=AG, AG_detail=ag, explained_a=EA, depends_b=DB, c_reading=CR, kernel=kern, label=lab)
    P(f"\n  [{ft}] KS {KS}, SS {SS}, RG {RG}, AG {AG} ("
      + "; ".join(f"{c}: KiDS K-in {v['eps_KiDS_Kin']:+.3f}+-{v['sig_K']:.3f} vs SLUGGS J {v['eps_SLUGGS_J']:+.3f}+-{v['sig_S']:.3f}, Z {v['Z']:+.2f}" for c, v in ag.items())
      + f"); (a) {EA}; (b) {DB}; (c) {CR}; (d) removes both: {KD}")
    P(f"  [{ft}] LABEL: {lab}")
labels = {V[f]["label"] for f in FOOTS}
HEAD = V["canonical"]["label"] if len(labels) == 1 else "FOOTING-DEPENDENT (" + "; ".join(f"{f}: {V[f]['label']}" for f in FOOTS) + ")"
RES["per_footing"] = V
# mechanism
mech = {}
for ft in FOOTS:
    sJ = S["eps"][f"J joint best case|{ft}"]["class4"]["eps"]
    ma = [S["mech_Ma"][f"NGC{n}|{ft}"]["eps_supplied"] for n in (4486, 4365, 4374, 5846)]
    ma_cls = sum(ma) / 4
    kin = {c: K["base"][f"{c}|{ft}|LAW_RTA"]["K-in"]["eps"] for c in CONS}
    mc_K = {c: K["base"][f"{c}|{ft}|LAW_RTA"]["K-in"]["eps"] - K["base"][f"{c}|{ft}|CENSUS"]["K-in"]["eps"] for c in CONS}
    mb_K = -K["mech_Mb"][ft]["K-in"]["d_eps_vs_point"]
    rows = {"M-a contraction (KiDS 0 by construction)": dict(KiDS=0.0, SLUGGS=ma_cls),
            "M-b extended baryons (supplied = -d eps)": dict(KiDS=mb_K, SLUGGS=0.0),
            "M-c census edge (supplied = eps_law - eps_census)": dict(KiDS=min(mc_K.values()), SLUGGS=0.0)}
    found = []
    for k_, v in rows.items():
        fk = v["KiDS"] / min(kin.values()) if min(kin.values()) > 0 else float("nan")
        fs = v["SLUGGS"] / sJ if sJ > 0 else float("nan")
        v.update(frac_KiDS=fk, frac_SLUGGS=fs, found=bool(fk >= 0.5 and fs >= 0.5))
        if v["found"]:
            found.append(k_)
    mech[ft] = dict(rows=rows, found=found)
    P(f"  mechanism [{ft}]: " + "; ".join(f"{k_}: KiDS {v['KiDS']:+.4f} ({v['frac_KiDS']:.2f} of need), SLUGGS {v['SLUGGS']:+.3f} ({v['frac_SLUGGS']:.2f})" for k_, v in rows.items()))
MECH = "FOUND" if all(mech[f]["found"] for f in FOOTS) else "NONE"
RES["mechanism"] = dict(per_footing=mech, verdict=MECH)
mut = dict(kids={k: v["ok"] for k, v in KM["checks"].items()}, sluggs={k: v["ok"] for k, v in SM["checks"].items()})
RES["mutate"] = mut
P(f"\n  MUTATE: kids {sum(mut['kids'].values())}/{len(mut['kids'])}, sluggs {sum(mut['sluggs'].values())}/{len(mut['sluggs'])}")
P(f"\nHEADLINE: {HEAD}; mechanism {MECH}")
RES["headline"] = HEAD
json.dump(RES, open(os.path.join(HERE, "cfg531_verdict_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg531_verdict.out"), "w").write("\n".join(LOG) + "\n")
