# E6_native_fret — FROZEN CRITERIA (written before any script or number of this lane)

Wave E follow-up to E3 Part B. E3 found the sub-threshold satellites' extra bound cold mass is UNDECIDABLE because the
supply ceiling C = 5.364 · M_b / f_ret turns on f_ret (the catchment-to-present baryon ratio), which only the ΛCDM-processed
census fixes. This lane asks for a **framework-native rule for a satellite's catchment**: turnaround in the framework's own
background, tidal truncation by the host in the framework's own law, and what is retained. Then it recomputes E3's
per-system available-vs-required cold mass on both footings.

κ = ½ FITTED. Footings canonical a0 = 9.3603e-11, alt 1.1312e-10 m/s², never pooled. Cold energy, no particle.
Not "theory closed". Nothing here says the data favour the framework.

## Record checked before freezing
E3 (README, script, per-system CSV); CFG920 (leaky-box loss, UNDERDETERMINED on the Fe yield); CFG953 SCT rules R1–R3
(domain born at turnaround; labelled dust inert; body capped at the catchment's cold); CFG959 (H-UNR fails dSphs; native
supply = 5.364 × census catchment); CFG822/823/842/888/889 (dwarf supply/binding); CFG804 (catchment N = 1/f_ret, census);
CFG806 (native f_ret: NOT DERIVED; cooling/feedback decide baryon retention); CFG886 (5.364 recovered not pinned; f_ret MIXED);
CFG424 (phantom source sums to zero on every catchment); CFG557 D1 (candidate-B switch = the turnaround ball);
CFG548 (law ON outside bound systems overshoots the LG zero-velocity radius ~2×, Z +6); CFG654 (native Δ_ta(z), law off
until turnaround = primary; native IC column h 0.67403, Ω_cb 0.31285, A_s, n_s, σ8 0.8271); THEORY_CANONICAL 10-21 draft
(f_ret input, NOT DERIVED); memory notes on CFG860 and CFG822–889. Covariant push C2/C4: dust abundance is an initial condition.

## Part D — the native catchment rule (dynamics)

**D1 (analytic, stated before computing).** In the record's rules the law acts only inside the turnaround ball (CFG557 D1,
CFG654 primary, SCT R1; the law-on-outside reading is excluded by CFG548), and the phantom it builds there is drawn from the
same catchment so the source sums to zero on it (CFG424, SCT R3). By Gauss, a shell outside the ball feels the true enclosed
mass, so its turnaround is GR dust + Λ spherical collapse in the framework's background (𝒮 = 0 on FRW). Hence a satellite's
catchment mass M_ta is set by the linear overdensity profile δ_L(M) of its Lagrangian patch (an initial condition) and by
the epoch at which accretion stops; **M_b, a0, κ and L★ do not enter.** Baryon retention (what fraction of the catchment's
baryons is in the satellite today) is set by cooling and feedback (CFG806), not by the law. The cold supply itself needs no
baryon retention: C = 5.364 f_b M_ta = (Ω_c/Ω_m) M_ta.
Expected class from D1 alone: the dynamics leave M_ta (hence f_ret) **not fixed by M_b**. The numbers below quantify what
the required catchment is and what the framework's own tides demand of it; they do not fit anything to the dwarfs.

**D2 (tidal truncation in the framework's law).** At present host distance d (LVD distance_host; MW 6.0e10 M☉ baryons CFG332,
M31 1.0e11 labelled external, as in E3), host field g_h = g_N ν(g_N/a0), ν(y) = ½(1 + √(1 + 4/y)) (E3/A26 law; unscreened at
kpc). Tidal strength T = g_h/d − dg_h/dd. The satellite catchment, mass-conserving, has Newtonian self-gravity of its true
mass m, so r_J = (G m / T)^{1/3}. A catchment that must survive inside r_J must have turned around when its turnaround
sphere was at least that dense: Δ_ta(z) ρ̄_m(z) ≥ 3T/(4πG). This defines z_req per satellite, **independent of m**.
Δ_ta(z): CFG654 native N0 table (read-only, interpolated in ln(1+z)); ρ̄_m from the native column (h 0.67403, Ω_cb 0.31285).
Field systems (Leo T): no host, z_req not defined. Pericentres would raise T (z_req is the least demanding orbit-consistent
value at d_now, not a bound in the other direction for earlier, more distant infall: reported as such).

**D3 (initial-condition sensitivity — EXTERNALLY CALIBRATED).** Required catchment M_ta,req = M_c,req · 6.364/5.364 (q = 1).
Required linear overdensity today δ_req = δ_lin,ta(z_req) · D(0)/D(z_req), with δ_lin,ta from this lane's spherical-collapse
integrator and D from the CFG654 native lnD table. σ(M) from the CFG654 native z = 0 linear P(k) (A_s, n_s from the Planck
chain: ΛCDM-PROCESSED initial-condition column), top-hat, M in M☉/h; P(k) beyond the table's k_max = 110 h/Mpc extrapolated
with the log-slope over the last half-decade (bracket: slope n_s − 4). ν_req = δ_req / σ(M_ta,req). This says only whether
the **required** catchment is an ordinary fluctuation; it does not give a satellite's actual catchment (that needs its
infall epoch and the larger patches it sits in).

