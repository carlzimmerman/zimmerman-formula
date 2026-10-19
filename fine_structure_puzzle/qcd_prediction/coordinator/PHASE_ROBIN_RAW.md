# Further hand calculation: decoupled Robin partner

Coordinator raw calculation following PHASE_BLOCK_RAW.md, saved before reading the agents' new phase-block work. These are candidate identities for independent verification, not a physical whole-vacuum determinant.

For L_A=-d²+h²+(1+K²)/r², a candidate regular zero-energy solution normalized to r² at zero is

u_A(r)=3[sinh(r)/r-r/sinh(r)].

It follows alternatively by applying Q-dagger to (u_A,0): the result is proportional to the regular gauge-kernel solution (sqrt2 K h,r h'). Its Robin functional is exactly

u_A'-h u_A=6K h.

For the explicit auxiliary reference L_A*= -d²+1+2/r², with the SAME outer Robin parameter h(R), the normalized regular solution is u_*=3[cosh(r)-sinh(r)/r]. Its Robin functional is

u_*'-h u_*=3[cosh(r)/r-csch(r)].

Hence the proposed relative Robin determinant at x=R is

D_A^Robin=2x[x cosh(x)-sinh(x)] /
          {sinh(x)[sinh(x)cosh(x)-x]}.

At large x it is 8x(x-1)e^(-2x) times exponentially small relative corrections. Its log has a residual -1/x-1/(2x²)+... . The exponentially small near-zero eigenvalue must remain in the finite-wall spectrum; it cannot also be replaced by an independent collective-coordinate Jacobian without a justified limiting prescription.

If the first-order pairing is a true isospectral correspondence on the mixed relative domain and no zero eigenvalues occur at finite x, the phase-vector determinant is the product of this L_A Robin determinant and the L_g Dirichlet determinant, each relative to its stated auxiliary scalar reference. The static complex ghost contributes the full L_g determinant. Combining their determinant weights would therefore give

Z_phase+ghost^relative=sqrt(D_g/D_A^Robin),

D_g=3[x cosh(x)-sinh(x)]/[x² sinh(x)],

D_g/D_A^Robin=3[sinh(x)cosh(x)-x]/(2x³).

The logarithm of this last expression has no inverse powers at all after its explicit x and log x terms: (1/2)log(D_g/D_A)=x-(3/2)log x+(1/2)log(3/8)+exponentially small terms. Thus the 1/x terms cancel within this consistent, explicitly defined static auxiliary comparison. This is a candidate calculation, not permission to add the old unframed zero-mode factor or call the remaining real block a full coefficient.

Required verification: expand the spherical action with the actual gauge-fixing normalization; check the mixed vector and ghost domains including origin regularity and the nonzero-eigenvalue Q map; authenticate the determinant theorem; independently evaluate the Robin determinant or phase operator; preserve a common auxiliary comparison and all near-zero eigenvalues. No angular/Fourier modes, global physical-vacuum matching, de Sitter continuation, c_H or alpha follows from this block identity alone.
