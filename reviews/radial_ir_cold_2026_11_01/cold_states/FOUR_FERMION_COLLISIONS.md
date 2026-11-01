# Final named leading collision classes: four fermions and light exchange

This is the authorized final bounded collision continuation. Contracts and
all preceding evidence stay frozen. The scope is the same leading weak
rigid EFT and conditional1MeV,e=.003 local state. No finite-temperature
average, production calculation, new exact box sum or all-order kinetic
claim is introduced. The hard gap and bundle are those independently
reviewed in gapless_charge/decay_bound/DERIVATION.md. A scalar evaluation
checks the bounds below with one thread,30s wall/25s CPU, RSS<1GB.

## Heavy one-loop four-fermion contact

Every external photino, Goldstino and unbroken gaugino is neutral under
the residual U1. A photino insertion starts a charged heavy cycle and
each further insertion preserves that nonzero charge. In Feynman xi=1
the entire cycle therefore has the same strictly positive common charged
gap M. This is not a bound on a light radial or Goldstino propagator.

Four external fermions enter as four boson-to-fermion insertions in the
quadratic heavy bundle. A one-loop word has two boson and two fermion
resolvents. Its norm is bounded by r^(-6), r²=kE²+M², and

    integral d4k/(2pi)^4 r^(-6)=1/[2(16pi²)M²].

There are at most4!=24 ordered words; overcount by64. The original
real/vector/four-component bundle trace bound512 and continuation factor2
apply. There is no renormalizable four-fermion seagull in the canonical
action. These diagrams are UV convergent by the displayed absolute bound.

For any normalized chiral external source the superpotential Yukawa
Frobenius eigenvalues are24e² for X,6.2e² for A and2.1e² for B.
Thus24e² bounds the normalized Goldstino projection. Scalar/gaugino
Yukawa contributions add at most10g² and the four Lorentz components of
the vector current add at most20g². The pure unbroken external gaugino
has the smaller total40g². A deliberately excessive real/four-component
embedding envelope, covering either type, is

    Ymax=32 sqrt(24e²+30g²).

Unitary mass rotations preserve these norms; no small-F expansion or
inverse mass enters at a vertex. The corresponding local amputated
four-fermion coefficient norm is bounded by

    C6 <= 32768 Ymax^4 /[(16pi²) M²].

Four normalized external spinors have norm product at most4m² at NR
threshold. For chi chi -> GG the four final spin choices, initial spin
average and identical-final factor give sigma v<=C6²m²/pi. Overcount
all13 light Weyl/Majorana labels in each final slot and drop the
identical suppression: the inclusive bound

    sigma v (all light fermion pairs) <=338 C6²m²/pi

is safe. It includes gauge-forbidden and elastic channels, so it is also
an upper bound on the number-loss subset. This is a finite norm majorant,
not a matched signed Wilson coefficient.

## Separate light exchanges

These exchanges have light denominators and must not be assigned the
charged gap. Use a=sqrt2v, y_pi_i=m_i/a and
y_sigma_chi=kappa_s m/a. All open final unbroken gauginos satisfy m_i<=m.

For s-channel phase exchange into gaugino pairs the two external
pseudoscalar bilinears are each bounded by2m, and s=4m². Each amplitude
is at most m²/a². Radial exchange into these pairs is smaller by at most
4|kappa_s kappa_i|m²/(mrad²-4m²); the measured slopes have magnitude<1
and mrad/m about499. The phase-pair t/u/contact bound is separately in
SOFT_COMPLETION.md. Summing all13² final labels/spins is still safely
covered, at this point, by

    sigma v (phase and light-gaugino-pair channels)
        <=100 m²/(pi a^4).

The Goldstino has no canonical mass-phase Yukawa. Its radial coupling
instead follows the actual Goldstino low-energy theorem:
y_sigma_GG=mrad²/(sqrt2 Ftot). Together with the measured scalar
source y_sigma_chi this gives an uncanceled scalar-exchange amplitude
bound2sqrt2|kappa_s| m³/[a Ftot(1-4m²/mrad²)]. Even without using
possible SUSY contact cancellations, its cross section is safely below

    sigma v (radial -> GG) <=100 kappa_s² m^4/(pi a² Ftot²).

The two-Ward-vertex photon/Goldstino exchange diagrams chi chi -> gamma
gamma and chi chi -> GG have t=u=-m² at threshold. Using commutator
norm<=4m, internal massless-fermion norm<=1/m, and the crossed transverse
photon Ward identity gives the inclusive loose envelope

    sigma v (two Ward vertices) <=512 m^6/(pi Ftot^4).

It exceeds the direct norm/flux estimates for both named channels.
It is not a claim that every Goldstino-pair amplitude is this small;
the distinct heavy contact and radial exchange are included separately
above. All these are zero-temperature NR threshold envelopes.

## Coverage and interpretation

The leading open two-body annihilation final states in this retained
model are phase pairs, unbroken-vector pairs and light-fermion pairs.
The heavy one-loop2fermion2vector bundle, heavy one-loop4fermion bundle,
and the separate light phase/radial/Ward exchange classes cover them.
Scalar radial production is closed; one photon plus phase is C-forbidden;
a single colored object is not a gauge-invariant final state. Inclusive
counts above deliberately include additional forbidden labels.
Higher loops, extra final particles, finite-temperature scattering,
nonperturbative effects and gravity/UV interactions are not promoted to
computed rates. Each bound is evaluated at the stated local density;
the calculation does not provide the initial FD distribution.

The numerical result is in run_four_fermion/result.json. The leading
collision-loss upper bound can be compared with the retained decay width
without identifying the residual photon with observed EM or choosing
any production/thermal history. Fresh independent proof review is
required in addition to successful scalar arithmetic.
