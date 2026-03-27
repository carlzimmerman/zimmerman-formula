'use client'

import { useRef, useMemo, useState, useCallback } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Stars, Html } from '@react-three/drei'
import * as THREE from 'three'
import { motion, AnimatePresence } from 'framer-motion'
import CollapsiblePanel from './CollapsiblePanel'
import { SPARC_GALAXIES, SPARCGalaxy, RotationPoint } from '../data/sparc_galaxies'

// Physics constants (CODATA 2018)
const Z = 2 * Math.sqrt(8 * Math.PI / 3)  // 5.788810
const G = 6.67430e-11  // m³/kg/s²
const c = 299792458    // m/s
const a0_local = 1.2e-10  // m/s² (McGaugh et al. 2016)
const kpc_to_m = 3.08567758e19
const M_sun = 1.98892e30  // kg

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

// Size scaling based on physics model
function sizeScalingZimmerman(z: number): number {
  return 1 / Math.sqrt(E_z(z))
}

function sizeScalingLCDM(z: number): number {
  return Math.pow(1 + z, -0.75)
}

function sizeScalingNewton(z: number): number {
  return 1
}

// Zimmerman/MOND rotation velocity using RAR formula
function zimmermanVelocity(r_kpc: number, M_solar: number, a0: number): number {
  const r_m = r_kpc * kpc_to_m
  const M_kg = M_solar * M_sun
  const g_bar = G * M_kg / (r_m * r_m)
  const x = Math.sqrt(g_bar / a0)
  const g_obs = g_bar / (1 - Math.exp(-x))
  return Math.sqrt(g_obs * r_m)
}

// Newtonian rotation velocity (no dark matter)
function newtonianVelocity(r_kpc: number, M_solar: number): number {
  const r_m = r_kpc * kpc_to_m
  const M_kg = M_solar * M_sun
  return Math.sqrt(G * M_kg / r_m)
}

// ΛCDM velocity with NFW dark matter halo
function lcdmVelocity(r_kpc: number, M_solar: number): number {
  const r_m = r_kpc * kpc_to_m
  const M_kg = M_solar * M_sun
  const v_bar_sq = G * M_kg / r_m
  const M_halo = M_kg * 5
  const rs = 20 * kpc_to_m
  const x = r_m / rs
  const f_nfw = Math.log(1 + x) - x / (1 + x)
  const M_dm_enclosed = M_halo * f_nfw / (Math.log(11) - 10/11)
  const v_dm_sq = G * M_dm_enclosed / r_m
  return Math.sqrt(v_bar_sq + v_dm_sq)
}

type PhysicsModel = 'zimmerman' | 'newton' | 'lcdm'

interface StarParticlesProps {
  count: number
  galaxy: SPARCGalaxy
  a0: number
  model: PhysicsModel
  redshift: number
}

// Generate spiral arm pattern
function spiralArmOffset(theta: number, armCount: number, winding: number = 0.3): number {
  if (armCount === 0) return 0
  const armPhase = (theta * armCount) % (2 * Math.PI)
  return Math.sin(armPhase) * winding
}

// Get star color based on position (bluer outer, yellower center)
function getStarColor(r_ratio: number, hasArms: boolean): THREE.Color {
  if (hasArms) {
    // Spiral galaxies: yellow core, bluer arms
    const hue = 0.08 + r_ratio * 0.12  // Yellow to blue-white
    const saturation = 0.3 - r_ratio * 0.2
    const lightness = 0.9 + r_ratio * 0.1
    return new THREE.Color().setHSL(hue, saturation, lightness)
  } else {
    // Irregular/LSB: more uniform blue-white
    return new THREE.Color().setHSL(0.6, 0.2, 0.95)
  }
}

