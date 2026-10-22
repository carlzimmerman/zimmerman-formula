# A48 — RECORD AUDIT: A33 §5's first integral, and which mass the law's `g_N` carries

**Lane:** A48_first_integral · **Date:** 2026-10-21 · **Base:** `A33_master_action/MASTER_ACTION.md`
(§1, §3.1, §5, §7.3), `A40_growth/report.md` §5, `A18_two_ratios/report.md`, `A11_cold_normalization/report.md`,
A7's frozen SPARC selection. **Script:** `a48_checks.py` (25/25 PASS, exit 0, 12.5 s) · **Output:** `a48.out` ·
**Data:** `a48_results.json` · **Mutations:** `MUTATE.md` (five, each exits 1).

## Claim

A33 §5 states the first integral `(r²g)′ = Kρ_src r² + (r²u)′`, i.e. `g = g_N + u` with
`g_N = GM_src/r²`. A40 reads `ρ_src` off the lapse equation (`ρ = ρ_m + ρ_c`) and concludes
`M_src = M_b + M_c` = total matter, making the deep-MOND amplitude `√6.3643 = 2.523×` the
baryon-only value that every SPARC fit in the record uses. **That reading is wrong, and the record
already contains its refutation.**

The first integral is an *identity that defines* `g_N ≡ g − u`. It carries no information about which
mass is in the source. What fixes `M_src` is A33 §1's own partition `ρ_c = ςρ_c + (1−ς)ρ_c`
(charge + native), which gives

> **`M_src = M_b + (1−ς) M_c`, so `M_src = M_b` exactly at `ς = 1`.**

`ς = 1` is not a choice this lane makes: A33 §7.3 *forces* it (a constant partition `ς = 0.4716`
deforms the law by 0.243 at `g = a₀/2`, excluded by the RAR by orders of magnitude). A40's
`M_src = M_b + M_c` is the **`ς → 0` end** of that family — the end at which the charge's source
vanishes (`ς = 0 ⇒ d = 0`), so the RAR's `u(r)` profile is no longer a solution of the P equation. On top of that,
A33 §3.1's printed source double counts `ςρ_c` (the charge's share sits in `ρ_c` *and* in `d`), which
is the mechanical reason §3.1 reads as if total matter were forced.

**The data then put the matter beyond argument.** On all 171 SPARC galaxies with one `Υ` per galaxy
(identical error model, identical `Υ` bounds, identical selection as A7):

| branch | `χ²` (a₀ = 9.3603e-11) | `χ²` (a₀ = 1.132e-10) | `χ²` (a₀ free) |
|---|---|---|---|
| **B** `g_N = G M_b/r²` | **7259.44** | **7916.90** | **7114.30** (a₀* = 8.08e-11) |
| **T** `g_N = 6.3643 G M_b/r²` | 81835.81 | 97368.83 | 17471.11 (a₀* = 2.65e-12) |
| **Δχ² (T−B)** | **+74576** | **+89452** | **+10357** |

The data select **baryons only**, by `Δχ² = 1.04×10⁴` even when `a₀` is refitted (branch T's own best
`a₀` collapses to `2.65×10⁻¹²`, 35× below the closure), and by `7.5×10⁴` at the theory's own `a₀`.
There is no `a₀` that rescues total matter, because the Newtonian end (`g_bar > a₀`, 793 of 3375
points) is `a₀`-independent and `6.364×` too massive: `V` is `2.523×` too high with nothing to absorb
it. The systematics-free statement is the same: at fixed `Υ = 0.5/0.7`, the median `|ΔV/V|` is
**10.7 % (B)** against **90.7 % (T)** — 128.8 % in the Newtonian end — for a 5 % error floor.

A33 §5's algebra is therefore **not** wrong. The attribution built on it is — "the first integral fixes
`M_src = M_b + M_c`", which A40 takes from §3.1's `ρ = ρ_m + ρ_c`. Downstream, A33's §5 attribution and
A40's adjudication do not survive; A40's *numbers* (σ8 = 0.7619, χ² = 14.21/8) and A44's mass-budget
use do (§4 below).

---

