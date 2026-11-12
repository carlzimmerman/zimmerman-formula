"""EUC5R spectral fitter (A1.2 as read in READING.md), F1 mock gate, DESI fits, F3, SLACS real-spectra scale.

Stages (run from the repo root):
  python .../euc5r_fit.py f1      -> euc5r_f1.json   (gate)
  python .../euc5r_fit.py desi    -> euc5r_desi_fits.csv
  python .../euc5r_fit.py slacs   -> euc5r_slacs_fits.csv, euc5r_slacs_scale.json   (needs desi fits + P list)
"""
import glob, json, math, os, sys, time, warnings
import numpy as np
import pandas as pd
from astropy.io import fits
warnings.filterwarnings("ignore")
from ppxf.ppxf import ppxf
import ppxf.ppxf_util as util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import euc5r_data as D

C = 299792.458
FWHM_TPL = 2.51
SIG_TPL_A = FWHM_TPL / 2.354820045
TPL_DIR = "_external_data/lam9_emiles_bi_basti/fits"
LINES = [3727.09, 3729.88, 3869.86, 4102.89, 4341.69, 4862.68, 4960.30, 5008.24]
SKY = [(5570, 5590), (6290, 6310), (6860, 6960), (7590, 7700)]
SEED = 20261112

# ------------------------------------------------------------------ templates
_TPL = {}


def templates():
    if "all" not in _TPL:
        files = sorted(glob.glob(f"{TPL_DIR}/Ebi1.30Z*T*_iTp0.00_baseFe.fits"))
        assert len(files) == 84, len(files)
        lam = None
        arr = []
        for f in files:
            h = fits.open(f)
            hd = h[0].header
            y = h[0].data.astype(float)
            if lam is None:
                lam = hd["CRVAL1"] + hd["CDELT1"] * np.arange(hd["NAXIS1"])
            arr.append(y)
        arr = np.array(arr).T
        cut = (lam >= 3300) & (lam <= 6100)
        _TPL["all"] = (lam[cut], arr[cut], [os.path.basename(f) for f in files])
    return _TPL["all"]


def one_template(name):
    lam, arr, names = templates()
    return lam, arr[:, names.index(name)]


# ------------------------------------------------------------------ spectra
def load(path, kind):
    d = np.load(path, allow_pickle=True)
    w = d["wavelength"].astype(float)
    f = d["flux"].astype(float)
    iv = d["ivar"].astype(float)
    mask = d["mask"].astype(int) if "mask" in d.files else np.zeros(len(w), int)
    ws = d["wave_sigma"].astype(float)
    if kind == "sdss":
        ws = ws * np.gradient(w)        # pixels -> Angstrom (READING section 2.4)
    return dict(w=w, f=f, iv=iv, mask=mask, ws=ws)


def window(spec, z):
    w = spec["w"]
    sel = (w >= 3650) & (w <= 9700) & (w / (1 + z) >= 3750) & (w / (1 + z) <= 5600)
    good = sel & (spec["iv"] > 0) & (spec["mask"] == 0)
    return sel, good


def snr(spec, z):
    sel, good = window(spec, z)
    if good.sum() < 10:
        return float("nan"), float("nan")
    s = float(np.median(spec["f"][good] * np.sqrt(spec["iv"][good])))
    dl = float(np.median(np.gradient(spec["w"])[sel])) / (1 + z)
    return s, s / math.sqrt(dl)          # per pixel, per rest-frame Angstrom


