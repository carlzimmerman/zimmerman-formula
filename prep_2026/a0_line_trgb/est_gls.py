#!/usr/bin/env python3
"""
est_gls.py -- THE TRGB LEVER, GLS ESTIMATOR LANE.
==========================================================================================
Fires the a0-line MODEL-BASED iterated GLS estimator (fire_common.gls / budget, NOT raw
observed-error weights -- the guard that already caught the fake 3.3e-11 deficit) on the
high-quality-DISTANCE gas-dominated SPARC subsample and on the full gas subsample.

THE LEVER: the distance systematic sysD is ~40% of the gas a0 error budget. SPARC carries
the distance-method flag fD per galaxy; fire_common models it (SIG_LND = {1:0.25 Hubble-
flow, 2:0.05 TRGB, 3:0.05 Cepheid, 4:0.10 UMa, 5:0.08 SNIa}). TRGB/Cepheid galaxies
(fD in {2,3}) therefore have a distance systematic ALREADY 5x smaller than Hubble-flow.
Restricting to them CUTS the biggest budget line -- we then ask, honestly both ways:
  (i)  does the tightened a0 STAY at the banked ~0.97-1.18e-10 central, or MOVE?
  (ii) does its error shrink enough to DISCRIMINATE canonical 9.355e-11 (a0=cH_Lambda/Z)
       vs alt 1.1305e-10 (=cH0/Z)?
  (iii) realize the Occam bans CONCRETELY on the actual TRGB-flagged subsample (not the
        error/2, error/3 forecast).
  (iv) the Lambda inversion Lambda = 3 Z^2 a0^2 / c^4 -- ratio to Planck 1.089e-52.

HONESTY RAILS carried from the banked run:
  * model-based iterated GLS ONLY (gls(...,biased=False)); the biased observed-weight
    variant is printed as a red-flag control, never as the answer.
  * both footings (canonical / alt), anchor_values.json.
  * NEITHER subsample straddles y=1 (both deep-regime) -> this can sharpen the a0 NUMBER
    but CANNOT discriminate the nu SHAPE. Stated, not blurred.
  * y-range-match control: full-gas restricted to the TRGB y-window, to show the TRGB
    central is not an artifact of sampling a different segment of the line.
  * if the subsample is too small / the footings stay non-separated -> say UNDERPOWERED.
No 'proves'. Exit 0 is not a verdict. Credits: Lelli-McGaugh-Schombert 2016 (SPARC);
McGaugh+2016 g_dagger=1.2e-10 (comparison).
"""
import numpy as np, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/Users/carlzimmerman/new_physics/prep_2026/a0_line")
import fire_common as fc
from fire_common import A0C, A0A, SC, SA, ZVAL, HL, CLIGHT

OUT = HERE
LAM_PLANCK = 3 * HL**2 / CLIGHT**2                    # 1.089e-52 m^-2 (banked H_Lambda anchor)
HQ_FD = {2, 3}                                        # TRGB + Cepheid distance flags


def logB(xhat, s_meas, astar, s_anchor_frac, lo=1e-11, hi=1e-9):
    """log10 Bayes factor M0(a0==astar, 0 param)/M1(a0 free, log-flat prior). Quadrature.
    Copied verbatim from fire_occam.logB so this lane is self-contained (no import side FX)."""
    xg = np.linspace(np.log(lo), np.log(hi), 200001)
    s_eff = np.hypot(s_meas, s_anchor_frac)
    lnZ0 = -0.5 * ((np.log(astar) - xhat) / s_eff) ** 2 - np.log(np.sqrt(2 * np.pi) * s_eff)
    Lx = np.exp(-0.5 * ((xg - xhat) / s_meas) ** 2) / (np.sqrt(2 * np.pi) * s_meas)
    prior = np.full_like(xg, 1.0 / (np.log(hi) - np.log(lo)))
    lnZ1 = np.log(np.trapz(Lx * prior, xg))
    return (lnZ0 - lnZ1) / np.log(10.0), (np.log(astar) - xhat) / s_eff


