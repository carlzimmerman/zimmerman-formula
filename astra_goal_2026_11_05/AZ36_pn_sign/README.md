# NO VERDICT — full nonspherical PN-sign claim

Lane5(b), criteria59adccf59f; pre-computation matter amendment27dc122863.
Kappa = 1/2 FITTED; not theory closed. The radial calculation establishes
an exact conditional UV-sign theorem, but does not supply the omitted
nonspherical physical-mode operator required for a full PASS.

For a static spherical positive-divergence branch, with positive lapse and
radial metric and nonnegative K(Q) dust, the constrained radial kinetic and
gradient coefficients are positive without a PN expansion. In vacuum,

    B_tau = s + gamma s² + mu²(1-N)/(K N²),
    T_A = 1/(K² N A³ B_tau),
    c_rad² = gamma B_tau / [(1+gamma s)² + gamma mu²/(K N²)].

In the mu0 limit this becomes gamma*s/(1+gamma*s): the radial correction
reduces the leading PN speed and cannot flip its sign. The exact derivation,
constraint treatment, matter cancellation and scope are in `DERIVATION.md`.
The Galactic external field, arbitrary propagation angles, transverse
metric/polarization mixing and finite-wavelength modes are still missing.

## Checks and retained failures

All20 symbolic identities and known answers pass. The main script passes
26/28 checks and exits1: both original float64/80-digit comparisons narrowly
miss their frozen1e-12 line. The mutant passes24/28 and exits1, additionally
failing the gradient-sign gate on both footings. Reversing gamma makes the
radial principal speed negative throughout the declared grid, while its
kinetic factor stays positive. This is a changed-action control, not a
claim that the adopted action has that instability.

| Quantity | Canonical | Alt |
|---|---:|---:|
| Coefficient cells per mode | 162 | 162 |
| Main c_rad² range | 1.0000e-12–9.99001e-4 | 1.0000e-12–9.99001e-4 |
| Mutant c_rad² range | -1.00101e-3–-1.0000e-12 | -1.00101e-3–-1.0000e-12 |
| Original maximum float discrepancy | 1.819e-12 | 1.528e-12 |
| Main40/80-digit maximum discrepancy | 9.967e-33 | 1.037e-32 |
| Frozen40/80-digit tolerance | 1e-30 | 1e-30 |

The separate POST-RESULT A2 diagnostic was frozen as189970f3ae. It confirms
the failure is representation/cancellation in1-N near unity. Against the
same exact binary64 inputs, the maximum discrepancy is3.75e-16; evaluating
the decimal-input lapse offset stably gives3.96e-16. Both main and mutant
diagnostic trees pass the unchanged1e-12 line. The original failures remain.
A2's prose quoted the40/80-digit error at the worst float sample, below
1.04e-37; the whole-grid maximum is1.037e-32 as tabulated here. Both satisfy
the frozen1e-30 precision-pair line; this corrects the prose, not the gate.

The initial main/mutant JSON records the amendment file as it stood at A1
(commit27dc122863). A2 was added afterward and is separately hashed by the
diagnostic. Reruns against the later document have different provenance
hashes but identical equations, parameters and criteria.

## Inputs and non-claims

Both a0 footings are separate. The length endpoints and center are inherited
from CQ7, with its existing caveat. The test uses illustrative local y, lapse,
radial metric and matter coefficients; these are not solved Solar profiles.
The inherited mu^-1=100kpc is explicit. The exact theorem is conditional on
the background equations, not established by the finite sample.

The matter completion is a minimally coupled static scalar used to verify
the shift Hessian. Omitting it would spuriously leave rho_m+p_r in the
radial kinetic denominator. Its independent perturbations are not solved,
so a frozen-matter sub-block is not a full interior spectrum. In the vacuum
exterior the radial theorem does not depend on this matter example.

Main and mutant each took under2s and peaked below60MB RSS, single threaded.
No numerical PDE/background solution or astronomical exclusion was graded;
the numerical checks are algebraic precision pairs and controls.

## Reproduce and continue

From the repository root:

```sh
OMP_NUM_THREADS=1 PYTHONHASHSEED=0 python3 -B astra_goal_2026_11_05/AZ36_pn_sign/run.py
OMP_NUM_THREADS=1 PYTHONHASHSEED=0 python3 -B astra_goal_2026_11_05/AZ36_pn_sign/run.py --mutate
OMP_NUM_THREADS=1 python3 -B astra_goal_2026_11_05/AZ36_pn_sign/precision_diagnostic.py
```

Expected exits1,1,0; the original numerical misses must remain visible.
Each mode writes its own atomic result. The next proof obligation is the
full constrained second variation on the nonspherical screened background,
including transverse metric/polarization and matter blocks. Use this exact
radial result as a known answer; do not replace that calculation by a
smallness assertion. The all-lanes program next addresses the moving Sun.
