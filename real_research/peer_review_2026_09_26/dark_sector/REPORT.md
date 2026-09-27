# Dark-sector peer review — 2026-09-26

**Normalized claim:** the L380/L386 pooled cosmological window, L381/L387 merger
checks, and DE1/DE2 gate checks describe one particle-free action, with the same
constitutive law, gate, carrier dynamics and parameter/shape cell.

**Primary verdict: incomplete, with the smallest missing implication identified.**
The active Harvey gate is demonstrably different from the gate used to evolve
the retained carrier. Its merger result cannot certify or exclude the pooled
cell. Even after this parameter error is corrected, the force operator and
carrier-profile bridges remain unproved. These are specific research obligations,
not a no-go theorem for the user's framework.

This review starts at `f3b848273e635b81bc328882db0ffb4206d86e45`. It reads existing
research and writes only this directory. It does not rerun or overwrite L380,
L381, L386, L387, DE1 or DE2. The validated run manifest pins its actual inputs;
the additional source inventory records SHA-256 hashes. No root `.mathbox`
ledger was present. External observational claims are conditional inputs, not
independently revalidated observations in this review.

## New finding: the Harvey solver has a different gate

The complete source path is:

1. `dark_sector_2026/L377_full_construction_pm.py:94` fixes
   `P_GATE=2, X_C0=2`; L380 imports that evolution through L379 at
   `L380_pooled_window_fixed_cell_clearing.py:38,46,79,85`.
2. `merger_infall_2026/L370_boosted_infall_mergers.py:159–161` instead fixes
   `SW_DEF="p1_x1.5"`, whose active threshold is `1.5*Ez2(z)`.
3. `merger_infall_2026/L371_harvey_slow_kick_carrier.py:79–80` imports that default.
   It is the only store to `SW_DEF` in L371. The value is actively passed into
   the lensing-mass root at line 157, the main-halo map at line 201, and the
   displaced-gas lensing map at line 214. L370 line 290 reads the supplied value
   through `x_ceff(z,sw)` to construct the actual region mask.
4. `dark_sector_2026/L381_harvey_on_pooled_window.py:64–78` replaces retention,
   kick, mutation flag and variants, but never the gate. L387 imports this
   unchanged adapter at `L387_harvey_window_slow_end.py:58–59,78`.

The new AST/source check establishes that this is an active parameter mismatch,
not an unused documentary default. At the merger epoch `z=0.4`, using exactly
L370's background, the inherited threshold is **2.3205940453**, whereas the
pooled `p=2,xc0=2` threshold is **4.7868059759**. Matching kick and total retained
mass alone therefore does not match the model.

**Minimal correction before a costly merger run:** make `(p,xc0)` an explicit
argument to `harvey()`; after L371 imports its machinery, assign the selected
`SW_DEF` (the existing `p2_x2.0` entry supports the pooled cell). Record the
resolved gate, kernel, epoch and force-operator identity in the output. All
three active uses above must receive it. Replace the old intact-carrier
reproduction control with a gate-matched intact control; the old reference is
itself at `p1_x1.5` and need not reproduce after a real gate change. Recompute
S2 at 600 first, since its current margin is only 0.0086442. Merely obtaining
another L387 output without changing this adapter repeats the mismatch.

This is a **new finding**, unlike the exact-kernel, prescribed-gate variation,
and independent-field-data gaps already established by
`closure_resume_2026_09_26/recipe_audit.md` and `gate_review.md`.

## Additional bridge that a gate-only correction does not solve

The PM and merger force operators differ. L377 lines 117–127 compute the
baryonic Newtonian field from **all** baryons, then mask its constitutive
response; lines 160–165 let baryons feel its projected field. L370 lines
286–305 first label connected regions, solve the Newtonian field from each
region's own `rb*f`, and restrict the felt phantom field to that region. These
are different nonlocal source/response operations even with identical
`nu_mono` and gate numbers. L377 additionally uses a background-subtracted
matter gate (line 120), whereas L370's halo mask uses absolute real density
(line 290). A local-density approximation may motivate the latter, but no
controlled error bound is provided here.

