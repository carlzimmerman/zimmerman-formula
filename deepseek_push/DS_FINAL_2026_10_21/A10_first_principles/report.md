# A10 — Can ONE first-principles statement give both postulates?

Lane A10, `DS_FINAL_2026_10_21`. Script: `a10_checks.py`; output: `a10.out`; numbers: `a10_results.json`.
Status word used below: **NO-GO(obstruction)** — a negative result with the obstruction proven, per BRIEF §5.

## Claim

The response law **P2 follows exactly** from one statement about a saturating conserved current, and P1's
*scaling* follows from the same statement, but **P1's coefficient does not follow from any principle of that
class**: every principle that builds `a0` from the horizon acceleration `cH_Λ` with a rational cell count
gives `κ ∈ √(8π/3)·ℚ = {2.8944, 1.4472, 0.9648, 0.7236, …}`, which **cannot contain 1/2**, because
`1/(2√(8π/3))` is irrational. The natural horizon counts give `κ = 0.2303` (4π), `0.4607` (2π), `0.9213` (π)
— a factor-4 spread (0.230329 to 0.921318) — and the canonical `κ = 1/2` sits **7.9 % above the nearest of them**. So the single
principle reduces to the single number `a0/(cH_Λ) = κ/√(8π/3) = 0.172747`, and that number is a
normalisation, not a count. The kernel carries a *second*, independent normalisation — the cell quantum
`q`, equal to `a0` for P2 and to `a0/2` for the quadrature — which S has to **state** (clause S1) rather
than derive. Those two numbers are the whole of what a genuine one-principle derivation would have to
produce, and neither is a count.

## Derivation

Symbols: `c, G, Λ, ρ_DE` per BRIEF §4; `H_Λ ≡ c√(Λ/3)`; `a0` the vacuum scale; `g` the observed (total)
acceleration, `g_N` the baryonic one; `j ≡ g − g_N` the vacuum current; `û ≡ j/a0`, `ŝ ≡ g_N/a0`; `b` the
kernel capacity integer.

### 1. P1 in the form that exposes its content

With `ρ_DE = Λc²/(8πG)` and `H_Λ² = Λc²/3`, the three published forms are one equation, and it has a
one-number content:

    (1)  a0 = κ c √(G ρ_DE) = κ c² √(Λ/8π) = κ c H_Λ / √(8π/3)
    (2)  a0/(c H_Λ) = κ/√(8π/3) = 0.172747 (κ=1/2; BRIEF rounds to 0.172746)   and   c H_Λ/a0 = (1/κ)√(8π/3) = Z = 5.788810

`Z = 2√(8π/3)` is the "1/12 of the horizon" number: the twelfth is really `2Z = 11.577620`, not 12 (K11).
Everything in P1 beyond "`a0` is built from `c, G, ρ_DE`" is the single number in (2).

### 2. The one statement (S), with its three clauses separated

**S.** *The vacuum answers a baryonic source with a conserved current `j` whose magnitude saturates at the
vacuum acceleration `a0` — one quantum per cell, and the quantum is `a0` — the source is the flux of that
current through the cell (`g_N = j²/a0` as `j → 0`), and no scale other than `a0` enters.*

- **S1 (capacity):** `|j| ≤ a0`, one quantum per cell; the quantum *is* `a0`.
- **S2 (flux):** the source couples to the second power of the current: `g_N → j²/a0` as `j → 0`.
- **S3 (no free function):** the response is the least-degree rational map satisfying S1–S2.

S1 and S2 are physics; **S3 is the "no free function" demand of the task**; the clause "the quantum *is*
`a0`" in S1 is what ties P2 to P1. S is *not* an information statement — §4 shows why information cannot
supply the coefficient.

**Premises, and which are new** (task part (b)):