## 1. The quotation, and what the first integral actually says

### 1.1 The exact text

`A33_master_action/MASTER_ACTION.md:278–280`, verbatim:

> *Consistency of the three:* `(L)` differentiated and `(P-sph)` substituted give
> `(r²g)′ = Kρ_src r² + (r²u)′`, i.e. `g = g_N + u` with `g_N = GM_src/r²`, which is `(P-sph)`'s first
> integral. That is why the law is *exact* and not an expansion, and why the P sector is a **charge**
> sector.

and §3.1, verbatim: "`ρ ≡ ρ_m + ρ_c` is the total matter density, `d ≡ D_iP^i`", with the printed
lapse equation

```
R3 − K_ijK^ij + (1+β)θ² − 2Λ = 4K [ ρ_m + ρ_c + d + W(u) + (γ/2)d² ].            (L)
```

The two other equations of §5 are `n₁(1+γd) + γd′ = KW′(u)` (P-sph, `f = 1`) and the Jeans equation
`σ_c² dlnρ_c/dr = −g`.

### 1.2 Independent derivation from the action

I rebuilt the reduced Lagrangian from A33 §1 — `L = 4πr²{N f^{3/2}[(R3−2Λ)/(4K) − W − (γ/2)d²] + √f P N′ − ρN}`
— and varied it:

- **A1: residual 0.** The lapse EL is exactly the printed `(L)`. The equation is not where the defect sits.
- **A2: residual 0.** At `O(ε)` with `N = 1+Φ`, `f = 1−2Φ`, `P = εp`, the constraint reduces to
  `∇²Φ = K(ρ + ∇·P) = 4πG(ρ + d)`. (Λ is absorbed by the background.)
- **A3: 3.2×10⁻⁴.** Integrating with Gauss' law gives `g = G M_ρ/r² + u`, `u ≡ KP` — the `+u` is
  literally `GM_d/r²`, the charge's own contribution. The "first integral" is Gauss' law plus a
  definition, nothing more.
- **A4: residual 0.** With `u = a₀g/(g+a₀)` (from `g = KW′(u)`), `g − u = g²/(g+a₀)` identically.

So the complete content of §5 is:

```
g = G M_ρ/r² + u ,   u = a₀g/(g+a₀)   ⟺   g_N ≡ g − u = g²/(g+a₀) = G M_ρ/r² .
```

`g_N` **is** the Newtonian field of whatever sits in `M_ρ`. The identity cannot tell you what that is;
it only tells you that the law is "the Newtonian field of the source equals `g²/(g+a₀)`". The
question "is it `M_b` or `M_b + M_c`?" is entirely a question about the Hamiltonian constraint's
source, and the answer is not in §5.

### 1.3 What `M_src` is: A33's own one-parameter family

A33 §1, verbatim: "The total cold density splits as `ρ_c = ςρ_c + (1−ς)ρ_c`: the first part is what
the P sector's charge reproduces, the second gravitates natively." With `D·P = ς(ρ_c − ρ̄_c)` (§1,
eq. C2) the corrected lapse source is `ρ_b + (1−ς)ρ_c + d`, and §5's split (`ρ_src` → `g_N`, `d` → `u`)
reads

```
M_src = ∫ρ_src = M_b + (1−ς)M_c ,      u = G·ς(M_c − M̄_c)/r² = G M_ph/r² ,
g = G[M_b + (1−ς)M_c]/r² + G M_ph/r² = G(M_b + M_c − ςM̄_c)/r² .                        (1)
```

The total is total matter, as it must be — the cold density is in the lapse source either way. What
(1) fixes is the *split*: §5's `g_N` carries only the native part, `M_src`; the rest sits in `u`.

The printed `(L)` instead has `ρ_b + ρ_c + ς(ρ_c−ρ̄_c)`, which is **larger by exactly `ςρ_c`** (A6:
symbolic residual `ρ_c·ς`). That is the double count: the charge's share of the cold density is
counted once as native matter and once as charge. It is why §3.1 reads as if total matter were forced.

Equation (1) is the answer to Task 1. Evaluating it (A6b):

