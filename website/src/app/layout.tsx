import type { Metadata, Viewport } from 'next'
import './globals.css'

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
    default: 'Zimmerman (2025) — MOND Acceleration Scale from Critical Density',
    template: '%s | Zimmerman Framework'
  },
  description: 'Deriving the MOND acceleration scale a₀ from cosmological critical density: a₀ = c√(Gρc)/2 = cH₀/Z where Z = 2√(8π/3). Framework predicts a₀(z) evolution, resolves Hubble tension (H₀ = 71.5), and explains JWST early galaxies. DOI: 10.5281/zenodo.19199167',
  keywords: [
    // Core physics
    'Zimmerman constant', 'Z = 2√(8π/3)', '5.788810', 'fundamental constants',
    'unified physics theory', 'geometric physics', 'dimensional analysis',
    // Cosmology
    'dark energy density', 'Omega Lambda', 'matter density', 'Omega matter',
    'cosmological constant', 'Hubble tension', 'cosmic coincidence problem',
    'ΛCDM alternative', 'dark energy origin', 'cosmological parameters',
    // Galaxy dynamics
    'Zimmerman acceleration', 'MOND acceleration scale', 'a0 evolution',
    'galaxy rotation curves', 'Tully-Fisher relation', 'BTFR evolution',
    'radial acceleration relation', 'modified Newtonian dynamics',
    // Specific tests
    'El Gordo cluster', 'ACT-CL J0102-4915', 'JWST early galaxies',
    'high redshift galaxy dynamics', 'wide binary stars', 'GAIA data',
    // Particle physics
    'fine structure constant', 'alpha 137', '1/137 origin',
    'proton electron mass ratio', 'muon electron mass ratio',
    'strong coupling constant', 'Weinberg angle',
    // Advanced concepts
    'Einstein field equations 8π', 'gravitational coupling',
    'spatial dimensions geometry', 'quantum gravity connection',
    // DOI and verification
    'Carl Zimmerman physics', 'DOI 10.5281/zenodo.19199167'
  ],
  authors: [{ name: 'Carl Zimmerman' }],
  creator: 'Carl Zimmerman',
  publisher: 'Zimmerman Framework Research',
  formatDetection: {
    email: false,
    telephone: false,
  },
  openGraph: {
    title: 'The Zimmerman Framework: One Constant, All Physics',
    description: 'Z = 2√(8π/3) = 5.788810 derives 36 fundamental constants including dark energy (0.01% error), fine structure constant (0.004% error), and predicts MOND acceleration evolution testable by JWST.',
    url: 'https://abeautifullygeometricuniverse.web.app',
    siteName: 'Zimmerman Framework',
    locale: 'en_US',
    type: 'website',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'Zimmerman Framework: Z = 2√(8π/3) = 5.788810',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Zimmerman Framework: Z = 2√(8π/3)',
    description: 'One geometric constant derives dark energy, fine structure constant, and predicts galaxy dynamics evolution with redshift. Testable by JWST.',
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
    'citation_title': 'The Zimmerman Framework: Deriving Fundamental Constants from Z = 2√(8π/3)',
    'citation_author': 'Carl Zimmerman',
    'citation_publication_date': '2024',
    'citation_doi': '10.5281/zenodo.19199167',
    'dc.title': 'Zimmerman Framework',
    'dc.creator': 'Carl Zimmerman',
    'dc.subject': 'theoretical physics; cosmology; fundamental constants',
    'dc.description': 'Geometric derivation of fundamental physical constants from Z = 2√(8π/3)',
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
        {children}
      </body>
    </html>
  )
}
