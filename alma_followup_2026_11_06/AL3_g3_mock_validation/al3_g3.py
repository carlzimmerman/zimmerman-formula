"""AL3: the filed AC1 addendum G3 (ADDENDUM_G3_2026-11-06.md) applied in-process to the frozen scorer. Criteria FROZEN_CRITERIA.md (6dce9813a6).

install(S) replaces cfg942_common.fit_disc (main fits only; calls with an I0 argument, the C1 injection, keep the frozen fitter) and wraps
ac1_score.g1_3d to record the G1-3D flux-weighted velocity centroid. No frozen file is edited. kappa = 1/2 FITTED; not theory closed."""
import math
import numpy as np

STATE = dict(on=False, vsys_centroid=None, log=[])
DPA = (0.0, 45.0, -45.0, 90.0, -90.0, 180.0); DVS = (-100.0, -50.0, 0.0, 50.0, 100.0)


def rho1(box, vcont):
    """AL2 R4's measurement: continuum channels |v| > vcont, pixels at r > 2", every 97th pixel, lag-1 autocorrelation."""
    v_all = box["v"]; cont = np.abs(v_all) > vcont; dc = np.nan_to_num(box["data"][cont]); yy, xx = np.indices(dc.shape[1:])
    rr = np.hypot(xx - box["xc"], yy - box["yc"]) * box["pix"]; sp = dc[:, rr > 2.0][:, ::97].astype(np.float64); sp = sp - sp.mean(axis=0)
    return float(np.sum(sp[1:] * sp[:-1]) / np.sum(sp * sp)) if sp.shape[0] > 2 else float("nan")


def install(S):
    C = S.C; frozen_fit = C.fit_disc; frozen_g1 = S.g1_3d

    def g1_wrap(box, rng, vcen=0.0, n=200):
        g3, mk3, b = frozen_g1(box, rng, vcen, n); vc = float("nan")
        if g3["nvox"]:   # the same lines measure() uses for z_line of G1-3D; v = c (z_line - z)/(1 + z) is this mean
            d = np.nan_to_num(box["data"][:, :mk3.shape[1] * b, :mk3.shape[2] * b])
            if b > 1: d = d.reshape(box["data"].shape[0], mk3.shape[1], b, mk3.shape[2], b).mean(axis=(2, 4))
            sp3 = np.clip(d * mk3, 0, None).sum(axis=(1, 2))
            if sp3.sum() > 0: vc = float((sp3 * box["v"]).sum() / sp3.sum())
        STATE["vsys_centroid"] = vc
        return g3, mk3, b

    def g3_fit(box, inc, kpa, sig_vox, centre, pa0, vsys0, vf0, h0, R_kpc, Rd_kpc, rfit=1.4, vfit=600.0, I0=None):
        if not STATE["on"] or I0 is not None:
            return frozen_fit(box, inc, kpa, sig_vox, centre, pa0, vsys0, vf0, h0, R_kpc, Rd_kpc, rfit=rfit, vfit=vfit, I0=I0)
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
        def M1(p):
            q = np.array(p, float); q[7] = 1.0; return (C.disc_model(q, X, Y, vv, dv, inc, kpa, kf)[:, circ] / sig_vox).ravel()
        # ---- rule 2: vsys start from the G1-3D centroid ----
        vc = STATE["vsys_centroid"]; vc_ok = vc is not None and np.isfinite(vc); vcen = vc if vc_ok else vsys0
        # ---- rule 3: fixed grid, analytic amplitude ----
        grid = []
        for dvs in DVS:
            for dpa in DPA:
                p = np.array([centre[0], centre[1], pa0 + math.radians(dpa), vcen + dvs, vf0, 1.0, 40.0, 1.0, h0]); p = np.clip(p, lo + 1e-6, hi - 1e-6)
                m = M1(p); mm = float(np.dot(m, m)); a = max(float(np.dot(m, Dn)) / mm if mm > 0 else 0.0, 1e-6 * I0f)
                r_ = a * m - Dn; grid.append((float(np.dot(r_, r_)), dvs, dpa, a, p))
        cg, dvs_b, dpa_b, I0s, pg = min(grid, key=lambda t: t[0])
        # ---- rule 1: u = ln I0 ----
        lou, hiu = lo.copy(), hi.copy(); lou[7], hiu[7] = math.log(1e-4 * I0s), math.log(1e3 * I0s)
        p0u = pg.copy(); p0u[7] = math.log(I0s); p0u = np.clip(p0u, lou + 1e-6, hiu - 1e-6)
        def res(q):
            p = np.array(q, float); p[7] = math.exp(q[7]); return (C.disc_model(p, X, Y, vv, dv, inc, kpa, kf)[:, circ] - D).ravel() / sig_vox
        xu, covu, chi2, nfev, nvox, status = C.lm_fit(res, p0u, lou, hiu)
        x = xu.copy(); x[7] = math.exp(xu[7]); cov = np.array(covu, float); cov[7, :] *= x[7]; cov[:, 7] *= x[7]
        # ---- rules 5, 6 ----
        r1 = rho1(box, 600.0); fac = 1.0 + 2.0 * r1; cov = cov * fac
        dchi2 = chi2_empty - chi2; thr = 25.0 / fac; thr_strict = 25.0 * fac; adequate = bool(dchi2 >= thr)
        if not adequate: cov = np.full_like(cov, np.nan)
        bp = C.beam_pix(box["beam"], pix)
        out = dict(params=x.tolist(), names=["x0", "y0", "pa", "vsys", "vf", "rt_kpc", "s0", "I0", "h_arcsec"], chi2=chi2, nvox=nvox, nfev=nfev, status=status, inc=inc)
        out.update({k: v_ for k, v_ in C.vc_from_params(x, cov, R_kpc, Rd_kpc).items()})
        vb = C.vc_from_params(x, cov * bp, R_kpc, Rd_kpc); out.update({k + "_beamcorr": vb[k] for k in ("eVrot", "eVc_PB", "eVc_P0")}); out["cov"] = cov.tolist()
        g = dict(inc=inc, vf0=vf0, vsys_frozen_start=vsys0, vsys_centroid=vc if vc_ok else None, centroid_used=bool(vc_ok), grid_cost=cg, grid_dvsys=dvs_b,
                 grid_dpa=dpa_b, I0_star=I0s, I0_frozen_start=I0f, I0_final=x[7], u_final=float(xu[7]), u_at_bound=bool(xu[7] <= lou[7] + 1e-3 or xu[7] >= hiu[7] - 1e-3),
                 u_near_zero=bool(abs(xu[7]) < 0.05), chi2=chi2, chi2_empty=chi2_empty, dchi2=dchi2, rho1=r1, thr_filed=thr, adequate=adequate,
                 would_pass_strict=bool(dchi2 >= thr_strict), thr_strict=thr_strict, status=status, nfev=nfev, params=x.tolist())
        out["g3"] = g; STATE["log"].append(g)
        return out

    C.fit_disc = g3_fit; S.g1_3d = g1_wrap
    return frozen_fit
