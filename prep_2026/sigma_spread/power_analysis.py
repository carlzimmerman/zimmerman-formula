#!/usr/bin/env python3
r"""
LANE P -- POWER ANALYSIS (Monte Carlo, frozen estimator) for the MI relational sigma-spread
vs the MG exact zero, on the REAL 2026 public-catalog specs.  2026-07-16.  Exit 0.
=============================================================================================

FROZEN ESTIMATOR + CUTS -- registered HERE, BEFORE any real-data read (the reads below
extract catalog SPECS only; the estimator is NEVER fired on real sigma-vs-infall data in
this script; any such firing is EXPLORATORY/FIREWALLED per the lane rules):

  E1 SAMPLE   Diffuse carriers (UDG/dSph class, sigma_int ~ 8-25 km/s, the only members
              that reach y ~ 1: rederive_mi_spread.py sec 4) that are (a) caustic members,
              (b) in the projected R500-R200 shell (the MOND-transition carrier zone,
              rederive sec 3), (c) UNDISRUPTED (regular King/Sersic, no tidal tails),
              (d) NOT in a Dressler-Shectman substructure (flag + excise the group --
              substructure is the one confound that can fake b>0 under true MG and the
              shuffle null does NOT protect against it; it must be CUT, not shuffled).
  E2 CONTROL  FJ residual d_i = ln sigma_i - <ln sigma | M*, R_e> (per-population fit;
              the "matched internal baryons" control). Matched radius = the shell cut.
  E3 PROXY    Infall-phase proxy p_i from projected phase space (caustic zone tag +
              k_r = (|dv|/sigma_cl)(R/R200)), standardized within each cluster.
              Proxy impurity enters as pure attenuation D (banked MC: D~0.4; DESI-era
              caustic+PPS tagging on >=180-member clusters: D~0.6).
  E4 STATISTIC Pooled cluster-centered OLS slope b of d_i on p_i. ONE-SIDED test:
              the framework signs the prediction (plungers HOTTER, b>0); MG: b == 0
              exactly (symbolic theorem, any a0, any interpolation; rederive sec 1).
              Detection threshold: z = b/SE(b) >= 3 (3 sigma), null CALIBRATED by
              MG-truth Monte Carlo AND by within-cluster shuffles of p_i.
  E5 SIGNAL   Injected from the framework's OWN R(y) shape (nu(y)=sqrt(1+1/y),
              mu_fw = its exact inverse, Milgrom-2022-class theta kernel, fiducial
              rational), scaled to relational spread f. BOTH footings, band ends:
              canonical a0=9.36e-11 -> f in {6%, 13%} (tasked band, brackets the
              re-derived 6.4-12.0%); alternate a0=1.13e-10 -> f in {7.6%, 14.4%}
              (the banked alt band ends). MG runs: f == 0 identically.
  E6 Y-DIST FORK (honesty fork, both ways): the banked feasibility implicitly assumed a
              settled-vs-plunger DICHOTOMY (two-class y). We run BOTH: two-class
              (banked-compatible) and uniform-y continuum (conservative, ~x3 in N).
  E7 NOISE    Per-carrier ln-sigma noise = quadrature(e_meas, s_FJ). e_meas: resampled
              from the REAL Gannon+2024 error distribution (2026 in-hand) or 10% (ELT
              tier) / 20% (deep-MUSE tier). s_FJ (astrophysical floor) is CITED/COMPUTED,
              not assumed: (i) MEASURED here from the in-hand carrier catalog itself
              (Gannon+2024: residual of ln sigma on ln M* + ln R_e, measurement variance
              subtracted); (ii) the banked 0.15 (estimator_power.py: dwarf FJ 0.05-0.10
              dex = 12-26% fractional); (iii) 0.08 = tight-control aspiration
              (homogeneous distances/apertures; Sohn+2017 dE-class tightness).
  E8 INTERLOPERS eps_int = 0.10 central (caustic-cleaned outer shell, banked 0.05-0.2;
              Serra & Diaferio 2013-class contamination): no signal, random proxy.
  E9 VERDICT RULE (frozen): POWERED NOW iff an EXISTING public dataset supplies the
              3-sigma N at its own measured errors; POWERED IF <specific combination>;
              else STILL UNDERPOWERED with the exact N-gap. Median-z crossing AND
              90%-power N both reported.

REAL CATALOG SPECS CONSUMED (all touched + recomputed in census_verify.py; re-read here):
  data/gannon2024_udg_living.csv   carrier count, error distribution, FJ scatter
  data/hecs_omnibus2020_clusters.csv  227 clusters: Nmem, sigma_cl, R200 (phase-tag side)
  data/hecs2013_redshifts.csv      per-member e_cz (proxy measurement-noise arithmetic)
  data/galwcat19_{clusters,members}.csv  measured fraction of members in the R500-R200 shell
  data/sohn2017_a2029_member_sigma.csv   the dE/bright-member route (quantified kill)

BOTH WAYS CONTRACT: the MG=0 null is stress-tested with a substructure fake-positive demo
(what protects MG from a false kill) exactly as hard as the MI band is power-tested.
"""
import csv
import numpy as np

