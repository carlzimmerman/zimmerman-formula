#!/usr/bin/env python3
"""
prereg_freeze.py -- BUILD AND FREEZE THE PRE-REGISTRATION for the a0-line ESTIMATOR-BIAS
mock study (Step-A estimator ambiguity: GLS 1.181e-10 vs robust median 9.726e-11).
=========================================================================================
This script is the PREREGISTER phase. It runs BEFORE any mock is generated and BEFORE any
estimator other than the two already-committed ones is evaluated on anything.

WHAT IT DOES (and nothing else):
  1. Rebuilds the EXACT gas-dominated SPARC subsample from the committed pipeline
     (fire_common.load(Ud=0.70) -> gasdom point mask) and asserts the committed counts
     (N = 310 points, N_gal = 49). This manifest IS the mock's fixed truth-structure.
  2. Writes the FROZEN CONFIG prereg_estimator_bias_config.json: every fiducial, the
     forward model, the 9 estimator definitions, the 3 injected a0 values, the seed, the
     realization count, the zero-noise null tolerance, and the NUMERIC decision rule.
  3. Computes SHA-256 of the two frozen artifacts (the .md and the .json) and writes
     PREREG_ESTIMATOR_BIAS.sha256 so an adversary can verify nothing changed afterwards.

IT DOES NOT compute any a0 estimate, run any estimator, or generate any mock. It is
deliberately incapable of producing a result that could bias the frozen criterion.

HONESTY RAILS: the two real-data numbers (GLS 1.181e-10, median 9.726e-11) are already
PUBLIC in the committed Step-A artifacts and cannot be un-known; the decision rule is
therefore written to depend ONLY on |bias| magnitudes measured at THREE injected values
(canonical, ALT, standard-MOND), never on the sign or direction of a bias and never on
which footing an estimator's real-data value favours. See PREREG_ESTIMATOR_BIAS.md S7.
Exit 0 = manifest rebuilt + config frozen + hashes written. Exit code is not a verdict.
"""
import numpy as np, os, json, hashlib, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fire_common as fc

HERE = fc.HERE
bar = "=" * 96
UD = 0.70

# ---------------------------------------------------------------- 1. sample manifest
print(bar); print("1 -- REBUILD THE GAS-DOMINATED TRUTH-STRUCTURE MANIFEST (real SPARC)"); print(bar)
gals = fc.load(UD)
GB, GO, FV, PHI, GAL, SLD, CTI = fc.flat(gals, True)
N, NGAL = int(len(GB)), len(set(GAL.tolist()))
assert N == 310, f"point count drifted from the committed Step-A sample: {N}"
assert NGAL == 49, f"galaxy count drifted from the committed Step-A sample: {NGAL}"
print(f"  N points = {N}, N_gal = {NGAL}  [matches committed per_galaxy_budget.py P0]")

manifest = []
for g in gals:
    m = g["gasdom"]
    if int(m.sum()) == 0:
        continue
    manifest.append(dict(
        name=g["name"], fD=int(g["fD"]), sig_lnD=float(g["sig_lnD"]),
        inc_deg=float(np.degrees(g["inc"])), npt=int(m.sum()),
        # the FIXED per-point truth structure: g_bar (distance-independent, exact),
        # stellar share phi, and the measured fractional velocity error fv = eV/Vobs.
        g_bar_true=[float(v) for v in g["gb"][m]],
        phi=[float(v) for v in g["phi"][m]],
        fv=[float(v) for v in g["fv"][m]]))
assert len(manifest) == NGAL
assert sum(r["npt"] for r in manifest) == N
sld_census = {str(v): int((SLD == v).sum()) for v in sorted(set(SLD.tolist()))}
fd_census = {}
for r in manifest:
    fd_census[str(r["fD"])] = fd_census.get(str(r["fD"]), 0) + 1
print(f"  distance-method census (galaxies): {fd_census}   sigma_lnD census (points): {sld_census}")
print(f"  y = g_bar/1e-10 range [{(GB/1e-10).min():.5f}, {(GB/1e-10).max():.5f}], "
      f"median {np.median(GB/1e-10):.4f}   (the subsample is DEEP-MOND throughout)")
