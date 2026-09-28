#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG23 -- THE LCDM CONTROL IN THE SAME MACHINERY: is the KiDS-vs-Local-Group conflict (CFG21/CFG22, 5-7 sigma) specific to the
framework's phantom, or does it also bite standard halos scored the same way?

WHY.  CFG21/22 score KiDS's isolated lenses with FP1/L355's machinery (FP20's exact projector, a LINEAR 2-halo template whose
amplitude is the lens bias) and the LG with FP1's shell integrator.  If NFW halos with a standard concentration relation and the
standard (linear, peak-background) bias also cannot fit KiDS and the LG together in THIS machinery, the 5-7 sigma measures a
limitation of the machinery or a tension between the data sets, not a failure specific to the framework.  If they can, the conflict
belongs to the framework's phantom shape.  NFW, Duffy et al. 2008's c(M200m, z) (full sample: 10.14 (M/2e12 h^-1)^-0.081 (1+z)^-1.01)
and Tinker et al. 2010's bias (Delta = 200 mean) are used ONLY as a control -- no framework statement rests on them.

THE CONTROL MODEL (per KiDS lens bin): M(r) = M_b (point) + M_NFW(r; M200m, c(M200m, z_l = 0.25)); the 2-halo template (FP1's, linear,
unchanged) with amplitude A = b_Tinker(M200m) (fixed, not fitted); M_b profiled over FP1's grid, log M200m profiled over 10.5-14.5;
the same per-bin minimisation and full-covariance chi^2 as FP1's kfit.  The LG: MW (M_b 6e10) and M31 (1.2e11) as NFW halos with the
KiDS-fitted M200m(M_b) (interpolated in log M_b), their enclosed masses summed about the barycentre, R0 from FP1's integrator run
as Newton + Lambda on that mass (static in time, the standard timing convention).

