/**
 * =============================================================================
 * STANDING WAVE NODES - T³ Topology Resonance Visualization
 * =============================================================================
 *
 * Visualizes standing wave patterns in a finite T³ universe with L_c = 20.6 Gpc.
 * Standing waves form when the universe's finite size quantizes allowed wavelengths.
 *
 * Physics:
 * - Allowed wavelengths: λ_n = 2L_c/n for mode n = 1,2,3,...
 * - Fundamental mode (n=1): λ₁ = 41.2 Gpc (spans entire box twice)
 * - Node positions for mode n: x = (k/n) × L_c for k = 1,2,...,n-1
 * - L_c/2 = 10.3 Gpc is where n=2 mode has its central node
 *
 * Cosmological Implications:
 * - CMB power spectrum suppression at k < 2π/L_c (large-scale cutoff)
 * - Galaxy underdensity predicted at nodal surfaces
 * - BAO scale (150 Mpc) as potential L_c harmonic: L_c/150 ≈ 137 ≈ 1/α
 *
 * Visualization:
 * - Nodal planes: Semi-transparent surfaces where amplitude = 0
 * - Amplitude field: 3D visualization of wave intensity
 * - Void correlation: Overlay of observed cosmic voids
 * - BAO shells: 150 Mpc scale resonance rings
 *
 * =============================================================================
 */

import React, { useRef, useMemo, useState, useEffect } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';
import { Line, Html } from '@react-three/drei';

interface StandingWaveNodesProps {
  visible?: boolean;
  opacity?: number;
  showNodalPlanes?: boolean;
  showAmplitudeField?: boolean;
  showVoidCorrelation?: boolean;
  showBAOResonance?: boolean;
  showLabels?: boolean;
  selectedMode?: number;
  maxMode?: number;
}

interface CosmicVoid {
  name: string;
  ra_deg: number;
  dec_deg: number;
  redshift: number;
  radius_mpc: number;
  x_gpc: number;
  y_gpc: number;
  z_gpc: number;
  underdensity: number;
}

interface VoidData {
  metadata: {
    total_voids: number;
  };
  voids: CosmicVoid[];
}

// Fundamental domain size
const L_C = 20.6; // Gpc
const HALF_L_C = L_C / 2; // 10.3 Gpc - position of n=2 mode node

// BAO scale
const BAO_SCALE_MPC = 150;
const BAO_SCALE_GPC = BAO_SCALE_MPC / 1000; // 0.15 Gpc

// Mode colors (spectral)
const MODE_COLORS: Record<number, string> = {
  1: '#ff0000', // Red - fundamental
  2: '#ff8800', // Orange
  3: '#ffff00', // Yellow
  4: '#00ff00', // Green
  5: '#00ffff', // Cyan
  6: '#0088ff', // Blue
  7: '#8800ff', // Violet
  8: '#ff00ff', // Magenta
};

/**
 * Calculate node positions for a given mode number
 * For mode n, nodes are at x = (k/n) × L_c for k = 1,2,...,n-1
 */
function getNodePositions(mode: number, Lc: number): number[] {
  const nodes: number[] = [];
  for (let k = 1; k < mode; k++) {
    nodes.push((k / mode) * Lc - Lc / 2); // Center coordinates at 0
  }
  return nodes;
}

/**
 * Calculate wavelength for a given mode
 */
function getWavelength(mode: number, Lc: number): number {
  return (2 * Lc) / mode;
}

/**
 * Standing wave amplitude at position x for mode n
 * A(x) = cos(n × π × x / L_c)
 */
function standingWaveAmplitude(x: number, mode: number, Lc: number): number {
  return Math.cos((mode * Math.PI * (x + Lc / 2)) / Lc);
}

