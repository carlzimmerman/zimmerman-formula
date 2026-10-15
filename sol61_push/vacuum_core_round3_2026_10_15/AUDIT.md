# Evidence and authority for VC3-2026-10-15-01

This is the contemporaneous assessment of the third mechanism phase on
15 October 2026. The original target is **partially advanced, still OPEN**.
The common base is `e661d9f281726991b1076a42b835cf450578b79a`, continuing
the published second-round commit `efafb8fb2012ed49e31244a1933e30d55964c7fb`.
Later action and empirical leaves identify their own exact source revisions.
The shared checkout changed during work; actual listed input hashes, rather
than one moving HEAD, identify each computation. No executable .mathbox ledger
was present or initialized.

## Authoritative records

Proofs, declared amendments and independent derivations give the mathematical
scope. Check counts describe implemented reductions and bounded controls;
they are neither independent theorem counts nor universal proof certificates.

| Route | Current run | Executed checks | Required review or scope record |
|---|---|---|---|
| Vacuum coefficient and phase | [vacuum/run_v1](vacuum/run_v1/manifest.json) | 25 symbolic identities, 12 exact parent controls, 36 exact blend controls | [Proof](vacuum/PROOF.md), [self-review](vacuum/SELF_REVIEW.md); phase used in independently audited joined model |
| Lorentz obstruction | [lorentz/run_v1](lorentz/run_v1/manifest.json) | 10 exact identities, 3 exact parameter controls | [Independent audit](lorentz/AUDIT.md), [primary-source convention check](lorentz/LITERATURE.md) |
| Independent Lorentz matrix | [action_join/lorentz_audit_run_v2](action_join/lorentz_audit_run_v2/manifest.json) | 10 exact checks of the full six-field constitutive matrix | [Audit](lorentz/AUDIT.md) |
| Static action bridge | [action_join/run_v2](action_join/run_v2/manifest.json) | 28 exact checks plus pinned raw AG4 comparison | [Report](action_join/REPORT.md); root reconstructed the dictionary |
| Critical soft core failure | [core/run_v3](core/run_v3/manifest.json) | 27 exact checks and a high-precision trial quadrature | [Amendment](core/AMENDMENT.md), [independent audit](core/AUDIT.md); analytic family bound supplies the negative direction |
| Subcritical stiff core | [stiff_core/run_v2](stiff_core/run_v2/manifest.json) | 15 exact checks, 3 floating continuation controls | [Amendment](stiff_core/AMENDMENT.md), [independent audit](stiff_core/AUDIT.md) |
| Fixed-core Maxwell interface | [interface/run_v2](interface/run_v2/manifest.json) | 32 exact checks | [Amendment](interface/AMENDMENT.md), [independent audit](interface/AUDIT.md) |
| Counted dynamical/KKT lift | [dynamical_lift/run_v2](dynamical_lift/run_v2/manifest.json) | 25 exact checks, 2 high-precision relative-energy quadratures | [Proof](dynamical_lift/PROOF.md); root reconstructed the convexity and outside inequality |
| Exact finite-stiffness halo | [stiff_halo/run_v1](stiff_halo/run_v1/manifest.json) | 16 exact identities and a degree-14 Bernstein positivity certificate on the whole interval | [Independent audit](stiff_halo/AUDIT.md), [relativistic scope](stiff_halo/SCOPE.md) |
| Independent finite-stiffness check | [dynamical_lift/stiff_halo_audit_run_v2](dynamical_lift/stiff_halo_audit_run_v2/manifest.json) | 17 orthogonal exact checks | [Independent audit](stiff_halo/AUDIT.md) |
| Critical stiff moving pair | [critical_stiff/run_v1](critical_stiff/run_v1/manifest.json) | 24 exact checks, Maxwell benchmark and 3 floating finite-field IVPs | [Independent audit](critical_stiff/AUDIT.md); qualitative branch theorem is distinct from floating diagnostics |
| Joined critical pair/wall/Maxwell | [critical_interface/run_v1](critical_interface/run_v1/manifest.json) | 37 exact checks, including rational contraction, traction and radial coercivity bounds | [Radial audit](critical_interface/AUDIT.md), [action audit](critical_interface/ACTION_AUDIT.md) |

The final joined proof is SHA-256
`ec4f77a2adbf9a8f35c400103b4ab82cd872c3ef2c78c0c7b5a251ba21ebbbc3`;
both independent audits reference those exact bytes. The root also checked
the moving finite-density Gauss trace, gravity/electric operator cancellations,
common trace bound, current enthalpy inertia and area-wall gravitational work.
All agree at the declared static and radial quadratic hybrid scope.

## Historical records retained

- `action_join/run_v1`: failed symbolic logarithm simplification without the
  needed positive chart. Version 2 fixes the declared assumptions.
- `action_join/lorentz_audit_run_v1`: failed proof locator after mathematical
  checks; version 2 uses the correct path.
- `dynamical_lift/run_v1`: failed symbolic square-root assumption; version 2
  supplies the positive-root certificate.
- `core/run_v1` and `core/run_v2`: their live proof input was subsequently
  edited, so current-input validation correctly fails. Exact original bytes
  survive as `core/DRAFT_PROOF_V1.md` and `core/DRAFT_PROOF_V2.md` and match
  the respective recorded hashes. Version 1 also had a parenthesis bug;
  version 2 completed a preliminary proof. Neither is authoritative.
- `dynamical_lift/stiff_halo_audit_run_v1`: failed a transcribed factor of
  three in the draft audit's central source, while the root construction was
  correct. The old input is archived as
  `dynamical_lift/inputs/STIFF_HALO_AUDIT_DRAFT.md`; its hash matches. The
  final audit and version 2 correct the transcription.
- `stiff_core/run_v1`: hash-valid completed record with incorrectly declared
  NumPy version 1.26.4; the actual runtime was 1.26.2. Version 2 corrects the
  metadata and reexecutes; the historical manifest is unchanged.
- `interface/run_v1`: hash-valid completed record in the earlier bare-density
  inertia convention. The amendment and version 2 use the inherited current
  enthalpy inertia and corrected Rayleigh bound.

The final [verification observation](verification_observation.json) records
all current manifest results and the exact preserved draft replacements.
Hash-valid failed runs remain failures. Archived-byte matches do not turn
stale preliminary runs into current evidence. No original manifest is repaired
by refreshing its hashes.

## Interpretation and remaining obligations

No single positive result proves the original physical theory. The canonical
mechanical model, subcritical core, critical stiff pair and high-pressure
phase body have different hypotheses. Only the last has the stated actual
critical two-fluid/common-wall/Maxwell radial join. Its ideal confinement,
EOSs, magnetic response and tension are inputs. Radial positive energy and
pure-electric bulk cones do not establish angular/interface hyperbolicity,
magnetic-background health, nonlinear evolution, Einstein constraints,
formation, abundance, galactic lensing or cosmology.

The contemporaneous [CFG801 dependency](EMPIRICAL_DEPENDENCY.md) is retained
as an empirical exclusion of the tested settled-only cutoff interpretation,
without rewriting the mathematical theorem or any lane's criteria. The AG4
raw stiffness residual and frozen G4 failure are also retained. The root's
[self-review](SELF_REVIEW.md) and separate-agent reviews share a model/tool
environment; they are not external peer review or formal verification.

The local [current decision](CURRENT.md) keeps the next route open with its
first discriminating calculation. Further metric, phase and angular routes
are deferred open obligations, not claimed exhausted or impossible.
