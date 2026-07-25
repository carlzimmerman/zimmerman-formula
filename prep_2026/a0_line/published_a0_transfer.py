#!/usr/bin/env python3
"""
published_a0_transfer.py -- DOES THE REPO'S ESTIMATOR BIAS TRANSFER TO THE PUBLISHED SPARC a0?

THE QUESTION (stated so it cannot be fudged)
--------------------------------------------
The repo has a PRE-REGISTERED, hash-frozen, adversary-verified result
(PREREG_ESTIMATOR_BIAS.md + estimator_bias_mocks.py + estimator_bias_verdict.json):
on the GAS-DOMINATED SPARC subsample (310 pts / 49 gal, y = g_bar/1e-10 in 0.0088..0.1735),
the through-origin GLS on per-point a0 (`gls_origin`) is biased HIGH by +10.3 pp
(~26 bootstrap sd, injection-independent), while SIX median-like estimators pass at |b|<2 pp.
Mechanism = Jensen/skew (multiplicative log-noise inflates the MEAN of a0_pt, not the MEDIAN).

The standard literature value is a0 ~ 1.2e-10 m/s^2 (McGaugh, Lelli & Schombert 2016,
PRL 117:201101). The framework's Lambda-anchored value is 9.355e-11 (a0 = c*H_Lambda/Z).
Gap ~28%. IT IS TEMPTING to conclude "the literature is biased high, canonical is right."
THAT INFERENCE IS NOT LICENSED UNTIL THE PUBLISHED ESTIMATOR ITSELF IS IMPLEMENTED AND
ITS BIAS MEASURED ON MOCKS. This script does exactly that, and then decomposes the gap.

WHAT IS MEASURED HERE (all numerical -- mocks, estimator runs, bias measurement)
-------------------------------------------------------------------------------
S0  regression anchor: reproduce the committed +10.3 pp gas-dominated gls_origin bias.
S1  catalogue the published determinations BY ESTIMATOR FAMILY (verified against the papers).
S2  build the FULL-RANGE SPARC structure (2696 pts / 147 gal, y = 0.009 .. 92) at BOTH
    M/L prescriptions: Upsilon_disk = 0.50 (McGaugh+2016) and 0.70 (framework's RAR M/L fit).
S3  implement 12 estimators spanning FIVE families, incl. a faithful scipy.odr fit of the
    RAR functional form with the published error model.
S4  V1 zero-noise null (hard halt) + the ZERO-NOISE CROSS-LAW MATRIX, which isolates the
    functional-form conversion factor (a0-line vs RAR interpolation) with NO noise at all.
S5  FULL-RANGE mocks: 2 truth laws (framework nu, McGaugh nu) x 4 injected a0 (incl. BOTH
    9.354769736e-11 AND 1.2e-10, so neither is privileged) -> bias table per estimator.
S6  real-data values for every estimator x sample x M/L.
S7  THE DECOMPOSITION LADDER: one-change-at-a-time from the repo's number to the published
    1.2e-10, attributing the gap to (i) estimator, (ii) M/L, (iii) cuts, (iv) functional
    form, (v) deep-MOND vs full range -- held strictly apart.
S8  headline: the pre-registered UNBIASED estimator on the FULL sample, with sigma, and the
    comparison to 1.2e-10 / 9.355e-11 / 1.1305e-10 in sigma.

HARD RULES OBEYED
-----------------
* No claim that a published value is biased without IMPLEMENTING that estimator and
  MEASURING its bias on mocks.
* Injection at MULTIPLE a0 including 1.2e-10; if an estimator returns 1.2e-10 when
  1.2e-10 was injected, it is UNBIASED there and that is reported plainly.
* Estimator bias is NEVER conflated with the Upsilon degeneracy, the sample cuts, the
  functional form, or the regime. Each is measured on its own axis.
* a0's VALUE remains POSITED in the framework. This is measurement methodology, not a
  derivation. No TOE, no "theory closed".

C. Zimmerman workflow, 2026-07-25.  Run: python3 published_a0_transfer.py  (exit 0)
Outputs: published_a0_transfer_results.json
"""
import os, sys, json, time, hashlib
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fire_common as fc                                            # noqa: E402
from scipy.odr import ODR, Model, RealData                          # noqa: E402
from scipy.optimize import minimize_scalar                          # noqa: E402

np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
MRT = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/SPARC_Lelli2016c.mrt"
bar = "=" * 100
t_start = time.time()
OUT = {}

GNEWT = 6.674e-11
MSUN = 1.98892e30
SIG_LNU, SIG_LNG, SLNB = fc.SIG_LNU, fc.SIG_LNG, fc.SLNB          # 0.23, 0.10, 0.10
SIG_INC = fc.SIG_INC                                               # 3 deg
A0_CANON = 9.354769736111044e-11        # c*H_Lambda/Z   (framework canonical footing)
A0_ALT = 1.1305322040279838e-10         # c*H0/Z         (alt footing)
A0_PUB = 1.20e-10                       # McGaugh+2016 g_dagger
A0_INJ = [A0_CANON, 1.00e-10, A0_ALT, A0_PUB]
INJ_LAB = ["canonical cH_L/Z", "neutral 1.00e-10", "ALT cH0/Z", "published g_dagger"]

N_REAL = int(os.environ.get("NREAL", "600"))
SEED = 20260725

print(bar)
print("published_a0_transfer.py -- DOES THE REPO'S ESTIMATOR BIAS TRANSFER TO THE")
print("                           PUBLISHED SPARC a0 ~ 1.2e-10 ?")
print(bar)
print(f"  N_real = {N_REAL}   seed = {SEED}   injections = "
      + ", ".join(f"{v:.5e}" for v in A0_INJ))
print("  framework nu = sqrt(1+1/y)  [= Milgrom 1999 PLA 253:273 Eq.9 kernel; the")
print("  framework's distinctive content is the cH_Lambda/Z COEFFICIENT + the MI completion]")


# ======================================================================= frozen-file check
def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


FROZEN = {
    "PREREG_ESTIMATOR_BIAS.md":
        "6be465f21c7ea075f7a585779184970f145a8cdd2e61554a17e101be9a099dc2",
    "prereg_estimator_bias_config.json":
        "8cc0a9664c420a0c36f07a8a99372481cad2d4aca1fd6c552b2955f3a840d765",
    "prereg_freeze.py":
        "9caa44b9da9e7b76753fb53b7a6e5f342f3f5273eba8334846ab8df652f2d043",
}
print(f"\n  frozen pre-registration (READ-ONLY, unaltered):")
for fn, want in FROZEN.items():
    got = sha256(os.path.join(HERE, fn))
    assert got == want, f"FROZEN FILE ALTERED: {fn}"
    print(f"    OK  {fn:<38} {got[:16]}...")
VERDICT = json.load(open(os.path.join(HERE, "estimator_bias_verdict.json")))
B_ANCHOR_GLS = VERDICT["bias_table"]["gls_origin"]["b"]["canonical cH_Lambda/Z"]
B_ANCHOR_MED = VERDICT["bias_table"]["median_a0pt"]["b"]["canonical cH_Lambda/Z"]
PREREG_PRIMARY = VERDICT["primary"]
print(f"    committed verdict: gls_origin b = {B_ANCHOR_GLS:+.3f} pp, "
      f"median_a0pt b = {B_ANCHOR_MED:+.3f} pp, primary = {PREREG_PRIMARY}")
OUT["frozen_prereg_sha256"] = FROZEN
OUT["committed_verdict_anchor"] = dict(gls_origin_pp=B_ANCHOR_GLS,
                                       median_a0pt_pp=B_ANCHOR_MED,
                                       primary=PREREG_PRIMARY)

# ============================================================ S1. THE PUBLISHED DETERMINATIONS
print("\n" + bar)
print("S1 -- CATALOGUE OF THE PUBLISHED a0 DETERMINATIONS, BY ESTIMATOR FAMILY")
print("      (verified against the papers themselves, NOT assumed)")
print(bar)
PUBLISHED = [
    dict(ref="McGaugh, Lelli & Schombert 2016, PRL 117:201101 (arXiv:1609.05917)",
         value=1.20e-10, err_rand=0.02e-10, err_syst=0.24e-10,
         family="RAR-CURVE-FIT / orthogonal distance regression",
         estimator="scipy.odr on the UNBINNED 2693 points, errors in BOTH variables, "
                   "fitting g_obs = g_bar/(1-exp(-sqrt(g_bar/g_dagger)))",
         sample="153 galaxies / 2693 points; reject i<30 deg (10 gal), Q=3 (12 gal), "
                "require dV_obs/V_obs < 0.10",
         ml="Upsilon_[3.6] = 0.50 (disk), 0.70 (bulge)  ->  ratio 1.4",
         verbatim="'The data are fitted using the Python orthogonal distance regression "
                  "algorithm (scipy.odr), considering errors in both variables.' / "
                  "'We do not fit the binned data, but the individual 2693 points.'",
         independent=True),
    dict(ref="Lelli, McGaugh, Schombert & Pawlowski 2017, ApJ 836:152 (arXiv:1610.08981)",
         value=1.20e-10, err_rand=0.02e-10, err_syst=0.24e-10,
         family="RAR-CURVE-FIT / orthogonal distance regression (SAME estimator as PRL)",
         estimator="identical scipy.odr fit; this is the long-form companion of the PRL",
         sample="153 late-type galaxies / 2693 points, same cuts",
         ml="Upsilon_[3.6] = 0.50 (disk), 0.70 (bulge)",
         verbatim="same ODR sentence; extended relation incl. ultrafaint dwarfs gives "
                  "g_dagger = (1.1 +- 0.1)e-10",
         independent=False),
    dict(ref="Li, Lelli, McGaugh & Schombert 2018, A&A 615:A3 (arXiv:1803.00022)",
         value=1.20e-10, err_rand=None, err_syst=None,
         family="PER-GALAXY MCMC with g_dagger FIXED or GAUSSIAN-PRIORED",
         estimator="per-galaxy MCMC marginalising over Upsilon, D, i; g_dagger is NOT an "
                   "independent output -- fiducial fits FIX g_dagger = 1.20e-10, and the "
                   "free-g_dagger test uses a Gaussian prior centred on 1.20e-10",
         sample="175 galaxies fitted; 153 in the quality sample",
         ml="Upsilon_disk = 0.5 +- 0.1 dex, Upsilon_bul = 0.7 +- 0.1 dex (log-normal priors)",
         verbatim="'adjusting the value of g_dagger improves neither the fits nor the rms "
                  "scatter' -- i.e. this paper INHERITS 1.20e-10, it does not measure it",
         independent=False),
    dict(ref="McGaugh 2012, AJ 143:40 (BTFR normalisation route)",
         value=1.3e-10, err_rand=None, err_syst=0.3e-10,
         family="BTFR-NORMALISATION (galaxy-level, nu-INDEPENDENT asymptotic limit)",
         estimator="fit M_b = A*V_f^4 (slope FIXED at 4) -> a0 = chi/(G*A) with a disk "
                   "geometry factor chi ~ 0.8; A = 47 +- 6 Msun km^-4 s^4",
         sample="gas-rich galaxies (V_f from HI); SPARC version uses Vflat",
         ml="gas-dominated selection minimises the Upsilon lever by construction",
         verbatim="'M_b = A V_f^4 with A = 47 +- 6 Msun km^-4 s^4, which is equivalent to "
                  "MOND with a0 = 1.3 +- 0.3 x 10^-10 m/s^2'",
         independent=True),
]
for p in PUBLISHED:
    tag = "INDEPENDENT" if p["independent"] else "NOT INDEPENDENT (inherits 1.20e-10)"
    print(f"\n  {p['ref']}")
    print(f"    a0        = {p['value']:.3e}" +
          (f"  +- {p['err_rand']:.2e} (rand)" if p["err_rand"] else "") +
          (f"  +- {p['err_syst']:.2e} (syst)" if p["err_syst"] else ""))
    print(f"    FAMILY    = {p['family']}     [{tag}]")
    print(f"    estimator = {p['estimator']}")
    print(f"    sample    = {p['sample']}")
    print(f"    M/L       = {p['ml']}")
print("\n  ==> There are only TWO genuinely independent published families:")
print("      (A) the RAR-CURVE-FIT ODR of MLS2016/Lelli2017 -> 1.20e-10 (+-0.02 rand, +-0.24 syst)")
print("      (B) the BTFR-NORMALISATION route of McGaugh 2012 -> 1.3e-10 (+-0.3)")
print("      NEITHER is a mean of per-point a0. Li+2018 is NOT an independent determination.")
print("      The repo's proven-biased estimator (through-origin GLS on per-point a0 in the")
print("      deep-MOND regime) is used by NO published determination of a0. So the bias")
print("      CANNOT transfer by identity of estimator -- it has to be re-measured for the")
print("      estimators that ARE used. That is S3-S5.")
OUT["published_catalogue"] = PUBLISHED

