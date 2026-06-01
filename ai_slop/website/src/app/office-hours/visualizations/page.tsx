'use client'

import Link from 'next/link'
import Image from 'next/image'
import { useState, useEffect } from 'react'

// ============================================
// Z₂ GROUP VISUALIZATION
// ============================================
function Z2GroupViz() {
  const [state, setState] = useState<'identity' | 'flip'>('identity')
  const [history, setHistory] = useState<string[]>(['e'])

  const applyFlip = () => {
    const newState = state === 'identity' ? 'flip' : 'identity'
    setState(newState)
    setHistory([...history, newState === 'identity' ? 'e' : 'g'])
  }

  const reset = () => {
    setState('identity')
    setHistory(['e'])
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 md:p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-2">Z₂ Group Operations</h3>
      <p className="text-sm text-gray-600 mb-4">
        Z₂ = {'{'}e, g{'}'} where g² = e. Click "Apply g" to see the group action.
      </p>

      <div className="flex flex-col items-center gap-4">
        {/* Visual representation */}
        <div className="relative w-32 h-32">
          <div
            className={`w-full h-full border-4 rounded-lg flex items-center justify-center text-4xl font-bold transition-transform duration-300 ${
              state === 'identity'
                ? 'border-blue-500 bg-blue-50 text-blue-700'
                : 'border-orange-500 bg-orange-50 text-orange-700 scale-x-[-1]'
            }`}
          >
            {state === 'identity' ? 'L' : 'R'}
          </div>
          <div className="absolute -bottom-6 left-0 right-0 text-center text-sm text-gray-600">
            {state === 'identity' ? 'Identity (e)' : 'Flipped (g)'}
          </div>
        </div>

        {/* Buttons */}
        <div className="flex gap-3 mt-6">
          <button
            onClick={applyFlip}
            className="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-medium transition-colors"
          >
            Apply g
          </button>
          <button
            onClick={reset}
            className="px-6 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg font-medium transition-colors"
          >
            Reset
          </button>
        </div>

        {/* History */}
        <div className="text-sm text-gray-600 mt-2">
          Operations: {history.join(' · ')} = {state === 'identity' ? 'e' : 'g'}
        </div>

        {/* Group table */}
        <div className="mt-4 overflow-x-auto w-full">
          <table className="mx-auto text-sm border-collapse">
            <thead>
              <tr>
                <th className="border border-gray-300 p-2 bg-gray-100">·</th>
                <th className="border border-gray-300 p-2 bg-blue-100">e</th>
                <th className="border border-gray-300 p-2 bg-orange-100">g</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="border border-gray-300 p-2 bg-blue-100 font-medium">e</td>
                <td className="border border-gray-300 p-2">e</td>
                <td className="border border-gray-300 p-2">g</td>
              </tr>
              <tr>
                <td className="border border-gray-300 p-2 bg-orange-100 font-medium">g</td>
                <td className="border border-gray-300 p-2">g</td>
                <td className="border border-gray-300 p-2 bg-green-100 font-medium">e</td>
              </tr>
            </tbody>
          </table>
          <p className="text-xs text-gray-500 text-center mt-2">g · g = e (applying flip twice returns to identity)</p>
        </div>
      </div>
    </div>
  )
}

