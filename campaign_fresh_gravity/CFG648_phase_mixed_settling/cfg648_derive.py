#!/usr/bin/env python3
"""CFG648 derivations (FROZEN_CRITERIA.md, 2e9dffba1): phase-mixed settling H-SP on CFG637's infall solver (cfg648_lib.InfallSP).

D1 r_sp/r_ta vs Gamma (eps grid) for the CFG637 representative galaxy / group / cluster, both footings, both sources, brackets
(apo, R5lit), C2 (N 3200), C3 (no-core benchmark); D2 EPS seed (CFG557, CONTEXT) for the representative systems and the T6 masses;
per-system H-SP runs (eps = 1) for the gate systems: 63 Tian+26 groups, 12 X-COP clusters, Bullet BASE/B1/B2/B3, KiDS lens masses
(5/50/95 percentiles, and the eps grid at the median for the age-split bound), CFG556 halo masses (T6), SPARC galaxies (T1).
Writes cfg648_profiles.npz (not committed; regenerated here), cfg648_derive.out, cfg648_derive_results.json. No gate number.
MUTATE (CFG648_MUTATE=1): M-ta (H-SP off reproduces cfg637_lib to 0 on the three representative systems) and M-Gamma (EPS seeds
reversed across the T6 masses); writes *_MUTATE outputs.
Run from the repository root:  OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG648_phase_mixed_settling/cfg648_derive.py
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, math, json, time, contextlib, pickle
import numpy as np
from scipy.stats import spearmanr

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
for d in (LANES, HERE, os.path.join(LANES, "CFG515_census_edge_resolution"), os.path.join(LANES, "CFG543_group_supply"),
          os.path.join(LANES, "CFG540_vizier2026_bfjr_mhongoose"), os.path.join(LANES, "CFG625_merger_baryon_inputs"),
          os.path.join(LANES, "CFG557_settling_catchment_derived"), os.path.join(LANES, "CFG487_settled_fraction_switch"),
          os.path.join(REPO, "qwen_claude_field_theory", "closure_2026", "cluster_measurement_audit_2026")):
    sys.path.insert(0, d)
try:
    os.nice(10)
except OSError:
    pass
import cfg648_lib as S                                                      # noqa: E402
L = S.L
import CFG4_common as C4                                                    # noqa: E402
with contextlib.redirect_stdout(io.StringIO()):
    import cfg543_group_supply as G543                                       # noqa: E402
    import cfg625_lib as L625                                                # noqa: E402
    import cluster_audit as CA                                               # noqa: E402
    import cfg557_lib as E557                                                # noqa: E402
import cfg540_bfjr as C540                                                    # noqa: E402
from cfg597_lib import nu_mono as nu597                                       # noqa: E402
MUTATE = os.environ.get("CFG648_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
CACHE = os.environ.get("CFG648_CACHE")            # optional pickle of finished runs (restart aid; never committed)
LOG, CHK = [], {}
RES = {"lane": "CFG648", "script": "cfg648_derive", "criteria": "2e9dffba1", "mutate": MUTATE}
PROF = {}
K = L.SI_TO_KPCGYR2
FOOTS = ("canonical", "alt")
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
EPS_GRID = (0.3, 0.5, 0.75, 1.0, 1.5, 2.5)


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}: {msg}")


_cache = {}
if CACHE and os.path.exists(CACHE):
    _cache = pickle.load(open(CACHE, "rb"))
S1MAX = [0.0]


def run(key, *args, **kw):
    """one H-SP derivation; returns a compact record (summary, profiles on rg in kpc/Msun). Cached by key."""
    if key in _cache:
        return _cache[key]
    I = S.derive_sp(*args, **kw)
    d = I.sp_summary() if I.hsp else I.summary()
    rec = dict(sum=d, rg=I.rg.copy(), Mres=I.M_res_g.copy(), Mset=I.M_set_g.copy(), Mcore=I.M_core_g.copy(), Mtot=I.Mtot_g.copy(),
               rta=I.rta, supply=I.supply_turned, Mres_tot=I.M_res_tot, drawn=I.drawn, hsp=I.hsp)
    if I.hsp:
        # S1: settled H-SP profile never exceeds B's (law phantom truncated at B's full-supply edge, confined to r_ta)
        Ms = I.Mret_t * I.S_src
        mphB = L.phantom_trunc(I.x_core, Ms, I.rta, I.a0, I.nu, I.cold_t)[0]
        MB = np.interp(I.rg / I.rta, I.x_core, mphB, left=0.0)
        rec["MsetB"] = MB
        S1MAX[0] = max(S1MAX[0], float(np.max(I.M_set_g - MB) / max(MB[-1], 1e-30)))
        rec["cons_err"] = abs(I.drawn + I.M_res_tot - I.supply_turned) / I.supply_turned
    _cache[key] = rec
    if CACHE and len(_cache) % 10 == 0:
        pickle.dump(_cache, open(CACHE, "wb"))
    return rec


def band_mass(rec, M, lo=0.2, hi=0.5):
    x = rec["rg"] / rec["rta"]
    return float(np.interp(hi, x, M) - np.interp(lo, x, M))


P(__doc__.split("Run from")[0].strip())
P(f"  background: Om {L.OM:.4f}, OL {L.OL:.4f}, f_b {L.FB:.5f}, cold/b {L.COLD_PER_B:.4f}")

# ======================================================================================= representative systems (CFG637)
ROWS = G543.read_groups()
X, M_T, HERN_RE = G543.X, G543.M_T, G543.HERN_RE
o_med = ROWS[len(ROWS) // 2]
CL = [CA.load_cluster(p.name) for p in sorted(CA.DATA.iterdir()) if p.is_dir()]
NAMES = [c["name"] for c in CL]
GAS, STARS, MH = CA.profiles(CL, CA.RADII, False)
ETT = json.load(open(os.path.join(REPO, "real_research", "data", "xcop", "xcop_r500_ettori2019.json")))


def loglin_extrap(x, xp, fp):                     # CFG634's function, verbatim (as CFG637)
    ok = np.isfinite(fp) & (fp > 0) & (xp > 0)
    xp, fp = np.asarray(xp)[ok], np.asarray(fp)[ok]
    if x <= xp[-1]:
        return float(np.exp(np.interp(np.log(x), np.log(xp), np.log(fp))))
    s = np.polyfit(np.log(xp[-3:]), np.log(fp[-3:]), 1)[0]
    return float(fp[-1] * (x / xp[-1]) ** s)


# X-COP cores: CFG637 cfg637_derive.py construction, copied verbatim
R200 = {n: ETT[n]["R200"] * 1000.0 for n in NAMES}
G200, S200 = {}, {}
for c in CL:
    G200[c["name"]] = loglin_extrap(R200[c["name"]], c["rg"], c["mg"])
    S200[c["name"]] = loglin_extrap(R200[c["name"]], c["rs"], c["ms"]) if c["has_star"] else np.nan
rat200 = np.nanmedian([S200[n] / G200[n] for n in NAMES if np.isfinite(S200[n])])
for n in NAMES:
    if not np.isfinite(S200[n]):
        S200[n] = rat200 * G200[n]
XCORE = {}
for i, c in enumerate(CL):
    n = c["name"]; R2 = R200[n]
    rr = np.geomspace(1.0, R2, 400)
    gas = np.array([loglin_extrap(x, c["rg"], c["mg"]) for x in np.maximum(rr, c["rg"][0])])
    gas = np.where(rr < c["rg"][0], gas * (rr / c["rg"][0]) ** 2, gas)
    lr = np.log(np.r_[CA.RADII, R2]); rat = np.r_[STARS[i] / GAS[i], S200[n] / G200[n]]
    okr = np.isfinite(rat) & (rat > 0)
    stars = gas * np.interp(np.log(rr), lr[okr], rat[okr])
    rr = np.r_[rr, 3e4]; gas = np.r_[gas, gas[-1]]; stars = np.r_[stars, stars[-1]]
    XCORE[n] = (rr, gas, stars)
n0 = "A1795" if "A1795" in NAMES else NAMES[0]
M = 10 ** o_med["lM"]; ak = o_med["Re"] / HERN_RE; rG = X * ak
rrA, gasA, starsA = XCORE[n0]; MbA = G200[n0] + S200[n0]
REPS = {
    "galaxy": dict(args=(6e10 / 0.10 / L.FB, 0.10, X * 3.0, 6e10 * M_T), src={"B": 6e10 * M_T}, nu=C540.nu, kind="galaxy"),
    "group": dict(args=(M / 0.10 / L.FB, 0.10, rG, M * M_T), src={"B": M * M_T, "HCB": 0.92 * M * M_T}, nu=C540.nu, kind="group"),
    "cluster": dict(args=(MbA / 0.90 / L.FB, 0.90, rrA, gasA + starsA), src={"B": gasA + starsA, "HCB": starsA}, nu=C4.nu_mono, kind="cluster"),
}
P(f"  representative group {o_med['id']} (log M_bar {o_med['lM']:.2f}); cluster {n0}")


def rep_run(nm, src, foot, tag, **kw):
    Mta, fr, r_, Mc = REPS[nm]["args"]
    return run(f"REP|{nm}|{src}|{foot}|{tag}", Mta, fr, r_, Mc, REPS[nm]["src"][src], A0[foot] * K, REPS[nm]["nu"], **kw)


# ======================================================================================= MUTATE M-ta (derive side)
if MUTATE:
    P("\n== M-ta: H-SP off (r_sp -> r_ta) vs cfg637_lib.derive, same inputs (canonical)")
    worst = 0.0
    for nm, src in (("galaxy", "B"), ("group", "B"), ("cluster", "HCB")):
        Mta, fr, r_, Mc = REPS[nm]["args"]; a0 = A0["canonical"] * K
        I0 = L.derive(Mta, fr, r_, Mc, REPS[nm]["src"][src], a0, REPS[nm]["nu"])
        I1 = S.derive_sp(Mta, fr, r_, Mc, REPS[nm]["src"][src], a0, REPS[nm]["nu"], hsp=False)
        d = max(float(np.max(np.abs(I0.M_res_g - I1.M_res_g))) / max(I0.supply_turned, 1), abs(I0.drawn - I1.drawn) / I0.supply_turned,
                abs(I0.rta - I1.rta) / I0.rta, float(np.max(np.abs(I0.Mtot_g - I1.Mtot_g)) / I0.Mtot_g[-1]))
        worst = max(worst, d)
        P(f"  {nm} ({src}): max rel diff {d:.1e}; reservoir/supply {I0.M_res_tot / I0.supply_turned:.4f} / {I1.M_res_tot / I1.supply_turned:.4f}")
    check("M-ta derive: H-SP off reproduces cfg637_lib.derive (M_res, drawn, r_ta, M_tot) to 0", worst == 0.0, f"max rel diff {worst:.1e}")
    RES["M_ta_derive_maxdiff"] = worst

# ======================================================================================= D1
D1 = {}
if not MUTATE:
    P("\n== D1 r_sp/r_ta vs Gamma (eps grid), representative systems, PRIMARY (max caustic, phase-mixed draw)")
    P("   system  src  foot       eps   Gamma    s=r_sp/r_ta  x_edge_B  x_edge_SP  x_set  settled/B  res/supply  first-infall/supply  set(0.2-0.5)/B  scattered")
    for nm in REPS:
        for src in REPS[nm]["src"]:
            for foot in FOOTS:
                rows = []
                for eps in EPS_GRID:
                    rec = rep_run(nm, src, foot, f"eps{eps}", eps=eps)
                    s = rec["sum"]
                    bB = band_mass(rec, rec["MsetB"]); bS = band_mass(rec, rec["Mset"]); bR = band_mass(rec, rec["Mres"])
                    row = dict(eps=eps, gamma=s["gamma"], s=s["s"], x_edge_B=s["x_edge_B"], x_edge_SP=s["x_edge_sp"], x_set=s["x_cut"],
                               settled_over_B=s["settled_over_Btarget"], res_over_supply=s["reservoir_total"] / s["supply_turned"],
                               firstinfall_over_supply=s["res_firstinfall_frac"], band_set_over_B=bS / max(bB, 1e-30),
                               band_res_over_Bset=bR / max(bB, 1e-30), n_scattered=s["n_scattered"], r_ta_kpc=s["r_ta_kpc"],
                               t_peri_apo=s["t_peri_to_apo_gyr_recent"], shortfall=s["final_shortfall"])
                    rows.append(row)
                    P(f"   {nm:8s} {src:4s} {foot:9s} {eps:4.2f}  {row['gamma']:6.3f}   {row['s']:8.3f}    {row['x_edge_B'] or float('nan'):7.3f}   "
                      f"{row['x_edge_SP'] if row['x_edge_SP'] is not None else float('nan'):7.3f}  {row['x_set']:6.3f}   {row['settled_over_B']:6.3f}    "
                      f"{row['res_over_supply']:6.3f}       {row['firstinfall_over_supply']:6.3f}            {row['band_set_over_B']:6.3f}       {row['n_scattered']}")
                g = [r["gamma"] for r in rows]; sv = [r["s"] for r in rows]
                rho = float(spearmanr(g, sv).correlation)
                r1 = rows[EPS_GRID.index(1.0)]
                D1[f"{nm}|{src}|{foot}"] = dict(rows=rows, spearman_s_gamma=rho,
                                                binds_eps1=bool(r1["x_edge_B"] is None or r1["s"] < r1["x_edge_B"]))
    lab = {}
    for nm in REPS:
        for src in REPS[nm]["src"]:
            rr_ = [D1[f"{nm}|{src}|{f}"] for f in FOOTS]
            lab[f"{nm}|{src}"] = dict(trend="TREND" if all(v["spearman_s_gamma"] < 0 for v in rr_) else "NO TREND",
                                      binds="BINDS" if all(v["binds_eps1"] for v in rr_) else "DOES NOT BIND",
                                      rho=[v["spearman_s_gamma"] for v in rr_])
            P(f"  D1 label {nm}|{src}: {lab[nm + '|' + src]['trend']} (Spearman rho(s, Gamma) {rr_[0]['spearman_s_gamma']:+.2f} / {rr_[1]['spearman_s_gamma']:+.2f}); "
              f"r_sp vs B edge at eps 1: {lab[nm + '|' + src]['binds']}")
    RES["D1"] = D1; RES["D1_labels"] = lab

    P("\n== D1 brackets at eps = 1 (apo caustic; R5lit draw) and C2 (N 3200)")
    BR = {}
    for nm in REPS:
        for src in REPS[nm]["src"]:
            for foot in FOOTS:
                for tag, kw in (("apo", dict(rsp_mode="apo")), ("R5lit", dict(draw_sp="R5lit"))):
                    rec = rep_run(nm, src, foot, tag, **kw); s = rec["sum"]
                    BR[f"{nm}|{src}|{foot}|{tag}"] = dict(s=s["s"], x_set=s["x_cut"], settled_over_B=s["settled_over_Btarget"],
                                                          res_over_supply=s["reservoir_total"] / s["supply_turned"], gamma=s["gamma"])
                    P(f"  {nm}|{src}|{foot}|{tag:5s}: s {s['s']:.3f}  x_set {s['x_cut']:.3f}  settled/B {s['settled_over_Btarget']:.3f}  res/supply {s['reservoir_total'] / s['supply_turned']:.3f}")
    C2 = {}
    for nm in REPS:
        r1 = rep_run(nm, "B", "canonical", "eps1.0", eps=1.0)
        r2 = rep_run(nm, "B", "canonical", "N3200", N=3200)
        C2[nm] = abs(r2["sum"]["s"] / r1["sum"]["s"] - 1)
    check("C2 N 1600 vs 3200: s within 5% (galaxy, group, cluster; eps 1; canonical)", all(v <= 0.05 for v in C2.values()),
          ", ".join(f"{k} {v:.3f}" for k, v in C2.items()), lb=False)
    xB = np.geomspace(1e-4, 4, 700); z0 = np.zeros_like(xB)
    Ib = S.InfallSP(1e14, 0.0, xB, z0, z0, A0["canonical"] * K, L.nu_exp, eps=1.0, q=0.02).run().final_profile()
    P(f"  C3 (reported) no-core benchmark (eps 1, q 0.02, Lambda background): s = {Ib.rsp_eff / Ib.rta:.3f}, Gamma = {Ib.gamma():.3f}, "
      f"scattered {Ib.n_scattered}")
    RES["brackets"] = BR; RES["C2"] = C2; RES["C3"] = dict(s=Ib.rsp_eff / Ib.rta, gamma=Ib.gamma())

# ======================================================================================= D2 EPS seed (CONTEXT)
P("\n== D2 EPS seed shape (CFG557 mean main-progenitor history; LCDM-background, PROVISIONAL, CONTEXT)")
with contextlib.redirect_stdout(io.StringIO()):
    EP0 = E557.Epoch(0.0)
SEEDS = {}


def eps_seed_for(Mta_phys, ep=None):
    ep = ep or EP0
    Xm, dL = ep.mah(Mta_phys * L.h)
    return S.eps_seed(Xm, dL)


# CFG556 halo masses for T6 (inherited context ingredients as in CFG556)
S556 = open(os.path.join(LANES, "CFG556_halo_model_matter_power", "cfg556_halo_model.py")).read()
pre = S556[:S556.index("# ------------------------------------------------------------------ run")]
NS6 = dict(__file__=os.path.join(LANES, "CFG556_halo_model_matter_power", "cfg556_halo_model.py"), __name__="cfg556_ro")
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(pre, "cfg556_ro", "exec"), NS6)
S634 = open(os.path.join(LANES, "CFG634_condensed_baryon_source", "cfg634_halo.py")).read()
fn_src = S634[S634.index("def cum_parts("):S634.index("def U_set(fn):")]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(fn_src, "cfg634_halo_fns", "exec"), NS6)
h6 = NS6["h"]
T6M = [1e11, 3e11, 1e12, 3e12, 1e13, 1e14, 1e15]


def t6_inputs(M200, src, foot="canonical"):
    hb = NS6["halo_basics"](M200)
    Mta = hb["Mta"]; f = NS6["fret_of"](math.log10(Mta)); Mb = f * NS6["FB"] * Mta
    a0m = NS6["A0MPC"][foot]
    rM = math.sqrt(NS6["G"] * Mb * h6 / a0m); reB = min(rM / math.log1p(f * NS6["FB"] / (1 - NS6["FB"])), hb["rta"])
    r = np.geomspace(1e-5, 1.0, 400) * hb["rta"]
    ms = min(NS6["mstar"](hb), Mb)
    Mc = Mb if src == "B" else min(max(ms, 0.10 * NS6["FB"] * Mta), Mb)
    mb, mc, _ = NS6["cum_parts"](hb, Mb, Mc, r, reB)
    rk = r / h6 * 1000.0
    return hb, Mta / h6, f, np.r_[rk, max(3e4, 2 * rk[-1])], np.r_[mb, mb[-1]] / h6, np.r_[mc, mc[-1]] / h6


T6R = {}
for M200 in T6M:
    for src in ("B", "HCB"):
        for foot in FOOTS:
            hb, Mta, f, rk, mb, mc = t6_inputs(M200, src, foot)
            rec = run(f"T6|{M200:.0e}|{src}|{foot}|eps1", Mta, f, rk, mb, mc, A0[foot] * K, L.nu_exp)
            T6R[f"{M200:.0e}|{src}|{foot}|fw"] = rec
            if not MUTATE:
                sd = eps_seed_for(Mta)
                rec2 = run(f"T6|{M200:.0e}|{src}|{foot}|EPS", Mta, f, rk, mb, mc, A0[foot] * K, L.nu_exp, seed=sd)
                T6R[f"{M200:.0e}|{src}|{foot}|eps"] = rec2
P("   M200m     src  foot       Gamma_fw  s_fw   x_set_fw  set/B_fw | Gamma_EPS  s_EPS  x_set_EPS  set/B_EPS")
T6S = {}
for M200 in T6M:
    for src in ("B", "HCB"):
        for foot in FOOTS:
            a = T6R[f"{M200:.0e}|{src}|{foot}|fw"]["sum"]
            row = dict(logMta=math.log10(T6R[f"{M200:.0e}|{src}|{foot}|fw"]["sum"]["M_ta"]), gamma_fw=a["gamma"], s_fw=a["s"], x_set_fw=a["x_cut"],
                       set_over_B_fw=a["settled_over_Btarget"], res_frac_fw=a["reservoir_total"] / a["supply_turned"])
            if not MUTATE:
                b = T6R[f"{M200:.0e}|{src}|{foot}|eps"]["sum"]
                row.update(gamma_eps=b["gamma"], s_eps=b["s"], x_set_eps=b["x_cut"], set_over_B_eps=b["settled_over_Btarget"],
                           res_frac_eps=b["reservoir_total"] / b["supply_turned"])
            T6S[f"{M200:.0e}|{src}|{foot}"] = row
            P(f"   {M200:8.0e}  {src:4s} {foot:9s}  {row['gamma_fw']:6.3f}  {row['s_fw']:6.3f}  {row['x_set_fw']:6.3f}   {row['set_over_B_fw']:6.3f}"
              + (f"  |  {row['gamma_eps']:6.3f}   {row['s_eps']:6.3f}  {row['x_set_eps']:6.3f}    {row['set_over_B_eps']:6.3f}" if not MUTATE else ""))
RES["T6_runs"] = T6S
for k, rec in T6R.items():
    PROF[f"T6|{k}|r"] = rec["rg"]; PROF[f"T6|{k}|Mres"] = rec["Mres"]; PROF[f"T6|{k}|rta"] = np.array([rec["rta"]])
    PROF[f"T6|{k}|supply"] = np.array([rec["supply"]])

if MUTATE:
    P("\n== M-Gamma: EPS seeds reversed across the T6 masses (B, both footings)")
    MG = {}
    for foot in FOOTS:
        own, used, ss, ss0 = [], [], [], []
        seeds = [eps_seed_for(t6_inputs(M200, "B")[1]) for M200 in T6M]
        rev = seeds[::-1]
        g_own = []
        for i, M200 in enumerate(T6M):
            hb, Mta, f, rk, mb, mc = t6_inputs(M200, "B", foot)
            r0 = run(f"T6|{M200:.0e}|B|{foot}|EPS", Mta, f, rk, mb, mc, A0[foot] * K, L.nu_exp, seed=seeds[i])
            r1 = run(f"T6|{M200:.0e}|B|{foot}|EPSrev", Mta, f, rk, mb, mc, A0[foot] * K, L.nu_exp, seed=rev[i])
            own.append(r0["sum"]["gamma"]); ss0.append(r0["sum"]["s"]); used.append(r1["sum"]["gamma"]); ss.append(r1["sum"]["s"])
        sl0 = float(np.polyfit(own, ss0, 1)[0]); sl_own = float(np.polyfit(own, ss, 1)[0]); sl_used = float(np.polyfit(used, ss, 1)[0])
        MG[foot] = dict(gamma_own=own, s_unshuffled=ss0, gamma_used=used, s_shuffled=ss, slope_unshuffled=sl0, slope_vs_own=sl_own,
                        slope_vs_used=sl_used)
        P(f"  [{foot}] slope ds/dGamma unshuffled {sl0:+.4f}; shuffled vs own Gamma {sl_own:+.4f}; shuffled vs used Gamma {sl_used:+.4f}")
    ok = all((np.sign(v["slope_vs_own"]) != np.sign(v["slope_unshuffled"]) or abs(v["slope_vs_own"]) < 0.5 * abs(v["slope_unshuffled"]))
             and np.sign(v["slope_vs_used"]) == np.sign(v["slope_unshuffled"]) for v in MG.values())
    na = all(abs(v["slope_unshuffled"]) < 1e-3 for v in MG.values())
    check("M-Gamma shuffled EPS seeds remove the trend vs own Gamma and keep it vs the Gamma used", ok or na,
          ("not applicable (no unshuffled trend); " if na else "") + ", ".join(f"{f}: {MG[f]['slope_unshuffled']:+.3f} -> own {MG[f]['slope_vs_own']:+.3f}, used {MG[f]['slope_vs_used']:+.3f}" for f in FOOTS))
    RES["M_Gamma"] = MG

if not MUTATE:
    P("\n== D2 representative systems with the EPS seed (CONTEXT)")
    D2 = {}
    for nm in REPS:
        sd = eps_seed_for(REPS[nm]["args"][0])
        for src in REPS[nm]["src"]:
            for foot in FOOTS:
                rec = rep_run(nm, src, foot, "EPS", seed=sd); s = rec["sum"]
                D2[f"{nm}|{src}|{foot}"] = dict(gamma=s["gamma"], s=s["s"], x_set=s["x_cut"], settled_over_B=s["settled_over_Btarget"],
                                                res_over_supply=s["reservoir_total"] / s["supply_turned"], seed_slope_hi=sd.slope_hi)
                P(f"  {nm}|{src}|{foot}: EPS seed slope at M_ta {sd.slope_hi:+.3f} -> Gamma {s['gamma']:.3f}, s {s['s']:.3f}, x_set {s['x_cut']:.3f}, settled/B {s['settled_over_Btarget']:.3f}")
    RES["D2"] = D2

    # ======================================================================================= gate systems (eps = 1, PRIMARY)
    SUMM = {}

    def store(key, rec, supply_gate):
        sc = supply_gate / rec["supply"]
        PROF[key + "|r"] = rec["rg"]; PROF[key + "|Mres"] = rec["Mres"] * sc
        s = rec["sum"]
        PROF[key + "|rsp"] = np.array([s["rsp_eff_kpc"]]); PROF[key + "|rcut"] = np.array([s["x_cut"] * rec["rta"]])
        SUMM[key] = dict(s=s["s"], x_set=s["x_cut"], gamma=s["gamma"], settled_over_B=s["settled_over_Btarget"],
                         res_over_supply=rec["Mres_tot"] / rec["supply"], rta=rec["rta"], rcut_kpc=s["x_cut"] * rec["rta"],
                         rsp_kpc=s["rsp_eff_kpc"], cons_err=rec["cons_err"], scattered=s["n_scattered"], shortfall=s["final_shortfall"],
                         t_peri_apo=s["t_peri_to_apo_gyr_recent"], excess_drawn=s["excess_drawn"])

    P("\n== groups (63 Tian+26), X-COP (12), Bullet: H-SP runs (eps 1)")
    for foot, fk in (("canonical", "can"), ("alt", "alt")):
        a0 = C540.FOOT[fk] * K
        for o in ROWS:
            Mg = 10 ** o["lM"]; ak = o["Re"] / HERN_RE; r = X * ak
            Mta = Mg / 0.10 / L.FB; supply = L.COLD_PER_B * Mg / 0.10
            for src, fs in (("B", 1.0), ("HCB", 0.92)):
                key = f"G|{o['id']}|{foot}|{src}"
                store(key, run(key, Mta, 0.10, r, Mg * M_T, fs * Mg * M_T, a0, C540.nu), supply)
        P(f"  [{foot}] groups done ({time.time() - T0:.0f} s)")
    for foot in FOOTS:
        a0 = C4.A0[foot] * K
        for n in NAMES:
            rr, gas, stars = XCORE[n]
            Mb200 = G200[n] + S200[n]; Mta = Mb200 / 0.90 / L.FB; supply = (0.1200 / 0.02237) * Mb200 / 0.90
            for src in ("B", "HCB"):
                key = f"X|{n}|{foot}|{src}"
                store(key, run(key, Mta, 0.90, rr, gas + stars, gas + stars if src == "B" else stars, a0, C4.nu_mono), supply)
        P(f"  [{foot}] X-COP done ({time.time() - T0:.0f} s)")
    AOBS_B = 1 / 1.296
    for var in ("BASE", "B1", "B2", "B3"):
        for ft in ("can", "alt"):
            for role, M200 in (("main", 1.5e15), ("sub", 1.5e14)):
                p = L625.Progenitor625(M200, ft, cloud=(role == "sub"), variant=var)
                Mta = p.Mb / L.FB; supply = 5.364 * p.Mb
                for src in ("B", "HCB"):
                    key = f"BU|{var}_{role}|{ft}|{src}"
                    store(key, run(key, Mta, 1.0, np.maximum(p.r, 1e-3), p.Mbar, p.Mbar if src == "B" else p.Ms, p.a0, nu597, a_obs=AOBS_B), supply)
        P(f"  Bullet {var} done ({time.time() - T0:.0f} s)")
    for grp in ("G", "X", "BU"):
        sel = {k: v for k, v in SUMM.items() if k.startswith(grp + "|")}
        for src in ("B", "HCB"):
            for ft in (("canonical", "alt") if grp != "BU" else ("can", "alt")):
                ss = [v for k, v in sel.items() if k.endswith(f"|{ft}|{src}")]
                if ss:
                    P(f"  {grp:2s} {src:3s} {ft:9s}: s {min(v['s'] for v in ss):.3f}-{max(v['s'] for v in ss):.3f}, x_set {min(v['x_set'] for v in ss):.3f}-{max(v['x_set'] for v in ss):.3f}, "
                      f"settled/B {min(v['settled_over_B'] for v in ss):.3f}-{max(v['settled_over_B'] for v in ss):.3f}, reservoir/supply {min(v['res_over_supply'] for v in ss):.3f}-{max(v['res_over_supply'] for v in ss):.3f}, "
                      f"Gamma {min(v['gamma'] for v in ss):.2f}-{max(v['gamma'] for v in ss):.2f}")
    b1 = SUMM["BU|B1_main|can|B"]
    P(f"  T4 merger statement input: B1 main (B, can) pericentre -> first apocentre of the most recent shells {b1['t_peri_apo']:.2f} Gyr; r_sp {b1['rsp_kpc']:.0f} kpc")

    # ======================================================================================= KiDS lenses
    P("\n== KiDS lens masses (point-mass baryons, f_ret 0.10; B = H-CB for the lens source)")
    LZ = np.load(os.path.join(REPO, "real_research", "data", "lensing_rar", "lr_lenses.npz"))
    Mg_pct = np.percentile(LZ["Mgal"], [5, 50, 95])
    KI = {}
    r_pm = np.array([1e-3, 3e4])
    for pc, Mg in zip((5, 50, 95), Mg_pct):
        Mta = Mg / 0.10 / L.FB
        for foot in FOOTS:
            prof = np.array([Mg, Mg])
            for hsp in (True, False):
                key = f"K|p{pc}|{foot}|{'SP' if hsp else 'B'}"
                rec = run(key, Mta, 0.10, r_pm, prof, prof, A0[foot] * K, C4.nu_mono, hsp=hsp)
                PROF[key + "|r"] = rec["rg"]; PROF[key + "|Mtot"] = rec["Mtot"]
                KI[key] = dict(logMgal=math.log10(Mg), rta=rec["rta"], s=rec["sum"].get("s"), x_set=rec["sum"].get("x_cut"))
            if pc == 50:
                for eps in EPS_GRID:
                    key = f"K|p50|{foot}|SPeps{eps}"
                    rec = run(key, Mta, 0.10, r_pm, prof, prof, A0[foot] * K, C4.nu_mono, eps=eps)
                    PROF[key + "|r"] = rec["rg"]; PROF[key + "|Mtot"] = rec["Mtot"]
                    KI[key] = dict(gamma=rec["sum"]["gamma"], s=rec["sum"]["s"], x_set=rec["sum"]["x_cut"], rta=rec["rta"])
            P(f"  p{pc} log M_gal {math.log10(Mg):.2f} [{foot}]: r_ta {KI[f'K|p{pc}|{foot}|SP']['rta']:.0f} kpc, s {KI[f'K|p{pc}|{foot}|SP']['s']:.3f}, x_set {KI[f'K|p{pc}|{foot}|SP']['x_set']:.3f}")
    RES["KiDS"] = KI; RES["KiDS_Mgal_pct"] = Mg_pct

    # ======================================================================================= SPARC galaxies
    P("\n== SPARC galaxies (CFG487 harness exec'd read-only; rotmod baryons; f_ret 0.10)")
    S634s = open(os.path.join(LANES, "CFG634_condensed_baryon_source", "cfg634_static.py")).read()
    hdr = S634s[:S634s.index("P(__doc__.split")]
    NS = dict(__file__=os.path.join(LANES, "CFG634_condensed_baryon_source", "cfg634_static.py"), __name__="cfg634_static_ro", __doc__="")
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(hdr, "cfg634_static_hdr", "exec"), NS)
    C7, LB = NS["C7"], NS["LB"]
    from scipy.integrate import quad
    src = open(os.path.join(LANES, "CFG487_settled_fraction_switch", "cfg487_data.py")).read()
    m0 = "# =================================================================================================== (a) SPARC (CFG346 copy)"
    m1 = "SPA = {}"
    NSS = dict(os=os, sys=sys, io=io, math=math, json=json, time=time, contextlib=contextlib, np=np, quad=quad, C7=C7, C4=C4, LB=LB,
               LANES=LANES, FOOTS=FOOTS, P=lambda *a: None, m_profile=None, __name__="cfg487_sparc_ro")
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src[src.index(m0):src.index(m1)], "cfg487_sparc_ro", "exec"), NSS)
    gb4, ok4, Rm, GI, GMB = (NSS[k] for k in ("gb4", "ok4", "Rm", "GI", "GMB"))
    GSI, MSI, KPCm = 6.67430e-11, 1.98847e30, C4.KPC
    SPS = {}
    for foot in FOOTS:
        for i, Mb in GMB.items():
            sel = np.where((GI == i) & ok4)[0]
            if not len(sel):
                continue
            sel = sel[np.argsort(Rm[sel])]; rr = Rm[sel] / KPCm
            Mbar = gb4[sel] * Rm[sel] ** 2 / GSI / MSI
            Mtot = Mb / MSI
            prof = np.maximum.accumulate(np.r_[Mbar, max(Mtot, Mbar[-1])])
            r_ = np.r_[rr, 3e4]
            key = f"S|{i}|{foot}"
            rec = run(key, prof[-1] / 0.10 / L.FB, 0.10, r_, prof, prof, A0[foot] * K, C4.nu_mono)
            PROF[key + "|r"] = rec["rg"]; PROF[key + "|Mres"] = rec["Mres"] * (L.COLD_PER_B * prof[-1] / 0.10) / rec["supply"]
            PROF[key + "|rcut"] = np.array([rec["sum"]["x_cut"] * rec["rta"]])
            SPS[key] = dict(rcut_over_Rlast=rec["sum"]["x_cut"] * rec["rta"] / rr[-1],
                            res_in_Rlast_over_Mbar=float(np.interp(rr[-1], rec["rg"], rec["Mres"]) * (L.COLD_PER_B * prof[-1] / 0.10) / rec["supply"] / Mbar[-1]),
                            s=rec["sum"]["s"], x_set=rec["sum"]["x_cut"])
        ss = [v for k, v in SPS.items() if k.endswith("|" + foot)]
        P(f"  [{foot}] {len(ss)} galaxies: r_set/R_last min {min(v['rcut_over_Rlast'] for v in ss):.1f}; reservoir inside R_last / M_bar(R_last) max "
          f"{max(v['res_in_Rlast_over_Mbar'] for v in ss):.3f}, median {np.median([v['res_in_Rlast_over_Mbar'] for v in ss]):.4f} ({time.time() - T0:.0f} s)")
    RES["SPARC"] = SPS
    RES["gate_systems"] = SUMM

    c1 = max(v.get("cons_err", 0.0) for v in _cache.values() if v.get("hsp"))
    check("C1 supply = drawn + reservoir (1e-9), every H-SP run", c1 < 1e-9, f"max rel {c1:.1e}")
    exd = max(v["sum"].get("excess_drawn", 0.0) for v in _cache.values() if v.get("hsp"))
    check("C1b gravitating settled = drawn: max (drawn - target)/target <= 1e-3", exd <= 1e-3, f"max {exd:.1e}", lb=False)
    check("S1 settled H-SP M(<r) <= candidate B's at every r, every run (1e-9 rel)", S1MAX[0] <= 1e-9, f"max excess {S1MAX[0]:.1e}")
    nsc = [v["sum"].get("n_scattered", 0) for v in _cache.values() if v.get("hsp")]
    P(f"  scattering guard (post-freeze, disclosed): shells past pericentre beyond their own turnaround radius excluded from the caustic; "
      f"max count per run {max(nsc)} of 1600 (median {int(np.median(nsc))})")

RES["checks"] = CHK; RES["elapsed_s"] = round(time.time() - T0, 1)
nf = sum(1 for c in CHK.values() if not c["ok"] and c["load_bearing"])
P(f"\n{sum(1 for c in CHK.values() if c['ok'])}/{len(CHK)} checks pass ({nf} load-bearing failures); elapsed {RES['elapsed_s']} s")
if CACHE:
    pickle.dump(_cache, open(CACHE, "wb"))
np.savez_compressed(os.path.join(HERE, f"cfg648_profiles{SUF}.npz"), **PROF)
json.dump(C4.jclean(RES), open(os.path.join(HERE, f"cfg648_derive_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg648_derive{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nf else 0)
