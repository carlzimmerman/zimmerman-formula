/**
 * =============================================================================
 * COSMIC WEB - Galaxy Cluster Distribution Visualization
 * =============================================================================
 *
 * Renders galaxy cluster structures using real cluster member data.
 * Data sources: Coma (A1656), Virgo, Shapley Supercluster catalogs.
 * Uses WebGL InstancedMesh for GPU-efficient rendering.
 *
 * Galaxy types (by redshift):
 * - BGS: z < 0.02, cyan - Bright nearby galaxies
 * - LRG: 0.02 < z < 0.03, red - Luminous red galaxies
 * - ELG: 0.03 < z < 0.04, blue - Emission line galaxies
 * - QSO: z > 0.04, magenta - Quasars/AGN
 *
 * Coordinates: Cartesian (X,Y,Z) in Gpc, Earth at origin
 * Note: Local cluster data scaled to fill T³ visualization volume
 *
 * T³ EDUCATIONAL GHOSTS:
 * When enabled, shows "ghost" copies of the cosmic web at ±L_c offsets,
 * demonstrating how T³ topology creates mirror images across boundaries.
 * These are illustrative - real clusters at ~200 Mpc wouldn't physically wrap.
 *
 * =============================================================================
 */

import React, { useRef, useMemo, useEffect, useState } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';
import { Html } from '@react-three/drei';

// T³ fundamental domain size
const L_C = 20.6; // Gpc
const HALF_L_C = 10.3; // Gpc

interface CosmicWebProps {
  visible?: boolean;
  opacity?: number;
  showBGS?: boolean;
  showLRG?: boolean;
  showELG?: boolean;
  showQSO?: boolean;
  showGhosts?: boolean; // Educational T³ ghost images
}

interface GalaxyObject {
  x: number;
  y: number;
  z: number;
  redshift: number;
  type: string;
}

interface CosmicWebData {
  metadata: {
    total_objects: number;
    source_counts: Record<string, number>;
    fundamental_domain_gpc: number;
  };
  objects: GalaxyObject[];
  boundary_alignment?: Record<string, {
    alignment_ratio: number;
    near_wall_density: number;
    far_wall_density: number;
  }>;
}

// Galaxy type colors
const TYPE_COLORS: Record<string, THREE.Color> = {
  BGS: new THREE.Color('#00ffff'),  // Cyan - nearby bright galaxies
  LRG: new THREE.Color('#ff4444'),  // Red - luminous red galaxies
  ELG: new THREE.Color('#4488ff'),  // Blue - emission line galaxies
  QSO: new THREE.Color('#ff00ff'),  // Magenta - quasars
  G: new THREE.Color('#4A90D9'),    // Default galaxy blue
};

// Ghost offset directions (6 face-adjacent copies in T³)
const GHOST_OFFSETS: [number, number, number][] = [
  [L_C, 0, 0],   // +X mirror
  [-L_C, 0, 0],  // -X mirror
  [0, L_C, 0],   // +Y mirror
  [0, -L_C, 0],  // -Y mirror
  [0, 0, L_C],   // +Z mirror
  [0, 0, -L_C],  // -Z mirror
];

// Ghost label positions (at boundaries)
const GHOST_LABELS: { offset: [number, number, number]; label: string }[] = [
  { offset: [L_C, 0, 0], label: '+X Ghost' },
  { offset: [-L_C, 0, 0], label: '-X Ghost' },
  { offset: [0, L_C, 0], label: '+Y Ghost' },
  { offset: [0, -L_C, 0], label: '-Y Ghost' },
  { offset: [0, 0, L_C], label: '+Z Ghost' },
  { offset: [0, 0, -L_C], label: '-Z Ghost' },
];

