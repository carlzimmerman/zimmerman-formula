# Independent audit of the finite-host control

Normalized claim: the threshold-matched dilute repulsive daughter scalar, in the declared cold Newtonian, spherical Thomas–Fermi (TF) state inside a live uniform incompressible baryon ball, has an explicit finite static profile and a positive relative dipole curvature. Its full gravitational source includes baryon recoil. In the centered rigid dipole projection its finite-gap one-mode density oscillator weight starts at `k^6`; the resulting overlap spring is insufficient to identify the canonical material action, source, domain, or permanent released-off state.

**Primary verdict: correct only after a stated restriction.** Equations (19)–(20), when written as derivatives of the laboratory source (16), require the centered COM origin `R=0`, or removal of the common phase `exp(-ik·R)`. Without that convention their displayed vertex omits this phase. This is a minor coordinate issue: it cancels in (21), does not affect the multipole order, and does not alter the finite-state result or its scoped canonical mismatch. All substantive bounded analytic implications audited below pass within the already declared TF/incompressible, nested spherical, linear dipole control. No critical error was found.

Exact proof reviewed: `reviews/collective_state_door_2026_10_20/finite_host/RESULT.md`, 27,877 bytes, SHA-256
`4099de88f5de0f6cee6fcaac584b0ac86e64de4a81aa5c9805f697fde5534386`.

The review was reconstructed independently from the raw carrier and canonical equations. The author's verdict and prior review conclusions were not used as mathematical premises. Prior packet files named in the supplied manifest were byte-hashed only; their mathematical contents were not consulted.

## Claim card and dependency graph

The objects are positive masses `m,M_s,M_c,M_b`, positive `lambda_rep,G,rho_b0,kappa_c`, finite host radius `R_b`, and a nonnegative scalar mass density of fixed mass `M_c`. The scalar is on the daughter-only, threshold-matched dilute coherent branch: negligible real source stock and small virtual source fraction, energies below source detuning, lengths exceeding the eliminated-source range, Hartree validity, weak fields and cold velocities. The baryon host is a live ideal incompressible, nonrotating sphere with a free surface. The TF solution is radial with its first density zero at `R<R_b`. Quantum pressure is omitted for the exact TF calculation; use as a finite-hbar GP bulk candidate separately requires a small healing/boundary layer and negligible scalar mass outside the harmonic host. Linear mode claims concern the admitted irrotational `l=1` sector. Full stability, preparation and astrophysical realization are not hypotheses proved by this note.

The implication graph is:

1. Raw positive-square carrier action → threshold amplitude and matched daughter contact → GP density energy and leading common mass source.
2. GP stationary equation → TF radial Helmholtz equation plus positivity/free-boundary inequality → finite density and mass relation.
3. Scalar density plus live incompressible host → nonnegative hydrostatic host pressure and a free boundary.
4. Translation-invariant internal scalar terms plus cross gravity → overlap Hessian; spherical symmetry and Poisson → positive isotropic dipole curvature.
5. Two live masses plus the admitted host pressure adjustment → COM/reduced-mass kinetic energy and actual dipole frequency.
6. Full mass Fourier operator plus COM cancellation → internal vertex and `k^6` optical weight; separate COM and tidal channels remain.
7. Physical conserved-density displacement map plus unchanged cross-gravity energy → source accounting and canonical projection mismatch.
8. Displacement-space Poisson equation plus exact ball intersection volume → the negative hard-edge cubic diagnostic.

Items 1–8 are internal algebra, elementary integration, or explicitly stated state/material assumptions; no external theorem or numerical computation is a load-bearing leaf. There is no circular inference from the canonical target to the constructed profile or its Hessian.

## Obligation matrix

