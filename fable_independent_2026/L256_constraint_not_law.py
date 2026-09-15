#!/usr/bin/env python3
"""L256 -- IS THE RADIAL ACCELERATION RELATION A FORCE LAW, OR A CONSTRAINT ON THE INITIAL DATA?

THE STRUCTURAL MOVE THIS LANE TESTS.  Every completion this programme has attempted is a DYNAMICAL law --
an action, a modified field equation, a new field -- and the pincer has closed on all of them: the kernel as
modified gravity gives a Cassini-excluded external-field quadrupole, the same kernel as modified inertia is
lensing-dead at 21 sigma, and L248 showed that the phantom carrying the weak-lensing signal cannot be the
galaxy's own bounded sector.  The untried structural move is to STOP MODIFYING ANYTHING: gravity is exactly
Einstein's, the dark matter is exactly collisionless and cold, and the radial acceleration relation holds not
because a force produces it but because the galaxies that EXIST occupy a thin, selected subset of the possible
baryon-plus-halo configurations -- an ATTRACTOR of the assembly process rather than a law of motion.

BE HONEST ABOUT WHAT THIS IS.  This is NOT new.  It is, essentially, the standard LambdaCDM explanation --
feedback self-regulation driving discs onto a tight relation -- and it is the reading this programme has spent
its whole existence arguing against.  The only thing this lane can add is a SHARP STRUCTURAL DISCRIMINATOR,
and there is exactly one:

    A FORCE LAW IS EXACT AND INSTANTANEOUS.  It holds for every system at every time, with zero intrinsic
    scatter, whether or not the system has had time to settle.  A recently disturbed galaxy obeys it just as
    a quiescent one does, because the field is solved afresh on every slice from the instantaneous baryons
    (that is precisely this programme's own L98 result: the cuscuton makes the RAR a single-valued law with
    identically zero halo-assembly scatter).

    A SELECTION / ATTRACTOR READING ONLY HAS TO HOLD FOR RELAXED SYSTEMS.  It must FAIL, measurably, for
    systems that have not had enough dynamical times to reach the attractor, and the size of the failure must
    scale with the ratio of dynamical time to age.

So the two readings make OPPOSITE predictions about one measurable thing: whether the RAR residual scatter
depends on how many orbits a galaxy has completed.  That is what is measured here, on the 175 SPARC rotation
curves.

------------------------------------------------------------------------------------------------------------
PRE-REGISTRATION.  Every number below is fixed HERE, in the docstring, before any split is computed.  The
thresholds appear again as named constants at the top of the code and are printed at run time.

  RELAXATION PROXY.  N_orb = T_AGE * V_out / (2 pi R_out): the number of orbital periods completed at the
  OUTERMOST measured radius of the rotation curve in an assumed disc age T_AGE = 10 Gyr.  This is the
  cleanest available "has this system had time to settle" variable, and it is computed from the rotation
  curve itself with nothing fitted.

  SPLIT.  SPLIT_NORB = 10 orbits.  Ten orbital periods is the standard rule of thumb for phase mixing to
  complete; it is chosen for that reason and NOT from the data.

  WHAT EACH READING PREDICTS FOR THE RATIO  r = sigma_int(N_orb < 10) / sigma_int(N_orb >= 10) ,
  where sigma_int is the galaxy-to-galaxy scatter in the mean RAR residual AFTER the per-object
  observational error budget has been subtracted in quadrature:

      FORCE LAW                      r = 1.00 exactly.  No dependence on assembly state is permitted at all.
      SELECTION / ATTRACTOR          r >= SELECTION_RATIO_MIN = 1.3.  A 30% excess is the minimum a reading
                                     in which relaxation is what MAKES the relation can produce while still
                                     being called an explanation; anything smaller is an attractor so fast
                                     that it is observationally indistinguishable from a law.

  DECISION RULE (fixed here).  The ratio's 95% bootstrap interval over galaxies decides:
      lower bound > 1.3                  -> favours the SELECTION reading
      upper bound < 1.3 and interval
        contains 1.0                     -> favours the FORCE-LAW reading (or any relation with no assembly
                                            dependence); the attractor prediction is excluded at its own
                                            stated minimum
      interval straddles both            -> UNDECIDED, and the lane says so

  THE CONFOUND, NAMED IN ADVANCE.  N_orb is LOW exactly for extended, low-surface-brightness, slowly rotating
  dwarfs -- which are also the galaxies with the worst distances, the worst inclinations, the worst
  mass-to-light ratios and the largest velocity errors.  Raised scatter in the least-relaxed bin is therefore
  confounded BY CONSTRUCTION.  Three controls are pre-registered:
      (a) a forward observational error budget per galaxy (distance, inclination, velocity, mass-to-light),
          subtracted in quadrature bin by bin;
      (b) a GOLD cut: SPARC quality flag Q = 1, median velocity error below 5%, and a distance NOT from the
          Hubble flow (f_D != 1), i.e. TRGB / Cepheid / cluster / supernova distances only;
      (c) a CONFOUND-REVERSING axis: gas fraction.  Gas-dominated galaxies are less evolved (the attractor
          reading says: MORE scatter) but their baryonic mass is measured from HI with NO mass-to-light ratio
          at all (the observational-confound reading says: LESS scatter).  The two explanations predict
          OPPOSITE signs on this axis, so it breaks the degeneracy the other two controls can only bound.

  WHAT A POSITIVE RESULT WOULD MEAN FOR THIS PROGRAMME.  It would be an argument FOR standard gravity plus
  cold dark matter with an assembly attractor, and AGAINST this programme's own modified-force reading.  It
  is reported that way whichever way the numbers fall.

  WHAT IS NOT CLAIMED.  Nothing here derives a_0 from assembly.  The epoch coincidence is reported in V8 as a
  coincidence with a number attached, and as a statement about the REACH of this sample, not as a derivation.
------------------------------------------------------------------------------------------------------------

Checks state measurement and threshold separately; no literal-True conditions.  Both a_0 footings throughout.
"""
import glob, json, math, os, sys
import numpy as np