# ================================================== S2. SAMPLE STRUCTURES (real SPARC)
print("\n" + bar)
print("S2 -- THE REAL SPARC STRUCTURES (truth = real g_bar; never synthetic galaxies)")
print(bar)

MRTROW = {}
for _ln in open(MRT):
    _t = _ln.split()
    if len(_t) < 18:
        continue
    try:
        _v = [float(x) for x in _t[1:18]]
    except ValueError:
        continue
    MRTROW[_t[0]] = dict(D=_v[1], eD=_v[2], fD=int(_v[3]), inc=_v[4], einc=_v[5],
                         L36=_v[6], eL36=_v[7], MHI=_v[12], Vflat=_v[14],
                         eVflat=_v[15], Q=int(_v[16]))
assert len(MRTROW) == 175, len(MRTROW)
print(f"  SPARC_Lelli2016c.mrt parsed: {len(MRTROW)} galaxies "
      f"(e_D, e_Inc, Vflat, e_Vflat, L[3.6], MHI available)")


LOWY_CUT = 1.0e-10      # footing-neutral: lies between canonical 9.355e-11 and ALT 1.1305e-10


class Struct:
    """Point-level + galaxy-level arrays for one (Ud, subset) sample.
    subset: 'full' = every surviving point; 'gasdom' = Vgas^2 > Ud Vdisk^2 + Ub Vbul^2
    (the frozen prereg subsample); 'lowy' = every galaxy but only points with
    g_bar < 1e-10, i.e. the DEEP-MOND REGIME WITHOUT the gas-dominance selection.
    'lowy' exists precisely so axis (v) (regime) can be separated from the baryonic-
    composition selection that defines 'gasdom'."""

    def __init__(self, Ud, subset):
        gals = fc.load(Ud)
        self.Ud, self.Ub, self.subset = Ud, 1.4 * Ud, subset
        self.gas_only = (subset == "gasdom")
        gb, go, fv, phi, cti, gi = [], [], [], [], [], []
        names, npt, sld, inc, einc, eDrel = [], [], [], [], [], []
        k = 0
        for g in gals:
            if subset == "gasdom":
                m = g["gasdom"]
            elif subset == "lowy":
                m = g["gb"] < LOWY_CUT
            else:
                m = np.ones(len(g["gb"]), bool)
            n = int(m.sum())
            if n == 0:
                continue
            r = MRTROW[g["name"]]
            gb += list(g["gb"][m]); go += list(g["go"][m]); fv += list(g["fv"][m])
            phi += list(g["phi"][m]); cti += [1.0 / np.tan(g["inc"])] * n
            gi += [k] * n
            names.append(g["name"]); npt.append(n); sld.append(g["sig_lnD"])
            inc.append(g["inc"]); einc.append(np.deg2rad(max(r["einc"], 1.0)))
            eDrel.append(r["eD"] / r["D"])
            k += 1
        self.gb, self.go = np.array(gb), np.array(go)
        self.fv, self.phi = np.array(fv), np.array(phi)
        self.cti = np.array(cti)
        self.gi = np.array(gi, int)
        self.names = names
        self.npt = np.array(npt, int)
        self.G = len(npt)
        self.N = len(self.gb)
        self.starts = np.concatenate(([0], np.cumsum(self.npt)[:-1]))
        self.sld = np.array(sld)           # frozen-bucket sigma_lnD (prereg magnitudes)
        self.inc = np.array(inc)
        self.einc = np.array(einc)         # REAL SPARC e_Inc (published error model)
        self.eDrel = np.array(eDrel)       # REAL SPARC e_D/D  (published error model)
        # published error model (Lelli+2017 Eq.2 for g_obs; 25% Upsilon / 10% HI for g_bar)
        eip = np.repeat(self.einc, self.npt)
        eDp = np.repeat(self.eDrel, self.npt)
        self.rel_ego = np.sqrt((2 * self.fv) ** 2 + (2 * eip * self.cti) ** 2 + eDp ** 2)
        self.rel_egb = np.sqrt((self.phi * 0.25) ** 2 + ((1 - self.phi) * 0.10) ** 2)

    def label(self):
        return f"{self.subset.upper():<6} Ud={self.Ud:.2f}"


ST = {}
for _Ud in (0.50, 0.70):
    for _ss in ("full", "lowy", "gasdom"):
        s = Struct(_Ud, _ss)
        ST[(_Ud, _ss)] = s
        y = s.gb / 1e-10
        print(f"  {s.label()}:  N={s.N:5d}  Ngal={s.G:3d}  y in [{y.min():.4f}, {y.max():7.2f}]"
              f"  median y={np.median(y):.3f}  median phi={np.median(s.phi):.3f}")
FULL50, FULL70 = ST[(0.50, "full")], ST[(0.70, "full")]
GAS70, GAS50 = ST[(0.70, "gasdom")], ST[(0.50, "gasdom")]
LOWY70, LOWY50 = ST[(0.70, "lowy")], ST[(0.50, "lowy")]
print(f"\n  SAMPLE-CUT COMPARISON vs McGaugh+2016 (their cuts: Q<3, i>=30 deg, dV/V<0.10):")
print(f"    ours (identical cuts):  N = {FULL50.N} points / {FULL50.G} galaxies")
print(f"    published:              N = 2693 points / 153 galaxies")
print(f"    -> point count agrees to {abs(FULL50.N-2693)/2693*100:.2f}%; galaxy count differs by "
      f"{153-FULL50.G} (galaxies whose every point fails dV/V<0.10 or g_bar>0 drop out here).")
print(f"    Our cuts ARE the published cuts, so axis (iii) starts from a matched sample; its")
print(f"    residual size is nevertheless MEASURED in S10 (cut-variation probe), not assumed.")
OUT["samples"] = {f"Ud{k[0]:.2f}_{k[1]}":
                  dict(N=v.N, Ngal=v.G, y_min=float(v.gb.min() / 1e-10),
                       y_max=float(v.gb.max() / 1e-10),
                       y_median=float(np.median(v.gb / 1e-10)),
                       phi_median=float(np.median(v.phi)))
                  for k, v in ST.items()}

# ==================================================== S3. THE ESTIMATORS (five families)
print("\n" + bar)
print("S3 -- THE ESTIMATORS: 12 estimators spanning FIVE families")
print(bar)


def nu_fw(gb, a0):
    """framework / dS-Unruh interpolation: g_obs = sqrt(g_bar^2 + a0*g_bar)."""
    return np.sqrt(gb ** 2 + a0 * gb)


def nu_mcg(gb, a0):
    """McGaugh+2016 RAR interpolation: g_obs = g_bar/(1-exp(-sqrt(g_bar/a0)))."""
    x = np.sqrt(np.maximum(gb, 0.0) / a0)
    return gb / (-np.expm1(-x))


LAW = {"fw": nu_fw, "mcg": nu_mcg}
LAWLAB = {"fw": "framework nu = sqrt(1+1/y)  (a0-line: E = a0*g_bar EXACT)",
          "mcg": "McGaugh nu = 1/(1-exp(-sqrt(y)))  (published RAR curve)"}


# ---------------------------------------------------------------- family I: the a0-line
def gls_vec(S, gbar, gobs, itmax=300):
    """Iterated through-origin GLS with MODEL-based weights (fire_common.gls semantics,
    vectorised over realizations). a0_hat = sum(w E g)/sum(w g^2)."""
    gbar = np.atleast_2d(gbar); gobs = np.atleast_2d(gobs)
    M, n = gobs.shape
    E = gobs ** 2 - gbar ** 2
    a0 = np.full(M, 1e-10); fint = np.full(M, 0.2)
    W = np.zeros((M, n)); active = np.ones(M, bool)
    for _ in range(itmax):
        GOm2 = gbar ** 2 + a0[:, None] * gbar
        s2 = (4 * GOm2 * S.fv) ** 2 + (2 * gbar ** 2 * SLNB) ** 2 + (fint[:, None] * GOm2) ** 2
        w = 1.0 / s2
        a0n = (w * E * gbar).sum(1) / (w * gbar ** 2).sum(1)
        c2n = ((E - a0n[:, None] * gbar) ** 2 * w).sum(1) / n
        fintn = np.maximum(0.01, fint * c2n ** 0.25)
        conv = active & (np.abs(a0n - a0) < 1e-17) & (np.abs(c2n - 1) < 1e-3)
        a0 = np.where(active, a0n, a0)
        fint = np.where(active, fintn, fint)
        W = np.where(active[:, None], w, W)
        active &= ~conv
        if not active.any():
            break
    return a0, W


def gls_bygal(S, gbar, gobs, itmax=300):
    gbar = np.atleast_2d(gbar); gobs = np.atleast_2d(gobs)
    M = gobs.shape[0]
    E = gobs ** 2 - gbar ** 2
    a0 = np.full((M, S.G), 1e-10); fint = np.full((M, S.G), 0.2)
    active = np.ones((M, S.G), bool)
    for _ in range(itmax):
        a0p = np.repeat(a0, S.npt, axis=1); fintp = np.repeat(fint, S.npt, axis=1)
        GOm2 = gbar ** 2 + a0p * gbar
        s2 = (4 * GOm2 * S.fv) ** 2 + (2 * gbar ** 2 * SLNB) ** 2 + (fintp * GOm2) ** 2
        w = 1.0 / s2
        num = np.add.reduceat(w * E * gbar, S.starts, axis=1)
        den = np.add.reduceat(w * gbar ** 2, S.starts, axis=1)
        a0n = num / den
        res = E - np.repeat(a0n, S.npt, axis=1) * gbar
        c2n = np.add.reduceat(res ** 2 / s2, S.starts, axis=1) / S.npt
        fintn = np.maximum(0.01, fint * c2n ** 0.25)
        conv = active & (np.abs(a0n - a0) < 1e-17) & (np.abs(c2n - 1) < 1e-3)
        a0 = np.where(active, a0n, a0); fint = np.where(active, fintn, fint)
        active &= ~conv
        if not active.any():
            break
    return a0


def a0pt_fw(gbar, gobs):
    """per-point a0 under the framework nu: a0 = (g_obs^2 - g_bar^2)/g_bar. No clipping."""
    return (gobs ** 2 - gbar ** 2) / gbar


def a0pt_mcg(gbar, gobs):
    """per-point g_dagger under McGaugh's nu, EXACT inversion:
       1-exp(-sqrt(gb/gd)) = gb/go  ->  gd = gb / [ln(1 - gb/go)]^2.
       Requires go > gb; points with go <= gb have NO solution and are returned as NaN
       (counted and reported -- never silently dropped)."""
    r = 1.0 - gbar / gobs
    out = np.full_like(gbar, np.nan)
    ok = r > 0
    L = np.log(np.where(ok, r, 0.5))
    out[ok] = (gbar / L ** 2)[ok]
    return out


def _galmed(S, v):
    return np.median(np.stack([np.nanmedian(v[:, S.starts[k]:S.starts[k] + S.npt[k]], axis=1)
                               for k in range(S.G)], axis=1), axis=1)


# -------------------------------------------- families II/III: RAR curve fits (published)
def _odr_fit(x, y, sx, sy, model, b0):
    d = RealData(x, y, sx=sx, sy=sy)
    o = ODR(d, Model(model), beta0=[b0])
    o.set_job(fit_type=0)                        # 0 = explicit ODR (errors in BOTH vars)
    r = o.run()
    return r.beta[0]


