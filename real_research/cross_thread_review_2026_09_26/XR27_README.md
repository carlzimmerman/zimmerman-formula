# XR27 — the external-field systems in the chain's band-passed law

Cross-thread review, 2026-09-27. Read-only on every other file: three new scripts in this folder, each with controls
that reproduce committed numbers and a MUTATE run that fails (rc = 1). Both a0 footings in every chain cell (FP0:
9.3603e-11 / 1.1312e-10 m s⁻²). κ = ½ stays fitted. No new constant is added.

**Question.** Nobody had scored the EFE systems in the derivation chain's law. The separator band-passes the kernel's
argument: a uniform external field is removed (FP11 F11j), while a host closer than about L partly survives. That could
flip the EFE samples M* fails, or break the systems that seemed to favour an EFE.

**Answer.**
- None of M*'s three EFE failures flips at any L in 0.5–5 Mpc under the record's own gates. That includes H_Y's cell
  (1.69 Mpc) and H_S's (2.88 Mpc).
- No L passes both classes. No L passes even one whole class.
- Every dwarf-scale system is L-independent. Their hosts sit within about 0.3 Mpc. Even at L = 0.5 Mpc, (1 − S_L) keeps a
  median 99.8% of the host's field there, and ≥ 95% out to 0.3 Mpc. For these systems the chain is M* up to the kernel
  (P2 against ν_mono; ≤ 0.4σ).
- Two systems depend on L, and they pull opposite ways. That is a new pincer:
  - the cluster-infall slope improves only at short L;
  - Chae's SPARC signal needs long L.

## The law as scored

This is FP11's QUMOND statement of the chain's static law, with nothing added:
g = g_N + P(1 − S_L)X(g_bp), with g_bp = (1 − S_L)g_N. The kernel is P2, and the argument reads baryons only (FP10's L353
pair).

For a satellite much smaller than both its distance D from the host and L, the internal dynamics reduce to the ordinary
QUMOND EFE with the host's field replaced by its band-passed value:

  e_bp(D) = G[M_h(<D) − (S_L M_h)(<D)]/D²

- For a point host this is e_N·Efac(D/L).
- For extended hosts it uses FP6's shell smoothing (checked against quadrature to 9e-6).
- The term the reduction drops is the output filter's smoothed host-phantom density. Its median is ≤ 2e-3 of the
  object's dynamical mass (K2c).

Each sample is scored in the record's own statistic:
- the XR4/XR6/XR9 cluster slope, in the scalar-sum and subtract forms;
- statistic C for the LV dwarfs;
- L23's arm for the Coma UDGs;
- g05/u02/h43 for Crater II, DF2/DF4 and the M31 dwarfs;
- Chae+2021's medians for SPARC.

A third form is reported beside them and never pooled: the exact sphere-averaged ("flux") monopole of FP11's own
interaction field, over the host's actual non-uniform band-passed field.

Scan: L = 0.5–5 Mpc, plus L → ∞, plus the two separators' own cells at each system's redshift:
- H_Y: FP9's L(z), with its yield.
- H_S: FP13's committed headline length. It is pending FP19, because XR18 found H_S ill-posed as written.

## Verdicts (σ against the data; `XR27_gate_table.out`)

| System (record statistic) | L → ∞ (chain, P2) | L = 0.5 Mpc | H_Y | H_S | M* | Flips? |
|---|---|---|---|---|---|---|
| Cluster-infall BTFR slope, all variants (N = 314) | 2.35–5.30 | 1.06–4.57 | 2.11–6.39 | 2.35–5.91 | 2.23–6.28 | **no** (see note) |
| … scalar-sum form only | 3.36 | **1.83** | 3.30 | 3.45 | 3.36 | only at 0.5 Mpc |
| … flux form (reported) | 3.36 | **1.39** | 2.82 | 3.17 | — | only at L ≤ 0.8 Mpc |
| … zero point (members − field) | 3.35 | **1.02** | **1.12** | 2.18 | 0.01–3.15 | passes for L ≤ 2.4 Mpc |
| LV dwarfs, statistic C (N = 92) | 3.92–4.58 | 3.93–4.59 | 3.92–4.58 | 3.92–4.58 | 3.87–4.48 | **no**, at any L |
| Coma UDGs, central arm (worst of footings and extents) | 4.61 | 3.07 | 4.34 | 4.52 | 4.20–4.35 | **no** (best 2.83) |
| Crater II (g05, exact QUMOND; EFE prediction 1.30 km/s) | 4.22–8.12 | same | same | same | 4.07–7.85 | no |
| DF2 (u02; predicted 18.9 km/s) | 1.2–3.5 | same | same | same | 1.3–3.6 | no |
| DF4 (u02; predicted 19.2 km/s) | 1.2–4.6 | same | same | same | 1.3–4.7 | no |
| M31 dSphs (LVD + Collins+2013 medians) | 2.9–4.7 | 2.8–4.7 | 2.9–4.7 | 2.9–4.7 | 2.8–4.7 | no |
| Chae D2, as catalogued (fitted median 0.060 vs the predicted band) | **0.0** | 4.2 | 2.9 | 2.8 | 2.9 | passes only for L ≥ 4.5 Mpc |
| Chae D2, group-collapsed geometry | **0.0** | 2.3 | **1.3** | **1.0** | — | passes for L ≥ 0.6 Mpc |
| Chae D1 (median fitted e~ 0.053, 143 galaxies; any geometry) | **0.8** | 2.9 | 2.4 | 2.3 | 3.5–3.6 | passes only at 5 Mpc |

