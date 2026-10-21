#!/usr/bin/env python3
"""CFG942 harness for GS4_24110 (ALMA 2025.1.01377.L, [CI](2-1) + dust, public 2026-11-28).
Reads the frozen plan campaign_fresh_gravity/CFG809_gs4_24110_ci21_scoring/FROZEN_CRITERIA.md (966d50a87), the CFG571 seal
(259f7825c, be27457d...) and CFG572's public routes; edits none of them.  Criteria of this lane: FROZEN_CRITERIA.md (556c36582).
  python3 -B cfg942_gs4.py --selftest                                  K1-K5, reproduction, transcription, C4, C5, MOCK-JSON classes, power, forecast
  python3 -B cfg942_gs4.py --make-mock a|b|e --scratch DIR             write the MOCK [CI] cube + continuum (seeded; OBJECT='MOCK')
  python3 -B cfg942_gs4.py --mock a|b|e --scratch DIR [--mutate]       score that MOCK from FITS, exactly as real data
  python3 -B cfg942_gs4.py --cube CI21.fits --cont CONT.fits [--mutate]   release day (after the owner's yes and the download)
  python3 -B cfg942_gs4.py --measured MEAS.json                        score measured quantities only
kappa = 1/2 FITTED; footings never pooled; routes never averaged; one disc = a demonstration, no exclusion; not theory closed."""
import os, sys, json, math
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg942_common as C

PLAN = "campaign_fresh_gravity/CFG809_gs4_24110_ci21_scoring/FROZEN_CRITERIA.md"
RA, DEC = 53.166889, -27.798733                    # CFG809 section 1
Z_LINE = 1.9975                                    # CFG809 G1 window centre (CO(6-5) redshift)
NU_REST = 809.342; NU_OBS = NU_REST / (1 + Z_LINE)
VWIN, VCONT = 300.0, 600.0                         # CFG809 G1: +-300 km/s window; continuum = median of line-free channels |v| > 600
RING = 6.5                                         # harness default: ring radius inside CFG809's 5-8 arcsec
BOX, CUBE_HALF = 10.5, 2.6
KPA = C.kpc_per_arcsec(Z_LINE)
RE = C.GS4["R"]; RD = C.GS4["Rd"]
G = 4.30091e-6
ARGS = sys.argv[1:]
def opt(k, d=None):
    return ARGS[ARGS.index(k) + 1] if k in ARGS else d


NS = C.load_cfg571()
SEAL = C.sealed()["GS4_24110"]
J572 = json.load(open(os.path.join(C.REPO, "campaign_fresh_gravity/CFG572_gs4_24110_gas_now/cfg572_gas_results.json")))["measured"]


# ------------------------------------------------------------------------------------------------ the frozen comparison (CFG809 section 4)
def v2s(lm, R=RE): return float(NS["v2_exp"](10 ** lm, RD, R))
def v2g(lg, Rg, R=RE): return float(NS["v2_exp"](10 ** lg, Rg, R)) if lg is not None else 0.0


def vreq2(key, lm, Vc=None):
    """V_bar,req^2 at R_e: the sealed number at V_c 206 (never recomputed); the CFG571 functions only for the [CI] V_c branch (3.4)"""
    if Vc is None:
        return 10 ** SEAL[str(lm)][key]["logVbar2R_G"] * G / RE
    return 10 ** C.predict(NS, RE, Vc, C.GS4["z"], lm, RD)[key]["logVbar2R_G"] * G / RE


def floor_at(key, lm, Vc=None, dm=0.0):
    return vreq2(key, lm, Vc) - v2s(lm + dm) <= 0


def delta_v(route, key, lm, Rg, Vc=None):
    """route: dict(logMgas, sig_flux_dex, detected). Returns Delta_v, sigma, wording (CFG809 s4; FLOOR rule; one-sided for limits)."""
    vr = vreq2(key, lm, Vc); g = route["logMgas"]; sg = math.hypot(route["sig_flux_dex"], 0.2)
    f = lambda dg, dm: math.log10((v2s(lm + dm) + v2g(g + dg if g is not None else None, Rg)) / vr)
    fl = floor_at(key, lm, Vc)
    out = dict(model=key.split("|")[1], foot=key.split("|")[0], Mstar=lm, floor=fl)
    if route["detected"]:
        D = f(0, 0); s = 0.5 * math.hypot(f(sg, 0) - f(-sg, 0), f(0, 0.2) - f(0, -0.2))
        w = "consistent with" if abs(D) <= 2 * s else "in tension with"
        out.update(Delta=D, sigma=s, wording_dv=w)
        if fl:
            red = not floor_at(key, lm, Vc, -0.2)
            out.update(wording="in tension with (FLOOR)", reduced=("not FLOOR at M*-0.2: tension REDUCED" if red else "FLOOR persists at M*-0.2"),
                       floor_overrides=(w == "consistent with"))
        else:
            out.update(wording=w)
    else:                                                  # upper limit: Delta_v in [f(gas = 0), f(UL)]
        fs = lambda dm: math.log10(v2s(lm + dm) / vr)
        Dmax = f(0, 0); Dmin = fs(0)
        s = 0.5 * math.hypot(f(sg, 0) - f(-sg, 0), f(0, 0.2) - f(0, -0.2))
        w = "in tension with (too few baryons even at the limit)" if Dmax < -2 * s else ("in tension with (stars alone exceed)" if Dmin > 2 * s else "consistent with (one-sided)")
        out.update(Delta=Dmax, Delta_min=Dmin, sigma=s, wording=w, wording_dv=w, upper_limit=True)
    return out


def tense(w): return w.startswith("in tension")


def side(rows):
    cl = {r["model"]: r["wording"] for r in rows}
    fw_ok = any(not tense(cl[m]) for m in C.FRAMEWORK); rv_t = tense(cl[C.RIVAL])
    if fw_ok and rv_t: return "FRAMEWORK SIDE"
    if (not rv_t) and all(tense(cl[m]) for m in C.FRAMEWORK): return "RIVAL SIDE"
    return "NO SIDE"


