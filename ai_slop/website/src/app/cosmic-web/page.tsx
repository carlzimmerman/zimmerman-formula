'use client'

import dynamic from 'next/dynamic'

const CosmicWeb = dynamic(() => import('@/components/cosmicweb/CosmicWeb'), { ssr: false })

export default function CosmicWebPage() {
  return <CosmicWeb />
}
