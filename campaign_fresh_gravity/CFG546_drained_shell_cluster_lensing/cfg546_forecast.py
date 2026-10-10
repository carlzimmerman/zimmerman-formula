#!/usr/bin/env python3
"""CFG546 Step F: Fisher forecast of the drained-shell amplitude A against a DK14 baseline with splashback marginalised.

Implements FROZEN_CRITERIA.md (baf7e3dd4), Step F, K4 and MUTATE-FORECAST.
Templates: cfg546_predict_results.json (R5, this lane) and ../CFG495_drawdown_shell/cfg495_sim_analysis_results.json (variant).
On-disk dataset: DESI DR1 LRG ΔΣ covariance (reads only rp bin edges and the joint covariance; no ΔΣ values).
Outputs: cfg546_forecast.out / cfg546_forecast_results.json; CFG546_MUTATE=1 -> *_MUTATE.* (noise-realisation recovery).
Run: nice -n 10 python3 cfg546_forecast.py
"""
import os, sys, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
from scipy.optimize import least_squares
from astropy.io import fits
import cfg546_lib as LB

MUTATE = os.environ.get("CFG546_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT = os.path.join(HERE, f"cfg546_forecast{TAG}.out")
JS = os.path.join(HERE, f"cfg546_forecast{TAG}_results.json")
EXT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_external_data"))
DD = os.path.join(EXT, "desi_dr1_lensing", "extracted")
_lines = []
RES = {"mutate": MUTATE, "criteria_commit": "baf7e3dd4", "checks": {}, "forecast": {}}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); _lines.append(s)


def check(name, detail, ok, gated=True):
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if gated else ' (reported)'} {name}: {detail}")
    RES["checks"][name] = dict(ok=bool(ok), detail=detail, gated=gated)
    return ok


P(__doc__.split("Run:")[0].strip())

# ------------------------------------------------------------ templates
PR = json.load(open(os.path.join(HERE, "cfg546_predict_results.json")))
XC = np.array(PR["xc"])
T = PR["templates"]
C495 = json.load(open(os.path.join(LB.CFG, "CFG495_drawdown_shell", "cfg495_sim_analysis_results.json")))
X495 = np.array(C495["N512_s359_can"]["xc"])


def t495(run, b):
    bb = C495[run]["bins"][b]
    return np.array(bb["eff3d_minus_S0"], float) / np.array(bb["dS0_3d"], float)


TEMPL = {
    ("clusters", "canonical", "R5_512"): (XC, T["clusters"]["canonical"]),
    ("clusters", "alt", "R5_512"): (XC, T["clusters"]["alt"]),            # 256 alt x s_res (frozen construction)
    ("clusters", "canonical", "R5_256"): (XC, T["clusters"]["canonical_256"]),
    ("clusters", "alt", "R5_256"): (XC, T["clusters"]["alt_256"]),
    ("clusters", "canonical", "CFG495"): (X495, t495("N512_s359_can", "14.2-16.0")),
    ("clusters", "alt", "CFG495"): (X495, t495("N512_s359_alt", "14.2-16.0")),
    ("groups", "canonical", "R5_512"): (XC, T["groups"]["canonical"]),
    ("groups", "alt", "R5_512"): (XC, T["groups"]["alt"]),                # built on the UNRESOLVED 256^3 groups: does not count
    ("groups", "canonical", "CFG495"): (X495, t495("N512_s359_can", "13.4-13.7")),
    ("groups", "alt", "CFG495"): (X495, t495("N512_s359_alt", "13.4-13.7")),
}
RESOLVED = {k: True for k in TEMPL}
RESOLVED[("groups", "alt", "R5_512")] = False
P(f"\nTemplates: clusters s_res {T['clusters']['s_res']:.3f}; groups s_res {T['groups']['s_res']:.3f} "
  f"(groups 256^3 median r_ta < 5 cells: the alt R5 group template does NOT count by the resolution rule)")

# ------------------------------------------------------------ K4
rs, rhos = 0.3, 1e15
dr = rhos / ((LB.RG / rs) * (1 + LB.RG / rs) ** 2)
ds = LB.project(dr)
x = np.geomspace(0.1, 10, 30)


def _F(x):
    out = np.empty_like(x)
    lo = x < 1; hi = x > 1
    out[lo] = np.arccosh(1 / x[lo]) / np.sqrt(1 - x[lo] ** 2); out[hi] = np.arccos(1 / x[hi]) / np.sqrt(x[hi] ** 2 - 1); out[~(lo | hi)] = 1
    return out


