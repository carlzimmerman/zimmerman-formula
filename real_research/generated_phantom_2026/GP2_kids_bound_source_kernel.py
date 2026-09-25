#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
GP2 -- KiDS-1000 FOR THE GENERATED-PHANTOM CONSTRUCTION: a kernel sourced only by bound baryons (GP1), screened at a
length lambda, fitted to the isolated-lens lensing profiles of Brouwer+2021 with the committed blind-kernel machinery.

WHY.  Every earlier completion failed KiDS-1000 through the external-field effect (EFE) of the web on each lens:
C-H/K + switch reads the whole web (+404, BS3), a baryons-only kernel reads the web's gas (+133..+152, BS3; +233..+241,
L355), and the Yukawa-screened kernel reads the whole web inside lambda (best +7.7 / +8.0 at lambda = 0.7 Mpc, BK1),
while its growth fails (BK3).  In GP1's construction the kernel's source is the baryons of BOUND regions only; the
web's gas and the dark component are kernel-invisible, so they neither source the phantom nor feel it.  An isolated
lens then feels only the field of OTHER bound baryons: the large-scale part is the matter field times beta_B (GP0), the
discrete part is the pull of individual galaxies, groups and clusters (GP0's Poisson sampler, KiDS-like isolation).

MACHINERY (loaded unedited from real_research/blind_kernel_2026/BK1_screened_kernel.py, everything before its C1):
the four Brouwer+21 stellar-mass bins with full covariance, the exact stacked-lens QUMOND flux law with L340's
nu_mono, the screened point-mass law M_dyn = M_b [1 + s (N(s y_N, e) - 1)], s = (1 + r/lambda) e^(-r/lambda), the
linear screened field outside the 3 Mpc isolation sphere (SIGE), the projected linear 2-halo template with a free
amplitude b <= 2 per bin, M_b profiled per bin.  The comparator is BK1's: the EFE-free switch fit (lambda = inf,
e = 0, x_c profiled over 0/3/5/7/10) -- an idealisation, the same for every model here.
THE PHANTOM'S FORM: the Lagrangian one of GP1 (N2/N3): the action re-screens the phantom's source, rho_ph -> S* rho_ph,
which BK1's M_dyn = M_b [1 + s (N - 1)] omits (BK1's one-S form is 3% non-reciprocal, GP1 N3); applied here exactly
for the stacked spherical profile by a closed-form Yukawa shell kernel.  BK1's form is used only to reproduce BK1 (C0)
and is reported alongside (W6).
THE CONSTRUCTION'S FIELD: g = g_lin + g_P per lens, g_lin Gaussian with rms beta_B(z_l) x SIGE(lambda) and g_P from
GP0's Monte Carlo of discrete bound clumps; the stack uses the sampled |g| distribution (not a Maxwellian).  There is
NO flux switch in the construction (x_c = 0): the source switch keeps the web Newtonian (GP1), so nothing truncates a
lens's phantom except its own screening and the bound baryons' EFE.

