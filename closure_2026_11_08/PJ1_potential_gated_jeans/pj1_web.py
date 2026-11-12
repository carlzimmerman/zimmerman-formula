"""PJ1 gates G8 and G9 (FROZEN_CRITERIA.md e3c9bc7d3c) on the linear web.
G8: QX3 iter2's growth ODE (BG1's form) with the component's clustered weight W(k, a) = S(Phi_lin(k, a))/R / (1 + (k R_J(Phi)/a)^4)
    (per-mode linear potential by Poisson from CLASS's P_lin on the footing background; R_J a proper length), GL1's corrected Limber
    kernel on raw PR4 lensing (Delta chi^2 <= 4) and CE2's fsigma8 ratio against DESI DR1 (within 2 sigma, QX3/BG1 rule).
G9: NC2 G3's forest machinery (DESI DR1 P1D table + covariance, read-only loader copy): the ratio r = P1D_PJ1 / P1D_uniform of the linear
    1D power with P_PJ1 = P_lin x (delta_m,PJ1/delta_m,ref)^2 from the same growth solve; Delta chi^2_Asimov <= 4 PASS, 4-25 TENSION, > 25 FAIL.
Reported: the total-potential reading (S = S(sigma_Phi) with QX7 iter_1's large-scale sigma_Phi 4.5e-5, cutoff at R_J(sigma_Phi)).
kappa = 1/2 FITTED; not theory closed; footings never pooled."""
import os, sys, json, math, time, tarfile, io, hashlib
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.linalg import cho_factor, cho_solve
import pj1 as J
P = J.P
SIGMA_PHI_LSS = 4.5e-5   # QX7 iter_1 (k_min = H0/c), reported reading only
DESI = [("BGS", 0.295, 0.80, 0.20, 0.20, 0.84, 0.19, 0.19), ("LRG1", 0.510, 1.09, 0.12, 0.14, 1.16, 0.13, 0.13),
        ("LRG2", 0.706, 1.05, 0.12, 0.12, 1.04, 0.11, 0.092), ("LRG3", 0.919, 0.96, 0.11, 0.10, 0.997, 0.10, 0.084)]   # DESI DR1 Table 9 as CE2 / BG1 transcribed it