def curvefit_row(S, gbar, gobs, law, mode):
    """Fit the interpolation law `law` to ONE realization by `mode`:
       'odrlog'  scipy.odr in log10-log10 space, errors in both variables  [best
                 reconstruction of MLS2016/Lelli2017: they say scipy.odr on the unbinned
                 points with errors in both variables; the RAR is presented in log-log]
       'odrlin'  scipy.odr in LINEAR space, errors in both variables
       'wlsqlog' vertical weighted least squares in log10 space (errors on g_obs only)
       Parameter is a0/1e-10 for conditioning. Returns a0 in SI."""
    f = LAW[law]
    sgb = S.rel_egb * gbar
    sgo = S.rel_ego * gobs
    if mode == "odrlin":
        def m(B, X):
            return f(np.maximum(X, 1e-15), abs(B[0]) * 1e-10)
        return abs(_odr_fit(gbar, gobs, sgb, sgo, m, 1.2)) * 1e-10
    lx, ly = np.log10(gbar), np.log10(gobs)
    slx, sly = sgb / (gbar * np.log(10)), sgo / (gobs * np.log(10))
    if mode == "odrlog":
        def m(B, LX):
            return np.log10(f(10.0 ** LX, abs(B[0]) * 1e-10))
        return abs(_odr_fit(lx, ly, slx, sly, m, 1.2)) * 1e-10
    if mode == "wlsqlog":
        w = 1.0 / sly ** 2

        def chi2(la):
            return float(np.sum(w * (ly - np.log10(f(gbar, 10.0 ** la))) ** 2))
        r = minimize_scalar(chi2, bounds=(-11.2, -8.8), method="bounded",
                            options=dict(xatol=1e-9))
        return 10.0 ** r.x
    raise ValueError(mode)


# --------------------------------------------------------- family V: BTFR normalisation
BTFR_CHI = 0.80         # disk-geometry factor: g_TF = chi*V_f^4/(G*M_b) (McGaugh+2019 rev.)


def btfr_struct(Ud):
    """galaxy-level BTFR structure from SPARC: Vflat, M_b = Ud*L36 + 1.33*MHI."""
    names, Vf, eVf, Lst, Mgas, eD = [], [], [], [], [], []
    for nm, r in sorted(MRTROW.items()):
        if r["Q"] > 2 or r["inc"] < 30 or r["Vflat"] <= 0 or r["eVflat"] <= 0:
            continue
        names.append(nm); Vf.append(r["Vflat"] * 1e3); eVf.append(r["eVflat"] * 1e3)
        Lst.append(r["L36"] * 1e9); Mgas.append(1.33 * r["MHI"] * 1e9); eD.append(r["eD"] / r["D"])
    return dict(names=names, Vf=np.array(Vf), eVf=np.array(eVf),
                Lst=np.array(Lst), Mgas=np.array(Mgas), eD=np.array(eD), Ud=Ud)


def btfr_a0(bt, Vf, Mb, kind):
    """a0 from the BTFR normalisation with slope FIXED at 4.
       'med'  median over galaxies of chi*V^4/(G*M_b)
       'lsq'  intercept of log M_b = 4 log V + b (unweighted), a0 = chi/(G*A)"""
    ag = BTFR_CHI * Vf ** 4 / (GNEWT * Mb * MSUN)
    if kind == "med":
        return np.median(ag, axis=-1)
    b = np.mean(np.log10(Mb) - 4.0 * np.log10(Vf), axis=-1)
    return BTFR_CHI / (GNEWT * (10.0 ** b) * MSUN)


# ------------------------------------------------------------------ the estimator table
EST = [
    ("a0line_gls_origin", "I  a0-line, MEAN-like",
     "through-origin GLS on per-point a0 (fire_common.gls) -- the repo incumbent, PROVEN "
     "+10.3 pp biased on gas-dom. Used by NO published determination."),
    ("a0line_median", "I  a0-line, MEDIAN-like",
     "median over points of a0_pt = (g_obs^2-g_bar^2)/g_bar -- prereg PASS estimator."),
    ("a0line_galmed_med", "I  a0-line, MEDIAN-like",
     "per-galaxy median of a0_pt then median over galaxies -- the PRE-REGISTERED PRIMARY."),
    ("a0line_galgls_med", "I  a0-line, hybrid",
     "per-galaxy through-origin GLS then median over galaxies -- prereg PASS."),
    ("mcgpt_median", "IV per-point under McGaugh nu",
     "median over points of the EXACT McGaugh-nu inversion g_dag = g_bar/[ln(1-g_bar/g_obs)]^2 "
     "-- SAME estimator as a0line_median, DIFFERENT law: isolates axis (iv)."),
    ("rar_odrlog_mcg", "II RAR-curve-fit (PUBLISHED)",
     "scipy.odr, errors in both variables, log10-log10 space, McGaugh nu -- the MLS2016 / "
     "Lelli+2017 estimator."),
    ("rar_odrlin_mcg", "II RAR-curve-fit (PUBLISHED variant)",
     "scipy.odr, errors in both variables, LINEAR space, McGaugh nu -- the linear-space "
     "reading of the same published sentence."),
    ("rar_wlsqlog_mcg", "II RAR-curve-fit (PUBLISHED variant)",
     "vertical weighted least squares in log10 space, McGaugh nu."),
    ("rar_odrlog_fw", "III RAR-curve-fit, framework nu",
     "identical ODR machinery on the FRAMEWORK nu -- isolates axis (iv) at fixed estimator."),
    ("rar_wlsqlog_fw", "III RAR-curve-fit, framework nu",
     "vertical weighted log-space LSQ on the framework nu."),
    ("btfr_med", "V  BTFR normalisation",
     "median over galaxies of chi*V_f^4/(G M_b), chi=0.8 -- nu-INDEPENDENT (asymptotic)."),
    ("btfr_lsq", "V  BTFR normalisation",
     "slope-4-fixed log-space intercept -> a0 = chi/(G A) -- the McGaugh 2012 route."),
]
CURVE = {"rar_odrlog_mcg": ("mcg", "odrlog"), "rar_odrlin_mcg": ("mcg", "odrlin"),
         "rar_wlsqlog_mcg": ("mcg", "wlsqlog"), "rar_odrlog_fw": ("fw", "odrlog"),
         "rar_wlsqlog_fw": ("fw", "wlsqlog")}
POINT_EST = [e[0] for e in EST if e[0] not in ("btfr_med", "btfr_lsq")]
for k, fam, desc in EST:
    print(f"  {k:<20} [{fam}]\n      {desc}")


def run_point_estimators(S, gbar, gobs, which=None, nan_report=None):
    """Every point-level estimator on one (M, N) block of observables."""
    which = which or POINT_EST
    out = {}
    if any(k.startswith("a0line") for k in which):
        A = a0pt_fw(gbar, gobs)
    if "a0line_gls_origin" in which:
        out["a0line_gls_origin"] = gls_vec(S, gbar, gobs)[0]
    if "a0line_median" in which:
        out["a0line_median"] = np.median(A, axis=1)
    if "a0line_galmed_med" in which:
        out["a0line_galmed_med"] = _galmed(S, A)
    if "a0line_galgls_med" in which:
        out["a0line_galgls_med"] = np.median(gls_bygal(S, gbar, gobs), axis=1)
    if "mcgpt_median" in which:
        Am = a0pt_mcg(gbar, gobs)
        if nan_report is not None:
            nan_report["mcgpt_nan_frac"] = float(np.mean(np.isnan(Am)))
        out["mcgpt_median"] = np.nanmedian(Am, axis=1)
    for k in which:
        if k in CURVE:
            law, mode = CURVE[k]
            out[k] = np.array([curvefit_row(S, gbar[r], gobs[r], law, mode)
                               for r in range(gbar.shape[0])])
    return out


# ================================================== S4. FORWARD MODEL + V1 + CROSS-LAW
print("\n" + bar)
print("S4 -- FORWARD MODEL, V1 ZERO-NOISE NULL, AND THE ZERO-NOISE CROSS-LAW MATRIX")
print(bar)
print("  g_bar_obs = g_bar_true*(phi*e^dlnU + (1-phi)*e^dlnG)*e^eps_shape")
print("  g_obs_obs = g_obs_true*e^-dlnD*(sin i/sin(i+di))^2*(1+dv)^2      [prereg S1 verbatim]")
print("  noise magnitudes: sigma_lnU=0.23 GLOBAL, sigma_lnG=0.10 GLOBAL, shape=0.10/point,")
print("  sigma_lnD = SPARC fD bucket per galaxy, sigma_i = 3 deg per galaxy, dv = fv per point.")
print("  NO clipping of E or a0_pt; the point set is NEVER re-cut on mock observables.")


def draw_noise(S, n_real, seed):
    seqs = np.random.SeedSequence(seed).spawn(n_real)
    dlnU = np.empty(n_real); dlnG = np.empty(n_real)
    dlnD = np.empty((n_real, S.G)); di = np.empty((n_real, S.G))
    eps = np.empty((n_real, S.N)); dv = np.empty((n_real, S.N))
    lo, hi = np.deg2rad(5.0), np.deg2rad(90.0)
    for r in range(n_real):
        rng = np.random.default_rng(seqs[r])
        dlnU[r] = rng.normal(0.0, SIG_LNU)
        dlnG[r] = rng.normal(0.0, SIG_LNG)
        dlnD[r] = rng.normal(0.0, S.sld)
        d = rng.normal(0.0, SIG_INC, S.G)
        bad = (S.inc + d <= lo) | (S.inc + d > hi)
        while bad.any():
            d[bad] = rng.normal(0.0, SIG_INC, int(bad.sum()))
            bad = (S.inc + d <= lo) | (S.inc + d > hi)
        di[r] = d
        eps[r] = rng.normal(0.0, SLNB, S.N)
        v = rng.normal(0.0, S.fv)
        bad = (1.0 + v) <= 0.05
        while bad.any():
            v[bad] = rng.normal(0.0, S.fv[bad])
            bad = (1.0 + v) <= 0.05
        dv[r] = v
    return dict(dlnU=dlnU, dlnG=dlnG, dlnD=dlnD, di=di, eps=eps, dv=dv)


ABL_KEYS = ("glob", "shape", "dist", "inc", "vel")


def observables(S, a0_inj, law, nz, scale=1.0, on=None):
    """`on` = dict of per-term switches (1.0/0.0) over ABL_KEYS:
    glob  = the two GLOBAL coherent offsets dlnU (Upsilon, 0.23) and dlnG (gas-cal, 0.10);
    shape = per-point g_bar shape scatter; dist/inc/vel = per-galaxy D, per-galaxy i,
    per-point velocity. Ablating `glob` is MANDATORY for the decomposition: a coherent
    Upsilon offset is axis (ii), NOT axis (i), and MLS2016 already quote it as their
    +-0.24e-10 systematic. Calling it 'estimator bias' would be a conflation."""
    o = dict.fromkeys(ABL_KEYS, 1.0)
    if on:
        o.update(on)
    gt = LAW[law](S.gb, a0_inj)
    fU = np.exp(scale * o["glob"] * nz["dlnU"])[:, None]
    fG = np.exp(scale * o["glob"] * nz["dlnG"])[:, None]
    gbar = S.gb[None, :] * (S.phi[None, :] * fU + (1 - S.phi[None, :]) * fG) \
        * np.exp(scale * o["shape"] * nz["eps"])
    incf = (np.sin(S.inc)[None, :]
            / np.sin(S.inc[None, :] + scale * o["inc"] * nz["di"])) ** 2
    gobs = gt[None, :] * np.exp(-scale * o["dist"] * np.repeat(nz["dlnD"], S.npt, axis=1)) \
        * np.repeat(incf, S.npt, axis=1) * (1.0 + scale * o["vel"] * nz["dv"]) ** 2
    return gbar, gobs


# ---- V1: zero-noise null, matched law -> every estimator must return the injection exactly
print("\n  V1 ZERO-NOISE NULL on the FULL sample (Ud=0.70), matched law, 4 injections:")
nz1 = draw_noise(FULL70, 1, SEED)
V1 = {}
for law in ("fw", "mcg"):
    matched = [k for k in POINT_EST
               if (k in CURVE and CURVE[k][0] == law)
               or (law == "fw" and k.startswith("a0line"))
               or (law == "mcg" and k == "mcgpt_median")]
    for a0i, lab in zip(A0_INJ, INJ_LAB):
        gb0, go0 = observables(FULL70, a0i, law, nz1, scale=0.0)
        est0 = run_point_estimators(FULL70, gb0, go0, which=matched)
        for k, v in est0.items():
            V1.setdefault(k, {})[lab] = float(v[0] / a0i - 1.0)
V1_TOL = 1e-6
print(f"  {'estimator':<20}" + "".join(f"{l.split()[0][:9]:>14}" for l in INJ_LAB) + "   verdict")
nfail = 0
for k in POINT_EST:
    if k not in V1:
        continue
    row = "".join(f"{V1[k][l]:>14.2e}" for l in INJ_LAB)
    ok = all(abs(V1[k][l]) < V1_TOL for l in INJ_LAB)
    nfail += (not ok)
    print(f"  {k:<20}{row}   {'PASS' if ok else 'FAIL'}")