def routes_from(meas):
    """CI21 (new) + CFG572's public routes, re-quoted unchanged (CO43, CI10 limit, dust)"""
    r = {}
    for X in ("1.9e-5", "3.0e-5"):
        r[f"CI21 X{X}"] = dict(logMgas=meas["CI21"]["logMgas"][X], sig_flux_dex=meas["CI21"]["sig_flux_dex"], detected=meas["CI21"]["detected"])
    co = J572["CO43"]; sf = 0.4343 * co["sig"] / co["S"]
    for k in ("r41 0.37", "r41 0.25", "r41 0.55"):
        r[f"CO43 {k}"] = dict(logMgas=co["logM"][k], sig_flux_dex=sf, detected=True, requoted=True)
    for k in ("X_CI 1.9e-5", "X_CI 3.0e-5"):
        r[f"CI10 {k} (limit)"] = dict(logMgas=J572["CI10"]["logM"][k], sig_flux_dex=0.0, detected=False, requoted=True)
    du = J572["DUST"]["logM"]
    r["D alphaCO 4.36"] = dict(logMgas=du["alphaCO 4.36 (primary)"], sig_flux_dex=0.4343 * 3.2 / 32.1, detected=True, requoted=True)
    r["D Scoville 6.5"] = dict(logMgas=du["Scoville alphaCO 6.5"], sig_flux_dex=0.4343 * 3.2 / 32.1, detected=True, requoted=True)
    return r


PRIMARY_ROUTE, ROBUST_ROUTES = "CI21 X1.9e-5", ("CO43 r41 0.37", "D alphaCO 4.36")


def score(meas, run):
    run.P("\n=== SCORE (CFG809 section 4; single disc = demonstration; routes, footings, M* and shapes never pooled; no exclusion) ===")
    R = routes_from(meas); res = dict(routes=R, rows=[], sides={}, robust={})
    shapes = {"Rg=Rd": RD, "Rg=1.5Rd": 1.5 * RD}
    if meas.get("G3") and meas.get("Rg_meas_kpc"):
        shapes = {"measured": meas["Rg_meas_kpc"], **shapes}
    run.P("  routes: " + "; ".join(f"{k} {'<' if not v['detected'] else ''}{v['logMgas']:.2f}" + (" (re-quoted CFG572)" if v.get("requoted") else "") for k, v in R.items()))
    run.P(f"  gas shapes: " + ", ".join(f"{k} R_g {v:.2f} kpc" for k, v in shapes.items()) + ("   (G3 passed: the measured size is primary)" if "measured" in shapes else "   (G3 not passed: CFG571 shapes)"))
    vc_branches = {"V_c 206 (RC100, sealed)": None}
    for b, (V, eV) in meas.get("ci_vc", {}).items():
        vc_branches[f"V_c {b} {V:.1f}+-{eV:.1f} ([CI] branch, recomputed)"] = V
    for vb, Vc in vc_branches.items():
        for rn, rt in R.items():
            for lm in C.GS4["lmstars"]:
                for shn, Rg in shapes.items():
                    for f in C.FOOTS:
                        rows = [delta_v(rt, f"{f}|{m}", lm, Rg, Vc) for m in C.MODELS]
                        for r in rows: r.update(route=rn, shape=shn, vc=vb)
                        res["rows"] += rows; res["sides"][f"{vb}|{rn}|{lm}|{shn}|{f}"] = side(rows)
    prim_shape = "measured" if "measured" in shapes else "Rg=Rd"
    # robustness flag (frozen): CI21 verdict ROBUST only if the same wording holds on every other route with a detection
    for vb in vc_branches:
        for lm in C.GS4["lmstars"]:
            for shn in shapes:
                for f in C.FOOTS:
                    for m in C.MODELS:
                        get = lambda rn: next(r for r in res["rows"] if r["vc"] == vb and r["route"] == rn and r["Mstar"] == lm and r["shape"] == shn and r["foot"] == f and r["model"] == m)
                        p = get(PRIMARY_ROUTE)
                        if not R[PRIMARY_ROUTE]["detected"]:
                            res["robust"][f"{vb}|{lm}|{shn}|{f}|{m}"] = "NO CI21 DETECTION (no primary verdict to qualify)"; continue
                        same = all(tense(get(o)["wording"]) == tense(p["wording"]) for o in ROBUST_ROUTES if R[o]["detected"])
                        res["robust"][f"{vb}|{lm}|{shn}|{f}|{m}"] = "ROBUST" if same else "NOT ROBUST"
    for vb in vc_branches:
        run.P(f"\n  [{vb}]")
        for lm in C.GS4["lmstars"]:
            for f in C.FOOTS:
                run.P(f"    M* {lm} | {f} | shape {prim_shape}:")
                for rn in [PRIMARY_ROUTE] + list(ROBUST_ROUTES):
                    sel = [r for r in res["rows"] if r["vc"] == vb and r["route"] == rn and r["Mstar"] == lm and r["shape"] == prim_shape and r["foot"] == f]
                    cells = []
                    for r in sel:
                        c = f"{r['model']} {r['Delta']:+.2f}+-{r['sigma']:.2f} {r['wording']}"
                        if r.get("floor_overrides"): c += " [Delta_v alone: consistent]"
                        if r["floor"] and "reduced" in r: c += f" [{r['reduced']}]"
                        if rn == PRIMARY_ROUTE: c += f" <{res['robust'][f'{vb}|{lm}|{prim_shape}|{f}|{r['model']}']}>"
                        cells.append(c)
                    run.P(f"      {rn:15s}: " + "; ".join(cells) + f"  => {res['sides'][f'{vb}|{rn}|{lm}|{prim_shape}|{f}']}")
        tally = {}
        for k, v in res["sides"].items():
            if k.startswith(vb + "|" + PRIMARY_ROUTE + "|"): tally[v] = tally.get(v, 0) + 1
        run.P(f"    CI21 primary-route sides over M* x shape x footing: {tally}")
    if any(r.get("floor_overrides") for r in res["rows"]):
        run.flag("A-G2", "a FLOOR model with detected gas reads 'in tension' by CFG809's FLOOR rule although its |Delta_v| <= 2 sigma (the two rules disagree; the harness prints both)")
    res["primary_side"] = res["sides"][f"V_c 206 (RC100, sealed)|{PRIMARY_ROUTE}|10.89|{prim_shape}|canon 9.36e-11"]
    res["primary_shape"] = prim_shape
    return res


