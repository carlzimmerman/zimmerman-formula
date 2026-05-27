/**
 * =============================================================================
 * COSMIC WIND SHADER - kSZ Galaxy Cluster Visualization
 * =============================================================================
 *
 * Directive YYYY: Visualize galaxy clusters with measured line-of-sight
 * velocities from kSZ effect measurements.
 *
 * REAL DATA ONLY:
 * - Galaxy cluster positions from Planck SZ + ACT catalogs
 * - Cluster masses from SZ/X-ray scaling relations
 * - Line-of-sight velocities from kSZ measurements (Bullet, El Gordo)
 *   or bulk flow models (nearby clusters)
 * - Cosmic wind vector derived from cluster velocity field
 *
 * NO SIMULATED ELEMENTS - removed CMB photon particle animation
 * (photon trajectories were conceptual, not real data)
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
const COLORS = {
  blueshift: '#4444FF',
  redshift: '#FF4444',
  neutral: '#88FF88',
  cluster: '#FFD700',
};

// Interfaces
interface Cluster {
  name: string;
  ra: number;
  dec: number;
  galactic_l: number;
  galactic_b: number;
  distance_gpc: number;
  position: { x: number; y: number; z: number };
  v_los_kms: number;
  direction: 'toward' | 'away';
  ksz_amplitude_uk: number;
  mass_1e14_msun: number;
}

interface CosmicWind {
  magnitude_kms: number;
  direction_l: number;
  direction_b: number;
  cartesian: number[];
}

interface KSZData {
  metadata: {
    total_clusters: number;
  };
  clusters: Cluster[];
  cosmic_wind: CosmicWind;
  boundary_alignment: {
    best_aligned_axis: string;
    best_alignment_angle: number;
  };
}

interface CosmicWindShaderProps {
  opacity?: number;
  showWind?: boolean;
}

// CMB Photon simulation REMOVED - was not based on real data
// (100 randomly generated particles were conceptual visualization only)

/**
 * Galaxy cluster marker - REAL DATA
 * Position from Planck/ACT catalogs, size scaled by mass, color by velocity direction
 */
function ClusterMarker({ cluster }: { cluster: Cluster }) {
  const position = useMemo(() => new THREE.Vector3(
    cluster.position.x * SCALE,
    cluster.position.y * SCALE,
    cluster.position.z * SCALE
  ), [cluster]);

  // Size scaled by cluster mass (real measurement)
  const size = useMemo(() => {
    return 0.05 + cluster.mass_1e14_msun * 0.003;
  }, [cluster.mass_1e14_msun]);

  // Color indicates line-of-sight velocity direction (real measurement)
  const color = useMemo(() => {
    return cluster.direction === 'toward' ? COLORS.blueshift : COLORS.redshift;
  }, [cluster.direction]);

  // Static - no pulsing animation (kSZ amplitude is a measurement, not a pulsation)

  return (
    <group position={position}>
      <mesh>
        <sphereGeometry args={[size, 12, 12]} />
        <meshStandardMaterial
          color={COLORS.cluster}
          emissive={color}
          emissiveIntensity={0.5}
        />
      </mesh>
      <mesh>
        <sphereGeometry args={[size * 2, 12, 12]} />
        <meshBasicMaterial
          color={color}
          transparent
          opacity={0.1}
          side={THREE.BackSide}
        />
      </mesh>
    </group>
  );
}

/**
 * Cosmic Wind vector arrow
 */
function CosmicWindArrow({ wind }: { wind: CosmicWind }) {
  const direction = useMemo(() => {
    const normalized = new THREE.Vector3(
      wind.cartesian[0],
      wind.cartesian[1],
      wind.cartesian[2]
    ).normalize();
    return normalized.multiplyScalar(3);
  }, [wind]);

  return (
    <group>
      <Line
        points={[new THREE.Vector3(0, 0, 0), direction]}
        color="#FFD700"
        lineWidth={3}
      />
      <mesh position={direction}>
        <coneGeometry args={[0.1, 0.3, 8]} />
        <meshStandardMaterial
          color="#FFD700"
          emissive="#FFD700"
          emissiveIntensity={0.5}
        />
      </mesh>
      <Text
        position={direction.clone().multiplyScalar(1.2)}
        fontSize={0.12}
        color="#FFD700"
        anchorX="center"
      >
        {`${wind.magnitude_kms.toFixed(0)} km/s`}
      </Text>
    </group>
  );
}