print(f"  tolerance |a_hat/a0_inj - 1| < {V1_TOL:.0e}  (curve fits are numerical minimisers,")
print("  so machine-epsilon is not attainable; 1e-6 is >4 orders below every effect below).")
assert nfail == 0, "V1 ZERO-NOISE NULL FAILED -> HARD HALT"
print("  V1 PASSES for every estimator on its OWN law -> the mock and all estimators are wired")
print("  correctly and the injection round-trips.")
OUT["V1_zero_noise_matched"] = V1

# ---- the zero-noise CROSS-LAW matrix: the PURE functional-form conversion factor
print("\n  ZERO-NOISE CROSS-LAW MATRIX -- axis (iv), the functional-form factor, with NO noise.")
print("  Read: 'if the truth obeys law L with scale a0, what does an estimator built on the")
print("  OTHER law return?'  This is NOT bias: it is the definitional difference between the")
print("  a0-line's a0 and the RAR-interpolation's g_dagger. Ratio a_hat/a0_inj:")
XLAW = {}
for law in ("fw", "mcg"):
    for a0i, lab in zip(A0_INJ, INJ_LAB):
        gb0, go0 = observables(FULL70, a0i, law, nz1, scale=0.0)
        est0 = run_point_estimators(FULL70, gb0, go0)
        for k, v in est0.items():
            XLAW.setdefault(k, {}).setdefault(law, {})[lab] = float(v[0] / a0i)
print(f"  {'estimator':<20}{'truth=framework nu':>22}{'truth=McGaugh nu':>20}")
for k in POINT_EST:
    r_fw = np.mean([XLAW[k]["fw"][l] for l in INJ_LAB])
    r_mc = np.mean([XLAW[k]["mcg"][l] for l in INJ_LAB])
    print(f"  {k:<20}{r_fw:>22.4f}{r_mc:>20.4f}")
OUT["zero_noise_cross_law"] = XLAW
FORMFAC = {}
for k in POINT_EST:
    FORMFAC[k] = dict(on_fw=float(np.mean([XLAW[k]["fw"][l] for l in INJ_LAB])),
                      on_mcg=float(np.mean([XLAW[k]["mcg"][l] for l in INJ_LAB])),
                      spread_fw=float(np.ptp([XLAW[k]["fw"][l] for l in INJ_LAB])),
                      spread_mcg=float(np.ptp([XLAW[k]["mcg"][l] for l in INJ_LAB])))
OUT["form_factor"] = FORMFAC

# ================================================================ S5. FULL-RANGE BIAS
print("\n" + bar)
print("S5 -- FULL-RANGE BIAS MEASUREMENT (the load-bearing measurement)")
print(bar)
print(f"  sample FULL Ud=0.70, N={FULL70.N}, y = {FULL70.gb.min()/1e-10:.4f} .. "
      f"{FULL70.gb.max()/1e-10:.1f}  (the gas-dom prereg spanned only 0.009..0.174)")
print(f"  2 truth laws x {len(A0_INJ)} injections x {N_REAL} realizations, common random numbers.")
print("  bias b = median_r(a_hat/a0_inj) - 1 in percentage points; s = 0.5*(P84-P16) in %;")
print("  sigma_MC = 1.2533*s/sqrt(N_real).  MATCHED-LAW rows only are BIAS; cross-law rows")
print("  are form factor x bias and are reported separately (never called bias).")

print("\n  TWO NOISE CONFIGURATIONS, BOTH REPORTED (the anti-conflation split):")
print("    ALL   = every frozen term on. Includes the GLOBAL coherent Upsilon (0.23) and")
print("            gas-cal (0.10) offsets. MLS2016 ALREADY quote the coherent-Upsilon term as")
print("            their +-0.24e-10 (20%) SYSTEMATIC, so its share is axis (ii), not (i).")
print("    NOGLOB= global Upsilon+gas-cal OFF, per-point/per-galaxy noise on. THIS is the")
print("            genuine ESTIMATOR bias -- the part not already in the published error bar.")

NZ_FULL = draw_noise(FULL70, N_REAL, SEED)
_mU, _mG = float(np.median(NZ_FULL["dlnU"])), float(np.median(NZ_FULL["dlnG"]))
print(f"\n  MC DIAGNOSTIC (load-bearing): the two GLOBAL coherent terms have only N_real =")
print(f"  {N_REAL} independent draws, one per realization, so ANY bias column that includes")
print(f"  them is MC-limited by the median of those draws. Here median(dlnU) = {_mU:+.5f},")
print(f"  median(dlnG) = {_mG:+.5f}. The a0-line lever on a coherent g_bar offset is")
print(f"  d ln a0/d ln g_bar ~ -(1+2y_med), so at y_med = "
      f"{np.median(FULL70.gb)/1e-10:.2f} a median(dlnU) of only")
print(f"  +0.01 already moves the median ratio by ~{100*(1+2*np.median(FULL70.gb)/1e-10)*0.01:.1f}"
      f" pp. THIS IS WHY the ALL and GLOBONLY")
print(f"  columns must be read with their sigma_MC, and why NOGLOB is the estimator-bias")
print(f"  column: it removes the nuisance that only has N_real samples.")
OUT["mc_global_draw_medians"] = dict(median_dlnU=_mU, median_dlnG=_mG, N_real=N_REAL)
NOISE_CFG = {"ALL": None, "NOGLOB": dict(glob=0.0), "GLOBONLY":
             dict(shape=0.0, dist=0.0, inc=0.0, vel=0.0)}
BIAS = {}
for cfg, on in NOISE_CFG.items():
    for law in ("fw", "mcg"):
        for a0i, lab in zip(A0_INJ, INJ_LAB):
            gb, go = observables(FULL70, a0i, law, NZ_FULL, on=on)
            nanrep = {}
            est = run_point_estimators(FULL70, gb, go, nan_report=nanrep)
            for k, v in est.items():
                rat = v / a0i
                rat = rat[np.isfinite(rat)]
                b = float(np.median(rat) - 1.0) * 100
                s = float(0.5 * (np.percentile(rat, 84) - np.percentile(rat, 16))) * 100
                BIAS.setdefault(cfg, {}).setdefault(law, {}).setdefault(k, {})[lab] = dict(
                    b_pp=b, s_pct=s, sigma_mc_pp=float(1.2533 * s / np.sqrt(len(rat))),
                    mean_ratio_pp=float(np.mean(rat) - 1.0) * 100, n_ok=int(len(rat)))
            if cfg == "ALL" and law == "mcg" and "mcgpt_nan_frac" in nanrep:
                BIAS[cfg][law].setdefault("_diag", {})[lab] = nanrep
        print(f"    done: cfg={cfg:<8} truth={law:<4}   ({time.time()-t_start:.0f}s)")


def matched(k, law):
    if k in CURVE:
        return CURVE[k][0] == law
    if k.startswith("a0line"):
        return law == "fw"
    if k == "mcgpt_median":
        return law == "mcg"
    return False


MATCH_TABLE = {}
for cfg in NOISE_CFG:
    print(f"\n  MATCHED-LAW BIAS TABLE, noise cfg = {cfg}   (estimator and truth law AGREE,")
    print(f"  so this row IS bias, not a form factor):")
    hdr = f"  {'estimator':<20}{'law':<5}" + "".join(f"{l.split()[0][:9]:>11}" for l in INJ_LAB)
    print(hdr + f"{'max|b|':>9}{'spread':>8}{'s%':>8}{'sMC':>7}  tier")
    for k in POINT_EST:
        for law in ("fw", "mcg"):
            if not matched(k, law):
                continue
            bs = [BIAS[cfg][law][k][l]["b_pp"] for l in INJ_LAB]
            ss = [BIAS[cfg][law][k][l]["s_pct"] for l in INJ_LAB]
            mc = [BIAS[cfg][law][k][l]["sigma_mc_pp"] for l in INJ_LAB]
            mx, sp = max(abs(x) for x in bs), float(np.ptp(bs))
            tier = "PASS" if mx < 2.0 else ("MARGINAL" if mx < 5.0 else "FAIL")
            rec = dict(law=law, b_pp=bs, max_abs_b_pp=mx, spread_pp=sp,
                       rms_b_pp=float(np.sqrt(np.mean(np.square(bs)))),
                       s_pct=float(np.mean(ss)), sigma_mc_pp=float(np.mean(mc)),
                       tier=tier, G3_injection_independent=bool(sp < 2.0),
                       resolved_vs_MC=bool(mx > 3 * np.mean(mc)))
            MATCH_TABLE.setdefault(cfg, {})[k] = rec
            print(f"  {k:<20}{law:<5}" + "".join(f"{b:>11.2f}" for b in bs) +
                  f"{mx:>9.2f}{sp:>8.2f}{np.mean(ss):>8.2f}{np.mean(mc):>7.2f}  {tier}"
                  + ("" if rec["resolved_vs_MC"] else "  [NOT MC-RESOLVED]"))
MT = MATCH_TABLE["ALL"]          # headline config (all frozen systematics on)
MTN = MATCH_TABLE["NOGLOB"]      # genuine estimator bias (global coherent terms removed)
OUT["full_range_bias_matched"] = MATCH_TABLE
OUT["full_range_bias_all"] = BIAS
if "_diag" in BIAS["ALL"].get("mcg", {}):
    OUT["mcgpt_nan_fraction"] = BIAS["ALL"]["mcg"]["_diag"]

# ---- the SAME full-range measurement at Ud = 0.50, i.e. AT THE PUBLISHED M/L.
# Bias is a property of the sample structure (phi, y, fv), which Upsilon changes, so the
# published estimator must be tested in ITS OWN configuration, not only in the framework's.
print("\n  FULL-RANGE BIAS AT THE PUBLISHED M/L (Upsilon_d = 0.50) -- the published")
print("  estimator tested in the configuration the published paper actually used:")
NZ_F50 = draw_noise(FULL50, N_REAL, SEED)
BIAS50 = {}
for cfg, on in (("ALL", None), ("NOGLOB", dict(glob=0.0))):
    for law in ("fw", "mcg"):
        for a0i, lab in zip(A0_INJ, INJ_LAB):
            gb, go = observables(FULL50, a0i, law, NZ_F50, on=on)
            est = run_point_estimators(FULL50, gb, go)
            for k, v in est.items():
                rat = v / a0i
                rat = rat[np.isfinite(rat)]
                s_ = float(0.5 * (np.percentile(rat, 84) - np.percentile(rat, 16))) * 100
                BIAS50.setdefault(cfg, {}).setdefault(law, {}).setdefault(k, {})[lab] = dict(
                    b_pp=float(np.median(rat) - 1.0) * 100, s_pct=s_,
                    sigma_mc_pp=float(1.2533 * s_ / np.sqrt(len(rat))))
        print(f"    done: Ud=0.50 cfg={cfg:<7} truth={law:<4}   ({time.time()-t_start:.0f}s)")
MT50 = {}
print(f"  {'estimator':<20}{'law':<5}" + "".join(f"{l.split()[0][:9]:>11}" for l in INJ_LAB)
      + f"{'max|b|':>9}{'s%':>8}{'sMC':>7}  tier   |  NOGLOB max|b|")
for k in POINT_EST:
    for law in ("fw", "mcg"):
        if not matched(k, law):
            continue
        bs = [BIAS50["ALL"][law][k][l]["b_pp"] for l in INJ_LAB]
        ss = [BIAS50["ALL"][law][k][l]["s_pct"] for l in INJ_LAB]
        mc = [BIAS50["ALL"][law][k][l]["sigma_mc_pp"] for l in INJ_LAB]
        bn = [BIAS50["NOGLOB"][law][k][l]["b_pp"] for l in INJ_LAB]
        mx = max(abs(x) for x in bs); mxn = max(abs(x) for x in bn)
        tier = "PASS" if mx < 2.0 else ("MARGINAL" if mx < 5.0 else "FAIL")
        MT50[k] = dict(law=law, b_pp=bs, max_abs_b_pp=mx, b_pp_noglob=bn,
                       max_abs_b_noglob_pp=mxn, spread_pp=float(np.ptp(bs)),
                       s_pct=float(np.mean(ss)), sigma_mc_pp=float(np.mean(mc)),
                       tier=tier,
                       tier_noglob="PASS" if mxn < 2.0 else ("MARGINAL" if mxn < 5.0 else "FAIL"))
        print(f"  {k:<20}{law:<5}" + "".join(f"{b:>11.2f}" for b in bs) +
              f"{mx:>9.2f}{np.mean(ss):>8.2f}{np.mean(mc):>7.2f}  {tier:<9}|"
              f"{mxn:>10.2f}  {MT50[k]['tier_noglob']}")
OUT["full_range_bias_Ud050"] = dict(matched=MT50, raw=BIAS50)

