# A78 — IS β A PHYSICAL PARAMETER? FIELD REDEFINITION, BACKGROUND, OR HOLE

**Lane:** A78_beta_closure · **Date:** 2026-10-22
**Read first (canonical):** `A54_four_gates/report.md` (Q₀ = (2+3β)/(Kβ) + ηk²/K²; 4c_β−2 = −2β/(2+3β); Legendre map singular only at β = −2/3),
`A33_master_action/MASTER_ACTION.md` (β's row: "nothing (free)"; 2+3β = 2Λ_bare c²/(3H²); Λ_bare ≥ 1.462 Λ_obs; β invisible to α₁, α₂, β_PPN),
`A68_bracket_algebra/report.md` (Z = K(2+3β)/β + ηp², positive iff β > 0 on the 2+3β > 0 branch), `A69_psector_sound/report.md`.
**Script:** `a78_checks.py` — **30/30 PASS, exit 0, 0.56 s** · **Output:** `a78.out` · **Data:** `a78_results.json` · **Mutations:** `MUTATE.md` (11 dials, each exit 1).

Every number below is printed by `a78_checks.py`; the check that produces it is named in brackets.

---

## 0. The answer in one paragraph

**β is not a field-redefinition redundancy, and the premise that it is invisible to every observable is false.** The
three rescalings that could absorb a kinetic coefficient — `h → Ω²h`, `N → χN`, `P → λP` — are each pinned by an
independent measured normalisation (the `R₃` coefficient = the static `G`; the `K_ijK^ij` coefficient = `c_T² = 1`;
the clock coefficient = 1, i.e. the *shape* of `g_N = g²/(g+a₀)`); the 3×3 system has determinant **4** and its unique
solution is the identity **[C23_DET, C24_IDENT]**. No shift redefinition can do it either: `N^i` is eliminated by its
own equation, so any `δN^i` changes the reduced action only at `O(δ²)` (ratio **4.000** on halving ε) **[C26_SHIFT2]**.
What β actually does is deform the `θ` sector, and `θ` is *identically zero on every static configuration* — which is
why it is invisible to the law, to α₁, α₂, β_PPN, and to the TT sector, all of which I verify are exactly β-free
**[C07–C16]**. But `θ ≠ 0` on any expanding background, and there β enters through the Friedmann normalisation:
`3(2+3β)H² = 2Λ_bare c² + 4Kρ`, i.e. **`G_cosmo/G_N = 2/(2+3β)`** **[C01, C03]**. That ratio is measured by the
expansion rate at fixed radiation density, so β has a handle: BBN's `|ΔN_eff| < 0.30` gives **β < 0.0280**
**[C29_BBN]**, i.e. `G_cosmo/G_N > 0.961` **[C03b]**. With that, the same background equation fixes the bare vacuum to
**`Λ_bare = Λ_obs(1 + 2.194 β)`**, so `Λ_bare/Λ_obs ∈ (1, 1.061)` **[C05, C30, C29]**. **Verdict: (c)** — β is physical, with one
quantified observable (the cosmological/static coupling ratio), and it is fixed by the background; the hole does not
disappear but it **relocates entirely to `Λ_bare`**, and the residual fine-tuning is O(β) ~ 4 %, not 10¹²⁰.

---

## 1. Task 1 — where β does and does not appear

The whole β-dependence of the action is the single operator `−(1+β)θ²/(4K)`, `θ = K^i_i = (1/N)(∂_t ln√h − D_iN^i)`.
Every statement below follows from one fact: **θ measures the volume change of the slicing**. Static ⟹ θ = 0 ⟹ β absent.

| # | observable | β-dependence | computed evidence |
|---|---|---|---|
| (a) | `g_N = g²/(g+a₀)` | **none, exactly** | C07, C08, C10, C11 |
| (b) | α₁, α₂, β_PPN | **none, exactly** | C07–C13 |
| (c) | graviton `c_T²`, `m_T²` | **none at O(h²)** | C14, C15, C16 |
| (d) | fifth mode `ω² = αp⁴/Z`, `Z = K(2+3β)/β + ηp²` | **O(1), in the overall coefficient only** | C17–C20, C22 |
| (e) | background `3(2+3β)H² = 2Λ_bare c² + 4Kρ` | **O(1): `G_cosmo/G_N = 2/(2+3β)`** | C01, C02, C03, C29 |

### (a) The law is β-free on shell, non-perturbatively

On the static branch (`ḣ_ij = 0`, `N^i = 0`, all `∂_t = 0`), `K_ij = (1/2N)(ḣ_ij − 2D_(iN_j)) ≡ 0`, hence
`θ = h^{ij}K_ij ≡ 0` and the entire β-term vanishes — for **every** β, at every order **[C07, C08]**. Differentiating
the static action density with respect to β gives `−9c_s²f³/(4KN)`, which is zero at `c_s = 0` **[C10_DSDB]**; the
sharpness check confirms the term is *not* zero as soon as `N^i = c_s r r̂` (`c_s = 0.05`) is switched on (`θ = −3c_s/N`,
density `2.25 c_s²f³(1+β)/(KN)`, value **8.014e−02** at the test point) **[C09_SHARP]**. So β's invisibility is
*staticity*, not absence.

The static equations therefore contain no β at all, and the record's chain survives verbatim: `g_N = g − u` with
`ξg = KW'(u)` ⟹ `g_N = g²/(g+a₀)` **[C11_LAW]**, which is AQUAL `μ(x) = x/(1+x)` **[C12_AQUAL]**. The `ξ = 2`
deformation reproduces A33 K5's `−0.550 a₀` at `g = a₀/3` from those two relations alone **[C11]**.

### (b) PPN: β-free because the static solution is

α₁, α₂, β_PPN are functionals of the static post-Newtonian solution. Since the static action has identically zero
β-derivative (above), that solution is β-independent, so all three parameters are. The only β-carrying object in the
PPN inventory would be θ, and θ ≡ 0. Numerically: `α₁(1 AU) = 2r²/L*² = r²K/γ = 8.161261e−14` **[C13_ALPHA1]**,
which contains γ and no β. This agrees with the known khronometric result for the λ-only sector (`α = β_aether = 0`):
the only new operator is `(∇·u)²`, which is inert for a static foliation-normal aether. **The record is right that β
is PPN-invisible; the inference "therefore invisible" is what §1(e) overturns.**

### (c) TT: β enters at O(h⁴), not O(h²)

For a TT mode `diag(h₊, −h₊, 0)` the determinant is `1 − h₊²`, so `θ = ½∂_t ln det = −ε²a ∂_t a + …`: the O(ε)
coefficient is **0** **[C14_TTTHETA]** and `θ²` starts at O(ε⁴). Hence the quadratic TT action is
`(1/4K)[ḣ²/4 − k²h²/4]` with `c_T² = 1` **[C15_CT2]** and `dS_TT/dβ ≡ 0` **[C16_TTBETA]** — speed *and* mass are β-free.
(The mass *value* `m_T²` is A54 G2's; what is proven here is that no β can enter it at O(h²).)

### (d) The fifth mode: β survives, with an O(1) coefficient

Eliminating the shift from the quadratic scalar action gives `L = ½Z σ̇² − ½αp⁴σ²`,
`Z = B + ηp²`, `B = K(2+3β)/β`, reproduced here from the action (symbolic elimination *and* a numerical extremum agree
to 3e−13) and matched against A68's formula **[C17_B, C18_Z_b1, C18_Z_b3]**. `Z`'s sign is β's sign on the
`2+3β > 0` branch **[C19_ZSIGN]**: `Z/K = −0.333, −1.000, −17.00, +23.00, +7.000, +5.000, +3.667` at
`β = −0.6, −0.5, −0.1, 0.1, 0.5, 1, 3`.

Size of the effect: `ω² = αp⁴/Z` at fixed `p → 0` shifts by
`ω²(β=3)/ω²(β=1) = B(1)/B(3) = 15/11 = 1.3636` (printed as `ω²(1)/ω²(3) = 0.7333`) **[C20_RATIO]** — a **36 %**
change in the fifth mode's frequency for an O(1) change in β. This is an on-shell quantity (a pole), so it is a genuine
β-channel. It is not *observable*: at every momentum of interest the `ηp²` piece is negligible
(`η p_sc²/B = 1.1328e−89`, printed in `a78.out`, so `Z(p_sc) = B` to 89 digits), the mode is gapless with `c_s² = αp²/Z → 0`, and its
loop factor is ≤ 1.9e−70 (A69). The mode therefore *carries* β and cannot *measure* it. (Note `p_sc` itself is β-free:
`Z³κ_L⁶ = α³`.)

### (e) The background: β survives where it is observable

`3(2+3β)H² = 2Λ_bare c² + 4Kρ` — derived twice (full-ADM substitution vs the reduced ansatz, difference **0**)
**[C01_FRW]**, and the second Friedmann equation follows from the first along its own numerical solution
(`A(2Ḣ+3H²) = 2.0000000000`, `2Λ = 2.0`, residual 8e−16) **[C02_FRW2]**. Written in GR form,

```
3H² = Λ_eff + 8πG_eff ρ ,   Λ_eff = 2Λ_bare/(2+3β) ,   G_eff = 2G/(2+3β) .
```

`G_eff/G_N = 2/(2+3β)` = **1.000000, 0.961076, 0.571429, 0.400000, 0.181818** at β = 0, 0.027, 0.5, 1, 3
**[C03_GEFF]**, where `G_N = K/4π` comes independently from the *static* Poisson equation `∇²Φ = Kρ`. This ratio is a
prediction: the static and cosmological gravitational couplings differ by a β-dependent factor. **It is the observable
that closes β.**

---

## 2. Task 2 — the field-redefinition test: β cannot be absorbed

β multiplies no vertex, so the only redefinitions that could move it are normalisations. Three are available, and three
measured numbers pin them:

| rescaling | induced change | measured normalisation that pins it |
|---|---|---|
| `h_ij → Ω² h_ij` | `R₃` coeff `→ χΩ` | the static law's `G` (`R₃ = 2Λ + 4Kρ` ⟹ `G_N = K/4π`) |
| `N → χ N` | `K_ijK^ij` coeff `→ Ω³/χ`; `θ²` coeff `→ Ω³/χ` | `c_T² = 1` (GW170817, `|c_T−1| < 1e−15`) |
| `P_i → λ P_i` | clock coeff `→ ξχΩλ`; `B, α → λ²B, λ²α` | the *shape* of `g_N = g²/(g+a₀)` |

In log space the system is `M·(lnΩ, lnχ, lnλ) = (0, 0, −ln ξ)` with `M = [[1,1,0],[−1,3,0],[1,1,1]]`.
**`det M = 4`** (symbolic vs numerical 3×3 determinant agree to 0) **[C23_DET]**, and the unique solution is
`(Ω, χ, λ) = (1, 1, 1)` **[C24_IDENT]**. The determinant is non-zero *because* the `R₃` and `K_ijK^ij` coefficients
respond differently to a constant Weyl rescaling (`Ω¹` vs `Ω³` at fixed χ): that inequality is exactly the statement
that `G` and `c_T` are independent measurements. **There is no redundancy direction.**

Three corroborations, each computed:

1. **A nondimensional lapse rescaling is excluded at 1e−15.** `N → (1+χ)N` multiplies the `R₃` term by `(1+χ)` and
   divides the kinetic term by `(1+χ)`, so `c_T² → (1+χ)²` — a *speed*, not a normalisation. Same for a spatial Weyl
   rescaling, `c_T² → Ω⁴`.
2. **A shift redefinition is on-shell trivial.** `N^i_*` is defined by `δS/δN^i = 0`, so `N^i → N^i + δN^i` changes the
   reduced action only at `O(δ²)`: perturbing `Y_*` by ε gives `|ΔL|(ε) = 3.4225e−08, 8.5562e−09` for ε = 1e−3, 5e−4,
   ratio **4.000000** **[C26_SHIFT2]**. A shift redefinition therefore cannot change `Z` — and `Z` demonstrably carries β.
3. **The S-matrix is not invariant under any redefinition that would remove β.** `ω² = αp⁴/Z` is invariant under
   `σ → λσ` (all quadratic terms scale by λ²: `1.9999996e−13` at λ = 0.3, 1, 7, ratio 1 + 2e−16) **[C28_SMAT]**,
   but changes by 36 % between β = 1 and β = 3. Poles are redefinition-invariant; β moves a pole; hence β is not a
   redundancy. The unit charge is what makes this airtight for `λ`: without `ξ = 1` one could rescale `P` and trade
   `Z` for a normalisation, but `ξ = 1` is the law (`ξ = 1.05` deforms `g_N` by **−7.56 %** at `g = a₀`) **[C27_XI]**.

**No disformal transformation escapes this.** A time-space disformal piece `g_μν → g_μν + (1+χ)n_μn_ν` is a lapse
rescaling (row 2 above); a spatial one is row 1; both move `c_T²`, which is measured to 1e−15. There is no
θ-redefinition available because θ is a composite of `(h, N, N^i)`, not a field.

---

## 3. Task 3 — the background route: what fixes β, and what it costs

The exact relation, for all FRW epochs, is

```
3(2+3β) H² = 2Λ_bare c² + 4Kρ                                    [C01]
```

**What β = 1 requires.** `Λ_bare = 3.1936 Λ_obs` at the present epoch with matter included (`Ω_m = 0.3162` implied by
`Λ_obs, H₀`; Planck's 0.316) **[C05]**; or `Λ_bare = 3.6560 Λ_obs` in A33's vacuum/dS slice at `H = H₀` **[C04]**.
The two differ only because A33 sets `ρ = 0` while keeping `H = H₀` (i.e. `Ω_Λ,eff = 1`).

**What stability requires.** `β > 0 ⟺ Λ_bare > Λ_obs` in the matter-inclusive reading, `⟺ Λ_bare > 1.4624 Λ_obs` in
A33's dS reading **[C06_STAB]**, with the slopes agreeing: `Λ_bare − Λ_obs = (9/2)βH₀²/c²`, i.e. `2.194 Λ_obs` per unit β
**[C30_BARE]**. So the bare vacuum must *strictly exceed* the observed one, and the clock's negative stress
`ρ_β = −9βH²/(4K)` supplies the difference. **This is a prediction, not a tuning**: the excess is `O(β)`.

**What the observed expansion rate requires.** Two readings of the same measurement, and this is where the record needs
a correction. A33 (K16) applies the *vacuum* equation at `H = H₀` and concludes `Λ_bare ≥ 1.462 Λ_obs`. But at the
present epoch `ρ_m ≠ 0`; with matter included, `β = 0` sits **exactly** at `Λ_bare = Λ_obs`
(`Λ_bare(0)/Λ_obs = 1.0000000000`) **[C05_LAM0]**. The 1.462 figure is the `Ω_Λ,eff = 1` slice, not a bound on
`Λ_bare` in the real cosmology. **Both readings agree on the structure** (β > 0 needs `Λ_bare` above the value that
would reproduce the observed acceleration with β = 0); they differ by the O(β) matter term.

**Is any of this forced?** No. The action gives one equation for two unknowns (A33's degeneracy #4, `β ↔ Λ_bare`), and
nothing in A33/A72/the cell structure fixes `Λ_bare`. What breaks the degeneracy is *not* `Λ_bare` — it is the second
background observable, the normalisation `G_eff/G_N = 2/(2+3β)`. **That is a measurement of β alone**, independent of
`Λ_bare`; `Λ_bare` then follows from `Λ_eff`. With `|ΔN_eff| < 0.30` (Planck 2018 + BBN, 95 %),
`ΔN_eff = 7.4492(G_eff/G_N − 1) = −11.1738 β` ⟹

```
β < 0.0280   ⟹   G_eff/G_N > 0.9611   ⟹   Λ_bare/Λ_obs ∈ (1.000, 1.061)      [C29, C03b, C05]
```

So the theory predicts a bare vacuum within **6 %** of the observed one — a 10¹¹⁸ improvement in the "why so small"
bookkeeping is *not* what happens here; what happens is that the *coefficient* is pinned to 1.000–1.061, and only the
usual "why is Λ_obs ~ H₀² at all" remains.

**Does this merely relocate the hole?** Yes, explicitly: the free parameter left is `Λ_bare` (one number), and β is a
function of it and of the measured `H₀`. The relocation is nevertheless a *strict improvement*: (i) β's O(1) freedom is
gone, removed by data rather than by a posit; (ii) the surviving number is the one every theory with a cosmological
term already has; (iii) the required value is O(1)× the observed one, so no new fine-tuning is introduced. The closure
`Λ = 32πa₀²/c⁴` (A33 row 2) then applies to `Λ_eff` and, within 6 %, to `Λ_bare` as well
(`32πa₀²/c⁴ / Λ_obs = 1.001246`) **[C30]**.

---

## 4. Task 4 — verdict

**(c): β is a physical parameter with one observable consequence, and it is fixed by the background.**

- **(a) is false, by computation.** The rescaling group that preserves `{G_N, c_T² = 1, ξ = 1}` is trivial
  (`det = 4`, unique solution `(1,1,1)`) **[C23, C24]**; shift redefinitions are second-order on shell (ratio 4.000)
  **[C26]**; and `ω²(p)` is a pole that moves by 36 % between β = 1 and β = 3 **[C20, C28]**. β is not a redundancy.
- **(d) is false, by computation.** β has a handle: `G_cosmo/G_N = 2/(2+3β)`, a 1.5β fractional change in the expansion
  rate at fixed radiation density; the current bound is β < 0.0280 **[C29]**.
- **(b) is true as a corollary, not as the classification.** β is not fixed *by* `Λ_bare`; it is fixed *independently*,
  by the expansion normalisation, and `Λ_bare` then follows. The residual hole is `Λ_bare` alone.
- **(c) holds.** The observable is `G_cosmo/G_N`; its size is `2/(2+3β)` (0.961 at the bound, 0.400 at β = 1); the
  measurement that fixes it is the expansion rate at fixed `T` (BBN `ΔN_eff`, equivalently `Y_p`).

**Why the record thought β was a hole.** "PPN-invisible" was read as "invisible". β is invisible to every *static*
observable because θ ≡ 0 statically — a structural accident of this action, not a property of β. The one place θ ≠ 0
in a way we have already measured is the expansion of the universe, and there β is not a free parameter at all: it is
the ratio of the two gravitational couplings the theory possesses.

**Parameter count.** A33 lists four free numbers `(κ, β, η, γ)`. After this lane: `β = (2G/G_eff − 2)/3` is *measured*
by the background normalisation, so the free list is `(κ, η, γ)` plus `Λ_bare`. β leaves the ledger.

---

## 5. Checks and mutations

`a78_checks.py`, 30 checks, 0.56 s, stdlib + sympy/scipy, exit 0 iff all pass. Each check compares two independently
computed numbers (two variations, two eliminations, a closed form vs a root-find, theory vs the record's formula).

```
C01_FRW      H^2 from the full ADM density vs the reduced ansatz        0
C02_FRW2     A(2Hdot+3H^2)=2Lambda along the solution of F1             1.0000000000
C03_GEFF     G_eff/G_N from Friedmann vs G_N=K/4pi from the static Poisson   1.00000000
C03b_GEFF    G_eff/G_N at beta=0.027 vs 1 (BBN 5%)                      0.96107641
C04_K16      beta(Lambda_bare=Lambda_obs,H0): closed form vs brentq      -0.210799756681
C05_LAM0     Lambda_bare(beta=0)/Lambda_obs vs 1                        1.0000000000
C06_STAB     sign(beta) vs sign(Lambda_bare-Lambda_obs), 5 points       all match
C07_THETA    theta on the static ansatz vs 0                            0
C08_BTERM    (1+beta)theta^2 N sqrt h/(4K) static vs 0                  0
C09_SHARP    same with N^i != 0: must be NON-zero                       8.014e-02
C10_DSDB     d/dbeta of the static action density vs 0                  0
C11_LAW      g_N = g - xi u vs g^2/(g+a0) at xi=1                       0
C12_AQUAL    the action's first integral g-u(g) vs g mu(g/a0)           0
C13_ALPHA1   alpha_1(1AU) from L* vs from r^2K/gamma                    8.161261e-14
C14_TTTHETA  O(eps) coefficient of theta for a TT mode vs 0             0
C15_CT2      c_T^2 = <-R3>/<K^2> vs 1                                    1.000000000000
C16_TTBETA   dS_TT/dbeta vs 0                                           0
C17_B        B from the action vs K(2+3beta)/beta at beta=1             5.000000000000
C18_Z_b1/b3  Z from the action vs A68's K(2+3b)/b + eta p^2             5.4900000000 / 4.1566666667
C19_ZSIGN    sign(Z) vs sign(beta), 7 points                            all match
C20_RATIO    omega^2(1)/omega^2(3) vs record B(3)/B(1)                  0.733333333333
C22_UVSPEED  c_s^2(UV) vs gamma/eta                                     1.0000000000
C23_DET      det M symbolic vs numerical                                4.000000000000
C24_IDENT    (Omega,chi,lam) vs (1,1,1)                                 0
C26_SHIFT2   |dL| ratio on halving eps vs 4                             4.000000415
C27_XI       law deformation at xi=1 vs 0                               0
C28_SMAT     omega^2 invariance under lambda=0.3,1,7                    1 + 2.2e-16
C29_BBN      Delta N_eff at beta_max vs -0.30                           -0.300000000000
C30_BARE     slope dLambda_bare/dbeta vs (9/2)H0^2                      1.000000000000
```

Eleven mutations, each one input, each exit 1: `beta_sign`, `no_theta2`, `clock_xi`, `Z_eta`, `tt_beta`, `G_factor`,
`static_shift`, `frw_ansatz`, `gamma_factor2`, `W_quad`, `tt_trace`. Coverage, per-mutation failing checks, exact exit
codes and the three identity checks that no single-input mutation can separate are in `MUTATE.md`.

---

## 6. What this does not do

* **The BBN bound is a bound, not a derivation.** β < 0.0280 assumes standard BBN and `|ΔN_eff| < 0.30`; a different
  `ΔN_eff` prior moves the number linearly (`ΔN_eff = −11.1738 β`). The *structure* — `G_cosmo/G_N = 2/(2+3β)` — is
  derived exactly and is prior-independent.
* **Whether the theory survives BBN at all is a separate question.** With `β = O(1)` it does not (`ΔN_eff = −4.47` at
  β = 1). The lane reports this as a measurement of β, not as a consistency claim about the cold sector, which also
  contributes to `ρ` at BBN and is not modelled here.
* **The α₁/α₂/β_PPN invisibility is proven for the static sector**; the boost argument that turns the static solution
  into the PPN metric is A54/A22's and is not re-derived. What is new is that the *static action itself* has identically
  zero β-derivative, so no static functional of it can carry β.
* **The m_T² value is A54's**, not re-derived; only its β-independence is proven.
* **`Λ_bare` is not derived.** This is the whole of what remains, and §3 says so explicitly.
* **The fifth mode's dispersion is an on-shell β-channel that is not observable** — the mode decouples (loop factor
  ≤ 1.9e−70, A69). The lane does not claim β is measurable there.
* **No claim about the second-order PPN metric, strong field, or the cosmological slip.**

## 7. Reproduce

```bash
cd deepseek_push/DS_FINAL_2026_10_21/A78_beta_closure
python3 a78_checks.py --json-out a78_results.json | tee a78.out     # 30/30, exit 0
A78_MUTATE=beta_sign python3 a78_checks.py; echo $?                   # 1
```
