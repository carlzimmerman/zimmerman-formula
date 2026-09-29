#!/usr/bin/env python3
"""CFG184 -- how much of the KURVS outer sigma can be beam-smeared rotation, and what pressure-support scale the data then allow.

Frozen criteria: FROZEN_CRITERIA.md in this directory (cb1e8a77b), committed before any number and before the measured V(R) markers
(kurvs_rc_points.csv) were read; they are NOT read here (reserved for CFG189).
  forward model  thin disc; V_los = V(R) sin i cos phi; I ~ exp(-R/R_d); intrinsic V(R) = the authors' exponential-disc model curve
                 deprojected by sin i_SFR (primary) or a Freeman disc normalised to the tabulated V(R_max) (variant);
                 kernel = Gaussian PSF (FWHM 0.57'', variants 0.32/0.82) x box spaxel bin (0.6'', variants 0.3/0.9); the profile value
                 is the median over the +-0.3'' pseudo-slit; sigma_bs^2 = kernel- and intensity-weighted variance of V_los.
  radii          exactly CFG141's: the side(s) reaching R_max (interpolated there), else the outermost three unclipped points (1/e^2).
  outputs        f_bs = sigma_bs^2 / sigma_out^2 per disc; s_eff(s) = the uniform s giving the same Delta'_flat as the sigma_int
                 pipeline; the three laws' cells, break-evens and fit points with sigma_int; the Girard+2021 scenario (reported only).
MUTATE=1: FWHM x 3 (f_bs must rise, s_eff(1) fall).  MUTATE=2: FWHM -> 0.01'', bin -> 0.1'' (f_bs -> 0, s_eff(1) -> 1).
Turbulent support cannot be separated from unresolved or non-circular motion with these data: sigma_int is an upper bound on the
pressure-bearing dispersion, not a measurement.  kappa = 1/2 and Omega_c h^2 stay fitted.
Run: python3 campaign_fresh_gravity/CFG184_kurvs_beam_smearing/cfg184_beam_smearing.py
"""
import os, sys, io, math, csv, json, contextlib
import numpy as np
from scipy.optimize import brentq
from scipy.special import erf, i0, i1, k0, k1
from scipy.integrate import quad

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
import CFG7_common as C

MODE = os.environ.get("MUTATE", "").strip()
assert MODE in ("", "1", "2")
R = C.Report("cfg184_beam_smearing" + (f"_MUTATE{MODE}" if MODE else ""), False)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())

F141 = os.path.join(CFG, "CFG141_kurvs_measured_sigma.py")
src = open(F141).read()
g141 = {"__file__": F141, "__name__": "cfg141"}
_saved = os.environ.pop("MUTATE", None)                         # the exec'd pipeline runs unmutated in every mode of this lane
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src[:src.index("# ================================================================== C1 / C2")], "CFG141", "exec"), g141)
finally:
    if _saved is not None:
        os.environ["MUTATE"] = _saved
KU2, SP, KR, PROF = g141["KU2"], g141["SP"], g141["g140"]["KR"], g141["PROF"]
A0, E, gbar, gpred, slope, KPC = g141["A0"], g141["E"], g141["gbar"], g141["gpred"], g141["slope"], g141["KPC"]
OM = g141["g140"]["OM"]
LN10, FOOT = math.log(10), "canonical"
AT = os.path.join(REPO, "data_assembly", "arxiv_tables")
INTEG = {int(r["kurvs_id"]): r for r in csv.DictReader(open(os.path.join(AT, "kurvs2023_integrated.csv")))}
VEL = {int(r["kurvs_id"]): r for r in csv.DictReader(open(os.path.join(AT, "kurvs2023_velocities_at_radii.csv")))}
MODEL = {}
for r in csv.DictReader(open(os.path.join(AT, "kurvs_rc_profiles", "kurvs_rc_model_curves.csv"))):     # the authors' MODEL curves only
    MODEL.setdefault(int(r["kurvs_id"]), []).append((float(r["R_kpc"]), float(r["v_model_obs_kms"])))
