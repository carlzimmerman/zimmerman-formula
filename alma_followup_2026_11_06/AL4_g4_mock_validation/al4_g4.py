"""AL4: the filed AC1 addendum G4 (ADDENDUM_G4_2026-11-06.md, filed 8ff85f806e) applied in-process to the frozen scorer.
Criteria FROZEN_CRITERIA.md (31e5110862 / origin 8551af59dd).

install(S) replaces cfg942_common.fit_disc for main fits only. Calls carrying an I0 argument (the C1 injection) keep the frozen
fitter. It also wraps ac1_score.g1_3d to record the G1-3D flux-weighted velocity centroid (the same lines as AL3's al3_g3.py).
STATE["mode"] is "frozen", "g4" or "g4lin" (rule 1 off: linear I0, bound 0). No frozen or AL3 file is edited.
MOCK only. kappa = 1/2 FITTED; one disc excludes no model; not theory closed."""
import math
import numpy as np

STATE = dict(mode="frozen", vsys_centroid=None, log=[], rho1_cache={})


def rho1_g4(box):
    """G4 rule 6: every box channel (|v| <= 650), all pixels at r > 2", each pixel's spectrum mean-subtracted, pooled lag-1."""
    key = id(box["data"])
    if key in STATE["rho1_cache"]: return STATE["rho1_cache"][key]
    d = np.nan_to_num(box["data"]); yy, xx = np.indices(d.shape[1:]); rr = np.hypot(xx - box["xc"], yy - box["yc"]) * box["pix"]
    sp = d[:, rr > 2.0].astype(np.float64); sp = sp - sp.mean(axis=0)
    r = float(np.sum(sp[1:] * sp[:-1]) / np.sum(sp * sp)) if sp.shape[0] > 2 else float("nan")
    STATE["rho1_cache"] = {key: r}; return r


