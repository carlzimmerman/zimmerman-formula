# CFG690 — does deep-regime scale invariance fix astra's cubic, and is that symmetry independent of the law? (frozen criteria)

Block CFG690–699 (owner-approved for this chat, 2026-10-12). Written before any CFG690 script or number. Committed alone.
κ = ½ fitted; both footings (9.3603e-11 / 1.1312e-10), never pooled; the cold energy's mass is required; no particle species;
not theory closed.

## Why
CFG679 Part 2 scored astra's stable φ + P sector R0-SHAPED: its cubic β|P|³/3 is "a phenomenological assumption" chosen to give
the deep law. Part 2's rule says a form fixed by a symmetry can pass R0. Milgrom's deep-MOND scale invariance (SI: x, t → λx, λt
with masses fixed) is the obvious candidate symmetry. This lane asks whether SI forces the cubic and whether SI is independent of
the law. It also scores the static interpolation that astra's form gives on SPARC.

The sector is read only from `sol61_push/.../STABLE_SOURCED_RESPONSE.md` (astra's file, not edited): static energy
E = (a/2)|∇φ − P/a|² + W(|P|) + (γ/2)|∇P|² − α ρ_b φ, with W = β|P|³/3 in astra's choice. Total force (astra's asymptotics):
g = g_N + G_s M/r² + α p/a, G_s = α²/4πa, with G_s a_s = G a₀ matched.

## Tests

**T1 (sympy). SI uniqueness.** Under SI the deep-regime fields scale as φ → φ, P → P/λ, ρ_b → λ⁻³ρ_b (fixed mass), d³x → λ³d³x.
- (a) ∫W d³x is invariant for every λ iff W is homogeneous of degree 3 in |P|, i.e. W = c|P|³. Shown for W = |P|ⁿ (invariant
  iff n = 3) and for general W via λ³W(p/λ) = W(p) ⇒ W(p) = W(1)p³.
- (b) ∫αρ_bφ d³x is invariant. The quadratic term and the stiffness term scale as λ⁻¹, so they are irrelevant in the deep regime.
- PASS iff (a) and (b) hold symbolically.

**T2 (sympy). Is SI the law restated?**
- (a) For W = β|P|ⁿ/n with γ = 0 and a point source: V(r) is flat iff n = 3, and V⁴ ∝ M iff n = 3.
- (b) SI plus dimensional analysis: if deep dynamics depends on G and a₀ only through A₀ = G a₀, then V is a function of A₀M and
  r only. The only velocity is (A₀M)^{1/4}, independent of r. So SI ⇒ flat curves and V⁴ = k G M a₀.
- (c) The deep law g = √(G M a₀)/r is invariant under SI.
- **Reading rule (frozen).** If (a), (b) and (c) all hold, SI is equivalent to the deep law's content (flat curves + BTFR). Then the
  cubic scores **R0-SHAPED, REDUCED**: the free functional choice becomes one postulate, deep-regime SI, which is the deep law
  restated. R0 can PASS only if a committed source on the record derives SI, or the G-a₀-only-as-A₀ property, from something
  other than the deep law. Search done before this file: the repository's documents mentioning "scale invariance" (grep,
  2026-10-12) contain no such derivation. If (a)–(c) do not all hold, the lane reports which one fails and why.

**T3 (raw SPARC, data). The interpolation astra's form gives.** With γ = 0, eliminating p gives
g = (1 + G_s/G) g_N + √(a₀' g_N). Absorbing G_s into the locally measured G (the only consistent choice: the high-field force is
the measured Newtonian one) gives **ν_SI(y) = 1 + y^{-1/2}** at the framework's a₀ (the coefficient of the measured deep tail).
- Statistic: the CFG4 statistic exactly (SPARC 175, weights (V_obs/e_V)², Υ_bul = 1.4 Υ_disk, one global Υ_disk profiled on
  0.30–1.20 in steps of 0.01), computed by this lane's copy of CFG4's vectorised code.
- **PASS line:** CFG4 H2: rms ≤ 0.110 dex with Υ_disk in 0.50–0.80, on **both** footings. Otherwise FAIL.
- Label: "γ = 0 limit". Stiffness changes the interior below ℓ_γ (astra), so a FAIL here applies to the γ = 0 form only, and the
  lane says so.
- **Controls (load-bearing, exit 1 if any fails):** the copy reproduces CFG4's committed ν_mono rms and Υ (0.1003@0.61 canonical,
  0.0991@0.57 alt) and Newton rms 0.27548 to within 1e-6 in rms and exactly in Υ, read from `CFG4_galaxy_law_results.json`.

**T4 (reported, no verdict weight). Solar System at γ = 0.** Δg/g_N = y^{-1/2} at Saturn's orbit (9.58 AU) and at 1 AU, both
footings. Reported as the size of the high-field residual that stiffness would have to screen. Not scored against Cassini here.

## MUTATE (`CFG690_MUTATE=1`, exit 1 iff every tooth bites)
- M1: W = |P|² in T1 must be NOT invariant.
- M2: the source with ρ_b → λ⁻²ρ_b (wrong mass scaling) must break T1(b).
- M3: ν = 1 in T3 must FAIL the PASS line (rms ≥ 0.25).

## Verdict
- R0 status of the cubic: PASS / R0-SHAPED, REDUCED / R0-SHAPED (unchanged), by the reading rule.
- C2 status of astra's γ = 0 interpolation: PASS / FAIL on both footings.
- Not claimed: anything about stiffness, attractors (M1a), the energy ledger (M2) or lensing (M3a). Those stay as scored in
  CFG679 Part 2.