def run_web(RES):
    Q3 = J.load_prefix(os.path.join(J.CL6, "QX3_cmb_growth", "iter2_kq_dust", "iter2.py"), 'if __name__ == "__main__":', "qx3_iter2_lib")
    Class, LMAX, ZPK = Q3["Class"], Q3["LMAX"], Q3["ZPK"]
    Q15 = json.load(open(os.path.join(J.CL6, "QX15_cmb_primary_likelihood", "qx15.json")))
    THETA = {f: dict(Q15["footings"][f]["main"]["theta"], h=Q15["footings"][f]["main"]["h"]) for f in J.FOOTS}
    KG = np.logspace(-4, math.log10(200.0), 100); ZG = np.linspace(0.02, ZPK, 120)
    # ---------------- NC2 G3 forest data (loader copy, read-only)
    RAW = os.path.join(J.REPO, "_external_data", "desi_dr1_p1d_qmle", "raw", "data_points.tar")
    from astropy.io import fits
    md5 = hashlib.md5()
    with open(RAW, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 22), b""): md5.update(blk)
    MD5 = md5.hexdigest()
    with tarfile.open(RAW) as tf: HD = fits.open(io.BytesIO(tf.extractfile("desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits").read()))
    T = HD["P1D_BLIND"].data; Zall, Kall, Pall = np.asarray(T["Z"], float), np.asarray(T["K"], float), np.asarray(T["PLYA"], float); C_full = np.asarray(HD["COVARIANCE"].data, float)
    ZB = np.round(np.unique(Zall), 2); CLIGHT, LLYA, DLAM = 299792.458, 1215.67, 0.8
    kmaxz = lambda z: 0.5 * math.pi / (CLIGHT * DLAM / ((1 + z) * LLYA)); SEL = np.zeros(len(Zall), bool)
    for z in ZB: SEL |= (np.round(Zall, 2) == z) & (Kall > 0.001) & (Kall < kmaxz(z))
    NB = int(SEL.sum()); zs, ks, Pd = np.round(Zall[SEL], 2), Kall[SEL], Pall[SEL]; Cs = C_full[np.ix_(SEL, SEL)]; CF = cho_factor(0.5 * (Cs + Cs.T)); del HD, T, C_full
    def dchi2_forest(r): d = (r - 1.0) * Pd; return float(d @ cho_solve(CF, d))
    KF = np.exp(np.linspace(math.log(1e-4), math.log(200.0), 60000))
    def p1d_at(kpar, Pk):
        f = KF * Pk; seg = 0.5 * (f[1:] + f[:-1]) * np.diff(KF); cum = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]]); return np.interp(np.log(kpar), np.log(KF), cum) / (2 * math.pi)
    RES["forest_data"] = dict(md5=MD5, md5_ok=MD5 == "33d7fc21bfd3d745ed71a0bbe80ca433", nbins=NB, nbins_ok=NB == 755)
    P(f"forest data: md5 ok {RES['forest_data']['md5_ok']}, {NB} bins  [{time.time()-J.T0:.0f}s {J.rss():.2f}GB]")
    # ---------------- GL1 corrected Limber kernel (BG1's limber4) and the growth ODE with a per-k clustered weight
    def limber4(M, kgrid, zgrid, Rm):
        chis = M.angular_distance(1089.0) * (1 + 1089.0); chi = np.array([M.angular_distance(z) * (1 + z) for z in zgrid]); lnk = np.log(kgrid)
        Pm = np.array([[M.pk_lin(k, z) for z in zgrid] for k in kgrid])
        w = ((chis - chi) / (chi * chis)) ** 2 * (1 + np.asarray(zgrid)) ** 2 / np.array([M.Hubble(z) for z in zgrid])
        Ls = np.arange(2, LMAX + 1); num = np.zeros(len(Ls)); den = np.zeros(len(Ls))
        for j in range(len(zgrid)):
            kk = (Ls + 0.5) / chi[j]; m = (kk >= kgrid[0]) & (kk <= kgrid[-1])
            Pj = np.interp(np.log(kk[m]), lnk, Pm[:, j]); Rj = np.interp(np.log(kk[m]), lnk, Rm[:, j]); ex = (chi[j] / (Ls[m] + 0.5)) ** 4
            num[m] += w[j] * Pj * Rj ** 2 / chi[j] ** 2 * ex; den[m] += w[j] * Pj / chi[j] ** 2 * ex
        S = np.ones(LMAX + 1); ok = den > 0; S[Ls[ok]] = num[ok] / den[ok]; return S, Pm
    def growth(M, ob, od, H0, kgrid, zgrid):
        """QX3 iter2 / BG1 growth solve; fc(lna) -> array over k = the component's NON-clustering fraction (1 - W). Returns ratio_of(fc), ref."""
        h = H0 / 100; Om_b0 = ob / h ** 2; Om_d0 = od / h ** 2
        lna_t = np.linspace(math.log(1 / 3500.0), 0.0, 4000); lnH_t = np.array([math.log(M.Hubble(1 / math.exp(x) - 1)) for x in lna_t]); dlnH_t = np.gradient(lnH_t, lna_t); H0c = M.Hubble(0.0)
        ai = 1 / 3401.0; adec = 1 / 1091.0; lnz = np.log(1 / (1 + np.asarray(zgrid))); kv = np.asarray(kgrid); nk = len(kv)
        grid = np.unique(np.concatenate([np.linspace(math.log(ai), 0.0, 6001), lnz])); tset = {float(x): i for i, x in enumerate(lnz)}; I4 = np.eye(4)[None, :, :]
        E2t = np.exp(2 * np.interp(grid, lna_t, lnH_t)) / H0c ** 2; dlt = np.interp(grid, lna_t, dlnH_t)
        def solve(fc):
            y = np.zeros((nk, 4)); y[:, 0] = ai; y[:, 1] = ai; rec = {}
            for n in range(len(grid) - 1):
                h_ = grid[n + 1] - grid[n]; lm = 0.5 * (grid[n] + grid[n + 1]); a = math.exp(lm)
                E2 = math.exp(2 * np.interp(lm, lna_t, lnH_t)) / H0c ** 2; dl = float(np.interp(lm, lna_t, dlnH_t))
                fcv = fc(lm) if fc is not None else 0.0
                Od = Om_d0 * a ** -3 / E2 * (1.0 - fcv); Ob = Om_b0 * a ** -3 / E2; on = a > adec
                A = np.zeros((nk, 4, 4)); A[:, 0, 1] = 1; A[:, 1, 0] = 1.5 * Od; A[:, 1, 1] = -(2 + dl)
                if on: A[:, 1, 2] = 1.5 * Ob; A[:, 2, 3] = 1; A[:, 3, 0] = 1.5 * Od; A[:, 3, 2] = 1.5 * Ob; A[:, 3, 3] = -(2 + dl)
                y = np.linalg.solve(I4 - 0.5 * h_ * A, ((I4 + 0.5 * h_ * A) @ y[:, :, None]))[:, :, 0]
                t = float(grid[n + 1])
                if t in tset: rec[tset[t]] = y.copy()
            out = np.empty((nk, len(zgrid)))
            for jz in range(len(zgrid)):
                yy = rec[jz]; a = 1 / (1 + zgrid[jz]); E2 = math.exp(2 * np.interp(math.log(a), lna_t, lnH_t)) / H0c ** 2
                Od = Om_d0 * a ** -3 / E2; Ob = Om_b0 * a ** -3 / E2; fz = fc(math.log(a)) if fc is not None else 0.0
                out[:, jz] = (Od * (1 - fz) * yy[:, 0] + Ob * yy[:, 2]) / (Od + Ob)
            return out
        ref = solve(None); return (lambda fc: solve(fc) / ref), ref
    for f in J.FOOTS:
        th = THETA[f]; R_ = {}; RES[f] = R_; Rf = J.RF[f]
        M = Class(); M.set({'output': 'tCl,lCl,mPk', 'l_max_scalars': LMAX + 100, 'h': th["h"], 'omega_b': th["omega_b"], 'omega_cdm': th["omega_d"], 'A_s': Q3["AS0"],
                            'n_s': th["n_s"], 'tau_reio': th["tau"], 'N_ur': 3.046, 'T_cmb': 2.7255, 'P_k_max_1/Mpc': 210.0, 'z_max_pk': ZPK}); M.compute()
        X0 = Q3["X_of"](M); c0, _ = Q3["best_amp_chi2"](X0); H0c = 100 * th["h"]; hh = th["h"]
        ratio_of, ref = growth(M, th["omega_b"], th["omega_d"], H0c, KG, ZG)
        S1, Pref = limber4(M, KG, ZG, np.ones_like(ref)); c1, _ = Q3["best_amp_chi2"](X0 * S1)
        # per-mode linear potential on the web (Poisson; matter era), Phi/c^2 = 1.5 Omega_m (H0/c)^2 delta_rms / (a k^2)
        Om = (th["omega_b"] + th["omega_d"]) / hh ** 2; H0c_Mpc = hh / 2997.92458
        lnPref = np.log(Pref); drms = np.sqrt(KG[:, None] ** 3 * Pref / (2 * math.pi ** 2)); AG = 1 / (1 + ZG)
        PHI = 1.5 * Om * H0c_Mpc ** 2 * drms / (AG[None, :] * KG[:, None] ** 2)        # (nk, nz)
        lnA_z = np.log(AG); o = np.argsort(lnA_z); lnA_s = lnA_z[o]; PHI_s = PHI[:, o]
        def phi_at(lna):
            if lna <= lnA_s[0]: return PHI_s[:, 0]
            j = np.searchsorted(lnA_s, lna); j = min(max(j, 1), len(lnA_s) - 1); t = (lna - lnA_s[j - 1]) / (lnA_s[j] - lnA_s[j - 1]); return PHI_s[:, j - 1] * (1 - t) + PHI_s[:, j] * t
        R_["phi_web_table"] = {f"k {k:g}": {f"z {z:g}": float(PHI[np.argmin(abs(KG - k)), np.argmin(abs(ZG - z))]) for z in (0.02, 1, 3, 10)} for k in (1e-3, 0.01, 0.1, 1.0, 10.0)}
        # fsigma8 (CE2 / BG1 statistic)
        R8 = 8.0 / hh; lk = np.log(KG); W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3; w2k3 = W8(KG * R8) ** 2 * KG ** 3 / (2 * np.pi ** 2)
        def sig8(Rr): return np.sqrt(np.trapz(Pref * Rr ** 2 * w2k3[:, None], lk, axis=0))
        lna_z = np.log(1 / (1 + ZG))
        def fs8_ratio(Rr):
            oo = np.argsort(lna_z); s_sw = sig8(Rr); s_rf = sig8(np.ones_like(Rr))
            d_sw = CubicSpline(lna_z[oo], s_sw[oo]).derivative()(lna_z); d_rf = CubicSpline(lna_z[oo], s_rf[oo]).derivative()(lna_z); rr = d_sw / d_rf
            return {b[0]: float(np.interp(b[1], ZG, rr)) for b in DESI}
        def fs8_gate(rf):
            rows = []
            for (t, z, r1, p1, m1, r2, p2, m2) in DESI:
                e1, e2 = 0.5 * (p1 + m1), 0.5 * (p2 + m2); x = rf[t]; rows.append(dict(bin=t, z=z, Rf=x, in_sf=bool(abs(x - r1) <= 2 * e1), in_sfb=bool(abs(x - r2) <= 2 * e2), s8dir=bool(x <= 1.001)))
            return dict(rows=rows, pass_=bool(all(r["in_sf"] and r["in_sfb"] and r["s8dir"] for r in rows)))
        # forest grader pieces (NC2 G3): base P1D per z from CLASS pk_lin on KF
        HZ = {float(z): M.Hubble(float(z)) * CLIGHT for z in ZB}; kp = np.array([k * HZ[float(z)] / (1 + z) for k, z in zip(ks, zs)])
        ksamp = np.exp(np.linspace(math.log(1e-4), math.log(0.999 * 200.0), 700)); PL = {}
        for z in ZB:
            lp = np.log([M.pk_lin(float(kk), float(z)) for kk in ksamp]); PL[float(z)] = np.exp(CubicSpline(np.log(ksamp), lp, extrapolate=True)(np.log(KF)))
        base = np.empty(NB)
        for z in ZB: s_ = zs == z; base[s_] = p1d_at(kp[s_], PL[float(z)])
        def forest(Rr):
            r = np.empty(NB)
            for z in ZB:
                s_ = zs == z; jz = int(np.argmin(abs(ZG - z))); Rk = np.interp(np.log(KF), lk, Rr[:, jz]); r[s_] = p1d_at(kp[s_], PL[float(z)] * Rk ** 2) / base[s_]
            d = dchi2_forest(r); return dict(dchi2=d, status="PASS" if d <= 4 else ("TENSION" if d <= 25 else "FAIL"), r_min=float(r.min()), r_max=float(r.max()))
        ka5 = fs8_ratio(np.ones_like(ref)); fr0 = forest(np.ones_like(ref))
        R_["KA5_identity"] = dict(fs8_at_R1=ka5, dchi2_lensing_at_R1=float(c1 - c0), forest_dchi2_at_R1=fr0["dchi2"], baseline_lensing_chi2=float(c0),
                                  pass_=bool(max(abs(v - 1) for v in ka5.values()) <= 1e-6 and abs(c1 - c0) <= 1e-9 and fr0["dchi2"] <= 1e-9))
        P(f"[{f}] KA5: R = 1 gives Rf 1, dchi2 {c1-c0:.2e}, forest {fr0['dchi2']:.1e}; baseline lensing chi2 {c0:.3f} -> {'PASS' if R_['KA5_identity']['pass_'] else 'FAIL'}  [{time.time()-J.T0:.0f}s {J.rss():.2f}GB]")
        if not R_["KA5_identity"]["pass_"]: continue
        def eval_point(pt, mode="per_mode"):
            RJ0, PHS, p_, form = pt["RJ0"], pt["PHS"], pt["p"], pt["form"]
            def W(lna):
                a = math.exp(lna); ph = phi_at(lna) if mode == "per_mode" else np.full(len(KG), SIGMA_PHI_LSS)
                return J.S_of(ph, PHS, p_, 1.0) / (1.0 + (KG * J.RJ_of(ph, RJ0, PHS, p_, form) / a) ** 4)
            fc = lambda lna: 1.0 - W(lna)
            Rr = ratio_of(fc); S, _ = limber4(M, KG, ZG, Rr); c, A = Q3["best_amp_chi2"](X0 * S); dchi = float(c - c0); rf = fs8_ratio(Rr); fg = fs8_gate(rf); fo = forest(Rr)
            W0 = W(0.0); W3 = W(math.log(1 / 4.0))
            return dict(point=pt, G8=dict(status="PASS" if (dchi <= 4.0 and fg["pass_"]) else "FAIL", lensing_dchi2=dchi, lensing_pass=bool(dchi <= 4.0), fsigma8=fg, S_L100=float(S[100]), S_L400=float(S[400])),
                        G9=dict(status=fo["status"], **{k: v for k, v in fo.items() if k != "status"}),
                        W_today={f"k {k:g}": float(np.interp(k, KG, W0)) for k in (0.01, 0.1, 1.0, 10.0)}, W_z3={f"k {k:g}": float(np.interp(k, KG, W3)) for k in (0.1, 1.0, 10.0)},
                        R_z0_k0p1=float(np.interp(0.1, KG, Rr[:, 0])), R_z3_k1=float(Rr[np.argmin(abs(KG - 1.0)), np.argmin(abs(ZG - 3.0))]))
        pts = J.POINTS if J.POINTS is not None else J.grid_points()
        if J.POINTS is None:
            R_["as_written"] = {}
            for form in J.FORMS:
                pt = dict(RJ0=J.ASW["RJ0"], PHS=J.ASW["PHS"], p=J.ASW["p"], form=form)
                o = eval_point(pt); R_["as_written"][form] = o; o2 = eval_point(pt, "total_potential"); R_["as_written"][form + "_total_potential_reading"] = o2
                P(f"[{f}] AS-WRITTEN {form}: G8 {o['G8']['status']} dchi2 {o['G8']['lensing_dchi2']:.2f} Rf " + " ".join(f"{r['bin']} {r['Rf']:.3f}" for r in o['G8']['fsigma8']['rows'])
                  + f" | G9 {o['G9']['status']} dchi2 {o['G9']['dchi2']:.1f} r [{o['G9']['r_min']:.3f}, {o['G9']['r_max']:.3f}] | W(z0) " + " ".join(f"{k}:{v:.2f}" for k, v in o['W_today'].items())
                  + f" || total-potential reading: G8 {o2['G8']['status']} {o2['G8']['lensing_dchi2']:.2f}, G9 {o2['G9']['status']} {o2['G9']['dchi2']:.1f}  [{time.time()-J.T0:.0f}s {J.rss():.2f}GB]")
        grid = []
        for i, pt in enumerate(pts):
            o = eval_point(pt); o2 = eval_point(pt, "total_potential"); o["total_potential_reading"] = dict(G8=o2["G8"], G9=o2["G9"], W_today=o2["W_today"]); grid.append(o)
            if i % 12 == 0 or i == len(pts) - 1:
                P(f"[{f}] {J.pkey(pt):34s}: G8 {o['G8']['status'][0]} {o['G8']['lensing_dchi2']:7.2f} fs8 {'P' if o['G8']['fsigma8']['pass_'] else 'F'} | G9 {o['G9']['status'][0]} {o['G9']['dchi2']:9.1f} | W(z0) k0.1 {o['W_today']['k 0.1']:.2f} k1 {o['W_today']['k 1']:.2f} k10 {o['W_today']['k 10']:.2f}"
                  f" || total-potential: G8 {o2['G8']['status'][0]} {o2['G8']['lensing_dchi2']:7.2f} G9 {o2['G9']['status'][0]} {o2['G9']['dchi2']:9.1f}  [{time.time()-J.T0:.0f}s {J.rss():.2f}GB]")
                R_["grid"] = grid; J.dump(f"web{J.SUFFIX}_partial.json", RES)
        R_["grid"] = grid; M.struct_cleanup(); M.empty()
    RES["peak_rss_GB"] = J.rss(); RES["seconds"] = time.time() - J.T0; RES["criteria"] = J.CRIT; RES["note"] = J.NOTE
    J.dump(f"web{J.SUFFIX}.json", RES)
    pp = os.path.join(J.PARTS, f"web{J.SUFFIX}_partial.json")
    if os.path.exists(pp): os.remove(pp)
    P(f"web{J.SUFFIX} done {RES['seconds']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB")