| `ς` | `M_src/M_b` | deep-MOND amplitude `√(M_src/M_b)` | what it is |
|---|---|---|---|
| 0.0000 | 6.3643 | 2.5228 | A40's branch: charge off, `M_ph = 0` |
| 0.4716 | 3.8345 | 1.9582 | A21's MID band, if read as a partition |
| 0.9865 | 1.0724 | 1.0356 | A21's OUT band, if read as a partition |
| **1.0000** | **1.0000** | **1.0000** | **A33 §7.3's forced value: baryons only** |

**`M_src = M_b + M_c` is not forced. It is a choice of how the P charge is defined — and it is the
choice `ς = 0`, at which `d = 0` and the P sector decouples.** A33 §7.3 then closes the argument
against it: a *constant* partition coefficient `ς = 0.4716` deforms the law by 0.243 at `g = a₀/2`,
"a 24 % effect, excluded by the RAR by orders of magnitude. So the partition reading is only
consistent with `ς = 1`". At `ς = 1`, (1) gives `M_src = M_b`.

The measured `ς = 0.4716 (MID) / 0.9865 (OUT)` (A21) does not reopen this: A33 §7.3 identifies it
with the *catchment* `f_ret`, not with a partition. If one nevertheless reads it as a partition, the
amplitude excess is 1.96× (MID) to 1.04× (OUT) — the MID value is excluded by the RAR, the OUT value
is a 3.6 % effect and is not.

### 1.4 Why "total matter" cannot even be a reading of the law

There is a second, independent argument that does not depend on the partition at all. If the source
already contains the phantom (`M_ρ = M_b + M_ph`, `M_ph ≡ r²u/G`), the first integral gives
`g = g_N + 2u`, and the law `u = a₀g/(g+a₀)` becomes

```
g_N = g − 2a₀g/(g+a₀) ,      deep limit:  g_N − g → −2a₀   (Newtonian + 2a₀, not MOND).
```

A48's check A7 recomputes this symbolically: the limit is `−2a₀`. So "the source includes the phantom" is not a
different normalisation of the law — it is a *different law*. The only self-consistent assignment is
that `M_ρ` is the mass that is **not** already represented by the charge. That is the baryons.

### 1.5 One secondary defect: §5's "exact"

A5 solves the `(L)` and `(P)` equations for `ρ` and `P″` and evaluates the residual of
`(r²(g−u))′ − Kρr²` at a point where both hold: **0.221 of the terms**, i.e. the identity does not
close beyond `O(ε)`. §5 invokes only `(L)` and `(P)`; at all orders the `f`-equation (which §5 does not
use) would be needed. **This is a wording defect, not a numerical one** — every galactic use is at
`O(ε)`, where A2/A3 show the identity is exact to `3×10⁻⁴` — but "that is why the law is exact and not
an expansion" is not supported by the derivation offered.

---

## 2. The consequence, computed

### 2.1 Method

Exactly A7's frozen pipeline, re-implemented here and validated against its published total:

- 175 `*_rotmod.dat` files, 3391 rows, **171 galaxies with ≥ 5 points, 3375 points** (B1);
- `σ² = errV² + (0.05 V_obs)²`, `χ²` in velocity space;
- **one `Υ` per galaxy**, `Υ ∈ [0.05, 2.50]`, disk = bulge, 400-point log grid + bounded Brent;
- branch B: `g_N = G M_b/r²`, `M_b` from `V_gas² + Υ(V_disk²+V_bul²)`;
- branch T: `g_N = 6.3643 G M_b/r²` (i.e. `M_c = 5.3643 M_b` added at every radius, the assumption
  implicit in `g_N = G(M_b+M_c)/r²`);
- identical `Υ` freedom in both branches, so no parameter penalty.

Validation: branch B at `a₀ = 9.3603×10⁻¹¹` returns **7259.44**, against A7's published **7259.38**
(Δ = 0.06, 8×10⁻⁶ relative) — B2.

### 2.2 The χ² table

`dof = 3204`.

