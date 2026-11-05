# CQ2_v3s_dr4_seal: FROZEN CRITERIA (2026-11-04)

Committed alone, before any script or number of this lane. κ = ½ FITTED; not theory closed. Footings
9.3603e-11 / 1.1312e-10 m/s², never pooled. No particle, no separate cold sector. Nothing here says the data favour the
framework.

## Question

What does v3s, the record's current theory (`covariant_push_2026_10_22/V3_FULL_PICTURE.md`: the khronon plus the switched
stiffness −(γ_L/2)[max(D·P, 0)]², γ_L = K L★²/2, L★ ≥ 21.682 / 22.849 pc after X3's switched re-solve), predict for
Gaia DR4 wide binaries? Seal the prediction, pushed through the frozen DR4 pipeline, before DR4 (due about 2026-12-02).

## Not blind: what the record already says

- C6 (`covariant_push_2026_10_22/C6_literal_cassini`), C3 K7 and C6P: a 1.5 M☉ binary at 20 kAU has γ_v − 1 = 8.1e-6 /
  1.9e-6 / 5.8e-7 at L★ = 24 / 50 / 90 pc on both footings (γ_v = √γ_r, Route F monopole in a uniform Galactic field). This
  was computed for v3 (the unswitched form) and never pushed through the DR4 pipeline.
- X3 D2 (`rebuild_2026_10_22/X3_switched_stiffness`): the Galactic phantom keeps D·P > 0 within 1 kpc of the Sun (minimum
  +0.0055 / +0.0062 M☉/pc³ over R 7.2–9.2 kpc, |z| ≤ 1 kpc); a 1 M☉ point mass's own negative lobes are ≤ 3.1e-7 M☉/pc³
  deep; margin ≥ 1.8e4; "the wide binary is unchanged exactly".
- V3S_FINAL_VERDICT: "both predict Newtonian wide binaries (v3s is screened)". X15: at β = 0 (v3s) a source moving
  through the khronon frame does not carry its hedgehog; the linear solution is GR with the bare G.
- Grep for "wide binar" in V3W and V3X: no hits. O1: velocity-screened reading also Newtonian.
- CW1 (`cw_lanes_2026_11_04/CW1_wide_binary_seal_dr4`, e7672a30e1): Newton and plain QUMOND (Newtonian Galactic field
  in ν) give DR3 Q_pred −0.0010 / +0.0514 (canonical) and −0.0030 / +0.0542 (alt); the frozen pipeline returns γ_inf
  1.0019 / 1.1494 (canonical) and 1.0100 / 1.2081 (alt).

So the expectation is NEWTONIAN. This lane does not assume it: it re-derives the screened state from the static limit,
checks the switch and the Galactic field, computes γ_r(s) and pushes it through CW1's machinery.

## Derivation route (static limit)

1. **Static weak-field equations** (C6, the C4-literal form v3s uses, η = 0, β = 0; p = K P, Φ = ln N):
   (L) ∇²Φ = Kρ + ∇·p; (P_L) ∇Φ + (L★²/2)∇(∇·p) = a₀p/(a₀ − |p|) where D·P ≥ 0; where D·P < 0 the switch removes the
   stiffness term and (P_L) is AQUAL's.
