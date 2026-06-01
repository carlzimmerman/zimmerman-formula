/**
 * =============================================================================
 * VPOS SATELLITES - Vast Polar Structure of the Milky Way
 * =============================================================================
 *
 * Renders the Milky Way satellite galaxies showing the VPOS plane alignment.
 * VPOS is a thin planar structure containing 82% of MW satellites - anomalously
 * high for ΛCDM dark matter models, but predicted by MOND External Field Effect.
 *
 * Key physics:
 * - VPOS plane normal: (l=169.3°, b=-2.8°)
 * - Plane thickness: ~20 kpc
 * - On-plane fraction: 82% (vs ~30% ΛCDM prediction)
 * - Orbital pole alignment: 0.449 (vs 0.3 ΛCDM, >0.7 MOND prediction)
 *
 * Visual encoding:
 * - Satellite position: Galactocentric coordinates (Sun at origin)
 * - Color: Green (on VPOS plane) vs Red (off plane)
 * - Size: log(stellar mass)
 * - Orbital poles: Vector arrows showing orbital angular momentum
 *
 * =============================================================================
 */

import React, { useRef, useMemo, useEffect, useState } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';
import { Html, Line } from '@react-three/drei';

interface VPOSSatellitesProps {
  visible?: boolean;
  opacity?: number;
  showOrbitalPoles?: boolean;
  showVPOSPlane?: boolean;
  showLabels?: boolean;
}

interface Satellite {
  name: string;
  l: number;      // Galactic longitude (deg)
  b: number;      // Galactic latitude (deg)
  d_kpc: number;  // Distance from Sun (kpc)
  v_los: number;  // Line-of-sight velocity (km/s)
  mu_l: number;   // Proper motion in l (mas/yr)
  mu_b: number;   // Proper motion in b (mas/yr)
  log_mass: number;
  on_vpos: boolean;
  x_kpc: number;
  y_kpc: number;
  z_kpc: number;
  orbital_pole_l: number;
  orbital_pole_b: number;
  angular_momentum: number;
  dist_from_vpos_kpc: number;
}

interface VPOSData {
  metadata: {
    total_satellites: number;
  };
  vpos_analysis: {
    on_plane_count: number;
    off_plane_count: number;
    on_plane_fraction: number;
    vpos_plane_normal: { l: number; b: number };
    vpos_thickness_kpc: number;
    orbital_pole_alignment: number;
    dm_prediction: string;
    mond_prediction: string;
    interpretation: string;
  };
  vpos_plane: {
    normal_x: number;
    normal_y: number;
    normal_z: number;
    thickness_kpc: number;
    radius_kpc: number;
  };
  satellites: Satellite[];
  physics_interpretation: {
    dark_matter_prediction: string;
    mond_prediction: string;
    observation: string;
    conclusion: string;
  };
}

const KPC_TO_GPC = 1e-6; // Convert kpc to Gpc for consistent rendering

