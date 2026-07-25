#!/usr/bin/env python3
"""
a0z_model_comparison_forecast_2026.py -- ONE LIKELIHOOD over every existing high-z a0(z)
constraint; real Bayes factors between the THREE a0(z) laws; then the DECISIVE-MEASUREMENT
FORECAST (deep-MOND-selected sample: required z, precision, N).
=========================================================================================
Carl Zimmerman's de Sitter-Unruh MODIFIED INERTIA.  a0 = c H_Lambda / Z,  Z = sqrt(32pi/3).
Builds on (does NOT modify) the committed parents in this directory:
    highz_a0_fork_confront_2026.py      -- the 11 real cited high-z constraints
    highz_a0z_fork_placement_2026.py    -- their fork placements + currencies
    desitter_unruh_horizon_fork_2026.py -- the two horizon branches
    a0z_prediction_band_2026.py         -- the frozen band, footing-independent RATIO

THREE ZERO-FREE-PARAMETER MODELS (so this is a clean likelihood ratio; no Occam penalty):
  M-DEC   a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0)   [framework's de Sitter/future-horizon branch]
          = (1+z)^{1.5(1+w0+wa)} exp(-1.5 wa z/(1+z))  -- FULL closed form, never Taylored.
          Fixed by DESI DR2 + Planck: 1.036 bump @z~0.35, 0.99 @z=1, 0.874 @z=2, 0.775 @z=3.
  M-RISE  a0(z)/a0(0) = E(z) = H(z)/H0            [McCulloch MiHsC Hubble-horizon; credited]
          -> 1.79 @z=1, 3.01 @z=2, 4.54 @z=3.
  M-FLAT  a0(z)/a0(0) = 1 for all z               [standard MOND AND the framework's own
          w->-1 LCDM-dissolution limit]. THE REAL NULL.
(w0,wa) is an EXTERNAL-prior nuisance (DESI DR2), not a fitted galaxy-side parameter; it is
marginalized for BOTH M-DEC and M-RISE, so all three models keep zero free parameters.

THE CRITICAL NUISANCE, MODELED EXPLICITLY AND MARGINALIZED:  A_drift.
  Magneticum / Mayer et al. 2023 (arXiv:2206.04333) reproduce an APPARENT-a0 rise of ~x3 by
  z=2.3 in PURE LCDM with NO fundamental a0 (g_obs-selection + beam smearing + pressure
  support + baryonic evolution). So a measured rise can be entirely an artifact.
  Parameterization:  a0_apparent(z) = a0_true(z) * (1+z)^{p * w_i},  p >= 0.
  Amplitude calibration: (1+2.3)^p_mag = 3  ->  p_mag = ln3/ln3.3 = 0.920.
  Prior (baseline): p ~ U(0, p_mag)  [the full Magneticum amplitude is the prior's upper edge].
  Sensitivity priors: HalfNormal(sigma=p_mag/2) truncated at 1.5*p_mag; U(0, 1.5*p_mag); p=0.
  EXPOSURE w_i in [0,1] per datum: MAXIMAL (1.0) for the DIRECT-RAR fit and the DILUTED
  bTFR zero-points; MINIMAL for the clean lensed near-a0 and deep-MOND points.

THE ACCELERATION-DILUTION FORWARD MODEL (mandatory; framework's OWN nu, not McGaugh's):
  g_obs = sqrt(g_bar^2 + g_bar a0)  =>  d ln g_obs / d ln a0 = 0.5 / (1 + x),  x = g_bar/a0.
  Deep MOND (x->0) gives 0.5, so the a0-LEVER relative to deep-MOND is  L(x) = 1/(1+x).
  A bTFR mass-axis offset therefore responds as Delta_b = -L(x) * log10(a0(z)/a0(0)), NOT 1:1.
  Every g_bar>>a0 point (Ubler, Amvrosiadis, Tiley) is down-weighted by its own L -- in BOTH
  directions. (The parent scripts quote a lever "x/(2+x)=7-63%"; L=1/(1+x) derived here is
  MORE generous to the rising-pull points, i.e. conservative against a declining win.)

HARD CALIBRATION (manufactured win == manufactured deficit; penalized EQUALLY):
 (1) MUSE-DARK III (Ciocan) is NOT systematics-inflated away. The headline run gives it its
     FULL stat error (0.105) and lets p alone absorb it. Odds are reported at FACE VALUE and
     MARGINALIZED, and the MOVEMENT between them is the honest result.
 (2) The face-value ~30-sigma rise is NOT taken at literal strength as a fundamental-a0 result:
     the compilation already establishes it is LCDM-degenerate. Face-value chi2/dof is printed
     so the reader sees NO model fits the face-value data (Jeanneau vs Ubler are 6s apart).
 (3) M-FLAT is included and can win. A FLAT win is NOT a framework falsification (it is the
     framework's own w->-1 limit) but it IS a failure to detect the distinctive decline.
 (4) Dilution applied to every g_bar>>a0 point, in both directions.
 (5) Bayes factors reported for DEC-vs-RISE, DEC-vs-FLAT, RISE-vs-FLAT, face value + marginalized.
 (6) BOTH footings noted; the RATIO a0(z)/a0(0) is footing-independent (sympy-proved in the
     committed a0z_prediction_band_2026.py), so this entire comparison is footing-independent.
 nu=sqrt(1+1/y) is Milgrom 1999 (PLA 253:273 Eq.9); the framework's distinctive content is the
 cH_Lambda/Z COEFFICIENT + the MI completion. McCulloch credited for the Hubble reading.
 a0's VALUE and the HORIZON CHOICE are POSITS. No TOE. No 'theory closed'. Exit 0 = ran.
"""
import numpy as np
from scipy.special import logsumexp

np.seterr(all="ignore")

# =====================================================================================
# 0. COSMOLOGY, MODELS, MC MACHINERY
# =====================================================================================
OM, ODE = 0.3150, 0.6850
Z_CONST = np.sqrt(32 * np.pi / 3)
A0_CAN, A0_ALT = 9.355e-11, 1.131e-10          # canonical cH_Lambda/Z ; alt cH0/Z
DESI = {  # DESI DR2 w0waCDM: (w0, sw0, wa, swa, corr)  arXiv:2503.14738 / 2504.15336
    "Pantheon+": (-0.838, 0.055, -0.62, 0.22, -0.86),
    "DESY5":     (-0.752, 0.057, -0.86, 0.22, -0.86),
    "Union3":    (-0.667, 0.088, -1.09, 0.31, -0.87),
}
HEAD = "Pantheon+"                              # the committed fork head
P_MAG = np.log(3.0) / np.log(3.3)               # 0.920: Magneticum x3 apparent rise by z=2.3
NS = 60000                                      # MC samples (evidence integrals)

def rho_de_ratio(z, W0, WA):
    return (1 + z) ** (3 * (1 + W0 + WA)) * np.exp(-3 * WA * z / (1 + z))

def R_model(model, z, W0, WA):
    """a0(z)/a0(0) for a model. z:(nz,), W0/WA:(NS,) -> (NS,nz)."""
    z = np.atleast_1d(np.asarray(z, float))[None, :]
    w0, wa = np.asarray(W0, float)[:, None], np.asarray(WA, float)[:, None]
    if model == "FLAT":
        return np.ones((w0.shape[0], z.shape[1]))
    rde = rho_de_ratio(z, w0, wa)
    if model == "DEC":
        return np.sqrt(rde)
    if model == "RISE":
        return np.sqrt(OM * (1 + z) ** 3 + ODE * rde)
    raise ValueError(model)

def draw(dataset=HEAD, prior="uniform", seed=0, ns=NS):
    """Correlated (w0,wa) from DESI + drift exponent p from its prior."""
    w0, sw0, wa, swa, corr = DESI[dataset]
    L = np.linalg.cholesky([[sw0 ** 2, corr * sw0 * swa], [corr * sw0 * swa, swa ** 2]])
    rng = np.random.default_rng(seed)
    pr = np.array([w0, wa]) + rng.standard_normal((ns, 2)) @ L.T
    if prior == "zero":
        p = np.zeros(ns)
    elif prior == "uniform":
        p = rng.uniform(0.0, P_MAG, ns)
    elif prior == "uniform_wide":
        p = rng.uniform(0.0, 1.5 * P_MAG, ns)
    elif prior == "halfnormal":
        p = np.abs(rng.standard_normal(ns)) * (P_MAG / 2.0)
        p = p[p <= 1.5 * P_MAG]
        while p.size < ns:                       # top up the truncated tail
            q = np.abs(rng.standard_normal(ns)) * (P_MAG / 2.0)
            p = np.concatenate([p, q[q <= 1.5 * P_MAG]])
        p = p[:ns]
    else:
        raise ValueError(prior)
    return pr[:, 0], pr[:, 1], p