# ------------------------------------------------------------------ PRE-REGISTERED CONSTANTS (see docstring)
T_AGE_GYR           = 10.0     # assumed disc age setting the "how many orbits" clock
SPLIT_NORB          = 10.0     # orbits at the outermost measured radius -- the relaxation split
SELECTION_RATIO_MIN = 1.3      # the attractor reading's minimum predicted scatter excess
FORCE_RATIO         = 1.0      # the force law's exact prediction
GOLD_Q              = 1        # SPARC quality flag for the gold cut
GOLD_EV_FRAC        = 0.05     # median velocity error fraction for the gold cut
GAS_RICH_FRAC       = 0.5      # gas-dominated threshold on M_gas/M_bar
ML_SCATTER_DEX      = 0.11     # scatter on log10(Upsilon_[3.6]) (population-synthesis floor, stated)
UPS_D, UPS_B        = 0.5, 0.7 # the standard SPARC mass-to-light ratios used elsewhere in this repo
POINT_EV_FRAC       = 0.10     # per-point velocity error cut (same as L92/L232)
MIN_POINTS          = 4        # minimum retained points per galaxy
DETREND_DEX         = 0.25     # width of the log10 g_bar bins used to remove any global tilt
NBOOT               = 4000     # bootstrap resamples over galaxies

A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
G, C_LIGHT, KPC, KMS, GYR, MSUN = 6.674e-11, 2.99792458e8, 3.0857e19, 1.0e3, 3.1557e16, 1.989e30
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "real_research", "data")
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)

print(__doc__)
print("PRE-REGISTERED THRESHOLDS AS RUN:")
print(f"    T_AGE = {T_AGE_GYR} Gyr | SPLIT_NORB = {SPLIT_NORB} orbits | force law r = {FORCE_RATIO:.2f} | "
      f"attractor r >= {SELECTION_RATIO_MIN:.2f}")
print(f"    gold cut: Q = {GOLD_Q}, median eV/V < {GOLD_EV_FRAC}, distance method != 1 (not Hubble flow)")
print(f"    gas-dominated: M_gas/M_bar > {GAS_RICH_FRAC} | M/L scatter {ML_SCATTER_DEX} dex | "
      f"point cut eV/V < {POINT_EV_FRAC}, >= {MIN_POINTS} points\n")
OUT["prereg"] = dict(T_AGE_GYR=T_AGE_GYR, SPLIT_NORB=SPLIT_NORB, SELECTION_RATIO_MIN=SELECTION_RATIO_MIN,
                     FORCE_RATIO=FORCE_RATIO, GOLD_Q=GOLD_Q, GOLD_EV_FRAC=GOLD_EV_FRAC,
                     GAS_RICH_FRAC=GAS_RICH_FRAC, ML_SCATTER_DEX=ML_SCATTER_DEX,
                     POINT_EV_FRAC=POINT_EV_FRAC, MIN_POINTS=MIN_POINTS, DETREND_DEX=DETREND_DEX)

# ------------------------------------------------------------------ the master table (Lelli et al. 2016)
mrt = open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")).read().splitlines()
start = [i for i, l in enumerate(mrt) if l.strip() and set(l.strip()) == {"-"}][-1] + 1
MASTER = {}
for line in mrt[start:]:
    t = line.split()
    if len(t) != 19: continue                       # every row of this table has exactly 19 fields; verified
    MASTER[t[0]] = dict(T=int(t[1]), D=float(t[2]), eD=float(t[3]), fD=int(t[4]), inc=float(t[5]),
                        einc=float(t[6]), L36=float(t[7]), Reff=float(t[9]), SBeff=float(t[10]),
                        Rdisk=float(t[11]), SBdisk=float(t[12]), MHI=float(t[13]), Vflat=float(t[15]),
                        Q=int(t[17]))
print(f"    master table: {len(MASTER)} galaxies parsed")

# ------------------------------------------------------------------ the rotation curves
def nu_rar(gb, a0):
    """the RAR interpolating function -- this programme's own kernel (L227): g = g_bar/(1-exp(-sqrt(g_bar/a0)))"""
    x = np.sqrt(np.maximum(gb, 1e-30)/a0)
    return gb/(1.0 - np.exp(-x))
def dlog_slope(gb, a0, h=1e-3):
    """d log10 g_pred / d log10 g_bar, evaluated numerically -- how a horizontal M/L shift moves the residual"""
    lo, hi = gb*10**(-h), gb*10**(+h)
    return (np.log10(nu_rar(hi, a0)) - np.log10(nu_rar(lo, a0)))/(2*h)

