#!/usr/bin/env python3
"""CFG315: the small scales DESI DR1 lensing cut (Heydenreich+25 release, Zenodo 22914838).

Implements campaign_fresh_gravity/CFG315_desi_dr1_lensing/FROZEN_CRITERIA.md (committed dd80cf2a0 before any Delta Sigma value was read).
  (a) cross-survey consistency of the conservative tomographic BGS measurements (KiDS / DES / HSC-Y3) at r_p <= 1 h^-1 Mpc
      under the joint analytic covariance: error-inflation factor s (S1 total, S2 between surveys) vs CFG108's x1.58.
  (b) population RAR via SIS g_obs = 4 G DeltaSigma and the Mistele+24 deprojection at R_phys <= 0.30 Mpc.
  (c) the law with nu_mono, both footings, against the data at those radii; M* from the KiDS-bright LePhare calibration.
Controls C0-C5; MUTATE=1 multiplies every KiDS Delta Sigma by 1.2 (outputs *_MUTATE.*).
Run from the repository root:  python3 campaign_fresh_gravity/CFG315_desi_dr1_lensing/cfg315_run.py   (MUTATE=1 for the control)
Data (outside git): ../_external_data/desi_dr1_lensing/extracted/  and  ../_external_data/kids_lensing_zsplit/ (read-only).
"""
import os, sys, math, json
import numpy as np
from scipy import stats
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
import CFG7_common as C  # noqa: E402
trapz = getattr(np, "trapezoid", None) or np.trapz

MUTATE = os.environ.get("MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
EXT = os.path.join(REPO, "..", "_external_data")
DD = os.path.join(EXT, "desi_dr1_lensing", "extracted")
KIDS_LP = os.path.join(EXT, "kids_lensing_zsplit", "KiDS_DR4_brightsample_LePhare.fits")
OUT = os.path.join(HERE, f"cfg315_run{TAG}.out")
JS = os.path.join(HERE, f"cfg315_results{TAG}.json")
_lines = []
RES = {"mutate": MUTATE, "checks": {}}


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _lines.append(s)


def check(name, detail, ok, gated=True):
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if gated else ' (reported)'} {name}: {detail}")
    RES["checks"][name] = dict(ok=bool(ok), detail=detail, gated=gated)
    return ok


P(__doc__.split("Run from")[0].strip())
if MUTATE:
    P("\n*** MUTATE=1: every KiDS Delta Sigma x 1.2 (covariance unchanged); S2 must flag ***")

H = 0.6766                     # Planck18 h
OM = 0.30966
SURV = {"KiDS": 1, "DES": 2, "HSCY3": 3}
RMAX_OPT = {"KiDS": 1, "DES": 2, "HSCY3": 4}
LENS = {  # name: (sample, zmin, zmax, ilens in the joint covariance, z_mid, conservative combos {survey: [1-based source bins]})
    "BGS1": ("BGS_BRIGHT", 0.1, 0.2, 1, 0.15, {"KiDS": [4, 5], "DES": [3, 4], "HSCY3": [2, 3, 4]}),
    "BGS2": ("BGS_BRIGHT", 0.2, 0.3, 2, 0.25, {"KiDS": [4, 5], "DES": [3, 4], "HSCY3": [2, 3, 4]}),
    "BGS3": ("BGS_BRIGHT", 0.3, 0.4, 3, 0.35, {"KiDS": [4, 5], "DES": [3, 4], "HSCY3": [2, 3, 4]}),
    "LRG1": ("LRG", 0.4, 0.6, 1, 0.5, {"KiDS": [4, 5], "DES": [4], "HSCY3": [3, 4]}),
    "LRG2": ("LRG", 0.6, 0.8, 2, 0.7, {"HSCY3": [3, 4]}),
}
BGS = ["BGS1", "BGS2", "BGS3"]
MR_CUT = {"BGS1": -19.5, "BGS2": -20.5, "BGS3": -21.0}


def chi_com(z, n=2000):
    """comoving distance [h^-1 Mpc], flat LCDM Planck18 (no radiation)"""
    zz = np.linspace(0, z, n)
    return 2997.92458 * trapz(1 / np.sqrt(OM * (1 + zz) ** 3 + 1 - OM), zz)


# ------------------------------------------------------------------ load
def fname(lens, surv, k):
    s, a, b = LENS[lens][:3]
    return os.path.join(DD, "ggl", surv, f"deltasigma_{s}_zmin_{a}_zmax_{b}_lenszbin_{k - 1}_blindA_boost_False.fits")


def load_cov(kind):
    base = os.path.join(DD, "covariances")
    idx = np.loadtxt(os.path.join(base, f"bin_ds_kids1000desy3hscy3_desiy1{kind}.dat"), comments="#")
    raw = np.loadtxt(os.path.join(base, f"dscovcorr_kids1000desy3hscy3_desiy1{kind}_pzwei.dat"), skiprows=1)
    n = len(idx)
    Cm = np.zeros((n, n))
    Cm[raw[:, 0].astype(int) - 1, raw[:, 1].astype(int) - 1] = raw[:, 2]
    key = {(int(r[1]), int(r[2]), int(r[3]), int(r[4])): i for i, r in enumerate(idx)}
    Rk = {(int(r[1]), int(r[2]), int(r[3]), int(r[4])): r[5] for r in idx}
    return Cm, key, Rk


