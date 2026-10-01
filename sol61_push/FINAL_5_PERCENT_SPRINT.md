# Final bounded attempt: microscopic counting and horizon temperature

Base: 8c925db215c913edc00e5af919129b3ddc0c63c6. User requested one final attempt within the remaining weekly usage. Original goal remains unresolved; this is the final saved checkpoint, not a breakthrough claim.

## Quantized mode count leaves a continuous interaction

For the previously checked neutral planar Dirac mechanism, cubic bulk capacity is C0=nu d y³/(6pi v²), where nu is surface area per volume, d is the negative-band degeneracy, v is tangential speed, and m=yP. The conditional reduced dictionary gives a0=2M²/(3C0). Holding the same vacuum curvature and mode count fixed while changing y to t y changes Lambda/a0² by t^6. This is not a field redefinition: the physical polarization normalization is already fixed by its gravitational quadratic term and coupling to acceleration. Its interaction y remains free unless an independent microscopic principle fixes it.

At P=0 the free-band spectrum and its thermal free energy do not depend on y. Thus fixing an integer d does not itself tie vacuum energy to the polarization response. This is an obstruction to mode counting alone, not to all possible symmetries or microscopic completions.

## A concrete horizon-temperature attempt

Consider actually thermally populated, free neutral planar fermions at T>0. Retain the earlier zero-temperature analytic subtraction. Per area, their grand potential is

Omega(m,T)=d m³/(6pi v²)−d T/(pi v²) integral_m^infinity E log(1+exp(−E/T)) dE.

The thermal factor includes particle and hole excitations. Differentiating the lower integration limit gives

dOmega/dm=d T m log[2 cosh(m/(2T))]/(pi v²).

The small-m expansion is

Omega(m,T)−Omega(0,T)=d T log(2)m²/(2pi v²)+d m⁴/(32pi v²T)−d m⁶/(1152pi v²T³)+O(m⁸).

The zero-temperature cubic cancels in the strict infrared at any positive T. Removing the quadratic term with a matching counterterm leaves a quartic response, not the desired cubic. Conversely, for m>>T the zero-temperature cubic response returns. The two limits T→0 and m→0 therefore require care.

In the existing frozen-expansion dictionary, b=g−P becomes

b=2TP log[2 cosh(yP/(2T))]/(y a0,b), a0,b=2H/beta.

Its infrared stiffness is delta_T=2T log(2)/(y a0,b). If, as an additional hypothesis, the actual surface temperature is the conventional de Sitter detector scale T=H/(2pi), then delta_T=beta log(2)/(2pi y). At the formal target Cb=3beta²/4=32pi, this is approximately 1.277/y. A small thermal cutoff therefore requires a separately selected sufficiently large y. It does not fix beta or the requested coefficient. Identifying the cutoff or temperature by hand merely supplies another relation to fit.

De Sitter detector thermality was used only as a conditional temperature substitution. No derivation equates the curved-space vacuum state to a preferred-frame planar gas, nor derives its gravitational stress. Web discovery found arXiv:2211.14747 and arXiv:1101.5235; an attempted HTML retrieval of the former failed. Search results are not proof of a state-transfer theorem. All free-band formulas above follow directly from the stated integral, not from an imported theorem. The horizon-temperature mechanism remains conditional at that physical transfer step.

## Evidence and stopping point

Eight exact identities pass in `thermal_surface_final_sprint.py`; the contract and validated manifest are saved under `contracts/thermal_surface_final_sprint.json` and `runs/thermal_surface_final_sprint/`. Checks cover the thermal logarithm, infrared series, absence of a cubic, zero-temperature limit, force limits, conditional temperature normalization, and continuous coupling freedom. They do not establish a healthy interacting theory or an observational fit.

This sprint did not force 32pi. The decisive missing input is still an independently derived constraint on the physical microscopic interaction and vacuum mechanism. Prescribing y, beta, a radius, or a subtraction to produce the answer would not satisfy the original goal. Stop research here to preserve usage; resume with this bottleneck rather than repeating the completed checks.
