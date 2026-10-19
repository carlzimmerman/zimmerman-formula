# Independent charged SU(2) far-field derivation

Prepared before reading the target RAW, REPORT, contracts, code, results, or source PDF. The only inputs are the parent task's operator/convention statement. This is an analytic audit; no finite executable assertion has yet been run.

## Contract and conventions

Four-dimensional Euclidean SU(2), tr(Ta Tb)=delta_ab/2, fixed circle circumference L. A4=h T3, commuting Cartan spatial field, E_i=partial_i h and B_i=(1/2)epsilon_ijk F^3_jk. D has charge eigenvalues +/-1; omega_n=2 pi n/L. The effective action is Gamma_1=(1/2)Tr_real-adj,vector log H - Tr_real-adj log M, H=-D^2 delta-2 ad F, M=-D^2. The determinant contribution to log weight is -Gamma_1. The derivation describes a local bulk derivative expansion on a gapped holonomy chamber 0<nu=Lh/(2pi)<1. It does not determine a finite-ball spectral determinant or its boundary heat-kernel terms.

## Charged and frequency counting

Complexifying the two-dimensional real charged adjoint subspace gives roots q=+1,-1. The real trace equals the sum of their complex eigenvalue traces. The q=-1 spectrum at n is the q=+1 spectrum at -n, including the reversed Abelian charge. Thus, for parity-even invariants, the charged pair gives, for EACH n in Z, one complex four-vector trace log H_n minus TWO complex scalar traces log Q_n, with Q_n=-D_i^2+p_n^2, p_n=omega_n+h. The orbital coefficient is 4-2=2 scalar traces. This includes n=0 only once after combining the roots. It does not include a factor of L: the normalized circle-mode trace is a discrete sum, and a single mode determinant is three dimensional. The density divided by L would be a four-dimensional density.

## One three-dimensional scalar trace

For m=|p|>0, the constant magnetic heat kernel is (4pi s)^(-3/2) exp(-m^2 s) Bs/sinh(Bs). Since log Q=-int ds K/s and Bs/sinh(Bs)=1-B^2s^2/6+..., one scalar trace contributes +B^2/(48pi m).

For X=m^2, the scalar two-insertion bubble is
I(k)=int d^3p/(2pi)^3 [(p^2+m^2)((p+k)^2+m^2)]^-1
=arctan(k/(2m))/(4pi k)=1/(8pi m)-k^2/(96pi m^3)+... .
The quadratic log term is -deltaX(k)deltaX(-k)I(k)/2, hence + (partial X)^2/(192pi m^3)=+(partial m)^2/(48pi m). This is the integration-by-parts (IBP) bulk representative.

A useful local diagonal heat-kernel representative retains a divergence:
Gamma_scalar,2 = int [B^2/(48pi m)+(partial m)^2/(48pi m)+Delta m/(24pi)].
Indeed, before substituting X=m^2 it has +Delta X/(48pi m) -(partial X)^2/(192pi m^3). The integrated bubble fixes the bulk representative; it does not authorize dropping finite-domain surfaces.

## Vector spin term

In one charged complex sector V_mu nu=-2 i F_mu nu (the overall charge sign cancels quadratically). tr_Lor V^2=8(B^2+E^2). The second log term is -1/2 tr_Lor V^2 I(0)=- (B^2+E^2)/(2pi m). There is no linear term. Combining two orbital scalar traces with the spin term gives, for a strictly three-dimensional unregulated mode in IBP convention,
Gamma_n,2 = -11/(24pi |p_n|) int (B^2+E^2).
For static n=0, Gamma_0,2=-11/(24pi h) int(B^2+E^2), 0<h. The corresponding determinant log weight has the opposite sign.

## Full KK sum and the regulator-sensitive finite electric constant

The per-mode coefficient alone cannot fix the finite electric-versus-magnetic constant of the FOUR-dimensional determinant. Summing an already specialized d=3 answer discards an evanescent term times the ultraviolet pole. A four-dimensional background-gauge-invariant Pauli-Villars subtraction supplies an independent derivation. Replace each Q by Q+M^2 and H by H+M^2, and subtract their logs. Let m_M=sqrt(p_n^2+M^2). The regulated magnetic coefficient is
K_B(M)=-11/(24pi) sum_n [1/|p_n|-1/m_M].
The electric orbital derivative acts on m_M and gives p_n^2/m_M^3, not 1/m_M. Consequently
K_E(M)=K_B(M)+1/(24pi) sum_n M^2/(p_n^2+M^2)^(3/2).
For M L >>1, the sum in the last term tends to L/pi, so
K_E-K_B=L/(24pi^2)
in the IBP bulk representative. This finite anisotropy is independent of nu away from the gapless endpoints. A scheme change of the renormalized four-dimensional gauge coupling shifts B and E equally.

