# Independent static phase/gauge reconstruction

Coordinator raw hand derivation saved before reading the agents' new phase-block calculations. This is a candidate derivation to compare, not a completed physical determinant.

Use the reduced static SU(2) spherical action in dimensionless radius r, with complex amplitude w and residual radial connection b:

E=integral[|w'-i b w|²+(|w|²-1)²/(2r²)+r²h'²/2+|w|²h²].

Around w=K real, b=0, K=r/sinh r and h=coth r-1/r, set w=K+i q. Residual gauge transformations are delta q=K lambda, delta b=lambda'. Direct expansion gives

E_phase=integral[q'²+(h²+(K²-1)/r²)q²-2b(Kq'-K'q)+K²b²].

Because K''/K=h²+(K²-1)/r², this equals

integral[(q'-(K'/K)q-Kb)²]+[(K'/K)q²]_boundary.

Thus it is a gauge square with a boundary term. For q=0 at the outer wall and regular fields at zero, that term vanishes.

The candidate background divergence is G=b'+2b/r-2Kq/r²; it varies as lambda''+2lambda'/r-2K²lambda/r². Consequently the regular radial ghost u_g=r lambda has operator L_g=-d²+2K²/r², agreeing with the frozen ghost calculation.

With u=sqrt(2)q, v=r b and gauge-fixing contribution (1/2)integral r²G², the two first-order squares are

Q y, Q=d/dr+W, y=(u,v),

W=[[h,-a],[-a,1/r]], a=sqrt(2)K/r=sqrt(2)csch r.

This gives H_phase=Q-dagger Q with

U11=h²+(3K²-1)/r²,
U22=2K²/r²+2/r²,
U12=-2a(h+1/r).

Using a'=-a(h+1/r), the partner is diagonal:

Q Q-dagger=diag(L_A,L_g),
L_A=-d²+h²+(1+K²)/r².

At the origin, W has leading r^-1[[0,-sqrt2],[-sqrt2,1]], whose eigenvalues are 2,-1. H_phase therefore has centrifugal eigenvalues 6 and0, with regular branches r³ and r, respectively. Both partner channels have centrifugal2/r² and regular branch r². One must not impose the frozen real block's r²I origin normalization on this different block.

Framed ghost Dirichlet means lambda(R)=0. It preserves q(R)=0 but generally does NOT preserve b(R)=0 since lambda'(R) need not vanish. A candidate compatible relative boundary prescription is tangential phase u(R)=0 and background-divergence G(R)=0, that is v'(R)+v(R)/R=0 on this block. It needs the full vector/BRST domain checked; an arbitrary all-component Dirichlet prescription is not automatically gauge compatible.

For this mixed prescription, z=Qy satisfies z2(R)=0. For a nonzero eigenvalue, Q-dagger z=E y and u(R)=0 imply z1'(R)=h(R)z1(R). Thus the decoupled partner has ghost Dirichlet and L_A Robin, not both scalar Dirichlet. A determinant identity would need these domains, regular-origin normalization, possible zero-mode treatment and matching factors. No determinant normalization or inverse-radius coefficient is inferred here.

The regular ghost zero-energy solution lambda=h generates a regular Q-kernel candidate y=(sqrt2 K h, r h'). Its u(R) is nonzero at finite R, so it does not belong to this mixed outer domain. This is consistent with excluding a framed finite-wall rotation zero mode. The infinite-radius limit is nonuniform and requires a separate spectral analysis.

This calculation changes no prior determinant packet. It is only the spherical static sector; no angular/Fourier sum, matched vacuum determinant or QCD c_H is obtained. Signs of q/b can be changed together by ansatz convention, leaving the spectrum and boundary issue unchanged.