export function CosmicWeb({
  visible = true,
  opacity = 0.7,
  showBGS = true,
  showLRG = true,
  showELG = true,
  showQSO = true,
  showGhosts = false,
}: CosmicWebProps) {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const ghostMeshRef = useRef<THREE.InstancedMesh>(null);
  const [data, setData] = useState<CosmicWebData | null>(null);
  const [loading, setLoading] = useState(true);
  const timeRef = useRef(0);

  // Load cosmic web data from cluster members
  useEffect(() => {
    if (!visible) return;

    fetch('/data/cluster_members_data.json')
      .then(res => res.json())
      .then((clusterData: any) => {
        // Transform cluster data into cosmic web format
        const objects: GalaxyObject[] = [];
        const types = ['BGS', 'LRG', 'ELG', 'QSO'];
        const sourceCounts: Record<string, number> = {};

        // Process each cluster
        // Scale factor: cluster data is in Mpc (local universe ~200 Mpc)
        // T³ box walls at ±10.3 Gpc - scale to fit INSIDE the fundamental domain
        // Raw data spans ~-213 to +67 Mpc, scale 0.035 keeps within ±8 Gpc
        const SCALE_TO_GPC = 0.035;
        const HALF_BOX = 10.3; // T³ wall position in Gpc

        Object.values(clusterData.clusters || {}).forEach((cluster: any) => {
          const members = cluster.members || [];

          members.forEach((member: any) => {
            if (!member.position) return;

            // Scale positions - no artificial offsets, preserve natural structure
            let x = member.position.x * SCALE_TO_GPC;
            let y = member.position.y * SCALE_TO_GPC;
            let z = member.position.z * SCALE_TO_GPC;

            // Clamp to stay inside T³ fundamental domain
            x = Math.max(-HALF_BOX + 0.1, Math.min(HALF_BOX - 0.1, x));
            y = Math.max(-HALF_BOX + 0.1, Math.min(HALF_BOX - 0.1, y));
            z = Math.max(-HALF_BOX + 0.1, Math.min(HALF_BOX - 0.1, z));

            // Assign galaxy types based on redshift
            let type: string;
            if (member.redshift < 0.02) {
              type = 'BGS';
            } else if (member.redshift < 0.03) {
              type = 'LRG';
            } else if (member.redshift < 0.04) {
              type = 'ELG';
            } else {
              type = 'QSO';
            }

            sourceCounts[type] = (sourceCounts[type] || 0) + 1;

            objects.push({
              x,
              y,
              z,
              redshift: member.redshift,
              type,
            });
          });
        });

        setData({
          metadata: {
            total_objects: objects.length,
            source_counts: sourceCounts,
            fundamental_domain_gpc: 20.6,
          },
          objects,
        });
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load cosmic web data:', err);
        setLoading(false);
      });
  }, [visible]);

  // Filter and prepare galaxy data
  const { positions, colors, count } = useMemo(() => {
    if (!data?.objects) return { positions: null, colors: null, count: 0 };

    const filtered = data.objects.filter(obj => {
      const type = obj.type;
      if (type === 'BGS' && !showBGS) return false;
      if (type === 'LRG' && !showLRG) return false;
      if (type === 'ELG' && !showELG) return false;
      if (type === 'QSO' && !showQSO) return false;
      return true;
    });

    const posArray = new Float32Array(filtered.length * 3);
    const colorArray = new Float32Array(filtered.length * 3);

    filtered.forEach((obj, i) => {
      posArray[i * 3] = obj.x;
      posArray[i * 3 + 1] = obj.y;
      posArray[i * 3 + 2] = obj.z;

      const color = TYPE_COLORS[obj.type] || TYPE_COLORS.G;
      colorArray[i * 3] = color.r;
      colorArray[i * 3 + 1] = color.g;
      colorArray[i * 3 + 2] = color.b;
    });

    return { positions: posArray, colors: colorArray, count: filtered.length };
  }, [data, showBGS, showLRG, showELG, showQSO]);

  // Ghost positions - copies at T³ boundary offsets (educational visualization)
  const ghostData = useMemo(() => {
    if (!showGhosts || !positions || count === 0) {
      return { ghostPositions: null, ghostColors: null, ghostCount: 0 };
    }

    // Create 6 ghost copies (one for each face of the T³ cube)
    const totalGhosts = count * GHOST_OFFSETS.length;
    const ghostPosArray = new Float32Array(totalGhosts * 3);
    const ghostColorArray = new Float32Array(totalGhosts * 3);

    // Ghost color: cyan tint to indicate T³ mirror image
    const ghostTint = new THREE.Color('#00ffff');

    let ghostIndex = 0;
    for (const offset of GHOST_OFFSETS) {
      for (let i = 0; i < count; i++) {
        // Offset position by L_c in one direction
        ghostPosArray[ghostIndex * 3] = positions[i * 3] + offset[0];
        ghostPosArray[ghostIndex * 3 + 1] = positions[i * 3 + 1] + offset[1];
        ghostPosArray[ghostIndex * 3 + 2] = positions[i * 3 + 2] + offset[2];

        // Mix original color with cyan ghost tint
        ghostColorArray[ghostIndex * 3] = colors![i * 3] * 0.3 + ghostTint.r * 0.7;
        ghostColorArray[ghostIndex * 3 + 1] = colors![i * 3 + 1] * 0.3 + ghostTint.g * 0.7;
        ghostColorArray[ghostIndex * 3 + 2] = colors![i * 3 + 2] * 0.3 + ghostTint.b * 0.7;

        ghostIndex++;
      }
    }

    return { ghostPositions: ghostPosArray, ghostColors: ghostColorArray, ghostCount: totalGhosts };
  }, [showGhosts, positions, colors, count]);

  // Create instanced mesh geometry
  useEffect(() => {
    if (!meshRef.current || !positions || count === 0) return;

    const mesh = meshRef.current;
    const matrix = new THREE.Matrix4();
    const color = new THREE.Color();

    for (let i = 0; i < count; i++) {
      matrix.setPosition(
        positions[i * 3],
        positions[i * 3 + 1],
        positions[i * 3 + 2]
      );
      mesh.setMatrixAt(i, matrix);

      color.setRGB(
        colors![i * 3],
        colors![i * 3 + 1],
        colors![i * 3 + 2]
      );
      mesh.setColorAt(i, color);
    }

    mesh.instanceMatrix.needsUpdate = true;
    if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
  }, [positions, colors, count]);

  // Setup ghost instanced mesh
  useEffect(() => {
    if (!ghostMeshRef.current || !ghostData.ghostPositions || ghostData.ghostCount === 0) return;

    const mesh = ghostMeshRef.current;
    const matrix = new THREE.Matrix4();
    const color = new THREE.Color();

    for (let i = 0; i < ghostData.ghostCount; i++) {
      matrix.setPosition(
        ghostData.ghostPositions[i * 3],
        ghostData.ghostPositions[i * 3 + 1],
        ghostData.ghostPositions[i * 3 + 2]
      );
      mesh.setMatrixAt(i, matrix);

      color.setRGB(
        ghostData.ghostColors![i * 3],
        ghostData.ghostColors![i * 3 + 1],
        ghostData.ghostColors![i * 3 + 2]
      );
      mesh.setColorAt(i, color);
    }

    mesh.instanceMatrix.needsUpdate = true;
    if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
  }, [ghostData]);

  // Subtle shimmer animation + ghost pulse
  useFrame((state) => {
    timeRef.current = state.clock.elapsedTime;

    if (meshRef.current) {
      const material = meshRef.current.material as THREE.MeshBasicMaterial;
      material.opacity = opacity * (0.9 + 0.1 * Math.sin(state.clock.elapsedTime * 0.5));
    }

    // Ghosts pulse more dramatically to emphasize they're illustrative
    if (ghostMeshRef.current) {
      const ghostMaterial = ghostMeshRef.current.material as THREE.MeshBasicMaterial;
      ghostMaterial.opacity = 0.25 * (0.7 + 0.3 * Math.sin(state.clock.elapsedTime * 1.5));
    }
  });

  if (!visible || loading || count === 0) return null;

  return (
    <group>
      {/* Primary cosmic web - real cluster data */}
      <instancedMesh
        ref={meshRef}
        args={[undefined, undefined, count]}
        frustumCulled={false}
      >
        <sphereGeometry args={[0.05, 6, 6]} />
        <meshBasicMaterial
          transparent
          opacity={opacity}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
        />
      </instancedMesh>

      {/* T³ Ghost Images - Educational visualization of topology */}
      {showGhosts && ghostData.ghostCount > 0 && (
        <>
          <instancedMesh
            ref={ghostMeshRef}
            args={[undefined, undefined, ghostData.ghostCount]}
            frustumCulled={false}
          >
            <sphereGeometry args={[0.04, 4, 4]} />
            <meshBasicMaterial
              transparent
              opacity={0.25}
              blending={THREE.AdditiveBlending}
              depthWrite={false}
            />
          </instancedMesh>

          {/* Ghost direction labels */}
          {GHOST_LABELS.map((ghost, i) => (
            <Html
              key={i}
              position={[ghost.offset[0] * 0.5, ghost.offset[1] * 0.5, ghost.offset[2] * 0.5]}
              center
              style={{ pointerEvents: 'none' }}
            >
              <div style={{
                background: 'rgba(0, 255, 255, 0.15)',
                border: '1px solid rgba(0, 255, 255, 0.4)',
                borderRadius: '4px',
                padding: '4px 8px',
                fontSize: '10px',
                fontFamily: 'monospace',
                color: '#00ffff',
                whiteSpace: 'nowrap',
                textShadow: '0 0 10px #00ffff',
              }}>
                {ghost.label}
                <div style={{ fontSize: '8px', color: '#00aaaa' }}>
                  T³ Mirror
                </div>
              </div>
            </Html>
          ))}

          {/* Boundary markers at ghost region centers */}
          {GHOST_OFFSETS.map((offset, i) => (
            <mesh key={`ghost-marker-${i}`} position={[offset[0] * 0.5, offset[1] * 0.5, offset[2] * 0.5]}>
              <sphereGeometry args={[0.15, 8, 8]} />
              <meshBasicMaterial
                color="#00ffff"
                transparent
                opacity={0.15}
                wireframe
              />
            </mesh>
          ))}
        </>
      )}
    </group>
  );
}

