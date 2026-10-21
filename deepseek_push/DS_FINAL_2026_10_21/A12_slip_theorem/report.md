# A12 — the slip theorem: why lensing equals dynamics in a covector sector

**Lane:** A12_slip_theorem · **Date:** 2026-10-21 · **Base:** `deepseek_push/DS_FINAL_2026_10_21/BRIEF.md`
**Script:** `a12_checks.py` (11/11 PASS, exit 0) · **Output:** `a12.out` · **Data:** `a12_results.json`

---

## Claim

For a metric theory with Einstein–Hilbert gravity, ordinary matter, and an extra sector that is a
**spatial covector** `P_i` whose Lagrangian has **≤ 2 derivatives**, **no P–curvature coupling**, and a
potential `W = W(h^{ij}P_iP_j)` alone, the Weyl ratio on static solutions is

> **Φ/Ψ = 1 + O(Ψ), i.e. Φ = Ψ identically at the post-Newtonian order at which Φ and Ψ are defined.**

The equality is *not* an accident of isotropy and *not* exact. The structural reason is that the sector is a
**charge sector, not a stress sector**: at first order in the Newtonian counting `ε ~ Ψ`, the *only* thing the
sector contributes to the gravitational equations is the divergence `D·P` (the lapse source of the clock
operator `P^iD_i ln N`), while **every** ≤2-derivative operator's traceless spatial stress is `O(ε²)`
(Table 1). A sector whose leading-order content is a charge density has `T^TF_ij = 0` at leading order — it
gravitates as **dust** — and dust has no anisotropic stress, so no slip. The first nonzero slip is second
order: `1 − Φ/Ψ = O(Ψ) = O(v²/c²) ≈ 3×10⁻⁷` for a galaxy, `≈ 10⁻⁹` at Saturn. The general breaker is any term
that gives the sector an `O(ε)` traceless stress, which inside the class is impossible: it requires an extra
scale (a condensate VEV or a Proca mass), a P–curvature coupling, or **removal of the clock operator** — and
without the clock operator the density *is* the stress and the slip is `O(1)` (the Janis–Newman–Winicour
class, `|Π/σ| = 2`).

---

## Theorem box

**Hypotheses.**
- **(H1)** Static spacetime, `ds² = −N²dt² + h_ij dx^i dx^j`, `h_ij = f δ_ij`; ordinary matter with
  `T^TF_ij(matter) = 0`; Einstein–Hilbert gravitational sector with `K = 4πG`.
- **(H2)** Extra sector: spatial covector `P_μ` (`n^μP_μ = 0`), Lagrangian density `√h N L` built from
  `P, N, h_ij` with **≤ 2 derivatives**, **no P–curvature coupling** (no `R_ijP^iP^j`, `RP²`, `R_μνP^μP^ν`).
- **(H3)** `W = W(h^{ij}P_iP_j)` only, with `W(0) = W′(0) = 0` (asymptotic flatness: `g = K W′(u) → 0`).
- **(H4)** The static solution is on the **clock-aligned branch**: the P equation is solved by
  `P ∥ D ln N`, with `u ≡ K|P| < a₀` (cap unsaturated).
- **(H5)** No independent dimensionful scale in the sector other than `a₀`: `|P|` is *slaved* to `∇ln N`
  (no condensate VEV, no mass term with a hierarchy `m² ≫ a₀/K`).

**Statement.** On any solution of (H1)–(H5),
`T^t_t(P) = O(ε)`, `T^i_j(P) = O(ε²)`, hence
`(∂_i∂_j − ⅓δ_ij∇²)(Φ−Ψ) = O(ε²)` and

  **Φ − Ψ = O(ε²) = O(Ψ)·Ψ, i.e. (Φ − Ψ)/Ψ = O(Ψ) = O(v²/c²).**

**Proof sketch.**
1. *Slip lemma* (exact, no approximation): `G^i_j − ⅓δ^i_jG^k_k = (∂^i∂_j − ⅓δ^i_j∇²)(Φ−Ψ)` (K1), and
   `G^t_t = −2∇²Φ` (K2). So `Φ = Ψ ⟺ T^TF_ij(P) = 0`. This is the whole content of "no slip".
2. *χ-machinery.* Expand `h_ij = f[δ_ij + χ(n_in_j − ⅓δ_ij)]` — the radial-vs-tangential trace-free mode,
   which is precisely the mode whose equation of motion *is* the slip equation. Since `tr T = 0`, `√h N` is
   χ-independent at first order and `dS/dχ = −⅓∫√h N Π` gives
   **`Π_O ≡ T^r_r − T^θ_θ = −3 ∂L_O/∂χ`** for every operator (verified as a functional identity).