def install(S):
    C = S.C; frozen_fit = C.fit_disc; frozen_g1 = S.g1_3d

    def g1_wrap(box, rng, vcen=0.0, n=200):
        g3, mk3, b = frozen_g1(box, rng, vcen, n); vc = float("nan")
        if g3["nvox"]:
            d = np.nan_to_num(box["data"][:, :mk3.shape[1] * b, :mk3.shape[2] * b])
            if b > 1: d = d.reshape(box["data"].shape[0], mk3.shape[1], b, mk3.shape[2], b).mean(axis=(2, 4))
            sp3 = np.clip(d * mk3, 0, None).sum(axis=(1, 2))
            if sp3.sum() > 0: vc = float((sp3 * box["v"]).sum() / sp3.sum())
        STATE["vsys_centroid"] = vc
        return g3, mk3, b

    def g4_fit(box, inc, kpa, sig_vox, centre, pa0, vsys0, vf0, h0, R_kpc, Rd_kpc, rfit=1.4, vfit=600.0, I0=None):
        mode = STATE["mode"]
        if mode == "frozen" or I0 is not None:
            out = frozen_fit(box, inc, kpa, sig_vox, centre, pa0, vsys0, vf0, h0, R_kpc, Rd_kpc, rfit=rfit, vfit=vfit, I0=I0)
            if I0 is None: STATE["log"].append(dict(mode="frozen", inc=inc, vf0=vf0, I0_final=out["params"][7], chi2=out["chi2"]))
            return out
        # ---- fit_disc's own set-up, unchanged ----
        v = box["v"]; sel_v = np.abs(v) <= vfit; data = box["data"][sel_v]; vv = v[sel_v]; dv = box["dv"]; pix = box["pix"]
        ny, nx = data.shape[1:]; hp = int(math.ceil(rfit / pix)) + 4; xc, yc = box["xc"], box["yc"]
        x0i, x1i = max(0, int(xc) - hp), min(nx, int(xc) + hp + 1); y0i, y1i = max(0, int(yc) - hp), min(ny, int(yc) + hp + 1)
        sub = np.nan_to_num(data[:, y0i:y1i, x0i:x1i].astype(np.float64))
        yy, xx = np.indices(sub.shape[1:]); X, Y = (xx - (xc - x0i)) * pix, (yy - (yc - y0i)) * pix
        circ = np.hypot(X, Y) <= rfit; kf = C.kernel_rfft(sub.shape[1:], box["beam"], pix)
        I0f = max(float(np.nanmax(np.nansum(sub, axis=0)) * dv), 1e-12)
        lo = np.array([-0.5, -0.5, pa0 - math.pi, -400, 10, 0.05, 3.0, 0.0, 0.01]); hi = np.array([0.5, 0.5, pa0 + math.pi, 400, 800, 15.0, 250, np.inf, 3.0])
        D = sub[:, circ]; Dn = (D / sig_vox).ravel(); chi2_empty = float(np.sum(Dn * Dn))
        # ---- rule 2 ----
        vc = STATE["vsys_centroid"]; vc_ok = vc is not None and np.isfinite(vc); vcen = vc if vc_ok else vsys0
        # ---- rule 3: the frozen start with vsys from rule 2; analytic amplitude there; no grid ----
        p = np.array([centre[0], centre[1], pa0, vcen, vf0, 1.0, 40.0, 1.0, h0]); p = np.clip(p, lo + 1e-6, hi - 1e-6); p[7] = 1.0
        m1 = (C.disc_model(p, X, Y, vv, dv, inc, kpa, kf)[:, circ] / sig_vox).ravel(); mm = float(np.dot(m1, m1))
        I0s = max(float(np.dot(m1, Dn)) / mm if mm > 0 else 0.0, 1e-6 * I0f)
        if mode == "g4":   # ---- rule 1: u = ln I0 ----
            lou, hiu = lo.copy(), hi.copy(); lou[7], hiu[7] = math.log(1e-4 * I0s), math.log(1e3 * I0s)
            p0u = p.copy(); p0u[7] = math.log(I0s); p0u = np.clip(p0u, lou + 1e-6, hiu - 1e-6)
            def res(q):
                pp = np.array(q, float); pp[7] = math.exp(q[7]); return (C.disc_model(pp, X, Y, vv, dv, inc, kpa, kf)[:, circ] - D).ravel() / sig_vox
            xu, covu, chi2, nfev, nvox, status = C.lm_fit(res, p0u, lou, hiu)
            x = xu.copy(); x[7] = math.exp(xu[7]); cov = np.array(covu, float); cov[7, :] *= x[7]; cov[:, 7] *= x[7]; uf = float(xu[7])
        else:              # ---- g4lin: rule 1 off (linear I0, bound 0), everything else G4 ----
            p0 = p.copy(); p0[7] = I0s; p0 = np.clip(p0, lo + 1e-6, hi - 1e-6)
            def res(q): return (C.disc_model(q, X, Y, vv, dv, inc, kpa, kf)[:, circ] - D).ravel() / sig_vox
            x, cov, chi2, nfev, nvox, status = C.lm_fit(res, p0, lo, hi); cov = np.array(cov, float); uf = None
        # ---- rules 5, 6 ----
        r1 = rho1_g4(box); fac = 1.0 + 2.0 * max(r1, 0.0) if np.isfinite(r1) else 1.0; cov = cov * fac
        dchi2 = chi2_empty - chi2; thr = 25.0 * fac; adequate = bool(dchi2 >= thr)
        if not adequate: cov = np.full_like(cov, np.nan)
        bp = C.beam_pix(box["beam"], pix)
        out = dict(params=list(map(float, x)), names=["x0", "y0", "pa", "vsys", "vf", "rt_kpc", "s0", "I0", "h_arcsec"], chi2=chi2, nvox=nvox, nfev=nfev, status=status, inc=inc)
        out.update({k: v_ for k, v_ in C.vc_from_params(x, cov, R_kpc, Rd_kpc).items()})
        vb = C.vc_from_params(x, cov * bp, R_kpc, Rd_kpc); out.update({k + "_beamcorr": vb[k] for k in ("eVrot", "eVc_PB", "eVc_P0")}); out["cov"] = cov.tolist()
        g = dict(mode=mode, inc=inc, vf0=vf0, vsys_frozen_start=vsys0, vsys_centroid=vc if vc_ok else None, centroid_used=bool(vc_ok), I0_star=I0s,
                 I0_frozen_start=I0f, I0_final=float(x[7]), u_final=uf, chi2=chi2, chi2_empty=chi2_empty, dchi2=dchi2, rho1=r1, thr=thr,
                 adequate=adequate, status=status, nfev=nfev, params=list(map(float, x)))
        out["g4"] = g; STATE["log"].append(g)
        return out

    C.fit_disc = g4_fit; S.g1_3d = g1_wrap
    return frozen_fit