| model | `χ²` | `χ²/dof` | `Δχ²` vs B at the same `a₀` |
|---|---|---|---|
| B, `a₀ = 9.3603e-11` (canonical, κ = 1/2) | **7259.44** | 2.266 | — |
| T, `a₀ = 9.3603e-11` | 81835.81 | 25.542 | **+74576.4** |
| B, `a₀ = 1.132e-10` (the record's `a₀`) | **7916.90** | 2.471 | — |
| T, `a₀ = 1.132e-10` | 97368.83 | 30.390 | **+89451.9** |
| B, `a₀` free | **7114.30** (`a₀* = 8.080e-11`) | 2.220 | — |
| T, `a₀` free | 17471.11 (`a₀* = 2.650e-12`) | 5.453 | **+10356.8** |
| B, fixed `Υ = 0.5/0.7`, `a₀ = 1.132e-10` | **22919.22** | 6.791 | — |
| T, fixed `Υ = 0.5/0.7`, `a₀ = 1.132e-10` | 841163.93 | 249.234 | **+818244.7** |

### 2.3 Which branch, and by how much

**Baryons only, by `Δχ² = 74 576` at the theory's `a₀`, `89 452` at the record's, and `10 357` with
`a₀` refitted.** The last number is the one that matters methodologically: it is the comparison at
equal parameter count, with each branch at its own best `a₀`. Branch T's best `a₀` is
`2.65×10⁻¹²` — 35× below the closure — and its `χ²/dof` is still 5.45 against 2.22.

Three independent statements of the same thing, in increasing order of robustness:

1. **`Δχ²`.** `+74576` at fixed `a₀` is `386σ` formal, `+10357` at free `a₀` is `144σ` formal. SPARC's
   `χ²/dof ≈ 2.3` means the absolute `χ²` is systematics-dominated, so the *formal* σ overstates; but
   the branch difference is 93× the largest *footing* difference in the same table (`Δχ² = 803`
   between the record's `a₀` and branch B's own best fit), so no plausible systematic rescales it away.
2. **Systematics-free velocity residuals** (B11), fixed `Υ = 0.5/0.7`: median `|ΔV/V|` = **0.107 (B)**
   vs **0.907 (T)** over all 3375 points, and **0.095 vs 1.288** at `g_bar > a₀`. A 5 % error floor
   against a 91 % median error is not a weighting artefact.
3. **The deep-MOND amplitude** (B9): in the deep limit at fixed baryonic mass the ratio is
   `√6.3643 = 2.5228` exactly; the median over the 126 galaxies with points at `g_bar < 0.1a₀`
   returns 2.5228. That is the A40 number, reproduced.

The high-acceleration end is the irreducible kill: **793 of 3375 points have `g_bar > a₀`**, where
branch T predicts `g = 6.364 g_bar` (V `2.523×` too high) and `a₀` does not enter. No rescaling of
`a₀` can remove a mass excess in the Newtonian limit.

Two honest qualifications:

- 17 of 171 galaxies individual `χ²` prefer T by more than 1 (B10). They carry **0.8 %** of
  `Σ|Δχ²_g|` — a tail, not a population.
- Branch B itself prefers `a₀ = 8.08×10⁻¹¹` over the closure `9.354×10⁻¹¹` by `Δχ² = 145`. That is
  the record's known `a₀`/distance degeneracy (A9: `a₀ → a₀/f` under a uniform distance rescaling;
  the free-SPARC fits quote `1.1033e-10`, the gas-rich subsample `6.62e-11`). SPARC alone fixes `a₀`
  to ~±25 %, systematics-limited. It does not touch the 6.364× question, which is nearly 4× the
  entire observed spread of `a₀` values (6.6e-11 to 1.1e-10, a factor 1.67).

### 2.4 Why no `a₀` rescues total matter

The tempting escape is "absorb 6.3643 into `a₀`". It fails for two reasons.

1. **`a₀` enters as `√(a₀ g_N)`.** A source factor `1+M_c/M_b = 6.3643` is absorbed by
   `a₀ → a₀/6.3643`, **not** `a₀/2.523`. (The lane brief's "a₀ must be 2.523× smaller" is one factor
   of 2.523 short: 2.523 is the amplitude factor, and `2.523² = 6.3643`. A8.) The required values are
   `1.7787×10⁻¹¹` (record footing) or `1.4707×10⁻¹¹` (canonical).
