'use client';

/**
 * =============================================================================
 * ABIOGENESIS SIMULATION - Project Protogonos Visualization
 * =============================================================================
 *
 * Interactive 5-phase visualization of the geometric origin of life:
 *
 * Phase 1: Prebiotic Synthesis - Miller-Urey style synthesis on mineral surfaces
 * Phase 2: Chirality Breaking - L-amino acid selection via Z² geometry
 * Phase 3: Polymerization - Geometric natural selection of peptides
 * Phase 4: Autocatalytic Closure - Emergence of self-replicating networks
 * Phase 5: Compartmentalization - Proto-cell membrane assembly
 *
 * Each phase demonstrates how Z² geometry makes life inevitable.
 *
 * =============================================================================
 */

import React, { useState, useRef, useMemo, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Html, Text } from '@react-three/drei';
import * as THREE from 'three';

// =============================================================================
// Z² CONSTANTS
// =============================================================================

const Z_SQUARED = (32 * Math.PI) / 3; // ~33.51
const Z_CONSTANT = 2 * Math.sqrt((8 * Math.PI) / 3); // ~5.7888 Å
const THETA_Z = Math.PI / Z_CONSTANT; // ~0.543 rad = ~31.09°

// Backbone angles
const PHI_HELIX = -57; // degrees
const PSI_HELIX = -47; // degrees

// =============================================================================
// PHASE DEFINITIONS
// =============================================================================

interface Phase {
  id: number;
  name: string;
  subtitle: string;
  description: string;
  color: string;
  metrics: Record<string, string | number>;
}

const PHASES: Phase[] = [
  {
    id: 1,
    name: 'Prebiotic Synthesis',
    subtitle: 'From Chaos to Chemistry',
    description: 'Simple molecules (H₂O, CO₂, NH₃, HCN) form amino acids on mineral surfaces at ~100°C. Catalytic surfaces with ~5.79 Å lattice spacing are optimal.',
    color: '#ff6b35',
    metrics: {
      'Temperature': '80-120°C',
      'Catalyst': 'FeS₂ / Montmorillonite',
      'Z Distance': `${Z_CONSTANT.toFixed(4)} Å`,
      'Products': '20 amino acids',
    }
  },
  {
    id: 2,
    name: 'Chirality Breaking',
    subtitle: 'Left-Handed Selection',
    description: 'The Z² geometry creates a ~0.05 kJ/mol bias favoring L-amino acids. Through autocatalytic amplification, this tiny excess grows to 99.9%+ homochirality.',
    color: '#7b68ee',
    metrics: {
      'Initial L-excess': '10⁻¹⁷ (parity violation)',
      'Final L-excess': '99.99%',
      'Energy bias': '0.05 kJ/mol',
      'Mechanism': 'Frank autocatalysis',
    }
  },
  {
    id: 3,
    name: 'Polymerization',
    subtitle: 'The First Peptides',
    description: 'Random polymerization produces many peptides, but only those adopting Z² backbone angles (φ=-57°, ψ=-47°) are stable. Geometric natural selection.',
    color: '#00d4aa',
    metrics: {
      'α-helix φ': `${PHI_HELIX}°`,
      'α-helix ψ': `${PSI_HELIX}°`,
      'Stability factor': '10-100× longer half-life',
      'Selection': 'Geometric shielding',
    }
  },
  {
    id: 4,
    name: 'Autocatalytic Closure',
    subtitle: 'Self-Replication Emerges',
    description: 'Z²-stable peptides catalyze each others formation via aromatic stacking at 6.015 Å. Reflexively Autocatalytic Sets (RAF) spontaneously emerge.',
    color: '#ffd700',
    metrics: {
      'Stacking distance': '6.015 Å',
      'RAF sets': '3-8 peptides',
      'Replication': 'Geometric templating',
      'Error threshold': '±7° angle deviation',
    }
  },
  {
    id: 5,
    name: 'Compartmentalization',
    subtitle: 'The First Cell',
    description: 'Fatty acids self-assemble into vesicles with head-group spacing matching the Z constant. Z²-compliant amphipathic helices spontaneously insert as proto-channels.',
    color: '#00bfff',
    metrics: {
      'Head spacing': `${Z_CONSTANT.toFixed(3)} Å`,
      'Bilayer': 'Fatty acid vesicles',
      'Insertion ΔG': '-8 kcal/mol (Z² helix)',
      'Result': 'PROTO-CELL',
    }
  },
];

// =============================================================================
// MOLECULE VISUALIZATIONS
// =============================================================================

