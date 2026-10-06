# Independent coupled homogeneous-history audit

**Primary verdict: computationally verified only in the stated finite examples, with the background equation reduction proved analytically.** The action, expanding constraint root, trace/geometry closure and full improved stress are consistent. The six floating-point trajectories support the reported finite continuation through ordinary dust–radiation equality to the positive-F guard. They do not certify a singularity, continuation to a=10^-4, all-frequency health or a positive cold-dust identity.

## Final inspected inputs

Frozen REPORT.md SHA256 `68c606301a531fce4571ee93e5e4e4c7259df640718c8d4d8624d51362e1c8f5`; equations.py `f28552fae9281b3e7bbdfea3f77ad6702c0c425595228cc8fc8059998529cbbf`; checks.py `5d740a6c2bedc44f4dc5adca2608e48a5e7455d174998507dca898c269fe9546`; history.py `b70e58264e6b382bab9b8cbad4310c05ed3c7a2e065eb9eadd5491fedf142973`. Peer-inspection HEAD was `bcf5f7a09d7dfc3a25a7ecd9d8a20a4af23ff921`. Parent action and sharp-matching inputs were read; no parent or author scientific input was changed or executed by this peer.

The class is four-dimensional FRW with the canonical complex nonminimal scalar, positive ordinary conserved dust/radiation densities, xi>3/16, and the expanding F>0 branch. This peer does not transfer the previous prescribed radiation metric or finite EdS perturbation response into the actual mixed history.

## Independent full trace and geometry reduction

Use the action `M R/2-|partial chi|²-xi R|chi|²`, f=|chi|², E=|chi_dot|², D=Re(conjugate(chi)chi_dot). The homogeneous scalar equation is

`chi_ddot=-3H chi_dot-xi R chi`.

It gives `f_dot=2D`, `D_dot=E-3HD-xi R f`, and `E_dot=-6HE-2xi R D`. Consequently

`Box f=-f_ddot-3H f_dot=-2E+2xi R f`.

The full carrier trace is the canonical trace plus the improvement:

`T_chi=2E+2xi[-fR+3Box f]`

`=2(1-6xi)E+2xi(6xi-1)fR`.

Ordinary dust has trace -rho_d and ordinary radiation zero. Thus `-MR=-rho_d+T_chi` gives precisely

`B R=rho_d+2(6xi-1)E`,

`B=M+2xi(6xi-1)f=F+12xi²f`, `F=M-2xi f`.

There is no missing factor of two from the complex normalization. For the stipulated xi>3/16, B>=M>0, and a charged state has E>0. Ordinary radiation domination does not set this R to zero. The earlier prescribed R=0 mismatch is correctly removed rather than carried into this evolution.

## Friedmann branch and cancellation-safe evaluation

The full00 equation is

`3F H²+3F_dot H=rho_d+rho_r+E`, with `F_dot=-4xi D`.

For F>0 and total positive RHS, its discriminant is `Gamma=sqrt(F_dot²+4F total/3)>|F_dot|`. The expanding root is

`H=(-F_dot+Gamma)/(2F)>0`.

Multiplying numerator and denominator by Gamma+F_dot yields the exact alternative

`H=2 total/[3(Gamma+F_dot)]`.

The code uses the alternative when F_dot>=0 and the direct form otherwise. This avoids subtracting nearly equal positive numbers without changing the constraint or clamping the equations. All quantities have consistent natural dimensions: F,B,M are mass-squared, F_dot has mass-cubed, total density has mass-fourth and H mass/ inverse-time.

With `C=3F H²+3F_dot H-rho_d-rho_r-E`, independent differentiation of all scalar and matter invariants using `H_dot=R/6-2H²` gives

`C_dot=H[BR-rho_d-2(6xi-1)E]-4HC`.

The stated trace therefore propagates C=0. Conversely, the algebraically solved root has `C_H=3(2FH+F_dot)=3Gamma>0`. Differentiating C=0 along the actual field/matter evolution and comparing with the identity uniquely recovers the geometric H_dot. This is not a circular imposition of two unrelated Ricci formulas: the scalar/trace root and the geometric evolution are mutually consistent because the derivative coefficient is nonzero. Matter conservation is exactly rho_d proportional to a^-3 and rho_r to a^-4 in the Jordan frame.

