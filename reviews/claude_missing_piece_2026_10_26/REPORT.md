# Review of Claude's latest work: a missing connection and a false shortcut

Review date: 2026-10-26 (America/New_York). Starting checkpoint:
`6ebe8911c9b6340ec81073f396c0061896353cd3`. This is a separate review;
the live theory statements, criteria and simulations were not changed.

**Main result:** there is a useful connection to revisit: a local measure of
the cold component's multistream motion could activate *core formation* after
collapse. An older version was rejected because it activated too far inside a
halo to supply the old modified-gravity law. That particular failure does not
exclude its new role in route E. This is a conditional opening, not a derived
mechanism. The missing step is a conserving dynamical response that selects and
stabilizes the proposed core surface density.

**A concrete correction is also necessary:** PS2's bound on central
`Q = rho0 / sigma0^3` is not licensed by Liouville's theorem. Its own isotropic
Burkert progenitor has divergent maximum distribution function despite finite
central Q. The cap may be investigated as a phenomenological assumption; it
cannot be credited as a theorem-derived mechanism.

## 1. What changed in the latest work

The [current statement](../../rebuild_2026_10_22/THEORY_STATEMENT_2026-10-26.md)
uses ordinary gravity, clumping cold dark energy, and prescribed Burkert cores:

\[
\Sigma_{\rm core}=\max\left[\frac{a_0}{2\pi G},\eta(c_f)\Sigma_{\rm coll}\right].
\]

The floor is not obtained from an action. The quoted successes also depend on
halo masses, profile shape, formation history and boundary conventions. In
particular, the latest X53 lensing result postdates parts of the summary and
exposes a mass-normalization problem. Saying that only the floor's origin is
missing understates the remaining dependencies.

The three investigations here were: the floor's local mechanism, the X53
mass/profile connection, and the PS1/PS2 phase-space justification. Independent
agents read the raw artifacts; their agreement is not a proof certificate.

## 2. The useful old piece: multistream stress, with a new job

[X47](../../rebuild_2026_10_22/X47_vacuum_tethered_core_floor/README.md)
correctly excludes its local acceleration threshold. A cored halo has zero
self-acceleration at its center; the proposed threshold also suppresses the
weak linear cosmological field. Its final extension to *every* local invariant
is not established by those calculations.

A different local quantity is the kinetic stress tensor

\[
\Pi_{ij}=\rho_c\sum_s w_s(v_{s,i}-\bar v_i)(v_{s,j}-\bar v_j),
\qquad \sum_s w_s=1.
\]