interface MoleculeProps {
  position: [number, number, number];
  color: string;
  size?: number;
  label?: string;
}

function SimpleMolecule({ position, color, size = 0.15, label }: MoleculeProps) {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y = state.clock.elapsedTime * 0.5;
    }
  });

  return (
    <group position={position}>
      <mesh ref={meshRef}>
        <sphereGeometry args={[size, 16, 16]} />
        <meshStandardMaterial color={color} metalness={0.3} roughness={0.7} />
      </mesh>
      {label && (
        <Html position={[0, size + 0.1, 0]} center>
          <div className="text-xs text-white bg-black/70 px-1 rounded whitespace-nowrap">
            {label}
          </div>
        </Html>
      )}
    </group>
  );
}

// =============================================================================
// PHASE 1: PREBIOTIC SYNTHESIS VISUALIZATION
// =============================================================================

function PrebioticSynthesis() {
  const groupRef = useRef<THREE.Group>(null);
  const timeRef = useRef(0);

  // Simple molecules floating
  const molecules = useMemo(() => [
    { pos: [-1.5, 0.5, 0], color: '#3498db', label: 'H₂O' },
    { pos: [1.5, 0.3, 0.5], color: '#e74c3c', label: 'CO₂' },
    { pos: [0, 1.2, -0.5], color: '#2ecc71', label: 'NH₃' },
    { pos: [-0.8, -0.5, 0.8], color: '#9b59b6', label: 'HCN' },
    { pos: [1.0, -0.3, -0.8], color: '#f39c12', label: 'H₂S' },
  ], []);

  // Amino acid products
  const aminoAcids = useMemo(() => [
    { pos: [0, 0, 0], color: '#ff6b35', label: 'Gly' },
    { pos: [0.5, -0.3, 0.3], color: '#ff6b35', label: 'Ala' },
    { pos: [-0.4, -0.2, -0.3], color: '#ff6b35', label: 'Ser' },
  ], []);

  useFrame((state, delta) => {
    timeRef.current += delta;
    if (groupRef.current) {
      groupRef.current.rotation.y = Math.sin(timeRef.current * 0.2) * 0.1;
    }
  });

  return (
    <group ref={groupRef}>
      {/* Mineral surface */}
      <mesh position={[0, -1, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[4, 4, 20, 20]} />
        <meshStandardMaterial color="#4a3728" wireframe={false} metalness={0.8} roughness={0.2} />
      </mesh>

      {/* Lattice grid showing Z distance */}
      <gridHelper args={[4, 7, '#ff6b35', '#553322']} position={[0, -0.99, 0]} />

      {/* Simple molecules */}
      {molecules.map((m, i) => (
        <SimpleMolecule key={i} position={m.pos as [number, number, number]} color={m.color} label={m.label} size={0.12} />
      ))}

      {/* Amino acid products emerging */}
      {aminoAcids.map((aa, i) => (
        <SimpleMolecule key={`aa-${i}`} position={aa.pos as [number, number, number]} color={aa.color} label={aa.label} size={0.18} />
      ))}

      {/* Lightning/energy spark */}
      <pointLight position={[0, 2, 0]} color="#ffff00" intensity={2} distance={5} />
    </group>
  );
}

// =============================================================================
// PHASE 2: CHIRALITY BREAKING VISUALIZATION
// =============================================================================

function ChiralityBreaking() {
  const groupRef = useRef<THREE.Group>(null);
  const [lRatio, setLRatio] = useState(0.5);

  useFrame((state, delta) => {
    // Animate amplification
    if (lRatio < 0.999) {
      setLRatio(prev => Math.min(0.999, prev + delta * 0.05));
    }
  });

  const lCount = Math.round(lRatio * 30);
  const dCount = 30 - lCount;

  return (
    <group ref={groupRef}>
      {/* L-amino acids (left side, green) */}
      {Array.from({ length: lCount }).map((_, i) => (
        <mesh
          key={`L-${i}`}
          position={[
            -1.5 + Math.random() * 1.5,
            Math.random() * 2 - 1,
            Math.random() * 2 - 1
          ]}
        >
          <tetrahedronGeometry args={[0.12]} />
          <meshStandardMaterial color="#00ff88" metalness={0.5} roughness={0.5} />
        </mesh>
      ))}

      {/* D-amino acids (right side, red) */}
      {Array.from({ length: dCount }).map((_, i) => (
        <mesh
          key={`D-${i}`}
          position={[
            0.5 + Math.random() * 1.5,
            Math.random() * 2 - 1,
            Math.random() * 2 - 1
          ]}
        >
          <tetrahedronGeometry args={[0.12]} />
          <meshStandardMaterial color="#ff4444" metalness={0.5} roughness={0.5} />
        </mesh>
      ))}

      {/* Labels */}
      <Html position={[-1.5, 1.5, 0]}>
        <div className="text-emerald-400 font-bold text-lg">
          L: {(lRatio * 100).toFixed(1)}%
        </div>
      </Html>
      <Html position={[1.5, 1.5, 0]}>
        <div className="text-red-400 font-bold text-lg">
          D: {((1 - lRatio) * 100).toFixed(1)}%
        </div>
      </Html>

      {/* Mirror plane */}
      <mesh position={[0, 0, 0]} rotation={[0, 0, 0]}>
        <planeGeometry args={[0.05, 3]} />
        <meshBasicMaterial color="#ffffff" transparent opacity={0.3} />
      </mesh>
    </group>
  );
}

// =============================================================================
// PHASE 3: POLYMERIZATION VISUALIZATION
// =============================================================================

function Polymerization() {
  const helixRef = useRef<THREE.Group>(null);

  useFrame((state) => {
    if (helixRef.current) {
      helixRef.current.rotation.y = state.clock.elapsedTime * 0.3;
    }
  });

  // Generate helix backbone
  const helixPoints = useMemo(() => {
    const points: THREE.Vector3[] = [];
    for (let i = 0; i < 40; i++) {
      const t = i * 0.3;
      const x = Math.cos(t) * 0.5;
      const y = i * 0.08 - 1.5;
      const z = Math.sin(t) * 0.5;
      points.push(new THREE.Vector3(x, y, z));
    }
    return points;
  }, []);

  return (
    <group ref={helixRef}>
      {/* Helix backbone */}
      <line>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            count={helixPoints.length}
            array={new Float32Array(helixPoints.flatMap(p => [p.x, p.y, p.z]))}
            itemSize={3}
          />
        </bufferGeometry>
        <lineBasicMaterial color="#00d4aa" linewidth={2} />
      </line>

      {/* Residue spheres along helix */}
      {helixPoints.filter((_, i) => i % 3 === 0).map((p, i) => (
        <mesh key={i} position={[p.x, p.y, p.z]}>
          <sphereGeometry args={[0.1, 12, 12]} />
          <meshStandardMaterial color="#00d4aa" metalness={0.4} roughness={0.6} />
        </mesh>
      ))}

      {/* Angle indicator */}
      <Html position={[1.2, 0, 0]}>
        <div className="bg-black/80 p-2 rounded text-xs">
          <div className="text-emerald-400">φ = {PHI_HELIX}°</div>
          <div className="text-emerald-400">ψ = {PSI_HELIX}°</div>
        </div>
      </Html>

      {/* Unstable random coil (fading) */}
      <mesh position={[1.5, -0.5, 0]}>
        <torusKnotGeometry args={[0.3, 0.05, 50, 8]} />
        <meshStandardMaterial color="#666666" transparent opacity={0.3} />
      </mesh>
      <Html position={[1.5, 0.3, 0]}>
        <div className="text-gray-500 text-xs">Unstable</div>
      </Html>
    </group>
  );
}

// =============================================================================
// PHASE 4: AUTOCATALYTIC CLOSURE VISUALIZATION
// =============================================================================

function AutocatalyticClosure() {
  const groupRef = useRef<THREE.Group>(null);

  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = state.clock.elapsedTime * 0.2;
    }
  });

  // RAF network nodes
  const nodes = useMemo(() => [
    { pos: [0, 0, 0], label: 'P1' },
    { pos: [1, 0.5, 0.5], label: 'P2' },
    { pos: [-0.5, 1, 0], label: 'P3' },
    { pos: [0.5, -0.8, 0.3], label: 'P4' },
    { pos: [-1, -0.3, -0.5], label: 'P5' },
  ], []);

  // Network connections (catalytic relationships)
  const edges = useMemo(() => [
    [0, 1], [1, 2], [2, 0], [0, 3], [3, 4], [4, 0], [1, 3], [2, 4]
  ], []);

  return (
    <group ref={groupRef}>
      {/* Network nodes */}
      {nodes.map((node, i) => (
        <group key={i} position={node.pos as [number, number, number]}>
          <mesh>
            <dodecahedronGeometry args={[0.2]} />
            <meshStandardMaterial color="#ffd700" metalness={0.6} roughness={0.4} />
          </mesh>
          <Html position={[0, 0.35, 0]} center>
            <div className="text-yellow-400 text-xs font-bold">{node.label}</div>
          </Html>
        </group>
      ))}

      {/* Network edges (catalytic arrows) */}
      {edges.map(([from, to], i) => {
        const start = new THREE.Vector3(...(nodes[from].pos as [number, number, number]));
        const end = new THREE.Vector3(...(nodes[to].pos as [number, number, number]));
        const mid = start.clone().lerp(end, 0.5);
        return (
          <line key={i}>
            <bufferGeometry>
              <bufferAttribute
                attach="attributes-position"
                count={2}
                array={new Float32Array([...start.toArray(), ...end.toArray()])}
                itemSize={3}
              />
            </bufferGeometry>
            <lineBasicMaterial color="#ffd700" transparent opacity={0.5} />
          </line>
        );
      })}

      {/* Label */}
      <Html position={[0, -1.5, 0]} center>
        <div className="text-yellow-400 text-sm">Reflexively Autocatalytic Set</div>
      </Html>
    </group>
  );
}

