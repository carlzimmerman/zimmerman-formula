#!/usr/bin/env python3
"""CFG637 derivations (FROZEN_CRITERIA.md, e67940c56): Method A (self-similar secondary infall, cfg637_lib) for every gate system
(63 Tian+26 groups, 12 X-COP clusters, Bullet progenitors BASE/B1/B2/B3) on both footings and both source variants (candidate B:
all retained baryons source the phantom; H-CB: condensed only), the derivation brackets, Method B (maximum entropy), the
representative mass-scale shapes, controls C1-C4 and MUTATE M-G / M-D. Writes cfg637_profiles.npz (reservoir M_res(<r) per
system/cell, kpc and Msun), cfg637_derive.out and cfg637_derive_results.json. Computes no gate number.
Run from the repository root:  OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG637_derived_reservoir/cfg637_derive.py
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, math, json, time, contextlib
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
for d in (LANES, HERE, os.path.join(LANES, "CFG515_census_edge_resolution"), os.path.join(LANES, "CFG543_group_supply"),
          os.path.join(LANES, "CFG540_vizier2026_bfjr_mhongoose"), os.path.join(LANES, "CFG625_merger_baryon_inputs"),
          os.path.join(REPO, "qwen_claude_field_theory", "closure_2026", "cluster_measurement_audit_2026")):
    sys.path.insert(0, d)
try:
    os.nice(10)
except OSError:
    pass
import cfg637_lib as L                                                      # noqa: E402
import CFG4_common as C4                                                    # noqa: E402
with contextlib.redirect_stdout(io.StringIO()):
    import cfg543_group_supply as G543                                       # noqa: E402
    import cfg625_lib as L625                                                # noqa: E402
    import cluster_audit as CA                                               # noqa: E402
import cfg540_bfjr as C540                                                    # noqa: E402
from cfg597_lib import nu_mono as nu597                                       # noqa: E402
QUICK = os.environ.get("CFG637_QUICK") == "1"
LOG, RES, PROF = [], {"lane": "CFG637", "script": "cfg637_derive", "criteria": "e67940c56"}, {}
CHK = {}
K = L.SI_TO_KPCGYR2


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


P(__doc__.split("Run from")[0].strip())
P(f"  background: Om {L.OM:.4f}, OL {L.OL:.4f}, f_b {L.FB:.5f}, cold/b {L.COLD_PER_B:.4f}, H0 {L.H0:.5f}/Gyr")
BRK = {"P": dict(), "eps0.5": dict(eps=0.5), "q0.05": dict(q=0.05), "q0.2": dict(q=0.2), "uniform": dict(draw_mode="uniform")}


def store(key, I, supply_gate):
    """reservoir M(<r) in gate units: derivation profile x supply_gate / supply_A (FROZEN 1)."""
    s = supply_gate / I.supply_turned
    PROF[key + "|r"] = I.rg.astype(np.float64)
    PROF[key + "|Mres"] = (I.M_res_g * s).astype(np.float64)
    if I.M_res_avg is not None:
        PROF[key + "|Mres_avg"] = (np.interp(I.rg, I.rgrid_avg, I.M_res_avg, right=I.M_res_avg[-1]) * s).astype(np.float64)
    summ = I.summary(); summ.update(supply_gate=supply_gate, scale=s, rta_pred=I.rta_pred,
                                    cons_err=abs(I.drawn + I.M_res_tot - I.supply_turned) / I.supply_turned,
                                    res_frac=I.M_res_tot / I.supply_turned)
    return summ


def maxent(key, I, supply_gate):
    Mfix = I.Mtot_g - I.M_res_g
    if I.M_res_tot <= 0:
        PROF[key.replace("|A|", "|B|") + "|r"] = I.rg.astype(np.float64); PROF[key.replace("|A|", "|B|") + "|Mres"] = 0 * I.rg
        return dict(s2=None, empty=True)
    Mr, s2, E, ok = L.maxent_reservoir(I.rg, Mfix, I.M_res_tot, I.E_res, I.rta)
    PROF[key.replace("|A|", "|B|") + "|r"] = I.rg.astype(np.float64)
    PROF[key.replace("|A|", "|B|") + "|Mres"] = (Mr * supply_gate / I.supply_turned).astype(np.float64)
    return dict(s2=s2, sigma_kms=math.sqrt(s2) / L.KMS, E_reached=E, E_target=I.E_res, converged=ok)


SUMM = {}
# ======================================================================================= groups (63, per group)
P("\n== groups: Method A per group (Hernquist retained core, f_ret 0.10, catchment M_bar/0.10)")
ROWS = G543.read_groups()
if QUICK:
    ROWS = ROWS[::16]
X, M_T, HERN_RE = G543.X, G543.M_T, G543.HERN_RE
for foot, fk in (("canonical", "can"), ("alt", "alt")):
    a0 = C540.FOOT[fk] * K
    for o in ROWS:
        M = 10 ** o["lM"]; ak = o["Re"] / HERN_RE; r = X * ak
        Mta = M / 0.10 / L.FB; supply = L.COLD_PER_B * M / 0.10
        for src, fs in (("B", 1.0), ("HCB", 0.92)):
            for bk, kw in BRK.items():
                if bk != "P" and QUICK:
                    continue
                key = f"G|{o['id']}|{foot}|{src}|A|{bk}"
                I = L.derive(Mta, 0.10, r, M * M_T, fs * M * M_T, a0, C540.nu, N=1600 if bk == "P" else 1000, **kw)
                SUMM[key] = store(key, I, supply)
                if bk == "P":
                    SUMM[key]["maxent"] = maxent(key, I, supply)
    P(f"  [{foot}] {len(ROWS)} groups done ({time.time() - T0:.0f} s)")

# ======================================================================================= X-COP (12 clusters)
P("\n== X-COP: Method A per cluster (audit gas + stars to R200, f_ret 0.90, catchment M_b(<R200)/0.90)")
CL = [CA.load_cluster(p.name) for p in sorted(CA.DATA.iterdir()) if p.is_dir()]
NAMES = [c["name"] for c in CL]
GAS, STARS, MH = CA.profiles(CL, CA.RADII, False)
ETT = json.load(open(os.path.join(REPO, "real_research", "data", "xcop", "xcop_r500_ettori2019.json")))


def loglin_extrap(x, xp, fp):                     # CFG634's function, verbatim
    ok = np.isfinite(fp) & (fp > 0) & (xp > 0)
    xp, fp = np.asarray(xp)[ok], np.asarray(fp)[ok]
    if x <= xp[-1]:
        return float(np.exp(np.interp(np.log(x), np.log(xp), np.log(fp))))
    s = np.polyfit(np.log(xp[-3:]), np.log(fp[-3:]), 1)[0]
    return float(fp[-1] * (x / xp[-1]) ** s)


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
    assert np.all(np.isfinite(gas)) and np.all(np.isfinite(stars)), n
    rr = np.r_[rr, 3e4]; gas = np.r_[gas, gas[-1]]; stars = np.r_[stars, stars[-1]]
    XCORE[n] = (rr, gas, stars)
for foot in ("canonical", "alt"):
    a0 = C4.A0[foot] * K
    for n in (NAMES[:3] if QUICK else NAMES):
        rr, gas, stars = XCORE[n]
        Mb200 = G200[n] + S200[n]; Mta = Mb200 / 0.90 / L.FB; supply = (0.1200 / 0.02237) * Mb200 / 0.90
        for src in ("B", "HCB"):
            Msrc = gas + stars if src == "B" else stars
            for bk, kw in BRK.items():
                if bk != "P" and QUICK:
                    continue
                key = f"X|{n}|{foot}|{src}|A|{bk}"
                I = L.derive(Mta, 0.90, rr, gas + stars, Msrc, a0, C4.nu_mono, **kw)
                SUMM[key] = store(key, I, supply)
                if bk == "P":
                    SUMM[key]["maxent"] = maxent(key, I, supply)
    P(f"  [{foot}] X-COP done ({time.time() - T0:.0f} s)")

# ======================================================================================= Bullet progenitors
P("\n== Bullet: Method A per progenitor (p.Mbar retained, f_ret 1, catchment p.Mb, a_obs = 1/1.296)")
AOBS_B = 1 / 1.296
for var in ("BASE", "B1", "B2", "B3"):
    for ft in ("can", "alt"):
        for role, M200 in (("main", 1.5e15), ("sub", 1.5e14)):
            p = L625.Progenitor625(M200, ft, cloud=(role == "sub"), variant=var)
            Mta = p.Mb / L.FB; supply = 5.364 * p.Mb
            for src in ("B", "HCB"):
                Msrc = p.Mbar if src == "B" else p.Ms
                for bk, kw in BRK.items():
                    if bk != "P" and (var != "B1" or QUICK):
                        continue
                    key = f"BU|{var}_{role}|{ft}|{src}|A|{bk}"
                    I = L.derive(Mta, 1.0, np.maximum(p.r, 1e-3), p.Mbar, Msrc, p.a0, nu597, a_obs=AOBS_B, **kw)
                    SUMM[key] = store(key, I, supply)
                    if bk == "P":
                        SUMM[key]["maxent"] = maxent(key, I, supply)
    P(f"  Bullet {var} done ({time.time() - T0:.0f} s)")

# ======================================================================================= controls + MUTATE
P("\n== controls and MUTATE")
c1 = max(v["cons_err"] for v in SUMM.values()); c1b = max(abs(v["M_turned_over_Mta"] - 1) for v in SUMM.values())
check("C1 mass conservation supply = drawn + reservoir (1e-9)", c1 < 1e-9, f"max rel {c1:.1e}")
kw_ = max(SUMM, key=lambda k: abs(SUMM[k]["M_turned_over_Mta"] - 1))
check("C1b turned-around mass within 1% of M_ta", c1b <= 0.0105, f"max |M_turned/M_ta - 1| {c1b:.4f} ({kw_})")
o = ROWS[len(ROWS) // 2]; M = 10 ** o["lM"]; ak = o["Re"] / HERN_RE; rG = X * ak
repG = (M / 0.10 / L.FB, 0.10, rG, M * M_T, M * M_T, C540.nu)
n0 = "A1795" if "A1795" in NAMES else NAMES[0]
rr, gas, stars = XCORE[n0]; Mb200 = G200[n0] + S200[n0]
repX = (Mb200 / 0.90 / L.FB, 0.90, rr, gas + stars, gas + stars, C4.nu_mono)
repXH = (Mb200 / 0.90 / L.FB, 0.90, rr, gas + stars, stars, C4.nu_mono)
CTRL = {}
# candidate-B sources empty the reservoir in groups and clusters (supply-limited); the H-CB cluster carries one, so M-G / M-D /
# C2 / C4 are evaluated on it as well (the group reservoir is empty under both sources: M-G not applicable there, reported)
for nm, (Mta, fr, r_, Mc, Ms, nu) in (("group " + o["id"] + " (B source)", repG), ("cluster " + n0 + " (B source)", repX),
                                      ("cluster " + n0 + " (H-CB source)", repXH)):
    for foot, a0s in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
        a0 = a0s * K
        I1 = L.derive(Mta, fr, r_, Mc, Ms, a0, nu)
        I2 = L.derive(Mta, fr, r_, Mc, Ms, a0, nu, N=3200)
        Ig = L.derive(Mta, fr, r_, Mc, Ms, a0, nu, selfgrav=False)
        Iu = L.derive(Mta, fr, r_, Mc, Ms, a0, nu, draw_mode="uniform")
        f = lambda I, x: float(np.interp(x * I.rta, I.rg, I.M_res_g) / max(I.M_res_tot, 1e-30))
        fa = lambda I, x: float(np.interp(x * I.rta, I.rgrid_avg, I.M_res_avg) / max(I.M_res_tot, 1e-30))
        xs = (0.02, 0.05, 0.1, 0.3)
        res = dict(N1600={x: f(I1, x) for x in xs}, N3200={x: f(I2, x) for x in xs},
                   selfgrav_off={x: f(Ig, x) for x in xs}, uniform={x: f(Iu, x) for x in xs},
                   timeavg={x: fa(I1, x) for x in xs}, abs_res_frac=I1.M_res_tot / I1.supply_turned,
                   abs_res_frac_gravoff=Ig.M_res_tot / Ig.supply_turned)
        if I1.M_res_tot > 0:
            res["C2_maxdiff"] = max(abs(res["N3200"][x] / res["N1600"][x] - 1) for x in xs)
            res["MG_change_0.1"] = abs(Ig.M_res_tot * f(Ig, 0.1) / (I1.M_res_tot * f(I1, 0.1)) - 1)
            res["MD_change_0.05"] = abs(Iu.M_res_tot * f(Iu, 0.05) / (I1.M_res_tot * f(I1, 0.05)) - 1)
            res["C4_0.05_0.1"] = [fa(I1, 0.05) / f(I1, 0.05), fa(I1, 0.1) / f(I1, 0.1)]
        else:      # the derived reservoir is EMPTY (supply-limited): nothing to perturb; reported as not applicable
            res.update(C2_maxdiff=None, MG_change_0_1=None, MD_change_0_05=None, C4_0_05_0_1=None, empty=True,
                       gravoff_res_frac=Ig.M_res_tot / Ig.supply_turned, N3200_res_frac=I2.M_res_tot / I2.supply_turned,
                       uniform_res_frac=Iu.M_res_tot / Iu.supply_turned)
            res["MG_change_0.1"] = res["MD_change_0.05"] = res["C2_maxdiff"] = None; res["C4_0.05_0.1"] = [None, None]
        CTRL[f"{nm}|{foot}"] = res
        P(f"  {nm} [{foot}] M_res(<x r_ta)/M_res at x 0.02/0.05/0.1/0.3: N1600 " + " ".join(f"{res['N1600'][x]:.4f}" for x in xs)
          + " | N3200 " + " ".join(f"{res['N3200'][x]:.4f}" for x in xs) + " | gravity off " + " ".join(f"{res['selfgrav_off'][x]:.4f}" for x in xs)
          + " | uniform " + " ".join(f"{res['uniform'][x]:.4f}" for x in xs) + " | time-avg " + " ".join(f"{res['timeavg'][x]:.4f}" for x in xs)
          + f" | reservoir/supply {res['abs_res_frac']:.3f}")
fmt = lambda v: "n/a (reservoir empty)" if v is None else f"{v:.3f}"
NE = {k: v for k, v in CTRL.items() if not v.get("empty")}
for k, v in CTRL.items():
    if v.get("empty"):
        P(f"  {k}: derived reservoir EMPTY in the primary run; gravity off / N3200 / uniform reservoir fractions "
          f"{v['gravoff_res_frac']:.3f} / {v['N3200_res_frac']:.3f} / {v['uniform_res_frac']:.3f} (M-G not applicable: nothing to perturb)")
check("M-G reservoir self-gravity off changes M_res(<0.1 r_ta) by > 5% (every control system with a non-empty reservoir, both footings)",
      len(NE) > 0 and all(v["MG_change_0.1"] > 0.05 for v in NE.values()), ", ".join(f"{k}: {fmt(v['MG_change_0.1'])}" for k, v in CTRL.items()))
P("  M-D (reported) uniform draw changes M_res(<0.05 r_ta) by: " + ", ".join(f"{k}: {fmt(v['MD_change_0.05'])}" for k, v in CTRL.items()))
P("  C2 (reported) N1600 vs N3200 max rel diff at 0.02-0.3 r_ta: " + ", ".join(f"{k}: {fmt(v['C2_maxdiff'])}" for k, v in CTRL.items())
  + f" -> {'within 10%' if all(v['C2_maxdiff'] <= 0.10 for v in NE.values()) else 'NOT within 10% (precision-limiting, reported)'}")
P("  C4 (reported) time-avg / phase-mixed at 0.05, 0.1 r_ta: " + ", ".join(f"{k}: {fmt(v['C4_0.05_0.1'][0])}/{fmt(v['C4_0.05_0.1'][1])}" for k, v in CTRL.items()))
# C3 Bertschinger benchmark: no core, no settling, eps 1, q 0.02
xB = np.geomspace(1e-4, 4, 700); z0 = np.zeros_like(xB)
Ib = L.Infall(1e14, 0.0, xB, z0, z0, 9.3603e-11 * K, L.nu_exp, eps=1.0, q=0.02).run().final_profile()
# all matter is cold-like here (f_ret 0: baryons stay on the shells); slope of the reservoir (cold) density
rgx = Ib.rg / Ib.rta; Mr = Ib.M_res_g
rho = np.gradient(Mr, Ib.rg) / (4 * math.pi * Ib.rg ** 2)
sel = (rgx >= 0.03) & (rgx <= 0.15) & (rho > 0)
slope = float(np.polyfit(np.log(rgx[sel]), np.log(rho[sel]), 1)[0])
P(f"  C3 (reported) Bertschinger benchmark (no core, no settling, eps 1, q 0.02, Lambda background): log-slope over 0.03-0.15 r_ta = {slope:.3f} (EdS theory -2.25)")
RES["controls"] = dict(CTRL=CTRL, C3_slope=slope)

# ======================================================================================= mass-scale shapes (report)
P("\n== reservoir shapes by mass scale (Method A primary; M_res(<x r_ta)/M_res and local log-slope of rho_res)")
SHAPES = {}
xs = (0.01, 0.03, 0.1, 0.3, 1.0)
reps = {"galaxy (M_b 6e10, Hernquist a 3 kpc, f_ret 0.10)": (6e10 / 0.10 / L.FB, 0.10, X * 3.0, 6e10 * M_T, 6e10 * M_T, C540.nu),
        f"group ({o['id']}, log M_bar {o['lM']:.2f})": repG, f"cluster ({n0})": repX}
for nm, (Mta, fr, r_, Mc, Ms, nu) in reps.items():
    for foot, a0s in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
        for src in ("B", "HCB"):
            Ms2 = Ms if src == "B" else (0.92 * Ms if "group" in nm else (Ms if "galaxy" in nm else stars))
            I = L.derive(Mta, fr, r_, Mc, Ms2, a0s * K, nu)
            rgx = I.rg / I.rta; rho = np.gradient(I.M_res_g, I.rg) / (4 * math.pi * I.rg ** 2)
            sl = {x: float(np.interp(math.log(x), np.log(rgx[1:-1]), np.gradient(np.log(np.maximum(rho, 1e-300)), np.log(I.rg))[1:-1])) for x in (0.03, 0.1, 0.3)}
            fr_ = {x: float(np.interp(x, rgx, I.M_res_g) / I.M_res_tot) for x in xs}
            ratio_set = {x: float(np.interp(x, rgx, I.M_res_g) / max(np.interp(x, rgx, I.M_set_g + I.M_core_g), 1e-30)) for x in (0.03, 0.1, 0.3)}
            SHAPES[f"{nm}|{foot}|{src}"] = dict(r_ta_kpc=I.rta, res_over_supply=I.M_res_tot / I.supply_turned, frac=fr_, slope=sl,
                                                res_over_baryon_plus_settled=ratio_set, x_edge=I.x_edge)
            P(f"  {nm} [{foot}|{src}] r_ta {I.rta:.0f} kpc, reservoir/supply {I.M_res_tot / I.supply_turned:.3f}, edge x {I.x_edge}"
              + " | frac(<x) " + " ".join(f"{fr_[x]:.4f}" for x in xs) + " | slope at 0.03/0.1/0.3 " + " ".join(f"{sl[x]:+.2f}" for x in sl)
              + " | M_res/(M_b+M_set) at 0.03/0.1/0.3 " + " ".join(f"{ratio_set[x]:.2f}" for x in ratio_set))
RES["shapes"] = SHAPES
RES["summaries"] = SUMM
RES["checks"] = CHK; RES["elapsed_s"] = round(time.time() - T0, 1)
nf = sum(1 for c in CHK.values() if not c["ok"])
P(f"\n{len(CHK) - nf}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
suf = "_QUICK" if QUICK else ""
np.savez_compressed(os.path.join(HERE, f"cfg637_profiles{suf}.npz"), **PROF)
json.dump(C4.jclean(RES), open(os.path.join(HERE, f"cfg637_derive_results{suf}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg637_derive{suf}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nf else 0)
