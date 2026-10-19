# Claude handoff for the cold energy particle model

19 October 2026. From Codex to Claude, at the user's request.
Research checkpoint: **CE-FM093 / CE-NONLINEAR-ORIGIN-2026-10-19**.
Assessment base: `e54c33252909e38a529a69f7adac265e37b54cb4`.

**The theory is not closed.** The current work derives several conditional
states and nonlinear responses, but no physical state yet selects the occupied
acceleration dipoles, rational saturation and universal gravitational
normalization together. Do not describe the compression result below as that
missing derivation.

The user's next physics request was:

> Keep going and derive a physical scalar-baryon state that selects the occupied
> dipole spectrum, nonlinear saturation, and universal gravitational
> normalization from the original particle model, including the full
> acceleration response.

The user then requested this handoff and push. No new physical-state result was
established after CE-FM093. Continue from that checkpoint, not from an assumed
solution to the latest request.

## Start here

The supporting research was untracked in the shared working tree. It is included
as a portable, byte-pinned snapshot beside this handoff in
[`claude_handoff_2026_10_19/`](claude_handoff_2026_10_19/).
The archive includes the actual model bytes used, which differ from the
pre-existing tracked master file in the assessment-base commit. Extract into a
new directory; do not overwrite another checkout's master action.

```bash
python3 sol61_push/claude_handoff_2026_10_19/verify_bundle.py
python3 sol61_push/claude_handoff_2026_10_19/verify_bundle.py --extract /tmp/cold-energy-claude
```

Inside the extracted snapshot, read in this order:

1. `sol61_push/nonlinear_origin_2026_10_19/RESULT.txt` and `HANDOFF.json`.
2. `sol61_push/nonlinear_origin_2026_10_19/SELF_REVIEW.txt` and
   `VALIDATION.json` for the scope of evidence and corrections.
3. `sol61_push/shared_state_2026_10_19/HANDOFF.json` and the needed sections of
   `equilibrium/EQUILIBRIUM.md` and
   `equilibrium/static_response/STATIC_RESPONSE.md`.
4. The specific CE-FM093 route note needed for the next calculation. Do not
   reload the entire historical log as the default context.

The bundle verifier checks archive and artifact hashes, the four current
computation records' input/output bytes, and reviewed-note revisions. It is
portable and does not require Codex's installed Mathbox tools. It does not rerun
the science or certify the mathematics. Recorded scripts require the Python
libraries named in their manifests; run any reproduction to a fresh directory.

## Preserve the original model and conventions

The action uses canonical complex fields Phi and X with charges one and two,
daughter mass m and source mass M>2m, minimal gravity, and

\[
 V=m^2|\Phi|^2+M^2|X|^2+g(X^*\Phi^2+\mathrm{c.c.})
       +\lambda_{\rm tot}|\Phi|^4,
 \qquad
 \lambda_{\rm tot}=\lambda_{\rm rep}+\frac{g^2}{M^2-4m^2},
 \quad \lambda_{\rm rep}>0.
\]

Its positive-square form is

\[
 V=m^2(|\Phi|^2+4|X|^2)
 +(M^2-4m^2)\left|X+\frac{g\Phi^2}{M^2-4m^2}\right|^2
 +\lambda_{\rm rep}|\Phi|^4.
\]

After full tree threshold matching, the source-eliminated daughter contact is
`g2=lambda_rep/(2m²)` in `(g2/2) psi†² psi²`. Do not use the excess contact of
the older retained-source rotating-wave block as the matched daughter contact.
Conversely, do not keep an explicit source and subtract its effect twice.
No separate real-mediator/fermion force sector, new scalar-baryon contact,
negative gravitational mass, or fitted dipole interaction has been admitted.

The illustrative original benchmark is m=1 MeV, u*=.02,
`M=2m sqrt(1+u*²)`, lambda_rep=.00587528017, g/m=.00216800003.
Other numerical controls declare different parameters and are not this
benchmark unless explicitly mapped to it.

The desired medium law, with K=4 pi G, is

\[
 p(E)=p_{\rm sat}\frac{E}{a_0+E},\qquad
 \frac{p_{\rm sat}}{a_0}=\frac1{4\pi G}\quad(E\ge0),
\]

with the corresponding odd vector response if E is an acceleration magnitude.
A conditional TLS construction can reproduce this by inserting
`w(Delta)=p_sat a0 Delta/(a0²+Delta²)^(3/2)` and an appropriate source kernel.
That weight is a target to derive, not an occupied spectrum predicted by the
original scalar action. Actual gaps Omega, source matrix elements d, reduced
gaps Delta=Omega/(2d), stock and populations must be distinguished.

## What has actually been established

