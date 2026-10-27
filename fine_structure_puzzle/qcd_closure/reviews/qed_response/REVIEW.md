# Independent FSP-005 physical and mathematical review

Normalized claim: under the four explicit curved-space locality, mixed
metric-current clustering, global-state and differentiated-remainder inputs
in `qed_infrared/DERIVATION.md` section 5, the actual order-e^2 current insertion
has zero projected linear-H stress coefficient. The claim does not establish
those hypotheses for QCD and does not interchange the charge derivative with
the curvature limit without an additional uniformity input.

**Primary verdict: conditional on a named input.** The named inputs are exactly
section 5 hypotheses 1-4 and, for a derivative of the fixed-charge coefficient
itself, the additional interchange in lines 244-247. No substantive error was
found in that restricted implication. The full-spectrum Gaussian resummation
is a separate defined-model statement and is proved as written under its
explicit common spectral subtraction. Neither statement supplies an alpha
value or an unconditional QCD no-go.

## Provenance and exact targets

Fresh subagent `qed_response_review` derived the spectral values and Gaussian
Mellin cancellation before reading either target. Its immutable
`RAW_DERIVATION_v1.md` was saved and reported to the coordinator first. The
subsequent `CONVENTION_ADDENDUM.md` translates an ambiguity in the delegation:
the project stress is `(1-D/4)(W/V)=-DW/(4V)`, not `V^-1(1-D/4)W`. This was
confirmed by the coordinator and is not a target discrepancy. All reported
stress comparisons below use the authoritative project convention.

Audited bytes, SHA-256:

- `qed_infrared/DERIVATION.md`: `d48bd5d2cad2fefa4e95a3a447a356da7f683c26a70cd5b94db5b0e8ccc66833`.
- `qed_infrared/REPORT.md`: `803d53398af45cd035c548fa07336eda0d11b01a25f9545249e22990ad967b3b`.
- `qed_resummation/RAW_DERIVATION_v1.md`: `338ccf48bf3b9dd9006c8fb3fbc15892e4ad2526eb0c7cea47ea6250cc7a56c5`.

Repository base HEAD: `9516ee01c79f35c04b7556050669ba77b0c98b99`, with a dirty
workspace. Only this review directory was written. Targets and prior run
artifacts were not changed. No new mathematical computation or fit was run.

## Dependency graph

1. Canonical source coupling and fixed-regulator Gaussian integration give the
   positive current-current insertion in W. Source contacts and parameter
   matching are required. Metric variation then acts on the photon inverse,
   transverse projector, measures, current kernel, contacts and matching.
2. A flat positive gapped current spectral measure gives an analytic flat
   polarization near Q^2=0. This leaf does not control all soft metric limits
   of T...TJJ or finite-volume/global sectors.
3. Uniform mixed cumulant and metric-Taylor/remainder inputs plus a controlled
   sphere state give the covariant local photon/gravity EFT. Those are named
   assumptions, not deductions from the flat spectrum.
4. The smooth S4 Maxwell spectrum, scalar ghost and compact global quotient
   fix the low-mode determinant and anomaly. Local irrelevant insertions add
   even curvature powers; local matching contributes H^0,H^2,H^4,... to f.
5. Differentiated remainders allow P(D)(1-D/4) and the H->0 limit. This proves
   the conditional insertion projection. A further uniform charge limit is
   needed for partial_(e^2) A_rho.
6. The finite-mode global example tests the missing uniformity. The exact
   full-spectrum Gaussian with common subtraction tests why a first-order H
   term does not necessarily survive fixed-charge resummation.

Leaves 1,4 and the defined Gaussian calculation are independently checked
internal derivations, with the source translations below. Leaf 2 is conditional
on ordinary unitary current spectral axioms and renormalizable QCD short-distance
behavior. Leaves 3 and the relevant uniform QCD limit in 5 remain unestablished
physical inputs. No circular QCD inference is used in the target.

## Obligation matrix

