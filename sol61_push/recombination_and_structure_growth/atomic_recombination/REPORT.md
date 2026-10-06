# What atomic recombination determines, and what it leaves unidentified

Checkpoint SOL61-ATOMIC-RECOMBINATION-2026-10-05. Owner: `puzzle_32pi`
research subagent. Initial observed HEAD was
`3b06b67c4ed9180a3b7dc6692f3daf64f9625986`; current execution HEAD and actual
input hashes are in the scientific result. All writes are confined to this
directory. No commits, peer edits or global ledger changes.

**Result:** hydrogen neutralization is understood from dilute-gas entropy and
non-equilibrium atomic escape. It supplies necessary constraints on the atomic,
expansion, opacity and energy-transfer parts of a candidate action. It does
not identify dark energy or a cold component's microscopic nature. The new
project-level contribution is a reproducible hydrogen-rate laboratory,
precise correction of four earlier shortcuts, an exact rate-system degeneracy,
and analytic sensitivities separating atomic equilibrium from last scattering.
This is established atomic physics, not a claim of new recombination theory.

## Primary-source verification and previous scope

Read L37_RECOMBINATION.md, L182_recombination_kernel_solver.py,
L183_class_kernel_recombination.py, mi_recombination_why_2026.py and
cmb_inertia_recombination.py. L182 assumes instantaneous decoupling and imposed
finite-width damping; L183 uses patched CLASS perturbations. This lane does
not repeat their spectral calculations or turn their prescribed kernels into
field equations. L37's background-blind statements hold only within its
specified completions; they are not universal statements about arbitrary actions.

The exact public primary PDFs, extracted texts and SHA256 hashes are retained
under `sources/` and indexed in `sources.json`:

