# Printed source inconsistency and independent resolution

No frozen scientific file or author output was edited.

## The mismatch in arXiv:2212.11848v1

The exact pinned PDF SHA256 is `677ed007e8e1e6696c2ce60fd21637cb7818349f841f0b4b488dc8df6b2ad06c`. I checked printed p.20 visually as well as through text extraction.

* Equation (4.30) prints `G2_ferm,div=dG nf Tf/(6pi^2 epsilon)`.
* Equation (4.34) gives a summed fermion pole `dG nf Tf/(12pi^2 epsilon)`.
* Equation (4.37) prints a positive finite fermion term `+dG nf Tf(5+3L)/(36pi^2)`.
* Equation (4.39) includes the negative of that finite term.

Equation (4.2) is an ordinary sum of the listed diagrams. Calling (4.39) a signed sum does not reconcile these printed differences. The frozen coordinator text's source narrative therefore needs this correction note: **not every intermediate printed fermion equation has been authenticated as mutually consistent**. The sum (4.39), total pole (4.34), and gauge/curvature renormalization (4.40)-(4.46) are consistent for the logarithm used in the fixed-parameter sphere stress.

## Independent primary QED source

I separately acquired and authenticated S. Giombi, I. R. Klebanov, G. Tarnopolsky, *Conformal QED_d, F-Theorem and the epsilon Expansion*, [arXiv:1508.06354v3](https://arxiv.org/abs/1508.06354v3), dated 2015-10-30. Retained PDF: `reviews/global_sphere/1508.06354v3.pdf`, SHA256 `7b73526ccf7575077a9f102ce3a028230d64f81e379e1e0d00245901ea7f72fd`. The cover and printed pp.18,25 were visually inspected. Poppler emitted a recoverable xref-reconstruction warning; both relevant rendered equations and the independent web PDF text agree.

Its convention is `d=4-epsilon_Q` and its (4.15) has `W_int=+e0^2 G2_Q/2`, unlike the minus sign multiplying G2 in the non-Abelian paper. Equation (4.16) gives

`G2_Q/Nf=1/(6pi^2 epsilon_Q)+(5+3L)/(36pi^2)+O(epsilon_Q)`.

This can be checked without relying on a reconstructed finite constant: its exact (B.5), for a four-component Dirac trace, is

`G2_Q/Nf = -4 R^(4-d) Gamma(d-1) / [(d-3) 4^((d+2)/2) (4pi)^((d-3)/2) sin(pi d/2) Gamma((d+1)/2)]`.

For `d=4-epsilon_Q`, the residue is `1/(6pi^2)`. Its finite residue multiplier is

`log R - psi(3)+1+(log4)/2+(log(4pi))/2+psi(5/2)/2`

`=log R+5/6+gamma/2+log(4pi)/2`.

I derived the logarithmic derivative of the Gamma expression directly and checked the polygamma simplification independently with SymPy. This reproduces the stated logarithm and finite term. It is source verification and algebra, not a fresh derivation of every propagator contraction.

Because `epsilon_Q=-2epsilon_NA` and the two G2 definitions have opposite signs in W, the consistent non-Abelian fermion terms would be `+dG nf Tf/(12pi^2 epsilon_NA)` and `-dG nf Tf(5+3L)/(36pi^2)`. These agree with (4.34)/(4.39), and expose the mismatches in the printed (4.30)/(4.37).

The QED source therefore independently supports `W_int=uS log(mu R)/(12pi^2)+H-independent terms`, with `S=Nc sum Qf^2`; its fixed-coupling stress is `rho_int=uS/(48pi^2 V)`. The frozen coordinator's electromagnetic coefficient is accepted in this weak, massless regime. Its citation to the inconsistent individual non-Abelian fermion equations cannot be treated as additional independent corroboration.