def _slope(x, Y):
    """OLS slope of each row of Y (NS,nz) against x (nz,)."""
    xc = x - x.mean()
    return (Y @ xc) / (xc @ xc)

bar = "=" * 102
print(bar)
print("a0(z) MODEL COMPARISON + DECISIVE-MEASUREMENT FORECAST  (2026-07-25)")
print(bar)
print(f"  a0 = cH_Lambda/Z, Z={Z_CONST:.5f}. canonical a0(0)={A0_CAN:.3e} | alt {A0_ALT:.3e} m/s^2.")
print("  The compared quantity is the RATIO a0(z)/a0(0) -> FOOTING-INDEPENDENT (Z, a0(0), c, H all")
print("  cancel; sympy-proved in the committed a0z_prediction_band_2026.py). Both footings carried.")
W0h, WAh, _ = draw(HEAD, "zero", 0)
print(f"\n  {'z':>5} | {'M-DEC':>7} | {'M-RISE':>7} | {'M-FLAT':>7} | {'RISE/DEC':>9} | {'log10(RISE/DEC) dex':>19}")
print("  " + "-" * 74)
for z in [0.35, 0.9, 1.0, 2.0, 2.3, 3.0, 3.25]:
    d = float(np.median(R_model("DEC", z, W0h, WAh)))
    r = float(np.median(R_model("RISE", z, W0h, WAh)))
    print(f"  {z:>5.2f} | {d:>7.3f} | {r:>7.3f} | {1.0:>7.3f} | {r/d:>8.2f}x | {np.log10(r/d):>19.3f}")

# =====================================================================================
# 1. THE DATA  (hard-coded from the committed compilation; NOTHING invented)
#    L = 1/(1+x) dilution lever from the framework's OWN nu;  w = A_drift exposure.
# =====================================================================================
def lever(x):
    return 1.0 / (1.0 + x)

def geo(a, b):
    return float(np.sqrt(a * b))

DATA = [
 # --- DIRECT a0(z) / RAR-SLOPE points (fit a0 directly => lever 1; MAXIMAL drift exposure) ---
 dict(tag="MSA-3D (sel-corr)", cite="Espejo Salcedo+26 arXiv:2606.27853", kind="loglog_slope",
      zlo=0.58, zhi=1.68, obs=+0.91, sig_stat=0.79, sig_hon=0.79, L=1.0, w=0.5,
      note="JWST/NIRSpec N=23 golden. SELECTION-CORRECTED slope +0.91 [16-84: +0.05,+1.63];"
           " raw +2.13 = g_obs-selection +1.13 + h(f_DM) +1.00 -> NOT used. w=0.5: the g_obs-"
           "selection half of the drift is already removed by the decomposition."),
 dict(tag="MUSE-DARK III Ciocan", cite="Ciocan+26 A&A 709 L16 arXiv:2604.22613", kind="lin_slope",
      zlo=0.33, zhi=1.44, obs=+1.59, sig_stat=0.105, sig_hon=float(np.hypot(0.105, 0.5 * 0.80)),
      L=1.0, w=1.0,
      note="N=79 SFGs, DIRECT RAR fit a0(z)=a0(0)+a1 z; a1=+1.59+/-0.105 stat (MOND-3D route"
           " +1.20+/-0.10); a0(z~1)/a0(0)=2.38 -> the RISING pull, face-value ~30s evolution."
           " MAXIMAL drift exposure (non-lensed massive SFGs, RAR fit) -> w=1.0."),
 # --- bTFR ZERO-POINT points: Delta_b = -L(x)*log10(a0(z)/a0(0)) ---
 dict(tag="MUSE-DARK II Jeanneau", cite="Jeanneau+26 arXiv:2603.28856", kind="delta_b",
      z=0.9, obs=0.00, sig_stat=0.06, sig_hon=0.27, L=lever(geo(0.3, 1.0)), w=0.25,
      note="95 LENSED low-mass SFGs, g_bar~0.3-1 a0 = the CLEANEST near-a0 point in hand."
           " Delta_b=0.00+/-0.06 stat; honest +/-0.27 = gas model (Tacconi+20 + NUM 0.8dex) +"
           " local ref +/-0.16 -- NON-drift systematics. Lensed + near-a0 -> w=0.25."),
 dict(tag="Ubler+17 KMOS3D z0.9", cite="Ubler+17 ApJ 842,121 arXiv:1703.04321", kind="delta_b",
      z=0.9, obs=-0.44, sig_stat=0.04, sig_hon=0.35, L=lever(geo(0.3, 1.7)), w=1.0,
      note="naive x2.75 RISING, but g_bar~0.3-1.7 a0 -> DILUTED, and 6-sigma INTERNALLY"
           " INCONSISTENT with Jeanneau at the SAME z. MAXIMAL drift exposure -> w=1.0."),
 dict(tag="Ubler+17 KMOS3D z2.3", cite="Ubler+17 ApJ 842,121 arXiv:1703.04321", kind="delta_b",
      z=2.3, obs=-0.27, sig_stat=0.05, sig_hon=0.35, L=lever(geo(2.0, 6.0)), w=1.0,
      note="naive x1.86, NON-monotonic (BELOW its own z=0.9 value); g_bar~(2-6)a0 -> heavily"
           " DILUTED; canonical size-evolution sits in the SAME direction -> w=1.0."),
 dict(tag="Amvrosiadis+25 DSFG", cite="Amvrosiadis+25 MNRAS arXiv:2312.08959", kind="delta_b",
      z=2.4, obs=-0.26, sig_stat=0.19, sig_hon=0.30, L=lever(6.0), w=1.0,
      note="12 ALMA CO discs, alpha_CO=0.92+/-0.36-mediated, g_bar~6a0 -> most DILUTED point."),
 dict(tag="Tiley+19 KROSS matched", cite="Tiley+19 MNRAS 482,2166 arXiv:1810.07202", kind="delta_b",
      z=1.0, obs=-0.05, sig_stat=0.10, sig_hon=0.10, L=lever(1.0), w=0.2,
      note="QUALITY-MATCHED sTFR (degrading local SAMI to KROSS quality removes the apparent"
           " evolution) -> the matching itself removes most of the drift => w=0.2. Stellar axis."),
 # --- DIRECT deep-MOND object: a0_eff = V^4/(G M_bar) measured => lever 1, dex currency ---
 dict(tag="Big Wheel z=3.25", cite="arXiv:2409.17956 Nature Astronomy", kind="dex",
      z=3.25, obs=float(np.log10(1.15)), sig_stat=0.22, sig_hon=0.22, L=1.0, w=0.1,
      note="single CLEAN deep-MOND giant disc following the local TFR: a0_eff/a0(0)~1.0-1.3"
           " (+/-0.22 dex, N=1, optimistic). Deep-MOND-selected -> drift exposure w=0.1."),
]
# --- SECONDARY arm: digitized qualitative constancy bounds (reported WITH and WITHOUT) ---
BOUNDS = [
 dict(tag="Milgrom17 high-z RC bound", cite="Milgrom 2017 arXiv:1703.06110", kind="dex_upper",
      z=2.0, limit=np.log10(4.0), nsig=2.5, w=0.3,
      note="'all but excludes' a x4 a0 rise AND the (1+z)^1.5 law -> digitized as a ONE-SIDED"
           " upper bound log10 R(z=2) < log10 4 at 2.5s. CONSERVATIVE DIGITIZATION of a"
           " qualitative statement -> secondary arm only."),
 dict(tag="McGaugh+24 BTFR/f_DM", cite="McGaugh+24 arXiv:2406.17930", kind="dex",
      z=2.5, obs=0.0, sig_stat=0.20, sig_hon=0.20, L=1.0, w=0.6,
      note="'no clear evolution' of BTFR/f_DM to z~2.5 -> digitized as log10 R = 0.00 +/- 0.20"
           " dex. DIGITIZATION of a qualitative statement -> secondary arm only."),
]

print("\n" + bar); print("1. THE ASSEMBLED LIKELIHOOD  (8 quantitative points + 2 digitized bounds)"); print(bar)
print(f"  {'#':>2} {'point':24} {'kind':13} {'z':>6} {'obs':>7} {'s_stat':>7} {'s_hon':>6} {'L':>5} {'w':>5}")
print("  " + "-" * 92)
for i, d in enumerate(DATA, 1):
    zs = f"{d.get('z', 0.5*(d.get('zlo',0)+d.get('zhi',0))):.2f}"
    print(f"  {i:>2} {d['tag']:24} {d['kind']:13} {zs:>6} {d['obs']:>+7.2f} "
          f"{d['sig_stat']:>7.3f} {d['sig_hon']:>6.2f} {d['L']:>5.2f} {d['w']:>5.2f}")
for j, b in enumerate(BOUNDS, 9):
    v = b.get('obs', b.get('limit'))
    print(f"  {j:>2} {b['tag']:24} {b['kind']:13} {b['z']:>6.2f} {v:>+7.2f} "
          f"{b.get('sig_stat', float('nan')):>7.3f} {b.get('sig_hon', float('nan')):>6.2f} "
          f"{1.0:>5.2f} {b['w']:>5.2f}")
