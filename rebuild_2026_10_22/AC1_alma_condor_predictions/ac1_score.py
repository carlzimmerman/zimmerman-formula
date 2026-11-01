#!/usr/bin/env python3
"""AC1 scoring harness for U4_28473, CO(3-2) (FROZEN_CRITERIA.md section 4, 57d3ac6b64). Scoring only; no prediction changes.
    python3 -B ac1_score.py --selftest DIR    # MOCK cubes in DIR (never committed), required classes; exit 1 on any failure
    python3 -B ac1_score.py --cube FILE       # a real or MOCK cube; real runs write ac1_score_RELEASE.out/.json
    python3 -B ac1_score.py --power DIR --n 6     # MOCK seeds at archive noise: detection and fit recovery
    python3 -B ac1_score.py --cube FILE --mutate   # velocity axis +1000 km/s; exit 1 if G1 fails there (the control bites)
G1 is the frozen moment-0 gate. The 3D statistic always prints; it decides only if ADDENDUM_G1.md is filed here (owner) or, for MOCK cubes, with --test-addendum.
kappa = 1/2 FITTED; footings never pooled; cold dark energy, never a particle; one disc excludes no model; not theory closed."""
import contextlib, hashlib, io, json, math, os, subprocess, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); ROOT = os.path.dirname(REB)
sys.path.insert(0, os.path.join(ROOT, "campaign_fresh_gravity", "CFG942_alma_scoring_readiness"))
_ARGS = sys.argv[1:]; sys.argv = [sys.argv[0]]
import cfg942_common as C
_s = open(os.path.join(HERE, "ac1_predict.py")).read(); _h = _s[:_s.index("# ---- K2, K4 ----")]; PR = {"__file__": os.path.join(HERE, "ac1_predict.py"), "__name__": "ac1_head"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(_h, "ac1_head", "exec"), PR)
assert all(o for _, o in PR["CHK"]), PR["CHK"]
def opt(k, d=None): return _ARGS[_ARGS.index(k) + 1] if k in _ARGS else d
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))

# ---- target, frozen inputs ----
RA, DEC, Z = PR["PC"][0], PR["PC"][1], PR["ZB"]; NU_REST = 345.796; NU = NU_REST / (1 + Z); DZ_G1 = 0.004; VWIN, VCONT = 500.0, 600.0; BOX, HALF = 4.0, 3.4; RFIT = 1.0
F_PUB, eF_PUB = 0.79, 0.08; Q_T = 0.55; RE_G = 1.56; RDG = RE_G / 1.678; KPA = PR["scale"](Z); R31 = 1.8; LP10 = R31 * PR["Lp"](F_PUB, NU, Z)
SHAPES = {"S1": 1.37, "S2": 0.383 * KPA}; LMS = (11.31, 11.35); R_G2 = 3.0; AL_LO, AL_HI = 0.5, 6.0; SENS = 0.4342e-3; BEAM0 = 0.0657
FOOT, RF0 = PR["FOOT"], {"F-flat": 1.0, "F-DESI": PR["ns"]["r_desi"](Z), "band low 0.325": 0.325, "band high 1.212": 1.212, "R-H": PR["ns"]["r_H"](Z), "L-fb(RAR-eq)": PR["ns"]["r_fb"](Z)}
KERN = dict(PR["KERN"]); KERN["Newton"] = PR["nuN"]; LM200 = (12.0, 12.5, 13.0)

