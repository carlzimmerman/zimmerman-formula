# L47 — the coherence-length collision: the programme carries a floor its own equation does not permit

2026-09-09. Lane L47, opened on the collision L30 exposed between the deposited theory's ξ = 0.10/0.15 pc
and the 4 pc its own static scalar equation forces.
Script: [L47_xi_collision.py](L47_xi_collision.py) → [L47_xi_collision.out](L47_xi_collision.out).
**18 PASS, 13 FAIL; all 12 controls PASS.** Every FAIL below is a substantive finding; each is a claim that could have gone
the other way and did not.

**Nothing was written into `PREREGISTRATION_DR4.md` or any `*_HASH.txt`.** What an amendment would have to
say is set out in §7 and printed by the script, for the owner to file or not.

## Verdict in three sentences

L30's number reproduces independently and is stronger than L30 claimed: the enclosed phantom-mass law
`M_ph(<r)/M = r²/(2ξ²)` is not an artefact of a point source (it survives a finite Sun, the eight planets,
the interstellar medium and the full Oort-limit local mass density to 0.24%), it is not an artefact of
L30's repair of the kernel (no solve anywhere in the floor computation reaches more than 0.46 C, so the
repaired region is never touched, and the law follows from an exact linear Green's function that contains
no kernel at all), and it is independent of the external field, of a₀ and of the Sun's mass — so
**ξ ≥ 4.00 pc on both footings** from Pitjev–Pitjeva, or ≥ 1.38 pc from the profile-appropriate sunward
gate alone. The standing 0.10/0.15 pc is blind to the fourth-order operator in a way that is now
quantified rather than asserted: the machinery that produced it (`g02`/`g03x`) contains no fourth-order
operator at all and screens with a linear Helmholtz filter on the phantom *density*; the one script that
does solve a fourth-order equation (`g03d`, and with it `g03g`, the solver behind the registered γ_v) puts
that operator on the **AQUAL correction field**, whose source is `(μ−1)`-suppressed by 9.3×10⁻⁷ at Saturn;
and PAPER8's own analytic justification applies the gradient-scale suppression `(ξ/R_Sat)²` to the
*saturated residual* rather than to the *Newtonian source*, an error of exactly `g_N(Saturn)/(2Ca₀) =
5.37×10⁵`. **Amendment 11's Arm B ceilings 1.0450 / 1.0300 are therefore no longer the right numbers:** at
the ξ the analysis supports the registered estimator returns γ_v = 1.0000 ± 0.0025 on both footings (force
boost 2.88×10⁻⁴ at 20 kAU, 320× below the registered ceiling's), the ceilings are not falsified but are
vacuous, and the registered kill-from-above threshold must move from 1.129 to 1.084.

---

## 1. The collision, stated once

Two things the programme carries at the same time:

| | value | provenance |
|---|---|---|
| the deposited theory's coherence length | **ξ = 0.10 pc canonical / 0.15 pc alt**, "theorem-forced" | PAPER8 (DOI 10.5281/zenodo.22667688) parameter table, citing L34, `g03d`, `g03z`; `L43_assemble_theory.py` `XI_FLOOR` |
| Amendment 11(b)'s registered Arm B ceilings, computed at those floors | **γ_v ≤ 1.0450 / 1.0300** | `g03y_gammav_corrected_floors.py` via `g03g_3d_pair_solver.py` |
| L30's solve of the action's own scalar equation | **ξ ≥ 4.00 pc**, both footings | `L30_saturated_branch.py` Gate 2 |

At 4 pc the largest DR4 separation, 30 kAU = 0.145 pc, is 28× *inside* the healing length — exactly where
the registered prediction is evaluated. They cannot both be right.

### The fork that generates the collision

Both readings write the same symbol for the same field, and they agree **exactly** for a spherical
monopole at ξ = 0 — which is what "the carried kernel" means, and is why the fork stayed invisible.

- **The carrier structure.** PAPER5 §7, `g03x`'s own docstring and L34's control A3 all state that the
  MOND scalar is sourced by matter: `∇·[J_Y(Y)∇φ] = 4πGρ`, hence `J_Y(g_φ)g_φ = g_N` on a sphere. This is
  the structure in which the bounded-boost theorem, the saturation at `C a₀`, and L34's corollary "no
  kernel of the class can screen the Solar System" exist at all. **Amendment 11(b) registers Arm B in
  exactly this structure** ("ν_RAR carried and saturated at its maximum").
- **The AQUAL structure.** `g03c`/`g03d`/`g03g` solve
  `∇·[μ(|∇(Φ₀+ψ)|/a₀)∇ψ] − ξ²∇⁴ψ = −∇·[(μ−1)∇Φ₀]`, in which ψ is the *correction* to the Newtonian
  potential and carries no point source. `g03d`'s own docstring: "no point source, no screening of Newton".

Once the fourth-order operator is switched on the two stop agreeing, because in the carrier structure that
operator must fight the **full point mass** and in the AQUAL structure only `(μ−1)` of it. At Saturn
`(μ−1) = C a₀/g_N = 9.30×10⁻⁷`. **That single factor is the whole collision.**

---

## 2. Controls — twelve, all PASS

Written from scratch, not inherited from L30. Two of L30's own controls are reproduced with different
mathematics and different numerics, and three more are added.

**The analytic route (no kernel, no solver).** Linearise the carrier equation about any background of
stiffness Σ — the galactic field, a cluster core, or nothing:

    Sigma grad^2 phi - xi^2 grad^4 phi = 4 pi G rho
      =>  1/[k^2(Sigma + xi^2 k^2)] = (1/Sigma)[ 1/k^2 - 1/(k^2 + Sigma/xi^2) ]   (Coulomb MINUS Yukawa)
      =>  phi(r) = -(GM/Sigma)(1 - e^{-r/l})/r ,   l = xi/sqrt(Sigma)
      =>  w(r) = (GM/(Sigma r^2)) [ 1 - e^{-r/l}(1 + r/l) ]  ->  GM/(2 xi^2)   as r -> 0,  Sigma cancelling.

**K1a/K1b (sympy, exact).** The Green's function satisfies the PDE identically for arbitrary Σ, and its
`r → 0` force limit is `GM/(2ξ²)` with Σ cancelling symbolically. **The biharmonic cone therefore does not
need L30's continuation, does not need a kernel, and does not need a nonlinear solve.**
**K1c.** Σ-independence verified numerically over four decades, Σ = 0.03 … 300, to 1.2×10⁻¹¹.
**K2.** An independent **3-D FFT** solve of the same operator on a periodic box (differenced against ξ = 0
so the residual is the short-ranged Yukawa and periodic images are exponentially harmless) reproduces the
analytic profile to 2.7% — a different dimensionality and a different code path from any 1-D solver.

**The nonlinear route.** The action's static scalar equation with the coherence operator outside `J`,
integrated once, `J_Y(w)u − ξ²(u″ − 2u′/r) = GM(<r)` with `u = r²w`, nondimensionalised and solved by
**Newton in `û = u/(r_M²a₀)`** on a uniform log grid — L30 solved in `q = s(w)`, so the variable, the
linearisation and the Jacobian are all different.

| control | what it reproduces | result |
|---|---|---|
| **K3** | L30's K4: kernel switched off ⇒ the exact biharmonic cone `w = GM/(2ξ²)` | 0.0064% at three radii spanning two decades |
| **K4** | L30's K5: `ξ → 0` ⇒ the algebraic carrier law `w = a₀Δ(g_N/a₀)` | 0.0036% over 6 solves, both footings |
| **K5** | L30's K6: the analytic interior prediction `min[GM/(2ξ²), Ca₀]` | 0.037% over 18 solves, ξ = 0.05 … 30 pc |
| **K6** | *new*: the saturated branch is never entered | largest Δ anywhere in any solve = **0.4598 C** |
| **K7** | L30's K3: the repository's own filtered proxy (`g02` imported unedited, driven as `g03x` drives it) returns the standing floors | **0.10 pc canonical / 0.15 pc alt**, exactly |
| **K8** | the gate constants and L34's bare-kernel shortfall | 1.388×10⁴ / 1.673×10⁴ vs L34's 1.400×10⁴ / 1.687×10⁴ (the 1% is `R_Sat` = 9.54 vs 9.58 AU) |
| **K9** | PAPER8's own printed screening numbers from `L43` line 540 | `(ξ/R_Sat)² = 4.636×10⁶` (paper 4.6×10⁶); screened/bound `3.020×10⁻³` (paper 3.0×10⁻³) |
| **K10** | the registered estimator, fed `g03g`'s original table **and** `g03y`'s carried table | **1.0325 / 1.0400** (g03h published 1.032/1.040) and **1.0450 / 1.0300** (Amendment 11(b) exactly) |

**K6 is the answer to "is it the repair that drives the 4 pc?" It is not.** The interior field sits at
`Δ = 4.65×10⁻⁵ a₀`, deep on the MOND branch, and the plateau where L30's continuation lives is never
touched by any solve that sets the floor. The repair is needed to *write* the equation down; it is not
needed to get this number, and the analytic route (K1a–K1c) gets it with no kernel at all.

**K10 matters for the propagation in §6**: the estimator used there is not a re-implementation whose
differences could be mistaken for physics — it returns Amendment 11(b)'s registered numbers to the fourth
decimal from the registered inputs.

---

## 3. Does `r²/(2ξ²)` survive a realistic Solar-System source? — yes, R1

The same fourth-order equation, six mass models, both footings, ξ = 4 pc, phantom mass read at Saturn's
orbit directly against Pitjev–Pitjeva.

| source model | `M_ph(<Sat)/M` | vs `r²/(2ξ²)` |
|---|---|---|
| point mass | 6.6827×10⁻¹¹ | 0.99968 |
| uniform ball, `R_☉` | 6.6827×10⁻¹¹ | 0.99968 |
| n = 3 polytrope | 6.6827×10⁻¹¹ | 0.99968 |
| + the eight planets | 6.6899×10⁻¹¹ | 1.00076 |
| + local ISM (1 cm⁻³) | 6.6939×10⁻¹¹ | 1.00135 |
| + Oort-limit 0.1 M☉/pc³ | 6.7009×10⁻¹¹ | 1.00240 |

Identical on both footings to five digits. **Every departure raises the phantom mass, so a realistic source
moves the floor up, not down.**

The reason is structural, and worth stating because it is why no reasonable source model can rescue the
standing floor: inside the healing length the fourth-order operator inverts to `ξ²∇²φ = −Φ_N`, so

    w(r) = (1/r^2) int_0^r [ -Phi_N(r') ] r'^2 dr' / xi^2

— the scalar responds to the enclosed **potential**, not to the local density. For any mass distribution
wholly inside `r` that is `GM/(2ξ²)` up to `O((R_source/r)²)`, and at Saturn `(R_☉/R_Sat)² = 2.4×10⁻⁷`.
The interstellar mass inside Saturn's orbit is 1.4×10⁻¹⁴ M☉.

The nearest stars are handled separately and are not a loophole: α Cen (2 M☉ at 1.34 pc) contributes its
own cone, 8.7×10⁻¹⁵ m s⁻², but it varies by only 2.0×10⁻¹⁹ m s⁻² across Saturn's orbit — 4.6×10⁻⁵ of the
gate. It is an external field, not a monopole inside Saturn's orbit, and K1c already shows the cone is
external-field-free.

---

## 4. Where the two calculations differ — the anatomy, in one table

Same quantity in every column: the phantom mass inside Saturn's orbit as a fraction of the Pitjev–Pitjeva
bound, carried ν_RAR, canonical footing.

| ξ [pc] | (A) PAPER8's formula `Ca₀/(1+(ξ/R_Sat)²)` | (B) `g03x`'s filtered proxy — **the standing floor's actual source** | (C) the action's equation, solved | C/B | C/A |
|---|---|---|---|---|---|
| 0.05 | 1.188×10⁻² | 2.862 | 6.384×10³ | 2231 | 5.373×10⁵ |
| 0.10 | 2.970×10⁻³ | 0.7917 | 1.596×10³ | 2016 | 5.373×10⁵ |
| 0.15 | 1.320×10⁻³ | 0.3643 | 7.093×10² | 1947 | 5.373×10⁵ |
| 0.30 | 3.300×10⁻⁴ | 9.434×10⁻² | 1.773×10² | 1880 | 5.373×10⁵ |
| 1.00 | 2.970×10⁻⁵ | 8.705×10⁻³ | 1.596×10¹ | 1834 | 5.373×10⁵ |
| 4.00 | 1.856×10⁻⁶ | 5.484×10⁻⁴ | **0.9975** | 1819 | 5.373×10⁵ |

Three ways in which the standing floor never sees the fourth-order operator, each now a check:

- **S1 (PASS).** All three have the *same* ξ-scaling (≈ 1/ξ²). The disagreement is a **normalisation, not a
  different physical law** — which is why it survived every consistency check the programme ran.
- **S2 (PASS).** The factor between PAPER8's formula and the solve is *exactly* `g_N(Saturn)/(2Ca₀) =
  5.3735×10⁵`, measured to four digits. **PAPER8 applies the gradient-scale suppression `(ξ/R_Sat)²` to
  the saturated residual `C a₀`; the equation applies it to the full Newtonian source `GM/R²`.** That is
  the entire content of the paper's §"the operator's gradient-scale suppression … brings the residual to
  3.0×10⁻³ of the bound".
- **S3 (FAIL = finding).** Neither `g02_filtered_efe.py` nor `g03x_nurar_carrier_and_cassini.py` contains
  any fourth-order operator. Their screening is a Helmholtz **output filter on the QUMOND phantom
  density**; the scalar's own equation is never solved. This is read out of the files, not inferred.
- **S4 (FAIL = finding).** The one standing script that *does* solve a fourth-order equation, `g03d`,
  states in its own docstring that the scalar has "no point source, no screening of Newton": its source is
  `−∇·[(μ−1)∇Φ₀]`, suppressed at Saturn by 9.30×10⁻⁷. **The operator there never sees the Sun.**

L34's gate returning identical floors for four different kernels — flagged in the lane brief as
suspicious — is explained by the same structure: a linear output filter on a phantom density whose
high-acceleration value is `C a₀` for every carried kernel cannot distinguish them.

---

## 5. The floor — F1–F4

    M_ph(<r)/M = r^2/(2 xi^2)
      Pitjev-Pitjeva  M_ph(<Saturn) < 6.7e-11 M_sun  =>  xi >= r_Sat/sqrt(2 x 6.7e-11) = 3.995 pc
                                                        (9.58 AU convention: 4.012 pc)
      alpha = 1 sunward, GM/(2 xi^2) < 3.662e-14 m/s^2 =>  xi >= 1.380 pc
      Saturn binds by 2.90x.

**F2 (PASS).** The floor is **identical on both footings**, 4.0 pc, because the cone contains neither a₀ nor
the kernel. That is itself a diagnostic: the standing floor *does* differ between footings (0.10 vs
0.15 pc) precisely because it comes from machinery in which a₀ enters.

**F1 (FAIL = finding).** The fourth-order carrier equation does not admit ξ ≤ 0.15 pc: the smallest
admissible tabulated ξ is 4.0 pc on both footings, **40× the canonical standing floor and 27× the alt one.**

**F3 (FAIL = finding).** The 4 pc does **not** depend on L30's repair (K6: max Δ = 0.46 C).

**F4 (FAIL = finding).** The two placements of the coherence operator are not interchangeable, confirming
L30's S1 with the same numbers by an independent route:

| placement | floor ξ, canonical | floor ξ, alt |
|---|---|---|
| outside J (solved exactly) | 4.00 pc | 4.00 pc |
| inside J (asymptotic balance `w = √(GMa₀/2)/ξ`, self-consistency verified to 0.00%) | 585 pc | 642 pc |

**Both exceed the standing floor by more than 25×, so the collision does not depend on which placement is
adopted.** The action document's and PAPER8's "it may equivalently sit outside J" is false as a statement
about the Solar System.

### Honest caveat on the gate

Applying the Pitjev–Pitjeva *phantom-mass* bound to a **constant** radial acceleration rather than to an
extra `δM/r²` is an approximation. It is the approximation the repository's own gates make (`g02`
`observables` reads `M_ph = G M_enc/r²` at `R_Sat`; `g03d` reads `r²ψ₀′`), so the comparison here is
like-for-like and the ratio between the two machineries is unaffected. The gate whose *profile* is
exactly right for a constant acceleration is the α = 1 sunward gate, and it gives **ξ ≥ 1.38 pc** — still
9–14× the standing floor. Both numbers are carried through §6.

---

## 6. Arm B at the ξ the analysis supports — B1–B4

Inside the healing length each star's scalar force is the **constant** `GM_i/(2ξ²)`, so for a pair of total
mass `M` at separation `r` the relative radial acceleration is `GM/r² + GM/(2ξ²)` and

    gamma_force(r) = 1 + [1 - e^{-x}(1+x)]/Sigma ,  x = r sqrt(Sigma)/xi   ->   1 + r^2/(2 xi^2)

— independent of the masses, of the orientation, of the external field and of a₀. At ξ = 4 pc, 30 kAU is
`r/ℓ = 0.058`, so the fourth-order term dominates the kernel term by `(ℓ/r)² ≈ 300`: superposition of the
two cones is exact there and `g03g`'s nonlinear external-field machinery is irrelevant. Varying Σ from 1.0
to 12.9 (Σ⊥ to Σ∥) moves γ_force at 20 kAU by 9.7×10⁻⁶.

| case | ξ [pc] | γ_force at 3 / 10 / 20 / 30 kAU | **γ_v, registered estimator** |
|---|---|---|---|
| Saturn phantom-mass floor | 3.995 | 1.00001 / 1.00007 / 1.00029 / 1.00064 | **1.0000 ± 0.0025** (both footings) |
| sunward-gate floor only | 1.380 | 1.00006 / 1.00060 / 1.00231 / 1.00502 | **1.0025 ± 0.0037** (both footings) |
| *registered* (AQUAL structure, ξ = 0.10/0.15) | 0.10 / 0.15 | — | 1.0450 / 1.0300 |

**B1 (FAIL = finding).** The registered ceilings are no longer the right numbers. In the force boost, which
does not round away: **2.876×10⁻⁴ at 20 kAU against the registered ceiling's 9.2×10⁻², a factor 320.**

**B2 (FAIL = finding, and the fair reading).** The corrected prediction is strictly positive and strictly
below the registered ceilings, so **nothing registered is falsified** — the ceilings are *vacuous*, 320×
too loose to exclude anything.

**B3 (FAIL = finding).** Amendment 11(d)'s row "γ̂ ≥ 1.129 → Arm B falsified" is the ceiling + 3σ_tot. At
the supported ξ the ceiling is 1.0000, so the threshold should be **1.084** (1.086 on the sunward-gate
floor). **A DR4 value in [1.084, 1.129] would kill Arm B and the registered table would not say so.** This
is the one place where the registered rule is *too lenient*, and it is the reason to fix it before the data
rather than after.

**B4 (FAIL = finding).** Inside the carrier structure there is **no** ξ that both passes the Solar System
and returns γ_v = 1.0450: that boost needs ξ = 0.226 pc, which the same structure excludes by 313× on the
Saturn phantom mass. The registered ceiling and the Solar-System gate are **mutually exclusive** in the
structure Amendment 11(b) names, separated by a factor 18 in ξ.

### What an amendment would have to say — NOT written into the preregistration

1. Arm B's floor, in the carrier structure Amendment 11(b) names, is **ξ ≥ 4.00 pc** (Pitjev–Pitjeva) or
   **≥ 1.38 pc** (sunward gate alone), **identical on both footings**. The floors 0.10 / 0.15 pc are
   superseded.
2. Arm B's ceiling becomes **γ_v ≤ 1.00014 (both footings)** on the Saturn gate, or **≤ 1.0025 (both
   footings)** on the sunward gate. 1.0450 / 1.0300 are superseded and must not be scored; they are not
   falsified, but they are 320× too loose in the force boost.
3. Amendment 11(d)'s kill-from-above threshold moves **1.129 → 1.084**. Amendment 11(e)'s statement that
   DR4 cannot separate Arm B from Newton becomes *stronger*: at a force boost of 2.876×10⁻⁴ — 0.0051 σ_tot in γ_v — the wide-binary
   channel stops being a test of Arm B at all — it can only kill it from above.
4. The row "1.007 – 1.056 → the arm question is decided for B" is no longer right: at the supported ξ a
   measurement anywhere in that range is 0.25–2.0 σ_tot **above** Arm B, not consistent with it.
5. PAPER8's "ξ ≥ 0.10 pc canonical / 0.15 pc alt — theorem-forced" and its `(ξ/R_Sat)²` suppression need
   the same correction, a factor `g_N(Saturn)/(2Ca₀) = 5.37×10⁵`.
6. "It may equivalently sit outside J" is false in the Solar System: 4.0 pc against 585 pc.

---

## 7. The documentation conflict — D1–D4

Read out of the files themselves, not from memory.

| document / script | placement of the coherence operator | source of the scalar |
|---|---|---|
| `THE_ACTION_2026-09-05.md` §1 | **inside J**, `J(Y + ξ²q^{λσ}q^{μν}∇_λV_μ∇_σV_ν)` | carrier (AeST coupling `2(2−K_B)J^μ∂_μφ`, statically `∇·J = ∇²Ψ`) |
| PAPER8 (DOI 22667688) eq. (1) | **inside J**, verbatim the same | carrier (PAPER5 §7's theorem is quoted as the reason ξ exists) |
| `g03d_exact_fourth_order_solar.py` | outside J, bare `ξ²Δ²ψ` | **AQUAL correction**, `−∇·[(μ−1)∇Φ₀]`, "no point source" |
| **`g03g_3d_pair_solver.py` — Arm B's solver** | outside J, bare `ξ²Δ²ψ` | **AQUAL correction** |
| `g02`/`g03x` — the standing floor | **no fourth-order operator at all** | QUMOND phantom density + one Helmholtz output filter |
| `L43_assemble_theory.py` line 540 | no operator: heuristic `Ca₀/(1+(ξ/R_Sat)²)` | n/a |
| L30 / L47 Gate 2 | outside J, bare `ξ²∇⁴φ` | **carrier**, `4πGρ` |

**D1 (PASS).** The deposited paper and the action document agree with each other: both display the operator
**inside J**.

**D2 (FAIL = finding).** The solver behind the registered Arm B number uses the **other** placement. The two
placements' Solar-System floors are 4.0 pc and 585 pc, so they are not interchangeable.

**D3 (FAIL = finding).** The solver behind the registered Arm B number uses the **other source**. Amendment
11(b) names the carrier structure ("ν_RAR carried and saturated at its maximum") but the number is produced
by the AQUAL correction equation.

**D4 (FAIL = finding, recorded).** The conflict is visible inside a single registered clause: Amendment
11(b) names "the coherence operator ξ²|∇⊥V|² **inside the kernel**; ν_RAR **carried** and saturated at its
maximum" and in the next sentence takes its floor from `g03d_exact_fourth_order_solar.py`, which puts the
operator **outside** the kernel and **removes the point source**.

**So yes: the paper and the preregistration describe the same theory in words, and the preregistration's
number is computed in a different one.**

---

## 8. Which ξ the programme should carry — V1, V2

**V1 (FAIL = finding).** Inside the structure it registers, the programme should carry **ξ ≥ 4.0 pc**
(Saturn) or **≥ 1.38 pc** (sunward gate alone), on both footings — not 0.10/0.15 pc.

**V2 (FAIL = finding).** Amendment 11 needs correcting before DR4, not after.

### Stated against interest — the one way out, and its price

If the theory is read in the **AQUAL structure** instead, the residual vanishes in the Solar System by
itself — PAPER8 says so in its own words ("only the carrier arm needs a coherence length at all") — ξ is
set by the Cassini **quadrupole** at 0.03/0.05 pc (`g03d`'s own solve), and there is no 4 pc problem. But
in that structure:

- PAPER5's bounded-boost theorem does not apply (it is derived from `J_Y(g_φ)g_φ = g_N`, i.e. from the
  carrier);
- the saturation at `C a₀` — the object Amendment 11(b) explicitly registers — does not exist;
- L34's "ξ is theorem-forced" corollary, which PAPER8 quotes as the reason ξ is in the action at all, does
  not exist either;
- and Arm B is then a *different registered prediction*, whose ceiling would need recomputing at the
  quadrupole-driven floors and whose relation to Arm A would need restating.

**That is a different theory, not a rescue of this one — and it happens to be the theory the registered
γ_v solver actually solves.** The programme has to pick one. It cannot register Arm B as the carrier
structure and evaluate both its coherence length and its wide-binary boost in the AQUAL one.

---

## PASS/FAIL, verbatim

See [L47_xi_collision.out](L47_xi_collision.out). 18 PASS / 13 FAIL. The 12 controls (K1a, K1b, K1c, K2, K3, K4, K5,
K6, K7, K8, K9, K10) all PASS, and so do R1, S1, S2, F2, D1 and V1. The FAILs are findings: **R1's own tolerance held** (the law
survives a realistic source), while **S3, S4** (the standing machinery is blind to the fourth-order
operator), **F1** (the equation does not admit ξ ≤ 0.15 pc), **F3** (the number does not depend on L30's
repair), **F4** (the two placements are not equivalent), **B1–B4** (the registered ceilings are superseded,
vacuous, and the kill threshold is misplaced), **D2–D4** (paper and preregistration compute in different
structures) and **V1, V2** (the verdict) each record something the programme did not previously carry.

## Scope — what is not done here

- The Cassini **quadrupole** is not re-solved in the carrier structure. Only the monopole is, which is the
  binding gate in every machinery the repository runs (`g03x`'s own table: at ξ = 0.10 pc, Q2/ceiling
  0.121 against M/bound 0.792) and is the gate L30 and this lane both use. A carrier-structure quadrupole
  solve is the obvious next item and would only raise the floor.
- The two rows of the §6 table at ξ = 0.10 / 0.15 pc are a **linear-response diagnostic, not a solve**: at
  those lengths the pair's own field is not a small perturbation on the external field at 15–30 kAU. They
  are shown only to record that the carrier structure does not return 1.0450/1.0300 at those lengths
  either; those lengths are excluded by 1600× in the same structure anyway, so nothing rests on them.
- The inside-J floor (585/642 pc) is an **asymptotic balance with its self-consistency verified**, not a
  solve, exactly as in L30. It is not load-bearing: the conclusion holds for either placement.
- Whether ξ = 4 pc is *survivable elsewhere* is not tested here. It screens the scalar out to 104 solar
  MOND radii around every star, which leaves galaxy-scale MOND untouched (kpc ≫ 4 pc) but makes wide
  binaries, globular clusters and the local stellar granularity Newtonian to O(r²/2ξ²). Those are separate
  gates and this lane does not run them.
- The `α = 1` sunward gate is inherited from `g02` unchanged, including its 1278× normalisation.
- No file in `prep_2026/`, `papers_2026/` or the lead's trees was edited. `g02_filtered_efe.py` and
  `wide_binary_pipeline.py` were **imported**, never modified.
