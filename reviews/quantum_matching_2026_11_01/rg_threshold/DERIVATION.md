# TP02 reduced threshold/RG matching and pressure comparator

## Result and exact scope

The old full one-loop thresholds have been combined with all running
couplings, the dimensional parameter f, and the canonical field dictionary.
One-loop Callan-Symanzik cancellation is exact. Two-loop beta/gamma
coefficients are independently reconstructed in `../rg_derivation/`.
The calculation then separates RG-resummed one-loop thresholds, the
CS-required reduced two-loop scale logarithms, and an explicitly computed
finite heavy-normal relaxation subset. Direct finite two-loop diagrams and
direct finite kinetic threshold graphs remain uncalculated.

The waterbag exp(2s) source is a comparator. The native phase source and
its occupied heavy response are derived/tested separately in
`../matter_coupling/`; no microscopic waterbag portal is inferred here.

## 1. One-loop consistency before improvement

Use Delta=30h^2+lambda^2 and U0=f^2lambda^2/Delta. On the actual stationary
classical valley the full TP01 supertrace is

    S4=STr M^4=6f^2h^2lambda^2(29lambda^2-200g^2)/Delta^2.

Let beta1 denote the independent one-loop nonrenormalization betas. Exact
parameter differentiation, including beta_f=f gammaX, gives

    C1 := beta1.dU0=S4/(32pi^2).

The full threshold contribution satisfies Q partial_Q U1=-C1. Therefore
the reduced one-loop CS equation cancels for arbitrary positive couplings,
not just on the old critical surface. The full tree field-gradient term
vanishes because the entire tree valley is stationary. Testing only the
special S4=0 point would not have established this normalization.

For arbitrary f and subtraction scale Q, every noncanceling mass square
is f times the f=1 mass square at X/sqrt(f). Hence the exact restoration
of dimensions and the common logarithm is

    U1(X,c,Q)=f^2 CW_f=1(X/sqrt(f);h,lambda,g)
                               -ln(Q/sqrt(f)) C1(c).

All scalar, gauge and mixed gaugino thresholds are retained. A radial
leading logarithm is not substituted for the finite spectrum.

## 2. Characteristics and re-minimization

Write t=ln(Q/Q0). The retained original canonical singlet obeys

    dot X=-gammaX X,
    dot h=h(gammaX+2gammaA),
    dot lambda=lambda(gammaB+2gammaA),
    dot f=f gammaX.

The gauge beta is run at the same declared order. The independently
checked two-loop coefficients and their primary-source conventions are in
the algebra worker's DERIVATION.md and SOURCE_RECORD.json.

The classical flat coordinate and effective linear F parameter satisfy

    T=sqrt(Delta)X/lambda, f_eff=f lambda/sqrt(Delta),
    dot T/T=-gamma_eff, dot f_eff/f_eff=gamma_eff,
    gamma_eff=(lambda^2 gammaX+30h^2 gammaB)/Delta.

Thus f_eff T=fX is invariant. At the reference scale T is a fixed multiple
of X, so their reference logarithmic radial coordinates agree. It would
be incorrect to transport T with gammaX or to use constant canonical s.

The re-minimized b=hX/lambda obeys dot b/b=-gammaB. In contrast,

    dot a/a=-gammaA+[lambda^2/Delta](gammaX-gammaB),
    a^2=2fh/Delta.

This normal drift is why evaluating U0+U1 on a running tree valley is
not by itself a complete two-loop matched potential.

The relation g^2=29lambda^2/200 is imposed only as a reference trial input
at Q0. It is not reset during the evolution. In fact on that surface

    d(29lambda^2-200g^2)/dt
      =29lambda^2(16h^2+13lambda^2)/(4*16pi^2)>0.

## 3. What the reduced CS logarithms determine

Define Ured by minimizing the full quantum potential over physical heavy
normal fields at fixed retained X, after quotienting gauge directions.
Assume a local smooth heavy branch and diagonal multiplicative field
renormalization. Because the heavy gradient vanishes at that minimum,

    [Q partial_Q+beta.partial_c-gammaX X partial_X]Ured=0.