def fit(spec, z, return_pp=False):
    sel, good0 = window(spec, z)
    idx = np.where(sel)[0]
    if len(idx) < 50:
        return dict(status="no_window")
    i0, i1 = idx[0], idx[-1] + 1
    w = spec["w"][i0:i1]
    f = spec["f"][i0:i1].copy()
    iv = spec["iv"][i0:i1]
    bad = ~((iv > 0) & (spec["mask"][i0:i1] == 0))
    if (~bad).sum() < 50:
        return dict(status="no_good")
    f[bad] = np.interp(w[bad], w[~bad], f[~bad])
    sig = np.where(bad, 0.0, 1.0 / np.sqrt(np.where(iv > 0, iv, 1.0)))
    sig[bad] = np.interp(w[bad], w[~bad], sig[~bad])
    lam = w / (1 + z)
    gal, ln_lam, velscale = util.log_rebin(lam, f)
    badr, _, _ = util.log_rebin(lam, bad.astype(float))
    noise = np.interp(ln_lam, np.log(lam), sig)
    velscale = float(np.atleast_1d(velscale)[0])
    norm = np.median(gal[badr == 0]) if np.any(badr == 0) else 1.0
    if not np.isfinite(norm) or norm <= 0:
        norm = np.median(np.abs(gal)) + 1e-30
    gal, noise = gal / norm, noise / norm
    lt, tarr, _ = templates()
    tpl, ln_lt, _ = util.log_rebin(lt, tarr, velscale=velscale)
    tpl = tpl / np.median(tpl)
    lr = np.exp(ln_lam)
    gp = (badr == 0)
    for L in LINES:
        gp &= np.abs(lr - L) > 10.0
    lo = lr * (1 + z)
    for a, b in SKY:
        gp &= ~((lo >= a) & (lo <= b))
    gp &= np.isfinite(gal) & np.isfinite(noise) & (noise > 0)
    gpi = np.where(gp)[0]
    if len(gpi) < 100:
        return dict(status="few_pixels", npix=int(len(gpi)))
    kw = dict(moments=2, degree=8, mdegree=0, lam=lr, lam_temp=np.exp(ln_lt), quiet=True)
    pp = ppxf(tpl, gal, noise, velscale, [0.0, 200.0], goodpixels=gpi, **kw)
    res = (gal - pp.bestfit) / noise
    gpi2 = gpi[np.abs(res[gpi]) <= 3.0]
    pp = ppxf(tpl, gal, noise, velscale, list(pp.sol[:2]), goodpixels=gpi2, **kw)
    V, sfit = float(pp.sol[0]), float(pp.sol[1])
    chi2 = float(pp.chi2)
    efit = float(pp.error[1]) * math.sqrt(max(chi2, 1.0))
    lmean = float(np.mean(lr[gpi2]))
    s_tpl = SIG_TPL_A / lmean * C
    s_inst = float(np.interp(lmean * (1 + z), spec["w"], spec["ws"])) / (1 + z) / lmean * C
    s2 = sfit ** 2 + s_tpl ** 2 - s_inst ** 2
    sigma = math.sqrt(s2) if s2 > 0 else 0.0
    esig = efit * sfit / sigma if sigma > 0 else float("inf")
    out = dict(status="ok", V=V, sigma_fit=sfit, sigma=sigma, err_fit=efit, err=esig, chi2=chi2,
               npix=int(len(gpi2)), npix_preclip=int(len(gpi)), lmean=lmean, s_tpl=s_tpl, s_inst=s_inst,
               velscale=velscale)
    if return_pp:
        out["pp"] = pp
    return out


def quality(r):
    if r.get("status") != "ok":
        return False
    return (70 <= r["sigma"] <= 500) and (r["err"] / r["sigma"] <= 0.25) and abs(r["V"]) <= 300 and r["npix"] >= 800


# ------------------------------------------------------------------ F1 mock gate
def mock_spec(real, z, sigma_in, mode, tname, rng):
    lt, T = one_template(tname)
    w = real["w"]
    if mode == "gate":
        si = np.interp(lt * (1 + z), w, real["ws"]) / (1 + z)
        wid2 = (sigma_in / C * lt) ** 2 + si ** 2 - SIG_TPL_A ** 2
        Tb = util.varsmooth(lt, T, np.sqrt(np.maximum(wid2, 0)), xout=lt, oversample=2)
    else:   # literal: template broadened by sigma_in in velocity only
        Tb = util.varsmooth(lt, T, sigma_in / C * lt, xout=lt, oversample=2)
    mf = np.interp(w / (1 + z), lt, Tb, left=0, right=0)
    sel, good = window(real, z)
    med_real = np.median(real["f"][good])
    scale = med_real / np.median(mf[sel])
    sig = np.where(real["iv"] > 0, 1.0 / np.sqrt(np.where(real["iv"] > 0, real["iv"], 1)), 0)
    f = mf * scale + rng.normal(size=len(w)) * sig
    return dict(w=w, f=f, iv=real["iv"].copy(), mask=real["mask"].copy(), ws=real["ws"]), float(med_real)


