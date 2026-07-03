**STATUS UPDATE 2026-07-03: GATE-G CLOSED NEGATIVE — the classification is resolved: FIFTH THEOREM (gas-clamp form). See GATE_G_VERDICT_2026-07.md. The inverted-line kernel is a KK-locked super-threshold amplifier at its own frequency; the cold-ISM acoustic continuum spans every placement in the surviving box (0/25 subregions alive): either the inversion clamps and erases the deep-MOND limit exactly where SPARC measures it, or the pump budget fails x>=350 (F falls with G). The WB gamma->1.28 prediction and the binary separation-gap observable are WITHDRAWN with this kernel. Scope: the inverted-line MI realization; the a0 reframing and live empirical fronts untouched.**

# KERNEL CONSTRUCTION — ADVERSARIAL VERDICT (2026-07)

**Verifier pass over the four-bureau gauntlet.** All 6 bureau scripts re-run exit 0; the three load-bearing numbers re-derived independently in `av_verify.py` (scratchpad, exit 0). No number was found asserted-not-computed. Framework objects only: a0 = cH_Λ/Z = 9.36e-11, μ_fw(x) = (√(1+4x²)−1)/(2x), Z = √(32π/3).

## 1. The construction (exact)

m_eff(t) = m·[1 − S(|a(t)|/a₀)·R(ω)], S = 1 − μ_fw, evaluated on the worldline in the preferred (CMB) frame. Medium: ONE inverted (non-KMS) spectral line at ν₂ ∈ [1.1e6, 9.9e7] H₀ (period 0.9–83 kyr), homogeneous width Γ_hom = 3H₀ (pump-refresh, medium-internal — NOT baryon drag), **Gaussian** (super-exponential) inhomogeneous profile, **anharmonic/dispersive** saturation (amplitude-dependent stiffness, lag τ_eff = Γ_hom/ν₂² ≈ hours), coupling −m-tuned ∝ mass (≤1%, WEP-blind).

**Verified exact (rtol 1e-12):** on circular orbits the kernel collapses to μ_fw(g/a₀)·g = g_bar ⇔ g_obs = √(g_bar² + g_bar·a₀) — Milgrom 2022 (PRD 106,064060) constraint held; SPARC 0.108 dex by construction.

## 2. Re-derived load-bearing numbers (verifier's own, vs gauntlet)

| Quantity | Gauntlet | Verifier (independent) | Verdict |
|---|---|---|---|
| Saturn ceiling ν₂_max | 9.88e7 H₀ | 1.00e8 H₀ (S(u=6.9e5)=7.2e-7, Ω_Sat=3.07e9 H₀, δa<5e-14) | **CONFIRMED** |
| Saturn δa @ box center | 5.3e-16 m/s² | 5.0e-16 | CONFIRMED |
| WB γ at 2/10/30 kAU | 1.021/1.236/1.276 | 1.016/1.215/1.275; asymptote = 1/μ_fw(g_ext/a₀) = **1.276 forced** | **CONFIRMED** |
| Energetics headroom | 25× (D1 demand 5.3e-29 W/m³ vs Λ-draw 1.2e-27) | independent demand model (MOND-zone dressing refreshed at 3H₀): 2.5e-30 → 470×; D1's is ×21 harsher and still passes | **CONFIRMED — no energetics fifth theorem, both ways** |
| Lorentzian-tail kill | ~1e3 over tolerance | ×6e6 over tolerance (Im/Re = 2.7e2 vs 4.8e-5 orbit-count budget at band top); Gaussian clears at 2e-8 | CONFIRMED (stronger than quoted) |
| τ_eff = Γ_hom/ν₂² | claimed | verified analytically (off-resonant driven phase lag); population-saturation lag = 1/Γ ≈ 2e17 s contrast — D3's pump theorem correctly becomes a floor, not a kill | CONFIRMED |
| R2-drag exclusion | ×42 | ×42 (v decay ×0.125 / 10 Gyr) | CONFIRMED |
| Pump floor under calibration stress | 1.08e6 H₀ | ×1.7 miss (0.66-vs-0.38) → floor 1.4e6; box still 1.85 decades, **NONEMPTY** | CONFIRMED under stress |

## 3. Adversarial findings (both-ways; none manufactured, two under-statements found)

1. **F–G coupling (new, structural):** GATE-F's headroom prices *spontaneous* refresh at Γ=3H₀. If GATE-G fails (collective lasing/ASE), the drain is stimulated and unbounded until clamped — **F is PASS conditional on G**, not independent. The gauntlet table did not state this.
2. **WB prediction supersedes the banked one:** this kernel forces γ(wide) → 1/μ_fw(g_ext/a₀) = 1.28, ABOVE both the banked framework MI-EFE range (γ ~ 1.05–1.10) and the MG value 1.137. Kernel-specific and more exposed: Gaia DR4 at γ ≈ 1.05–1.10 kills THIS kernel while generic MI survives; γ ≈ 1.0 (Banik-confirmed) kills the whole box. The banked WB standing must be marked superseded-for-this-kernel.
3. **Soft spots (flagged, not verdict-flipping):** the "γ rising with separation" rolloff signature is floor-specific (at ν₂ ≥ 3e6 H₀ all WB separations are in-band; the rise is then pure μ_fw+EFE); the ×1.7 calibration miss was labeled "✓"; the Saturn 5e-14 gate is order-of-magnitude (ceiling soft by ~×2, box robust).
4. **Strawman check (fifth-theorem side): passed.** The energetics pass, the τ_eff floor mechanism, and the Lorentzian kill are all realization-generic (class-level), not artifacts of one bureau's ansatz. "No fifth theorem at gates A–F" covers the class.
5. **No hidden R-selection:** kernel variables |a| and ω are worldline-intrinsic; a₀, ν₂, Γ_hom are medium constants; band flatness 1.8e-8 dex ≪ 0.079 (R3). Fourth Horn respected: amplitude dependence enters via NONLINEAR (anharmonic) response, which the linear-law theorem does not bind.