Two accountings, both reported: **F1** = E3's extra-only M_c,req = M_dyn − (M*/2)·B_scr (L★ = 24 pc); **F2** (mass-conserving,
the phantom is also paid from the catchment, CFG424) = M_dyn − M*/2 (E3's "Newton" row).

## Part C — chemical lower bound on the catchment (non-dynamical, reported with its own class)
Baryons that passed through a satellite's star-forming gas were in its catchment, so catchment baryons ≥ L_min · M_b. L_min
from CFG920's homogeneous leaky box (functions copied verbatim, K-checked), LVD [Fe/H] (column `metallicity`, as CFG920),
gas from LVD M_HI × 1.33, M* = E3's (Υ_V = 2). Corners log y ∈ {−0.5, −0.2, +0.1} × {W1, W2}; W2 = W1 for gas-bearing.
Assumption carried: wind at ISM metallicity (ζ = 1) and no pre-enrichment; ζ > 1 or pre-enrichment lowers L. ζ_need (price
of escaping) reported at log y = −0.5 for systems still short. Classified SURVEY-CALIBRATION (yield) + MODEL ASSUMPTION.
q_chem = L_req / L_min (L_req from E3's CSV). Systems without LVD [Fe/H]: NOT TESTED, counted.

## Outcome lines (frozen)

**Main verdict (dynamics, as the brief asks):**
- **SUPPLIES IT:** a native rule with no unfixed number gives median q ≤ 1 (bootstrap 84th percentile ≤ 1) on both footings.
- **SHORTFALL (N dex, systems):** a native rule with no unfixed number gives median q with bootstrap 16th percentile > 1 on
  both footings; or, under D3's externally calibrated IC column, the median ν_req ≥ 5 on both footings in F1 (then labelled
  "SHORTFALL under the IC column").
- **STILL UNDECIDABLE (ingredient named):** otherwise. The ingredient is named from D1–D3.

**D3 descriptive class:** IC-ORDINARY if median ν_req ≤ 3 (both footings, F1 and F2); IC-STRAINED if 3 < median ν_req < 5;
IC-FORBIDS if ≥ 5.

**Part C class** (both footings; tested systems only; bootstrap over systems, seeded):
- **CHEM-SUPPLIES:** at the most conservative corner (log y −0.5, W2) median q_chem ≤ 1 and its bootstrap 84th pct ≤ 1.
- **CHEM-SHORTFALL:** at the least conservative corner (+0.1, W1) median q_chem > 1 and its bootstrap 16th pct > 1.
- **CHEM-UNDERDETERMINED:** otherwise.
Also counted: systems with q_chem > 1 at the conservative corner using E3's 2.5% lower q (scaled by 10/L_min).
Part C does not override the main verdict (it is not dynamics); it is reported as the clean non-ΛCDM handle.

## Checks (script `e6_native_fret.py`, one line each; exit 0 iff all pass)
- K1 spherical collapse: Ω_m = 1 run gives ρ_ta/ρ̄ = 9π²/16 to ≤ 1e-4 rel and δ_lin,ta = 1.0624 to ≤ 1e-3; native-parameter
  dust+Λ run reproduces the CFG654 N0 Δ_ta table at z ∈ {0, 0.5, 1, 2, 4, 9} to ≤ 1% (CFG654 adds radiation + trickle).
- K2 catchment identity (code check, true by construction under Gauss; not a finding): a shell outside the turnaround ball
  turns around at the same time with the law on inside the ball (phantom drawn from the catchment) as with the law off,
  to ≤ 1e-6 rel.
- K3 E3 reproduced from its CSV: median q(f_ret 0.10) 0.811 canonical / 0.768 alt within 0.005; median L_req 8.3 / 8.0 within 0.1.
- K4 CFG920 reproduced: copied leaky-box L_min for Hercules, all six corners, within 1e-6 rel of cfg920_results.json.
- K5 IC column: σ8 from the CFG654 z = 0 P(k) within 0.5% of 0.8271.
- **--mutate:** the law acts on shells outside the ball as an extra (non-conserving) source (CFG654 bracket-B / CFG548
  reference reading). K2 must FAIL. Outputs `*_MUTATE.out`, `e6_native_fret_results_MUTATE.json`.

## Not blind (disclosed)
Before freezing, the author made back-of-envelope estimates: L_min ~ 40–150 for [Fe/H] ≈ −2.5 at ζ = 1; z_req ~ 9 at d ≈ 80 kpc;
ν_req ~ 1–2 for M_ta ~ 6e5 M☉. E3's numbers and CFG920's were seen. No threshold above was moved after those estimates.

Compute: one thread, nice 15, < 1 GB, seconds. Nothing downloaded. Writes only inside this lane.

## AMENDMENT A1 (after the first run crashed; PRE-RESULT for every D/C number — none was printed)
The first run printed only K1–K4 and then crashed in K5 (`np.trapezoid` is absent in NumPy 1.26; replaced by `np.trapz`,
no numerical change). K3 failed as frozen: it compared the median over systems of E3's per-system q (the CSV, 0.828 / 0.804)
with E3's printed headline 0.811 / 0.768, which is a different statistic (E3's `boot_median` over log q of all MC draws).
The L_req half of K3 is the same statistic as E3's printed `median_Lreq` and passed (8.28 / 8.04).
**K3 is replaced by K3′:** (i) median over systems of the CSV L_req equals E3's printed median_Lreq 8.3 / 8.0 within 0.1, and
(ii) per system q_fret010 = L_req / 10 to ≤ 1e-9 (E3 internal consistency of the CSV this lane uses). The frozen K3 line is
still printed, labelled "as frozen, mis-specified statistic", and does not enter the exit code. No other line changes.
