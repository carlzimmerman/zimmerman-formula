#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR28 -- CAN THE OUTSKIRTS OF GALAXY CLUSTERS MEASURE THE CHAIN'S BAND-PASS LENGTH L?  A secondary-infall (shell) model of
cluster outskirts in the chain's law -- baryons feeling the band-passed MOND phantom, the two-phase dark sector feeling
Newtonian gravity only -- scored against the published splashback radii and slopes of stacked weak lensing and galaxy
counts, with an LCDM control computed by the same machinery, both a0 footings, L0 = L(z = 0) over 0.5-5 Mpc and L = oo.

THE CHAIN'S LAW HERE.  FP6/FP9's band-pass chi = (S_xi - S_L) phi: the MOND scalar reads the baryons' band-passed field and
its output is band-passed again, so every isolated system is Gauss-compensated (FP6 G6e: the phantom's monopole vanishes
beyond ~2L).  L(z) = L0 [Omega_L(z)/Omega_L(0)] (n = 2).  H_Y (FP9): L0 = 2.46 Omega_L(0) = 1.688 Mpc.  H_S (FP13, ill-posed as
written per XR18, FP19 repairing): L0 = 1.87-3.25 Mpc from its committed readouts.  Baryons (galaxies, gas; collisionless here)
and light feel Newton(all) + phantom(baryons); the dark state feels Newton(all) only (L353 reciprocity).  The dark sector is
FK1/FP10's fluid with XR19's web conversion: at z_obs about 9% of a shell's fluid is bound in sub-haloes (cold), 49% escaped
sub-haloes at z ~ 5-13 with v_k, 30% converted in the web at z ~ 1.1-2.1 with v_k (the recaptured hot phase), and the rest
converts at the host's front (0.95 r200c) -- v_k = 600 km/s (FK1's window 575-650; hot-phase brackets in XR28_hot_phase).

THE OBSERVABLES AND THE DATA.  Four stacked samples (DATA in XR28_common; h = 0.7, comoving): DES-Y1 redMaPPer (Chang et al.
2018: WL r_sp/r200m 0.97 +- 0.15, gamma -3.5 +- 0.4; galaxies 0.82 +- 0.05, -3.6 +- 0.3; optically selected), ACT-DR5 x DES-Y3
(Shin et al. 2021: WL 1.16 +0.21/-0.29, -3.42 +0.54/-0.40; galaxies 1.10 +0.06/-0.14, -3.40 +0.32/-0.17; N-body 1.07), CCCP
(Contigiani et al. 2019: WL 1.34 +0.45/-0.26, -4.3 +1.0/-1.5) and Planck SZ (Zurcher & More 2019: galaxies 0.92 +0.13/-0.15).
The model is read the way the observers read the sky: the stacked (3-member Gauss-Hermite environment ensemble x 7 snapshots
over Delta ln a = +-0.12) profile is projected to Delta Sigma (lensing: Newton + phantom) and Sigma_g (baryonic tracers) and
fitted with DK14 under Shin et al.'s priors; r_sp and gamma(r_sp) come from the fitted 3D profile (steepest slope in
[0.5, 3] r200m).  The particle-based matter profiles carry a declared lognormal apocentre scatter of 0.12 in r (the
triaxiality a spherical model lacks; the phantom is not smoothed).  Each model cluster's LENSING
M200m (Newton + phantom) is matched to the sample's (within 6%).