GAL = []
nfile = nomaster = nshort = 0
for fn in sorted(glob.glob(os.path.join(DATA, "sparc_data", "*_rotmod.dat"))):
    nfile += 1
    name = os.path.basename(fn).replace("_rotmod.dat", "")
    if name not in MASTER: nomaster += 1; continue
    m = MASTER[name]
    try:
        d = np.genfromtxt(fn, comments="#")
    except Exception:
        continue
    if d.ndim != 2 or d.shape[1] < 6: continue
    R, Vo, eV, Vg, Vd, Vb = (d[:, i] for i in range(6))
    keep = (R > 0) & (Vo > 0) & (eV > 0) & (eV/Vo < POINT_EV_FRAC)
    if keep.sum() < MIN_POINTS: nshort += 1; continue
    R, Vo, eV, Vg, Vd, Vb = R[keep], Vo[keep], eV[keep], Vg[keep], Vd[keep], Vb[keep]
    Vb2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
    ok = Vb2 > 0
    if ok.sum() < MIN_POINTS: nshort += 1; continue
    R, Vo, eV, Vg, Vd, Vb, Vb2 = R[ok], Vo[ok], eV[ok], Vg[ok], Vd[ok], Vb[ok], Vb2[ok]
    r_m = R*KPC
    gbar = Vb2*KMS**2/r_m
    gobs = Vo**2*KMS**2/r_m
    f_star = (UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb))/Vb2        # stellar share of g_bar, per point
    # number of orbits completed in T_AGE, per point and at the outermost measured radius
    norb_pt = (T_AGE_GYR*GYR)*(Vo*KMS)/(2*math.pi*r_m)
    Mstar = UPS_D*m["L36"]*1e9                                       # M_sun, disc M/L (bulge L not tabulated)
    Mgas = 1.33*m["MHI"]*1e9                                         # helium-corrected HI mass
    fgas = Mgas/(Mgas + Mstar) if (Mgas + Mstar) > 0 else np.nan
    GAL.append(dict(name=name, R=R, Vo=Vo, eV=eV, gbar=gbar, gobs=gobs, f_star=f_star,
                    norb_pt=norb_pt, norb_out=float(norb_pt[-1]), n=int(len(R)),
                    D=m["D"], eD=m["eD"], fD=m["fD"], inc=m["inc"], einc=m["einc"], Q=m["Q"], T=m["T"],
                    SBdisk=m["SBdisk"], fgas=float(fgas),
                    ev_med=float(np.median(eV/Vo))))
print(f"    rotation curves: {nfile} files, {nomaster} without a master row, {nshort} too short after cuts "
      f"-> {len(GAL)} galaxies, {sum(g['n'] for g in GAL)} points retained\n")
OUT["n_galaxies"] = len(GAL); OUT["n_points"] = int(sum(g["n"] for g in GAL))

# ------------------------------------------------------------------ V1: the baseline relation
print("V1 -- the baseline: reproduce this repo's own RAR scatter before splitting anything")
for tag, a0 in A0.items():
    gb = np.concatenate([g["gbar"] for g in GAL]); go = np.concatenate([g["gobs"] for g in GAL])
    res = np.log10(go) - np.log10(nu_rar(gb, a0))
    OUT[f"rms_raw_{tag}"] = float(np.std(res)); OUT[f"mean_raw_{tag}"] = float(np.mean(res))
    print(f"    [{tag:9s}] a_0 = {a0:.4e}: point scatter {np.std(res):.4f} dex about a mean offset of "
          f"{np.mean(res):+.4f} dex")
ref = 0.145                                                          # L98's control value, stated separately
worst = max(abs(OUT[f"rms_raw_{t}"] - ref) for t in A0)
check("V1 [THE SAMPLE AND THE KERNEL REPRODUCE THIS REPO'S OWN RAR SCATTER] the point-by-point residual "
      f"scatter about the kernel is measured on both footings and compared with the value L98's controls "
      f"recorded for the same data ({ref} dex); agreement to better than 0.03 dex means nothing has been "
      "broken in the loading before any split is taken",
      worst < 0.03,
      f"{OUT['rms_raw_canonical']:.4f} dex (canonical) / {OUT['rms_raw_alt']:.4f} dex (alt) against {ref}; "
      f"largest deviation {worst:.4f} dex. The mean offsets ({OUT['mean_raw_canonical']:+.3f} / "
      f"{OUT['mean_raw_alt']:+.3f} dex) are the known gap between these two footings and the 1.2e-10 that "
      "SPARC itself fits, and they are removed by the detrending below -- an offset cannot produce a "
      "relaxation-dependent scatter")

# ------------------------------------------------------------------ detrended residuals + the error budget
def build(tag, a0):
    """per-galaxy mean residual after removing any global tilt, and its forward observational error budget"""
    gb = np.concatenate([g["gbar"] for g in GAL])
    res = np.concatenate([np.log10(g["gobs"]) - np.log10(nu_rar(g["gbar"], a0)) for g in GAL])
    lg = np.log10(gb)
    edges = np.arange(np.floor(lg.min()/DETREND_DEX)*DETREND_DEX, lg.max() + DETREND_DEX, DETREND_DEX)
    idx = np.clip(np.digitize(lg, edges) - 1, 0, len(edges) - 2)
    med = np.array([np.median(res[idx == k]) if (idx == k).sum() >= 5 else np.nan for k in range(len(edges)-1)])
    fill = np.nanmedian(res)
    med = np.where(np.isfinite(med), med, fill)
    k = 0
    for g in GAL:
        n = g["n"]; sl = slice(k, k + n); k += n
        eps = res[sl] - med[idx[sl]]                                  # detrended per-point residual
        g[f"eps_{tag}"] = eps
        g[f"dbar_{tag}"] = float(np.mean(eps))
        # --- forward observational error budget on that per-galaxy mean, in dex
        s_D = (g["eD"]/g["D"])/math.log(10) if g["D"] > 0 else 0.0    # D shifts g_obs by 1/D, g_bar not at all
        ir = math.radians(g["inc"]); er = math.radians(g["einc"])
        s_i = 2*er/math.tan(ir)/math.log(10) if 0 < ir < math.pi/2 else 0.30
        s_V = float(np.sqrt(np.mean((2*g["eV"]/g["Vo"]/math.log(10))**2))/math.sqrt(n))
        s_ML = float(np.mean(dlog_slope(g["gbar"], a0)*g["f_star"])*ML_SCATTER_DEX)
        g[f"spred_{tag}"] = float(math.sqrt(s_D**2 + s_i**2 + s_V**2 + s_ML**2))
        g[f"budget_{tag}"] = dict(D=s_D, inc=s_i, V=s_V, ML=abs(s_ML))
