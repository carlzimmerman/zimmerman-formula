/**
 * =============================================================================
 * DISPERSION TOMOGRAPHY - FRB Cubic Anisotropy Visualization
 * =============================================================================
 *
 * Directive XXXX: Visualize CHIME FRB dispersion measures as volumetric
 * rays probing the intergalactic medium, testing for cubic anisotropy.
 *
 * Features:
 * - FRB markers as pulsing strobes
 * - Dispersion cones from FRB to Earth
 * - Color-coded by DM (matter density)
 * - Direction classification (axis vs diagonal)
 *
 * =============================================================================
 */

import React, { useMemo, useState, useEffect } from 'react';
import * as THREE from 'three';
import { Line, Text } from '@react-three/drei';

// Constants
const L_C = 20.6;
const HALF_BOX = L_C / 2;
const SCALE = 0.3;

// Color scheme
const DM_COLORS = {
  low: '#4ECDC4',   // Teal - sparse
  medium: '#F39C12', // Orange
  high: '#FF6B6B',  // Red - dense
};

// Interfaces
interface FRB {
  name: string;
  ra: number;
  dec: number;
  galactic_l: number;
  galactic_b: number;
  dm_observed: number;
  dm_cosmic: number;
  redshift: number | null;
  distance_gpc: number | null;
  position: { x: number; y: number; z: number } | null;
  repeater: boolean;
  direction_type: 'axis' | 'diagonal' | 'intermediate';
  nearest_axis: string | null;
}

interface FRBData {
  metadata: {
    total_frbs: number;
  };
  frbs: FRB[];
  anisotropy_analysis: {
    n_axis: number;
    n_diagonal: number;
    mean_dm_per_z_axis: number | null;
    mean_dm_per_z_diagonal: number | null;
    anisotropy_ratio: number | null;
  };
}

interface DispersionTomographyProps {
  opacity?: number;
  showCones?: boolean;
}

/**
 * Single FRB marker - REAL DATA
 * Position from CHIME/DSA-110/ASKAP catalogs, color by dispersion measure
 */
