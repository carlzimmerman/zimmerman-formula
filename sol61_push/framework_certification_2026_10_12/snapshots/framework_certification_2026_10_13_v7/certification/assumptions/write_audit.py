from pathlib import Path
import json,hashlib,collections
out=Path('sol61_push/framework_certification_2026_10_12/assumptions'); d=json.loads((out/'assumption_register.json').read_text()); byid={e['id']:e for e in d['entries']}
def ref(i):
 s=byid[i]['sources'][0]; return f"{s['path']}:{s['line']} [sha256 {s['sha256']}]"
counts=collections.Counter(e['classification'] for e in d['entries'])
text=f'''FRAMEWORK-CERT-2026-10-12: framework assumptions and closure-boundary audit
Primary verdict: incomplete, with the smallest missing implication.
Normalized target: certify that the current framework's own specified dynamical equations, without inherited Lambda-CDM background/initial-spectrum/supply functions or standard MOND comparator assumptions, produce a healthy conserved theory, the galaxy profile as a derived attractor, consistent metric lensing, and the required observations. The stronger requested whole-theory/TOE closure also includes the declared quantum and Standard-Model obligations.

Provenance
Base checkpoint supplied by orchestrator: {d['base_git']}.
Observed HEAD: {d['observed_git_head']}.
This is a dirty shared-checkout snapshot. Source identities below are SHA256 of actual bytes, not inferred from HEAD. No source files outside this agent's assumptions directory were modified. No new cosmological fit, no raw-data reanalysis, no compiler run by this bounded agent. Existing results.json and current theorem source were inspected. Exact statements, source excerpts, line locators and all 16 source hashes are in assumption_register.json. This is a bounded source audit, not an exhaustive repository audit or external scientific referee review.

Register coverage
{len(d['entries'])} records, including the nine explicit v2 axioms and all 18 exact Lean theorem statements.
Category counts: {dict(counts)}.
The category 'independently proved math' denotes kernel-checked mathematical implications independent of extra physical axioms, not an independent empirical review. Source-reported stress no-go evidence not itself formalized in this package is deliberately classified as an open verification/dynamical obligation.

Exact dependency graph
A1 + nonnegative G*rho_DE -> scale_squared; additionally adopted Lambda normalization and c!=0 -> vacuum_coefficient; choosing kappa=1/2 -> half_kappa_32pi.
The converse does not select kappa: coefficient_family exhibits a solution for every kappa. Thus 32*pi is conditional on fitted kappa, not a derivation of that fit.
A2 + ideal circular-orbit/deep-law premises -> baryonic_quartic.
A2 + A7 spherical Newtonian reconstruction -> target_mass_unique/sufficient and tail results. These uniquely reconstruct enclosed mass AT A RADIUS, not the temporal transport law.
Chosen target + mass supply -> finite-supply tail bound; neither catchment partition nor physical boundary dynamics is derived.
Chosen component exchanges -> exchange_conserves_total; zero-divergence receiver hypothesis -> passive_vacuum_no_exchange. Neither theorem supplies a reservoir field, stress tensor, metric compatibility or action variation.
Fixed-source response-energy coefficients -> nonnegative scalar energy; this does not establish global coupled gravity health or an attractor.
A3/q + inherited background + EH input spectrum/growth + turnaround census/retention + scorer continuations -> tested cosmological likelihood. Both improvements and failures using this chain remain conditional.

Decisive source locators
Explicit v2 law premise: {ref('A2')}
Inherited abundance: {ref('B-abundance')}
Inherited dynamical background: {ref('B-background')}
Current target-in settling: {ref('O-selector')}
Same-action receiver gate: {ref('O-receiver')}
Current 'forced form' overclaim: {ref('O-uniqueness')}
18-theorem source: {ref('LEAN-scale_squared')}

Smallest missing implications, in dependency order
1. R0/R3: supplied microscopic degrees of freedom plus one specified action -> a non-target-derived transport operator whose profile is an attractor. Current drift inserts rho_ph, and rho_ph is computed from nu. Formally certifying that drift certifies the inserted target, not its derivation. A conservative static energy minimum does not show attraction. The attractor test needs the existing declared ICs and each separate footing. Source: {ref('G-no-target')}.
2. Bound/phase selection plus reciprocal force -> action Noether identity for ALL evolving components. Current 1_B 1_C masks are prescriptions. No action and reaction completion is supplied. Exact imbalance and reaction tests are frozen in CFG678 B1 / CFG679 M2a. Source: {ref('O-bound-switch')}.
3. Same action -> named receiver field with signed exchange, two-sign energy ledger, and a well-posed coupled initial-value problem. The v2 Q>=0 hand-off and ghost-condensate sketch are not such a completion; the contract explicitly requires import as well as export. Abstract cancellation of Q and -Q cannot fill this leaf. Source: {ref('O-receiver')}.
4. Same healthy metric/source equations -> lensing, c_T=1, Cassini and EFE-blind dynamics. Fixed-source convex positivity supplies none of the gravitating metric coupling. Adding a conformal non-lensing scalar fails the tested M3a gate; this excludes the named construction, not every possible coupling. Source: {ref('O-lensing')}.
5. Same closed evolution -> framework background and perturbations, transport-derived catchments/retention and explicitly justified initial/boundary data -> nonlinear predictions and absolute raw-data likelihoods. Replacing imported functions by undefined symbols does not supply this implication. Source: {ref('O-cosmology')}.
6. Additional selection principles -> kappa, abundance, vacuum tie and law-shaped coefficients. The present relation plus Lean algebra does not select them. Source: {ref('O-normalization')}.
7. Passing held-out observations and the declared E1-E3 obligations. Nov/Dec data are pending; Lean cannot prove what unreleased observations will be. The framework-only cosmological age is also not derived merely by freezing t<=13.8 Gyr. A provisional CFG679 pass that permits S8 PENDING is narrower than whole-theory closure. Source: {ref('O-pending')}.

Audit of the claim 'forced form'
MECHANISM_JOINT section 5 asserts CFG541/544/638 are 'the forced form, not one option.' Its stated no-go premises are local, first-order, spherical and constants {{G,a0}}; its catalogue contains 15 candidates. Neither restricted class exclusion nor failure of those 15 provides an exhaustive quantification over permitted nonlocal/history-dependent dynamics. No uniqueness theorem for the drift/phase/receiver operator is supplied. The exact smallest gap here is 'every admissible completion satisfying the framework postulates has the prescribed operator.' It is missing.
Even uniqueness of a target does not imply uniqueness of evolution: as an algebraic counterexample to that inference alone, xdot=-x and xdot=-2x share the equilibrium x=0 but have different rates. This is not proposed as a physical halo model; it isolates the invalid inference. The specification constrains possible completions; it does not establish that no one has further physics to supply.

Admission ambiguity requiring a prospective explicit convention
CFG679 M1a says 'three declared non-law initial states' but lists uniform, Plummer, and r^-2 at half AND twice the target amplitude. That can describe three families or four actual amplitudes/ICs. A candidate's frozen criteria must enumerate actual ICs and their normalizations before execution; interpreting this as three runs silently drops a stated test. This audit does not rewrite the original gate.
The A2 implementation is also finer than the summary analytic expression: current PM code repairs the derivative using DELTA=0.05, a 240001-node grid on log10(y) in [-12,12], numerical integration/interpolation and a y floor. Exact universal claims about that implementation require error/domain certification and implementation correspondence. See A2-implementation in register.

Conditional success/failure symmetry
Retain existing frozen scores for the exact constructions at their declared inputs. Downgrade both positive cluster/CMB/shear claims AND exclusions if the user's requested no-Lambda-CDM interpretation would remove inputs on which they depend. Do not erase a failed likelihood because those inputs were inherited. Do not turn a passed conditional likelihood into independent framework prediction. Do not silently change the original benchmark gate.
The scorecard's 10% departure from an S0 spectrum is a benchmark, not by itself an observational exclusion. A matched-control difference does not remove cosmological dependence:
Delta chi^2 = e^T C^-1 e + 2(s-d)^T C^-1 e.
For C=1,d=1,e=1, s=0 gives -1 and s=1 gives +1. This exact counterexample is already recorded in the dependency audit. External primary-source provenance is reported there; not independently refetched in this source audit.
Standard MOND comparators have distinct free-function, EFE and metric assumptions. The current framework explicitly adopts its own nu and explicitly postulates no EFE. Comparator exclusions cannot supply a microphysical derivation of the adopted nu. Removing standard MOND assumptions does not remove the framework's own law postulate.

Strongest safe statement
The existing package certifies 18 exact conditional mathematical deductions from expressly supplied gravity/law/conservation premises. The current phenomenological framework is specified and has conditional observational successes, failures and pending tests. The no-target dynamical selector, complete receiver/reaction system, healthy common-metric theory and independent cosmology have not been supplied. A whole-theory certification is therefore not available from these sources. The shortest productive next step is one explicitly specified candidate action satisfying R0/R1/R3, followed by its derived selector/receiver equations and formalization of that actual system; not additional algebra of the prescribed target.
'''
(out/'audit.txt').write_text(text)
# Verify locators and hashes against actual source bytes. This checks artifact integrity, not physics.
failures=[]
for s in d['source_snapshots']:
 b=Path(s['path']).read_bytes()
 if hashlib.sha256(b).hexdigest()!=s['sha256']: failures.append('changed source: '+s['path'])
for e in d['entries']:
 for s in e['sources']:
  lines=Path(s['path']).read_text().splitlines()
  if lines[s['line']-1]!=s['excerpt']: failures.append('bad locator: '+e['id'])
existing=json.loads(Path('sol61_push/gravity_architecture_lean_2026_10_12/run/results.json').read_text())
main=next(x for x in existing['cases'] if x['case']=='main')
if main['source_sha256']!=hashlib.sha256(Path('sol61_push/gravity_architecture_lean_2026_10_12/Architecture.lean').read_bytes()).hexdigest(): failures.append('old Lean report source mismatch')
verification={'source_count':len(d['source_snapshots']),'records':len(d['entries']),'locator_count':sum(len(x['sources']) for x in d['entries']),'all_locators_and_source_hashes_match':not failures,'existing_lean_main_hash_matches':main['source_sha256']==hashlib.sha256(Path('sol61_push/gravity_architecture_lean_2026_10_12/Architecture.lean').read_bytes()).hexdigest(),'failures':failures,'scope':'Integrity verification only; no new Lean compiler or astrophysical computation.'}
(out/'integrity.json').write_text(json.dumps(verification,indent=2)+'\n'); print(json.dumps(verification))
assert not failures