IDS = [int(o["name"].split("-")[1]) for o in KU2]


# ------------------------------------------------------------------ geometry: the paper's cosmology (H0 = 70, Om = 0.3)
def kpc_per_arcsec(z, H0=70.0, om=0.3):
    dc = quad(lambda zz: 1.0 / math.sqrt(om * (1 + zz) ** 3 + 1 - om), 0, z)[0] * 299792.458 / H0 * 1e3   # kpc
    return dc / (1 + z) * math.pi / (180 * 3600)


# ------------------------------------------------------------------ CFG141's radii and weights, re-implemented (C1 checks it)
def radii_used(kid, Rmax):
    pts = [(abs(Rk), s, 0.5 * (eu + el), Rk >= 0) for Rk, s, eu, el, cl in PROF.get(kid, []) if not cl]
    reach = []
    for side in (True, False):
        sp = sorted((p[0], p[1], p[2]) for p in pts if p[3] == side)
        if sp and sp[-1][0] >= Rmax and sp[0][0] <= Rmax:
            rr, ss, ee = zip(*sp)
            reach.append((Rmax, float(np.interp(Rmax, rr, ss)), float(np.interp(Rmax, rr, ee))))
    if reach:
        s = float(np.mean([v[1] for v in reach]))
        return dict(status="reaches R_max", radii=[Rmax] * len(reach), w=[1.0] * len(reach), s=s)
    out3 = sorted(pts, key=lambda p: -p[0])[:3]
    rr3 = [p[0] for p in out3]; s3 = np.array([p[1] for p in out3]); e3 = np.array([p[2] for p in out3])
    w = 1 / e3 ** 2
    return dict(status="outermost three", radii=rr3, w=list(w / w.sum()), s=float(np.sum(w * s3) / np.sum(w)))


# ------------------------------------------------------------------ intrinsic rotation curves
def v_model_folded(kid, sini):
    pts = sorted(MODEL[kid])
    Rs = np.array([p[0] for p in pts]); Vs = np.array([p[1] for p in pts])
    rg = np.linspace(0, float(np.max(np.abs(Rs))), 400)
    vp = np.interp(rg, Rs, Vs); vm = np.interp(-rg, Rs, Vs)
    vv = 0.5 * (np.abs(vp) + np.abs(vm)) / sini
    return lambda R: np.interp(R, rg, vv, right=vv[-1])


def v_freeman(Rd, Vmax_at, Rmax):
    def shape(R):
        y = np.maximum(np.asarray(R, float), 1e-6) / (2 * Rd)
        return np.sqrt(np.maximum(y ** 2 * (i0(y) * k0(y) - i1(y) * k1(y)), 0))
    norm = Vmax_at / float(shape(Rmax))
    return lambda R: norm * shape(R)


# ------------------------------------------------------------------ the forward model
XG = np.arange(-4.0, 4.0001, 0.02)
YG = np.arange(-3.0, 3.0001, 0.02)
XX, YY = np.meshgrid(XG, YG)


def k1d(u, fwhm, b):
    sg = max(fwhm, 1e-4) / 2.3548
    return (erf((u + b / 2) / (math.sqrt(2) * sg)) - erf((u - b / 2) / (math.sqrt(2) * sg))) / (2 * b)


def sky_fields(Vfun, inc_deg, Rd_kpc, scale):
    ci, si = math.cos(math.radians(inc_deg)), math.sin(math.radians(inc_deg))
    Ras = np.sqrt(XX ** 2 + (YY / ci) ** 2)                      # arcsec in the disc plane
    Rk = Ras * scale
    cphi = np.where(Ras > 0, XX / np.maximum(Ras, 1e-12), 0.0)
    V = Vfun(Rk) * si * cphi
    I = np.exp(-Rk / Rd_kpc)
    return I, I * V, I * V * V


