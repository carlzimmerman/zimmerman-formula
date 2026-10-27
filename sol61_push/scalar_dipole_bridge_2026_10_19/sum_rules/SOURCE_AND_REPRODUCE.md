# Source convention and reproduction record

Checked 2026-10-19. The root mathematics is derived from the displayed
Phi/X Hamiltonian; the external source below is used only for spectral
normalization comparison. No novelty claim is made.

H. Hu, E. Taylor, X.-J. Liu, S. Stringari and A. Griffin,
*Second sound and the density response function in uniform superfluid atomic
gases*, [arXiv:1001.0772v2](https://arxiv.org/pdf/1001.0772v2).
The official current PDF at https://arxiv.org/pdf/1001.0772 was opened and
its header identifies v2, 23 April 2010; title and authors match.
Equations (2)-(3) distinguish response and structure factor via detailed
balance; Eqs. (7)-(11) give their number-normalized first and inverse moments.
Our positive force-response convention reverses the sign of their static
response to a positive added potential. Their S is per particle: multiply
by n m² for a single-species mass measure per volume, and restrict to
positive frequencies at T=0. Those translations agree with our factors.
The paper does not establish the molecular conversion corrections, the
dipole map or the rational gap moments in this packet.

Exact-version cache lookup returned zero matches in the existing ignored
`.research-cache/literature`; no new cache entry, PDF or full text was
retained. Consequently no retained-PDF SHA256 is claimed.

The root run command is recorded verbatim as an argv array in
`run_001/manifest.json`. To regenerate, invoke the installed computation-audit
`run_experiment.py` with root=this repository, contract=`sum_rules/contract.json`,
each of its five execution_artifacts as a repeated --input, a *new* output
directory and a declared results.json in that directory. The child command
is `python3 sum_rules/check_sum_rules.py --output NEW_DIRECTORY/results.json`,
with both paths relative to the repository rather than this note. Use the
full packet-relative paths from the existing manifest. Caps: 45 seconds wall,
30 CPU seconds, max-threads=1. No address-space or affinity cap was requested.

Read-only validation of the existing run:

    python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py sol61_push/scalar_dipole_bridge_2026_10_19/sum_rules/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula

Observed Python 3.9.6, NumPy 1.26.2 and SciPy 1.11.4. Four complete sectors
gave 24 operator identities, 24 spectral moment checks and eight zero-mode
controls. Seven integral controls passed. The largest matrix residual was
1.8311e-15. The run is completed, with code/input/output hashes unchanged.
No scientific rerun was needed after the independent review added explicit
continuum-domain and localization qualifications to the prose.

`occupied_spectrum/SUM_RULE_REVIEW.md` independently reconstructed the
critical factors and requested the continuum/regulator restriction, now
implemented. `relative_modes/PACKING_REVIEW.md` reviews the additional
packing and shared-reservoir continuation; its mean-subtracted Jeans scope
qualification is implemented. Review reconciliation records final hashes.
