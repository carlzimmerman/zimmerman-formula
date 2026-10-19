# A finite gluon threshold and its mixed quark partner

The new local matching result is

    (g_s,EFT-g_s)/e^2 = g_s^3 sum Q_f^2/(256 pi^4)
                            [log(s/mu^2)-3/4],

for a heavy canonical photon with conserved vector couplings and light
fundamental quarks. This fixes the previously unspecified finite number
at the first nonzero gluonic operator order. The independently extracted
mixed quark threshold is

    (m_f,EFT-m_f)/(e^2 m_f)
      =Q_f^2/(16 pi^2)[-3log(s/mu^2)+5/2]
       +Q_f^2 C_F g_s^2/(16 pi^2)^2[-3log(s/mu^2)+17/4].

These are operator coefficients at fixed full-theory MSbar parameters.
No measured alpha, mass scale, sigma term, or cosmological target was fitted
or numerically inserted. The source-to-project implication is derived here
and requires the fresh source-first review commissioned by the coordinator;
the primary sources' Feynman integrals were not independently recomputed.

The finite gluon coefficient follows from the complete two-loop matching
formula in Martin's exact arXiv:1812.04100v3 PDF, with the independent
antecedent of Bednyakov arXiv:1410.7603v4. A small-top hierarchy exposes the
six-flavor intermediate theory. Both subsequent top QED matching and the
top mass conversion must be subtracted. The latter includes the one-loop
5/2 term. The resulting W/Z threshold is

    3[L_W-3/4]+[(20r^2-22r+11)/(6r)][L_Z-3/4].

The neutral charge polynomial equals the explicit sum of all six massless
quarks' left/right squared couplings. At this order the complete single
massless-quark-loop tensor has only that chiral sum, which admits the
conserved-vector limit. The formal hierarchical limit is used to extract
fixed-order Wilson coefficients, not as an unresummed numerical prediction
with large physical scale logarithms.

The corresponding canonical proton gluon insertion is

    f_g(s)=-B_g[log(s/mu^2)-3/4],
    B_g=g_s^2 sum Q_f^2 <p|[G^2]|p>/(1024 pi^4 M^2).

Its logarithm reproduces the inherited signed full-tensor OPE and corrected
Gasser normalization. The pure-QCD trace anomaly supplies the matrix
element only after scalar sigma inputs are specified; it did not supply
the finite 3/4.

The sharp O(4) photon cutoff is a separate regulator. At this order its
finite conversion agrees with the heavy-photon endpoint because the
absolutely convergent difference of their low-pass filters has zero moment
against the dimension-four B/t density. This is proved in DERIVATION.md
(11), including the needed asymptotic remainder condition. It does not
identify the two regulators at higher orders: a log(t)/t density has the
nonzero filter moment pi^2/6. At mu=Lambda the finite sharp conversion is
(3/4) B_g, not zero.

For the explicitly declared three-massless-flavor theory, S_Q=2/3 and
beta_0=9. The leading trace identity gives B_g=-1/(216 pi^2), hence the
finite local sharp conversion at its matching point is

    (D_ct^g/M)|_(mu=Lambda)=-1/(288 pi^2)+O(alpha_s).

This analytic corollary is a subtracted UV matching constant in that
microscopic theory. Choosing a matching point does not mean varying the
original fixed-MSbar path with s; it is not the full mass response or R.

The bounded run_v3 completed 16 exact checks of source-expression algebra,
six-flavor charges, mass-threshold composition, vector mass projection,
filter moments, and canonical trace normalization. All three manifests
validate against the unchanged inputs. The first two runs failed on
SymPy's complex branch choice for an optional real logarithmic integral.
The third used an absolutely summable integrated geometric series; both
failed attempts and their exact code/contracts remain. No RLIMIT_AS was
requested. Successful algebra does not independently certify the source's
two-loop pole, gauge, or IR subtraction.

The hadronic limitation matters: H_g is O(1/g_s^2). The unknown next gluon
threshold therefore contributes at the same hadronic order as the known
mixed quark 17/4 term. Equation (9) of the frozen derivation is not a complete
NLO hadronic endpoint. See ADDENDUM.md for operator versus hadronic power
counting. The remaining physical leaf includes full nonlocal proton
current correlations, scalar matrix elements, higher matching/running and
physical thresholds, finite-s remainder control, and the independent
unconditioned curved-QCD response. Neither the proton hard constant nor
the curved vacuum A, R, or alpha has been completely evaluated.

Durable evidence: DERIVATION.md, ADDENDUM.md, BRANCH_AUDIT.md,
SOURCE_INPUT.json, SOURCES.json, INPUT_PINS.json, three pre-run freezes,
the three scripts/contracts, and run_v1/run_v2/run_v3 manifests. The exact
primary PDFs are retained only in the authorized ignored literature cache.
