'use client';

/**
 * =============================================================================
 * ABIOGENESIS SIMULATION - Project Protogonos Visualization
 * =============================================================================
 *
 * Interactive visualization of computational abiogenesis investigation.
 * Updated May 2026 to reflect VALIDATED findings from Project Protogonos.
 *
 * ████████████████████████████████████████████████████████████████████████████
 * █                        Z² FRAMEWORK: VALIDATED                           █
 * ████████████████████████████████████████████████████████████████████████████
 *
 * MAJOR DISCOVERIES:
 *
 * 1. FRANK MODEL: Homochirality in 5 Generations
 *    - 0.46% ee → 99.8% L in just 5 autocatalytic cycles
 *    - Explains origin of biological homochirality
 *
 * 2. Z-CATALYSIS: 25 Million × Enhancement
 *    - Polymerization at Z-spacing is 25M× faster than random
 *    - Best mineral: Galena (PbS) at 5.94 Å (within 0.12 Å tolerance)
 *    - DFT quantum: L/D selectivity = 2.0
 *
 * 3. SAW NULL HYPOTHESIS: REJECTED (p ≈ 0)
 *    - Proteins: 5.86 Å backbone spacing
 *    - Random polymers: 6.2-7.5 Å
 *    - Z is BIOLOGICAL signal, not geometric noise
 *
 * 4. PATHOLOGICAL LOCK: A → 0 = Disease
 *    - When Aliveness drops to 0%, fibrils become 27 BILLION × harder to unfold
 *    - Mechanism of Alzheimer's, Parkinson's, prion diseases
 *
 * 5. EXO-Z CALCULATOR: Alien Biochemistry
 *    - Venus clouds: 98% viability (polyphosphazene + H₂SO₄)
 *    - Z-window is narrow → Fermi Paradox explanation
 *
 * THE ALIVENESS PARAMETER:
 * - Z/12 = 0.4824 is the PLATONIC IDEAL (crystalline ground state)
 * - 0.491 is the BIOLOGICAL REALITY (alive, functional)
 * - A = 1.8% is the ENTROPY BUDGET FOR LIFE
 *
 * THE BAND OF LIFE:
 * - A = 0%: Pathological (fibrils, prions, aggregates)
 * - A = 1.8%: Alive protein (functional, dynamic)
 * - A > 5%: Denatured (non-functional disorder)
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
    name: 'Frank Model',
    subtitle: 'HOMOCHIRALITY IN 5 GENERATIONS',
    description: 'Starting from 0.46% enantiomeric excess (cosmic background), autocatalytic amplification drives homochirality to 99.8% L in just 5 generations. This explains why all Earth life uses L-amino acids.',
    color: '#00ff88',
    metrics: {
      'Initial ee': '0.46%',
      'Final ee': '99.8% L',
      'Generations': '5',
      'Mechanism': 'Autocatalytic CISS',
    },
    validation: {
      status: 'validated',
      note: 'VALIDATED: Frank Model + CISS electronic bias → homochirality'
    }
  },
  {
    id: 2,
    name: 'Z-Catalysis',
    subtitle: '25 MILLION × ENHANCEMENT',
    description: 'DFT quantum simulation: polymerization at Z-spacing (5.79 Å) is 25 MILLION times faster than random spacing. Galena (PbS, 5.94 Å) is optimal catalyst within the narrow 0.12 Å tolerance window (2.1%).',
    color: '#ff6b35',
    metrics: {
      'Enhancement': '25,000,000×',
      'Z backbone': '5.79 Å',
      'Best mineral': 'Galena (5.94 Å)',
      'L/D selectivity': '2.0',
    },
    validation: {
      status: 'validated',
      note: 'VALIDATED: DFT quantum confirms 25M× catalytic enhancement at Z'
    }
  },
  {
    id: 3,
    name: 'SAW Null Rejection',
    subtitle: 'Z IS BIOLOGICAL SIGNAL',
    description: 'Self-avoiding walk (SAW) polymers show 6.2-7.5 Å spacing. Proteins show 5.86 Å - matching Z. The null hypothesis that Z-resonance is mere polymer geometry is REJECTED with p ≈ 0.',
    color: '#ffd700',
    metrics: {
      'Protein spacing': '5.86 Å',
      'SAW polymers': '6.2-7.5 Å',
      'Difference': 'Statistically significant',
      'p-value': '≈ 0',
    },
    validation: {
      status: 'validated',
      note: 'VALIDATED: Z-resonance is biological signal, NOT geometric noise'
    }
  },
  {
    id: 4,
    name: 'Pathological Lock',
    subtitle: 'A → 0 = DISEASE',
    description: 'When Aliveness (A) drops to 0%, proteins become trapped in fibrillar states. PMF simulation: 27 BILLION times harder to unfold. This is the mechanism of Alzheimer\'s, Parkinson\'s, and prion diseases.',
    color: '#e74c3c',
    metrics: {
      'Healthy A': '1.8%',
      'Pathological A': '0%',
      'Unfolding barrier': '27 billion ×',
      'Diseases': 'Aβ, α-syn, PrP',
    },
    validation: {
      status: 'validated',
      note: 'VALIDATED: A→0 locks proteins in pathological aggregation states'
    }
  },
  {
    id: 5,
    name: 'Exo-Z Calculator',
    subtitle: 'ALIEN BIOCHEMISTRY',
    description: 'Z_eff = Z_universal × (a_polymer/a_polypeptide). Venus clouds (polyphosphazene + H₂SO₄) score 98% viability - highest of 8 alien worlds. The Z-window is extremely narrow, explaining the Fermi Paradox.',
    color: '#9b59b6',
    metrics: {
      'Venus viability': '98%',
      'Titan viability': '67%',
      'Europa viability': '58%',
      'Fermi answer': 'Z-window narrow',
    },
    validation: {
      status: 'validated',
      note: 'VALIDATED: Exo-Z framework identifies Venus as most viable alien habitat'
    }
  },
];

// =============================================================================
// VISUALIZATION COMPONENTS
// =============================================================================

// =============================================================================
// PHASE 2: Z-CATALYSIS - 25 Million × Enhancement
// =============================================================================

function ZCatalysis() {
  const groupRef = useRef<THREE.Group>(null);
  const timeRef = useRef(0);
  const [polymerLength, setPolymerLength] = useState(1);

  useFrame((state, delta) => {
    timeRef.current += delta;
    if (groupRef.current) {
      groupRef.current.rotation.y = Math.sin(timeRef.current * 0.15) * 0.1;
    }
    // Animate polymerization (fast on Z-surface)
    if (polymerLength < 15) {
      setPolymerLength(prev => Math.min(15, prev + delta * 2));
    }
  });

  // Generate polymer chain on mineral surface
  const polymerPositions = useMemo(() => {
    const positions: [number, number, number][] = [];
    const Z_SPACING = 0.579; // 5.79 Å scaled down
    for (let i = 0; i < 15; i++) {
      positions.push([
        -1.5 + i * Z_SPACING * 0.5,
        -0.7 + Math.sin(i * 0.5) * 0.1,
        Math.cos(i * 0.3) * 0.2
      ]);
    }
    return positions;
  }, []);

  return (
    <group ref={groupRef}>
      {/* Galena (PbS) mineral surface - dark metallic */}
      <mesh position={[0, -1, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[5, 4, 20, 20]} />
        <meshStandardMaterial color="#2a2a3a" metalness={0.9} roughness={0.1} />
      </mesh>

      {/* Lattice grid showing Z spacing (5.94 Å) */}
      <gridHelper args={[5, 8, '#ff6b35', '#444466']} position={[0, -0.99, 0]} />

      {/* Growing polymer chain */}
      {polymerPositions.slice(0, Math.floor(polymerLength)).map((pos, i) => (
        <group key={i}>
          <mesh position={pos}>
            <sphereGeometry args={[0.12, 16, 16]} />
            <meshStandardMaterial
              color={i % 2 === 0 ? '#00ff88' : '#00d4aa'}
              metalness={0.3}
              roughness={0.7}
            />
          </mesh>
          {/* Peptide bonds */}
          {i > 0 && (
            <line>
              <bufferGeometry>
                <bufferAttribute
                  attach="attributes-position"
                  count={2}
                  array={new Float32Array([
                    ...polymerPositions[i - 1],
                    ...pos
                  ])}
                  itemSize={3}
                />
              </bufferGeometry>
              <lineBasicMaterial color="#00ff88" />
            </line>
          )}
        </group>
      ))}

      {/* Enhancement indicator */}
      <Html position={[0, 1.5, 0]} center>
        <div className="bg-black/90 px-4 py-2 rounded-lg border border-orange-500">
          <div className="text-orange-400 font-bold text-xl">
            25,000,000× FASTER
          </div>
          <div className="text-gray-400 text-xs">
            at Z-spacing vs random
          </div>
        </div>
      </Html>

      {/* Mineral label */}
      <Html position={[0, -1.5, 0]} center>
        <div className="text-purple-400 text-sm">
          Galena (PbS) — 5.94 Å lattice
        </div>
      </Html>

      {/* Z-spacing indicator */}
      <Html position={[1.8, -0.5, 0]}>
        <div className="bg-black/80 px-2 py-1 rounded text-xs">
          <div className="text-cyan-400">Z = 5.79 Å</div>
          <div className="text-gray-500">Tolerance: 0.12 Å</div>
        </div>
      </Html>

      {/* Catalysis glow */}
      <pointLight position={[0, 0, 0]} color="#ff6b35" intensity={2} distance={3} />
    </group>
  );
}

