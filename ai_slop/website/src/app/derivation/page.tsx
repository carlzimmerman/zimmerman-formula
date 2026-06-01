'use client'

import dynamic from 'next/dynamic'

const Derivation = dynamic(
  () => import('@/components/Derivation'),
  { ssr: false }
)

export default function DerivationPage() {
  return <Derivation />
}
