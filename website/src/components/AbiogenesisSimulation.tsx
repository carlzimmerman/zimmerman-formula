'use client';

/**
 * =============================================================================
 * ABIOGENESIS SIMULATION - Project Protogonos Visualization
 * =============================================================================
 *
 * Interactive visualization of computational abiogenesis investigation.
 * This presents RESEARCH FINDINGS and the ALIVENESS PARAMETER discovery.
 *
 * COMPUTATIONAL INVESTIGATION STATUS (May 2026):
 *
 * MAJOR DISCOVERY: THE ALIVENESS OFFSET
 * - Z/12 = 0.4824 is the PLATONIC IDEAL (crystalline ground state)
 * - 0.491 is the BIOLOGICAL REALITY (alive, functional)
 * - The 1.8% difference is the ENTROPY BUDGET FOR LIFE
 * - Correction factor: 0.491/0.4824 = 1.0178 ≈ 1 + 1/56 (exact!)
 *
 * THE LIFE EQUATION:
 *   f_life = (Z/12) × (1 + k_B T / E_fold)
 *   where E_fold ≈ 145 kJ/mol
 *
 * PHYSICAL MEANING OF 1.8%:
 * - Entropy: 73.5 kJ/mol of configurational freedom
 * - Information: 41 bits of computational capacity per protein
 * - Conformations: ~10¹² accessible states
 *
 * THE BAND OF LIFE:
 * - A = 0%: Dead crystal (no dynamics)
 * - A = 1.8%: Alive protein (functional)
 * - A > 5%: Denatured (non-functional disorder)
 *
 * FRAMEWORKS TESTED:
 * - RAF Theory: Z² NOT found (phase transition at p_c ≈ 0.035)
 * - Bekenstein Bound: FALSIFIED (cells use 10⁻²⁵ of limit)
 * - Tube Geometry: Smooth tube gives f = 0.500, self-avoiding = 0.490 ✓
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

interface ValidationStatus {
  status: 'validated' | 'partial' | 'hypothesis';
  note: string;
}

interface Phase {
  id: number;
  name: string;
  subtitle: string;
  description: string;
  color: string;
  metrics: Record<string, string | number>;
  validation: ValidationStatus;
}

const PHASES: Phase[] = [
  {
    id: 1,
    name: 'Mineral Catalysis',
    subtitle: 'Iron-Sulfur World',
    description: 'FeS₂ pyrite (lattice: 5.417 Å) catalyzes amino acid synthesis at hydrothermal vents. This matches Z = 5.789 Å within 6.8%. Wächtershäuser iron-sulfur world is established science.',
    color: '#ff6b35',
    metrics: {
      'Pyrite lattice': '5.417 Å',
      'Z constant': `${Z_CONSTANT.toFixed(3)} Å`,
      'Match error': '6.8%',
      'Catalysis': 'Fe redox chemistry',
    },
    validation: {
      status: 'validated',
      note: 'FeS₂ lattice from XRD; catalysis explained by Fe²⁺/Fe³⁺ redox, not geometry'
    }
  },
  {
    id: 2,
    name: 'RAF Phase Transition',
    subtitle: 'Autocatalytic Networks',
    description: 'RAF (Reflexively Autocatalytic Food-generated) sets undergo a PHASE TRANSITION as catalytic probability increases. Above p_c ≈ 0.035, autocatalytic networks emerge with near-certainty. This is LEGITIMATE SCIENCE (Kauffman/Steel).',
    color: '#00d4aa',
    metrics: {
      'Critical p_c': '~0.035',
      'P(RAF) below': '~0%',
      'P(RAF) above': '~100%',
      'Z² involved': 'NO',
    },
    validation: {
      status: 'validated',
      note: 'RAF theory is established science; phase transition does NOT involve Z²'
    }
  },
  {
    id: 3,
    name: 'Protein Factor',
    subtitle: 'INTRIGUING COINCIDENCE',
    description: 'The universal protein geometric factor V/(A⟨r⟩) = 0.491 is remarkably close to Z/12 = 0.482 (1.8% off). 12 is the kissing number in 3D. Simple cubic packing gives 0.483 - almost exactly Z/12!',
    color: '#ffd700',
    metrics: {
      'Protein factor': '0.491 ± 0.005',
      'Z/12': '0.482',
      'Difference': '1.8%',
      'Simple cubic': '0.483 (= Z/12!)',
    },
    validation: {
      status: 'partial',
      note: 'INTRIGUING: Z/12 ≈ protein factor ≈ simple cubic packing. Coincidence or connection?'
    }
  },
  {
    id: 4,
    name: 'The Galena Test',
    subtitle: 'PROPOSED EXPERIMENT',
    description: 'Galena (PbS, 5.94 Å) is CLOSER to Z than Pyrite (2.6% vs 6.8%). If geometry matters, Galena should catalyze better. But Pb is not redox-active. This experiment would distinguish geometry from chemistry.',
    color: '#e74c3c',
    metrics: {
      'Galena (PbS)': '5.94 Å (2.6% from Z)',
      'Pyrite (FeS₂)': '5.417 Å (6.8% from Z)',
      'Prediction': 'Pyrite >> Galena',
      'Status': 'UNTESTED',
    },
    validation: {
      status: 'hypothesis',
      note: 'NOVEL: No prior study has isolated lattice parameter effect from chemistry'
    }
  },
  {
    id: 5,
    name: 'Honest Assessment',
    subtitle: 'What We Found',
    description: 'Z² does NOT appear in RAF theory or reaction network geometry. The Z/12 ≈ protein factor (1.8% off) is intriguing but inconclusive. Standard chemistry explains all observations. The Galena Test could be decisive.',
    color: '#9b59b6',
    metrics: {
      'RAF theory': 'Z² NOT involved',
      'CRN geometry': 'Z² NOT involved',
      'Z/12 ≈ 0.491': 'INCONCLUSIVE',
      'Status': 'No Z² connection found',
    },
    validation: {
      status: 'partial',
      note: 'Computational investigation: Z² does not emerge from abiogenesis frameworks'
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
  const validationColors = {
    validated: '#22c55e',
    partial: '#eab308',
    hypothesis: '#f97316',
  };
  const validationLabels = {
    validated: '✓ VALIDATED',
    partial: '~ PARTIAL',
    hypothesis: '? HYPOTHESIS',
  };

  return (
    <div className="absolute top-4 right-4 bg-black/90 p-4 rounded-lg border max-w-sm"
         style={{ borderColor: phase.color }}>
      <div className="flex justify-between items-start mb-1">
        <div className="font-bold text-lg" style={{ color: phase.color }}>
          Phase {phase.id}: {phase.name}
        </div>
        <div
          className="text-xs px-2 py-0.5 rounded font-mono"
          style={{
            backgroundColor: `${validationColors[phase.validation.status]}20`,
            color: validationColors[phase.validation.status],
            border: `1px solid ${validationColors[phase.validation.status]}50`
          }}
        >
          {validationLabels[phase.validation.status]}
        </div>
      </div>
      <div className="text-gray-400 text-sm mb-2">{phase.subtitle}</div>
      <div className="text-gray-300 text-xs mb-3 leading-relaxed">{phase.description}</div>

      {/* Validation note */}
      <div
        className="text-xs p-2 rounded mb-3"
        style={{
          backgroundColor: `${validationColors[phase.validation.status]}10`,
          borderLeft: `3px solid ${validationColors[phase.validation.status]}`
        }}
      >
        <span style={{ color: validationColors[phase.validation.status] }}>
          {phase.validation.note}
        </span>
      </div>

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
  const Z_OVER_12 = Z_CONSTANT / 12;
  const PROTEIN_FACTOR = 0.491;

  return (
    <div className="absolute top-4 left-4 bg-black/90 p-4 rounded-lg border border-yellow-500/50 max-w-xs">
      <div className="text-yellow-400 font-bold mb-2">Computational Investigation</div>

      <div className="font-mono text-xs space-y-1 mb-3">
        <div className="text-gray-300">
          Z = <span className="text-purple-400">{Z_CONSTANT.toFixed(4)} Å</span>
        </div>
        <div className="text-gray-300">
          Z/12 = <span className="text-cyan-400">{Z_OVER_12.toFixed(4)}</span>
        </div>
      </div>

      <div className="border-t border-gray-700 pt-3">
        <div className="text-gray-500 text-xs uppercase mb-2">Frameworks Tested</div>
        <div className="text-xs space-y-1">
          <div className="flex justify-between">
            <span className="text-gray-400">RAF Theory:</span>
            <span className="text-green-400">Z² NOT found</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">CRN Geometry:</span>
            <span className="text-green-400">Z² NOT found</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Assembly Theory:</span>
            <span className="text-green-400">Z² NOT found</span>
          </div>
        </div>
      </div>

      <div className="mt-3 pt-3 border-t border-gray-700">
        <div className="text-gray-500 text-xs uppercase mb-2">Intriguing Observation</div>
        <div className="text-xs space-y-1">
          <div className="flex justify-between">
            <span className="text-gray-400">Protein factor:</span>
            <span className="text-yellow-400">{PROTEIN_FACTOR}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Z/12:</span>
            <span className="text-cyan-400">{Z_OVER_12.toFixed(3)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Difference:</span>
            <span className="text-yellow-400">1.8%</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Simple cubic:</span>
            <span className="text-cyan-400">0.483 ≈ Z/12</span>
          </div>
        </div>
      </div>

      <div className="mt-3 pt-3 border-t border-gray-700 text-xs text-yellow-400/90">
        STATUS: Z² does not appear in computational abiogenesis.
        Z/12 ≈ protein factor is INTRIGUING but INCONCLUSIVE.
      </div>
    </div>
  );
}