The carrier dynamics are explicitly phenomenological: L377 lines 175–185 use
a chosen activation threshold, a Poisson decay probability with `Gamma=10H`,
and random fixed-speed kicks. Its own conclusion at lines 344–347 says that
the trigger has no action. L371 lines 101–117 derive orbit retention for an
assumed Newtonian kick model; lines 120–146 impose and renormalize S1/S2/S3
profiles, and lines 167–170 use a lensing-mass halo as the S2 shape proxy.
Those orbit computations are not a derivation of the kick law or of the
cosmological carrier's resolved core dynamics. The retained mass comes from
`z=0` but the merger map is at `z=0.4` (L371 lines 13–25,85,97).

Numerical particles here sample a continuum phase-space evolution. Their use
does not establish a fundamental particle dark-matter ontology. Conversely,
calling the sampled component a classical carrier does not derive its stress,
charge, initial data, or transport from the allowed clock action.

## What the stored results actually support

| Obligation | Finding | Scope |
|---|---|---|
| Pooled L380 arithmetic | Passed independent reconstruction | Halo mass-bin medians and cluster medians agree exactly; no PM rerun |
| Common retained mass input to L381 | Passed in stored data | Same four kick labels and window; retentions are copied as declared |
| Common gate across PM and Harvey | Failed | `p2_x2.0` versus active `p1_x1.5` |
| Common force operator | Not established | Global-source masked PM versus region-source masked merger solver |
| Common physical core shape | Conditional | S1/S2/S3 are imposed profiles normalized to a coarse retained mass |
| Exact requested kernel | Failed as an identification | Existing simulations use `nu_mono`, neither requested law by definition |
| Carrier dynamics from the allowed action | Not addressed | Chosen kick/decay law and assumed orbit distribution |
| Complete vacuum-gate window | Incomplete | DE1 excludes the current canonical p2 flagship; DE2 uses different inputs |

L380's stored pooled window is `{600,625,650,675}` km/s, under its corrected
fixed-cell clearing statistic and its finite three-box setup. L381's stored
Harvey passes are **S1 at 600 and 625 only**; S2 fails at all four kicks, with
fit value `0.10864420305035277` at 600 against the adopted 0.10 cutoff. Thus
the strongest statement is about the two stated cusp profiles under the
inherited merger gate. There is neither an S2 pass nor a gate-consistent S2
exclusion yet. The numerical medians and pass flags were checked independently
from the saved per-halo rows and estimator values in `check.py`.

At inspection L386's log ends at `15 runs, pool 8` and its results JSON is
absent. L387 has a script but no completed output/results. They are pending
evidence, not passes; **L386's runtime status is unknown** from these artifacts
(this audit did not inspect or stop any live process). The source comment
mentioning L380 in L387 lines 11–14 is
stale prose; its executable loader correctly requests L386 at line 64.

DE2 now has a saved JSON, unlike the earlier closure-resume checkpoint, but
its own load-bearing W3 **fails** (`10/12 corners pass exactly`). Its log is
startup-only while the source contains comments about an intervening correction,
so source/output freshness is not established by their presence. More basically,
DE2 lines 57–63 explicitly retain Newtonian single-box transfer data, switch-only
KiDS fits, and the obligation to rerun the carrier calculation for another gate.
Its claimed forest/growth dominance (lines 21–24) is not a proof for nonlinear
carrier evolution with feedback. Do not inherit the old p2 cosmological or
merger window into a new p1 cell on this basis.

## New separate-law calculation under DE1's stated approximation

The user's two laws are kept separate:

\[
\nu_{RAR}(t)=\frac1{1-e^{-\sqrt t}},\qquad
t=x(1-e^{-x}),\quad\nu_{exp}(t)=x/t,
\quad t=g_N/a_0,
\]

