#!/usr/bin/env python3
"""CFG551 Tasks 2-3: predicted splashback-radius ratio (framework / LCDM) per published measurement, the confrontation, controls.

Implements FROZEN_CRITERIA.md (b1b7c9e08).
Inputs (read-only): ../CFG546_drained_shell_cluster_lensing/cfg546_predict_results.json (rho_g templates, S0 stack),
  cfg546_predict_MUTATE_results.json (shuffled-centre template), cfg546_forecast_results.json (linear r_sp shifts),
  ../CFG495_drawdown_shell/cfg495_sim_analysis_results.json (V6), ../CFG504_smooth_halo_transition/cfg504_calib_results.json (K-S0),
  cfg551_ptemplate_results.json (particle templates, this lane), cfg551_measurements.json (compilation, this lane).
Outputs: cfg551_predict.out / cfg551_predict_results.json; CFG551_MUTATE=1 -> cfg551_predict_MUTATE.out / _results.json.
Run: OMP_NUM_THREADS=2 nice -n 10 python3 cfg551_predict.py ; CFG551_MUTATE=1 OMP_NUM_THREADS=2 nice -n 10 python3 cfg551_predict.py
"""
import os, sys, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
from scipy.optimize import brentq
import cfg551_lib as C

LB = C.LB
MUTATE = os.environ.get("CFG551_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT = os.path.join(HERE, f"cfg551_predict{TAG}.out")
JS = os.path.join(HERE, f"cfg551_predict{TAG}_results.json")
D546 = os.path.join(C.CFG, "CFG546_drained_shell_cluster_lensing")
H = 0.6766
_lines = []
RES = {"mutate": MUTATE, "criteria_commit": "b1b7c9e08", "checks": {}}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); _lines.append(s)


def check(name, detail, ok, gated=True):
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if gated else ' (reported)'} {name}: {detail}")
    RES["checks"][name] = dict(ok=bool(ok), detail=detail, gated=gated)
    return ok


def dump():
    json.dump(RES, open(JS, "w"), indent=1, default=float)
    open(OUT, "w").write("\n".join(_lines) + "\n")


P(__doc__.split("Run:")[0].strip())

# ------------------------------------------------------------------ templates
G = json.load(open(os.path.join(D546, "cfg546_predict_results.json")))
XC = np.array(G["xc"]); TG = G["templates"]["clusters"]
PT = json.load(open(os.path.join(HERE, "cfg551_ptemplate_results.json")))
assert PT["K_DEP"], "K-DEP failed: particle templates not usable"
TP = PT["templates"]["clusters"]
C495 = json.load(open(os.path.join(C.CFG, "CFG495_drawdown_shell", "cfg495_sim_analysis_results.json")))


def t495(run):
    bb = C495[run]["bins"]["14.2-16.0"]
    return np.array(C495[run]["xc"]), np.array(bb["eff3d_minus_S0"], float) / np.array(bb["dS0_3d"], float)


def tmpl(method, foot, kind="primary", sign=0, s=1.0):
    """Template object. method L: rho_g (CFG546); G: rho_p (this lane). kind primary | 256 | cfg495; sign +-1 adds +-1 sigma."""
    if kind == "cfg495":
        xc, rel = t495("N512_s359_can" if foot == "canonical" else "N512_s359_alt")
        return LB.Template(xc, rel, xscale=s)
    T = TG if method == "L" else TP
    key = foot if kind == "primary" else f"{foot}_256"
    rel = np.array(T[key], float)
    if sign:
        sk = f"{foot}_sig" if kind == "primary" else (f"{foot}_256_sig" if f"{foot}_256_sig" in T else None)
        if sk is None:                       # CFG546 rho_g 256^3 bootstrap errors live in the run records
            run = "N256_LRcan" if foot == "canonical" else "N256_LRalt"
            sig = np.array(G["runs"][run]["bins"]["clusters"]["rel_sig"], float)
        else:
            sig = np.array(T[sk], float)
        rel = rel + sign * sig
    return LB.Template(XC, rel, xscale=s)


FOOTS = ("canonical", "alt")