Sg = 2 * rs * rhos * (1 - _F(x)) / (x ** 2 - 1)
Mb = 4 * rs * rhos * (_F(x) + np.log(x / 2)) / x ** 2
an = (Mb - Sg) * 1e-12
dev = float(np.max(np.abs(np.interp(np.log(x * rs), np.log(LB.RP), ds) / an - 1)))
check("K4 projection vs analytic NFW", f"max |dev| {dev:.2e} over 0.1-10 R/r_s", dev < 0.01)

# ------------------------------------------------------------ datasets
D = {  # ID: name, N, zl, logM200m, neff, sigma_e, zs, published range (phys Mpc), template class
    "D1": ("DES-Y1 redMaPPer lambda>=20", 6500, 0.40, 14.3, 6.0, 0.27, 0.75, (0.03, 30.0), "clusters"),
    "D2": ("DES-Y3 redMaPPer lambda>=20", 16000, 0.42, 14.3, 5.6, 0.26, 0.75, (0.03, 30.0), "clusters"),
    "D3": ("SDSS redMaPPer x SDSS shear", 5500, 0.24, 14.3, 1.2, 0.36, 0.40, (0.1, 30.0), "clusters"),
    "D4": ("HSC-Y3 x CAMIRA/redMaPPer", 1800, 0.50, 14.1, 15.0, 0.24, 1.0, (0.1, 15.0), "clusters"),
    "D5": ("KiDS-1000 x GAMA groups Nfof>=5", 2400, 0.20, 13.6, 6.2, 0.27, 0.65, (0.02, 2.0), "groups"),
    "D6": ("eRASS1 x DES/KiDS/HSC", 2200, 0.30, 14.4, 6.0, 0.26, 0.75, (0.5, 3.2), "clusters"),
    "D7": ("SPT x DES-Y3", 700, 0.55, 14.8, 5.6, 0.26, 0.85, (0.5, 3.2), "clusters"),
    "D8": ("ACT DR5 x DES-Y3/HSC", 1000, 0.50, 14.6, 5.6, 0.26, 0.85, (0.1, 10.0), "clusters"),
}
H = 0.6766


def edges_for(rmin, rmax, n=15):
    return np.geomspace(rmin, rmax, n + 1)


# DESI LRG1 (on disk): covariance and bin edges only
SURV = {"KiDS": 1, "DES": 2, "HSCY3": 3}
LRG1_COMBOS = {"KiDS": [4, 5], "DES": [4], "HSCY3": [3, 4]}
LRG2_COMBOS = {"HSCY3": [3, 4]}
base = os.path.join(DD, "covariances")
idx = np.loadtxt(os.path.join(base, "bin_ds_kids1000desy3hscy3_desiy1lrg.dat"), comments="#")
raw = np.loadtxt(os.path.join(base, "dscovcorr_kids1000desy3hscy3_desiy1lrg_pzwei.dat"), skiprows=1)
Cj = np.zeros((len(idx), len(idx))); Cj[raw[:, 0].astype(int) - 1, raw[:, 1].astype(int) - 1] = raw[:, 2]
KEY = {(int(r[1]), int(r[2]), int(r[3]), int(r[4])): i for i, r in enumerate(idx)}
t = fits.open(os.path.join(DD, "ggl", "DES", "deltasigma_LRG_zmin_0.4_zmax_0.6_lenszbin_3_blindA_boost_False.fits"))[1].data
RPMIN = np.array(t["rp_min"], float); RPMAX = np.array(t["rp_max"], float); RPC = np.array(t["rp"], float)


def desi_setup(il, combos, rmin, rmax):
    sel = np.where((RPC >= rmin) & (RPC <= rmax))[0]
    ii = []
    for sv, ks in combos.items():
        for k in ks:
            ii += [KEY[(SURV[sv], il, k, j + 1)] for j in sel]
    C = Cj[np.ix_(ii, ii)]
    edges = np.concatenate([RPMIN[sel], [RPMAX[sel][-1]]])
    return edges, C, sum(len(v) for v in combos.values())