COV = {"bgs": load_cov("bgs"), "lrg": load_cov("lrg")}
rmax_tab = np.loadtxt(os.path.join(DD, "covariances", "rmax_values.dat"), comments="#")

P("\n== C0: formats and units")
c0 = True
for kind, (Cm, key, Rk) in COV.items():
    sym = float(np.max(np.abs(Cm - Cm.T)) / np.max(np.abs(np.diag(Cm))))
    ev = float(np.linalg.eigvalsh(0.5 * (Cm + Cm.T)).min())
    ok = sym < 1e-8 and ev > 0
    c0 &= ok
    P(f"  {kind}: N = {len(Cm)}, max asymmetry / max diag {sym:.1e}, min eigenvalue {ev:.3e} -> {'ok' if ok else 'BAD'}")

DATA = {}
missing = []
rp_dev = 0.0
for L, (s, a, b, il, zm, combos) in LENS.items():
    kind = "bgs" if s.startswith("BGS") else "lrg"
    Cm, key, Rk = COV[kind]
    for sv, ks in combos.items():
        for k in ks:
            f = fname(L, sv, k)
            if not os.path.exists(f):
                missing.append(f); continue
            t = fits.open(f)[1].data
            rp = np.array(t["rp"], float)
            ds = np.array(t["ds"], float)
            mb = np.array(t["magnification_bias"], float)
            if MUTATE and sv == "KiDS":
                ds = ds * 1.2; mb = mb * 1.2
            Rcov = np.array([Rk[(SURV[sv], il, k, i + 1)] for i in range(15)])
            rp_dev = max(rp_dev, float(np.max(np.abs(rp / Rcov - 1))))
            DATA[(L, sv, k)] = dict(rp=rp, ds=ds, mb=mb, err=np.array(t["ds_err"], float), zl=np.array(t["z_l"], float),
                                   cidx=np.array([key[(SURV[sv], il, k, i + 1)] for i in range(15)]), kind=kind)
counts = {L: sum(len(v) for v in LENS[L][5].values()) for L in LENS}
ok = not missing and counts == {"BGS1": 7, "BGS2": 7, "BGS3": 7, "LRG1": 5, "LRG2": 2}
c0 &= ok
P(f"  conservative combinations present: {counts}; missing files {len(missing)}")
c0 &= rp_dev < 0.01
P(f"  index-file R vs FITS rp: max relative deviation {rp_dev:.2e}")


def scale_mask(L, rng):
    s, a, b, il, zm, _ = LENS[L]
    rp = DATA[next(k for k in DATA if k[0] == L)]["rp"]
    thmin = 0.5 / 60 * math.pi / 180
    m = rp / chi_com(zm) >= thmin
    lens_i = il if s.startswith("BGS") else il + 3
    rmax = min(float(rmax_tab[(rmax_tab[:, 0] == RMAX_OPT[sv]) & (rmax_tab[:, 1] == lens_i), 2][0]) for sv in RMAX_OPT)
    m &= rp <= rmax
    if rng == "small": m &= rp <= 1.0
    elif rng == "large": m &= rp > 1.0
    return m, rmax


ratios = []
for (L, sv, k), d in DATA.items():
    if not L.startswith("BGS"): continue
    m, _ = scale_mask(L, "small")
    Cm = COV[d["kind"]][0]
    ratios += list(np.sqrt(np.diag(Cm)[d["cidx"][m]]) / d["err"][m])
med_ratio = float(np.median(ratios))
c0 &= 0.6 <= med_ratio <= 1.6
P(f"  median sqrt(diag C_analytic) / ds_err over used BGS small-scale bins: {med_ratio:.3f} (range {np.min(ratios):.2f}-{np.max(ratios):.2f})")
mbr = []
for (L, sv, k), d in DATA.items():
    if L.startswith("BGS"):
        m, _ = scale_mask(L, "small"); mbr += list(np.abs(d["mb"][m]) / np.abs(d["ds"][m]))
mb_med = float(np.median(mbr))
MB_OK = mb_med <= 0.3
P(f"  magnification_bias column: median |mb|/|ds| at r_p <= 1 (BGS) = {mb_med:.4f} -> variant {'kept' if MB_OK else 'DROPPED (reading wrong)'}")
check("C0 formats/units", f"cov symmetric+PD, counts {counts}, rp match {rp_dev:.1e}, sqrt(diag)/ds_err median {med_ratio:.2f}", c0)
RES["C0"] = dict(counts=counts, rp_dev=rp_dev, sqrtdiag_over_err_median=med_ratio, mb_over_ds_median=mb_med)
for L in LENS:
    for rng in ("small", "large"):
        m, rmax = scale_mask(L, rng)
        rp = DATA[next(k for k in DATA if k[0] == L)]["rp"]
        if rng == "small": P(f"  {L}: R_max {rmax:.1f}; small-scale bins r_p = {np.round(rp[m], 3).tolist()}; large {int(scale_mask(L, 'large')[0].sum())} bins")