export function VPOSSatellites({
  visible = true,
  opacity = 0.9,
  showOrbitalPoles = true,
  showVPOSPlane = true,
  showLabels = false,
}: VPOSSatellitesProps) {
  const groupRef = useRef<THREE.Group>(null);
  const [data, setData] = useState<VPOSData | null>(null);
  const [loading, setLoading] = useState(true);
  const planeRef = useRef<THREE.Mesh>(null);

  // Load VPOS data
  useEffect(() => {
    if (!visible) return;

    fetch('/data/vpos_satellites.json')
      .then(res => res.json())
      .then((vposData: VPOSData) => {
        setData(vposData);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load VPOS data:', err);
        setLoading(false);
      });
  }, [visible]);

  // Compute VPOS plane orientation
  const planeRotation = useMemo(() => {
    if (!data?.vpos_plane) return new THREE.Euler(0, 0, 0);

    const normal = new THREE.Vector3(
      data.vpos_plane.normal_x,
      data.vpos_plane.normal_y,
      data.vpos_plane.normal_z
    ).normalize();

    // Compute rotation to align plane with normal
    const up = new THREE.Vector3(0, 1, 0);
    const quaternion = new THREE.Quaternion().setFromUnitVectors(up, normal);
    return new THREE.Euler().setFromQuaternion(quaternion);
  }, [data]);

  // Subtle animation
  useFrame((state) => {
    if (!planeRef.current) return;
    const material = planeRef.current.material as THREE.MeshBasicMaterial;
    material.opacity = 0.15 + 0.05 * Math.sin(state.clock.elapsedTime * 0.5);
  });

  if (!visible || loading || !data) return null;

  const planeRadius = (data.vpos_plane?.radius_kpc || 300) * KPC_TO_GPC;

  return (
    <group ref={groupRef}>
      {/* Milky Way center indicator */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[0.00001, 16, 16]} />
        <meshBasicMaterial color="#6699ff" />
      </mesh>

      {/* Sun position indicator (at origin for galactocentric coords) */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[0.000002, 8, 8]} />
        <meshBasicMaterial color="#ffdd00" />
      </mesh>

      {/* VPOS Plane (translucent disk) */}
      {showVPOSPlane && (
        <mesh ref={planeRef} rotation={planeRotation}>
          <cylinderGeometry args={[planeRadius, planeRadius, data.vpos_plane.thickness_kpc * KPC_TO_GPC, 64, 1, true]} />
          <meshBasicMaterial
            color="#00ff88"
            transparent
            opacity={0.15}
            side={THREE.DoubleSide}
            blending={THREE.AdditiveBlending}
            depthWrite={false}
          />
        </mesh>
      )}

      {/* VPOS Plane boundary ring */}
      {showVPOSPlane && (
        <mesh rotation={planeRotation}>
          <ringGeometry args={[planeRadius * 0.98, planeRadius, 64]} />
          <meshBasicMaterial
            color="#00ff88"
            transparent
            opacity={0.4}
            side={THREE.DoubleSide}
          />
        </mesh>
      )}

      {/* Satellite galaxies */}
      {data.satellites.map((sat, i) => {
        const pos = [
          sat.x_kpc * KPC_TO_GPC,
          sat.z_kpc * KPC_TO_GPC, // Swap y/z for Three.js
          sat.y_kpc * KPC_TO_GPC,
        ] as [number, number, number];

        const color = sat.on_vpos ? '#00ff88' : '#ff4444';
        const size = 0.000003 + sat.log_mass * 0.000001;

        // Orbital pole direction (for arrow)
        const poleL = sat.orbital_pole_l * Math.PI / 180;
        const poleB = sat.orbital_pole_b * Math.PI / 180;
        const poleDir = new THREE.Vector3(
          Math.cos(poleB) * Math.cos(poleL),
          Math.sin(poleB),
          Math.cos(poleB) * Math.sin(poleL)
        ).normalize();

        return (
          <group key={sat.name}>
            {/* Satellite marker */}
            <mesh position={pos}>
              <sphereGeometry args={[size, 12, 12]} />
              <meshBasicMaterial
                color={color}
                transparent
                opacity={opacity}
              />
            </mesh>

            {/* Glow effect */}
            <mesh position={pos}>
              <sphereGeometry args={[size * 2, 8, 8]} />
              <meshBasicMaterial
                color={color}
                transparent
                opacity={0.2}
                blending={THREE.AdditiveBlending}
                depthWrite={false}
              />
            </mesh>

            {/* Orbital pole arrow */}
            {showOrbitalPoles && (
              <arrowHelper
                args={[
                  poleDir,
                  new THREE.Vector3(...pos),
                  0.00005, // Arrow length
                  sat.on_vpos ? 0x00ffaa : 0xff6666,
                  0.00001,
                  0.000005,
                ]}
              />
            )}

            {/* Label */}
            {showLabels && (
              <Html position={[pos[0], pos[1] + size * 3, pos[2]]} center>
                <div style={{
                  background: 'rgba(0,0,0,0.8)',
                  padding: '2px 5px',
                  borderRadius: '3px',
                  fontSize: '9px',
                  color: color,
                  whiteSpace: 'nowrap',
                  border: `1px solid ${color}`,
                }}>
                  {sat.name}
                  <div style={{ fontSize: '7px', color: '#aaa' }}>
                    {sat.d_kpc} kpc
                  </div>
                </div>
              </Html>
            )}
          </group>
        );
      })}

      {/* Connection lines to MW center for major satellites */}
      {data.satellites
        .filter(sat => sat.log_mass > 8)
        .map((sat, i) => {
          const pos = [
            sat.x_kpc * KPC_TO_GPC,
            sat.z_kpc * KPC_TO_GPC,
            sat.y_kpc * KPC_TO_GPC,
          ] as [number, number, number];

          return (
            <Line
              key={`line-${sat.name}`}
              points={[[0, 0, 0], pos]}
              color={sat.on_vpos ? '#00ff88' : '#ff4444'}
              lineWidth={0.5}
              transparent
              opacity={0.2}
              dashed
              dashSize={0.00001}
              gapSize={0.00001}
            />
          );
        })}
    </group>
  );
}