3. *Classification* (Table 1). Every nontrivial ≤2-derivative operator carries `Π_O ≠ 0`; only `F_ijF^ij`
   and `E_iE^i` are inert on a static radial background, and total derivatives are inert by construction.
4. *Scaling.* Under `N = 1+ε n₁`, `f = 1+ε h₁`, `P = ε p₁`, every `Π_O` is `O(ε²)` (K5) because each is a
   product of two first-order objects (`P ~ ε`, `∂lnN ~ ε`, `∂P ~ ε`). **Exactly one** operator has a lapse
   source at `O(ε)`: the clock `P^iD_i ln N`, whose source is `σ_clock = −D·P`.
5. Therefore at `O(ε)` the sector's stress is `diag(−ρ_P, 0, 0, 0)` — dust. Its traceless part vanishes
   identically, and by the slip lemma `Φ = Ψ` at that order. The first nonzero slip is `O(ε²)`.

**Counterexample (shows the hypotheses have content).** Drop the clock operator:
`L_P = −W(|P|)` with `P_i = ∂_iφ`. Then `ρ = W` and `Π = −uW′ = −2W` are the **same** order,
`|Π/σ| = 2` (K8) → `Φ ≠ Ψ` at `O(1)`. This is exactly the static-scalar (Janis–Newman–Winicour) class:
a static gradient has `p_r − p_t = (φ′)² ≠ 0` and `γ_PPN ≠ 1`. Two further breakers: a Proca mass
`m²|P|²/2` with `m² ≫ 1/(G M)`, and a P-condensate with `|P| = v` fixed by the potential rather than by
`∇ln N`. **In the class as stated, no operator produces `O(ε)` stress** — that is the theorem's content.

---

## Derivation

**(1) Metric and potentials.** `ds² = −(1+2Ψ)dt² + (1−2Φ)δ_ij dx^i dx^j`; `K = 4πG` (round-2
normalization: `R3/(4K)`, `G^t_t = 2K T^t_t`).

**(2) Slip lemma (exact linearized identity).**
`G^i_j − ⅓δ^i_jG^k_k = (∂^i∂_j − ⅓δ^i_j∇²)(Φ−Ψ)`, `G^t_t = −2∇²Φ`, `G^k_k = 2∇²(Ψ−Φ)`.
With `G^μ_ν = 2K T^μ_ν`:
`(∂_i∂_j − ⅓δ_ij∇²)(Φ−Ψ) = 2K[T^i_j − ⅓δ^i_jT^k_k]`. **(E1)**

**(3) Spherical first integral.** For `f ≡ Φ−Ψ`, `(∂_r² − ⅓∇²)f = (2/3)(f″ − f′/r)`, so (E1) gives
`f″ − f′/r = 2KΠ`, `Π ≡ T^r_r − T^θ_θ`. Then `(f′/r)′ = 2KΠ/r` and **asymptotic flatness** (the
homogeneous mode is `Ar²`) fixes

  `(Φ−Ψ)′(r) = −2K r ∫_r^∞ Π(r′)/r′ dr′`. **(E2)**

The sign of the homogeneous mode matters: integrating *outward from zero* instead picks the growing `r²`
branch and over-estimates the slip by many orders of magnitude (a growing `r²` mode).

**(4) Stress from the shear mode.** With `h_ij = f[δ_ij + χT_ij]`, `T_ij = n_in_j − ⅓δ_ij`,
`dS/dχ = −⅓∫d³x√hN Π` ⇒ `Π = −3∂L/∂χ`. This gives, at `f → 1`:
`Π_W = −uW′`, `Π_clock = +2PN′ = 2ug/K`, `Π_d² = −2γ(D·P)²`, `Π_shear = −(4γ_s/3)(A−B)²`.

**(5) The framework's branch.** The round-2 action is
`L/(N√h) = [R3 + K_ijK^ij − (1+β)θ² − 2Λ]/(4K) + P^iD_i lnN − W_full(u) + ηE²/2 − γd²/2 − γF²/4`,
`W_full = (a₀²/K)[−u/a₀ − ln(1−u/a₀)]`, `u = K|P|`. Its P equation on the gradient branch (`F = 0`,
`E = 0`) is `∂_i ln N = W′K²P_i/u`, hence `g ≡ |∇ln N| = K W′(u)`. With
`K W_full′ = a₀u/(a₀−u)`, `g_N ≡ g − u = u²/(a₀−u)`, so `g² = g_N(g+a₀)` — **the canonical law** (K10).
Its lapse equation gives `∇²Φ = K(ρ_m + W + D·P + ½γ(D·P)²)`, so the sector's `O(ε)` source is the **charge**
`σ = −D·P`. Combining the two stress terms: `Π_net = −uW′ + 2uW′ = +uW′`, and for `u ∝ 1/r`,
`D·P = u/(Kr)`, so

  `|Π_net/σ| = K r W′ = r g = Ψ`. **(E3)**