def sigma_bs_at(fields, x_as, fwhm, b):
    I, IV, IV2 = fields
    wx = k1d(XG - x_as, fwhm, b)
    vals = []
    for ys in (-0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3):
        wy = k1d(YG - ys, fwhm, b)
        m0 = wy @ I @ wx; m1 = wy @ IV @ wx; m2 = wy @ IV2 @ wx
        vals.append(max(m2 / m0 - (m1 / m0) ** 2, 0.0))
    return math.sqrt(float(np.median(vals)))


FWHM0, BIN0 = 0.57, 0.6
FW = {"": 1.0, "1": 3.0, "2": None}[MODE]


def run_variant(kid, vmodel="model", fwhm=FWHM0, b=BIN0, rdx=1.0, incsrc="sfr"):
    o = KU2[IDS.index(kid)]
    it, vt = INTEG[kid], VEL[kid]
    z = float(it["z_halpha"]); scale = kpc_per_arcsec(z)
    inc = float(it["inc_sfr_deg"]) if incsrc == "sfr" else float(it["inc_star_deg"])
    Rd = float(it["reff_kpc"]) / 1.68 * rdx
    Rmax = float(vt["R_halpha_max_kpc"])
    if vmodel == "model":
        Vf = v_model_folded(kid, math.sin(math.radians(inc)))
    else:
        Vf = v_freeman(float(it["reff_kpc"]) / 1.68, float(vt["v_at_last_point_kms"]), Rmax)
    ru = radii_used(kid, Rmax)
    flds = sky_fields(Vf, inc, Rd, scale)
    sb2 = sum(w * sigma_bs_at(flds, r / scale, fwhm, b) ** 2 for r, w in zip(ru["radii"], ru["w"]))
    return dict(sbs=math.sqrt(sb2), sout=o["sig"], f=sb2 / o["sig"] ** 2, status=ru["status"], radii=ru["radii"], scale=scale)


# ================================================================== controls
R.banner("C0-C3  CONTROLS")
sc = kpc_per_arcsec(1.54)
check("C0 CONTROL: the angular scale at z = 1.54 (H0 70, Om 0.3) is ~8.47 kpc/arcsec (groundwork value 8.463-8.472 at z 1.5-1.6)",
      f"{sc:.4f} kpc/arcsec", abs(sc - 8.47) < 0.02)
c1 = [(kid, radii_used(kid, float(VEL[kid]["R_halpha_max_kpc"]))["s"], KU2[IDS.index(kid)]["sig"]) for kid in IDS]
check("C1 CONTROL: my re-implementation of CFG141's radii/weights reproduces its sigma_out for every disc (1e-9)",
      "; ".join(f"K{k} {a:.3f}/{b_:.3f}" for k, a, b_ in c1), all(abs(a - b_) < 1e-9 for _, a, b_ in c1))
flat = lambda Rk: np.full_like(np.asarray(Rk, float), 150.0)
c2 = sigma_bs_at(sky_fields(flat, 0.0, 2.5, 8.4), 1.2, FWHM0, BIN0)
check("C2 CONTROL: a flat V(R) seen face-on (i = 0) gives sigma_bs = 0 (1e-6 km/s)", f"{c2:.2e} km/s", c2 < 1e-6)
c3 = sigma_bs_at(sky_fields(flat, 60.0, 2.5, 8.4), 1.2, 1e-4, 0.1)
check("C3 CONTROL: sigma_bs -> 0 as FWHM -> 0 and bin -> 0.1'' for a flat V(R) (0.5 km/s)", f"{c3:.3f} km/s", c3 < 0.5)
# post hoc (added after the first run, kept as *_firstrun*): C3's 0.5 km/s line was too tight -- a 0.1'' spaxel at the pseudo-slit's
# off-axis positions (|y_s| up to 0.3'') still spans a real V_los gradient; the limit itself is checked with a 0.01'' bin.
c3b = sigma_bs_at(sky_fields(flat, 60.0, 2.5, 8.4), 1.2, 1e-4, 0.01)
check("C3-posthoc (reported) the same with bin -> 0.01'': sigma_bs -> 0", f"{c3b:.3f} km/s", c3b < 0.5, load_bearing=False)

