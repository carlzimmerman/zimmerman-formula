# Frozen cancellation and spectator tests

Base e6d278b74755885d9f62106becef5d7b753c512c. Target: a microscopic
same-state model cancelling K796's s^(5/2) term, retaining sourced MOND cubic,
and fixing positive gravitating vacuum with no fitted normalization.
Kappa=1/2 remains FITTED; CFG493 kappa_Lambda=0.417 +/- 0.095 and
kappa_crit=0.345 +/- 0.078 are separate and unused. rho_DE footing only.

Prior records: CFG894 rules, ledger, doors; reviews/microscopic_ir_matching_2026_10_26;
reviews/susy_lifshitz_matching_2026_10_24; W4_08/formal/protected_auxiliaries
and symmetry_protection. Equal full-spectrum pairing is already tried. The
new work tests unequal-spectrum cancellation and a derivative-coupled spectator
outside the earlier single-field detailed-balance obstruction. No four-form,
GF1 or pending p62/p63/Lean work is duplicated. Scope of novelty: inspected
local predecessors, not a global literature claim.

Route A: modes omega_i=v_i k sqrt(k^2+t_i s(1+mu^2)), t_i,v_i>0.
Define signed weights w_i=sigma_i d_i v_i and M_p=sum w_i t_i^p.
In n dimensions the nonanalytic determinant moment is (n+2)/2; specialize n=3.
Test M1=M2=M(5/2)=0 without imposing M0=0. Prove the one-distinct-spectrum
on-one-side obstruction using convexity. For a constructive algebraic fixture,
fix t_i=1,4,9,16 before computing and solve the exact nullspace; these are
unfitted test nodes, not proposed particles. No spectrum scans or target numbers.
Vary the overall spectral normalization to test whether cancellation selects
vacuum or cubic. These spectra need not have a microscopic interacting action.

Route B: canonical time-domain detailed balance with two real fields and
W=integral[a|grad phi|^2/2+b|grad chi|^2/2+f chi+g chi^3/3
           +lambda chi |grad phi|^2], a,b,f,g,lambda>0.
F_A=delta W/delta field_A, E=sum F_A^2/2. Fermion operator is W's Hessian.
Work in general n first, then n=3. Derive constant-gradient homogeneous
relaxation, energy, boson/fermion zero-momentum gaps and source response.
Compare the regular massive spectator variant replacing g chi^3/3 with
m chi^2/2. No bare MOND cubic or vacuum uplift is appended.
Source reference 1908.03220v1 section2.1 eq5 motivates the action class;
the multifield extension and calculations are ours, not a source claim.

Option class audit (no kappa options, no chance-hit candidate). Inputs purely
symbolic; hbar and phase-space pi retained in determinant. Positive energy in
a preferred-frame algebra is not automatically cosmological rho_DE c^2.
No c-based gravitational completion, baryon embedding or vacuum principle is
assumed. Absence of these is a failure to meet the target, not an excuse to fit.

Kill/partial/success: failure of any of cancellation, cubic, vacuum selection
kills that explicit joint candidate only. Unequal spectral cancellation alone
is partial algebraic progress, not a physical model. Success requires all three
plus health/source checks. Second diagnostic: bosonic/fermionic gap splitting
and static force exponents. Mutation: perturb the last spectral weight; moment
checks must fail. Removing lambda must remove response in the spectator model.
I1-I8: no empirical inputs; dependence explicit; dimension/scaling; no naming
of a coefficient as target; no Friedmann identity; rho_DE not rho_crit;
hbar explicit; pi tracked. No downloads, heavy runs or parameter scans.

Freeze alone before executable. Write check.py and separate normal/MUTATE
outputs, RESULT.md with self-review and open continuation. Append distinct
route audit rows to register and regenerate ledger; commit only own files.