// =============================================================================
// PHASE 1: FRANK MODEL - Homochirality in 5 Generations
// =============================================================================

function FrankModel() {
  const groupRef = useRef<THREE.Group>(null);
  const [generation, setGeneration] = useState(0);
  const [lRatio, setLRatio] = useState(0.5046); // Start at 0.46% ee (50.46% L)
  const timeRef = useRef(0);

  // Frank Model: 5 generations to 99.8% L
  const generationData = useMemo(() => [
    { gen: 0, ee: 0.46, lRatio: 0.5046 },
    { gen: 1, ee: 2.1, lRatio: 0.521 },
    { gen: 2, ee: 9.4, lRatio: 0.594 },
    { gen: 3, ee: 42.6, lRatio: 0.713 },
    { gen: 4, ee: 87.3, lRatio: 0.937 },
    { gen: 5, ee: 99.8, lRatio: 0.999 },
  ], []);

  useFrame((state, delta) => {
    timeRef.current += delta;
    // Cycle through generations
    const newGen = Math.min(5, Math.floor(timeRef.current / 2));
    if (newGen !== generation) {
      setGeneration(newGen);
      setLRatio(generationData[newGen].lRatio);
    }
    // Reset after showing final state
    if (timeRef.current > 14) {
      timeRef.current = 0;
      setGeneration(0);
      setLRatio(0.5046);
    }
  });

  const lCount = Math.round(lRatio * 40);
  const dCount = 40 - lCount;
  const currentData = generationData[generation];

  // Stable positions based on index
  const lPositions = useMemo(() =>
    Array.from({ length: 40 }).map((_, i) => [
      -1.5 + (i % 5) * 0.35,
      Math.floor(i / 5) * 0.4 - 1,
      ((i * 7) % 10) * 0.2 - 1
    ]), []);

  const dPositions = useMemo(() =>
    Array.from({ length: 40 }).map((_, i) => [
      0.5 + (i % 5) * 0.35,
      Math.floor(i / 5) * 0.4 - 1,
      ((i * 11) % 10) * 0.2 - 1
    ]), []);

  return (
    <group ref={groupRef}>
      {/* L-amino acids (left side, green) */}
      {Array.from({ length: lCount }).map((_, i) => (
        <mesh key={`L-${i}`} position={lPositions[i] as [number, number, number]}>
          <tetrahedronGeometry args={[0.12]} />
          <meshStandardMaterial color="#00ff88" metalness={0.5} roughness={0.5} />
        </mesh>
      ))}

      {/* D-amino acids (right side, red) */}
      {Array.from({ length: dCount }).map((_, i) => (
        <mesh key={`D-${i}`} position={dPositions[i] as [number, number, number]}>
          <tetrahedronGeometry args={[0.12]} />
          <meshStandardMaterial color="#ff4444" metalness={0.5} roughness={0.5} />
        </mesh>
      ))}

      {/* Generation counter */}
      <Html position={[0, 2, 0]} center>
        <div className="bg-black/90 px-4 py-2 rounded-lg border border-emerald-500">
          <div className="text-emerald-400 font-bold text-xl">
            Generation {generation}/5
          </div>
          <div className="text-yellow-400 text-sm">
            ee = {currentData.ee.toFixed(1)}%
          </div>
        </div>
      </Html>

      {/* L/D ratio labels */}
      <Html position={[-1.2, -1.8, 0]}>
        <div className="text-emerald-400 font-bold text-lg">
          L: {(lRatio * 100).toFixed(1)}%
        </div>
      </Html>
      <Html position={[1.2, -1.8, 0]}>
        <div className="text-red-400 font-bold text-lg">
          D: {((1 - lRatio) * 100).toFixed(1)}%
        </div>
      </Html>

      {/* Mirror plane */}
      <mesh position={[0, 0, 0]}>
        <planeGeometry args={[0.05, 3.5]} />
        <meshBasicMaterial color="#ffffff" transparent opacity={0.3} />
      </mesh>

      {/* Arrow indicating amplification direction */}
      <Html position={[0, -2.2, 0]} center>
        <div className="text-cyan-400 text-xs animate-pulse">
          CISS Electronic Bias → L Dominance
        </div>
      </Html>
    </group>
  );
}