| # | premise | status |
|---|---|---|
| B1 | `g = g_N + j`, `j` the vacuum's extra acceleration | **in the theory** (PAPER49 action, `g = g_N + u`) |
| B2 | deep limit `g_N → j²/a0` | **in the theory** (P2's own deep limit, BRIEF §1) |
| B3 | `|j| ≤ a0` — the current saturates at the vacuum scale | **new** (AG6B's finite capacity A3, pinned to `a0` here) |
| B4 | the cell quantum is exactly `a0` | **new** — this single clause is what produces P2 rather than the quadrature |
| B5 | least-degree rational response (no free function) | **new** (the task's demand; equivalent to "one scale only") |
| B6 | `a0` is built from `c, G, ρ_DE` | **in the theory** (P1's dimensional content) |
| B7 | `a0 = cH_Λ/𝒩` with `𝒩` a rational count | **new, and false** — refuted by (13) |
| B8 | horizon entropy `S = A/4G`, `T_dS = H/2π` | **standard physics**, not framework-specific |

B1, B2, B6 are the theory; B3–B5 and B7 are new; B7 is the one that fails, and B4 is the clause doing the
work of "deriving P2" — a normalisation, not a consequence. The SPARC `g_bar` convention is external; see
`a10_results.json.external_inputs`.

### 3. P2 follows exactly (and the family around it)

With `g = g_N + j` and S3, the least-degree map with a pole at `j = a0` and `g_N ~ j²/a0` at small `j` is

    (3)  g_N = j²/(a0 − j)        ⇔   û² + û ŝ = ŝ .

Eliminating `j` between (3) and `g = g_N + j`:

    (4)  (g − j)(a0 − j) = j²   ⇒   j(a0 + g) = a0 g   ⇒   j = a0 g/(a0+g)   ⇒   g_N = g²/(g + a0).

**That is P2, identically** (K1). The same elimination for a cell whose quantum is `a0/b` gives the family
AG6B already registered (`R_n(u) = u²/(a0 − n u)`):

    (5)  û² + b ŝ û = ŝ    ⇔    g_N = u²/(a0 − b u),   u = g − g_N
    (6)  b = 1:  g_N = g²/(g+a0)                     (P2, Langmuir / pumped two-level, AG6B C-1)
    (7)  b = 2:  g² − g_N² = a0 g_N                  (quadrature a0-line, Deser–Levin, AG6B E-1)

both verified identically (K2, K3). So S derives P2 **and** its neighbour; the only difference between them
is the value of the cell's quantum, `q = a0` (b=1) or `q = a0/2` (b=2). S fixes `q = a0` by declaration,
not by argument — that is the kernel-side residual freedom, and §4 shows it is not a small one.

### 4. What S fixes and what it does not

Four exact statements; (8) and (9) hold for every `b`, (10) and (11) do not:

    (8)  deep limit:      lim_{ŝ→0} (g−g_N)²/(a0 g_N) = 1        for every b   (K5)  → cannot select b
    (9)  capacity:        sup (g−g_N)/a0 = 1/b                   (K6)          → b only via the quantum
    (10) deep shape:      g/√(a0 g_N) = 1 + (1 − b/2)√(g_N/a0) + O(g_N/a0)     (K4)
    (11) strong field:    lim_{y→∞} y(ν−1) = 1/b,  y ≡ g_N/a0,  ν ≡ g/g_N      (K7)

So S pins the deep limit (which every capacity theory shares) and leaves **one integer**: `b`, equivalently
the quantum's normalisation `q/a0`. P2 is the member with `q = a0`, which S1 asserts; the same derivation
with `q = a0/2` gives the quadrature. Since the assertion `q = a0` is a normalisation and not a consequence,
the kernel-side residual freedom is real, and it is not small — (10) and (11) show it is a measurable shape
difference at both ends of the RAR.

### 5. P1 fails: the coefficient is not a count

Read P1 as an information statement (candidate (i)); units `c = 1` here. The de Sitter horizon stores
`S = A/4G = π/(G H²)` nats, i.e. one nat per cell per e-fold. Any such principle can only return the horizon
acceleration divided by a normalisation `𝒩` built from the cell count, so the class has one free number:

    (12)  a0 = c H_Λ / 𝒩     ⇒     κ = √(8π/3)/𝒩          (exactly, from (1))

The admissible cell counts of horizon thermodynamics and their κ:

| 𝒩 | geometric meaning | κ = √(8π/3)/𝒩 |
|---|---|---|
| 4π | cells over the full horizon sphere | **0.230329** |
| 2π | modular / one-sided (Unruh) normalisation | **0.460659** |
| π | hemisphere | **0.921318** |
| 1 | surface gravity (`cH_Λ` itself) | **2.894405** |

`κ = 1/2` requires `𝒩 = 2√(8π/3) = 5.788810` — not a count, nor any rational multiple of a count:

    (13) THEOREM. If a0 = r · cH_Λ with r ∈ ℚ, then κ = r√(8π/3) ∈ √(8π/3)·ℚ.
         κ = 1/2 would need r = 1/(2√(8π/3)), i.e. 8π/3 = 1/(4r²) ∈ ℚ, i.e. π ∈ ℚ.
         π is irrational (Lindemann), so no rational count can give κ = 1/2.

Checked exactly: `sympy` returns `is_rational = False` for `√(8π/3)` and for `κ/√(8π/3)` (K10); the nearest
admissible count is 7.9 % away in κ (K9); `Z` is irrational (K11). The corollary is what matters for the κ
programme: **any "derive κ" lane whose output is (rational counting) × (a horizon scale) searches an empty
set** — not because the algebra is hard, but because 1/2 is not in it. `κ = 1/2` is the convention
`a0 = (1/2)c²√(Λ/8π)`: the quantum is half the free-fall acceleration at ρ_DE. The half is a definition.

### 6. Candidate (ii) is dead on the repo's own numbers

MaxEnt at a fixed moment gives an exponential family, but neither family is in (5): AG6B measured
fixed-`⟨c⟩` cells → `U = (a0/2)(1−e^{−2x})`, `n_cap = 2`, `n₁ = 4/3`, **out of family**; fixed-`⟨c²⟩` cells →
half-normal/erfc, `n_cap = π`, **out of family** (K12, read from `ag6b_media_results.json`). And the
quadrature is not a MaxEnt law at all: it is the *moment identity* `x² = ⟨n²⟩` for a Poisson cell with mean
`s` (K13, `⟨n²⟩ = λ² + λ` exactly). So "which moment is held fixed" does **not** reduce n=1 to n=2; the two
kernels differ in the *coupling* to the cell (log-fugacity occupation vs relativistic dispersion), which is
precisely the free function (ii) was supposed to remove.

### 7. One new consequence, not P1 and not P2: `A = 1 − 1/(2T)`

(10) and (11) are two faces of the same integer, so the family predicts a cross-regime relation between the
deep-limit shape `A` and the strong-field anomaly coefficient `T`:

    (14)  A(b) = 1 − b/2 ,   T(b) = 1/b    ⇒    A = 1 − 1/(2T)      (identically, K14)
          b=1 (P2):        A = 1/2,  T = 1     → constant anomaly a0
          b=2 (quadrature): A = 0,   T = 1/2    → constant anomaly a0/2

`T` is the coefficient of the constant sunward anomaly, `δg = T·a0`. Numbers on the canonical footing,
against the registered Earth limit `3.66e-14 m s⁻²` (read at runtime from
`real_research/reviews/mi_disformal_tail_freedom_2026.py`):

    (15)  T=1/2:  a0/2 = 4.680e-11 = 1278.69 × bound     (reproduces the registered 1279×, K8)
          T=1:    a0   = 9.360e-11 = 2557.38 × bound     (new)

**This answers the asymptotic half of the BRIEF's open question for lane C2**: the canonical law does not
escape the cure — it needs it *twice as badly* as the quadrature. Both are excluded at >10³×, so the turn-off
is mandatory for P2 too, with the same functional form and the anomaly doubled.

### 8. The failure mode, as neighbouring principles

Each row is a one-sentence principle of the same standing as S, and each changes the answer:

| neighbouring principle | consequence |
|---|---|
| "one nat per cell per e-fold, counted over the full horizon sphere (4π)" | κ = **0.2303** |
| "…with the modular (Unruh) normalisation (2π)" | κ = **0.4607** |
| "…counted over the hemisphere (π)" | κ = **0.9213** |
| "the horizon's surface gravity is the cell (`𝒩 = 1`)" | κ = **2.8944** |
| "the cell's quantum is `a0/2`, as the relativistic dispersion forces (Deser–Levin)" | b = 2: `g² − g_N² = a0 g_N` |
| "the response reaches its deep limit with no √ŝ correction" (`A = 0`) | b = 2: same quadrature |

The κ rows span a factor 12.6 end-to-end (0.2303–2.8944) and a factor 4 across the three thermodynamic
counts; the canonical 1/2 is not on the list at any resolution. The b rows show that the quadrature is
selected by *two* independently natural statements, so P2 is not the default — it needs B4, the declaration
that the quantum is the full `a0`. That is exactly how much is being assumed: one number per sector, and
neither number is fixed by the principle.

## Status

**NO-GO(obstruction)**, with two derived sub-results.

- **P2 — DERIVED** from S (S1+S2+S3), identically, with the capacity `a0` (K1–K3, K6).
- **P1 — NO-GO(obstruction).** The scaling `a0 ∝ c√(Gρ_DE)` is dimensional and follows; the coefficient is
  not a count (13), and `κ = 1/2` is a normalisation. Nearest admissible count: 7.9 % away; spread: factor 4.
- **The residual freedom is two numbers**: `κ` (scale) and `q/a0` (kernel quantum). They are independent —
  (κ=1/2, b=1) and (κ=1/2, b=2) are both coherent, and the data do not separate them (AG6B, global Υ:
  0.1009 vs 0.1083 dex, b=1 slightly preferred; BRIEF §1 paired: 0.178 vs 0.220, b=2). Empirical tie.

## Checks

18 checks, all PASS (`a10.out`: `A10 COMPLETE: 18/18 checks PASS.`), each printing value and threshold.

| id | what it measures | measured | threshold |
|---|---|---|---|
| K1 | b=1 member minus `g²/(g+a0)` | 0 (exact) | identically 0 |
| K2 | b=2 member minus `(√(a0²+4g²)−a0)/2` | 0 (exact) | identically 0 |
| K3 | both inverse forms `g(g_N)` | exact | both identities |
| K4 | deep coefficient `A(b)` | 1/2, 0, −1/2 | exact |
| K5 | `lim (g−g_N)²/(a0 g_N)` for b=1,2,3 | 1, 1, 1 | all = 1 |
| K6 | `sup (g−g_N)/a0` for b=1,2,3 | 1, 1/2, 1/3 | = 1/b |
| K7 | `lim y(ν−1)` | 1 (b=1), 1/2 (b=2) | = 1/b |
| K8 | a0/2 and a0 vs Earth limit | 1278.69 / 2557.38 | 1279 to 1 %; ratio exactly 2 |
| K9 | nearest admissible κ to 1/2 | 0.0787 rel. | > 0.01 |
| K10 | `√(8π/3)`, `κ/√(8π/3)` rationality | both irrational | both False |
| K11 | `Z`, `2Z` | 5.788810, 11.577620 | `Z` irrational, `|Z−5.788810|<1e-6` |
| K12 | AG6B MaxEnt rows in family? | False, False | both False |
| K13 | Poisson `⟨n²⟩ = λ²+λ` | exact | identity |
| K14 | `A − (1 − 1/(2T))` | 0 | identity |
| K15 | SPARC `A` at Υ=0.5 / 0.7 | 0.8922±0.0438 / 0.3427±0.0427 | swing > 0.5 |
| K16 | Υ accuracy needed to split b | 0.061 | < 0.10 |
| K17 | Υ accuracy needed for the capacity bound | 0.018 | < 0.10 |
| K18 | P1 round trip on both normalisations | 9.3512e-11, 9.3542e-11 | within 0.3 % of 9.36e-11 |

Data checks use 3391 points in 175 SPARC `rotmod` curves; `g_bar = (V_gas² + Υ V_disk² + 1.4Υ V_bul²)/r`,
`g_obs = V_obs²/r`. The measured `A` is neither 1/2 nor 0 at either Υ; the full Υ band (0.5→0.7) moves it by
0.549, more than the whole b=1↔b=2 separation (0.5), and a 3σ split needs ΔΥ = 0.061 against the ~0.10 that
SPARC supplies; the capacity bound needs Υ to ±0.018. So **SPARC cannot decide `b`** (K15–K17), and (14) is a
cross-regime prediction with a quantified instrument requirement, not a test that has been passed.

## What this does not do

- **It does not derive κ**, and it proves that no counting principle of the stated class can. It does not
  exclude a principle that fixes the *quantum's normalisation* by something other than counting (a
  variational principle on the horizon's modular Hamiltonian, say). That is the open door, and it is a
  different door from the ~50 count-based lanes closed in BRIEF §2 (sonnet55 `puzzle_32pi`).
- **It does not fix b.** S narrows the kernel to (5) and leaves `q/a0 ∈ {1, 1/2}`; the data tie.
- **It does not test the numerical value of `a0`** — `a0_can = 9.36e-11` is an input throughout.
- **It does not address the turn-off cure.** (15) says the cure is needed for P2; it does not say what the
  cure is, and it does not touch the `y_t ≈ 94–129` value.
- **It does not build a covariant parent** — S is a statement about the static, isotropic response only — and
  nothing here is certified beyond sympy's `simplify`/`limit`/`series` (no Lean).
- **The `A` measurement is crude**: an unweighted fit of `B−1 = A√s` over `ŝ < 0.2`, no error weighting, no
  inclination/distance cuts. It is used only to size the Υ lever arm, never to claim a value of `b`.

## Next

1. **The only viable κ door** named by (13): a principle that outputs an *irrational* number, i.e. one that
   computes a ratio of areas/entropies rather than a count — e.g. `κ = 1/2` as the statement that the modular
   Hamiltonian of a half-horizon patch carries one nat of spectral weight. That is a normalisation statement
   and should be written as one, not as a derivation.
2. **Decide `b`** with a Υ-free tracer at `ŝ ∈ (3,10)` (required Υ accuracy ±0.018, K17): gas-dominated
   dwarfs, where the stellar normalisation is a small perturbation, or a distance-independent sample. A 3σ
   answer either way is worth more than another kernel family.
3. **Register (15) as the C2 answer**: P2 needs the same turn-off, with `a0` (not `a0/2`) as the anomaly.
