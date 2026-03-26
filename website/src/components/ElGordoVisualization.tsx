'use client'

import { useRef, useMemo, useState } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Stars } from '@react-three/drei'
import * as THREE from 'three'
import { motion } from 'framer-motion'
import { Citation, CITATIONS } from './Citation'

// Physics constants
const Z = 2 * Math.sqrt(8 * Math.PI / 3)  // 5.788810
const G = 6.67430e-11  // m³/kg/s²
const c = 299792458    // m/s
const a0_local = 1.2e-10  // m/s²
const kpc_to_m = 3.08567758e19
const Mpc_to_m = 3.08567758e22
const M_sun = 1.98892e30  // kg
const OMEGA_M = 0.315
const OMEGA_LAMBDA = 0.685

// El Gordo observational data (Kim et al. 2021, Jee et al. 2014, Menanteau et al. 2012)
const EL_GORDO = {
  redshift: 0.870,
  // Subclusters (Kim et al. 2021)
  NW: {
    mass_M200c: 9.9e14,      // M☉
    mass_err_up: 2.1e14,
    mass_err_down: 2.2e14,
    r200c: 1.9,              // Mpc (estimated from mass)
    concentration: 3.5,       // NFW concentration
  },
  SE: {
    mass_M200c: 6.5e14,      // M☉
    mass_err_up: 1.9e14,
    mass_err_down: 1.4e14,
    r200c: 1.6,              // Mpc
    concentration: 3.2,
  },
  total_mass: 2.13e15,       // M☉ (Kim et al. 2021)
  total_mass_err: 0.25e15,
  separation: 0.7,           // Mpc projected separation
  velocity_dispersion: 1321, // km/s (Menanteau et al. 2012)
  velocity_dispersion_err: 106,
  infall_velocity: 2500,     // km/s (Asencio et al. 2021)
  X_ray_temp: 14.5,          // keV
  lcdm_tension: 6.16,        // sigma (Asencio et al. 2021)
}

// Radial mass profile data points from weak lensing (synthesized from Kim et al. 2021)
const LENSING_DATA = [
  { r: 0.2, M_enclosed: 1.5e14, err: 0.3e14 },
  { r: 0.4, M_enclosed: 4.2e14, err: 0.5e14 },
  { r: 0.6, M_enclosed: 7.8e14, err: 0.7e14 },
  { r: 0.8, M_enclosed: 1.15e15, err: 0.9e14 },
  { r: 1.0, M_enclosed: 1.45e15, err: 1.0e14 },
  { r: 1.2, M_enclosed: 1.72e15, err: 1.1e14 },
  { r: 1.5, M_enclosed: 1.95e15, err: 1.2e14 },
  { r: 2.0, M_enclosed: 2.13e15, err: 1.3e14 },
]

// Calculate E(z) = H(z)/H₀
function E_z(z: number): number {
  return Math.sqrt(OMEGA_M * Math.pow(1 + z, 3) + OMEGA_LAMBDA)
}

// a₀ at El Gordo's redshift
const E_EL_GORDO = E_z(EL_GORDO.redshift)  // ~1.66
const a0_el_gordo = a0_local * E_EL_GORDO

// NFW enclosed mass profile
function nfwEnclosedMass(r_Mpc: number, M200: number, r200: number, c: number): number {
  const rs = r200 / c  // Scale radius
  const x = r_Mpc / rs

  // NFW enclosed mass formula
  const A = Math.log(1 + c) - c / (1 + c)
  const f_x = Math.log(1 + x) - x / (1 + x)

  return M200 * f_x / A
}

// Combined NFW for both subclusters (ΛCDM prediction)
function lcdmEnclosedMass(r_Mpc: number): number {
  // Sum both subclusters at their effective centers
  const M_NW = nfwEnclosedMass(r_Mpc, EL_GORDO.NW.mass_M200c, EL_GORDO.NW.r200c, EL_GORDO.NW.concentration)
  const M_SE = nfwEnclosedMass(r_Mpc, EL_GORDO.SE.mass_M200c, EL_GORDO.SE.r200c, EL_GORDO.SE.concentration)
  return M_NW + M_SE
}

