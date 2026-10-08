import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'A real galaxy, live, under the law',
  description: 'A live N-body of a real SPARC disk galaxy under the MOND-type law with a₀ fixed by the cosmological constant, beside the standard picture with a fitted dark halo. Runs in your browser; indicative, not a result.',
  openGraph: { title: 'A real galaxy, live, under the law', description: 'A live N-body of a real SPARC disk galaxy under the MOND-type law with a₀ fixed by the cosmological constant, beside the standard picture with a fitted dark halo. Runs in your browser; indicative, not a result.' },
}

export default function Layout({ children }: { children: React.ReactNode }) {
  return children
}
