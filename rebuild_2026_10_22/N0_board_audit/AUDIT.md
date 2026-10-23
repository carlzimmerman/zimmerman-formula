# N0_board_audit: is every tile on the status board computed for the current best theory (v3)?

**The owner's instruction:** "we should only have the status of the current theory on the crispy fried chicken board but if
it changes we need to make sure all the calculations are current and reflect our best theory.. if something fails it should
be for our best theory."

This is a read-only audit. No calculation was rerun, apart from one kernel comparison (below, seconds, < 0.1 GB). Nothing on
the board, in the generator or in any lane was edited. κ = ½ is FITTED. The footings (canonical 9.3603e-11, alt 1.1312e-10
m/s²) are never pooled. No dark-matter particle. Not theory closed. Nothing here says the data favour the framework.

## The yardstick: v3 (`covariant_push_2026_10_22/THEORY_V3_DRAFT.md` §1–3)

- **Action:** the Blanchet–Skordis Khronon in its literal healthy form (β = 0, η = 0), an independent covector P, BS K(Q)
  dust, and one stiffness term −(γ_L/2)(D·P)².
- **Static limit:** AQUAL with μ = x/(1+x) exactly (E2, C4). It is not QUMOND, ν_RAR or ν_mono. Through BS24 Eq. 35 it also
  carries the dust's μ_K²ψ term (L1 frozen criteria §1).
- **Screening:** L★ ≥ 21.7 / 22.9 pc (D10), up to about 90 pc.
- **Cold sector:** BS dust with a fitted abundance. There are no settling, relocation, supply-edge, catchment, ownership or
  round rules, and no additive phantom.
- **v4 (AeST + γ_L) is not the best theory:** it is ill-posed off symmetry (I1) and runs away on FRW (C7).

## How each tile was checked

The 55 tiles in `explainers/make_status_board.py` (`TILES`) were taken one at a time. For each evidence lane, the README was
read, and the scripts were grepped for the kernel and the rules they use (ν_mono / ν_RAR / QUMOND / AQUAL / settling / supply /
catchment / gated / chassis / NFW / ΛCDM).

The only computation was a kernel comparison, ν_mono vs v3's ν₁ = (1 + √(1 + 4/y))/2, both from
`campaign_fresh_gravity/CFG2_common.py`. ν₁/ν_mono − 1 is:

| y = g_N/a₀ | ν₁/ν_mono − 1 |
|---|---|
| 0.01 / 0.05 / 0.084 | +0.04 % / +0.19 % / +0.30 % |
| 0.5 / 1 / 3 | +1.4 % / +2.3 % / +3.8 % |
| 10 / 50 | +2.2 % / +0.5 % |

So swapping the kernel moves g by at most 0.017 dex. Changes of verdict come from two other places: the **geometry** (AQUAL
in discs) and, above all, the **external-field effect (EFE) that v3's AQUAL has**.

## Cross-cutting findings (read these first)

1. **v3 has an EFE everywhere. The old "isolated law, no EFE" ownership class is gone.**
   - Many tiles were computed with the EFE-free law: satellites, tidal dwarfs, DF2/DF4, Coma UDGs, low-g lensing, red lenses.
   - Each of these has to be redone in its host's field, and several are **at risk of turning red**:
     - **TDGs.** The nearest computed analogue, CFG953's SCT-Q with a host EFE, puts the Lelli+15 TDGs at −0.38 / −0.41 dex
       against the observed −0.69 / −0.73 (z −3.5 / −3.8).
     - **Satellites.** F3 estimates the EFE costs −0.30 dex on a satellite's boost.
     - **Coma UDGs.** The data sit +0.76 ln above the isolated law, and Newton is excluded at z +5.45 (CFG948).
2. **v3's static equation has a μ_K²ψ term (BS24 Eq. 35).** With μ_K at or below BS's cap of 14.8 h/Mpc, it acts beyond about
   0.1 Mpc. F1 (clusters) and F2 (outer lensing) were run without it. H2's AeST analogue of the same term cannot fix the
   cores (wrong shape), but no v3 run exists. SMALL (batch R6).
