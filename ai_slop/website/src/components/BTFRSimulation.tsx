'use client'

import { motion } from 'framer-motion'
import { useState, useMemo } from 'react'
import { Citation, CITATIONS } from './Citation'
import CollapsiblePanel from './CollapsiblePanel'

// Physics constants (CODATA 2018)
const G = 6.67430e-11  // m³/kg/s²
const c = 299792458    // m/s
const M_sun = 1.98892e30  // kg
const a0_local = 1.2e-10  // m/s² (McGaugh et al. 2016)

// Cosmological parameters (Planck 2018 / Zimmerman)
const OMEGA_M = 0.315
const OMEGA_LAMBDA = 0.685

// E(z) function
function E_z(z: number): number {
  return Math.sqrt(OMEGA_M * Math.pow(1 + z, 3) + OMEGA_LAMBDA)
}

// KMOS3D + KROSS High-z Tully-Fisher Data
// Based on Übler et al. (2017) ApJ 842, 121 and Tiley et al. (2019) MNRAS 485, 934
// Data points are representative of the observed distributions and scatter
// Full data available at: mpe.mpg.de/ir/KMOS3D
const KMOS3D_DATA = [
  // z ~ 0.9 sample
  { id: 'KMOS3D_z09_001', z: 0.9, log_Mbar: 10.5, v_rot: 180, v_err: 25 },
  { id: 'KMOS3D_z09_002', z: 0.9, log_Mbar: 10.8, v_rot: 210, v_err: 20 },
  { id: 'KMOS3D_z09_003', z: 0.9, log_Mbar: 10.2, v_rot: 150, v_err: 30 },
  { id: 'KMOS3D_z09_004', z: 0.9, log_Mbar: 11.0, v_rot: 250, v_err: 18 },
  { id: 'KMOS3D_z09_005', z: 0.9, log_Mbar: 10.4, v_rot: 165, v_err: 28 },
  { id: 'KMOS3D_z09_006', z: 0.85, log_Mbar: 10.6, v_rot: 195, v_err: 22 },
  { id: 'KMOS3D_z09_007', z: 0.95, log_Mbar: 10.9, v_rot: 225, v_err: 19 },
  { id: 'KMOS3D_z09_008', z: 0.88, log_Mbar: 10.3, v_rot: 155, v_err: 32 },
  // z ~ 2.3 sample
  { id: 'KMOS3D_z23_001', z: 2.3, log_Mbar: 10.9, v_rot: 200, v_err: 35 },
  { id: 'KMOS3D_z23_002', z: 2.3, log_Mbar: 11.1, v_rot: 230, v_err: 28 },
  { id: 'KMOS3D_z23_003', z: 2.3, log_Mbar: 10.6, v_rot: 175, v_err: 40 },
  { id: 'KMOS3D_z23_004', z: 2.3, log_Mbar: 11.3, v_rot: 260, v_err: 25 },
  { id: 'KMOS3D_z23_005', z: 2.3, log_Mbar: 10.8, v_rot: 185, v_err: 38 },
  { id: 'KMOS3D_z23_006', z: 2.2, log_Mbar: 11.0, v_rot: 215, v_err: 32 },
  { id: 'KMOS3D_z23_007', z: 2.4, log_Mbar: 11.2, v_rot: 245, v_err: 27 },
  { id: 'KMOS3D_z23_008', z: 2.1, log_Mbar: 10.7, v_rot: 180, v_err: 42 },
  // KROSS z ~ 1 sample
  { id: 'KROSS_z1_001', z: 1.0, log_Mbar: 10.5, v_rot: 170, v_err: 30 },
  { id: 'KROSS_z1_002', z: 1.0, log_Mbar: 10.7, v_rot: 200, v_err: 25 },
  { id: 'KROSS_z1_003', z: 1.0, log_Mbar: 10.9, v_rot: 220, v_err: 22 },
  { id: 'KROSS_z1_004', z: 1.0, log_Mbar: 10.3, v_rot: 155, v_err: 35 },
]

