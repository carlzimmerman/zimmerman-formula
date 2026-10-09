"""CFG523 stage 2: fetch line sub-cubes for the shortlist (public pipeline pbcor cubes) and apply the measured gates M1-M3.
Criteria: FROZEN_CRITERIA.md (429b1d7a6). Inputs: cfg523_inventory_results.json (shortlist), DataLink tables saved in the work dir.
Run: nice -n 10 python3 cfg523_cubes.py   (fetches once; sub-cubes cached as FITS in ../../../_external_data/cfg523_work/subcubes/)
MUTATE=1: V_rot x 0.5 in the analysis stage (only reached for REACHES-DEEP rows with measured gas); with no analysed rows the
MUTATE run instead scrambles the channel order of every sub-cube (velocity field destroyed) and M2 must fail for every cube.
"""
import glob, hashlib, json, math, os, sys, warnings
warnings.filterwarnings('ignore')
import numpy as np
from astropy.io import fits
from astropy.table import Table
from astropy.wcs import WCS
from scipy.ndimage import gaussian_filter, map_coordinates
from scipy.special import i0, i1, k0, k1
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg523_fetch as F

HERE = os.path.dirname(os.path.abspath(__file__)); WORK = F.WORK
SUB = os.path.join(WORK, "subcubes"); os.makedirs(SUB, exist_ok=True)
MUTATE = os.environ.get("MUTATE") == "1"; TAG = "_MUTATE" if MUTATE else ""
CONTROL = os.environ.get("CONTROL")      # POST-FREEZE positive control (dated note 2026-10-09): run the same gates on a named relaxed-list galaxy with a published detection
if CONTROL: TAG += "_CONTROL"
SMOOTH = float(os.environ.get("SMOOTH", "0"))   # POST-FREEZE diagnostic (dated note 2026-10-09): image-plane Gaussian smoothing to this FWHM (arcsec)
if SMOOTH: TAG += f"_SMOOTH{SMOOTH:g}"
FOOT = {"A": 9.36e-11, "B": 1.13e-10}; G = 6.674e-11; MSUN = 1.989e30; KPC = 3.0857e19; C = 299792.458
LINES = {"CO(3-2)": 345.796, "CO(4-3)": 461.041, "CO(5-4)": 576.268, "CO(6-5)": 691.473, "CO(7-6)": 806.652,
         "[CI](1-0)": 492.161, "[CI](2-1)": 809.342, "[CII]": 1900.537}
PREF = ["CO(3-2)", "CO(4-3)", "[CI](1-0)", "CO(5-4)", "CO(6-5)", "CO(7-6)", "[CI](2-1)", "[CII]"]   # lowest-J first
VWIN, VLINE, BOX = 1000.0, 400.0, 5.0
out = []
def say(s=""):
    print(s, flush=True); out.append(s)
def g_freeman(M, Rd, R):
    y = R / (2 * Rd); return 2 * G * M * MSUN / (Rd * KPC) * y ** 2 * (i0(y) * k0(y) - i1(y) * k1(y)) / (R * KPC)

