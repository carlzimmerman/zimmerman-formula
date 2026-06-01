'use client'

import dynamic from 'next/dynamic'

const ElGordoVisualization = dynamic(
  () => import('@/components/ElGordoVisualization'),
  { ssr: false }
)

export default function ElGordoPage() {
  return <ElGordoVisualization />
}
