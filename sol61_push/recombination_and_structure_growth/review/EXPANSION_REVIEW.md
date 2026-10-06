# Independent expansion-lever review

Primary verdict: **proved as written**, for the weighted-sensitivity identity
and early-ruler bound in the specified approximate flat-GR model. The saved
numerical values agree with an independent reconstruction. No actionable
mathematical error or unsupported precision/identity claim was found. This
verdict does not apply to a solved recombination history, a Planck likelihood,
or any modified-gravity/dynamical-switch action.

## Definitions and parameter variation

Reconstructed from physical densities, rather than using the stored integrals.
At fixed omega_b,omega_c,omega_gamma,omega_r and H100, flatness implies
h^2=omega_r+omega_m+omega_Lambda. Varying omega_Lambda therefore varies H0;
there is no simultaneous fixed-h assumption in the implemented integrals.
The density fractions Omega_i vary accordingly. Physical density means
rho_i,0 in units of 3H100^2/(8piG); this reference is fixed, even though the
actual critical density 3H0^2/(8piG) changes.

With a_star fixed, H=H100 sqrt(F)/a^2. Hence da/(a^2H)=da/(H100 sqrt(F)).
The tightly coupled photon/baryon sound speed is
c/sqrt(3[1+3omega_b a/(4omega_gamma)]), which yields the stated r_s integral.
The comoving radial distance in flat space is the same measure integrated
from a_star to 1 with sound-speed weight replaced by c. Thus D_M and r_s
normalizations are correct. This uses the stipulated idealized sound speed
and fixed integration endpoint, not a calculation of ionization or z_star.

The blackbody mass-equivalent density is
pi^2(k_B T)^4/(15 hbar^3 c^5), not the energy density with c^-3; dividing by
the physical critical-density reference produces the implemented omega_gamma.
The massless-neutrino factor 1+(7/8)(4/11)^(4/3)N_eff is correct for this
explicit model. All baryonic/cold matter is in omega_m=omega_b+omega_c.
Omitting the baseline massive-neutrino interpolation changes the cosmological
model, but the report discloses that omission and makes no precision Planck
reproduction claim. This is internally consistent as an approximate massless
model at the quoted conditional parameter values.

## Independent sensitivity derivation

Let I(v)=integral W(a)/sqrt(F(a,v)) da, with W positive and independent of
v=omega_Lambda. Since F=omega_r+omega_m a+v a^4,

    v I'(v)/I(v) = -1/2 [integral W/sqrt(F) (v a^4/F) da]/I(v).

Differentiation under these integrals is valid for positive densities: F is
bounded away from zero at the acoustic lower endpoint by omega_r>0, while the
late interval is compact. No endpoint derivative appears because z_star is
held fixed. If z_star changes, its boundary term must be restored.

For positive v,matter and radiation,

    f_v'(a) = v a^3 [4omega_r+3omega_m a]/F^2 > 0.

This proves 0<=-dln r_s/dln v<=f_v(a_star)/2 uniformly, independently of a
sample grid. The inequalities are strict at positive v for nonzero integration
range. The corresponding late distance derivative is a weighted average on
[a_star,1], so

    f_v(a_star)/2 <= -dln D_M/dln v <= f_v(1)/2.

It also follows analytically, without the numeric sign check, that

    dln theta_star/dln v
    = (mean_D f_v - mean_s f_v)/2 > 0.

The late support samples larger a than the early support, and f_v is strictly
increasing. At v=0 a logarithmic derivative is not itself defined; the finite
zero-vacuum variant in the script is a well-defined distance/ruler ratio.
No misuse of a logarithmic derivative at zero was found.

## Numeric reconstruction

Used an inline 60-digit mpmath calculation with physical constants independently
entered as decimal strings. Scaled the early integral to t=a/a_star on [0,1]
and evaluated the weighted derivative directly. No root script was imported
or run, and no existing outputs were rewritten. Recovered:

    omega_gamma = 2.4729753332598058652e-5,
    omega_r = 4.1837027335400382208e-5,
    omega_Lambda = .3113251229726645996,
    f_v(a_star) = 1.2751147579336724843e-9,
    r_s = 144.4318261019475740 Mpc,
    D_M = 13894.06430166831669 Mpc,
    dln r_s/dln v = -1.1083141999632513382e-10,
    dln D_M/dln v = -.06644933449444049353,
    dln theta_star/dln v = .06644933438360907354.

These agree with the saved SciPy and mpmath values at their stated numerical
precision. The local H derivative is exactly f_v(a_star)/2 from the Friedmann
equation. The numbers' computational precision does not validate cosmological
accuracy. In particular r_s here is the fixed-last-scattering ruler, not the
baryon-drag ruler, as the report states.

For the early extra-component control, if its density is f_e of the *new*
total with the old densities held fixed, rho_new=rho_old/(1-f_e). The stated
H ratio 1/sqrt(1-f_e), including 1.05409255 at f_e=.1, follows exactly within
GR. This is a local background algebra control, not a specified density history,
ionization solution or bound on an early-dark-energy model.

## Interpretation and remaining gaps

The direct present-constant-vacuum contribution to the expansion at this fixed
epoch is tiny, while the late distance has a substantial lever arm. The
calculation therefore supports the report's separation of local early expansion
from late geometry. It does not establish that recombination is insensitive
to every possible dark-energy excitation or switch stress. A component with a
different rho(a), an interaction, or modified Friedmann dynamics has to be
recomputed. The report explicitly makes this restriction.

Atomic rates, baryon/photon ratio and early expansion belong to a recombination
calculation; this background calculation does not verify those rates or solve
x_e(z). The prose presents them as the physical interpretation and does not
report a new atomic-clock test. Similarly, cold-source microphysical identity
and growth-transfer constraints require the separate same-action perturbation
analysis. The distance sensitivity alone cannot identify a microscopic cold
species or dark-energy mechanism. The stated warning about labeling two roles
as one field is justified as a closure requirement, not an impossibility theorem.

Planck Table 2/section 3.1 source authentication is supplied by the coordinator;
this review does not claim a separate literature authentication or chain run.
The quoted model values are used as conditional illustrative inputs, not as
model-independent measurements. The report's exact bound, finite numerics and
physical interpretation keep these scopes separate.

## Reviewed evidence hashes

    EXPANSION_LEVERS.md: e07b364d793caa7c9b607647ad8ab02e9b32fdf5ac6df9ca8f859e5ae2b63ac6
    expansion_levers.py: 69b2174ac0c3f86d4eb8f42fe2e995dee55409c287fbef66068e90b44b783854
    runs/expansion_a/results.json: 38fdfe06b6436a3aef0dd86cb7ca79ab2a106b0a7b7d86a294d425b7262b8a3d

Review status: exact sensitivity/bounds passed; finite numeric cross-check
passed; parameter-variation consistency passed. Ionization, massive-neutrino
interpolation, likelihood adequacy and modified-action transfer remain outside
this calculation. The next missing implication is the actual common action's
rho(a), stress and perturbation transfer, followed by recombination with its
resulting H(a); no expansion-lever identity supplies that implication.
