# Claude update: finalized CFG932 and relevant CFG933 result

Read-only follow-up at base `e63b8b234e855d802dbbad73bd575415a84c648e`.
Audited, not executed: no original lane was rerun. Source and result byte
receipts, including comparison with the earlier provisional audit, are in
`sources_claude.json`. No frozen criteria, publications or original artifacts
were edited.

**The missing receiver is now explicitly acknowledged and supplied in a
separate post-hoc endpoint calculation. The frozen main script and results
are unchanged.** The useful new clue is that completing the receiver raises
Draco's required feedback fraction to roughly 35–51%, while Fornax requires
more than its entire declared feedback budget. It does not establish that a
receiver forms, remains stable, or receives the required angular momentum.

## 1. Exact revision change

CFG932's final README, scripts and outputs are committed in
`ef7833fe593598cb21f04930ae93a665bc668e71`, an ancestor of the assigned base.
The frozen criteria remain at
`dce2a2e3da65565cd30b4b2c0d20b8cf4b3e8c42`.

| Artifact | Current SHA256 | Change from provisional packet |
|---|---|---|
| `cfg932.py` | `b408efe5b735a6332b4325d6afdb7fcc166bbb718401ce5b317eb9bf9563cc50` | unchanged |
| `cfg932_results.json` | `b8b638ef03faff9b3e3c70fdfcb382915e3024cf800ea219d129b0b861d79c6e` | unchanged |
| `cfg932.out` | `fae773c5720be97c61b815aa0b7fd4cfd59e1e1f047735fcf1f7831d399b7442` | unchanged |
| `README.md` | `69b884bd5b7fdb95a04fd4f3104dad859affa0fdad513462996274bd97a8c138` | new finalized explanation |
| `cfg932_posthoc.py` | `e9eabe40565611670937f31d313c5f92b9dc1b535be995a38431d96f96024b80` | same bytes previously inventoried, now audited |
| `cfg932_posthoc.json` | `0390261f6b42a73080fc874568ded1566ced82cd45cf98b87a51b778cba79a21` | same bytes previously inventoried, now audited |

Thus this is a newly finalized interpretation and source commit, not new
unseen primary experimental numbers. The previous packet's warning still
applies to the primary false-zero branch. README amendment A1 explicitly
states that its 16 over-supplied system rows were unanticipated, that the
frozen machinery ignores their overfill, and that the primary class is
preserved. PH1–PH3 are labeled post hoc, with no frozen-verdict weight.

## 2. What PH1 actually repairs

For the 16 L=100 Draco/Fornax system-grid rows, PH1 defines

```
R = r_ta,
M_over = M_cat - M_ph(R) > 0,
rho_set = rho_law inside R + M_over delta(r-R)/(4 pi R^2).
```

This accounts explicitly for the mass absent from the primary smooth
endpoint. The three energy measures remain distinct:

* **a, self-consistent virial endpoint:** `cfg932_posthoc.py:61` adds
  `W_shell = -G M_over [M_b(R)+M_ph(R)+M_over/2]/R` before taking
  `Delta E_a = (Delta W_smooth + W_shell)/2`. The shell self/cross term has
  the correct thin spherical shell form. The half-Delta-W step assumes
  virialized equilibria with suitable boundary terms; it does not evolve
  the shell or prove that it is such an equilibrium.
* **b, fixed smooth law potential:** the existing integral can now be read
  consistently as the energy cost of transferring the excess to R in that
  fixed potential. After adding the shell, the endpoint cumulative masses
  agree, so the integration-by-parts boundary term cancels. Shell gravity
  backreaction is not included in this fixed-potential diagnostic; it must
  not be described as the same energy as measure a.
* **c, gross fixed-potential transport:** mass quantiles beyond the smooth
  law's enclosed mass are clamped to R. This represents the shell's mass in
  the monotone transport map. The saved c-net and b costs agree to at most
  `2.5637920231247335e-8` relative over these 16 rows.

In particular PH1 replaces the five positive-surplus/no-crossing primary
zero costs with positive completed-endpoint costs. It repairs their mass
and fixed-potential zero-point problem as an explicitly chosen endpoint.
The primary script's `R_x=None -> zero cost` branch was not changed.

| Footing | System | Shell mass, Msun | Shell radius, kpc | `epsilon_req,b` range over cusps |
|---|---|---:|---:|---:|
| canonical | Draco-like | 5.3305297146e8 | 117.2961820 | 0.35648498–0.50316237 |
| alternate | Draco-like | 3.1957474815e8 | 117.2961820 | 0.34784467–0.50907250 |
| canonical | Fornax-like | 1.3175727886e11 | 505.4139272 | 4.17743326–5.85827665 |
| alternate | Fornax-like | 1.2352988290e11 | 505.4139272 | 4.40219178–6.24964803 |

These are L=100 representative catchment endpoints, not measured extended
halos or the actual four-dwarf catalog. The large shell radii and masses
must remain in any proposed receiver budget rather than being replaced
silently by an arbitrarily compact or massless envelope.