An exact dimensionless identity: the traceless stress is the charge times the local potential depth.

**(6) Numbers** (declared model: `M_bar = 5×10¹⁰ M_⊙`, Hernquist `a = 3 kpc`, `a₀ = 9.36×10⁻¹¹`):

| r | g_N | g | Ψ = gr/c² | g_lens/g_dyn − 1 | \|1−Φ/Ψ\| |
|---|---|---|---|---|---|
| 10 kpc | 4.12e−11 | 8.61e−11 | 2.95e−7 | −9.13e−8 | 2.6e−7 |
| 100 kpc | 6.57e−13 | 8.18e−12 | 2.81e−7 | −1.32e−7 | 2.6e−7 |

**(7) The most general breaker.** A term whose second metric variation is **linear** in `P`. With no other
field and no other scale in the sector, the only such operator at ≤2 derivatives is the clock term — and its
stress is `O(ε²)` because its metric variation brings down a second first-order factor (`P` or `∂lnN`).
Hence the class is uniformly slip-free at `O(ε)`. Concretely, `Φ=Ψ` is broken at `O(1)` only by:
`ξR_ijP^iP^j` (breaks H2), a mass/condensate scale `m² ≫ a₀/K` (breaks H5), a direct `P·J_matter` coupling,
or deletion of the clock term (breaks H4; K8).

---

## Status

**CLOSED-DERIVED** (positive theorem, with H1–H5 explicit) **+ CLOSED-NO-GO** for the negative half:
within the ≤2-derivative, no-curvature-coupling, single-scale class **no operator produces `O(1)` slip**.
The equality `Φ = Ψ` is therefore structural at post-Newtonian order, not a fine-tuning; and it is *not*
exact — the leading violation is `O(Ψ)`.

*Framework (task 3).* The round-2 action **falls in the class**: (H2) holds (the `R3` term is pure gravity,
not `P`-contracted), (H3) holds exactly (`W = W(|P|)`), and (H4) is *derived*, not assumed, from its own P
equation. Extra hypotheses it needs to be named explicitly: (i) the solution sits on the **gradient branch**
`F = 0, E = 0` (static); (ii) the `γ = K L*²/2` terms are negligible outside the screening core; (iii) the
cap `u < a₀` is unsaturated (`W′ → ∞` at `u = a₀`); (iv) `W′(0) = 0` so that `g → 0` at large `r`.
Under those, the framework predicts `1 − Φ/Ψ ≈ −Ψ`, i.e. `≈ 3×10⁻⁷` in a galaxy.

---

## Checks (`a12_checks.py`, 11/11 PASS, exit 0)

| id | what it proves | measured |
|---|---|---|
| K1 | (E1) on components (11),(22),(12) — exact symbolic identity | residual 0 |
| K2 | `G^t_t = −2∇²Φ` (fixes `K = 4πG`) | residual 0 |
| K3 | (E2) solves `(2/3)(f″−f′/r) = 2KΠ` on 5 power-law Π | 5/5 zero |
| K4 | classification: 6 of 9 operators carry `Π ≠ 0`; `F²`,`E²`,tot.div. inert | 6/9 |
| K5 | every `Π_O` is `O(ε²)`; **exactly one** `O(ε)` lapse source (clock) | 1 charge op |
| K6 | framework identity (E3): `\|Π/σ\| = rg = Ψ` | exact |
| K7 | integrated Hernquist+MOND profile, asymptotically flat | `2.63e−7` |
| K8 | counterexample without clock: `\|Π/σ\| = 2` → `O(1)` slip | 2.000 |
| K9 | KiDS-1000 vs dynamical RAR: constant slip exactly degenerate | `Δχ²(1%)=1.4e−14` |
| K10 | the round-2 gradient branch *is* `g_N = g²/(g+a₀)` | residual 0 |
| K11 | mutation: dropping the clock stress must break K6 | K6 FAIL as designed |

**Table 1 — operator classification** (`Π_O` from the χ-machinery; `ε`-power under
`N=1+εn₁, f=1+εh₁, P=εp₁`):