# ------------------------------------------------------------------------------------------------ measurement (CFG809 section 3)
def detect(m0d, run, tag=""):
    m0, pix, beam = m0d["m0"], m0d["pix"], m0d["beam"]; bp = C.beam_pix(beam, pix); xc, yc = m0d["xc"], m0d["yc"]
    r = C.radius_map(m0.shape, xc, yc) * pix
    s0 = C.robust_std(m0[r > 2.5]); mask = C.make_mask(m0, s0, xc, yc, pix)
    rng = np.random.default_rng(942)
    aper = mask if mask.sum() else (r <= RE / KPA)
    ring = C.translated_apertures(m0, aper, bp, C.ring_offsets(RING / pix, 8))
    rms = float(np.std(ring, ddof=1)) if len(ring) > 2 else float("nan")
    S = float(np.nansum(m0[aper]) / bp)
    rmax = float(np.max(r[aper]))
    nul = C.seeded_null(m0, s0, mask, xc, yc, pix, bp, rmax + 0.8, 200, rng)
    mu_n, sd_n = (float(np.mean(nul)), float(np.std(nul, ddof=1))) if len(nul) > 2 else (float("nan"), float("nan"))
    SN = S / rms if rms > 0 else float("nan"); SNsel = (S - mu_n) / sd_n if sd_n > 0 else float("nan")
    det = bool(mask.sum() and np.isfinite(SNsel) and SNsel >= 5); det_lit = bool(mask.sum() and np.isfinite(SN) and SN >= 5)
    d = dict(S=S, ring_rms=rms, n_ring=len(ring), SN=SN, SN_selection=SNsel, null_mean=mu_n, null_sd=sd_n, detected=det, detected_literal=det_lit,
             mask_pix=int(mask.sum()), sig_mom0=s0, mask_rmax_arcsec=rmax)
    run.P(f"  {tag}G1 [CI](2-1): S dv {S:.5f} Jy km/s in the >= 2 sigma moment-0 mask ({int(mask.sum())} px); ring rms {rms:.5f} ({len(ring)} apertures at {RING}\") -> S/N {SN:.1f}; "
          f"selection-aware null ({len(nul)} seeds): mean {mu_n:.5f}, sd {sd_n:.5f} -> S/N {SNsel:.1f} -> {'DETECTED' if det else 'NOT DETECTED'} (literal ring S/N reading: {'DETECTED' if det_lit else 'NOT DETECTED'})")
    if det != det_lit:
        run.flag("A-G13", "G1 differs between the selection-aware S/N (harness default) and the ring-aperture S/N: the >= 2 sigma mask selects positive noise")
    return d, mask, r, rng


