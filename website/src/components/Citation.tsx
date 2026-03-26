'use client'

/**
 * Academic Citation Component
 *
 * Displays proper academic citations for data sources used in visualizations.
 * Following APA/astronomy journal style.
 */

interface CitationProps {
  citations: Array<{
    authors: string
    year: number | string
    title?: string
    journal: string
    volume?: string
    pages?: string
    doi?: string
    arxiv?: string
    ads?: string
    description?: string
  }>
  compact?: boolean
}

export function Citation({ citations, compact = false }: CitationProps) {
  if (compact) {
    return (
      <div className="mt-4 p-3 bg-gray-900/80 rounded-lg border border-gray-700">
        <div className="text-xs text-gray-400 mb-1 font-semibold">Data Sources:</div>
        <div className="space-y-1">
          {citations.map((cite, i) => (
            <div key={i} className="text-xs text-gray-500">
              {cite.authors} ({cite.year}), {cite.journal}
              {cite.volume && ` ${cite.volume}`}
              {cite.pages && `, ${cite.pages}`}
              {cite.doi && (
                <a
                  href={`https://doi.org/${cite.doi}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-400 hover:text-blue-300 ml-1"
                >
                  [DOI]
                </a>
              )}
              {cite.arxiv && (
                <a
                  href={`https://arxiv.org/abs/${cite.arxiv}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-green-400 hover:text-green-300 ml-1"
                >
                  [arXiv]
                </a>
              )}
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="mt-6 p-4 bg-gray-900/80 rounded-xl border border-gray-700">
      <h4 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
        <span className="text-lg">📚</span> Data Sources & References
      </h4>
      <div className="space-y-3">
        {citations.map((cite, i) => (
          <div key={i} className="text-sm">
            <div className="text-gray-300">
              <span className="font-medium">{cite.authors}</span>
              <span className="text-gray-500"> ({cite.year})</span>
              {cite.title && <span className="italic text-gray-400">. {cite.title}</span>}
            </div>
            <div className="text-xs text-gray-500 mt-0.5">
              {cite.journal}
              {cite.volume && <span className="font-medium"> {cite.volume}</span>}
              {cite.pages && <span>, {cite.pages}</span>}
              {cite.description && <span className="text-gray-600 ml-2">— {cite.description}</span>}
            </div>
            <div className="flex gap-2 mt-1">
              {cite.doi && (
                <a
                  href={`https://doi.org/${cite.doi}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-blue-400 hover:text-blue-300 hover:underline"
                >
                  DOI: {cite.doi}
                </a>
              )}
              {cite.arxiv && (
                <a
                  href={`https://arxiv.org/abs/${cite.arxiv}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-green-400 hover:text-green-300 hover:underline"
                >
                  arXiv:{cite.arxiv}
                </a>
              )}
              {cite.ads && (
                <a
                  href={`https://ui.adsabs.harvard.edu/abs/${cite.ads}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-orange-400 hover:text-orange-300 hover:underline"
                >
                  ADS
                </a>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// Pre-defined citation sets for common data sources
export const CITATIONS = {
  SPARC: {
    authors: 'Lelli, F., McGaugh, S.S., Schombert, J.M.',
    year: 2016,
    title: 'SPARC: Mass Models for 175 Disk Galaxies with Spitzer Photometry and Accurate Rotation Curves',
    journal: 'The Astronomical Journal',
    volume: '152',
    pages: '157',
    doi: '10.3847/0004-6256/152/6/157',
    arxiv: '1606.09251',
    description: '175 galaxies with rotation curves'
  },

  RAR: {
    authors: 'McGaugh, S.S., Lelli, F., Schombert, J.M.',
    year: 2016,
    title: 'Radial Acceleration Relation in Rotationally Supported Galaxies',
    journal: 'Physical Review Letters',
    volume: '117',
    pages: '201101',
    doi: '10.1103/PhysRevLett.117.201101',
    arxiv: '1609.05917',
    description: 'RAR with 2,693 data points'
  },

  PLANCK_2018: {
    authors: 'Planck Collaboration',
    year: 2020,
    title: 'Planck 2018 results. VI. Cosmological parameters',
    journal: 'Astronomy & Astrophysics',
    volume: '641',
    pages: 'A6',
    doi: '10.1051/0004-6361/201833910',
    arxiv: '1807.06209',
    description: 'H₀ = 67.4 ± 0.5 km/s/Mpc'
  },

  SHOES_2022: {
    authors: 'Riess, A.G. et al. (SH0ES)',
    year: 2022,
    title: 'A Comprehensive Measurement of the Local Value of the Hubble Constant',
    journal: 'The Astrophysical Journal Letters',
    volume: '934',
    pages: 'L7',
    doi: '10.3847/2041-8213/ac5c5b',
    arxiv: '2112.04510',
    description: 'H₀ = 73.04 ± 1.04 km/s/Mpc'
  },

  CODATA_2018: {
    authors: 'CODATA',
    year: 2018,
    title: 'CODATA Recommended Values of the Fundamental Physical Constants',
    journal: 'Reviews of Modern Physics',
    volume: '93',
    pages: '025010',
    doi: '10.1103/RevModPhys.93.025010',
    description: 'Fundamental constants'
  },

  EL_GORDO: {
    authors: 'Asencio, E., Banik, I., Kroupa, P.',
    year: 2021,
    title: 'A massive blow for ΛCDM – the high redshift, mass, and collision velocity of the interacting galaxy cluster El Gordo',
    journal: 'Monthly Notices of the Royal Astronomical Society',
    volume: '500',
    pages: '5249-5267',
    doi: '10.1093/mnras/staa3441',
    arxiv: '2012.03950',
    description: '6.16σ tension with ΛCDM'
  },

  WIDE_BINARIES: {
    authors: 'Chae, K.-H.',
    year: 2023,
    title: 'Breakdown of Standard Gravity at Low Acceleration in Binary Stars',
    journal: 'The Astrophysical Journal',
    volume: '952',
    pages: '128',
    doi: '10.3847/1538-4357/ace101',
    arxiv: '2305.04613',
    description: '16,000+ Gaia DR3 wide binaries'
  },

  JWST_CEERS: {
    authors: 'Finkelstein, S.L. et al. (CEERS)',
    year: 2023,
    title: 'CEERS Key Paper. I. An Early Look into the First 500 Myr of Galaxy Formation with JWST',
    journal: 'The Astrophysical Journal Letters',
    volume: '946',
    pages: 'L13',
    doi: '10.3847/2041-8213/acade4',
    arxiv: '2211.05792',
    description: 'High-z galaxies z > 10'
  },

  JWST_JADES: {
    authors: 'D\'Eugenio, F. et al. (JADES)',
    year: 2024,
    title: 'JADES: Resolving the Stellar Component and Filamentary Overdense Environment of HST-Dark Submillimeter Galaxies',
    journal: 'Astronomy & Astrophysics',
    volume: '681',
    pages: 'A78',
    doi: '10.1051/0004-6361/202347755',
    arxiv: '2308.06317',
    description: 'High-z kinematics'
  },

  DESI_2024: {
    authors: 'DESI Collaboration',
    year: 2024,
    title: 'DESI 2024 VI: Cosmological Constraints from the Measurements of Baryon Acoustic Oscillations',
    journal: 'arXiv preprint',
    arxiv: '2404.03002',
    description: 'BAO measurements suggesting evolving dark energy'
  },

  KMOS3D: {
    authors: 'Übler, H. et al.',
    year: 2017,
    title: 'The Evolution of the Tully-Fisher Relation between z ~ 2.3 and z ~ 0.9 with KMOS3D',
    journal: 'The Astrophysical Journal',
    volume: '842',
    pages: '121',
    doi: '10.3847/1538-4357/aa7558',
    arxiv: '1703.04321',
    description: 'z ~ 0.9-2.3 kinematics'
  },

  MILGROM_1983: {
    authors: 'Milgrom, M.',
    year: 1983,
    title: 'A modification of the Newtonian dynamics as a possible alternative to the hidden mass hypothesis',
    journal: 'The Astrophysical Journal',
    volume: '270',
    pages: '365-370',
    doi: '10.1086/161130',
    description: 'Original MOND formulation'
  }
}

export default Citation
