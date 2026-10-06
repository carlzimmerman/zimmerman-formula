# Independent raw-action audit: shear-clock repair

**Primary verdict: proved as written for the declared constrained quadratic vacuum claim.** On coincident on-shell de Sitter, n>=3, H>0, k>0 and 0<eta<1, the specified negative shear-square deformation gives a positive reduced relative-scalar kinetic coefficient and a nonzero elliptic common-clock constraint. It does not supply a propagating common-clock mode or prove nonlinear/source/matter health. Those exclusions are explicit in the frozen report and are essential to this verdict.

Reviewed bytes: REPORT.md SHA256 `7c734e8f716a6b2f7ed27905f9b1cdab9b9a1cadcf9140baf75e062c8a9ada0d`; checks.py SHA256 `2878ca65464a499773a940925c41f1e36f1cea19da415670eb300f832ba0d3a6`. Review reads actual covariant operator and geometric quadratic fields, without importing author functions or treating the author's verdict/test count as proof. No author scientific inputs were changed. The reviewer had prior project context; this is an independent algebra reconstruction, not a claim of absence of shared-model errors.

## Claim and dependencies

Raw added action is -eta K times the sum of each metric's volume times its own trace-free extrinsic-curvature norm, with a single common timelike foliation clock. The source interaction remains the projected acceleration-difference action with geometric-mean volume, M=-A+I/2+O(I^1.5), chi=(n-1)/[2(n-2)]. The background relation is H²=chi a0²A/[n(n-1)]. Each metric's lapse, longitudinal shift and scalar spatial shear are retained; relative shear is not removable by the one common spatial coordinate symmetry.

Dependency chain: normalized foliation and ADM geometry -> raw Einstein/shear quadratic trace identities -> background cosmological-volume subtraction and projected lapse-gradient term -> both shift rows -> relative shear and both lapse rows -> positive relative kinetic / spatial-only mean constraint -> tensor/vector blocks. The project-derived parent operator and on-shell background are declared inputs. No external stability theorem is used to complete this chain.

## Independent geometric reconstruction

In unitary clock coordinates, the new term is -eta K N sqrt(gamma)[KijK^ij-Theta²/n]. Thus Einstein kinetic becomes (1-eta)KijK^ij-(1-eta/n)Theta². For a Fourier scalar perturbation, mixed extrinsic curvature is f times identity plus t times the rank-one projector along k, f=zetadot-Hnu, t=edot+Pbeta. Tracing these matrices directly gives Einstein quadratic -n(n-1)f²-2(n-1)ft and trace-free norm (n-1)t²/n. This verifies the action sign and normalization without assuming a healthy lapse block.

Conformal intrinsic curvature is a^-2 exp(-2zeta)[-2(n-1)Delta zeta-(n-1)(n-2)(grad zeta)²]. Integrating spatial derivatives with the perturbed volume/lapse yields +(n-1)(n-2)Pzeta²+2(n-1)Pnu zeta. The on-shell Einstein-plus-individual-Lambda background removes time tadpoles. The actual interaction instead has geometric-mean volume. Its difference from the two reference individual vacuum terms is 2KLambda(Vg+Vh-2sqrt(Vg Vh)); expanding to second order gives K a^n Lambda D²/2, D=relative_nu+n relative_zeta+relative_e. The retained shear trace in D is compulsory. The positive projected invariant supplies K a^n chi P relative_nu² and no common-clock term at this order.

Average/difference splitting gives exactly the two raw scalar actions printed in report section3. No independent coordinate choice for the two metrics was used.

## Actual relative elimination and sign

Let c=Ka^n. Relative shift variation is -(n-1)f-eta(n-1)t/n=0, so t=-nf/eta. This is invertible at P>0,eta>0 and removes edot through the shift. The remaining relative shear row is Lambda D=0, hence D=0 at H>0. Substitution gives

    Lrel/c=-An(zdot-Hnu)²+chi P[nu+(n-2)z]²,
    An=-n(n-1)(1-eta)/(2eta)<0.

The lapse stationary row has coefficient An H²-chi P<0, giving the unique lapse specified by the author. Direct completing-the-square elimination gives

    Lrel,red=c Kr[zdot+(n-2)Hz]²,
    Kr=An chi P/(An H²-chi P)>0.

Neither a bare lapse Hessian nor the original indefinite conformal Einstein kinetic establishes this sign. Indeed the unreduced (z,e) velocity determinant is proportional to (eta-1), negative in the admitted interval; that is not a physical ghost verdict before constraints. The full elimination above is nonsingular for every stated finite P,H and eta interval.

