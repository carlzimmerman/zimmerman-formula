# Supplement to the original frozen checks

2026-10-20. Original criteria commit `72a3b470d`; original normal run passed
27/27 and its mutant failed C08 and C20 as declared. No original check is
withdrawn or relaxed. These additions precede the revised checker run.

Independent review requested that the dimension control explicitly select
n=4 in MUTATE instead of only comparing sphere factors in both modes. Add
a check against the original n=3 factor; it should fail in the mutant,
while the normalized force and portal remain unchanged.

The analytic quadratic member was developed after the original run. It is
not a new numerical trial or an exact-coefficient candidate. Verify its
integral derivative, both characteristic Hessian factors, subluminal
factorization and zero energy at g=0. It has arbitrary a>0 and no fitted or
target coefficient. The argument and its timing are recorded in PROOF.md.

The mutable top-level puzzle dashboard is a historical navigation source,
not an execution dependency. Preserve its base hash in this record:
`b201053154dc5e2011a7d8eb70c5ade50a231d4768909a796515ced7c83a71bb` at
`177591c05a384bc07c819e3fe0d5517aa8798cb4`. Revised runs use the proof and
this supplement as actual input artifacts. Their exact hashes are recorded
before and after execution, independently of later dashboard updates.
