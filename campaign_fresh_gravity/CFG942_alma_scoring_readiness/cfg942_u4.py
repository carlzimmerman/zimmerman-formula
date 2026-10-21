#!/usr/bin/env python3
"""CFG942 harness for U4_27928 (ALMA 2024.1.00100.L, CO(2-1), public 2026-11-06).
Reads the frozen plan campaign_fresh_gravity/CFG806_u4_27928_scoring/FROZEN_CRITERIA.md (1bf70683b) and the CFG571 seal
(259f7825c, be27457d...); edits neither.  Criteria of this lane: FROZEN_CRITERIA.md (556c36582).
  python3 -B cfg942_u4.py --selftest                          K1-K5, reproduction, transcription, C4, MOCK-JSON classes, power, forecast
  python3 -B cfg942_u4.py --make-mock a|b|c|d --scratch DIR   write the MOCK cube (seeded; OBJECT='MOCK')
  python3 -B cfg942_u4.py --mock a|b|c|d --scratch DIR [--mutate] [--no-c1]   score that MOCK cube from FITS, exactly as real data
  python3 -B cfg942_u4.py --cube CUBE.fits [--mutate]          release day (after the owner's yes and the download); a real cube's
                                                               outputs are also copied to the plan's dir as cfg806_u4[_MUTATE].out/_results.json
  python3 -B cfg942_u4.py --measured MEAS.json                 score measured quantities only
Implements the owner's CLARIFICATION_2026-10-21.md in the CFG806 dir (commit 35ea5e1be): the beam-corrected V_c interval is primary
(A-U16), the gap reads "not in tension (within 2σ_tot)" (A-U1), the 20% flux flag uses the 2" diameter aperture (A-U14); CFG571's
Delta_m on M_bar is printed as information (A-X3); a C2 failure carries the false-failure note (A-U17). MUTATE's continuum excludes
channels within +-600 km/s of the true line (CFG809 addendum A s2's reading, applied here by instruction after a check on MOCK U4-a).
kappa = 1/2 FITTED; footings never pooled; one disc = a demonstration, no exclusion; not theory closed."""
import os, sys, json, math, csv
sys.dont_write_bytecode = True
# memory guard (10-21): macOS keeps freed 32 KB-8 MB blocks resident in malloc's medium zone; the thin-disc fits pushed U4-a to 997 MiB
# resident against a 123 MB unique set. The zone is switched off at process start by re-executing once with MallocMediumZone=0
# (same process id; numerics unchanged).
if __name__ == "__main__" and sys.platform == "darwin" and os.environ.get("MallocMediumZone") != "0":
    os.environ["MallocMediumZone"] = "0"; os.execv(sys.executable, [sys.executable, "-B"] + sys.argv)
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg942_common as C

PLAN = "campaign_fresh_gravity/CFG806_u4_27928_scoring/FROZEN_CRITERIA.md"
CAT = {r["ID"]: r for r in csv.DictReader(open(os.path.join(C.REPO, "data_assembly/kmos3d_phibss/kmos3d_catalog.csv")))}["U4_27928"]
RA, DEC, Z_CAT, Q_KMOS = float(CAT["RA"]), float(CAT["DEC"]), float(CAT["Z"]), float(CAT["Q"])
NU_REST = 230.538; NU_OBS = NU_REST / (1 + Z_CAT)
Z_G1, DZ_G1 = 1.4193, 0.002
VWIN, VCONT = 500.0, 600.0          # harness default H-U3 (the plan states no moment-0 window); continuum = |v| > 600 km/s
BOX = 8.0                           # half-size (arcsec) of the moment-0 box: mask, flux, 100 random apertures (harness default)
R_VC = 8.3                          # CFG806 3.1: V_c is the model value at R = 8.3 kpc
GEO = C.u4_geometry()               # CFG571: R = 2 Re (8.27 kpc), Rd = Re/1.678, log M* 10.74, z 1.41933
KPA = C.kpc_per_arcsec(Z_CAT)
SIG_FLOOR = 0.15
ARGS = sys.argv[1:]
def opt(k, d=None):
    return ARGS[ARGS.index(k) + 1] if k in ARGS else d


# ------------------------------------------------------------------------------------------------ required gas (CFG571 functions)
NS = C.load_cfg571()
_cache = {}
def req(V, lm=GEO["lmstar"]):
    k = (round(float(V), 9), lm)
    if k not in _cache:
        _cache[k] = C.predict(NS, GEO["R"], float(V), GEO["z"], lm, GEO["Rd"])
    return _cache[k]


def gas_req(V, key, shape, lm=GEO["lmstar"]):
    d = req(V, lm)[key]; return None if d["floor"] else d["logMgas_" + shape]


def dm_bar(g, sg, V, eV, key, shape):
    """CFG571's own single-disc statistic, printed as information only (CLARIFICATION A-X3; the verdict is CFG806's Delta_m on M_gas):
    Delta_m = log M_bar,meas - log M_bar,req, with M_bar the spherical-equivalent V_bar^2 R/G that CFG571's predict() returns
    (logVbar2R_G) at its sealed radius 2 R_e; M_bar,meas from M* 10.74 and the measured M_gas in the declared shapes (Freeman discs).
    Interval: the gas error (sg) and the primary V_c interval (eV) propagated through the same functions."""
    R, Rd = GEO["R"], GEO["Rd"]; Rg = Rd * (1.0 if shape == "Rg=Rd" else 1.5)
    vs2 = float(NS["v2_exp"](10 ** GEO["lmstar"], Rd, R))
    f = lambda gg, VV: math.log10((vs2 + float(NS["v2_exp"](10 ** gg, Rg, R))) * R / NS["G"]) - req(VV)[key]["logVbar2R_G"]
    D = f(g, V)
    return D, math.hypot(0.5 * (f(g + sg, V) - f(g - sg, V)), 0.5 * (f(g, V + eV) - f(g, V - eV)) if eV else 0.0)


# ------------------------------------------------------------------------------------------------ scoring (CFG806 section 4)
NIT = "not in tension (within 2σ_tot)"      # CLARIFICATION A-U1: the case between "inside the range" and "> 2 sig_tot outside"; never "consistent"


def three_way(g, lo, hi, st):
    if lo <= g <= hi: return "CONSISTENT"
    if g < lo - 2 * st: return "IN TENSION (low gas)"
    if g > hi + 2 * st: return "IN TENSION (high gas)"
    return NIT


def in_tension(c): return c.startswith("IN TENSION")


