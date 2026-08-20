# I002 — The 1 AU anomaly is s·a0(local), not s·a0(cosmic)

**Verdict:** KILL
**Decisive number:** at the physical local DM density (0.4 GeV/cm³, R = 2.84e5) the local
a0 suppression is **S = a0_cosmic/a0_local = 1.10×** (< 3× → the briefed KILL fires); even the
most extreme grid point (R = 1e8) caps the shrink at **S = 15.4×**, so the ephemeris gap
shrinks only **13600× → 885× (canon, a0 = 9.3619e-11)** / **17300× → 1126× (alt,
a0 = 1.1279e-10)** — not closed. Closing it by local suppression alone would need
**R ≈ 7.8e13 ≈ 2.8e8× the local DM density (~1.1e8 GeV/cm³)**, and the galaxy RAR caps usable
suppression at **S ≤ 12.5×** regardless.
**Script:** `runs/i002_local_a0_suppression.py`   (checks: 11/11, exit 0)

## Hypothesis
Because a0 is a field (`a0²(Q) = κ²G(−K(Q))`), the saturated sunward term at 1 AU,
`u_sat = s·a0`, is set by the *local* dark-charge density, not the cosmic mean; using
a0 local instead of cosmic shrinks the ephemeris gap by the local suppression factor and
closes R1's ephemeris end.

## What I actually did
As briefed, I **did not re-derive** the suppression law: I reused the exact expression
`f = a0_local/a0_cosmic = [(1+ν₀²)/(1+ν²)]^(1/4)` with `ν = ν₀·(ρ_local/ρ₀)` from
`real_research/reviews/a0_local_ephemeris_2026.py`, first reproducing its two committed
numbers as a gate (f = 0.141 at ν₀ = 1.77e-4; f = 0.403 at ν₀ = 2.14e-5, both at R = 2.84e5 —
its A3 values, matched to <5%). I then formed ν at the **recombination-pin ceiling
ν₀ = 2.36e-6** (PROTOCOL line 6 / stage76; the *most* suppression-favourable value allowed,
since S grows with ν₀) over the briefed grid ρ_local/ρ₀ ∈ {1e2, 1e4, 4.24e5, 1e6, 1e8},
evaluated f, and divided the in-force ephemeris gaps 13600 (canon) / 17300 (alt) by the
shrink S = 1/f (`new_gap = gap·f`). I report both a0 footings: f is footing-independent, so the
two footings enter only through the two gap numbers. I also added, as owed, the density that
would be required to close the gap, and a cross-check against the stage75 galaxy-coupling
adjudication (cited, not re-derived). No deviation from the spec.

## The math
- Promotion (PROTOCOL line 6, stage75 PART C): `a0(ν)/a0(0) = [(1+ν₀²)/(1+ν²)]^(1/4)`,
  `ν = ν₀·(ρ_local/ρ₀)`, `ν₀ ≤ 2.36e-6`. At the cosmic mean ρ_local/ρ₀ = 1, ν = ν₀ and the
  factor is 1 (normalisation); at higher density ν > ν₀ so the factor `f < 1` (a0 is suppressed).
- The ephemeris anomaly is `u_sat = s·a0_local = s·f·a0_cosmic`; the ephemeris bound is fixed
  in physical units, so the gap (galaxy floor / ephemeris ceiling, stage75 = 13600×/17300×)
  shrinks by f: `new_gap = gap·f`, and `new_gap ≤ 1` (closed) needs `f ≤ 1/gap`.
- Grid at ν₀ = 2.36e-6 (computed, monotone in R):

  | ρ_local/ρ₀ | ν | f = a0_l/a0_c | S = 1/f | new_gap canon | new_gap alt |
  |---|---|---|---|---|---|
  | 1e2 | 2.36e-4 | 1.00000 | 1.000 | 13600 | 17300 |
  | 1e4 | 2.36e-2 | 0.99986 | 1.000 | 13598 | 17298 |
  | 4.24e5 | 1.001 | 0.84076 | 1.189 | 11434 | 14545 |
  | 1e6 | 2.36 | 0.62462 | 1.601 | 8495 | 10806 |
  | 1e8 | 236 | 0.06509 | 15.362 | 885 | 1126 |
  | **2.84e5 (physical)** | **0.670** | **0.91142** | **1.097** | **12395** | **15767** |

- Density to close the gap: `new_gap ≤ 1 ⇔ 1+ν² = gap⁴ ⇔ ν = gap²`.
  Canonical: ν = 1.85e8 → R = ν/ν₀ = 7.84e13 → ρ = 7.84e13·(0.265·9.47e-27)/1.7827e-21
  = 1.10e8 GeV/cm³ ≈ 2.8e8× the local 0.4 GeV/cm³. Alt: R = 1.27e14, ρ = 1.79e8 GeV/cm³.
