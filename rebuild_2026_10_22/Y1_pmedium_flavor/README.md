# Y1_pmedium_flavor — the P-medium flavor scored on the board tiles

## Verdict: CRISP FINDING. P-medium fixes v3's growth failure, but it has no galaxy law and no gravitational-wave sector

**The recipe in two lines.**
- Newtonian gravity acts on all matter: ∇²Φ = 4πG(δρ_b + δρ_c). Baryons feel Φ only.
- The cold collisionless medium also feels h = e/χ.
  - e = δρ_c − ∇·P is the mismatch between the cold density and the divergence of a saturating polarization P (W = −|P| − ln(1−|P|)).
  - χ is a stiffening scalar, with potential α(χ−1)²/2 and gradient term d|∇χ|²/2.
- Preferred frame, imposed EdS background.

**The action scored.** Codex's XP-20261023 reduced action (`sol61_push/expanding_polarization_2026_10_23/DERIVATION.md`)
and its 3D form SE-20261023 (`sol61_push/spatial_expansion_2026_10_23/DERIVATION.md`). The sha256 of every source is in
ASSUMPTION_LEDGER.md. The parameters:

| parameter | value | source |
|---|---|---|
| η (inertia of P) | .005 | prescribed: `radiating_collapse_2026_10_22/CONTRACT.md` L8 |
| α | .005 | prescribed: `cooling_assembly_2026_10_23/CONTRACT.md` L4 (λ = 100) |
| b, d | .125 | prescribed: same file and line |
| ℓ₀ | 0.440422 kpc | **FITTED to a growth criterion**: `parent_compliance_2026_10_22/RESULT.md` L82–L85. The galaxy law needs ≥ 134 / 140 kpc |
| a₀ | units only | κ = ½ FITTED; canonical 9.3603e-11, alt 1.1312e-10 m/s² |
| background | EdS, H₀ 67.4, Ω_m .315, f_b 1/6.364 | ΛCDM-processed |

Footings are never pooled. This is not "theory closed". Nothing here says the data favour the framework.

| board tile | P-medium verdict | key numbers (canonical / alt) | evidence |
|---|---|---|---|
| Gravity waves at light speed | **NOT COMPUTABLE** | The action has no tensor sector: gravity is instantaneous Poisson. In a minimal-coupling completion the (P, χ) stress is zero on the vacuum and FRW mean, so c_T = c there. That is reported, not scored | `.out` L5–L7; §1 |
| Binary pulsars + GW170817 | **NOT COMPUTABLE** | Same reason. Baryons do not enter the P or χ equations, so there is no dipole channel | `.out` L6; §1 |
| Health: ghosts, gradients | **PASS** (reduced action) | Max growth rate / √(4πG(ρ_c+ρ_b)) = 1.000000 over 2000 backgrounds × k = 1 … 1e8. That is the Jeans rate exactly, so there is no faster mode. Fast P speed √((ρ_c+1/η)/χ) (504 km/s at ρ_c = 0); χ waves 35.7 km/s | `.out` L10–L12; §2 |
| Leaf problem well-posed | **PASS** (reduced action) | FRW modes are damped: retained amplitude 0.999995 / 0.9995 / 0.9518 / 0.673 / 0.278 at k = 0.01 / 0.1 / 1 / 3 / 10 Mpc⁻¹, never above dust. WT-02's FRW ill-posedness is absent. Scope: no covariant completion; the mean-density subtraction is global | `.out` L13–L14; §2 |
| Rotation curves (SPARC RAR) | **NOT COMPUTABLE** (no law); its only history-free branch **FAILS** | The RAR is Newtonian gravity of baryons plus the cold medium, so it depends on how the cold matter is distributed. The zero-dispersion branch scores rms **0.242 / 0.241 dex** with median Υ **1.20** (pinned at the edge), against the line ≤ 0.110 and Υ in 0.50–0.80. The AQUAL law on the same points gives 0.048 | `.out` L17–L34; §3 |
| Solar system + Cassini | **CONDITIONAL** | Ambient cold medium: worst gate ratio 7.4e-4 (ρ = 0.1 M☉/pc³). A zero-dispersion cold atmosphere bound to the Sun would fail: mass inside Saturn **2.2e4 / 2.6e4×** the bound, sunward pull 2557 / 3091×. Conservative dynamics cannot capture one beyond 0.18 AU | `.out` L36–L41; §4 |
| Tidal dwarfs, NGC 1052-DF2/DF4 | **CONDITIONAL** | The TDGs are derived cold-free: Newton gives **+0.055 ± 0.114 dex** (PASS). DF2/DF4 under Newton sit at +0.30 ± 0.73 and −0.24 ± 0.79 ln, but being cold-free is a formation history for them | `.out` L44–L50; §5 |
| Dwarf satellites (MW / M31) | **NOT COMPUTABLE** | Cold-free (Newton): **+2.00 / +1.99 dex** (fails). Cold cores can bind inside a host here: 42/42 needed zero-dispersion cores fit inside their Jacobi radii. Unlike v3's T3, cold matter has weight. But the core masses (1e6–4e8 M☉) are free, one per system | `.out` L47–L50; §5 |
| Cluster cores | **NOT COMPUTABLE** | There is no static cluster prediction that is independent of the cold distribution. Cold-free Newton gives A_MID 9.8 (F1) | `.out` L53; §6 |
| Linear growth | **PASS** | σ8 / dust limit **0.9991** (from a = 1e-3) and **0.967** (from 1e-4), on both F3 backgrounds. Codex's EdS table is reproduced to 4e-10 | `.out` L62–L68; §7 |