# ================================================================== per-disc smearing
R.banner("PER DISC: sigma_bs at CFG141's radii and f_bs = sigma_bs^2/sigma_out^2  (primary: model V(R), FWHM 0.57'', bin 0.6'', R_d, i_SFR)")
fw_main = FWHM0 if not MODE else (FWHM0 * 3 if MODE == "1" else 0.01)
b_main = BIN0 if MODE != "2" else 0.1
prim = {kid: run_variant(kid, fwhm=fw_main, b=b_main) for kid in IDS}
nomin = {kid: run_variant(kid) for kid in IDS} if MODE else prim
for kid in IDS:
    p_ = prim[kid]
    P(f"  KURVS-{kid:2d} ({p_['status']:15s} radii {', '.join(f'{r:.2f}' for r in p_['radii'])} kpc): sigma_out {p_['sout']:5.1f}  "
      f"sigma_bs {p_['sbs']:5.1f} km/s  f_bs {p_['f']:.3f}")
fmean = float(np.mean([prim[k]["f"] for k in IDS])); fmed = float(np.median([prim[k]["f"] for k in IDS])); fmax = max(prim[k]["f"] for k in IDS)
P(f"  sample: mean f_bs {fmean:.3f}, median {fmed:.3f}, max {fmax:.3f}")
R.num("primary", {str(k): v for k, v in prim.items()})

# variants (main run only)
VARS = []
if not MODE:
    for vm in ("model", "freeman"):
        for fwhm in (0.32, 0.57, 0.82):
            for b in (0.3, 0.6, 0.9):
                for rdx in (0.7, 1.0, 1.5):
                    for incsrc in ("sfr", "star"):
                        rr = {kid: run_variant(kid, vm, fwhm, b, rdx, incsrc) for kid in IDS}
                        VARS.append(dict(vm=vm, fwhm=fwhm, b=b, rdx=rdx, inc=incsrc, fmean=float(np.mean([rr[k]["f"] for k in IDS])),
                                         fmax=max(rr[k]["f"] for k in IDS), per={str(k): rr[k]["f"] for k in IDS},
                                         sbs={str(k): rr[k]["sbs"] for k in IDS}))
    VARS.sort(key=lambda v: v["fmean"])
    lo, hi = VARS[0], VARS[-1]
    P(f"\n  variants ({len(VARS)}): sample-mean f_bs from {lo['fmean']:.3f} ({lo['vm']}, FWHM {lo['fwhm']}, bin {lo['b']}, R_d x{lo['rdx']}, i_{lo['inc']})"
      f" to {hi['fmean']:.3f} ({hi['vm']}, FWHM {hi['fwhm']}, bin {hi['b']}, R_d x{hi['rdx']}, i_{hi['inc']}); the largest single-disc f_bs "
      f"{max(v['fmax'] for v in VARS):.3f}")
    R.num("variants", VARS)


# ================================================================== the pipeline with sigma_int (CFG175's machinery, three laws)
def alpha_k21(x):                                                # CFG160's, verbatim
    x = min(max(x, 0.0), 4.0)
    return -0.146 * x * x + 1.204 * x + 1.475


def pooled(d, s):                                                # CFG140's
    w = 1 / s ** 2
    m = float(np.sum(w * d) / np.sum(w)); e = float(1 / math.sqrt(np.sum(w)))
    chi = float(np.sum(w * (d - m) ** 2)); dof = max(len(d) - 1, 1)
    if chi / dof > 1:
        e *= math.sqrt(chi / dof)
    return m, e


