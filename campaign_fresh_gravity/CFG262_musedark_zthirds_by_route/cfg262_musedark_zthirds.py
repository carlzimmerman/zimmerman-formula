#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG262 -- MUSE-DARK implied-a0 levels (CFG223's s*) in redshift thirds, by baryon route (i fitted DC14 masses / ii SED + H2 / iii SED) and velocity reading (b: no pressure, a LOWER bound; bD: with the asymmetric-drift term).

Criteria frozen and committed before this script existed: campaign_fresh_gravity/CFG262_musedark_zthirds_by_route/FROZEN_CRITERIA.md (1c1e4fe44) + ADDENDUM_1.md.
  data      the CFG236 chain (S = 109) and the 126 external true_Vrot.dat files (read-only; hash-checked); equal-count thirds of S by z (37 / 36 / 36).
  machinery CFG236_common (routes in the R199 construction, gperp_reading, thirds, load_dat, verify_hashes, boot_median) and CFG229's a0implied.implied (CFG223's estimator, verbatim), nu_mono, canonical a0.
  STAGE=A   the blind pre-flight: no g_perp, D, s* or median a0 of any third is printed or formed from the real velocities.
  STAGE=B   the measurement (once, after stage A and this script are committed); STAGE=B MUTATE=1 plants the law at s = 2; STAGE=B SELFTEST=1 fabricates g_perp.