# ------------------------------------------------------------ forecast core
def forecast(info, p0, tclass, foot, tname, edges, C, ntile=1, desi=False, xscale=1.0, cov_f=1.0, quiet=False):
    xc, rel = TEMPL[(tclass, foot, tname)]
    tm = LB.Template(xc, rel, xscale=xscale)
    J = LB.jacobian(p0, info, tm, edges, ntile=ntile)
    Cinv = np.linalg.inv(C * cov_f)
    pri = LB.priors(p0, desi=desi)
    s = LB.fisher_summary(J, Cinv, pri)
    # apparent splashback shift if the drained shell (A = 1) is fitted with the baseline alone
    p1 = dict(p0); p1["A"] = 1.0
    delta = np.tile(LB.model(p1, info, tm, edges) - LB.model(p0, info, tm, edges), ntile)
    b = LB.bias_baseline(J, Cinv, pri, delta)
    pb = dict(p0); [pb.__setitem__(k, p0[k] + v) for k, v in b.items()]
    d0 = LB.drho(p0, info["r200m"])["tot"]; db = LB.drho(pb, info["r200m"])["tot"]
    rta0 = LB.rta_of(d0, info["z"]); rsp0 = LB.rsp_of(d0); rspb = LB.rsp_of(db)
    s.update(dict(rsp_over_rta=rsp0 / rta0, rsp_over_r200m=rsp0 / info["r200m"], rta=rta0, rsp=rsp0,
                  dlnrt_apparent=float(b["lnrt"]), rsp_shift_frac=rspb / rsp0 - 1, dse_apparent=float(b["se"]),
                  max_template_frac=float(np.max(np.abs(delta[:len(edges) - 1] / LB.model(p0, info, None, edges))))))
    return s


def fmt(s):
    return (f"Z {s['Z']:5.2f} (fixed splash {s['Z_fixed_splash']:5.2f}); corr(A,ln r_t) {s['corr_A_lnrt']:+.2f}, corr(A,s_e) {s['corr_A_se']:+.2f}; "
            f"r_sp/r_ta {s['rsp_over_rta']:.2f} (r_sp/r200m {s['rsp_over_r200m']:.2f}); apparent r_sp shift {100 * s['rsp_shift_frac']:+.1f}%; "
            f"max |dDS/DS| {100 * s['max_template_frac']:.1f}%")


