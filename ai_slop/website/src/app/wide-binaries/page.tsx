'use client'

import dynamic from 'next/dynamic'

const WideBinaries = dynamic(() => import('@/components/widebinaries/WideBinaries'), { ssr: false })

export default function WideBinariesPage() {
  return <WideBinaries />
}
