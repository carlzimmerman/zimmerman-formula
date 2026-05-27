/**
 * =============================================================================
 * VELOCITY RIVERS - Cosmicflows-4 Bulk Flow Visualization
 * =============================================================================
 *
 * Renders the cosmic velocity field as luminous rivers of flow.
 * Each galaxy shows a comet tail indicating its peculiar velocity vector.
 *
 * Key physics:
 * - Bulk flow: ~254 km/s toward (l=295°, b=14°)
 * - Great Attractor: Major flow convergence point
 * - Shapley Supercluster: Secondary attractor
 * - Dipole Repeller: Primary void pushing galaxies
 *
 * Visual encoding:
 * - Galaxy position: Cartesian coordinates in Mpc
 * - Comet tail: 3D velocity vector (length ∝ |v|)
 * - Color: Blue (approaching) to Red (receding) along line of sight
 *
 * =============================================================================
 */

import React, { useRef, useMemo, useEffect, useState } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';
import { Line } from '@react-three/drei';

interface VelocityRiversProps {
  visible?: boolean;
  opacity?: number;
  showAttractors?: boolean;
  showStreamlines?: boolean;
  velocityScale?: number;
}

interface Galaxy {
  name?: string;
  x_mpc: number;
  y_mpc: number;
  z_mpc: number;
  vx: number;
  vy: number;
  vz: number;
  v_total: number;
  distance_mpc: number;
}

interface Attractor {
  name: string;
  x_mpc: number;
  y_mpc: number;
  z_mpc: number;
  mass_description: string;
  distance_mpc: number;
  influence_type: string;
}

interface VelocityData {
  metadata: {
    total_galaxies: number;
    bulk_flow: {
      velocity_km_s: number;
      l_deg: number;
      b_deg: number;
    };
  };
  attractors: Attractor[];
  galaxies: Galaxy[];
}

const MPC_TO_GPC = 0.001; // Convert Mpc to Gpc for rendering

export function VelocityRivers({
  visible = true,
  opacity = 0.8,
  showAttractors = true,
  showStreamlines = true,
  velocityScale = 0.0005, // Scale factor for velocity vectors
}: VelocityRiversProps) {
  const groupRef = useRef<THREE.Group>(null);
  const [data, setData] = useState<VelocityData | null>(null);
  const [loading, setLoading] = useState(true);
  const timeRef = useRef(0);

  // Load velocity field data
  useEffect(() => {
    if (!visible) return;

    fetch('/data/cosmicflows4_velocities.json')
      .then(res => res.json())
      .then((velData: VelocityData) => {
        setData(velData);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load velocity field data:', err);
        setLoading(false);
      });
  }, [visible]);

  // Compute velocity color (blue = approaching, red = receding)
  const getVelocityColor = (vLOS: number) => {
    // vLOS > 0 = receding (redshift), vLOS < 0 = approaching (blueshift)
    const normalized = Math.max(-1, Math.min(1, vLOS / 500)); // Normalize to ±500 km/s
    if (normalized > 0) {
      return new THREE.Color().setHSL(0, 0.8, 0.5); // Red
    } else {
      return new THREE.Color().setHSL(0.6, 0.8, 0.5); // Blue
    }
  };

  // Animate streamlines
  useFrame((state, delta) => {
    timeRef.current += delta;
    if (!groupRef.current) return;

    // Pulse effect on attractors
    groupRef.current.children.forEach((child) => {
      if (child.userData.isAttractor) {
        const pulse = 1 + 0.1 * Math.sin(timeRef.current * 2 + child.userData.index);
        child.scale.setScalar(child.userData.baseScale * pulse);
      }
    });
  });

  // Create comet tail geometry for a galaxy
  const CometTail = useMemo(() => {
    return ({ galaxy, scale }: { galaxy: Galaxy; scale: number }) => {
      const pos = new THREE.Vector3(
        galaxy.x_mpc * MPC_TO_GPC,
        galaxy.y_mpc * MPC_TO_GPC,
        galaxy.z_mpc * MPC_TO_GPC
      );

      const vel = new THREE.Vector3(
        galaxy.vx * scale,
        galaxy.vy * scale,
        galaxy.vz * scale
      );

      const tailEnd = pos.clone().sub(vel); // Tail points opposite to velocity

      // Color based on radial velocity (approximate as z-component for simplicity)
      const color = getVelocityColor(galaxy.vz);

      // Create gradient tail
      const points = [
        pos.toArray() as [number, number, number],
        tailEnd.toArray() as [number, number, number],
      ];

      return (
        <Line
          points={points}
          color={color}
          lineWidth={1.5}
          transparent
          opacity={opacity * 0.6}
        />
      );
    };
  }, [opacity]);

  if (!visible || loading || !data) return null;

  return (
    <group ref={groupRef}>
      {/* Galaxy positions with comet tails */}
      {data.galaxies.map((galaxy, i) => {
        const pos = [
          galaxy.x_mpc * MPC_TO_GPC,
          galaxy.y_mpc * MPC_TO_GPC,
          galaxy.z_mpc * MPC_TO_GPC,
        ] as [number, number, number];

        const vel = new THREE.Vector3(
          galaxy.vx * velocityScale,
          galaxy.vy * velocityScale,
          galaxy.vz * velocityScale
        );

        const tailEnd = [
          pos[0] - vel.x,
          pos[1] - vel.y,
          pos[2] - vel.z,
        ] as [number, number, number];

        const color = getVelocityColor(galaxy.vz);
        const velMagnitude = galaxy.v_total / 1000; // Normalize to km/s / 1000

        return (
          <group key={galaxy.name || `gal-${i}`}>
            {/* Galaxy point */}
            <mesh position={pos}>
              <sphereGeometry args={[0.002 + velMagnitude * 0.001, 8, 8]} />
              <meshBasicMaterial
                color={color}
                transparent
                opacity={opacity}
              />
            </mesh>

            {/* Velocity tail (comet effect) */}
            {showStreamlines && (
              <Line
                points={[pos, tailEnd]}
                color={color}
                lineWidth={1.5}
                transparent
                opacity={opacity * 0.5}
              />
            )}
          </group>
        );
      })}

      {/* Major attractors */}
      {showAttractors && data.attractors.map((attractor, i) => {
        const pos = [
          attractor.x_mpc * MPC_TO_GPC,
          attractor.y_mpc * MPC_TO_GPC,
          attractor.z_mpc * MPC_TO_GPC,
        ] as [number, number, number];

        const isRepeller = attractor.influence_type === 'repeller';
        const color = isRepeller ? '#ff4400' : '#00ffaa';
        const size = isRepeller ? 0.02 : 0.025;

        return (
          <group key={attractor.name}>
            {/* Attractor/Repeller marker */}
            <mesh
              position={pos}
              userData={{ isAttractor: true, index: i, baseScale: size }}
            >
              <sphereGeometry args={[size, 16, 16]} />
              <meshBasicMaterial
                color={color}
                transparent
                opacity={0.8}
              />
            </mesh>

            {/* Influence sphere */}
            <mesh position={pos}>
              <sphereGeometry args={[attractor.distance_mpc * MPC_TO_GPC * 0.3, 24, 24]} />
              <meshBasicMaterial
                color={color}
                transparent
                opacity={0.1}
                side={THREE.BackSide}
                blending={THREE.AdditiveBlending}
                depthWrite={false}
              />
            </mesh>

            {/* Wireframe boundary */}
            <mesh position={pos}>
              <sphereGeometry args={[attractor.distance_mpc * MPC_TO_GPC * 0.3, 12, 12]} />
              <meshBasicMaterial
                color={color}
                transparent
                opacity={0.2}
                wireframe
              />
            </mesh>
          </group>
        );
      })}

      {/* Bulk flow direction indicator */}
      {data.metadata?.bulk_flow && (
        <group>
          {/* Arrow pointing in bulk flow direction */}
          <arrowHelper
            args={[
              new THREE.Vector3(
                Math.cos(data.metadata.bulk_flow.b_deg * Math.PI / 180) *
                  Math.cos(data.metadata.bulk_flow.l_deg * Math.PI / 180),
                Math.sin(data.metadata.bulk_flow.b_deg * Math.PI / 180),
                Math.cos(data.metadata.bulk_flow.b_deg * Math.PI / 180) *
                  Math.sin(data.metadata.bulk_flow.l_deg * Math.PI / 180)
              ).normalize(),
              new THREE.Vector3(0, 0, 0),
              0.5,
              0xffaa00,
              0.1,
              0.05,
            ]}
          />
        </group>
      )}
    </group>
  );
}