export function StandingWaveNodes({
  visible = true,
  opacity = 0.6,
  showNodalPlanes = true,
  showAmplitudeField = true,
  showVoidCorrelation = true,
  showBAOResonance = false,
  showLabels = false,
  selectedMode = 2,
  maxMode = 5,
}: StandingWaveNodesProps) {
  const groupRef = useRef<THREE.Group>(null);
  const timeRef = useRef(0);
  const [voidData, setVoidData] = useState<VoidData | null>(null);

  // Load void data for correlation
  useEffect(() => {
    if (!visible || !showVoidCorrelation) return;

    fetch('/data/cosmic_voids.json')
      .then(res => res.json())
      .then((data: VoidData) => setVoidData(data))
      .catch(err => console.error('Failed to load void data:', err));
  }, [visible, showVoidCorrelation]);

  // Animation
  useFrame((state, delta) => {
    timeRef.current += delta;
  });

  // Generate mode data
  const modes = useMemo(() => {
    const modeList = [];
    for (let n = 1; n <= maxMode; n++) {
      modeList.push({
        mode: n,
        wavelength: getWavelength(n, L_C),
        nodePositions: getNodePositions(n, L_C),
        color: MODE_COLORS[n] || '#ffffff',
      });
    }
    return modeList;
  }, [maxMode]);

  // Generate amplitude field points (3D grid sampling)
  const amplitudeFieldPoints = useMemo(() => {
    if (!showAmplitudeField) return [];

    const points: Array<{
      position: [number, number, number];
      amplitude: number;
    }> = [];

    const gridSize = 8; // Sample points per axis
    const step = L_C / gridSize;

    for (let ix = 0; ix <= gridSize; ix++) {
      for (let iy = 0; iy <= gridSize; iy++) {
        for (let iz = 0; iz <= gridSize; iz++) {
          const x = -HALF_L_C + ix * step;
          const y = -HALF_L_C + iy * step;
          const z = -HALF_L_C + iz * step;

          // Combined amplitude from selected mode in all three axes
          const ampX = standingWaveAmplitude(x, selectedMode, L_C);
          const ampY = standingWaveAmplitude(y, selectedMode, L_C);
          const ampZ = standingWaveAmplitude(z, selectedMode, L_C);

          // 3D standing wave has amplitude product
          const totalAmp = ampX * ampY * ampZ;

          points.push({
            position: [x, y, z],
            amplitude: totalAmp,
          });
        }
      }
    }

    return points;
  }, [showAmplitudeField, selectedMode]);

  // BAO resonance shells centered at origin
  const baoShells = useMemo(() => {
    if (!showBAOResonance) return [];

    const shells = [];
    // Show BAO shells as harmonics: n × 150 Mpc
    for (let n = 1; n <= 10; n++) {
      shells.push({
        radius: n * BAO_SCALE_GPC,
        harmonic: n,
      });
    }
    return shells;
  }, [showBAOResonance]);

  // Calculate void-node correlation
  const voidCorrelations = useMemo(() => {
    if (!voidData || !showVoidCorrelation) return [];

    const selectedModeData = modes.find(m => m.mode === selectedMode);
    if (!selectedModeData) return [];

    return voidData.voids.map(voidObj => {
      // Check if void is near any nodal plane
      let minDistToNode = Infinity;
      let nearestNodeAxis: 'x' | 'y' | 'z' = 'x';

      selectedModeData.nodePositions.forEach(nodePos => {
        const distX = Math.abs(voidObj.x_gpc - nodePos);
        const distY = Math.abs(voidObj.y_gpc - nodePos);
        const distZ = Math.abs(voidObj.z_gpc - nodePos);

        if (distX < minDistToNode) {
          minDistToNode = distX;
          nearestNodeAxis = 'x';
        }
        if (distY < minDistToNode) {
          minDistToNode = distY;
          nearestNodeAxis = 'y';
        }
        if (distZ < minDistToNode) {
          minDistToNode = distZ;
          nearestNodeAxis = 'z';
        }
      });

      // Correlation score: 1 if exactly on node, decays with distance
      const correlationScale = L_C / (selectedMode * 4); // Characteristic scale
      const correlation = Math.exp(-minDistToNode / correlationScale);

      return {
        void: voidObj,
        minDistToNode,
        nearestNodeAxis,
        correlation,
        isCorrelated: correlation > 0.5,
      };
    });
  }, [voidData, showVoidCorrelation, selectedMode, modes]);

  if (!visible) return null;

  const selectedModeData = modes.find(m => m.mode === selectedMode);
  const time = timeRef.current;

  return (
    <group ref={groupRef}>
      {/* Nodal Planes for selected mode */}
      {showNodalPlanes && selectedModeData && selectedModeData.nodePositions.map((nodePos, i) => (
        <group key={`node-${selectedMode}-${i}`}>
          {/* X-axis nodal plane (YZ plane at x = nodePos) */}
          <mesh position={[nodePos, 0, 0]} rotation={[0, Math.PI / 2, 0]}>
            <planeGeometry args={[L_C, L_C]} />
            <meshBasicMaterial
              color={selectedModeData.color}
              transparent
              opacity={0.15 + 0.05 * Math.sin(time * 2 + i)}
              side={THREE.DoubleSide}
              depthWrite={false}
            />
          </mesh>

          {/* Y-axis nodal plane (XZ plane at y = nodePos) */}
          <mesh position={[0, nodePos, 0]} rotation={[Math.PI / 2, 0, 0]}>
            <planeGeometry args={[L_C, L_C]} />
            <meshBasicMaterial
              color={selectedModeData.color}
              transparent
              opacity={0.15 + 0.05 * Math.sin(time * 2 + i + 1)}
              side={THREE.DoubleSide}
              depthWrite={false}
            />
          </mesh>

          {/* Z-axis nodal plane (XY plane at z = nodePos) */}
          <mesh position={[0, 0, nodePos]} rotation={[0, 0, 0]}>
            <planeGeometry args={[L_C, L_C]} />
            <meshBasicMaterial
              color={selectedModeData.color}
              transparent
              opacity={0.15 + 0.05 * Math.sin(time * 2 + i + 2)}
              side={THREE.DoubleSide}
              depthWrite={false}
            />
          </mesh>

          {/* Node position labels */}
          {showLabels && (
            <>
              <Html position={[nodePos, HALF_L_C + 0.5, 0]} center>
                <div style={{
                  background: 'rgba(0,0,0,0.8)',
                  padding: '2px 6px',
                  borderRadius: '3px',
                  fontSize: '9px',
                  color: selectedModeData.color,
                  whiteSpace: 'nowrap',
                }}>
                  x = {nodePos.toFixed(1)} Gpc
                </div>
              </Html>
            </>
          )}
        </group>
      ))}

      {/* Nodal plane intersection lines (where 2 planes meet) */}
      {showNodalPlanes && selectedModeData && selectedModeData.nodePositions.map((nodePos, i) => (
        <group key={`nodeline-${i}`}>
          {/* X-Y intersection line */}
          <Line
            points={[[nodePos, nodePos, -HALF_L_C], [nodePos, nodePos, HALF_L_C]]}
            color={selectedModeData.color}
            lineWidth={2}
            transparent
            opacity={0.8}
          />
          {/* X-Z intersection line */}
          <Line
            points={[[nodePos, -HALF_L_C, nodePos], [nodePos, HALF_L_C, nodePos]]}
            color={selectedModeData.color}
            lineWidth={2}
            transparent
            opacity={0.8}
          />
          {/* Y-Z intersection line */}
          <Line
            points={[[-HALF_L_C, nodePos, nodePos], [HALF_L_C, nodePos, nodePos]]}
            color={selectedModeData.color}
            lineWidth={2}
            transparent
            opacity={0.8}
          />
        </group>
      ))}

      {/* Amplitude field visualization */}
      {showAmplitudeField && amplitudeFieldPoints.map((point, i) => {
        const absAmp = Math.abs(point.amplitude);
        if (absAmp < 0.3) return null; // Skip near-zero amplitude points

        const size = 0.15 * absAmp;
        const color = point.amplitude > 0 ? '#00ff88' : '#ff4488';

        return (
          <mesh key={`amp-${i}`} position={point.position}>
            <sphereGeometry args={[size, 6, 6]} />
            <meshBasicMaterial
              color={color}
              transparent
              opacity={0.3 * absAmp}
              blending={THREE.AdditiveBlending}
              depthWrite={false}
            />
          </mesh>
        );
      })}

      {/* Void correlation markers */}
      {showVoidCorrelation && voidCorrelations.map((corr, i) => {
        const pos = [corr.void.x_gpc, corr.void.y_gpc, corr.void.z_gpc] as [number, number, number];
        const size = corr.void.radius_mpc / 1000 * 0.5; // Scale for visibility
        const color = corr.isCorrelated ? '#00ffff' : '#ff8800';

        return (
          <group key={`void-${i}`}>
            {/* Void sphere */}
            <mesh position={pos}>
              <sphereGeometry args={[size, 16, 16]} />
              <meshBasicMaterial
                color={color}
                transparent
                opacity={0.2 + 0.3 * corr.correlation}
                wireframe
              />
            </mesh>

            {/* Correlation indicator ring */}
            {corr.isCorrelated && (
              <mesh position={pos} rotation={[Math.PI / 2, 0, 0]}>
                <ringGeometry args={[size * 1.2, size * 1.4, 32]} />
                <meshBasicMaterial
                  color="#00ffff"
                  transparent
                  opacity={0.6 * corr.correlation}
                  side={THREE.DoubleSide}
                  blending={THREE.AdditiveBlending}
                  depthWrite={false}
                />
              </mesh>
            )}

            {/* Label for correlated voids */}
            {showLabels && corr.isCorrelated && (
              <Html position={[pos[0], pos[1] + size + 0.3, pos[2]]} center>
                <div style={{
                  background: 'rgba(0,0,0,0.8)',
                  padding: '3px 6px',
                  borderRadius: '3px',
                  fontSize: '9px',
                  color: '#00ffff',
                  whiteSpace: 'nowrap',
                  border: '1px solid #00ffff',
                }}>
                  <div>{corr.void.name}</div>
                  <div style={{ fontSize: '8px', color: '#88ffff' }}>
                    r = {(corr.minDistToNode).toFixed(2)} Gpc from node
                  </div>
                  <div style={{ fontSize: '8px', color: '#00ff88' }}>
                    Corr: {(corr.correlation * 100).toFixed(0)}%
                  </div>
                </div>
              </Html>
            )}
          </group>
        );
      })}

      {/* BAO resonance shells */}
      {showBAOResonance && baoShells.map((shell, i) => (
        <group key={`bao-${i}`}>
          <mesh>
            <sphereGeometry args={[shell.radius, 32, 16]} />
            <meshBasicMaterial
              color="#ffaa00"
              transparent
              opacity={0.08}
              wireframe
              depthWrite={false}
            />
          </mesh>

          {/* BAO shell glow */}
          <mesh>
            <sphereGeometry args={[shell.radius, 16, 8]} />
            <meshBasicMaterial
              color="#ffaa00"
              transparent
              opacity={0.02 + 0.02 * Math.sin(time + i)}
              side={THREE.BackSide}
              blending={THREE.AdditiveBlending}
              depthWrite={false}
            />
          </mesh>

          {showLabels && i % 3 === 0 && (
            <Html position={[shell.radius, 0, 0]} center>
              <div style={{
                background: 'rgba(0,0,0,0.7)',
                padding: '2px 4px',
                borderRadius: '2px',
                fontSize: '8px',
                color: '#ffaa00',
              }}>
                {shell.harmonic}×BAO
              </div>
            </Html>
          )}
        </group>
      ))}

      {/* Fundamental domain boundary (for reference) */}
      <Line
        points={[
          [-HALF_L_C, -HALF_L_C, -HALF_L_C],
          [HALF_L_C, -HALF_L_C, -HALF_L_C],
          [HALF_L_C, HALF_L_C, -HALF_L_C],
          [-HALF_L_C, HALF_L_C, -HALF_L_C],
          [-HALF_L_C, -HALF_L_C, -HALF_L_C],
        ]}
        color="#333366"
        lineWidth={1}
        transparent
        opacity={0.3}
      />
      <Line
        points={[
          [-HALF_L_C, -HALF_L_C, HALF_L_C],
          [HALF_L_C, -HALF_L_C, HALF_L_C],
          [HALF_L_C, HALF_L_C, HALF_L_C],
          [-HALF_L_C, HALF_L_C, HALF_L_C],
          [-HALF_L_C, -HALF_L_C, HALF_L_C],
        ]}
        color="#333366"
        lineWidth={1}
        transparent
        opacity={0.3}
      />

      {/* Mode indicator at origin */}
      {selectedModeData && (
        <mesh position={[0, 0, 0]}>
          <octahedronGeometry args={[0.3]} />
          <meshBasicMaterial
            color={selectedModeData.color}
            transparent
            opacity={0.5 + 0.2 * Math.sin(time * 3)}
          />
        </mesh>
      )}
    </group>
  );
}

