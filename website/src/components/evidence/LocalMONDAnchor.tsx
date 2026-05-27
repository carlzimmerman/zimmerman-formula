/**
 * =============================================================================
 * LOCAL MOND ANCHOR - Gaia Wide Binary Visualization
 * =============================================================================
 *
 * Directive WWWW: Visualize Gaia DR3 wide binaries showing MOND acceleration
 * anomaly, with topological tethers connecting to T³/Z₂ boundaries.
 *
 * Features:
 * - Rotating binary star pairs
 * - Color-coded by MOND regime (deep/transitional/Newtonian)
 * - Velocity comparison overlay
 * - Topological tether to nearest boundary
 *
 * =============================================================================
 */

import React, { useRef, useMemo, useState, useEffect } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';
import { Line, Text } from '@react-three/drei';

// Constants
const SCALE = 0.1; // Scale factor for visualization
const ORBIT_SPEED = 0.3; // Rotation speed

// Color scheme
const REGIME_COLORS = {
  deep_mond: '#2ECC71',     // Green
  transitional: '#F39C12',  // Orange
  newtonian: '#9B59B6',     // Purple
};

// Interfaces
interface WideBinary {
  name: string;
  ra: number;
  dec: number;
  distance_pc: number;
  separation_au: number;
  v_observed_kms: number;
  v_newton_kms: number;
  m1_msun: number;
  m2_msun: number;
  total_mass_msun: number;
  internal_accel: number;
  internal_accel_over_a0: number;
  observed_boost: number;
  mond_predicted_boost: number;
  regime: 'deep_mond' | 'transitional' | 'newtonian';
  topological_tether: {
    nearest_boundary: string;
    distance_to_boundary_gpc: number;
    direction_vector: number[];
  };
}

interface BinaryData {
  metadata: {
    total_binaries: number;
    mond_a0: number;
  };
  binaries: WideBinary[];
  statistics: {
    deep_mond_count: number;
    transitional_count: number;
    newtonian_count: number;
    mean_boost_deep_mond: number;
    mean_boost_newtonian: number;
  };
}

interface LocalMONDAnchorProps {
  opacity?: number;
  showTethers?: boolean;
  selectedRegime?: string;
}

/**
 * Single wide binary pair
 */
function WideBinaryPair({
  binary,
  index,
  showTether = true,
}: {
  binary: WideBinary;
  index: number;
  showTether?: boolean;
}) {
  const groupRef = useRef<THREE.Group>(null);
  const star1Ref = useRef<THREE.Mesh>(null);
  const star2Ref = useRef<THREE.Mesh>(null);

  // Position based on RA/Dec (simplified projection)
  const position = useMemo(() => {
    const theta = (binary.ra / 360) * Math.PI * 2;
    const phi = ((binary.dec + 90) / 180) * Math.PI;
    const r = 2 + index * 0.3; // Radial spread

    return new THREE.Vector3(
      r * Math.sin(phi) * Math.cos(theta),
      r * Math.sin(phi) * Math.sin(theta),
      r * Math.cos(phi)
    );
  }, [binary, index]);

  const color = useMemo(() => new THREE.Color(REGIME_COLORS[binary.regime]), [binary.regime]);

  // Star sizes based on mass
  const star1Size = useMemo(() => 0.03 + binary.m1_msun * 0.02, [binary.m1_msun]);
  const star2Size = useMemo(() => 0.03 + binary.m2_msun * 0.02, [binary.m2_msun]);

  // Separation for visualization (exaggerated)
  const separation = useMemo(() => {
    return Math.log10(binary.separation_au) * 0.1;
  }, [binary.separation_au]);

  // Orbital animation with velocity boost visualization
  useFrame(({ clock }) => {
    if (groupRef.current) {
      // Rotation speed proportional to observed velocity
      const t = clock.getElapsedTime() * ORBIT_SPEED * binary.observed_boost;

      if (star1Ref.current && star2Ref.current) {
        star1Ref.current.position.x = separation * Math.cos(t);
        star1Ref.current.position.y = separation * Math.sin(t);
        star2Ref.current.position.x = -separation * Math.cos(t);
        star2Ref.current.position.y = -separation * Math.sin(t);
      }
    }
  });

  // Tether endpoint (toward boundary)
  const tetherEnd = useMemo(() => {
    if (!showTether) return null;
    const dir = binary.topological_tether.direction_vector;
    // Draw tether toward boundary (scaled down for visualization)
    return new THREE.Vector3(
      dir[0] * 5,
      dir[1] * 5,
      dir[2] * 5
    );
  }, [binary.topological_tether, showTether]);

  return (
    <group ref={groupRef} position={position}>
      {/* Primary star */}
      <mesh ref={star1Ref}>
        <sphereGeometry args={[star1Size, 16, 16]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={0.8}
        />
      </mesh>

      {/* Secondary star */}
      <mesh ref={star2Ref}>
        <sphereGeometry args={[star2Size, 16, 16]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={0.6}
        />
      </mesh>

      {/* Orbital ring */}
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <ringGeometry args={[separation - 0.01, separation + 0.01, 32]} />
        <meshBasicMaterial color={color} transparent opacity={0.3} side={THREE.DoubleSide} />
      </mesh>

      {/* Topological tether */}
      {showTether && tetherEnd && (
        <Line
          points={[new THREE.Vector3(0, 0, 0), tetherEnd]}
          color="#FFD700"
          lineWidth={1}
          transparent
          opacity={0.2}
          dashed
          dashSize={0.1}
          dashScale={10}
        />
      )}

      {/* Label */}
      <Text
        position={[0, separation + 0.15, 0]}
        fontSize={0.06}
        color={color}
        anchorX="center"
      >
        {binary.observed_boost.toFixed(2)}x
      </Text>
    </group>
  );
}

/**
 * Main Local MOND Anchor visualization
 */
export function LocalMONDAnchor({
  opacity = 1,
  showTethers = true,
  selectedRegime = 'all',
}: LocalMONDAnchorProps) {
  const [data, setData] = useState<BinaryData | null>(null);
  const groupRef = useRef<THREE.Group>(null);

  // Load data
  useEffect(() => {
    fetch('/data/wide_binary_data.json')
      .then(res => res.json())
      .then((loadedData: BinaryData) => {
        setData(loadedData);
      })
      .catch(console.error);
  }, []);

  // Filter binaries
  const filteredBinaries = useMemo(() => {
    if (!data) return [];
    if (selectedRegime === 'all') return data.binaries;
    return data.binaries.filter(b => b.regime === selectedRegime);
  }, [data, selectedRegime]);

  // Slow rotation
  useFrame(({ clock }) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = clock.getElapsedTime() * 0.05;
    }
  });

  if (!data) return null;

  return (
    <group ref={groupRef}>
      {/* Milky Way center marker */}
      <mesh>
        <sphereGeometry args={[0.2, 32, 32]} />
        <meshStandardMaterial
          color="#FFD700"
          emissive="#FFD700"
          emissiveIntensity={0.3}
          transparent
          opacity={0.5}
        />
      </mesh>
      <Text
        position={[0, 0.4, 0]}
        fontSize={0.12}
        color="#FFD700"
        anchorX="center"
      >
        Milky Way
      </Text>

      {/* Wide binaries */}
      {filteredBinaries.map((binary, i) => (
        <WideBinaryPair
          key={binary.name || i}
          binary={binary}
          index={i}
          showTether={showTethers}
        />
      ))}

      {/* Legend */}
      <group position={[-3, 2, 0]}>
        <Text position={[0, 0.3, 0]} fontSize={0.1} color="#fff" anchorX="left">
          MOND Regime:
        </Text>
        <mesh position={[0, 0, 0]}>
          <sphereGeometry args={[0.05, 8, 8]} />
          <meshBasicMaterial color={REGIME_COLORS.deep_mond} />
        </mesh>
        <Text position={[0.15, 0, 0]} fontSize={0.08} color={REGIME_COLORS.deep_mond} anchorX="left">
          Deep MOND
        </Text>
        <mesh position={[0, -0.15, 0]}>
          <sphereGeometry args={[0.05, 8, 8]} />
          <meshBasicMaterial color={REGIME_COLORS.transitional} />
        </mesh>
        <Text position={[0.15, -0.15, 0]} fontSize={0.08} color={REGIME_COLORS.transitional} anchorX="left">
          Transitional
        </Text>
        <mesh position={[0, -0.3, 0]}>
          <sphereGeometry args={[0.05, 8, 8]} />
          <meshBasicMaterial color={REGIME_COLORS.newtonian} />
        </mesh>
        <Text position={[0.15, -0.3, 0]} fontSize={0.08} color={REGIME_COLORS.newtonian} anchorX="left">
          Newtonian
        </Text>
      </group>
    </group>
  );
}