def measure(path, cont_path, run, vshift=0.0, c1=True, truth=None):
    run.P(f"\n=== MEASUREMENT (CFG809 section 3) of {os.path.basename(path)}{'  [MUTATE: velocity axis +2000 km/s]' if vshift else ''} ===")
    m0d = C.stream_mom0(path, RA, DEC, NU_OBS, BOX, VWIN, VCONT, vshift)
    if m0d["beam"] is None: raise SystemExit("C3: no beam (no BMAJ keyword and no BEAMS table): cannot proceed")
    if m0d["beam_source"] != "header": run.flag("A-M2", "per-plane beams (BEAMS table): the harness uses their median")
    run.P(f"  file sha256 {m0d['sha256'][:16]}…; OBJECT '{m0d['object']}'; pixel {m0d['pix']:.4f}\"; beam {m0d['beam'][0]:.3f}x{m0d['beam'][1]:.3f}\" ({m0d['beam_source']}); dv {m0d['dv']:.1f} km/s; "
          f"v coverage {m0d['v_cover'][0]:.0f}..{m0d['v_cover'][1]:.0f}; window |v| <= 300 ({m0d['nwin']} ch); continuum {m0d['ncont']} ch")
    if m0d["object"] == "MOCK": run.P("  *** MOCK cube (generated by this harness; NOT ALMA DATA) ***")
    cov = m0d["nu_cover"][0] <= 270.0 <= m0d["nu_cover"][1] or m0d["nu_cover"][0] <= NU_OBS <= m0d["nu_cover"][1]
    run.check("C3 frequency axis covers 270.0 GHz; beam and channel keywords exist", cov and m0d["beam"] is not None and np.isfinite(m0d["dv"]), f"[CI](2-1) observed {NU_OBS:.4f} GHz")
    if not m0d["win_covered"]:
        run.P("  the window |v| <= 300 km/s is not covered by the cube" + (" after the MUTATE shift" if vshift else ""))
    m, mask, r, rng = detect(m0d, run)
    m.update(file=m0d["file"], sha256=m0d["sha256"], object=m0d["object"], win_covered=m0d["win_covered"])
    cube = C.load_box(path, RA, DEC, NU_OBS, CUBE_HALF, 650.0, VCONT, vshift)
    if m["detected"]:
        ms, lost = C.sub_mask(mask, m0d, cube); win = np.abs(cube["v"]) <= VWIN
        spec = np.nansum(cube["data"][win][:, ms], axis=1); vv = cube["v"][win]; sp = np.clip(spec, 0, None)
        vcen = float((sp * vv).sum() / sp.sum()) if sp.sum() > 0 else float("nan"); zl = Z_LINE + (1 + Z_LINE) * vcen / C.CKMS
        m.update(z_line=zl)
        run.check("C3 detected line redshift 1.9975 +- 0.002", abs(zl - Z_LINE) <= 0.002, f"z {zl:.5f}")
    # C2: five off-source apertures in the line window
    aper = mask if mask.sum() else (r <= RE / KPA)
    bp = C.beam_pix(m0d["beam"], m0d["pix"])
    off5 = C.translated_apertures(m0d["m0"], aper, bp, [(7 / m0d["pix"] * math.cos(t), 7 / m0d["pix"] * math.sin(t)) for t in (0.3, 1.5, 2.7, 3.9, 5.1)])
    if np.isfinite(m["ring_rms"]):
        run.check("C2 five off-source apertures in the line window consistent with zero (|S dv| < 3 sigma)", len(off5) == 5 and all(abs(x) < 3 * m["ring_rms"] for x in off5), str(np.round(off5, 5).tolist()))
    # 3.3 CI21 gas mass (or the 3 sigma limit in a circle of radius R_e: harness default)
    if m["detected"]:
        S = m["S"]; sf = 0.4343 * m["ring_rms"] / S
    else:
        circ = r <= RE / KPA; ring = C.translated_apertures(m0d["m0"], circ, bp, C.ring_offsets(RING / m0d["pix"], 8))
        rc = float(np.std(ring, ddof=1)) if len(ring) > 2 else float("nan"); S = 3 * rc; sf = 0.0
        run.P(f"  G1 not passed: 3-sigma upper limit in a circle of radius R_e = {RE / KPA:.2f}\": S dv < {S:.5f} Jy km/s")
        run.flag("A-G5", "the non-detection limit aperture is not stated in CFG809; the harness uses a circle of radius R_e = 0.88 arcsec with the same ring noise")
    m["CI21"] = dict(detected=m["detected"], S=S, sig_flux_dex=sf,
                     logMgas={X: math.log10(C.mgas_ci21(S, Z_LINE, NU_OBS, X=float(X))) if S > 0 else float("nan") for X in ("1.9e-5", "3.0e-5")},
                     logMgas_Tex40_info=math.log10(C.mgas_ci21(S, Z_LINE, NU_OBS, X=1.9e-5, T=40.0)) if S > 0 else float("nan"))
    run.P(f"  3.3 CI21: log M_gas {'<' if not m['detected'] else ''}{m['CI21']['logMgas']['1.9e-5']:.3f} (X_CI 1.9e-5, T_ex 25 K) / {m['CI21']['logMgas']['3.0e-5']:.3f} (3.0e-5); "
          f"T_ex 40 K information only {m['CI21']['logMgas_Tex40_info']:.3f}; flux error {sf:.3f} dex (+ 0.2 dex route systematic in the score)")
    if truth: run.P(f"  MOCK truth: log M_gas {truth.get('lg')}; S dv {truth.get('S', 0):.5f} Jy km/s; recovered/true flux {m['S'] / truth['S']:.3f}" if truth.get("S") else f"  MOCK truth: zero line flux")
    # 3.1 continuum
    if cont_path:
        im = C.load_image(cont_path, RA, DEC, BOX)
        rr = C.radius_map(im["img"].shape, im["xc"], im["yc"]) * im["pix"]; sc = C.robust_std(im["img"][rr > 2.5])
        cm = remap(mask if mask.sum() else (r <= RE / KPA), m0d, im)
        pk = float(np.nanmax(im["img"][cm])) / sc if cm.sum() else float("nan"); tot = float(np.nansum(im["img"][cm]) / C.beam_pix(im["beam"], im["pix"]))
        m["cont"] = dict(peak_SN=pk, flux_in_mask=tot, rms=sc, file=im["file"], sha256=im["sha256"])
        line = f"  3.1 continuum ({im['file']}): peak S/N {pk:.1f} in the {'[CI] mask' if mask.sum() else 'R_e circle'}; flux in it {tot * 1e6:.1f} uJy"
        if pk >= 5:
            gc = C.fit_gauss2d(im["img"], sc, im["pix"], im["beam"], im["xc"], im["yc"], half=2.0)
            m["cont"].update(fwhm_maj=gc["fwhm_maj"], fwhm_min=gc["fwhm_min"], fwhm_circ=gc["fwhm_circ"], efwhm_circ=gc["efwhm_circ"], R_e_kpc=gc["fwhm_circ"] / 2 * KPA)
            line += f"; beam-convolved Gaussian FWHM {gc['fwhm_maj']:.3f}x{gc['fwhm_min']:.3f}\" (circ {gc['fwhm_circ']:.3f} +- {gc['efwhm_circ']:.3f}; R_e {gc['fwhm_circ'] / 2 * KPA:.2f} kpc)"
        run.P(line)
        run.flag("A-G6", "3.1 'peak S/N ... If S/N >= 5' is read as the peak S/N of the continuum image inside the [CI] mask (R_e circle if no [CI] detection)")
    if not m["detected"]:
        m["G3"] = False; return m
    # 3.2 gas size (G3)
    gf = C.fit_gauss2d(m0d["m0"], m["sig_mom0"], m0d["pix"], m0d["beam"], m0d["xc"], m0d["yc"], half=2.5)
    G3 = bool(gf["fwhm_circ"] > 2 * gf["efwhm_circ"] and m["detected"])
    Re_ci = gf["fwhm_circ"] / 2 * KPA
    m.update(gauss=gf, G3=G3, Re_CI_kpc=Re_ci, Rg_meas_kpc=Re_ci / 1.678 if G3 else None)
    run.P(f"  3.2 [CI] size: beam-convolved Gaussian FWHM {gf['fwhm_maj']:.3f}x{gf['fwhm_min']:.3f}\" (circ {gf['fwhm_circ']:.3f} +- {gf['efwhm_circ']:.3f}; x{gf['corr_factor']:.1f} if pixel "
          f"correlation is counted) -> R_e,CI {Re_ci:.2f} kpc, R_g {Re_ci / 1.678:.2f} kpc; G3 {'PASS' if G3 else 'FAIL'}")
    if truth and truth.get("Rg"): run.P(f"  MOCK truth: R_g {truth['Rg']:.2f} kpc (exponential); recovered/true {Re_ci / 1.678 / truth['Rg']:.3f}  (a Gaussian fit to an exponential disc is biased)")
    run.flag("A-G9", "G3 uses the fit covariance (independent pixels); with beam-correlated noise the FWHM error is underestimated by about sqrt(pixels per beam)")
    # 3.4 kinematics branch (G4)
    ms, _ = C.sub_mask(mask, m0d, cube)
    m0s = np.nansum(cube["data"][np.abs(cube["v"]) <= VWIN], axis=0) * cube["dv"]
    pa0, vs0, amp, m1 = C.kinematic_pa(cube, m0s, ms, VWIN, cube["xc"], cube["yc"])
    g4, prof = gradient_gate(cube, m0s, m1, m["sig_mom0"] * 1.0, pa0, gf)
    m["G4"] = g4; m["G4_profile"] = prof
    run.P(f"  3.4 G4 (moment-1 monotonic over >= 2 beams at S/N >= 5): {'PASS' if g4 else 'FAIL'}; samples {prof}")
    run.flag("A-G12", "G4 is implemented as >= 3 consecutive beam-spaced samples along the kinematic axis, each at moment-0 S/N >= 5, with strictly monotonic moment-1")
    if g4:
        ip, _ = C.inc_from_q(gf["q"]); fd = C.fit_disc(cube, ip, KPA, m0d["sig_ch"], (0.0, 0.0), pa0, vs0, amp / max(math.sin(math.radians(ip)), 0.2), max(gf["fwhm_maj"] / 2.5, 0.05), RE, RD, rfit=2.2)
        m["ci_fit"] = {k: v for k, v in fd.items() if k != "cov"}
        m["ci_vc"] = {"P-B": (fd["Vc_PB"], fd["eVc_PB"]), "P0": (fd["Vc_P0"], fd["eVc_P0"])}
        run.P(f"  3.4 [CI] thin-disc fit (i {ip:.1f} from the [CI] axis ratio): V_c(R_e) P-B {fd['Vc_PB']:.1f} +- {fd['eVc_PB']:.2f}, P0 {fd['Vc_P0']:.1f} +- {fd['eVc_P0']:.2f} "
              f"(sigma0 {fd['params'][6]:.1f}); a BRANCH, never pooled with 206")
    if vshift == 0 and c1:
        m["C1"] = injection(path, run, m)
    return m