| Obligation | Status | Scope/evidence |
|---|---|---|
| Original source elimination and matching | passed | Distinguishes the regulated positive-frequency Hamiltonian from the fully threshold-matched contact; does not transfer its old positive-square bound. |
| Density/phase normalization and gravity energy | passed | `rho_c=m|psi|^2`, `kappa_c=g2/m^2`, self gravity has factor `1/2`, cross gravity occurs once. |
| TF radial state, first zero, mass and small-mass limit | passed | Equations (5)–(8) reconstruct; monotone mass map has derivative `(1-x cot x)^2`. |
| Static host pressure and scalar vacuum inequality | passed | Equations (9) and the exterior monotone potential supply the two free-boundary conditions. |
| Exact finite-hbar state or full stability | out of scope | Not supplied or claimed; sharp TF density is not an exact finite-hbar GP profile. |
| Frozen-profile Hessian and spherical overlap sign | passed | Equations (10)–(12), with spherical symmetry essential. |
| Live host `l=1` force and boundary response | passed | Pressure perturbation vanishes at the freely translating host surface at the asserted acceleration. |
| Relative frequency and uniform source | passed | Exact reduced-mass identity and cancellation of the internal total mass dipole. |
| Laboratory vertex in (19)–(20) | conditional | Set the centered COM origin, or restore `exp(-ik·R)` in the vertex. |
| Optical residue and generic tidal order | passed | At fixed finite gap: rigid concentric optical weight `k^6`; general internal tidal matrix elements can be `k^2`, hence weight `k^4`. |
| Nonlinear advection/source identity | passed | Translation is a conserved-density path, and its quadratic spring is existing cross gravity. |
| Canonical projected coefficients and nonlinear branch | passed | Equations (25)–(27) and the missing positive cubic/domain/stiffness are correctly scoped to the candidate operator and control. |
| Hard-edge diagnostic | passed | Equation (28) follows from the exact intersection volume; these balls are not asserted to be the GP state. |
| Actual halo, arbitrary host relaxation, or retention time | not addressed | No such certification follows from this finite control. |

## Independent reconstruction

### Original scalar to GP and TF

Expanding the raw carrier square gives source mass `M_s^2=4m^2+Delta_c`, cubic conversion `g_c(X*Phi^2+X Phi*^2)`, and `lambda_tot=lambda_rep+g_c^2/Delta_c`. The same-charge tree threshold amplitude is

`-4[lambda_tot + g_c^2/(4m^2-M_s^2)] = -4 lambda_rep`.

The NR substitution `Phi=e^{-imt}psi/sqrt(2m)` makes the daughter quartic energy `lambda_rep |psi|^4/(4m^2)=g2 n^2/2`. Hence `g2=lambda_rep/(2m^2)>0`. The retained positive-frequency source alone instead gives

`k_c-c3^2/delta=lambda_rep/(4m^2)+g_c^2/[8m^2 M_s(M_s+2m)]`.

The propagator decomposition at threshold contributes the negative analytic correction `-g_c^2/[8m^2 M_s(M_s+2m)]`; the distinction in (1)–(2) is necessary and is handled correctly. This is a dilute low-energy matching statement, not an exact all-density source elimination or a transfer of the regulated positivity inequality to gravity.

Writing `psi=sqrt(rho_c/m) exp(i theta)`, with `v_c=hbar grad(theta)/m`, gives the gradient, kinetic and contact terms in (3). Varying at fixed mass gives exactly the quantum-potential coefficient in (4). Varying Newtonian self energy `1/2 integral rho_c Phi_c` yields `Phi_c`; cross energy gives `Phi_b` once. The common probe source at this order is total ordinary mass density, including the live baryons.

In the TF interior, `kappa_c rho_c+Phi_c+Phi_b=bar_mu`. Its Laplacian is

`Delta rho_c + q^2 rho_c = -q^2 rho_b0`, `q^2=K/kappa_c`.

Regularity excludes the singular spherical solution, leaving `rho_c=A sin(qr)/(qr)-rho_b0`. On `0<qr<pi`, `sin(qr)/(qr)` decreases strictly; selecting its first zero gives exactly (5) and `A=rho_b0 x/sin x`. This proves positivity in the interior and a zero density trace at the boundary. Direct integration gives

`M_c=(4 pi rho_b0/q^3)[x-x^2 cot x-x^3/3]`.

The bracket is positive and has derivative `(1-x cot x)^2>0`; it tends to zero at `x=0` and infinity at `x=pi`. The condition `R<R_b` must still be imposed: for `qR_b<pi` it supplies a finite upper allowed mass. Series of `cot x` gives the `x^5/45` coefficient in (7). Setting the host density to zero before the zero-density boundary gives the isolated TF radius, mass and surface chemical potential in (8); taking that limit after dividing by the host density would be invalid, and the note avoids it.

Since the total spherical potential increases outside `R`, the TF inequality `bar_mu-Phi_c-Phi_b<0` holds there. Thus the differentiated equation is backed by the undifferentiated chemical equilibrium and the vacuum condition. Equation (9) is finite at the origin, nonnegative throughout the host, and zero at its free surface. It solves static incompressible Euler force balance. This checks a conditional static state, not a global variational or all-mode stability theorem.

The actual TF density is continuous but has an edge derivative discontinuity; direct use as an exact finite-hbar wavefunction would make the quantum-pressure treatment invalid near its zero. The note explicitly retains only TF/bulk control and requests the smoothed GP state separately. No uniform error bound or exact GP existence/stability theorem has been reconstructed here.

### Overlap Hessian and live dipole sector

A scalar translation leaves its contact, quantum and self-gravitational energies invariant. Changing variables in the cross energy gives

