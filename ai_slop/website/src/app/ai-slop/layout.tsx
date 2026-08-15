import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Retracted work — the Z² numerology, kept as a record',
  description:
    'Everything collected here was retracted publicly on 23 June 2026: the claimed derivations of fundamental constants from Z² = 32π/3, the T³/Z₂ cosmic topology, and the applications built on them. Kept unaltered, each page carrying its own notice, so the record is checkable. The one surviving claim — a₀ = cH_Λ/Z as a de Sitter curvature scale — is on the front page.',
  robots: { index: false, follow: true },
}

export default function AiSlopLayout({ children }: { children: React.ReactNode }) {
  return children
}