for tag, a0 in A0.items(): build(tag, a0)

def scatters(sub, tag):
    """measured galaxy-to-galaxy scatter, predicted observational scatter, and the intrinsic remainder"""
    d = np.array([g[f"dbar_{tag}"] for g in sub]); p = np.array([g[f"spred_{tag}"] for g in sub])
    sm = float(np.std(d, ddof=1)) if len(d) > 1 else float("nan")
    sp = float(np.sqrt(np.mean(p**2)))
    return sm, sp, float(math.sqrt(max(sm**2 - sp**2, 0.0)))

def ratio_ci(lo_set, hi_set, tag, use_int=True):
    """bootstrap the low/high scatter ratio by resampling galaxies inside each bin"""
    rng = np.random.default_rng(20260914)
    out = []
    for _ in range(NBOOT):
        a = [lo_set[i] for i in rng.integers(0, len(lo_set), len(lo_set))]
        b = [hi_set[i] for i in rng.integers(0, len(hi_set), len(hi_set))]
        sa = scatters(a, tag)[2 if use_int else 0]; sb = scatters(b, tag)[2 if use_int else 0]
        if sb > 0: out.append(sa/sb)
    out = np.array(out)
    return (float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5)), float(np.median(out)),
            float(np.mean(out > SELECTION_RATIO_MIN)))

# ------------------------------------------------------------------ V2: does the sample have the power?
print("\nV2 -- the power statement: are there enough genuinely unrelaxed galaxies in SPARC to run this at all?")
norb = np.array([g["norb_out"] for g in GAL])
nlo = int((norb < SPLIT_NORB).sum())
OUT["norb_min"] = float(norb.min()); OUT["norb_med"] = float(np.median(norb))
OUT["norb_max"] = float(norb.max()); OUT["n_low"] = nlo; OUT["n_high"] = len(GAL) - nlo
print(f"    N_orb at the outermost measured radius spans {norb.min():.1f} to {norb.max():.1f}, median "
      f"{np.median(norb):.1f}")
print(f"    below the pre-registered split of {SPLIT_NORB:.0f} orbits: {nlo} galaxies; at or above it: "
      f"{len(GAL)-nlo}")
check("V2 [THE SPLIT DIVIDES THE SAMPLE INTO TWO USABLE BINS] the number of orbital periods completed at the "
      "outermost measured radius is computed for every galaxy and compared with the pre-registered split of "
      f"{SPLIT_NORB:.0f}; at least 15 galaxies on the sparse side are required for a scatter ratio to mean "
      "anything",
      min(nlo, len(GAL)-nlo) >= 15,
      f"{nlo} galaxies below {SPLIT_NORB:.0f} orbits and {len(GAL)-nlo} at or above, out of {len(GAL)}. "
      f"The full range is {norb.min():.1f}-{norb.max():.1f} orbits: even the sparsest SPARC galaxy has "
      "completed several orbits at its last measured point, which is the ceiling on this test's reach and is "
      "quantified in V8")

# ------------------------------------------------------------------ V3: the raw split
print("\nV3 -- THE MEASUREMENT: galaxy-to-galaxy RAR scatter split by the relaxation proxy (raw, no controls)")
for tag in A0:
    lo = [g for g in GAL if g["norb_out"] < SPLIT_NORB]; hi = [g for g in GAL if g["norb_out"] >= SPLIT_NORB]
    sm_l, sp_l, si_l = scatters(lo, tag); sm_h, sp_h, si_h = scatters(hi, tag)
    lo95, hi95, med, pgt = ratio_ci(lo, hi, tag, use_int=False)
    OUT[f"v3_{tag}"] = dict(n_lo=len(lo), n_hi=len(hi), sm_lo=sm_l, sm_hi=sm_h, sp_lo=sp_l, sp_hi=sp_h,
                            si_lo=si_l, si_hi=si_h, ratio_meas=sm_l/sm_h, ci=[lo95, hi95], p_gt_min=pgt)
    print(f"    [{tag:9s}] least relaxed (N_orb < {SPLIT_NORB:.0f}, n={len(lo)}): measured scatter "
          f"{sm_l:.4f} dex, error budget predicts {sp_l:.4f}")
    print(f"                more relaxed (N_orb >= {SPLIT_NORB:.0f}, n={len(hi)}): measured scatter "
          f"{sm_h:.4f} dex, error budget predicts {sp_h:.4f}")
    print(f"                RAW measured ratio = {sm_l/sm_h:.3f}, 95% bootstrap [{lo95:.3f}, {hi95:.3f}]; "
          f"P(ratio > {SELECTION_RATIO_MIN}) = {pgt:.3f}")
