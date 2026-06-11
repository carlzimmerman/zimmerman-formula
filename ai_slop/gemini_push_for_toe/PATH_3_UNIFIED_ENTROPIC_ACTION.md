# Path 3: Unified Entropic Action and Horizon Thermodynamics

---

## 1. The Physics: Jacobson's GR and Verlinde's MOND

The thermodynamic origin of gravity rests on two major papers:
1. **Jacobson (1995, arXiv:gr-qc/9504004):** Derived the full Einstein field equations of General Relativity from the Clausius relation $\delta Q = T dS$ on local Rindler horizons, using the Bekenstein-Hawking area law for entropy:
   $$S_{\text{area}} = \frac{A}{4 \ell_{\text{Pl}}^2}$$
2. **Verlinde (2016, arXiv:1611.02269):** Proposed that a positive cosmological constant $\Lambda$ gives the cosmic horizon a thermal, **volume-law** entanglement entropy:
   $$S_{\text{volume}} = \frac{V}{\ell_{\text{Pl}}^2 L_0}$$
   where $L_0 = \sqrt{3/\Lambda}$ is the de Sitter horizon radius. Displacing this entropy by adding a mass $M$ induces an elastic response in the holographic screen, recovering the MOND relation $g = \sqrt{a_0 g_N}$ for low accelerations.

---

## 2. The Covariant Completion Problem

While both derivations are physically compelling, they are heuristic. In particular, Verlinde's entropic gravity lacks a covariant action. Standard attempts to make MOND covariant (such as Bekenstein's TeVeS or Skordis & Złośnik's AeST) do so by **classically adding fields and ad-hoc potentials** to the Einstein-Hilbert action:
* **TeVeS:** Uses a scalar, a vector, and a tensor field, but suffers from stability issues and is strongly constrained by GW170817 (which requires gravity and gravitational waves to travel at the same speed).
* **AeST:** Survives the CMB and GW170817 by coupling a vector field $A^\mu$ to a scalar field $\phi$, but faces Solar System (Cassini) quadrupole constraints. It is a highly complex, tuned action rather than a clean derivation.

This pathway proposes to bypass these classical field-construction issues by formulating a **unified entropic action** where both GR and the $a_0$ correction emerge from a single thermodynamic functional.

---

## 3. The Unification Pathway

Instead of postulating fields, we postulate a generalized **horizon entropy functional** $S_{\text{tot}}$ that incorporates both area and volume terms:
$$S_{\text{tot}} = S_{\text{area}} + S_{\text{volume}} = \int_{\mathcal{H}} \left( \frac{1}{4 \ell_{\text{Pl}}^2} + \gamma \frac{r}{\ell_{\text{Pl}}^2 L_0} \right) dA$$
where $\mathcal{H}$ is the horizon, $r$ is the local horizon radius, and $\gamma$ is a dimensionless O(1) coupling.

```
                      Unified Entropy Functional: S_tot = S_area + S_volume
                                                 |
                       +-------------------------+-------------------------+
                       |                                                   |
                       v (Jacobson δQ=TdS)                                 v (Verlinde displacement)
               General Relativity (GR)                              MOND (a0 ~ c²√Λ)
               - Area law                                           - Volume law
               - Strong accelerations                               - Low accelerations
```

### Steps to Build the Bridge:
1. **Formulate the Covariant Entropy Density:** Define the entropy density on an arbitrary null hypersurface (horizon) in terms of covariant geometric quantities. The volume term must be mapped to a vector field $A^\mu$ (representing the horizon's normal/aether flow) such that its expansion $\theta = \nabla_\mu A^\mu$ tracks the volume-to-area ratio.
2. **Apply the Thermodynamic Variation Principle:** Vary the generalized entropy functional with respect to the metric and the boundary coordinates. Show that the stationarity of the entropy ($\delta S_{\text{tot}} = 0$ at equilibrium) yields the Einstein equations with a MONDian correction term of the form $\mathcal{K}(\mathcal{Q})$, where $\mathcal{Q}$ is the covariant acceleration.
3. **Determine the $a_0(z)$ Evolution:** Because the volume term is explicitly scaled by the cosmic horizon size $L_0(z) \propto 1/H(z)$ (or the event horizon size), the resulting field equations will naturally contain a time-dependent acceleration scale $a_0(z) \propto 1/L_0(z)$, deriving the DESI-locked evolution from the horizon's expansion.

### Open Research Questions:
* *How do we avoid Cassini violations in the Solar System?* The entropic action must naturally suppress the volume-law contribution in regions of high curvature (near massive bodies) where the area law dominates, leading to an automatic "screening" effect.
* *Does the entropic action yield the correct deep-MOND sign?* We must prove that varying the volume-law term leads to gravity enhancement ($g \propto 1/r$), which requires the DSSYK center state to be stable.
