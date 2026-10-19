# A linear insertion disappears in the exact finite-charge response

This defined Gaussian test closes a concrete order-of-limits question.
Its first perturbative density has a strictly nonzero term proportional
to M^3 H. Its full response at fixed positive M has zero coefficient of H.
The proof is analytic and independently derived; no numerical fit or
mathematical computation was executed for this route.

The test operator is

    P_eff=Delta_T[1+M^3 Delta_T^(-3/2)]

on coexact Maxwell one-forms on S4. It deliberately contains a singular
nonlocal polarization. Such a flat current kernel is incompatible with
ordinary gapped QCD and is not claimed as its microscopic response.
Writing M^3=e^2 gamma Lambda^3 only labels hypothetical independent
parameters; it selects no value of e or alpha.

The common spectral prescription is

    delta W(t)=1/2 sum_l d_l[log(1+t/x_l^(3/2))-t/x_l^(3/2)]
                  +(t/2)zeta_T(3/2), t=(M/H)^3.

The sum in brackets converges absolutely. Its explicit first-order trace
is retained in the same subtraction, rather than discarded. Separate
zeta-determinant multiplicativity is not assumed.

For small t the physical stress includes

    rho_first=9 zeta_T(3/2) M^3 H/(64pi^2).

The independent reviewer proves zeta_T(3/2)<-2 by a convergent Hurwitz
representation and elementary inequalities. The coefficient is therefore
nonzero; no numerical coincidence is involved. Small t, however, requires
M<<H, and is not the curvature limit at fixed nonzero charge.

For large t the exact Mellin representation has poles at 4/3,1,2/3,0.
The s=1 residue cancels the explicit first-order trace. The full action is

    delta W=-pi t^(4/3)/(4sqrt(3))-pi t^(2/3)/sqrt(3)
              +(19/60)log t+(3/4)zeta_T'(0)+O(t^(-sigma)),
    0<sigma<1.

The heat representation supplies exponential control on the vertical
contours, including a fixed number of scale derivatives. Consequently
the physical stress rho=(1-D/4)(W/V), D=H partial_H, at fixed M is

    delta rho=-pi M^4/(4sqrt(3)Omega4)
               -pi M^2 H^2/(2sqrt(3)Omega4)
               +19H^4/(80Omega4)+O(H^(4+3sigma)).

The same flat subtraction removes the first extensive term. There is no
linear H term. The charge expansion and H tending to zero do not commute.
Local curvature matching can change the displayed analytic local pieces;
it cannot reinterpret the missing H term as an ordinary local counterterm.

[RAW_DERIVATION_v1.md](RAW_DERIVATION_v1.md) contains the definition,
continuation, residues and remainder proof. The
[independent review](../reviews/qed_response/REVIEW.md) saved its own Mellin
derivation before target reads and accepts the defined-model theorem.
Its [convention addendum](../reviews/qed_response/CONVENTION_ADDENDUM.md)
preserves and translates an initially ambiguous compressed delegation of
the stress formula; the raw spectral calculation was unchanged. The
authoritative stress acts on W/V, not on W followed by division by V.

This is an exact counterexample to using a zero-charge insertion alone
as a prediction of a finite-charge linear-curvature coefficient. It is
not a full-QCD no-go, a physical source of dark energy, or an alpha selector.
The missing physical step remains a complete neutral QCD+QED metric
functional with controlled fixed-charge and global/state limits.