# ------------------------------------------------------------------ amplitude machinery
def build(L, rng, use_mb=False, scale=None):
    """stacked data vector, covariance, combo list, radial mask"""
    m, _ = scale_mask(L, rng)
    keys = [(L, sv, k) for sv, ks in LENS[L][5].items() for k in ks]
    Cm = COV[DATA[keys[0]]["kind"]][0]
    ii = np.concatenate([DATA[k]["cidx"][m] for k in keys])
    d = np.concatenate([(DATA[k]["ds"] - (DATA[k]["mb"] if use_mb else 0))[m] for k in keys])
    Cs = Cm[np.ix_(ii, ii)]
    return d, Cs, keys, m


def gls_profile(d, Cs, nc, nb):
    X = np.tile(np.eye(nb), (nc, 1))
    Ci = np.linalg.inv(Cs)
    F = X.T @ Ci @ X
    t = np.linalg.solve(F, X.T @ Ci @ d)
    return t, np.linalg.inv(F)


def amplitudes(d, Cs, keys, m, template="gls", rp=None):
    nc, nb = len(keys), int(m.sum())
    if template == "gls":
        t, _ = gls_profile(d, Cs, nc, nb)
    else:
        t = rp[m] ** -1.0
    Csum = sum(Cs[j * nb:(j + 1) * nb, j * nb:(j + 1) * nb] for j in range(nc))
    w = np.linalg.solve(Csum, t)
    W = np.zeros((nc, nc * nb))
    for j in range(nc):
        W[j, j * nb:(j + 1) * nb] = w / (w @ t)
    A = W @ d
    CA = W @ Cs @ W.T
    sig_j = np.sqrt(np.diag(CA))
    return A, CA, sig_j, t


def gls_mean(A, CA):
    Ci = np.linalg.inv(CA); o = np.ones(len(A))
    mu = (o @ Ci @ A) / (o @ Ci @ o)
    r = A - mu
    return mu, float(r @ Ci @ r)


def between(A, CA, keys):
    groups = [sv for sv in SURV if any(k[1] == sv for k in keys)]
    G = np.array([[1.0 if k[1] == g else 0.0 for g in groups] for k in keys])
    Ci = np.linalg.inv(CA)
    Cm_ = np.linalg.inv(G.T @ Ci @ G)
    mh = Cm_ @ G.T @ Ci @ A
    if len(groups) < 2:
        return groups, mh, Cm_, 0.0, 0
    mu, chi = gls_mean(mh, Cm_)
    return groups, mh, Cm_, chi, len(groups) - 1


def s_ci(chi, dof):
    if dof <= 0: return (float("nan"),) * 3
    return (math.sqrt(chi / dof), math.sqrt(chi / stats.chi2.ppf(0.975, dof)), math.sqrt(chi / stats.chi2.ppf(0.025, dof)))


def run_a(rng, lens_list, template="gls", data_override=None):
    out = {}
    tot = dict(chi1=0.0, dof1=0, chi2=0.0, dof2=0)
    for L in lens_list:
        d, Cs, keys, m = build(L, rng)
        if data_override is not None: d = data_override[L]
        rp = DATA[keys[0]]["rp"]
        A, CA, sj, t = amplitudes(d, Cs, keys, m, template, rp)
        mu, chi1 = gls_mean(A, CA)
        groups, mh, Cmh, chi2_, dof2 = between(A, CA, keys)
        out[L] = dict(A=A.tolist(), sig=sj.tolist(), keys=[f"{k[1]}{k[2]}" for k in keys], mean=mu, chi1=chi1, dof1=len(A) - 1,
                      groups=groups, survey_means=mh.tolist(), survey_sig=np.sqrt(np.diag(Cmh)).tolist(), chi2=chi2_, dof2=dof2,
                      Cmh=Cmh.tolist())
        tot["chi1"] += chi1; tot["dof1"] += len(A) - 1; tot["chi2"] += chi2_; tot["dof2"] += dof2
    tot["p1"] = float(stats.chi2.sf(tot["chi1"], tot["dof1"])) if tot["dof1"] else float("nan")
    tot["p2"] = float(stats.chi2.sf(tot["chi2"], tot["dof2"])) if tot["dof2"] else float("nan")
    tot["s1"] = s_ci(tot["chi1"], tot["dof1"]); tot["s2"] = s_ci(tot["chi2"], tot["dof2"])
    return out, tot


def kids_ratio(res):
    """pooled KiDS survey amplitude relative to the GLS mean of the other surveys (inverse-variance over lens bins)"""
    rs, ws = [], []
    for L, o in res.items():
        if "KiDS" not in o["groups"] or len(o["groups"]) < 2: continue
        g = o["groups"]; mh = np.array(o["survey_means"]); Cmh = np.array(o["Cmh"])
        iK = g.index("KiDS"); io = [i for i in range(len(g)) if i != iK]
        Co = Cmh[np.ix_(io, io)]; Ci = np.linalg.inv(Co); oo = np.ones(len(io))
        wv = Ci @ oo / (oo @ Ci @ oo)
        mo = wv @ mh[io]
        J = np.zeros(len(g)); J[iK] = 1 / mo; J[io] = -mh[iK] / mo ** 2 * wv
        r = mh[iK] / mo; sr = math.sqrt(J @ Cmh @ J)
        rs.append(r); ws.append(1 / sr ** 2)
    rs, ws = np.array(rs), np.array(ws)
    return float(np.sum(rs * ws) / np.sum(ws)), float(1 / math.sqrt(np.sum(ws)))