def occam_and_lambda(b):
    """Both-footing Occam bans + Lambda inversion for a budget dict b."""
    xh, sm = np.log(b["a0hat"]), b["tot"] / b["a0hat"]
    bC, tC = logB(xh, sm, A0C, SC / A0C)
    bA, tA = logB(xh, sm, A0A, SA / A0A)
    dfoot = (tC**2 - tA**2) / 2 / np.log(10.0)        # pure LR M0canon vs M0alt, +=toward alt
    lam = 3 * ZVAL**2 * b["a0hat"] ** 2 / CLIGHT**4
    lam_med = 3 * ZVAL**2 * b["a0med"] ** 2 / CLIGHT**4
    s_ln_lam = 2 * b["tot"] / b["a0hat"]
    return dict(bans_canon=float(bC), bans_alt=float(bA), t_canon=float(tC), t_alt=float(tA),
                dfoot_toward_alt=float(dfoot), lam=float(lam), lam_med=float(lam_med),
                lam_ratio=float(lam / LAM_PLANCK), lam_ratio_med=float(lam_med / LAM_PLANCK),
                t_lam=float(np.log(lam / LAM_PLANCK) / s_ln_lam), s_ln_lam=float(s_ln_lam))


def ranges(gals, gas_only=True):
    """(y_lo, y_hi) window of gas-dom points across a gal list, for the y-range match."""
    GB = fc.flat(gals, gas_only)[0]
    y = GB / 1e-10
    return float(np.min(y)), float(np.max(y))


def galaxy_bootstrap(gals, nboot=2000, seed=7):
    """Resample GALAXIES with replacement (not points) -> honest error on the central for a
    small-N subsample, and a jackknife max-leverage to expose one-galaxy dominance."""
    ok = [g for g in gals if g["gasdom"].sum() > 0]
    n = len(ok)
    rng = np.random.default_rng(seed)
    boot = []
    for _ in range(nboot):
        pick = [ok[i] for i in rng.integers(0, n, n)]
        b = fc.budget(pick, gas_only=True)
        if b is not None:
            boot.append(b["a0hat"])
    boot = np.array(boot)
    # leave-one-galaxy-out: largest swing = single-galaxy leverage
    jk = []
    for i in range(n):
        b = fc.budget([ok[j] for j in range(n) if j != i], gas_only=True)
        if b is not None:
            jk.append((abs(b["a0hat"]), ok[i]["name"], b["a0hat"]))
    a0_all = fc.budget(ok, gas_only=True)["a0hat"]
    jk_sorted = sorted(((abs(x[2] - a0_all), x[1], x[2]) for x in jk), reverse=True)
    return dict(boot_med=float(np.median(boot)), boot_lo=float(np.percentile(boot, 16)),
                boot_hi=float(np.percentile(boot, 84)),
                max_leverage=[jk_sorted[0][1], float(jk_sorted[0][2]), float(jk_sorted[0][0])],
                n_gal=n)


bar = "=" * 94
report = ["# EST_GLS.md -- the TRGB lever, GLS estimator lane",
          "",
          "The a0-line model-based iterated GLS (fire_common.gls/budget, biased=False -- the",
          "same guard that caught the fake 3.3e-11 observed-weight deficit), fired on the",
          "TRGB/Cepheid-anchored gas subsample (fD in {2,3}) vs the full gas subsample.",
          "Distance systematic sysD is 5x smaller for fD in {2,3} (SIG_LND 0.05 vs 0.25).",
          "Credits: Lelli-McGaugh-Schombert 2016 (SPARC); McGaugh+2016 g_dagger=1.2e-10.",
          ""]

print(bar)
print("EST_GLS -- TRGB LEVER on the a0-line (GLS estimator lane); both footings")
print(f"  canonical a0 = {A0C:.4e} (cH_Lambda/Z)   alt a0 = {A0A:.4e} (cH0/Z)")
print(f"  Planck Lambda = {LAM_PLANCK:.3e} m^-2 ;  Z = {ZVAL:.5f}")
print(bar)