2. **Even that does not work.** The two branches are related exactly by
   `g_T(a₀, x) = 6.3643 · g_B(a₀/6.3643, x)` (same `x = g_bar`), so rescaling `a₀` can match the
   deep-MOND amplitude — but only by moving the RAR knee to a lower baryonic acceleration, and it
   cannot touch the Newtonian end at all, where `g_T = 6.364 g_bar` for any `a₀`. Fitting `a₀` freely,
   branch T bottoms out at `a₀* = 2.65×10⁻¹²` with `χ²/dof = 5.45`: it prefers to switch the MOND
   boost off rather than live with the mass excess.

### 2.5 The closure (Part C)

| branch | `a₀` required | `κ = a₀/(c√(Gρ_DE))` | `Λ/Λ_obs` | `1/κ` |
|---|---|---|---|---|
| baryons (record `a₀`) | 1.1320e-10 | 0.6051 | 1.464 | 1.65 |
| baryons (canonical) | 9.3603e-11 | 0.5003 | 1.001 | 2.00 |
| total matter (record) | 1.7787e-11 | 0.0951 | 0.0362 | 10.52 |
| total matter (canonical) | 1.4707e-11 | 0.0786 | 0.0247 | 12.72 |

`a₀ = κc√(Gρ_Λ)` with `Λ_obs = 1.0890×10⁻⁵² m⁻²` gives `a₀ = 9.3542×10⁻¹¹` and `c√(Gρ_DE) = 1.8708×10⁻¹⁰`,
i.e. `κ = 0.5003` (C1, reproducing A33 K14b/K14c). Branch T's `a₀ = 1.4707×10⁻¹¹`
requires `κ = 0.0786`, a factor `6.3643` below `1/2`, and at fixed `κ = 1/2` requires
`Λ = 2.692×10⁻⁵⁴ m⁻² = Λ_obs/40.5` (C4). `Λ` is measured to ~1 %; a factor 40.5 is not a tension.

---

## 3. Verdict on Task 1

**Is `M_src = M_b + M_c` forced by the action? No.**

- The first integral is an identity defining `g_N ≡ g − u`; it fixes nothing about the source.
- A33 §1's partition gives `M_src = M_b + (1−ς)M_c`. `M_src = M_b+M_c` is the `ς → 0` end, where the
  P charge vanishes and the law is not the law.
- A33 §7.3 forces `ς = 1`, hence `M_src = M_b`.
- The printed `(L)` additionally double counts `ςρ_c`, which is what makes §3.1 look total.

So it is **a choice of how the P charge is defined**, and A40 chose the one value (`ς = 0`) at which
the P sector does nothing.

## 4. Downstream flags (Task 3)

The data select baryons-only, so every file in the record that carries `M_src` / `M_b + M_c` is
listed with its status (Part D of `a48.out`; the scan finds 7 files, of which 6 are substantive
and one, `A44_no_edge/a44_checks.py`, only repeats the `6.364 M_b` constant):

