# Finite bound identified-medium equilibrium, before computation

Test gamma=0 identified-medium model, not independent A33: fixed extended Plummer baryons gNb=r/(1+r²)^(3/2), dimensions GMb=a0=rM=1. Let m be enclosed cold mass in Mb units, q=m/r²<1, and effective relative potential Psi=Ecut-mu. Then m'=r² rho_hat and Psi'=q²/(1-q)-gNb.

Use an explicitly positive anisotropic distribution f(Q)=F Q_+, Q=Psi-v²/2-L²/(2ra²). Velocity integration gives rho_hat=A Psi^(5/2)/(1+r²/ra²), with positive A absorbing constants. This has isotropic centre and increasingly radial orbits. Integrate from rmin1e-6 to the first Psi=0 (edge), or q=0.99 (invalid-cap proximity), or radius100. Scan Psi_c=0.2,0.5,0.8, A=0.1,1,10 and ra=0.5,1,3. Report all outcomes, do not hide failures. Boundness must be checked using the exterior effective potential mu'=gNb-R(m_edge/r²), rather than assuming every Psi zero confines all orbits.

For successful finite cases verify positive density, q<1, inward edge force, conserved exterior mass and potential depth to infinity, and convergence of edge/mass under solver refinement. This is an equilibrium family, not formation, stability, a selected source fraction, finite stiffness or observational validation.

Post-scan checks: record q and total gravity relative to the native cold algebraic law at0.1,0.5,0.9 of each edge, without using this as an observational pass. Verify the distribution's Jeans identity with p_r=2rho Psi/7 and beta_anis=r²/(r²+ra²). The exterior force ratio R/gNb decreases monotonically when r²>m, since d ln(R/gNb)/dr=3r/(1+r²)-3/r-2r/(r²-m)<0. Thus inward edge force plus cap avoidance certifies an inward exterior in this point-free Plummer/gamma0 model; the sampled exterior check is supplementary.
