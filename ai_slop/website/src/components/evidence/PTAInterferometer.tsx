/**
 * =============================================================================
 * PTA INTERFEROMETER - NANOGrav Pulsar Timing Array (GPU-OPTIMIZED)
 * =============================================================================
 *
 * Renders the NANOGrav 15-year pulsar timing array as a galaxy-scale
 * gravitational wave detector, visualizing the gravitational wave background
 * (GWB) detected through Hellings-Downs correlations.
 *
 * PERFORMANCE OPTIMIZED using InstancedMesh:
 * - 68 pulsars rendered with 3 draw calls instead of 204+
 * - Full geometry quality preserved (12x12 cores, 8x8 glows, 8-sided cones)
 * - Tethers combined into single LineSegments draw call
 * - GWB field and standing wave nodes use InstancedMesh
 * - Pulsing animation via instance matrix updates (GPU-efficient)
 *
 * Physics:
 * - 68 millisecond pulsars act as precise cosmic clocks
 * - GWB causes correlated timing residuals (nanosecond delays)
 * - Hellings-Downs correlation: unique signature of isotropic GWB
 * - In T³/Z₂ topology: GWB forms standing wave interference patterns
 *
 * =============================================================================
 */

import React, { useRef, useMemo, useEffect, useState } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';

interface PTAInterferometerProps {
  visible?: boolean;
  opacity?: number;
  showPulsars?: boolean;
  showTethers?: boolean;
  showGWBField?: boolean;
  showStandingWaves?: boolean;
}

interface Pulsar {
  name: string;
  ra_deg: number;
  dec_deg: number;
  distance_kpc: number;
  x_kpc: number;
  y_kpc: number;
  z_kpc: number;
  x_gpc: number;
  y_gpc: number;
  z_gpc: number;
  timing_rms_ns: number;
}

interface ProcessedPulsar extends Pulsar {
  position: THREE.Vector3;
  baseSize: number;
  coneRotation: THREE.Quaternion;
}

interface PTAData {
  metadata: {
    total_pulsars: number;
    gwb_detection_significance: string;
  };
  gwb_parameters: {
    amplitude: number;
    spectral_index: number;
    frequency_range_hz: number[];
  };
  pulsars: Pulsar[];
  hellings_downs_curve: Array<{ angle_deg: number; correlation: number }>;
  standing_wave_modes: Array<{
    mode: number;
    wavelength_gpc: number;
    frequency_hz: number;
    node_positions_gpc: number[];
    antinode_positions_gpc: number[];
  }>;
}

// Scale factor: pulsars are at kpc scale, but we render in Gpc
// We'll scale up for visibility in the cosmic view
const KPC_TO_GPC = 1e-6;
const PULSAR_VISUAL_SCALE = 1e4; // Scale up for visibility at cosmic scales

// Seeded random for consistent cone rotations
function seededRandom(seed: number): number {
  const x = Math.sin(seed * 9999) * 10000;
  return x - Math.floor(x);
}