// =============================================================================
// PHASE 5: COMPARTMENTALIZATION VISUALIZATION
// =============================================================================

function Compartmentalization() {
  const vesicleRef = useRef<THREE.Mesh>(null);

  useFrame((state) => {
    if (vesicleRef.current) {
      vesicleRef.current.rotation.y = state.clock.elapsedTime * 0.15;
      vesicleRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.3) * 0.1;
    }
  });

  return (
    <group>
      {/* Vesicle membrane */}
      <mesh ref={vesicleRef}>
        <sphereGeometry args={[1.2, 32, 32]} />
        <meshStandardMaterial
          color="#00bfff"
          transparent
          opacity={0.3}
          side={THREE.DoubleSide}
        />
      </mesh>

      {/* Inner membrane layer */}
      <mesh>
        <sphereGeometry args={[1.0, 32, 32]} />
        <meshStandardMaterial
          color="#0088cc"
          transparent
          opacity={0.2}
          side={THREE.DoubleSide}
        />
      </mesh>

      {/* Internal autocatalytic network (from phase 4) */}
      <group scale={0.5}>
        {[
          [0, 0, 0], [0.4, 0.3, 0.2], [-0.3, 0.4, -0.1], [0.2, -0.4, 0.3]
        ].map((pos, i) => (
          <mesh key={i} position={pos as [number, number, number]}>
            <dodecahedronGeometry args={[0.1]} />
            <meshStandardMaterial color="#ffd700" />
          </mesh>
        ))}
      </group>

      {/* Proto-channel (helix) inserted in membrane */}
      <group position={[1.1, 0, 0]} rotation={[0, 0, Math.PI / 2]}>
        <mesh>
          <cylinderGeometry args={[0.08, 0.08, 0.4, 12]} />
          <meshStandardMaterial color="#00d4aa" />
        </mesh>
      </group>

      {/* Labels */}
      <Html position={[0, 1.8, 0]} center>
        <div className="text-cyan-400 font-bold text-lg">PROTO-CELL</div>
      </Html>
      <Html position={[1.5, 0, 0]}>
        <div className="text-emerald-400 text-xs">Z² Channel</div>
      </Html>
    </group>
  );
}