def read_model(g, sg_rms, V, eV, key, shape, detected, eV_info=None):
    """CFG806 s4 reading as clarified on 2026-10-21. eV is the PRIMARY 1-sigma V_c error: the beam-corrected one (A-U16).
    Information readings, never the verdict: alt1 single 0.15 floor (A-U2), alt2 |Delta| <= 2 sig, alt3 M* +-0.2 in the range (A-U15),
    and the independent-pixel V_c error eV_info (the pre-A-U16 interval). Returns dict."""
    d0 = req(V)[key]
    out = dict(model=key.split("|")[1], foot=key.split("|")[0], shape=shape, V=V, eV=eV)
    sg = math.hypot(sg_rms, SIG_FLOOR)                 # section 3.3: flux error = random-aperture rms (+) 0.15 dex floor
    st = math.hypot(sg, SIG_FLOOR)                     # section 4: sigma_tot = interval from section 3 (+) 0.15 dex (literal)
    if d0["floor"]:
        red = req(V, GEO["lmstar"] - 0.2)[key]
        out.update(cls="IN TENSION (FLOOR)" if detected else "FLOOR (no gas detected)", floor=True, Delta=None,
                   reduced=("not FLOOR at M*-0.2 (needs log M_gas %.2f): tension REDUCED" % red["logMgas_" + shape]) if not red["floor"] else "FLOOR persists at M*-0.2")
        return out
    ends = [gas_req(V - eV, key, shape), gas_req(V + eV, key, shape)]
    r0 = d0["logMgas_" + shape]
    lo = min([e for e in ends if e is not None] + [r0]) if None not in ends else -np.inf
    hi = max([e for e in ends if e is not None] + [r0])
    sV = abs(ends[1] - ends[0]) / 2 if None not in ends else abs(hi - r0)
    out.update(floor=False, req=r0, range=(lo, hi), Delta=g - r0, eDelta=math.hypot(sg, sV), sigma_tot=st, cls=three_way(g, lo, hi, st))
    alts = {}
    alts["alt1 single 0.15 floor"] = three_way(g, lo, hi, math.hypot(sg_rms, SIG_FLOOR))
    st2 = math.sqrt(sg ** 2 + sV ** 2 + SIG_FLOOR ** 2)
    alts["alt2 |Delta| <= 2sig (sig incl. V_c)"] = "CONSISTENT" if abs(g - r0) <= 2 * st2 else ("IN TENSION (low gas)" if g < r0 else "IN TENSION (high gas)")
    e3 = [gas_req(V + s * eV, key, shape, GEO["lmstar"] + dm) for s in (-1, 0, 1) for dm in (-0.2, 0.2)]
    lo3 = -np.inf if None in e3 else min(e3 + [lo]); hi3 = max([e for e in e3 if e is not None] + [hi])
    alts["alt3 range incl. M* +-0.2"] = three_way(g, lo3, hi3, st)
    if eV_info is not None:
        ea = [gas_req(V - eV_info, key, shape), gas_req(V + eV_info, key, shape)]
        loa = -np.inf if None in ea else min(ea + [r0]); hia = max([e for e in ea if e is not None] + [r0])
        alts["info: independent-pixel V_c error (pre-A-U16)"] = three_way(g, loa, hia, st)
    out["alts"] = {k: v for k, v in alts.items() if (in_tension(v) != in_tension(out["cls"])) or (v == "CONSISTENT") != (out["cls"] == "CONSISTENT")}
    return out


def side(rows):
    cl = {r["model"]: r["cls"] for r in rows}
    fw_ok = any(not in_tension(cl[m]) for m in C.FRAMEWORK); rv_t = in_tension(cl[C.RIVAL])
    if fw_ok and rv_t: return "FRAMEWORK SIDE"
    if (not rv_t) and all(in_tension(cl[m]) for m in C.FRAMEWORK): return "RIVAL SIDE"
    return "NO SIDE"


def score(meas, run):
    """meas: detected, logMgas{aco}, sig_rms_dex, logMgas_UL{aco}, branches{incl|press: (V, eV_independent_pixel, eV_beamcorr)}, G2 {reached, Rmax_kpc}.
    CLARIFICATION A-U16: the beam-corrected error (third element) is the PRIMARY 1-sigma interval for TESTS NOTHING, PARTIAL, every
    Delta_m and every verdict; the independent-pixel error (second element) is printed as information only."""
    res = dict(kind="U4 score", branches={})
    run.P("\n=== SCORE (CFG806 section 4; single disc = demonstration; no model is excluded) ===")
    if not meas["detected"]:
        run.P("  G1 FAILED: CO(2-1) not detected. 3-sigma upper limits: " + ", ".join(f"alpha_CO {a}: log M_gas < {v:.2f}" for a, v in meas["logMgas_UL"].items()))
        run.P("  NO KINEMATIC TEST: the predictions are conditional on V_c, which G1 failure leaves unmeasured -> nothing scored.")
        run.flag("A-U6", "CFG806 3.4 promises a one-sided Delta_m for a non-detection, but G1 failure stops the kinematic test, so no V_c exists to evaluate it; the harness scores nothing.")
        res["overall"] = "G1 FAIL: UPPER LIMIT, NO KINEMATIC TEST"; return res
    if not meas["G2"]["reached"]:
        run.P(f"  G2 FAILED: detected emission reaches only {meas['G2']['Rmax_kpc']:.2f} kpc (< 6 kpc): RADIUS NOT REACHED, kinematic test stopped.")
        run.P("  gas: " + ", ".join(f"alpha_CO {a}: log M_gas {v:.2f}" for a, v in meas["logMgas"].items()))
        res["overall"] = "G2 FAIL: RADIUS NOT REACHED"; return res
    overall = []
    for bname, (V, eVi, eVb) in meas["branches"].items():
        eV = eVb                                       # CLARIFICATION A-U16: the beam-corrected interval is primary
        b = dict(V=V, eV=eV, eV_source="fit covariance x sqrt(pixels per beam) (beam-corrected; CLARIFICATION A-U16)", eV_indep_info=eVi)
        st_info = "TESTS NOTHING" if V + eVi < 200 else ("PARTIAL" if V - eVi < 200 else "SCORED")
        b["status_indep_info"] = st_info
        vline = f"V_c {V:.1f} +- {eV:.2f} km/s (1 sigma, beam-corrected: primary, CLARIFICATION A-U16; independent-pixel covariance +- {eVi:.2f}: information)"
        if V + eV < 200:
            b["status"] = "TESTS NOTHING"
            run.P(f"  [{bname}] {vline}: 1-sigma interval entirely below 200 -> TESTS NOTHING (every model FLOOR). gas: "
                  + ", ".join(f"alpha_CO {a}: {v:.2f}" for a, v in meas["logMgas"].items()))
            if st_info != b["status"]: run.P(f"    information: the independent-pixel interval would read {st_info}")
            res["branches"][bname] = b; overall.append("TESTS NOTHING"); continue
        partial = V - eV < 200
        evals = [(V - eV, 0.0, "lower end"), (V + eV, 0.0, "upper end")] if partial else [(V, eV, "")]
        b["status"] = "PARTIAL" if partial else "SCORED"; b["rows"] = []
        for (Vx, eVx, tag) in evals:
            for aco, g in meas["logMgas"].items():
                for shape in ("Rg=Rd", "Rg=1.5Rd"):
                    for f in C.FOOTS:
                        rows = [read_model(g, meas["sig_rms_dex"], Vx, eVx, f"{f}|{m}", shape, True, None if partial else eVi) for m in C.MODELS]
                        sd = side(rows)
                        for r in rows:
                            r.update(aco=aco, end=tag,
                                     Delta_Mbar_info=dm_bar(g, math.hypot(meas["sig_rms_dex"], SIG_FLOOR), Vx, eVx, f"{f}|{r['model']}", shape))
                        b["rows"] += rows; b.setdefault("sides", {})[f"{tag}|{aco}|{shape}|{f}"] = sd
        res["branches"][bname] = b
        overall.append(b["status"])
        # print the primary cut and the side table
        run.P(f"\n  [{bname}] {vline}{'  -> PARTIAL (interval straddles 200): Delta_m at both ends' if partial else ''}")
        if st_info != b["status"]: run.P(f"    information: the independent-pixel interval would read {st_info}")
        for (Vx, eVx, tag) in evals:
            for f in C.FOOTS:
                sel = [r for r in b["rows"] if r["foot"] == f and r["aco"] == "4.36" and r["shape"] == "Rg=Rd" and r["end"] == tag]
                run.P(f"    {tag + ' ' if tag else ''}{f} | alpha_CO 4.36 | Rg=Rd:")
                for r in sel:
                    if r["floor"]:
                        run.P(f"      {r['model']:13s} FLOOR at V_c {r['V']:.1f} -> {r['cls']}; {r['reduced']}")
                    else:
                        rng = f"[{r['range'][0]:.2f}, {r['range'][1]:.2f}]" if np.isfinite(r["range"][0]) else f"[no gas, {r['range'][1]:.2f}]"
                        run.P(f"      {r['model']:13s} req {r['req']:.2f} range {rng}; meas {meas['logMgas']['4.36']:.2f}; Delta {r['Delta']:+.2f} +- {r['eDelta']:.2f}; sig_tot {r['sigma_tot']:.2f} -> {r['cls']}"
                              + (f"   (alternative readings differ: {r['alts']})" if r.get("alts") else ""))
                run.P(f"      side: {b['sides'][f'{tag}|4.36|Rg=Rd|{f}']}")
                run.P("      information (CFG571's own Delta_m on M_bar, CLARIFICATION A-X3; never the verdict): "
                      + "; ".join(f"{r['model']} {r['Delta_Mbar_info'][0]:+.2f} +- {r['Delta_Mbar_info'][1]:.2f}" for r in sel))
        allsides = {}
        for k, v in b["sides"].items(): allsides.setdefault(v, []).append(k)
        run.P("    all branches (end|alpha_CO|shape|footing): " + "; ".join(f"{v}: {len(k)}" for v, k in allsides.items()))
    res["overall"] = overall
    return res