CHECKS (pre-declared; load-bearing unless marked)
  O1  CONTROL: the LCDM model reproduces the LCDM-consistent measurements -- its DK14 WL and galaxy r_sp/r200m and gamma lie
      within 2 sigma of the scored SZ/X-ray-selected samples.  O1b (reported): the 3D read-out against every sample.
  O2  THE BAND-PASS IS VISIBLE IN THE OUTSKIRTS: for every finite L0 the phantom's 3D density has its most negative point in
      [0.5, 6] L(z_obs) (the Gauss-compensation trough) at r/L(z_obs) in [1, 3], every sample, both footings.
  O3  THE EDGE TRACKS L, NOT MASS: at H_Y's L0 the trough radius varies by <= 0.15 dex across the four samples while their
      r200m spans >= 0.25 dex.
  O4  THE PIN: the published splashback radii and slopes (sum of squared pulls, relative to the LCDM model's) exclude
      (Delta chi^2 > 9 on both footings) at least one L0 in [0.5, 5] Mpc -- the outskirts constrain L.  SCORING RULE: a
      (sample, probe) enters only where the LCDM control's DK14 read-out is interior to [0.5, 3] r200m with fit chi^2 <= 2
      N_bins; pulls capped at |5|.
  O5  (reported) the allowed range: every L0 with Delta chi^2 <= 4 on both footings, H_Y's L0 and H_S's band marked.
  O6  (reported) the outer Delta Sigma SHAPE PROXY (R >= 0.8 h^-1 cMpc, free amplitude, the published per-bin precision of
      Shin et al. 2021, 8.7% -- not their data vector): Delta chi^2_shape of each L0 against the LCDM model.
  O7  (reported) nu_mono in place of P2 at H_Y's L0 (ACT-DR5 sample, both footings).
  O8  (reported) L = oo (no band-pass): the outer Delta Sigma and the data pulls.
  H   (reported) the pre-declared hypotheses, as they fall:
      H1 H_Y's L0 (1.688 Mpc) is excluded by the published r_sp/gamma (Delta chi^2 > 9, both footings);
      H2 every L0 in [1.0, 3.25] Mpc (H_S's band included) fails the shape proxy (Delta chi^2_shape > 9);
      H3 at H_Y's L0 the chain's galaxy r_sp/r200m sits >= 10% below the LCDM model's (the phantom pulls baryonic tracers in);
      H4 the two footings agree on every O-verdict.
MUTATE=1: the band-pass is removed in every chain run (L = oo): O2 and O3 must FAIL (no trough) -- rc = 1.

HISTORY (stated).  Exploratory runs in the session scratch came first (not committed): the point-mass phantom at L = 0.5-5 Mpc;
a cold-dark-matter chain run at the ACT-DR5 mass over L0 (lensing density turns negative at ~1-1.5 r200m for L0 ~ 1-2.2 Mpc);
and the DK14 forward-fit at L0 = 1.0/1.69/2.9/5/oo on the t = 0 member only (H_Y: WL x_sp 0.86, gamma -4.5; galaxies 0.87,
-3.7; LCDM 1.19/-3.23 and 1.03/-3.19).  The checks, hypotheses and thresholds above were written after those runs and before
this script's first run.  After XR28_controls' MUTATE run showed the LCDM read-out unstable (an inner 1-D caustic
read as splashback), three settings were fixed before any run of this script: the apocentre scatter (0.12), the
[0.5, 3] r200m read-out window and ds = 0.00075 (XR28_controls K6b checks them); 2 kick nodes here (4 in the hot-phase
lane; K6b checks the difference).  A SMOKE RUN of this script (scratch copy, reduced grid L0 = 0.75/1.69/oo, outputs not
kept) then showed (i) the DK14 MAP read-out degenerate for the two massive samples (CCCP, Planck SZ: the infall power law
replaces the one-halo term and the steepest slope sits at the window edge, for LCDM as well), (ii) the trough finder taking
a negative phantom density in the model's cored centre (r/L = 0.02; the 1-D model's baryon core under the band-pass
subtraction), and (iii) those artefacts dominating Delta chi^2.  Before any recorded run the trough search was restricted
to [0.5, 6] L and the scoring rule of O4 was declared.  The inner Delta Sigma bins (R < 0.8) are left out of the shape proxy because the 1-D model's cores
(and the data's miscentring) are not trusted there.

SCOPE.  A spherical 1-D model: no triaxiality, substructure, dynamical friction or gas pressure (baryons collisionless); the
phantom of an isolated spherical system in the web's absence (no external field); projection effects of optical selection not
modelled.  The DK14 fit uses fractional errors from Shin et al.'s total S/N, not the data covariances.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR28_outskirts_L.py  (~16 min, 2 workers)
"""
import os, sys, math, json, time, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
warnings.filterwarnings("ignore")
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import XR28_common as X

MUTATE = os.environ.get("MUTATE", "0") == "1"
NQ, NMU, VK = 600, 2, 600.0
LGRID = [0.5, 0.75, 1.0, 1.3, X.L0_HY, 2.2, 2.9, 5.0, float("inf")]
SAMPLES = list(X.DATA.keys())


def observe(st, a_obs, L0):
    st = X.smooth_matter(st)
    r200 = st["r200m_lens"]; r200h = r200 * X.HD
    e = X.model_esd(st); g = X.model_sigma(st)
    fw = X.dk14_fit(e, "esd", r200h=r200h); fg = X.dk14_fit(g, "sigma", r200h=r200h)
    s3l = X.splashback3d(st["prof"]["lens"], r200); s3g = X.splashback3d(st["prof"]["bar"], r200)
    s3d = X.splashback3d(st["prof"]["dark"], r200)
    ph = st["prof"]["phantom"]; Lz = X.L_of_a(a_obs, L0)
    tr = None
    if Lz:                                   # the Gauss-compensation trough: the most negative phantom density in [0.5, 6] L(z)
        rph = X.XBM * a_obs; wmask = (rph >= 0.5 * Lz) & (rph <= 6.0 * Lz)
        if np.any(ph[wmask] < 0):
            i = int(np.where(wmask)[0][np.argmin(ph[wmask])])
            tr = dict(r_phys=float(rph[i]), over_L=float(rph[i] / Lz), over_r200=float(X.XBM[i] / r200), min_contrast=float(ph[i]))
    edge = lambda f: bool(min(abs(math.log(f["r_sp"] / (0.5 * r200h))), abs(math.log(f["r_sp"] / (3.0 * r200h)))) < math.log(1.03))
    return dict(M200m_lens=st["M200m_lens"], M200m_newt=st["M200m_newt"], r200m=r200,
                x3=s3l.get("x_sp"), g3=s3l["gamma"], neg=s3l["neg_range"], minima=s3l.get("minima"),
                x3_gal=s3g.get("x_sp"), g3_gal=s3g["gamma"], x3_dm=s3d.get("x_sp"), g3_dm=s3d["gamma"], minima_dm=s3d.get("minima"),
                xwl=fw["r_sp"] / r200h, gwl=fw["gamma"], chi2wl=fw["chi2"], xgal=fg["r_sp"] / r200h, ggal=fg["gamma"], chi2gal=fg["chi2"],
                esd=e.tolist(), trough=tr, edge_wl=edge(fw), edge_gal=edge(fg))


def run_member(Mf, z, t_env, dark, L0, a0, kernel, fp10, fweb, vk=None, nmu=None):
    ic = X.initial_profile(Mf, z, NQ, t_env=t_env)
    parts = X.build_particles(ic, dark, vk=VK if vk is None else vk, nmu=NMU if nmu is None else nmu, fp10=fp10, fweb=fweb, zobs=z)
    res = X.run_shells(ic, parts, a0=a0, L0=L0, kernel=kernel, z_obs=z)
    sp = res["sp"]
    return X.snapshot_profiles(res, {"all": np.ones_like(sp, bool), "bar": sp == 0, "dark": sp == 1})


def model_point(key, dark, L0, a0, kernel, Mf_guess, fp10, fweb, tol=0.06):
    """match the stacked lensing M200m to the sample's, then run the 3-member ensemble; returns observables."""
    d = X.DATA[key]; z = d["z"]; Mt = d["M200m"] * 1e14 / X.HD
    Mf = Mf_guess; t0 = None; hist = []
    for _ in range(4):                       # secant in ln M: the phantom makes M200m_lens sub-linear in the IC mass
        t0 = run_member(Mf, z, 0.0, dark, L0, a0, kernel, fp10, fweb)
        Mm = X.stack([(1.0, s_) for s_ in t0])["M200m_lens"]
        if abs(Mm / Mt - 1) <= tol:
            break
        hist.append((math.log(Mf), math.log(Mm)))
        slope = 1.0 if len(hist) < 2 else float(np.clip((hist[-1][1] - hist[-2][1]) / (hist[-1][0] - hist[-2][0] + 1e-12), 0.3, 1.5))
        Mf = math.exp(math.log(Mf) + (math.log(Mt) - math.log(Mm)) / slope); t0 = None
    if t0 is None:
        t0 = run_member(Mf, z, 0.0, dark, L0, a0, kernel, fp10, fweb)
    items = [(w_ / len(t0), s_) for s_ in t0 for (tt, w_) in [X.GH3[1]]]
    for tt, w_ in (X.GH3[0], X.GH3[2]):
        items += [(w_ / 7.0, s_) for s_ in run_member(Mf, z, tt, dark, L0, a0, kernel, fp10, fweb)]
    st = X.stack(items)
    out = observe(st, 1 / (1 + z), L0)
    out.update(Mf=Mf, mass_ratio=st["M200m_lens"] / Mt)
    return out


def job(args):
    key, foot, what = args
    fp10 = X.fp10_budget(VK, "185"); fweb = X.fweb_history(fp10)
    d = X.DATA[key]; Mt = d["M200m"] * 1e14 / X.HD
    rows = []
    # LCDM calibration (shared guess)
    Mf = Mt
    for _ in range(4):
        st = X.stack([(1.0, s_) for s_ in run_member(Mf, d["z"], 0.0, "lcdm", None, None, "p2", fp10, fweb)])
        Mf *= Mt / st["M200m_lens"]
    if what == "lcdm":
        r = model_point(key, "lcdm", None, None, "p2", Mf, fp10, fweb); r.update(model="LCDM", L0=None, foot=None)
        return [dict(key=key, **r)]
    if what == "mono":
        r = model_point(key, "nominal", X.L0_HY, X.A0[foot], "mono", Mf * 0.8, fp10, fweb)
        r.update(model="chain-mono", L0=X.L0_HY, foot=foot)
        return [dict(key=key, **r)]
    fac = 0.8
    for L0 in LGRID:
        Leff = float("inf") if MUTATE else L0
        r = model_point(key, "nominal", Leff, X.A0[foot], "p2", Mf * fac, fp10, fweb)
        fac = r["Mf"] / Mf
        r.update(model="chain", L0=L0, foot=foot)
        rows.append(dict(key=key, **r))
    return rows


if __name__ == "__main__":
    R = X.Report("XR28 outskirts", "XR28_outskirts_L", MUTATE)
    P, check = R.P, R.check
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: the band-pass is removed in every chain run (L = oo) -- O2 and O3 must FAIL ***")
    P(f"\n  H_Y: L0 = {X.L0_HY:.3f} Mpc; H_S band: {X.L0_HS_BAND[0]:.2f}-{X.L0_HS_BAND[1]:.2f} Mpc; grid {[round(v, 3) for v in LGRID]}; "
      f"footings a0 = {X.A0_SI['canonical']:.4e} / {X.A0_SI['alt']:.4e} m/s^2; {NQ} shells, {NMU} kick nodes, v_k = {VK:.0f} km/s")
    jobs = [(k_, f_, "chain") for k_ in SAMPLES for f_ in X.FOOTS] + [(k_, None, "lcdm") for k_ in SAMPLES] \
        + [("ACT-DR5 x DES-Y3 (Shin+2021)", f_, "mono") for f_ in X.FOOTS]
    jobs.sort(key=lambda j_: 0 if j_[2] == "chain" else 1)
    with Pool(2) as pool:
        res = [r_ for rows in pool.imap_unordered(job, jobs) for r_ in rows]
    P(f"  runs done {R.el()}")
    LC = {r_["key"]: r_ for r_ in res if r_["model"] == "LCDM"}
    CH = {(r_["key"], r_["foot"], r_["L0"]): r_ for r_ in res if r_["model"] == "chain"}
    MO = {r_["foot"]: r_ for r_ in res if r_["model"] == "chain-mono"}
    R.numbers["LCDM"] = LC; R.numbers["chain"] = {f"{k_[0]}|{k_[1]}|{k_[2]}": v_ for k_, v_ in CH.items()}; R.numbers["mono"] = MO

    # ---------------------------------------------------------------------------------------------- tables
    R.banner("THE MODEL CLUSTERS: lensing (Newton + phantom) and galaxies, read by the DK14 forward-fit and in 3D")
    for key in SAMPLES:
        d = X.DATA[key]; lc = LC[key]
        P(f"\n  {key}: M200m = {d['M200m']}e14 h^-1 Msun, z = {d['z']} ({d['sel']}-selected)")
        P(f"    {'model':>14s} {'M/Mt':>5s} | {'WL x_sp':>7s} {'g':>6s} {'chi2':>5s} | {'gal x_sp':>8s} {'g':>6s} | {'3D lens':>7s} {'g':>7s} "
          f"{'neg [r/r200m]':>14s} | {'3D gal':>6s} {'3D DM':>6s} {'gDM':>6s} | trough r/L, r/r200m")
        def line(lab, r_):
            tr = r_["trough"]; trs = f"{tr['over_L']:.2f}, {tr['over_r200']:.2f}" if tr and tr["over_L"] else ("-" if not tr else f"-, {tr['over_r200']:.2f}")
            neg = f"{r_['neg'][0]:.2f}-{r_['neg'][1]:.2f}" if r_["neg"] else "-"
            P(f"    {lab:>14s} {r_['mass_ratio']:5.2f} | {r_['xwl']:7.3f} {r_['gwl']:6.2f} {r_['chi2wl']:5.1f} | {r_['xgal']:8.3f} {r_['ggal']:6.2f} | "
              f"{r_['x3']:7.3f} {r_['g3']:7.2f} {neg:>14s} | {r_['x3_gal']:6.3f} {r_['x3_dm']:6.3f} {r_['g3_dm']:6.2f} | {trs}")
        line("LCDM", lc)
        for f_ in X.FOOTS:
            for L0 in LGRID:
                line(f"{f_[:3]} L0 {L0:.2f}", CH[(key, f_, L0)])

    # ---------------------------------------------------------------------------------------------- data pulls
    R.banner("THE DATA: pulls of the published r_sp/r200m and gamma(r_sp) (the error on the model's side)")

    # the declared scoring rule (fixed after a smoke run, before any recorded run): a (sample, probe) enters the load-bearing
    # chi^2 only where the LCDM control's DK14 read-out is interior to [0.5, 3] r200m and its fit chi^2 <= 2 N_bins (the
    # model then has a detectable splashback at the published precision); every pull is capped at |5| (an edge read-out is a
    # non-detection, not a measurement)
    SCORED = []
    for key in SAMPLES:
        for kind, ek, ck, nb in (("wl", "edge_wl", "chi2wl", len(X.R_WL)), ("gal", "edge_gal", "chi2gal", len(X.R_GAL))):
            if X.DATA[key][kind] is not None and not LC[key][ek] and LC[key][ck] <= 2 * nb:
                SCORED.append((key, kind))
    P(f"    scored (sample, probe): {[(k_.split(' (')[1].split(')')[0], kd) for k_, kd in SCORED]}")
    R.numbers["scored"] = SCORED
    CAP = 5.0

    def chi2_of(get, which=None):
        which = SCORED if which is None else which
        tot = 0.0; parts = {}
        for key, kind in which:
            d = X.DATA[key]; r_ = get(key); dd = d[kind]
            xk, gk = ("xwl", "gwl") if kind == "wl" else ("xgal", "ggal")
            px = float(np.clip(X.pull(r_[xk], dd, "x"), -CAP, CAP)); parts[f"{key}|{kind}|x"] = px; tot += px * px
            if dd.get("g") is not None:
                pg = float(np.clip(X.pull(r_[gk], dd, "g"), -CAP, CAP)); parts[f"{key}|{kind}|g"] = pg; tot += pg * pg
        return tot, parts

    c2_l, parts_l = chi2_of(lambda k_: LC[k_])
    P(f"    LCDM model: chi^2 = {c2_l:.2f} over {len(parts_l)} numbers: " + ", ".join(f"{k_.split(' (')[1].split(')')[0]}|{k_.split('|', 1)[1]} {v_:+.2f}" for k_, v_ in parts_l.items()))
    DCH = {}
    for f_ in X.FOOTS:
        for L0 in LGRID:
            c2, pt = chi2_of(lambda k_: CH[(k_, f_, L0)])
            DCH[(f_, L0)] = dict(chi2=c2, dchi2=c2 - c2_l, pulls=pt)
            P(f"    {f_:9s} L0 {L0:5.2f}: chi^2 = {c2:7.2f} (Delta {c2 - c2_l:+7.2f}); largest pulls: "
              + ", ".join(f"{k_.split(' (')[1].split(')')[0]}|{k_.split('|', 1)[1]} {v_:+.2f}" for k_, v_ in sorted(pt.items(), key=lambda kv: -abs(kv[1]))[:4]))
    R.numbers["data_chi2"] = dict(LCDM=dict(chi2=c2_l, pulls=parts_l), chain={f"{k_[0]}|{k_[1]}": v_ for k_, v_ in DCH.items()})

    # ---------------------------------------------------------------------------------------------- shape proxy
    R.banner("THE OUTER Delta Sigma SHAPE PROXY (R >= 0.8 h^-1 cMpc; free amplitude; 8.7% per bin, Shin+2021's precision)")
    sel = X.R_WL >= 0.8; sig = math.sqrt(len(X.R_WL)) / X.ERR_WL
    SH = {}
    for f_ in X.FOOTS:
        for L0 in LGRID:
            tot = 0.0; rows = {}
            for key in SAMPLES:
                if X.DATA[key]["wl"] is None:
                    continue
                e0 = np.array(LC[key]["esd"])[sel]; e1 = np.array(CH[(key, f_, L0)]["esd"])[sel]
                rt = e1 / e0; A = float(np.sum(rt) / np.sum(rt * rt))
                c2 = float(np.sum(((A * rt - 1) / sig) ** 2)); tot += c2; rows[key] = dict(chi2=c2, ratio=(A * rt).tolist())
            SH[(f_, L0)] = dict(chi2=tot, rows=rows)
            k0 = "ACT-DR5 x DES-Y3 (Shin+2021)"
            P(f"    {f_:9s} L0 {L0:5.2f}: Delta chi^2_shape = {tot:9.1f}; ACT-DR5 A x ratio at R = " +
              ", ".join(f"{R_:.2f}:{v_:.2f}" for R_, v_ in zip(X.R_WL[sel], rows[k0]["ratio"])))
    R.numbers["shape"] = {f"{k_[0]}|{k_[1]}": v_ for k_, v_ in SH.items()}

    # ---------------------------------------------------------------------------------------------- checks
    R.banner("CHECKS")
    clean = [(k_, kd) for k_, kd in SCORED if X.DATA[k_]["sel"] != "optical"]
    o1 = {k_: v_ for k_, v_ in parts_l.items() if (k_.split("|")[0], k_.split("|")[1]) in clean}
    check("O1 CONTROL: the LCDM model's DK14 WL and galaxy r_sp/r200m and gamma lie within 2 sigma of the SZ/X-ray-selected "
          "measurements it can score (the scored SZ/X-ray (sample, probe) pairs)",
          (", ".join(f"{k_.split(' (')[1].split(')')[0]}|{k_.split('|', 1)[1]} {v_:+.2f}" for k_, v_ in o1.items()) or "none scored"),
          len(o1) > 0 and all(abs(v_) <= 2.0 for v_ in o1.values()))
    r1 = {}
    for key in SAMPLES:
        for kind, xk in (("wl", "x3"), ("gal", "x3_gal")):
            dd = X.DATA[key][kind]
            if dd is None:
                continue
            r1[f"{key}|{kind}"] = dict(LCDM=X.pull(LC[key][xk], dd, "x"),
                                       HY=[X.pull(CH[(key, f_, X.L0_HY)][xk], dd, "x") for f_ in X.FOOTS])
    check("O1b (reported) the 3D read-out (the smoothed model's own slope minimum, what DK14 fits are built to recover) against "
          "every published r_sp/r200m, LCDM and the chain at H_Y (canonical/alt)",
          "; ".join(f"{k_.split(' (')[1].split(')')[0]}|{k_.split('|')[1]}: LCDM {v_['LCDM']:+.2f}, H_Y {v_['HY'][0]:+.2f}/{v_['HY'][1]:+.2f}"
                    for k_, v_ in r1.items()), True, load_bearing=False)
    R.numbers["O1b"] = r1
    trs = [(k_, v_["trough"]) for k_, v_ in CH.items() if np.isfinite(k_[2])]
    ok2 = all(t_ is not None and t_["over_L"] is not None and 1.0 <= t_["over_L"] <= 3.0 for _, t_ in trs)
    vals = [t_["over_L"] for _, t_ in trs if t_ is not None and t_["over_L"] is not None]
    check("O2 THE BAND-PASS IS VISIBLE: for every finite L0 the phantom's 3D density has its compensation trough at r/L(z_obs) "
          "in [1, 3] (4 samples, 2 footings, 8 finite L0)",
          f"{len(vals)}/{len(trs)} runs with a trough; r/L range {min(vals) if vals else float('nan'):.2f}-{max(vals) if vals else float('nan'):.2f}", ok2)
    hy = [CH[(k_, "canonical", X.L0_HY)] for k_ in SAMPLES]
    trr = [r_["trough"]["r_phys"] for r_ in hy if r_["trough"]]
    r2p = [r_["r200m"] / (1 + X.DATA[k_]["z"]) for r_, k_ in zip(hy, SAMPLES)]
    spread_t = math.log10(max(trr) / min(trr)) if len(trr) == 4 else float("inf")
    spread_r = math.log10(max(r2p) / min(r2p))
    check("O3 THE EDGE TRACKS L, NOT MASS: at H_Y's L0 the trough's physical radius varies by <= 0.15 dex across the four samples "
          "while their r200m spans >= 0.25 dex (canonical)",
          f"trough {', '.join(f'{v_:.2f}' for v_ in trr)} Mpc ({spread_t:.2f} dex); r200m {', '.join(f'{v_:.2f}' for v_ in r2p)} Mpc ({spread_r:.2f} dex)",
          len(trr) == 4 and spread_t <= 0.15 and spread_r >= 0.25)
    finite = [L0 for L0 in LGRID if np.isfinite(L0)]
    excl = [L0 for L0 in finite if all(DCH[(f_, L0)]["dchi2"] > 9 for f_ in X.FOOTS)]
    allow = [L0 for L0 in finite if all(DCH[(f_, L0)]["dchi2"] <= 4 for f_ in X.FOOTS)]
    check("O4 THE PIN: the published splashback radii and slopes exclude (Delta chi^2 > 9 on both footings, relative to the LCDM "
          "model) at least one L0 in [0.5, 5] Mpc",
          f"excluded L0: {[round(v_, 3) for v_ in excl]}; allowed (<= 4 both): {[round(v_, 3) for v_ in allow]}; "
          + "; ".join(f"L0 {L0:.2f}: {DCH[('canonical', L0)]['dchi2']:+.1f}/{DCH[('alt', L0)]['dchi2']:+.1f}" for L0 in finite), len(excl) >= 1)
    hs_in = [L0 for L0 in finite if X.L0_HS_BAND[0] <= L0 <= X.L0_HS_BAND[1]]
    check("O5 (reported) THE ALLOWED RANGE of L0 (Delta chi^2 <= 4 on both footings), with H_Y's L0 and H_S's band marked",
          f"allowed {[round(v_, 3) for v_ in allow]}; H_Y L0 {X.L0_HY:.3f}: {DCH[('canonical', X.L0_HY)]['dchi2']:+.1f} / "
          f"{DCH[('alt', X.L0_HY)]['dchi2']:+.1f}; H_S band {X.L0_HS_BAND[0]:.2f}-{X.L0_HS_BAND[1]:.2f}: grid points {hs_in} -> "
          + ", ".join(f"{DCH[('canonical', L0)]['dchi2']:+.1f}/{DCH[('alt', L0)]['dchi2']:+.1f}" for L0 in hs_in), True, load_bearing=False)
    sh_ok = [L0 for L0 in LGRID if all(SH[(f_, L0)]["chi2"] <= 9 for f_ in X.FOOTS)]
    check("O6 (reported) THE SHAPE PROXY: L0 with Delta chi^2_shape <= 9 on both footings (outer Delta Sigma within the published "
          "per-bin precision of an LCDM-shaped profile)", f"passing: {[round(v_, 3) for v_ in sh_ok]}; "
          + "; ".join(f"{L0:.2f}: {SH[('canonical', L0)]['chi2']:.0f}/{SH[('alt', L0)]['chi2']:.0f}" for L0 in LGRID), True, load_bearing=False)
    k0 = "ACT-DR5 x DES-Y3 (Shin+2021)"
    check("O7 (reported) nu_mono in place of P2 at H_Y's L0 (ACT-DR5 sample)",
          "; ".join(f"{f_}: WL x_sp {MO[f_]['xwl']:.3f} (P2 {CH[(k0, f_, X.L0_HY)]['xwl']:.3f}), gamma {MO[f_]['gwl']:.2f} "
                    f"(P2 {CH[(k0, f_, X.L0_HY)]['gwl']:.2f}); galaxies {MO[f_]['xgal']:.3f} ({CH[(k0, f_, X.L0_HY)]['xgal']:.3f})" for f_ in X.FOOTS),
          True, load_bearing=False)
    inf_ = float("inf")
    check("O8 (reported) L = oo (no band-pass): the data pulls and the shape proxy", f"Delta chi^2 {DCH[('canonical', inf_)]['dchi2']:+.1f}/"
          f"{DCH[('alt', inf_)]['dchi2']:+.1f}; shape {SH[('canonical', inf_)]['chi2']:.0f}/{SH[('alt', inf_)]['chi2']:.0f}", True, load_bearing=False)

    # hypotheses
    H1 = all(DCH[(f_, X.L0_HY)]["dchi2"] > 9 for f_ in X.FOOTS)
    H2 = all(SH[(f_, L0)]["chi2"] > 9 for f_ in X.FOOTS for L0 in finite if 1.0 <= L0 <= 3.25)
    H3 = all(CH[(k_, f_, X.L0_HY)]["xgal"] <= 0.9 * LC[k_]["xgal"] for k_ in (k0, "DES-Y1 redMaPPer (Chang+2018)") for f_ in X.FOOTS)
    H4 = all((DCH[("canonical", L0)]["dchi2"] > 9) == (DCH[("alt", L0)]["dchi2"] > 9) and
             (DCH[("canonical", L0)]["dchi2"] <= 4) == (DCH[("alt", L0)]["dchi2"] <= 4) for L0 in finite)
    HH = {"H1 H_Y excluded by r_sp/gamma": H1, "H2 [1, 3.25] fails the shape proxy": H2, "H3 galaxies >= 10% inside LCDM at H_Y": H3,
          "H4 footings agree": H4}
    check("H (reported) the pre-declared hypotheses, as they fell", "; ".join(f"{k_}: {'held' if v_ else 'FELL'}" for k_, v_ in HH.items()),
          True, load_bearing=False)
    R.numbers["H"] = HH
    R.numbers["grid"] = dict(L=LGRID, L0_HY=X.L0_HY, L0_HS=X.L0_HS_BAND)
    sys.exit(R.finish())
