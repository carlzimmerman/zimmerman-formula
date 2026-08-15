'use client'

import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-white">
      {/* Header */}
      <header className="border-b border-gray-200 bg-gray-50">
        <div className="max-w-5xl mx-auto px-6 py-4">
          <nav className="flex items-center justify-between flex-wrap gap-3">
            <div className="text-lg font-semibold text-gray-900">a₀ from the Cosmological Constant</div>
            <div className="flex items-center gap-6 text-sm">
              <Link href="/rar" className="text-gray-600 hover:text-gray-900">Galaxy data</Link>
              <Link href="/simulate" className="text-gray-600 hover:text-gray-900">Simulations</Link>
              <Link href="/office-hours" className="text-gray-600 hover:text-gray-900">Background</Link>
              <Link href="/ai-slop" className="text-amber-700 hover:text-amber-900 font-medium">Retracted work</Link>
              <a
                href="https://github.com/carlzimmerman/zimmerman-formula"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-600 hover:text-gray-900"
              >
                GitHub
              </a>
            </div>
          </nav>
        </div>
      </header>

      <div className="max-w-5xl mx-auto px-6 py-12">
        {/* Retraction notice, first thing on the page */}
        <aside
          role="note"
          className="mb-10 rounded-md border border-amber-300 border-l-4 border-l-amber-500 bg-amber-50 px-5 py-4 text-sm leading-relaxed"
        >
          <p className="font-semibold text-amber-900 mb-2">
            Retraction in force — read this before anything else
          </p>
          <p className="text-amber-900/90 mb-2">
            On <span className="font-medium">23 June 2026</span> the author publicly retracted, to
            approximately forty physicists, every theory-of-everything and Standard-Model claim
            previously made on this site — the fine-structure constant, the mass ratios, the
            &ldquo;19 first-principles derivations,&rdquo; the cube&times;sphere numerology, and the
            T³/Z₂ cosmic-topology claim. Those claims were wrong and are not being revived.
          </p>
          <p className="text-amber-900/90">
            The pages that carried them are kept for transparency, collected under{' '}
            <Link href="/ai-slop" className="underline font-medium hover:text-amber-950">
              Retracted work
            </Link>
            . This front page states the one claim that survived.
          </p>
        </aside>

        {/* Title */}
        <article className="mb-12">
          <h1 className="text-3xl md:text-4xl font-serif font-normal text-gray-900 mb-3">
            The MOND acceleration scale as a de Sitter curvature scale
          </h1>
          <p className="text-xl text-gray-600 mb-6 font-light">
            One claim: the acceleration scale of the mass-discrepancy&ndash;acceleration relation is set
            by the dark-energy density.
          </p>

          <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500 mb-8 pb-8 border-b border-gray-200">
            <span className="font-medium text-gray-700">Carl P. Zimmerman</span>
            <span className="text-gray-300">|</span>
            <span>Standing revision 4 &mdash; 30 July 2026</span>
            <span className="text-gray-300">|</span>
            <a
              href="https://github.com/carlzimmerman/zimmerman-formula/blob/main/STANDING.md"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              STANDING.md
            </a>
          </div>

          {/* The equation */}
          <section className="bg-gray-50 border border-gray-200 rounded-lg p-8 mb-4">
            <div className="text-center">
              <div className="font-mono text-xl md:text-2xl text-gray-900 mb-3">
                a₀ = κ c √(G ρ_Λ) = c H_Λ / Z
              </div>
              <div className="font-mono text-base text-blue-700 mb-4">
                κ = ½ &nbsp;&nbsp; Z = √(32π/3) = 5.78881 &nbsp;&nbsp; a₀ = 9.36 × 10⁻¹¹ m s⁻²
              </div>
              <p className="text-sm text-gray-600 max-w-2xl mx-auto">
                Realised as <span className="font-medium">modified gravity</span> — the modified-inertia arm
                was closed by lensing in August 2026 — with the exact relation
                g_obs² = g_bar² + a₀ g_bar and the Milgrom&ndash;Sanders (2008) kernel
                ν(y) = 1/(1 − e^(−√y)) as the operative interpolation.
              </p>
            </div>
          </section>

          {/* The credit line — mandatory, and it goes here, not in a footnote */}
          <section className="mb-10 rounded-md border border-gray-300 bg-white px-5 py-4 text-sm leading-relaxed">
            <p className="font-semibold text-gray-900 mb-2">Attribution — what is and is not original here</p>
            <p className="text-gray-700 mb-2">
              This law is <span className="font-medium">not new, and neither is its derivation</span>.{' '}
              <span className="font-medium">Milgrom (1999, Phys. Lett. A 253, 273, Eqs. 6&ndash;9)</span>{' '}
              derives this exact law from the de Sitter&ndash;Unruh balance <em>and</em> fixes its
              coefficient at a₀ = 2 c H_Λ. His Eq. (9) is identically the relation above &mdash; verified
              symbolically, difference exactly zero. The same law was independently re-derived
              entropically by <span className="font-medium">Pikhitsa (2010)</span> and{' '}
              <span className="font-medium">Klinkhamer &amp; Kopp (2011)</span>, both also landing on
              2 c H_Λ.
            </p>
            <p className="text-gray-700">
              So the de Sitter&ndash;Unruh argument does not leave the coefficient free &mdash; it
              predicts one, and that prediction is <span className="font-medium">11.58× the value used
              here</span>. What this programme actually contributes is therefore narrow and should be
              stated as such: a <span className="font-medium">re-normalisation of the coefficient to fit
              data</span> (κ = ½ in place of Milgrom&rsquo;s 2), plus the relativistic completion — the scale
              embedded in Aether&ndash;Scalar&ndash;Tensor theory — and its derived a₀(z).
              It is not a derivation of the law, and not a derivation of its scale.
            </p>
          </section>
        </article>

        {/* Earned */}
        <section className="mb-12">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">What is earned</h2>
          <div className="overflow-x-auto border border-gray-200 rounded-lg">
            <table className="w-full text-sm">
              <thead className="bg-gray-50">
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Result</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-gray-100">
                  <td className="py-3 px-4 text-gray-700">Radial-acceleration relation on SPARC (175 galaxies), the framework&rsquo;s own ν and a₀</td>
                  <td className="py-3 px-4 text-gray-900"><span className="font-medium">0.108 dex</span> at Υ = 0.70 — beats regular MOND&rsquo;s 0.122–0.140</td>
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-3 px-4 text-gray-700">The a₀-line, g_obs² − g_bar² = a₀ g_bar</td>
                  <td className="py-3 px-4 text-gray-900">Exact identity, verified</td>
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-3 px-4 text-gray-700">The κ reduction a₀ = κ c √(G ρ_Λ)</td>
                  <td className="py-3 px-4 text-gray-900">Every π, the 32 and the 3 cancel</td>
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-3 px-4 text-gray-700">Modified-inertia action (v1–v11); disformal lensing construction</td>
                  <td className="py-3 px-4 text-gray-900">Published; constraint structure machine-verified, zero frame degrees of freedom; lensing Cassini-safe and Ostrogradsky-free</td>
                </tr>
                <tr>
                  <td className="py-3 px-4 text-gray-700">Seven structural theorems</td>
                  <td className="py-3 px-4 text-gray-900">
                    Published 30 July 2026 —{' '}
                    <a
                      href="https://doi.org/10.5281/zenodo.21708842"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline"
                    >
                      DOI 10.5281/zenodo.21708842
                    </a>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        {/* Postulated */}
        <section className="mb-12">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            What is postulated — not derived, and not presented otherwise
          </h2>
          <ul className="space-y-3 text-sm text-gray-700">
            <li className="border-l-2 border-gray-300 pl-4">
              <span className="font-medium text-gray-900">κ = ½.</span> Its <em>value</em> is not
              derived. Ghost-freedom, unitarity and holography have each been shown insufficient to
              force it. This is a <span className="font-medium">one-parameter effective theory, not a
              zero-parameter derivation</span>. Z has the same status.
            </li>
            <li className="border-l-2 border-gray-300 pl-4">
              <span className="font-medium text-gray-900">The law itself is not the Euler&ndash;Lagrange
              equation of the published action.</span> It <em>does</em> arise variationally in a
              nonlocal, non-quadratic class — Milgrom&rsquo;s own virial construction — but only on the
              two-parameter family of circular orbits. Infinitely many extensions share that slice and
              none is written down. Milgrom&rsquo;s own status line still applies: &ldquo;we do not have
              a modified-inertia theory for MOND at the level of satisfaction achieved for
              modified-gravity formulations.&rdquo;
            </li>
            <li className="border-l-2 border-gray-300 pl-4">
              <span className="font-medium text-gray-900">Two footings are carried on every dimensional
              number</span>, always: canonical ρ_DE (a₀ = 9.36 × 10⁻¹¹) and alternative ρ_total
              (1.13 × 10⁻¹⁰).
            </li>
          </ul>
        </section>

        {/* Open liabilities */}
        <section className="mb-12">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Open liabilities, stated plainly</h2>
          <div className="space-y-4 text-sm">
            <div className="border-l-4 border-red-400 pl-4 py-2 bg-red-50/50">
              <div className="font-medium text-gray-900 mb-1">
                The exact law is in conflict with the inner-planet ephemerides
              </div>
              <p className="text-gray-700">
                Held to all accelerations, the relation implies a constant sunward anomaly of a₀/2 =
                4.68 × 10⁻¹¹ m s⁻² that never decays. Against the Earth 2σ limit derived from Sereno
                &amp; Jetzer (2006) that is <span className="font-medium">1278× too large</span>, and
                119&ndash;189× too large even after the framework&rsquo;s own external-field effect.
                Galaxy data does not require this: across SPARC the α = 1, α = 2 and α = ∞ tails fit
                within 0.0084 dex of one another. The honest reading is that the relation is an{' '}
                <span className="font-medium">infrared</span> statement — which costs nothing in
                galaxies but withdraws the claim that it is <em>exact</em>.
              </p>
            </div>
            <div className="border-l-4 border-orange-400 pl-4 py-2 bg-orange-50/50">
              <div className="font-medium text-gray-900 mb-1">Galaxy clusters</div>
              <p className="text-gray-700">
                η(R₅₀₀) = 2.33 median / 2.54 geometric mean on real eRASS1 (N = 9830) using the
                framework&rsquo;s own kernel — significant at 4.1/2.7/2.0σ against a 0.10/0.15/0.20 dex
                systematic floor. The cluster acceleration scale is 21.6× the framework&rsquo;s a₀. The
                framework&rsquo;s lower coefficient makes this <span className="font-medium">13.2%
                worse</span> than standard MOND. Real, soft, central, and shared with AeST by an
                in-corpus argument — not a published family-wide theorem.
              </p>
            </div>
            <div className="border-l-4 border-gray-400 pl-4 py-2 bg-gray-50">
              <div className="font-medium text-gray-900 mb-1">
                A correction that runs the other way, reported at equal weight
              </div>
              <p className="text-gray-700">
                The previously advertised &ldquo;6&ndash;8σ&rdquo; Lyman-α forest exclusion of the
                diffuse-baryon sector is <span className="font-medium">withdrawn</span>. Three defects
                compounded: the observed cutoff values were unsourceable, the error bar was invented,
                and the response kernel was evaluated at the Newtonian rather than the observed
                acceleration — inflating every significance by 1.9&ndash;5.6×. On the best estimator and
                the defensible error channel it is <span className="font-medium">0.4&ndash;0.9σ</span>:
                a weak, convention-dominated tension, not an exclusion.
              </p>
            </div>
            <div className="border-l-4 border-gray-300 pl-4 py-2">
              <div className="font-medium text-gray-900 mb-1">arXiv endorsement</div>
              <p className="text-gray-700">
                Remains the blocker on everything that matters. Nothing here has been through
                peer review.
              </p>
            </div>
          </div>
        </section>

        {/* Live tests */}
        <section className="mb-12">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">What would falsify it</h2>
          <p className="text-sm text-gray-700 mb-4">
            The forward tests are pre-registered before the data, with targets and signs frozen and
            hash-stamped. A confirmation that lands in the wrong place is scored as a kill.
          </p>
          <div className="overflow-x-auto border border-gray-200 rounded-lg">
            <table className="w-full text-sm">
              <thead className="bg-gray-50">
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Front</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Prediction</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Clock</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-gray-100">
                  <td className="py-3 px-4 text-gray-700">Wide binaries</td>
                  <td className="py-3 px-4 text-gray-700">
                    In force (Amendment 10, Aug 2026): γ_v = 1.1614&ndash;1.1814 canonical / 1.1917&ndash;1.2267
                    alt footing, no-verdict edge 1.23 — hash-stamped, amended in the open before
                    data. Earlier targets (1.09, 1.1582) superseded on the record.
                  </td>
                  <td className="py-3 px-4 text-gray-500">Gaia DR4, Dec 2026</td>
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-3 px-4 text-gray-700">Lorentz-violation dipole s<sup>TX</sup></td>
                  <td className="py-3 px-4 text-gray-700">
                    Sign frozen negative; margin 1.50× / 1.24× on the two footings
                  </td>
                  <td className="py-3 px-4 text-gray-500">Gaia DR4</td>
                </tr>
                <tr>
                  <td className="py-3 px-4 text-gray-700">a₀(z) evolution</td>
                  <td className="py-3 px-4 text-gray-700">
                    Bump-then-decline, not a monotonic rise. Dissolves if w → −1.
                  </td>
                  <td className="py-3 px-4 text-gray-500">DESI, ongoing</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        {/* Where to look */}
        <section className="mb-12">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Where to look</h2>
          <div className="grid md:grid-cols-2 gap-4 text-sm">
            <Link href="/rar" className="block border border-gray-200 rounded-lg p-4 hover:border-gray-400 transition-colors">
              <div className="font-medium text-gray-900 mb-1">Galaxy data</div>
              <p className="text-gray-600">The radial acceleration relation and baryonic Tully&ndash;Fisher behaviour — the part that is empirically grounded.</p>
            </Link>
            <Link href="/simulate" className="block border border-gray-200 rounded-lg p-4 hover:border-gray-400 transition-colors">
              <div className="font-medium text-gray-900 mb-1">Simulations</div>
              <p className="text-gray-600">Rotation curves and the acceleration relation, computed from the law rather than illustrated.</p>
            </Link>
            <a
              href="https://github.com/carlzimmerman/zimmerman-formula/blob/main/STANDING.md"
              target="_blank"
              rel="noopener noreferrer"
              className="block border border-gray-200 rounded-lg p-4 hover:border-gray-400 transition-colors"
            >
              <div className="font-medium text-gray-900 mb-1">STANDING.md</div>
              <p className="text-gray-600">The single source of truth: earned, postulated, live, closed, retracted. Newer than this page if they disagree.</p>
            </a>
            <Link href="/ai-slop" className="block border border-amber-300 bg-amber-50/50 rounded-lg p-4 hover:border-amber-500 transition-colors">
              <div className="font-medium text-amber-900 mb-1">Retracted work</div>
              <p className="text-amber-900/80">The cube&times;sphere numerology, the &ldquo;19 derivations,&rdquo; the T³/Z₂ topology, and the visualisations built on them. Kept as a record.</p>
            </Link>
          </div>
        </section>

        {/* Footer */}
        <footer className="border-t border-gray-200 pt-8 text-sm text-gray-500">
          <p className="mb-2">
            Modified gravity anchored to the cosmological constant — a proposal about gravity and the dark sector.{' '}
            <span className="font-medium">Not a theory of everything.</span>
          </p>
          <p className="mb-2">
            Every load-bearing number on this site is backed by a runnable script in the{' '}
            <a
              href="https://github.com/carlzimmerman/zimmerman-formula"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              public repository
            </a>
            . Where a claim has been corrected, the correction and its direction are recorded rather
            than quietly dropped.
          </p>
          <p>Carl P. Zimmerman &middot; Standing revision 4, 30 July 2026</p>
        </footer>
      </div>
    </main>
  )
}