/**
 * HUD overlay for Cosmic Web statistics
 */
export function CosmicWebHUD({
  visible = false,
  galaxyCount = 0,
  sourceCounts = {},
  showGhosts = false,
}: {
  visible?: boolean;
  galaxyCount?: number;
  sourceCounts?: Record<string, number>;
  showGhosts?: boolean;
}) {
  if (!visible) return null;

  const ghostCount = showGhosts ? galaxyCount * 6 : 0;

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
      minWidth: '220px',
      border: '1px solid #4A90D9',
      boxShadow: '0 0 20px rgba(74, 144, 217, 0.3)',
    }}>
      <div style={{ marginBottom: '10px', fontWeight: 'bold', color: '#4A90D9' }}>
        COSMIC WEB - CLUSTER DATA
      </div>

      <div style={{ marginBottom: '8px', fontSize: '11px' }}>
        <span style={{ color: '#aaa' }}>Total galaxies:</span>{' '}
        <span style={{ color: '#4A90D9' }}>{galaxyCount.toLocaleString()}</span>
      </div>

      {showGhosts && (
        <div style={{ marginBottom: '8px', fontSize: '11px' }}>
          <span style={{ color: '#00ffff' }}>T³ Ghost copies:</span>{' '}
          <span style={{ color: '#00aaaa' }}>{ghostCount.toLocaleString()}</span>
          <span style={{ color: '#666', fontSize: '9px' }}> (6 mirrors)</span>
        </div>
      )}

      <div style={{ borderTop: '1px solid #333', paddingTop: '8px', marginTop: '8px' }}>
        <div style={{ color: '#666', fontSize: '10px', marginBottom: '5px' }}>By Type:</div>
        {Object.entries(sourceCounts).map(([type, count]) => (
          <div key={type} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2px' }}>
            <span style={{ color: TYPE_COLORS[type]?.getStyle() || '#aaa' }}>{type}:</span>
            <span style={{ color: '#fff' }}>{count.toLocaleString()}</span>
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
        Data: Coma, Virgo, Shapley clusters
        <br />
        Earth at origin (0, 0, 0)
        {showGhosts && (
          <>
            <br />
            <span style={{ color: '#00aaaa' }}>
              Ghosts show T³ topology wrapping
            </span>
          </>
        )}
      </div>
    </div>
  );
}

export default CosmicWeb;
