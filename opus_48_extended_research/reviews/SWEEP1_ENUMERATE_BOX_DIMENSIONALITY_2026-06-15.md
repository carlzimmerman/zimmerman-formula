# Sweep 1 — the effective parameter box of the framework on AeST + its dimensionality (Opus 4.8 [1m], 2026-06-15)

*Enumerate EVERY effective free parameter, its allowed range, and what constrains it. State the dimensionality and
classify each parameter (a) TIED, (b) NUISANCE, (c) GENUINELY-FREE AeST extension. Count the genuinely-free numbers
beyond a0=Lambda. Both ways: count the AeST free functions as a COST; count the a0=Lambda tie as a SAVING. Quarantine
held: a0/Z never asserted derived. All numbers recomputed in `/tmp/enumerate_box.py` + `/tmp/squeeze_and_dim.py`.*

---

## Headline (the count, one line)

The framework on AeST is a **2-extra-number** theory beyond the `a0=Λ` spine: **I0** (the CMB dust amplitude, ≈Ω_c)
and **μ** (the cluster scalar mass). The `a0=Λ` tie is a genuine **−1 saving vs generic MOND** (a0 is not an
independent number). The AeST free function `K(Q)` is a real **cost** (a constructed shape), but its load-bearing
content reduces to those same 2 effective numbers. Net: roughly ΛCDM's effective parameter count at the CMB — the win
is conceptual unity (one geometry, c_GW=c, no-slip lensing), **not** parameter parsimony.

---

## THE BOX  [parameter × [min,max] × constrained-by × class]

| # | parameter | allowed range | constrained-by | class |
|---|---|---|---|---|
| 1 | **a0** | framework 9.36e-11; galactic band [9.1e-11 (simple-μ), 1.2e-10 (McGaugh)] | TIED: `a0 = c²√(Λ/32π)`; one number with Λ | **(a) TIED** — saving −1 |
| 2 | **Υ_disk** | [0.4, 0.7] | stellar pops 3.6 µm; sets RAR a0-opt + cluster η | **(b) NUISANCE** (shared by all MOND) |
| 3 | **ν (IF)** | discrete {dS-Unruh, simple-μ, standard-μ, McGaugh} | framework = dS-Unruh √(1+1/y); only bites transition/EFE | **(b) NUISANCE** (~0 dof, chosen) |
| 4 | **μ** (scalar mass) | 1/μ ≈ 1 Mpc; `m²/f_G ∈ [0.001, 2.5] Mpc⁻²` | Mistele squeeze (galaxy-WL <1 vs cluster >2.5) | **(c) GENUINELY-FREE AeST** |
| 5 | **I0** (dust ampl) | `8πG̃ρ̄₀ = Q₀ I0` → Ω_dust ≈ 0.26 | CMB 3rd peak (Ω_c h²=0.12); integration constant | **(c) GENUINELY-FREE AeST** |
| 6 | **cs²** | [0,1]; CMB forces ~0 | k-essence `cs²=(Q−Q0)/Q ∝ a⁻³`; pinned ≲10⁻⁹ today | **(c′) DERIVED-not-free** (pinned ~0) |
| 7 | **K2, Q0** (K-shape) | free-function coeffs | CMB fit; together SET μ and I0 (not extra dof) | **(c) FREE but reducible to #4,#5** |
| 8 | **λ_s, β0** | O(1), RAR-pinned | SPARC RAR transition / Cassini exposure | **(b) NUISANCE** (galaxy-pinned) |
| 9 | **Z** (coeff) | 5.789 (κ=½); 6 (Verlinde); 2π (thermal) | UNFORCED; cancels in every falsifiable test | **MOOT** (0 effective dof) |

---

## CLASSIFICATION (a)/(b)/(c) and the count