For q=a^(n-2)z the action is K a^(4-n)Kr qdot²; canonical momentum 2K a^(4-n)Kr qdot yields instantaneous Hamiltonian Pi²/[4K a^(4-n)Kr]>=0. This is not a standard finite-sound-speed wave: no restoring gradient survives in this point variable, and its time-dependent normalization is important. Reversing the covariant shear sign gives An=n(n-1)(1+1/s)/2>0 and Kr->-An at large P, a genuine negative reduced temporal coefficient. The author correctly avoids inferring the opposite-sign problem from an unreduced metric component alone.

## Mean-clock row, vectors and TT

Mean shift similarly sets tbar=-nF/eta, leaving the coefficient Amean=2An. The independent mean lapse equation gives V=Zdot/H+(n-1)PZ/(Amean H²). Substitution yields a cross term 2(n-1)PZZdot/H plus the intrinsic term (n-1)(n-2)PZ². They are exactly the derivative of (n-1)a^n PZ²/H since (a^nP)dot=(n-2)Ha^nP. Removing the actual evolving boundary leaves

    Lmean,red=-2c [(n-1)eta/(n(1-eta))] P²/H² (Z-Hpi)².

Restoring the common clock before interpreting the result gives gauge-invariant Q=Z-Hpi, not an extra surviving Zdot or pidot coefficient. Variation is +4c[(n-1)eta/(n(1-eta))]P² Q/H. Thus for a fixed nonzero Fourier mode the clock/mean scalar condition is Q=0. In position space this is a fourth-spatial-order elliptic equation with appropriate spatial kernel/boundary qualifications. It does not establish a healthy propagating clock, full nonlinear constraint preservation or instantaneous-response causal admissibility. The fixed-metric bare term misses the factor1/(1-eta); the author's emphasis on solving the full metric rows is correct.

For TT, the first shear is hdot/2 and its trace vanishes. The deformation changes only time kinetic, giving K a^n[(1-eta)hdot²-P h²]/4 and cT²=1/(1-eta). In the stated interval it is positive and faster than the minimally coupled matter light cone. This is a real action prediction, not a phenomenological viability claim or a clock-gauge artifact. The transverse-vector norm gives K a^n(1-eta)P(Fdot-S)²/2; its actual shift row sets S=Fdot, with no independent vacuum vector kinetic surviving. This check applies only to the present coincident isotropic quadratic background.

## Exact preserved branches and scope

Static zero-shift theta=t gives each Kij=0. Isotropic homogeneous configurations give Kij=Hproper gammaij even with different homogeneous lapses/scales. Consequently each sigma is exactly zero. Both the operator value and every first variation vanish, including clock and shift variations, because delta(V sigma²)=deltaV sigma²+2V sigma delta sigma. The original static equations and any already admitted isotropic background therefore remain unchanged; their perturbation health does not follow. Moving/flowing clocks and arbitrary stationary shifts are not covered.

For the n3 old decaying seed, f=t=0 in both sectors, so the new deformation does not alter its linear equations. This only verifies the linear seed. At second order the covariant geometric shear and added Euler operator must be expanded with all metric constraints and cubic envelope effects; the current report explicitly does not supply this solution. A clock-row inverse alone cannot establish it.

Exceptional limits are necessary: eta0 restores a vanishing mean clock coefficient and makes its sourced inverse nonuniform; eta1 degenerates tensors and the relative velocity system; H0 and P0 cannot use the displayed divisions, volume/shear chain or mode count. The homogeneous foliation mode is not removed by the nonzero-mode elliptic result. The static NR source kernel, offset A and eta stay free because all added first variations vanish on their background branches. No32pi or abundance follows.

## Primary-source and execution audit

Independently reopened [Flanagan arXiv:2302.14846v3](https://arxiv.org/pdf/2302.14846v3), Eq37 and surrounding Eq38-39. The primary operator is a negative shear-square plus trace-expansion-square addition; beta=eta and lambda=-eta/3 indeed yields pure shear in n3. Its slow-motion discussion warns of noncommuting parameter/velocity limits. Its single-metric stationary stability result is not used as a theorem about this two-metric de-Sitter/matter action. The author's attribution and limited use are accurate.

All four current manifests independently validated with the installed mathbox validator using --root and current input/output hashes: main_a41/41; control_sign_a40/41 only `declared_all_finite_p_positive_physical_scalar` fails; control_shear_a40/41 only `declared_relative_shear_retained` fails; control_bare_a40/41 only `declared_constrainted_clock_not_bare` fails. Counts corroborate stated finite assertions; the analytic trace and elimination argument above supplies the sign for the full declared n,P interval.

Obligations: raw operator/conventions passed; static/FRW first variations passed; scalar volume/background term passed; complete quadratic relative and mean elimination passed; constrained sign/TT speed passed; external Eq37 attribution passed; current provenance/controls passed. Nonlinear Dirac admission, second-order sourced compatibility, matter/radiation perturbations, moving-source response and EFT/tensor empirical viability are explicitly not addressed. The smallest missing physical implication is a simultaneous second-order clock-plus-metric sourced solution in this changed action, not another inference from the elliptic row.