**Overall reading.** No: P-medium does not fix v3's structural failures without losing v3's passes.
- **What it fixes.** It turns v3's growth FAIL into a PASS.
- **What it avoids.** It avoids v3's weightless-dust obstruction for satellites.
- **What it gives up.** It gives up the galaxy law itself:
  - at the fitted ℓ₀ = 0.44 kpc, the medium is a cored, self-interacting cold component;
  - the RAR, MeerKAT a₀ and group (BFJR) passes of v3 are no longer predictions (the last two by the same argument, not recomputed);
  - the GW-speed and binary-pulsar passes become not computable.
- This is the growth side of the record's D-T dichotomy (CFG941). A finite tether gives a¹ growth and no external-field effect (EFE), but no law. So "law + a¹ growth + no EFE, local" stays FAIL.

## 1. Gravity waves and binary pulsars (Y-T1)

- **The fields.** The action's fields are the particle positions, P, χ and Φ. Φ obeys an instantaneous Poisson equation. There is no h_ij, and the minisuperspace adds only a(t). So c_T is not defined in this action: NOT COMPUTABLE.
- **What is missing.** A metric sector, or a covariant completion.
- **Reported, no class weight (K1, sympy).**
  - The field energy W + e²/(2χ) + α(χ−1)²/2 and its first derivatives vanish at P = 0, χ = 1, e = 0. A completion with GR plus these fields, minimally coupled and with no aether kinetic term, therefore propagates tensor modes at c on the vacuum and on the FRW mean.
  - ∂e/∂ρ_b = 0, so baryonic binaries source no P or χ radiation.
- **CFG938's c_T ≠ c (WT-02, CFG961).** That result came from CFG938's covariant parent (a Christoffel² term with L★). It does not transfer: this action has no such parent.

## 2. Health and well-posedness (Y-T2)

**The derivation (exact, frozen coefficients, any admissible background).**
- The quadratic energy is gravity plus a positive semidefinite rest:
  - W is convex for |P| < 1 (Hessian W″ = 1/(1−p)², W′/p = 1/(1−p));
  - e²/(2χ) is jointly convex in (e, χ) for χ > 0;
  - α and d k² are positive.