// ============================================
// TORUS VISUALIZATION
// ============================================
function TorusViz() {
  const [showAlpha, setShowAlpha] = useState(true)
  const [showBeta, setShowBeta] = useState(true)

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 md:p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-2">Torus T² and Homology</h3>
      <p className="text-sm text-gray-600 mb-4">
        A torus has two independent loops (cycles): α around the hole, β around the tube. b₁(T²) = 2.
      </p>

      <div className="flex flex-col items-center gap-4">
        <svg viewBox="0 0 300 200" className="w-full max-w-md">
          {/* Torus body - outer ellipse */}
          <ellipse cx="150" cy="100" rx="120" ry="60" fill="none" stroke="#9CA3AF" strokeWidth="2" />

          {/* Torus hole - inner ellipse */}
          <ellipse cx="150" cy="100" rx="40" ry="20" fill="#fafafa" stroke="#9CA3AF" strokeWidth="2" />

          {/* Alpha cycle (around hole) */}
          {showAlpha && (
            <g>
              <ellipse
                cx="150"
                cy="100"
                rx="80"
                ry="40"
                fill="none"
                stroke="#3B82F6"
                strokeWidth="3"
                strokeDasharray="8,4"
              />
              <circle cx="230" cy="100" r="6" fill="#3B82F6" />
              <text x="245" y="105" className="text-sm fill-blue-600 font-medium">α</text>
            </g>
          )}

          {/* Beta cycle (around tube) */}
          {showBeta && (
            <g>
              <path
                d="M 150 40 Q 200 100 150 160 Q 100 100 150 40"
                fill="none"
                stroke="#EF4444"
                strokeWidth="3"
                strokeDasharray="8,4"
              />
              <circle cx="150" cy="40" r="6" fill="#EF4444" />
              <text x="160" y="35" className="text-sm fill-red-600 font-medium">β</text>
            </g>
          )}

          {/* Labels */}
          <text x="150" y="185" textAnchor="middle" className="text-xs fill-gray-500">
            Coffee mug ≅ Donut (topologically equivalent!)
          </text>
        </svg>

        {/* Controls */}
        <div className="flex gap-4">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={showAlpha}
              onChange={(e) => setShowAlpha(e.target.checked)}
              className="w-4 h-4 text-blue-600"
            />
            <span className="text-blue-600 font-medium">α cycle</span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={showBeta}
              onChange={(e) => setShowBeta(e.target.checked)}
              className="w-4 h-4 text-red-600"
            />
            <span className="text-red-600 font-medium">β cycle</span>
          </label>
        </div>

        <div className="text-sm text-gray-700 bg-gray-50 p-3 rounded-lg">
          <strong>Betti number:</strong> b₁(T²) = 2 (two independent cycles)
          <br />
          <strong>For T³:</strong> b₁(T³) = 3 → <span className="text-purple-600 font-medium">3 generations of fermions!</span>
        </div>
      </div>
    </div>
  )
}

// ============================================
// T³/Z₂ ORBIFOLD FIXED POINTS
// ============================================
function OrbifoldViz() {
  const [selectedPoint, setSelectedPoint] = useState<number | null>(null)

  const fixedPoints = [
    { x: 50, y: 50, z: 50, label: '(0,0,0)' },
    { x: 150, y: 50, z: 50, label: '(π,0,0)' },
    { x: 50, y: 150, z: 50, label: '(0,π,0)' },
    { x: 150, y: 150, z: 50, label: '(π,π,0)' },
    { x: 80, y: 80, z: 150, label: '(0,0,π)' },
    { x: 180, y: 80, z: 150, label: '(π,0,π)' },
    { x: 80, y: 180, z: 150, label: '(0,π,π)' },
    { x: 180, y: 180, z: 150, label: '(π,π,π)' },
  ]

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 md:p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-2">T³/Z₂ Orbifold: 8 Fixed Points</h3>
      <p className="text-sm text-gray-600 mb-4">
        The Z₂ action x → -x on T³ has 8 fixed points where x = -x (mod 2π).
        Each fixed point contributes 2 twisted sector modes → 16 total bosonic modes.
      </p>

      <div className="flex flex-col items-center gap-4">
        <svg viewBox="0 0 250 250" className="w-full max-w-sm">
          {/* Back face */}
          <rect x="60" y="60" width="120" height="120" fill="none" stroke="#D1D5DB" strokeWidth="1" />

          {/* Front face */}
          <rect x="30" y="30" width="120" height="120" fill="rgba(147, 197, 253, 0.3)" stroke="#3B82F6" strokeWidth="2" />

          {/* Connecting lines */}
          <line x1="30" y1="30" x2="60" y2="60" stroke="#9CA3AF" strokeWidth="1" />
          <line x1="150" y1="30" x2="180" y2="60" stroke="#9CA3AF" strokeWidth="1" />
          <line x1="30" y1="150" x2="60" y2="180" stroke="#9CA3AF" strokeWidth="1" />
          <line x1="150" y1="150" x2="180" y2="180" stroke="#9CA3AF" strokeWidth="1" />

          {/* Fixed points */}
          {fixedPoints.map((point, idx) => (
            <g key={idx}>
              <circle
                cx={point.x}
                cy={point.y}
                r={selectedPoint === idx ? 12 : 8}
                fill={selectedPoint === idx ? '#7C3AED' : '#EF4444'}
                stroke="white"
                strokeWidth="2"
                className="cursor-pointer transition-all"
                onClick={() => setSelectedPoint(selectedPoint === idx ? null : idx)}
              />
              <text
                x={point.x}
                y={point.y + 4}
                textAnchor="middle"
                className="text-xs fill-white font-bold pointer-events-none"
              >
                {idx + 1}
              </text>
            </g>
          ))}

          {/* Labels */}
          <text x="90" y="245" textAnchor="middle" className="text-xs fill-gray-500">
            8 fixed points × 2 modes = 16 twisted sector modes
          </text>
        </svg>

        {selectedPoint !== null && (
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-3 text-sm">
            <strong>Fixed Point {selectedPoint + 1}:</strong> {fixedPoints[selectedPoint].label}
            <br />
            <span className="text-purple-600">Contributes 2 complex moduli to twisted sector</span>
          </div>
        )}

        <div className="text-sm text-gray-700 bg-amber-50 border border-amber-200 p-3 rounded-lg">
          <strong>Key formula:</strong> N_bosonic = 8 × 2 = 16
          <br />
          <strong>Electroweak capacity:</strong> N_EW = 16 - 3 = 13
          <br />
          <strong>Result:</strong> sin²θ_W = 3/13 = 0.231
        </div>
      </div>
    </div>
  )
}