if not MUTATE:
    P("\n== Template peak effect in ΔΣ (A = 1) and the forecast, per dataset (Z = 1/sigma_A, DK14 r_t, beta, gamma, b_e, s_e free; m0, m1)")
    for did, (name, N, zl, lM, neff, se, zs, prng, tcl) in D.items():
        M = 10 ** lM
        p0, info = LB.fiducial(M, zl)
        P(f"\n-- {did} {name}: N {N}, z_l {zl}, log M200m {lM}, n_eff {neff}, sigma_e {se}, z_s {zs}; template {tcl}  [(U) recalled parameters]")
        RES["forecast"][did] = {"name": name, "params": dict(N=N, zl=zl, lM=lM, neff=neff, se=se, zs=zs, pub_range_phys_Mpc=prng), "rows": {}}
        pmin = max(prng[0] * (1 + zl) * H, 0.3); pmax = prng[1] * (1 + zl) * H
        ranges = {"published": (pmin, pmax), "extended": (0.3, 30.0)}
        for rname, (a, b) in ranges.items():
            if b <= a * 2:
                P(f"   {rname}: range too short"); continue
            e = edges_for(a, b)
            dsf = LB.model(p0, info, None, e)
            par = dict(N=N, zl=zl, zs=zs, neff=neff, se=se)
            C1 = LB.constructed_cov(dsf, e, par)
            C2 = LB.constructed_cov(dsf, e, par, f_lss=2.0)
            for foot in ("canonical", "alt"):
                for tn in ("R5_512", "R5_256", "CFG495"):
                    if (tcl, foot, tn) not in TEMPL: continue
                    s = forecast(info, p0, tcl, foot, tn, e, C1)
                    row = {"primary": s}
                    if tn == "R5_512":
                        row["rta_plus"] = forecast(info, p0, tcl, foot, tn, e, C1, xscale=10 ** 0.05)["Z"]
                        row["rta_minus"] = forecast(info, p0, tcl, foot, tn, e, C1, xscale=10 ** -0.05)["Z"]
                        row["cov_x1.3"] = forecast(info, p0, tcl, foot, tn, e, C1, cov_f=1.3)["Z"]
                        row["lss_x2"] = forecast(info, p0, tcl, foot, tn, e, C2)["Z"]
                    RES["forecast"][did]["rows"][f"{rname}|{foot}|{tn}"] = row
                    extra = "" if tn != "R5_512" else (f" | variants Z: r_ta+ {row['rta_plus']:.2f}, r_ta- {row['rta_minus']:.2f}, "
                                                      f"cov1.3 {row['cov_x1.3']:.2f}, LSSx2 {row['lss_x2']:.2f}")
                    lab = "" if RESOLVED[(tcl, foot, tn)] else " [UNRESOLVED template: does not count]"
                    P(f"   {rname:9s} {a:5.2f}-{b:5.1f} h^-1 Mpc | {foot:9s} | {tn:6s}: {fmt(s)}{extra}{lab}")

    # DESI LRG (on disk), pre-data fiducial log M200m 13.4 (U)
    for lname, il, combos, zl in (("LRG1", 1, LRG1_COMBOS, 0.5), ("LRG2", 2, LRG2_COMBOS, 0.7)):
        p0, info = LB.fiducial(10 ** 13.4, zl)
        P(f"\n-- DESI DR1 {lname} x {combos} (joint analytic covariance; pre-data fiducial log M200m 13.4 (U)); template groups; GALAXY-SELECTED, NOT HALO-CENTRED")
        RES["forecast"][f"DESI_{lname}"] = {"rows": {}}
        for rname, (a, b) in {"primary": (0.5, 30.0), "r1": (1.0, 30.0), "to80": (0.5, 80.0)}.items():
            e, C, nt = desi_setup(il, combos, a, b)
            for foot in ("canonical", "alt"):
                for tn in ("R5_512", "CFG495"):
                    s = forecast(info, p0, "groups", foot, tn, e, C, ntile=nt, desi=True)
                    row = {"primary": s}
                    if tn == "R5_512" and rname == "primary":
                        row["rta_plus"] = forecast(info, p0, "groups", foot, tn, e, C, ntile=nt, desi=True, xscale=10 ** 0.05)["Z"]
                        row["rta_minus"] = forecast(info, p0, "groups", foot, tn, e, C, ntile=nt, desi=True, xscale=10 ** -0.05)["Z"]
                        row["cov_x1.3"] = forecast(info, p0, "groups", foot, tn, e, C, ntile=nt, desi=True, cov_f=1.3)["Z"]
                    RES["forecast"][f"DESI_{lname}"]["rows"][f"{rname}|{foot}|{tn}"] = row
                    lab = "" if RESOLVED[("groups", foot, tn)] else " [UNRESOLVED template: does not count]"
                    extra = "" if "rta_plus" not in row else f" | variants Z: r_ta+ {row['rta_plus']:.2f}, r_ta- {row['rta_minus']:.2f}, cov1.3 {row['cov_x1.3']:.2f}"
                    P(f"   {rname:7s} {a:4.1f}-{b:4.0f} | {foot:9s} | {tn:6s}: {fmt(s)}{extra}{lab}")

    # ------------------------------------------------------------ ranking and lane-level forecast verdict
    P("\n== Ranking (primary R5_512 template, best range per dataset; Z both footings; alt group template does not count)")
    rank = []
    for did, v in RES["forecast"].items():
        best = None
        for rk, row in v["rows"].items():
            rng, foot, tn = rk.split("|")
            if tn != "R5_512" or foot != "canonical": continue
            alt = v["rows"].get(f"{rng}|alt|{tn}")
            zc = row["primary"]["Z"]; za = alt["primary"]["Z"] if alt else float("nan")
            tcl = "groups" if did.startswith("DESI") or did == "D5" else "clusters"
            za_counts = RESOLVED[(tcl, "alt", "R5_512")]
            zmin = min(zc, za) if za_counts else float("nan")
            z256 = v["rows"].get(f"{rng}|canonical|R5_256", {}).get("primary", {}).get("Z", float("nan"))
            cand = dict(id=did, range=rng, Z_can=zc, Z_alt=za, alt_counts=za_counts, Z_min=zmin, Z_256_can=z256,
                        corr=row["primary"]["corr_A_lnrt"], cost=row["primary"]["cost"])
            if best is None or (np.nan_to_num(cand["Z_min"], nan=-1) > np.nan_to_num(best["Z_min"], nan=-1)) or \
               (np.isnan(cand["Z_min"]) and np.isnan(best["Z_min"]) and cand["Z_can"] > best["Z_can"]):
                best = cand
        if best: rank.append(best)
    rank.sort(key=lambda r: (-np.nan_to_num(r["Z_min"], nan=-1), -r["Z_can"]))
    for r in rank:
        P(f"  {r['id']:9s} [{r['range']}]: Z can {r['Z_can']:.2f}, alt {r['Z_alt']:.2f}{'' if r['alt_counts'] else ' (alt does not count)'}; "
          f"Z(256^3 can) {r['Z_256_can']:.2f}; corr(A, ln r_t) {r['corr']:+.2f}; sigma_A cost of freeing splashback x{r['cost']:.2f}")
    RES["ranking"] = rank
    ok3 = [r for r in rank if not r["id"].startswith("DESI") and np.nan_to_num(r["Z_min"]) >= 3]
    ok2 = [r for r in rank if not r["id"].startswith("DESI") and np.nan_to_num(r["Z_min"]) >= 2]
    alldeg = all(abs(r["corr"]) > 0.9 for r in rank)
    P(f"\n  Cluster candidates with Z >= 3 on both footings: {[r['id'] + '[' + r['range'] + ']' for r in ok3]}")
    P(f"  ... with Z >= 2: {[r['id'] + '[' + r['range'] + ']' for r in ok2]}; |corr(A, ln r_t)| > 0.9 for all: {alldeg}")
    rescond = [r["id"] for r in ok3 if not (r["Z_256_can"] >= 2)]
    P(f"  RESOLUTION-CONDITIONAL (Z>=3 with 512^3 template but Z<2 with 256^3): {rescond}")
    RES["download_ok3"] = ok3; RES["download_ok2"] = ok2; RES["all_degenerate"] = alldeg; RES["resolution_conditional"] = rescond

