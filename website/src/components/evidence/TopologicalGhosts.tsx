/**
 * =============================================================================
 * TOPOLOGICAL GHOSTS - T³/Z₂ Mirror Image Visualization
 * =============================================================================
 *
 * In T³/Z₂ topology, space is finite and wraps around. Every cosmic structure
 * has "ghost" copies visible at positions offset by the fundamental domain
 * size L_c = 20.6 Gpc. Light from distant objects can reach us via multiple
 * topological paths, creating mirror images.
 *
 * Physics:
 * - T³ wrapping: position → position + n·L_c where n ∈ {-1, 0, +1}³
 * - Z₂ antipodal: additional parity inversion at identification
 * - Each object has up to 26 ghost copies (3³ - 1)
 * - Ghosts near boundaries are most visible (shortest alternative path)
 *
 * Key structures visualized:
 * - Great Attractor (0.08 Gpc)
 * - Shapley Concentration (0.2 Gpc)
 * - Sloan Great Wall (0.3 Gpc)
 * - Hercules-Corona Borealis Great Wall (3 Gpc)
 * - Distant QSOs and GW events
 *
 * =============================================================================
 */

import React, { useRef, useMemo } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';
import { Line, Html } from '@react-three/drei';

interface TopologicalGhostsProps {
  visible?: boolean;
  opacity?: number;
  showConnections?: boolean;
  showLabels?: boolean;
  ghostOpacity?: number;
}

// Fundamental domain size
const L_C = 20.6; // Gpc
const HALF_L_C = 10.3; // Gpc - boundary wall position

// Major cosmic structures with known positions (comoving Gpc)
interface CosmicStructure {
  name: string;
  position: [number, number, number]; // Gpc
  type: 'attractor' | 'wall' | 'cluster' | 'void' | 'qso' | 'gw';
  size: number; // Visual size
  color: string;
  mass?: string; // For display
  redshift?: number;
}