# ------------------------------------------------------------------------------------------------ measurement (CFG806 section 3)
def core(m0d, cube, run, tag="", fit=True, inc_branches=True):
    """m0d: streamed moment-0 over a wide box (mask, flux, noise apertures, centroid, G2); cube: small continuum-subtracted sub-cube
    (masked spectrum, kinematic fits)."""
    m = dict(file=m0d["file"], sha256=m0d["sha256"], object=m0d["object"], target_img_xy=(m0d["x0"] + m0d["xc"], m0d["y0"] + m0d["yc"]))
    m0, pix, beam, dv = m0d["m0"], m0d["pix"], m0d["beam"], m0d["dv"]; bp = C.beam_pix(beam, pix); xc, yc = m0d["xc"], m0d["yc"]
    r = C.radius_map(m0.shape, xc, yc) * pix
    s0 = C.robust_std(m0[r > 2.0]); mask = C.make_mask(m0, s0, xc, yc, pix)
    m.update(win_channels=m0d["nwin"], cont_channels=m0d["ncont"], sig_mom0=s0, mask_pix=int(mask.sum()))
    if m0d["ncont"] < 3: run.flag("A-U3b", "fewer than 3 line-free channels (|v| > 600 km/s): continuum not subtracted")
    rng = np.random.default_rng(942)
    aper = mask if mask.sum() else (r <= 2 * GEO["Re"] / KPA)
    rmax_ap = float(np.max(r[aper]))
    offs = C.random_offsets(rng, aper, m0.shape, xc, yc, (rmax_ap + 0.3) / pix, 100)
    ap = C.translated_apertures(m0, aper, bp, offs)
    rms = float(np.std(ap, ddof=1)) if len(ap) > 2 else float("nan")
    S = float(np.nansum(m0[aper]) / bp)
    m.update(n_random_apertures=len(ap), n_indep=C.independent_count(aper, offs), ap_mean=float(np.mean(ap)) if ap else float("nan"), ap_rms=rms, S=S,
             SN=S / rms if rms > 0 else float("nan"))
    quoted = C.mask_sum_noise(aper, beam, pix, m0d["sig_ch"], dv, m0d["nwin"], m0d["ncont"])
    m.update(sig_ch=m0d["sig_ch"], quoted_noise=quoted)
    if len(ap) < 100: run.flag("A-U4", f"only {len(ap)} off-source translated-mask apertures fit in the {BOX}\" box (CFG806 C2 asks for 100)")
    if mask.sum():
        w = np.where(mask, np.clip(np.nan_to_num(m0), 0, None), 0.0); ys, xs = np.indices(m0.shape)
        cx, cy = (w * xs).sum() / w.sum(), (w * ys).sum() / w.sum(); off = math.hypot(cx - xc, cy - yc) * pix
        ms, lost = C.sub_mask(mask, m0d, cube)
        win = np.abs(cube["v"]) <= VWIN
        spec = np.nansum(cube["data"][win][:, ms], axis=1); vv = cube["v"][win]; sp = np.clip(spec, 0, None)
        vcen = float((sp * vv).sum() / sp.sum()) if sp.sum() > 0 else float("nan"); zl = Z_CAT + (1 + Z_CAT) * vcen / C.CKMS
        if lost: run.flag("A-U8", f"{lost} mask pixels fall outside the {CUBE_HALF}\" sub-cube used for the spectrum and the fits")
    else:
        off, zl, vcen = float("nan"), float("nan"), float("nan")
    nul = C.seeded_null(m0, s0, mask, xc, yc, pix, bp, rmax_ap + 0.8, 200, rng)
    mu_n, sd_n = (float(np.mean(nul)), float(np.std(nul, ddof=1))) if len(nul) > 2 else (float("nan"), float("nan"))
    SNsel = (S - mu_n) / sd_n if sd_n > 0 else float("nan")
    G1 = bool(np.isfinite(SNsel) and SNsel >= 5 and off <= 0.5 and abs(zl - Z_G1) <= DZ_G1)
    G1_literal = bool(np.isfinite(m["SN"]) and m["SN"] >= 5 and off <= 0.5 and abs(zl - Z_G1) <= DZ_G1)
    m.update(centroid_offset_arcsec=off, z_line=zl, v_centroid=vcen, G1=G1, G1_literal=G1_literal, SN_selection=SNsel, null_mean=mu_n, null_sd=sd_n,
             n_null=len(nul), mask_rmax_arcsec=rmax_ap)
    run.P(f"  {tag}G1: S dv {S:.5f} Jy km/s in the >= 2 sigma moment-0 mask ({int(mask.sum())} px); translated-mask rms {rms:.5f} ({len(ap)} apertures) -> S/N {m['SN']:.1f}; "
          f"selection-aware null (same mask grown at {len(nul)} off-source seeds): mean {mu_n:.5f}, sd {sd_n:.5f} -> S/N {SNsel:.1f}; centroid offset {off:.3f}\"; "
          f"z_line {zl:.5f} -> {'PASS' if G1 else 'FAIL'} (literal translated-mask S/N reading: {'PASS' if G1_literal else 'FAIL'})")
    if G1 != G1_literal:
        run.flag("A-U13", "G1 differs between the selection-aware S/N (harness default) and the translated-mask S/N: the >= 2 sigma mask selects positive noise, so the literal reading can pass on pure noise (MOCK U4-d)")
    for rad in (1.0, 2.0):
        m[f"ap_r{rad:.0f}"] = float(np.nansum(m0[r <= rad]) / bp)
    if S > 0 and mask.sum():                     # CFG806 3.3 20% flux-agreement flag; CLARIFICATION A-U14: the "2\" aperture" is diameter 2" (radius 1")
        f1, f2 = S / m["ap_r1"], S / m["ap_r2"]; ok1 = abs(f1 - 1) <= 0.2
        m["flux_agreement"] = dict(aperture="circle of diameter 2 arcsec (radius 1 arcsec), CLARIFICATION A-U14", mask_over_aperture=f1, within_20pct=ok1,
                                   flag=bool(G1 and not ok1), info_radius2_mask_over_aperture=f2)
        run.P(f"  {tag}3.3 flux-agreement check (CLARIFICATION A-U14: circular aperture of diameter 2\" = radius 1\"): mask/aperture = {f1:.3f} -> "
              + ("within 20%, no flag" if ok1 else ("NOT within 20%: FLAG (CFG806 3.3)" if G1 else "not within 20% (G1 failed: no gas mass, so no flag)"))
              + f"; information: radius-2\" aperture, mask/aperture = {f2:.3f}")
        if G1 and not ok1:
            run.flag("CFG806-3.3", "the mask flux and the 2\"-diameter aperture flux differ by more than 20% (CFG806 3.3: reported as a flag)")
    sr = 0.4343 * rms / S if (S > 0 and rms > 0) else float("nan")
    m["sig_rms_dex"] = sr
    m["logMgas"] = {a: math.log10(C.mgas_co21(S, Z_CAT, NU_OBS, aco=float(a))) if S > 0 else float("nan") for a in ("4.36", "1.0")}
    m["detected"] = G1
    if not G1:                                   # upper limit in a fixed circular aperture of radius 2 R_e (A-U5), noise from translated copies
        circ = r <= 2 * GEO["Re"] / KPA
        oc = C.random_offsets(rng, circ, m0.shape, xc, yc, (2 * GEO["Re"] / KPA + 0.3) / pix, 100)
        apc = C.translated_apertures(m0, circ, bp, oc); rmsc = float(np.std(apc, ddof=1)) if len(apc) > 2 else float("nan")
        m.update(UL_aperture_arcsec=2 * GEO["Re"] / KPA, UL_rms=rmsc, UL_flux=3 * rmsc, UL_n_apertures=len(apc))
        m["logMgas_UL"] = {a: math.log10(C.mgas_co21(3 * rmsc, Z_CAT, NU_OBS, aco=float(a))) for a in ("4.36", "1.0")} if rmsc > 0 else {}
        run.P(f"  {tag}G1 failed: 3-sigma upper limit in a circular aperture of radius {2 * GEO['Re'] / KPA:.2f}\" (2 R_e): S dv < {3 * rmsc:.5f} Jy km/s ({len(apc)} translated apertures)")
        run.flag("A-U5", "the plan does not say which aperture gives the non-detection upper limit; the harness uses a circle of radius 2 R_e = 0.98 arcsec (CFG571's radius)")
    if G1:
        run.P(f"  {tag}gas: log M_gas {m['logMgas']['4.36']:.3f} (alpha_CO 4.36) / {m['logMgas']['1.0']:.3f} (1.0); random-aperture error {sr:.3f} dex (+ 0.15 dex floor)")
    if not G1 or not fit:
        return m, mask
    gf = C.fit_gauss2d(m0, s0, pix, beam, xc, yc, half=2.0)
    ip, cl = C.inc_from_q(gf["q"]); ik, _ = C.inc_from_q(Q_KMOS)
    if cl: run.flag("A-U11", "moment-0 axis ratio below q0 = 0.2 (or above 1): inclination clamped")
    m.update(gauss={k: v for k, v in gf.items()}, inc_primary=ip, inc_kmos=ik)
    run.P(f"  {tag}moment-0 beam-convolved Gaussian: q {gf['q']:.3f} -> i {ip:.1f} deg (primary, q0 0.2); KMOS3D q {Q_KMOS} -> i {ik:.1f} deg (branch)")
    ms, _ = C.sub_mask(mask, m0d, cube)
    m0s = np.nansum(cube["data"][np.abs(cube["v"]) <= VWIN], axis=0) * dv
    pa0, vs0, amp, _ = C.kinematic_pa(cube, m0s, ms, VWIN, cube["xc"], cube["yc"])
    fits_ = {}
    for nm, inc in ((("incl-primary", ip), ("incl-KMOS3D", ik)) if inc_branches else (("incl-primary", ip),)):
        fd = C.fit_disc(cube, inc, KPA, m0d["sig_ch"], (0.0, 0.0), pa0, vs0, amp / max(math.sin(math.radians(inc)), 0.2), max(gf["fwhm_maj"] / 2.5, 0.05), R_VC, GEO["Rd"])
        fits_[nm] = fd
        run.P(f"  {tag}thin-disc fit [{nm}, i {inc:.1f}]: V_f {fd['params'][4]:.1f}, R_t {fd['params'][5]:.2f} kpc, sigma0 {fd['params'][6]:.1f}; "
              f"V_rot(8.3 kpc) {fd['Vrot']:.1f} +- {fd['eVrot_beamcorr']:.2f}; V_c P-B {fd['Vc_PB']:.1f} +- {fd['eVc_PB_beamcorr']:.2f} "
              f"(errors beam-corrected = primary, A-U16; independent-pixel +- {fd['eVrot']:.2f} / +- {fd['eVc_PB']:.2f}, information); "
              f"chi2/N {fd['chi2'] / fd['nvox']:.3f}, nfev {fd['nfev']}")
    m["fits"] = fits_
    fp = fits_["incl-primary"]["params"]
    c_, s_ = math.cos(fp[2]), math.sin(fp[2]); ys, xs = np.nonzero(mask)
    X, Y = (xs - xc) * pix - fp[0], (ys - yc) * pix - fp[1]
    xr, yr = X * c_ + Y * s_, -X * s_ + Y * c_
    Rdep = np.sqrt(xr ** 2 + (yr / max(math.cos(math.radians(ip)), 0.05)) ** 2) * KPA; Rproj = np.hypot(X, Y) * KPA
    m["G2"] = dict(reached=bool(Rdep.max() >= 6.0), Rmax_kpc=float(Rdep.max()), Rmax_proj_kpc=float(Rproj.max()))
    run.P(f"  {tag}G2: farthest mask pixel at {Rdep.max():.2f} kpc deprojected ({Rproj.max():.2f} projected) -> {'PASS' if m['G2']['reached'] else 'FAIL'} (>= 6 kpc)")
    run.flag("A-U12b", "G2 'detected emission reaches 6 kpc': the harness uses the deprojected radius of the farthest >= 2 sigma moment-0 mask pixel (projected also printed)")
    m["branches"] = {}
    for nm, fd in fits_.items():
        m["branches"][f"{nm}|P-B"] = (fd["Vc_PB"], fd["eVc_PB"], fd["eVc_PB_beamcorr"])
        m["branches"][f"{nm}|P0"] = (fd["Vc_P0"], fd["eVc_P0"], fd["eVc_P0_beamcorr"])
    return m, mask


