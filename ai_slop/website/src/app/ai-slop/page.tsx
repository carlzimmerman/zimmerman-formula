'use client'

import Link from 'next/link'

type Item = {
  href: string
  title: string
  what: string
  why: string
}

// The retracted material, grouped by what kind of claim it was. Every entry here is kept as a
// record, not as a claim. The reasons are the same ones RouteNotice.tsx attaches to each page.
const NUMEROLOGY: Item[] = [
  {
    href: '/all-derivations',
    title: 'The "19 first-principles derivations"',
    what: 'Claimed derivations of the fine-structure constant, the proton-to-electron mass ratio, the Weinberg angle, CKM elements and cosmological density parameters, all from Z² = 32π/3.',
    why: 'Numerology. It failed a look-elsewhere / false-discovery test: a randomly chosen constant of similar size reproduces the same retrodictions equally well. Chance alone hits roughly ten of nineteen targets.',
  },
  {
    href: '/derivation',
    title: 'The derivation chain',
    what: 'The cube×sphere construction: Z² = 8 × (4π/3), presented as the origin of all coupling constants and mass hierarchies.',
    why: 'The "8" (fixed points of a T³/Z₂ orbifold) and the "4π/3" (spherical measure) do not combine into a physical coupling. In the one place 32π/3 legitimately appears — the coefficient Z in a₀ = cH_Λ/Z — every π and both integers cancel, and what is left (κ = ½) is a free posit.',
  },
  {
    href: '/why-z2',
    title: 'Why Z²?',
    what: 'An argument that Z² = 32π/3 is a fundamental constant of nature.',
    why: 'It is not. It appears only as a coefficient in the acceleration scale, and the de Sitter–Unruh argument that produces it actually predicts a coefficient 11.58× larger (Milgrom 1999). The value in use is fitted to data, not derived.',
  },
  {
    href: '/calculator',
    title: 'Constant calculator',
    what: 'A tool that computed "predicted" values of fundamental constants from Z.',
    why: 'It reproduces the retracted derivations. Its outputs are numerical coincidences.',
  },
  {
    href: '/predictions',
    title: 'Predictions table',
    what: 'sin²θ_W = 3/13, Ω_Λ = 13/19, specific particle masses.',
    why: 'Retracted numerology. The surviving falsifiable predictions are gravity-side and pre-registered: the wide-binary γ, the Lorentz-violation dipole sign, and the shape of a₀(z).',
  },
  {
    href: '/compare',
    title: 'Model comparison',
    what: 'Comparisons of this framework against ΛCDM on particle-physics constants.',
    why: 'The particle-physics side of the comparison uses retracted numerology. Only the gravity-side comparison — the radial acceleration relation — is meaningful.',
  },
  {
    href: '/curiosities',
    title: 'Curiosities',
    what: 'Pairings of Z² with cultural, historical and biological patterns.',
    why: 'Numerical coincidences. Included at the time as play; kept now as an illustration of how the pattern-matching went wrong.',
  },
]

const TOPOLOGY: Item[] = [
  {
    href: '/topology',
    title: 'The T³/Z₂ cosmic topology',
    what: 'A claim that the universe is a 20.6 Gpc orbifold, with the DESI four-point correlation function as confirmation.',
    why: 'Tested against CMB matched-circle statistics and rejected. The claimed 4PCF "confirmation" does not survive as evidence for a topology.',
  },
  {
    href: '/universe',
    title: 'Digital twin of the universe',
    what: 'An interactive render of the claimed orbifold topology.',
    why: 'Renders a rejected topology. Kept because the visualisation itself is the artefact worth showing.',
  },
  {
    href: '/digital-twin',
    title: 'Digital twin (alternate)',
    what: 'A second rendering of the same rejected topology.',
    why: 'Same rejection.',
  },
  {
    href: '/lattice',
    title: 'The lattice construction',
    what: 'A lattice underlying the orbifold claim.',
    why: 'Part of the retracted numerology.',
  },
]

const APPLIED: Item[] = [
  {
    href: '/abiogenesis',
    title: 'Abiogenesis',
    what: 'A claim that Z² = 32π/3 appears in protein-backbone geometry and bears on the origin of life.',
    why: 'Failed a false-discovery test — proteins show no significant Z² signal beyond chance. The framework makes no prediction about the origin of life, and never should have.',
  },
  {
    href: '/dark-matter',
    title: 'A dark-matter particle',
    what: 'A Z²-derived particle candidate with a specific keV mass.',
    why: 'The framework uses modified inertia, not particle dark matter. The quoted mass was fabricated.',
  },
  {
    href: '/early-universe',
    title: 'Early universe',
    what: 'Claims that Z² sets primordial structure formation.',
    why: 'Numerology. The surviving claim concerns the present-day galactic acceleration scale, not primordial structure.',
  },
  {
    href: '/el-gordo',
    title: 'El Gordo',
    what: 'A claimed cluster confirmation.',
    why: 'Relies on the retracted cluster numerology. Galaxy clusters are in fact a standing difficulty for MOND-type theories — including this one — not a confirmation of any of them.',
  },
  {
    href: '/ghost-quasars',
    title: 'Ghost quasars',
    what: 'A Z²-based account of anomalous quasar observations.',
    why: 'Part of the retracted numerology.',
  },
  {
    href: '/cosmic-fate',
    title: 'Cosmic fate',
    what: 'A narrative of the universe’s long-term future built on Z².',
    why: 'Built on the retracted numerology.',
  },
  {
    href: '/visualizations',
    title: 'Visualisations',
    what: 'The full visualisation gallery, including the constant "derivations" and the rejected topology.',
    why: 'Mixed. Some panels depict retracted material; the empirically grounded ones — the radial acceleration and Tully–Fisher relations — are on the Simulations page instead.',
  },
]

