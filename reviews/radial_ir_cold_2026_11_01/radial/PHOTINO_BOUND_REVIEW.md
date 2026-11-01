# Fresh review of the leading hard photino-transition majorant

**Claim:** In the stated canonical-K rigid SU5 action at e=.003 and the specified1MeV photino benchmark, the leading heavy one-loop two-unbroken-vector transition into a final unbroken gaugino obeys |c7_eff|<=6.606061e6 in Gamma_hard=c7_eff² mchi7/(256pi³M6). This is a bound on that class, not an all-orders total width.

**Primary verdict: correct only after a stated restriction.** Read the executed `gapless_charge/decay_bound/DERIVATION.md` with its `SCOPE_ADDENDUM.md`: the C-forbidden one-field-strength transition must have a final **unbroken gaugino**. The known allowed Goldstino-photon Ward dipole is separate. The raw proof's broader sentence is false if extended to that dipole. The addendum makes the pre-run target precise without changing executed bytes. Under this restriction, the finite-topology proof and its physical normalization pass this review. The numerical spectrum/arithmetic leaf was freshly reconstructed in `run_bound_review`.

## Dependencies and obligations

The dependency chain is raw canonical vertices and U1 charge conservation -> fully massive charged loop -> boson/fermion operator-norm and topology bound -> two external momentum derivatives -> convergent radial integral -> inclusive three-body width -> unit restoration. The C selection and absence of a lower tree transition are essential to the momentum order. The benchmark pole coefficient and hbar/age constants are imported frozen inputs; this review does not recalculate the one-loop photino mass or independently authenticate those physical constants.

| Obligation | Verdict | Reconstruction |
|---|---|---|
| Charged internal block | Passed at the benchmark | An initial unbroken U1 gaugino couples to charged internal pairs; all external unbroken generators commute with that U1, so charge persists around the cycle. Neutral radial/phase/Goldstino propagators cannot appear in this hard one-loop trace. |
| xi1 rather than a Landau null cutoff | Passed | With Z=[-Im(Rz),Re(Rz)]^T, Hxi=H+2g²ZZ^T. Nonzero2g²Z^TZ agrees with the broken-vector mass matrix. This genuinely lifts the Goldstone directions; it does not relabel their Landau masses. |
| Charged counts and hierarchy | Finite range passed | Independent generator d/sqrt30 and eigensystems give48real scalars,36Weyls,12vectors; Mhat=.036898336774072726 and Mmax/M=6.00489381581<100. |
| Fermion/boson embeddings and trace | Passed | The full dimensions194+292=486 are below512. Canonical scalar-gaugino Frobenius norm squared20g² and vector-current5g² follow from two adjoints and Tr_adj R²=5. A32sqrt5g insertion envelope overcounts the real/complex, spin and mixed block norms. |
| Gauge, scalar-vector and seagull vertices | Passed as generous envelopes | Scalar currents have2k+p; the vector current has at most the three standard metric/momentum terms. Higgs mixing is bounded by g||R||||C|| with ||C||<=Mmax. These fit32sqrt5g(1+kappa)r;64g²5 overcounts scalar and vector seagulls. No small-F limit is used. |
| Box/triangle coverage | Passed for the declared class | Two external-gaugino insertions are off-diagonal boson/fermion blocks. Gauge insertions give boxes or a seagull triangle.24+6 ordered words are below64 before symmetry factors. Ghosts have no external-gaugino vertex. Scalar/vector mixing is an operator block rather than an omitted extra species. |
| Propagator differentiation | Passed | ||D||<=r^-2,||D'||<=2r^-3,||D''||<=10r^-4; ||S||<=r^-1,||S'||<=r^-2,||S''||<=2r^-3. For a box the maximal first-derivative coefficient sum is9 and second-coefficient sum32, so the mixed Leibniz bound is<=113<256. |
| Momentum degree | Passed after stated restriction | Gauge invariance plus forbidden one-field-strength transitions removes lower terms for final unbroken gauginos. This argument does not remove the separate Goldstino dipole. |
| Radial integral and continuation | Passed | Integral d4k/(2pi)^4(k²+M²)^(-7/2)=Gamma(3/2)/[L Gamma(7/2)M³]=4/(15LM³). Actual mchi/M=1.4915e-9 makes the factor2 continuation envelope very loose. |
| Inclusive spin/color/phase space | Passed | Per-label amplitude<=4Bloop mchi³/M³.13×12²×2×2²=14976<32768 final labels; the Goldstino is a zero overcount in this class. Phi3<=mchi²/(256pi³), and1/(2mchi) times32768×16 gives512². Initial-spin averaging/identical-particle factors can only reduce the bound. |
| One-loop reducible/LSZ pieces | Passed for this class | The tree transition vanishes. Neutral adjoint-scalar exchange needs both a generated chi-lambda-scalar vertex and generated scalar-two-unbroken-vector vertex, because neither relevant tree vertex exists. Its two-loop exchange is not covered. |
| All-body/all-order lifetime | Not addressed by this bound | Light Ward/phase radiation, higher-loop reducible channels and UV/nonperturbative symmetry violation are separate obligations. |

