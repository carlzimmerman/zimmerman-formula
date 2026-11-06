# Shared baryon/phase/particle interaction test

Base: 9144e8bc0a. Scope: only action_scale_investigation_2026_11_05.
Target: derive material inventory and phase stress together, and test whether
a0=c sqrt(G rho_DE)/2 follows without a target-calibrated parameter.

Use an illustrative canonical two-real-scalar effective theory in c=hbar=1:
V_sigma=V0+ms^2 sigma^2/2+lambda sigma^4/4,
A(sigma)=1-alpha sigma^2/2 for nonrelativistic baryon rest masses,
m_chi^2(sigma)=m0^2+g^2 sigma^2. Positive ms^2, lambda, alpha, m0^2, g^2.
Use only A>0 and weak mass shifts when making weak-force approximations.
Treat homogeneous baryons as a fixed density for the local minimum, then
vary the conserved baryon density correctly for pressure. Derive sigma's
baryon-triggered minimum, bare scalar energy versus combined energy, pressure,
and fifth force. Include finite-size gradient threshold for a top-hat source.

Quantized chi modes experience a time-varying mass when the phase develops.
Derive sudden-quench Bogoliubov production from oscillator matching, compare
with the adiabatic limit for the same endpoint phases, and retain finite mode
range/transition time. Test exact identities symbolically. No artificial UV
cutoff is a physical abundance prediction. Include backreaction explicitly
as an unresolved dependency if produced energy is appreciable.

Discriminators: same final density/phase with different formation histories
refutes endpoint-only abundance selection in this construction. Vacuum offset
V0 leaves local flat-background phase and production equations unchanged, so
no local identity ties their normalization to rho_DE=V0. This is not a no-go
theorem for fully coupled cosmological evolution or every possible interaction.

Validation: exact SymPy identities, finite mode illustrative fixtures with
omega_i=1 and omega_f=2 (not galaxy inputs), 60 seconds, one thread. Negative
control changes the sign of beta in oscillator derivative matching and must
fail that matching check. No 1/2 target used to set physical parameters. No
claim that a static condensate is cold matter, or that an instantaneous
quench yields a finite integrated energy in the continuum.

Pre-execution extension: compare smooth tanh omega(t)^2 transitions from 1
to 4 at tau=0.05,0.5,5. Integrate each oscillator on [-12 tau,12 tau] with
DOP853 rtol 1e-9 and 1e-11, atol=rtol/100, max_step=min(tau/20,0.1).
Require Wronskian error below 1e-7, occupation agreement below 1e-7 absolute,
and a smaller occupation at the slowest than the fastest transition. These
six solves test finite mode history dependence, not an integrated halo yield.