| file | where | role | survives? |
|---|---|---|---|
| `A33_master_action/MASTER_ACTION.md` | §3.1 source `ρ = ρ_m+ρ_c`; §5 first integral | **source of the claim** | **No** — §5's `M_src` sentence is wrong (the integral is not). Everything else in A33 — the law K3, PPN, `c_T`, the coefficient table, K13 — never uses the *value* of `M_src` and survives unchanged. |
| `A40_growth/report.md` | §5.1, K11, branch S, abstract | the adjudication | **No** — "the action decides for S" falls. **The number survives:** A40's own K11 gives `σ8(S)/σ8(C) = 1.0019`, so `σ8 = 0.7619`, `f(z)`, `χ² = 14.21/8` and every growth conclusion stand to 0.19 %. |
| `A40_growth/a40_checks.py` | K11, lines 478–492 | the check encoding the claim | **No** — the assertion is the defect. The numbers it prints (2.523, `M_c/M_ph = 0.207`) are correct, and they are the evidence against it. |
| `A45_reference_field/report.md` | `g_N = GM_src/r^2` in the (P-sph) section; the "what this does not do" item | repeats the fork as **open** | **Yes**, with a wording fix — its reference-field conclusions never use the value of `M_src`. The fork sentence should now read "`M_src = M_b`, so the SPARC fits are the action's own branch". |
| `A47_fret/report.md` | §2, `M_tot = M_b + M_c` (r200c conversion) | **mass budget** | **Yes** — same as A44: a total-halo-mass definition for an overdensity argument, not the law's `g_N`. |
| `A44_no_edge/report.md` | §5, `M200 = M_b + M_c = 6.364 M_b` | **mass budget**, not the law's `g_N` | **Yes** — it converts `M200 → M_b` through the cosmic share, a definition (A18), not a claim about the source. It rests on A18's independent cluster determination `R_req = 5.55 ± 0.43`, not on §5. Flagged for clarity only. |

Scope: every other lane that uses the law (A7, A9, A11, A14, A16, A18, A20, A21, A25, A26, A29,
A36, A41, A43) writes `g_N = G M_b/r²` with `M_b` baryonic. **None of them consumes A33 §5**, so the
2.523× is confined to the rows above.

## 5. The counterfactual branch, stated plainly (Task 4)

If the data had selected total matter, the footing would collapse as follows — stated with the
corrected factors, because the brief's 2.523× is too kind by one power:

- `a₀ = 1.132×10⁻¹⁰ m/s²` would be wrong by **6.3643×**, not 2.523×; the required value is
  **`a₀ = 1.7787×10⁻¹¹ m/s²`** (record footing) or **`1.4707×10⁻¹¹`** (canonical).
- `κ = a₀/(c√(Gρ_Λ))` would fall from **0.6051 to 0.0951** (record) or **0.5003 to 0.0786** (canonical) —
  outside the saturation cap's admissible set `{1, 0.707, 0.5}` (A19) and `3.4σ` below A19's measured
  `κ = 0.417 ± 0.095`.
- At fixed `κ = 1/2`, `Λ = 32πa₀²/c⁴` would have to be **`2.692×10⁻⁵⁴ m⁻² = Λ_obs/40.5`**.
- `a₀ = κc√(Gρ_Λ)` would be broken by 6.3643×, `Λ = 32πa₀²/c⁴` by 40.5×, and the record's
  `Λ_bare ≥ 1.462Λ_obs` (A33 K16) would become `Λ_bare ≥ 59.2 Λ_obs`.

That is not a correction to the footing. It is a different universe with the same galaxies in it.
**The data do not select it**, so this paragraph is a contingency, not the record's state.

## 6. Status

- **Task 1 — DERIVED (negative).** The first integral is an identity (A1–A4); `M_src = M_b + (1−ς)M_c`
  is A33's own partition (A6); `M_src = M_b + M_c` is the `ς = 0`, charge-off end (A6b); `ς = 1`
  follows from A33 §7.3. "Forced" is false. `§5`'s "exact" is an overstatement (A5).
- **Task 2 — NUMERICAL, decisive.** Baryons only by `Δχ² = 74 576 / 89 452 / 10 357` (fixed canonical /
  fixed record / `a₀` free), `χ²/dof` 2.27 vs 25.5, median `|ΔV/V|` 10.7 % vs 90.7 % (B1–B11).
- **Task 3 — FLAGGED.** Three statements do not survive (A33 §5's `M_src` sentence, A40's §5.1
  adjudication, A40 K11); A40's numbers, A44's and A47's mass budgets, and A45's reference-field result
  do (§4 above).
- **Task 4 — CONTINGENT, computed.** `a₀ = 1.7787e-11`, `κ = 0.0951`, `Λ = Λ_obs/40.5` if total matter
  were selected. It is not.

## 7. Checks

`a48_checks.py` — 25 checks, deterministic, stdlib + numpy/scipy/sympy, 12.5 s, no network, exit 0 iff
all pass. `a48.out` is the captured stdout.

