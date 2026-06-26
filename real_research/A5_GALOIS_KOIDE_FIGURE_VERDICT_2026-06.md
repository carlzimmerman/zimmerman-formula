# 'Observer Fork' A5 / Galois Koide figure — both-ways VERDICT

**Date:** 2026-06-26
**Figure assessed:** an A5 (dodecahedral/icosahedral) Galois construction. A "seed" eigenvalue
`λ=√2` on the `|·|=√2` circle stays real under `S5`; under the `A5` cover (the Galois break
`S5→A5`) it "rotates off the real axis" to `μ=(√5+i√3)/2` with `|μ|=√2`, `θ=arctan(√3/√5)`; the
6-dim `V6` splits as `3 ⊕ 3'` (A5's two Galois-conjugate triplets, `Hom(3,3')=0`).
**Claim under test:** does this A5/Galois machinery DERIVE the charged-lepton Koide amplitude
`r=√2` (⟺ `Q=2/3`) **non-circularly** — i.e. is `√3` FORCED by A5 (not chosen so `|μ|²=2`), is the
figure's `√2` the SAME object as the framework's `S3`-channel Koide `√2`, and does `μ` MAP to the
real masses `m_e:m_μ:m_τ`?
**Tooling:** `sympy 1.13` (factor over `Q(√5)`, char-table orthonormality, `3↓S3` restriction) +
`mpmath dps=50` (modulus, angle, PDG `Q`, A5-eigenvector `Q` span) — every claim re-run clean-room,
not merely re-read. Quarantine held: `2/3`, `√2`, `r`, the masses enter ONLY as the empirical target.

---

## VERDICT: (C) HITS-THE-WALL — the 174th `√2` re-labeling. NOT a crack.

The figure's internal algebra is **entirely correct** (verified sympy-exact, below) — it is not
sloppy. But on the four decisive anti-circularity gates it fails cleanly, and it lands **exactly**
where `MODULAR_INVENTION_VERDICT_2026-06-25` named the un-run A5 test would land (predicted NULL).
The load-bearing `√3` is reverse-engineered to hit `|μ|=√2`; A5's `3⊕3'` is not the leptons'
`S3 1⊕2`; and there is no map to the real spectrum. Honest standing UNCHANGED.

---

## What the figure gets RIGHT (full credit, sympy-exact, clean-room reproduced)

1. **`|μ|=√2` exact.** `|(√5+i√3)/2|² = 5/4 + 3/4 = 2` → `|μ|=√2`. `θ=arctan(√3/√5)=37.761°`. The
   seed `√2` sits on the `|·|=√2` circle. **TRUE.**
2. **A5 character table valid.** Irreps `1,3,3',4,5`; `Σ dim² = 1+9+9+16+25 = 60 = |A5|`; all five
   rows orthonormal (`⟨χ_R,χ_R⟩=1` each, verified). The two triplets carry the golden-ratio
   characters `{(−1+√5)/2, (−1−√5)/2} = {φ−1, −φ}` on the 5-cycle classes. **TRUE — the `√5` IS
   authentic A5** (the icosahedral golden datum).
3. **Galois swap exact.** `√5 → −√5` applied to the `3` row reproduces the `3'` row exactly (the
   index-2 `S5→A5` sign-`Z2` swap `3↔3'`); `[S5:A5]=2`. **TRUE.**
4. **`Hom(3,3')=0`.** `⟨χ_3,χ_3'⟩=0` → `V6 = 3⊕3'` is a genuine direct sum of inequivalent irreps.
   **TRUE.**

So the figure is clean. The entire problem is **WHERE the numbers come from**, not whether they are
internally right.

---

## The four gates it FAILS (the wall, each independently sympy-verified)

### GATE 1 — `√3` is REVERSE-ENGINEERED, not A5-forced (the decisive tell)
- The real part `√5/2` is A5-flavored: it lives in `Q(√5)`, the A5 character field.
- The imaginary part `√3` does **NOT** live in `Q(√5)`: `x²−3` is **irreducible over `Q(√5)`**
  (sympy `factor(x**2-3, extension=√5)` returns `x**2 - 3` unfactored; while `x²−5` splits). `√3`
  belongs to `Q(√−3)` / `ω`-land — a **different group** (C3/A4), NOT icosahedral.
