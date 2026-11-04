# Small-amplitude action flow

For a common set of comoving number coordinates Y, define
U(x;N,Y)=V(x)+Tc^3 sum_a Y_a E_a(x,N). The mechanical action is
J=(1/2pi) integral p_x dx, with dJ/dE=1/omega and
(dJ/dY_a)_E=−Tc^3 <E_a>/omega. All physical daughter populations are retained.
Each local collision operator obeys sum_a E_a(x) C_a(x)=0. Consequently

    dJ/dtau|collision = Tc^3/omega sum_a cov_phase(E_a,C_a).

The centered finite expression

    Tc^3 sum_{k,a} w_k (E_ka−Ebar_a)(C_ka−Cbar_a)

is algebraically identical to the covariance. It avoids subtracting two
order-one energy terms to extract a term of order amplitude squared.
For a harmonic orbit with amplitude A,

    covariance = Tc^3 A^2/2 sum_a E'_a(xm) C'_a(xm) + o(A^2),
    J = mass_scalar omega A^2/2.

Thus the collision contribution to dlogJ/dtau has a finite small-amplitude
limit. This is an orbit-averaged closure, not a derivation of the full
nonequilibrium quantum field theory. It assumes a common slowly evolving
species distribution over each orbit; direct comparisons test selected
windows and weighted moments, not every microscopic soft occupation.

The energy-based warm integrator preserves the energy variable during each
finite population step. At very small J, a finite shift of the well minimum
can create a spurious mechanical excitation of order (delta Y)^2. Its
adaptive action-linearization condition then forces vanishingly small time
steps. This is a numerical representation limit, not evidence of a physical
stall or loss of the vacuum.

`action_averaged.py` instead advances logJ with centered covariance, adds
−3 to dlogJ/dN for expansion, and reconstructs the orbit from J and Y. It
integrates 3<kin2+rho+P> independently for the expansion work. The resulting
energy-plus-work residual is an independent check; it does not telescope
from the reconstructed energy change. Collision stepping is implicit and
keeps explicit fermion vacancy coordinates. Predictor/corrector checks on
logJ and entropy/bounds are recorded. The population update remains a
first-order frozen-orbit step, so step refinement is required.

The initial test deliberately retains the old two-point global angular
quadrature. That quadrature has failed a material refinement check in the
warm crossing window. Its long trajectory is conditional numerical evidence
only. The segmented angular calculation must replace it before a continuum
or physical abundance claim. No late four-state memory, loop decays,
2-to-2 channels, bound states, or complete cosmic production history is
included in these warm action runs.