print(f"  phi (stellar share) median {np.median(PHI):.3f} max {PHI.max():.3f}; "
      f"fv median {np.median(FV):.4f} max {FV.max():.4f}")
print(f"  inclination range {min(r['inc_deg'] for r in manifest):.1f}-"
      f"{max(r['inc_deg'] for r in manifest):.1f} deg; points/galaxy "
      f"{min(r['npt'] for r in manifest)}-{max(r['npt'] for r in manifest)}")

# ---------------------------------------------------------------- 2. frozen config
print(); print(bar); print("2 -- WRITE THE FROZEN CONFIG"); print(bar)

A0_INJ = [float(fc.A0C), float(fc.A0A), 1.2e-10]          # canonical / ALT / standard-MOND
CFG = dict(
    prereg_id="a0_line_estimator_bias_v1",
    frozen_utc_date="2026-07-25",
    purpose=("Measure the BIAS and SCATTER of candidate a0-line slope estimators on mocks "
             "with a KNOWN injected a0, to decide whether the committed 22% GLS-vs-median "
             "estimator spread is an estimator artifact or real data structure. This is a "
             "MEASUREMENT-statistics study only: a0's VALUE remains POSITED in the "
             "framework either way, and no mock can test the framework's nu."),

    # ---- sample (fixed truth structure; NOT re-drawn) --------------------------------
    sample=dict(
        source="fire_common.load(Ud=0.70) -> per-galaxy 'gasdom' point mask",
        sparc_cuts="Q<=2, inc>=30 deg, point cut eV/Vobs < 0.10 (Lelli+2017 standard)",
        gas_cut="POINT level: Vgas^2 > Ud*Vdisk^2 + Ub*Vbul^2, Ud=0.70, Ub=1.4*Ud",
        N_points=N, N_gal=NGAL,
        fD_census_galaxies=fd_census, sig_lnD_census_points=sld_census,
        y_min_at_1e10=float((GB / 1e-10).min()), y_max_at_1e10=float((GB / 1e-10).max()),
        y_median_at_1e10=float(np.median(GB / 1e-10)),
        galaxies=[r["name"] for r in manifest],
        manifest=manifest),

    # ---- injection ------------------------------------------------------------------
    injection=dict(
        identity="g_obs_true = sqrt(g_bar_true^2 + a0_inj*g_bar_true)  (EXACT, no approximation)",
        a0_injected=A0_INJ,
        a0_injected_labels=["canonical cH_Lambda/Z", "ALT cH0/Z", "standard-MOND g_dagger"],
        note=("All three are injected so NEITHER footing is privileged. An estimator that is "
              "unbiased must be unbiased at ALL THREE.")),

    # ---- forward error model (every magnitude stated; all lifted from fire_common) ----
    forward_model=dict(
        order=["draw global dlnU, dlnG (once per realization)",
               "draw per-galaxy dlnD_k, di_k",
               "draw per-point eps_shape_i, dv_i",
               "form g_bar_obs and g_obs_obs",
               "hand (g_bar_obs, g_obs_obs, fv, gal_id) to every estimator"],
        g_bar_obs=("g_bar_obs_i = g_bar_true_i * (phi_i*exp(dlnU) + (1-phi_i)*exp(dlnG)) "
                   "* exp(eps_shape_i)"),
        g_obs_obs=("g_obs_obs_i = g_obs_true_i * exp(-dlnD_k) "
                   "* (sin(inc_k)/sin(inc_k+di_k))^2 * (1+dv_i)^2"),
        rationale=("g_bar is EXACTLY distance-independent for gas AND stars (estimator_theory.py "
                   "S2, sympy-verified); distance enters only through g_obs ~ 1/D. "
                   "d ln g_obs = -dlnD - 2 dln sin i + 2 dv/v, matching the committed S3 "
                   "sensitivities d a0_pt/dlnD = -2a0(y+1), d/dln sin i = -4a0(y+1), "
                   "d/(dv/v) = +4a0(y+1)."),
        deep_mond_amplification=("NOT an added ingredient: the ~4(y+1) lever on a0_pt is a "
                                 "DERIVED consequence of the forward model above and MUST be "
                                 "verified numerically (validation V2/V3), never injected by "
                                 "hand -- injecting it separately would double-count."),
        terms=dict(
            Upsilon_offset=dict(symbol="dlnU", dist="Normal(0, 0.23)", scope="GLOBAL, one draw per realization",
                                source="fire_common.SIG_LNU = 0.23 = 0.10 dex stellar M/L"),
            gascal_offset=dict(symbol="dlnG", dist="Normal(0, 0.10)", scope="GLOBAL, one draw per realization",
                               source="fire_common.SIG_LNG = 0.10 gas-mass calibration"),
            gbar_shape=dict(symbol="eps_shape", dist="Normal(0, 0.10)", scope="PER POINT, independent",
                            source="fire_common.SLNB = 0.10 per-point g_bar shape scatter"),
            distance=dict(symbol="dlnD", dist="Normal(0, sigma_lnD[fD])", scope="PER GALAXY, independent",
                          sigma_lnD={"1 Hubble-flow": 0.25, "2 TRGB": 0.05, "3 Cepheid": 0.05,
                                     "4 UMa": 0.10, "5 SNIa": 0.08},
                          source="fire_common.SIG_LND"),
            inclination=dict(symbol="di", dist="Normal(0, 3 deg)", scope="PER GALAXY, independent",
                             source="fire_common.SIG_INC = 3 deg",
                             guard="redraw if inc_k+di_k outside (5 deg, 90 deg]"),
            velocity=dict(symbol="dv", dist="Normal(0, fv_i)", scope="PER POINT, independent",
                          note="fv_i = eV_i/Vobs_i taken from the REAL data, per point",
                          guard="redraw if (1+dv_i) <= 0.05 (never triggers at fv<0.10; logged if it does)")),
        no_clipping=("E_i = g_obs_obs^2 - g_bar_obs^2 and a0_pt_i = E_i/g_bar_obs_i are used AS IS. "
                     "Negative E or negative a0_pt are NOT clipped, dropped, or floored -- doing so "
                     "would itself bias the estimators under test."),
        no_reselection=("The gas-dominated point set is FIXED by the real data and is NOT re-cut on "
                        "the mock observables: re-applying the gas cut to noisy mocks would inject a "
                        "selection effect absent from the real pipeline.")),

    # ---- estimators under test ------------------------------------------------------
    estimators=[
        dict(id="gls_origin", incumbent=True,
             defn="fire_common.gls(GB,GO,FV): iterated through-origin GLS with MODEL-based "
                  "weights, a0_hat = sum(w E g)/sum(w g^2), w = 1/sig2_model, f_int iterated to chi2/N=1"),
        dict(id="median_a0pt", incumbent=True,
             defn="median over points of a0_pt_i = (g_obs^2-g_bar^2)/g_bar"),
        dict(id="theilsen_pairwise", incumbent=False,
             defn="Theil-Sen with FREE intercept: median over all point pairs (i<j) with "
                  "g_j != g_i of (E_j-E_i)/(g_j-g_i); all 47,895 pairs used exactly (no "
                  "subsampling at N=310). Intercept median(E - slope*g) reported as a diagnostic only. "
                  "NOTE: the ORIGIN-anchored Theil-Sen is algebraically identical to median_a0pt, "
                  "so the free-intercept form is the only non-degenerate Theil-Sen variant."),
        dict(id="trimmed_mean_a0pt", incumbent=False,
             defn="symmetric 20%-trimmed mean of a0_pt (drop the lowest 20% and highest 20%)"),
        dict(id="ivw_median_a0pt", incumbent=False,
             defn="weighted median of a0_pt with w_i = g_bar_i^2 / sig2_model_i, i.e. the SAME "
                  "error model as the GLS (weights evaluated at the gls_origin-converged a0 and "
                  "f_int: a two-stage estimator). Directly probes the 'GLS upweights high-g_bar' "
                  "hypothesis while staying robust."),
        dict(id="galaxy_median_then_median", incumbent=False,
             defn="per-galaxy median of a0_pt, then the unweighted median over the 49 galaxy values"),
        dict(id="galaxy_gls_then_median", incumbent=False,
             defn="per-galaxy through-origin GLS a0_hat_k (same weights/iteration as gls_origin, "
                  "run within galaxy k), then the unweighted median over the 49 values"),
        dict(id="log_median_a0pt", incumbent=False,
             defn="exp(median(ln a0_pt)) over points with a0_pt>0; the count of discarded "
                  "non-positive points is REPORTED per realization (this estimator is the one "
                  "candidate that cannot use them, which is itself a defect to be reported)"),
        dict(id="gls_lowy", incumbent=False,
             defn="gls_origin restricted to points with g_bar < 1.0e-10 (y<1 at the footing-neutral "
                  "reference scale 1.0e-10, fixed in advance, NOT tuned; it lies between the "
                  "canonical and ALT candidates). Diagnostic estimator for the "
                  "catastrophic-cancellation / high-g_bar-leverage hypothesis.")],

    # ---- realizations, seeds, reproducibility ---------------------------------------
    monte_carlo=dict(
        N_real=2000, N_real_minimum_allowed=1000,
        seed=20260725,
        stream="numpy.random.default_rng(SeedSequence(20260725).spawn(N_real)[r]) per realization",
        common_random_numbers=("ALL estimators see the SAME realizations, and the SAME noise draws "
                              "are reused across the three injected a0 values (paired design), so "
                              "estimator-to-estimator and injection-to-injection differences are "
                              "not Monte-Carlo noise."),
        required_mc_precision=("sigma_MC on the median ratio, ~1.2533*s/sqrt(N_real), must be "
                              "< 0.50 percentage points; it must be computed and reported. If "
                              "N_real is reduced below 2000 for wall-clock reasons the reduction "
                              "and the achieved sigma_MC must be recorded, and sigma_MC must "
                              "remain < 0.70 pp."),
        vectorization_clause=("A vectorized reimplementation of fire_common.gls is permitted ONLY "
                             "if it is asserted to agree with fire_common.gls to <1e-12 relative "
                             "on (a) the real gas-dominated sample and (b) 20 mock realizations. "
                             "The assertion must be in the results script.")),

    # ---- validation gates that must pass BEFORE any bias number is believed ---------
    validation=dict(
        V1_zero_noise_null=dict(
            spec="With dlnU=dlnG=eps_shape=dlnD=di=dv=0, EVERY estimator must return a0_inj at "
                 "ALL THREE injected values: |a_hat/a0_inj - 1| < 1e-10.",
            n_checks=27,
            tolerance_rel=1e-10,
            justification=("With zero noise E_i = a0_inj*g_bar_i EXACTLY, so every listed estimator "
                          "is algebraically exact independent of its weights; float64 roundoff on "
                          "sums of 310 terms is ~1e-14, so 1e-10 is a generous machine-level bound."),
            on_failure="HARD HALT. The mock or that estimator is broken and must be fixed before "
                       "any noisy realization is run. No bias number from a failed build may be used."),
        V2_linear_response=dict(
            spec="Enabling each noise term ALONE at small amplitude, the measured per-point "
                 "d a0_pt/d(lever) must match the committed sympy coefficients "
                 "(-2a0(y+1) for lnD, -4a0(y+1) for ln sin i, +4a0(y+1) for dv/v, "
                 "-phi*a0(2y+1) for lnUpsilon, -(1-phi)a0(2y+1) for ln gascal) to < 1%.",
            on_failure="HARD HALT: the forward model does not reproduce the committed sensitivities."),
        V3_deep_mond_amplification=dict(
            spec="With velocity noise only, median |Delta a0_pt|/a0 must equal 4(1+y)*fv within 5% "
                 "-- the numerical confirmation that a0 errors go as ~2x the fractional g_obs error, "
                 "NOT half of it.",
            on_failure="HARD HALT (same reason as V2).")),

    # ---- THE FROZEN DECISION RULE (numeric, written before any result exists) --------
    decision_rule=dict(
        bias_metric="b(est, a0_inj) = median over realizations of (a_hat / a0_inj) - 1, in percent",
        scatter_metric=("s(est, a0_inj) = 0.5*(P84 - P16) of a_hat/a0_inj, in percent; "
                        "s(est) = arithmetic mean of s over the three injections"),
        G1_null="V1 zero-noise null must PASS (hard prerequisite for every estimator).",
        G2_bias_gate="PASS iff |b(est, a0_inj)| < 2.0 percentage points at ALL THREE injected values.",
        G3_injection_independence=("PASS iff max_inj b(est) - min_inj b(est) < 2.0 percentage points. "
                                   "An estimator unbiased at only one injected value is DISQUALIFIED "
                                   "from primary status and must be reported as a red flag."),
        G4_efficiency=("Among estimators passing G1+G2+G3, PASS iff s(est) <= 1.30 * "
                       "min(s) over that surviving set."),
        tiers=dict(PASS="max_inj |b| < 2.0 pp", MARGINAL="2.0 pp <= max_inj |b| < 5.0 pp",
                   FAIL="max_inj |b| >= 5.0 pp"),
        primary_selection=("Among G1+G2+G3+G4 survivors: smallest RMS bias over the three "
                           "injections. If two are within 0.25 pp RMS, the smaller s(est) wins. "
                           "If still within 2% relative in s, the FROZEN PRIORITY ORDER below "
                           "decides."),
        frozen_priority_order=["gls_origin", "median_a0pt", "theilsen_pairwise",
                               "trimmed_mean_a0pt", "ivw_median_a0pt",
                               "galaxy_median_then_median", "galaxy_gls_then_median",
                               "log_median_a0pt", "gls_lowy"],
        priority_order_provenance=("Provenance-based, fixed now: the two INCUMBENT estimators "
                                   "already committed in fire_common.py first (in the order they "
                                   "appear there), then the new candidates in the order the task "
                                   "brief enumerated them. Note that this order puts the "
                                   "ALT-side incumbent (gls_origin) FIRST -- the tie-break "
                                   "cannot be a canonical-favouring choice."),
        residual_estimator_systematic=("On the real data, sysEst_new := (max - min)/2 over ALL "
                                       "G1+G2+G3 survivors (conservative: the wider set, not just "
                                       "the G4 set)."),
        outcome_map=dict(
            a_one_passes=("Exactly one estimator survives G2+G3 -> the estimator-choice variance "
                          "term collapses to its bias bound; recompute the box and STATE which "
                          "footing the surviving estimator's real-data value implies -- ONLY after "
                          "the verdict file is written and hashed."),
            b_multiple_pass=("Several survive G2+G3. If sysEst_new/a0 > 5% the 22% spread is REAL "
                             "DATA STRUCTURE: the ambiguity STANDS and the Step-A NO-GO HOLDS. "
                             "If sysEst_new/a0 <= 2% the ambiguity is resolved to within the bias "
                             "gate. Between 2% and 5%: PARTIAL shrink, report the new box, NO-GO "
                             "status re-evaluated against the 6.31% target."),
            c_none_pass=("All estimators FAIL or are MARGINAL -> report that a third estimator is "
                         "needed. Any new estimator requires an APPENDED amendment "
                         "(PREREG_AMENDMENT_<n>.md, its own hash, a statement of what was already "
                         "known) BEFORE its real-data value is computed."),
            d_all_fail_null="V1 fails -> no verdict at all; fix the machinery and rerun."),
        forbidden=["adding, removing or redefining an estimator after any bias number is seen",
                   "changing X=2.0/5.0 pp, Y=1.30, N_real, the seed, or the injected values",
                   "selecting among survivors using their real-data a0 values or the footing those imply",
                   "using the SIGN or DIRECTION of a measured bias in any gate",
                   "reporting a footing implication before the verdict JSON is written and hashed"]),

    # ---- footing-blindness protocol --------------------------------------------------
    blindness=dict(
        rule=("The bias verdict (per-estimator tier, G2/G3/G4 flags, the primary estimator, and "
              "the eligible set) MUST be written to estimator_bias_verdict.json and hashed BEFORE "
              "any real-data estimator value beyond the two already-committed ones is computed or "
              "reported."),
        acknowledged_leak=("The two incumbent real-data values are already public in the committed "
                           "Step-A artifacts: gls_origin = 1.181e-10 (~ALT footing 1.1305e-10) and "
                           "median_a0pt = 9.726e-11 (~canonical 9.355e-11). They cannot be un-known. "
                           "The leak is neutralized structurally, not by pretending otherwise: every "
                           "gate uses only |bias| MAGNITUDES measured against injected truths, is "
                           "symmetric in the sign of the bias, and is evaluated at all three "
                           "injections including both candidate footings."),
        counterfactual_audit=("The results must print the FULL bias table (9 estimators x 3 "
                              "injections) so an adversary can re-apply the frozen rule independently "
                              "and confirm it would equally have selected an ALT-side estimator had "
                              "the numbers come out the other way."),
        posited_clause=("Whichever estimator wins, a0's VALUE remains POSITED in the framework. This "
                        "study resolves a MEASUREMENT ambiguity, not the theory's free coefficient. "
                        "No 'theory closed', no TOE claim, both footings carried on every number.")),

    provenance=dict(
        committed_step_A=["estimator_theory.py", "identity_uniqueness.py",
                          "per_galaxy_budget.py", "reach_target.py", "fire_common.py"],
        step_A_findings=dict(box_frac=0.161, N_points=N, N_gal=NGAL,
                             estimator_share_of_variance=0.301,
                             Upsilon_share=0.253, gascal_share=0.206,
                             gls_real=1.181e-10, median_real=9.726e-11,
                             spread=2.089e-11, footing_gap=1.951e-11,
                             target_1sigma_for_3sigma_separation=0.0631),
        anchor_values="/Users/carlzimmerman/new_physics/prep_2026/concordance_ledger/anchor_values.json"),
)

