'use client'

import dynamic from 'next/dynamic'

const ModelComparison = dynamic(
  () => import('@/components/ModelComparison'),
  { ssr: false }
)

export default function ComparePage() {
  return <ModelComparison />
}