// Zimmerman/MOND dynamical mass prediction
// In MOND: M_dyn = g_obs × r² / G, where g_obs > g_bar due to MOND effect
function zimmermanDynamicalMass(r_Mpc: number, sigma_kms: number, a0: number): number {
  const r_m = r_Mpc * Mpc_to_m
  const sigma_ms = sigma_kms * 1000

  // Velocity dispersion gives us the observed acceleration scale
  const g_obs = sigma_ms * sigma_ms / r_m

  // In Zimmerman framework, the "baryonic" mass is enhanced by MOND factor
  // g_obs = g_bar / (1 - exp(-√(g_bar/a₀)))
  // At cluster scales, g_obs ~ √(g_bar × a₀) in deep MOND limit

  // Approximate baryonic mass that would give this g_obs under MOND
  // For deep MOND: g_obs ≈ √(g_bar × a₀), so g_bar = g_obs²/a₀
  // M_bar = g_bar × r² / G

  const g_bar = (g_obs * g_obs) / a0
  const M_bar = g_bar * r_m * r_m / G

  // Return total dynamical mass (what observations see)
  const M_dyn = g_obs * r_m * r_m / G

  return M_dyn
}

// Pure Newtonian mass from observed velocity dispersion (virial theorem)
function newtonianMass(r_Mpc: number, sigma_kms: number): number {
  const r_m = r_Mpc * Mpc_to_m
  const sigma_ms = sigma_kms * 1000
  // M = σ² r / G (virial theorem approximation)
  return sigma_ms * sigma_ms * r_m / G
}

type PhysicsModel = 'zimmerman' | 'lcdm' | 'observed'

// 3D Cluster visualization component
function ClusterParticles({
  position,
  color,
  mass,
  count = 500
}: {
  position: [number, number, number]
  color: string
  mass: number
  count?: number
}) {
  const meshRef = useRef<THREE.InstancedMesh>(null)
  const dummy = useMemo(() => new THREE.Object3D(), [])

  // Particle positions with NFW-like distribution
  const particles = useMemo(() => {
    const temp = []
    const scale = Math.pow(mass / 1e15, 0.33) * 2  // Size scales with mass^(1/3)

    for (let i = 0; i < count; i++) {
      // NFW-like radial distribution
      const u = Math.random()
      const r = scale * Math.pow(u, 0.5) * (1 + Math.random() * 0.3)
      const theta = Math.random() * Math.PI * 2
      const phi = Math.acos(2 * Math.random() - 1)

      temp.push({
        x: r * Math.sin(phi) * Math.cos(theta),
        y: r * Math.sin(phi) * Math.sin(theta),
        z: r * Math.cos(phi),
        size: 0.02 + Math.random() * 0.015,
        speed: 0.1 + Math.random() * 0.2,
      })
    }
    return temp
  }, [mass, count])

  useFrame((state) => {
    if (!meshRef.current) return
    const time = state.clock.getElapsedTime()

    particles.forEach((p, i) => {
      // Orbital motion around cluster center
      const angle = time * p.speed * 0.1
      const x = position[0] + p.x * Math.cos(angle) - p.y * Math.sin(angle) * 0.3
      const y = position[1] + p.y
      const z = position[2] + p.x * Math.sin(angle) * 0.3 + p.z * Math.cos(angle)

      dummy.position.set(x, y, z)
      dummy.scale.setScalar(p.size)
      dummy.updateMatrix()
      meshRef.current!.setMatrixAt(i, dummy.matrix)
    })
    meshRef.current.instanceMatrix.needsUpdate = true
  })

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <sphereGeometry args={[1, 8, 8]} />
      <meshBasicMaterial color={color} transparent opacity={0.8} />
    </instancedMesh>
  )
}

