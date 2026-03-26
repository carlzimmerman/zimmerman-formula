'use client'

import { useRef, useMemo, useState } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Stars, Html } from '@react-three/drei'
import * as THREE from 'three'
import { motion } from 'framer-motion'

// Physics constants (CODATA 2018)
const Z = 2 * Math.sqrt(8 * Math.PI / 3)  // 5.788810
const G = 6.67430e-11  // m³/kg/s²
const c = 299792458    // m/s
const a0_local = 1.2e-10  // m/s² (McGaugh et al. 2016)
const kpc_to_m = 3.08567758e19
const M_sun = 1.98892e30  // kg

// Real SPARC Galaxy Data (Lelli, McGaugh, Schombert 2016, AJ 152, 157)
// Selected galaxies spanning dwarf to massive spirals
const SPARC_GALAXIES = [
  { name: 'NGC 2403', distance: 3.2, vFlat: 134, rLast: 22, mass: 3.2e10, type: 'Spiral (Sc)' },
  { name: 'NGC 3198', distance: 13.8, vFlat: 150, rLast: 30, mass: 4.5e10, type: 'Spiral (SBc)' },
  { name: 'NGC 6946', distance: 5.9, vFlat: 210, rLast: 20, mass: 8.1e10, type: 'Spiral (SABcd)' },
  { name: 'UGC 128', distance: 64, vFlat: 131, rLast: 55, mass: 2.9e10, type: 'LSB' },
  { name: 'DDO 154', distance: 4.0, vFlat: 47, rLast: 8, mass: 4.0e8, type: 'Dwarf Irregular' },
  { name: 'NGC 2841', distance: 14.1, vFlat: 305, rLast: 50, mass: 2.1e11, type: 'Spiral (SAb)' },
  { name: 'NGC 7331', distance: 14.7, vFlat: 250, rLast: 35, mass: 1.2e11, type: 'Spiral (SAb)' },
  { name: 'IC 2574', distance: 4.0, vFlat: 67, rLast: 13, mass: 1.5e9, type: 'Dwarf Irregular' },
  { name: 'NGC 3521', distance: 10.7, vFlat: 227, rLast: 35, mass: 9.5e10, type: 'Spiral (SABbc)' },
  { name: 'NGC 5055', distance: 10.1, vFlat: 200, rLast: 45, mass: 7.2e10, type: 'Spiral (SAbc)' },
]

// Calculate E(z) = H(z)/H₀
function E_z(z: number): number {
  const Omega_m = 0.315
  const Omega_L = 0.685
  return Math.sqrt(Omega_m * Math.pow(1 + z, 3) + Omega_L)
}

// Calculate a₀ at redshift z
function a0_at_z(z: number): number {
  return a0_local * E_z(z)
}

// Calculate MOND radius scaling at redshift z
// r_M(z) = r_M(0) / sqrt(E(z)) - galaxies are more compact at high z
function sizeScaling(z: number): number {
  return 1 / Math.sqrt(E_z(z))
}

// Zimmerman/MOND rotation velocity using RAR formula
function zimmermanVelocity(r_kpc: number, M_solar: number, a0: number): number {
  const r_m = r_kpc * kpc_to_m
  const M_kg = M_solar * M_sun
  const g_bar = G * M_kg / (r_m * r_m)  // Baryonic acceleration

  // RAR interpolating function: g_obs = g_bar / (1 - exp(-√(g_bar/a₀)))
  const x = Math.sqrt(g_bar / a0)
  const g_obs = g_bar / (1 - Math.exp(-x))

  return Math.sqrt(g_obs * r_m)  // m/s
}

// Newtonian rotation velocity (no dark matter)
function newtonianVelocity(r_kpc: number, M_solar: number): number {
  const r_m = r_kpc * kpc_to_m
  const M_kg = M_solar * M_sun
  return Math.sqrt(G * M_kg / r_m)  // m/s
}