## 4. FORCED vs POSITED

**Forced (computed):** above-band inverted weight; Gaussian/super-exponential tails (Markovian killed ×6e6); dispersive-not-population saturation; Γ_hom ≈ 3H₀ pinning, medium-internal (drag excluded ×42); ν₂ box [1.1e6, 9.9e7] H₀ (pump floor + Saturn ceiling); WBs MONDian with γ→1.28 asymptote; η(β) slide inherited (DOI 10.5281/zenodo.21104820).
**Posited (enumerated, per the state clause the medium is a NEW POSIT):** (1) the inverted medium itself — the dS horizon is a thermostat, not this source (DOI 10.5281/zenodo.21139029); (2) pump identity (best survivor: CMB-cycled radio-tail, 3-deep stack); (3) −m tuning ≤1% ∝ mass; (4) |a| as saturation variable + inserted μ_fw shape (gauntlet3: physical gain saturation gives wrong exponents); (5) Gaussian profile (forced in class, Gaussian in particular chosen); (6) spatial homogeneity of the tuned coupling (R3 beyond band-flatness — "anharmonic collective scales unmodeled"); (7) laser-threshold analogy for GATE-G; (8) a₀ = cH_Λ/Z remains a posited normalization.

## 5. CLASSIFICATION: **OPEN — at exactly one gate (GATE-G), leaning candidate**

- **Undetermined gate:** G (medium self-consistency): collective-lasing/ASE clamp ~H₀ vs demand 3H₀ — same order, undecidable at bureau resolution (their own script says so), and F is conditional on it.
- **Closing computation (named):** collective-mode/ASE threshold sum for the inverted ensemble WITH Gaussian inhomogeneous broadening over the gravitational mode structure. Verifier's standard-scaling estimate: threshold raised ~σ_inh/Γ_hom ≈ 5.6e5 — five decades of margin over the ×3 shortfall — but a scaling estimate may not close a gate; the mode-sum is the computation.
- **Not FIFTH-THEOREM:** every anticipated killer was computed and dies or becomes a bound (energetics ≥25× re-derived; sum-rule doesn't reach above-band weight; pump theorem → floor). No kill was soft-pedaled: the box shrank 2.1 decades under the pump theorem and survived my calibration stress.
- **Not yet FIRST-CANDIDATE:** one gate open, headroom on F conditional on it. If the mode-sum closes G as the scaling indicates, this becomes the first covariant-MI candidate — with the 8 posits above enumerated, clusters keeping their matter component, and NOT a TOE.

**Kill lines, ranked:** (1) GATE-G mode-sum (computable now, decides the classification); (2) Gaia DR4 WBs — γ ≈ 1.28 rising-to-asymptote or dead (Newtonian corner eliminated: Ω_WB ≈ 1.9e5 H₀ < ν₂ floor); (3) η(β) anisotropy slide on pressure-supported systems, inherited unchanged.

## 6. Paper recommendation

**MAY:** publish as a *specification note* — the four theorems assembled, the ν₂ box with floor/ceiling derivations, the gate table (G explicitly OPEN, F conditional on G), the forced-vs-posited ledger, and the sharpened WB falsifier γ(s) → 1.28 with the explicit statement that it supersedes the banked MI-EFE 1.05–1.10 for this kernel.
**MAY NOT:** claim "candidate survives/found" (G open); claim a₀ derived, the medium identified, or the pump known; call it a TOE or cluster solution; present "no fifth theorem" as "no kill possible" (G may yet be it); cite the WB numbers without the Banik kill-line; present the rising-γ(s) rolloff signature as box-wide.

**Scripts:** `av_verify.py` (this verdict, exit 0) + `int_gauntlet.py`, `d1_kernel_inversion.py`, `d2_band_ladder.py`, `d2_pump_energetics.py`, `d3_kernel_gauntlet.py`, `d3_pump_certify_v4.py` (all re-run exit 0, 2026-07-02) in session scratchpad; promote to `reviews/` before commit.
**Citations:** DOI 10.5281/zenodo.21148494 (Fourth Horn); 10.5281/zenodo.21139029 (state clause); 10.5281/zenodo.21104820 (η(β)); Milgrom 2022 PRD 106,064060; Hees+ 2014 PRD 89,102002; Desmond-Hees-Famaey 2024 MNRAS 530,1781; Park+ 2026 arXiv:2602.17884; Chae 2023 ApJ 952,128; Banik+ 2024 MNRAS 527,4573; `real_research/PUMP_HUNT_AND_TRIGGERS_2026-07.md`.