rr = OUT["v3_canonical"]["ratio_meas"]
check("V3 [THE LEAST-RELAXED GALAXIES SCATTER MORE ABOUT THE RELATION, BEFORE ANY CONTROL] the galaxy-to-"
      "galaxy scatter in the mean detrended RAR residual is measured separately in the two pre-registered "
      f"relaxation bins and their ratio compared with the attractor reading's stated minimum of "
      f"{SELECTION_RATIO_MIN}",
      rr > SELECTION_RATIO_MIN,
      f"raw ratio {rr:.3f} (canonical) / {OUT['v3_alt']['ratio_meas']:.3f} (alt), 95% interval "
      f"[{OUT['v3_canonical']['ci'][0]:.3f}, {OUT['v3_canonical']['ci'][1]:.3f}]. This is the RAW number and "
      "it is confounded by construction -- the least-relaxed bin is also the worst-measured bin. V4-V6 are "
      "the controls, and they decide, not this")

# ------------------------------------------------------------------ V4: the error budget subtracted
print("\nV4 -- CONTROL (a): the forward observational error budget, subtracted in quadrature")
for tag in A0:
    lo = [g for g in GAL if g["norb_out"] < SPLIT_NORB]; hi = [g for g in GAL if g["norb_out"] >= SPLIT_NORB]
    for nm, s in (("least relaxed", lo), ("more relaxed", hi)):
        b = {k: float(np.sqrt(np.mean([g[f"budget_{tag}"][k]**2 for g in s]))) for k in ("D", "inc", "V", "ML")}
        print(f"    [{tag:9s}] {nm:13s} budget: distance {b['D']:.4f}, inclination {b['inc']:.4f}, "
              f"velocity {b['V']:.4f}, mass-to-light {b['ML']:.4f} dex")
    si_l = scatters(lo, tag)[2]; si_h = scatters(hi, tag)[2]
    lo95, hi95, med, pgt = ratio_ci(lo, hi, tag, use_int=True)
    OUT[f"v4_{tag}"] = dict(si_lo=si_l, si_hi=si_h, ratio_int=(si_l/si_h if si_h > 0 else float("nan")),
                            ci=[lo95, hi95], p_gt_min=pgt)
    print(f"                intrinsic remainder: {si_l:.4f} dex (least relaxed) vs {si_h:.4f} dex (more "
          f"relaxed) -> ratio {si_l/si_h if si_h>0 else float('nan'):.3f}, "
          f"95% [{lo95:.3f}, {hi95:.3f}], P(> {SELECTION_RATIO_MIN}) = {pgt:.3f}")
ri = OUT["v4_canonical"]["ratio_int"]; ci = OUT["v4_canonical"]["ci"]
check("V4 [THE EXCESS SURVIVES THE OBSERVATIONAL ERROR BUDGET] the per-galaxy distance, inclination, velocity "
      "and mass-to-light errors are propagated to the mean residual, subtracted in quadrature bin by bin, and "
      f"the remaining intrinsic ratio compared with the attractor minimum {SELECTION_RATIO_MIN}; the "
      "pre-registered decision rule requires the 95% lower bound to clear it",
      ci[0] > SELECTION_RATIO_MIN,
      f"error-corrected ratio {ri:.3f}, 95% bootstrap [{ci[0]:.3f}, {ci[1]:.3f}] (canonical); alt "
      f"{OUT['v4_alt']['ratio_int']:.3f} [{OUT['v4_alt']['ci'][0]:.3f}, {OUT['v4_alt']['ci'][1]:.3f}]. "
      f"The force law's prediction is exactly {FORCE_RATIO:.2f}")

# ------------------------------------------------------------------ V5: the gold cut
print("\nV5 -- CONTROL (b): the gold cut -- only galaxies whose data cannot be blamed")
GOLD = [g for g in GAL if g["Q"] == GOLD_Q and g["ev_med"] < GOLD_EV_FRAC and g["fD"] != 1]
gl = [g for g in GOLD if g["norb_out"] < SPLIT_NORB]; gh = [g for g in GOLD if g["norb_out"] >= SPLIT_NORB]
print(f"    gold sample: {len(GOLD)} of {len(GAL)} galaxies (Q = {GOLD_Q}, median eV/V < {GOLD_EV_FRAC}, "
      f"distance method != 1) -> {len(gl)} least relaxed, {len(gh)} more relaxed")
for tag in A0:
    if len(gl) >= 5 and len(gh) >= 5:
        sm_l, sp_l, si_l = scatters(gl, tag); sm_h, sp_h, si_h = scatters(gh, tag)
        lo95, hi95, med, pgt = ratio_ci(gl, gh, tag, use_int=False)
        OUT[f"v5_{tag}"] = dict(n_lo=len(gl), n_hi=len(gh), sm_lo=sm_l, sm_hi=sm_h, sp_lo=sp_l, sp_hi=sp_h,
                                ratio_meas=sm_l/sm_h, ci=[lo95, hi95], p_gt_min=pgt)
        print(f"    [{tag:9s}] measured {sm_l:.4f} vs {sm_h:.4f} dex (budgets {sp_l:.4f} / {sp_h:.4f}) -> "
              f"ratio {sm_l/sm_h:.3f}, 95% [{lo95:.3f}, {hi95:.3f}], P(> {SELECTION_RATIO_MIN}) = {pgt:.3f}")
    else:
        OUT[f"v5_{tag}"] = dict(n_lo=len(gl), n_hi=len(gh), ratio_meas=float("nan"), ci=[float("nan")]*2,
                                p_gt_min=float("nan"))
        print(f"    [{tag:9s}] the gold cut leaves {len(gl)}/{len(gh)} galaxies -- too few to split")