// ΛCDM velocity with NFW dark matter halo
function lcdmVelocity(r_kpc: number, M_solar: number): number {
  const r_m = r_kpc * kpc_to_m
  const M_kg = M_solar * M_sun

  // Baryonic contribution
  const v_bar_sq = G * M_kg / r_m

  // NFW halo parameters (typical concentration c~10, mass ratio ~5:1)
  const M_halo = M_kg * 5  // Dark matter mass ~5× baryonic
  const rs = 20 * kpc_to_m  // Scale radius ~20 kpc
  const x = r_m / rs

  // NFW enclosed mass fraction
  const f_nfw = Math.log(1 + x) - x / (1 + x)
  const M_dm_enclosed = M_halo * f_nfw / (Math.log(11) - 10/11)  // Normalized to total
  const v_dm_sq = G * M_dm_enclosed / r_m

  return Math.sqrt(v_bar_sq + v_dm_sq)  // m/s
}

type PhysicsModel = 'zimmerman' | 'newton' | 'lcdm'

interface StarParticlesProps {
  count: number
  galaxy: typeof SPARC_GALAXIES[0]
  a0: number
  model: PhysicsModel
  redshift: number
}

function StarParticles({ count, galaxy, a0, model, redshift }: StarParticlesProps) {
  const meshRef = useRef<THREE.InstancedMesh>(null)
  const dummy = useMemo(() => new THREE.Object3D(), [])

  // Scale factor: galaxy rLast maps to 5 visual units
  // In Zimmerman mode, galaxies are more compact at high z (MOND radius shrinks)
  const zimScale = model === 'zimmerman' ? sizeScaling(redshift) : 1
  const scaleFactor = (5 / galaxy.rLast) * zimScale

  // Generate star positions with exponential disk distribution
  const stars = useMemo(() => {
    const temp = []
    for (let i = 0; i < count; i++) {
      // Exponential disk distribution scaled to galaxy size
      const u = Math.random()
      const r_kpc = -galaxy.rLast * 0.3 * Math.log(1 - u * 0.95)  // Exponential with scale ~30% of rLast
      const r_visual = Math.min(r_kpc * scaleFactor, 5)  // Clamp to visual bounds
      const theta = Math.random() * Math.PI * 2
      const height = (Math.random() - 0.5) * 0.15 * Math.exp(-r_kpc / (galaxy.rLast * 0.3))  // Thin disk

      temp.push({
        r_visual,
        r_kpc: Math.max(r_kpc, 0.5),  // Minimum radius
        theta,
        height,
      })
    }
    return temp
  }, [count, galaxy, scaleFactor, zimScale])

  useFrame((state) => {
    if (!meshRef.current) return

    const time = state.clock.getElapsedTime()

    stars.forEach((star, i) => {
      // Calculate orbital velocity based on selected physics model
      let v: number
      switch (model) {
        case 'zimmerman':
          v = zimmermanVelocity(star.r_kpc, galaxy.mass, a0)
          break
        case 'lcdm':
          v = lcdmVelocity(star.r_kpc, galaxy.mass)
          break
        case 'newton':
        default:
          v = newtonianVelocity(star.r_kpc, galaxy.mass)
      }

      // Angular velocity ω = v / r
      const r_m = star.r_kpc * kpc_to_m
      const omega = v / r_m

      // Scale time for visualization (speed up by ~10^15)
      const scaledOmega = omega * 5e14

      // Update position
      const currentTheta = star.theta + scaledOmega * time
      const x = star.r_visual * Math.cos(currentTheta)
      const z = star.r_visual * Math.sin(currentTheta)
      const y = star.height

      dummy.position.set(x, y, z)
      dummy.scale.setScalar(0.015 + 0.008 * Math.random())
      dummy.updateMatrix()
      meshRef.current!.setMatrixAt(i, dummy.matrix)
    })

    meshRef.current.instanceMatrix.needsUpdate = true
  })

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <sphereGeometry args={[1, 6, 6]} />
      <meshBasicMaterial color="#ffffff" />
    </instancedMesh>
  )
}

interface RotationCurveDisplayProps {
  galaxy: typeof SPARC_GALAXIES[0]
  a0: number
  model: PhysicsModel
}