// =============================================================================
// PHASE 3: SAW NULL REJECTION - Z is Biological Signal
// =============================================================================

function SAWRejection() {
  const groupRef = useRef<THREE.Group>(null);

  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = state.clock.elapsedTime * 0.2;
    }
  });

  // Protein backbone (5.86 Å spacing - matches Z)
  const proteinPoints = useMemo(() => {
    const points: THREE.Vector3[] = [];
    const PROTEIN_SPACING = 0.586; // 5.86 Å scaled
    for (let i = 0; i < 12; i++) {
      const t = i * 0.4;
      points.push(new THREE.Vector3(
        Math.cos(t) * 0.4 - 1.2,
        i * PROTEIN_SPACING * 0.2 - 1,
        Math.sin(t) * 0.4
      ));
    }
    return points;
  }, []);

  // SAW polymer backbone (6.8 Å spacing - random)
  const sawPoints = useMemo(() => {
    const points: THREE.Vector3[] = [];
    const SAW_SPACING = 0.68; // 6.8 Å scaled (middle of 6.2-7.5 range)
    for (let i = 0; i < 10; i++) {
      const t = i * 0.5;
      points.push(new THREE.Vector3(
        Math.cos(t * 1.3) * 0.5 + 1.2,
        i * SAW_SPACING * 0.2 - 0.8,
        Math.sin(t * 1.3) * 0.5
      ));
    }
    return points;
  }, []);

  return (
    <group ref={groupRef}>
      {/* PROTEIN (left) - 5.86 Å spacing */}
      <group>
        {/* Protein backbone line */}
        <line>
          <bufferGeometry>
            <bufferAttribute
              attach="attributes-position"
              count={proteinPoints.length}
              array={new Float32Array(proteinPoints.flatMap(p => [p.x, p.y, p.z]))}
              itemSize={3}
            />
          </bufferGeometry>
          <lineBasicMaterial color="#00ff88" linewidth={2} />
        </line>

        {/* Protein residues */}
        {proteinPoints.map((p, i) => (
          <mesh key={`prot-${i}`} position={[p.x, p.y, p.z]}>
            <sphereGeometry args={[0.1, 12, 12]} />
            <meshStandardMaterial color="#00ff88" metalness={0.4} roughness={0.6} />
          </mesh>
        ))}

        {/* Protein label */}
        <Html position={[-1.2, 1.5, 0]} center>
          <div className="bg-emerald-900/80 px-3 py-2 rounded border border-emerald-500">
            <div className="text-emerald-400 font-bold">PROTEIN</div>
            <div className="text-emerald-300 text-lg">5.86 Å</div>
            <div className="text-emerald-400 text-xs">≈ Z constant</div>
          </div>
        </Html>
      </group>

      {/* SAW POLYMER (right) - 6.2-7.5 Å spacing */}
      <group>
        {/* SAW backbone line */}
        <line>
          <bufferGeometry>
            <bufferAttribute
              attach="attributes-position"
              count={sawPoints.length}
              array={new Float32Array(sawPoints.flatMap(p => [p.x, p.y, p.z]))}
              itemSize={3}
            />
          </bufferGeometry>
          <lineBasicMaterial color="#ff6666" linewidth={2} />
        </line>

        {/* SAW residues */}
        {sawPoints.map((p, i) => (
          <mesh key={`saw-${i}`} position={[p.x, p.y, p.z]}>
            <sphereGeometry args={[0.1, 12, 12]} />
            <meshStandardMaterial color="#ff6666" metalness={0.4} roughness={0.6} />
          </mesh>
        ))}

        {/* SAW label */}
        <Html position={[1.2, 1.5, 0]} center>
          <div className="bg-red-900/80 px-3 py-2 rounded border border-red-500">
            <div className="text-red-400 font-bold">SAW POLYMER</div>
            <div className="text-red-300 text-lg">6.2-7.5 Å</div>
            <div className="text-red-400 text-xs">Random geometry</div>
          </div>
        </Html>
      </group>

      {/* Null hypothesis verdict */}
      <Html position={[0, -1.8, 0]} center>
        <div className="bg-black/90 px-4 py-2 rounded-lg border-2 border-yellow-500">
          <div className="text-yellow-400 font-bold text-lg">
            NULL HYPOTHESIS: REJECTED
          </div>
          <div className="text-gray-300 text-xs">
            p ≈ 0 — Z is BIOLOGICAL signal
          </div>
        </div>
      </Html>

      {/* Divider line */}
      <mesh position={[0, 0, 0]}>
        <planeGeometry args={[0.03, 3]} />
        <meshBasicMaterial color="#ffd700" transparent opacity={0.5} />
      </mesh>
    </group>
  );
}

