# L54 — the repair survives the Dirac count, the count stays at four, and κ turns out not to be free

2026-09-09. Lane L54 of [CHARTER.md](CHARTER.md), doing the one calculation
[L52_MARGINAL_SWEEP.md](L52_MARGINAL_SWEEP.md) named and deliberately did not do:
*"a full Dirac constraint analysis of the (g, τ, φ, W) system has **not** been done and would be the next
step before it is claimed as a completed repair."*
Script: [L54_repair_constraints.py](L54_repair_constraints.py) → [L54_repair_constraints.out](L54_repair_constraints.out).
**73 checks, 73 PASS, exit 0.**

Method: the Dirac counter is written here and **runs the algorithm** rather than evaluating a formula on
hand-supplied numbers — the quadratic Lagrangian of each theory is built from its own action, the null
vectors of the velocity Hessian *are* the primary constraints, the consistency algorithm generates the
rest, and first/second class is decided by the **rank of `A J Aᵀ`**. Nothing under
`closure_2026/integrable_clock_construction_2026/` was imported, run or read for this. `L46_mode_floor.py`
and `L52_marginal_sweep.py` were not imported either; five of L52's numbers are recomputed from scratch
and compared only at the end of each control. Polarity: every check asserts a **statement** and PASS means
the statement is true — so a PASS on `D7` is a *negative* result for the repair and a PASS on `B2` is a
*positive* one. Each line says which. Both footings, **9.3619×10⁻¹¹ / 1.1279×10⁻¹⁰ m s⁻²**, on every
dimensional number.

---

## The short answer, in three sentences

**The repair survives: the mode count is four, by an algorithm that returns 2 / 3 / 5 / 3 on ADM general
relativity, GR + a scalar, Einstein-aether and khronometric theory, and the auxiliary contributes exactly
three second-class pairs — three new coordinates in, six phase-space dimensions removed, net zero.**
**The risk L52 named does not fire where the theory lives: the auxiliary's Hessian degenerates on the
surface `Δ′(s) = −κ` and nowhere else, which is empty for the published flat splice (where `Δ′ ≥ 0`) and
for the deposited C-family (where `Δ′ > 0` analytically), and the negative control confirms that if it
*did* degenerate the count would fall to three — `W_z` becoming a multiplier that deletes the very mode it
was added to repair.** **But the repair is not free the way L52 priced it: `κ` was treated as bounded only
from below, and it is bounded from **above** — at about **1.6 × 10⁻⁶** by gravitational Cherenkov and about
**3.1 × 10⁻⁴ / 7.0 × 10⁻⁴** by the screened Saturn phantom-mass row — which kills L52's `κ = 10⁻², 10⁻¹`
rows and, with the `κ ≥ 0.0324` that the ν_RAR arm would need, closes that arm by a pincer rather than by
the qualitative argument L52 gave.

---

## 1. Controls — the counter has to earn the right to be believed

`A1–A6b`, all mandatory, all PASS:

| control | required | returned | structure the algorithm found |
|---|---|---|---|
| ADM general relativity | 2 | **2** | N_q = 10, 4 primary + 4 secondary, **all 8 first class**, 0 second class |
| GR + one minimally coupled scalar | 3 | **3** | N_q = 11, same 8 first class |
| Einstein-aether | 5 | **5** | N_q = 13, same 8 first class (`c₁…c₄ = 1/5, 1/7, 1/11, 1/13`) |
| khronometric | 3 | **3** | N_q = 11, same 8 first class |

`A4b`: the machinery *sees* why — the only change from Einstein-aether to khronometric is that `u_i` is a
gradient, and exactly the spin-1 pair disappears (5 − 3 = 2). `A4c`: the count is `k`-independent.

Two **speed** controls, because a degeneracy count can be right while the sign conventions are wrong
(`A5`, `A6`): the tensor speed comes out as Jacobson's `c_T² = 1/(1 − c₁₃)` and the khronometric spin-0 as
Blas–Pujolàs–Sibiryakov's `(2 − c₁₄)c₂/[c₁₄(2 + 3c₂)]`, both exactly in rationals. `A6b`: a **second,
independent counter** — the determinantal divisor of the Euler-Lagrange operator, with no gauge fixing and
nothing eliminated — returns the same 3 for khronometric.