cfg_path = os.path.join(HERE, "prereg_estimator_bias_config.json")
with open(cfg_path, "w") as fh:
    json.dump(CFG, fh, indent=1, sort_keys=True)
    fh.write("\n")
print(f"  wrote {cfg_path}  ({os.path.getsize(cfg_path)} bytes)")
print(f"  injected a0 values: " + ", ".join(f"{v:.6e}" for v in A0_INJ))
print(f"  estimators frozen: {len(CFG['estimators'])}   N_real = {CFG['monte_carlo']['N_real']}"
      f"   seed = {CFG['monte_carlo']['seed']}")
print(f"  decision rule: |bias| < 2.0 pp at all 3 injections (G2), injection-spread < 2.0 pp (G3),")
print(f"                 scatter within 1.30x best (G4); FAIL at >= 5.0 pp.")

# ---------------------------------------------------------------- 3. hashes
print(); print(bar); print("3 -- SHA-256 OF THE FROZEN ARTIFACTS"); print(bar)
md_path = os.path.join(HERE, "PREREG_ESTIMATOR_BIAS.md")
if not os.path.exists(md_path):
    raise SystemExit("PREREG_ESTIMATOR_BIAS.md missing -- write the prereg document before freezing.")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 16), b""):
            h.update(blk)
    return h.hexdigest()


