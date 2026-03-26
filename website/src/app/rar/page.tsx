'use client'

import dynamic from 'next/dynamic'

const RARVisualization = dynamic(
  () => import('@/components/RARVisualization'),
  { ssr: false }
)

export default function RARPage() {
  return <RARVisualization />
}
