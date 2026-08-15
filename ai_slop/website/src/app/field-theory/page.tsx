'use client';

import Link from 'next/link';
import dynamic from 'next/dynamic';

const RARRealPanel = dynamic(() => import('@/components/RARRealPanel'), { ssr: false });
const ActionExplorer = dynamic(() => import('@/components/ActionExplorer'), { ssr: false });
const DbiPressurePanel = dynamic(() => import('@/components/DbiPressurePanel'), { ssr: false });
const A0RedshiftDiscriminator = dynamic(() => import('@/components/A0RedshiftDiscriminator'), { ssr: false });

const VERIFIED = [
  ['Lensing (the test that killed modified inertia)', 'Φ = Ψ ⇒ γ_PPN = 1; the 21.2σ exclusion clears at 0.6σ'],
  ['CMB', 'full Boltzmann (CLASS) pass; re-run with the derived a₀(z): 0.01σ vs cosmic variance'],
  ['Gravitational waves', 'c_T = 1 exactly, by construction (GW170817-safe)'],
  ['Stability', 'no-ghost theorem over the whole field range; subluminal sound speed'],
  ['Radial acceleration relation', '0.108 dex on 175 SPARC galaxies at Υ = 0.70 — the panel above'],
  ['Weak lensing, 40 kpc – 2.2 Mpc', 'pure framework, no dark component: χ²/dof = 2.03 canonical / 0.94 alt (real KiDS data)'],
  ['Solar system', 'Newtonian residual e^(−√y) ≈ 10⁻³⁴⁵⁷ at Earth'],
  ['Wide binaries (the live test)', 'hash-frozen pre-registration for Gaia DR4: γ_v = 1.1614–1.1814 / 1.1917–1.2267, decided ~Dec 2026'],
];

const NOT_CLAIMED = [
  'κ = ½ is NOT derived. It is fitted; the distance-free measurement is 0.551 ± 0.043, and four candidate coefficients sit inside 2σ.',
  'β = 1 is selected by the CMB off-switch, not derived.',
  'Dark matter exists at full Ω_dm here. The claim is "no dark-matter PARTICLE" — the dark sector is a field. Whether galaxies keep their captured charge is the programme’s named open problem, worked in the open.',
  'The full nonlinear Boltzmann run at this kinetic function is still owed (its stakes are priced at ≤0.5%, but priced is not performed).',
  'The scaffold — AeST itself — is Skordis & Złośnik’s (PRL 127, 161302), credited throughout. This programme contributes the a₀ normalisation, the pressure promotion, the derived a₀(z), and the Q₀ pin.',
];