def m200m_of(mm):
    """sample mass as M200m [h^-1 Msun]; 500c / 200c converted with colossus diemer19 c at the sample z."""
    from colossus.cosmology import cosmology
    from colossus.halo import concentration, mass_defs
    cosmology.setCosmology("planck18")
    M, z, md = float(mm["M_hinv"]), float(mm["z"]), mm["mass_def"]
    if md == "200m":
        return M
    c = float(concentration.concentration(M, md, z, model="diemer19"))
    return float(mass_defs.changeMassDefinition(M, c, z, md, "200m")[0])


def predictable(MEAS):
    return [m for m in MEAS if m.get("M_hinv") and m.get("z") is not None and m.get("mass_def")]

if not MUTATE:
    # ============================================================== K-S0: LCDM's own ratio from our S0 boxes
    P("\n== K-S0 (gate): DK14 pipeline (3D, sigma_bin 0.05, 0.2-10 Mpc/h, priors) on CFG504 S0 512^3 stacks vs colossus more15")
    from colossus.cosmology import cosmology
    from colossus.halo import concentration, mass_defs, splashback
    cosmology.setCosmology("planck18")
    K5 = json.load(open(os.path.join(C.CFG, "CFG504_smooth_halo_transition", "cfg504_calib_results.json")))["fits"]

    def fit3d(r, rho_over_mean, M200m, z):
        p0, info = LB.fiducial(M200m, z)
        ld = np.log(rho_over_mean * LB.RHOM)

        def res(v):
            p = dict(p0); p.update(zip(C.FREE, v))
            m = np.log(LB.RHOM + C.dk14(p, r, info["r200m"]))
            return np.concatenate([(m - ld) / 0.05, [(p[k] - p0[k]) / s for k, s in C.PRI.items()]])
        from scipy.optimize import least_squares
        best = None
        v0 = np.array([p0[k] for k in C.FREE])
        for frt, dse in ((1.0, 0.0), (1.3, 0.3), (1 / 1.3, -0.3)):
            v = v0.copy(); v[C.FREE.index("lnrt")] += math.log(frt); v[C.FREE.index("se")] += dse
            sol = least_squares(res, v, x_scale=np.array([C.XS[k] for k in C.FREE]), max_nfev=3000)
            if best is None or sol.cost < best.cost: best = sol
        p = dict(p0); p.update(zip(C.FREE, best.x))
        return p, info, p0, float(2 * best.cost)

    ks0 = {}; ok_all = True
    for run in ("S0_512_a", "S0_512_b"):
        for b in ("R3", "R4"):
            d = K5[run][b]
            r = np.array(d["r"]); xi = np.array(d["xi"]); m = (r >= 0.2) & (r <= 10.0)
            M200c = 10 ** d["logM200c_med_Msun"] * H
            c200c = float(concentration.concentration(M200c, "200c", 0.0, model="diemer19"))
            M200m = float(mass_defs.changeMassDefinition(M200c, c200c, 0.0, "200c", "200m")[0])
            p, info, p0, chi2 = fit3d(r[m], 1 + xi[m], M200m, 0.0)
            rs_fit, edge = C.rsp(p, info["r200m"]); rs_fid, _ = C.rsp(p0, info["r200m"])
            rs_m15 = float(splashback.splashbackRadius(0.0, "200m", M=M200m, model="more15")[0]) / 1000.0
            # cross-check mass: fiducial M200m whose r_ta equals the bin's median r_ta
            rta = d["r_ta_med"]
            lMr = brentq(lambda l: LB.rta_of(LB.drho(LB.fiducial(10 ** l, 0.0)[0], LB.r200m(10 ** l))["tot"], 0.0) - rta, 12.0, 15.5, xtol=1e-4)
            rs_m15r = float(splashback.splashbackRadius(0.0, "200m", M=10 ** lMr, model="more15")[0]) / 1000.0
            rat = rs_fit / rs_m15
            ok = 0.85 <= rat <= 1.15
            ok_all &= ok
            ks0[f"{run}|{b}"] = dict(logM_ta=d["logM_ta_med"], M200m=M200m, r200m=info["r200m"], rsp_fit=rs_fit, edge=edge, rsp_more15=rs_m15,
                                     ratio_more15=rat, rsp_fid=rs_fid, ratio_fid=rs_fit / rs_fid, chi2=chi2, logM200m_rta_matched=lMr,
                                     ratio_more15_rta_matched=rs_fit / rs_m15r)
            P(f"   {run} {b}: log M_ta {d['logM_ta_med']:.2f}, log M200m {math.log10(M200m):.2f} (r_ta-matched {lMr:.2f}); r_sp fit {rs_fit:.3f}"
              f"{' EDGE' if edge else ''} = {rs_fit / info['r200m']:.2f} r200m; more15 {rs_m15:.3f} -> ratio {rat:.3f} (r_ta-matched mass: "
              f"{rs_fit / rs_m15r:.3f}); DK14 fiducial {rs_fid:.3f} -> ratio {rs_fit / rs_fid:.3f}; chi2 {chi2:.1f}")
    check("K-S0 LCDM own ratio (S0 boxes / more15) in 0.85-1.15", ", ".join(f"{k} {v['ratio_more15']:.3f}" for k, v in ks0.items()), ok_all)
    RES["K_S0"] = ks0

    # ============================================================== V7 sim route / K-ROUTE
    P("\n== V7 sim route (reported): DK14 3D fits to the CFG546 stacked S0 rho_g profile and to S0 x (1 + rel), x 0.2-3.95 r_ta (512^3 clusters)")
    b546 = G["runs"]["N512_LRcan"]["bins"]["clusters"]
    rta546 = b546["rta_med"]; S0p = np.array(b546["S0_profile"]); relg = np.array(TG["canonical"])
    lMs = brentq(lambda l: LB.rta_of(LB.drho(LB.fiducial(10 ** l, 0.0)[0], LB.r200m(10 ** l))["tot"], 0.0) - rta546, 12.5, 15.5, xtol=1e-4)
    msk = (XC >= 0.2) & (XC <= 3.95)
    rr = XC[msk] * rta546
    pS, infoS, _, cS = fit3d(rr, S0p[msk], 10 ** lMs, 0.0)
    out7 = {"logM200m_rta_matched": lMs}
    for nm, rel in (("rho_g canonical 512", relg), ("rho_p canonical 512", np.array(TP["canonical"]))):
        Fp = S0p * 0 + 1 + (S0p - 1) * (1 + rel)
        pF, _, _, cF = fit3d(rr, Fp[msk], 10 ** lMs, 0.0)
        rS, eS = C.rsp(pS, infoS["r200m"]); rF, eF = C.rsp(pF, infoS["r200m"])
        an = C.predicted_ratio(10 ** lMs, 0.0, "L" if "rho_g" in nm else "G", tmpl("L" if "rho_g" in nm else "G", "canonical"))
        out7[nm] = dict(rsp_S0=rS, rsp_F=rF, ratio_sim=rF / rS, ratio_analytic=an["R"], chi2_S0=cS, chi2_F=cF, edge=bool(eS or eF))
        P(f"   {nm}: sim route r_sp S0 {rS:.3f}{' EDGE' if eS else ''}, F {rF:.3f}{' EDGE' if eF else ''} -> ratio {rF / rS:.3f}; "
          f"analytic route at the same mass (z = 0) {an['R']:.3f}  (chi2 S0 {cS:.1f}, F {cF:.1f})")
    check("K-ROUTE sim vs analytic ratio (rho_g canonical 512)",
          f"{out7['rho_g canonical 512']['ratio_sim']:.3f} vs {out7['rho_g canonical 512']['ratio_analytic']:.3f}", True, gated=False)
    RES["V7_sim_route"] = out7
    dump()

    # ============================================================== predictions per measurement
    MEAS = json.load(open(os.path.join(HERE, "cfg551_measurements.json")))["measurements"]
    P(f"\n== Predictions: {len(MEAS)} compiled measurements; R_pred = r_sp(fit framework) / r_sp(fit LCDM), same pipeline")
    RES["pred"] = {}
    from colossus.halo import splashback as _spb
    for mm in MEAS:
        if mm not in predictable(MEAS):
            P(f"\n-- {mm['id']} [{mm['method']}-{mm['selection']}] {mm['ref']}: no mass / z compiled -> no prediction ({mm['note']})")
            continue
        mid, meth, z = mm["id"], mm["method"], float(mm["z"]); M = m200m_of(mm)
        if mm.get("R_obs") is None and mm.get("rsp_obs_hinv"):
            r15 = float(_spb.splashbackRadius(z, "200m", M=M, model="more15")[0]) / 1000.0 * (1 + z)   # comoving
            P(f"   (reported only, not in criteria) r_sp,obs / more15 at this mass, comoving: {mm['rsp_obs_hinv']:.2f} / {r15:.2f} = {mm['rsp_obs_hinv'] / r15:.3f}")
            RES.setdefault("more15_constructed", {})[mid] = dict(rsp_obs=mm["rsp_obs_hinv"], rsp_more15_com=r15, ratio=mm["rsp_obs_hinv"] / r15)
        labs = []
        if M < 1e14: labs.append("TEMPLATE MASS EXTRAPOLATED")
        if z >= 0.5: labs.append("z = 0 TEMPLATE")
        P(f"\n-- {mid} [{meth}-{mm['selection']}] {mm['ref']}: z {z}, M200m {M:.2e} h^-1 Msun {('; ' + ', '.join(labs)) if labs else ''}")
        zs = max(0.75, z + 0.3)
        cpar = dict(N=16000, zl=z, zs=zs, neff=5.6, se=0.26)
        row = {"labels": labs}
        for foot in FOOTS:
            r = {}
            t0 = time.time()
            base = C.predicted_ratio(M, z, meth, tmpl(meth, foot))
            rp = C.predicted_ratio(M, z, meth, tmpl(meth, foot, sign=+1))["R"]
            rm = C.predicted_ratio(M, z, meth, tmpl(meth, foot, sign=-1))["R"]
            r["primary"] = dict(base, sig_pred=abs(rp - rm) / 2)
            b2 = C.predicted_ratio(M, z, meth, tmpl(meth, foot, "256"))
            rp2 = C.predicted_ratio(M, z, meth, tmpl(meth, foot, "256", sign=+1))["R"]
            rm2 = C.predicted_ratio(M, z, meth, tmpl(meth, foot, "256", sign=-1))["R"]
            r["V1_256"] = dict(b2, sig_pred=abs(rp2 - rm2) / 2)
            sp = r["primary"]["sig_pred"]
            for s in (1.25, 1.55):
                r[f"V2_s{s}"] = dict(C.predicted_ratio(M, z, meth, tmpl(meth, foot, s=s)), sig_pred=sp)
            for sb in (0.02, 0.10):
                r[f"V3_sb{sb}"] = dict(C.predicted_ratio(M, z, meth, tmpl(meth, foot), sig_bin=sb), sig_pred=sp)
            r["V4_range"] = dict(C.predicted_ratio(M, z, meth, tmpl(meth, foot), rng=(0.3, 30.0)), sig_pred=sp)
            if meth == "L":
                r["V5_cov"] = dict(C.predicted_ratio(M, z, meth, tmpl(meth, foot), cov_par=cpar), sig_pred=sp)
                r["V6_cfg495"] = dict(C.predicted_ratio(M, z, meth, tmpl(meth, foot, "cfg495")), sig_pred=sp)
            row[foot] = r
            P(f"   {foot:9s}: R_pred {r['primary']['R']:.3f} +- {sp:.3f} (r_sp {r['primary']['rsp_L']:.3f} -> {r['primary']['rsp_F']:.3f} h^-1 Mpc, "
              f"{r['primary']['rsp_L'] / r['primary']['r200m']:.2f} -> {r['primary']['rsp_F'] / r['primary']['r200m']:.2f} r200m"
              f"{', EDGE' if r['primary']['edge'] else ''}); 256^3 {r['V1_256']['R']:.3f} +- {r['V1_256']['sig_pred']:.3f}; "
              f"soft 1.25/1.55 {r['V2_s1.25']['R']:.3f}/{r['V2_s1.55']['R']:.3f}; sb 0.02/0.10 {r['V3_sb0.02']['R']:.3f}/{r['V3_sb0.1']['R']:.3f}; "
              f"0.3-30 {r['V4_range']['R']:.3f}" + (f"; cov {r['V5_cov']['R']:.3f}; CFG495 {r['V6_cfg495']['R']:.3f}" if meth == "L" else "")
              + f"  ({time.time() - t0:.0f} s)")
        RES["pred"][mid] = row
        dump()

    # ============================================================== confrontation
    P("\n== Confrontation: Z_i = (R_pred - R_obs) / sqrt(sig_obs^2 + sig_pred^2); sig_obs on the side facing the prediction")
    CLASSES = ("L-SZX", "L-OPT", "G-SZX", "G-OPT")
    VARS = ["primary", "V1_256", "V2_s1.25", "V2_s1.55", "V3_sb0.02", "V3_sb0.1", "V4_range", "V5_cov", "V6_cfg495"]
    usable = [m for m in MEAS if m.get("R_obs") is not None and m.get("provenance") in ("SOURCE TEXT", "PROVISIONAL")]
    # overlap rule: within a class and overlap group keep the smallest mean error
    incl = {}
    for m in usable:
        cl = f"{m['method']}-{m['selection']}"
        k = (cl, m.get("overlap_group") or m["id"])
        e = 0.5 * (m["sig_lo"] + m["sig_hi"])
        if k not in incl or e < 0.5 * (incl[k]["sig_lo"] + incl[k]["sig_hi"]):
            incl[k] = m
    incl_ids = {m["id"] for m in incl.values()}
    RES["Z"] = {}; RES["class"] = {}
    for m in MEAS:
        if m["id"] not in RES["pred"]: continue
        zz = {}
        for foot in FOOTS:
            for v in VARS:
                pr = RES["pred"][m["id"]][foot].get(v)
                if pr is None or m.get("R_obs") is None: continue
                so = m["sig_hi"] if pr["R"] > m["R_obs"] else m["sig_lo"]
                zz[f"{foot}|{v}"] = dict(Z=(pr["R"] - m["R_obs"]) / math.sqrt(so ** 2 + pr["sig_pred"] ** 2), R_pred=pr["R"], sig_obs=so,
                                        sig_pred=pr["sig_pred"])
        RES["Z"][m["id"]] = zz
        st = "IN" if m["id"] in incl_ids else ("not usable" if m not in usable else "overlap: reported only")
        if zz:
            P(f"   {m['id']:10s} [{m['method']}-{m['selection']}] R_obs {m['R_obs']:.3f} (-{m['sig_lo']:.3f}/+{m['sig_hi']:.3f}, {m['provenance']}) | "
              f"Z can {zz['canonical|primary']['Z']:+.2f} (R {zz['canonical|primary']['R_pred']:.3f}), alt {zz['alt|primary']['Z']:+.2f} "
              f"(R {zz['alt|primary']['R_pred']:.3f}); 256^3 can {zz['canonical|V1_256']['Z']:+.2f}, alt {zz['alt|V1_256']['Z']:+.2f} [{st}]")
        else:
            P(f"   {m['id']:10s} [{m['method']}-{m['selection']}] no usable R_obs ({m.get('provenance')}) [{st}]")
    for cl in CLASSES:
        mem = [m for m in incl.values() if f"{m['method']}-{m['selection']}" == cl]
        out = {"members": [m["id"] for m in mem]}
        for foot in FOOTS:
            for v in VARS:
                rows = [RES["Z"][m["id"]].get(f"{foot}|{v}") for m in mem]
                rows = [(m, r) for m, r in zip(mem, rows) if r is not None]
                if not rows: continue
                w = np.array([1 / (r["sig_obs"] ** 2 + r["sig_pred"] ** 2) for _, r in rows])
                d = np.array([r["R_pred"] - m["R_obs"] for m, r in rows])
                dbar = float(np.sum(w * d) / np.sum(w)); Zc = dbar * math.sqrt(np.sum(w))
                Rp = np.array([r["R_pred"] for _, r in rows])
                S = float(np.sum(w * (Rp - 1)) / np.sum(w) * math.sqrt(np.sum(w)))
                Robs_bar = float(np.sum(w * np.array([m["R_obs"] for m, _ in rows])) / np.sum(w))
                out[f"{foot}|{v}"] = dict(n=len(rows), dbar=dbar, Z=Zc, S=S, Robs_bar=Robs_bar, sig_bar=float(1 / math.sqrt(np.sum(w))))
        RES["class"][cl] = out
        if "canonical|primary" in out:
            P(f"\n   class {cl}: members {out['members']}")
            for foot in FOOTS:
                o = out[f"{foot}|primary"]; o1 = out[f"{foot}|V1_256"]
                P(f"     {foot:9s}: mean R_obs {o['Robs_bar']:.3f} +- {o['sig_bar']:.3f}; Z primary {o['Z']:+.2f} (S {o['S']:.2f}), 256^3 {o1['Z']:+.2f} (S {o1['S']:.2f}); "
                  + ", ".join(f"{v} {out[f'{foot}|{v}']['Z']:+.2f}" for v in VARS[2:] if f"{foot}|{v}" in out))
        else:
            P(f"\n   class {cl}: no usable members")

    # ============================================================== verdict (frozen)
    def verdict(cl):
        o = RES["class"].get(cl, {})
        if "canonical|primary" not in o:
            return "NOT DIAGNOSTIC (no clean data)", {}
        Z = lambda f, v: o[f"{f}|{v}"]["Z"]
        per = {}
        for f in FOOTS:
            zp, z1 = Z(f, "primary"), Z(f, "V1_256")
            zs = [Z(f, "V2_s1.25"), Z(f, "V2_s1.55")]
            S = o[f"{f}|primary"]["S"]
            if zp >= 3 and z1 >= 3 and min(zs) >= 3: per[f] = (5, "EXCLUDED")
            elif zp >= 2 and z1 >= 2: per[f] = (4, f"TENSION (Z {zp:.2f})")
            elif zp >= 2: per[f] = (3, f"NOT DIAGNOSTIC (template non-convergence; Z {zp:.2f} at 512^3, {z1:.2f} at 256^3)")
            elif abs(zp) < 2 and S < 2: per[f] = (1, f"NOT DIAGNOSTIC (data precision; S {S:.2f})")
            elif abs(zp) < 2 and abs(z1) < 2: per[f] = (2, "CONSISTENT")
            else: per[f] = (1, f"NOT DIAGNOSTIC (Z {zp:.2f} at 512^3, {z1:.2f} at 256^3)")
        lab = min(per.values())[1]
        return lab, {f: v[1] for f, v in per.items()}

    P("\n== Verdicts (frozen rule; L-SZX sets the lane verdict)")
    RES["verdicts"] = {}
    for cl in CLASSES:
        lab, per = verdict(cl)
        extra = []
        o = RES["class"].get(cl, {})
        if "canonical|primary" in o:
            if o["canonical|primary"]["n"] < 3: extra.append("FEW MEASUREMENTS")
            for f in FOOTS:
                base_lab = per[f]
                for v in ("V3_sb0.02", "V3_sb0.1", "V4_range", "V5_cov"):
                    if f"{f}|{v}" not in o: continue
                    zp = o[f"{f}|{v}"]["Z"]
                    if (zp >= 2) != (o[f"{f}|primary"]["Z"] >= 2):
                        extra.append(f"NOT ROBUST ({f} {v})"); break
        if cl == "G-OPT" and "canonical|primary" in RES["class"].get("G-SZX", {}) and "canonical|primary" in o:
            a, b = o["canonical|primary"], RES["class"]["G-SZX"]["canonical|primary"]
            if abs(a["Robs_bar"] - b["Robs_bar"]) > math.hypot(a["sig_bar"], b["sig_bar"]): extra.append("SELECTION-DOMINATED")
        RES["verdicts"][cl] = dict(verdict=lab, per_footing=per, labels=sorted(set(extra)))
        P(f"   {cl}: {lab}  per footing {per}  labels {sorted(set(extra))}{'  <- LANE VERDICT' if cl == 'L-SZX' else ' (reported)'}")

