# Exterior remainder and the actual mixed-boundary Schur complement

This hand argument closes the exterior-mode qualification left explicit in the bounded asymptotic algebra run. It uses the exact Cartesian potential, charge/normal-projector identities checked in asymptotic-003, and the primary-source kernel/rank audit in ../../reviews/kernel_rank/RAW_DERIVATION_v1.md. It does not rerun, alter or reinterpret numerical tolerances as an infinity proof.

## Exact exterior normal form

For t sufficiently large, a constant Gram-orthogonal change separates the neutral and charged subspaces. The actual symmetric canonical operator is

H=-d²/dt²+diag(U_c,U_n)+E(t),
U_c=diag(1-2/t+C/t²), C=(0,0,2,2,6,6),
U_n=diag(C/t²), C=(0,2,2,6).

Every entry of E and each of its finitely required derivatives is bounded by a polynomial in t times e^-t. This follows directly from K=2t e^-t/(1-e^-2t), h=1-1/t+2e^-2t/(1-e^-2t), Kprime=-Kh and hprime=(1-K²)/t² in the exact potential. It is an exponentially small coefficient statement, not an assertion that E acting on every solution is exponentially small.

The uncoupled charged pairs have g_C=e^t/t[1+a1/t+a2/t²+O(t^-3)] and d_C=t e^-t[1+O(t^-1)], with nonzero constant Wronskian. The coefficients a1=(2-C)/2,a2=(6-C)a1/4 follow by direct substitution. The C0 growing series is nonterminating; its exact reduction-of-order integral has the same displayed asymptotic expansion. The neutral pairs are exactly t^(l+1),t^-l for C=l(l+1).

Variation of constants constructs an exact fourteen-dimensional space with no charged growing coefficient: six charged decreasing seeds and eight neutral power seeds. In that space the neutral components are the chosen finite combinations of free powers plus O(e^-t poly(t)log(t)), and charged components are O(e^-t poly(t)log(t)); the same bounds hold for the derivatives needed by the wall. One way to see the relevant estimates explicitly is to use the massive Green terms

g_C(t) integral_t^infinity d_C(s) f(s)ds,
d_C(t) integral_t0^t g_C(s) f(s)ds,

with their constant Wronskian denominator. For f=e^-t poly(t), the second integral can be resonant and add polynomial/logarithmic factors, but both products remain e^-t times polynomial/logarithmic factors. For the neutral Euler pairs, choose both integration constants at infinity for the correction; exponentially decreasing forcing again gives exponentially decreasing corrections. Iteration on a sufficiently far exterior interval closes these estimates: every off-diagonal return has an additional e^-t factor, and the remaining diagonal errors also have exponential decay. Polynomial/log weights accommodate the finite resonances; they cannot introduce an algebraic correction to a prescribed neutral free power. This supplies exact outer solutions, not only solutions of the operator with K set to zero.

The remaining six exact solutions have independent charged growing coefficients. Their charged projections have the uncoupled g_C asymptotic series, up to a constant invertible growing-coefficient matrix and polynomial/logarithmic additions. Their neutral projections can be polynomial/logarithmic. Indeed E_nc g_C is generally algebraic, and the neutral Euler Green operator can add powers and logs. Feeding those polynomial neutral terms back into the charged equation gives only exponentially decreasing forcing; the direct diagonal exponential error acting on g_C is algebraic forcing of the massive equation and gives polynomial additions. Both are exponentially small *relative to g_C*. Thus neither changes any displayed algebraic coefficient in its charged e^t/t series. These variation-of-constants estimates also show why discarding the neutral tails of charged growing solutions without checking the determinant would be invalid.

## Regular connection and neutral powers

The independent kernel/rank audit proves that the regular-origin space has charged growing rank six and a four-dimensional growing-free subspace. It also proves that, per magnetic component, the latter has one translation decreasing direction and neutral growing rank three. The gauge gradient with C0 growth eliminates the non-L² C0 constant resonance. These statements use the rigorous weighted index plus its explicit bridge to the actual Coulomb Hessian; a naive unweighted Fredholm argument is not used.

Choose six regular columns with independent charged growth, and four columns with no charged growth. Within the latter, the neutral power/scattering structures are exactly those in DERIVATION.md. In blockA use

g=v0 t+gamma v6/t²,
h=v6 t³+5gamma v0+delta v6/t²,

up to exponentially decreasing terms and constant nonsingular column transformations. In blockB use translation vminus/t and an orthogonal growing column vplus t²+O(t^-1). The Wronskian fixes the stated C0 constant in h and excludes it in g. Hence neutral scattering changes the boundary determinant only at relative order t^-3. The translation tail is nonzero, and the exact neutral boundary determinants calculated in asymptotic-003 have nonzero leading coefficients.

## Charge-adapted mixed wall matrix

The normal projector PN commutes with the charge projector M0. Therefore a constant invertible row transformation separates the actual mixed wall output into six charged rows (4D+2R) and four neutral rows (3D+1R). The transformed regular boundary matrix, with the column choice above, has blocks

Fwall=[[A,B],[C,D]].

Here A is6x6 and corresponds to charged growing columns, B to their growing-free companions, C to the neutral tails of charged growing columns, and D to the four neutral columns. The actual estimates are

A=(e^t/t)[A0+A1/t+A2/t²+O(t^-3)]+O(poly(t)log(t)),
B=O(e^-t poly(t)log(t)),
C=O(poly(t)log(t)),
D=D_power(t)+O(e^-t poly(t)log(t)).

A0 is invertible. On charged growing fields the reduced normal Robin functional is u'+u/t=e^t/t[1+a1/t+O(t^-2)], so at leading order the mixed wall operator acts as the identity on each charged value vector, as does Dirichlet. Thus A^-1=O(t e^-t). Importantly C is not presumed exponential. Nevertheless

C A^-1 B=O(e^-2t poly(t)log(t)^2).

The neutral matrix D_power has a nonzero polynomial leading determinant and polynomially bounded inverse. The exact Schur identity

detFwall=detA det(D-C A^-1 B)

then proves that charged-induced neutral tails change no algebraic inverse-power coefficient. Constant row/column changes only affect the radius-independent normalization. This is the required domain-sensitive control on the actual wall; bulk quaternion pairing alone would not supply it.

## Result and scope

The six charged growing factors contribute e^(6t)t^-6 and inverse-power coefficient sum a1=-2. The four neutral powers contribute t^(1+3+2-1)=t5 and their wall determinant contributes one additional t^-1. Hence Fwall=C e^(6t)t^-2[1-2/t+O(t^-2)], with C nonzero. Dividing by the exact common reference gives

logDvec=6x-22logx+Cvec-2/x+O(x^-2).

The exact ghost has logDg=2x-6logx+log(15/8)+exponential per magnetic number. Therefore the complete static J1 Gaussian, with degeneracy three, is

logZ_J1=-3x+15logx+Cz+3/x+O(x^-2).

This coefficient is established within the specified pure-SU2 BPS action, smooth origin, actual relative mixed wall, unprimed finite modes, common unbroken auxiliary reference and fixed asymptotic m_W path. It is not a full angular/Fourier sum, UV subtraction, physical same-holonomy vacuum matching, or physical QCD A_rho.