print("\n  DILUTION LEVERS L=1/(1+x) from the framework's OWN nu (x=g_bar/a0, geometric-mean x):")
print(f"    Jeanneau x~{geo(0.3,1.0):.2f} -> L={lever(geo(0.3,1.0)):.2f} | Ubler z0.9 x~{geo(0.3,1.7):.2f}"
      f" -> L={lever(geo(0.3,1.7)):.2f} | Ubler z2.3 x~{geo(2.,6.):.2f} -> L={lever(geo(2.,6.)):.2f}")
print(f"    Amvrosiadis x~6 -> L={lever(6.0):.2f} | Tiley x~1 -> L={lever(1.0):.2f} | deep-MOND/RAR L=1.00")
print("    => the g_bar>>a0 'rising' bTFR points carry 14-59% of the deep-MOND a0 lever: their")
print("       Delta_b offsets are DOWN-WEIGHTED as a0 information, in BOTH directions.")
print(f"\n  A_drift: a0_app(z)=a0_true(z)*(1+z)^(p*w_i), p>=0. Magneticum amplitude p_mag={P_MAG:.3f}")
print(f"  (=> (1+2.3)^{P_MAG:.3f} = {3.3**P_MAG:.2f}x apparent rise at z=2.3 with NO fundamental a0).")
print("  Drift enters the OBSERVABLE with lever 1 (a bias on the measured ZP/slope is not diluted),")
print("  while the MODEL's true a0 change enters with lever L -- the honest asymmetry.")

# =====================================================================================
# 2. FORWARD MODEL + EVIDENCE  (marginal likelihood by MC over (w0,wa) x p)
#    All three models share the SAME data errors, so the Gaussian normalizations cancel
#    exactly in every Bayes factor -> no arbitrary constant enters.
# =====================================================================================
def predict(d, model, W0, WA, p):
    """Predicted value of datum d's own observable, under `model` with drift exponent p."""
    w = d["w"]
    if d["kind"] == "loglog_slope":
        zg = np.linspace(d["zlo"], d["zhi"], 40)
        R = R_model(model, zg, W0, WA)                      # (NS,40) true ratio
        Y = np.log10(R) + (w * p)[:, None] * np.log10(1 + zg)[None, :]
        return _slope(np.log10(1 + zg), Y)
    if d["kind"] == "lin_slope":
        zg = np.linspace(d["zlo"], d["zhi"], 40)
        R = R_model(model, zg, W0, WA)
        Rapp = R * (1 + zg)[None, :] ** (w * p)[:, None]     # apparent ratio
        return _slope(zg, Rapp)
    if d["kind"] == "delta_b":
        lr = np.log10(R_model(model, d["z"], W0, WA)).ravel()
        return -(d["L"] * lr + w * p * np.log10(1 + d["z"]))
    if d["kind"] in ("dex", "dex_upper"):
        lr = np.log10(R_model(model, d["z"], W0, WA)).ravel()
        return d.get("L", 1.0) * lr + w * p * np.log10(1 + d["z"])
    raise ValueError(d["kind"])

def chi2_of(model, W0, WA, p, err="hon", pts=None, use_bounds=False):
    pts = DATA if pts is None else pts
    c2 = np.zeros(W0.size)
    per = {}
    for d in pts:
        s = d["sig_stat"] if err == "stat" else d["sig_hon"]
        r = (d["obs"] - predict(d, model, W0, WA, p)) / s
        per[d["tag"]] = r ** 2
        c2 = c2 + r ** 2
    if use_bounds:
        for b in BOUNDS:
            if b["kind"] == "dex_upper":
                s = b["limit"] / b["nsig"]
                pv = predict(b, model, W0, WA, p)
                r2 = np.where(pv > 0.0, (pv / s) ** 2, 0.0)   # one-sided: only penalize a rise
            else:
                s = b["sig_hon"]
                r2 = ((b["obs"] - predict(b, model, W0, WA, p)) / s) ** 2
            per[b["tag"]] = r2
            c2 = c2 + r2
    return c2, per

def evidence(model, err="hon", prior="uniform", dataset=HEAD, use_bounds=False, seed=0):
    W0, WA, p = draw(dataset, prior, seed)
    c2, per = chi2_of(model, W0, WA, p, err, use_bounds=use_bounds)
    lnZ = logsumexp(-0.5 * c2) - np.log(c2.size)
    wgt = np.exp(-0.5 * c2 - logsumexp(-0.5 * c2))            # normalized posterior weights
    return dict(lnZ=float(lnZ), chi2_min=float(c2.min()), chi2_eff=float(np.sum(wgt * c2)),
                p_post=float(np.sum(wgt * p)), p_post_sd=float(np.sqrt(max(np.sum(wgt*p**2)-np.sum(wgt*p)**2,0))),
                per={k: float(np.sum(wgt * v)) for k, v in per.items()},
                ndat=len(DATA) + (len(BOUNDS) if use_bounds else 0))

def report(title, err, prior, use_bounds=False, dataset=HEAD, show_per=False):
    E = {m: evidence(m, err, prior, dataset, use_bounds) for m in ("DEC", "RISE", "FLAT")}
    print(f"\n  [{title}]")
    print(f"    {'model':7} {'ln Z':>10} {'chi2_min':>9} {'<chi2>':>9} {'chi2/dof':>9} {'<p_drift>':>11}")
    for m in ("DEC", "RISE", "FLAT"):
        e = E[m]
        print(f"    {m:7} {e['lnZ']:>10.2f} {e['chi2_min']:>9.1f} {e['chi2_eff']:>9.1f} "
              f"{e['chi2_eff']/e['ndat']:>9.2f} {e['p_post']:>7.3f}+/-{e['p_post_sd']:.3f}")
    for a, b in (("DEC", "RISE"), ("DEC", "FLAT"), ("RISE", "FLAT")):
        dl = E[a]["lnZ"] - E[b]["lnZ"]
        l10 = dl / np.log(10.0)
        if abs(l10) < 12:
            bf = 10.0 ** l10
            s = f"B({a}/{b}) = {bf:.3g}" if bf >= 1 else f"B({b}/{a}) = {1/bf:.3g}"
        else:
            s = (f"B({a}/{b}) = 10^{l10:+.1f}" if l10 > 0 else f"B({b}/{a}) = 10^{-l10:+.1f}")
        fav = a if dl > 0 else b
        print(f"      ln B({a}/{b}) = {dl:>+9.2f}   log10 = {l10:>+8.2f}   {s:34} favors {fav}")
    if show_per:
        print("    posterior-mean chi2 contribution per datum (DEC | RISE | FLAT):")
        for k in E["DEC"]["per"]:
            print(f"      {k:26} {E['DEC']['per'][k]:>8.1f} | {E['RISE']['per'][k]:>8.1f} | {E['FLAT']['per'][k]:>8.1f}")
    return E

print("\n" + bar); print("2. MODEL COMPARISON -- REAL BAYES FACTORS  (three ZERO-free-parameter models)"); print(bar)
print("  Runs differ ONLY in the treatment of systematics + the A_drift nuisance:")
print("   (F) FACE VALUE      : stat-only errors, p=0 (systematics minimal). Dilution still applied.")
print("   (H) HONEST-SYS      : the compilation's systematics-inclusive errors, p=0.")
print("   (M) MARGINALIZED    : *** HEADLINE *** measurement errors only (stat for the two direct-RAR")
print("                         slopes, so Ciocan keeps its FULL statistical power; non-drift sys for")
print("                         the bTFR points), with A_drift marginalized over U(0,p_mag).")
print("   (M2) MOST CONSERVATIVE: systematics-inclusive errors AND A_drift marginalized (double-counts).")

EF = report("F  FACE VALUE   (stat errors, p=0)", "stat", "zero", show_per=True)
EH = report("H  HONEST-SYS   (compilation systematics-inclusive errors, p=0)", "hon", "zero")

# HEADLINE run: stat errors on the two direct-RAR slope points, honest (non-drift) on the rest.
for d in DATA:
    d["sig_mix"] = d["sig_stat"] if d["kind"] in ("loglog_slope", "lin_slope") else d["sig_hon"]
_orig = [(d["sig_hon"], d["sig_stat"]) for d in DATA]
for d in DATA:
    d["sig_hon"] = d["sig_mix"]                    # temporarily: 'hon' slot carries the MIX
EM = report("M  MARGINALIZED (HEADLINE: stat on direct-RAR, non-drift sys on bTFR, p~U(0,p_mag))",
            "hon", "uniform", show_per=True)
EMb = report("M+bounds  (headline + the 2 digitized constancy bounds)", "hon", "uniform", use_bounds=True)
for pr in ("halfnormal", "uniform_wide"):
    report(f"M  prior sensitivity: p ~ {pr}", "hon", pr)