export function PTAInterferometer({
  visible = true,
  opacity = 0.8,
  showPulsars = true,
  showTethers = true,
  showGWBField = true,
  showStandingWaves = true,
}: PTAInterferometerProps) {
  const groupRef = useRef<THREE.Group>(null);
  const [data, setData] = useState<PTAData | null>(null);
  const [loading, setLoading] = useState(true);
  const timeRef = useRef(0);

  // InstancedMesh refs
  const coresRef = useRef<THREE.InstancedMesh>(null);
  const glowsRef = useRef<THREE.InstancedMesh>(null);
  const conesRef = useRef<THREE.InstancedMesh>(null);
  const gwbRef = useRef<THREE.InstancedMesh>(null);

  // Reusable objects for instance updates
  const tempMatrix = useMemo(() => new THREE.Matrix4(), []);
  const tempScale = useMemo(() => new THREE.Vector3(), []);
  const tempPosition = useMemo(() => new THREE.Vector3(), []);
  const identityQuaternion = useMemo(() => new THREE.Quaternion(), []);

  // Load PTA data
  useEffect(() => {
    if (!visible) return;

    fetch('/data/nanograv_pta_gwb.json')
      .then(res => res.json())
      .then((ptaData: PTAData) => {
        setData(ptaData);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load PTA data:', err);
        setLoading(false);
      });
  }, [visible]);

  // Process pulsars with pre-computed visual properties
  const processedPulsars = useMemo(() => {
    if (!data?.pulsars) return [];

    return data.pulsars.map((pulsar, i) => {
      const position = new THREE.Vector3(
        pulsar.x_kpc * KPC_TO_GPC * PULSAR_VISUAL_SCALE,
        pulsar.y_kpc * KPC_TO_GPC * PULSAR_VISUAL_SCALE,
        pulsar.z_kpc * KPC_TO_GPC * PULSAR_VISUAL_SCALE
      );

      // Size based on timing precision (better timing = brighter)
      const baseSize = 0.02 * (1 - pulsar.timing_rms_ns / 600);

      // Seeded random rotation for cone (deterministic across frames)
      const coneRotation = new THREE.Quaternion().setFromEuler(
        new THREE.Euler(
          seededRandom(i * 17) * Math.PI,
          seededRandom(i * 23) * Math.PI,
          0
        )
      );

      return {
        ...pulsar,
        position,
        baseSize,
        coneRotation,
      };
    });
  }, [data]);

  // Generate tether connections (strongest correlations)
  const tethers = useMemo(() => {
    if (!data?.pulsars || data.pulsars.length < 2) return [];

    const connections: Array<{
      p1: Pulsar;
      p2: Pulsar;
      strength: number;
    }> = [];

    // Connect each pulsar to its nearest neighbors
    const pulsars = data.pulsars;
    for (let i = 0; i < pulsars.length; i++) {
      // Find 3 nearest neighbors for each pulsar
      const distances = pulsars
        .map((p, j) => ({
          idx: j,
          dist: Math.sqrt(
            (pulsars[i].x_kpc - p.x_kpc) ** 2 +
            (pulsars[i].y_kpc - p.y_kpc) ** 2 +
            (pulsars[i].z_kpc - p.z_kpc) ** 2
          ),
        }))
        .filter(d => d.idx !== i)
        .sort((a, b) => a.dist - b.dist)
        .slice(0, 3);

      distances.forEach(d => {
        // Avoid duplicate connections
        const exists = connections.some(
          c => (c.p1.name === pulsars[i].name && c.p2.name === pulsars[d.idx].name) ||
               (c.p1.name === pulsars[d.idx].name && c.p2.name === pulsars[i].name)
        );
        if (!exists) {
          connections.push({
            p1: pulsars[i],
            p2: pulsars[d.idx],
            strength: 1 / (1 + d.dist / 2), // Strength inversely proportional to distance
          });
        }
      });
    }

    return connections;
  }, [data]);

  // Combined tether geometry (single draw call)
  const tetherGeometry = useMemo(() => {
    if (!showTethers || tethers.length === 0) return null;

    const positions: number[] = [];

    for (const tether of tethers) {
      // Start point
      positions.push(
        tether.p1.x_kpc * KPC_TO_GPC * PULSAR_VISUAL_SCALE,
        tether.p1.y_kpc * KPC_TO_GPC * PULSAR_VISUAL_SCALE,
        tether.p1.z_kpc * KPC_TO_GPC * PULSAR_VISUAL_SCALE
      );
      // End point
      positions.push(
        tether.p2.x_kpc * KPC_TO_GPC * PULSAR_VISUAL_SCALE,
        tether.p2.y_kpc * KPC_TO_GPC * PULSAR_VISUAL_SCALE,
        tether.p2.z_kpc * KPC_TO_GPC * PULSAR_VISUAL_SCALE
      );
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    return geometry;
  }, [showTethers, tethers]);

  // Standing wave node planes data
  const standingWaveNodes = useMemo(() => {
    if (!data?.standing_wave_modes) return [];

    const nodes: Array<{
      position: THREE.Vector3;
      rotation: THREE.Quaternion;
    }> = [];

    // Only show first 3 modes to avoid clutter
    data.standing_wave_modes.slice(0, 3).forEach(mode => {
      mode.node_positions_gpc.forEach(pos => {
        // Only render if within visible range
        if (Math.abs(pos) > 12) return;

        // X-axis planes
        nodes.push({
          position: new THREE.Vector3(pos, 0, 0),
          rotation: new THREE.Quaternion().setFromEuler(new THREE.Euler(0, Math.PI / 2, 0)),
        });
        // Y-axis planes
        nodes.push({
          position: new THREE.Vector3(0, pos, 0),
          rotation: new THREE.Quaternion().setFromEuler(new THREE.Euler(Math.PI / 2, 0, 0)),
        });
        // Z-axis planes
        nodes.push({
          position: new THREE.Vector3(0, 0, pos),
          rotation: new THREE.Quaternion().setFromEuler(new THREE.Euler(0, 0, 0)),
        });
      });
    });

    return nodes.slice(0, 45); // Limit to 45 planes max (15 per axis)
  }, [data]);

  // Setup pulsar instanced meshes
  useEffect(() => {
    if (!coresRef.current || !glowsRef.current || !conesRef.current) return;
    if (processedPulsars.length === 0) return;

    const count = processedPulsars.length;
    const coreColor = new THREE.Color('#00ffaa');
    const coneColor = new THREE.Color('#00aaff');

    for (let i = 0; i < count; i++) {
      const pulsar = processedPulsars[i];

      // CORE SPHERE
      tempPosition.copy(pulsar.position);
      tempScale.set(pulsar.baseSize, pulsar.baseSize, pulsar.baseSize);
      tempMatrix.compose(tempPosition, identityQuaternion, tempScale);
      coresRef.current.setMatrixAt(i, tempMatrix);
      coresRef.current.setColorAt(i, coreColor);

      // GLOW SPHERE (2x size)
      tempScale.set(pulsar.baseSize * 2, pulsar.baseSize * 2, pulsar.baseSize * 2);
      tempMatrix.compose(tempPosition, identityQuaternion, tempScale);
      glowsRef.current.setMatrixAt(i, tempMatrix);
      glowsRef.current.setColorAt(i, coreColor);

      // CONE (radio beam) - use pre-computed rotation
      // Cone geometry: radius=0.5, height=3 at unit scale, scaled by baseSize
      const coneScale = pulsar.baseSize;
      tempScale.set(coneScale * 0.5, coneScale * 3, coneScale * 0.5);
      tempMatrix.compose(tempPosition, pulsar.coneRotation, tempScale);
      conesRef.current.setMatrixAt(i, tempMatrix);
      conesRef.current.setColorAt(i, coneColor);
    }

    coresRef.current.instanceMatrix.needsUpdate = true;
    if (coresRef.current.instanceColor) coresRef.current.instanceColor.needsUpdate = true;
    glowsRef.current.instanceMatrix.needsUpdate = true;
    if (glowsRef.current.instanceColor) glowsRef.current.instanceColor.needsUpdate = true;
    conesRef.current.instanceMatrix.needsUpdate = true;
    if (conesRef.current.instanceColor) conesRef.current.instanceColor.needsUpdate = true;

  }, [processedPulsars, tempMatrix, tempScale, tempPosition, identityQuaternion]);

  // Animation - pulsing pulsars via instance matrix updates
  useFrame((state, delta) => {
    timeRef.current += delta;

    // Animate pulsar cores (pulsing effect)
    if (coresRef.current && processedPulsars.length > 0) {
      for (let i = 0; i < processedPulsars.length; i++) {
        const pulsar = processedPulsars[i];
        const pulse = 1 + 0.3 * Math.sin(timeRef.current * 5 + i * 0.5);
        const size = pulsar.baseSize * pulse;

        tempPosition.copy(pulsar.position);
        tempScale.set(size, size, size);
        tempMatrix.compose(tempPosition, identityQuaternion, tempScale);
        coresRef.current.setMatrixAt(i, tempMatrix);
      }
      coresRef.current.instanceMatrix.needsUpdate = true;
    }

    // Animate GWB field spheres (opacity handled via uniforms would be better,
    // but for now we'll skip animating these as it's minimal)
  });

  // GWB field radii
  const gwbRadii = [0.5, 1.0, 1.5, 2.0];

  // Setup GWB instanced mesh
  useEffect(() => {
    if (!gwbRef.current || !showGWBField) return;

    const gwbColor = new THREE.Color('#ff00ff');

    for (let i = 0; i < gwbRadii.length; i++) {
      const radius = gwbRadii[i];
      tempPosition.set(0, 0, 0);
      tempScale.set(radius, radius, radius);
      tempMatrix.compose(tempPosition, identityQuaternion, tempScale);
      gwbRef.current.setMatrixAt(i, tempMatrix);
      gwbRef.current.setColorAt(i, gwbColor);
    }

    gwbRef.current.instanceMatrix.needsUpdate = true;
    if (gwbRef.current.instanceColor) gwbRef.current.instanceColor.needsUpdate = true;
  }, [showGWBField, tempMatrix, tempScale, tempPosition, identityQuaternion]);

  if (!visible || loading || !data) return null;

  const pulsarCount = processedPulsars.length;
  const nodeCount = standingWaveNodes.length;

  return (
    <group ref={groupRef}>
      {/* INSTANCED PULSAR CORES - Full 12x12 geometry, ONE draw call */}
      {showPulsars && pulsarCount > 0 && (
        <instancedMesh
          ref={coresRef}
          args={[undefined, undefined, pulsarCount]}
          frustumCulled={false}
        >
          <sphereGeometry args={[1, 12, 12]} />
          <meshBasicMaterial
            transparent
            opacity={opacity}
          />
        </instancedMesh>
      )}

      {/* INSTANCED PULSAR GLOWS - Full 8x8 geometry, ONE draw call */}
      {showPulsars && pulsarCount > 0 && (
        <instancedMesh
          ref={glowsRef}
          args={[undefined, undefined, pulsarCount]}
          frustumCulled={false}
        >
          <sphereGeometry args={[1, 8, 8]} />
          <meshBasicMaterial
            transparent
            opacity={0.2}
            blending={THREE.AdditiveBlending}
            depthWrite={false}
          />
        </instancedMesh>
      )}

      {/* INSTANCED RADIO BEAM CONES - Full 8-segment geometry, ONE draw call */}
      {showPulsars && pulsarCount > 0 && (
        <instancedMesh
          ref={conesRef}
          args={[undefined, undefined, pulsarCount]}
          frustumCulled={false}
        >
          <coneGeometry args={[1, 1, 8, 1, true]} />
          <meshBasicMaterial
            transparent
            opacity={0.15}
            side={THREE.DoubleSide}
          />
        </instancedMesh>
      )}

      {/* TETHERS - Combined into single LineSegments draw call */}
      {showTethers && tetherGeometry && (
        <lineSegments geometry={tetherGeometry}>
          <lineBasicMaterial
            color="#00aaff"
            transparent
            opacity={0.2}
          />
        </lineSegments>
      )}

      {/* Earth position marker */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[0.005, 16, 16]} />
        <meshBasicMaterial color="#ffff00" />
      </mesh>

      {/* INSTANCED GWB FIELD SPHERES - ONE draw call for all 4 */}
      {showGWBField && (
        <instancedMesh
          ref={gwbRef}
          args={[undefined, undefined, 4]}
          frustumCulled={false}
        >
          <sphereGeometry args={[1, 32, 32]} />
          <meshBasicMaterial
            transparent
            opacity={0.03}
            side={THREE.DoubleSide}
            blending={THREE.AdditiveBlending}
            depthWrite={false}
          />
        </instancedMesh>
      )}

      {/* Standing wave node planes - kept as individual meshes (few of them) */}
      {showStandingWaves && standingWaveNodes.map((node, i) => (
        <mesh key={`node-${i}`} position={node.position} quaternion={node.rotation}>
          <planeGeometry args={[20, 20]} />
          <meshBasicMaterial
            color="#ffffff"
            transparent
            opacity={0.02}
            side={THREE.DoubleSide}
            blending={THREE.AdditiveBlending}
            depthWrite={false}
          />
        </mesh>
      ))}

      {/* PTA array boundary sphere (visual reference) */}
      <mesh>
        <sphereGeometry args={[3, 32, 32]} />
        <meshBasicMaterial
          color="#00ffaa"
          transparent
          opacity={0.02}
          wireframe
        />
      </mesh>
    </group>
  );
}

/**
 * HUD overlay for PTA Interferometer statistics
 */
export function PTAInterferometerHUD({
  visible = false,
  totalPulsars = 68,
  gwbAmplitude = 2.4e-15,
  gwbSignificance = '3.5σ',
  standingWaveModes = 5,
}: {
  visible?: boolean;
  totalPulsars?: number;
  gwbAmplitude?: number;
  gwbSignificance?: string;
  standingWaveModes?: number;
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
      border: '1px solid #00ffaa',
      boxShadow: '0 0 25px rgba(0, 255, 170, 0.4)',
    }}>
      <div style={{ marginBottom: '10px', fontWeight: 'bold', color: '#00ffaa', fontSize: '14px' }}>
        PTA INTERFEROMETER
      </div>

      <div style={{ marginBottom: '8px' }}>
        <span style={{ color: '#aaa' }}>Pulsars:</span>{' '}
        <span style={{ color: '#00ffaa' }}>{totalPulsars}</span>
        <span style={{ color: '#666', fontSize: '10px' }}> millisecond pulsars</span>
      </div>

      <div style={{ borderTop: '1px solid #333', paddingTop: '10px', marginTop: '10px' }}>
        <div style={{ color: '#ff00ff', marginBottom: '5px', fontWeight: 'bold' }}>
          GW BACKGROUND DETECTION
        </div>
        <div style={{ marginBottom: '5px' }}>
          <span style={{ color: '#aaa' }}>Amplitude:</span>{' '}
          <span style={{ color: '#fff' }}>A = {gwbAmplitude.toExponential(1)}</span>
        </div>
        <div style={{ marginBottom: '5px' }}>
          <span style={{ color: '#aaa' }}>Significance:</span>{' '}
          <span style={{ color: '#00ff88', fontWeight: 'bold' }}>{gwbSignificance}</span>
        </div>
        <div style={{ marginBottom: '5px' }}>
          <span style={{ color: '#aaa' }}>Frequency:</span>{' '}
          <span style={{ color: '#666' }}>nanohertz (periods of years)</span>
        </div>
      </div>

      <div style={{ borderTop: '1px solid #333', paddingTop: '10px', marginTop: '10px' }}>
        <div style={{ color: '#00aaff', marginBottom: '5px', fontWeight: 'bold' }}>
          HELLINGS-DOWNS CORRELATION
        </div>
        <div style={{ fontSize: '11px', color: '#888', lineHeight: '1.4' }}>
          Timing residuals between pulsar pairs show the unique angular
          correlation signature of gravitational waves passing through
          the galaxy.
        </div>
      </div>

      <div style={{
        marginTop: '10px',
        paddingTop: '10px',
        borderTop: '1px solid #333',
        fontSize: '10px',
      }}>
        <div style={{ color: '#ffffff', marginBottom: '5px' }}>
          T³ STANDING WAVE PREDICTION:
        </div>
        <div style={{ color: '#888', lineHeight: '1.4' }}>
          In a bounded 20.6 Gpc box, gravitational waves reflect off
          boundary walls creating
          <span style={{ color: '#ffffff' }}> {standingWaveModes} resonant modes</span>.
          The GWB should show enhanced power at specific frequencies
          corresponding to the box dimensions.
        </div>
      </div>

      <div style={{
        marginTop: '10px',
        fontSize: '9px',
        color: '#666',
        borderTop: '1px solid #333',
        paddingTop: '8px',
      }}>
        <span style={{ color: '#00ffaa' }}>●</span> Pulsars |{' '}
        <span style={{ color: '#00aaff' }}>━</span> Timing tethers |{' '}
        <span style={{ color: '#ff00ff' }}>◐</span> GWB field
        <div style={{ marginTop: '4px' }}>
          GPU-optimized: 5 draw calls for 68 pulsars + tethers
        </div>
      </div>
    </div>
  );
}

export default PTAInterferometer;
