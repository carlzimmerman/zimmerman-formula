# GATE_CONVENTION — the x = 2.5 gate: the two readings, and why 152/220 and 304 are both right
(2026-09-17; resolves the apparent 2× between SW01b D and SW06 D2)

## The issue

SW01b D reported **152.1 / 220.3** (canonical / alt). SW06 D2 reported **304.1 canonical** and
**220.3 alt**. The canonical slot differs by exactly 2×. That is not a discrepancy in the
physics — it is two different readings of "the departure at x = 2.5", mixed inside one script.
It is named here because a hostile reader stops at the first unexplained factor of two.

## The two readings

At the gate point the sourced field is g_src = 2.5 a₀ and the uniform external field is
g_ext = 2.5 a₀.

**(i) PER-FIELD reading** — the departure of the SOURCED sector's response from Newton:

```
D_src = S(η) · [ν(2.5) − 1]          ->  ratio = D_int / D_src = 1/S(η)
```

**(ii) DILUTION-INCLUSIVE reading** — the departure of the TOTAL field from the total
Newtonian field (the external field passes through unmodified, so it dilutes the anomaly):

```
g_obs = g_ext + [1 + S(η)(ν−1)] g_src
g_N   = g_ext + g_src
D_tot = S(η)(ν−1) · g_src/(g_src+g_ext)  ->  ratio = (1/S) · (g_src+g_ext)/g_src
```

At the gate, g_src = g_ext = 2.5 a₀, so (g_src+g_ext)/g_src = 2 **exactly** — the 2×.

## The four numbers (computed, both readings × both footings)

| footing | S(2.5) | (i) per-field 1/S | (ii) dilution-inclusive 2/S |
|---|---|---|---|
| canonical (η_c = 0.2034) | 0.006576 | **152.1** | **304.1** |
| alt (η_c = 0.1688) | 0.004538 | **220.3** | **440.7** |

Internal departure D_int = ν(2.5) − 1 = 0.2590 (both footings; ν is footing-independent).

**Both readings clear the 6.4 gate on both footings, by 24× to 69×.** The gate verdict is
reading-independent — which is the point: the 2× carries no physics, only convention.

## What is fixed going forward

- The **per-field** reading (i) is the lane's default — it is the one L264's own asymmetry
  statement uses (26% internal vs ≤ 4% external at the same x), and the one to quote.
- The dilution-inclusive number may be quoted only if labelled as such.
- SW06 D2's alt value (220.3) was already the per-field reading while its canonical value
  (304.1) was the dilution reading: the script is amended to print BOTH readings on BOTH
  footings, so the two can never again be compared as if they were one quantity.
- Neither reading is fitted or tuned: S(η) is the declared scalar response and η_c is the
  measured constant (window [0.028, 0.203], Fornax ≤ 0.145).

## The brief's stop rule, honoured

Both readings exceed 6.4, so the brief's "if the ratio is < 6.4, stop" never fires. The
remaining gates (quadrupole, BTFR slope, ghost) are the ones that have actually killed
candidates — and the ghost/α₂ gate is the open door (G03, SW08).
