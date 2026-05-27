/**
 * =============================================================================
 * PTA INTERFEROMETER - NANOGrav Pulsar Timing Array Visualization
 * =============================================================================
 *
 * Renders the NANOGrav 15-year pulsar timing array as a galaxy-scale
 * gravitational wave detector, visualizing the gravitational wave background
 * (GWB) detected through Hellings-Downs correlations.
 *
 * Physics:
 * - 68 millisecond pulsars act as precise cosmic clocks
 * - GWB causes correlated timing residuals (nanosecond delays)
 * - Hellings-Downs correlation: unique signature of isotropic GWB
 * - In T³/Z₂ topology: GWB forms standing wave interference patterns
 *
 * Visualization:
 * - Pulsar positions at exact kiloparsec scale
 * - Pulsing laser tethers representing timing correlations
 * - Volumetric GWB field (spacetime ripples)
 * - Standing wave nodes from T³ boundary resonance
 *
 * =============================================================================
 */

import React, { useRef, useMemo, useEffect, useState } from 'react';
import * as THREE from 'three';
import { useFrame, extend } from '@react-three/fiber';
import { Line, shaderMaterial } from '@react-three/drei';

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
  const tetherRefs = useRef<THREE.Line[]>([]);

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

  // Animation - pulsing tethers and GWB ripples
  useFrame((state, delta) => {
    timeRef.current += delta;

    // Animate pulsar markers
    if (groupRef.current) {
      groupRef.current.children.forEach((child, i) => {
        if (child.userData.isPulsar) {
          const pulse = 1 + 0.3 * Math.sin(timeRef.current * 5 + i * 0.5);
          child.scale.setScalar(child.userData.baseScale * pulse);
        }
      });
    }
  });

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

  // Standing wave node planes
  const standingWaveNodes = useMemo(() => {
    if (!data?.standing_wave_modes) return [];

    const nodes: Array<{
      position: number;
      axis: 'x' | 'y' | 'z';
      mode: number;
    }> = [];

    // Only show first 3 modes to avoid clutter
    data.standing_wave_modes.slice(0, 3).forEach(mode => {
      mode.node_positions_gpc.forEach(pos => {
        ['x', 'y', 'z'].forEach(axis => {
          nodes.push({
            position: pos,
            axis: axis as 'x' | 'y' | 'z',
            mode: mode.mode,
          });
        });
      });
    });

    return nodes;
  }, [data]);

  if (!visible || loading || !data) return null;

  return (
    <group ref={groupRef}>
      {/* Pulsars */}
      {showPulsars && data.pulsars.map((pulsar, i) => {
        // Scale position for visibility (pulsars are very close to origin at cosmic scale)
        const pos = [
          pulsar.x_kpc * KPC_TO_GPC * PULSAR_VISUAL_SCALE,
          pulsar.y_kpc * KPC_TO_GPC * PULSAR_VISUAL_SCALE,
          pulsar.z_kpc * KPC_TO_GPC * PULSAR_VISUAL_SCALE,
        ] as [number, number, number];

        // Size based on timing precision (better timing = brighter)
        const baseSize = 0.02 * (1 - pulsar.timing_rms_ns / 600);

        return (
          <group key={pulsar.name}>
            {/* Pulsar core */}
            <mesh
              position={pos}
              userData={{ isPulsar: true, baseScale: baseSize }}
            >
              <sphereGeometry args={[baseSize, 12, 12]} />
              <meshBasicMaterial
                color="#00ffaa"
                transparent
                opacity={opacity}
              />
            </mesh>

            {/* Pulsar glow */}
            <mesh position={pos}>
              <sphereGeometry args={[baseSize * 2, 8, 8]} />
              <meshBasicMaterial
                color="#00ffaa"
                transparent
                opacity={0.2}
                blending={THREE.AdditiveBlending}
                depthWrite={false}
              />
            </mesh>

            {/* Radio beam cone (representing pulsar emission) */}
            <mesh
              position={pos}
              rotation={[Math.random() * Math.PI, Math.random() * Math.PI, 0]}
            >
              <coneGeometry args={[baseSize * 0.5, baseSize * 3, 8, 1, true]} />
              <meshBasicMaterial
                color="#00aaff"
                transparent
                opacity={0.15}
                side={THREE.DoubleSide}
              />
            </mesh>
          </group>
        );
      })}

      {/* Timing correlation tethers */}
      {showTethers && tethers.map((tether, i) => {
        const p1 = [
          tether.p1.x_kpc * KPC_TO_GPC * PULSAR_VISUAL_SCALE,
          tether.p1.y_kpc * KPC_TO_GPC * PULSAR_VISUAL_SCALE,
          tether.p1.z_kpc * KPC_TO_GPC * PULSAR_VISUAL_SCALE,
        ] as [number, number, number];

        const p2 = [
          tether.p2.x_kpc * KPC_TO_GPC * PULSAR_VISUAL_SCALE,
          tether.p2.y_kpc * KPC_TO_GPC * PULSAR_VISUAL_SCALE,
          tether.p2.z_kpc * KPC_TO_GPC * PULSAR_VISUAL_SCALE,
        ] as [number, number, number];

        return (
          <Line
            key={`tether-${i}`}
            points={[p1, p2]}
            color="#00aaff"
            lineWidth={1}
            transparent
            opacity={tether.strength * 0.3}
            dashed
            dashSize={0.01}
            gapSize={0.005}
          />
        );
      })}

      {/* Earth position marker */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[0.005, 16, 16]} />
        <meshBasicMaterial color="#ffff00" />
      </mesh>

      {/* GWB Field - volumetric representation (simplified as nested spheres) */}
      {showGWBField && (
        <group>
          {[0.5, 1.0, 1.5, 2.0].map((radius, i) => (
            <mesh key={`gwb-${i}`}>
              <sphereGeometry args={[radius, 32, 32]} />
              <meshBasicMaterial
                color="#ff00ff"
                transparent
                opacity={0.02 * Math.sin(timeRef.current * 0.5 + i)}
                side={THREE.DoubleSide}
                blending={THREE.AdditiveBlending}
                depthWrite={false}
              />
            </mesh>
          ))}
        </group>
      )}

      {/* Standing wave nodes - planes where GWB amplitude = 0 */}
      {showStandingWaves && standingWaveNodes.slice(0, 15).map((node, i) => {
        const rotation: [number, number, number] =
          node.axis === 'x' ? [0, Math.PI / 2, 0] :
          node.axis === 'y' ? [Math.PI / 2, 0, 0] :
          [0, 0, 0];

        const position: [number, number, number] =
          node.axis === 'x' ? [node.position, 0, 0] :
          node.axis === 'y' ? [0, node.position, 0] :
          [0, 0, node.position];

        // Only render if within visible range
        if (Math.abs(node.position) > 12) return null;

        return (
          <mesh key={`node-${i}`} position={position} rotation={rotation}>
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
        );
      })}

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
      </div>
    </div>
  );
}

export default PTAInterferometer;