In a loop expansion Ured1 is the full one-loop potential evaluated on the
tree valley, while

    Ured2=V2|tree-.5 (grad_perp V1)^T H0_perp^-1 grad_perp V1.

Thus the heavy drift and relaxation logarithms are included when the CS
operator acts on the *reduced* U1, rather than discarded.

At a fixed local matching scale Qm define D1=beta1.partial_c-gammaX1 X
partial_X and C2=beta2.partial_c U0=2U0 gamma_eff2. If
delta=ln(Q/Qm), the scale-dependent part required at order two is

    U2log=-delta [D1 U1(X,c,Qm)+C2(c)]
                                  +delta^2 D1 C1(c)/2.

The code holds Qm fixed while taking D1. Its field dependence enters later
when differentiating the final profile in the physical reference X0.
Using the final running coefficients instead of central coefficients in
this order-two correction changes only higher orders. This expression
does not compute the finite function Ured2(X,c,Qm). We do not declare that
function zero as a property of the physical model.

Numerical partial schemes are distinguished:

- `fixed`: full fixed-reference one-loop potential;
- `rg1`: one-loop characteristics plus full one-loop thresholds;
- `rg2`: two-loop characteristics plus full one-loop thresholds;
- `rg2log`: rg2 plus the explicit U2log about the central matching scale.

At eta=1 the last two coincide because delta=0. The finite matching
remainder is omitted from both, not calculated by a scale choice.

## 4. Trial inputs, scale and derivative controls

Reference units are Q0=1,f0=1. The unselected equal trial couplings are
h0=lambda0=e in {.01,.03,.05,.1}, with g0=sqrt(29/200)e. The smooth
matching proxy is

    c0=e/31, z0=eX0/sqrt(c0),
    Qm(X0)=sqrt(c0)*sqrt(1+z0^2), Q=eta Qm, eta in {.5,1,2}.

This is a full-theory mass-independent DR convention with finite
thresholds evaluated explicitly. It is not a sequentially decoupled
low-energy EFT matched across every light/unbroken gauge threshold.
The proxy follows the heavy field-dependent masses without vanishing at
the origin. Its variation probes a truncation prescription, not dynamics.

All coupling and field characteristics use 32 RK4 steps with 50-digit
arithmetic, compared with64. At e=.03 the potential step difference is
1.31e-28 and the relative angular coefficient difference is1.31e-26.
The integrated T characteristic and algebraically reconstructed T agree.
Reference-log field derivatives use a five-point stencil and separate
direct mpmath differentiation at all reported roots and witnesses.

At e=.03 and the inherited minimum, the eta-scale spread is2.78e-11 for
rg2 and2.47e-15 for rg2log. This checks the CS completion. It supplies no
bound on unknown finite potential or kinetic matching terms.

## 5. Old waterbag comparator

For the assumed W=k rho^(5/3)exp(-2s)+U(s), s=ln(X0/Xmin), the unchanged
identities are

    E=U_s/2, P=U_s/3-U,
    D_waterbag=U_ss+2U_s,
    dP/dlnrho=5U_s(U_ss-3U_s)/(9D_waterbag).

Only U_s>0 and D_waterbag>0 define an admitted local radial branch. The
CS-completed scale variants retain the nearby pressure root and a
negative-compressibility witness at X0/Xmin=1.2 for all four weak trials.
Detailed values are in the run_pressure_* results and REPORT.md. The
unknown phase level cancels from the conditional density comparison

    rho/rho_*=[U_s exp(2s)/(3Bcurv)]^(3/5), Bcurv=Uss(Xmin)/9.

This is not a physical acceleration or absolute density prediction.

## 6. A genuine finite matching subset

At fixed X, unbroken gauge symmetry and CP restrict one-loop heavy
tadpoles to A=i aD,B=bD. The tree potential and its normal Hessian are

    V0=(f-15ha^2)^2+(15/2)lambda^2 a^4
                                      +30a^2(hX-lambda b)^2,
    Haa=120fh, Hbb=60lambda^2 a^2, Hab=0.