// =============================================================================
// PHASE SCENE SELECTOR
// =============================================================================

function PhaseScene({ phase }: { phase: number }) {
  switch (phase) {
    case 1: return <PrebioticSynthesis />;
    case 2: return <ChiralityBreaking />;
    case 3: return <Polymerization />;
    case 4: return <AutocatalyticClosure />;
    case 5: return <Compartmentalization />;
    default: return <PrebioticSynthesis />;
  }
}

// =============================================================================
// HUD PANEL
// =============================================================================

function PhaseHUD({ phase }: { phase: Phase }) {
  return (
    <div className="absolute top-4 right-4 bg-black/85 p-4 rounded-lg border max-w-xs"
         style={{ borderColor: phase.color }}>
      <div className="font-bold text-lg mb-1" style={{ color: phase.color }}>
        Phase {phase.id}: {phase.name}
      </div>
      <div className="text-gray-400 text-sm mb-3">{phase.subtitle}</div>
      <div className="text-gray-300 text-xs mb-4">{phase.description}</div>

      <div className="border-t border-gray-700 pt-3">
        <div className="text-gray-500 text-xs uppercase mb-2">Key Metrics</div>
        {Object.entries(phase.metrics).map(([key, value]) => (
          <div key={key} className="flex justify-between text-xs mb-1">
            <span className="text-gray-400">{key}:</span>
            <span style={{ color: phase.color }}>{value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

// =============================================================================
// TIMELINE
// =============================================================================

function Timeline({ currentPhase, onPhaseChange }: { currentPhase: number; onPhaseChange: (p: number) => void }) {
  return (
    <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-black/85 p-4 rounded-lg">
      <div className="flex items-center gap-2">
        {PHASES.map((phase) => (
          <button
            key={phase.id}
            onClick={() => onPhaseChange(phase.id)}
            className={`relative px-4 py-2 rounded-lg transition-all ${
              currentPhase === phase.id
                ? ''
                : 'opacity-60 hover:opacity-100'
            }`}
            style={{
              backgroundColor: currentPhase === phase.id ? phase.color : '#333',
              boxShadow: currentPhase === phase.id ? `0 0 0 2px black, 0 0 0 4px ${phase.color}` : 'none',
            }}
          >
            <span className="text-white font-bold text-sm">{phase.id}</span>
            <div className="absolute -bottom-6 left-1/2 transform -translate-x-1/2 whitespace-nowrap text-xs text-gray-400">
              {currentPhase === phase.id && phase.name}
            </div>
          </button>
        ))}
      </div>

      {/* Progress line */}
      <div className="flex items-center gap-0 mt-2">
        {PHASES.map((phase, i) => (
          <React.Fragment key={phase.id}>
            <div
              className="w-8 h-1 rounded"
              style={{
                backgroundColor: phase.id <= currentPhase ? phase.color : '#444'
              }}
            />
            {i < PHASES.length - 1 && (
              <div className="w-4 h-0.5 bg-gray-600" />
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}

// =============================================================================
// Z² CONSTANTS PANEL
// =============================================================================

function ConstantsPanel() {
  return (
    <div className="absolute top-4 left-4 bg-black/85 p-4 rounded-lg border border-purple-500/50 max-w-xs">
      <div className="text-purple-400 font-bold mb-2">Z² Geometric Constants</div>
      <div className="font-mono text-xs space-y-1">
        <div className="text-gray-300">
          Z² = 32π/3 = <span className="text-purple-400">{Z_SQUARED.toFixed(4)}</span>
        </div>
        <div className="text-gray-300">
          Z = 2√(8π/3) = <span className="text-purple-400">{Z_CONSTANT.toFixed(4)} Å</span>
        </div>
        <div className="text-gray-300">
          θ_Z = π/Z = <span className="text-purple-400">{(THETA_Z * 180 / Math.PI).toFixed(2)}°</span>
        </div>
      </div>
      <div className="mt-3 pt-3 border-t border-gray-700 text-xs text-gray-500">
        The geometry of spacetime IS the code for life.
      </div>
    </div>
  );
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export default function AbiogenesisSimulation() {
  const [currentPhase, setCurrentPhase] = useState(1);

  // Auto-advance through phases (optional)
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentPhase(prev => prev >= 5 ? 1 : prev + 1);
    }, 12000); // 12 seconds per phase

    return () => clearInterval(timer);
  }, []);

  const phase = PHASES.find(p => p.id === currentPhase) || PHASES[0];

  return (
    <div className="relative w-full h-[700px] bg-slate-950 rounded-lg overflow-hidden">
      <Canvas
        camera={{ position: [3, 2, 3], fov: 50 }}
        gl={{ antialias: true }}
      >
        <ambientLight intensity={0.4} />
        <directionalLight position={[5, 5, 5]} intensity={1} />
        <pointLight position={[-5, -5, -5]} intensity={0.5} color="#8888ff" />

        <PhaseScene phase={currentPhase} />

        <OrbitControls
          enableZoom={true}
          enablePan={false}
          minDistance={2}
          maxDistance={8}
          autoRotate={false}
        />

        {/* Background */}
        <mesh>
          <sphereGeometry args={[50, 32, 32]} />
          <meshBasicMaterial color="#0a0a15" side={THREE.BackSide} />
        </mesh>
      </Canvas>

      {/* UI Overlays */}
      <ConstantsPanel />
      <PhaseHUD phase={phase} />
      <Timeline currentPhase={currentPhase} onPhaseChange={setCurrentPhase} />

      {/* Title overlay */}
      <div className="absolute top-4 left-1/2 transform -translate-x-1/2 text-center">
        <div className="text-white/80 text-sm font-mono">
          PROTOGONOS — Geometric Origin of Life
        </div>
      </div>
    </div>
  );
}