3. **CFG960 is not a v3 test.** It is the SCT-M engine (domains, conversion of cold energy into phantom bodies, census
   baryons).
   - Since the board was drawn, SC1x has been scored: **FAILS, KiDS EXCLUDED, Δχ² +47.28** (89fbefe1c0), and the chain was
     stopped.
   - The v3 shear and nonlinear-growth test is **L1_khronon_pm's frozen 512³ plan** (062b199c77). That is the one HEAVY
     item.
4. **16 of the 55 tiles test models that v3 does not contain.** These are the settling engine, the supply edge, ownership,
   the round rule, the 2026-09 filtered C-H/K chassis, v4, and the SCT-M and theory-v2 engines. Under the owner's
   instruction they leave the current-theory board. Three of them are in `MUST_STAY_RED`, so removing them needs a generator
   edit: "Growth, zero-knob supply rule", "Linear growth, v4 AeST" and "v4 well-posedness".
5. **No STALE tile needs a simulation.** All 15 STALE recomputes are SMALL (< 1 GB, one thread). The only HEAVY item is L1's
   production run, which stands in for 5 retired tiles and the open escape in "Covariant completion".

## Counts

| class | tiles |
|---|---|
| CURRENT | 15 |
| STALE | 15 (all SMALL; 5 at risk of a colour change: rows 17, 19, 25, 29, 30) |
| OLD-MODEL ONLY | 16 |
| DATA-GATED / OPEN | 9 |

## The table

Columns: C0 = Relativistic theory (the chassis), C1 = Galaxies, C2 = The excess family, C3 = Cosmology and a₀ over time,
C4 = The deep 'why' and the parent.