gr = OUT["v5_canonical"]["ratio_meas"]; gci = OUT["v5_canonical"]["ci"]
check("V5 [THE EXCESS SURVIVES RESTRICTING TO WELL-MEASURED GALAXIES] the split is repeated on galaxies with "
      "the highest SPARC quality flag, small velocity errors and a direct (non-Hubble-flow) distance, where "
      "the observational explanation for raised scatter is at its weakest",
      np.isfinite(gci[0]) and gci[0] > SELECTION_RATIO_MIN,
      f"gold ratio {gr:.3f}, 95% [{gci[0]:.3f}, {gci[1]:.3f}] on {OUT['v5_canonical']['n_lo']} + "
      f"{OUT['v5_canonical']['n_hi']} galaxies (canonical); alt {OUT['v5_alt']['ratio_meas']:.3f} "
      f"[{OUT['v5_alt']['ci'][0]:.3f}, {OUT['v5_alt']['ci'][1]:.3f}]")

# ------------------------------------------------------------------ V6: the confound-reversing axis
print("\nV6 -- CONTROL (c): the confound-reversing axis -- gas fraction")
print("     the attractor reading says gas-dominated discs are LESS evolved -> MORE scatter")
print("     the observational reading says gas-dominated discs need NO mass-to-light ratio -> LESS scatter")
WG = [g for g in GAL if np.isfinite(g["fgas"])]
grich = [g for g in WG if g["fgas"] > GAS_RICH_FRAC]; gpoor = [g for g in WG if g["fgas"] <= GAS_RICH_FRAC]
print(f"    gas-dominated (M_gas/M_bar > {GAS_RICH_FRAC}): {len(grich)} galaxies; star-dominated: "
      f"{len(gpoor)}")
for tag in A0:
    sm_r, sp_r, si_r = scatters(grich, tag); sm_p, sp_p, si_p = scatters(gpoor, tag)
    lo95, hi95, med, pgt = ratio_ci(grich, gpoor, tag, use_int=False)
    b_r = float(np.sqrt(np.mean([g[f"budget_{tag}"]["ML"]**2 for g in grich])))
    b_p = float(np.sqrt(np.mean([g[f"budget_{tag}"]["ML"]**2 for g in gpoor])))
    OUT[f"v6_{tag}"] = dict(n_rich=len(grich), n_poor=len(gpoor), sm_rich=sm_r, sm_poor=sm_p,
                            ml_rich=b_r, ml_poor=b_p, ratio=sm_r/sm_p, ci=[lo95, hi95], p_gt_min=pgt)
    print(f"    [{tag:9s}] gas-dominated scatter {sm_r:.4f} dex (M/L budget {b_r:.4f}) vs star-dominated "
          f"{sm_p:.4f} dex (M/L budget {b_p:.4f})")
    print(f"                ratio {sm_r/sm_p:.3f}, 95% [{lo95:.3f}, {hi95:.3f}], "
          f"P(> {SELECTION_RATIO_MIN}) = {pgt:.3f}")
v6 = OUT["v6_canonical"]
check("V6 [THE CONFOUND-REVERSING AXIS SEPARATES THE TWO EXPLANATIONS] gas-dominated galaxies have the "
      "SMALLEST mass-to-light error and, on the attractor reading, the LEAST relaxed history; the two "
      "explanations therefore predict opposite signs, so a scatter excess here cannot be blamed on the "
      f"mass-to-light ratio and is compared with the attractor minimum {SELECTION_RATIO_MIN}",
      v6["ci"][0] > SELECTION_RATIO_MIN,
      f"gas-dominated/star-dominated scatter ratio {v6['ratio']:.3f}, 95% [{v6['ci'][0]:.3f}, "
      f"{v6['ci'][1]:.3f}], with the mass-to-light budget SMALLER in the gas-dominated bin "
      f"({v6['ml_rich']:.4f} vs {v6['ml_poor']:.4f} dex). Whatever sign this carries, it is not a "
      "mass-to-light artefact")

# ------------------------------------------------------------------ V7: monotone trend, and the within-galaxy version
print("\nV7 -- is the dependence a TREND in the relaxation variable, as an attractor requires, or a step?")
for tag in A0:
    x = np.array([math.log10(g["norb_out"]) for g in GAL])
    y = np.array([abs(g[f"dbar_{tag}"]) for g in GAL])
    rk = lambda v: np.argsort(np.argsort(v)).astype(float)
    rx, ry = rk(x), rk(y)
    rho = float(np.corrcoef(rx, ry)[0, 1]); nn = len(x)
    z = abs(rho)*math.sqrt(nn - 1)
    # four equal-count bins in the relaxation variable
    q = np.quantile(x, [0.25, 0.5, 0.75])
    bins = [[g for g, xv in zip(GAL, x) if lo_ <= xv < hi_]
            for lo_, hi_ in zip([-1e9, q[0], q[1], q[2]], [q[0], q[1], q[2], 1e9])]
    sig = [scatters(b, tag)[0] for b in bins]
    bud = [scatters(b, tag)[1] for b in bins]
    OUT[f"v7_{tag}"] = dict(spearman=rho, z=z, quartile_scatter=sig, quartile_budget=bud,
                            quartile_norb=[float(10**np.median([math.log10(g['norb_out']) for g in b]))
                                           for b in bins])
    print(f"    [{tag:9s}] Spearman(|mean residual|, log N_orb) = {rho:+.4f} over {nn} galaxies "
          f"({z:.2f} sigma)")
    print(f"                quartiles by N_orb (median {', '.join(f'{v:.0f}' for v in OUT[f'v7_{tag}']['quartile_norb'])} "
          f"orbits): scatter {', '.join(f'{v:.4f}' for v in sig)} dex")
    print(f"                                                        budget  "
          f"{', '.join(f'{v:.4f}' for v in bud)} dex")
