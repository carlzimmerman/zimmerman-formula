'use client'

import { motion } from 'framer-motion'
import { useState } from 'react'
import { Citation, CITATIONS } from './Citation'

interface Evidence {
  year: number
  month?: string
  title: string
  source: string
  description: string
  relevance: string
  type: 'supports' | 'challenges_lcdm' | 'prediction' | 'foundational'
  sigma?: number
  link?: string
  doi?: string
  arxiv?: string
}

const EVIDENCE: Evidence[] = [
  // Foundational
  {
    year: 1983,
    title: 'MOND Proposed',
    source: 'Milgrom, M.',
    description: 'Modified Newtonian Dynamics proposed to explain flat rotation curves without dark matter.',
    relevance: 'Foundation for the acceleration scale a₀ ≈ 1.2 × 10⁻¹⁰ m/s²',
    type: 'foundational',
    doi: '10.1086/161130',
    link: 'https://ui.adsabs.harvard.edu/abs/1983ApJ...270..365M',
  },
  {
    year: 2016,
    title: 'SPARC Database Released',
    source: 'Lelli, McGaugh, Schombert',
    description: '175 galaxies with high-quality rotation curves, enabling the Radial Acceleration Relation discovery.',
    relevance: 'RAR shows zero intrinsic scatter — unexplained by ΛCDM, natural in Zimmerman framework',
    type: 'foundational',
    doi: '10.3847/0004-6256/152/6/157',
    arxiv: '1606.09251',
    link: 'http://astroweb.cwru.edu/SPARC/',
  },
  {
    year: 2016,
    month: 'September',
    title: 'RAR Discovered',
    source: 'McGaugh, Lelli, Schombert',
    description: '2,693 data points show g_obs correlates perfectly with g_bar across all galaxy types.',
    relevance: 'The RAR formula g_obs = g_bar/(1-e^(-√(g_bar/a₀))) has no free parameters',
    type: 'supports',
    doi: '10.1103/PhysRevLett.117.201101',
    arxiv: '1609.05917',
  },
  // Recent challenges to ΛCDM
  {
    year: 2022,
    month: 'July',
    title: 'JWST First Deep Field',
    source: 'NASA/ESA/CSA',
    description: 'JWST reveals unexpectedly massive, mature galaxies at z > 10.',
    relevance: 'Zimmerman predicts a₀ was 20× stronger at z=10, enabling faster structure formation',
    type: 'challenges_lcdm',
    sigma: 4,
    link: 'https://www.nasa.gov/image-feature/goddard/2022/nasa-s-webb-delivers-deepest-infrared-image-of-universe-yet',
  },
  {
    year: 2023,
    month: 'February',
    title: 'JWST "Impossible" Galaxies',
    source: 'Labbé et al.',
    description: 'Six massive galaxy candidates at z > 7 with stellar masses exceeding ΛCDM predictions.',
    relevance: 'Would require >100% star formation efficiency in ΛCDM; ~10% works with Zimmerman\'s evolving a₀',
    type: 'challenges_lcdm',
    sigma: 5,
    doi: '10.1038/s41586-023-05786-2',
    arxiv: '2207.12446',
  },
  {
    year: 2023,
    month: 'August',
    title: 'Wide Binary Anomaly',
    source: 'Chae, K.-H.',
    description: 'GAIA DR3 data shows wide binary stars deviate from Newton at separations > 2000 AU.',
    relevance: 'Deviation occurs exactly at the MOND/Zimmerman acceleration scale a₀',
    type: 'supports',
    sigma: 5,
    doi: '10.3847/1538-4357/ace101',
    arxiv: '2305.04613',
  },
  {
    year: 2021,
    month: 'September',
    title: 'El Gordo Timing Problem',
    source: 'Asencio, Banik, Kroupa',
    description: 'Massive cluster collision at z=0.87 has 6.16σ tension with ΛCDM timescales.',
    relevance: 'At z=0.87, Zimmerman predicts a₀ was 1.66× stronger, resolving the timing tension',
    type: 'challenges_lcdm',
    sigma: 6.16,
    doi: '10.1093/mnras/staa3441',
    arxiv: '2012.03950',
  },
  {
    year: 2024,
    month: 'April',
    title: 'DESI BAO Year 1',
    source: 'DESI Collaboration',
    description: 'Baryon acoustic oscillation data suggests dark energy may be evolving (w₀ = -0.55, wₐ = -1.3).',
    relevance: 'Evolving dark energy is consistent with Zimmerman\'s cosmological framework',
    type: 'challenges_lcdm',
    sigma: 2.5,
    arxiv: '2404.03002',
  },
  {
    year: 2023,
    month: 'April',
    title: 'CEERS High-z Spectroscopy',
    source: 'Finkelstein et al. (CEERS)',
    description: 'Confirmed spectroscopic redshifts for galaxies at z > 10 with unexpected properties.',
    relevance: 'Mass-to-light ratios consistent with Zimmerman\'s enhanced early dynamics',
    type: 'supports',
    doi: '10.3847/2041-8213/acade4',
    arxiv: '2211.05792',
  },
  {
    year: 2024,
    month: 'October',
    title: 'S8 Tension Persists',
    source: 'DES Y3 + KiDS-1000',
    description: 'Local structure growth measurements remain 2-3σ below CMB predictions.',
    relevance: 'Zimmerman\'s evolving a₀ naturally produces redshift-dependent structure growth',
    type: 'challenges_lcdm',
    sigma: 2.7,
    arxiv: '2305.17173',
  },
  {
    year: 2024,
    month: 'November',
    title: 'Gaia DR3 Wide Binaries Confirmed',
    source: 'Chae, K.-H.',
    description: 'Updated analysis with improved Gaia data confirms MOND signal in wide binaries at 6σ.',
    relevance: 'Strengthens evidence for breakdown of Newton at a₀ scale',
    type: 'supports',
    sigma: 6,
    arxiv: '2309.10404',
  },
  // Predictions
  {
    year: 2026,
    title: 'Zimmerman Prediction: BTFR Evolution',
    source: 'DOI: 10.5281/zenodo.19199167',
    description: 'Baryonic Tully-Fisher relation should show systematic offset at high redshift.',
    relevance: 'Δlog M = -0.47 dex at z=2 — testable with JWST/ELT spectroscopy',
    type: 'prediction',
    doi: '10.5281/zenodo.19199167',
  },
  {
    year: 2026,
    title: 'Zimmerman Prediction: RAR Evolution',
    source: 'DOI: 10.5281/zenodo.19199167',
    description: 'The RAR transition scale g† should evolve with E(z).',
    relevance: 'At z=2, transition occurs at 3× higher acceleration — falsifiable',
    type: 'prediction',
    doi: '10.5281/zenodo.19199167',
  },
]