def stage_f1():
    cat = D.samples()
    sl = D.spectra_list(cat)
    fl = sl[(sl.kind == "flagged") & sl.specprimary].copy()
    s = []
    for _, r in fl.iterrows():
        sp = load(f"{D.DESI_DIR}/{r.sparcl_id}.npz", "desi")
        s.append(snr(sp, r.z_def)[0])
    fl["snr"] = s
    fl = fl[np.isfinite(fl.snr)].sort_values("snr").reset_index(drop=True)
    k = (len(fl) - 1) // 2
    ref = fl.iloc[k]
    real = load(f"{D.DESI_DIR}/{ref.sparcl_id}.npz", "desi")
    print(f"F1 reference spectrum: index {k} of {len(fl)} flagged primaries, S/N per pixel {ref.snr:.3f}")
    rng = np.random.default_rng(SEED)
    out = dict(ref_sparcl_id=ref.sparcl_id, ref_snr_pix=float(ref.snr), n_flagged_primary=len(fl), runs={})
    plan = [("gate", "Ebi1.30Zp0.06T10.0000_iTp0.00_baseFe.fits", 40),
            ("literal", "Ebi1.30Zp0.06T10.0000_iTp0.00_baseFe.fits", 20),
            ("mismatch", "Ebi1.30Zm0.35T05.0000_iTp0.00_baseFe.fits", 20)]
    gate_ok = True
    for mode, tn, nreal in plan:
        for sin in (150.0, 250.0, 350.0):
            vals, efs, qual = [], [], 0
            for i in range(nreal):
                m, _ = mock_spec(real, 0.45, sin, "literal" if mode == "literal" else "gate", tn, rng)
                r = fit(m, 0.45)
                if r["status"] == "ok":
                    vals.append(r["sigma"])
                    efs.append(r["err"])
                    qual += quality(r)
            med = float(np.median(vals))
            truth = sin if mode != "literal" else math.sqrt(sin ** 2 + r["s_tpl"] ** 2 - r["s_inst"] ** 2)
            rec = dict(sigma_in=sin, n=len(vals), median=med, ratio_to_sigma_in=med / sin, truth=truth,
                       ratio_to_truth=med / truth, scatter=float(np.std(vals)), median_err=float(np.median(efs)),
                       n_quality=int(qual))
            out["runs"][f"{mode}_{int(sin)}"] = rec
            print(f"  {mode:9s} sigma_in {sin:5.0f}: median {med:7.2f}  /in {med/sin:.4f}  /truth {med/truth:.4f}"
                  f"  scatter {np.std(vals):6.2f}  med err {np.median(efs):6.2f}  quality {qual}/{len(vals)}", flush=True)
            if mode == "gate" and abs(med / sin - 1) > 0.05:
                gate_ok = False
    out["F1_gate_pass"] = gate_ok
    print("F1 gate:", "PASS" if gate_ok else "FAIL")
    json.dump(out, open(f"{HERE}/euc5r_f1.json", "w"), indent=1)


def stage_f1diag():
    """POST-GATE DIAGNOSTIC (written after F1 failed; cannot change any word): the same gate mock with the
    reference spectrum's noise divided by 2, 4 and 10, to show whether the failure is noise (fitter sane at high
    S/N) or a bug.  20 realisations each."""
    f1 = json.load(open(f"{HERE}/euc5r_f1.json"))
    real = load(f"{D.DESI_DIR}/{f1['ref_sparcl_id']}.npz", "desi")
    rng = np.random.default_rng(SEED + 1)
    out = {}
    for k in (2.0, 4.0, 10.0):
        r2 = dict(real)
        r2["iv"] = real["iv"] * k * k
        for sin in (150.0, 250.0, 350.0):
            vals, q = [], 0
            for i in range(20):
                m, _ = mock_spec(r2, 0.45, sin, "gate", "Ebi1.30Zp0.06T10.0000_iTp0.00_baseFe.fits", rng)
                r = fit(m, 0.45)
                if r["status"] == "ok":
                    vals.append(r["sigma"])
                    q += quality(r)
            med = float(np.median(vals))
            out[f"snrx{int(k)}_{int(sin)}"] = dict(median=med, ratio=med / sin, scatter=float(np.std(vals)), n_quality=q)
            print(f"  S/N x{k:4.1f} sigma_in {sin:5.0f}: median {med:7.2f} ratio {med/sin:.4f} scatter {np.std(vals):6.2f}"
                  f" quality {q}/20", flush=True)
    json.dump(out, open(f"{HERE}/euc5r_f1diag.json", "w"), indent=1)