The box power count was reconstructed independently: nB+nF=4 with nB-1 bosonic gauge vertices gives r^(-2nB-nF+nB-1)=r^-5. A two-boson/one-fermion seagull triangle also gives r^-5. Two derivatives give r^-7. The combinatorial256 and bundle512 constants are conservative absolute bounds, not empirical fitted Wilson factors. Matrix rotations do not enlarge the norms. A pole mass or scalar mixing denominator is not secretly substituted for a charged propagator gap.

## Fresh finite execution and physical result

`reconstruct_bound.py` uses TP03 `current.assemble` directly, not the bound author's `build_model`, `ext_basis`, charged masks or Takagi columns. Its U1 generator is constructed as d/sqrt30, and its fermion masses/eigenvectors come from MFdagMF. It independently reproduces the xi1 gap within1e-14relative. The remaining finite arithmetic was reconstructed from the written constants rather than copied from the result fields.

    c7_eff_upper = 6606060.610293782,
    mu = 18170662.1117420 GeV,
    Mcharged = 670467.21000694 GeV,
    Gamma_Goldstino_photon = 5.65729502984e-45 GeV,
    Gamma_hard_upper = 6.05243684583e-47 GeV,
    Gamma_hard_upper/Gamma_Goldstino_photon = .01069846422,
    tau_retained_lower = 1.15115905400e20 seconds,
    survival_retained_lower(13.8Gyr) = .996224047788.

This agrees with the author's finite result, including all512/phase-space factors. The one-age coefficient budget is about1.042e9; the leading hard majorant is smaller by a factor157.7 in amplitude. It also lies below the separate99%-survival budget. All9 reconstruction controls pass;0.013seconds,46.2MB observed RSS, one numerical thread. Its v2 record validates. The author's run_001 manifest also validates, with the exact pre-addendum proof preserved.

The safe scientific statement is that the specified Ward partial plus the **entire bounded leading hard two-vector class** permit a long lifetime at the explicit benchmark. This closes the prior unbounded dimension-seven-coefficient objection at that order. It does not infer a selected cold population or establish an all-orders total lifetime. The cheapest remaining implication is to add the explicit soft/Ward completion and any leading light-exchange channel, then retain perturbative-order/UV/gravity assumptions in the final physical statement. The companion cold-state author is independently deriving that light completion; its result is not assumed here.

## Provenance

This reviewer authored the earlier angular/radial matching, not the photino pole, decay selection or hard bound. The parent supplied the target benchmark and the existence of an expected loose majorant, so this is a fresh constrained review, not a blind session. Critical propagator, topology, derivative, integral, inclusive-width and unit steps were reconstructed before inheriting the author's verdict. The independent numerical route uses a different charge basis/mass-square eigensystem, while sharing the already-frozen canonical action. Exact proof/source/result bytes reviewed are pinned in `PHOTINO_REVIEW_INPUTS.json`; numerical execution inputs and before/after hashes are separately in `run_bound_review/manifest.json`.