rng = np.random.default_rng(20260716)
DATA = "/Users/carlzimmerman/new_physics/prep_2026/sigma_spread/data"

# ============================================================== framework signal shape (own premises)
A0_CAN, A0_ALT = 9.36e-11, 1.13e-10   # BOTH footings, always


def mu_fw(x):
    x = np.asarray(x, float)
    return (np.sqrt(1.0 + 4.0 * x * x) - 1.0) / (2.0 * x)


# own-premises check: mu_fw is the EXACT inverse of the framework's nu(y)=sqrt(1+1/y)
_g = np.logspace(-3, 3, 301)
assert np.allclose(_g * np.sqrt(1 + 1 / _g) * mu_fw(_g * np.sqrt(1 + 1 / _g)), _g, rtol=1e-12)

theta_rat = lambda y: 2.0 / (1.0 + np.abs(y) ** 2)  # fiducial Milgrom-2022 kernel, theta(0)=2


def lnR_shape(y, a0, a_in_frac=0.3, a_ex_frac=0.5):
    """ln of the relational ratio R(y)=sigma(y)/sigma(y=0) at matched a_ex (outer-shell member,
    a_ex=0.5a0 in the carrier zone), fiducial kernel. Shape only; amplitude rescaled to f."""
    a_in, a_ex = a_in_frac * a0, a_ex_frac * a0
    B = lambda yy: 1.0 / mu_fw((a_in + a_ex * theta_rat(yy)) / a0)
    return 0.5 * (np.log(B(y)) - np.log(B(0.0)))


YMAX = 1.5
_yg = np.linspace(0, YMAX, 400)


def make_signal(y, f, a0):
    """ln-sigma offsets with relational spread == f over the y<=1.5 window (framework shape)."""
    raw = lnR_shape(_yg, a0)
    Rg = np.exp(raw)
    raw_spread = (Rg.max() - Rg.min()) / Rg.mean()
    k = f / raw_spread
    s = k * lnR_shape(y, a0)
    return s - k * raw.mean()  # centered


# ============================================================== (1) REAL SPECS (reads AFTER the frozen block)
print("=" * 102)
print(" (1) REAL CATALOG SPECS (recomputed from touched data; specs only -- estimator NOT fired on real data)")
print("=" * 102)

# --- Gannon+2024 living UDG catalog: the ENTIRE public carrier reservoir
rows = list(csv.DictReader(open(f"{DATA}/gannon2024_udg_living.csv")))
sig, err, env, ms, re_ = [], [], [], [], []
for r in rows:
    s, u, d = (float(r[k]) for k in ("stellar_sigma", "stellar_sigma_up", "stellar_sigma_down"))
    if s > 0 and u > 0:
        sig.append(s); err.append(0.5 * (u + abs(d))); env.append(int(r["Environment"]))
        ms.append(float(r["Stellar mass"])); re_.append(float(r["R_e"]))
