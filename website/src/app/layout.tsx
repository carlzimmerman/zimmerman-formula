import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'The Zimmerman Framework | Z = 2√(8π/3)',
  description: 'A unified theory deriving fundamental constants from a single value: Z = 2√(8π/3) = 5.788810...',
  keywords: ['physics', 'cosmology', 'fundamental constants', 'MOND', 'dark energy', 'fine structure constant'],
  authors: [{ name: 'Carl Zimmerman' }],
  openGraph: {
    title: 'The Zimmerman Framework',
    description: 'One constant. All of physics.',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css"
          integrity="sha384-n8MVd4RsNIU0tAv4ct0nTaAbDJwPJzDEaqSD1odI+WdtXRGWt2kTvGFasHpSy3SV"
          crossOrigin="anonymous"
        />
      </head>
      <body className="font-mono text-white antialiased">
        {children}
      </body>
    </html>
  )
}
