# Parent action and excess mechanism: finite-compliance route

Base checkpoint: e9e534936852643bb3f3ca9df07a31ed2734a30c. Scope authorized by the user on 2026-10-22: inspect prior attempts and pursue the strongest remaining parent/excess route. This directory alone is writable for this investigation. Existing work, including the live CFG960 edit and mechanism_reassessment, is not changed. No large simulation, external publication, or fit is authorized by this contract.

Target: one conservative parent with positive cold mass, a galaxy-law limit, ordinary cosmological growth, and a derived dwarf/cluster excess. A reduced Newtonian action or a necessary condition is partial progress, not this target. Kappa=1/2 remains an input. Both a0 footings are kept separate.

## Portfolio and history

1. Exact density/polarization identification: CFG941 D-T, CFG944 instantaneous expansion gates, D9b multiplier. First uncertain implication has already failed in those constructions: self-gravity is canceled or switching is pathological. Do not repeat them unchanged.
2. Finite positive density/polarization compliance: replace the identity by stored mismatch energy, retaining a separately conserved cold current. First check: derive the action, static law error and linear self-gravity from the same energy. Selected because it changes the precise hard-identity hypothesis without importing a phenomenological dissipative target.
3. Material-dependent compliance: if a constant fails, derive its density-dependent variation and full local convexity condition before claiming that time dependence rescues it. First check: coefficient derivatives cannot be omitted. A healthy energy is not a selector.

Also checked: CFG946 independent dust plus field (EFE/reciprocity and missing selector), CFG955 thermostatted kinetic parent (selection and stability), the 2026-10-19 formation roadmap (mass/E/J budgets), and mechanism_reassessment's new constraint and radiation work. The last is an unfinished separate route and is not duplicated. This is not an exhaustive repository-wide novelty claim.

## Model and first frozen checks

K=4piG. Cold density rho is transported by a conserved fluid current, d=div P, C=rho-rhobar. Newtonian field couples once to rho+baryons. Potential energy is

 E = E_Newton[rho+rho_b] + integral W(K|P|) + A(C-d)^2/2,

where A>0, ell^2=A/K and W(u)=a0^2/K[-u/a0-ln(1-u/a0)]. Add positive inertia eta |dot P|^2/2 and cold kinetic energy. The dot here is a preferred-frame reduced-model derivative; a generally covariant parent and its metric constraints are not established. Initially omit positive gradient stiffness and cold pressure to expose the most permissive growth limit. The static radial test sets rhobar=0 and has finite boundary R with zero mismatch chemical potential at R.

Pre-computation discriminators:
- derive quadratic Schur complement, including gravitational sign;
- derive exact two-mode growing root and a bound uniform in positive polarization inertia;
- derive constant-A static Euler equations and a necessary lower bound on ell for a point source obeying the law within 10 percent at 50 kpc, M_b=1e10 solar masses (an illustrative benchmark, not a data fit);
- compare with a declared instantaneous EdS growth requirement |n-1|<=0.001 at k_com=0.1/Mpc, z=1100, using cold/baryon ratio 5.364 from the record. This is a conservative diagnostic, not a CMB likelihood;
- symbolic identities tolerance zero; numeric cross-check tolerance 1e-10 relative where meaningful; deliberate sign mutation must fail;
- numerical work single thread, <1 GB, <60 s per run; no external data.

If the interval is empty, reject this constant-compliance construction under these criteria, not all parent theories. If nonempty, proceed to radial solutions. Inertia must be varied analytically, not tuned to hide a bad static limit. A follow-up density-dependent energy must include A' and A'' and distinguish mathematical admissibility from physical derivation.

No successful count of algebra checks will be reported as a successful theory. Self-review only unless explicitly independently reviewed.