function StarParticles({ count, galaxy, a0, model, redshift }: StarParticlesProps) {
  const meshRef = useRef<THREE.InstancedMesh>(null)
  const colorsRef = useRef<Float32Array | null>(null)
  const dummy = useMemo(() => new THREE.Object3D(), [])

  let sizeScale = 1
  switch (model) {
    case 'zimmerman':
      sizeScale = sizeScalingZimmerman(redshift)
      break
    case 'lcdm':
      sizeScale = sizeScalingLCDM(redshift)
      break
    case 'newton':
      sizeScale = sizeScalingNewton(redshift)
      break
  }
  const scaleFactor = (5 / galaxy.rLast) * sizeScale

  const hasArms = (galaxy.armCount || 0) > 0

  // Generate stars with realistic distribution
  const stars = useMemo(() => {
    const temp = []
    const armCount = galaxy.armCount || 0

    for (let i = 0; i < count; i++) {
      // Exponential disk distribution
      const u = Math.random()
      let r_kpc = -galaxy.rLast * 0.3 * Math.log(1 - u * 0.95)

      let theta = Math.random() * Math.PI * 2

      // Add spiral arm concentration
      if (armCount > 0) {
        const armPerturbation = spiralArmOffset(theta - r_kpc * 0.15, armCount, 0.25)
        r_kpc *= (1 + armPerturbation * 0.3)
      }

      const r_visual = Math.min(r_kpc * scaleFactor, 5.5)

      // Disk thickness (thinner at outer radii)
      const diskThickness = 0.12 * Math.exp(-r_kpc / (galaxy.rLast * 0.4))
      const height = (Math.random() - 0.5) * diskThickness

      // Bulge probability (more stars near center are in bulge)
      const bulgeProb = Math.exp(-r_kpc / (galaxy.rLast * 0.15))
      const isBulge = Math.random() < bulgeProb * 0.5

      temp.push({
        r_visual,
        r_kpc: Math.max(r_kpc, 0.3),
        theta,
        height: isBulge ? height * 3 : height,
        isBulge,
        r_ratio: r_kpc / galaxy.rLast,
      })
    }
    return temp
  }, [count, galaxy, scaleFactor, sizeScale])

  // Initialize colors
  useMemo(() => {
    if (meshRef.current) {
      const colors = new Float32Array(count * 3)
      stars.forEach((star, i) => {
        const color = star.isBulge
          ? new THREE.Color('#ffe4b5')  // Moccasin for bulge
          : getStarColor(star.r_ratio, hasArms)
        colors[i * 3] = color.r
        colors[i * 3 + 1] = color.g
        colors[i * 3 + 2] = color.b
      })
      colorsRef.current = colors
      meshRef.current.geometry.setAttribute(
        'color',
        new THREE.InstancedBufferAttribute(colors, 3)
      )
    }
  }, [stars, count, hasArms])

  useFrame((state) => {
    if (!meshRef.current) return

    const time = state.clock.getElapsedTime()

    stars.forEach((star, i) => {
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

      const r_m = star.r_kpc * kpc_to_m
      const omega = v / r_m
      const scaledOmega = omega * 5e14

      const currentTheta = star.theta + scaledOmega * time
      const x = star.r_visual * Math.cos(currentTheta)
      const z = star.r_visual * Math.sin(currentTheta)
      const y = star.height

      dummy.position.set(x, y, z)
      const size = star.isBulge ? 0.025 : (0.012 + 0.008 * Math.random())
      dummy.scale.setScalar(size)
      dummy.updateMatrix()
      meshRef.current!.setMatrixAt(i, dummy.matrix)
    })

    meshRef.current.instanceMatrix.needsUpdate = true
  })

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <sphereGeometry args={[1, 4, 4]} />
      <meshBasicMaterial vertexColors />
    </instancedMesh>
  )
}

// Dust lane particles for spiral galaxies
function DustLanes({ galaxy, scaleFactor }: { galaxy: SPARCGalaxy, scaleFactor: number }) {
  const meshRef = useRef<THREE.InstancedMesh>(null)
  const dummy = useMemo(() => new THREE.Object3D(), [])
  const count = 500

  const particles = useMemo(() => {
    if ((galaxy.armCount || 0) === 0) return []

    const temp = []
    for (let i = 0; i < count; i++) {
      const r = (0.3 + Math.random() * 0.5) * galaxy.rLast
      const theta = Math.random() * Math.PI * 2
      const armPhase = theta * (galaxy.armCount || 2)

      // Dust concentrates on inner edge of spiral arms
      if (Math.sin(armPhase + r * 0.1) > 0.3) {
        temp.push({
          r: r * scaleFactor,
          theta,
        })
      }
    }
    return temp
  }, [galaxy, scaleFactor, count])

  useFrame((state) => {
    if (!meshRef.current) return

    const time = state.clock.getElapsedTime() * 0.1
    particles.forEach((p, i) => {
      const x = p.r * Math.cos(p.theta + time)
      const z = p.r * Math.sin(p.theta + time)
      dummy.position.set(x, (Math.random() - 0.5) * 0.02, z)
      dummy.scale.setScalar(0.03)
      dummy.updateMatrix()
      meshRef.current!.setMatrixAt(i, dummy.matrix)
    })
    meshRef.current.instanceMatrix.needsUpdate = true
  })

  if (particles.length === 0) return null

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, particles.length]}>
      <sphereGeometry args={[1, 3, 3]} />
      <meshBasicMaterial color="#331100" transparent opacity={0.3} />
    </instancedMesh>
  )
}