**A stable shared-state reduced functional exists.** With fixed positive scalar
and baryon masses and a declared ideal gamma5/3 baryon pressure law, the matched
daughter GP-Poisson energy has a global constrained minimum. The proof includes
quantum pressure, coercivity and prevention of mass loss. This is energetic
stability, not a complete ordinary-matter phase, formation history, unique
minimum, orbital-stability theorem or quantum-gap calculation. Numerical
stationary BVP candidates are separate from the existence proof. An exactly
decomposable gamma2 two-fluid control is a different baryon closure; do not
transfer its mode values to the gamma5/3 finite-GP state.

**The complete acceleration source is the first bottleneck.** For a common
uniform Newtonian field, the internal mass dipole vanishes after including
baryon recoil and removing the total COM. A heavy freely translating host is
not a fixed anchor: its small displacement times its large mass remains in the
source. Source-carrying internal modes exist for non-affine gravity. For the
specified COM-projected odd sine probe, fixed gapped states give an internal
source of order k² and susceptibility of order k⁴. This is not a statement
about every tidal source or every critical limit. In the exact common-profile
two-fluid control, relative modes have positive gaps but zero total linear
gravitational source pointwise. The same gamma5/3 finite-GP state has a computed
positive finite-k l1 response; its full plane-wave l3 response was not computed.

**Original particles can saturate, with a different force law.** The CE-FM093
two-orbital projection derives every contact, Newtonian, mass-polarization and
complete finite-host source term from explicit orthonormal spatial orbitals.
The fixed-N Hilbert space has dimension N+1. Generic finite-matrix saturation
has deficit A/E², and the coherent two-mode GP approximation has the same
power. A simple gapped parity-symmetric ground state has an analytic odd
zero-field response, unlike the rational target's E|E| term. These transitions
share one particle inventory; they are not separately stocked TLS sites. The
Gaussian continuum truncation, baryon support, omitted modes and valid bias
window have not been certified.

**The rational shape has a genuine but different canonical origin.** In an
ideal harmonic baryon core, a classical isothermal tracer cloud has
`Q=sum m r_i²/(2L)`, `a=kappa0 L` and `Q0=3NT/(2a)`. Canonical phase space gives

\[
 Q_0-\langle Q\rangle_E=Q_0\frac{E}{a+E},\qquad
 F_{\rm conn}=-Q_0[E-a\log(1+E/a)].
\]

This comes from an actual Gamma distribution of Q. Q is a compression moment
conjugate to isotropic gravitational curvature, not the uniform acceleration
dipole. The baseline source was not removed by the connected subtraction.
An isolated adiabatic cloud gives a one-half deficit exponent; a finite passive
heat receiver gives exponent `1-C_s/[2(C_s+C_b)]`. Its actual quantum source
line is `2 hbar omega`, with a separate thermal population contribution.
The one-particle quantum width eventually scales as E^-1/2. Many-particle MB
formulas cannot be extrapolated through degeneracy/contact domination.

A finite Newtonian core alone is not a globally confining canonical trap.
`FINITE_CORE_WINDOW.md` derives an explicit incomplete-gamma error bound for a
position-conditioned cloud; at depth parameter x0=10 its uniform absolute
normalized error is below .001082. That conditioning does not supply a
dynamical trapping/escape or thermalization mechanism. In a uniform core,

\[
 4\pi G\,\chi/V=\frac32(\rho_d/\rho_b)\langle r^2\rangle_0/L^2.
\]

Thus gravitational restoring scales do not fix the coefficient without state
selection, even before the acceleration-versus-curvature operator mismatch.
A separate repulsive-contact TF comparison predicts an E^-2/5 compression
deficit. Only the reduced TF constants and scaling are established; no whole
nonlinear continuum branch or full-functional error theorem was computed.

**A concrete occupied-spectrum mechanism was derived conditionally.** Disjoint
mutual-nearest-neighbor pairs in a declared 3D Poisson baryon snapshot have
intensity `2 pi n_b² r² exp[-9 pi n_b r³/4] dr`, pair density `8n_b/27`, and
fixed-level gravitational tunneling exponentially small in separation. The
resulting available soft tail is log-cubic, with finite inverse-gap moments;
it is not the target universal power. The joint physical source measure keeps
orientation, packet widths and full baryon recoil. Its uniform dipole is zero.

Original onsite contact permits a conditional hard-core occupation trace,

\[
 f_1=\frac{2z\cosh(\beta J)}
 {1+2z\cosh(\beta J)+z^2e^{-\beta V_{LR}}}.
\]