def stage_f1s():
    """AMENDMENT F1S (post hoc, committed alone before this ran): F1 with the noise scaled so that the mock's median
    S/N per pixel in the fit window equals the reference spectrum's own (euc5r_f1.json ref_snr_pix)."""
    f1 = json.load(open(f"{HERE}/euc5r_f1.json"))
    real = load(f"{D.DESI_DIR}/{f1['ref_sparcl_id']}.npz", "desi")
    target = f1["ref_snr_pix"]
    tn = "Ebi1.30Zp0.06T10.0000_iTp0.00_baseFe.fits"
    rng = np.random.default_rng(SEED + 2)
    out = dict(target_snr_pix=target, runs={})
    ok_all = True
    for sin in (150.0, 250.0, 350.0):
        r0 = dict(real)
        r0["iv"] = real["iv"]
        noiseless, _ = mock_spec(r0, 0.45, sin, "gate", tn, np.random.default_rng(0))
        # deterministic part: rebuild without noise
        lt, T = one_template(tn)
        si = np.interp(lt * 1.45, real["w"], real["ws"]) / 1.45
        Tb = util.varsmooth(lt, T, np.sqrt(np.maximum((sin / C * lt) ** 2 + si ** 2 - SIG_TPL_A ** 2, 0)), xout=lt, oversample=2)
        mf = np.interp(real["w"] / 1.45, lt, Tb, left=0, right=0)
        sel, good = window(real, 0.45)
        mf = mf * np.median(real["f"][good]) / np.median(mf[sel])
        sn_now = float(np.median(mf[good] * np.sqrt(real["iv"][good])))
        k = sn_now / target
        r2 = dict(real)
        r2["iv"] = real["iv"] / k ** 2
        vals, q = [], 0
        for i in range(40):
            m, _ = mock_spec(r2, 0.45, sin, "gate", tn, rng)
            r = fit(m, 0.45)
            if r["status"] == "ok":
                vals.append(r["sigma"])
                q += quality(r)
        med = float(np.median(vals))
        out["runs"][str(int(sin))] = dict(sn_before=sn_now, noise_factor=k, median=med, ratio=med / sin,
                                         scatter=float(np.std(vals)), n_quality=q, n=len(vals))
        ok_all &= abs(med / sin - 1) <= 0.05
        print(f"  F1S sigma_in {sin:5.0f}: S/N {sn_now:.3f} -> {target:.3f} (noise x{k:.3f}); median {med:7.2f}"
              f" ratio {med/sin:.4f} scatter {np.std(vals):6.2f} quality {q}/{len(vals)}", flush=True)
    out["F1S_pass"] = bool(ok_all)
    print("F1S:", "PASS" if ok_all else "FAIL")
    json.dump(out, open(f"{HERE}/euc5r_f1s.json", "w"), indent=1)


# ------------------------------------------------------------------ DESI fits
def stage_desi():
    cat = D.samples()
    sl = D.spectra_list(cat)
    sl = sl[sl.in_S].reset_index(drop=True)
    rows = []
    t0 = time.time()
    for i, r in sl.iterrows():
        p = f"{D.DESI_DIR}/{r.sparcl_id}.npz"
        if not os.path.exists(p):
            rows.append(dict(r, status="missing"))
            continue
        sp = load(p, "desi")
        sn, snA = snr(sp, r.z_def)
        res = fit(sp, r.z_def)
        res.pop("pp", None)
        row = dict(r)
        row.update(res)
        row["snr_pix"], row["snr_restA"] = sn, snA
        row["quality"] = quality(res)
        rows.append(row)
        print(f"  {i+1:3d}/{len(sl)} {r.unique_identifier} P={r.in_P} prim={r.specprimary} z={r.z_def:.4f} "
              f"S/N={sn:6.2f} -> {res.get('status')} sigma={res.get('sigma', float('nan')):7.1f} "
              f"err={res.get('err', float('nan')):6.1f} V={res.get('V', float('nan')):7.1f} q={row['quality']} "
              f"[{time.time()-t0:.0f}s]", flush=True)
    pd.DataFrame(rows).to_csv(f"{HERE}/euc5r_desi_fits.csv", index=False)


