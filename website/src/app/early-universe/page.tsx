'use client'

import dynamic from 'next/dynamic'

const EarlyUniverse = dynamic(
  () => import('@/components/EarlyUniverse'),
  { ssr: false }
)

export default function EarlyUniversePage() {
  return <EarlyUniverse />
}
