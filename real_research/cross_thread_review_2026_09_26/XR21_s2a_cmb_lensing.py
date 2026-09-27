#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR21_s2a_cmb_lensing -- STAGE 2a: the chain's separator (FP19's H_K1) in the particle-mesh box, scored at the CMB-lensing
wall.

WHY.  XR26 (68135cb7a) found the chain's late web MOND over-lenses the CMB.  On FP13's per-mode linear yardstick, Planck 2018's
8-400 lensing amplitude comes out at 1.149 (linear base, the most favourable) or 2.13 (halofit base), against 1.011 +- 0.028
(+4.9 / +40 sigma).  Passing needs the web phantom cut to 0.62x (linear base) / 0.18x (halofit base) (XR26 L2b).  XR21 stage 1
found that the model's real-space operator gives only 0.28-0.91 of the per-mode linear boost, and the nonlinear web's fields
are stronger still.  The coordinator's go for stage 2a: the box decides.  The separator is now FP19's H_K1 (0c18c582f), which
replaced FP13's H_S (linearly ill-posed, XR18).

THE MODEL IN THE BOX (FP19's H_K1; the QUMOND-type approximation of FP7's AQUAL root, as in stage 1):
  phi_ph = B u,  lap u = div[C^Q(y) G],  G = grad(B phi_N[source]),  y = |G|/(a a0),  C^Q y = X_P2(y - y_th),
  B = 1 - exp(-k^2 L^2/2),  L = L_Lambda Omega_L(<K>_h) (L_Lambda = 2.9 Mpc, n = 2),
  y_th = c_y max(0, 2q) 4 pi G rho_bar L/a0, c_y = 2 (FP19's tied yield; 2q = 1 + Omega_r - 9 Lambda/<K>_h^2),
  <K>_h = 3H on the box (XR21_pm_core.HK1; read on FP6's background, as FP19).
  lambda (phi's inertia) = 0.01 > 0 as the regulator, below XR25's inertness edge (~0.03).  It enters only the tracking
  weight, which the quasi-static box sets to 1 (the bound is printed, Q1).
  Two readings:
    'chain': FP10/L353 reciprocity -- the kernel reads the baryons, only they feel the phantom, the dark fluid is Newtonian;
    'fp9':   FP9/FP13/FP19's yardstick convention -- all matter sources and feels the phantom.
  Lensing sees phi_N + phi_ph (psi = Phi, FP7 R7d): delta_lens = delta_m + delta_ph.  No conversion (a cold dark fluid).
THE RUNS (one seed, the coordinator's specification): 100 Mpc/h, 256^3 mesh (0.39 Mpc/h cells), L366's layout (seed 7, L362's
  CLASS P_lin at z = 49, Zel'dovich ICs, KDK with dlna = 0.02, the record's output convention: the first step past each output
  z), 3 threads, one box at a time.
    lcdm (two species; this is L366's LCDM box);
    chain_canonical, chain_alt (two species) -- the decisive reading (see the amendment below);
    fp9_canonical, fp9_alt (one species: in the all-matter reading the co-located species never separate) -- the bridge;
    MUTATE: chain_canonical_noyield.
  Outputs at z = 5, 4, 3, 2.5, 2, 1.5, 1.25, 1, 0.8, 0.635, 0.5, 0.4, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05, 0: the exact-shell
  spectra of delta_m and delta_ph and their cross; sigma_8 (L366's estimator) at z = 1, 0.5, 0.25, 0; L367's cosmic-shear bins
  at z = 0.5.
THE LENSING goes through XR26's machinery, exec'd read-only from XR26_cmb.py: CAMB and CLASS at the Planck 2018 best fit, its
  Limber integral, band powers, amplitudes and phantom budget.
  - B_box(k, z) = P[delta_m + delta_ph]_model / P[delta_m]_LCDM from the matched boxes.
  - It multiplies CLASS's halofit P(k, z) for the headline (a nonlinear ratio on the nonlinear base), and CLASS's linear
    P(k, z) for comparison with XR26's most favourable variant.
  - Below the box's first bin B - 1 follows the band-pass, (h_k/h_k1)^2; the brackets are B - 1 = 0 and B held.  Above
    k = k_Nyq/2 = 4 h/Mpc B is held.  Above the last output (z = 5) B = 1.
  - H_K1's own per-mode yardstick (FP9/FP13's rule: XR26's growth_ceff with H_K1's L and yield, c_2 -> oo, lambda = 0.01)
    goes through the same machinery.  The cut factor f_box is the scaling of that yardstick's phantom (C_eff -> f C_eff, the
    growth held, XR26 L2b's construction) at which its Planck 8-400 amplitude equals the box's; the wall is the yardstick's f*.

AMENDMENT (made before the first full run, after one 64^3 smoke run that stopped in K2 on a missing import; prompted by the
coordinator's update relaying FP22, bfe9a2fe5).
  - FP22 derives that the action as written implies the all-matter reading, and that CMB lensing excludes it (real-space cut
    0.52-1.35 of XR26's per-mode phantom against the 0.62 / 0.18 needed).
  - The chain now adopts the dark field on the root's Einstein-frame metric g~ = g + (1 - e^-2chi) n n: the dark field neither
    sources nor feels chi.  That is this box's 'chain' reading, so it is the decisive test; 'fp9' is a bridge.
  - Lensing sees 2 (Phi_N[delta_m] + chi[f_b delta_b]).  The box's delta_L = delta_m + delta_ph is exactly that, from the
    potentials (the factor 2 cancels in B).
  - FP22's semi-analytic cut in this reading: 0.13-0.26 (H_K1 real-space 0.13-0.19).  It passes Planck and ACT on the linear
    base, fails ACT on the halofit base (>= 3.8 sigma), and passes Planck on halofit only in the canonical real-space cells.
  Changes made:
  - the boxes run chain first; the MUTATE runs only chain_canonical_noyield;
  - the cut factor is ALSO reported on FP22's scale, f_eff: the scaling of XR26's H_S per-mode phantom (XR26 L2b's curve, K3)
    whose Planck 8-400 amplitude equals the box's, per base -- beside FP22's 0.13-0.19;
  - X1 (reported, cheap) measures the web's band-passed field that enters the kernel at halo positions: the 27-cell vector
    mean of G (the halo's own radial field cancels in it) at local density peaks with delta_m >= 30, at z = 0.5, 0.25 and 0.
    It is compared with FP22's linear 3D rms (H_K1 canonical (b): 3.54e-14 m/s^2 at z = 0.25) and with BS2's stacked KiDS
    bound (6.7e-5 a0).  EXPECT the nonlinear field at halo positions to exceed FP22's linear rms: halos sit in the web's nodes.
  - The boxes are computed by this script's box runner in the decisive order (XR21_S2A_BOXES=<names>: it computes only
    uncached boxes and writes only the cache).  The record invocations (MUTATE=1 first, then main) load them by key.
  - R1 (reported, run if time allows after the requested boxes): a resolution partner for the decisive cell -- lcdm_hr and
    chain_canonical_hr, 50 Mpc/h on the same 256^3 mesh (0.195 Mpc/h cells, 8x the mass resolution; its own realisation of
    seed 7).  Reported: B_box - 1 at k = 0.3-3 h/Mpc, z = 0, 0.25, 0.5 against the 100 Mpc/h box, and the Planck/ACT
    amplitudes with the partner's B spliced in at k >= 0.4 h/Mpc.  No expectation (the phantom's small-scale part may grow with
    resolution); a change of the verdict under R1 would make the 100 Mpc/h result resolution-limited.
  - E6's contrast is printed whenever both chain_canonical and chain_canonical_noyield are in the cache (both invocations).
AMENDMENT 2 (made while the production boxes ran -- the LCDM box done, the first chain box in progress -- and before any analysis
of production data; prompted by the coordinator relaying XR18b's five conditions for H_K1):
  1-2 the separator's L(a) and y_th(a) are prescribed from the box's scale factor (XR21_pm_core.HK1 on FP6's background), and
      the q = 0 ramp is analytic: y_th switches off exactly at z_q0 = 0.6348, not 0.010 lower as FP13's table did.  Already so
      in every box (K2 checks the functions against FP19's table).
  3   lambda = 0.01 <= 0.03 (declared above): a pure regulator.  The box is quasi-static, the lambda -> 0+ limit of the tracking
      weight (Q1), so no box number depends on lambda.
  4   two more cell sizes for the decisive cell:
      - R2: lcdm_128 and chain_canonical_128 -- the same 100 Mpc/h box and the same realisation (ICs drawn on the 256^3 mesh)
        on a 128^3 mesh (0.78 Mpc/h cells);
      - R1 (0.195 Mpc/h cells) as declared.
      Reported: B_box - 1 at k = 0.3-2 h/Mpc, z = 0, 0.25, 0.5, and the Planck/ACT amplitudes at 0.78 / 0.39 / 0.195 Mpc/h.
      R2 (reported): the verdicts (halofit base) are unchanged between 128^3 and 256^3.  No expectation on the trend: XR18b's
      cold-matter growth (d_min^-1/4 at yield surfaces and, below z_q0, at zeros of the band-passed field) would make B - 1
      rise as the cell shrinks.
  5   the low-field monitor:
      - M1 (reported), every model box, between consecutive outputs at z <= 0.5 (after the yield has switched off), in every
        bin with P_pp/P_mm > 1e-6: the phantom's own amplification d ln[P_pp/(h_k^4 P_mm)]/d ln a stays <= 5 per e-fold (the
        raw d ln P_pp/d ln a is printed beside it).  EXPECT TRUE: the quasi-static operator carries no DE12-type mode (XR18b:
        up to 1.4e5 H), and a runaway would be a code instability.  DISCLOSED: the first form scored the raw rate <= 5; a 64^3
        smoke run of the new code (before any production analysis) showed that the prescribed opening of the band-pass alone
        drives the raw rate to ~8 d ln L/d ln a ~ 6-7 per e-fold at low k (P_pp ~ h_k^4 ~ L^8 there), so the monitor divides
        out h_k^4 and the matter.
      - M2 (reported, R1/R2 model boxes, every output): how low the kernel's argument y = |G|/(a a0) gets -- the low-tail
        volume and baryon-mass quantiles, the fractions below 1e-6/1e-5/1e-4 a0 and y_rms/100, the minimum, and y in the
        halo-centre cells.  The production boxes (already running) record the halo-centre field only (X1).
      These boxes run through run_box_mesh (the production boxes' keys are unchanged).

PRE-DECLARED (written before any run of this script: tolerances for the code checks, expectations for the physics)
  CONTROLS (load-bearing)
  K1  the LCDM box reproduces L366's committed sigma_8(z = 0) = 1.0208791238487946 and XR21 stage 1's committed L367 bins at
      z = 0.5 (R4, A6) to 1e-8 (relative): the stage-2 box is the record's box.
  K2  the box's H_K1 readout and this lane's H_K1 yardstick model reproduce FP19's committed L(z) and y_th(z) (H1: L at
      z = 0-3; y_th at z = 0.25-3, canonical) to 1e-9 (relative; absolute 1e-15 where FP19's value is 0).
  K3  XR26's machinery, exec'd read-only here, reproduces XR26's committed H_S headline to 1e-6 (relative): the Planck 8-400
      amplitude (linear base 1.14918, halofit base 2.13436) and the phantom budget f* (0.6182 / 0.1776).
  K4  every model box ran FP19's H_K1 at its footing: the separator state it recorded at every output (L, y_th) equals
      H_K1's to 1e-12.  MUTATE removes the yield, so K4 must FAIL (rc = 1).
  K5  the Limber integral's cut: at the earliest output (z = 5), |B_box - 1| <= 0.01 at k <= 1 h/Mpc in every box (B = 1 is
      used above z = 5).
  HYPOTHESES (reported: the physics verdicts, kept as run)
  E1  H_K1's per-mode yardstick fails Planck 8-400 like H_S's (FP19's per-mode P boost is ~0.6-0.7x H_S's).  EXPECT a
      linear-base amplitude above 1.067 (a pull of +2 to +4 sigma).  UNCERTAIN.
  E2  the box cuts the per-mode phantom: the nonlinear web's fields are stronger than the linear rms, so C^Q is smaller.
      EXPECT f_box < 1 in the all-matter reading, both footings.
  E3  whether the box passes Planck 8-400 (|A - 1.011| <= 2 x 0.028, halofit base).  THE QUESTION; no expectation.  ACT DR6
      (40 <= L <= 763, A = 1.013 +- 0.023, Qu et al. 2024) is reported alongside.  ACT's band-power covariance is not used:
      Planck's MV errors on the same bins weight the mean, and uniform weights bracket it.
  E4  the chain reading lenses less than the all-matter reading: the baryons' field is ~f_b of the matter's, so C^Q ~ 1/sqrt(y)
      rises by ~2.5 while the source falls by ~6.  EXPECT A_chain - 1 below A_fp9 - 1.
  E5  the alt footing (larger a0) lenses more than the canonical.  EXPECT TRUE.
  E6  (the MUTATE contrast) removing the yield raises B_box at z >= 0.8 and k >= 1 h/Mpc but barely moves Planck 8-400
      (|Delta A| <= 0.1 sigma = 0.0028, halofit base): at z >= 1 the band-pass hides k <~ 0.3 h/Mpc (h_k^2 <~ 0.03).  The yield
      is not what protects CMB lensing; z < 0.635 is.
  G   gates reported with the verdicts:
      - Planck 8-400 and ACT DR6 (E3);
      - the record's cosmic-shear gate (L364/L367): R(k) = P_lens/P_LCDM <= 1.2 at z = 0.5, k = 0.1-1 h/Mpc;
      - sigma_8 against FP19's tight band (<= 1.02), as the box's ratio and as that ratio completed below the box's fundamental
        with linear theory.
MUTATE=1: H_K1's yield floor removed (y_th = 0 at every epoch) in the chain reading (canonical footing).  K4 must FAIL (rc = 1).

SCOPE.
  - One seed.  Cosmic variance largely cancels in B = model/LCDM (matched initial conditions).
  - Resolution: the band-pass is resolved (L >= 2 cells) only at z <~ 1.  At z >~ 1.5 the box carries only the k <= k_Nyq tail
    of the phantom.  Planck 8-400 at z >= 1.5 reads k <~ 0.2 h/Mpc, where h_k^2 <~ 1e-5.
  - The dynamics use the record's PM background ('l362': no radiation, Omega_m = 0.3138), so the LCDM box is L366's.  The
    separator is read on FP6's background (with radiation), as FP19.  E(a) differs by <= 2e-4 at z <= 1 and 8e-4 at z = 5.
  - Quasi-static: the state term's own force (XR18) is not in the operator.  FP19 finds H_K1 well posed; XR18b is re-auditing.
  - The kernel is P2 (FP19's J_P2).  The chain's decided kernel nu_mono differs from P2 near y ~ 1, not in the deep regime
    that carries the web phantom.
  - Both a0 footings (FP0).  kappa = 1/2 is FITTED (Z = 5.7888); nothing here depends on it, and nothing here closes the
    theory.  The dark mass is still required: a cold dark fluid (FK1's order parameter) carried by particles as a numerical
    device.
  - Box caches (the shell spectra) go to XR21_CACHE (default: a temporary directory), keyed by a hash of the box's
    configuration and code.  The .out lists each box's key and whether it was computed in this invocation or loaded.

Run from the repository root:  XR21_CACHE=<scratch dir> python3 real_research/cross_thread_review_2026_09_26/XR21_s2a_cmb_lensing.py
(MUTATE=1 for the control; ~1.5 h for the five main boxes on 3 threads, ~6 GB; a cached re-run takes ~5 min)
"""
import os, sys, io, json, math, time, hashlib, inspect, tempfile, contextlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import XR21_common as X
THREADS = int(os.environ.get("XR21_THREADS", "3"))
X.pin_threads(THREADS)
import numpy as np

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR21_s2a_cmb_lensing"
SMOKE = os.environ.get("XR21_S2A_SMOKE", "0") == "1"             # a code test at 64^3 (scratch only, never for the record)
BOX = dict(L=100.0, NG=64 if SMOKE else 256, NP=48 if SMOKE else 192, zi=49.0, seed=7)
ZOUT = [5.0, 4.0, 3.0, 2.5, 2.0, 1.5, 1.25, 1.0, 0.8, 0.635, 0.5, 0.4, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05, 0.0]
Z_S8 = (1.0, 0.5, 0.25, 0.0)
KG_CS = (0.1, 0.2, 0.3, 0.5, 0.7, 1.0)                           # L364/L367's cosmic-shear k grid
LAM = 0.01                                                       # the regulator (XR25: inert below ~0.03)
PL_AMP, ACT_AMP = (1.011, 0.028), (1.013, 0.023)                 # Planck 2018 VIII eq. 23; ACT DR6 (Qu et al. 2024), 40-763
RUNS = {
    "lcdm": dict(mode="two", gravity="newton"),
    "fp9_canonical": dict(mode="single", gravity="hy", reading="fp9", foot="canonical"),
    "chain_canonical": dict(mode="two", gravity="hy", reading="chain", foot="canonical"),
    "fp9_alt": dict(mode="single", gravity="hy", reading="fp9", foot="alt"),
    "chain_alt": dict(mode="two", gravity="hy", reading="chain", foot="alt"),
    "fp9_canonical_noyield": dict(mode="single", gravity="hy", reading="fp9", foot="canonical", yield_on=False),
    "chain_canonical_noyield": dict(mode="two", gravity="hy", reading="chain", foot="canonical", yield_on=False),
    "lcdm_hr": dict(mode="two", gravity="newton", L=50.0, fn="mesh"),
    "chain_canonical_hr": dict(mode="two", gravity="hy", reading="chain", foot="canonical", L=50.0, fn="mesh"),
    "lcdm_128": dict(mode="two", gravity="newton", NG=BOX["NG"] // 2, ic_NG=BOX["NG"], fn="mesh"),
    "chain_canonical_128": dict(mode="two", gravity="hy", reading="chain", foot="canonical", NG=BOX["NG"] // 2, ic_NG=BOX["NG"], fn="mesh"),
}
MODELS = ["chain_canonical_noyield"] if MUTATE else ["chain_canonical", "chain_alt", "fp9_canonical", "fp9_alt"]
ORDER = ["lcdm"] + MODELS
CACHE = os.environ.get("XR21_CACHE") or os.path.join(tempfile.gettempdir(), "xr21_s2a_cache")


# ============================================================================================= one box (a spawned child)
Z_EXT = (0.5, 0.25, 0.0)
DPEAK = 30.0


def ext_field_stats(b, a):
    """X1: the band-passed field the kernel reads (G = grad(B phi_N[source]), this box's reading) at halo positions: local maxima
    of the matter CIC density with delta_m >= 30.  At a peak the halo's own (radial) field cancels in the 27-cell vector mean of
    G; what survives is the field of everything else within the band-pass -- the web's field in the kernel.  In units of a0
    (y = |G|/(a a0)), with the peak cell's own |G| and the volume rms alongside."""
    from scipy.ndimage import uniform_filter, maximum_filter
    m = b.mesh
    rb, rd = b.densities(); b.cb = b.cd = None
    rho = rb + rd; del rd
    src = b.source(rb, rho); del rb
    F = m.rfft(src); del src
    F *= b.hy.hk(a, m.K2); F *= -(1.5 * b.c.Om / a); F /= m.K2; F[0, 0, 0] = 0.0
    phib = m.irfft(F); del F
    pk = (rho == maximum_filter(rho, size=3, mode="wrap")) & (rho - 1.0 >= DPEAK)
    npk = int(pk.sum()); del rho
    gc2 = np.zeros(npk); ge2 = np.zeros(npk); gv2 = 0.0
    for i in range(3):
        g = m.grad_axis(phib, i)
        gv2 += float(np.mean(g * g))
        gc2 += g[pk] ** 2
        ge2 += uniform_filter(g, size=3, mode="wrap")[pk] ** 2
        del g
    sc = a * b.a0c
    ye, yc = np.sqrt(ge2) / sc, np.sqrt(gc2) / sc
    q = lambda v: [float(x) for x in np.percentile(v, [16, 50, 84])] if len(v) else [float("nan")] * 3
    return dict(n_peaks=npk, ext_q=q(ye), ext_rms=float(np.sqrt(np.mean(ye ** 2))) if npk else float("nan"), cell_q=q(yc),
                vol_rms=math.sqrt(gv2) / sc, a0_SI=b.a0c * b.c.UNIT_ACC)


def run_box(name):
    """run one box and write its outputs (shell spectra, sigma_8, L367 bins, the separator state) to the cache."""
    X.pin_threads(THREADS)
    import XR21_pm_core as C
    cfg = RUNS[name]
    cos, sep = C.Cosmo("l362"), C.Cosmo("fp6")
    Pl = X.l362_plin()
    foot = cfg.get("foot", "canonical")
    hy = C.HK1(sep, sep.a0_code(foot), yield_on=cfg.get("yield_on", True)) if cfg["gravity"] == "hy" else None
    t0 = time.time()
    box = C.Box(cfg.get("L", BOX["L"]), BOX["NG"], BOX["NP"], cos, zi=BOX["zi"], seed=BOX["seed"], mode=cfg["mode"], gravity=cfg["gravity"],
                reading=cfg.get("reading", "chain"), hy=hy, foot=foot, Pfun=lambda q: Pl(q, BOX["zi"]), workers=THREADS,
                threads=THREADS)
    t_ic = time.time() - t0
    m = box.mesh
    n2 = m.n2.ravel(); wr = m.wr.ravel(); nmax = int(n2.max()) + 1
    cnt = np.bincount(n2, weights=wr, minlength=nmax)
    norm = m.L ** 3 / m.NG ** 6
    arrs, rows = {}, []

    def out(b, a, z):
        dm, dph = b.lensing_delta(a)
        Fm = m.rfft(dm).ravel()
        j = len(rows)
        r = dict(z_nom=z, a=a, z=1.0 / a - 1.0)
        arrs[f"smm_{j}"] = np.bincount(n2, weights=wr * (Fm.real ** 2 + Fm.imag ** 2), minlength=nmax) * norm
        if b.gravity == "hy":
            Fp = m.rfft(dph).ravel()
            arrs[f"spm_{j}"] = np.bincount(n2, weights=wr * (Fp.real * Fm.real + Fp.imag * Fm.imag), minlength=nmax) * norm
            arrs[f"spp_{j}"] = np.bincount(n2, weights=wr * (Fp.real ** 2 + Fp.imag ** 2), minlength=nmax) * norm
            del Fp
            r["diag"] = {k_: float(v) for k_, v in b.diag.items()}
            r["sep"] = dict(L_com=float(b.hy.L_com(a)), y_th=float(b.hy.y_th(a)))
        else:
            arrs[f"spm_{j}"] = np.zeros(nmax); arrs[f"spp_{j}"] = np.zeros(nmax)
        del Fm
        if z in Z_S8:
            r["s8_m"] = m.sigma8(dm); r["s8_l"] = m.sigma8(dm + dph)
        if z == 0.5:
            r["pkb_m"] = {str(q): v for q, v in m.pk_bins(dm, KG_CS).items()}
            r["pkb_l"] = {str(q): v for q, v in m.pk_bins(dm + dph, KG_CS).items()}
        del dm, dph
        if b.gravity == "hy" and z in Z_EXT:
            r["ext"] = ext_field_stats(b, a)
        rows.append(r)
        print(f"      [{name}] output z = {r['z']:+.4f} (nominal {z}) after {b.nstep} steps, {time.time() - t0:.0f} s", flush=True)
        return {}

    box.run(ZOUT, dlna=0.02, on_output=out)
    info = dict(wall=time.time() - t0, t_ic=t_ic, steps=box.nstep, rss_gb=C.peak_rss_gb(),
                n_particles=len(box.xb) + len(box.xd), threads=THREADS)
    os.makedirs(CACHE, exist_ok=True)
    path = cache_path(name)
    np.savez_compressed(path + ".tmp.npz", cnt=cnt, meta=json.dumps(dict(rows=rows, info=info, cfg=cfg, box=BOX)), **arrs)
    os.replace(path + ".tmp.npz", path)
    return name, info


def box_fn(name):
    """the production boxes run run_box; the resolution partners (R1, R2) run run_box_mesh (their own mesh, a common IC mesh, and
    the low-field monitor)."""
    return run_box_mesh if RUNS[name].get("fn") == "mesh" else run_box


def box_key(name):
    core = open(os.path.join(HERE, "XR21_pm_core.py"), "rb").read()
    fn = box_fn(name)
    blob = (json.dumps(dict(run=RUNS[name], box=BOX, zout=ZOUT, z_s8=Z_S8, kg=KG_CS, threads=THREADS, z_ext=Z_EXT, dpeak=DPEAK),
                       sort_keys=True).encode()
            + core + inspect.getsource(fn).encode() + inspect.getsource(ext_field_stats).encode()
            + (inspect.getsource(low_field_stats).encode() if fn is run_box_mesh else b""))
    return hashlib.sha256(blob).hexdigest()[:16]


def cache_path(name):
    return os.path.join(CACHE, f"{name}_{box_key(name)}.npz")


def load_box(name):
    f = np.load(cache_path(name), allow_pickle=False)
    meta = json.loads(str(f["meta"]))
    rows = meta["rows"]
    for j, r in enumerate(rows):
        r["smm"], r["spm"], r["spp"] = f[f"smm_{j}"], f[f"spm_{j}"], f[f"spp_{j}"]
    return dict(rows=rows, info=meta["info"], cnt=f["cnt"])


LOW_T = (1e-6, 1e-5, 1e-4)                                        # the low-field thresholds (a0 units)
LOW_Q = (1e-4, 1e-3, 1e-2, 0.1, 0.5)                               # the low-tail quantiles


def low_field_stats(b, a):
    """XR18b's condition 5: how low the kernel's argument y = |G|/(a a0) gets (G = grad(B phi_N[source]), this box's reading):
    its volume and baryon-mass quantiles in the low tail, the volume and mass fractions below 1e-6, 1e-5, 1e-4 a0 and below
    y_rms/100, the minimum, and y in the halo-centre cells (local density maxima with delta_m >= 30)."""
    from scipy.ndimage import maximum_filter
    m = b.mesh
    rb, rd = b.densities(); b.cb = b.cd = None
    rho = rb + rd; del rd
    src = b.source(rb, rho)
    F = m.rfft(src); del src
    F *= b.hy.hk(a, m.K2); F *= -(1.5 * b.c.Om / a); F /= m.K2; F[0, 0, 0] = 0.0
    phib = m.irfft(F); del F
    g2 = np.zeros_like(phib)
    for i in range(3):
        g = m.grad_axis(phib, i); g2 += g * g; del g
    del phib
    y = (np.sqrt(g2) / (a * b.a0c)).ravel(); del g2
    yr = float(np.sqrt(np.mean(y * y)))
    w = (rb / rb.sum()).ravel(); del rb
    o = np.argsort(y, kind="stable"); ys = y[o]; cw = np.cumsum(w[o]); del o
    mass_q = [float(ys[min(int(np.searchsorted(cw, q)), len(ys) - 1)]) for q in LOW_Q]
    vol_q = [float(ys[min(int(q * len(ys)), len(ys) - 1)]) for q in LOW_Q]
    thr = list(LOW_T) + [yr / 100.0]
    vol_f = [float(np.searchsorted(ys, t) / len(ys)) for t in thr]
    mass_f = [float(cw[int(np.searchsorted(ys, t)) - 1]) if np.searchsorted(ys, t) > 0 else 0.0 for t in thr]
    del ys, cw
    pk = ((rho == maximum_filter(rho, size=3, mode="wrap")) & (rho - 1.0 >= DPEAK)).ravel()
    ypk = y[pk]
    return dict(y_rms=yr, y_min=float(y.min()), vol_q=vol_q, mass_q=mass_q, thr=thr, vol_f=vol_f, mass_f=mass_f,
                n_peaks=int(pk.sum()), peak_q=[float(x) for x in np.percentile(ypk, [16, 50, 84])] if len(ypk) else [float("nan")] * 3,
                y_th=float(b.hy.y_th(a)))


def run_box_mesh(name):
    """run_box for the resolution partners: the box's own mesh (cfg NG) and IC mesh (cfg ic_NG: the same realisation as the
    production box when 256), plus the low-field monitor (low_field_stats) at every output of the model boxes."""
    X.pin_threads(THREADS)
    import XR21_pm_core as C
    cfg = RUNS[name]
    cos, sep = C.Cosmo("l362"), C.Cosmo("fp6")
    Pl = X.l362_plin()
    foot = cfg.get("foot", "canonical")
    hy = C.HK1(sep, sep.a0_code(foot), yield_on=cfg.get("yield_on", True)) if cfg["gravity"] == "hy" else None
    t0 = time.time()
    box = C.Box(cfg.get("L", BOX["L"]), cfg.get("NG", BOX["NG"]), BOX["NP"], cos, zi=BOX["zi"], seed=BOX["seed"], mode=cfg["mode"],
                gravity=cfg["gravity"], reading=cfg.get("reading", "chain"), hy=hy, foot=foot, Pfun=lambda q: Pl(q, BOX["zi"]),
                workers=THREADS, threads=THREADS, ic_NG=cfg.get("ic_NG"))
    t_ic = time.time() - t0
    m = box.mesh
    n2 = m.n2.ravel(); wr = m.wr.ravel(); nmax = int(n2.max()) + 1
    cnt = np.bincount(n2, weights=wr, minlength=nmax)
    norm = m.L ** 3 / m.NG ** 6
    arrs, rows = {}, []

    def out(b, a, z):
        dm, dph = b.lensing_delta(a)
        Fm = m.rfft(dm).ravel()
        j = len(rows)
        r = dict(z_nom=z, a=a, z=1.0 / a - 1.0)
        arrs[f"smm_{j}"] = np.bincount(n2, weights=wr * (Fm.real ** 2 + Fm.imag ** 2), minlength=nmax) * norm
        if b.gravity == "hy":
            Fp = m.rfft(dph).ravel()
            arrs[f"spm_{j}"] = np.bincount(n2, weights=wr * (Fp.real * Fm.real + Fp.imag * Fm.imag), minlength=nmax) * norm
            arrs[f"spp_{j}"] = np.bincount(n2, weights=wr * (Fp.real ** 2 + Fp.imag ** 2), minlength=nmax) * norm
            del Fp
            r["diag"] = {k_: float(v) for k_, v in b.diag.items()}
            r["sep"] = dict(L_com=float(b.hy.L_com(a)), y_th=float(b.hy.y_th(a)))
        else:
            arrs[f"spm_{j}"] = np.zeros(nmax); arrs[f"spp_{j}"] = np.zeros(nmax)
        del Fm
        if z in Z_S8:
            r["s8_m"] = m.sigma8(dm); r["s8_l"] = m.sigma8(dm + dph)
        if z == 0.5:
            r["pkb_m"] = {str(q): v for q, v in m.pk_bins(dm, KG_CS).items()}
            r["pkb_l"] = {str(q): v for q, v in m.pk_bins(dm + dph, KG_CS).items()}
        del dm, dph
        if b.gravity == "hy":
            if z in Z_EXT:
                r["ext"] = ext_field_stats(b, a)
            r["low"] = low_field_stats(b, a)
        rows.append(r)
        print(f"      [{name}] output z = {r['z']:+.4f} (nominal {z}) after {b.nstep} steps, {time.time() - t0:.0f} s", flush=True)
        return {}

    box.run(ZOUT, dlna=0.02, on_output=out)
    info = dict(wall=time.time() - t0, t_ic=t_ic, steps=box.nstep, rss_gb=C.peak_rss_gb(),
                n_particles=len(box.xb) + len(box.xd), threads=THREADS)
    os.makedirs(CACHE, exist_ok=True)
    path = cache_path(name)
    np.savez_compressed(path + ".tmp.npz", cnt=cnt, meta=json.dumps(dict(rows=rows, info=info, cfg=cfg, box=BOX)), **arrs)
    os.replace(path + ".tmp.npz", path)
    return name, info


# ============================================================================================= XR26's machinery (read-only)
def load_xr26():
    """XR26_cmb.py's inputs, CAMB/CLASS fiducial, FP13 yardstick, Limber machinery and late-lensing section, exec'd read-only
    from its source in a private namespace.  Skipped: the output tee, the patched-CLASS build, the CAMB-vs-CLASS comparisons,
    the primary-CMB and re-lensing sections.  XR26's own check()/P() are replaced by silent recorders."""
    path = os.path.join(HERE, "XR26_cmb.py")
    src = open(path).read()

    def seg(a, b):
        i = src.index(a)
        return src[i:src.index(b, i)]
    parts = [seg("import sys, io, re, json, math, time, shutil", "class _Tee:"),
             seg("def exec_ro(path, stop=None):", "P(__doc__.strip())"),
             seg('P18 = {"omega_b"', 'banner("BUILD: a patched CLASS'),
             seg("BBN_PAR = camb_bbn", "RAW = cl_fid.raw_cl(LMAXC)"),
             seg("# ---- FP13's (H_S) growth yardstick", "# ---- re-lensing with CAMB's correlation-function method"),
             seg('banner("L  THE LATE-TIME LENSING', "# L3/L4 the lensed spectra")]
    log = io.StringIO()
    ns = {"__file__": path, "__name__": "xr26_readonly", "OUT": {"numbers": {}, "checks": {}}, "CH": [], "os": os}

    def P_(*a):
        print(*a, file=log)

    def check_(name, measured, ok, reading="", load_bearing=True):
        ns["CH"].append((name.split()[0], bool(ok)))
        return bool(ok)
    old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    try:
        for i, s in enumerate(parts):
            ns.update(P=P_, banner=lambda t: P_(t), el=lambda: "", check=check_)
            with contextlib.redirect_stdout(log):
                exec(compile(s, f"{path}:segment{i}", "exec"), ns)
    finally:
        if old is None:
            os.environ.pop("MUTATE", None)
        else:
            os.environ["MUTATE"] = old
    ns["_log"] = log.getvalue()
    return ns


# ============================================================================================= the analysis
if __name__ == "__main__" and os.environ.get("XR21_S2A_BOXES"):
    # the box runner: compute the listed boxes (skipping cached ones) in the given order; writes only the cache
    from multiprocessing import get_context
    ctx = get_context("spawn")
    for name in os.environ["XR21_S2A_BOXES"].split(","):
        t_ = time.time()
        if os.path.exists(cache_path(name)):
            print(f"  {name}: cached ({box_key(name)})", flush=True); continue
        with ctx.Pool(1, maxtasksperchild=1) as pool:
            _, inf = pool.apply(box_fn(name), (name,))
        print(f"  {name}: done ({box_key(name)}): {inf['wall']:.0f} s, {inf['steps']} steps, peak {inf['rss_gb']:.2f} GB", flush=True)
    sys.exit(0)

if __name__ == "__main__":
    from multiprocessing import get_context
    lane = X.Lane(SLUG, MUTATE)
    P, check, banner = lane.P, lane.check, lane.banner
    P(__doc__.split("PRE-DECLARED")[0].strip())
    P("\n  PRE-DECLARED" + __doc__.split("PRE-DECLARED")[1].split("SCOPE.")[0].rstrip())
    if MUTATE:
        P("\n  *** MUTATE=1: H_K1's yield floor removed (y_th = 0 at every epoch), both readings, canonical footing; K4 must FAIL ***")
    if SMOKE:
        P("\n  *** SMOKE: 64^3 code test (not for the record) ***")
    import XR21_pm_core as C
    cos, sep = C.Cosmo("l362"), C.Cosmo("fp6")
    FP19 = json.load(open(os.path.join(X.CHAIN, "FP19_hs_repair_results.json")))["numbers"]

    # ------------------------------------------------------------------------------------------ the boxes
    banner("BOXES: 100 Mpc/h, " + f"{BOX['NG']}^3 mesh, {BOX['NP']}^3 particles per species, seed 7, z_i = 49; {THREADS} threads; "
           f"cache {os.path.basename(CACHE)}/")
    ctx = get_context("spawn")
    B = {}
    for name in ORDER:
        key = box_key(name)
        if os.path.exists(cache_path(name)):
            B[name] = load_box(name); how = "loaded from the cache"
        else:
            with ctx.Pool(1, maxtasksperchild=1) as pool:
                pool.apply(box_fn(name), (name,))
            B[name] = load_box(name); how = "computed now"
        inf = B[name]["info"]
        P(f"    {name:24s} key {key} ({how}): {inf['wall']:.0f} s ({inf['steps']} steps, ICs {inf['t_ic']:.0f} s), peak "
          f"{inf['rss_gb']:.2f} GB, {inf['n_particles']} particles, {inf['threads']} threads   {lane.el()}")
    lane.out["runs"] = {n: dict(key=box_key(n), **B[n]["info"]) for n in ORDER}
    OPT = ["chain_canonical"] if MUTATE else ["chain_canonical_noyield", "lcdm_128", "chain_canonical_128", "lcdm_hr", "chain_canonical_hr"]
    for name in OPT:                                                         # E6's contrast and R1: used only if cached
        if os.path.exists(cache_path(name)):
            B[name] = load_box(name); inf = B[name]["info"]
            lane.out["runs"][name] = dict(key=box_key(name), optional=True, **inf)
            P(f"    {name:24s} key {box_key(name)} (optional; loaded from the cache): {inf['wall']:.0f} s ({inf['steps']} steps), "
              f"peak {inf['rss_gb']:.2f} GB, {inf['n_particles']} particles")
        else:
            P(f"    {name:24s} (optional) not in the cache: not run")
    ZN = [r["z_nom"] for r in B["lcdm"]["rows"]]
    for n in B:
        assert [r["z_nom"] for r in B[n]["rows"]] == ZN
        assert all(abs(r["a"] - q["a"]) < 1e-14 for r, q in zip(B[n]["rows"], B["lcdm"]["rows"]))   # matched steps
    ZA = np.array([r["z"] for r in B["lcdm"]["rows"]])
    AA = np.array([r["a"] for r in B["lcdm"]["rows"]])
    P("    output redshifts (actual; the record's first step past each nominal z): " + ", ".join(f"{z:.3f}" for z in ZA))

    # ------------------------------------------------------------------------------------------ controls
    banner("K  CONTROLS: the record's LCDM box; FP19's H_K1; XR26's machinery; the model the boxes ran; the Limber cut")
    L366 = json.load(open(os.path.join(X.DSEC, "L366_triggered_carrier_cluster_retention_results.json")))["numbers"]["runs"]["lcdm"]
    A6 = json.load(open(os.path.join(HERE, "XR21_s1_lcdm_controls_results.json")))["numbers"]["A4_A6"]["pk_bins_z05"]
    jz = {z: ZN.index(z) for z in ZN}
    s8_lcdm0 = B["lcdm"]["rows"][jz[0.0]]["s8_m"]
    d_s8 = abs(s8_lcdm0 / L366["0.0"]["sigma8"] - 1)
    pkb0 = B["lcdm"]["rows"][jz[0.5]]["pkb_m"]
    d_pkb = max(abs(pkb0[str(q)] / A6[str(q)] - 1) for q in KG_CS)
    check("K1 CONTROL: the LCDM box is the record's: its sigma_8(z = 0) equals L366's committed 1.0208791238487946 and its L367 bins "
          "at z = 0.5 equal XR21 stage 1's committed R4 values, to 1e-8",
          f"sigma_8 {s8_lcdm0:.16f} (dev {d_s8:.1e}); L367 bins max dev {d_pkb:.1e}",
          (d_s8 <= 1e-8 and d_pkb <= 1e-8) if not SMOKE else True)
    # K2: FP19's committed tables
    ref_L, ref_y = FP19["H1"]["L_kpc"], FP19["H1"]["yth"]
    hk_c = C.HK1(sep, sep.a0_code("canonical"))

    def k2dev(Lf, yf):
        dl = max(abs(Lf(1 / (1 + float(z))) * 1e3 / v - 1) for z, v in ref_L.items())
        dy = max((abs(yf(1 / (1 + float(z))) / v - 1) if v > 0 else abs(yf(1 / (1 + float(z))))) for z, v in ref_y.items())
        return dl, dy
    k2_box = k2dev(hk_c.L_phys, hk_c.y_th)
    t_x = time.time()
    NS = load_xr26()
    P(f"    XR26's machinery exec'd read-only ({time.time() - t_x:.0f} s): its own controls inside the exec'd segments: "
      + ", ".join(f"{n_} {'pass' if ok else 'FAIL'}" for n_, ok in NS["CH"]))
    Om9, OL9, Or9, h9, H09, Mpc9 = NS["Om9"], NS["OL9"], NS["Or9"], NS["h9"], NS["H09"], NS["Mpc9"]
    A0_9, KHF, DIF, Z_L, cutfac, YIELD = NS["A0_9"], NS["KHF"], NS["DIF"], NS["Z_L"], NS["cutfac"], NS["YIELD"]

    def L_K1(a_):
        return 2.9 * OL9 / (Om9 / a_ ** 3 + OL9 + Or9 / a_ ** 4)

    def y_K1(a_, f, on=True):
        if not on:
            return 0.0
        E2 = Om9 / a_ ** 3 + OL9 + Or9 / a_ ** 4
        tq = 1.0 + (Or9 / a_ ** 4) / E2 - 3.0 * OL9 / E2
        return 2.0 * max(0.0, tq) * 1.5 * H09 ** 2 * (Om9 / a_ ** 3 + Or9 / a_ ** 4) * L_K1(a_) * Mpc9 / A0_9[f]

    def hk1_model(f, on=True):
        return {"hfac": lambda a_, k_: 1.0 - np.exp(-0.5 * (k_ * h9 * L_K1(a_) / a_) ** 2),
                "cut": lambda y, a_, f=f, on=on: cutfac(y, y_K1(a_, f, on), YIELD), "yr": 0.0}
    k2_yard = k2dev(L_K1, lambda a_: y_K1(a_, "canonical"))
    check("K2 CONTROL: FP19's H_K1 -- the box's readout and this lane's yardstick model reproduce FP19's committed L(z) (z = 0-3) "
          "and y_th(z) (z = 0.25-3, canonical) to 1e-9",
          f"box readout: L {k2_box[0]:.1e}, y_th {k2_box[1]:.1e}; yardstick model: L {k2_yard[0]:.1e}, y_th {k2_yard[1]:.1e}",
          max(k2_box + k2_yard) <= 1e-9)
    X26 = json.load(open(os.path.join(HERE, "XR26_cmb_results.json")))["numbers"]
    HEAD = NS["HEAD"]
    got = dict(lin=NS["L2"]["8-400"]["rows"][(HEAD, "lin")]["amp"], NL=NS["L2"]["8-400"]["rows"][(HEAD, "NL")]["amp"],
               flin=NS["FSTAR"]["lin"], fNL=NS["FSTAR"]["NL"])
    ref = dict(lin=X26["L2"]["8-400"]["rows"][f"{HEAD} || lin"]["amp"], NL=X26["L2"]["8-400"]["rows"][f"{HEAD} || NL"]["amp"],
               flin=X26["L2b"]["f_star"]["lin"], fNL=X26["L2b"]["f_star"]["NL"])
    d_k3 = max(abs(got[k_] / ref[k_] - 1) for k_ in got)
    check("K3 CONTROL: XR26's machinery, exec'd read-only, reproduces XR26's committed H_S headline -- Planck 8-400 amplitude "
          "(linear / halofit base) and the phantom budget f* (linear / halofit base) -- to 1e-6",
          "; ".join(f"{k_} {got[k_]:.6f} vs {ref[k_]:.6f}" for k_ in got) + f" (max dev {d_k3:.1e})", d_k3 <= 1e-6)
    k4 = {}
    for n in MODELS:
        hd = C.HK1(sep, sep.a0_code(RUNS[n]["foot"]))                      # the declared model (the yield on)
        dL = max(abs(r["sep"]["L_com"] / hd.L_com(r["a"]) - 1) for r in B[n]["rows"])
        dy = max(abs(r["sep"]["y_th"] - hd.y_th(r["a"])) / max(hd.y_th(r["a"]), 1e-300) if hd.y_th(r["a"]) > 0
                 else abs(r["sep"]["y_th"]) for r in B[n]["rows"])
        k4[n] = (dL, dy)
    check("K4 every model box ran FP19's H_K1 at its footing: the separator state it recorded at every output (L, y_th) equals "
          "H_K1's (the yield on) to 1e-12",
          "; ".join(f"{n}: L {v[0]:.1e}, y_th {v[1]:.1e}" for n, v in k4.items()), all(max(v) <= 1e-12 for v in k4.values()),
          "MUTATE removes the yield: this check must fail there" if not MUTATE else "")

    # ------------------------------------------------------------------------------------------ the box's B(k, z)
    NB = 24

    def binning(L_, cnt_, NG_=None):
        """24 log bins from the box's fundamental to k_Nyq/2 on the exact shells; mode-weighted bin centres."""
        kf_ = 2 * math.pi / L_; kmax_ = 0.5 * math.pi * (NG_ or BOX["NG"]) / L_
        ksh_ = kf_ * np.sqrt(np.arange(len(cnt_)))
        edges_ = np.geomspace(kf_ * 0.999, kmax_ * 1.0001, NB + 1)
        idx_ = np.digitize(ksh_, edges_) - 1; idx_[0] = -1
        good_ = (idx_ >= 0) & (idx_ < NB) & (cnt_ > 0)
        bs = lambda arr: np.bincount(idx_[good_], weights=arr[good_], minlength=NB)
        c_ = bs(cnt_); ok_ = c_ > 0
        return dict(bs=bs, ok=ok_, kc=(bs(cnt_ * ksh_) / np.maximum(c_, 1e-300))[ok_], kf=kf_, kmax=kmax_)
    BIN = binning(BOX["L"], B["lcdm"]["cnt"])
    kf, kmax_use, kc = BIN["kf"], BIN["kmax"], BIN["kc"]

    def ratios(n, ref="lcdm", bn=None):
        """per output: b_m = P_mm/P_mm^LCDM and B = P_lens/P_mm^LCDM on the bins; the phantom's cross transfer P_pm/P_mm."""
        bn = bn or BIN; bs, ok_ = bn["bs"], bn["ok"]
        out_ = []
        for r, q in zip(B[n]["rows"], B[ref]["rows"]):
            mm, pm, pp, ml = bs(r["smm"]), bs(r["spm"]), bs(r["spp"]), bs(q["smm"])
            out_.append(dict(bm=(mm / ml)[ok_], B=((mm + 2 * pm + pp) / ml)[ok_], T=(pm / np.maximum(mm, 1e-300))[ok_]))
        return out_
    R = {n: ratios(n) for n in B if n != "lcdm" and not n.endswith("_hr") and not n.endswith("_128")}
    kmax_d = {}
    for n in MODELS:
        j5 = ZN.index(5.0)
        kmax_d[n] = float(np.max(np.abs(R[n][j5]["B"][kc <= 1.0] - 1)))
    check("K5 the Limber cut at z = 5: |B_box - 1| <= 0.01 at k <= 1 h/Mpc at the earliest output in every model box (B = 1 is "
          "used above z = 5)", "; ".join(f"{n} {v:.1e}" for n, v in kmax_d.items()), max(kmax_d.values()) <= 0.01)

    # tracking weight bound (Q1)
    c_over_H0 = 2997.92458                                                   # Mpc/h
    kk = np.geomspace(kf, math.pi * BOX["NG"] / BOX["L"], 50)
    Lc0 = C.HK1(sep, sep.a0_code("canonical")).L_com(1.0)
    hk0 = -np.expm1(-0.5 * (kk * Lc0) ** 2)
    Ccrit = 0.0101 * (c_over_H0 * kk) ** 2 / (LAM + 3 * hk0 ** 2)             # w < 0.99 needs C^Q above this (z = 0)
    cq_max = max(r["diag"]["cbar"] for n in MODELS for r in B[n]["rows"])
    check("Q1 (reported) the quasi-static operator: with lambda = 0.01 and c_2 -> oo, the tracking weight w = 1/(1 + (H/(c_s k))^2), "
          "c_s^2 = c^2/(C^Q (lambda + 3 h_k^2)), stays above 0.99 at every box k unless C^Q exceeds the printed floor (a field below "
          "~C^-2 a0: field nulls only)",
          f"C^Q floor for w < 0.99 over k = {kk[0]:.3f}-{kk[-1]:.2f} h/Mpc at z = 0: >= {Ccrit.min():.2e} (y <~ {Ccrit.min() ** -2:.1e}); "
          f"the boxes' largest field-weighted mean C^Q (cbar) at any output: {cq_max:.2f}", True, load_bearing=False)

    # ------------------------------------------------------------------------------------------ H_K1's per-mode yardstick
    banner("Y  H_K1'S PER-MODE YARDSTICK through XR26's machinery (FP9/FP13's rule, c_2 -> oo, lambda = 0.01): B, C_L^pp, amplitudes, f*")
    GL = NS["GL"]
    RBS = NS["RectBivariateSpline"]
    limber_pp, LIMB_FID, L_G, bandpowers, PL18_MV = NS["limber_pp"], NS["LIMB_FID"], NS["L_G"], NS["bandpowers"], NS["PL18_MV"]
    PL18_MV["ACT 40-763"] = [(lo, hi, 1.0, sA, fid) for (lo, hi, A_, sA, fid) in PL18_MV["8-2048"] if lo >= 40 and hi <= 763]
    PL18_MV["ACT 40-763 uniform"] = [(lo, hi, 1.0, 1.0, fid) for (lo, hi, A_, sA, fid) in PL18_MV["ACT 40-763"]]
    FEET = ["canonical"] if MUTATE else ["canonical", "alt"]
    YON = not MUTATE

    def amp_of(Rl, rng):
        bp_c = bandpowers(lambda ll: np.interp(ll, L_G, Rl), rng)
        bp_l = bandpowers(lambda ll: np.ones_like(ll, float), rng)
        w = 1 / np.array([b_[3] for b_ in PL18_MV[rng]]) ** 2
        dat = np.array([b_[2] * b_[4] for b_ in PL18_MV[rng]]); err = np.array([b_[3] * b_[4] for b_ in PL18_MV[rng]])
        return float(np.sum(w * bp_c / bp_l) / np.sum(w)), float(np.sum(((dat - bp_c) / err) ** 2) - np.sum(((dat - bp_l) / err) ** 2))

    def amps(Bfun):
        o = {}
        for base in ("NL", "lin"):
            Rl = limber_pp(base, Bfun) / LIMB_FID[base]
            a8, dchi = amp_of(Rl, "8-400")
            o[base] = dict(planck=a8, dchi2=dchi, pull=(a8 - PL_AMP[0]) / PL_AMP[1],
                           act=amp_of(Rl, "ACT 40-763")[0], act_uniform=amp_of(Rl, "ACT 40-763 uniform")[0],
                           R={str(L_): float(np.interp(L_, L_G, Rl)) for L_ in (40, 100, 200, 400, 763)})
            o[base]["act_pull"] = (o[base]["act"] - ACT_AMP[0]) / ACT_AMP[1]
        return o
    YD, YAMP, FSTAR, AMPF = {}, {}, {}, {}
    FS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.85, 1.0, 1.25, 1.5, 2.0]
    TARGET = PL_AMP[0] + 2 * PL_AMP[1]
    for f in FEET:
        lab = f"H_K1 per-mode | {f} | lam {LAM}" + ("" if YON else " | no yield")
        gr = NS["growth_ceff"](hk1_model(f, YON), A0_9[f], "permode", Z_L, KHg=KHF, Dig=DIF, lam=LAM, c2=1e15)
        Bz = np.array([((1 + gr[round(z_, 6)][1]) * gr[round(z_, 6)][0] / GL[round(z_, 6)][0]) ** 2 for z_ in Z_L])
        ib = RBS(np.array(Z_L), np.log(KHF), Bz, kx=1, ky=1)
        YD[f] = dict(Bz=Bz, ib=ib, gr=gr)
        Bf = (lambda ib_: (lambda k_h, z_: np.where(z_ > Z_L[-1], 1.0, ib_(np.minimum(z_, Z_L[-1]),
                                                                            np.log(np.clip(k_h, KHF[0], KHF[-1])), grid=False))))(ib)
        YD[f]["Bfun"] = Bf
        YAMP[f] = amps(Bf)
        NS["GROW"][lab] = gr; NS["HEAD"] = lab
        AMPF[f] = {b: [NS["amp_for_f"](f_, b) for f_ in FS] for b in ("lin", "NL")}
        FSTAR[f] = {b: (float(np.interp(TARGET, v, FS)) if v[-1] > TARGET and v[0] < TARGET else (0.0 if v[0] >= TARGET else float("inf")))
                    for b, v in AMPF[f].items()}
        P(f"    {lab}: B(k, z = 0) at k = 0.1/0.3/0.5/1/3 = " + "/".join(f"{float(ib.ev(0.0, math.log(kv))):.3f}" for kv in (0.1, 0.3, 0.5, 1.0, 3.0))
          + "; B(1 h/Mpc, z = 0.25/0.5/1/2) = " + "/".join(f"{float(ib.ev(zz, 0.0)):.3f}" for zz in (0.25, 0.5, 1.0, 2.0)))
        for b in ("lin", "NL"):
            v = YAMP[f][b]
            P(f"        {b:3s} base: Planck 8-400 A = {v['planck']:.4f} (pull {v['pull']:+.2f} sigma, Delta chi^2 {v['dchi2']:+.2f}); "
              f"ACT 40-763 A = {v['act']:.4f} (uniform weights {v['act_uniform']:.4f}; pull {v['act_pull']:+.2f}); "
              f"f* = {FSTAR[f][b]:.3f} (amplitude at f = " + ", ".join(f"{f_}: {a_:.3f}" for f_, a_ in zip(FS, AMPF[f][b]) if f_ in (0.0, 0.5, 1.0, 2.0)) + ")")
    check("E1 (reported) H_K1's PER-MODE YARDSTICK fails Planck 8-400 like H_S's (expected: linear-base amplitude above 1.067, "
          "pull +2 to +4 sigma)", "; ".join(f"{f}: linear base {YAMP[f]['lin']['planck']:.4f} (pull {YAMP[f]['lin']['pull']:+.2f}), "
                                            f"halofit base {YAMP[f]['NL']['planck']:.4f} (pull {YAMP[f]['NL']['pull']:+.2f}); wall f* = "
                                            f"{FSTAR[f]['lin']:.3f} / {FSTAR[f]['NL']:.3f}" for f in FEET),
          all(YAMP[f]["lin"]["planck"] > TARGET for f in FEET), load_bearing=False)
    lane.out["numbers"]["yardstick"] = {f: dict(amps=YAMP[f], f_star=FSTAR[f], amp_of_f={b: dict(zip(map(str, FS), v)) for b, v in AMPF[f].items()},
                                             B_z0={str(kv): float(YD[f]["ib"].ev(0.0, math.log(kv))) for kv in (0.1, 0.3, 0.5, 1.0, 3.0)})
                                        for f in FEET}

    # ------------------------------------------------------------------------------------------ the box's lensing
    banner("L  THE BOX'S LENSING: B_box(k, z) -> C_L^pp -> Planck 8-400 and ACT DR6 amplitudes, both readings and footings; the cut factor")
    KGRID = np.geomspace(1e-4, 50.0, 320)
    order = np.argsort(ZA)

    def B_rows(Rn, kc_, foot, rule="hk2"):
        """B on KGRID at every output from binned ratios: log-interpolated inside the bins, held above, and below the first bin
        B - 1 x (h_k/h_k1)^2 ('hk2'), 1 ('zero') or held ('hold')."""
        hk = C.HK1(sep, sep.a0_code(foot))
        rows_ = []
        for j in range(len(ZN)):
            Bb = Rn[j]["B"]
            v = np.exp(np.interp(np.log(KGRID), np.log(kc_), np.log(np.maximum(Bb, 1e-300))))
            lo = KGRID < kc_[0]
            if rule == "hk2":
                Lc = hk.L_com(AA[j])
                hr = (-np.expm1(-0.5 * (KGRID[lo] * Lc) ** 2)) / (-np.expm1(-0.5 * (kc_[0] * Lc) ** 2))
                v[lo] = 1.0 + (Bb[0] - 1.0) * hr ** 2
            elif rule == "zero":
                v[lo] = 1.0
            rows_.append(v)
        return np.array(rows_)

    def Bfun_of(rows_):
        ib = RBS(ZA[order], np.log(KGRID), rows_[order], kx=1, ky=1)
        ztop = float(ZA.max())
        return (lambda k_h, z_: np.where(z_ > ztop, 1.0, ib(np.minimum(z_, ztop), np.log(np.clip(k_h, KGRID[0], KGRID[-1])), grid=False)))

    def box_Bfun(n, rule="hk2"):
        return Bfun_of(B_rows(R[n], kc, RUNS[n]["foot"], rule))
    LA = {}
    for n in MODELS:
        LA[n] = {rule: amps(box_Bfun(n, rule)) for rule in ("hk2", "zero", "hold")}
    A_l = amps(lambda k_h, z_: np.ones_like(np.asarray(z_, float)))
    P(f"    the matched LCDM box (B = 1 by construction; the Planck 2018 best fit): Planck 8-400 A = {A_l['NL']['planck']:.4f} (pull "
      f"{A_l['NL']['pull']:+.2f} sigma), ACT 40-763 A = {A_l['NL']['act']:.4f} (pull {A_l['NL']['act_pull']:+.2f} sigma)")
    lane.out["numbers"]["lcdm_amps"] = A_l

    def fbox(n, base):
        f = RUNS[n]["foot"]; v = AMPF[f][base]; A_ = LA[n]["hk2"][base]["planck"]
        return float(np.interp(A_, v, FS)) if v[0] <= A_ <= v[-1] else (0.0 if A_ < v[0] else float("inf"))
    XFS, XAMPS = list(NS["FS"]), NS["AMPS"]                                    # XR26 L2b's curve: H_S per-mode phantom x f (K3)

    def feff_x26(A_, base):
        """FP22's scale: the scaling f of XR26's H_S per-mode phantom (growth held) whose Planck 8-400 amplitude equals A_ (FP22's
        extrapolation above f = 1; 0 below the curve's f = 0 floor, which carries H_S's growth)."""
        v = XAMPS[base]
        if A_ < v[0]:
            return 0.0
        if A_ <= v[-1]:
            return float(np.interp(A_, v, XFS))
        return 1.0 + (A_ - v[-1]) / (v[-1] - v[-2]) * (XFS[-1] - XFS[-2])
    for n in MODELS:
        v, f = LA[n]["hk2"], RUNS[n]["foot"]
        P(f"    {n:24s} halofit base: Planck 8-400 A = {v['NL']['planck']:.4f} (pull {v['NL']['pull']:+.2f} sigma, Delta chi^2 "
          f"{v['NL']['dchi2']:+.2f}); ACT 40-763 A = {v['NL']['act']:.4f} (uniform {v['NL']['act_uniform']:.4f}; pull {v['NL']['act_pull']:+.2f}) "
          f"| linear base: Planck {v['lin']['planck']:.4f} (pull {v['lin']['pull']:+.2f}), ACT {v['lin']['act']:.4f}")
        P(f"    {'':24s} R(L) halofit base at L = 40/100/200/400/763: " + "/".join(f"{x:.4f}" for x in v["NL"]["R"].values())
          + f"; low-k brackets (B - 1 = 0 / held below k = {kc[0]:.3f}): Planck A = {LA[n]['zero']['NL']['planck']:.4f} / "
          f"{LA[n]['hold']['NL']['planck']:.4f}; cut factor f_box = {fbox(n, 'NL'):.3f} (halofit) / {fbox(n, 'lin'):.3f} (linear) "
          f"vs the wall f* = {FSTAR[f]['NL']:.3f} / {FSTAR[f]['lin']:.3f} (H_S's: 0.178 / 0.618)")
    FE = {n: {b: feff_x26(LA[n]["hk2"][b]["planck"], b) for b in ("lin", "NL")} for n in MODELS}
    P("    FP22's scale (f_eff = the fraction of XR26's H_S per-mode phantom giving the same Planck 8-400 amplitude; the wall is "
      f"f* = {NS['FSTAR']['lin']:.3f} linear / {NS['FSTAR']['NL']:.3f} halofit): " + "; ".join(
          f"{n}: {FE[n]['lin']:.3f} / {FE[n]['NL']:.3f}" for n in MODELS)
      + "  [FP22's semi-analytic real-space cut in the chain reading: H_K1 0.13/0.16 (canonical), 0.16/0.19 (alt); all separators 0.13-0.26]")
    lane.out["numbers"]["box_lensing"] = {n: dict(amps=LA[n], f_box=dict(NL=fbox(n, "NL"), lin=fbox(n, "lin")), f_eff_fp22_scale=FE[n])
                                          for n in MODELS}
    pl_ok = {n: abs(LA[n]["hk2"]["NL"]["planck"] - PL_AMP[0]) <= 2 * PL_AMP[1] for n in MODELS}
    act_ok = {n: abs(LA[n]["hk2"]["NL"]["act"] - ACT_AMP[0]) <= 2 * ACT_AMP[1] for n in MODELS}
    check("E3 (reported; THE QUESTION) CMB LENSING FROM THE BOX (halofit base): the chain's amplitude lies within 2 sigma of Planck "
          "2018's 8-400 (1.011 +- 0.028) AND of ACT DR6's 40-763 (1.013 +- 0.023) -- per box (the chain reading decides; fp9 is the bridge)",
          "; ".join(f"{n}: Planck {LA[n]['hk2']['NL']['planck']:.4f} ({LA[n]['hk2']['NL']['pull']:+.1f} sigma), ACT "
                    f"{LA[n]['hk2']['NL']['act']:.4f} ({LA[n]['hk2']['NL']['act_pull']:+.1f} sigma): "
                    f"{'pass' if (pl_ok[n] and act_ok[n]) else 'FAIL'}" for n in MODELS),
          all(pl_ok[n] and act_ok[n] for n in MODELS), "the low-k brackets are printed above; ACT's covariance is not used (Planck's "
          "MV band errors weight ACT's range, uniform weights alongside)", load_bearing=False)
    if not MUTATE:
        fb = {n: fbox(n, "NL") for n in MODELS if n.startswith("fp9")}
        check("E2 (reported) THE BOX CUTS THE PER-MODE PHANTOM: in the all-matter reading the cut factor f_box < 1 (halofit base; "
              "the linear base alongside above)", "; ".join(f"{n}: f_box {v:.3f}" for n, v in fb.items()),
              all(v < 1 for v in fb.values()), load_bearing=False)
        ex = {n: LA[n]["hk2"]["NL"]["planck"] - 1 for n in MODELS}
        check("E4 (reported) THE CHAIN READING LENSES LESS THAN THE ALL-MATTER READING (A - 1, halofit base)",
              "; ".join(f"{f}: chain {ex['chain_' + f]:+.4f} vs fp9 {ex['fp9_' + f]:+.4f}" for f in FEET),
              all(ex["chain_" + f] < ex["fp9_" + f] for f in FEET), load_bearing=False)
        check("E5 (reported) THE ALT FOOTING LENSES MORE THAN THE CANONICAL (A - 1, halofit base)",
              "; ".join(f"{r_}: alt {ex[r_ + '_alt']:+.4f} vs canonical {ex[r_ + '_canonical']:+.4f}" for r_ in ("fp9", "chain")),
              all(ex[r_ + "_alt"] > ex[r_ + "_canonical"] for r_ in ("fp9", "chain")), load_bearing=False)

    # ------------------------------------------------------------------------------------------ P(k), sigma_8, cosmic shear
    banner("P  THE NONLINEAR P(k) BOOST, sigma_8 AND THE RECORD'S COSMIC-SHEAR GATE")
    KQ = [0.1, 0.3, 0.5, 1.0, 2.0, 3.0]

    def at_k(arr, q):
        return float(np.exp(np.interp(math.log(q), np.log(kc), np.log(np.maximum(arr, 1e-300))))) if kc[0] <= q <= kc[-1] else float("nan")
    PB = {}
    for n in MODELS:
        PB[n] = {}
        f = RUNS[n]["foot"]
        for zq in (0.0, 0.25, 0.5, 1.0):
            j = ZN.index(zq); rr = R[n][j]
            yb = [float(YD[f]["ib"].ev(max(ZA[j], 0.0), math.log(q))) - 1 for q in KQ] if f in YD else [float("nan")] * len(KQ)
            PB[n][str(zq)] = dict(z=float(ZA[j]), b_m={str(q): at_k(rr["bm"], q) - 1 for q in KQ},
                                  b_lens={str(q): at_k(rr["B"], q) - 1 for q in KQ}, yard_lens={str(q): v for q, v in zip(KQ, yb)},
                                  diag=B[n]["rows"][j]["diag"])
            d_ = B[n]["rows"][j]["diag"]
            P(f"    {n:24s} z {ZA[j]:+.3f}: b_m at k = " + "/".join(f"{q:g}" for q in KQ) + ": "
              + "/".join(f"{PB[n][str(zq)]['b_m'][str(q)]:+.4f}" for q in KQ) + "; B - 1 (lensing): "
              + "/".join(f"{PB[n][str(zq)]['b_lens'][str(q)]:+.4f}" for q in KQ) + " | per-mode yardstick B - 1: "
              + "/".join(f"{v:+.4f}" for v in yb) + f" | y_rms {d_['y_rms']:.3g}, y_th {d_['y_th']:.3g}, on {d_['on_frac']:.3f}, "
              f"cbar {d_['cbar']:.3g}, L {d_['L_com']:.3f} Mpc/h")
    lane.out["numbers"]["Pboost"] = PB
    fp19_pm, fp19_st = FP19["H5"]["Pboost"], FP19["H7"]["headline"]["canonical"]["b"]
    if "fp9_canonical" in PB:
        z0 = PB["fp9_canonical"]["0.0"]["b_m"]
        P("    FP19's linear all-matter boosts at z = 0 (canonical) for comparison with fp9_canonical's b_m: per-mode (H5) k = 0.3/0.5/1: "
          + "/".join(f"{fp19_pm[q]:+.4f}" for q in ("0.3", "0.5", "1.0")) + "; real-space Stein (H7): "
          + "/".join(f"{fp19_st['0.0/' + q]:+.4f}" for q in ("0.3", "0.5", "1.0")) + "; box: "
          + "/".join(f"{z0[q]:+.4f}" for q in ("0.3", "0.5", "1.0")))
    # sigma_8
    Pl = X.l362_plin()
    lk = np.linspace(math.log(1e-4), math.log(kf), 400)

    def S_low(z):
        k_ = np.exp(lk); x = 8.0 * k_
        W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
        return float(np.trapz(k_ ** 3 * np.array([Pl(q, max(z, 0.0)) for q in k_]) / (2 * math.pi ** 2) * W ** 2, lk))
    S8 = {}
    SL = {zq: S_low(ZA[ZN.index(zq)]) for zq in Z_S8}
    for n in MODELS:
        S8[n] = {}
        for zq in Z_S8:
            j = ZN.index(zq); rL = B["lcdm"]["rows"][j]; rM = B[n]["rows"][j]; sl = SL[zq]
            S8[n][str(zq)] = dict(box_m=rM["s8_m"] / rL["s8_m"], box_lens=rM["s8_l"] / rL["s8_m"],
                                  completed_m=math.sqrt((rM["s8_m"] ** 2 + sl) / (rL["s8_m"] ** 2 + sl)),
                                  completed_lens=math.sqrt((rM["s8_l"] ** 2 + sl) / (rL["s8_m"] ** 2 + sl)), s8_lcdm_box=rL["s8_m"], S_low=sl)
        P(f"    {n:24s} sigma_8/LCDM at z = 1/0.5/0.25/0: matter (box) " + "/".join(f"{S8[n][str(z)]['box_m']:.4f}" for z in Z_S8)
          + ", completed " + "/".join(f"{S8[n][str(z)]['completed_m']:.4f}" for z in Z_S8) + "; lensing field (box) "
          + "/".join(f"{S8[n][str(z)]['box_lens']:.4f}" for z in Z_S8) + ", completed " + "/".join(f"{S8[n][str(z)]['completed_lens']:.4f}" for z in Z_S8))
    lane.out["numbers"]["sigma8"] = S8
    s8ok = {n: S8[n]["0.0"]["completed_m"] <= 1.02 for n in MODELS}
    check("G1 (reported) sigma_8 (matter, z = 0, completed below the box's fundamental with linear LCDM) inside FP19's tight band "
          "(<= 1.02)", "; ".join(f"{n}: {S8[n]['0.0']['completed_m']:.4f}" for n in MODELS), all(s8ok.values()), load_bearing=False)
    CS = {}
    jh = ZN.index(0.5)
    for n in MODELS:
        CS[n] = {str(q): B[n]["rows"][jh]["pkb_l"][str(q)] / B["lcdm"]["rows"][jh]["pkb_m"][str(q)] for q in KG_CS}
    check("G2 (reported) THE RECORD'S COSMIC-SHEAR GATE (L364/L367): R(k) = P_lens/P_LCDM <= 1.2 at z = 0.5 (L367's bins, "
          "k = 0.1-1 h/Mpc)", "; ".join(f"{n}: " + "/".join(f"{v:.3f}" for v in CS[n].values()) for n in MODELS),
          all(max(v.values()) <= 1.2 for v in CS.values()), load_bearing=False)
    lane.out["numbers"]["cosmic_shear"] = CS
    FP22_GEXT = {"canonical": 3.5387972549297215e-14, "alt": 3.5821604512699143e-14}      # FP22 D: H_K1 (b), linear 3D rms, z = 0.25
    BS2 = {"canonical": 6.73e-05, "alt": 4.6e-05}                                        # FP22 D_bs2_bound (a0 units)
    XE = {}
    for n in MODELS:
        f = RUNS[n]["foot"]; XE[n] = {}
        for zq in Z_EXT:
            e_ = B[n]["rows"][ZN.index(zq)]["ext"]; XE[n][str(zq)] = e_
            P(f"    X1 {n:24s} z {ZA[ZN.index(zq)]:+.3f}: {e_['n_peaks']} peaks (delta_m >= {DPEAK:g}); web field at the peaks y_ext "
              f"16/50/84% = " + "/".join(f"{v:.2e}" for v in e_["ext_q"]) + f" a0 (rms {e_['ext_rms']:.2e}; median "
              f"{e_['ext_q'][1] * e_['a0_SI']:.2e} m/s^2); the peak cell's own |G| median {e_['cell_q'][1]:.2e}; volume rms {e_['vol_rms']:.2e} a0")
        e25 = XE[n]["0.25"]
        P(f"       vs FP22's linear rms (H_K1 {f}, chain reading, z = 0.25) {FP22_GEXT[f] / e25['a0_SI']:.2e} a0: median x"
          f"{e25['ext_q'][1] / (FP22_GEXT[f] / e25['a0_SI']):.1f}; vs BS2's stacked KiDS bound {BS2[f]:.1e} a0: median x{e25['ext_q'][1] / BS2[f]:.1f}")
    lane.out["numbers"]["X1_web_field_in_kernel"] = XE
    if not MUTATE:
        xr = {n: XE[n]["0.25"]["ext_q"][1] / (FP22_GEXT[RUNS[n]["foot"]] / XE[n]["0.25"]["a0_SI"]) for n in MODELS if n.startswith("chain")}
        check("X1 (reported; FP22's KiDS risk) THE WEB'S BAND-PASSED FIELD IN THE KERNEL AT HALO POSITIONS (chain reading, z = 0.25): "
              "EXPECTED above FP22's linear 3D rms", "; ".join(f"{n}: median y_ext / FP22's linear rms = {v:.2f}" for n, v in xr.items()),
              all(v > 1 for v in xr.values()), "the 27-cell (1.2 Mpc/h) vector mean keeps the field of everything but the halo's own "
              "symmetric part; mesh-limited (0.39 Mpc/h cells): galaxy-scale halos are sub-cell", load_bearing=False)

    # ------------------------------------------------------------------------------------------ E6: the yield's role (both invocations)
    banner("E6 / R1  THE YIELD'S ROLE (the MUTATE contrast) AND THE RESOLUTION PARTNER")
    if "chain_canonical" in B and "chain_canonical_noyield" in B:
        E6 = {}
        for n in ("chain_canonical", "chain_canonical_noyield"):
            A_ = LA[n]["hk2"] if n in LA else amps(box_Bfun(n))
            E6[n] = dict(planck=A_["NL"]["planck"], act=A_["NL"]["act"],
                         B={str(zq): {str(q): at_k(R[n][ZN.index(zq)]["B"], q) - 1 for q in (0.3, 1.0, 2.0, 3.0)} for zq in (1.5, 1.0, 0.8)})
        for n, v in E6.items():
            P(f"    {n:24s}: Planck 8-400 A = {v['planck']:.4f}, ACT {v['act']:.4f} (halofit base); B - 1 at k = 0.3/1/2/3: "
              + "; ".join(f"z {zq}: " + "/".join(f"{x:+.4f}" for x in bq.values()) for zq, bq in v["B"].items()))
        pairs = [(E6["chain_canonical_noyield"]["B"][zq][q], E6["chain_canonical"]["B"][zq][q])
                 for zq in ("1.0", "0.8") for q in ("1.0", "2.0", "3.0") if np.isfinite(E6["chain_canonical"]["B"][zq][q])]
        up = len(pairs) > 0 and all(a_ > b_ for a_, b_ in pairs)
        dA = E6["chain_canonical_noyield"]["planck"] - E6["chain_canonical"]["planck"]
        check("E6 (reported) THE YIELD'S ROLE: removing it raises B_box at z >= 0.8 and k >= 1 h/Mpc, but moves Planck 8-400 by "
              "|Delta A| <= 0.0028 (0.1 sigma): the yield is not what protects CMB lensing",
              f"B raised at z = 0.8, 1, k = 1-3: {up}; Delta A (Planck, halofit base) = {dA:+.4f}", up and abs(dA) <= 0.0028,
              load_bearing=False)
        lane.out["numbers"]["E6"] = E6
    else:
        P("    E6: the other half of the contrast is not in the cache (it is printed by whichever invocation runs after both boxes)")
    # ------------------------------------------------------------------------------------------ R1: the resolution partner
    if "lcdm_hr" in B and "chain_canonical_hr" in B:
        BINH = binning(RUNS["lcdm_hr"]["L"], B["lcdm_hr"]["cnt"])
        RH = ratios("chain_canonical_hr", "lcdm_hr", BINH)
        KS = 0.4
        rows_lr = B_rows(R["chain_canonical"], kc, "canonical")
        rows_hr = B_rows(RH, BINH["kc"], "canonical")
        rows_sp = np.where(KGRID[None, :] >= KS, rows_hr, rows_lr)
        Asp = amps(Bfun_of(rows_sp)); Alr = LA["chain_canonical"]["hk2"]
        R1 = {}
        for zq in (0.0, 0.25, 0.5):
            j = ZN.index(zq)
            lo_ = {str(q): at_k(R["chain_canonical"][j]["B"], q) - 1 for q in (0.3, 0.5, 1.0, 2.0, 3.0)}
            hi_ = {str(q): (float(np.exp(np.interp(math.log(q), np.log(BINH["kc"]), np.log(np.maximum(RH[j]["B"], 1e-300))))) - 1)
                   if BINH["kc"][0] <= q <= BINH["kc"][-1] else float("nan") for q in (0.3, 0.5, 1.0, 2.0, 3.0)}
            R1[str(zq)] = dict(lr=lo_, hr=hi_)
            P(f"    R1 z {ZA[j]:+.3f}: B - 1 at k = 0.3/0.5/1/2/3 -- 100 Mpc/h: " + "/".join(f"{x:+.4f}" for x in lo_.values())
              + "; 50 Mpc/h: " + "/".join(f"{x:+.4f}" for x in hi_.values()))
        P(f"    R1 amplitudes with the 50 Mpc/h B spliced in at k >= {KS} h/Mpc: Planck 8-400 {Asp['NL']['planck']:.4f} ({Asp['NL']['pull']:+.2f} sigma; "
          f"100 Mpc/h alone {Alr['NL']['planck']:.4f}), ACT {Asp['NL']['act']:.4f} ({Asp['NL']['act_pull']:+.2f}; alone {Alr['NL']['act']:.4f}) "
          f"halofit base; linear base Planck {Asp['lin']['planck']:.4f}, ACT {Asp['lin']['act']:.4f}")
        same = ((abs(Asp["NL"]["planck"] - PL_AMP[0]) <= 2 * PL_AMP[1]) == (abs(Alr["NL"]["planck"] - PL_AMP[0]) <= 2 * PL_AMP[1]) and
                (abs(Asp["NL"]["act"] - ACT_AMP[0]) <= 2 * ACT_AMP[1]) == (abs(Alr["NL"]["act"] - ACT_AMP[0]) <= 2 * ACT_AMP[1]))
        check("R1 (reported) THE RESOLUTION PARTNER (50 Mpc/h, 0.195 Mpc/h cells, the decisive cell): the Planck/ACT verdicts (halofit "
              "base) are unchanged when its B replaces the 100 Mpc/h box's at k >= 0.4 h/Mpc",
              f"Planck {Alr['NL']['planck']:.4f} -> {Asp['NL']['planck']:.4f}; ACT {Alr['NL']['act']:.4f} -> {Asp['NL']['act']:.4f}; "
              f"verdicts unchanged: {same}", same, load_bearing=False)
        XH = B["chain_canonical_hr"]["rows"][ZN.index(0.25)]["ext"]
        P(f"    R1 X1 at 0.195 Mpc/h (z {ZA[ZN.index(0.25)]:+.3f}): {XH['n_peaks']} peaks; web field at the peaks y_ext 16/50/84% = "
          + "/".join(f"{v:.2e}" for v in XH["ext_q"]) + f" a0; volume rms {XH['vol_rms']:.2e} a0")
        lane.out["numbers"]["R1"] = dict(B=R1, amps_spliced=Asp, amps_lr=Alr, X1_hr=XH, k_splice=KS)
    elif not MUTATE:
        P("    R1: the resolution partner is not in the cache (not run)")
    # ------------------------------------------------------------------------------------------ R2: 128^3 vs 256^3, one realisation
    if "lcdm_128" in B and "chain_canonical_128" in B:
        NG2 = RUNS["lcdm_128"]["NG"]
        BIN2 = binning(BOX["L"], B["lcdm_128"]["cnt"], NG2)
        R2r = ratios("chain_canonical_128", "lcdm_128", BIN2)
        A128 = amps(Bfun_of(B_rows(R2r, BIN2["kc"], "canonical"))); Alr = LA["chain_canonical"]["hk2"]
        R2 = {}
        for zq in (0.0, 0.25, 0.5):
            j = ZN.index(zq)
            c_ = {str(q): (float(np.exp(np.interp(math.log(q), np.log(BIN2["kc"]), np.log(np.maximum(R2r[j]["B"], 1e-300))))) - 1)
                  if BIN2["kc"][0] <= q <= BIN2["kc"][-1] else float("nan") for q in (0.3, 0.5, 1.0, 2.0)}
            f_ = {str(q): at_k(R["chain_canonical"][j]["B"], q) - 1 for q in (0.3, 0.5, 1.0, 2.0)}
            R2[str(zq)] = dict(c128=c_, c256=f_)
            P(f"    R2 z {ZA[j]:+.3f}: B - 1 at k = 0.3/0.5/1/2 -- 128^3 (0.78 Mpc/h cells): " + "/".join(f"{x:+.4f}" for x in c_.values())
              + "; 256^3 (0.39): " + "/".join(f"{x:+.4f}" for x in f_.values()))
        cells = [("0.78 (128^3)", A128), ("0.39 (256^3)", Alr)]
        if "R1" in lane.out["numbers"]:
            cells.append(("0.195 (50 Mpc/h, spliced at k >= 0.4)", lane.out["numbers"]["R1"]["amps_spliced"]))
        P("    R2 the decisive cell's amplitudes by cell size [Mpc/h] (halofit base; linear base in brackets): " + "; ".join(
            f"{c}: Planck {v['NL']['planck']:.4f} ({v['lin']['planck']:.4f}), ACT {v['NL']['act']:.4f} ({v['lin']['act']:.4f})" for c, v in cells))
        same2 = ((abs(A128["NL"]["planck"] - PL_AMP[0]) <= 2 * PL_AMP[1]) == (abs(Alr["NL"]["planck"] - PL_AMP[0]) <= 2 * PL_AMP[1]) and
                 (abs(A128["NL"]["act"] - ACT_AMP[0]) <= 2 * ACT_AMP[1]) == (abs(Alr["NL"]["act"] - ACT_AMP[0]) <= 2 * ACT_AMP[1]))
        check("R2 (reported; XR18b's condition 4) 128^3 vs 256^3 ON ONE REALISATION: the decisive cell's Planck/ACT verdicts (halofit "
              "base) are unchanged when the cell doubles", f"Planck {A128['NL']['planck']:.4f} (0.78) vs {Alr['NL']['planck']:.4f} (0.39); "
              f"ACT {A128['NL']['act']:.4f} vs {Alr['NL']['act']:.4f}; verdicts unchanged: {same2}", same2, load_bearing=False)
        lane.out["numbers"]["R2"] = dict(B=R2, amps_128=A128, amps_256=Alr, cells=[c for c, _ in cells])
    elif not MUTATE:
        P("    R2: the 128^3 partner is not in the cache (not run)")

    # ------------------------------------------------------------------------------------------ M1/M2: the low-field monitor
    banner("M  THE LOW-FIELD MONITOR (XR18b's condition 5): the phantom's growth rate after z_q0; how low the kernel's argument gets")
    GRW = {}
    for n in B:
        if RUNS[n]["gravity"] != "hy":
            continue
        ref = "lcdm_hr" if n.endswith("_hr") else ("lcdm_128" if n.endswith("_128") else "lcdm")
        if ref not in B:
            continue
        bn = binning(RUNS[n].get("L", BOX["L"]), B[ref]["cnt"], RUNS[n].get("NG"))
        rates, rcor, rl = [], [], []
        hkq = C.HK1(sep, sep.a0_code(RUNS[n]["foot"]))
        for j in range(1, len(ZN)):
            if ZN[j - 1] > 0.5:
                continue
            dla = math.log(AA[j] / AA[j - 1])
            p0, p1 = bn["bs"](B[n]["rows"][j - 1]["spp"])[bn["ok"]], bn["bs"](B[n]["rows"][j]["spp"])[bn["ok"]]
            m0, m1 = bn["bs"](B[n]["rows"][j - 1]["smm"])[bn["ok"]], bn["bs"](B[n]["rows"][j]["smm"])[bn["ok"]]
            h0 = -np.expm1(-0.5 * (bn["kc"] * hkq.L_com(AA[j - 1])) ** 2); h1 = -np.expm1(-0.5 * (bn["kc"] * hkq.L_com(AA[j])) ** 2)
            ok_ = (p0 > 1e-6 * m0) & (p1 > 0)
            if ok_.any():
                rates.append(float(np.max(np.log(p1[ok_] / p0[ok_]) / dla)))
                rcor.append(float(np.max(np.log((p1 / (h1 ** 4 * m1))[ok_] / (p0 / (h0 ** 4 * m0))[ok_]) / dla)))
            l0, l1 = bn["bs"](B[ref]["rows"][j - 1]["smm"])[bn["ok"]], bn["bs"](B[ref]["rows"][j]["smm"])[bn["ok"]]
            rl.append(float(np.max(np.log(l1 / l0) / dla)))
        GRW[n] = dict(max_rate_pp=max(rates) if rates else float("nan"), max_rate_amplification=max(rcor) if rcor else float("nan"),
                      max_rate_lcdm_matter=max(rl) if rl else float("nan"))
        P(f"    M1 {n:24s}: at z <= 0.5 the phantom's own amplification max d ln[P_pp/(h_k^4 P_mm)]/d ln a = "
          f"{GRW[n]['max_rate_amplification']:.2f} per e-fold (raw d ln P_pp/d ln a {GRW[n]['max_rate_pp']:.2f}; the LCDM matter's "
          f"{GRW[n]['max_rate_lcdm_matter']:.2f})")
    check("M1 (reported) NO RUNAWAY AFTER z_q0: the phantom's own amplification d ln[P_pp/(h_k^4 P_mm)]/d ln a stays <= 5 per e-fold in "
          "every bin with P_pp/P_mm > 1e-6 between consecutive outputs at z <= 0.5, in every model box (XR18b's DE12-type growth: up to "
          "1.4e5 H where the web's field is absent)", "; ".join(f"{n}: {v['max_rate_amplification']:.2f}" for n, v in GRW.items()),
          all(np.isfinite(v["max_rate_amplification"]) and v["max_rate_amplification"] <= 5 for v in GRW.values()), load_bearing=False)
    lane.out["numbers"]["M1"] = GRW
    M2 = {}
    for n in ("chain_canonical_128", "chain_canonical_hr"):
        if n not in B:
            continue
        M2[n] = {}
        for zq in (0.5, 0.25, 0.0):
            lo_ = B[n]["rows"][ZN.index(zq)]["low"]; M2[n][str(zq)] = lo_
            P(f"    M2 {n:22s} z {ZA[ZN.index(zq)]:+.3f}: y_rms {lo_['y_rms']:.2e}, min {lo_['y_min']:.1e}; volume quantiles "
              + "/".join(f"{q:g}: {v:.1e}" for q, v in zip(LOW_Q, lo_["vol_q"])) + "; baryon-mass quantiles "
              + "/".join(f"{v:.1e}" for v in lo_["mass_q"]) + "; volume / mass fraction below 1e-6, 1e-5, 1e-4 a0 and y_rms/100: "
              + ", ".join(f"{v:.1e}/{w_:.1e}" for v, w_ in zip(lo_["vol_f"], lo_["mass_f"]))
              + f"; halo-centre cells ({lo_['n_peaks']}): y 16/50/84% " + "/".join(f"{v:.1e}" for v in lo_["peak_q"]))
    if M2:
        lane.out["numbers"]["M2"] = M2
    else:
        P("    M2: the monitored partners are not in the cache (not run)")

    banner("VERDICT")
    for n in MODELS:
        v = LA[n]["hk2"]
        P(f"  {n}: Planck 8-400 A = {v['NL']['planck']:.4f} ({v['NL']['pull']:+.1f} sigma) halofit base / {v['lin']['planck']:.4f} "
          f"({v['lin']['pull']:+.1f}) linear base; ACT DR6 {v['NL']['act']:.4f} ({v['NL']['act_pull']:+.1f}) / {v['lin']['act']:.4f} "
          f"({v['lin']['act_pull']:+.1f}); cut f_eff (FP22's scale) {FE[n]['lin']:.3f} / {FE[n]['NL']:.3f}")
    P("  (the per-mode yardstick: " + "; ".join(f"{f}: {YAMP[f]['NL']['planck']:.4f} halofit / {YAMP[f]['lin']['planck']:.4f} linear" for f in FEET) + ")")
    sys.exit(lane.finish())