def terms(objs, sig_over=None):
    V = np.array([o["V"] for o in objs]); eV = np.array([o["eV"] for o in objs])
    sg = np.array([o["sig"] for o in objs]) if sig_over is None else np.array(sig_over)
    es = np.array([o["esig"] for o in objs]); Rr = np.array([o["R"] for o in objs]); sm = np.array([o["sm"] for o in objs])
    inc = [math.radians(o["inc"]) if np.isfinite(o["inc"]) and o["inc"] > 1 else math.radians(60) for o in objs]
    ti = np.array([2 * o["V"] ** 2 * o["einc"] / math.tan(i) for o, i in zip(objs, inc)])
    ak = np.array([alpha_k21(o["R"] / (1.68 * o["Rd"]) - 1.0) for o in objs])
    return dict(V=V, eV=eV, sg=sg, es=es, R=Rr, sm=sm, ti=ti, ak=ak)


def DS(T, s, gp, sl):
    al = s * T["ak"]
    vc2 = T["V"] ** 2 + al * T["sg"] ** 2
    go = vc2 * 1e6 / (T["R"] * KPC)
    dlog = np.sqrt((2 * T["V"] * T["eV"]) ** 2 + (2 * al * T["sg"] * T["es"]) ** 2 + T["ti"] ** 2) / vc2 / LN10
    return np.log10(go / gp), np.hypot(dlog, sl * T["sm"])


def tratio(z, om=OM):
    k = math.sqrt((1 - om) / om)
    return math.asinh(k * (1 + z) ** -1.5) / math.asinh(k)


LAWS = {"flat": lambda z: 1.0, "rival": E, "T": tratio}
LAWN = ("flat", "rival", "T")
TS = terms(SP)
_pc = {}


def pred(objs, key, mu, law, sparc=False):
    kk = (key, round(mu, 12), law)
    if kk not in _pc:
        gb = np.array([gbar(o, 0.67, 0.0, True) if sparc else gbar(o, mu, 0.0) for o in objs])
        a = np.array([A0[FOOT] * LAWS[law](o["z"]) for o in objs])
        _pc[kk] = (np.array([gpred(g, aa) for g, aa in zip(gb, a)]), np.array([slope(g, aa) for g, aa in zip(gb, a)]))
    return _pc[kk]


def delta(T, mu, s, law):
    gp, sl = pred(KU2, "KURVS", mu, law)
    k, ek = pooled(*DS(T, s, gp, sl))
    ga, sa = pred(SP, "SPARC", 0.67, law, True)
    an, ea = pooled(*DS(TS, s, ga, sa))
    return k - an, math.hypot(ek, ea)


GRID = np.exp(np.linspace(math.log(0.01), math.log(30.0), 36))


def root_mu(T, s, law, target=0.0):
    fn = lambda mu: (lambda d: d[0] - target * d[1])(delta(T, mu, s, law))
    vals = [fn(m) for m in GRID]
    for lo_, hi_, flo, fhi in zip(GRID[:-1], GRID[1:], vals[:-1], vals[1:]):
        if flo * fhi < 0:
            return float(brentq(fn, lo_, hi_, xtol=1e-6, rtol=1e-6))
    return float("nan")


def s0(T, law, mu=0.67):
    fn = lambda s: delta(T, mu, s, law)[0]
    if fn(0.0) > 0:
        return float("-inf")
    if fn(6.0) < 0:
        return float("inf")
    return float(brentq(fn, 0.0, 6.0, xtol=1e-6))


def s_eff(T_int, s):
    target = delta(T_int, 0.67, s, "flat")[0]
    fn = lambda sp_: delta(TOUT, 0.67, sp_, "flat")[0] - target
    if fn(0.0) > 0:
        return 0.0
    return float(brentq(fn, 0.0, 6.0, xtol=1e-7))


fs = lambda v: "< 0" if v == float("-inf") else ("> 6" if v == float("inf") else f"{v:.3f}")
TOUT = terms(KU2)
R.banner("C4  CONTROL: with sigma_int = sigma_out the pipeline reproduces CFG160's cell and CFG175's T cell")
c4 = {law: delta(TOUT, 0.67, 1.0, law)[0] for law in LAWN}
check("C4 CONTROL: flat +0.1441 / rival -0.0060 (CFG160) and T +0.3227 (CFG175) at mu 0.67, s = 1 (1e-4)",
      f"flat {c4['flat']:+.4f}, rival {c4['rival']:+.4f}, T {c4['T']:+.4f}",
      abs(c4["flat"] - 0.1441) < 1e-4 and abs(c4["rival"] + 0.0060) < 1e-4 and abs(c4["T"] - 0.3227) < 1e-4)