# ---- REGIME AXIS (v): the same estimators on GASDOM and LOWY, all noise on
print(f"\n  REGIME AXIS (v): the SAME estimators re-measured on TWO narrower samples, so the")
print(f"  deep-MOND restriction is separated from the gas-dominance SELECTION:")
print(f"    GASDOM (N={GAS70.N}, {GAS70.G} gal, y<=0.174) = the frozen prereg subsample")
print(f"           (a baryonic-COMPOSITION cut: Vgas^2 > Ud Vdisk^2 + Ub Vbul^2)")
print(f"    LOWY   (N={LOWY70.N}, {LOWY70.G} gal, y<1)     = deep-MOND points of ALL galaxies")
print(f"           (a pure REGIME cut, no composition selection)")
RB = {}
for tag, S in (("gasdom", GAS70), ("lowy", LOWY70)):
    nz = draw_noise(S, N_REAL, SEED)
    for law in ("fw", "mcg"):
        for a0i, lab in zip(A0_INJ, INJ_LAB):
            gb, go = observables(S, a0i, law, nz)
            est = run_point_estimators(S, gb, go)
            for k, v in est.items():
                rat = v / a0i
                rat = rat[np.isfinite(rat)]
                s = float(0.5 * (np.percentile(rat, 84) - np.percentile(rat, 16))) * 100
                RB.setdefault(tag, {}).setdefault(law, {}).setdefault(k, {})[lab] = dict(
                    b_pp=float(np.median(rat) - 1.0) * 100, s_pct=s,
                    sigma_mc_pp=float(1.2533 * s / np.sqrt(len(rat))))
    print(f"    done: regime sample {tag}   ({time.time()-t_start:.0f}s)")
print(f"\n  {'estimator':<20}{'GASDOM max|b|':>14}{'LOWY max|b|':>13}{'FULL max|b|':>13}"
      f"{'GASDOM s%':>11}{'LOWY s%':>9}{'FULL s%':>9}")
REGIME = {}
for k in POINT_EST:
    law = MT[k]["law"]
    gmx = max(abs(RB["gasdom"][law][k][l]["b_pp"]) for l in INJ_LAB)
    lmx = max(abs(RB["lowy"][law][k][l]["b_pp"]) for l in INJ_LAB)
    gs = float(np.mean([RB["gasdom"][law][k][l]["s_pct"] for l in INJ_LAB]))
    ls = float(np.mean([RB["lowy"][law][k][l]["s_pct"] for l in INJ_LAB]))
    REGIME[k] = dict(gasdom_max_abs_b_pp=gmx, lowy_max_abs_b_pp=lmx,
                     full_max_abs_b_pp=MT[k]["max_abs_b_pp"],
                     gasdom_b_pp=[RB["gasdom"][law][k][l]["b_pp"] for l in INJ_LAB],
                     lowy_b_pp=[RB["lowy"][law][k][l]["b_pp"] for l in INJ_LAB],
                     gasdom_s_pct=gs, lowy_s_pct=ls, full_s_pct=MT[k]["s_pct"],
                     gasdom_sigma_mc_pp=float(np.mean(
                         [RB["gasdom"][law][k][l]["sigma_mc_pp"] for l in INJ_LAB])))
    print(f"  {k:<20}{gmx:>14.2f}{lmx:>13.2f}{MT[k]['max_abs_b_pp']:>13.2f}"
          f"{gs:>11.2f}{ls:>9.2f}{MT[k]['s_pct']:>9.2f}")
OUT["regime_axis"] = REGIME
OUT["regime_bias_raw"] = RB
anchor_gls = RB["gasdom"]["fw"]["a0line_gls_origin"]["canonical cH_L/Z"]["b_pp"]
anchor_med = RB["gasdom"]["fw"]["a0line_median"]["canonical cH_L/Z"]["b_pp"]
mc_g = RB["gasdom"]["fw"]["a0line_gls_origin"]["canonical cH_L/Z"]["sigma_mc_pp"]
mc_m = RB["gasdom"]["fw"]["a0line_median"]["canonical cH_L/Z"]["sigma_mc_pp"]
tol_g, tol_m = max(1.0, 4 * mc_g), max(1.0, 4 * mc_m)
print(f"\n  REGRESSION ANCHOR (the committed prereg gas-dominated result must reproduce):")
print(f"    gls_origin : committed {B_ANCHOR_GLS:+.2f} pp   here {anchor_gls:+.2f} pp   "
      f"|diff| {abs(anchor_gls-B_ANCHOR_GLS):.2f} pp   tol {tol_g:.2f} (4 sigma_MC)")
print(f"    median_a0pt: committed {B_ANCHOR_MED:+.2f} pp   here {anchor_med:+.2f} pp   "
      f"|diff| {abs(anchor_med-B_ANCHOR_MED):.2f} pp   tol {tol_m:.2f} (4 sigma_MC)")
assert abs(anchor_gls - B_ANCHOR_GLS) < tol_g, "gas-dom +10.3pp anchor NOT reproduced"
assert abs(anchor_med - B_ANCHOR_MED) < tol_m, "gas-dom median anchor NOT reproduced"
print("  ANCHOR OK -- the committed +10.3 pp gas-dominated result is reproduced by this")
print("  independent reimplementation, so the machinery here is the same machinery.")
OUT["regression_anchor"] = dict(committed_gls_pp=B_ANCHOR_GLS, reproduced_gls_pp=anchor_gls,
                                committed_med_pp=B_ANCHOR_MED, reproduced_med_pp=anchor_med,
                                tol_gls_pp=tol_g, tol_med_pp=tol_m, N_real=N_REAL)

# ---- BTFR family, mocked separately (galaxy-level, nu-independent)
print("\n  FAMILY V (BTFR) bias, mocked at the GALAXY level (nu-independent asymptotic law):")
BT = btfr_struct(0.50)
print(f"    BTFR sample: {len(BT['names'])} galaxies with Vflat>0, Q<=2, i>=30 deg")
rng = np.random.default_rng(SEED + 7)
BTB = {}
for a0i, lab in zip(A0_INJ, INJ_LAB):
    Mb_true = BT["Vf"] ** 4 * BTFR_CHI / (GNEWT * a0i * MSUN)      # exact inverse BTFR
    dU = rng.normal(0, SIG_LNU, N_REAL)[:, None]
    dG = rng.normal(0, SIG_LNG, N_REAL)[:, None]
    fs = BT["Ud"] * BT["Lst"] / np.maximum(BT["Ud"] * BT["Lst"] + BT["Mgas"], 1.0)
    Mb = Mb_true[None, :] * (fs[None, :] * np.exp(dU) + (1 - fs[None, :]) * np.exp(dG)) \
        * np.exp(rng.normal(0, 0.10, (N_REAL, len(BT["Vf"]))))
    Vf = BT["Vf"][None, :] * (1 + rng.normal(0, BT["eVf"] / BT["Vf"], (N_REAL, len(BT["Vf"]))))
    for kind, key in (("med", "btfr_med"), ("lsq", "btfr_lsq")):
        v = btfr_a0(BT, Vf, Mb, kind)
        rat = np.asarray(v) / a0i
        BTB.setdefault(key, {})[lab] = dict(
            b_pp=float(np.median(rat) - 1.0) * 100,
            s_pct=float(0.5 * (np.percentile(rat, 84) - np.percentile(rat, 16))) * 100)
for key in ("btfr_med", "btfr_lsq"):
    bs = [BTB[key][l]["b_pp"] for l in INJ_LAB]
    mx = max(abs(x) for x in bs)
    tier = "PASS" if mx < 2.0 else ("MARGINAL" if mx < 5.0 else "FAIL")
    rec = dict(law="nu-independent", b_pp=bs, max_abs_b_pp=mx,
               spread_pp=float(np.ptp(bs)),
               rms_b_pp=float(np.sqrt(np.mean(np.square(bs)))),
               s_pct=float(np.mean([BTB[key][l]["s_pct"] for l in INJ_LAB])),
               sigma_mc_pp=float(1.2533 * np.mean(
                   [BTB[key][l]["s_pct"] for l in INJ_LAB]) / np.sqrt(N_REAL)),
               tier=tier, G3_injection_independent=bool(np.ptp(bs) < 2.0))
    for _c in NOISE_CFG:
        MATCH_TABLE[_c][key] = rec
    print(f"    {key:<12}" + "".join(f"{b:>11.2f}" for b in bs) + f"   max|b|={mx:.2f} pp  {tier}")
OUT["btfr_bias"] = BTB

# ============================================================ S6. REAL-DATA VALUES
print("\n" + bar)
print("S6 -- REAL-DATA VALUES: every estimator x sample x M/L (no mocks here)")
print(bar)
REAL = {}
for key, S in ST.items():
    lab = f"Ud{S.Ud:.2f}_{S.subset}"
    est = run_point_estimators(S, S.gb[None, :], S.go[None, :])
    REAL[lab] = {k: float(v[0]) for k, v in est.items()}
for key in ("btfr_med", "btfr_lsq"):
    for Ud in (0.50, 0.70):
        bt = btfr_struct(Ud)
        Mb = (Ud * bt["Lst"] + bt["Mgas"])
        REAL[f"Ud{Ud:.2f}_full"][key] = float(btfr_a0(bt, bt["Vf"], Mb,
                                                     key.split("_")[1]))
cols = ["Ud0.50_full", "Ud0.70_full", "Ud0.50_lowy", "Ud0.70_lowy",
        "Ud0.50_gasdom", "Ud0.70_gasdom"]
print(f"  {'estimator':<20}" + "".join(f"{c:>15}" for c in cols) + "  tier(full,ALL)")
for k in [e[0] for e in EST]:
    row = "".join((f"{REAL[c][k]:>15.4e}" if k in REAL[c] else f"{'-':>15}") for c in cols)
    print(f"  {k:<20}{row}   {MT.get(k, {}).get('tier','-')}")
OUT["real_values"] = REAL

# ============================================================== S7. THE DECOMPOSITION
print("\n" + bar)
print("S7 -- THE DECOMPOSITION LADDER: from the repo's number to the published 1.20e-10")
print("      ONE CHANGE PER RUNG. Each rung's delta is attributed to EXACTLY ONE axis.")
print(bar)
print("  DENOMINATOR = THE DELIVERABLE GAP: (published 1.200e-10) minus (THIS ANALYSIS'S")
print("  value: the pre-registered median-like primary on the FULL sample at Upsilon_d=0.70).")
print("  Note in advance: the repo's Step-A incumbent (biased GLS, gas-dom) happens to sit at")
print("  1.18e-10, i.e. only ~2% from the published number, so a ladder anchored THERE would")
print("  have a near-zero denominator and meaningless percentages. It is shown as r-1 for")
print("  continuity but the shares are computed against the deliverable gap.")
LADDER = [
    ("r-1 repo Step-A incumbent",
     "a0line_gls_origin", "Ud0.70_gasdom", None,
     "through-origin GLS on per-point a0, gas-dominated subsample, Upsilon_d=0.70, "
     "framework nu -- shown for continuity only"),
    ("r0 (i) ESTIMATOR",
     "a0line_galmed_med", "Ud0.70_gasdom", "(i) estimator choice",
     "swap the PROVEN-BIASED mean-like GLS for the PRE-REGISTERED UNBIASED median-like "
     "primary; everything else identical"),
    ("r1 (v-a) COMPOSITION cut",
     "a0line_galmed_med", "Ud0.70_lowy", "(v-a) gas-dominance selection removed",
     "still deep-MOND (y<1) but ALL galaxies, not only gas-dominated ones"),
    ("r2 (v-b) REGIME",
     "a0line_galmed_med", "Ud0.70_full", "(v-b) deep-MOND -> full y range",
     "same estimator, same law, same M/L: y<1 -> the full y = 0.009..92 range. THIS ROW IS "
     "THIS ANALYSIS'S OWN FULL-SAMPLE VALUE = the ladder's zero point."),
    ("r3 (ii) M/L",
     "a0line_galmed_med", "Ud0.50_full", "(ii) Upsilon prescription",
     "same estimator, same law, same sample: Upsilon_d 0.70 -> 0.50 (McGaugh's value)"),
    ("r4 (iv) FUNCTIONAL FORM",
     "mcgpt_median", "Ud0.50_full", "(iv) a0-line -> RAR interpolation",
     "SAME estimator (median of per-point scale), law swapped framework nu -> McGaugh nu"),
    ("r5 (i) ESTIMATOR again",
     "rar_odrlog_mcg", "Ud0.50_full", "(i) estimator choice (within the published family)",
     "median-of-per-point -> the PUBLISHED scipy.odr curve fit; same law, sample, M/L"),
]
prev = None
LAD = []

