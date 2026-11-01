# TP02 normal-relaxation matching: method cross-check

**Normalized claim.** The specified finite matching subset computes full tree-mass-matrix directional Coleman–Weinberg tadpoles on the commuting SU(5) valley, eliminates two heavy invariant coordinates at fixed retained X, and propagates that known vacuum-relaxation contribution through a weak-coupling comparator pressure calculation. It does not compute the complete finite effective action.

**Primary verdict: correct only after a stated restriction.** The inspected matrix differentiation, first-spectral-trace derivative, raw heavy-coordinate Hessian and retained-X pullback are consistent with this fixed-scheme, on-tree-valley finite subset. The controls support its finite implementation and pressure witnesses. They do not certify a complete two-loop potential, finite kinetic matching, a quantum transverse Hessian, an invariant physical endpoint, or a three-step root-convergence result.

Review scope/provenance: I authored the adjacent `matter_coupling/` pressure calculations and had already inspected and used the `normal_data_reference` interface and its numerical outputs. This is therefore an exposed-input method cross-check by a different author from `rg_threshold/`, **not a blind independent pressure audit** and not an independent reproduction of all SU(5) spectral assembly. I freshly reconstructed the derivative and chart normalization below. No numerical rerun was needed: no concrete implementation discrepancy was found. Only this review file was written in this turn; existing matter and RG artifacts were unchanged. Shared HEAD observed during review was `a7bade87f24f37a759b840f0ebb78b80a2d82aac`; the pinned source hashes below are the relevant identity in the active checkout.

## Matrix derivative reconstruction

Let Y be the symmetric cubic tensor, F_i=f_i+Y_ijk z_j z_k/2 and M_ij=Y_ijk z_k. For a real directional displacement delta z along either raw a or b,

    delta F=M delta z, delta M=Y delta z,
    delta B_ij=sum_k conjugate(delta F_k)Y_kij,
    delta(M^dagger M)=delta M^dagger M+M^dagger delta M.

`relaxation.py:20–37` implements these variations and the corresponding real scalar Hessian blocks. With A=M^dagger M Hermitian and B symmetric, the real Hessian in delta z=(q+i p)/sqrt(2) is

    [[Re(A+B), -Im(A+B)], [Im(A-B), Re(A-B)]].

This is exactly `real_hessian` at line18 and its directional derivative at line32. The lower-left block is not missing a sign: `A.imag-B.imag` is the correct transpose-compatible block for Hermitian A and symmetric B.

On these commuting diagonal normal slices the background remains D-flat. The tree D Hessian is L^T L, so its variation is delta L^T L+L^T delta L. The gaugino mixing J proportional to z^dagger R and its derivative proportional to delta z^dagger R are retained before forming the full 73-Weyl M_F^dagger M_F. Vector mass derivatives likewise differentiate both factors in 2g^2 Re[(Rz)^dagger(Rz)]. I found no missing product-rule term or conjugation in lines24–36.

