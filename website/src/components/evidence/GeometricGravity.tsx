/**
 * =============================================================================
 * GEOMETRIC GRAVITY - COWLS Strong Lensing Visualization
 * =============================================================================
 *
 * Directive UUUU: Visualize JWST COSMOS-Web strong lenses with MOND analysis.
 * Now uses REAL data from COWLS (COSMOS-Web Lens Survey) 2025 public release.
 *
 * Features:
 * - Individual strong lens markers at real positions
 * - Einstein radius visualization
 * - MOND regime coloring (green=deep MOND, orange=transition, purple=Newtonian)
 * - Source/lens redshift display
 *
 * =============================================================================
 */

import React, { useMemo, useState, useEffect } from 'react';
import * as THREE from 'three';
import { Text, Line } from '@react-three/drei';

// =============================================================================
// INTERFACES
// =============================================================================

interface Lens {
  name: string;
  ra: number;
  dec: number;
  galactic_l: number;
  galactic_b: number;
  z_lens: number;
  z_source: number;
  einstein_radius_arcsec: number;
  distance_gpc: number;
  position: { x: number; y: number; z: number };
  velocity_dispersion_kms: number;
  mond_regime: 'deep_mond' | 'transition' | 'newtonian';
  source: string;
}

interface LensingData {
  metadata: {
    source: string;
    total_lenses: number;
    survey_area_sq_deg: number;
    data_integrity: string;
    references: string[];
  };
  lenses: Lens[];
  statistics: {
    n_deep_mond: number;
    n_transition: number;
    n_newtonian: number;
    mean_einstein_radius: number;
    max_source_redshift: number;
  };
}

interface GeometricGravityProps {
  opacity?: number;
  showMOND?: boolean;
  showLabels?: boolean;
  position?: [number, number, number];
  scale?: number;
}

// Color scheme for MOND regimes
const REGIME_COLORS = {
  deep_mond: '#2ECC71',     // Green
  transition: '#F39C12',    // Orange
  newtonian: '#9B59B6',     // Purple
};

// =============================================================================
// COMPONENTS
// =============================================================================

/**
 * Individual lens marker - REAL DATA from JWST COSMOS-Web
 * Position from catalog, color by MOND regime, ring by Einstein radius
 */
