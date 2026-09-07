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
              <Link href="/field-theory" className="text-gray-900 font-medium hover:text-gray-600">Field theory</Link>
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
            <span>Standing revision 8 &mdash; 6 September 2026</span>
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
                was closed by lensing in August 2026 — with the Milgrom&ndash;Sanders (2008) kernel
                ν(y) = 1/(1 − e^(−√y)) as the operative interpolation. κ = ½ is{' '}
                <span className="font-medium">fitted, not derived</span>: measured 0.551 ± 0.043 (distance-free)
                and 0.465 ± 0.076 (Tully&ndash;Fisher) &mdash; and, as of 6 September 2026,{' '}
                <span className="font-medium">proven underivable by the programme&rsquo;s own covariant action</span>: the MOND
                primitive enters the field equations only through its derivative and the cosmological background only
                through Λ + (2 − K_B) J(0)/2, a normalisation zero mode (
                <a href="https://doi.org/10.5281/zenodo.22559892" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">DOI 10.5281/zenodo.22559892</a>
                ). The one coefficient-free alternative, the horizon form a₀ = c²/(2π L_dS) with κ = 0.461, is 8.5% away and
                exactly degenerate with the H₀ tension: κ = ½ on Planck&rsquo;s H₀ and κ = 0.461 on SH0ES&rsquo;s predict the
                same a₀ to 0.2%. Because a₀ tracks the dark-energy density it{' '}
                <span className="font-medium">cannot track the expansion rate</span>: a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE(0))
                exactly, which is flat if Λ is constant, 13% lower by z = 2 on DESI&rsquo;s w₀wₐ fit, and within ±20% of
                today&rsquo;s value out to z = 3 for any dark energy the data allow &mdash; against ×3 for a₀ ∝ H(z) and
                ×1.8 for ΛCDM&rsquo;s emergent scale. That is the one statement here that ΛCDM does not make.
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
                  <td className="py-3 px-4 text-gray-700">The coefficient κ cannot be derived by the candidate action (6 September 2026)</td>
                  <td className="py-3 px-4 text-gray-900">
                    Zero-mode theorem; the Λ-free repair has the wrong sign and is 220× too small; a global constraint misses by
                    10⁵; a four-form promotion of a₀ fixes the sign and makes a₀ ∝ √(Gρ_Λ) structural but leaves κ as the
                    free coupling ratio Z/β² = 8; the horizon coefficient 0.461 vs ½ is locked to H₀. Published &mdash;{' '}
                    <a href="https://doi.org/10.5281/zenodo.22559892" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">DOI 10.5281/zenodo.22559892</a>
                  </td>
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-3 px-4 text-gray-700">The condensate polytrope (September 2026)</td>
                  <td className="py-3 px-4 text-gray-900">
                    The dust of the Aether&ndash;Scalar&ndash;Tensor completion is a γ = 2 polytrope whose sound speed in a
                    well is the well depth, c_s² = |Ψ| c²; the static Helmholtz equation is its hydrostatics.
                    Algebra published &mdash;{' '}
                    <a href="https://doi.org/10.5281/zenodo.22242701" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">DOI 10.5281/zenodo.22242701</a>
                    {' '}(the cluster cosmology built on it is withdrawn, see below)
                  </td>
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-3 px-4 text-gray-700">Nonlocal MOND kernels (Deffayet&ndash;Woodard class) are unstable</td>
                  <td className="py-3 px-4 text-gray-900">
                    In-in linear analysis: longitudinal gradient instability and a deep-MOND ghost; an independent tensor-speed kill.
                    Published &mdash;{' '}
                    <a href="https://doi.org/10.5281/zenodo.22253953" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">DOI 10.5281/zenodo.22253953</a>
                  </td>
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-3 px-4 text-gray-700">Modified-inertia action (v1–v11); disformal lensing construction</td>
                  <td className="py-3 px-4 text-gray-900">Published; the arm is closed as physics (lensing, 21σ); kept as mathematics</td>
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
              derived, and since 6 September 2026 it is proven underivable by the candidate action itself: the
              additive zero of the MOND primitive is a zero mode of the field equations, the two repairs that could fix it
              fail on sign and by five orders of magnitude, and the four-form extension that fixes the sign turns the
              question into a free coupling ratio. It is an <span className="font-medium">empirical boundary condition</span>
              that only a stellar mass-to-light zero point, an absolute gas scale and a settled H₀ can pin. This is a{' '}
              <span className="font-medium">one-parameter effective theory, not a zero-parameter derivation</span>. Z has the same status.
            </li>
            <li className="border-l-2 border-gray-300 pl-4">
              <span className="font-medium text-gray-900">Dark matter exists, at full Ω_dm, and it is cold.</span>{' '}
              The CMB needs a pressureless component and the relativistic completion (v9, on Skordis &amp;
              Złośnik&rsquo;s Aether&ndash;Scalar&ndash;Tensor chassis) supplied it with a condensate. On 2 September 2026
              that condensate&rsquo;s own equation of state closed the door: read on the cosmic background it fixes
              c_s²(z) = 4πG ρ_dm(z)/μ², which pins the theory&rsquo;s free amplitude 18&ndash;300× above its own
              power-spectrum ceiling, and for <em>any</em> such field a galaxy well today is the background at
              z ≲ 16 with the same sound speed &mdash; so a field cold enough for the Lyman-α forest falls into
              galaxies. The slogan &ldquo;no dark matter in galaxies&rdquo; has no kinetic mechanism left.
            </li>
            <li className="border-l-2 border-gray-300 pl-4">
              <span className="font-medium text-gray-900">A two-field metric MOND that light and matter both
              see is forced to carry a third field.</span> At quadratic order around de Sitter, any elliptic
              auxiliary that enters the lapse equation frees one dust-like scalar; couplings to the spatial
              curvature free none but split lensing from dynamics. That is why TeVeS, AeST and the superfluid
              all carry a genuine extra field, and it is why the hoped-for constraint-only theory does not exist.
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
                Dark matter falls into galaxies, and MOND is still there
              </div>
              <p className="text-gray-700">
                The completion needs an Ω_dm-worth of cold energy for the acoustic peaks and the 100-Mpc
                clustering. Cold means it clusters into galaxies, where the MOND boost is also acting: by the
                repository&rsquo;s own numbers that double count overshoots rotation curves by{' '}
                <span className="font-medium">2.7&ndash;4.4×</span>. Every kinetic escape has now been run and
                closed &mdash; pressure support, a superfluid phase, a rising a₀, a Hubble-scaled filter &mdash;
                each one a committed script with checks that can fail. On 6 September 2026 the last particle candidate, a
                thermal relic at the mass the N_eff bound allows (about 28 eV), closed as a pincer with no interior: N_eff needs
                at least 27.6 eV, the radial acceleration relation needs at most 11 eV, and the cluster profile worked only at
                11.4 eV. Four condensate constructions are closed on the action&rsquo;s own terms. The dark-sector hunt is frozen
                behind the coefficient question. This is the programme&rsquo;s blocking problem, and it is the same one
                MOND-plus-halos always had.
              </p>
            </div>
            <div className="border-l-4 border-orange-400 pl-4 py-2 bg-orange-50/50">
              <div className="font-medium text-gray-900 mb-1">Galaxy clusters</div>
              <p className="text-gray-700">
                The framework&rsquo;s own kernel leaves clusters short by η(R₅₀₀) ≈ 1.9&ndash;2.1. The condensate
                polytrope pins a core worth 23&ndash;33% of the missing mass (published, DOI 10.5281/zenodo.22242701, v2
                22254075), but the cosmology behind that mechanism is the one excluded on 2 September 2026: the
                static algebra stands, the yield is <span className="font-medium">withdrawn as a live number</span>.
                Recorded in RETRACTIONS.md.
              </p>
            </div>
            <div className="border-l-4 border-gray-400 pl-4 py-2 bg-gray-50">
              <div className="font-medium text-gray-900 mb-1">The inner-planet ephemerides &mdash; discharged</div>
              <p className="text-gray-700">
                The earlier &ldquo;exact&rdquo; α = 1 law implied a constant sunward anomaly 1278× over the Earth
                bound. The exponential kernel now in force (Route A, 2 August 2026) makes the departure from Newton
                exponentially small in the Solar System, 2.7 × 10⁻²² at the Sun. The word &ldquo;exact&rdquo; stays withdrawn.
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
                    Two mutually exclusive arms, both registered before the data (Amendment 11, 6 Sep 2026, append-only and
                    hash-stamped). Arm A, the frozen kernel as modified gravity: γ_v = 1.1614&ndash;1.1814 canonical /
                    1.1917&ndash;1.2267 alt, no-verdict edge 1.23. Arm B, the covariant candidate at its Cassini-minimal coherence
                    length: γ_v ≤ 1.0450 / ≤ 1.0300, falling toward 1.000 as the length grows. Decision rule fixed in advance:
                    A falsified below 1.056, B falsified at or above 1.129. Stated against interest: DR4 separates the arms at
                    4.2σ but cannot confirm Arm B over Newton beyond 1.6σ &mdash; a Newtonian result kills A and leaves B alive but
                    unconfirmed, never a success. Newton = 1.000.
                  </td>
                  <td className="py-3 px-4 text-gray-500">Gaia DR4, Dec 2026</td>
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-3 px-4 text-gray-700">Deep-MOND Tully&ndash;Fisher zero-point at z ≈ 2.5</td>
                  <td className="py-3 px-4 text-gray-700">
                    Framework: <span className="font-medium">0.00 dex</span> (−0.09 with DESI dark energy).
                    ΛCDM&rsquo;s emergent halo scale: <span className="font-medium">+0.33 dex</span>. One clean
                    low-acceleration rotator measured to ±0.13 dex decides at 20:1. On present data the two are
                    undecided and prior-dominated; the apparent rise seen by MUSE and JWST is also what ΛCDM&rsquo;s halo
                    structure produces. A robust measured rise kills the framework&rsquo;s law either way.
                  </td>
                  <td className="py-3 px-4 text-gray-500">JWST / ALMA, a handful of objects</td>
                </tr>
                <tr>
                  <td className="py-3 px-4 text-gray-700">a₀(z) evolution</td>
                  <td className="py-3 px-4 text-gray-700">
                    a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE(0)), footing-independent: constant to &lt;1% for z ≤ 5 if Λ is constant
                    (the v9 completion switches it off only above z ≈ 20), a ~13% decline by z = 2 on DESI&rsquo;s w₀wₐ fit,
                    and never more than ±20% out to z = 3 for any allowed w. ΛCDM&rsquo;s emergent scale rises ×1.8 by z = 2;
                    to mimic a flat a₀ its haloes would have to be diluted to 0.61 (z = 2) and 0.40 (z = 3) of their N-body
                    concentrations.
                  </td>
                  <td className="py-3 px-4 text-gray-500">DESI, ongoing</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        {/* Papers */}
        <section className="mb-12">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Papers, September 2026 (Zenodo; AI-assisted drafts, not peer reviewed)</h2>
          <ul className="space-y-2 text-sm text-gray-700">
            {[
              ['10.5281/zenodo.22559892', 'The Coefficient of the a₀–Λ Relation: a Zero-Mode Theorem for Local MOND Actions, Two Failed Repairs, a Four-Form Reframing, and an H₀ Degeneracy (6 Sep)'],
              ['10.5281/zenodo.22548669', 'A Ceiling Dark Matter Cannot Impose: the Bounded-Boost Theorem for MOND-Class Kernels, and What It Says About Galaxies and Clusters (v4, 6 Sep)'],
              ['10.5281/zenodo.22347632', 'The Filtered MOND Action: a Central Tidal Identity, Comparable-Mass Forces, a First Covariant Clock Action, and the Operator That Screens the Solar System (5 Sep)'],
              ['10.5281/zenodo.22261001', 'Crispy Fried Chicken Matching Theorem (2 Sep)'],
              ['10.5281/zenodo.22255522', 'The Retarded Nonlocal MOND Kernel Is Unstable on MOND Backgrounds: a Longitudinal Gradient Instability and a Deep-MOND Ghost Close the Nonlocal Door (v2, 2 Sep)'],
              ['10.5281/zenodo.22254075', 'The Aether-Scalar-Tensor Dark Sector Is a γ = 2 Polytrope: the Cluster Helmholtz Phase Is Its Mass, It Pins Dynamically, and It Fills About a Quarter of the Cluster Gap (v2, 2 Sep; cosmology withdrawn)'],
              ['10.5281/zenodo.22135510', 'An Obstruction Map for Relativistic MOND: the Conformal Lensing Barrier and the Cost of Its Repair (28 Aug)'],
              ['10.5281/zenodo.22133406', 'A Conditionally Closed Constraint-Defined MOND Theory with Two Tensor Degrees of Freedom: Hamiltonian Certification, Kernel-Agnostic Chassis, and Solar-System Gates (v2, 27 Aug)'],
              ['10.5281/zenodo.22132648', 'Carrier No-Go Theorems for Two-Degree-of-Freedom MOND: the F(A²) Class, the Auxiliary-Legendre Escape, and a Hamiltonian Audit of Causal Nonlocal MOND (27 Aug)'],
            ].map(([doi, title]) => (
              <li key={doi} className="border-l-2 border-gray-300 pl-4">
                <span className="text-gray-900">{title}</span>{' '}&mdash;{' '}
                <a href={`https://doi.org/${doi}`} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">DOI {doi}</a>
              </li>
            ))}
          </ul>
          <p className="text-sm text-gray-600 mt-3">
            The full record, every deposit since June 2026 with its title and concept DOI, is the{' '}
            <a href="https://github.com/carlzimmerman/zimmerman-formula#doi-index--every-deposit-with-its-title-newest-first-version-doi-concept-doi-in-brackets" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">DOI index in the repository README</a>.
          </p>
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
          <p>Carl P. Zimmerman &middot; Standing revision 8, 6 September 2026</p>
        </footer>
      </div>
    </main>
  )
}