| Obligation | Status | Review finding |
|---|---|---|
| Actual order-e^2 current insertion and sign | Passed at fixed regulator | Integrating exp(-i e A.J) gives exp[-e^2(J,DJ)/2], hence positive insertion in W; all quark contractions and matching are included. |
| Metric response includes TJJ and contacts | Passed | The explicit variation of D and K and the further mixed cumulants are retained; flat transversality is not promoted to metric analyticity. |
| Flat gap controls flat Pi_R | Conditional on ordinary spectral/OPE inputs | Dispersion sign and moment expansion agree with the declared transverse tensor convention; a gap gives the stated low-Q domain. Mere abstract temperedness alone would not specify the required number of UV subtractions. |
| Flat gap controls uniform curved/global response | Not addressed as a theorem; correctly not claimed | Section 5 explicitly supplies these as stronger hypotheses. |
| Hodge rather than rough vector operator | Passed | Ric=3H^2 shifts the cited rough spectrum to (l+1)(l+2)H^2; l=1 has eigenvalue 6H^2 and multiplicity 10. |
| Legitimate zeta continuation at 0,-1 | Passed | Independent Hurwitz calculation retains pole-times-zero terms -17/64 and 13/384; results 19/30 and 5/63 agree. |
| Scalar/global U1 normalization and anomaly | Passed in the stated canonical compact theory | Nonconstant scalar zeta is -61/90 and log global-group volume contributes -2 log H to W, giving -31/45 log(H/mu). |
| Dimension-six photon trace | Passed as a convention-fixed EFT contribution | W_6=e^2 H^2[(19/30)c_R+(5/63)c_lambda]/2, hence rho_6=-e^2 H^6[(19/30)c_R+(5/63)c_lambda]/(4 Omega4). |
| Full physical H^6 matching | Conditional and not calculated | c_R requires curved matching; redundant derivative photon operators and their Jacobians shift local gravitational matching. Pure-gravity curvature-cubed coefficients are independent. Target states these limits. |
| Conditional zero-H insertion projection | Passed under section 5 inputs | Local even powers and controlled higher logarithmic terms vanish under the projected limit; D^0,...,D^4 remainders are needed and named. |
| Finite soft-mode inference counterexample | Passed as a kinematic nonlocal source model | Positive covariant transverse projector addition preserves pointwise flat correlators while violating uniform clustering; it is not claimed to realize local reflection-positive QCD. |
| Finite soft-mode fixed-charge conclusion | Passed | Exact logarithms give only H^4 log H in f and H^4 stress; the first derivative at zero charge is nonuniform. |
| Exact full-spectrum relative determinant | Passed under its common subtraction | Absolute convergence, Mellin interchange, residues, cancellation and differentiated remainder all checked independently. |
| Physical alpha/QCD coefficient derived | Out of scope and not established | Neither target makes this claim. |

## Decisive checks

The coexact zeta expansion at n=l+3/2 is

\[
 \sum_{j\geq0}\frac{(s)_j}{j!4^j}
 [\zeta_H(2s+2j-3,5/2)-\tfrac94\zeta_H(2s+2j-1,5/2)].
\]

The corrections which survive vanishing Pochhammer factors are -9/32+1/64
at s=0 and 9/256-1/768 at s=-1. Together with the Bernoulli values they give
19/30 and 5/63. The nonzero minimal scalar gives -61/90. The canonical global
constant-gauge quotient scales as V^(-1/2) in Z, so

\[
 \frac{dW_\gamma}{d\log a}=-\frac{19}{30}-\frac{61}{90}+2
 =\frac{31}{45},\quad
 \rho_\gamma=\frac{31H^4}{180\Omega_4}.
\]

The field-redefinition caveat in target section 6 is essential. A derivative
operator proportional to the Maxwell equation is redundant; removing it
changes the measure and local gravity coefficients. Its isolated spectral
trace is meaningful in a fixed convention but cannot determine the full H^6
vacuum response. This does not generate freedom to insert a nonanalytic H
term as an ordinary local gravitational counterterm.

For the finite soft-mode construction, the smallest three degeneracies are
10,35,81 and eigenvalues are 6,12,20. Their exact d/x sum is 259/30, giving
the stated insertion coefficient 259 gamma Lambda^3/(80 Omega4) in rho.
Its position-space kernel vanishes in a fixed physical patch as H^3 while
its long-distance tail at separation proportional to H^-1 is polynomial,
not uniformly exponentially small. Consequently it refutes only the attempted
implication from pointwise flat gap plus Ward identities. Reflection positivity,
local QCD realization and actual QCD source response are not supplied.

At fixed nonzero e its exact finite-mode W has leading -189 log H, up to an
H-independent constant. Thus its physical stress is 189 H^4/(4 Omega4) plus
higher powers. The nonzero order-e^2 H insertion cannot be identified with the
charge derivative of the fixed-charge H coefficient.

## Full-spectrum Gaussian audit

Let t=(M/H)^3. The target defines, rather than infers by a potentially invalid
order-zero determinant factorization,

\[
 \Phi(t)=\frac12\sum_l d_l[\log(1+t/x_l^{3/2})-t/x_l^{3/2}]
 +\frac t2\zeta_T(3/2).
\]

Its bracket sum is absolutely convergent, locally uniform for t>=0, with
tail O(t^2 l^-3). It has the declared common small-t subtraction. The
first-order density coefficient is nonzero: the analytic estimate in the
convention addendum proves zeta_T(3/2)<-2 without a numerical fit. Small-t
requires M/H small, which cannot persist in a fixed-M curvature limit.

For 4/3<c<2, the log-minus-linear Mellin formula may be summed absolutely.
The integrand is pi t^s zeta_T(3s/2)/(s sin pi s), with the overall 1/2.
Its relevant poles after shifting left are 4/3,1,2/3,0. The s=1 residue is
exactly -t zeta_T(3/2)/2 and cancels the explicit first insertion. The others
give