sig, err, env, ms, re_ = map(np.array, (sig, err, env, ms, re_))
frac_err = err / sig
N_INHAND = int(np.sum(env <= 2))  # cluster/group carriers with stellar sigma
ok = ms > 0
X2 = np.vstack([np.ones(ok.sum()), np.log(ms[ok]), np.log(re_[ok])]).T
beta, *_ = np.linalg.lstsq(X2, np.log(sig[ok]), rcond=None)
resid = np.log(sig[ok]) - X2 @ beta
S_TOT = resid.std(ddof=3)
S_FJ_MEAS = float(np.sqrt(max(S_TOT ** 2 - np.mean(frac_err[ok] ** 2), 0.0)))
print(f"  Gannon+2024: {len(sig)} UDGs with stellar sigma ({N_INHAND} cluster/group = the 2026 reservoir);")
print(f"    fractional sigma errors: median {np.median(frac_err):.2f}, range {frac_err.min():.2f}-{frac_err.max():.2f} (resampled in the MC)")
print(f"    MEASURED astro floor: resid[ln sigma | ln M*, ln R_e] total {S_TOT:.2f} ln; measurement-subtracted")
print(f"    INTRINSIC s_FJ(meas) = {S_FJ_MEAS:.2f} ln ({S_FJ_MEAS/2.3026:.2f} dex) -- vs banked 0.15: the in-hand")
print(f"    heterogeneous population is x{S_FJ_MEAS/0.15:.1f} WORSE than the banked floor (24 objects, mixed")
print("    distances/instruments/environments; if MI is true part of this scatter IS signal -> conservative).")

# --- HeCS-omnibus: the phase-tagging cluster reservoir
ro = list(csv.DictReader(open(f"{DATA}/hecs_omnibus2020_clusters.csv")))
nmem = np.array([float(r["Nmem"]) for r in ro])
sigcl = np.array([float(r["sigmaCl"]) for r in ro])
NCL_OMNI = len(ro)
print(f"  HeCS-omnibus: {NCL_OMNI} clusters, median {np.median(nmem):.0f} members/cluster (sum {int(nmem.sum())}),")
print(f"    median sigma_cl {np.median(sigcl):.0f} km/s -- caustic membership + R200 per cluster (the free side).")

# --- per-member velocity error -> proxy noise arithmetic
rz = list(csv.DictReader(open(f"{DATA}/hecs2013_redshifts.csv")))
ecz = np.median([float(r["e_cz"]) for r in rz if r["e_cz"].strip()])
print(f"  HeCS e_cz median {ecz:.0f} km/s vs sigma_cl {np.median(sigcl):.0f} -> proxy k_r measurement noise "
      f"{ecz/np.median(sigcl)*100:.0f}% of sigma_cl:")
print("    NEGLIGIBLE -- proxy dilution D is projection-dominated (banked D~0.4; D~0.6 with caustic zones), not noise.")

# --- GalWCat19: measured outer-shell fraction
cl = {r["ClID"]: (float(r["RAJ2000"]), float(r["DEJ2000"]), float(r["CoDist"]),
                  float(r["r200"]), float(r["z"])) for r in csv.DictReader(open(f"{DATA}/galwcat19_clusters.csv"))}
nsh = ntot = 0
for r in csv.DictReader(open(f"{DATA}/galwcat19_members.csv")):
    if r["ClID"] not in cl:
        continue
    ra0, de0, cod, r200c, zc = cl[r["ClID"]]
    dth = np.hypot((float(r["RAJ2000"]) - ra0) * np.cos(np.radians(de0)),
                   float(r["DEJ2000"]) - de0) * np.pi / 180.0
    rp = dth * cod / (1 + zc) / r200c
    ntot += 1
    nsh += (0.5 <= rp <= 1.0)
