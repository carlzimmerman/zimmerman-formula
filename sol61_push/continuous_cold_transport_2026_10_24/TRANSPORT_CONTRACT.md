# CCT-002: measured anisotropic wave transport

This contract precedes the simulation. Scope: isolated dimensionless Schrodinger–Poisson candidate from CCT-001, G=M=1, eta=0.7. Not v3s, no derived acceleration-law coupling, no four-dwarf initial histories or stellar likelihood. A gravity-law coupling failure is not repaired by numerical contraction.

Initial Gaussian widths (4,2,2); potential phase S=-0.03 r^2/2 + beta xy, beta in {0,+0.03,-0.03}. This irrotational shear gives nonzero total angular momentum for the elongated cloud; it is not rigid-body rotation. No hand-inserted compact core. Normalise total mass to one. Periodic cube L=24, Poisson zero mode removed, absorbing layer r>9 with damping 0.15 ((r-9)/3)^4. The layer is a disclosed numerical boundary, not microscopic dissipation. Directly ledger all changes it causes in mass, total Hamiltonian and Jz; negative energy removal is NOT certified escaping radiation. Cubic periodic gravity may torque the cloud; measure the residual explicitly.

Run N=48 (zero,+,- spin), N=64 (+ spin), and N=48 half-step (+ spin). T=30, dt=0.06 or 0.03, one numerical thread, nice 15. Expected arrays well below 1 GB; no other experiments or queued jobs touched. Save scalar histories only.

Numerical gates: relative Hamiltonian ledger residual <=1%; spin ledger residual <=2% of initial |Jz|; parity mass/energy/radius and J sign <=1%; finer-grid and half-step final mass, half-mass radius, energy-export and J-export fractions agree within 10% (fractions compared using absolute tolerance 0.01 as well). A failed gate prevents a converged transport claim. In this finite box we do not certify isolated-boundary convergence.

Exploratory transport target (not an observed dwarf threshold): positive net energy export, >=50% initial |Jz| exported for a spinning run, half-mass radius contracted by >=1.5, and final-quarter radius variation <=10%. Record each individually. If none or only some pass, preserve the distinction. Absorbing field tails can mimic escape; full physical certification needs larger boxes, outward positive-energy flux and boundary independence.

Analytic companion: in the conditional Gaussian core family C=3 sqrt(2 pi)/2 and eta=sqrt(G M_c R_c/C). If escaping waves are confined to |m|<=m_max and M_out/M_c=q, then lambda_removed=|Delta J|/[M_c sqrt(G M_c R_c)] <= m_max q/sqrt(C). Reuse the older Sextans receiver fraction only as a labelled conditional budget, not a present observational fit. Scan q={0.001,0.01,0.01146/(1-0.01146),0.1} and m_max={0,1,2,4,8}; retain all outputs.

No per-dwarf efficiencies, spin or eta fits. No theorem that gravity can distinguish all four. No publication, push, automatic monitor or shared frozen edits.