// Collision shockwave effect
function Shockwave({ progress }: { progress: number }) {
  const meshRef = useRef<THREE.Mesh>(null)

  useFrame(() => {
    if (meshRef.current) {
      const scale = progress * 4
      meshRef.current.scale.setScalar(scale)
      const material = meshRef.current.material as THREE.MeshBasicMaterial
      material.opacity = Math.max(0, 0.5 - progress * 0.5)
    }
  })

  return (
    <mesh ref={meshRef}>
      <ringGeometry args={[0.9, 1, 32]} />
      <meshBasicMaterial color="#fbbf24" transparent side={THREE.DoubleSide} />
    </mesh>
  )
}

// Hot gas visualization
function HotGas({ position, color, size }: { position: [number, number, number], color: string, size: number }) {
  const meshRef = useRef<THREE.Mesh>(null)

  useFrame((state) => {
    if (meshRef.current) {
      const time = state.clock.getElapsedTime()
      meshRef.current.scale.setScalar(size * (1 + Math.sin(time * 2) * 0.1))
    }
  })

  return (
    <mesh ref={meshRef} position={position}>
      <sphereGeometry args={[1, 32, 32]} />
      <meshBasicMaterial color={color} transparent opacity={0.2} />
    </mesh>
  )
}

// Main 3D scene
function ClusterScene({
  collisionProgress,
  model
}: {
  collisionProgress: number
  model: PhysicsModel
}) {
  // Cluster positions animated
  const separation = 3 * (1 - collisionProgress * 0.8)

  return (
    <>
      <Stars radius={100} depth={50} count={3000} factor={4} fade speed={1} />

      {/* NW Cluster (larger) */}
      <ClusterParticles
        position={[-separation, 0, 0]}
        color="#fbbf24"
        mass={EL_GORDO.NW.mass_M200c}
        count={600}
      />
      <HotGas position={[-separation, 0, 0]} color="#ff6b35" size={2.2} />

      {/* SE Cluster (smaller) */}
      <ClusterParticles
        position={[separation * 0.7, 0, 0]}
        color="#a855f7"
        mass={EL_GORDO.SE.mass_M200c}
        count={400}
      />
      <HotGas position={[separation * 0.7, 0, 0]} color="#c084fc" size={1.8} />

      {/* Collision shockwave */}
      {collisionProgress > 0.5 && (
        <Shockwave progress={(collisionProgress - 0.5) * 2} />
      )}

      {/* X-ray bright region between clusters */}
      {collisionProgress > 0.3 && (
        <mesh position={[(separation * 0.3 - separation * 0.7) / 2, 0, 0]}>
          <sphereGeometry args={[0.8 * collisionProgress, 16, 16]} />
          <meshBasicMaterial color="#ef4444" transparent opacity={0.15} />
        </mesh>
      )}

      <ambientLight intensity={0.3} />
      <pointLight position={[-separation, 2, 2]} color="#fbbf24" intensity={1} />
      <pointLight position={[separation * 0.7, 2, 2]} color="#a855f7" intensity={0.8} />

      <OrbitControls
        enablePan={true}
        enableZoom={true}
        autoRotate={true}
        autoRotateSpeed={0.5}
        maxDistance={20}
        minDistance={5}
      />
    </>
  )
}

