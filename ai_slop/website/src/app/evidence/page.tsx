'use client'

import dynamic from 'next/dynamic'

const EvidenceTimeline = dynamic(
  () => import('@/components/EvidenceTimeline'),
  { ssr: false }
)

export default function EvidencePage() {
  return <EvidenceTimeline />
}