mono = OUT["v7_canonical"]["quartile_scatter"]
is_mono = all(mono[i] >= mono[i+1] for i in range(3))
check("V7 [THE SCATTER FALLS MONOTONICALLY WITH THE NUMBER OF COMPLETED ORBITS] an attractor approached over "
      "a relaxation time requires the residual scatter to decrease monotonically across quartiles of the "
      "relaxation variable, not merely to differ between two bins; monotonicity across all four quartiles is "
      "the threshold",
      is_mono,
      f"quartile scatter {', '.join(f'{v:.4f}' for v in mono)} dex from least to most relaxed "
      f"(canonical); alt {', '.join(f'{v:.4f}' for v in OUT['v7_alt']['quartile_scatter'])}. Spearman "
      f"{OUT['v7_canonical']['spearman']:+.3f} ({OUT['v7_canonical']['z']:.1f} sigma). The predicted "
      f"observational budget across the same quartiles is "
      f"{', '.join(f'{v:.4f}' for v in OUT['v7_canonical']['quartile_budget'])} dex -- compare shapes, not "
      "just amplitudes")

print("\nV7b -- the within-galaxy version: distance and mass-to-light errors are COHERENT across a galaxy,")
print("       so subtracting each galaxy's own mean removes them exactly, leaving a radial relaxation test")
for tag in A0:
    e_lo, e_hi, v_lo, v_hi = [], [], [], []
    for g in GAL:
        eps = g[f"eps_{tag}"] - g[f"dbar_{tag}"]
        sv = 2*g["eV"]/g["Vo"]/math.log(10)
        m = g["norb_pt"] < SPLIT_NORB
        e_lo += list(eps[m]); v_lo += list(sv[m]); e_hi += list(eps[~m]); v_hi += list(sv[~m])
    e_lo, e_hi, v_lo, v_hi = map(np.array, (e_lo, e_hi, v_lo, v_hi))
    if len(e_lo) >= 30 and len(e_hi) >= 30:
        sl, sh = float(np.std(e_lo)), float(np.std(e_hi))
        il = math.sqrt(max(sl**2 - float(np.mean(v_lo**2)), 0.0)); ih = math.sqrt(max(sh**2 - float(np.mean(v_hi**2)), 0.0))
        OUT[f"v7b_{tag}"] = dict(n_lo=len(e_lo), n_hi=len(e_hi), s_lo=sl, s_hi=sh, i_lo=il, i_hi=ih,
                                 ratio=(il/ih if ih > 0 else float("nan")))
        print(f"    [{tag:9s}] {len(e_lo)} points inside galaxies at N_orb(r) < {SPLIT_NORB:.0f}: scatter "
              f"{sl:.4f} dex (velocity-error corrected {il:.4f})")
        print(f"                {len(e_hi)} points at N_orb(r) >= {SPLIT_NORB:.0f}: scatter {sh:.4f} dex "
              f"(corrected {ih:.4f}) -> ratio {il/ih if ih>0 else float('nan'):.3f}")
    else:
        OUT[f"v7b_{tag}"] = dict(n_lo=len(e_lo), n_hi=len(e_hi), ratio=float("nan"))
        print(f"    [{tag:9s}] only {len(e_lo)}/{len(e_hi)} points -- the radial split has no power")
r7b = OUT["v7b_canonical"]["ratio"]
check("V7b [THE RADIAL VERSION AGREES WITH THE GALAXY-LEVEL VERSION] each galaxy's own mean residual is "
      "removed, which cancels its distance, inclination and mass-to-light errors exactly, and the remaining "
      "point scatter is split by the number of orbits completed AT EACH RADIUS; the attractor reading "
      f"requires the same excess here, at least {SELECTION_RATIO_MIN}",
      np.isfinite(r7b) and r7b > SELECTION_RATIO_MIN,
      f"velocity-error-corrected radial ratio {r7b:.3f} (canonical) / {OUT['v7b_alt']['ratio']:.3f} (alt) on "
      f"{OUT['v7b_canonical']['n_lo']} + {OUT['v7b_canonical']['n_hi']} points. This test carries its own "
      "confounds -- warps, non-circular motions and mass-to-light gradients all live at large radius -- so a "
      "positive here is weaker evidence than V6, and a null here is strong evidence against")

# ------------------------------------------------------------------ V8: the reach of the sample, and the coincidence
print("\nV8 -- the reach of this sample, and the epoch coincidence stated as a coincidence")
H0 = 67.4*1000/3.0857e22
rho_crit = 3*H0**2/(8*math.pi*G)
rho_lam = 0.685*rho_crit
t_lam = 1.0/math.sqrt(G*rho_lam)
print(f"    the dark-energy timescale 1/sqrt(G rho_Lambda) = {t_lam/GYR:.1f} Gyr, against the assumed disc "
      f"age {T_AGE_GYR:.0f} Gyr: ratio {t_lam/GYR/T_AGE_GYR:.2f}")