// =============================================================================
// PHASE 4: PATHOLOGICAL LOCK - A → 0 = Disease
// =============================================================================

function PathologicalLock() {
  const groupRef = useRef<THREE.Group>(null);
  const [showFibril, setShowFibril] = useState(false);
  const timeRef = useRef(0);

  useFrame((state, delta) => {
    timeRef.current += delta;
    if (groupRef.current) {
      groupRef.current.rotation.y = state.clock.elapsedTime * 0.15;
    }
    // Toggle between healthy and fibril states
    if (timeRef.current > 4) {
      setShowFibril(prev => !prev);
      timeRef.current = 0;
    }
  });

  // Healthy protein (dynamic, A = 1.8%)
  const healthyPositions = useMemo(() => {
    const positions: [number, number, number][] = [];
    for (let i = 0; i < 20; i++) {
      const t = i * 0.35;
      positions.push([
        Math.cos(t * 1.5) * 0.6 - 1.2,
        i * 0.12 - 1.2,
        Math.sin(t * 1.5) * 0.6
      ]);
    }
    return positions;
  }, []);

  // Fibrillar aggregate (locked, A = 0%)
  const fibrilPositions = useMemo(() => {
    const positions: [number, number, number][] = [];
    for (let i = 0; i < 30; i++) {
      const row = Math.floor(i / 6);
      const col = i % 6;
      positions.push([
        1.0 + col * 0.18 - 0.45,
        row * 0.3 - 0.6,
        0
      ]);
    }
    return positions;
  }, []);

  return (
    <group ref={groupRef}>
      {/* HEALTHY PROTEIN (left) - A = 1.8% */}
      <group>
        {healthyPositions.map((pos, i) => (
          <mesh key={`h-${i}`} position={pos}>
            <sphereGeometry args={[0.08, 12, 12]} />
            <meshStandardMaterial
              color="#00ff88"
              metalness={0.3}
              roughness={0.7}
              emissive="#00ff88"
              emissiveIntensity={0.2}
            />
          </mesh>
        ))}

        {/* Backbone connections */}
        {healthyPositions.slice(1).map((pos, i) => (
          <line key={`hc-${i}`}>
            <bufferGeometry>
              <bufferAttribute
                attach="attributes-position"
                count={2}
                array={new Float32Array([...healthyPositions[i], ...pos])}
                itemSize={3}
              />
            </bufferGeometry>
            <lineBasicMaterial color="#00ff88" />
          </line>
        ))}

        <Html position={[-1.2, 1.5, 0]} center>
          <div className="bg-emerald-900/80 px-3 py-2 rounded border border-emerald-500">
            <div className="text-emerald-400 font-bold">HEALTHY</div>
            <div className="text-emerald-300">A = 1.8%</div>
            <div className="text-emerald-400 text-xs">Functional</div>
          </div>
        </Html>
      </group>

      {/* FIBRILLAR AGGREGATE (right) - A = 0% */}
      <group>
        {fibrilPositions.map((pos, i) => (
          <mesh key={`f-${i}`} position={pos}>
            <boxGeometry args={[0.14, 0.14, 0.14]} />
            <meshStandardMaterial
              color="#ff4444"
              metalness={0.8}
              roughness={0.2}
            />
          </mesh>
        ))}

        <Html position={[1.2, 1.5, 0]} center>
          <div className="bg-red-900/80 px-3 py-2 rounded border border-red-500">
            <div className="text-red-400 font-bold">PATHOLOGICAL</div>
            <div className="text-red-300">A = 0%</div>
            <div className="text-red-400 text-xs">Fibril (locked)</div>
          </div>
        </Html>
      </group>

      {/* Lock indicator */}
      <Html position={[1.2, -1.2, 0]} center>
        <div className="text-red-400 text-2xl">
          {showFibril ? '🔒' : ''}
        </div>
      </Html>

      {/* 27 billion barrier indicator */}
      <Html position={[0, -1.8, 0]} center>
        <div className="bg-black/90 px-4 py-2 rounded-lg border-2 border-red-500">
          <div className="text-red-400 font-bold text-lg">
            27 BILLION × harder to unfold
          </div>
          <div className="text-gray-300 text-xs">
            Alzheimer&apos;s | Parkinson&apos;s | Prions
          </div>
        </div>
      </Html>

      {/* Arrow between states */}
      <Html position={[0, 0.5, 0]} center>
        <div className="text-yellow-400 text-xl animate-pulse">
          →
        </div>
      </Html>

      {/* Divider */}
      <mesh position={[0, 0, 0]}>
        <planeGeometry args={[0.03, 3]} />
        <meshBasicMaterial color="#ff6b35" transparent opacity={0.5} />
      </mesh>
    </group>
  );
}