- Galaxy coupling cross-check (stage75 adjudication 2026-08-17, *cited not re-derived*):
  "a LOCAL a0 HURTS" — suppressing a0 by f forces the saturation s up so the galaxy-RAR
  product s·f stays ~fixed or grows (0.435 at f=1 → 2.00 at f=0.1) and is unsatisfiable below
  f = 0.080, capping usable suppression at S = 1/0.080 = 12.5×.

## Numbers
| quantity | value | note |
|---|---|---|
| GATE f(1.77e-4, 2.84e5) | 0.1410 | reproduces prior file A3 (0.141) |
| GATE f(2.14e-5, 2.84e5) | 0.4029 | reproduces prior file A3 (0.405) |
| ν₀ used | 2.36e-6 | recombination-pin ceiling; most suppression-favourable |
| **physical-density suppression S** | **1.097×** | R = 2.84e5 (0.4 GeV/cm³) |
| **max suppression over grid** | **15.36×** | at R = 1e8 (unphysical) |
| new_gap, physical density | 12395× (canon) / 15767× (alt) | essentially unchanged |
| **new_gap, max grid (R=1e8)** | **885× (canon) / 1126× (alt)** | still 3 orders over |
| density to close canon gap | R = 7.84e13 = 1.10e8 GeV/cm³ | 2.8e8× the local DM density |
| density to close alt gap | R = 1.27e14 = 1.79e8 GeV/cm³ | 4.5e8× the local DM density |
| galaxy-RAR suppression cap | S ≤ 12.5× (f ≥ 0.080) | stage75 adjudication |
| ephemeris need vs galaxy cap | 13600× / 12.5× = 1088× | irreconcilable |

## Why this verdict
The briefed **PASS** ("gap shrinks by >100×") is **NOT met**: the maximum shrink over the whole
briefed grid is S = 15.4× (at the unphysical R = 1e8); at the physically-motivated local density
it is S = 1.10×. The briefed **KILL** ("suppression < 3×") **fires** at the physical density
(1.10× < 3×). Both readings agree: local a0 suppression, at the recombination-pinned ν₀, shrinks
the 13600×/17300× ephemeris gap to at best 885×/1126× — it does not close it. Worse, the very
suppression the ephemeris demands (S = 13600×, i.e. f < 7.4e-5, i.e. R ~ 7.8e13 ≈ 3e8× the local
DM density, ~1e8 GeV/cm³, between white-dwarf and neutron-star matter) is *forbidden by the
galaxy RAR*, which caps usable suppression at S ≤ 12.5×. KILL: local a0 cannot close R1's
ephemeris end, and it provably cannot — the 13600×/17300× liability stands.

## Against my own result
- **Direction of "divide by it."** The brief says "divide the gap by it," but with
  `f = [(1+ν₀²)/(1+ν²)]^(1/4) < 1` a literal `gap/f` would *grow* the gap; the only coherent
  reading of PASS/KILL is `new_gap = gap·f` (suppressing a0 shrinks the anomaly by f). I used that.
  If Carl meant the inverse convention, the numbers invert but the *conclusion does not*: S = 1.1×
  at the physical density is < 3× under either convention, so KILL holds.
- **The physical density is an assumption.** I took ρ_local = 0.4 GeV/cm³ (R = 2.84e5) from the
  prior file. The local DM density has a ~factor-of-2 uncertainty; even doubling R to 5.7e5 moves
  S from 1.10× to ~1.16× — still < 3×. The verdict is insensitive to this.
- **The galaxy-cap cross-check is a citation, not a re-derivation.** The "S ≤ 12.5×" cap comes
  from the stage75 2026-08-17 adjudication (the s·f product, unsatisfiable below f = 0.080), which
  I did not re-derive here; it *strengthens* the KILL but is owed its own check. If that coupling
  were wrong, the KILL still stands on the grid alone (15× << 100×, physical 1.1× < 3×).
- **ν₀ = 2.36e-6 is the ceiling, i.e. the best case.** I used the *largest* allowed ν₀, which
  *maximises* S. A smaller ν₀ gives *less* suppression, so no allowed ν₀ can rescue the gap.
- **EFE is deliberately excluded.** I001 found the EFE relief is ~1.0× (an artefact), so I did not
  compound it; the verdict is the pure local-a0 effect.

## Owed / not computed
- A self-consistent s·f product from the galaxy RAR on the real SPARC data (to replace the cited
  12.5× cap with a computed one) — owed to a later idea; here it is quoted from stage75.
- A per-environment a0 field solution (a0(r) across the solar system to the galaxy outskirts)
  rather than a single local factor — would need the PDE, not this algebraic reduction.
- Whether any *legal* kernel outside the a0-line (slower saturation in radius) changes the
  density-to-close figure — not tested here; the density requirement (R ~ 7.8e13) is kernel-independent.

## Files touched
- `runs/i002_local_a0_suppression.py` (script, 11/11 checks, exit 0)
- `results/I002_local_a0_suppression.md` (this file)
- `LEDGER.md` (one row appended)
- read-only: `real_research/reviews/a0_local_ephemeris_2026.py`,
  `nbody_2026/stage75_the_closed_theory_2026.py`
