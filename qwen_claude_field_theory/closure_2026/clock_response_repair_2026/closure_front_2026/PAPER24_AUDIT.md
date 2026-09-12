# PAPER24/L215 action-to-claim audit

Audited local commit `96512fc6e`, manuscript
`qwen_claude_field_theory/papers_2026/PAPER24_the_decoupling_locus_2026.tex`,
and its cited L213–L215 scripts. This is a correction note, not an edit to the
published deposit. The existing Lean statements can be valid while their
physical premises have not been derived.

1. **Minimal coupling does not imply no modified force** (manuscript lines
   10, 25). It removes a direct matter derivative in the scalar equation, but
   the cubic scalar couples to curvature. Independent variation in
   `metric_response/REPORT.md` gives
   \(G_0\Delta\pi=2b\Delta\Phi\),
   \(2M^2\Delta\Phi=\rho+2b\Delta\pi\), on the stated local static branch.
   The source is therefore transmitted through the metric. This does not
   establish MOND; it refutes the no-force implication.

2. **The clock response does not vanish at \(W_0=0\)** (lines 28–33, 97, 99).
   The paper itself quotes
   \(\sigma/\pi=2qsW_Y/(2q^2W_Y-W_0)\); at \(W_0=0\) this equals \(s/q\),
   not zero, for nonzero \(qW_Y\). The local clock constraint block is regular
   there. Only the reduced \(W_Y\) correction cancels. The nonlinear frozen
   calculation now supplies an exact extension: in unit clock-time coordinates,
   \(z=p/q\), \(Y=0\), \(sW=0\), but a nonzero clock tilt remains.
   See `nonlinear_clock/REPORT.md`. Dropping the clock response is not licensed.

3. **Reference-clock derivatives are not proper-time derivatives** (lines
   30, 38–44). The fixed action uses
   \(W_0=U-2\gamma\bar q^2\bar q'(\tau)\).
   The stress tensor instead gives \(p_3=2\gamma Q^2\dot Q\), with the dot
   denoting physical proper time. Under the tracked interpretation
   \(Q=\bar q(\tau)\), \(\dot Q=s\bar q'\), so \(W_0=0\) implies
   **\(p_3=sU\)**, not \(U\). If one further imports the paper's
   \(p_3=w\rho_3\), \(\rho=U/m\), \(w=m(s-1)\), it gives
   \(\rho_3/\rho=s/(s-1)>1\) for finite \(s>1\), not \(1/(s-1)\).
   This conditional correction invalidates that derivation of a positive
   noncubic share; it does not exclude every off-track solution.
   L213 lines 7 and 119 explicitly invoke a tracked family. If an off-track
   interpretation is intended, neither \(p_3=U\) nor the imported simple
   total-density identities has been established. See the independently
   varied controls in `health/pressure/REPORT.md`.

4. **A small background momentum ratio is not a perturbation theorem**
   (line 54). It does not bound inverse constraint operators or small kinetic
   eigenvalues. The statement that every earlier gate survives to four percent
   requires new perturbation and cosmological calculations on that locus.

5. **L215 derives conditional leading shifts, not full PPN** (lines 80–94).
   L215 line 59 substitutes \(\Psi=\Phi\). Its Lean theorem likewise assumes
   this and a nonzero denominator. Equal shifts are correct at first order,
   but do not derive the baseline equality from the new matter-coupled action,
   a full solar-system solution, or exact strong-scalar lensing. A conformal
   factor shifts the two potentials oppositely, rather than shifting only time.
   Matching one boosted \(g_{0i}\) term while keeping the Einstein off-diagonal
   metric zero does not determine the full PPN \(\alpha_1\).
   Setting the solar-system potential share \(f_s=1\) is an additional
   assumption, not a consequence of the required MOND high-acceleration force
   limit. Consequently the 4.6 m/s figure is a conditional diagnostic, not a
   derived final gate. None of \(\beta,\alpha_1,\alpha_2,\alpha_3\) is newly
   certified here.

6. **The disformal proposal also changes the photon cone**, even for a
   perfectly aligned clock. `disformal_cone/REPORT.md` derives the Maxwell
   equation and proves the conditional cone/no-slip obstruction. Keeping the
   original tensor action while changing only the matter metric cannot inherit
   the old common-cone result.

No claim in this note establishes \(\Lambda\)CDM, excludes all MOND theories,
or proves the fitted \(\kappa=1/2\). The specific statement that only alignment
and \(\kappa\) remain is not supported by these action-to-claim dependencies.