CUBE_HALF = 2.2


def mutate_continuum_check(path, run, m0d_excl):
    """MUTATE only: the flux in the 2 R_e circle at the target in the shifted window, with the true-line channels in the continuum
    (the 10-21 harness) and with them excluded (primary); translated-circle rms of each map. Information."""
    out = {}
    m0d_incl = C.stream_mom0(path, RA, DEC, NU_OBS, BOX, VWIN, VCONT, 2000.0)
    for lab, d in (("true-line channels in the continuum (10-21 harness)", m0d_incl), ("true-line channels excluded (primary)", m0d_excl)):
        bp = C.beam_pix(d["beam"], d["pix"]); r = C.radius_map(d["m0"].shape, d["xc"], d["yc"]) * d["pix"]; circ = r <= 2 * GEO["Re"] / KPA
        S = float(np.nansum(d["m0"][circ]) / bp); rng = np.random.default_rng(942)
        off = C.random_offsets(rng, circ, d["m0"].shape, d["xc"], d["yc"], (2 * GEO["Re"] / KPA + 0.3) / d["pix"], 100)
        ap = C.translated_apertures(d["m0"], circ, bp, off); s = float(np.std(ap, ddof=1))
        out[lab] = dict(ncont=d["ncont"], S=S, rms=s, sigma=S / s)
        run.P(f"  MUTATE continuum check, {lab}: {d['ncont']} continuum channels; 2 R_e circle at the target {S:+.5f} Jy km/s = {S / s:+.1f} sigma")
    return out