2. **Switch state (does the Galactic field or the binary unscreen it?).** Lean `switched_agrees_where_screened`: v3s = v3
   pointwise wherever D·P ≥ 0. Total D·P = ρ_gal + ρ_1 + ρ_2. The response is linear in mass (step 3), so a binary of
   M_tot ≤ 2.5 M☉ has negative lobes at most 2.5× a 1 M☉ point mass's. From X3's D2 json rows (read only): binary margin
   = min over rows of ρ_gal,min / (2.5 × max negative lobe). Near each star the response is the hedgehog's positive
   divergence. If the margin ≥ 10 the binaries (all within 250 pc of the Sun, inside X3's box) sit on the stiff side and
   v3s's static binary is exactly v3's.
3. **Linear response about the Galactic background.** With x_e = g_obs/a₀, J = diag(1+x_e, 1+x_e, (1+x_e)²) and C6's
   closed-form kernel χ(k, ĉ) = m/(1 − m + (kL★)²m/2), m = k̂·J⁻¹·k̂. Expansion parameter
   ε = (GM/L★²) / (a₀x_e/(1+x_e)), the hedgehog over the background p. The Newtonian field of the binary itself is
   cancelled in χ = Φ + (L★²/2)∇·p by the stiffness, so ε (not g_N/g_e) controls linearity.
4. **Relative acceleration.** The kernel is even in k̂, so a star has no self-force. Each star feels the other's
   monopole response, so the relative anomalous acceleration is Δa = routeF_radial(G M_tot, L★, x_e, r, r_F = 0)
   (C6's Route F monopole integral, copied, not imported), and γ_r(r) = 1 + Δa/(G M_tot/r²) = 1 + ρ²F(ρ; x_e), ρ = r/L★.
   This is independent of M_tot. Its analytic screened limit is F → 1, i.e. γ_r − 1 = (r/L★)² (the hedgehog GM/L★²,
   independent of a₀ and x_e). The anisotropic part is bounded with C6's recorded Q₂ (scaled by M_tot and L★⁻³) and
   reported, not injected. The μ_K term enters at ≤ 1e-14 (C3 K7's mass-term part, 2.4e-15) and is dropped.
5. **Motion.** Two readings, both sealed:
   - **V3S-REST** (primary, upper envelope): the static hedgehog at the L★ floor, at the primary field 1.9e-10 m/s²; the
     other fields (1.778e-10, 2.32e-10) reported as a range. Larger L★ only lowers γ_r − 1.
   - **V3S-MOVE** (X15): a binary moving through the khronon frame carries no hedgehog; γ_r ≡ 1, identical to Newton by
     construction (no computation).

## Machinery (copied from CW1, CW1's files untouched)

- DR3: KT21's Q estimator as in CW1 (`wide_binaries_dr3.csv`, K = 40 orbits per pair, seeds 2026110302 / 2026110402,
  σ_sys 0.020, bootstrap seeds 11 / 12). V3S's γ_r is the monopole at each orbit's 3D separation r3.
- DR4: `prep_2026/gaia_dr4_prep/wide_binary_pipeline.py` imported read only with `sys.dont_write_bytecode = True`, as
  CW1 does. Nothing in `prep_2026/gaia_dr4_prep/` is edited, run as a script, or hashed by this lane; CW1's recorded
  pipeline SHA-256 is quoted from cw1.json. CW1's exact random sequence is replayed (seed 20261216, 1,000,000 master,
  N_data 30,000, 4 realisations, the K6 injections, then per footing N, PQ, LOC3, LOC1, E55, HALF; the four forms this lane
  does not need are fitted with γ = 1 to consume the same draws). V3S is fitted on the same draws as N with a copy of the
  random state taken before N's fit (paired). The separation r for V3S is √(G M_obs/g_true); the 5 % mass noise moves
  γ_r − 1 by ≤ 10 % of itself.
- Separation labels as CW1: dQ / 0.020 and dγ_inf / 0.028; SEPARABLE if max ≥ 3, MARGINAL if ≥ 2, else NOT SEPARABLE;
  V3S vs plain (PQ) and V3S vs Newton (N), each footing.
- DR3 labels: z = (Q_obs − Q_pred)/σ; CONSISTENT |z| ≤ 2, TENSION ≤ 3, EXCLUDED > 3.

## Outputs

γ_r(s) for M_tot 0.5, 1.0, 1.5, 2.5 M☉ and s 1, 2, 3, 5, 7, 10, 15, 20, 30 kAU, both footings, three fields, at the L★
floor and at 24 / 50 / 90 pc; Route F numeric beside the analytic (s/L★)²; Q_pred and z for N, PQ, V3S-REST; γ_inf for N,
PQ, V3S-REST (mean, spread, paired Δ to N); labels. Files: `cq2.py`, `cq2.out`, `cq2.json`, `cq2_MUTATE.*`,
`cq2_seal.py`, `SEALED_PREDICTION.md`, `SEALED_PREDICTION.sha256`, `README.md`.

## Checks (frozen lines)

- **K1** Route F copy reproduces C6's 24 recorded wide-binary γ_v − 1 (1.5 M☉, 20 kAU, L★ 24/50/90, E0–E3 from D7b's
  json, C6's a₀ 9.36e-11 / 1.13e-10), max relative ≤ 1e-6.
- **K2** DR3: CW1's Q_obs, σ, Q_pred(N) and Q_pred(PQ) at 1.9e-10 reproduced, both footings, max abs ≤ 1e-9.
- **K3** Pipeline: CW1's K6 recoveries and every realisation's γ_inf for N and PQ reproduced, both footings, max abs ≤ 1e-9.
- **K4** Switch: binary margin (step 2) ≥ 10 in every X3 D2 row, and X3's near-zone minimum > 0.
- **K5** Linearity: ε ≤ 1e-4 for M_tot = 2.5 M☉ at the L★ floor and every field, both footings.
- **K6** Screened limit: |F − 1| ≤ 0.05 on the sealed (M, s) grid at the floor, every field, both footings.
- **K7** Convergence: Route F with n_c 96, upper k 800/ρ and 400,000 k-points moves γ_r − 1 by ≤ 1e-3 relative at
  s = 1 and 30 kAU, both footings; the log-ρ table interpolation matches direct evaluation at 5 off-grid ρ to ≤ 1e-4
  relative.

## Verdict rule (per footing, then combined)

- **SCREENED** iff K4 and K5 pass.
- **NEWTONIAN** iff SCREENED and max γ_r − 1 on the sealed grid ≤ 1e-3, |Q(V3S) − Q(N)| ≤ 1e-3 and paired
  |γ_inf(V3S) − γ_inf(N)| ≤ 1e-3. Otherwise SCREENED, DR4-VISIBLE RESIDUAL (numbers given).
- **SCREENING LIFTED** if K4 fails: the lane stops there and says where (no AQUAL solve here).
- Any of K1–K3, K6, K7 failing makes the headline UNDECIDED unless the failure is shown not to touch the sealed numbers.
- Headline first line of the README: `# CQ2_v3s_dr4_seal: <RESULT>`.

## MUTATE twin (`--mutate`, outputs `cq2_MUTATE.*`)

The switch inverted: −(γ_L/2)[min(D·P, 0)]². Around the binaries D·P > 0 (K4), so the stiffness never acts and the
binary sees the unscreened law. Stand-in: CW1's plain QUMOND curve (Newtonian field in ν, primary field, μ-dependent
table for DR3) replaces V3S's γ_r in the DR3 Q and the pipeline. It must bite: V3S vs Newton must become SEPARABLE and
the NEWTONIAN lines must fail, so the MUTATE run exits non-zero. If it still reads NEWTONIAN the machinery is blind and the
verdict is void.

## Compute

One thread (`OMP_NUM_THREADS=1` etc.), `nice -n 10`, `python3 -I -B`, under 1 GB physical memory (only two QUMOND
solvers, against CW1's thirty). Heavy queue not used.

## What this lane does not do

It does not re-grade v3s, edit any other lane, decide the khronon's rest frame, or add X15's β term (v3s has β = 0). The
sealed number is a prediction, not a result.

κ = ½ FITTED; not theory closed.
