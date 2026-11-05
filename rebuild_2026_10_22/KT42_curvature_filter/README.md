# KT42: useful new tests, no surviving response yet

Publication summary and spending gates: [Results and next steps](RESULTS_AND_NEXT_STEPS.md).

The KT41 audit identified one exact response-law application not found in its
searched local texts and two useful closure applications. All three were
executed, keeping the baryon sources, original acceleration footings and
observational cuts fixed. The generic mechanisms are prior work; no global
novelty or proof of absence from every repository file is claimed.

The new response smooths only curvature, retaining the unfiltered auxiliary
gradient and the full action variation:

\[
\bar H=\operatorname{Hess}(e^{a^2\Delta/2}\psi),\quad
E=|\nabla\psi|^2 R\!\left(
\frac{|\nabla\psi|^2}{a_0^2}
+\left[\frac{\ell^2\bar H:\bar H}{a_0^2}\right]^{9/8}\right),
\qquad \ell=3\,\mathrm{kpc}.
\]

`DERIVATION.md` gives the complete equations and `mw/filtered_model.py` their
finite variational implementation. The physical Gaussian width a is a new
declared trial parameter, not a derived constant. Higher-derivative generalized
QUMOND and nonlocal filtering are existing architectures.

## What the new calculation establishes

1. **Curvature smoothing has a severe scale conflict in the unchanged tests.**
   The regular Solar quadrupole crosses its ceiling near a=.5471pc (canonical)
   and .5238pc (alternate). At1pc it exceeds the ceiling by7.18/8.31; at100pc
   and above it is close to7.88/9.06. These are bracketed numerical crossings,
   not a proof of one global allowed interval: the function is nonmonotone.

2. **Small smoothing fails the MW force test across every historical pass.**
   All52 original primary-pass baryon cells give outward force at R12,z.3kpc
   for a = 0, 0.1, and 1 pc:156/156 cases, corroborated by468 potential differences.
   Fifty retain the primary observational passes at refinement3; none also
   has a restoring force at that point. This selection is not all1375 cells
   of the new action. In the two refined witnesses, a100pc reverses the force
   at z.3 but leaves another outward band; a300pc removes outward force only
   on the sampled R12 profile. Every sampled witness still fails strict Lh.

3. **Draco is not repaired.** At fixed Upsilon2 and uniform auxiliary eta=.01,
   W/(3M) stays negative for every sampled width through300pc, on both
   footings. At1kpc it turns positive but gives sigma≈3.07km/s, below the
   unchanged6.7km/s scalar comparison floor. Fornax, the declared size
   control, behaves differently and passes its scalar screen at300pc/1kpc.

The mechanism is explicit: sufficiently large smoothing can weaken the curvature stress responsible
for the bad galactic forces, but also removes the Sun's curvature screening.
There is no joint survivor among the sampled configurations. A Gaussian
factor bounds the former unbounded cold-fluid growth rate; bounded growth is
not stability, and a successful primary-score window is not a complete model.

![Fixed-source scale conflict](/Users/carlzimmerman/new_physics/zimmerman-formula/rebuild_2026_10_22/KT42_curvature_filter/scale_conflict.png)

## Additional Solar failure: the radial anomaly survives

The origin audit exposed a separate failure that the Cassini quadrupole alone
does not measure. At fixed positive filter width, Hbar is finite near the Sun
while the unfiltered gradient diverges. Thus x dominates s^p, giving

\[
g_A\longrightarrow a_0,\qquad g_B=O(r),
\]

for the inward monopole anomaly. The full finite-radius calculation confirms
that the returned B term cannot cancel it at the tested planetary radii.
Mars and Saturn fail both archived supplementary radial/precession screens
at a=.1,1,100,300pc on both footings: all16 cases. The precession/error ratios
are approximately9522–20255 against the archived acceptance line2. These are
ratios to archived errors, not statistical exclusion significances from a
joint fit. The exact orbit average includes eccentricity and the full B term.

Even a=.1pc, which passes the regular Cassini quadrupole comparison, fails
this separate radial screen. The field/orbit calculation retains the original
KT42 Solar mass and raw auxiliary external field; only archived orbital data,
comparison errors and the averaging formula are reused from AZ11/AZ12.
`planets/DERIVATION.md` gives two independent full-adjoint monopole integrals;
`PLANET_AUDIT.md` records their independent review. Actual-model Newtonian-null,
omitted-return and aphelion-domain controls supplement the original run.
No raw tracking data were fit and no covariance-refitted ephemeris is claimed.

## Two closure applications

For every constant isotropic quadratic Hessian correction
Delta E=alpha(tr H)^2+beta H:H, only c=alpha+beta affects the bulk equations:

\[
\Delta N=c,\qquad \Delta\Phi=-4\pi Gc\rho,
\qquad \Delta W=6\pi Gc\int\rho^2\,d^3x.
\]

The sign c<0 that reduces the bad short-wave response makes the already
outward MW force and negative Draco virial worse. c>=0 retains the positive-N
witness. Under the stated fixed-boundary/matter assumptions, this is an
analytic exclusion of the constant quadratic family, not just a sampled scan.
Nonconstant coefficients and other actions are outside that theorem.

An extra kinetic term, memory time or microscopic cutoff that leaves the
reduced static energy and matter coupling unchanged inherits the same static
failure. That implication was already in the repo. Its new quantified KT40
application requires changes of at least843.77/936.11 (km/s)^2/kpc at the MW
witness and19.3383 (km/s)^2 in the canonical Draco virial merely to reach zero.
These thresholds carry the original discretization qualifications. No newly
specified dynamical parent survived the novelty audit as a separate candidate.

## Evidence, limits and supplementary work

`verification_001/` validates13 branch manifests, including three retained
failed runs, and independently regrades48 MW rows,7152 profilepoints,156
historical-pass evaluations,18 main Solar ratios and36 dwarf rows. The
verification manifest itself also validates. Prospective contracts and exact
commands are stored beside each immutable run. `FINAL_AUDIT.md` reconstructs
the Solar/dwarf algebra independently; `endpoint/FILTER_REVIEW.md` checks the
MW adjoint and the frozen symbol. These are numerical convergence checks and
analytic reviews, not interval-certified solutions.

Solar and dwarf comparisons preserve the inherited uniform auxiliary external
field, with zero external Hessian. They are not self-consistent embeddings in
the complete Galactic tidal field. The reported Solar q is the regular l=2
coefficient, not the central Hessian of a singular point-source potential.
No relativistic completion, microphysical derivation, all-width exclusion or
full new-action baryon census is established.

`PLANET_EXTENSION.md` prospectively declared the additional orbital test.
`finish_001/` validates the expanded evidence and independently regrades its
16 supplementary comparisons; the original Cassini cut and all preceding
evidence remain unchanged. The three initial failed runs and rejected launcher
request are retained and explained rather than overwritten.
