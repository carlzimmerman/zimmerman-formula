#!/usr/bin/env python3
"""WD1 gates G8 and G9 (FROZEN_CRITERIA.md 0cd6ef1dcb) on the web, through the record's machinery as PJ1's pj1_web.py carries it
(QX3 iter2 growth ODE in BG1's two-fluid form, GL1's corrected Limber kernel on raw PR4 lensing, CE2's fsigma8 rule on DESI DR1,
NC2 G3's forest machinery on the DESI DR1 P1D; own transcription, the sources read-only; KA: R = 1 reproduces PJ1's identities and
baseline lensing chi^2).
G8 growth: before shell-crossing the component is cold dust, so the linear growth is the record's own (fsigma8 ratios 1 by
    construction; stated). Reported beside: the footing-background reading in which only 4.40 of the R = 5.41 omega_b clusters.
G8 lensing: every collapsed halo's component sits in a core of R_c0 = 1.6 Mpc PHYSICAL (field halos, N 0). The core's density is
    a Plummer sphere (rho ~ R_c^2/(r^2 + R_c^2)^(5/2)), whose Fourier profile is u(x) = x K_1(x), x = k R_c0 / a. Entered as a
    halo-model one-halo suppression: P_supp = P_lin + (P_halofit - P_lin)_+ x S_1h, S_1h = [(f u + 1)/(1 + f)]^2 (the baryons keep
    their compact profile), and the record's kernel takes the ratio R^2 = P_supp / P_halofit. The record's kernel integrates LINEAR
    power, so the suppression enters as a ratio of nonlinear powers (disclosed); the nonlinear-baseline reading (chi^2 at P_supp
    minus chi^2 at P_halofit, both on the kernel) is reported beside it.
G9 forest: Jeans-type suppression at the Thomas-Fermi scale from the first minihalo shell-crossings (z 20) on: the component's
    clustering fraction at wavenumber k is T_J = 1/(1 + (k/k_J)^2), k_J = pi a / R_c0 (the n^2 polytrope's Jeans wavenumber at the
    core radius), entered in the growth ODE as BG1's non-clustering fraction 1 - T_J; the sharper 1/(1 + (k/k_J)^4) form reported.
    Ly-alpha P1D at z 2-4 within the NC2 band (Delta chi^2_Asimov <= 4 PASS, 4-25 TENSION, > 25 FAIL).
kappa = 1/2 FITTED; not theory closed; footings never pooled; adopts nothing."""
import os, sys, json, math, time, tarfile, io, hashlib
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.linalg import cho_factor, cho_solve
from scipy.special import k1 as bessel_k1
import wd1 as W
J = W.J; P = W.P
DESI = [("BGS", 0.295, 0.80, 0.20, 0.20, 0.84, 0.19, 0.19), ("LRG1", 0.510, 1.09, 0.12, 0.14, 1.16, 0.13, 0.13),
        ("LRG2", 0.706, 1.05, 0.12, 0.12, 1.04, 0.11, 0.092), ("LRG3", 0.919, 0.96, 0.11, 0.10, 0.997, 0.10, 0.084)]   # DESI DR1 Table 9 as CE2 / BG1 / PJ1 transcribed it
PJ1_BASE = {"canonical": 8.559852345908991, "alt": 8.560405550735853}          # PJ1 KA5 baseline lensing chi^2 (parts/web.json)
RC0_MPC = W.RC0_KPC / 1e3; Z_SC = 20.0; A_SC = 1.0 / (1.0 + Z_SC)

