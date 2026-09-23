# D-YM3 swing: the Hardy-marginal 1/4 is the Laplacian's Hardy constant, not a κ source

**Door (from the reopen directives).** I14's route to κ = 1/2 needs the
framework's constrained Hessian to be Hardy-marginal: the canonical radial
potential V must equal 1/4 identically. Door H killed this for the
committed interpolant μ₂. According to the directive, the only
resurrection would be "a DIFFERENT action … whose constrained Hessian is
Hardy-marginal at its background."

**Swing.** `verify.py` (sympy, exact, 20/20 checks, exit 0) repeats door H's
reduction for the whole single-scalar class L = Λ⁴ f(K), with f′ = μ
arbitrary. It works on the on-shell sourceless background, where the flux
r^{n−1} u μ(u) is conserved, in any space dimension n.

1. **The 1/4 is generic.** In the Newtonian limit μ → 1, the log-coordinate
   shift is s = (n−2)/2 and V = ((n−2)/2)². This is the classical Hardy
   constant of the n-dimensional Laplacian, checked for n = 3, 4, 5, 6. At
   n = 3 it equals 1/4, which makes "κ = 1/2" a dimension count,
   (n−2)/2 = 1/2. Every theory with a Newtonian limit has it. It carries no
   framework-specific information and cannot select κ.
2. **The physical corner has V → 0.** Any interpolant with a deep-MOND
   regime, μ(u) = u(1 + O(u)), gives V → 0 as u → 0. For μ = u exactly,
   V = 0 identically. This was checked for a generic deep-MOND expansion
   and for μ₂, the "simple" interpolant and the "standard" interpolant, on
   both the on-shell background and door H's log profile.

   EFE-capped physical halos sit deep in this corner (door H:
   u(r_break) ~ 10⁻¹⁹), so no deep-MOND action is Hardy-marginal on its
   physical background.
3. **The only exact realisations are not MOND.** V ≡ 1/4 with s ≡ 1/2
   forces a_r = μ + uμ′ to be constant, i.e. μ = A + B/u. That is a
   Newtonian term plus a √K (cuscuton-type) term. It has no deep-MOND
   regime, since μ/u → ∞.
4. **Consistency.** Door H's closed forms for s and V (μ₂, log profile) are
   reproduced exactly.

**Verdict.** D-YM3 is closed for the entire single-scalar f(K) class,
not just μ₂. Reopening it would need an action that is neither
single-scalar f(K) nor Newtonian in its Hardy corner. Multi-field and
vector completions have their own recorded kills elsewhere in the
register; none is reopened here.

**Relation to the prize.** None. This door concerns the framework's κ, not
the Yang–Mills mass gap. It is swung here only because the directive
listed it under the YM doors.