const TYPE_COLORS = {
  supports: { bg: 'bg-green-900/30', border: 'border-green-500/50', text: 'text-green-400', label: 'Supports Zimmerman' },
  challenges_lcdm: { bg: 'bg-red-900/30', border: 'border-red-500/50', text: 'text-red-400', label: 'Challenges ΛCDM' },
  prediction: { bg: 'bg-purple-900/30', border: 'border-purple-500/50', text: 'text-purple-400', label: 'Zimmerman Prediction' },
  foundational: { bg: 'bg-blue-900/30', border: 'border-blue-500/50', text: 'text-blue-400', label: 'Foundational' },
}

export default function EvidenceTimeline() {
  const [filter, setFilter] = useState<string | null>(null)

  const filteredEvidence = filter
    ? EVIDENCE.filter(e => e.type === filter)
    : EVIDENCE

  return (
    <div className="w-full min-h-screen bg-gradient-to-b from-black via-gray-950 to-black p-4 md:p-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-4xl mx-auto"
      >
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-red-400 via-yellow-400 to-green-400 bg-clip-text text-transparent mb-4">
            Evidence Timeline
          </h1>
          <p className="text-xl text-gray-400">
            Observational support for the Zimmerman framework
          </p>
        </div>

        {/* Summary stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: 'Supporting', count: EVIDENCE.filter(e => e.type === 'supports').length, color: 'green' },
            { label: 'ΛCDM Tensions', count: EVIDENCE.filter(e => e.type === 'challenges_lcdm').length, color: 'red' },
            { label: 'Predictions', count: EVIDENCE.filter(e => e.type === 'prediction').length, color: 'purple' },
            { label: 'Total Items', count: EVIDENCE.length, color: 'cyan' },
          ].map(stat => (
            <div key={stat.label} className="p-4 bg-gray-900/50 rounded-xl text-center">
              <div className={`text-2xl font-bold text-${stat.color}-400`}>{stat.count}</div>
              <div className="text-xs text-gray-500">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-2 mb-8 justify-center">
          <button
            onClick={() => setFilter(null)}
            className={`px-4 py-2 rounded-lg text-sm transition-all ${
              filter === null ? 'bg-white text-black' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
          >
            All
          </button>
          {Object.entries(TYPE_COLORS).map(([type, colors]) => (
            <button
              key={type}
              onClick={() => setFilter(type)}
              className={`px-4 py-2 rounded-lg text-sm transition-all ${
                filter === type ? `${colors.bg} ${colors.text} ${colors.border} border` : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
              }`}
            >
              {colors.label}
            </button>
          ))}
        </div>

        {/* Timeline */}
        <div className="relative">
          {/* Vertical line */}
          <div className="absolute left-4 md:left-1/2 top-0 bottom-0 w-0.5 bg-gray-700 transform md:-translate-x-0.5" />

          {filteredEvidence.map((item, index) => {
            const colors = TYPE_COLORS[item.type]
            const isLeft = index % 2 === 0

            return (
              <motion.div
                key={`${item.year}-${item.title}`}
                initial={{ opacity: 0, x: isLeft ? -20 : 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className={`relative mb-8 ${isLeft ? 'md:pr-1/2' : 'md:pl-1/2 md:ml-auto'}`}
              >
                {/* Timeline dot */}
                <div className={`absolute left-4 md:left-1/2 w-4 h-4 rounded-full ${colors.bg} ${colors.border} border-2 transform -translate-x-1/2 z-10`} />

                {/* Content card */}
                <div className={`ml-12 md:ml-0 ${isLeft ? 'md:mr-8' : 'md:ml-8'}`}>
                  <div className={`p-5 rounded-xl ${colors.bg} ${colors.border} border`}>
                    {/* Header */}
                    <div className="flex items-start justify-between gap-4 mb-3">
                      <div>
                        <div className={`text-sm font-mono ${colors.text}`}>
                          {item.month ? `${item.month} ` : ''}{item.year}
                        </div>
                        <h3 className="text-lg font-bold text-white">{item.title}</h3>
                        <div className="text-xs text-gray-500">{item.source}</div>
                      </div>
                      {item.sigma && (
                        <div className={`px-2 py-1 rounded text-xs font-bold ${colors.bg} ${colors.text}`}>
                          {item.sigma}σ
                        </div>
                      )}
                    </div>

                    {/* Description */}
                    <p className="text-sm text-gray-300 mb-3">{item.description}</p>

                    {/* Relevance */}
                    <div className="p-3 bg-black/30 rounded-lg">
                      <div className="text-xs text-gray-500 mb-1">Zimmerman Relevance:</div>
                      <p className="text-sm text-cyan-300">{item.relevance}</p>
                    </div>

                    {/* Links */}
                    <div className="flex flex-wrap gap-2 mt-3">
                      {item.doi && (
                        <a
                          href={`https://doi.org/${item.doi}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-xs text-blue-400 hover:text-blue-300 px-2 py-1 bg-blue-900/20 rounded"
                        >
                          DOI
                        </a>
                      )}
                      {item.arxiv && (
                        <a
                          href={`https://arxiv.org/abs/${item.arxiv}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-xs text-green-400 hover:text-green-300 px-2 py-1 bg-green-900/20 rounded"
                        >
                          arXiv
                        </a>
                      )}
                      {item.link && !item.doi && (
                        <a
                          href={item.link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-xs text-purple-400 hover:text-purple-300"
                        >
                          View source →
                        </a>
                      )}
                    </div>
                  </div>
                </div>
              </motion.div>
            )
          })}
        </div>

        {/* Key tensions summary */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="mt-12 p-6 bg-gradient-to-r from-red-900/20 to-purple-900/20 rounded-2xl border border-red-500/30"
        >
          <h2 className="text-xl font-bold text-red-400 mb-4 text-center">ΛCDM Tension Summary</h2>
          <div className="grid md:grid-cols-3 gap-4">
            {[
              { name: 'Hubble Tension', sigma: '5σ', desc: 'H₀: 67.4 vs 73 km/s/Mpc' },
              { name: 'S8 Tension', sigma: '2.7σ', desc: 'Structure growth mismatch' },
              { name: 'El Gordo', sigma: '6.16σ', desc: 'Cluster formation timing' },
            ].map(t => (
              <div key={t.name} className="p-4 bg-black/30 rounded-xl text-center">
                <div className="text-2xl font-bold text-red-400">{t.sigma}</div>
                <div className="text-sm text-white font-medium">{t.name}</div>
                <div className="text-xs text-gray-500">{t.desc}</div>
              </div>
            ))}
          </div>
          <p className="text-center text-sm text-gray-400 mt-4">
            The Zimmerman framework addresses all three tensions with a single mechanism: evolving a₀
          </p>
        </motion.div>

        {/* Falsification criteria */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mt-8 p-6 bg-purple-900/20 rounded-2xl border border-purple-500/30"
        >
          <h2 className="text-xl font-bold text-purple-400 mb-4 text-center">Falsification Criteria</h2>
          <div className="space-y-3">
            {[
              'High-z BTFR shows NO offset from local relation',
              'High-z galaxies show SAME dynamics as local galaxies',
              'Wide binaries follow Newton at ALL separations',
              'RAR transition scale is CONSTANT with redshift',
            ].map((criterion, i) => (
              <div key={i} className="flex items-center gap-3 text-sm">
                <span className="text-red-400">✗</span>
                <span className="text-gray-300">If: {criterion}</span>
              </div>
            ))}
          </div>
          <p className="text-center text-xs text-gray-500 mt-4">
            Any of these observations would falsify the Zimmerman framework
          </p>
        </motion.div>

        {/* Key References */}
        <Citation
          citations={[
            CITATIONS.RAR,
            CITATIONS.WIDE_BINARIES,
            CITATIONS.EL_GORDO,
            CITATIONS.JWST_CEERS,
            CITATIONS.DESI_2024,
            CITATIONS.MILGROM_1983,
          ]}
        />

        {/* Back link */}
        <div className="mt-8 text-center">
          <a href="/" className="text-purple-400 hover:text-purple-300 transition-colors">
            ← Back to Home
          </a>
        </div>
      </motion.div>
    </div>
  )
}