def sig_int(res):
    return [math.sqrt(max(KU2[IDS.index(k)]["sig"] ** 2 - res[k]["sbs"] ** 2, 0.0)) for k in IDS]


def evaluate(label, res):
    T_int = terms(KU2, sig_int(res))
    out = dict(seff={}, cell={}, be={}, s0={})
    for s in (1.0, 1.42, 1.62, 1.69, 3.0):
        out["seff"][f"{s:.2f}"] = s_eff(T_int, s)
    for s in (0.0, 1.0):
        out["cell"][f"{s:.2f}"] = {law: delta(T_int, 0.67, s, law) for law in LAWN}
    for s in (1.0, 1.42, 1.62, 1.69, 3.0):
        out["be"][f"{s:.2f}"] = {law: root_mu(T_int, s, law) for law in LAWN}
    out["s0"] = {law: s0(T_int, law) for law in LAWN}
    P(f"  [{label}]  s_eff: " + ", ".join(f"s {k} -> {v:.3f}" for k, v in out["seff"].items()))
    for s in ("0.00", "1.00"):
        P(f"      cell s {s}: " + ";  ".join(f"{law} {out['cell'][s][law][0]:+.3f} ({out['cell'][s][law][0] / out['cell'][s][law][1]:+.1f})"
                                           for law in LAWN))
    for s in ("1.00", "1.42", "1.62", "1.69", "3.00"):
        P(f"      break-evens s {s}: " + ";  ".join(f"{law} {out['be'][s][law]:.3f}" for law in LAWN))
    P("      fit points s0 at mu 0.67: " + ";  ".join(f"{law} {fs(v)}" for law, v in out["s0"].items()))
    return out


R.banner("THE PRESSURE-SUPPORT SCALE THE DATA ALLOW, AND THE THREE LAWS WITH sigma_int (CFG162's s_mid = 0.67; CFG175 fit points flat 0.39, rival 1.03, T < 0)")
ev_prim = evaluate("primary" if not MODE else f"MUTATE={MODE}", prim)
ev = {"primary": ev_prim}
if not MODE:
    hi_res = {kid: dict(sbs=hi["sbs"][str(kid)]) for kid in IDS}
    ev["max_smearing"] = evaluate(f"maximal-smearing variant ({hi['vm']}, FWHM {hi['fwhm']}, bin {hi['b']}, R_d x{hi['rdx']}, i_{hi['inc']})",
                                  hi_res)
    # the Girard+2021 scenario (reported only): the pressure-bearing dispersion is the molecular layer's, s_eff = s / 6.0
    gs = 1.0 / 2.45 ** 2
    P(f"\n  Girard+2021 scenario (REPORTED ONLY; not the default): K21 at s_eff = {gs:.3f}: " + ";  ".join(
        f"{law} {delta(TOUT, 0.67, gs, law)[0]:+.3f} ({delta(TOUT, 0.67, gs, law)[0] / delta(TOUT, 0.67, gs, law)[1]:+.1f})" for law in LAWN))
    # post hoc (added after the first run; reported, not a frozen reading): s_eff(1) over ALL 108 declared variants, so the reader can see
    # whether only the extreme corner crosses s_mid = 0.67
    se_all = []
    for v in VARS:
        rr_ = {kid: dict(sbs=v["sbs"][str(kid)]) for kid in IDS}
        se_all.append(s_eff(terms(KU2, sig_int(rr_)), 1.0))
    se_all = np.array(se_all)
    P(f"\n  POST HOC (reported): s_eff(1) over all {len(se_all)} declared variants: median {np.median(se_all):.3f}, 16-84% "
      f"[{np.percentile(se_all, 16):.3f}, {np.percentile(se_all, 84):.3f}], min {se_all.min():.3f}; fraction below s_mid 0.67: "
      f"{np.mean(se_all < 0.67):.3f}; with the model V(R) only: fraction below 0.67 = "
      f"{np.mean([s_ < 0.67 for s_, v in zip(se_all, VARS) if v['vm'] == 'model']):.3f}, min "
      f"{min(s_ for s_, v in zip(se_all, VARS) if v['vm'] == 'model'):.3f}")
    R.num("posthoc_seff_all", dict(values=[float(x) for x in se_all], median=float(np.median(se_all)), frac_below=float(np.mean(se_all < 0.67))))
