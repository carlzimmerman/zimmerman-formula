# IC39: constructive finite-order activation variant

Base c23c1d7ec34f32b1c982648a27ae25ce88243115 and frozen IC37/38 evidence.
Full gravity target OPEN. Carl Zimmerman's exponential MOND law, vacuum-scale
proposal and primordial-clock direction motivate this variant. No empirical
fit, novelty claim, or derivation of the factor one half.

## Bounded plan and explicit action change

Retain the IC29/30 action and fixed repaired coefficient. Change ONLY its
auxiliary pin activation, not mu(y). Define x=alpha^2-1/2, b=1/4 and

    eta4(x)=0                              x<=0,
            x^4/[x^4+(b-x)^4]              0<x<b,
            1                              x>=b.

In the radial action's sign convention replace

    J exp(S) ell (w-wc) eta_old(alpha)

by the identical expression with eta4. Equivalently add the difference of
these two pin potentials to the same parent phase action, with the same scalar
alpha=-exp(-3w)q/(3 m h0). No matter coupling, tensor kinetic term, or MOND
constitutive primitive is changed. This is a NEW variant, not a claim that
IC37's old action passed. Every transition-sensitive requirement must be
rechecked for this variant.

1. Test the endpoint limits and derivatives, monotonicity, the varied pin
   potential and a manufactured quartic source, including lower-order leakage.
2. Derive the finite-response limit symbolically; consume the actual frozen
   IC37 joint-selection values without fitting new action coefficients.
3. Record the differentiability loss as a cost, not a hidden pass. Run the
   script and tests with input provenance. No claim of full time evolution.

## Exact conditional finite-response result

On the active side retain IC37's w=wc, ell=ell_t=0. Variation of the new
potential gives the same differentiated equation with eta replaced:

    E + eta4 exp(S) L=0, E=W_tt, L=ell_tt.

Let delta=r-r0, x=a delta+o(delta), a>0, and S->S0. If the data satisfy
E(r0)=E_r(r0)=E_rr(r0)=E_rrr(r0)=0 EXACTLY and admit
E=E4 delta^4/24+o(delta^4), then

    lim L = -E4 b^4/[24 exp(S0) a^4].

Thus the finite quartic source that defeats the old exponential activation
does not by itself defeat this variant. A residual constant, linear, quadratic
or cubic term still diverges after division by eta4. Numerically small root
residuals are NOT exact zero: the numerical IC37 roots need an existence/error
certificate before asserting a bounded exact field solution.

eta4 is C3 across both plateau joins, but not C4: its fourth one-sided
derivative differs from that on the constant plateau. This suffices for the
displayed conditional second-time calculation, not for all subsequent Dirac
preservations, nonlinear well-posedness or perturbative strong-coupling claims.
The numerical selector never divides its tiny residual by eta4 and calls it
finite. It reports the conditional limit plus the unresolved lower-order jets.

## Next unavoidable gates

First certify exact initial profiles satisfying the four zero-jet conditions,
and solve the inactive side with its unpinned w response rather than keeping
w=wc there by fiat. Then preserve constraints through the next time order
using eta4's actual derivatives and audit the rank-changing surface. A bounded
ell_tt is only one necessary gate. Full functional Dirac closure, healthy
separately counted clock, tensor light cone, PPN, k=0/y=0 control, global
cosmology/galaxy matching, and empirical CMB/galaxy/binary/cluster tests remain
unproved. No favorable result from the old transition is imported as proof.

## Concurrent Claude/Fable input, checked before adoption

Commits b349cb0f35c92a23b90082c1155e86716e5105ca and
01c2a05144640d1d96b2b9d0170072a4061688c6 add L44 and its handoff.
`fable_independent_2026/L44_COLLAR.md` section 5 independently proposes a
finite-order activation exit; credit that parallel contribution. L44 locates
the earlier transition-ghost escape at IC20's auxiliary Schur complement,
not at the subsequent finite-multiplier calculation. This is consistent with
the preserved IC20/30 action and the distinction maintained in IC36/37.

The IC39 script differentiates its actual new pin potential before setting
w=wc and independently computes

    a_UV=t/6+(h_qq-h_qz^2/h_zz)/2=A^2/(4D+24E4 z^2).

For D>0, E4>=0 and A!=0 this is positive. It is a particular pinned reduced
coefficient, not a proof that the entire constrained scalar sector is healthy.
In particular mixed derivatives involving w and the multiplier must not be
discarded in a full constraint analysis. The new switch remains OUT of this
q/z Schur coefficient, rather than being moved onto the kinetic energy.

The L44 pass count is not 76 proof certificates: D3 includes `or True`, F6
checks supplied count arithmetic/documentary text, and several other entries
are substring or bounded sampling checks. Its independently derived D4/D5 and
Schur algebra, corroborated here, are the useful evidence. Its suggested
superluminal-clock direction is not adopted as permission to relax the user's
causality requirement. Its proposed fourth-mode diagnosis is also not accepted
as a substitute for the missing functional Dirac analysis.