## 3. Post-hoc windows independently reconciled

All 18 combinations of PH1/PH2/PH3, measures a/b/c, and starved sets S_A/S_B
were recomputed by cheap arithmetic from saved energies. Counts and maximum
upper edges agree with the saved JSON. Footings were checked separately.

| Mode, primary b / S_A | Canonical nonempty | Alternate nonempty | Canonical largest upper edge | Alternate largest upper edge |
|---|---:|---:|---:|---:|
| Frozen PH0 | 12/36 | 24/36 | 1.4710233e-6 | 6.6221638e-7 |
| PH1 shell completion | 12/36 | 27/36 | 0.015979158 | 0.019244674 |
| PH2 flagged costs set to infinity | 12/36 | 27/36 | 0.015979158 | 0.019244674 |
| PH3 flagged corners dropped | 6/24 | 18/24 | 1.1277099e-14 | 1.9879579e-11 |

PH1 and PH2 have the same windows because the remaining faint-dwarf
constraints already cap epsilon below the completed Draco/Fornax costs.
Adding Fornax to S_B also leaves those PH1 counts unchanged. This is not a
prediction that Fornax is cleared: in these windows its surplus is
unaffordable and retained under the hypothesized energy throttle.

All surviving windows permit epsilon extremely close to zero. Some canonical
ones have a positive lower edge `7.38855315948e-11`, so literal epsilon=0 is
not in every interval. The physical point is the absence of a substantial
rotator payment requirement, not a derived selective transport efficiency.
The final README correctly separates this from a mechanism. A hypothesis
that uses L=100 for Draco and low L for Fornax would additionally need an
independent formation/baryon-loss selector: the frozen scan uses one common
L for the gas-poor representatives.

PH4 also supplies a useful nontrivial inward-drift control absent from the
frozen null example. At a0=1 its one-sided run has 31 initial deficit cells,
negative work, and relative work-identity error `0.00016786147909734814`;
the two-sided error is `0.0016665506349575062`. These are separate post-hoc
drift-only tests, not a full OU/field/receiver simulation.

## 4. Remaining accounting and transport obligations

The shell completion contains no conserved field charge, vector angular
momentum, orbital population, stress, transport rate, formation history or
survival calculation. Measure a's virial factor implicitly assumes kinetic
support, but no distribution or torque creates that support in the lane.
It is consequently an endpoint receiver, not a dynamically demonstrated
sink for a compact fragment's energy and angular momentum.

For the finite-fragment work, the useful next test is to compute boundary
energy, Noether-charge and angular-momentum fluxes from the **same** matter
action as the fragments, retain the outgoing carrier in the global ledger,
and compare receiver mass/energy/J simultaneously. A stable small-amplitude
mode does not by itself establish a transfer rate or a dwarf-scale outlet.
The phenomenological drift's alpha and feedback throttle cannot be imported
as transport coefficients of the new action without a derivation. Neither
Sextans nor Leo I appears in CFG932.

One finalized wording should not be carried forward uncritically: the
README's opening statement that the gated rule never pushes a surplus out
conflicts with its unchanged `DERIVATION.md` section 3. A gate on **local**
deficit cells does not determine the direction of a drift sourced by the
**cumulative** mass difference; the surplus skin can move outward, and the
derivation explicitly discusses this erosion. PH4 does not test the gated
system. A local gate therefore does not establish retention or no overboost.

## 5. Relevant CFG933 selector warning; no CFG934 arrival

CFG933's criteria are `dd6dc4f35...`, its control amendment A1
`ea8ac96eb...`, results `87b15752ee5360705a702a0d6199cf499c7f08ee`, and final
README `ad94c10f82b65eeb1180e377401b579e270798e3`. The main JSON and README
agree: **NOT DIAGNOSTIC, FRAGILE on both footings** for the sealed P2
representative UDG prediction. The saved Coma arithmetic independently gives

| Footing | Mean observed E | Mean predicted E | Combined SE | z |
|---|---:|---:|---:|---:|
| canonical | 0.7603580 | 0.0717140 | 0.2628425 | 2.6199874 |
| alternate | 0.6694635 | 0.0527006 | 0.2624872 | 2.3496873 |

These E values are natural logarithms, not dex. Pooled cancellation between
Coma excesses and the below-isolated-law NGC1052 systems is explicitly not
claimed as agreement. The declared lower-stellar-mass and higher-aperture-
dispersion sensitivities both change P2 to EXCLUDED. The planted-on-law
control fails the power requirement; the planted +0.4 dex control behaves.
This constrains reuse of P2 as a settled physical selector: it is not
confirmed, and finite-fragment stability would not resolve its population
selection issue. No CFG933 experiment was repeated and no full external-data
audit is claimed here.

No CFG934 directory/files were present in the campaign inventory at this
audit. CFG933 offers a selector limitation, not a new microscopic receiver
or fragmentation mechanism.