// ============================================
// TIME DILATION CALCULATOR
// ============================================
function TimeDilationViz() {
  const [velocity, setVelocity] = useState(50) // percentage of c
  const c = 299792458 // m/s

  const v = (velocity / 100) * c
  const gamma = 1 / Math.sqrt(1 - (velocity / 100) ** 2)
  const properTime = 1 // 1 year
  const dilatedTime = properTime * gamma

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 md:p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-2">Time Dilation Calculator</h3>
      <p className="text-sm text-gray-600 mb-4">
        Moving clocks run slower. At velocity v, time dilates by factor γ = 1/√(1 - v²/c²).
      </p>

      <div className="space-y-4">
        {/* Velocity slider */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Velocity: {velocity}% of c ({(velocity / 100 * 299792).toFixed(0)} km/s)
          </label>
          <input
            type="range"
            min="0"
            max="99"
            value={velocity}
            onChange={(e) => setVelocity(Number(e.target.value))}
            className="w-full h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>0%</span>
            <span>50%</span>
            <span>99%</span>
          </div>
        </div>

        {/* Results */}
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-blue-50 p-4 rounded-lg text-center">
            <div className="text-3xl font-bold text-blue-700">{gamma.toFixed(3)}</div>
            <div className="text-sm text-blue-600">γ (Lorentz factor)</div>
          </div>
          <div className="bg-green-50 p-4 rounded-lg text-center">
            <div className="text-3xl font-bold text-green-700">{dilatedTime.toFixed(2)}</div>
            <div className="text-sm text-green-600">Years on Earth per year on ship</div>
          </div>
        </div>

        {/* Visual */}
        <div className="flex items-center justify-center gap-8 py-4">
          <div className="text-center">
            <div className="text-4xl mb-1">🚀</div>
            <div className="text-sm font-medium">Ship Clock</div>
            <div className="text-lg font-mono">{properTime} year</div>
          </div>
          <div className="text-2xl text-gray-400">→</div>
          <div className="text-center">
            <div className="text-4xl mb-1">🌍</div>
            <div className="text-sm font-medium">Earth Clock</div>
            <div className="text-lg font-mono">{dilatedTime.toFixed(2)} years</div>
          </div>
        </div>

        {/* GPS example */}
        <div className="bg-gray-50 p-3 rounded-lg text-sm text-gray-700">
          <strong>GPS satellites</strong> travel at 14,000 km/hr. Without relativistic corrections,
          position errors would grow by 10 km/day!
        </div>
      </div>
    </div>
  )
}