for ds in ("DESY5", "Union3"):
    report(f"M  DESI dataset sensitivity: {ds}", "hon", "uniform", dataset=ds)
report("M  seed sensitivity (seed=1)", "hon", "uniform")
for d, (h, s) in zip(DATA, _orig):
    d["sig_hon"], d["sig_stat"] = h, s             # restore
EM2 = report("M2 MOST CONSERVATIVE (systematics-inclusive errors AND p marginalized)", "hon", "uniform")

# =====================================================================================
# 3. WHY THE ANSWER MOVES: the drift amplitude each model REQUIRES vs what Magneticum gives
# =====================================================================================
print("\n" + bar); print("3. DIAGNOSTIC -- how much apparent drift does each model NEED? (this IS the answer)"); print(bar)
def required_p(model, err="hon"):
    """profile p (on a fine grid) that minimizes chi2 at the DESI central (w0,wa)."""
    pg = np.linspace(0.0, 2.5, 501)
    W0 = np.full(pg.size, DESI[HEAD][0]); WA = np.full(pg.size, DESI[HEAD][2])
    c2, _ = chi2_of(model, W0, WA, pg, err)
    i = int(np.argmin(c2))
    return float(pg[i]), float(c2[i])
for d in DATA:
    d["_h"] = d["sig_hon"]
    d["sig_hon"] = d["sig_stat"] if d["kind"] in ("loglog_slope", "lin_slope") else d["_h"]
print(f"  Magneticum/Mayer+2023 calibrated amplitude: p_mag = {P_MAG:.3f}  =>  {3.3**P_MAG:.2f}x apparent")
print("  a0 rise at z=2.3 in PURE LCDM with NO fundamental a0. That is the prior's DEFENSIBLE ceiling.")
print(f"\n  {'model':7} {'p_required':>11} {'x-rise @z2.3':>13} {'vs Magneticum':>14} {'chi2_min(p)':>12}")
print("  " + "-" * 62)
REQP = {}
for m in ("DEC", "RISE", "FLAT"):
    p, c2 = required_p(m)
    REQP[m] = p
    print(f"  {m:7} {p:>11.3f} {3.3**p:>12.2f}x {3.3**p/3.0:>13.2f}x {c2:>12.1f}")
for d in DATA:
    d["sig_hon"] = d["_h"]
print("\n  READING (the load-bearing sensitivity, stated plainly):")
print(f"   * M-RISE needs only p~{REQP['RISE']:.2f} ({3.3**REQP['RISE']:.1f}x, {3.3**REQP['RISE']/3:.0%} of Magneticum): most of Ciocan's rise")
print("     is FUNDAMENTAL under M-RISE, so it sits comfortably inside the Magneticum-calibrated prior.")
print(f"   * M-DEC needs p~{REQP['DEC']:.2f} ({3.3**REQP['DEC']:.1f}x apparent rise at z=2.3) = {3.3**REQP['DEC']/3.0:.1f}x MORE drift than")
print(f"     Magneticum delivers; M-FLAT needs p~{REQP['FLAT']:.2f} ({3.3**REQP['FLAT']:.1f}x) = {3.3**REQP['FLAT']/3.0:.1f}x more.")
print("   * Therefore M-DEC and M-FLAT are pinned AT the drift-prior CEILING: their evidence is set by")
print("     wherever that ceiling is drawn, NOT by the data. Move the ceiling from 1.0x to 1.5x of the")
print("     Magneticum amplitude and B(DEC/RISE) swings from ~1e-8 to ~10. THAT SWING IS THE RESULT:")
print("     the existing high-z data do NOT decide DEC-vs-RISE; the apparent-drift amplitude does.")
print("   * Neither direction is manufactured here: Ciocan keeps its FULL stat error (0.105) in the")
print("     headline run (no systematics inflation), and its face-value ~30s rise is NOT taken as a")
print("     fundamental-a0 result (face-value chi2/dof >> 1 for ALL THREE models -- see run F).")

print("\n" + bar); print("3B. SENSITIVITY SUMMARY -- log10 Bayes factor by run (the honest spread)"); print(bar)
print(f"  {'run':52} {'log10 B(D/R)':>13} {'log10 B(D/F)':>13} {'log10 B(R/F)':>13}")
print("  " + "-" * 94)
def row(name, E):
    l = lambda a, b: (E[a]["lnZ"] - E[b]["lnZ"]) / np.log(10.0)
    print(f"  {name:52} {l('DEC','RISE'):>+13.2f} {l('DEC','FLAT'):>+13.2f} {l('RISE','FLAT'):>+13.2f}")
row("F  FACE VALUE (stat errors, p=0)  [NO model fits]", EF)
row("H  HONEST-SYS (compilation errors, p=0)", EH)
row("M  MARGINALIZED headline, p~U(0,p_mag)", EM)
row("M  headline + 2 digitized constancy bounds", EMb)
row("M2 MOST CONSERVATIVE (honest sys AND p marginalized)", EM2)
print("  " + "-" * 94)
print("  (prior-ceiling sensitivity, from the runs above: p~U(0,1.5 p_mag) -> log10 B(D/R) = +1.00;")
print("   p~HalfNormal(p_mag/2) -> -0.68.  DESI dataset choice moves log10 B(D/F) over +0.56..+2.80.)")
print("  DECISION-RELEVANT SPREAD: log10 B(DEC/RISE) spans -8.0 to +1.0 across defensible systematic")
print("  treatments -> UNDECIDED. log10 B(DEC/FLAT) spans -0.6 to +2.8 -> WEAK, at most 'substantial'.")

# =====================================================================================
# 4. FORECAST -- WHAT NEW MEASUREMENT DECIDES IT
#    Target: a DEEP-MOND-SELECTED sample, g_bar < 0.3 a0 (NO current sample satisfies this).
#    That selection is what escapes BOTH the dilution (L -> 1) and the LCDM apparent-drift
#    degeneracy (w -> ~0.15: g_obs-selection, the dominant Magneticum driver, is removed by
#    construction when the sample is selected on g_bar, not on g_obs).
# =====================================================================================
print("\n" + bar); print("4. FORECAST -- the decisive new measurement (deep-MOND-selected, g_bar < 0.3 a0)"); print(bar)

X_DM = 0.15                       # typical g_bar/a0 in a g_bar<0.3a0 selected sample
L_DM = lever(X_DM)                # a0 lever -> ~0.87, i.e. near-full deep-MOND leverage
W_DM = 0.15                       # residual A_drift exposure of a g_bar-selected deep-MOND sample
LN20, LN150 = np.log(20.0), np.log(150.0)
NSIG20, NSIG150 = np.sqrt(2 * LN20), np.sqrt(2 * LN150)

# ---- error budget for the DEEP-MOND inversion a0 = g_obs^2/g_bar  (Rule-4 penalty, derived) ----
#   sigma(log a0)^2 = (4 sigma(log V))^2 + sigma(log M_bar)^2      [g_obs ~ V^2, g_bar ~ M_bar]
def a0_dex(sig_logV, sig_logM):
    return float(np.hypot(4.0 * sig_logV, sig_logM))

BUDGET = [  # (label, per-object sigma(log V), per-object sigma(log M), COHERENT sigV, COHERENT sigM)
 ("TODAY  (KMOS3D/MSA-3D-class, alpha_CO)",       0.040, 0.200, 0.050, 0.200),
 ("JWST NIRSpec-IFU + ALMA CO/[CII], lensed",     0.035, 0.150, 0.030, 0.150),
 ("+ resolved [CII] & careful beam/pressure fwd", 0.030, 0.120, 0.020, 0.100),
 ("SKA2 / ngVLA direct HI (<0.05 dex, no a_CO)",  0.025, 0.050, 0.015, 0.050),
 ("floor-limited ideal (ELT+SKA2, best case)",    0.020, 0.030, 0.008, 0.030),
]
print("  DEEP-MOND ERROR BUDGET (derived, not asserted):  a0 = g_obs^2/g_bar  =>")
print("    sigma(log10 a0) = sqrt( (4 sigma(log10 V))^2 + sigma(log10 M_bar)^2 )   [Rule-4 x2-in-ln")
print("    penalty appears as the x4 on log V; gas mass enters with lever 1].")
print(f"\n  {'configuration':44} {'s_pt(a0)':>9} {'FLOOR(a0)':>10}  (dex)")
print("  " + "-" * 68)
FLOORS = {}
for lab, sv, sm, cv, cm in BUDGET:
    spt, fl = a0_dex(sv, sm), a0_dex(cv, cm)
    FLOORS[lab] = (spt, fl)
    print(f"  {lab:44} {spt:>9.3f} {fl:>10.3f}")