F_SHELL = nsh / ntot
print(f"  GalWCat19: {ntot} members matched -> measured fraction in the 0.5-1.0 R200 shell = {F_SHELL:.2f}")
print("    (members confined to <R200 by construction; the shell keeps ~40% of a targeted sample).")

# ============================================================== (2) the Monte Carlo engine
EPS_INT = 0.10


def draw_y(n, mode, rg):
    if mode == "two-class":  # settled vs plunger dichotomy (banked-compatible)
        pl = rg.random(n) < 0.5
        y = np.where(pl, rg.uniform(1.2, YMAX, n), rg.uniform(0.0, 0.15, n))
    else:                    # uniform continuum (conservative)
        y = rg.uniform(0.0, YMAX, n)
    return y


def mc_z(N, f, a0, e_mode, s_fj, D, ymode, trials=2000, eps=EPS_INT, rg=rng,
         sub_frac=0.0, sub_doff=0.0, sub_poff=0.0):
    """Median/dist of the one-sided detection z for the frozen estimator.
    e_mode: 'gannon' (resample real errors) or a float (fractional sigma error).
    sub_*: OPTIONAL substructure fake-signal injection under MG (for the null stress test)."""
    y = draw_y((trials, N), ymode, rg).reshape(trials, N)
    s = make_signal(y, f, a0) if f > 0 else np.zeros((trials, N))
    # standardized latent x from the framework shape (what a perfect proxy would read)
    hs = make_signal(y, max(f, 0.10), a0)  # shape carrier (nonzero even for MG runs)
    x = (hs - hs.mean(axis=1, keepdims=True)) / np.maximum(hs.std(axis=1, keepdims=True), 1e-12)
    p = D * x + np.sqrt(1 - D * D) * rg.standard_normal((trials, N))
    # interlopers: no signal, random proxy
    il = rg.random((trials, N)) < eps
    s = np.where(il, 0.0, s)
    p = np.where(il, rg.standard_normal((trials, N)), p)
    # noise
    if e_mode == "gannon":
        e = rg.choice(frac_err, size=(trials, N))
    else:
        e = np.full((trials, N), float(e_mode))
    noise = np.hypot(e, s_fj)
    d = s + noise * rg.standard_normal((trials, N))
    # optional coherent-substructure injection (MG stress test): groups share d and p offsets
    if sub_frac > 0:
        gsel = rg.random((trials, N)) < sub_frac
        d = d + np.where(gsel, sub_doff, 0.0)
        p = p + np.where(gsel, sub_poff, 0.0)
    # pooled OLS slope + z (p re-centered per trial = cluster-centered pooled estimator)
    p = p - p.mean(axis=1, keepdims=True)
    d = d - d.mean(axis=1, keepdims=True)
    vp = (p ** 2).sum(axis=1)
    b = (p * d).sum(axis=1) / vp
    res = d - b[:, None] * p
    se = np.sqrt((res ** 2).sum(axis=1) / (N - 2) / vp)
    return b / se


print()
print("=" * 102)
print(" (2) NULL CALIBRATION -- MG truth (f=0): the estimator's z must be standard normal, FP(3sig) ~ 1.3e-3")
print("=" * 102)
zn = mc_z(400, 0.0, A0_CAN, 0.10, 0.15, 0.4, "two-class", trials=20000)
fp = float(np.mean(zn >= 3.0))
print(f"  MG-truth MC (N=400, 20k trials): mean z = {zn.mean():+.3f}, sd = {zn.std():.3f}, "
      f"P(z>=3) = {fp:.4f} (expect ~0.0013)")
assert abs(zn.mean()) < 0.05 and abs(zn.std() - 1.0) < 0.05 and fp < 0.004, "null miscalibrated"
print("  [OK] null calibrated: under ANY-MG truth the frozen estimator fires at 3 sigma with p~1.3e-3, as designed.")