**L52's own numbers, recomputed here** (`A7–A11b`):

| quantity | L54 (rebuilt) | L52 |
|---|---|---|
| ν_RAR interior maximum `s_sat`, ceiling `C` | 2.5396383, 0.64761024 | 2.5396, 0.64761 |
| `min Δ′` on raw ν_RAR | **−0.0323806** | −0.0324 |
| `1/Δ′` at Saturn, C-family, canonical / alt | **9.61731×10¹⁵ / 5.75919×10¹⁵** | 9.617e15 / 5.759e15 |
| L44's parallel Schur `a_UV` at `D = 0.13`, `q = −1.29078` | **0.0173858743518** | 0.01738587435 |
| the series Schur, symbolically | `f_eff″ = 2Λf″/(f″ + 2Λ)` | same |

One correction fell out of the last row and is reported rather than inherited (`A11b`): **L52's `E3` says
`κ = 1/(2λ)`, which is inconsistent with L52's own `D2` by a factor of two** — `D2`'s harmonic rule
`1/Σ_eff = 1/Σ + 1/λ` gives `κ = 1/λ`. It is a bookkeeping slip in the translation between the spring
constant and the compliance; the cap `1/κ`, the `Σ_eff` table and every structural statement in L52's E3
and F are unaffected. This lane carries `κ` itself as the parameter, so nothing below depends on it.

---

## 2. The count, with the arithmetic

The system counted is the deposited action of `THE_COMPLETE_THEORY_2026-09-08.md` §2 with

    − (2 − K_B) J( Y + ξ²|∇⊥V|² )   replaced by   − (2 − K_B)[ J( W·W + ξ²|∇⊥V|² ) + Λ (V − W)·(V − W) ]

`W_μ = q_μ^ν W_ν` spatial, **no derivatives on W**, `Λ = 1/κ`. Perturbations about flat space, one Fourier
mode with `k` along `z`, `Q₀ = 0` (the condensate is removed, as the deposited theory requires).

```
  canonical pairs        N_q                = 15    (10 metric + 1 clock chi + 1 MOND scalar phi + 3 auxiliary W_i)
  phase-space dimension  2 N_q              = 30
  rank of the velocity Hessian              = 8     (so 7 primary constraints)
  primary constraints                       = 7     (pi_n, pi_nu_x, pi_nu_y, pi_nu_z, pi_W_x, pi_W_y, pi_W_z)
  constraint generations                    = [7, 7]
  total independent constraints             = 14
  FIRST class   n_1                         = 8     (4 lapse/shift momenta + Hamiltonian and 3 momentum constraints)
  SECOND class  n_2                         = 6     (3 pairs: pi_W_i and the algebraic W_i equations)

  DOF = (2 N_q - n_2 - 2 n_1)/2 = (30 - 6 - 16)/2 = 8/2 = 4
```

`B2`, `B2b`, `B2c`. The classification is **the rank of `A J Aᵀ`** on the constraint set the algorithm
itself produced, not an inspection. The unrepaired action returns `(24 − 0 − 16)/2 = 4` with the same eight
first-class constraints (`B1`), so the comparison is like for like: **Δ(2N_q) = +6 and Δ(n₂) = +6, and the
mode cost is exactly zero.**

Robustness (`B3`–`B3e`): 4 at 18 parameter points spanning three `K_B`, five orders of `Λ` and both signs of
`K₂`; 4 at `k = 3`; 4 at `ξ = 0` (so the coherence operator adds no Ostrogradsky mode alongside the
auxiliary); 4 with the `(∂_zχ)(φ̇)` coupling a non-zero background gradient switches on — a term the
*unrepaired* action carries too, so it cannot distinguish them; and 4 at both extremes of the real theory,
`σ_∥ = σ_⊥ = 0` exactly (a zero of the background gradient) and `σ_∥ = 10¹⁶` (the saturated branch).

`B6`: the **independent** counter agrees — 2 tensor + 0 vector + 2 scalar = 4 — and `W_x, W_y, W_z` appear
in **no** sector's dispersion polynomial at all, which is the same fact the second-class pairs express.

### The negative controls, which is where a mode count is usually wrong

* `B4` — give the same auxiliary a kinetic term and the count goes to **7**. "Holonomic" is the entire
  mode-count budget, and the machinery detects the difference.
