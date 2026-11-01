# TP02 coordinator RG reconstruction

This is a separate algebraic reconstruction from the raw superpotential,
the one-loop Yukawa Gram matrix and the primary Martin–Vaughn formulas.
It is not a calculation of the finite two-loop threshold potential.
Couplings f,h,lambda,g are positive and L=16 pi².

## Group contractions

For each component in sectors X,A,B, define
Q_i=(1/2) sum_pq |Y_ipq|². The diagonal Gram values are

    Q_X=12h²,
    Q_A=h²+(21/10)lambda²,
    Q_B=(21/20)lambda².

The quartic-Yukawa contraction in the two-loop gamma reduces to
-sum_mn |Y_imn|² Q_n. For X the two internal legs are A; for B they
are A; for A they are the X/A and A/B pairs with their actual
multiplicities. The gauge Casimirs are C_X=0, C_A=C_B=5, the total
Dynkin index is 10 and its Casimir-weighted sum is 50.

With gamma=gamma1/L+gamma2/L², this gives

    gamma1_X=12h²,
    gamma1_A=h²+(21/10)lambda²-10g²,
    gamma1_B=(21/20)lambda²-10g²,

    gamma2_X=-24h⁴-(252/5)h²lambda²+240g²h²,
    gamma2_A=-13h⁴-(21/5)h²lambda²-(1323/200)lambda⁴
                  +21g²lambda²+50g⁴,
    gamma2_B=-(21/10)h²lambda²-(441/100)lambda⁴
                  +(21/2)g²lambda²+50g⁴.

The corresponding superpotential running is

    beta_h=h(gamma_X+2gamma_A),
    beta_lambda=lambda(gamma_B+2gamma_A),
    beta_f=f gamma_X,
    beta_g=-5g³/L+[150g⁵-g³(10h²+(63/2)lambda²)]/L².

The first two-loop gauge term follows from -6*25+2*5*10+4*50=150.
The Yukawa gauge contraction is 10(Q_A+Q_B)=10h²+(63/2)lambda².

## One-loop scale cancellation

Let D=lambda²+30h², V0=f²lambda²/D, and

    gamma_eff=(lambda² gamma_X+30h² gamma_B)/D.

Exactly under superpotential running, beta·partial ln(V0)=2gamma_eff.
At one-loop order this equals STr(M⁴)/(32pi²V0), using TP01's complete
supertrace. The explicit Q derivative of the one-loop threshold potential
is minus that term. Their cancellation must be checked before RG improvement.

The hypersurface 29lambda²-200g²=0 is not invariant. Running off it is a
necessary part of the matching calculation, not a new force parameter.

## Fields, valley and finite matching

For the original renormalized coordinate, dln X/dt=-gamma_X. On the
re-minimized classical valley T=sqrt(D)X/lambda, direct differentiation
instead gives dln T/dt=-gamma_eff.

The heavy valley amplitude a²=2fh/D has

    dln a/dt=-gamma_A+(lambda²/D)(gamma_X-gamma_B).

Thus evaluating a freshly minimized classical valley at every scale is
not identical to transporting its original A background. Their mismatch
is one-loop in fields and affects matching at the following order.

After minimizing the *quantum* heavy variables at fixed original X, the
reduced Callan–Symanzik operator uses -gamma_X X partial_X. At two-loop
order, its logarithmic terms are fixed by beta2·partial V0 and
(beta1·partial-gamma1_X X partial_X)V1. The finite matching value at Q0
is not fixed by this differential equation. It includes both genuine
two-loop graphs and the heavy one-loop displacement contribution.

Consequently cancellation of scale logarithms, running one-loop thresholds,
and two-loop beta functions must not be reported as the complete finite
two-loop effective action. Pressure additionally needs a consistently
matched matter interaction and kinetic metric.
