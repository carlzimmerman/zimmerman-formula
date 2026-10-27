# Bounded internal-state variant

The polynomial state map was only admissible for x in [0,1]. With nonlocal
mobility from gradient damping, even a stable relaxation can slightly cross
that coordinate interval. The f=.99 massive-galaxy case reproducibly reached
x=1.00000101 and was rejected; do not dismiss it by relaxing the tolerance.

Introduce an actual mixing angle theta=pi*x/2:

    q_T=sin^2(theta), q_F=cos^2(theta),
    s(x)=sin^2(pi*x)/pi^2 = 4 q_T q_F/pi^2.

State probabilities are nonnegative and sum to one for every real x. This is
a new, explicitly disclosed potential ansatz, not merely a numerical fix.
There is no clamping. The small-displacement barrier curvature remains 2 at
either endpoint, whereas h''(1) changes from -6 to -pi^2/2. Re-derive and test
that curvature; retain beta=20, ell=30 kpc, all profiles, all streaming values,
the same drag, seeds, duration and acceptance criteria without retuning.

An angle is a natural parameterization of two internal amplitudes; this alone
does not identify particles or derive the interaction from a microscopic
Hamiltonian. The calculation remains a classical effective order-parameter
model with an assumed dissipative receiver.

Run N=64/128/256. Validate the field-energy derivative, Hessian, domain,
conservation, endpoint forces, label independence and counterfactual failures
anew. The earlier polynomial runs remain evidence for that earlier variant,
not for this one. Thermal lifetimes and absolute physical times remain open.