PRE-DECLARED (before this script's first run)
  C1  CONTROL  the exec'd KiDS machinery reproduces FP1/FP20's committed isolated-P2 chi^2 (139.800, canonical) and CFG21's committed
      KiDS best for the framework (canonical P2: 139.800 - 35.114 = 104.686).
  C2  CONTROL  the point-mass Newton + Lambda R0(M) from FP1's integrator is monotone in M and returns 0.93 Mpc for a mass in the
      range quoted by LG timing studies (2-5e12 Msun); the value is reported.
  H1  [the diagnostic's first half; MUTATE must fail] NFW + Duffy c(M) + Tinker linear bias fits KiDS within +9 of the framework's best
      (chi^2 <= 113.7).  Expectation: uncertain.
  H2  [the second half] with the KiDS-fitted M200m(M_b), MW + M31 give the LG an R0 within 2 sigma of 0.93 +- 0.12 Mpc (<= 1.17).
      Expectation: uncertain.
  READING (declared): H1 and H2 both pass -> the KiDS-LG conflict is the framework's own (its phantom shape); H1 passes, H2 fails ->
  standard halos meet the same wall in this machinery (a data tension or a modelling limit, e.g. the linear 2-halo); H1 fails -> the
  machinery's 2-halo is insufficient for any single-halo model.
MUTATE=1: the halo-mass grid is capped at 10^11 Msun (halos far too small) -- H1 must FAIL (rc = 1).

REVISION (after the first -- MUTATE -- run, before any main run; disclosed).  The first-written checks are all still computed and
scored exactly as written; four changes make the control parallel to what the framework was given, and one fixes a declared range:
  (a) C2 as written FAILED in the MUTATE run: R0 = 0.93 Mpc falls at M = 1.57e12 Msun.  The declared 2-5e12 range is the MW-M31
      timing-argument mass (a radial-orbit estimate), not the zero-velocity-surface mass this integrator computes; zero-velocity-
      surface estimates in the literature are lower (e.g. Karachentsev et al. 2009).  The first-written C2 stays scored (FAIL).  The
      operative C2: the exec'd integrator reproduces FP1's committed E1 control (nu_RAR, 1.145e11: 1.929 / 2.021 Mpc, FP1's 2e-3
      tolerance), R0(M) is monotone for a Newtonian point mass, and the point-mass table interpolates to 1e-3 Mpc.
  (b) C1 as written compares exec'd numbers only; it does not test this script's own fitter.  Operative C1: the fitter (kfit_caps's
      algebra with a halo axis) reproduces BASE (canonical P2, caps 0) and kfit_caps at CFG21's KiDS-best edge with CFG16's
      self-consistent caps, both equal to CFG21's committed value; the halo-plus-point-mass split of FIX is exact (1e-10).
  (c) The 2-halo: the first-written H1 fixes A = b_Tinker; the framework in CFG16/21 was granted A in [0, its bias] (KiDS's isolation
      criterion lowers the 2-halo).  Operative treatment: A in [0, b_Tinker(M200m)] per bin -- kfit_caps's algebra.
  (d) The edge: the framework's phantom was given an edge x_e r_ta scanned jointly with the LG (CFG21).  The operative control gives
      the NFW the same freedom: truncation at x_t R200m (mass constant beyond), x_t in {0.5 .. 4, infinity}, the KiDS fit redone at
      every x_t.  x_t = 1 is the halo-model convention; x_t = infinity is the first-written model.
  (e) The LG's halos: the first-written H2 interpolates the KiDS fit in the PROFILED M_b (a nuisance).  Operative: the MW sits in bin
      3 (B21's log M* 10.6-10.8 in h70^-2 Msun, i.e. 10.63-10.83 at h = 0.674; the MW's is ~10.7-10.8) and M31 in bin 4 (10.83-11.03;
      M31's ~11.0-11.1 sits at or above the top edge, so bin 4's halo is a LOWER bound for M31's).  Both halos are centred on the
      barycentre (FP1's convention); their KiDS-fitted physical profiles at z_l are used unchanged (growth to z = 0 omitted: generous
      to LCDM).  The mass inside a shell is conserved in spherical infall before shell crossing, so R0 is the point-mass R0 of the
      mass inside R0 today, solved self-consistently.  LG baryons 1.145e11 / 1.72e11 (FP1's), total only (both centred).
  OPERATIVE CHECKS (declared now, before any main run):
  H1p [MUTATE must fail] the parallel control fits KiDS within +9 of the framework's best (canonical P2) at its best x_t.
  H3  [HEADLINE; the READING] the parallel control's KiDS-LG tension is acceptable: T_min <= 9, with CFG21's statistic
      T = [chi2_KiDS(x_t, m3, m4) - min chi2_KiDS] + [(R0 - 0.93)/0.12]^2 minimised over the parameters the two data sets share
      (x_t and the halo masses m3, m4 of bins 3 and 4; every KiDS nuisance profiled), Duffy c, Tinker caps, LG M_b 1.145e11.
      READING: H3 PASS -> the conflict is specific to the framework's phantom; H3 FAIL -> standard halos meet a conflict in this
      machinery too, and the framework's excess over the control, dT = T_fw - T_LCDM, is what belongs to the phantom.
  R1  (reported) variants: c x 0.7 / x 1.4; the framework's own bias formula (CFG16's bias_of) as the cap; MW in bin 4; LG M_b
      1.72e11; T at x_t = 1 alone; the KiDS model comparison (parameter counts: LCDM 4 M_b + 4 M200m + 4 A + x_t = 13; the
      framework 4 M_b + 4 A + x_e = 9).
  (f) AMENDED after the revised script's MUTATE run, before any main run (disclosed): that run showed the READING as just written
      (H3 alone) calls a control that fails KiDS by +900 'framework-specific' -- T measures each data set against its OWN best, so it
      is blind to a bad fit.  The READING now requires H1p, as the first-written READING required H1:  H1p FAIL -> the control does
      not fit KiDS in this machinery (no reading);  H1p PASS + H3 PASS -> the conflict is specific to the framework's phantom;
      H1p PASS + H3 FAIL -> standard halos meet a conflict in this machinery too, and dT is what belongs to the phantom.
Run: python3 campaign_fresh_gravity/CFG23_lcdm_control.py   (MUTATE=1 for the control; ~3 min)
"""
import os, sys, math, json, time
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C7
C = C7.C4
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C7.Report("CFG23_lcdm_control", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: halo masses capped at 1e11 Msun -- H1 and H1p must FAIL ***")
np.seterr(all="ignore")
t0 = time.time()
C21 = json.load(open(os.path.join(HERE, "CFG21_kids_lg_joint_results.json")))["numbers"]["RES"]

# ================================================================================================ CFG16's machinery (exec'd slices, as CFG21)
C16P = os.path.join(HERE, "CFG16_selfconsistent_floor.py")
src = open(C16P).read()
ns = {"__file__": C16P, "__name__": "cfg16_slices", "json": json, "os": os, "sys": sys, "math": math, "time": time, "np": np,
      "C7": C7, "C": C, "HERE": HERE, "MUTATE": False, "P": lambda *a, **k: None,
      "check": lambda *a, **k: None, "R": type("Q", (), {"banner": lambda self, *a, **k: None, "num": lambda self, *a, **k: None})()}
a_ = src.index("SWJ = json.load(")
b_ = src.index("# ================================================================================================ C1\n")
exec(compile("\n" * src[:a_].count("\n") + src[a_:b_], C16P, "exec"), ns)
GK, FIX, BASE, table, kfit_caps, caps_at, M_trunc_xta, bias_of, KERN = (
    ns[k] for k in ("GK", "FIX", "BASE", "table", "kfit_caps", "caps_at", "M_trunc_xta", "bias_of", "KERN"))
LM, NPB, RPK, MPCK, MSK, RRK = GK["LM"], GK["npb"], GK["Rp"], GK["MPCm"], GK["MS"], GK["rrK"]
Ed, Sd, T2H, Ci, Rd = GK["Ed"], GK["Sd"], GK["T2H"], GK["Ci"], GK["Rd"]
DAT = np.concatenate(Ed)
PM = FIX.conv / (math.pi * FIX.Rp ** 2)                                                 # ESD per kg of point mass
PMd = np.array([np.interp(Rd[b], RPK / MPCK, PM) for b in range(4)])                   # at the data radii

# ================================================================================================ the control's ingredients
cos = C7.LCDM
H_ = cos.h
ZL = 0.25
GZ = float(cos.D(1.0 / (1 + ZL)) / cos.D(1.0))
RHOMZ = cos.rhom0 * (1 + ZL) ** 3                                                      # Msun / Mpc^3, physical, at z_l


def sigma_M(M):
    Rl = float(C7.R_lagr(M, cos))
    return math.sqrt(C7.sig2(Rl, Rl, cos)) * GZ


def c_duffy(M200m):
    return 10.14 * (np.asarray(M200m, float) / (2e12 / H_)) ** (-0.081) * (1 + ZL) ** (-1.01)


def bias_tinker(M200m):
    y = math.log10(200.0)
    A = 1.0 + 0.24 * y * math.exp(-(4.0 / y) ** 4); a = 0.44 * y - 0.88
    B, b = 0.183, 1.5
    Cc = 0.019 + 0.107 * y + 0.19 * math.exp(-(4.0 / y) ** 4); c = 2.4
    nu = 1.686 / sigma_M(M200m)
    return 1.0 - A * nu ** a / (nu ** a + 1.686 ** a) + B * nu ** b + Cc * nu ** c


def _fnfw(x):
    return np.log1p(x) - x / (1 + x)


def M_nfw_msun(r_mpc, lm200, xt, cfac):
    """enclosed mass [Msun] of an NFW halo of log M200m = lm200 (Delta = 200 x the mean at z_l), concentration cfac x Duffy, truncated
    at xt R200m (mass constant beyond; xt = inf: untruncated); r in physical Mpc.  Broadcasts over r and lm200."""
    M200 = 10.0 ** np.asarray(lm200, float)
    R200 = (3 * M200 / (4 * math.pi * 200 * RHOMZ)) ** (1 / 3)
    c = cfac * c_duffy(M200)
    x = np.minimum(np.asarray(r_mpc, float), xt * R200) / (R200 / c)
    return M200 * _fnfw(x) / _fnfw(c)


LM200 = np.round(np.arange(10.5, 14.5001, 0.05), 3)
if MUTATE:
    LM200 = LM200[LM200 <= 11.0]
K = len(LM200)
BT = np.array([bias_tinker(10 ** lm) for lm in LM200])
BPS = np.array([bias_of(10 ** lm)[0] for lm in LM200])
XT = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0, float("inf")]
P(f"\n    Tinker bias at log M200m = 11 / 12 / 13 / 14 (z_l = 0.25): " + ", ".join(
    f"{bias_tinker(10 ** v):.2f}" for v in (11, 12, 13, 14)) + "; the framework's formula (CFG16's bias_of): " + ", ".join(
    f"{bias_of(10 ** v)[0]:.2f}" for v in (11, 12, 13, 14)) + f"; Duffy c at 1e12: {float(c_duffy(1e12)):.2f}")


def halo_tables(xt, cfac):
    """TT (K, NLM, 4, npb): the model ESD at the data radii (no 2-halo) for every (log M200m, log M_b)."""
    TT = np.zeros((K, len(LM), 4, NPB))
    for k, lm2 in enumerate(LM200):
        Mh = M_nfw_msun(RRK / MPCK, lm2, xt, cfac) * MSK
        dh = FIX(Mh, 0.0)
        hd = np.array([np.interp(Rd[b], RPK / MPCK, dh) for b in range(4)])
        TT[k] = hd[None] + (10.0 ** LM)[:, None, None] * MSK * PMd[None]
    return TT


def per_bin(TT, caps, mode="cap"):
    """kfit_caps's algebra per bin with a halo axis: for every halo k, the best M_b (diagonal chi^2) with the 2-halo amplitude
    A in [0, caps[k, b]] ('cap') or A = caps[k, b] ('fixed').  Returns, per bin, arrays over k."""
    out = []
    kk_ = np.arange(TT.shape[0])
    for b in range(4):
        t2 = T2H[b]; wv = 1.0 / Sd[b] ** 2
        mk = TT[:, :, b, :]
        if mode == "cap":
            A = np.clip(np.sum(wv * t2 * (Ed[b] - mk), -1) / np.sum(wv * t2 * t2), 0.0, caps[:, b][:, None])
        else:
            A = np.repeat(caps[:, b][:, None], mk.shape[1], 1)
        mm = mk + A[..., None] * t2
        c2 = np.sum(((Ed[b] - mm) / Sd[b]) ** 2, -1)
        im = np.argmin(c2, 1)
        out.append(dict(c2=c2[kk_, im], mod=mm[kk_, im], A=A[kk_, im], im=im))
    return out


def chi2_full(mods):
    dv = DAT - np.concatenate(mods)
    return float(dv @ Ci @ dv)


def kfit_best(pb):
    """FP1's convention: each bin at its own diagonal best; the total with the full covariance."""
    ks = [int(np.argmin(pb[b]["c2"])) for b in range(4)]
    return chi2_full([pb[b]["mod"][ks[b]] for b in range(4)]), ks


# ================================================================================================ C1 (first-written)
R.banner("C1  CONTROL (first-written): the machinery reproduces FP1/FP20's base and CFG21's framework best")
b0 = BASE[("canonical", "P2")]
FW = {(f, kn): BASE[(f, kn)] + C21[f"{f}|{kn}|1.145e+11"]["kids_min"] for f in C.FOOTS for kn in KERN}
fw_best = FW[("canonical", "P2")]
check("C1 CONTROL (first-written): the exec'd KiDS machinery reproduces FP1/FP20's isolated-P2 chi^2 (139.800) and gives CFG21's "
      "framework best", f"base {b0:.4f}; framework best (CFG21) {fw_best:.3f}", abs(b0 - 139.800) < 1e-3)

# ================================================================================================ C1 (operative): this script's fitter
R.banner("C1op  CONTROL: this script's fitter against the committed kfit_caps; the FIX split")
Tb = table(ns["M_law"](KERN["P2"]), "canonical")
pb0 = per_bin(Tb[0][None], np.zeros((1, 4)))
v_a = chi2_full([pb0[b]["mod"][0] for b in range(4)])
xk = C21["canonical|P2|1.145e+11"]["kids_best_x"]
Tx = table(M_trunc_xta(KERN["P2"], xk), "canonical")
cx = caps_at("canonical", "P2", xk)
v_ref = kfit_caps(Tx, cx)
v_ref = v_ref[0] if isinstance(v_ref, tuple) else v_ref
pbx = per_bin(Tx[0][None], np.array([cx]))
v_b = chi2_full([pbx[b]["mod"][0] for b in range(4)])
rng = np.random.default_rng(23)
dsplit = 0.0
for _ in range(4):
    lm2 = float(rng.uniform(11, 14)); lmb = float(rng.choice(LM)); xt = float(rng.choice([0.7, 1.3, float("inf")]))
    Mh = M_nfw_msun(RRK / MPCK, lm2, xt, 1.0) * MSK; Mb = 10 ** lmb * MSK
    lit = FIX(Mb + Mh, Mb); spl = FIX(Mh, 0.0) + Mb * PM
    dsplit = max(dsplit, float(np.max(np.abs(lit - spl) / np.maximum(np.abs(lit), 1e-30))))
c1op = abs(v_a - b0) < 1e-9 and abs(v_b - v_ref) < 1e-9 and abs(v_b - (b0 + C21["canonical|P2|1.145e+11"]["kids_min"])) < 1e-6 \
    and dsplit < 1e-10
check("C1op CONTROL: the fitter reproduces BASE (caps 0) and kfit_caps at CFG21's KiDS-best edge with CFG16's caps (= CFG21's "
      "committed value); the FIX halo + point-mass split is exact",
      f"BASE {v_a:.6f} vs {b0:.6f}; x_e {xk}: {v_b:.6f} vs kfit_caps {v_ref:.6f} vs CFG21 {fw_best:.6f}; split rel {dsplit:.1e}", c1op)

# ================================================================================================ C2 (first-written + operative): the LG point mass
R.banner("C2  CONTROL: FP1's integrator as Newton + Lambda on a point mass")
FP1P = os.path.join(C.CHAIN, "FP1_static_sector.py")
lg = {"np": np, "math": math, "_trap": C._trap}
lg = C.exec_slices(FP1P, [("# ---- LG: XR4's point-mass", "Rctl = lg_R0(")], ns=lg, name="fp1_lg")[0]
lg_R0, Ntab_lg, LG_A0 = lg["lg_R0"], lg["Ntab_lg"], lg["LG_A0"]
newton = lambda y: np.ones_like(np.asarray(y, float))
MGRID = np.geomspace(5e11, 3e13, 18)
R0N = lg_R0([Ntab_lg(newton, 0.0)] * len(MGRID), list(MGRID), [LG_A0["canonical"]] * len(MGRID))
m093 = float(10 ** np.interp(0.93, R0N, np.log10(MGRID)))
mono = bool(np.all(np.diff(R0N) > 0))
P("    point mass [Msun] -> R0 [Mpc]: " + ", ".join(f"{m:.1e}: {r:.3f}" for m, r in zip(MGRID[::3], R0N[::3])) + f"; R0 = 0.93 at M = {m093:.2e}")
check("C2 CONTROL (first-written): the point-mass Newton + Lambda R0(M) is monotone and R0 = 0.93 Mpc falls at 2-5e12 Msun "
      "[see REVISION (a): the declared range is the timing-argument mass]",
      f"monotone {mono}; M(R0 = 0.93) = {m093:.2e} Msun", mono and 2e12 <= m093 <= 5e12)
rc_ = lg_R0([Ntab_lg(C.nu_rar, 0.0)] * 2, [1.145e11] * 2, [LG_A0["canonical"], LG_A0["alt"]])
MG = np.geomspace(1e11, 1e16, 51)
R0G = lg_R0([Ntab_lg(newton, 0.0)] * len(MG), list(MG), [LG_A0["canonical"]] * len(MG))
LMG, LRG = np.log10(MG), np.log10(R0G)
R0_pm = lambda M: 10 ** np.interp(np.log10(M), LMG, LRG)
MT = np.array([3.3e11, 2.2e12, 7.7e13])
R0T = lg_R0([Ntab_lg(newton, 0.0)] * 3, list(MT), [LG_A0["canonical"]] * 3)
dint = float(np.max(np.abs(R0_pm(MT) - R0T)))
c2op = abs(rc_[0] - 1.9290) < 2e-3 and abs(rc_[1] - 2.0214) < 2e-3 and bool(np.all(np.diff(R0G) > 0)) and dint < 1e-3
P(f"    FP1 E1 control: {rc_[0]:.4f} / {rc_[1]:.4f} Mpc (1.929 / 2.021); table 1e11-1e16 monotone {bool(np.all(np.diff(R0G) > 0))}; "
  f"interpolation error at 3 off-grid masses {dint:.1e} Mpc")
check("C2op CONTROL: the integrator reproduces FP1's E1 control; the Newtonian point-mass R0(M) table is monotone and interpolates to "
      "1e-3 Mpc", f"E1 {rc_[0]:.4f} / {rc_[1]:.4f}; interp {dint:.1e}", c2op)

# ================================================================================================ the halo tables
R.banner("THE LCDM FITS: NFW (Duffy c) + point M_b + linear 2-halo, every x_t")
CF = [1.0, 0.7, 1.4]
PB = {}
for cfac in CF:
    for xt in XT:
        TT = halo_tables(xt, cfac)
        PB[(cfac, xt, "T")] = per_bin(TT, np.repeat(BT[:, None], 4, 1))
        if cfac == 1.0:
            PB[(cfac, xt, "PS")] = per_bin(TT, np.repeat(BPS[:, None], 4, 1))
            if xt == float("inf"):
                PB[(cfac, xt, "fixed")] = per_bin(TT, np.repeat(BT[:, None], 4, 1), mode="fixed")
P(f"    tables built ({time.time() - t0:.0f} s)")

# ================================================================================================ H1 (first-written) + H2 (first-written)
R.banner("H1 / H2 (first-written): fixed A = b_Tinker, untruncated NFW")
pbF = PB[(1.0, float("inf"), "fixed")]
chiF, ksF = kfit_best(pbF)
parsF = [(float(LM[pbF[b]["im"][ksF[b]]]), float(LM200[ksF[b]])) for b in range(4)]
P(f"    chi^2 = {chiF:.2f} (framework best {fw_best:.2f}: d = {chiF - fw_best:+.2f}); per bin (log M_b, log M200m): " +
  ", ".join(f"({x:.2f}, {y:.2f})" for x, y in parsF) + "; bias " + ", ".join(f"{BT[k]:.2f}" for k in ksF))
check("H1 (first-written) NFW + Duffy c(M) + Tinker linear bias (A fixed) fits KiDS within +9 of the framework's best" +
      ("  [MUTATE: M200 <= 1e11]" if MUTATE else ""), f"chi^2 {chiF:.2f} vs {fw_best:.2f} + 9", chiF <= fw_best + 9.0)
lmb_b = np.array([x for x, y in parsF]); lmh_b = np.array([y for x, y in parsF]); o = np.argsort(lmb_b)
lmh_of = lambda v: float(np.interp(v, lmb_b[o], lmh_b[o]))
MWh, M31h = lmh_of(math.log10(6.0e10)), lmh_of(math.log10(1.2e11))
Menc_F = lambda r: 1.8e11 + float(M_nfw_msun(r, MWh, float("inf"), 1.0) + M_nfw_msun(r, M31h, float("inf"), 1.0))
R0F = brentq(lambda r: r - float(R0_pm(Menc_F(r))), 0.05, 20.0)
P(f"    MW log M200m {MWh:.2f}, M31 {M31h:.2f} (interpolated in the profiled M_b); R0 = {R0F:.3f} Mpc ({(R0F - 0.93) / 0.12:+.1f} sigma)")
check("H2 (first-written) with the KiDS-fitted halos MW + M31 give the LG an R0 within 2 sigma of 0.93 +- 0.12 Mpc",
      f"R0 = {R0F:.3f} Mpc", R0F <= 1.17)

# ================================================================================================ H1p: the parallel control on KiDS
R.banner("H1p  THE PARALLEL CONTROL ON KiDS: A in [0, b_Tinker], NFW truncated at x_t R200m (x_t scanned)")
KB = {}
for key, pb in PB.items():
    if key[2] == "fixed":
        continue
    chi, ks = kfit_best(pb)
    KB[key] = dict(chi2=chi, ks=ks, lmh=[float(LM200[k]) for k in ks], lmb=[float(LM[pb[b]["im"][ks[b]]]) for b in range(4)],
                   A=[float(pb[b]["A"][ks[b]]) for b in range(4)], cap=[float((BT if key[2] == "T" else BPS)[k]) for k in ks])
for xt in XT:
    v = KB[(1.0, xt, "T")]
    P(f"    x_t {xt:5}: chi^2 {v['chi2']:7.2f}; log M200m " + ", ".join(f"{m:.2f}" for m in v["lmh"]) + "; log M_b " +
      ", ".join(f"{m:.2f}" for m in v["lmb"]) + "; A/cap " + ", ".join(f"{a:.2f}/{c:.2f}" for a, c in zip(v["A"], v["cap"])))
xbest = min(XT, key=lambda x: KB[(1.0, x, "T")]["chi2"])
chiL = KB[(1.0, xbest, "T")]["chi2"]
edge = any(m in (LM200[0], LM200[-1]) for m in KB[(1.0, xbest, "T")]["lmh"])
P(f"    best x_t = {xbest}: chi^2 {chiL:.2f} against the framework's best (CFG21): canonical P2 {FW[('canonical', 'P2')]:.2f}, nu_mono "
  f"{FW[('canonical', 'nu_mono')]:.2f}; alt P2 {FW[('alt', 'P2')]:.2f}, nu_mono {FW[('alt', 'nu_mono')]:.2f}; halo mass at a grid edge: {edge}")
h1p = chiL <= fw_best + 9.0
check("H1p the parallel LCDM control fits KiDS within +9 of the framework's best (canonical P2) at its best x_t" +
      ("  [MUTATE: M200 <= 1e11]" if MUTATE else ""), f"chi^2 {chiL:.2f} (x_t {xbest}) vs {fw_best:.2f} + 9", h1p)

# ================================================================================================ H3: the joint tension
R.banner("H3  THE KiDS-LG TENSION FOR THE PARALLEL CONTROL (CFG21's statistic; shared: x_t, m3, m4)")


def joint(cfac, bias, bMW, bM31, MbLG, xts=None):
    """min over (x_t, halo of bin bMW, halo of bin bM31) of T; every other KiDS nuisance profiled (FP1's per-bin convention)."""
    xts = XT if xts is None else xts
    rows = []
    for xt in xts:
        pb = PB[(cfac, xt, bias)]
        kfix = [int(np.argmin(pb[b]["c2"])) for b in range(4)]
        k1 = np.arange(K)[:, None]                                                     # the MW's halo index
        k2 = k1 if bMW == bM31 else np.arange(K)[None, :]                             # M31's (the same halo if the same bin)
        mods = []
        for b in range(4):
            if b == bMW:
                mods.append(pb[b]["mod"][k1])
            elif b == bM31:
                mods.append(pb[b]["mod"][k2])
            else:
                mods.append(pb[b]["mod"][kfix[b]][None, None, :])
        shp = np.broadcast_shapes(*[m.shape[:2] for m in mods])
        dv = DAT - np.concatenate([np.broadcast_to(m, shp + (NPB,)) for m in mods], -1)
        chi = np.einsum("...i,ij,...j->...", dv, Ci, dv)
        lm1 = LM200[k1] * np.ones(shp); lm2 = LM200[k2] * np.ones(shp)
        Rr = np.ones(shp)
        for _ in range(300):
            Mt = MbLG + M_nfw_msun(Rr, lm1, xt, cfac) + M_nfw_msun(Rr, lm2, xt, cfac)
            Rn = R0_pm(Mt)
            if np.max(np.abs(Rn - Rr)) < 1e-8:
                Rr = Rn
                break
            Rr = 0.5 * (Rr + Rn)
        rows.append((xt, chi, Rr, lm1, lm2))
    cmin = min(float(np.min(r[1])) for r in rows)
    best = None
    for xt, chi, Rr, lm1, lm2 in rows:
        T = (chi - cmin) + ((Rr - 0.93) / 0.12) ** 2
        j = np.unravel_index(np.argmin(T), T.shape)
        if best is None or T[j] < best["T"]:
            best = dict(T=float(T[j]), x_t=xt, lmMW=float(lm1[j]), lmM31=float(lm2[j]), R0=float(Rr[j]), kids_excess=float(chi[j] - cmin),
                        lg=float(((Rr[j] - 0.93) / 0.12) ** 2), chi2_kids_min=cmin)
    # the KiDS-preferred point (for the record): R0 at the KiDS minimum
    for xt, chi, Rr, lm1, lm2 in rows:
        j = np.unravel_index(np.argmin(chi), chi.shape)
        if abs(float(chi[j]) - cmin) < 1e-12:
            best.update(kids_best=dict(x_t=xt, lmMW=float(lm1[j]), lmM31=float(lm2[j]), R0=float(Rr[j])))
    best["sigma_eq"] = math.sqrt(max(best["T"], 0.0))
    return best


VAR = {}
VAR["baseline"] = joint(1.0, "T", 2, 3, 1.145e11)
VAR["LG Mb 1.72e11"] = joint(1.0, "T", 2, 3, 1.72e11)
VAR["c x 0.7"] = joint(0.7, "T", 2, 3, 1.145e11)
VAR["c x 1.4"] = joint(1.4, "T", 2, 3, 1.145e11)
VAR["framework's bias formula as cap"] = joint(1.0, "PS", 2, 3, 1.145e11)
VAR["MW in bin 4"] = joint(1.0, "T", 3, 3, 1.145e11)
VAR["x_t = 1 only"] = joint(1.0, "T", 2, 3, 1.145e11, xts=[1.0])
VAR["x_t = inf only (first-written model)"] = joint(1.0, "T", 2, 3, 1.145e11, xts=[float("inf")])
for k, v in VAR.items():
    kb = v.get("kids_best", {})
    P(f"    {k:38s}: T_min {v['T']:6.1f} (~{v['sigma_eq']:.1f} sigma) at x_t {v['x_t']}, log M200m MW {v['lmMW']:.2f} / M31 {v['lmM31']:.2f}, "
      f"R0 {v['R0']:.3f} (KiDS excess {v['kids_excess']:.1f} + LG {v['lg']:.1f}); KiDS's own best: x_t {kb.get('x_t')}, "
      f"{kb.get('lmMW', float('nan')):.2f} / {kb.get('lmM31', float('nan')):.2f}, R0 {kb.get('R0', float('nan')):.3f}")
TFW = {k: v["T_min"] for k, v in C21.items()}
tb = VAR["baseline"]["T"]
h3 = tb <= 9.0
check("H3 [HEADLINE] the parallel LCDM control's KiDS-LG tension is acceptable (T_min <= 9; Duffy c, Tinker caps, LG M_b 1.145e11)",
      f"T_min {tb:.1f} (~{VAR['baseline']['sigma_eq']:.1f} sigma) at x_t {VAR['baseline']['x_t']}; the framework's (CFG21, canonical, "
      f"1.145e11): P2 {TFW['canonical|P2|1.145e+11']:.1f}, nu_mono {TFW['canonical|nu_mono|1.145e+11']:.1f}", h3)
dT = {k: TFW[k] - (VAR["baseline"]["T"] if k.endswith("1.145e+11") else VAR["LG Mb 1.72e11"]["T"]) for k in TFW}
reading = ("no reading: the control does not fit KiDS in this machinery (H1p FAIL)" if not h1p else
           "the KiDS-LG conflict is specific to the framework's phantom" if h3 else
           "standard halos meet a KiDS-LG conflict in this machinery too; the framework's excess dT is what belongs to the phantom")
P(f"\n    READING (declared, (f)): {reading}")
P("    dT = T_framework - T_LCDM (same LG M_b): " + "; ".join(f"{k}: {v:+.1f}" for k, v in dT.items()))
check("R1 (reported) variants, the framework's excess dT, the KiDS model comparison",
      "; ".join(f"{k}: T {v['T']:.1f}" for k, v in VAR.items()) + f"; KiDS chi^2 LCDM {chiL:.2f} (13 params) vs framework "
      f"{fw_best:.2f} (9)", True, load_bearing=False)
R.num("fit", dict(first_written=dict(chi2=chiF, pars=parsF, MW_lm200=MWh, M31_lm200=M31h, R0=R0F, M_R0_093=m093),
                  kids=dict((f"{k[0]}|{k[1]}|{k[2]}", v) for k, v in KB.items()), x_t_best=xbest, chi2_best=chiL,
                  framework_best={f"{k[0]}|{k[1]}": v for k, v in FW.items()}, joint=VAR, dT=dT, reading=reading,
                  controls=dict(E1=list(map(float, rc_)), interp=dint, split=dsplit, fitter=[v_a, v_b, v_ref])))
nf = R.write()
sys.exit(1 if nf else 0)