The x=ln(a) equations divide proper-time evolution by the solved H. The elapsed-time derivative 1/H has the correct meaning, with only an arbitrary time origin. The reference tau=1 is not a measured age or a prescribed mixed-era clock.

## Full stress and initial radiation-type carrier

Direct metric variation yields

`rho_chi=E+6xi H²f+12xi HD`

`=E-3H F_dot+3(M-F)H²`.

The raw pressure with scalar f_ddot eliminated is

`p_chi=(1-4xi)E+4xi HD+2xi f[(2xi-1/3)R+H²]`.

Using the verified Friedmann and trace closure gives the independent metric dictionary

`rho_chi=3M H²-rho_d-rho_r`,

`p_chi=-M(2H_dot+3H²)-rho_r/3`.

The raw versus metric equality is a genuine normalization/variation check. Differentiating the raw density with the actual scalar equations and geometric R gives `rho_dot_chi+3H(rho_chi+p_chi)=0`; adding the independently conserved ordinary components gives total conservation. Canonical E alone would be the wrong source stress.

For the specified M=tau_reference=1 initial data, E_i=4xi fe/3, D_i=-fe/2 and rho_di=4/3. The trace numerator is exactly (4/3)B_i, so R_i=4/3 even after ordinary radiation is added. On the constraint surface this makes the initial carrier trace zero. More explicitly,

`rho_chi,i=6xi fe(H_i-2/3)(H_i-1/3)`.

C(2/3)=-rho_ri<0 and the expanding root lies above 2/3, so this initial stress is tiny positive and `p_chi,i=rho_chi,i/3`. It is radiation-type, not dust. At the reported guard the signed carrier density is negative and pressure nonzero; calling it positive pressureless cold mass would contradict the actual stress dictionary. This does not classify every other initial condition or mixed solution.

For Q=a³ Im(conjugate(chi)chi_dot), the angular scalar invariant obeys `d Im(conjugate(chi)chi_dot)/dt=-3H Im(conjugate(chi)chi_dot)`. Thus Q is conserved exactly, with the explicitly chosen half-canonical complex normalization. Its conservation does not determine an energy/mass abundance or equation of state.

## Principal field health: correct but restricted

Writing chi=(phi1+i phi2)/sqrt(2) gives F=M-xi(phi1²+phi2²). For F>0, the conformal change gE=(F/M)gJ converts the gravity block to Einstein form and gives

`K_ab=(M/F)delta_ab+3M F_a F_b/(2F²)`.

Here F_a=-2xi phi_a and sum F_a²=8xi²f. The tangential eigenvalue is M/F and the radial eigenvalue `M(F+12xi²f)/F²=MB/F²`, confirming their positive signs in this region. Their principal cones and the graviton cone are luminal, and the positive conformal transformation preserves null cones. This independently derived principal-field statement is appropriate for this action. It does not establish low-frequency mixed-fluid stability, CMB transfer, EFT validity, quantum behavior or the other clock/cutoff model's health. At F=0 the tensor/frame description degenerates; a homogeneous background equation can remain regular there without restoring full physical health.

## Numerical implementation and geometry monitor

The state stores real and imaginary chi and proper-time velocities separately. Therefore its analytic continuation for a complex-step directional derivative uses sums of squares, not complex conjugation of the perturbation; that is the correct derivative of a real-component function. The branch chosen by real(F_dot) stays on a locally equivalent analytic root formula, including the zero-F_dot limit, since the discriminant is positive. Nonholomorphic absolute values in diagnostic scales do not enter the differentiated H.

The geometric monitor differentiates H(x,state) along the actual RHS, then evaluates `6(H dH/dx+2H²)`. H itself contains no inserted R; R enters only the evolved scalar direction. The zero-R mutation changes that direction, so its six failed geometry checks are meaningful. The algebraically solved Friedmann residual alone would be a weak monitor because it is zero by construction even on a wrongly evolved field history. The independent trace/geometry identity, charge, solver comparison and recovery supply the additional checks.

