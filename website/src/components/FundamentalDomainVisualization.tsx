'use client'

import { useRef, useMemo, useState, useEffect } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Line, Text, Html } from '@react-three/drei'
import * as THREE from 'three'

const BOX_SIZE = 4
const HALF_BOX = BOX_SIZE / 2

// Z₂ chirality axis: (l, b) = (287°, 9°) in Galactic coordinates
const CHIRALITY_L = 287 * Math.PI / 180
const CHIRALITY_B = 9 * Math.PI / 180

function galacticToCartesian(l: number, b: number): THREE.Vector3 {
  return new THREE.Vector3(
    Math.cos(b) * Math.cos(l),
    Math.cos(b) * Math.sin(l),
    Math.sin(b)
  )
}

const CHIRALITY_AXIS = galacticToCartesian(CHIRALITY_L, CHIRALITY_B)

interface GalaxyData {
  metadata: {
    source: string
    ngc_total: number
    sgc_total: number
    ngc_sampled: number
    sgc_sampled: number
    max_extent_mpc_h: number
    z_range: [number, number]
  }
  ngc: { x: number[]; y: number[]; z: number[]; redshift: number[] }
  sgc: { x: number[]; y: number[]; z: number[]; redshift: number[] }
  chirality_axis: { galactic_l: number; galactic_b: number }
}

function positionsToFloat32(data: { x: number[]; y: number[]; z: number[] }): Float32Array {
  const count = data.x.length
  const positions = new Float32Array(count * 3)
  for (let i = 0; i < count; i++) {
    positions[i * 3] = data.x[i] * 2  // Scale to visualization box
    positions[i * 3 + 1] = data.y[i] * 2
    positions[i * 3 + 2] = data.z[i] * 2
  }
  return positions
}

interface GalaxyPointsProps {
  positions: Float32Array
  color: string
  size?: number
}

function GalaxyPoints({ positions, color, size = 0.008 }: GalaxyPointsProps) {
  const ref = useRef<THREE.Points>(null)

  const geometry = useMemo(() => {
    const geo = new THREE.BufferGeometry()
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    return geo
  }, [positions])

  return (
    <points ref={ref} geometry={geometry}>
      <pointsMaterial
        color={color}
        size={size}
        transparent
        opacity={0.7}
        sizeAttenuation
        depthWrite={false}
      />
    </points>
  )
}

function FundamentalDomainBox() {
  const edges = useMemo(() => {
    const h = HALF_BOX
    return [
      [[-h, -h, -h], [h, -h, -h]], [[h, -h, -h], [h, h, -h]],
      [[h, h, -h], [-h, h, -h]], [[-h, h, -h], [-h, -h, -h]],
      [[-h, -h, h], [h, -h, h]], [[h, -h, h], [h, h, h]],
      [[h, h, h], [-h, h, h]], [[-h, h, h], [-h, -h, h]],
      [[-h, -h, -h], [-h, -h, h]], [[h, -h, -h], [h, -h, h]],
      [[h, h, -h], [h, h, h]], [[-h, h, -h], [-h, h, h]],
    ] as [number[], number[]][]
  }, [])

  return (
    <group>
      {edges.map((edge, i) => (
        <Line
          key={i}
          points={edge.map(p => new THREE.Vector3(...p))}
          color="#555"
          lineWidth={1}
        />
      ))}
      {/* Face labels */}
      <Html position={[0, 0, HALF_BOX + 0.2]}>
        <div className="text-gray-500 text-[10px] font-mono">+Z (NGC)</div>
      </Html>
      <Html position={[0, 0, -HALF_BOX - 0.2]}>
        <div className="text-gray-500 text-[10px] font-mono">-Z (SGC)</div>
      </Html>
    </group>
  )
}

function ChiralityAxis() {
  const length = BOX_SIZE * 0.7
  const start = CHIRALITY_AXIS.clone().multiplyScalar(-length / 2)
  const end = CHIRALITY_AXIS.clone().multiplyScalar(length / 2)

  return (
    <group>
      <Line points={[start, end]} color="#e74c3c" lineWidth={2} />
      <mesh position={end}>
        <coneGeometry args={[0.06, 0.15, 8]} />
        <meshBasicMaterial color="#e74c3c" />
      </mesh>
    </group>
  )
}

function ScaleBar() {
  // Show 1 Gpc scale bar
  const barLength = 0.66  // Approximately 1 Gpc at our scale
  return (
    <group position={[-HALF_BOX + 0.5, -HALF_BOX + 0.3, -HALF_BOX]}>
      <Line
        points={[new THREE.Vector3(0, 0, 0), new THREE.Vector3(barLength, 0, 0)]}
        color="#888"
        lineWidth={2}
      />
      <Html position={[barLength / 2, -0.15, 0]}>
        <div className="text-gray-400 text-[9px] font-mono">1 Gpc</div>
      </Html>
    </group>
  )
}