# ------------------------------------------------------------------ (a)
P("\n== (a) cross-survey consistency (amplitudes A_j = w'd_j / w't, Cov(A) from the full joint covariance)")
RES["a"] = {}
for rng in ("small", "large", "all"):
    for tmpl in ("gls", "powerlaw"):
        res, tot = run_a(rng, BGS, tmpl)
        resL, totL = run_a(rng, ["LRG1", "LRG2"], tmpl)
        RES["a"][f"{rng}_{tmpl}"] = dict(BGS=res, BGS_pooled=tot, LRG=resL, LRG_pooled=totL)
        P(f"\n  -- scales {rng}, template {tmpl}")
        for L in BGS + ["LRG1", "LRG2"]:
            o = (res if L in res else resL)[L]
            P(f"   {L}: A = " + ", ".join(f"{k}:{a:.3f}+-{s:.3f}" for k, a, s in zip(o["keys"], o["A"], o["sig"])))
            P(f"         S1 chi2 {o['chi1']:.2f}/{o['dof1']} (p {stats.chi2.sf(o['chi1'], o['dof1']):.3g}); survey means " +
              ", ".join(f"{g} {mm:.3f}+-{ss:.3f}" for g, mm, ss in zip(o["groups"], o["survey_means"], o["survey_sig"])) +
              (f"; S2 chi2 {o['chi2']:.2f}/{o['dof2']} (p {stats.chi2.sf(o['chi2'], o['dof2']):.3g})" if o["dof2"] else ""))
        for lab, t in (("BGS pooled", tot), ("LRG pooled", totL)):
            P(f"   {lab}: S1 chi2 {t['chi1']:.2f}/{t['dof1']} p {t['p1']:.3g}  s = {t['s1'][0]:.3f} [95%: {t['s1'][1]:.3f}, {t['s1'][2]:.3f}]"
              f" | S2 chi2 {t['chi2']:.2f}/{t['dof2']} p {t['p2']:.3g}  s_between = {t['s2'][0]:.3f} [95%: {t['s2'][1]:.3f}, {t['s2'][2]:.3f}]")
        kr = kids_ratio(res)
        RES["a"][f"{rng}_{tmpl}"]["kids_ratio"] = kr
        P(f"   KiDS / (DES, HSC) amplitude ratio, pooled over BGS bins: {kr[0]:.3f} +- {kr[1]:.3f}")

prim = RES["a"]["small_gls"]["BGS_pooled"]
s1, s2 = prim["s1"], prim["s2"]
A1 = s1[2] < 1.58 and s2[2] < 1.58
A2 = (s1[0] >= 1.58 and s1[1] > 1.25) or (s2[0] >= 1.58 and s2[1] > 1.25)
verdict_a = "A1: x1.58 disfavoured" if A1 else ("A2: excess of CFG108's size present" if A2 else "A3: inconclusive at CFG108's level")
P(f"\n  VERDICT (a) [pooled BGS small scales, GLS template]: s_S1 = {s1[0]:.3f} [{s1[1]:.3f}, {s1[2]:.3f}], "
  f"s_S2 = {s2[0]:.3f} [{s2[1]:.3f}, {s2[2]:.3f}] -> {verdict_a}")
P(f"  CFG314's line f_x < 1.25 (S1 point): {'yes' if s1[0] < 1.25 else 'no'}")
lg = RES["a"]["large_gls"]["BGS_pooled"]["s1"]
check("large-scale S1 95% interval contains 1 (paper: consistent at 2 sigma)", f"s = {lg[0]:.3f} [{lg[1]:.3f}, {lg[2]:.3f}]",
      lg[1] <= 1.0 <= lg[2], gated=False)
RES["verdict_a"] = verdict_a

# ------------------------------------------------------------------ C1: reproduce the paper's sigma_sys
P("\n== C1: the paper's excess-scatter likelihood (eq. 25), conservative tomographic, GLS template")


def sigma_sys_mode(L, rng, use_mb):
    d, Cs, keys, m = build(L, rng, use_mb=use_mb)
    A, CA, sj, t = amplitudes(d, Cs, keys, m, "gls")
    x = A - A.mean()
    ag = np.linspace(-1, 1, 2001); sg = np.linspace(0, 2, 4001)
    V = sj[None, :] ** 2 + sg[:, None] ** 2                        # (ns, n)
    # marginalise A analytically on the fine grid: sum over ag of exp(logL)
    logL = np.empty((len(sg), len(ag)))
    for i in range(len(sg)):
        r = x[None, :] - ag[:, None]
        logL[i] = -0.5 * np.sum(r ** 2 / V[i][None, :] + np.log(V[i])[None, :], axis=1)
    mx = logL.max()
    post = np.exp(logL - mx).sum(axis=1)
    i0 = int(np.argmax(post))
    cdf = np.cumsum(post) / post.sum()
    lo = sg[np.searchsorted(cdf, 0.16)]; hi = sg[np.searchsorted(cdf, 0.84)]
    return float(sg[i0]), float(lo), float(hi)