`H_ij=integral rho_c(y) partial_i partial_j Phi_b(y) d^3y`.

For concentric spheres, isotropy forces `H_ij=h delta_ij`; Poisson gives `3h=K integral rho_c rho_b`. In the nested uniform host this is `h=K rho_b0 M_c/3>0`. Because `Phi_b` is exactly quadratic throughout the translated occupied support, the cross energy is exactly quadratic until that support reaches the host boundary. For spherical GP tails, the trace identity weights only the scalar mass within `R_b`; the claimed small-tail qualification is correct. Neither trace positivity nor this nested control proves positivity for an arbitrary nonspherical configuration.

The two-body change of variables gives `T=M_T dot(R)^2/2+mu_r dot(d)^2/2`, with `mu_r=M_cM_b/M_T`. Therefore

`Omega_opt^2=h/mu_r=G(M_c+M_b)/R_b^3=(K rho_b0/3)(1+M_c/M_b)`.

This is also a valid linear solution in the admitted live-host dipole sector. In host-centered coordinates, the shifted scalar gives `delta Phi_c=-d·grad Phi_c`. Uniform host acceleration solves incompressible Euler if

`delta p_b=-rho_b0(delta Phi_c+a_b·y)`.

At the free surface, all scalar mass is interior and `delta Phi_c=-GM_c d·y/R_b^3`. Vanishing pressure perturbation fixes `a_b=GM_c d/R_b^3`, while the scalar acceleration is `-GM_b d/R_b^3`. Their difference reproduces the frequency and their mass-weighted sum vanishes. Regular irrotational incompressible `l=1` velocity is a translation; other host motions are not certified by this check. The proof does not import a radial breathing curvature as Cartesian support.

### Actual source and multipole order

Mass conservation gives `M_c alpha=M_b beta=mu_r`. Expanding the actual translated densities yields (16), and differentiating it at `d=0` gives, in laboratory coordinates,

`partial rho_k/partial d_i = exp(-ik·R)[-i mu_r k_i(F_c-F_b)]`.

This is the sole literal formula issue found: (19), at proof lines 333–337, suppresses the COM phase while calling the result the derivative of `rho_k`. Its stated right side is the internal vertex at `R=0`, or `exp(+ik·R) partial rho_k/partial d_i`. Equation (20) uses that same internal convention. The phase is immaterial to `Q_i (H-mu_r z)^(-1)_ij Q_j*`.

The ball form factor and both radial integrals in (17)–(18) reconstruct, including the removable `k=0` and `k=q` limits and the isolated `pi^2 sin(y)/[y(pi^2-y^2)]` check. At small `k`, finite centered spherical densities give

`F_c-F_b=-k^2(<r^2>_c-<r^2>_b)/6+O(k^4)`.

Thus the internal vertex is cubic in `k`; harmonic inversion gives precisely (21) and a `k^6` numerator. For the executed nested state this leading coefficient is nonzero: its scalar density decreases radially, so `<r^2>_c<3R^2/5<3R_b^2/5=<r^2>_b`. Consequently the asserted leading order is genuinely `k^6`, not merely an upper bound arising from a possibly vanishing second-moment difference in this state.

A uniform gravitational acceleration couples only to `M_T R`. Taking a heavy-host limit does not discard `M_b x_b`; that term cancels the scalar internal mass dipole before the limit. Omitting host recoil would therefore change the measured operator. For a compact object in COM coordinates, expansion of total mass density has no internal term linear in `k`. Its generic quadrupole term can have `O(k^2)` matrix elements and `O(k^4)` weight. In this centered spherical rigid projection, parity and the first derivative of the quadratic relative-coordinate term instead select the higher one-mode order. The two-quantum/thermal channels and the separate free COM response quoted in the note are consistent with this distinction.

This analysis takes fixed finite internal gaps and finite moments. It supplies no theorem uniform in a continuum, thermodynamic, zero-gap or large-object limit. A finite object's response is in general a two-momentum kernel; (21) is the stated projection in which the Fourier source and measured density use the same selected mode.

### Nonlinear advection and canonical comparison

With `div P_c=delta rho_c` and `dot P_c=-j_c`, the physical linear map is `P_c=-rho_c u_c`. A decaying finite polarization describes zero-total-mass perturbations and cannot identify the positive stock itself with `integral div P_c`. Both scalar and host displacements are needed for the total COM source.

The exact translated-density representative in (23) satisfies

`div[-d integral_0^1 rho_c(x-sd) ds]=rho_c(x-d)-rho_c(x)`.

