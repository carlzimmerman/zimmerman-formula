# Independent scalar–matter kinetic reconstruction

Primary verdict on the coefficient/determinant claim: proved under the stated four-dimensional, minimally coupled regular perfect-fluid/dust and nonzero-Fourier-mode hypotheses. A verdict of an invariant physical ghost or rejected cosmological branch is incomplete, with the missing IR canonical/dispersion classification stated below. The scalar Schur coefficient on the positive-charge logKGB background is

    Kclock(p)=M[3eta(1+eta-h)+kappa p²/H*²]/(h-eta)².

It controls the sign of the coupled scalar velocity form in the constrained unitary-curvature variables even with matter. Thus the early GR branch h>1+eta fails the specifically declared all-mode positive-velocity-form criterion for a finite nonzero-p band. A positive acceleration response can rescue the coefficient at sufficiently large p, not remove the entire band. No short-wavelength rapid-instability theorem follows if that band is super-Hubble. This is an independent raw-action reconstruction; the main report/checks were not yet durable at the initial write and have not been endorsed by pass count.

## Covariant coefficient and gravity mixing

All kinetic formulas here are n=3. Use M R/2, K=-c ln(X/Xref), G=-sqrt(2)c/(3H*)X^-1/2, q=sqrt(2X)>0, eta=c/(3MH*²), h=H/H*>1. The minimally sourced covariant braiding time coefficient before the new acceleration operator is

    D=K_X+2XK_XX+6Hq(G_X+XG_XX)+6X²G_X²/M.

The final term is the Einstein scalar-metric kinetic reaction. It cannot be dropped when minimally coupled matter is present. This convention is Bernardo2101.00965v2 equation3.66 with restored positive Einstein coefficient M; the local exact-version text was inspected. The ADM constraint reconstruction below independently checks the coefficient and its meaning in the coupled matter system, rather than assuming the source's vacuum G>0 statement automatically decides matter health.

Direct differentiation gives K_X=-c/X, K_XX=c/X², G_X=sqrt(2)c/(6H*)X^-3/2, G_XX=-(3/2)G_X/X. Therefore the kinetic, braid and Einstein-reaction pieces are respectively c/X,-ch/X,c eta/X, and

    D=c(1-h+eta)/X.

Minimal matter introduces its own dynamical variables; the covariantly de-braided scalar equation is not by itself a diagonalized two-field action. The coefficient's relevance to the full determinant is established next.

Independently, the literal KYY ADM coefficient definitions give

    Theta=MH-qXG_X=MH*(h-eta),
    Sigma=XK_X+2X²K_XX+12HqXG_X+6HqX²G_XX-3MH²
         =3MH*²[eta(1+h)-h²].

Thus the scalar part after the shift constraint, before matter kinetic squares, is

    Gpure=Sigma M²/Theta²+3M
         =3M eta(1+eta-h)/(h-eta)²
         =X M²D/Theta².

This equality verifies the restored Einstein-reaction normalization. It is not taken as a matter-free health verdict. For h>1,0<eta<1,Theta is nonzero throughout the tuned history, including h=1+eta.

## Regular-fluid principal square and actual full determinant

Let a minimally coupled matter scalar chi represent a regular irrotational barotropic fluid P(Y), Y=-partial chi²/2, with positive enthalpy Rm=rho_m+p_m>0 and positive sound speed cs². Define v=delta chi/chi_dot and t_shift=Delta B/a_FRW². Direct expansion of N sqrt(h)P(Y) gives the velocity/lapse principal square

    C(vdot-nu)², C=Rm/(2cs²)>0,

and the shift term +Rm v t_shift. Spatial matter pressure contributes -Rm p²v²/2. Background chi_ddot, zeta factors and other matter terms supply at most one time derivative and do not alter this two-velocity Hessian. In particular, replacing the fluid with a density source while forgetting its velocity variation would not be this calculation.

The raw gravitational shift terms are -2Theta nu t_shift+2M zetadot t_shift. Its nonzero-k constraint is consequently

    nu=d0 zetadot+Rm v/(2Theta), d0=M/Theta.

The exact added response about a homogeneous clock contributes +M kappa p²nu²: the cubic W and its scale A are absent at this order. It has no shift variation and does not add a vdot. After imposing the shift constraint the two-velocity quadratic form is

    Kclock zetadot²+C(vdot-d0 zetadot)²,
    Kclock=Gpure+kappa M³p²/Theta².

Terms involving the undifferentiated v in nu contribute only lower-derivative terms or one-derivative mixing. With the convention Lkin=(zetadot,vdot)K(zetadot,vdot)^T,

    K=[[Kclock+C d0²,-C d0],[-C d0,C]],
    det K=C Kclock.

Completing the square is an invertible field-velocity transformation for finite C>0. Hence positive fluid inertia cannot change the sign of the scalar Schur complement. This is the coupled determinant result that the pure Gpure argument alone would not establish. No v kinetic auxiliary field was omitted; lapse and shift have both been eliminated.

## Exact dust limit instead of discarding a singular square

The cs->0 limit makes C diverge, so naively using its matrix entries as an ordinary two-scalar dust Hessian is inappropriate. Exact pressureless matter has a canonical density/velocity pair. In the comoving-current density convention pi=delta rho_phys+3rho zeta, its quadratic action contains

    pi(vdot-nu)-rho p²v²/2+rho v t_shift.

Here pi is the density perturbation, not a second-velocity scalar; the background rho is positive. This form follows by varying the conserved dust-current action and eliminating the spatial current, and is consistent with the matter expansion sent by the main agent. It avoids the missing 3rho zeta vdot term that would occur if physical density and coordinate density were interchanged without transformation.

