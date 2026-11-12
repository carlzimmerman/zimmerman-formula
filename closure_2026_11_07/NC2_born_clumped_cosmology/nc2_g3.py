#!/usr/bin/env python3
"""NC2 gate G3 (R6 / K2): forest 1D power z 2.2-4.4, DESI DR1 P1D (P1D3's table + full covariance, read-only loader copy).

Grades the RATIO r(k, z) = P1D_NC / P1D_uniform of the linear 1D matter power, Delta chi2_Asimov = d^T C^-1 d,
d = (r - 1) x PLYA, on two brackets of the born-clumped cold dark energy field (FROZEN_CRITERIA.md row G3, KA3, M2/M3):
  (i)  P_NC = P_lin [f_b + f_c (1 - f_in) + f_c f_in W]^2 + P_cl,  W = |u(k r_cl)|,  P_cl = f_in^2 f_c^2 u^2 / n_cl
  (ii) inter-clump sightlines: P_NC = P_b,inter = P_b(k, z_dec 1090) [(1 + 1090)/(1 + z)]^(2p),
       p = (sqrt(1 + 24 f) - 1)/4 with f = f_b (reading implemented; disclosed in the outputs).
Labels: <= 4 PASS, 4-25 TENSION, > 25 FAIL; G3 FAIL needs BOTH brackets to fail. Both footings, never pooled.
Cold dark energy = the gravitating w ~ 0 component QX15 needs; never a particle.
Run: OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I nc2_g3.py   (NC2_MUTATE=1 twin)
kappa = 1/2 FITTED; not theory closed.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, time, resource, hashlib, tarfile, io
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.linalg import cho_factor, cho_solve
from astropy.io import fits
from classy import Class

NOTE = "kappa = 1/2 FITTED; not theory closed"
MUT = os.environ.get("NC2_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
RAW = os.path.join(REPO, "_external_data", "desi_dr1_p1d_qmle", "raw", "data_points.tar")
QX15 = os.path.join(REPO, "closure_2026_11_06", "QX15_cmb_primary_likelihood", "parts")
T0 = time.time()
OUT = open(os.path.join(HERE, f"nc2_g3{TAG}.out"), "w")
RES = {"lane": "NC2_born_clumped_cosmology", "gate": "G3", "mutate": MUT, "criteria": "FROZEN_CRITERIA.md (row G3, KA3, M2, M3)"}


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); OUT.write(s + "\n"); OUT.flush()


def label(d):
    return "PASS" if d <= 4 else ("TENSION" if d <= 25 else "FAIL")


P("NC2 G3 forest 1D power" + (" [MUTATE M2/M3: control output, not physics]" if MUT else "") + "; " + NOTE)

# ---------------------------------------------------------------- data (minimal copy of P1D3's loader, read-only)
md5 = hashlib.md5()
with open(RAW, "rb") as fh:
    for blk in iter(lambda: fh.read(1 << 22), b""):
        md5.update(blk)
MD5 = md5.hexdigest()
with tarfile.open(RAW) as tf:
    HD = fits.open(io.BytesIO(tf.extractfile("desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits").read()))
T = HD["P1D_BLIND"].data
Zall, Kall = np.asarray(T["Z"], float), np.asarray(T["K"], float)
Pall = np.asarray(T["PLYA"], float)
C_full = np.asarray(HD["COVARIANCE"].data, float)
ZB = np.round(np.unique(Zall), 2)
CLIGHT, LLYA, DLAM = 299792.458, 1215.67, 0.8
kmaxz = lambda z: 0.5 * math.pi / (CLIGHT * DLAM / ((1 + z) * LLYA))
SEL = np.zeros(len(Zall), bool)
for z in ZB:
    SEL |= (np.round(Zall, 2) == z) & (Kall > 0.001) & (Kall < kmaxz(z))
NB = int(SEL.sum())
zs, ks, Pd = np.round(Zall[SEL], 2), Kall[SEL], Pall[SEL]
Cs = C_full[np.ix_(SEL, SEL)]
CF = cho_factor(0.5 * (Cs + Cs.T))
del HD, T, C_full
P(f"data: md5 {MD5}; z bins {list(ZB)}; selected {NB} (DESI cut 0.001 < k < 0.5 pi/R_z); covariance = full COVARIANCE "
  f"(stat + syst, cross-z kept), as P1D3's primary")


def dchi2(r):
    d = (r - 1.0) * Pd
    return float(d @ cho_solve(CF, d))


# ---------------------------------------------------------------- model pieces
RHO = 2.77536627e11
KMAX = 200.0
NK = 60000
KG = np.exp(np.linspace(math.log(1e-4), math.log(KMAX), NK))
Z_DEC = 1090.0


def u_th(x):
    x = np.asarray(x, float)
    out = np.empty_like(x)
    s = x < 1e-3
    out[s] = 1.0 - x[s] ** 2 / 10.0
    xs = x[~s]
    out[~s] = 3.0 * (np.sin(xs) - xs * np.cos(xs)) / xs ** 3
    return out


def p1d_at(kpar, Pk, kmax=KMAX):
    """(1/2pi) int_{kpar}^{kmax} k P(k) dk on the log grid KG (trapezoid in k)."""
    m = KG <= kmax * (1 + 1e-12)
    k, f = KG[m], KG[m] * Pk[m]
    seg = 0.5 * (f[1:] + f[:-1]) * np.diff(k)
    cum = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])   # int from k_i to kmax
    return np.interp(np.log(kpar), np.log(k), cum) / (2 * math.pi)


def build_footing(foot):
    fit = json.load(open(os.path.join(QX15, f"fit_{foot}_main.json")))
    th, h = fit["theta"], fit["h"]
    ob, od = th["omega_b"], th["omega_d"]
    As, ns = math.exp(th["lnAs1e10"]) * 1e-10, th["n_s"]
    base = {"omega_b": ob, "omega_cdm": od, "h": h, "A_s": As, "n_s": ns, "tau_reio": th["tau"], "N_ur": 3.046,
            "T_cmb": 2.7255, "P_k_max_1/Mpc": KMAX}
    c = Class(); c.set(dict(base, output="mPk", z_max_pk=5)); c.compute()
    # transfer-only run to reach z_dec (CLASS refuses mPk with z_pk > z_rec; current-gauge = synchronous d_b, disclosed)
    c2 = Class(); c2.set(dict(base, output="mTk", z_max_pk=1100, matter_source_in_current_gauge="yes",
                             k_per_decade_for_pk=60)); c2.compute()
    tr = c2.get_transfer(Z_DEC)
    kt = tr["k (h/Mpc)"] * h
    kpiv = 0.05
    Pb_dec = 2 * math.pi ** 2 / kt ** 3 * As * (kt / kpiv) ** (ns - 1) * tr["d_b"] ** 2
    # normalization check of the transfer convention: d_tot at z 3 vs pk_lin at z 3 (same run family)
    tr3 = c2.get_transfer(3.0); k3 = tr3["k (h/Mpc)"] * h
    msk = (k3 > 1e-2) & (k3 < 0.95 * KMAX)
    Pt3 = 2 * math.pi ** 2 / k3[msk] ** 3 * As * (k3[msk] / kpiv) ** (ns - 1) * tr3["d_tot"][msk] ** 2
    pl3 = np.array([c.pk_lin(float(kk), 3.0) for kk in k3[msk]])
    normdev = float(np.max(np.abs(Pt3 / pl3 - 1)))
    # dense Pb(k, z_dec): spline of d_b in ln k (keeps sign through BAO zeros)
    dsp = CubicSpline(np.log(kt), tr["d_b"])
    kc = np.clip(KG, kt[0], kt[-1])
    Pb_dec_G = 2 * math.pi ** 2 / KG ** 3 * As * (KG / kpiv) ** (ns - 1) * dsp(np.log(kc)) ** 2
    # P_lin(k, z) at each DESI z: pk_lin on 700 log points, spline ln P in ln k
    ksamp = np.exp(np.linspace(math.log(1e-4), math.log(0.999 * KMAX), 700))
    PL, HZ = {}, {}
    for z in ZB:
        lp = np.log([c.pk_lin(float(kk), float(z)) for kk in ksamp])
        PL[float(z)] = np.exp(CubicSpline(np.log(ksamp), lp, extrapolate=True)(np.log(KG)))
        HZ[float(z)] = c.Hubble(float(z)) * CLIGHT
    c.struct_cleanup(); c2.struct_cleanup()
    R = od / ob
    return {"foot": foot, "theta": th, "h": h, "ob": ob, "od": od, "R": R, "f_c": R / (1 + R), "f_b": 1 / (1 + R),
            "rho_c": od * RHO, "rho_m": (ob + od) * RHO, "PL": PL, "HZ": HZ, "Pb_dec": Pb_dec_G, "normdev": normdev}


def kpar_mpc(F):
    return np.array([k * F["HZ"][float(z)] / (1 + z) for k, z in zip(ks, zs)])


class Grader:
    def __init__(self, F):
        self.F = F
        self.kp = kpar_mpc(F)
        self.base = {}
        for kmax in (100.0, KMAX):
            self.base[kmax] = np.empty(NB)
            for z in ZB:
                s = zs == z
                self.base[kmax][s] = p1d_at(self.kp[s], self.F["PL"][float(z)], kmax)

    def r_of(self, Pfun, kmax=KMAX):
        r = np.empty(NB)
        for z in ZB:
            s = zs == z
            r[s] = p1d_at(self.kp[s], Pfun(float(z)), kmax) / self.base[kmax][s]
        return r

    def rcl(self, M):
        F = self.F
        return (3 * M * (1 + 1 / F["R"]) / (4 * math.pi * F["rho_m"])) ** (1 / 3)

    def bracket_i(self, M, f_in, rscale=1.0, kmax=KMAX, rfix=None):
        F = self.F
        u = u_th(KG * (self.rcl(M) * rscale if rfix is None else rfix))
        W = np.abs(u)
        ncl = F["rho_c"] / M
        Pcl = f_in ** 2 * F["f_c"] ** 2 * u ** 2 / ncl
        amp = (F["f_b"] + F["f_c"] * (1 - f_in) + F["f_c"] * f_in * W) ** 2
        return self.r_of(lambda z: F["PL"][z] * amp + Pcl, kmax)

    def bracket_ii(self, p, kmax=KMAX):
        F = self.F
        return self.r_of(lambda z: F["Pb_dec"] * ((1 + Z_DEC) / (1 + z)) ** (2 * p), kmax)


def rsummary(r):
    out = {}
    for z in ZB:
        s = zs == z
        out[f"{z:.1f}"] = {"r_min": float(r[s].min()), "r_max": float(r[s].max()),
                           "within_10pct_all_bins": bool(np.all(np.abs(1 - r[s]) <= 0.10))}
    return out


MCL = (1e13, 1e14, 1e15)
R_III = 0.1   # post-freeze bracket (iii), disclosed


def tolerance(fun):
    """scan f_in 0..1 (21 points) for monotonicity, then bisection on Delta chi2 = 4 and 25."""
    fgrid = np.linspace(0, 1, 21)
    dgrid = [fun(f) for f in fgrid]
    mono = bool(np.all(np.diff(dgrid) >= -1e-9))

    def edge(thr):
        if dgrid[-1] <= thr:
            return 1.0
        lo, hi = 0.0, 1.0
        for _ in range(40):
            mid = 0.5 * (lo + hi)
            if fun(mid) <= thr:
                lo = mid
            else:
                hi = mid
        return lo
    return fgrid, dgrid, mono, edge(4.0), edge(25.0)
ok_all = True
RES["footings"] = {}
for foot in ("canonical", "alt"):
    F = build_footing(foot)
    G = Grader(F)
    fb = F["f_b"]
    p_fb = (math.sqrt(1 + 24 * fb) - 1) / 4
    FR = {"R": F["R"], "f_c": F["f_c"], "f_b": fb, "h": F["h"], "transfer_norm_check_max_dev_z3": F["normdev"],
          "kpar_Mpc_range": [float(G.kp.min()), float(G.kp.max())], "note": NOTE}
    P(f"\n== footing {foot}: R {F['R']:.4f} f_c {F['f_c']:.4f} f_b {fb:.4f}; k_par {G.kp.min():.3f}-{G.kp.max():.3f} /Mpc; "
      f"transfer normalization vs pk_lin at z 3: max dev {F['normdev']:.1e}")
    # KA3
    r0 = G.bracket_i(1e14, 0.0)
    ka3 = {"md5": MD5, "md5_ok": MD5 == "33d7fc21bfd3d745ed71a0bbe80ca433", "nbins": NB, "nbins_ok": NB == 755,
           "f_in0_max_abs_r_minus_1": float(np.max(np.abs(r0 - 1))), "f_in0_dchi2": dchi2(r0)}
    ka3["pass"] = ka3["md5_ok"] and ka3["nbins_ok"] and ka3["f_in0_max_abs_r_minus_1"] <= 1e-12 and ka3["f_in0_dchi2"] <= 1e-12
    ok_all &= ka3["pass"]
    FR["KA3"] = ka3
    P(f"  KA3 {'PASS' if ka3['pass'] else 'FAIL'}: md5 ok {ka3['md5_ok']}, {NB} bins, f_in 0 max|r-1| "
      f"{ka3['f_in0_max_abs_r_minus_1']:.1e}, dchi2 {ka3['f_in0_dchi2']:.1e}")
    # bracket (ii) is M_cl- and f_in-independent
    rii = G.bracket_ii(p_fb)
    rii100 = G.bracket_ii(p_fb, 100.0)
    dii = dchi2(rii)
    rii_p1 = G.bracket_ii(1.0)
    FR["bracket_ii"] = {"reading": "p = (sqrt(1+24 f)-1)/4 with f = f_b = Omega_b/Omega_m (baryons cluster, mean matter "
                                   "density drives expansion); grown from a = 1/1091 as a^p, Lambda late suppression ignored; "
                                   "whole sightline inter-clump; d_b synchronous gauge at z 1090 from CLASS",
                        "p": p_fb, "dchi2": dii, "label": label(dii), "r_per_z": rsummary(rii),
                        "dchi2_kmax100": dchi2(rii100),
                        "reported_not_graded_p1_f_b_loc_1": {"p": 1.0, "dchi2": dchi2(rii_p1), "label": label(dchi2(rii_p1)),
                                                             "r_per_z": rsummary(rii_p1)}}
    P(f"  bracket (ii) p {p_fb:.4f}: dchi2 {dii:.4g} -> {label(dii)}; r z2.2 "
      f"{FR['bracket_ii']['r_per_z']['2.2']['r_min']:.3g}-{FR['bracket_ii']['r_per_z']['2.2']['r_max']:.3g}; "
      f"(reported p = 1: dchi2 {dchi2(rii_p1):.4g})")
    FR["bracket_i"] = {}
    for M in MCL:
        if MUT:
            break
        ri = G.bracket_i(M, 1.0)
        ri100 = G.bracket_i(M, 1.0, kmax=100.0)
        di = dchi2(ri)
        fgrid, dgrid, mono, f4, f25 = tolerance(lambda f: dchi2(G.bracket_i(M, f)))
        # post-freeze bracket (iii), disclosed: bracket (i) with the clump window at r = 0.1 Mpc in W and P_cl
        r3 = G.bracket_i(M, 1.0, rfix=R_III)
        d3 = dchi2(r3)
        fg3, dg3, mono3, f4_3, f25_3 = tolerance(lambda f: dchi2(G.bracket_i(M, f, rfix=R_III)))
        rec3 = {"tag": "post-freeze bracket (iii), disclosed", "r_window_Mpc": R_III, "dchi2": d3, "label": label(d3),
                "dchi2_kmax100": dchi2(G.bracket_i(M, 1.0, kmax=100.0, rfix=R_III)), "r_per_z": rsummary(r3),
                "f_in_tolerated_PASS_dchi2_le_4": f4_3, "f_in_edge_dchi2_le_25": f25_3,
                "dchi2_vs_f_in_grid": dict(zip([f"{f:.2f}" for f in fg3], dg3)), "monotone_in_f_in": mono3}
        FR.setdefault("bracket_iii_post_freeze", {})[f"{M:.0e}"] = rec3
        z3 = rec3["r_per_z"]
        P(f"  post-freeze bracket (iii), disclosed: M_cl {M:.0e}, r 0.1 Mpc, f_in 1: dchi2 {d3:.4g} -> {label(d3)}; "
          f"r z2.2 {z3['2.2']['r_min']:.3f}-{z3['2.2']['r_max']:.3f}, z3.0 {z3['3.0']['r_min']:.3f}-{z3['3.0']['r_max']:.3f}, "
          f"z4.4 {z3['4.4']['r_min']:.3f}-{z3['4.4']['r_max']:.3f}; tolerated f_in (<=4) {f4_3:.4g}, (<=25) {f25_3:.4g}; monotone {mono3}")
        g3 = "FAIL" if (label(di) == "FAIL" and label(dii) == "FAIL") else \
             ("PASS" if (label(di) == "PASS" or label(dii) == "PASS") else "TENSION")
        rec = {"r_cl_Mpc": G.rcl(M), "dchi2": di, "label": label(di), "dchi2_kmax100": dchi2(ri100),
               "max_rel_r_change_kmax100_vs_200": float(np.max(np.abs(ri100 / ri - 1))),
               "r_per_z": rsummary(ri), "f_in_tolerated_PASS_dchi2_le_4": f4, "f_in_edge_dchi2_le_25": f25,
               "dchi2_vs_f_in_grid": dict(zip([f"{f:.2f}" for f in fgrid], dgrid)), "monotone_in_f_in": mono,
               "G3_label_both_brackets": g3}
        FR["bracket_i"][f"{M:.0e}"] = rec
        rz = rec["r_per_z"]
        P(f"  M_cl {M:.0e} (r_cl {rec['r_cl_Mpc']:.2f} Mpc) bracket (i) f_in 1: dchi2 {di:.4g} -> {label(di)} "
          f"[kmax 100: {rec['dchi2_kmax100']:.4g}]; r z2.2 {rz['2.2']['r_min']:.3f}-{rz['2.2']['r_max']:.3f}, "
          f"z3.0 {rz['3.0']['r_min']:.3f}-{rz['3.0']['r_max']:.3f}, z4.4 {rz['4.4']['r_min']:.3f}-{rz['4.4']['r_max']:.3f}; "
          f"tolerated f_in (<=4) {f4:.4g}, (<=25) {f25:.4g}; monotone {mono}; G3 (both brackets) {g3}")
    if MUT:
        mut = {}
        for M in MCL:
            r3 = G.bracket_i(M, 1.0, rscale=0.1)
            d3 = dchi2(r3)
            mut[f"M3_{M:.0e}"] = {"dchi2": d3, "label": label(d3), "bites": d3 > 25, "r_per_z": rsummary(r3)}
            P(f"  M3 M_cl {M:.0e} f_in 1, r_cl x 0.1: dchi2 {d3:.4g} -> {label(d3)} (must FAIL)")
        r2 = G.bracket_i(1e14, 0.0); d2 = dchi2(r2)
        mut["M2"] = {"dchi2": d2, "label": label(d2), "max_abs_r_minus_1": float(np.max(np.abs(r2 - 1))), "bites": d2 <= 4}
        P(f"  M2 f_in 0: dchi2 {d2:.1e}, max|r-1| {mut['M2']['max_abs_r_minus_1']:.1e} -> {label(d2)} (must PASS)")
        ok_all &= mut["M3_1e+14"]["bites"] and mut["M2"]["bites"]
        FR["MUTATE"] = mut
    RES["footings"][foot] = FR

RES["disclosures"] = [
    "bracket (ii) growth exponent read with f = f_b = Omega_b/Omega_m (clustering fraction relative to the mean matter "
    "density that drives expansion); the alternative reading f_b,loc = 1 (p = 1) is reported, not graded",
    "bracket (ii) grows d_b from a = 1/1091 as a^p, ignoring Lambda's late suppression at z 2-4; the whole sightline is "
    "taken inter-clump",
    "d_b(k, 1090) from a second CLASS run (output mTk, z_max_pk 1100, matter_source_in_current_gauge yes: synchronous-gauge "
    "d_b; CLASS refuses mPk with z_pk > z_rec); normalization P = 2 pi^2/k^3 A_s (k/0.05)^(n_s-1) T^2 checked against "
    "pk_lin at z 3",
    "P_lin evaluated by CLASS pk_lin directly at each DESI z (no z interpolation needed); 700 log-k samples splined in ln P",
    "1D integral: trapezoid on 60000 log-k points, 1e-4 to 200 /Mpc; kmax 100 vs 200 reported",
    "covariance: full COVARIANCE (stat + syst) restricted to the 755 bins, cross-z kept (P1D3's primary)",
    "G3 label per M_cl: FAIL only if both brackets FAIL; PASS if either PASSes (frozen rule fixes only the FAIL line)",
    "post-freeze bracket (iii), disclosed (coordinator addition after the freeze): bracket (i)'s formula with the clump "
    "window u evaluated at r = 0.1 Mpc comoving in both W and P_cl, n_cl from the same M_cl; same statistic and labels; "
    "not part of the frozen G3 label (the G3 label uses brackets (i) and (ii) only)",
    "MUTATE M3 bite graded at the primary M_cl 1e14; other M_cl reported",
]
RES["all_checks_pass"] = bool(ok_all)
RES["elapsed_s"] = time.time() - T0
RES["peak_rss_GB_self"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
RES["note"] = NOTE
json.dump(RES, open(os.path.join(HERE, f"nc2_g3{TAG}.json"), "w"), indent=1, default=float)
P(f"\nall checks {'PASS' if ok_all else 'FAIL'}; elapsed {RES['elapsed_s']:.0f} s; peak RSS {RES['peak_rss_GB_self']:.2f} GB; {NOTE}")
sys.exit(0 if ok_all else 1)
