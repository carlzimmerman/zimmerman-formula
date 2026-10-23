# A collisionless damping route has a resonance and Jeans gate

The declared Vlasov matter sector supplies a potential conservative relaxation channel: particles can absorb coherent field energy by phase mixing. A local Maxwellian calculation has damped coupled scalar roots when particle and wave speeds are comparable. However, the beta value used in our previous examples puts the polarized scalar far above the cold-particle velocity dispersion. Resonant damping is then negligible in the local approximation. Moving the mode into resonance requires a very different, still unpredicted beta and must also satisfy a gravitational stability condition.

This does not derive a new fundamental interaction or the cold/P sourcing split. It is a discriminator for a completion using the matter sector already declared by A33.

## What the repository actually supplies

A33_MASTER_ACTION §1 declares a collisionless distribution obeying the Vlasov equation and quotes sigma_c=8.33km/s in its discussion. It separately identifies div P=varsigma(rho_c-rhobar_c) on a solution and explicitly says that this is not an extra action term. Therefore this calculation uses minimal gravitational coupling only; it does not silently impose that unproved identification. In particular it cannot repair the double-counting and sourcing problems found in the multiplier lane.

Earlier CFG935 and CFG939 already discuss phase mixing, and CFG939's tethered multistream engine settles partly by ejection. Those are different dynamics and are not rerun or certified here. Collisionless relaxation itself is not new.

## Local kinetic determinant

Use a uniform polarized patch, a Maxwellian equilibrium with one-dimensional velocity dispersion s, and a longitudinal perturbation parallel to the polarization. Cosmological gradients, background curvature and the self-consistent nonuniform matter equilibrium are omitted. The homogeneous gravitational background requires the usual local background subtraction; it is not an isolated equilibrium halo.

Define

    Q=B+eta k²,
    D=(h+gamma k²)k²-Q omega²,
    z=omega/(sqrt(2) k s),
    R(z)=1+z Z(z), Z(z)=i sqrt(pi) wofz(z),
    J=K rho/(k² s²).

The linear Vlasov response and the reduced gravity/scalar equations are

    delta_rho=-(rho/s²) R Phi,
    sigma=-K delta_rho/D,
    Phi=-K delta_rho/k²+K sigma.

Eliminating the density and potentials yields

    D(1-J R)-K k² J R=0.

Equivalently, with a=K/(h+gamma k²) and z0 the bare positive field frequency divided by sqrt(2)ks,

    [1-(z/z0)²](1-J R)-a J R=0.

The Landau continuation and exp(-i omega t) convention mean negative Im z is damping. Damping is transfer of coherent energy into particle phase-space structure, not destruction of total energy or guaranteed thermal equilibration.

## Static and resonant checks

At zero frequency R=1, giving the local static threshold

    Jcrit=1/(1+a),
    k² s²=K rho [1+K/(h+gamma k²)].

The polarization increases the attractive static response and tightens the Jeans condition relative to bare Newtonian gravity. The threshold alone does not prove stability of every finite-frequency root or every inhomogeneous configuration.

For a=1/3 the threshold is J=0.75. Positive-frequency field roots were followed from seeds near z0 for z0=0.5,1,2,5 and J=0.1,0.5,0.74. All12 converge with residual below6e-16 and negative imaginary part. Examples:

| z0 | J | coupled z |
|---|---:|---|
| 0.5 | 0.5 | 0.493465 - 0.052055 i |
| 1 | 0.5 | 1.025132 - 0.043906 i |
| 2 | 0.5 | 2.030337 - 0.007678 i |
| 5 | 0.5 | 5.008758 - 4.58263e-11 i |

These are found roots, not a census or a proof of unique continuation between the discrete J values. At J=0.8,z0=1, a separate search finds a growing root z=0.0365449 i with residual1.12e-16. Stronger gravitational coupling is not a free route to efficient damping: it can introduce collapse.

## The parameter mismatch

For the previous x=g/a0=1 example, h/K=3. Neglecting gradient corrections at sufficiently small k, the bare phase speed is

    v_phase=c sqrt[3 beta/(2+3 beta)].

At beta=0.02798 this is60167.6km/s, versus the quoted8.33km/s cold dispersion. The ratio is about7223 and z0 about5107.4. The formal nonrelativistic Maxwellian resonant factor exp(-z0²) has log10 approximately-11328945. This number must not be interpreted as an accurate relativistic tail probability; the Maxwellian model is inappropriate for precision at such speeds. The large velocity mismatch, rather than that particular exponent, is the useful result.

Setting v_phase=s in this approximation requires

    beta=2(s/c)²/[3-3(s/c)²] approximately5.147e-10.

No mechanism here predicts that beta. Choosing it specifically to make damping effective would be a fit. A finite-polarization constraint reduction and all existing parameter bounds must be reconsidered before using that value. The damping rate also depends on J, hence on density and wavelength; phase-speed matching alone does not guarantee rapid relaxation.

Heating and phase-space redistribution would change the medium beyond linear order. A fixed quoted dispersion cannot simultaneously be treated as an inexhaustible sink for a large settling energy. A live distribution and its energy budget are required.

## Prior art and verification

SciSpace returned Moretti, Bombacigno and Montani, *Gravitational Landau Damping for massive scalar modes*, Eur. Phys. J. C80,1203(2020). The primary arXiv record https://arxiv.org/abs/2005.08010v4 confirms a homogeneous isotropic Juttner-Maxwell/Vlasov analysis of massive scalar waves and the role of subluminal phase velocity. This was verified at abstract level only; its equations and relativistic massive mode have not been imported as a theorem about A33. It establishes relevant prior art and prevents treating gravitational scalar Landau damping as a novelty claim.

kinetic_run/manifest.json validates; seven checks pass. The initial serialization-only error from NumPy bool values was corrected without changing equations or thresholds. The numerical roots use SciPy's complex probability function and a two-real-variable root solve. No independent root census, global kinetic simulation or new mutation was performed. The main reduction and interpretation are self-reviewed.

The concrete next question is whether an actual conserved matter completion fixes a compatible phase speed and density/wavelength range while producing the required static sourcing. If it cannot, phase mixing is merely another available phenomenon, not the missing mechanism. Current evidence does not derive kappa, varsigma or a viable galaxy/cluster selector.
