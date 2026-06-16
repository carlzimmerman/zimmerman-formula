import type { Metadata, Viewport } from 'next'
import './globals.css'
import { Analytics } from '@/components/Analytics'
import RouteNotice from '@/components/RouteNotice'

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
  themeColor: '#0a0a1a',
}

export const metadata: Metadata = {
  metadataBase: new URL('https://abeautifullygeometricuniverse.web.app'),
  title: {
    default: 'The MOND Acceleration Scale as a de Sitter Curvature Scale — a₀ = c²√(Λ/32π)',
    template: '%s | Zimmerman Framework'
  },
  description: 'An emergent-gravity proposal in which the galactic acceleration scale is set by the cosmological constant: a₀ = c²√(Λ/32π) = (c/2)√(Gρ_DE) = cH_Λ/Z, Z = √(32π/3) = 5.789, giving a₀ = 9.36×10⁻¹¹ m/s². A theory of gravity and the dark sector — not a theory of everything. Falsifiable via Cassini and the declining prediction a₀(z=3) ≈ 0.74 a₀(0). DOI: 10.5281/zenodo.20721540',
  keywords: [
    // Core result (gravity and dark sector)
    'MOND acceleration scale', 'a0 = c^2 sqrt(Lambda/32pi)', 'de Sitter curvature scale',
    'modified inertia', 'emergent gravity', 'cosmological constant', 'dark energy density',
    // Galaxy dynamics (audited)
    'radial acceleration relation', 'baryonic Tully-Fisher relation',
    'galaxy rotation curves', 'a0 redshift evolution', 'de Sitter-Unruh effect',
    // Tests
    'Cassini test', 'modified inertia vs modified gravity', 'DESI dark energy',
    'high redshift galaxy dynamics', 'external field effect',
    // Foundations
    'MacDowell-Mansouri gravity', 'SO(4,1) gauge gravity', 'AeST',
    // Attribution
    'Carl Zimmerman physics', 'DOI 10.5281/zenodo.20721540'
  ],
  authors: [{ name: 'Carl Zimmerman' }],
  creator: 'Carl Zimmerman',
  publisher: 'Zimmerman Framework Research',
  formatDetection: {
    email: false,
    telephone: false,
  },
  openGraph: {
    title: 'The MOND Acceleration Scale as a de Sitter Curvature Scale',
    description: 'a₀ = c²√(Λ/32π) = 9.36×10⁻¹¹ m/s² — the galactic acceleration scale set by the cosmological constant, via de Sitter–Unruh modified inertia. Reproduces the radial acceleration and baryonic Tully–Fisher relations; predicts a declining a₀(z=3) ≈ 0.74 a₀(0). A theory of gravity and the dark sector, not a theory of everything.',
    url: 'https://abeautifullygeometricuniverse.web.app',
    siteName: 'Zimmerman Framework',
    locale: 'en_US',
    type: 'website',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'a₀ = c²√(Λ/32π) — the MOND scale as a de Sitter curvature scale',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'a₀ = c²√(Λ/32π): the MOND scale as a de Sitter curvature scale',
    description: 'An emergent-gravity proposal tying the galactic acceleration scale to the cosmological constant via modified inertia. Falsifiable by Cassini and by a declining a₀(z). A theory of gravity and the dark sector.',
    creator: '@carlzimmerman',
    images: ['/og-image.png'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    google: 'verification-code-here',
  },
  alternates: {
    canonical: 'https://abeautifullygeometricuniverse.web.app',
  },
  category: 'science',
  other: {
    'citation_title': 'The MOND Acceleration Scale as a de Sitter Curvature Scale: Gauged SO(4,1) Gravity Reduces a₀ = c²√(Λ/32π) to a Single Free Number',
    'citation_author': 'Carl P. Zimmerman',
    'citation_publication_date': '2026',
    'citation_doi': '10.5281/zenodo.20721540',
    'dc.title': 'The MOND Acceleration Scale as a de Sitter Curvature Scale',
    'dc.creator': 'Carl P. Zimmerman',
    'dc.subject': 'modified gravity; modified inertia; cosmology; dark sector; MOND',
    'dc.description': 'An emergent-gravity proposal in which the galactic acceleration scale a₀ = c²√(Λ/32π) is set by the cosmological constant via de Sitter–Unruh modified inertia.',
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
      <body className="antialiased">
        <Analytics />
        <RouteNotice />
        {children}
      </body>
    </html>
  )
}
