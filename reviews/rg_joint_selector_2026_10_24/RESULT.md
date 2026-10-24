# Can quantum flow select the MOND/vacuum ratio?

No joint microscopic selector was obtained. The new result is a precise distinction between three claims: an RG-invariant ratio, a ratio independent of free trajectory data, and an observed force coefficient. Only the second, together with a healthy force calculation, would answer the request. The current evidence supplies neither a microscopic beta-function system for the required three amplitudes nor a unique allowed matching trajectory.

Base 095fd76b2ec5d399f0bc7fc7274fb32bd3272f9a; freeze 4020715cf3. Parent: ../condensate_joint_matching_2026_10_24/RESULT.md. Kappa=1/2 remains FITTED; CFG493 kappa_Lambda=0.417 +/- 0.095 and kappa_crit=0.345 +/- 0.078 are separate, unused inputs. Dark-energy footing; c=hbar=1. No numerical kappa output or hit claim.

## 1. What actually needs to be fixed

The parent derived a0=q^3/(4pi G C) from the sourced cubic action and conditionally matched

C=c3 Lambda, q=cb Lambda/Mpl, epsilon_DE=c0 Lambda^4.

Consequently

K = a0/sqrt(G epsilon_DE) = 2sqrt(8pi) cb^3/(c3 sqrt(c0)).       (1)

It is stronger than necessary to require each amplitude to be individually unique. They may vary along physical trajectories while the combination (1) remains fixed. Let p_A denote all independently allowed microscopic boundary parameters after fixing units and any independently measured inputs. The real prediction test at the physical matching scale is

partial_pA ln K = 3 partial_pA ln cb - partial_pA ln c3
                 - (1/2) partial_pA ln c0 = 0                  (2)

for every free direction throughout the connected allowed family. A stationary point at one specially chosen parameter value is insufficient. If the family has disconnected branches, their values must also be compared. Stability and the force-law dictionary remain separate requirements.

For a logarithmic tangent vector v=(v0,v3,vb), the local test is

(-1/2,-1,3) dot v = 0.

For example, the exact paths with tangent vectors (6,0,1) and (0,3,1) preserve K while the individual coefficients change. These are algebraic examples showing what could work, not derived RG eigenvectors of a microscopic theory. They must not be promoted into dynamics by naming them an attractor.

## 2. An RG invariant is not a prediction

Writing beta_i=d c_i/d ln k gives

d ln K/d ln k = 3 beta_b/cb - beta_3/c3 - beta_0/(2c0).          (3)

Setting the right-hand side to zero only says that K does not run at that point or along the specified trajectory. It does not choose its value across trajectories. All beta functions could vanish while there is a continuous fixed family with different K. Conversely, a predictive theory can have a running K at intermediate auxiliary scales and still produce a unique physical endpoint. Equation (2), applied to the full matching map, is the relevant test.

Near a UV fixed point, allowed relevant directions come with free amplitudes. Their projection into the physical matching coefficients, including nonlinear evolution and thresholds, has to obey (2). Orthogonality checked only at the UV linearization is not enough when the critical surface curves. An actual computation of this map is missing; no beta functions for cb or the nonanalytic MOND operator have been invented here.

## 3. A matter fixed point cannot remove an arbitrary vacuum offset by itself

There is an exact obstruction under explicit hypotheses: quantize matter on a fixed external metric, with the same field-independent regulator and measure in the two theories. Do not integrate over the metric. Add a constant vacuum density Delta epsilon to the microscopic action:

S'[phi;g]=S[phi;g]+Delta epsilon integral sqrt(g).

This term factors out of the matter path integral. The normalized matter correlation functions are unchanged, and the effective action shifts by the same term. Equivalently its matter-field Hessian vanishes. Thus the matter-only functional RG has the same right-hand side in both theories, and

Delta epsilon_k=Delta epsilon,
Delta v(k)=Delta epsilon/k^d,
k partial_k Delta v=-d Delta v.                              (4)

Here d is spacetime dimension. In four dimensions the vacuum difference is a relevant perturbation with critical exponent 4: it vanishes in dimensionless units toward arbitrarily high k, but remains an arbitrary dimensionful constant at low energies. Requiring the same matter UV fixed point therefore does not fix it. Gravitating that effective action makes this surviving offset consequential.