const COSMIC_STRUCTURES: CosmicStructure[] = [
  // === NEARBY ATTRACTORS ===
  {
    name: 'Great Attractor',
    position: [0.047, -0.014, 0.065], // l=320°, b=0°, d=0.08 Gpc
    type: 'attractor',
    size: 0.15,
    color: '#ff4444',
    mass: '5×10¹⁶ M☉',
  },
  {
    name: 'Shapley Concentration',
    position: [0.12, -0.08, 0.14], // l=307°, b=27°, d=0.2 Gpc
    type: 'attractor',
    size: 0.2,
    color: '#ff6644',
    mass: '1×10¹⁷ M☉',
  },
  {
    name: 'Laniakea Barycenter',
    position: [0.05, -0.02, 0.075],
    type: 'attractor',
    size: 0.12,
    color: '#ff8844',
    mass: '1×10¹⁷ M☉',
  },

  // === GREAT WALLS ===
  {
    name: 'Sloan Great Wall',
    position: [0.25, 0.1, 0.15], // Approximate centroid
    type: 'wall',
    size: 0.3,
    color: '#4488ff',
    redshift: 0.08,
  },
  {
    name: 'Hercules-Corona Wall',
    position: [2.5, 1.2, -0.8], // z ≈ 2, d ≈ 3 Gpc
    type: 'wall',
    size: 0.5,
    color: '#44aaff',
    redshift: 2.0,
  },
  {
    name: 'BOSS Great Wall',
    position: [0.6, 0.3, 0.2],
    type: 'wall',
    size: 0.25,
    color: '#4466ff',
    redshift: 0.47,
  },

  // === MAJOR CLUSTERS ===
  {
    name: 'Coma Cluster',
    position: [0.088, 0.032, 0.078], // d = 0.1 Gpc
    type: 'cluster',
    size: 0.08,
    color: '#44ff88',
    mass: '7×10¹⁴ M☉',
  },
  {
    name: 'Virgo Cluster',
    position: [0.012, 0.008, 0.01], // d = 0.017 Gpc
    type: 'cluster',
    size: 0.05,
    color: '#44ffaa',
    mass: '1×10¹⁵ M☉',
  },
  {
    name: 'Perseus Cluster',
    position: [0.055, 0.04, -0.03], // d = 0.074 Gpc
    type: 'cluster',
    size: 0.07,
    color: '#44ffcc',
    mass: '8×10¹⁴ M☉',
  },

  // === COSMIC VOIDS ===
  {
    name: 'Boötes Void',
    position: [0.22, 0.12, 0.08],
    type: 'void',
    size: 0.15,
    color: '#8844ff',
  },
  {
    name: 'KBC Void',
    position: [0.15, 0.05, 0.1], // Local underdensity
    type: 'void',
    size: 0.2,
    color: '#aa44ff',
  },
  {
    name: 'Dipole Repeller',
    position: [-0.12, 0.08, -0.06], // Opposite to bulk flow
    type: 'void',
    size: 0.18,
    color: '#cc44ff',
  },

  // === DISTANT QSOS (near boundary) ===
  {
    name: 'ULAS J1342+0928',
    position: [6.2, 3.1, -4.8], // z = 7.54, d ≈ 8.5 Gpc
    type: 'qso',
    size: 0.1,
    color: '#ff44ff',
    redshift: 7.54,
  },
  {
    name: 'J0313-1806',
    position: [-5.8, 4.2, 5.1], // z = 7.64
    type: 'qso',
    size: 0.1,
    color: '#ff66ff',
    redshift: 7.64,
  },
  {
    name: 'GN-z11',
    position: [4.5, -3.2, 6.8], // z = 10.6, d ≈ 9.8 Gpc
    type: 'qso',
    size: 0.08,
    color: '#ff88ff',
    redshift: 10.6,
  },

  // === GW EVENTS (distant) ===
  {
    name: 'GW190521',
    position: [4.2, 1.8, -2.5], // d = 5.3 Gpc
    type: 'gw',
    size: 0.12,
    color: '#ffaa00',
    mass: '142 M☉ remnant',
  },
  {
    name: 'GW231123',
    position: [-5.5, 3.2, 4.1], // d = 7.2 Gpc
    type: 'gw',
    size: 0.1,
    color: '#ffbb00',
    mass: '228 M☉ remnant',
  },
];

// Compute ghost positions for T³ wrapping
function computeGhosts(
  original: [number, number, number],
  Lc: number
): Array<{ position: [number, number, number]; offset: [number, number, number]; distance: number }> {
  const ghosts: Array<{ position: [number, number, number]; offset: [number, number, number]; distance: number }> = [];

  // Generate all 26 ghost positions (excluding the original at [0,0,0] offset)
  for (let nx = -1; nx <= 1; nx++) {
    for (let ny = -1; ny <= 1; ny++) {
      for (let nz = -1; nz <= 1; nz++) {
        if (nx === 0 && ny === 0 && nz === 0) continue; // Skip original

        const ghostPos: [number, number, number] = [
          original[0] + nx * Lc,
          original[1] + ny * Lc,
          original[2] + nz * Lc,
        ];

        // Calculate distance from observer
        const distance = Math.sqrt(ghostPos[0]**2 + ghostPos[1]**2 + ghostPos[2]**2);

        ghosts.push({
          position: ghostPos,
          offset: [nx, ny, nz],
          distance,
        });
      }
    }
  }

  // Sort by distance (closest ghosts first)
  ghosts.sort((a, b) => a.distance - b.distance);

  return ghosts;
}