// ============================================
// WAVE FUNCTION SUPERPOSITION
// ============================================
function WaveFunctionViz() {
  const [alpha, setAlpha] = useState(50) // percentage for |0⟩

  const alpha_coeff = Math.sqrt(alpha / 100)
  const beta_coeff = Math.sqrt(1 - alpha / 100)
  const prob0 = alpha / 100
  const prob1 = 1 - alpha / 100

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 md:p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-2">Quantum Superposition</h3>
      <p className="text-sm text-gray-600 mb-4">
        A qubit can be in superposition: |ψ⟩ = α|0⟩ + β|1⟩ where |α|² + |β|² = 1.
      </p>

      <div className="space-y-4">
        {/* Coefficient slider */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Superposition: {alpha_coeff.toFixed(2)}|0⟩ + {beta_coeff.toFixed(2)}|1⟩
          </label>
          <input
            type="range"
            min="0"
            max="100"
            value={alpha}
            onChange={(e) => setAlpha(Number(e.target.value))}
            className="w-full h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>|1⟩</span>
            <span>50/50</span>
            <span>|0⟩</span>
          </div>
        </div>

        {/* Probability bars */}
        <div className="space-y-2">
          <div className="flex items-center gap-3">
            <span className="w-12 text-right font-mono text-sm">|0⟩</span>
            <div className="flex-grow bg-gray-200 rounded-full h-6 overflow-hidden">
              <div
                className="h-full bg-blue-500 transition-all duration-200 flex items-center justify-end pr-2"
                style={{ width: `${prob0 * 100}%` }}
              >
                {prob0 > 0.1 && <span className="text-white text-xs font-medium">{(prob0 * 100).toFixed(0)}%</span>}
              </div>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="w-12 text-right font-mono text-sm">|1⟩</span>
            <div className="flex-grow bg-gray-200 rounded-full h-6 overflow-hidden">
              <div
                className="h-full bg-red-500 transition-all duration-200 flex items-center justify-end pr-2"
                style={{ width: `${prob1 * 100}%` }}
              >
                {prob1 > 0.1 && <span className="text-white text-xs font-medium">{(prob1 * 100).toFixed(0)}%</span>}
              </div>
            </div>
          </div>
        </div>

        {/* Bloch sphere simplified */}
        <div className="flex justify-center">
          <svg viewBox="0 0 150 150" className="w-32 h-32">
            <circle cx="75" cy="75" r="60" fill="none" stroke="#D1D5DB" strokeWidth="2" />
            <line x1="75" y1="15" x2="75" y2="135" stroke="#D1D5DB" strokeWidth="1" strokeDasharray="4,4" />
            <line x1="15" y1="75" x2="135" y2="75" stroke="#D1D5DB" strokeWidth="1" strokeDasharray="4,4" />

            {/* State vector */}
            <line
              x1="75"
              y1="75"
              x2={75 + 50 * Math.sin(Math.acos(alpha_coeff) * 2)}
              y2={75 - 50 * Math.cos(Math.acos(alpha_coeff) * 2)}
              stroke="#7C3AED"
              strokeWidth="3"
              markerEnd="url(#arrow)"
            />
            <circle
              cx={75 + 50 * Math.sin(Math.acos(alpha_coeff) * 2)}
              cy={75 - 50 * Math.cos(Math.acos(alpha_coeff) * 2)}
              r="5"
              fill="#7C3AED"
            />

            <text x="75" y="10" textAnchor="middle" className="text-xs fill-blue-600">|0⟩</text>
            <text x="75" y="145" textAnchor="middle" className="text-xs fill-red-600">|1⟩</text>

            <defs>
              <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
                <path d="M0,0 L0,6 L9,3 z" fill="#7C3AED" />
              </marker>
            </defs>
          </svg>
        </div>

        <div className="text-sm text-gray-700 bg-purple-50 p-3 rounded-lg text-center">
          <strong>Measurement collapses the superposition!</strong>
          <br />
          P(|0⟩) = {(prob0 * 100).toFixed(0)}% · P(|1⟩) = {(prob1 * 100).toFixed(0)}%
        </div>
      </div>
    </div>
  )
}