For an isolated point mass, `M_dyn(r)=Mb*nu(t)` and `t=GMb/(a0*r^2)` give the
on-branch local gate variable at the flagship radius:

\[
X_F=\frac{GM_b}{r_F^3H^2}[-2t\nu'(t)]-
\frac{3\Omega_m(z)}2,\qquad
r_F=\sqrt{GM_b/(0.1a_0)}.
\]

This is an independent derivative calculation, using DE1's background constants
and hard on-branch convention. It never imports `nu_mono`. A symmetric radial
finite difference independently checks the density derivative in all 12
mass/footing/law cases. At `z=2.5`, `Mb=1e11 Msun`, the p2 threshold is
`2*E(z)^4=399.9004102813`:

| Law | Canonical X_F | Canonical p_max at xc0=2 | Canonical inactive shift | Alternative X_F |
|---|---:|---:|---:|---:|
| Published nu_RAR | 364.4986385 | 1.965008860 | -1.133719864 dex | 482.4698532 |
| Closure mu_exp | 364.3176614 | 1.964821383 | -1.072510226 dex | 482.2305308 |

Both canonical laws fail local activation at the flagship radius for that gate;
both alternative-footing cases pass it. The lower masses `1e10` and `1e10.5`
pass the same local test for both footings and laws. These are conditional
spherical diagnostics, not new action-derived gates, full static switched
solutions, or equality of the nonspherical AQUAL and QUMOND equations. The
inactive shifts use DE1's compensated hard-edge Newtonian-exterior assumption.

The RAR number happens to agree closely with DE1's tabulated `nu_mono` cap,
but the two functions have not been declared identical. In fact DE1 lines
153–157 computes the edge with `nu_mono` for **both** of its advertised kernel
labels and changes only the inactive amplitude. Its old “both kernels” flag
therefore was not two independently computed edges. This check supplies the
separate spherical derivative for the requested published law and closure law.

## Reproduction, provenance and next computation

The dependency graph is:

`spec + recipe amendment -> one action/kernel -> carrier evolution + region
force law -> retained mass and core shape -> merger lensing + cosmological
observables -> one common accepted cell`.

The first action-to-carrier and common-force-law implications are absent; the
active common-gate implication is false. The numerical reconstruction checks
only the final stored bookkeeping and the new spherical diagnostic.

`check.py`, `contract.json`, `run_001/results.json` and
`run_001/manifest.json` are the complete new evidence. The run uses Python
3.9.6 binary64 arithmetic, no randomness, 100 bisection steps per inverse,
30-second wall cap and 20-second CPU cap; actual execution took under one
second. The manifest validator returned
`valid evidence record; mathematical interpretation requires review`.

Regenerate in a fresh output directory with the computation-audit runner and
the declared contract; the exact executed argv and input hashes are in the
manifest. Validate the present record with:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py real_research/peer_review_2026_09_26/dark_sector/run_001/manifest.json --root .
```

**Cheapest next computation:** first test the selected *same* gate and kernel in
a single resolved spherical halo to compare the PM and region-restricted force
operators, with the same initial density and an explicit measured force error.
That is cheaper and more discriminating than another pooled scan. In parallel,
correct the merger adapter as above and run one gate-matched S2 600 case with
its own control only after the intended operator is fixed. For each requested
kernel branch, retain a separate parameter/observable record; changing the
kernel requires recomputing retention and shape predictions, not relabeling
the stored `nu_mono` result.

Historical cost is substantial: L380's 15-run pool took **13,209 s (3.67 h)**;
L381's four-kick pool took **5,467 s (1.52 h)** on the recorded machine. L386's
same-sized 15-run setup is comparable in scope, not guaranteed timing. A
single merger kick is not reliably one quarter of pooled wall time because
the four kicks were parallelized. No full simulation was launched here.
