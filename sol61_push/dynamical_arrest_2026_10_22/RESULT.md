# Dynamical arrest: rotation, reciprocal drive and outgoing energy

DA-20261022, continuing core_formation_transport_2026_10_22 from Git revision 1b2ced55a4d56b426880aaad8d1d89cf2490812b. **A common selected core mass and distribution has not been obtained.** This checkpoint strengthens the angular-momentum obstruction, finds a surviving but parameter-dependent weak-drive branch, and derives actual field-radiation response rather than introducing free damping. All review is self-review. These are necessary Newtonian tests, not a completed relativistic theory.

## 1. Angular momentum supports size but does not select mass on the tested branches

Use the passive isolated action, X=0, with the predecessor's U,V,Z,J,T,B,D,H notation. Here J is scalar-gradient energy; denote material angular momentum by L and rotational kinetic energy by C. Consider smooth axisymmetric rigidly rotating stationary solutions, with finite energies and vanishing boundary terms. They are conditional solutions, not asserted to exist for every L or M. Extremizing energy at fixed M,L, without further circulation constraints, gives

    v = Omega cross r,  C = L²/(2I),  Omega L = 2C,
    mu_c = Phi+h-Omega² r_perp²/2.

The first law is dE=mu_c dM+Omega dL. Fixed-mass dilation at fixed L sends C to t²C. The field identities become

    U+3V-3Z-J+3T+2D-3B+2C=0,
    mu_c M=2U+2V+D+2T-C,
    V=2J+2Z+H/2.

Consequently, for total energy E=U+V+Z+J+T+B+C,

    mu_c M-E = -4J-2Z-H-2T+2B-D-4C < 0,
    (partial(E/M)/partial M)_L < 0.

The logarithmic polarization potential still gives D>2B. Thus conserved total spin does not introduce an interior preferred mass through binding energy. This does not mean spin fails to resist compression at fixed mass.

More generally, on a differentiable family with alpha=d ln L/d ln M,

    M² d(E/M)/dM = -4J-2Z-H-2T+2B-D+(2alpha-4)C.

It remains negative for alpha<=2. This includes fixed specific angular momentum (alpha=1). It also includes a *conditional* constant-density, constant-dimensionless-spin scaling R proportional to M^(1/3), L proportional to M sqrt(GMR), hence alpha=5/3. No cosmological spin distribution is inferred from that dimensional example. Steeper supplied spin growth can evade the sign argument, but its accretion history is then the missing input.

This is not a theorem about arbitrary differentially rotating states, conserved circulation distributions, external confinement or driven fields. Nor is a rotating stationary point a global minimum: angular momentum can reside in a low-mass distant component, and mass shedding must be considered. Finite-branch endpoints do not by themselves predict the abundance of remnants.

### Formation cannot simply invent cold-fluid vorticity

The actual cold equation is D_t v_c=-grad(Phi+h), even when h varies with time through driven fields. For a smooth material loop,

    d/dt integral v_c.dr = integral [-grad(Phi+h)+grad(v_c²/2)].dr = 0.