**(a) TIED — a0 = c²√(Λ/32π).** Recomputed: Λ = 3Ω_Λ H₀²/c² = 1.091e-52 m⁻², giving `a0 = 9.3614e-11` (target 9.36e-11,
0.00%). Equivalently `a0 = cH_Λ/Z` with `cH_Λ = cH₀√Ω_Λ` and `Z=√(32π/3)=5.7888` — both constructions agree to 0.00%.
This is the unification: a0 is **not** an independent number. **Saving: −1 vs generic MOND** (where a0 is fit freely).
Quarantine: this is a TIE (posit a0↔Λ), NOT a derivation — AeST itself does not enforce the link (Λ is "freely
specifiable just as in ΛCDM," Skordis-Złośnik verbatim); the tie is an extra posit Carl adds.

**(b) NUISANCE — Υ, ν, λ_s, β0.** Not framework-specific; shared with every MOND/AeST analysis. Their effect is real but
bounded and non-diagnostic of the framework:
- **Υ_disk ∈ [0.4, 0.7]** — the load-bearing nuisance; the RAR a0-optimum and the cluster η both move with it.
- **ν (IF)** — DISCRETE, not continuous. The framework picks dS-Unruh. IF spread at fixed a0 (recomputed): **1.5%
  deep-MOND → 8.5% near-MOND → 13% transition → 1.0% Newtonian** (crude boost formulas; the banked transition figure is
  ~23.5% on the exact ν's). The IF only bites in the transition + external-field regime; deep-MOND (BTFR, dSph) and
  Newtonian are intrinsically IF-robust, and a0(z) is IF-FREE (cancels in the ratio). So ν is ~0 effective dof.
- **λ_s, β0** — O(1), pinned by the SPARC RAR fit (and they transplant the Cassini quadrupole tension).

**(c) GENUINELY-FREE AeST extension — I0, μ (the +2), with cs² pinned and K2/Q0 reducing to I0&μ.**
- **I0 (the dust amplitude)** — `8πG̃ρ̄₀ = Q₀ I0`, an integration constant Skordis-Złośnik state is "not (classically)
  predicted." Fixes Ω_dust ≈ Ω_c ≈ 0.26 to match the CMB 3rd peak (Ω_c h²=0.119 vs Planck 0.120). **The real cost: a0=Λ
  does NOT supply it** — a0 is absent from linear cosmology (δq⁰⁰=0; Ȳ=0 on FRW), so the unification fails at the CMB.
- **μ (the cluster scalar mass)** — `μ² = 2K2 Q0²/(2−K_B)`, 1/μ ≈ 1 Mpc. Recomputed (μr)² at 1/μ=1 Mpc: 6e-20 (50 AU) →
  1e-4 (10 kpc galaxy) → **1.69 (R500)** → 9 (3 Mpc): OFF below clusters, ON at clusters (right scale). But **the
  Mistele squeeze** double-binds it: galaxy-WL needs `m²/f_G < 1 Mpc⁻²` (<0.001 if MONDian to 10⁻¹⁵), clusters need
  `> 2.5 Mpc⁻²` for ≥10%. **One μ cannot do both.**
- **cs² is DERIVED, not free** — sympy result `cs²=(Q−Q0)/Q ∝ a⁻³`; the CMB forces cs²(a_rec)≪1, so cs²_today ≲ a_rec³ ≈
  7.7e-10 ≈ 0. This is the **scale-blindness** result: a cs²≈0 dust clusters at BOTH cluster (1-3 Mpc) and galaxy
  (30 kpc) scales, so **I0 cannot double as the cluster residual** — that is why the cost is +2 (separate μ), not the
  +1 a unified scalar would buy.
- **K2, Q0** — the underlying free-function coefficients. They are genuinely free, but they jointly **parametrize** I0
  (via Q₀·I0) and μ (via 2K2Q0²) — they are not 2 dof *on top of* I0 and μ; they ARE the parametrization of those 2.

---

## THE COUNT (both ways)

```
Genuinely-free numbers BEYOND a0=Λ:
  I0  (CMB dust Ω≈0.26)          +1   the real cost; a0=Λ does not give it (CMB-only)
  μ   (cluster mass, 1/μ~1 Mpc)  +1   Mistele-squeezed; not from a0/Λ
  K2,Q0                           —    parametrize I0&μ, not extra dof
  cs²                            +0   derived ∝a⁻³, pinned ~0 by CMB
  Z                              +0   moot (cancels in every test)
  Υ, ν, λ_s, β0                  +0   shared-MOND/galaxy-pinned nuisance
  ----------------------------------------------------------------
  NET genuinely-free AeST extension beyond a0=Λ:  +2  (I0, μ)
```

**Dimensionality, stated cleanly:**
- **Effective free dof = 2** (I0, μ) on top of the `a0=Λ` spine.
- Plus the **shared nuisance subspace** (Υ ∈ [0.4,0.7]; ν discrete; λ_s,β0 O(1)) that every MOND/AeST analysis carries.
- Plus the **moot** dof (Z, the O(1) coefficient; cs² pinned ~0) — both 0 effective.

**Both ways — the saving and the cost stated honestly:**
- **SAVING (credit the tie):** a0 is TIED to Λ → −1 vs generic MOND (a0 not independent). At z=0 galaxies this is a real
  unification (MOND boost ↔ dark energy, one number), verified: a0=9.36e-11 reproduced from Λ to 0.00%.
- **COST (concede the free functions):** AeST needs a free function K(Q) constructed to mimic CDM, whose load-bearing
  content is the +2 (I0, μ). At the CMB level AeST ≈ ΛCDM's effective parameter count (it trades the CDM *particle* for a
  dust *mode* with the same effective Ω). The win is conceptual unity + GW-safety + no-slip lensing — NOT parsimony.

---

## What this sweep does NOT settle (handed to the later sweeps)

This is the box enumeration only. It does **not** decide whether a single connected (a0~Λ, Υ, ν, μ, I0, cs²) region is
simultaneously viable across the 9 fronts, nor how fine-tuned it is. The pre-loaded blockers for that intersection (from
the banked work, to be quantified downstream): the **Mistele squeeze** makes the μ that clusters need (>2.5 Mpc⁻²)
collide with the μ galaxy-WL allows (<1, <0.001 tight); and the **cs² scale-blindness** forbids reusing I0 for clusters.
If those hold, the cluster front needs a μ the galaxy-WL front forbids → the intersection is empty *for a quantitative
cluster cure*, while the rest (RAR/BTFR/dSph/lensing/a0(z)) sit in a broad, non-diagnostic region. Sweep 1's job is the
**box**; the intersection + fine-tuning volume is Sweeps 2+.

*Sources: Skordis & Złośnik 2021 PRL 127 161302 (arXiv:2007.00082, a0 in Y^{3/2}, I0 "not classically predicted", Λ
"freely specifiable"); Verwayen/Skordis/Złośnik 2024 MNRAS 531 272 (arXiv:2304.05134, μ,β0,χ_out); Durakovic & Skordis
2024 JCAP 04 040 (arXiv:2312.00889, μ²=2K2Q0²/(2−K_B), 1/μ≳1 Mpc); Mistele+2023 A&A 676 A100 (arXiv:2301.03499, m²/f_G
squeeze); Garriga-Mukhanov 1999 (cs²); banked ROUTE5_UNIFICATION_COST, FRONTIER3_UNIFIED_SCALAR_SOUNDSPEED,
INTERPOLATION_FUNCTION_AUDIT_LEDGER, SKORDIS_GEOMETRIC_FRAMEWORK_REVIEW, OPEN_PROBLEM_yphi32_KQ. Numbers in
/tmp/enumerate_box.py + /tmp/squeeze_and_dim.py.*
