# Retarded curvature memory: exact de Sitter obstruction and a real saturation escape

The covariant Deser–Woodard curvature distortion has a genuine time/history response, unlike a spatial heat kernel acting on a constant. **It does not select32pi or provide a MOND source law.** New results here are a general-dimensional exact-initial-deSitter obstruction for every nonconstant distortion on its visited branch, a full-FRW numerical saturation escape, and a separate local-source calculation showing why its asymptotic vacuum suppression is not suppression relative to the locally measured Newton constant.

Requested and actual entry HEAD310f0d1a46ca858e9a63cf37f699f10baa07ad3d. Writes are confined here. Sources/input hashes and fresh standard runs are recorded separately. This is an audit of a stated causal nonlocal field-equation prescription, not an assertion that the retarded functional itself has an ordinary single-history variational principle.

## 1. Source action, causal prescription and conventions

Signature(-+++), c1, spacetime dimension d=n+1, flat FRW spatial slices. Use

    S_g = (1/16piG_b) integral sqrt(-g) R[1+f(X)],
    X=Box_ret^-1 R,
    Y=Box_ret^-1[R f'(X)],
    F=1+f(X)+Y,
    kappa=8piG_b.

Matter is minimally coupled to g and conserved. No independent bare geometric cosmological term is added; constant vacuum is a matter source rho_v,p_v=−rho_v. G_b=G_EH,b denotes the Einstein–Hilbert action coefficient, not an already measured local Newton constant. Away from4D, the force-calibrated bare Newton coefficient also has a dimension-dependent conversion described in section6. The inverse is the covariant scalar wave operator with X=dot X=Y=dot Y=0 on the specified initial surface.

The original [Deser–Woodard0706.2151v2](https://arxiv.org/pdf/0706.2151v2) and [Deffayet–Woodard0904.0961v2](https://arxiv.org/pdf/0904.0961v2), eq10-17, were authenticated as exact-version primary PDFs. The latter gives the retarded nested integral and the two4D metric equations, and explains the causal prescription and reconstruction freedom. Sources are cached with hashes. Its f is phenomenological; reconstruction of an expansion history is not a microscopic coefficient prediction.

A convenient local differential representation is

    L_loc = sqrt(-g)[F R + partial X dot partial Y],
    Box X=R, Box Y=R f'(X).

Varying Y imposes R−BoxX=0; varying X gives Rf'−BoxY=0. Varying the metric gives

    F G_munu +(g_munu Box−nabla_mu nabla_nu)F
      +partial_(mu X partial_nu)Y
      −(1/2)g_munu partial X dot partial Y = kappa T_munu.

The local auxiliary action with arbitrary initial X,Y data is a **different dynamical theory**. Its off-diagonal kinetic pair is indefinite; this fact is not a ghost proof for the retarded theory, whose auxiliary homogeneous modes are prescribed rather than independently excitable. Conversely removing independent auxiliary data is not a complete stability theorem. Ordinary variation of a purely retarded nonlocal functional generally symmetrizes inverse kernels or produces advanced terms. The causal model is defined by the conserved equations with the retarded prescription, as the primary source states; it is not obtained by naively varying only a retarded single-history kernel. No underlying Schwinger–Keldysh effective action or UV health result is proved here.

## 2. General-dimensional FRW equations

For homogeneous U, BoxU=−ddot U−nH dot U and

    R=2n dot H+n(n+1)H²,
    X(t)=−integral_ti^t du a(u)^−n integral_ti^u dv a(v)^n R(v),
    ddot X+nH dot X=−R,
    ddot Y+nH dot Y=−R f'(X).

Writing A_n=n(n−1)/2, the two independent metric components are

    E00 = A_n H² F+nH dot F+(1/2)dot X dot Y = kappa rho,
    Esp = −[(n−1)dot H+A_n H²]F−ddot F−(n−1)H dot F
           +(1/2)dot X dot Y = kappa p.

Their sum is

    −(n−1)F dot H+H dot F−ddot F+dot X dot Y=kappa(rho+p).

The signs match the primary4D equations with Y=Box_ret^-1(Rf'), including the plus kinetic product in both00 and spatial components. Papers using an auxiliary U=−Y require a sign translation; no plus-sign local-coupling formula is transplanted here. The derivation uses n>=2 for the vacuum discussion; d2 has topological Einstein gravity and is outside this cosmological normalization.

## 3. A constant vacuum has a secular retarded curvature response

On prescribed exact expanding deSitter H>0 starting at t_i0,

    R=n(n+1)H²,
    X=−(n+1)[Ht−(1−exp(−nHt))/n],
    dot X=−(n+1)H[1−exp(−nHt)].

Thus constant R does not imply constant X: Box of a constant vanishes and cannot be replaced by an assigned inverse eigenvalue. The initial surface breaks deSitter-invariant time translation in this memory variable. X runs monotonically from0 to−infinity.

For the cheapest f=alpha X, zero retarded data give Y=alpha X,F=1+2alpha X. The initial00 equation has E00(0)=A_n H², while the spatial equation adds a mismatch

    [E00+Esp](0)=2alpha R.

A constant vacuum needs this sum zero, so alpha=0 for H>0. At long times E00 has secular slope−alpha n(n²−1)H³. Even checking only00 later cannot identify a constant vacuum with this prescribed H. These statements exclude exact constant-H, constant-rho evolution under the specified initial data; they do not exclude time-dependent solutions or a vacuum-like epoch after prior history.

## 4. Stronger exact obstruction, not limited to linear f

Let f be smooth enough for the displayed equations and impose exact deSitter and constant rho,p=−rho from the same zero-data retarded surface. Initial00 sets

    kappa rho=A_n H² F0, F0=1+f(0),
    F(0)=F0, dot F(0)=0.

Eliminate dot X dot Y using the vacuum sum equation. Both metric components together give

    ddot F+(2n−1)H dot F+n(n−1)H²(F−F0)=0.

Its homogeneous roots are−(n−1)H and−nH. Initial zero displacement and velocity force F=F0 identically. The vacuum sum then requires dot X dot Y=0. Since dot X is nonzero for every t>0, dot Y=0; retarded initial Y0 gives Y=0, and consequently f(X(t))=f(0) throughout X in(−infinity,0].

Therefore **an exact deSitter phase beginning at the zero-data retarded initial surface permits only a constant distortion on its entire visited negative-X branch**. A globally real-analytic f on a connected domain containing that branch would be constant there and throughout its analytic continuation. A smooth function constant on X<=0 but varying on X>0 is an exception outside the visited branch; it still supplies only constant EH renormalization for this cosmology. Singular/distributional f, different retarded histories, additional operators or nonvacuum matter are not covered.

If exact deSitter begins after previous evolution, F0 and dot F0 need not match these zero-data values. The same ODE then admits decaying transients around kappa rho/(A_n H²); that necessary metric condition alone does not construct a distortion satisfying both auxiliary equations. The initial-deSitter theorem must not be silently extended to arbitrary late histories.

## 5. Legitimate escape: solve a saturating distortion with all equations

Take f(X)=beta[1−exp(X)], beta>=0. It has f(0)=0, f' =f''=−beta exp(X), and approaches beta as X becomes large negative. The nonlocal effect saturates in f but the second retarded field retains history. Instead of prescribing exact H, evolve the complete homogeneous differential system with constant vacuum and optional conserved pressureless matter. Define m=rho_m/rho_v, choose units kappa rho_v=A_n, and use

    D=(n−1)F−4n f',
    dot F=f' dot X+dot Y,
    dot H=[(n+1)H dot F−f'' dot X²
            +2n(n+1)f' H²+dot X dot Y−A_n m]/D,
    dot m=−nH m.

The remaining auxiliary equations are those above. Initial X,Y and their velocities vanish; H(0)=sqrt(1+m0). This follows from the00 constraint since f(0)=0. We evolve n2,3,4; beta0,.05,.2; t0→80, with DOP853 rtol2e-10,atol2e-12,max-step.25. The initial constraint is propagated and its independently computed residual is monitored. Positive F and D on these runs are background regularity checks, not a full retarded perturbation-health proof.

The bounded solutions approach constant H with f' negligible and F approaching1+beta+Y_infinity. In4D:

| beta, initial m | H_final | F_final | Y_final |
|---|---:|---:|---:|
| 0,0 | 1 | 1 | 0 |
| .05,0 | .935114768 | 1.143589525 | .093589525 |
| .2,0 | .798924749 | 1.566708684 | .366708684 |
| .2,10 | .804323962 | 1.545745480 | .345745480 |

For beta.2,m0 the maximum fractional00 residual is6.31e-11; for m10 it is1.47e-10. Late H²F=1 within2.5e-11. Tightening rtol to2e-12 changes H_final by6.72e-13 and F_final1.55e-12. The added matter redshifts below3.1e-84 by the final time, yet the late auxiliary/coupling value differs. This is an actual same-equation history dependence, not arbitrary free auxiliary data at the final surface.

These finite results exhibit a consistent asymptotic escape from the exact-initial-deSitter obstruction. They are not a theorem of convergence for every beta, dimension or initial history, and no arbitrary large-vacuum self-tuning is demonstrated. Beta and f shape remain inputs. The clock scale is set by the initial density/time units; the model introduces no MOND force scale by this calculation.

## 6. Independent local Newton calculation and its measurement dictionary

Freeze a slowly evolving homogeneous background with values Fbar,pbar=f'(Xbar), and consider nonrelativistic matter perturbations with k/a>>H, after their retarded near-zone response has settled. Neglect background-gradient/H² corrections relative to the local k² terms. Then

    delta X≈Box^-1 delta R,
    delta Y≈pbar delta X,
    delta F≈2pbar delta X,
    Dbar=(n−1)Fbar−4n pbar,
    delta R=2kappa delta rho/Dbar.

The last relation is the trace of the linearized metric equation, not a guessed effective-G substitution. For metric

    ds²=−(1+2Psi)dt²+(1−2Phi)delta_ij dx_i dx_j,

Psi is the test-force potential. The spatial equation gives Fbar[(n−2)Phi−Psi]=delta F and00 gives Fbar(n−1)laplacian Phi−laplacian delta F=kappa delta rho. Hence for n>=3,

    G_N,dyn/G_N,b = (1/Fbar)[1−4pbar/((n−2)Dbar)].

The reference bare GR Poisson coefficient is kappa(n−2)/(n−1). If g=G_N,b M/r^(n−1) defines the physical force constant, sphere flux gives

    Omega_(n−1)=2pi^(n/2)/Gamma(n/2),
    G_N,b=8pi(n−2)G_EH,b/[(n−1)Omega_(n−1)].

Thus the formula above is a ratio of **force-calibrated Newton constants**, not an identification G_N=G_EH in every dimension. In4D these constants coincide, and only there we write G_dyn/G_b without the extra conversion:

    G_dyn/G_b=(Fbar−8pbar)/[Fbar(Fbar−6pbar)],
    G_lens/G_b=1/Fbar,
    Phi/Psi=(Fbar−4pbar)/(Fbar−8pbar).

Here delta R=2laplacian(2Phi−Psi), and off-diagonal Fbar(Phi−Psi)=delta F. Authors interchanging the names of the time/spatial potentials give swapped intermediate formulas; the source-to-test-force dictionary above fixes which coupling is measured. In d3 the bare GR Newton potential coefficient is zero, so the ratio to that coefficient is undefined; we do not use a4D formula there. Singular Fbar or Dbar invalidates this reduction.

For the saturating4D beta.2 model, the initial local dynamic coupling is1.181818 G_b even though initial F1. Thus local force is not simply G_b/F when f' is active. At late times pbar→0 and **both local and vacuum couplings become G_b/F_infinity**. The vacuum history has G_dyn/G_b≈.63828; the matter history≈.646937. Asymptotic00 then reads

    H_infinity² = 8pi G_dyn,infinity rho_v/3.

The apparent vacuum suppression relative to the bare coefficient disappears when expressed using the measured local Newton coefficient at that same asymptotic epoch. This escape renormalizes gravity together; it does not selectively degravitate homogeneous vacuum while preserving local gravity. No such equivalence is asserted during the evolving intermediate regime, where the local coupling and auxiliary terms differ.

This perturbative response is linear in source mass with a Newtonian spatial kernel. It does not yield deep MOND sqrt(M_b)/r or fix a0. A nonlinear galaxy solution, its source/test-metric normalization and cosmological boundary would be a new obligation. An arbitrary f reconstructed to reproduce a desired cosmology is neither that galaxy solution nor a32pi selector. Any claim for Lambda c4/a0² must use the same action to derive a0 and the physical local G before comparing constants.

## 7. Uniform late coupling result on an exact deSitter segment

The coordinator suggested the following stronger continuation; I reconstructed it independently. Suppose an exact expanding deSitter segment persists to arbitrarily late time, with constant vacuum and finite auxiliary data inherited from any earlier retarded history. Let F_Lambda=kappa rho_v/(A_n H²) be finite and positive. The metric ODE from section4 now has the general solution

    F=F_Lambda+C_n exp(−nH tau)+C_(n−1) exp(−(n−1)H tau).

Also dot X→−(n+1)H. The vacuum sum requires dot X dot Y=ddot F−H dot F, so dot Y→0. Since dot F=f' dot X+dot Y, f'(X)→0. Therefore the frozen near-zone local coupling converges toG_N,b/F_Lambda, while the Einstein vacuum coefficient isG_EH,b/F_Lambda: their **relative renormalizations** coincide. The exact force-unit Friedmann relation is

    H²=[2Omega_(n−1)/(n(n−2))] G_N,dyn,infinity rho_v,

for n>=3, reducing to8piG_dyn rho_v/3 in4D. It is incorrect to equate the raw Einstein action and force constants outside4D. This conclusion is independent of earlier history and of the detailed smooth distortion, provided the stated exact-segment and local-response assumptions hold. Earlier history can change F_Lambda and the solution's H; it does not sustain differential late vacuum/local coupling within this limit.

This theorem is stronger than the finite saturation example but does not automatically apply to every merely asymptotic H→H_infinity trajectory: one also needs decay/control of dot H, F derivatives and auxiliary limits. The numerical examples supply bounded corroboration of those limits in their runs, not a universal extension theorem. Similarly an isolated finite-duration near-deSitter interval does not justify a tau→infinity conclusion.

A separate frozen-background diagnostic is

    [G_N,dyn/G_N,b]/[G_EH,pref/G_EH,b] < (n−1)²/[n(n−2)]
    G_EH,pref/G_EH,b=1/Fbar

when n>=3,Fbar>0,Dbar>0. Subtracting the left side from the bound gives exactly(n−1)Fbar/[n(n−2)Dbar]>0. If G_N,dyn>0, the reciprocal relative Einstein-prefactor/local-force renormalization ratio is greater than1−1/(n−1)², hence greater than3/4 in4D. This is a bound relative to the instantaneous EH prefactor, **not** a definition of a vacuum response during evolving FRW, where derivative and kinetic terms are present. It cannot be used to replace the full cosmological equations by G_b/Fbar.

## Audit, failures and next implication

The primary model and retarded FRW signs were checked directly. General-dimensional expressions, initial-deSitter proof and local trace/source dictionary were independently derived. The coordinator separately reconstructed the exact F ODE and4D local coupling, agreeing after potential-label conventions were made explicit. A peer review corrected the general-dimensional action-versus-force constant labels; the ratio formula is unchanged, and fresh evidence pins the explicit sphere-flux calibration. No old spatial heat-kernel blindness argument is repeated here.

One initial check failed because SymPy's structurally different factorizations were compared by literal equality; algebraic simplification repaired that predicate without changing the derived roots. Its direct development output is retained and not counted as final evidence. Negative controls deliberately replace the secular inverse by a constant, discard the spatial vacuum equation, or identify the active local coupling with1/F; each is rejected. Fresh standard bounded records preserve positive and expected-failed results, and their manifests authenticate execution rather than proving physical health.

The smallest missing implication is a specific healthy causal nonlinear action/distortion and cosmological boundary that suppresses vacuum relative to **measured** local gravity while also supplying the actual MOND source law and protected a0 relation. The current nonlocal model supplies a memory mechanism, a real late-time escape and free reconstruction choices, but no such selector. Covariant equations alone do not remove functional or history inputs. Source-cache restoration at recorded hashes is required for future source-audit reruns.