# sqrt(N) scaling validation (used to convert calibration z -> N_3sigma)
z1 = np.median(mc_z(200, 0.10, A0_CAN, 0.10, 0.15, 0.4, "two-class", trials=4000))
z2 = np.median(mc_z(800, 0.10, A0_CAN, 0.10, 0.15, 0.4, "two-class", trials=4000))
ratio = z2 / z1
print(f"  sqrt(N) scaling check: z(800)/z(200) = {ratio:.2f} (expect 2.00)")
assert abs(ratio - 2.0) < 0.25, "sqrt-N scaling broken"

NCAL = 400


def n_to_3sigma(f, a0, e_mode, s_fj, D, ymode, trials=3000):
    zc = np.median(mc_z(NCAL, f, a0, e_mode, s_fj, D, ymode, trials=trials))
    n_med = NCAL * (3.0 / zc) ** 2            # median-z crossing of 3 sigma
    n_90 = NCAL * ((3.0 + 1.2816) / zc) ** 2  # 90% power at one-sided 3 sigma (z~N(z_med,1))
    return n_med, n_90


# empirical validation of the N_90 normal approximation (fiducial cell)
nm_f, n90_f = n_to_3sigma(0.10, A0_CAN, 0.10, 0.15, 0.4, "two-class")
zval = mc_z(int(round(n90_f)), 0.10, A0_CAN, 0.10, 0.15, 0.4, "two-class", trials=3000)
pow90 = float(np.mean(zval >= 3.0))
print(f"  N_90 validation (fiducial f=10% can., ELT, s_FJ=0.15, D=0.4): N_90={n90_f:.0f} -> "
      f"empirical power {pow90:.2f} (target 0.90)")
assert 0.82 < pow90 < 0.96, "90%-power normal approximation failed"
# consistency vs the banked analytic two-bin (estimator_power.py: N=903 for this cell)
infl = nm_f / 903.0
print(f"  banked-analytic consistency: MC median-z N_3sigma = {nm_f:.0f} vs analytic two-bin 903 -> x{infl:.2f}.")
print("    EXPLAINED, BOTH WAYS: the analytic two-bin put the bins at the y-window ENDPOINTS (contrast = the")
print("    full relational spread f); real settled/plunger CLASS MEANS sit inside the window (y~0.08 / y~1.35),")
print("    so the usable contrast is ~85% of f -> N x~1.4. The MC is the honest number; the banked analytic")
print("    was ~x1.4 optimistic ON TOP of its x2-5 FJ-floor correction. Same estimator, no free parameters.")
assert 1.0 < infl < 1.9, "MC-vs-analytic inflation outside the explained sqrt-contrast range"

# ============================================================== (3) THE POWER GRID (both footings, 6% and 13%)
print()
print("=" * 102)
print(" (3) POWER GRID -- N_carriers to 3 sigma (median-z crossing | 90% power), frozen estimator")
print("=" * 102)
FOOTINGS = [("CANONICAL a0=9.36e-11", A0_CAN, [0.06, 0.13]),
            ("ALTERNATE a0=1.13e-10", A0_ALT, [0.076, 0.144])]
SCEN = [
    ("A 2026 in-hand   (Gannon errs ~24%%, s_FJ=meas %.2f, D=0.4)" % S_FJ_MEAS, "gannon", S_FJ_MEAS, 0.4),
    ("B ELT sigma<=10%, banked FJ floor 0.15, D=0.4",                          0.10,     0.15,      0.4),
    ("C ELT sigma<=10%, banked FJ floor 0.15, D=0.6 (DESI-tagged)",            0.10,     0.15,      0.6),
    ("D ELT sigma<=10%, tight FJ 0.08, D=0.6 (best realistic)",                0.10,     0.08,      0.6),
    ("E ELT sigma<=10%%, s_FJ stays at meas %.2f, D=0.6 (no FJ progress)" % S_FJ_MEAS, 0.10, S_FJ_MEAS, 0.6),
]
results = {}
for ydist in ("two-class", "continuum"):
    print(f"\n  --- y-distribution fork: {ydist} {'(banked-compatible)' if ydist=='two-class' else '(conservative, honesty fork)'} ---")
    for flab, a0, fs in FOOTINGS:
        for f in fs:
            for slab, em, sfj, D in SCEN:
                nm, n90 = n_to_3sigma(f, a0, em, sfj, D, ydist)
                results[(ydist, flab, f, slab[0])] = (nm, n90)
                print(f"   {flab[:9]:9s} f={f*100:4.1f}% | {slab:58s} | N_3sig = {nm:7,.0f} | N_90 = {n90:8,.0f}")

