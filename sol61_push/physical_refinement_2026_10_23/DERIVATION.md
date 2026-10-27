# Physically resolved spherical restriction

This is a restriction of the preferred-frame action in ../expanding_polarization_2026_10_23/DERIVATION.md, not a new covariant completion. Let A=a/a_initial, D=A^-1 grad, h=(delta rho_c-D.P)/chi. The background is imposed EdS; both material species are collisionless radial shells, with pressureless baryons. The angular mediator is zero. Spherical symmetry removes torques, nonradial instability and fragmentation by construction.

After angular integration divided by 4pi, cell and edge quadrature weights are v_i=(r_right^3-r_left^3)/3 and w_j=r_j^2 dr. G is the adjacent-cell gradient and D_r P is the difference of r^2 P fluxes divided by v_i. Therefore sum v f D_r P = -sum w (Gf)P with zero boundary flux. The discrete field energy is

 U_f = A^3 [sum w W(|P|) + sum v (delta rho_c-D_r P/A)^2/(2chi)
       + alpha/2 sum v(chi-1)^2 + d/(2A^2) sum w(Gchi)^2],

with W(p)=-p-log(1-p), eta=alpha=.005 and b=d=.125. Canonical field momenta used by the code are Q=A^3 Pdot and V=A^3 chidot, with the constant kinetic coefficients retained in forces/energy. Material momenta are pi=A^2 xdot. The corresponding forces are

 pi_c_dot=-grad_x(Phi+h), pi_b_dot=-grad_x Phi,
 eta Qdot=-A^3 [P/(1-|P|)+Gh/A],
 b Vdot=A^3 [h^2/2-alpha(chi-1)+d D_r Gchi/A^2].

Each shell deposits with reflected TSC weights. Its force differentiates these same weights, not a separately interpolated force grid. Positive shell masses solve the TSC assignment tridiagonal system so undeformed shells reproduce uniform density to floating point accuracy. The two conserved species means are subtracted separately. Radial Poisson flux is grad_x Phi=A^2 cumulative(sum v delta rho_total)/r^2; its weighted mean is zero. Origin crossings reflect position and radial momentum, allowing collisionless shell passage. There is no merger, drag, gas pressure, cooling prescription or absorbing boundary.

The finite-domain expansion-work identity is the preceding full-field identity, with the radial quadratures and the additional phase-gradient energy U_grad:

 dE/dlnA=-2T_m-3T_f-U_g+3(U_W+U_chi+U_mismatch)+U_grad
          +A^3 sum v h[-3 delta rho_c+D_r P/A].

Work against imposed expansion is not exported radiation. The reflecting domain stores field radiation and cannot certify escape to infinity. A constant comoving grid has increasing physical spacing; the grids here are chosen fine enough at the final time to resolve the reference radius radially. This is not adaptive 3D refinement.

## Initial minimum and history

The compensated radial displacement is xi(Q)=-epsilon sin(kQ)/(3k), k=pi/Rout. It vanishes at the outer boundary and has central linear density contrast epsilon. This is a deterministic radial sine seed, not a Gaussian random field. Initial dust velocity is H_initial xi. The canonical wavelength convention fixes R_L=.04037934389859046 Mpc and Rout_com=pi R_L size, not the mass of a pre-existing core.

Stationary fields obey P=-g/(1+|g|), g=Gh/A, and

 chi h - D_r[g/(1+|g|)]/A = delta rho_c,
 (alpha-d D_r G/A^2)(chi-1)=h^2/2.

A coupled sparse Newton solve with line search replaces an insufficiently converged L-BFGS attempt. A centered derivative of the minimum along dlnA and the specified dust displacement sets Pdot and chidot. Initial residual checks and derivative-step checks are necessary numerical checks; they do not establish that cosmology reaches this state.

For the earlier z2200 history, shoot its seed amplitude until the mass-weighted cold displacement sine projection at z1100 is .03 within 1e-4 fraction. Do not reset the fields or their momenta. This matches one matter mode, not the entire density/velocity state. Its remaining difference from a freshly prepared z1100 state cannot be assigned solely to the fields. No primordial probability measure, radiation-era transfer function, lapse/metric constraints or self-consistent Friedmann backreaction is supplied.

## Mass and binding diagnostics

Report cold mass by integrating the deposited density inside fixed physical radii, including a partial final cell. Sharp shell-count aperture masses are also retained but have shell-quantization jumps. Neither definition identifies a remnant boundary or selected mass.

For context only, combine both species inside a candidate radius, sort by physical r=A x, and compute T=sum m(Hr+pi/A)^2/2 and U=-sum_i m_i(M_inside_i+m_i/2)/max(r_i,s dr_physical), with s=.5,1,2. The self-shell term is explicit. This isolated Newtonian energy uses total physical velocity, not peculiar velocity alone. It omits the action's positive mismatch, polarization, phase and field kinetic energy, exterior/tidal contributions and a consistent reference/flux subtraction. Negativity is not sufficient for a bound core. Even diffuse weak seeds have negative values. Adding all positive field energy in the box gives a deliberately severe diagnostic, not a rigorous binding theorem or a physical assignment of that energy to the aperture.

To certify a mass-selected core still requires a converged finite central structure, a full-action binding/flux diagnostic, persistence rather than continuing infall, and robustness to seed scale, field history, baryonic pressure and nonradial dynamics.
