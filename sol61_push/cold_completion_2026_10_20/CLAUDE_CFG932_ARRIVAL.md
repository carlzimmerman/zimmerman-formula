# Provisional CFG932 arrival audit

Audit date: 2026-10-20. Scope: the newly arrived, uncommitted CFG932 primary script,
derivation, main output and mutation controls. **Audited, not executed:** the lane
was not rerun. Only saved-number arithmetic and the stated profile formulas were
independently evaluated. No frozen criteria or original outputs were changed.

**Verdict:** the saved energy identity and reported class arithmetic check out.
There is a material endpoint-accounting defect in the high-supply bracket:
five rows assign zero core cost to a positive primordial surplus because no
equal-mass crossing was found. Consequently the saved Q3 class is an accurate
transcription of this implementation, but is not yet an audited physical
universal-coupling window. It neither closes the four-dwarf problem nor supplies
a microscopic transport kernel.

## 1. Exact arrival and limits of provenance

The frozen criteria are committed at
`dce2a2e3da65565cd30b4b2c0d20b8cf4b3e8c42`. At inspection, the primary
script, derivation and results were untracked local files; no CFG932 README
existed. Local HEAD when the receipt was recorded was
`ac09dba80e1b8224ce5f00675657b101a9b90623`, which is context, not a CFG932
result-source commit. The complete current-byte receipts are in
`sources_cfg932.json`.

| Artifact | SHA256 |
|---|---|
| `cfg932.py` | `b408efe5b735a6332b4325d6afdb7fcc166bbb718401ce5b317eb9bf9563cc50` |
| `cfg932_results.json` | `b8b638ef03faff9b3e3c70fdfcb382915e3024cf800ea219d129b0b861d79c6e` |
| `cfg932.out` | `fae773c5720be97c61b815aa0b7fd4cfd59e1e1f047735fcf1f7831d399b7442` |

These hashes agree with the parent audit's arrival snapshot. No original
bounded-runner manifest, input-before/after receipt, execution versions,
runtime or peak-memory measurement accompanies this arrival. Current source
association is therefore pinned, while generation-time provenance remains
provisional. The documented regeneration command is `OMP_NUM_THREADS=1 nice
-n 10 python3 cfg932.py` from the lane directory; it was not executed here.
Separate `cfg932_posthoc.*` files also appeared and are inventoried by hash only;
their changed questions/results are outside this primary-arrival audit.

## 2. Q1 energy identity: supported for the stated phenomenological system

For CFG638's position drift plus centered velocity OU bath, with isolated or
zero-flux boundaries and symmetric Newtonian Green's function, the equations give

```
d(K_c + K_b + W)/dt = P_drift + P_bath,
W = (1/2) integral rho_tot Phi dV,
P_drift = integral rho_c v_s . grad(Phi) dV,
P_bath = integral (alpha/tau) [3 rho_c sigma_J^2 - tr(Pi)] dV.
```

The two-sided rule has `v_s = alpha tau (g_law - g)`, hence
`P_drift = alpha integral rho_c tau g . (g - g_law) dV`. In spherical
symmetry a cumulative surplus produces outward drift and positive matter-sector
work. Ordinary gravitational exchange with baryons cancels in the total
matter ledger; the model contains no direct feedback payment for this extra
work. These are the same Class-A/Newtonian equations audited separately in
`GRAVITY_ACTION_AUDIT.md`, not a deduction from the canonical ID tether action.

The saved drift-only test has no OU evolution and leaves element velocities
untouched, so its tested identity is specifically `Delta W = integral P_drift dt`.

| Quantity | Saved value, independently checked arithmetic |
|---|---:|
| Two-sided final time / steps | 200 / 804 |
| `W0` | -42.69209979683711 |
| `Delta W` | 25.302081067941938 |
| `Delta W / abs(W0)` | 0.5926642444000018 |
| `integral P_drift dt` | 25.349227329224004 |
| Relative identity residual | 0.0018633353183663936 |
| Relative mass error | 4.736951571734001e-16 |