else:
    # ============================================================== MUTATE
    MEAS = predictable(json.load(open(os.path.join(HERE, "cfg551_measurements.json")))["measurements"])
    P("\n== MUTATE-0 (gate): template zero; fits start only from the perturbed points; R_pred must be 1 +- 0.01")
    worst = 0.0
    for mm in MEAS:
        M, z = m200m_of(mm), float(mm["z"])
        for meth in ("L", "G"):
            p0, info = LB.fiducial(M, z); e = C.edges_for(0.2, 10.0)
            d0 = C.observe(C.framework_tot(p0, info, None), meth, e)
            v0 = np.array([p0[k] for k in C.FREE]); st = []
            for frt, dse in ((1.3, 0.3), (1 / 1.3, -0.3)):
                v = v0.copy(); v[C.FREE.index("lnrt")] += math.log(frt); v[C.FREE.index("se")] += dse; st.append(v)
            pf, _ = C.fit(d0, p0, info, meth, e, starts=st)
            R = C.rsp(pf, info["r200m"])[0] / C.rsp(p0, info["r200m"])[0]
            worst = max(worst, abs(R - 1))
    check("MUTATE-0 zero shell", f"max |R_pred - 1| = {worst:.4f} over {len(MEAS)} measurements x 2 methods", worst <= 0.01)

    P("\n== MUTATE-SHUF (gate): CFG546 shuffled-centre rho_g template (512^3 canonical clusters); |R_pred - 1| <= 0.05")
    GM = json.load(open(os.path.join(D546, "cfg546_predict_MUTATE_results.json")))
    tsh = LB.Template(GM["xc"], GM["runs"]["N512_LRcan"]["bins"]["clusters"]["rel"])
    worst = 0.0; rs = []
    for mm in MEAS:
        R = C.predicted_ratio(m200m_of(mm), float(mm["z"]), "L", tsh)["R"]; rs.append(R); worst = max(worst, abs(R - 1))
    check("MUTATE-SHUF shuffled centres", f"R_pred {min(rs):.3f}-{max(rs):.3f}; max |R - 1| = {worst:.4f}", worst <= 0.05)

    P("\n== MUTATE-FULL (gate): CFG546's linear-bias r_sp shift re-run with its own lib, setups and constructed covariances")
    F546 = json.load(open(os.path.join(D546, "cfg546_forecast_results.json")))
    D = {"D1": (6500, 0.40, 14.3, 6.0, 0.27, 0.75, "clusters"), "D2": (16000, 0.42, 14.3, 5.6, 0.26, 0.75, "clusters"),
         "D3": (5500, 0.24, 14.3, 1.2, 0.36, 0.40, "clusters"), "D4": (1800, 0.50, 14.1, 15.0, 0.24, 1.0, "clusters"),
         "D6": (2200, 0.30, 14.4, 6.0, 0.26, 0.75, "clusters"), "D7": (700, 0.55, 14.8, 5.6, 0.26, 0.85, "clusters"),
         "D8": (1000, 0.50, 14.6, 5.6, 0.26, 0.85, "clusters")}
    worst = 0.0; RES["mutate_full"] = {}
    for did, (N, zl, lM, neff, se, zs, tcl) in D.items():
        p0, info = LB.fiducial(10 ** lM, zl)
        e = np.geomspace(0.3, 30.0, 16)
        dsf = LB.model(p0, info, None, e)
        Cv = LB.constructed_cov(dsf, e, dict(N=N, zl=zl, zs=zs, neff=neff, se=se))
        Cinv = np.linalg.inv(Cv); pri = LB.priors(p0)
        for foot in FOOTS:
            tm = LB.Template(XC, TG[foot])
            J = LB.jacobian(p0, info, tm, e)
            p1 = dict(p0); p1["A"] = 1.0
            delta = LB.model(p1, info, tm, e) - LB.model(p0, info, tm, e)
            b = LB.bias_baseline(J, Cinv, pri, delta)
            pb = dict(p0); [pb.__setitem__(k, p0[k] + v) for k, v in b.items()]
            sh = LB.rsp_of(LB.drho(pb, info["r200m"])["tot"]) / LB.rsp_of(LB.drho(p0, info["r200m"])["tot"]) - 1
            ref = F546["forecast"][did]["rows"][f"extended|{foot}|R5_512"]["primary"]["rsp_shift_frac"]
            nl = C.predicted_ratio(10 ** lM, zl, "L", tm, rng=(0.3, 30.0))["R"] - 1
            nlc = C.predicted_ratio(10 ** lM, zl, "L", tm, rng=(0.3, 30.0), cov_par=dict(N=N, zl=zl, zs=zs, neff=neff, se=se))["R"] - 1
            worst = max(worst, abs(sh - ref))
            RES["mutate_full"][f"{did}|{foot}"] = dict(linear=sh, cfg546=ref, nonlinear_sigbin=nl, nonlinear_cov=nlc)
            P(f"   {did} {foot:9s}: linear shift {100 * sh:+.1f}% (CFG546 JSON {100 * ref:+.1f}%); nonlinear fit, 0.3-30, sigma_bin 0.05: "
              f"{100 * nl:+.1f}%, constructed covariance: {100 * nlc:+.1f}%")
            dump()
    check("MUTATE-FULL reproduces CFG546 linear shifts", f"max |diff| = {worst:.4f} (gate 0.005)", worst <= 0.005)

dump()