CHECKS (gates fixed before the run unless marked)
  C0 CONTROL: with the whole matter field in the kernel (beta = 1, BK1's Maxwellian stack) the code reproduces BK1's
     no-switch Delta chi^2 at lambda = 0.7 (+7.7 / +8.0) and lambda = inf (+396.3 / +407.8) within 0.5; GP0's P(k)
     equals BK1's to 1e-3; the generalised fitter (2-halo + carrier template by bounded least squares) reproduces
     BK1's fitter when the carrier is switched off.
  E1 (documentary) the construction's external field per reading of "bound" and per lambda (median and rms, a0).
  E2 THE SOURCE SWITCH QUIETS THE KERNEL'S EXTERNAL FIELD: for every lambda <= 2 Mpc on the grid, the median field of
     the observed reading is below KiDS's single-field bound (7.2e-5 / 5.2e-5 of each footing's a0, BS2 E7).
  W1 THE WINDOW (no dark halo around the lens): for the OBSERVED reading (stars + cold gas + the hot gas of groups and
     clusters), some lambda >= 0.5 Mpc (BK1 C1: the Sun keeps the Galaxy's field, SPARC unchanged to 100 kpc) fits
     KiDS-1000 within Delta chi^2 <= 4 of the switch comparator on all points AND inside 0.3 Mpc, both footings.
  W2 (documentary) W1 for the stars, galaxy and maximal readings.   W3 (documentary) no screening (lambda = inf).
  R1 (documentary; added after the second run) THE PHYSICAL FLOOR on this machinery: the best a point-mass QUMOND lens
     can do with ONE uniform external field (e profiled, no screening, same 2-halo freedom), and screening alone (e = 0).
     The comparator is BK1's retained-mass switch profile, which Gauss forbids for a local switch (L352); R1 says how
     close a realizable model can get.
  B1 (documentary) a simple LCDM benchmark (point-mass baryons tied by Moster+13, NFW(M200 free per bin) truncated at
     r200 with L355's c(M), the same 2-halo term).  NOT a fair LCDM fit (no M200 scatter, miscentring or splashback);
     reported so that no one reads the construction's chi^2 against it as a win.
  F1 (documentary) the dark component around the lens: the construction plus the carrier's surviving halo,
     f_s (1 - f_b) NFW(M200) of each bin's Moster+13 host (L355's template; kernel-invisible, so it adds linearly),
     f_s profiled on [0, 1]: the best f_s, and Delta chi^2 at f_s = 1 (a CDM halo the carrier never cleared).
  W6 (documentary) W1's table with BK1's one-S (non-Lagrangian) form, for comparison with BK1 and the first run.
  W5 (documentary) the same numbers against L352's acceptance (the reference of L352/L359/L360: Delta chi^2 <= +4 against
     the UNSWITCHED base, isolated MOND + the 2-halo term), so the lanes can be read side by side.
  W4 (documentary) the assembled construction (observed reading + lambda + the carrier's surviving halo, f_s in
     [0, 0.5]) against the switch comparator and the physical floor given the SAME carrier freedom.
     (Record: W4 was first declared as a gate against B1 and "passed" at every lambda by ~150-200 in chi^2.  B1 scores
      these data at chi^2 = 286 (185 with the NFW untruncated), far from published LCDM halo-model fits of the same
      profiles, so that pass carried no information and was withdrawn before commit.)
  I1 INJECTION at W1's best lambda (observed, canonical): synthetic data from the construction pass W1's test in >= 80%
     of 10 draws (the gate has the power to pass a true construction).
  MUTATE=1: the kernel reads the whole matter field (beta = 1, BK1's stack): E2 must FAIL (rc = 1).
  (Record: the first two runs used BK1's one-S form throughout; GP1's reciprocity test then showed that form is not
   Lagrangian (3% asymmetric) and that the action's form lowers the enclosed lensing mass by 6-35% at 1-2.6 Mpc
   (lambda 2-3 Mpc).  Every table is now built with the Lagrangian form; BK1's form survives only in C0 and W6.)
SCOPE.  Static, QUMOND-form, point-mass baryons, lens z = 0.25, the isolation criterion approximated as in GP0; the
large-scale field in linear theory (BS3: isolation does not quiet the long modes, and a linear mock agrees with the
analytic field to 2%).  lambda remains a free length (BK2: not derived).

Run from the repository root:  python3 real_research/generated_phantom_2026/GP2_kids_bound_source_kernel.py
"""
import os, sys, json, math, time, io, contextlib, warnings
import numpy as np
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")   # spurious macOS-Accelerate BLAS flags (as BK1)
warnings.filterwarnings("ignore", category=RuntimeWarning)
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import GP0_bound_baryon_census as GP0                                  # noqa: E402

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "GP2_kids_bound_source_kernel"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "GP2", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the kernel reads the whole matter field (beta = 1, BK1's stack); E2 must FAIL ***")

# ---------------------------------------------------------------------------------- BK1's machinery, unedited
P1 = os.path.join(REPO, "real_research", "blind_kernel_2026", "BK1_screened_kernel.py")
NS = {"__name__": "bk1", "__file__": P1}
_src = open(P1).read().split('banner("C1  WHAT THE SCREENING MUST LEAVE ALONE')[0]
_src = _src.replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src, NS)
esd_from_M, model_M, stack_weights, fit_2h = NS["esd_from_M"], NS["model_M"], NS["stack_weights"], NS["fit_2h"]
ENODES, LMB, Rd, Ed, npb, T2H = NS["ENODES"], NS["LM"], NS["Rd"], NS["Ed"], NS["npb"], NS["T2H"]
SIGE, K_out, kq, CG, Pk0_bk1, A0, FOOTS = NS["SIGE"], NS["K_out"], NS["kq"], NS["CG"], NS["Pk0"], NS["A0"], NS["FOOTS"]
MS, PCm, MPCm, G, rr, Rp, GS, XCS, Cf = NS["MS"], NS["PCm"], NS["MPCm"], NS["G"], NS["rr"], NS["Rp"], NS["GS"], NS["XCS"], NS["Cf"]
_trap = NS["_trap"]; ZL = NS["ZL"]
BK1_RES = json.load(open(os.path.join(REPO, "real_research", "blind_kernel_2026", "BK1_screened_kernel_results.json")))
LAM_MIN = float(BK1_RES["numbers"]["lambda_min"])
P(f"  BK1 machinery loaded; lambda_min (Sun + SPARC, BK1 C1) = {LAM_MIN} Mpc   [{time.time() - T0:.0f}s]")

LAMS = [0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 5.0, 7.0, 10.0, float("inf")]
for lam in LAMS:                                                        # the screened linear field for lambdas BK1 lacks
    if lam not in SIGE:
        SIGE[lam] = {Ri: math.sqrt(CG ** 2 * _trap(Pk0_bk1(kq) * K_out(kq, Ri, lam) ** 2, kq) / (2 * math.pi ** 2)) for Ri in (3.0, 1.0)}
DATA = [np.array(e) for e in Ed]
SEL = [b * npb + i for b in range(4) for i in range(npb) if Rd[b][i] <= 0.3]
NSAMP = 20000


def shell_frac(r, rp, lam):
    """fraction of a unit-mass shell of radius rp, smeared by the normalised Yukawa kernel e^(-d/lam)/(4 pi lam^2 d),
    that lies inside radius r (closed form; -> 1 as r -> inf, 0 at r = 0)."""
    em = np.exp(-rp / lam)
    IB = lam * em * (lam - np.exp(-r / lam) * (r + lam))
    IA_in = lam * (np.exp(np.minimum(r - rp, 0.0) / lam) * (r - lam) + lam * em)
    IA_rp = lam * ((rp - lam) + lam * em)
    IA_out = IA_rp + lam * ((rp + lam) - np.exp(-np.maximum(r - rp, 0.0) / lam) * (r + lam))
    return (np.where(r <= rp, IA_in, IA_out) - IB) / (2 * lam * rp)


_PCACHE = {}


def rescreen(Mstack, Mb, lam):
    """THE LAGRANGIAN FORM (GP1 N2/N3): the action re-screens the phantom's source, rho_ph -> S* rho_ph = rho_ph -
    Y_lam * rho_ph.  Mstack: (n, len(rr)) enclosed masses of BK1's one-S form; returns the Lagrangian enclosed masses."""
    if not np.isfinite(lam): return Mstack
    if lam not in _PCACHE:
        _PCACHE.clear(); lm_ = lam * MPCm
        _PCACHE[lam] = shell_frac(rr[:, None], rr[None, :], lm_)
    Pm = _PCACHE[lam]
    Mph = Mstack - Mb
    dM = np.diff(Mph, axis=1, prepend=0.0)
    return Mstack - dM @ Pm.T


FORM = "lagrangian"


def table_from_samples(e_abs_a0, a0, lam, extra_M=None, form=None):
    """stacked ESD block [im, bin, R] for |e| samples (units of a0) at screening lam, no flux switch (x_c = 0).
    form: "lagrangian" (default; S* div[q' grad S u_B], GP1) or "bk1" (BK1's one-S form).
    extra_M: optional per-bin enclosed-mass arrays (kg) of an unboosted, kernel-invisible component."""
    form = form or FORM
    w = stack_weights(e_abs_a0); nz = [i for i in range(len(ENODES)) if w[i] > 1e-4]; w = w[nz] / w[nz].sum()
    arr = np.zeros((len(LMB), 4, npb))
    for im, lm in enumerate(LMB):
        Mb = 10 ** lm * MS
        Ms = np.array([model_M(Mb, a0, ie, lam) for ie in nz])
        if form == "lagrangian": Ms = rescreen(Ms, Mb, lam)
        if extra_M is None:
            acc = 0
            for wi, M in zip(w, Ms):
                Rq, dS = esd_from_M(M, Mb, 0.0); acc = acc + wi * dS
            arr[im] = [np.interp(Rd[b], Rq, acc) for b in range(4)]
        else:
            for b in range(4):
                acc = 0
                for wi, M in zip(w, Ms):
                    Rq, dS = esd_from_M(M + extra_M[b], Mb, 0.0); acc = acc + wi * dS
                arr[im, b] = np.interp(Rd[b], Rq, acc)
    return arr


def comparator(a0):
    arr = np.zeros((len(XCS), len(LMB), 4, npb))
    for im, lm in enumerate(LMB):
        Mb = 10 ** lm * MS; M = model_M(Mb, a0, 0, float("inf"))
        for ix, xc in enumerate(XCS):
            Rq, dS = esd_from_M(M, Mb, xc); arr[ix, im] = [np.interp(Rd[b], Rq, dS) for b in range(4)]
    return arr


def best_over_xc(arr, data, bmax, sel=None):
    best = None
    for ix in range(arr.shape[0]):
        c_, im, bb = fit_2h(arr[ix], data, bmax, sel)
        if best is None or c_ < best[0]: best = (c_, ix, im, bb)
    return best


TM = NS["TM"]
from scipy.optimize import lsq_linear


def fit_gen(blk, data, bmax, sel=None, tcar=None, fmax=0.0):
    """BK1's fit_2h generalised: blk[ip, bin, R] with any number of profiled values ip per bin; 2-halo amplitude
    b in [0, bmax] per bin; optional kernel-invisible template tcar[bin][R] with ONE shared amplitude f in [0, fmax]
    (bounded least squares, as BK1 does for b).  Returns (chi2, ip per bin, amplitudes)."""
    D = np.concatenate(data); idx = np.arange(4 * npb) if sel is None else np.array(sel)
    Cs = Cf[np.ix_(idx, idx)]; U = np.linalg.cholesky(np.linalg.inv(Cs))
    cols = [TM[idx]]; ub = [bmax] * 4
    if tcar is not None and fmax > 0:
        cols.append(np.concatenate(tcar)[idx][:, None]); ub = ub + [fmax]
    A = U.T @ np.hstack(cols); Apinv = np.linalg.pinv(A); ub = np.array(ub, float)
    def solve_batch(R_):
        Y = (U.T @ R_[:, idx].T).T
        if np.all(ub == 0): return np.zeros((len(Y), A.shape[1])), np.sum(Y ** 2, 1)
        Bu = (Apinv @ Y.T).T; out = Bu.copy(); c2 = np.sum((Bu @ A.T - Y) ** 2, 1)
        bad = np.where(np.any(Bu < 0, 1) | np.any(Bu > ub, 1))[0]
        for i in bad:
            r_ = lsq_linear(A, Y[i], bounds=(np.zeros_like(ub), np.maximum(ub, 1e-300)), method="bvls")
            out[i] = r_.x; c2[i] = float(np.sum((A @ r_.x - Y[i]) ** 2))
        return out, c2
    n_p = blk.shape[0]; ip = [n_p // 2] * 4; best, bb = None, None
    for _ in range(12):
        moved = False
        for b in range(4):
            base = np.concatenate([blk[ip[q], q] for q in range(4)])
            V = np.repeat(base[None, :], n_p, axis=0); V[:, b * npb:(b + 1) * npb] = blk[:, b]
            bs, c2 = solve_batch(D[None, :] - V)
            j = int(np.argmin(c2))
            if j != ip[b]: ip[b], moved = j, True
            best, bb = float(c2[j]), bs[j]
        if not moved: break
    return best, ip, bb


COMP = {f: comparator(A0[f]) for f in FOOTS}
REF = {f: {"all": best_over_xc(COMP[f], DATA, 2.0)[0], "in": best_over_xc(COMP[f], DATA, 2.0, SEL)[0],
           "iso_all": fit_2h(COMP[f][0], DATA, 2.0)[0], "iso_in": fit_2h(COMP[f][0], DATA, 2.0, SEL)[0]} for f in FOOTS}
P(f"  comparator (EFE-free switch, x_c profiled) chi^2: canonical {REF['canonical']['all']:.1f}, alt {REF['alt']['all']:.1f}; "
  f"isolated MOND (no switch, no EFE) sits at {REF['canonical']['iso_all'] - REF['canonical']['all']:+.1f} / "
  f"{REF['alt']['iso_all'] - REF['alt']['all']:+.1f}   [{time.time() - T0:.0f}s]")
OUT["numbers"]["reference"] = {f: {k: float(v) for k, v in REF[f].items()} for f in FOOTS}


def score(arr, foot):
    return (fit_2h(arr, DATA, 2.0)[0] - REF[foot]["all"], fit_2h(arr, DATA, 2.0, SEL)[0] - REF[foot]["in"])


# ============================================================================================ C0
banner("C0  CONTROL: the whole matter field in the kernel (BK1's Maxwellian stack) reproduces BK1; GP0's P(k) = BK1's")
c0 = {}
for foot in FOOTS:
    for lam in (0.7, float("inf")):
        e_s = np.linalg.norm(GS, axis=1) * SIGE[lam][3.0] / math.sqrt(3) / A0[foot]
        c0[(foot, lam)] = score(table_from_samples(e_s, A0[foot], lam, form="bk1"), foot)[0]
bk1 = {("canonical", 0.7): 7.7, ("alt", 0.7): 8.0, ("canonical", float("inf")): 396.3, ("alt", float("inf")): 407.8}
kk = np.geomspace(1e-3, 10, 50); pk_dev = float(np.max(np.abs(GP0.Pk0(kk) / Pk0_bk1(kk) - 1)))
fit_dev = max(abs(fit_gen(COMP[f][ix], DATA, 2.0, sel)[0] - fit_2h(COMP[f][ix], DATA, 2.0, sel)[0])
              for f in FOOTS for ix in range(len(XCS)) for sel in (None, SEL))
P(f"    generalised fitter vs BK1's fit_2h (carrier off): max |Delta chi^2| = {fit_dev:.1e}")
P("    " + "; ".join(f"{f} lambda {l}: {v:+.1f} (BK1 {bk1[(f, l)]:+.1f})" for (f, l), v in c0.items()) + f";  max |P_GP0/P_BK1 - 1| = {pk_dev:.1e}")
OUT["numbers"]["C0"] = {f"{f}|{l}": v for (f, l), v in c0.items()}; OUT["numbers"]["C0_pk_dev"] = pk_dev; OUT["numbers"]["C0_fit_dev"] = fit_dev
check("C0 CONTROL: BK1's no-switch Delta chi^2 reproduced within 0.5 (lambda = 0.7 and inf, both footings), GP0's P(k) = BK1's to "
      "1e-3, and the generalised fitter = BK1's fitter to 1e-6 with the carrier off",
      {**{f"{f}|{l}": round(v, 2) for (f, l), v in c0.items()}, "pk_dev": f"{pk_dev:.1e}", "fit_dev": f"{fit_dev:.1e}"},
      all(abs(v - bk1[k]) <= 0.5 for k, v in c0.items()) and pk_dev < 1e-3 and fit_dev < 1e-6)

# ============================================================================================ fields
banner("E1  THE CONSTRUCTION'S EXTERNAL FIELD AT AN ISOLATED LENS: large-scale bound baryons + discrete clumps (z = 0.25)")
READS = ("stars", "galaxy", "observed", "maximal")
BETA = {rd: GP0.census(ZL, rd)["beta_B"] for rd in READS}
rng = np.random.default_rng(20260925)
FIELD = {}
for rd in READS:
    for lam in LAMS:
        if MUTATE:
            g = GS[:NSAMP] * SIGE[lam][3.0] / math.sqrt(3)
        else:
            g_lin = rng.standard_normal((NSAMP, 3)) * BETA[rd] * SIGE[lam][3.0] / math.sqrt(3)
            g = g_lin + GP0.poisson_field_samples(ZL, rd, lam, NSAMP, rng)
        FIELD[(rd, lam)] = np.linalg.norm(g, axis=1)
e1 = {}
for rd in READS:
    e1[rd] = {str(l): {"median_a0": float(np.median(FIELD[(rd, l)]) / A0["canonical"]),
                       "rms_a0": float(np.sqrt(np.mean(FIELD[(rd, l)] ** 2)) / A0["canonical"])} for l in LAMS}
    P(f"    {rd:9s} (beta_B {BETA[rd]:.4f}): " + "; ".join(f"lam {l}: med {e1[rd][str(l)]['median_a0']:.1e}, rms {e1[rd][str(l)]['rms_a0']:.1e}"
                                                        for l in LAMS))
OUT["numbers"]["E1"] = {"beta_B": BETA, "field": e1, "kids_single_field_bound": {"canonical": 7.2e-5, "alt": 5.2e-5}}
check("E1 (documentary) the construction's field (median / rms, a0 canonical) vs KiDS's single-field bound 7.2e-5 / 5.2e-5",
      {rd: {str(l): f"{e1[rd][str(l)]['median_a0']:.1e}/{e1[rd][str(l)]['rms_a0']:.1e}" for l in (1.0, 2.0, 3.0, float('inf'))} for rd in READS},
      True, "", load_bearing=False)

FIELD_MED = {f: {l: float(np.median(FIELD[("observed", l)]) / A0[f]) for l in LAMS} for f in FOOTS}
EBOUND = {"canonical": 7.2e-5, "alt": 5.2e-5}
e2_ok = all(FIELD_MED[f][l] <= EBOUND[f] for f in FOOTS for l in LAMS if l <= 2.0)
check("E2 THE SOURCE SWITCH QUIETS THE KERNEL'S EXTERNAL FIELD: observed reading, every lambda <= 2 Mpc, median field below "
      "KiDS's single-field bound (each footing's a0)",
      {f: {str(l): f"{FIELD_MED[f][l]:.1e}" for l in LAMS if l <= 2.0} for f in FOOTS}, e2_ok,
      "the kernel that reads the whole matter field exceeds the bound from lambda ~ 0.8 Mpc up (BK1 C2)")

# ============================================================================================ W1-W3
banner("W1-W3  KiDS-1000 WITH THE BOUND-SOURCE KERNEL (no flux switch; 2-halo b <= 2; vs BK1's EFE-free switch comparator)")
RES, TABS, RES_BK1 = {}, {}, {}
for lam in LAMS:
    for rd in READS:
        for foot in FOOTS:
            arr = table_from_samples(FIELD[(rd, lam)] / A0[foot], A0[foot], lam)
            TABS[(rd, foot, lam)] = arr
            RES[(rd, foot, lam)] = score(arr, foot)
    for foot in FOOTS:                                                  # BK1's one-S (non-Lagrangian) form, observed reading
        RES_BK1[(foot, lam)] = score(table_from_samples(FIELD[("observed", lam)] / A0[foot], A0[foot], lam, form="bk1"), foot)
for rd in READS:
    P(f"    {rd:9s}: " + " | ".join(f"lam {l}: {RES[(rd, 'canonical', l)][0]:+.1f}/{RES[(rd, 'alt', l)][0]:+.1f} "
                                    f"(<0.3: {RES[(rd, 'canonical', l)][1]:+.1f}/{RES[(rd, 'alt', l)][1]:+.1f})" for l in LAMS))
P("    observed, BK1's one-S form: " + " | ".join(f"lam {l}: {RES_BK1[('canonical', l)][0]:+.1f}/{RES_BK1[('alt', l)][0]:+.1f}" for l in LAMS)
  + f"   [{time.time() - T0:.0f}s]")
OUT["numbers"]["W_bk1_form"] = {f"{f}|{l}": v for (f, l), v in RES_BK1.items()}
OUT["numbers"]["W"] = {f"{rd}|{f}|{l}": {"dchi2_all": v[0], "dchi2_in03": v[1]} for (rd, f, l), v in RES.items()}


def window(rd):
    return [l for l in LAMS if l >= LAM_MIN and all(RES[(rd, f, l)][0] <= 4 and RES[(rd, f, l)][1] <= 4 for f in FOOTS)]


WIN = {rd: window(rd) for rd in READS}
check("W1 THE WINDOW (observed reading): some lambda >= lambda_min fits KiDS-1000 within Delta chi^2 <= 4 of the comparator, "
      "all points AND inside 0.3 Mpc, both footings", f"passing lambda: {WIN['observed']}", len(WIN["observed"]) > 0,
      "a non-empty window: the kernel blind to the web's gas and dark matter, with a screening length, survives what "
      "excluded C-H/K + switch (BS3), the baryons-only kernel (L355) and the all-matter screened kernel (BK1)")
check("W2 (documentary) the window for the other readings of 'bound'", {rd: WIN[rd] for rd in READS}, True, "", load_bearing=False)
check("W3 (documentary) no screening (lambda = inf): Delta chi^2 per reading (canonical/alt)",
      {rd: f"{RES[(rd, 'canonical', float('inf'))][0]:+.1f}/{RES[(rd, 'alt', float('inf'))][0]:+.1f}" for rd in READS}, True,
      "", load_bearing=False)

# ============================================================================================ W5
ISO = {f: REF[f]["iso_all"] - REF[f]["all"] for f in FOOTS}
W5 = {rd: {str(l): [RES[(rd, f, l)][0] - ISO[f] for f in FOOTS] for l in LAMS} for rd in READS}
P("    against L352's acceptance (unswitched isolated MOND + 2-halo base, gate <= +4), observed reading: "
  + ", ".join(f"lam {l}: {W5['observed'][str(l)][0]:+.1f}/{W5['observed'][str(l)][1]:+.1f}" for l in LAMS))
OUT["numbers"]["W5"] = W5
check("W5 (documentary) against L352's acceptance (isolated MOND + 2-halo base; the reference of L352/L359/L360)",
      {rd: {str(l): f"{W5[rd][str(l)][0]:+.1f}/{W5[rd][str(l)][1]:+.1f}" for l in (1.5, 2.0, 3.0, float('inf'))} for rd in READS},
      True, "", load_bearing=False)

# ============================================================================================ R1
banner("R1  THE PHYSICAL FLOOR: one uniform external field (profiled), no screening; and screening alone (e = 0)")


def tab_uniform(a0, ie, lam):
    arr = np.zeros((len(LMB), 4, npb))
    for im, lm in enumerate(LMB):
        Mb = 10 ** lm * MS; M = model_M(Mb, a0, ie, lam); Rq, dS = esd_from_M(M, Mb, 0.0)
        arr[im] = [np.interp(Rd[b], Rq, dS) for b in range(4)]
    return arr


R1 = {}
for foot in FOOTS:
    rows = {}
    for ie in range(1, len(ENODES)):
        if not (3e-6 <= ENODES[ie] <= 2e-3): continue
        rows[ENODES[ie]] = score(tab_uniform(A0[foot], ie, float("inf")), foot)
    e_best = min(rows, key=lambda e: rows[e][0])
    scr = {l: score(tab_uniform(A0[foot], 0, l), foot)[0] for l in (0.7, 1.0, 1.5, 2.0, 3.0)}
    R1[foot] = {"e_best": e_best, "floor_all": rows[e_best][0], "floor_in": rows[e_best][1], "screening_only": scr,
                "by_e": {f"{e:.1e}": v[0] for e, v in rows.items()}}
    P(f"    {foot}: best uniform e = {e_best:.1e} a0 -> Delta chi^2 {rows[e_best][0]:+.1f} (inside 0.3: {rows[e_best][1]:+.1f}); "
      f"screening alone: " + ", ".join(f"lam {l}: {v:+.1f}" for l, v in scr.items()))
OUT["numbers"]["R1"] = {f: {k: (v if not isinstance(v, dict) else {str(a): b for a, b in v.items()}) for k, v in R1[f].items()} for f in FOOTS}
check("R1 (documentary) the physical floor: the best uniform-field QUMOND fit against the (Gauss-forbidden) switch comparator",
      {f: f"e = {R1[f]['e_best']:.1e}: {R1[f]['floor_all']:+.1f}" for f in FOOTS}, True,
      "no realizable point-mass QUMOND lens tested here reaches W1's <= 4; the construction is measured against this floor",
      load_bearing=False)

# ============================================================================================ B1
banner("B1  THE LCDM BENCHMARK on the same data: baryons (Moster+13, M_b = 1.4 M_*) + NFW(M200 free per bin) + 2-halo b <= 2")
LOGMS = [10.0, 10.45, 10.70, 10.90]                                  # typical log M* of the four bins (L355)
M200s = [10 ** brentq(lambda lm: math.log10(GP0.moster_Mstar(10 ** lm, ZL)) - ls, 10.5, 15.5) for ls in LOGMS]
h = 0.6736
rho_c_z = GP0.RHO_CRIT0 * (GP0.Om * (1 + ZL) ** 3 + GP0.OL)          # Msun / Mpc^3 (physical)
c200 = lambda M: 10 ** (0.905 - 0.101 * math.log10(M / (1e12 / h)))   # Dutton & Maccio 2014 (as L355)


def nfw_M(M200, r_mpc):
    cc = c200(M200); r200 = (3 * M200 / (4 * math.pi * 200 * rho_c_z)) ** (1 / 3); rs = r200 / cc
    mm = lambda s_: np.log(1 + s_) - s_ / (1 + s_)
    return M200 * mm(np.minimum(r_mpc, r200) / rs) / mm(cc)


LM200 = np.linspace(10.8, 13.8, 101)
blk_l = np.zeros((len(LM200), 4, npb))
for i_, lm in enumerate(LM200):
    M200 = 10 ** lm; Mb = min(1.4 * float(GP0.moster_Mstar(M200, ZL)), 0.5 * M200)
    M = (Mb + (M200 - Mb) * nfw_M(M200, rr / MPCm) / M200) * MS
    Rq, dS = esd_from_M(M, Mb * MS, 0.0); blk_l[i_] = [np.interp(Rd[b], Rq, dS) for b in range(4)]
LCDM = {}
for foot in FOOTS:                                                      # data are the same for both footings
    ra = fit_gen(blk_l, DATA, 2.0); ri = fit_gen(blk_l, DATA, 2.0, SEL)
    LCDM[foot] = {"all": ra[0], "in": ri[0], "logM200": [float(LM200[i]) for i in ra[1]], "b": [round(float(x), 2) for x in ra[2][:4]]}
P(f"    LCDM chi^2 = {LCDM['canonical']['all']:.1f} (all points), {LCDM['canonical']['in']:.1f} (inside 0.3 Mpc); "
  f"log M200 per bin {LCDM['canonical']['logM200']} (Moster+13 hosts {[round(math.log10(m), 2) for m in M200s]}); b {LCDM['canonical']['b']}")
P(f"    switch comparator chi^2 = {REF['canonical']['all']:.1f} / {REF['alt']['all']:.1f};  LCDM - comparator = "
  f"{LCDM['canonical']['all'] - REF['canonical']['all']:+.1f} / {LCDM['alt']['all'] - REF['alt']['all']:+.1f}")
OUT["numbers"]["B1"] = LCDM
check("B1 (documentary) a simple LCDM benchmark (NOT a fair LCDM fit: no M200 scatter, miscentring or splashback)",
      f"{LCDM['canonical']['all']:.1f} (all), {LCDM['canonical']['in']:.1f} (<0.3 Mpc); vs switch comparator "
      f"{LCDM['canonical']['all'] - REF['canonical']['all']:+.1f}", True,
      "published halo-model fits of these profiles do far better; nothing below is scored against B1", load_bearing=False)

# ============================================================================================ F1
banner("F1  THE DARK COMPONENT AROUND THE LENS: + the carrier's surviving NFW halo (L355's template), f_s profiled")
TCAR = []
for b in range(4):
    Mc = (1 - GP0.FB) * nfw_M(M200s[b], rr / MPCm) * MS
    Rq, dS = esd_from_M(Mc + 1.0, 1.0, 0.0); TCAR.append(np.interp(Rd[b], Rq, dS))
F1 = {}
for foot in FOOTS:
    for lam in LAMS:
        arr = TABS[("observed", foot, lam)]
        ra = fit_gen(arr, DATA, 2.0, None, TCAR, 1.0); ri = fit_gen(arr, DATA, 2.0, SEL, TCAR, 1.0)
        full = fit_gen(arr + 0.0, [d - 1.0 * t for d, t in zip(DATA, TCAR)], 2.0)[0]          # f_s = 1 fixed
        F1[(foot, lam)] = {"best_fs": float(ra[2][4]), "chi2_all": ra[0], "chi2_in": ri[0], "chi2_fs1": full}
P("    lambda | best f_s (can/alt) | chi^2 - LCDM (can/alt) | at f_s = 1 (uncleared CDM halo), chi^2 - LCDM")
for lam in LAMS:
    c_, a_ = F1[("canonical", lam)], F1[("alt", lam)]
    P(f"    {lam:>6} | {c_['best_fs']:.2f} / {a_['best_fs']:.2f}        | {c_['chi2_all'] - LCDM['canonical']['all']:+6.1f} / "
      f"{a_['chi2_all'] - LCDM['alt']['all']:+6.1f}      | {c_['chi2_fs1'] - LCDM['canonical']['all']:+7.1f} / {a_['chi2_fs1'] - LCDM['alt']['all']:+7.1f}")
OUT["numbers"]["F1"] = {f"{f}|{l}": v for (f, l), v in F1.items()}
fs1_min = min(min(F1[(f, l)]["chi2_fs1"] - LCDM[f]["all"] for l in LAMS) for f in FOOTS)
check("F1 (documentary) KiDS on the dark component: best f_s per lambda, and the cost of an uncleared CDM halo (f_s = 1)",
      f"best f_s at lambda 3: {F1[('canonical', 3.0)]['best_fs']:.2f}/{F1[('alt', 3.0)]['best_fs']:.2f}; f_s = 1 costs >= {fs1_min:+.1f} vs LCDM",
      True, "the construction's dark component must be mostly absent from galaxy halos -- the carrier's job (L357, L365)",
      load_bearing=False)

# ============================================================================================ W4
banner("W4  THE ASSEMBLED CONSTRUCTION (documentary): + the carrier's surviving halo, f_s in [0, 0.5], vs the SAME freedom")
W4 = {}
FLOOR_FS = {}
for foot in FOOTS:
    ie_b = ENODES.index(R1[foot]["e_best"])
    FLOOR_FS[foot] = fit_gen(tab_uniform(A0[foot], ie_b, float("inf")), DATA, 2.0, None, TCAR, 0.5)[0]
    CMP_FS = min(fit_gen(COMP[foot][ix], DATA, 2.0, None, TCAR, 0.5)[0] for ix in range(len(XCS)))
    for lam in LAMS:
        arr = TABS[("observed", foot, lam)]
        ra = fit_gen(arr, DATA, 2.0, None, TCAR, 0.5)
        W4[(foot, lam)] = {"vs_switch_same_fs": ra[0] - CMP_FS, "vs_floor_same_fs": ra[0] - FLOOR_FS[foot], "fs": float(ra[2][4]),
                           "chi2": ra[0]}
P("    lambda | vs switch comparator + f_s (can/alt) | vs uniform-e floor + f_s (can/alt) | f_s (can/alt)")
for lam in LAMS:
    c_, a_ = W4[("canonical", lam)], W4[("alt", lam)]
    P(f"    {lam:>6} | {c_['vs_switch_same_fs']:+6.1f} / {a_['vs_switch_same_fs']:+6.1f}                     | "
      f"{c_['vs_floor_same_fs']:+6.1f} / {a_['vs_floor_same_fs']:+6.1f}                   | {c_['fs']:.2f} / {a_['fs']:.2f}")
OUT["numbers"]["W4"] = {f"{f}|{l}": v for (f, l), v in W4.items()}
lam4 = min(LAMS, key=lambda l: W4[("canonical", l)]["vs_floor_same_fs"] + W4[("alt", l)]["vs_floor_same_fs"])
check("W4 (documentary) the assembled construction against the realizable floor and the comparator, same carrier freedom",
      {"best lambda": lam4, "vs floor": f"{W4[('canonical', lam4)]['vs_floor_same_fs']:+.1f}/{W4[('alt', lam4)]['vs_floor_same_fs']:+.1f}",
       "vs comparator": f"{W4[('canonical', lam4)]['vs_switch_same_fs']:+.1f}/{W4[('alt', lam4)]['vs_switch_same_fs']:+.1f}",
       "f_s": f"{W4[('canonical', lam4)]['fs']:.2f}/{W4[('alt', lam4)]['fs']:.2f}"}, True, "", load_bearing=False)

# ============================================================================================ I1
banner("I1  INJECTION at W1's best lambda (observed, canonical): does W1's gate pass when the construction is true?")
lam_b = min(LAMS, key=lambda l: RES[("observed", "canonical", l)][0] + RES[("observed", "alt", l)][0])
rngi = np.random.default_rng(20260926); Lch = np.linalg.cholesky(Cf)
IMS = [int(np.argmin(np.abs(LMB - l))) for l in (10.2, 10.6, 10.9, 11.2)]
arr_t = TABS[("observed", "canonical", lam_b)]
mean_t = np.concatenate([arr_t[IMS[b], b] + T2H[b] for b in range(4)])
dd = []
for t in range(10):
    dv = mean_t + Lch @ rngi.standard_normal(4 * npb); dat = [dv[b * npb:(b + 1) * npb] for b in range(4)]
    dd.append(fit_2h(arr_t, dat, 2.0)[0] - best_over_xc(COMP["canonical"], dat, 2.0)[0])
fr = float(np.mean(np.array(dd) <= 4))
P(f"    lambda = {lam_b}: Delta chi^2 per draw {np.round(dd, 1).tolist()}; pass fraction {fr:.2f}")
OUT["numbers"]["I1"] = {"lambda": lam_b, "dchi2": dd, "pass_fraction": fr}
check("I1 when the construction is true W1's gate passes in >= 80% of 10 draws", f"{fr:.2f}", fr >= 0.8, "")

# ============================================================================================ verdict
banner("VERDICT")
P("  lambda | observed field med (a0) | kernel alone vs comparator (can/alt) | + carrier halo vs floor+f_s (can/alt), f_s")
for l in LAMS:
    P(f"  {l:>6} | {e1['observed'][str(l)]['median_a0']:.1e}               | {RES[('observed', 'canonical', l)][0]:+6.1f} / {RES[('observed', 'alt', l)][0]:+6.1f}"
      f"                     | {W4[('canonical', l)]['vs_floor_same_fs']:+6.1f} / {W4[('alt', l)]['vs_floor_same_fs']:+6.1f}, {W4[('canonical', l)]['fs']:.2f}")
P(f"""  The realizable floor (R1, one uniform field, no screening): {R1['canonical']['floor_all']:+.1f} / {R1['alt']['floor_all']:+.1f} against the Gauss-forbidden comparator;
  isolated MOND {REF['canonical']['iso_all'] - REF['canonical']['all']:+.1f} / {REF['alt']['iso_all'] - REF['alt']['all']:+.1f}; BK1's all-matter screened kernel +7.7 / +8.0 (lambda 0.7); C-H/K + switch +404 / +415 (BS3);
  baryons-only kernel +133..+152 (BS3).  W1 window (<= 4 vs the comparator): {WIN['observed']}.
  Against L352's acceptance (isolated MOND + 2-halo base, <= +4; the reference of L352/L359/L360), observed reading:
  {', '.join(f"lam {l}: {W5['observed'][str(l)][0]:+.1f}/{W5['observed'][str(l)][1]:+.1f}" for l in LAMS)}.
  Parameter-free variant (galaxy reading: stars + cold gas, no screening): {RES[('galaxy', 'canonical', float('inf'))][0]:+.1f} / {RES[('galaxy', 'alt', float('inf'))][0]:+.1f};
  stars only: {RES[('stars', 'canonical', float('inf'))][0]:+.1f} / {RES[('stars', 'alt', float('inf'))][0]:+.1f}.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname} ({time.time() - T0:.0f} s)")
sys.exit(0 if n_fail == 0 else 1)