Run: STAGE=A python3 .../cfg262_musedark_zthirds.py ; STAGE=B python3 ... ; STAGE=B MUTATE=1 python3 ...
kappa = 1/2 is FITTED.  No verdict words.
"""
import os, sys, io, json, math, time, zlib, csv, contextlib
sys.dont_write_bytecode = True
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
for p in (CFG, os.path.join(CFG, "CFG236_musedark_referee"), os.path.join(CFG, "CFG229_class_m_gold")):
    sys.path.insert(0, p)
STAGE = os.environ.get("STAGE", "").strip().upper()
MUTATE = os.environ.get("MUTATE", "0") == "1"
SELFTEST = os.environ.get("SELFTEST", "0") == "1"
assert STAGE in ("A", "B"), "set STAGE=A or STAGE=B"
assert not ((MUTATE or SELFTEST) and STAGE == "A") and not (MUTATE and SELFTEST), "MUTATE / SELFTEST apply to stage B, one at a time"
SFX = f"_stage{STAGE}" + ("_MUTATE1" if MUTATE else "") + ("_SELFTEST" if SELFTEST else "")
LOG, CHK, NUM = [], [], {}


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def check(name, detail, ok, load_bearing=True):
    CHK.append((name, bool(ok), load_bearing))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}")


P(__doc__.split("Run:")[0].strip())
P(f"\nSTAGE {STAGE}" + ("  *** MUTATE=1: the law at s = 2 planted on every galaxy's own baryons (D scaled by nu(y/2)/nu(y)) ***" if MUTATE else "")
  + ("  *** SELFTEST: FABRICATED g_perp (route iii on the law at s_true = 1.7 plus 0.3 dex scatter); debugging only ***" if SELFTEST else ""))

import CFG236_common as c
import a0implied as AI
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as K4
NU, NUP2 = K4.nu_mono, K4.nu_p2
A0C, A0A = 9.3603e-11, 1.1312e-10
CONV = c.CONV
FLOOR = 0.001
B_BOOT = 10000
S_TRUE_SELF = 1.7

# ------------------------------------------------------------------ data
T = c.load_numeric()
idx, cnt = c.sample(T)
C = c.get_cols(T, idx)
z = C["z"]; NG = len(z)
TH = c.thirds(z)
THN = {f"z{k + 1}": TH[k] for k in range(3)}
dat = c.load_dat(T, idx)                                    # v1, s1, v22r, s22r  (read; only isfinite counted at stage A)
READS = {"b": dict(reading="b", drift=None), "bD": dict(reading="b", drift="D1"), "a": dict(reading="a", drift=None), "aD": dict(reading="a", drift="D1")}
ROUTES = ("i", "ii", "iii")
J223 = json.load(open(os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_results.json")))["curves"]
LAWS = {"FLAT": lambda zz: 1.0, "H(z)": lambda zz: float(np.interp(zz, J223["z"], J223["H(z)"])), "PROXY": lambda zz: float(np.interp(zz, J223["z"], J223["PROXY"]))}
ZMED = {k: float(np.median(z[v])) for k, v in THN.items()}
P(f"S = {NG} galaxies; thirds " + "; ".join(f"{k} N={len(v)} z_med={ZMED[k]:.3f}" for k, v in THN.items()))


def gperp_of(rd, datx=None):
    d_ = dat if datx is None else datx
    return c.gperp_reading(d_["v1"], C["Re"], C["incl"], READS[rd]["reading"], sig1=d_["s1"], drift=READS[rd]["drift"])


def routes_of(gp, **extra):
    return c.routes(C, dict(mode="R199", gperp=gp, **extra))


def s_star(D, gb, nu=NU, a0=A0C):
    ls, unb = AI.implied(D, gb, nu, a0)
    return float(ls[0]), bool(unb[0])


def boot_s(D, gb, label, B=B_BOOT, nu=NU):
    rng = np.random.default_rng(zlib.crc32(label.encode()) % 100000)
    n = len(D)
    ib = rng.integers(0, n, size=(B, n))
    lsb, ub = AI.implied(D[ib], gb[ib], nu, A0C)
    return lsb, ub


def pct(ls_b):
    return {k: float(v) for k, v in zip(("lo68", "hi68", "lo95", "hi95"), np.percentile(ls_b, [16, 84, 2.5, 97.5]))}


def s_of(ls, unb):
    return FLOOR if unb else 10 ** ls


# ================================================================== STAGE A
if STAGE == "A":
    P("\nSTAGE A  THE BLIND PRE-FLIGHT (no g_perp, D, s* or median a0 of any third is formed from the real velocities)")
    # ---------------------------------------------------------------- C1 hashes, C2 chain, C3 route identity, C4 estimator identity
    hv = c.verify_hashes()
    check("C1 CONTROL: the 882 run files and 9 catalogue files match their manifests (882 / 882, 9 / 9)", f"files ok {hv['n_ok']}/{hv['n_listed']} (bad {hv['n_bad']}, missing {hv['n_missing']}); catalogue ok {hv['cat_ok']} (bad {hv['cat_bad']}, missing {hv['cat_missing']})",
          hv["n_ok"] == 882 and hv["n_listed"] == 882 and hv["n_bad"] == 0 and hv["n_missing"] == 0 and hv["cat_ok"] == 9 and hv["cat_bad"] == 0 and hv["cat_missing"] == 0)
    check("C2 CONTROL: the sample chain counts 126 / 124 / 14 (15 in 126) / 110 / 109 and the thirds N = 37 / 36 / 36", f"{cnt}; thirds {[len(v) for v in TH]}",
          (cnt["n_rows"], cnt["n_finite"], cnt["bulge_in_finite"], cnt["bulge_all"], cnt["n_disc"], cnt["n_S"]) == (126, 124, 14, 15, 110, 109) and [len(v) for v in TH] == [37, 36, 36])
    C_id = dict(C); C_id["logMsed"] = C["logMfit"]
    Rid = c.routes(C_id, dict(mode="R199", gperp=np.ones(NG), mu_fac=0.0))
    dd = max(float(np.max(np.abs(Rid["gb_ii"] / Rid["gb_i"] - 1))), float(np.max(np.abs(Rid["gb_iii"] / Rid["gb_i"] - 1))))
    check("C3 CONTROL: route identity -- with M*_SED := M_fit and mu := 0, routes (ii) and (iii) equal route (i) (rho = 1 exactly)", f"max relative deviation {dd:.1e}", dd < 1e-12)
    src223 = open(os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_a0_over_time.py")).read()
    seg = src223[src223.index("LO_LS, HI_LS, NIT"):src223.index("_IDX = {}")]
    ns223 = {"np": np}
    exec(compile(seg, "cfg223_a0_over_time.py", "exec"), ns223)
    rr = np.random.default_rng(1234); same = True
    for _ in range(200):
        Dq = 10 ** rr.uniform(-0.3, 0.9, size=(5, 7)); gq = 10 ** rr.uniform(-11, -8, size=(5, 7))
        a1, u1 = ns223["implied"](Dq, gq, NU, A0C); a2, u2 = AI.implied(Dq, gq, NU, A0C)
        same = same and np.array_equal(a1, a2) and np.array_equal(u1, u2)
    check("C4 CONTROL: the imported implied-a0 estimator equals CFG223's original bit for bit on 200 random sets", f"identical {same}", bool(same))

    # ---------------------------------------------------------------- velocity-free baryon side (R198 mode: thin-disc baryons of each route; D from fDM and M_fit)
    R198 = c.routes(C, dict(mode="R198"))
    GB = {r: R198["gb_" + r] * CONV for r in ROUTES}                       # m s^-2, velocity-free
    # route (i) in the law world: D_i = 1/(1 - fDM), y_i = nu^-1(D_i)
    Di = 1.0 / (1.0 - C["fDM"])
    yi = c.invert(Di, NU)
    GBW = {"i": yi * A0C, "ii": GB["ii"], "iii": GB["iii"]}                 # the noiseless world's baryon accelerations (law at s = 1 for route i by construction)

    # ---------------------------------------------------------------- C5 noiseless identity
    d5 = 0.0
    for r in ROUTES:
        for k, t in THN.items():
            g = GBW[r][t]
            for st in (0.5, 1.0, 2.5):
                D = NU(g / (A0C * st))
                ls, unb = s_star(D, g)
                d5 = max(d5, abs(ls - math.log10(st)) if not unb else 9.0)
    check("C5 CONTROL: the noiseless world D_i = nu(g_bar,i / (a0 s_true)) returns s_true to 1e-6 dex for s_true = 0.5, 1, 2.5, each route's baryon side and each third", f"max |d log10 s| {d5:.1e}", d5 < 1e-6)

    # ---------------------------------------------------------------- C6 counts only
    fin_v = np.isfinite(dat["v1"]); fin_s = np.isfinite(dat["s1"]); fin_i = np.isfinite(C["incl"])
    P("  C6 counts only (no value printed): finite v_f(R_e) / sigma_1 / inclination / D1 reading per third: " + "; ".join(f"{k}: {int(fin_v[t].sum())}/{int(fin_s[t].sum())}/{int(fin_i[t].sum())}/{int((fin_v & fin_s & fin_i)[t].sum())} of {len(t)}" for k, t in THN.items()))
    n_all = int((fin_v & fin_s & fin_i).sum())
    check("C6 CONTROL (counts): the D1 reading is finite for every galaxy of S (109 of 109) -- if not, the rows' N is reported per third", f"{n_all} of {NG}", n_all >= 100, load_bearing=False)

    # ---------------------------------------------------------------- C7 coverage on a noiseless world with 0.3 dex scatter on log g_obs (about 0.6 dex in the deep a0)
    rng7 = np.random.default_rng(262)
    cov = {"68": 0, "95": 0}; nd = 0
    t0 = THN["z1"]; g0 = GBW["iii"][t0]
    for it in range(400):
        sel = rng7.choice(len(t0), size=36, replace=False)
        g = g0[sel]; Dn = NU(g / A0C) * 10 ** rng7.normal(0, 0.3, size=len(g))
        ls, unb = s_star(Dn, g)
        ib = rng7.integers(0, 36, size=(1000, 36))
        lsb, ub = AI.implied(Dn[ib], g[ib], NU, A0C)
        pr = pct(lsb)
        if not unb:
            nd += 1
            cov["68"] += (pr["lo68"] <= 0.0 <= pr["hi68"]); cov["95"] += (pr["lo95"] <= 0.0 <= pr["hi95"])
    c68, c95 = cov["68"] / max(nd, 1), cov["95"] / max(nd, 1)
    check("C7 CONTROL: bootstrap coverage (400 draws of N = 36, noiseless world + 0.3 dex scatter on g_obs): >= 60 % at 68 % and >= 88 % at 95 %", f"68 %: {c68:.3f}, 95 %: {c95:.3f} (draws with a root {nd})", c68 >= 0.60 and c95 >= 0.88)

    # ---------------------------------------------------------------- A1 levers (noiseless world)
    P("\nA1  BARYON LEVER d log10 s*/d(baryon dex) in the noiseless world (law at s = 1 on each route's baryon side; y quantiles 16/50/84)")
    LEV = {}
    for r in ROUTES:
        for k, t in THN.items():
            g = GBW[r][t]
            Dw = NU(g / A0C)
            lv, fl = AI.lever(Dw, g, NU, A0C)
            y = g / A0C
            LEV[(r, k)] = float(lv[0]) if not fl[0] else float("nan")
            P(f"    route ({r:3s}) {k}: y = {np.round(np.percentile(y, [16, 50, 84]), 3).tolist()}  lever {LEV[(r, k)]:+.3f}{' (no root)' if fl[0] else ''}")
    # ---------------------------------------------------------------- A2 no-root forecast
    P("\nA2  NO-ROOT FORECAST: the impossibility proxy (half the route's disc mass + pi R_e^2 Sigma_HI above the model's log_Mdyn; log_Mdyn read as the mass within R_e, unverified); rule NO ROOT LIKELY iff >= 0.50")
    mu = c.mu_mol(z, C["logMsed"])
    Mgas = np.pi * C["Re"] ** 2 * 1e6 * C["Sig"]
    PROXY = {}
    for r, Mb in (("i", 10 ** C["logMfit"]), ("ii", 10 ** C["logMsed"] * (1 + mu)), ("iii", 10 ** C["logMsed"])):
        base = 0.5 * Mb + Mgas
        for k, t in THN.items():
            m_ = np.isfinite(C["logMdyn"][t])
            PROXY[(r, k)] = float(np.mean(np.log10(base[t][m_]) > C["logMdyn"][t][m_]))
        P(f"    route ({r:3s}): fraction by third " + " / ".join(f"{PROXY[(r, k)]:.2f}" for k in THN) + "   -> " + ", ".join(f"{k}: {'NO ROOT LIKELY' if PROXY[(r, k)] >= 0.5 else 'root expected'}" for k in THN))
    # ---------------------------------------------------------------- A3 precision forecast
    SD_F = 1.2533 * 0.6 / math.sqrt(36)
    P(f"\nA3  PRECISION FORECAST (planning scatter 0.6 dex per galaxy, N = 36): SD of log10 s* = {SD_F:.3f} dex")
    # ---------------------------------------------------------------- A4 z-dependent calibration drifts (velocity-free: R198-mode baryons, the analyst's baryons shifted by the drift)
    P("\nA4  CALIBRATION DRIFTS on the thirds' relative levels (noiseless world at s = 1; the analyst's baryons carry tau = +-0.25 dex/z (SED mass) or t_H = +-0.3 dex/z (H2 tilt); d = log s*(z3) - log s*(z1))")
    DRIFT = {}
    for r in ("ii", "iii"):
        g_true = GBW[r]
        gobs_w = g_true * NU(g_true / A0C)
        for nm, cfgv in (("tau+0.25", dict(tau=0.25)), ("tau-0.25", dict(tau=-0.25)), ("tH+0.3", dict(tH=0.3)), ("tH-0.3", dict(tH=-0.3))):
            if r == "iii" and nm.startswith("tH"):
                continue
            Rd_ = c.routes(C, dict(mode="R198", **cfgv))
            gb_a = Rd_["gb_" + r] * CONV
            ls_ = {}
            for k, t in THN.items():
                ls_[k] = s_star(gobs_w[t] / gb_a[t], gb_a[t])
            d = ls_["z3"][0] - ls_["z1"][0]
            DRIFT[(r, nm)] = dict(ls=ls_, d=d)
            P(f"    route ({r:3s}) {nm:9s}: log10 s* per third {[round(ls_[k][0], 3) for k in THN]}{' (no root: ' + ','.join(k for k in THN if ls_[k][1]) + ')' if any(ls_[k][1] for k in THN) else ''}  d(z3 - z1) = {d:+.3f}")
    # ---------------------------------------------------------------- A5 FLAT versus H(z)
    P("\nA5  FLAT versus H(z) from the thirds' levels (the rival's expected change in log10 s* from z1 to z3 against 2 sqrt(2 SD^2 + drift^2))")
    rv = math.log10(LAWS["H(z)"](ZMED["z3"]) / LAWS["H(z)"](ZMED["z1"]))
    A5 = {}
    for r in ROUTES:
        dr = max([abs(v["d"]) for (rr_, nm), v in DRIFT.items() if rr_ == r] + [0.0])
        thr = 2 * math.sqrt(2 * SD_F ** 2 + dr ** 2)
        A5[r] = dict(rival=rv, drift=dr, thr=thr, possible_sys=bool(abs(rv) >= thr), possible_stat=bool(abs(rv) >= 2 * math.sqrt(2) * SD_F))
        P(f"    route ({r:3s}): rival d = {rv:+.3f}; max |drift| {dr:.3f}; threshold {thr:.3f}; POSSIBLE_STAT {A5[r]['possible_stat']}; POSSIBLE_SYS {A5[r]['possible_sys']}")
    # ---------------------------------------------------------------- decisions and hand estimates
    pfd1 = all(ok for n, ok, lb in CHK if lb)
    P("\nDECISIONS (the frozen map)")
    P(f"  PF-D1 ESTIMATOR VALIDATED: {pfd1}")
    P("  PF-D2 ROOT FORECAST: " + "; ".join(f"({r}, {k}) {'NO ROOT LIKELY' if PROXY[(r, k)] >= 0.5 else 'root'}" for r in ROUTES for k in THN))
    P("  PF-D3 DRAWABLE rows: " + ", ".join(f"({r}, {k})" for r in ROUTES for k in THN if pfd1 and PROXY[(r, k)] < 0.5) + "; floor triangles: " + (", ".join(f"({r}, {k})" for r in ROUTES for k in THN if PROXY[(r, k)] >= 0.5) or "none"))
    P("  PF-D4 FLAT versus H(z) from the thirds' levels: " + "; ".join(f"route ({r}) {'POSSIBLE_SYS' if A5[r]['possible_sys'] else 'NOT POSSIBLE'}" for r in ROUTES))
    P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 8) scored (HE3, HE6-HE8 are scored at stage B):")
    he = {}
    he["HE1"] = [(r, k) for r in ROUTES for k in THN if PROXY[(r, k)] >= 0.5] == [("ii", "z3")]
    he["HE2"] = all(-1.6 <= LEV[("i", k)] <= -0.9 for k in THN) and all(-4.0 <= LEV[(r, k)] <= -1.0 for r in ("ii", "iii") for k in THN if np.isfinite(LEV[(r, k)]))
    he["HE4"] = all(0.2 <= abs(DRIFT[(r, "tau+0.25")]["d"]) <= 0.5 for r in ("ii", "iii") if not any(DRIFT[(r, "tau+0.25")]["ls"][k][1] for k in THN))
    he["HE5"] = (not A5["ii"]["possible_sys"]) and (not A5["iii"]["possible_sys"]) and A5["i"]["possible_sys"]
    for k, v in he.items():
        P(f"    {k}: {'hit' if v else 'MISS (kept as it falls)'}")
    NUM.update(counts=cnt, lever={f"{r}|{k}": v for (r, k), v in LEV.items()}, proxy={f"{r}|{k}": v for (r, k), v in PROXY.items()}, drift={f"{r}|{nm}": dict(d=v["d"], ls={k: list(x) for k, x in v["ls"].items()}) for (r, nm), v in DRIFT.items()},
               a5=A5, sd_forecast=SD_F, coverage=dict(c68=c68, c95=c95, n=nd), hand_estimates=he, pf=dict(PF_D1=bool(pfd1)), z_med=ZMED)

# ================================================================== STAGE B
if STAGE == "B":
    P("\nSTAGE B  THE MEASUREMENT" + (" (SELFTEST)" if SELFTEST else "") + (" (MUTATE: planted s = 2)" if MUTATE else ""))
    datx = dict(dat)
    if SELFTEST:
        # fabricate g_perp so that route (iii) sits on the law at s_true with 0.3 dex scatter (D_iii does not depend on g_perp in the R199 construction)
        R0 = routes_of(np.ones(NG))
        D3 = R0["D_iii"]; rho3 = R0["gb_iii"] / R0["gb_i"]
        ys = c.invert(np.where(D3 > 1.05, D3, np.nan), NU)
        rngS = np.random.default_rng(2620)
        ys = np.where(np.isfinite(ys), ys, np.nanmedian(ys))
        gfab = (A0C * S_TRUE_SELF * ys) / (1.0 - C["fDM"]) / rho3 / CONV            # (km/s)^2/kpc
        gfab = gfab * 10 ** rngS.normal(0, 0.3, size=NG)
        datx["v1"] = np.sqrt(gfab * C["Re"]) * np.sin(np.radians(C["incl"]))        # reading b: v_perp = v1 / sin i
        datx["s1"] = np.zeros(NG)                                                    # the drift term vanishes
        P(f"SELFTEST: fabricated v_f so that route (iii) follows the law at s_true = {S_TRUE_SELF} with 0.3 dex scatter on g_perp (D1 reduces to b)")
    # per reading: routes object
    RO = {}
    for rd in READS:
        gp = gperp_of(rd, datx)
        RO[rd] = routes_of(gp)
    if MUTATE:
        for rd in READS:
            for r in ROUTES:
                gb = RO[rd]["gb_" + r] * CONV
                D = RO[rd]["D_" + r]
                RO[rd]["D_" + r] = D * NU(gb / (A0C * 2.0)) / NU(gb / A0C)
    P(f"  routes built ({time.time() - T0:.0f} s)")
    RES = {}

    def row_levels(rd, r, k, extra=None, nu=NU):
        Rx = RO[rd] if extra is None else routes_of(gperp_of(rd, datx), **extra)
        t = THN[k]
        D = Rx["D_" + r][t]; gb = Rx["gb_" + r][t] * CONV
        ok = np.isfinite(D) & np.isfinite(gb) & (gb > 0) & (D > 0)
        return D[ok], gb[ok], Rx, t[ok]

    for rd in ("bD", "b"):
        for r in ROUTES:
            for k in THN:
                lab = f"{k}-route{r}-{rd}"
                D, gb, Rx, tt = row_levels(rd, r, k)
                ls0, u0 = s_star(D, gb)
                lsb, ub = boot_s(D, gb, lab)
                itv = pct(lsb); itv["unb_frac"] = float(ub.mean()); itv["sd"] = float(lsb.std())
                band = {}
                for sh in (-0.30, -0.15, 0.15, 0.30):
                    band[f"{sh:+.2f}"] = s_star(D * 10 ** (-sh), gb * 10 ** sh)
                lv, lf = AI.lever(D, gb, NU, A0C)
                kn = {}
                ls_p2, u_p2 = s_star(D, gb, NUP2)
                kn["kernel P2"] = [None if (u0 or u_p2) else ls_p2 - ls0]
                if r in ("ii", "iii"):
                    kn["gas (b)"] = []
                    for nm, cfgv in (("Sig0", dict(Sig=0.0)), ("Sig15", dict(Sig=15.0)), ("HIx0.5", dict(gcoef=0.5)), ("HIx2", dict(gcoef=2.0))):
                        D2, g2, _, _ = row_levels(rd, r, k, cfgv); l2, u2 = s_star(D2, g2); kn["gas (b)"].append(None if (u0 or u2) else l2 - ls0)
                if r == "ii":
                    kn["H2 (b2)"] = []
                    for nm, cfgv in (("mu0.5", dict(mu_scale=0.5)), ("mu2", dict(mu_scale=2.0))):
                        D2, g2, _, _ = row_levels(rd, r, k, cfgv); l2, u2 = s_star(D2, g2); kn["H2 (b2)"].append(None if (u0 or u2) else l2 - ls0)
                    D2, g2, _, _ = row_levels(rd, r, k, dict(natlog=True)); l2, u2 = s_star(D2, g2); kn["natlog (d)"] = [None if (u0 or u2) else l2 - ls0]
                # historical estimator (kernel RAR, D > 1.05 rows only)
                a0h = Rx["a0_" + r][tt]
                Lh = c.level_log(a0h); Lh = Lh[np.isfinite(Lh)]
                if len(Lh) >= 3:
                    hmed = float(np.median(Lh)); hlo, hhi = c.boot_median(Lh, B_BOOT, zlib.crc32(("HIST|" + lab).encode()) % 100000)
                else:
                    hmed = hlo = hhi = float("nan")
                kn["historical estimator"] = [None if (u0 or not np.isfinite(hmed)) else hmed - math.log10(A0C) - ls0]
                half = math.sqrt(sum(max([abs(x) for x in v if x is not None] + [0.0]) ** 2 for v in kn.values()))
                half_nn = math.sqrt(sum(max([abs(x) for x in v if x is not None] + [0.0]) ** 2 for k_, v in kn.items() if k_ != "natlog (d)"))   # reported alternative (Addendum 2)
                # drifts (routes ii, iii)
                dr = {}
                if r in ("ii", "iii"):
                    for nm, cfgv in (("tau+0.25", dict(tau=0.25)), ("tau-0.25", dict(tau=-0.25)), ("tH+0.3", dict(tH=0.3)), ("tH-0.3", dict(tH=-0.3))):
                        if r == "iii" and nm.startswith("tH"): continue
                        D2, g2, _, _ = row_levels(rd, r, k, cfgv); l2, u2 = s_star(D2, g2); dr[nm] = (l2, u2)
                med_D = float(np.median(D)); n_lt1 = int((D < 1).sum()); n_le105 = int((D <= 1.05).sum())
                RES[lab] = dict(rd=rd, route=r, third=k, n=len(D), z=ZMED[k], ls=ls0, s=s_of(ls0, u0), no_root=u0, itv=itv, band={s_: dict(ls=v[0], s=s_of(*v), unb=v[1]) for s_, v in band.items()},
                                lever=(float(lv[0]) if not lf[0] else float("nan")), knobs=kn, recipe_half=half, recipe_half_no_natlog=half_nn, hist=dict(med=hmed, lo=float(hlo), hi=float(hhi), n=len(Lh)),
                                drift={nm: dict(ls=v[0], unb=v[1]) for nm, v in dr.items()}, median_D=med_D, n_D_lt1=n_lt1, n_D_le_105=n_le105)
                R_ = RES[lab]
                P(f"  {lab:18s} N {R_['n']:2d} z {R_['z']:.3f}:  " + (f"NO ROOT (median D {med_D:.2f}; D<1: {n_lt1}/{R_['n']})" if u0 else f"s* = {10 ** ls0:.3f} (a0 = {10 ** ls0 * 0.93603:.3f}e-10)")
                  + f"  68% [{s_of(itv['lo68'], False):.3f}, {s_of(itv['hi68'], False):.3f}]  95% [{s_of(itv['lo95'], False):.3f}, {s_of(itv['hi95'], False):.3f}]  (SD {itv['sd']:.3f} dex; unbounded {itv['unb_frac']:.3f}; median D {med_D:.2f}; D<1 {n_lt1}, D<=1.05 {n_le105})")
                b15 = sorted([R_["band"]["-0.15"]["s"], R_["band"]["+0.15"]["s"]]); b30 = sorted([R_["band"]["-0.30"]["s"], R_["band"]["+0.30"]["s"]])
                P(f"      baryon +-0.15 [{b15[0]:.3f}, {b15[1]:.3f}] +-0.30 [{b30[0]:.3f}, {b30[1]:.3f}] (lever {R_['lever']:+.2f}); recipe half-width {half:.3f} dex (without the natural-log mu reading: {half_nn:.3f}); historical level {hmed:.2f} [{hlo:.2f}, {hhi:.2f}] (n {len(Lh)}, a0 in log10 m s^-2; canonical -10.029)")
                P("      knobs (Delta log10 s*): " + "; ".join(f"{k_} " + "/".join('--' if x is None else f"{x:+.3f}" for x in v) for k_, v in kn.items()) + (";  drifts: " + "; ".join(f"{nm} {'no root' if v[1] else format(v[0] - ls0, '+.3f')}" for nm, v in dr.items()) if dr and not u0 else ""))

    # ---------------------------------------------------------------- reading (a) and (aD): sensitivity rows (reported, never points)
    P("\nSENSITIVITY ROWS: reading a (v_perp = v_f) and aD (a plus D1); s* per route and third (no bootstrap; never drawn)")
    SENS = {}
    for rd in ("a", "aD"):
        Ra = routes_of(gperp_of(rd, datx))
        for r in ROUTES:
            vals = []
            for k in THN:
                t = THN[k]; D = Ra["D_" + r][t]; gb = Ra["gb_" + r][t] * CONV
                ok = np.isfinite(D) & np.isfinite(gb) & (gb > 0) & (D > 0)
                ls_, u_ = s_star(D[ok], gb[ok])
                SENS[f"{k}-route{r}-{rd}"] = dict(ls=ls_, no_root=u_, s=s_of(ls_, u_), n=int(ok.sum()))
                vals.append("no root" if u_ else f"{10 ** ls_:.3f}")
            P(f"  reading {rd:2s} route ({r:3s}): s* z1 / z2 / z3 = " + " / ".join(vals))
    NUM["sensitivity"] = SENS
    # ---------------------------------------------------------------- route contrast and the thirds' differences
    P("\nTHE ROUTES' CONTRAST (log10 s*(route) - log10 s*(i), rows with a root in both) and THE THIRDS' DIFFERENCES (z3 - z1, with sqrt(sd1^2 + sd3^2))")
    CON = {}
    for rd in ("bD", "b"):
        for k in THN:
            for r in ("ii", "iii"):
                a, b = RES[f"{k}-route{r}-{rd}"], RES[f"{k}-routei-{rd}"]
                CON[f"{rd}|{k}|{r}"] = None if (a["no_root"] or b["no_root"]) else a["ls"] - b["ls"]
        P(f"  reading {rd}: contrast (ii - i) " + " / ".join('--' if CON[f'{rd}|{k}|ii'] is None else f"{CON[f'{rd}|{k}|ii']:+.3f}" for k in THN) + "; (iii - i) " + " / ".join('--' if CON[f'{rd}|{k}|iii'] is None else f"{CON[f'{rd}|{k}|iii']:+.3f}" for k in THN))
    DIF = {}
    for rd in ("bD", "b"):
        for r in ROUTES:
            a, b = RES[f"z3-route{r}-{rd}"], RES[f"z1-route{r}-{rd}"]
            DIF[f"{rd}|{r}"] = None if (a["no_root"] or b["no_root"]) else dict(d=a["ls"] - b["ls"], sd=math.sqrt(a["itv"]["sd"] ** 2 + b["itv"]["sd"] ** 2),
                                                                               rival=math.log10(LAWS["H(z)"](ZMED["z3"]) / LAWS["H(z)"](ZMED["z1"])))
            if DIF[f"{rd}|{r}"]:
                q = DIF[f"{rd}|{r}"]
                P(f"  reading {rd} route ({r:3s}): d(z3 - z1) = {q['d']:+.3f} +- {q['sd']:.3f} dex (H(z) expects {q['rival']:+.3f}; FLAT 0)")
            else:
                P(f"  reading {rd} route ({r:3s}): d(z3 - z1) not formed (a third has no root)")
    # flags
    FLAGS = {}
    for lab, R_ in RES.items():
        b15 = [R_["band"]["-0.15"]["s"], R_["band"]["+0.15"]["s"]]; b30 = [R_["band"]["-0.30"]["s"], R_["band"]["+0.30"]["s"]]
        lo95, hi95 = s_of(R_["itv"]["lo95"], False), s_of(R_["itv"]["hi95"], False)
        f = {}
        for L, fn in LAWS.items():
            sL = fn(R_["z"])
            f[L] = dict(s=sL, in95=bool(lo95 <= sL <= hi95), in15=bool(min([lo95] + b15) <= sL <= max([hi95] + b15)), in30=bool(min([lo95] + b30) <= sL <= max([hi95] + b30)))
        FLAGS[lab] = f
    P("\nFLAGS PER LAW (95 % / inner-widened / outer-widened), reading bD: " + "; ".join(f"{lab.replace('-bD', '')} " + "/".join(''.join('Y' if FLAGS[lab][L][kk] else 'n' for kk in ('in95', 'in15', 'in30')) for L in LAWS) for lab in RES if lab.endswith("bD")))
    NUM.update(rows=RES, contrast=CON, diff=DIF, flags=FLAGS)

    # ---------------------------------------------------------------- controls
    P("\nCONTROLS (stage B)")
    if MUTATE:
        main = json.load(open(os.path.join(HERE, "cfg262_stageB_results.json")))["numbers"]["rows"]
        sh = {k: (RES[k]["ls"] - main[k]["ls"]) for k in RES if not RES[k]["no_root"] and not main[k]["no_root"]}
        check("M2 MUTATE=1 (reactivity): the planted law at s = 2 moves every row with a root in both runs by +0.301 +- 0.05 dex", "; ".join(f"{k} {v:+.3f}" for k, v in sh.items()), len(sh) > 0 and all(abs(v - 0.30103) <= 0.05 for v in sh.values()))
        NUM["mutate_shift"] = sh
    else:
        # M1: alt footing, same absolute a0
        d1 = 0.0
        for lab, R_ in RES.items():
            if R_["no_root"]: continue
            rd, r, k = R_["rd"], R_["route"], R_["third"]
            D, gb, _, _ = row_levels(rd, r, k)
            la, ua = AI.implied(D, gb, NU, A0A)
            if not ua[0]: d1 = max(d1, abs(float(la[0]) + math.log10(A0A / A0C) - R_["ls"]))
        check("M1 CONTROL: the alt footing implies the same absolute a0 in every row with a root", f"max |d log10| = {d1:.1e}", d1 < 1e-9)
        # M3: reproduction of the record (historical estimator, route (i), lowest third of the route-(i)-finite galaxies)
        tg = {"a": -10.38, "b": -10.14, "aD": -10.05, "bD": -9.93}
        m3 = {}
        for rd in ("a", "b", "aD", "bD"):
            Rr = routes_of(gperp_of(rd, datx))
            vi = np.isfinite(Rr["a0_i"]); thr = c.thirds(z[vi]); ids = np.where(vi)[0]
            m3[rd] = float(np.median(c.level_log(Rr["a0_i"])[ids[thr[0]]]))
        check("M3 CONTROL (the record's arithmetic): the historical estimator on route (i), lowest third of the route-(i)-finite galaxies, reproduces CFG199's -10.38 (a), -10.14 (b) and CFG236's -10.05 (a + D1), -9.93 (b + D1) to +-0.05 dex",
              "; ".join(f"{rd}: {m3[rd]:+.3f} (target {tg[rd]:+.2f})" for rd in m3), all(abs(m3[rd] - tg[rd]) <= 0.05 for rd in m3) if not SELFTEST else True, load_bearing=not SELFTEST)
        NUM["m3"] = m3
        nrows = {rd: sum(len(THN[k]) for k in THN) for rd in ("b", "bD")}
        check("M5 the three thirds partition the 109 galaxies for every route and reading", f"{nrows}", all(v == NG for v in nrows.values()))
        if SELFTEST:
            ok = all(10 ** RES[f"{k}-route{'iii'}-{rd}"]["itv"]["lo95"] <= S_TRUE_SELF <= 10 ** RES[f"{k}-route{'iii'}-{rd}"]["itv"]["hi95"] for k in THN for rd in ("b", "bD") if not RES[f"{k}-routeiii-{rd}"]["no_root"])
            check("SELFTEST: every route-(iii) row returns the fabricated truth inside its 95 % interval", "; ".join(f"{k}-{rd}: {RES[f'{k}-routeiii-{rd}']['s']:.3f}" for k in THN for rd in ('b', 'bD')) + f" (truth {S_TRUE_SELF})", ok)

    # ---------------------------------------------------------------- the points file
    cols = ["lane", "object", "gas_class", "z", "z_shown", "no_root", "s_star", "a0_1e-10_m_s2", "stat68_lo", "stat68_hi", "stat95_lo", "stat95_hi", "inner_lo", "inner_hi", "inner_noroot_corner", "outer_lo", "outer_hi", "outer_noroot_corner",
            "recipe_half_dex", "recipe_lo", "recipe_hi", "n", "route", "reading", "third", "median_D", "n_D_lt1", "quality", "flags_FLAT", "flags_H(z)", "flags_PROXY", "hist_level_log10", "hist_lo95", "hist_hi95", "recipe_half_no_natlog"]
    ref = os.path.join(CFG, "CHART_a0z_combined_2026-09-30", "chart_a0z_points.csv")
    ref_cols = open(ref).readline().strip().split(",")
    check("M4 CONTROL: the first 18 columns of the points file equal chart_a0z_points.csv's header", f"{ref_cols == cols[:18]}", ref_cols == cols[:18])
    GC = {"i": "MD-i (DC14 fitted masses: the model's own decomposition)", "ii": "MD-ii (SED M* + scaling H2, prior HI)", "iii": "MD-iii (SED M*, prior HI)"}
    with open(os.path.join(HERE, f"cfg262_points{SFX}.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(cols)
        for lab, R_ in RES.items():
            b15 = sorted([R_["band"]["-0.15"]["s"], R_["band"]["+0.15"]["s"]]); b30 = sorted([R_["band"]["-0.30"]["s"], R_["band"]["+0.30"]["s"]])
            nr15 = int(R_["band"]["-0.15"]["unb"] or R_["band"]["+0.15"]["unb"]); nr30 = int(R_["band"]["-0.30"]["unb"] or R_["band"]["+0.30"]["unb"])
            q = ("pressure-corrected (asymmetric drift D1), " if R_["rd"] == "bD" else "no-pressure LOWER bound, ") + ("model-internal decomposition" if R_["route"] == "i" else "SED-mass / scaling-gas calibrated") + ("; NO ROOT (median D <= 1: baryons above the dynamics)" if R_["no_root"] else "")
            fl = FLAGS[lab]
            w.writerow(["CFG262", f"MUSE-DARK {lab}", GC[R_["route"]], f"{R_['z']:.4f}", f"{R_['z']:.4f}", int(R_["no_root"]), f"{R_['s']:.6f}", f"{R_['s'] * 0.93603:.6f}",
                        f"{s_of(R_['itv']['lo68'], False):.6f}", f"{s_of(R_['itv']['hi68'], False):.6f}", f"{s_of(R_['itv']['lo95'], False):.6f}", f"{s_of(R_['itv']['hi95'], False):.6f}",
                        f"{b15[0]:.6f}", f"{b15[1]:.6f}", nr15, f"{b30[0]:.6f}", f"{b30[1]:.6f}", nr30,
                        f"{R_['recipe_half']:.4f}", f"{R_['s'] * 10 ** (-R_['recipe_half']):.6f}", f"{R_['s'] * 10 ** R_['recipe_half']:.6f}", R_["n"], R_["route"], R_["rd"], R_["third"],
                        f"{R_['median_D']:.3f}", R_["n_D_lt1"], q, *["".join("Y" if fl[L][kk] else "n" for kk in ("in95", "in15", "in30")) for L in LAWS],
                        f"{R_['hist']['med']:.4f}", f"{R_['hist']['lo']:.4f}", f"{R_['hist']['hi']:.4f}", f"{R_['recipe_half_no_natlog']:.4f}"])
    P(f"\n  points written: cfg262_points{SFX}.csv ({len(RES)} rows)")

nf = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nf}   ({time.time() - T0:.0f} s)")


def jc(o):
    if isinstance(o, dict): return {(k if isinstance(k, str) else str(k)): jc(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [jc(v) for v in o]
    if isinstance(o, np.ndarray): return jc(o.tolist())
    if isinstance(o, (np.floating, float)): return None if not np.isfinite(o) else float(o)
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o


open(os.path.join(HERE, f"cfg262{SFX}.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
json.dump(dict(stage=STAGE, mutate=MUTATE, selftest=SELFTEST, checks=[dict(name=n, ok=ok, load_bearing=lb) for n, ok, lb in CHK], numbers=jc(NUM)), open(os.path.join(HERE, f"cfg262{SFX}_results.json"), "w"), indent=1)
sys.exit(1 if nf else 0)
