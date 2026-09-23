#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L324 -- THE NAKED-BLACK-HOLE ROTATION LAW AT z = 7.04: A2744-QSO1 ON THE FRAMEWORK'S OWN (FLAT-a0) TERMS.

WHY.  The BH* campaign (09-19..09-22) touched the framework only through the density-form a0(rho_gas), a branch the record
already excludes as an environmental law (SPARC +0.5 fork null, 13-34 sigma) and which the framework does not use: its law is
FLAT, a0 = kappa c sqrt(G rho_DE).  With the framework's actual a0, the one BH* object that carries a clean test is the one
door B found: A2744-QSO1 (z = 7.0451), a "naked" black hole -- M_BH/M_* > 2, its mass measured DYNAMICALLY from Keplerian
rotation of narrow H-alpha (Juodzbalis+26, Nature, arXiv:2508.21748).  A point mass with no M/L and no halo in the fit is the
cleanest possible zero-parameter MOND-type rotation law:

    v_c(r)^2 = (G M / r) nu(y),   y = G M /(r^2 a0) = (r_M / r)^2,   r_M = sqrt(G M / a0),   v_flat^4 = G M a0.

For the framework's RAR kernel nu(y) = 1/(1 - exp(-sqrt y)) the PHANTOM FRACTION of the dynamical mass is EXACTLY

    f_ph(r) = 1 - 1/nu = exp(-r_M / r)            (Lean I18 phantom_fraction_rar + sqrt_y_point_mass)

so "any extended component is sub-dominant at radius r" (f_ph < 1/2) is EXACTLY  r ln2 < r_M,  i.e.

    a0(z = 7.04)  <  G M / (r ln 2)^2            (Lean I18 subdominance_iff_a0_bound).