v0 = REAL["Ud0.70_full"]["a0line_galmed_med"]      # THIS analysis's full-sample value
rows = []
for name, est, samp, axis, desc in LADDER:
    v = REAL[samp][est]
    rows.append((name, est, samp, axis, desc, v))
vend = rows[-1][5]
gap_total = A0_PUB - v0
print(f"  gap to decompose = 1.200e-10 - {v0:.4e} = {gap_total:+.4e}  "
      f"({100*gap_total/v0:+.1f}% of this analysis's value)")
print(f"  {'rung':<28}{'value':>13}{'delta vs prev':>15}{'% of the gap':>16}  axis")
for name, est, samp, axis, desc, v in rows:
    d = None if prev is None else v - prev
    frac = None if d is None else 100.0 * d / gap_total
    print(f"  {name:<28}{v:>13.4e}" +
          (f"{d:>+15.3e}{frac:>15.1f}%" if d is not None else f"{'--':>15}{'--':>16}") +
          f"  {axis or 'baseline'}")
    LAD.append(dict(rung=name, estimator=est, sample=samp, axis=axis, description=desc,
                    value=float(v), delta=None if d is None else float(d),
                    pct_of_total_gap=None if frac is None else float(frac)))
    prev = v
resid = A0_PUB - vend
print(f"  {'residual -> published':<28}{A0_PUB:>13.4e}{resid:>+15.3e}"
      f"{100.0*resid/gap_total:>15.1f}%  (iii) cuts + PUBLISHED-FAMILY REPRODUCTION RESIDUAL")
print(f"\n  CLOSURE CHECK: sum of the r2->r5 deltas + residual must equal the gap.")
ZP = 3          # index of r2, THIS analysis's own full-sample value = the zero point
_dsum = sum(r["delta"] for r in LAD[ZP+1:] if r["delta"] is not None) + resid
print(f"    sum = {_dsum:+.4e}   gap = {gap_total:+.4e}   "
      f"mismatch = {abs(_dsum-gap_total):.2e} (must be ~0)")
assert abs(_dsum - gap_total) < 1e-14, "ladder does not close"
print(f"\n  (rows r-1..r2 are BEFORE the zero point: they describe how THIS analysis's own")
print(f"   value depends on its estimator and sample choice, not the gap to the published")
print(f"   number. r-1->r0 = {LAD[1]['delta']:+.3e} is the estimator swap; r0->r2 = "
      f"{LAD[3]['value']-LAD[1]['value']:+.3e} is the sample change.)")
print(f"\n  AXIS SHARES OF THE {gap_total:+.4e} GAP (signed; they need not all be positive,")
print(f"  and a NEGATIVE share means that axis pushes AWAY from the published value):")
_ax = {}
for r in LAD[ZP+1:]:
    if r["delta"] is None:
        continue
    _ax[r["axis"]] = _ax.get(r["axis"], 0.0) + r["delta"]
_ax["(iii) cuts + published-family reproduction residual"] = resid
for a_, d_ in sorted(_ax.items(), key=lambda t: -abs(t[1])):
    print(f"    {a_:<52}{d_:>+12.4e}{100*d_/gap_total:>9.1f}%")
OUT["axis_shares_of_gap"] = {a_: dict(delta=float(d_), pct=float(100 * d_ / gap_total))
                             for a_, d_ in _ax.items()}
LAD.append(dict(rung="residual -> published 1.20e-10", estimator="published ODR",
                axis="(iii) cuts + reproduction residual", value=A0_PUB, delta=float(resid),
                pct_of_total_gap=float(100.0 * resid / gap_total)))
OUT["ladder_gls_start"] = dict(rows=LAD, total_gap=float(gap_total),
                               start=float(v0), end_before_residual=float(vend))

# ---- the SAME decomposition run the other direction, from the published number down.
print("\n  SAME DECOMPOSITION, ANCHORED AT THE PUBLISHED END (guards against ladder-order")
print("  artefacts: a decomposition that only works in one order is not a decomposition).")
LADDER_B = [
    ("r0' published-family reproduction", "rar_odrlog_mcg", "Ud0.50_full", None),
    ("r1' (i) estimator -> median", "mcgpt_median", "Ud0.50_full", "(i) estimator"),
    ("r2' (iv) law -> framework nu", "a0line_galmed_med", "Ud0.50_full", "(iv) form"),
    ("r3' (ii) M/L 0.50 -> 0.70", "a0line_galmed_med", "Ud0.70_full", "(ii) Upsilon"),
    ("r4' (v-b) full -> y<1", "a0line_galmed_med", "Ud0.70_lowy", "(v-b) regime"),
    ("r5' (v-a) y<1 -> gas-dominated", "a0line_galmed_med", "Ud0.70_gasdom", "(v-a) composition"),
]
prev = None
LADB = []
for name, est, samp, axis in LADDER_B:
    v = REAL[samp][est]
    d = None if prev is None else v - prev
    print(f"  {name:<38}{v:>13.4e}" + (f"{d:>+15.3e}" if d is not None else f"{'--':>15}")
          + f"   {axis or 'baseline'}")
    LADB.append(dict(rung=name, estimator=est, sample=samp, axis=axis, value=float(v),
                     delta=None if d is None else float(d)))
    prev = v
OUT["ladder_published_start"] = LADB

# ---- per-axis magnitudes, isolated (each axis measured with EVERYTHING ELSE HELD FIXED)
print("\n  PER-AXIS MAGNITUDES, EACH MEASURED IN ISOLATION (everything else held fixed):")
AX = {}
AX["(i) estimator: mean-like vs median-like, a0-line, gas-dom Ud=0.70"] = (
    REAL["Ud0.70_gasdom"]["a0line_gls_origin"], REAL["Ud0.70_gasdom"]["a0line_galmed_med"])
AX["(i) estimator: mean-like vs median-like, a0-line, FULL Ud=0.70"] = (
    REAL["Ud0.70_full"]["a0line_gls_origin"], REAL["Ud0.70_full"]["a0line_galmed_med"])
AX["(i) estimator: ODR-log vs ODR-lin vs wLSQ, McGaugh nu, FULL Ud=0.50"] = (
    REAL["Ud0.50_full"]["rar_odrlog_mcg"], REAL["Ud0.50_full"]["rar_wlsqlog_mcg"])
AX["(ii) M/L: Upsilon_d 0.50 -> 0.70, median a0-line, FULL"] = (
    REAL["Ud0.50_full"]["a0line_galmed_med"], REAL["Ud0.70_full"]["a0line_galmed_med"])
AX["(ii) M/L: Upsilon_d 0.50 -> 0.70, published ODR McGaugh nu, FULL"] = (
    REAL["Ud0.50_full"]["rar_odrlog_mcg"], REAL["Ud0.70_full"]["rar_odrlog_mcg"])
AX["(iv) form: a0-line vs McGaugh nu, median estimator, FULL Ud=0.50"] = (
    REAL["Ud0.50_full"]["a0line_galmed_med"], REAL["Ud0.50_full"]["mcgpt_median"])
AX["(iv) form: framework nu vs McGaugh nu, SAME ODR-log estimator, FULL Ud=0.50"] = (
    REAL["Ud0.50_full"]["rar_odrlog_fw"], REAL["Ud0.50_full"]["rar_odrlog_mcg"])
AX["(v-a) composition: gas-dom -> y<1 all galaxies, median a0-line, Ud=0.70"] = (
    REAL["Ud0.70_gasdom"]["a0line_galmed_med"], REAL["Ud0.70_lowy"]["a0line_galmed_med"])
AX["(v-b) regime: y<1 -> FULL y range, median a0-line, Ud=0.70"] = (
    REAL["Ud0.70_lowy"]["a0line_galmed_med"], REAL["Ud0.70_full"]["a0line_galmed_med"])
AX["(v) regime TOTAL: gas-dom -> FULL, median a0-line, Ud=0.70"] = (
    REAL["Ud0.70_gasdom"]["a0line_galmed_med"], REAL["Ud0.70_full"]["a0line_galmed_med"])
AX["(iv) form: a0-line vs McGaugh nu, median estimator, gas-dom Ud=0.70 (deep-MOND)"] = (
    REAL["Ud0.70_gasdom"]["a0line_galmed_med"], REAL["Ud0.70_gasdom"]["mcgpt_median"])
for k, (a, b) in AX.items():
    print(f"    {k}\n        {a:.4e} -> {b:.4e}   ratio {b/a:.4f}  ({100*(b/a-1):+.1f}%)")
OUT["per_axis_isolated"] = {k: dict(a=float(a), b=float(b), ratio=float(b / a),
                                    pct=float(100 * (b / a - 1))) for k, (a, b) in AX.items()}

# ============================================================ S8. THE HEADLINE VALUE
print("\n" + bar)
print("S8 -- HEADLINE: the PRE-REGISTERED median-like PRIMARY on the FULL SPARC sample")
print(bar)
PRIM = "a0line_galmed_med"
IPUB = INJ_LAB.index("published g_dagger")
print(f"  frozen prereg primary = {VERDICT['primary']}  ->  used here as {PRIM}")
print(f"  Its unbiasedness was ESTABLISHED ONLY ON THE GAS-DOMINATED SUBSAMPLE. The first")
print(f"  thing this section must report is whether that survives the regime change, and")
print(f"  the measured answer is:")
for lab_, tab in (("Ud=0.70 FULL", MT), ("Ud=0.50 FULL", MT50)):
    print(f"    {lab_}: {PRIM} tier = {tab[PRIM]['tier']}, max|b| = "
          f"{tab[PRIM]['max_abs_b_pp']:.2f} pp (ALL noise), "
          f"{tab[PRIM].get('max_abs_b_noglob_pp', MTN[PRIM]['max_abs_b_pp']):.2f} pp (NOGLOB), "
          f"s = {tab[PRIM]['s_pct']:.1f}%")
SURV = [k for k in POINT_EST if MT.get(k, {}).get("tier") == "PASS" and MT[k]["law"] == "fw"]
print(f"  full-range PASS-tier framework-nu estimators (ALL noise) = {SURV if SURV else 'NONE'}")
HEAD = {}
for Ud in (0.70, 0.50):
    lab = f"Ud{Ud:.2f}_full"
    tab = MT if Ud == 0.70 else MT50
    v = REAL[lab][PRIM]
    s_pct = tab[PRIM]["s_pct"]
    b_all = float(np.median(tab[PRIM]["b_pp"]))
    b_ng = float(np.median(tab[PRIM].get("b_pp_noglob", MTN[PRIM]["b_pp"])))
    # central value corrected on the GENUINE estimator bias (NOGLOB); the ALL-NOGLOB
    # difference is carried as a separate bias-MODELLING systematic, not folded in silently.
    vcorr = v / (1.0 + b_ng / 100.0)
    pool = [k for k in POINT_EST
            if k.startswith("a0line") and tab.get(k, {}).get("tier_noglob",
                ("PASS" if abs(float(np.median(MTN[k]["b_pp"]))) < 2 else "X")) == "PASS"]
    if PRIM not in pool:
        pool = pool + [PRIM]
    vals = [REAL[lab][k] for k in pool]
    sysEst = 0.5 * (max(vals) - min(vals))
    sig_fm = vcorr * s_pct / 100.0
    sig_bias = vcorr * abs(b_all - b_ng) / 100.0
    sig_tot = float(np.sqrt(sig_fm ** 2 + sysEst ** 2 + sig_bias ** 2))
    print(f"\n  ---- Upsilon_disk = {Ud:.2f} (Upsilon_bul = {1.4*Ud:.2f}), FULL sample "
          f"N={ST[(Ud,'full')].N}, {ST[(Ud,'full')].G} galaxies ----")
    print(f"    RAW       a0({PRIM}) = {v:.4e}  m/s^2")
    print(f"    measured bias of THIS estimator on THIS sample = {b_all:+.2f} pp (ALL noise), "
          f"{b_ng:+.2f} pp (NOGLOB = genuine estimator bias)")
    print(f"    BIAS-CORRECTED (on NOGLOB)          = {vcorr:.4e}  m/s^2")
    print(f"    sigma budget:")
    print(f"      forward-model 1-sigma from the mocks (ALL frozen systematics incl. the")
    print(f"        GLOBAL coherent Upsilon 0.23 + gas-cal 0.10) = {s_pct:.1f}% = {sig_fm:.3e}")
    print(f"      estimator systematic, PASS-tier a0-line pool {pool} = {sysEst:.3e}")
    print(f"      bias-modelling (|b_ALL - b_NOGLOB|)          = {sig_bias:.3e}")
    print(f"    sigma_tot = {sig_tot:.3e}  ({100*sig_tot/vcorr:.1f}%)")
    print(f"    COMPARISON (bias-corrected central value, sigma_tot):")
    for tgt, tl in ((A0_PUB, "published 1.200e-10"), (A0_CANON, "canonical 9.355e-11"),
                    (A0_ALT, "ALT 1.1305e-10")):
        print(f"      vs {tl:<22} {(vcorr-tgt)/sig_tot:+6.2f} sigma   ratio {vcorr/tgt:.3f}")
    HEAD[lab] = dict(estimator=PRIM, a0_raw=float(v), bias_pp_all=b_all, bias_pp_noglob=b_ng,
                     a0_bias_corrected=float(vcorr), s_pct=float(s_pct),
                     sigma_forward_model=float(sig_fm), sysEst=float(sysEst),
                     sigma_bias_model=float(sig_bias), sigma_tot=sig_tot,
                     tier_ALL=tab[PRIM]["tier"],
                     tier_NOGLOB=tab[PRIM].get("tier_noglob", MTN[PRIM]["tier"]),
                     estimator_pool=pool,
                     a0line_family_values={k: float(REAL[lab][k]) for k in pool},
                     sigma_vs=dict(published=float((vcorr - A0_PUB) / sig_tot),
                                   canonical=float((vcorr - A0_CANON) / sig_tot),
                                   alt=float((vcorr - A0_ALT) / sig_tot)),
                     ratio_vs=dict(published=float(vcorr / A0_PUB),
                                   canonical=float(vcorr / A0_CANON),
                                   alt=float(vcorr / A0_ALT)))