// Get color for connection based on wrap direction
function getWrapColor(offset: [number, number, number]): string {
  const [nx, ny, nz] = offset;
  // Color by primary wrap axis
  if (Math.abs(nx) > 0 && ny === 0 && nz === 0) return '#ff4444'; // X-wrap: red
  if (Math.abs(ny) > 0 && nx === 0 && nz === 0) return '#44ff44'; // Y-wrap: green
  if (Math.abs(nz) > 0 && nx === 0 && ny === 0) return '#4444ff'; // Z-wrap: blue
  // Diagonal wraps
  if (Math.abs(nx) > 0 && Math.abs(ny) > 0 && nz === 0) return '#ffff44'; // XY: yellow
  if (Math.abs(nx) > 0 && Math.abs(nz) > 0 && ny === 0) return '#ff44ff'; // XZ: magenta
  if (Math.abs(ny) > 0 && Math.abs(nz) > 0 && nx === 0) return '#44ffff'; // YZ: cyan
  // Corner wraps (all three)
  return '#ffffff'; // XYZ: white
}

// Format wrap direction as human-readable string
function formatWrapDirection(offset: [number, number, number]): string {
  const [nx, ny, nz] = offset;
  const parts: string[] = [];

  if (nx !== 0) parts.push(nx > 0 ? '+X' : '-X');
  if (ny !== 0) parts.push(ny > 0 ? '+Y' : '-Y');
  if (nz !== 0) parts.push(nz > 0 ? '+Z' : '-Z');

  return parts.join('');
}