| # | tile | col | colour | class | mismatch with v3 (or why it is identical) | v3 recompute needed | size |
|---|---|---|---|---|---|---|---|
| 1 | Gravity waves at light speed | C0 | PASS | CURRENT | C5 and C8 are v3: β = 0 gives c_T = 1, and only the 2 tensor modes propagate. CFG292 (2026-09 chassis) also has β = 0, so its tensor sector is identical | none | — |
| 2 | Health: ghosts, gradients | C0 | COND | CURRENT | C5 is v3 (literal β = η = 0, BS dust, γ_L > 0). The note also cites H3, which is v4: drop it | none (re-annotate) | — |
| 3 | Leaf problem well-posed | C0 | COND | CURRENT | C8 is v3's own leaf functional | none | — |
| 4 | Causality: criterion A / B | C0 | COND | CURRENT | C5 and C8 are v3 | none | — |
| 5 | v4 well-posedness | C0 | FAIL | OLD-MODEL ONLY | v4 (AeST + γ_L) is not v3. v3 counterpart: I1 shows that a hypersurface-orthogonal (Khronon) aether is the well-posed case, i.e. tile 3 (C8) | none; remove (also from `MUST_STAY_RED`) | — |
| 6 | Lapse condition, realistic matter | C0 | PASS | OLD-MODEL ONLY | CFG294/312 lapse kernel W of the filtered C-H/K chassis (Bianchi-I leaves, C-H sector absent, ν_mono). v3's lapse sits inside C8's strictly convex leaf functional. v3 counterpart: tile 3 | optional strong-field leaf check in R5 | SMALL |
| 7 | Binary pulsars + GW170817 | C0 | PASS | CURRENT | C8 is v3: no radiative channel (≤ 3.2e-14 of the double-pulsar error), Δv/c ≤ 6e-32. CFG291 and CFG311 are the filtered C-H/K chassis at α_c ≠ 0 with ν_mono: drop them from the lanes | none (re-annotate) | — |
| 8 | Solar system + Cassini (screened) | C0 | PASS | CURRENT | C6 is the v3 literal form (γ_F = 0, AQUAL, both footings, fields E0–E3): 2.8e7–5.1e9 inside. D7d (curl-stiffened A33 form) is superseded. Disclose that C6's frozen verdict is UNDECIDED on one float-rounding check | none | — |
| 9 | Unscreened law vs Cassini | C0 | FAIL (control) | CURRENT | E2 is v3's AQUAL μ = x/(1+x) at L★ = 0: 2.44–4.59× canonical, 2.85–5.19× alt. D7c (QUMOND family) is superseded | none | — |
| 10 | Strong coupling | C0 | COND | STALE | XC1/XC3 used the heat-filtered C-H/K chassis (S[h] = exp(bΔ_h), ν_mono splice, α_c, c_2). v3 has no filter; its kinetic structure is the BS khronon (β = 0) + J_x + γ_L + K(Q) dust | yes: v3 strong-coupling scale on Solar, galaxy and cluster backgrounds (R5) | SMALL |
| 11 | Matter conservation (G9) | C0 | PASS | CURRENT | Identical by theorem: the Noether-II identity ∇T = 0 holds for any diffeomorphism-invariant action whose matter couples to g alone, and v3 (C4) is one. CFG329 computed it on the old chassis, but the result does not depend on the chassis | none (re-cite C4) | — |
| 12 | Structural order (G0) | C0 | COND | OLD-MODEL ONLY | G0 gate of the filtered C-H/K chassis. For v3 its content is C5 (no ghost) + C8 (elliptic, unique), already tiles 2–3 | none; remove (duplicate) | — |
| 13 | Zero-field nonlinear, ungated | C0 | FAIL | OLD-MODEL ONLY | ungated ν_mono chassis on open FRW (CFG321/358). v3 counterpart: L1's native nonlinear run | via L1 | HEAVY |
| 14 | Black holes (EHT, LIGO ringdown) | C0 | COND | STALE | CFG318/319 used the filtered C-H/K chassis at α_c ≠ 0 (L340 window, ν_mono). In v3 (BS Khronon β = 0, η = 0 + P + γ_L + dust) the strong field is OPEN (C8) | yes: v3 static exterior + slowly-moving regularity (Ramos–Barausse: regular only on α = β = 0) (R5) | SMALL (sympy/ODE; one thread, may take hours) |
| 15 | Rotation curves (SPARC RAR) | C1 | PASS | STALE (minor) | The kernel is v3's exactly (CFG695: g_N = g²/(g+a₀), 0.1009 / 0.0994 dex), but it was applied algebraically. v3 is AQUAL, which differs in discs. The QUMOND analogue (CFG516) puts the in-plane force up to 20 % below the algebraic value at R ~ 1 kpc, raises the rms by 0.006–0.008 dex and shifts fitted a₀ by +0.03 dex | yes: AQUAL axisymmetric solve on SPARC discs, giving rms and fitted κ (R3) | SMALL |
| 16 | Local a0 from MeerKAT | C1 | PASS | CURRENT | ν_mono was used, but all 47 galaxies are deep (y ≤ 0.084), where ν₁/ν_mono − 1 ≤ 0.3 % (computed here). The estimator is spherical V²/R, and disc-geometry effects are ≪ the 0.143 dex recipe width | optional (R3) | — |
| 17 | Isolated-galaxy lensing, inner | C1 | PASS | STALE (at risk) | "Supply suffices ≤ 0.31 Mpc" is the catchment supply rule (CFG804/902), and v3 has no supply rule. CFG829/840's blue-lens A = 1.016 used the isolated, EFE-free algebraic law. v3's AQUAL has an EFE, and in CFG829's window (g_bar ~ 1e-13) the weakest on-disk field (y_e = 7.8e-4, F2) is comparable to the internal field. F2's v3 inner number for all isolated lenses is A_in 1.13 ± 0.04 | yes: blue/red/all A in CFG829's window with F2's AQUAL + EFE solver and inventory baryons (R2) | SMALL |
| 18 | Isolated-galaxy lensing, all radii | C1 | UNDEC | CURRENT | F2 is v3: its own AQUAL μ = x/(1+x) solver, no edge, native h, an EFE grid. Caveat: run without v3's μ_K²ψ term | add the μ_K² term (R6) | SMALL |
| 19 | Tidal dwarfs, NGC 1052-DF2/DF4 | C1 | COND | STALE (at risk) | "At Newton if they captured no cold energy" is the supply/capture route (CFG936 route i, CFG939 no-capture), which v3 lacks. In v3 the law acts on all baryons, so the only route below the isolated law is the host EFE. CFG936's route iii (1-D QUMOND EFE) FAILS the TDGs, and CFG953's SCT-Q gives z −3.5 / −3.8 | yes: AQUAL in the host field for the 6 Lelli+15 TDGs and DF2/DF4 (R1). Could go COND → FAIL | SMALL |
| 20 | Outer globulars: L* floor | C1 | COND | CURRENT | D10 is v3: the C4-literal stiffened field equation, Plummer clusters in the Galaxy's field, no ν_RAR, no EFE recipe | none | — |
| 21 | Globulars + ownership rule | C1 | COND | OLD-MODEL ONLY | FG001 ownership classes (owned → Newton), ν_mono, QUMOND EFE (CFG332/333). v3 has no ownership. v3 counterpart: tile 20 (D10) | none; remove | — |
| 22 | Central ellipticals (SLUGGS) | C1 | UNDEC | STALE (verdict-safe) | ν_mono (2–4 % less ν than v3 at y = 1–10). Uses CFG331 machinery with the R-own / census-edge / round-rule options and the isolated law (centrals, so the EFE is small) | yes: CFG528b with ν₁, all baryons, no rules. The kernel moves σ by ≤ 0.01 dex against offsets of +0.06–0.15 dex (R4) | SMALL |
| 23 | Galaxy groups (BFJR) | C1 | PASS | STALE (relabel) | The tile's pass is "consistent supply closes" (CFG543 containment against CFG515's census edge), and v3 has no edge. v3's number already exists: CFG543's law-with-no-edge row, +0.010 / −0.010. That row is deep-regime with a whole-system aperture (σ⁴ = (4/81)GMa₀, independent of μ's transition), and spherical, so AQUAL = algebraic | relabel; optional EFE check (R4) | none / SMALL |
| 24 | MW vertical force (round rule) | C1 | PASS | OLD-MODEL ONLY | The round enclosed-mass rule is not in v3. v3's disc phantom is AQUAL's own, which is disc-like. Its nearest computed analogue, the QUMOND phantom disc (PD, ν_mono), lost in all 32 K_z cells (PD − NFW +80 to +477, CFG516) | v3 counterpart "MW vertical force, AQUAL disc" must be computed and is at risk of FAIL (R3) | SMALL |
| 25 | MW outer slope (Gaia) | C1 | UNDEC | STALE (at risk) | round rule (RM-v / RM-φ) + ν_mono, no AQUAL, no EFE (CFG532b/533) | yes: AQUAL disc curve, 15–27.5 kpc slope (R3) | SMALL |
| 26 | Dwarf satellites vs screened law | C2 | FAIL | STALE | E3 used v3's kernel (ν₁) but the isolated CFG691/820 screening factor S(s) and no EFE; its EFE row (+1.25 dex) is only a 1-D QUMOND diagnostic. G2 tests PAPER36's retention rule (old model). v3 means AQUAL in the MW/M31 field with native screening (D10: screening in a field is not multiplicative) | yes: D10 solver on the 45 satellites (R1). FAIL will not lift; the +0.89 dex number changes | SMALL |
| 27 | Dwarf cold supply (chemistry) | C2 | COND | OLD-MODEL ONLY | catchment supply, ζ = 1 winds, bound cold energy (E6). v3's cold sector is BS dust with no supply or capture rule. v3 counterpart: dust capture into satellites, which only L1 can answer | via L1 | HEAVY |
| 28 | Cluster cores (318 eRASS1) | C2 | FAIL | CURRENT | F1 is v3: AQUAL (vs QUMOND ≤ 4 %), native h, raw KiDS on **326** clusters (the tile says 318). Caveats: the note cites H2 (v4); v3's μ_K²ψ term is not included (H2's AeST analogue cannot help: wrong shape) | add the μ_K² term (R6); fix the note | SMALL |
| 29 | Coma ultra-diffuse galaxies | C2 | UNDEC | STALE (at risk) | Uses the isolated, EFE-free law with ν_mono (CFG933), CFG928's P2 posit and CFG948's no-capture ceiling (P-medium). In v3 the UDGs sit in Coma's field, and AQUAL's EFE pulls the prediction toward Newton × ν_e. The data sit +0.76 / +0.67 ln above the isolated law, and Newton is excluded at z +5.45 | yes: AQUAL + Coma field per UDG (R1). Could go UNDEC → FAIL | SMALL |
| 30 | Red (early-type) lenses | C2 | COND | STALE (at risk) | EFE-free law (ν_e / ν_mono; QUMOND in CFG926 R6) + CFG667's +0.123 dex + the IMF α–σ posit. In v3 red lenses sit in denser fields, so the EFE adds to the excess | yes: F2 solver with EFE, IMF variant (R2) | SMALL |
| 31 | One selector for the family | C2 | OPEN | DATA-GATED / OPEN | J1 and K1 used v3-era numbers (F1, E3). CFG914/919/921/928 graded excesses over the old EFE-free ν_mono law. The family's membership has to be re-derived once R1, R2 and R6 are in | after R1 / R2 / R6 | — |
| 32 | a0(z): native band vs a0 ~ H(z) | C3 | UNDEC | DATA-GATED / OPEN | The computation is background-only (BAO + BBN; a₀ cannot enter v3's FRW, C2), so it holds for v3. v3's action has a constant a₀ in J_x; the √ρ_DE(z) tracking is the owner's 10-06 postulate, not in the action. v3 predicts the flat line, which lies inside CFG689's band | none | — |
| 33 | High-z on halo-free inputs | C3 | UNDEC | STALE (verdict-safe) | ν_mono with the algebraic disc law (CFG303). The kernel moves g by ≤ 0.017 dex, ≪ the lanes' spreads | optional kernel swap (R4) | SMALL |
| 34 | CRISTAL z~5 / ALESS 122.1 | C3 | UNDEC | STALE (verdict-safe) | ν_mono (CFG307/308). s★ spans a factor of 3–15 across the grids | optional kernel swap (R4) | SMALL |
| 35 | Cosmic shear, native inputs | C3 | COND | OLD-MODEL ONLY | The theory-v2 PM engine (T1x/T2x/NC1x/NC2x): switch, catchment, census edge, settling/relocation, QUMOND ν_mono phantom (F3 §1). It has no parent (CFG941–955). v3 counterpart: F3's linear S₈ (μ_K → ∞: 0.814–0.845, 0.9–1.5σ from raw KiDS; inside BS's cap σ₈ is 0.03–0.32) and L1's native run | via L1 | HEAVY |
| 36 | Native shear rerun (CFG960) | C3 | OPEN | OLD-MODEL ONLY | The SCT-M engine, not v3. Since the board was drawn: SC1x **FAILS, KiDS EXCLUDED, Δχ² +47.28** (89fbefe1c0); SC2x not run (owner decision). v3 counterpart: L1 | none; record as retired-model result | — |
| 37 | Native CMB (patched CLASS) | C3 | OPEN | STALE | C7's patch is AeST (v4); C2 and F3 K0c ran only the dust limit μ_K → ∞. v3 at finite μ_K (J′(0) = −1: no Newtonian term on FRW for k > aμ_K) has not been computed | yes: a Khronon-v3 CLASS patch → TT/EE/φφ, P(k) (R7) | SMALL compute (code effort) |
| 38 | CMB lensing (Planck PR4) | C3 | UNDEC | OLD-MODEL ONLY | theory-v2 runs (NC1x/T1x/T2x) against their control. v3 counterpart: C_L^φφ from the v3 CLASS patch, scored by CFG917 Part A | via R7 | SMALL |
| 39 | Growth, zero-knob supply rule | C3 | FAIL | OLD-MODEL ONLY | the settling engine (F3, G1). v3 counterpart: tile 40 | none; remove (also from `MUST_STAY_RED`) | — |
| 40 | Linear growth, v3 Khronon | C3 | FAIL | CURRENT | F3 is v3 | none (L1 decides the nonlinear escape) | — |
| 41 | Linear growth, v4 AeST | C3 | FAIL | OLD-MODEL ONLY | v4 | none; remove (also from `MUST_STAY_RED`) | — |
| 42 | Structure growth, chassis alone | C3 | FAIL | OLD-MODEL ONLY | L341: C-H/K chassis with an unfloored ν boost on all matter. v3 counterpart: tile 40 | none; remove | — |
| 43 | ALMA U4 (6 Nov), GS4 (28 Nov) | C3 | OPEN | DATA-GATED / OPEN | The governing plan uses ν_mono (owner decision 10-20, CFG806/809). v3's kernel ν₁ is sealed separately as AG4e (9802de0d). All three seals are algebraic-disc predictions; the AQUAL in-plane correction is not applied | owner: name AG4e (n = 1) as the v3 reading; sealed AQUAL-disc addendum before 2026-11-06 (R3) | SMALL |
| 44 | Gaia DR4 wide binaries (Dec) | C3 | OPEN | DATA-GATED / OPEN | The prediction is v3: C6 screened γ − 1 = 8.1e-6 at 24 pc; E2's AQUAL 1.167 / 1.199 is the unscreened contrast. D2 (QUMOND) is superseded | none | — |
| 45 | Gaia DR4 MW predictions | C3 | OPEN | DATA-GATED / OPEN | Sealed 10-10 with ν_mono, the round rule (RM-v / RM-φ), the QUMOND PD and no EFE: not v3 | yes: a new dated v3 sealed file (AQUAL disc, ν₁) before 2026-12-02; never edit CFG553 (R3) | SMALL |
| 46 | The owner's wave a0(z) idea | C3 | OPEN | DATA-GATED / OPEN | An extension, not in v3 (it needs a new light scalar, CFG957). CFG956's bound is background-level | none | — |
| 47 | Why kappa = 1/2 | C4 | OPEN | DATA-GATED / OPEN | A theory question. The quoted 0.417 ± 0.095 (CFG493) combines routes run with ν_mono and algebraic laws; the law's definition moves fitted a₀ by up to 0.05 dex (CFG516), against a 0.099 dex error | re-fit with ν₁ + AQUAL discs (R3) | SMALL |
| 48 | Stiffness length L* | C4 | OPEN | DATA-GATED / OPEN | C3 and D10 are v3 (computation current) | none | — |
| 49 | What sets the cold-mass amount | C4 | OPEN | DATA-GATED / OPEN | C2 and C4 are v3 (dust abundance = initial condition); CFG886 is background-only | none | — |
| 50 | Ownership from an action | C4 | OPEN | OLD-MODEL ONLY | the label sector (tether, LDT, SCT: CFG945/950/953). v3 has no ownership and needs none (the law acts on all baryons, with an EFE) | none; remove | — |
| 51 | Law + a^1 growth + no EFE, local | C4 | FAIL | CURRENT | F3 restates the no-go for v3: v3 pays the no-EFE leg with an EFE, and the growth leg is inherited (empty μ_K window). CFG946's theorem does not depend on the model. The note cites v4 / H1: re-annotate | none (re-annotate) | — |
| 52 | Physical parent of the shear engine | C4 | OPEN | OLD-MODEL ONLY | the parent of the theory-v2 engine; v3 is not its parent (CFG941, CFG947) | none; remove | — |
| 53 | Energy books of settling | C4 | OPEN | OLD-MODEL ONLY | v3 has no settling | none; remove | — |
| 54 | Radiative stability (G12) | C4 | COND | STALE | Computed on the filtered C-H/K chassis (α_c / c_2 window, ν_mono heat filter). v3 also has a preferred foliation, so its Lorentz-violation leakage bound must be redone with v3's couplings | yes (R5) | SMALL |
| 55 | Covariant completion | C4 | FAIL | CURRENT | The I1 / C7 / F3 trilemma. Its one open escape is the native nonlinear v3 run | via L1 | HEAVY |