function FRBMarker({
  frb,
}: {
  frb: FRB;
}) {
  // Position from catalog
  const position = useMemo(() => {
    if (frb.position) {
      return new THREE.Vector3(
        frb.position.x * SCALE,
        frb.position.y * SCALE,
        frb.position.z * SCALE
      );
    }
    // Fallback: use angular position on sphere
    const l = frb.galactic_l * Math.PI / 180;
    const b = frb.galactic_b * Math.PI / 180;
    const r = (frb.distance_gpc || 2) * SCALE;
    return new THREE.Vector3(
      r * Math.cos(b) * Math.cos(l),
      r * Math.cos(b) * Math.sin(l),
      r * Math.sin(b)
    );
  }, [frb]);

  // Color based on DM (real measurement)
  const color = useMemo(() => {
    const dm = frb.dm_cosmic;
    if (dm < 200) return new THREE.Color(DM_COLORS.low);
    if (dm < 600) return new THREE.Color(DM_COLORS.medium);
    return new THREE.Color(DM_COLORS.high);
  }, [frb.dm_cosmic]);

  // Size: repeaters slightly larger (real property)
  const size = useMemo(() => {
    return frb.repeater ? 0.08 : 0.05;
  }, [frb.repeater]);

  // Static - no flash animation
  // (Real FRB bursts are milliseconds, not observable in this visualization timescale)

  return (
    <group position={position}>
      {/* Core marker */}
      <mesh>
        <sphereGeometry args={[size, 12, 12]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={0.8}
        />
      </mesh>

      {/* Glow */}
      <mesh>
        <sphereGeometry args={[size * 3, 12, 12]} />
        <meshBasicMaterial
          color={color}
          transparent
          opacity={0.15}
          side={THREE.BackSide}
        />
      </mesh>

      {/* Line to Earth - shows sightline through IGM */}
      <Line
        points={[new THREE.Vector3(0, 0, 0), position.clone().negate()]}
        color={color}
        lineWidth={1}
        transparent
        opacity={0.2}
        dashed
        dashSize={0.1}
        dashScale={5}
      />
    </group>
  );
}

/**
 * Main Dispersion Tomography visualization
 */
export function DispersionTomography({
  opacity = 1,
  showCones = true,
}: DispersionTomographyProps) {
  const [data, setData] = useState<FRBData | null>(null);

  // Load real FRB data
  useEffect(() => {
    fetch('/data/frb_dispersion_data.json')
      .then(res => res.json())
      .then((loadedData: FRBData) => {
        setData(loadedData);
      })
      .catch(console.error);
  }, []);

  // Static - no group rotation (FRBs are at fixed sky positions)

  if (!data) return null;

  return (
    <group>
      {/* Earth marker at center (observer position) */}
      <mesh>
        <sphereGeometry args={[0.05, 16, 16]} />
        <meshStandardMaterial
          color="#4444FF"
          emissive="#4444FF"
          emissiveIntensity={0.5}
        />
      </mesh>
      <Text
        position={[0, 0.15, 0]}
        fontSize={0.08}
        color="#4444FF"
        anchorX="center"
      >
        Earth
      </Text>

      {/* FRB markers - REAL positions from CHIME/DSA-110/ASKAP */}
      {data.frbs.map((frb, i) => (
        <FRBMarker
          key={frb.name || i}
          frb={frb}
        />
      ))}

      {/* T³ axis indicators */}
      <Line
        points={[new THREE.Vector3(-3, 0, 0), new THREE.Vector3(3, 0, 0)]}
        color="#FF4444"
        lineWidth={1}
        transparent
        opacity={0.3}
      />
      <Text position={[3.2, 0, 0]} fontSize={0.1} color="#FF4444">X</Text>

      <Line
        points={[new THREE.Vector3(0, -3, 0), new THREE.Vector3(0, 3, 0)]}
        color="#44FF44"
        lineWidth={1}
        transparent
        opacity={0.3}
      />
      <Text position={[0, 3.2, 0]} fontSize={0.1} color="#44FF44">Y</Text>

      <Line
        points={[new THREE.Vector3(0, 0, -3), new THREE.Vector3(0, 0, 3)]}
        color="#4444FF"
        lineWidth={1}
        transparent
        opacity={0.3}
      />
      <Text position={[0, 0, 3.2]} fontSize={0.1} color="#4444FF">Z</Text>

      {/* Fundamental domain wireframe */}
      <lineSegments>
        <edgesGeometry args={[new THREE.BoxGeometry(L_C * SCALE, L_C * SCALE, L_C * SCALE)]} />
        <lineBasicMaterial color="#333" transparent opacity={0.2} />
      </lineSegments>
    </group>
  );
}

/**
 * HUD overlay for FRB Dispersion statistics
 */
export function DispersionHUD({
  totalFRBs = 0,
  axisCount = 0,
  diagonalCount = 0,
  anisotropyRatio = 0,
  maxDM = 0,
}: {
  totalFRBs?: number;
  axisCount?: number;
  diagonalCount?: number;
  anisotropyRatio?: number;
  maxDM?: number;
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
      <div style={{ marginBottom: '10px', fontWeight: 'bold', color: '#4ECDC4' }}>
        FRB DISPERSION MAP
      </div>

      <div style={{ marginBottom: '5px' }}>
        Total FRBs: {totalFRBs}
      </div>
      <div style={{ marginBottom: '5px' }}>
        <span style={{ color: '#FF4444' }}>Along axes:</span> {axisCount}
      </div>
      <div style={{ marginBottom: '5px' }}>
        <span style={{ color: '#FFFF44' }}>Along diagonals:</span> {diagonalCount}
      </div>

      <div style={{
        marginTop: '10px',
        paddingTop: '10px',
        borderTop: '1px solid #444',
        fontSize: '11px',
      }}>
        <div style={{ marginBottom: '5px', color: '#FFD700' }}>
          Anisotropy: {anisotropyRatio.toFixed(2)}
        </div>
        <div style={{ marginBottom: '5px' }}>
          Max DM: {maxDM} pc/cm³
        </div>
      </div>

      {/* DM Color Legend */}
      <div style={{
        marginTop: '10px',
        paddingTop: '10px',
        borderTop: '1px solid #444',
        fontSize: '10px',
      }}>
        <div style={{ marginBottom: '5px', color: '#888' }}>Dispersion Measure:</div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '3px' }}>
          <span><span style={{ color: '#4ECDC4' }}>●</span> Low DM (&lt;200 pc/cm³)</span>
          <span><span style={{ color: '#F39C12' }}>●</span> Medium DM (200-600)</span>
          <span><span style={{ color: '#FF6B6B' }}>●</span> High DM (&gt;600 pc/cm³)</span>
        </div>
      </div>

      {/* Direction Legend */}
      <div style={{
        marginTop: '8px',
        fontSize: '10px',
      }}>
        <div style={{ marginBottom: '5px', color: '#888' }}>Sightline Direction:</div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <span style={{ color: '#FF4444' }}>— X</span>
          <span style={{ color: '#44FF44' }}>— Y</span>
          <span style={{ color: '#4444FF' }}>— Z</span>
        </div>
      </div>

      <div style={{ fontSize: '9px', color: '#666', marginTop: '8px' }}>
        DM along axes vs diagonals
        <br />tests cubic geometry
        <br />Data: CHIME / DSA-110 / ASKAP
      </div>
    </div>
  );
}

export default DispersionTomography;