export function TopologicalGhosts({
  visible = true,
  opacity = 0.8,
  showConnections = true,
  showLabels = false,
  ghostOpacity = 0.3,
}: TopologicalGhostsProps) {
  const groupRef = useRef<THREE.Group>(null);
  const timeRef = useRef(0);

  // Animation
  useFrame((state, delta) => {
    timeRef.current += delta;
  });

  // Compute all ghosts for all structures
  const structuresWithGhosts = useMemo(() => {
    return COSMIC_STRUCTURES.map(structure => {
      const ghosts = computeGhosts(structure.position, L_C);

      // Filter to only show ghosts within reasonable viewing distance
      // and prioritize the closest few
      const visibleGhosts = ghosts
        .filter(g => g.distance < 25) // Within ~25 Gpc
        .slice(0, 6); // Show up to 6 closest ghosts per structure

      return {
        ...structure,
        ghosts: visibleGhosts,
      };
    });
  }, []);

  if (!visible) return null;

  return (
    <group ref={groupRef}>
      {/* T³ Boundary Box Wireframe */}
      <lineSegments>
        <edgesGeometry args={[new THREE.BoxGeometry(L_C, L_C, L_C)]} />
        <lineBasicMaterial color="#00ffff" transparent opacity={0.3} />
      </lineSegments>

      {/* Boundary wall labels */}
      {[
        { pos: [HALF_L_C, 0, 0], label: '+X Wall' },
        { pos: [-HALF_L_C, 0, 0], label: '-X Wall' },
        { pos: [0, HALF_L_C, 0], label: '+Y Wall' },
        { pos: [0, -HALF_L_C, 0], label: '-Y Wall' },
        { pos: [0, 0, HALF_L_C], label: '+Z Wall' },
        { pos: [0, 0, -HALF_L_C], label: '-Z Wall' },
      ].map((wall, i) => (
        <Html key={i} position={wall.pos as [number, number, number]} center>
          <div style={{
            color: '#00ffff',
            fontSize: '10px',
            fontFamily: 'monospace',
            opacity: 0.5,
            whiteSpace: 'nowrap',
          }}>
            {wall.label}
          </div>
        </Html>
      ))}

      {structuresWithGhosts.map((structure, si) => {
        const originalDist = Math.sqrt(
          structure.position[0]**2 +
          structure.position[1]**2 +
          structure.position[2]**2
        );

        return (
          <group key={structure.name}>
            {/* Original structure */}
            <mesh position={structure.position}>
              <sphereGeometry args={[structure.size, 16, 16]} />
              <meshBasicMaterial
                color={structure.color}
                transparent
                opacity={opacity}
              />
            </mesh>

            {/* Original glow */}
            <mesh position={structure.position}>
              <sphereGeometry args={[structure.size * 1.5, 12, 12]} />
              <meshBasicMaterial
                color={structure.color}
                transparent
                opacity={0.2}
                blending={THREE.AdditiveBlending}
                depthWrite={false}
              />
            </mesh>

            {/* Label for original */}
            {showLabels && (
              <Html position={structure.position} center>
                <div style={{
                  background: 'rgba(0,0,0,0.8)',
                  padding: '4px 8px',
                  borderRadius: '4px',
                  fontSize: '10px',
                  color: structure.color,
                  whiteSpace: 'nowrap',
                  border: `1px solid ${structure.color}`,
                }}>
                  <div style={{ fontWeight: 'bold' }}>{structure.name}</div>
                  <div style={{ fontSize: '8px', color: '#aaa' }}>
                    d = {originalDist.toFixed(2)} Gpc
                  </div>
                </div>
              </Html>
            )}

            {/* Ghost copies */}
            {structure.ghosts.map((ghost, gi) => {
              const wrapColor = getWrapColor(ghost.offset);
              const ghostSize = structure.size * 0.7; // Slightly smaller

              // Pulsing opacity for ghosts
              const pulseOpacity = ghostOpacity * (0.7 + 0.3 * Math.sin(timeRef.current * 2 + si + gi));

              return (
                <group key={`ghost-${gi}`}>
                  {/* Ghost sphere */}
                  <mesh position={ghost.position}>
                    <sphereGeometry args={[ghostSize, 12, 12]} />
                    <meshBasicMaterial
                      color={structure.color}
                      transparent
                      opacity={pulseOpacity}
                      blending={THREE.AdditiveBlending}
                      depthWrite={false}
                    />
                  </mesh>

                  {/* Ghost ring indicator (shows it's a copy) */}
                  <mesh
                    position={ghost.position}
                    rotation={[Math.PI / 2, 0, 0]}
                  >
                    <ringGeometry args={[ghostSize * 1.2, ghostSize * 1.4, 32]} />
                    <meshBasicMaterial
                      color={wrapColor}
                      transparent
                      opacity={pulseOpacity * 0.5}
                      side={THREE.DoubleSide}
                    />
                  </mesh>

                  {/* Connection line from original to ghost */}
                  {showConnections && (
                    <Line
                      points={[structure.position, ghost.position]}
                      color={wrapColor}
                      lineWidth={1}
                      transparent
                      opacity={0.15}
                      dashed
                      dashSize={0.5}
                      gapSize={0.3}
                    />
                  )}

                  {/* Ghost label - shows structure name + wrap direction */}
                  {showLabels && (
                    <Html position={ghost.position} center>
                      <div style={{
                        background: 'rgba(0,0,0,0.85)',
                        padding: '3px 8px',
                        borderRadius: '4px',
                        fontSize: '9px',
                        color: wrapColor,
                        whiteSpace: 'nowrap',
                        opacity: 0.9,
                        border: `1px solid ${wrapColor}40`,
                      }}>
                        <div style={{ fontWeight: 'bold', color: structure.color }}>
                          {structure.name}
                        </div>
                        <div style={{ fontSize: '7px', color: '#aaa', marginTop: '1px' }}>
                          Ghost {formatWrapDirection(ghost.offset)} • {ghost.distance.toFixed(1)} Gpc
                        </div>
                      </div>
                    </Html>
                  )}
                </group>
              );
            })}
          </group>
        );
      })}

      {/* Observer marker */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[0.05, 16, 16]} />
        <meshBasicMaterial color="#ffffff" />
      </mesh>

      {/* Legend showing wrap directions */}
      <group position={[-HALF_L_C + 1, HALF_L_C - 1, HALF_L_C - 1]}>
        {/* This would be better as HTML overlay */}
      </group>
    </group>
  );
}

/**
 * HUD overlay for Topological Ghosts
 */
