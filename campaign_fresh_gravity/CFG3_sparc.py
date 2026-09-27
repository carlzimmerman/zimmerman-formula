#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG3_sparc -- THE PRINCIPLE'S GALAXY LAW ON SPARC: the radial acceleration relation and the baryonic Tully-Fisher relation.

WHAT THE PRINCIPLE GIVES IN A GALAXY.  Every SPARC galaxy is a held-back region (bound; the gate is open, CFG3_principle D5),
the dark component is not answered and must not sit there (the requirement quantified in S6), and the answer is the Bose
kernel nu(y) = 1 + 1/(e^sqrt(y) - 1) (D2) acting on the baryons' field, with a0 = kappa c sqrt(G rho_Lambda) (kappa = 1/2
FITTED).  The coherence length l* >= 0.05 pc changes kpc-scale forces by <= 7.5 (l*/a)^2 (FP1 C1's bound: 3e-5 at 1 pc on a
0.5-kpc galaxy), so on SPARC the law is g_obs = nu(g_bar/a0) g_bar at every point.  The statistic is the record's
(real_research/rar_framework_a0_mlfit.py as FP1 C copies it: weighted rms of log g_obs - log nu g_bar, Upsilon_disc profiled on
0.30..1.20 in steps of 0.01, Upsilon_bul = 1.4 Upsilon_disc, weights (e_V/V)^-2), both footings, a0 fixed (never fitted).

CHECKS
  K1 CONTROL: the copied statistic reproduces FP1's committed numbers -- C0 (P2 at the ml-fit script's a0 and Upsilon = 0.70:
     0.108 dex) and C2 (P2 0.10827/0.10355, nu_mono 0.10033/0.09910 dex, Upsilon 0.70/0.65/0.61/0.57) to < 1e-9 -- which also
     validates this lane's copy of nu_mono.
  K2 CONTROL: the record's BTFR door (real_research/reviews/mi_btfr_intercept_kappa_door_2026.py, exec'd read-only) reproduces
     its kappa_hat = 0.465 +- 0.076 on its adopted Route-A kernel, and that kernel IS the Bose kernel (to 1e-12).
  S1 [HEADLINE] the Bose kernel on SPARC, both footings, Upsilon profiled, with FP1's paired galaxy bootstrap against nu_mono and P2.
  S2 [load-bearing; MUTATE must fail] the derived kernel is as good as the record's best kernel: its rms lies within 0.005 dex
     of nu_mono's on both footings.
  S3 (reported) the residual trend: binned median residual vs y at the best Upsilon, |median| < 0.05 dex in every bin with >= 30 points.
  S4 the BTFR: slope exactly 4 from the Rayleigh-Jeans limit (V^4 = G M a0 with coefficient 1, D2), and the intercept's kappa
     (K2) within 1 sigma of 1/2.
  S5 (reported) the dark-field requirement: adding a fraction f of each galaxy's LCDM-like halo (Moster+13 halo mass, Duffy+08
     NFW concentration) to the Bose law's g_obs raises the SPARC rms; the largest f with d rms <= +0.005 dex is the amount of
     unanswered dark field a galaxy's gated region may hold.
PRE-DECLARED HYPOTHESES (written before the first run of this script):
  H1 |rms(Bose) - rms(nu_mono)| <= 0.003 dex on both footings (the kernels differ by <= 0.0104 dex, only above y = 2.34). EXPECT TRUE.
  H2 the Bose kernel beats P2 in >= 95% of paired galaxy resamples on both footings (as nu_mono does, FP1 C2). EXPECT TRUE.
  H3 S5's f_max < 0.3: the dark field must be cleared from galaxies to well below its cosmic share. EXPECT TRUE.