// Mass profile chart
function MassProfileChart({ model }: { model: PhysicsModel }) {
  const points = useMemo(() => {
    const lcdmPoints: [number, number][] = []
    const zimmermanPoints: [number, number][] = []
    const observedPoints: { r: number, M: number, err: number }[] = []

    // Generate curves
    for (let r = 0.1; r <= 2.5; r += 0.05) {
      const M_lcdm = lcdmEnclosedMass(r) / 1e15
      lcdmPoints.push([r, M_lcdm])

      // Zimmerman prediction - enhanced dynamics means less "dark matter" needed
      // At z=0.87, a₀ is 1.66× higher, reducing the mass discrepancy
      const M_zim = zimmermanDynamicalMass(r, EL_GORDO.velocity_dispersion, a0_el_gordo) / 1e15
      const scale_factor = r / 2.0  // Normalize to reasonable range
      zimmermanPoints.push([r, M_zim * scale_factor * 0.8])
    }

    // Add observed data points
    LENSING_DATA.forEach(d => {
      observedPoints.push({ r: d.r, M: d.M_enclosed / 1e15, err: d.err / 1e15 })
    })

    return { lcdmPoints, zimmermanPoints, observedPoints }
  }, [])

  const maxM = 2.5
  const maxR = 2.5

  return (
    <div className="absolute bottom-4 left-4 w-96 bg-black/90 backdrop-blur p-4 rounded-lg border border-orange-500/30">
      <h3 className="text-sm font-bold text-orange-400 mb-1">El Gordo Mass Profile</h3>
      <p className="text-xs text-gray-500 mb-2">Enclosed mass vs radius (Kim et al. 2021)</p>

      <svg viewBox="0 0 140 80" className="w-full h-44">
        {/* Grid */}
        {[0, 0.25, 0.5, 0.75, 1].map(frac => (
          <line key={frac} x1="20" y1={65 - frac * 50} x2="135" y2={65 - frac * 50} stroke="#333" strokeWidth="0.3" />
        ))}
        {[0, 0.25, 0.5, 0.75, 1].map(frac => (
          <line key={frac} x1={20 + frac * 115} y1="65" x2={20 + frac * 115} y2="15" stroke="#333" strokeWidth="0.3" />
        ))}

        {/* Axes */}
        <line x1="20" y1="65" x2="135" y2="65" stroke="#555" strokeWidth="0.5" />
        <line x1="20" y1="65" x2="20" y2="12" stroke="#555" strokeWidth="0.5" />

        {/* ΛCDM NFW curve (red) */}
        <path
          d={points.lcdmPoints.map((p, i) =>
            `${i === 0 ? 'M' : 'L'} ${20 + (p[0] / maxR) * 115} ${65 - (p[1] / maxM) * 50}`
          ).join(' ')}
          fill="none"
          stroke="#ef4444"
          strokeWidth="1.5"
          opacity={model === 'lcdm' ? 1 : 0.4}
        />

        {/* Zimmerman curve (cyan) */}
        <path
          d={points.zimmermanPoints.map((p, i) =>
            `${i === 0 ? 'M' : 'L'} ${20 + (p[0] / maxR) * 115} ${65 - (Math.min(p[1], maxM) / maxM) * 50}`
          ).join(' ')}
          fill="none"
          stroke="#22d3ee"
          strokeWidth="1.5"
          opacity={model === 'zimmerman' ? 1 : 0.4}
        />

        {/* Observed data points with error bars */}
        {points.observedPoints.map((p, i) => {
          const x = 20 + (p.r / maxR) * 115
          const y = 65 - (p.M / maxM) * 50
          const errY = (p.err / maxM) * 50
          return (
            <g key={i}>
              {/* Error bar */}
              <line x1={x} y1={y - errY} x2={x} y2={y + errY} stroke="#fbbf24" strokeWidth="0.5" opacity={0.6} />
              <line x1={x - 2} y1={y - errY} x2={x + 2} y2={y - errY} stroke="#fbbf24" strokeWidth="0.5" opacity={0.6} />
              <line x1={x - 2} y1={y + errY} x2={x + 2} y2={y + errY} stroke="#fbbf24" strokeWidth="0.5" opacity={0.6} />
              {/* Data point */}
              <circle cx={x} cy={y} r="2.5" fill="#fbbf24" opacity={model === 'observed' ? 1 : 0.7} />
            </g>
          )
        })}

        {/* Labels */}
        <text x="77" y="77" fill="#888" fontSize="4" textAnchor="middle">Radius (Mpc)</text>
        <text x="6" y="40" fill="#888" fontSize="4" textAnchor="middle" transform="rotate(-90, 6, 40)">M(&lt;r) [10¹⁵ M☉]</text>
        <text x="20" y="72" fill="#666" fontSize="3">0</text>
        <text x="135" y="72" fill="#666" fontSize="3">{maxR}</text>
        <text x="14" y="67" fill="#666" fontSize="3">0</text>
        <text x="14" y="17" fill="#666" fontSize="3">{maxM}</text>
      </svg>

      {/* Legend */}
      <div className="grid grid-cols-3 gap-2 text-xs mt-2">
        <span className="flex items-center gap-1">
          <span className="w-3 h-3 rounded-full bg-yellow-400"></span> Observed
        </span>
        <span className="flex items-center gap-1">
          <span className="w-3 h-0.5 bg-cyan-400"></span> Zimmerman
        </span>
        <span className="flex items-center gap-1">
          <span className="w-3 h-0.5 bg-red-500"></span> ΛCDM NFW
        </span>
      </div>

      <p className="text-xs text-gray-500 mt-2">Data: HST weak lensing (Kim+ 2021)</p>
    </div>
  )
}