def run_web(RES):
    Q3 = J.load_prefix(os.path.join(J.CL6, "QX3_cmb_growth", "iter2_kq_dust", "iter2.py"), 'if __name__ == "__main__":', "qx3_iter2_lib")
    Class, LMAX, ZPK = Q3["Class"], Q3["LMAX"], Q3["ZPK"]
    Q15 = json.load(open(os.path.join(J.CL6, "QX15_cmb_primary_likelihood", "qx15.json")))
    THETA = {f: dict(Q15["footings"][f]["main"]["theta"], h=Q15["footings"][f]["main"]["h"]) for f in W.FOOTS}
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
    P(f"forest data: md5 ok {RES['forest_data']['md5_ok']}, {NB} bins  [{time.time()-W.T0:.0f}s {W.rss():.2f}GB]")
    # ---------------- GL1 corrected Limber kernel (BG1's limber4) and the growth ODE with a per-k non-clustering fraction
    def limber4(M, kgrid, zgrid, Rm, Pm=None):
        chis = M.angular_distance(1089.0) * (1 + 1089.0); chi = np.array([M.angular_distance(z) * (1 + z) for z in zgrid]); lnk = np.log(kgrid)
        if Pm is None: Pm = np.array([[M.pk_lin(k, z) for z in zgrid] for k in kgrid])
        w = ((chis - chi) / (chi * chis)) ** 2 * (1 + np.asarray(zgrid)) ** 2 / np.array([M.Hubble(z) for z in zgrid])
        Ls = np.arange(2, LMAX + 1); num = np.zeros(len(Ls)); den = np.zeros(len(Ls))
        for j in range(len(zgrid)):
            kk = (Ls + 0.5) / chi[j]; m = (kk >= kgrid[0]) & (kk <= kgrid[-1])
            Pj = np.interp(np.log(kk[m]), lnk, Pm[:, j]); Rj = np.interp(np.log(kk[m]), lnk, Rm[:, j]); ex = (chi[j] / (Ls[m] + 0.5)) ** 4
            num[m] += w[j] * Pj * Rj ** 2 / chi[j] ** 2 * ex; den[m] += w[j] * Pj / chi[j] ** 2 * ex
        S = np.ones(LMAX + 1); ok = den > 0; S[Ls[ok]] = num[ok] / den[ok]; return S, Pm
    def growth(M, ob, od, H0, kgrid, zgrid):
        h = H0 / 100; Om_b0 = ob / h ** 2; Om_d0 = od / h ** 2
        lna_t = np.linspace(math.log(1 / 3500.0), 0.0, 4000); lnH_t = np.array([math.log(M.Hubble(1 / math.exp(x) - 1)) for x in lna_t]); dlnH_t = np.gradient(lnH_t, lna_t); H0c = M.Hubble(0.0)
        ai = 1 / 3401.0; adec = 1 / 1091.0; lnz = np.log(1 / (1 + np.asarray(zgrid))); kv = np.asarray(kgrid); nk = len(kv)
        grid = np.unique(np.concatenate([np.linspace(math.log(ai), 0.0, 6001), lnz])); tset = {float(x): i for i, x in enumerate(lnz)}; I4 = np.eye(4)[None, :, :]
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
    for f in W.FOOTS:
        th = THETA[f]; R_ = {}; RES[f] = R_; Rf = W.RF[f]; hh = th["h"]
        base_pars = {'output': 'tCl,lCl,mPk', 'l_max_scalars': LMAX + 100, 'h': hh, 'omega_b': th["omega_b"], 'omega_cdm': th["omega_d"], 'A_s': Q3["AS0"], 'n_s': th["n_s"], 'tau_reio': th["tau"], 'N_ur': 3.046, 'T_cmb': 2.7255, 'P_k_max_1/Mpc': 210.0, 'z_max_pk': ZPK}
        M = Class(); M.set(base_pars); M.compute()
        X0 = Q3["X_of"](M); c0, _ = Q3["best_amp_chi2"](X0); H0c = 100 * hh
        ratio_of, ref = growth(M, th["omega_b"], th["omega_d"], H0c, KG, ZG)
        S1, Pref = limber4(M, KG, ZG, np.ones_like(ref)); c1, _ = Q3["best_amp_chi2"](X0 * S1)
        # halofit nonlinear power on the same background (a second CLASS instance, released after the table is taken)
        MN = Class(); MN.set(dict(base_pars, **{'non linear': 'halofit'})); MN.compute()
        PNL = np.array([[MN.pk(k, z) for z in ZG] for k in KG]); MN.struct_cleanup(); MN.empty()
        # fsigma8 (CE2 / BG1 statistic) and the forest base
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
            d = dchi2_forest(r); return dict(dchi2=d, status="PASS" if d <= 4 else ("TENSION" if d <= 25 else "FAIL"), r_min=float(r.min()), r_max=float(r.max()),
                                            r_by_z={f"{z:g}": float(np.mean(r[zs == z])) for z in ZB})
        ka5 = fs8_ratio(np.ones_like(ref)); fr0 = forest(np.ones_like(ref))
        R_["KA_web"] = dict(fs8_at_R1=ka5, dchi2_lensing_at_R1=float(c1 - c0), forest_dchi2_at_R1=fr0["dchi2"], baseline_lensing_chi2=float(c0), pj1_baseline=PJ1_BASE[f],
                            pass_=bool(max(abs(v - 1) for v in ka5.values()) <= 1e-6 and abs(c1 - c0) <= 1e-9 and fr0["dchi2"] <= 1e-9 and abs(c0 - PJ1_BASE[f]) <= 1e-3))
        P(f"[{f}] KA web: R = 1 gives Rf 1, dchi2 {c1-c0:.2e}, forest {fr0['dchi2']:.1e}; baseline lensing chi2 {c0:.4f} (PJ1 {PJ1_BASE[f]:.4f}) -> {'PASS' if R_['KA_web']['pass_'] else 'FAIL'}  [{time.time()-W.T0:.0f}s {W.rss():.2f}GB]")
        if not R_["KA_web"]["pass_"]: continue
        AG = 1 / (1 + ZG)
        # ---- G8 growth: the frozen reading (cold dust before shell-crossing: Rf = 1 by construction) and the footing-background reading (4.40 of R clusters)
        fc_bg = 1.0 - W.F_COSMIC / Rf
        Rr_bg = ratio_of(lambda lna: np.full(len(KG), fc_bg)); S_bg, _ = limber4(M, KG, ZG, Rr_bg); c_bg, _ = Q3["best_amp_chi2"](X0 * S_bg); fg_bg = fs8_gate(fs8_ratio(Rr_bg))
        R_["G8_growth"] = dict(status="PASS", reading="cold dust before shell-crossing: the record's own linear growth, fsigma8 ratios 1 by construction (frozen statement)", fs8=fs8_gate(ka5),
                               footing_background_reported=dict(non_clustering_fraction=fc_bg, fs8=fg_bg, lensing_dchi2=float(c_bg - c0)))
        P(f"[{f}] G8 growth: PASS by construction; footing-background reading (1 - {W.F_COSMIC}/{Rf:.3f} smooth): Rf " + " ".join(f"{r['bin']} {r['Rf']:.3f}" for r in fg_bg['rows']) + f", fs8 {'PASS' if fg_bg['pass_'] else 'FAIL'}, lensing dchi2 {c_bg - c0:.2f}")
        # ---- G8 lensing: halo-model one-halo suppression from the 1.6 Mpc physical cores
        x = KG[:, None] * RC0_MPC / AG[None, :]; u = np.where(x > 0, x * bessel_k1(np.maximum(x, 1e-300)), 1.0); S1h = ((W.F_COSMIC * u + 1.0) / (1.0 + W.F_COSMIC)) ** 2
        P1h = np.maximum(PNL - Pref, 0.0); Psupp = Pref + P1h * S1h
        R2_ratio = Psupp / PNL; S_L, _ = limber4(M, KG, ZG, np.sqrt(R2_ratio)); c_L, A_L = Q3["best_amp_chi2"](X0 * S_L); d_L = float(c_L - c0)
        S_nl, _ = limber4(M, KG, ZG, np.sqrt(PNL / Pref)); c_nl, _ = Q3["best_amp_chi2"](X0 * S_nl); S_ns, _ = limber4(M, KG, ZG, np.sqrt(Psupp / Pref)); c_ns, _ = Q3["best_amp_chi2"](X0 * S_ns)
        iz0 = 0; iz2 = int(np.argmin(abs(ZG - 2.0)))
        R_["G8_lensing"] = dict(status="PASS" if d_L <= 4.0 else "FAIL", dchi2=d_L, reading="ratio P_supp / P_halofit on the record's (linear) kernel vs the record's baseline",
                                nonlinear_baseline_reported=dict(chi2_halofit=float(c_nl - c0), chi2_halofit_suppressed=float(c_ns - c0), dchi2=float(c_ns - c_nl)),
                                S_L={f"L {L}": float(S_L[L]) for L in (10, 40, 100, 200, 400)}, one_halo_fraction_z0={f"k {k:g}": float((P1h[np.argmin(abs(KG - k)), iz0]) / PNL[np.argmin(abs(KG - k)), iz0]) for k in (0.1, 0.3, 1.0, 3.0)},
                                S1h_z0={f"k {k:g}": float(S1h[np.argmin(abs(KG - k)), iz0]) for k in (0.1, 0.3, 1.0, 3.0)}, S1h_z2={f"k {k:g}": float(S1h[np.argmin(abs(KG - k)), iz2]) for k in (0.1, 0.3, 1.0, 3.0)},
                                core_Mpc_physical=RC0_MPC, kernel_note="the record's lensing kernel (GL1 / BG1 limber4) integrates linear power; the one-halo suppression enters as the ratio of nonlinear powers (disclosed)")
        R_["G8"] = dict(status="PASS" if (R_["G8_growth"]["status"] == "PASS" and R_["G8_lensing"]["status"] == "PASS") else "FAIL", lensing_dchi2=d_L, fsigma8=R_["G8_growth"]["fs8"])
        P(f"[{f}] G8 lensing (1.6 Mpc physical cores, one-halo suppression): dchi2 {d_L:+.2f} -> {R_['G8_lensing']['status']}; S_L(100) {S_L[100]:.3f} S_L(400) {S_L[400]:.3f}; nonlinear-baseline reading {c_ns - c_nl:+.2f} (halofit alone {c_nl - c0:+.2f}); 1-halo share z0 k1 {R_['G8_lensing']['one_halo_fraction_z0']['k 1']:.2f}  [{time.time()-W.T0:.0f}s {W.rss():.2f}GB]")
        # ---- G9 forest: Jeans-type suppression at the Thomas-Fermi scale from z 20 on
        def TJ(lna, p_):
            a = math.exp(lna)
            if a < A_SC: return np.ones(len(KG))
            kJ = math.pi * a / RC0_MPC; return 1.0 / (1.0 + (KG / kJ) ** p_)
        g9 = {}
        for tag, p_ in (("primary_k2", 2), ("sharper_k4_reported", 4)):
            Rr = ratio_of(lambda lna, p_=p_: 1.0 - TJ(lna, p_)); fo = forest(Rr); fg = fs8_gate(fs8_ratio(Rr)); S_, _ = limber4(M, KG, ZG, Rr); c_, _ = Q3["best_amp_chi2"](X0 * S_)
            g9[tag] = dict(fo, fsigma8_reported=fg, lensing_dchi2_reported=float(c_ - c0), kJ_comoving_z3=math.pi / (4 * RC0_MPC), kJ_comoving_z0=math.pi / RC0_MPC,
                           R_z3={f"k {k:g}": float(Rr[np.argmin(abs(KG - k)), np.argmin(abs(ZG - 3.0))]) for k in (0.1, 0.3, 1.0, 3.0, 10.0)}, R_z0_k1=float(Rr[np.argmin(abs(KG - 1.0)), 0]))
            P(f"[{f}] G9 {tag}: {fo['status']} dchi2 {fo['dchi2']:.1f}, r [{fo['r_min']:.3f}, {fo['r_max']:.3f}] by z " + " ".join(f"{z}:{v:.2f}" for z, v in fo['r_by_z'].items()) + f"; R(z3) " + " ".join(f"{k}:{v:.2f}" for k, v in g9[tag]['R_z3'].items())
              + f"; fs8 {'P' if fg['pass_'] else 'F'}, lensing {c_ - c0:+.1f}  [{time.time()-W.T0:.0f}s {W.rss():.2f}GB]")
        R_["G9"] = dict(status=g9["primary_k2"]["status"], dchi2=g9["primary_k2"]["dchi2"], r_min=g9["primary_k2"]["r_min"], r_max=g9["primary_k2"]["r_max"], readings=g9)
        W.dump("web_partial.json", RES); M.struct_cleanup(); M.empty()
    RES["peak_rss_GB"] = W.rss(); RES["seconds"] = time.time() - W.T0; RES["criteria"] = W.CRIT; RES["note"] = W.NOTE; RES["mutate"] = W.MUTATE
    W.dump(f"web{W.SUFFIX}.json", RES)
    pp = os.path.join(W.PARTS, "web_partial.json")
    if os.path.exists(pp): os.remove(pp)
    P(f"web done {RES['seconds']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB")

if __name__ == "__main__":
    P(f"WD1 web. Criteria {W.CRIT}. R_c0 {RC0_MPC} Mpc physical, f {W.F_COSMIC}, shell-crossing z {Z_SC}. {W.NOTE}; footings never pooled; adopts nothing.")
    run_web({})