# ------------------------------------------------------------------ SLACS real-spectra scale
def chosen_desi(df):
    """one spectrum per lens: the primary, else the one with the smaller fitted error."""
    out = []
    for u, g in df.groupby("unique_identifier"):
        pr = g[g.specprimary]
        if len(pr):
            out.append(pr.iloc[0])
        else:
            gg = g[g.status == "ok"]
            out.append((gg if len(gg) else g).sort_values("err").iloc[0])
    return pd.DataFrame(out)


def stage_slacs():
    sys.path.insert(0, HERE)
    from euc5r_checks import load_slacs
    df = pd.read_csv(f"{HERE}/euc5r_desi_fits.csv")
    ch = chosen_desi(df)
    gP = ch[ch.in_P & ch.quality.astype(bool)]
    target = float(np.median(gP.snr_restA))
    print(f"DESI target S/N per rest-frame Angstrom (median over {len(gP)} graded P spectra): {target:.3f}")
    tab = {d["name"]: d for d in load_slacs()}
    rng = np.random.default_rng(SEED)
    rows = []
    for p in sorted(glob.glob(f"{D.SLACS_DIR}/*.npz")):
        name = os.path.basename(p)[:-4]
        d = tab[name]
        sp = load(p, "sdss")
        z = d["zl"]
        sn, snA = snr(sp, z)
        a = fit(sp, z)
        a.pop("pp", None)
        row = dict(name=name, z=z, sig_slacs=d["sig"], esig_slacs=d["esig"], snr_pix=sn, snr_restA=snA,
                   nat_status=a.get("status"), nat_sigma=a.get("sigma"), nat_err=a.get("err"), nat_V=a.get("V"),
                   nat_q=quality(a), nat_chi2=a.get("chi2"))
        fac = snA / target
        row["degrade_factor"] = fac
        row["already_noisier"] = bool(fac <= 1)
        vals, qs = [], []
        for k in range(5):
            if fac > 1:
                sig = np.where(sp["iv"] > 0, 1 / np.sqrt(np.where(sp["iv"] > 0, sp["iv"], 1)), 0)
                add = sig * math.sqrt(fac ** 2 - 1)
                s2 = dict(sp)
                s2["f"] = sp["f"] + rng.normal(size=len(sp["f"])) * add
                s2["iv"] = np.where(sp["iv"] > 0, sp["iv"] / fac ** 2, 0)
            else:
                s2 = sp
            b = fit(s2, z)
            vals.append(b.get("sigma", np.nan) if b.get("status") == "ok" else np.nan)
            qs.append(quality(b))
            if fac <= 1:
                break
        row["deg_sigma"] = float(np.nanmedian(vals))
        row["deg_q_frac"] = float(np.mean(qs))
        row["deg_q"] = bool(np.mean(qs) >= 0.5)
        rows.append(row)
        print(f"  {name} z={z:.3f} S/N/A={snA:6.2f} fac={fac:5.2f} sig_SLACS={d['sig']:.0f}  native={row['nat_sigma']:.1f}"
              f" (q={row['nat_q']})  degraded={row['deg_sigma']:.1f} (qfrac={row['deg_q_frac']:.1f})", flush=True)
    t = pd.DataFrame(rows)
    t.to_csv(f"{HERE}/euc5r_slacs_fits.csv", index=False)
    rng2 = np.random.default_rng(SEED)
    res = dict(target_snr_restA=target, n_graded_P=int(len(gP)))
    for case, col, q in (("degraded", "deg_sigma", "deg_q"), ("native", "nat_sigma", "nat_q")):
        u = t[t[q].astype(bool)]
        r = (u[col] / u.sig_slacs).values
        bs = np.array([np.median(rng2.choice(r, len(r))) for _ in range(2000)])
        res[case] = dict(N=int(len(r)), s=float(np.median(r)), lo=float(np.percentile(bs, 2.5)),
                         hi=float(np.percentile(bs, 97.5)), mean=float(np.mean(r)), scatter=float(np.std(r)))
        print(f"scale {case}: N={len(r)} s={np.median(r):.4f} [{res[case]['lo']:.4f}, {res[case]['hi']:.4f}]"
              f" mean {np.mean(r):.4f} sd {np.std(r):.4f}")
    json.dump(res, open(f"{HERE}/euc5r_slacs_scale.json", "w"), indent=1)


if __name__ == "__main__":
    {"f1": stage_f1, "f1diag": stage_f1diag, "f1s": stage_f1s, "desi": stage_desi, "slacs": stage_slacs}[sys.argv[1]]()