Its second-order term is `+d(d·grad rho_c)/2`. Integration by parts in the ordinary cross energy then reproduces `d_i H_ij d_j/2`, including the positive sign. Thus the source path itself produces this spring; introducing the same spring again while retaining the same full cross-gravity energy double counts it. Translation-invariant contact and scalar self-gravity do not supply another hidden translation curvature.

For the explicitly conditional linear host-frame candidate `P_c=-rho_c d`, the target quadratic energy projects to `(K A2+gamma B2)|d|^2/2`. The TF Helmholtz equation and its zero density trace give

`B2=-integral rho_c Delta rho_c=q^2(A2+rho_b0 M_c)`.

Direct squared-profile integration yields the displayed `A2` in (26). The candidate matching condition is therefore exactly (27), not an identity in the physical parameters and state data. For the parabolic limit, `M_c=8 pi rho_c0 R^3/15` and `A2=32 pi rho_c0^2 R^3/105`, so `M_c/A2=7/(4rho_c0)` and the inferred overlap coefficient is the state-dependent `7K rho_b0/(12rho_c0)`.

From the frozen S2 equation, expansion of the actual target remainder begins with `K^2|P|^3/(3a0)>0` and requires `K|P|<a0`; its stiffness also has the separately specified canonical coefficient. The contained-support translation energy is exactly quadratic, so it does not generate that positive cubic or saturation/domain. The note correctly treats this as failure of the executed candidate and control. It does not establish impossibility for arbitrary singular, polarized, thermal, fragmented or nonlinear states, nor does it identify the cosmological background or a nonzero `P_0` Hessian. The full canonical background/operator matching is still missing.

### Hard-edge cubic

For two coincident-radius uniform balls, `Delta_d E_cb=K rho_c rho_b V(d)`, where

`V(d)=4 pi R^3/3-pi R^2 |d|+pi |d|^3/12` for `|d|<2R`.

Writing the radial energy as `a d^2+b d^3+c d^5` for `d=|d|`, radial Poisson gives `6a`, `12b d` and `30c d^3`. Integrating with zero derivative at the origin gives exactly (28): coefficients `1/2`, `-3/16`, `1/160` after factoring `GM_cM_b/R`. The nonanalytic cubic is negative and support-dependent. This is a valid diagnostic against a universal analyticity assertion, and its discontinuous scalar balls are not the TF/GP state already constructed.

## Exact remaining gap and strongest safe statement

The strongest supported physical statement is an explicit conditional finite TF equilibrium and a live positive dipole mode with its full mass source. Within that control it fails to derive the canonical material functional/source/domain and irreversible release rule. The Hessian depends only on the instantaneous translated densities; a change of condensate fraction at the same density does not by itself delete this gravitational curvature. This statement does not claim identical kinetic or thermal susceptibility for all states sharing that density. No preparation protocol, restoration ensemble, transport/decay channel, retained off branch or memory lifetime has been supplied.

The cheapest local check is to state the centered COM convention explicitly when quoting (19)–(20), or retain their common laboratory phase. Beyond that convention, the smallest substantive missing implication is a physical operator/background identification that produces the full canonical functional and source from a realizable restored state. A real host equation of state and coupled response about that state are needed before passing beyond the ideal dipole sector. They cannot be replaced by the present positive Hessian or by a fitted lifetime.

## Source checks, commands and provenance

Substantively read raw inputs were `TARGET.md`, the frozen canonical statement, the carrier action and NR equations in `MASTER_COLD_ENERGY_EQUATIONS.md`, the matching/gravity portion of `micro_response/DERIVATION.md`, and the original-particle/source conventions of `occupied_landscape/LANDSCAPE.md`. All listed source bytes, the supplied manifest, and the reviewed proof were independently SHA-256 hashed; every declared source/proof pin matched. Exact paths, sizes, hashes and substantive-read flags are in `provenance.json`.

Commands were read-only `cat`, `sed`, `nl`, `rg` and Python-standard-library byte hashing, followed by writes only to this audit's two allowed output files. No scientific numerical run, scan, fit, symbolic package, process/job inspection, Git operation, campaign edit or author-file fix was performed. The relevant proof-audit checklist sections were general logic/typing, source normalization and computation-range scope. External-source obligations have no unchecked theorem leaf in this elementary reconstruction.

Review provenance: a fresh isolated audit subagent reconstructed the raw implications without receiving an author's proposed verdict or suspected mathematical error as a premise. This is independent reconstruction, not a new proof of the full research target and not an assurance from reviewer agreement. The report applies only to the exact proof hash stated above.

Proofread: this new audit report only, in self-review mode. Routine edits: none. Mathematical-token changes: none. Unresolved report issues: none beyond the explicitly recorded COM-phase convention. Validation: provenance JSON, report hash, reviewed-proof hash, all listed source hashes, and the two-file output boundary were checked successfully.
