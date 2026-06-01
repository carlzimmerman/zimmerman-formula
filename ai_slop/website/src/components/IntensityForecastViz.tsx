'use client'

export default function IntensityForecastViz() {
  return (
    <div className="w-full h-full min-h-screen bg-black flex items-center justify-center p-8">
      <div className="max-w-2xl text-center">
        <div className="text-6xl mb-6">📈</div>
        <h2 className="text-2xl font-bold text-white mb-4">Intensity Forecast Visualization</h2>
        <p className="text-gray-400 mb-6">
          Full intensity evolution comparison between models and observations.
        </p>

        <div className="bg-gray-800/50 rounded-lg p-6 border border-rose-500/30 mb-6">
          <div className="text-rose-400 font-mono mb-2">
            I(t) = I₀ × exp(−t/τ) × f(Z)
          </div>
          <p className="text-gray-500 text-sm">
            Intensity decay with Z-dependent correction factor
          </p>
        </div>

        <div className="grid grid-cols-3 gap-4 text-sm">
          <div className="bg-gray-900 rounded p-3">
            <div className="text-rose-400 font-bold">ΛCDM</div>
            <div className="text-gray-500">Standard model</div>
          </div>
          <div className="bg-gray-900 rounded p-3">
            <div className="text-purple-400 font-bold">Z²</div>
            <div className="text-gray-500">This framework</div>
          </div>
          <div className="bg-gray-900 rounded p-3">
            <div className="text-green-400 font-bold">Observed</div>
            <div className="text-gray-500">Real data</div>
          </div>
        </div>

        <p className="text-gray-600 text-sm mt-6">
          Full comparison visualization coming soon
        </p>
      </div>
    </div>
  )
}