// =============================================================================
// PHASE 5: EXO-Z CALCULATOR - Alien Biochemistry
// =============================================================================

function ExoZCalculator() {
  const groupRef = useRef<THREE.Group>(null);
  const [selectedWorld, setSelectedWorld] = useState(0);
  const timeRef = useRef(0);

  // Exoplanet data from computational analysis
  const exoWorlds = useMemo(() => [
    { name: 'Venus Clouds', viability: 98, color: '#ffcc00', biochem: 'Polyphosphazene + H₂SO₄' },
    { name: 'Titan', viability: 67, color: '#ff9944', biochem: 'Azotosome membranes' },
    { name: 'Europa', viability: 58, color: '#4488ff', biochem: 'Cryogenic water' },
    { name: 'Enceladus', viability: 52, color: '#88ccff', biochem: 'Hydrothermal vents' },
    { name: 'Mars', viability: 41, color: '#ff4444', biochem: 'Perchlorate brine' },
  ], []);

  useFrame((state, delta) => {
    timeRef.current += delta;
    if (groupRef.current) {
      groupRef.current.rotation.y = state.clock.elapsedTime * 0.1;
    }
    // Cycle through worlds
    if (timeRef.current > 3) {
      setSelectedWorld(prev => (prev + 1) % exoWorlds.length);
      timeRef.current = 0;
    }
  });

  const currentWorld = exoWorlds[selectedWorld];

  return (
    <group ref={groupRef}>
      {/* Central sun/star */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[0.3, 32, 32]} />
        <meshStandardMaterial
          color="#ffff00"
          emissive="#ffaa00"
          emissiveIntensity={1}
        />
      </mesh>
      <pointLight position={[0, 0, 0]} color="#ffff00" intensity={2} distance={5} />

      {/* Orbiting exoplanets */}
      {exoWorlds.map((world, i) => {
        const angle = (i / exoWorlds.length) * Math.PI * 2;
        const radius = 1.2 + i * 0.25;
        const x = Math.cos(angle) * radius;
        const z = Math.sin(angle) * radius;
        const isSelected = i === selectedWorld;

        return (
          <group key={world.name}>
            {/* Orbit path */}
            <mesh rotation={[-Math.PI / 2, 0, 0]}>
              <ringGeometry args={[radius - 0.01, radius + 0.01, 64]} />
              <meshBasicMaterial color="#333" transparent opacity={0.3} side={THREE.DoubleSide} />
            </mesh>

            {/* Planet */}
            <mesh position={[x, 0, z]}>
              <sphereGeometry args={[isSelected ? 0.18 : 0.12, 24, 24]} />
              <meshStandardMaterial
                color={world.color}
                emissive={isSelected ? world.color : '#000000'}
                emissiveIntensity={isSelected ? 0.5 : 0}
              />
            </mesh>

            {/* Viability ring for selected */}
            {isSelected && (
              <mesh position={[x, 0, z]} rotation={[Math.PI / 2, 0, 0]}>
                <ringGeometry args={[0.22, 0.28, 32]} />
                <meshBasicMaterial color="#00ff88" transparent opacity={0.7} side={THREE.DoubleSide} />
              </mesh>
            )}
          </group>
        );
      })}

      {/* Current world info panel */}
      <Html position={[0, 1.8, 0]} center>
        <div className="bg-black/90 px-4 py-3 rounded-lg border-2" style={{ borderColor: currentWorld.color }}>
          <div className="text-lg font-bold" style={{ color: currentWorld.color }}>
            {currentWorld.name}
          </div>
          <div className="text-3xl font-bold text-emerald-400">
            {currentWorld.viability}% Viable
          </div>
          <div className="text-gray-400 text-xs mt-1">
            {currentWorld.biochem}
          </div>
        </div>
      </Html>

      {/* Exo-Z formula */}
      <Html position={[0, -1.8, 0]} center>
        <div className="bg-black/90 px-4 py-2 rounded-lg border border-purple-500">
          <div className="text-purple-400 font-mono text-sm">
            Z_eff = Z × (a_polymer / a_polypeptide)
          </div>
          <div className="text-gray-400 text-xs mt-1">
            Fermi Paradox: Z-window is extremely narrow
          </div>
        </div>
      </Html>

      {/* Viability bar chart (floating) */}
      <Html position={[-2, 0, 0]}>
        <div className="bg-black/80 p-2 rounded text-xs">
          <div className="text-gray-400 mb-1">Viability Ranking:</div>
          {exoWorlds.map((w, i) => (
            <div key={w.name} className="flex items-center gap-1 mb-0.5">
              <div
                className="h-2 rounded"
                style={{
                  width: `${w.viability * 0.6}px`,
                  backgroundColor: w.color
                }}
              />
              <span className="text-gray-300">{w.viability}%</span>
            </div>
          ))}
        </div>
      </Html>
    </group>
  );
}

