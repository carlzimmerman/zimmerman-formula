# TP02 threshold/RG result

The weak-coupling old-waterbag pressure obstruction survives every tested
RG/scale-log prescription and the calculated finite heavy-relaxation
subset. This is stronger than a naive running-coupling plug-in, but remains
partial matching: the direct finite two-loop potential and direct finite
kinetic thresholds have not been computed. No physical all-order halo
no-go or coupling selection follows. DERIVATION.md gives the exact scope.

The first consistency checks are established before improvement:

- Exact one-loop Callan-Symanzik cancellation uses the *complete* spectrum:
  beta1.partial U0=STr M^4/(32pi^2)=-Q partial_Q U1.
- All h,lambda,g,f and the canonical X field run. The canonical flat
  coordinate T runs with gamma_eff, not gammaX. The old critical g/lambda
  relation is only a Q0 comparator input and is not reset along the flow.
- Two-loop beta/gamma functions were independently reconstructed from the
  raw 49-field Yukawa tensor. Reduced-CS two-loop scale logarithms include
  the normal-valley drift through derivatives of the reduced potential.
  A missing finite matching function is not fixed by choosing a scale.

Reference trial inputs are f0=Q0=1, h0=lambda0=e and
g0=sqrt(29/200)e. The matching proxy is
Qm=sqrt(e/31+(eX0)^2), varied by eta=.5,1,2. The RG characteristics and
complete finite one-loop thresholds use 50-digit arithmetic. The central
rg2 result includes two-loop running; rg2log supplies its CS-required
scale-log completion about Qm. These are not a complete finite two-loop
effective potential or sequential low-energy EFT matching.

| e | central RG pressure X/Xmin | RG density rho/rho_* | plus finite normal relaxation X/Xmin | plus-relaxation density |
|---:|---:|---:|---:|---:|
| .01 | 1.177179 | .590403 | 1.177112 | .590209 |
| .03 | 1.177393 | .590863 | 1.176779 | .589077 |
| .05 | 1.179115 | .595863 | 1.177392 | .590845 |
| .1 | 1.191494 | .633643 | 1.185303 | .615304 |

The fixed-one-loop comparator gives1.1772996111 and.5908117662.
Every reported pressure boundary has positive U_s and positive radial
curvature W_ss. Every scheme has a resolved negative-compressibility
witness at X/Xmin=1.2. The density dictionary uses the stipulated old
waterbag and Bcurv=Uss(Xmin)/9; its unknown phase level cancels. These
columns are not physical density or acceleration predictions.
Raw result files retain diagnostic digits; they are not certified error
bounds. The finite matching table is rounded to respect its repeated
float64 spectral-gradient derivative controls.

The finite matching subset was computed from all scalar, mixed-Weyl and
vector mass-matrix Frechet derivatives, not from a radial effective mass:

    deltaUrelax=-.5[CWa^2/(120fh)+CWb^2/(60lambda^2 a^2)].

Independent polynomial matrix differences, CP-odd tadpole zeros, stencil
repeats and direct baseline-plus-finite-part derivative checks pass. This
is a gauge/scheme-dependent subset: its gauge dependence requires the
remaining genuine two-loop diagrams for a physical matched result. It
does not bound those diagrams from above or below.

The same computed heavy B shift supplies a geometric angular correction,
but that is not the whole occupied source. The matter route retains

    Omega=U_RG-omega^2 F_RG
            -.5[CWa^2/Haa+(CWb-omega^2*60b)^2/Hbb],

including its omega^4 term. It tests the native phase charge rather than
calling the old waterbag a derived microscopic coupling. See the separate
matter_coupling report for its finite endpoint and stiff EOS. Our F_RG is
only the running projected tree angular coefficient; direct finite
component two-point/derivative matching remains missing. Supersymmetry
breaking splittings were not assumed small relative to all mode masses.

Numerical scale stability is not a missing-matching bound. At e=.03 the
potential scale spread drops from2.78e-11 to2.47e-15 after the CS log
completion. Yet the separately calculated normal-relaxation subset shifts
the pressure endpoint by about6.14e-4, much more than that completed
scheme's residual endpoint scale variation. This directly demonstrates
why a tiny scale spread cannot replace finite matching.

The safe small-coupling inference is conditional. At fixed z, massive
mass squares scale as e, U1 scales as e^2, finite two-loop and occupied
normal-relaxation terms as e^4, and relative finite metric corrections
as e^2. A strict leading pressure sign therefore persists asymptotically
under a bounded matched C^2 remainder on a compact admissible branch,
allowing the known logarithms. No verified finite-e bound on that remainder
has been supplied. Quantitative derivative margins are separately recorded
by the algebra worker; they are conditions, not assumed error bars.

Eight successful v2 records cover exact CS checks, the RG/field interface,
four seven-scheme weak scans, full finite-normal matching controls and
finite-relaxation pressure roots. Input hashes and run statuses are in
VERIFICATION.json; code and commands are described in REPRODUCE.md. No
TP01 input, old theory file, Git staging area or history was modified.

The next unresolved implication is the finite reduced two-loop potential
and direct finite occupied-state derivative/current matching, in the same
gauge/subtraction convention with the already computed heavy term counted
once. Further running-only resummations cannot determine those functions.
No kappa, alpha, vacuum normalization or cosmological occupation was derived.

Independent review: the separate algebra worker reconstructed the beta
coefficients and CS/field dictionary, inspected the improvement and full
normal-gradient implementations, and independently rederived the normal
Hessian and occupied source square. Its restricted implementation verdict
is recorded in ../rg_derivation/IMPLEMENTATION_REVIEW.md, with final inputs
pinned separately. It did not independently rerun these pressure scans;
review agreement does not complete the missing physical matching.