R.num("evaluations", {k: dict(seff=v["seff"], s0={l_: (None if not np.isfinite(x) else x) for l_, x in v["s0"].items()},
                              cell={s: {l_: list(x) for l_, x in d.items()} for s, d in v["cell"].items()}, be=v["be"]) for k, v in ev.items()})

# ================================================================== headline
R.banner("HEADLINE")
se1 = ev_prim["seff"]["1.00"]
if MODE == "1":
    se_nom = evaluate("nominal (for the MUTATE comparison)", nomin)["seff"]["1.00"]
    fnom = float(np.mean([nomin[k]["f"] for k in IDS]))
    check("MUTATE=1 [control]: FWHM x 3 raises the sample-mean f_bs and lowers s_eff(1)", f"f_bs {fnom:.3f} -> {fmean:.3f}; s_eff(1) {se_nom:.3f} -> {se1:.3f}",
          fmean > fnom and se1 < se_nom)
    summary = f"MUTATE=1: mean f_bs {fmean:.3f}, s_eff(1) {se1:.3f}"
elif MODE == "2":
    main = os.path.join(LANE, "cfg184_beam_smearing_results.json")
    msum = json.load(open(main))["numbers"]["summary"] if os.path.exists(main) else None
    summary = "minor" if (fmean <= 0.10 and se1 >= 0.9) else "not minor"
    changed = msum is not None and (msum.startswith("Beam smearing is minor") != (summary == "minor"))
    check("MUTATE=2 [control]: FWHM -> 0.01'', bin -> 0.1'' drives f_bs -> ~0 and s_eff(1) -> ~1; the headline changes if the main run found "
          "non-negligible smearing", f"mean f_bs {fmean:.4f}, s_eff(1) {se1:.4f}; main: {msum}",
          fmean < 0.01 and se1 > 0.98 and (changed or (msum or "").startswith("Beam smearing is minor")))
else:
    se1_hi = ev["max_smearing"]["seff"]["1.00"]
    if fmean <= 0.10 and se1 >= 0.9:
        summary = (f"Beam smearing is minor: primary mean f_bs {fmean:.3f} (max disc {fmax:.3f}), s_eff(1) = {se1:.3f}; K21 stays where CFG162 "
                   f"placed it")
    elif se1_hi < 0.67:
        summary = f"Beam smearing can move K21 across the crossing: the maximal-smearing variant gives s_eff(1) = {se1_hi:.3f} < 0.67"
    else:
        summary = f"Non-diagnostic: s_eff(1) from {se1_hi:.3f} (maximal smearing) to {se1:.3f} (primary)"
    if fmean <= 0.10 and se1 >= 0.9 and se1_hi < 0.67:
        summary += f"; but the maximal-smearing variant gives s_eff(1) = {se1_hi:.3f} < 0.67 (the crossing)"
    elif fmean <= 0.10 and se1 >= 0.9:
        summary += f"; the maximal-smearing variant gives s_eff(1) = {se1_hi:.3f}"
    check("H1 [HEADLINE, reported] the declared reading", summary, True, load_bearing=False)
R.num("summary", summary)
P(f"\n    SUMMARY (declared): {summary}")
nf = R.write(LANE)
raise SystemExit(1 if nf else 0)