INPUTS (published, cited; none from this repo) -- the PUBLISHED Nature 2026 version (PMC13215880), which supersedes arXiv v1:
  Juodzbalis+26 (Nature, arXiv:2508.21748): MOKA3D point mass log M = 7.7 +/- 0.3 at i = 52 +/- 2 deg (PSF-modelled, the
  headline); spectroastrometric inclination-corrected log M = 6.9-7.2 ("consistent within 2 sigma"); 1-D rotation-curve fit
  log M sin^2 i = 6.75 +/- 0.15 (lower limit); r_spec = 12.5 +/- 4.7 pc with <v sin i> = 51 +/- 4 km/s; rotation bins at 100 and
  150 pc with <v sin i> ~ 10 km/s; narrow H-alpha extended to ~200 pc; NFW / NSC / Plummer extended components all collapse
  to a point: "any extended mass component is sub-dominant at the < 200 pc scales probed"; M_* < 2e7 Msun; outflow 300-450 pc.
  (arXiv v1 read 7.2 +/- 0.15 for the low mass, bins 50/100/150 pc, 61 +/- 6 and 20 +/- 6 km/s: this lane's first commit
  used v1; corrected here.)
  a0 footings: canonical 9.3619e-11, alt 1.1279e-10 m/s^2 (the repo's two footings; alt/canonical = 1.2048).
  Rival branch a0 proportional to H(z): a0(z) = a0_0 E(z), E(7.0451) = 12.7 (Planck 2018 Om = 0.3153).

WHAT IS SCORED:
  K2  the exact phantom-fraction identity (numeric mirror of the Lean theorem).
  K3  the mass is measured where every branch is Newtonian to < 1% (no circularity in using the published M).
  K4  at the headline MOKA3D mass the framework (flat a0, both footings, three kernels) satisfies sub-dominance at 150 and
      200 pc.
  K4d THE DEFICIT, verified as hard as the pass: at the LOW end of the published range (10^6.9) the framework VIOLATES
      sub-dominance at 200 pc on both footings and at 150 pc on the alt footing.  The test bites the framework.
  K5  the a0 ~ H(z) rival: the mass it needs to satisfy sub-dominance, in sigma of each published mass reading.
  K6  the registered zero-parameter prediction at 300-1000 pc (the decisive window): the framework's boost over Keplerian is
      separated from Newton and from the rival across the whole mass band.
NOT SCORED (context): the LCDM NFW halo-mass cap from the same statement (a halo is a free parameter; this test does not
discriminate the framework from LCDM and is not presented as doing so).

HONEST SCOPE: "sub-dominant" is the paper's qualitative wording, and its extended-mass fits used NFW/NSC/Plummer shapes, not
the MOND phantom profile (M_ph(<r) ~ r in deep MOND).  Reading it as f_ph < 1/2 is INTERPRETIVE.  The decisive version is a
refit of the published kinematics with the zero-parameter curve above (one parameter M, like the Keplerian fit).
MUTATE=1 replaces the framework's flat a0 by the rival's a0(z = 7.04): K4 must then FAIL (rc = 1).

Run from the repository root:  python3 real_research/bhstar_audit_2026/L324_qso1_naked_bh_rotation_law.py
"""
import os, sys, json, math

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L324_qso1_naked_bh_rotation_law"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L324", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__)
G, MSUN, PC, MPC = 6.6743e-11, 1.98892e30, 3.0856775814913673e16, 3.0856775814913673e22
h = 0.6736; H0 = 100 * h * 1e3 / MPC; Om, OL = 0.3153, 0.6847
Z_QSO1 = 7.0451
A0_FLAT = {"canonical": 9.3619e-11, "alt": 1.1279e-10}


def Ez(z): return math.sqrt(Om * (1 + z) ** 3 + OL)


E7 = Ez(Z_QSO1)
A0_RIVAL = {k: v * E7 for k, v in A0_FLAT.items()}
A0_FW = A0_RIVAL if MUTATE else A0_FLAT          # MUTATE: hand the framework the rival's a0


# ---------------------------------------------------------------- kernels (nu(y), y = g_N / a0)
def nu_rar(y):
    return 1.0 / (1.0 - math.exp(-math.sqrt(y)))


def nu_simple(y):
    return 0.5 + math.sqrt(0.25 + 1.0 / y)


def nu_expmu(y):
    """the exp kernel mu(x) = 1 - exp(-x): solve x mu(x) = y for x = g/a0, nu = x/y (bisection)."""
    lo, hi = 0.0, max(10.0, 2 * y + 10)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid * (1 - math.exp(-mid)) < y:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi) / y


KERNELS = {"rar": nu_rar, "simple": nu_simple, "exp_mu": nu_expmu}


def r_M(M, a0): return math.sqrt(G * M * MSUN / a0)                     # m
def v_flat(M, a0): return (G * M * MSUN * a0) ** 0.25                   # m/s
def y_of(r_pc, M, a0): return G * M * MSUN / ((r_pc * PC) ** 2 * a0)
def boost(r_pc, M, a0, k="rar"): return math.sqrt(KERNELS[k](y_of(r_pc, M, a0)))   # v_c / v_Kepler
def f_ph(r_pc, M, a0, k="rar"): return 1.0 - 1.0 / KERNELS[k](y_of(r_pc, M, a0))


def logM_needed(a0, r_pc):
    """RAR kernel, exact: sub-dominance at r  <=>  M > a0 (r ln2)^2 / G."""
    return math.log10(a0 * (r_pc * PC * math.log(2)) ** 2 / G / MSUN)


# ---------------------------------------------------------------- published data (Juodzbalis+26, arXiv:2508.21748)
MASS = {"MOKA3D (headline)": (7.7, 0.3), "spectroastrometric, i-corrected (low end)": (6.9, 0.15),
        "spectroastrometric, i-corrected (high end)": (7.2, 0.15)}
R_SPEC, R_SPEC_ERR = 12.5, 4.7
R_BINS = (100.0, 150.0)
R_PROBED = 200.0
M_STAR_MAX = 2e7
OUT["numbers"]["inputs"] = {"mass_readings": MASS, "r_spec_pc": [R_SPEC, R_SPEC_ERR], "rotation_bins_pc": R_BINS,
                            "narrow_Halpha_extent_pc": R_PROBED, "Mstar_max": M_STAR_MAX, "E(z=7.0451)": E7,
                            "a0_framework_used": A0_FW, "a0_rival": A0_RIVAL}

# ================================================================= K1
banner("K1 -- CONTROL: the framework's two scales for QSO1 at the headline mass (both footings)")
M0 = 10 ** 7.7
for fk, a0 in A0_FLAT.items():
    P(f"   {fk:9s}: a0 = {a0:.4e}   r_M = {r_M(M0, a0)/PC:6.1f} pc   v_flat = {v_flat(M0, a0)/1e3:5.2f} km/s   "
      f"(rival a0(z) = {A0_RIVAL[fk]:.3e}: r_M = {r_M(M0, A0_RIVAL[fk])/PC:5.1f} pc, v_flat = {v_flat(M0, A0_RIVAL[fk])/1e3:5.1f} km/s)")
rM_can = r_M(M0, A0_FLAT["canonical"]) / PC
OUT["numbers"]["rM_pc_headline"] = {k: r_M(M0, a) / PC for k, a in A0_FLAT.items()}
OUT["numbers"]["vflat_kms_headline"] = {k: v_flat(M0, a) / 1e3 for k, a in A0_FLAT.items()}
OUT["numbers"]["rival_rM_pc_headline"] = {k: r_M(M0, a) / PC for k, a in A0_RIVAL.items()}
check("K1 r_M(canonical, 10^7.7) in [250, 300] pc and E(7.0451) in [12.5, 13.0]",
      f"r_M = {rM_can:.1f} pc, E = {E7:.3f}", 250 < rM_can < 300 and 12.5 < E7 < 13.0,
      "the framework's Kepler->flat transition sits just outside the probed 200 pc; the rival's sits at ~77 pc, inside it")

# ================================================================= K2
banner("K2 -- THE EXACT PHANTOM-FRACTION IDENTITY (RAR kernel): 1 - 1/nu(y) = exp(-r_M/r)")
err = 0.0
for r in (5, 12.5, 50, 100, 150, 200, 375, 1000, 5000):
    for a0 in list(A0_FLAT.values()) + list(A0_RIVAL.values()):
        lhs = f_ph(r, M0, a0, "rar"); rhs = math.exp(-r_M(M0, a0) / (r * PC))
        err = max(err, abs(lhs - rhs))
check("K2 max |f_ph - exp(-r_M/r)| < 1e-12 over 9 radii x 4 a0 values", f"{err:.2e}", err < 1e-12,
      "Lean I18 certifies it symbolically; the numbers are the mirror")

# ================================================================= K3
banner("K3 -- NO CIRCULARITY: the mass is measured where every branch is Newtonian")
worst_fw, worst_rv = 0.0, 0.0
for lbl, (lm, sl) in MASS.items():
    for lmv in (lm - sl, lm, lm + sl):
        for k in KERNELS:
            for a0 in A0_FW.values():
                worst_fw = max(worst_fw, boost(R_SPEC, 10 ** lmv, a0, k) - 1)
            for a0 in A0_RIVAL.values():
                worst_rv = max(worst_rv, math.log10(KERNELS[k](y_of(R_SPEC, 10 ** lmv, a0))))
check("K3 framework: its inflation of the 12.5 pc mass reading, 2 log10(boost), is < 0.02 dex (vs the +/-0.15-0.3 dex mass "
      "errors) over masses x footings x kernels",
      f"max boost {100*worst_fw:.3f}% = {2*math.log10(1+worst_fw):.4f} dex", 2 * math.log10(1 + worst_fw) < 0.02,
      "the Keplerian/spectroastrometric mass IS the framework's baryonic point mass to far better than its error; "
      "M enters no framework check circularly")
check("K3b rival: its own 12.5 pc mass reading is inflated by nu, at most this many dex (reported, conservative)",
      f"{worst_rv:.3f} dex", worst_rv < 0.1,
      "the rival is NOT Newtonian at 12.5 pc for low masses (up to ~6% in v); its baryonic M would be LOWER than the "
      "published M by <= this, which only strengthens K5 -- ignoring it is conservative for the rival", load_bearing=False)
OUT["numbers"]["K3"] = {"framework_max_boost": worst_fw, "rival_max_mass_inflation_dex": worst_rv}

# ================================================================= K4
banner("K4 -- SUB-DOMINANCE AT 150 / 200 pc FOR EVERY PUBLISHED MASS READING (the pass AND the deficit)")
rows, allpass150 = [], True
for lbl, (lm, sl) in MASS.items():
    M = 10 ** lm
    for fk, a0 in A0_FW.items():
        for r in (150.0, 200.0):
            fs = {k: f_ph(r, M, a0, k) for k in KERNELS}
            rows.append({"mass": lbl, "logM": lm, "footing": fk, "r_pc": r, **{f"fph_{k}": v for k, v in fs.items()},
                         "logM_needed_rar": logM_needed(a0, r)})
            if r == 150.0 and max(fs.values()) >= 0.5:
                allpass150 = False
            P(f"   {lbl:32s} {fk:9s} r = {r:5.0f} pc:  f_ph rar {fs['rar']:.3f}  simple {fs['simple']:.3f}  "
              f"exp_mu {fs['exp_mu']:.3f}   (RAR passes for log M > {logM_needed(a0, r):.2f})")
OUT["numbers"]["framework_subdominance"] = rows
head = [x for x in rows if x["mass"].startswith("MOKA3D")]
check("K4 at the headline MOKA3D mass the framework has f_ph < 1/2 at 150 AND 200 pc, both footings, all three kernels",
      "; ".join(f"{x['footing']} {x['r_pc']:.0f}pc max f_ph={max(x[f'fph_{k}'] for k in KERNELS):.3f}" for x in head),
      all(max(x[f"fph_{k}"] for k in KERNELS) < 0.5 for x in head),
      "the flat-a0 law is consistent with 'extended mass sub-dominant' at the paper's PSF-modelled mass")
low = [x for x in rows if "low end" in x["mass"]]
viol = {(x["footing"], x["r_pc"]): x["fph_rar"] >= 0.5 for x in low}
check("K4d DEFICIT (verified): at the published low mass 10^6.9 the framework VIOLATES sub-dominance (RAR) at 200 pc on BOTH "
      "footings and at 150 pc on the ALT footing",
      "; ".join(f"{k[0]} {k[1]:.0f}pc f_ph_rar={x['fph_rar']:.3f}" for k, x in zip(viol, low)),
      viol[("canonical", 200.0)] and viol[("alt", 200.0)] and viol[("alt", 150.0)] and not viol[("canonical", 150.0)],
      "TWO-SIDED, and it cuts against the framework: the verdict hinges on which published mass is right.  The low "
      "readings come from spectroastrometry the paper itself calls lower limits before inclination correction; the "
      "MOKA3D mass models PSF and inclination.  Not a kill of the framework, not a pass: mass-reading-limited")

# ================================================================= K5
banner("K5 -- THE a0 ~ H(z) RIVAL: the mass it needs, in sigma of each published reading (RAR kernel, exact)")
rival_rows, rival_fails_headline = [], True
for fk, a0 in A0_RIVAL.items():
    for r in (150.0, 200.0):
        need = logM_needed(a0, r)
        for lbl, (lm, sl) in MASS.items():
            nsig = (need - lm) / sl
            rival_rows.append({"footing": fk, "r_pc": r, "mass": lbl, "logM_needed": need, "sigma_above": nsig})
            P(f"   rival {fk:9s} r = {r:5.0f} pc: needs log M > {need:.2f}   vs {lbl:32s} {lm}+/-{sl}: "
              f"{nsig:+.1f} sigma")
        if f_ph(r, 10 ** 7.7, a0, "rar") < 0.5:
            rival_fails_headline = False
OUT["numbers"]["rival_mass_needed"] = rival_rows
check("K5 the rival fails sub-dominance at the headline central mass (10^7.7) at 150 and 200 pc, both footings",
      f"f_ph(150 pc) = {f_ph(150, M0, A0_RIVAL['canonical']):.3f}/{f_ph(150, M0, A0_RIVAL['alt']):.3f}, "
      f"f_ph(200 pc) = {f_ph(200, M0, A0_RIVAL['canonical']):.3f}/{f_ph(200, M0, A0_RIVAL['alt']):.3f}",
      rival_fails_headline,
      "HINT-level against a0 ~ H(z): 0.9-2.0 sigma on the headline mass, >= 5 sigma only on the lower spectroastrometric mass; "
      "the rival is NOT the framework (FLAT is the framework's distinctive branch), so this is a flat-vs-rival discriminator")

# ================================================================= K6
banner("K6 -- THE REGISTERED ZERO-PARAMETER PREDICTION: v_c / v_Kepler at 300-1000 pc (the decisive window)")
logMs = [6.75 + 0.05 * i for i in range(26)]     # 10^6.75 .. 10^8.00: every published reading at 1 sigma
pred = {}
for r in (300.0, 375.0, 450.0, 1000.0):
    fw = [boost(r, 10 ** lm, a0, k) for lm in logMs for a0 in A0_FW.values() for k in KERNELS]
    rv = [boost(r, 10 ** lm, a0, k) for lm in logMs for a0 in A0_RIVAL.values() for k in KERNELS]
    vf = [math.sqrt(G * 10 ** lm * MSUN / (r * PC)) * boost(r, 10 ** lm, a0, "rar") / 1e3
          for lm in logMs for a0 in A0_FW.values()]
    pred[r] = {"framework_boost": [min(fw), max(fw)], "rival_boost": [min(rv), max(rv)], "newton_boost": [1.0, 1.0],
               "framework_vc_kms_rar": [min(vf), max(vf)]}
    P(f"   r = {r:6.0f} pc:  framework v_c/v_K in [{min(fw):.3f}, {max(fw):.3f}]  (v_c {min(vf):.1f}-{max(vf):.1f} km/s)"
      f"   rival [{min(rv):.3f}, {max(rv):.3f}]   Newton 1.000")
OUT["numbers"]["registered_prediction"] = {str(k): v for k, v in pred.items()}
sep_newton = pred[375.0]["framework_boost"][0] - 1.0
gap_rival = pred[375.0]["rival_boost"][0] - pred[375.0]["framework_boost"][1]
fixed = []
for lm in logMs:
    fwm = [boost(375.0, 10 ** lm, a0, k) for a0 in A0_FW.values() for k in KERNELS]
    rvm = [boost(375.0, 10 ** lm, a0, k) for a0 in A0_RIVAL.values() for k in KERNELS]
    fixed.append((lm, min(fwm), max(fwm), min(rvm), min(rvm) / max(fwm)))
worst_fixed = min(x[4] for x in fixed)
OUT["numbers"]["K6_fixed_mass_375pc"] = [dict(zip(("logM", "fw_min", "fw_max", "rival_min", "rival_min_over_fw_max"), x))
                                         for x in fixed]
check("K6 at 375 pc the framework clears Newton by > 15% over 10^6.75-10^8.0, and at any FIXED weighed mass the rival sits "
      ">= 1.3x above the framework",
      f"framework lower edge - 1 = {sep_newton:+.3f}; full-band rival lower edge - framework upper edge = {gap_rival:+.3f} "
      f"(bands overlap if < 0); at any FIXED weighed mass rival_min/framework_max >= {worst_fixed:.2f}",
      sep_newton > 0.15 and worst_fixed > 1.3,
      "over the full published mass range the framework and rival bands OVERLAP (the spread is mass + kernel); once M "
      "is weighed jointly with the rotation curve the rival sits >= the fixed-mass ratio above the framework: a joint "
      "refit with 300-450 pc rotation good to ~10% splits Newton / framework / rival")

# ================================================================= context (not scored): LCDM NFW cap
banner("CONTEXT (not scored) -- LCDM: the NFW halo-mass cap from the same 'sub-dominant at 150 pc' reading")


def rho_crit(z): return 3 * (H0 * Ez(z)) ** 2 / (8 * math.pi * G)
def m_nfw(x): return math.log(1 + x) - x / (1 + x)


cap = {}
for c in (2.0, 3.0, 5.0):
    for lm in (7.2, 7.7):
        lo, hi = 7.0, 13.0
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            Mh = 10 ** mid * MSUN
            R200 = (3 * Mh / (4 * math.pi * 200 * rho_crit(Z_QSO1))) ** (1 / 3)
            Mdm = Mh * m_nfw(150 * PC / (R200 / c)) / m_nfw(c)
            if Mdm / (Mdm + 10 ** lm * MSUN) < 0.5:
                lo = mid
            else:
                hi = mid
        cap[f"c={c:g}, logM_BH={lm}"] = lo
        P(f"   c = {c:3.0f}, log M_BH = {lm}:  NFW sub-dominant at 150 pc for log M_200 < {lo:.2f}")
OUT["numbers"]["lcdm_nfw_cap_logM200"] = cap
P("   (a z = 7 halo hosting M_* <~ 2e7 Msun is typically 1e9.5-1e10.5 Msun: LCDM is NOT discriminated by this test)")

# ================================================================= verdict
lb = [c for c in CH if c[2]]
npass = sum(1 for c in lb if c[1])
banner(f"VERDICT  ({npass}/{len(lb)} load-bearing PASS{'  -- MUTATE RUN' if MUTATE else ''})")
P("""  * NEW (framework's own terms): for a naked BH the framework's rotation law has ZERO free parameters once M is weighed at
    small radius, and under the RAR kernel its phantom fraction is exactly exp(-r_M/r).
  * The published 'extended mass sub-dominant within the probed radii' becomes a DIRECT BOUND ON a0 AT z = 7.04:
    a0 < G M/(r ln2)^2.  The flat framework passes at 150 and 200 pc at the PSF-modelled
    headline mass; at the LOW end of the published range (10^6.9) it FAILS at 200 pc (both footings) -- the verdict is
    mass-reading-limited, two-sided.  The a0 ~ H(z) rival fails at every published mass (0.9-2.0 sigma on the headline 7.7,
    far more on the low readings) -- a HINT, not a kill.
  * LCDM is NOT discriminated (a small halo passes).  NOT a breakthrough: the reading of 'sub-dominant' is interpretive.
  * DECISIVE NEXT STEP: refit the public NIRSpec-IFU kinematics with v_c = sqrt(GM/r)/sqrt(1-exp(-r_M/r)) (one parameter,
    like Kepler) and measure the 300-450 pc narrow-line rotation (outflow-separated): framework v_c/v_K in the K6 band.""")
OUT["verdict"] = {"load_bearing_pass": npass, "load_bearing_total": len(lb)}
suffix = "_MUTATE" if MUTATE else ""
with open(os.path.join(HERE, f"{SLUG}_results{suffix}.json"), "w") as f:
    json.dump(OUT, f, indent=1, default=str)
sys.exit(0 if npass == len(lb) else 1)
