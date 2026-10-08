'use client'

import dynamic from 'next/dynamic'

const GalaxySim = dynamic(() => import('@/components/galaxysim/GalaxySim'), { ssr: false })

export default function GalaxySimPage() {
  return <GalaxySim />
}
