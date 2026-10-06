# Acoustic memory, baryon catch-up and what growth identifies

This lane derives two diagnostics. **After photon drag and gas pressure become
negligible, the baryon/cold relative velocity obeys an exact gravity-cancelling
invariant.** The common growing mode retains both the baryon density and its
velocity at drag, even when baryons later catch up with the cold density.
Separately, a constant-pressure dark fluid is exactly equivalent to dust plus
a cosmological constant at the stress-tensor level before dust caustics. These
results constrain a unified action, but do not select particle identity or
derive the cold abundance from the vacuum value.

Checkpoint: `RECOMB_RELATIVE_MEMORY_AFFINE_DARK_20261005`. Observed run HEAD:
`3b06b67c4ed9180a3b7dc6692f3daf64f9625986`; checkout was dirty. Version-2
manifests pin actual source hashes before/after execution. Writes are confined
to `growth_and_identity/`; no commits, other-lane edits or new Boltzmann runs.
The computation takes about half a second. This is a derivation/self-review
checkpoint, not a CMB likelihood analysis or a complete cosmological action.

## 1. Why the coupled baryons oscillate while a cold mode can seed growth

Use conformal Newtonian gauge, conformal time tau, Hcal=a'/a, and Fourier
velocity divergence theta. The source conventions and species equations were
checked in [Ma and Bertschinger, astro-ph/9506072v1, 11 June
1995](https://arxiv.org/pdf/astro-ph/9506072), equations (43), (64), (67), (70).
Our baryon loading Rb=3rho_b/(4rho_gamma) is the inverse of their section-5.7 R.
The equations below are derived in our conventions; we retain c=1.

In the tight-coupling, negligible-shear and negligible gas-pressure limit,
theta_b=theta_gamma=theta and

    delta_gamma' = -(4/3)theta+4Phi',
    theta' = -Hcal Rb/(1+Rb) theta
             + k² delta_gamma/[4(1+Rb)] + k²Psi.

Combining them gives

    delta_gamma'' + Hcal Rb/(1+Rb) delta_gamma'
       + k² delta_gamma/[3(1+Rb)]
       = 4Phi'' + 4Hcal Rb/(1+Rb)Phi' -(4/3)k²Psi.                (1)

Thus the pressure term supplies a positive acoustic frequency. For constant
potentials and approximately constant loading over one oscillation, the
equilibrium is delta_gamma,eq=-4(1+Rb)Psi and the perturbation about it
oscillates. Recombination reduces photon scattering/drag; it removes that
large pressure coupling from baryonic bulk motion. It does not create a
pressureless gravitating seed by itself. Photon last scattering, baryon drag
release and thermal decoupling are distinct events; this lane's a_d is a
chosen **drag-free starting surface**, not an atomic recombination calculation.

For a pressureless mode on subhorizon scales, continuity plus Euler and
Poisson instead give

    delta_i,NN + [2+dlnH/dln a]delta_i,N = (3/2)Omega_m delta_m,
    N=ln a, delta_m=f_c delta_c+f_b delta_b.                       (2)

There is no acoustic restoring term. In radiation domination with negligible
self-gravity, dlnH/dln a=-2, so delta_c=A+B ln a: growth is only logarithmic.
In matter domination once all source matter clusters, the growing mode is
delta_m proportional to a. Its Poisson potential is proportional to
a²rho_m delta_m, hence constant; the decaying contribution falls as a^-5/2.
This explains potential persistence **in the matter era**, not an assertion
that every potential is constant throughout radiation domination.

If a fraction f_c clusters and pressure-supported baryons average nearly
smooth in an EdS background, delta_c proportional to a^p with

    p=[sqrt(1+24f_c)-1]/4.

The cold contribution to the potential then scales as a^(p-1), a slow decline
when f_c is large. This is a controlled smooth-baryon approximation, not the
full acoustic transfer function. Oscillatory baryon forcing, radiation,
neutrino stress and equality require the full equations for precision.

## 2. Exact relative-mode null test, independent of gravitational source

After pressure and drag vanish, the **linear GR** species equations are

    delta_i'=-theta_i+3Phi',
    theta_i'=-Hcal theta_i+k²Psi,

for both baryons and cold matter. Subtract them, putting Delta=delta_b-delta_c:

    Delta'=-Delta_theta,
    Delta_theta'+Hcal Delta_theta=0,
    Delta''+Hcal Delta'=0.

Consequently, in cosmic time t,

    U=a² dDelta/dt = a²H dDelta/dln a = constant,                 (3)
    Delta(a)=Delta_d + U_d integral_a_d^a da'/(a'^3 H(a')).       (4)

Unlike (2), this relative identity does not require a subhorizon Poisson
approximation or a matter-only background. Metric sources cancel directly;
it holds for arbitrary common linear metric perturbations and expansion
history while both fluids are pressureless, drag-free and feel the same force.
Delta is gauge invariant when both background species have w=0 because their
linear gauge shifts are identical. The shared-force premise is substantive.

This is a useful **null diagnostic for a proposed unified action**: matching
H(a) and total growing matter alone is insufficient if baryons and the cold
field have different accelerations. With common continuity equations but
effective Euler potentials Psi_b and Psi_c, baryon pressure cb² and cold
pressure cc², the invariant acquires

    dU/dt = -k²(Psi_b-Psi_c)
             -cb²k²delta_b+cc²k²delta_c
             -Gamma_b(theta_gamma-theta_b),                    (5)

where Gamma_b=(4rho_gamma/3rho_b)a n_e sigma_T is the conformal drag
coefficient. All terms follow by subtracting Euler equations before changing
time coordinate. Changes to the continuity equations require additional
terms and are outside this formula. Equation (5) prevents silently borrowing
the cold/baryon catch-up relation from a different action.

For an explicitly massive nonrelativistic wave, linearizing the Schrödinger
quantum-pressure term gives

    cc² = hbar² k²/(4m²a²),
    cold contribution to dU/dt = hbar² k^4 delta_c/(4m²a²).

This k^4 departure is a conditional scale-dependent diagnostic of that
realization, not a unique inference of it from growth. It applies in its
subhorizon nonrelativistic regime, not as an exact all-scale relativistic
extension of (3). The wave mass remains an input. FL1's unequal forces in
MOND-active regions would instead contribute Psi_b-Psi_c; cosmological OFF
behavior must be verified in the same action before setting it to zero.

## 3. Exact four-mode transfer after drag: catch-up retains acoustic memory

Now restrict (2) to EdS, common pressureless gravity and constant mass
fractions 0<f_b<1, f_c=1-f_b. Let x=a/a_d, and initial data be

    u=delta_m,d, v=delta_m,N,d,
    w=Delta_d, z=Delta_N,d.

Solving the common and relative equations gives

    A=(3u+2v)/5, B=2(u-v)/5,
    delta_m=A x+B x^-3/2,
    Delta=w+2z(1-x^-1/2),
    delta_b=delta_m+f_c Delta,
    delta_c=delta_m-f_b Delta.                                  (6)

The transfer matrix in state (delta_m,delta_m,N,Delta,Delta_N) is

    T_common = (1/5)[[3x+2x^-3/2, 2x-2x^-3/2],
                     [3x-3x^-3/2, 2x+3x^-3/2]],
    T_relative = [[1,2(1-x^-1/2)],[0,x^-1/2]].

Its determinant is x^-1>0 for finite x. The physical state is not erased by
drag release. Asymptotically the relative velocity dies, Delta approaches
w+2z, and Delta/delta_m falls approximately as 1/x whenever A is nonzero.
If A=0, this catch-up conclusion fails: a purely compensated density mode
can retain opposite species perturbations without total growing matter.

The surviving common growing amplitude is particularly informative:

    A(k)=f_c[3delta_c,d+2delta_c,N,d]/5
         +f_b[3delta_b,d+2delta_b,N,d]/5.                        (7)

Thus acoustic **density and velocity phase** at drag imprint later growing
structure. Delta/delta_m becoming small does not erase BAO or acoustic-phase
information already projected into A(k). This is a transfer statement, not a
fitted BAO model; a real prediction needs initial transfer functions from the
photon/baryon/cold equations rather than hand-chosen acoustic phases.

For the explicitly chosen normalized example delta_c,d=delta_c,N,d=1,
delta_b,d=delta_b,N,d=0, equation (6) becomes

    delta_m=f_c x,
    delta_b=f_c[x-3+2x^-1/2],
    delta_c=f_c x+f_b[3-2x^-1/2].                               (8)

With f_b=0.02237/(0.02237+0.1200), baryon deficits of 50%, 10%, and 1%
occur at x=4.49725, 30.82670 and 342.56568. These are **EdS normalized
example lever arms**, not inferred cosmological catch-up redshifts. The script
also stores a declared illustrative redshift conversion, which inherits every
EdS/initial-state approximation. Multiplying all initial perturbations by an
arbitrarily small amplitude makes these shape calculations genuinely linear;
the normalization 1 is not a claim of nonlinear-density accuracy.

## 4. Exact cold/vacuum degeneracy and its limit

For signature (-+++), a perfect fluid with exactly constant pressure
p=-rho_Lambda has

    T^mu_nu=(rho+p)u^mu u_nu+p delta^mu_nu
           =rho_c u^mu u_nu-rho_Lambda delta^mu_nu,
    rho_c=rho-rho_Lambda>=0.                                   (9)

This is an exact local stress identity for arbitrary allowed u, not a
background-only equation-of-state match. With constant rho_Lambda and the
usual conserved, universally metric-coupled total stress, divergence of the
vacuum part vanishes. Projecting conservation along and perpendicular to u
gives dust continuity and geodesic acceleration where rho_c>0. Conversely
dust plus that vacuum gives exactly this fluid. Hence the same initial metric,
baryons and total dark stress produce the same gravity within this class.

In FRW,

    rho=rho_Lambda+C a^-3, w=-rho_Lambda/(rho_Lambda+C a^-3),
    dp/drho=0, delta p=0.                                      (10)

The constant-pressure label combines two cosmological roles, but C is still an
independent conserved initial amplitude. No equation in (9)-(10) chooses it
from rho_Lambda. It does not convert the measured/fitted cold amount into a
derived vacuum prediction. The degeneracy is consistent with the primary
discussion of total dark stress and perturbations in [Kunz,
astro-ph/0702615v2, 27 February 2007](https://arxiv.org/pdf/astro-ph/0702615),
section “Beyond the background”; the particular identity (9) is proved here.

Exact background equivalence alone is weaker: it permits different pressure
perturbations and anisotropic stresses. Those can change acoustic driving and
growth even with identical H(a). A canonical scalar generally has nonzero
rest-frame pressure response; adding a potential offset does not grant it
(9)'s perturbation equivalence. A rapidly oscillating scalar can approximate
dust with mass/gradient-dependent residuals, which require explicit bounds.

The single-velocity perfect-fluid equivalence is valid before dust caustics.
Multistream dark matter can require anisotropic stress or a phase-space/wave
description; a single perfect u cannot represent arbitrary intersecting
streams. Also a gravity theory with auxiliaries coupling separately to cold
and vacuum variables may distinguish the split even at identical metric
stress: the **same action and couplings**, rather than a shared field name,
must justify borrowing this degeneracy.

## Scope, evidence and next implication

Read before route selection: CFG253/288, L37/L182/L183 and
`reviews/cmb_inertia_recombination.py`. L37 distinguishes gravitational field
from photon-fluid acceleration. L182 is an approximate fluid Boltzmann
instrument with omitted hierarchy/source derivatives; L183 tests a particular
mean-field kernel in patched CLASS. Their successes/failures do not prove a
universal CMB statement about all MOND actions. CFG253/288 already test late
cold creation and energy/CMB obstructions. This lane does not rerun them.

What is new within this package is the exact four-mode transfer and invariant
as a **same-action source/pressure diagnostic**, plus explicit preservation
of acoustic density/velocity memory during baryon catch-up. The underlying
linear-fluid equations and constant-pressure dark degeneracy are known; no
worldwide novelty is claimed. Internal overlap search did not establish that
these combined diagnostics were already implemented in the new fourth lane.

Main run: 23/23 checks, exit 0. Five independent coupled two-species ODE
controls over 1<=x<=1000 agree with the analytic transfer to maximum scaled
error 4.1e-11; relative-invariant drift is below 1.8e-11. Exact symbolic
checks cover initial density/velocity, invertibility, mass weights, potential
memory and affine stress/continuity. Omitting the initial velocity from the
growing projection leaves the density unchanged but fails the velocity
initial-condition and finite-time invertibility checks, giving 21/23 and
expected exit 1. Both standard
runner manifests validate with unchanged actual inputs and retained outputs.
Limits: 30 s wall, 20 s CPU per process, 1 MiB logs, cooperative one-thread
numerical libraries; no requested memory or affinity cap.

Self-review verdict: exact identities proved in their displayed regimes;
the bounded ODE calculations corroborate them. No independent CMB spectrum,
atomic recombination calculation, nonlinear galaxy formation, microphysical
identity or abundance selection is established.

A unified cold/vacuum action must next provide: a cold clustering state
through acoustic driving/equality; the correct pressure and drag responses;
its same-action metric sources and forces obeying (3) or quantitatively
predicting (5); a state that survives caustics; and a rule selecting the
otherwise free C if a cold-abundance derivation is claimed. The cheapest new
calculation is to initialize (3)/(5) with actual baryon/cold density **and
velocity** transfer functions, or to derive the right-hand side directly
from the retained action. That calculation remains open.

Artifacts: `checks.py`, `contract.json`, `runs/main_a/{manifest.json,
stdout.txt,stderr.txt,results.json}`, and corresponding
`runs/velocity_drop_a/` preserving the failed control. Reproduce with
`python3 .../growth_and_identity/checks.py`; add
`--mutate-drop-initial-velocity` for the expected failing control.