def remap(mask, m0d, im):
    """nearest-neighbour map of a mask on the cube grid onto the continuum-image grid (offsets from the target in arcsec)"""
    ys, xs = np.nonzero(mask); dx, dy = (xs - m0d["xc"]) * m0d["pix"], (ys - m0d["yc"]) * m0d["pix"]
    X = np.round(im["xc"] + dx / im["pix"]).astype(int); Y = np.round(im["yc"] + dy / im["pix"]).astype(int)
    out = np.zeros(im["img"].shape, bool); ok = (X >= 0) & (Y >= 0) & (X < out.shape[1]) & (Y < out.shape[0]); out[Y[ok], X[ok]] = True
    return out


def gradient_gate(cube, m0s, m1, sig_m0, pa, gf):
    pix = cube["pix"]; bm = cube["beam"][0]; c, s = math.cos(pa), math.sin(pa)
    sm = sig_m0                                            # moment-0 noise from the wide box (same units as the sub-cube moment-0)
    vals = []
    for k in range(-4, 5):
        x, y = cube["xc"] + k * bm / pix * c, cube["yc"] + k * bm / pix * s
        ix, iy = int(round(x)), int(round(y))
        if 0 <= iy < m0s.shape[0] and 0 <= ix < m0s.shape[1] and m0s[iy, ix] >= 5 * sm:
            vals.append((k, round(float(m1[iy, ix]), 1)))
        else:
            vals.append((k, None))
    best = run_ = 0; prev = None
    for k, v in vals:
        if v is None: run_ = 0; prev = None; continue
        if prev is None or v > prev: run_ += 1
        else: run_ = 1
        prev = v; best = max(best, run_)
    return best >= 3, vals


def injection(path, run, m):
    """C1: a Gaussian source of known flux and size, 10 arcsec from the target, in the real cube's noise (added to the line-window
    moment-0, which is linear in the cube), recovered by the same mask and Gaussian-fit code."""
    out = {}
    lg = SEAL["10.89"]["canon 9.36e-11|F-DESI"]["logMgas_Rg=Rd"]
    S = C.SdV_from_Lprime(10 ** lg / (1.36 * C.mci_21(1.0, 25.0) / (6 * 1.9e-5)), NU_OBS, Z_LINE)
    fw = 0.8
    ra_off = RA + 10.0 / 3600.0 / math.cos(math.radians(DEC))
    m0d = C.stream_mom0(path, ra_off, DEC, NU_OBS, 3.0, VWIN, VCONT)
    yy, xx = np.indices(m0d["m0"].shape); X, Y = (xx - m0d["xc"]) * m0d["pix"], (yy - m0d["yc"]) * m0d["pix"]
    sg = fw / 2.3548
    m0d["m0"] = m0d["m0"] + C.gauss2d_model([S, 0.0, 0.0, math.log(sg), math.log(sg), 0.0], X, Y, C.beam_cov(m0d["beam"]), m0d["pix"], C.beam_pix(m0d["beam"], m0d["pix"]))
    q = C.Quiet(); bp = C.beam_pix(m0d["beam"], m0d["pix"])
    r = C.radius_map(m0d["m0"].shape, m0d["xc"], m0d["yc"]) * m0d["pix"]; s0 = C.robust_std(m0d["m0"][r > 2.0])
    mask = C.make_mask(m0d["m0"], s0, m0d["xc"], m0d["yc"], m0d["pix"])
    Sr = float(np.nansum(m0d["m0"][mask]) / bp) if mask.sum() else 0.0
    fr = Sr / S
    if mask.sum():
        gf = C.fit_gauss2d(m0d["m0"], s0, m0d["pix"], m0d["beam"], m0d["xc"], m0d["yc"], half=2.0); sz = gf["fwhm_circ"] / fw
    else:
        sz = float("nan")
    ok = abs(fr - 1) <= 0.2 and abs(sz - 1) <= 0.25
    run.check("C1 injection 10\" away (known log M_gas %.2f, S dv %.4f Jy km/s, FWHM %.1f\"): flux within 20%% and size within 25%%" % (lg, S, fw), ok, f"flux ratio {fr:.3f}, size ratio {sz:.3f}")
    return dict(flux_ratio=fr, size_ratio=sz, ok=ok)


def mutate(path, run):
    """MUTATE (CFG809 s5): the velocity window shifted by +2000 km/s; the flux in the true-run mask must drop below 3 sigma."""
    run.P("\n=== MUTATE (velocity window +2000 km/s) ===")
    m0d = C.stream_mom0(path, RA, DEC, NU_OBS, BOX, VWIN, VCONT, 0.0)
    d0, mask, r, _ = detect(m0d, run, tag="true z: ")
    sh = C.stream_mom0(path, RA, DEC, NU_OBS, BOX, VWIN, VCONT, 2000.0)
    if not sh["win_covered"] or sh["nwin"] == 0:
        run.P(f"  the shifted window lies outside the cube's coverage ({sh['v_cover'][0]:.0f}..{sh['v_cover'][1]:.0f} km/s after the shift): MUTATE NOT RUNNABLE AS FROZEN (exit 2)")
        run.flag("A-G11", "MUTATE +2000 km/s can leave a 1.875 GHz spectral window at 270 GHz (about +-1040 km/s); CFG572 hit the same and disclosed a +1000 variant")
        return 2
    if not d0["detected"]:
        run.P("  line not detected at the true redshift: MUTATE is NON-DIAGNOSTIC (as frozen)"); return 0
    bp = C.beam_pix(sh["beam"], sh["pix"]); Ssh = float(np.nansum(sh["m0"][mask]) / bp)
    ring = C.translated_apertures(sh["m0"], mask, bp, C.ring_offsets(RING / sh["pix"], 8)); rs = float(np.std(ring, ddof=1))
    bites = Ssh < 3 * rs
    run.P(f"  shifted flux in the true-run mask {Ssh:.5f} Jy km/s, ring rms {rs:.5f} -> {Ssh / rs:.2f} sigma -> {'below 3 sigma: the control BITES (exit 1)' if bites else 'NOT below 3 sigma'}")
    return 1 if bites else 0