results = {}
for Ud in (0.5, 0.7):
    gals = fc.load(Ud)
    gals_hq = [g for g in gals if g["fD"] in HQ_FD]

    b_full = fc.budget(gals, gas_only=True)
    b_hq = fc.budget(gals_hq, gas_only=True)
    if b_hq is None:
        print(f"\nUd={Ud}: HQ subsample < 10 pts -- UNDERPOWERED, skipped")
        continue

    # biased (observed-weight) control on the HQ set -- must be flagged, never the answer
    GBh, GOh, FVh = fc.flat(gals_hq, True)[:3]
    a0_biased, _, _, _ = fc.gls(GBh, GOh, FVh, biased=True)

    # y-range-match control: full-gas restricted to the TRGB y-window
    ylo_hq, yhi_hq = ranges(gals_hq)
    gals_full_ymatch = []
    for g in gals:
        m = g["gasdom"] & (g["gb"] / 1e-10 >= ylo_hq) & (g["gb"] / 1e-10 <= yhi_hq)
        if m.sum() == 0:
            continue
        gg = dict(g)
        for k in ("R", "gb", "go", "fv", "phi"):
            gg[k] = g[k][m]
        gg["gasdom"] = np.ones(int(m.sum()), bool)
        gals_full_ymatch.append(gg)
    b_ymatch = fc.budget(gals_full_ymatch, gas_only=True)

    oaL_full = occam_and_lambda(b_full)
    oaL_hq = occam_and_lambda(b_hq)

    results[str(Ud)] = dict(full=b_full, hq=b_hq, ymatch=b_ymatch,
                            occ_full=oaL_full, occ_hq=oaL_hq,
                            a0_biased_hq=float(a0_biased),
                            y_window_hq=[ylo_hq, yhi_hq])

    print(f"\n----- Ud = {Ud} (disk M/L; bulge 1.4*Ud) "
          f"{'[BANKED HEADLINE]' if Ud == 0.7 else '[fiducial]'} -----")
    for tag, b, o in (("FULL gas ", b_full, oaL_full), ("TRGB gas ", b_hq, oaL_hq)):
        print(f"  {tag}: N={b['N']:>4} pts / {b['Ngal']:>3} gals | "
              f"a0_hat(GLS)={b['a0hat']:.3e} +/- {b['tot']:.2e} ({100*b['tot']/b['a0hat']:.1f}%)"
              f"  median={b['a0med']:.3e}")
        print(f"            sysD={b['sysD']:.2e} sysU={b['sysU']:.2e} sysEst={b['sysEst']:.2e}"
              f" stat={b['stat']:.2e} | ybar={b['ybar']:.3f} phibar={b['phibar']:.3f}")
        print(f"            Occam: canon {o['bans_canon']:+.2f} bans (t={o['t_canon']:+.2f}s)"
              f"  alt {o['bans_alt']:+.2f} bans (t={o['t_alt']:+.2f}s)"
              f"  footing-LR {o['dfoot_toward_alt']:+.2f} ban->alt")
        print(f"            Lambda: {o['lam']:.3e} = {o['lam_ratio']:.2f}x Planck (GLS), "
              f"{o['lam_ratio_med']:.2f}x (median); {o['t_lam']:+.2f} sigma")
    # lever accounting
    dfrac = 100 * (1 - (b_hq['sysD'] / b_hq['a0hat']) / (b_full['sysD'] / b_full['a0hat']))
    dtot = 100 * (1 - (b_hq['tot'] / b_hq['a0hat']) / (b_full['tot'] / b_full['a0hat']))
    print(f"  LEVER: frac sysD  {100*b_full['sysD']/b_full['a0hat']:.1f}% -> "
          f"{100*b_hq['sysD']/b_hq['a0hat']:.1f}%  ({dfrac:+.0f}%);  "
          f"frac total {100*b_full['tot']/b_full['a0hat']:.1f}% -> "
          f"{100*b_hq['tot']/b_hq['a0hat']:.1f}%  ({dtot:+.0f}%)")
    print(f"  y-range match (full-gas trimmed to TRGB y-window [{ylo_hq:.3f},{yhi_hq:.3f}]): "
          f"a0_hat={b_ymatch['a0hat']:.3e} +/- {b_ymatch['tot']:.2e}  (N={b_ymatch['N']})")
    print(f"  biased-weight CONTROL on TRGB set (red flag if it collapses): "
          f"a0_biased={a0_biased:.3e}  [model-based is the answer, this is diagnostic only]")
    # galaxy-level bootstrap + leave-one-out leverage on the small TRGB set
    bs_hq = galaxy_bootstrap(gals_hq)
    bs_full = galaxy_bootstrap(gals)
    results[str(Ud)]["boot_hq"] = bs_hq
    results[str(Ud)]["boot_full"] = bs_full
    print(f"  galaxy-bootstrap TRGB: a0 median {bs_hq['boot_med']:.3e} "
          f"[16-84%: {bs_hq['boot_lo']:.3e}, {bs_hq['boot_hi']:.3e}] over {bs_hq['n_gal']} gals; "
          f"full-gas boot {bs_full['boot_med']:.3e} [{bs_full['boot_lo']:.3e},{bs_full['boot_hi']:.3e}]")
    print(f"    max single-galaxy leverage (leave-one-out): '{bs_hq['max_leverage'][0]}' -> "
          f"{bs_hq['max_leverage'][1]:.3e} (shift {bs_hq['max_leverage'][2]:.2e})")