print(f"    kappa c sqrt(G rho_Lambda) with kappa = 1/2 is {0.5*C_LIGHT*math.sqrt(G*rho_lam):.4e} m/s^2, "
      f"the canonical footing -- a COINCIDENCE of scales, not a derivation, and nothing below uses it")
for tag, a0 in A0.items():
    v = 100*KMS                                                      # a representative flat rotation speed
    g_one = a0*(2*math.pi*v/(a0*T_AGE_GYR*GYR))                      # g where exactly one orbit fits in T_AGE
    # N_orb = T_AGE*v/(2 pi r) = 1  ->  r = T_AGE*v/(2 pi); g = v^2/r = 2 pi v/(T_AGE)
    g_one = 2*math.pi*v/(T_AGE_GYR*GYR)
    gmin = min(float(g["gbar"].min()) for g in GAL)
    gmin_obs = min(float(g["gobs"].min()) for g in GAL)
    OUT[f"v8_g_one_orbit_{tag}"] = g_one; OUT[f"v8_g_one_over_a0_{tag}"] = g_one/a0
    OUT["v8_gbar_min"] = gmin; OUT["v8_gobs_min"] = gmin_obs
    print(f"    [{tag:9s}] a galaxy with v_flat = 100 km/s completes exactly ONE orbit in {T_AGE_GYR:.0f} Gyr "
          f"at g = {g_one:.3e} m/s^2 = {g_one/a0:.4f} a_0")
    print(f"                the lowest acceleration SPARC reaches is g_bar = {gmin:.3e} "
          f"({gmin/a0:.4f} a_0), g_obs = {gmin_obs:.3e} ({gmin_obs/a0:.4f} a_0)")
gap = OUT["v8_gobs_min"]/OUT["v8_g_one_orbit_canonical"]
OUT["v8_reach_factor"] = float(gap)
check("V8 [SPARC DOES NOT REACH THE REGIME WHERE THE TWO READINGS DIFFER MOST] the acceleration at which a "
      "disc completes only one orbit in the assumed age is computed and compared with the lowest acceleration "
      "SPARC measures; the test is fully powered only if the data reach down to that acceleration, i.e. if "
      "the ratio is at or below 1",
      gap <= 1.0,
      f"one orbit per {T_AGE_GYR:.0f} Gyr sits at {OUT['v8_g_one_orbit_canonical']:.2e} m/s^2 = "
      f"{OUT['v8_g_one_over_a0_canonical']:.3f} a_0, while the lowest acceleration in the sample is "
      f"{OUT['v8_gobs_min']:.2e} m/s^2 -- a factor {gap:.0f} ABOVE it. Every SPARC galaxy has completed "
      f"at least {OUT['norb_min']:.0f} orbits at its last measured point. This is the honest ceiling on the "
      "lane: SPARC can only probe the TAIL of any relaxation dependence, never its onset, so a null here "
      "bounds an attractor's relaxation time rather than excluding an attractor")

# ------------------------------------------------------------------ V9: the verdict, stated against this programme
print("\nV9 -- the verdict, and which reading it favours")
dec = OUT["v4_canonical"]["ci"]; dec_a = OUT["v4_alt"]["ci"]
def verdict(ci):
    if ci[0] > SELECTION_RATIO_MIN: return "SELECTION/ATTRACTOR"
    if ci[1] < SELECTION_RATIO_MIN and ci[0] < FORCE_RATIO < ci[1]: return "FORCE LAW"
    if ci[1] < SELECTION_RATIO_MIN: return "attractor prediction EXCLUDED at its own minimum"
    return "UNDECIDED"
vc, va = verdict(dec), verdict(dec_a)
OUT["verdict_canonical"] = vc; OUT["verdict_alt"] = va
print(f"    error-corrected ratio 95% interval: canonical [{dec[0]:.3f}, {dec[1]:.3f}] -> {vc}")
print(f"                                        alt       [{dec_a[0]:.3f}, {dec_a[1]:.3f}] -> {va}")
print(f"    confound-reversing gas axis:        canonical [{v6['ci'][0]:.3f}, {v6['ci'][1]:.3f}]")
print(f"    gold cut:                           canonical [{gci[0]:.3f}, {gci[1]:.3f}]")
print("    NOTE ON DIRECTION: a SELECTION verdict would be an argument for standard gravity plus cold")
print("    collisionless dark matter with an assembly attractor, and AGAINST this programme's own")
print("    modified-force reading. A FORCE-LAW verdict is the one that leaves this programme's reading")
print("    standing, and is therefore the one this lane had every incentive to manufacture.")
check("V9 [THE TWO FOOTINGS AGREE ON THE VERDICT] the pre-registered decision rule is applied independently "
      "on the canonical and the alternative a_0 footing; a lane whose conclusion depends on which footing is "
      "used has not measured anything",
      vc == va,
      f"canonical -> {vc}; alt -> {va}. The decision rule was fixed in the docstring before any split was "
      "computed and is not adjusted here")

json.dump(OUT, open(os.path.join(HERE, "L256_results.json"), "w"), indent=1, default=float)
print(f"\nL256 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
sys.exit(0 if all(CH) else 1)
