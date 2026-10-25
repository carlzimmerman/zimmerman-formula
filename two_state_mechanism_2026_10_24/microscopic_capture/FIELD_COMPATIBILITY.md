# Can a second simple mediator repair the atomic candidate?

This follow-up is an analytic check, not part of the numerical rate manifest.
It narrows two simple microscopic routes under explicit assumptions. It does
not exclude collective media, extra charge carriers, broken gauge symmetries,
nonlocal theories or all possible completions.

## Binding gauge field

For the chosen unbroken U(1), Q_A=Q_X+Q_C=0 exactly. A photon carries no U(1)
charge. Neutral bound atoms therefore cannot acquire the mass-proportional
monopole charge required of T. More generally a neutral F plus a neutral anchor
cannot turn into a charged T plus only neutral radiation under an unbroken
gauge symmetry. Extra oppositely charged products or a charged anchor would
change the particle inventory and field sources and must be tracked explicitly.

## A canonical scalar with state-dependent masses

A scalar can evade gauge-charge conservation because its effective source is a
mass derivative, not a conserved U(1) charge. For a slowly varying scalar phi,

    M_A(phi)=mX(phi)+mC(phi)-B(phi), q_A=dM_A/dphi.

If the constituent masses are phi-independent at tree level but alpha_D varies,
then q_A=-2B*d(log alpha_D)/dphi. This ties the new coupling to the binding-energy
derivative. It does not fix d(log alpha_D)/dphi, and loop-induced constituent
couplings require checking. It provides a possible state-sensitive scalar
source, not the required repulsive force.

For a healthy canonical scalar with real nonderivative charges q_i, its static
energy in natural units is

    E[phi]=1/2 integral [(grad phi)^2+m_phi² phi²] d³x
            + integral rho_q phi d³x.

Writing L=-Laplacian+m_phi², minimization gives phi=-L^-1 rho_q. Therefore

    E_on_shell=-1/2 integral rho_q L^-1 rho_q,
    V_ij=-q_i q_j exp(-m_phi*r)/(4pi*r).

Identical scalar charges attract. The result includes the source interaction;
retaining only the positive scalar field energy would reverse this conclusion
incorrectly. The current tether functional instead has the positive quadratic
cross energy +G*m_i*m_j/r in its point-source, weak-field limit, hence a
repulsive T-T contribution. Changing the sign of a healthy scalar charge for
every T does not help because q_i*q_j is unchanged.

The scalar calculation is an explicit derivation. For standard exchange-force
background see David Tong's original QFT notes, sections on scalar Yukawa
scattering and QED:
https://www.damtp.cam.ac.uk/user/tong/qft/qft.pdf
https://www.damtp.cam.ac.uk/user/tong/qft/six.pdf

## What actually remains open

Neither the neutral atomic gauge field nor a single canonical scalar with
identical state charges reproduces the current weak-field tether force. The
simple scalar has the desired freedom to change effective charge, but the wrong
force sign. The gauge field gives repulsion for like charges, but requires a
conserved charge inventory that the present two-state conversion does not have.

A next microscopic proposal must specify that inventory or a collective field
action before a new formation-rate calculation. It must derive both the field
energy and its source coupling together; reproducing only a positive field-energy
integral is insufficient. This is a more restrictive next step than fitting
another binding energy, restitution coefficient or galaxy-dependent threshold.

Self-review verdict: correct under the listed weak-field, canonical, real-charge,
static assumptions. A general no-go for all state-dependent interactions is not
claimed. No independent review has been performed.