rows = [(os.path.basename(p), os.path.getsize(p), sha256(p)) for p in (md_path, cfg_path)]
# the freeze script itself is hashed too, so the recipe that generated the config is pinned
rows.append((os.path.basename(__file__), os.path.getsize(os.path.abspath(__file__)),
             sha256(os.path.abspath(__file__))))
hash_path = os.path.join(HERE, "PREREG_ESTIMATOR_BIAS.sha256")
with open(hash_path, "w") as fh:
    fh.write("# FROZEN PRE-REGISTRATION -- a0-line estimator-bias mock study\n")
    fh.write("# prereg_id: a0_line_estimator_bias_v1   frozen 2026-07-25\n")
    fh.write("# verify:  shasum -a 256 PREREG_ESTIMATOR_BIAS.md "
             "prereg_estimator_bias_config.json prereg_freeze.py\n")
    fh.write("# (prereg_freeze.py's own hash is self-referential only in the sense that it is\n")
    fh.write("#  computed AFTER the file is written to disk; re-running the command above\n")
    fh.write("#  reproduces all three digests byte-for-byte.)\n")
    for name, size, dig in rows:
        fh.write(f"{dig}  {name}  ({size} bytes)\n")
for name, size, dig in rows:
    print(f"  {dig}  {name}  ({size} bytes)")
print(f"  wrote {hash_path}")

print()
print(bar)
print("EXIT 0: pre-registration FROZEN. No mock generated, no estimator evaluated, no verdict.")
print(bar)
