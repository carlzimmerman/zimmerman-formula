/**
 * =============================================================================
 * COSMIC WIND SHADER - kSZ Photon Collision Visualization
 * =============================================================================
 *
 * Directive YYYY: Visualize the kSZ effect as CMB photons colliding with
 * moving galaxy clusters, producing Doppler-shifted temperature fluctuations.
 *
 * Features:
 * - CMB photon particles from boundary
 * - Galaxy cluster markers
 * - Collision flashes with color shift
 * - Cosmic Wind vector overlay
 *
 * =============================================================================
 */

import React, { useRef, useMemo, useState, useEffect } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';
import { Line, Text } from '@react-three/drei';

// Constants
const L_C = 20.6;
const HALF_BOX = L_C / 2;
const SCALE = 0.3;
const PHOTON_SPEED = 0.02;
const NUM_PHOTONS = 100;

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
  showPhotons?: boolean;
  showWind?: boolean;
}

/**
 * CMB Photon particle
 */
function CMBPhoton({
  startPosition,
  clusters,
  onCollision,
}: {
  startPosition: THREE.Vector3;
  clusters: Cluster[];
  onCollision?: (cluster: Cluster) => void;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  const [color, setColor] = useState(new THREE.Color(COLORS.neutral));
  const [position, setPosition] = useState(startPosition.clone());
  const [hasCollided, setHasCollided] = useState(false);

  // Direction toward Earth
  const direction = useMemo(() => {
    return startPosition.clone().negate().normalize();
  }, [startPosition]);

  useFrame(() => {
    if (!meshRef.current) return;

    // Move toward Earth
    const newPos = position.clone().add(direction.clone().multiplyScalar(PHOTON_SPEED));

    // Check for cluster collisions
    if (!hasCollided) {
      for (const cluster of clusters) {
        const clusterPos = new THREE.Vector3(
          cluster.position.x * SCALE,
          cluster.position.y * SCALE,
          cluster.position.z * SCALE
        );

        const dist = newPos.distanceTo(clusterPos);
        const collisionRadius = 0.15 + cluster.mass_1e14_msun * 0.005;

        if (dist < collisionRadius) {
          // Collision! Apply Doppler shift
          setHasCollided(true);
          if (cluster.direction === 'toward') {
            setColor(new THREE.Color(COLORS.blueshift));
          } else {
            setColor(new THREE.Color(COLORS.redshift));
          }
          onCollision?.(cluster);
          break;
        }
      }
    }

    // Reset when reaching center
    if (newPos.length() < 0.1) {
      setPosition(startPosition.clone());
      setColor(new THREE.Color(COLORS.neutral));
      setHasCollided(false);
    } else {
      setPosition(newPos);
    }

    meshRef.current.position.copy(newPos);
  });

  return (
    <mesh ref={meshRef} position={position}>
      <sphereGeometry args={[0.02, 8, 8]} />
      <meshBasicMaterial color={color} transparent opacity={0.8} />
    </mesh>
  );
}

/**
 * Galaxy cluster marker
 */
function ClusterMarker({ cluster }: { cluster: Cluster }) {
  const meshRef = useRef<THREE.Mesh>(null);
  const glowRef = useRef<THREE.Mesh>(null);

  const position = useMemo(() => new THREE.Vector3(
    cluster.position.x * SCALE,
    cluster.position.y * SCALE,
    cluster.position.z * SCALE
  ), [cluster]);

  const size = useMemo(() => {
    return 0.05 + cluster.mass_1e14_msun * 0.003;
  }, [cluster.mass_1e14_msun]);

  const color = useMemo(() => {
    return cluster.direction === 'toward' ? COLORS.blueshift : COLORS.redshift;
  }, [cluster.direction]);

  useFrame(({ clock }) => {
    if (meshRef.current) {
      const pulse = 1 + Math.sin(clock.getElapsedTime() * 2 + cluster.ksz_amplitude_uk) * 0.2;
      meshRef.current.scale.setScalar(pulse);
    }
  });

  return (
    <group position={position}>
      <mesh ref={meshRef}>
        <sphereGeometry args={[size, 12, 12]} />
        <meshStandardMaterial
          color={COLORS.cluster}
          emissive={color}
          emissiveIntensity={0.5}
        />
      </mesh>
      <mesh ref={glowRef}>
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
 * Main Cosmic Wind visualization
 */
export function CosmicWindShader({
  opacity = 1,
  showPhotons = true,
  showWind = true,
}: CosmicWindShaderProps) {
  const [data, setData] = useState<KSZData | null>(null);
  const groupRef = useRef<THREE.Group>(null);

  // Load data
  useEffect(() => {
    fetch('/data/ksz_cosmic_wind_data.json')
      .then(res => res.json())
      .then((loadedData: KSZData) => {
        setData(loadedData);
      })
      .catch(console.error);
  }, []);

  // Generate photon start positions on boundary sphere
  const photonStarts = useMemo(() => {
    const positions: THREE.Vector3[] = [];
    for (let i = 0; i < NUM_PHOTONS; i++) {
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      const r = HALF_BOX * SCALE * 0.8;

      positions.push(new THREE.Vector3(
        r * Math.sin(phi) * Math.cos(theta),
        r * Math.sin(phi) * Math.sin(theta),
        r * Math.cos(phi)
      ));
    }
    return positions;
  }, []);

  // Slow rotation
  useFrame(({ clock }) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = clock.getElapsedTime() * 0.01;
    }
  });

  if (!data) return null;

  return (
    <group ref={groupRef}>
      {/* Earth at center */}
      <mesh>
        <sphereGeometry args={[0.08, 16, 16]} />
        <meshStandardMaterial
          color="#4444FF"
          emissive="#4444FF"
          emissiveIntensity={0.3}
        />
      </mesh>

      {/* Cluster markers */}
      {data.clusters.map((cluster, i) => (
        <ClusterMarker key={cluster.name || i} cluster={cluster} />
      ))}

      {/* CMB Photons */}
      {showPhotons && photonStarts.map((start, i) => (
        <CMBPhoton
          key={i}
          startPosition={start}
          clusters={data.clusters}
        />
      ))}

      {/* Cosmic Wind vector */}
      {showWind && <CosmicWindArrow wind={data.cosmic_wind} />}

      {/* Boundary shell (where CMB photons originate) */}
      <mesh>
        <sphereGeometry args={[HALF_BOX * SCALE * 0.8, 32, 32]} />
        <meshBasicMaterial
          color="#88FF88"
          transparent
          opacity={0.02}
          side={THREE.BackSide}
          wireframe
        />
      </mesh>

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