- The kinetic matrix diag(ρ_c, ρ_b, η, b) is positive, since ρ_c ≥ 0 for particles.
- Gravity contributes −|ρ_cξ_c + ρ_bξ_b|²/4. By Cauchy–Schwarz, ω² ≥ −4πG(ρ_c + ρ_b). Every mode grows at most at the local Jeans rate, at every k: there are no ghosts and no gradient or Hadamard instability.
- K2 confirms this in 60-digit arithmetic: max Γ/√(ρ_c+ρ_b) = 1 over 2000 random backgrounds, with ρ up to 1e4, |P| up to .985, χ from 0.1 to 1e3, |e| up to 1e3 and k up to 1e8.

**Principal part (K3).** The fast P mode has c² = (ρ_c + 1/η)/χ and the χ mode has c² = d/b, matching to rounding. The transverse P has no gradient term; it is an ODE, which is harmless.

**FRW (K4).**
- The action supplies the 2H (matter) and 3H (field) friction itself.
- The linear modes never outgrow dust, and the retained amplitude falls monotonically with k.
- WT-02's defect (a forward-parabolic χ with a backward-parabolic multiplier) needs a multiplier and a first-order χ; this action has neither.
- H4's saddle maps do not apply: no fluid here has a sign-indefinite density, and e enters only squared.

**Not covered.**
- Relativistic constraints and causality: Φ is instantaneous.
- The cold reference density is a global slice average, i.e. non-local (XP AUDIT item 7).
- The P speed exceeds c only if ρ_c/χ > 8.6e6 M☉/pc³ (canonical).

## 3. Static galaxy limit and the RAR (Y-T3)

**Baryons feel Φ only, and ∇²Φ = 4πG(ρ_b + δρ_c) is linear.**
- The RAR is therefore the Newtonian field of the baryons plus the cold medium.
- P and χ never act on baryons. They only decide where the cold matter sits.
- Any collisionless distribution function in equilibrium in Φ + h is a static solution. So the RAR depends on the cold matter's history: **NOT COMPUTABLE as a prediction**.

**The only history-free static state** is the zero-dispersion (T = 0), non-rotating cold medium.
- On its support Φ + h = μ_c, so P/(1−|P|) = ∇Φ and |P| = g/(g+a₀) (K5).
- The field equation becomes ∇·[μ(|∇Φ|/a₀)∇Φ] = 4πGρ_b + χ(μ_c − Φ)/ℓ₀², with μ = x/(1+x).
- This is AQUAL plus a term that the tether's finiteness forces. The AQUAL law holds only where that term is negligible, i.e. on scales ≪ ℓ₀/√χ ≤ ℓ₀ = 0.44 kpc. The minimum principle gives χ ≥ 1.
- The record's benchmark needs ℓ ≥ 134 / 140 kpc for the law (parent_compliance L84–L85). χ ≥ 1 rules this out in this action.