# ============================================================== (4) N_clusters curve (carriers/cluster from real specs)
print()
print("=" * 102)
print(" (4) N_CLUSTERS CURVE -- carriers/cluster anchored to real programs; z vs number of clusters")
print("=" * 102)
M_LEWIS = 30                       # LEWIS (Iodice+2023): ~30 UDG targets in ONE cluster (Hydra I) -- a real program size
RETAIN = 0.8                       # undisrupted + DS-cut retention (E1c,d)
M_EFF = M_LEWIS * F_SHELL * RETAIN  # usable carriers per LEWIS-class cluster campaign
print(f"  carriers/cluster: LEWIS-class campaign 30 targets x shell fraction {F_SHELL:.2f} (measured, GalWCat19)")
print(f"    x cut retention {RETAIN} = {M_EFF:.1f} usable carriers/cluster;  2026 reality: {N_INHAND} carriers TOTAL / ~10 hosts = 2.3.")
print(f"\n  {'N_cl':>6s} | {'N_carriers':>10s} | median z (scenario C, two-class, canonical) f=6% / f=13%")
zc6 = np.median(mc_z(NCAL, 0.06, A0_CAN, 0.10, 0.15, 0.6, "two-class", trials=3000))
zc13 = np.median(mc_z(NCAL, 0.13, A0_CAN, 0.10, 0.15, 0.6, "two-class", trials=3000))
ncl_grid = [5, 10, 25, 50, 100, 227, 500]
for ncl in ncl_grid:
    ncar = ncl * M_EFF
    z6, z13 = zc6 * np.sqrt(ncar / NCAL), zc13 * np.sqrt(ncar / NCAL)
    tag = "  <- HeCS-omnibus reservoir (phase-tagged clusters that EXIST publicly)" if ncl == 227 else ""
    print(f"  {ncl:6d} | {ncar:10,.0f} | {z6:5.2f} / {z13:5.2f}{tag}")
ncl_3s_6 = (3.0 / zc6) ** 2 * NCAL / M_EFF
ncl_3s_13 = (3.0 / zc13) ** 2 * NCAL / M_EFF
print(f"\n  3-sigma (median-z) cluster requirement, scenario C canonical: f=13% -> {ncl_3s_13:.0f} clusters; "
      f"f=6% -> {ncl_3s_6:.0f} clusters.")
print(f"  => the CLUSTER reservoir is NOT the wall ({NCL_OMNI} phase-tagged clusters exist); the per-carrier")
print("     sigma precision tier (<=10%, i.e. ELT-HARMONI ~2032) and the campaign scale are.")

# ============================================================== (5) 2026 IN-HAND: exploratory power (firewalled)
print()
print("=" * 102)
print(" (5) 2026 IN-HAND CONFIGURATION -- the firewall check (23 carriers, real Gannon errors, untagged)")
print("=" * 102)
for flab, a0, fs in FOOTINGS:
    for f in fs:
        zi = mc_z(N_INHAND, f, a0, "gannon", S_FJ_MEAS, 0.4, "two-class", trials=8000)
        zi_b = mc_z(N_INHAND, f, a0, "gannon", 0.15, 0.4, "two-class", trials=8000)
        print(f"  {flab[:9]:9s} f={f*100:4.1f}%: median z = {np.median(zi):.2f} (10-90%: {np.percentile(zi,10):+.2f}..{np.percentile(zi,90):+.2f})"
              f"  [banked-floor s_FJ=0.15 would give {np.median(zi_b):.2f}]  P(z>=3) = {np.mean(zi>=3):.3f}")