/**
 * HUD overlay for VPOS Satellites statistics
 */
export function VPOSSatellitesHUD({
  visible = false,
  totalSatellites = 0,
  onPlaneCount = 0,
  offPlaneCount = 0,
  onPlaneFraction = 0,
  orbitalPoleAlignment = 0,
  dmPrediction = '',
  mondPrediction = '',
}: {
  visible?: boolean;
  totalSatellites?: number;
  onPlaneCount?: number;
  offPlaneCount?: number;
  onPlaneFraction?: number;
  orbitalPoleAlignment?: number;
  dmPrediction?: string;
  mondPrediction?: string;
}) {
  if (!visible) return null;

  const favorsMOND = onPlaneFraction > 0.6;

  return (
    <div style={{
      position: 'absolute',
      top: '400px',
      right: '20px',
      background: 'rgba(0,0,0,0.85)',
      padding: '15px',
      borderRadius: '8px',
      fontFamily: 'monospace',
      fontSize: '12px',
      color: '#fff',
      minWidth: '280px',
      border: '1px solid #00ff88',
      boxShadow: '0 0 20px rgba(0, 255, 136, 0.3)',
    }}>
      <div style={{ marginBottom: '10px', fontWeight: 'bold', color: '#00ff88' }}>
        VPOS - SATELLITE PLANE
      </div>

      <div style={{ marginBottom: '5px' }}>
        <span style={{ color: '#aaa' }}>Total satellites:</span>{' '}
        <span style={{ color: '#00ff88' }}>{totalSatellites}</span>
      </div>

      <div style={{ borderTop: '1px solid #333', paddingTop: '8px', marginTop: '8px' }}>
        <div style={{ marginBottom: '5px' }}>
          <span style={{ color: '#00ff88' }}>On-plane:</span> {onPlaneCount}{' '}
          <span style={{ color: '#ff4444' }}>Off-plane:</span> {offPlaneCount}
        </div>
        <div style={{ marginBottom: '5px' }}>
          <span style={{ color: '#aaa' }}>Alignment fraction:</span>{' '}
          <span style={{ color: favorsMOND ? '#00ff88' : '#ff8800', fontWeight: 'bold' }}>
            {(onPlaneFraction * 100).toFixed(1)}%
          </span>
        </div>
        <div style={{ marginBottom: '5px' }}>
          <span style={{ color: '#aaa' }}>Orbital pole alignment:</span>{' '}
          <span style={{ color: '#ffaa00' }}>{orbitalPoleAlignment.toFixed(3)}</span>
        </div>
      </div>

      <div style={{ borderTop: '1px solid #333', paddingTop: '8px', marginTop: '8px', fontSize: '10px' }}>
        <div style={{ marginBottom: '5px' }}>
          <span style={{ color: '#ff6666' }}>ΛCDM prediction:</span>{' '}
          <span style={{ color: '#888' }}>~30% on-plane</span>
        </div>
        <div style={{ marginBottom: '5px' }}>
          <span style={{ color: '#00ffaa' }}>MOND prediction:</span>{' '}
          <span style={{ color: '#888' }}>{'>'}70% co-planar</span>
        </div>
      </div>

      <div style={{
        marginTop: '10px',
        paddingTop: '8px',
        borderTop: '1px solid #333',
        fontSize: '10px',
        color: favorsMOND ? '#00ff88' : '#ff8800',
        fontWeight: 'bold',
      }}>
        {favorsMOND
          ? '✓ Observation favors MOND External Field Effect'
          : '? Intermediate alignment - more data needed'}
      </div>

      <div style={{
        marginTop: '8px',
        fontSize: '9px',
        color: '#666',
      }}>
        Green = on VPOS plane | Red = off plane
        <br />
        Arrows = orbital angular momentum direction
      </div>
    </div>
  );
}

export default VPOSSatellites;