The final exact run passes22 identities; the history run passes40 bounded checks for xi=100,1000, three solver/tolerance choices and81 samples per achieved path. The field, Friedmann, raw pressure and numerical direction were inspected directly. No extra peer integration was performed. Actual last samples have a approximately0.0095599065 and0.00187092534, before the requested0.0001 target, with ordinary rho_r/rho_d approximately1.046 and5.345. They therefore reach ordinary equality in these finite toy normalizations; they do not establish a pure-GR radiation era or a real recombination history.

All three implementations stop at the declared positive-F floor rather than solver failure. Charge errors in the final history outputs are below3.0e-8; geometric scaled errors below5.2e-13. The endpoint log-a comparison bound1.72e-8 and state discrepancy bound7.67e-7 are **relative to the tighter DOP853 reference**, as implemented by the code. The largest all-pair log-a difference (looser DOP853 versus Radau at xi1000) is approximately2.41e-8. The final report now explicitly states that these are comparisons to the tighter DOP853 reference. This clarification changes no execution input or acceptance criterion; it prevents reading a reference norm as an all-pair bound.

These are floating-point consistency tests, not interval error certificates or exhaustive positivity tests between all samples. The retained Radau adaptation warnings are internal numerical warnings, and the successful finite-state/constraint/method checks do not turn them into a physical divergence or erase them.

## Forward recovery and preserved earlier criterion

The archived old history.py divides each component by `1e-6+abs(initial_component)`. For the initially zero imaginary field it imposes a scale unrelated to the nonzero field amplitude. Its preserved37/38 preflight failure at2.15056e-4 remains a failure of that old criterion. The authoritative history.py instead uses common scales |chi_i| for both field components, |chi_dot_i| for both velocity components and reference time1 for elapsed time. The same2e-4 threshold applies to a different declared norm. This is physically transparent but is not retroactive proof that the original zero-component criterion passed. The report explicitly preserves that distinction.

The final six common-vector recovery errors are approximately1.9e-8 to3.4e-7. They corroborate reversibility of the achieved bounded integration and are accompanied by independent method/tolerance comparisons. Roundtrip recovery by itself would not bound the true global trajectory error. The earlier exact preflight script was not archived and its historical hash is correctly marked unavailable; the corrected22-identity authoritative script, not the reconstructed development history, supports the analytic checks.

## Positive-F guard versus a real singularity

The guard F/M=1e-8 is deliberately positive and is neither an evaluated zero nor a singularity theorem. From the actual Radau endpoint states, F_dot is approximately1373.65913 and25017.71620 for xi100 and1000, both positive; H is finite. Algebraically, at fixed finite state with positive F_dot the expanding root has the finite F-to-zero limit

`H=total/(3F_dot)`.

Also B tends to6xi M at F=0, not zero. Thus the homogeneous algebraic system need not produce an infinite Ricci scalar merely because F vanishes. This observation is not a continuation calculation for these stopped solutions, nor a statement that the physical tensor theory remains healthy across the boundary. The report appropriately leaves that implication open.

## Validation and remaining implication

All five standard manifests independently validate current declared input and result hashes. The exact trace mutation fails4 identities, canonical-density substitution fails1, and prescribed-R=0 evolution fails6 geometry checks. REPORT is excluded from execution inputs, so evidence-summary precision changes do not stale the actual runs. No author script or frozen parent evidence was edited by this peer.

Passed analytically: full trace normalization, stable expanding root, constraint/geometry equivalence, improved stress and conservation, initial trace/pressure character, U(1) normalization and restricted principal-field positivity. Verified only as bounded numerical evidence: the six histories, endpoints, equality crossing, guard attainment and recovery. Open: completion to an earlier declared interval, physical continuation at F=0, perturbations on this mixed background, initial charge/amplitude selection, positive cold-dust behavior and any cosmological/MOND/vacuum identification. No blocking inconsistency remains in the stated finite-history result.
