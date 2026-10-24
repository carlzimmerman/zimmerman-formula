#!/usr/bin/env python3
"""ZT4_zstar_outer_lensing: Z-T4 of design Z* (v3s-OC), outer isolated-galaxy lensing on P2's spectroscopic sample.

Criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (8cdfbc843e, committed alone before any script or number).
Test line: rebuild_2026_10_22/Z1_successor_design/TEST_PLAN.md section 2 "Z-T4" (0d1959a4f5).
Run:  OMP_NUM_THREADS=1 nice -n 15 python3 zt4_outer_lensing.py <kids_source_cache_dir> <work_dir> [--mutate]
  <kids_source_cache_dir>: F1's reader cache (as P2). <work_dir>: a COPY of P2's scratch caches (p2_*.npz/pkl/json).
Two sequential processes: phase C (CLASS linear P(k), two-halo tables, K3) and phase S (P2 executed read-only up to its
verdict loop, Z* model, scoring). Outputs: zt4_outer_lensing{,_MUTATE}.out, zt4_outer_lensing_results{,_MUTATE}.json.
--mutate: the data use cross shear in place of tangential (K0 must fail, exit 1).
kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed.
"""
import os, sys, subprocess
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
if not any(a.startswith("--phase=") for a in sys.argv[1:]):
    _base = [sys.executable, os.path.abspath(__file__)] + sys.argv[1:]
    if subprocess.call(_base + ["--phase=C"]) != 0:
        sys.exit(2)
    sys.exit(subprocess.call(_base + ["--phase=S"]))
PHASE = [a for a in sys.argv[1:] if a.startswith("--phase=")][0].split("=")[1]
import json, math, time, resource, io, contextlib, hashlib
import numpy as np
from scipy import special

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
R22 = os.path.join(REPO, "rebuild_2026_10_22")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
MUT = "--mutate" in sys.argv[1:]
SFX = "_MUTATE" if MUT else ""
CACHE, WORK = ARGS[0], ARGS[1]
T0 = time.time()
CRIT = "8cdfbc843e"
FOOTS = ("canonical", "alt")
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FENDS = (5.364, 50.0)
BGS = ("A_c2b_refit", "B_cfg886_bg")
RHO_UNIT = 2.77536627e11                       # Msun/Mpc^3 per unit omega (h^2-free)
EDGES = np.logspace(np.log10(0.03), np.log10(3.0), 16)   # = P2 (Mpc, physical native)
NSUB = 12                                      # = P2 bin_avg
ZT = np.round(np.arange(0.0, 0.5501, 0.025), 4)
OUTL, CHK = [], {}


def P(s=""):
    print(s, flush=True); OUTL.append(str(s))


