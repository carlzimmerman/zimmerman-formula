# Independent derivation before opening the candidate report/checks

Base: 431f22bd6fe998759b843d13113762d73356aec6. Input is the action supplied
directly by the coordinator, with c=1, signature -+++, K=4 pi G>0, beta>0,
eta>0, gamma>0, independent timelike clock, and spatial physical covector P.
Neither 03_relativity/report.md nor its checks.py has been read at this point.

Use ADM unitary gauge T=t, lapse N, shift N^i, spatial metric h_ij. Orthogonality
implies P_0=N^i P_i, P^0=0 and P^i=h^ij P_j. Therefore, exactly,

    P^mu a_mu = h^ij P_i partial_j ln N,
    E_i = [dot P_i - N^j partial_j P_i - P_j partial_i N^j]/N,
    E_mu E^mu = h^ij E_i E_j.

No lapse or spatial-metric time derivative is hidden in E when P_i is the
independent variable. This is a consequential covector convention.

## Scalar reduction at exact P=0 Minkowski

Set N=1+phi, N_i=partial_i B, h_ij=e^(2zeta) delta_ij, P_i=partial_i sigma.
Use spatial diffeomorphisms to remove the second scalar metric potential.
For a Fourier mode of nonzero wavenumber k, write b=Delta B and v=dot zeta.
The Einstein-Hilbert ADM term plus the expansion term is

    L_g = {-(6+9 beta)v² +(4+6 beta)v b - beta b²
            +2 k² zeta² +4 k² phi zeta}/(4K).

The spatial curvature terms follow directly from
R3=e^(-2zeta)[-4 Delta zeta-2(partial zeta)²], after integration by parts.
The extrinsic-curvature terms use K_ij=dot zeta delta_ij-partial_i partial_j B.
W_full=K P_i P_i/2+O(|P|³). The remaining quadratic scalar terms are

    L_P = k² phi sigma -K k² sigma²/2
          +eta k² dot sigma²/2 -gamma k⁴ sigma²/2.

The lapse equation gives zeta=-K sigma (k is nonzero). The shift equation gives

    b=(2+3 beta) dot zeta/beta.

After eliminating both, the k² potential from spatial curvature cancels the
quadratic W term exactly. The single remaining scalar has

    L_red = [eta k² + C] dot sigma²/2 -gamma k⁴ sigma²/2,
    C = K(2+3 beta)/beta >0,
    omega² = gamma k⁴/(C+eta k²).

It has positive kinetic energy and positive omega² for k>0. The k=0 homogeneous
sector was not derived by dividing the lapse constraint by k². The beta=0 limit
is not covered. At small k the branch is quadratic in k, not an ordinary linear
sound cone. At large k its phase/front speed tends to sqrt(gamma/eta).

Finite-frequency group velocity has a useful distinction:

    v_g²=(gamma/eta) t(t+2)²/(1+t)³,  t=eta k²/C.

Its derivative has sign 4-t², so its maximum is 32 gamma/(27 eta) at t=2.
Thus gamma<=eta bounds phase and high-k speed, not every group velocity.
Whether front speed alone establishes causal propagation for the constrained
full system is a separate question and is not claimed here.

## Frozen nonzero P, pure TT principal terms

At a point take locally constant spatial covector P_i and flat coefficients;
discard background gradients only for the principal-symbol check. Let h_ij be
the metric perturbation, with partial_i h_ij=0 and h_ii=0, and set perturbations
of P_i, lapse, shift and clock to zero when extracting the pure TT block.

    delta(D_i P^i)= -P_j partial_i h_ij +(P_i/2)partial_i h_jj =0,
    delta F_ij = partial_i delta P_j -partial_j delta P_i =0,
    delta E_i =0,
    delta theta =dot h_ii/2 =0,
    delta a_i =0.

Hence the Hodge divergence-plus-curl stiffness contributes no quadratic pure
TT derivative term, unlike the naive |D_i P_j|² operator. W changes only
algebraic terms. The tensor principal action remains

    L_TT=[dot h_ij dot h_ij -partial_l h_ij partial_l h_ij]/(16K).

For an explicit wave along z, h_xx=A,h_yy=-A,h_xy=B, the naive |DP|² at fixed
P instead equals |P|²[(A')²+(B')²]/2. This is a real difference between the
two operators; replacing one by the other on curved slices is not innocuous.
No claim about arbitrary on-shell polarized backgrounds or all mixed
characteristics follows from this pure TT calculation.

## Weak static lifting check

At static shift zero, theta=0 and E=0. At leading weak-field order the spatial
metric equation gives zeta=-phi. Substitution in the static EH terms yields
-|grad phi|²/(2K). The other terms give P dot grad phi-W_full and the Hodge
stiffness. In flat three-space, with vanishing boundary contribution,

    integral [(div P)²+F_ij F_ij/2] = integral partial_i P_j partial_i P_j.

This reproduces the expanded S2 static action; equivalently use the completed
square with W_rem=W_full-K P²/2. No immediate algebraic obstruction was found
to this restricted lifting. Full source-matched static solutions, PPN, strong
coupling, nonlinear constraints and finite-background stability are unresolved.
