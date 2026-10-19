# QCD-E independent mixed chiral derivation

Saved before reading the coordinator's independent derivation. Inputs are the already authenticated chiral vacuum and baryon actions, with common positive light-quark mass varied at fixed ratio, fixed strange quark mass and fixed strong reference theory. The electric-charge derivative is taken at zero charge first.

Write \(M^2=B(m_u+m_d)\), \(z=m_u/m_d>0\) fixed. \(F_0,Z_0,g_0\) are the light-quark chiral-limit SU(2) LECs at the fixed strange mass. They are constants of the EFT, not functions fitted at each \(M\).

\[
V(M)\equiv \left.\partial_{e^2}{\chi(M,e^2)\over\chi_0(M)}\right|_{e^2=0}
=K_\chi^r(z)-{Z_0\over8\pi^2}
 [1+\log(M^2/\bar\mu^2)]+\cdots,
\]
\[
B_p(M)\equiv\left.\partial_{e^2}m_p(M,e^2)\right|_{e^2=0}
=L_p-{3g_0^2Z_0M\over16\pi}+\cdots.
\]
Here \(\chi_0=F_0^2M^2z/(1+z)^2\),
\(K_\chi^r=(20/9)(k_5^r+k_6^r)+(4/9)(1+3\Delta)k_7^r\),
\(\Delta=(1-z)/(1+z)\), and
\(L_p=-F_0^2(f_1+f_3+f_2)/2\) in the operator-defined convention of the frozen report.

Therefore the two mass-shape derivatives are
\[
D_\chi=M^2\partial_{M^2}V(M)=-{Z_0\over8\pi^2}+\cdots,\qquad
D_p=\partial_M B_p(M)=-{3g_0^2Z_0\over16\pi}+\cdots.
\]
The counterterm-independent leading relation is
\[
\boxed{\quad {D_p\over D_\chi}={3\pi\over2}g_0^2,\qquad
\mathcal U(M)\equiv {2D_p\over3\pi g_0^2D_\chi}=1
\quad}
\]
within the retained meson \(O(e^2p^2)\) and baryon \(O(e^2p)\) terms, provided \(Z_0g_0\ne0\). The unknown \(Z_0\) cancels; \(F_0\) already cancels between the leading pion mass shift and the loop vertices.

At the next meson orders, local \(e^2M^2\) terms in the fractional susceptibility and \(e^2M^2\log^k M^2\) loop terms generate \(D_\chi\) corrections vanishing as \(M^2\log^k M^2\). Baryon \(e^2M^2\) terms and \(e^2M^2\log M^2\) terms generate \(D_p\) corrections of order \(M\log^k M^2\). Thus the relation is a leading infrared asymptotic prediction under the EFT's regular chiral expansion; it is not an exact finite-mass identity. The pion-nucleon gap to other explicit baryons is held nonzero; a simultaneous degenerate-Delta limit changes the EFT.

The order of limits matters. Keeping the leading charged mass
\(\Delta_\pi^2=2e^2F_0^2Z_0\) inside one loop gives
\[
D_\chi(M,e^2)=-{Z_0\over8\pi^2}{M^2\over M^2+\Delta_\pi^2},\qquad
D_p(M,e^2)=-{3g_0^2Z_0\over16\pi}
 {M\over\sqrt{M^2+\Delta_\pi^2}},
\]
for the corresponding derivatives before setting \(e^2=0\). Their ratio is
\[
{D_p(M,e^2)\over D_\chi(M,e^2)}
={3\pi g_0^2\over2}\sqrt{1+{\Delta_\pi^2\over M^2}},
\]
which has no finite \(M\to0\) limit at fixed positive charge. The required operation is \(e^2\to0\) derivative at each \(M>0\), then mass derivative, then the chiral limit.

For a chirally regular mass-independent scheme change
\(m_i'=m_i(1+e^2a_i+\cdots)\), holding primed masses fixed adds
\(-\sum_i a_i m_i\partial_{m_i}\chi_{\rm QCD}/\chi_0\) to \(V\).
Its LO part is constant at fixed \(z\), so \(D_\chi\) removes it. The analogous proton shift starts at \(M^2\), so its mass derivative vanishes in the chiral limit. Fixed-UV QED running gives such constant \(a_i\), not new independently adjustable infrared logarithms.

This restriction is essential: a mass-dependent prescription
\(a_i(M)\propto\log M^2\) shifts the leading \(D_\chi\) constant. A prescription that changes the physical inputs as \(M\) varies is a different path. An electromagnetic pion mass used as the varying coordinate can likewise mix the mass and charge derivatives. Use the \(e=0\) pion coordinate and state the mass/strong matching prescription.

The normalization can be made directly measurable by replacing \(\chi_0(M)\) with the separately computed \(\chi(M,0)\), or by using \(\partial_{e^2}\log\chi|_0\). The difference is higher chiral order; it must not be called an exact equality at finite \(M\). Similarly \(g_A(M,0)\) may replace \(g_0\) in \(\mathcal U\) for the asymptotic test.

This is a cross-sector flat-space infrared consistency test. It is not the fixed-proton mass path, does not determine a geometric stress-energy coefficient, and does not select alpha.