# ------------------------------------------------------------------------------------------------ MOCKs
def mock_spec(kind):
    lg = {"a": SEAL["10.89"]["canon 9.36e-11|F-DESI"]["logMgas_Rg=Rd"], "b": None, "e": 11.6}[kind]
    S = 0.0 if lg is None else C.SdV_from_Lprime(10 ** lg / (1.36 * C.mci_21(1.0, 25.0) / (6 * 1.9e-5)), NU_OBS, Z_LINE)
    Sa = C.SdV_from_Lprime(10 ** SEAL["10.89"]["canon 9.36e-11|F-DESI"]["logMgas_Rg=Rd"] / (1.36 * C.mci_21(1.0, 25.0) / (6 * 1.9e-5)), NU_OBS, Z_LINE)
    inc, s0, rt = 45.0, 50.0, 1.0
    vr = math.sqrt(206.0 ** 2 - 2 * s0 ** 2 * RE / RD); vf = vr / (2 / math.pi * math.atan(RE / rt))
    pix, n, beam = 0.03, 880, (0.095, 0.085, 60.0); h = RD / KPA; qi = math.sqrt(math.cos(math.radians(inc)) ** 2 * 0.96 + 0.04); pa = math.radians(60.0)
    bp = C.beam_pix(beam, pix); yy, xx = np.indices((n, n)); X, Y = (xx - n // 2) * pix, (yy - n // 2) * pix
    xr = X * math.cos(pa) + Y * math.sin(pa); yr = -X * math.sin(pa) + Y * math.cos(pa)
    I0a = Sa * bp / np.exp(-np.sqrt(xr ** 2 + (yr / qi) ** 2) / h).sum()
    sigma = I0a / 400.0 / (20.0 * math.sqrt(int(2 * VWIN / 20) + 1))      # MOCK noise: GS4-a central moment-0 pixel S/N = 400 (NOT the archive sensitivity)
    cube = dict(ra=RA, dec=DEC, nu_line=NU_OBS, restfrq=NU_REST, pix=pix, n=n, beam=beam, dv=20.0, vlo=-1000.0, vhi=2400.0, inc=inc, pa=pa, q_int=qi, h=h,
                vf=vf, rt=rt, s0=s0, kpa=KPA, SdV=S, sigma=sigma, seed=9420 + ord(kind), label=f"CFG942 GS4 MOCK {kind}",
                true={"LOGMGAS": lg if lg is not None else -1.0, "SDV": S, "RG_KPC": RD, "VC_PB": 206.0})
    hd = 2.5 / 1.678 / KPA
    cont = dict(ra=RA, dec=DEC, pix=pix, n=n, beam=beam, pa=pa, q_int=qi, h=hd, S=478e-6, sigma=478e-6 / 2 / math.pi / (hd / pix) ** 2 * bp / qi / 30.0,
                seed=9430 + ord(kind), label=f"CFG942 GS4 MOCK {kind} continuum")
    return cube, cont, dict(lg=lg, S=S, Rg=RD)


def required(kind, m, sc, run):
    run.P("\n=== REQUIRED MOCK CLASS (CFG942 criteria section 2) ===")
    if kind == "a":
        p = sc["primary_side"]; ok = m["detected"] and p == "FRAMEWORK SIDE"
        prim = [r for r in sc["rows"] if r["vc"].startswith("V_c 206") and r["route"] == PRIMARY_ROUTE and r["Mstar"] == 10.89 and r["shape"] == sc["primary_shape"] and r["foot"].startswith("canon")]
        run.P("  primary (canonical, M* 10.89, CI21 X1.9e-5, shape %s): " % sc["primary_shape"] + "; ".join(f"{r['model']} {r['wording']}" for r in prim))
        return run.check("GS4-a FRAMEWORK: G1 PASS, F-DESI consistent, R-H and L-fb in tension (FLOOR) -> FRAMEWORK SIDE", ok and all(tense(r["wording"]) for r in prim if r["model"] in ("R-H", "L-fb(RAR-eq)"))
                         and not tense(next(r for r in prim if r["model"] == "F-DESI")["wording"]), p)
    if kind == "b":
        prim = [r for r in sc["rows"] if r["vc"].startswith("V_c 206") and r["route"] == PRIMARY_ROUTE and r["Mstar"] == 10.89 and r["shape"] == "Rg=Rd" and r["foot"].startswith("canon")]
        run.P("  primary (canonical, M* 10.89, CI21 limit, Rg=Rd): " + "; ".join(f"{r['model']} {r['wording']}" for r in prim) + f" -> {sc['primary_side']} (reported as it falls)")
        return run.check("GS4-b RIVAL-MATCHED (zero gas): G1 FAIL -> upper limit; the FLOOR rule does not fire", (not m["detected"]) and not any("FLOOR" in r["wording"] for r in prim))
    if kind == "e":
        prim = [r for r in sc["rows"] if r["vc"].startswith("V_c 206") and r["route"] == PRIMARY_ROUTE and r["Mstar"] == 10.89 and r["shape"] == sc["primary_shape"] and r["foot"].startswith("canon")]
        fd = next(r for r in prim if r["model"] == "F-DESI")
        run.P("  primary: " + "; ".join(f"{r['model']} {r['Delta']:+.2f}+-{r['sigma']:.2f} {r['wording']}" for r in prim))
        return run.check("GS4-e EXCESS GAS: F-DESI in tension", m["detected"] and tense(fd["wording"]), fd["wording"])


# ------------------------------------------------------------------------------------------------ selftest pieces
def selftest(run):
    run.P("\n=== R2 reproduction of the sealed GS4 numbers by CFG571's own functions (executed read-only) ===")
    w, n, bad = C.reproduce(NS, "GS4_24110")
    run.check("R2 reproduction <= 1e-12 dex, FLOOR flags identical", w <= 1e-12 and not bad, f"max |d| {w:.1e} over {n} entries; mismatches {bad}")
    run.P("\n=== R3 transcription: CFG809 section 2 table vs the seal ===")
    rows, worst, bad = C.transcription(PLAN, "GS4_24110")
    run.check("R3 every CFG809 s2 cell within 0.005 dex of the seal; FLOOR cells identical", rows == 4 and not bad, f"{rows} rows, worst {worst:.4f} dex, mismatches {bad}")
    tc = open(os.path.join(C.REPO, "campaign_fresh_gravity/THEORY_CANONICAL_2026-10-14.md")).read()
    run.P("  THEORY_CANONICAL_2026-10-14 s2 GS4 row quotes '9.46–10.36 (flat) / 9.82–10.43 (DE-tracking)': seal R_g=R_d values "
          f"{SEAL['10.89']['canon 9.36e-11|F-flat']['logMgas_Rg=Rd']:.2f}/{SEAL['10.76']['canon 9.36e-11|F-flat']['logMgas_Rg=Rd']:.2f} and "
          f"{SEAL['10.89']['canon 9.36e-11|F-DESI']['logMgas_Rg=Rd']:.2f}/{SEAL['10.76']['canon 9.36e-11|F-DESI']['logMgas_Rg=Rd']:.2f} (R_g = 1.5 R_d branch omitted there)")
    run.P("\n=== K4 pre-data controls of the plan ===")
    A10, A21, n10, n21 = 7.93e-8, 2.68e-7, 492.161, 809.342
    c21 = 5.706e-4 * (n21 ** 2 / A21) / (n10 ** 2 / A10)
    run.check("C4a [CI](2-1) coefficient from Einstein A values within 1% of 4.566e-4", abs(c21 / 4.566e-4 - 1) < 0.01, f"derived {c21:.6e} (rel. {c21 / 4.566e-4 - 1:+.1e}); AG5's Boogaard+20 value 4.556e-4 is {4.556e-4 / c21 - 1:+.2%} from it")
    T = 25.0; ratio = (5 / 3) * math.exp(-(62.5 - 23.6) / T) * (A21 / n21 ** 2) / (A10 / n10 ** 2)
    L10 = 1.0e8; L21 = ratio * L10
    m10 = C.mci_10(L10, T); m21d = c21 * C.Q_ci(T) / 5 * math.exp(62.5 / T) * L21; m21f = C.mci_21(L21, T)
    run.check("C4b (1-0) and (2-1) mass formulas agree < 1e-6 at the LTE ratio (derived coefficient)", abs(m21d / m10 - 1) < 1e-6, f"rel. {m21d / m10 - 1:+.1e}")
    run.P(f"  C4b with the frozen 4.566e-4 coefficient: rel. {m21f / m10 - 1:+.1e} (exceeds 1e-6 by the coefficient's rounding)")
    run.flag("A-G10", "C4's '< 1e-6' agreement holds for the coefficient derived from the A values, not for the rounded frozen 4.566e-4 (3.7e-5 off); AG5 freezes 4.556e-4 (Boogaard+20), 0.22% lower")
    pk, at = C.freeman_peak(NS)
    run.check("C5 CFG571 C3: Freeman V^2 peak 0.387 +- 0.003 GM/R_d near 2.15 R_d", abs(pk - 0.387) < 0.003 and abs(at - 2.15) < 0.05, f"{pk:.4f} at {at:.3f} R_d")
    run.check("C5 CFG571 C4: Newtonian round trip < 1e-6", C.newtonian_round_trip(NS) < 1e-6, f"{C.newtonian_round_trip(NS):.1e}")
    run.P("\n=== MOCK-JSON classes through the scoring path (MOCK inputs, no cube) ===")
    q = C.Quiet()
    base = lambda lg, det, sf=0.05: dict(CI21=dict(logMgas={"1.9e-5": lg, "3.0e-5": lg - 0.2}, sig_flux_dex=sf, detected=det), G3=False)
    s1 = score(base(9.82, True), q)
    run.check("MOCK-JSON F-DESI-matched gas -> FRAMEWORK SIDE", s1["primary_side"] == "FRAMEWORK SIDE", s1["primary_side"])
    s2 = score(base(11.6, True), q)
    fd = next(r for r in s2["rows"] if r["vc"].startswith("V_c 206") and r["route"] == PRIMARY_ROUTE and r["Mstar"] == 10.89 and r["shape"] == "Rg=Rd" and r["foot"].startswith("canon") and r["model"] == "F-DESI")
    run.check("MOCK-JSON excess gas 11.6 -> F-DESI in tension", tense(fd["wording"]), fd["wording"])
    s3 = score(base(9.0, False, 0.0), q)
    run.check("MOCK-JSON non-detection -> one-sided readings, no FLOOR tension, ROBUST flag undefined", not any("FLOOR" in r["wording"] for r in s3["rows"] if r["route"] == PRIMARY_ROUTE)
              and all(v.startswith("NO CI21") for v in s3["robust"].values()))
    rob = {}
    for lg in np.arange(8.0, 11.81, 0.2):
        s = score(base(float(lg), True), q)
        for k, v in s["robust"].items():
            if k.startswith("V_c 206") and "|10.89|Rg=Rd|canon" in k: rob.setdefault(v, []).append((round(float(lg), 1), k.split("|")[-1]))
    run.check("MOCK-JSON ROBUST and NOT ROBUST are both returnable (CI21 scan with CFG572's CO43 and dust routes fixed)", "ROBUST" in rob and "NOT ROBUST" in rob,
              "; ".join(f"{k}: {len(v)} cases" for k, v in rob.items()))
    nr = sorted({x for x in rob.get("NOT ROBUST", [])})
    run.P("  NOT ROBUST cases (log M_gas CI21, model), canonical M* 10.89 R_g=R_d: " + ", ".join(f"{a}:{b}" for a, b in nr[:40]))
    return dict(reproduction=dict(max_d=w, n=n), transcription=dict(rows=rows, worst=worst), robust_scan={k: len(v) for k, v in rob.items()})


def power(run):
    run.P("\n=== R6 POWER (information; CFG809 rules; CI21 flux error 0.05 dex; R_g = R_d; canonical and alternate footings) ===")
    q = C.Quiet(); out = {}
    for lm in C.GS4["lmstars"]:
        for f in C.FOOTS:
            run.P(f"  M* {lm} | {f}:")
            for lg in np.arange(8.0, 11.61, 0.4):
                cells = []
                for det in (True, False):
                    s = score(dict(CI21=dict(logMgas={"1.9e-5": float(lg), "3.0e-5": float(lg) - 0.2}, sig_flux_dex=0.05 if det else 0.0, detected=det), G3=False), q)
                    rows = [r for r in s["rows"] if r["vc"].startswith("V_c 206") and r["route"] == PRIMARY_ROUTE and r["Mstar"] == lm and r["shape"] == "Rg=Rd" and r["foot"] == f]
                    sd = s["sides"][f"V_c 206 (RC100, sealed)|{PRIMARY_ROUTE}|{lm}|Rg=Rd|{f}"]
                    ab = lambda w: "T" if tense(w) else "C"
                    cells.append(f"{'det' if det else 'UL '}: " + " ".join(f"{r['model'][:6]} {r['Delta']:+.2f}/{r['sigma']:.2f} {ab(r['wording'])}" for r in rows) + f" -> {sd}")
                    out[f"{lm}|{f}|{lg:.1f}|{det}"] = sd
                run.P(f"    log M_gas {lg:5.2f}: " + " || ".join(cells))
    rv = [k for k, v in out.items() if v == "RIVAL SIDE"]
    run.P(f"  RIVAL SIDE reachable anywhere in this scan: {'yes: ' + ', '.join(rv) if rv else 'NO'}")
    return out


def forecast(run):
    run.P("\n=== R7 SENSITIVITY FORECAST (information; CFG570 archive metadata: 0.5183 mJy/beam at 10 km/s, beam 0.089\"; not re-verified) ===")
    run.P("  [CI](2-1) flux for a gas mass (CI21 primary: T_ex 25 K, X_CI 1.9e-5); noise in a circular aperture over the +-300 km/s window")
    out = {}
    for lab, lg in (("F-DESI req (M* 10.89, canon, R_g=R_d)", SEAL["10.89"]["canon 9.36e-11|F-DESI"]["logMgas_Rg=Rd"]),
                    ("F-DESI req (M* 10.76, canon, R_g=R_d)", SEAL["10.76"]["canon 9.36e-11|F-DESI"]["logMgas_Rg=Rd"]),
                    ("dust route (CFG572)", J572["DUST"]["logM"]["alphaCO 4.36 (primary)"]), ("CO43 route (CFG572)", J572["CO43"]["logM"]["r41 0.37"])):
        S = C.SdV_from_Lprime(10 ** lg / (1.36 * C.mci_21(1.0, 25.0) / (6 * 1.9e-5)), NU_OBS, Z_LINE); cells = []
        for rap, fr, nm in ((RE / KPA, 0.5, "r R_e (0.88\"; exponential at R_g = R_d holds 50%)"), (0.3, None, "r 0.3\" (compact gas holding all flux)"), (0.0, 1.0, "one beam")):
            nz, nb = C.aperture_noise_SdV(0.5183, 0.089, rap, 600.0); f = 1.0 if fr is None else fr
            cells.append(f"{nm}: S/N {S * f / nz:.2f}")
        out[lab] = dict(logMgas=lg, SdV=S, cells=cells)
        run.P(f"  {lab}: log M_gas {lg:.2f} -> S dv {S:.4f} Jy km/s; " + "; ".join(cells))
    run.P("  The CFG572 [CI](1-0) limit (< 10.28 at 3 sigma) already sits below the CO43 route; G1 needs S/N >= 5. The plan has no taper branch (A-G14).")
    return out


# ------------------------------------------------------------------------------------------------ main
def main():
    mutate_ = "--mutate" in ARGS
    if "--make-mock" in ARGS:
        kind = opt("--make-mock"); sc = opt("--scratch"); os.makedirs(sc, exist_ok=True)
        cs, ct, _ = mock_spec(kind)
        a = C.write_mock_cube(os.path.join(sc, f"cfg942_gs4_MOCK_{kind}.fits"), cs); b = C.write_mock_image(os.path.join(sc, f"cfg942_gs4_MOCK_{kind}_cont.fits"), ct)
        print(f"MOCK cube cfg942_gs4_MOCK_{kind}.fits sha256 {a}; continuum sha256 {b}"); sys.exit(0)
    if "--selftest" in ARGS: slug = "cfg942_gs4_selftest"
    elif "--mock" in ARGS: slug = f"cfg942_gs4_MOCK_{opt('--mock')}" + ("_MUTATE" if mutate_ else "")
    elif "--cube" in ARGS: slug = "cfg942_gs4_RELEASE" + ("_MUTATE" if mutate_ else "")
    elif "--measured" in ARGS: slug = "cfg942_gs4_measured_" + os.path.splitext(os.path.basename(opt("--measured")))[0]
    else:
        print(__doc__); sys.exit(0)
    run = C.Run(slug, sample_memory=True)
    run.P(f"CFG942 GS4_24110 harness ({slug}); plan {PLAN} (966d50a87); seal CFG571 259f7825c")
    run.P("Frozen predictions = CFG571's four models as sealed. The CFG689 native a0(z) band folded into THEORY_CANONICAL_2026-10-18 does NOT change them and is not scored here.")
    run.P("kappa = 1/2 FITTED; footings never pooled; routes never averaged; single disc = demonstration, no exclusion; not theory closed.")
    run.P(f"target: GS4_24110 RA {RA} Dec {DEC}; [CI](2-1) observed at {NU_OBS:.4f} GHz (z {Z_LINE}); R_e {RE} kpc = {RE / KPA:.3f}\"")
    snap0 = C.snapshot(); res = dict(K1=C.verify_frozen(run))
    if run.failed():
        run.P("a frozen file or seal does not match: STOP (nothing scored)"); run.save(res); sys.exit(2)
    run.flag("A-X6", "CFG809 says it 'imports cfg571_prereg.py read-only'; a plain import runs the whole script (rewrites its results JSON, sys.exit). The harness executes only the text above '# ---- controls ----'")
    code = 0
    if "--selftest" in ARGS:
        res["selftest"] = selftest(run); res["power"] = power(run); res["forecast"] = forecast(run)
    elif "--mock" in ARGS or "--cube" in ARGS:
        if "--mock" in ARGS:
            kind = opt("--mock"); sc = opt("--scratch"); cs, ct, truth = mock_spec(kind)
            path, cpath = os.path.join(sc, f"cfg942_gs4_MOCK_{kind}.fits"), os.path.join(sc, f"cfg942_gs4_MOCK_{kind}_cont.fits")
            from astropy.io import fits
            assert fits.getheader(path).get("MOCKLAB") == cs["label"], "not this harness's MOCK cube"
            run.P(f"\nMOCK cube {os.path.basename(path)} sha256 {C.sha256_file(path)[:16]}…; continuum {os.path.basename(cpath)} sha256 {C.sha256_file(cpath)[:16]}… (scratch; not committed). "
                  f"Truth: log M_gas {truth['lg']}, S dv {truth['S']:.5f}, R_g {truth['Rg']:.2f} kpc, i 45, continuum 478 uJy R_e 2.5 kpc; noise {cs['sigma']:.3e} Jy/beam/channel (MOCK)")
            res["mock"] = dict(kind=kind, file=os.path.basename(path), sha256=C.sha256_file(path), cont_sha256=C.sha256_file(cpath), truth=cs["true"])
        else:
            path, cpath, truth = opt("--cube"), opt("--cont"), None
        if mutate_:
            code = mutate(path, run); res["mutate_exit"] = code
        else:
            meas = measure(path, cpath, run, truth=truth)
            res["measured"] = meas
            sc_ = score(meas, run); res["score"] = {k: v for k, v in sc_.items() if k != "rows"}; res["score_rows"] = sc_["rows"]
            if "--mock" in ARGS: res["required_ok"] = required(opt("--mock"), meas, sc_, run)
            elif run.failed(): run.P("A control FAILED: the run is NOT DIAGNOSTIC (CFG809 section 5)."); code = 1
    elif "--measured" in ARGS:
        sc_ = score(json.load(open(opt("--measured"))), run); res["score"] = {k: v for k, v in sc_.items() if k != "rows"}
    run.check("K5 no frozen file changed during the run (sha256 and mtime)", snap0 == C.snapshot())
    run.P("\nflags raised in this run (harness defaults; see README ambiguity list): " + ", ".join(c for c, _ in run.flags))
    run.save(res)
    if code == 0 and run.failed() and not mutate_: code = 1
    sys.exit(code)


if __name__ == "__main__":
    main()