Bold marks a pass. The pass rule is XR9's: every variant ≤ 2σ.

**Clusters.**
- The record's gate needs both 1-D forms. The subtract form never gets below 2.99σ, because it keeps a √e_bp deficit
  even when e_bp is 2% of e_N.
- Between 0.8 and 1.4 Mpc the subtract form is *worse* than L → ∞ (up to 6.44σ). The band-pass removes the EFE from the
  outer members first, so it acts as a smoothed version of M*'s step.
- The zero point is a secondary statistic. It passes at H_Y (1.12σ).

**Coma UDGs.**
- The band-pass strips Coma's extended baryons fast: only 6–41% of the field is kept at L = 0.5 Mpc.
- The offset still stays at +0.72 dex (3.0σ). The isolated floor is about 2σ, and P2 adds +0.05 dex.

**The dwarf-scale "EFE-favouring" systems do not favour the EFE in the record's own statistic at Υ_V = 2, for M* as well
as for the chain.**
- **Crater II** lies between the exact-QUMOND EFE prediction (1.30 km/s, 4.2σ too cold) and the isolated one
  (3.87 km/s, 2.8σ too hot). The EFE "success" lives in the literature convention: full mass and projected R_h give
  0.06–2.48σ.
- **DF2 and DF4** get almost no EFE in QUMOND, because the Newtonian host field is 0.023 a0, below their internal y.
  Famaey et al.'s 13.4 km/s reads the host's MONDian field (reproduced as the reported control C2b). Neither M*'s law nor
  the chain's does that.
- **The M31 dwarfs** fit better without the EFE: +0.121 dex isolated against +0.300 with it. This is h43's
  Υ_V ≈ 14–24 tension.

**Chae's signal** is the only EFE-favouring system that needs the EFE at full environmental strength.
- At L → ∞ the chain reproduces Chae's agreement: D2 inside the band, D1 at +0.8σ.
- At H_Y's L the band-pass keeps a median 2.3% of each galaxy's environmental field in the catalogued 3-D geometry, and
  27% in the group-collapsed bracket.
- The verdict is therefore bracket-dependent at the separators' L:
  - catalogued: D2 2.8–2.9σ, D1 3.3–3.5σ;
  - collapsed: D2 1.0–1.3σ, D1 2.4σ.
- Redshift-space distances scramble exactly the Mpc-scale geometry the band-pass reads.
- M* also fails Chae's signal: D2 2.9σ (approximate region-overlap rule). No thread had scored M* on it before.

## One L for both classes? No. Where the pincer sits

| Requirement | L window (Mpc) |
|---|---|
| Cluster slope, flux form (scalar form alone) | ≤ 0.8 (≤ 0.5) |
| Chae D2, catalogued (group-collapsed) | ≥ 4.5 (≥ 0.6) |
| KiDS (FP9 R9j: L(0.25) ≳ 1.2 Mpc, so L(0) ≳ 1.56 at n = 2); **pending FP20**, since FP9's KiDS used esd_of_M | ≳ 1.56 |
| LV dwarfs, Coma UDGs, Crater II, DF2/DF4, M31 dSphs | none in 0.5–5 |

**The new pincer.**
- The cluster slope wants L ≲ 0.8 Mpc; Chae's signal, as catalogued, wants L ≳ 4.5 Mpc.
- Only the most lenient readings of both overlap: the flux form together with the collapsed geometry, at 0.6–0.8 Mpc.
  Even there, Chae's D1 fails (2.6–2.8σ).
- That window also lies below KiDS's floor and below both separators.
- Every dwarf-scale system fails independently of L. This part is not new: it is inherited from MOND at Υ_V = 2.

## Controls and MUTATE

| Script | Controls (all pass) | MUTATE (must fail) |
|---|---|---|
| `XR27_efe_disfavouring.py` (~70 s) | C1: XR6's S0 and S1 rows (24 × 8) and XR9's uncapped range, 0e+00. C2: XR4's statistic C and M*'s XR9 rows, exact. C3: XR6's UDG candidate arm = M*'s XR9 rows, 0e+00. C4: FP11's committed K3 two-body numbers from FP11's own definitions, 0e+00. K1: band-pass machinery. F1: flux-form limits | The host field enters un-band-passed: B1 fails, rc = 1 |
| `XR27_efe_favouring.py` (~80 s) | C1: g05's +0.492 and project15's 1.93 / 1.71 km/s. C2: u02's DF rows (≤ 4.6e-4 dex) and h8's dispersions. C3: u02's and h43's M31 medians. C4: the 2M++ rebuild's estimator (exact), its CSV (5e-6), and Chae's 0.053 / 143 | Every source enters un-band-passed: B1 fails, rc = 1 |
| `XR27_gate_table.py` | T1: bookkeeping | Reads the MUTATE JSONs: T2 fails, rc = 1 |