def measure(path, run, vshift=0.0, c1=True, true_flux=None):
    run.P(f"\n=== MEASUREMENT (CFG806 section 3) of {os.path.basename(path)}{'  [MUTATE: velocity axis +2000 km/s]' if vshift else ''} ===")
    ex = C.MUTATE_EXCL if vshift else 0.0
    m0d = C.stream_mom0(path, RA, DEC, NU_OBS, BOX, VWIN, VCONT, vshift, excl_true=ex)
    cube = C.load_box(path, RA, DEC, NU_OBS, CUBE_HALF, 650.0, VCONT, vshift, excl_true=ex)
    mcheck = None
    if vshift:
        run.P(f"  MUTATE continuum: the median of the {m0d['ncont']} channels that are line-free relative to BOTH the shifted window (|v| > 600) "
              f"and the true line (more than {C.MUTATE_EXCL:.0f} km/s from z {Z_CAT}). This is CFG809 addendum A s2's reading (748dd8095), applied to U4 "
              f"by instruction because the check below shows the same over-subtraction; CFG806's own text does not state it.")
        mcheck = mutate_continuum_check(path, run, m0d)
    if m0d["beam"] is None: raise SystemExit("C3: no beam (no BMAJ keyword and no BEAMS table): cannot proceed")
    if m0d["beam_source"] != "header": run.flag("A-M2", "per-plane beams (BEAMS table): the harness uses their median")
    run.P(f"  file sha256 {m0d['sha256'][:16]}…; OBJECT '{m0d['object']}'; pixel {m0d['pix']:.4f}\"; beam {m0d['beam'][0]:.3f}x{m0d['beam'][1]:.3f}\" PA {m0d['beam'][2]:.0f} ({m0d['beam_source']}); "
          f"dv {m0d['dv']:.1f} km/s; v coverage {m0d['v_cover'][0]:.0f}..{m0d['v_cover'][1]:.0f} km/s; window |v| <= {VWIN:.0f} ({m0d['nwin']} ch), continuum {m0d['ncont']} ch")
    if m0d["object"] == "MOCK": run.P("  *** MOCK cube (generated by this harness; NOT ALMA DATA) ***")
    run.flag("A-U3", f"CFG806 gives no moment-0 velocity window: harness default |v| <= {VWIN:.0f} km/s about z_cat (AG5 uses 400); continuum = median of all line-free channels |v| > 600")
    cov = m0d["nu_cover"][0] <= NU_OBS <= m0d["nu_cover"][1]
    rf = m0d["restfrq"]; rfok = rf is not None and abs(rf / 1e9 - NU_REST) < 1e-3
    run.check("C3 frequency axis covers CO(2-1) at z_cat and beam keywords exist", cov and m0d["beam"] is not None, f"nu_obs {NU_OBS:.4f} GHz; channel {m0d['dv']:.1f} km/s")
    run.P(f"  C3 RESTFRQ = {('%.6f GHz' % (rf / 1e9)) if rf else 'absent'} ({'= 230.538' if rfok else 'not 230.538: reported, not failed'})")
    if not rfok: run.flag("A-U9", "C3 'rest frequency 230.538 GHz': pipeline cubes may carry another RESTFRQ; the harness checks frequency coverage and reports RESTFRQ")
    if not m0d["win_covered"]: run.P("  NOTE: the window |v| <= 500 km/s is not fully covered by the cube after the shift")
    m, mask = core(m0d, cube, run)
    if mcheck: m["mutate_continuum_check"] = mcheck
    if m["n_random_apertures"] > 2:
        ni = max(m["n_indep"], 1)
        ok_mean = abs(m["ap_mean"]) < 3 * m["ap_rms"] / math.sqrt(ni); ok_rms = abs(m["ap_rms"] / m["quoted_noise"] - 1) <= 0.2
        okc2 = run.check("C2 off-source apertures: mean consistent with zero (3 rms/sqrt(N_independent)) and rms within 20% of the quoted noise", ok_mean and ok_rms,
                         f"mean {m['ap_mean']:+.5f}, rms {m['ap_rms']:.5f}, quoted {m['quoted_noise']:.5f} (ratio {m['ap_rms'] / m['quoted_noise']:.2f}; N {m['n_random_apertures']}, independent {m['n_indep']})")
        if not okc2:                             # CLARIFICATION A-U4 / A-U17: the false-failure rate is stated beside a C2 failure; s5 is not changed
            pf = math.erfc(0.2 * math.sqrt(max(ni - 1, 1)))
            m["C2_false_failure_note"] = dict(mock_rate="about 10%", gaussian_estimate=pf, n_independent=ni)
            run.P(f"    note beside the C2 failure (CLARIFICATION A-U4/A-U17): on pure noise the 20% rms test fails about 10% of the time (MOCK); "
                  f"Gaussian estimate at N_independent {ni}: {pf:.0%}. CFG806 s5 is not changed: the failed control stands and the run is NOT DIAGNOSTIC.")
    run.flag("A-U10", "C2 'quoted noise' is undefined in CFG806; the harness uses the analytic noise of the mask sum (beam-shaped noise autocorrelation, per-channel rms, window channels, continuum-median term)")
    if true_flux:
        run.P(f"  MOCK truth: S dv {true_flux:.4f} Jy km/s; recovered/true = {m['S'] / true_flux:.3f}")
    if vshift == 0 and m["detected"] and c1:
        m["C1"] = injection(path, run, m)
    return m


def injection(path, run, m):
    """C1: discs of known V_c (200, 250 km/s, P-B at 8.3 kpc) and known flux injected into off-source noise from the same cube
    (same channels; position shifted east by max(2.6", 2 x (mask radius + 0.3")), real source blanked), measured by the same code."""
    out = {}
    rblank = m["mask_rmax_arcsec"] + 0.3; shift = max(2.6, 2 * rblank)
    ra_off = RA + shift / 3600.0 / math.cos(math.radians(DEC))
    m0b = C.stream_mom0(path, ra_off, DEC, NU_OBS, BOX, VWIN, VCONT)
    cb = C.load_box(path, ra_off, DEC, NU_OBS, CUBE_HALF, 650.0, VCONT)
    for d, key in ((m0b, "m0"), (cb, "data")):            # blank the real source so the injection sees off-source noise only
        arr = d[key]; shp = arr.shape[-2:]
        rr = C.radius_map(shp, m["target_img_xy"][0] - d["x0"], m["target_img_xy"][1] - d["y0"]) * d["pix"]
        if key == "m0": arr[rr <= rblank] = np.nan
        else: arr[:, rr <= rblank] = 0.0
    inc = m["inc_primary"]; qi = math.sqrt(math.cos(math.radians(inc)) ** 2 * 0.96 + 0.04)
    lg_inj = gas_req(250.0, "canon 9.36e-11|F-DESI", "Rg=Rd")                 # known M_gas: F-DESI's sealed canonical requirement at 250 km/s
    Sinj = C.SdV_from_Lprime(10 ** lg_inj / 4.36 * 0.77, NU_OBS, Z_CAT); s0 = 30.0; rt = 1.0; pa = 0.5; h = GEO["Rd"] / KPA
    run.P(f"  C1: injection {shift:.2f}\" east of the target (known log M_gas {lg_inj:.2f}, S dv {Sinj:.4f} Jy km/s, i = measured primary); the real source is blanked within {rblank:.2f}\" of the target")
    for Vc in (200.0, 250.0):
        vr = math.sqrt(Vc ** 2 - 2 * s0 ** 2 * R_VC / GEO["Rd"]); vf = vr / (2 / math.pi * math.atan(R_VC / rt))
        cube = dict(cb); cube["data"] = cb["data"].copy(); m0d = dict(m0b); m0d["m0"] = m0b["m0"].copy()
        for tgt, isc in ((cube, True), (m0d, False)):
            shp = tgt["data"].shape[1:] if isc else tgt["m0"].shape
            yy, xx = np.indices(shp); X, Y = (xx - tgt["xc"]) * tgt["pix"], (yy - tgt["yc"]) * tgt["pix"]
            c, s = math.cos(pa), math.sin(pa); xr = X * c + Y * s; yr = -X * s + Y * c
            bp = C.beam_pix(tgt["beam"], tgt["pix"]); I0 = Sinj * bp / np.exp(-np.sqrt(xr ** 2 + (yr / qi) ** 2) / h).sum()
            kf = C.kernel_rfft(shp, tgt["beam"], tgt["pix"]); p = [0, 0, pa, 0, vf, rt, s0, I0, h]
            if isc:
                tgt["data"] += C.disc_model(p, X, Y, tgt["v"], tgt["dv"], inc, KPA, kf, q_int=qi).astype(np.float32)
            else:                                          # model moment-0 on a sub-grid about the injection point
                vw = np.arange(-VWIN, VWIN + 1e-6, tgt["dv"]); hs = int(math.ceil((10 * h + 4 * tgt["beam"][0]) / tgt["pix"]))
                ix, iy = int(round(tgt["xc"])), int(round(tgt["yc"])); ya, yb, xa, xb = max(0, iy - hs), min(shp[0], iy + hs + 1), max(0, ix - hs), min(shp[1], ix + hs + 1)
                Xs, Ys = X[ya:yb, xa:xb], Y[ya:yb, xa:xb]; kfs = C.kernel_rfft(Xs.shape, tgt["beam"], tgt["pix"])
                acc = np.zeros(Xs.shape)
                for j in range(0, len(vw), 8):
                    acc += C.disc_model(p, Xs, Ys, vw[j:j + 8], tgt["dv"], inc, KPA, kfs, q_int=qi).sum(axis=0) * tgt["dv"]
                tgt["m0"][ya:yb, xa:xb] += acc
        q = Run_quiet(); mm, _ = core(m0d, cube, q, fit=True, inc_branches=False)
        run.P("    C1 inner: " + " | ".join(l.strip() for l in q.lines if "G1" in l or "thin-disc" in l))
        rec_f = mm["S"] / Sinj if Sinj else float("nan")
        Vrec = mm["fits"]["incl-primary"]["Vc_PB"] if mm.get("fits") else float("nan")
        ok = abs(Vrec / Vc - 1) <= 0.15 and abs(rec_f - 1) <= 0.2
        run.check(f"C1 injection V_c {Vc:.0f} km/s: V_c within 15% and flux within 20%", ok, f"V_c(P-B) recovered {Vrec:.1f}, flux ratio {rec_f:.3f}")
        out[str(Vc)] = dict(Vc_rec=Vrec, flux_ratio=rec_f, ok=ok)
    return out