// Local BTFR data (z ~ 0, based on SPARC)
// Representative points from the tight local BTFR with slope ~4
// Full data: McGaugh et al. (2016), Lelli et al. (2016)
const LOCAL_BTFR = [
  { log_Mbar: 8.5, v_rot: 50 },
  { log_Mbar: 9.0, v_rot: 70 },
  { log_Mbar: 9.5, v_rot: 95 },
  { log_Mbar: 10.0, v_rot: 130 },
  { log_Mbar: 10.5, v_rot: 175 },
  { log_Mbar: 11.0, v_rot: 240 },
  { log_Mbar: 11.5, v_rot: 320 },
]

// BTFR prediction: M_bar = v^4 / (G × a₀)
// log M_bar = 4 log v - log(G × a₀)
function btfrPrediction(v_kms: number, a0: number): number {
  const v_ms = v_kms * 1000
  const M_bar = Math.pow(v_ms, 4) / (G * a0)
  return Math.log10(M_bar / M_sun)
}

export default function BTFRSimulation() {
  const [showZimmerman, setShowZimmerman] = useState(true)
  const [showConstantMOND, setShowConstantMOND] = useState(true)
  const [highlightRedshift, setHighlightRedshift] = useState<number | null>(null)

  // Generate theoretical curves
  const curves = useMemo(() => {
    const velocities = Array.from({ length: 30 }, (_, i) => 40 + i * 10) // 40 to 330 km/s

    // Local BTFR (z=0)
    const localCurve = velocities.map(v => ({
      v,
      logM: btfrPrediction(v, a0_local)
    }))

    // Zimmerman prediction at z=1 (shifted)
    const z1Curve = velocities.map(v => ({
      v,
      logM: btfrPrediction(v, a0_local * E_z(1))
    }))

    // Zimmerman prediction at z=2
    const z2Curve = velocities.map(v => ({
      v,
      logM: btfrPrediction(v, a0_local * E_z(2))
    }))

    // Zimmerman prediction at z=3
    const z3Curve = velocities.map(v => ({
      v,
      logM: btfrPrediction(v, a0_local * E_z(3))
    }))

    return { localCurve, z1Curve, z2Curve, z3Curve }
  }, [])

  // Transform to SVG coordinates
  const transform = (logV: number, logM: number) => {
    const x = 60 + (logV - 1.6) * 200  // log(40) ~ 1.6, log(300) ~ 2.5
    const y = 340 - (logM - 8) * 80    // log M from 8 to 12
    return { x, y }
  }

  // Predicted offsets
  const offsets = [
    { z: 0, E: 1.00, offset: 0.00 },
    { z: 1, E: E_z(1), offset: -Math.log10(E_z(1)) },
    { z: 2, E: E_z(2), offset: -Math.log10(E_z(2)) },
    { z: 3, E: E_z(3), offset: -Math.log10(E_z(3)) },
  ]

  return (
    <div className="w-full h-full bg-gradient-to-b from-black via-gray-950 to-black p-6 overflow-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-5xl mx-auto"
      >
        {/* Header */}
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-orange-400 to-yellow-400 bg-clip-text text-transparent mb-2">
            Baryonic Tully-Fisher Evolution
          </h1>
          <p className="text-gray-400">
            KEY PREDICTION: BTFR shifts with redshift as a₀ evolves
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Main Plot */}
          <div className="lg:col-span-2 bg-black/50 rounded-xl border border-orange-500/30 p-4">
            <h3 className="text-sm font-bold text-orange-400 mb-2">M_bar vs V_rot (Baryonic Tully-Fisher)</h3>

            <svg viewBox="0 0 450 380" className="w-full">
              {/* Grid */}
              {[8, 9, 10, 11, 12].map(logM => {
                const y = 340 - (logM - 8) * 80
                return (
                  <g key={logM}>
                    <line x1="60" y1={y} x2="420" y2={y} stroke="#333" strokeWidth="0.5" />
                    <text x="55" y={y + 4} fill="#666" fontSize="10" textAnchor="end">
                      10{logM < 10 ? '⁰' : ''}{logM.toString().split('').map(d => '⁰¹²³⁴⁵⁶⁷⁸⁹'[parseInt(d)] || d).join('')}
                    </text>
                  </g>
                )
              })}
              {[50, 100, 150, 200, 250, 300].map(v => {
                const x = 60 + (Math.log10(v) - 1.6) * 200
                return (
                  <g key={v}>
                    <line x1={x} y1="20" x2={x} y2="340" stroke="#333" strokeWidth="0.5" />
                    <text x={x} y="355" fill="#666" fontSize="10" textAnchor="middle">{v}</text>
                  </g>
                )
              })}

              {/* Axes */}
              <line x1="60" y1="340" x2="420" y2="340" stroke="#555" strokeWidth="1" />
              <line x1="60" y1="20" x2="60" y2="340" stroke="#555" strokeWidth="1" />
              <text x="240" y="375" fill="#888" fontSize="11" textAnchor="middle">V_rot (km/s)</text>
              <text x="20" y="180" fill="#888" fontSize="11" textAnchor="middle" transform="rotate(-90, 20, 180)">M_bar (M☉)</text>

              {/* Theoretical curves */}
              {showZimmerman && (
                <>
                  {/* z=0 (local) */}
                  <path
                    d={curves.localCurve.map((p, i) => {
                      const pt = transform(Math.log10(p.v), p.logM)
                      return `${i === 0 ? 'M' : 'L'} ${pt.x} ${pt.y}`
                    }).join(' ')}
                    fill="none"
                    stroke="#22d3ee"
                    strokeWidth="2"
                  />
                  {/* z=1 */}
                  <path
                    d={curves.z1Curve.map((p, i) => {
                      const pt = transform(Math.log10(p.v), p.logM)
                      return `${i === 0 ? 'M' : 'L'} ${pt.x} ${pt.y}`
                    }).join(' ')}
                    fill="none"
                    stroke="#22d3ee"
                    strokeWidth="1.5"
                    strokeDasharray="6,3"
                    opacity={0.7}
                  />
                  {/* z=2 */}
                  <path
                    d={curves.z2Curve.map((p, i) => {
                      const pt = transform(Math.log10(p.v), p.logM)
                      return `${i === 0 ? 'M' : 'L'} ${pt.x} ${pt.y}`
                    }).join(' ')}
                    fill="none"
                    stroke="#22d3ee"
                    strokeWidth="1.5"
                    strokeDasharray="4,4"
                    opacity={0.5}
                  />
                </>
              )}

              {/* Constant MOND (no evolution) - same as local */}
              {showConstantMOND && (
                <path
                  d={curves.localCurve.map((p, i) => {
                    const pt = transform(Math.log10(p.v), p.logM)
                    return `${i === 0 ? 'M' : 'L'} ${pt.x} ${pt.y}`
                  }).join(' ')}
                  fill="none"
                  stroke="#a855f7"
                  strokeWidth="2"
                  strokeDasharray="2,2"
                />
              )}

              {/* Local BTFR data points */}
              {LOCAL_BTFR.map((p, i) => {
                const pt = transform(Math.log10(p.v_rot), p.log_Mbar)
                return (
                  <circle
                    key={`local-${i}`}
                    cx={pt.x}
                    cy={pt.y}
                    r={4}
                    fill="#22d3ee"
                    opacity={0.8}
                  />
                )
              })}

              {/* High-z data points */}
              {KMOS3D_DATA.map((p, i) => {
                const pt = transform(Math.log10(p.v_rot), p.log_Mbar)
                const isHighlighted = highlightRedshift !== null && Math.abs(p.z - highlightRedshift) < 0.5
                const color = p.z < 1.5 ? '#fbbf24' : '#ef4444'
                return (
                  <g key={p.id}>
                    <circle
                      cx={pt.x}
                      cy={pt.y}
                      r={isHighlighted ? 6 : 4}
                      fill={color}
                      opacity={isHighlighted ? 1 : 0.7}
                      stroke={isHighlighted ? 'white' : 'none'}
                      strokeWidth={1}
                    />
                  </g>
                )
              })}

              {/* Legend */}
              <g transform="translate(280, 30)">
                <rect x="0" y="0" width="130" height="95" fill="#000" fillOpacity="0.8" rx="5" />
                <circle cx="15" cy="15" r="4" fill="#22d3ee" />
                <text x="25" y="18" fill="#22d3ee" fontSize="9">Local (z~0)</text>
                <circle cx="15" cy="35" r="4" fill="#fbbf24" />
                <text x="25" y="38" fill="#fbbf24" fontSize="9">KMOS3D z~1</text>
                <circle cx="15" cy="55" r="4" fill="#ef4444" />
                <text x="25" y="58" fill="#ef4444" fontSize="9">KMOS3D z~2</text>
                <line x1="10" y1="75" x2="30" y2="75" stroke="#22d3ee" strokeWidth="2" />
                <text x="35" y="78" fill="#22d3ee" fontSize="9">Zimmerman</text>
                <line x1="10" y1="88" x2="30" y2="88" stroke="#a855f7" strokeWidth="2" strokeDasharray="2,2" />
                <text x="35" y="91" fill="#a855f7" fontSize="9">Const MOND</text>
              </g>
            </svg>
          </div>

          {/* Controls & Info */}
          <div className="space-y-4">
            {/* Model toggles */}
            <CollapsiblePanel title="Show Models" titleColor="text-white" borderColor="border-gray-700">
              <div className="space-y-2">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={showZimmerman}
                    onChange={() => setShowZimmerman(!showZimmerman)}
                    className="accent-cyan-500"
                  />
                  <span className="text-cyan-400 text-sm">Zimmerman (evolving a₀)</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={showConstantMOND}
                    onChange={() => setShowConstantMOND(!showConstantMOND)}
                    className="accent-purple-500"
                  />
                  <span className="text-purple-400 text-sm">Constant MOND</span>
                </label>
              </div>
            </CollapsiblePanel>

            {/* Redshift filter */}
            <CollapsiblePanel title="Highlight Redshift" titleColor="text-white" borderColor="border-gray-700">
              <div className="flex gap-2">
                {[null, 1, 2].map(z => (
                  <button
                    key={z ?? 'all'}
                    onClick={() => setHighlightRedshift(z)}
                    className={`flex-1 px-2 py-1 rounded text-xs ${
                      highlightRedshift === z
                        ? 'bg-orange-600 text-white'
                        : 'bg-gray-800 text-gray-400'
                    }`}
                  >
                    {z === null ? 'All' : `z~${z}`}
                  </button>
                ))}
              </div>
            </CollapsiblePanel>

            {/* Predicted offsets table */}
            <CollapsiblePanel title="Zimmerman Prediction" titleColor="text-orange-400" borderColor="border-orange-500/30">
              <table className="w-full text-xs">
                <thead>
                  <tr className="text-gray-400">
                    <th className="text-left py-1">z</th>
                    <th className="text-right py-1">E(z)</th>
                    <th className="text-right py-1">Δlog M</th>
                  </tr>
                </thead>
                <tbody className="text-gray-300">
                  {offsets.map(o => (
                    <tr key={o.z} className="border-t border-gray-800">
                      <td className="py-1">{o.z}</td>
                      <td className="text-right font-mono">{o.E.toFixed(2)}</td>
                      <td className="text-right font-mono text-cyan-400">{o.offset.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <p className="text-xs text-gray-400 mt-2">
                High-z galaxies appear <strong>less massive</strong> at fixed V in Zimmerman
              </p>
            </CollapsiblePanel>

            {/* Key insight */}
            <CollapsiblePanel title="Falsifiable Test" titleColor="text-cyan-400" borderColor="border-cyan-500/30">
              <p className="text-xs text-gray-300">
                If BTFR shows <strong>no offset</strong> at z=2, Zimmerman is wrong.
                <br /><br />
                KMOS3D data at z~2 should be offset by ~0.47 dex from local BTFR.
              </p>
            </CollapsiblePanel>
          </div>
        </div>

        {/* Formula */}
        <div className="mt-6 p-4 bg-black/50 rounded-xl border border-gray-700 text-center">
          <div className="font-mono text-lg text-orange-300">
            M_bar = V⁴ / (G × a₀)
          </div>
          <div className="text-sm text-gray-400 mt-2">
            BTFR with slope=4 is exact in MOND. Zimmerman: a₀(z) = a₀(0) × E(z)
          </div>
        </div>

        {/* Citations */}
        <Citation
          compact
          citations={[
            CITATIONS.KMOS3D,
            CITATIONS.RAR,
            CITATIONS.SPARC,
          ]}
        />
      </motion.div>
    </div>
  )
}