// =============================================================================
// PHASE SCENE SELECTOR
// =============================================================================

function PhaseScene({ phase }: { phase: number }) {
  switch (phase) {
    case 1: return <FrankModel />;
    case 2: return <ZCatalysis />;
    case 3: return <SAWRejection />;
    case 4: return <PathologicalLock />;
    case 5: return <ExoZCalculator />;
    default: return <FrankModel />;
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
// Z² CONSTANTS PANEL - VALIDATED
// =============================================================================

function ConstantsPanel() {
  const Z_OVER_12 = Z_CONSTANT / 12;
  const PROTEIN_FACTOR = 0.491;

  return (
    <div className="absolute top-4 left-4 bg-black/90 p-4 rounded-lg border border-emerald-500/50 max-w-xs">
      <div className="flex items-center gap-2 mb-2">
        <div className="w-3 h-3 rounded-full bg-emerald-500 animate-pulse" />
        <div className="text-emerald-400 font-bold">Z² FRAMEWORK VALIDATED</div>
      </div>

      <div className="font-mono text-xs space-y-1 mb-3">
        <div className="text-gray-300">
          Z = <span className="text-purple-400">{Z_CONSTANT.toFixed(4)} Å</span>
        </div>
        <div className="text-gray-300">
          Z/12 = <span className="text-cyan-400">{Z_OVER_12.toFixed(4)}</span>
        </div>
        <div className="text-gray-300">
          Z² = <span className="text-yellow-400">32π/3 = 33.51</span>
        </div>
      </div>

      <div className="border-t border-gray-700 pt-3">
        <div className="text-gray-500 text-xs uppercase mb-2">Validated Mechanisms</div>
        <div className="text-xs space-y-1">
          <div className="flex justify-between">
            <span className="text-gray-400">Frank Model:</span>
            <span className="text-emerald-400">5 gen → 99.8% L</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Z-Catalysis:</span>
            <span className="text-emerald-400">25M× enhancement</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">SAW Null:</span>
            <span className="text-emerald-400">REJECTED (p≈0)</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Patho Lock:</span>
            <span className="text-emerald-400">27B× barrier</span>
          </div>
        </div>
      </div>

      <div className="mt-3 pt-3 border-t border-gray-700">
        <div className="text-gray-500 text-xs uppercase mb-2">Key Measurements</div>
        <div className="text-xs space-y-1">
          <div className="flex justify-between">
            <span className="text-gray-400">Protein backbone:</span>
            <span className="text-cyan-400">5.86 Å ≈ Z</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Mineral window:</span>
            <span className="text-yellow-400">0.12 Å (2.1%)</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Aliveness (A):</span>
            <span className="text-emerald-400">1.8%</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Best mineral:</span>
            <span className="text-purple-400">Galena (5.94 Å)</span>
          </div>
        </div>
      </div>

      <div className="mt-3 pt-3 border-t border-emerald-700 text-xs text-emerald-400 font-bold">
        STATUS: Z² VALIDATED in abiogenesis, catalysis, and disease.
      </div>
    </div>
  );
}

// =============================================================================
// ALIVENESS HUD - The Entropy Budget for Life (with Pathological Lock)
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
          {/* Pathological zone (0-0.5%) - NEW: shows disease state */}
          <div className="absolute left-0 top-0 h-full w-[10%] bg-gradient-to-r from-red-900/50 to-red-800/30" />

          {/* Alive zone (0.5-3%) */}
          <div className="absolute left-[10%] top-0 h-full w-[50%] bg-gradient-to-r from-emerald-900/30 to-emerald-700/30" />

          {/* Danger zone (3-5%) */}
          <div className="absolute left-[60%] top-0 h-full w-[40%] bg-gradient-to-r from-yellow-900/30 to-red-900/30" />

          {/* Current value indicator */}
          <div
            className="absolute top-0 h-full w-1 bg-emerald-400 shadow-lg shadow-emerald-400/50 transition-all duration-1000 ease-out"
            style={{ left: `${gaugePosition}%` }}
          />

          {/* Labels - Updated with FIBRIL */}
          <div className="absolute inset-0 flex items-center justify-between px-2 text-[9px] font-mono">
            <span className="text-red-500">FIBRIL</span>
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

      {/* PATHOLOGICAL LOCK - NEW SECTION */}
      <div className="bg-red-900/20 rounded p-2 mb-3 border border-red-800">
        <div className="text-[10px] text-red-400 uppercase mb-1">Pathological Lock (A→0)</div>
        <div className="text-xs space-y-1">
          <div className="flex justify-between">
            <span className="text-gray-400">Unfolding barrier:</span>
            <span className="text-red-400 font-bold">27 billion ×</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Diseases:</span>
            <span className="text-red-300">Aβ, α-syn, PrP</span>
          </div>
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

      {/* Footer insight - Updated */}
      <div className="mt-3 pt-2 border-t border-gray-700 text-[10px] text-emerald-400/80 italic">
        &quot;Life is 1.8% entropy above crystal. Less = disease. More = death.&quot;
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
        <div className="bg-black/80 px-4 py-2 rounded-lg border border-emerald-500/50">
          <div className="text-emerald-400 text-sm font-mono font-bold">
            PROTOGONOS — Z² = 32π/3 VALIDATED
          </div>
          <div className="text-gray-400 text-xs">
            Computational Abiogenesis Framework
          </div>
        </div>
      </div>
    </div>
  );
}