function Section({ heading, blurb, items }: { heading: string; blurb: string; items: Item[] }) {
  return (
    <section className="mb-12">
      <h2 className="text-lg font-semibold text-gray-900 mb-2">{heading}</h2>
      <p className="text-sm text-gray-600 mb-5">{blurb}</p>
      <div className="space-y-4">
        {items.map((it) => (
          <div key={it.href} className="border border-gray-200 rounded-lg p-4">
            <div className="flex flex-wrap items-baseline justify-between gap-2 mb-2">
              <div className="font-medium text-gray-900">{it.title}</div>
              <Link href={it.href} className="text-sm text-blue-600 hover:underline shrink-0">
                view the page as it stood &rarr;
              </Link>
            </div>
            <p className="text-sm text-gray-700 mb-2">
              <span className="font-medium text-gray-800">Claimed: </span>
              {it.what}
            </p>
            <p className="text-sm text-gray-700">
              <span className="font-medium text-amber-800">Why it is retracted: </span>
              {it.why}
            </p>
          </div>
        ))}
      </div>
    </section>
  )
}

export default function AiSlop() {
  return (
    <main className="min-h-screen bg-white">
      <header className="border-b border-gray-200 bg-gray-50">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <nav className="flex items-center justify-between flex-wrap gap-3">
            <Link href="/" className="text-lg font-semibold text-gray-900 hover:text-gray-600">
              de Sitter&ndash;Unruh Modified Inertia
            </Link>
            <div className="flex items-center gap-6 text-sm">
              <Link href="/" className="text-gray-600 hover:text-gray-900">&larr; Back to the actual claim</Link>
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

      <div className="max-w-4xl mx-auto px-6 py-12">
        <h1 className="text-3xl md:text-4xl font-serif font-normal text-gray-900 mb-3">
          Retracted work
        </h1>
        <p className="text-xl text-gray-600 mb-8 font-light">
          Everything on this page is wrong. It is kept because deleting it would be worse.
        </p>

        <aside
          role="note"
          className="mb-10 rounded-md border border-amber-300 border-l-4 border-l-amber-500 bg-amber-50 px-5 py-4 text-sm leading-relaxed"
        >
          <p className="font-semibold text-amber-900 mb-2">What happened</p>
          <p className="text-amber-900/90 mb-2">
            Between 2025 and mid-2026 this site presented a claimed theory of everything built on a
            single number, Z² = 32π/3, said to arise from the coupling of cubic and spherical symmetry
            in compactified extra dimensions. A large amount of it was generated with heavy AI
            assistance and was not independently checked before publication.
          </p>
          <p className="text-amber-900/90 mb-2">
            On <span className="font-medium">23 June 2026</span> the author retracted all of it
            publicly, to approximately forty physicists. The central failure was simple and is worth
            naming precisely: <span className="font-medium">the recurrence of a number across unrelated
            domains is not evidence.</span> Once a proper false-discovery test was applied, the hit
            rate was indistinguishable from what a randomly chosen constant of similar magnitude
            achieves.
          </p>
          <p className="text-amber-900/90">
            These pages are preserved unaltered, each carrying its own notice, so that the record is
            checkable rather than quietly rewritten. The{' '}
            <Link href="/" className="underline font-medium hover:text-amber-950">
              front page
            </Link>{' '}
            states the one narrow claim that survived audit.
          </p>
        </aside>

        <section className="mb-12 rounded-md border border-gray-300 bg-gray-50 px-5 py-4 text-sm leading-relaxed">
          <p className="font-semibold text-gray-900 mb-2">What survived, for contrast</p>
          <p className="text-gray-700 mb-2">
            One claim: the acceleration scale of the mass-discrepancy&ndash;acceleration relation is set
            by the dark-energy density, a₀ = κ c √(G ρ_Λ) = c H_Λ / Z = 9.36 × 10⁻¹¹ m s⁻², realised as
            modified inertia. It reproduces the radial acceleration relation on 175 SPARC galaxies at
            0.108 dex.
          </p>
          <p className="text-gray-700">
            Even that is narrower than it looks. The law and its de Sitter&ndash;Unruh derivation are{' '}
            <span className="font-medium">Milgrom&rsquo;s (1999)</span>, and his derivation fixes a
            coefficient 11.58× larger than the one used here. The contribution is a re-normalisation of
            that coefficient to fit data, plus a modified-inertia completion. It is also currently in
            conflict with the inner-planet ephemerides at the level of ~10³ unless the relation is read
            as an infrared statement rather than an exact one.
          </p>
        </section>

        <Section
          heading="The numerology"
          blurb="Claims that fundamental constants follow from Z². This is the core of what was retracted."
          items={NUMEROLOGY}
        />

        <Section
          heading="The cosmic topology"
          blurb="Claims about the global shape of the universe, and the visualisations built to render it."
          items={TOPOLOGY}
        />

        <Section
          heading="Applications and extensions"
          blurb="Places the number was extended into domains it had no business in."
          items={APPLIED}
        />

        <footer className="border-t border-gray-200 pt-8 text-sm text-gray-500">
          <p className="mb-2">
            The complete retraction record, including the corrections made <em>after</em> the June 2026
            retraction, is maintained in the public repository at{' '}
            <a
              href="https://github.com/carlzimmerman/zimmerman-formula/blob/main/STANDING.md"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              STANDING.md
            </a>
            , which is newer than this page if the two disagree.
          </p>
          <p>Carl P. Zimmerman &middot; Standing revision 4, 30 July 2026</p>
        </footer>
      </div>
    </main>
  )
}
