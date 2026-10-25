# Resolve a field interface and scatter waves

Continue cac381e206. Fix illustrative r=1,s=1/4, not derived parameters.
Use Palatini canonical q=chi/v, f=cos²(sqrt(s)q), y=sin²(sqrt(s)q)/s,
W/D=[r+(y-1)²]/f². Coordinate z=x sqrt(D)/v. Hold fixed a prescribed conserved
Einstein-frame rest-density source d=rho_star/D, with effective potential
V=W/D+d A, A=f^-1/2. This differs from holding Jordan density fixed during
perturbations. rho_J=rho_star/A³; at restored interior A=1 they agree.
Source step d=20,32,100 on z<0, zero on z>0; source is mechanically supported,
not free responding dust. Einstein metric/lapse taken constant. This is a local
scalar boundary calculation, NOT a complete gravitational or galactic solution.

Match field and derivative using both first integrals; source-step surface
value A_s=1+[W(0)-W(vac)]/(D d). Resolve profiles on [-15,15] and [-20,20].
Compute lowest scalar eigenvalues of -d²/dz²+V_qq with Dirichlet endpoints at
spacings .02,.01, requiring fine-grid/domain shifts <.01. Do not assume stability
before inspecting eigenvalues; positive finite-box values alone are not a
universal continuum stability proof or a live-matter test.

Scatter small-amplitude waves from vacuum at p/m_out=.001,.1,1,3. Interior
outgoing condition for propagating waves, decaying condition for forbidden
energies. Compare conserved flux R+T to 1 (<1e-6); repeat on both domains
(<1e-5). These are four specified energy sensitivities, not a reservoir spectrum.
Mutation drops the matter term from the interior first integral and must fail
surface derivative matching. Timeout60s, one numerical thread.