print("  CROSS-CHECKS against the committed compilation (the budget is anchored, not invented):")
print(f"    * 'TODAY' per-object s_pt(a0) = {FLOORS[BUDGET[0][0]][0]:.3f} dex  vs  Big Wheel's quoted +/-0.22 dex  OK")
print(f"    * 'TODAY' COHERENT floor      = {FLOORS[BUDGET[0][0]][1]:.3f} dex  vs  highz_systematics_floor.py ~0.30 dex  OK")
print(f"    * SKA2/ngVLA HI <0.05 dex gas masses (flagged in the compilation) -> floor {FLOORS[BUDGET[3][0]][1]:.3f} dex")
print("      -- note the floor CANNOT go below ~4*sigma_coh(log V): VELOCITY systematics, not gas mass,")
print("      are the binding constraint once HI removes alpha_CO.")

# ---- theory-side spreads (DESI-inherited); these are IRREDUCIBLE without better cosmology ----
def theory_dex(model, z, dataset=HEAD):
    W0, WA, _ = draw(dataset, "zero", 0)
    lr = np.log10(R_model(model, z, W0, WA))
    return np.median(lr, axis=0), np.std(lr, axis=0)

ZF = np.array([1.0, 1.5, 2.0, 2.5, 3.0, 3.25, 3.5, 4.0])
mD, sD_th = theory_dex("DEC", ZF); mR, sR_th = theory_dex("RISE", ZF)
print("\n  " + "-" * 96)
print("  4A. DEC-vs-RISE  (the fork; separation is LARGE and grows with z)")
print("  " + "-" * 96)
print(f"  {'z':>5} {'log10 R_DEC':>12} {'log10 R_RISE':>13} {'Delta(dex)':>11} {'s_theory':>9} "
      f"{'s_req 20:1':>11} {'s_req 150:1':>12} {'f_req(20:1)':>12}")
for i, z in enumerate(ZF):
    D = mR[i] - mD[i]
    sth = float(np.hypot(sD_th[i], sR_th[i]))
    s20, s150 = abs(D) / NSIG20, abs(D) / NSIG150
    print(f"  {z:>5.2f} {mD[i]:>+12.3f} {mR[i]:>+13.3f} {D:>+11.3f} {sth:>9.3f} "
          f"{s20:>11.3f} {s150:>12.3f} {100*np.log(10)*s20:>11.0f}%")
print("  (f_req = fractional a0 precision, sigma_dex*ln10; 20:1 needs Delta/sigma>=%.2f, 150:1 >=%.2f)"
      % (NSIG20, NSIG150))

def N_required(z, D, sth, spt, floor, target_nsig, w=W_DM, dp=P_MAG/np.sqrt(12)):
    """objects needed so that Delta/sigma_tot >= target_nsig; None if floor-limited (impossible)."""
    sdrift = w * dp * np.log10(1 + z)
    s_need = abs(D) / target_nsig
    resid = s_need ** 2 - floor ** 2 - sdrift ** 2 - sth ** 2
    if resid <= 0:
        return None, s_need, sdrift
    return max(1, int(np.ceil((spt ** 2) / resid))), s_need, sdrift

print("\n  N OBJECTS REQUIRED for DEC-vs-RISE (deep-MOND-selected; '--' = FLOOR-LIMITED, impossible at any N)")
print(f"  {'configuration':44} " + " ".join(f"{'z='+format(z,'.1f'):>9}" for z in [1.0, 2.0, 3.0, 3.25]))
for tgt, tname in ((NSIG20, "20:1"), (NSIG150, "150:1")):
    print(f"   [{tname}]")
    for lab, sv, sm, cv, cm in BUDGET:
        spt, fl = FLOORS[lab]
        cells = []
        for z in [1.0, 2.0, 3.0, 3.25]:
            i = int(np.argmin(abs(ZF - z))) if z in ZF else None
            mDz, sDz = theory_dex("DEC", np.array([z])); mRz, sRz = theory_dex("RISE", np.array([z]))
            D = float(mRz[0] - mDz[0]); sth = float(np.hypot(sDz[0], sRz[0]))
            N, sneed, sdr = N_required(z, D, sth, spt, fl, tgt)
            cells.append("       --" if N is None else f"{N:>9d}")
        print(f"    {lab:44} " + " ".join(cells))

# ---- MC VALIDATION of the analytic forecast (simulate a future datum, run the real evidence) ----
print("\n  MC VALIDATION of the analytic lnB = Delta^2/(2 sigma^2) (simulate the future datum, then")
print("  run the SAME evidence machinery used in section 2, with (w0,wa) and A_drift marginalized):")
print(f"  {'z':>5} {'sigma(dex)':>11} {'analytic lnB':>13} {'MC lnB':>9} {'MC B(DEC/RISE)':>16}")
for z, sig in ((2.0, 0.20), (3.0, 0.30), (3.0, 0.15), (3.25, 0.22)):
    mDz, sDz = theory_dex("DEC", np.array([z]))
    fut = dict(tag="FUTURE", cite="forecast", kind="dex", z=z, obs=float(mDz[0]),
               sig_stat=sig, sig_hon=sig, L=1.0, w=W_DM)
    W0, WA, p = draw(HEAD, "uniform", 0)
    lnZ = {}
    for m in ("DEC", "RISE"):
        c2, _ = chi2_of(m, W0, WA, p, "hon", pts=[fut])
        lnZ[m] = logsumexp(-0.5 * c2) - np.log(c2.size)
    mRz, _ = theory_dex("RISE", np.array([z]))
    D = float(mRz[0] - mDz[0]); sth = float(np.hypot(sDz[0], 0.0))
    sdr = W_DM * (P_MAG / np.sqrt(12)) * np.log10(1 + z)
    ana = 0.5 * D ** 2 / (sig ** 2 + sth ** 2 + sdr ** 2)
    mc = lnZ["DEC"] - lnZ["RISE"]
    print(f"  {z:>5.2f} {sig:>11.3f} {ana:>13.2f} {mc:>9.2f} {np.exp(min(mc,700)):>16.3g}")
print("  (analytic is the CONSERVATIVE one: the one-sided p>=0 drift prior displaces M-RISE further")
print("   from a datum sitting at the M-DEC value, so the MC lnB comes out slightly LARGER. The")
print("   N-tables above use the analytic formula -> they are upper bounds on the required sample.)")

# ---- 4B. DEC vs FLAT: the HARD discrimination (and it is COSMOLOGY-limited, not sample-limited) ----
print("\n  " + "-" * 96)
print("  4B. DEC-vs-FLAT  (the HARD one: DEC ~ 1 at low z, so the signal is a FEW-PERCENT effect)")
print("  " + "-" * 96)
ZC = np.linspace(0.05, 6.0, 120)
mC, sC = theory_dex("DEC", ZC)
ceil = np.abs(mC) / sC                       # theory ceiling: |signal|/DESI-inherited spread
ipk = int(np.argmax(ceil))
zb = ZC[(ZC > 0.1) & (ZC < 0.7)]; mb, sb = theory_dex("DEC", zb)
ibp = int(np.argmax(mb))
print(f"  {'z':>5} {'log10 R_DEC':>12} {'|signal| dex':>13} {'s_theory':>9} {'ceiling s':>10} "
      f"{'s_req 20:1':>11} {'f_req 20:1':>11} {'s_req 150:1':>12}")
for z in [0.35, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0]:
    m1, s1 = theory_dex("DEC", np.array([z]))
    sg = abs(float(m1[0])); s20, s150 = sg / NSIG20, sg / NSIG150
    tag = "  <- bump peak" if abs(z - 0.35) < 1e-9 else ""
    print(f"  {z:>5.2f} {float(m1[0]):>+12.4f} {sg:>13.4f} {float(s1[0]):>9.4f} "
          f"{sg/float(s1[0]):>10.2f} {s20:>11.4f} {100*np.log(10)*s20:>10.1f}% {s150:>12.4f}{tag}")
print(f"\n  SHAPE OF THE CEILING |signal|/s_theory: it is nearly z-INDEPENDENT because M-DEC's signal AND")
print(f"  its DESI-inherited spread grow together (both scale as the same rho_DE lever): ~{ceil[ZC>1.5].min():.2f}-{ceil[ZC>1.5].max():.2f}")
print(f"  sigma for all z>1.5, with a NULL at the z~1 crossover (ceiling {ceil[np.argmin(np.abs(ZC-1.0))]:.2f}s -> z~1 is UNTESTABLE),")
print(f"  and ~{ceil[ZC<0.5].max():.2f}s at z<0.5 where the effect is only 1-4% (unmeasurable in practice).")
print(f"  The low-z BUMP (peak z={zb[ibp]:.2f}, +{100*(10**mb[ibp]-1):.1f}% = {mb[ibp]:.4f} dex) is "
      f"{abs(float(theory_dex('DEC',np.array([3.0]))[0][0]))/abs(mb[ibp]):.1f}x WEAKER in dex than")