**Two bounds (README derivation; K7 confirms both numerically).**
- (i) h > 0 only within r₁ ≤ πℓ₀. This is reciprocal_field's theorem: it needs χ ≥ 1 and no P-gradient term, and both hold here.
- (ii) Beyond r₁, keeping ρ_c ≥ 0 requires ∫_{r₁}^r s²|h| ds ≤ r²|P| < r², with |h(s)| ≥ ∫_{r₁}^s g_N,b. The support must therefore end by R_s, computed per galaxy at Υ = 0.30 and r₁ = πℓ₀ (the most generous choice). Outside R_s the field is exactly Newtonian with a compact cold mass M_c.
- K7: a nonlinear spherical solver (χ by a Yukawa Green's function, Anderson-mixed, converged < 1e-8) on NGC 3198, DDO 154 and NGC 2841 at four central amplitudes. In all 12 cases r₁ ≤ πℓ₀, and the support ends at 0.74–1.72 ℓ₀, well inside R_s (4.4–13.4 ℓ₀).

**Scored with P4's statistic** on the points beyond R_s (R_s median 3.1 / 3.2 kpc), with Υ and M_c ≥ 0 free per galaxy.
- The rms is 0.2420 / 0.2414 dex (N 145 / 140) and the median Υ is 1.20. That **FAILS** the line on both footings.
- A point mass cannot make a flat curve: the fit is the cold-free Newtonian one (median M_c 7.5e5 M☉).
- K6 confirms the data read: it reproduces P4's AQUAL per-galaxy-Υ rms, 0.05409 / 0.05372, exactly.

## 4. Solar System (Y-T4; gates from CFG3: M(<Saturn) < 6.7e-11 M☉, 3.66e-14 m/s² at 1 AU, Q₂ < 9.0e-27 s⁻²)

- **S-a: ambient collisionless medium.** ρ_loc is 0.013 or 0.1 M☉/pc³, with σ ≥ 100 km/s focusing.
  - Worst ratios: 6.4e-4 for M(<Saturn), 9.8e-6 at 1 AU, 7.4e-4 for Q₂ (a full-anisotropy bound).
  - There is no external-field quadrupole, because the baryon equation is linear.
- **S-b: a T = 0 cold atmosphere bound to the Sun and reaching Saturn.** This is a static solution of the action.
  - P saturates into a hedgehog, so the cold mass is ≥ (a₀r²/G)(1 − a₀/g_N). The solver gives the same 1.449e-6 M☉ (K8).
  - That is 2.2e4 / 2.6e4 × the Saturn bound, and 2557 / 3091 × the 1 AU bound: it fails.
  - Conservative dynamics cannot assemble S-b from a stream with v_rel ≥ 100 km/s beyond 0.18 AU (V_esc = v_rel).
  - Field radiation is the only dissipation channel, and its capture rate is not computed.
- Frozen rule: **CONDITIONAL**.

## 5. TDGs, DF2/DF4 and hosted satellites (Y-T5)

**Equation check before reuse.** In this action a cold-free system is exactly Newtonian, which is U1's B0 branch. K9 reproduces B0 from the raw inputs: TDGs +0.0547 ± 0.1144, DF2 / DF4 +0.296 / −0.239 ln.

**TDGs: PASS.**
- Their V_esc is 23–64 km/s, while the host's cold medium moves at ≥ 100 km/s or, in the T = 0 branch, sits in the host's central core.
- So they cannot capture cold matter. B0 is within 2 se (χ² 1.17 / 6).

**DF2/DF4: B0 passes,** but the cold matter here has weight, so a cold-free DF2/DF4 needs a formation history. The tile is therefore **CONDITIONAL**.

**Satellites.**
- **Cold-free:** +2.001 / +1.987 dex above Newton (S1 statistic; K10 matches U1 B0). That fails.
- **Contrast with U1's T3.** Here cold matter feels Φ + h, so it is not weightless, and hosted cores can bind.
- **Zero-dispersion cores.** For each S1 satellite I took the pure-cold T = 0 core that gives its g_obs at r₁/₂.
  - Those cores have support radii of 0.24–0.78 kpc and masses of 6.6e5–4.5e8 M☉.
  - All 42 that exist fit inside their Jacobi radii (0.7–7.7 kpc; canonical ranges quoted, alt the same count).
  - Crater II (r₁/₂ = 1.41 kpc) is larger than any T = 0 core (0.78 kpc max). Boötes III and And XVII (plus And XV on alt) fall outside the family's g range.
- The core masses are not derived (W1: no certified core forms), so the tile is **NOT COMPUTABLE**. Binding itself is allowed.

## 6. Cluster cores (Y-T6)

There is no static prediction independent of the cold distribution. The T = 0 support ends within kpc (§3), so at 0.1–3 Mpc that branch is just a point mass. Cold-free Newton gives A_MID 9.8 ± 0.6 (F1 README L46–L47). **NOT COMPUTABLE.**

## 7. Linear growth (Y-T7)

- **K11.** My own integrator of XP's one-mode equations reproduces Codex's six `growth/result.json` values to 3.6e-10. At k = 1 Mpc⁻¹ the values are 0.95176 / 0.96153 / 0.95397.
- **K12 (sympy).** XP's quasi-static limit (η → 0, χ = 1) gives cold self-gravity S = 1/(1+(kℓ₀/a)²). That is exactly F3's BSK2 kernel at μ = 1/ℓ₀, so F3's machinery applies.
- **K13.** My implementation reproduces F3 K4 (0.9927 / 0.8609 vs 0.993 / 0.861).
- **σ8 / dust limit:** 0.9991 (from a = 1e-3) and 0.9670 / 0.9672 (from 1e-4) on backgrounds A / B. Both are ≥ 0.95, so **PASS**.
- **Finite inertia** changes the k = 1 EdS value by −0.4 % to +0.6 % against quasi-static. The footings differ by ≤ 0.04 %.
- **Flag, not scored.** The small-scale transfer T(k = 1, 3, 10, 30 h/Mpc) is 0.98 / 0.89 / 0.62 / 0.39 from a = 1e-3, and 0.74 / 0.51 / 0.32 / 0.20 from 1e-4.
  - That is a cutoff like warm dark matter's, at k ~ 1–6 h/Mpc.
  - The Lyman-α forest is the test it must face; no frozen line here.
- **Inputs.** The background (Λ, abundance, A_s) is the ΛCDM-processed input, as for F3's ΛCDM row. The flavor's minisuperspace allows a ρ_Λ but does not derive it.

## Re-checks of the record (ASSUMPTION_LEDGER §D)

| record statement | about this action |
|---|---|
| CFG938/CFG941 D-T: the tethered medium has no linear self-gravity | Does not transfer. The tether is finite here (e²/(2χ)), giving S = 1/(1+(kℓ₀/a)²) and full growth at k ≪ a/ℓ₀. The price is the law (§3) |
| WT-02 / CFG961: ill-posed on FRW; c_T ≠ c | Ill-posedness absent: χ is second order and there is no multiplier (K2, K4). c_T is not defined: there is no metric sector |
| CFG939 no-capture (v_rel > V_esc) | Applies: the action is conservative. Used in §4 and §5 |
| reciprocal_field R ≤ πℓ₀ | Holds here (χ ≥ 1, no P-gradient term). K7 confirms it, together with the new support-end bound |
| parent_compliance "no overlap" (law ≥ 134 kpc, growth ≤ 0.44 kpc) | Confirmed and sharpened: χ ≥ 1 caps the effective tether length at ℓ₀ |
| H4 saddle ill-posedness | Not applicable: there is no sign-indefinite fluid density |
| U1 T3 weightless dust | Not applicable: cold matter has weight here, so hosted cores can bind |

## Checks, MUTATE, compute, files

- **Main run.** `y1_pmedium_flavor.py`: **14/14 PASS**, exit 0, about 6 min, peak 0.48 GB, one thread at nice 15. Every number above is in `y1_pmedium_flavor_results.json`; the output is `y1_pmedium_flavor.out`.
- **`--mutate`** plants three defects:
  - M1: d → −d;
  - M2: the e²/(2χ) term removed (the exact tether, i.e. the law);
  - M3: the h-force removed from growth.

  Results are in `*_MUTATE.out` and `*_results_MUTATE.json`. **MUTATE: 10/14, exit 1.** K2 fails under M1 (growth rate ∝ k, max Γ/Jeans 5.7e10). K7 fails under M2 (0/12: the support never ends). K11 and K13 fail under M3 (Codex's table off by 0.048; F3 K4 gives 1.000).
- **ENQUEUE.** None needed: every computation here takes minutes. A core-population or Lyman-α test would need its own lane.
- **Commits.** Frozen criteria and ledger first, alone (00b0e13d0b); then this README, the script and the outputs. Nothing in `sol61_push/` or `explainers/` was edited.