These derivatives use a,b themselves; their noncanonical normalization
must not be dropped. Compute the full one-loop tadpoles ga=CW_a and
gb=CW_b with spectral Frechet derivatives,

    partial_r CW=sum_spin weight Tr[h'(M_spin^2) partial_r M_spin^2]
                                                        /(64pi^2),
    h'(x)=2x[ln(x/Q^2)-1], h'(0)=0.

The scalar Hessian derivative includes D terms, the 73-Weyl derivative
includes all gauge mixing, and the vector derivative includes all twelve
massive gauge fields. Polynomial matrix-direction central differences
check those derivatives independently. CP-odd singlet tadpoles vanish.
No off-shell negative-mass potential is substituted for a stable vacuum;
only the well-defined first derivative at zero masses is used. This does
not license arbitrary second off-shell derivatives at Goldstone zero.

The vacuum shifts and their finite reduced contribution are

    deltaa=-ga/Haa, deltab=-gb/Hbb,
    deltaUrelax=-.5[ga^2/Haa+gb^2/Hbb].

Twelve weak-coupling states have relative shifts below1e-2 (in fact the
largest sampled shifts are much smaller). The relative shifts and actual
matrix error controls are retained in run_relaxation/result.json.

This subset is gauge/scheme dependent. Its gauge dependence generally
cancels only with the direct finite two-loop diagrams, which remain
uncalculated. Adding it is a sensitivity/matching-subset test, neither an
upper nor lower bound on the final physical potential. The central-Qm
finite term is added once; it is not added again to CS scale logarithms.

## 7. Angular and occupied-state interface

The RG-only angular coefficient in reference coordinates is

    F_RG=[Delta(t)/lambda(t)^2] X(t)^2=|T(t)|^2.

It is a projected running tree coefficient, not a complete finite kinetic
matching result. The actual supersymmetry-breaking mass splittings are
retained in the spectrum; no uncontrolled small-F Kahler expansion is
assumed. Component two-point/derivative thresholds remain missing.

Since the R phase rotates X and B, but not A, the computed heavy shift
gives the geometric subset deltaFtheta=60b deltab. More importantly, at
fixed phase charge the occupied normal source also displaces B. Its
complete same-order square must be kept, not only the vacuum metric shift.
In the grand-potential representation used by the matter worker,

    Omega=U_RG-omega^2 F_RG
            -.5[ga^2/Haa+(gb-omega^2*60b)^2/Hbb].

It contains the vacuum relaxation, angular geometric correction and
omega^4 term. At fixed charge n, the same source is
Jb=gb-E(60b/F0), E=n^2/(4F0), F0=X^2+30b^2.
The normal_data_reference API exposes ga,gb,Haa,Hbb,b,F0 and60b at the
central matching scale for this calculation. The matter worker owns its
phase EOS and stability test. Direct derivative graphs and higher-order
current matching still remain absent.

## 8. Precise perturbative persistence statement

At fixed dimensionless z, scale h,lambda,g as e and X as e^(-1/2), with
f fixed. Every massive mass square is proportional to e. Consequently
the full one-loop potential is e^2 times a dimensionless shape, finite
two-loop diagrams and normal-relaxation terms scale as e^4, and finite
metric corrections scale relatively as e^2. Matching-scale RG logs add
powers of ln e but e^2 ln^k e tends to zero for fixed finite k.

For the phase state E scales as U_s, hence as e^2; F scales as e^(-1),
so omega^2 scales as e^3. Its occupied heavy source then has the same
e^(5/2) scaling as the one-loop normal tadpole, making its relaxation
contribution e^4 as well. This explains why the occupied square cannot be
discarded as a higher-order effect than vacuum relaxation.

Therefore a strict sign failure of the leading one-loop source is stable
asymptotically under a bounded matched C^2 remainder on a compact admitted
branch. This implication is conditional on such an expansion and the
declared source/kinetic matching; it is not a proven finite-e error bound.
The independent algebra worker supplies explicit derivative margin
budgets in `../rg_derivation/persistence_001/`, without asserting the
unknown matching remainders meet them. Actual finite graph and derivative
matching is what remains to turn the finite-e evidence into a controlled
physical verdict.