def check(name, ok, val, thr):
    CHK[name] = bool(ok)
    P(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")


def rss():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9


def tsec():
    return f"[{time.time() - T0:.0f} s, RSS {rss():.2f} GB]"


def sub_points(edges):
    """P2's bin_avg sub-points (12 log points per bin) and R^2 weights."""
    lr = np.log(edges); nb = len(edges) - 1
    sub = np.concatenate([np.exp(lr[b] + (np.arange(NSUB) + 0.5) / NSUB * (lr[b + 1] - lr[b])) for b in range(nb)])
    return sub, sub.reshape(nb, NSUB) ** 2


# ---------------------------------------------------------------- Hankel J2 integral on a log k grid
KF = np.geomspace(1e-5, 1e3, 400_000)          # frozen: 4e5 log-spaced points, 1/Mpc
LNK = np.log(KF)
WTRAP = np.empty_like(LNK); d_ = np.diff(LNK); WTRAP[0] = d_[0] / 2; WTRAP[-1] = d_[-1] / 2; WTRAP[1:-1] = (d_[1:] + d_[:-1]) / 2


def j2_proj(Pk, Rc):
    """int k dk/(2 pi) P(k) J2(k R), R comoving Mpc (array); trapezoid in ln k."""
    base = KF * KF * Pk * WTRAP / (2 * math.pi)
    out = np.empty(len(Rc))
    for i, R in enumerate(Rc):
        x = KF * R
        out[i] = np.dot(base, 2 * special.j1(x) / x - special.j0(x))
    return out


TWOH = os.path.join(WORK, f"zt4_twohalo{SFX}.npz")
K3J = os.path.join(WORK, f"zt4_phaseC{SFX}.json")

# ======================================================================== phase C: CLASS, two-halo tables, K3
if PHASE == "C":
    from classy import Class
    P(f"ZT4_zstar_outer_lensing phase C{'  [MUTATE]' if MUT else ''}   criteria {CRIT}   kappa = 1/2 FITTED")
    f3 = json.load(open(os.path.join(R22, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]
    lines = []; res = {"K3": {}}
    # (b) Hankel machinery vs the analytic Gaussian case
    s_ = 0.2; Rt = np.array([0.4, 1.0, 3.0]); xg = Rt ** 2 / (4 * s_ ** 2)
    num = j2_proj(np.exp(-(KF * s_) ** 2), Rt); ana = (1 - np.exp(-xg) * (1 + xg)) / (math.pi * Rt ** 2)
    k3b = float(np.max(np.abs(num / ana - 1)))
    sub, wts = sub_points(EDGES)
    KS = np.geomspace(1e-4, 50.0, 1500)        # h/Mpc (F3's sigma8 grid)
    W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    LGM = np.round(np.arange(9.0, 14.51, 0.05), 3)
    tabs = {}; k3a = 0.0
    for bg in BGS:
        p = f3[bg]["params"]; h = p["h"]
        c = Class(); c.set({"omega_b": p["omega_b"], "omega_cdm": p["omega_cdm"], "h": h, "ln10^{10}A_s": p["lnAs"],
                            "n_s": p["n_s"], "tau_reio": p["tau"], "N_ur": 3.044, "T_cmb": 2.7255, "output": "mPk",
                            "P_k_max_h/Mpc": 60.0, "z_max_pk": 0.6})
        c.compute()
        Pk0h = np.array([c.pk_lin(k * h, 0.0) for k in KS]) * h ** 3
        s8_own = math.sqrt(np.trapz(Pk0h * W8(KS * 8.0) ** 2 * KS ** 2, KS) / (2 * math.pi ** 2))
        s8_cl = c.sigma8(); s8_f3 = f3[bg]["sigma8"]
        k3a = max(k3a, abs(s8_own / s8_cl - 1), abs(s8_cl / s8_f3 - 1))
        kc = np.geomspace(1e-5, 60.0 * h * 0.999, 1500)       # 1/Mpc, CLASS range
        rho_c0 = p["omega_cdm"] * RHO_UNIT; rho_m0 = (p["omega_cdm"] + p["omega_b"]) * RHO_UNIT
        DS = np.empty((len(ZT), 15)); LNSIG = np.empty((len(ZT), len(LGM)))
        RL = (3 * 10 ** LGM / (4 * math.pi * rho_m0)) ** (1 / 3)   # comoving Lagrangian radius, Mpc
        for iz, z in enumerate(ZT):
            pc = np.array([c.pk_lin(k, z) for k in kc])
            ld = kc > kc[-1] / 10
            sl = np.polyfit(np.log(kc[ld]), np.log(pc[ld]), 1)          # last decade (log-log), extrapolation slope
            lp = np.interp(LNK, np.log(kc), np.log(pc))
            hi = KF > kc[-1]; lp[hi] = np.log(pc[-1]) + sl[0] * (LNK[hi] - math.log(kc[-1]))
            Pf = np.exp(lp)
            ds = j2_proj(Pf, sub * (1 + z)) * rho_c0 * (1 + z) ** 2 / 1e12      # Msun/pc^2, b = 1
            DS[iz] = np.sum(ds.reshape(15, NSUB) * wts, 1) / np.sum(wts, 1)
            ks_, Ps_, ws_ = KF[::20], Pf[::20], WTRAP[::20] * 20       # sigma(M): every 20th point is ample
            xr = ks_[None, :] * RL[:, None]
            Wt = np.where(xr < 1e-3, 1 - xr ** 2 / 10, 3 * (np.sin(xr) - xr * np.cos(xr)) / np.maximum(xr, 1e-300) ** 3)
            LNSIG[iz] = 0.5 * np.log(np.sum(ks_[None, :] ** 3 * Ps_[None, :] * Wt ** 2 * ws_[None, :], 1) / (2 * math.pi ** 2))
            del xr, Wt
        tabs[bg] = dict(DS=DS, LNSIG=LNSIG, s8_own=s8_own, s8_class=s8_cl, s8_f3=s8_f3, ext_slope=float(sl[0]))
        P(f"  [{bg}] sigma8 own {s8_own:.5f} CLASS {s8_cl:.5f} F3 {s8_f3:.5f}; two-halo (b = 1) at z 0.225, O1/O2 bins: "
          + " ".join(f"{x:.3f}" for x in DS[9][(np.sqrt(EDGES[1:] * EDGES[:-1]) > 0.4)]) + f"  {tsec()}")
        c.struct_cleanup(); c.empty(); del c
    check("K3_two_halo_machinery", k3a <= 1e-3 and k3b <= 1e-4,
          f"sigma8 max rel dev {k3a:.1e}; J2 Gaussian test {k3b:.1e}", "<=1e-3 and <=1e-4")
    lines = list(OUTL)
    np.savez(TWOH, ZT=ZT, LGM=LGM, **{f"{bg}_DS": tabs[bg]["DS"] for bg in BGS}, **{f"{bg}_LNSIG": tabs[bg]["LNSIG"] for bg in BGS})
    json.dump(dict(lines=lines, checks={"K3_two_halo_machinery": CHK["K3_two_halo_machinery"]},
                   K3=dict(sigma8=k3a, j2_gauss=k3b, per_bg={bg: {k: v for k, v in tabs[bg].items() if k not in ("DS", "LNSIG")} for bg in BGS}),
                   peak_RSS_GB=rss(), runtime_s=time.time() - T0), open(K3J, "w"))
    print(f"  phase C done: peak RSS {rss():.2f} GB, {time.time() - T0:.0f} s", flush=True)
    sys.exit(0)

# ======================================================================== phase S: P2 replay, Z* model, scoring
PC_ = json.load(open(K3J))
for _l in PC_["lines"]:
    P(_l)
CHK.update(PC_["checks"])
TW = np.load(TWOH)
# ---- execute P2 read-only up to its verdict loop
P2DIR = os.path.join(R22, "P2_spec_isolated_lensing")
P2PY = os.path.join(P2DIR, "p2_spec_isolated_lensing.py")
src = open(P2PY).read()
assert hashlib.sha256(src.encode()).hexdigest().startswith("8420630a1cc5970e")
cut = src.index("VER = {}; AMP = {}")
NS = {"__file__": P2PY, "__name__": "p2_exec"}
_argv = sys.argv[:]
sys.argv = [P2PY, CACHE, WORK, "--phase=B"]
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(compile(src[:cut], P2PY, "exec"), NS)
sys.argv = _argv
p2lines = buf.getvalue().splitlines()
P(f"  P2 executed read-only to its verdict loop ({len(p2lines)} lines); P2 checks in this replay: "
  + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in NS["CHK"].items()) + f"  {tsec()}")
P2J = json.load(open(os.path.join(P2DIR, "p2_spec_isolated_lensing_results.json")))
if MUT:
    NS["MEAS"]["WG"] = NS["MEAS"]["WX"].copy()                    # cross shear as data
AQ = NS["AQ"]; stack = NS["stack"]; amps = NS["amps"]; SETS = NS["SETS"]; NL = NS["NL"]
L3 = NS["L3"]; I3 = SETS["I3"]; L1 = SETS["L"]; I1 = SETS["I1"]
idxS1, idxS3 = NS["idxS1"], NS["idxS3"]; lM70 = NS["lM70"]; z_g = NS["z_g"]
RCEN = NS["RCEN"]; RANGE = NS["RANGE"]; NP_ = NS["NP_"]
OUTER = RANGE["out"]; INNER = RANGE["in"]; ALL = np.ones(15, bool)
assert np.allclose(NS["EDGES"], EDGES) and NS["NSUB"] == NSUB


def cov_of(st):
    dj = st["dj"]
    return (NP_ - 1) / NP_ * (dj - dj.mean(0)).T @ (dj - dj.mean(0))


def chi2(d, m, cov, mask, hartlap=True):
    r = (np.asarray(d) - np.asarray(m))[mask]; C = np.asarray(cov)[np.ix_(mask, mask)]
    hf = (NP_ - mask.sum() - 2) / (NP_ - 1) if hartlap else 1.0
    return float(hf * r @ np.linalg.solve(C, r))


def chi2_diag(d, m, cov, mask):
    r = (np.asarray(d) - np.asarray(m))[mask]
    return float(np.sum(r ** 2 / np.diag(np.asarray(cov))[mask]))


# ---- K0: P2 replay vs the committed JSON
K0 = {}; k0ok = all(P2J["checks"].values())
for foot in FOOTS:
    sa = NS["primary"](foot, "a"); sb = NS["primary"](foot, "b")
    pj = P2J["verdict"][foot]["profile"]
    devs = []
    for mine, key in ((sa["d"], "d"), (np.sqrt(sa["var"]), "sig"), (sa["m"], "m_a"), (sb["m"], "m_b")):
        ref = np.array(pj[key]); devs.append(float(np.max(np.abs(mine - ref)) / np.max(np.abs(ref))))
    cj = chi2(pj["d"], pj["m_a"], pj["cov"], OUTER); cm = chi2(sa["d"], sa["m"], cov_of(sa), OUTER)
    K0[foot] = dict(profile_dev=max(devs), chi2_v3a_json=cj, chi2_v3a_replay=cm, chi2_rel=abs(cm / cj - 1))
    k0ok &= max(devs) <= 1e-9 and abs(cm / cj - 1) <= 1e-6
check("K0_P2_replay", k0ok, "; ".join(f"{f}: profile dev {K0[f]['profile_dev']:.1e}, outer chi2 v3(a) JSON {K0[f]['chi2_v3a_json']:.4f} "
                                       f"replay {K0[f]['chi2_v3a_replay']:.4f}" for f in FOOTS) + f"; P2 committed checks all true {all(P2J['checks'].values())}",
      "<=1e-9, <=1e-6")
P(f"  {tsec()}")

# ======================================================================== Z* model pieces
RGRID_PC = NS["RGRID_PC"]; LMG = NS["LMG"]; bin_avg = NS["bin_avg"]; meff_lens = NS["meff_lens"]
SG = NS["SG"]; UGR, VGR = NS["UGR"], NS["VGR"]; mc_table = NS["mc_table"]
LMB_T = NS["LMB_T"]; DGR = NS["DGR"]; NSUBB = NS["NSUBB"]; G_SI, MSUN, MPC = NS["G_SI"], NS["MSUN"], NS["MPC"]
from scipy.interpolate import RegularGridInterpolator


def town_table_Z(foot, f):
    """T_own,Z[lMG, bin]: P2's y_e = 0 profile capped at (1+f) M_b (constant tail once the cap is reached)."""
    tab = np.empty((len(LMG), 15)); capviol = 0.0; eqviol = 0.0
    for gi, lm in enumerate(LMG):
        lm70 = lm - 2 * np.log10(0.70 / NS["H0N"])
        lmc = lm + (-0.69 * lm70 + 6.63)
        Miso, _t = meff_lens(foot, lm, lmc, 0.5 * 10 ** lm, 0.0)
        Mb = 10 ** lm + 10 ** lmc + 0.5 * 10 ** lm
        M = np.minimum(Miso, (1 + f) * Mb)
        tail = "const" if np.any(Miso >= (1 + f) * Mb) else "linear"
        capviol = max(capviol, float(np.max(M / ((1 + f) * Mb))) - 1)
        below = Miso < (1 + f) * Mb
        eqviol = max(eqviol, float(np.max(np.abs(M[below] - Miso[below]))) if below.any() else 0.0)
        tab[gi] = bin_avg(EDGES * 1e6, lambda R: AQ.delta_sigma(R, RGRID_PC, M, tail))
    return tab, capviol, eqviol


def town_lens_Z(tab, lens_g):
    lm = NS["lMs_nat"](lM70[lens_g], z_g[lens_g], NS["H0N"])
    gx = np.clip((lm - LMG[0]) / (LMG[1] - LMG[0]), 0, len(LMG) - 1.001); i0 = gx.astype(int); fx = gx - i0
    return (1 - fx)[:, None] * tab[i0] + fx[:, None] * tab[i0 + 1]


def ext_profile_m(mfull):
    """= P2 ext_profile with m(s) given (dimensionless M/M_b on SG); tail constant once capped, else linear."""
    m = mfull - 1.0
    capped = np.any(np.diff(mfull[-50:]) == 0)
    lr = np.log(SG); dMdr = np.gradient(m, lr) / SG
    tl = 0.0 if capped else dMdr[-1]
    ch = np.cosh(AQ.TT); sh = np.sinh(AQ.TT); th_ = np.tanh(AQ.TT)
    w = np.full(AQ.TT.size, AQ.TT[1] - AQ.TT[0]); w[0] *= 0.5; w[-1] *= 0.5
    Sig = np.empty(SG.size); Mcyl = np.empty(SG.size)
    for c0 in range(0, SG.size, 100):
        R = SG[c0:c0 + 100]
        r = R[:, None] * ch[None, :]
        fv = np.interp(np.log(r), lr, dMdr, left=dMdr[0], right=tl)
        Mcyl[c0:c0 + 100] = np.interp(np.log(R), lr, m) + np.sum(fv * (1 - th_) * R[:, None] * sh * w, axis=1)
        Sig[c0:c0 + 100] = np.sum(fv / ch * w, axis=1) / (2 * math.pi * R)
    return 2 * math.pi * SG ** 2 * Sig, Mcyl


def gtables_Z(f):
    """neighbour extended-part tables for the capped profile, both footings: {foot: (types, 15, len(DGR))}."""
    mfull = np.minimum(AQ.M_iso(SG), 1 + f)
    fS, Mcyl = ext_profile_m(mfull)
    MCT = mc_table(fS, Mcyl)
    mci = RegularGridInterpolator((np.log(UGR), np.log(VGR)), np.log(np.maximum(MCT, 1e-300)), bounds_error=False, fill_value=None)
    del MCT
    out = {}
    for foot in FOOTS:
        G = np.empty((len(LMB_T), 15, len(DGR)))
        for ti, lmb in enumerate(LMB_T):
            Mb = 10 ** lmb
            rM = math.sqrt(G_SI * Mb * MSUN / A0[foot]) / MPC
            for k in range(15):
                R1, R2 = EDGES[k], EDGES[k + 1]
                Rs = np.exp(np.linspace(np.log(R1), np.log(R2), NSUBB))
                uu = np.repeat(Rs / rM, len(DGR)); vv = np.maximum(np.tile(DGR / rM, NSUBB), VGR[0])
                Mc = np.exp(mci(np.c_[np.log(uu), np.log(vv)])).reshape(NSUBB, len(DGR))
                hstep = (np.log(R2) - np.log(R1)) / (NSUBB - 1)
                wS = np.ones(NSUBB); wS[1:-1:2] = 4; wS[2:-1:2] = 2; wS *= hstep / 3
                G[ti, k] = Mb * (2 * np.sum(Mc * wS[:, None], axis=0) - (Mc[-1] - Mc[0])) / (math.pi * ((R2 * 1e6) ** 2 - (R1 * 1e6) ** 2))
        out[foot] = G
    return out


PCp, PJp, PDp = NS["PC"], NS["PJ"], NS["PD"]; tix = NS["tix"]; MBN_g = NS["MBN_g"]; point_part = NS["point_part"]
NCEN = len(NS["CEN"]["ra"])


def tnbr_Z(G_):
    """= P2 tnbr at a fixed profile (no y_e interpolation)."""
    out = np.zeros((NCEN, 15))
    for c0 in range(0, len(PCp), 8000):
        s = np.arange(c0, min(len(PCp), c0 + 8000))
        pd_ = PDp[s].astype(float)
        gd = np.clip((np.log(np.maximum(pd_, DGR[0])) - np.log(DGR[0])) / (np.log(DGR[1]) - np.log(DGR[0])), 0, len(DGR) - 1.001)
        d0 = gd.astype(np.int64); fd = (gd - d0)[:, None]
        t = tix[PJp[s]]
        contrib = (1 - fd) * G_[t, :, d0] + fd * G_[t, :, d0 + 1] + point_part(MBN_g[PJp[s]], pd_)
        for k in range(15):
            out[:, k] += np.bincount(PCp[s], contrib[:, k], NCEN)
    return out


# ---- two-halo per lens row (S1 superset), b = 1 and Sheth-Tormen (reported)
zl = z_g[idxS1]
iz = np.clip(np.searchsorted(ZT, zl, "right") - 1, 0, len(ZT) - 2); tz = (zl - ZT[iz]) / (ZT[iz + 1] - ZT[iz])
TWO = {bg: (1 - tz)[:, None] * TW[f"{bg}_DS"][iz] + tz[:, None] * TW[f"{bg}_DS"][iz + 1] for bg in BGS}
lMb_l = NS["lMb_g"][idxS1]
LGM = TW["LGM"]


def b_st(bg, f):
    lm = np.clip(lMb_l + np.log10(1 + f), LGM[0], LGM[-1])
    LS = TW[f"{bg}_LNSIG"]
    s0 = np.array([np.interp(lm[i], LGM, LS[iz[i]]) for i in range(len(lm))])
    s1 = np.array([np.interp(lm[i], LGM, LS[iz[i] + 1]) for i in range(len(lm))])
    sig = np.exp((1 - tz) * s0 + tz * s1)
    a, p, dc = 0.707, 0.3, 1.686
    an2 = a * (dc / sig) ** 2
    return 1 + (an2 - 1) / dc + 2 * p / dc / (1 + an2 ** p)


# ---- K2: cap identity (point mass, closed form)
k2pt = max(abs(float(AQ.nu_simple(1.0 / (f * (f + 1)))) - (1 + f)) for f in FENDS)

# ---- build Z* models
TOWN_Z, TN_Z = {}, {}
capv = 0.0; eqv = 0.0
for f in FENDS + (1e7,):
    for foot in FOOTS:
        tab, cv, ev = town_table_Z(foot, f)
        TOWN_Z[(foot, f)] = tab; capv = max(capv, cv); eqv = max(eqv, ev)
    G = gtables_Z(f)
    for foot in FOOTS:
        TN_Z[(foot, f)] = tnbr_Z(G[foot])
    del G
    P(f"  Z* tables f = {f:g} ready  {tsec()}")
check("K2_cap_identity", k2pt <= 1e-12 and capv <= 1e-12 and eqv == 0.0,
      f"point mass |nu(r_s) - (1+f)| {k2pt:.1e}; extended max M_Z/((1+f)M_b) - 1 {capv:.1e}; M_Z = M_iso below the cap (max dev {eqv:.1e})",
      "<=1e-12, <=1e-12, 0")

# ---- K1: untruncated limit
k1 = {}
for foot in FOOTS:
    ref = NS["TOWN"][(foot, "central")][:, 0, :]
    k1t = float(np.max(np.abs(TOWN_Z[(foot, 1e7)] / ref - 1)))
    sa = NS["primary"](foot, "a")
    mod = TN_Z[(foot, 1e7)].copy(); mod[:NL] += town_lens_Z(TOWN_Z[(foot, 1e7)], idxS1)
    st = stack([(L3, +1, mod), (I3, -1, mod)])
    k1m = float(np.max(np.abs(st["m"] - sa["m"])) / np.max(np.abs(sa["m"])))
    k1[foot] = dict(town=k1t, model=k1m)
check("K1_untruncated_limit", all(v["town"] <= 1e-3 and v["model"] <= 1e-3 for v in k1.values()),
      "; ".join(f"{f}: T_own table {v['town']:.1e}, stacked model {v['model']:.1e}" for f, v in k1.items()), "<=1e-3")


# ---- scoring
def model_rows(foot, f, bg=None, bias=None, nbr=True):
    mod = TN_Z[(foot, f)].copy() if nbr else np.zeros((NCEN, 15))
    lens = town_lens_Z(TOWN_Z[(foot, f)], idxS1)
    if bg is not None:
        lens = lens + (TWO[bg] if bias is None else TWO[bg] * bias[:, None])
    mod[:NL] += lens
    return mod


RES = {"lane": "ZT4_zstar_outer_lensing", "criteria": CRIT, "test_plan": "0d1959a4f5", "mutate": MUT,
       "K0": K0, "K1": k1, "K2": dict(point=k2pt, cap=capv, eq=eqv), "K3": PC_["K3"]}
TAB = {}; REP = {}; posdef = True; finite = True
for foot in FOOTS:
    sa = NS["primary"](foot, "a"); cov = cov_of(sa); d = sa["d"]; ma = sa["m"]
    try:
        np.linalg.cholesky(cov[np.ix_(OUTER, OUTER)])
    except np.linalg.LinAlgError:
        posdef = False
    c_a = chi2(d, ma, cov, OUTER); c_a15 = chi2(d, ma, cov, ALL); c_ain = chi2(d, ma, cov, INNER); c_ad = chi2_diag(d, ma, cov, OUTER)
    s1a = NS["primary"](foot, "a", sample="S1"); cov1 = cov_of(s1a); c1_a = chi2(s1a["d"], s1a["m"], cov1, OUTER)
    TAB[foot] = {"chi2_v3a_outer": c_a}; REP[foot] = {"v3a": dict(chi2_15=c_a15, chi2_inner=c_ain, chi2_diag_outer=c_ad,
                                                               chi2_S1_outer=c1_a, amps=amps(sa), m=ma.tolist())}
    for f in FENDS:
        mdl_no2h = model_rows(foot, f)
        st0 = stack([(L3, +1, mdl_no2h), (I3, -1, mdl_no2h)])
        REP[foot][f"f{f:g}_no2h"] = dict(dchi2_outer=chi2(d, st0["m"], cov, OUTER) - c_a, m=st0["m"].tolist(), amps=amps(st0))
        for bg in BGS:
            mdl = model_rows(foot, f, bg)
            st = stack([(L3, +1, mdl), (I3, -1, mdl)])
            cz = chi2(d, st["m"], cov, OUTER); finite &= math.isfinite(cz)
            TAB[foot][f"f{f:g}|{bg}"] = dict(chi2=cz, dchi2=cz - c_a, m=st["m"].tolist())
            rep = dict(dchi2_15=chi2(d, st["m"], cov, ALL) - c_a15, dchi2_inner=chi2(d, st["m"], cov, INNER) - c_ain,
                       dchi2_diag_outer=chi2_diag(d, st["m"], cov, OUTER) - c_ad, amps=amps(st))
            mn = model_rows(foot, f, bg, nbr=False); stn = stack([(L3, +1, mn), (I3, -1, mn)])
            rep["dchi2_outer_2h_no_Tnbr"] = chi2(d, stn["m"], cov, OUTER) - c_a
            bst = b_st(bg, f); ms = model_rows(foot, f, bg, bias=bst); sts = stack([(L3, +1, ms), (I3, -1, ms)])
            rep["b_ST_S3_median"] = float(np.median(bst[np.isin(idxS1, idxS3)])); rep["dchi2_outer_bST"] = chi2(d, sts["m"], cov, OUTER) - c_a
            st1 = stack([(L1, +1, mdl), (I1, -1, mdl)]); rep["dchi2_S1_outer"] = chi2(s1a["d"], st1["m"], cov1, OUTER) - c1_a
            REP[foot][f"f{f:g}|{bg}"] = rep
check("K4_statistic", posdef and finite, f"outer 7x7 jackknife covariance positive definite {posdef}; all chi2 finite {finite}", "both")

# ---- verdicts
VER = {}
for foot in FOOTS:
    vals = [TAB[foot][f"f{f:g}|{bg}"]["dchi2"] for f in FENDS for bg in BGS]
    v = "PASS" if all(x <= 4 for x in vals) else ("FAIL" if all(x >= 9 for x in vals) else "UNDECIDED")
    VER[foot] = v
LANE = "PASS" if all(v == "PASS" for v in VER.values()) else ("FAIL" if all(v == "FAIL" for v in VER.values()) else
       ("UNDECIDED" + ("" if len(set(VER.values())) == 1 else " (footing split)")))

# ---- print
P(f"\n  Z-T4 outer lensing (S3, Delta = L - I3; outer 0.4 < R <= 3 Mpc, 7 bins, jackknife cov + Hartlap {(NP_ - 9) / (NP_ - 1):.3f})")
P("  R (Mpc)        " + " ".join(f"{r:7.3f}" for r in RCEN[OUTER]))
for foot in FOOTS:
    sa_d = np.array(NS["primary"](foot, "a")["d"])
    P(f"  [{foot}] Delta          " + " ".join(f"{x:7.3f}" for x in sa_d[OUTER]))
    P(f"  [{foot}] v3 (a) y_e = 0 " + " ".join(f"{x:7.3f}" for x in np.array(REP[foot]['v3a']['m'])[OUTER]) + f"   chi2 {TAB[foot]['chi2_v3a_outer']:.2f}")
    for f in FENDS:
        P(f"  [{foot}] Z* f={f:<6g} no 2h " + " ".join(f"{x:7.3f}" for x in np.array(REP[foot][f'f{f:g}_no2h']['m'])[OUTER])
          + f"   dchi2 {REP[foot][f'f{f:g}_no2h']['dchi2_outer']:+.2f} (reported)")
        for bg in BGS:
            t = TAB[foot][f"f{f:g}|{bg}"]
            P(f"  [{foot}] Z* f={f:<6g} {bg[:1]}    " + " ".join(f"{x:7.3f}" for x in np.array(t['m'])[OUTER]) + f"   dchi2 {t['dchi2']:+.2f}")
    P(f"  VERDICT [{foot}]: {VER[foot]}")
P(f"\n  LANE VERDICT (Z-T4, both footings): {LANE}")
P("\n  REPORTED (not verdict lines)")
for foot in FOOTS:
    for f in FENDS:
        for bg in BGS:
            r = REP[foot][f"f{f:g}|{bg}"]
            P(f"   [{foot}] f {f:g} {bg[:1]}: dchi2 15-bin {r['dchi2_15']:+.2f}, inner {r['dchi2_inner']:+.2f}, diag outer {r['dchi2_diag_outer']:+.2f}, "
              f"2h without T_nbr {r['dchi2_outer_2h_no_Tnbr']:+.2f}, b_ST (S3 median {r['b_ST_S3_median']:.2f}) {r['dchi2_outer_bST']:+.2f}, "
              f"S1 outer {r['dchi2_S1_outer']:+.2f}; A_O1 {r['amps']['A_O1']:.2f}+-{r['amps']['sA_O1']:.2f} A_O2 {r['amps']['A_O2']:.2f}+-{r['amps']['sA_O2']:.2f}")
    va = REP[foot]["v3a"]["amps"]
    P(f"   [{foot}] v3 (a): A_O1 {va['A_O1']:.2f}+-{va['sA_O1']:.2f} A_O2 {va['A_O2']:.2f}+-{va['sA_O2']:.2f}; chi2 outer {TAB[foot]['chi2_v3a_outer']:.2f}, "
      f"15-bin {REP[foot]['v3a']['chi2_15']:.2f}, inner {REP[foot]['v3a']['chi2_inner']:.2f}, S1 outer {REP[foot]['v3a']['chi2_S1_outer']:.2f}")
lmb_med = float(np.median(NS["lMb_g"][idxS3]))
RS = {}
for foot in FOOTS:
    rM = math.sqrt(G_SI * 10 ** lmb_med * MSUN / A0[foot]) / (MPC / 1e3)
    RS[foot] = {f"{f:g}": rM * math.sqrt(f * (f + 1)) for f in FENDS}; RS[foot]["r_M_kpc"] = rM
    P(f"   [{foot}] median S3 lens log M_b {lmb_med:.2f}: r_M {rM:.1f} kpc; r_s(5.364) {RS[foot]['5.364']:.0f} kpc, r_s(50) {RS[foot]['50']:.0f} kpc")
P(f"   two-halo (b = 1) at z 0.225, outer bins, A: " + " ".join(f"{x:.3f}" for x in TW[f'{BGS[0]}_DS'][9][OUTER])
  + "; B: " + " ".join(f"{x:.3f}" for x in TW[f'{BGS[1]}_DS'][9][OUTER]))
pkS = rss(); pkC = PC_["peak_RSS_GB"]
check("K5_resources", pkS < 1.0 and pkC < 1.0, f"peak RSS phase C {pkC:.2f} GB, phase S {pkS:.2f} GB", "<1 GB each")
RES.update(dict(table=TAB, verdict=VER, lane_verdict=LANE, reported=REP, r_s_median_lens_kpc=RS, median_lMb_S3=lmb_med,
                checks=CHK, peak_RSS_GB=dict(C=pkC, S=pkS), runtime_s=dict(C=PC_["runtime_s"], S=time.time() - T0)))
npass = sum(CHK.values()); nck = len(CHK)
P(f"\nZT4_ZSTAR_OUTER_LENSING COMPLETE: {npass}/{nck} checks PASS.  kappa = 1/2 FITTED; footings never pooled; not theory closed.")


def _js(o):
    if isinstance(o, dict): return {str(k): _js(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_js(v) for v in o]
    if isinstance(o, (np.floating, np.integer, np.bool_)): return o.item()
    if isinstance(o, np.ndarray): return _js(o.tolist())
    if isinstance(o, float) and not math.isfinite(o): return None
    return o


json.dump(_js(RES), open(os.path.join(HERE, f"zt4_outer_lensing_results{SFX}.json"), "w"), indent=1)
open(os.path.join(HERE, f"zt4_outer_lensing{SFX}.out"), "w").write("\n".join(OUTL) + "\n")
sys.exit(0 if npass == nck else 1)