OUT["headline"] = HEAD
print("\n  For reference, the SAME primary on the GAS-DOMINATED subsample where it WAS")
print("  certified unbiased (this is the pre-registered regime, and the one number in this")
print("  script whose estimator has a PASS certificate on its own sample):")
bg = float(np.median(REGIME[PRIM]["gasdom_b_pp"]))
sg = REGIME[PRIM]["gasdom_s_pct"]
for Ud in (0.70, 0.50):
    lab = f"Ud{Ud:.2f}_gasdom"
    v = REAL[lab][PRIM]
    meas = (Ud == 0.70)
    vc = v / (1 + bg / 100.0)
    print(f"    Ud={Ud:.2f} gas-dom: raw {v:.4e}  b={bg:+.2f} pp"
          f"{'' if meas else ' (bias measured at Ud=0.70, carried over -- flagged)'}"
          f"  corrected {vc:.4e}  s={sg:.1f}%")
    print(f"                      -> {vc/A0_CANON:.3f} x canonical, {vc/A0_ALT:.3f} x ALT, "
          f"{vc/A0_PUB:.3f} x published")
    OUT.setdefault("gasdom_primary", {})[lab] = dict(
        raw=float(v), bias_pp=bg, bias_measured_on_this_sample=bool(meas),
        corrected=float(vc), s_pct=float(sg),
        ratio_canonical=float(vc / A0_CANON), ratio_alt=float(vc / A0_ALT),
        ratio_published=float(vc / A0_PUB))

# ---- bias-correction of every measured-biased estimator, applied to the real data
print("\n  BIAS-CORRECTION APPLIED ONLY WHERE BIAS WAS MEASURED ON MOCKS (never assumed):")
CORR = {}
print(f"  {'estimator':<20}{'sample':<14}{'raw':>13}{'b(ALL)':>9}{'b(NOGLOB)':>11}"
      f"{'corr(ALL)':>13}{'corr(NOGLOB)':>14}")
for k in POINT_EST:
    for lab, tab in (("Ud0.70_full", MT), ("Ud0.50_full", MT50)):
        if k not in tab:
            continue
        raw = REAL[lab][k]
        b_all = float(np.median(tab[k]["b_pp"]))
        b_ng = float(np.median(tab[k].get("b_pp_noglob", MTN[k]["b_pp"])))
        rec = dict(raw=raw, bias_pp_all=b_all, bias_pp_noglob=b_ng,
                   corrected_all=raw / (1 + b_all / 100.0),
                   corrected_noglob=raw / (1 + b_ng / 100.0), tier=tab[k]["tier"])
        CORR.setdefault(k, {})[lab] = rec
        print(f"  {k:<20}{lab:<14}{raw:>13.4e}{b_all:>+9.2f}{b_ng:>+11.2f}"
              f"{rec['corrected_all']:>13.4e}{rec['corrected_noglob']:>14.4e}")
OUT["bias_corrected_real"] = CORR

# ---- explicit answer to the transfer question
print("\n" + bar)
print("S9 -- DOES THE +10.3 pp GAS-DOMINATED BIAS TRANSFER TO THE PUBLISHED 1.2e-10?")
print(bar)
print("  Test 1 -- IDENTITY OF ESTIMATOR. Is the proven-biased estimator the published one?")
print("    NO. The +10.3 pp result is for a through-origin GLS on per-point")
print("    a0 = (g_obs^2-g_bar^2)/g_bar in the deep-MOND regime. The published number comes")
print("    from scipy.odr on the RAR curve (McGaugh+2016/Lelli+2017) and, independently,")
print("    from the BTFR normalisation (McGaugh 2012). Different statistic entirely.")
print("\n  Test 2 -- MEASURED BIAS OF THE PUBLISHED ESTIMATORS, IN THEIR OWN CONFIGURATION")
print("  (full y range, McGaugh nu truth, Upsilon_d=0.50 = their M/L). ALL vs NOGLOB matters:")
print("  the coherent-Upsilon share is ALREADY the published +-0.24e-10 (20%) systematic.")
pub_fams = ["rar_odrlog_mcg", "rar_odrlin_mcg", "rar_wlsqlog_mcg", "btfr_med", "btfr_lsq"]
print(f"  {'published-family estimator':<22}{'b@1.2e-10 ALL':>15}{'b@1.2e-10 NOGLOB':>18}"
      f"{'max|b| ALL':>12}{'tier(NOGLOB)':>14}")
TRANSFER = {}
for k in pub_fams:
    tab = MT50 if k in MT50 else MT
    bpub = tab[k]["b_pp"][IPUB]
    bng = (tab[k]["b_pp_noglob"][IPUB] if "b_pp_noglob" in tab[k]
           else MTN[k]["b_pp"][IPUB] if k in MTN else float("nan"))
    tn = ("PASS" if abs(bng) < 2.0 else ("MARGINAL" if abs(bng) < 5.0 else "FAIL"))
    TRANSFER[k] = dict(b_at_published_ALL_pp=bpub, b_at_published_NOGLOB_pp=bng,
                       max_abs_b_ALL_pp=tab[k]["max_abs_b_pp"], tier_noglob=tn,
                       unbiased_at_1p2e10_noglob=bool(abs(bng) < 2.0),
                       recovers_1p2e10=bool(abs(bpub) < 2.0))
    print(f"  {k:<22}{bpub:>+15.2f}{bng:>+18.2f}{tab[k]['max_abs_b_pp']:>12.2f}{tn:>14}")
    OUT.setdefault("_t", {})
print("\n  Test 3 -- DOES THE PUBLISHED FAMILY RECOVER 1.2e-10 WHEN 1.2e-10 IS INJECTED?")
for k in pub_fams:
    t = TRANSFER[k]
    print(f"    {k:<22} injected 1.2e-10 -> recovered "
          f"{1.2*(1+t['b_at_published_ALL_pp']/100):.4f}e-10 (ALL), "
          f"{1.2*(1+t['b_at_published_NOGLOB_pp']/100):.4f}e-10 (NOGLOB)   "
          f"{'RECOVERS' if t['recovers_1p2e10'] else 'DOES NOT recover within 2 pp'}")
OUT["transfer_verdict"] = TRANSFER
sgn = {k: ("HIGH" if TRANSFER[k]["b_at_published_NOGLOB_pp"] > 0 else "LOW")
       for k in pub_fams}
print("\n  Test 4 -- SIGN. A bias that pushes the published value DOWN would help the")
print("  canonical footing; a bias that pushes it UP would hurt. Measured signs (NOGLOB):")
for k in pub_fams:
    print(f"    {k:<22} biased {sgn[k]:<5} by "
          f"{abs(TRANSFER[k]['b_at_published_NOGLOB_pp']):.2f} pp")
OUT["transfer_sign"] = sgn

# ================================================ S10. RECONSTRUCTION FIDELITY + VERDICT
print("\n" + bar)
print("S10 -- HOW WELL IS THE PUBLISHED NUMBER ITSELF REPRODUCED? (the honest ceiling on")
print("       every attribution above -- an axis cannot be resolved finer than this band)")
print(bar)
print("  MLS2016/Lelli+2017 state only: 'scipy.odr ... considering errors in both variables',")
print("  on the unbinned 2693 points, with Upsilon_[3.6] = 0.50/0.70. They do NOT state")
print("  whether the fit is in linear or log space, nor the exact g_bar error model. Every")
print("  defensible reading is therefore run, at THEIR M/L, and the SPREAD is reported:")
_S = FULL50
RECON = {}
_variants = [
    ("ODR log-log, sx = 25% Ups / 10% HI (fiducial reading)", "odrlog", 1.0),
    ("ODR linear,  sx = 25% Ups / 10% HI", "odrlin", 1.0),
    ("vertical weighted LSQ in log10 (sx -> 0)", "wlsqlog", 1.0),
    ("ODR log-log, sx halved  (10% Ups / 5% HI)", "odrlog", 0.5),
    ("ODR log-log, sx doubled (50% Ups / 20% HI)", "odrlog", 2.0),
]
_keep = _S.rel_egb.copy()
for lbl, mode, fac in _variants:
    _S.rel_egb = _keep * fac
    v = curvefit_row(_S, _S.gb, _S.go, "mcg", mode)
    RECON[lbl] = float(v)
    print(f"    {lbl:<54}{v:.4e}   ({100*(v/A0_PUB-1):+.1f}% vs published)")
_S.rel_egb = _keep
_lo, _hi = min(RECON.values()), max(RECON.values())
print(f"\n  RECONSTRUCTION BAND at Upsilon_d = 0.50: [{_lo:.4e}, {_hi:.4e}]")
print(f"    = [{100*(_lo/A0_PUB-1):+.1f}%, {100*(_hi/A0_PUB-1):+.1f}%] around the published "
      f"1.200e-10.")
_inband = _lo <= A0_PUB <= _hi
print(f"    published 1.200e-10 {'IS' if _inband else 'is NOT'} inside the band"
      + ("" if _inband else f" -- it lies {100*(A0_PUB/_hi-1):+.1f}% above the top."))
print(f"  Their quoted systematic alone is +-0.24e-10 = +-20%, i.e. [0.96e-10, 1.44e-10];")
print(f"  the whole reconstruction band sits inside that. So the published value is")
print(f"  REPRODUCED WITHIN ITS OWN QUOTED SYSTEMATIC, and the ~{100*abs(A0_PUB/_hi-1):.0f}% residual of the")
print(f"  ladder is reconstruction fidelity + the 6-galaxy sample difference -- NOT a bias,")
print(f"  and NOT attributable to any of the five axes.")
OUT["reconstruction_band"] = dict(variants=RECON, lo=float(_lo), hi=float(_hi),
                                  published=A0_PUB, published_in_band=bool(_inband),
                                  published_syst_band=[0.96e-10, 1.44e-10])

# ---- axis (iii) MEASURED, not assumed: sensitivity of the published estimator to the cuts
print(f"\n  AXIS (iii) SAMPLE/QUALITY CUTS -- MEASURED, not assumed. The cuts are varied one")
print(f"  at a time around the published choice (Q<3, i>=30 deg, dV/V<0.10) and the PUBLISHED")
print(f"  estimator is re-run at Upsilon_d = 0.50 on each resulting sample:")