This is more general than the earlier one-loop curvature-tracker test, but it is not a quantum-gravity theorem. A metric variation differentiates sqrt(g); with dynamical metric fluctuations the gravitational Hessian changes, so the above proof does not apply. Nor does it establish identical on-shell cosmologies for shifted vacua: the comparison holds on the same external background while matching matter response. A principle restricting the permitted vacuum boundary term is additional input.

## 4. Test gravitational escapes using actual primary results

### Coupling selection through asymptotic safety

[Emergence of Horndeski gravity from asymptotic safety?](https://arxiv.org/html/2609.29369v1), Eichhorn, Fernandes and Willaschek, v1, 2026-09-24: inspected equations 10-18, 28-29 and section 2.3. The truncation relates curvature-derivative scalar couplings to a cosmological-constant trajectory parameter. Imposing the Horndeski ratio selects a trajectory; its converged endpoint has negative cosmological constant. A positive counterpart encounters an unresolved IR singularity. Matter is omitted. Neither the MOND cubic nor its baryon portal is calculated. This is a concrete partial example of gravitationally correlated coefficients, but not the requested joint matching. Its operator ratio -1/2 is unrelated to the campaign's kappa.

A further direct operator check: the cited scalar truncation preserves phi -> -phi and phi -> phi+constant. A linear term phi rho_b breaks both, so that specific portal is excluded on its symmetry-preserving constant-scalar branch, rather than assigned a useful nonzero value. Scalar-metric mixing on another background could mediate forces through a different matching dictionary; this observation does not exclude that possibility. It is not supplied by equating the two curvature couplings.

### Infrared vacuum screening

[Infrared Screening of the Cosmological Constant](https://arxiv.org/html/2609.29979v1), Branchina, Gandolfo and Pernace, v1, 2026-09-24: inspected equations 5-10, 21-27 and the supplemental setup. It reports Lambda_cc(k) approximately A k^2 within an Einstein-Hilbert plus R^2 calculation using frozen G and R^2 coupling and a single-mode shell saddle. The physical endpoint is identified with an inverse cosmological size. The calculation contains no matching for C or q. We have not independently reproduced its gravity flow, and treat its conclusion as a reported truncation result, not an established microscopic solution.

One can test a proposed closure without assuming a numerical A. Suppose the final constant couplings obey Lambda_cc=A k_IR^2, and set k_IR=xi H. The four-dimensional vacuum Einstein equation gives

3H^2=A xi^2 H^2.

For nonzero H this fixes xi^2=3/A but leaves H arbitrary. Rescaling H and k_IR together preserves the equations. Thus this closure alone does not select an absolute nonzero vacuum scale. This is our conditional algebraic test, not a refutation of the paper: an independently determined cosmological size, boundary condition or further field equation could supply a scale. We have not replaced the endpoint equation with a spacetime-dependent RG-improved action. The unknown MOND matching is a separate gap even if the vacuum-screening claim is granted.

## 5. What changed and what remains open

The fixed-point route is more sharply posed now. It does not need three individually unique numbers; it needs the physical invariant (1) to be independent of every allowed free parameter. Matter-only flow fails that test through an explicit vacuum-offset direction. Full quantum gravity can evade that obstruction, and published calculations do correlate some coefficients, but the checked examples do not compute the required operator set or its baryon source.

No microscopic symmetry, beta-function system or boundary principle satisfying (2) has been established here. Simply writing a flow whose stable point is the desired K would insert the answer. A genuine continuation requires a specified microscopic action generating a healthy MOND operator, then its vacuum and matter-source matching from the same quantum calculation. Repeating the ratio algebra or choosing a convenient RG stopping scale would not close this gap.

Evidence: check.py passes 11/11 symbolic identities. The separate mutation changes the vacuum critical sign and a ratio weight; both assertions fail, with nonzero exit. This verifies algebra, not the proposed gravitational models or a microscopic mechanism. No fitted input, scan, numerical kappa, source-code beta integration or global cosmological solution was used.