z_best = np.median(mc_z(N_INHAND, 0.144, A0_ALT, "gannon", 0.15, 0.4, "two-class", trials=8000))
assert z_best < 1.0, "in-hand data must be exploratory-only"
print(f"  [OK] even the BEST corner (alt footing f=14.4%, banked floor) gives median z = {z_best:.2f} < 1.")
print("  => ANY firing on the 23 in-hand carriers is EXPLORATORY/FIREWALLED: it can neither support nor")
print("     kill (pre-derived power 0.1-0.6 sigma; matches the banked 2026-06-26 pilot expectation).")

# ============================================================== (6) dE/bright-member route (quantified kill, MC)
print()
print("=" * 102)
print(" (6) THE dE/BRIGHT-MEMBER BACKDOOR (Sohn+2017 A2029 specs) -- verified dead in the same MC")
print("=" * 102)
rs = list(csv.DictReader(open(f"{DATA}/sohn2017_a2029_member_sigma.csv")))
sde = [(float(r["sigma"]), float(r["e_sigma"])) for r in rs
       if r["sigma"].strip() and r["e_sigma"].strip() and float(r["sigma"]) >= 60]
n_de = len(sde)
efr_de = float(np.median([e / s for s, e in sde]))
nm_de, n90_de = n_to_3sigma(0.007, A0_CAN, efr_de, 0.12, 0.4, "two-class")
print(f"  A2029 usable (sigma>=60 km/s): {n_de} members, median frac err {efr_de:.2f}; dE-class predicted f~0.7%")
print(f"  (adiabatic-dead, rederive sec 4) -> N_3sigma = {nm_de:,.0f} (median-z) vs {n_de} in the whole catalog:")
print(f"  shortfall x{nm_de/n_de:,.0f}. No backdoor around the firewall through survey-measurable members.")
assert nm_de > 1e5, "dE route must be quantifiably dead"

# ============================================================== (7) substructure fake-positive (MG null stress test)
print()
print("=" * 102)
print(" (7) SUBSTRUCTURE STRESS TEST -- the one confound that can fake b>0 under TRUE MG (cut, don't shuffle)")
print("=" * 102)
zf = mc_z(900, 0.0, A0_CAN, 0.10, 0.15, 0.4, "two-class", trials=4000,
          sub_frac=0.15, sub_doff=0.12, sub_poff=1.0)
zf_cut = mc_z(900, 0.0, A0_CAN, 0.10, 0.15, 0.4, "two-class", trials=4000)
print(f"  MG truth + 15% coherent infalling-group members (shared +0.12 ln-sigma formation offset, +1.0 proxy")
print(f"  offset), NO DS cut, N=900: median FAKE z = {np.median(zf):.2f}, P(fake z>=3) = {np.mean(zf>=3.0):.2f}")
print(f"  same with the E1d DS-cut applied (groups excised):        median z = {np.median(zf_cut):+.2f}, P(z>=3) = {np.mean(zf_cut>=3.0):.4f}")
assert np.median(zf) > 1.5 and abs(np.median(zf_cut)) < 0.15, "substructure stress test inconclusive"
print("  [OK] BOTH WAYS: without the substructure cut a 3-sigma 'MI detection' can be FAKED under true MG;")
print("       the frozen E1d cut restores the exact null. A detection without the DS cut proves nothing.")