function RotationCurveDisplay({ galaxy, a0, model }: RotationCurveDisplayProps) {
  const points = useMemo(() => {
    const zimmermanPoints: [number, number][] = []
    const newtonPoints: [number, number][] = []
    const lcdmPoints: [number, number][] = []
    const observedFlat: [number, number][] = []

    const rMax = galaxy.rLast
    const dr = rMax / 40

    for (let r = 1; r <= rMax; r += dr) {
      const vZim = zimmermanVelocity(r, galaxy.mass, a0) / 1000  // km/s
      const vNewton = newtonianVelocity(r, galaxy.mass) / 1000
      const vLcdm = lcdmVelocity(r, galaxy.mass) / 1000

      zimmermanPoints.push([r, vZim])
      newtonPoints.push([r, vNewton])
      lcdmPoints.push([r, vLcdm])

      // Observed flat rotation (approximation)
      observedFlat.push([r, galaxy.vFlat])
    }

    return { zimmermanPoints, newtonPoints, lcdmPoints, observedFlat }
  }, [galaxy, a0])

  const maxV = Math.max(galaxy.vFlat * 1.3, ...points.zimmermanPoints.map(p => p[1]))
  const maxR = galaxy.rLast

  return (
    <div className="absolute bottom-4 left-4 w-80 bg-black/90 backdrop-blur p-4 rounded-lg border border-purple-500/30">
      <h3 className="text-sm font-bold text-purple-400 mb-1">{galaxy.name} Rotation Curve</h3>
      <p className="text-xs text-gray-500 mb-2">{galaxy.type} | M = {(galaxy.mass / 1e10).toFixed(1)} × 10¹⁰ M☉</p>

      <svg viewBox="0 0 120 70" className="w-full h-36">
        {/* Grid */}
        {[0, 0.5, 1].map(frac => (
          <line key={frac} x1="15" y1={55 - frac * 45} x2="115" y2={55 - frac * 45} stroke="#333" strokeWidth="0.3" />
        ))}

        {/* Axes */}
        <line x1="15" y1="55" x2="115" y2="55" stroke="#555" strokeWidth="0.5" />
        <line x1="15" y1="55" x2="15" y2="8" stroke="#555" strokeWidth="0.5" />

        {/* Observed flat (yellow dashed) */}
        <path
          d={points.observedFlat.map((p, i) =>
            `${i === 0 ? 'M' : 'L'} ${15 + (p[0] / maxR) * 100} ${55 - (p[1] / maxV) * 45}`
          ).join(' ')}
          fill="none"
          stroke="#fbbf24"
          strokeWidth="1.5"
          strokeDasharray="3,2"
          opacity={0.8}
        />

        {/* Newtonian (gray dashed) */}
        <path
          d={points.newtonPoints.map((p, i) =>
            `${i === 0 ? 'M' : 'L'} ${15 + (p[0] / maxR) * 100} ${55 - (p[1] / maxV) * 45}`
          ).join(' ')}
          fill="none"
          stroke="#666"
          strokeWidth="1"
          strokeDasharray="2,2"
        />

        {/* ΛCDM (red) */}
        <path
          d={points.lcdmPoints.map((p, i) =>
            `${i === 0 ? 'M' : 'L'} ${15 + (p[0] / maxR) * 100} ${55 - (p[1] / maxV) * 45}`
          ).join(' ')}
          fill="none"
          stroke="#ef4444"
          strokeWidth="1.2"
          opacity={model === 'lcdm' ? 1 : 0.5}
        />

        {/* Zimmerman (cyan) */}
        <path
          d={points.zimmermanPoints.map((p, i) =>
            `${i === 0 ? 'M' : 'L'} ${15 + (p[0] / maxR) * 100} ${55 - (p[1] / maxV) * 45}`
          ).join(' ')}
          fill="none"
          stroke="#22d3ee"
          strokeWidth="1.5"
          opacity={model === 'zimmerman' ? 1 : 0.5}
        />

        {/* Labels */}
        <text x="65" y="68" fill="#888" fontSize="4" textAnchor="middle">Radius (kpc)</text>
        <text x="5" y="30" fill="#888" fontSize="4" textAnchor="middle" transform="rotate(-90, 5, 30)">V (km/s)</text>
        <text x="15" y="63" fill="#666" fontSize="3">0</text>
        <text x="115" y="63" fill="#666" fontSize="3">{maxR}</text>
        <text x="10" y="57" fill="#666" fontSize="3">0</text>
        <text x="8" y="12" fill="#666" fontSize="3">{Math.round(maxV)}</text>
      </svg>

      {/* Legend */}
      <div className="grid grid-cols-2 gap-1 text-xs mt-1">
        <span className="flex items-center gap-1"><span className="w-3 h-0.5 bg-yellow-400"></span> Observed</span>
        <span className="flex items-center gap-1"><span className="w-3 h-0.5 bg-cyan-400"></span> Zimmerman</span>
        <span className="flex items-center gap-1"><span className="w-3 h-0.5 bg-red-500"></span> ΛCDM</span>
        <span className="flex items-center gap-1"><span className="w-3 h-0.5 bg-gray-500"></span> Newton</span>
      </div>

      <p className="text-xs text-gray-500 mt-2">Data: SPARC (Lelli+ 2016)</p>
    </div>
  )
}