RES["C1"] = {}
for use_mb in ((True, False) if MB_OK else (False,)):
    tag = "mb-corrected" if use_mb else "uncorrected"
    for L, rng, ref in (("BGS2", "all", 0.077), ("BGS2", "small", 0.102), ("BGS3", "all", 0.052), ("LRG1", "all", 0.068), ("LRG1", "small", 0.089)):
        md, lo, hi = sigma_sys_mode(L, rng, use_mb)
        RES["C1"][f"{tag}_{L}_{rng}"] = dict(mode=md, q16=lo, q84=hi, paper=ref)
        P(f"  {tag:13s} {L} {rng:5s}: sigma_sys mode {md:.3f} (16-84% of the marginal {lo:.3f}-{hi:.3f}); paper {ref:.3f}")
use = "mb-corrected" if MB_OK else "uncorrected"
c1a, c1b = RES["C1"][f"{use}_BGS2_all"]["mode"], RES["C1"][f"{use}_BGS2_small"]["mode"]
check("C1 reproduce sigma_sys BGS2 (0.077 +-0.030 all; 0.102 +-0.040 small)", f"{use}: {c1a:.3f} / {c1b:.3f}",
      abs(c1a - 0.077) <= 0.030 and abs(c1b - 0.102) <= 0.040)

# ------------------------------------------------------------------ C2: shuffled survey labels
P("\n== C2: 2,000 random relabellings of survey membership (group sizes kept), pooled BGS small-scale S2")
rngen = np.random.default_rng(315)
base = {}
for L in BGS:
    d, Cs, keys, m = build(L, "small")
    A, CA, sj, t = amplitudes(d, Cs, keys, m, "gls")
    base[L] = (A, CA, keys)
obs_chi2 = sum(between(*base[L])[3] for L in BGS)
flags, chis = 0, []
for it in range(2000):
    chi = 0.0
    for L in BGS:
        A, CA, keys = base[L]
        perm = rngen.permutation(len(keys))
        keys_p = [(keys[i][0], keys[perm[i]][1], keys[i][2]) for i in range(len(keys))]
        chi += between(A, CA, keys_p)[3]
    chis.append(chi)
    flags += stats.chi2.sf(chi, 6) < 0.01
chis = np.array(chis)
emp_p = float(np.mean(chis >= obs_chi2 - 1e-12))
RES["C2"] = dict(flag_rate=flags / 2000, observed_chi2=obs_chi2, empirical_p=emp_p, null_mean=float(chis.mean()))
check("C2 shuffled-survey false-flag rate <= 5%", f"flag rate {flags / 2000:.3f}; relabelled chi2 mean {chis.mean():.2f} (dof 6); observed S2 chi2 {obs_chi2:.2f}, empirical p {emp_p:.3f}",
      flags / 2000 <= 0.05)

# ------------------------------------------------------------------ C3: Gaussian null mocks
P("\n== C3: 2,000 Gaussian draws from the joint covariance about the GLS profile (pooled BGS small scales)")
prep = {}
for L in BGS:
    d, Cs, keys, m = build(L, "small")
    nb = int(m.sum()); t, _ = gls_profile(d, Cs, len(keys), nb)
    prep[L] = (np.tile(t, len(keys)), np.linalg.cholesky(Cs))
s1sq, a2f = [], 0
for it in range(2000):
    ov = {L: prep[L][0] + prep[L][1] @ rngen.standard_normal(len(prep[L][0])) for L in BGS}
    _, tt = run_a("small", BGS, "gls", data_override=ov)
    s1sq.append(tt["s1"][0] ** 2)
    a2f += (tt["s1"][0] >= 1.58 and tt["s1"][1] > 1.25) or (tt["s2"][0] >= 1.58 and tt["s2"][1] > 1.25)
s1sq = np.array(s1sq)
RES["C3"] = dict(mean_s1sq=float(s1sq.mean()), A2_rate=a2f / 2000, s1_q95=float(np.quantile(np.sqrt(s1sq), 0.95)))
check("C3 null mocks: mean s1^2 in [0.9, 1.1] and A2 rate <= 5%", f"mean s1^2 {s1sq.mean():.3f}; A2 rate {a2f / 2000:.3f}; 95th pct of s1 under the null {np.quantile(np.sqrt(s1sq), 0.95):.3f}",
      0.9 <= s1sq.mean() <= 1.1 and a2f / 2000 <= 0.05)

# ------------------------------------------------------------------ law machinery: projector + C4, C5
G_SI, MSUN, MPC = 6.67430e-11, 1.98892e30, C.MPC_M