| operator | `Π_O` | `Π` pow | `σ` pow (lapse source) | slip |
|---|---|---|---|---|
| `W(\|P\|)` | `−uW′` | 2 | 2 | sources, but `O(ε²)` |
| `P^iD_i ln N` (clock) | `+2PN′/f` | 2 | **1** | **charge; the protector** |
| `(D·P)²` | `−2γ(D·P)²` | 2 | 2 | `O(ε²)` |
| `F_ijF^ij` | 0 (radial P) | — | — | inert statically |
| `(P·DlnN)²` | `−4(PN′/N)²/f²` | 4 | 4 | `O(ε⁴)` |
| `(D_iu)(D^iu)` | `−K²γ(P′−Pf′/2f)²/f²` | 2 | — | `O(ε²)` |
| `(D_(iP_j))_TF²` | `−(4γ_s/3)(A−B)²` | 2 | 2 | `O(ε²)` |
| `E_iE^i` | 0 (static) | — | — | inert statically |
| `D_i(P^iD·P)` | 0 | — | — | total derivative |

---

## Observational discriminator (task 4)

**Which dataset on disk.** `real_research/data/lensing_rar/brouwer2021_rar/`
— the KiDS-1000 excess-surface-density RAR (Brouwer et al. 2021, Fig. 4/5 C1 isolated lenses,
15 bins + full 15×15 covariance), converted with `g_lens = 2πG·ESD`, compared against the **dynamical**
RAR at the same `g_bar` (SPARC rotmods; here the canonical law `g_dyn = (g_bar/2)(1+√(1+4a₀/g_bar))`).

**A 1% slip is not detectable with it — and the reason is structural, not statistical.** A constant slip
enters as `g_lens = A·g_dyn·(1 − s/2)`, which is **exactly degenerate** with the baryonic normalisation `A`:
`A(1−s/2)` is one number. Profiling `A`, `Δχ²(1% slip) = 1.4×10⁻¹⁴` (K9). The same degeneracy is why the
record carries the `+0.355 dex` (2.26×) amplitude offset as "free dust" rather than as a slip
(`G073`, `G089`). Any galaxy-scale lensing-vs-dynamics test therefore measures the *shape* of the slip,
never a constant amplitude.

**The record's actual bound on `1 − Φ/Ψ`.** The tight one is Solar-System PPN:
`γ − 1 = (1.7 ± 1.6)×10⁻⁴` (Biskupek, Müller & Torre 2021, LLR; quoted in
`prep_2026/planetary_doors/BOUNDS.md`), i.e. `|1 − Φ/Ψ| < 4.9×10⁻⁴` at 2σ; the classic Cassini value is
`2.3×10⁻⁵` (Bertotti et al. 2003, labelled external). Predicted: `2.6×10⁻⁷` at 10–100 kpc and
`1.0×10⁻⁹` at Saturn's orbit — 1.9 and 3.3 orders below the Cassini and LLR bounds respectively. **The framework is safe: the prediction sits 87× below Cassini and 1860× below the record's LLR
bound, while a 1% slip is already excluded by Cassini alone at 435×**, so any future detection of slip at
the 1% level kills this class regardless of galaxies.

---

## What this does not do

- It does not prove the equality nonlinearly. `Φ = Ψ` holds at `O(ε)`; the `O(ε²)` piece is computed, not
  cancelled. An exact statement would need the second-order metric, which is not derived here.
- It does not solve the full nonlinear static system numerically (β, η, γ arbitrary); the branch is assumed
  regular, with `F = 0`, `E = 0`, cap unsaturated. Global existence/uniqueness of the gradient branch is not
  established.
- `E_iE^i` is inert *statically* only. Cosmological/perturbed slip (the `ηE²` kinetic term active, `P̄`
  evolving) is **not** covered; the theorem says nothing about the cosmological slip parameter.
- The `γ = KL*²/2` terms contribute `O(ε²)` and are dropped outside the core; inside a screening core they
  can be larger and the estimate degrades there.
- K9 shows the KiDS comparison cannot bound a **constant** slip; it does not exclude a *shaped* slip
  (`s(r)` or `s(g_bar)`), which is the statistic a future test should use.
- `(D·P)²`'s fixed-P traceless stress is a total divergence on shell (its weighted integral vanishes by the
  P equation); the table reports the local stress, and the integrated slip from that operator alone is not
  separately bounded here.

## Next

1. Compute the **cosmological** slip for this action (the `E²` term and evolving `P̄` are active there) —
   that is the only regime where the `O(ε)` protection can fail without leaving the class.
2. Replace the constant-slip test with a **shape** statistic on the Brouwer covariance: fit `s(g_bar)` in two
   or three acceleration bins with the amplitude marginalised; that is the only galaxy-scale route with
   sensitivity.
3. Solve the exact static system for `(N, f, P)` at fixed `(β, η, γ)` and measure `f − (2−N²)` directly, to
   confirm the `O(Ψ)` residual beyond linear order.
4. Fold `(Φ−Ψ)/Ψ = −Ψ` into `G073`'s "phantom floor" as a stated `10⁻⁷` correction (it is currently assumed,
   not derived) — this lane supplies the derivation.