* `B5`/`B5b` — set the **longitudinal** Hessian entry to zero (`σ_∥ + Λ = 0`) and the count falls to **3**:
  the generations become `[7, 7, 1]`, one constraint turns first class, and the mode that dies is the
  **MOND scalar** — `W_z` becomes a Lagrange multiplier enforcing `∂_zφ = 0`. This is exactly the failure
  mode L52 named, exhibited.
* `B5c` — a degenerate **transverse** entry does *not* change the count (`W_x, W_y` simply drop out of the
  Lagrangian and their momenta go first class, removing `2 × (2 − 2)/2 = 0`). **Only the longitudinal entry
  is dangerous**, which is worth knowing because the transverse stiffness is the one that vanishes at every
  symmetry centre.

---

## 3. Where the auxiliary's Hessian can degenerate — solved, not scanned

`C1` derives the Hessian rather than quoting it: with `f(w) = J(w·w)`, `f″(w) = 2J_Y + 4J_YY w² = 2σ_∥`,
the auxiliary's own Hessian is `f″ + 2Λ = 2(σ_∥ + Λ)`.

`C1b` — **the condition is one-sided.** The elimination `w(v)` exists and is single-valued iff
`dv/dw = 1 + f″/(2Λ)` never vanishes, i.e. iff `σ_∥ > −Λ`. So an **infinite** `σ_∥` is harmless (`dv/dw → ∞`,
the map is still strictly increasing) and only a sufficiently *negative* one is fatal. That matters: on the
published flat splice `σ_∥ = +∞` on the whole saturated branch, and the map `w ↦ v` still has a corner but
stays monotone. **Elimination needs monotonicity, not `C²`.**

`C1c` — **the degeneracy locus, exactly.** With the deposited theory's own identity `σ_∥ = 1/Δ′(s)` (§4.1)
and `κ = 1/Λ`:

```
    Hessian degenerate   <=>   sigma_par + Lambda = 0   <=>   Delta'(s) = -kappa   <=>   Delta_eff'(s) = 0
```

The repair therefore **cannot hide its own failure**: wherever the auxiliary stops being eliminable, the
repaired stiffness `Σ_eff = 1/(Δ′ + κ)` is simultaneously infinite. There is no silent degeneracy.