MUTATE=1 replaces the Bose occupation by Fermi-Dirac (nu = 1 + 1/(e^sqrt(y) + 1): no classical enhancement): S2 must FAIL (rc = 1).
Run from the repository root (MUTATE first):  MUTATE=1 python3 campaign_fresh_gravity/CFG3_sparc.py; python3 campaign_fresh_gravity/CFG3_sparc.py
"""
import os, sys, math, json, re
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG3_common as C
import numpy as np

R = C.Run("CFG3_sparc", __doc__)
P, check = R.P, R.check
KER = C.nu_fermi if C.MUTATE else C.nu_bose
KNAME = "Fermi-Dirac (MUTATE)" if C.MUTATE else "Bose (derived)"
if C.MUTATE:
    P("\n  *** MUTATE=1: the derived kernel is replaced by the Fermi-Dirac occupation (no classical enhancement): S2 must FAIL ***")

# ------------------------------------------------------------------------------------------------ FP1 C's statistic (copied with attribution: FP1_static_sector.py:394-437)
kpc = 3.0857e19
DATA = os.path.join(C.REPO, "real_research", "data", "sparc_data")
GAL, NAMES = [], []
for f in sorted(os.listdir(DATA)):
    if not f.endswith("_rotmod.dat"):
        continue
    try:
        d = np.genfromtxt(os.path.join(DATA, f), comments="#")
    except Exception:
        continue
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    GAL.append(tuple(d[:, i] for i in range(6))); NAMES.append(f.replace("_rotmod.dat", ""))
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)


def gal_sums(nuf, a0, extra=None):
    """per-galaxy weighted SSR and weight on the Upsilon grid; extra(ig, Rm) adds a Newtonian acceleration to the model (S5)."""
    S = np.zeros((len(GAL), len(UPS)))
    Wt = np.zeros((len(GAL), len(UPS)))
    for ig, (Rk, Vobs, eV, Vgas, Vdisk, Vbul) in enumerate(GAL):
        Rm = Rk * kpc
        gx = extra(ig, Rm) if extra is not None else 0.0
        for iu, U in enumerate(UPS):
            Vbar2 = np.sign(Vgas) * Vgas ** 2 + U * Vdisk ** 2 + 1.4 * U * Vbul ** 2
            gb = Vbar2 * 1e6 / Rm
            go = (Vobs * 1e3) ** 2 / Rm
            ok = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (Vobs > 0)
            gm = nuf(gb[ok] / a0) * gb[ok] + (gx[ok] if extra is not None else 0.0)
            r_ = np.log10(go[ok]) - np.log10(gm)
            w_ = 1 / (np.clip(eV[ok], 1, None) / np.clip(Vobs[ok], 1, None)) ** 2
            S[ig, iu] = np.sum(w_ * r_ ** 2)
            Wt[ig, iu] = np.sum(w_)
    return S, Wt


def best(S, Wt, wg=None):
    wg = np.ones(len(GAL)) if wg is None else wg
    mse = (wg @ S) / (wg @ Wt)
    i = int(np.argmin(mse))
    return math.sqrt(mse[i]), float(UPS[i])


# ================================================================================================ K1
R.banner("K1  CONTROL: FP1's SPARC statistic and its committed numbers")
a0_mlfit = (2.998e8 / 2) * math.sqrt(6.674e-11 * 0.685 * 3 * 2.184e-18 ** 2 / (8 * math.pi * 6.674e-11))
S0, W0 = gal_sums(C.nu_p2, a0_mlfit)
iu70 = int(np.argmin(np.abs(UPS - 0.70)))
rms70 = math.sqrt(S0[:, iu70].sum() / W0[:, iu70].sum())
fp1 = json.load(open(os.path.join(C.CHAIN, "FP1_static_sector_results.json")))["numbers"]["C2"]["sparc"]
SUMS = {}
dev_k1 = 0.0
for foot, a0 in C.A0.items():
    SUMS[(foot, "P2")] = gal_sums(C.nu_p2, a0)
    SUMS[(foot, "mono")] = gal_sums(C.nu_mono, a0)
    rp, up = best(*SUMS[(foot, "P2")]); rm, um = best(*SUMS[(foot, "mono")])
    ref = fp1[foot]
    dev_k1 = max(dev_k1, abs(rp - ref["rms_P2"]), abs(rm - ref["rms_mono"]), abs(up - ref["ups_P2"]), abs(um - ref["ups_mono"]))
    P(f"    {foot:9s}: P2 {rp:.6f} dex (Upsilon {up:.2f}; FP1 {ref['rms_P2']:.6f}, {ref['ups_P2']:.2f});  nu_mono {rm:.6f} (Upsilon {um:.2f}; "
      f"FP1 {ref['rms_mono']:.6f}, {ref['ups_mono']:.2f})")
check("K1 CONTROL: the copied statistic (rar_framework_a0_mlfit.py's, as FP1 C) reproduces FP1 C0 (P2 at a0 = 9.3614e-11, Upsilon = 0.70: "
      "0.108 dex) and FP1 C2's committed rms and best Upsilon for P2 and nu_mono on both footings -- validating this lane's nu_mono copy",
      f"C0 {rms70:.4f} dex ({len(GAL)} galaxies); max |dev| vs FP1 C2 {dev_k1:.1e}", abs(rms70 - 0.108) < 5e-4 and dev_k1 < 1e-9)
R.num("K1", dict(C0=rms70, max_dev=dev_k1))

# ================================================================================================ K2
R.banner("K2  CONTROL: the record's BTFR intercept door, and its kernel")
btfr_path = os.path.join(C.REPO, "real_research", "reviews", "mi_btfr_intercept_kappa_door_2026.py")
sys.path.insert(0, os.path.dirname(btfr_path))
nsb, txt = C.exec_slices(btfr_path, [(None, None)], name="btfr_ro")
m_ = re.search(r"on the adopted kernel: kappa_hat = ([0-9.]+) \+- ([0-9.]+)", txt)
k_hat, k_err = (float(m_.group(1)), float(m_.group(2))) if m_ else (float("nan"), float("nan"))
yk = np.logspace(-6, 5, 2001)
kdev = float(np.max(np.abs(nsb["nu"](yk) / C.nu_bose(yk) - 1)))
P(f"    the record's door (exec'd read-only, stdout captured): kappa_hat = {k_hat} +- {k_err} on its adopted Route-A kernel; "
  f"max |nu_RouteA/nu_Bose - 1| = {kdev:.1e}")
check("K2 CONTROL: the record's BTFR door reproduces kappa_hat = 0.465 +- 0.076 on its adopted kernel, and that kernel is the Bose "
      "kernel to 1e-12 -- so the record's BTFR measurement IS this law's", f"kappa_hat {k_hat} +- {k_err}; kernel dev {kdev:.1e}",
      abs(k_hat - 0.465) < 1e-9 and abs(k_err - 0.076) < 1e-9 and kdev < 1e-12)
R.num("K2", dict(kappa_hat=k_hat, kappa_err=k_err, kernel_dev=kdev))

# ================================================================================================ S1-S2
R.banner(f"S1  THE DERIVED KERNEL ON SPARC ({KNAME}), both footings, Upsilon profiled, paired galaxy bootstrap")
rng = np.random.default_rng(12)
Wb = rng.multinomial(len(GAL), np.full(len(GAL), 1.0 / len(GAL)), size=999).astype(float)
S1 = {}
for foot, a0 in C.A0.items():
    SUMS[(foot, "law")] = gal_sums(KER, a0)
    rl, ul = best(*SUMS[(foot, "law")]); rm, um = best(*SUMS[(foot, "mono")]); rp, up = best(*SUMS[(foot, "P2")])
    d_m = np.array([best(*SUMS[(foot, "law")], w)[0] - best(*SUMS[(foot, "mono")], w)[0] for w in Wb])
    d_p = np.array([best(*SUMS[(foot, "P2")], w)[0] - best(*SUMS[(foot, "law")], w)[0] for w in Wb])
    S1[foot] = dict(rms=rl, ups=ul, rms_mono=rm, rms_P2=rp, d_vs_mono_median=float(np.median(d_m)),
                    d_vs_mono_95=[float(np.percentile(d_m, 2.5)), float(np.percentile(d_m, 97.5))],
                    frac_law_beats_P2=float(np.mean(d_p > 0)))
    P(f"    {foot:9s}: {KNAME} {rl:.5f} dex (Upsilon {ul:.2f});  nu_mono {rm:.5f};  P2 {rp:.5f};  paired d(rms) law - mono "
      f"{np.median(d_m):+.5f} [{np.percentile(d_m, 2.5):+.5f}, {np.percentile(d_m, 97.5):+.5f}];  law beats P2 in {np.mean(d_p > 0):.3f}")
R.num("S1", S1)
check("S1 (H1, H2) THE DERIVED KERNEL FITS SPARC AS WELL AS THE RECORD'S BEST: |rms(Bose) - rms(nu_mono)| <= 0.003 dex and the Bose kernel "
      "beats P2 in >= 95% of paired galaxy resamples, on both footings",
      "; ".join(f"{f}: {v['rms']:.4f} vs mono {v['rms_mono']:.4f}, beats P2 in {v['frac_law_beats_P2']:.3f}" for f, v in S1.items()),
      all(abs(v["rms"] - v["rms_mono"]) <= 0.003 and v["frac_law_beats_P2"] >= 0.95 for v in S1.values()), load_bearing=False)
check("S2 [load-bearing; MUTATE must fail] the derived kernel's SPARC rms lies within 0.005 dex of the record's best kernel (nu_mono) on "
      "both footings", "; ".join(f"{f}: {v['rms']:.4f} vs {v['rms_mono']:.4f}" for f, v in S1.items()),
      all(abs(v["rms"] - v["rms_mono"]) <= 0.005 for v in S1.values()))

# ================================================================================================ S3
R.banner("S3  THE RESIDUAL TREND ALONG y (the shape the Bose occupation fixes)")
edges = np.array([-3.0, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.5])
S3 = {}
for foot, a0 in C.A0.items():
    U = S1[foot]["ups"]
    ly, res = [], []
    for (Rk, Vobs, eV, Vgas, Vdisk, Vbul) in GAL:
        Rm = Rk * kpc
        gb = (np.sign(Vgas) * Vgas ** 2 + U * Vdisk ** 2 + 1.4 * U * Vbul ** 2) * 1e6 / Rm
        go = (Vobs * 1e3) ** 2 / Rm
        ok = (gb > 0) & (go > 0) & (Vobs > 0)
        ly.append(np.log10(gb[ok] / a0)); res.append(np.log10(go[ok]) - np.log10(KER(gb[ok] / a0) * gb[ok]))
    ly, res = np.concatenate(ly), np.concatenate(res)
    rows = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (ly >= lo) & (ly < hi)
        if m.sum() >= 30:
            rows.append((lo, hi, int(m.sum()), float(np.median(res[m]))))
    S3[foot] = rows
    P(f"    {foot:9s} (Upsilon {U:.2f}): " + "; ".join(f"[{lo:+.1f},{hi:+.1f}) N={n} med {md:+.3f}" for lo, hi, n, md in rows))
check("S3 (reported) no residual trend along y: the binned median residual is below 0.05 dex in every bin with >= 30 points, both footings",
      "; ".join(f"{f}: max |median| {max(abs(r[3]) for r in v):.3f}" for f, v in S3.items()),
      all(max(abs(r[3]) for r in v) < 0.05 for v in S3.values()), load_bearing=False)
R.num("S3", S3)

# ================================================================================================ S4
R.banner("S4  THE BARYONIC TULLY-FISHER RELATION")
k_sig = (k_hat - 0.5) / k_err
check("S4 THE BTFR: the Rayleigh-Jeans limit of the Bose kernel gives V^4 = G M_b a0 with coefficient exactly 1 (slope 4, D2); the record's "
      "intercept door on this very kernel measures kappa_hat = 0.465 +- 0.076, within 1 sigma of the fitted 1/2 (and of 1/2pi: the "
      "intercept cannot separate them, the door's own D8b)", f"kappa_hat {k_hat} +- {k_err}: {k_sig:+.2f} sigma from 1/2",
      abs(k_sig) < 1.0)
R.num("S4", dict(kappa_hat=k_hat, kappa_err=k_err, sigma_from_half=k_sig))

# ================================================================================================ S5
R.banner("S5  (reported) HOW MUCH UNANSWERED DARK FIELD A GALAXY MAY HOLD")
master = {}
for ln in open(os.path.join(C.REPO, "real_research", "data", "SPARC_Lelli2016c.mrt"), encoding="latin-1").read().splitlines():
    fz = ln.split()
    if len(fz) >= 18:
        try:
            master[fz[0]] = dict(L36=float(fz[7]), MHI=float(fz[13]))
        except ValueError:
            pass


def nfw_g_factory(f_dm, U):
    """Newtonian acceleration of f_dm x an LCDM-like NFW halo per galaxy: M_h from Moster+13 at z = 0 with M_* = U L_3.6, Duffy+08
    concentration c200 = 5.71 (M_h/2e12 h^-1)^-0.084, r200 from 200 rho_crit."""
    rc = C.RHO_CRIT_K
    cache = {}

    def g(ig, Rm):
        nm = NAMES[ig]
        if nm not in master:
            return np.zeros_like(Rm)
        if ig not in cache:
            Ms = max(U * master[nm]["L36"] * 1e9, 1e6)
            Mh = float(C.mh_of_mstar(Ms, 0.0))
            c200 = 5.71 * (Mh / (2e12 / C.H_KIDS)) ** (-0.084)
            r200 = (3 * Mh * C.MSUN / (4 * math.pi * 200 * rc)) ** (1 / 3)
            cache[ig] = (Mh, c200, r200)
        Mh, c200, r200 = cache[ig]
        rs = r200 / c200
        mfun = lambda x: np.log(1 + x) - x / (1 + x)
        Menc = Mh * C.MSUN * mfun(Rm / rs) / mfun(c200)
        return f_dm * C.G_SI * Menc / Rm ** 2
    return g


S5 = {}
for foot, a0 in C.A0.items():
    base, Ub = S1[foot]["rms"], S1[foot]["ups"]
    rows = []
    for f_dm in (0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0):
        Sx, Wx = gal_sums(KER, a0, extra=nfw_g_factory(f_dm, Ub))
        rx, ux = best(Sx, Wx)
        rows.append((f_dm, rx - base, ux))
    fmax = max([r[0] for r in rows if r[1] <= 0.005], default=0.0)
    S5[foot] = dict(rows=rows, f_max=fmax)
    P(f"    {foot:9s}: d rms for f = " + ", ".join(f"{r[0]:.2f}: {r[1]:+.4f} (Ups {r[2]:.2f})" for r in rows) + f"  -> f_max = {fmax}")
check("S5 (H3, reported) THE DARK-FIELD REQUIREMENT: the principle does not answer the dark field, so any dark field left inside a galaxy "
      "adds Newtonian mass on top of the answer; SPARC tolerates (d rms <= +0.005 dex) only a fraction f_max < 0.3 of an LCDM-like "
      "halo -- the dark sector must clear galaxies (the record's FP10 kick is one candidate)",
      "; ".join(f"{f}: f_max {v['f_max']}" for f, v in S5.items()), all(v["f_max"] < 0.3 for v in S5.values()), load_bearing=False)
R.num("S5", S5)

R.banner("W  THE LEDGER")
R.ledger("SP1", "DERIVED", "on SPARC the principle's law is nu_Bose = nu_RAR at fixed a0 (kappa = 1/2): rms " +
         " / ".join(f"{S1[f]['rms']:.4f}" for f in C.FOOTS) + " dex (canonical / alt)", "S1, S2")
R.ledger("SP2", "DERIVED", f"BTFR slope 4 with coefficient 1; the record's intercept on this kernel: kappa_hat = {k_hat} +- {k_err}", "S4, K2")
R.ledger("SP3", "REQUIREMENT", "unanswered dark field inside galaxies <= f_max of an LCDM halo: " + " / ".join(str(S5[f]["f_max"]) for f in C.FOOTS), "S5")
sys.exit(R.finish())