# ---- G1-3D (ADDENDUM_G1): smooth, threshold, grow, compare with the same procedure off source ----
Q_MIN = 0.2   # moment-0 q at or below q0 is clamped (A-U11): that branch is flagged and not scored
SM_FWHM, SM_DV, THR_HI, THR_LO, SEED_R, MIN_BIN = 0.15, 100.0, 4.0, 2.5, 0.5, 0.02
def g1_3d(box, rng, vcen=0.0, n=200):
    """box: continuum-subtracted sub-cube. Returns S (Jy km/s) in the 3D mask touching the seed cylinder at the target, the selection-aware S/N and the mask."""
    pix, dv = box["pix"], box["dv"]; b = max(1, int(MIN_BIN // pix)); d = np.nan_to_num(box["data"].astype(np.float32))
    if b > 1:
        ny, nx = d.shape[1] // b, d.shape[2] // b; d = d[:, :ny * b, :nx * b].reshape(d.shape[0], ny, b, nx, b).mean(axis=(2, 4))
    px = pix * b; xc, yc = box["xc"] / b, box["yc"] / b; bp = C.beam_pix(box["beam"], pix) / b ** 2
    sg = SM_FWHM / 2.3548 / px; nv = max(1, int(round(SM_DV / dv)))
    s = ndimage.uniform_filter1d(ndimage.gaussian_filter(d, (0, sg, sg), truncate=3.0), nv, axis=0, mode="nearest")
    v = box["v"]; yy, xx = np.indices(s.shape[1:]); r = np.hypot(xx - xc, yy - yc) * px; off = r > 1.5
    sd = np.array([C.robust_std(s[k][off]) for k in range(s.shape[0])]); sdm = float(np.nanmedian(sd)); z = s / sdm
    lab, nl = ndimage.label(z >= THR_LO, structure=ndimage.generate_binary_structure(3, 1))
    pk = ndimage.maximum(z, lab, index=np.arange(nl + 1)); pk[0] = 0.0; sums = ndimage.sum(d, lab, index=np.arange(nl + 1)) * dv / bp; npx = ndimage.sum(np.ones_like(z), lab, index=np.arange(nl + 1))
    good = pk >= THR_HI; vok = np.abs(v - vcen) <= VWIN
    def at(x0, y0, excl=None):
        rs = SEED_R / px; ya, yb, xa, xb = int(max(0, y0 - rs)), int(y0 + rs + 1), int(max(0, x0 - rs)), int(x0 + rs + 1)
        cyl = np.hypot(xx[ya:yb, xa:xb] - x0, yy[ya:yb, xa:xb] - y0) <= rs; ls = set(np.unique(lab[vok][:, ya:yb, xa:xb][:, cyl])) - {0}
        return [l for l in ls if good[l] and (excl is None or l not in excl)]
    src = at(xc, yc); S = float(sum(sums[l] for l in src)); mask = np.isin(lab, src) if src else np.zeros_like(lab, bool)
    srcset = set(src); null = []; ny, nx = s.shape[1:]; tries = 0; rs = SEED_R / px
    while len(null) < n and tries < 50 * n:
        tries += 1; x0, y0 = rng.uniform(rs + 1, nx - rs - 2), rng.uniform(rs + 1, ny - rs - 2)
        if math.hypot(x0 - xc, y0 - yc) * px < 1.5 + SEED_R: continue
        null.append(float(sum(sums[l] for l in at(x0, y0, srcset))))
    mu, sdn = float(np.mean(null)), float(np.std(null, ddof=1)); sdn = max(sdn, 1e-30)
    # a zero-flux null (no chance component near any seed) has no sd: then the noise of the mask sum sets the scale
    sigv = float(np.nanmedian([C.robust_std(d[k][off]) for k in range(d.shape[0])])); nvox = int(mask.sum()); sig_sum = sigv * dv * math.sqrt(max(nvox, 1) / max(bp, 1e-9)) if nvox else float("nan")
    scale_ = max(sdn, sig_sum) if nvox else sdn; sn = (S - mu) / scale_ if nvox else 0.0
    Rp = float(r[mask.any(axis=0)].max()) if nvox else float("nan")
    return dict(S=S, SN=sn, null_mean=mu, null_sd=sdn, sig_sum=sig_sum, nvox=nvox, n_null=len(null), f_null_nonzero=float(np.mean(np.array(null) != 0)), Rmax_proj_as=Rp, sm_sigma=sdm, n_comp=len(src)), mask, b

# ---- scoring (section 4) ----
def alpha_req(R, V, lms, sh, kn, a0=None, lm200=None):
    Rd, kw = SHAPES[sh] / 1.678, 10 ** lms
    x = PR["mgas_N"](R, V, kw, Rd, RDG, lm200, Z) if kn == "route N" else PR["mgas_req"](R, V, kw, Rd, RDG, a0, KERN[kn])
    return None if x is None else 10 ** x / LP10
def interval(R, V, eV, lms, sh, kn, a0=None, lm200=None):
    nom = alpha_req(R, V, lms, sh, kn, a0, lm200); lo = alpha_req(R, max(V - eV, 1.0), lms + 0.2, sh, kn, a0, lm200); hi = alpha_req(R, V + eV, lms - 0.2, sh, kn, a0, lm200)
    ms_lo, ms_hi = alpha_req(R, V, lms + 0.2, sh, kn, a0, lm200), alpha_req(R, V, lms - 0.2, sh, kn, a0, lm200)
    if alpha_req(R, V, lms - 0.2, sh, kn, a0, lm200) is None: cl = "FLOOR"
    elif hi is None: cl = "FLOOR"
    else:
        l_ = 0.0 if lo is None else lo
        cl = "IN TENSION (above)" if l_ > AL_HI else "IN TENSION (below)" if hi < AL_LO else "CONSISTENT"
    return dict(nominal=nom, lo=lo, hi=hi, class_=cl, ms_width=None if (ms_hi is None) else ms_hi - (ms_lo or 0.0))
def score(V, eV, R):
    S = {}
    for lms in LMS:
        for sh in SHAPES:
            k = f"lgM*{lms}|{sh}"; S[k] = {}
            for kn in ("n=1", "nu_mono", "n=2", "Newton"):
                for fn, a00 in FOOT.items():
                    for mn, rf in RF0.items(): S[k][f"{kn}|{fn}|{mn}"] = interval(R, V, eV, lms, sh, kn, a0=a00 * rf)
            for l in LM200: S[k][f"route N|{l}"] = interval(R, V, eV, lms, sh, "route N", lm200=l)
    return S
def separated(a, b):
    if a["nominal"] is None or b["nominal"] is None or a["ms_width"] is None or b["ms_width"] is None: return False
    return abs(a["nominal"] - b["nominal"]) > max(a["ms_width"], b["ms_width"])

# ---- measurement ----
def measure(path, vshift=0.0, use3d=False, inject=True):
    ex = C.MUTATE_EXCL if vshift else 0.0
    m0d = C.stream_mom0(path, RA, DEC, NU, BOX, VWIN, VCONT, vshift, excl_true=ex); box = C.load_box(path, RA, DEC, NU, HALF, 650.0, VCONT, vshift, excl_true=ex)
    if m0d["beam"] is None: raise SystemExit("no beam: cannot proceed")
    cov = m0d["nu_cover"][0] <= NU <= m0d["nu_cover"][1]; rng = np.random.default_rng(942)
    m = dict(file=m0d["file"], sha256=m0d["sha256"], object=m0d["object"], beam=m0d["beam"], pix=m0d["pix"], dv=m0d["dv"], sig_ch=m0d["sig_ch"], line_covered=bool(cov), nwin=m0d["nwin"], ncont=m0d["ncont"], vshift=vshift)
    P(f"file {m['file']} sha256 {m['sha256'][:16]}; OBJECT {m['object']}; pix {m['pix']:.4f}\", beam {m['beam'][0]:.3f}x{m['beam'][1]:.3f}\", dv {m['dv']:.1f}, sigma/ch {m['sig_ch'] * 1e3:.3f} mJy/beam, line covered {cov}, shift {vshift:+.0f}")
    if m["object"] == "MOCK": P("*** MOCK cube, NOT ALMA DATA ***")
    # frozen G1, moment-0
    im, pix, beam = m0d["m0"], m0d["pix"], m0d["beam"]; bp = C.beam_pix(beam, pix); xc, yc = m0d["xc"], m0d["yc"]; r = C.radius_map(im.shape, xc, yc) * pix
    s0 = C.robust_std(im[r > 2.0]); mask = C.make_mask(im, s0, xc, yc, pix); S = float(np.nansum(im[mask]) / bp); rmax = float(r[mask].max()) if mask.sum() else 0.5
    nul = C.seeded_null(im, s0, mask, xc, yc, pix, bp, rmax + 0.8, 200, rng); mu, sd = float(np.mean(nul)), float(np.std(nul, ddof=1)); snm = (S - mu) / sd if sd > 0 else float("nan")
    zl, off = float("nan"), float("nan")
    if mask.sum():
        w = np.where(mask, np.clip(np.nan_to_num(im), 0, None), 0.0); ys, xs = np.indices(im.shape); cx, cy = (w * xs).sum() / w.sum(), (w * ys).sum() / w.sum(); off = math.hypot(cx - xc, cy - yc) * pix
        ms, _ = C.sub_mask(mask, m0d, box); win = np.abs(box["v"]) <= VWIN; sp = np.clip(np.nansum(box["data"][win][:, ms], axis=1), 0, None)
        if sp.sum() > 0: zl = Z + (1 + Z) * float((sp * box["v"][win]).sum() / sp.sum()) / C.CKMS
    g1m = bool(np.isfinite(snm) and snm >= 5 and off <= 0.5 and abs(zl - Z) <= DZ_G1)
    m["G1_frozen"] = dict(S=S, SN=snm, null_mean=mu, null_sd=sd, offset=off, z_line=zl, mask_pix=int(mask.sum()), PASS=g1m)
    P(f"G1 frozen (moment-0, selection-aware): S {S:.4f} Jy km/s, S/N {snm:.2f}, offset {off:.3f}\", z {zl:.5f} -> {'PASS' if g1m else 'FAIL'}")
    # 3D
    g3, mk3, b = g1_3d(box, rng); zl3 = float("nan")
    if g3["nvox"]:
        sp3 = np.clip((np.nan_to_num(box["data"][:, :mk3.shape[1] * b, :mk3.shape[2] * b]) if b == 1 else np.nan_to_num(box["data"][:, :mk3.shape[1] * b, :mk3.shape[2] * b]).reshape(box["data"].shape[0], mk3.shape[1], b, mk3.shape[2], b).mean(axis=(2, 4))) * mk3, 0, None).sum(axis=(1, 2))
        if sp3.sum() > 0: zl3 = Z + (1 + Z) * float((sp3 * box["v"]).sum() / sp3.sum()) / C.CKMS
    g1d = bool(g3["SN"] >= 5 and abs(zl3 - Z) <= DZ_G1); g3.update(z_line=zl3, PASS=g1d); m["G1_3D"] = g3
    P(f"G1-3D (addendum, {'decides' if use3d else 'information only'}): S {g3['S']:.4f} Jy km/s in {g3['nvox']} voxels, S/N {g3['SN']:.2f} (null mean {g3['null_mean']:.4f}, sd {g3['null_sd']:.4f}, mask-sum noise {g3['sig_sum']:.4f}, null nonzero {g3['f_null_nonzero']:.2f}), z {zl3:.5f} -> {'PASS' if g1d else 'FAIL'}")
    m["detected"] = g1d if use3d else g1m; m["gate"] = "G1-3D (addendum)" if use3d else "G1 frozen"
    circ = r <= 1.0; oc = C.random_offsets(rng, circ, im.shape, xc, yc, 1.3 / pix, 100); ap = C.translated_apertures(im, circ, bp, oc); rmsc = float(np.std(ap, ddof=1)) if len(ap) > 2 else float("nan"); m["UL"] = dict(aperture_as=1.0, rms=rmsc, UL3=3 * rmsc, ap_flux=float(np.nansum(im[circ]) / bp), n=len(ap))
    P(f"1\" radius aperture flux {m['UL']['ap_flux']:.3f} +- {rmsc:.3f} Jy km/s against published {F_PUB} +- {eF_PUB}; 3 sigma limit {3 * rmsc:.3f}; off-source rms against archive sensitivity: sigma/ch x sqrt(dv/10) = {m['sig_ch'] * 1e3 * math.sqrt(m['dv'] / 10):.3f} mJy/beam at 10 km/s, archive 0.434")
    if not m["detected"]: P(f"{m['gate']} FAILED: upper limit reported, no kinematic test (criteria section 4)"); return m, box
    Sref = g3["S"] if use3d else S
    m["flux_check"] = dict(S=Sref, ratio=Sref / F_PUB, within_30pct=bool(abs(Sref / F_PUB - 1) <= 0.3)); P(f"flux check: measured/published {Sref / F_PUB:.2f}" + ("" if m["flux_check"]["within_30pct"] else " FLAG: outside 30%; the published flux governs L'"))
    # kinematics, branches never pooled
    sub2 = C.sub_mask(mask, m0d, box)[0] if not use3d else None
    m0s = np.nansum(box["data"][np.abs(box["v"]) <= VWIN], axis=0) * m["dv"]; s2 = C.robust_std(m0s[C.radius_map(m0s.shape, box["xc"], box["yc"]) * pix > 2.0])
    mm = sub2 if sub2 is not None and sub2.sum() else (ndimage.zoom(mk3.any(axis=0).astype(float), b, order=0) > 0.5)[:m0s.shape[0], :m0s.shape[1]]
    if mm.shape != m0s.shape:
        t = np.zeros_like(m0s, bool); t[:mm.shape[0], :mm.shape[1]] = mm; mm = t
    gf = C.fit_gauss2d(m0s, s2, pix, beam, box["xc"], box["yc"], half=1.2); ip, _ = C.inc_from_q(gf["q"]); it, _ = C.inc_from_q(Q_T)
    pa0, vs0, amp, _ = C.kinematic_pa(box, m0s, mm, VWIN, box["xc"], box["yc"]); h0 = max(gf["fwhm_maj"] / 2.5, 0.05)
    m.update(q_mom0=gf["q"], inc_mom0=ip, inc_tadaki=it); P(f"moment-0 q {gf['q']:.3f} -> i {ip:.1f}; Tadaki q4.4 {Q_T} -> i {it:.1f}; initial PA {math.degrees(pa0):.0f}, vsys {vs0:.0f}, amp {amp:.0f}")
    ys, xs = np.nonzero(mm); wt = np.clip(np.nan_to_num(m0s[ys, xs]), 0, None) + 1e-30; fits = {}; branches = {}
    for nm, inc, clamped in (("incl-mom0", ip, not (Q_MIN < gf["q"] < 1.0)), ("incl-Tadaki", it, False)):
        trials = [C.fit_disc(box, inc, KPA, m["sig_ch"], (0.0, 0.0), pa0, vs0, v0, h0, R_G2, RDG, rfit=RFIT) for v0 in (max(amp / max(math.sin(math.radians(inc)), 0.2), 50.0), 300.0, 500.0)]
        fd0 = min(trials, key=lambda t: t["chi2"]); near = [t for t in trials if t["chi2"] - fd0["chi2"] <= 9.0]; p = fd0["params"]
        vcs = [C.vc_from_params(np.array(t["params"]), np.array(t["cov"]), R_G2, RDG)["Vc_PB"] for t in near]; spread = (max(vcs) - min(vcs)) / max(np.median(vcs), 1.0)
        c_, s_ = math.cos(p[2]), math.sin(p[2]); X, Y = (xs - box["xc"]) * pix - p[0], (ys - box["yc"]) * pix - p[1]
        xr, yr = X * c_ + Y * s_, -X * s_ + Y * c_; Rdp = np.hypot(xr, yr / max(math.cos(math.radians(inc)), 0.05)) * KPA; o = np.argsort(Rdp); cw = np.cumsum(wt[o]) / wt.sum(); Rdep = float(Rdp[o][np.searchsorted(cw, 0.9)]); reached = Rdep >= R_G2; Rs = R_G2 if reached else max(Rdep, 0.5)
        cov = np.array(fd0["cov"]); v = C.vc_from_params(np.array(p), cov * bp, Rs, RDG)
        atb = [n for n, i_, lo, hi in (("V_f", 4, 10.0, 800.0), ("R_t", 5, 0.05, 15.0), ("sigma0", 6, 3.0, 250.0), ("h", 8, 0.01, 3.0)) if p[i_] <= lo * 1.02 or p[i_] >= hi * 0.98]
        valid = not clamped and not atb and spread <= 0.15 and np.isfinite(v["eVc_PB"]) and v["eVc_PB"] / max(v["Vc_PB"], 1.0) <= 0.25 and np.isfinite(v["eVc_P0"]) and v["eVc_P0"] / max(v["Vc_P0"], 1.0) <= 0.25
        fits[nm] = dict(params=p, names=fd0["names"], chi2N=fd0["chi2"] / fd0["nvox"], inc=inc, G2_reached=reached, R90_dep_kpc=Rdep, R_score=Rs, V=v, valid=bool(valid), at_bound=atb, start_spread=spread, inc_clamped=bool(clamped))
        if valid: branches[f"{nm}|P-B"] = (v["Vc_PB"], v["eVc_PB"], Rs); branches[f"{nm}|P0"] = (v["Vc_P0"], v["eVc_P0"], Rs)
        P(f"thin-disc fit [{nm}, i {inc:.1f}]: V_f {p[4]:.0f}, R_t {p[5]:.2f} kpc, sigma0 {p[6]:.0f}, h {p[8]:.3f}\"; G2 {'PASS' if reached else 'FAIL'} (90% flux radius {Rdep:.2f} kpc), at {Rs:.2f} kpc: V_c P-B {v['Vc_PB']:.0f} +- {v['eVc_PB']:.0f}, P0 {v['Vc_P0']:.0f} +- {v['eVc_P0']:.0f}; chi2/N {fits[nm]['chi2N']:.3f}; start spread {spread:.2f}; at bound {atb}; " + ("scored" if valid else "FIT NOT CONSTRAINED: not scored"))
    m["fits"], m["branches"] = fits, branches; m["score"] = {}
    for bn, (V, eV, Rs) in branches.items():
        if not (V > 0 and np.isfinite(eV)): continue
        sc = score(float(V), float(eV), float(Rs)); m["score"][bn] = sc; c0 = "canon 9.36e-11"
        for k in ("lgM*11.31|S1", "lgM*11.31|S2"):
            row = sc[k]; fm = lambda e: f"{'FLOOR' if e['nominal'] is None else format(e['nominal'], '.2f')} [{e['class_']}]"
            P(f"  {bn} {k}: alpha_req n=1 flat {fm(row[f'n=1|{c0}|F-flat'])}; F-DESI {fm(row[f'n=1|{c0}|F-DESI'])}; R-H {fm(row[f'n=1|{c0}|R-H'])}; Newton {fm(row[f'Newton|{c0}|F-flat'])}; route N 12.5 {fm(row['route N|12.5'])}")
            sep = separated(row[f"n=1|{c0}|F-flat"], row[f"n=1|{c0}|R-H"]); P(f"    flat vs R-H: {'separated' if sep else 'not separated'}")
    # C1: injection into off-source noise of this cube
    if inject and not vshift:
        m["C1"] = injection(box, m, it)
    return m, box

def injection(box, m, inc):
    pix, dv, beam = box["pix"], box["dv"], box["beam"]; res = {}; dx = int(round(2.0 / pix))
    xc, yc = box["xc"] + dx, box["yc"]; half = int(RFIT / pix) + 6
    for Vt in (300.0, 430.0):
        s0, rt = 40.0, 0.5; R = R_G2; vr = math.sqrt(max(Vt ** 2 - 2 * s0 ** 2 * R / RDG, 1.0)); vf = vr / (2 / math.pi * math.atan(R / rt))
        ny, nx = box["data"].shape[1:]; y0, y1, x0, x1 = max(0, int(yc) - half), min(ny, int(yc) + half + 1), max(0, int(xc) - half), min(nx, int(xc) + half + 1)
        d = np.nan_to_num(box["data"][:, y0:y1, x0:x1].astype(np.float64)); yy, xx = np.indices(d.shape[1:]); X, Y = (xx - (xc - x0)) * pix, (yy - (yc - y0)) * pix
        kf = C.kernel_rfft(d.shape[1:], beam, pix); h = RDG / KPA; bp = C.beam_pix(beam, pix); pa = 0.5; c, s = math.cos(pa), math.sin(pa); ci = math.cos(math.radians(inc))
        xr, yr = X * c + Y * s, -X * s + Y * c; I0 = F_PUB * bp / np.exp(-np.hypot(xr, yr / ci) / h).sum()
        p = [0.0, 0.0, pa, 0.0, vf, rt, s0, I0, h]; b2 = dict(box); b2["data"] = (d + C.disc_model(p, X, Y, box["v"], dv, inc, KPA, kf)).astype(np.float32); b2["xc"], b2["yc"] = xc - x0, yc - y0
        fd = C.fit_disc(b2, inc, KPA, m["sig_ch"], (0.0, 0.0), pa, 0.0, vf * 0.9, h, R, RDG, rfit=RFIT, I0=I0 * 0.9)
        rv = fd["Vc_PB"] / Vt; res[str(Vt)] = dict(V_true=Vt, V_rec=fd["Vc_PB"], eV_beamcorr=fd["eVc_PB_beamcorr"], ratio=rv, within_15pct=bool(abs(rv - 1) <= 0.15))
        P(f"C1 injection V_c {Vt:.0f}, flux {F_PUB} into off-source noise: recovered {fd['Vc_PB']:.0f} +- {fd['eVc_PB_beamcorr']:.0f} (ratio {rv:.2f}) -> {'within' if abs(rv - 1) <= 0.15 else 'NOT within'} 15%")
    return res

# ---- MOCK ----
def spec(kind, seed=None):
    Vc, s0, rt, inc = 430.0, 40.0, 0.5, C.inc_from_q(Q_T)[0]; F = F_PUB; Reg = RE_G; nf = 1.0
    if kind == "bright": nf = 1 / 30.0
    if kind == "noise": F = 0.0
    if kind == "compact": Reg = 0.8
    if kind == "tension": Vc, nf = 300.0, 1 / 30.0
    vr = math.sqrt(Vc ** 2 - 2 * s0 ** 2 * R_G2 / RDG); vf = vr / (2 / math.pi * math.atan(R_G2 / rt)); dv = 20.0
    return dict(ra=RA, dec=DEC, nu_line=NU, restfrq=NU_REST, pix=BEAM0 / 3, n=512, beam=(0.070, 0.062, 30.0), dv=dv, vlo=-1560.0, vhi=1560.0, inc=inc, pa=0.5, q_int=math.cos(math.radians(inc)), h=(Reg / 1.678) / KPA, vf=vf, rt=rt, s0=s0, kpa=KPA,
                SdV=F, sigma=SENS * math.sqrt(10 / dv) * nf, seed=(9420 + sum(map(ord, kind))) if seed is None else seed, label=f"AC1 MOCK {kind}", true={"VC_PB": Vc, "SDV": F}), Vc
def selftest(d):
    os.makedirs(d, exist_ok=True); ok = []; RES = {}; use3 = True
    def need(n, c, x=""): ok.append((n, bool(c))); P(f"[{'PASS' if c else 'FAIL'}] {n} {x}")
    for kind in ("realistic", "compact", "noise", "bright", "tension"):
        sp, Vc = spec(kind); p = os.path.join(d, f"AC1_MOCK_{kind}.fits"); C.write_mock_cube(p, sp)
        P(f"\n=== MOCK {kind}: V_c {Vc:.0f}, flux {sp['SdV']}, noise {'archive' if sp['sigma'] > 1e-4 else 'archive/30'} ===")
        m, _ = measure(p, use3d=use3, inject=kind in ("realistic", "bright")); RES[kind] = m
        if kind == "noise":
            need("noise: frozen G1 fails", not m["G1_frozen"]["PASS"]); need("noise: G1-3D fails", not m["G1_3D"]["PASS"], f"S/N {m['G1_3D']['SN']:.2f}")
        if kind == "bright":
            need("bright: G1-3D passes", m["G1_3D"]["PASS"], f"S/N {m['G1_3D']['SN']:.1f}"); b = m["branches"].get("incl-Tadaki|P-B")
            need("noise-limited mock not forced: bright fit scored", m["fits"]["incl-Tadaki"]["valid"]); need("bright: V_c within 15% on the Tadaki P-B branch", b and abs(b[0] / Vc - 1) <= 0.15, f"{b[0]:.0f} of {Vc:.0f}" if b else "")
            need("bright: flux within 30%", m["flux_check"]["within_30pct"], f"{m['flux_check']['ratio']:.2f}")
            need("bright: injection within 15%", all(v["within_15pct"] for v in m["C1"].values()))
            s = m["score"]["incl-Tadaki|P-B"]["lgM*11.31|S1"]["Newton|canon 9.36e-11|F-flat"]; need("bright: V_c 430 reads FLOOR on lg M* 11.31, S1 (stars exceed)", s["class_"] == "FLOOR", s["class_"])
        if kind == "tension":
            s = m["score"]["incl-Tadaki|P-B"]["lgM*11.31|S2"]["n=1|canon 9.36e-11|F-flat"]; need("tension: V_c 300 reads FLOOR on lg M* 11.31, S2", s["class_"] == "FLOOR", s["class_"])
        if kind == "bright":
            P("\n--- MUTATE on bright: velocity axis +1000 ---"); mm, _ = measure(p, vshift=1000.0, use3d=use3, inject=False); RES["bright_MUTATE"] = mm
            need("MUTATE: frozen G1 and G1-3D both fail", not mm["G1_frozen"]["PASS"] and not mm["G1_3D"]["PASS"], f"S/N {mm['G1_frozen']['SN']:.2f}, {mm['G1_3D']['SN']:.2f}")
        os.remove(p)
    P("\nselftest: " + ", ".join(f"{'PASS' if o else 'FAIL'}" for _, o in ok))
    json.dump(dict(checks=ok, results=RES), open(os.path.join(HERE, "ac1_score_selftest_results.json"), "w"), indent=0, default=str)
    open(os.path.join(HERE, "ac1_score_selftest.out"), "w").write("\n".join(OUT) + "\n")
    return all(o for _, o in ok)

def power(d, N):
    os.makedirs(d, exist_ok=True); T = {"realistic": [], "compact": [], "noise": []}
    for kind in T:
        for i in range(N):
            sp, Vc = spec(kind, seed=70000 + 97 * i + sum(map(ord, kind))); p = os.path.join(d, f"AC1_MOCK_power_{kind}.fits"); C.write_mock_cube(p, sp)
            n0 = len(OUT); m, _ = measure(p, use3d=True, inject=False); del OUT[n0:]; f = m.get("fits", {}).get("incl-Tadaki")
            T[kind].append(dict(seed=i, m0=m["G1_frozen"]["SN"], g3=m["G1_3D"]["SN"], det=m["G1_3D"]["PASS"], valid=bool(f and f["valid"]), Vc=f["V"]["Vc_PB"] if f else None, eV=f["V"]["eVc_PB"] if f else None, R90=f["R90_dep_kpc"] if f else None, S=m["G1_3D"]["S"])); os.remove(p)
            P(f"POWER {kind} {i}: " + json.dumps(T[kind][-1], default=str))
    summ = {k: dict(N=len(v), m0_pass=sum(x["m0"] >= 5 for x in v), g3_pass=sum(x["det"] for x in v), valid=sum(x["valid"] for x in v), Vc_valid=[round(x["Vc"]) for x in v if x["valid"]]) for k, v in T.items()}
    P("POWER summary " + json.dumps(summ)); json.dump(dict(runs=T, summary=summ, note="MOCK smooth exponential discs at the archive sensitivity; V_c 430; never real data"), open(os.path.join(HERE, "ac1_score_power_results.json"), "w"), indent=0, default=str)
    open(os.path.join(HERE, "ac1_score_power.out"), "w").write("\n".join(OUT) + "\n")

def main():
    want = "57d3ac6b64"; cur = hashlib.sha256(open(os.path.join(HERE, "FROZEN_CRITERIA.md"), "rb").read()).hexdigest()
    old = hashlib.sha256(subprocess.run(["git", "show", f"{want}:rebuild_2026_10_22/AC1_alma_condor_predictions/FROZEN_CRITERIA.md"], cwd=ROOT, capture_output=True).stdout).hexdigest()
    if cur != old: raise SystemExit("FROZEN_CRITERIA.md differs from its freezing commit")
    P(f"AC1 scoring harness; criteria {want} unchanged; kappa = 1/2 FITTED; one disc excludes no model; not theory closed")
    if "--selftest" in _ARGS: sys.exit(0 if selftest(opt("--selftest")) else 1)
    if "--power" in _ARGS: power(opt("--power"), int(opt("--n", "6"))); sys.exit(0)
    path = opt("--cube"); mock = C.cube_object(path) == "MOCK"; filed = os.path.exists(os.path.join(HERE, "ADDENDUM_G1.md")); use3 = filed or (mock and "--test-addendum" in _ARGS)
    if "--mutate" in _ARGS:
        m, _ = measure(path, vshift=1000.0, use3d=use3, inject=False); bite = not m["detected"]; P(f"MUTATE +1000 km/s: {'bites (exit 1)' if bite else 'DOES NOT BITE'}"); tag = "_MUTATE"
    else:
        m, _ = measure(path, use3d=use3); bite = False; tag = ""
    if not mock:
        json.dump(m, open(os.path.join(HERE, f"ac1_score_RELEASE{tag}.json"), "w"), indent=0, default=str); open(os.path.join(HERE, f"ac1_score_RELEASE{tag}.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(1 if bite else 0)
main()