def project(r, Md, Rs):
    """Delta Sigma [Msun/Mpc^2] at projected radii Rs of a spherical mass profile Md(<r) (r in Mpc)"""
    dMdr = np.gradient(Md, r); lr = np.log(r); out = np.empty(len(Rs))
    for i, Rp in enumerate(Rs):
        X = math.sqrt(max(r[-1] ** 2 - Rp ** 2, 0.0))
        x = np.concatenate([[0.0], np.geomspace(1e-5 * Rp, X, 1200)])
        rr = np.sqrt(x * x + Rp * Rp)
        dm = np.interp(np.log(rr), lr, dMdr, right=0.0)
        Sig = trapz(dm / rr ** 2, x) / (2 * math.pi)
        Mcyl = np.interp(math.log(Rp), lr, Md) + trapz(dm * (1 - x / rr) * (x / rr), x)
        out[i] = Mcyl / (math.pi * Rp * Rp) - Sig
    return out


def nfw_ds_wb(Rs, M200, c, r200):
    rs = r200 / c; dc = (200.0 / 3) * c ** 3 / (math.log(1 + c) - c / (1 + c))
    rho_c = M200 / (4 / 3 * math.pi * r200 ** 3 * 200.0)
    out = np.empty(len(Rs))
    for i, xi in enumerate(Rs / rs):
        if xi < 1:
            a = math.sqrt((1 - xi) / (1 + xi))
            g = 8 * math.atanh(a) / (xi * xi * math.sqrt(1 - xi * xi)) + 4 / xi ** 2 * math.log(xi / 2) - 2 / (xi * xi - 1) + 4 * math.atanh(a) / ((xi * xi - 1) * math.sqrt(1 - xi * xi))
        else:
            a = math.sqrt((xi - 1) / (1 + xi))
            g = 8 * math.atan(a) / (xi * xi * math.sqrt(xi * xi - 1)) + 4 / xi ** 2 * math.log(xi / 2) - 2 / (xi * xi - 1) + 4 * math.atan(a) / ((xi * xi - 1) ** 1.5)
        out[i] = rs * dc * rho_c * g
    return out


P("\n== C4 / C5: projector and law asymptote")
r_t = np.geomspace(1e-6, 200.0, 6000)
M200, cc, r200 = 1e13, 6.0, 0.4
mf = lambda y: np.log(1 + y) - y / (1 + y)
Mn = M200 * mf(r_t / (r200 / cc)) / mf(cc)
Rt = np.geomspace(0.02, 2.0, 12)
dev = float(np.max(np.abs(project(r_t, Mn, Rt) / nfw_ds_wb(Rt, M200, cc, r200) - 1)))
check("C4 projector vs Wright & Brainerd NFW (<= 1e-3); point mass exact (analytic)", f"max rel. dev {dev:.1e}", dev < 1e-3)

RG3 = np.geomspace(1e-6, 60.0, 3000)
c5 = []
for Mb in (1e10, 1e11):
    a0 = C.A0["canonical"]
    gg = 1e-12
    Rp = math.sqrt(G_SI * Mb * MSUN / gg) / MPC
    ML = np.asarray(C.M_law(Mb, RG3, a0, C.nu_mono), float)
    ds = project(RG3, ML - Mb, np.array([Rp]))[0] + Mb / (math.pi * Rp ** 2)
    sis = math.sqrt(Mb * a0 / C.GMPC) / (4 * Rp)            # Msun/Mpc^2 (a0 in (km/s)^2/Mpc, G in Mpc (km/s)^2/Msun)
    c5.append(abs(ds / sis - 1))
check("C5 law asymptote: untruncated law at g_bar = 1e-12 within 5% of sqrt(M a0/G)/(4R)", f"rel. dev {c5[0]:.3f}, {c5[1]:.3f}", max(c5) < 0.05)


def law_ds(Mb, z, foot, Rs):
    """the framework's Delta Sigma [Msun/pc^2, physical] at physical radii Rs [Mpc]"""
    a0 = C.A0[foot]
    rta = float(C.r_ta_law(Mb, a0, C.nu_mono, 1.0 / (1.0 + z)))
    re = 0.40 * rta
    ML = np.asarray(C.M_law(Mb, np.minimum(RG3, re), a0, C.nu_mono), float)
    return (project(RG3, ML - Mb, Rs) + Mb / (math.pi * Rs ** 2)) / 1e12


# ------------------------------------------------------------------ stellar-mass calibration (KiDS-bright LePhare)
P("\n== Stellar masses (the release has none): KiDS-bright LePhare calibration, read-only")
lp = fits.open(KIDS_LP, memmap=True)[1].data
zK = np.array(lp["REDSHIFT"], float); MK = np.array(lp["MAG_ABS_r"], float); lMK = np.array(lp["MASS_MED"], float)
good = np.isfinite(zK) & np.isfinite(MK) & np.isfinite(lMK) & (lMK > 6) & (lMK < 13) & (MK > -30) & (MK < -10)
P(f"  rows {len(zK)}, usable {int(good.sum())}")
fcold = lambda lm: 10 ** (-0.69 * lm + 6.63)


def dm70(z):
    zz = np.linspace(0, z, 2000)
    dc = 2997.92458 / 0.7 * trapz(1 / np.sqrt(0.3 * (1 + zz) ** 3 + 0.7), zz)
    return 5 * math.log10(dc * (1 + z) * 1e5)


