# The current scale identity after eliminating the heavy fields

The component current graph alone runs with Landau component anomalous
dimensions. The reduced current in the original singlet X chart must instead
include the normal heavy displacement. Write L=16 pi^2 and b=hX/lambda.

    F0=X^2+30b^2,
    D1_reduced=beta1 partial_c - gammaX X partial_X,
    D1_reduced F0=-2gammaX X^2-60gammaB_chiral b^2.

The one-loop graph identity is

    partial_lnQ deltaF_current
       =2gammaX X^2+60gammaB_component b^2.

These are consistent because the heavy pullback is

    deltaF_heavy=-CWb F_b/Hbb,       F_b=60b,
    partial_lnQ deltaF_heavy=-300g^2 b^2/L
       =60(gammaB_chiral-gammaB_component)b^2.

Thus partial_lnQ(deltaF_current+deltaF_heavy)+D1_reduced F0=0.
The normal tadpole is differentiated at fixed raw a,b,X,Q and the pullback
is applied once. Replacing component gamma with chiral gamma in the graph,
or dropping the pullback, would break this identity. Both use the same
singlet gammaX. No finite field renormalization is adjusted to enforce it.

This algebra follows from the off-valley component potential CS equation
differentiated in b, the tree Hbb, and the source-checked component/chiral
gamma difference. The bounded numerical check uses independent full mass
matrix tadpoles and the finite current graph at three Q values. It is a
one-loop current consistency check, not a calculation of the full radial
kinetic coefficient or a bound on higher-order response.