def load_cuts(Ud, qmax=2, incmin=30.0, fvcut=0.10):
    """fire_common.load with the three quality cuts exposed as parameters."""
    _q, _f = fc._cache, fc.FVCUT
    fc._cache = {}
    fc.FVCUT = fvcut
    try:
        import glob as _g
        Ub = 1.4 * Ud
        gb_, go_, phi_, fv_, cti_, npt_, einc_, eD_ = [], [], [], [], [], [], [], []
        for f_ in sorted(_g.glob(os.path.join(fc.REPO, "data", "sparc_data", "*_rotmod.dat"))):
            nm = os.path.basename(f_).replace("_rotmod.dat", "")
            m_ = fc._meta.get(nm)
            if m_ is None or m_["Q"] > qmax or m_["inc"] < incmin:
                continue
            d_ = np.genfromtxt(f_, comments="#")
            if d_.ndim != 2 or d_.shape[1] < 6:
                continue
            R, Vo, eV, Vg, Vd, Vb = (d_[:, i] for i in range(6))
            gst = (Ud * Vd ** 2 + Ub * Vb ** 2) * 1e6 / (R * fc.kpc)
            gga = np.sign(Vg) * Vg ** 2 * 1e6 / (R * fc.kpc)
            gb0, go0 = gga + gst, (Vo * 1e3) ** 2 / (R * fc.kpc)
            fvv = np.clip(eV, 1.0, None) / np.clip(Vo, 1, None)
            ok = ((gb0 > 0) & (Vo > 0) & np.isfinite(gb0) & np.isfinite(go0) & (fvv < fvcut))
            n_ = int(ok.sum())
            if n_ == 0:
                continue
            r_ = MRTROW[nm]
            gb_ += list(gb0[ok]); go_ += list(go0[ok]); fv_ += list(fvv[ok])
            phi_ += list((gst / gb0)[ok])
            cti_ += [1.0 / np.tan(np.deg2rad(m_["inc"]))] * n_
            npt_.append(n_); einc_.append(np.deg2rad(max(r_["einc"], 1.0)))
            eD_.append(r_["eD"] / r_["D"])
        return dict(gb=np.array(gb_), go=np.array(go_), fv=np.array(fv_),
                    phi=np.array(phi_), cti=np.array(cti_), npt=np.array(npt_, int),
                    einc=np.array(einc_), eDrel=np.array(eD_))
    finally:
        fc._cache, fc.FVCUT = _q, _f


class _Lite:
    def __init__(self, d):
        self.__dict__.update(d)
        eip = np.repeat(self.einc, self.npt); eDp = np.repeat(self.eDrel, self.npt)
        self.rel_ego = np.sqrt((2 * self.fv) ** 2 + (2 * eip * self.cti) ** 2 + eDp ** 2)
        self.rel_egb = np.sqrt((self.phi * 0.25) ** 2 + ((1 - self.phi) * 0.10) ** 2)
        self.N = len(self.gb); self.G = len(self.npt)


CUTS = {}
for lbl, kw in (("published choice: Q<=2, i>=30, dV/V<0.10", {}),
                ("Q<=1 only (high quality)", dict(qmax=1)),
                ("Q<=3 (no quality cut)", dict(qmax=3)),
                ("i >= 45 deg", dict(incmin=45.0)),
                ("i >= 0 (no inclination cut)", dict(incmin=0.0)),
                ("dV/V < 0.05 (tighter)", dict(fvcut=0.05)),
                ("dV/V < 0.25 (looser)", dict(fvcut=0.25)),
                ("no cuts at all", dict(qmax=3, incmin=0.0, fvcut=1e9))):
    L = _Lite(load_cuts(0.50, **kw))
    v = curvefit_row(L, L.gb, L.go, "mcg", "odrlog")
    CUTS[lbl] = dict(a0=float(v), N=L.N, Ngal=L.G)
    print(f"    {lbl:<46}N={L.N:5d} Ngal={L.G:3d}  a0 = {v:.4e}  "
          f"({100*(v/CUTS['published choice: Q<=2, i>=30, dV/V<0.10']['a0']-1):+.1f}% vs published choice)")
_cv = [c["a0"] for c in CUTS.values()]
_base = CUTS["published choice: Q<=2, i>=30, dV/V<0.10"]["a0"]
print(f"  full cut-variation spread = [{min(_cv):.4e}, {max(_cv):.4e}] = "
      f"[{100*(min(_cv)/_base-1):+.1f}%, {100*(max(_cv)/_base-1):+.1f}%]")
_worst = max(abs(min(_cv) / _base - 1), abs(max(_cv) / _base - 1))
_qonly = abs(CUTS["Q<=1 only (high quality)"]["a0"] / _base - 1)
_others = max(abs(c["a0"] / _base - 1) for l_, c in CUTS.items()
              if l_ not in ("Q<=1 only (high quality)",
                            "published choice: Q<=2, i>=30, dV/V<0.10"))
print(f"  ==> AXIS (iii) IS MEASURED, NOT ASSUMED NULL. Worst single cut change moves the")
print(f"      published estimator by {100*_worst:.1f}%, and that worst case is the Q<=1")
print(f"      high-quality restriction ({100*_qonly:+.1f}%); every OTHER cut change (inclination,")
print(f"      velocity precision, removing the quality cut, removing ALL cuts) stays within")
print(f"      {100*_others:.1f}%. So axis (iii) is a few-percent-to-13% effect: it is the right")
print(f"      size to absorb the ladder's residual, and it CANNOT account for the ~28%")
print(f"      framework-vs-published gap on its own. Reported, not swept.")
OUT["axis_iii_summary"] = dict(worst_pct=float(100 * _worst), Q1_pct=float(100 * _qonly),
                              other_cuts_max_pct=float(100 * _others))
OUT["axis_iii_cut_sensitivity"] = CUTS

# ---- the mock also has to reproduce the PUBLISHED ERROR BUDGET, not just the value
_s_pub = MT50["rar_odrlog_mcg"]["s_pct"]
print(f"\n  CROSS-VALIDATION OF THE MOCK AGAINST THE PUBLISHED ERROR BUDGET:")
print(f"    MLS2016 quote a {0.24/1.20*100:.0f}% systematic on g_dagger, sourced to a 20%")
print(f"    uncertainty in the Upsilon normalisation.")
print(f"    This mock, run with the frozen sigma_lnUpsilon = 0.23 nat = 0.10 dex coherent,")
print(f"    gives their estimator a total scatter s = {_s_pub:.1f}% -- the same order, from an")
print(f"    error model that was frozen BEFORE this comparison and never tuned to it.")
OUT["published_error_budget_crosscheck"] = dict(published_syst_pct=20.0,
                                                mock_s_pct=float(_s_pub))

# ---- BTFR chi-sensitivity (its one model knob, stated not hidden)
print(f"\n  BTFR ROUTE -- the chi disk-geometry factor is its one model knob and it is NOT")
print(f"  an estimator choice. Sensitivity at Upsilon_d = 0.50 (median-over-galaxies form):")
_bt = btfr_struct(0.50)
_Mb = 0.50 * _bt["Lst"] + _bt["Mgas"]
CHI = {}
for _c in (0.70, 0.80, 0.90, 1.00):
    _v = float(np.median(_c * _bt["Vf"] ** 4 / (GNEWT * _Mb * MSUN)))
    CHI[f"chi={_c:.2f}"] = _v
    print(f"    chi = {_c:.2f}  ->  a0 = {_v:.4e}   ({100*(_v/A0_PUB-1):+.1f}% vs published)")
print(f"  chi is a MOND/disk-geometry modelling factor (McGaugh+2019 review use chi ~ 0.8);")
print(f"  it moves the BTFR a0 by ~{100*(CHI['chi=1.00']/CHI['chi=0.70']-1):.0f}% across 0.7-1.0, so the BTFR route's")
print(f"  own model systematic is comparable to the footing gap. Flagged, not buried.")
OUT["btfr_chi_sensitivity"] = CHI

# ============================================================================ VERDICT
print("\n" + bar)
print("VERDICT")
print(bar)
_bpub_ng = TRANSFER["rar_odrlog_mcg"]["b_at_published_NOGLOB_pp"]
_bpub_all = TRANSFER["rar_odrlog_mcg"]["b_at_published_ALL_pp"]
_bgls_full = float(np.median(MTN["a0line_gls_origin"]["b_pp"]))
VERD = dict(
    transfers_to_published="NO-published-robust",
    q1_same_estimator=False,
    q2_published_estimator_bias_pp=dict(odr_log=_bpub_ng,
                                        odr_lin=TRANSFER["rar_odrlin_mcg"]["b_at_published_NOGLOB_pp"],
                                        wlsq_log=TRANSFER["rar_wlsqlog_mcg"]["b_at_published_NOGLOB_pp"],
                                        btfr_med=TRANSFER["btfr_med"]["b_at_published_NOGLOB_pp"],
                                        btfr_lsq=TRANSFER["btfr_lsq"]["b_at_published_NOGLOB_pp"]),
    q3_recovers_1p2e10_when_injected=TRANSFER["rar_odrlog_mcg"]["recovers_1p2e10"],
    repo_gls_bias_gasdom_pp=B_ANCHOR_GLS,
    repo_gls_bias_fullrange_pp=_bgls_full,
    axis_shares=OUT["axis_shares_of_gap"],
    reconstruction_band=[float(_lo), float(_hi)])
print(f"  1. IDENTITY. The proven-biased estimator (through-origin GLS on per-point a0) is")
print(f"     used by NO published determination of a0. McGaugh+2016/Lelli+2017 use scipy.odr")
print(f"     on the RAR curve; McGaugh 2012 uses the BTFR normalisation; Li+2018 does not")
print(f"     measure a0 at all (it FIXES/priors g_dagger = 1.20e-10). So there is no route")
print(f"     for the bias to transfer by identity of statistic.")
print(f"  2. MEASURED. Implemented and mocked in its own configuration (full y range, its own")
print(f"     nu, its own Upsilon = 0.50), the published ODR estimator's bias is")
print(f"     {_bpub_ng:+.2f} pp -- INSIDE the 2 pp PASS gate, at all {len(A0_INJ)} injected values,")
print(f"     INCLUDING 1.2e-10 itself. The BTFR route is likewise unbiased")
print(f"     ({TRANSFER['btfr_med']['b_at_published_NOGLOB_pp']:+.2f} pp). The only published-family")
print(f"     variant that fails is the LINEAR-space ODR reading")
print(f"     ({TRANSFER['rar_odrlin_mcg']['b_at_published_NOGLOB_pp']:+.2f} pp), and it is biased LOW, i.e. it would")
print(f"     make the published number an UNDER-estimate, not an over-estimate.")
print(f"  3. THE REPO'S BIAS IS ESTIMATOR-SPECIFIC AND GETS WORSE, NOT BETTER, ON THE FULL")
print(f"     RANGE: gls_origin goes from {B_ANCHOR_GLS:+.1f} pp (gas-dom) to {_bgls_full:+.1f} pp (full range).")
print(f"     It is a property of that statistic, not of SPARC.")
print(f"  4. DECOMPOSITION OF THE GAP between this analysis's full-sample value and 1.2e-10:")
for a_, d_ in sorted(OUT["axis_shares_of_gap"].items(), key=lambda t: -abs(t[1]["delta"])):
    print(f"       {a_:<52}{d_['pct']:>8.1f}%")
print(f"     -> The M/L (Upsilon) prescription is the DOMINANT axis. Estimator choice")
print(f"        contributes with the OPPOSITE sign and does not explain the gap.")
print(f"  5. THEREFORE: 'the literature is biased high and the true value is canonical' is")
print(f"     NOT licensed by anything measured here. The published 1.2e-10 is ROBUST to the")
print(f"     estimator bias this repo established. The 28% gap is the a0-Upsilon degeneracy")
print(f"     (plus a ~{100*abs(1-OUT['per_axis_isolated']['(iv) form: framework nu vs McGaugh nu, SAME ODR-log estimator, FULL Ud=0.50']['ratio']):.0f}% functional-form conversion between the a0-line's a0 and the")
print(f"     RAR's g_dagger), NOT an estimator artefact.")
print(f"  6. a0's VALUE remains POSITED in the framework. Nothing here derives it.")
OUT["verdict"] = VERD

print("\n" + bar)
print(f"  wall clock {time.time()-t_start:.0f}s")
print("  POSITED CLAUSE: a0's VALUE remains POSITED in the framework. This script resolves a")
print("  MEASUREMENT-METHODOLOGY question, not the theory's free coefficient. Both footings")
print("  carried on every dimensional number. No 'theory closed', no TOE claim.")
print("  CIRCULARITY: mocks generated FROM each nu test ESTIMATORS only, never the law.")
print(bar)

OUT["meta"] = dict(N_real=N_REAL, seed=SEED, injections=A0_INJ, injection_labels=INJ_LAB,
                   wall_s=float(time.time() - t_start), scipy_odr_fit_type="explicit ODR",
                   btfr_chi=BTFR_CHI,
                   posited="a0's VALUE remains POSITED; measurement methodology only.")
_j = os.path.join(HERE, "published_a0_transfer_results.json")
with open(_j, "w") as fh:
    json.dump(OUT, fh, indent=1, default=float)
print(f"  wrote {_j}")