READ = {"i_h1": -0.775, "ii_hPl": +0.074}
MSAMP = {}
for L in BGS:
    s, a, b, il, zm, _ = LENS[L]
    for rd, off in READ.items():
        cut = MR_CUT[L] + off
        sel = good & (zK >= a) & (zK < b) & (MK < cut)
        lm = lMK[sel]
        MSAMP[(L, rd)] = lm
        mb_eff = float(np.mean(np.sqrt(10 ** lm * (1 + fcold(lm)))) ** 2)
        P(f"  {L} reading {rd}: KiDS cut M_r < {cut:.3f}; N = {len(lm)}; median log M* {np.median(lm):.3f}; log M_b,eff = {math.log10(mb_eff):.3f}; "
          f"cut's KiDS apparent mag at z_max (no K-corr) {cut + dm70(b):.2f} (KiDS-bright limit r < 20)")

# per-lens-bin law tables on a log M grid
LMG = np.arange(8.5, 12.51, 0.05)


def pop_pred(L, foot, rd, shift, Rs, z):
    lm = MSAMP[(L, rd)] + shift
    hist, _ = np.histogram(lm, bins=np.append(LMG - 0.025, LMG[-1] + 0.025))
    w = hist / hist.sum()
    out = np.zeros(len(Rs))
    for j, lmj in enumerate(LMG):
        if w[j] == 0: continue
        Mb = 10 ** lmj * (1 + fcold(lmj))
        out += w[j] * law_ds(Mb, z, foot, Rs)
    return out


# ------------------------------------------------------------------ (b) and (c)
P("\n== (b) population RAR and (c) the law at the usable radii (R_phys <= 0.30 Mpc; BGS only; lenses NOT isolated)")
SIG_UNIT = MSUN / (3.0856775814913673e16) ** 2         # Msun/pc^2 -> kg/m^2
RES["b"], RES["c"] = {}, {}
UNITS = {"comoving": lambda rp, ds, z: (rp / (H * (1 + z)), ds * H * (1 + z) ** 2, H * (1 + z) ** 2),
         "physical": lambda rp, ds, z: (rp / H, ds * H, H)}
cfail_count, cexc_count = {}, {}
for uname, conv in UNITS.items():
    for L in BGS:
        s, a, b, il, zm, _ = LENS[L]
        d, Cs, keys, m = build(L, "all")
        rp_all = DATA[keys[0]]["rp"]
        Rph_all = conv(rp_all, rp_all * 0, zm)[0]
        thmin = 0.5 / 60 * math.pi / 180
        U = (Rph_all <= 0.30) & (rp_all / chi_com(zm) >= thmin)
        keysU = keys
        Cm = COV["bgs"][0]
        ii = np.concatenate([DATA[k]["cidx"][U] for k in keysU])
        y = np.concatenate([DATA[k]["ds"][U] for k in keysU])
        CU = Cm[np.ix_(ii, ii)]
        Rph, _, fac = conv(rp_all[U], rp_all[U], zm)
        y = y * fac; CU = CU * fac ** 2
        nb = int(U.sum()); nc = len(keysU)
        prof, Cprof = gls_profile(y, CU, nc, nb)
        gobs = 4 * G_SI * prof * SIG_UNIT; egobs = 4 * G_SI * np.sqrt(np.diag(Cprof)) * SIG_UNIT
        # Mistele+24: g(R) = 4G int_0^{pi/2} DS(R/sin th) dth, log-log interpolation inside, R^-1 tail beyond the last usable bin (MC errors)
        th = np.linspace(1e-4, math.pi / 2, 4000)

        def mistele(pv):
            lp_ = np.log(np.maximum(pv, 1e-30)); lR = np.log(Rph)
            g = []
            for R0 in Rph:
                Rr = R0 / np.sin(th)
                v = np.where(Rr <= Rph[-1], np.exp(np.interp(np.log(Rr), lR, lp_)), pv[-1] * Rph[-1] / Rr)
                g.append(4 * G_SI * trapz(v, th) * SIG_UNIT)
            return np.array(g)
        gm = mistele(prof)
        draws = np.random.default_rng(7).multivariate_normal(prof, Cprof, 500)
        gmd = np.array([mistele(np.abs(x)) for x in draws])
        RES["b"][f"{uname}_{L}"] = dict(R_phys=Rph.tolist(), r_p=rp_all[U].tolist(), DS_phys=prof.tolist(), DS_err=np.sqrt(np.diag(Cprof)).tolist(),
                                        gobs_SIS=gobs.tolist(), gobs_SIS_err=egobs.tolist(), gobs_Mistele=gm.tolist(), gobs_Mistele_err=gmd.std(0).tolist())
        P(f"\n  [{uname} units] {L} (z_mid {zm}): usable r_p {np.round(rp_all[U], 3).tolist()} h^-1 Mpc = R_phys {np.round(Rph, 3).tolist()} Mpc")
        for j in range(nb):
            P(f"     R {Rph[j]:.3f} Mpc: DS {prof[j]:.2f} +- {math.sqrt(Cprof[j, j]):.2f} Msun/pc^2; g_obs SIS {gobs[j]:.3e} +- {egobs[j]:.1e}; Mistele {gm[j]:.3e} +- {gmd.std(0)[j]:.1e} m/s^2")
        for foot in ("canonical", "alt"):
            preds = {}
            for rd in READ:
                for sh in (-0.1, 0.0, 0.1):
                    preds[(rd, sh)] = pop_pred(L, foot, rd, sh, Rph, zm)
            lo_key = min(preds, key=lambda k: preds[k].mean()); hi_key = max(preds, key=lambda k: preds[k].mean())
            Ci = np.linalg.inv(CU)
            row = {}
            for lab, key in (("lowest", lo_key), ("primary", ("i_h1", 0.0)), ("highest", hi_key)):
                mvec = np.tile(preds[key], nc)
                F = mvec @ Ci @ mvec
                Q = float(mvec @ Ci @ y / F); sQ = float(1 / math.sqrt(F))
                chi_1 = float((y - mvec) @ Ci @ (y - mvec)); chi_q = float((y - Q * mvec) @ Ci @ (y - Q * mvec))
                row[lab] = dict(key=list(map(str, key)), pred=preds[key].tolist(), Q=Q, sQ=sQ, chi2_Q1=chi_1, chi2_Qhat=chi_q, dof=len(y))
            # M_b,eff the law would need for Q = 1 (deep-regime sqrt scaling from the primary)
            Qp = row["primary"]["Q"]
            lm = MSAMP[(L, "i_h1")]
            mbeff_p = float(np.mean(np.sqrt(10 ** lm * (1 + fcold(lm)))) ** 2)
            need = math.log10(mbeff_p * Qp ** 2) if Qp > 0 else float("nan")
            # g_bar for the RAR points (primary reading)
            gbar = G_SI * mbeff_p * MSUN / (Rph * MPC) ** 2
            width = math.log10(preds[hi_key].mean() / preds[lo_key].mean())
            RES["c"][f"{uname}_{L}_{foot}"] = dict(rows=row, logMb_eff_primary=math.log10(mbeff_p), logMb_eff_needed_Q1_sqrtscaling=need,
                                                   bracket_width_dex=width, gbar_primary=gbar.tolist())
            P(f"   (c) {foot:9s}: Q = DS_obs/DS_law  lowest-pred {row['lowest']['Q']:.3f} +- {row['lowest']['sQ']:.3f} | primary {row['primary']['Q']:.3f} +- {row['primary']['sQ']:.3f}"
              f" (chi2 at Q=1 {row['primary']['chi2_Q1']:.1f}, at Q^ {row['primary']['chi2_Qhat']:.1f} / {row['primary']['dof']}) | highest-pred {row['highest']['Q']:.3f} +- {row['highest']['sQ']:.3f};"
              f" bracket {width:.2f} dex; log M_b,eff {math.log10(mbeff_p):.2f}, needed for Q=1 ~{need:.2f}")
            P(f"        g_bar (primary) {np.array2string(gbar, precision=2)} m/s^2;  law DS (primary) {np.array2string(preds[('i_h1', 0.0)], precision=2)} Msun/pc^2")
            fail = row["lowest"]["Q"] + 3 * row["lowest"]["sQ"] < 1
            exc = row["highest"]["Q"] - 3 * row["highest"]["sQ"] > 1
            cfail_count[(uname, foot)] = cfail_count.get((uname, foot), 0) + int(fail)
            cexc_count[(uname, foot)] = cexc_count.get((uname, foot), 0) + int(exc)

