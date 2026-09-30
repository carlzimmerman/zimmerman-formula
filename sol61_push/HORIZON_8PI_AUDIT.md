# What would r_H² Lambda=8pi mean?

Added goal question: “why r_H² Lambda=8pi.” The symbol r_H was not defined in that message. A text clarification is pending. This audit preserves the original 32pi target and checks several meanings without silently identifying a density length with a geometric horizon.

Use rho_Lambda as mass density in SI, so Lambda=8pi G rho_Lambda/c². This Einstein conversion factor does not independently select a galaxy acceleration.

| Defined radius | Product Lambda r² | Meaning |
|---|---|---|
| R_H=c/H | 3 Omega_Lambda, where Omega_Lambda=Lambda c²/(3H²) | Hubble length; generally epoch and slicing dependent |
| R_dS=sqrt(3/Lambda) | 3 | De Sitter geometric horizon |
| R_rho=c/sqrt(G rho_Lambda) | 8pi | Density-defined length; not the standard de Sitter horizon |
| R_acc=c²/a0 | 32pi, conditional on the target | Acceleration length; this just rewrites the target |
| R_half=c²/(2a0) | 8pi, conditional on the target | Half acceleration length; also just rewrites the target |

For the Hubble definition, multiplication is immediate: Lambda(c/H)²=3Omega_Lambda. In a spatially flat cosmology with nonnegative other energy densities, Omega_Lambda<=1, so the product is at most 3. It cannot be 8pi in that class. Do not extend this bound to arbitrary closed cosmologies: the Hubble length can exceed a geometric horizon and Omega_Lambda can exceed one. In closed-slicing pure de Sitter, for example, H=H_dS tanh(H_dS t), so the product is 3/tanh²(H_dS t). It equals 8pi at a particular time, not as a universal horizon identity.

The flat pure-vacuum Friedmann equation gives H_dS²=Lambda c²/3. The invariant de Sitter horizon therefore has R_dS² Lambda=3. Its static metric lapse is 1-Lambda r²/3. At the density-defined R_rho, that lapse is 1-8pi/3, rather than zero; R_rho/R_dS=sqrt(8pi/3). Calling R_rho a de Sitter horizon would change the geometric meaning.

The identity for R_rho follows solely by substitution:

Lambda R_rho²=(8pi G rho_Lambda/c²)(c²/(G rho_Lambda))=8pi.

The 32pi puzzle is then equivalent to the *additional physical claim* a0=c²/(2R_rho), or a0=(c/2)sqrt(G rho_Lambda). Multiplying the density identity by four reproduces the target, but provides no new selection of the factor one-half. Likewise, defining R_half from a0 and imposing the 8pi identity is circular unless that radius and its gravitational response are independently derived.

Primary convention check: [PDG 2026 Big-Bang Cosmology](https://pdg.lbl.gov/2026/reviews/rpp2026-rev-bbang-cosmology.pdf), revised August 2025, Section 22.1.3–4, Eqs. (22.6),(22.8),(22.11), and Omega_Lambda definition. The source uses c=1; factors of c above restore SI mass-density conventions. Its Friedmann and density definitions support the Hubble dictionary. De Sitter and density-length products above are direct algebraic consequences, not a new theorem or a fitted numerical result.

Decision: the added equality is definition-dependent. It is not established for an unspecified r_H. Once the user's radius definition is supplied, retain only the applicable physical interpretation. No result here solves the original common-theory obligation.
