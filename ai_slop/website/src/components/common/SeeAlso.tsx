import React from 'react'
import Link from 'next/link'

const PAGES = [
  { href: '/cosmic-web', title: 'The 512³ run', blurb: 'the simulation behind the growth check, particle by particle' },
  { href: '/galaxy-sim', title: 'A real galaxy, live', blurb: 'SPARC disks under the law, beside a fitted dark halo' },
  { href: '/wide-binaries', title: 'What Gaia DR4 will see', blurb: 'a mock wide-binary sky from the frozen pipeline' },
]

export default function SeeAlso({ current }: { current: string }) {
  return (
    <nav className="py-8 border-t border-gray-200" aria-label="Other simulations">
      <div className="text-xs uppercase tracking-wider text-gray-500 mb-3">more simulations</div>
      <div className="grid sm:grid-cols-2 gap-3 text-sm">
        {PAGES.filter(p => p.href !== current).map(p => (
          <Link key={p.href} href={p.href} className="block border border-gray-200 rounded-lg p-3 hover:border-gray-400 transition-colors">
            <div className="font-medium text-gray-900">{p.title}</div>
            <div className="text-gray-600">{p.blurb}</div>
          </Link>
        ))}
        <Link href="/" className="block border border-gray-200 rounded-lg p-3 hover:border-gray-400 transition-colors"><div className="font-medium text-gray-900">Home</div><div className="text-gray-600">the status of the framework, with what is and is not established</div></Link>
      </div>
    </nav>
  )
}