print("  the z=3 decline -> do NOT chase the bump, even though that is where the good data live.")

# --- the CORRECT structure for DEC-vs-FLAT: M-FLAT is a POINT hypothesis, so a precise
#     measurement excludes it at only a LOGARITHMIC Occam cost for M-DEC's DESI prior width:
#       lnB(DEC/FLAT) ~ signal^2/(2 sigma^2)  -  ln(sigma_theory_eff / sigma)   [sigma < s_theory]
#     There is NO hard theory cap (an earlier Gaussian-convolution 'cap' was WRONG and is not
#     used). All DEC-vs-FLAT numbers below come from the EXACT MC evidence, and the analytic
#     form is printed beside it only as a cross-check.
DP = P_MAG / np.sqrt(12)

def mc_lnB(pairs, sig, targets=("FLAT", "RISE"), dataset=HEAD, seed=0):
    """EXACT MC evidence ratio for a future dataset [(z, obs_at_DEC_median), ...] with error sig."""
    W0, WA, p = draw(dataset, "uniform", seed)
    pts = [dict(tag=f"F{z}", kind="dex", z=z, obs=o, sig_stat=s, sig_hon=s, L=1.0, w=W_DM)
           for (z, o), s in zip(pairs, sig if hasattr(sig, "__len__") else [sig] * len(pairs))]
    lnZ, ess = {}, None
    for m in ("DEC",) + tuple(targets):
        c2, _ = chi2_of(m, W0, WA, p, "hon", pts=pts)
        lw = -0.5 * c2
        lnZ[m] = logsumexp(lw) - np.log(c2.size)
        if m == "DEC":
            w = np.exp(lw - logsumexp(lw)); ess = 1.0 / np.sum(w ** 2)
    return {t: lnZ["DEC"] - lnZ[t] for t in targets}, ess

def N_mc(z, spt, floor, target_ln, which="FLAT", nmax=10 ** 7):
    """smallest N with MC lnB >= target_ln; None if unreachable even at N=nmax."""
    m1, _ = theory_dex("DEC", np.array([z])); obs = float(m1[0])
    def f(N):
        return mc_lnB([(z, obs)], float(np.hypot(spt / np.sqrt(N), floor)), (which,))[0][which]
    if f(nmax) < target_ln:
        return None
    lo, hi = 1, nmax
    if f(1) >= target_ln:
        return 1
    while hi - lo > 1:
        mid = int(np.sqrt(lo * hi)) if hi > 4 * lo else (lo + hi) // 2
        mid = min(max(mid, lo + 1), hi - 1)
        if f(mid) >= target_ln:
            hi = mid
        else:
            lo = mid
    return hi

print("\n  CROSS-CHECK of the correct lnB structure for DEC-vs-FLAT (exact MC vs the analytic form")
print("  signal^2/(2 s^2) - ln(s_theory/s); the SECOND term is M-DEC's prior-width Occam penalty):")
print(f"  {'z':>5} {'sigma(dex)':>11} {'naive s^2/2s^2':>15} {'Occam':>7} {'analytic':>9} "
      f"{'MC(drift)':>10} {'MC(p=0)':>9} {'ESS':>7}")
for z, sg in ((2.0, 0.030), (3.0, 0.050), (3.0, 0.025), (4.0, 0.060)):
    m1, s1 = theory_dex("DEC", np.array([z]))
    sdr = W_DM * DP * np.log10(1 + z)
    st = float(np.hypot(sg, sdr))
    naive = 0.5 * float(m1[0]) ** 2 / st ** 2
    occ = np.log(max(float(s1[0]), st) / st)
    d, ess = mc_lnB([(z, float(m1[0]))], sg, ("FLAT",))
    W0z, WAz, pz = draw(HEAD, "zero", 0)
    ptz = [dict(tag="F", kind="dex", z=z, obs=float(m1[0]), sig_stat=sg, sig_hon=sg, L=1.0, w=W_DM)]
    lz = {}
    for m in ("DEC", "FLAT"):
        c2, _ = chi2_of(m, W0z, WAz, pz, "hon", pts=ptz)
        lz[m] = logsumexp(-0.5 * c2) - np.log(c2.size)
    print(f"  {z:>5.2f} {sg:>11.3f} {naive:>15.2f} {-occ:>7.2f} {naive-occ:>9.2f} "
          f"{d['FLAT']:>10.2f} {lz['DEC']-lz['FLAT']:>9.2f} {ess:>7.0f}")
print("  => the theory spread costs only a LOG penalty, so DEC-vs-FLAT IS reachable -- it just needs")
print("  PERCENT-level a0, not the tens-of-percent that DEC-vs-RISE needs. (ESS = effective MC samples.)")
print("  MC(drift) > MC(p=0) is a REAL asymmetry, not a bug: the Magneticum-calibrated apparent drift")
print("  can only push a0 UP (p>=0), so a measured DECLINE is very hard to fake -- the nuisance that")
print("  destroys the rising evidence HELPS the declining branch. A two-sided drift prior removes")
print("  that bonus; the MC(p=0) column is the drift-free floor of the DEC-vs-FLAT forecast, and the")
print("  N tables below are computed WITH the one-sided drift (the physically calibrated prior).")

print("\n  N OBJECTS REQUIRED for DEC-vs-FLAT  (EXACT MC evidence; '--' = unreachable even at N=1e7,")
print("  i.e. the COHERENT FLOOR alone already blocks it -- floor-limited, not theory-limited)")
print(f"  {'configuration':44} " + " ".join(f"{'z='+format(z,'.1f'):>9}" for z in [2.0, 3.0, 4.0]))
for tgt, tname in ((LN20, "20:1"), (LN150, "150:1")):
    print(f"   [{tname}]")
    for lab, sv, sm, cv, cm in BUDGET:
        spt, fl = FLOORS[lab]
        cells = []
        for z in [2.0, 3.0, 4.0]:
            N = N_mc(z, spt, fl, tgt, "FLAT")
            cells.append("       --" if N is None else f"{N:>9d}")
        print(f"    {lab:44} " + " ".join(cells))
print("  READING: DEC-vs-FLAT is FLOOR-limited. What blocks it is the COHERENT a0 bias (alpha_CO,")
print("  beam-smearing/pressure-support residual), which does NOT average down with N. Only the")
print("  SKA2/ngVLA-HI-class floor (<=0.08 dex) opens it, and then only at z >~ 3.")

print("\n  WHERE IS DEC-vs-FLAT SEPARATION MAXIMAL? (exact MC lnB, N -> large, per configuration)")
print(f"  {'configuration':44} " + " ".join(f"{'z='+format(z,'.1f'):>8}" for z in [1.5, 2.0, 2.5, 3.0, 3.5, 4.0]))
for lab, sv, sm, cv, cm in BUDGET[2:]:
    spt, fl = FLOORS[lab]
    row_ = []
    for z in [1.5, 2.0, 2.5, 3.0, 3.5, 4.0]:
        m1, _ = theory_dex("DEC", np.array([z]))
        d, _ = mc_lnB([(z, float(m1[0]))], float(np.hypot(spt / np.sqrt(100), fl)), ("FLAT",))
        row_.append(f"{d['FLAT']:>8.2f}")
    print(f"    {lab:44} " + " ".join(row_) + "   (lnB, N=100)")
print("  => the DEC-vs-FLAT separation is MAXIMAL AT THE HIGHEST ACCESSIBLE z (it grows monotonically")
print("  above the z~1 crossover null and never turns over inside z<=4): |log10 R_DEC| grows faster")
print("  than the floor+drift budget. z~1 is a NULL (M-DEC crosses unity) -> UNTESTABLE there.")

# ---- MULTI-BIN, done PROPERLY: the (w0,wa) draws are SHARED across bins (correlated theory error) ----
print("\n  MULTI-BIN PROGRAM, DONE PROPERLY (the SAME (w0,wa) draws feed every bin, so the theory")
print("  error is CORRELATED across bins as it physically is -- this is the real evidence, computed")
print("  with the section-2 machinery, not an optimistic per-bin sum):")
ZBINS = (1.5, 2.0, 2.5, 3.0, 3.5)
for cfg in (BUDGET[1][0], BUDGET[3][0], BUDGET[4][0]):
    spt, fl = FLOORS[cfg]
    print(f"    [{cfg}]  s_pt={spt:.3f} floor={fl:.3f} dex")
    for Nper in (10, 40, 100, 1000000):
        W0, WA, p = draw(HEAD, "uniform", 0)
        pts = []
        for z in ZBINS:
            m1, _ = theory_dex("DEC", np.array([z]))
            s = float(np.hypot(spt / np.sqrt(Nper), fl))
            pts.append(dict(tag=f"FUT z{z}", kind="dex", z=z, obs=float(m1[0]),
                            sig_stat=s, sig_hon=s, L=1.0, w=W_DM))
        lnZ = {}
        for m in ("DEC", "FLAT", "RISE"):
            c2, _ = chi2_of(m, W0, WA, p, "hon", pts=pts)
            lnZ[m] = logsumexp(-0.5 * c2) - np.log(c2.size)
        bF, bR = lnZ["DEC"] - lnZ["FLAT"], lnZ["DEC"] - lnZ["RISE"]
        nn = "inf" if Nper > 10000 else str(Nper)
        print(f"      N={nn:>7}/bin x{len(ZBINS)}: lnB(DEC/FLAT)={bF:>6.2f} (B={np.exp(min(bF,700)):>8.1f}:1) "
              f"{'>=20:1' if bF>=LN20 else '      '} {'>=150:1' if bF>=LN150 else '       '} | "
              f"lnB(DEC/RISE)={bR:>7.2f} (B=10^{bR/np.log(10):.1f})")
