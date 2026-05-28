/**
 * =============================================================================
 * VELOCITY RIVERS - Cosmicflows-4 Bulk Flow Visualization (GPU-OPTIMIZED)
 * =============================================================================
 *
 * Renders the cosmic velocity field as luminous rivers of flow.
 * Each galaxy shows a comet tail indicating its peculiar velocity vector.
 *
 * PERFORMANCE OPTIMIZED using InstancedMesh:
 * - 5,000+ galaxies rendered with 2 draw calls instead of 10,000+
 * - Full geometry quality preserved
 * - Velocity tails combined into single LineSegments draw call
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

interface VelocityRiversProps {
  visible?: boolean;
  opacity?: number;
  showAttractors?: boolean;
  showStreamlines?: boolean;
  velocityScale?: number;
}

interface Galaxy {
  name?: string;
  x: number;       // Cartesian position in Mpc
  y: number;
  z: number;
  d_mpc: number;   // Distance from observer
  v_pec_kms: number;  // Peculiar velocity magnitude (km/s)
  v_pec_l: number;    // Velocity direction: galactic longitude (deg)
  v_pec_b: number;    // Velocity direction: galactic latitude (deg)
  v_los?: number;     // Line-of-sight velocity component
}

interface Attractor {
  name: string;
  x: number;  // Position in Gpc
  y: number;
  z: number;
  d_mpc: number;
  v_infall_kms?: number;
  mass_1e15_msun?: number;
}

interface ProcessedGalaxy {
  name?: string;
  position: THREE.Vector3;
  velocity: THREE.Vector3;  // Cartesian velocity vector
  tailEnd: THREE.Vector3;
  color: THREE.Color;
  size: number;
  v_total: number;  // Total velocity magnitude
}

interface VelocityData {
  metadata: {
    total_galaxies: number;
    fundamental_domain_gpc?: number;
  };
  attractors: Attractor[];
  galaxies: Galaxy[];
}

const MPC_TO_GPC = 0.001; // Convert Mpc to Gpc for rendering

// Compute velocity color (blue = approaching, red = receding)
function getVelocityColor(vLOS: number): THREE.Color {
  const normalized = Math.max(-1, Math.min(1, vLOS / 500));
  if (normalized > 0) {
    return new THREE.Color().setHSL(0, 0.8, 0.5); // Red (receding)
  } else {
    return new THREE.Color().setHSL(0.6, 0.8, 0.5); // Blue (approaching)
  }
}

export function VelocityRivers({
  visible = true,
  opacity = 0.8,
  showAttractors = true,
  showStreamlines = true,
  velocityScale = 0.0005,
}: VelocityRiversProps) {
  const groupRef = useRef<THREE.Group>(null);
  const galaxyMeshRef = useRef<THREE.InstancedMesh>(null);
  const [data, setData] = useState<VelocityData | null>(null);
  const [loading, setLoading] = useState(true);
  const timeRef = useRef(0);

  // Reusable objects for instance updates
  const tempMatrix = useMemo(() => new THREE.Matrix4(), []);
  const tempScale = useMemo(() => new THREE.Vector3(), []);
  const tempPosition = useMemo(() => new THREE.Vector3(), []);
  const identityQuaternion = useMemo(() => new THREE.Quaternion(), []);

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

  // Process galaxies with pre-computed visual properties
  const processedGalaxies = useMemo(() => {
    if (!data?.galaxies) return [];

    return data.galaxies
      .filter(g => g.v_pec_kms > 0 && g.d_mpc > 0) // Filter out zero-velocity or at-origin galaxies
      .map((galaxy): ProcessedGalaxy => {
        // Position in Gpc
        const position = new THREE.Vector3(
          galaxy.x * MPC_TO_GPC,
          galaxy.y * MPC_TO_GPC,
          galaxy.z * MPC_TO_GPC
        );

        // Convert galactic velocity (magnitude + l,b direction) to cartesian
        const v = galaxy.v_pec_kms;
        const l = (galaxy.v_pec_l || 0) * Math.PI / 180;
        const b = (galaxy.v_pec_b || 0) * Math.PI / 180;

        // Galactic to cartesian conversion
        const vx = v * Math.cos(b) * Math.cos(l);
        const vy = v * Math.cos(b) * Math.sin(l);
        const vz = v * Math.sin(b);

        const velocity = new THREE.Vector3(
          vx * velocityScale,
          vy * velocityScale,
          vz * velocityScale
        );

        const tailEnd = position.clone().sub(velocity);

        // Color based on line-of-sight velocity (z component approximation)
        const vLOS = galaxy.v_los ?? vz;
        const color = getVelocityColor(vLOS);

        const velMagnitude = v / 1000;
        const size = 0.002 + velMagnitude * 0.001;

        return {
          name: galaxy.name,
          position,
          velocity,
          tailEnd,
          color,
          size,
          v_total: v,
        };
      });
  }, [data, velocityScale]);

  // Combined velocity tail geometry (single draw call)
  const tailGeometry = useMemo(() => {
    if (!showStreamlines || processedGalaxies.length === 0) return null;

    const positions: number[] = [];
    const colors: number[] = [];

    for (const galaxy of processedGalaxies) {
      // Start point
      positions.push(galaxy.position.x, galaxy.position.y, galaxy.position.z);
      colors.push(galaxy.color.r, galaxy.color.g, galaxy.color.b);

      // End point
      positions.push(galaxy.tailEnd.x, galaxy.tailEnd.y, galaxy.tailEnd.z);
      colors.push(galaxy.color.r * 0.3, galaxy.color.g * 0.3, galaxy.color.b * 0.3); // Fade out
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    return geometry;
  }, [showStreamlines, processedGalaxies]);

  // Setup galaxy instanced mesh
  useEffect(() => {
    if (!galaxyMeshRef.current || processedGalaxies.length === 0) return;

    const count = processedGalaxies.length;

    for (let i = 0; i < count; i++) {
      const galaxy = processedGalaxies[i];

      tempPosition.copy(galaxy.position);
      tempScale.set(galaxy.size, galaxy.size, galaxy.size);
      tempMatrix.compose(tempPosition, identityQuaternion, tempScale);
      galaxyMeshRef.current.setMatrixAt(i, tempMatrix);
      galaxyMeshRef.current.setColorAt(i, galaxy.color);
    }

    galaxyMeshRef.current.instanceMatrix.needsUpdate = true;
    if (galaxyMeshRef.current.instanceColor) {
      galaxyMeshRef.current.instanceColor.needsUpdate = true;
    }
  }, [processedGalaxies, tempMatrix, tempScale, tempPosition, identityQuaternion]);

  // Animate attractors only (lightweight)
  useFrame((state, delta) => {
    timeRef.current += delta;

    // Pulse attractor markers
    if (groupRef.current) {
      groupRef.current.children.forEach((child) => {
        if (child.userData.isAttractor) {
          const pulse = 1 + 0.1 * Math.sin(timeRef.current * 2 + child.userData.index);
          child.scale.setScalar(child.userData.baseScale * pulse);
        }
      });
    }
  });

  if (!visible || loading || !data) return null;

  const galaxyCount = processedGalaxies.length;

  return (
    <group ref={groupRef}>
      {/* INSTANCED GALAXY POINTS - ONE draw call for 5000+ galaxies */}
      {galaxyCount > 0 && (
        <instancedMesh
          ref={galaxyMeshRef}
          args={[undefined, undefined, galaxyCount]}
          frustumCulled={false}
        >
          <sphereGeometry args={[1, 6, 6]} />
          <meshBasicMaterial
            transparent
            opacity={opacity}
          />
        </instancedMesh>
      )}

      {/* VELOCITY TAILS - Single LineSegments draw call */}
      {showStreamlines && tailGeometry && (
        <lineSegments geometry={tailGeometry}>
          <lineBasicMaterial
            vertexColors
            transparent
            opacity={opacity * 0.5}
          />
        </lineSegments>
      )}

      {/* Major attractors (kept as individual meshes - only ~5) */}
      {showAttractors && data.attractors?.map((attractor, i) => {
        // Attractor positions are already in Gpc
        const pos = [attractor.x, attractor.y, attractor.z] as [number, number, number];
        const color = '#00ffaa';
        const size = 0.02 + (attractor.mass_1e15_msun || 1) * 0.005;

        return (
          <group key={attractor.name}>
            {/* Attractor marker */}
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
              <sphereGeometry args={[attractor.d_mpc * MPC_TO_GPC * 0.5, 16, 16]} />
              <meshBasicMaterial
                color={color}
                transparent
                opacity={0.1}
                side={THREE.BackSide}
                blending={THREE.AdditiveBlending}
                depthWrite={false}
              />
            </mesh>
          </group>
        );
      })}

      {/* Earth/observer marker at origin */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[0.005, 8, 8]} />
        <meshBasicMaterial color="#ffffff" />
      </mesh>
    </group>
  );
}

/**
 * HUD overlay for Velocity Rivers statistics
 */
export function VelocityRiversHUD({
  visible = false,
  totalGalaxies = 0,
  attractors = [] as Attractor[],
}: {
  visible?: boolean;
  totalGalaxies?: number;
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
        <div style={{ color: '#00ffaa', fontSize: '10px', marginBottom: '3px' }}>
          Major Attractors
        </div>
        {attractors.slice(0, 5).map((a, i) => (
          <div key={i} style={{ fontSize: '9px', marginBottom: '2px', color: '#00ffaa' }}>
            {a.name}: {a.d_mpc} Mpc
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
        <div style={{ marginTop: '4px' }}>
          GPU-optimized: 2 draw calls for {totalGalaxies.toLocaleString()} galaxies
        </div>
      </div>
    </div>
  );
}

export default VelocityRivers;
