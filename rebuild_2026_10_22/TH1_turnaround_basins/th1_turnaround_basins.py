#!/usr/bin/env python3
"""TH1_turnaround_basins: SPARC basins from the measured radial-velocity zero crossing around UNGC group centres; flags compared with BS1.
Frozen criteria 4322b7a2a4 (committed alone). Machinery: BS1's committed UNGC frame/select/linfit block (979363d820), executed read-only
(the LG fit is K0); group frames use the Karachentsev-Makarov projection with the centre's own velocity.

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, not a particle; not theory closed;
nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 python3 -I th1_turnaround_basins.py      (TH1_MUTATE=1 twin)
"""
import os, sys, json, math, hashlib, resource
import numpy as np

MUT = os.environ.get("TH1_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
DATA = os.path.join(REPO, "real_research", "data")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
P(f"TH1_turnaround_basins (criteria 4322b7a2a4){'  [MUTATE: centre velocity sign flipped]' if MUT else ''}; kappa = 1/2 FITTED; not theory closed")
BS1S = open(os.path.join(REB, "BS1_basin_switch", "bs1_basin_switch.py")).read().split("\n")
NS = {"os": os, "np": np, "math": math, "DATA": DATA}
exec("\n".join(BS1S[47:84]), NS)                                   # BS1's vizier_tsv, _f, UNGC, ACC, frame, select, linfit_R0, LG fit
UNGC, ACC, _f, linfit_R0 = NS["UNGC"], NS["ACC"], NS["_f"], NS["linfit_R0"]
checks = {}
checks["K0"] = abs(NS["R0D"] - 794.7292882801886) < 1.0
P(f"  K0 LG zero crossing via BS1's block: R0 {NS['R0D']:.1f} kpc (BS1 794.7): {'PASS' if checks['K0'] else 'FAIL'}; H_LG {NS['H_lin']:.1f} km/s/Mpc")

nm = np.array([r["Name"].strip() for r in UNGC]); MDc = np.array([r["MD"].strip() for r in UNGC])
ra = np.array([_f(r["_RAJ2000"]) for r in UNGC]); de = np.array([_f(r["_DEJ2000"]) for r in UNGC])
D = np.array([_f(r["Dist"]) for r in UNGC]) * 1e3; V = np.array([_f(r["Vlg"]) for r in UNGC])
fD = np.array([r["f_Dist"].strip() for r in UNGC]); KL = np.array([_f(r["KLum"]) for r in UNGC])
un = np.nan_to_num(np.stack([np.cos(np.radians(de)) * np.cos(np.radians(ra)), np.cos(np.radians(de)) * np.sin(np.radians(ra)), np.sin(np.radians(de))], axis=1))
def m200(logLK):
    Mb = 1.2 * 0.6 * 10 ** logLK
    return 10 ** (11.18 + 0.90 * (math.log10(Mb) - 10))

def group_frame(ic):
    Dc, Vc = D[ic], V[ic] * (-1 if MUT else 1)
    with np.errstate(all="ignore"):
        cth = np.clip(un @ un[ic], -1, 1)
        R = np.sqrt(np.clip(D ** 2 + Dc ** 2 - 2 * D * Dc * cth, 0, None))
        Vr = V * (D - Dc * cth) / np.maximum(R, 1e-9) - Vc * (D * cth - Dc) / np.maximum(R, 1e-9)
    return R, Vr

# SPARC <-> UNGC match (0.05 deg)
pos = json.load(open(os.path.join(DATA, "sparc_positions_merged.json")))
match = {}
for k, v in sorted(pos.items()):
    with np.errstate(all="ignore"):
        c = np.sin(math.radians(v["dec"])) * np.sin(np.radians(de)) + np.cos(math.radians(v["dec"])) * np.cos(np.radians(de)) * np.cos(np.radians(ra) - math.radians(v["ra"]))
    s = np.degrees(np.arccos(np.clip(np.nan_to_num(c, nan=-1), -1, 1))); j = int(np.argmin(s))
    if s[j] < 0.05: match[k] = j
P(f"  SPARC galaxies with a UNGC counterpart: {len(match)}")

BSJ = json.load(open(os.path.join(REB, "BS1_basin_switch", "bs1_basin_switch_results.json")))
BSB = BSJ["primary_basins"]["lgM_basin_sparc"]["A_c2b_refit"]
groups = sorted({MDc[j] for j in match.values() if MDc[j]})
RES = dict(criteria="4322b7a2a4", mutate=MUT, LG=dict(R0=NS["R0D"], H=NS["H_lin"]), groups={}, sparc={})
rng = np.random.default_rng(20261028)
for g in groups:
    ii = np.where(nm == g)[0]
    if len(ii) == 0 or not np.isfinite(D[ii[0]]) or not np.isfinite(V[ii[0]]): RES["groups"][g] = dict(det=False, why="centre not in UNGC with D, Vlg"); continue
    ic = int(ii[0]); R, Vr = group_frame(ic)
    sel = np.isfinite(R) & np.isfinite(Vr) & np.isin(fD, ACC) & (R >= 200) & (R <= 3000) & (np.arange(len(nm)) != ic)
    n = int(sel.sum())
    if n < 8: RES["groups"][g] = dict(det=False, why=f"N {n} < 8"); continue
    R0, H, rms = linfit_R0(R[sel], Vr[sel])
    if not (H > 0 and 200 <= R0 <= 3000): RES["groups"][g] = dict(det=False, why=f"H {H:.0f}, R0 {R0:.0f} outside window", N=n); continue
    bs = []
    Rs, Vs = R[sel], Vr[sel]
    for _ in range(400):
        k = rng.integers(0, n, n); bs.append(float(linfit_R0(Rs[k], Vs[k])[0]))
    inside = np.isfinite(R) & (R < R0)
    lgM = math.log10(sum(m200(KL[k]) for k in np.where(inside)[0] if np.isfinite(KL[k])))
    RES["groups"][g] = dict(det=True, N=n, R0_kpc=float(R0), R0_sig=float(np.std(bs)), H=float(H), rms=rms, n_inside=int(inside.sum()), lgM_basin=lgM,
                            members=[str(x) for x in nm[inside]])
P("  groups (main disturbers of matched SPARC galaxies):")
for g, o in RES["groups"].items():
    P(f"   {g:14s} " + (f"N {o['N']:3d}  R0 {o['R0_kpc']:6.0f} +- {o['R0_sig']:4.0f} kpc  H {o['H']:6.1f}  inside {o['n_inside']:3d}  log M_basin {o['lgM_basin']:.2f}" if o["det"] else f"not determinable ({o['why']})"))
checks["K1"] = all((200 <= o["R0_kpc"] <= 3000) for o in RES["groups"].values() if o["det"])
Hs = [o["H"] for o in RES["groups"].values() if o["det"]]
checks["K3"] = any(NS["H_lin"] / 3 <= h <= 3 * NS["H_lin"] for h in Hs)

def own_lg(j): return math.log10(m200(KL[j])) if np.isfinite(KL[j]) else float("nan")
for T, lab in ((12.3, "PRIMARY T 12.3"), (12.236, "CL3 T 12.236")):
    changed = []; rows = {}
    for k, j in match.items():
        own = own_lg(j)
        bs1 = (BSB.get(k, own) > T) or (own > T)
        flow = own > T
        gi = None
        for g, o in RES["groups"].items():
            if o["det"] and nm[j] in o["members"] and o["lgM_basin"] > T: flow = True; gi = g
        rows[k] = dict(ungc=str(nm[j]), own_lgM200=own, bs1_halo=bool(bs1), flow_halo=bool(flow), flow_group=gi)
        if bs1 != flow: changed.append(k)
    v = "FLOW BASINS REPRODUCE BS1" if not changed else f"FLOW BASINS CHANGE {len(changed)} GALAXIES"
    RES["sparc"][lab] = dict(rows=rows, changed=changed, verdict=v)
    P(f"\n  {lab}: halo by flow {sum(r['flow_halo'] for r in rows.values())} / by BS1 {sum(r['bs1_halo'] for r in rows.values())} of {len(rows)}; changed: "
      + (", ".join(f"{k} (BS1 {'halo' if rows[k]['bs1_halo'] else 'law'} -> flow {'halo' if rows[k]['flow_halo'] else 'law'}; group {rows[k]['flow_group']}, own {rows[k]['own_lgM200']:.2f}, BS1 basin {BSB.get(k, float('nan')):.2f})" for k in changed) or "none"))
    P(f"  VERDICT [{lab}]: {v}")
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9; checks["K2"] = peak < 1.0
RES["checks"] = checks; RES["verdict"] = RES["sparc"]["PRIMARY T 12.3"]["verdict"]
P(f"\n  K1 {'PASS' if checks['K1'] else 'FAIL'}; K3 a group H within x3 of the LG's {'PASS' if checks['K3'] else 'FAIL'}; K2 peak RSS {peak:.2f} GB")
fn = os.path.join(HERE, f"th1_turnaround_basins_results{TAG}.json")
json.dump(RES, open(fn, "w"), indent=1, default=float)
P(f"checks {sum(checks.values())}/{len(checks)}; results sha256 {hashlib.sha256(open(fn, 'rb').read()).hexdigest()}")
open(os.path.join(HERE, f"th1_turnaround_basins{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(checks.values()) else 1)