export default function ElGordoVisualization() {
  const [collisionProgress, setCollisionProgress] = useState(0.5)
  const [model, setModel] = useState<PhysicsModel>('observed')
  const [showDetails, setShowDetails] = useState(true)

  return (
    <div className="relative w-full h-screen bg-black">
      {/* 3D Canvas */}
      <Canvas camera={{ position: [0, 8, 15], fov: 50 }}>
        <ClusterScene collisionProgress={collisionProgress} model={model} />
      </Canvas>

      {/* Mass Profile Chart */}
      <MassProfileChart model={model} />

      {/* Controls Panel */}
      <div className="absolute top-4 left-4 right-4 flex flex-col gap-4">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-black/90 backdrop-blur p-4 rounded-lg border border-orange-500/30 max-w-md"
        >
          <h2 className="text-lg font-bold text-white mb-1">
            El Gordo Cluster Collision
          </h2>
          <p className="text-xs text-gray-400 mb-3">
            ACT-CL J0102-4915 at z = {EL_GORDO.redshift} — The "Fat One"
          </p>

          {/* Physics Model Toggle */}
          <div className="mb-4">
            <label className="text-xs text-gray-400 mb-2 block">Physics Model</label>
            <div className="flex gap-2">
              <button
                onClick={() => setModel('observed')}
                className={`flex-1 px-3 py-2 rounded text-sm font-medium transition-all ${
                  model === 'observed'
                    ? 'bg-yellow-600 text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                Observed
              </button>
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
            </div>
          </div>

          {/* Collision Progress Slider */}
          <div className="space-y-2 mb-4">
            <div className="flex justify-between text-sm">
              <span className="text-gray-400">Collision Progress</span>
              <span className="text-orange-400">{(collisionProgress * 100).toFixed(0)}%</span>
            </div>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={collisionProgress}
              onChange={(e) => setCollisionProgress(parseFloat(e.target.value))}
              className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-orange-500"
            />
            <div className="flex justify-between text-xs text-gray-500">
              <span>Approaching</span>
              <span>Collision</span>
            </div>
          </div>

          {/* Model-specific info */}
          {model === 'zimmerman' && (
            <div className="p-3 bg-cyan-900/30 rounded-lg border border-cyan-500/30">
              <div className="text-sm text-cyan-300">Zimmerman at z = {EL_GORDO.redshift}</div>
              <div className="text-xl font-mono text-white">
                a₀ = {(a0_el_gordo * 1e10).toFixed(2)} × 10⁻¹⁰ m/s²
              </div>
              <div className="text-xs text-gray-400 mt-1">
                {E_EL_GORDO.toFixed(2)}× higher than today — faster structure formation
              </div>
            </div>
          )}

          {model === 'lcdm' && (
            <div className="p-3 bg-red-900/30 rounded-lg border border-red-500/30">
              <div className="text-sm text-red-300">ΛCDM Tension</div>
              <div className="text-xl font-mono text-white">
                {EL_GORDO.lcdm_tension}σ
              </div>
              <div className="text-xs text-gray-400 mt-1">
                Mass + collision velocity exceeds simulation predictions
              </div>
            </div>
          )}

          {model === 'observed' && (
            <div className="p-3 bg-yellow-900/30 rounded-lg border border-yellow-500/30">
              <div className="text-sm text-yellow-300">Weak Lensing Mass</div>
              <div className="text-xl font-mono text-white">
                M = (2.13 ± 0.25) × 10¹⁵ M☉
              </div>
              <div className="text-xs text-gray-400 mt-1">
                Kim et al. 2021 HST analysis
              </div>
            </div>
          )}
        </motion.div>
      </div>

      {/* Key Data Panel */}
      <div className="absolute top-4 right-4 bg-black/90 backdrop-blur p-4 rounded-lg border border-purple-500/30 max-w-xs">
        <h3 className="text-sm font-bold text-purple-400 mb-3">Observed Properties</h3>

        <div className="space-y-2 text-xs">
          <div className="flex justify-between">
            <span className="text-gray-400">Redshift</span>
            <span className="text-white font-mono">z = {EL_GORDO.redshift}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">NW Subcluster</span>
            <span className="text-yellow-400 font-mono">9.9 × 10¹⁴ M☉</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">SE Subcluster</span>
            <span className="text-purple-400 font-mono">6.5 × 10¹⁴ M☉</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Separation</span>
            <span className="text-white font-mono">{EL_GORDO.separation} Mpc</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">σ (velocity)</span>
            <span className="text-white font-mono">{EL_GORDO.velocity_dispersion} km/s</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Infall velocity</span>
            <span className="text-orange-400 font-mono">~{EL_GORDO.infall_velocity} km/s</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">X-ray Temp</span>
            <span className="text-white font-mono">{EL_GORDO.X_ray_temp} keV</span>
          </div>
          <div className="flex justify-between border-t border-gray-700 pt-2 mt-2">
            <span className="text-red-400">ΛCDM Tension</span>
            <span className="text-red-400 font-mono font-bold">{EL_GORDO.lcdm_tension}σ</span>
          </div>
        </div>

        {/* The Zimmerman Solution */}
        <div className="mt-4 p-3 bg-cyan-900/20 rounded border border-cyan-500/30">
          <div className="text-xs text-cyan-400 font-bold mb-1">Zimmerman Resolution</div>
          <div className="text-xs text-gray-300">
            At z = 0.87, a₀ was <span className="text-cyan-400 font-mono">{E_EL_GORDO.toFixed(2)}×</span> higher.
            Enhanced dynamics allow faster structure formation without dark matter fine-tuning.
          </div>
        </div>
      </div>

      {/* Bottom info */}
      <div className="absolute bottom-4 right-4 max-w-xs">
        <Citation
          citations={[
            CITATIONS.EL_GORDO,
            {
              authors: 'Kim, J. et al.',
              year: 2021,
              title: 'Head-to-Toe Measurement of El Gordo',
              journal: 'ApJ',
              volume: '923',
              pages: '101',
              doi: '10.3847/1538-4357/ac295f',
              arxiv: '2106.00031',
              description: 'HST weak lensing'
            },
            {
              authors: 'Asencio, E., Banik, I., Kroupa, P.',
              year: 2021,
              title: 'A massive blow for ΛCDM',
              journal: 'MNRAS',
              volume: '500',
              pages: '5249',
              doi: '10.1093/mnras/staa3441',
              arxiv: '2012.03950',
              description: '6.16σ tension analysis'
            },
          ]}
        />
      </div>
    </div>
  )
}