function GalaxyCore() {
  const coreRef = useRef<THREE.Mesh>(null)

  useFrame((state) => {
    if (coreRef.current) {
      coreRef.current.rotation.y = state.clock.getElapsedTime() * 0.1
    }
  })

  return (
    <mesh ref={coreRef}>
      <sphereGeometry args={[0.3, 32, 32]} />
      <meshBasicMaterial color="#fbbf24" transparent opacity={0.8} />
      <pointLight color="#fbbf24" intensity={2} distance={10} />
    </mesh>
  )
}

export default function GalaxySimulation() {
  const [redshift, setRedshift] = useState(0)
  const [model, setModel] = useState<PhysicsModel>('zimmerman')
  const [galaxyIndex, setGalaxyIndex] = useState(0)

  const galaxy = SPARC_GALAXIES[galaxyIndex]
  const a0 = a0_at_z(redshift)

  // Calculate cosmic time from redshift (approximate)
  const cosmicTime = redshift === 0 ? 13.8 : 13.8 / Math.pow(1 + redshift, 1.5)

  return (
    <div className="relative w-full h-screen bg-black">
      {/* 3D Canvas */}
      <Canvas camera={{ position: [0, 8, 12], fov: 45 }}>
        <ambientLight intensity={0.1} />
        <Stars radius={100} depth={50} count={5000} factor={4} fade speed={1} />

        <GalaxyCore />
        <StarParticles
          count={2500}
          galaxy={galaxy}
          a0={a0}
          model={model}
          redshift={redshift}
        />

        <OrbitControls
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          autoRotate={false}
          maxDistance={30}
          minDistance={5}
        />
      </Canvas>

      {/* Rotation Curve Display */}
      <RotationCurveDisplay galaxy={galaxy} a0={a0} model={model} />

      {/* Controls */}
      <div className="absolute top-4 left-4 right-4 flex flex-col gap-4">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-black/90 backdrop-blur p-4 rounded-lg border border-purple-500/30 max-w-md"
        >
          <h2 className="text-lg font-bold text-white mb-1">
            Galaxy Rotation Simulation
          </h2>
          <p className="text-xs text-gray-400 mb-3">
            Real SPARC data: compare Newton, ΛCDM dark matter, and Zimmerman predictions
          </p>

          {/* Galaxy Selector */}
          <div className="mb-4">
            <label className="text-xs text-gray-400 mb-1 block">Select Galaxy (SPARC)</label>
            <select
              value={galaxyIndex}
              onChange={(e) => setGalaxyIndex(parseInt(e.target.value))}
              className="w-full bg-gray-800 text-white px-3 py-2 rounded border border-gray-600 text-sm"
            >
              {SPARC_GALAXIES.map((g, i) => (
                <option key={g.name} value={i}>
                  {g.name} — {g.type} (v={g.vFlat} km/s)
                </option>
              ))}
            </select>
          </div>

          {/* Physics Model Toggle */}
          <div className="mb-4">
            <label className="text-xs text-gray-400 mb-2 block">Physics Model</label>
            <div className="flex gap-2">
              <button
                onClick={() => setModel('zimmerman')}
                className={`flex-1 px-3 py-2 rounded text-sm font-medium transition-all ${
                  model === 'zimmerman'
                    ? 'bg-cyan-600 text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                Zimmerman
              </button>
              <button
                onClick={() => setModel('lcdm')}
                className={`flex-1 px-3 py-2 rounded text-sm font-medium transition-all ${
                  model === 'lcdm'
                    ? 'bg-red-600 text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                ΛCDM
              </button>
              <button
                onClick={() => setModel('newton')}
                className={`flex-1 px-3 py-2 rounded text-sm font-medium transition-all ${
                  model === 'newton'
                    ? 'bg-gray-500 text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                Newton
              </button>
            </div>
          </div>

          {/* Time/Redshift Slider */}
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-gray-400">Redshift z = {redshift.toFixed(1)}</span>
              <span className="text-cyan-400">t = {cosmicTime.toFixed(1)} Gyr ago</span>
            </div>
            <input
              type="range"
              min="0"
              max="10"
              step="0.1"
              value={redshift}
              onChange={(e) => setRedshift(parseFloat(e.target.value))}
              className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-purple-500"
            />
            <div className="flex justify-between text-xs text-gray-500">
              <span>Now</span>
              <span>← Earlier Universe</span>
            </div>
          </div>

          {/* a₀ Display - only show for Zimmerman model */}
          {model === 'zimmerman' && (
            <div className="mt-4 p-3 bg-cyan-900/30 rounded-lg border border-cyan-500/30">
              <div className="text-sm text-cyan-300">Zimmerman Acceleration Scale</div>
              <div className="text-xl font-mono text-white">
                a₀ = {(a0 * 1e10).toFixed(2)} × 10⁻¹⁰ m/s²
              </div>
              <div className="text-xs text-gray-400 mt-1">
                {redshift > 0 ? `${E_z(redshift).toFixed(2)}× higher than today (E(z) factor)` : 'Local value (McGaugh+ 2016)'}
              </div>
              {redshift > 0 && (
                <div className="text-xs text-purple-300 mt-2 border-t border-cyan-500/20 pt-2">
                  <span className="text-gray-400">Galaxy size:</span> {(sizeScaling(redshift) * 100).toFixed(0)}% of local
                  <br />
                  <span className="text-gray-500">(MOND radius shrinks as a₀ increases)</span>
                </div>
              )}
            </div>
          )}

          {model === 'lcdm' && (
            <div className="mt-4 p-3 bg-red-900/30 rounded-lg border border-red-500/30">
              <div className="text-sm text-red-300">ΛCDM Dark Matter Halo</div>
              <div className="text-xs text-gray-400 mt-1">
                NFW profile with M_halo/M_bar ~ 5:1
                <br />
                Requires tuning per galaxy
              </div>
            </div>
          )}

          {model === 'newton' && (
            <div className="mt-4 p-3 bg-gray-800/50 rounded-lg border border-gray-600/50">
              <div className="text-sm text-gray-300">Newtonian Gravity</div>
              <div className="text-xs text-gray-400 mt-1">
                Baryons only, no dark matter
                <br />
                Predicts Keplerian decline (v ∝ r⁻¹/²)
              </div>
            </div>
          )}
        </motion.div>
      </div>

      {/* Info Panel */}
      <div className="absolute bottom-4 right-4 bg-black/90 backdrop-blur p-4 rounded-lg border border-purple-500/30 max-w-xs">
        <h3 className="text-sm font-bold text-purple-400 mb-2">Key Predictions</h3>
        <p className="text-xs text-gray-400 mb-2">
          At z {'>'} 0, Zimmerman predicts <strong>evolving dynamics</strong>:
        </p>
        <div className="text-xs font-mono text-cyan-400 bg-black/50 p-2 rounded space-y-1">
          <div>a₀(z) = a₀(0) × E(z)</div>
          <div className="text-purple-300">r_M(z) = r_M(0) / √E(z)</div>
          <div className="text-gray-500">E(z) = √(Ωm(1+z)³ + ΩΛ)</div>
        </div>
        <p className="text-xs text-gray-400 mt-2">
          <span className="text-yellow-400">•</span> Higher a₀ at high z = stronger MOND effect
          <br />
          <span className="text-purple-400">•</span> Smaller r_M at high z = more compact galaxies
        </p>
        <p className="text-xs text-gray-500 mt-2">
          Data: SPARC (Lelli, McGaugh, Schombert 2016)
        </p>
      </div>
    </div>
  )
}