P("\n  VERDICT (c):")
verdict_c = {}
for foot in ("canonical", "alt"):
    f_both = all(cfail_count[(u, foot)] >= 2 for u in UNITS)
    e_any = {u: cexc_count[(u, foot)] >= 2 for u in UNITS}
    f_any = {u: cfail_count[(u, foot)] >= 2 for u in UNITS}
    if f_both: v = "C-FAIL (both unit readings)"
    elif all(e_any.values()): v = "C-EXCESS (both unit readings)"
    else: v = "C-CONSISTENT / mixed: " + "; ".join(f"{u}: fail-bins {cfail_count[(u, foot)]}, excess-bins {cexc_count[(u, foot)]}" for u in UNITS)
    verdict_c[foot] = v
    P(f"   {foot}: {v}")
RES["verdict_c"] = verdict_c

# ------------------------------------------------------------------ MUTATE requirement
if MUTATE:
    P("\n== MUTATE requirement")
    kr = RES["a"]["small_gls"]["kids_ratio"]
    req = prim["p2"] < 0.01 and abs(kr[0] - 1.2) <= 2 * kr[1] and not A1
    check("MUTATE: S2 p < 0.01 AND KiDS ratio within 1.2 +- 2 sigma AND A1 not issued",
          f"S2 p {prim['p2']:.2e}; KiDS ratio {kr[0]:.3f} +- {kr[1]:.3f}; A1 {'issued' if A1 else 'not issued'}", req)

gated = {k: v for k, v in RES["checks"].items() if v["gated"]}
npass = sum(v["ok"] for v in gated.values())
P(f"\n== SUMMARY: gated checks {npass}/{len(gated)} pass; verdict (a) {verdict_a}; verdict (c) {verdict_c}")
rc = 0 if npass == len(gated) else 1
P(f"exit code {rc}")
open(OUT, "w").write("\n".join(_lines) + "\n")
json.dump(RES, open(JS, "w"), indent=1, default=float)
sys.exit(rc)