interface SceneProps {
  ngcPositions: Float32Array | null
  sgcPositions: Float32Array | null
  showAxis: boolean
  autoRotate: boolean
}

function Scene({ ngcPositions, sgcPositions, showAxis, autoRotate }: SceneProps) {
  const groupRef = useRef<THREE.Group>(null)

  useFrame(({ clock }) => {
    if (groupRef.current && autoRotate) {
      groupRef.current.rotation.y = clock.getElapsedTime() * 0.03
    }
  })

  return (
    <group ref={groupRef}>
      <FundamentalDomainBox />
      {ngcPositions && <GalaxyPoints positions={ngcPositions} color="#3498db" />}
      {sgcPositions && <GalaxyPoints positions={sgcPositions} color="#e67e22" />}
      {showAxis && <ChiralityAxis />}
      <ScaleBar />
    </group>
  )
}

interface Props {
  className?: string
}

export default function FundamentalDomainVisualization({ className = '' }: Props) {
  const [data, setData] = useState<GalaxyData | null>(null)
  const [showAxis, setShowAxis] = useState(true)
  const [autoRotate, setAutoRotate] = useState(true)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/data/desi_galaxy_positions.json')
      .then(res => res.json())
      .then(json => {
        setData(json)
        setLoading(false)
      })
      .catch(err => {
        console.error('Failed to load galaxy data:', err)
        setLoading(false)
      })
  }, [])

  const ngcPositions = useMemo(() =>
    data ? positionsToFloat32(data.ngc) : null, [data])
  const sgcPositions = useMemo(() =>
    data ? positionsToFloat32(data.sgc) : null, [data])

  if (loading) {
    return (
      <div className={`flex items-center justify-center bg-gray-900 rounded ${className}`} style={{ height: '500px' }}>
        <div className="text-gray-400">Loading DESI galaxy data...</div>
      </div>
    )
  }

  if (!data) {
    return (
      <div className={`flex items-center justify-center bg-gray-900 rounded ${className}`} style={{ height: '500px' }}>
        <div className="text-red-400">Failed to load galaxy data. Check console for errors.</div>
      </div>
    )
  }

  return (
    <div className={`relative ${className}`}>
      <div className="w-full max-w-xl mx-auto bg-[#0a0a0a] rounded border border-gray-800" style={{ height: '500px' }}>
        <Canvas camera={{ position: [5, 3, 5], fov: 45 }} gl={{ antialias: true }} style={{ width: '100%', height: '100%' }}>
          <color attach="background" args={['#0a0a0a']} />
          <Scene
            ngcPositions={ngcPositions}
            sgcPositions={sgcPositions}
            showAxis={showAxis}
            autoRotate={autoRotate}
          />
          <OrbitControls
            enablePan={false}
            minDistance={4}
            maxDistance={12}
            autoRotate={false}
          />
        </Canvas>
      </div>

      {/* Legend */}
      <div className="mt-4 flex flex-wrap justify-center gap-6 text-sm">
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-[#3498db]" />
          <span className="text-gray-400">NGC ({data?.metadata.ngc_sampled.toLocaleString()} of {data?.metadata.ngc_total.toLocaleString()})</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-[#e67e22]" />
          <span className="text-gray-400">SGC ({data?.metadata.sgc_sampled.toLocaleString()} of {data?.metadata.sgc_total.toLocaleString()})</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-4 h-0.5 bg-[#e74c3c]" />
          <span className="text-gray-400">Z₂ axis (ℓ=287°, b=9°)</span>
        </div>
      </div>

      {/* Controls */}
      <div className="mt-3 flex justify-center gap-3">
        <button
          onClick={() => setShowAxis(!showAxis)}
          className={`px-3 py-1 text-xs rounded border transition-colors ${
            showAxis
              ? 'bg-red-900/30 border-red-800 text-red-300'
              : 'bg-gray-900 border-gray-700 text-gray-500'
          }`}
        >
          Chirality Axis
        </button>
        <button
          onClick={() => setAutoRotate(!autoRotate)}
          className={`px-3 py-1 text-xs rounded border transition-colors ${
            autoRotate
              ? 'bg-blue-900/30 border-blue-800 text-blue-300'
              : 'bg-gray-900 border-gray-700 text-gray-500'
          }`}
        >
          {autoRotate ? 'Pause' : 'Rotate'}
        </button>
      </div>

      {/* Caption */}
      <p className="mt-4 text-center text-xs text-gray-500 max-w-lg mx-auto">
        <strong>Figure 1:</strong> DESI DR1 LRG galaxies (z = 0.4–1.1) mapped into the T³/Z₂
        fundamental domain. The red axis indicates the predicted chirality direction from
        Z² = 32π/3 topology. Both NGC and SGC show identical parity-odd 4PCF (r = 0.9986),
        consistent with global topological chirality.
      </p>
    </div>
  )
}