# Candidate: the diffuse singular equations retain acoustic freedom

Use the compact on-branch PF13 weak class and PF14's no-jump neighborhood.
Let p_a=partial_a phi be spacetime BV, with its jump part zero. Auxiliary fields
A,Pi are Lipschitz and the metric is C1 intersect W2,1. Write D^c for the Cantor
part of the derivative, and use the approximate representatives of BV fields.
All formulas below concern measure identities, not pointwise second derivatives.

At a diffuse singular point, derivatives of the metric, A,Pi, explicit potential
and volume density have no Cantor part. Freeze their values in the constitutive
chain rule. With k^a=h n^a (density E stripped off), the exact algebra gives

    partial H/partial p_a=k^a,
    T^a_b=H delta^a_b-k^a p_b.

The BV chain/product rules on the Cantor part consequently yield

    D^c_a T^a_b
      =-p_b D^c_a k^a+k^a(D^c_b p_a-D^c_a p_b).

The scalar equation has bounded source, so D^c_a k^a=0. Clock compatibility
makes D^c_b p_a-D^c_a p_b=0. Hence the Cantor part of stress divergence vanishes
without adding an independent restriction. This differs from a finite jump,
where the finite nonlinear flux differences produce the earlier obstruction.
No differentiation of an arbitrary singular product is being assigned: these
are the canonical diffuse BV chain rules at approximate values.

For the acoustic state U=(m,phi_x) used in PF13, with the common auxiliary and
metric coefficients frozen in the diffuse chain rule, the singular equation is

    D_t^c U+DF(U) D_x^c U=0.

Writing l_i for smooth left eigenvectors in the compact hyperbolic neighborhood,

    l_i D_t^c U+lambda_i l_i D_x^c U=0.

Thus any surviving Cantor component must obey the acoustic transport relation.
This is a necessary relation between measures, not a theorem that such a
component exists, can be created from smooth data, or is uniquely transported.
In particular it is not an assertion of a global characteristic flow for BV
coefficients. No rank-one theorem is needed for the displayed projections.

## Consequence for the attempted exclusion

Einstein stress conservation supplies the decisive extra nonlinear condition at
jumps, but its diffuse principal identity is redundant with scalar evolution
and clock compatibility. It therefore does not remove Cantor variation by the
same algebraic argument. The full Einstein equations still constrain metric
and absolutely continuous parts; their redundancy is not asserted globally.

A dynamical regularity or transport theorem is required to prove that the
incoming zero-Cantor data remain zero-Cantor, or to construct a permitted
singular part. The identity alone settles neither existence nor uniqueness
and provides no evidence that an extension is unavoidable.