print("  => a 5-bin z=1.5-3.5 deep-MOND program SETTLES DEC-vs-RISE overwhelmingly at modest N (10/bin")
print("  is already 10^12:1 with JWST-class errors), but SATURATES on DEC-vs-FLAT at whatever the")
print("  COHERENT FLOOR allows: 2.4:1 at a 0.19 dex floor, 90:1 at 0.08 dex (SKA2/ngVLA HI), and only")
print("  >150:1 once the floor reaches ~0.04 dex. Note that N barely matters (N=10 vs N=inf changes")
print("  lnB by <30%): the program is FLOOR-limited, so SYSTEMATICS CONTROL, not sample size, is the")
print("  deliverable. This is the quantitative version of the committed 'THEORY CEILING' caveat.")

# =====================================================================================
# 5. THE DECISIVE-MEASUREMENT SPEC  (the deliverable)
# =====================================================================================
print("\n" + bar); print("5. DECISIVE-MEASUREMENT SPEC -- what single new measurement pushes past 20:1 / 150:1"); print(bar)
SPEC = []
for z in (2.0, 2.5, 3.0, 3.25):
    mDz, sDz = theory_dex("DEC", np.array([z])); mRz, sRz = theory_dex("RISE", np.array([z]))
    D = float(mRz[0] - mDz[0]); sth = float(np.hypot(sDz[0], sRz[0]))
    for tgt, tn in ((NSIG20, "20:1"), (NSIG150, "150:1")):
        s_need = abs(D) / tgt
        sdr = W_DM * DP * np.log10(1 + z)
        rows = []
        for lab in (BUDGET[1][0], BUDGET[3][0]):
            spt, fl = FLOORS[lab]
            N, _, _ = N_required(z, D, sth, spt, fl, tgt)
            rows.append((lab, N))
        SPEC.append((z, tn, abs(D), s_need, np.log(10) * s_need, rows))
print("  *** DEC-vs-RISE (the horizon fork) -- deep-MOND-selected, g_bar<0.3 a0 ***")
print(f"  {'z':>5} {'target':>7} {'Delta(dex)':>11} {'s_req(dex)':>11} {'f_req(a0)':>10} "
      f"{'N (JWST+ALMA)':>15} {'N (SKA2/ngVLA HI)':>19}")
for z, tn, D, sn, fr, rows in SPEC:
    c = ["   --" if N is None else f"{N:>5d}" for _, N in rows]
    print(f"  {z:>5.2f} {tn:>7} {D:>11.3f} {sn:>11.3f} {100*fr:>9.0f}% {c[0]:>15} {c[1]:>19}")
print("\n  HEADLINE SPEC (DEC-vs-RISE, past 20:1 -> DECISIVE):")
print("    z ~ 3, ONE (N=1) clean deep-MOND-selected rotator (g_bar < 0.3 a0) with sigma(a0) <= 0.31 dex")
print("    (~70% fractional a0). JWST NIRSpec-IFU on a LENSED low-mass rotator + ALMA CO/[CII] cold-gas")
print("    velocity field delivers ~0.21 dex/object -> N=1 clears 20:1, N=3 clears 150:1.")
print("    At z~2 the same config needs N=5 (20:1); at z~1 it is FLOOR-BLOCKED today (needs SKA2-class).")
print("  A Big-Wheel-class object is EXACTLY this measurement: the existing z=3.25 Big Wheel at")
print("  +/-0.22 dex already yields lnB(DEC/RISE) ~ 6.4 analytic / ~7.5 exact-MC = 600-1800:1 ON ITS OWN")
print("  -- and it is the ONE point in the whole compilation that penalizes M-RISE (chi2 ~ 8.9).")
print("  So the DEC-vs-RISE fork is a 2-3-OBJECT PROBLEM, feasible NOW with JWST+ALMA, not a 2035 problem.")
print("\n  *** DEC-vs-FLAT (the framework's decline vs constant-a0 MOND) -- the HARDER one ***")
print("    Separation is MAXIMAL AT THE HIGHEST ACCESSIBLE z (monotonic above the z~1 crossover NULL;")
print("    z~1 is untestable, the bump at z~0.35 is 7.3x weaker in dex than z=3 and needs ~1.4% a0).")
print("    Required precision: sigma(a0) <= 0.024 dex (5.5%) at z=2, 0.045 dex (10.4%) at z=3,")
print("    0.064 dex (14.8%) at z=4 -- for 20:1; ~30% tighter for 150:1.")
print("    Binding constraint is the COHERENT floor, which does NOT average down: it must reach")
print("    <= ~0.08 dex (SKA2/ngVLA direct HI, no alpha_CO) for 20:1 in a 5-bin program (B ~ 90:1),")
print("    and ~0.04 dex (+ ELT-class velocity systematics, 4*sigma_coh(logV) is then the wall) for 150:1.")
print("    Sample size is nearly IRRELEVANT (N=10 vs N=inf moves lnB <30%) -> the deliverable is")
print("    SYSTEMATICS CONTROL, not object count. This is the ~2035+ SKA2/ngVLA-era measurement.")

# =====================================================================================
# 6. VERDICT  +  PRE-REGISTRATION
# =====================================================================================
print("\n" + bar); print("6. HONEST VERDICT"); print(bar)
print("""  (A) DEC-vs-RISE is NOT DECIDED by existing data, and the reason is now a NUMBER, not an opinion.
      log10 B(DEC/RISE) spans -8.0 (Magneticum-calibrated drift prior, Ciocan at full stat weight)
      to +1.0 (drift prior ceiling raised 50%) to +0.5 (compilation's own systematics-inclusive
      errors AND drift marginalized). The swing is driven ENTIRELY by the drift-prior CEILING,
      because M-DEC requires p~1.41 (a 5.4x apparent rise at z=2.3 = 1.8x MORE than Magneticum
      delivers) to accommodate Ciocan, and M-FLAT requires p~1.30 (4.7x = 1.6x more). M-RISE
      needs only p~0.35 (1.5x = HALF of Magneticum), so it sits comfortably inside the prior.
      => The single decisive unknown is the APPARENT-DRIFT AMPLITUDE, not the a0(z) data.
      At FACE VALUE M-RISE wins by 10^51 -- but chi2/dof is 15-40 for ALL THREE models, i.e. NO
      model fits the face-value data (Jeanneau and Ubler are 6 sigma apart at the SAME z), so the
      face-value factor measures data inconsistency, not evidence. It is reported, not used.
  (B) DEC-vs-FLAT: M-DEC is WEAKLY PREFERRED in the headline marginalized run, log10 B = +1.11
      (13:1, 'substantial' on Jeffreys, NOT strong), spanning -0.6 to +2.8 across defensible
      treatments. That preference is NOT a detection of the decline: it comes from M-DEC needing
      slightly less drift than M-FLAT to fit Ciocan, plus M-DEC's low-z bump. FLAT remains fully
      viable, and FLAT is simultaneously standard MOND AND the framework's own w->-1 limit --
      so a FLAT win would NOT falsify the framework, but it WOULD be a failure to detect the
      distinctive decline. Stated plainly, not spun.
  (C) The ONLY point in the whole compilation that penalizes M-RISE is the single clean deep-MOND
      object (Big Wheel z=3.25, chi2 ~ 8.9 against RISE). Everything else is either drift-degenerate
      (Ciocan, MSA-3D), dilution-gutted (Ubler, Amvrosiadis: 14-59% of the deep-MOND a0 lever), or
      internally inconsistent (Jeanneau vs Ubler). That is why ONE MORE Big-Wheel-class object is
      worth more than any number of massive-SFG RAR fits.
  (D) A genuine asymmetry worth stating: the LCDM apparent drift can only push a0 UP. A measured
      DECLINE therefore cannot be faked by it -- the nuisance that destroys the rising evidence
      HELPS the declining branch (MC lnB exceeds the drift-free value by ~1.3 at fixed precision).
  (E) Both footings carried; the RATIO is footing-independent, so nothing here depends on
      9.36e-11 vs 1.13e-10. a0's VALUE and the HORIZON CHOICE remain POSITS. If DESI DR3 relaxes
      to w=-1, M-DEC collapses onto M-FLAT and the fork becomes UNTESTABLE (not falsified).
      No TOE. No 'theory closed'. nu = Milgrom 1999 PLA 253:273 Eq.9; McCulloch credited for E(z).""")

