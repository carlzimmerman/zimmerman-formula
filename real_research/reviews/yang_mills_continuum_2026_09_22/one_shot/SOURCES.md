# Source check for YM-C2

Checked 2026-09-22. Question: does the compact heat equation with nonnegative
Ricci curvature satisfy the gradient inequality (5) used in `PROOF.md`?

Peter Li and Shing-Tung Yau, *On the parabolic kernel of the Schrödinger
operator*, Acta Mathematica 156 (1986), 153–201,
[DOI 10.1007/BF02399203](https://doi.org/10.1007/BF02399203).
Theorem 1.1, printed page 157; proof continues on page 158.
The original article was read through a
[full-paper mirror](https://scispace.com/pdf/on-the-parabolic-kernel-of-the-schrodinger-operator-26njhmohgk.pdf).
Title, authors, journal pagination and theorem hypotheses agree. A CiteSeer
mirror returned HTTP 403; it was not used as evidence. No article copy is
redistributed with these notes.

The theorem concerns a compact manifold with nonnegative Ricci curvature,
and allows a convex boundary with Neumann conditions. Here SU(N) is compact
and boundaryless. Its heat equation uses generator Delta; our kernel k_s
uses exp(-s C)=exp(s Delta). The change from Riemannian volume to normalized
Haar only multiplies the kernel by a constant, leaving log derivatives and
the Harnack inequality unchanged. Our Brownian physical time t corresponds
to s=xt/2, not s=xt.

The extracted result is the bound
|grad log u|^2-partial_t log u <= n/(2t). `PROOF.md` reproduces the compact
Bochner/maximum-principle derivation and derives its own diameter estimates
by integration. The finite-block Feynman–Kac comparison and conditional
variance argument are written out there; they are not attributed to a
Yang–Mills theorem in this source.

Classification: standard heat estimate used in a direct comparison argument.
No novelty search or novelty claim. Search scope was this exact Li–Yau
theorem and its normalization; the existing project sources already cover
the finite-volume ground-state transform and Casimir normalization.