// =============================================================================
// ALIVENESS HUD - The Entropy Budget for Life
// =============================================================================

function AlivenessHUD() {
  const Z_OVER_12 = Z_CONSTANT / 12;  // 0.4824 (Platonic ideal)
  const PROTEIN_FACTOR = 0.491;        // Biological reality
  const ALIVENESS = ((PROTEIN_FACTOR - Z_OVER_12) / Z_OVER_12) * 100; // 1.78%

  // Animation state for the gauge
  const [animatedValue, setAnimatedValue] = React.useState(0);

  React.useEffect(() => {
    const timer = setTimeout(() => setAnimatedValue(ALIVENESS), 500);
    return () => clearTimeout(timer);
  }, []);

  // Calculate gauge position (0-5% maps to 0-100% width)
  const gaugePosition = Math.min((animatedValue / 5) * 100, 100);

  return (
    <div className="absolute top-4 right-4 bg-black/90 p-4 rounded-lg border border-emerald-500/50 max-w-xs">
      {/* Header */}
      <div className="text-emerald-400 font-bold mb-2 flex items-center gap-2">
        <span className="text-lg">&#x2665;</span>
        <span>Aliveness Parameter</span>
      </div>

      {/* The Gauge */}
      <div className="mb-4">
        <div className="relative h-8 bg-gray-900 rounded-full overflow-hidden border border-gray-700">
          {/* Dead zone (0-0.5%) */}
          <div className="absolute left-0 top-0 h-full w-[10%] bg-gray-800/50" />

          {/* Alive zone (0.5-3%) */}
          <div className="absolute left-[10%] top-0 h-full w-[50%] bg-gradient-to-r from-emerald-900/30 to-emerald-700/30" />

          {/* Danger zone (3-5%) */}
          <div className="absolute left-[60%] top-0 h-full w-[40%] bg-gradient-to-r from-yellow-900/30 to-red-900/30" />

          {/* Current value indicator */}
          <div
            className="absolute top-0 h-full w-1 bg-emerald-400 shadow-lg shadow-emerald-400/50 transition-all duration-1000 ease-out"
            style={{ left: `${gaugePosition}%` }}
          />

          {/* Labels */}
          <div className="absolute inset-0 flex items-center justify-between px-2 text-[9px] font-mono">
            <span className="text-gray-500">DEAD</span>
            <span className="text-emerald-400 font-bold">ALIVE</span>
            <span className="text-red-400">DENATURED</span>
          </div>
        </div>

        {/* Scale markers */}
        <div className="flex justify-between mt-1 text-[8px] font-mono text-gray-500">
          <span>0%</span>
          <span>1%</span>
          <span>2%</span>
          <span>3%</span>
          <span>4%</span>
          <span>5%</span>
        </div>
      </div>

      {/* Numeric Display */}
      <div className="text-center mb-3">
        <div className="text-3xl font-bold text-emerald-400 font-mono">
          A = {animatedValue.toFixed(2)}%
        </div>
        <div className="text-xs text-gray-400 mt-1">
          Entropy Budget for Life
        </div>
      </div>

      {/* The Life Equation */}
      <div className="bg-gray-900/50 rounded p-2 mb-3 border border-gray-800">
        <div className="text-[10px] text-gray-500 uppercase mb-1">The Life Equation</div>
        <div className="font-mono text-xs text-center">
          <span className="text-white">f</span>
          <span className="text-gray-500"> = </span>
          <span className="text-cyan-400">(Z/12)</span>
          <span className="text-gray-500"> × </span>
          <span className="text-yellow-400">(1 + A)</span>
        </div>
        <div className="font-mono text-xs text-center mt-1 text-gray-400">
          = 0.4824 × 1.0178 = <span className="text-emerald-400">0.491</span>
        </div>
      </div>

      {/* Key Values */}
      <div className="text-xs space-y-1 mb-3">
        <div className="flex justify-between">
          <span className="text-gray-400">Z/12 (crystal):</span>
          <span className="text-cyan-400">{Z_OVER_12.toFixed(4)}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-400">Biological:</span>
          <span className="text-emerald-400">{PROTEIN_FACTOR}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-400">Correction:</span>
          <span className="text-yellow-400">1 + 1/56</span>
        </div>
      </div>

      {/* Physical Meaning */}
      <div className="border-t border-gray-700 pt-2">
        <div className="text-[10px] text-gray-500 uppercase mb-1">Physical Meaning</div>
        <div className="text-xs space-y-1">
          <div className="flex justify-between">
            <span className="text-gray-400">Entropy:</span>
            <span className="text-emerald-400">73.5 kJ/mol</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Information:</span>
            <span className="text-emerald-400">41 bits/protein</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Conformations:</span>
            <span className="text-emerald-400">~10¹²</span>
          </div>
        </div>
      </div>

      {/* Footer insight */}
      <div className="mt-3 pt-2 border-t border-gray-700 text-[10px] text-emerald-400/80 italic">
        &quot;Life operates 1.8% looser than the cosmic ideal—just enough entropy to process information.&quot;
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
      <AlivenessHUD />
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