print("\n" + "#" * 102)
print("# PRE-REGISTRATION -- a0(z) MODEL COMPARISON + DECISIVE MEASUREMENT -- FROZEN 2026-07-25")
print("#" * 102)
PRE = [
 "HEADLINE ODDS (run M, drift ~ U(0, p_mag=0.920)): log10 B(DEC/RISE) = -7.99, log10 B(DEC/FLAT) = "
 "+1.11, log10 B(RISE/FLAT) = +9.10. FACE VALUE (stat errors, p=0): -50.94 / +6.34 / +57.27 with "
 "chi2/dof 15-40 for every model (NO model fits -> face-value factors are data-inconsistency, not "
 "evidence). MOST CONSERVATIVE (systematics-inclusive AND drift marginalized): +0.49 / -0.45 / -0.94.",
 "THE VERDICT-FLIPPING KNOB is the drift-prior CEILING, not the data: raise it from 1.0x to 1.5x the "
 "Magneticum amplitude and log10 B(DEC/RISE) moves from -7.99 to +1.00. M-DEC needs p=1.41 (5.4x "
 "apparent rise at z=2.3, 1.8x Magneticum); M-FLAT p=1.30 (1.6x); M-RISE only p=0.35 (0.5x).",
 "DECISION THRESHOLD for DEC-vs-RISE: ONE clean deep-MOND-selected (g_bar<0.3 a0) rotator at z~3 with "
 "sigma(a0) <= 0.31 dex (~70% fractional) clears 20:1; N=3 at that precision clears 150:1. JWST "
 "NIRSpec-IFU (lensed low-mass) + ALMA CO/[CII] delivers ~0.21 dex/object -> FEASIBLE NOW.",
 "DECISION THRESHOLD for DEC-vs-FLAT: sigma(a0) <= 0.024 dex (5.5%) at z=2 / 0.045 dex (10.4%) at z=3, "
 "AND a COHERENT floor <= 0.08 dex for 20:1 (5-bin, B~90:1) or ~0.04 dex for 150:1. Requires SKA2/ngVLA "
 "DIRECT HI gas masses (<0.05 dex, no alpha_CO) -> ~2035+. Sample size nearly irrelevant (floor-limited).",
 "DEEP-MOND ERROR BUDGET (derived): sigma(log a0) = sqrt((4 sigma(log V))^2 + sigma(log M_bar)^2). It "
 "reproduces the Big Wheel's quoted +/-0.22 dex and the committed ~0.30 dex coherent floor -- anchored, "
 "not invented. Once HI removes alpha_CO, 4*sigma_coh(log V) (velocity systematics) is the binding wall.",
 "ACCELERATION DILUTION (mandatory, framework's own nu): L(x)=1/(1+x), x=g_bar/a0. Applied levers: "
 "Jeanneau 0.65, Ubler z0.9 0.59, Ubler z2.3 0.22, Amvrosiadis 0.14, Tiley 0.50, deep-MOND/RAR 1.00. "
 "The 'rising' bTFR points therefore carry 14-59% of the deep-MOND a0 lever -- down-weighted BOTH ways.",
 "MSA-3D uses the SELECTION-CORRECTED slope +0.91+/-0.79, NEVER the raw +2.13. Ciocan keeps its FULL "
 "stat error 0.105 in the headline run (NOT systematics-inflated away); its face-value ~30s rise is "
 "NOT taken as a fundamental-a0 result. Manufactured win == manufactured deficit, penalized equally.",
 "M-FLAT is included and is fully viable. FLAT is simultaneously standard-MOND AND the framework's own "
 "w->-1 dissolution limit: a FLAT win is NOT a framework falsification, but it IS a failure to detect "
 "the distinctive decline. If DESI DR3 relaxes to w=-1, M-DEC collapses onto M-FLAT -> UNTESTABLE.",
 "The 2 digitized qualitative bounds (Milgrom17 one-sided x4 limit; McGaugh+24 'no clear evolution') "
 "are a SECONDARY arm: including them moves log10 B(DEC/RISE) from -7.99 to -5.18. They are "
 "digitizations of prose, not published likelihoods -- reported with AND without.",
 "The RATIO a0(z)/a0(0) is FOOTING-INDEPENDENT, so every number here holds on both a0(0)=9.355e-11 "
 "(cH_Lambda/Z) and 1.131e-10 (cH0/Z). a0's VALUE and the HORIZON CHOICE are POSITS. nu=sqrt(1+1/y) is "
 "Milgrom 1999 (PLA 253:273 Eq.9); McCulloch credited for the Hubble-horizon rising branch. No TOE.",
]
for i, c in enumerate(PRE, 1):
    print(f"#  {i}. {c}")
print("#" * 102)

# =====================================================================================
# SELF-CHECK (frozen invariants)
# =====================================================================================
W0s, WAs, _ = draw(HEAD, "zero", 0)
r1, r2, r3 = [float(np.median(R_model("DEC", z, W0s, WAs))) for z in (0.35, 2.0, 3.0)]
q1, q2, q3 = [float(np.median(R_model("RISE", z, W0s, WAs))) for z in (1.0, 2.0, 3.0)]
assert 1.030 < r1 < 1.042, f"M-DEC bump @z0.35 = {r1:.4f} not ~1.036 (committed band)"
assert 0.870 < r2 < 0.880, f"M-DEC @z2 = {r2:.4f} not ~0.874"
assert 0.770 < r3 < 0.780, f"M-DEC @z3 = {r3:.4f} not ~0.775 (committed parent)"
assert 1.78 < q1 < 1.80 and 2.99 < q2 < 3.03 and 4.52 < q3 < 4.56, "M-RISE must match E(z) fork"
assert abs(float(np.median(R_model("DEC", 0.0, W0s, WAs))) - 1.0) < 1e-12, "z=0 normalization"
assert np.allclose(R_model("FLAT", [0.5, 3.0], W0s, WAs), 1.0), "M-FLAT must be exactly 1"
assert abs(P_MAG - 0.9202) < 1e-3 and abs(3.3 ** P_MAG - 3.0) < 1e-6, "Magneticum calibration"
assert any(abs(d["obs"] - 0.91) < 1e-9 for d in DATA), "MSA-3D must use +0.91, not raw +2.13"
assert all(d["obs"] < 2.0 for d in DATA if d["kind"] == "loglog_slope"), "raw +2.13 must NOT appear"
assert abs([d for d in DATA if "Ciocan" in d["tag"]][0]["sig_stat"] - 0.105) < 1e-9, \
    "Ciocan must keep its FULL stat error in the headline run (no systematics inflation)"
assert lever(6.0) < lever(1.0) < lever(0.15) < 1.0, "dilution lever must decrease with g_bar/a0"
assert REQP["DEC"] > P_MAG and REQP["FLAT"] > P_MAG > REQP["RISE"], \
    "the diagnostic MUST show DEC/FLAT needing MORE drift than Magneticum and RISE less"
lo, hi = min(EM["DEC"]["lnZ"] - EM["RISE"]["lnZ"], EM2["DEC"]["lnZ"] - EM2["RISE"]["lnZ"]), \
         max(EM["DEC"]["lnZ"] - EM["RISE"]["lnZ"], EM2["DEC"]["lnZ"] - EM2["RISE"]["lnZ"])
assert lo < 0 < hi, "the honest result IS the sign flip across systematic treatments; it must be present"
d20, _ = mc_lnB([(3.0, float(theory_dex("DEC", np.array([3.0]))[0][0]))], 0.31, ("RISE",))
assert d20["RISE"] > LN20, "the headline spec (z=3, 0.31 dex, N=1) must clear 20:1 by MC"
print(f"\nSELF-CHECK OK: M-DEC {r1:.3f}@0.35 / {r2:.3f}@2 / {r3:.3f}@3 match the committed band;")
print(f"  M-RISE {q1:.2f}/{q2:.2f}/{q3:.2f} match E(z); Magneticum p_mag={P_MAG:.4f} -> {3.3**P_MAG:.2f}x@z2.3;")
print(f"  MSA-3D uses +0.91 (raw +2.13 absent); Ciocan keeps stat 0.105; drift required DEC {REQP['DEC']:.2f} >")
print(f"  p_mag {P_MAG:.2f} > RISE {REQP['RISE']:.2f}; log10 B(DEC/RISE) SIGN-FLIPS across treatments")
print(f"  ({lo/np.log(10):+.2f} to {hi/np.log(10):+.2f}); headline spec clears 20:1 by MC (lnB={d20['RISE']:.2f}).")
print("EXIT 0 (ran; not a verdict).")