The same shift constraint gives nu=d0 zetadot+rho v/(2Theta). The invertible time-dependent change w=v-d0 zeta then gives

    pi(vdot-nu)=pi[wdot+d0_dot zeta-rho v/(2Theta)].

There is no pi zetadot left. All other scalar velocity terms have coefficient Kclock plus lower-derivative functions. Its canonical Hamiltonian therefore contains

    (p_zeta-L1)^2/(4Kclock),

where L1 is a field/matter-dependent linear momentum shift, together with the independent canonical dust pair (w,a_FRW³pi). A negative Kclock supplies a negative canonical scalar momentum direction in this chosen representation. The cs->0 singularity cannot turn this velocity square positive. An indefinite IR Hamiltonian is not by itself an invariant ghost diagnosis: a canonical momentum/coordinate exchange can trade such a term for a negative potential, and healthy dust gravity already permits a Jeans instability. At Kclock=0 the ordinary Legendre inversion in these variables fails; one must analyze the original canonical constraints/gauge variables separately rather than divide by zero or claim a physical degeneracy from this representation alone. This proves an instantaneous velocity-form sign, not an adiabatic growth rate or invariant physical ghost classification.

## Band, fold and scale limits

The coefficient is the displayed Kclock(p). On the early branch h>1+eta, it is negative when

    0<p²/H*²<3eta(h-1-eta)/kappa.

The response lifts finite-p kinetic curvature at the fold h=1+eta, while its zero-p limit vanishes there. The exact p=0 momentum constraint is exceptional because the shift Laplacian is not invertible; it is not silently included in the finite-mode reduction.

Relative to the actual cosmological H=hH*, the maximal band edge obeys

    max(pcrit²/H²)=3eta/[4kappa(1+eta)],

at h=2(1+eta). At eta=.5,kappa=.99 this is .252525..., so pcrit/H<=.502519.... Negative modes are then super-Hubble; a local high-frequency temporal WKB interpretation is unjustified. The quadratic global Fourier action still fails the additional requirement that this reduced velocity form be positive at every finite wavelength. That criterion is stronger than a verified statement of invariant IR health and is not adopted silently as a universal necessity. For sufficiently small kappa the band can extend above H, but this review supplies no full dispersion relation or faster-growth claim even then.

The background theorem remains mathematically correct and on shell. The smooth background cannot be promoted to a healthy completed theory from vacuum coefficients alone. The coupled matter result establishes a real IR sign change to classify; it does not yet reject the background as physical. The acceleration scale A remains absent from this quadratic test; changing A cannot repair this sign or select32pi. Matter gradients, full gauge/canonical dispersion, EFT admission at small X and nonlinear behavior are separate obligations. In particular the smallest missing implication is to distinguish a genuine negative-residue degree of freedom from an IR Jeans/constraint representation effect, and determine whether crossing Kclock=0 is a physical evolution singularity or a removable variable choice. The local covariant D<0 diagnosis before the acceleration response cannot simply be imported as an ultraviolet verdict for the response-completed action.

## Provenance and limits of this independent pass

Observed HEAD `cfa06dbfae97280425bbb61f862eb61468c03dce`.

- `sol61_push/puzzle_32pi/dynamical_sector_2026_10_06/kinetic_braiding/REPORT.md` SHA256 `f60cc5a4940fbd311e4cab34f1be7e60db186b51e3344cb92048c394e8596a1b`.
- `sol61_push/puzzle_32pi/dynamical_sector_2026_10_06/kinetic_braiding/sources/bernardo_2021.txt` SHA256 `cb20dc3de88e6b09646b213ad0b2a557a8fd1ff33d640e1a4ecfb45e0dcdfe94`.
- `sol61_push/puzzle_32pi/dynamical_sector_2026_10_06/kinetic_braiding/sources/kobayashi_2011.txt` SHA256 `61e46b2ff5aee388b50392681d62dda3558f61b13b9cee2fe904aad90d130d4a`.
- `sol61_push/recombination_and_structure_growth/homogeneous_clock_current_2026_10_06/REPORT.md` SHA256 `c0e0ed1b377bc1470c193a9c54796676e47e2be5403821c64a38e306c6a527e8`.


No peer source/check inputs edited or executed. Source/cache hashes authenticate the exact conventions inspected, not a universal health theorem. The algebra above was reconstructed directly from the action and matter square; no new astronomical data or finite computation is relied on. Main report/check-source hashes should be appended after they are durable if this note is used as their formal audit.

## Final durable input audit

The completed REPORT and checks were read after freezing. The full coordinate-density action retains3rho zeta nu, its pressureless canonical convention agrees with the direct Sorkin reduction, and the displayed finite-time mode equations follow from its reduced action. That tadpole contributes at most one velocity after the shift constraint, so its earlier absence from the principal-only reconstruction does not change the Hessian verdict. The B<0 and L_z=rho Kclock/M identities at Kclock0 are correct; they strengthen the reduced quadratic rank observation but do not settle a nonsingular full canonical completion. The completed report preserves the IR/Jeans caveats and does not promote the coefficient into a universal physical death claim. No concrete algebraic error found in the frozen statement.

- Final `REPORT.md` SHA256 `d99aec2e6f2bc3b9d232c932630e32131cf73fc093170d43e35ce2f705de3d5b`.
- Final `checks.py` SHA256 `7f3a2edf1a07b0a53ecd09b31365e82344cda35fc1403f99a61f0bb87fd717be`.
