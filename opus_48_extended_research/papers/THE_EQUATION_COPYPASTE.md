# The field theory in one equation — copy/paste versions

Three forms of the same thing: LaTeX (display), LaTeX (align, for a paper), and plain
Unicode text (for email, Slack, a talk slide). All are the same equation.

---

## 1. LaTeX — single display equation

```latex
\begin{equation}
S=\int d^{4}x\sqrt{-g}\left\{\frac{R-\tfrac{K_{B}}{2}F^{\mu\nu}F_{\mu\nu}+2(2-K_{B})J^{\mu}\nabla_{\mu}\varphi-(2-K_{B})Y}{16\pi G}+\frac{\kappa^{2}\mathcal{P}}{8\pi}\,\mathcal{F}_{Y}\!\left(\frac{Y}{\kappa^{2}G\mathcal{P}}\right)-\mathcal{P}\right\}+S_{\mathrm{m}}[g,\psi]
\end{equation}
```

with

```latex
\begin{gather}
\mathcal{P}(Q)=M^{4}\sqrt{1-\frac{(Q-Q_{0})^{2}}{\Lambda_{D}^{2}}},\qquad
Q\equiv A^{\mu}\nabla_{\mu}\varphi,\qquad
Y\equiv\left(g^{\mu\nu}+A^{\mu}A^{\nu}\right)\nabla_{\mu}\varphi\nabla_{\nu}\varphi,\\
A^{\mu}A_{\mu}=-1,\qquad
\frac{d\mathcal{F}_{Y}}{dz}=1-e^{-\sqrt{z}},\qquad
M^{4}=\rho_{\Lambda}c^{2},\qquad
\kappa=\tfrac{1}{2}\ \text{(fitted)},\\
a_{0}^{2}=\kappa^{2}G\,\mathcal{P}\quad\Longrightarrow\quad
a_{0}=\kappa c\sqrt{G\rho_{\Lambda}}=9.36\times10^{-11}\ \mathrm{m\,s^{-2}}\ \ \text{today.}
\end{gather}
```

---

## 2. LaTeX — broken over lines (for a two-column paper)

```latex
\begin{align}
S=\int d^{4}x\sqrt{-g}\,\Bigg\{
&\frac{1}{16\pi G}\Big[R-\frac{K_{B}}{2}F^{\mu\nu}F_{\mu\nu}
+2(2-K_{B})J^{\mu}\nabla_{\mu}\varphi-(2-K_{B})Y\Big] \nonumber\\
&+\frac{\kappa^{2}\mathcal{P}}{8\pi}\,
\mathcal{F}_{Y}\!\left(\frac{Y}{\kappa^{2}G\mathcal{P}}\right)
-\mathcal{P}\Bigg\}+S_{\mathrm{m}}[g,\psi],
\end{align}
```

---

## 3. Plain Unicode text — for email, Slack, or a slide

```
S = ∫ d⁴x √−g { [ R − (K_B/2)F^μν F_μν + 2(2−K_B)J^μ∇_μφ − (2−K_B)Y ] / (16πG)
                 + (κ²𝒫/8π) · 𝓕_Y( Y / κ²G𝒫 )
                 − 𝒫 }
    + S_m[g, ψ]

where

    𝒫(Q) = M⁴ √( 1 − (Q−Q₀)² / Λ_D² )        the dark sector: a pure DBI brane,
                                              tension M⁴ = ρ_Λ c²

    Q ≡ A^μ ∇_μ φ                             scalar gradient along the aether (temporal)
    Y ≡ (g^μν + A^μ A^ν) ∇_μφ ∇_νφ            scalar gradient orthogonal to it (spatial)
    A^μ A_μ = −1                              unit-timelike aether
    d𝓕_Y/dz = 1 − e^(−√z)                     interpolation (Milgrom & Sanders 2008, α=½)

and the one new identification:

    a₀² = κ² G 𝒫        "the MOND scale IS the dark sector's pressure"

    → today (Q = Q₀, 𝒫 = ρ_Λc²):  a₀ = κ c √(G ρ_Λ) = 9.36×10⁻¹¹ m s⁻²,  κ = ½ (fitted)
    → in the past (𝒫 smaller):     a₀(z) derived, flat below z ≈ 20, off at recombination
```

---

## 4. The one-paragraph gloss (if you need to say what it is out loud)

> The first term is Aether-Scalar-Tensor gravity — general relativity plus a unit-timelike
> vector carrying a cosmic frame plus a scalar, with matter coupled to the metric alone, so
> lensing and dynamics agree without a dark halo. The whole dark sector is the single
> function 𝒫, which is a Dirac–Born–Infeld brane of tension ρ_Λc²: at its minimum it is a
> cosmological constant with w = −1 exactly, small excitations of it are pressureless dust,
> and at the brane wall its pressure vanishes. The middle term is MOND, and its acceleration
> scale is not an independent constant — it is a₀² = κ²G𝒫, the dark sector's own pressure.
> One bounded function therefore delivers dark energy, dark matter and the MOND scale
> together. The price, stated plainly: κ = ½ is fitted (measured 0.551 ± 0.043), β = 1 is a
> selection, the dark-matter abundance is an integration constant, and whether the dust
> stays put inside galaxies is unsolved.

---

## 5. Attribution line (use it whenever the equation travels)

> The aether-scalar-tensor scaffold is Skordis & Złośnik, *Phys. Rev. Lett.* **127**, 161302
> (2021); the interpolation is Milgrom & Sanders, *ApJ* **678**, 131 (2008), Eq. (13) at
> α = ½. This framework contributes the normalisation a₀ = κc√(Gρ_Λ), the pressure
> promotion a₀² = κ²G𝒫, and the derived a₀(z).