else:
    # ------------------------------------------------------------ MUTATE-FORECAST
    P("\n== MUTATE-FORECAST: 300 noise realisations per case; A = 0 and A = 1 injected; full nonlinear fit with priors")
    rng = np.random.default_rng(5461)
    cases = []
    p0, info = LB.fiducial(10 ** 14.3, 0.42)
    e = edges_for(0.3, 30.0)
    C = LB.constructed_cov(LB.model(p0, info, None, e), e, dict(N=16000, zl=0.42, zs=0.75, neff=5.6, se=0.26))
    cases.append(("D2-extended canonical", p0, info, "clusters", e, C, 1, False))
    p0d, infod = LB.fiducial(10 ** 13.4, 0.5)
    ed, Cd, nt = desi_setup(1, LRG1_COMBOS, 0.5, 30.0)
    cases.append(("DESI LRG1 canonical", p0d, infod, "groups", ed, Cd, nt, True))
    for name, p0, info, tcl, e, C, nt, desi in cases:
        xc, rel = TEMPL[(tcl, "canonical", "R5_512")]
        tm = LB.Template(xc, rel)
        pri = LB.priors(p0, desi=desi)
        Lc = np.linalg.cholesky(C); Li = np.linalg.inv(Lc)
        J = LB.jacobian(p0, info, tm, e, ntile=nt)
        sF = LB.fisher_summary(J, np.linalg.inv(C), pri)["sigma_A"]
        names = LB.PNAMES
        for Ainj in (0.0, 1.0):
            pt = dict(p0); pt["A"] = Ainj
            mt = np.tile(LB.model(pt, info, tm, e), nt)
            Ah = []
            t0 = time.time()
            for it in range(300):
                d = mt + Lc @ rng.standard_normal(len(mt))
                def res(v):
                    pp = dict(zip(names, v))
                    r = Li @ (np.tile(LB.model(pp, info, tm, e), nt) - d)
                    pr = [(pp[k] - p0[k]) / s for k, s in pri.items()]
                    return np.concatenate([r, pr])
                v0 = np.array([pt[k] for k in names])
                sol = least_squares(res, v0, x_scale=np.array([LB.STEP[k] for k in names]) * 10, max_nfev=400)
                Ah.append(sol.x[0])
            Ah = np.array(Ah)
            mean = float(Ah.mean()); sd = float(Ah.std()); fr2 = float(np.mean(np.abs(Ah / sF) > 2))
            if Ainj == 0.0:
                check(f"MUTATE-FORECAST {name} A=0", f"mean Ahat {mean:+.3f} (sigma_A Fisher {sF:.3f}; {mean / sF:+.2f} sigma), scatter {sd:.3f}, "
                      f"frac |Ahat/sigma|>2 = {fr2:.3f} ({time.time() - t0:.0f} s)", abs(mean) <= 0.2 * sF and 0.02 <= fr2 <= 0.10)
            else:
                check(f"MUTATE-FORECAST {name} A=1", f"mean Ahat {mean:+.3f} ({(mean - 1) / sF:+.2f} sigma from 1), scatter {sd:.3f} vs Fisher {sF:.3f} "
                      f"(ratio {sd / sF:.2f}) ({time.time() - t0:.0f} s)", abs(mean - 1) <= 0.2 * sF and abs(sd / sF - 1) <= 0.25)
            RES.setdefault("mutate_cases", {})[f"{name} A={Ainj}"] = dict(mean=mean, sd=sd, sigma_fisher=sF, frac2=fr2)

json.dump(RES, open(JS, "w"), indent=1, default=float)
open(OUT, "w").write("\n".join(_lines) + "\n")