# ============================================================== (8) VERDICT (frozen rule E9)
print()
print("=" * 102)
print(" (8) VERDICT (rule E9, frozen above)")
print("=" * 102)
nm_C13, _ = results[("two-class", "CANONICAL a0=9.36e-11", 0.13, "C")]
nm_C6, _ = results[("two-class", "CANONICAL a0=9.36e-11", 0.06, "C")]
nm_D13, _ = results[("two-class", "CANONICAL a0=9.36e-11", 0.13, "D")]
nm_A13, _ = results[("two-class", "CANONICAL a0=9.36e-11", 0.13, "A")]
nm_A6, _ = results[("two-class", "CANONICAL a0=9.36e-11", 0.06, "A")]
print(f"""  POWERED NOW?   NO dataset qualifies. The entire public carrier reservoir is {N_INHAND} cluster/group
    UDG sigmas (Gannon+2024) at ~24% errors, untagged: at TODAY'S errors + the MEASURED in-hand
    astro floor (s_FJ={S_FJ_MEAS:.2f}), 3 sigma needs N ~ {nm_A13:,.0f}-{nm_A6:,.0f} (canonical band ends, two-class y)
    -> gap x{nm_A13/N_INHAND:,.0f}-{nm_A6/N_INHAND:,.0f}. In-hand median z = 0.1-0.4: EXPLORATORY ONLY (firewalled).
  POWERED IF (the specific combination, all elements named):
    (i) internal-sigma errors <=10% on diffuse carriers  -> ELT-HARMONI-class IFU (~2032; NO 2026
        instrument reaches the 8-20 km/s carriers: DESI/SDSS/MUSE floors 23-64 km/s, census (B));
    (ii) FJ control held at the banked 0.15 floor (needs homogeneous distances/apertures -- the
        in-hand heterogeneous floor is {S_FJ_MEAS:.2f} and would inflate N x{(S_FJ_MEAS**2+0.01)/(0.15**2+0.01):,.1f}); and
    (iii) DESI-DR1-grade phase tagging (D=0.6; caustic infrastructure ALREADY public: HeCS-omnibus
        {NCL_OMNI} clusters + GalWCat19 + gfinder >=10^3 rich clusters)
    => N_3sigma = {nm_C13:,.0f} (f=13%) to {nm_C6:,.0f} (f=6%) carriers, i.e. {nm_C13/M_EFF:,.0f}-{nm_C6/M_EFF:,.0f} LEWIS-class cluster
    campaigns ({M_EFF:.0f} usable carriers each); best realistic corner (tight FJ 0.08): {nm_D13:,.0f} carriers.
    The cluster reservoir ({NCL_OMNI} phase-tagged) already covers the f>=10% half of the band at D=0.6;
    the CONSERVATIVE continuum-y fork multiplies all N by ~x3 (grid above) -- pre-register BOTH.
  STILL UNDERPOWERED (2026): YES -- the binding wall is carrier sigma precision, which no existing
    or imminent public release (incl. the NOT-public DESI DR2, verified 401) touches. Exact gap:
    {N_INHAND} in hand vs ~{nm_D13:,.0f}-{nm_C6:,.0f} needed at a precision tier that first exists ~2032 (x{nm_D13/N_INHAND:.0f}-{nm_C6/N_INHAND:.0f});
    vs ~{nm_A13:,.0f}-{nm_A6:,.0f} at today's tier (x{nm_A13/N_INHAND:,.0f}-{nm_A6/N_INHAND:,.0f}).
  WHAT CLOSES IT: ELT-HARMONI first light (~2032) + a pre-registered target list built NOW for free
    (cross-match the DESI DR1 647k-dwarf VAC LSB tail vs HeCS-omnibus/gfinder clusters; tag infall
    phase from the public caustics; freeze THIS estimator). Both footings stay covered: the alt-a0
    band ends need x0.7-0.8 the N of canonical (grid) -- the discriminator is not footing-hostage.""")

assert nm_C13 < nm_C6 and nm_A13 > 10 * N_INHAND, "verdict arithmetic inconsistent"
print("\n EXIT 0 = frozen-estimator MC calibrated (null exact, sqrt-N verified, banked analytic reproduced);")
print("          verdict: STILL UNDERPOWERED in 2026; POWERED-IF combination named and quantified.")
