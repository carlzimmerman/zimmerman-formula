#!/usr/bin/env python3
"""KL1 (FROZEN_CRITERIA.md 99a42c78ef) row A3: the gas where RB1 measured it, put into CO1's layout of form B.
CO1's co1_hm.py above its KA1 section executed unchanged (it executes CFG556's library part read-only). In CO1's group / cluster
regime only: inside R500 the gas cumulative mass is scaled so that stars + gas = f_ret(M500) x the layout's own baryons there; the
removed mass goes back between R500 and R_out with M(<r) linear in r. The cold component is held. Galaxy regime unchanged.
  f_ret primary: RB1's 176-system ladder (KVM18 stars) by log M500 [Msun]; bracket: slope +0.160 through (13.75, 0.592). Cap 1.
  R_out graded: r_ta; reported: R200c.
KA3 (i) f_ret = 1 and no inserted points -> CO1's stored R_tot to 1e-9; (ii) with inserted points, 2e-3; (iii) mass and order.
MA3 (MUTATE): f_ret = 0.2 for every group / cluster (edge r_ta) must move R_tot at k 1 by >= 0.05 (the chi^2 half is in kl1.py).

  OMP_NUM_THREADS=1 nice -n 10 python3 kl1_gas.py     -> kl1_gas.json, kl1_gas.out, kl1_gas_MUTATE.json
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing. Inherited halo list (CO1's criteria)."""
import os, sys, json, math, time, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CO1 = os.path.join(REPO, "closure_2026_11_09", "CO1_form_b_cosmology_computed")
_src = open(os.path.join(CO1, "co1_hm.py")).read(); _cut = _src.index("# ------------------------------------------------------------------ KA1: CFG556's committed primary table")
NS = {"__file__": os.path.join(CO1, "co1_hm.py"), "__name__": "co1_hm_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src[:_cut], "co1_hm.py", "exec"), NS)
L, layout, is_cluster, bar_cum = NS["L"], NS["layout"], NS["is_cluster"], NS["bar_cum"]
h, FB, KK, MM = L["h"], L["FB"], L["KK"], L["MM"]
RGRID0 = NS["rgrid"]
HMJ = json.load(open(os.path.join(CO1, "co1_hm.json")))
RB1 = json.load(open(os.path.join(REPO, "closure_2026_11_09", "RB1_form_b_hot_systems", "rb1.json")))
FOOTS = ("canonical", "alt"); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()

tab = RB1["gate2"]["canonical"]["extended_GS4"]["median_fret_gas_by_mass"]
assert tab == RB1["gate2"]["alt"]["extended_GS4"]["median_fret_gas_by_mass"]
LMC = np.array([13.25, 13.75, 14.25, 14.75, 15.25]); FRT = np.array([tab[k]["kvm"] for k in ("13.0-13.5", "13.5-14.0", "14.0-14.5", "14.5-15.0", "15.0-15.5")])
def fret_table(lm500): return min(float(np.interp(lm500, LMC, FRT)), 1.0)
def fret_power(lm500): return min(0.592 * 10 ** (0.160 * (lm500 - 13.75)), 1.0)
FRET = {"table": fret_table, "power": fret_power}

def r500_of(hb, r, M):
    rho_c = hb["M200c"] / (200 * 4 / 3 * math.pi * hb["r200c"] ** 3)
    g = lambda x: float(np.interp(x, r, M)) - 500 * rho_c * 4 / 3 * math.pi * x ** 3
    return brentq(g, 1e-3 * hb["r200c"], hb["r200c"], xtol=1e-12 * hb["r200c"])
def layout_gas(hb, foot, fret="table", edge="rta", insert=True, fixed=None):
    if not is_cluster(hb, foot, "vstiff"):
        return layout(hb, foot, mode="B")
    r, M, inf = layout(hb, foot, mode="B")
    R500 = r500_of(hb, r, M); M500 = float(np.interp(R500, r, M)); lm500 = math.log10(M500 / h)
    Rout = hb["rta"] if edge == "rta" else hb["r200c"]
    if insert:
        NS["rgrid"] = lambda hb_, rmax: np.unique(np.concatenate([RGRID0(hb_, rmax), [R500, Rout]]))
        try: r, M, inf = layout(hb, foot, mode="B")
        finally: NS["rgrid"] = RGRID0
    f = fixed if fixed is not None else FRET[fret](lm500)
    R2 = hb["r200c"]; Mbs = FB * hb["M200c"]; ms = min(L["mstar"](hb), Mbs); mg = Mbs - ms
    rc = 0.1 * R2; gb = lambda x: x / rc - np.arctan(x / rc)
    mg_cum = lambda x: mg * gb(np.minimum(x, R2)) / gb(R2)
    mb500 = float(bar_cum(hb, Mbs, np.array([R500]), R2)[0]); mg500 = float(mg_cum(np.array([R500]))[0]); ms500 = mb500 - mg500
    s = (f * mb500 - ms500) / mg500 if mg500 > 0 else 1.0; short = s < 0; s = min(max(s, 0.0), 1.0)
    dM = (1 - s) * mg500
    Mn = M - (1 - s) * mg_cum(np.minimum(r, R500)) + dM * np.clip((r - R500) / (Rout - R500), 0.0, 1.0)
    inf = dict(inf, R500=R500, R500_over_R200c=R500 / R2, lgM500_Msun=lm500, f_ret=f, s=s, gas_short=bool(short), dM_over_M200c=dM / hb["M200c"])
    return r, Mn, inf

def R_tot_of(foot, **kw):
    NS["set_population"]()
    Ustd = L["U_std"](); Pstd, _, _ = L["spectra_std"](Ustd)
    UL, _ = L["U_set"](lambda hb: layout(hb, foot, mode="L")); PLta, _, _ = L["spectra_ta"](UL)
    UB, infB = L["U_set"](lambda hb: layout_gas(hb, foot, **kw)); PB, _, _ = L["spectra_ta"](UB)
    return 1 + (PB - PLta) / Pstd, infB
KSEL = (0.1, 0.3, 0.5, 1.0, 2.0, 3.0, 5.0)
def at(R): return {str(k): float(np.interp(k, KK, R)) for k in KSEL}

RES = dict(lane="KL1", row="A3", criteria="99a42c78ef", note="kappa = 1/2 FITTED; not theory closed; adopts nothing; inherited halo list", k=KK.tolist(),
           fret_table=dict(lgM500=LMC.tolist(), f=FRT.tolist(), source="rb1.json gate2 extended_GS4 median_fret_gas_by_mass kvm"), KA={}, rows={})
MUT = {}
P("KL1 A3: RB1's retained gas fraction in CO1's layout of form B (group / cluster regime). kappa = 1/2 FITTED; not theory closed.")
P("  f_ret table (log M500 Msun: f): " + ", ".join(f"{a:.2f}: {b:.3f}" for a, b in zip(LMC, FRT)))
for ft in FOOTS:
    ref = np.array(HMJ["primary"][ft]["R_tot"])
    R_a, _ = R_tot_of(ft, insert=False, fixed=1.0); R_b, _ = R_tot_of(ft, insert=True, fixed=1.0)
    ka_i = float(np.max(np.abs(R_a - ref))); ka_ii = float(np.max(np.abs(R_b / ref - 1)))
    # (iii) mass conservation and order, on every halo, both edges, primary f_ret
    worst, mono, short = 0.0, True, 0
    for edge in ("rta", "r200c"):
        for hb in L["HB"]:
            r, M, inf = layout_gas(hb, ft, edge=edge)
            worst = max(worst, abs(M[-1] - hb["Mta"]) / hb["Mta"]); mono = mono and bool(np.all(np.diff(M) >= -1e-9 * hb["Mta"])); short += int(inf.get("gas_short", False))
    RES["KA"][ft] = dict(KA3_i=ka_i, KA3_i_pass=bool(ka_i <= 1e-9), KA3_ii=ka_ii, KA3_ii_pass=bool(ka_ii <= 2e-3), KA3_iii_mass=worst, KA3_iii_monotone=mono,
                         KA3_iii_pass=bool(worst <= 1e-9 and mono), gas_short_halos=short)
    P(f"\n[{ft}] KA3 (i) f_ret = 1, no inserted points: max |R - CO1| {ka_i:.1e} -> {'PASS' if ka_i <= 1e-9 else 'FAIL'}; (ii) with inserted points: max rel {ka_ii:.1e} -> "
      f"{'PASS' if ka_ii <= 2e-3 else 'FAIL'}; (iii) max |M(<r_ta) - M_ta| / M_ta {worst:.1e}, non-decreasing {mono} -> {'PASS' if worst <= 1e-9 and mono else 'FAIL'}; halos short of gas {short}")
    for name, kw in (("rta_table", dict(edge="rta", fret="table")), ("r200c_table", dict(edge="r200c", fret="table")), ("rta_power", dict(edge="rta", fret="power"))):
        R, inf = R_tot_of(ft, **kw)
        cl = [(math.log10(MM[i]), x) for i, x in enumerate(inf) if x.get("regime") == "cluster"]
        rows = {}
        for lm in (12.5, 13.0, 13.5, 14.0, 14.5, 15.0):
            j = min(range(len(cl)), key=lambda q: abs(cl[q][0] - lm)) if cl else None
            if j is not None and abs(cl[j][0] - lm) < 0.05:
                x = cl[j][1]; rows[f"{lm:g}"] = {k: float(x[k]) for k in ("lgM500_Msun", "f_ret", "s", "R500_over_R200c", "dM_over_M200c")}
        RES["rows"].setdefault(ft, {})[name] = dict(R_tot=R.tolist(), R_tot_at=at(R), R_over_CO1_at=at(R / ref), halos=rows, n_cluster=len(cl))
        P(f"  {name:12s} R_tot: " + "  ".join(f"k {k}: {v:.3f}" for k, v in at(R).items()) + " | over CO1's: " + "  ".join(f"{v:.3f}" for v in at(R / ref).values()))
        for lm, x in rows.items():
            P(f"      log M200m {lm}: log M500 {x['lgM500_Msun']:.2f}, f_ret {x['f_ret']:.3f}, gas kept inside R500 {x['s']:.3f}, R500/R200c {x['R500_over_R200c']:.3f}, moved {x['dM_over_M200c']:.4f} M200c")
    R, _ = R_tot_of(ft, edge="rta", fixed=0.2); d1 = float(np.interp(1.0, KK, R) - np.interp(1.0, KK, ref))
    MUT[ft] = dict(R_tot=R.tolist(), R_tot_at=at(R), dR_k1=d1, bites_R=bool(abs(d1) >= 0.05))
    P(f"  MA3 (MUTATE) f_ret = 0.2, edge r_ta: R_tot(k 1) moves by {d1:+.3f} -> {'bites' if abs(d1) >= 0.05 else 'DOES NOT BITE'}   [{time.time() - T0:.0f} s]")
RES["KA_ok"] = bool(all(v["KA3_i_pass"] and v["KA3_ii_pass"] and v["KA3_iii_pass"] for v in RES["KA"].values()))
P(f"\nKnown answers KA3 all pass: {RES['KA_ok']}   ({time.time() - T0:.0f} s)")
json.dump(RES, open(os.path.join(HERE, "kl1_gas.json"), "w"), indent=1)
json.dump(dict(lane="KL1", arm="MA3 (MUTATE): f_ret = 0.2, edge r_ta", note="kappa = 1/2 FITTED; not theory closed", rows=MUT), open(os.path.join(HERE, "kl1_gas_MUTATE.json"), "w"), indent=1)
open(os.path.join(HERE, "kl1_gas.out"), "w").write("\n".join(OUT) + "\n")