function LensMarker({
  lens,
  scale = 1,
  showLabel = true,
}: {
  lens: Lens;
  scale: number;
  showLabel?: boolean;
}) {
  // Position from real catalog coordinates
  // COSMOS field is ~0.7 deg across, center at 150.1°, 2.3°
  const position = useMemo(() => {
    const ra_offset = (lens.ra - 150.1) * 10 * scale;  // Convert deg to viz units
    const dec_offset = (lens.dec - 2.3) * 10 * scale;
    const z_offset = lens.z_lens * 0.5 * scale;  // Stack by redshift
    return new THREE.Vector3(ra_offset, z_offset, dec_offset);
  }, [lens, scale]);

  // Ring size based on Einstein radius (real measurement)
  const ringSize = useMemo(() => {
    return 0.05 + lens.einstein_radius_arcsec * 0.1;
  }, [lens.einstein_radius_arcsec]);

  // Color by MOND regime (derived from velocity dispersion)
  const color = useMemo(() => {
    return new THREE.Color(REGIME_COLORS[lens.mond_regime]);
  }, [lens.mond_regime]);

  // Static - no pulsing or rotation (lens positions are fixed measurements)

  return (
    <group position={position}>
      {/* Lens galaxy marker */}
      <mesh>
        <sphereGeometry args={[0.08 * scale, 12, 12]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={0.4}
          roughness={0.3}
          metalness={0.7}
        />
      </mesh>

      {/* Einstein ring - static (shows measured Einstein radius) */}
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <ringGeometry args={[ringSize * 0.9, ringSize * 1.1, 32]} />
        <meshBasicMaterial
          color={color}
          transparent
          opacity={0.4}
          side={THREE.DoubleSide}
        />
      </mesh>

      {/* Glow */}
      <mesh>
        <sphereGeometry args={[0.15 * scale, 12, 12]} />
        <meshBasicMaterial
          color={color}
          transparent
          opacity={0.15}
          side={THREE.BackSide}
        />
      </mesh>

      {/* Labels */}
      {showLabel && (
        <>
          <Text
            position={[0, 0.2 * scale, 0]}
            fontSize={0.06 * scale}
            color={color}
            anchorX="center"
          >
            {lens.name}
          </Text>
          <Text
            position={[0, 0.12 * scale, 0]}
            fontSize={0.04 * scale}
            color="#888"
            anchorX="center"
          >
            {`z_s=${lens.z_source.toFixed(1)}`}
          </Text>
        </>
      )}

      {/* Source indicator (behind lens) */}
      <mesh position={[0, 0, -0.3 * scale]}>
        <circleGeometry args={[0.03 * scale, 16]} />
        <meshBasicMaterial color="#FFF" transparent opacity={0.3} />
      </mesh>
    </group>
  );
}

/**
 * Main Geometric Gravity visualization
 */
export function GeometricGravity({
  opacity = 1,
  showMOND = true,
  showLabels = true,
  position = [0, 0, 0],
  scale = 3,
}: GeometricGravityProps) {
  const [data, setData] = useState<LensingData | null>(null);

  // Load real COWLS lens data
  useEffect(() => {
    fetch('/data/cosmos_lensing_data.json')
      .then(res => res.json())
      .then((loadedData: LensingData) => {
        setData(loadedData);
      })
      .catch(console.error);
  }, []);

  // Static - no group rotation (lenses are at fixed sky positions)

  if (!data) return null;

  return (
    <group position={position}>
      {/* Lens markers */}
      {data.lenses.map((lens, i) => (
        <LensMarker
          key={lens.name || i}
          lens={lens}
          scale={scale / 3}
          showLabel={showLabels}
        />
      ))}

      {/* Survey field boundary */}
      <Line
        points={[
          [-scale/2, 0, -scale/2],
          [scale/2, 0, -scale/2],
          [scale/2, 0, scale/2],
          [-scale/2, 0, scale/2],
          [-scale/2, 0, -scale/2],
        ]}
        color="#333"
        lineWidth={1}
      />

      {/* Redshift axis */}
      <Line
        points={[
          [0, 0, 0],
          [0, scale * 0.8, 0],
        ]}
        color="#444"
        lineWidth={1}
        dashed
        dashSize={0.1}
      />
      <Text
        position={[0, scale * 0.85, 0]}
        fontSize={0.08}
        color="#666"
        anchorX="center"
      >
        z (redshift)
      </Text>

      {/* Legend */}
      <group position={[-scale/2 - 0.5, 0, 0]}>
        <mesh position={[0, 0.3, 0]}>
          <sphereGeometry args={[0.05, 8, 8]} />
          <meshBasicMaterial color={REGIME_COLORS.deep_mond} />
        </mesh>
        <Text position={[0.15, 0.3, 0]} fontSize={0.06} color={REGIME_COLORS.deep_mond} anchorX="left">
          Deep MOND
        </Text>

        <mesh position={[0, 0.15, 0]}>
          <sphereGeometry args={[0.05, 8, 8]} />
          <meshBasicMaterial color={REGIME_COLORS.transition} />
        </mesh>
        <Text position={[0.15, 0.15, 0]} fontSize={0.06} color={REGIME_COLORS.transition} anchorX="left">
          Transition
        </Text>

        <mesh position={[0, 0, 0]}>
          <sphereGeometry args={[0.05, 8, 8]} />
          <meshBasicMaterial color={REGIME_COLORS.newtonian} />
        </mesh>
        <Text position={[0.15, 0, 0]} fontSize={0.06} color={REGIME_COLORS.newtonian} anchorX="left">
          Newtonian
        </Text>
      </group>

      {/* Field label */}
      <Text
        position={[0, -0.3, scale/2 + 0.3]}
        fontSize={0.1}
        color="#888"
        anchorX="center"
      >
        COWLS / COSMOS-Web (0.54 deg²)
      </Text>
      <Text
        position={[0, -0.45, scale/2 + 0.3]}
        fontSize={0.07}
        color="#666"
        anchorX="center"
      >
        REAL JWST Strong Lens Data
      </Text>
    </group>
  );
}

/**
 * HUD overlay for MOND statistics
 */
export function MONDHUD({
  totalLenses = 0,
  deepMONDCount = 0,
  transitionCount = 0,
  newtonianCount = 0,
  maxSourceRedshift = 0,
}: {
  totalLenses?: number;
  deepMONDCount?: number;
  transitionCount?: number;
  newtonianCount?: number;
  maxSourceRedshift?: number;
}) {
  return (
    <div style={{
      position: 'absolute',
      top: '280px',
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
        COWLS STRONG LENSING
      </div>

      <div style={{ marginBottom: '5px' }}>
        Total Lenses: {totalLenses}
      </div>
      <div style={{ marginBottom: '5px' }}>
        <span style={{ color: '#2ECC71' }}>Deep MOND:</span> {deepMONDCount}
      </div>
      <div style={{ marginBottom: '5px' }}>
        <span style={{ color: '#F39C12' }}>Transition:</span> {transitionCount}
      </div>
      <div style={{ marginBottom: '5px' }}>
        <span style={{ color: '#9B59B6' }}>Newtonian:</span> {newtonianCount}
      </div>

      <div style={{
        marginTop: '10px',
        paddingTop: '10px',
        borderTop: '1px solid #444',
        fontSize: '11px',
      }}>
        <div style={{ color: '#4ECDC4' }}>
          Max z_source: {maxSourceRedshift.toFixed(1)}
        </div>
        <div style={{ marginTop: '5px', fontSize: '10px', color: '#666' }}>
          Data: JWST COSMOS-Web
          <br />a₀ = 1.2×10⁻¹⁰ m/s²
        </div>
      </div>
    </div>
  );
}

export default GeometricGravity;