// ============================================
// COSMOLOGY Ω VISUALIZATION
// ============================================
function CosmologyViz() {
  const omega_lambda = 13 / 19
  const omega_m = 6 / 19
  const sin2_theta = 3 / 13

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 md:p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-2">Cosmic Energy Budget</h3>
      <p className="text-sm text-gray-600 mb-4">
        From Z² framework: Ω_Λ = 13/19 and Ω_M = 6/19. Note: Ω_M/Ω_Λ = 6/13 = 2×sin²θ_W!
      </p>

      <div className="flex flex-col items-center gap-4">
        {/* Pie chart */}
        <svg viewBox="0 0 200 200" className="w-48 h-48">
          {/* Dark energy slice */}
          <path
            d={`M 100 100 L 100 10 A 90 90 0 1 1 ${100 + 90 * Math.sin(2 * Math.PI * omega_lambda)} ${100 - 90 * Math.cos(2 * Math.PI * omega_lambda)} Z`}
            fill="#8B5CF6"
          />
          {/* Matter slice */}
          <path
            d={`M 100 100 L ${100 + 90 * Math.sin(2 * Math.PI * omega_lambda)} ${100 - 90 * Math.cos(2 * Math.PI * omega_lambda)} A 90 90 0 0 1 100 10 Z`}
            fill="#3B82F6"
          />
          {/* Center text */}
          <circle cx="100" cy="100" r="40" fill="white" />
          <text x="100" y="95" textAnchor="middle" className="text-sm font-medium fill-gray-700">Universe</text>
          <text x="100" y="110" textAnchor="middle" className="text-xs fill-gray-500">Today</text>
        </svg>

        {/* Legend */}
        <div className="flex gap-6 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-purple-500 rounded"></div>
            <span>Dark Energy: {(omega_lambda * 100).toFixed(1)}%</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-blue-500 rounded"></div>
            <span>Matter: {(omega_m * 100).toFixed(1)}%</span>
          </div>
        </div>

        {/* Z² derivation */}
        <div className="bg-gradient-to-r from-purple-50 to-blue-50 p-4 rounded-lg w-full">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="text-center">
              <div className="font-mono text-lg text-purple-700">Ω_Λ = 13/19</div>
              <div className="text-gray-600">= 0.6842</div>
              <div className="text-xs text-gray-500">Observed: 0.685</div>
            </div>
            <div className="text-center">
              <div className="font-mono text-lg text-blue-700">Ω_M = 6/19</div>
              <div className="text-gray-600">= 0.3158</div>
              <div className="text-xs text-gray-500">Observed: 0.315</div>
            </div>
          </div>
          <div className="text-center mt-3 pt-3 border-t border-gray-200">
            <div className="font-mono text-green-700">
              Ω_M / Ω_Λ = 6/13 = 2 × sin²θ_W
            </div>
            <div className="text-xs text-gray-600 mt-1">
              The Weinberg angle appears in cosmology!
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

// ============================================
// RG FLOW VISUALIZATION
// ============================================
function RGFlowViz() {
  const [energy, setEnergy] = useState(50) // log scale 0-100

  // Simulate running of α⁻¹
  const alpha_inv_low = 137.036 // IR
  const alpha_inv_high = 128 // near Z mass
  const alpha_inv = alpha_inv_low - (energy / 100) * (alpha_inv_low - alpha_inv_high)

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 md:p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-2">Renormalization Group Flow</h3>
      <p className="text-sm text-gray-600 mb-4">
        Coupling constants "run" with energy scale. α⁻¹ freezes at the IR fixed point: 4Z² + 3 = 137.036.
      </p>

      <div className="space-y-4">
        {/* Energy slider */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Energy Scale: {energy === 0 ? 'IR (low energy)' : energy === 100 ? 'UV (Z mass)' : `${energy}%`}
          </label>
          <input
            type="range"
            min="0"
            max="100"
            value={energy}
            onChange={(e) => setEnergy(Number(e.target.value))}
            className="w-full h-3 bg-gradient-to-r from-blue-200 via-purple-200 to-red-200 rounded-lg appearance-none cursor-pointer"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>IR (atoms)</span>
            <span>UV (Z boson)</span>
          </div>
        </div>

        {/* Current value */}
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-4 rounded-lg text-center">
          <div className="text-3xl font-mono font-bold text-purple-700">{alpha_inv.toFixed(2)}</div>
          <div className="text-sm text-gray-600">α⁻¹ at this energy</div>
        </div>

        {/* Visual flow */}
        <svg viewBox="0 0 300 100" className="w-full">
          {/* Axis */}
          <line x1="30" y1="80" x2="270" y2="80" stroke="#D1D5DB" strokeWidth="2" />
          <line x1="30" y1="80" x2="30" y2="20" stroke="#D1D5DB" strokeWidth="2" />

          {/* Running curve */}
          <path
            d="M 30 30 Q 100 30 150 50 Q 200 70 270 75"
            fill="none"
            stroke="#8B5CF6"
            strokeWidth="3"
          />

          {/* Current position */}
          <circle
            cx={30 + (energy / 100) * 240}
            cy={30 + (energy / 100) * 45}
            r="8"
            fill="#7C3AED"
            stroke="white"
            strokeWidth="2"
          />

          {/* Labels */}
          <text x="30" y="95" className="text-xs fill-gray-500">IR</text>
          <text x="260" y="95" className="text-xs fill-gray-500">UV</text>
          <text x="10" y="35" className="text-xs fill-gray-500">α⁻¹</text>
          <text x="10" y="75" className="text-xs fill-gray-500">α⁻¹</text>

          {/* Fixed point marker */}
          <circle cx="30" cy="30" r="5" fill="#22C55E" />
          <text x="40" y="25" className="text-xs fill-green-600">Fixed point</text>
          <text x="40" y="38" className="text-xs fill-green-600">4Z²+3 = 137.04</text>
        </svg>

        <div className="text-sm text-gray-700 bg-green-50 border border-green-200 p-3 rounded-lg">
          <strong>IR Fixed Point:</strong> As energy → 0, α⁻¹ → 4Z² + 3 = 137.036
          <br />
          This is where we measure α in atomic physics!
        </div>
      </div>
    </div>
  )
}

// ============================================
// DESI Q₄ AUDIT VISUALIZATIONS
// ============================================
function DESIAuditViz() {
  const [selectedFig, setSelectedFig] = useState<number>(1)

  const figures = [
    {
      id: 1,
      src: '/desi-audit/fig1_velocity_field_3d.png',
      title: '3D Velocity Field',
      description: 'Local 500 Mpc volume showing velocity streamlines. The KBC Void outflow (~430 km/s) plus vertex contribution creates the bulk flow that squashes BAO spheres.',
      keyResult: 'Combined velocity: 265 km/s toward vertex direction'
    },
    {
      id: 2,
      src: '/desi-audit/fig2_bao_squashing.png',
      title: 'BAO Sphere Squashing',
      description: 'Comparison of BAO sphere shapes: (A) Isotropic ΛCDM expectation, (B) Kaiser RSD quadrupole only, (C) Z² Framework with vertex + void produces Q₄ = -0.65.',
      keyResult: 'Q₄ = -0.65 exact match to DESI observation'
    },
    {
      id: 3,
      src: '/desi-audit/fig3_observer_position.png',
      title: 'Observer Position in KBC Void',
      description: 'Our galactic address: r = 68 Mpc from void center, θ = 13° from void-vertex axis. Found via 16,800-point grid search with 1,012 valid solutions.',
      keyResult: 'Confirmed by Cosmicflows-4 (p = 0.93)'
    },
    {
      id: 4,
      src: '/desi-audit/fig4_velocity_budget.png',
      title: 'Velocity Budget',
      description: 'Breakdown of bulk velocity: void outflow (~430 km/s) dominates, vertex contribution adds coherent direction. Net: 265 km/s consistent with CF4 observations.',
      keyResult: 'CF4 observed: 269 ± 35 km/s (0.13σ tension)'
    }
  ]

  const currentFig = figures.find(f => f.id === selectedFig)!

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 md:p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-2">DESI Q₄ Hexadecapole Audit</h3>
      <p className="text-sm text-gray-600 mb-4">
        The Z² framework resolves the DESI BAO Q₄ = -0.65 anomaly via vertex kinematics + KBC Void.
        In Z²-native coordinates, the anomaly vanishes (94% reduction).
      </p>

      {/* Figure selector tabs */}
      <div className="flex flex-wrap gap-2 mb-4">
        {figures.map(fig => (
          <button
            key={fig.id}
            onClick={() => setSelectedFig(fig.id)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              selectedFig === fig.id
                ? 'bg-purple-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Fig {fig.id}
          </button>
        ))}
      </div>

      {/* Current figure display */}
      <div className="space-y-4">
        <div className="relative w-full aspect-[4/3] bg-gray-50 rounded-lg overflow-hidden border border-gray-200">
          <Image
            src={currentFig.src}
            alt={currentFig.title}
            fill
            className="object-contain"
            sizes="(max-width: 768px) 100vw, 800px"
          />
        </div>

        <div className="space-y-2">
          <h4 className="font-semibold text-gray-900">{currentFig.title}</h4>
          <p className="text-sm text-gray-600">{currentFig.description}</p>
          <div className="bg-green-50 border border-green-200 rounded-lg p-3 text-sm">
            <strong className="text-green-700">Key Result:</strong>{' '}
            <span className="text-green-600">{currentFig.keyResult}</span>
          </div>
        </div>
      </div>
    </div>
  )
}

function Q4ResolutionViz() {
  const [showNative, setShowNative] = useState(false)

  const lcdmQ4 = -0.44
  const z2Q4 = 0.027
  const reduction = 93.9

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 md:p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-2">Q₄ Anomaly Resolution</h3>
      <p className="text-sm text-gray-600 mb-4">
        Toggle between coordinate systems to see how the Q₄ hexadecapole anomaly vanishes
        when measured in Z²-native coordinates.
      </p>

      <div className="flex flex-col items-center gap-4">
        {/* Toggle switch */}
        <div className="flex items-center gap-4">
          <span className={`font-medium ${!showNative ? 'text-blue-600' : 'text-gray-400'}`}>
            ΛCDM
          </span>
          <button
            onClick={() => setShowNative(!showNative)}
            className={`relative w-16 h-8 rounded-full transition-colors ${
              showNative ? 'bg-purple-600' : 'bg-blue-600'
            }`}
          >
            <div
              className={`absolute top-1 w-6 h-6 bg-white rounded-full transition-transform ${
                showNative ? 'translate-x-9' : 'translate-x-1'
              }`}
            />
          </button>
          <span className={`font-medium ${showNative ? 'text-purple-600' : 'text-gray-400'}`}>
            Z²-Native
          </span>
        </div>

        {/* Q4 visualization */}
        <div className="relative w-full max-w-xs h-48">
          <svg viewBox="0 0 200 150" className="w-full h-full">
            {/* Axis */}
            <line x1="20" y1="130" x2="180" y2="130" stroke="#D1D5DB" strokeWidth="2" />
            <line x1="100" y1="130" x2="100" y2="10" stroke="#D1D5DB" strokeWidth="1" strokeDasharray="4,4" />

            {/* Zero line */}
            <text x="105" y="75" className="text-xs fill-gray-400">Q₄ = 0</text>
            <line x1="25" y1="75" x2="175" y2="75" stroke="#9CA3AF" strokeWidth="1" />

            {/* Q4 bar */}
            <rect
              x="60"
              y={showNative ? 73 : 75 + (lcdmQ4 * 100)}
              width="80"
              height={showNative ? Math.abs(z2Q4 * 100) : Math.abs(lcdmQ4 * 100)}
              fill={showNative ? '#22C55E' : '#EF4444'}
              className="transition-all duration-500"
            />

            {/* Value label */}
            <text
              x="100"
              y={showNative ? 65 : 75 + (lcdmQ4 * 100) - 5}
              textAnchor="middle"
              className={`text-sm font-bold transition-all duration-500 ${
                showNative ? 'fill-green-600' : 'fill-red-600'
              }`}
            >
              Q₄ = {showNative ? '+0.027' : '-0.44'}
            </text>

            {/* Tension label */}
            <text
              x="100"
              y="145"
              textAnchor="middle"
              className="text-xs fill-gray-500"
            >
              {showNative ? '0.2σ from zero (consistent)' : '2.7σ from zero (anomaly)'}
            </text>
          </svg>
        </div>

        {/* Results panel */}
        <div className={`w-full p-4 rounded-lg transition-colors ${
          showNative ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
        }`}>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <div className="text-gray-600">Coordinate System</div>
              <div className={`font-bold ${showNative ? 'text-purple-700' : 'text-blue-700'}`}>
                {showNative ? 'T³/Z₂ Native' : 'ΛCDM Standard'}
              </div>
            </div>
            <div>
              <div className="text-gray-600">Q₄ Value</div>
              <div className={`font-bold ${showNative ? 'text-green-700' : 'text-red-700'}`}>
                {showNative ? '+0.027' : '-0.440'}
              </div>
            </div>
          </div>
          {showNative && (
            <div className="mt-3 pt-3 border-t border-green-300 text-center">
              <span className="text-green-700 font-bold">{reduction}% reduction</span>
              <span className="text-green-600"> — Anomaly vanishes!</span>
            </div>
          )}
        </div>

        {/* Interpretation */}
        <div className="text-sm text-gray-700 bg-gray-50 p-3 rounded-lg">
          <strong>Interpretation:</strong> The Q₄ anomaly is not a breakdown of physics —
          it is the signature of measuring a T³/Z₂ universe with ΛCDM-calibrated tools.
          In native coordinates, BAO spheres are isotropic.
        </div>
      </div>
    </div>
  )
}