Cross-check in dimensional regularization: with d=3-2epsilon spatial dimensions and D=d+1 vector components, C_d=(4pi)^(-d/2) Gamma(2-d/2) |p|^(d-4), the one-mode coefficients are [(d-1)/6-4]C_d for B^2 and [(d-1)(4-d)/6-4]C_d for E^2. Their difference is (d-1)(3-d) C_d/6. The Matsubara sum of C_d has pole L/(16pi^2 epsilon), producing L/(24pi^2). This is why equal per-mode coefficients do not justify equal renormalized full-KK coefficients.

A symmetric harmonic subtraction defines
F(nu)=1/nu+sum_{n>=1}[1/(n+nu)+1/(n-nu)-2/n]
=-psi(nu)-psi(1-nu)-2gamma_E.
The universal holonomy-dependent magnetic coefficient is -11L F(nu)/(48pi^2). A nu-independent renormalization constant remains. A cutoff N contributes -11L H_N/(24pi^2) to the B^2 coefficient; cancellation by tree L/(2g_bare^2) requires d(1/g^2)/dlog Lambda=11/(12pi^2)=b0/(8pi^2), b0=22/3.

## Surfaces and Coulomb equations of motion

The strictly three-dimensional scalar local density differs from its IBP representative by Delta m/(24pi). With two orbital traces and PV subtraction the charged KK divergence is
Delta F_0(h)/(12pi), F_0(h)=sum_n [|omega_n+h|-sqrt((omega_n+h)^2+M^2)],
up to h-independent terms. In the large-M limit, F_0'(h)=1-2nu=1-Lh/pi and F_0''(h)=-L/pi within the chamber. Therefore the local-minus-IBP divergence is
[(1-Lh/pi)Delta h-(L/pi)E^2]/(12pi).
A sign convention for a source's log weight, or an intermediate EOM-separated representative, can move signs around; the invariant comparison must include the explicit divergence and the sign of Gamma.

For h=v-1/r, Delta h=0 on a Coulomb annulus but the divergence above is nonzero: its boundary integral is [4pi F_0'(h)]_inner^outer/(12pi). Its outer boundary has +L/(3pi R). Thus imposing Delta h=0 and discarding a related divergence cannot be used interchangeably on a finite ball. More generally E^2/h=div(log h grad h)-log h Delta h, so even the static electric kinetic term is an EOM term plus a surface; the surface has an inverse-radius expansion. Boundary data and spectral boundary conditions are needed to give a complete determinant's finite-radius tail. Bulk coefficients alone are not a finite-ball result.

## Radial kinetic tail and screened versus unscreened holonomy

For an IBP bulk density K_B(h)B^2+K_E(h)E^2 and the off-shell BPS Coulomb tail B^2=E^2=r^-4, h=v-1/r, the leading tail is
Gamma_bulk(R)=Gamma_bulk(infinity)-4pi [K_B(v)+K_E(v)]/R+O(R^-2).
For static n=0 this gives +11/(3v R) in Gamma, and -11/(3v R) in log weight. This statement uses the stipulated bulk convention, without adding determinant boundary terms.

If the holonomy is physically massive and approaches a stable vacuum as exp(-m_h r)/r, its electric kinetic and potential tails decay exponentially. The algebraic kinetic 1/R term then comes from B only, with coefficient -4pi K_B(v)/R in Gamma. A stable nontrivial holonomy requires the specified deformation or other stabilizing dynamics; the pure-YM GPY potential is not minimized at nu=1/2.

## GPY zero-derivative term

Up to a nu-independent constant, the charged pure-YM one-loop action density after the time integral is
V_3(nu)=4pi^2/(3L^3) nu^2(1-nu)^2.
For nu(r)=nu_infinity-L/(2pi r), the vacuum-subtracted radial integral generally has R^2, R, and log R terms, as follows directly from its quartic polynomial. Its quartic term is L/(12pi^2 r^4), giving an inverse-radius contribution -L/(3pi R) to Gamma and +L/(3pi R) to log weight. This is part of a generally divergent off-shell Coulomb evaluation, not a finite physical monopole determinant by itself. Screening removes the algebraic potential tail.

## Matching to the dual photon

Define the magnetic action S_B=(kappa_B/2) int B^2. With tree tr normalization above, kappa_B=L/g^2+2 K_B (plus any explicitly specified higher-loop/matter contribution). The minimally charged SU(2) monopole has Cartan flux 4pi. Enforcing Bianchi identity with i sigma div B/(4pi) and integrating out B yields S_dual=(1/(32pi^2 kappa_B)) int(partial sigma)^2. Thus if S_dual=(kappa_dual/2)int(partial sigma)^2,
kappa_dual=1/(16pi^2 kappa_B).
The electric coefficient, the sum K_B+K_E evaluated on an unscreened BPS tail, the GPY term, and a log-weight coefficient are not replacements for kappa_B.

## Scope

The derivation is analytic and conditional on a gapped Cartan derivative expansion and a four-dimensional gauge-consistent UV regulator. It does not test the monopole core, zero modes, collective coordinates, physical alpha, full QCD, global determinant phases, or a finite-domain spectral boundary problem. No target files were consulted before saving this document.
