# D9b_A33_multiplier: A33 plus a multiplier that enforces D·P = ρ_c − ρ̄

**Verdict: SCOPED NO-GO.** This is the open row 12′ of `../D9_uv_parent/MAP.md`. A33 with a Lagrange multiplier λ enforcing
D·P = ρ_c − ρ̄ as a field equation (A66's "Route A") is not a viable parent.
- **Literal version** (A33 as written + λ): fails the law. The medium's mass is counted twice.
- **Law-preserving version M\*** (unique up to a redefinition of λ): a healthy, causal, well-posed EFT. But it meets every
  hypothesis of theorem D-T, so the medium has no linear self-gravity (growth a^0.6095 in EdS). NG1 also applies: the static
  law needs ρ_c down to −231 ρ̄ at saddles.

So enforcing the identity is exactly what brings D-T and NG1 back. A33 escapes them only because it does not enforce it.

Settings: κ = ½ FITTED (thermal κ = Z/4π is a postulate). Footings 9.36e-11 / 1.13e-10 m/s², never pooled. Cold energy, no
particle species. Not "theory closed". Nothing here says the data favour the framework over ΛCDM.

## Files and runs
- `FROZEN_CRITERIA.md`: committed alone first (ce12fb3210).
- `d9b_a33_multiplier.py` (sympy + numpy; 18 s, 108 MB RSS, single thread). It writes `d9b_a33_multiplier.out` and
  `d9b_a33_multiplier_results.json`. Result: **14/14 PASS**, exit 0.
- **First run: 11/14** (kept as `*_firstrun.*`). The three FAILs were code bugs, not physics:
  - C2 and C4: sympy `Integer(2) == 2.0` is False.
  - V1: an un-cancelled (a₀ − u)²/(a₀ − u)² made `has(a0)` true.
  - Fixed by casting to float and by `cancel`. No criterion changed.
- `D9B_MUTATE=1` puts WT-02/CFG938 S1d's −3Hσ̇ into the constraint. F1 and F2 then FAIL: Re s/k² = 4.71 at every k, which is
  Hadamard-ill-posed (`*_MUTATE.*`).

## Results
1. **The literal theory double-counts the medium (L1, exact).**
   - Static cold branch: (ξ + m_c) g = KW′(u) and g = g_N + (ξ + m_c) u. Here ξ is the clock coefficient and m_c the medium's
     rest-mass coupling to the lapse.
   - The law holds iff ξ + m_c = 1.
   - A33 as written has ξ = 1 (its K5) and m_c = 1 (minimally coupled T^c, §1/§3.4), so s = 2.
     - At g = a₀/3, g_N − law = −0.55 a₀ (−5.15e-11 / −6.22e-11 m/s²). This is A33's own K5 number.
     - There is no deep-MOND branch: g_N → 0 at g = 1.5 a₀ (1.40e-10 / 1.70e-10 m/s²).
2. **The law-preserving parent is unique, and it is S2 + identity (L2, L3).**
   - The members with ξ + m_c = 1 are one theory: λ → λ + cΦ maps between them (by construction).
   - Its static cold equations are AQUAL L49 with μ = x/(1+x), exactly.
   - Natural form: A33 with the clock term removed and the medium minimally coupled.
3. **Constraint algebra and DOF (C1–C4).** Linear Dirac algorithm per scalar Fourier mode (A68's H = 0 action + medium + λ),
   cross-checked by deg det/2 of the EL operator.
   - Control: A68's single scalar is reproduced.
   - λ adds 2 dimensions and a chain of **4 second-class constraints**: π_λ, φ = D·P − δρ_c, φ̇, and the equation that fixes λ.
     It removes exactly **one** scalar.
   - Field theory: 26 + 6 (medium labels) + 2 = 34 dimensions, 8 first-class, 4 second-class ⇒ **7 DOF**. Without λ there are 8.
     Both counts are 2 tensor + 2 transverse P + 2 vortical medium + the scalars (2 without λ, 1 with).
   - A68's fifth mode (γ/η) and the bare medium sound (σ_c²) merge into one dressed sound: ω²/k² = (σ_c² + γρ_c)/(1 + ηρ_c).
   - So A66's "4 DOF" is right only if the medium is not counted. Its check A3 never computed it.
4. **D-T applies (T1–T3).** All four hypotheses of CFG941 DERIVATION §1.3 are MET, each tied to a computed item.
   - Low-k Newtonian reduction of M\*: c₂ = 1 exactly. The W-quadratic restoring term cancels the medium's Jeans term, so
     ω² = k²(σ_c² + γρ)/(1 + ηρ), with no −Kρ̄.
   - The medium still feels the baryons (cross term = dust value).
   - EdS growth exponent from the derived accelerations: **n = 0.60953**. This reproduces CFG941 K3 (0.60954); dust gives 1.
   - The literal theory gives c₂ = −2 (triple self-gravity).
5. **NG1 applies (N1).** M\*'s static branch is L49 (item 2), and ρ_c = ρ̄ + ρ_ph is enforced. AG6C's committed saddle solve
   therefore applies verbatim:
   - MW–M31 pair: min ρ_c/ρ̄ = −210 (canonical) / −231 (alt).
   - Cluster pair: −78 / −86.
6. **The cone is healthy (V1).**
   - The polarization that carried A33's sup v² = (γ/η)(1 + 4ηa₀²/K) is the longitudinal δP. The constraint now ties it to the
     medium (q = −ρ_c s).
   - Its speed becomes v² = (σ_c² + γρ_c)/(1 + ηρ_c/Δ). Here Δ = 1 − 2ηu²cos²θ/(Kβ) + 4ηu²sin²θ/K, round-2's margin.
   - u enters only through Δ, in the denominator. The W Hessian, including the a₀/(a₀ − u) factor, drops out at principal order.
     There is no U(1)-type divergence.
   - sup v² = max(γ/η, σ_c² + γρ_c) for Δ > 0.
   - At η = γ the non-tensor excess over c is 0 (A33's was 1.19e-18 / 1.73e-18 at L★ = 24 pc and 2.07e-15 / 3.01e-15 at 1 kpc).
     The dressed sound has v²/c² = 7.7e-10 / 9.3e-10 (24 pc) and 3.2e-8 / 3.9e-8 (1 kpc) at ρ̄_c.
7. **FRW is well posed (F1, F2).**
   - The constraint uses the intrinsic leaf divergence with an explicit ρ̄ subtraction. That is WT-02's MU3 repair.
   - The frozen-coefficient root set has max Re s = −0.075 (= −¾H in the test units) at k = 10 to 10⁴, so Re s/k² → 0.
   - λ obeys an elliptic leaf equation with coefficient k²(1/η + ρ_c) > 0.
8. **(Not frozen; reported only, no verdict weight) X1.** In M\* the medium's dispersion sits in the tether balance, so the
   static law is exact only as σ_c → 0.
   - For the deep phantom (ρ_c ∝ r⁻²), (g − KW′)/g = 2L★/r_M.
   - At L★ = 24 pc: 1.2% / 1.4% for 1e10 M☉ and 12% / 14% for 1e8 M☉ (canonical / alt).
   - A33 without λ has no such term.

## What this does not show
- No full nonlinear constraint algebra. {H_⊥, H_⊥} first-classness is inherited from A54/A68. The per-mode count is at
  H = 0, linear, with a Jeans swindle. Its low-k limit is not used (a flat background with ρ̄ ≠ 0 is not a solution).
  D-T is tested in the Newtonian decoupling instead.
- **NG1 here is AG6C's solve, not a new one.** This lane shows only that M\*'s static branch is L49 with ρ_c = ρ̄ + ρ_ph enforced.
- The ρ̄ in the constraint is either a prescribed function of cosmic time or the leaf mean of ρ_c (integrating the constraint over
  a closed leaf forces it). The second choice is non-local. Neither is analysed further.
- **Not excluded:** parents that enforce only part of the identity, or that gate it. Those are CFG941's R3θ family (ghost,
  CFG944).
- **No UV completion.** L★ and η/γ remain inputs.

## Record checked
- A33 MASTER_ACTION §1, §3, K5, K13, K15.
- A66 report and its erratum.
- A68 report, especially §1.5 B9 ("Route A not checked").
- D9 README and MAP.
- CFG941 README and DERIVATION §1.1–1.4.
- AG6C README §5 and `ag6c_s0_saddle_results.json`.
- WT-02 README (a) and MU3.
- Round-2 `03_relativity/report.md` §4.

## Record issues found
- **A66 `report.md` §2.2–2.3.** The Route A pair (π_λ, φ) is called "first-class". It is not: the chain is 4 second-class
  constraints (C3).
  - The "4 DOF" holds only with the medium uncounted. With the medium there are 7 in total, 1 scalar.
  - "Law preserved" is false for A33 as written (L1: s = 2).
- **A33 `MASTER_ACTION.md` line 131 vs line 63.** The lapse source ρ_m + ρ_c + d, with d = ς(ρ_c − ρ̄), counts the medium's excess
  twice at ς = 1. That is the one partition §7.3 allows.
  - It is consistent only if the ρ_c in (L) means the native part (1 − ς)ρ_c, which the text does not say.
  - Line 279's g_N = GM_src/r² then includes the medium.
  - This is harmless for A33 itself, because its identity is only a matching. It is exactly what breaks the law once the identity
    is enforced.
