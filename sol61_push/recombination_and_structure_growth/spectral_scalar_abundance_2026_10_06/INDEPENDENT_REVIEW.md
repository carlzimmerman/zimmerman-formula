# Independent spectral normal-stress audit

Primary verdict: **proved as written as a conditional formal order-two theorem in the specified de Sitter scalar sector**. The arbitrary-spectrum extension of the actual preferred-normal interaction stress is correct. Its pressure cannot vanish on an open time interval for nonzero nonhomogeneous scalar data. This is not a theorem about all cold matter or a proof of complete second-order perturbative admission.

Pins: REPORT.md `560e23577e00c8e13286942c8c39df06d816c1d19f339cfb82bf086c89266e7e`; checks.py `5774fb97a33c92f9673e442f8dbe121dbd406570f9c347674a4ed260598a37f5`; contract.json `e98894cc5f4d472732c8a806bb7e0a238a97b9457a9b0aba0ad0b9e5acd5bcef`; provenance.json `d30b80f645d2496ed9097c2c111547a8b1a59352acc03ce8e398339b3222f37b`. These files were read only. The action stress was reconstructed independently from lapse and conformal-spatial variations in the preceding momentum stress audit, then extended here using the actual scalar mode solution and Fourier orthogonality, not author assertion counts.

## Normalized claim and hypotheses

The same projected acceleration plus individual shear action has n=3, K,H,a0>0, 0<eta<1, b=3(1−eta)/eta, and empty coincident de Sitter a=exp(Ht), H²=A a0²/6. Each Einstein coefficient is M=2K. The clock is timelike and shared. First-order common fields and homogeneous relative modes are absent. Relative four-volume Dlog1=Dlog2 is zero in the stated exponential chart, with no extra second-order homogeneous relative particular data. The needed second-order field coefficients and Euler jets are assumed admitted; their existence and regularity do not follow from the moment hypotheses below.

The spatial domain is a fixed flat periodic torus. Every summed lattice wave vector is nonzero; the sum includes both conjugate members. Spectra are finite or satisfy sum k²|D_k|²<infinity and sum k^6|C_k|²<infinity. Reality is D_-k=D_k*, C_-k=C_k*. The conclusion concerns the formal quadratic, properly spatial-volume-weighted normal interaction density and pressure trace. No perfect-fluid conservation or equation of state is presumed.

## Stress reconstruction with arbitrary orientation

For one metric, rho=−EL_logN/(N sqrt(gamma)). Varying the projected interaction before equating the volumes gives its direct quadratic term −K|grad nu|²/(2a²) and its leading density divergence 2K Delta nu/a². The first proper spatial weight is 1−nu/2. Integration by parts of its covariance produces +K<|grad nu|²>/a². Their sum is +K<|grad nu|²>/(2a²). The opposite metric reverses both linear signs and has the same average. The average denominator makes no further quadratic correction to the vacuum-subtracted density: its background vanishes and its linear average is zero.

For an independent conformal variation of one spatial metric, delta v/v=3 delta Z/2 and delta of the averaged inverse spatial metric is −gamma_g^-1 delta Z. This gives p_grad=K<|grad nu|²>/(6a²). The variation of −eta K N sqrt(gamma) sigma² gives rho_shear=p_shear=−eta K sigma². This split negative contribution is not a statement about the sign of the constrained scalar Hamiltonian.

The interaction vacuum term has v/Vg=v/Vhat=1 through this order under Dlog1=Dlog2=0. No vacuum-ratio correction is thereby omitted. A linear second-order relative Laplacian has zero average. The norm-cube lapse force is a periodic divergence of order two; multiplying it by a first-order averaging weight would first contribute at order three. Its spatial-volume stress starts at order three. These statements require the admitted Euler/boundary regularity specified in the report, not merely square-integrability of the Fourier modes.

For each wave vector the first scalar shear is

sigma_{ij,k}=−3H u_k/(2eta) (khat_i khat_j−delta_ij/3),

where u_k=C_k k²/(bH²a²). Its tensor projector has squared trace 2/3 for every orientation. Fourier averaging pairs only k and −k, whose projectors are identical. There is no surviving cross between unequal wave vectors, even when their directions are not orthogonal. Thus

<sigma_1²>=3H²/(2eta²) sum |u_k|².