Here the loading diagonal E_b(r), entering z, includes the other baryon's
projected potential shift. The T=0 single-occupation chemical window has width
`V_LR+2J`; the original attraction `V_LR~-Gm²/r` can close it as J decreases
exponentially. Onsite repulsion does not force one scalar per pair. Capture,
exchange, host lifetime, tides and finite inventory remain to be calculated.
The same-species contact supplies conditional dipole-phonon noise proportional
to Omega^5, describing internal relaxation rather than capture. The gravitating
homogeneous bath is Jeans unstable in the infrared; this is only a stable
supported/finite-patch phonon window.

**Microscopic gravity does produce real soft bound levels.** Including the
two-daughter Coulomb attraction gives `E_n=-B/n²`, `a_B=2/(m alpha_G)` and
`B=m alpha_G²/4`. A local source produces S waves with
`|v_n|²=g²m alpha_G³/(32 pi M n³)`. The continuum tends to
`J*=g² alpha_G/(16 pi M)`. Bound accumulation cancels the spurious infrared
logarithm from a continuum-only calculation. At the 1 MeV benchmark, leading
bare-source bound overlap is about 5.30e-134, a_B about 5.88e31 m and
hbar/B about 5.85e67 s. These are not capture rates. The COM-centered odd mass
source of two equal positive daughter masses is identically zero at every
wavelength; even tidal response is allowed.

## Evidence and exact revisions

CE-FM093 has four current completed, validated runner records:

| Route | Current record | Finite scope |
| --- | --- | --- |
| Canonical response | `canonical_response/run_001` | 104 controls |
| Particle saturation | `particle_saturation/run_004` | 88 controls, ten N<=12 matrices |
| Coulomb spectrum | `gravitational_spectrum/run_002` | Declared spectrum, source, threshold and benchmark checks |
| Occupied landscape | `occupied_landscape/run_004` | Geometry, Coulomb WKB/LCAO, source, loading and bath checks |

Paths in this table are relative to `sol61_push/nonlinear_origin_2026_10_19/`.
The four main routes have focused independent in-session reviews, and six
note/review byte relations are checked. These are not external refereeing or
interval proofs. Historical failed and superseded runs are preserved; do not
refresh their manifests to match changed current code. The finite-core
supplement is an analytic bound with illustrative numerical values, not a
fifth runner experiment.

The master source actually used has SHA256
`c81b4a3136d433a2b7a0bf06ec87f61389b8e5a73da6c7603a6b264dda0bbe43`.
The bundle contents and checkpoint records pin every included byte.

## Next executable work

1. **Derive the complete acceleration response before a spectrum fit.** State
   the actual baryonic action/material state, which bodies are free or
   supported, the metric source and the measured observable. Remove only the
   total COM; retain the host/support/receiver source and recoil. Calculate
   both the affine-field limit and finite-wavelength response, with the order
   of static, long-wavelength and critical limits explicit. A subsystem
   displacement alone does not meet the target.
2. **Choose and certify one physical shared state.** If continuing the finite-GP
   candidate, establish that branch's constrained Hessian and its own coupled
   scalar-baryon modes, including the free surface/tail. Account for the
   material closure and preparation rather than relabeling a chosen EOS or
   fixed mass ratio as an action prediction. A compact energy-truncated
   collisionless cloud is an untested alternative to the nonconfining global
   canonical trace; its occupation protocol still needs derivation.
3. **Derive occupation and nonlinear response in that same state.** Compute
   capture/exchange or initial-state evolution with finite conserved stock and
   energy. Distinguish available modes, populated sectors, transition
   strengths and internal relaxation. Include leakage/escape before claiming a
   two-mode saturation window or an occupied rare-gap tail.
4. **Derive normalization without imposing it.** Keep inventory, entropy,
   geometry and receiver variables visible through Poisson matching. If the
   coefficient still varies with these inputs, report the first missing
   selection equation. A restoring frequency proportional to sqrt(G rho) is
   insufficient. An exact rational law needs a source-carrying soft/critical
   family outside the bounded isolated-gapped class; a finite-window claim
   instead needs predicted cutoffs and an error interval.

Do not rerun the already obstructed finite gapped TLS/GP construction with the
same assumptions and expect an exact rational cusp. Do not turn the
compression formula into acceleration polarization by renaming its source.
None of the scoped restrictions excludes every phase of the original model.

Earlier source-normalization, transport, cooling, stock, spin, ARGON convergence
and halo-fit obligations remain open; CE-FM093 did not retest or repair them.
Use bounded local calculations with exact source/input pins, preserve failures,
and perform independent audits before a closure claim. Heavy simulations,
source-action/manuscript changes, publication, automation/queue changes and
messages to other chats were outside the research scope. This user request
authorizes publishing this handoff and its supporting snapshot to the Git
remote; it does not assert that Claude has already run the next calculation.