\[
 \Phi(t)=-\frac{\pi}{4\sqrt3}t^{4/3}-\frac{\pi}{\sqrt3}t^{2/3}
 +\frac{19}{60}\log t+\frac34\zeta_T'(0)+R(t).
\]

The remainder claim is justified, not merely formal. Subtract enough integer
heat terms to bound the Mellin representation in the chosen finite strip.
At z=3s/2, inverse Gamma grows with exponential type 3pi/4 in Im s; the
1/sin(pi s) decay leaves an integrable type -pi/4 envelope. Each fixed
number of t partial_t derivatives adds only polynomial powers of s. Hence
for 0<sigma<1, `(t partial_t)^j R=O(t^-sigma)` for every fixed required j.
This controls the physical stress and the P(D) projection.

It follows at fixed M that

\[
 \delta\rho=-\frac{\pi M^4}{4\sqrt3\Omega_4}
 -\frac{\pi M^2H^2}{2\sqrt3\Omega_4}
 +\frac{19H^4}{80\Omega_4}+O(H^{4+3\sigma}).
\]

There is no M^3 H term. Finite ordinary local polynomial gravitational matching
may shift the first two local terms but cannot undo the absence of H in this
defined model. The singular nonlocal current Hessian is incompatible with the
ordinary gapped flat current representation. This calculation is a counterexample
to an order-of-limits inference, not a model-independent theorem about QCD.

## Sources and computational evidence

Primary-source checks were performed with the literature-check workflow.
Read-only exact-identifier project-cache queries returned no hits. Existing
temporary exact-version PDFs/text for the two sphere/global-mode sources were
read and rehashed; no source text or PDF was added to scientific directories.

- [de Divitiis et al., 1303.4896v1](https://arxiv.org/html/1303.4896v1), section 2,
  equations (2)-(7): the physical two-current convolution, short-distance contacts
  and parameter-retuning framework are verified. The torus prescription is not
  imported as a sphere prescription. Authentication, extraction and this limited
  application were checked; no curved QCD uniformity theorem is attributed.
- [Donnelly, Michel and Wall, 1611.05920v1](https://arxiv.org/html/1611.05920v1),
  PDF equations (2.7)-(2.9),(2.14),(2.19): determinant powers and the canonical
  zero-mode volume are verified. Setting p=1, b1=b2=0 and Gamma0=V gives the
  needed V^(-1/2) factor. The source's connection normalization must be rescaled
  together with its measure; it is not a strong-coupling identification.
- [Kluth and Litim, 1910.00543v2](https://arxiv.org/html/1910.00543v2), Table 4:
  the rough-vector/scalar spectra are verified in the exact version. At d=4,
  R=12H^2, the Hodge shift gives the target Maxwell spectrum and multiplicities.
  The source does not establish QCD metric clustering or the infrared loophole.

The retained temporary source hashes match `qed_infrared/SOURCES.json`:
1611.05920v1 PDF `65ece3e49ef8f7ea373ecd29af67a9ce9ddc1e151b6800b3d22b6654286accd2`,
text `9b1283e07c9417e198a952990b6eba14390df8f1711bd179521a96f7f16293f1`;
1910.00543v2 PDF `2f55677d90a9ba44543260ca8776fb9a1fa9577fee988271673efe4618cf464b`,
text `c7738b5d1db0bd31431654ae74b577573cab517c7bc6146fae0173e77ef19d8e`.
The 1303.4896v1 primary HTML header and equations were read; no retained local
PDF hash is claimed for that source. No novelty search was attempted.

`spectral_check.py`, its precontract, run_002 manifest and result were inspected
read-only. The exact formulas and finite ranges agree with the claimed checks:
eight heat sums on l=1..300 and four t values at 60/80 digits, a Dirac moment,
and the three-mode sum. Their finite decimals do not prove the complete heat
expansion or QCD matching. The tail-integral formula is a valid decreasing
majorant in the declared range, but its quadrature decimal is not interval
certified, as the target discloses. I did not rerun or independently validate
the runner schema; the hand derivation is the mathematical evidence used here.

## Exact remaining gap and strongest safe statement

The open physical arrow is a same-regulator QCD source/metric functional on
the closed-sphere state with low-mode, global-sector and differentiated-radius
control. Flat current moments alone cannot provide it. A bounded next test is
to calculate the low-l transverse current Hessian and soft TJJ response with
all contacts/matching, testing the proposed uniform bounds as H decreases;
the global QCD sum needs separate control. Fixed-charge resummation or an
equally strong uniformity result is then required before interpreting an
e^2 insertion as a derivative of A_rho.

The strongest justified result is the target's conditional order-e^2 zero-H
projection, the independently verified spectral/EFT benchmark, and the exact
absence of H in the explicitly defined positive Gaussian resummation at fixed
M. The QCD value A_rho(alpha)/m_p^3 remains uncalculated.

Proofreading self-review: all new review prose/displays checked for notation,
delimiter balance, sign conventions and file scope. No target mathematical
tokens were changed. Independence applies to the saved pre-read raw; source
verification and target comparison were necessarily performed afterward.
