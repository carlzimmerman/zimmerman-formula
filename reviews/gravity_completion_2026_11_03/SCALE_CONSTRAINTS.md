# Structural constraints shared by gravity and production

The raw-source and tuned-net-vacuum questions are independent obligations.
This derivation applies to the equal-coupling finite weak branch of TP01--05,
not an arbitrary SUSY-breaking model or an added mass source.

## A quantitative lower bound on the required vacuum cancellation

For a two-spin-state fermion with occupation at most one and momenta bounded
by p<=m v_max, counting states gives

    rho <= g m^4 v_max^3/(6 pi²), g=2.

No thermal distribution is assumed. This is a compact-support phase-space
bound for the specified benchmark, not an observational halo likelihood.
At the rigid CW minimum m_chi=C mu e^(5/2), C is the actual TP04 leading pole
coefficient. Thus, with e<=e_max and that mass source,

    V_raw=mu^4/31 >= [m_Pauli/(C e_max^(5/2))]^4/31.

This supplies a lower bound on the raw-energy/DE ratio for even a maximally
occupied fermion halo. It strengthens the earlier single1MeV example to a
necessary cancellation bound at the inherited minimum. Different background
threshold coefficients must be substituted before applying it elsewhere.
Production cannot evade this count by choosing a nonthermal distribution.
Additional forces, interactions or a different mass-generating sector change
the premise and require their own calculation.

## Gravity-branch scaling and the production/lifetime tradeoff

At fixed t on the leading tuned-W0 branch, away from a moving threshold,

    mu ~ e^(5/2), R ~ e², m_sigma,m_a ~ e^4, m_chi ~ e^5,
    F ~ e^5, Gamma_chi->Ggamma ~ m_chi^5/F² ~ e^15.

The intrinsic scalar/phase fermion-pair width scales as
m_chi² m_parent/R² ~ e^10 with its actual threshold function retained.
For radiation-dominated decay a_d~Gamma^(-1/2)~e^-5 and relativistic daughter
momentum-to-mass at injection ~e^-1, so q/m~e^-6. Larger e can cool a decay
population while shortening the candidate lifetime. This is a scaling
discriminator, not a global exclusion: threshold factors, competing channels,
backreaction and finite corrections must be evaluated by the production lane.

For a single scalar pair channel with r=m_parent/(2m_chi)>1 and beta=sqrt(1-r^-2),
Gamma~m_parent beta³ at fixed daughter coupling. Redshifted momentum in RD
is proportional to p/sqrt(Gamma)~sqrt(r)/sqrt(beta). Its minimum is at
r=sqrt2, and it increases as r approaches1. The threshold can therefore
delay decay enough to undo the small injection momentum. Other open channels
change this result; in particular lighter nonabelian companions must remain.

## Vacuum sensitivity

At leading canonical cancellation V_net=F²-3W0²/Mp²,

    dV_net/dlnW0=-6W0²/Mp²,
    |delta W0|/|W0| ~ rho_DE/[2(F²-rho_DE)].

An exact high-precision root enforces this chosen cancellation only in its
truncated potential. Finite omitted terms exceed rho_DE by enormous factors
and require retuning. A successful stationary solve does not make the tiny
residual radiatively predicted or protected.
