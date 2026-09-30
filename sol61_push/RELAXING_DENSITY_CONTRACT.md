# Relaxing density common-energy probe

Base 0374ab1f68a6139d5a50df21fe751e468c764654; previous goal turn was progress. In c=hbar=1 units, take positive area-density variable q, polarization magnitude P, and positive A,B,K,G. Proposed homogeneous energy is E(q,P)=A/q^2+Bq^2+KqP^3, with K=nu*y^3/(6pi*v^2) from the planar free-band calculation. This is an assumed effective energy, not a derived microscopic action. Retain the assumed critical gravitational matching W=P^2/2+4pi G[E_min(P)-E_min(0)].

Test exact stationarity, the low/high-field response and proxy curvature ratio. Then independently embed the density-only vacuum energy into a conserved material-coordinate action L=-U(q), q=(det B_material)^(1/6), to test stress, expansion and local phonon kinetic energy. This embedding is a discriminator; it does not supply a covariant completion of the polarization term.

Exact symbolic algebra plus double-precision roots. Numeric parameter triples (A,B,K)={(0.5,0.25,0.1),(2,3,0.7)}, G=0.1, P={1e-4,0.01,1,10,1e4}; root is t^4+u*t^3-1=0 on (0,1], t=q/q0, u=KP^3/(2Bq0). Root residual tolerance 1e-9; independent finite-difference force slope tolerance 1e-5 relative. No random inputs, 30-second timeout, one thread.

Passing verifies these formal uniform-energy and material-action identities. It cannot derive A,B,K, enforce zero vacuum counterterm, select 32pi, establish a galaxy profile, or prove an interacting covariant theory. A vacuum equation of state at one density is not a de Sitter solution. The relevant primary medium EFT is Endlich, Nicolis and Wang arXiv:1210.0569v1 Sections 2-3; the particular U and coefficient bridge are derived here.