- [Peebles 1968](https://articles.adsabs.harvard.edu/pdf/1968ApJ...153....1P),
  the original ground-state population and radiative bottleneck calculation.
- [Seager, Sasselov & Scott 1999](https://arxiv.org/pdf/astro-ph/9909275v2),
  arXiv v2, 16 September 1999; equations (1),(3) and their atomic constants: the approximate hydrogen rate
  equation and Case-B fit used here.
- [HyRec, arXiv:1011.3758v2](https://arxiv.org/pdf/1011.3758v2), section II A,
  equations (1)-(12): detailed balance, parallel ground-state channels and
  matter-temperature evolution; section III gives effective multilevel rates.
  The PDF identifies the 21 January 2011 arXiv version but its rebuilt title
  page says November 2024. The retained byte hash pins what was read.
- [CosmoRec, arXiv:1010.3631v3](https://arxiv.org/pdf/1010.3631v3), confirms
  the multilevel/radiative-transfer correction scope.
- [Planck parameters, arXiv:1807.06209v4](https://arxiv.org/pdf/1807.06209v4),
  Tables 1-2, sections 2.1 and 7.7: base-model conventions and recombination
  treatment. Quoted values below belong to TT,TE,EE+lowE+lensing, not an
  assumption-free determination of arbitrary-gravity parameters.
- [CAMB results source](https://raw.githubusercontent.com/cmbant/CAMB/master/fortran/results.f90),
  retained with a content hash, checks the tau=1 and drag definitions directly.
  This is a 2026-10-06 master snapshot; a repository commit was not retrieved.

The mathematical convention translation is explicit below, including the
factor-four difference between HyRec's shell photoionization rate and the
RECFAST effective coefficient. No source supplies the candidate gravitational
action or derives its cold/vacuum identity.

## 1. The entropy reason for a temperature far below 13.6 eV

For a Planck spectrum,

    n_gamma = 2 zeta(3)/pi^2 (kT/hbar c)^3,
    s_gamma/(n_gamma k) = 2pi^4/[45 zeta(3)] = 3.60157.

At the illustrative Planck baryon density omega_b=.02237 and T0=2.7255 K,
the mass-to-baryon-number approximation used here gives eta=n_b/n_gamma
=6.1129e-10, or photon entropy about 5.8918e9 k per baryon. With Yp=.245,
eta_H=n_H/n_gamma=4.6152e-10. Hydrogen nuclei, all baryons and electrons are
not interchangeable number densities.

For neutral ground-state hydrogen plus nonrelativistic electrons/protons in
chemical equilibrium, detailed balance gives

    S=x_e^2/(1-x_e)
     =(1/n_H)(m_e kT/2pi hbar^2)^(3/2) exp(-chi/kT),
    chi=13.5984346 eV.

Proton/electron/H degeneracies cancel in this conventional ground-state
formula; excited populations and helium electrons are omitted. The reduced
mass correction is neglected in the phase-space prefactor. At fixed eta_H,
rewrite it as

    S=A/eta_H (m_e c^2/kT)^(3/2) exp(-theta),
    A=sqrt(pi)/[2^(5/2) zeta(3)], theta=chi/kT.

Thus at a specified x_e, theta equals the logarithm of the enormous dilute
free-electron phase space, not a number of order unity. In the computation,
S=.5 corresponds to x_e=.5 and gives

    T_half,Saha=3733.912 K, z_half,Saha=1368.991,
    theta=42.26219, kT=.3218 eV.

The large photon entropy fixes the very small hydrogen density at a given T;
the electron translational entropy adds the phase-space factor. Binding must
overcome that entropy before neutral hydrogen dominates. The statement
'recombination occurs when kT crosses 13.6 eV' misses this effect.

The blackbody ionizing-photon inventory is useful but is not the Saha condition:

    F(>chi)= [1/(2 zeta(3))] integral_theta^infinity t^2/(exp(t)-1)dt
      = [1/(2 zeta(3))] sum_j>=1 exp(-j theta)
         [theta^2/j+2theta/j^2+2/j^3].

For theta large the leading numerator is
(theta^2+2theta+2)exp(-theta). The older exp(-theta) proxy omits this polynomial.
The correct condition F/eta_H=1 gives theta=27.30676 and T=5778.910 K,
not the proxy's roughly 7400 K. **Neither condition determines recombination.**
At Saha half ionization the ambient ionizing blackbody population is only
7.4656e-7 photons per hydrogen nucleus, yet half the hydrogen remains ionized
in equilibrium. There need not be a simultaneous inventory of one ionizing
photon per ion: equilibrium is a balance of rates and phase-space populations,
and recombination itself creates nonthermal photons. The earlier claim that
hydrogen stays ionized *while and only while* this inventory exceeds unity is
not a valid derivation.

## 2. Exact Saha sensitivities and their restrictions

Differentiating ln S at fixed ionization fraction gives

    (theta-3/2) dln T
      =dln eta_H -(3/2)dln m_e+theta dln chi.

For the leading nonrelativistic Coulomb binding chi proportional to m_e alpha_EM^2,

    dln T/dln eta_H =1/(theta-3/2)=.02453254,
    dln T/dln m_e =1,
    dln T/dln alpha_EM =2theta/(theta-3/2)=2.07359762.

The mass relation is exact within that leading Coulomb approximation, with
eta_H held fixed; using the reduced mass instead would require its derivative.
The independent eta perturbation is checked by numerical finite differences.
The full physical response to changing alpha_EM or m_e also changes transition
rates, Thomson scattering and detailed atomic structure. These equilibrium
sensitivities are not the full last-scattering sensitivities.

Since T=T0(1+z), redshift sensitivities also depend on T0. At fixed baryon
physical density, eta_H is proportional to (1-Yp) omega_b/T0^3, so one cannot
vary eta_H and T0 independently while claiming omega_b was unchanged.
Saha equilibrium contains no H. Its applicability, departures and the
observable scattering epoch do contain H.

## 3. Why rate-limited neutralization is later than Saha

Let alpha_B be the excited-state Case-B recombination coefficient, beta_rec
its detailed-balance photoionization coefficient, Lambda=8.22458 s^-1, and

    E2=chi/4, E21=3chi/4,
    beta_rec=alpha_B(T_gamma)(2pi m_e kT_gamma/h^2)^(3/2)exp(-E2/kT_gamma),
    R_escape=8pi H/[lambda_Lya^3 n_H(1-x_e)].

In the RECFAST convention adopted here,

    C=(Lambda+R_escape)/(Lambda+R_escape+beta_rec),
    dx_e/dz=C/[H(1+z)]
      [n_H alpha_B(T_m)x_e^2-beta_rec(1-x_e)exp(-E21/kT_gamma)].

HyRec defines a shell coefficient beta_B=beta_rec/4 and a 2p rate
R_Lya=R_escape/3. Its equation (11) is therefore the same C after multiplying
numerator and denominator by four. Mixing these conventions would be a
factor-four error. Matter temperature evolves with Compton energy exchange
and adiabatic cooling; this is included in the laboratory.

Both two-photon 2s decay and cosmological Lyman-alpha photon escape contribute
in parallel. Direct ground-state recombination produces ionizing photons
which are quickly reabsorbed under the optically thick assumptions. Lambda
is small relative to allowed atomic transition rates, but enormous relative
to H: at z=1100, Lambda/H=1.5976e14. The bottleneck is not a years-long
individual 2s lifetime. Most captures are reionized before reaching a durable
ground state, the excited-state populations are tiny, and line photons are
trapped. The calculation gives beta_rec=517.77 s^-1, R_escape=3.3324 s^-1
and C=.0218333 at z=1100.

Modern multilevel codes resolve effective excited-state transitions and
radiative transfer, including line feedback, frequency diffusion, stimulated
and higher-level two-photon effects, and helium processes. The source papers
justify the reduction and explain why this elementary three-level laboratory
is insufficient for precision cosmological inference. F=1.14 is an old
RECFAST effective correction, not a modern multilevel calculation.

## 4. Recombination, last scattering, visibility width and drag are distinct

Hydrogen recombination denotes the changing x_e history. A specified chemical
milestone, such as x_e=.5, is not a photon-decoupling definition. Photon optical
depth excluding reionization is

    tau(z)=integral_0^z c sigma_T n_e/[H(1+z)] dz.

CAMB's derived zstar uses tau=1, not an exact visibility-maximum definition.
The conformal-time visibility is g_eta=a c sigma_T n_e exp(-tau), while the
probability density per redshift is g_z=tau_z exp(-tau). Their modes differ
because of the coordinate Jacobian; a width must name its measure.

Baryon drag uses the momentum-transfer weighting

    tau_drag(z)=integral_0^z tau_z/R_b dz,
    R_b=3rho_b/(4rho_gamma).

A drag epoch defined by tau_drag=1 is a separate milestone. Its separation
from zstar is not a thickness. In the baseline laboratory:

| Quantity | Redshift/result |
|---|---:|
| Saha x_e=.5 | 1368.991 |
| kinetic x_e=.5 | 1272.619 |
| tau=1 | 1089.521 |
| conformal visibility maximum | 1089.25 |
| redshift-density visibility maximum | 1078.75 |
| drag tau=1 | 1059.673 |
| conformal visibility FWHM expressed in z | 195.947 |

The visibility mode uses a .25-redshift grid, so its listed decimals are grid
locations, not sub-grid precision. The tau/drag integrals begin at z=50 and
exclude reionization. Assuming post-recombination electrons continue to
recombine without sources, omitted tau below 50 is bounded by .0001996.
This small cutoff does not change the distinction between the milestones.
No actual recombination-width measurement or CMB fit is claimed.

Planck's base model quotes omega_b=.02237, omega_c=.1200, H0=67.36 km/s/Mpc,
zstar=1089.92 and zdrag=1059.94 for the stated data combination. omega_i means
Omega_i h^2; h=H0/(100 km/s/Mpc). 100theta_MC is the sampled approximation,
not exactly 100theta_star. Base-model neutrino assumptions include total mass
.06 eV and N_eff=3.046. The laboratory approximates that transition by adding
.00064 to matter while retaining massless N_eff radiation, a small early
neutrino-density double count. It omits helium electrons and multilevel
corrections. Its close tau=1 resemblance to Planck is **not** proof of
Planck-level accuracy, a calibrated likelihood or correct neutrino dynamics.

## 5. Expansion versus atomic rates: a useful separation

At fixed x_e,T,n_H and atomic constants, R_escape is proportional to H. Hence

    dln(C/H)/dln H
      =-1+R_escape beta_rec/[(Lambda+R_escape)(Lambda+R_escape+beta_rec)].

H affects line escape as well as the redshift-time conversion and scattering
optical depth. It is therefore incorrect to say H enters *only* through
cooling. If alpha_B and its detailed-balance beta are changed together,

    dln(alpha_B C/H)/dln alpha_B=C.

Both local derivatives are checked independently by finite differences.
When C is tiny, the early bottleneck rate is weakly sensitive to the exact
capture coefficient; increasing capture also increases reionization. At late
times C tends to one and capture controls the residual electrons.

The laboratory gives a concrete counterexample to equating the chemical and
scattering responses: increasing H everywhere by 10% moves the half-ionization
redshift *down* from 1272.62 to 1269.11, but moves the tau=1 photon milestone
*up* from 1089.52 to 1092.64. The residual x_e at z=200 rises from .00037793
to .00041486. Chemistry and opacity compete, so one 'recombination redshift'
cannot summarize the response to a modified expansion rate.

Deleting two-photon decay delays tau=1 to 1016.63; deleting Lyman-alpha escape
delays it to 1063.93. The zero-channel controls show that both channels matter.
Neither deletion is a physically plausible altered atomic theory by itself.

There is an exact **phenomenological common-clock degeneracy** in these rate
and opacity equations: at fixed densities, temperatures, binding energies,
lambda_Lya and initial data, rescale

    H, alpha_B, beta_rec, Lambda, sigma_T -> s times their original values.

Then C, dx_e/dz, the Compton-temperature equation, optical depths and drag
history are invariant. The s=1.1 control changes x_e by at most 9.74e-11
numerically. This follows analytically because every rate/H ratio and each
ratio inside C is unchanged. It is not a demonstrated transformation of
alpha_EM or m_e, a realizable microscopic theory, or a conserved gravitational
action. Atomic relations, Friedmann dynamics, external clock measurements
and sound-horizon/distances can break it. Recombination history alone measures
these combinations; it does not identify each rate or the absolute expansion
clock separately.

## 6. Physically necessary clues for the candidate action

A candidate must derive its *physical* H(z), proton/electron conservation,
photon temperature/redshifting law, transition rates and scattering opacity
from the same action. The relevant baryon density is the atomic number
current; extra gravitational source density cannot be substituted into n_H
unless it genuinely produces hydrogen and electrons. Additional ionizing
photons or heat deposition require explicit source terms and a reaction/energy
budget. Any formation switch coupled to baryons must expose those terms.

Reproducing x_e(z) does not reproduce the acoustic potentials. L182/L183
already separate imposed acoustic gravitational forcing from atomic opacity;
we do not convert their mean-field kernel tests into universal MOND exclusions.
A cold source that mimics cosmological matter must supply the required
perturbation stress and clustering without increasing Thomson-coupled baryon
loading or electron opacity. Neutralizing baryons does not automatically
create that source: those same baryons carried photon-coupled inertia before
decoupling and retain a baryon number/thermal history afterward. This is a
necessary distinction between atomic and gravitational source dictionaries,
not identification of a cold particle species.

The vacuum sector is constrained indirectly through its contribution to H,
distances and perturbations. Atomic recombination supplies no microscopic
identity or 32pi selection rule for dark energy. A label/density switch that
preserves an unexcited FRW internal stress branch still owes its varied
baryon/photon/atomic reaction equations. Conversely, ordinary recombination
can remain nearly standard while an extra cold perturbation source changes
the acoustic forcing. The source and clock dictionaries must be checked
separately and then reunited in the same action.

## Reproduction, audit and limits

Run `python3 sol61_push/recombination_and_structure_growth/atomic_recombination/atomic_checks.py`.
A supplied output-directory argument writes only that directory's
`atomic_results.json`; the standard runner invocation and validated outer
manifest are in `runs/atomic_lab_v2_sources/`. `contract.json` pins the exact inputs,
software, bounds and non-claims. Sources are independently hashed in sources.json.

The laboratory integrates z=2200 to 50 with Radau, max step 5 and a dense
.25-redshift output grid, relative tolerance 2e-8, with a 2e-10 convergence
control. Maximum difference in x_e is 1.58e-9. The exact blackbody tail,
Saha root, atomic-convention mapping, channel controls, two local derivatives
and common-clock invariance are checked. Finite results corroborate the
stated rate system, not a multilevel error budget or candidate-action closure.

Smallest missing implication: obtain the candidate action's changed H,
physical opacity/atomic source terms and any energy deposition, and pass
those into an authenticated multilevel solver together with its fully derived
perturbation equations. A successful atomic history by itself neither proves
structure growth nor determines the nature of cold matter or dark energy.

The initial `runs/atomic_lab/` precedes refinement of the Seager source
registry to its verified v2 identifier. Its source-registry input is therefore
stale against the present file; `runs/atomic_lab_v2_sources/` is the final
validated run. No equations or numerical criteria changed in that refinement.
