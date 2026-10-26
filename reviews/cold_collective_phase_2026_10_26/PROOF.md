# Exact fixed-background pressure obstruction (self-audited)

## Claim and hypotheses

For a canonical real scalar q with |q|<pi, uniform time-independent d>=8,
U=(d-8)z+36z²+40z³+10z⁴, z=sec(q/2)-1, consider classical solutions of
q_tt=lap q-U'(q). Assume averages exist, spatial integrations by parts have
vanishing boundary terms (periodic box or sufficient decay), and the temporal
average of d/dt integral(q q_t) vanishes. Then the integrated/volume-averaged
isotropic effective scalar pressure satisfies

    <P> = <|grad q|²>/3 + <q U'/2-U> >= 0.

Its right side is strictly positive for any nonzero field on a set of positive
space-time measure. This is not a statement about the separately varying matter
stress or a solved modified-gravity stress tensor.

For an isolated configuration add finite energy, sufficient spatial moments,
vanishing surface flux, and vanishing long-time derivative of the stress moment
integral x_i T^{0i}. Under these additional hypotheses there is no nontrivial
stationary self-bound state of this fixed-background scalar in flat space.
This includes interacting/incoherent configurations satisfying the hypotheses;
it is not restricted to a homogeneous oscillator or fluid closure.

## Derivation

Write G=<|grad q|²>, K=<q_t²>/2, V=<U>, J=<q U'>. Multiplication of the field
PDE by q and integration gives 2K=G+J. The canonical spatial stress trace gives
P=K-G/6-V, hence P=G/3+J/2-V.

For q>=0, z(0)=z'(0)=0. Direct differentiation gives

    z'''(q)=sec(q/2) tan(q/2) [6 sec²(q/2)-1]/8 >=0.

Let h=q z'-2z. Then h(0)=h'(0)=0 and h''=q z'''>=0, so q z'>=2z.
Parity extends this inequality to negative q. All coefficients of U(z) are
nonnegative for d>=8. Therefore

    q U'/2-U >= 36z²+80z³+30z⁴ >=0,

strictly for q!=0, including d=8. No quartic truncation has been made.

For the isolated-state statement, translation invariance of this uniform-d
scalar problem gives stress conservation. Integration of its spatial moment
implies <integral T^{ii}>=0 when the time derivative and surface terms vanish.
Thus <integral P>=0. The positive expression above forces q=0 and G=0 almost
everywhere, and the field virial identity then forces K=0. This contradicts any
nontrivial isolated stationary field configuration under those hypotheses.

## Finite-time identity used in the lattice calculation

In local m units s=m t, y=m x, m²=(d-8)/4, the exact diagnostic relation is

    Pbar - Pvir,bar = m² [<q q_s>_b-<q q_s>_a]/[2(b-a)],
    Pvir = m² <|grad_y q|²>/3 + <q U'/2-U>.

The endpoint term cannot be dropped for a short run. In particular the weakest
lattice case has a large relative endpoint correction; its short-window direct
pressure is not an equilibrium EOS measurement. The finite-volume/symmetric
lattice integration-by-parts identity uses its discrete gradient energy.

## Audit and remaining gaps

Primary verdict: **proved as written under the stated hypotheses**, by direct
algebra and integrations by parts. This is a same-author proof audit, not an
independent review. Signs, factors and q=0/d=8 cases were reconstructed from the
PDE and stress definitions. No external theorem or sampled data establishes the
inequality; the numerics check the finite-time identity only.

Self-gravity, expanding geometry, time-dependent baryons, external confining
boundaries, nonuniform source forces, quantum states, noncanonical operators,
and configurations with persistent energy flux are not covered by the isolated
state conclusion. A periodic box is allowed in the pressure identity but is
not an isolated object. Neither positive pressure alone nor this theorem excludes
a gravitationally supported object. No arbitrary-density coupled-theory no-go
is claimed. An oscillating or fragmented phase may exist without being cold or
self-bound.