export function TopologicalGhostsHUD({
  visible = false,
  totalStructures = COSMIC_STRUCTURES.length,
  fundamentalDomain = 20.6,
  maxGhostDistance = 25,
}: {
  visible?: boolean;
  totalStructures?: number;
  fundamentalDomain?: number;
  maxGhostDistance?: number;
}) {
  if (!visible) return null;

  return (
    <div style={{
      position: 'absolute',
      top: '400px',
      right: '20px',
      background: 'rgba(0,0,0,0.9)',
      padding: '15px',
      borderRadius: '8px',
      fontFamily: 'monospace',
      fontSize: '12px',
      color: '#fff',
      minWidth: '280px',
      border: '1px solid #00ffff',
      boxShadow: '0 0 25px rgba(0, 255, 255, 0.4)',
    }}>
      <div style={{ marginBottom: '10px', fontWeight: 'bold', color: '#00ffff', fontSize: '14px' }}>
        TOPOLOGICAL GHOST IMAGES
      </div>

      <div style={{ marginBottom: '8px' }}>
        <span style={{ color: '#aaa' }}>Structures tracked:</span>{' '}
        <span style={{ color: '#00ffff' }}>{totalStructures}</span>
      </div>

      <div style={{ marginBottom: '8px' }}>
        <span style={{ color: '#aaa' }}>Fundamental domain:</span>{' '}
        <span style={{ color: '#fff' }}>L_c = {fundamentalDomain} Gpc</span>
      </div>

      <div style={{ borderTop: '1px solid #333', paddingTop: '10px', marginTop: '10px' }}>
        <div style={{ color: '#ffaa00', marginBottom: '8px', fontWeight: 'bold' }}>
          T³ TOPOLOGY EXPLANATION
        </div>
        <div style={{ fontSize: '11px', color: '#888', lineHeight: '1.4' }}>
          In a finite universe with T³ topology, space wraps around like a
          3D video game. Light from distant objects can reach us via multiple
          paths, creating <span style={{ color: '#00ffff' }}>ghost images</span> at
          positions offset by L_c = {fundamentalDomain} Gpc.
        </div>
      </div>

      <div style={{ borderTop: '1px solid #333', paddingTop: '10px', marginTop: '10px' }}>
        <div style={{ color: '#ff4444', marginBottom: '5px', fontWeight: 'bold' }}>
          GHOST POSITIONS
        </div>
        <div style={{ fontSize: '10px', color: '#888', lineHeight: '1.6' }}>
          <code style={{ color: '#fff' }}>r_ghost = r_original + n·L_c</code>
          <br />
          where n ∈ {'{'}-1, 0, +1{'}'}³ (26 possible ghosts)
        </div>
      </div>

      <div style={{ borderTop: '1px solid #333', paddingTop: '10px', marginTop: '10px' }}>
        <div style={{ marginBottom: '5px', fontWeight: 'bold', color: '#fff' }}>
          WRAP DIRECTION KEY
        </div>
        <div style={{ fontSize: '10px', lineHeight: '1.8' }}>
          <span style={{ color: '#ff4444' }}>━━</span> X-axis wrap<br />
          <span style={{ color: '#44ff44' }}>━━</span> Y-axis wrap<br />
          <span style={{ color: '#4444ff' }}>━━</span> Z-axis wrap<br />
          <span style={{ color: '#ffff44' }}>━━</span> XY diagonal<br />
          <span style={{ color: '#ff44ff' }}>━━</span> XZ diagonal<br />
          <span style={{ color: '#44ffff' }}>━━</span> YZ diagonal<br />
          <span style={{ color: '#ffffff' }}>━━</span> XYZ corner
        </div>
      </div>

      <div style={{
        marginTop: '10px',
        fontSize: '9px',
        color: '#666',
        borderTop: '1px solid #333',
        paddingTop: '8px',
      }}>
        <span style={{ color: '#00ffff' }}>●</span> Original |{' '}
        <span style={{ color: '#00ffff', opacity: 0.5 }}>○</span> Ghost copy |{' '}
        <span style={{ color: '#00ffff' }}>□</span> T³ boundary
      </div>
    </div>
  );
}

export default TopologicalGhosts;
