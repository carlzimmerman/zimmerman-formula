# The question at hand, stated in full (2026-11-07)

Self-contained. Everything needed to attack the problem is here or named by commit in the repository. Units SI
unless stated. "Both footings" means two calibrations of the galaxy law that the programme carries in parallel
(canonical and alt); any answer must hold on both. No LCDM input may be used as a premise; raw data or quantities
native to this framework only. kappa = 1/2 is FITTED, not derived.

## A. The theory as it stands (deposited, DOI 10.5281/zenodo.24040313)

A1. Galaxy law. For a system with Newtonian baryonic acceleration g_N, the observed acceleration g obeys
    g_N = g^2 / (g + a0), with a0 = kappa c sqrt(G rho_DE), kappa = 1/2, rho_DE the dark-energy density
    (a0 ~ 1.1-1.2e-10 m/s^2). It passes 145-175 SPARC rotation curves (rms 0.054-0.056 dex), galaxy-galaxy lensing
    (KiDS), the Solar System (Cassini margin >= 4.8e7, PPN gamma = beta = 1 to 1e-12), gravitational-wave speed
    (c to 6e-32). It fails two large low-surface-brightness discs (AGC 114905, Malin 1) by over-predicting.
A2. Action (v3s). S = (c^3/16 pi G) Int sqrt(-g) [R - 2 J(Y) + 2 K(Q)] - S_stiff + S_m[g, matter], with tau the
    khronon (a preferred foliation scalar), A_mu its acceleration, Y = A.A/c^4, J(Y) = Lambda - 2 a_geo^2 [u - ln(1+u)],
    u = sqrt(Y)/a_geo, a_geo = a0/c^2; Q the clock rate, K(Q) = mu_K^2 (Q - 1)^2; P an independent spatial covector
    with Legendre form P.A - W(K|P|); stiffness S_stiff = (gamma_L/2) Int sqrt(-g) F(Pi), Pi = D.P (the khronon charge),
    F the owner-adopted blend: pure Pi^6 near 0, C^4-blended to Pi^2 above b = rho_DE, gamma_L = K L*^2/2 with
    L* >= 21.7 / 22.9 pc. Covariant field equations certified (sympy residuals <= 7e-40; Lean theorems with mutation
    twins). Candidate successor AC2q switches on Sigma = D.P + 2X (X ~ rho_DE) instead of D.P; differs only in
    0 < Sigma < X.
A3. Static consequence used below: in the law's field an isolated galaxy's potential grows logarithmically,
    Phi = v_f^2 ln r, v_f^4 = G M_b a0, out to the radius where an external field takes over. Escape speeds at the
    formation radius are 107-421 km/s for galaxies with M_b <= 1e11 Msun, >= ~2000 km/s for clusters.

## B. Three measured facts (the contradiction)

F1. Something cold and non-baryonic gravitates at z ~ 1100. Planck PR4 + ACT DR6 primary CMB fits the framework's
    background only with a cold component of about 5.4 times the baryon density; baryons only fail. The CMB-lensing
    power shape (L <= 400), linear growth and the existence of a z ~ 10 quasar host (A2744-QSO1) need the same.
F2. Galaxies hold none of it today. Rotation curves allow extra mass <= 0.33 / 0.19 of the baryons inside the
    discs. KiDS isolated-lens stacks, once the hot circumgalactic gas is taken from kinetic-SZ measurements rather
    than assumed, allow no bound extra halo at 100-300 kpc (posterior excess over the law -0.21 to +0.05 dex).
    X-ray ellipticals, the KiDS colour split and the bright M31 dwarfs are explained by the stellar-mass-to-light
    budget. Coma UDGs are not a test (tidally disturbed). Wide binaries are predicted Newtonian.
F3. Clusters hold it today. Seven X-COP clusters need extra mass f = 4.2 / 3.8 times the baryons inside r500
    (+0.44 / +0.41 dex over the law), with a radial profile between the gas's and the stars'. Twenty groups need
    f = 1.2-3.5 / 0.9-2.9 (step +0.26 / +0.22 dex, fragile). The Bullet cluster needs the extra mass collisionless
    (it sits on the galaxies, not the gas).

Needed extra mass as a fraction of baryons, by class: discs <= 0.33 / 0.19; ellipticals ~0 after IMF; groups
1.2-3.5 / 0.9-2.9; clusters 4.2 / 3.8; cosmic (CMB) ~5.4.

## C. What has been eliminated (each by a frozen, mutation-controlled lane; commits in CLOSURE_REGISTER.json)

C1. Any time-independent sector: cold fluid (captured by every well, discs included: f_cap 4.1 in discs);
    warm fixed-temperature sea (retention exp(-depth/sigma^2) is a step in host mass and gives the wrong cluster
    profile; in the log potential an isothermal sector has slope -(v_f/sigma)^2); hot thermal fermion (11 eV:
    out of discs but fails CMB lensing chi^2 166-194 and under-fills clusters); shock-heated sector with an entropy
    floor; primordial black holes and late compact objects (track the gas or fail the Bullet).
