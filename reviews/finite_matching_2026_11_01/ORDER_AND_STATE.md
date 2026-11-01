# Order, state and interpretation of the finite matching

This calculation uses the native homogeneous rotating phase, not an imposed
particle gas. Write T=R exp(i theta), keep the original singlet X as the
coordinate, and integrate the normal heavy fields perturbatively. With
q=omega^2 the reduced grand potential through the computed order is

    Omega(X,omega) = V(X) - F(X) q - J(X) q^2/2,
    V = V0 + V1 + V2_diagrams - (CWa^2/Haa + CWb^2/Hbb)/2,
    F = F0 + deltaF_current - CWb F_b/Hbb,
    J = F_b^2/Hbb.

Here CWa,CWb are the one-loop normal tadpoles at fixed X and fixed Q,
Haa,Hbb are the raw-a,b tree Hessians and F_b=60b. The last three heavy
pieces are the expansion of one square, not three independent additions.
All ten vacuum graph classes enter V2_diagrams; no RG-determined log is
added again. The direct one-loop current term is evaluated on the classical
valley. Its change under the one-loop normal displacement is a higher order.

For fixed scaled field X sqrt(e), fixed Q^2/e, f=1 and couplings proportional
to e, denote L=16 pi^2. The exact scaling of the terms is

    tree masses^2 ~ e,       X,b,a ~ e^(-1/2),   F0 ~ e^(-1),
    V1 ~ e^2/L,             V2_reduced ~ e^4/L^2,
    deltaF_current,heavy ~ e/L,                 J ~ e^(-2).

On a finite nonzero-source portion of the rotating branch,
q ~ V1_s/F0 ~ e^3/L. Consequently deltaF q and J q^2 enter at the same
e^4/L^2 order as the finite two-loop vacuum correction. Omitting either
would not match the pressure to that order. An ordinary gapped one-loop
omega^4 coefficient scales as 1/L and contributes e^6/L^3, one order
beyond this calculation. This counting does not assert a uniform expansion
over arbitrary fields, momenta or states. The action is algebraically solved
without re-expanding its response; the extra higher-order terms thereby
generated are not an estimate or bound on the missing terms.

The current calculation retains exact tree supersymmetry-breaking splittings,
Goldstones and gaugino mixing; it is not a small-F Kahler approximation.
The scalar/vector mixing diagram is necessary even though the vector squared
mass is independent of theta. Current UV running is checked against component
Landau anomalous dimensions. Finite current matching does not protect the
global R charge against its gauge anomaly or select its cosmological density.

This is a local low-momentum coefficient and a thermodynamic response on the
specified circular branch. It does not supply the full nonlocal action of
gapless sectors, a confinement contribution, a halo solution or gravity.
The massless-massless phase vertices vanish at this order; no arbitrary IR
mass is inserted into the two-derivative current coefficient. Higher-current
and anomalous infrared dynamics remain separate obligations.

The measured question is whether these particular finite next-order terms
remove the pressure-rich endpoint or the later negative sound speed at weak
trial couplings. Numerical persistence establishes that sampled finite-order
statement. It is not an all-orders no-go, a selected cold species, a lifetime
calculation, or a proof over all branches and occupations.