For h(x)=x^2[ln(x/Q^2)-3/2],

    delta Tr h(H)=Tr[h'(H)delta H], h'(x)=2x[ln(x/Q^2)-1].

In an orthonormal eigensystem this is sum_i h'(lambda_i)(V^dagger delta H V)_ii. Lines48–53 implement this with scalar/Weyl/vector weights1,-2,3 and the 1/(64pi^2) prefactor. No derivative of an individual eigenvector is needed for this first trace derivative. The expression is basis-independent inside a truly degenerate eigenspace. This is an appropriate way to avoid unstable numerical eigenvector derivatives.

## Gauge zeros and actual finite controls

The right-sided limit h'(0)=0 justifies zero tree masses contributing zero to this first tadpole. It does not establish a finite second derivative of h at zero, or authorize interpreting arbitrary off-shell negative masses as a stable effective potential. The normal-matrix controls differentiate the underlying polynomial matrices, not an off-shell logarithm through a tachyon.

The implementation uses the numerical cutoff `lambda>1e-12*max(1,max(lambda))`, rather than symbolic null projectors. The recorded minimum scalar eigenvalues are about -1e-15 to -9e-17, compatible with numerical null directions in this already checked tree spectrum. This review does not convert that tolerance into a theorem about all fields/couplings. No cutoff sweep is included in `check_relaxation.py`, and no pressure conclusion should be extended into a regime with a physical light eigenvalue comparable to that cutoff without one. The input tree-spectrum positivity/case counts remain dependencies from TP01, rather than newly proved by this cutoff.

`check_relaxation.py` contains eight analytic-versus-central matrix-gradient controls: two directions at each of e=.01,.03,.05,.1, at the fixed-coupling TP01 minimum. They compare original polynomial matrices at displaced a or b to the analytic directional matrices. The maximum recorded scaled error is 9.39e-12, well inside 1e-7. The scaling denominator is max(1,max|delta H|), so this is not a relative-accuracy certificate for every small matrix entry. The derivative control also does not independently authenticate the original mass-matrix construction: both routes share it.

The twelve running-valley sample states (four couplings times three field ratios) pass the separate CP-odd-tadpole, small-shift, positive angular coefficient and negative relaxation checks. The largest recorded CP-odd source is 6.06e-19. The CP-odd checks cover the two declared invariant singlet directions; they are not a quantum transverse-positivity calculation. Negative deltaU with positive raw Hessian follows algebraically from -J^T H^(-1)J/2 and is a consistency check, not an independent measurement of the tadpole's correctness.

## Raw Hessian and the retained chart

On A=i aD,B=bD, TrD^2=30 and X fixed, the tree potential is

    V=(f-15ha^2)^2+(15/2)lambda^2 a^4+30a^2(hX-lambda b)^2.

At a0^2=2fh/(30h^2+lambda^2), b0=hX/lambda its raw Hessian is

    Haa=120fh, Hbb=60lambda^2 a0^2, Hab=0.

Thus delta a=-CW_a/Haa, delta b=-CW_b/Hbb and

    deltaU=-1/2(CW_a^2/Haa+CW_b^2/Hbb)

are correctly normalized in **raw a,b coordinates**, as used by `relaxation.py:54–58`. These Hessians are not themselves canonical mass squares. The kinetic terms for these directions are30(partial a)^2 and30(partial b)^2; a canonical real directional coordinate contains sqrt(60). In addition, b at fixed X is not the orthogonal massive normal at fixed canonical flat field T. Dividing Hbb by60 does not produce the full normal-mode eigenvalue of the mixed X,b sector.

This is not an error in static coordinate elimination. With y=sqrt(30)b and r=sqrt(30)h/lambda, a convenient orthonormal light/heavy pair is

    T=(X+r y)/sqrt(1+r^2), H=(y-r X)/sqrt(1+r^2).

On the tree valley T=sqrt(30h^2+lambda^2)X/lambda. A shift delta b at fixed X also shifts that projected T by30h delta b/sqrt(30h^2+lambda^2). The implemented reduction is therefore naturally a **retained-X chart**, not minimization of an orthogonal heavy field at fixed projected canonical T. A comparison with the latter chart would require the corresponding field redefinition at the same order.

The angular pullback is consistent with the retained-X convention: the R phase rotates X and B, not A, so F=X^2+30b^2 and deltaF=60b0 delta b to first order. A coordinate change must transform both the reduced potential and this pullback. `normal_data_reference` maps the original reference X0 to running canonical X,couplings,Qm, evaluates the fixed-X normal data there, and returns the quantities as functions of X0. `scan_relaxed_pressure` then differentiates the composite reference-field function, rather than confusing partial running-X derivatives with reference-X derivatives.

A ratio X0/Xmin is consequently a useful chart-dependent numerical diagnostic, not an observable invariant field displacement. The potential/metric pair, pressure and current must be kept together when drawing physical conclusions. The known geometric deltaF is not the direct finite two-point matching contribution. Nor does a small heavy shift bound every missing quantum term.

## Relaxed comparator pressure and step control

`scan_relaxed_pressure.py:9–15` adds the computed deltaU once to the high-precision RG potential and uses finite logarithmic-field stencils. Converting the float64 correction to an mp value does not restore its lost precision, but avoids truncating the much larger baseline U to float64. This correctly avoids infinitesimal `mp.diff` of a float spectral-tadpole function.

The formula at lines25–30 is the **old waterbag comparator**, with N=Uss-3Us, D=Uss+2Us and the corresponding curvature-normalized density. It is not the microscopic phase-current equation and does not include the occupied heavy square. This restriction is explicit in the output non-claims. The native occupied state is a different pressure problem; I do not use my adjacent calculation as an independent validation of this comparator.

The recorded nearby comparator endpoints are:

| e | X_pressure/Xmin | rho/rho_* | dP/dlnrho at X/Xmin=1.2 |
|---:|---:|---:|---:|
| .01 | 1.17711196 | .5902093 | -2.7520e-12 |
| .03 | 1.17677909 | .5890772 | -2.4820e-11 |
| .05 | 1.17739218 | .5908446 | -6.6396e-11 |
| .10 | 1.18530251 | .6153036 | -1.7591e-10 |

Every recorded endpoint/witness is positive-source and radially stable. The negative-compressibility witness numerators at1.2 are orders of magnitude larger than the recorded coarse/fine derivative changes, supporting their signs within this subset.

**What the step check actually establishes:** roots are solved with stencil h=.005. At those fixed roots and the1.2 witness, h=.01 repeats the first and second derivatives; maximum absolute differences range from4.10e-18 to4.45e-16. A separate h=.0025 stencil differentiates only the added relaxation contribution for a composite-versus-direct derivative check; its discrepancy is at most7.30e-16. These are useful local derivative controls. The source does **not** independently resolve all endpoints at h=.01,.005,.0025, so no explicit three-step root-location convergence was demonstrated by this script. The printed long root decimals are not certified accuracy. A literal root-stability claim beyond the displayed diagnostic precision should first repeat the root solve at another stencil, rather than infer it solely from absolute derivative differences.

## Exact validity limits and next implication

The strongest supported statement is that a numerically well-resolved, fixed-gauge/subtraction-scheme normal-relaxation subset has been calculated from the full declared matrices and does not remove the old comparator's negative-pressure-derivative witnesses at these four weak trial inputs. It is one finite reduced two-loop contribution, with a corresponding geometric angular correction. The isolated subset is gauge-dependent and cannot replace the remaining matched effective action.

Direct finite two-loop vacuum graphs, finite derivative/kinetic graphs, quantum transverse stability, light/gauge IR sectors, occupied-state selection/current lifetime and gravity remain uncomputed here. None is resolved by CP-odd tadpole zeros or small raw-coordinate shifts. The smallest numerical continuation, if more endpoint precision is needed, is a second-stencil root solve with the same pinned input chart and explicit cutoff sensitivity at any newly light spectrum. The smallest physical continuation is the remaining matched effective action, rather than another re-labeling of the comparator pressure as microscopic matter.

## Audited source identity

| File under `rg_threshold/` | SHA-256 |
|---|---|
| `relaxation.py` | `34c4acde459f7406f6adc6857be86757f7ad5500aff85069475154636757f500` |
| `check_relaxation.py` | `0c15f2cca07d0968370fc340e4401e3a59acc0a603e3f7d64ae645fd36aeb438` |
| `scan_relaxed_pressure.py` | `9fad145061e812a888ba311fb8a97291f9dc4255f75917de68f3728d8ec1e122` |
| `improved.py` | `156d9d8e329a2af13ad72703409a7c0dcd9154748b33d53e26f8ca91239677f3` |

Existing `run_relaxation/result.json`, `run_relaxed_pressure/result.json` and their v2 manifests were inspected. No new numerical run or independent endpoint reproduction was performed by this review.