| kernel | min Δ′ over `s ∈ [10⁻⁸, 10¹²]` | degenerates for |
|---|---|---|
| published flat splice (ν_RAR then held flat) | **0** | never — `Δ′ ≥ 0` everywhere |
| **deposited C-family** (§4.3, the kernel carried) | **1.15×10⁻³³** | never — and this is analytic (`C3b`) |
| raw ν_RAR (the other arm of §4.4's open fork) | **−0.0323806** | every `κ ≤ 0.0324` |

`C3b` proves the C-family case symbolically rather than by sampling: `dΔ_C/ds = Cp W^{−p−1}(a₁ + 2a₂u)/(2u)`
with every factor positive, so it has **no zero on `0 < s < ∞`** for any positive `(C, p, a₁, a₂)`.

The four places the question names, at `κ = 10⁻⁶` (`C5`, `C6`):

| background | `s` | `σ_∥ = 1/Δ′` | Hessian `σ_∥ + Λ` |
|---|---|---|---|
| deep-MOND limit, `s → 0` | 10⁻⁸ | 2.00×10⁻⁴ | 1.0×10⁶ |
| MOND transition | 1 | 11.07 | 1.00×10⁶ |
| saturation onset | 2.5396 | 53.89 | 1.00×10⁶ |
| galaxy core / Saturn's orbit | 6.96×10⁵ | 9.617×10¹⁵ | 9.617×10¹⁵ |
| Cassini conjunction | 1.14×10¹² | 1.243×10³³ | 1.243×10³³ |

Strictly positive at every one, on both footings, with no cancellation anywhere. At a **zero of the
background gradient** — every symmetry centre, every MOND saddle including the Solar System's own — the
longitudinal entry is not the operative one (`σ_∥ → 0` there, because `Δ′ → ∞`) and the transverse entry
`σ_⊥ = s/Δ(s) → 0` like `√s`; both leave the Hessian at `Λ = 1/κ > 0`. **The repair is safest at exactly
the backgrounds where L52's C-L2 marginality lives.**

`C7` **refines L52's E3e**, which said only that the repair "fails for the raw decreasing ν_RAR". The exact
statement is a threshold: the repair **convexifies ν_RAR** and the auxiliary stays eliminable for every
`κ > 0.0324`. Whether that `κ` is affordable is a separate question — §5 answers it, and the answer is no.

---

## 4. The gates

**Nothing in the clock sector moves, and this is verified rather than argued.** `D1` compares the
11 × 11 metric-and-clock block of *both* the velocity Hessian and the gradient Hessian, entry by entry, with
and without the auxiliary: identical. So `c_T`, `α₁`, `α₂`, `α₃` and the clock's own kinetic normalisation
cannot move. `D1b`: `c_T = c` exactly, computed from the repaired action's own tensor block. `D2`: the
clock-tachyon gate is satisfied identically because `Q₀ = 0`, and the added term contains **no `Q` at all** —
`V_μ = q_μ^ν∂_νφ` is orthogonal to `n` by construction, which is also why `W` has no velocity anywhere in
the Hessian (`D2b`) and hence why its momenta are primary constraints in the first place.

`D3`: PPN `γ` and the no-slip result survive because they were proved for a **generic `J`**, and `J_eff` is a
*better-behaved* member of the same class — strictly convex (`f_eff″ = 2/(Δ′ + κ) > 0`) and `C¹` with a
**bounded** second derivative where `J` itself has an infinite one. `D3b`: the one PPN-adjacent thing `κ`
does is rescale `G` by `(1 + κ)`, which shifts no dimensionless PPN parameter.

### Two rows improve

`D4` — **L33's D2 FAIL is removed.** Its statement was: *"the longitudinal sector is not strongly
hyperbolic; `Δ′ = 0` identically at every Solar-System background so the longitudinal speed is infinite;
the sector degenerates into an elliptic constraint solved with boundary conditions at infinity."* The
repaired principal symbol is `(2 − K_B)/(Δ′ + κ)` — finite and strictly positive — so the Cauchy problem
regains a finite domain of dependence in the longitudinal direction. `D4b`: the deposited *Hadamard* row
(`S₄ > 0` at 59/59 branch points) is a clock-sector quantity and does not move. `D4c`, stated because it is
not fixed: L33's D4, the unbounded ultraviolet group velocity from the `ξ²` operator, is untouched.

`D4d` is a control on the cone formula itself — L33's published Saturn transverse cone reproduces on both
footings at both of its `|K₂|` values (mine 1.967/1.792 and 3.11/2.834 against 1.96/1.78 and 3.10/2.82).
`D4e` records a documentation discrepancy found in passing and not load-bearing: **`THE_COMPLETE_THEORY`
§4.3's "the corresponding longitudinal cone is ~10¹⁰c" is the *square* of the cone**; the identity gives
`c_∥² = 1.77×10¹⁰` and `c_∥ = 1.33×10⁵ c` at the exhibited point.

`D5` — the cones at Saturn, both footings, `κ = 10⁻⁶`:

| `\|K₂\|` | footing | `c_∥` before | `c_∥` after | `c_⊥` before | `c_⊥` after |
|---|---|---|---|---|---|
| 1.087×10⁶ (L52's operative) | canonical | 1.297×10⁵ | **1.322** | 1.371 | **0.952** |
| 1.087×10⁶ | alt | 1.003×10⁵ | **1.322** | 1.249 | **0.908** |
| 5×10⁵ (L33's) | can / alt | 1.86×10⁵ / 1.44×10⁵ | 1.897 | 1.967 / 1.792 | 1.366 / 1.303 |

`D5b` — and this **breaks L33's F2 no-go**, which said the ephemerides *force* the cone open at ≥ 182 at
Saturn, because subluminality needs a scalar force `g_φ ≥ (2−K_B)g_N/|K₂| = 1.14×10⁻¹⁰ m s⁻²`, exceeding the
anomalous-sunward bound by 3.3×10⁴. **The `κ` force is exactly Newtonian in shape, so it is not an anomalous
sunward acceleration at all** — it is absorbed into `GM_⊙`. F2's hypothesis fails. Precisely: at
`κ = 10⁻⁶` the transverse cone at Saturn is `0.95 c`, subluminal, which F2 says is impossible.

### One row moves against, and it is the same fact seen from the other side

`D7` — **gravitational Cherenkov.** L33's E2 passes this gate by "there is no emission channel into a
superluminal mode at all": the scalar is superluminal wherever `s > s_crit = C|K₂|/(2 − K_B)`, and emission
needs `v > c_s`. Under the repair `c_⊥² = (2 − K_B)s/[|K₂|(Δ + κs)]`, so the crossing moves **outward** and
above `κ_c = (2 − K_B)/|K₂|` it disappears entirely — the scalar becomes subluminal *everywhere* and the
protection is gone. Requiring L33's own worst-case `D_loss = 2(c²/a₀)/s_crit` to stay above the 10 kpc
Galactic path (its control reproduces here: `s_crit = 1.799×10⁵`, `D_loss = 1.067×10²² m` = 34.6× canonical,
28.7× alt):

| `\|K₂\|` | `K_B` | `κ_c = (2−K_B)/\|K₂\|` | κ ceiling, canonical | κ ceiling, alt |
|---|---|---|---|---|
| 1.087×10⁶ | 0.1 | 1.748×10⁻⁶ | **1.644×10⁻⁶** | **1.623×10⁻⁶** |
| 9.754×10⁵ | 0.2 | 1.845×10⁻⁶ | 1.741×10⁻⁶ | 1.720×10⁻⁶ |
| 5×10⁵ | 0.2 | 3.6×10⁻⁶ | 3.496×10⁻⁶ | 3.475×10⁻⁶ |
| 2×10⁵ | 0.2 | 9.0×10⁻⁶ | 8.896×10⁻⁶ | 8.875×10⁻⁶ |

`D7b`, and it must travel with the number: **this ceiling is soft.** L33's E4 names two suppressions it
deliberately omitted, both of which lengthen `D_loss` (the `1/J_Y` screening in the emitting shell and the
`1/|K₂|` kinetic normalisation), and the `ξ²` operator supplies a third by making every mode below 0.1 pc
superluminal again. All three raise the ceiling. So the honest statement is `κ ≲ 1.6×10⁻⁶` *conservatively*,
with the true ceiling higher by an uncomputed factor — but it is the binding one until those are computed,
and it is the **first upper bound on `κ` anyone has computed at all.**

`D8` — a **second** ceiling, from the row the theory only passes by screening. The bare kernel is
1.4005×10⁴ / 1.6873×10⁴ over the Pitjev–Pitjeva phantom-mass bound and the `ξ²` screening brings it to
3.0×10⁻³ / 1.6×10⁻³. The repair multiplies the *unscreened* scalar force at Saturn by `(1 + κs/Δ)`. If the
screening acts as a common factor on the total scalar force — the conservative bracket — that gives

    kappa <= 3.09e-4 (canonical)   /   7.00e-4 (alt)

The opposite bracket, in which the screened response is set entirely by the `ξ²` operator and `κ` drops out,
leaves the row untouched. **Which bracket holds needs the fourth-order solve and is not done here**; the
conservative one is quoted.

### Rows that do not move

`D9`/`D9b`: the bounded-boost ceiling and its SPARC test are unchanged — the observable excess over the
baryonic gravity computed with the *measured* `G` is `g_tot − (1+κ)g_N = a₀Δ(s)`, whose supremum over 401
points across twenty decades is 0.64761 `a₀` = `C`, independent of `κ`. `Δ_eff = Δ + κs` is unbounded and
**this must be stated explicitly or the theorem reads as broken** — L52's F3, confirmed. `D10`: deep MOND
untouched (`κs/Δ` = 10⁻⁸ to 10⁻⁷ across `s ∈ [10⁻⁴, 10⁻²]` at `κ = 10⁻⁶`). `D11`: BBN, 8×10⁴ inside its
tolerance.

`D12` — **the kernel fork does not close.** The ν_RAR arm needs `κ > 0.0324` and the gates cap `κ` at
1.62×10⁻⁶ / 3.09×10⁻⁴. The two are incompatible by **2.0×10⁴×** and **105×**. L52's conclusion stands, now
for a quantitative reason — a pincer with no interior — rather than the qualitative "`Δ′ < 0` makes the
auxiliary equation multivalued".

`D13` — **the ceiling costs the repair none of its purpose.** At the largest gate-compatible
`κ = 1.62×10⁻⁶`:

| footing | `Σ_∥` at Saturn, before → after | cap `1/κ` | L34's `g_*` grows by |
|---|---|---|---|
| canonical | 9.617×10¹⁵ → **6.162×10⁵** | 6.162×10⁵ | **2.44×10²⁰×** |
| alt | 5.759×10¹⁵ → **6.162×10⁵** | 6.162×10⁵ | **8.74×10¹⁹×** |

against L34's required 552–3.8×10⁴. A19's unwritable cubic action, L34's strong coupling at every planet
and L30's gate G2 are all still discharged.

---

## 5. The ephemeris signature — verified, and the one place the verification does not reach

`E1` — L52's F1 is **correct as a statement about the force**, and it is proved here rather than inherited:
`Δ_eff − Δ = κs` means an extra acceleration `a₀κs = κg_N` at *every* `s`, not only in a limit, its
divergence vanishes identically in vacuum, so the phantom density it creates is exactly zero. `E1b`: the
degeneracy with `GM` is **exact, not approximate** — the repaired field is the Newtonian field of a source
of mass `(1+κ)M` at every radius, so a one-parameter refit of `GM_⊙` removes it to all orders in `r`, with
identically zero residual. `E1c`: the degeneracy is universal, including the laboratory value of `G`, and
at `κ = 1.6×10⁻⁶` the shift is 1.6×10⁻⁴ %, against a laboratory `G` known to 2×10⁻³ %.

`E2` — **where it does not reach, stated plainly.** The deposited theory passes its Solar-System rows only
with the `ξ²` screening switched on, and screening is precisely what breaks the exact `1/r²` shape: the
total scalar force becomes `S(r)[a₀Δ + κg_N]` with `S` varying, so its divergence is no longer zero. At the
gate-compatible `κ` the `κ` piece is 2.74× / 2.45× the piece the gate table already accounts for, i.e.
**0.0082 / 0.0039 of the Pitjev–Pitjeva bound** — still a PASS, with the margin cut from 333× to 121×.

So the honest verdict is: **exactly zero in the unscreened theory, proved; bounded but not zero in the
screened theory the gate table actually uses.** L52's F1 is right about the operator and incomplete about
the theory.

---

## 6. Verdict

**The repair is complete as a construction and the count stays at four.** The Dirac analysis was run by an
algorithm that returns 2 / 3 / 5 / 3 on the four reference theories and reproduces two published mode
speeds; the auxiliary contributes three second-class pairs and no first-class constraint, so three new
coordinates cost exactly zero modes; a second independent counter agrees; and the risk L52 named is shown
to have an *exact* locus, `Δ′(s) = −κ`, which is empty for the published flat splice and analytically empty
for the deposited C-family, while the negative control confirms the count really would fall to three if it
were not.

**But `κ` is not the free constant L52 priced it as, and that is the real cost this lane found.** L52 bounds
`κ` only from below and tabulates `κ` up to 0.1 as costing a 10% shift in the action's `a₀` and `G`; the
gates bound it from **above**, at ≈ 1.6×10⁻⁶ from gravitational Cherenkov on L33's own worst-case model
(soft, three named omissions all raise it) and ≈ 3.1×10⁻⁴ / 7.0×10⁻⁴ from the screened Saturn phantom-mass
row on the conservative screening bracket. That leaves every benefit intact — `Σ_∥` still falls from
9.6×10¹⁵ to 6.2×10⁵ and all three liabilities are still discharged — but it kills the `κ = 10⁻²` and `10⁻¹`
rows of L52's table, and, with the `κ ≥ 0.0324` the ν_RAR arm would need, closes that arm of §4.4's fork by
a **pincer with no interior** rather than by the qualitative argument L52 gave.

**One item is left open by name and this must not be read as a closure.** The two ceilings pull in opposite
directions on the same physics — the repair shortens the scalar cone, which is what removes the longitudinal
ill-posedness and breaks L33's F2 no-go, and it is the *same* shortening that removes the "no emission
channel" argument the Cherenkov row rests on. Deciding both properly needs the screened fourth-order solve,
which this lane does not do: it would fix whether the Saturn ceiling is real or an artefact of the
conservative bracket, and whether the Cherenkov ceiling survives its three omitted suppressions. Until then
the repair should be carried as **counted, classified and gated, with a two-sided window on `κ` whose upper
edge is provisional** — not as a closure.