C2. Any local switch making the law stronger in hot systems: pressure/density, temperature, virial heating, khronon
    velocity, enclosed density, clock depth, kinematic support, cold-gas fraction, morphology, environment /
    external field; and any monotone function of two such variables (best non-circular pair leaves clusters 3.5-4.5
    sigma high with discs at 0). The needed amount spans ~100x across classes, so no switch carries it.
C3. Any alternative action family graded: non-minimal / disformal couplings, a second length scale, two-branch
    kernels, Weyl couplings, nonlocal kernels, flow memory, formation-epoch memory, conserved phantom charge,
    AeST (screening mass needed by the web and by KiDS differ 160x), nuHDM (fails as a prediction).
C4. Time-dependent sectors: (a) late heating as a fluid (Jeans scale growing with Omega_DE): passes CMB lensing,
    growth and the forest, fails KiDS when bound and fails X-COP / groups / Bullet when it evaporates (fluid is
    ram-stripped); (b) a late KICK of a cold collisionless carrier to 575-650 km/s at halo virialisation (Sept 2026):
    passed galaxy clearing, KiDS, S8, forest, Bullet; failed X-COP against a requirement of >= 0.87 retention and
    groups against 0.78-1.08 of a LCDM-like halo, while retaining 0.79-0.85 (massive clusters) and 0.17-0.34
    (groups). Those requirements have since been re-measured: today's are 0.78 / 0.70 (X-COP) and 0.17-0.65
    (groups). The re-grade at today's needs is running (lane CK1).

## D. The question

Q1 (the hinge). Does the action in A2 (or its AC2q successor) contain a mechanism that releases, at the moment a
    collapsing region virialises (or at a fixed cosmic condition such as the onset of acceleration), an energy per
    unit mass of the cold component equal to (1/2) v_k^2 with v_k = 500-650 km/s, with v_k INDEPENDENT of the depth of
    the well in which it happens? Constraints: (i) from a0, rho_DE, c and G alone the only velocities are
    ~sqrt(a0 L*) ~ 9 km/s and ~c, so a mass or density scale must enter; (ii) if the released energy scales with the
    local potential depth, the kick tracks the host, every well retains the same fraction, and the hundredfold
    spread in B is not reproduced, so that route fails; (iii) no new constant may be introduced and tuned to the gates;
    (iv) the cold component must be identifiable with a term already present (the K(Q) clock-depth dust is the
    candidate) or with a second phase of the vacuum whose smooth phase is rho_DE.
    A complete answer gives the term, the branch change, the released energy per unit mass, its dependence on the
    environment (must be flat across galaxies to clusters within the 500-650 window), and a mutation (wrong branch or
    wrong term) that gives a different number.

Q2 (if Q1 has no answer). Is there ANY mechanism, inside or outside A2, that carries F1, F2 and F3 together without
    any ingredient in C1-C4 and without a tuned constant? A valid answer names the physical quantity that separates
    a 1e11 Msun galaxy from a 1e14 Msun cluster for the component, shows the component is cold at z 1100, absent from
    galaxies to the F2 lines, present and collisionless in clusters at f ~ 4 with a gas-to-stars profile, and states
    what measurement kills it.

Q3 (if Q2 has no answer). Which of F1, F2, F3 is wrong, and what measurement shows it? F2 is the firmest. F3 rests
    on seven X-COP clusters (hydrostatic, with lensing cross-checks) and provisional group masses. F1 is a fit under
    the framework's own background and the record marks it as not independent evidence.

## E. Rules any answer must obey to count

Both footings. No LCDM inputs. Derive from the action; do not posit a profile or scan a knob. Keep every existing
pass in A1. State the kill measurement in advance. Nothing is adopted by an answer; the owner adopts.

## F. Update, same day (CK2, fe224c21ec): Q1 is answered NO for the action in A2

No isolated host ever changes the switch branch (the phantom density stays positive at every radius and epoch for
1e8-1e15 Msun), the adopted blend has F = F' = 0 at the branch point so a branch change carries zero latent energy,
and the only stored energy, pi G L*^2 rho_ph^2 per unit carrier, gives 0.8-125 km/s and tracks the well. AC2q's
background stiffness vanishes at the FRW point. So the action as written releases nothing at virialisation or at the
acceleration crossover. The question for an outside solver therefore narrows to:

Q1'. What MINIMAL addition to A2 (one field or one term, no tuned constant) releases a well-independent
     (1/2) v_k^2 with v_k in 500-650 km/s from the cold component at virialisation, keeps every pass in A1, and
     has a stated kill? The scale must come from somewhere: name it.
Q2 and Q3 stand as written.
