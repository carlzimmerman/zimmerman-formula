import Link from 'next/link'

export const metadata = {
  title: 'Predictions moved',
}

// The old predictions cards predate the retractions. The current record is the Kepler Grade Prediction Chart.
export default function Predictions() {
  return (
    <main className="min-h-screen bg-[#fafafa]">
      <meta httpEquiv="refresh" content="0; url=/kepler-grade/" />
      <div className="max-w-xl mx-auto px-4 py-12">
        <h1 className="text-2xl font-semibold text-gray-900 mb-3">The predictions page has moved</h1>
        <p className="text-gray-600 mb-4">
          The earlier cards on this page predate the retractions. The current record, with every dated test, its kill
          criterion, the confronted results and the withdrawn claims, is the Kepler Grade Prediction Chart.
        </p>
        <a href="/kepler-grade/" className="text-blue-600 hover:underline">Open the Kepler Grade Prediction Chart</a>
        <p className="mt-6 text-sm"><Link href="/" className="text-blue-600 hover:underline">← Home</Link></p>
      </div>
    </main>
  )
}