class Run_quiet(C.Run):
    def __init__(self): super().__init__("quiet")
    def P(self, s=""): self.lines.append(str(s))


# ------------------------------------------------------------------------------------------------ MOCK cubes
def mock_spec(kind):
    Vc = {"a": 250.0, "b": 250.0, "c": 165.0, "d": 250.0}[kind]
    s0, rt, inc = 30.0, 1.0, 55.0
    vr = math.sqrt(Vc ** 2 - 2 * s0 ** 2 * R_VC / GEO["Rd"]); vf = vr / (2 / math.pi * math.atan(R_VC / rt))
    key = {"a": "canon 9.36e-11|F-DESI", "b": "canon 9.36e-11|R-H", "c": "canon 9.36e-11|F-DESI", "d": None}[kind]
    if kind == "c":
        lg = gas_req(250.0, key, "Rg=Rd")                     # any gas: the same gas as U4-a
    elif key:
        lg = gas_req(Vc, key, "Rg=Rd")
    else:
        lg = None
    SdV = 0.0 if lg is None else C.SdV_from_Lprime(10 ** lg / 4.36 * 0.77, NU_OBS, Z_CAT)
    Sa = C.SdV_from_Lprime(10 ** gas_req(250.0, "canon 9.36e-11|F-DESI", "Rg=Rd") / 4.36 * 0.77, NU_OBS, Z_CAT)
    pix = 0.07 / 3; n = 720; beam = (0.075, 0.065, 30.0); h = GEO["Rd"] / KPA
    qi = math.sqrt(math.cos(math.radians(inc)) ** 2 * 0.96 + 0.04)
    bp = C.beam_pix(beam, pix); yy, xx = np.indices((n, n)); X, Y = (xx - n // 2) * pix, (yy - n // 2) * pix
    pa = math.radians(30.0); c, s = math.cos(pa), math.sin(pa); xr = X * c + Y * s; yr = -X * s + Y * c
    I0a = Sa * bp / np.exp(-np.sqrt(xr ** 2 + (yr / qi) ** 2) / h).sum()
    nwin = int(2 * VWIN / 20.0) + 1
    sigma = I0a / 600.0 / (20.0 * math.sqrt(nwin))           # MOCK noise: U4-a central moment-0 pixel S/N = 600 (NOT the archive sensitivity)
    return dict(ra=RA, dec=DEC, nu_line=NU_OBS, restfrq=NU_REST, pix=pix, n=n, beam=beam, dv=20.0, vlo=-1000.0, vhi=2600.0, inc=inc, pa=pa, q_int=qi,
                h=h, vf=vf, rt=rt, s0=s0, kpa=KPA, SdV=SdV, sigma=sigma, seed=942 + ord(kind), label=f"CFG942 U4 MOCK {kind}",
                true={"VC_PB": Vc, "LOGMGAS": lg if lg is not None else -1.0, "SDV": SdV, "INC": inc}), lg, Vc


def required_classes(kind, meas, sc, run):
    run.P("\n=== REQUIRED MOCK CLASS (CFG942 criteria section 2) ===")
    if kind == "d":
        return run.check("U4-d NON-DETECTION: G1 FAIL -> upper limit, no kinematic test", not meas["detected"] and sc["overall"].startswith("G1 FAIL"))
    if kind == "c":
        st = [b["status"] for b in sc["branches"].values()] if isinstance(sc.get("overall"), list) else []
        return run.check("U4-c NOTHING TESTED: TESTS NOTHING", meas["detected"] and st and all(s == "TESTS NOTHING" for s in st), str(st))
    b = sc["branches"].get("incl-primary|P-B", {})
    sd = b.get("sides", {}).get("|4.36|Rg=Rd|canon 9.36e-11")
    ok1 = meas["detected"] and meas["G2"]["reached"]
    run.P(f"  primary branch (canonical, P-B, primary inclination, Rg=Rd, alpha_CO 4.36): {sd}")
    alt = b.get("sides", {}).get("|4.36|Rg=Rd|alt 1.13e-10"); run.P(f"  same branch, alternate footing (reported): {alt}")
    want = "FRAMEWORK SIDE" if kind == "a" else "RIVAL SIDE"
    return run.check(f"U4-{kind} {'FRAMEWORK' if kind == 'a' else 'RIVAL'}: G1 and G2 pass and the primary branch reads {want}", ok1 and sd == want, str(sd))


# ------------------------------------------------------------------------------------------------ selftest pieces
def selftest(run):
    run.P("\n=== R2 reproduction of the sealed U4 numbers by CFG571's own functions (executed read-only) ===")
    w, n, bad = C.reproduce(NS, "U4_27928")
    run.check("R2 reproduction <= 1e-12 dex, FLOOR flags identical", w <= 1e-12 and not bad, f"max |d| {w:.1e} over {n} entries; mismatches {bad}")
    run.P(f"  CFG571 radius 2 R_e = {GEO['R']:.3f} kpc (R_e {GEO['Re']:.3f} kpc), R_d = {GEO['Rd']:.3f} kpc; CFG806 evaluates V_c at 8.3 kpc")
    run.flag("A-U7", f"radius: CFG806 3.1 reads V_c at R = 8.3 kpc; the sealed requirement is computed at CFG571's 2 R_e = {GEO['R']:.3f} kpc. The harness uses 8.3 for V_c and 2 R_e for the requirement (as sealed)")
    run.P("\n=== R3 transcription: CFG806 section 2 table vs the seal ===")
    rows, worst, bad = C.transcription(PLAN, "U4_27928")
    run.check("R3 every CFG806 s2 cell within 0.005 dex of the seal; FLOOR cells identical", rows == 9 and not bad, f"{rows} rows, worst {worst:.4f} dex, mismatches {bad}")
    run.P("\n=== K4 pre-data control of the plan ===")
    run.check("C4 Newtonian round trip (nu = 1): V_bar,req = V_c to < 1e-6", C.newtonian_round_trip(NS) < 1e-6, f"{C.newtonian_round_trip(NS):.1e}")
    b, src = C.beams_table_selftest()
    run.check("I/O: per-plane BEAMS table (no BMAJ keyword) read as the median beam", src == "BEAMS table median" and abs(b[0] - 0.0735) < 1e-6 and abs(b[1] - 0.0635) < 1e-6, f"{b} from {src}")
    run.P("\n=== MOCK-JSON classes through the scoring path (MOCK inputs, no cube) ===")
    base = dict(detected=True, logMgas={"4.36": 10.3, "1.0": 9.7}, sig_rms_dex=0.05, logMgas_UL={}, G2=dict(reached=True, Rmax_kpc=8.0))
    q = Run_quiet()
    s1 = score(dict(base, branches={"incl-primary|P-B": (200.0, 10.0, 20.0)}), q)
    run.check("MOCK-JSON PARTIAL: V_c 200 +- 20 (beam-corrected) -> PARTIAL", s1["branches"]["incl-primary|P-B"]["status"] == "PARTIAL")
    s2 = score(dict(base, branches={"incl-primary|P-B": (180.0, 5.0, 10.0)}), q)
    run.check("MOCK-JSON TESTS NOTHING: V_c 180 +- 10 (beam-corrected)", s2["branches"]["incl-primary|P-B"]["status"] == "TESTS NOTHING")
    s6 = score(dict(base, branches={"incl-primary|P-B": (205.0, 3.0, 8.0)}), q)
    b6 = s6["branches"]["incl-primary|P-B"]
    run.check("MOCK-JSON A-U16: V_c 205, independent-pixel +-3, beam-corrected +-8 -> PARTIAL (the beam-corrected interval decides)",
              b6["status"] == "PARTIAL" and b6["status_indep_info"] == "SCORED", f"{b6['status']} (independent-pixel, information: {b6['status_indep_info']})")
    g7 = gas_req(250.0, "canon 9.36e-11|F-DESI", "Rg=Rd") + 0.2
    s7 = score(dict(base, logMgas={"4.36": g7, "1.0": g7 - 0.64}, branches={"incl-primary|P-B": (250.0, 0.5, 1.0)}), q)
    r7 = next(r for r in s7["branches"]["incl-primary|P-B"]["rows"] if r["foot"].startswith("canon") and r["shape"] == "Rg=Rd" and r["aco"] == "4.36" and r["model"] == "F-DESI")
    run.check(f"MOCK-JSON A-U1: gas 0.2 dex above F-DESI's need at V_c 250 +- 1 -> '{NIT}', never CONSISTENT", r7["cls"] == NIT, r7["cls"])
    okc, names = C.release_copy_selftest("cfg806_u4")
    run.check("A-X7 release-day copy step (temporary files only): byte-identical copies named " + " / ".join(names), okc)
    s3 = score(dict(base, G2=dict(reached=False, Rmax_kpc=4.2), branches={"incl-primary|P-B": (260.0, 5.0, 10.0)}), q)
    run.check("MOCK-JSON G2 FAIL: emission to 4.2 kpc -> RADIUS NOT REACHED", s3["overall"].startswith("G2 FAIL"))
    s4 = score(dict(base, detected=False, logMgas_UL={"4.36": 9.4, "1.0": 8.8}), q)
    run.check("MOCK-JSON NON-DETECTION -> no kinematic test", s4["overall"].startswith("G1 FAIL"))
    s5 = score(dict(base, logMgas={"4.36": 9.0, "1.0": 8.4}, branches={"incl-primary|P-B": (212.0, 3.0, 6.0)}), q)
    r5 = [r for r in s5["branches"]["incl-primary|P-B"]["rows"] if r["foot"].startswith("canon") and r["shape"] == "Rg=Rd" and r["aco"] == "4.36"]
    run.check("MOCK-JSON FLOOR: at V_c 212 the rivals are FLOOR and gas is detected -> IN TENSION (FLOOR)", all(r["cls"] == "IN TENSION (FLOOR)" for r in r5 if r["model"] in ("R-H", "L-fb(RAR-eq)")),
              "; ".join(f"{r['model']} {r['cls']}" for r in r5))
    return dict(reproduction=dict(max_d=w, n=n), transcription=dict(rows=rows, worst=worst))


def power(run):
    run.P("\n=== R6 POWER (information; frozen functions and CFG806 readings; sigma_rms 0.05 dex, V_c error 5 km/s taken as the beam-corrected primary (A-U16); primary branch Rg=Rd, alpha_CO 4.36) ===")
    run.P(f"  gas set equal to one model's requirement; classes of F-DESI / F-flat / R-H and the side (C = consistent, nit = {NIT} (A-U1), T = in tension)")
    out = {}
    for f in C.FOOTS:
        run.P(f"  footing {f}:")
        for V in (200, 210, 220, 225, 230, 240, 250, 260, 275, 300, 325, 350, 375, 400):
            line = []
            for mm in ("F-DESI", "R-H"):
                g = gas_req(float(V), f"{f}|{mm}", "Rg=Rd")
                if g is None: line.append(f"gas=req({mm}): {mm} FLOOR"); continue
                rows = [read_model(g, 0.05, float(V), 5.0, f"{f}|{m}", "Rg=Rd", True) for m in C.MODELS]
                cl = {r["model"]: r["cls"].replace("IN TENSION", "T").replace(NIT, "nit").replace("CONSISTENT", "C") for r in rows}
                sd = side(rows); out[f"{f}|{V}|{mm}"] = dict(classes={r["model"]: r["cls"] for r in rows}, side=sd, gas=g)
                line.append(f"gas=req({mm}) {g:.2f}: F-DESI {cl['F-DESI']}, F-flat {cl['F-flat']}, R-H {cl['R-H']} -> {sd}")
            run.P(f"    V_c {V:3d}: " + " || ".join(line))
    return out


def forecast(run):
    run.P("\n=== R7 SENSITIVITY FORECAST (information; CFG570 archive metadata: 0.4393 mJy/beam at 10 km/s, beam 0.066\"; not re-verified) ===")
    run.P("  CO(2-1) flux for the required gas (alpha_CO 4.36, r21 0.77); noise in a circular aperture over the velocity window; exponential gas disc with R_d = R_half/1.678")
    out = {}
    Rd_as = GEO["Rd"] / KPA
    for V, key in ((250, "canon 9.36e-11|F-DESI"), (275, "canon 9.36e-11|F-DESI"), (300, "canon 9.36e-11|F-DESI"), (275, "canon 9.36e-11|R-H"), (300, "canon 9.36e-11|R-H")):
        g = gas_req(float(V), key, "Rg=Rd"); S = C.SdV_from_Lprime(10 ** g / 4.36 * 0.77, NU_OBS, Z_CAT)
        cells = []
        for rap, W in ((GEO["Re"] / KPA, 600.0), (2 * GEO["Re"] / KPA, 600.0), (2 * GEO["Re"] / KPA, 1000.0)):
            nz, nb = C.aperture_noise_SdV(0.4393, 0.0657, rap, W); fr = C.exp_frac(rap / Rd_as)
            cells.append(f"r {rap:.2f}\" W {W:.0f}: S/N {S * fr / nz:.2f}")
        nz1, _ = C.aperture_noise_SdV(0.4393, 0.0657, 0.0, 600.0)
        cells.append(f"all flux in one beam: S/N {S / nz1:.1f}")
        out[f"{V}|{key}"] = dict(logMgas=g, SdV=S, cells=cells)
        run.P(f"  V_c {V} {key.split('|')[1]:7s} log M_gas {g:.2f} -> S dv {S:.3f} Jy km/s; " + "; ".join(cells))
    run.P("  G1 needs S/N >= 5 in the >= 2 sigma moment-0 mask. At native resolution the extended disc is surface-brightness limited;")
    run.P("  the plan states no taper or smoothing branch (see README ambiguity A-U12).")
    return out


# ------------------------------------------------------------------------------------------------ main
def main():
    mutate = "--mutate" in ARGS
    if "--make-mock" in ARGS:
        kind = opt("--make-mock"); scratch = opt("--scratch"); os.makedirs(scratch, exist_ok=True)
        sp, lg, Vc = mock_spec(kind); path = os.path.join(scratch, f"cfg942_u4_MOCK_{kind}.fits")
        print(f"MOCK cube {os.path.basename(path)} written, sha256 {C.write_mock_cube(path, sp)}"); sys.exit(0)
    if "--selftest" in ARGS:
        slug = "cfg942_u4_selftest"
    elif "--mock" in ARGS:
        slug = f"cfg942_u4_MOCK_{opt('--mock')}" + ("_MUTATE" if mutate else "")
    elif "--cube" in ARGS:
        slug = "cfg942_u4_RELEASE" + ("_MUTATE" if mutate else "")
    elif "--measured" in ARGS:
        slug = "cfg942_u4_measured_" + os.path.splitext(os.path.basename(opt("--measured")))[0]
    else:
        print(__doc__); sys.exit(0)
    run = C.Run(slug, sample_memory=True)
    run.P(f"CFG942 U4_27928 harness ({slug}); plan {PLAN} (1bf70683b); seal CFG571 259f7825c")
    run.P("Frozen predictions = CFG571's four models as sealed. The CFG689 native a0(z) band folded into THEORY_CANONICAL_2026-10-18 does NOT change them and is not scored here.")
    run.P("kappa = 1/2 FITTED; footings never pooled; single disc = demonstration, no exclusion; not theory closed.")
    run.P(f"target: KMOS3D U4_27928 RA {RA:.6f} Dec {DEC:.6f} z {Z_CAT}; CO(2-1) observed at {NU_OBS:.4f} GHz; KMOS3D q {Q_KMOS}")
    clar = C.announce_clarification(run, C.U4_CLAR, __file__)
    run.P(f"memory guard: MallocMediumZone={os.environ.get('MallocMediumZone', 'unset')} (macOS; see the top of this script)")
    snap0 = C.snapshot()
    res = dict(K1=C.verify_frozen(run), memory_guard=dict(MallocMediumZone=os.environ.get("MallocMediumZone")), **clar)
    if run.failed():
        run.P("a frozen file or seal does not match: STOP (nothing scored)"); run.save(res); sys.exit(2)
    run.flag("A-X6", "CFG806 says it 'imports cfg571_prereg.py read-only'; a plain import runs the whole script (rewrites its results JSON, sys.exit). The harness executes only the text above '# ---- controls ----'")
    code = 0; release = None
    if "--selftest" in ARGS:
        res["selftest"] = selftest(run); res["power"] = power(run); res["forecast"] = forecast(run)
    elif "--mock" in ARGS:
        kind = opt("--mock"); scratch = opt("--scratch")
        assert kind in "abcd" and scratch, "--mock a|b|c|d needs --scratch DIR (make the cube first with --make-mock)"
        sp, lg, Vc = mock_spec(kind); path = os.path.join(scratch, f"cfg942_u4_MOCK_{kind}.fits")
        from astropy.io import fits
        hh = fits.getheader(path)
        assert hh.get("OBJECT") == "MOCK" and hh.get("MOCKLAB") == sp["label"], "not this harness's MOCK cube"
        sha = C.sha256_file(path)
        run.P(f"\nMOCK cube: {os.path.basename(path)} sha256 {sha[:16]}… (scratch; not committed). Truth: V_c(P-B, 8.3 kpc) {Vc} km/s, "
              f"log M_gas {lg if lg is None else round(lg, 3)}, S dv {sp['SdV']:.4f} Jy km/s, i {sp['inc']} deg, sigma0 {sp['s0']}, noise {sp['sigma']:.3e} Jy/beam/channel (MOCK)")
        res["mock"] = dict(kind=kind, file=os.path.basename(path), sha256=sha, truth=sp["true"])
        meas = measure(path, run, vshift=2000.0 if mutate else 0.0, c1=("--no-c1" not in ARGS), true_flux=sp["SdV"] or None)
        res["measured"] = {k: v for k, v in meas.items() if k not in ("fits",)}; res["fits"] = meas.get("fits")
        if mutate:
            det = meas["detected"]
            run.P(f"\nMUTATE (velocity axis +2000 km/s): G1 {'PASSED (NOT detected by the control)' if det else 'FAILED -> the control bites (exit 1)'}")
            res["mutate"] = dict(G1=det); code = 0 if det else 1
        else:
            sc = score(meas, run); res["score"] = sc
            res["required_class_ok"] = required_classes(kind, meas, sc, run)
    elif "--cube" in ARGS:
        meas = measure(opt("--cube"), run, vshift=2000.0 if mutate else 0.0, c1=not mutate)
        res["measured"] = {k: v for k, v in meas.items() if k not in ("fits",)}; res["fits"] = meas.get("fits")
        if mutate:
            code = 0 if meas["detected"] else 1; run.P(f"MUTATE: G1 {'PASSED (control did not bite)' if meas['detected'] else 'FAILED (exit 1, control bites)'}")
        else:
            res["score"] = score(meas, run)
            if run.failed(): run.P("A control FAILED: the run is NOT DIAGNOSTIC (CFG806 section 5)."); code = 1
        if C.cube_object(opt("--cube")).strip().upper() == "MOCK":
            run.P("\nrelease-day copy NOT made: the cube's OBJECT is 'MOCK' (the copy into the plan's dir is made only for a real cube; CLARIFICATION A-X7)")
        else:
            release = ("campaign_fresh_gravity/CFG806_u4_27928_scoring", "cfg806_u4" + ("_MUTATE" if mutate else ""))
            res["release_copy"] = dict(dir=release[0], files=[release[1] + ".out", release[1] + "_results.json"])
            run.P(f"\nrelease-day copy (CLARIFICATION A-X7): this output and its results JSON are also written, byte-identical, to {release[0]}/{release[1]}.out and {release[1]}_results.json")
    elif "--measured" in ARGS:
        meas = json.load(open(opt("--measured"))); res["score"] = score(meas, run)
    snap1 = C.snapshot()
    run.check("K5 no frozen file changed during the run (sha256 and mtime)", snap0 == snap1)
    run.P("\nflags raised in this run (harness defaults; see README ambiguity list): " + ", ".join(c for c, _ in run.flags))
    run.save(res)
    if release:
        cp = C.release_copy(C.HERE, slug, os.path.join(C.REPO, release[0]), release[1])
        print("release-day copy written and verified byte-identical: " + "; ".join(f"{k} sha256 {v[:16]}…" for k, v in cp.items()))
    if code == 0 and run.failed() and "--mutate" not in ARGS: code = 1
    sys.exit(code)


if __name__ == "__main__":
    main()