/**
 * Main Cosmic Wind visualization - REAL DATA ONLY
 * Shows galaxy clusters at measured positions with velocity directions
 */
export function CosmicWindShader({
  opacity = 1,
  showWind = true,
}: CosmicWindShaderProps) {
  const [data, setData] = useState<KSZData | null>(null);

  // Load real cluster data
  useEffect(() => {
    fetch('/data/ksz_cosmic_wind_data.json')
      .then(res => res.json())
      .then((loadedData: KSZData) => {
        setData(loadedData);
      })
      .catch(console.error);
  }, []);

  // Static - no group rotation (clusters are at fixed positions)

  if (!data) return null;

  return (
    <group>
      {/* Earth at center (observer position) */}
      <mesh>
        <sphereGeometry args={[0.08, 16, 16]} />
        <meshStandardMaterial
          color="#4444FF"
          emissive="#4444FF"
          emissiveIntensity={0.3}
        />
      </mesh>

      {/* Cluster markers - REAL positions from Planck/ACT catalogs */}
      {data.clusters.map((cluster, i) => (
        <ClusterMarker key={cluster.name || i} cluster={cluster} />
      ))}

      {/* Cosmic Wind vector - derived from cluster velocity field */}
      {showWind && <CosmicWindArrow wind={data.cosmic_wind} />}

      {/* Fundamental domain frame */}
      <lineSegments>
        <edgesGeometry args={[new THREE.BoxGeometry(L_C * SCALE, L_C * SCALE, L_C * SCALE)]} />
        <lineBasicMaterial color="#333" transparent opacity={0.2} />
      </lineSegments>
    </group>
  );
}

/**
 * HUD overlay for kSZ Cosmic Wind statistics
 */
export function CosmicWindHUD({
  totalClusters = 0,
  windMagnitude = 0,
  windDirection = { l: 0, b: 0 },
  bestAxis = 'Y',
  alignmentAngle = 0,
}: {
  totalClusters?: number;
  windMagnitude?: number;
  windDirection?: { l: number; b: number };
  bestAxis?: string;
  alignmentAngle?: number;
}) {
  return (
    <div style={{
      position: 'absolute',
      top: '440px',
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
      <div style={{ marginBottom: '10px', fontWeight: 'bold', color: '#FFD700' }}>
        kSZ COSMIC WIND
      </div>

      <div style={{ marginBottom: '5px' }}>
        Clusters: {totalClusters}
      </div>
      <div style={{ marginBottom: '5px', color: '#FFD700' }}>
        Wind: {windMagnitude.toFixed(0)} km/s
      </div>
      <div style={{ marginBottom: '5px', fontSize: '10px' }}>
        (l={windDirection.l.toFixed(0)}°, b={windDirection.b.toFixed(0)}°)
      </div>

      <div style={{
        marginTop: '10px',
        paddingTop: '10px',
        borderTop: '1px solid #444',
        fontSize: '11px',
      }}>
        <div style={{ marginBottom: '5px' }}>
          Aligned: <span style={{ color: '#2ECC71' }}>{bestAxis}-axis</span>
        </div>
        <div style={{ marginBottom: '5px' }}>
          Angle: {alignmentAngle.toFixed(1)}°
        </div>
        <div style={{ fontSize: '9px', color: '#666', marginTop: '5px' }}>
          <span style={{ color: '#4444FF' }}>Blue</span>=toward,{' '}
          <span style={{ color: '#FF4444' }}>Red</span>=away
        </div>
      </div>
    </div>
  );
}

export default CosmicWindShader;
