# TP01 pressure mapping: fresh analytic cross-review

**Normalized claim.** For the stated local material energy W(rho,s)=k rho^(5/3) exp(-2s)+U(s), k>0, eliminate s on a differentiable positive-source stationary branch and calculate the total thermodynamic pressure and its density derivative. Check the implementation's normalized density and canonical radial-mass conversion. The full microscopic spectrum is outside this review.

**Primary verdict: conditional on a named input.** The pressure and density dictionaries are correct for the stipulated waterbag energy, exp(-2s) portal and local stationary-branch elimination. No algebraic pressure-map or density-normalization error was found. Their application to microscopic matter remains conditional on that portal and on the effective potential actually being the matched local energy. The calculated fixed-order branch's pressure-sign change is not a physical halo exclusion.

This is a fresh analytical cross-review by the gravity reviewer, distinct from the microscopic calculation's author. It reconstructs the critical thermodynamic arrows from the supplied raw energy, then inspects the source. It is not a blind reproduction, an independent full-spectrum reconstruction, or an external-literature audit. Reviewed at shared-checkout HEAD `17b9d33134c9120da129704b93e61c400eb62481`; TP01's starting checkpoint was `0fe706856e8a897a9ab350be4931dbf36416ada4`. Exact audited file hashes are below because the shared tree is active.

## Raw derivation and exact sign conditions

Write A=k rho^(5/3) exp(-2s). Assume rho>0, U twice continuously differentiable in the interval in question, and a differentiable local stationary solution s(rho). Stationarity gives

    W_s = -2A+U_s = 0, hence A=U_s/2.

Thus positive K=k rho^(5/3) requires U_s>0. At that stationary point,

    D := W_ss = 4A+U_ss = 2U_s+U_ss.

A strict local radial minimum requires D>0. These assumptions permit the implicit-function calculation below; D=0 is excluded. They establish a local minimum only, not its global dominance over other minima or phase coexistence.

For epsilon(rho)=W(rho,s(rho)), the envelope identity gives

    d epsilon/d ln rho = (5/3) A = 5U_s/6.

Consequently the full pressure, including the scalar potential stress, is

    P = rho d epsilon/d rho - epsilon
      = (2/3)A-U = U_s/3-U.

Dropping the -U term would give the wrong pressure derivative. Differentiating stationarity, or equivalently solving for density, gives

    rho(s) = [U_s exp(2s)/(2k)]^(3/5),
    d ln rho/ds = 3(2U_s+U_ss)/(5U_s) = 3D/(5U_s),
    ds/d ln rho = 5U_s/(3D).

Since dP/ds=(U_ss-3U_s)/3,

    dP/d ln rho = 5U_s(U_ss-3U_s)/[9(2U_s+U_ss)].

The sign statements must retain their hypotheses:

| Quantity/obligation | Exact condition on this branch |
|---|---|
| Positive density/source | U_s>0, with k>0 |
| Strict local radial minimum | D=2U_s+U_ss>0 |
| Strictly increasing density with s | Automatic under the preceding two conditions |
| Positive dP/d rho (positive compressibility sign) | U_ss>3U_s, **on that positive-source stable branch** |
| Zero dP/d rho | U_ss=3U_s; then D=5U_s>0 |
| Positive absolute P | U_s>3U; independent of the compressibility sign |
| Positive epsilon | U_s/2+U>0; not supplied by either stability condition |

An additive constant in U changes epsilon and P but leaves U_s, D, dP/d ln rho and the computed compressibility boundary unchanged. Absolute pressure therefore needs the vacuum/reference-stress convention; the derivative obstruction does not. Positive compressibility alone is not a proof of relativistic causal sound speed or all-mode stability. Those also require the complete energy, conserved density and kinetic/matter action.

## Density normalization

Let s=0 be the stated vacuum stationary point, with U_s(0)=0 and U_ss(0)>0. Define, as requested,

    B_curv=U_ss(0)/9,
    rho_*=[3B_curv/(2k)]^(3/5).

Taking the ratio of this definition and the stationary density expression yields exactly

    rho/rho_* = [U_s exp(2s)/(3B_curv)]^(3/5).

No phase-level value k is selected by this ratio. B_curv is a specified curvature parameter in the logarithmic coordinate, not a canonical mass squared and not a proven coefficient of a large-density logarithmic equation of state. U_ss(0)=0 or a negative vacuum curvature would invalidate this positive reference scale as defined.

The stored boundary values in `run_density/result.json` reproduce rho/rho_*=0.5908117662032266 when inserted directly into the formula; the arithmetic agrees at the displayed float64 precision. This is conditional on the supplied U and its numerical root. It does not determine an observed density in physical units.

## Source-to-formula checks