**The L → ∞ limit against M*.**
- The dwarfs' and UDGs' M* numbers are the chain's L → ∞ limit with M*'s kernel, and are reproduced exactly.
- The cluster number differs. M* screens the members beyond its κ cap: 8% under the "galaxy" reading, 49% under the
  "two-field" reading, at the converged cell. That region rule has no counterpart in the chain. The chain's L → ∞ limit
  is XR6's S1 row, which is reproduced exactly.
- The kernel alone (P2 against ν_mono or ν_RAR) moves the worst σ by 0.39 (clusters), 0.10 (dwarfs) and 0.26 (UDGs).

## Pre-declared hypotheses, as they fell

- H1 (the dwarfs do not flip): held.
- H2 (the cluster slope flips at L ≲ 1 Mpc and fails at both separators): **failed**. It never flips under the record's
  gate. The second clause held.
- H3 (the UDGs do not flip): held.
- H4 (the kernel moves each worst σ by < 0.5σ): held.
- G1 (Crater II is L-independent, EFE > 2σ off): held.
- G2 (DF2/DF4 > 3σ in every variant): **failed**. The most lenient variants are 1.2σ (DF2: Emsellem's σ at 13 Mpc;
  DF4: van Dokkum's asymmetric error at 13 Mpc). At 20 Mpc, DF2 is 1.9–3.1σ and DF4 is 1.5–4.3σ.
- G3 (the M31 EFE offset exceeds the isolated one): held.
- G4 (Chae: > 3σ at both separators, no scanned L passes): **failed**. D2 is 2.9 / 2.8σ, and L = 4.5–5 Mpc passes.
- G5 (M* fails Chae D2): held.

## Disclosed

**Development runs, all overwritten by the committed MUTATE-then-main sequence.**
- Lane 1 had three runs:
  - The pre-declared K2 failed. Its bound is loose: a sphere average feels only the divergence of S_L X.
  - K2b was added post-hoc and failed too. It put the host's whole phantom inside D + 5L into one Gaussian ball.
  - K2c was added post-hoc and passes. It computes the actual smoothed density with FP6's shell smoothing.
  - K2 and K2b are kept as run.
  - The flux form was extended to every cell, and per-form pass sets were added.
  - Run 2 crashed on those new keys in the final print loop (a KeyError). This was fixed in run 3.
  - No scan number changed between runs.
- Lane 2 had one run. It used catalog_mode 'full' and the rounded CSV test points, and load-bearing C4 failed (0.15 dex).
  The rebuild's log shows its CSV was made in 'ks115' from the unrounded VizieR SPARC table. This lane now does the same,
  and carries 'full' as a variant, which moves D2 by ≤ 0.1σ. M*'s rows for Crater II, DF2/DF4 and M31 were added after
  that run.

**A background both forms drop (K2c).** Plain QUMOND's host-phantom density at the object is dropped by the record's
forms for M* and by this lane for the chain alike. Its median is ≤ 1e-2 of the dynamical mass, but it reaches 1.2 for
the worst cluster member and 1.0 for the worst dwarf. That is a tidal-scale term neither model's scoring carries.

**No lensing projection is used.** esd_of_M is not used. KiDS's L floor is quoted from FP9 and is pending FP20.

## Scope

- Spherical hosts and 1-D kinematic forms, plus the exact monopole. Discs and anisotropy are not modelled.
- Υ_V = 2.
- Member 3-D radii are the projected radii times 1 and 1.3.
- Coma's β-model tail is extrapolated; the r200 truncation brackets it.
- Hosts' tides and the members' neighbours are not modelled.
- 2M++ is shallow (Ks ≤ 11.5). The max-clustering bracket up-weights visible galaxies.
- Chae's e~ carry his fitting function and a0 = 1.2e-10; no rotation-curve re-fit exists on disk.
- No particle-mesh run.

## Files (only these)

| Stem | Script | Output | Results | MUTATE output | MUTATE results |
|---|---|---|---|---|---|
| `XR27_efe_disfavouring` | `.py` | `.out` | `_results.json` | `_MUTATE.out` | `_results_MUTATE.json` |
| `XR27_efe_favouring` | `.py` | `.out` | `_results.json` | `_MUTATE.out` | `_results_MUTATE.json` |
| `XR27_gate_table` | `.py` | `.out` | `_results.json` | `_MUTATE.out` | `_results_MUTATE.json` |

Plus this `XR27_README.md`.

Run from the repository root, in this order: the two lanes, then `XR27_gate_table.py`. Add `MUTATE=1` for the controls,
and run those before the main runs.