/**
 * HUD overlay for Standing Wave Nodes
 */
export function StandingWaveNodesHUD({
  visible = false,
  selectedMode = 2,
  maxMode = 5,
  onModeChange,
  totalVoids = 0,
  correlatedVoids = 0,
}: {
  visible?: boolean;
  selectedMode?: number;
  maxMode?: number;
  onModeChange?: (mode: number) => void;
  totalVoids?: number;
  correlatedVoids?: number;
}) {
  if (!visible) return null;

  const wavelength = getWavelength(selectedMode, L_C);
  const nodeCount = selectedMode - 1;
  const correlationRate = totalVoids > 0 ? (correlatedVoids / totalVoids * 100) : 0;

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
      border: '1px solid #00ffaa',
      boxShadow: '0 0 25px rgba(0, 255, 170, 0.3)',
    }}>
      <div style={{ marginBottom: '12px', fontWeight: 'bold', color: '#00ffaa', fontSize: '14px' }}>
        T³ STANDING WAVE NODES
      </div>

      {/* Mode selector */}
      <div style={{ marginBottom: '12px' }}>
        <div style={{ color: '#aaa', marginBottom: '5px' }}>Select Mode (n):</div>
        <div style={{ display: 'flex', gap: '5px', flexWrap: 'wrap' }}>
          {Array.from({ length: maxMode }, (_, i) => i + 1).map(mode => (
            <button
              key={mode}
              onClick={() => onModeChange?.(mode)}
              style={{
                width: '28px',
                height: '28px',
                border: `2px solid ${MODE_COLORS[mode] || '#fff'}`,
                borderRadius: '4px',
                background: selectedMode === mode ? MODE_COLORS[mode] : 'transparent',
                color: selectedMode === mode ? '#000' : MODE_COLORS[mode],
                cursor: 'pointer',
                fontWeight: 'bold',
                fontSize: '12px',
              }}
            >
              {mode}
            </button>
          ))}
        </div>
      </div>

      {/* Mode info */}
      <div style={{
        background: 'rgba(0,255,170,0.1)',
        padding: '10px',
        borderRadius: '4px',
        marginBottom: '12px',
      }}>
        <div style={{ color: '#00ffaa', fontWeight: 'bold', marginBottom: '5px' }}>
          MODE n = {selectedMode}
        </div>
        <div style={{ marginBottom: '3px' }}>
          <span style={{ color: '#aaa' }}>Wavelength:</span>{' '}
          <span style={{ color: '#fff' }}>{wavelength.toFixed(1)} Gpc</span>
        </div>
        <div style={{ marginBottom: '3px' }}>
          <span style={{ color: '#aaa' }}>Nodal planes:</span>{' '}
          <span style={{ color: '#fff' }}>{nodeCount} per axis</span>
          <span style={{ color: '#666' }}> ({nodeCount * 3} total)</span>
        </div>
        {nodeCount > 0 && (
          <div style={{ fontSize: '10px', color: '#888' }}>
            Node positions: {getNodePositions(selectedMode, L_C).map(p => `${(p + HALF_L_C).toFixed(1)}`).join(', ')} Gpc
          </div>
        )}
      </div>

      {/* Void correlation */}
      {totalVoids > 0 && (
        <div style={{
          background: correlationRate > 40 ? 'rgba(0,255,255,0.15)' : 'rgba(255,136,0,0.1)',
          padding: '10px',
          borderRadius: '4px',
          marginBottom: '12px',
        }}>
          <div style={{ color: '#00ffff', fontWeight: 'bold', marginBottom: '5px' }}>
            VOID CORRELATION
          </div>
          <div>
            <span style={{ color: '#aaa' }}>Correlated voids:</span>{' '}
            <span style={{ color: '#00ffff', fontWeight: 'bold' }}>
              {correlatedVoids}/{totalVoids}
            </span>
            <span style={{ color: '#666' }}> ({correlationRate.toFixed(1)}%)</span>
          </div>
          <div style={{ fontSize: '10px', color: '#888', marginTop: '5px' }}>
            Voids within characteristic distance of nodal planes
          </div>
        </div>
      )}

      {/* Physics explanation */}
      <div style={{
        borderTop: '1px solid #333',
        paddingTop: '10px',
        fontSize: '10px',
        color: '#888',
        lineHeight: '1.5',
      }}>
        <div style={{ color: '#00ffaa', marginBottom: '5px' }}>PHYSICS:</div>
        <div>
          In a finite T³ universe (L<sub>c</sub> = {L_C} Gpc), only discrete wavelengths
          are allowed: λ<sub>n</sub> = 2L<sub>c</sub>/n. Standing waves have zero amplitude
          at <span style={{ color: '#ffaa00' }}>nodal planes</span>, predicting regions
          of <span style={{ color: '#00ffff' }}>galaxy underdensity</span>.
        </div>
      </div>

      {/* BAO connection */}
      <div style={{
        marginTop: '10px',
        fontSize: '10px',
        color: '#888',
        borderTop: '1px solid #333',
        paddingTop: '10px',
      }}>
        <div style={{ color: '#ffaa00', marginBottom: '3px' }}>BAO RESONANCE:</div>
        <div>
          L<sub>c</sub> / BAO scale = {L_C} Gpc / 0.15 Gpc ={' '}
          <span style={{ color: '#ffaa00', fontWeight: 'bold' }}>
            {(L_C / BAO_SCALE_GPC).toFixed(0)}
          </span>
          <span style={{ color: '#666' }}> ≈ 1/α (fine structure)</span>
        </div>
      </div>

      {/* Legend */}
      <div style={{
        marginTop: '10px',
        paddingTop: '8px',
        borderTop: '1px solid #333',
        fontSize: '9px',
        color: '#666',
      }}>
        <span style={{ color: MODE_COLORS[selectedMode] }}>■</span> Mode {selectedMode} nodal planes |{' '}
        <span style={{ color: '#00ffff' }}>○</span> Correlated voids |{' '}
        <span style={{ color: '#ff8800' }}>○</span> Other voids
      </div>
    </div>
  );
}

export default StandingWaveNodes;