/**
 * HUD overlay for Velocity Rivers statistics
 */
export function VelocityRiversHUD({
  visible = false,
  totalGalaxies = 0,
  bulkFlowVelocity = 0,
  bulkFlowDirection = { l: 0, b: 0 },
  attractors = [] as Attractor[],
}: {
  visible?: boolean;
  totalGalaxies?: number;
  bulkFlowVelocity?: number;
  bulkFlowDirection?: { l: number; b: number };
  attractors?: Attractor[];
}) {
  if (!visible) return null;

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
      minWidth: '260px',
      border: '1px solid #ffaa00',
      boxShadow: '0 0 20px rgba(255, 170, 0, 0.3)',
    }}>
      <div style={{ marginBottom: '10px', fontWeight: 'bold', color: '#ffaa00' }}>
        VELOCITY RIVERS - CF4
      </div>

      <div style={{ marginBottom: '5px' }}>
        <span style={{ color: '#aaa' }}>Galaxies:</span>{' '}
        <span style={{ color: '#ffaa00' }}>{totalGalaxies.toLocaleString()}</span>
      </div>

      <div style={{ borderTop: '1px solid #333', paddingTop: '8px', marginTop: '8px' }}>
        <div style={{ color: '#00ffaa', fontSize: '11px', marginBottom: '5px' }}>
          Bulk Flow
        </div>
        <div style={{ marginBottom: '3px' }}>
          <span style={{ color: '#aaa' }}>Velocity:</span>{' '}
          <span style={{ color: '#fff' }}>{bulkFlowVelocity.toFixed(0)} km/s</span>
        </div>
        <div style={{ marginBottom: '3px', fontSize: '10px' }}>
          <span style={{ color: '#aaa' }}>Direction:</span>{' '}
          l={bulkFlowDirection.l.toFixed(1)}°, b={bulkFlowDirection.b.toFixed(1)}°
        </div>
      </div>

      <div style={{ borderTop: '1px solid #333', paddingTop: '8px', marginTop: '8px' }}>
        <div style={{ color: '#ff4400', fontSize: '10px', marginBottom: '3px' }}>
          Major Structures
        </div>
        {attractors.slice(0, 4).map((a, i) => (
          <div key={i} style={{ fontSize: '9px', marginBottom: '2px', color: a.influence_type === 'repeller' ? '#ff4400' : '#00ffaa' }}>
            {a.name}: {a.distance_mpc.toFixed(0)} Mpc
          </div>
        ))}
      </div>

      <div style={{
        marginTop: '10px',
        paddingTop: '8px',
        borderTop: '1px solid #333',
        fontSize: '9px',
        color: '#666',
      }}>
        Blue = approaching | Red = receding
        <br />
        Tail length ∝ peculiar velocity
      </div>
    </div>
  );
}

export default VelocityRivers;
