import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'What Gaia DR4 will see: a mock wide-binary sky',
  description: "A mock Gaia DR4 wide-binary sky built with the repository's frozen pre-registered pipeline: what each law would return when DR4 is released on 2 December 2026. A forecast, not a measurement.",
  openGraph: { title: 'What Gaia DR4 will see: a mock wide-binary sky', description: "A mock Gaia DR4 wide-binary sky built with the repository's frozen pre-registered pipeline: what each law would return when DR4 is released on 2 December 2026. A forecast, not a measurement." },
}

export default function Layout({ children }: { children: React.ReactNode }) {
  return children
}
