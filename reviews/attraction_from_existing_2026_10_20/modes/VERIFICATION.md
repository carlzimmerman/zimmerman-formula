# Analytic verification and scope

No scientific simulation, fitting, symbolic package, or numerical spectral
diagonalization was used. No computational evidence range is claimed.
File hashing and source comparisons are provenance operations only.

The load-bearing derivations were checked directly:

1. Expand each square in RESULT (2): its cross terms reproduce exactly
   `C b^dagger+C^* b`, while its constant is canceled by `-|C|^2/E`.
2. Form the four static sector energies. The constant, baseline coupling,
   one-site self shifts, and linear mean field cancel. The remaining cross
   term is `-2 Re(g1^*g2)/E`.
3. Substitute `E_q^2=epsilon_q(epsilon_q+2g2 n0)` into the exchange sum.
   Since `epsilon_q=q^2/(2m)`, its Fourier coefficient is
   `-4m gamma^2 n0/(q^2+4mg2 n0)`; the three-dimensional Green function
   supplies `exp(-kappa r)/(4pi r)` and yields RESULT (6).
4. Replace both physical densities by `rho_f+n Delta rho` before the same
   four-sector subtraction. This gives RESULT (9), not an added-particle
   monopole. A density-preserving change sets the coefficient to zero.
5. At endpoint coexistence, the memory multiplicities `(1,4,2)` give
   `w1=2sqrt(2)exp(U_pair/(2theta))`. Solving `w1<1` gives exactly
   `U_pair<-3theta ln2`.
6. Check the original source elimination against the raw matched kernel:
   its negative source diagram is already in the positive residual contact.
   Read the separate real-host and nodal-sector raw vertices before making
   any carrier identification. No such identification is inferred.

These checks establish conditional algebra, not the existence of a bath,
the validity of same-species fragmentation, positivity of a live host's
full Hessian, actual site formation, or a release rate. The author performed
the checks. A sibling agent independently reconstructed the factor, kernel,
and conversion subtraction from the raw source equations without receiving
the present proof. Its bounded review is recorded in `EXCHANGE_AUDIT.md`;
the remaining argument is author self-review.

Mathematical proofreading used `mathbox:proofread-math` in self-review mode
for these new files only. The review covered display delimiters, definitions,
sign/factor consistency, physical-sector distinctions, references, and scope.
No old source note was edited. No unresolved typographical issue was found;
unproved physical implications remain explicitly marked.