export default function FieldTheoryPage() {
  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800">
        <div className="mx-auto max-w-5xl px-6 py-4">
          <nav className="flex flex-wrap items-center justify-between gap-3">
            <Link href="/" className="text-lg font-semibold text-white hover:text-gray-300">
              a₀ from the Cosmological Constant
            </Link>
            <div className="flex items-center gap-6 text-sm">
              <Link href="/simulate" className="text-gray-400 hover:text-white">Simulations</Link>
              <Link href="/rar" className="text-gray-400 hover:text-white">Galaxy data</Link>
              <Link href="/ai-slop" className="text-amber-500 hover:text-amber-300">Retracted work</Link>
            </div>
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-6 py-12">
        {/* hero */}
        <p className="text-sm uppercase tracking-widest text-gray-500">The flagship result</p>
        <h1 className="mt-2 text-3xl font-bold text-white sm:text-4xl">
          One field theory for the galaxies and the CMB
        </h1>
        <div className="mt-6 rounded-xl border border-gray-800 bg-gray-900/60 p-6 text-center">
          <div className="font-mono text-xl text-cyan-300 sm:text-2xl">
            a₀ = κ c √(G ρ_Λ) = c²√(Λ/32π) = 9.36 × 10⁻¹¹ m s⁻²
          </div>
          <div className="mt-2 text-sm text-gray-400">
            the galactic acceleration scale, set by the dark-energy density — with κ = ½ fitted, not
            derived — embedded in a complete relativistic action where{' '}
            <span className="text-gray-200">the MOND scale is the dark sector&rsquo;s pressure</span>:
            𝒜(Q) ≡ a₀²(Q) = κ²G(−K(Q))
          </div>
        </div>
        <p className="mt-4 text-sm leading-relaxed text-gray-400">
          Five steps, each with the real numbers on it. Everything here is reproduced by committed,
          runnable scripts in the{' '}
          <a href="https://github.com/carlzimmerman/zimmerman-formula" className="text-cyan-400 hover:text-cyan-300">
            repository
          </a>{' '}
          — and everything this site once claimed beyond it is retracted and archived under{' '}
          <Link href="/ai-slop" className="text-amber-500 hover:text-amber-300">Retracted work</Link>.
        </p>

        {/* step 1 */}
        <section className="mt-14">
          <h2 className="text-xl font-semibold text-white">
            <span className="mr-2 text-cyan-400">1.</span> Start from the data: one acceleration, everywhere
          </h2>
          <p className="mb-4 mt-2 text-sm leading-relaxed text-gray-400">
            In every disc galaxy measured, the gravity that is observed departs from the gravity the
            visible matter provides at the same acceleration, a₀ ≈ 10⁻¹⁰ m s⁻². Below: no simulation,
            no synthetic points — the actual SPARC measurements, one dot per measured radius, against
            the framework&rsquo;s two curves at a fixed, global mass-to-light ratio.
          </p>
          <RARRealPanel />
        </section>

        {/* step 2 */}
        <section className="mt-14">
          <h2 className="text-xl font-semibold text-white">
            <span className="mr-2 text-cyan-400">2.</span> The coincidence that becomes the claim
          </h2>
          <p className="mt-2 text-sm leading-relaxed text-gray-400">
            That scale is numerically tied to the cosmological constant: a₀ = κc√(Gρ_Λ) with κ = ½
            makes every π and every numerical factor cancel. The tie itself has prior art three times
            over (Milgrom 1999 derived the exact law with coefficient 2cH_Λ; Pikhitsa 2010 and
            Klinkhamer–Kopp 2011 landed on the same 2cH_Λ) — what this programme adds is the
            re-normalised coefficient that the data actually select, and everything below.
          </p>
        </section>

        {/* step 3 */}
        <section className="mt-14">
          <h2 className="text-xl font-semibold text-white">
            <span className="mr-2 text-cyan-400">3.</span> Give it a relativistic home
          </h2>
          <p className="mb-4 mt-2 text-sm leading-relaxed text-gray-400">
            A number is not a theory. The scale is embedded in Aether–Scalar–Tensor theory — the one
            relativistic MOND-class theory that fits the CMB — with a single structural promotion.
          </p>
          <ActionExplorer />
        </section>

        {/* step 4 */}
        <section className="mt-14">
          <h2 className="text-xl font-semibold text-white">
            <span className="mr-2 text-cyan-400">4.</span> The engine: dark energy, dark matter, and the
            off-switch are one function
          </h2>
          <p className="mb-4 mt-2 text-sm leading-relaxed text-gray-400">
            The promotion makes a₀² proportional to the dark sector&rsquo;s pressure. One bounded
            function then does three jobs at once — and because the excitation grows into the past,
            the theory itself decides when MOND is on.
          </p>
          <DbiPressurePanel />
        </section>

        {/* step 5 */}
        <section className="mt-14">
          <h2 className="text-xl font-semibold text-white">
            <span className="mr-2 text-cyan-400">5.</span> The derived a₀(z) — and what would kill it
          </h2>
          <p className="mb-4 mt-2 text-sm leading-relaxed text-gray-400">
            The redshift dependence is no longer imposed; it follows from the action. It is flat to
            &lt;1% everywhere rotation data exist, and off at recombination — so the CMB&rsquo;s
            clustering is a prediction, and the observed absence of Tully–Fisher zero-point evolution
            at 1 &lt; z &lt; 5 is a pass. Falsifier, either sign: a robust 0.15 dex zero-point shift
            in gas-dominated systems at z ≤ 1.
          </p>
          <A0RedshiftDiscriminator />
        </section>

        {/* step 6 */}
        <section className="mt-14">
          <h2 className="text-xl font-semibold text-white">
            <span className="mr-2 text-cyan-400">6.</span> What is verified — and what is not claimed
          </h2>
          <div className="mt-4 overflow-x-auto rounded-xl border border-gray-800">
            <table className="w-full text-sm">
              <tbody>
                {VERIFIED.map(([k, v]) => (
                  <tr key={k} className="border-b border-gray-800/60 last:border-0">
                    <td className="px-4 py-3 font-medium text-gray-200">{k}</td>
                    <td className="px-4 py-3 text-gray-400">{v}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="mt-6 rounded-xl border border-amber-900/60 bg-amber-950/20 p-5">
            <div className="mb-2 text-sm font-semibold text-amber-300">Stated as plainly as the results:</div>
            <ul className="list-disc space-y-2 pl-5 text-sm text-gray-300">
              {NOT_CLAIMED.map((n) => (
                <li key={n.slice(0, 24)}>{n}</li>
              ))}
            </ul>
          </div>
          <p className="mt-6 text-sm text-gray-400">
            Papers:{' '}
            <a href="https://doi.org/10.5281/zenodo.21895046" className="text-cyan-400 hover:text-cyan-300">
              THE COMPLETION (v9)
            </a>{' · '}
            <a href="https://doi.org/10.5281/zenodo.21937958" className="text-cyan-400 hover:text-cyan-300">
              Pinning AeST&rsquo;s Q₀ (v4)
            </a>{' · '}
            <a href="https://doi.org/10.5281/zenodo.21937976" className="text-cyan-400 hover:text-cyan-300">
              The DR4 target under a local a₀
            </a>{' · '}
            <a href="https://doi.org/10.5281/zenodo.21865866" className="text-cyan-400 hover:text-cyan-300">
              plain-language companion
            </a>
          </p>
        </section>
      </main>

      <footer className="border-t border-gray-800 py-8 text-center text-sm text-gray-500">
        Modified gravity anchored to the cosmological constant — a proposal about gravity and the dark
        sector. <span className="font-medium text-gray-400">Not a theory of everything.</span>
      </footer>
    </div>
  );
}