For an exactly cold single stream this vanishes. Several streams with
noncoplanar velocity offsets can give full-rank stress, including at a core's
center where acceleration vanishes. This is collisionless random-motion
stress; it need not describe a collisional gas. Its emergence and anisotropy
after shell crossing are established kinetic phenomena, not a new discovery
([Buehlmann and Hahn 2019, sections 1–2](https://doi.org/10.1093/mnras/stz1243)).

The repository already has the relevant lead:
[CFG351](../../campaign_fresh_gravity/CFG351_cold_threeaxis_switch/README.md)
tested a full-rank velocity-covariance switch. Its principal edge failure was
that activation stopped around `0.232 r_ta`, while the old law needed to extend
to turnaround. [CFG352](../../campaign_fresh_gravity/CFG352_caustic_edge_vs_data/README.md)
confirmed that failure against lensing. In route E, ordinary halo gravity
continues outside the region where core physics operates. Therefore the old
edge test does not by itself reject a switch for *inner core processing*.

The limitations survive the change of purpose:

- CFG351's original switch formally exerts no force on the cold component. It
  does not redistribute mass or set a floor.
- Its sharp rank test turns on for any nonzero isotropic primordial dispersion.
- Full rank does not universally imply a bound halo; substructure and unbound
  overlapping streams can produce it. Four streams are necessary, not
  sufficient, for rank three.
- The specific second-caustic boundary assumes a model for nonradial velocities.
- A field model must derive an appropriate kinetic/coarse-grained stress and
  its response; one cannot simply identify it with an arbitrary wave stress.

### A small independent check of the missing variable

For an isotropic, baryon-free, self-gravitating Burkert halo with zero pressure
at infinity, let `x=r/r0`, `Sigma=rho0*r0`, and

\[
q(x)=\frac1{(1+x)(1+x^2)},\qquad
B(x)=2\ln(1+x)+\ln(1+x^2)-2\arctan x.
\]

The Jeans equation gives

\[
P_0=\int_0^\infty\rho\frac{GM(r)}{r^2}\,dr
=C G\Sigma^2,\qquad
C=\pi\int_0^\infty\frac{q(x)B(x)}{x^2}\,dx
=0.82610703600191.
\]

At the proposed floor,

\[
P_0=\frac{C}{4\pi^2}\frac{a_0^2}{G}
=0.00523138391894\,\rho_\Lambda c^2
\]

on the canonical footing `a0^2=G rho_Lambda c^2/4`. The final equality must not
be transferred to the alternative footing as an identity in the same Lambda.
The first pressure identity is shape-, boundary- and anisotropy-dependent;
baryons add to it. The untruncated Burkert model is a diagnostic with divergent
total mass but a convergent central-pressure integral, not a finite halo model.

This calculation supplies a local stress scale that acceleration alone misses.
It does **not** derive its selection. For example, the smooth diagnostic

\[
F(\Pi)=\frac{\det\Pi}{P_*^3+\det\Pi},\qquad P_*>0,
\]

is zero on the exactly cold stream, ideal sheet and ideal filament examples,
and positive on the tested three-dimensional stream example. It is invariant
under boosts and rotations. The finite stream tests use unit mass density,
so their velocity covariance equals their pressure tensor in test units.
But `P_*` and the function itself would be new
assumptions; choosing them to recover the floor would be reverse engineering.
No action or force law for this F was proposed here.

Finite primordial random motion remains a stringent check: for nonrelativistic
freely redshifting velocities, `rho sigma^2` grows backward as `a^-5`. A stress
gate that is small today can be active early. A rank/amplitude diagnostic must
pass an actual allowed-primordial-dispersion test before any growth claim.

There is also a direction-of-evolution question. At fixed mass in a homologous
virialized family, `Sigma ~ R^-2` and `E ~ -GM^2/R ~ -sqrt(Sigma)`. A state
below the floor needs energy export to contract upward. A denser initial cusp
could expand downward and stop at the floor. These are different claims.
Energy may move into outskirts or ejecta; an external sink is not automatically
required. Neither sign nor a stable stopping condition follows from Jeans
equilibrium.

[CFG461](../../campaign_fresh_gravity/CFG461_settling_temperature_mechanism/README.md)
already excluded a shortcut: treating vacuum stress as a boundary pressure
leaves the SIS velocity dispersion free. That was a normalization/boundary
failure, not a test of post-multistream activation of route-E core physics.

## 3. PS2: central Q is not the conserved phase-space maximum

The exact assertion under audit is in
[PS2 criteria, lines 25–40](../../rebuild_2026_10_22/PS2_theorem_phase_space_cap/FROZEN_CRITERIA.md):
that collisionlessness licenses `Q_core <= Q_prog`, with Q taken from one
half-mass Burkert progenitor's central Jeans moments.

**Verdict: incomplete; the proposed Q inequality is not established by the
stated theorem.** The identification of finite Q with the distribution-function
maximum is false for the stated progenitor. Liouville conserves
the fine-grained distribution function along collisionless trajectories.
It does not identify its maximum with `rho/sigma^3`, or the maximum over all
ancestral material with the central moments of one selected progenitor.

There is a decisive counterexample to that identification inside the proposed
profile family. For a
self-gravitating isotropic Burkert center,

\[
\rho(r)=\rho_0-\frac{\rho_0}{r_0}r+O(r^2),\qquad
\Psi_0-\Psi(r)=\frac{2\pi G\rho_0}{3}r^2+O(r^3).
\]

Writing `A=rho0/(r0 sqrt(2 pi G rho0/3))` gives
`rho(Psi)=rho0-A sqrt(Psi0-Psi)+O(Psi0-Psi)`.
Eddington inversion therefore yields

\[
f(\mathcal E)\sim
\frac{\sqrt{3\rho_0}}{8\pi^{5/2}r_0\sqrt G}
\frac1{\Psi_0-\mathcal E}.
\]

Its supremum is infinite. Meanwhile the Jeans integral above gives finite
`sigma0^2 = C G rho0 r0^2`, hence finite Q. For `G=rho0=r0=1`,
`sigma0^2=0.8261070360` and `Q0=1.3318199569`.
An independent high-precision inversion at turning radii `1e-2,1e-3,1e-4`
confirmed the divergence coefficient: the ratios to the asymptote were
`1.00016296, 1.00000056, 0.999999995`.

This asymptotic is also known: [Mashchenko and Sills,
astro-ph/0409605v1](https://arxiv.org/abs/astro-ph/0409605v1), Appendix A,
equations A2–A4, explicitly use the Burkert `(1-E)^-1` behavior. The source
agrees with the independent derivation; this review claims no novelty for it.
A sharp outer truncation requires its own admissible distribution-function
completion. Any admissible isotropic completion preserving the stated central
terms retains the local divergence. A finite primordial phase-space bound
would require regularizing that inner profile, rather than treating its
finite Q as the bound.

This does not prove the numerical PS2 cap fails all data. It proves that its
current justification is an additional assumption. Stronger collisionless
mixing constraints require actual distribution functions and an assembly
history. Those are not supplied by a Jeans second moment alone.

## 4. The floor also needs a baryon–halo relation

[X38's implementation](../../rebuild_2026_10_22/X38_a0_surface_density_halos/x38_sd_halos.py)
imports the SPARC-calibrated EM1 relation `log M200 = a+b(log Mb-10)`
and fits stellar mass-to-light ratios. The relation was calibrated with NFW
halos, then transferred to a different cored family. It is not an output of
the surface-density floor.

One can expose the missing factor algebraically. For a floor Burkert halo,
`M(r)=pi Sigma r0^2 B(x)`. Let `h_v=max B(x)/x` and `c=R200/r0`.
If the circular-speed maximum lies inside the truncation radius, its
**halo-only** speed satisfies

\[
\frac{V_{h,\max}^4}{GM_ba_0}
=\frac{M_{200}}{M_b}\frac{h_v^2}{2B(c)}.
\]

The floor cancels one scale, but leaves the mass ratio and concentration.
This is not an identity for an observed baryon-plus-halo flat speed; it is
already enough to show why the floor alone cannot imply the BTFR or the RAR.

[X53](../../rebuild_2026_10_22/X53_outer_lensing_law_vs_halos/README.md)
makes this dependency observationally consequential. A common halo-mass shift
of about `+0.35 dex` on the inner sample or `+0.50 dex` on all radii removes
most of the reported lensing discrepancy. Our independent reconstruction of
the covariance statistic reproduced the stored chi-squares to `2.3e-13`.
The common mass shift removes 79.6% / 71.5% of the all-radius gap on the
canonical / alternative footings. Extending the halo instead of sharply
truncating at R200 removes about another 60 in chi-square; residual differences
remain and environment/isolation leakage is a stated caveat.

These are conditional diagnostics of the tested profile and mass assignment,
not a general rejection of ordinary gravity or a validated rescue. The next
comparison needs one consistently calibrated cored halo family across rotation
curves and lensing, with its outer boundary and sample selection modeled.
Simply making every halo isothermal repeats an already failed cluster route;
the active IJ1 lane also does not supply the Lambda normalization.

## 5. What the next mechanism must actually establish

The precise research target is **post-collapse transport with a derived
stopping rule and baryonic normalization**. A useful first action calculation
must demonstrate all of the following, without inserting the desired profile:

1. The modification is negligible in the permitted early cold state, including
   finite primordial dispersion, and need not suppress linear self-gravity.
2. Its kinetic stress/activation variable follows from the cold field's degrees
   of freedom with a specified coarse-graining regime.
3. Its energy and momentum transfer has the correct sign and conserves the
   total ledger; the core has a stable endpoint near the floor. The scope must
   state whether this is a stopping bound or a two-sided attractor.
4. The same dynamics fixes the baryon–halo amplitude/size relation and leaves
   enough outer gravitating material for lensing.

Ordinary collisionless gravity plus Lambda does not enforce a universal floor
by itself. The Newtonian Vlasov–Poisson system, including `-Lambda c^2` in
Poisson's equation, admits the homology
`f_lambda(x,v,t)=lambda^-3 f(x/lambda,v/lambda,t)` and
`Phi_lambda(x,t)=lambda^2 Phi(x/lambda,t)`.
It sends `M -> lambda^3 M` and `Sigma -> lambda Sigma` at fixed Lambda.
Thus a universal nonzero floor over unrestricted initial data requires a
homology-breaking physical input. Fixed cosmological initial conditions or
additional field scales restrict this argument; it is not a no-go theorem for
every completed cosmological theory.

## Evidence and limitations

- Main stress computation: `check_stress.py`, `stress_contract.json`, and
  `run_stress_checked/manifest.json`. Eight finite checks passed; adaptive
  quadrature and a separate logarithmic Simpson integral agree. The manifest
  validates with current source hashes. No formation evolution was run.
- The first run, `run_stress`, failed while serializing a NumPy boolean to
  JSON. Its logs and original source are preserved. Converting check values
  to Python booleans fixes serialization; no mathematical tolerance changed.
- Lensing audit reconstructs scoring from released covariance and saved model
  predictions. It does not independently regenerate the halo profiles or fit
  a new halo family.
- Burkert inversion: `check_burkert_df.py`, `df_contract.json`, and `run_df/`.
  This preserves a reproducible version of the independent reviewer's
  calculation; the analytic asymptotic, not three numerical samples, proves
  the distribution-function divergence.
- Primary literature was checked for the kinetic-state interpretation and
  Burkert distribution function. The proposed new *role* for the old switch
  is our inference, not a result supplied by those papers.
- Audit provenance and inputs are pinned separately. No manuscript, shared
  status, or running research lane was modified; no new long job was launched.
- Independent review checked the pressure coefficient and conversions using
  a separate enclosed-mass quadrature, and checked the final phase-space and
  homology arguments. Mathematical proofreading covered this report's new
  equations and definitions; no existing research text was edited.

The core mechanism remains open. The review identifies a reusable ingredient,
a specific false theorem shortcut, and the extra normalization condition that
the mechanism must satisfy.
