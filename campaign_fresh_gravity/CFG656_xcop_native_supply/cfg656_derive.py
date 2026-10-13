#!/usr/bin/env python3
"""CFG656 catchments + derivations (FROZEN_CRITERIA.md, c1236bf88). For each X-COP cluster: the framework's own turnaround
catchment (CFG654 native Delta_ta(z), census f_ret) filled with the MEASURED gas (rule P / HI / LO / FLOOR beyond the last data
point) plus stars; supply = (1 - f_b)/f_b x catchment baryons (brackets RET = SHELL placement, NAT = CFG654 native 5.481). Then
CFG637's Method A derivation (cfg637_lib, unchanged) per cluster, both footings, both sources (candidate B / H-CB), plus the
OLD convention (M-OLD), the half-supply MUTATE (M-HALF), the derivation brackets on the primary, and the T2-CEN group bracket.
Writes cfg656_profiles.npz (reservoir M_res(<r), gate units), cfg656_derive.out, cfg656_derive_results.json. Computes no gate number.
Run from the repository root:  OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG656_xcop_native_supply/cfg656_derive.py
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, math, json, time, contextlib
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
D637 = os.path.join(LANES, "CFG637_derived_reservoir")
for d in (LANES, D637, os.path.join(LANES, "CFG515_census_edge_resolution"), os.path.join(LANES, "CFG543_group_supply"),
          os.path.join(LANES, "CFG540_vizier2026_bfjr_mhongoose"),
          os.path.join(REPO, "qwen_claude_field_theory", "closure_2026", "cluster_measurement_audit_2026")):
    sys.path.insert(0, d)
try:
    os.nice(10)
except OSError:
    pass
import cfg637_lib as L                                                      # noqa: E402
import CFG4_common as C4                                                    # noqa: E402
import cfg515_lib as L515                                                   # noqa: E402
with contextlib.redirect_stdout(io.StringIO()):
    import cfg543_group_supply as G543                                       # noqa: E402
    import cluster_audit as CA                                               # noqa: E402
import cfg540_bfjr as C540                                                    # noqa: E402

QUICK = os.environ.get("CFG656_QUICK") == "1"
PARTS = os.environ.get("CFG656_PARTS", "xcop,groups").split(",")
LOG, RES, PROF, CHK = [], {"lane": "CFG656", "script": "cfg656_derive", "criteria": "c1236bf88"}, {}, {}
K = L.SI_TO_KPCGYR2
LIB0 = {k: getattr(L, k) for k in ("h", "OM", "OL", "FB", "COLD_PER_B", "H0", "RHOC0")}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


def set_lib(fb=None, native_bg=False):
    """cfg637_lib module constants: restore, then optionally the native background / a different shell composition."""
    for k, v in LIB0.items():
        setattr(L, k, v)
    if native_bg:
        L.h = 0.67403; L.OM = 0.31285; L.OL = 1 - L.OM
        L.H0 = 100 * L.h * L.KMS / 1000.0; L.RHOC0 = 3 * L.H0 ** 2 / (8 * math.pi * L.G)
    if fb is not None:
        L.FB = fb; L.COLD_PER_B = (1 - fb) / fb


P(__doc__.split("Run from")[0].strip())
FB_ENG = 0.02237 / 0.14237; FB_NAT = 0.15431; FB_HALF = 1.0 / (1.0 + 0.5 * (1 - FB_ENG) / FB_ENG)
P(f"  f_b engine {FB_ENG:.5f} (cold/b {(1 - FB_ENG) / FB_ENG:.4f}); native {FB_NAT} (cold/b {(1 - FB_NAT) / FB_NAT:.4f}); "
  f"half {FB_HALF:.5f} (cold/b {(1 - FB_HALF) / FB_HALF:.4f})")

# ======================================================================================= turnaround radius (CFG654 native)
DTA = json.load(open(os.path.join(LANES, "CFG654_independent_inputs", "cfg654_delta_ta.json")))
DTA361_0 = 11.80562                                       # cfg361 Delta_ta(z=0) as printed in cfg654_delta_ta.out (shift reported only)
OMCB_H2 = 0.31285 * 0.67403 ** 2
RHOM0 = 2.77536627e11 * OMCB_H2 / 1e9                     # Msun / kpc^3


def delta_ta(z):
    return float(np.interp(z, DTA["z"], DTA["D"]))


def r_ta_of(Mta, z):
    return (3 * Mta / (4 * math.pi * delta_ta(z) * RHOM0 * (1 + z) ** 3)) ** (1 / 3)


# ======================================================================================= X-COP data (as CFG634 / CFG637)
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


# ---- OLD convention: CFG637's code, verbatim in substance (M-OLD)
R200 = {n: ETT[n]["R200"] * 1000.0 for n in NAMES}
G200, S200 = {}, {}
for c in CL:
    G200[c["name"]] = loglin_extrap(R200[c["name"]], c["rg"], c["mg"])
    S200[c["name"]] = loglin_extrap(R200[c["name"]], c["rs"], c["ms"]) if c["has_star"] else np.nan
rat200 = np.nanmedian([S200[n] / G200[n] for n in NAMES if np.isfinite(S200[n])])
for n in NAMES:
    if not np.isfinite(S200[n]):
        S200[n] = rat200 * G200[n]
XCORE_OLD = {}
for i, c in enumerate(CL):
    n = c["name"]; R2 = R200[n]
    rr = np.geomspace(1.0, R2, 400)
    gas = np.array([loglin_extrap(x, c["rg"], c["mg"]) for x in np.maximum(rr, c["rg"][0])])
    gas = np.where(rr < c["rg"][0], gas * (rr / c["rg"][0]) ** 2, gas)
    lr = np.log(np.r_[CA.RADII, R2]); rat = np.r_[STARS[i] / GAS[i], S200[n] / G200[n]]
    okr = np.isfinite(rat) & (rat > 0)
    stars = gas * np.interp(np.log(rr), lr[okr], rat[okr])
    rr = np.r_[rr, 3e4]; gas = np.r_[gas, gas[-1]]; stars = np.r_[stars, stars[-1]]
    XCORE_OLD[n] = (rr, gas, stars)


# ---- the declared gas rules beyond r_max
def gas_rule(c, rule):
    ok = np.isfinite(c["mg"]) & (c["mg"] > 0) & (c["rg"] > 0)
    xp, fp = c["rg"][ok], c["mg"][ok]; L_ = np.log(xp); F_ = np.log(fp); rmax = xp[-1]
    s3 = float(np.polyfit(L_[-3:], F_[-3:], 1)[0])
    sel = xp >= c["R500"]
    if sel.sum() < 3:
        sel = np.zeros_like(sel); sel[-3:] = True
    sHI = float(np.polyfit(L_[sel], F_[sel], 1)[0])
    cq, bq, aq = np.polyfit(L_[sel], F_[sel], 2)
    Lm = math.log(rmax)

    def M(r):
        r = np.atleast_1d(np.asarray(r, float)); out = np.empty_like(r)
        inside = r <= rmax
        out[inside] = np.exp(np.interp(np.log(r[inside]), L_, F_))
        x = r[~inside]
        if len(x):
            if rule == "P":
                out[~inside] = fp[-1] * (x / rmax) ** s3
            elif rule == "HI":
                out[~inside] = fp[-1] * (x / rmax) ** sHI
            elif rule == "FLOOR":
                out[~inside] = fp[-1]
            elif rule == "LO":
                lx = np.log(x)
                # integrate d ln M / d ln r = s(L) = max(min(s3, b + 2cL), 0) from Lm (exact on a fine grid)
                Lg = np.linspace(Lm, float(lx.max()), 4000)
                sg = np.maximum(np.minimum(s3, bq + 2 * cq * Lg), 0.0)
                lnM = F_[-1] + np.r_[0.0, np.cumsum(0.5 * (sg[1:] + sg[:-1]) * np.diff(Lg))]
                out[~inside] = np.exp(np.interp(lx, Lg, lnM))
            else:
                raise ValueError(rule)
        return out
    return M, dict(rmax=float(rmax), s_last3=s3, s_HI=sHI, quad_b=float(bq), quad_c=float(cq))


def star_rule(c, rule):
    if not c["has_star"]:
        return None
    ok = np.isfinite(c["ms"]) & (c["ms"] > 0)
    xp, fp = c["rs"][ok], c["ms"][ok]

    def S(r):
        r = np.atleast_1d(np.asarray(r, float))
        if rule == "FLOOR":
            return np.exp(np.interp(np.log(r), np.log(xp), np.log(fp)))       # flat beyond the last stellar point
        return np.array([loglin_extrap(x, xp, fp) for x in r])
    return S


GRULE = {}
for c in CL:
    for rule in ("P", "HI", "LO", "FLOOR"):
        GRULE[(c["name"], rule)] = (gas_rule(c, rule), star_rule(c, rule))


def stars_at(n, rule, r):
    (Mg, _), S = GRULE[(n, rule)]
    if S is not None:
        return float(S(r)[0])
    ratios = []
    for c2 in CL:
        if c2["has_star"]:
            (Mg2, _), S2 = GRULE[(c2["name"], rule)]
            ratios.append(float(S2(r)[0] / Mg2(r)[0]))
    return float(np.median(ratios)) * float(Mg(r)[0])


def Mb_ret(n, rule, r):
    (Mg, _), _ = GRULE[(n, rule)]
    return float(Mg(r)[0]) + stars_at(n, rule, r)


def catchment(n, rule="P", fb=FB_ENG, fret_mode="census"):
    z = ETT[n]["z"]
    rt = 2.0 * R200[n]
    for it in range(200):
        mb = Mb_ret(n, rule, rt)
        f = L515.fret_census(mb)[0] if fret_mode == "census" else 1.0
        Mcat = mb / f; Mta = Mcat / fb
        rn = r_ta_of(Mta, z)
        if abs(rn / rt - 1) < 1e-10:
            rt = rn; break
        rt = rn
    else:
        raise RuntimeError(f"catchment fixed point did not converge: {n} {rule}")
    mb = Mb_ret(n, rule, rt); f = L515.fret_census(mb)[0] if fret_mode == "census" else 1.0
    Mcat = mb / f; Mta = Mcat / fb
    return dict(z=z, r_ta=rt, r_ta_over_R200=rt / R200[n], Mb_ret=mb, gas_ret=float(GRULE[(n, rule)][0][0](rt)[0]),
                stars_ret=stars_at(n, rule, rt), f_ret=f, M_b_catch=Mcat, M_ta=Mta, supply=(1 - fb) / fb * Mcat, iters=it + 1,
                Delta_ta=delta_ta(z))


def core_profile(i, n, rule, rt):
    """retained-core cumulative gas, stars on 1 kpc .. r_ta (rule), flat beyond (as CFG637's construction)."""
    c = CL[i]; (Mg, _), _ = GRULE[(n, rule)]
    rr = np.geomspace(1.0, rt, 500)
    gas = Mg(np.maximum(rr, c["rg"][0]))
    gas = np.where(rr < c["rg"][0], gas * (rr / c["rg"][0]) ** 2, gas)
    lr = np.log(np.r_[CA.RADII, rt]); rat = np.r_[STARS[i] / GAS[i], stars_at(n, rule, rt) / float(Mg(rt)[0])]
    okr = np.isfinite(rat) & (rat > 0)
    o = np.argsort(lr[okr])
    stars = gas * np.interp(np.log(rr), lr[okr][o], rat[okr][o])
    assert np.all(np.isfinite(gas)) and np.all(np.isfinite(stars)), n
    rr = np.r_[rr, 3e4]; gas = np.r_[gas, gas[-1]]; stars = np.r_[stars, stars[-1]]
    return rr, gas, stars


SUMM = {}


def store(key, I, supply_gate):
    s = supply_gate / I.supply_turned
    PROF[key + "|r"] = I.rg.astype(np.float64)
    PROF[key + "|Mres"] = (I.M_res_g * s).astype(np.float64)
    summ = I.summary(); summ.update(supply_gate=supply_gate, scale=s, rta_pred=I.rta_pred,
                                    cons_err=abs(I.drawn + I.M_res_tot - I.supply_turned) / I.supply_turned,
                                    res_frac=I.M_res_tot / I.supply_turned)
    SUMM[key] = summ
    return summ


# ======================================================================================= catchments (all brackets)
CAT = {}
if "xcop" in PARTS:
    P("\n== X-COP turnaround catchments (CFG654 native Delta_ta(z); census f_ret; measured gas + stars)")
    P(f"  cfg361 Delta_ta(0) {DTA361_0} vs native {DTA['D'][0]:.4f}: r_ta shift {(DTA361_0 / DTA['D'][0]) ** (1 / 3) - 1:+.4%} at fixed M_ta (reported only)")
    for n in NAMES:
        Mb200 = G200[n] + S200[n]
        CAT[(n, "OLD")] = dict(M_b_catch=Mb200 / 0.90, supply=(0.1200 / 0.02237) * Mb200 / 0.90, M_ta=Mb200 / 0.90 / L.FB, f_ret=0.90,
                               Mb_R200=Mb200, R200=R200[n])
        for rule in ("P", "HI", "LO", "FLOOR"):
            CAT[(n, rule)] = catchment(n, rule)
        CAT[(n, "RET")] = catchment(n, "P", fret_mode="one")
        CAT[(n, "NAT")] = catchment(n, "P", fb=FB_NAT)
        cP = CAT[(n, "P")]
        CAT[(n, "HALF")] = dict(cP, supply=(1 - FB_HALF) / FB_HALF * cP["M_b_catch"], M_ta=cP["M_b_catch"] / FB_HALF)
        gi = GRULE[(n, "P")][0][1]
        P(f"  {n:8s} z {cP['z']:.4f} r_ta {cP['r_ta']:.0f} kpc ({cP['r_ta_over_R200']:.2f} R200; gas data to {gi['rmax']:.0f}, s3 {gi['s_last3']:.3f}, "
          f"sHI {gi['s_HI']:.3f}) | Mb_ret(<r_ta) {cP['Mb_ret']:.3e} (gas {cP['gas_ret']:.3e}, stars {cP['stars_ret']:.3e}), f_ret {cP['f_ret']:.3f} "
          f"| supply P {cP['supply']:.3e} vs OLD {CAT[(n, 'OLD')]['supply']:.3e} (x{cP['supply'] / CAT[(n, 'OLD')]['supply']:.2f}); "
          + " ".join(f"{b} x{CAT[(n, b)]['supply'] / CAT[(n, 'OLD')]['supply']:.2f}" for b in ("HI", "LO", "FLOOR", "RET", "NAT")))
    RES["catchments"] = {f"{n}|{b}": v for (n, b), v in CAT.items()}
    fr = [CAT[(n, 'P')]['f_ret'] for n in NAMES]
    P(f"  census f_ret (primary): {min(fr):.3f}-{max(fr):.3f}; fixed points converged in <= {max(CAT[(n, b)].get('iters', 0) for n in NAMES for b in ('P', 'HI', 'LO', 'FLOOR', 'RET', 'NAT'))} iterations")
    check("C-FP catchment fixed points converged (1e-10)", True, "all converged (a non-converged one raises)")

# ======================================================================================= X-COP derivations
BRK = {"eps0.5": dict(eps=0.5), "q0.05": dict(q=0.05), "q0.2": dict(q=0.2), "uniform": dict(draw_mode="uniform")}
if "xcop" in PARTS:
    MODES = ["OLD", "P", "HI", "LO", "FLOOR", "RET", "NAT", "HALF"] + [f"P_{b}" for b in BRK]
    if QUICK:
        MODES = ["OLD", "P", "HALF"]
    for mode in MODES:
        base = mode.split("_")[0]; kw = BRK.get(mode[2:], {}) if mode.startswith("P_") else {}
        for foot in ("canonical", "alt"):
            a0 = C4.A0[foot] * K
            for i, n in enumerate(NAMES[:2] if QUICK else NAMES):
                ct = CAT[(n, base)]
                if base == "OLD":
                    set_lib(); rr, gas, stars = XCORE_OLD[n]; fret = 0.90
                else:
                    rule = base if base in ("P", "HI", "LO", "FLOOR") else "P"
                    rr, gas, stars = core_profile(i, n, rule, ct["r_ta"])
                    fret = 1.0 if base == "RET" else ct["f_ret"]
                    set_lib(fb=FB_NAT, native_bg=True) if base == "NAT" else (set_lib(fb=FB_HALF) if base == "HALF" else set_lib())
                if f"XC|{base}|{n}|r" not in PROF:
                    PROF[f"XC|{base}|{n}|r"], PROF[f"XC|{base}|{n}|gas"], PROF[f"XC|{base}|{n}|stars"] = rr, gas, stars
                for src in ("B", "HCB"):
                    Msrc = gas + stars if src == "B" else stars
                    I = L.derive(ct["M_ta"], fret, rr, gas + stars, Msrc, a0, C4.nu_mono, **kw)
                    sm = store(f"X|{mode}|{n}|{foot}|{src}", I, ct["supply"])
                    sm.update(r_ta_catch=ct.get("r_ta"))
            set_lib()
            P(f"  X-COP {mode} [{foot}] done ({time.time() - T0:.0f} s): reservoir/supply B "
              + " ".join(f"{SUMM[f'X|{mode}|{n}|{foot}|B']['res_frac']:.2f}" for n in (NAMES[:2] if QUICK else NAMES))
              + " | H-CB " + " ".join(f"{SUMM[f'X|{mode}|{n}|{foot}|HCB']['res_frac']:.2f}" for n in (NAMES[:2] if QUICK else NAMES)))
    # derivation r_ta vs catchment r_ta (primary)
    rr_ = [SUMM[f"X|P|{n}|canonical|B"]["r_ta_kpc"] / CAT[(n, "P")]["r_ta"] for n in (NAMES[:2] if QUICK else NAMES)]
    P(f"  C-FP (reported) derivation r_ta / catchment r_ta (primary, canonical, B): {min(rr_):.3f}-{max(rr_):.3f} "
      f"(the derivation uses a_obs = 1 and cfg637_lib's background; the catchment uses each cluster's z and CFG654's native table)")

# ======================================================================================= groups: T2-CEN bracket
if "groups" in PARTS:
    P("\n== groups: T2-CEN bracket (census f_ret per group, catchment M_bar/f_ret)")
    set_lib()
    ROWS = G543.read_groups()
    if QUICK:
        ROWS = ROWS[::16]
    X, M_T, HERN_RE = G543.X, G543.M_T, G543.HERN_RE
    FCEN = {}
    for foot, fk in (("canonical", "can"), ("alt", "alt")):
        a0 = C540.FOOT[fk] * K
        for o in ROWS:
            M = 10 ** o["lM"]; ak = o["Re"] / HERN_RE; r = X * ak
            f = L515.fret_census(M)[0]; FCEN[o["id"]] = f
            Mta = M / f / L.FB; supply = L.COLD_PER_B * M / f
            for src, fs in (("B", 1.0), ("HCB", 0.92)):
                I = L.derive(Mta, f, r, M * M_T, fs * M * M_T, a0, C540.nu)
                store(f"G|CEN|{o['id']}|{foot}|{src}", I, supply)
        mxB = max(SUMM["G|CEN|%s|%s|B" % (o["id"], foot)]["res_frac"] for o in ROWS)
        mxH = max(SUMM["G|CEN|%s|%s|HCB" % (o["id"], foot)]["res_frac"] for o in ROWS)
        P(f"  [{foot}] {len(ROWS)} groups done ({time.time() - T0:.0f} s); census f_ret {min(FCEN.values()):.3f}-{max(FCEN.values()):.3f}; "
          f"reservoir/supply max B {mxB:.3f}, H-CB {mxH:.3f}")
    RES["group_fret_census"] = FCEN

# ======================================================================================= controls
c1 = max(v["cons_err"] for v in SUMM.values()); c1b = max(abs(v["M_turned_over_Mta"] - 1) for v in SUMM.values())
kw_ = max(SUMM, key=lambda k: abs(SUMM[k]["M_turned_over_Mta"] - 1))
check("C1 mass conservation supply = drawn + reservoir (1e-9)", c1 < 1e-9, f"max rel {c1:.1e}")
check("C1b turned-around mass within 1.05% of M_ta", c1b <= 0.0105, f"max |M_turned/M_ta - 1| {c1b:.4f} ({kw_})")
RES["summaries"] = SUMM; RES["checks"] = CHK; RES["elapsed_s"] = round(time.time() - T0, 1)
nf = sum(1 for c in CHK.values() if not c["ok"])
P(f"\n{len(CHK) - nf}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
suf = ("_QUICK" if QUICK else "") + ("" if PARTS == ["xcop", "groups"] else "_" + "_".join(PARTS))
np.savez_compressed(os.path.join(HERE, f"cfg656_profiles{suf}.npz"), **PROF)
json.dump(C4.jclean(RES), open(os.path.join(HERE, f"cfg656_derive_results{suf}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg656_derive{suf}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nf else 0)