interface RotationCurveDisplayProps {
  galaxy: SPARCGalaxy
  a0: number
  model: PhysicsModel
}

function RotationCurveDisplay({ galaxy, a0, model }: RotationCurveDisplayProps) {
  const points = useMemo(() => {
    const zimmermanPoints: [number, number][] = []
    const newtonPoints: [number, number][] = []
    const lcdmPoints: [number, number][] = []
    const observedPoints: [number, number, number][] = []  // r, v, err

    // Use real SPARC rotation curve data if available
    if (galaxy.rotationCurve && galaxy.rotationCurve.length > 0) {
      galaxy.rotationCurve.forEach(pt => {
        observedPoints.push([pt.r, pt.vObs, pt.errV])
      })
    }

    const rMax = galaxy.rLast
    const dr = rMax / 50

    for (let r = 1; r <= rMax; r += dr) {
      const vZim = zimmermanVelocity(r, galaxy.mass, a0) / 1000
      const vNewton = newtonianVelocity(r, galaxy.mass) / 1000
      const vLcdm = lcdmVelocity(r, galaxy.mass) / 1000

      zimmermanPoints.push([r, vZim])
      newtonPoints.push([r, vNewton])
      lcdmPoints.push([r, vLcdm])
    }

    return { zimmermanPoints, newtonPoints, lcdmPoints, observedPoints }
  }, [galaxy, a0])

  const maxV = Math.max(
    galaxy.vFlat * 1.4,
    ...points.zimmermanPoints.map(p => p[1]),
    ...(points.observedPoints.map(p => p[1] + p[2]) || [])
  )
  const maxR = galaxy.rLast

  return (
    <CollapsiblePanel
      title={`${galaxy.name} Rotation Curve`}
      className="absolute bottom-4 left-4 w-96 max-w-[calc(100vw-2rem)]"
      defaultOpen={true}
    >
      <p className="text-xs text-gray-500 mb-2">
        {galaxy.type} | M = {(galaxy.mass / 1e10).toFixed(1)} × 10¹⁰ M☉ | D = {galaxy.distance} Mpc
      </p>

      <svg viewBox="0 0 140 80" className="w-full h-44">
        {/* Grid */}
        {[0, 0.25, 0.5, 0.75, 1].map(frac => (
          <line key={frac} x1="20" y1={65 - frac * 50} x2="135" y2={65 - frac * 50} stroke="#333" strokeWidth="0.3" />
        ))}

        {/* Axes */}
        <line x1="20" y1="65" x2="135" y2="65" stroke="#555" strokeWidth="0.5" />
        <line x1="20" y1="65" x2="20" y2="12" stroke="#555" strokeWidth="0.5" />

        {/* Observed data points with error bars */}
        {points.observedPoints.map((p, i) => {
          const x = 20 + (p[0] / maxR) * 115
          const y = 65 - (p[1] / maxV) * 50
          const errY = (p[2] / maxV) * 50
          return (
            <g key={i}>
              <line x1={x} y1={y - errY} x2={x} y2={y + errY} stroke="#fbbf24" strokeWidth="0.8" opacity={0.7} />
              <circle cx={x} cy={y} r="1.5" fill="#fbbf24" />
            </g>
          )
        })}

        {/* Newtonian (gray dashed) */}
        <path
          d={points.newtonPoints.map((p, i) =>
            `${i === 0 ? 'M' : 'L'} ${20 + (p[0] / maxR) * 115} ${65 - (p[1] / maxV) * 50}`
          ).join(' ')}
          fill="none"
          stroke="#666"
          strokeWidth="1"
          strokeDasharray="3,2"
        />

        {/* ΛCDM (red) */}
        <path
          d={points.lcdmPoints.map((p, i) =>
            `${i === 0 ? 'M' : 'L'} ${20 + (p[0] / maxR) * 115} ${65 - (p[1] / maxV) * 50}`
          ).join(' ')}
          fill="none"
          stroke="#ef4444"
          strokeWidth="1.2"
          opacity={model === 'lcdm' ? 1 : 0.5}
        />

        {/* Zimmerman (cyan) */}
        <path
          d={points.zimmermanPoints.map((p, i) =>
            `${i === 0 ? 'M' : 'L'} ${20 + (p[0] / maxR) * 115} ${65 - (p[1] / maxV) * 50}`
          ).join(' ')}
          fill="none"
          stroke="#22d3ee"
          strokeWidth="1.5"
          opacity={model === 'zimmerman' ? 1 : 0.5}
        />

        {/* Labels */}
        <text x="75" y="78" fill="#888" fontSize="4" textAnchor="middle">Radius (kpc)</text>
        <text x="7" y="38" fill="#888" fontSize="4" textAnchor="middle" transform="rotate(-90, 7, 38)">V (km/s)</text>
        <text x="20" y="73" fill="#666" fontSize="3">0</text>
        <text x="133" y="73" fill="#666" fontSize="3">{maxR.toFixed(0)}</text>
        <text x="15" y="67" fill="#666" fontSize="3">0</text>
        <text x="12" y="17" fill="#666" fontSize="3">{Math.round(maxV)}</text>
      </svg>

      {/* Legend */}
      <div className="grid grid-cols-2 gap-1 text-xs mt-1">
        <span className="flex items-center gap-1">
          <span className="w-2 h-2 rounded-full bg-yellow-400"></span> SPARC Data
        </span>
        <span className="flex items-center gap-1">
          <span className="w-3 h-0.5 bg-cyan-400"></span> Zimmerman
        </span>
        <span className="flex items-center gap-1">
          <span className="w-3 h-0.5 bg-red-500"></span> ΛCDM
        </span>
        <span className="flex items-center gap-1">
          <span className="w-3 h-0.5 bg-gray-500 border-dashed"></span> Newton
        </span>
      </div>

      <p className="text-xs text-gray-500 mt-2">Data: SPARC (Lelli, McGaugh, Schombert 2016)</p>
    </CollapsiblePanel>
  )
}