## Recompute batches to launch

Shared rules for every batch:
- Frozen criteria are committed alone first.
- Change one ingredient at a time and report how the statistic moves with each: kernel → geometry (AQUAL) → EFE → native
  screening → μ_K² term.
- Both footings, never pooled. Run with `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, no downloads, `--mutate`.
- A fail is checked as hard as a pass.

**R1 — v3 small systems in their host's field (SMALL; about 1 h on one thread). Tiles 19, 26, 29; feeds 31.**
- Model: v3's static equation (AQUAL μ = x/(1+x) + γ_L stiffness at L★ = 21.7 / 22.9, 24, 90 pc) for each system as a
  Plummer or exponential sphere in a uniform host field. No ownership, capture or supply.
- Solvers: `doors_push_2026_10_22/D10_native_Lstar/d10_solver.py` (stiffened AQUAL in a host field),
  `rebuild_2026_10_22/F2_outer_lensing/f2_aqual.py`, `doors_push_2026_10_22/E2_field_equation/aqual_axi.py`.
- Inputs:
  - satellites: `doors_push_2026_10_22/E3_dwarf_excess/e3_per_system.csv` (host masses as E3: MW 6e10, M31 1e11);
  - TDGs and DF2/DF4 with their hosts: `campaign_fresh_gravity/CFG936_below_law_systems/cfg936.py`;
  - Coma UDGs and the Coma field: `campaign_fresh_gravity/CFG933_udg_sealed_test/cfg933.py` and
    `CFG948_nocapture_vs_udgs/cfg948.py`.
- Reproduce E3's +0.89 dex and CFG936's TDG offsets first.

**R2 — v3 galaxy–galaxy lensing at low g (SMALL; minutes). Tiles 17, 30; feeds 31.**
- `rebuild_2026_10_22/F2_outer_lensing/f2_outer_lensing.py` and `f2_aqual.py` (Model T: AQUAL, y_e grid
  0 / primary / maxclu, inventory baryons + hot CGM).
- `campaign_fresh_gravity/CFG829_lensing_low_g_vs_dwarf_excess/cfg829.py` (B21 window and the A estimator).
- `CFG840_cfg829_robustness/cfg840.py` (variants) and `CFG926_small_reframings_B/cfg926.py` R5 (IMF α–σ).
- Output: blue, red and all-lens A in the dwarfs' g_bar window, on both footings, at each y_e.

**R3 — v3 discs: AQUAL with ν₁ (SMALL; the SPARC set may take 1–2 h on one thread). Tiles 15, 24 (v3 counterpart), 25, 43,
45, 47; optionally 16.**
- Solver: `doors_push_2026_10_22/E2_field_equation/aqual_axi.py` (validated against BN11 to 1.1 %).
- Milky Way:
  - `campaign_fresh_gravity/CFG514_directional_milky_way/cfg514_directional.py` (McMillan17 baryons, Bovy–Rix K_z);
  - `CFG516_round_cold_energy/cfg516_mw.py` and `cfg516_sparc.py`: swap PD (QUMOND) for AQUAL and ν_mono for ν₁, and drop
    RM;
  - `CFG532_mw_gaia_rotation_curves/cfg532_mw_curves.py`, `cfg532b_more_curves.py` and
    `CFG533_mw_exceptionalism/cfg533_mw_exceptionalism.py`.
- SPARC loader: `CFG695_saturating_vacuum/cfg695.py`.
- κ re-fit: `CFG493_kappa_combined/cfg493_kappa_combined.py`.
- `CFG553_sealed_gaia_dr4_predictions/cfg553_predict.py` is a template only. Write a **new dated sealed file** before
  2026-12-02.
- ALMA: `argon_push/AG4e_n1_alma_seal/ag4e.py`, as a sealed AQUAL-disc **addendum** before 2026-11-06. Never edit
  `SEALED_N1.json`.

**R4 — kernel-only swaps, verdict-safe (SMALL; minutes; lowest priority). Tiles 22, 23, 33, 34.**
- `campaign_fresh_gravity/CFG528_sluggs_centrals_mechanism/cfg528b_measured_tracers.py` (and `cfg528_mechanism.py`) with
  ν₁ and no R-own / edge / round options.
- `CFG540_vizier2026_bfjr_mhongoose/cfg540_bfjr.py` with no edge and ν₁ (it should reproduce CFG543's no-edge row).
- `CFG303_lcdm_free_inputs/cfg303_*_LCDMFREE.py`, `CFG307_aless122_stress_test/cfg307_stress.py` and
  `CFG308_cristal_stress_test/cfg308_cristal_stress.py` with ν₁.

**R5 — v3 relativistic sector (SMALL, sympy; the slowly-moving-BH marching may take hours on one thread). Tiles 10, 14,
54; optionally 6.**
- v3 action: `covariant_push_2026_10_22/C4_khronon_parent/c4_khronon_parent.py`, `C5_health/c5_health.py`, and C8's leaf
  functional.
- BS PN system: `real_research/bs_khronon_2026/BSK1_moving_source_gate.py`.
- Templates:
  - `real_research/extra_crispy_2026/XC1_strong_coupling_chk.py` and `XC3_filter_foliation_vertices.py`;
  - `campaign_fresh_gravity/CFG318_strong_field_bh/cfg318_strong_field_bh.py`;
  - `CFG319_moving_black_hole/cfg319_moving_bh.py` + `cfg319_lib.py`;
  - `CFG320_radiative_stability_g12/cfg320_radiative_stability.py`.

**R6 — v3's static μ_K² term beyond 0.1 Mpc (SMALL; minutes). Tiles 28, 18; feeds 31.**
- Solve ∇·[μ(|∇ψ|/a₀)∇ψ] + μ_K²ψ = 4πGρ_b (BS24 Eq. 35; L1 §1) in spherical symmetry.
  - Objects: F1's 326 clusters and F2's isolated-lens stack.
  - μ_K values: (0, 14.8 h/Mpc] (BS cap) and F3's growth-needed 361–2542 h/Mpc.
  - Zero point per H2's convention.
- Reuse `rebuild_2026_10_22/H2_aest_clusters/h2_aest_clusters.py` (the same structure in its AeST form),
  `F1_cluster_cores/f1_cluster_cores.py` (`f1_meas.pkl`) and `F2_outer_lensing/f2_outer_lensing.py`.

**R7 — v3 linear Boltzmann (SMALL compute, mostly code). Tiles 37, 38 (v3 counterpart); cross-checks 40.**
- Write a Khronon-v3 CLASS patch: J_x with J′(0) = −1, and BS K(Q) dust with μ_K.
- Templates: `covariant_push_2026_10_22/C7_aest_class/c7_make_patch.py`, `c7_derive.py`, `c7_validate.py`. Equations:
  `rebuild_2026_10_22/F3_growth_audit/f3_growth_audit.py` (K1, K2) and `real_research/bs_khronon_2026/BSK2_frw_dust_sigma8.py`.
- μ_K values: 14.8, 361, 2542 h/Mpc and ∞.
- Scoring: TT/EE as C2 did, and C_L^φφ with `campaign_fresh_gravity/CFG917_cmb_lensing_gate/cfg917_cmb_lensing.py`
  Part A.
- a₀ does not enter at linear order, so the footings give identical numbers here. Say so rather than pooling.

**HEAVY — L1 production (after the running 1024³ job). Tiles 13, 27, 35, 36, 39, 42 (v3 counterparts) and 55's open
escape.**
- `rebuild_2026_10_22/L1_khronon_pm/FROZEN_CRITERIA.md`: the frozen 512³ plan (μ_K 14.8 and 400, both footings, CFG592/596
  KiDS scorer against S0), after its 32³–128³ validation gates.
- It is the only v3 test of nonlinear growth and shear. CFG960's slot should not be reused for an older engine.

## Board edits implied (no computation)

- **Remove, or move to a dated "retired models" strip, the 16 OLD-MODEL ONLY tiles** (rows 5, 6, 12, 13, 21, 24, 27, 35, 36,
  38, 39, 41, 42, 50, 52, 53). Each one's v3 counterpart is named in the table.
  - Three of them are in `MUST_STAY_RED`: "Growth, zero-knob supply rule", "Linear growth, v4 AeST" and "v4 well-posedness".
    The generator's list has to be edited with that reason.
  - v3 counterparts that are not yet tiles and should be added once computed: "MW vertical force, AQUAL disc" (R3) and
    "CMB lensing, v3 linear" (R7).
- **Re-annotate these CURRENT tiles:**
  - 2: drop H3.
  - 7: drop CFG291 and CFG311.
  - 8: disclose C6's frozen UNDECIDED.
  - 9: drop D7c.
  - 11: cite C4.
  - 28: 326 clusters; drop H2.
  - 51: drop v4 / H1.
- **Relabel tile 23** to CFG543's no-edge row.
- **Header:** replace "Khronon (v3, fails growth) or AeST (v4, ill-posed off symmetry)" with the recipe below. Keep "The
  theory is incomplete".

## Proposed "crispiest recipe" (board subtitle; 39 words)

> General relativity plus a preferred cosmic time (Khronon) and one extra field giving the simple MOND law (AQUAL,
> external-field effect included, κ fitted), switched off within L★ ≥ 22 pc, plus fitted cold dust; no settling or supply
> rules.
