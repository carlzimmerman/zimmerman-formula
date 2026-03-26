'use client'

import { useRef, useState, useMemo } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Text, Html, Line } from '@react-three/drei'
import * as THREE from 'three'
import { motion, AnimatePresence } from 'framer-motion'

const Z = 2 * Math.sqrt(8 * Math.PI / 3)  // 5.788810
const Z_SQUARED = 32 * Math.PI / 3  // 33.51

// Cube vertices
const cubeVertices = [
  [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
  [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1],
] as const

// Cube edges
const cubeEdges = [
  [0, 1], [1, 2], [2, 3], [3, 0],  // bottom
  [4, 5], [5, 6], [6, 7], [7, 4],  // top
  [0, 4], [1, 5], [2, 6], [3, 7],  // verticals
]

function RotatingCube({ opacity = 1, scale = 1 }: { opacity?: number, scale?: number }) {
  const groupRef = useRef<THREE.Group>(null)

  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = state.clock.getElapsedTime() * 0.3
      groupRef.current.rotation.x = Math.sin(state.clock.getElapsedTime() * 0.2) * 0.1
    }
  })

  return (
    <group ref={groupRef} scale={scale}>
      {/* Cube edges */}
      {cubeEdges.map((edge, i) => {
        const start = cubeVertices[edge[0]]
        const end = cubeVertices[edge[1]]
        return (
          <Line
            key={i}
            points={[start, end]}
            color="#22d3ee"
            lineWidth={2}
            transparent
            opacity={opacity}
          />
        )
      })}

      {/* Cube vertices - highlight the 8 */}
      {cubeVertices.map((pos, i) => (
        <mesh key={i} position={pos}>
          <sphereGeometry args={[0.08, 16, 16]} />
          <meshBasicMaterial color="#22d3ee" transparent opacity={opacity} />
        </mesh>
      ))}
    </group>
  )
}

function UnitSphere({ opacity = 0.3, scale = 1 }: { opacity?: number, scale?: number }) {
  const meshRef = useRef<THREE.Mesh>(null)

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y = state.clock.getElapsedTime() * 0.3
    }
  })

  // Unit sphere has volume 4π/3
  // To inscribe in cube of side 2, sphere radius = 1
  return (
    <mesh ref={meshRef} scale={scale}>
      <sphereGeometry args={[1, 64, 64]} />
      <meshBasicMaterial
        color="#a855f7"
        transparent
        opacity={opacity}
        wireframe
      />
    </mesh>
  )
}

function GeometricLabels() {
  return (
    <>
      <Html position={[0, 2.5, 0]} center>
        <div className="text-cyan-400 text-lg font-bold bg-black/80 px-3 py-1 rounded whitespace-nowrap">
          Z² = 8 × (4π/3)
        </div>
      </Html>
      <Html position={[2, 0.5, 0]} center>
        <div className="text-cyan-300 text-sm bg-black/80 px-2 py-1 rounded whitespace-nowrap">
          8 vertices
        </div>
      </Html>
      <Html position={[-2, -0.5, 0]} center>
        <div className="text-purple-300 text-sm bg-black/80 px-2 py-1 rounded whitespace-nowrap">
          V = 4π/3
        </div>
      </Html>
    </>
  )
}

// Connection lines showing relationships
function ConnectionWeb() {
  const lines = useMemo(() => {
    // Create lines from center to each vertex
    return cubeVertices.map(v => ({
      start: [0, 0, 0] as [number, number, number],
      end: v as unknown as [number, number, number]
    }))
  }, [])

  return (
    <>
      {lines.map((line, i) => (
        <Line
          key={i}
          points={[line.start, line.end]}
          color="#a855f7"
          lineWidth={1}
          transparent
          opacity={0.3}
          dashed
          dashSize={0.1}
          gapSize={0.1}
        />
      ))}
    </>
  )
}

