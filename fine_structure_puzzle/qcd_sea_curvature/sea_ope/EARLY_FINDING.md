# Early OPE finding (FSP-007)

The same-sea-loop short-distance term is calculable at leading order in a declared operator scheme. Hill–Paz, arXiv:1611.09917v2, equations (6),(7),(18)–(22),(28), gives the canonical gluon scalar Wilson coefficient

\[
c_{1g}=\frac{\alpha_s}{4\pi}\frac{\operatorname{Tr}Q^2}{3}.
\]

It starts at order alpha_s, carries Tr Q² rather than (Tr Q)², and survives the three-flavor degenerate-charge cancellation. A single gluon attachment vanishes by its color trace; two attachments to the same closed current loop produce the gluonic dimension-four operators.

With \(\langle p|G^2|p\rangle=-2m_p^2\widetilde f_g\), the full four-dimensional Euclidean photon shell has

\[
\frac{D_p^{g,\mathrm{shell}}}{m_p}
=-\frac{3c_{1g}\widetilde f_g}{32\pi^2}\log\frac{\Lambda^2}{Q_0^2}
\]

at this fixed perturbative order. Every spin-two dimension-four contribution cancels in the angular integral of the full traced tensor, although it is nonzero in the subtraction function alone. The scalar shell is ultraviolet divergent and is canceled by the required strong-coupling counterterm at fixed renormalized coupling. It is not a full sea mass shift.

At leading trace-anomaly order this shell slope is

\[
-\frac{\operatorname{Tr}Q^2}{16\pi^2\beta_0}
\left(1-\sum_f f_f^{(0)}\right),\qquad \beta_0=11-2n_f/3.
\]

For the explicitly massless, fixed-n_f=3 theory this is \(-1/(216\pi^2)\). This is an alpha-free ultraviolet coefficient, conditional on that microscopic theory. It is not a prediction for physical finite-mass QCD, the infrared sea contribution, or R(alpha). Exact contraction checks, source conventions and counterterm matching are being recorded in DERIVATION.md and a bounded run.