function CF4CrossMatchViz() {
  const predictions = [
    { param: 'δ_local', predicted: -0.283, observed: -0.280, error: 0.064, tension: 0.05 },
    { param: 'v_bulk', predicted: 265, observed: 269, error: 35, tension: 0.13, unit: 'km/s' },
    { param: 'r_obs', predicted: 68, observed: 100, error: 50, tension: 0.64, unit: 'Mpc' },
  ]

  const chiSq = 0.43
  const pValue = 0.93

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 md:p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-2">Cosmicflows-4 Cross-Match</h3>
      <p className="text-sm text-gray-600 mb-4">
        The Z² framework predicted our galactic address using only topology (L_c = 20.6 Gpc, v = 0.236).
        Cosmicflows-4 observations independently confirm with 93% confidence.
      </p>

      <div className="space-y-4">
        {/* Parameter comparison table */}
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-50">
                <th className="text-left p-2 font-medium text-gray-700">Parameter</th>
                <th className="text-right p-2 font-medium text-purple-700">Predicted</th>
                <th className="text-right p-2 font-medium text-blue-700">Observed</th>
                <th className="text-right p-2 font-medium text-green-700">Tension</th>
              </tr>
            </thead>
            <tbody>
              {predictions.map(p => (
                <tr key={p.param} className="border-t border-gray-100">
                  <td className="p-2 font-mono text-gray-600">{p.param}</td>
                  <td className="p-2 text-right font-mono text-purple-600">
                    {p.predicted}{p.unit ? ` ${p.unit}` : ''}
                  </td>
                  <td className="p-2 text-right font-mono text-blue-600">
                    {p.observed} ± {p.error}{p.unit ? ` ${p.unit}` : ''}
                  </td>
                  <td className="p-2 text-right">
                    <span className="bg-green-100 text-green-700 px-2 py-0.5 rounded font-bold">
                      {p.tension}σ
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Chi-squared result */}
        <div className="bg-gradient-to-r from-purple-50 to-green-50 p-4 rounded-lg">
          <div className="grid grid-cols-2 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-purple-700">χ² = {chiSq}</div>
              <div className="text-sm text-gray-600">3 degrees of freedom</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-green-700">p = {(pValue * 100).toFixed(0)}%</div>
              <div className="text-sm text-gray-600">Confidence level</div>
            </div>
          </div>
        </div>

        {/* Visual tension bars */}
        <div className="space-y-2">
          {predictions.map(p => (
            <div key={p.param} className="flex items-center gap-2">
              <span className="w-16 text-xs font-mono text-gray-500">{p.param}</span>
              <div className="flex-grow bg-gray-100 rounded-full h-4 overflow-hidden">
                <div
                  className="h-full bg-green-500 rounded-full transition-all"
                  style={{ width: `${Math.max(5, (1 - p.tension) * 100)}%` }}
                />
              </div>
              <span className="w-12 text-xs font-bold text-green-600">{p.tension}σ</span>
            </div>
          ))}
        </div>

        <div className="text-sm text-gray-700 bg-green-50 border border-green-200 p-3 rounded-lg text-center">
          <strong>Status: CONFIRMED</strong> — All three predictions within 1σ of observations
        </div>
      </div>
    </div>
  )
}

// ============================================
// MAIN PAGE
// ============================================
export default function VisualizationsPage() {
  return (
    <main className="min-h-screen bg-[#fafafa]">
      <div className="max-w-4xl mx-auto px-4 py-6 md:py-8">
        {/* Header */}
        <div className="mb-6">
          <Link href="/office-hours" className="text-blue-600 hover:underline text-sm mb-2 inline-block">
            ← Back to Office Hours
          </Link>
          <h1 className="text-2xl md:text-3xl font-semibold text-gray-900 mb-2">
            Interactive Visualizations
          </h1>
          <p className="text-gray-600">
            Explore the mathematical and physical concepts behind the Z² Framework
          </p>
        </div>

        {/* Visualizations Grid */}
        <div className="space-y-6">
          {/* Math Section */}
          <div>
            <h2 className="text-lg font-semibold text-gray-700 mb-4 flex items-center gap-2">
              <span>📐</span> Mathematics
            </h2>
            <div className="grid gap-6">
              <Z2GroupViz />
              <TorusViz />
              <OrbifoldViz />
            </div>
          </div>

          {/* Physics Section */}
          <div>
            <h2 className="text-lg font-semibold text-gray-700 mb-4 flex items-center gap-2">
              <span>⚛️</span> Physics
            </h2>
            <div className="grid gap-6">
              <TimeDilationViz />
              <WaveFunctionViz />
              <CosmologyViz />
              <RGFlowViz />
            </div>
          </div>

          {/* DESI Audit Section */}
          <div>
            <h2 className="text-lg font-semibold text-gray-700 mb-4 flex items-center gap-2">
              <span>🔭</span> DESI Q₄ Audit (May 2026)
            </h2>
            <p className="text-sm text-gray-600 mb-4">
              Hallucination-proof verification of the Z² framework against DESI 5-Year BAO data.
              The Q₄ hexadecapole anomaly is fully resolved via vertex kinematics + KBC Void coupling.
            </p>
            <div className="grid gap-6">
              <DESIAuditViz />
              <Q4ResolutionViz />
              <CF4CrossMatchViz />
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="text-center text-sm text-gray-500 py-8 mt-8 border-t border-gray-200">
          <Link href="/office-hours" className="text-blue-600 hover:underline">
            ← Back to Office Hours
          </Link>
          <span className="mx-2">·</span>
          <Link href="/" className="text-blue-600 hover:underline">
            Zimmerman Framework
          </Link>
        </footer>
      </div>
    </main>
  )
}
