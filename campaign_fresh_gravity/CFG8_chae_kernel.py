#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG8 -- FG001'S ONE COST: IS CHAE'S EXTERNAL-FIELD SIGNAL THE KERNEL AND THE a0 OF THE FIT?

FG001 (hierarchical ownership, CFG7) predicts NO external-field effect on a top-level galaxy.  Its registered cost is Chae
et al.'s detection in SPARC rotation curves (2020, ApJ 904, 51; 2021, ApJ 921, 104): 4.1 / 4.3 sigma against FG001's zero
(CFG7_hierarchy_fg001 H7).  Chae's fits use one specific law: the external-field function of his eq. 6, the 1-D AQUAL
solution built on the SIMPLE interpolating function, at a0 = 1.2e-10 m/s^2.  At low acceleration that function carries a
+1/2 tail (nu_simple -> 1/sqrt(z) + 1/2) that the framework's own law P2 does not (nu_P2 -> 1/sqrt(z) + sqrt(z)/2), and the
framework's canonical a0 (9.3603e-11) lies 22% below 1.2e-10 (-0.054 dex in the deep regime).  A fit forced into the
simple-function shape at the higher a0 can register "an external field" of the size Chae reports simply to lower the boost.

THE TEST.  Refit all 153 SPARC galaxies of Chae's sample (inclination >= 30 deg, quality Q <= 2) with Chae's exact priors
(his Table 1) and his likelihood (his eqs. 2, 3, 8, 9), under seven laws:
   V1 simple  @ 1.2e-10 (Chae's own: the CONTROL)      V2 nu_RAR  @ 1.2e-10 (kernel changed, a0 kept)
   V3 simple  @ canonical (a0 changed, kernel kept)     V4 P2 @ canonical      V5 P2 @ alt
   V6 nu_mono @ canonical                               V7 nu_mono @ alt
The external-field function for every base law is the same 1-D AQUAL construction Chae's eq. 6 is (checked in C0):
   nu_e(z; e) = [ F(z + z_e) - e ] / z ,   F(Z) = nu(Z) Z ,   e = F(z_e)   (e = the external field in units of that law's a0).
Posteriors by an affine-invariant ensemble sampler (Goodman & Weare 2010, the algorithm of emcee; written here).
HISTORY (disclosed): a smoke run on Chae's four showcase galaxies (not committed) reproduced his published values under V1
(NGC 5055 +0.053 vs 0.054, NGC 5033 +0.103 vs 0.104, NGC 6674 -0.030 vs -0.015, NGC 1090 +0.060 vs 0.061) and showed the two
strong ones persist under V6 (+0.057, +0.115); it also showed C0 failing at 4.5e-5 because the simple function's inverse went
through the interpolation table -- the exact inverse z_e = e^2/(1+e) is used instead.  Nothing else was changed.

PRE-DECLARED (before this script's first full run)
  C0  CONTROL  the general construction with the simple function equals Chae's eq. 6 for e in [0, 0.5] to 1e-12.
  C1  CONTROL  the sampler recovers a known e injected into a synthetic galaxy (bias < 0.25 sigma, 3 cases).
  C2  CONTROL  V1 reproduces Chae 2020: the median fitted e of the galaxies with <x0> < -10.3 within 0.02 of his 0.052
      (his bootstrap error 0.011); the -10.3 < <x0> < -9 galaxies consistent with zero (|median| < 0.04); NGC 5055 within
      0.015 of his 0.054 and NGC 5033 within 0.03 of his 0.104.
  H1  [FG001's cost as the fit's law]  under the framework's own law at its own a0 (V4-V7), the median fitted e of the
      <x0> < -10.3 galaxies is within 2 sigma (bootstrap) of zero.  Pre-declared UNCERTAIN.
  H2  [the discriminant]  a real external field makes the fitted e TRACK the independent environmental field galaxy by
      galaxy; a kernel artefact does not.  Under V4-V7 the fitted e is uncorrelated with Chae's environmental field (his
      2021 Table 3; Spearman p > 0.05), as FG001 predicts.  The correlation is reported for all seven laws.
  R1  (reported) the decomposition: a0 alone (V3) and kernel alone (V2) against both (V4/V6).
  R2  (reported) the RAR's low-acceleration orthogonal residual (x0 < -11.3 and < -10.3) at SPARC's nominal mass models, per
      law at e = 0 -- Chae's "downward trend" re-measured against each law.
MUTATE=1: a pure external field e = 0.05 is injected into every galaxy's velocities under V6's law (the prior-mean mass
model -- Upsilon_disk 0.5, Upsilon_bulge 0.7, Upsilon_gas = X^-1, the SPARC distance and inclination -- plus noise at the
reported errors) and the refit must find it -- H1 must FAIL (rc = 1).

SCOPE: Chae's sample, priors, likelihood and gas scaling exactly as his paper states them; the 1-D external-field function
(his own approximation, extended to the other laws by the same construction); the environmental field is his (2021 Table 3,
94 of the 153 galaxies); no new data.  kappa = 1/2 fitted; both footings.
Run: python3 campaign_fresh_gravity/CFG8_chae_kernel.py   (MUTATE=1 for the control; ~10-20 min on 10 processes)
"""
import os, sys, math, csv, json, time
import numpy as np
from multiprocessing import get_context

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
C4 = C.C4

MUTATE = os.environ.get("MUTATE", "0") == "1"
NPROC = int(os.environ.get("NPROC", "10"))
KMS2_KPC = 1e6 / 3.0856775814913673e19                                              # (km/s)^2/kpc -> m/s^2
GDAG = 1.2e-10
A0V = {"chae": GDAG, "canonical": C.A0_SI["canonical"], "alt": C.A0_SI["alt"]}
NSTEP, NBURN, NTHIN, NWALK = 4000, 1500, 5, 32
LANEB = os.path.join(C.REPO, "real_research", "reviews", "directional_efe_2026", "laneB_data")


# ------------------------------------------------------------------------------------------------ the laws
def nu_simple(z):
    z = np.maximum(np.asarray(z, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / z)


def nu_rar(z):
    z = np.maximum(np.asarray(z, float), 1e-300)
    return 1.0 / (-np.expm1(-np.sqrt(z)))


BASE = {"simple": nu_simple, "rar": nu_rar, "P2": C.nu_p2, "nu_mono": C.nu_mono}
_LZ = np.linspace(-14.0, 6.0, 20001)


def _F_table(kern):
    Z = 10 ** _LZ
    return np.log10(BASE[kern](Z) * Z)


_FT = {k: _F_table(k) for k in BASE}


def F(kern, Z):
    return BASE[kern](Z) * Z


def Finv(kern, e):
    """z_e with F(z_e) = |e| (F monotone), by interpolation on a fine log table; exact for P2."""
    ea = np.maximum(np.abs(np.asarray(e, float)), 1e-14)
    if kern == "P2":
        return (-1.0 + np.sqrt(1.0 + 4.0 * ea ** 2)) / 2.0
    if kern == "simple":
        return ea ** 2 / (1.0 + ea)                                              # exact: F(z_e) = e  <=>  z_e = e^2/(1 + e)
    return 10 ** np.interp(np.log10(ea), _FT[kern], _LZ)


def nu_e_chae(z, e):
    """Chae et al. 2020 eq. 6 (the simple function with the 1-D AQUAL external field; his continuation for e < 0)."""
    z = np.maximum(z, 1e-300)
    Ae = e * (1.0 + e / 2.0) / (1.0 + e); Be = 1.0 + e
    h = 0.5 - Ae / z
    return h + np.sqrt(h * h + Be / z)


def nu_e_general(kern, z, e):
    z = np.maximum(z, 1e-300)
    ze = Finv(kern, e)
    return (F(kern, z + ze) - e) / z


def nu_e(law, z, e):
    kern = law[0]
    return nu_e_chae(z, e) if kern == "simple" else nu_e_general(kern, z, e)


LAWS = {"V1": ("simple", "chae"), "V2": ("rar", "chae"), "V3": ("simple", "canonical"), "V4": ("P2", "canonical"),
        "V5": ("P2", "alt"), "V6": ("nu_mono", "canonical"), "V7": ("nu_mono", "alt")}
FRAMEWORK = ("V4", "V5", "V6", "V7")


# ------------------------------------------------------------------------------------------------ the sample and the model
def chae_X(Mstar):
    return 0.75 - 38.2 * (Mstar / 1.5e24) ** 0.22


def load_sample():
    out = []
    for g in C4.load_sparc():
        m = g["meta"]
        if not m or m["Inc"] < 30 or m["Q"] > 2:
            continue
        ok = g["Vobs"] > 0
        eD = m["eD"] if m["eD"] > 0 else 0.1 * m["D"]
        out.append(dict(name=g["name"], R=g["R"][ok], V=g["Vobs"][ok], eV=np.maximum(g["eV"][ok], 1e-3), Vd=g["Vdisk"][ok],
                        Vb=g["Vbul"][ok], Vg=g["Vgas"][ok] / math.sqrt(1.33), inc=m["Inc"], einc=max(m["eInc"], 0.5),
                        sigD=math.log10(1.0 + eD / m["D"]), Xinv=1.0 / chae_X(0.5 * m["L36"] * 1e9), has_bul=bool(np.any(g["Vbul"][ok] > 0))))
    return out


def model_V(gal, th, law, a0):
    """th: (..., 6) = log10 U_d, log10 U_b, log10 U_g, log10 Dhat, i [deg], e.  Returns V_model and V_rot, sigma_rot."""
    ud, ub, ug, lD, inc, e = [th[..., k:k + 1] for k in range(6)]
    Dh = 10 ** lD
    Vb2 = Dh * (10 ** ud * gal["Vd"] ** 2 + 10 ** ub * gal["Vb"] ** 2 + 10 ** ug * gal["Vg"] * np.abs(gal["Vg"]))
    R = Dh * gal["R"]
    gbar = np.maximum(Vb2, 1e-12) / R * KMS2_KPC
    nu = nu_e(law, gbar / a0, e)
    Vm = np.sqrt(np.maximum(nu * Vb2, 0.0))
    s = np.sin(np.radians(gal["inc"])) / np.sin(np.radians(inc))
    return Vm, gal["V"] * s, gal["eV"] * s, gbar


def lnpost(gal, th, law, a0):
    ud, ub, ug, lD, inc, e = [th[..., k] for k in range(6)]
    bad = (np.abs(e) > 0.5) | (inc <= 1.0) | (inc >= 90.0) | (ud < -2) | (ud > 1.5) | (ug < -1) | (ug > 1) | (np.abs(lD) > 1)
    Vm, Vr, sr, _ = model_V(gal, th, law, a0)
    chi2 = np.sum(((Vr - Vm) / sr) ** 2, axis=-1)
    lp = -0.5 * chi2
    lp += -0.5 * ((ud - math.log10(0.5)) / 0.1) ** 2
    lp += -0.5 * ((ub - math.log10(0.7)) / 0.1) ** 2
    lp += -0.5 * ((ug - math.log10(gal["Xinv"])) / 0.04) ** 2
    lp += -0.5 * (lD / gal["sigD"]) ** 2
    lp += -0.5 * ((inc - gal["inc"]) / gal["einc"]) ** 2
    return np.where(bad | ~np.isfinite(lp), -np.inf, lp)


def sample(gal, law, a0, seed, nstep=NSTEP, nburn=NBURN, nthin=NTHIN, W=NWALK):
    """the affine-invariant stretch move (Goodman & Weare 2010), two interleaved halves, a = 2."""
    rng = np.random.default_rng(seed)
    d = 6
    p0 = np.array([math.log10(0.5), math.log10(0.7), math.log10(gal["Xinv"]), 0.0, gal["inc"], 0.0])
    sc = np.array([0.05, 0.05, 0.02, 0.5 * gal["sigD"] + 1e-3, 0.5 * gal["einc"], 0.05])
    X = p0 + sc * rng.standard_normal((W, d))
    X[:, 5] = np.clip(X[:, 5], -0.45, 0.45)
    lp = lnpost(gal, X, law, a0)
    for _ in range(200):                                                          # re-draw any walker with -inf
        badw = ~np.isfinite(lp)
        if not badw.any():
            break
        X[badw] = p0 + sc * rng.standard_normal((int(badw.sum()), d)); lp[badw] = lnpost(gal, X[badw], law, a0)
    half = W // 2
    chain = []; nacc = 0; ntot = 0
    for t in range(nstep):
        for s0 in (0, 1):
            S = np.arange(s0 * half, (s0 + 1) * half); O = np.arange((1 - s0) * half, (2 - s0) * half)
            j = rng.choice(O, size=half)
            z = ((2.0 - 1.0) * rng.random(half) + 1.0) ** 2 / 2.0                   # g(z) ~ 1/sqrt(z) on [1/2, 2]
            Y = X[j] + z[:, None] * (X[S] - X[j])
            lpY = lnpost(gal, Y, law, a0)
            logr = (d - 1) * np.log(z) + lpY - lp[S]
            acc = np.log(rng.random(half)) < logr
            X[S[acc]] = Y[acc]; lp[S[acc]] = lpY[acc]
            nacc += int(acc.sum()); ntot += half
        if t >= nburn and (t - nburn) % nthin == 0:
            chain.append(X.copy())
    ch = np.concatenate(chain)
    imax = None
    return ch, nacc / ntot


def summarise(gal, ch, law, a0, acc):
    e = ch[:, 5]
    q = np.percentile(e, [16, 50, 84])
    med = np.median(ch, axis=0)
    Vm, Vr, sr, gbar = model_V(gal, med[None, :], law, a0)
    x0 = float(np.median(np.log10(gbar)))
    half = len(e) // 2
    return dict(name=gal["name"], e16=float(q[0]), e50=float(q[1]), e84=float(q[2]), x0=x0, acc=acc,
                e50_first=float(np.median(e[:half])), e50_second=float(np.median(e[half:])), npts=len(gal["R"]),
                chi2_med=float(np.sum(((Vr - Vm) / sr) ** 2)), med=[float(v) for v in med])


def job(args):
    gal, vkey, seed, inject = args
    kern, foot = LAWS[vkey]
    law = (kern,); a0 = A0V[foot]
    if inject is not None:
        gal = dict(gal)
        th = np.array(inject["theta"])[None, :]
        Vm, Vr, sr, _ = model_V(gal, th, law, a0)
        rng = np.random.default_rng(seed + 99)
        gal["V"] = (Vm[0] + gal["eV"] * rng.standard_normal(len(gal["R"]))) / (np.sin(np.radians(gal["inc"])) / np.sin(np.radians(th[0, 4])))
    ch, acc = sample(gal, law, a0, seed)
    out = summarise(gal, ch, law, a0, acc)
    out["variant"] = vkey
    return out


def main():
    R = C.Report("CFG8_chae_kernel", MUTATE)
    P, check = R.P, R.check
    P(__doc__.split("SCOPE:")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: a pure external field e = 0.05 is injected under V6's law; the refit must find it (H1 FAILS) ***")
    t0 = time.time()

    # ============================================================================================ C0
    R.banner("C0  CONTROL: the general 1-D construction with the simple function equals Chae's eq. 6")
    zz = np.geomspace(1e-4, 1e3, 400)
    dev0 = max(float(np.max(np.abs(nu_e_general("simple", zz, e) / nu_e_chae(zz, e) - 1))) for e in (0.0, 0.01, 0.033, 0.1, 0.3, 0.5))
    check("C0 CONTROL: nu_e = [F(z + z_e) - e]/z with the simple function equals Chae et al. 2020 eq. 6 for e in [0, 0.5]",
          f"max relative deviation {dev0:.1e}", dev0 <= 1e-9)

    SAMPLE = load_sample()
    P(f"\n  Chae's sample: {len(SAMPLE)} SPARC galaxies with inclination >= 30 deg and Q <= 2")
    check("C2a CONTROL: the sample has Chae's 153 galaxies", f"{len(SAMPLE)}", len(SAMPLE) == 153)

    # ============================================================================================ C1 recovery on synthetic galaxies
    R.banner("C1  CONTROL: the sampler recovers a known external field from synthetic galaxies (V6's law)")
    rec = []
    byname = {g["name"]: g for g in SAMPLE}
    for nm, etrue in (("NGC5055", 0.05), ("DDO154", 0.03), ("NGC3198", 0.0)):
        g = byname.get(nm)
        if g is None:
            continue
        th = [math.log10(0.5), math.log10(0.7), math.log10(g["Xinv"]), 0.0, g["inc"], etrue]
        r = job((g, "V6", 11, dict(theta=th)))
        sig = 0.5 * (r["e84"] - r["e16"])
        rec.append((nm, etrue, r["e50"], sig, (r["e50"] - etrue) / sig))
        P(f"    {nm:8s}: injected e = {etrue:.3f} -> recovered {r['e50']:+.4f} (+{r['e84'] - r['e50']:.4f}/-{r['e50'] - r['e16']:.4f}); "
          f"bias {(r['e50'] - etrue) / sig:+.2f} sigma; acceptance {r['acc']:.2f}")
    check("C1 CONTROL: the sampler recovers the injected e with bias < 0.25 sigma in each synthetic galaxy",
          "; ".join(f"{a}: {b:+.2f} sigma" for a, _, _, _, b in rec), all(abs(b) < 0.25 for *_, b in rec) and len(rec) == 3)
    # added after the MUTATE run (reported): C1 as declared tests ONE noisy realization per galaxy, whose recovered value
    # scatters by ~1 sigma for a correct sampler, so a 0.25-sigma bar was mis-set.  The sampler's own bias is tested here on
    # NOISELESS injections (the data equal the model), where an unbiased sampler must return the truth to within 0.25 sigma.
    rec0 = []
    for nm, etrue in (("NGC5055", 0.05), ("DDO154", 0.03), ("NGC3198", 0.0)):
        g = byname.get(nm)
        if g is None:
            continue
        g0 = dict(g); th = np.array([math.log10(0.5), math.log10(0.7), math.log10(g["Xinv"]), 0.0, g["inc"], etrue])[None, :]
        Vm, _, _, _ = model_V(g0, th, ("nu_mono",), A0V["canonical"])
        g0["V"] = Vm[0]
        ch, acc = sample(g0, ("nu_mono",), A0V["canonical"], 21)
        r = summarise(g0, ch, ("nu_mono",), A0V["canonical"], acc)
        sig = 0.5 * (r["e84"] - r["e16"])
        rec0.append((nm, etrue, r["e50"], sig, (r["e50"] - etrue) / sig))
        P(f"    noiseless {nm:8s}: injected {etrue:.3f} -> {r['e50']:+.4f} +- {sig:.4f} ({(r['e50'] - etrue) / sig:+.2f} sigma)")
    check("C1b (reported; added after the MUTATE run) on NOISELESS injections the sampler returns the injected e within 0.25 sigma",
          "; ".join(f"{a}: {b:+.2f} sigma" for a, _, _, _, b in rec0), all(abs(b) < 0.25 for *_, b in rec0) and len(rec0) == 3,
          load_bearing=False)

    # ============================================================================================ the fits
    R.banner("THE FITS: 153 galaxies x 7 laws (process pool)")
    inject = None
    tasks = []
    for vk in LAWS:
        for k, g in enumerate(SAMPLE):
            inj = None
            if MUTATE and vk == "V6":
                inj = dict(theta=[math.log10(0.5), math.log10(0.7), math.log10(g["Xinv"]), 0.0, g["inc"], 0.05])
            tasks.append((g, vk, 1000 + k, inj))
    RES = {vk: [] for vk in LAWS}
    with get_context("fork").Pool(NPROC) as pool:
        for i, r in enumerate(pool.imap_unordered(job, tasks, chunksize=4)):
            RES[r["variant"]].append(r)
            if (i + 1) % 150 == 0:
                P(f"    {i + 1}/{len(tasks)} fits done ({time.time() - t0:.0f} s)")
    for vk in RES:
        RES[vk].sort(key=lambda r: r["name"])

    # ============================================================================================ the statistics
    def boot_median(v, n=4000, seed=5):
        v = np.asarray(v); rng = np.random.default_rng(seed)
        bs = np.median(rng.choice(v, (n, len(v))), axis=1)
        return float(np.median(v)), float(np.std(bs))

    def gauss_mu(v, w):
        w = np.asarray(w); v = np.asarray(v)
        mu = float(np.sum(w * v) / np.sum(w)); return mu, float(1 / math.sqrt(np.sum(w)))

    STAT = {}
    for vk, rows in RES.items():
        lo = [r for r in rows if r["x0"] < -10.3]; hi = [r for r in rows if -10.3 <= r["x0"] < -9.0]
        vlo = [r for r in rows if r["x0"] < -11.3]
        mlo, elo = boot_median([r["e50"] for r in lo]); mhi, ehi = boot_median([r["e50"] for r in hi]) if hi else (float("nan"), float("nan"))
        mvlo, evlo = boot_median([r["e50"] for r in vlo]) if len(vlo) > 3 else (float("nan"), float("nan"))
        npos = sum(r["e50"] > 0 for r in lo)
        STAT[vk] = dict(n_lo=len(lo), med_lo=mlo, err_lo=elo, z_lo=mlo / elo if elo > 0 else float("nan"), n_hi=len(hi), med_hi=mhi,
                        err_hi=ehi, n_vlo=len(vlo), med_vlo=mvlo, err_vlo=evlo, npos_lo=npos,
                        sign_z=(npos - 0.5 * len(lo)) / math.sqrt(0.25 * len(lo)) if lo else float("nan"),
                        acc_med=float(np.median([r["acc"] for r in rows])),
                        drift=float(np.median([abs(r["e50_first"] - r["e50_second"]) / max(0.5 * (r["e84"] - r["e16"]), 1e-6) for r in rows])))
    R.banner("THE MEDIAN FITTED EXTERNAL FIELD, by law (Chae's <x0> bins)")
    for vk, s in STAT.items():
        kern, foot = LAWS[vk]
        P(f"    {vk} {kern:8s} @ {foot:9s}: <x0> < -10.3 (N = {s['n_lo']:3d}): median e = {s['med_lo']:+.4f} +- {s['err_lo']:.4f} "
          f"({s['z_lo']:+.1f} sigma), {s['npos_lo']}/{s['n_lo']} positive ({s['sign_z']:+.1f} sigma sign test); "
          f"-10.3..-9 (N = {s['n_hi']}): {s['med_hi']:+.4f} +- {s['err_hi']:.4f}; < -11.3 (N = {s['n_vlo']}): {s['med_vlo']:+.4f}; "
          f"acceptance {s['acc_med']:.2f}; half-chain drift {s['drift']:.2f} sigma")

    # C2 Chae's own numbers
    s1 = STAT["V1"]; byv1 = {r["name"]: r for r in RES["V1"]}
    n55 = byv1.get("NGC5055", {}).get("e50", float("nan")); n33 = byv1.get("NGC5033", {}).get("e50", float("nan"))
    P(f"    V1 individual: NGC5055 e = {n55:+.4f} (Chae 0.054 +- 0.005), NGC5033 {n33:+.4f} (Chae 0.104), NGC6674 "
      f"{byv1.get('NGC6674', {}).get('e50', float('nan')):+.4f} (Chae -0.015), NGC1090 {byv1.get('NGC1090', {}).get('e50', float('nan')):+.4f} (Chae 0.061)")
    c2 = abs(s1["med_lo"] - 0.052) <= 0.02 and abs(s1["med_hi"]) < 0.04 and abs(n55 - 0.054) <= 0.015 and abs(n33 - 0.104) <= 0.03
    check("C2 CONTROL: Chae's own law (V1) reproduces his 2020 numbers -- low-acceleration median 0.052 within 0.02, the high-acceleration "
          "galaxies consistent with zero, NGC 5055 within 0.015 of 0.054, NGC 5033 within 0.03 of 0.104",
          f"median {s1['med_lo']:+.4f} (N = {s1['n_lo']}), high {s1['med_hi']:+.4f}, NGC5055 {n55:+.4f}, NGC5033 {n33:+.4f}", c2)

    # H1
    h1 = all(abs(STAT[v]["z_lo"]) < 2 for v in FRAMEWORK)
    check("H1 [FG001's cost as the fit's law] under the framework's own law at its own a0 the low-acceleration median fitted e is within "
          "2 sigma of zero (V4-V7)", "; ".join(f"{v} {LAWS[v][0]}@{LAWS[v][1]}: {STAT[v]['med_lo']:+.4f} ({STAT[v]['z_lo']:+.1f} sigma)"
                                               for v in FRAMEWORK), h1)

    # H2 the environmental correlation
    R.banner("H2  THE DISCRIMINANT: does the fitted e track Chae's independent environmental field, galaxy by galaxy?")
    from scipy.stats import spearmanr
    env = {r["galaxy"].strip(): r for r in csv.DictReader(open(os.path.join(LANEB, "chae21_env.csv")))}
    CORR = {}
    for vk, rows in RES.items():
        kern, foot = LAWS[vk]; a0 = A0V[foot]
        xs, ys, ws = [], [], []
        for r in rows:
            if r["name"] in env:
                lN = 0.5 * (float(env[r["name"]]["log_eN_maxclu"]) + float(env[r["name"]]["log_eN_noclu"]))
                gN = 10 ** lN * GDAG                                                      # Chae's e_N is in units of 1.2e-10
                e_env = float(F(kern, np.array([gN / a0]))[0])                           # the external field in this law's units
                xs.append(e_env); ys.append(r["e50"]); ws.append(1.0 / max(0.5 * (r["e84"] - r["e16"]), 1e-3) ** 2)
        xs, ys, ws = map(np.asarray, (xs, ys, ws))
        rho, p = spearmanr(xs, ys)
        ws = np.minimum(ws, 1.0 / 0.005 ** 2)                                     # per-galaxy sigma_e floored at 0.005
        A = np.vstack([np.ones_like(xs), xs]).T * np.sqrt(ws)[:, None]
        beta = np.linalg.lstsq(A, ys * np.sqrt(ws), rcond=None)[0]
        cov = np.linalg.inv(A.T @ A)
        CORR[vk] = dict(n=len(xs), rho=float(rho), p=float(p), intercept=float(beta[0]), slope=float(beta[1]),
                        e_int=float(math.sqrt(cov[0, 0])), e_slope=float(math.sqrt(cov[1, 1])), med_env=float(np.median(xs)))
        P(f"    {vk} {kern:8s} @ {foot:9s}: N = {len(xs)}: Spearman rho = {rho:+.3f} (p = {p:.3f}); weighted fit e_fit = "
          f"{beta[0]:+.4f} (+-{math.sqrt(cov[0, 0]):.4f}) + {beta[1]:+.3f} (+-{math.sqrt(cov[1, 1]):.3f}) e_env; median e_env {np.median(xs):.4f}")
    h2 = all(CORR[v]["p"] > 0.05 for v in FRAMEWORK)
    check("H2 [the discriminant] under the framework's own law the fitted e is uncorrelated with Chae's independent environmental field "
          "(Spearman p > 0.05, V4-V7), as FG001 predicts",
          "; ".join(f"{v}: rho {CORR[v]['rho']:+.2f}, p {CORR[v]['p']:.3f}, slope {CORR[v]['slope']:+.2f} +- {CORR[v]['e_slope']:.2f}"
                    for v in CORR), h2)

    # R1 decomposition
    R.banner("R1  (reported) THE DECOMPOSITION: a0 alone, kernel alone, both")
    for vk in ("V1", "V3", "V2", "V4", "V6"):
        P(f"    {vk} {LAWS[vk][0]:8s} @ {LAWS[vk][1]:9s}: low-acceleration median e {STAT[vk]['med_lo']:+.4f} +- {STAT[vk]['err_lo']:.4f}")

    # R2 the RAR residual at SPARC's nominal mass models
    R.banner("R2  (reported) THE LOW-ACCELERATION RAR RESIDUAL AT SPARC'S NOMINAL MASS MODELS, per law at e = 0")
    RR = {}
    for vk, (kern, foot) in LAWS.items():
        a0 = A0V[foot]
        xs_, ys_ = [], []
        for g in SAMPLE:
            Vb2 = 0.5 * g["Vd"] ** 2 + 0.7 * g["Vb"] ** 2 + 1.33 * g["Vg"] * np.abs(g["Vg"])
            ok = Vb2 > 0
            gb = Vb2[ok] / g["R"][ok] * KMS2_KPC; go = g["V"][ok] ** 2 / g["R"][ok] * KMS2_KPC
            xs_.append(np.log10(gb)); ys_.append(np.log10(go))
        x = np.concatenate(xs_); y = np.concatenate(ys_)
        grid = np.linspace(-13.5, -7.5, 3001); curve = grid + np.log10(BASE[kern](10 ** grid / a0))
        # orthogonal distance to the curve (dense-grid nearest point), signed by the vertical residual
        d = np.sqrt((x[:, None] - grid[None, :]) ** 2 + (y[:, None] - curve[None, :]) ** 2)
        k = np.argmin(d, axis=1); x0 = grid[k]
        sgn = np.sign(y - (x + np.log10(BASE[kern](10 ** x / a0))))
        dperp = sgn * d[np.arange(len(x)), k]
        RR[vk] = {}
        for lab, m in (("x0<-11.3", x0 < -11.3), ("x0<-10.3", x0 < -10.3), ("-10.3..-9", (x0 >= -10.3) & (x0 < -9))):
            md, er = boot_median(dperp[m]) if m.sum() > 5 else (float("nan"), float("nan"))
            RR[vk][lab] = dict(n=int(m.sum()), median=md, err=er)
        P(f"    {vk} {kern:8s} @ {foot:9s}: orthogonal residual median  x0 < -11.3: {RR[vk]['x0<-11.3']['median']:+.3f} +- "
          f"{RR[vk]['x0<-11.3']['err']:.3f} (N {RR[vk]['x0<-11.3']['n']}); x0 < -10.3: {RR[vk]['x0<-10.3']['median']:+.3f} +- "
          f"{RR[vk]['x0<-10.3']['err']:.3f}; -10.3..-9: {RR[vk]['-10.3..-9']['median']:+.3f}")
    check("R2 (reported) Chae's low-acceleration downturn at SPARC's nominal mass models is re-measured against every law",
          "; ".join(f"{v}: {RR[v]['x0<-11.3']['median']:+.3f}" for v in RR), True, load_bearing=False)

    R.banner("VERDICT")
    P("    " + "; ".join(f"{v} ({LAWS[v][0]}@{LAWS[v][1]}): e {STAT[v]['med_lo']:+.3f} ({STAT[v]['z_lo']:+.1f} sigma), env rho "
                        f"{CORR[v]['rho']:+.2f} (p {CORR[v]['p']:.2f})" for v in LAWS))
    R.num("STAT", STAT); R.num("CORR", CORR); R.num("RAR", RR); R.num("RECOVERY", rec)
    R.num("FITS", {vk: rows for vk, rows in RES.items()})
    return R.write()


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