/**
 * HUD overlay for Wide Binary statistics
 */
export function WideBinaryHUD({
  deepMondCount = 0,
  transitionalCount = 0,
  newtonianCount = 0,
  meanBoostDeepMond = 0,
  meanBoostNewtonian = 0,
}: {
  deepMondCount?: number;
  transitionalCount?: number;
  newtonianCount?: number;
  meanBoostDeepMond?: number;
  meanBoostNewtonian?: number;
}) {
  return (
    <div style={{
      position: 'absolute',
      top: '120px',
      right: '20px',
      background: 'rgba(0,0,0,0.7)',
      padding: '15px',
      borderRadius: '8px',
      fontFamily: 'monospace',
      fontSize: '12px',
      color: '#fff',
      minWidth: '200px',
      border: '1px solid #333',
    }}>
      <div style={{ marginBottom: '10px', fontWeight: 'bold', color: '#2ECC71' }}>
        LOCAL MOND ANCHOR
      </div>

      <div style={{ marginBottom: '5px' }}>
        <span style={{ color: REGIME_COLORS.deep_mond }}>Deep MOND:</span> {deepMondCount}
      </div>
      <div style={{ marginBottom: '5px' }}>
        <span style={{ color: REGIME_COLORS.transitional }}>Transitional:</span> {transitionalCount}
      </div>
      <div style={{ marginBottom: '5px' }}>
        <span style={{ color: REGIME_COLORS.newtonian }}>Newtonian:</span> {newtonianCount}
      </div>

      <div style={{
        marginTop: '10px',
        paddingTop: '10px',
        borderTop: '1px solid #444',
        fontSize: '11px',
      }}>
        <div style={{ marginBottom: '5px' }}>
          <span style={{ color: '#2ECC71' }}>Deep MOND boost:</span> {meanBoostDeepMond.toFixed(2)}x
        </div>
        <div style={{ marginBottom: '5px' }}>
          <span style={{ color: '#9B59B6' }}>Newtonian boost:</span> {meanBoostNewtonian.toFixed(2)}x
        </div>
        <div style={{ marginTop: '8px', fontSize: '10px', color: '#FFD700' }}>
          a₀ = 1.2×10⁻¹⁰ m/s²
        </div>
        <div style={{ fontSize: '9px', color: '#666', marginTop: '3px' }}>
          T³ volume ➔ local gravity
        </div>
      </div>
    </div>
  );
}

export default LocalMONDAnchor;
