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

import React, { useRef, useMemo, useState, useEffect } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';
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
  flashEnabled?: boolean;
}

/**
 * Single FRB marker with flash animation
 */
function FRBMarker({
  frb,
  flashEnabled = true,
}: {
  frb: FRB;
  flashEnabled?: boolean;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  const glowRef = useRef<THREE.Mesh>(null);
  const [flashPhase, setFlashPhase] = useState(Math.random() * Math.PI * 2);

  // Position
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

  // Color based on DM
  const color = useMemo(() => {
    const dm = frb.dm_cosmic;
    if (dm < 200) return new THREE.Color(DM_COLORS.low);
    if (dm < 600) return new THREE.Color(DM_COLORS.medium);
    return new THREE.Color(DM_COLORS.high);
  }, [frb.dm_cosmic]);

  // Size based on fluence (or fixed for non-repeaters)
  const size = useMemo(() => {
    return frb.repeater ? 0.08 : 0.05;
  }, [frb.repeater]);

  // Flash animation
  useFrame(({ clock }) => {
    if (!flashEnabled || !meshRef.current) return;

    const t = clock.getElapsedTime();
    // Random flash pattern
    const flash = Math.pow(Math.sin(t * 3 + flashPhase), 8);

    meshRef.current.scale.setScalar(1 + flash * 2);

    if (glowRef.current) {
      (glowRef.current.material as THREE.MeshBasicMaterial).opacity = 0.1 + flash * 0.5;
    }
  });

  return (
    <group position={position}>
      {/* Core marker */}
      <mesh ref={meshRef}>
        <sphereGeometry args={[size, 12, 12]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={0.8}
        />
      </mesh>

      {/* Glow */}
      <mesh ref={glowRef}>
        <sphereGeometry args={[size * 3, 12, 12]} />
        <meshBasicMaterial
          color={color}
          transparent
          opacity={0.15}
          side={THREE.BackSide}
        />
      </mesh>

      {/* Dispersion cone to Earth */}
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
  flashEnabled = true,
}: DispersionTomographyProps) {
  const [data, setData] = useState<FRBData | null>(null);
  const groupRef = useRef<THREE.Group>(null);

  // Load data
  useEffect(() => {
    fetch('/data/frb_dispersion_data.json')
      .then(res => res.json())
      .then((loadedData: FRBData) => {
        setData(loadedData);
      })
      .catch(console.error);
  }, []);

  // Slow rotation
  useFrame(({ clock }) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = clock.getElapsedTime() * 0.02;
    }
  });

  if (!data) return null;

  return (
    <group ref={groupRef}>
      {/* Earth marker at center */}
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

      {/* FRB markers */}
      {data.frbs.map((frb, i) => (
        <FRBMarker
          key={frb.name || i}
          frb={frb}
          flashEnabled={flashEnabled}
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
        <div style={{ fontSize: '9px', color: '#666', marginTop: '5px' }}>
          DM along axes vs diagonals
          <br />tests cubic geometry
        </div>
      </div>
    </div>
  );
}

export default DispersionTomography;