inv = json.load(open(os.path.join(HERE, "cfg523_inventory_results.json")))
res = []
TARGETS = [g for g in inv["relaxed"] if CONTROL in g["ids"]] if CONTROL else inv["shortlist"]
for g in TARGETS:
    name = "/".join(g["ids"]); say(f"\n=== {name}  z {g['z']:.4f}  y_pred(2Re) {g['y_out']['A']:.2f}")
    # pick the coverage row: lowest-J line, then best resolution
    covs = sorted(g["cov_pub03"], key=lambda h: (PREF.index(h["line"]), h["res"]))
    rec = dict(name=name, z=g["z"], lm=g["lm"], re_kpc=g["re_kpc"], kpc_as=g["kpc_as"], Mbar=g["Mbar"], y_pred=g["y_out"], label=None, notes=[])
    chosen = None
    for h in covs:
        dl = os.path.join(WORK, "datalink_" + h["ous"].replace("uid://", "").replace("/", "_") + ".ecsv")
        if not os.path.exists(dl):
            rec["notes"].append(f"no DataLink table for {h['ous']}"); continue
        t = Table.read(dl)
        urls = [str(u) for u in t["access_url"] if str(u).endswith(".cube.I.pbcor.fits") and h["target"] in str(u)]
        if not urls:
            rec["notes"].append(f"{h['proposal']} {h['ous']}: no pipeline pbcor cube for target {h['target']} (raw only)"); continue
        nu = LINES[h["line"]] / (1 + g["z"]) * 1e9
        for u in sorted(urls, key=lambda u: ("ari_l" in u, u)):          # pipeline first, then ARI-L
            hdr, hl = F.header(name, u)
            w = WCS(hdr).sub([3]); n3 = hdr["NAXIS3"]
            f0, f1 = sorted(w.wcs_pix2world([0, n3 - 1], 0)[0])
            if f0 < nu < f1:
                chosen = (h, u, hdr, hl); break
        if chosen: break
        rec["notes"].append(f"{h['proposal']}: no cube of {h['target']} contains {h['line']} at {nu/1e9:.3f} GHz")
    if not chosen:
        rec["label"] = "NOT USEFUL (no pipeline cube holds the line)"; say("  " + rec["label"] + "; " + "; ".join(rec["notes"])); res.append(rec); continue
    h, u, hdr, hl = chosen
    rec.update(proposal=h["proposal"], line=h["line"], url=u, ous=h["ous"])
    nu = LINES[h["line"]] / (1 + g["z"]) * 1e9
    fn = os.path.join(SUB, os.path.basename(u).replace(".fits", f".sub_{h['line'].replace('[','').replace(']','').replace('(','').replace(')','')}.fits"))
    if not os.path.exists(fn):
        w3 = WCS(hdr).celestial
        px, py = w3.wcs_world2pix([[g["ra"], g["dec"]]], 0)[0]
        pix = abs(hdr["CDELT2"]) * 3600; r = int(math.ceil(BOX / pix))
        x0, x1 = max(0, int(px) - r), min(hdr["NAXIS1"], int(px) + r + 1); y0, y1 = max(0, int(py) - r), min(hdr["NAXIS2"], int(py) + r + 1)
        wf = WCS(hdr).sub([3]); dnu = abs(hdr["CDELT3"])
        cc = float(wf.wcs_world2pix([nu], 0)[0][0]); nch = int(math.ceil(nu * VWIN / C / dnu))
        c0, c1 = max(0, int(cc) - nch), min(hdr["NAXIS3"], int(cc) + nch + 1)
        if x1 <= x0 or y1 <= y0:
            rec["label"] = "NOT USEFUL (target outside the cube)"; res.append(rec); say("  " + rec["label"]); continue
        data = F.subcube(name, u, hdr, hl, c0, c1, y0, y1, x0, x1)
        nh = WCS(hdr).sub([1, 2, 3]).slice((slice(c0, c1), slice(y0, y1), slice(x0, x1))).to_header()
        for k in ("BMAJ", "BMIN", "BPA", "BUNIT", "RESTFRQ", "SPECSYS", "OBJECT"):
            if k in hdr: nh[k] = hdr[k]
        nh["ORIGURL"] = u[:68]; nh["ORIGCH"] = f"{c0}:{c1}"; nh["ORIGROW"] = f"{y0}:{y1}"; nh["ORIGCOL"] = f"{x0}:{x1}"
        fits.writeto(fn, data, nh, overwrite=True)
    d, nh = fits.getdata(fn), fits.getheader(fn)
    rec["subcube"] = os.path.relpath(fn, WORK); rec["subcube_sha256"] = hashlib.sha256(open(fn, "rb").read()).hexdigest()
    # ---- velocity axis ----
    wf = WCS(nh).sub([3]); freqs = wf.wcs_pix2world(np.arange(d.shape[0]), 0)[0]
    v = C * (nu - freqs) / nu                                    # radio-ish, relative to the parent z
    order = np.argsort(v); v = v[order]; d = d[order]
    keep = np.isfinite(d).any(axis=(1, 2)); v, d = v[keep], d[keep]          # drop fully blanked channels
    if MUTATE:
        rng = np.random.default_rng(523); d = d[rng.permutation(d.shape[0])]
    dv = float(np.median(np.abs(np.diff(v))))
    bmaj, bmin = nh["BMAJ"] * 3600, nh["BMIN"] * 3600; pix = abs(nh["CDELT2"]) * 3600
    if SMOOTH and SMOOTH > bmaj:
        sk = math.sqrt(SMOOTH ** 2 - bmaj * bmin) / 2.3548 / pix
        d = np.stack([gaussian_filter(np.nan_to_num(p), sk) for p in d]); bmaj = bmin = SMOOTH
    rec.update(beam_as=[round(bmaj, 3), round(bmin, 3)], dv_kms=round(dv, 1), nchan=int(d.shape[0]))
    lf = (np.abs(v) > VLINE + 100) & np.isfinite(d).all(axis=(1, 2)) if False else (np.abs(v) > VLINE + 100)
    ln = np.abs(v) <= VLINE
    # DATED NOTE 2026-10-09 (after the first pass): per-pixel continuum subtraction (median of the line-free channels) added; the first
    # pass summed continuum into moment 0, which matters for dusty band-6/7 targets (GS4_20422 passed M1 on continuum). All cubes re-run.
    d = d - np.nanmedian(d[lf], axis=0)[None]
    dd = np.nan_to_num(d)
    mom0 = dd[ln].sum(axis=0) * dv
    # DATED NOTE 2026-10-09: moment-0 noise = robust spatial rms of the moment-0 map itself outside 1.5" of the target (includes the
    # continuum-subtraction noise and channel correlation); replaces the per-pixel channel-MAD estimate of the first pass.
    yy, xx = np.indices(mom0.shape); w2 = WCS(nh).celestial
    tx, ty = w2.wcs_world2pix([[g["ra"], g["dec"]]], 0)[0]
    outer = (np.hypot(xx - tx, yy - ty) * pix > 1.5) & np.isfinite(d).all(axis=0)
    smom0 = 1.4826 * np.median(np.abs(mom0[outer] - np.median(mom0[outer])))
    snr = mom0 / smom0
    near = np.hypot(xx - tx, yy - ty) * pix <= 1.0
    pk = float(np.nanmax(np.where(near, snr, -np.inf)))
    rec["M1_peak_snr_within1as"] = round(pk, 2)
    say(f"  {h['proposal']} {h['line']} beam {bmaj:.3f}x{bmin:.3f}\" dv {dv:.1f} km/s, channels {d.shape[0]} (line {ln.sum()}), peak mom0 S/N within 1\" = {pk:.1f}")
    if not pk >= 5:
        rec["label"] = "NOT USEFUL (M1: no detection, peak S/N < 5)"; say("  " + rec["label"]); res.append(rec); continue
    # ---- moment 1 on the S/N >= 3 island connected to the peak ----
    from scipy.ndimage import label as cclabel
    lab, _ = cclabel(snr >= 3)
    pki = np.unravel_index(np.argmax(np.where(near, snr, -np.inf)), snr.shape); m = lab == lab[pki]
    wgt = np.clip(dd[ln], 0, None)
    mom1 = np.where(m, (wgt * v[ln][:, None, None]).sum(0) / np.maximum(wgt.sum(0), 1e-30), np.nan)
    cy, cx = np.average(yy[m], weights=mom0[m]), np.average(xx[m], weights=mom0[m])
    sm = np.where(m, gaussian_filter(np.nan_to_num(mom1), 1.0), np.nan)
    iy, ix = np.unravel_index(np.nanargmax(sm), sm.shape); jy, jx = np.unravel_index(np.nanargmin(sm), sm.shape)
    pa = math.atan2(iy - jy, ix - jx)
    ux, uy = math.cos(pa), math.sin(pa)
    # slit samples at beam spacing, beam-wide average of mom1 and S/N
    step = bmaj / pix; prof = []
    for k in range(-20, 21):
        sx, sy = cx + k * step * ux, cy + k * step * uy
        ap = np.hypot(xx - sx, yy - sy) <= 0.5 * bmaj / pix
        if not ap.any(): continue
        s_ap = float(np.nanmean(snr[ap])); v_ap = float(np.nanmean(mom1[ap & m])) if (ap & m).any() else float("nan")
        prof.append((k * bmaj, s_ap, v_ap))
    good = [p for p in prof if p[1] >= 3 and math.isfinite(p[2])]
    gv = [p[2] for p in sorted(good)]
    mono = len(gv) >= 3 and (all(np.diff(gv) >= -0.5 * dv) or all(np.diff(gv) <= 0.5 * dv)) and abs(gv[-1] - gv[0]) > 2 * dv
    # R_out: largest |r| along the axis (pixel-level) with S/N >= 3, contiguous from the centre
    rr = np.arange(0, 6.0 / pix, 0.5)
    def reach(sgn):
        last = 0.0
        for t in rr:
            val = map_coordinates(snr, [[cy + sgn * t * uy], [cx + sgn * t * ux]], order=1)[0]
            if val >= 3: last = t
            else: break
        return last * pix
    Rout_as = max(reach(+1), reach(-1)); Rout = Rout_as * g["kpc_as"]
    rec.update(PA_deg=round(math.degrees(pa), 1), slit=[(round(a, 3), round(b, 2), round(c, 1)) for a, b, c in prof], n_good=len(good),
               monotonic=bool(mono), Rout_as=round(Rout_as, 3), Rout_kpc=round(Rout, 2), dV_obs=round(gv[-1] - gv[0], 1) if gv else None)
    say(f"  M2: PA {math.degrees(pa):.0f} deg, {len(good)} beam-spaced positions with S/N >= 3, monotonic {mono}, dV_obs {rec['dV_obs']} km/s, "
        f"R_out {Rout_as:.2f}\" = {Rout:.2f} kpc (beam {bmaj:.2f}\")")
    if not (len(good) >= 3 and mono and Rout_as >= bmaj):
        rec["label"] = "NOT USEFUL (M2: rotation not resolved to >= 3 beams / R_out < 1 beam)"; say("  " + rec["label"]); res.append(rec); continue
    Rd = g["re_kpc"] / 1.678
    ym = {k: g_freeman(g["Mbar"], Rd, Rout) / a for k, a in FOOT.items()}
    rec["y_meas"] = ym
    rec["label"] = "REACHES-DEEP" if max(ym.values()) <= 2 else "NEAR-NEWTONIAN"
    say(f"  M3: y_meas(R_out) = {ym['A']:.2f} (9.36e-11) / {ym['B']:.2f} (1.13e-10) -> {rec['label']}")
    res.append(rec)

say("\nSUMMARY")
for r in res:
    say(f"  {r['name']:28s} {r.get('proposal','-'):15s} {r.get('line','-'):10s} {r['label']}  R_out {r.get('Rout_kpc','-')} kpc  y_meas {r.get('y_meas',{}).get('A','-')}")
led = F._led(); say(f"\nbytes fetched (cumulative ledger, incl. the 223.7 MB probe): {led['used']:,} in {led['requests']} requests")
if MUTATE:
    n_m2 = sum(1 for r in res if r["label"] in ("REACHES-DEEP", "NEAR-NEWTONIAN"))
    say(f"MUTATE premise (channel scramble): cubes passing M2 = {n_m2} (must be 0)")
    ok = n_m2 == 0
    say("MUTATE premise " + ("MET" if ok else "NOT MET") + "; MUTATE forces rc 1")
json.dump({"lane": "CFG523", "stage": "cubes", "mutate": MUTATE, "results": res}, open(os.path.join(HERE, f"cfg523_cubes_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg523_cubes{TAG}.out"), "w").write("\n".join(out) + "\n")
sys.exit(1 if MUTATE else 0)
