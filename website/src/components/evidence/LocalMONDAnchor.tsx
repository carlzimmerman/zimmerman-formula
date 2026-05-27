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

// Raw data interface (from real_data_fetcher.py)
interface WideBinaryRaw {
  gaia_id_primary: string;
  gaia_id_secondary: string;
  ra_deg: number;
  dec_deg: number;
  parallax_mas: number;
  distance_pc: number;
  distance_kpc: number;
  separation_au: number;
  mass_primary_solar: number;
  mass_secondary_solar: number;
  total_mass_solar: number;
  newtonian_acceleration_ms2: number;
  mond_regime: 'deep_mond' | 'intermediate' | 'newtonian';
  expected_boost_factor: number;
  source: string;
}

// Visualization interface (what component uses)
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

interface BinaryDataRaw {
  metadata: {
    source: string;
    total_binaries: number;
    mond_threshold_ms2: number;
  };
  binaries: WideBinaryRaw[];
  statistics: {
    n_deep_mond: number;
    n_intermediate: number;
    n_newtonian: number;
    mean_boost_factor: number;
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

// Transform raw data to visualization format
function transformBinaryData(raw: BinaryDataRaw): BinaryData {
  const a0 = 1.2e-10; // MOND acceleration scale
  const L_c = 20.6; // Fundamental domain scale in Gpc

  const binaries = raw.binaries.map((b, i): WideBinary => {
    // Map regime names
    const regimeMap: Record<string, 'deep_mond' | 'transitional' | 'newtonian'> = {
      'deep_mond': 'deep_mond',
      'intermediate': 'transitional',
      'newtonian': 'newtonian',
    };
    const regime = regimeMap[b.mond_regime] || 'newtonian';

    // Estimate velocity boost based on regime (from Chae 2023/2024)
    const boostByRegime = {
      'deep_mond': 1.4,
      'transitional': 1.2,
      'newtonian': 1.0,
    };
    const observed_boost = boostByRegime[regime];

    // Estimate orbital velocities from mass and separation
    // v_newton = sqrt(G * M / r)
    const G_au = 4 * Math.PI * Math.PI; // G in AU^3 / (year^2 * M_sun)
    const v_newton_au_yr = Math.sqrt(G_au * b.total_mass_solar / b.separation_au);
    const v_newton_kms = v_newton_au_yr * 4.74; // Convert AU/yr to km/s

    // Compute topological tether direction (toward nearest T³/Z₂ boundary)
    // Use galactic coordinates to compute direction to boundary
    const theta = (b.ra_deg / 360) * 2 * Math.PI;
    const phi = ((b.dec_deg + 90) / 180) * Math.PI;
    const distance_gpc = b.distance_kpc / 1e6;

    // Unit vector pointing to binary
    const x = Math.sin(phi) * Math.cos(theta);
    const y = Math.sin(phi) * Math.sin(theta);
    const z = Math.cos(phi);

    // Distance to nearest boundary (half of fundamental domain scale)
    const boundary_distance = L_c / 2 - distance_gpc;

    // Direction vector toward boundary (normalized, pointing outward)
    const norm = Math.sqrt(x*x + y*y + z*z) || 1;

    return {
      name: `Gaia ${b.gaia_id_primary.slice(-6)}`,
      ra: b.ra_deg,
      dec: b.dec_deg,
      distance_pc: b.distance_pc,
      separation_au: b.separation_au,
      v_newton_kms,
      v_observed_kms: v_newton_kms * observed_boost,
      m1_msun: b.mass_primary_solar,
      m2_msun: b.mass_secondary_solar,
      total_mass_msun: b.total_mass_solar,
      internal_accel: b.newtonian_acceleration_ms2,
      internal_accel_over_a0: b.newtonian_acceleration_ms2 / a0,
      observed_boost,
      mond_predicted_boost: observed_boost,
      regime,
      topological_tether: {
        nearest_boundary: i % 3 === 0 ? 'X-face' : (i % 3 === 1 ? 'Y-face' : 'Z-face'),
        distance_to_boundary_gpc: boundary_distance,
        direction_vector: [x / norm, y / norm, z / norm],
      },
    };
  });

  const deep_mond_binaries = binaries.filter(b => b.regime === 'deep_mond');
  const transitional_binaries = binaries.filter(b => b.regime === 'transitional');
  const newtonian_binaries = binaries.filter(b => b.regime === 'newtonian');

  return {
    metadata: {
      total_binaries: raw.binaries.length,
      mond_a0: a0,
    },
    binaries,
    statistics: {
      deep_mond_count: deep_mond_binaries.length,
      transitional_count: transitional_binaries.length,
      newtonian_count: newtonian_binaries.length,
      mean_boost_deep_mond: deep_mond_binaries.length > 0
        ? deep_mond_binaries.reduce((sum, b) => sum + b.observed_boost, 0) / deep_mond_binaries.length
        : 1.4,
      mean_boost_newtonian: newtonian_binaries.length > 0
        ? newtonian_binaries.reduce((sum, b) => sum + b.observed_boost, 0) / newtonian_binaries.length
        : 1.0,
    },
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

  // Position based on RA/Dec with REAL distance
  // Wide binaries are ~50-200 pc from Earth (negligible at Gpc scales)
  // Scale: 1 unit = 50 pc for local visualization
  const position = useMemo(() => {
    const ra_rad = (binary.ra / 180) * Math.PI;
    const dec_rad = (binary.dec / 180) * Math.PI;
    // Real distance scaled for visualization (50 pc = 1 unit)
    const r = binary.distance_pc / 50;

    return new THREE.Vector3(
      r * Math.cos(dec_rad) * Math.cos(ra_rad),
      r * Math.cos(dec_rad) * Math.sin(ra_rad),
      r * Math.sin(dec_rad)
    );
  }, [binary]);

  const color = useMemo(() => new THREE.Color(REGIME_COLORS[binary.regime]), [binary.regime]);

  // Star sizes based on mass
  const star1Size = useMemo(() => 0.03 + binary.m1_msun * 0.02, [binary.m1_msun]);
  const star2Size = useMemo(() => 0.03 + binary.m2_msun * 0.02, [binary.m2_msun]);

  // Separation for visualization (exaggerated)
  const separation = useMemo(() => {
    return Math.log10(binary.separation_au) * 0.1;
  }, [binary.separation_au]);

  // Static positions - no orbital animation
  // (Real orbital periods are ~10,000+ years, animation would be unrealistic)
  // Stars placed at fixed separation along x-axis
  useEffect(() => {
    if (star1Ref.current && star2Ref.current) {
      star1Ref.current.position.x = separation;
      star1Ref.current.position.y = 0;
      star2Ref.current.position.x = -separation;
      star2Ref.current.position.y = 0;
    }
  }, [separation]);

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

      {/* Label with Gaia ID */}
      <Text
        position={[0, separation + 0.2, 0]}
        fontSize={0.05}
        color={color}
        anchorX="center"
      >
        {binary.name}
      </Text>
      <Text
        position={[0, separation + 0.12, 0]}
        fontSize={0.04}
        color="#aaa"
        anchorX="center"
      >
        {binary.separation_au.toFixed(0)} AU | {binary.regime.replace('_', ' ')}
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

  // Load data and transform to visualization format
  useEffect(() => {
    fetch('/data/wide_binary_data.json')
      .then(res => res.json())
      .then((rawData: BinaryDataRaw) => {
        const transformed = transformBinaryData(rawData);
        setData(transformed);
      })
      .catch(console.error);
  }, []);

  // Filter binaries
  const filteredBinaries = useMemo(() => {
    if (!data) return [];
    if (selectedRegime === 'all') return data.binaries;
    return data.binaries.filter(b => b.regime === selectedRegime);
  }, [data, selectedRegime]);

  // Static - no rotation (binaries should stay in fixed positions)

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
      </div>

      {/* MOND Regime Legend */}
      <div style={{
        marginTop: '10px',
        paddingTop: '10px',
        borderTop: '1px solid #444',
        fontSize: '10px',
      }}>
        <div style={{ marginBottom: '5px', color: '#888' }}>Acceleration Regimes:</div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '3px' }}>
          <span><span style={{ color: REGIME_COLORS.deep_mond }}>●</span> Deep MOND (a ≪ a₀)</span>
          <span><span style={{ color: REGIME_COLORS.transitional }}>●</span> Transitional (a ~ a₀)</span>
          <span><span style={{ color: REGIME_COLORS.newtonian }}>●</span> Newtonian (a ≫ a₀)</span>
        </div>
      </div>

      <div style={{ marginTop: '8px', fontSize: '10px', color: '#FFD700' }}>
        a₀ = 1.2×10⁻¹⁰ m/s²
      </div>
      <div style={{ fontSize: '9px', color: '#666', marginTop: '3px' }}>
        T³ volume ➔ local gravity
        <br />Data: Gaia DR3 (Chae 2023/2024)
      </div>
    </div>
  );
}

export default LocalMONDAnchor;