| id | proves | measured | threshold |
|---|---|---|---|
| A1 | `(L)` is the lapse EL of A33's reduced action | 0 | 0 |
| A2 | `O(ε)` reduction is `∇²Φ = 4πG(ρ+d)` | 0 | 0 |
| A3 | Gauss = first-integral form `g = GM_ρ/r² + u` | 3.2e-4 | <5e-3 |
| A4 | `g − u = g²/(g+a₀)` identically | 0 | 0 |
| A5 | all-orders identity does **not** close | 0.221 | >0.02 |
| A6 | printed `(L)` exceeds the partition by `ςρ_c` | `ρ_c·ς` | `ςρ_c` |
| A6b | `ς=0 → 6.3643 M_b`; `ς=1 → 1.0000 M_b` | 6.3643 / 1.0000 | exact |
| A7 | phantom-in-source gives `g_N − g → −2a₀` | `−2a₀` | `−2a₀` |
| A8 | `√6.3643 = 2.52276`; a₀ factor 6.3643; Λ factor 40.50 | exact | exact |
| B1 | sample = A7's frozen selection | 175/3391/171/3375 | exact |
| B2 | branch B reproduces A7's `χ²` | 7259.44 | 7259.38 ± 0.5 |
| B3 | `Δχ²(T−B)` at canonical `a₀` | +74576.4 | >1000 |
| B4 | `Δχ²(T−B)` at record `a₀` | +89451.9 | >1000 |
| B5 | sign stable across footings | both >0 | — |
| B6 | zero-parameter `Υ=0.5/0.7` comparison | 22919 vs 841164 | T ≫ B |
| B7 | branch B best `a₀` | 8.08e-11 | (0.5, 1.3)e-10 |
| B8 | branch T best `a₀` and `Δχ²*` | 2.65e-12, +10357 | >1000 |
| B9 | deep-end amplitude ratio | 2.5228 | 2.5228 |
| B10 | galaxies preferring T | 17/171, 0.8 % of `Σ|Δχ²|` | ≤20, <1 % |
| B11 | median `|ΔV/V|` fixed `Υ` | B 0.107, T 0.907 | B<0.2, T>0.5 |
| C1 | `a₀(Λ_obs)`, `c√(Gρ_DE)`, `κ` | 9.3542e-11, 1.8708e-10, 0.5003 | exact |
| C2 | branch T's required `a₀` | 1.7787e-11 / 1.4707e-11 | exact |
| C3 | `κ` per branch | 0.6051/0.5003 vs 0.0951/0.0786 | <0.12 |
| C4 | `Λ` required by branch T | 2.692e-54 = `Λ_obs`/40.45 | <0.03 |
| D1 | downstream scan finds all listed files | 7 files / 6 rows | 6/6 |

Five mutations (`total`, `baryon`, `a0factor`, `exact`, `nocount`), each breaks at least one check and
exits 1 — `MUTATE.md`.

## 8. What this does not do

1. **It does not settle the cluster sector.** A18's `R_req = 5.55 ± 0.43` at clusters says the law
   *under*-supplies there by ~2×, while at galaxies it over-supplies if the cold mass is in the source.
   That asymmetry is a real open problem (A41's lane), and this audit does not solve it — it only
   establishes that the galaxy normalisation is baryonic.
2. **It does not derive `ς`.** It uses A33 §7.3 and A21's measurements to fix the branch; the
   mechanism behind `ς(r)` remains open, as A33 §6.2 says.
3. **It does not re-derive the law from the action at all orders.** A5 shows §5's "exact" claim is
   unsupported; the `O(ε)` derivation (A2/A3) is the one every number here rests on.
4. **SPARC's `χ²/dof ≈ 2.3`** means the absolute `χ²` values in §2.2 are systematics-dominated; the
   branch comparison is protected by B11's velocity medians, not by the formal σ.
5. **The `a₀` preference inside branch B** (8.08e-11 vs the closure 9.354e-11, `Δχ² = 145`) is
   reported, not resolved; it is the known distance/`Υ` degeneracy (A9, A14), and it is 71× below the
   branch difference this lane measures (`Δχ² = 10 357`).