Arbitrary relative phases between decay and momentum at the SAME vector survive as Re(D_k C_k*), precisely as the report states. Neither this geometric factor nor the Parseval pairing uses a single-axis surrogate as proof.

Together with nu_k=D_k/a+C_k k²/(bH²a²), the raw variations therefore give

rho_bar=K/(2a²) sum k²|nu_k|²−3KH²/(2eta) sum |u_k|²,
p_bar=K/(6a²) sum k²|nu_k|²−3KH²/(2eta) sum |u_k|².

A real cosine of amplitude nu has Fourier coefficients nu/2 at its two signed vectors, reproducing the preceding single-cosine normalization exactly.

## Convergence and interval theorem

On the fixed torus k_min>0, sum k^4|C|² is bounded by k_min^-2 sum k^6|C|². Cauchy–Schwarz gives

sum k^4 |D C*| <= (sum k²|D|²)^(1/2)(sum k^6|C|²)^(1/2).

Hence all displayed moments converge absolutely; on every compact time interval their time-dependent factors are bounded and the averages and finite three-power decomposition are justified. This argument establishes quadratic stress averages, not pointwise higher derivatives or nonlinear PDE regularity.

Expanding gives only a^-4, a^-5 and a^-6. In particular the pressure's highest coefficient is

P6=K/(6b²H^4) sum k^6|C_k|² >=0.

If pressure vanishes on an open time interval, multiplying by a^6 leaves a polynomial of degree two in a that vanishes on an open interval. All its coefficients vanish. P6=0 forces every C_k=0, since each summand is nonnegative with strictly positive k^6 weight. Then P4=K sum k²|D_k|²/6 forces every D_k=0. Cancellation at selected times cannot satisfy the identity. Similarly no nonzero three-power density can equal a constant nonzero a^-3 density on an open interval; multiplication by a^6 produces a polynomial with a distinct cubic term.

The pressure theorem does not use a fluid equation of state inferred from redshifting. Pressure was separately varied. A scalar mean expansion can have the signed a^-3 mixed term, but the action-derived density does not: the intrinsic curvature term cancels that term in the actual Hamiltonian, leaving the a^-5 physical cross. This is consistent with, rather than an omission of, the earlier mixed-branch geometric clue.

## Obligations and remaining implication

Passed: actual normal and spatial-trace stress signs; own-metric averaging covariance; arbitrary-orientation projector contraction; phase/Parseval normalization; absolute moment bounds; exact independent time powers and strict positive highest pressure moment. Conditional: the stated timelike action domain, Dlog1/Dlog2 constraint and absence of extra homogeneous relative data, and admission of the formal second-order fields/Euler jets. Not addressed: complete nonlinear or smooth second-order solution, ordinary matter era, additional common/tensor/vector sectors, nonperturbative condensates, optical averaging and coefficient selection.

The strongest safe conclusion is the absence of a nonzero mean pressureless comoving scalar population in this fixed-background, fixed-sector, formal preparation. It does not identify cold matter, exclude dark matter in general, or constrain A or eta to a number. The smallest physical missing implication is a regular full sourced family and its matter-era transfer, not another identification of canonical energy or mean expansion as abundance.

## Executable audit

The symbolic checks reconstruct the linear lapse/volume rows, the shear and conformal variation coefficients, and the exact polynomial coefficients. They treat the moment positivity and convergence argument analytically rather than claiming finite samples prove all spectra. Standard-record validation is reported below after the frozen runs finish; it is provenance verification distinct from the proof above.

Independently validated all four current standard manifests with validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula. Every validation returned exit 0 and `valid evidence record; mathematical interpretation requires review`. Current main_a has 17/17 assertions; control_weight_a and control_expansion_a each 16/17, and control_dust_a 17/18 with the intended false pressureless assertion. The control behavior matches the named operator/interpretation mutation. No author scientific inputs were modified.

Manifest SHA256 pins: main_a `7c75e6da833d516a58509f85777700e741fd8d8e6b07258cdd7e5752d15565cb`; control_weight_a `6a0a0c0c844a56edd58b018410d9207c6ace0fdd3e3e9d48eefcb347f15c0cef`; control_expansion_a `f3723602dfd844f98ae0786bf4944a440810dcc5e0c5578df76cf375d75e8605`; control_dust_a `349c4bb12dc27e042e8c5db1d6a4bbd4cccd3ed430f9a201f1fc55c94506d2c3`. The report and executable hashes above remain unchanged.