Initially zero circulation stays zero while the single-stream smooth description applies. This blocks assuming rigid rotation appears automatically from irrotational initial data. It does **not** prohibit tidal angular momentum of an irrotational nonspherical patch, orbiting substructures, or a kinetic/multistream continuation. Those need their own evolution and initial data. The standard loop identity is also given in [Fitzpatrick's derivation, equations 4.79–4.81](https://farside.ph.utexas.edu/teaching/336L/Fluidhtml/node63.html); the present application follows directly from the displayed cold equation and does not require incompressibility.

## 2. Finite rotational support: size and fit sensitivity

To quantify the direction of the effect without pretending to solve a rotating galaxy, retain the canonical matched core and minimize its energy over one spherical dilation. This is a trial family, not an axisymmetric equilibrium. Its exact restricted energy is

    E(t)=t U+t³ V+t^-3 integral W(t²w)+t² C0,
    R(t)=R0/t,  I(t)=I0/t².

The exterior field tail is included. The canonical profile has I/(MR0²)=0.348731. Six rotational energies C0/|U| were tested, with independent 160/320-node quadratures. The resulting monopole profiles were inserted into the same empirical-law-plus-core comparison, without refitting. This does not include flattening, stellar response, or the extra baryonic force from a driven mediator.

| C0/abs(U) | trial edge (pc) | MW calibration RMS ln residual | UFD mean ln residual | SPARC mean dex residual |
|---:|---:|---:|---:|---:|
| 0 | 321.5 | .2156 | .0923 | .02674 |
| .01 | 327.0 | .2177 | .1077 | .02674 |
| .05 | 350.4 | .2270 | .1680 | .02674 |
| .10 | 381.8 | .2464 | .2401 | .02694 |
| .20 | 452.1 | .2986 | .3702 | .02709 |
| .40 | 617.2 | .4013 | .5638 | .02757 |

Positive dwarf residual means observed dispersion exceeds the model. UFD standard errors range .116–.122; these summary errors are not full observational/systematic likelihoods. The strongest expansion worsens dwarf support, while the rotational sample scarcely changes because exterior monopole mass is unchanged. Modest expansion remains possible. None of these rows selects its own spin or mass, and the large-spin rows especially cannot stand in for flattened equilibria.

The translating-polarization inertia correction scales as t³ at fixed mass in this trial family. With the predecessor's imposed z=10 conversion, the k=1/Mpc retained amplitude rises from .952756 to .955247 across the table. Expansion reduces late inertial suppression but does not recover the preformation diffuse loss. This is a sensitivity result, not a formation calculation.

## 3. A prescribed drive can hide the baryonic reaction

In a local adiabatic phase calculation with h held fixed, set chiA=chi0+h²/(2mu²). Prescribing baryonic vorticity omega gives X=g omega/chi, hence

    y²(1-y)=d_v,
    y=chi/chiA,  d_v=g² omega²/(2mu² chiA³).

The positive locally stable branch satisfies y>2/3 and ends at d_v=4/27. Its local effective potential is unbounded toward chi=0 for nonzero maintained drive. The branch loss is not a new stable arrested phase. Prescribing omega assumes an external agent supplies the torque/work needed to maintain it; the isolated reciprocal action does not supply that agent.

To retain reaction, use the homogeneous transverse mode already present in the reciprocal action:

    L_mode=rho v²/2+MX Xdot²/2-chi X²/2+g k X v.

At fixed mode canonical momentum p=rho v+gkX, its energy is

    E_mode=(p-gkX)²/(2rho)+chi X²/2,
    X=(gkp/rho)/(chi+c),  c=g²k²/rho,
    E_mode,min=p² chi/[2rho(chi+c)].

For the density-weighted coupling g=g0 sqrt(rho), c=g0² k². Define q=c/chiA and d=p² c/(2rho mu² chiA³). The local phase equation and relaxed curvature become

    (1-y)(y+q)²=d,
    V_eff''/mu²=(3y+q-2)/(y+q).

The stable positive branch requires 3y+q>2. For q<2 it folds at y=(2-q)/3; for q>=2 it can reach arbitrarily small positive y before hitting the forbidden chi=0 boundary. These are families parametrized by momentum and coupling, not a selected cold mass. A field gradient on the mode scale changes this reduction; it was omitted deliberately in this local test. Holding nonzero h fixed would also require a cold reservoir. The time-evolution tests below use h=0, chiA=chi0, so no such cold reservoir is hidden in them.

### Strong phase shifts conflict with small reciprocal curve corrections in this local comparison

The previously derived local flat-disc relation is

    v² = r Phi'/(1+n f0),  f0=g0²/(chi r²),

for density proportional to r^-n, negligible pressure and locally constant chi. Identifying the mode scale k=1/r gives f0=q/y. Requiring a speed change below epsilon and combining with local phase stability yields

    y > 2/[3+((1-epsilon)^-2-1)/n].

For n=2 and a declared 5% speed tolerance, y must exceed .654875. Large q can stabilize much smaller chi only at the price of large velocity feedback in this comparison. This is not a global exclusion: the k=1/r identification, adiabatic reduction and flat-disc approximation are explicit assumptions.

There is a surviving weak-drive witness: y=.9, q=.01 is locally stable and changes the local flat speed by about 1.1% for n=2. It is not a common fitted parameter solution across galaxies, nor does it determine a core mass, a central occupation or a cluster profile.

## 4. Energy export exists conditionally; local stability is not cooling

The full two-coordinate local model, in units rho=mu=chiA=MX=Mchi=1, has potential

    V(y,x)=(y-1)²/2+y x²/2+(p-sqrt(q)x)²/2.

Three stable equilibria were perturbed by .005 in y and evolved to time 100. Their energy was conserved to relative error below 3.1e-14, and late chi oscillations remained approximately .01 peak-to-peak. The positive Hessian agrees with the relaxed-curvature condition. This closed local system has no outgoing channel and no attracting settled phase. It can exchange energy, not dispose of it.

Spatial fields do provide a possible outlet. In fixed-chi vacuum,

    MX Xtt-DX laplacian X+chi0 X=J_X,
    omega_gap²=chi0/MX,
    k²=(MX omega²-chi0)/DX.

For a real harmonic localized source and outgoing boundary conditions, the far-field Green function gives

    X ~ exp[i(kr-omega t)] Jtilde(k n)/(4pi DX r),
    P_out = omega k/(32pi² DX) integral |Jtilde(k n)|² dOmega.

Below the gap the harmonic far field is evanescent and carries no time-averaged outgoing flux. Above it the power is positive. Direct phase averaging verifies the sign and normalization of the flux -DX Xdot.grad X.

Source geometry matters. For a constant-g curl source of the form

    J_X=A curl[e_z exp(-r²/(2R²))],

one obtains

    P_out=omega k³ A²(2pi)³ R^6 exp[-(kR)²]/(12pi DX).

Thus this source is additionally suppressed as k³ near threshold; a freely chosen radiating monopole would misrepresent it. The formula assumes this particular smooth source and locally constant g. A variable-density source need not share its cancellation. The source amplitude and frequency here are prescribed to test the response, not derived from collapse.

The phase field has its own possible channel:

    Mchi delta_chi_tt-Dchi laplacian delta_chi+mu² delta_chi
        = (h²-|X|²)/2,

to leading vacuum-response order. Its gap is mu/sqrt(Mchi); its source need not have the curl cancellation. This can export energy without putting it directly into stars, but no actual emitted power or formation time follows until the coefficients and nonlinear source history are specified. In particular, the exactly fixed-chi benchmark cannot simultaneously be claimed to radiate through a dynamical chi field. Finite-compliance profile changes must be recomputed.

A transient finite-energy drive need not obey a single-frequency approximation. High-frequency tails, nonlinear mode conversion and material ejection remain possible. Conversely, an outgoing boundary does not generate power from a static source. Neither positive radiation response nor stable local oscillations supplies an accretion stopping rule.

## 5. Growth and distributions remain coupled missing obligations

At the unpumped homogeneous state X=0, the new sources are quadratic and the previous linear scalar decoupling remains. A nonzero driven background removes that argument: the phase equation contains -Xbar.delta_X at linear order, and its background chi is shifted. The following is only a necessary, favorable compliance diagnostic, holding chi=y chi0 homogeneous and constant while retaining the old EdS quasistatic equations:

| y | k=.1/Mpc amplitude/dust | k=1/Mpc amplitude/dust |
|---:|---:|---:|
| 1 | .999500 | .955654 |
| .95 | .999473 | .953594 |
| .8 | .999375 | .946071 |
| 2/3 | .999250 | .936976 |
| .5 | .999000 | .920079 |

Lowering chi increases ell=1/sqrt(K chi) and worsens this inherited growth loss. A drive confined to late collapsed regions can avoid this particular homogeneous modification, but then its localization and abundance must be obtained from formation. No full driven cosmology or CMB likelihood has been performed.

For angular supply, the exterior circularization scale is r_circ approximately j²/(GM). The supply distribution in j is required to turn this into an occupation or mass. Fixing a preferred j by hand simply replaces the earlier free core mass. Radiation removes energy and may angular momentum; it does not manufacture cold material or specify how much reaches the centre. Nor does local phase stability choose the orbital distribution of a cluster population. A kinetic population calculation needs source, capture, fragmentation and escape terms derived from actual encounters and initial conditions. The previous very slow pure-gravity cluster relaxation and dwarf heating constraints are not removed by any calculation here.

## 6. Status and next discriminating calculation

Three routes were executed: angular support, reciprocal phase drive and outgoing-field response. The joint target remains open. The useful surviving possibility is **localized, time-dependent phase-field radiation with modest spin**, followed by a supply-limited remnant. Its mass would have to emerge from the inflow and angular-momentum distribution; it is not a universal mass minimum of the tested passive action.

The next discriminating computation is a finite-chi collapse or encounter with specified conserved initial mass/angular momentum, dynamical baryons, outgoing X/chi fields, and a measured partition into remnant, ejecta and radiation. It must vary the initial inventory/spin to determine whether any remnant scale is insensitive to those inputs, and then repeat the profile/growth tests. Missing coefficients and initial data currently prevent a unique predictive run; a parameter survey must be labelled as such. No source distribution or damping coefficient was silently selected in this checkpoint.

Verification: 24 action/homology/drive/growth checks, 14 empirical-feedback checks and 6 radiation/compatibility checks passed. The initial run's one failure was structural symbolic equality between equivalent factorizations, corrected by simplifying their difference; the original evidence is retained. Passing checks verify the declared finite diagnostics, not the requested physical explanation. See AUDIT.md, HANDOFF.md and the per-run manifests.