The residual is below the frozen 2% threshold and the energy change exceeds
the frozen 0.001 threshold, supporting **NON-CONSERVING for the matter sector
of this drift prescription**. The one-sided null control has zero active
steps and zero work: it does not independently test a nontrivial inward-flow
energy balance. The gated prescription and full OU bath were derived, not
numerically evolved in this test.

Booking `Q = -rho_c v_s . grad(Phi)` to a dynamical partner can cancel drift
work by construction; it does not automatically cancel the OU bath source.
The derivation itself acknowledges the bath's unnamed partner. An exact
constant cosmological term cannot provide such exchange. This is not a
no-go for a separately constructed conservative matter model or a proof of a
closed covariant partner theory.

## 3. Controls and window arithmetic

The saved K1 analytic NFW/Plummer comparisons pass their relative `1e-6`
criterion, with maximum recorded error `1.2381207170619746e-12`. K2 reproduces
the CFG541 catchment ratio exactly at saved precision, the edge to
`2.220446049250313e-16` relative, and the continuous/cell phantom mass to
`0.0001039949994142697`. K3's canonical whole-catchment Jeans comparisons pass
the declared tolerance; these are two central rows, not all profiles/corners.
Their direct/half-Delta-W differences are about 0.2443% (MW) and 0.0512%
(Draco). These are saved controls, not rerun controls.

The mutation output reports 28 zero-cost comparisons and 14 acceleration-scale
sensitivity comparisons passing, with exit 1 as explicitly required by the
mutation convention. Two near-Newtonian MW phantom values underflow to zero
and the serialized ratio is Infinity; this limits interpretation of that
ratio's magnitude but not the stated greater-than-ten sensitivity test.

Recomputing all 72 saved corners from the raw grid energies and available
energies reproduces every stored epsilon and nonempty flag. Footings were
kept separate. For every finite nonzero core cost the independently computed
gross-transport net agrees with primary measure b to at most
`2.3259952531828887e-6` relative; the gross positive cost is no smaller than
the net within that discretization accuracy.

| Measure / starved set | Saved nonempty count | Class |
|---|---:|---|
| b / S_A | 36 / 72 | BRACKET-DEPENDENT |
| b / S_B, adding Fornax-like | 33 / 72 | BRACKET-DEPENDENT |
| a / S_A | 36 / 72 | BRACKET-DEPENDENT |
| a / S_B | 33 / 72 | BRACKET-DEPENDENT |
| c / S_A | 30 / 72 | BRACKET-DEPENDENT |
| c / S_B | 27 / 72 | BRACKET-DEPENDENT |
| b / S_A, canonical alone | 12 / 36 | BRACKET-DEPENDENT |
| b / S_A, alternate alone | 24 / 36 | BRACKET-DEPENDENT |

At the central canonical corner the saved interval is empty:
`[7.388553159480013e-11, 8.16793803663621e-15)`.
At the central alternate corner it is nonempty:
`[0, 4.619873973450045e-15)`. These are conditional diagnostic intervals, with
the endpoint caveat below; no numerical universal feedback coupling has been
derived.

## 4. Material endpoint defect: missing receiver and false zero-cost branch

At `cfg932.py:220`, `over` detects that the complete supplied cold mass cannot
fit the law profile inside the catchment. Line 221 clips `r_star` to `r_ta`.
The smooth endpoint `Ms` in lines 222-223 then contains only `M_ph(r_ta)`
inside the integration region. Its otherwise declared transition to `M_cat`
outside the edge is not represented by a mass-carrying shell or receiver in
`dMs`.

If the positive jump in `Ms` just outside the clipped edge is interpreted as
a thin receiver shell, its delta-function mass, self/cross potential energy,
kinetic energy, conserved charge and angular momentum must be included. The
present smooth `dMs` and energy integrals omit that shell; merely naming it
does not close the endpoint budget.

All 16 flagged system-grid rows are Draco-like or Fornax-like with L=100
(both footings and four cusp choices). The inside-edge settled/supplied cold
mass ratios are:

| Footing | Draco-like | Fornax-like |
|---|---:|---:|
| canonical | 0.8012600838074087 | 0.38595618163410544 |
| alternate | 0.8808518813993235 | 0.42429927491077296 |

For 11 of those rows an inner `R_x` root really is present. Independent profile
evaluation finds `M_p(R_x)-M_s(R_x)` at most `2.60e-8 Msun` in absolute value;
the code does not substitute an unequal catchment boundary as an inner root.
Those inner equal-mass costs retain their defined local meaning, while the
unplaced outer cold mass and the whole-catchment endpoint remain unclosed.

For the other five rows **no positive-to-negative crossing is found despite a
positive cumulative surplus**:

| Footing / cusp / L | System | Unplaced mass at `r_ta`, Msun | Saved core b cost |
|---|---|---:|---:|
| can / EPS0.05 / 100 | Fornax-like | 1.3175727886259717e11 | 0 |
| can / EPS0.01 / 100 | Draco-like | 5.3305297145978975e8 | 0 |
| can / EPS0.01 / 100 | Fornax-like | 1.3175727886259717e11 | 0 |
| alt / EPS0.01 / 100 | Draco-like | 3.1957474814665174e8 | 0 |
| alt / EPS0.01 / 100 | Fornax-like | 1.2352988289800154e11 | 0 |

The branch at lines 245-246 assigns zero to every core energy whenever
`R_x is None`. This conflates *no surplus* with *no available equal-mass
endpoint*. It does not satisfy the frozen criterion's zero-cost condition,
which says that the cumulative difference is never positive. In the
canonical EPS0.01 Draco row, for example, `M_cat=2.6821636119803343e9 Msun`,
the smallest difference on the declared 20,001-point grid is positive
`6.384904189917437e-6 Msun`, and the endpoint surplus is
`5.3305297145978975e8 Msun`, yet `dE_b=epsilon_req=0`.
This feeds the starved-set minimum directly: its primary window has
`epsilon_lo=0.025865047916602855`, `epsilon_hi=0`. Six primary S_A corners
and nine S_B corners include this false-zero condition (three BH choices
repeat each relevant system-grid case). The current counts are therefore
not physically validated by arithmetically matching the implementation.

There is also a zero-point issue for the clipped whole-catchment b costs.
For `f(r)=Phi_law(r)+v_c,law(r)^2/2`, integration by parts gives

```
Delta E_b = [(M_s-M_p) f]_0^R + integral_0^R (M_p-M_s) f' dr,
f' = (G/2) [M_law/r^2 + M_law'/r].
```

The script's integral alone is a zero-point-independent energy difference
only when the boundary mass difference vanishes. It does not vanish at
`r_ta` in these 16 rows. An extra outer shell, envelope beyond `r_ta`, or
escaped mass could repair the ledger, but each choice changes the endpoint,
potential, boundary work and receiver requirements. No corrected physical
class is asserted here and frozen criteria have not been changed.

## 5. What this arrival does and does not advance

The useful substantive result is explicit identification of who must pay for
phenomenological outward settling: the unmodified two-sided drift injects
matter energy, while baryonic feedback payment is a new post-hoc constitutive
rule, H-ELS. Saved energy-window arithmetic does not determine that coupling,
an angular-momentum flux, receiver response, transfer rate, formation history,
or survival. A successful integrated budget must also avoid spending the same
available feedback energy independently on census gas expulsion and cold
redistribution; the recorded M3 energy diagnostic alone is not that ledger.

The representative set contains UFDs, Draco-like, Fornax-like, a gas-rich
rotator, MW-like and cluster-core systems. **Sextans and Leo I are absent**;
the inputs are declared representatives, not the actual four-dwarf catalog.
Adding Fornax to S_B gives only another conditional diagnostic comparison.
No result here establishes sufficient Draco/Sextans central mass or protects
the measured Fornax/Leo I budgets. The next discriminating action is to define
the missing receiver without deleting mass, classify the no-crossing surplus
rows as unresolved until that endpoint exists, then evaluate conservative
energy and angular-momentum exchange for the actual four dwarfs with one
shared transport law.