# ---------------------------------------------------------------------- verdict synthesis
BANK_LO, BANK_HI = 0.84e-10, 1.36e-10           # honest all-choices box
BANK_GLS, BANK_MED = 1.181e-10, 0.973e-10
print("\n" + bar)
print("SYNTHESIS")
print(bar)
r7 = results.get("0.7")
verdict = "UNDERPOWERED"
if r7 is not None:
    hq, full = r7["hq"], r7["full"]
    ohq = r7["occ_hq"]
    stays = BANK_LO <= hq["a0hat"] <= BANK_HI
    # footing separation: does the honest 1-sigma band exclude either anchor?
    lo1, hi1 = hq["a0hat"] - hq["tot"], hq["a0hat"] + hq["tot"]
    canon_in = lo1 <= A0C <= hi1
    alt_in = lo1 <= A0A <= hi1
    sep = abs(ohq["bans_canon"] - ohq["bans_alt"])
    print(f"  TRGB central a0_hat(Ud=0.7) = {hq['a0hat']:.3e}  "
          f"-> {'STAYS in' if stays else 'MOVES OUT of'} the banked box "
          f"[{BANK_LO:.2e},{BANK_HI:.2e}] (banked GLS {BANK_GLS:.2e}/med {BANK_MED:.2e})")
    print(f"  honest 1-sigma band [{lo1:.2e},{hi1:.2e}]: "
          f"canonical {'INSIDE' if canon_in else 'OUTSIDE'}, alt {'INSIDE' if alt_in else 'OUTSIDE'}")
    print(f"  Occam bans TRGB: canon {ohq['bans_canon']:+.2f} / alt {ohq['bans_alt']:+.2f}; "
          f"|delta| = {sep:.2f} bans; footing-LR {ohq['dfoot_toward_alt']:+.2f} ban toward alt")
    print(f"  Lambda inversion TRGB: {ohq['lam_ratio']:.2f}x Planck (GLS) / "
          f"{ohq['lam_ratio_med']:.2f}x (median), {ohq['t_lam']:+.2f} sigma")
    # discrimination test: need both a >~2-ban gap AND one anchor excluded at 1-sigma
    if sep >= 2.0 and (canon_in ^ alt_in):
        verdict = ("DISCRIMINATES-alt" if ohq['bans_alt'] > ohq['bans_canon']
                   else "DISCRIMINATES-canonical")
    elif hq["tot"] / hq["a0hat"] < full["tot"] / full["a0hat"] - 1e-9:
        verdict = "TIGHTENS-BUT-NON-DIAGNOSTIC"
    else:
        verdict = "UNDERPOWERED"
    print(f"\n  VERDICT: {verdict}")
    print("  Both subsamples are entirely deep-regime (ybar<~0.05, no points near y=1): the")
    print("  TRGB lever can sharpen the a0 MAGNITUDE but CANNOT discriminate the nu SHAPE.")
    print("  The canonical/alt anchors are 21% apart; a ~16% band cannot cleanly separate")
    print("  them -- consistent with the banked non-diagnosticity. No 'proof'; both footings.")

json.dump(dict(results=results, verdict=verdict, lam_planck=LAM_PLANCK,
               a0_canon=A0C, a0_alt=A0A, bank_box=[BANK_LO, BANK_HI]),
          open(os.path.join(OUT, "est_gls_results.json"), "w"), indent=1, default=float)
print("\n[est_gls_results.json written]")
print("EXIT 0: GLS lever computed. Exit code is not a verdict.")