| Source obligation | Audit result |
|---|---|
| `spectrum_pressure/pressure_scan.py:44–47` differentiates with respect to s | **Passed:** X is replaced by X exp(j step), so these are logarithmic-coordinate U_s and U_ss, not canonical-T second derivatives. The tree contribution used at line 74 is X-independent and contributes no derivative. |
| `pressure_scan.py:75–82` branch and compressibility formula | **Passed on the stated branch:** source is U_s>0, radial test is D>0, and dP/d ln rho uses the derived expression. The standalone `positive_compressibility` row flag tests only U_ss-3U_s; outside the admissible branch that flag alone is not a physical stability statement. The combined counts at lines 108–109 retain the needed branch conditions. |
| `spectrum_pressure/exact_and_gap.py:50–56` direct pressure/density derivative | **Passed:** pressure includes -Vtree-CW. Its local density function contains exp(2t), without exp(2s_base); that omitted base factor and k are constants in t and cancel in d ln rho/dt. It is appropriate for this derivative check, not an absolute-density assignment. |
| `spectrum_pressure/density_reach.py:7–15` vacuum origin and reference scale | **Passed:** s=ln(X/X_min), B_curv=U_ss(X_min)/9, and the implementation uses the derived dimensionless density ratio and monotonicity identity. |
| `density_reach.py:16–20` 33-state checks | **Computationally verified only at those recorded states.** The analytic identity proves monotonicity on any connected branch satisfying U_s>0,D>0 throughout; the finite sampling alone does not prove those conditions over the whole interval. |
| Promotion to a globally stable fluid, halo or full quantum theory | **Not addressed:** a local stationary branch and its compressibility are less than a global phase-selection rule or complete field/matter evolution. |

The five stored direct-versus-formula pressure derivatives agree at their serialized precision, and their stored D values are positive. I checked those output identities and the boundary-density arithmetic without rerunning the spectrum or a full simulation. These checks supplement the hand derivation; they do not independently authenticate the one-loop spectrum, root locations or omitted corrections.

## Canonical field metric

The stated fixed-phase microscopic coordinate is T=T_v exp(s), with L_kin=|partial T|^2=|T|^2(partial s)^2. In real-field 1/2 G_ss(partial s)^2 notation, G_ss=2|T|^2; equivalently phi=sqrt(2)|T| is canonical. At a matter-loaded stationary point W_s=0,

    m_radial^2 = d^2W/dphi^2
               = (W_ss-W_s)/(2|T|^2)
               = D/(2|T|^2).

Thus `exact_and_gap.py:48–49`, with T^2=(30h^2+lambda^2)X^2/lambda^2, makes the correct stated tree-metric conversion. Away from a stationary point the -W_s term cannot be dropped. Calling s canonical would be wrong, but the reviewed code does not do that.

A positive nonconstant effective metric G_ss(s) changes the canonical mass to W_ss/G_ss at a stationary point. It does not change the local stationary equation or the thermodynamic envelope identity if the same W(rho,s) and conserved rho are retained. A matched effective action may, however, change U, the portal, density dependence or metric together; the present formula cannot assume those changes away. The condition U_ss>3U_s refers to the specific portal coordinate s in exp(-2s); it cannot be transferred unchanged to an arbitrarily redefined canonical coordinate. This review therefore supports the documented canonical-field caveat, not an all-order shape-protection claim.

## Strongest safe conclusion and smallest remaining physical implication

For the stipulated local waterbag portal, a positive-source radially stable occupied branch has the full pressure and compressibility stated above. Its reported finite-threshold branch reaches a zero-compressibility point while the local radial Hessian is still positive. That phenomenon is algebraically distinct from a radial tachyon, and an arbitrary vacuum offset cannot erase the derivative sign change. The normalized boundary density quoted by the author is mapped correctly.

The smallest missing physical arrow is **from the microscopic theory to this occupied-state material energy with its conserved density, portal, normalization and matched effective U**. Only after that arrow is established can a negative branch compressibility be interpreted as a physical instability of the claimed material. Global branch choice/coexistence, running metric/effective-action matching, gradients, the light sectors and gravity remain separate obligations. Nothing in this mapping review proves or disproves a full physical halo, and no conclusion about the full SU(5) spectrum is issued here.

## Audited input hashes

Hashes were observed unchanged across this review's two source reads. These pin the reviewed artifacts independently of shared HEAD movement.

| File under `spectrum_pressure/` | SHA-256 |
|---|---|
| `pressure_scan.py` | `ca9770b212e6bccd6f2f3bd53c9ca134fed365ecfec4fb16c81d25f0f73012d2` |
| `exact_and_gap.py` | `fb9cc7efc628b7c9cf173127971ba0b0ed58951d67ab9214f28ab0a83929e2cb` |
| `density_reach.py` | `0a19f0dc6f0c5437916b366d4a52cbb44c986abd98d3f43afdf48b877a9cc390` |
| `DERIVATION.md` | `df12e2a74bd3a4133ebe05a069976eccc9316c29d19c42d805f48cef4186aeef` |
| `REPORT.md` | `76cf68510a72c5c67c7fadb548a13808cc0b850320f35a2bd6b1d40c97e5cd3a` |
| `DENSITY_CONTRACT.md` | `07465c1587cece0fa49d31a5c13ef6d6e875c6f0eb9b10e8584d96546df13470` |

No artifact other than this review was written by this cross-review turn. No old source, run, spin artifact, simulation queue or Git state was modified.
