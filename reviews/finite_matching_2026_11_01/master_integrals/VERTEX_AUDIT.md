# Independent real-scalar/Weyl vertex and graph-weight audit

Reviewer: `/root/independent_math_transport`, 1 November 2026. **Verdict:
the inspected component vertices, Takagi transformation and nonvector
graph prefactors follow from the stated raw action and Martin conventions.**
This is an independent algebraic reconstruction and code review of
`two_loop/model.py`, followed by inspection of the saved controls. No full
vacuum calculation was rerun here; numerical and physical scopes remain
those of the pinned finite records.

Let E=(I,iI)/√2 map real canonical fluctuations r to δz=Er. With the
source superpotential normalization W=linear+μzz/2+Yzzz/6, write

    F_i(r)=F_i0+K_ia r_a+T_iab r_a r_b/2,
    K=ME, T_iab=Y_ijk E_ja E_kb.

Expanding |F|² and differentiating gives

    λ_F,abc=2 Re[K_ia* T_ibc+K_ib* T_iac+K_ic* T_iab],
    λ_F,iijj=2 Re[Σ_k T_kii* T_kjj]+4Σ_k|T_kij|².

These are exactly the code's three cubic permutations and quartic
diagonal contraction. The all-identical index case gives 6|T_iii|²,
so no extra multiplicity is missing there.

For each gauge generator the real D expansion is

    D_p(r)=D_p0+L_pa r_a+S_pab r_a r_b/2,
    L=2g Re(E†R_p z), S=2g Re(E†R_p E).

Since V_D=Σ_p D_p²/2,

    H_D=LᵀL+Σ_p D_p0 S_p,
    λ_D,abc=Σ_p[L_pa S_pbc+L_pb S_pac+L_pc S_pab],
    λ_D,iijj=Σ_p[S_pii S_pjj+2 S_pij²].

The D0S Hessian term is retained for non-D-flat fixtures. The code's E,
L,S normalizations, cubic axes and quartic factors agree with these direct
expansions. No radial-only scalar interaction replaces the complete tensor.

The full Weyl mass matrix includes both W_ij and the symmetric gaugino
mixing J_pi=√2g(z†R_p)_i. Its derivative with respect to a real scalar
therefore includes both Y_ijk E_ka and √2g(E†R_p)_ai. The code includes
the latter in both symmetric off-diagonal blocks. It rotates a Yukawa
matrix by UᵀyU, with the same U satisfying UᵀMFU=diag(m)≥0.

For the CP slice a constant diagonal phase P makes PᵀMFP real symmetric.
If V diagonalizes it with signed eigenvalues μ_i, then
U=PV diag(1 for μ_i≥0, i for μ_i<0) is the correct Takagi matrix. Its
negative-eigenvalue phases turn μ_i into |μ_i| and must remain in y. This
is why Re(y²)m_i m_j retains helicity-flip signs even with nonnegative
Takagi masses. A generic complex background outside the declared branch
is explicitly rejected, not approximated as real.

The primary graph normalizations are Martin,
[hep-ph/0111209v2](https://arxiv.org/pdf/hep-ph/0111209v2), Eqs. (4.2)–(4.5):
ordered sums use λ_ijk²/12 for SSS, λ_iijj/8 for SS, |y_IJk|²/2 for FFS,
and y_IJk y_I'J'k M*_II' M*_JJ'/4 plus its complex conjugate for barFFS.
In the Takagi basis the last is Re(y_IJk²)m_I m_J/2. The grouped code
weights match these expressions; it does not add the complex conjugate
twice. Degeneracy grouping sums all original ordered indices before
kernel evaluation.

The vector function transcription was independently compared with the
same primary source: SSV Eqs. (4.16),(4.24), and DRbar-prime Eqs.
(6.21)–(6.30). The positive-mass formulas and zero-vector limits agree.
The three-term gauge sum implements the two source exchanges correctly.
The master module naming mismatch in the first draft was corrected before
its successful runs.

Saved broken/unbroken supersymmetric U(1) function identities, all-SU(5)
supersymmetric cancellation, degenerate-basis invariance, coupling
homogeneity and reduced CS checks provide complementary finite controls.
Their passing results do not replace the vertex derivation above, nor do
they prove accuracy outside the stated mass-group/background tolerance
and CP branch. Exact reviewed hashes and current-input validation are
recorded separately.
