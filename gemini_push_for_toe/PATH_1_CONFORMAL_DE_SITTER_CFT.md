# Path 1: Conformal de Sitter CFT and the $SO(4,1)$ Interface

---

## 1. The Physics: Conformal Symmetry in deep-MOND

In the deep-MOND limit ($g \ll a_0$), the gravitational acceleration of a test particle around a mass $M$ is given by:
$$g = \sqrt{g_N a_0} = \frac{\sqrt{G M a_0}}{r}$$

Milgrom (2009, arXiv:0906.5377) demonstrated that the equations of motion in this limit are invariant under the **conformal group of 3-dimensional Euclidean space**, which is isomorphic to **$SO(4,1)$**—the isometry group of 4-dimensional de Sitter space ($dS_4$). 

Under a conformal transformation $x^i \to x'^i$, the coordinates transform while preserving angles, and the deep-MOND force law remains form-invariant. This is a highly non-trivial symmetry. In standard Newtonian gravity, the symmetry group is the Galilean group (which is not conformal). In General Relativity, the isometry group of a Schwarzschild mass is just $SO(3) \times \mathbb{R}$ (rotations and time translations). The emergence of the full de Sitter isometry group $SO(4,1)$ in the non-relativistic, low-acceleration regime is a direct mathematical link between galactic dynamics and the cosmological vacuum.

---

## 2. Strominger's dS/CFT Duality

Strominger (2001, arXiv:hep-th/0106113) proposed the **dS/CFT correspondence**, which states that quantum gravity on a $dS_d$ space is dual to a conformal field theory (CFT) residing on the future boundary $\mathcal{I}^+$ (future infinity). 

For $dS_4$, the boundary $\mathcal{I}^+$ is a 3-dimensional Euclidean space. The isometry group of the bulk spacetime ($SO(4,1)$) acts as the conformal symmetry group of the boundary CFT. 

```
               Future Infinity (I+) — 3D Conformal Boundary (Euclidean CFT)
                                  |
                                  | (dS/CFT Duality: SO(4,1) Isometry -> Conformal Symmetry)
                                  v
                  Bulk dS4 Spacetime — (1+3)D de Sitter Space
                                  |
                                  | (IR Limit: Physical distance r -> infinity, g << a0)
                                  v
                       Galactic Scales (deep-MOND)
```

In the boundary CFT:
* Spacetime translation in the bulk time coordinate corresponds to a renormalization group (RG) flow in the CFT.
* Physical distance $r \to \infty$ in the bulk (which is the deep-MOND limit where $g \ll a_0$) maps to the extreme **Infrared (IR) limit** of the CFT.
* The MOND scale $a_0$ acts as the UV/IR transition boundary. For accelerations $g \gg a_0$, the conformal symmetry is broken, and we recover Newtonian/GR behavior. For $g \ll a_0$, the conformal symmetry $SO(4,1)$ is restored.

---

## 3. The Unification Pathway

This pathway proposes that **the galactic dark sector (MOND dynamics) is the IR limit of the boundary CFT dual of de Sitter space**. Instead of dark matter being a physical particle in the bulk, it is a holographic manifestation of boundary CFT correlators in the IR.

### Steps to Build the Bridge:
1. **Define the Boundary Theory:** Formulate the specific boundary CFT whose operator spectrum reproduces the bulk gravitational field in the presence of a point source. The boundary stress-energy tensor $\langle T_{ij} \rangle$ must encode the $1/r$ force law in the IR.
2. **Holographic Reconstruction:** Use boundary-to-bulk propagators to reconstruct the bulk metric perturbations. The emergent field equations must yield the MOND relation $g \propto 1/r$ at large distances, while matching GR at short distances.
3. **The DSSYK Connection:** Double-Scaled SYK is a $(0+1)$D quantum system whose chord algebra describes $dS_2$ JT gravity. To model $dS_4$, we must construct a spatial network (tensor network) of DSSYK nodes on the 3D boundary. The large-N scaling of the SYK fermions must map to the conformal fields on $\mathcal{I}^+$.

### Open Research Questions:
* *How is the conformal symmetry broken at $g \approx a_0$?* In the CFT, this must correspond to an operator getting a vacuum expectation value (VEV) that triggers an RG flow away from the conformal fixed point.
* *Can this realize the Standard Model?* If the boundary CFT contains fields carrying internal gauge charges ($SU(3) \times SU(2) \times U(1)$), these fields would propagate in the reconstructed bulk. The challenge is ensuring these emergent bulk fields are chiral.