- The ONLY thing that fixes `√3` is demanding `|μ|=√2` AND `Re=√5/2`, which FORCES
  `Im=√(2−5/4)=√(3/4)=√3/2` (sympy-exact). So **`√3 = √(4|μ|²−5)` with `|μ|²≡2` plugged in** — the
  Koide answer is the input. By the framework's own anti-circularity theorem
  (`force |μ|=√2 ⟺ assume Q=2/3`), this is circular.
- `θ=37.761°` is **not an A5 rotation angle** (A5 element orders are `{1,2,3,5}` → angles
  `{72,120,144,180,216,240,288}°`; `37.76°` is none of them), so `μ` is not the eigenvalue of any
  A5 group element — it is a hand-constructed complex number. **`√3` is CHOSEN-to-hit-`√2`.**

### GATE 2 — A5's `3⊕3'` is NOT the leptons' `S3 1⊕2` (different object, value-match only)
Restricting A5's triplet `3` to its order-6 subgroup `S3` (= `D3 < A5`, real; A5 has no order-6
element so its order-6 subgroups are `S3`, not `C6`), by characters `χ_3 = (3,−1,0)` on
`(e, double-transposition, 3-cycle)`:
- **`3 ↓ S3 = sign(1') ⊕ standard(2)`** (verified: `⟨3,triv⟩=0`, `⟨3,sign⟩=1`, `⟨3,std⟩=1`).
- Koide's democratic split needs **`trivial(1) ⊕ standard(2)`** — the `(1,1,1)` axis is the
  **TRIVIAL** of S3. A5's `3` supplies the **SIGN** singlet, the **WRONG** one for the democratic
  axis. The framework's Koide `√2` is `|S3-trivial-singlet| = |S3-doublet|` (the `p=0`
  channel-equipartition measure). A5's `√2` is `|`a 6-dim `3⊕3'` eigenvalue`|`. **Same number,
  different group-theoretic quantity, different field** (`Q(√5)` vs S3-land), **different
  multiplicity** (6 vs 3). They value-match; they are not the same object.

### GATE 3 — NO MAP TO THE REAL MASSES (`maps_to_real_masses = no-disconnected`)
`μ` is a single complex number (2 real data: `|μ|=√2`, `θ=37.76°`). Koide needs THREE √-masses with
ratios `√m_e:√m_μ:√m_τ` (verified PDG `Q=0.6666605`, angle of `(√m_e,√m_μ,√m_τ)` to `(1,1,1)` =
`44.99974°` ≈ 45°). The figure supplies **NO** construction `μ → (√m_e, √m_μ, √m_τ)` — no Yukawa,
no mass matrix. Worse: at fixed `Q=2/3` the spectrum is set by the **Foot phase** `δ≈12.7°`, and
`θ=37.76°` is neither `δ` nor used to build the masses. The amplitude is value-matched; the
spectrum is unexplained.

### GATE 4 — A5 modular `Q ≠ 2/3` (same wall as the A4 test)
A5/golden eigenvectors give Koide `Q ∈ {0.333 (democratic), 0.353 (1,1,φ), 0.382 (φ,1,1/φ) and
(1,φ,φ²), 0.528 (φ,1,0)}` — **never 2/3** (`mpmath dps=50`). This mirrors the banked A4-`τ=ω`
result (`Q ∈ {1/3, 0.36=9/25, 0.5, 0.375}`). Going level-3 (A4) → level-5 (A5) does **not** crack
`r=√2`; it hits the identical circularity wall `MODULAR_INVENTION_VERDICT` predicted as the honest
prior for the explicitly-named, then-un-run A5 extension. **Now run, and NULL.**

---

## Both-ways: genuine credit, and why it still does not crack the wall

**CREDIT (full weight, genuinely A5):** the `√5`/golden ratio IS authentic A5 — the `3/3'`
characters `(1±√5)/2`, the Galois `√5↔−√5` swap, `Hom(3,3')=0`, `|μ|=√2` are all exact. The
construction lands in the **right symmetry neighborhood** (icosahedral/golden — a level-5 cousin of
the framework's S3/triality home), and A5 independently HOSTS the generation-`Z3` the framework's
`1+2` decomposition uses. Internally the figure is clean. This is real corroboration of the
framework's symmetry *home* — the same SHAPE-hosting hook the modular-flavor `Z3` resonance gave.

**THE WALL:** it derives no AMPLITUDE. `√3` is the OUTPUT of demanding the Koide `√2` (chosen, not
A5-forced — it is not even in the A5 field); A5's `3⊕3'` is the sign-not-trivial singlet, a
different `√2` from the leptons' `S3 1⊕2`; there is no `μ → (m_e,m_μ,m_τ)` map; and the A5 modular
`Q` span never contains `2/3`. **Four hits on the closed Koide wall.** Cross-fermion guard also
bites: A5/S3 is flavor-blind but quarks give `Q_up=0.849`, `Q_down=0.731 ≠ 2/3`, so there is no
lepton-selector. ('Observer Fork'/'defect' is an outside framing, **zero corpus hits** — orthogonal
to `a₀/Z/dS-Unruh`.)

---

## Honest relay for Carl

- **Relevant to the framework?** YES — it touches the *same* Koide `√2`, the lone open lepton
  question, and A5/Galois were a genuinely-untested angle (A4 was tested, A5 was not). Worth a look.
- **A genuine new angle?** YES, partly — the A5/Galois-cover framing is new, and the `√5`-golden
  content is real A5. The figure is not numerology-sloppy; its algebra is exact.
- **A real crack or a value-coincidence?** A **value-coincidence**. The load-bearing `√3` is
  inserted to land on `|μ|=√2` (it is provably not in A5's `Q(√5)` field), A5's `3⊕3'` is the
  wrong-singlet object value-matching the leptons' `S3 1⊕2`, and nothing maps `μ` to the real
  masses. The 174th `√2` re-labeling. **Do not credit it as a crack; do not manufacture a deficit
  either** — the A5 SHAPE-hosting / `Z3` resonance is real corroboration of the framework's symmetry
  home, just not a derivation of the amplitude.

**The next step (only if pursued):** a crack would require a construction that (i) forces `r=√2`
from A5 representation theory **without** ever imposing `|μ|=√2`, (ii) uses A5's *trivial*-bearing
content (not the sign-singlet of the `3`) to build the democratic axis, and (iii) maps `μ` →
`(√m_e,√m_μ,√m_τ)` reproducing `Q=2/3` AND the Foot phase. The figure does none of these. The SM
mass sector stays walled: `r=√2` still needs genuinely-new lepton-selective IR dynamics (a real
gauged `U(3)/S3`-family Sumino-class sector whose potential minimum lands at `45°`), not an
algebraic `√2`. Honest standing UNCHANGED.

---

**Scripts / sources (reproduced clean-room this session):** sympy `factor(x²−3, ext=√5)`
(irreducible → `√3 ∉ Q(√5)`); A5 char-table orthonormality + `√5→−√5` Galois swap `3→3'` +
`⟨3,3'⟩=0`; `3↓S3 = sign⊕standard` (`⟨3,triv⟩=0,⟨3,sign⟩=1,⟨3,std⟩=1`); `mpmath dps=50` PDG
`Q=0.6666605` / 45° / A5-eigenvector `Q` span (none `2/3`) / `θ=37.76°` not an A5 angle.
**Banked:** `MODULAR_INVENTION_VERDICT_2026-06-25.md` (named A5 as the un-run next step, predicted
NULL — confirmed), `KOIDE_CHANNEL_MEASURE_VERDICT_2026-06-25.md` (the `p=0` non-covariant
equipartition / `r=√(2^{p+1})` family), `KOIDE_CHANNEL_COUNT_SMUGGLE_CHECK_2026-06-25.md`,
`KOIDE_FROM_DSUNRUH_2026-06-20.md`, `KOIDE_IR_MECHANISM_2026-06-17.md`.