// Physics constants display
function PhysicsOverlay({ showDetails }: { showDetails: boolean }) {
  return (
    <AnimatePresence>
      {showDetails && (
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: 20 }}
          className="absolute top-4 right-4 bg-black/90 backdrop-blur p-4 rounded-lg border border-purple-500/30 max-w-xs"
        >
          <h3 className="text-sm font-bold text-purple-400 mb-3">Geometric Identities</h3>

          <div className="space-y-3 text-xs">
            <div className="border-b border-gray-700 pb-2">
              <div className="text-cyan-400 font-mono">Z = 2√(8π/3) = {Z.toFixed(4)}</div>
              <div className="text-gray-500 mt-1">Master constant from Friedmann geometry</div>
            </div>

            <div className="border-b border-gray-700 pb-2">
              <div className="text-purple-400 font-mono">Z² = 8 × (4π/3) = {Z_SQUARED.toFixed(4)}</div>
              <div className="text-gray-500 mt-1">Cube vertices × Sphere volume</div>
            </div>

            <div className="border-b border-gray-700 pb-2">
              <div className="text-yellow-400 font-mono">Z⁴ × 9/π² = 1024 = 2¹⁰</div>
              <div className="text-gray-500 mt-1">10 bits of information</div>
            </div>

            <div className="border-b border-gray-700 pb-2">
              <div className="text-green-400 font-mono">9Z²/(8π) = 12</div>
              <div className="text-gray-500 mt-1">= dim(SU(3)×SU(2)×U(1))</div>
            </div>

            <div>
              <div className="text-red-400 font-mono">α⁻¹ = 4Z² + 3 = 137.04</div>
              <div className="text-gray-500 mt-1">Fine structure constant (0.004% error)</div>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}

export default function GeometricVisualization() {
  const [showDetails, setShowDetails] = useState(true)
  const [showSphere, setShowSphere] = useState(true)
  const [showCube, setShowCube] = useState(true)
  const [showConnections, setShowConnections] = useState(false)

  return (
    <div className="relative w-full h-screen bg-gradient-to-b from-gray-900 to-black">
      {/* 3D Canvas */}
      <Canvas camera={{ position: [4, 3, 4], fov: 50 }}>
        <ambientLight intensity={0.3} />
        <pointLight position={[10, 10, 10]} intensity={1} />

        {showCube && <RotatingCube opacity={0.9} />}
        {showSphere && <UnitSphere opacity={0.3} />}
        {showConnections && <ConnectionWeb />}

        <GeometricLabels />

        <OrbitControls
          enablePan={false}
          enableZoom={true}
          minDistance={3}
          maxDistance={10}
        />
      </Canvas>

      {/* Title and Controls */}
      <div className="absolute top-4 left-4 bg-black/90 backdrop-blur p-4 rounded-lg border border-purple-500/30 max-w-sm">
        <h2 className="text-lg font-bold text-white mb-1">Geometric Structure of Z</h2>
        <p className="text-xs text-gray-400 mb-3">
          Visualizing Z² = 8 × (4π/3) = cube vertices × sphere volume
        </p>

        {/* Toggle controls */}
        <div className="space-y-2 text-sm">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={showCube}
              onChange={(e) => setShowCube(e.target.checked)}
              className="rounded border-gray-600"
            />
            <span className="text-cyan-400">Cube (8 vertices)</span>
          </label>

          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={showSphere}
              onChange={(e) => setShowSphere(e.target.checked)}
              className="rounded border-gray-600"
            />
            <span className="text-purple-400">Sphere (V = 4π/3)</span>
          </label>

          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={showConnections}
              onChange={(e) => setShowConnections(e.target.checked)}
              className="rounded border-gray-600"
            />
            <span className="text-gray-400">Connection lines</span>
          </label>

          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={showDetails}
              onChange={(e) => setShowDetails(e.target.checked)}
              className="rounded border-gray-600"
            />
            <span className="text-gray-400">Show identities panel</span>
          </label>
        </div>

        {/* Key equation */}
        <div className="mt-4 p-3 bg-gradient-to-r from-cyan-900/30 to-purple-900/30 rounded border border-cyan-500/30">
          <div className="text-center">
            <span className="text-cyan-400 text-lg font-mono">Z² = </span>
            <span className="text-cyan-300 text-lg">8</span>
            <span className="text-gray-400 text-lg"> × </span>
            <span className="text-purple-300 text-lg">(4π/3)</span>
          </div>
          <div className="text-center mt-1 text-xs text-gray-500">
            cube × sphere = cosmology × geometry
          </div>
        </div>
      </div>

      {/* Physics overlay */}
      <PhysicsOverlay showDetails={showDetails} />

      {/* Bottom info */}
      <div className="absolute bottom-4 left-4 right-4 flex justify-center">
        <div className="bg-black/80 backdrop-blur px-4 py-2 rounded-lg border border-gray-700 text-xs text-gray-400 max-w-lg text-center">
          The number 8 (cube vertices) and 4π/3 (sphere volume) combine in Z to connect
          discrete and continuous geometry. Drag to rotate, scroll to zoom.
        </div>
      </div>
    </div>
  )
}