function GalaxyCore({ color = '#fbbf24' }: { color?: string }) {
  const coreRef = useRef<THREE.Mesh>(null)

  useFrame((state) => {
    if (coreRef.current) {
      coreRef.current.rotation.y = state.clock.getElapsedTime() * 0.1
    }
  })

  return (
    <mesh ref={coreRef}>
      <sphereGeometry args={[0.25, 32, 32]} />
      <meshBasicMaterial color={color} transparent opacity={0.9} />
      <pointLight color={color} intensity={2} distance={8} />
    </mesh>
  )
}

export default function GalaxySimulation() {
  const [redshift, setRedshift] = useState(0)
  const [model, setModel] = useState<PhysicsModel>('zimmerman')
  const [galaxyIndex, setGalaxyIndex] = useState(0)

  const galaxy = SPARC_GALAXIES[galaxyIndex]
  const a0 = a0_at_z(redshift)

  const sizeScale = model === 'zimmerman' ? sizeScalingZimmerman(redshift) :
                    model === 'lcdm' ? sizeScalingLCDM(redshift) : 1
  const scaleFactor = (5 / galaxy.rLast) * sizeScale

  // Cosmic time from redshift
  const cosmicTime = redshift === 0 ? 13.8 : 13.8 / Math.pow(1 + redshift, 1.5)

  return (
    <div className="relative w-full h-screen bg-black">
      <Canvas camera={{ position: [0, 8, 12], fov: 45 }}>
        <ambientLight intensity={0.05} />
        <Stars radius={100} depth={50} count={5000} factor={4} fade speed={1} />

        <GalaxyCore color={galaxy.color || '#fbbf24'} />
        <StarParticles
          count={3500}
          galaxy={galaxy}
          a0={a0}
          model={model}
          redshift={redshift}
        />
        {(galaxy.armCount || 0) > 0 && (
          <DustLanes galaxy={galaxy} scaleFactor={scaleFactor} />
        )}

        <OrbitControls
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          autoRotate={false}
          maxDistance={30}
          minDistance={5}
        />
      </Canvas>

      <RotationCurveDisplay galaxy={galaxy} a0={a0} model={model} />

      {/* Controls */}
      <div className="absolute top-4 left-4 right-4 flex flex-col gap-4">
        <CollapsiblePanel
          title="Galaxy Rotation Simulation"
          className="max-w-md max-w-[calc(100vw-2rem)]"
          defaultOpen={true}
        >
          <p className="text-xs text-gray-400 mb-3">
            Real SPARC data: {SPARC_GALAXIES.length} galaxies with measured rotation curves
          </p>

          {/* Galaxy Selector */}
          <div className="mb-4">
            <label className="text-xs text-gray-400 mb-1 block">Select Galaxy (SPARC Database)</label>
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

          {/* Model-specific info panels */}
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
                  <span className="text-gray-400">Galaxy size:</span> {(sizeScalingZimmerman(redshift) * 100).toFixed(0)}% of local
                  <br />
                  <span className="text-green-400">★ PREDICTED:</span> <span className="text-gray-400">r_M ∝ 1/√E(z)</span>
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
              {redshift > 0 && (
                <div className="text-xs text-orange-300 mt-2 border-t border-red-500/20 pt-2">
                  <span className="text-gray-400">Galaxy size:</span> {(sizeScalingLCDM(redshift) * 100).toFixed(0)}% of local
                  <br />
                  <span className="text-gray-500">(Empirical fit: r ∝ (1+z)⁻⁰·⁷⁵)</span>
                </div>
              )}
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
              {redshift > 0 && (
                <div className="text-xs text-gray-400 mt-2 border-t border-gray-600/30 pt-2">
                  <span className="text-red-400 font-bold">No size evolution shown</span>
                  <br />
                  <span className="text-gray-500 mt-1 block">
                    Newton has no characteristic scale a₀ — no prediction for size evolution.
                  </span>
                </div>
              )}
            </div>
          )}
        </CollapsiblePanel>
      </div>

      {/* Size Evolution Panel */}
      <CollapsiblePanel
        title="Size Evolution Comparison"
        className="absolute bottom-4 right-4 max-w-sm max-w-[calc(100vw-2rem)]"
        defaultOpen={false}
      >
        <div className="space-y-2 text-xs">
          <div className="p-2 bg-cyan-900/20 rounded border-l-2 border-cyan-500">
            <span className="text-cyan-400 font-bold">Zimmerman:</span>
            <span className="text-gray-300 ml-1">r_M = r₀/√E(z)</span>
            <div className="text-green-400 text-[10px]">★ PREDICTED from theory</div>
          </div>

          <div className="p-2 bg-red-900/20 rounded border-l-2 border-red-500">
            <span className="text-red-400 font-bold">ΛCDM:</span>
            <span className="text-gray-300 ml-1">r ∝ (1+z)⁻⁰·⁷⁵</span>
            <div className="text-orange-400 text-[10px]">Empirical fit to simulations</div>
          </div>

          <div className="p-2 bg-gray-800/50 rounded border-l-2 border-gray-500">
            <span className="text-gray-400 font-bold">Newton:</span>
            <span className="text-gray-300 ml-1">No evolution</span>
            <div className="text-red-500 text-[10px]">NO PREDICTION POSSIBLE</div>
          </div>
        </div>

        <p className="text-xs text-gray-500 mt-3">
          The key: Zimmerman has a <strong>fundamental scale</strong> a₀ that
          defines galaxy structure.
        </p>
        <p className="text-xs text-gray-600 mt-1">
          Data: SPARC (Lelli+ 2016) | {SPARC_GALAXIES.length} galaxies
        </p>
      </CollapsiblePanel>
    </div>
  )
}
