# Pointwise photon decoupling and a hard-band discriminator

Analytical continuation written after run_001. It is not a frozen input or
a claim of additional numerical execution. It sharpens the endpoint
obligation of DERIVATION.md without changing its formulas or run.

## Pointwise coordinate reconstruction is exact away from coincidence

For r>0,

    D_s(r)=integral_0^infinity d tau (4 pi tau)^(-2)
                      exp[-r^2/(4tau)-s tau].

The coordinate kernel corresponding to h_n is

    K_n(s,r)=(-1)^n s^(n-1) partial_s^n D_s(r)/(n-1)!.

In the Schwinger representation its integrand is nonnegative. Tonelli and
the elementary gamma integral give, for every positive integer n,

    integral_0^infinity ds K_n(s,r)
      =integral_0^infinity d tau (4 pi tau)^(-2) exp[-r^2/(4tau)]
      =D_0(r)=1/(4 pi^2 r^2).                             (C1)

Explicitly,

    K_1(s,r)=K0(sqrt(s)r)/(8 pi^2),
    K_3(s,r)=s r^2 K2(sqrt(s)r)/(64 pi^2).                (C2)

Thus the all-scale coordinate kernel itself has no missing normalization.
Its pointwise endpoint `D_s(r)->0` as s->infinity is valid for r>0.
Applying (C1) to a singular coincident-current product is a separate
operation: the product requires an extension/contact prescription at r=0.
No dominating integrable bound for that renormalized product is supplied
by pointwise photon decay. The explicit fixed-MSbar Dirac function is a
counterexample to the inference that pointwise decay forces the integrated
renormalized response to zero. Its large-s logarithm and threshold are the
local mass matching just calculated. In a fully specified canonical theory
this contact is calculable; its value is not an independently adjustable
new physical interaction. A decoupling prescription that absorbs it into
the low-energy mass parameter specifies a different matching trajectory.

## Even a known leading endpoint does not replace the missing middle scales

Consider the admissible integral fixture

    delta g(t)=(c/T) 1_(T<t<2T),  T>0,
    delta f(s)=c[1-(s/T)log((2T+s)/(T+s))].                (C3)

This is not asserted to be a realizable QCD tensor or a new EFT coupling.
It tests exactly the information content of a reconstruction from only a
soft filter and leading UV endpoint. It obeys

    delta f(0)=c,
    delta f(s)=c[1-(s/T)log2+s^2/(2T^2)+O(s^3/T^3)] at zero,
    delta f(s)=3cT/(2s)+O(T^2/s^2) at infinity.           (C4)

It changes neither any infrared nonanalytic coefficient selected by the
FSP-009 filters nor the leading UV logarithm or finite B. Yet (3) of the
main derivation gives

    integral_0^infinity ds delta h_n(s)
      =integral_T^(2T) dt delta g(t)=c.                   (C5)

Fubini is justified by compact t-support for c>=0 and by absolute
integrability for either sign. The hard-band contribution is therefore
fully visible to actual all-mass derivative data, while being invisible
to the stated endpoint information. It must be measured/calculated, not
chosen to recover a preferred number. Higher power OPE coefficients could
detect (C3); they are additional inputs, not part of the leading endpoint
premises. The fixture refutes only endpoint-only reconstruction in this
explicit function class, not microscopic QCD or all dispersive approaches.

The state-dependent Ward gap is similarly precise: the trace equation
fixes one row of a matrix-element vector, whereas electric-charge weights
select a different row. In the mass-matching sector, the trace-preserving
variation described in the main derivation changes the finite leading
quark endpoint by `delta B=5 d/(96 pi^2 M)` and its log coefficient by
`delta a=d/(16 pi^2 M)`. No actual proton sigma-term variation is inferred.
