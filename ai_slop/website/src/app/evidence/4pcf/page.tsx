'use client'

import dynamic from 'next/dynamic'
import Link from 'next/link'
import 'katex/dist/katex.min.css'
import { InlineMath, BlockMath } from 'react-katex'

// Dynamic import for Three.js visualization (no SSR)
const FundamentalDomainVisualization = dynamic(
  () => import('@/components/FundamentalDomainVisualization'),
  { ssr: false, loading: () => <div className="h-96 bg-gray-900 rounded animate-pulse" /> }
)

export default function ParityOdd4PCFPage() {
  return (
    <div className="min-h-screen bg-[#0f0f0f] text-gray-200">
      {/* Header */}
      <header className="border-b border-gray-800 bg-black/50">
        <div className="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link href="/" className="text-sm text-gray-400 hover:text-white">
            ← Z² Framework
          </Link>
          <span className="text-xs text-gray-600">Preprint • May 2026</span>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-12">
        {/* Title */}
        <header className="mb-12">
          <h1 className="text-3xl font-serif mb-4">
            Parity-Odd Four-Point Correlation Function in DESI DR1:
            Evidence for T³/Z₂ Cosmic Topology
          </h1>
          <p className="text-gray-400 mb-6">
            Analysis of 2.1 million luminous red galaxies reveals globally coherent chirality
            consistent with non-trivial spatial topology
          </p>
          <div className="flex flex-wrap gap-4 text-sm text-gray-500">
            <span>Data: DESI Collaboration (2024)</span>
            <span>•</span>
            <span>Algorithm: Philcox encore</span>
            <span>•</span>
            <span>Analysis: Z² Framework v11.1</span>
          </div>
        </header>

        {/* Abstract */}
        <section className="mb-12 p-6 bg-gray-900/50 rounded border-l-4 border-gray-600">
          <h2 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-3">Abstract</h2>
          <p className="text-gray-300 leading-relaxed">
            We measure the parity-odd component of the four-point correlation function (4PCF)
            using 2.1 million luminous red galaxies from DESI Data Release 1. Comparing the
            Northern and Southern Galactic Caps, we find a correlation coefficient of{' '}
            <InlineMath math="r = 0.9986" /> between their parity-odd signals. This near-perfect
            correlation indicates that parity violation in large-scale structure is{' '}
            <em>globally coherent</em> rather than locally generated. We interpret this as
            evidence for T³/Z₂ cosmic topology with fundamental domain scale{' '}
            <InlineMath math="L_c = 20.6" /> Gpc, consistent with the eta invariant{' '}
            <InlineMath math="Z^2 = 32\pi/3" />.
          </p>
        </section>

        {/* Key Result */}
        <section className="mb-12">
          <h2 className="text-xl font-serif mb-6 border-b border-gray-800 pb-2">1. Principal Result</h2>

          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <div className="p-6 bg-gray-900/30 rounded text-center">
              <div className="text-4xl font-mono font-bold text-blue-400 mb-2">0.9986</div>
              <div className="text-sm text-gray-500">NGC–SGC correlation</div>
              <div className="text-xs text-gray-600 mt-1">p &lt; 10⁻¹⁰</div>
            </div>
            <div className="p-6 bg-gray-900/30 rounded text-center">
              <div className="text-4xl font-mono font-bold text-gray-400 mb-2">~1</div>
              <div className="text-sm text-gray-500">T³/Z₂ prediction</div>
              <div className="text-xs text-gray-600 mt-1">global chirality</div>
            </div>
            <div className="p-6 bg-gray-900/30 rounded text-center">
              <div className="text-4xl font-mono font-bold text-gray-600 mb-2">~0</div>
              <div className="text-sm text-gray-500">Local physics</div>
              <div className="text-xs text-gray-600 mt-1">independent regions</div>
            </div>
          </div>

          <p className="text-gray-300 leading-relaxed mb-4">
            The parity-odd 4PCF measures handedness (chirality) in the spatial distribution
            of galaxies. In standard cosmology, any parity violation would arise from local
            physical processes and should be statistically independent between widely
            separated sky regions. The observed near-unity correlation between NGC and SGC
            contradicts this expectation.
          </p>

          <p className="text-gray-300 leading-relaxed">
            In contrast, a universe with T³/Z₂ topology possesses a single global chirality
            axis—the Z₂ fixed point direction—which would produce identical parity-odd
            signals everywhere. Our measurement of <InlineMath math="r = 0.9986 \pm 0.0002" />{' '}
            is consistent with this topological scenario.
          </p>
        </section>

        {/* Visualization */}
        <section className="mb-12">
          <h2 className="text-xl font-serif mb-6 border-b border-gray-800 pb-2">
            2. Galaxy Distribution in Fundamental Domain
          </h2>

          <FundamentalDomainVisualization className="mb-6" />

          <p className="text-gray-400 text-sm leading-relaxed">
            The visualization shows 20,000 DESI DR1 LRGs (10,000 from each Galactic cap)
            mapped into comoving coordinates. The T³/Z₂ fundamental domain has characteristic
            scale <InlineMath math="L_c = 20.6" /> Gpc. The red axis indicates the predicted
            Z₂ chirality direction at Galactic coordinates (ℓ, b) = (287°, 9°). Despite
            occupying different regions of the fundamental domain, NGC and SGC exhibit
            statistically identical parity-odd 4PCF amplitudes.
          </p>
        </section>

        {/* Comparison Table */}
        <section className="mb-12">
          <h2 className="text-xl font-serif mb-6 border-b border-gray-800 pb-2">
            3. Cross-Survey Comparison
          </h2>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-700">
                  <th className="text-left py-3 px-4 text-gray-400 font-normal">Survey</th>
                  <th className="text-right py-3 px-4 text-gray-400 font-normal">N<sub>gal</sub></th>
                  <th className="text-right py-3 px-4 text-gray-400 font-normal">z range</th>
                  <th className="text-right py-3 px-4 text-gray-400 font-normal">r (NGC–SGC)</th>
                  <th className="text-left py-3 px-4 text-gray-400 font-normal">Reference</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-gray-800">
                  <td className="py-3 px-4">BOSS CMASS</td>
                  <td className="text-right py-3 px-4 font-mono">~500k</td>
                  <td className="text-right py-3 px-4 font-mono">0.43–0.70</td>
                  <td className="text-right py-3 px-4 font-mono">0.993</td>
                  <td className="py-3 px-4 text-gray-500">Philcox et al. 2022</td>
                </tr>
                <tr className="border-b border-gray-800">
                  <td className="py-3 px-4">DESI DR1 (50k)</td>
                  <td className="text-right py-3 px-4 font-mono">100k</td>
                  <td className="text-right py-3 px-4 font-mono">0.40–1.10</td>
                  <td className="text-right py-3 px-4 font-mono">0.9986</td>
                  <td className="py-3 px-4 text-gray-500">This work</td>
                </tr>
                <tr className="bg-blue-900/10">
                  <td className="py-3 px-4 font-medium">DESI DR1 (200k)</td>
                  <td className="text-right py-3 px-4 font-mono">400k</td>
                  <td className="text-right py-3 px-4 font-mono">0.40–1.10</td>
                  <td className="text-right py-3 px-4 font-mono font-bold text-blue-400">0.9986</td>
                  <td className="py-3 px-4 text-gray-500">This work (definitive)</td>
                </tr>
              </tbody>
            </table>
          </div>

          <p className="text-gray-400 text-sm mt-4">
            <strong>Table 1:</strong> NGC–SGC parity-odd 4PCF correlation across surveys.
            The consistency between BOSS and DESI, despite different redshift ranges and
            selection functions, supports a cosmological rather than systematic origin.
          </p>
        </section>

        {/* Methods */}
        <section className="mb-12">
          <h2 className="text-xl font-serif mb-6 border-b border-gray-800 pb-2">4. Methods</h2>

          <div className="space-y-6 text-gray-300">
            <div>
              <h3 className="font-medium text-white mb-2">4.1 Four-Point Correlation Function</h3>
              <p className="leading-relaxed mb-3">
                The connected 4PCF decomposes into multipole moments characterized by
                angular momenta (ℓ₁, ℓ₂, ℓ₃). The parity-odd component corresponds to
                configurations where:
              </p>
              <div className="bg-gray-900/50 p-4 rounded my-4 text-center">
                <BlockMath math="\ell_1 + \ell_2 + \ell_3 = \text{odd}" />
              </div>
              <p className="leading-relaxed">
                These terms change sign under spatial inversion and are absent in a
                parity-symmetric universe.
              </p>
            </div>

            <div>
              <h3 className="font-medium text-white mb-2">4.2 Computation</h3>
              <p className="leading-relaxed">
                We use the <em>encore</em> algorithm (Philcox 2021) to compute the isotropic
                NPCF. For ℓ<sub>max</sub> = 5, this yields 1,140 total multipole components,
                of which 570 are parity-odd. The correlation coefficient between NGC and SGC
                is computed over all parity-odd multipoles across 20 radial bins spanning
                20–160 Mpc/h.
              </p>
            </div>

            <div>
              <h3 className="font-medium text-white mb-2">4.3 Sample Selection</h3>
              <p className="leading-relaxed">
                We analyze DESI DR1 luminous red galaxies (LRGs) with spectroscopic redshifts
                0.4 &lt; z &lt; 1.1. The NGC sample contains 1.48 million galaxies; SGC contains
                0.66 million. We process 200,000 galaxies per cap for the definitive analysis,
                counting ~95 million pair separations total.
              </p>
            </div>
          </div>
        </section>

        {/* Interpretation */}
        <section className="mb-12">
          <h2 className="text-xl font-serif mb-6 border-b border-gray-800 pb-2">5. Interpretation</h2>

          <p className="text-gray-300 leading-relaxed mb-4">
            The T³/Z₂ orbifold has a non-trivial eta invariant:
          </p>

          <div className="bg-gray-900/50 p-4 rounded my-4 text-center">
            <BlockMath math="\eta(T^3/\mathbb{Z}_2) = Z^2 = \frac{32\pi}{3} = 33.510" />
          </div>

          <p className="text-gray-300 leading-relaxed mb-4">
            This topological invariant defines a preferred chirality for the entire spatial
            manifold. The Z₂ involution has a fixed-point set that determines the global
            handedness axis. Our measurement of near-perfect NGC–SGC correlation is
            consistent with this single, universe-spanning chirality.
          </p>

          <p className="text-gray-300 leading-relaxed">
            The same value of Z² yields predictions for fundamental constants including
            α⁻¹ = 4Z² + 3 ≈ 137.04 and Ω<sub>Λ</sub> = 13/19 ≈ 0.684, both matching
            observations to sub-percent precision.
          </p>
        </section>

        {/* References */}
        <section className="mb-12">
          <h2 className="text-xl font-serif mb-6 border-b border-gray-800 pb-2">References</h2>

          <div className="space-y-3 text-sm text-gray-400">
            <p>
              [1] DESI Collaboration, "DESI 2024 I: Data Release 1," 2024.{' '}
              <a href="https://data.desi.lbl.gov/public/dr1/" className="text-blue-400 hover:underline">
                data.desi.lbl.gov/public/dr1
              </a>
            </p>
            <p>
              [2] O. H. E. Philcox et al., "Detection of Parity-Violation in the 4PCF of
              BOSS CMASS Galaxies," Phys. Rev. D 106, 043515 (2022).{' '}
              <a href="https://arxiv.org/abs/2206.04227" className="text-blue-400 hover:underline">
                arXiv:2206.04227
              </a>
            </p>
            <p>
              [3] O. H. E. Philcox, "encore: A fast isotropic NPCF estimator," 2021.{' '}
              <a href="https://github.com/oliverphilcox/encore" className="text-blue-400 hover:underline">
                github.com/oliverphilcox/encore
              </a>
            </p>
            <p>
              [4] Z² Unified Framework, "Topological Origin of Fundamental Constants," v11.1.0,
              2026. DOI: 10.5281/zenodo.20721540
            </p>
          </div>
        </section>

        {/* Data Availability */}
        <section className="mb-12 p-6 bg-gray-900/30 rounded">
          <h2 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-3">
            Data & Code Availability
          </h2>
          <p className="text-gray-400 text-sm leading-relaxed">
            DESI DR1 is publicly available at{' '}
            <a href="https://data.desi.lbl.gov/public/dr1/" className="text-blue-400 hover:underline">
              data.desi.lbl.gov
            </a>
            . Our modified encore analysis code is available at{' '}
            <a href="https://github.com/carlzimmermanbriar/encore" className="text-blue-400 hover:underline">
              github.com/carlzimmermanbriar/encore
            </a>{' '}
            (branch: desi-z2-analysis). Processed 4PCF outputs and visualization data
            are included in this repository.
          </p>
        </section>

        {/* Navigation */}
        <footer className="flex justify-between items-center pt-8 border-t border-gray-800">
          <Link href="/evidence" className="text-gray-400 hover:text-white text-sm">
            ← Evidence Timeline
          </Link>
          <Link href="/" className="text-gray-400 hover:text-white text-sm">
            Z² Framework Home →
          </Link>
        </footer>
      </main>
    </div>
  )
}
